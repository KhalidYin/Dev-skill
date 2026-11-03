# Input Contract

## Documents

| Role | Required | Used by | If missing |
|------|----------|---------|------------|
| `sap` | Yes | All dimensions | Stop: nothing to review |
| `protocol` | For PRO | PRO-01 to PRO-12, PRG-14 fallback | Mark every PRO item `not-assessable`; still run STR, INT, PRG |
| `protocol-amendment` | When any exist | PRO-01 and all PRO items | Mark PRO-01 a finding if the SAP cites an amendment that was not supplied; otherwise note it as a limitation |
| `tfl_shells` | No | PRG-15, INT-04 | Mark PRG-15 `not-assessable` |
| `crf` | No | PRG-14 | Use the Protocol schedule of activities and note the substitution; if there is no Protocol either, mark PRG-14 `not-assessable` |
| `dmc_charter` | No | PRO-09 | Review PRO-09 against the Protocol only |
| `sponsor_sop` | No | STR administrative items | Use the generic checklist |
| `prior_sap` | No | STR-02 (change verification) | Review the revision history as stated |

Record each document once as a `document` record: role, title, version, date, and file name.

## Formats

- `.docx`: read the text with section numbering preserved, and keep page or section locators. Only a .docx can receive comments later.
- `.pdf`: extract the text. Use the page number as the locator. Rasterize the page when tables or numbers do not extract cleanly. Scanned PDFs need OCR. Lower the confidence of findings drawn from OCR text.
- `.md` or plain text: use heading paths as locators.

Never edit the supplied files. Work on copies.

## Design tags

Derive the design tags from the documents. Do not ask for them unless the documents conflict.

- `rct`: randomized comparison between arms.
- `early-phase`: phase I or I/II, dose finding, or first-in-human.
- `tte`: any time-to-event primary or key secondary endpoint.
- `non-inferiority`: an NI or equivalence hypothesis.
- `adaptive`: pre-planned adaptations (sample size re-estimation, arm dropping, seamless phases).
- `bayesian`: Bayesian inference or decision rules.
- `multi-cohort`: basket, umbrella, platform, or expansion cohorts.

`all` items always apply. Record the chosen tags in the `review` record.

## When to ask before starting

Ask one short question only if one of these applies:

- No SAP was supplied, or the file cannot be read.
- Several SAP versions were supplied and it is unclear which one is under review.
- The user asked for Protocol consistency, but the Protocol was not supplied.

Otherwise, start, and record gaps as `not-assessable` coverage with the missing input named.

## Language

Write findings in the language the user writes in. Keep SAP and Protocol excerpts in their original language. Excel headers are bilingual.

## Confidentiality

Study documents are confidential by default. Do not send their content to web search. Checklist-basis lookups use only generic terms (guideline names, method names).
