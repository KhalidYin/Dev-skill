# Dev Log Protocol

Every non-trivial development action MUST be recorded in `docs/dep/DEVLOG.md`. This log is the primary source the review process uses to cross-check claims against code and docs.

## Monthly rotation

DEVLOG.md uses monthly rotation to prevent content bloat:

- **Current month**: `DEVLOG.md` — active, append-only
- **Previous months**: `DEVLOG-YYYY-MM.md` — read-only archives, created by rotation
- **Rotation trigger**: When a new month begins and the first entry is written, rename the old `DEVLOG.md` to `DEVLOG-YYYY-MM.md`
- **Archives are immutable** — never edit or delete past month files

## Format

Entries are organized by date, rounds by time. All DEVLOG files (current and archives) use the same format:

```markdown
# Dev Log

---

## 2026-05-04

### Round 1 [14:30]

#### Done
- [what was accomplished — concrete and verifiable]

#### Issues / Blockers
- [problems encountered, unresolved items]
- (write "None" if nothing)

#### Next
1. [immediate next step]
2. [follow-up task]

#### Files Changed / Commits
- `path/to/file.py` (added/modified/removed, +N lines) — `abc1234`

---

### Round 2 [16:45]

#### Done
- ...

## 2026-05-03

### Round 1 [10:00]
- ...
```

## Rules

- **Append-only** — never delete or edit past entries; always append new ones
- **Date header** — `## YYYY-MM-DD`, one per day. Create only when work happens that day
- **Round header** — `### Round N [HH:MM]`, sequential within each day, starting at 1
- **Separator** — use `---` between rounds within the same date section
- **Be concrete** — "Fixed login timeout" not "Worked on auth"
- **Files Changed / Commits** — list every file touched with commit hash. If not yet committed, write "(uncommitted)"
- **Next** — always end with clear next steps; if fully done, write "Done — no next steps"
- **Open issues persist** — if an issue from a prior round is still unresolved, mention it again in the current round

## Layered reading

To minimize token consumption, read DEVLOG files selectively:

| Scenario | What to read |
|----------|-------------|
| Development mode (task resume check) | DEVLOG.md: last date section only |
| Development mode (write new round) | DEVLOG.md: append to current date or create new date header |
| Review (within current month) | DEVLOG.md: full read |
| Review (cross-month range) | DEVLOG.md + relevant DEVLOG-YYYY-MM.md: read only the specified date range |
| User asks about specific date | That date's section only, in the appropriate file |

### How to find the right file

```
1. Is the date in the current month? → Read DEVLOG.md
2. Is the date in a past month?      → Read DEVLOG-YYYY-MM.md for that month
3. Unclear which month?              → Check file listing in docs/dep/
```

## When to write

**Mandatory** — after each completed round in Development mode:
- A feature implementation is done (even partial)
- A bug is fixed
- A refactor is completed
- An investigation / diagnosis was performed (even if unresolved)

Write BEFORE responding to the user. The dev log entry is part of the task output.

## Quick Fix entry format

Quick Fix changes use a one-line entry instead of a full round. Append under the current date header:

```markdown
## 2026-05-04

### QF [14:30] — Fixed login timeout in src/auth.py:42 — `abc1234`
```

Format: `### QF [HH:MM] — [one-line description] — [commit hash or (uncommitted)]`

If no date header exists for today, create it first. If a full round already exists for today, append the QF entry after the last round.

## When NOT to write

- Consultation mode (no changes made)
- Trivial edits (typo fix in a comment, whitespace)
- The act of writing docs or dev logs themselves
