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
    │   ├── PLAN.md                 # 主线仪表盘（仅活跃项 + 最近完成 + 延后）
    │   ├── plans/                  # 子计划目录（持久文件，完成后不移除）
    │   │   ├── user-auth.md        # 每个功能/模块的完整 Phase-Gate 实施方案
    │   │   └── ...
    │   ├── DEVLOG-R001-R040.md     # Current batch (active, append-only, up to 40 rounds)
    │   ├── DEVLOG-R041-R080.md     # Completed batches (read-only archives)
    │   ├── REVIEWS.md              # Review reports (single file, append-only)
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
| `PLAN.md` | Planning / Development | When any sub-plan is active | 仪表盘，只存指针和状态。子计划完成后移除指针 |
| `plans/<name>.md` | Planning | When a new feature/module/refactor is planned | 持久文件，完成后不移除。是该功能的设计决策记录 |
| `DEVLOG-RXXX-RXXX.md` | Development (mandatory) | After each completed round; append-only | Active until 40 rounds filled, then sealed |
| `REVIEWS.md` | Review (on demand) | Only after user confirms Full Report; append-only | Permanent, no rotation |
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
| `PLAN.md` | 主线仪表盘。仅存指针和状态（进行中/待开始/最近完成/延后）。不存 Phase 细节。 |
| `plans/<name>.md` | 子计划文件。kebab-case 命名，与功能名对应（如 `user-auth.md`）。持久保留，完成后不移除。 |
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

## 三层计划体系

```
PLAN.md             → 仪表盘层：只看"正在发生什么"，完成即移除指针
docs/dep/plans/<name>.md → 合同层：每个功能/模块的完整 Phase-Gate 实施方案
TASK_STATE.md       → 执行层：当前 Phase 内的单步进度
```

---

## PLAN.md — 主线仪表盘

PLAN.md 是仪表盘，不是实施文档。它只包含指向子计划的指针、状态和优先级，不包含任何 Phase 的实施细节。Phase 细节全部在 `plans/<name>.md` 中。

### 格式

```markdown
---
updated: YYYY-MM-DD
---

# 项目计划

## 进行中
| 子计划 | 文件 | 当前 Phase | 已用轮次 | 开始日期 |
|--------|------|-----------|---------|---------|
| 用户认证 | [plans/user-auth.md](plans/user-auth.md) | P2: 注册/登录 API | R004-R006 | YYYY-MM-DD |

## 待开始
| 优先级 | 子计划 | 文件 | 预估总轮次 | 依赖 |
|--------|--------|------|----------|------|
| 1 | 管理后台 | [plans/admin-panel.md](plans/admin-panel.md) | 5-8 | 用户认证 P3 完成 |
| 2 | 数据导出 | [plans/data-export.md](plans/data-export.md) | 3-5 | - |

## 最近完成
> 仅保留最近 3 条。更早的直接移除。

| 日期 | 子计划 | 已同步到 |
|------|--------|---------|
| YYYY-MM-DD | 数据库迁移框架 | PROJECT_GUIDE, PROJECT_SPEC |

## 延后
- OAuth 第三方登录 → 下个计划周期再评估
```

### 维护规则

- **进行中**：每个活跃子计划一行。当前 Phase 和已用轮次在每次 Gate 通过后更新
- **待开始**：按优先级降序排列。新子计划注册时插入到正确位置
- **最近完成**：保留最近 3 条。超过的直接删除——内容已在子计划文件 + 主文档 + DEVLOG 中
- **延后**：不需要立即处理的需求。下个计划周期时作为输入
- **状态一致性**：PLAN.md "进行中"的当前 Phase 必须与子计划文件的 Phase 总览一致

---

## plans/<name>.md — 子计划合同

子计划文件是某个功能/模块的完整实施方案。它是持久文件，完成后不移除、不归档——是功能的设计决策记录。

### 文件命名

kebab-case，与功能名对应：`user-auth.md`、`admin-panel.md`、`frontend-redesign.md`

### 何时独立建子计划 vs 合并

```
独立建子计划：
  - 预估 ≥ 2 个 Phase
  - 涉及 ≥ 3 个文件
  - 跨模块改动
  - 需要头脑风暴的

合并到已有子计划：
  - 改动属于同一模块
  - 已有子计划还在 planning 或 in-progress
  - 新需求不改变已有子计划的核心目标

不建子计划（直接用 TASK_STATE.md）：
  - 单 Phase 内可完成
  - 预估 1-2 个 DEVLOG 轮次
  - Bug 修复（原因已知）
  - 不需要头脑风暴
```

### 格式

```markdown
---
status: planning | in-progress | done
created: YYYY-MM-DD
updated: YYYY-MM-DD
priority: 1
estimated_rounds: 4-8
depends_on: []
syncs_to:
  - PROJECT_SPEC.md
  - PROJECT_GUIDE.md
---

# [功能/模块名称]

## 目标
[一句话 — 要构建什么，为什么]

## 背景
- 当前状态：[现在怎么做 / 没有做什么]
- 约束：[技术约束、时间约束]
- 方案来源：[正式头脑风暴 / 轻量讨论 / 已有明确需求]

## 涉及范围
- **包含**：[明确要做的事]
- **不包含**：[明确不做的事]

## 主文档影响
完成后需要更新：
- `PROJECT_SPEC.md`：[具体章节]
- `PROJECT_GUIDE.md`：[具体章节]

---

## Phase 总览
| Phase | 目标 | 预估轮次 | 依赖 | 状态 |
|-------|------|---------|------|------|
| P1 | [一句话] | RXXX-RXXX | - | done |
| P2 | [一句话] | RXXX-RXXX | P1 | in-progress |
| P3 | [一句话] | RXXX-RXXX | P2 | pending |

---

## P1: [Phase 名称]

### 输入条件
- [开始本 Phase 前必须为真的条件]

### 产出
- [具体的、可验证的交付物]

### 完成标准
- [ ] [可客观验证的标准，至少 3 条]

### 边界（本 Phase 明确不做）
- [防止 AI 在执行中越界，至少 2 条]

### 涉及文件
| 文件 | 操作 | 预计行数 |
|------|------|---------|
| `path/to/file.py` | 新建 | ~40 |
| `path/to/other.py` | 修改 | +5 |

### 关键决策
- [本 Phase 的技术选择]：[选项 A / 选项 B]，选择 [X]，理由：[具体理由]
- 如果没有决策点，写"无"

---

## P2: [Phase 名称]
[... 同上 ...]

---

## 执行中发现
| ID | 描述 | 发现于 | 类型 | 处理 |
|----|------|--------|------|------|
| D1 | [问题描述] | P2 | 阻断 | → 新增 P4 |

## 关键决策记录
| 日期 | 决策 | 选项 | 选择 | 理由 |
|------|------|------|------|------|
| YYYY-MM-DD | [具体决策] | [A / B] | [X] | [理由] |
```

### UI 类 Phase 额外要求

UI 类 Phase 细化时必须包含：
- **涉及页面/组件**：列出所有新建和复用的 UI 文件
- **组件树**：ASCII 树形图展示组件嵌套关系
- **状态矩阵**：初始 / 提交中 / 成功 / 错误 / 空数据 / 网络错误 — 每个状态的触发条件和 UI 表现
- **交互流**：用户操作 → 系统响应 → 状态变更的完整链路
- **不做**：明确排除的 UI 细节（动画、响应式、暗色模式等）

### 生命周期

```
头脑风暴/轻量讨论 → 创建 plans/<name>.md，status: planning
用户确认 Phase 拆解 → status 改为 in-progress
Phase 推进 → Gate 时勾选完成标准，更新 Phase 总览
全部 Phase 完成 → 验证 → 同步主文档 → status 改为 done
  子计划文件保留在 plans/ 目录，不移除
  PLAN.md 将指针从"进行中"移到"最近完成"
```

### 与 PLAN.md 的关系

PLAN.md 只存指向子计划的指针（文件名、当前 Phase、状态、优先级）。子计划的 Phase 细节、完成标准、边界、决策全部在子计划文件内。PLAN.md "进行中"行的当前 Phase 必须与子计划的 Phase 总览状态一致。

---

## TASK_STATE.md — 与子计划的关联

当存在子计划时，TASK_STATE.md 的 Goal 和 Phase Context 必须引用子计划：

```markdown
## Goal
P2 — 实现注册/登录 API（子计划：plans/user-auth.md）

## Phase Context
- **输入条件**：[引用子计划中 P2 的输入条件]
- **完成标准**：[引用子计划中 P2 的完成标准]
- **边界**：[引用子计划中 P2 的边界]
```

## DEVLOG — 子计划和 Phase 标注

当存在子计划时，DEVLOG 轮次标题同时标注子计划和 Phase：

```markdown
### R007 [14:30] [user-auth] P2: 实现 POST /api/auth/register
```

无子计划时（单 Phase 的 bug 修复等）省略子计划标注：

```markdown
### R007 [14:30] 修复登录超时问题
```

## Phase-Gate 验证

当前 Phase 所有 TASK_STATE 项完成时：
1. 逐条检查子计划中该 Phase 的完成标准
2. 检查是否有越界改动（做了边界中排除的内容）
3. 检查"执行中发现"是否有新条目需要分类
4. 全部通过 → 勾选完成标准，更新子计划 Phase 总览和 PLAN.md
5. 有未通过 → 补齐缺口，不进入下一 Phase
6. 有越界 → 标记并询问用户
7. 有新发现 → 分类为阻断/增强/延后，按 `references/planning-protocol.md` § 执行中发现处理
