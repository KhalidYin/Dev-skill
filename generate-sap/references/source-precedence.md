# Source Precedence and Citation

Use this file whenever sources, guidance, precedents, or conflicts affect drafted content.

## Evidence classes

Keep these classes distinct:

1. `current_study_fact`: study-specific facts from the current approved source set.
2. `confirmed_decision`: a documented decision by the accountable study team or Sponsor.
3. `sponsor_convention`: an effective organization-wide rule.
4. `normative_reference`: an actually verified regulatory guideline or formal standard.
5. `trial_precedent`: a comparable study's SAP, protocol, CSR, review, or publication.
6. `method_reference`: a verified methodological source.
7. `general_knowledge`: uncited background knowledge; never sufficient for a study-specific fixed parameter.

## Default precedence

Use explicit task instructions first, then the current approved Protocol and amendments, documented study decisions, effective Sponsor conventions, verified normative references, verified trial precedents, and finally general knowledge.

This order is not permission to hide conflicts. If two current authoritative sources disagree, preserve both and create a `CONFLICT` query. Do not choose one merely because it appears later or looks more plausible.

## Citation record

Every material external reference must include:

```yaml
reference_id: REF-001
reference_type: normative_reference | trial_precedent | method_reference
title: ""
authors_or_organization: ""
document_type: guidance | sap | protocol | csr | regulatory-review | publication
version: ""
date: ""
status: final | effective | draft | withdrawn | historical | unknown
direct_url: ""
retrieved_date: YYYY-MM-DD
location:
  section: ""
  page: null
supported_summary: "short paraphrase of the relevant point"
limitations: []
```

Never cite a search-result page, an unverified snippet, a fabricated clause, or a source that cannot be resolved. Keep quotations short and prefer paraphrase.

## Conflict handling

For a conflict:

1. Record each statement with its source and locator.
2. State the affected content units and downstream sections.
3. Generate only the common supported content.
4. Insert a stable `CONFLICT` author query where the decision is required.
5. Do not mark the content final until an accountable owner resolves it.

## Precedent boundary

A trial precedent may identify a candidate method, specification, sensitivity analysis, or drafting pattern. It cannot establish that the same choice is appropriate for the current study. Record material similarities and differences before using it.

For autonomous comparable-study research, follow [precedent-research.md](precedent-research.md). It defines the source tiers, screening process, direct-reference fields, and explicit failure states.
