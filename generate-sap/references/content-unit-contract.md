# Content Unit and Generation Record Contract

Use one `ContentUnit` for every material SAP statement or tightly related paragraph.

## Allowed generation modes

| Mode | Meaning | Allowed behavior |
|------|---------|------------------|
| `sourced` | Directly supported by an authoritative current source | Draft faithfully and cite the source fact |
| `derived` | Follows from a deterministic declared rule | Draft and record the applied rule and inputs |
| `proposed` | A study-specific choice is not confirmed, but a recommendation is useful | Label conditional, state assumptions and alternatives, add an author query |
| `tbd` | Support is insufficient for a responsible proposal | Retain the structure and state exactly what is missing |
| `conflict` | Authoritative inputs disagree | Preserve the conflict; do not select silently |
| `not-applicable` | The section or item does not apply | State non-applicability and its supported reason |

Never use `approved`, `validated`, or `compliant` as a generation mode.

## ContentUnit schema

```yaml
content_id: SAP-12.2-001
section_id: SEC-12.2
topic: primary-efficacy-method
generation_mode: sourced | derived | proposed | tbd | conflict | not-applicable
status: complete | partial | blocked

source_facts:
  - fact_id: FACT-001
    source_id: SRC-001
    locator: "Protocol 8.1"
    summary: ""

applied_rules:
  - rule_id: EFF-001
    summary: ""

assumptions: []
derivation_summary: "concise reviewable rationale, not hidden chain-of-thought"
alternatives: []
references: []

generated_content:
  paragraph_id: SAP-12.2-P1
  text: ""

open_questions: []
downstream_sections: []
```

## Open question schema

```yaml
query_id: Q-EST-001
origin_section: SEC-07.2
query_type: missing-input | missing-decision | source-conflict | verification-needed
severity: blocking | non-blocking
topic: intercurrent-event-strategy
known: []
missing_or_conflicting: []
impact: []
question: ""
owner: statistician | clinician | programmer | data-management | sponsor
status: open | resolved
affected_sections: []
```

`blocking` is local to the affected content. It must not halt the whole document.

## Required logical outputs

1. `sap_review_draft`: complete target structure and drafted content.
2. `generation_evidence_ledger`: one entry for each material `ContentUnit`.
3. `open_questions`: unique queries indexed by stable ID.
4. `references`: unique source records.
5. `consistency_findings`: cross-section checks and unresolved mismatches.

## Review and clean modes

- `review-draft`: show `TBD`, `AUTHOR QUERY`, and `CONFLICT` markers inline.
- `clean-draft`: remove resolved markers only. Do not silently remove unresolved blocking items; retain an inline marker or an explicit linked unresolved-item appendix.

## Traceability rules

- Every material paragraph must map to at least one fact, rule, confirmed decision, or explicit proposed assumption.
- Every proposed choice must state what would change it.
- Every external claim must map to a resolvable reference.
- Every query must point to affected content and every affected content item must point back to the query.
