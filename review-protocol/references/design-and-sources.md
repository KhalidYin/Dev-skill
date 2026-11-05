# Design and evidence routing

## Classify each statistically distinct part

Capture phase if stated, but use purpose, comparator, implementation and decision to route. A randomized arm assignment alone does not establish that the protocol plans formal between-arm inference. Likewise, a single-arm study may make a formal comparison with a prespecified benchmark. Where cohorts share rules, summarize together and retain cohort-specific parameters in the crosswalk.

For a multipart trial add one `scope: shared` unit for study-wide commitments and `scope: part` units for distinct statistical plans. For a homogeneous trial use one `scope: whole` unit. Record `purpose`, `comparison`, `structure`, `inference`, and an evidence `locator` for each unit. Classification can be partial. Use `uncertain_tags` only for design features that might apply and lack sufficient or consistent evidence. Explain the uncertainty, including conflicting locators when available. Unrelated tags stay inactive.

| Tag | Activate when the protocol provides evidence of |
|---|---|
| randomized | Random allocation, including randomized dose selection or clusters |
| blinded | Blinding of participants, investigators, assessors, or trial roles |
| single-arm | A treatment cohort analyzed without a concurrent trial comparison for that analysis |
| benchmark | A prespecified comparison to a fixed historical or clinical threshold |
| external-control | External participants or data used as an analysis comparator |
| nonrandomized-comparison | A planned comparison using nonrandomized concurrent or external groups |
| dose-escalation | Dose assignment informed by accumulating dose or toxicity data |
| dose-expansion | Dose expansion cohorts with separate objectives, sizing or decisions |
| multistage | Prespecified sequential enrollment or decisions, including Simon designs |
| multi-cohort | Distinct cohorts with relevant between-cohort rules |
| interim | A planned interim look or formal decision at a prespecified data review |
| adaptive | Planned design modifications informed by accumulating data |
| bayesian | Bayesian estimation or decisions |
| tte | A material time-to-event outcome, whether comparative or descriptive |
| event-driven | A look or completion based on an event count or information threshold |
| non-inferiority | A prespecified non-inferiority objective |
| multiplicity | Multiple analyses or claims for which the error-control strategy or claim hierarchy must be explained |
| estimand | A protocol states an estimand, or treatment-effect definition and handling of intercurrent events are material to the stated objective |
| specialist | Material statistical rules require a review beyond the supplied checklist, such as novel borrowing, complex platform changes or unfamiliar designs |

A historical benchmark is a fixed reference value. Activate `external-control` only when external data serve as a comparator. For example, a Simon design may activate `single-arm`, `benchmark` and `multistage` if those features are actually stated. The need for formal multiplicity adjustment depends on which analyses support which claims.

## Search and record sources

Use the classification first. Search official sources for the applicable jurisdiction, product class, indication, design, regulatory purpose and effective date when relevant. Check final/draft status and scope. Ask for jurisdiction only when needed for jurisdiction-specific review. An unknown jurisdiction still permits general statistical review. Use the packaged basis register for common topics, and verify current status and applicability when relying on a source for a finding. SPIRIT 2025 is a reporting reference for randomized trial protocols. Sponsor requirements supplied for the review are current-study documents and do not change a guideline's status.

For public precedents, prefer the actual protocol and amendments from a registry, sponsor, or publication supplement. Match purpose, comparison structure, endpoint and statistical decision. For benchmarks check indication, line, eligibility, ascertainment, follow-up and reference-data era. Record direct URL, document version/date, locator, matching traits and limiting differences. Public parameters are examples. A difference alone does not establish an issue. If only a registry summary is accessible, record it as such and limit what can be inferred. Search generically and omit confidential study IDs, compound and sponsor names, verbatim text, or other unpublished identifiers. If no comparable source is located, distinguish the limits of the search from a lack of comparable trials.

Initial public examples for checklist calibration:

- [NCT02811861](https://cdn.clinicaltrials.gov/large-docs/61/NCT02811861/Prot_000.pdf), synopsis and §9.7.4, for event-driven analysis, interim timing and multiplicity.
- [NCT03045406 Caravaggio](https://cdn.clinicaltrials.gov/large-docs/06/NCT03045406/Prot_000.pdf), Sample Size, for relationships among the non-inferiority margin, scale, sample size and loss to follow-up.
- [NCT03773133](https://cdn.clinicaltrials.gov/large-docs/33/NCT03773133/Prot_000.pdf), §11.3.1 and §11.3.3.4, for formal Simon two-stage inference.
- [NCT02737475](https://cdn.clinicaltrials.gov/large-docs/75/NCT02737475/Prot_000.pdf), §8.1.2 and Table 8.1.2-1, for Simon-guided exploratory expansion decisions.
- [NCT02529553](https://cdn.clinicaltrials.gov/large-docs/53/NCT02529553/Prot_000.pdf), §7.2.2 and Attachment 10, for DLT and model-guided dose escalation.
