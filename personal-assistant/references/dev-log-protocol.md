# Dev Log Protocol

Every non-trivial development action MUST be recorded in a DEVLOG batch file under `docs/dep/`. This log is the primary source the review process uses to cross-check claims against code and docs.

## Round batch system

DEVLOG uses **40-round batches** to control file size. Each file holds exactly one batch.

- **Active batch**: `DEVLOG-RXXX-RXXX.md` — current file, append-only
- **Sealed batches**: `DEVLOG-RXXX-RXXX.md` — read-only, never modified
- **Batch size**: 40 global rounds per file
- **Round numbering**: Global, monotonic (R001, R002, ... RXXX)

```
docs/dep/
├── DEVLOG-R001-R040.md     # Global rounds R001–R040
├── DEVLOG-R041-R080.md     # Global rounds R041–R080
└── DEVLOG-R081-R120.md     # Global rounds R081–R120 (active)
```

### Global round counter

Each round gets a unique global identifier. When writing a new round:

```
1. Find the active batch file (highest round range)
2. Read the last round number in that file
3. Next round = last round + 1
4. If the active batch has 40 rounds → seal it, create next batch, start with R((N-1)*40+1)
5. If no DEVLOG files exist → start with R001
```

## Format

Entries use date headers with global round numbers. All DEVLOG batch files use the same format:

```markdown
# Dev Log — R001–R040

---

## 2026-05-04

### R007 [14:30] [user-auth] P2: 实现注册 API

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

### R008 [16:45] [user-auth] P2: 实现登录 API

#### Done
- ...

## 2026-05-03

### R006 [10:00]
- ...
```

**Key**: rounds use global numbering `R001, R002, ...` — not daily restart.

## Rules

- **Append-only** — never delete or edit past entries; always append new ones
- **Batch file title** — `# Dev Log — R001–R040` reflects the round range in that file
- **Date header** — `## YYYY-MM-DD`, one per day. Create only when work happens that day
- **Round header** — `### RXXX [HH:MM]`, global monotonic number (R001, R002, ...)
- **Sub-plan and Phase annotation** — 当存在活跃子计划时，轮次标题必须同时标注子计划和 Phase：`### RXXX [HH:MM] [sub-plan] PX: [简短描述]`。子计划名与 `plans/<name>.md` 文件名一致（不含扩展名）。无子计划时省略子计划标注，有子计划但单 Phase 时省略 Phase 标注
- **Separator** — use `---` between rounds within the same date section
- **Be concrete** — "Fixed login timeout" not "Worked on auth"
- **Files Changed / Commits** — list every file touched with commit hash. If not yet committed, write "(uncommitted)"
- **Next** — always end with clear next steps; if fully done, write "Done — no next steps"
- **Open issues persist** — if an issue from a prior round is still unresolved, mention it again in the current round

## Layered reading

| Scenario | What to read |
|----------|-------------|
| Development mode (task resume check) | Active batch: last round only |
| Development mode (write new round) | Active batch: append new round |
| Review (recent, within same batch) | Active batch: full read |
| Review (cross-batch range) | Active batch + relevant sealed batch: read only the specified round range |
| User asks about specific round | That round's section in the appropriate batch file |

### How to find the right batch

```
1. Determine the round number needed (e.g., R052)
2. Batch = DEVLOG-R041-R080.md (since 41 ≤ 52 ≤ 80)
3. Formula: batch N contains rounds R((N-1)*40+1) to R(N*40)
4. Read only the relevant sections from that file
```

## When to write

**Mandatory** — after each completed round in Development mode:
- A feature implementation is done (even partial)
- A bug is fixed
- A refactor is completed
- An investigation / diagnosis was performed (even if unresolved)

Write BEFORE responding to the user. The dev log entry is part of the task output.

## Quick Fix entry format

Quick Fix changes use a one-line entry instead of a full round. Append under the current date header in the active batch file:

```markdown
## 2026-05-04

### R007 [14:30] [user-auth] P2: QF: Fixed login timeout in src/auth.py:42 — `abc1234`
```

Format: `### RXXX [HH:MM] [<sub-plan>] [PX:] QF: [one-line description] — [commit hash or (uncommitted)]`

子计划标注 `[<sub-plan>]` 和 Phase 前缀 `PX:` 在存在活跃子计划时为必填，否则省略。

QF entries use the global round counter just like full rounds — this ensures no gaps in the round sequence.

If no date header exists for today, create it first. If a full round already exists for today, append the QF entry after the last round.

## When NOT to write

- Consultation mode (no changes made)
- Trivial edits (typo fix in a comment, whitespace)
- The act of writing docs or dev logs themselves
