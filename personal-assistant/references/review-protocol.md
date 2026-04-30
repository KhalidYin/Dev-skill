# Review protocol

When the user issues an audit/review/inspection command (examples: "审核修复", "检查实现", "review this", "audit the code", "check for issues"), follow a two-tier approach: **Quick Review** first, then offer **Full Report**.

The review process cross-checks four sources:
- **Dev logs** (`docs/dep/dev-*.md`) — what was claimed as done
- **Git history** (`git log --oneline --since=<date>`) — what was actually committed
- **Main docs** (`docs/main/`) — what the architecture/spec says should exist
- **Actual code** — what is really there

## Quick Review (default)

Always start here. Read dev logs since the last review (or last 3 days if no prior review). Run `git log --oneline --since=<last review date>` to cross-check dev log claims against actual commits. Then output 3-5 bullet points directly in the response — no file is generated.

Format:

```
## Quick Review

- [finding 1: what was checked, what was found — reference dev log round if relevant]
- [finding 2: issue or gap identified vs dev log claims]
- [finding 3: risk or concern — dev log items still open, blockers, etc.]
- [summary verdict: OK / needs attention / blocking]

需要我生成完整的审查报告到 `docs/dep/` 吗？
```

Quick Review covers:
- Critical issues (bugs, security, data loss)
- Dev log claims not backed by git commits
- Missing pieces vs dev log claims and main docs
- Dev log items still marked as open/blocked
- Obvious deviations from conventions
- A one-line verdict

## Full Report (on demand)

Only generate when the user confirms they want it (after being prompted, or if they explicitly ask for "完整报告", "生成报告", "full report", "write report").

### Naming convention

See `references/doc-structure.md`. Reports follow `docs/dep/review-<YYYYMMDD>-<NN>.md`.

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

## Dev Logs Reviewed

| Date | Round | Claim | Verified |
|------|-------|-------|----------|
| YYYY-MM-DD | R1 | [what dev log says was done] | ✅ / ⚠️ / ❌ — [evidence] |

## Findings

### Issues
<!-- Problems found: bugs, inconsistencies, missing pieces -->

| # | Severity | File/Area | Description | Status |
|---|----------|-----------|-------------|--------|
| 1 | high/medium/low | path:line | ... | open/fixed/deferred |

### Unimplemented / Incomplete
<!-- Features or behaviors mentioned in docs/spec/dev-log but not in code -->

| # | Reference | Description | Next step |
|---|-----------|-------------|-----------|
| 1 | dev-YYYYMMDD R2 / spec ref | ... | ... |

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
