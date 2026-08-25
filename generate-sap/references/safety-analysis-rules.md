# Safety Analysis Rules

Load this file for Section 13. This first version supplies baseline authoring constraints, not a complete therapeutic-area safety standard.

## General rules

- `SAF-001`: Use the confirmed Safety Set and treatment assignment rule.
- `SAF-002`: Define the treatment-emergent period, reference period and follow-up window from current study sources; do not copy another trial's windows.
- `SAF-003`: State coding dictionaries and versions only when supplied.
- `SAF-004`: Define denominators, participant-level counting and event-level counting for adverse-event summaries.
- `SAF-005`: Preserve separate handling for deaths, serious adverse events, discontinuations due to adverse events, events of special interest, laboratory tests, vital signs and ECGs as applicable.
- `SAF-006`: Do not invent toxicity grades, abnormality thresholds, baseline definitions or clinically significant criteria.
- `SAF-007`: Safety analyses are generally descriptive unless a confirmed inferential plan exists.

## Missing-state behavior

Keep the full safety structure. Generate supported conventions, use `not-applicable` only with a sourced reason, and add `Q-SAF-*` for missing exposure windows, coding versions, AESI definitions, laboratory grading or other study-specific rules.
