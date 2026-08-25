---
phase_index: 1
status: done
created: 2026-08-14
updated: 2026-08-17
priority: 1
estimated_rounds: 7-10
depends_on: []
tags:
  - clinical-statistics
  - sap
  - skill
  - authoring
  - evidence
syncs_to:
  - PROJECT_SPEC.md
  - PROJECT_GUIDE.md
  - TEST_GUIDE.md
---

# Generate SAP Skill

> Lifecycle rule: this file's directory and `status` must match.
> `plans/backlog/` = `planning`; `plans/ongoing/` = `in-progress`; `plans/complete/` = `done`; `plans/deferred/` = `deferred`.

## 目标

构建一个单入口 `generate-sap` Skill，将 Protocol、SAP 模板、Sponsor 约定、已确认统计决定和公开同类研究先例，转换为结构完整、内容状态明确、依据可追溯的 SAP review draft。

## 背景

- 当前状态：仓库中存在一个未提交的 `clinical-statistical-design` draft，其目标是输出统计 `DecisionPackage`，与本计划确认的“生成 SAP 固定内容”目标不同；实现前必须明确迁移、复用或退役边界，不能把两个目标继续混在同一个入口中。
- 约束：只实现 Skill Layer；不实现 Agent Workflow、外部 Evidence Platform、知识图谱、向量库、GUI、独立 Validation Engine 或持久检索服务。
- 约束：无论前置信息是否充分，都必须实例化完整 SAP 章节结构；缺失、冲突和待决策内容在对应章节内以稳定 ID 的 `TBD`、`Author Query` 或 `Conflict` 表达，不阻断无关章节。
- 约束：同类研究检索必须使用宿主实际可用的网络检索能力；检索不可用或证据不足时必须显式降级，不得声称已经搜索或找到先例。
- 方案来源：正式头脑风暴及用户于 2026-08-14 确认的架构基线。
- 头脑风暴记录：放弃“半个 Agent Workflow/Decision Engine”方向；选择单一生成 Skill、逐内容项约束、结构化生成依据和按章节渐进式披露。公开 SAP 作为先例而非规范性要求。

## 涉及范围

- **包含**：`generate-sap` Skill 入口与显式调用策略；完整 SAP 结构模板；输入、来源优先级、内容项、章节和生成依据契约；`sourced / derived / proposed / tbd / conflict / not-applicable` 生成权限；章节内问题表达和跨章节稳定引用；核心统计章节规则；同类研究广泛检索、筛选、总结和明确 Reference；行为评测、项目校验、安装和索引更新。
- **包含**：首版对研究设计、Objectives/Endpoints、Estimands/ICE、Analysis Populations、Primary Efficacy Analysis、Missing Data/Sensitivity 提供实质生成规则；其他标准章节先保证结构存在，并按事实充分性生成、标记不适用或保留待确认项。
- **不包含**：自动批准统计决策、法规合规结论、TFL/ADaM/统计程序生成、患者级数据处理、Sponsor 专有模板的臆造、自动下载仓库、复杂相似度模型或长期证据存储。
- **与现有草稿的边界**：`clinical-statistical-design` 仅作为可选择复用的规则素材，不作为本计划的目标输出；任何删除、改名或退役必须在 P1 形成明确差异和处置决定后执行。

## 主文档影响

完成后需要更新：

- `PROJECT_SPEC.md`：将 SAP 能力目标从统计 DecisionPackage 修正为结构完整的 SAP 生成、内容项状态、依据追溯和先例检索契约。
- `PROJECT_GUIDE.md`：登记 `generate-sap` 模块、渐进式披露资源、生成数据流及与 `clinical-statistical-design` 的最终边界。
- `TEST_GUIDE.md`：增加结构完整性、章节内缺口、来源冲突、引用可追溯、无检索能力降级和跨章节一致性评测要求。

`syncs_to` 和本节保持一致；本计划不新增代码风格约定。

## 架构基线

```text
输入资料
  -> SapGenerationContext
  -> 实例化完整 SAP 章节骨架
  -> 按章节渐进加载规则
  -> 逐 Content Unit 判断并生成
       sourced / derived / proposed / tbd / conflict / not-applicable
  -> 跨章节一致性检查
  -> SAP Review Draft
     + Generation Evidence Ledger
     + Open Questions / References
```

同类研究检索位于 `SapGenerationContext` 建立之后、实质统计章节生成之前：先形成 `Study Fingerprint`，再搜索候选研究、筛选高相似研究、深入读取公开 SAP 或替代文档，最后形成带直接引用和差异说明的 `Precedent Summary`。

## 风险与缓解

| 风险 | 缓解措施 |
|------|----------|
| 输入不足导致章节被省略 | 先实例化完整模板；内容状态只在章节/内容项级别生效 |
| 模型用通用知识补造研究决定 | 强制生成权限分类；无法来源化或确定性推导时使用 `proposed` 或 `tbd` |
| 同类 SAP 被误当成监管要求 | 区分 `normative_reference` 与 `trial_precedent`，记录相似点和重要差异 |
| 网络搜索不可用却伪造检索结果 | 输出明确的 `search unavailable/limited` 状态，不允许无直接来源的先例结论 |
| 公开文档版本、状态或引用不清 | Reference 必须含文档类型、版本、日期、状态、直接 URL、章节/页码和检索日期 |
| 同一未决问题在多个章节产生漂移 | 使用稳定 Query ID，在起源章节完整提出，在受影响章节交叉引用 |
| 新 Skill 与现有 draft 职责重叠 | P1 先完成差异表和处置决定，后续 Phase 不并行维护两套相同职责 |

---

## Phase 总览

| Phase | 目标 | 预估轮次 | 依赖 | 状态 |
|-------|------|----------|------|------|
| P1 | 确认包边界并建立合规脚手架 | 1-2 | - | done |
| P2 | 建立完整结构和生成契约 | 2 | P1 | done |
| P3 | 实现首版核心 SAP 章节规则 | 2-3 | P2 | done |
| P4 | 实现受控的同类研究检索与引用规则 | 1-2 | P2 | done |
| P5 | 完成评测、校验、安装和文档同步 | 1-2 | P3, P4 | done |

---

## P1: 确认包边界并建立脚手架

### 输入条件

- 本计划处于 `planning` 且已登记到 `docs/dep/PLAN.md`。
- 用户已确认单一生成 Skill、完整 SAP 骨架、章节内缺口和同类研究检索的架构基线。
- 已检查工作区中 `clinical-statistical-design` 的实际内容和未提交状态。

### 产出

- `clinical-statistical-design` 与 `generate-sap` 的职责差异及处置决定。
- 通过项目 `scripts/new_skill.py` 创建的 `generate-sap` 标准脚手架。
- 窄化的 `SKILL.md` metadata、核心入口边界和 `agents/openai.yaml` 显式调用策略。
- `.skill-registry.json` 中状态为 `draft` 的登记项。

### 完成标准

- [x] 已明确现有 draft 是复用、改名还是退役，且没有静默删除用户改动。
- [x] `generate-sap` 使用项目脚手架创建，目录名与 frontmatter `name` 一致。
- [x] Description 只触发 SAP 创建/章节生成/修订，不吞并 SAP review、TFL、ADaM 或统计编程任务。
- [x] `agents/openai.yaml` 与 SKILL.md 一致，并按显式 Workflow 调用目标禁用隐式调用。
- [x] 本 Phase 不包含实质章节知识扩写。

### 边界（本 Phase 明确不做）

- 不生成真实研究 SAP。
- 不建立外部搜索服务、知识库或运行时。

### 涉及文件

| 文件 | 操作 | 预计行数 |
|------|------|----------|
| `generate-sap/SKILL.md` | 新建并收敛入口 | ~100 |
| `generate-sap/agents/openai.yaml` | 新建 | ~15 |
| `generate-sap/evals/evals.json` | 脚手架创建、保留待填 | ~10 |
| `.skill-registry.json` | 修改 | +10 |
| `clinical-statistical-design/` | 仅按已确认处置决定修改 | 待定 |

### 关键决策

- 顶层结构：多个生成子 Skill / 单一生成 Skill，选择单一 `generate-sap`，理由是避免入口重叠，章节差异由包内渐进式披露处理。
- 调用策略：自动关键词触发 / 上层 Workflow 显式调用，选择显式调用，理由是避免仅提到 SAP 时过触发。

---

## P2: 建立完整结构和生成契约

### 输入条件

- P1 Gate 已通过，目标包和现有 draft 的边界明确。
- `generate-sap` 脚手架存在并通过基础 frontmatter 校验。

### 产出

- `SapGenerationContext`、来源优先级、`Content Unit`、章节计划、Generation Evidence Ledger 和 Open Question 契约。
- 完整 SAP review-draft 模板及生成记录模板。
- 章节级状态和生成权限规则。
- 稳定 Query ID、跨章节传播和必要的一致性检查规则。

### 完成标准

- [x] 任意输入充分度下都能实例化完整 SAP 章节结构。
- [x] 每个内容项只能使用 `sourced / derived / proposed / tbd / conflict / not-applicable` 之一，并定义允许行为。
- [x] `partial/tbd/conflict` 在对应章节表达，且不会阻断无关章节。
- [x] 同一问题影响多个章节时使用一个稳定 Query ID 和交叉引用。
- [x] Review Draft 保留问题标记；Clean Draft 不得静默移除未解决的阻断项。
- [x] 事实、规则、假设、推导摘要、输出正文和未决问题可双向追溯。

### 边界（本 Phase 明确不做）

- 不填充全部治疗领域和终点类型的统计知识。
- 不把结构化依据写成模型原始思维链。

### 涉及文件

| 文件 | 操作 | 预计行数 |
|------|------|----------|
| `generate-sap/SKILL.md` | 修改 | +100 |
| `generate-sap/references/input-contract.md` | 新建 | ~150 |
| `generate-sap/references/source-precedence.md` | 新建 | ~100 |
| `generate-sap/references/content-unit-contract.md` | 新建 | ~180 |
| `generate-sap/references/section-map.md` | 新建 | ~160 |
| `generate-sap/references/cross-section-checks.md` | 新建 | ~120 |
| `generate-sap/assets/sap-template.md` | 新建 | ~180 |
| `generate-sap/assets/generation-record-template.yaml` | 新建 | ~100 |

### 关键决策

- 完整性：文档级 Ready Gate / 结构与内容双层完整性，选择双层完整性；结构必须完整，内容成熟度按章节和内容项表达。
- 缺口位置：集中问题清单 / 章节内问题，选择章节内提出并附全局索引；保证问题与受影响正文相邻且可集中审阅。

---

## P3: 实现首版核心 SAP 章节规则

### 输入条件

- P2 的输入、内容项和输出契约已稳定。
- 已确定首版通用 SAP 模板；若没有 Sponsor 模板，只能声明为 generic baseline。

### 产出

- 研究设计、Objectives/Endpoints、Estimands/ICE、Analysis Populations、Primary Efficacy、Missing Data/Sensitivity 的实质生成规则。
- 其他标准章节的结构、适用性判断和缺口表达规则。
- 固定正文模式与章节级示例，不绑定特定 Sponsor 或单个研究。

### 完成标准

- [x] 六个核心领域均定义必要输入、适用约束、禁止推断、输出内容和缺失时的章节表现。
- [x] Estimand、Population、Estimator、ICE、Missing Data 和 Sensitivity 之间存在明确一致性规则。
- [x] 未确认的 covariance、alpha、sample size、imputation 参数等研究特定值不会从通用知识或先例中直接复制。
- [x] 非核心章节仍出现在完整结构中，并能生成已知内容、`not-applicable` 或 `tbd`。
- [x] SKILL.md 只保留主循环和路由，详细知识通过直接链接的一层 references 渐进加载。

### 边界（本 Phase 明确不做）

- 不承诺覆盖所有疾病、复杂设计和终点类型。
- 不生成 TFL、ADaM spec、SAS/R代码或法规合规结论。

### 涉及文件

| 文件 | 操作 | 预计行数 |
|------|------|----------|
| `generate-sap/references/study-design-rules.md` | 新建 | ~150 |
| `generate-sap/references/estimand-ice-rules.md` | 新建 | ~180 |
| `generate-sap/references/population-rules.md` | 新建 | ~120 |
| `generate-sap/references/efficacy-analysis-rules.md` | 新建 | ~220 |
| `generate-sap/references/missing-sensitivity-rules.md` | 新建 | ~180 |
| `generate-sap/references/safety-analysis-rules.md` | 新建基础规则 | ~100 |
| `generate-sap/SKILL.md` | 更新资源路由 | +40 |

### 关键决策

- 首版覆盖：所有章节均深度实现 / 完整结构加核心章节深度实现，选择后者；先验证生成约束和追溯质量，不伪装成全领域成熟包。

---

## P4: 实现同类研究检索与明确引用

### 输入条件

- P2 的来源与内容项契约已稳定。
- 宿主搜索能力可能存在也可能缺失，降级状态已进入输出契约。

### 产出

- `Study Fingerprint`、分层来源、查询构造、候选筛选、深入阅读、停止规则和失败降级规范。
- `Precedent Summary` 和逐条 Reference 记录格式。
- Trial precedent 与 normative reference 的严格区分及应用限制。

### 完成标准

- [x] 检索优先覆盖 ClinicalTrials.gov、Health Canada、EMA 等可公开获得 Protocol/SAP/统计方法资料的权威入口，再考虑期刊附件、CSR和监管统计审评。
- [x] 广泛搜索采用候选集、短名单和深入阅读三步；数量不足时报告限制，不用低相似研究凑数。
- [x] 每条引用包含研究标识、文档类型、版本、日期、状态、直接 URL、章节/页码、检索日期、相似点和重要差异。
- [x] 不把搜索引擎摘要当证据，不把 CSR/论文描述冒充原始 SAP。
- [x] 先例只支持候选设计和推导说明，不能覆盖当前 Protocol、Sponsor 约定或已确认决定。
- [x] 无网络、页面不可访问或无高相似先例时输出明确降级状态。

### 边界（本 Phase 明确不做）

- 不实现爬虫、自动下载仓库、向量索引或复杂数值相似度模型。
- 不缓存或再分发受版权、许可或访问限制保护的完整文档。

### 涉及文件

| 文件 | 操作 | 预计行数 |
|------|------|----------|
| `generate-sap/references/precedent-research.md` | 新建 | ~220 |
| `generate-sap/references/source-precedence.md` | 修改 | +40 |
| `generate-sap/references/content-unit-contract.md` | 修改 | +30 |
| `generate-sap/SKILL.md` | 更新检索路由 | +30 |

### 关键决策

- 检索实现：外部检索服务 / Skill 指导宿主使用实际可用网络工具，选择后者；保持 Skill Layer 边界并允许明确降级。
- 先例用途：多数投票 / 比较与条件性支持，选择比较与条件性支持；研究差异必须进入推导和限制。

---

## P5: 评测、交付校验和文档同步

### 输入条件

- P3 和 P4 的资源、模板和路由均已完成。
- 已准备不含真实患者信息的结构化或合成测试材料。

### 产出

- 覆盖完整输入、部分输入、来源冲突、检索不可用、无高相似先例和跨章节传播的行为评测。
- 注册表、索引和主文档同步。
- 项目校验、Codex quick validation 和按单个 Skill 安装验证结果。

### 完成标准

- [x] 输入不足案例仍生成完整 SAP 结构，并在正确章节放置稳定问题 ID。
- [x] 完整输入案例生成的核心章节均能追溯到事实、规则、假设和 Reference。
- [x] 来源冲突案例不自动裁决；未确认研究特定参数不被补造。
- [x] 检索案例的引用均可直接定位；检索不可用案例不会伪造搜索结果。
- [x] 负向案例不生成 TFL、ADaM、代码、批准或合规结论。
- [x] `python scripts/validate_all.py` 和 Codex `quick_validate.py` 均通过。
- [x] 使用项目安装脚本仅安装 `generate-sap`，并运行 `python scripts/generate_index.py`。
- [x] `.skill-registry.json`、`SKILL_INDEX.md`、`PROJECT_SPEC.md`、`PROJECT_GUIDE.md` 和 `TEST_GUIDE.md` 与最终实现一致。

### 边界（本 Phase 明确不做）

- 不用“eval文件存在”替代实际行为验证。
- 不在验证阶段扩大方法或疾病覆盖范围。

### 涉及文件

| 文件 | 操作 | 预计行数 |
|------|------|----------|
| `generate-sap/evals/evals.json` | 修改 | ~200 |
| `generate-sap/evals/files/*` | 新建合成fixture | 待定 |
| `.skill-registry.json` | 修改 | +/−10 |
| `SKILL_INDEX.md` | 生成更新 | 自动 |
| `docs/main/PROJECT_SPEC.md` | 修改 | +/−40 |
| `docs/main/PROJECT_GUIDE.md` | 修改 | +/−40 |
| `docs/main/TEST_GUIDE.md` | 修改 | +/−50 |

### 关键决策

- 验收重点：文案相似度 / 约束遵循和可追溯性，选择约束遵循和可追溯性；SAP措辞允许合理变化，但结构、状态、引用和禁止事项必须稳定。

---

## 执行中发现

> 执行本子计划过程中暴露的问题。每个 Phase Gate 时审查并分类。

| ID | 描述 | 发现于 | 类型 | 处理 |
|----|------|--------|------|------|
| F-001 | 项目全量校验器在读取既有中文 Skill 时出现 GBK 解码错误，随后回退 builtin validator | P5 | tooling | `generate-sap` 另行通过 Codex 官方 quick validator；记录工具链编码风险，不扩大本 Skill 改动范围 |
| F-002 | 安全策略阻止清理工作区外的旧 Junction 和被忽略的旧 `.skill` 分发包 | P5 | delivery | 旧 Junction 指向不含 `SKILL.md` 的空目录，当前不可调用；旧分发包不参与新包安装或索引，交付中明确残留风险 |
| F-003 | Codebuddy skill 根目录不存在 | P5 | environment | 安装脚本按既有行为跳过；Codex、Claude、Agents 和 Workbuddy 安装成功 |

## 关键决策记录

| 日期 | 决策 | 选项 | 选择 | 理由 |
|------|------|------|------|------|
| 2026-08-14 | 顶层能力形态 | Decision Engine / 多 Skill Workflow / 单一 SAP 生成 Skill | 单一 `generate-sap` | 目标是规范固定 SAP 内容生成，不是构建半个 Agent Workflow |
| 2026-08-14 | 输入不足处理 | 阻断整份文档 / 省略章节 / 保留完整结构并局部标记 | 保留完整结构并局部标记 | SAP 起草需要先形成完整文档，成熟度按章节递进 |
| 2026-08-14 | 中间依据 | 原始思维过程 / 结构化生成证据 | 结构化生成证据 | 便于审阅和追溯，同时避免不可控的原始推理输出 |
| 2026-08-14 | 同类研究输入 | 不搜索 / 仅用户提供 / 自主广泛搜索 | 自主广泛搜索 | 用公开先例补充候选方案，但必须明确引用并保持谨慎边界 |
| 2026-08-14 | 外部架构 | 知识库和搜索服务 / 使用宿主现有搜索能力 | 使用宿主现有能力 | 保持 Skill Layer 和最小实现范围 |
| 2026-08-17 | 现有 draft 处置 | 长期并存 / 原地继续扩写 / 新包验证后替换 | 新包验证后替换 | 旧包目标是 DecisionPackage，与已批准的 SAP authoring 入口不一致；验证前保留以避免丢失可复用规则 |

## 同步记录

| 日期 | 已同步到 | 说明 |
|------|----------|------|
| 2026-08-17 | `PROJECT_SPEC.md`, `PROJECT_GUIDE.md`, `TEST_GUIDE.md` | 同步 `generate-sap` 的完整结构、生成模式、证据账本、先例检索、边界和评测要求 |
