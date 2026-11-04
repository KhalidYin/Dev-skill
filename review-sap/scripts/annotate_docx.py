#!/usr/bin/env python3
"""Insert review findings as Word comments into a COPY of the SAP .docx.

Run only after the user has explicitly confirmed docx output. The script
requires --confirmed, never writes to the input path, and refuses to
overwrite an existing output file.

Usage:
  annotate_docx.py --run-dir RUN --sap SAP.docx --out SAP_reviewed.docx --confirmed
      [--min-severity Minor] [--author "SAP Review (AI-assisted)"] [--initials AI]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_issue_log import (  # noqa: E402
    SEVERITIES, RecordError, check_records, load_checklist, read_staged)

RANK = {"Critical": 0, "Major": 1, "Minor": 2, "Editorial": 3, "n/a": 4}
SECTION_LOCATOR = re.compile(
    r"^\s*(?:sec(?:tion)?\.?\s*|§\s*|第\s*)?(\d+(?:\.\d+)*)(?=$|[\s,:，：节]|\.(?!\d))",
    re.IGNORECASE,
)
NUMBERED_HEADING = re.compile(r"^\s*(\d+(?:\.\d+)*)(?:[.、])?(?:\s+\S|$)")


def _norm(text: str) -> str:
    text = text.replace("“", '"').replace("”", '"').replace("’", "'")
    return re.sub(r"\s+", " ", text).strip().lower()


def iter_paragraphs(container):
    """Yield body paragraphs and table-cell paragraphs in document order."""
    from docx.text.paragraph import Paragraph

    for block in container.iter_inner_content():
        if isinstance(block, Paragraph):
            yield block
            continue
        seen_cells = set()
        for row in block.rows:
            for cell in row.cells:
                if cell._tc not in seen_cells:
                    seen_cells.add(cell._tc)
                    yield from iter_paragraphs(cell)


def find_anchor(paragraphs, finding):
    """Return (paragraph, method) for a finding, or (None, reason)."""
    excerpt = _norm(finding["sap_excerpt"])
    candidates = [p for p in paragraphs if p.runs and p.text.strip()]
    heading = None
    locator = SECTION_LOCATOR.match(finding["sap_locator"])
    if locator:
        number = locator.group(1)
        headings = []
        for index, paragraph in enumerate(candidates):
            match = NUMBERED_HEADING.match(paragraph.text)
            if match and len(paragraph.text) < 200:
                headings.append((index, match.group(1)))
        starts = [index for index, section in headings if section == number]
        if len(starts) > 1:
            return None, "ambiguous-section"
        if starts:
            start = starts[0]
            end = next((index for index, section in headings
                        if index > start and not section.startswith(number + ".")),
                       len(candidates))
            heading = candidates[start]
            candidates = candidates[start:end]

    if excerpt:
        matches = [p for p in candidates if excerpt in _norm(p.text)]
        if len(matches) == 1:
            return matches[0], "excerpt"
        if matches:
            return None, "ambiguous-excerpt"
    if heading is not None:
        return heading, "section-heading"
    return None, "no-match"


def comment_text(f) -> str:
    items = ", ".join(f["checklist_items"]) or "out of scope"
    parts = [f"[{f['finding_id']} | {f['severity']} | {f['dimension']} | {f['type']} | {items}]",
             f["issue"], f"Recommendation: {f['recommendation']}"]
    if f["comparator_source"]:
        parts.append(f"Comparator: {f['comparator_source']} {f['comparator_locator']}")
    parts.append("AI-assisted review comment; requires statistician confirmation.")
    return "\n".join(parts)


def annotate(run_dir: Path, sap: Path, out: Path, min_severity: str,
             author: str, initials: str) -> dict:
    import docx

    checklist = load_checklist()
    errors, grouped = check_records(read_staged(run_dir), checklist)
    if errors:
        raise RecordError("Staged records fail check; run build_issue_log.py check first.")
    limit = RANK[min_severity]
    findings = sorted((f for f in grouped["finding"] if RANK[f["severity"]] <= limit),
                      key=lambda f: (RANK[f["severity"]], f["finding_id"]))

    doc = docx.Document(str(sap))
    paragraphs = list(iter_paragraphs(doc))
    result = {"anchored": [], "unanchored": []}
    for f in findings:
        para, method = find_anchor(paragraphs, f)
        if para is None:
            result["unanchored"].append(f["finding_id"])
            continue
        doc.add_comment(para.runs, text=comment_text(f), author=author, initials=initials)
        result["anchored"].append((f["finding_id"], method))

    if result["unanchored"]:
        first = next((p for p in paragraphs if p.runs and p.text.strip()), None)
        if first is not None:
            summary = ("Findings that could not be anchored to SAP text (see the Excel issue "
                       "log for locators): " + ", ".join(result["unanchored"]))
            doc.add_comment(first.runs, text=summary, author=author, initials=initials)
    tmp = out.with_name(out.name + ".tmp")
    doc.save(str(tmp))
    tmp.replace(out)
    return result


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--run-dir", required=True, type=Path)
    parser.add_argument("--sap", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--confirmed", action="store_true",
                        help="Required: the user explicitly confirmed docx output.")
    parser.add_argument("--min-severity", default="Editorial", choices=SEVERITIES)
    parser.add_argument("--author", default="SAP Review (AI-assisted)")
    parser.add_argument("--initials", default="AI")
    args = parser.parse_args(argv)

    if not args.confirmed:
        print("Refusing to run: docx output needs explicit user confirmation (--confirmed).")
        return 2
    if args.sap.suffix.lower() != ".docx":
        print("The SAP must be a .docx file.")
        return 1
    if args.out.resolve() == args.sap.resolve():
        print("Output path must differ from the input SAP.")
        return 1
    if args.out.exists():
        print(f"Refusing to overwrite existing file: {args.out}")
        return 1
    try:
        res = annotate(args.run_dir, args.sap, args.out, args.min_severity,
                       args.author, args.initials)
    except RecordError as exc:
        print(f"REJECTED: {exc}")
        return 1
    print(f"WROTE: {args.out}")
    print(f"  anchored: {len(res['anchored'])} {res['anchored']}")
    print(f"  unanchored: {len(res['unanchored'])} {res['unanchored']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
