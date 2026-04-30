# Dev Log Protocol

Every non-trivial development action MUST be recorded in a daily dev log under `docs/dep/`. This log is the primary source the review process uses to cross-check claims against code and docs.

## File naming

See `references/doc-structure.md`. One file per day at `docs/dep/dev-<YYYYMMDD>.md`. Within a single file, append rounds using `---` as separator.

## When to write

**Mandatory** — after each completed round of work in Development mode:
- A feature implementation is done (even partial)
- A bug is fixed
- A refactor is completed
- An investigation / diagnosis was performed (even if unresolved)

Write BEFORE responding to the user. The dev log entry is part of the task output.

## Format

```markdown
---
date: YYYY-MM-DD
project: <project name>
---

# Dev Log — YYYY-MM-DD

---

## Round N [HH:MM]

### Done
- [what was accomplished — concrete and verifiable]

### Issues / Blockers
- [problems encountered, unresolved items, blockers]
- (write "None" if nothing)

### Next
1. [immediate next step]
2. [follow-up task]

### Files Changed / Commits
- `path/to/file.py` (added/modified/removed, +N lines) — `abc1234`
```

### Rules

- **One file per day**, multiple rounds within the file
- **Round numbers** restart at 1 for each new day
- **Use `---`** to separate rounds within the same file
- **Be concrete** — "Fixed login timeout" not "Worked on auth"
- **Files Changed / Commits** — list every file touched, with brief note on what changed, and the commit hash. If not yet committed, write "(uncommitted)"
- **Next** — always end with clear next steps; if fully done, write "Done — no next steps"
- **Issues remain open** — if an issue from a prior round is still unresolved, mention it again in the current round

## When NOT to write

Skip dev log for:
- Consultation mode (no changes made)
- Trivial edits (typo fix in a comment, whitespace)
- The act of writing docs or dev logs themselves
