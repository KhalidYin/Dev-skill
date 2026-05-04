# Project contract

## Document locations

See `references/doc-structure.md` — the authoritative source for all paths and naming conventions.

**Relationship**:
- `main/` — defines what the project IS (blueprint)
- `dep/DEVLOG.md` — records what was DONE (rolling dev log)
- `dep/REVIEWS.md` — records what was FOUND (rolling review reports)
- `dep/PLAN.md` — records what is PLANNED (optional, living document)
- `deploy/` — describes HOW to deploy (deployment guide)
- `USAGE.md` — how to USE the project (root level)

Reviews cross-check dev log claims against main docs, usage docs, and actual code.

Use these docs as the source of truth when they exist. If the repo uses different filenames or paths, map them to these roles once and keep that mapping consistent.

## Bootstrap

When ALL four canonical docs are missing from `docs/main/` (or root), auto-generate a minimal skeleton:

- `USAGE.md` — quick start filled with detected info; prerequisites and FAQ marked TBD
- `docs/main/PROJECT_GUIDE.md` — one-sentence summary + detected language/framework + top-level directory list
- `docs/main/PROJECT_SPEC.md` — TBD placeholder
- `docs/main/CODE_STYLE.md` — TBD placeholder
- `docs/main/TEST_GUIDE.md` — TBD placeholder
- `docs/main/memory/MEMORY.md` — empty index with header only
- `docs/dep/` — created, empty (DEVLOG.md created on first Development round)
- `docs/deploy/DEPLOY_GUIDE.md` — TBD placeholder

Bootstrap rules:
- Generate only what is immediately observable: project language, framework, top-level structure
- Use "TBD" placeholders for anything that requires human input
- Do NOT invent architecture, scope, or conventions — leave them blank
- Tell the user what was created and that they should fill in the details over time
- After bootstrap, proceed with the original request
- If SOME docs exist but not all, only generate the missing ones. Do not overwrite existing docs.

## Doc sync rules

If a required doc is missing, incomplete, or contradicts another doc, do not guess. Report the exact gap or conflict and ask the user to confirm the direction before changing code.

Document only what is actually implemented. Do not write planned work, placeholder menus, or future ideas as if they already exist.

Any code change that affects architecture, interfaces, data flow, validation rules, naming, or testing expectations must be reflected in the relevant docs in the same task.

If the change is purely local and does not alter behavior or project contracts, limit documentation updates to the affected area.
