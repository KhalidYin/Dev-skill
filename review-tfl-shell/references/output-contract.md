# Review bundle and workbook

Use UTF-8 JSON as the editable review record. The Python builder reads the bundle; it does not read or judge clinical documents. Dependencies: `python -m pip install openpyxl PyYAML` when unavailable.

## Prepare and route

Required top-level arrays are `documents`, `shells`, `analyses`, `findings`, `checks`, plus the `review` object. IDs are stable, unique within an array; shell and analysis IDs must not overlap. Use document versions/dates exactly as supplied; write `not stated` if absent.

```json
{
  "review": {
    "title": "Study TFL review", "date": "2026-11-06",
    "checklist_version": "0.1.0",
    "study_context": "Single-arm study; ORR estimation in all treated participants",
    "scope": "Complete SAP and supplied shell package",
    "limitations": "Collection specifications not supplied; field support unassessed"
  },
  "documents": [
    {"id":"D-SAP", "role":"sap", "title":"SAP", "version":"1.0", "date":"2026-10-01", "location":"/project/SAP.pdf"},
    {"id":"D-TFL", "role":"shell", "title":"Shells", "version":"1.0", "date":"2026-10-10", "location":"/project/shells.docx"}
  ],
  "analyses": [
    {"id":"A-ORR", "document_id":"D-SAP", "title":"Primary ORR", "locator":"§8.1"}
  ],
  "shells": [
    {"id":"T-ORR", "document_id":"D-TFL", "type":"T", "title":"ORR", "locator":"Table 14.2.1", "analysis_ids":["A-ORR"]}
  ],
  "findings": [], "checks": []
}
```

This is an intake example for `plan`, not a completed review. `plan --input review.json` lists each applicable target/check pair. Complete every pair with state `review` before `check` or `build`. Do not submit entries for automatically not-assessable pairs. No SAP means SAP-dependent checks are automatic not-assessable; no CRF, collection-spec or external-spec makes DATA-01 automatic not-assessable. If supplied collection specifications support only some variables, record that partial support rather than passing the whole shell.

Allowed document roles: `shell`, `sap`, `protocol`, `convention`, `crf`, `collection-spec`, `external-spec`, `adam-spec`, `reference`, `other`. At least one readable shell is required. `analyses: []` is valid without a SAP. A supplied but unreadable/incomplete SAP requires an explicit `review.analysis_gap` when no analyses can be inventoried; relevant checks remain not-assessable. Inventory analyses independently of the shell list to detect missing outputs.

## Checks and findings

Each check has `target_id`, `item_id`, `status`, `note`, and optionally `finding_ids` and `evidence`. States:

- `pass`: specific located evidence required, stating why the item is satisfied.
- `finding`: at least one linked finding required.
- `not-applicable`: concrete absent premise in note.
- `not-assessable`: missing input and blocked judgment in note.

Evidence is an array of `{ "doc_id": "D-SAP", "locator": "§8.1", "text": "Exact source excerpt" }`. Document locations can be local paths or verified source URLs. For an absence cite the searched section/directory and state the scope of the absence; do not manufacture a quotation. Analysis coverage cannot pass without a mapped shell. Coverage completeness is a record of performed checks, not proof of clinical validity.

Example finding (adapt to actual evidence):

```json
{
  "id":"F-001", "target_ids":["T-ORR"],
  "type":"inconsistency", "priority":"Major", "confidence":"high",
  "comment":"请将脚注中的可评价受试者分母改为所有已治疗受试者，并注明缺失或不可评价者计为非应答，与 SAP §8.1 保持一致。",
  "rationale":"当前脚注会排除不可评价者，改变预设 ORR 分母及应答率。",
  "evidence":[
    {"doc_id":"D-TFL", "locator":"Table 14.2.1 note a", "text":"Percentages use evaluable participants."},
    {"doc_id":"D-SAP", "locator":"§8.1", "text":"ORR denominator includes all treated participants; missing or unevaluable response is nonresponse."}
  ],
  "status":"Open", "author_response":"", "reviewer_followup":""
}
```

Allowed finding types: `omission`, `inconsistency`, `error`, `ambiguity`, `clarification`, `editorial`. Priorities: `Critical`, `Major`, `Minor`, `Editorial`, `Query`. Confidence: `high`, `medium`, `low`. Substantive ambiguity additionally requires different `reading_a` and `reading_b`, with consequences in rationale. Critical and inconsistency/error findings require at least two evidence locations. Each affected target needs its own location evidence and linked check; a shared defect is one finding with several targets. The script checks document IDs; the reviewer verifies that cited positions actually cover every target.

Link the finding in each affected check, for example `{"target_id":"T-ORR","item_id":"NOTE-02","status":"finding","note":"分母与 SAP 不一致","finding_ids":["F-001"]}`. Complete the remaining routed checks individually.

## Fixed core, study-specific extensions

The 21 core checks remain stable. Add scoped checks through optional `extra_checks`, without replacing core items:

```json
"extra_checks": [
  {"id":"X-DLT-01","group":"研究专项","target":"T","sap_required":true,
   "check":"Verify DLT evaluability, observation window and dose-decision summaries against the prespecified decision rule."}
]
```

Targets are `all`, `analysis`, `T`, `F`, `L`; `sap_required` is boolean. Give nonapplicable targets a reason. Add design/endpoint-specific checks where needed: dose escalation and expansion, single-arm benchmarks, recurrent events, competing risks, estimand strategies or multistage decisions. Select applicable current guidance and similar public studies to inform the review, and distinguish study commitments, guidance recommendations and illustrative practices.

## Build and deliver

Run `check` then `build --out review.xlsx`; `build` also validates. Existing files are never overwritten. Use a new output version when incorporating responses. Retain the JSON as the editable evidence record.

Default workbook:

1. **Overview**: scope, study context, document versions, blocked judgments and issue/status totals.
2. **Comments**: nine fixed columns — ID, Shell／分析, 级别, 作者批注, 理由, 位置、证据与来源, 状态, 作者回复, 复核意见. Status choices: Open, Responded, Closed. Original source strings are written as text.
3. **SAP-TFL Crosswalk**: bidirectional mapping and grouped coverage. Missing outputs appear under analysis IDs. Pass/finding/not-applicable/not-assessable remain distinguishable.

`--details` adds **Check Details** for individual items and evidence. Extra checks expand coverage rows, not the nine-column Comments schema. COUNTIF summary formulas recalculate on opening in Excel; openpyxl does not calculate cached values. Reopen the workbook to verify tabs, links, text and formulas; inspect layout when a renderer is available. Deliver the workbook and identify the material inputs still needed, without calling incomplete checks passed.
