from __future__ import annotations

import copy
import importlib.util
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "generate-sap" / "scripts" / "validate_output_contract.py"
SPEC = importlib.util.spec_from_file_location("generate_sap_output_contract", VALIDATOR_PATH)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


def generic_draft(extra: str = "") -> str:
    headings = [
        f"## {number}. {title}"
        for number, title in enumerate(VALIDATOR.EXPECTED_SECTIONS, start=1)
    ]
    return "# Statistical Analysis Plan\n\n" + "\n\n".join(headings) + f"\n\n{extra}\n"


def valid_ledger() -> dict:
    sections = [
        {
            "section_id": f"SEC-{number:02d}",
            "status": "complete" if number == 5 else "tbd",
            "content_ids": ["SAP-05-001"] if number == 5 else [],
            "query_ids": [],
        }
        for number in range(1, 19)
    ]
    return {
        "schema_version": "0.1",
        "document": {
            "title": "SAP for TARGET-STUDY-001",
            "status": "review-draft",
            "template": "generic",
            "source_versions": [
                {
                    "source_id": "SRC-CURRENT-001",
                    "label": "TARGET-STUDY-001",
                    "title": "Current Protocol for TARGET-STUDY-001",
                    "version": "1.0",
                    "date": "2026-01-01",
                }
            ],
        },
        "section_status": sections,
        "content_units": [
            {
                "content_id": "SAP-05-001",
                "section_id": "SEC-05",
                "topic": "governing-protocol",
                "generation_mode": "sourced",
                "status": "complete",
                "source_facts": [
                    {
                        "fact_id": "FACT-001",
                        "source_id": "SRC-CURRENT-001",
                        "locator": "Protocol section 1",
                        "summary": "The current study identifier is TARGET-STUDY-001.",
                    }
                ],
                "applied_rules": [],
                "assumptions": [],
                "derivation_summary": "Current Protocol fact transcribed.",
                "alternatives": [],
                "references": [],
                "generated_content": {
                    "paragraph_id": "SAP-05-P1",
                    "text": "TARGET-STUDY-001 is governed by the supplied Protocol.",
                },
                "open_questions": [],
                "downstream_sections": [],
            }
        ],
        "open_questions": [],
        "references": [],
        "consistency_findings": [],
        "search_summary": {
            "status": "prohibited",
            "queries_run": [],
            "repositories_checked": [],
            "candidates_found": 0,
            "shortlisted": 0,
            "deeply_reviewed": 0,
            "stop_reason": "External research was prohibited for this run.",
            "limitations": ["No external precedent research was performed."],
        },
    }


def generic_reference(**overrides: object) -> dict:
    record = {
        "reference_id": "REF-001",
        "reference_type": "normative_reference",
        "title": "External guidance",
        "authors_or_organization": "Regulatory organization",
        "document_type": "guidance",
        "version": "1.0",
        "date": "2025-01-01",
        "status": "effective",
        "direct_url": "https://example.org/guidance.pdf",
        "retrieved_date": "2026-08-27",
        "location": {"section": "2", "page": 10},
        "supported_summary": "External methodological context.",
        "limitations": [],
    }
    record.update(overrides)
    return record


def nested_precedent() -> dict:
    return {
        "reference_id": "PRECEDENT-001",
        "reference_type": "trial_precedent",
        "study": {
            "title": "Comparable study",
            "registry_id": "NCT00000001",
            "sponsor": "Example sponsor",
            "indication": "Example indication",
            "phase": "Phase 2",
        },
        "document": {
            "title": "Comparable SAP",
            "document_type": "sap",
            "version": "1.0",
            "date": "2024-01-01",
            "status": "final",
            "source_repository": "Public registry",
            "direct_url": "https://example.org/comparable-sap.pdf",
            "retrieved_date": "2026-08-27",
        },
        "location": {"section": "Primary analysis", "page": 40},
        "similarity": {"level": "medium", "matched": ["endpoint scale"], "differences": ["phase"]},
        "extracted_design": {
            "endpoint": "Endpoint",
            "estimand_or_ice": "Not reported",
            "population": "Analysis set",
            "primary_method": "Model",
            "missing_strategy": "Not reported",
            "sensitivity": [],
        },
        "use_in_current_sap": {
            "role": "drafting-pattern",
            "affected_sections": ["SEC-12"],
            "limitation": "precedent-not-normative",
        },
    }


class OutputContractTests(unittest.TestCase):
    def test_valid_generic_output_and_current_source_fact_pass(self) -> None:
        errors = VALIDATOR.validate(generic_draft("TARGET-STUDY-001"), valid_ledger())
        self.assertEqual(errors, [])

    def test_current_identifier_must_not_enter_external_search_or_references(self) -> None:
        for mutation in ("search", "reference"):
            with self.subTest(mutation=mutation):
                ledger = valid_ledger()
                if mutation == "search":
                    ledger["search_summary"]["queries_run"] = ["TARGET-STUDY-001 statistical analysis plan"]
                else:
                    ledger["references"] = [
                        generic_reference(title="TARGET-STUDY-001 current Protocol", document_type="protocol")
                    ]
                errors = VALIDATOR.validate(generic_draft(), ledger)
                self.assertTrue(any("Current-study identifiers" in error for error in errors))

    def test_current_source_and_bundle_cannot_be_external_reference_types(self) -> None:
        cases = (
            generic_reference(reference_type="current_study_fact", document_type="protocol"),
            generic_reference(reference_type="trial_precedent", document_type="bundle"),
        )
        for record in cases:
            with self.subTest(record=record):
                ledger = valid_ledger()
                ledger["references"] = [record]
                self.assertTrue(VALIDATOR.validate(generic_draft(), ledger))

    def test_generic_heading_drift_fails(self) -> None:
        draft = generic_draft().replace("## 12. Efficacy Analyses", "## 12. Efficacy Assessment")
        errors = VALIDATOR.validate(draft, valid_ledger())
        self.assertTrue(any("Section 12 title" in error for error in errors))

    def test_undefined_current_source_and_external_reference_fail(self) -> None:
        ledger = valid_ledger()
        unit = ledger["content_units"][0]
        unit["source_facts"][0]["source_id"] = "SRC-UNDEFINED"
        unit["references"] = ["REF-UNDEFINED"]
        errors = VALIDATOR.validate(generic_draft(), ledger)
        self.assertTrue(any("source_id is undefined" in error for error in errors))
        self.assertTrue(any("undefined external references" in error for error in errors))

    def test_invalid_precedent_and_search_enums_fail(self) -> None:
        ledger = valid_ledger()
        precedent = nested_precedent()
        precedent["document"]["status"] = "approved"
        precedent["use_in_current_sap"]["limitation"] = "similar-study"
        ledger["references"] = [precedent]
        ledger["search_summary"]["status"] = "bundle-provided"
        errors = VALIDATOR.validate(generic_draft(), ledger)
        self.assertTrue(any("document.status is invalid" in error for error in errors))
        self.assertTrue(any("precedent-not-normative" in error for error in errors))
        self.assertTrue(any("search_summary.status is invalid" in error for error in errors))

    def test_sourced_mode_rejects_proposed_assumptions_or_alternatives(self) -> None:
        for field, value in (
            ("assumptions", ["Use participant-level worst-grade counting."]),
            ("alternatives", ["Use the Sponsor-standard counting convention after confirmation."]),
        ):
            with self.subTest(field=field):
                ledger = valid_ledger()
                ledger["content_units"][0][field] = value
                errors = VALIDATOR.validate(generic_draft(), ledger)
                self.assertTrue(
                    any("sourced mode" in error and field in error for error in errors),
                    errors,
                )


class ExistingBlindRunRegressionTests(unittest.TestCase):
    OUTPUTS = ROOT / ".validation-work" / "generate-sap" / "oncology-phase1-2" / "outputs"

    @unittest.skipUnless(OUTPUTS.exists(), "local blind-run artifacts are intentionally not versioned")
    def test_existing_runs_are_rechecked_without_rewriting_artifacts(self) -> None:
        expected = {
            ("CASE-ONC-004", "ONC004-C01"): (False, ("sourced mode with assumptions",)),
            ("CASE-ONC-001", "ONC001-C03"): (False, ("reference_type is invalid",)),
            ("CASE-ONC-001", "ONC001-C04"): (False, ("Section 1 title", "reference_type is invalid")),
            ("CASE-ONC-001", "ONC001-P01"): (False, ("document.status is invalid", "precedent-not-normative")),
            ("CASE-ONC-001", "ONC001-P02"): (False, ("reference_type is invalid", "document_type is invalid", "search_summary.status is invalid")),
            ("CASE-ONC-004", "ONC004-P01"): (False, ("reference_type is invalid", "document_type is invalid")),
            ("CASE-ONC-004", "ONC004-P02"): (False, ("Section 1 title", "undefined external references")),
        }
        for (case_id, run_id), (should_pass, expected_fragments) in expected.items():
            with self.subTest(run_id=run_id):
                run_dir = self.OUTPUTS / case_id / run_id
                draft = (run_dir / "sap-review-draft.md").read_text(encoding="utf-8")
                ledger = yaml.safe_load(
                    (run_dir / "generation-evidence-ledger.yaml").read_text(encoding="utf-8")
                )
                errors = VALIDATOR.validate(draft, ledger)
                self.assertEqual(not errors, should_pass, errors)
                for fragment in expected_fragments:
                    self.assertTrue(
                        any(fragment in error for error in errors),
                        f"{run_id} did not report expected category {fragment!r}: {errors}",
                    )


if __name__ == "__main__":
    unittest.main()
