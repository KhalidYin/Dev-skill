# Estimand and Intercurrent-event Rules

Load this file for Sections 7.2, 7.3, 12.1, 12.3, and any analysis affected by post-ICE data.

## Required attributes

For every confirmatory estimand, seek:

1. population;
2. treatment condition or comparison;
3. variable or endpoint;
4. handling strategy for each material intercurrent event;
5. population-level summary measure.

## Rules

- `EST-001`: Map each estimand to one objective and endpoint. Do not create a generic study-wide estimand when endpoints target different questions.
- `EST-002`: Enumerate material ICE types from the current study conduct rules before assigning strategies.
- `EST-003`: Use only a supplied or explicitly proposed strategy: treatment policy, hypothetical, composite, while-on-treatment, or principal stratum.
- `EST-004`: Explain what data remain relevant after each ICE and whether those data are planned to be collected.
- `EST-005`: Keep ICE handling separate from missing-data handling. An ICE can occur with complete follow-up; missing data can occur without an ICE.
- `EST-006`: Do not describe censoring, imputation, or exclusion as an estimand strategy without stating the targeted clinical question.
- `EST-007`: When the estimand is incomplete, generate supported attributes, mark the remainder `proposed` or `tbd`, and create one stable query propagated to method and sensitivity sections.

## Evidence record

Record the source or proposal status of every attribute. For a proposed strategy, state:

- the clinical interpretation;
- required post-ICE data;
- at least one alternative;
- what study-team decision would change the proposal.

## Missing-state behavior

If ICE strategy is absent, do not silently assume treatment policy or hypothetical. Retain the estimand section, list known ICEs, add `Q-EST-*`, and mark dependent primary and sensitivity content conditional.
