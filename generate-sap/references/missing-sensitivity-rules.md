# Missing Data and Sensitivity Rules

Load this file for Sections 10.3, 12.1, and 12.3.

## Rules

- `MIS-001`: Describe which target data can be missing, at what time, and in relation to ICEs.
- `MIS-002`: State the assumption attached to the primary estimator, such as MAR, only when confirmed or clearly labeled proposed.
- `MIS-003`: Do not use LOCF, complete-case analysis, multiple imputation, reference-based imputation, delta adjustment, or tipping point merely because a precedent used it.
- `MIS-004`: Specify an imputation procedure only when its population, variables, visit structure, treatment grouping, number of imputations, analysis model, combination rule and failure handling are supported or explicitly marked TBD.
- `SEN-001`: Each sensitivity analysis must vary a named assumption relevant to the primary estimand or estimator.
- `SEN-002`: Distinguish sensitivity analyses from supplementary analyses targeting a different estimand or analysis set.
- `SEN-003`: State the interpretation of materially different results; do not define post-hoc success criteria unless confirmed.
- `SEN-004`: Ensure data collection can support the proposed sensitivity analysis.

## Alignment sequence

```text
ICE strategy
  -> relevant post-ICE outcome data
  -> unobserved data problem
  -> primary assumption and estimator
  -> sensitivity analysis varying that assumption
```

## Missing-state behavior

- If ICE strategy is unresolved, reference the originating `Q-EST-*` rather than inventing a separate missing-data assumption.
- If missing-data assumptions are absent, draft the observed-data structure and insert `Q-MIS-*` in both primary and sensitivity sections.
- If a sensitivity parameter is not study-confirmed, leave the value TBD and document how it would be selected.
