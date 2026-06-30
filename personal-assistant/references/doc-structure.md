# Document structure

Authoritative reference for document paths, naming rules, lifecycle, TASK_STATE.md format, and DEVLOG storage rules.

## 目录

- [Directory tree](#directory-tree)
- [File reference](#file-reference)
- [Naming rules](#naming-rules)
- [DEVLOG storage](#devlog-storage)
- [DEVLOG legacy adoption](#devlog-legacy-adoption)
- [TASK_STATE.md - Interrupt checkpoint](#task_statemd---interrupt-checkpoint)
- [Format ownership](#format-ownership)

## Directory tree

```
<project-root>/
├── USAGE.md
└── docs/
    ├── main/
    │   ├── PROJECT_GUIDE.md
    │   ├── PROJECT_SPEC.md
    │   ├── CODE_STYLE.md
    │   ├── TEST_GUIDE.md
    │   └── memory/
    │       ├── MEMORY.md
    │       └── <type>-<topic>.md
    │
    ├── dep/
    │   ├── PLAN.md
    │   ├── plans/
    │   │   ├── ongoing/            # 当前正在执行或已接受的立即阻断修复
    │   │   │   ├── P0-fix-auth-race.md
    │   │   │   └── P1-user-auth.md
    │   │   ├── backlog/            # 已确认但未开始；非阻断技术债池在这里
    │   │   │   ├── P0-tech-debt.md
    │   │   │   └── P2-admin-panel.md
    │   │   ├── complete/           # 已完成并同步主文档的历史子计划
    │   │   │   └── P1-db-migration.md
    │   │   └── deferred/           # 明确延后，不进入当前计划周期
    │   │       └── P4-oauth-login.md
    │   ├── DEVLOG.md              # DEVLOG entrypoint, not the detailed log
    │   ├── devlog/
    │   │   ├── active/
    │   │   │   └── DEVLOG-R121-R160.md
    │   │   ├── archive/
    │   │   │   ├── DEVLOG-R001-R040.md
    │   │   │   ├── DEVLOG-R041-R080.md
    │   │   │   └── DEVLOG-R081-R120.md
    │   │   ├── summary/
    │   │   │   ├── SUMMARY-R001-R040.md
    │   │   │   └── SUMMARY-R041-R080.md
    │   │   └── INDEX.md
    │   ├── REVIEWS.md
    │   └── TASK_STATE.md
    │
    └── deploy/
        └── DEPLOY_GUIDE.md
```

`docs/dep/PLAN.md` links to sub-plans using paths relative to itself, such as `[P1-user-auth.md](plans/ongoing/P1-user-auth.md)`. The canonical filesystem path is always `docs/dep/plans/<lifecycle>/Pn-name.md`.

## File reference

### Root

| File | Writes | When | Format |
|------|--------|------|--------|
| `USAGE.md` | Bootstrap / Development | Bootstrap creates; Development updates when usage changes | Quick start, prerequisites, common commands, FAQ |

### docs/main/ - Blueprint

The four canonical main docs follow bundled templates:

| File | Template | Writes | When |
|------|----------|--------|------|
| `docs/main/PROJECT_GUIDE.md` | `templates/PROJECT_GUIDE.md.template` | Bootstrap / Development | Architecture, tech stack, modules, data flow, directory structure |
| `docs/main/PROJECT_SPEC.md` | `templates/PROJECT_SPEC.md.template` | Bootstrap / Development | Goals, feature scope, decisions, API/data contracts, non-functional requirements |
| `docs/main/CODE_STYLE.md` | `templates/CODE_STYLE.md.template` | Bootstrap / Development | Naming, format, comments, imports, errors, project conventions |
| `docs/main/TEST_GUIDE.md` | `templates/TEST_GUIDE.md.template` | Bootstrap / Development | Test framework, layout, commands, coverage, fixtures |
| `docs/main/memory/MEMORY.md` | Context update | When memory entries are added or removed | Memory index |
| `docs/main/memory/<type>-<topic>.md` | Development / Consultation | When durable decisions, preferences, or project facts emerge | Memory entry |

### docs/dep/ - Diary

| File | Writes | When | Lifecycle |
|------|--------|------|-----------|
| `docs/dep/PLAN.md` | Planning / Development / Review | When any sub-plan is active or queued | Dashboard only; stores pointers, not Phase details |
| `docs/dep/plans/<lifecycle>/P<phase>-<name>.md` | Planning / Development / Review | When a feature, refactor, P0 repair, or technical debt track is planned | Persistent design record; moved between lifecycle directories |
| `docs/dep/DEVLOG.md` | Development / Review | Bootstrap or first Development round; updated when batches rotate | Lightweight entrypoint to active batch, index, summaries, and archive |
| `docs/dep/devlog/active/DEVLOG-RXXX-RYYY.md` | Development | After each completed round | Exactly one active writable batch |
| `docs/dep/devlog/archive/DEVLOG-RXXX-RYYY.md` | Development / Review | When an active batch is sealed | Immutable original log evidence |
| `docs/dep/devlog/summary/SUMMARY-RXXX-RYYY.md` | Development / Review | Generated when a batch is sealed | Derived summary; archive is authoritative if conflicts exist |
| `docs/dep/devlog/INDEX.md` | Development / Review | One row per DEVLOG round | Searchable round index |
| `docs/dep/REVIEWS.md` | Review | Only after user confirms Full Report | Single append-only file |
| `docs/dep/TASK_STATE.md` | Development | Created at task start, updated at checkpoints, deleted at completion | Temporary interrupt checkpoint |

### docs/deploy/ - Deployment

| File | Writes | When |
|------|--------|------|
| `docs/deploy/DEPLOY_GUIDE.md` | Deployment / Development | Bootstrap creates placeholder; updated when deployment details change |

## Naming rules

| Pattern | Rule |
|---------|------|
| `USAGE.md` | Root level. Auto-generated at bootstrap when missing. |
| `docs/dep/PLAN.md` | Main dashboard. Contains active, queued, recently completed, and deferred pointers only. |
| `docs/dep/plans/ongoing/P<phase>-<name>.md` | Active work. Contains current execution and accepted immediate P0 blockers only. |
| `docs/dep/plans/backlog/P<phase>-<name>.md` | Confirmed but not started work. Sorted by `phase_index`, then `priority`. |
| `docs/dep/plans/backlog/P0-tech-debt.md` | Reserved rolling technical debt pool for non-blocking Review findings. It should not live in `ongoing/`. |
| `docs/dep/plans/complete/P<phase>-<name>.md` | Completed and synced sub-plan history. |
| `docs/dep/plans/deferred/P<phase>-<name>.md` | Explicitly deferred work outside the current planning cycle. |
| `docs/dep/DEVLOG.md` | DEVLOG entrypoint. Links to active batch, index, recent summaries, and archive ranges. |
| `docs/dep/devlog/active/DEVLOG-R001-R040.md` | Active DEVLOG batch. 40 global rounds per batch by default. |
| `docs/dep/devlog/archive/DEVLOG-R001-R040.md` | Sealed DEVLOG batch. Immutable after archive. |
| `docs/dep/devlog/summary/SUMMARY-R001-R040.md` | Summary for a sealed DEVLOG batch. |
| `docs/dep/devlog/INDEX.md` | Round index: round, date, sub-plan, phase, summary, files, batch path. |
| `docs/dep/REVIEWS.md` | Single append-only review report file. Each full review uses `## Review N [YYYY-MM-DD]`. |
| `docs/dep/TASK_STATE.md` | Temporary checkpoint. Exists only while a task is in progress. |
| `docs/deploy/DEPLOY_GUIDE.md` | Persistent deployment guide. |
| `docs/main/memory/<type>-<topic>.md` | `type` is `user`, `project`, `feedback`, or `reference`; `topic` is short kebab-case. |

### Sub-plan naming details

See `references/planning-protocol.md` for the full planning behavior. This file is authoritative for path and naming syntax:

```
docs/dep/plans/ongoing/P0-fix-auth-race.md
docs/dep/plans/backlog/P0-tech-debt.md
docs/dep/plans/ongoing/P1-user-auth.md
docs/dep/plans/backlog/P2-admin-panel.md
docs/dep/plans/complete/P1-db-migration.md
docs/dep/plans/deferred/P4-oauth-login.md
```

Rules:
- `P0` can be inserted at any time for blocking repairs. Blocking Review findings become independent P0 plans; non-blocking Review debt goes into the debt pool.
- Blocking Review findings get independent `P0-<desc>.md` files and move to `ongoing/` only when accepted for immediate execution.
- Non-blocking technical debt goes into `backlog/P0-tech-debt.md`.
- `P1+` numbers represent execution order, not importance.
- Existing numbers are not rewritten when a new plan is inserted.
- PLAN.md relative links may use `plans/ongoing/P1-user-auth.md`; all protocol text should treat `docs/dep/plans/<lifecycle>/P1-user-auth.md` as canonical.

### Lifecycle directory rules

| Directory | Required `status` | Meaning |
|-----------|-------------------|---------|
| `plans/ongoing/` | `in-progress` | Currently executing work, or immediate P0 repair accepted as the next blocking action |
| `plans/backlog/` | `planning` | Confirmed but not started plans, including the rolling `P0-tech-debt.md` pool |
| `plans/complete/` | `done` | Completed plans after tests, Review if applicable, DEVLOG, and main-doc sync |
| `plans/deferred/` | `deferred` | Explicitly postponed work that should not be scheduled in the current cycle |

The directory and frontmatter `status` must match. Tags classify subject matter; directories classify lifecycle. Do not create keyword directories such as `plans/auth/` or `plans/api/`.

## DEVLOG storage

DEVLOG uses an entrypoint, one active batch, immutable archives, batch summaries, and a searchable index.

```
- Entry point: docs/dep/DEVLOG.md
- One active file at a time: docs/dep/devlog/active/DEVLOG-RXXX-RYYY.md
- Each batch = 40 global rounds by default
- Sealed batches move to docs/dep/devlog/archive/
- Each sealed batch gets docs/dep/devlog/summary/SUMMARY-RXXX-RYYY.md
- Every round has one row in docs/dep/devlog/INDEX.md
- Round numbering is global and monotonic
```

### Global round counter

Read the last round number from `docs/dep/devlog/active/` to determine the next value. If no active DEVLOG file exists, inspect `docs/dep/devlog/archive/` for the highest archived round and create the next active range after it. If no active or archived round exists, create `docs/dep/devlog/active/DEVLOG-R001-R040.md` and start at R001.

## DEVLOG legacy adoption

When a project already has older DEVLOG files, archive them directly before writing any new round:

| Legacy path | Action |
|-------------|--------|
| `docs/dep/DEVLOG-RXXX-RYYY.md` | Move unchanged to `docs/dep/devlog/archive/DEVLOG-RXXX-RYYY.md` |
| old detailed `docs/dep/DEVLOG.md` | Move unchanged to `docs/dep/devlog/archive/DEVLOG-legacy.md`, then create the new lightweight entrypoint |
| other one-off detailed DEVLOG files in `docs/dep/` | Move unchanged to `docs/dep/devlog/archive/` with a clear legacy filename |

Rules:
- Do not split, merge, renumber, reformat, or edit legacy DEVLOG content.
- Do not rewrite historical batch files to fit the new format.
- Create `docs/dep/DEVLOG.md`, `docs/dep/devlog/INDEX.md`, and `docs/dep/devlog/active/` for new work after archiving legacy files.
- Backfill `INDEX.md` for legacy rounds only when it is cheap and reliable; otherwise link archived files from `DEVLOG.md` and leave indexing for later Review work.
- Legacy summaries are optional during adoption. The archive file remains authoritative.

### Layered reading

| Layer | When to read | How |
|-------|--------------|-----|
| `DEVLOG.md` | First stop for Development and Review | Find active batch and index |
| `devlog/INDEX.md` | Always before searching historical rounds | Locate round date, summary, files, and batch |
| Active batch | Development resume/write, recent Review | Last round for resume; scoped sections for Review |
| Summary files | Review and context loading | Read before archive originals |
| Archive batches | User requests specific rounds, audit evidence, or summary is insufficient | Read only relevant round sections |
| REVIEWS.md | Review mode | Last 3 reviews full; older reviews status line only |

## TASK_STATE.md - Interrupt checkpoint

TASK_STATE.md enables cross-session task resumption. It is not a design document and should be deleted when the task or Phase completes.

### Lifecycle

```
Task starts        -> Create TASK_STATE.md with status: in-progress
Task progresses    -> Update checklist and Working Context
Task interrupted   -> TASK_STATE.md persists
New session starts -> Development mode checks TASK_STATE.md first
Task completes     -> Consolidate into active DEVLOG batch + INDEX.md, delete TASK_STATE.md
```

### Format

```markdown
---
status: in-progress
created: YYYY-MM-DD HH:MM
updated: YYYY-MM-DD HH:MM
---

# Current Task

## Goal
[one-line description of what is being done]

## Progress
- [x] [completed step]
- [ ] [current/next step]

## Working Context
- **Files being edited**: [list of files]
- **Last command run**: [command] ([status])
- **Key decisions**: [decision + reference to docs/memory]
- **Blocker**: [description or "None"]

## Phase Context
- **Sub-plan**: `docs/dep/plans/ongoing/P1-user-auth.md`
- **Phase**: P2 - [phase name]
- **Input conditions**: [copied or summarized from sub-plan]
- **Completion criteria**: [copied or summarized from sub-plan]
- **Boundaries**: [copied or summarized from sub-plan]

## Resume From
[explicit instruction for the next session: what to do, where to start]
```

`Phase Context` is required only when a sub-plan is active.

### Multi-task support

If multiple tasks are interrupted simultaneously:

```markdown
## Task 1: [name]
status: in-progress
[checkpoint content]

## Task 2: [name]
status: blocked
[checkpoint content]
```

Priority is `in-progress` before `blocked`. Present both to the user and let them choose.

## Format ownership

To avoid duplication:

| Format or flow | Authoritative source |
|----------------|----------------------|
| Directory tree, file paths, naming, TASK_STATE.md, DEVLOG storage | `references/doc-structure.md` |
| PLAN.md dashboard structure | `templates/plan-dashboard.md.template` |
| Sub-plan structure and Phase-Gate flow | `references/planning-protocol.md` + `templates/sub-plan.md.template` |
| Main document structures | `templates/PROJECT_GUIDE.md.template`, `templates/PROJECT_SPEC.md.template`, `templates/CODE_STYLE.md.template`, `templates/TEST_GUIDE.md.template` |
| Review workflow and Review-to-plan sync | `references/review-protocol.md` |
