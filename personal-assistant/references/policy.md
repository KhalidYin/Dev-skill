# Working policy

## Tests

- Keep tests under `tests/`
- Mirror the project structure when creating test subfolders
- If `tests/` does not exist, recommend initializing `tests/` and `tests/fixtures/`
- Prefer the smallest reliable test that proves the fix or feature

If test coverage is constrained by the current code structure, say so clearly and describe the smallest practical verification you can do.

## Fix quality

- fix the source of the bug, not just the symptom
- avoid unrelated refactors
- preserve existing naming and module boundaries unless they are part of the issue
- prefer lightweight automation over manual repetition

For recurring checks, suggest or use simple tools such as `pre-commit`, `styler`, `lintr`, or a small verification script if the repo already supports that pattern.

## Dev log (mandatory)

After every completed round of work in Development mode, write a dev log entry to `docs/dep/dev-<YYYYMMDD>.md`. This is non-negotiable — the review process depends on it.

- **One file per day**, multiple rounds within the file
- **Each round** must include: `Done`, `Issues / Blockers`, `Next`, `Files Changed`
- **Be concrete** — "Fixed login timeout" not "Worked on auth"
- **Next** — always end with clear next steps; write "Done — no next steps" if complete
- **Open issues** — if an issue from a prior round is still unresolved, mention it again

See `references/dev-log-protocol.md` for the full format spec.

## Task resume

Development mode checks the most recent dev log before starting new work:

- Read the last round of the most recent `dev-*.md` file
- If `Next` has open items (not "Done — no next steps") → remind the user what was pending and ask whether to continue or start fresh
- If no dev log exists or last round's `Next` is cleared → proceed as new task
- This uses existing dev log fields as natural checkpoints — no separate state file needed

## Doc consistency check

After updating docs in Development mode, cross-check the following files for consistency:

- `docs/main/PROJECT_GUIDE.md`
- `docs/main/PROJECT_SPEC.md`
- `docs/main/CODE_STYLE.md`
- `docs/main/TEST_GUIDE.md`
- `<root>/USAGE.md`

**Exclude:** `docs/main/memory/` (managed separately).

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

When responding, include:

- a risk note with one of: technical risk, maintenance risk, or project risk
- optimization advice grouped into: immediate, medium-term, and tooling
- a concise summary of what changed or what you recommend changing
- what was validated, or what could not be validated yet
- doc consistency check result (see above)

When pointing to code, use clickable file references with line numbers when possible, for example `path/to/file.py:42`.

## Review tiers

Reviews use a two-tier approach to avoid overhead:

1. **Quick Review** (default) — reads dev logs since last review, outputs 3-5 bullet points + cross-check verdict. No file written.
2. **Full Report** — detailed markdown report in `docs/dep/` with Dev Log Cross-check table. Only generated when the user confirms after seeing the Quick Review.

See `references/review-protocol.md` for the complete workflow.

## Conflict handling

If the project docs, code, and user request disagree, do not resolve the conflict silently.

1. identify the conflicting files or rules
2. explain the practical impact
3. ask the user which direction to follow

Only proceed once the conflict is explicit.

## Context memory

This skill maintains a cross-platform project memory. Before any significant change, check `docs/main/memory/MEMORY.md` for relevant context. After completing work, save new decisions, preferences, or project facts to memory.

See `references/context-memory.md` for the full memory protocol.

## Language guidance

Follow the existing stack first — this skill works with any language. Detect the project's language and tooling, then match its conventions.

- Prefer the testing framework already in use (pytest, unittest, testthat, Jest, etc.)
- Match the project's existing code style, naming conventions, and formatting
- Use the package manager and build system the project already uses
- Avoid introducing new tooling unless it clearly pays for itself
- For R: prefer clear data transformations and explicit dependencies
- For Python: prefer focused functions and readable control flow
