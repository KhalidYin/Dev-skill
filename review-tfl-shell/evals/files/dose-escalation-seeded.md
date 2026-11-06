# Synthetic dose-escalation study — review package

All documents v1.0, 2026-10-01. Scoped package contains DLT decision summary and DLT event listing for escalation. Expansion efficacy outputs are outside this review. Text only, no rendered pages or data-collection specifications.

## SAP §7.1 — A1 dose decision
Single-arm dose-escalation component. DLT observation window: Day 1 through Day 28 inclusive. DLT-evaluable participants have either a DLT during that window or complete follow-up through Day 28 with at least 75% of planned doses. Display by assigned dose: number treated, number DLT-evaluable, participants with DLT n/N (%), and total DLT events. N for the DLT percentage is the DLT-evaluable count. Count each participant once in the subject summary regardless of event number; count separate DLT episodes in the event summary. The cohort committee uses these summaries with the prespecified escalation rule in §7.2; shells do not introduce a comparative hypothesis test.

## SAP §7.2 — decision output
Provide a dose-by-dose row with rule category and planned next action from the approved decision algorithm. §7.2 algorithm is supplied separately and is outside this excerpt; rule implementation cannot be verified from this excerpt.

## SAP §9 — A2 event listing
List all DLT episodes in Day 1–28, one row per event; participant ID, assigned dose, event ID, preferred term, onset date, study day, grade and resolution date. Order by dose, participant and onset. Study day derivation is defined in the full SAP appendix, not provided in this scoped exercise.

## Shell directory
T1 DLT decision summary; L1 DLT event listing. Complete for this scope.

## Global conventions G1
N/n refer to participants unless an event count is explicitly labeled. Percentages to one decimal. Zero is 0; percentages with zero denominator are NE; dash is not applicable. Missing date is shown as missing. G1 accompanies both displays. Numeric xx.x and program path TBD are intentional placeholders.

## T1 — DLT decision summary by assigned dose
Columns: assigned dose | treated | DLT-evaluable N | participants with DLT n (%) | total DLT events | rule category | planned next action.
Footnote a: DLT window is Day 1–21 inclusive; participants without DLT are evaluable after follow-up through Day 21 and at least 75% of planned doses. N is DLT-evaluable. Subject deduplication and event counting follow SAP §7.1. Rule category/action reference SAP §7.2. Display conventions follow G1.

## L1 — DLT episodes in Day 1–28
One row per DLT event; columns and sort as SAP §9. Caption: includes Day 1–28 events, with all date and study-day conventions as SAP §9 and its appendix. Multi-event participants may have multiple rows. Program TBD.
