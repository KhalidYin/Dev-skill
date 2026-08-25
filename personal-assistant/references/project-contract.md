# Project contract

## 目录

- [Document locations](#document-locations)
- [Document adoption](#document-adoption)
- [Bootstrap](#bootstrap)
- [Doc sync rules](#doc-sync-rules)
- [Main document templates](#main-document-templates)
- [Plan sync rules](#plan-sync-rules)

## Document locations

See `references/doc-structure.md` for the authoritative source for all paths, naming conventions, and file lifecycles.

Relationship:
- `docs/main/` defines what the project is.
- `docs/dep/DEVLOG.md` and `docs/dep/devlog/` record what was done.
- `docs/dep/REVIEWS.md` records what was found.
- `docs/dep/PLAN.md` records the current dashboard.
- `docs/dep/plans/<lifecycle>/P<phase>-<name>.md` records planned work in detail and moves through lifecycle directories.
- `docs/deploy/` describes how to deploy.
- `USAGE.md` describes how to use the project.

Reviews cross-check DEVLOG claims against main docs, usage docs, git history, and actual code.

Use these docs as the source of truth when they exist. If the repo uses different filenames or paths, map them to these roles once and keep that mapping consistent.

## Document adoption

Missing canonical documents mean the repository has not adopted this document system; they are not an error and do not trigger Bootstrap by themselves.

- Bootstrap requires an explicit user request or explicit acceptance of a Bootstrap proposal.
- Consultation, Quick Fix, Review, and Deployment do not create `docs/main/`, `USAGE.md`, DEVLOG, or TASK_STATE merely because those files are absent.
- Full Development may proceed using code and tests without adopting the document system. Offer Bootstrap separately when durable architecture or interface contracts would materially help, and do not block implementation solely on missing docs.
- Existing canonical, planning, DEVLOG, or mapped equivalent documents remain authoritative for their roles and must be maintained when the task affects them.
- Partial adoption does not authorize filling every missing document during an unrelated task. Create missing skeletons only inside an approved Bootstrap operation.

## Bootstrap

When Bootstrap is explicitly requested or accepted, generate the missing parts of the minimal skeleton from the bundled templates:

- `USAGE.md` - quick start filled with detected info; prerequisites and FAQ marked TBD.
- `docs/main/PROJECT_GUIDE.md` - based on `templates/PROJECT_GUIDE.md.template`; fill only observed language/framework and top-level structure.
- `docs/main/PROJECT_SPEC.md` - based on `templates/PROJECT_SPEC.md.template`; unknown sections remain TBD.
- `docs/main/CODE_STYLE.md` - based on `templates/CODE_STYLE.md.template`; unknown conventions remain TBD.
- `docs/main/TEST_GUIDE.md` - based on `templates/TEST_GUIDE.md.template`; unknown test details remain TBD.
- `docs/main/memory/MEMORY.md` - empty index with header only.
- `docs/dep/` - created; first Development round runs DEVLOG legacy adoption. If no prior DEVLOG exists, create `DEVLOG.md`, `devlog/INDEX.md`, and `devlog/active/DEVLOG-R001-R040.md`. If legacy DEVLOG files exist, move them unchanged into `devlog/archive/` first and create the next active batch after the highest archived round.
- `docs/deploy/DEPLOY_GUIDE.md` - TBD placeholder.

Bootstrap rules:
- Do not enter Bootstrap solely because all four canonical docs are missing.
- Generate only what is immediately observable: project language, framework, top-level structure, commands found in package/config files.
- Use `TBD` placeholders for anything requiring human input.
- Do not invent architecture, scope, or conventions.
- If some docs exist but not all, create only missing docs. Do not overwrite existing docs.
- Tell the user what was created and that project-specific details should be filled in over time.
- After bootstrap, proceed with the original request.

## Doc sync rules

If a required doc is missing, incomplete, or contradicts another doc, do not guess. Report the exact gap or conflict and ask the user to confirm the direction before changing code when the answer cannot be inferred from implementation.

Document only what is actually implemented. Do not write planned work, placeholder menus, or future ideas as if they already exist.

Any code change that affects architecture, interfaces, data flow, validation rules, naming, or testing expectations must be reflected in the relevant docs in the same task.

If the change is purely local and does not alter behavior or project contracts, limit documentation updates to the affected area.

## Main document templates

The four canonical `docs/main/` documents have explicit structures. Review and plan sync checks use these sections as targets.

| Main doc | Template | Sync targets |
|----------|----------|--------------|
| `PROJECT_GUIDE.md` | `templates/PROJECT_GUIDE.md.template` | Overview, tech stack, module structure, data flow, directory structure, key conventions |
| `PROJECT_SPEC.md` | `templates/PROJECT_SPEC.md.template` | Project goals, feature scope, technical decisions, interface contracts, non-functional requirements |
| `CODE_STYLE.md` | `templates/CODE_STYLE.md.template` | Naming, formatting, comments, import order, error handling, special conventions |
| `TEST_GUIDE.md` | `templates/TEST_GUIDE.md.template` | Test framework, test structure, run commands, coverage, test conventions, test data |

## Plan sync rules

### Sub-plan completion sync

When all Phases in a sub-plan are complete, synchronize according to the sub-plan frontmatter `syncs_to` list and the body section `## 主文档影响`.

Rules:
- `syncs_to` lists document filenames only.
- `## 主文档影响` must name the specific sections to update in each listed document.
- The two must match. A document listed in one place and missing in the other is a sync error.
- Sync only implemented behavior and accepted decisions.

Common sync targets:

1. **PROJECT_SPEC.md** - feature scope, technical decisions, interface contracts, non-functional requirements.
2. **PROJECT_GUIDE.md** - architecture changes, module responsibilities, data flow, directory structure.
3. **TEST_GUIDE.md** - test commands, test layout, coverage notes, fixture/data strategy.
4. **CODE_STYLE.md** - new naming, formatting, error handling, import, or project-specific style conventions.
5. **docs/main/memory/** - durable decisions, facts, and user preferences.

### PLAN.md pointer update

After sync:

1. Move the sub-plan from PLAN.md `进行中` to `最近完成`.
2. Keep only the latest 3 rows in `最近完成`.
3. Move the sub-plan file to `docs/dep/plans/complete/` and set `status: done`.
4. PLAN.md removes or updates only pointer rows; full history lives in `plans/complete/`.

### Empty dashboard

When PLAN.md `进行中` and `待开始` are both empty, a new plan updates the existing dashboard structure in place. Keep existing `延后` entries as future planning input unless the user explicitly clears them or moves them to `plans/deferred/`.

### Lifecycle sync

Sub-plan lifecycle is represented by directory and frontmatter together:

| Transition | File move | Frontmatter |
|------------|-----------|-------------|
| Confirmed but not started | create in `docs/dep/plans/backlog/` | `status: planning` |
| Starts execution | move to `docs/dep/plans/ongoing/` | `status: in-progress` |
| Completes and syncs | move to `docs/dep/plans/complete/` | `status: done` |
| Explicitly postponed | move to `docs/dep/plans/deferred/` | `status: deferred` |

`P0-tech-debt.md` is a rolling debt pool and normally remains `docs/dep/plans/backlog/P0-tech-debt.md` with `status: planning`. Do not keep it in `ongoing/` unless a specific extracted debt plan is actively being executed.
