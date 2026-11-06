# Synthetic single-arm study — review package

All documents v1.0, 2026-10-01. Complete scoped package: ORR, response plot and treatment-exposure listing. Other analyses are outside scope. Text only; no rendered pages.

## SAP §8.1 — A1 ORR
Single-arm oncology study. ORR estimates the proportion with confirmed response in all treated participants; missing or unevaluable response counts as nonresponse. Display responders n, treated denominator N, n/N percent and two-sided 95% Clopper-Pearson CI. Assessment data come from independent imaging review under the external imaging specification.

## SAP §8.2 — A2 response plot
Descriptive waterfall plot of best percent change in target-lesion sum among treated participants with baseline and postbaseline evaluable measurements. Its population differs legitimately from A1. Bars ordered by percent change; horizontal reference at -30%. Include excluded count and reasons. No formal comparison.

## SAP §9 — A3 exposure listing
One row per treated participant. Columns: participant ID, treatment start date, treatment end date, duration in days. For completed treatment with complete dates, duration = end - start + 1; ongoing treatment uses cutoff - start + 1 with ongoing flag. No partial dates allowed. Sort by participant ID. Cutoff is 2026-09-30.

## CRF Exposure page
Participant ID; treatment start (YYYY-MM-DD); treatment end (YYYY-MM-DD); ongoing yes/no. Exact dates mandatory except end date for ongoing treatment. This page does not collect a separate duration field or imaging assessments.

## External imaging specification §2
Participant ID, assessment date (day precision), independent review confirmation status, response category, target-lesion sum in mm and evaluability reason. Baseline and postbaseline records identified by assessment date and schedule in SAP appendix. This supports the planned response analysis and plot.

## Global conventions G1
N is all treated participants unless a local display explicitly defines a descriptive subset. Percentages to one decimal; CI limits to one decimal. NE = not estimable; dash = not applicable. G1 accompanies all delivered displays; numeric placeholders are xx.x.

## Shell directory
T1 ORR; F1 waterfall; L1 exposure. Complete for this scope.

## T1 — Confirmed ORR, all-treated population
Rows: responders n; N; percent; two-sided 95% CI. Footnote a: Percentages and exact Clopper-Pearson CI use the response-evaluable participants as denominator; unevaluable participants are excluded. N follows this footnote. Confirmation and missing rules otherwise follow SAP §8.1.

## F1 — Best percent change from baseline
Y-axis: best change (%); X-axis: participant index ordered by change. One bar per evaluable participant. Reference line -30%. Legend: treated with baseline and evaluable postbaseline measurements, excluded n and reasons shown below plot; negative change denotes decrease. Rules and rounding follow SAP §8.2 and G1.

## L1 — Exposure, all treated
Columns and row grain as SAP §9. Notes: duration follows the complete-date derivation and ongoing cutoff rule in SAP §9; ongoing shown by an asterisk, dates YYYY-MM-DD. Sorted by participant ID. Program: TBD.
