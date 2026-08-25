# Generic SAP Section Map

Use a supplied Sponsor template when available. Otherwise instantiate this generic baseline and label it as such. Preserve every top-level section; use `not-applicable` or local queries instead of silently deleting sections.

| ID | Section | Minimum content or missing-state behavior |
|----|---------|-------------------------------------------|
| SEC-01 | Title Page and Approvals | Study identifier, title, SAP version/date, authoring status; unresolved metadata becomes local TBD |
| SEC-02 | Revision History | Version, date, change summary and rationale; state initial version when applicable |
| SEC-03 | Table of Contents | Reflect the complete instantiated structure |
| SEC-04 | Abbreviations and Definitions | Include used terms only; unresolved Sponsor terminology becomes a query |
| SEC-05 | Introduction and Purpose | Protocol relationship, SAP purpose, governing versions and analysis timing |
| SEC-06 | Study Objectives, Design and Treatments | Objectives, design, arms, randomization, masking, periods, visits and rescue/concomitant treatment rules |
| SEC-07 | Endpoints, Estimands and Intercurrent Events | Endpoint hierarchy and definitions; estimand attributes; ICE strategies and data relevance |
| SEC-08 | Sample Size, Randomization and Multiplicity | Transcribe confirmed assumptions and procedures; never invent numbers, alpha paths or randomization details |
| SEC-09 | Analysis Populations | Define each set, assignment rule, exclusions, protocol-deviation relationship and analysis use |
| SEC-10 | General Statistical Conventions | Analysis timing, baseline, study day, visits, summaries, confidence intervals, software if confirmed, and missing conventions |
| SEC-11 | Participant Disposition, Exposure and Compliance | Planned summaries, denominators, treatment exposure and compliance definitions |
| SEC-12 | Efficacy Analyses | Primary, key secondary, other secondary, sensitivity, supplementary and subgroup analyses |
| SEC-13 | Safety Analyses | Exposure, adverse events, deaths, labs, vital signs, ECG and other safety topics as applicable |
| SEC-14 | Other Analyses | PK, PD, immunogenicity, biomarkers, health economics or PRO analyses; mark each non-applicable when unsupported by design |
| SEC-15 | Interim Analyses and Data Monitoring | Confirmed timing, purpose, access, decision rules and alpha implications; otherwise retain a query or state none planned if sourced |
| SEC-16 | Changes from Protocol-Planned Analyses | Identify and justify confirmed changes; do not manufacture differences |
| SEC-17 | References | List only sources actually cited or used |
| SEC-18 | Appendices | Detailed derivations, model specifications, query index, or other supplied-template appendices |

## Section generation order

Draft in dependency order rather than final display order:

1. governing sources and design facts;
2. objectives and endpoints;
3. estimands and ICE strategies;
4. analysis populations;
5. primary estimator and missing-data strategy;
6. sensitivity and multiplicity;
7. supporting efficacy, safety, and general conventions;
8. administrative sections, references, and appendices.

Then render in the target template order.

## Section status

Assign every section one of `complete`, `partial`, `tbd`, `conflict`, or `not-applicable`. A section may be `partial` even when individual content units have different generation modes.
