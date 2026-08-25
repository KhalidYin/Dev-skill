# Analysis Population Rules

Load this file for Section 9 and whenever population choice affects an analysis.

## Required facts

- randomized/enrolled/treated definitions;
- treatment assignment rule;
- minimum post-baseline data requirements, if any;
- major protocol-deviation treatment;
- population-specific use by endpoint or analysis;
- safety exposure rule.

## Rules

- `POP-001`: Use the Sponsor's confirmed names and definitions; do not assume FAS, ITT, PP, or Safety Set are interchangeable.
- `POP-002`: State inclusion, exclusion, treatment assignment and analysis use for every set.
- `POP-003`: Align the primary analysis population with the estimand population and targeted treatment effect.
- `POP-004`: Do not exclude participants because of post-randomization events unless the confirmed estimand and design justify it.
- `POP-005`: Define protocol-deviation effects only when a deviation classification process is supplied; otherwise create a query.
- `POP-006`: Define the Safety Set using confirmed exposure criteria and actual/planned treatment assignment rules.

## Missing-state behavior

Retain all population subsections. Use `not-applicable` only with a sourced design reason. When definitions are absent, provide no generic final definition; add `Q-POP-*` with affected analyses and optionally present a clearly labeled candidate definition.
