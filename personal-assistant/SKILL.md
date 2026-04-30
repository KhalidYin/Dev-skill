---
name: personal-assistant
description: "Document-first development copilot for R/Python repos. Use whenever the user wants to change code, fix bugs, add tests, refactor modules, reconcile docs with implementation, or work in a project that uses PROJECT_GUIDE.md, PROJECT_SPEC.md, CODE_STYLE.md, and TEST_GUIDE.md."
---

# Personal Assistant

Use this skill for small to medium engineering tasks in R/Python codebases where documentation, tests, implementation, and project memory need to stay aligned.

## Modes

This skill routes tasks into one of four modes based on the user's intent:

| Mode | Trigger | What happens |
|------|---------|--------------|
| **Bootstrap** | Project has no docs at all | Generate minimal doc skeleton in `docs/main/`, then proceed |
| **Consultation** | "what is", "how does", "explain", "find" — read-only inquiry | Read docs + code, answer, no edits |
| **Development** | "fix", "add", "change", "refactor", "implement" | Full workflow: implement → test → update docs → update memory |
| **Review** | "review", "audit", "检查", "审核", "inspect" | Quick Review first (verbal); ask if Full Report is needed |

### Mode selection

1. Check if `docs/main/` exists with the four canonical docs. If entirely missing → **Bootstrap**
2. If the request is read-only (asking questions, understanding code) → **Consultation**
3. If the request asks for a review/audit/inspection → **Review**
4. If the request asks to change something → **Development**

## Working rules

Read the detailed workflow in:

- `references/project-contract.md` — document conventions, paths, and bootstrap
- `references/policy.md` — testing, fix quality, output discipline, conflict handling
- `references/review-protocol.md` — Quick Review and Full Report workflow
- `references/context-memory.md` — cross-platform project memory system

## Quick start by mode

### Bootstrap
1. check if `docs/main/` exists with any of the four canonical docs
2. if entirely missing, auto-generate a minimal skeleton (outline only, no speculative content)
3. tell the user what was created and ask them to fill in project-specific details later
4. proceed with the original request in the appropriate mode

### Consultation
1. read relevant docs and project memory
2. inspect nearby code as needed
3. answer the question concisely — no code changes, no doc updates
4. if the answer reveals important context, optionally save it to memory

### Development
1. inspect the relevant docs, nearby code, and project memory (`docs/main/memory/`)
2. state the constraint or design choice that matters
3. make the smallest viable implementation
4. add or update tests
5. update the relevant docs
6. update context memory if new decisions, facts, or user preferences emerged
7. summarize the change, risk, and validation

### Review
1. inspect the relevant docs, code, and memory
2. perform **Quick Review** — output 3-5 bullet points verbally (issues, gaps, risks)
3. ask the user: "需要我生成完整的审查报告到 `docs/dep/` 吗？"
4. only if the user confirms, generate a Full Report file in `docs/dep/review-<YYYYMMDD>-<round>.md`
5. link back to prior related reviews if any
