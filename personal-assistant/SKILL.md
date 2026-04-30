---
name: personal-assistant
description: "Document-first development copilot. Use whenever the user wants to change code, fix bugs, add tests, refactor modules, reconcile docs with implementation, review or audit code, summarize changes, deploy or ship code, or work in a project that uses PROJECT_GUIDE.md, PROJECT_SPEC.md, CODE_STYLE.md, and TEST_GUIDE.md."
---

# Personal Assistant

Use this skill for small to medium engineering tasks in any codebase where documentation, tests, implementation, and project memory need to stay aligned.

## Document system

See `references/doc-structure.md` for the complete document tree, naming conventions, and per-file write rules.

## Modes

This skill routes tasks into one of five modes based on the user's intent:

| Mode | Trigger | What happens |
|------|---------|--------------|
| **Bootstrap** | Project has no docs at all | Generate minimal doc skeleton + USAGE.md, then proceed |
| **Consultation** | "what is", "how does", "explain", "find" — read-only | Read docs + code, answer, no edits |
| **Development** | "fix", "add", "change", "refactor", "implement" | Implement → test → update docs → validate consistency → write dev log → update memory |
| **Review** | "review", "audit", "检查", "审核", "inspect" | Quick Review first (cross-checks dev logs); ask if Full Report needed |
| **Deployment** | "deploy", "部署", "上线", "发布", "ship" | Generate or update deployment guide in `docs/deploy/DEPLOY_GUIDE.md` |

### Mode selection

1. Check if `docs/main/` exists with the four canonical docs. If entirely missing → **Bootstrap**
2. If the request mentions deployment → **Deployment**
3. If the request is read-only (asking questions, understanding code) → **Consultation**
4. If the request asks for a review/audit/inspection → **Review**
5. If the request asks to change something → **Development**

## Working rules

Read the detailed workflow in:

- `references/doc-structure.md` — authoritative document paths and naming conventions
- `references/project-contract.md` — document conventions, paths, and bootstrap
- `references/policy.md` — testing, fix quality, output discipline, consistency check, conflict handling
- `references/dev-log-protocol.md` — dev log format and mandatory write rules
- `references/review-protocol.md` — Quick Review and Full Report workflow
- `references/context-memory.md` — cross-platform project memory system

## Quick start by mode

### Bootstrap
1. check if `docs/main/` exists with any of the four canonical docs
2. if entirely missing, auto-generate a minimal skeleton (outline only, no speculative content)
3. generate `USAGE.md` at project root: quick start, detected prerequisites, common commands (TBD where unknown)
4. create `docs/dep/` and `docs/deploy/` directories
5. tell the user what was created and ask them to fill in project-specific details later
6. proceed with the original request in the appropriate mode

### Consultation
1. read relevant docs and project memory
2. inspect nearby code as needed
3. answer the question concisely — no code changes, no doc updates
4. if the answer reveals important context, optionally save it to memory

### Development
1. **Check for unfinished work** — read the last dev log's most recent round; if `Next` has open items, ask: "上次 [date] 还有未完成的任务：xxx。继续上次的任务还是开始新任务？"
2. inspect the relevant docs, nearby code, and project memory (`docs/main/memory/`)
3. state the constraint or design choice that matters
4. make the smallest viable implementation
5. add or update tests
6. update the relevant docs in `docs/main/` and `USAGE.md` if applicable
7. **validate consistency** — cross-check `docs/main/*.md` (excl. memory/) + `USAGE.md` for terminology drift or conflicts (see policy.md § Doc consistency check)
8. **write a dev log round** to `docs/dep/dev-<YYYYMMDD>.md` (mandatory, include commit hashes in Files Changed / Commits)
9. update context memory if new decisions, facts, or user preferences emerged
10. summarize the change, risk, and validation

### Review
1. read all dev logs in `docs/dep/` since the last review (or all if first review)
2. run `git log --oneline --since=<last review date>` and cross-check against dev log claims
3. inspect the relevant docs in `docs/main/` and the actual code
4. perform **Quick Review** — output 3-5 bullet points + cross-check verdict (include git/dev-log mismatches if found)
5. ask the user: "需要我生成完整的审查报告到 `docs/dep/` 吗？"
6. only if the user confirms, generate a Full Report with Dev Log Cross-check table
7. link back to prior related reviews if any

### Deployment
1. check if `docs/deploy/DEPLOY_GUIDE.md` exists; if not, create from skeleton
2. identify the project's deployment target(s): environments, platforms, services
3. write or update the deployment guide with:

```markdown
# Deployment Guide

## Environments
| Name | URL / Host | Branch | Notes |
|------|-----------|--------|-------|
| staging | ... | develop | ... |
| production | ... | main | ... |

## Prerequisites
- ...

## Step-by-step
1. ...
2. ...

## Configuration
- Env vars: ...
- Secrets: ...

## Rollback
1. ...
2. ...

## Verification
- [ ] ...
```
4. keep the guide in sync when deployment-relevant code changes (config files, CI scripts, env vars)
