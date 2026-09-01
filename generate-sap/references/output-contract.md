# SAP Output Contract

Apply this contract to the final `SAP Review Draft` and `Generation Evidence Ledger`. It governs structure and traceability only; it does not decide whether a statistical method is appropriate.

## Generic draft headings

When `document.template` is `generic`, render these Markdown level-2 headings once, in this exact order and wording:

1. `## 1. Title Page and Approvals`
2. `## 2. Revision History`
3. `## 3. Table of Contents`
4. `## 4. Abbreviations and Definitions`
5. `## 5. Introduction and Purpose`
6. `## 6. Study Objectives, Design and Treatments`
7. `## 7. Endpoints, Estimands and Intercurrent Events`
8. `## 8. Sample Size, Randomization and Multiplicity`
9. `## 9. Analysis Populations`
10. `## 10. General Statistical Conventions`
11. `## 11. Participant Disposition, Exposure and Compliance`
12. `## 12. Efficacy Analyses`
13. `## 13. Safety Analyses`
14. `## 14. Other Analyses`
15. `## 15. Interim Analyses and Data Monitoring`
16. `## 16. Changes from Protocol-Planned Analyses`
17. `## 17. References`
18. `## 18. Appendices`

Do not rename generic headings to fit the study. A supplied Sponsor template may use its supplied structure; set `document.template` to a non-`generic` identifier and do not claim that it follows the generic heading contract.

## Keep current-study sources separate

The Ledger has two evidence collections with different purposes.

### Current-study source collection

Record the current Protocol, amendments, confirmed study-team decisions, and effective Sponsor conventions in `document.source_versions`. Link their facts inside each `ContentUnit.source_facts`:

```yaml
document:
  source_versions:
    - source_id: SRC-PROTOCOL-001
      source_type: protocol
      title: ""
      version: ""
      date: ""
      status: effective

source_facts:
  - fact_id: FACT-001
    source_id: SRC-PROTOCOL-001
    locator: "Protocol section 3.1"
    summary: "concise supported fact"
```

Allowed current `source_type` values are `protocol`, `protocol-amendment`, `confirmed-decision`, and `sponsor-convention`. The supplied input bundle or run directory is only a transport container; it is never a source or reference.

### External reference collection

Use top-level `references` only for verified public external material. Allowed `reference_type` values are `normative_reference`, `trial_precedent`, and `method_reference`. `ContentUnit.references` contains only IDs defined in this external collection. Never put a current-study Source ID in `ContentUnit.references`.

For a generic external record, require every field:

```yaml
reference_id: REF-001
reference_type: normative_reference | trial_precedent | method_reference
title: ""
authors_or_organization: ""
document_type: guidance | sap | protocol | csr | regulatory-review | publication
version: ""
date: ""
status: final | effective | draft | withdrawn | historical | unknown
direct_url: "https://..."
retrieved_date: YYYY-MM-DD
location:
  section: ""
  page: null
supported_summary: "short paraphrase"
limitations: []
```

For a deeply screened trial precedent, use the nested record in [precedent-research.md](precedent-research.md). Its exact enums are:

- `document.document_type`: `sap`, `protocol`, `csr`, `regulatory-review`, or `publication`;
- `document.status`: `final`, `draft`, `historical`, or `unknown`;
- `similarity.level`: `high`, `medium`, or `low`;
- `use_in_current_sap.role`: `candidate-design`, `drafting-pattern`, or `background-only`;
- `use_in_current_sap.limitation`: exactly `precedent-not-normative`.

All external records need a direct HTTP(S) document URL, retrieval date, and a stable section or page locator. Do not create an external record from a search snippet or inaccessible title.

## Identifier and linkage rules

- Use `SEC-01` through `SEC-18` for the generic section ledger.
- Every `section_status.content_ids` and `section_status.query_ids` value must be defined.
- Every material paragraph maps to one `ContentUnit`; every `ContentUnit.section_id` must exist.
- Every `ContentUnit.source_facts[].source_id` must be defined in `document.source_versions`.
- Every `ContentUnit.references[]` value must be defined in top-level external `references`.
- Every `ContentUnit.open_questions[]` value must be defined in top-level `open_questions`, and every open question must be linked from affected content.
- Render every open query ID in the review draft near the affected content.

Do not expose hidden chain-of-thought. `derivation_summary` is a concise, reviewable account of inputs, declared rules, assumptions, and resulting choice.

## Search outcome

Use exactly one `search_summary.status`:

- `completed`: requested research was performed and the planned screening/deep-read scope was met;
- `limited`: research ran, but access, similarity, version, or evidence quality remained material limitations;
- `unavailable`: research was allowed but the required search/opening capability was unavailable;
- `prohibited`: the user or run protocol explicitly prohibited external research;
- `not-run`: research was not yet performed and was neither reported as prohibited nor attempted as unavailable.

Always keep `queries_run`, `repositories_checked`, and `limitations` as lists; counts as non-negative integers; and `stop_reason` non-empty. Do not use ad hoc statuses such as `bundle-provided` or `not-required`.

## Deterministic Ledger serialization

When creating artifact files and the packaged scripts are available, do not write or append `generation-evidence-ledger.yaml` directly. Send one complete JSON object at a time to `scripts/build_evidence_ledger.py add`; the script parses the record before changing its private staging file. After every record is staged, call `finalize` once to serialize the final YAML in the contract's fixed top-level order.

Use these record types:

| `--record-type` | JSON object represented | Cardinality |
|---|---|---|
| `document` | top-level `document` | exactly one |
| `section_status` | one item in `section_status` | one per section |
| `content_unit` | one item in `content_units` | one per material content unit |
| `open_question` | one item in `open_questions` | zero or more |
| `reference` | one item in external `references` | zero or more |
| `consistency_finding` | one item in `consistency_findings` | zero or more |
| `search_summary` | top-level `search_summary` | exactly one |

Example PowerShell call for one record:

```powershell
$record = @'
{"section_id":"SEC-01","status":"partial","content_ids":["SAP-01-001"],"query_ids":["Q-ADM-001"]}
'@
$OutputEncoding = [Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$env:PYTHONIOENCODING = 'utf-8'
$record | python -X utf8 <generate-sap-skill-directory>/scripts/build_evidence_ledger.py add --output-root <output-directory> --record-type section_status --strip-pipeline-newline
```

After all records:

```text
python <generate-sap-skill-directory>/scripts/build_evidence_ledger.py finalize --output-root <output-directory>
```

Each JSON payload must be a single mapping and no more than 3,500 characters. Use one command per record and keep content values semantically complete. The builder rejects malformed JSON, duplicate singleton records, duplicate stable IDs, missing stable IDs, final-ledger overwrite, and path escape before mutating final YAML. A syntax rejection may be retried only as the same semantic record with corrected JSON syntax; do not use the error as permission to change a statistical decision or unsupported value.

The builder performs serialization safety, not output-contract or statistical validation. It does not add missing fields, repair record meaning, select methods, or resolve conflicts. The structural validator below remains mandatory after finalization.

## Final structural check

When the Draft and Ledger exist as files, resolve the validator relative to the installed `generate-sap` skill directory and run:

```text
python <generate-sap-skill-directory>/scripts/validate_output_contract.py --draft <sap-review-draft.md> --ledger <generation-evidence-ledger.yaml>
```

A non-zero exit means the artifacts remain a review draft that requires repair before delivery. Report the errors; do not silently rewrite the artifacts. This check does not establish statistical adequacy, approval, validation, or regulatory compliance.
