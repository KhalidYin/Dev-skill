# Project contract

Use these docs as the source of truth when they exist:

- `PROJECT_GUIDE.md` — architecture, module responsibilities, data flow, shared dependencies
- `PROJECT_SPEC.md` — technical scope, design decisions, feature boundaries
- `CODE_STYLE.md` — naming, formatting, style, and local conventions
- `TEST_GUIDE.md` — test layout, regression coverage, and test entry points

If the repo uses different filenames, map them to these roles once and keep that mapping consistent.

If a required doc is missing, incomplete, or contradicts another doc, do not guess. Report the exact gap or conflict and ask the user to confirm the direction before changing code.

If the docs are missing entirely, propose a short draft outline first and wait for approval before implementation.

Document only what is actually implemented. Do not write planned work, placeholder menus, or future ideas as if they already exist.

Any code change that affects architecture, interfaces, data flow, validation rules, naming, or testing expectations must be reflected in the relevant docs in the same task.

If the change is purely local and does not alter behavior or project contracts, limit documentation updates to the affected area.
