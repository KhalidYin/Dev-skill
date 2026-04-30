---
name: personal-assistant
description: "Document-first development copilot for R/Python repos. Use whenever the user wants to change code, fix bugs, add tests, refactor modules, reconcile docs with implementation, or work in a project that uses PROJECT_GUIDE.md, PROJECT_SPEC.md, CODE_STYLE.md, and TEST_GUIDE.md."
---

# Personal Assistant

Use this skill for small to medium engineering tasks in R/Python codebases where documentation, tests, and implementation need to stay aligned.

## When to use

Use this skill when the task involves any of the following:

- changing application code
- fixing a bug or regression
- adding or updating tests
- refactoring a module
- reviewing project structure or conventions
- updating developer-facing documentation
- reconciling code with existing project rules

If the request is only for a high-level idea or strategy, use the same document-first approach, but stop before implementation until the design is clear.

## Working rules

Read the detailed workflow in:

- `references/project-contract.md`
- `references/policy.md`

## Quick start

1. inspect the relevant docs and nearby code
2. state the constraint or design choice that matters
3. make the smallest viable implementation
4. add or update tests
5. update the relevant docs
6. summarize the change, risk, and validation

If the request is about docs only, skip implementation and focus on making the documentation accurate and internally consistent.
