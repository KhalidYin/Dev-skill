# Input Contract

Read this file for every invocation. Normalize supplied material into `SapGenerationContext` before drafting.

## Contract

```yaml
schema_version: "0.1"
request:
  mode: create | revise
  scope: full-sap | named-sections
  sections: []
  output_language: English | Chinese | bilingual
  maturity: review-draft | clean-draft
  target_template: generic | supplied-template

source_inventory:
  - source_id: SRC-001
    source_type: protocol | amendment | sponsor-decision | convention | guidance | sap | csr | publication
    title: ""
    version: ""
    date: ""
    status: approved | effective | final | draft | historical | unknown
    locator: "local path or direct URL"
    precedence: 1

study:
  identifiers: {}
  phase: null
  indication: null
  objectives: []
  design: {}
  treatments: []
  randomization: {}
  stratification: []
  masking: null
  periods: []
  visits: []
  endpoints: []
  intercurrent_events: []

confirmed_decisions:
  estimands: []
  analysis_populations: []
  statistical_methods: []
  missing_data: []
  sensitivity_analyses: []
  multiplicity: []
  interim_analyses: []

sponsor_conventions: []
constraints: []
unknowns: []
conflicts: []
```

## Normalization rules

1. Extract only statements present in supplied material or sources actually verified in the current task.
2. Assign every material fact a `fact_id`, `source_id`, and precise locator when available.
3. Preserve exact source status and version. Do not silently treat a draft or historical document as current.
4. Separate facts from confirmed decisions, working assumptions, constraints, unknowns, and conflicts.
5. Do not infer an unreported phase, endpoint timing, analysis population, estimand strategy, covariance structure, missingness assumption, alpha allocation, sample size, or regulatory position.
6. If the user supplies a template, preserve its section order and numbering. Otherwise use the generic baseline in `assets/sap-template.md` and label it generic.
7. Do not ingest direct identifiers or patient-level records. Ask for aggregate, synthetic, or de-identified study context.

## Readiness is local

Never assign one global ready/not-ready state to the whole SAP. Determine readiness for each section and content unit:

- `complete`: all material content is supported;
- `partial`: supported prose plus local open items;
- `tbd`: the section structure exists but material decisions are unresolved;
- `conflict`: authoritative inputs disagree;
- `not-applicable`: the section is retained and its non-applicability is stated.

Missing input blocks only affected content units. Continue with unaffected sections.

## Question discipline

- Ask no more than five decision-changing questions at once when interactive clarification is useful.
- Still produce the full review draft structure in the same response unless the user explicitly requests questions only.
- Place each question in its originating section and add it to the global open-question index.
- Reuse one stable ID when the same issue affects multiple sections.
