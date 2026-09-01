---
name: generate-sap
description: "Explicitly invoked authoring support for creating or revising a clinical trial Statistical Analysis Plan or SAP sections from protocol facts, sponsor conventions, confirmed decisions, and verified public precedents. Use only for SAP content generation. Do not use for SAP review alone, TFL or ADaM generation, or statistical programming."
---

# Generate SAP

Generate a reviewable clinical-trial Statistical Analysis Plan. Treat this skill as an authoring constraint package, not as an agent workflow or an approval authority.

## Non-negotiable behavior

1. Instantiate the complete target SAP structure before drafting section content.
2. Preserve every required section even when information is incomplete.
3. Place missing inputs, source conflicts, and unresolved decisions in the affected section with stable query IDs.
4. Continue drafting unaffected sections when one content item is blocked.
5. Distinguish sourced facts, deterministic derivations, proposed choices, unresolved items, conflicts, and non-applicable content.
6. Keep a structured generation record linking drafted content to facts, rules, assumptions, references, and open questions.
7. Never silently fill study-specific parameters from generic knowledge or another trial.
8. Require qualified statistician review. Never label output approved or regulator-compliant.
9. Keep current-study sources in `document.source_versions` and `source_facts`; reserve `references` for verified external material.

## Required outputs

Return these logical artifacts:

1. `SAP Review Draft`: the complete document structure with supported prose and inline author queries.
2. `Generation Evidence Ledger`: structured support for each material content unit.
3. `Open Questions and References`: unresolved items plus direct, traceable references.

## Authoring boundary

- Create or revise a full SAP or named SAP sections.
- Use supplied Protocol facts, Sponsor conventions, confirmed statistical decisions, and actually verified public sources.
- Search for comparable public SAPs when substantive statistical sections are requested and network search is available.
- Treat comparable trials as precedents, not normative requirements.
- If search is unavailable or yields weak matches, record the limitation and continue with supported content and local queries.

Do not perform standalone SAP compliance review, TFL or ADaM generation, statistical programming, patient-level analysis, or workflow orchestration.

## Core sequence

1. Normalize the request, source inventory, study facts, confirmed decisions, conventions, and unresolved inputs.
2. Select the target template and instantiate every required heading.
3. Build a study fingerprint and, when tools permit, research comparable public trials before drafting substantive statistical choices.
4. Load only the references needed for the current sections.
5. Generate each content unit under one allowed generation mode.
6. Add inline `TBD`, `AUTHOR QUERY`, or `CONFLICT` markers where support is insufficient.
7. Check cross-section consistency and assemble the three required outputs.
8. When writing artifacts as files, build the Ledger from individually validated JSON records with the packaged deterministic builder; do not hand-append the final YAML.
9. Apply the output contract. When Draft and Ledger files exist, run the packaged structural validator and report any failures without rewriting the artifacts.

## Load core resources

- Read [input-contract.md](references/input-contract.md) for every invocation.
- Read [output-contract.md](references/output-contract.md) for every invocation before drafting.
- Read [source-precedence.md](references/source-precedence.md) whenever sources, guidance, precedents, or conflicts are involved.
- Read [precedent-research.md](references/precedent-research.md) before drafting substantive statistical sections when external research is allowed; use its explicit degraded states when search cannot be performed.
- Read [content-unit-contract.md](references/content-unit-contract.md) before drafting any material section.
- Read [section-map.md](references/section-map.md) when selecting or instantiating a structure.
- Use [sap-template.md](assets/sap-template.md) when no Sponsor template is supplied.
- Use [generation-record-template.yaml](assets/generation-record-template.yaml) for the evidence ledger and query index.
- Use `scripts/build_evidence_ledger.py` when creating the Ledger as a file; it validates record syntax and serializes YAML without changing record meaning.
- Read [cross-section-checks.md](references/cross-section-checks.md) before final assembly.

Load section-specific rules only for sections being drafted:

- [study-design-rules.md](references/study-design-rules.md): Sections 5, 6, 7.1, 8, 10, and 15.
- [estimand-ice-rules.md](references/estimand-ice-rules.md): estimands, ICEs, and dependent analysis content.
- [population-rules.md](references/population-rules.md): analysis populations and assignment rules.
- [efficacy-analysis-rules.md](references/efficacy-analysis-rules.md): efficacy methods and model specifications.
- [missing-sensitivity-rules.md](references/missing-sensitivity-rules.md): missing-data assumptions and sensitivity analyses.
- [safety-analysis-rules.md](references/safety-analysis-rules.md): baseline safety authoring constraints.

Do not read every reference by default.
