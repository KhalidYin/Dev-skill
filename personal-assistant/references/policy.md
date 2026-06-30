# Working policy

## Tests

- Keep tests under `tests/`
- Mirror the project structure when creating test subfolders
- If `tests/` does not exist, recommend initializing `tests/` and `tests/fixtures/`
- Prefer the smallest reliable test that proves the fix or feature

If test coverage is constrained by the current code structure, say so clearly and describe the smallest practical verification you can do.

## Fix quality

- Fix the source of the bug, not just the symptom
- Avoid unrelated refactors
- Preserve existing naming and module boundaries unless they are part of the issue
- Prefer lightweight automation over manual repetition

For recurring checks, suggest or use simple tools such as `pre-commit`, `styler`, `lintr`, or a small verification script if the repo already supports that pattern.

## Quick Fix mode

Quick Fix is a lightweight sub-mode of Development for small, low-risk changes. It reduces ceremony while maintaining a minimum audit trail.

### When to use Quick Fix

**User-triggered**: User explicitly says "quick fix", "小改动", "快速修一下", or similar.

**AI validation is mandatory** — even if the user requests Quick Fix, the AI must autonomously assess the change scope before proceeding. If validation fails, upgrade to full Development mode and explain why.

### AI validation rules

Before entering Quick Fix, analyze the planned change against these criteria. **If ANY are true, reject Quick Fix and upgrade to full Development:**

| Check | Reject if true |
|-------|---------------|
| File count | Touches more than 2 files |
| Interface change | Modifies function signatures, API endpoints, or data models |
| Architecture impact | Affects modules, data flow, or shared dependencies described in PROJECT_GUIDE.md |
| Config/env change | Modifies configuration, environment variables, CI/CD, or deployment-related files |
| Test breakage | Existing tests fail after the change |
| Spec boundary | Crosses feature boundaries defined in PROJECT_SPEC.md |
| Naming convention | Introduces new naming that conflicts with CODE_STYLE.md |

If none of the above apply, proceed with Quick Fix.

### Quick Fix flow

```
1. Validate change scope (AI autonomous check above)
2. Make the change
3. Run related tests (if test suite exists)
4. Write one-line entry to the active DEVLOG batch and `devlog/INDEX.md` (not a full round — see dev-log-protocol.md)
5. Done — skip: TASK_STATE.md, doc consistency check, output discipline
```

### Rejection message format

When Quick Fix is rejected:

```
这个改动不适合 Quick Fix 模式，原因：
- [具体原因，如：修改了 API 接口签名，影响 PROJECT_SPEC.md 中定义的边界]

切换到完整 Development 模式处理。
```

## Dev log

After every completed round of work in Development mode, write a dev log entry to the active `docs/dep/devlog/active/DEVLOG-RXXX-RYYY.md` batch and one row to `docs/dep/devlog/INDEX.md`. This is non-negotiable — the review process depends on it.

**Quick Fix exception**: Quick Fix uses a one-line entry format instead of a full round. See `references/dev-log-protocol.md` for both formats.

## Doc consistency check

After updating docs in Development mode, cross-check the following files for consistency:

- `docs/main/PROJECT_GUIDE.md`
- `docs/main/PROJECT_SPEC.md`
- `docs/main/CODE_STYLE.md`
- `docs/main/TEST_GUIDE.md`
- `<root>/USAGE.md`

**Exclude:** `docs/main/memory/` (managed separately).

**Quick Fix exception**: Doc consistency check is skipped for Quick Fix changes (they don't touch docs).

### Check rules

1. **Terminology** — the same concept must use the same name across all docs. If GUIDE says "auth module" and SPEC says "authentication service", flag it.
2. **Claims** — a statement in one doc must not contradict another. If GUIDE says "stateless API" and SPEC says "session-based auth", flag it.
3. **Omissions** — if a feature/module is described in GUIDE but missing from SPEC, or vice versa, flag it.

### Output format

```
## Doc Consistency
- (no issues) → "All docs consistent."
- (issues found) → flag each with source files + the conflicting terms or claims
  - GUIDE: "auth module"  vs  SPEC: "authentication service" — terminology drift
  - GUIDE mentions "rate limiter" — not found in SPEC
```

### Rules

- **No fuzzy language** — never say "probably fine", "seems consistent", "looks OK". Either concrete mismatch or clear pass.
- **Do not silently fix** — flag the discrepancy to the user. Do not unilaterally rewrite one doc to match another.
- **Ask the user** which term or claim is correct, then apply the resolution.

## Output discipline

Output verbosity scales with change size. Determine the level before responding:

### Level 1 — Small change (single file, <10 lines, no interface/config change)

```
[一句话 summary]
已写入 dev log。
```

Skip: risk note, optimization advice, validation, doc consistency.

### Level 2 — Medium change (multi-file, or affects interfaces)

```
## Summary
[what changed]

## Risk Note
[one of: technical risk, maintenance risk, project risk]

## Doc Consistency
[check result]
```

Skip: optimization advice, detailed validation.

### Level 3 — Large change (architecture change, new module, spec boundary change)

```
## Summary
[what changed]

## Risk Note
[technical / maintenance / project risk]

## Optimization Advice
- Immediate: [...]
- Medium-term: [...]
- Tooling: [...]

## Validation
[what was validated, what could not be validated]

## Doc Consistency
[check result]
```

All 5 items included.

### Level selection

| Criteria | Level 1 | Level 2 | Level 3 |
|----------|---------|---------|---------|
| Files changed | 1 | 2-3 | 4+ |
| Lines changed | <10 | 10-100 | 100+ |
| Interface impact | None | Internal | Public API |
| Architecture impact | None | Minor | Significant |
| Quick Fix mode | Always L1 | N/A | N/A |

When pointing to code, use clickable file references with line numbers: `path/to/file.py:42`.

## Review tiers

Reviews use a two-tier approach:

1. **Quick Review** (default) — reads dev log since last review, outputs 3-5 bullet points + cross-check verdict. No file written.
2. **Full Report** — appends detailed report to `docs/dep/REVIEWS.md`. Only generated when the user confirms after Quick Review.

See `references/review-protocol.md` for the complete workflow.

## Conflict handling

If the project docs, code, and user request disagree, do not resolve the conflict silently.

1. Identify the conflicting files or rules
2. Explain the practical impact
3. Ask the user which direction to follow

Only proceed once the conflict is explicit.

## Context memory

Before any significant change, check `docs/main/memory/MEMORY.md` for relevant context. After completing work, save new decisions, preferences, or project facts to memory.

See `references/context-memory.md` for the full memory protocol.

## Document language

**All project documentation MUST be written in Chinese. This is non-negotiable.**

| Document | Language | Note |
|----------|----------|------|
| `USAGE.md` | Chinese | |
| `docs/main/PROJECT_GUIDE.md` | Chinese | |
| `docs/main/PROJECT_SPEC.md` | Chinese | |
| `docs/main/CODE_STYLE.md` | Chinese | |
| `docs/main/TEST_GUIDE.md` | Chinese | |
| `docs/main/memory/*.md` | Chinese | Frontmatter fields (`name`, `description`, `type`) may remain English |
| `docs/dep/DEVLOG.md` + `docs/dep/devlog/**` | Chinese | Section headers (`Done`, `Issues/Blockers`, `Next`, `Files Changed/Commits`) may remain English |
| `docs/dep/REVIEWS.md` | Chinese | Section headers and table headers may remain English |
| `docs/dep/PLAN.md` | Chinese | Section headers may remain English |
| `docs/dep/TASK_STATE.md` | Chinese | Progress items and context must be Chinese; section headers may remain English |
| `docs/deploy/DEPLOY_GUIDE.md` | Chinese | |

**Code identifiers** (function names, variable names, file paths, commit hashes) are exempt — they follow the programming language's convention.

**User-facing output** (Quick Review, responses, summaries) must be in Chinese.

## Language guidance (programming)

Follow the existing stack first — this skill works with any language. Detect the project's language and tooling, then match its conventions.

- Prefer the testing framework already in use (pytest, unittest, testthat, Jest, etc.)
- Match the project's existing code style, naming conventions, and formatting
- Use the package manager and build system the project already uses
- Avoid introducing new tooling unless it clearly pays for itself
- For R: prefer clear data transformations and explicit dependencies
- For Python: prefer focused functions and readable control flow
