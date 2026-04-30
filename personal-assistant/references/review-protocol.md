# Review protocol

When the user issues an audit/review/inspection command (examples: "审核修复", "检查实现", "review this", "audit the code", "check for issues"), follow a two-tier approach: **Quick Review** first, then offer **Full Report**.

## Quick Review (default)

Always start here. Output 3-5 bullet points directly in the response — no file is generated.

Format:

```
## Quick Review

- [finding 1: what was checked, what was found]
- [finding 2: issue or gap identified]
- [finding 3: risk or concern]
- [summary verdict: OK / needs attention / blocking]

需要我生成完整的审查报告到 `docs/dep/` 吗？
```

Quick Review covers:
- Critical issues (bugs, security, data loss)
- Missing pieces vs spec/docs
- Obvious deviations from conventions
- A one-line verdict

## Full Report (on demand)

Only generate when the user confirms they want it (after being prompted, or if they explicitly ask for "完整报告", "生成报告", "full report", "write report").

### Naming convention

```
docs/dep/review-<YYYYMMDD>-<round>.md
```

- `YYYYMMDD` — date the review was performed
- `round` — sequential round number per day: `01`, `02`, `03`, ...

If there is already a report for the same date and topic, increment the round. If the review is a continuation of a prior day's review, start a new file with `round-01` and link back to the previous report.

### Report template

```markdown
---
date: YYYY-MM-DD
round: N
trigger: "user prompt that triggered this review"
status: in-progress
---

# Review Report — YYYY-MM-DD Round N

## Scope
<!-- What was reviewed (files, features, modules) -->

## Findings

### Issues
<!-- Problems found: bugs, inconsistencies, missing pieces -->

| # | Severity | File/Area | Description | Status |
|---|----------|-----------|-------------|--------|
| 1 | high/medium/low | path:line | ... | open/fixed/deferred |

### Unimplemented / Incomplete
<!-- Features or behaviors mentioned in docs/spec but not in code -->

| # | Reference | Description | Next step |
|---|-----------|-------------|-----------|
| 1 | doc/spec ref | ... | ... |

### Deviations
<!-- Code that diverges from documented intent or conventions -->

| # | Expected | Actual | Impact |
|---|----------|--------|--------|
| 1 | ... | ... | ... |

## Next Actions
<!-- Concrete next steps, prioritized -->

1. ...
2. ...

## Linked Reports
<!-- Previous related reviews -->
- [Review YYYY-MM-DD Round N-1](review-YYYYMMDD-NN.md)
```

### Status tracking

- **in-progress** — report written, issues still open
- **resolved** — all issues closed, no remaining actions
- **deferred** — some issues explicitly deferred by user

Update the report's frontmatter `status` and the findings table as issues are addressed in follow-up work.

## When NOT to generate

Skip both Quick Review and Full Report when:

- The task is a simple code change or bug fix (not a review)
- The user asks for a one-line answer about code behavior
- The task is purely about writing new code (no review implied)
