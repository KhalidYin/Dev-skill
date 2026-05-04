---
name: personal-assistant
description: "Document-first development copilot. Use whenever the user wants to change code, fix bugs, add tests, refactor modules, reconcile docs with implementation, review or audit code, summarize changes, deploy or ship code, or work in a project that uses PROJECT_GUIDE.md, PROJECT_SPEC.md, CODE_STYLE.md, and TEST_GUIDE.md."
---

# Personal Assistant

Use this skill for small to medium engineering tasks in any codebase where documentation, tests, implementation, and project memory need to stay aligned.

## Document system

See `references/doc-structure.md` for the complete document tree, naming conventions, and per-file write rules.

## Reference authority

| Reference | Authoritative for |
|-----------|-------------------|
| `doc-structure.md` | All file paths, naming rules, directory layout, TASK_STATE.md lifecycle, DEVLOG rotation |
| `project-contract.md` | Document relationships, bootstrap rules, doc sync rules |
| `policy.md` | Tests, fix quality, doc consistency, output discipline, conflict handling, language guidance |
| `dev-log-protocol.md` | DEVLOG.md format, rotation rules, layered reading, when/how to write dev log entries |
| `review-protocol.md` | Scope determination, Quick Review and Full Report workflow, REVIEWS.md format, layered reading |
| `context-memory.md` | Cross-platform memory system, memory vs TASK_STATE vs DEVLOG relationship |

## Modes

This skill routes tasks into one of five modes:

| Mode | Trigger | What happens |
|------|---------|--------------|
| **Bootstrap** | Project has no docs at all | Generate minimal doc skeleton + USAGE.md, then proceed |
| **Consultation** | "what is", "how does", "explain", "find" — read-only | Read docs + code, answer, no edits |
| **Development** | "fix", "add", "change", "refactor", "implement" | Check TASK_STATE → implement → test → update docs → validate → write dev log → update memory |
| **Review** | "review", "audit", "检查", "审核", "inspect" | Determine scope → Quick Review first; ask if Full Report needed |
| **Deployment** | "deploy", "部署", "上线", "发布", "ship" | Generate or update deployment guide in `docs/deploy/DEPLOY_GUIDE.md` |

### Mode selection

1. Check if `docs/main/` exists with the four canonical docs. If entirely missing → **Bootstrap**
2. If the request mentions deployment → **Deployment**
3. If the request is read-only (asking questions, understanding code) → **Consultation**
4. If the request asks for a review/audit/inspection → **Review**
5. If the request asks to change something → **Development**

## Quick start by mode

### Bootstrap
1. Check if `docs/main/` exists with any of the four canonical docs
2. If entirely missing, auto-generate a minimal skeleton (outline only, no speculative content)
3. Generate `USAGE.md` at project root: quick start, detected prerequisites, common commands (TBD where unknown)
4. Create `docs/dep/` and `docs/deploy/` directories
5. Tell the user what was created and ask them to fill in project-specific details later
6. Proceed with the original request in the appropriate mode

See `references/project-contract.md` for bootstrap rules.

### Consultation
1. Read relevant docs and project memory
2. Inspect nearby code as needed
3. Answer the question concisely — no code changes, no doc updates
4. If the answer reveals important context, optionally save it to memory

### Development

#### Step 0: Check interrupt checkpoint

1. If `docs/dep/TASK_STATE.md` exists, read it
2. **Expiry check** — compare TASK_STATE.md `updated` time with DEVLOG.md last round time:
   - If DEVLOG last round time >= TASK_STATE.updated → the task may have already completed and TASK_STATE is a stale leftover
   - Prompt: "TASK_STATE.md 显示任务在 [updated time] 中断，但 DEVLOG 显示 [last round time] 已有完成记录。这个任务是否已完成？我可以清理 TASK_STATE.md。"
   - If user confirms → delete TASK_STATE.md, proceed as new task
   - If user says no → treat as genuine interrupt, proceed with resume
3. If TASK_STATE is valid (not expired), present the in-progress task(s) to the user
4. Ask: "发现未完成的任务：[Goal]。继续还是开始新任务？"
5. If user continues, use the checkpoint's `Resume From` as the starting point
6. If no TASK_STATE.md exists, proceed to step 1

#### Step 1: Check for unfinished work

Read the last round in `docs/dep/DEVLOG.md` (current month only, see layered reading in `references/dev-log-protocol.md`). If `Next` has open items not covered by TASK_STATE.md, ask: "上次 [date] 还有未完成的任务：xxx。继续上次的任务还是开始新任务？"

#### Step 2: Route to Quick Fix or Full Development

Determine if this is a Quick Fix or full Development task:

- **Quick Fix triggers**: User says "quick fix", "小改动", "快速修一下"; or the change is obviously small (single file, config tweak, typo)
- **AI validation is mandatory** — see `references/policy.md` § Quick Fix mode for the autonomous validation rules. If any check fails, reject Quick Fix and explain why.

If Quick Fix:
```
3. Make the change
4. Run related tests
5. Write one-line QF entry to DEVLOG.md (see dev-log-protocol.md)
6. Done
```

If full Development, continue to step 3.

#### Full Development (steps 3–13)

3. Inspect the relevant docs, nearby code, and project memory (`docs/main/memory/`)
4. State the constraint or design choice that matters
5. **Create TASK_STATE.md** — write the initial checkpoint with goal, progress checklist, and working context (see `references/doc-structure.md` § TASK_STATE.md)
6. Make the smallest viable implementation
7. **Update TASK_STATE.md** — after each significant step, update the progress checklist and working context
8. Add or update tests
9. Update the relevant docs in `docs/main/` and `USAGE.md` if applicable
10. **Validate consistency** — cross-check `docs/main/*.md` (excl. memory/) + `USAGE.md` for terminology drift or conflicts (see `references/policy.md` § Doc consistency check)
11. **Write a dev log round** — append to `docs/dep/DEVLOG.md` (see `references/dev-log-protocol.md`)
12. **Delete TASK_STATE.md** — task is complete, checkpoint is no longer needed
13. Update context memory if new decisions, facts, or user preferences emerged
14. **Output discipline** — verbosity scales with change size (see `references/policy.md` § Output discipline)

### Review
1. **Determine scope** — parse the user's request to identify time range, module, or "all" (see `references/review-protocol.md` § Scope determination). Default: all entries since last review
2. Read dev log entries within scope (use layered reading — current month + archives as needed)
3. Run `git log --oneline --since=<scope start date>` and cross-check against dev log claims
4. Inspect the relevant docs in `docs/main/` and the actual code
5. Perform **Quick Review** — output 3-5 bullet points + cross-check verdict (include git/dev-log mismatches if found)
6. Ask the user: "需要我生成完整的审查报告到 `docs/dep/REVIEWS.md` 吗？"
7. Only if the user confirms, append a Full Report to `docs/dep/REVIEWS.md` (see `references/review-protocol.md`)
8. Link back to prior related reviews if any

### Deployment
1. Check if `docs/deploy/DEPLOY_GUIDE.md` exists; if not, create from skeleton
2. Identify the project's deployment target(s): environments, platforms, services
3. Write or update the deployment guide with: Environments, Prerequisites, Step-by-step, Configuration, Rollback, Verification
4. Keep the guide in sync when deployment-relevant code changes (config files, CI scripts, env vars)
