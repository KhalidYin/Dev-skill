# Issue log input

Use UTF-8 JSON. Start with the review metadata, documents, review units and analysis inventory, then run `plan`. It prints unit/item routes and the matrix slots for each identified analysis. Supply coverage only for `review` pairs. The builder supplies coverage for unresolved tag applicability and absent required documents. Inactive design rules are omitted from the compact workbook. If evidence resolves a missing input or design feature, rerun the plan.

```json
{
  "review": {
    "title": "Protocol statistical review",
    "date": "2026-11-04",
    "protocol_id": "DOC-01",
    "checklist_version": "0.2.1",
    "input_scope": "full",
    "retrieval_status": "limited",
    "retrieval_note": "Official guidance consulted. No directly comparable public protocol located."
  },
  "documents": [
    {
      "id": "DOC-01",
      "role": "protocol",
      "title": "Study Protocol",
      "version": "2.0",
      "date": "2026-10-10",
      "location": "protocol.pdf"
    }
  ],
  "units": [
    {
      "id": "U-01",
      "title": "Whole study",
      "scope": "whole",
      "purpose": "Exploratory activity",
      "comparison": "Single-arm descriptive estimation",
      "structure": "One fixed-size cohort",
      "inference": "Estimate response and uncertainty",
      "locator": "Protocol §3.1 and §10.1",
      "tags": ["single-arm"],
      "uncertain_tags": [],
      "scope_note": "One cohort with shared statistical rules."
    }
  ],
  "sources": [],
  "crosswalk": [],
  "analyses": [
    {
      "id": "A-01",
      "unit_id": "U-01",
      "title": "Objective response rate",
      "role": "primary",
      "locator": "Protocol §3.1 and §10.1"
    }
  ],
  "analysis_matrix": [],
  "findings": [],
  "coverage": []
}
```

This example is the intake for `plan`. Add crosswalk, chapter and other coverage records, and the analysis matrix before `check` or `build`. Record unknown metadata explicitly as `unknown`. Use `excerpt` for partial protocol input. All fields are strings unless shown as arrays. Use stable IDs and retain the source document version when comparing. Supported optional document roles include `protocol-amendment`, `sap`, `crf`, `charter`, `simulation`, `sop` and `other`. In a multipart review use one `shared` unit and two or more `part` units. In the shared unit record study-wide commitments, and mark core items whose premise is entirely part-specific as `not-applicable` with a reason.

## Complete the review bundle

- **Sources.** Provide `id`, `kind` (`regulation`, `guidance`, `reporting-reference`, `public-precedent`), `title`, direct `url`, `version`, `status`, `region`, `checked_date`, `locator`, `relevance`, and `limits`. For a public precedent include `document_type` such as protocol, amendment, or registry summary. An applicable external requirement cited for Critical or Major must be verified as `effective` or `final` and linked to a precise provision.
- **Crosswalk.** Provide `unit_id`, `parameter`, `value`, `locator` and `assessment` (`observed`, `agrees`, `conflict`, `disclosed-change`, `unresolved`). Add `other_doc_id`, `other_locator`, and `other_evidence` for comparisons. An internal comparison uses the protocol document ID as the comparator. Use `note` to record disclosure separately from agreement. For a missing or conflicted value, report the gap and where you looked.
- **Analyses and matrix.** Each analysis has `id`, `unit_id`, `title`, `role` and `locator`. Roles are `primary`, `key-secondary`, `secondary`, `exploratory`, `safety`, `decision`, `sensitivity` and `supplementary`. For every routed slot give an `analysis_matrix` row with `analysis_id`, `slot`, `status`, `note`, and optional `value`, `locator`, `finding_ids` (list). Use `pass`, `finding`, `sap-detail`, `not-applicable`, or `not-assessable`. Pass and SAP detail need the protocol value and location. Findings need two-way links. For design slots that do not apply to a particular endpoint, give the reason. If the primary analysis cannot be identified, record the coverage finding or evidence gap under `CH-04` and continue with identifiable analyses.
- **Findings.** Provide `id`, `unit_id`, `item_ids` (list), `type`, `severity`, `confidence`, `locator`, `evidence`, author-facing `comment` and `rationale`. Include `analysis_ids` (list) for affected matrix analyses. Types are `error`, `inconsistency`, `omission`, `ambiguity`, `method-mismatch` and `statistician-review`. Severity is `Critical`, `Major`, `Minor`, or `Editorial`. Leave it empty for `statistician-review`, which may omit checklist links for questions outside the packaged checks. Confidence is `high`, `medium`, or `low`. A material ambiguity requires `reading_a` and `reading_b`. For a Critical, error or inconsistency include `other_doc_id`, `other_locator` and `other_evidence`. A method mismatch needs comparator evidence or a precise applicable external basis. For an external basis include `basis_id` and `basis_locator`. A precedent cannot serve as finding basis. `status` defaults to Open. `author_response` and `reviewer_followup` are optional.
- **Coverage.** For each routed `review` pair provide `unit_id`, `item_id`, `status`, `note`, optional `locator`, and `finding_ids` (list). Pass and SAP detail require a locator. Links are present exactly when the status is `finding` and must match the finding's unit and checklist IDs. Give an explanatory reason for `not-assessable` and `not-applicable`.

## Fixed workbook

The four tabs are `Overview` (version, scope, coverage and live status totals), `Comments` (nine columns for reading, evidence and tracking), `Coverage` (filter the chapter, statistical and cross-check layers), and `Analysis Matrix` (slot-level assessments). The comments include source titles, locators, evidence text and the URL for any cited external basis. The builder preserves excerpts as text and refuses to overwrite a workbook. Use `build --details` for one optional `Traceability` tab with cross-file comparisons and retrieved sources. Extend review topics and design-specific matrix slots through the YAML checklist while keeping the four core tab schemas fixed.

Bundles from checklist 0.1.0 require reassessment against the 0.2.0 chapter and matrix checks. Use the original workbook for its recorded review snapshot.
