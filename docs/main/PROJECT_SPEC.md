# 项目规格说明

## 项目目标

为 Codex 等 agent 提供可持续维护的技能工厂，使专业工作流能够以结构化、可校验、可分发的 skill 形式复用。

## 功能范围

### 已实现

- Skill 脚手架：创建标准目录、`SKILL.md` 和基础 eval 文件。
- Skill 工具链：安装、校验、索引生成和打包。
- `personal-assistant`：文档优先的开发协作与规划路由。
- `sub-brainstorm`：需求探索和设计规划。
- `generate-sap`（draft）：从 Protocol、Sponsor 约定、已确认决定和经核验的公开先例生成结构完整、内容状态明确、依据可追溯的 SAP review draft。
- `review-sap`（draft）：审阅外部 SAP，按版本化检查表覆盖结构完整性、内部一致性、与 Protocol 一致性和可编程性四个维度，输出证据关联的 Excel 问题清单；docx 批注须用户确认后生成。

### 规划中

- 无已确认的项目级规划项；具体 skill 以独立开发任务推进。

### 明确不做

- 不在项目工具链中实现业务运行时或通用 Agent Harness。
- 不把 Evidence、Validation、GUI 等外部平台能力伪装成已实现的 skill 能力。

## 技术决策记录

| 日期 | 决策 | 选项 | 选择 | 理由 |
|------|------|------|------|------|
| 2026-08-12 | Skill 组织方式 | 单体应用 / 顶层目录 | 每个顶层目录一个 skill | 与现有发现、安装和校验工具链一致 |
| 2026-08-17 | SAP 能力定位 | DecisionPackage / Agent Workflow / 固定内容生成 Skill | 单一 `generate-sap` authoring skill | Skill 负责规范生成内容和结构化依据，不承担外部编排或审批 |
| 2026-08-17 | 输入不足处理 | 阻断整份文档 / 省略章节 / 完整结构加局部问题 | 完整结构加局部问题 | 保持 SAP 可审阅，缺口只阻断受影响内容项 |
| 2026-08-17 | 同类研究 | 不搜索 / 外部知识库 / 宿主自主广搜 | 宿主自主广搜并明确降级 | 保持 Skill Layer 最小实现，同时要求直接引用和先例边界 |
| 2026-08-28 | Ledger 文件序列化 | 模型手写完整 YAML / 逐记录 JSON + 确定性组装 | 逐记录 JSON + 确定性组装 | 将语法可靠性从长文本生成中分离，同时不改写模型给出的语义或统计判断 |
| 2026-11-03 | SAP 审阅对象与范围 | 仅审 generate-sap 产出 / 外部 SAP / 两者 | 外部 SAP；v1 维度为结构、内部一致性、Protocol 一致性、可编程性 | 用户主要场景为外部 SAP；方法学恰当性误报风险高，后续单独模块细化 |
| 2026-11-03 | 审阅检查表来源 | Sponsor SOP / 模型自由判断 / 公开同类同期标准 | 以 Gamble 2017、Homer 2022、ICH E9/E9(R1)、SPIRIT 2025、ICH M11 等初定 v0.1.0 检查表 | 无 SOP；检查项须有可追溯依据，未核验来源不得单独支撑 Critical/Major |
| 2026-11-03 | 审阅输出形式 | Markdown / Excel / docx 批注 | Excel 问题清单为主；docx 批注经用户确认后生成新文件 | 贴合统计师跟踪关闭流程，避免未经确认改动受控文档 |
| 2026-09-02 | 临床评审后修复范围 | 个案提示 / 扩展工作流 / 最小生成约束 | 最小生成约束 | 只固化跨运行重复的 evidence-mode、adaptive/Bayesian 完整性和 Protocol 内部冲突检查，不把评分治理或参考 SAP 后续决定写入 Skill |

## 接口契约

- 每个 skill 的入口为 `<skill-name>/SKILL.md`。
- `.skill-registry.json` 记录 `status`、`category`、`last_modified`、`has_evals` 和 `tags`。
- `scripts/validate_all.py` 对所有注册 skill 执行 frontmatter 校验。
- `generate-sap` 输出三个逻辑产物：完整 `SAP Review Draft`、`Generation Evidence Ledger`、`Open Questions and References`。
- generic 模板的 18 个二级章节标题和顺序是固定合同；仅在提供 Sponsor 模板时允许改变。
- 当前研究的 Protocol、修订、确认决定和 Sponsor 约定只进入 Ledger 的 `document.source_versions` / `source_facts`；外部 `references` 只记录规范、同类研究和方法学来源。
- 写入文件时，`Generation Evidence Ledger` 由逐条、受限、可解析的 JSON 记录暂存后确定性序列化为 YAML；组装器不得推断、补写或修复语义内容。
- 每个 material content unit 只能标记为 `sourced`、`derived`、`proposed`、`tbd`、`conflict` 或 `not-applicable`。
- `sourced` 内容项不得包含 assumptions 或 alternatives；混合来源事实与研究特定提议时必须拆分，提议项必须在正文显式标记并关联 Query。
- 当 Protocol 提供 adaptive/Bayesian 方法时，必须从正文和附录完整提取适用的 prior、参数化、阈值、borrowing、升降级、停止和剂量推荐规则；已存在的来源事实不得降级为 TBD 或裸引用。
- 组装前必须核对 synopsis、设计正文、统计章节和附录中的 arm/sub-arm、cohort 和 sample-size 逻辑；不一致时保留 `conflict` 并生成稳定 Query。
- 同类研究 Reference 必须记录真实文档类型、版本/日期/状态、直接 URL、章节或页码、检索日期、相似点和重要差异。
- 所有输出必须要求合格统计师审核，不得声称已批准或已完成法规合规判断。
- `review-sap` 每个适用检查项必须有且仅有一个覆盖结论（`pass`、`finding`、`not-applicable`、`not-assessable`）；缺少对照文件时相关项只能为 `not-assessable`。
- `review-sap` 问题记录逐条以 JSON 暂存并由 `build_issue_log.py` 校验后生成 Excel；PRO 维度及 `error`/`inconsistency` 问题必须同时给出 SAP 与对照文件的位置和原文；低置信度问题不得为 Critical；方法学意见仅可记为 `out-of-scope-observation`。
- `review-sap` 不改写 SAP 正文，不得把研究标识或原文写入网络检索。

## 非功能需求

- 可维护性：使用渐进式披露，避免无关上下文加载。
- 可移植性：Skill 内容采用 Markdown、JSON 和 YAML 等文本格式。
- 安全性：专业或高风险领域输出必须显式保留证据、假设和人工审核边界。
- 可审计性：SAP正文可追溯到当前研究事实、应用规则、假设、先例和未决问题；不得伪造来源或输出批准/合规结论。
- 序列化可靠性：无效单条记录必须在修改暂存或最终文件前被拒绝；最终 Ledger 必须可解析、ID 唯一且不得静默覆盖既有输出。
- 结构完整性：任何输入充分度下都保留完整目标模板结构；缺失或冲突在对应章节表达。
- 谨慎检索：网络或文档不可用时显式记录 `limited` 或 `unavailable`，不得把搜索失败解释为不存在先例。
