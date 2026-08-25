---
name: personal-assistant
description: "Development copilot and planning router for repositories with or without an adopted document system. Use whenever the user wants to plan a feature, change code, fix bugs, add tests, refactor modules, reconcile docs with implementation, review or audit code, summarize changes, deploy or ship code, or work in a project that uses PROJECT_GUIDE.md, PROJECT_SPEC.md, CODE_STYLE.md, and TEST_GUIDE.md."
---

# Personal Assistant

Use this skill for small to medium engineering tasks in any codebase where documentation, tests, implementation, and project memory need to stay aligned.

## Document system

See `references/doc-structure.md` for the complete document tree, naming conventions, and per-file write rules.

## Reference authority

| Reference | Authoritative for |
|-----------|-------------------|
| `doc-structure.md` | All file paths, naming rules, directory layout, TASK_STATE.md lifecycle, DEVLOG storage rules |
| `project-contract.md` | Document relationships, bootstrap rules, doc sync rules |
| `policy.md` | Tests, fix quality, doc consistency, output discipline, conflict handling, language guidance |
| `dev-log-protocol.md` | DEVLOG entrypoint/index/active/archive/summary format, round counter, layered reading, when/how to write dev log entries |
| `review-protocol.md` | Scope determination, Quick Review and Full Report workflow, REVIEWS.md format, layered reading |
| `planning-protocol.md` | Three-tier planning system, brainstorming protocol, sub-plan specification, insert-during-execution protocol, execution-phase Phase-Gate |
| `context-memory.md` | Cross-platform memory system, memory vs TASK_STATE vs DEVLOG relationship |

## Modes

This skill routes tasks into one of six modes:

| Mode | Trigger | What happens |
|------|---------|--------------|
| **Bootstrap** | User explicitly asks to initialize/adopt the document system | Generate minimal doc skeleton + USAGE.md, then proceed |
| **Consultation** | "what is", "how does", "explain", "find" — read-only | Read docs + code, answer, no edits |
| **Planning** | "帮我规划", "先想清楚再做", "plan this", "设计一下方案" | Route formal design to `sub-brainstorm`; keep lightweight planning local; then enter Development only after approval |
| **Development** | "fix", "add", "change", "refactor", "implement" | Classify Quick Fix first → implement/test → maintain only already-adopted docs and tracking |
| **Review** | "review", "audit", "检查", "审核", "inspect" | Determine scope → Quick Review first; ask if Full Report needed |
| **Deployment** | "deploy", "部署", "上线", "发布", "ship" | Generate or update deployment guide in `docs/deploy/DEPLOY_GUIDE.md` |

### Mode selection

1. If the user explicitly asks to initialize/adopt project documentation → **Bootstrap**
2. If the request mentions deployment → **Deployment**
3. If the request is read-only (asking questions, understanding code) → **Consultation**
4. If the request asks for planning / design before implementation → **Planning**
5. If the request asks for a review/audit/inspection → **Review**
6. If the request asks to change something → **Development**, then classify Quick Fix before any documentation setup

Missing `docs/main/` is repository state, not a Bootstrap trigger. Consultation, Quick Fix, Review, and Deployment must not create the canonical document skeleton merely because it is absent. See `references/project-contract.md` for adoption rules.

## Quick start by mode

### Bootstrap
1. Enter only when the user explicitly requests documentation initialization/adoption, or explicitly accepts a Bootstrap proposal
2. Check which canonical documents already exist
3. Generate only missing skeleton files (outline only, no speculative content)
4. Generate `USAGE.md` at project root: quick start, detected prerequisites, common commands (TBD where unknown)
5. Create `docs/dep/` and `docs/deploy/` directories
6. Tell the user what was created and ask them to fill in project-specific details later
7. Proceed with the original request in the appropriate mode

See `references/project-contract.md` for bootstrap rules.

### Consultation
1. Read relevant docs and project memory
2. Inspect nearby code as needed
3. Answer the question concisely — no code changes, no doc updates
4. If the answer reveals important context, optionally save it to memory

### Planning

Planning uses a three-tier system: `docs/dep/PLAN.md` (dashboard) → `docs/dep/plans/<lifecycle>/P<phase>-<name>.md` (contract) → `docs/dep/TASK_STATE.md` (execution). See `references/planning-protocol.md` for the complete protocol.

**Route to the right planning mode:**

| 场景 | 模式 | 处理者 | 输出 |
|------|------|--------|------|
| 全新功能模块 / 新技术栈 / 大重构 | 正式头脑风暴 | `sub-brainstorm` | 子计划文件 |
| 复杂或设计稿驱动的 UI | 正式头脑风暴 | `sub-brainstorm` | UI 合同型子计划 |
| 存在多个重要方案或需求/证据/验收边界不明确 | 正式头脑风暴 | `sub-brainstorm` | 子计划文件 |
| 已有模块加小功能，1-2 个 Phase 且无架构决策 | 轻量讨论 | `personal-assistant` | 子计划文件 |
| Review 阻断型 bug | P0 前置修复 | `personal-assistant` | `docs/dep/plans/ongoing/P0-<desc>.md` 或 `docs/dep/plans/backlog/P0-<desc>.md` |
| Review 非阻断技术债务 | P0 技术债务池 | `personal-assistant` | `docs/dep/plans/backlog/P0-tech-debt.md` |
| Bug 修复（原因已知） | 跳过规划 | `personal-assistant` | Development；已采用跟踪时使用 TASK_STATE.md |
| Bug 修复（原因不明） | 跳过规划 | `personal-assistant` | Development 调查；已采用跟踪时使用 TASK_STATE.md |
| 配置调整 / 明确的性能优化 | 跳过规划 | `personal-assistant` | Development；不因缺文档而 Bootstrap |

**Formal planning delegation:**

1. Inspect `docs/main/`, existing plans, and relevant code enough to classify the request and detect filename/phase conflicts.
2. Load and follow the installed `sub-brainstorm` skill in **delegated mode**. This is skill routing in the current agent, not subagent spawning.
3. Pass a delegation context packet containing the user request, known constraints, relevant doc/code paths, existing plan inventory, suggested phase index/path, UI flag, and caller=`personal-assistant`.
4. Suspend this skill's local Storm-R1 → R4 and all sub-plan/PLAN writes while delegated. `sub-brainstorm` is the only writer for the new sub-plan and its PLAN registration.
5. Handle the returned status:
   - `approved-written` + `plan_registered: yes`: verify both files exist and agree, then ask whether to enter Development.
   - `cancelled`: make no planning writes and remain in Planning.
   - `blocked`: report the blocker and do not enter Development.
6. Never repeat design approval, recreate the sub-plan, or register the same PLAN row after a successful return.

If `sub-brainstorm` is unavailable, state that formal delegation is unavailable and use the fallback Storm-R1 → R4 in `references/planning-protocol.md`. Mark this as fallback behavior; do not silently pretend delegation occurred.

**轻量讨论 (已有模块加功能):**

1. AI 简要说明实现思路（1-2 句）
2. 如果一种做法 → 直接确认；如果多种 → 列选项让用户选
3. 确认后直接进入 Phase 细化（跳过方案对比和范围确认）
4. 写入子计划文件，注册到 PLAN.md

Do not delegate lightweight planning merely because `sub-brainstorm` is installed.

**子计划完成与 PLAN.md 移除:**

1. 全部 Phase 完成 + 测试通过 + Review 通过（如有）
2. 按 `syncs_to` 清单同步到主文档（PROJECT_SPEC / PROJECT_GUIDE / TEST_GUIDE / CODE_STYLE，按实际影响）
3. 关键决策保存到 `docs/main/memory/`
4. 子计划文件移动到 `docs/dep/plans/complete/`（持久设计记录）
5. PLAN.md 将指针从"进行中"移到"最近完成"（只保留最近 3 条完成指针，完整历史在 `plans/complete/`）

### Development

#### Step 0: Route to Quick Fix or Full Development

Classify the requested change before Bootstrap, DEVLOG adoption, TASK_STATE creation, or other documentation writes.

- **Quick Fix triggers**: User says "quick fix", "小改动", "快速修一下"; or the change is obviously small (single file, local behavior, typo)
- **AI validation is mandatory** — see `references/policy.md` § Quick Fix mode. If any check fails, upgrade to full Development and explain why.

If Quick Fix:
```
1. Make the change
2. Run related tests if available
3. If DEVLOG tracking already exists, write one-line QF entry and INDEX row
4. If DEVLOG tracking does not exist, do not create docs/main, docs/dep, DEVLOG, TASK_STATE, or USAGE.md
5. Done
```

If full Development, continue below. Do not auto-Bootstrap solely because project docs are absent.

#### Step 1: Check interrupt checkpoint

1. If `docs/dep/TASK_STATE.md` exists, read it
2. **Expiry check** — if an active DEVLOG exists, compare TASK_STATE.md `updated` time with its last round time:
   - If DEVLOG last round time >= TASK_STATE.updated → the task may have already completed and TASK_STATE is a stale leftover
   - Prompt: "TASK_STATE.md 显示任务在 [updated time] 中断，但 DEVLOG 显示 [last round time] 已有完成记录。这个任务是否已完成？我可以清理 TASK_STATE.md。"
   - If user confirms → delete TASK_STATE.md, proceed as new task
   - If user says no → treat as genuine interrupt, proceed with resume
3. If TASK_STATE is valid (not expired), present the in-progress task(s) to the user
4. Ask: "发现未完成的任务：[Goal]。继续还是开始新任务？"
5. If user continues, use the checkpoint's `Resume From` as the starting point
6. If no TASK_STATE.md exists, proceed to step 2

#### Step 2: Check for unfinished tracked work

If old root-level DEVLOG files exist, apply DEVLOG legacy adoption before writing a new tracked round. If modern DEVLOG tracking exists, read its entrypoint and active last round. If neither exists, skip DEVLOG setup without creating it. When the tracked last round has open `Next` items not covered by TASK_STATE.md, ask whether to continue them.

#### Full Development (steps 3–16)

3. Inspect available relevant docs, nearby code, and existing project memory
4. State the constraint or design choice that matters
5. **Phase-Gate check (if sub-plan exists)** — before starting work, verify current Phase:
   - Read the active sub-plan file (`docs/dep/plans/ongoing/P<phase>-<name>.md`) current Phase's input conditions, completion criteria, and boundaries
   - If previous Phase has unchecked completion criteria → flag and ask user before proceeding
   - If TASK_STATE.md exists from previous session, verify its Goal matches the current sub-plan Phase
   - If current request would cross Phase boundaries → flag and ask user
6. **Create TASK_STATE.md when tracking is adopted** — if `docs/dep/` planning/tracking artifacts already exist, write the checkpoint described in `references/doc-structure.md`. Otherwise do not create documentation artifacts solely for execution tracking.
7. Make the smallest viable implementation
8. **Update TASK_STATE.md if created** — after each significant step, update the progress checklist and working context
9. Add or update tests
10. Update existing relevant docs and `USAGE.md` if applicable; do not create the canonical skeleton as a side effect
11. **Validate consistency when the document system exists** — cross-check existing canonical docs and `USAGE.md`; if the user requested a docs consistency review but docs are absent, report that the check is unavailable
12. **Phase-Gate validation (if sub-plan exists)** — when TASK_STATE.md items are all checked:
    - Verify each completion criterion in the sub-plan file for the current Phase
    - Check for boundary violations (did we do things the Phase explicitly excluded?)
    - For UI Phases, cross-check the design baseline, UI contract matrix, implementation, behavior tests, and deviation approvals; passing tests alone is insufficient
    - For UI Phases, verify default/loading/empty/error/partial/narrow states and reject display values without a declared data source
    - Review "执行中发现" entries and classify new ones as 阻断/增强/延后 (see `references/planning-protocol.md` § 执行中发现)
    - All pass + no violations → check off completion criteria in sub-plan, update Phase overview, update PLAN.md dashboard
    - Failures → fix gaps before proceeding. Do not start next Phase.
    - Boundary violation → flag and ask user: expand this Phase's scope, or defer to later Phase?
13. **Write a dev log round when DEVLOG tracking exists** — append to the active batch and INDEX. Do not initialize DEVLOG solely because Development ran.
14. **Delete TASK_STATE.md if created** — task/phase is complete, checkpoint is no longer needed
15. Update existing context memory if new durable decisions, facts, or user preferences emerged
16. **Output discipline** — verbosity scales with change size (see `references/policy.md` § Output discipline)

### Review
1. **Determine scope** — parse the user's request to identify time range, module, or "all" (see `references/review-protocol.md` § Scope determination). Default: all entries since last review
2. If DEVLOG tracking exists, read rounds within scope using layered reading. If it does not exist, continue with Git/code evidence and state that DEVLOG cross-checking is unavailable; do not create tracking files.
3. Run `git log --oneline --since=<scope start date>` and cross-check against dev log claims
4. Inspect existing relevant docs and actual code. If document consistency was requested but no project docs exist, report that part as unavailable rather than bootstrapping.
5. Perform **Quick Review** — output 3-5 bullet points + cross-check verdict (include git/dev-log mismatches if found)
6. Ask the user: "需要我生成完整的审查报告到 `docs/dep/REVIEWS.md` 吗？"
7. Only if the user confirms, append a Full Report to `docs/dep/REVIEWS.md` (see `references/review-protocol.md`)
8. Link back to prior related reviews if any

### Deployment
1. Check if `docs/deploy/DEPLOY_GUIDE.md` exists; if not, create from skeleton
2. Identify the project's deployment target(s): environments, platforms, services
3. Write or update the deployment guide with: Environments, Prerequisites, Step-by-step, Configuration, Rollback, Verification
4. Keep the guide in sync when deployment-relevant code changes (config files, CI scripts, env vars)
