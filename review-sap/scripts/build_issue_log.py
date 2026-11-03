#!/usr/bin/env python3
"""Stage, check, and build the review-sap Excel issue log.

The builder serializes review records into a workbook. It validates structure and
cross-references only. It never changes the meaning of a finding or decides
whether a SAP is acceptable.

Usage:
  build_issue_log.py add   --run-dir RUN --type TYPE --json '{...}'
  build_issue_log.py add   --run-dir RUN --type TYPE --json-file record.json
  build_issue_log.py check --run-dir RUN
  build_issue_log.py build --run-dir RUN --out issue-log.xlsx
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

import yaml

SKILL_ROOT = Path(__file__).resolve().parent.parent
CHECKLIST_PATH = SKILL_ROOT / "assets" / "review-checklist.yaml"
STAGING_NAME = "review-records.jsonl"
MAX_RECORD_BYTES = 64 * 1024

DIMENSIONS = ["STR", "INT", "PRO", "PRG"]
FINDING_DIMENSIONS = DIMENSIONS + ["MTH"]
DOC_ROLES = ["sap", "protocol", "protocol-amendment", "tfl_shells", "crf",
             "dmc_charter", "sponsor_sop", "prior_sap", "other"]
MATCH_VALUES = ["match", "mismatch", "sap-only", "protocol-only", "declared-change", "unclear"]
FINDING_TYPES = ["error", "inconsistency", "omission", "ambiguity", "suggestion",
                 "out-of-scope-observation"]
SEVERITIES = ["Critical", "Major", "Minor", "Editorial", "n/a"]
CONFIDENCE = ["high", "medium", "low"]
VERIFICATION = ["self", "independent-confirmed", "independent-disputed"]
COVERAGE_STATUS = ["pass", "finding", "not-applicable", "not-assessable"]
TRACKING_STATUS = ["Open", "Accepted", "Rejected", "Resolved", "Closed"]

# field -> (kind, required). kind: str | list | enum:<name> | date | id:<regex>
SCHEMAS = {
    "review": {
        "review_id": (r"id:^RV-\d{3}$", True),
        "title": ("str", True),
        "sap_document_id": (r"id:^DOC-\d{2}$", True),
        "review_date": ("date", True),
        "reviewer": ("str", True),
        "design_tags": ("list", True),
        "dimensions_in_scope": ("list", True),
        "checklist_version": ("str", True),
        "language": ("str", True),
        "limitations": ("list", False),
    },
    "document": {
        "document_id": (r"id:^DOC-\d{2}$", True),
        "role": ("enum:DOC_ROLES", True),
        "title": ("str", True),
        "version": ("str", True),
        "date": ("str", False),
        "file_name": ("str", False),
    },
    "crosswalk": {
        "row_id": (r"id:^XW-\d{3}$", True),
        "group": ("str", True),
        "parameter": ("str", True),
        "sap_value": ("str", False),
        "sap_locator": ("str", False),
        "protocol_value": ("str", False),
        "protocol_locator": ("str", False),
        "match": ("enum:MATCH_VALUES", True),
        "finding_ids": ("list", False),
        "note": ("str", False),
    },
    "finding": {
        "finding_id": (r"id:^F-\d{3}$", True),
        "dimension": ("enum:FINDING_DIMENSIONS", True),
        "checklist_items": ("list", True),
        "type": ("enum:FINDING_TYPES", True),
        "severity": ("enum:SEVERITIES", True),
        "sap_locator": ("str", True),
        "sap_excerpt": ("str", True),
        "comparator_source": ("str", False),
        "comparator_locator": ("str", False),
        "comparator_excerpt": ("str", False),
        "issue": ("str", True),
        "recommendation": ("str", True),
        "rationale": ("str", True),
        "confidence": ("enum:CONFIDENCE", True),
        "verification": ("enum:VERIFICATION", True),
    },
    "coverage": {
        "item_id": ("str", True),
        "status": ("enum:COVERAGE_STATUS", True),
        "finding_ids": ("list", False),
        "note": ("str", True),
    },
}
ID_FIELD = {"review": "review_id", "document": "document_id", "crosswalk": "row_id",
            "finding": "finding_id", "coverage": "item_id"}
ENUMS = {"DOC_ROLES": DOC_ROLES, "MATCH_VALUES": MATCH_VALUES, "FINDING_TYPES": FINDING_TYPES,
         "SEVERITIES": SEVERITIES, "CONFIDENCE": CONFIDENCE, "VERIFICATION": VERIFICATION,
         "COVERAGE_STATUS": COVERAGE_STATUS, "FINDING_DIMENSIONS": FINDING_DIMENSIONS}


class RecordError(ValueError):
    """Raised when a single record or the staged set is invalid."""


def load_checklist(path: Path = CHECKLIST_PATH) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    data["by_id"] = {item["id"]: item for item in data["items"]}
    return data


def staging_path(run_dir: Path) -> Path:
    return run_dir / STAGING_NAME


def read_staged(run_dir: Path) -> list[dict]:
    path = staging_path(run_dir)
    if not path.exists():
        return []
    records = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.strip():
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise RecordError(f"Staging file line {line_no} is corrupt: {exc}") from exc
    return records


def normalize_record(record_type: str, value: object, checklist: dict) -> dict:
    """Validate one record's own fields and return a normalized copy."""
    if record_type not in SCHEMAS:
        raise RecordError(f"Unknown record type '{record_type}'. Allowed: {', '.join(SCHEMAS)}")
    if not isinstance(value, dict):
        raise RecordError("Record must be a JSON object.")
    schema = SCHEMAS[record_type]
    unknown = sorted(set(value) - set(schema))
    if unknown:
        raise RecordError(f"{record_type}: unknown field(s) {unknown}. Allowed: {sorted(schema)}")

    out: dict = {}
    for field, (kind, required) in schema.items():
        raw = value.get(field)
        if kind == "list":
            if raw is None:
                raw = []
            if not isinstance(raw, list) or not all(isinstance(x, str) for x in raw):
                raise RecordError(f"{record_type}.{field} must be a list of strings.")
            items = [x.strip() for x in raw if x.strip()]
            if required and not items and not (record_type == "finding" and field == "checklist_items"):
                raise RecordError(f"{record_type}.{field} must not be empty.")
            out[field] = items
            continue
        if raw is None:
            raw = ""
        if not isinstance(raw, str):
            raise RecordError(f"{record_type}.{field} must be a string.")
        text = raw.strip()
        if required and not text:
            raise RecordError(f"{record_type}.{field} is required.")
        if text and kind.startswith("enum:"):
            allowed = ENUMS[kind[5:]]
            if text not in allowed:
                raise RecordError(f"{record_type}.{field}='{text}' not in {allowed}.")
        elif text and kind.startswith("id:"):
            if not re.match(kind[3:], text):
                raise RecordError(f"{record_type}.{field}='{text}' does not match {kind[3:]}.")
        elif text and kind == "date":
            try:
                date.fromisoformat(text)
            except ValueError as exc:
                raise RecordError(f"{record_type}.{field} must be YYYY-MM-DD.") from exc
        out[field] = text

    _validate_semantics(record_type, out, checklist)
    return out


def _validate_semantics(record_type: str, rec: dict, checklist: dict) -> None:
    if record_type == "review":
        bad_tags = [t for t in rec["design_tags"] if t not in checklist["design_tags"] or t == "all"]
        if bad_tags:
            raise RecordError(f"review.design_tags has unknown or redundant tags {bad_tags}.")
        bad_dims = [d for d in rec["dimensions_in_scope"] if d not in DIMENSIONS]
        if bad_dims:
            raise RecordError(f"review.dimensions_in_scope has unknown dimensions {bad_dims}.")
        if rec["checklist_version"] != str(checklist["checklist_version"]):
            raise RecordError(
                f"review.checklist_version {rec['checklist_version']} != packaged "
                f"{checklist['checklist_version']}.")
    elif record_type == "crosswalk":
        if not rec["sap_value"] and not rec["protocol_value"]:
            raise RecordError("crosswalk needs at least one of sap_value or protocol_value.")
        if rec["match"] not in ("protocol-only", "declared-change") and not rec["sap_value"]:
            raise RecordError("crosswalk.sap_value is required unless match is protocol-only "
                              "or declared-change.")
        if rec["match"] not in ("sap-only", "declared-change") and not rec["protocol_value"]:
            raise RecordError("crosswalk.protocol_value is required unless match is sap-only "
                              "or declared-change.")
    elif record_type == "finding":
        ftype, sev = rec["type"], rec["severity"]
        if ftype == "out-of-scope-observation":
            if sev != "n/a" or rec["dimension"] != "MTH" or rec["checklist_items"]:
                raise RecordError("out-of-scope-observation needs severity n/a, dimension MTH, "
                                  "and checklist_items [].")
        else:
            if sev == "n/a" or rec["dimension"] == "MTH":
                raise RecordError("Only out-of-scope-observation may use severity n/a or dimension MTH.")
            if not rec["checklist_items"]:
                raise RecordError("finding.checklist_items must not be empty.")
            unknown = [i for i in rec["checklist_items"] if i not in checklist["by_id"]]
            if unknown:
                raise RecordError(f"finding.checklist_items not in checklist: {unknown}.")
        if ftype == "suggestion" and sev not in ("Minor", "Editorial"):
            raise RecordError("A suggestion can only be Minor or Editorial.")
        if rec["confidence"] == "low" and sev == "Critical":
            raise RecordError("A low-confidence finding cannot be Critical.")
        needs_comparator = ftype in ("error", "inconsistency") or rec["dimension"] == "PRO"
        if needs_comparator:
            missing = [f for f in ("comparator_source", "comparator_locator", "comparator_excerpt")
                       if not rec[f]]
            if missing:
                raise RecordError(f"finding {rec['finding_id']} needs comparator evidence: {missing}.")
    elif record_type == "coverage":
        if rec["item_id"] not in checklist["by_id"]:
            raise RecordError(f"coverage.item_id '{rec['item_id']}' is not a checklist item.")
        if (rec["status"] == "finding") != bool(rec["finding_ids"]):
            raise RecordError("coverage.finding_ids must be non-empty exactly when status is finding.")


def append_record(run_dir: Path, record_type: str, raw_json: str,
                  checklist: dict | None = None) -> dict:
    """Validate one record and append it to staging. Staging is untouched on failure."""
    checklist = checklist or load_checklist()
    if len(raw_json.encode("utf-8")) > MAX_RECORD_BYTES:
        raise RecordError(f"Record exceeds {MAX_RECORD_BYTES} bytes; split the content.")
    try:
        value = json.loads(raw_json)
    except json.JSONDecodeError as exc:
        raise RecordError(f"Invalid JSON: {exc}") from exc
    rec = normalize_record(record_type, value, checklist)
    existing = read_staged(run_dir)
    id_field = ID_FIELD[record_type]
    if record_type == "review" and any(r["_type"] == "review" for r in existing):
        raise RecordError("A review record is already staged.")
    for r in existing:
        if r["_type"] == record_type and r.get(id_field) == rec[id_field]:
            raise RecordError(f"Duplicate {record_type} id '{rec[id_field]}'.")
    run_dir.mkdir(parents=True, exist_ok=True)
    with staging_path(run_dir).open("a", encoding="utf-8") as fh:
        fh.write(json.dumps({"_type": record_type, **rec}, ensure_ascii=False) + "\n")
    return rec


def applicable_items(checklist: dict, review: dict) -> list[dict]:
    tags = set(review["design_tags"]) | {"all"}
    scope = set(review["dimensions_in_scope"])
    return [i for i in checklist["items"]
            if i["dimension"] in scope and tags & set(i["applies_to"])]


def check_records(records: list[dict], checklist: dict) -> tuple[list[str], dict]:
    """Return (errors, grouped records). Empty errors means the set is buildable."""
    errors: list[str] = []
    grouped: dict[str, list[dict]] = {t: [] for t in SCHEMAS}
    for r in records:
        grouped[r["_type"]].append(r)

    if len(grouped["review"]) != 1:
        errors.append(f"Exactly one review record is required (found {len(grouped['review'])}).")
        return errors, grouped
    review = grouped["review"][0]
    docs = {d["document_id"]: d for d in grouped["document"]}
    roles = {d["role"] for d in docs.values()}
    sap_doc = docs.get(review["sap_document_id"])
    if not sap_doc or sap_doc["role"] != "sap":
        errors.append(f"review.sap_document_id {review['sap_document_id']} is not a defined sap document.")

    findings = {f["finding_id"]: f for f in grouped["finding"]}
    coverage = {}
    for c in grouped["coverage"]:
        if c["item_id"] in coverage:
            errors.append(f"Duplicate coverage for {c['item_id']}.")
        coverage[c["item_id"]] = c

    applicable = {i["id"]: i for i in applicable_items(checklist, review)}
    for item_id in applicable:
        if item_id not in coverage:
            errors.append(f"Missing coverage for applicable item {item_id}.")
    for item_id, c in coverage.items():
        item = checklist["by_id"][item_id]
        if item_id not in applicable and c["status"] != "not-applicable":
            errors.append(f"{item_id} is not applicable to this review but has status {c['status']}.")
        if c["status"] in ("pass", "finding"):
            has_required = set(item["requires"]) <= roles
            has_alternate = set(item.get("alternate_requires", ["__none__"])) <= roles
            if not (has_required or has_alternate):
                missing = sorted(set(item["requires"]) - roles)
                errors.append(f"{item_id} needs {missing} but is marked {c['status']}; "
                              f"use not-assessable.")
        for fid in c["finding_ids"]:
            if fid not in findings:
                errors.append(f"coverage {item_id} references undefined finding {fid}.")

    referenced = set()
    for c in coverage.values():
        referenced.update(c["finding_ids"])
    for fid, f in findings.items():
        src = f["comparator_source"]
        if src and src != "SAP" and src not in docs:
            errors.append(f"{fid}.comparator_source '{src}' is not a defined document or 'SAP'.")
        for item_id in f["checklist_items"]:
            c = coverage.get(item_id)
            if not c or c["status"] != "finding" or fid not in c["finding_ids"]:
                errors.append(f"{fid} lists {item_id} but that item's coverage does not list {fid}.")
        if f["dimension"] != "MTH" and fid not in referenced:
            errors.append(f"{fid} is not referenced by any coverage record.")
    for x in grouped["crosswalk"]:
        for fid in x["finding_ids"]:
            if fid not in findings:
                errors.append(f"crosswalk {x['row_id']} references undefined finding {fid}.")
    return errors, grouped


# ---------------------------------------------------------------- workbook

def build_workbook(grouped: dict, checklist: dict, out_path: Path) -> None:
    from openpyxl import Workbook
    from openpyxl.formatting.rule import FormulaRule
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter
    from openpyxl.worksheet.datavalidation import DataValidation

    review = grouped["review"][0]
    header_fill = PatternFill("solid", fgColor="1F3864")
    header_font = Font(bold=True, color="FFFFFF")
    wrap = Alignment(wrap_text=True, vertical="top")
    sev_fill = {"Critical": "F8CBAD", "Major": "FCE4D6", "Minor": "FFF2CC", "Editorial": "E2EFDA"}

    wb = Workbook()

    def table(ws, headers, rows, widths):
        ws.append([h for h, _ in headers])
        for col, _ in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col)
            cell.fill, cell.font = header_fill, header_font
            cell.alignment = Alignment(wrap_text=True, vertical="center")
        for row in rows:
            ws.append(row)
        for col, width in enumerate(widths, 1):
            ws.column_dimensions[get_column_letter(col)].width = width
        for row in ws.iter_rows(min_row=2):
            for cell in row:
                cell.alignment = wrap
        ws.row_dimensions[1].height = 32
        ws.freeze_panes = "B2"
        if rows:
            ws.auto_filter.ref = f"A1:{get_column_letter(len(headers))}{len(rows) + 1}"

    # Read Me
    ws = wb.active
    ws.title = "Read Me"
    lines = [
        ("SAP Review Issue Log / SAP 审阅问题清单", True),
        (review["title"], True),
        ("", False),
        ("Status: AI-assisted review draft. Every finding requires confirmation by a qualified "
         "statistician. This log is not an approval or a regulatory compliance assessment. / "
         "状态：AI 辅助审阅草稿，所有问题须经合格统计师确认；本清单不代表批准或法规合规结论。", False),
        ("", False),
        (f"Review ID: {review['review_id']}", False),
        (f"Review date: {review['review_date']}", False),
        (f"Reviewer: {review['reviewer']}", False),
        (f"Checklist version: {review['checklist_version']}", False),
        (f"Dimensions in scope: {', '.join(review['dimensions_in_scope'])}", False),
        (f"Design tags: {', '.join(review['design_tags']) or '(all only)'}", False),
        ("", False),
        ("Severity / 严重度", True),
        ("Critical: primary or key secondary analysis cannot be done as written, or answers a "
         "different question than the Protocol. / 主要或关键次要分析无法按现文执行，或与方案问题不一致。", False),
        ("Major: likely to change secondary, sensitivity, or safety results, or an important "
         "derivation is ambiguous. / 可能影响次要、敏感性或安全性结果，或重要衍生规则有歧义。", False),
        ("Minor: limited effect on results; clarification needed. / 对结果影响有限，需澄清。", False),
        ("Editorial: wording, formatting, cross-references. / 文字、格式、交叉引用。", False),
        ("n/a: out-of-scope observation (methodology), not ranked in v1. / 范围外观察（方法学），v1 不分级。", False),
        ("", False),
        ("Tracking: update Status, Author Response and Reviewer Follow-up on the Findings sheet; "
         "Summary counts update automatically. / 跟踪：在 Findings 表更新状态与回复，Summary 自动汇总。", False),
        ("", False),
        ("Limitations / 局限", True),
    ] + [(f"- {x}", False) for x in (review["limitations"] or ["None recorded."])]
    for text, bold in lines:
        ws.append([text])
        ws.cell(row=ws.max_row, column=1).font = Font(bold=bold, size=12 if bold else 11)
        ws.cell(row=ws.max_row, column=1).alignment = Alignment(wrap_text=True, vertical="top")
    ws.column_dimensions["A"].width = 120

    # Findings
    sev_order = {s: i for i, s in enumerate(SEVERITIES)}
    findings = sorted(grouped["finding"], key=lambda f: (sev_order[f["severity"]], f["finding_id"]))
    docs = {d["document_id"]: d for d in grouped["document"]}

    def source_label(src):
        if src in docs:
            d = docs[src]
            return f"{src} {d['role']} v{d['version']}"
        return src

    f_headers = [
        ("Finding ID\n问题编号", 11), ("Severity\n严重度", 11), ("Dimension\n维度", 10),
        ("Type\n类型", 14), ("Checklist Items\n检查项", 14), ("SAP Locator\nSAP 位置", 16),
        ("SAP Excerpt\nSAP 原文", 40), ("Comparator Source\n对照来源", 16),
        ("Comparator Locator\n对照位置", 16), ("Comparator Excerpt\n对照原文", 40),
        ("Issue\n问题描述", 45), ("Recommendation\n建议", 40), ("Severity Rationale\n分级理由", 30),
        ("Confidence\n置信度", 11), ("Verification\n核验", 14), ("Status\n状态", 11),
        ("Author Response\n作者回复", 30), ("Reviewer Follow-up\n审阅跟进", 30),
        ("Resolved In Version\n解决版本", 14),
    ]
    rows = [[f["finding_id"], f["severity"], f["dimension"], f["type"],
             ", ".join(f["checklist_items"]), f["sap_locator"], f["sap_excerpt"],
             source_label(f["comparator_source"]), f["comparator_locator"],
             f["comparator_excerpt"], f["issue"], f["recommendation"], f["rationale"],
             f["confidence"], f["verification"], "Open", "", "", ""] for f in findings]
    ws = wb.create_sheet("Findings")
    table(ws, f_headers, rows, [w for _, w in f_headers])
    last = max(len(rows) + 1, 2)
    status_dv = DataValidation(type="list", formula1='"' + ",".join(TRACKING_STATUS) + '"',
                               allow_blank=False)
    ws.add_data_validation(status_dv)
    status_dv.add(f"P2:P{max(last, 500)}")
    for sev, color in sev_fill.items():
        ws.conditional_formatting.add(
            f"B2:B{max(last, 500)}",
            FormulaRule(formula=[f'$B2="{sev}"'], fill=PatternFill("solid", fgColor=color)))

    # Summary (formulas so it follows edits on Findings)
    ws = wb.create_sheet("Summary", 1)
    ws.append(["Findings by severity and dimension / 按严重度与维度统计"])
    ws.cell(row=1, column=1).font = Font(bold=True, size=12)
    dims = FINDING_DIMENSIONS
    ws.append(["Severity"] + dims + ["Total", "Open"])
    for col in range(1, len(dims) + 4):
        c = ws.cell(row=2, column=col)
        c.fill, c.font = header_fill, header_font
    for r, sev in enumerate(SEVERITIES, start=3):
        ws.cell(row=r, column=1, value=sev)
        for ci, dim in enumerate(dims, start=2):
            ws.cell(row=r, column=ci,
                    value=f'=COUNTIFS(Findings!$B:$B,"{sev}",Findings!$C:$C,"{dim}")')
        ws.cell(row=r, column=len(dims) + 2, value=f'=COUNTIF(Findings!$B:$B,"{sev}")')
        ws.cell(row=r, column=len(dims) + 3,
                value=f'=COUNTIFS(Findings!$B:$B,"{sev}",Findings!$P:$P,"Open")')
    tot_row = 3 + len(SEVERITIES)
    ws.cell(row=tot_row, column=1, value="Total").font = Font(bold=True)
    for ci in range(2, len(dims) + 4):
        col = get_column_letter(ci)
        ws.cell(row=tot_row, column=ci, value=f"=SUM({col}3:{col}{tot_row - 1})").font = Font(bold=True)

    start = tot_row + 2
    ws.cell(row=start, column=1, value="Checklist coverage / 检查项覆盖").font = Font(bold=True, size=12)
    ws.cell(row=start + 1, column=1, value="Status")
    for ci, dim in enumerate(DIMENSIONS, start=2):
        ws.cell(row=start + 1, column=ci, value=dim)
    ws.cell(row=start + 1, column=len(DIMENSIONS) + 2, value="Total")
    for col in range(1, len(DIMENSIONS) + 3):
        c = ws.cell(row=start + 1, column=col)
        c.fill, c.font = header_fill, header_font
    for r, status in enumerate(COVERAGE_STATUS, start=start + 2):
        ws.cell(row=r, column=1, value=status)
        for ci, dim in enumerate(DIMENSIONS, start=2):
            ws.cell(row=r, column=ci,
                    value=f'=COUNTIFS(\'Checklist Coverage\'!$B:$B,"{dim}",'
                          f'\'Checklist Coverage\'!$E:$E,"{status}")')
        ws.cell(row=r, column=len(DIMENSIONS) + 2,
                value=f'=COUNTIF(\'Checklist Coverage\'!$E:$E,"{status}")')
    ws.column_dimensions["A"].width = 18
    for ci in range(2, len(dims) + 4):
        ws.column_dimensions[get_column_letter(ci)].width = 10

    # Checklist Coverage
    coverage = {c["item_id"]: c for c in grouped["coverage"]}
    applicable = {i["id"] for i in applicable_items(checklist, review)}
    c_headers = [("Item ID\n检查项", 11), ("Dimension\n维度", 10), ("Title\n标题", 30),
                 ("Check\n检查内容", 60), ("Coverage\n结论", 15), ("Finding IDs\n问题编号", 16),
                 ("Note\n说明", 45), ("Basis\n依据", 30), ("Applicable\n适用", 10)]
    rows = []
    for item in checklist["items"]:
        if item["dimension"] not in review["dimensions_in_scope"]:
            continue
        c = coverage.get(item["id"])
        status = c["status"] if c else "not-applicable"
        note = c["note"] if c else "Not applicable to the recorded design tags."
        basis = "; ".join(f"{b['id']} ({b['locator']})" for b in item["basis"])
        rows.append([item["id"], item["dimension"], item["title"], item["check"], status,
                     ", ".join(c["finding_ids"]) if c else "", note, basis,
                     "yes" if item["id"] in applicable else "no"])
    ws = wb.create_sheet("Checklist Coverage")
    table(ws, c_headers, rows, [w for _, w in c_headers])

    # Crosswalk
    x_headers = [("Row ID", 9), ("Group\n类别", 16), ("Parameter\n参数", 24),
                 ("SAP Value\nSAP 值", 32), ("SAP Locator\nSAP 位置", 16),
                 ("Protocol Value\n方案值", 32), ("Protocol Locator\n方案位置", 16),
                 ("Match\n一致性", 14), ("Finding IDs\n问题编号", 14), ("Note\n说明", 36)]
    rows = [[x["row_id"], x["group"], x["parameter"], x["sap_value"], x["sap_locator"],
             x["protocol_value"], x["protocol_locator"], x["match"],
             ", ".join(x["finding_ids"]), x["note"]]
            for x in sorted(grouped["crosswalk"], key=lambda x: x["row_id"])]
    ws = wb.create_sheet("Protocol-SAP Crosswalk")
    table(ws, x_headers, rows, [w for _, w in x_headers])
    for value, color in (("mismatch", "F8CBAD"), ("unclear", "FFF2CC")):
        ws.conditional_formatting.add(
            f"H2:H{max(len(rows) + 1, 2)}",
            FormulaRule(formula=[f'$H2="{value}"'], fill=PatternFill("solid", fgColor=color)))

    # Documents
    d_headers = [("Document ID", 12), ("Role\n角色", 18), ("Title\n标题", 40),
                 ("Version\n版本", 12), ("Date\n日期", 14), ("File\n文件", 36)]
    rows = [[d["document_id"], d["role"], d["title"], d["version"], d["date"], d["file_name"]]
            for d in sorted(grouped["document"], key=lambda d: d["document_id"])]
    ws = wb.create_sheet("Documents")
    table(ws, d_headers, rows, [w for _, w in d_headers])

    # Basis
    b_headers = [("Basis ID", 16), ("Citation\n来源", 70), ("URL", 50), ("Verification\n核验", 30)]
    rows = [[b["id"], b["citation"], b["url"], b["verification"]] for b in checklist["basis_register"]]
    ws = wb.create_sheet("Basis")
    table(ws, b_headers, rows, [w for _, w in b_headers])

    tmp = out_path.with_name(out_path.name + ".tmp")
    wb.save(tmp)
    tmp.replace(out_path)


# ---------------------------------------------------------------- CLI

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)
    p_add = sub.add_parser("add")
    p_add.add_argument("--run-dir", required=True, type=Path)
    p_add.add_argument("--type", required=True, choices=list(SCHEMAS))
    src = p_add.add_mutually_exclusive_group(required=True)
    src.add_argument("--json")
    src.add_argument("--json-file", type=Path)
    p_check = sub.add_parser("check")
    p_check.add_argument("--run-dir", required=True, type=Path)
    p_build = sub.add_parser("build")
    p_build.add_argument("--run-dir", required=True, type=Path)
    p_build.add_argument("--out", required=True, type=Path)
    args = parser.parse_args(argv)

    checklist = load_checklist()
    try:
        if args.cmd == "add":
            raw = args.json if args.json is not None else args.json_file.read_text(encoding="utf-8")
            rec = append_record(args.run_dir, args.type, raw, checklist)
            print(f"OK: staged {args.type} {rec[ID_FIELD[args.type]]}")
            return 0
        records = read_staged(args.run_dir)
        errors, grouped = check_records(records, checklist)
        if errors:
            print(f"CHECK FAILED ({len(errors)} problem(s)):")
            for e in errors:
                print(f"  - {e}")
            return 1
        counts = {t: len(v) for t, v in grouped.items()}
        if args.cmd == "check":
            print(f"CHECK OK: {counts}")
            return 0
        if args.out.exists():
            print(f"Refusing to overwrite existing file: {args.out}")
            return 1
        args.out.parent.mkdir(parents=True, exist_ok=True)
        build_workbook(grouped, checklist, args.out)
        print(f"BUILT: {args.out} {counts}")
        return 0
    except RecordError as exc:
        print(f"REJECTED: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
