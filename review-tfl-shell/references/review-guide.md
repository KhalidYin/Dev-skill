# Review guide

## Inputs and precedence

Use the current SAP and its applicable amendments as the direct analysis specification. Use the Protocol to resolve the research objective, estimand and trial decision. Cite both sides of any unresolved upstream disagreement; identify the decision to reconcile. Global TFL conventions govern defaults when their scope is explicit. Local exceptions need a clear scope and consistent analysis rationale. Supplied sponsor templates govern their own formatting requirements.

Optional documents include blank or annotated CRF, completion instructions, data dictionaries, vendor transfer specifications, ADaM specifications, and prior shells. Record each document's role, version, date and path. Match the collection and analysis versions. CRF absence affects only collection checks. For central labs, imaging, ePRO and randomization data, inspect their external specifications before claiming a field is absent. A derived value can be supported by its inputs and a defined derivation. Annotated CRFs establish mappings, not actual data availability or numeric correctness.

For public guidance searches use generic design, analysis and document names without confidential identifiers or verbatim study text. Verify scope and current version for any external claim. ICH E3 provides report-content context. CDISC ARS describes traceable analysis/output relationships, and eTFL provides examples. Cite the precise applicable provision when it supports a finding. Do not infer a study requirement from a different trial's format.

- ICH E3, sections 11, 12, 14 and 16, subject to the study and reporting context. https://database.ich.org/sites/default/files/E3_Guideline.pdf
- ICH E9(R1), final 2019, A.2, A.3, A.5 and A.6: align the target, estimator, sensitivity analysis and interpretation. https://database.ich.org/sites/default/files/E9-R1_Step4_Guideline_2019_1203.pdf
- CDISC ARS, Analysis, Output, DisplaySection and DocumentReference. https://cdisc-org.github.io/analysis-results-standard/
- CDISC eTFL illustrative safety packages. https://www.cdisc.org/kb/etfl
- CDISC CDASH collection definitions and instructions. https://www.cdisc.org/standards/foundational/cdashig-v2-1

## Read and inspect

Support DOCX, PDF, XLSX, RTF and readable text through tools available in the environment. Preserve shell IDs, page/section/table locators and linked notes. For Office/PDF inputs inspect rendered pages or the live document as well as text to check clipping, spanning headers and footnote placement. If rendering is unavailable, mark visual items not-assessable; perform semantic checks on readable content. For text fixtures visual checks are not-assessable.

Inspect the whole package, including usage notes and appendices. Scan the SAP inventory independently of the shell directory so an absent output can be detected. Check apparent duplicates for different analysis populations, endpoints or roles before reporting them. If only a subset of shells or SAP is supplied, state the subset and avoid claiming package-wide absence.

## Footnotes and explanations

Read the global convention and the local display together. Determine which rule applies to which rows, columns or panels. Check:
- Population, grouping, period and cutoff against title and body.
- N, n, percentages, row/column denominators and subject/event counts.
- Within-category deduplication, worst grade, multiple categories and sorting when relevant.
- Model, covariates, contrasts, confidence level, sidedness and adjustment applicable to the displayed statistics.
- Missing, unevaluable, zero denominator, not estimable and the meanings of blank/dash/zero.
- Baseline, change, treatment-emergent and endpoint-specific definitions.
- Superscripts and footnote anchors in both directions, defined abbreviations and correct cross-references.
- Copied notes referencing the wrong endpoint, analysis population, method or study part.
- Meaning-critical information in the delivered output or an explicit, accessible convention reference. Programming-only notes are insufficient when readers need the definition to interpret results.
- Continuation-page headers, notes and legends after rendering.

Judge a globally defined convention as adequate when it clearly applies and readers can locate it. Dataset/program names may be placeholders in a mock shell. Do not treat planned numeric placeholders as actual results. Ask for an explicit display convention if a placeholder's meaning is ambiguous.

## T, F and L

Keep estimand attributes visible through the SAP-to-shell mapping: treatment conditions, population, variable, intercurrent-event strategy and population-level summary. Check that display filters, event/censor rules, post-event observations and sensitivity labels preserve the intended target. Sensitivity analyses examine the same estimand; supplementary analyses can address different targets. For dose-finding and other decision studies trace their stated decision rule and supporting summaries. Do not impose a randomized comparison or efficacy estimand on an unrelated descriptive output.

Tables: hierarchy, totals/subcategories, categorical and continuous summaries, uncertainty, units, rounding, zero counts and nonestimable outputs. For AE summaries distinguish subjects from episodes, and assess deduplication at SOC/PT and category levels.

Figures: endpoint and scale, axis units and origin, grouping, legend, intervals and reference lines. For survival displays check censor marks and risk counts if needed for the planned interpretation or required by the specification. For forest plots verify effect direction, reference line and whether subgroup inference is interaction or within-subgroup estimation.

Listings: define one row's granularity, identifiers, visit/event linkage, relevant dates, measured/derived values, status and ordering. Identify filters and exclusions. A subject need not have one row when multiple visits or events are intended.

Cross-output review: compare identical populations, endpoints and periods. Differences caused by analysis role, cutoff, population or method can be justified; cite that reason. Disposition, exposure and event populations need not have equal counts by design.

## Conclusions and comments

Coverage states are pass, finding, not-applicable and not-assessable. Pass requires located supporting evidence. A finding requires a linked comment. For not-applicable give the specific premise that is absent; for not-assessable name the missing input and blocked judgment.

Each comment states the defect and the correction or exact decision required. Explain the consequence in the rationale and cite source positions. For substantive ambiguity give two plausible readings and their different consequences. A generic “please clarify” is insufficient.

- Critical: a supported defect changes the primary inference or an essential trial decision.
- Major: changes an important analysis definition or creates material implementation or interpretation ambiguity.
- Minor: localized clarification with limited consequence.
- Editorial: typographic, reference or layout defect without statistical consequence.
- Query: evidence is insufficient to resolve a specific decision; name the evidence needed.

For Critical, inconsistencies and substantive numerical/definition errors provide both affected shell evidence and comparator evidence. Use the actual SAP, a supplied convention, another shell, a calculation or an applicable external provision. If no SAP is supplied, do not claim SAP agreement or disagreement. For a missing shell cite the SAP analysis and the reviewed shell directory. If the missing object has no ID, link the issue to its analysis ID. A single defect affecting several shells uses one comment linked to each affected check. Classify certainty separately from severity, and keep low-confidence issues out of Critical.

Mock review evaluates specified structure and logic. Numeric correctness of populated outputs requires analysis data and results-validation evidence.
