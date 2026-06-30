# Context memory

This skill maintains a **cross-platform project memory** — a portable, file-based system that persists project context across conversations, sessions, and platforms. It is stored in the project repository itself and travels with the code.

## Why repo memory

Claude Code has a native auto-memory system (`~/.claude/projects/.../memory/`), but it is **local to your machine**. The repo memory system solves problems that native memory cannot:

| Scenario | Native memory | Repo memory |
|----------|--------------|-------------|
| Switch to a different computer | Lost — not in the repo | Comes with `git clone` |
| New teammate joins | Starts with zero context | Full project memory available |
| CI / automated agents | No access to your local state | Reads from the repo |
| Use a different AI tool | Claude-only format | Platform-agnostic Markdown |
| Reinstall OS / wipe config | Gone | In version control |

**They are complementary, not redundant:**
- Repo memory is the **source of truth** — lives in the project, version-controlled, shared
- Native memory can act as a **local cache** — personal notes, temporary reminders, tool-specific preferences
- This skill reads from and writes to **repo memory** (`docs/main/memory/`)

## Relationship with TASK_STATE.md

| System | Purpose | Lifetime | Location |
|--------|---------|----------|----------|
| **Memory** (`docs/main/memory/`) | Long-term project knowledge: decisions, preferences, constraints, references | Permanent — persists across all sessions | Version-controlled in repo |
| **TASK_STATE.md** (`docs/dep/`) | Short-term task checkpoint: what's in-progress, working context, resume point | Temporary — exists only during active work | Version-controlled in repo |
| **DEVLOG storage** (`docs/dep/DEVLOG.md`, `docs/dep/devlog/`) | Historical record: what was done, issues, commits | Permanent indexed log with active/archive/summary layers | Version-controlled in repo |

Flow:
```
Task in progress  → TASK_STATE.md (hot checkpoint)
Task completes    → TASK_STATE.md → active DEVLOG batch + INDEX.md (historical record) + Memory (if new knowledge)
```

## Storage location

```
docs/main/memory/
├── MEMORY.md           # index of all memory entries (always read first)
├── user-role.md        # user role, goals, knowledge
├── user-prefs.md       # user preferences, tool choices, conventions
├── project-context.md  # project purpose, constraints, stakeholders
├── decisions.md        # architecture decisions, rationale
├── feedback.md         # user corrections, validated approaches
└── reference.md        # pointers to external resources
```

All files are Markdown with optional YAML frontmatter.

## When to read memory

**Always read `MEMORY.md` first** when starting work in a project. It is the index and tells you what memory entries exist.

Read specific memory files when:
- The user references past work or decisions ("remember when we...")
- You need to understand project conventions or constraints
- A task touches an area with recorded decisions
- The user asks you to recall something

## When to write memory

Save to memory when:
- The user explicitly asks you to remember something
- A significant architecture decision is made
- The user corrects your approach (save as feedback)
- You learn new constraints, deadlines, or stakeholder requirements
- The user confirms a non-obvious approach worked well

Do NOT save to memory:
- When TASK_STATE.md is sufficient (in-progress work details)
- Code patterns derivable from reading the code
- Git history or recent changes — `git log` is authoritative
- Ephemeral task details or temporary state
- Anything already documented in CLAUDE.md or `docs/main/` files

## Memory entry format

Each memory file uses this structure:

```markdown
---
name: <short name>
description: <one-line summary — used to decide relevance>
type: user | project | feedback | reference
---

<content — for feedback/project types, structure as: rule/fact, then **Why:** and **How to apply:** lines>
```

## MEMORY.md index format

```markdown
# Project Memory Index

- [Entry Title](memory/entry-file.md) — one-line description
- [Another Entry](memory/another-file.md) — one-line description
```

Keep entries under ~150 characters. The index is always loaded; individual files are read on demand.

## Cross-platform portability

- Uses only Markdown + YAML frontmatter — no proprietary formats
- Stored in the project repo — travels with the code
- Platform-agnostic: works with Claude Code, GitHub Copilot, custom AI tooling, or human readers
- No dependency on Claude Code's `.claude/` directory or memory system
- Can be version-controlled alongside the project

## Memory lifecycle

- **Create** — when new context is learned
- **Update** — when existing memory becomes stale or incorrect; overwrite the file
- **Delete** — when memory is no longer relevant; remove the file and its index entry
- **Verify** — before acting on memory, confirm it still matches current project state

If a recalled memory conflicts with current code or docs, trust what you observe now and update the memory.
