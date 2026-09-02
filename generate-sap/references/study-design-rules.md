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
- for adaptive or dose-finding designs: cohort evaluability, escalation/de-escalation, stopping, MTD/RP2D, dose recommendation and intra-participant escalation rules.

## Rules

- `DES-001`: Transcribe design facts from the current approved source set; do not reconstruct missing design details from a registry or precedent.
- `DES-002`: Keep objectives, endpoint hierarchy and planned analyses aligned. A primary objective must map to a primary endpoint and analysis.
- `DES-003`: Define each endpoint with measure, derivation, baseline, assessment window, timepoint and direction where supplied.
- `DES-004`: Distinguish repeated measurements from a single primary-timepoint analysis; do not infer the estimator from repetition alone.
- `DES-005`: Treat sample size, randomization, stratification, multiplicity and interim decisions as study-specific. Never copy their numeric values from another trial.
- `DES-006`: Identify rescue medication, treatment discontinuation, prohibited treatment, death and missed assessment as potential ICE or missing-data topics without assigning a strategy unless supported.
- `DES-007`: For adaptive or dose-finding designs, enumerate source-specified cohort evaluability, escalation/de-escalation, stopping, MTD/RP2D, dose-recommendation and intra-participant escalation criteria. A general citation to the Protocol does not replace material operational decision rules.
- `DES-008`: Reconcile arm and sub-arm names, cohort counts, per-arm sample sizes and total sample size across the synopsis, design body, statistical sections and appendices. Preserve any mismatch as `conflict` with one stable query; do not choose one statement silently.

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
