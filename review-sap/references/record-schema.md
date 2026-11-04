# Record Schema

Stage one JSON object per `add` call. The builder validates each record when it is added, and validates relationships between records in `check` and `build`. Unknown fields are rejected. Strings are trimmed, and required strings cannot be empty.

## `review` (exactly one)

```json
{
  "review_id": "RV-001",
  "title": "SAP review: <study short name>",
  "sap_document_id": "DOC-01",
  "review_date": "2026-11-03",
  "reviewer": "AI-assisted draft (requires statistician review)",
  "design_tags": ["rct", "tte"],
  "dimensions_in_scope": ["STR", "INT", "PRO", "PRG"],
  "checklist_version": "1.0.0",
  "language": "zh",
  "limitations": ["No CRF supplied; PRG-14 assessed against Protocol SoA"]
}
```

`design_tags` lists the matching design tags. Use `[]` when only the implied `all` applies. `checklist_version` must equal the packaged checklist's version. For a run staged under an earlier checklist version, reassess coverage under the current checklist and stage the records in a new run directory.

## `document`

```json
{"document_id": "DOC-02", "role": "protocol", "title": "Clinical Study Protocol", "version": "3.0", "date": "2026-05-10", "file_name": "protocol_v3.pdf"}
```

`role`: `sap`, `protocol`, `protocol-amendment`, `tfl_shells`, `crf`, `dmc_charter`, `sponsor_sop`, `prior_sap`, `other`. ID pattern `DOC-NN`.

## `crosswalk`

```json
{"row_id": "XW-001", "group": "Sample size", "parameter": "Total N", "sap_value": "N=400", "sap_locator": "Sec 8.1", "protocol_value": "N=420", "protocol_locator": "Sec 10.2", "match": "mismatch", "finding_ids": ["F-002"], "note": ""}
```

`match`: `match`, `mismatch`, `sap-only`, `protocol-only`, `declared-change`, `unclear`. ID pattern `XW-NNN`. At least one value is required. `sap_value` may be empty only for `protocol-only` or `declared-change`, and `protocol_value` only for `sap-only` or `declared-change` (for example, an analysis the SAP adds and declares).

## `finding`

```json
{
  "finding_id": "F-002",
  "dimension": "PRO",
  "checklist_items": ["PRO-05", "INT-03"],
  "type": "inconsistency",
  "severity": "Critical",
  "sap_locator": "Sec 8.1, para 2",
  "sap_excerpt": "A total of 400 participants (200 per arm) will be randomized.",
  "comparator_source": "DOC-02",
  "comparator_locator": "Sec 10.2",
  "comparator_excerpt": "Approximately 420 participants will be randomized 1:1.",
  "issue": "...",
  "recommendation": "...",
  "rationale": "...",
  "confidence": "high",
  "verification": "self"
}
```

- `dimension`: `STR`, `INT`, `PRO`, `PRG`, or `MTH`. Use `MTH` only with `out-of-scope-observation`.
- `type`: `error`, `inconsistency`, `omission`, `ambiguity`, `suggestion`, `out-of-scope-observation`.
- `severity`: `Critical`, `Major`, `Minor`, `Editorial`, `n/a`. Use `n/a` only for `out-of-scope-observation`. A `suggestion` is `Minor` or `Editorial`.
- `confidence`: `high`, `medium`, `low`. A `low` finding cannot be `Critical`.
- `verification`: `self`, `independent-confirmed`, `independent-disputed`.
- `comparator_*` fields are required for every Critical finding, every `error` or `inconsistency`, and every `PRO` finding. `comparator_source` is a defined `document_id` or `SAP`.
- `checklist_items` must be non-empty and defined in the checklist, except for `out-of-scope-observation`, which uses `[]`.
- ID pattern `F-NNN`.

## `coverage`

```json
{"item_id": "PRO-05", "status": "finding", "finding_ids": ["F-002"], "note": "Sec 8.1 vs Protocol 10.2"}
```

`status`: `pass`, `finding`, `not-applicable`, `not-assessable`. `note` is required. `finding_ids` is non-empty exactly when the status is `finding`.

## Cross-record rules enforced by `check`

1. Exactly one `review`. Its `sap_document_id` is a defined `sap` document.
2. Every applicable checklist item has exactly one coverage record. An item is applicable when its dimension is in scope and its `applies_to` includes `all` or one of the review's design tags. Coverage for a non-applicable item, if one is added, must be `not-applicable`.
3. If an item's required documents are missing, its status must be `not-assessable` or `not-applicable`. The one exception is an item whose `alternate_requires` are all present.
4. For each finding, every listed checklist item has coverage status `finding` that includes this finding ID. Each finding linked from coverage lists the same checklist item. Every finding ID listed in coverage or the crosswalk is defined.
5. Every non-`MTH` finding is referenced by at least one coverage record.
6. Every ID is unique within its type.
