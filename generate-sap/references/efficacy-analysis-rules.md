# Efficacy Analysis Rules

Load this file for Section 12 and detailed model appendices.

## Selection sequence

1. Confirm the objective, endpoint and estimand.
2. Classify endpoint scale and observation structure.
3. Confirm analysis population and treatment contrast.
4. Identify candidate estimators and assumptions.
5. Specify the selected or proposed method completely.
6. Link missing-data and sensitivity strategies.

Do not begin with a preferred model name.

## Primary-method specification

For any primary analysis, seek and record:

- response and analysis timepoint;
- treatment effect or contrast;
- model/test family;
- fixed effects, covariates and stratification factors;
- repeated or clustering structure;
- transformation or link function;
- estimation and degrees-of-freedom method;
- covariance/correlation structure and selection rule;
- estimate, confidence interval, significance level and hypothesis;
- convergence or model-failure handling;
- analysis population and data included after ICEs.

## Continuous repeated endpoint

- `EFF-CR-001`: Consider longitudinal models when repeated post-baseline observations are relevant to the estimand; repetition alone does not mandate MMRM.
- `EFF-CR-002`: Compare a longitudinal model with a primary-timepoint ANCOVA or another justified estimator when both can target the estimand.
- `EFF-CR-003`: For MMRM, define response, treatment, visit, treatment-by-visit, baseline terms, stratification factors, subject/repeated structure, covariance handling, estimation, degrees of freedom and target contrast.
- `EFF-CR-004`: Never invent covariance structure, fallback order, Kenward-Roger/Satterthwaite choice, or baseline-by-visit interaction. Mark unspecified items locally.
- `EFF-CR-005`: State whether post-discontinuation/rescue observations are included, because this must follow the estimand rather than model convention.

## Adaptive and Bayesian methods

When a current study source specifies an adaptive, Bayesian, dose-exposure or dose-toxicity method, seek and record every applicable item:

- likelihood, model equation, parameterization and reference dose;
- complete prior distributions, mixture components, weights, correlations and hyperparameters;
- posterior intervals, decision thresholds, admissibility criteria and reported posterior quantities;
- borrowing, down-weighting, schedule-transition and model-update rules;
- cohort evaluability, escalation/de-escalation, stopping and MTD/RP2D or dose-recommendation criteria;
- operating-characteristic assumptions and any source-specified fallback or model-failure handling.

- `EFF-AB-001`: Transcribe source-specified numeric priors, thresholds and decision criteria from both the main text and appendices. Do not replace an available specification with `TBD` or a bare cross-reference.
- `EFF-AB-002`: If any applicable item is absent, retain the supported components, mark only the missing component `tbd` or `proposed`, and create a local query. Do not import the missing value from a precedent.
- `EFF-AB-003`: Keep protocol-defined decision criteria distinct from later implementation settings such as code, simulation seeds, convergence diagnostics or Sponsor-selected borrowing weights.

## Other endpoint families

For binary, time-to-event, count, ordinal, recurrent-event, cluster, adaptive, Bayesian, non-inferiority, or complex multiplicity designs, preserve the complete section and supported facts. Generate a method only when supplied rules and verified references are sufficient; otherwise use `proposed` or `tbd` and request specialist confirmation. Do not pretend first-version coverage.

## Alternatives and precedent

For a proposed method, state one credible alternative and why it differs. A comparable SAP can support consideration but cannot determine the current method or study-specific parameter values.
