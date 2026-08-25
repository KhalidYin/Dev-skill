# Study Design, Objectives and Endpoints Rules

Load this file for Sections 5, 6, 7.1, 8, 10, or 15.

## Required facts

- governing Protocol and amendment versions;
- phase, objective and confirmatory/exploratory role;
- allocation, control, masking and design structure;
- treatment arms, periods, randomization ratio and stratification;
- visit schedule, treatment duration and follow-up;
- rescue/concomitant treatment and discontinuation rules;
- endpoint hierarchy, variable, assessment, derivation and timepoint.

## Rules

- `DES-001`: Transcribe design facts from the current approved source set; do not reconstruct missing design details from a registry or precedent.
- `DES-002`: Keep objectives, endpoint hierarchy and planned analyses aligned. A primary objective must map to a primary endpoint and analysis.
- `DES-003`: Define each endpoint with measure, derivation, baseline, assessment window, timepoint and direction where supplied.
- `DES-004`: Distinguish repeated measurements from a single primary-timepoint analysis; do not infer the estimator from repetition alone.
- `DES-005`: Treat sample size, randomization, stratification, multiplicity and interim decisions as study-specific. Never copy their numeric values from another trial.
- `DES-006`: Identify rescue medication, treatment discontinuation, prohibited treatment, death and missed assessment as potential ICE or missing-data topics without assigning a strategy unless supported.

## Output pattern

Draft concise factual prose first, then add local markers:

```text
[Supported design prose.]

[AUTHOR QUERY Q-DES-001]
Confirm [missing study-specific decision]. This affects [sections/topics].
```

## Missing-state behavior

- Missing administrative metadata: retain title fields as `TBD`; continue statistical sections.
- Missing endpoint derivation or timepoint: mark the affected endpoint and analysis `tbd`; do not choose a method.
- Missing randomization or sample-size detail: retain Sections 8.1/8.2 and add local queries.
- Conflicting Protocol versions: cite both statements and create one `CONFLICT` query reused in affected sections.
