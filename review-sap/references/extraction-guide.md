# Extraction Guide

Extract before judging. Extraction produces the Protocol-SAP crosswalk. The crosswalk is evidence for INT and PRO findings and becomes its own sheet in the workbook.

## Key parameters

Extract each parameter that exists in either document. Record it once per parameter (and per endpoint or arm where relevant).

| Group | Parameters |
|-------|-----------|
| Identity | Protocol version and date cited by SAP; Protocol version supplied; amendments |
| Design | Phase; design type; arms and doses; allocation ratio; stratification factors; blinding; periods; cohorts |
| Objectives | Each objective, with its role (primary, key secondary, secondary, exploratory) |
| Endpoints | Each endpoint: role, variable definition, timepoint, summary measure |
| Estimands | Treatment, population, variable, each intercurrent event with its strategy, population-level summary |
| Populations | Each population's name and inclusion rule |
| Sample size | N total and per arm; effect size; variability or event rate; alpha; sidedness; power; dropout; events required |
| Testing | Hypothesis type; margin; significance level; multiplicity procedure; testing order; alpha split |
| Interim | Number; timing (information fraction or events); purpose; boundaries or spending function; DMC |
| Analysis | Primary model; covariates; effect measure; missing-data approach |
| Visits | Primary timepoint; analysis visits; windows |
| Safety | AE collection period; treatment-emergent definition; AESI; DLT window; grading system |
| Early phase | Escalation design; cohort size; decision thresholds; MTD/RP2D rule; stopping rules |

## Crosswalk record rules

- `sap_value` and `protocol_value` are short normalized statements (for example, "N=420 (210/arm), 1:1"), not long quotations.
- Each value carries a locator: section number, table, or page.
- Within one document, record every place the value appears when it is stated more than once (synopsis, body, appendix). A difference inside one document is evidence for INT-03 or INT-04.
- `match` is one of `match`, `mismatch`, `sap-only`, `protocol-only`, `declared-change`, or `unclear`. Use `declared-change` when the SAP discloses the difference in its changes-from-Protocol section. Include the disclosure locator in `note` and link any finding about a substantive change through `finding_ids`.
- A `mismatch` or `unclear` row should normally be linked to a finding through `finding_ids`. If you decide it is not a defect, say why in `note`.

## Reading tips

- Synopses, sample size sections, and appendices are where numeric inconsistencies hide. Read all three.
- In M11-structured Protocols, statistical content is concentrated in the statistical considerations section and estimand subsections. Older Protocols often split it between the synopsis and the statistics section.
- Tables of planned analyses and TFL lists often contradict the prose. Compare them row by row.
- Record what the document says, not what it probably means. Ambiguity is itself a finding (`ambiguity`).
