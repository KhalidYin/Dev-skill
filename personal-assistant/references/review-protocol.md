# Review protocol

When the user issues an audit/review/inspection command, follow a two-tier approach: **Quick Review** first, then offer **Full Report**.

The review process cross-checks four sources:
- **Dev log** (`docs/dep/DEVLOG.md` + archives) — what was claimed as done
- **Git history** (`git log --oneline --since=<date>`) — what was actually committed
- **Main docs** (`docs/main/`) — what the architecture/spec says should exist
- **Actual code** — what is really there

## Scope determination

Review scope is determined by the user's request. If unspecified, default to: **all entries since the last review**.

| User says | Scope |
|-----------|-------|
| "review the codebase" | All entries since last review (or last 3 days if no prior review) |
| "review last week" | DEVLOG entries from the past 7 days, may cross month boundaries |
| "review the auth module" | Entries that touch auth-related files, regardless of date |
| "review everything" | All DEVLOG entries + archives |

When scope crosses month boundaries, read both `DEVLOG.md` and the relevant `DEVLOG-YYYY-MM.md` archives — only the date sections within scope.

## Quick Review (default)

Always start here. Read dev log entries within scope. Run `git log --oneline --since=<scope start date>` to cross-check claims against actual commits. Output 3-5 bullet points directly in the response — no file is written.

Format:

```
## Quick Review

- [finding 1: what was checked, what was found — reference dev log round if relevant]
- [finding 2: issue or gap identified vs dev log claims]
- [finding 3: risk or concern — dev log items still open, blockers, etc.]
- [summary verdict: OK / needs attention / blocking]

需要我生成完整的审查报告到 `docs/dep/REVIEWS.md` 吗？
```

Quick Review covers:
- Critical issues (bugs, security, data loss)
- Dev log claims not backed by git commits
- Missing pieces vs dev log claims and main docs
- Dev log items still marked as open/blocked
- Obvious deviations from conventions
- A one-line verdict

## Full Report (on demand)

Only generate when the user confirms (after Quick Review prompt) or explicitly asks for "完整报告", "生成报告", "full report".

### Format

`REVIEWS.md` is a **single rolling file**, append-only. Each review is a dated section.

Only include sections that have content — skip empty sections entirely, do not generate empty tables.

```markdown
# Review Reports

---

## 2026-05-04 Round 1

### Scope
<!-- What was reviewed: files, features, modules, time range -->

### Dev Logs Reviewed

| Date | Round | Claim | Verified |
|------|-------|-------|----------|
| 2026-05-04 | R1 | [what dev log says was done] | ✅ / ⚠️ / ❌ — [evidence] |

### Findings

#### Issues
<!-- Only include if issues found -->

| # | Severity | File/Area | Description | Status |
|---|----------|-----------|-------------|--------|
| 1 | high/medium/low | path:line | ... | open/fixed/deferred |

#### Unimplemented / Incomplete
<!-- Only include if unimplemented items found -->

| # | Reference | Description | Next step |
|---|-----------|-------------|-----------|
| 1 | DEVLOG 2026-05-03 R2 / spec ref | ... | ... |

#### Deviations
<!-- Only include if deviations found -->

| # | Expected | Actual | Impact |
|---|----------|--------|--------|
| 1 | ... | ... | ... |

### Next Actions
<!-- Always include — concrete, prioritized -->

1. ...

### Status: in-progress / resolved / deferred

---

## 2026-05-03 Round 1
- ...
```

### Rules

- **Append-only** — never delete or edit past reviews
- **Only include sections with content** — no empty tables or placeholder sections
- **Status tracking** — `in-progress` (issues open), `resolved` (all closed), `deferred` (some deferred)
- **Status is historical** — do not modify past reviews' status. If previously open issues are now resolved, note the resolution in the new review's findings
- Link to related prior reviews by date reference

### Layered reading for REVIEWS.md

To minimize token consumption when reading past reviews:

| Reviews to read | How |
|----------------|-----|
| Last 3 reviews | Full read — complete sections |
| Older reviews | Status line only — read just the `### Status:` line |
| User requests specific review | Full read of that review section |

## When NOT to generate

- Simple code change or bug fix (not a review)
- One-line answer about code behavior
- Purely writing new code (no review implied)
