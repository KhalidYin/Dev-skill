# SYNTHETIC TEST DOCUMENT - NOT A REAL STUDY (seeded-defect variant)
# Statistical Analysis Plan, Study XR-301

SAP version 1.0, 2026-06-01. Based on Protocol version 2.0 (Amendment 1), 2026-03-15.
Prepared by: Study Statistician. Reviewed by: Lead Statistician. Approved by: Clinical Lead. (Signature block on page 2.)

## 1 Revision History

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-06-01 | Initial version, finalized before any unblinded data access. |

## 2 Synopsis

Randomized 1:1, double-blind, placebo-controlled study of XR-17 200 mg once daily versus placebo for 24 weeks. Approximately 420 participants (210 per arm) will be randomized, stratified by region and baseline WIS category.

## 3 Objectives and Endpoints

- Primary: change from baseline in Weekly Itch Score (WIS) at Week 26.
- Key secondary 1: WIS responder (improvement of at least 4 points) at Week 24.
- Key secondary 2: time to first rescue medication use through Week 24.
- Secondary: change from baseline in DLQI at Week 24.

## 4 Estimands

Primary estimand: population as defined by the Protocol eligibility criteria; treatment XR-17 200 mg versus placebo with background emollients; variable change from baseline in WIS at Week 24; treatment discontinuation handled by treatment policy; rescue medication use handled by a hypothetical strategy; summary measure difference in mean change.

## 5 Analysis Sets

- FAS: all randomized participants, analyzed as randomized.
- PPS: FAS participants without major protocol deviations affecting the primary endpoint and with at least 70% study-drug compliance through Week 24. Major deviations are classified before unblinding, using the deviation categories in Appendix B.
- SS: all participants who received at least one dose, analyzed according to the treatment actually received. A participant who received the wrong treatment for the whole period is analyzed under that treatment.

## 6 General Conventions

### 6.1 Baseline and study day

Baseline WIS is the mean of the daily scores over the 7 days before the first dose, requiring at least 4 non-missing days; otherwise baseline is missing. For other variables, baseline is the value recorded at the Day 1 visit. Study Day 1 is the day of first dose; there is no Day 0.

### 6.2 Analysis visit windows

Weekly WIS is the mean of available daily scores in each study week, requiring at least 4 non-missing days. Clinic-based assessments use windows: Week 12 = Days 71-98; Week 16 = Days 92-126; Week 24 = Days 155-182. If more than one value falls in a window, the value closest to the target day is used; if two values are equally close, the later one is used. Unscheduled and early-termination values are mapped to windows by the same rule.

### 6.3 Presentation

Continuous variables: n, mean, SD, median, Q1, Q3, min, max. Means and medians are shown to one more decimal place than the raw data. Percentages use the number of participants in the analysis set as the denominator, shown to one decimal.

### 6.4 Dates

Partial dates will be handled according to standard programming conventions.

## 7 Efficacy Analyses

### 7.1 Primary analysis

The primary estimand is estimated in the FAS using MMRM with treatment, visit, treatment-by-visit interaction, region, and baseline WIS category as fixed effects and baseline WIS as a covariate. An unstructured covariance matrix is used, with Kenward-Roger degrees of freedom. If the model does not converge, Toeplitz and then compound symmetry structures are tried in that order. WIS values after rescue medication are set to missing (hypothetical strategy). Values after treatment discontinuation are included (treatment policy). The treatment difference at Week 24 is presented with a two-sided 95% CI and p-value.

### 7.2 Sensitivity analyses

Sensitivity analysis 1 (same estimand): reference-based multiple imputation (jump to reference) for missing data after treatment discontinuation, with 100 imputations, seed 20260601, and Rubin's rules. Sensitivity analysis 2 (same estimand): tipping-point analysis that varies a delta shift in the XR-17 arm.

### 7.3 Key secondary analyses

Key secondary 1 (responder) is analyzed with a CMH test stratified by region and baseline WIS category. Participants with missing Week 24 WIS or prior rescue use are non-responders.

Key secondary 2 (time to first rescue medication) is analyzed with a stratified log-rank test and a Cox model for the hazard ratio. Time origin is randomization. The event is the first recorded rescue medication use.

### 7.4 Multiplicity

Fixed-sequence testing at a two-sided 0.05 level: primary endpoint, then PGI-S responder at Week 24, then key secondary 2. Testing stops at the first non-significant result.

### 7.5 Other secondary analysis

Change from baseline in DLQI at Week 24 is analyzed in the FAS with ANCOVA, with treatment, region, and baseline WIS category as factors and baseline DLQI as a covariate. Missing Week 24 values are not imputed.

## 8 Sample Size and Interim Analysis

### 8.1 Sample size

Assuming a difference of 1.0 point, an SD of 2.8, a two-sided alpha of 0.05, and 90% power, 166 evaluable participants per arm are needed; with 20% dropout, 400 participants (200 per arm) will be randomized.

### 8.2 Interim analysis

Two interim analyses at 33% and 67% information. Efficacy boundaries use a Lan-DeMets O'Brien-Fleming alpha-spending function, and the study may stop early for efficacy. The DMC reviews the results; see Section 11.4 for testing at the final analysis.

## 9 Safety Analyses

TEAEs (onset on or after the first dose and up to 28 days after the last dose) are summarized by MedDRA SOC and PT (MedDRA version current at database lock), by maximum severity, and by relationship. Laboratory baseline is the last non-missing value before the first dose. Laboratory values are summarized by visit, with shift tables based on normal ranges.

## 10 Changes from the Protocol

Sensitivity analysis 2 (tipping point) is added; it is not described in the Protocol. It is added to assess the robustness of the primary result to departures from the missing-at-random assumption. There are no other changes.

## 11 Software

SAS version 9.4 or later.

## Appendix B Protocol Deviation Categories

Major deviations affecting the primary endpoint: wrong treatment received, prohibited systemic antipruritic medication, eDiary non-completion of more than 50% of days in Weeks 21-24.
