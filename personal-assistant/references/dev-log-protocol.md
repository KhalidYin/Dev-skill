# Dev Log Protocol

Every non-trivial development action MUST be recorded in the active DEVLOG batch. DEVLOG is the audit trail used by Review to cross-check claims against code, docs, and git history.

## 目录

- [Storage layout](#storage-layout)
- [Legacy adoption](#legacy-adoption)
- [Round batch system](#round-batch-system)
- [DEVLOG.md entrypoint](#devlogmd-entrypoint)
- [INDEX.md format](#indexmd-format)
- [Batch format](#batch-format)
- [Summary format](#summary-format)
- [Rules](#rules)
- [Layered reading](#layered-reading)
- [When to write](#when-to-write)
- [Quick Fix entry format](#quick-fix-entry-format)
- [When NOT to write](#when-not-to-write)

## Storage layout

DEVLOG uses an entrypoint, active batch, immutable archive, generated summaries, and a searchable index:

```
docs/dep/
├── DEVLOG.md
└── devlog/
    ├── active/
    │   └── DEVLOG-R121-R160.md
    ├── archive/
    │   ├── DEVLOG-R001-R040.md
    │   ├── DEVLOG-R041-R080.md
    │   └── DEVLOG-R081-R120.md
    ├── summary/
    │   ├── SUMMARY-R001-R040.md
    │   ├── SUMMARY-R041-R080.md
    │   └── SUMMARY-R081-R120.md
    └── INDEX.md
```

Purpose:
- `DEVLOG.md` is the human entrypoint. It points to the active batch, index, summaries, and recent archive ranges.
- `devlog/active/` contains exactly one writable active batch.
- `devlog/archive/` contains sealed batch files. These are immutable.
- `devlog/summary/` contains generated batch summaries for fast Review and context loading.
- `devlog/INDEX.md` maps each round to date, sub-plan, files, summary, and batch path.

## Legacy adoption

Some projects may already contain earlier DEVLOG files before this storage layout is introduced. Treat those files as historical evidence and archive them directly.

Legacy files:
- `docs/dep/DEVLOG-RXXX-RYYY.md` at the root of `docs/dep/`
- an old detailed `docs/dep/DEVLOG.md` that is not a lightweight entrypoint
- any earlier one-off detailed DEVLOG file in `docs/dep/` that was used as the primary development log

Adoption rules:
1. Create `docs/dep/devlog/archive/`, `docs/dep/devlog/active/`, `docs/dep/devlog/summary/`, and `docs/dep/devlog/INDEX.md` if missing.
2. Move legacy root batch files such as `docs/dep/DEVLOG-R001-R040.md` directly into `docs/dep/devlog/archive/` with the same filename.
3. If a legacy detailed `docs/dep/DEVLOG.md` exists, move it to `docs/dep/devlog/archive/DEVLOG-legacy.md` before creating the new lightweight `docs/dep/DEVLOG.md` entrypoint.
4. Do not split, merge, renumber, reformat, or edit legacy DEVLOG content during adoption.
5. Backfill `devlog/INDEX.md` from legacy archive files only when it is cheap and reliable. If not, add archive links in `DEVLOG.md` and leave detailed indexing for future review work.
6. The next active batch starts after the highest round number found in `devlog/archive/` and `devlog/active/`. If the highest legacy round is R065, create `active/DEVLOG-R066-R105.md`; do not restart at R001.
7. Legacy archive summaries are optional during adoption. Generate `summary/SUMMARY-RXXX-RYYY.md` later when a Review needs fast context or when the batch is naturally touched for sealing.

The goal is preservation, not migration cleanup. Old logs are archived as-is; all new work uses the new active/index/entrypoint structure.

## Round batch system

DEVLOG uses 40-round batches by default. Each batch holds one contiguous global range.

- **Active batch**: `docs/dep/devlog/active/DEVLOG-RXXX-RYYY.md`
- **Archived batches**: `docs/dep/devlog/archive/DEVLOG-RXXX-RYYY.md`
- **Batch summaries**: `docs/dep/devlog/summary/SUMMARY-RXXX-RYYY.md`
- **Batch size**: 40 global rounds per file by default
- **Round numbering**: global and monotonic (`R001`, `R002`, ... `RXXX`)

### Global round counter

When writing a new round:

```
1. Run Legacy adoption first if old root DEVLOG files exist.
2. Read docs/dep/devlog/active/ to find the active batch.
3. Read the last round number in the active batch.
4. If no active batch exists, inspect devlog/archive/ for the highest archived round and create the next active range after it.
5. If no archive or active round exists, create DEVLOG-R001-R040.md and start with R001.
6. Next round = last round + 1.
7. If the active batch already has 40 rounds:
   - move it to devlog/archive/
   - generate or update devlog/summary/SUMMARY-RXXX-RYYY.md
   - update devlog/INDEX.md
   - create the next active batch in devlog/active/
```

Do not renumber old rounds. Do not change sealed archive files.

## DEVLOG.md entrypoint

`docs/dep/DEVLOG.md` is not the detailed log. It is a lightweight entrypoint.

```markdown
# Dev Log

## Active

- Current batch: [DEVLOG-R121-R160.md](devlog/active/DEVLOG-R121-R160.md)
- Index: [devlog/INDEX.md](devlog/INDEX.md)

## Recent summaries

- [SUMMARY-R081-R120.md](devlog/summary/SUMMARY-R081-R120.md)
- [SUMMARY-R041-R080.md](devlog/summary/SUMMARY-R041-R080.md)

## Archive

- R001-R040: [log](devlog/archive/DEVLOG-R001-R040.md), [summary](devlog/summary/SUMMARY-R001-R040.md)
- R041-R080: [log](devlog/archive/DEVLOG-R041-R080.md), [summary](devlog/summary/SUMMARY-R041-R080.md)
```

Update `DEVLOG.md` whenever a batch is sealed or a new active batch is created.

## INDEX.md format

`docs/dep/devlog/INDEX.md` is append-only except for metadata refresh when paths move during batch sealing.

```markdown
# Dev Log Index

| Round | Date | Time | Sub-plan | Phase | Summary | Files | Batch |
|-------|------|------|----------|-------|---------|-------|-------|
| R121 | 2026-06-29 | 14:30 | P1-user-auth | P2 | Implement register API | `src/auth.py`, `tests/test_auth.py` | active/DEVLOG-R121-R160.md |
| R080 | 2026-06-20 | 16:10 | - | - | Fix config timeout | `config.py` | archive/DEVLOG-R041-R080.md |
```

Rules:
- Add one row for every full round and every Quick Fix round.
- Keep summaries short enough to scan.
- Use sub-plan stem without extension, such as `P1-user-auth`.
- When sealing a batch, update that batch's rows from `active/...` to `archive/...`.

## Batch format

Entries use date headers with global round numbers. Active and archived batch files use the same format:

```markdown
# Dev Log — R121-R160

---

## 2026-06-29

### R121 [14:30] [P1-user-auth] P2: 实现注册 API

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
```

## Summary format

Each archived batch should have one summary file:

```markdown
# Summary — R081-R120

## Scope

- Dates: YYYY-MM-DD to YYYY-MM-DD
- Main sub-plans: P1-user-auth, P2-admin-panel
- Archive: [DEVLOG-R081-R120.md](../archive/DEVLOG-R081-R120.md)

## Completed

- [high-value completed work, grouped by sub-plan or module]

## Decisions

- [decision] — source rounds: R087, R092

## Open Issues

- [issue] — source round: R099 — status: open/deferred/resolved

## Files / Areas Touched

- `src/auth/` — R081, R083, R087
- `docs/main/PROJECT_SPEC.md` — R090

## Review Notes

- [anything future Review should check first]
```

Summaries are derived artifacts. If a summary conflicts with an archive log, the archive log wins.

## Rules

- **Append-only active batch** — append new rounds only.
- **Immutable archive** — after a batch moves to `devlog/archive/`, do not edit it.
- **Index update** — every new round must add one row to `devlog/INDEX.md`.
- **Summary on seal** — every sealed batch must get or refresh its `summary/SUMMARY-RXXX-RYYY.md`.
- **Date header** — `## YYYY-MM-DD`, one per day. Create only when work happens that day.
- **Round header** — `### RXXX [HH:MM]`, global monotonic number.
- **Sub-plan and Phase annotation** — when an active sub-plan exists, annotate the round title: `### RXXX [HH:MM] [P1-user-auth] P2: [short description]`. The sub-plan name is the stem of `docs/dep/plans/<lifecycle>/P<phase>-<name>.md`, usually from `plans/ongoing/`.
- **Separator** — use `---` between rounds within the same date section.
- **Be concrete** — write "Fixed login timeout", not "Worked on auth".
- **Files Changed / Commits** — list every file touched with commit hash. If not committed, write `(uncommitted)`.
- **Next** — always end with clear next steps; if complete, write `Done — no next steps`.
- **Open issues persist** — if an earlier issue remains unresolved, mention it again in the current round.

## Layered reading

Read the smallest layer that can answer the question.

| Scenario | What to read |
|----------|--------------|
| Development resume check | `DEVLOG.md`, then active batch last round only |
| Development write new round | Active batch + `devlog/INDEX.md` |
| Review default / recent | `devlog/INDEX.md`, active batch, relevant summaries |
| Review cross-batch range | `devlog/INDEX.md` + summaries first; open archive sections only for rounds in scope |
| User asks about specific round | `devlog/INDEX.md`, then that exact round in active/archive |
| Audit evidence needed | Archive batch original sections, never summary alone |
| Project memory / context loading | Summary files before archive files |

### How to find a round

```
1. Look up the round in docs/dep/devlog/INDEX.md.
2. Read the Batch column.
3. If Batch starts with active/, read docs/dep/devlog/active/<file>.
4. If Batch starts with archive/, read docs/dep/devlog/archive/<file>.
5. Read only the requested round section unless broader context is required.
```

## When to write

Mandatory after each completed round in Development mode:
- A feature implementation is done, even partial.
- A bug is fixed.
- A refactor is completed.
- An investigation or diagnosis was performed, even if unresolved.

Write the active batch entry and `devlog/INDEX.md` row before responding to the user.

## Quick Fix entry format

Quick Fix changes use a one-line entry instead of a full round. Append under the current date header in the active batch and add one row to `devlog/INDEX.md`.

```markdown
## 2026-06-29

### R121 [14:30] [P1-user-auth] P2: QF: Fixed login timeout in src/auth.py:42 — `abc1234`
```

Format: `### RXXX [HH:MM] [<sub-plan>] [PX:] QF: [one-line description] — [commit hash or (uncommitted)]`

Sub-plan annotation and Phase prefix are required when an active sub-plan exists; otherwise omit them.

QF entries use the global round counter just like full rounds.

## When NOT to write

- Consultation mode with no changes made.
- Trivial edits such as comment typo or whitespace.
- The act of writing docs or dev logs themselves.
