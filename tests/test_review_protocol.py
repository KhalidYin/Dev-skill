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

ROOT = Path(__file__).resolve().parents[1] / "review-protocol"
SCRIPT = ROOT / "scripts" / "build_issue_log.py"
SPEC = importlib.util.spec_from_file_location("protocol_issue_log", SCRIPT)
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)
CHECKLIST = yaml.safe_load(builder.CHECKLIST.read_text(encoding="utf-8"))


def unit(unit_id, scope, title, purpose, comparison, structure, inference, locator, *tags):
    return dict(
        id=unit_id, scope=scope, title=title, purpose=purpose, comparison=comparison,
        structure=structure, inference=inference, locator=locator, tags=list(tags),
        uncertain_tags=[], scope_note="Synthetic protocol excerpt",
    )


RCT = unit("R", "whole", "Randomized", "Comparative efficacy", "Randomized placebo control",
           "Parallel", "Assigned-treatment comparison", "§1, §3 and §10", "randomized", "blinded", "estimand")
SINGLE = unit("S", "whole", "Single-arm", "Response", "Fixed benchmark",
              "Two-stage", "Formal benchmark test", "§1 and §10", "single-arm", "benchmark", "multistage")
SHARED = unit("STUDY", "shared", "Study-wide", "Safety and exploration", "No shared comparison",
              "Multipart", "Shared safety summary", "§1 and §10")
ESC = unit("A", "part", "Part A", "Dose escalation", "Noncomparative cohorts", "Sequential cohorts",
           "Dose assignment using posterior probability", "§4.1 and Appendix A",
           "dose-escalation", "bayesian", "specialist")
EXP = unit("B", "part", "Part B", "Estimate response", "Noncomparative cohorts", "Two expansion cohorts",
           "Descriptive estimation", "§4.2 and §10", "dose-expansion", "multi-cohort", "single-arm")


def make_bundle(*units):
    bundle = {
        "review": {
            "title": "合成方案审核", "date": "2026-11-04", "protocol_id": "DOC-1",
            "checklist_version": CHECKLIST["checklist_version"], "input_scope": "excerpt",
            "retrieval_status": "unavailable", "retrieval_note": "Offline fixture",
        },
        "documents": [
            {"id": "DOC-1", "role": "protocol", "title": "Synthetic protocol", "version": "1.0",
             "date": "unknown", "location": "fixture.md"},
        ],
        "units": copy.deepcopy(list(units)),
        "sources": [],
        "crosswalk": [
            {"unit_id": u["id"], "parameter": "Inference", "value": u["inference"], "locator": u["locator"],
             "assessment": "observed"} for u in units
        ],
        "findings": [],
        "coverage": [],
        "analyses": [
            {"id": f"AN-{u['id']}", "unit_id": u["id"], "title": u["inference"], "locator": u["locator"],
             "role": "decision" if u["id"] == "A" else "primary"}
            for u in units if u["scope"] != "shared"
        ],
        "analysis_matrix": [],
    }
    for uid, item, state, _ in get_plan(bundle):
        if state == "review":
            bundle["coverage"].append(dict(unit_id=uid, item_id=item["id"], status="not-assessable",
                                           note="This smoke test checks only the seeded evidence links."))
    _, _, review_units = builder.get_scope(bundle, CHECKLIST)
    _, slots = builder.analysis_plan(bundle, CHECKLIST, review_units)
    for analysis, requirements in slots.items():
        for slot in requirements:
            bundle["analysis_matrix"].append(dict(analysis_id=analysis, slot=slot, status="not-assessable",
                                                  note="Outside the seeded evidence for this smoke test."))
    return bundle


def get_plan(bundle):
    _, docs, units = builder.get_scope(bundle, CHECKLIST)
    return list(builder.plan_checks(units, docs, CHECKLIST))


def add_finding(bundle, uid, item, locators, excerpts, *, kind="inconsistency", severity="Major"):
    finding_id = f"F-{len(bundle['findings']) + 1}"
    row = dict(id=finding_id, unit_id=uid, item_ids=[item], type=kind, severity=severity,
               confidence="high", locator=locators[0], evidence=excerpts[0],
               comment="Confirm the governing rule and reconcile the stated decision.", rationale="Changes the decision.")
    if locators[1]:
        row.update(other_doc_id="DOC-1", other_locator=locators[1], other_evidence=excerpts[1])
    bundle["findings"].append(row)
    target = next(r for r in bundle["coverage"] if (r["unit_id"], r["item_id"]) == (uid, item))
    target.update(status="finding", finding_ids=[finding_id], note="See linked evidence")
    return row


class ReviewProtocolTests(unittest.TestCase):
    def validate(self, bundle):
        _, docs, units = builder.get_scope(bundle, CHECKLIST)
        return builder.validate(bundle, CHECKLIST, docs, units, get_plan(bundle))

    def test_three_design_routes_through_workbook(self):
        cases = [
            ((RCT,), "randomized", ("R", "DAT-02"), ("§3", "§7"),
             ("Results are to reflect the assigned treatment regardless of discontinuation.",
              "Participants who discontinue treatment do not receive any further Score S assessment."),
             {("R", "RND-01"): "review", ("R", "SGL-01"): "not-applicable"}),
            ((SINGLE,), "single-arm", ("S", "SEQ-01"), ("§1", "§10"),
             ("Enrollment continues to Stage 2 if at least four responses are observed.",
              "Enrollment continues to a total of 30 if at least three responses are observed"),
             {("S", "BMK-01"): "review", ("S", "RND-01"): "not-applicable", ("S", "EXT-01"): "not-applicable"}),
            ((SHARED, ESC, EXP), "escalation-expansion", ("A", "ESC-01"), ("§4.1", "§7"),
             ("Dose-limiting toxicity (DLT) is evaluated through Day 28",
              "Part A DLT surveillance stops after the Day 21 visit."),
             {("A", "BAY-01"): "review", ("A", "EXP-01"): "not-applicable",
              ("B", "ESC-01"): "not-applicable", ("B", "EXP-01"): "review", ("B", "BMK-01"): "not-applicable"}),
        ]
        for units, fixture, issue, locators, excerpts, expected_routes in cases:
            with self.subTest(fixture=fixture), tempfile.TemporaryDirectory() as temp:
                source = (ROOT / "evals" / "files" / f"{fixture}.md").read_text(encoding="utf-8")
                for excerpt in excerpts:
                    self.assertIn(excerpt, source)
                bundle = make_bundle(*units)
                add_finding(bundle, *issue, locators, excerpts)
                if fixture == "escalation-expansion":
                    evidence = "The protocol provides no exchangeability assessment."
                    self.assertIn(evidence, source)
                    add_finding(bundle, "A", "SPC-01", ("Appendix A", ""), (evidence, ""),
                                kind="statistician-review", severity="")
                bundle["findings"][0]["comment"] = "=2+2"
                inp, out = Path(temp) / "review.json", Path(temp) / "issues.xlsx"
                inp.write_text(json.dumps(bundle, ensure_ascii=False), encoding="utf-8")
                for command in ("plan", "check", "build"):
                    args = [sys.executable, str(SCRIPT), command, "--input", str(inp)]
                    if command == "build":
                        args += ["--out", str(out)]
                    process = subprocess.run(args, capture_output=True, text=True, encoding="utf-8")
                    self.assertEqual(process.returncode, 0, process.stderr)
                workbook = load_workbook(out)
                self.assertEqual(workbook.sheetnames, ["Overview", "Comments", "Coverage", "Analysis Matrix"])
                routes = {(uid, item["id"]): state for uid, item, state, _ in get_plan(bundle)}
                for pair, status in expected_routes.items():
                    self.assertEqual(routes[pair], status)
                self.assertEqual(routes[(units[0]["id"], "VER-03")], "not-assessable")
                self.assertIn(excerpts[0], workbook["Comments"]["F2"].value)
                self.assertIn(excerpts[1], workbook["Comments"]["F2"].value)
                self.assertEqual(workbook["Comments"]["D2"].data_type, "s")
                self.assertEqual(workbook["Comments"]["D2"].value, "=2+2")
                self.assertEqual(workbook["Comments"].max_column, 9)
                self.assertIn("chapter", {row[1] for row in workbook["Coverage"].values})
                self.assertIn("f", {row[1].data_type for row in workbook["Overview"]})
                workbook.close()
                before = out.read_bytes()
                retry = subprocess.run(args, capture_output=True)
                self.assertNotEqual(retry.returncode, 0)
                self.assertEqual(out.read_bytes(), before)
                expanded = Path(temp) / "details.xlsx"
                extra = subprocess.run(args[:-1] + [str(expanded), "--details"], capture_output=True)
                self.assertEqual(extra.returncode, 0, extra.stderr)
                workbook = load_workbook(expanded)
                self.assertEqual(workbook.sheetnames[-1], "Traceability")
                workbook.close()

    def test_uncertain_tag_and_absent_sap_are_local(self):
        changed = copy.deepcopy(SINGLE)
        changed["tags"].remove("multistage")
        changed["uncertain_tags"] = ["multistage"]
        bundle = make_bundle(changed)
        route = {item["id"]: (state, reason) for _, item, state, reason in get_plan(bundle)}
        self.assertEqual(route["SEQ-01"], ("not-assessable", "Uncertain design: multistage"))
        self.assertEqual(route["VER-03"], ("not-assessable", "Missing document: sap"))
        self.assertEqual(route["OBJ-01"][0], "review")
        self.validate(bundle)

    def test_blocks_missing_coverage_and_unlinked_finding(self):
        bundle = make_bundle(RCT)
        bundle["coverage"].pop()
        with self.assertRaisesRegex(ValueError, "Missing coverage"):
            self.validate(bundle)
        bundle = make_bundle(RCT)
        finding = add_finding(bundle, "R", "DAT-02", ("§3", "§7"), ("commitment", "schedule"))
        finding["item_ids"].append("DAT-01")
        with self.assertRaisesRegex(ValueError, "missing reverse coverage"):
            self.validate(bundle)

    def test_blocks_bad_critical_evidence_and_precedent_as_basis(self):
        bundle = make_bundle(RCT)
        finding = add_finding(bundle, "R", "DAT-02", ("§3", "§7"), ("commitment", "schedule"),
                              severity="Critical")
        finding["confidence"] = "low"
        with self.assertRaisesRegex(ValueError, "low-confidence Critical"):
            self.validate(bundle)
        finding["confidence"] = "high"
        finding["other_locator"] = "§3"
        with self.assertRaisesRegex(ValueError, "two distinct locators"):
            self.validate(bundle)
        finding["other_locator"] = "§7"
        bundle["sources"] = [dict(id="P-01", kind="public-precedent", title="Example",
                                  url="https://example.org/protocol", status="published", version="1",
                                  region="US", checked_date="2026-11-04", locator="§1",
                                  document_type="protocol", relevance="Comparable", limits="Different population")]
        finding.update(basis_id="P-01", basis_locator="§1")
        with self.assertRaisesRegex(ValueError, "precedent cannot serve"):
            self.validate(bundle)

    def test_all_checklist_references_resolve(self):
        item_ids = set()
        basis_ids = {row["id"] for row in CHECKLIST["basis_register"]}
        tags = set(CHECKLIST["design_tags"])
        for item in CHECKLIST["items"]:
            self.assertNotIn(item["id"], item_ids)
            item_ids.add(item["id"])
            self.assertTrue(set(item["basis"]) <= basis_ids)
            self.assertTrue(set(item.get("any_tags", [])) <= tags)
            self.assertTrue(set(item.get("requires", [])) <= builder.ROLES)

    def test_chapter_and_analysis_link_to_one_comment_and_sap_detail(self):
        bundle = make_bundle(SINGLE)
        finding = add_finding(bundle, "S", "CH-04", ("§1", "§10"), ("at least four", "at least three"))
        finding["analysis_ids"] = ["AN-S"]
        stage = next(row for row in bundle["analysis_matrix"] if row["slot"] == "stage-boundaries")
        stage.update(status="finding", finding_ids=[finding["id"]], note="Different continuation boundaries.")
        method = next(row for row in bundle["analysis_matrix"] if row["slot"] == "method")
        method.update(status="sap-detail", locator="§10", value="Binomial response estimation",
                      note="SAP to specify exact interval implementation.")
        self.validate(bundle)
        del method["locator"]
        with self.assertRaisesRegex(ValueError, "analysis value and locator required"):
            self.validate(bundle)
        method["locator"] = "§10"
        fit = next(row for row in bundle["analysis_matrix"] if row["slot"] == "method-fit")
        fit["status"] = "sap-detail"
        with self.assertRaisesRegex(ValueError, "method fit requires a review conclusion"):
            self.validate(bundle)
        fit["status"] = "not-assessable"
        bundle["analysis_matrix"].remove(stage)
        with self.assertRaisesRegex(ValueError, "Missing analysis matrix.*stage-boundaries"):
            self.validate(bundle)

    def test_ambiguity_and_method_mismatch_require_specific_evidence(self):
        bundle = make_bundle(SINGLE)
        finding = add_finding(bundle, "S", "SGL-01", ("§3", ""), ("response-evaluable", ""),
                              kind="ambiguity")
        with self.assertRaisesRegex(ValueError, "two plausible readings"):
            self.validate(bundle)
        finding.update(reading_a="All treated patients", reading_b="Only patients with a scan")
        self.validate(bundle)
        del finding["rationale"]
        with self.assertRaisesRegex(ValueError, "missing text field rationale"):
            self.validate(bundle)
        finding.update(type="method-mismatch", rationale="The planned method cannot use the available data.")
        with self.assertRaisesRegex(ValueError, "method mismatch needs comparator evidence"):
            self.validate(bundle)
        finding.update(other_doc_id="DOC-1", other_locator="§7", other_evidence="No postbaseline assessment.")
        self.validate(bundle)


if __name__ == "__main__":
    unittest.main()
