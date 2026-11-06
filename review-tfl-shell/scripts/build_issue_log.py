"""Build a three-tab, evidence-linked TFL mock-shell review workbook."""
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
STATES = {"pass", "finding", "not-applicable", "not-assessable"}
PRIORITIES = {"Critical", "Major", "Minor", "Editorial", "Query"}
TRACKING = ("Open", "Responded", "Closed")
COLLECTION_ROLES = {"crf", "collection-spec", "external-spec"}
ROLES = COLLECTION_ROLES | {"shell", "sap", "protocol", "convention", "adam-spec", "reference", "other"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def text_fields(row, names, label):
    require(isinstance(row, dict), f"{label}: object required")
    for name in names.split():
        require(isinstance(row.get(name), str) and row[name].strip(), f"{label}: missing {name}")


def list_ids(row, key):
    values = row.get(key, [])
    require(isinstance(values, list) and all(isinstance(v, str) and v.strip() for v in values),
            f"{key}: ID list required")
    require(len(set(values)) == len(values), f"{key}: duplicate IDs")
    return values


def indexed(bundle, key, fields):
    rows = bundle.get(key)
    require(isinstance(rows, list), f"{key}: list required")
    result = {}
    for row in rows:
        text_fields(row, "id " + fields, key)
        require(row["id"] not in result, f"{key}: duplicate {row['id']}")
        result[row["id"]] = row
    return result


def evidence(records, docs, label):
    require(isinstance(records, list) and records, f"{label}: evidence required")
    for row in records:
        text_fields(row, "doc_id locator text", label)
        require(row["doc_id"] in docs, f"{label}: unknown evidence document")


def intake(bundle, checklist):
    require(isinstance(bundle, dict), "Review must be an object")
    review = bundle.get("review")
    text_fields(review, "title date checklist_version study_context scope limitations", "review")
    require(review["checklist_version"] == checklist["checklist_version"], "Checklist version mismatch")
    docs = indexed(bundle, "documents", "role title version date location")
    require(all(d["role"] in ROLES for d in docs.values()), "Unknown document role")
    shells = indexed(bundle, "shells", "document_id type title locator")
    require(shells, "At least one shell required")
    analyses = indexed(bundle, "analyses", "document_id title locator")
    require(not (shells.keys() & analyses.keys()), "Shell and analysis IDs must differ")
    for row in analyses.values():
        require(docs.get(row["document_id"], {}).get("role") == "sap", f"{row['id']}: SAP document required")
    for row in shells.values():
        require(row["type"] in {"T", "F", "L"}, f"{row['id']}: type must be T, F or L")
        require(docs.get(row["document_id"], {}).get("role") == "shell", f"{row['id']}: shell document required")
        require(set(list_ids(row, "analysis_ids")) <= analyses.keys(), f"{row['id']}: unknown analysis")
    if any(d["role"] == "sap" for d in docs.values()) and not analyses:
        require(isinstance(review.get("analysis_gap"), str) and review["analysis_gap"].strip(),
                "Supplied SAP needs an analysis inventory or an explicit analysis_gap")
    return review, docs, shells, analyses


def extend_checklist(bundle, checklist):
    items = list(checklist["items"])
    ids = {item["id"] for item in items}
    extras = bundle.get("extra_checks", [])
    require(isinstance(extras, list), "extra_checks: list required")
    for item in extras:
        text_fields(item, "id group target check", "extra check")
        require(item["id"].startswith("X-") and item["id"] not in ids, "Extra check needs a unique X- ID")
        require(item["target"] in {"all", "analysis", "T", "F", "L"}, "Extra check: invalid target")
        require(isinstance(item.get("sap_required"), bool), "Extra check: sap_required boolean required")
        items.append(item)
        ids.add(item["id"])
    return {**checklist, "items": items}


def plan_checks(docs, shells, analyses, checklist):
    roles = {d["role"] for d in docs.values()}
    for item in checklist["items"]:
        targets = analyses if item["target"] == "analysis" else shells
        for target_id, target in targets.items():
            if item["target"] not in {"analysis", "all", target.get("type")}:
                continue
            state, note = "review", ""
            if item["sap_required"] and "sap" not in roles:
                state, note = "not-assessable", "SAP not supplied"
            if item["id"] == "DATA-01" and not roles.intersection(COLLECTION_ROLES):
                state, note = "not-assessable", "Collection or external data specifications not supplied"
            yield target_id, item, state, note


def validate(bundle, docs, shells, analyses, plan):
    findings = indexed(bundle, "findings", "type priority confidence comment rationale")
    targets = shells | analyses
    for fid, finding in findings.items():
        require(finding["type"] in {"omission", "inconsistency", "error", "ambiguity", "clarification", "editorial"},
                f"{fid}: invalid finding type")
        require(finding["priority"] in PRIORITIES, f"{fid}: invalid priority")
        require(finding["confidence"] in {"high", "medium", "low"}, f"{fid}: invalid confidence")
        require(finding.get("status", "Open") in TRACKING, f"{fid}: invalid tracking status")
        for field in ("author_response", "reviewer_followup"):
            require(isinstance(finding.get(field, ""), str), f"{fid}: {field} must be text")
        require(finding["priority"] != "Critical" or finding["confidence"] != "low", f"{fid}: low-confidence Critical")
        target_ids = list_ids(finding, "target_ids")
        require(target_ids and set(target_ids) <= targets.keys(), f"{fid}: invalid targets")
        evidence(finding.get("evidence"), docs, fid)
        for target_id in target_ids:
            require(any(e["doc_id"] == targets[target_id]["document_id"] for e in finding["evidence"]),
                    f"{fid}: missing evidence for {target_id}")
        if finding["priority"] == "Critical" or finding["type"] in {"inconsistency", "error"}:
            locators = {(e["doc_id"], e["locator"]) for e in finding["evidence"]}
            require(len(locators) >= 2, f"{fid}: two evidence locations required")
        if finding["type"] == "ambiguity" and finding["priority"] != "Editorial":
            text_fields(finding, "reading_a reading_b", fid)
            require(finding["reading_a"].strip().casefold() != finding["reading_b"].strip().casefold(),
                    f"{fid}: readings must differ")

    routed = {(tid, item["id"]): state for tid, item, state, _ in plan}
    reviews = bundle.get("checks")
    require(isinstance(reviews, list), "checks: list required")
    checked, referenced = {}, set()
    for row in reviews:
        text_fields(row, "target_id item_id status note", "check")
        pair = (row["target_id"], row["item_id"])
        require(pair in routed and routed[pair] == "review", f"{pair}: inactive or automatic check")
        require(pair not in checked, f"{pair}: duplicate check")
        require(row["status"] in STATES, f"{pair}: invalid status")
        links = list_ids(row, "finding_ids")
        require(bool(links) == (row["status"] == "finding"), f"{pair}: finding links required exactly for finding status")
        if row["status"] == "pass":
            evidence(row.get("evidence"), docs, str(pair))
        for fid in links:
            require(fid in findings and pair[0] in findings[fid]["target_ids"], f"{pair}: invalid finding link {fid}")
            referenced.add((pair[0], fid))
        if pair[1] == "MAP-01" and row["status"] == "pass":
            require(any(pair[0] in s.get("analysis_ids", []) for s in shells.values()),
                    f"{pair}: passing analysis needs a mapped shell")
        checked[pair] = row
    missing = {pair for pair, state in routed.items() if state == "review"} - checked.keys()
    require(not missing, f"Missing coverage: {sorted(missing)}")
    for fid, finding in findings.items():
        require(all((target_id, fid) in referenced for target_id in finding["target_ids"]),
                f"{fid}: each target needs a linked check")
    return findings, checked


# Formatting conventions follow review-protocol; kept local for standalone installation.
def table(workbook, name, headers, rows, widths):
    sheet = workbook.create_sheet(name)
    sheet.append(headers)
    for cell in sheet[1]:
        cell.font = Font(color="FFFFFF", bold=True)
        cell.fill = PatternFill("solid", fgColor="24445D")
    for number, width in enumerate(widths, 1):
        sheet.column_dimensions[get_column_letter(number)].width = width
    for number, values in enumerate(rows, 2):
        for column, value in enumerate(values, 1):
            if isinstance(value, str):
                require(len(value) <= 32767 and not ILLEGAL_CHARACTERS_RE.search(value),
                        f"{name} row {number}: text cannot be represented in Excel")
            cell = sheet.cell(number, column, value)
            if isinstance(value, str):
                cell.data_type = "s"
            cell.alignment = Alignment(vertical="top", wrap_text=True)
    sheet.freeze_panes = "A2"
    sheet.auto_filter.ref = sheet.dimensions
    return sheet


def evidence_text(records, docs):
    return "\n\n".join(
        f"{docs[e['doc_id']]['title']} · v{docs[e['doc_id']]['version']} · {docs[e['doc_id']]['date']}\n"
        f"{e['locator']}\n{e['text']}\n{docs[e['doc_id']]['location']}"
        for e in records
    )


def build(bundle, checklist, review, docs, shells, analyses, plan, findings, checked, details=False):
    wb = Workbook()
    wb.remove(wb.active)
    overview = [
        ["审核", review["title"]], ["日期", review["date"]], ["检查表", checklist["checklist_version"]],
        ["研究类型与分析目标", review["study_context"]],
        ["范围", review["scope"]], ["待补材料与影响", review["limitations"]],
    ]
    overview.extend([f"文件 · {key}", f"{d['title']} · {d['role']} · v{d['version']} · {d['date']}"]
                    for key, d in docs.items())
    if review.get("analysis_gap"):
        overview.append(["SAP 分析清单缺口", review["analysis_gap"]])
    summary = table(wb, "Overview", ["项目", "内容"], overview, [27, 95])
    for priority in ("Critical", "Major", "Minor", "Editorial", "Query"):
        summary.append([priority, f'=COUNTIF(Comments!$C:$C,"{priority}")'])
    for status in TRACKING:
        summary.append([status, f'=COUNTIF(Comments!$G:$G,"{status}")'])

    comment_rows = []
    for fid, finding in findings.items():
        rationale = finding["rationale"]
        if finding.get("reading_a"):
            rationale = f"A. {finding['reading_a']}\nB. {finding['reading_b']}\n{rationale}"
        comment_rows.append([
            fid, ", ".join(finding["target_ids"]), finding["priority"], finding["comment"],
            rationale, evidence_text(finding["evidence"], docs), finding.get("status", "Open"),
            finding.get("author_response", ""), finding.get("reviewer_followup", ""),
        ])
    comments = table(wb, "Comments",
                     ["ID", "Shell／分析", "级别", "作者批注", "理由", "位置、证据与来源", "状态", "作者回复", "复核意见"],
                     comment_rows, [12, 24, 15, 46, 45, 60, 15, 28, 28])
    choices = DataValidation(type="list", formula1='"' + ",".join(TRACKING) + '"')
    choices.showErrorMessage = True
    comments.add_data_validation(choices)
    choices.add(f"G2:G{max(200, comments.max_row + 200)}")
    comments.freeze_panes = "C2"

    groups, detail_rows = {}, []
    targets = shells | analyses
    for tid, item, state, note in plan:
        row = checked.get((tid, item["id"]), {"status": state, "note": note, "finding_ids": []})
        key = (tid, item["group"])
        groups.setdefault(key, []).append(row)
        detail_rows.append([
            tid, item["id"], item["check"], row["status"], row["note"],
            evidence_text(row.get("evidence", []), docs), ", ".join(row.get("finding_ids", [])),
        ])
    mapping = []
    for (tid, group), rows in groups.items():
        target = targets[tid]
        associated = [sid for sid, shell in shells.items() if tid in shell.get("analysis_ids", [])] if tid in analyses else target.get("analysis_ids", [])
        counts = Counter(row["status"] for row in rows)
        findings_here = sorted({fid for row in rows for fid in row.get("finding_ids", [])})
        mapping.append([
            tid, f"{target['title']}\n{target['locator']}", ", ".join(associated), group,
            "; ".join(f"{state} {count}" for state, count in sorted(counts.items())),
            "\n".join(dict.fromkeys(row["note"] for row in rows)), ", ".join(findings_here),
        ])
    table(wb, "SAP-TFL Crosswalk",
          ["对象 ID", "分析／输出及位置", "对应 Shell／分析", "检查组", "覆盖结论", "说明", "批注 ID"],
          mapping, [20, 42, 25, 22, 28, 64, 18])
    if details:
        table(wb, "Check Details", ["对象", "检查项", "检查内容", "结论", "说明", "证据", "批注"],
              detail_rows, [20, 17, 65, 22, 55, 60, 18])
    return wb


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("plan", "check", "build"))
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--details", action="store_true")
    args = parser.parse_args(argv)
    try:
        checklist = yaml.safe_load(CHECKLIST.read_text(encoding="utf-8"))
        bundle = json.loads(args.input.read_text(encoding="utf-8-sig"))
        checklist = extend_checklist(bundle, checklist)
        review, docs, shells, analyses = intake(bundle, checklist)
        plan = list(plan_checks(docs, shells, analyses, checklist))
        if args.command == "plan":
            for tid, item, state, note in plan:
                print(f"{tid}\t{item['id']}\t{state}\t{note}")
            return 0
        findings, checked = validate(bundle, docs, shells, analyses, plan)
        if args.command == "check":
            print(f"Validated {len(shells)} shells, {len(analyses)} analyses and {len(findings)} comments")
            return 0
        require(args.out is not None and args.out.suffix.lower() == ".xlsx", "build needs --out file.xlsx")
        wb = build(bundle, checklist, review, docs, shells, analyses, plan, findings, checked, args.details)
        with io.BytesIO() as buffer:
            wb.save(buffer)
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
    except (ValueError, OSError) as error:
        parser.exit(2, f"error: {error}\n")


if __name__ == "__main__":
    raise SystemExit(main())
