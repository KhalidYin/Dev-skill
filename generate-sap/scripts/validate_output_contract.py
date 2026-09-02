"""Validate Generate SAP draft and evidence-ledger structure.

This validator is intentionally read-only and does not judge statistical
appropriateness. It reports contract errors and returns a non-zero exit code.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

import yaml


EXPECTED_SECTIONS = (
    "Title Page and Approvals",
    "Revision History",
    "Table of Contents",
    "Abbreviations and Definitions",
    "Introduction and Purpose",
    "Study Objectives, Design and Treatments",
    "Endpoints, Estimands and Intercurrent Events",
    "Sample Size, Randomization and Multiplicity",
    "Analysis Populations",
    "General Statistical Conventions",
    "Participant Disposition, Exposure and Compliance",
    "Efficacy Analyses",
    "Safety Analyses",
    "Other Analyses",
    "Interim Analyses and Data Monitoring",
    "Changes from Protocol-Planned Analyses",
    "References",
    "Appendices",
)
EXPECTED_SECTION_IDS = {f"SEC-{number:02d}" for number in range(1, 19)}
TOP_SECTION_PATTERN = re.compile(r"^##\s+(\d{1,2})\.\s+(.+?)\s*$", re.MULTILINE)
QUERY_PATTERN = re.compile(r"^Q-[A-Z0-9]+(?:[.-][A-Z0-9]+)*-\d{3}$")
INLINE_QUERY_PATTERN = re.compile(r"\bQ-[A-Z0-9]+(?:[.-][A-Z0-9]+)*-\d{3}\b")
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")

GENERATION_MODES = {"sourced", "derived", "proposed", "tbd", "conflict", "not-applicable"}
CONTENT_STATUSES = {"complete", "partial", "blocked"}
SECTION_STATUSES = {"complete", "partial", "tbd", "conflict", "not-applicable"}
SEARCH_STATUSES = {"completed", "limited", "unavailable", "prohibited", "not-run"}
REFERENCE_TYPES = {"normative_reference", "trial_precedent", "method_reference"}
DOCUMENT_TYPES = {"guidance", "sap", "protocol", "csr", "regulatory-review", "publication"}
REFERENCE_STATUSES = {"final", "effective", "draft", "withdrawn", "historical", "unknown"}


def has_value(value: Any) -> bool:
    return value is not None and value != "" and value != [] and value != {}


def require_fields(record: dict[str, Any], fields: set[str], prefix: str, errors: list[str]) -> None:
    for field in sorted(fields - record.keys()):
        errors.append(f"{prefix} missing field {field!r}.")


def validate_generic_headings(draft: str, errors: list[str]) -> None:
    found = [(int(number), title.strip()) for number, title in TOP_SECTION_PATTERN.findall(draft)]
    expected_numbers = list(range(1, 19))
    numbers = [number for number, _ in found]
    if numbers != expected_numbers:
        errors.append(f"Generic top-level section order is {numbers}; expected {expected_numbers}.")
    for number, title in found:
        if 1 <= number <= 18 and " ".join(title.split()).casefold() != EXPECTED_SECTIONS[number - 1].casefold():
            errors.append(
                f"Section {number} title is {title!r}; expected {EXPECTED_SECTIONS[number - 1]!r}."
            )


def validate_section_status(
    records: Any, generic: bool, errors: list[str]
) -> tuple[set[str], set[str], set[str]]:
    if not isinstance(records, list):
        errors.append("section_status must be a list.")
        return set(), set(), set()
    section_ids: list[str] = []
    linked_content: set[str] = set()
    linked_queries: set[str] = set()
    for index, record in enumerate(records):
        prefix = f"section_status[{index}]"
        if not isinstance(record, dict):
            errors.append(f"{prefix} must be a mapping.")
            continue
        require_fields(record, {"section_id", "status", "content_ids", "query_ids"}, prefix, errors)
        section_id = record.get("section_id")
        if not isinstance(section_id, str) or not section_id:
            errors.append(f"{prefix}.section_id must be non-empty.")
        else:
            section_ids.append(section_id)
        if record.get("status") not in SECTION_STATUSES:
            errors.append(f"{prefix}.status is invalid: {record.get('status')!r}.")
        for field, target in (("content_ids", linked_content), ("query_ids", linked_queries)):
            values = record.get(field)
            if not isinstance(values, list):
                errors.append(f"{prefix}.{field} must be a list.")
            else:
                target.update(str(value) for value in values if has_value(value))
    duplicates = sorted({value for value in section_ids if section_ids.count(value) > 1})
    if duplicates:
        errors.append(f"Duplicate section_status IDs: {duplicates}.")
    if generic and set(section_ids) != EXPECTED_SECTION_IDS:
        errors.append("Generic section_status must define SEC-01 through SEC-18 exactly once.")
    return set(section_ids), linked_content, linked_queries


def validate_content_units(
    records: Any, section_ids: set[str], source_ids: set[str], errors: list[str]
) -> tuple[set[str], set[str], set[str]]:
    if not isinstance(records, list):
        errors.append("content_units must be a list.")
        return set(), set(), set()
    if not records:
        errors.append("content_units must contain at least one material record.")
    required = {
        "content_id", "section_id", "topic", "generation_mode", "status", "source_facts",
        "applied_rules", "assumptions", "derivation_summary", "alternatives", "references",
        "generated_content", "open_questions", "downstream_sections",
    }
    content_ids: list[str] = []
    referenced_queries: set[str] = set()
    referenced_external: set[str] = set()
    for index, record in enumerate(records):
        prefix = f"content_units[{index}]"
        if not isinstance(record, dict):
            errors.append(f"{prefix} must be a mapping.")
            continue
        require_fields(record, required, prefix, errors)
        content_id = record.get("content_id")
        if has_value(content_id):
            content_ids.append(str(content_id))
        else:
            errors.append(f"{prefix}.content_id must be non-empty.")
        if record.get("section_id") not in section_ids:
            errors.append(f"{prefix}.section_id is undefined: {record.get('section_id')!r}.")
        mode = record.get("generation_mode")
        if mode not in GENERATION_MODES:
            errors.append(f"{prefix}.generation_mode is invalid: {mode!r}.")
        if record.get("status") not in CONTENT_STATUSES:
            errors.append(f"{prefix}.status is invalid: {record.get('status')!r}.")
        for field in (
            "source_facts", "applied_rules", "assumptions", "alternatives", "references",
            "open_questions", "downstream_sections",
        ):
            if not isinstance(record.get(field), list):
                errors.append(f"{prefix}.{field} must be a list.")
        generated = record.get("generated_content")
        if not isinstance(generated, dict):
            errors.append(f"{prefix}.generated_content must be a mapping.")
        else:
            for field in ("paragraph_id", "text"):
                if not has_value(generated.get(field)):
                    errors.append(f"{prefix}.generated_content.{field} must be non-empty.")
        facts = record.get("source_facts") if isinstance(record.get("source_facts"), list) else []
        for fact_index, fact in enumerate(facts):
            fact_prefix = f"{prefix}.source_facts[{fact_index}]"
            if not isinstance(fact, dict):
                errors.append(f"{fact_prefix} must be a mapping.")
                continue
            for field in ("fact_id", "source_id", "locator", "summary"):
                if not has_value(fact.get(field)):
                    errors.append(f"{fact_prefix}.{field} must be non-empty.")
            if fact.get("source_id") not in source_ids:
                errors.append(f"{fact_prefix}.source_id is undefined: {fact.get('source_id')!r}.")
        questions = record.get("open_questions") if isinstance(record.get("open_questions"), list) else []
        references = record.get("references") if isinstance(record.get("references"), list) else []
        referenced_queries.update(str(value) for value in questions if has_value(value))
        referenced_external.update(str(value) for value in references if has_value(value))
        if mode == "sourced" and not (facts or references):
            errors.append(f"{prefix} uses sourced mode without source_facts or external references.")
        if mode == "sourced" and record.get("assumptions"):
            errors.append(
                f"{prefix} uses sourced mode with assumptions; split the content or use proposed mode."
            )
        if mode == "sourced" and record.get("alternatives"):
            errors.append(
                f"{prefix} uses sourced mode with alternatives; split the content or use proposed mode."
            )
        if mode == "derived" and (not record.get("applied_rules") or not has_value(record.get("derivation_summary"))):
            errors.append(f"{prefix} uses derived mode without rules and a derivation summary.")
        if mode == "proposed" and (not record.get("assumptions") or not record.get("alternatives")):
            errors.append(f"{prefix} uses proposed mode without assumptions and alternatives.")
        if mode in {"proposed", "tbd", "conflict"} and not questions:
            errors.append(f"{prefix} uses {mode} mode without an open question.")
        if mode == "not-applicable" and not (facts or record.get("applied_rules") or references):
            errors.append(f"{prefix} marks not-applicable without a recorded basis.")
    duplicates = sorted({value for value in content_ids if content_ids.count(value) > 1})
    if duplicates:
        errors.append(f"Duplicate content IDs: {duplicates}.")
    return set(content_ids), referenced_queries, referenced_external


def validate_questions(
    records: Any, draft: str, section_ids: set[str], referenced: set[str], errors: list[str]
) -> set[str]:
    if not isinstance(records, list):
        errors.append("open_questions must be a list.")
        return set()
    required = {
        "query_id", "origin_section", "query_type", "severity", "topic", "known",
        "missing_or_conflicting", "impact", "question", "owner", "status", "affected_sections",
    }
    query_ids: list[str] = []
    for index, record in enumerate(records):
        prefix = f"open_questions[{index}]"
        if not isinstance(record, dict):
            errors.append(f"{prefix} must be a mapping.")
            continue
        require_fields(record, required, prefix, errors)
        query_id = record.get("query_id")
        if not isinstance(query_id, str) or not QUERY_PATTERN.fullmatch(query_id):
            errors.append(f"{prefix}.query_id is invalid: {query_id!r}.")
        else:
            query_ids.append(query_id)
        if record.get("origin_section") not in section_ids:
            errors.append(f"{prefix}.origin_section is undefined: {record.get('origin_section')!r}.")
        if record.get("query_type") not in {"missing-input", "missing-decision", "source-conflict", "verification-needed"}:
            errors.append(f"{prefix}.query_type is invalid: {record.get('query_type')!r}.")
        if record.get("severity") not in {"blocking", "non-blocking"}:
            errors.append(f"{prefix}.severity is invalid: {record.get('severity')!r}.")
        if record.get("status") not in {"open", "resolved"}:
            errors.append(f"{prefix}.status is invalid: {record.get('status')!r}.")
        if not has_value(record.get("question")):
            errors.append(f"{prefix}.question must be non-empty.")
        for field in ("known", "missing_or_conflicting", "impact", "affected_sections"):
            if not isinstance(record.get(field), list):
                errors.append(f"{prefix}.{field} must be a list.")
        affected = record.get("affected_sections")
        if isinstance(affected, list) and any(value not in section_ids for value in affected):
            errors.append(f"{prefix}.affected_sections contains undefined section IDs.")
    defined = set(query_ids)
    if referenced - defined:
        errors.append(f"Content units reference undefined queries: {sorted(referenced - defined)}.")
    if defined - referenced:
        errors.append(f"Open questions are not linked from content units: {sorted(defined - referenced)}.")
    inline = set(INLINE_QUERY_PATTERN.findall(draft))
    if inline - defined:
        errors.append(f"Draft contains query IDs missing from ledger: {sorted(inline - defined)}.")
    if defined - inline:
        errors.append(f"Ledger query IDs are not rendered in the draft: {sorted(defined - inline)}.")
    return defined


def validate_generic_reference(record: dict[str, Any], prefix: str, errors: list[str]) -> None:
    required = {
        "reference_id", "reference_type", "title", "authors_or_organization", "document_type",
        "version", "date", "status", "direct_url", "retrieved_date", "location",
        "supported_summary", "limitations",
    }
    require_fields(record, required, prefix, errors)
    if record.get("reference_type") not in REFERENCE_TYPES:
        errors.append(f"{prefix}.reference_type is invalid: {record.get('reference_type')!r}.")
    if record.get("document_type") not in DOCUMENT_TYPES:
        errors.append(f"{prefix}.document_type is invalid: {record.get('document_type')!r}.")
    if record.get("status") not in REFERENCE_STATUSES:
        errors.append(f"{prefix}.status is invalid: {record.get('status')!r}.")
    for field in required - {"location", "limitations"}:
        if not has_value(record.get(field)):
            errors.append(f"{prefix}.{field} must be non-empty.")
    validate_url_date_location(record, prefix, errors)
    if not isinstance(record.get("limitations"), list):
        errors.append(f"{prefix}.limitations must be a list.")


def validate_url_date_location(record: dict[str, Any], prefix: str, errors: list[str]) -> None:
    url = record.get("direct_url")
    if not isinstance(url, str) or not url.startswith(("https://", "http://")):
        errors.append(f"{prefix}.direct_url must be an HTTP(S) URL.")
    date = record.get("retrieved_date")
    if not isinstance(date, str) or not DATE_PATTERN.fullmatch(date):
        errors.append(f"{prefix}.retrieved_date must use YYYY-MM-DD.")
    location = record.get("location")
    if not isinstance(location, dict):
        errors.append(f"{prefix}.location must be a mapping.")
    elif not has_value(location.get("section")) and not has_value(location.get("page")):
        errors.append(f"{prefix}.location requires a section or page.")


def validate_precedent(record: dict[str, Any], prefix: str, errors: list[str]) -> None:
    required = {"reference_id", "reference_type", "study", "document", "location", "similarity", "extracted_design", "use_in_current_sap"}
    require_fields(record, required, prefix, errors)
    if record.get("reference_type") != "trial_precedent":
        errors.append(f"{prefix}.reference_type must be trial_precedent.")
    for field in ("study", "document", "location", "similarity", "extracted_design", "use_in_current_sap"):
        if not isinstance(record.get(field), dict):
            errors.append(f"{prefix}.{field} must be a mapping.")
    study = record.get("study") if isinstance(record.get("study"), dict) else {}
    for field in ("title", "registry_id", "sponsor", "indication", "phase"):
        if not has_value(study.get(field)):
            errors.append(f"{prefix}.study.{field} must be non-empty.")
    document = record.get("document") if isinstance(record.get("document"), dict) else {}
    for field in ("title", "document_type", "version", "date", "status", "source_repository", "direct_url", "retrieved_date"):
        if not has_value(document.get(field)):
            errors.append(f"{prefix}.document.{field} must be non-empty.")
    if document.get("document_type") not in DOCUMENT_TYPES - {"guidance"}:
        errors.append(f"{prefix}.document.document_type is invalid: {document.get('document_type')!r}.")
    if document.get("status") not in {"final", "draft", "historical", "unknown"}:
        errors.append(f"{prefix}.document.status is invalid: {document.get('status')!r}.")
    validate_url_date_location({**document, "location": record.get("location")}, f"{prefix}.document", errors)
    similarity = record.get("similarity") if isinstance(record.get("similarity"), dict) else {}
    if similarity.get("level") not in {"high", "medium", "low"}:
        errors.append(f"{prefix}.similarity.level is invalid: {similarity.get('level')!r}.")
    if not isinstance(similarity.get("matched"), list) or not isinstance(similarity.get("differences"), list):
        errors.append(f"{prefix}.similarity matched and differences must be lists.")
    extracted = record.get("extracted_design") if isinstance(record.get("extracted_design"), dict) else {}
    for field in ("endpoint", "estimand_or_ice", "population", "primary_method", "missing_strategy", "sensitivity"):
        if field not in extracted:
            errors.append(f"{prefix}.extracted_design missing field {field!r}.")
    if "sensitivity" in extracted and not isinstance(extracted.get("sensitivity"), list):
        errors.append(f"{prefix}.extracted_design.sensitivity must be a list.")
    use = record.get("use_in_current_sap") if isinstance(record.get("use_in_current_sap"), dict) else {}
    if use.get("role") not in {"candidate-design", "drafting-pattern", "background-only"}:
        errors.append(f"{prefix}.use_in_current_sap.role is invalid: {use.get('role')!r}.")
    if use.get("limitation") != "precedent-not-normative":
        errors.append(f"{prefix}.use_in_current_sap.limitation must be precedent-not-normative.")
    if not isinstance(use.get("affected_sections"), list):
        errors.append(f"{prefix}.use_in_current_sap.affected_sections must be a list.")


def validate_references(records: Any, referenced: set[str], errors: list[str]) -> set[str]:
    if not isinstance(records, list):
        errors.append("references must be a list.")
        return set()
    reference_ids: list[str] = []
    for index, record in enumerate(records):
        prefix = f"references[{index}]"
        if not isinstance(record, dict):
            errors.append(f"{prefix} must be a mapping.")
            continue
        reference_id = record.get("reference_id")
        if has_value(reference_id):
            reference_ids.append(str(reference_id))
        else:
            errors.append(f"{prefix}.reference_id must be non-empty.")
        if record.get("reference_type") == "trial_precedent" and "document" in record:
            validate_precedent(record, prefix, errors)
        else:
            validate_generic_reference(record, prefix, errors)
    defined = set(reference_ids)
    if referenced - defined:
        errors.append(f"Content units reference undefined external references: {sorted(referenced - defined)}.")
    duplicates = sorted({value for value in reference_ids if reference_ids.count(value) > 1})
    if duplicates:
        errors.append(f"Duplicate reference IDs: {duplicates}.")
    return defined


def validate_search_summary(summary: Any, errors: list[str]) -> None:
    if not isinstance(summary, dict):
        errors.append("search_summary must be a mapping.")
        return
    required = {"status", "queries_run", "repositories_checked", "candidates_found", "shortlisted", "deeply_reviewed", "stop_reason", "limitations"}
    require_fields(summary, required, "search_summary", errors)
    if summary.get("status") not in SEARCH_STATUSES:
        errors.append(f"search_summary.status is invalid: {summary.get('status')!r}.")
    for field in ("queries_run", "repositories_checked", "limitations"):
        if not isinstance(summary.get(field), list):
            errors.append(f"search_summary.{field} must be a list.")
    for field in ("candidates_found", "shortlisted", "deeply_reviewed"):
        if not isinstance(summary.get(field), int) or summary.get(field, -1) < 0:
            errors.append(f"search_summary.{field} must be a non-negative integer.")
    if not has_value(summary.get("stop_reason")):
        errors.append("search_summary.stop_reason must be non-empty.")


def validate_current_source_separation(
    source_versions: Any, references: Any, search_summary: Any, errors: list[str]
) -> None:
    """Keep explicit current-study identifiers out of external evidence fields."""
    if not isinstance(source_versions, list):
        return
    identifiers: set[str] = set()
    for source in source_versions:
        if not isinstance(source, dict):
            continue
        for field in ("source_id", "label", "title", "protocol_id", "registry_id"):
            value = source.get(field)
            if isinstance(value, str) and len(value.strip()) >= 6:
                identifiers.add(value.strip().casefold())
    external_payload = yaml.safe_dump(
        {
            "references": references if isinstance(references, list) else [],
            "queries_run": search_summary.get("queries_run", [])
            if isinstance(search_summary, dict)
            else [],
        },
        allow_unicode=True,
        sort_keys=True,
    ).casefold()
    leaked = sorted(identifier for identifier in identifiers if identifier in external_payload)
    if leaked:
        errors.append(
            "Current-study identifiers appear in external references or search queries: "
            f"{leaked}."
        )


def validate(draft: str, ledger: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required_top = {"schema_version", "document", "section_status", "content_units", "open_questions", "references", "consistency_findings", "search_summary"}
    require_fields(ledger, required_top, "ledger", errors)
    document = ledger.get("document")
    if not isinstance(document, dict):
        errors.append("document must be a mapping.")
        document = {}
    generic = document.get("template") == "generic"
    if generic:
        validate_generic_headings(draft, errors)
    source_versions = document.get("source_versions")
    source_ids: set[str] = set()
    if not isinstance(source_versions, list):
        errors.append("document.source_versions must be a list.")
    else:
        for index, source in enumerate(source_versions):
            if not isinstance(source, dict) or not has_value(source.get("source_id")):
                errors.append(f"document.source_versions[{index}] requires a non-empty source_id.")
            else:
                source_ids.add(str(source["source_id"]))
    section_ids, linked_content, linked_queries = validate_section_status(ledger.get("section_status"), generic, errors)
    content_ids, referenced_queries, referenced_external = validate_content_units(ledger.get("content_units"), section_ids, source_ids, errors)
    query_ids = validate_questions(ledger.get("open_questions"), draft, section_ids, referenced_queries, errors)
    validate_references(ledger.get("references"), referenced_external, errors)
    validate_current_source_separation(
        source_versions, ledger.get("references"), ledger.get("search_summary"), errors
    )
    if linked_content - content_ids:
        errors.append(f"section_status references undefined content IDs: {sorted(linked_content - content_ids)}.")
    if content_ids - linked_content:
        errors.append(f"Content units are not linked from section_status: {sorted(content_ids - linked_content)}.")
    if linked_queries - query_ids:
        errors.append(f"section_status references undefined query IDs: {sorted(linked_queries - query_ids)}.")
    validate_search_summary(ledger.get("search_summary"), errors)
    for key in ("section_status", "content_units", "open_questions", "references", "consistency_findings"):
        if key in ledger and not isinstance(ledger[key], list):
            errors.append(f"{key} must be a list.")
    return errors


def load_inputs(draft_path: Path, ledger_path: Path) -> tuple[str, dict[str, Any]]:
    draft = draft_path.read_text(encoding="utf-8")
    ledger = yaml.safe_load(ledger_path.read_text(encoding="utf-8"))
    if not isinstance(ledger, dict):
        raise ValueError("Ledger root must be a YAML mapping.")
    return draft, ledger


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--draft", required=True, type=Path)
    parser.add_argument("--ledger", required=True, type=Path)
    args = parser.parse_args()
    try:
        draft, ledger = load_inputs(args.draft, args.ledger)
    except (OSError, UnicodeError, yaml.YAMLError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    errors = validate(draft, ledger)
    if errors:
        print(f"FAIL: {len(errors)} output-contract error(s).", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("PASS: SAP draft and evidence ledger satisfy the structural output contract.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
