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

## Output discipline

When responding, include:

- a risk note with one of: technical risk, maintenance risk, or project risk
- optimization advice grouped into: immediate, medium-term, and tooling
- a concise summary of what changed or what you recommend changing
- what was validated, or what could not be validated yet

When pointing to code, use clickable file references with line numbers when possible, for example `path/to/file.py:42`.

## Conflict handling

If the project docs, code, and user request disagree, do not resolve the conflict silently.

1. identify the conflicting files or rules
2. explain the practical impact
3. ask the user which direction to follow

Only proceed once the conflict is explicit.

## R and Python guidance

Follow the existing stack first, then fill gaps with standard practice.

- For R: prefer clear data transformations, explicit dependencies, and project-local testing tools when available
- For Python: prefer focused functions, readable control flow, and `pytest`-style tests when the repo already uses them
- For both: keep formatting consistent with the repository and avoid introducing new tooling unless it clearly pays for itself
