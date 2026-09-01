import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "generate-sap" / "scripts" / "build_evidence_ledger.py"
SPEC = importlib.util.spec_from_file_location("generate_sap_ledger_builder", SCRIPT)
BUILDER = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(BUILDER)


class EvidenceLedgerBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.output_root = Path(self.temp_dir.name) / "output"
        self.output_root.mkdir()

    def add(self, record_type: str, value: dict) -> None:
        BUILDER.append_record(
            self.output_root,
            record_type,
            json.dumps(value, ensure_ascii=False),
        )

    def test_valid_records_are_deterministically_assembled_as_yaml(self) -> None:
        self.add("document", {"title": "中文 SAP", "status": "review-draft", "template": "generic"})
        self.add(
            "section_status",
            {"section_id": "SEC-01", "status": "partial", "content_ids": ["SAP-01-001"], "query_ids": []},
        )
        self.add(
            "content_unit",
            {
                "content_id": "SAP-01-001",
                "section_id": "SEC-01",
                "assumptions": ["No semantic rewriting."],
            },
        )
        self.add("open_question", {"query_id": "Q-ADM-001", "status": "open"})
        self.add("reference", {"reference_id": "REF-001", "title": "Guidance"})
        self.add("consistency_finding", {"finding_id": "XCHK-001-01", "status": "pass"})
        self.add(
            "search_summary",
            {
                "status": "prohibited",
                "queries_run": [],
                "repositories_checked": [],
                "candidates_found": 0,
                "shortlisted": 0,
                "deeply_reviewed": 0,
                "stop_reason": "Control run.",
                "limitations": [],
            },
        )

        output_path = BUILDER.finalize_ledger(self.output_root)
        ledger = yaml.safe_load(output_path.read_text(encoding="utf-8"))

        self.assertEqual(
            list(ledger),
            [
                "schema_version",
                "document",
                "section_status",
                "content_units",
                "open_questions",
                "references",
                "consistency_findings",
                "search_summary",
            ],
        )
        self.assertEqual(ledger["document"]["title"], "中文 SAP")
        self.assertEqual(ledger["content_units"][0]["content_id"], "SAP-01-001")
        self.assertFalse((self.output_root / BUILDER.STAGING_NAME).exists())

    def test_malformed_json_is_rejected_before_staging_mutation(self) -> None:
        self.add("document", {"title": "Draft"})
        staging_path = self.output_root / BUILDER.STAGING_NAME
        before = staging_path.read_bytes()

        with self.assertRaisesRegex(ValueError, "valid JSON"):
            BUILDER.append_record(
                self.output_root,
                "content_unit",
                '{"content_id":"SAP-14-001","assumptions":["text"}',
            )

        self.assertEqual(staging_path.read_bytes(), before)
        self.assertFalse((self.output_root / BUILDER.OUTPUT_NAME).exists())

    def test_duplicate_singleton_and_stable_id_are_rejected(self) -> None:
        self.add("document", {"title": "Draft"})
        with self.assertRaisesRegex(ValueError, "document already exists"):
            self.add("document", {"title": "Replacement"})

        section = {"section_id": "SEC-01", "status": "tbd", "content_ids": [], "query_ids": []}
        self.add("section_status", section)
        with self.assertRaisesRegex(ValueError, "duplicate section_id"):
            self.add("section_status", section)

    def test_finalize_requires_both_singletons_and_never_overwrites(self) -> None:
        self.add("document", {"title": "Draft"})
        with self.assertRaisesRegex(ValueError, "search_summary"):
            BUILDER.finalize_ledger(self.output_root)

        self.add("search_summary", {"status": "not-run"})
        output_path = BUILDER.finalize_ledger(self.output_root)
        with self.assertRaisesRegex(ValueError, "already exists"):
            BUILDER.finalize_ledger(self.output_root)
        self.assertTrue(output_path.is_file())


if __name__ == "__main__":
    unittest.main()
