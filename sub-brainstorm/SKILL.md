---
name: sub-brainstorm
description: "Brainstorming skill for exploring requirements, comparing approaches, defining frontend/UI behavior contracts, and outputting approved designs to sub-plan files. Use when planning new features, architecture decisions, complex designs, or design-driven UI work. Outputs to docs/dep/plans/backlog/."
---

# Sub-Brainstorm

Turn ideas into approved, testable design contracts through collaborative dialogue. Output writes to sub-plan files.

<HARD-GATE>
Do NOT write code, create sub-plans, or take implementation action until design is approved. This applies to EVERY project regardless of perceived simplicity.
</HARD-GATE>

## Anti-Pattern: "Too Simple For Design"

Every project goes through this process. Simple projects are where unexamined assumptions cause the most wasted work. The design can be short, but you MUST present it and get approval.

## Invocation Modes

### Delegated mode

Use delegated mode when `personal-assistant` routes a formal Planning request here. Accept this context packet when provided:

```yaml
caller: personal-assistant
request: "[original request]"
known_constraints: []
relevant_paths: []
existing_plans: []
suggested_phase_index: N
suggested_sub_plan: docs/dep/plans/backlog/PN-name.md
ui_in_scope: true | false
```

- Treat packet values as hints, verify them against the workspace, and do not invent missing facts.
- Own the design dialogue, sub-plan write, and PLAN registration until returning.
- Do not ask the caller to repeat information already present in the packet.
- Do not invoke `personal-assistant` or start implementation.

### Standalone mode

Use standalone mode when the user invokes this skill directly. Gather the same context from the workspace, select a non-conflicting phase index/path, then follow the same design and output workflow.

## Checklist

Complete in order:

1. **Resolve invocation mode** — read the delegation packet or establish standalone context
2. **Explore project context** — check `docs/main/`, recent commits, existing plans; verify phase/path conflicts
3. **Offer visual companion** — just-in-time when visual questions arise (see `references/visual-companion.md`)
4. **Ask clarifying questions** — one at a time, understand purpose/constraints/success criteria
5. **Propose 2-3 approaches** — with trade-offs and your recommendation
6. **Present design** — in sections, get user approval after each section; for UI work, specify visible behavior and evidence boundaries
7. **Self-review** — check for placeholders, contradictions, ambiguity, scope
8. **User reviews design** — ask user to approve before writing
9. **Write and register** — use the canonical template, save the sub-plan, and register it once in PLAN.md
10. **Return control** — emit the return contract and stop

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
- If UI is in scope, cover what users see and can operate, not just module or component names
- Go back and clarify when something doesn't make sense

**UI design contract:**

For any frontend page, component workflow, or design-driven implementation, collect and obtain approval for:

1. **Design baseline and deviations** — source/version, module order, first-view defaults, shared KPIs, layout hierarchy, narrow-screen behavior, and every proposed deviation with reason.
2. **Page/component/state/interaction matrix** — stable UI IDs mapping each visible or operable element to its data source, default state, interaction result, URL restoration behavior, state coverage, test assertion, and deviation permission.
3. **Visual and behavior acceptance checklist** — assertions for core navigation, clicking, selection, filtering, grouping, default slots, responsive states, and approved deviations.

Use this mapping for every material UI element:

```text
design element -> data source -> page/component -> default state
-> interaction result -> test assertion -> deviation permission
```

Required states are default, loading, empty, error, partial-data, and narrow-screen. Mark a state `N/A` only with a reason. Every displayed metric, chart, and grouping must cite a payload path or another declared source. When evidence is missing, define placeholder/hide/disable/error behavior; do not invent derivations.

Do not approve a UI design that only names sections such as "implement Baseline, Demographics, Disposition". Do not turn the plan into CSS values or implementation-level class/function lists.

**Design principles:**

- Break into units with one clear purpose and well-defined interfaces
- Each unit should be understandable and testable independently
- Follow existing patterns in the codebase
- Don't propose unrelated refactoring

## Output

Use `personal-assistant/references/planning-protocol.md` as the workflow authority, `personal-assistant/templates/sub-plan.md.template` as the sub-plan format authority, and `personal-assistant/templates/plan-dashboard.md.template` when PLAN.md must be created. Locate the installed or workspace `personal-assistant` skill and read these files. Preserve the sub-plan template's frontmatter, Phase contract, main-doc sync, findings, decision, and sync sections. Do not maintain or invent a second planning schema in this skill.

For UI work, keep the template's three UI sections:

- `设计基线与偏差清单`
- `页面/组件/状态/交互矩阵`
- `视觉与行为验收清单`

Each UI Phase completion criterion must reference the UI IDs it owns. For non-UI work, remove the optional UI sections.

If the planning protocol, sub-plan template, or a required PLAN dashboard template cannot be found, return `blocked` before writing and report the missing `personal-assistant` dependency. The approved design may still be presented in chat, but must not be serialized into an incompatible plan.

## After Writing

1. Recheck that the final phase index/path does not conflict with existing plans.
2. Write the approved sub-plan to `docs/dep/plans/backlog/P<phase>-<name>.md`.
3. Register exactly one matching row in `docs/dep/PLAN.md` under "待开始".
4. Verify the sub-plan path, frontmatter status, and PLAN pointer agree.
5. Return:

```yaml
status: approved-written | cancelled | blocked
sub_plan: docs/dep/plans/backlog/PN-name.md | null
plan_registered: yes | no
decisions: []
unresolved: []
recommended_next: development | wait
```

Return rules:

- `approved-written`: user approved the design, both writes succeeded, and `plan_registered` is `yes`.
- `cancelled`: user did not approve or ended planning; write neither file.
- `blocked`: authority files are missing, a path conflict remains, documents conflict, or either write/verification failed.
- Never return `recommended_next: development` unless status is `approved-written`.
- In delegated mode, return control to `personal-assistant`; it decides whether to enter Development.
- In standalone mode, report the same contract to the user and stop.

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
