# Checklist Basis

No sponsor SOP was supplied when checklist v0.1.0 was drafted. Its items are therefore derived from published, broadly adopted guidance current at drafting (2026-11-03). Item text in `assets/review-checklist.yaml` paraphrases review checks; it does not quote the sources. A checklist item is a review baseline, not an agency requirement.

## Basis register

| ID | Source | Version / date | Role in checklist | Direct URL | Verification |
|----|--------|----------------|-------------------|------------|--------------|
| B-GAMBLE2017 | Gamble C, et al. Guidelines for the Content of Statistical Analysis Plans in Clinical Trials. JAMA 2017;318(23):2337-2343. doi:10.1001/jama.2017.18556 | Published 2017-12-19 | Backbone of STR items; minimum SAP content for later-phase RCTs (55 items in 32 numbered groups across 6 sections) | https://eprints.whiterose.ac.uk/id/eprint/125763/1/2017-JAMA-SAP.pdf | Item list checked 2026-11-03 |
| B-HOMER2022 | Homer V, et al. Early phase clinical trials extension to guidelines for the content of statistical analysis plans. BMJ 2022;376:e068177 | Published 2022-02-07 | STR-EP items: 11 new and 25 modified items for early-phase trials | https://www.bmj.com/content/376/bmj-2021-068177 | Totals and themes checked 2026-11-03; item numbers **not yet mapped**. Confirm against Table 1 before raising STR-EP to stable |
| B-ICHE9 | ICH E9 Statistical Principles for Clinical Trials | Step 4, 1998 | Pre-specification, documenting changes, multiplicity | https://www.ema.europa.eu/en/ich-e9-statistical-principles-clinical-trials-scientific-guideline | Current-version page checked 2026-11-03 |
| B-ICHE9R1 | ICH E9(R1) Addendum on Estimands and Sensitivity Analysis | Step 4, 2019 | Estimand attributes, intercurrent-event strategies, alignment of sensitivity analyses, documentation | Same EMA page as B-ICHE9 | Checked 2026-11-03 |
| B-SPIRIT2025 | Chan A-W, et al. SPIRIT 2025 statement: updated guideline for protocols of randomised trials. BMJ 2025;389:e081477 | 2025, 34-item checklist | Protocol-side items the SAP must agree with (PRO) | https://discovery.ucl.ac.uk/10207932/1/SPIRIT%202025%20BMJ.pdf | Checked 2026-11-03 |
| B-ICHM11 | ICH M11 Clinical Electronic Structured Harmonised Protocol (CeSHarP): guideline, template, technical specification | Step 4, adopted 2025-11-19 | Where to find statistical content in M11-structured Protocols | https://database.ich.org/sites/default/files/ICH_Step4_M11_Final_Template_2025_1119.pdf | Adoption date checked 2026-11-03 |
| B-NMPA2016 | 药物临床试验的生物统计学指导原则（原国家食品药品监督管理总局通告2016年第93号） | 2016-06-01 | Chinese regulatory context for SAP content, blind review, and changes | Not yet resolved to an official NMPA/CDE URL | **To verify**. Seen only through a secondary listing. Do not cite in findings until an official URL is recorded |
| B-ADAM | CDISC Analysis Data Model (ADaM) and ADaMIG: traceability and analysis-ready principles | Current CDISC release | PRG items on derivations and flags | https://www.cdisc.org/standards/foundational/adam | **To verify** version at use |
| B-FDA-TCG | FDA Study Data Technical Conformance Guide: traceability expectations | Current FDA release | PRG-14 data provenance | FDA study data standards resources page | **To verify** version at use |
| B-PRACTICE | Reviewer practice: reconciliation and reproducibility checks without a single normative source | n/a | INT and PRG items | n/a | Not normative. Findings that rest only on B-PRACTICE must show the internal contradiction or the ambiguity itself |

## How to use the basis in findings

- Cite the checklist item ID in every finding. Cite the basis ID only when the user asks for it or when the finding rests on the guideline itself (for example, missing estimand attributes).
- A basis marked **To verify** cannot be the only support for a Critical or Major finding.
- Do not describe any item as a regulatory requirement for NMPA, FDA, or EMA unless an official current source for that agency has been verified and recorded here.

## Revising the checklist

When a sponsor SOP or an updated guideline becomes available:

1. Add the source to the register with its URL, version, and verification date.
2. Add or edit items. Never reuse a retired item ID.
3. Bump `checklist_version` (minor for new items, major for changed semantics) and update `checklist_date`.
4. Re-run the evals in `evals/` before changing the skill's status.
