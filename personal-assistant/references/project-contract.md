# Project contract

## Document location

All generated project documentation lives under `docs/main/`. This keeps the root directory clean and separates living docs from code.

```
docs/
├── main/                          # Primary project documentation
│   ├── PROJECT_GUIDE.md           # architecture, module responsibilities, data flow, shared dependencies
│   ├── PROJECT_SPEC.md            # technical scope, design decisions, feature boundaries
│   ├── CODE_STYLE.md              # naming, formatting, style, and local conventions
│   ├── TEST_GUIDE.md              # test layout, regression coverage, and test entry points
│   └── memory/                    # cross-platform project memory (see context-memory.md)
│       ├── MEMORY.md              # memory index
│       ├── user-*.md              # user profile / preferences
│       ├── project-*.md           # project facts / decisions
│       └── feedback-*.md          # feedback / corrections
│
└── dep/                           # Review / audit reports (per round)
    └── review-<YYYYMMDD>-<round>.md
```

Use these docs as the source of truth when they exist.

If the repo uses different filenames or paths, map them to these roles once and keep that mapping consistent.

## Bootstrap

When ALL four canonical docs are missing from `docs/main/` (or root), do NOT refuse to work. Instead, auto-generate a minimal skeleton:

```
docs/main/
├── PROJECT_GUIDE.md    # one-sentence summary + detected language/framework + top-level directory list
├── PROJECT_SPEC.md     # "TBD — add technical scope, design decisions, and feature boundaries"
├── CODE_STYLE.md       # "TBD — add naming conventions, formatting rules, and style preferences"
├── TEST_GUIDE.md       # "TBD — add test layout, entry points, and regression coverage notes"
└── memory/
    └── MEMORY.md       # empty index with header only
```

Bootstrap rules:
- Generate only what is immediately observable: project language, framework, top-level structure
- Use "TBD" placeholders for anything that requires human input
- Do NOT invent architecture, scope, or conventions — leave them blank
- Tell the user what was created and that they should fill in the details over time
- After bootstrap, proceed with the original request

If SOME docs exist but not all, only generate the missing ones. Do not overwrite existing docs.

## Doc sync rules

If a required doc is missing, incomplete, or contradicts another doc, do not guess. Report the exact gap or conflict and ask the user to confirm the direction before changing code.

Document only what is actually implemented. Do not write planned work, placeholder menus, or future ideas as if they already exist.

Any code change that affects architecture, interfaces, data flow, validation rules, naming, or testing expectations must be reflected in the relevant docs in the same task.

If the change is purely local and does not alter behavior or project contracts, limit documentation updates to the affected area.
