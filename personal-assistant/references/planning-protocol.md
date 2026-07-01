# Planning Protocol

三层计划体系、头脑风暴流程、Phase-indexed 子计划命名、执行期 Phase-Gate 的唯一权威。

## 概述与定位

Planning Protocol 解决的是“复杂任务如何从讨论变成可执行合同，再落到单轮开发”的问题。它把长期意图、阶段合同和当前执行状态拆开，避免 PLAN.md 变成实施细节堆积，也避免 TASK_STATE.md 承担架构决策记录。

三层体系的目标：

- **PLAN.md**：告诉读者现在什么在进行、什么排队、什么刚完成。
- **plans/<lifecycle>/Pn-name.md**：保存某个功能、修复或重构的完整 Phase-Gate 合同，并用目录表示生命周期。
- **TASK_STATE.md**：只记录当前 Phase 的短期执行进度和恢复点。

## 目录

- [概述与定位](#概述与定位)
- [三层计划体系](#三层计划体系)
- [子计划命名规范](#子计划命名规范)
- [子计划文件模板](#子计划文件模板)
- [PLAN.md 仪表盘模板](#planmd-仪表盘模板)
- [规划触发与决策](#规划触发与决策)
- [技能委派与返回合同](#技能委派与返回合同)
- [头脑风暴流程 (Storm-R1 → R4)](#头脑风暴流程-storm-r1--r4)
- [快速规划](#快速规划)
- [执行阶段](#执行阶段)
- [执行中发现与处理](#执行中发现与处理)
- [执行中插入新计划](#执行中插入新计划)
- [子计划完成与同步](#子计划完成与同步)
- [UI 类 Phase 额外要求](#ui-类-phase-额外要求)

## 三层计划体系

```
docs/dep/PLAN.md             -> 仪表盘层：活跃项、排队项、最近完成、延后项
docs/dep/plans/<lifecycle>/Pn-name.md -> 合同层：功能/修复/重构的 Phase-Gate 实施方案
docs/dep/TASK_STATE.md       -> 执行层：当前 Phase 内的单步进度与恢复点
```

目录结构、文件生命周期、TASK_STATE.md 格式见 `references/doc-structure.md`。本文件只定义规划行为、Phase-Gate 流程和子计划合同规则。

### 职责边界

| 信息 | PLAN.md | plans/<lifecycle>/Pn-name.md | TASK_STATE.md |
|------|:---:|:---:|:---:|
| 子计划名称和文件路径 | yes | - | 引用当前子计划 |
| 当前 Phase 和状态 | yes | yes | yes |
| 子计划排序 | yes | `phase_index` + `priority` | - |
| 子计划间依赖 | yes | `depends_on` | - |
| 预估总轮次 | yes | `estimated_rounds` | - |
| 最近完成记录 | yes | - | - |
| 延后清单 | yes | 可引用 | - |
| 目标、背景、范围边界 | - | yes | 当前 Phase 摘要 |
| 主文档影响 `syncs_to` | - | yes | - |
| Phase 输入、产出、完成标准、边界 | - | yes | 当前 Phase 引用 |
| 关键决策记录 | - | yes | 可引用 |
| 执行中发现 | - | yes | 当前发现可临时记录 |

## 子计划命名规范

子计划文件使用 Phase-indexed 命名：

```
docs/dep/plans/<lifecycle>/P<phase>-<name>.md
```

示例：

| 前缀 | 含义 | 示例 |
|------|------|------|
| `P0-` | Review 后发现的前置修复或技术债务。阻断型 bug 必须在当前阶段开始前完成 | `P0-fix-auth-race.md` |
| `P1-` | 项目第一个执行阶段 | `P1-user-auth.md` |
| `P2-` | 项目第二个执行阶段 | `P2-admin-panel.md` |
| `P3-` | 项目第三个执行阶段 | `P3-data-export.md` |

### 命名规则

- `P0` 可随时插入：Review 发现阻断型 bug -> 创建独立 `P0-<desc>.md` -> 放入 `plans/backlog/` 最高位，或在接受为立即修复时放入 `plans/ongoing/`。
- Review 发现的非阻断技术债务统一写入 `plans/backlog/P0-tech-debt.md`，单个文件内部按 Phase 或条目区分。
- 不再使用旧的固定“技术债修复”文件名；统一进入 `P0-*.md` 命名体系。
- `P1+` 表示执行先后，不表示功能重要度。
- 编号不连续可以接受；不要为了插入新计划而重编号已有子计划。
- 一个功能可以跨多个编号，例如 `P1-user-auth-model.md` 与 `P3-user-auth-api.md`。
- `<name>` 使用 kebab-case，描述具体目标，避免过宽泛的 `misc`、`cleanup`。
- 关键词分类写入 frontmatter `tags`，不要创建 `plans/auth/`、`plans/api/` 这类关键词目录。

### 生命周期目录

| 目录 | `status` | 含义 |
|------|----------|------|
| `plans/ongoing/` | `in-progress` | 当前正在执行的计划，或已接受为立即修复的 P0 阻断项 |
| `plans/backlog/` | `planning` | 已确认但未开始的计划；`P0-tech-debt.md` 长期位于这里 |
| `plans/complete/` | `done` | 已完成、验证并同步主文档的历史计划 |
| `plans/deferred/` | `deferred` | 明确延后，不进入当前计划周期 |

目录和 frontmatter `status` 必须一致。计划推进时通过移动文件表达生命周期变化：

```
plans/backlog/P2-admin-panel.md  -> plans/ongoing/P2-admin-panel.md
plans/ongoing/P2-admin-panel.md  -> plans/complete/P2-admin-panel.md
plans/backlog/P4-oauth-login.md  -> plans/deferred/P4-oauth-login.md
```

技术债规则：
- `plans/backlog/P0-tech-debt.md` 是滚动债务池，不视为正在执行。
- 阻断型债务创建独立 `P0-<desc>.md`。
- 当某批非阻断债务被选中处理时，从 `P0-tech-debt.md` 拆出独立执行计划，如 `plans/ongoing/P0-reduce-auth-flakiness.md`。

### Frontmatter 字段

```yaml
---
phase_index: 0
status: planning | in-progress | done | deferred
created: YYYY-MM-DD
updated: YYYY-MM-DD
priority: 1
estimated_rounds: 4-8
depends_on: []
tags: []
syncs_to:
  - PROJECT_SPEC.md
  - PROJECT_GUIDE.md
---
```

字段含义：

| 字段 | 规则 |
|------|------|
| `phase_index` | 文件名前缀的数字部分。`P0-fix-auth-race.md` 必须写 `0` |
| `status` | `planning`、`in-progress`、`done`、`deferred` 四选一，且必须与生命周期目录一致 |
| `priority` | 同一 `phase_index` 内排序，数字越小越优先 |
| `estimated_rounds` | 预估 DEVLOG 轮次范围 |
| `depends_on` | 依赖的其他子计划文件名，如 `["P1-user-auth.md"]` |
| `tags` | 关键词分类，如 `["auth", "api", "security"]`；用于检索，不用于目录分层 |
| `syncs_to` | 完成后必须同步的 `docs/main/` 主文档清单 |

### DEVLOG 标注映射

DEVLOG 使用子计划文件 stem 作为标注，保留 `P0/P1` 前缀，避免同名功能跨阶段时混淆：

```markdown
### R007 [14:30] [P1-user-auth] P2: 实现 POST /api/auth/register
### R008 [16:45] [P0-fix-auth-race] P1: 定位竞态根因
```

内部 Phase 仍使用 `P1`、`P2` 表示子计划内阶段。外层文件名前缀表示计划排序，DEVLOG 标题同时保留两者。

## 子计划文件模板

子计划模板只定义一次，位于 `templates/sub-plan.md.template`。创建子计划时复制该模板，并按生命周期保存为 `docs/dep/plans/<lifecycle>/P<phase>-<name>.md`。

模板必须包含：
- frontmatter 字段
- 目标、背景、范围
- 主文档影响，且写明同步到目标文档的具体章节
- Phase 总览
- 每个 Phase 的输入条件、产出、完成标准、边界、涉及文件、关键决策
- UI 子计划的设计基线、行为合同、状态与数据证据、偏差审批和验收断言
- 执行中发现
- 关键决策记录

UI 类 Phase 的额外要求见 [UI 类 Phase 额外要求](#ui-类-phase-额外要求)。

## PLAN.md 仪表盘模板

PLAN.md 模板只定义一次，位于 `templates/plan-dashboard.md.template`。PLAN.md 是仪表盘，不是实施文档，只存指针、状态和排序。

维护规则：
- **进行中**：指向 `plans/ongoing/`。每个活跃子计划一行。当前 Phase 和已用轮次在 Gate 通过后更新。
- **待开始**：指向 `plans/backlog/`。按 `phase_index` 升序、同编号内按 `priority` 升序排列。`P0` 位于最高优先级。
- **最近完成**：指向 `plans/complete/`。PLAN.md 仅保留最近 3 条完成指针，完整历史留在 `plans/complete/`。
- **延后**：指向 `plans/deferred/`，或记录尚未形成子计划的延后想法。
- **状态一致性**：PLAN.md 中当前 Phase 必须与子计划文件的 Phase 总览一致；子计划目录必须与 `status` 一致。

## 规划触发与决策

以下任一情况进入规划流程：

- 用户明确说“帮我规划一下”、“先想清楚再做”、“plan this out”、“设计一下方案”。
- 任务预估超过 3 个 DEVLOG 轮次。
- 涉及多个模块或功能，需要排序。
- 引入新技术栈或跨模块大重构。
- Review 发现阻断型 bug，需要插入 `P0` 前置修复。

### 决策矩阵

| 场景 | 子计划 | 头脑风暴 | 理由 |
|------|:---:|:---:|------|
| 全新功能模块 | 必须 | 必须 | 技术选型、架构影响需要用户拍板 |
| 引入新技术栈 | 必须 | 必须 | 迁移成本、长期维护需要评估 |
| 跨模块大重构 | 必须 | 必须 | 影响面大，方案需要用户确认 |
| Review 阻断型 bug | 必须，`ongoing/P0-<desc>.md` 或 `backlog/P0-<desc>.md` | 可轻量 | 必须显式进入计划队列 |
| Review 非阻断技术债务 | 必须，`backlog/P0-tech-debt.md` | 不需要 | 统一积压和老化追踪，但不占用 ongoing |
| 已有模块加小功能 | 可选 | 轻量 | 2-3 个选项快速确认即可 |
| Bug 修复（原因已知） | 不建 | 不需要 | 直接写 TASK_STATE.md |
| Bug 修复（原因不明） | 可选 | 不需要 | 调查本身可作为第一 Phase |
| 配置调整、性能优化 | 不建 | 不需要 | 改动范围明确 |

### 轻量讨论 vs 正式头脑风暴

轻量讨论适用于已有模块加功能、范围明确的小计划：

```
1. AI 列出推荐方案，必要时给出 1-2 个备选
2. 用户确认或选择
3. 将选择记录到子计划“关键决策”
4. 直接进入 Phase 细化
```

正式头脑风暴适用于新功能、新技术栈、大重构。

## 技能委派与返回合同

`personal-assistant` 是 Planning 模式的总路由，`sub-brainstorm` 是正式头脑风暴执行器。这里的委派表示当前代理加载并遵循另一个技能，不表示创建子代理或新线程。

### 委派判定

以下任一条件成立时必须委派给 `sub-brainstorm`：

- 全新功能或独立模块。
- 引入新技术栈。
- 跨模块大重构。
- 复杂或设计稿驱动的 UI。
- 存在两个以上重要可行方案。
- 需求、数据证据或验收边界不明确，需要多轮确认。

以下情况不委派：

- 已有模块的小功能，预计 1-2 个 Phase，且无架构决策。
- 已知原因的 bug 修复。
- P0 阻断修复或技术债登记。
- 配置调整或边界明确的性能优化。

不确定时，优先判断是否存在需要用户选择的重要设计决策；存在则委派。

### 委派上下文包

`personal-assistant` 在加载 `sub-brainstorm` 前提供：

```yaml
caller: personal-assistant
request: "[用户原始需求]"
known_constraints: []
relevant_paths: []
existing_plans: []
suggested_phase_index: N
suggested_sub_plan: docs/dep/plans/backlog/PN-name.md
ui_in_scope: true | false
```

- `suggested_phase_index` 和路径是建议值，`sub-brainstorm` 写入前必须再次检查冲突。
- 上下文只传递已验证事实；未知项保留为空，不得推测。
- 如果用户直接调用 `sub-brainstorm`，由它自行收集这些信息。

### 写入所有权

| 操作 | 正式委派期间的唯一责任方 |
|------|--------------------------|
| 需求澄清、方案比较、设计审批 | `sub-brainstorm` |
| 创建新子计划 | `sub-brainstorm` |
| 将新子计划注册到 PLAN.md | `sub-brainstorm` |
| 验证返回路径和 PLAN 指针一致 | `personal-assistant` |
| 询问是否进入 Development | `personal-assistant` |

委派开始后，`personal-assistant` 必须暂停本地 Storm 流程和规划写入。委派成功返回后不得重复审批、重建文件或重复注册 PLAN。

### 返回合同

`sub-brainstorm` 结束时必须返回：

```yaml
status: approved-written | cancelled | blocked
sub_plan: docs/dep/plans/backlog/PN-name.md | null
plan_registered: yes | no
decisions: []
unresolved: []
recommended_next: development | wait
```

处理规则：

- `approved-written` 只在设计已获用户批准、子计划已写入且 PLAN 已注册时使用；此时 `plan_registered` 必须为 `yes`。
- `cancelled` 表示用户未批准或终止讨论；不得创建子计划或 PLAN 行。
- `blocked` 表示模板缺失、路径冲突、文档矛盾或写入失败；不得进入 Development。
- 返回字段互相矛盾时按 `blocked` 处理。

### 降级路径

若 `sub-brainstorm` 未安装或不可读取：

1. `personal-assistant` 明确告知用户正式委派不可用。
2. 使用本协议的 Storm-R1 → R4 作为本地降级流程。
3. 按同一权威模板写入子计划并注册 PLAN。
4. 最终说明本次使用了 fallback，不得声称已委派。

## 头脑风暴流程 (Storm-R1 → R4)

头脑风暴是多轮交互的独立过程，不直接改动代码。以下步骤是 `sub-brainstorm` 的行为合同，也是技能不可用时 `personal-assistant` 的降级流程。输出最终成为子计划的背景、方案来源和 Phase 拆解。

### Storm-R1: 现状与目标确认

```
1. AI 阅读相关主文档和代码
2. 输出：
   - 当前状态：现在怎么做 / 没做什么
   - 目标：要达成什么
   - 约束：技术债、时间、团队能力等限制
3. 用户确认或修正
```

### Storm-R2: 方案对比

AI 必须提出至少两个可行方案：

|  | 方案 A | 方案 B |
|---|---|---|
| 概述 | 一句话 | 一句话 |
| 优势 | 列举 | 列举 |
| 劣势 | 列举 | 列举 |
| 复杂度 | 低/中/高 | 低/中/高 |
| 影响面 | 模块/文件 | 模块/文件 |
| 与现有架构匹配度 | 高/中/低 | 高/中/低 |
| 预估轮次 | N | N |

最后给出推荐方案和具体理由。用户选择后进入 Storm-R3。

### Storm-R3: 范围边界确认

输出：

```markdown
## 范围
- **包含**：[明确要做的事]
- **不包含**：[明确不做的事]
- **与已有子计划的边界**：[如有]

## 主文档影响
完成后需要更新：
- PROJECT_SPEC.md：[具体章节]
- PROJECT_GUIDE.md：[具体章节]
- TEST_GUIDE.md：[具体章节]
- CODE_STYLE.md：[如有新约定]

## 风险
- [风险]：[缓解措施]
```

`syncs_to` 必须与主文档模板章节对齐。主文档模板见 `templates/PROJECT_GUIDE.md.template`、`templates/PROJECT_SPEC.md.template`、`templates/CODE_STYLE.md.template`、`templates/TEST_GUIDE.md.template`。

如果范围包含 UI，Storm-R3 还必须确认：

- 设计基线来源（设计稿、截图、现有页面或文字需求）及其版本。
- 用户在首屏看到什么、可以操作什么，以及关键交互结果。
- 数据证据边界：每个指标、图表和分组对应的 payload 字段；缺少证据时如何显示。
- 允许偏离设计的审批方式。未经用户确认的偏差不能写成既定方案。

### Storm-R4: Phase 拆解初稿

```
AI 将范围拆解为 2-6 个 Phase：

| Phase | 目标 | 预估轮次 | 依赖 |
|-------|------|---------|------|
| P1 | ... | ... | - |
| P2 | ... | ... | P1 |

用户调整后确认。
```

确认后创建 `docs/dep/plans/backlog/P<phase>-<name>.md`，并在 PLAN.md 中注册。

## 快速规划

适用于 1-2 个 Phase 的小任务，跳过完整 Storm-R1 -> R4。

触发：
- 用户说“快速规划一下”、“简单列个计划”。
- AI 判断任务只需要 1-2 个 DEVLOG 轮次。
- 不涉及新技术或架构变更。

流程：

```
1. AI 直接提出目标 + Phase 拆解
2. 一轮确认
3. 写入子计划文件或直接写入 TASK_STATE.md
4. 在 PLAN.md 中注册（如建了子计划）
5. 即刻开始执行
```

快速规划不能跳过：
- 每个 Phase 的完成标准
- 每个 Phase 的边界
- 需要同步的主文档章节（如有）

## 执行阶段

### Phase-Gate 验证

当前 Phase 所有 TASK_STATE 项完成时：

```
1. 逐条检查子计划中该 Phase 的完成标准
2. 检查是否有越界改动
3. 检查“执行中发现”是否有新条目
4. 全部标准通过且无越界
   -> 勾选完成标准，更新子计划 Phase 总览
   -> 更新 PLAN.md
5. 有未通过标准
   -> 补齐缺口，不进入下一 Phase
6. 有越界改动
   -> 标记并询问用户：扩展当前 Phase，还是拆到后续 Phase
7. 有新的执行中发现
   -> 按“阻断/增强/延后”分类处理
```

UI 类 Phase 还必须执行 UI 专项 Gate：

```
1. 逐项核对设计基线、UI 合同矩阵、实际实现和测试断言
2. 覆盖默认、加载、空数据、错误、部分数据和窄屏状态
3. 验证每个展示值都有声明的数据来源；没有证据时按合同降级，不得临时推导
4. 核对偏差清单；仅接受已记录且已获用户确认的偏差
5. 行为测试和视觉核验均通过后，才能判定 UI Phase 完成
```

“测试通过”本身不是 UI Phase 的充分完成条件。测试若只断言标题或静态文本存在，而未覆盖合同中的核心操作与结果，Gate 必须失败。

### TASK_STATE.md 与子计划关联

当存在子计划时，TASK_STATE.md 必须引用子计划文件和内部 Phase：

```markdown
## Goal
P2 — 实现注册/登录 API（子计划：docs/dep/plans/ongoing/P1-user-auth.md）

## Phase Context
- **输入条件**：[引用子计划中 P2 的输入条件]
- **完成标准**：[引用子计划中 P2 的完成标准]
- **边界**：[引用子计划中 P2 的边界]
- **上一 Phase 状态**：P1 done — 数据模型已就绪
```

TASK_STATE.md 的完整格式由 `references/doc-structure.md` 定义。

### DEVLOG 标注规范

有子计划时：

```markdown
### R007 [14:30] [P1-user-auth] P2: 实现 POST /api/auth/register
```

无子计划时省略子计划标注：

```markdown
### R007 [14:30] 修复登录超时问题
```

完整 DEVLOG 格式由 `references/dev-log-protocol.md` 定义。

## 执行中发现与处理

开发过程中暴露的问题先记录到子计划的“执行中发现”区域，在每个 Phase Gate 时集中分类。

| 类型 | 定义 | 处理 |
|------|------|------|
| **阻断** | 不处理会导致后续 Phase 无法进行或产生大量返工 | 当前子计划内新增 Phase，或拆成独立 `plans/ongoing/P0-<desc>.md` |
| **增强** | 显著改善质量，与未开始 Phase 自然关联 | 合并到相关未开始 Phase 的完成标准或产出 |
| **延后** | 锦上添花，不影响核心目标 | 移入 PLAN.md “延后”区域 |

处理流程：

```
Phase Gate 时发现新的 D 条目：

1. AI 逐条判断类型
2. 阻断型：
   - 若属于当前子计划范围，新增 Phase 并更新依赖链
   - 若会阻塞其他计划或来自 Review，创建独立 `plans/ongoing/P0-<desc>.md` 或 `plans/backlog/P0-<desc>.md`
3. 增强型：
   - 建议合并到哪个未开始 Phase
   - 用户确认后更新完成标准或产出
4. 延后型：
   - 移入 PLAN.md “延后”
   - 在子计划“执行中发现”中标注为延后
5. 更新子计划文件和 PLAN.md
```

如果阻断条目很多（至少 3 条且预估总轮次翻倍），建议用户重新拆分子计划。

## 执行中插入新计划

当已有子计划在执行中，用户提出新的大功能或 Review 插入阻断修复时：

```
Step 1: 不打断当前 Phase
  - 当前 Phase 继续跑完
  - Gate 窗口再处理排序

Step 2: 快速评估
  - 新计划是否直接影响当前 Phase
  - 是否必须作为 P0 前置修复
  - 是否高于所有待开始计划

Step 3: 规划
  - 新功能/新技术/大重构/复杂 UI -> 委派 sub-brainstorm 执行正式头脑风暴
  - 已有模块加功能 -> 轻量讨论
  - Review 阻断型 bug -> ongoing/P0-<desc>.md 或 backlog/P0-<desc>.md
  - Review 非阻断技术债务 -> backlog/P0-tech-debt.md

Step 4: 创建或更新子计划
  - 写入 docs/dep/plans/<lifecycle>/P<phase>-<name>.md
  - 在 PLAN.md 注册到“待开始”
  - P0 位于最高优先级

Step 5: 当前 Phase Gate 时告知用户
  - 当前 Phase 完成
  - 下一个执行项
  - 新插入计划的位置和理由
```

原则：
- 当前 Phase 是原子执行单元，除非直接冲突，否则不中断。
- Gate 是排序调整窗口。
- 用户决定优先级，AI 负责给出影响和风险。

## 子计划完成与同步

### 完成验证

子计划所有内部 Phase 完成时：

```
1. 全部完成标准已勾选
2. 测试通过（如有）
3. Review 通过（如适用）
4. DEVLOG 完整记录每个 Phase 的轮次
5. syncs_to 主文档已同步
```

### 同步到主文档

按子计划 frontmatter 中 `syncs_to` 清单逐项更新。同步目标必须落到主文档模板定义的具体章节：

| 主文档 | 模板 | 常见同步内容 |
|--------|------|--------------|
| `PROJECT_SPEC.md` | `templates/PROJECT_SPEC.md.template` | 功能范围、接口契约、技术决策、非功能需求 |
| `PROJECT_GUIDE.md` | `templates/PROJECT_GUIDE.md.template` | 技术栈、模块结构、数据流、目录结构、关键约定 |
| `TEST_GUIDE.md` | `templates/TEST_GUIDE.md.template` | 测试框架、测试结构、覆盖范围、测试数据 |
| `CODE_STYLE.md` | `templates/CODE_STYLE.md.template` | 命名、格式、注释、导入、错误处理、特殊约定 |

同步完成后：
- 关键决策写入或更新 `docs/main/memory/`。
- 在子计划文件中标注“已同步”及日期。
- 将子计划文件移动到 `docs/dep/plans/complete/`，并将 `status` 改为 `done`。
- PLAN.md 将子计划从“进行中”移到“最近完成”，只保留最近 3 条完成指针。

## UI 类 Phase 额外要求

UI 计划必须描述用户实际看到和能够操作的行为，不能只列模块名、组件名或“实现某页面”。细致度应落在产品行为、信息层级、状态和证据边界；Tailwind class、像素值、内部函数名等实现细节留在开发阶段。

在子计划的 Phase 总览之前增加以下三个强制章节。非 UI 子计划删除这些章节。

### 设计基线与偏差清单

记录设计依据及版本，并为关键视觉结构分配稳定 ID。至少说明模块顺序、首屏默认内容、共享 KPI、卡片/图表/表格布局和窄屏重排原则。

任何偏离必须逐项记录：

| 偏差 ID | 基线 ID | 原设计 | 调整方案 | 调整原因 | 用户确认 |
|---------|---------|--------|----------|----------|----------|
| D-01 | UI-03 | [原设计行为] | [拟调整行为] | [证据或约束] | pending / approved YYYY-MM-DD / rejected |

- `pending` 偏差不能进入实现。
- 开发中发现的新偏差必须先回写清单并取得用户确认。
- 没有设计稿时，以用户确认的文字需求或当前生产页面作为基线，并明确标注来源；不得假装存在设计稿。

### 页面/组件/状态/交互矩阵

每个可见或可操作元素使用一行合同，建立以下映射：

```text
设计稿元素 -> 数据来源 -> 页面/组件 -> 默认状态 -> 交互结果 -> 测试断言 -> 偏差许可
```

| UI ID | 页面/区域 | 用户可见内容或操作 | 数据来源 / 证据 | 默认状态 | 交互与结果 | 状态覆盖 | 验收断言 | 偏差 |
|-------|-----------|--------------------|-----------------|----------|------------|----------|----------|------|
| UI-01 | [页面/区域] | [看到什么/能做什么] | `payload.path` / 静态配置 / 无 | [首屏表现] | [点击/选择/筛选后的结果及 URL 行为] | 默认/加载/空/错误/部分/窄屏 | [可自动化验证的行为] | 不允许 / D-01 |

规则：

- 模块顺序、默认槽位、筛选联动、分组切换、导航目标和 URL 恢复都必须显式写出。
- 每个数字、图表和分组必须指向具体 payload 字段或其他可信来源。
- 数据不足时写明占位、隐藏、禁用或错误提示；禁止未声明的推导、补值或合并。
- 状态矩阵至少覆盖默认、加载、空数据、错误、部分数据和窄屏，并为每种状态写出具体 UI 表现；不适用时写 `N/A` 及理由。
- 组件树和涉及文件仅在能澄清职责时补充，不替代用户行为合同。

### 视觉与行为验收清单

验收项必须引用 `UI ID`，并同时覆盖视觉结构与核心行为：

```markdown
- [ ] `[UI-01]` 首屏模块顺序、默认内容和信息层级与基线一致
- [ ] `[UI-02]` 卡片点击到达合同指定目标，键盘操作等价
- [ ] `[UI-03]` 筛选、变量选择或分组切换按合同联动并可由 URL 恢复
- [ ] `[UI-04]` 默认/加载/空/错误/部分/窄屏状态均有视觉核验
- [ ] 所有设计偏差均已记录且为 `approved`
- [ ] 行为测试断言覆盖核心操作结果，不只检查标题或静态文本存在
```

每个 UI Phase 的“完成标准”必须引用其负责的 `UI ID` 和验收项。Phase Gate 同时对照设计基线、子计划合同、实际实现和测试；任一不一致且无已批准偏差时不得通过。
