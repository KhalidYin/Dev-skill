# Review rules

## Chapter completeness

Use the `CH-*` checks before inspecting individual analyses. Map each applicable statistical topic to substantive content across the current protocol and available controlled appendices, including content outside the statistics chapter. An empty heading or generic cross-reference alone does not establish coverage. Apply a supplied mandatory sponsor template's heading rules separately from substantive coverage. Record where you checked. An unavailable cited attachment produces `not-assessable` for what depends on it. If the protocol itself leaves an essential decision open and has no identifiable governing source, record a supported omission. Continue the checks supported by the material available.

## Per-analysis review

For each analysis, first establish its target from the protocol. For treatment effects record treatment, population, variable, intercurrent-event strategies and population-level summary in the existing matrix. For a dose or progression decision record its target, inputs and decision criteria. Identify missing or conflicting attributes explicitly, and continue the relationships that can be assessed. Register analyses by part, endpoint or objective and role, including a primary safety objective as primary. Evaluate the following against that target:

1. **Ambiguity.** Quote the wording, state two text-supported readings, and identify a concrete change to the analysis or decision. Check denominators, time origins, visit windows, censoring and exact threshold operators. Ask the author to resolve the choice and reconcile affected locations. Purely editorial wording may be classified Editorial.
2. **Prespecification.** Complete the analysis matrix for each analysis. Check the objective/endpoint, analysis population, estimator or method, material assumptions, estimand/intercurrent events where relevant, missingness, sensitivity and inference/decision. Apply only relevant design slots. Use `sap-detail` only when the material protocol commitment is located and the deferred detail is stated in the note. Identify how any controlled external document governs a key rule. Do not classify an unspecified design decision as SAP detail.
3. **Method fit.** In the existing slot, conclude whether design and collection support estimation of the stated target, whether the estimator and assumptions align with it, and whether sizing and decision rules use that analysis. Check that sensitivity analyses address robustness for the same estimand. For practical adjustments, explain which assumption changes and whether the target changes. Rank a substantiated mismatch with evidence. For a choice requiring clinical justification or simulation, give the exact decision and evidence needed.

## Evidence and coverage

Use precise section, page, table, appendix or stable paragraph locators. For conflicting values give both locations and the actual values. For omissions identify the reviewed sections and explain the protocol commitment that makes the missing item material. For findings on cross-file differences cite both documents. Use short excerpts or a faithful paraphrase, labeled if ambiguity matters.

Each active item gets one coverage result per applicable unit:

- `pass` with evidence from the supplied documents.
- `finding` with one or more linked issues. A defect has one finding per unit even when several items detect it.
- `sap-detail` with the locator for the locked protocol commitment and a note naming the implementation detail left to SAP.
- `not-assessable` with the missing document, unreadable passage or classification uncertainty. If the entire supplied material is an excerpt, distinguish material known absent from material outside the excerpt.
- `not-applicable` with a reason for an active check whose specific premise is absent (e.g. a defined protocol with no revision to disclose). The builder labels inactive tagged checks automatically.

If a protocol commits to a decision that affects conduct, participant protection, or interpretation, look for the associated rules in the protocol and referenced supplied material. A planned SAP can elaborate mechanics such as derivation details. A blanket SAP reference cannot resolve a contradiction already present in the protocol or establish an unstated key design commitment. Where a separately supplied SAP is needed to assess alignment, use `not-assessable` if it is missing. Score disclosure and agreement separately.

## Ranking and specialist questions

- **Critical** when strong evidence shows the primary objective or an essential safety decision cannot be carried out or interpreted as stated. Require a second source location or a second location in the protocol identifying the affected commitment. Low-confidence evidence never supports this ranking.
- **Major** for a substantiated discrepancy, omission or ambiguity likely to materially affect an important result, a key study decision or its interpretation.
- **Minor** for a localized clarification with limited consequence. **Editorial** is for wording or referencing defects.
- **Statistician review** for a specific unresolved method choice, clinical assumption or simulation-dependent decision. State what must be decided and what evidence will resolve it. Leave severity blank. Rank an established method mismatch by its impact.

Guidance establishes the applicable benchmark for judging an item. Precedent illustrates a possible approach. A contradiction, arithmetic error or missing conduct-critical rule may be actionable from protocol evidence alone. For a Critical or Major finding grounded in an external requirement, use a verified, applicable source and give its precise location. Describe what needs reconciliation or confirmation, and why it matters for the design or interpretation.

Lead each `comment` with the finding and the specific change or decision required. In `rationale`, explain the effect on the estimand, analysis or trial decision and justify priority. Cite the exact source. If evidence is missing, name the missing item and the judgment it prevents. Avoid vague requests such as “further consideration is recommended” and repeated general disclaimers. Link the same defect from chapter coverage and the analysis matrix to one finding.
