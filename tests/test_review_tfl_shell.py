"""Mechanical contracts; these tests do not grade clinical review decisions."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import yaml
from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "review-tfl-shell"
SCRIPT = SKILL / "scripts" / "build_issue_log.py"
SPEC = importlib.util.spec_from_file_location("tfl_review_builder", SCRIPT)
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)
CORE = yaml.safe_load(builder.CHECKLIST.read_text(encoding="utf-8"))


def ev(doc, locator="§1", text="Synthetic contract-test evidence"):
    return {"doc_id": doc, "locator": locator, "text": text}


def fixture(design="randomized"):
    bundle = {
        "review": {"title": "Synthetic review", "date": "2026-11-06", "checklist_version": "0.1.0",
                   "study_context": design, "scope": "Synthetic T/F/L", "limitations": "No rendered pages"},
        "documents": [{"id": ident, "role": role, "title": role, "version": "1", "date": "2026-10-01",
                       "location": f"/synthetic/{role}.md"}
                      for ident, role in [("S", "shell"), ("P", "sap"), ("C", "external-spec")]],
        "analyses": [{"id": "A1", "document_id": "P", "title": "Prespecified analysis", "locator": "§1"}],
        "shells": [{"id": kind + "1", "document_id": "S", "type": kind, "title": kind,
                    "locator": kind + "1", "analysis_ids": ["A1"]} for kind in "TFL"],
        "findings": [], "checks": [],
    }
    fill_checks(bundle)
    return bundle


def fill_checks(bundle):
    checklist = builder.extend_checklist(bundle, CORE)
    _, docs, shells, analyses = builder.intake(bundle, checklist)
    bundle["checks"] = [
        {"target_id": tid, "item_id": item["id"], "status": "not-assessable",
         "note": "Mechanical test: professional check not performed"}
        for tid, item, state, _ in builder.plan_checks(docs, shells, analyses, checklist) if state == "review"
    ]


def review_check(bundle, target, item):
    return next(c for c in bundle["checks"] if (c["target_id"], c["item_id"]) == (target, item))


def finding(bundle, targets=("T1",)):
    bundle["findings"] = [{
        "id": "F001", "target_ids": list(targets), "type": "inconsistency", "priority": "Major",
        "confidence": "high", "comment": "Correct the denominator to the prespecified population.",
        "rationale": "Excluding unevaluable participants changes the response proportion.",
        "evidence": [ev("S", target + " note a", "Evaluable population denominator") for target in targets]
                    + [ev("P", "§1", "All-treated denominator")],
    }]
    for target in targets:
        row = review_check(bundle, target, "NOTE-02")
        row.update(status="finding", note="Denominator mismatch", finding_ids=["F001"])


def validate(bundle):
    checklist = builder.extend_checklist(bundle, CORE)
    _, docs, shells, analyses = builder.intake(bundle, checklist)
    return builder.validate(bundle, docs, shells, analyses, list(builder.plan_checks(docs, shells, analyses, checklist)))


class ReviewTflShellTests(unittest.TestCase):
    def cli(self, *args):
        return subprocess.run([sys.executable, "-X", "utf8", str(SCRIPT), *map(str, args)],
                              capture_output=True, encoding="utf-8")

    def test_three_design_cli_workbooks_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            for design in ("randomized", "single-arm", "dose-escalation"):
                with self.subTest(design=design):
                    bundle = fixture(design)
                    finding(bundle)
                    bundle["findings"][0]["comment"] = '=literal source text, not a formula'
                    source, output = folder / f"{design}.json", folder / f"{design}.xlsx"
                    source.write_text(json.dumps(bundle, ensure_ascii=False), encoding="utf-8")
                    original = source.read_bytes()
                    for command in ("plan", "check", "build"):
                        args = [command, "--input", source]
                        if command == "build":
                            args += ["--out", output]
                        result = self.cli(*args)
                        self.assertEqual(result.returncode, 0, result.stderr)
                    wb = load_workbook(output)
                    self.assertEqual(wb.sheetnames, ["Overview", "Comments", "SAP-TFL Crosswalk"])
                    self.assertEqual(wb["Comments"].max_column, 9)
                    self.assertEqual(wb["Comments"]["D2"].data_type, "s")
                    self.assertEqual(wb["Comments"]["D2"].value, bundle["findings"][0]["comment"])
                    self.assertIn("§1", wb["Comments"]["F2"].value)
                    self.assertEqual(len(wb["Comments"].data_validations.dataValidation), 1)
                    self.assertEqual(sum(c.data_type == "f" for row in wb["Overview"] for c in row), 8)
                    wb.close()
                    before = output.read_bytes()
                    self.assertNotEqual(self.cli("build", "--input", source, "--out", output).returncode, 0)
                    self.assertEqual(before, output.read_bytes())
                    self.assertEqual(original, source.read_bytes())

    def test_evidence_and_actionable_comment_required(self):
        for field in ("comment", "rationale", "evidence"):
            bundle = fixture()
            finding(bundle)
            del bundle["findings"][0][field]
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate(bundle)
        bundle = fixture()
        finding(bundle)
        bundle["findings"][0]["evidence"] = [ev("S")]
        with self.assertRaisesRegex(ValueError, "two evidence"):
            validate(bundle)

    def test_missing_duplicate_and_orphan_coverage_rejected(self):
        for mutation in ("missing", "duplicate", "orphan", "unknown-link"):
            bundle = fixture()
            finding(bundle)
            if mutation == "missing":
                bundle["checks"].pop()
            elif mutation == "duplicate":
                bundle["checks"].append(copy.deepcopy(bundle["checks"][0]))
            elif mutation == "orphan":
                review_check(bundle, "T1", "NOTE-02").update(status="not-assessable", finding_ids=[])
            else:
                review_check(bundle, "T1", "NOTE-02")["finding_ids"] = ["NO-SUCH-FINDING"]
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                validate(bundle)

    def test_shared_issue_one_comment_multiple_targets(self):
        bundle = fixture()
        finding(bundle, ("T1", "L1"))
        findings, _ = validate(bundle)
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings["F001"]["target_ids"], ["T1", "L1"])

    def test_shell_only_cannot_claim_sap_or_collection_pass(self):
        bundle = fixture()
        bundle["documents"] = bundle["documents"][:1]
        bundle["analyses"] = []
        for shell in bundle["shells"]:
            shell["analysis_ids"] = []
        fill_checks(bundle)
        validate(bundle)
        for item in ("ANA-01", "DATA-01"):
            candidate = copy.deepcopy(bundle)
            candidate["checks"].append({"target_id": "T1", "item_id": item, "status": "pass",
                                        "note": "Unsupported claim", "evidence": [ev("S")]})
            with self.subTest(item=item), self.assertRaisesRegex(ValueError, "automatic"):
                validate(candidate)

    def test_pass_requires_evidence_and_analysis_mapping(self):
        bundle = fixture()
        row = review_check(bundle, "A1", "MAP-01")
        row.update(status="pass", note="Analysis mapped")
        with self.assertRaisesRegex(ValueError, "evidence"):
            validate(bundle)
        row["evidence"] = [ev("P"), ev("S", "T1")]
        validate(bundle)
        for shell in bundle["shells"]:
            shell["analysis_ids"] = []
        with self.assertRaisesRegex(ValueError, "mapped shell"):
            validate(bundle)

    def test_global_convention_and_external_derived_support_can_pass(self):
        bundle = fixture("single-arm")
        bundle["documents"].append({"id": "G", "role": "convention", "title": "Global conventions",
                                    "version": "1", "date": "2026-10-01", "location": "/global.md"})
        review_check(bundle, "T1", "NOTE-02").update(
            status="pass", note="Explicit global rule applies to the whole table",
            evidence=[ev("G", "G1", "All T1 percentages use the treated population"), ev("S", "T1", "See G1")])
        review_check(bundle, "L1", "DATA-01").update(
            status="pass", note="Duration supported by collected dates and the specified derivation",
            evidence=[ev("C", "Fields", "Start and end dates, precision day"),
                      ev("P", "Derivation", "Duration = end - start + 1"), ev("S", "L1", "Duration (days)")])
        validate(bundle)

    def test_ambiguity_requires_different_readings(self):
        bundle = fixture()
        finding(bundle)
        row = bundle["findings"][0]
        row["type"] = "ambiguity"
        with self.assertRaisesRegex(ValueError, "reading_a"):
            validate(bundle)
        row.update(reading_a="Subject count", reading_b="Subject count")
        with self.assertRaisesRegex(ValueError, "readings must differ"):
            validate(bundle)
        row["reading_b"] = "Event count"
        validate(bundle)

    def test_custom_checks_and_optional_details(self):
        bundle = fixture("dose-escalation")
        bundle["extra_checks"] = [{"id": "X-DLT", "group": "Study-specific", "target": "T",
                                    "sap_required": True, "check": "DLT window and decision summary"}]
        fill_checks(bundle)
        self.assertEqual(sum(c["item_id"] == "X-DLT" for c in bundle["checks"]), 1)
        checklist = builder.extend_checklist(bundle, CORE)
        review, docs, shells, analyses = builder.intake(bundle, checklist)
        plan = list(builder.plan_checks(docs, shells, analyses, checklist))
        findings, checks = builder.validate(bundle, docs, shells, analyses, plan)
        wb = builder.build(bundle, checklist, review, docs, shells, analyses, plan, findings, checks, True)
        self.assertEqual(wb.sheetnames[-1], "Check Details")
        self.assertIn("X-DLT", [row[1].value for row in wb["Check Details"]])
        wb.close()
        bundle["extra_checks"].append(copy.deepcopy(bundle["extra_checks"][0]))
        with self.assertRaisesRegex(ValueError, "unique X-"):
            builder.extend_checklist(bundle, CORE)

    def test_invalid_inventory_rejected(self):
        for mutation in ("unknown-analysis", "duplicate-shell", "empty-shell", "sap-without-inventory", "version"):
            bundle = fixture()
            if mutation == "unknown-analysis":
                bundle["shells"][0]["analysis_ids"] = ["A999"]
            elif mutation == "duplicate-shell":
                bundle["shells"].append(copy.deepcopy(bundle["shells"][0]))
            elif mutation == "empty-shell":
                bundle["shells"] = []
            elif mutation == "version":
                bundle["review"]["checklist_version"] = "bad"
            else:
                bundle["analyses"] = []
                for shell in bundle["shells"]:
                    shell["analysis_ids"] = []
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                validate(bundle)


if __name__ == "__main__":
    unittest.main()
