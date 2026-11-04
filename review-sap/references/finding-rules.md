# Finding Rules

## Finding types

| Type | Meaning |
|------|---------|
| `error` | Evidence shows that a statement is wrong or a value is impossible |
| `inconsistency` | Two source statements conflict, or the SAP substantively changes a Protocol-planned analysis |
| `omission` | Content required by a checklist item is absent |
| `ambiguity` | The content exists but allows more than one reasonable implementation |
| `suggestion` | An improvement that no checklist item or source requires. Never ranked above Minor |
| `out-of-scope-observation` | A methodological concern outside v1 scope. Severity is `n/a`. Kept so it is not lost |

## Severity

Judge severity by the consequence for the trial's conclusions and for the analysis work, not by how easy the fix is.

| Severity | Use when |
|----------|----------|
| **Critical** | The primary or key secondary analysis cannot be carried out as written, or would answer a different question than the Protocol. Examples: primary endpoint, estimand, population, alpha, sample size, or multiplicity contradicts the Protocol or itself; no stated hypothesis or margin for an NI test; censoring rules missing for a primary TTE endpoint; early-phase dose decision rules missing. |
| **Major** | Likely to change results of secondary, sensitivity, or safety analyses; or two programmers would implement an important derivation differently; or an inspection or regulatory query is likely. Examples: undefined baseline, overlapping visit windows, populations without derivation rules, an undeclared difference from the Protocol for a secondary endpoint. |
| **Minor** | Limited effect on results; a clarification is needed. Examples: missing rounding rules, missing dictionary version, adherence definition vague. |
| **Editorial** | Typos, formatting, broken cross-references, undefined abbreviations. |

The checklist's `severity_hint` is a starting point. Move it up or down only for a reason you can state in `rationale`. A finding on a primary endpoint is usually at least Major.

## Evidence

Each finding must carry:

- `sap_locator` (section, table, or page) and a short `sap_excerpt` (at most about 40 words, verbatim) or a precise statement of the absence ("Section 9 defines FAS and SS only; no PP definition").
- For every Critical finding, every `error` or `inconsistency`, and every PRO-dimension finding, supply `comparator_source` (a document ID, or `SAP` for internal comparisons), `comparator_locator`, and `comparator_excerpt`. For a Critical omission, cite the source statement that makes the missing rule necessary, such as the definition of the primary time-to-event endpoint.
- `checklist_items`: one or more checklist IDs. An `out-of-scope-observation` uses `[]`.

## Confidence and verification

- `confidence`: `high` when both locators are verbatim and unambiguous; `medium` when interpretation is involved; `low` when the text comes from OCR or unclear tables, or the finding depends on an assumption. A low-confidence finding cannot be Critical. Phrase it as a question to the author.
- `verification`: `self` by default; `independent-confirmed` or `independent-disputed` when a separate reviewer re-checked it. Keep a disputed finding, note the dispute, and let the human reviewer decide.

## Wording

- `issue`: one or two sentences saying what is wrong and where. Use neutral wording ("The SAP states... whereas the Protocol states..."). Do not write "the author failed to".
- `recommendation`: what needs to change or be decided, and by whom when that is clear ("Confirm with the study team whether..."). Do not draft replacement SAP text.
- `rationale`: why the severity was chosen, in one sentence.

## Coverage records

- Every applicable checklist item gets one coverage record.
- `pass` needs a short `note` naming where it was confirmed (for example, "Sec 8.1; matches Protocol 10.2").
- `finding` lists `finding_ids`.
- `not-applicable` says which design tag excludes it.
- `not-assessable` names the missing input or the unreadable content.

## Self-check before building

1. Does every finding have a locator I could open and point to?
2. Is any "requirement" I cited actually in the checklist or the documents? If not, it is a `suggestion`.
3. Are there duplicates (one defect raised under several items)? Merge them and list all affected items.
4. Does every Critical have both locators and `high` or `medium` confidence?
5. Did I mark items `pass` without looking? Every pass needs a location in its note.
6. Did I separate disclosure from consistency? A justified, disclosed change can satisfy PRO-12 and still warrant a finding under the affected PRO item. A supplementary analysis that preserves the planned analysis can satisfy both checks.
7. Did any methodology judgment slip into a ranked finding? Move it to `out-of-scope-observation`.
