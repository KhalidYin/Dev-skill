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

## Other endpoint families

For binary, time-to-event, count, ordinal, recurrent-event, cluster, adaptive, Bayesian, non-inferiority, or complex multiplicity designs, preserve the complete section and supported facts. Generate a method only when supplied rules and verified references are sufficient; otherwise use `proposed` or `tbd` and request specialist confirmation. Do not pretend first-version coverage.

## Alternatives and precedent

For a proposed method, state one credible alternative and why it differs. A comparable SAP can support consideration but cannot determine the current method or study-specific parameter values.
