"""Validate a protocol review bundle and assemble the evidence-linked workbook."""

from __future__ import annotations

import argparse
import io
import json
from collections import Counter
from pathlib import Path

import yaml
from openpyxl import Workbook
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

CHECKLIST = Path(__file__).resolve().parents[1] / "assets" / "checklist.yaml"
SEVERITIES = {"Critical", "Major", "Minor", "Editorial"}
STATUSES = {"pass", "finding", "not-applicable", "not-assessable"}
ANALYSIS_STATUSES = STATUSES | {"sap-detail"}
FINDING_TYPES = {"error", "inconsistency", "omission", "ambiguity", "method-mismatch", "statistician-review"}
TRACKING = ("Open", "Responded", "Closed")
ROLES = {"protocol", "protocol-amendment", "sap", "crf", "charter", "simulation", "sop", "other"}
SOURCE_KINDS = {"regulation", "guidance", "reporting-reference", "public-precedent"}
CROSSWALK_STATES = {"observed", "agrees", "conflict", "disclosed-change", "unresolved"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def present(record, key):
    return isinstance(record.get(key), str) and bool(record[key].strip())


def fields(record, required, label, *, lists=""):
    require(isinstance(record, dict), f"{label} must be an object")
    for key in required.split():
        require(present(record, key), f"{label}: missing text field {key}")
    list_keys = set(lists.split())
    for key, value in record.items():
        if key in list_keys:
            require(
                isinstance(value, list)
                and all(isinstance(entry, str) and entry.strip() for entry in value)
                and len(set(value)) == len(value),
                f"{label}: {key} must be a list of unique nonempty strings",
            )
        else:
            require(isinstance(value, str), f"{label}: {key} must be text")
            require(len(value) <= 32767, f"{label}: {key} exceeds the Excel cell limit")
            require(not ILLEGAL_CHARACTERS_RE.search(value), f"{label}: {key} contains an invalid control character")


def records(bundle, name):
    rows = bundle.get(name)
    require(isinstance(rows, list), f"{name} must be a list")
    return rows


def indexed(rows, name, required, *, lists=""):
    result = {}
    for row in rows:
        fields(row, f"id {required}", name, lists=lists)
        key = row["id"]
        require(key not in result, f"{name}: duplicate ID {key}")
        result[key] = row
    return result


def get_scope(bundle, checklist):
    """Validate inputs needed for routing, before any coverage is written."""
    require(isinstance(bundle, dict), "review bundle must be an object")
    review = bundle.get("review")
    fields(review, "title date protocol_id checklist_version input_scope retrieval_status retrieval_note", "review")
    require(review["checklist_version"] == checklist["checklist_version"], "Checklist version mismatch")
    require(review["input_scope"] in {"full", "excerpt"}, "Unknown input scope")
    require(review["retrieval_status"] in {"complete", "limited", "unavailable"}, "Unknown retrieval status")

    docs = indexed(records(bundle, "documents"), "documents", "role title version date location")
    for doc in docs.values():
        require(doc["role"] in ROLES, f"{doc['id']}: unknown document role")
    protocol = docs.get(review["protocol_id"], {})
    require(protocol.get("role") == "protocol", "review.protocol_id must identify a supplied protocol")

    units = indexed(
        records(bundle, "units"), "units",
        "title scope purpose comparison structure inference locator scope_note",
        lists="tags uncertain_tags",
    )
    scope_counts = Counter(unit["scope"] for unit in units.values())
    require(
        scope_counts == {"whole": 1}
        or (scope_counts["shared"] == 1 and scope_counts["part"] >= 2 and len(scope_counts) == 2),
        "Use one whole unit, or one shared unit and at least two part units",
    )
    tags = set(checklist["design_tags"])
    for unit in units.values():
        active = set(unit.get("tags", []))
        uncertain = set(unit.get("uncertain_tags", []))
        require(active | uncertain <= tags, f"{unit['id']}: unknown design tags")
        require(not (active & uncertain), f"{unit['id']}: a tag cannot be active and uncertain")
    return review, docs, units


def plan_checks(units, docs, checklist):
    roles = {doc["role"] for doc in docs.values()}
    for unit in units.values():
        for item in checklist["items"]:
            if item["scope"] == "study" and unit["scope"] == "part":
                continue
            tag_filter = set(item.get("any_tags", []))
            if tag_filter and not tag_filter.intersection(unit.get("tags", [])):
                unresolved = tag_filter.intersection(unit.get("uncertain_tags", []))
                if unresolved:
                    yield unit["id"], item, "not-assessable", f"Uncertain design: {', '.join(sorted(unresolved))}"
                else:
                    yield unit["id"], item, "not-applicable", "Design condition inactive"
                continue
            missing = set(item.get("requires", [])) - roles
            if missing:
                yield unit["id"], item, "not-assessable", f"Missing document: {', '.join(sorted(missing))}"
            else:
                yield unit["id"], item, "review", ""


def other_evidence(row, docs, label, *, required=False):
    keys = ("other_doc_id", "other_locator", "other_evidence")
    if required or any(present(row, key) for key in keys):
        require(all(present(row, key) for key in keys), f"{label}: incomplete comparator evidence")
        require(row["other_doc_id"] in docs, f"{label}: unknown comparator document")


def analysis_plan(bundle, checklist, units):
    analyses = indexed(records(bundle, "analyses"), "analyses", "unit_id title role locator")
    required_slots = {}
    for key, row in analyses.items():
        require(row["unit_id"] in units, f"{key}: unknown analysis unit")
        slots = [slot for slot, roles in checklist["analysis_slots"].items() if row["role"] in roles]
        require(slots, f"{key}: unknown analysis role")
        unit = units[row["unit_id"]]
        tags = set(unit.get("tags", [])) | set(unit.get("uncertain_tags", []))
        slots.extend(
            slot for slot, config in checklist.get("design_analysis_slots", {}).items()
            if row["role"] in config["roles"] and tags.intersection(config["any_tags"])
        )
        required_slots[key] = slots
    return analyses, required_slots


def linked_findings(row, findings, unit, label):
    links = row.get("finding_ids", [])
    require(bool(links) == (row["status"] == "finding"), f"{label}: invalid finding links for {row['status']}")
    for finding_id in links:
        require(findings.get(finding_id, {}).get("unit_id") == unit, f"{label}: invalid link to {finding_id}")
    return links


def validate_matrix(bundle, analyses, required_slots, findings):
    seen = set()
    for row in records(bundle, "analysis_matrix"):
        fields(row, "analysis_id slot status note", "analysis matrix", lists="finding_ids")
        key = row["analysis_id"]
        pair = (key, row["slot"])
        require(row["slot"] in required_slots.get(key, []), f"{pair}: unknown analysis or slot")
        require(pair not in seen, f"{pair}: duplicate matrix record")
        require(row["status"] in ANALYSIS_STATUSES, f"{pair}: unknown analysis status")
        if row["slot"] == "method-fit":
            require(row["status"] != "sap-detail", f"{pair}: method fit requires a review conclusion")
        if row["status"] in {"pass", "sap-detail"}:
            require(present(row, "value") and present(row, "locator"), f"{pair}: analysis value and locator required")
        for finding_id in linked_findings(row, findings, analyses[key]["unit_id"], pair):
            require(key in findings[finding_id].get("analysis_ids", []), f"{pair}: invalid reverse link to {finding_id}")
        seen.add(pair)
    missing = {(key, slot) for key, slots in required_slots.items() for slot in slots} - seen
    require(not missing, f"Missing analysis matrix: {', '.join('/'.join(pair) for pair in sorted(missing))}")


def validate(bundle, checklist, docs, units, plan):
    sources = indexed(
        records(bundle, "sources"), "sources",
        "kind title url version status region checked_date locator relevance limits",
    )
    basis = {row["id"]: row for row in checklist["basis_register"]}
    for row in sources.values():
        require(row["id"] not in basis, f"{row['id']}: source ID overlaps checklist basis")
        require(row["kind"] in SOURCE_KINDS, f"{row['id']}: unknown source kind")
        require(row["url"].startswith(("https://", "http://")), f"{row['id']}: source URL required")
        if row["kind"] == "public-precedent":
            require(present(row, "document_type"), f"{row['id']}: state the actual precedent document type")

    crosswalk_units = set()
    for row in records(bundle, "crosswalk"):
        fields(row, "unit_id parameter value locator assessment", "crosswalk")
        unit = row["unit_id"]
        require(unit in units, f"Crosswalk: unknown unit {unit}")
        require(row["assessment"] in CROSSWALK_STATES, f"{unit}: unknown crosswalk assessment")
        paired = row["assessment"] in {"agrees", "conflict", "disclosed-change"}
        other_evidence(row, docs, f"Crosswalk {unit}", required=paired)
        crosswalk_units.add(unit)
    require(crosswalk_units == set(units), "Crosswalk needs at least one record for each unit")

    analyses, required_slots = analysis_plan(bundle, checklist, units)
    findings = indexed(
        records(bundle, "findings"), "findings",
        "unit_id type confidence locator evidence comment rationale", lists="item_ids analysis_ids",
    )
    for key, row in findings.items():
        require(row["unit_id"] in units, f"{key}: unknown unit")
        kind, severity = row["type"], row.get("severity", "")
        require(kind in FINDING_TYPES, f"{key}: unknown finding type")
        require(row["confidence"] in {"high", "medium", "low"}, f"{key}: unknown confidence")
        require(row.get("status", "Open") in TRACKING, f"{key}: invalid tracking status")
        for analysis_id in row.get("analysis_ids", []):
            require(analyses.get(analysis_id, {}).get("unit_id") == row["unit_id"],
                    f"{key}: invalid analysis link {analysis_id}")
        if kind == "ambiguity" and severity != "Editorial":
            require(present(row, "reading_a") and present(row, "reading_b"),
                    f"{key}: material ambiguity needs two plausible readings")
            require(row["reading_a"].strip().casefold() != row["reading_b"].strip().casefold(),
                    f"{key}: ambiguity readings must differ")
        if kind == "statistician-review":
            require(not severity, f"{key}: statistician review has no severity")
        else:
            require(severity in SEVERITIES, f"{key}: invalid severity")
            require(row.get("item_ids"), f"{key}: ranked findings require checklist items")
        require(severity != "Critical" or row["confidence"] != "low", f"{key}: low-confidence Critical")
        other_evidence(row, docs, key, required=severity == "Critical" or kind in {"error", "inconsistency"})
        if row.get("other_doc_id") == bundle["review"]["protocol_id"]:
            require(row["locator"] != row["other_locator"], f"{key}: internal comparison needs two distinct locators")
        if present(row, "basis_id") or present(row, "basis_locator"):
            source_id = row.get("basis_id")
            require(source_id in sources or source_id in basis, f"{key}: unknown basis ID")
            source = sources.get(source_id, basis.get(source_id))
            require(source.get("kind") != "public-precedent", f"{key}: precedent cannot serve as finding basis")
            require(present(row, "basis_locator"), f"{key}: precise basis locator required")
            if severity in {"Critical", "Major"}:
                require(source["status"] in {"final", "effective"}, f"{key}: high severity requires final or effective basis")
        if kind == "method-mismatch":
            require(present(row, "other_locator") or present(row, "basis_locator"),
                    f"{key}: method mismatch needs comparator evidence or precise basis")

    routed = {(unit, item["id"]): state for unit, item, state, _ in plan}
    coverage = {}
    for row in records(bundle, "coverage"):
        fields(row, "unit_id item_id status note", "coverage", lists="finding_ids")
        key = (row["unit_id"], row["item_id"])
        require(key in routed, f"{key}: unknown or out-of-scope unit/item pair")
        require(routed[key] == "review", f"{key}: builder supplies coverage for this pair")
        require(key not in coverage, f"{key}: duplicate coverage")
        status = row["status"]
        require(status in ANALYSIS_STATUSES, f"{key}: unknown status")
        if status in {"pass", "sap-detail"}:
            require(present(row, "locator"), f"{key}: {status} needs a protocol locator")
        for finding_id in linked_findings(row, findings, key[0], key):
            require(key[1] in findings[finding_id].get("item_ids", []), f"{key}: invalid reverse link to {finding_id}")
        coverage[key] = row

    missing = {key for key, state in routed.items() if state == "review"} - coverage.keys()
    require(not missing, f"Missing coverage: {', '.join('/'.join(key) for key in sorted(missing))}")
    for finding_id, row in findings.items():
        for item_id in row.get("item_ids", []):
            key = (row["unit_id"], item_id)
            require(finding_id in coverage.get(key, {}).get("finding_ids", []), f"{finding_id}: missing reverse coverage for {key}")
    validate_matrix(bundle, analyses, required_slots, findings)
    matrix_links = {(row["analysis_id"], finding_id) for row in bundle["analysis_matrix"]
                    for finding_id in row.get("finding_ids", [])}
    for finding_id, row in findings.items():
        for analysis_id in row.get("analysis_ids", []):
            require((analysis_id, finding_id) in matrix_links, f"{finding_id}: missing matrix link for {analysis_id}")
    by_unit = {row["unit_id"] for row in analyses.values() if row["role"] in {"primary", "decision"}}
    for unit_id, unit in units.items():
        if unit["scope"] == "shared" or unit_id in by_unit:
            continue
        state = coverage[unit_id, "CH-04"]["status"]
        require(state in {"finding", "not-assessable"}, f"{unit_id}: covered primary content needs an analysis record")
    return sources, findings, coverage, analyses


def add_table(workbook, name, columns, rows):
    sheet = workbook.create_sheet(name)
    sheet.append([title for _, title, _ in columns])
    for cell in sheet[1]:
        cell.font = Font(color="FFFFFF", bold=True)
        cell.fill = PatternFill("solid", fgColor="24445D")
    for index, (_, _, width) in enumerate(columns, 1):
        sheet.column_dimensions[get_column_letter(index)].width = width
    for row_number, row in enumerate(rows, 2):
        for col, (key, _, _) in enumerate(columns, 1):
            value = row.get(key, "")
            if isinstance(value, list):
                value = ", ".join(value)
            if isinstance(value, str):
                require(len(value) <= 32767, f"{name} row {row_number}: {key} exceeds the Excel cell limit")
            cell = sheet.cell(row_number, col, value)
            if isinstance(value, str):
                cell.data_type = "s"
            cell.alignment = Alignment(vertical="top", wrap_text=True)
    sheet.freeze_panes = "A2"
    sheet.auto_filter.ref = sheet.dimensions
    return sheet


def columns(spec):
    return [(key, title, int(width)) for key, title, width in (field.split("|") for field in spec.split(";"))]


def document_label(doc):
    return f"{doc['title']} (v{doc['version']}, {doc['date']})"


def finding_evidence(row, review, docs, sources, checklist):
    protocol = document_label(docs[review["protocol_id"]])
    parts = [f"{protocol} · {row['locator']}\n{row['evidence']}"]
    if present(row, "other_doc_id"):
        comparator = document_label(docs[row["other_doc_id"]])
        parts.append(f"{comparator} · {row['other_locator']}\n{row['other_evidence']}")
    if present(row, "basis_id"):
        basis = {source["id"]: source for source in checklist["basis_register"]}
        source = sources.get(row["basis_id"], basis.get(row["basis_id"]))
        text = f"{source['title']} · {row['basis_locator']} · {source['status']}"
        if source.get("url"):
            text += f"\n{source['url']}"
        parts.append(text)
    return "\n\n".join(parts)


def traceability_rows(bundle, docs, sources):
    for doc in docs.values():
        yield {"focus": f"{doc['id']} · {doc['role']}", "detail": document_label(doc), "evidence": doc["location"]}
    for row in sources.values():
        yield {
            "focus": f"{row['id']} · {row['kind']}",
            "detail": f"{row['title']} · {row['version']} · {row['status']} · {row['region']}",
            "evidence": f"{row['locator']}\n{row['url']}\nChecked {row['checked_date']}",
            "note": "\n".join(filter(None, (row.get("document_type"), row["relevance"], row["limits"]))),
        }
    for row in bundle["crosswalk"]:
        detail = row["value"]
        locator = row["locator"]
        if present(row, "other_doc_id"):
            detail += f"\n{row['other_doc_id']}: {row['other_evidence']}"
            locator += f"\n{row['other_locator']}"
        yield {
            "focus": f"{row['unit_id']} · {row['parameter']}", "detail": detail,
            "evidence": locator, "note": f"{row['assessment']} {row.get('note', '')}".strip(),
        }


def build_workbook(bundle, checklist, review, docs, units, plan, sources, findings, coverage, analyses, *, details=False):
    workbook = Workbook()
    workbook.remove(workbook.active)

    def table(name, spec, rows):
        return add_table(workbook, name, columns(spec), rows)

    coverage_rows = [
        {
            "focus": f"{unit_id} · {item['id']}", "layer": item.get("layer", "statistical"),
            "check": item["check"],
            **coverage.get((unit_id, item["id"]), {"status": state, "note": note}),
        }
        for unit_id, item, state, note in plan if state != "not-applicable"
    ]
    overview = [
        {"field": "Protocol", "value": document_label(docs[review["protocol_id"]])},
        {"field": "Review", "value": f"{review['title']} · {review['date']} · {review['input_scope']}"},
        {"field": "Template", "value": f"0.2.0 · checklist {review['checklist_version']}"},
        {"field": "Source search", "value": f"{review['retrieval_status']} · {review['retrieval_note']}"},
        {"field": "Use", "value": "AI-assisted review draft for qualified statistician follow-up."},
    ]
    overview.extend({
        "field": f"Scope · {unit['id']}",
        "value": " · ".join(unit[key] for key in ("title", "purpose", "comparison", "structure", "inference", "locator", "scope_note")),
    } for unit in units.values())
    overview.extend({"field": f"Coverage · {status}", "value": count}
                    for status, count in sorted(Counter(row["status"] for row in coverage_rows).items()))
    summary = table("Overview", "field|Item|25;value|Summary|95", overview)
    for status in TRACKING:
        summary.append([f"Comments · {status}", f'=COUNTIF(Comments!$G:$G,"{status}")'])

    comment_rows = []
    for row in findings.values():
        rationale = row["rationale"]
        if present(row, "reading_a") and present(row, "reading_b"):
            rationale = f"A. {row['reading_a']}\nB. {row['reading_b']}\n{rationale}"
        comment_rows.append({
            **row,
            "focus": " · ".join([row["unit_id"], row["type"], *row.get("analysis_ids", [])]),
            "priority": row.get("severity") or "Statistician review",
            "rationale": rationale,
            "sources": finding_evidence(row, review, docs, sources, checklist),
            "status": row.get("status", "Open"),
        })
    comments = table(
        "Comments",
        "id|ID|12;focus|Focus|21;priority|Priority|15;comment|Author Comment|45;"
        "rationale|Rationale|46;sources|Evidence and Sources|58;status|Status|14;"
        "author_response|Author Response|28;reviewer_followup|Reviewer Follow-up|28",
        comment_rows,
    )
    status_list = DataValidation(type="list", formula1='"' + ",".join(TRACKING) + '"')
    status_list.showErrorMessage = True
    comments.add_data_validation(status_list)
    status_list.add(f"G2:G{max(comments.max_row + 200, 2)}")
    comments.freeze_panes = "C2"

    table(
        "Coverage",
        "focus|Check ID|19;layer|Layer|15;check|Check|49;status|Result|19;"
        "location|Location or reason|52;finding_ids|Comment IDs|18",
        ({**row, "location": "\n".join(filter(None, (row.get("locator"), row["note"])))}
         for row in coverage_rows),
    )
    table(
        "Analysis Matrix",
        "focus|Analysis|31;slot|Requirement|22;status|Result|18;"
        "protocol|Prespecified content and location|56;note|Assessment|46;finding_ids|Comment IDs|18",
        ({
            **row,
            "focus": (
                f"{analyses[row['analysis_id']]['unit_id']} · {row['analysis_id']}\n"
                f"{analyses[row['analysis_id']]['title']} ({analyses[row['analysis_id']]['role']})"
            ),
            "protocol": "\n".join(filter(None, (row.get("value"), row.get("locator")))),
        } for row in bundle["analysis_matrix"]),
    )
    if details:
        table("Traceability", "focus|Reference|35;detail|Detail|53;evidence|Source|60;note|Assessment|48",
              traceability_rows(bundle, docs, sources))
    return workbook


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["plan", "check", "build"])
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--details", action="store_true", help="Include the optional Traceability tab")
    args = parser.parse_args(argv)
    try:
        checklist = yaml.safe_load(CHECKLIST.read_text(encoding="utf-8"))
        bundle = json.loads(args.input.read_text(encoding="utf-8-sig"))
        review, docs, units = get_scope(bundle, checklist)
        plan = list(plan_checks(units, docs, checklist))
        if args.command == "plan":
            for unit, item, state, note in plan:
                print(f"{unit}\t{item['id']}\t{state}\t{note}")
            if "analyses" in bundle:
                _, required_slots = analysis_plan(bundle, checklist, units)
                for analysis, slots in required_slots.items():
                    for slot in slots:
                        print(f"{analysis}\t{slot}\treview-analysis")
            return 0

        sources, findings, coverage, analyses = validate(bundle, checklist, docs, units, plan)
        if args.command == "check":
            print(f"Validated {len(units)} unit(s), {len(coverage)} review records, {len(findings)} finding(s)")
            return 0

        require(args.out is not None and args.out.suffix.lower() == ".xlsx", "build requires --out ending in .xlsx")
        workbook = build_workbook(
            bundle, checklist, review, docs, units, plan, sources, findings, coverage, analyses,
            details=args.details,
        )
        with io.BytesIO() as buffer:
            workbook.save(buffer)
            with args.out.open("xb") as output:
                try:
                    output.write(buffer.getbuffer())
                    output.flush()
                except OSError:
                    output.close()
                    args.out.unlink()
                    raise
        print(f"Created {args.out}")
        return 0
    except (ValueError, OSError) as exc:
        parser.exit(2, f"error: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
