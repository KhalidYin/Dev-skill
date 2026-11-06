---
name: review-tfl-shell
description: "Review or QC existing clinical TFL mock shells (tables, figures and listings; TFL样表审核、脚注审核) against the SAP. Check analysis coverage, titles, headers, footnotes, legends, programming notes, statistical definitions, data support and cross-output consistency. Produce a concise Excel issue log with actionable comments, rationale and sources. Use tfls-shell for generating shells, review-sap for reviewing a SAP, and a results-validation workflow for populated TFL numerical validation."
---

# Review TFL Shell

Review existing shells against the study's analysis commitments. Read supplied documents without modifying them. Write comments in the user's language and preserve source excerpts in their original language.

1. **Intake.** Read [review-guide.md](references/review-guide.md). Identify the shell package and directory, SAP versions, global conventions and available Protocol, CRF, completion instructions, external data specifications and ADaM specifications. A readable shell is essential. Shell-only review proceeds with SAP-dependent checks marked not-assessable.
2. **Map analysis to output.** First identify the study design and statistically distinct parts, the estimands or decision targets, and the reporting purpose. Inventory every shell and every material SAP analysis, including primary, secondary, sensitivity, subgroup, safety and decision analyses. Assign stable IDs and locators. Map analyses and shells in both directions. One-to-many and many-to-one relationships are valid. Record omitted analyses and the purpose of additional outputs.
3. **Review the complete display.** Apply [checklist.yaml](assets/checklist.yaml). Read global conventions before local title, headers, body, footnotes, legends and programming notes. Review each shell's applicable items, then compare shared definitions across outputs. Use the SAP's definitions and trace unresolved study objectives or estimands to the Protocol.
4. **Assess data support.** Trace required information to collection fields or external sources and any derivations. Match versions. Distinguish absent evidence from a demonstrated collection gap. A visit schedule establishes planned assessments; field definitions and precision require collection specifications. Record partial support precisely.
5. **Verify comments.** Use the finding rules in review-guide.md. Give the exact shell/row/column/note location, author-facing correction, statistical or implementation consequence, and source. Reopen evidence. Merge repeated defects into one comment with all affected shells. Distinguish semantic defects from formatting issues.
6. **Build and deliver.** Follow [output-contract.md](references/output-contract.md). Run the packaged builder, deliver the three-tab workbook and summarize major issues and unresolved inputs. Add optional details only when requested or needed to inspect the full checks. Follow-up replies and status updates belong in Comments.

```powershell
python scripts/build_issue_log.py plan --input review.json
python scripts/build_issue_log.py check --input review.json
python scripts/build_issue_log.py build --input review.json --out tfl-shell-review.xlsx
```

Run from the skill directory or use absolute paths. Requires Python 3.9+, PyYAML and openpyxl. The builder validates links and evidence fields. Statistical interpretation and source verification are part of the review.
