# Document structure

Authoritative reference for all document paths and naming conventions.

## Directory tree

```
<project-root>/
├── USAGE.md                        # Quick start, prerequisites, common commands

└── docs/
    ├── main/                       # Blueprint — describes "what it IS"
    │   ├── PROJECT_GUIDE.md        # Architecture, module responsibilities, data flow
    │   ├── PROJECT_SPEC.md         # Technical scope, design decisions, feature boundaries
    │   ├── CODE_STYLE.md           # Naming, formatting, style conventions
    │   ├── TEST_GUIDE.md           # Test layout, regression coverage, entry points
    │   └── memory/                 # Cross-platform project memory (see context-memory.md)
    │       ├── MEMORY.md           # Memory index (always read first)
    │       └── <type>-<topic>.md   # Memory entries
    │
    ├── dep/                        # Diary — records "what was DONE"
    │   ├── DEVLOG-R001-R040.md     # Current batch (active, append-only, up to 40 rounds)
    │   ├── DEVLOG-R041-R080.md     # Completed batches (read-only archives)
    │   ├── REVIEWS.md              # Review reports (single file, append-only)
    │   ├── PLAN.md                 # Living project plan (optional)
    │   └── TASK_STATE.md           # Interrupt checkpoint (exists only when task is in-progress)
    │
    └── deploy/                     # Deployment — describes "HOW to deploy"
        └── DEPLOY_GUIDE.md        # Environments, steps, config, rollback
```

## File reference

### USAGE.md

| Writes | When | Format |
|--------|------|--------|
| Bootstrap / Development | Bootstrap auto-generates; dev mode updates as project evolves | Quick start, prerequisites, common commands, FAQ |

### docs/main/ — Blueprint

| File | Writes | When |
|------|--------|------|
| `PROJECT_GUIDE.md` | Bootstrap / Development | Bootstrap auto-generates; dev mode updates when architecture changes |
| `PROJECT_SPEC.md` | Bootstrap / Development | Bootstrap generates TBD placeholder; fills in over time |
| `CODE_STYLE.md` | Bootstrap / Development | Bootstrap generates TBD placeholder; fills in as conventions emerge |
| `TEST_GUIDE.md` | Bootstrap / Development | Bootstrap generates TBD placeholder; updates when test layout changes |
| `memory/MEMORY.md` | Bootstrap / Context update | Bootstrap creates empty; updated when a memory file is added/removed |
| `memory/<type>-<topic>.md` | Development / Consultation | When decisions, preferences, or project facts emerge |

### docs/dep/ — Diary

| File | Writes | When | Lifecycle |
|------|--------|------|-----------|
| `DEVLOG-RXXX-RXXX.md` | Development (mandatory) | After each completed round; append-only | Active until 40 rounds filled, then sealed |
| `REVIEWS.md` | Review (on demand) | Only after user confirms Full Report; append-only | Permanent, no rotation |
| `PLAN.md` | Development (optional) | When a multi-step plan is needed | Overwritten when plan evolves |
| `TASK_STATE.md` | Development | Created when task starts; updated at checkpoints; deleted when task completes | Exists only during active work |

### docs/deploy/ — Deployment

| File | Writes | When |
|------|--------|------|
| `DEPLOY_GUIDE.md` | Deployment / Development | Bootstrap generates TBD placeholder; filled in when deploying or when deployment-relevant code changes |

## Naming rules

| Pattern | Rule |
|---------|------|
| `USAGE.md` | Root level. Auto-generated at bootstrap. |
| `DEVLOG-R001-R040.md` | Round batch file. 40 rounds per batch. Global round numbering (R001, R002, ...). Naming: `DEVLOG-R001-R040.md`, `DEVLOG-R041-R080.md`, etc. |
| `REVIEWS.md` | Single file, append-only. Each entry: `## Review N [YYYY-MM-DD]` header. |
| `PLAN.md` | Living document, overwritten when plan evolves. |
| `TASK_STATE.md` | Checkpoint file. Exists only when a task is in-progress. Deleted on task completion. |
| `DEPLOY_GUIDE.md` | Persistent deployment guide. |
| `memory/<type>-<topic>.md` | `type` = `user` / `project` / `feedback` / `reference`. `topic` = short kebab-case. |

## DEVLOG round batches

DEVLOG uses 40-round batches to control file size. Each file holds exactly one batch.

### Batch rules

```
- One active file at a time: DEVLOG-RXXX-RXXX.md
- Each batch = 40 global rounds
- Batch 1: DEVLOG-R001-R040.md (global rounds R001–R040)
- Batch 2: DEVLOG-R041-R080.md (global rounds R041–R080)
- Batch N: DEVLOG-R((N-1)*40+1)-R(N*40).md
- When the active file reaches 40 rounds → seal it, create next batch file
- Sealed batches are read-only — never modify past batch files
- Round numbering is global and monotonic across batches
```

### Global round counter

Each round has a unique global identifier `RXXX` (e.g., R001, R042, R103). The counter is maintained by the active DEVLOG file:

```
Read the last round number from the active batch to determine the next value.
If no DEVLOG file exists, start at R001.
```

### Layered reading

To minimize token consumption, read DEVLOG files selectively:

| Layer | When to read | How |
|-------|-------------|-----|
| Active batch | Always in Development and Review modes | Full read |
| Previous batch (1 back) | Task resume references earlier round; review covers recent range | Full read |
| Older batches | User specifies older round range or date | Read only the relevant date sections |
| REVIEWS.md | Review mode | Last 3 reviews: full read. Older reviews: status line only |

### How to find the right batch

```
1. Determine the round number range needed (from scope)
2. Map to batch file: DEVLOG-RXXX-RXXX.md
3. Read from that file — only the relevant sections
```

## TASK_STATE.md — Interrupt checkpoint

TASK_STATE.md is a lightweight checkpoint file that enables cross-session task resumption.

### Lifecycle

```
Task starts       → Create TASK_STATE.md with status: in-progress
Task progresses   → Update checkpoint items ([x] / [ ]) and Working Context
Task interrupted  → TASK_STATE.md persists in repo (survives terminal/session switch)
New session starts → Step 0 in Development mode checks if TASK_STATE.md exists
Task completes    → Consolidate into DEVLOG batch round, delete TASK_STATE.md
```

### Format

```markdown
---
status: in-progress
created: YYYY-MM-DD HH:MM
updated: YYYY-MM-DD HH:MM
---

# Current Task

## Goal
[one-line description of what is being done]

## Progress
- [x] [completed step]
- [x] [completed step]
- [ ] [current/next step]
- [ ] [future step]

## Working Context
- **Files being edited**: [list of files]
- **Last command run**: [command] ([status])
- **Key decisions**: [decision + reference to docs/memory]
- **Blocker**: [description or "None"]

## Resume From
[explicit instruction for the next session: what to do, where to start]
```

### Multi-task support

If multiple tasks are interrupted simultaneously:

```markdown
## Task 1: [name]
status: in-progress
[checkpoint content]

## Task 2: [name]
status: blocked
[checkpoint content]
```

Priority: `in-progress` > `blocked`. Present both to user and let them choose.

## PLAN.md — Phase-Gate 项目计划

PLAN.md 是执行合同文件，不是愿望清单。它位于 TASK_STATE.md 之上，将多步骤工作拆解为有边界、有完成标准、可独立验证的 Phase。

### 层级关系

```
PLAN.md      = 战略 + 阶段合同（Phase map + 每个 Phase 的输入/产出/边界/完成标准）
TASK_STATE   = 当前 Phase 内的进度追踪（Goal 引用当前 Phase）
DEVLOG.md    = 执行记录（每轮标题标注所属 Phase）
```

### 何时使用

- 用户说"帮我规划一下"、"先想清楚再做"、"plan this out"、"设计一下方案"
- 任务预估超过 3 个 DEVLOG 轮次
- 多个相关功能需要排序
- 架构决策需要记录理由

### 规划流程

规划采用**多轮交互模式**，不是一次性生成。详细流程见 `references/planning-protocol.md`。

```
第 1 轮：目标与范围确认（包含明确的排除项）
第 2 轮：Phase 拆解（概要 — 每个 Phase 一句话目标）
第 3 轮：逐 Phase 细化（输入条件、产出、完成标准、边界、涉及文件）
第 4 轮：最终确认，写入 PLAN.md，用户说"开始"后进入执行
```

### PLAN.md 格式（Phase-Gate 结构）

```markdown
---
status: planning | in-progress | done
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# [功能/项目名称]

## 目标
[一句话 — 要构建什么，为什么]

## 背景
[约束、依赖、相关文档]

## Phase 总览
| Phase | 目标 | 预估轮次 | 依赖 | 状态 |
|-------|------|---------|------|------|
| P1 | [一句话目标] | RXXX-RXXX | - | done |
| P2 | [一句话目标] | RXXX-RXXX | P1 | in-progress |
| P3 | [一句话目标] | RXXX-RXXX | P2 | pending |

## P1: [Phase 名称]

### 输入条件
- [开始本 Phase 前必须为真的条件]

### 产出
- [具体的、可验证的交付物]

### 完成标准
- [ ] [可客观验证的标准]
- [ ] [如有多条，逐条列出]

### 边界（本 Phase 明确不做）
- [防止 AI 在执行中越界的排除项]

### 涉及文件
- `path/to/file.py` — 新建/修改

### 关键决策
- [技术选择，需要用户拍板的事项]

## P2: [Phase 名称]
...
```

### UI 类 Phase 额外要求

UI 类 Phase 必须在细化时包含：
- **涉及页面/组件**：列出所有新建和复用的 UI 文件
- **组件树**：ASCII 树形图展示组件嵌套关系
- **状态矩阵**：初始/加载中/成功/错误/空/网络错误 等状态及其 UI 表现
- **交互流**：用户操作 → 系统响应 → 状态变更的完整链路
- **不做**：明确排除的 UI 细节（防止 AI 自行添加动画、样式等）

### 生命周期

```
规划阶段 → 创建 PLAN.md，status: planning
用户确认 → status 改为 in-progress，开始执行
Phase 推进 → 勾选完成标准，更新 Phase 总览状态行
全部完成 → status 改为 done，保留文件
新规划触发 → 直接覆盖（旧内容已同步到主文档和 DEVLOG）
```

### 覆盖规则

覆盖 PLAN.md 前，AI 必须确认：
1. 旧计划的产出已反映在 `PROJECT_SPEC.md` 或 `PROJECT_GUIDE.md`
2. 旧计划的执行记录已完整写入 DEVLOG
3. 旧计划中的关键决策已保存到项目记忆

三项全部就绪 → 覆盖。有缺失 → 先补齐再覆盖。

PLAN.md 是执行工具而非历史档案，不归档。计划的核心内容在执行中已同步到主文档（蓝图）和 DEVLOG（日记），保留旧计划会造成混淆。

### 何时不用

- 单次任务，1-2 轮内可完成 → 用 TASK_STATE.md 即可
- 任务已经清晰、定义明确 → 跳过规划，直接进入 Development
- 用户没要求规划且任务直接明了

### TASK_STATE.md 与 Phase 的关联

当 PLAN.md 存在时，TASK_STATE.md 必须引用当前 Phase：

```markdown
## Goal
P2 — 实现注册/登录 API（PLAN.md Phase 2）

## Phase Context
- **Phase 完成标准**：[引用 PLAN.md 中 P2 的完成标准]
- **Phase 边界**：[引用 PLAN.md 中 P2 的边界]
```

### DEVLOG 中的 Phase 标注

每轮 DEVLOG 标题必须标注所属 Phase：

```markdown
### R005 [14:30] — P2: 实现 POST /api/auth/register
```

### Phase-Gate 验证

当前 Phase 所有 TASK_STATE 项完成时：
1. 逐条检查 PLAN.md 中该 Phase 的完成标准
2. 检查是否越界（做了边界中排除的内容）
3. 全部通过 → 勾选完成标准，更新 Phase 总览，进入下一 Phase
4. 有未通过 → 补齐缺口，不进入下一 Phase
5. 发现越界 → 标记并询问用户
