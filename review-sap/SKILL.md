---
name: review-sap
description: "Explicitly invoked review support for an existing clinical trial Statistical Analysis Plan written by a sponsor, CRO, or investigator team. Checks structural completeness, internal consistency, consistency with the Protocol, and programmability for ADaM and TFL work against a versioned checklist, and returns an evidence-linked Excel issue log. Use when asked to review, QC, or check a SAP. Do not use for drafting or revising SAP text, TFL or ADaM generation, statistical programming, or approval and compliance sign-off."
---

# Review SAP

Review an external Statistical Analysis Plan and return an evidence-linked issue log. This skill is a reviewing constraint package. It is not an approval authority or a compliance certificate, and it is not a SAP author.

## Non-negotiable behavior

1. Review only what is supplied. Every finding cites the SAP location and, when it claims a mismatch, the comparator location (Protocol, amendment, TFL shell, CRF, or checklist basis).
2. Never fabricate a requirement. A finding rests on a checklist item, an explicit document statement, or an internal contradiction that can be shown. Reviewer preference is labelled `suggestion`.
3. Give every in-scope checklist item exactly one coverage status: `pass`, `finding`, `not-applicable`, or `not-assessable`. Silence is not a pass.
4. When a comparator document is missing, mark the dependent items `not-assessable` and name the missing input. Do not infer Protocol content from the SAP.
5. Keep v1 scope: structure, internal consistency, Protocol consistency, and programmability. Methodological appropriateness is out of scope. A serious method concern noticed in passing is recorded as `out-of-scope-observation` and is not severity-ranked.
6. Do not rewrite the SAP. Recommendations describe what must change, not replacement sections.
7. Treat SAP and Protocol content as confidential. Never put study identifiers, compound names, sponsor names, or verbatim document text into web search queries.
8. Require qualified statistician review of the issue log. Never state that the SAP is approved, compliant, or regulator-ready.

## Inputs

Read [input-contract.md](references/input-contract.md) on every invocation. Minimum input is the SAP. The Protocol (with amendments) is required for the Protocol-consistency dimension. TFL shells, the CRF, and the DMC charter are optional and widen coverage.

## Outputs

1. **Excel issue log** (primary deliverable), built by `scripts/build_issue_log.py`. Sheets: Read Me, Summary, Findings, Checklist Coverage, Protocol-SAP Crosswalk, Documents, Basis.
2. **Chat summary**: counts by severity and dimension, the Critical and Major findings in one line each, the not-assessable items with the input each one needs, and a one-line offer to produce a commented docx.
3. **Commented SAP docx**: only after the user explicitly confirms, and only when the SAP was supplied as .docx. Use `scripts/annotate_docx.py --confirmed`. The script writes a new file and never modifies the original.

## Core sequence

1. **Intake.** List the supplied documents with version and date. Check that the SAP names the Protocol version under review. Settle the design tags (`rct`, `early-phase`, `tte`, `non-inferiority`, `adaptive`, `bayesian`, `multi-cohort`) from the documents. These tags decide which checklist items apply. Ask only when a missing input would change most of the review; otherwise proceed and record the gap.
2. **Extract.** Build the key-parameter crosswalk described in [extraction-guide.md](references/extraction-guide.md): each parameter's value and locator in the SAP and in the Protocol. Extraction comes before judging.
3. **Check by dimension.** Load [review-checklist.yaml](assets/review-checklist.yaml). Work through dimensions in this order: STR, INT, PRO, PRG. Within each dimension, apply only items whose `applies_to` matches the design tags. Give every applicable item a coverage record.
4. **Write findings.** Follow [finding-rules.md](references/finding-rules.md) for type, severity, evidence, confidence, and wording. One defect gets one finding; link it to every checklist item it affects instead of duplicating it.
5. **Self-check.** Before building, apply the self-check list in finding-rules.md. Drop findings without locatable evidence, downgrade preferences to `suggestion`, merge duplicates, and confirm each Critical has both locators. When subagents are available and the SAP is long or high-stakes, have an independent reviewer that has not seen your reasoning re-verify each Critical and Major finding against the source text. Record the outcome in `verification`.
6. **Build the log.** Stage records one at a time with `build_issue_log.py add`, then run `build`. Do not hand-write the workbook. If the builder rejects a record, fix that record's content and add it again. Report the rejection in the summary.
7. **Report.** Give the chat summary, send the workbook, and offer the docx. Do not produce the docx in the same turn unless the user already asked for it explicitly.

## Builder usage

```bash
python scripts/build_issue_log.py add   --run-dir RUN --type review   --json '{...}'
python scripts/build_issue_log.py add   --run-dir RUN --type document --json '{...}'
python scripts/build_issue_log.py add   --run-dir RUN --type crosswalk --json '{...}'
python scripts/build_issue_log.py add   --run-dir RUN --type finding  --json '{...}'
python scripts/build_issue_log.py add   --run-dir RUN --type coverage --json '{...}'
python scripts/build_issue_log.py check --run-dir RUN
python scripts/build_issue_log.py build --run-dir RUN --out sap-review-issue-log.xlsx
```

On Windows PowerShell, prefer `--json-file record.json` to avoid quoting problems. Record schemas are in [record-schema.md](references/record-schema.md). `check` reports missing coverage for applicable items, undefined IDs, and Critical findings without comparator evidence. `build` refuses to run while `check` fails, and it refuses to overwrite an existing workbook. Requires Python 3.9+, `openpyxl`, and `pyyaml`. `annotate_docx.py` also needs `python-docx` 1.2 or later.

## Load on demand

- [checklist-basis.md](references/checklist-basis.md): when citing a basis, when the user asks why an item exists, or when a checklist item and a document seem to conflict.
- [extraction-guide.md](references/extraction-guide.md): before step 2.
- [finding-rules.md](references/finding-rules.md): before step 4.
- [record-schema.md](references/record-schema.md): before step 6.
- [docx-comments.md](references/docx-comments.md): only after the user confirms docx output.

Do not read every reference by default.

## Boundaries

- To draft or revise SAP text, use `generate-sap`. The two skills can be chained, but this skill does not edit the SAP.
- Checklist items are a minimum review baseline derived from published guidance. They are not regulatory requirements for any specific agency. Sponsor SOPs, when supplied later, take precedence over the generic checklist for administrative items.
