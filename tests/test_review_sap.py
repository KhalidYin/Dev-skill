import contextlib
import importlib.util
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "review-sap"
SCRIPTS = SKILL / "scripts"
sys.path.insert(0, str(SCRIPTS))


def _load(name):
    spec = importlib.util.spec_from_file_location(f"review_sap_{name}", SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


BUILDER = _load("build_issue_log")
ANNOTATE = _load("annotate_docx")
CHECKLIST = BUILDER.load_checklist()

REVIEW = {
    "review_id": "RV-001", "title": "Test review", "sap_document_id": "DOC-01",
    "review_date": "2026-11-03", "reviewer": "AI-assisted draft", "design_tags": ["rct"],
    "dimensions_in_scope": ["STR", "INT", "PRO", "PRG"],
    "checklist_version": str(CHECKLIST["checklist_version"]), "language": "en",
}
SAP_DOC = {"document_id": "DOC-01", "role": "sap", "title": "SAP", "version": "1.0"}
PROTOCOL_DOC = {"document_id": "DOC-02", "role": "protocol", "title": "Protocol", "version": "2.0"}
FINDING = {
    "finding_id": "F-001", "dimension": "PRO", "checklist_items": ["PRO-05", "INT-03"],
    "type": "inconsistency", "severity": "Critical", "sap_locator": "Sec 8.1",
    "sap_excerpt": "400 participants (200 per arm) will be randomized.",
    "comparator_source": "DOC-02", "comparator_locator": "Sec 10.1",
    "comparator_excerpt": "approximately 420 participants (210 per arm)",
    "issue": "Sample size differs.", "recommendation": "Align with Protocol.",
    "rationale": "Primary analysis power.", "confidence": "high", "verification": "self",
}


class ReviewSapBuilderTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.run_dir = Path(self.tmp.name) / "run"

    def add(self, record_type, value):
        return BUILDER.append_record(self.run_dir, record_type,
                                     json.dumps(value, ensure_ascii=False), CHECKLIST)

    def stage_valid_set(self, with_protocol=True, finding=True):
        self.add("review", REVIEW)
        self.add("document", SAP_DOC)
        roles = {"sap"}
        if with_protocol:
            self.add("document", PROTOCOL_DOC)
            roles.add("protocol")
        if finding:
            self.add("finding", FINDING)
        for item in BUILDER.applicable_items(CHECKLIST, REVIEW):
            linked = finding and item["id"] in FINDING["checklist_items"]
            if linked:
                rec = {"item_id": item["id"], "status": "finding",
                       "finding_ids": ["F-001"], "note": "See F-001"}
            elif set(item["requires"]) <= roles:
                rec = {"item_id": item["id"], "status": "pass", "note": "Sec 1 confirmed"}
            else:
                rec = {"item_id": item["id"], "status": "not-assessable",
                       "note": "Missing input"}
            self.add("coverage", rec)

    def check(self):
        return BUILDER.check_records(BUILDER.read_staged(self.run_dir), CHECKLIST)[0]

    def staged_text(self):
        path = BUILDER.staging_path(self.run_dir)
        return path.read_text(encoding="utf-8") if path.exists() else ""

    # --- record-level validation -------------------------------------------

    def test_invalid_json_does_not_touch_staging(self):
        self.add("review", REVIEW)
        before = self.staged_text()
        with self.assertRaises(BUILDER.RecordError):
            BUILDER.append_record(self.run_dir, "document", "{not json", CHECKLIST)
        self.assertEqual(before, self.staged_text())

    def test_unknown_field_rejected(self):
        with self.assertRaises(BUILDER.RecordError):
            self.add("document", {**SAP_DOC, "query_id": "x"})

    def test_pro_finding_requires_comparator_evidence(self):
        bad = {**FINDING, "comparator_excerpt": ""}
        with self.assertRaisesRegex(BUILDER.RecordError, "comparator"):
            self.add("finding", bad)

    def test_low_confidence_cannot_be_critical(self):
        with self.assertRaisesRegex(BUILDER.RecordError, "low-confidence"):
            self.add("finding", {**FINDING, "confidence": "low"})

    def test_suggestion_cannot_be_major(self):
        bad = {**FINDING, "dimension": "STR", "type": "suggestion", "severity": "Major",
               "checklist_items": ["STR-20"]}
        with self.assertRaisesRegex(BUILDER.RecordError, "suggestion"):
            self.add("finding", bad)

    def test_out_of_scope_observation_shape(self):
        ok = {**FINDING, "finding_id": "F-009", "dimension": "MTH", "type": "out-of-scope-observation",
              "severity": "n/a", "checklist_items": [], "comparator_source": "",
              "comparator_locator": "", "comparator_excerpt": ""}
        self.add("finding", ok)
        with self.assertRaises(BUILDER.RecordError):
            self.add("finding", {**ok, "finding_id": "F-010", "severity": "Minor"})

    def test_unknown_checklist_item_rejected(self):
        with self.assertRaisesRegex(BUILDER.RecordError, "not in checklist"):
            self.add("finding", {**FINDING, "checklist_items": ["PRO-99"]})

    def test_checklist_version_must_match(self):
        with self.assertRaisesRegex(BUILDER.RecordError, "checklist_version"):
            self.add("review", {**REVIEW, "checklist_version": "9.9.9"})

    def test_duplicate_ids_and_second_review_rejected(self):
        self.add("review", REVIEW)
        self.add("document", SAP_DOC)
        with self.assertRaisesRegex(BUILDER.RecordError, "Duplicate"):
            self.add("document", SAP_DOC)
        with self.assertRaisesRegex(BUILDER.RecordError, "already staged"):
            self.add("review", {**REVIEW, "review_id": "RV-002"})

    # --- cross-record checks -----------------------------------------------

    def test_valid_set_passes_check(self):
        self.stage_valid_set()
        self.assertEqual([], self.check())

    def test_missing_coverage_is_reported(self):
        self.add("review", REVIEW)
        self.add("document", SAP_DOC)
        errors = self.check()
        self.assertTrue(any("Missing coverage for applicable item STR-01" in e for e in errors))

    def test_protocol_item_cannot_pass_without_protocol(self):
        self.add("review", REVIEW)
        self.add("document", SAP_DOC)
        for item in BUILDER.applicable_items(CHECKLIST, REVIEW):
            self.add("coverage", {"item_id": item["id"], "status": "pass", "note": "Sec 1"})
        errors = self.check()
        self.assertTrue(any(e.startswith("PRO-02 needs ['protocol']") for e in errors))

    def test_without_protocol_not_assessable_passes(self):
        self.stage_valid_set(with_protocol=False, finding=False)
        self.assertEqual([], self.check())

    def test_finding_must_be_linked_from_coverage(self):
        self.add("review", REVIEW)
        self.add("document", SAP_DOC)
        self.add("document", PROTOCOL_DOC)
        self.add("finding", FINDING)
        for item in BUILDER.applicable_items(CHECKLIST, REVIEW):
            note = {"item_id": item["id"], "status": "pass", "note": "Sec 1"}
            if item["requires"] == ["sap", "crf"] or "tfl_shells" in item["requires"]:
                note = {"item_id": item["id"], "status": "not-assessable", "note": "Missing"}
            self.add("coverage", note)
        errors = self.check()
        self.assertTrue(any("F-001 lists PRO-05" in e for e in errors))
        self.assertTrue(any("F-001 is not referenced" in e for e in errors))

    # --- workbook -------------------------------------------------------------

    def test_build_writes_expected_workbook_and_refuses_overwrite(self):
        import openpyxl

        self.stage_valid_set()
        out = Path(self.tmp.name) / "log.xlsx"
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(0, BUILDER.main(["build", "--run-dir", str(self.run_dir), "--out", str(out)]))
            self.assertEqual(1, BUILDER.main(["build", "--run-dir", str(self.run_dir), "--out", str(out)]))
        wb = openpyxl.load_workbook(out)
        self.assertEqual(["Read Me", "Summary", "Findings", "Checklist Coverage",
                          "Protocol-SAP Crosswalk", "Documents", "Basis"], wb.sheetnames)
        findings = wb["Findings"]
        self.assertEqual("F-001", findings["A2"].value)
        self.assertEqual("Open", findings["P2"].value)
        self.assertTrue(str(wb["Summary"]["B3"].value).startswith("=COUNTIFS("))
        coverage_ids = [r[0].value for r in wb["Checklist Coverage"].iter_rows(min_row=2)]
        self.assertIn("STR-EP-01", coverage_ids)  # non-applicable items are listed too

    def test_build_refuses_when_check_fails(self):
        self.add("review", REVIEW)
        self.add("document", SAP_DOC)
        out = Path(self.tmp.name) / "log.xlsx"
        with contextlib.redirect_stdout(io.StringIO()):
            rc = BUILDER.main(["build", "--run-dir", str(self.run_dir), "--out", str(out)])
        self.assertEqual(1, rc)
        self.assertFalse(out.exists())

    # --- docx comments ----------------------------------------------------------

    def _make_sap_docx(self, path):
        import docx

        d = docx.Document()
        d.add_heading("8 Sample Size", level=1)
        d.add_paragraph("8.1 Sample size")
        d.add_paragraph("With 20% dropout, 400 participants (200 per arm) will be randomized.")
        d.save(path)

    def test_annotate_requires_confirmation_and_writes_copy(self):
        import docx

        self.stage_valid_set()
        sap = Path(self.tmp.name) / "sap.docx"
        out = Path(self.tmp.name) / "sap_reviewed.docx"
        self._make_sap_docx(sap)
        original = sap.read_bytes()
        with contextlib.redirect_stdout(io.StringIO()):
            rc = ANNOTATE.main(["--run-dir", str(self.run_dir), "--sap", str(sap), "--out", str(out)])
        self.assertEqual(2, rc)
        self.assertFalse(out.exists())
        with contextlib.redirect_stdout(io.StringIO()):
            rc = ANNOTATE.main(["--run-dir", str(self.run_dir), "--sap", str(sap),
                                "--out", str(out), "--confirmed"])
        self.assertEqual(0, rc)
        self.assertEqual(original, sap.read_bytes())
        comments = list(docx.Document(str(out)).comments)
        self.assertEqual(1, len(comments))
        self.assertIn("F-001", comments[0].text)
        with contextlib.redirect_stdout(io.StringIO()):
            rc = ANNOTATE.main(["--run-dir", str(self.run_dir), "--sap", str(sap),
                                "--out", str(sap), "--confirmed"])
        self.assertEqual(1, rc)


class ReviewSapChecklistTests(unittest.TestCase):
    def test_checklist_integrity(self):
        items = CHECKLIST["items"]
        ids = [i["id"] for i in items]
        self.assertEqual(len(ids), len(set(ids)), "duplicate checklist ids")
        basis_ids = {b["id"] for b in CHECKLIST["basis_register"]}
        roles = set(BUILDER.DOC_ROLES)
        for item in items:
            self.assertIn(item["dimension"], BUILDER.DIMENSIONS, item["id"])
            self.assertTrue(item["id"].startswith(item["dimension"] + "-"), item["id"])
            self.assertTrue(set(item["applies_to"]) <= set(CHECKLIST["design_tags"]), item["id"])
            self.assertTrue(set(item["requires"]) <= roles, item["id"])
            self.assertIn("sap", item["requires"], item["id"])
            self.assertIn(item["severity_hint"], BUILDER.SEVERITIES[:-1], item["id"])
            for b in item["basis"]:
                self.assertIn(b["id"], basis_ids, item["id"])

    def test_basis_register_matches_reference_doc(self):
        text = (SKILL / "references" / "checklist-basis.md").read_text(encoding="utf-8")
        for b in CHECKLIST["basis_register"]:
            self.assertIn(f"| {b['id']} |", text)

    def test_answer_key_items_exist(self):
        key = yaml.safe_load((SKILL / "evals" / "files" / "seeded-answer-key.yaml").read_text(encoding="utf-8"))
        known = {i["id"] for i in CHECKLIST["items"]}
        for defect in key["defects"]:
            self.assertTrue(set(defect["expected_items"]) <= known, defect["id"])

    def test_seeded_fixture_differs_from_clean_only_by_defects(self):
        files = SKILL / "evals" / "files"
        clean = (files / "sap-clean.md").read_text(encoding="utf-8")
        seeded = (files / "sap-seeded.md").read_text(encoding="utf-8")
        self.assertIn("400 participants (200 per arm)", seeded)
        self.assertNotIn("400 participants (200 per arm)", clean)
        self.assertIn("Week 16 = Days 92-126", seeded)
        self.assertIn("Sensitivity analysis 2 (tipping point) is added", seeded)  # decoy kept


if __name__ == "__main__":
    unittest.main()
