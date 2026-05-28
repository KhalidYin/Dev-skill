# Document structure

Authoritative reference for document paths, naming rules, lifecycle, TASK_STATE.md format, and DEVLOG batch rules.

## 目录

- [Directory tree](#directory-tree)
- [File reference](#file-reference)
- [Naming rules](#naming-rules)
- [DEVLOG round batches](#devlog-round-batches)
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
    │   │   ├── P0-tech-debt.md
    │   │   ├── P0-fix-auth-race.md
    │   │   ├── P1-user-auth.md
    │   │   └── P2-admin-panel.md
    │   ├── DEVLOG-R001-R040.md
    │   ├── DEVLOG-R041-R080.md
    │   ├── REVIEWS.md
    │   └── TASK_STATE.md
    │
    └── deploy/
        └── DEPLOY_GUIDE.md
```

`docs/dep/PLAN.md` links to sub-plans using paths relative to itself, such as `[P1-user-auth.md](plans/P1-user-auth.md)`. The canonical filesystem path is always `docs/dep/plans/Pn-name.md`.

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
| `docs/dep/plans/P<phase>-<name>.md` | Planning / Development / Review | When a feature, refactor, P0 repair, or technical debt track is planned | Persistent design record; never deleted on completion |
| `docs/dep/DEVLOG-RXXX-RXXX.md` | Development | After each completed round | Active batch is append-only; sealed batches are read-only |
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
| `docs/dep/plans/P<phase>-<name>.md` | Phase-indexed sub-plan. `P0` is pre-stage repair/debt; `P1+` are execution order. `<name>` is kebab-case. |
| `docs/dep/plans/P0-tech-debt.md` | Reserved single technical debt track for non-blocking Review findings. |
| `docs/dep/DEVLOG-R001-R040.md` | DEVLOG batch file. 40 global rounds per batch. Naming continues `DEVLOG-R041-R080.md`, etc. |
| `docs/dep/REVIEWS.md` | Single append-only review report file. Each full review uses `## Review N [YYYY-MM-DD]`. |
| `docs/dep/TASK_STATE.md` | Temporary checkpoint. Exists only while a task is in progress. |
| `docs/deploy/DEPLOY_GUIDE.md` | Persistent deployment guide. |
| `docs/main/memory/<type>-<topic>.md` | `type` is `user`, `project`, `feedback`, or `reference`; `topic` is short kebab-case. |

### Sub-plan naming details

See `references/planning-protocol.md` for the full planning behavior. This file is authoritative for path and naming syntax:

```
docs/dep/plans/P0-fix-auth-race.md
docs/dep/plans/P0-tech-debt.md
docs/dep/plans/P1-user-auth.md
docs/dep/plans/P2-admin-panel.md
```

Rules:
- `P0` can be inserted at any time for blocking repairs or Review-discovered debt.
- Blocking Review findings get independent `P0-<desc>.md` files.
- Non-blocking technical debt goes into `P0-tech-debt.md`.
- `P1+` numbers represent execution order, not importance.
- Existing numbers are not rewritten when a new plan is inserted.
- PLAN.md relative links may use `plans/P1-user-auth.md`; all protocol text should treat `docs/dep/plans/P1-user-auth.md` as canonical.

## DEVLOG round batches

DEVLOG uses 40-round batches to control file size. Each file holds exactly one batch.

```
- One active file at a time: docs/dep/DEVLOG-RXXX-RXXX.md
- Each batch = 40 global rounds
- Batch 1: DEVLOG-R001-R040.md
- Batch 2: DEVLOG-R041-R080.md
- Batch N: DEVLOG-R((N-1)*40+1)-R(N*40).md
- When the active file reaches 40 rounds, seal it and create the next batch
- Sealed batches are read-only
- Round numbering is global and monotonic
```

### Global round counter

Read the last round number from the active batch to determine the next value. If no DEVLOG file exists, start at R001.

### Layered reading

| Layer | When to read | How |
|-------|--------------|-----|
| Active batch | Always in Development and Review modes | Last round for resume; full read for recent Review |
| Previous batch | Resume references earlier round; Review crosses batch boundary | Read relevant sections or full batch if needed |
| Older batches | User specifies older round range or date | Read only relevant date/round sections |
| REVIEWS.md | Review mode | Last 3 reviews full; older reviews status line only |

## TASK_STATE.md - Interrupt checkpoint

TASK_STATE.md enables cross-session task resumption. It is not a design document and should be deleted when the task or Phase completes.

### Lifecycle

```
Task starts        -> Create TASK_STATE.md with status: in-progress
Task progresses    -> Update checklist and Working Context
Task interrupted   -> TASK_STATE.md persists
New session starts -> Development mode checks TASK_STATE.md first
Task completes     -> Consolidate into DEVLOG batch, delete TASK_STATE.md
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
- **Sub-plan**: `docs/dep/plans/P1-user-auth.md`
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
| Directory tree, file paths, naming, TASK_STATE.md, DEVLOG batches | `references/doc-structure.md` |
| PLAN.md dashboard structure | `templates/plan-dashboard.md.template` |
| Sub-plan structure and Phase-Gate flow | `references/planning-protocol.md` + `templates/sub-plan.md.template` |
| Main document structures | `templates/PROJECT_GUIDE.md.template`, `templates/PROJECT_SPEC.md.template`, `templates/CODE_STYLE.md.template`, `templates/TEST_GUIDE.md.template` |
| Review workflow and Review-to-plan sync | `references/review-protocol.md` |
