# Comparable-study and SAP Research

Load this file after normalizing the current study and before drafting substantive statistical sections. Use only network/search tools actually available in the host.

## Tool gate

- If web search is available and the user has not prohibited external research, perform the search.
- If search is unavailable, access requires unapproved credentials, or a source cannot be opened, record `unavailable` or `limited`; do not claim that no precedent exists.
- Do not bypass login, licensing, robots, paywall, or access controls.
- Do not upload confidential study material to an external service unless the user has explicitly authorized that use.

## Study fingerprint

Build a fingerprint from supplied facts:

```yaml
indication: ""
phase: ""
objective_role: confirmatory | exploratory | unknown
design:
  allocation: ""
  masking: ""
  structure: ""
  control: ""
population: []
intervention_class: ""
primary_endpoint:
  scale: continuous | binary | time-to-event | count | ordinal | other | unknown
  definition: ""
  timepoint: ""
  repeated: null
estimand_topics: []
ice_topics: []
statistical_topics: []
regions: []
```

Do not infer missing fingerprint fields. Use multiple query families rather than one over-constrained query.

## Source tiers

Search in this order, while allowing useful sources from later tiers:

1. **Public full SAP or statistical-method appendix**
   - ClinicalTrials.gov study documents: <https://clinicaltrials.gov/policy/results-definitions>
   - Health Canada Public Release of Clinical Information, including CSR appendix 16.1.9: <https://www.canada.ca/en/health-canada/services/drug-health-product-review-approval/profile-public-release-clinical-information-guidance/document.html>
   - EMA Clinical Data Publication, including protocols and documentation of statistical methods: <https://www.ema.europa.eu/en/human-regulatory-overview/marketing-authorisation/clinical-data-publication>
2. **Study-specific substitutes when the SAP is unavailable**
   - Protocol statistical sections, CSR methods, journal supplements, open analysis-plan publications, and regulatory statistical reviews such as Drugs@FDA material.
3. **Normative and methodological context**
   - Current ICH, FDA, EMA, or other applicable official guidance and primary methodological sources.

Never label a Protocol, CSR, publication, or statistical review as the original SAP. Record its true document type.

## Search sequence

### 1. Discover

Run query families that combine:

- indication or closely related clinical setting;
- phase and design;
- endpoint name, scale and timepoint;
- intervention or control class when material;
- analysis topics such as estimand, MMRM, ANCOVA, missing data, reference-based imputation, multiplicity, or survival analysis;
- terms such as `statistical analysis plan`, `SAP`, `protocol`, or `statistical review`.

Aim initially for roughly 10-20 plausible records, but treat this as a discovery target rather than a quota.

### 2. Screen

Shortlist approximately 3-5 records using qualitative similarity:

1. endpoint and inferential question;
2. design and control structure;
3. population and disease setting;
4. ICE and missing-data problem;
5. phase and confirmatory role;
6. intervention class and region.

Assign `high`, `medium`, or `low` similarity and record why. Do not create a false-precision numeric score.

### 3. Deep read

When available, deeply read 2-3 high-similarity primary documents. Locate the actual passages for:

- endpoint and estimand;
- analysis population;
- primary estimator and complete model specification;
- ICE and missing-data handling;
- sensitivity and supplementary analyses;
- multiplicity, interim analysis, and sample-size assumptions when relevant.

Stop when additional credible records add no material design pattern, or when source availability limits are reached. Report the reason for stopping.

## Trial-precedent record

```yaml
reference_id: PRECEDENT-001
reference_type: trial_precedent
study:
  title: ""
  registry_id: ""
  sponsor: ""
  indication: ""
  phase: ""
document:
  title: ""
  document_type: sap | protocol | csr | regulatory-review | publication
  version: ""
  date: ""
  status: final | draft | historical | unknown
  source_repository: ""
  direct_url: ""
  retrieved_date: YYYY-MM-DD
location:
  section: ""
  page: null
similarity:
  level: high | medium | low
  matched: []
  differences: []
extracted_design:
  endpoint: ""
  estimand_or_ice: ""
  population: ""
  primary_method: ""
  missing_strategy: ""
  sensitivity: []
use_in_current_sap:
  role: candidate-design | drafting-pattern | background-only
  affected_sections: []
  limitation: precedent-not-normative
```

Use the direct document URL, not a search result. Record section and page when the source provides stable pagination. Summarize; do not reproduce substantial copyrighted text.

## Precedent summary

Produce a comparison matrix with study, similarity, endpoint, primary method, ICE strategy, missing-data assumption, sensitivity analysis, material differences, document type, and direct reference.

Then state:

- patterns shared by high-similarity sources;
- material disagreements and why they may differ;
- options plausibly relevant to the current study;
- practices not transferable because of design differences;
- current-study decisions that remain unresolved.

Never decide by majority vote. A method used in several trials remains conditional on the current estimand, data collection, design, and Sponsor decisions.

## Search outcome

Use one status:

```yaml
search_summary:
  status: completed | limited | unavailable | prohibited
  queries_run: []
  repositories_checked: []
  candidates_found: 0
  shortlisted: 0
  deeply_reviewed: 0
  stop_reason: ""
  limitations: []
```

`limited` includes cases with no accessible full SAP, no high-similarity record, incomplete version information, or only secondary descriptions. Do not equate `limited` with evidence of absence.
