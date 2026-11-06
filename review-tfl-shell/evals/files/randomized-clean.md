# Synthetic randomized study — review package

All documents v1.0, 2026-10-01. This text-only package is complete for the stated scope: primary Week 12 efficacy analysis, its sensitivity analysis, and subgroup figure. No collection specification or rendered pages supplied. Exclude safety and listings from this exercise.

## SAP §8.1 — A1 main analysis
Two-arm randomized superiority trial. Target: difference in mean Week 12 change from baseline for all randomized participants, including measurements after treatment discontinuation (treatment-policy strategy). Baseline is the last nonmissing measurement before first dose. ANCOVA includes randomized treatment and baseline value. Display adjusted means, A minus B adjusted mean difference and two-sided 95% CI. Missing Week 12 measurements are multiply imputed under MAR using treatment and baseline. All inference uses the imputation combining rules. Values and changes are in points.

## SAP §8.2 — A2 sensitivity
For the same target, perform a delta-adjusted multiple-imputation analysis with prespecified delta grid -5, 0, 5 points in Arm A. Display delta, adjusted difference and 95% CI. This output is required in this package.

## SAP §8.3 — A3 subgroup figure
Exploratory forest plot by age category (under 65 / 65 or older) with A minus B estimates and 95% CIs. Lower change is beneficial. Show treatment-by-age interaction p-value; no within-subgroup significance claims.

## Shell directory
T1: Week 12 change. T2: Delta sensitivity. F1: Week 12 change by age. This is the complete directory for this package.

## Global conventions G1
N is the randomized arm population; n is the number with observed Week 12 data. Report points and CI limits to one decimal. NE means not estimable, a dash means not applicable. Templates use xx.x for future values. Global conventions accompany all delivered displays. Program paths may remain placeholders.

## T1 — Week 12 change, randomized population
Columns: statistic | Arm A (N=xxx) | Arm B (N=xxx) | A minus B (95% CI).
Rows: observed n; adjusted Week 12 change and its SE; adjusted difference (contrast column only).
Footnote a: ANCOVA adjusted for baseline, including post-discontinuation measurements. Missing outcomes use MAR multiple imputation and combining rules. CI is two-sided 95%. Baseline and numeric conventions follow SAP §8.1 and G1.
Programming note: program TBD; use randomized group.

## F1 — Week 12 change by age, randomized population
Y-axis: age categories. X-axis: A minus B adjusted mean change (points); range -20 to 20, reference line 0. Dots and horizontal bars show estimates and two-sided 95% CI. Legend: ANCOVA and missing handling as SAP §8.1, with age main effect and treatment-by-age interaction; exploratory interaction p-value shown. Left arrow: favors A; right arrow: favors B. NE follows G1.

## T2 — Delta sensitivity, randomized population
Columns: delta in Arm A (points) | adjusted A minus B difference (points) | two-sided 95% CI. Rows: -5, 0, 5. Footnote: SAP §8.2 delta-adjusted multiple imputation for the same estimand, ANCOVA and combining rules as §8.1, including post-discontinuation measurements. Numeric conventions follow G1.
