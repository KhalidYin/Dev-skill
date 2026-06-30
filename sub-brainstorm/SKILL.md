---
name: sub-brainstorm
description: "Brainstorming skill for exploring requirements, comparing approaches, and outputting design to sub-plan files. Use when planning new features, architecture decisions, or complex designs. Outputs to docs/dep/plans/backlog/."
---

# Sub-Brainstorm

Turn ideas into designs through collaborative dialogue. Output writes to sub-plan files.

<HARD-GATE>
Do NOT write code, create sub-plans, or take implementation action until design is approved. This applies to EVERY project regardless of perceived simplicity.
</HARD-GATE>

## Anti-Pattern: "Too Simple For Design"

Every project goes through this process. Simple projects are where unexamined assumptions cause the most wasted work. The design can be short, but you MUST present it and get approval.

## Checklist

Complete in order:

1. **Explore project context** — check `docs/main/`, recent commits, existing plans
2. **Offer visual companion** — just-in-time when visual questions arise (see `references/visual-companion.md`)
3. **Ask clarifying questions** — one at a time, understand purpose/constraints/success criteria
4. **Propose 2-3 approaches** — with trade-offs and your recommendation
5. **Present design** — in sections, get user approval after each section
6. **Self-review** — check for placeholders, contradictions, ambiguity, scope
7. **User reviews design** — ask user to approve before writing
8. **Write sub-plan** — save to `docs/dep/plans/backlog/P<phase>-<name>.md`

## Process

**Understanding the idea:**

- Check current project state: `docs/main/`, recent commits, existing plans in `docs/dep/plans/`
- Assess scope: if multiple independent subsystems, flag immediately for decomposition
- Ask questions one at a time, prefer multiple choice
- Focus on: purpose, constraints, success criteria

**Exploring approaches:**

- Propose 2-3 different approaches with trade-offs
- Lead with your recommended option and explain why
- Compare: complexity, impact, alignment with existing architecture

**Presenting the design:**

- Present in sections scaled to complexity
- Ask after each section if it looks right
- Cover: architecture, components, data flow, error handling, testing
- Go back and clarify when something doesn't make sense

**Design principles:**

- Break into units with one clear purpose and well-defined interfaces
- Each unit should be understandable and testable independently
- Follow existing patterns in the codebase
- Don't propose unrelated refactoring

## Output

Write approved design to `docs/dep/plans/backlog/P<phase>-<name>.md` using sub-plan format:

```yaml
---
phase_index: N
status: planning
created: YYYY-MM-DD
updated: YYYY-MM-DD
priority: 1
estimated_rounds: X-Y
depends_on: []
tags: []
syncs_to: []
---
```

Followed by:

```markdown
# [Feature Name]

## Background & Goals
[Why this is needed, what it solves]

## Constraints
[Technical, time, resource limitations]

## Approach Comparison

### Approach A: [Name]
- Overview: [one sentence]
- Pros: [...]
- Cons: [...]
- Complexity: low/medium/high

### Approach B: [Name]
- Overview: [one sentence]
- Pros: [...]
- Cons: [...]
- Complexity: low/medium/high

### Recommendation
[Which one, why]

## Design Details
[Architecture, components, interfaces, data flow]

## Phase Overview
| Phase | Goal | Est. Rounds | Depends On |
|-------|------|-------------|------------|
| P1 | ... | ... | - |

## Risks
[Risks and mitigation]

## Execution Findings
(empty initially)
```

## After Writing

1. Commit the sub-plan file
2. Inform user: sub-plan written to `<path>`
3. **Done** — return control to caller (personal-assistant Planning mode or direct user)

Do NOT invoke any other skill. Do NOT start implementation.

## Key Principles

- **One question at a time** — don't overwhelm
- **Multiple choice preferred** — easier to answer
- **YAGNI ruthlessly** — remove unnecessary features
- **Explore alternatives** — always propose 2-3 approaches
- **Incremental validation** — present design, get approval before moving on

## Visual Companion

Browser-based companion for mockups, diagrams, and visual options. See `references/visual-companion.md`.

Offer just-in-time when a question would genuinely be clearer shown than told. Do NOT offer upfront.
