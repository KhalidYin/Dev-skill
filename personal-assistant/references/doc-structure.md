# Document structure

Authoritative reference for all document paths and naming conventions.

## Directory tree

```
<project-root>/
├── USAGE.md                        # Quick start, prerequisites, common commands

└── docs/
    ├── main/                       # Blueprint — describes "what it IS"
    │   ├── PROJECT_GUIDE.md        # Architecture, module responsibilities, data flow
    │   ├── PROJECT_SPEC.md         # Technical scope, design decisions, feature boundaries
    │   ├── CODE_STYLE.md           # Naming, formatting, style conventions
    │   ├── TEST_GUIDE.md           # Test layout, regression coverage, entry points
    │   └── memory/                 # Cross-platform project memory (see context-memory.md)
    │       ├── MEMORY.md           # Memory index (always read first)
    │       └── <type>-<topic>.md   # Memory entries
    │
    ├── dep/                        # Diary — records "what was DONE"
    │   ├── DEVLOG-R001-R040.md     # Current batch (active, append-only, up to 40 rounds)
    │   ├── DEVLOG-R041-R080.md     # Completed batches (read-only archives)
    │   ├── REVIEWS.md              # Review reports (single file, append-only)
    │   ├── PLAN.md                 # Living project plan (optional)
    │   └── TASK_STATE.md           # Interrupt checkpoint (exists only when task is in-progress)
    │
    └── deploy/                     # Deployment — describes "HOW to deploy"
        └── DEPLOY_GUIDE.md        # Environments, steps, config, rollback
```

## File reference

### USAGE.md

| Writes | When | Format |
|--------|------|--------|
| Bootstrap / Development | Bootstrap auto-generates; dev mode updates as project evolves | Quick start, prerequisites, common commands, FAQ |

### docs/main/ — Blueprint

| File | Writes | When |
|------|--------|------|
| `PROJECT_GUIDE.md` | Bootstrap / Development | Bootstrap auto-generates; dev mode updates when architecture changes |
| `PROJECT_SPEC.md` | Bootstrap / Development | Bootstrap generates TBD placeholder; fills in over time |
| `CODE_STYLE.md` | Bootstrap / Development | Bootstrap generates TBD placeholder; fills in as conventions emerge |
| `TEST_GUIDE.md` | Bootstrap / Development | Bootstrap generates TBD placeholder; updates when test layout changes |
| `memory/MEMORY.md` | Bootstrap / Context update | Bootstrap creates empty; updated when a memory file is added/removed |
| `memory/<type>-<topic>.md` | Development / Consultation | When decisions, preferences, or project facts emerge |

### docs/dep/ — Diary

| File | Writes | When | Lifecycle |
|------|--------|------|-----------|
| `DEVLOG-RXXX-RXXX.md` | Development (mandatory) | After each completed round; append-only | Active until 40 rounds filled, then sealed |
| `REVIEWS.md` | Review (on demand) | Only after user confirms Full Report; append-only | Permanent, no rotation |
| `PLAN.md` | Development (optional) | When a multi-step plan is needed | Overwritten when plan evolves |
| `TASK_STATE.md` | Development | Created when task starts; updated at checkpoints; deleted when task completes | Exists only during active work |

### docs/deploy/ — Deployment

| File | Writes | When |
|------|--------|------|
| `DEPLOY_GUIDE.md` | Deployment / Development | Bootstrap generates TBD placeholder; filled in when deploying or when deployment-relevant code changes |

## Naming rules

| Pattern | Rule |
|---------|------|
| `USAGE.md` | Root level. Auto-generated at bootstrap. |
| `DEVLOG-R001-R040.md` | Round batch file. 40 rounds per batch. Global round numbering (R001, R002, ...). Naming: `DEVLOG-R001-R040.md`, `DEVLOG-R041-R080.md`, etc. |
| `REVIEWS.md` | Single file, append-only. Each entry: `## Review N [YYYY-MM-DD]` header. |
| `PLAN.md` | Living document, overwritten when plan evolves. |
| `TASK_STATE.md` | Checkpoint file. Exists only when a task is in-progress. Deleted on task completion. |
| `DEPLOY_GUIDE.md` | Persistent deployment guide. |
| `memory/<type>-<topic>.md` | `type` = `user` / `project` / `feedback` / `reference`. `topic` = short kebab-case. |

## DEVLOG round batches

DEVLOG uses 40-round batches to control file size. Each file holds exactly one batch.

### Batch rules

```
- One active file at a time: DEVLOG-RXXX-RXXX.md
- Each batch = 40 global rounds
- Batch 1: DEVLOG-R001-R040.md (global rounds R001–R040)
- Batch 2: DEVLOG-R041-R080.md (global rounds R041–R080)
- Batch N: DEVLOG-R((N-1)*40+1)-R(N*40).md
- When the active file reaches 40 rounds → seal it, create next batch file
- Sealed batches are read-only — never modify past batch files
- Round numbering is global and monotonic across batches
```

### Global round counter

Each round has a unique global identifier `RXXX` (e.g., R001, R042, R103). The counter is maintained by the active DEVLOG file:

```
Read the last round number from the active batch to determine the next value.
If no DEVLOG file exists, start at R001.
```

### Layered reading

To minimize token consumption, read DEVLOG files selectively:

| Layer | When to read | How |
|-------|-------------|-----|
| Active batch | Always in Development and Review modes | Full read |
| Previous batch (1 back) | Task resume references earlier round; review covers recent range | Full read |
| Older batches | User specifies older round range or date | Read only the relevant date sections |
| REVIEWS.md | Review mode | Last 3 reviews: full read. Older reviews: status line only |

### How to find the right batch

```
1. Determine the round number range needed (from scope)
2. Map to batch file: DEVLOG-RXXX-RXXX.md
3. Read from that file — only the relevant sections
```

## TASK_STATE.md — Interrupt checkpoint

TASK_STATE.md is a lightweight checkpoint file that enables cross-session task resumption.

### Lifecycle

```
Task starts       → Create TASK_STATE.md with status: in-progress
Task progresses   → Update checkpoint items ([x] / [ ]) and Working Context
Task interrupted  → TASK_STATE.md persists in repo (survives terminal/session switch)
New session starts → Step 0 in Development mode checks if TASK_STATE.md exists
Task completes    → Consolidate into DEVLOG batch round, delete TASK_STATE.md
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
- [x] [completed step]
- [ ] [current/next step]
- [ ] [future step]

## Working Context
- **Files being edited**: [list of files]
- **Last command run**: [command] ([status])
- **Key decisions**: [decision + reference to docs/memory]
- **Blocker**: [description or "None"]

## Resume From
[explicit instruction for the next session: what to do, where to start]
```

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

Priority: `in-progress` > `blocked`. Present both to user and let them choose.

## PLAN.md — Project plan

PLAN.md is a living document for planning multi-step work before implementation. It sits above TASK_STATE.md in the abstraction hierarchy.

### Relationship

```
PLAN.md     = Strategy (what to do, why, in what order)
TASK_STATE  = Tactics (where we are in the plan, specific progress)
DEVLOG.md   = Record (what was done)
```

### When to use

- User says "帮我规划一下", "先想清楚再做", "plan this out"
- Task is estimated to span more than 3 dev log rounds
- Multiple related features that need sequencing
- Architecture decision that needs rationale documentation

When PLAN.md exists, TASK_STATE.md should reference which plan step is being worked on.

### Format

```markdown
---
status: planning | in-progress | done
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# [Feature/Project Name]

## Goal
[one sentence — what we're building and why]

## Context
[background: constraints, stakeholders, dependencies]

## Plan
1. [x] [completed step]
2. [ ] [current step — this should match TASK_STATE.md Progress]
3. [ ] [future step]

## Decisions
- [Decision]: chose [X] over [Y] because [Z]
- [Decision]: ...

## Risks
- [risk]: [mitigation]

## Related
- [links to relevant docs, issues, or memory entries]
```

### Lifecycle

```
Planning phase  → Create PLAN.md with status: planning
Work begins     → Update status: in-progress
Steps complete  → Check off items in Plan section
All done        → Update status: done (keep file as historical record)
New related work → Reopen by updating status and adding new steps
```

### When NOT to use

- Single task that can be done in 1-2 rounds → use TASK_STATE.md only
- Task is already clear and well-defined → skip planning, go straight to Development
- User didn't ask for planning and the task is straightforward
