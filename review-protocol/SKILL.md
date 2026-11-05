---
name: review-protocol
description: "Review an existing clinical trial protocol (临床试验方案审核、统计审阅) from a biostatistics perspective. Classify the study and each statistically distinct part before selecting checks and looking up applicable guidance and similar public protocols. Audit objectives, design, endpoints, data collection, sizing, analysis, safety and decision rules, then produce an evidence-linked Excel issue log. Covers single-arm, randomized, dose-finding, and other designs across phases. Use review-sap when the primary document under review is a Statistical Analysis Plan."
---

# Review Protocol

Audit an existing clinical trial protocol. The review is for qualified statistician follow-up. The protocol stays read-only. Report observed defects and questions for adjudication. Approval, regulatory compliance, and protocol drafting are outside this workflow.

1. **Intake.** Require the protocol or a readable excerpt with identifiable sections. Record version/date and input completeness. Optional inputs include amendments, SAP, charter, CRF, and operating-characteristic reports. A missing optional document affects only checks that depend on it. If the protocol itself is unavailable, request it and stop before issuing findings.
2. **Classify before searching.** Read [design-and-sources.md](references/design-and-sources.md). Extract purpose, comparison structure, implementation, and inference/decisions from the synopsis, design, objectives, and statistics. Cite the protocol. Use one unit for a homogeneous study and separate units for parts or cohorts with materially different statistical rules. In a multipart study record shared checks once in a study-wide unit. Flag conflicting or insufficient classification evidence and continue on unaffected checks. Record unusual design and its implications at intake.
3. **Establish the review target and basis.** Use [checklist.yaml](assets/checklist.yaml) and applicable regulatory guidance. For each treatment-effect objective, establish the protocol's estimand before judging methods. For decision-driven parts, establish the decision target, inputs and criteria. Search comparable public protocols by de-identified traits to assess practical choices. Record the specific effect of any missing evidence.
4. **Check statistical chapter completeness first.** Apply the chapter layer of the checklist. Map each applicable topic to its substantive content across the full protocol, regardless of headings. Separate missing commitments, supplied evidence, valid SAP detail and missing evidence. Follow [review-rules.md](references/review-rules.md).
5. **Trace each analysis to its target.** Complete the existing analysis matrix in this order: objective and target → design and data collection → estimator and assumptions → sensitivity and decision. Judge whether each step supports the same estimand or decision target. For practical adjustments, identify the reason, changed assumptions and effect on the target. Cross-check the synopsis, statistics, schedule and sizing; resolve substantive ambiguity through a specific author comment.
6. **Verify and deliver.** Reopen cited evidence and verify all Critical and Major findings. Give each defect one author-facing comment with rationale and source, linked across coverage and analysis matrix as needed. Read [output-contract.md](references/output-contract.md), write the UTF-8 JSON bundle, and run the builder. Deliver the four-tab workbook and a brief chat summary. Add the Traceability tab when requested or needed to show material comparisons or specialist evidence.

```powershell
python scripts/build_issue_log.py plan --input review.json
python scripts/build_issue_log.py check --input review.json
python scripts/build_issue_log.py build --input review.json --out protocol-review-issue-log.xlsx
```

Run these commands from the skill directory or use absolute paths. Python 3.9+, PyYAML and openpyxl are required. The builder checks the output contract and assembles the workbook. Assess the evidence and statistical logic before invoking it.
