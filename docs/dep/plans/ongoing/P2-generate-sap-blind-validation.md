---
phase_index: 2
status: in-progress
created: 2026-08-27
updated: 2026-09-01
priority: 1
estimated_rounds: 6-10
depends_on:
  - P1-generate-sap-skill.md
tags:
  - clinical-statistics
  - sap
  - skill-validation
  - blinded-review
  - oncology
syncs_to:
  - PROJECT_SPEC.md
  - TEST_GUIDE.md
---

# Generate SAP 真实方案盲测验证

> Lifecycle rule: this file's directory and `status` must match.
> `plans/backlog/` = `planning`; `plans/ongoing/` = `in-progress`; `plans/complete/` = `done`; `plans/deferred/` = `deferred`.

## 目标

使用两个公开肿瘤 I/II 期研究的 Protocol，在不向生成会话暴露对应 SAP 的条件下，对冻结的 `generate-sap` Skill 进行可行性盲测；比较 Protocol-only 与“Protocol + 其他研究先例”输入，评价结构完整性、统计合理性、证据追溯、谨慎降级和运行一致性。

## 背景

- 当前状态：post-remediation L1 六槽已 6/6 locked，4 个主样本 + 1 个重复样本的匿名包已经就绪；下一步只完成参考版本归因、AI 事实预审和合格统计师盲评。
- 2026-09-02 用户根据五包 AI candidate 评审明确授权启动最小 Skill 修复。现有 REV 包和分数保留为修复前基线；不回写历史产物，也不得将其结论表述为对当前工作树 Skill 版本的验证。P4-B 若继续，只用于完成修复前基线的专业归因。
- 当前资产：本地忽略目录 `.validation-work/generate-sap/oncology-phase1-2/` 已准备 4 个目标案例、其他研究先例库、搜索隔离材料、隐藏参考 SAP 和评分表模板。
- 约束：本计划只验证冻结版本，不在运行或评分过程中修改 Skill；发现的问题必须完成解盲归因后再决定是否建立后续修复计划。
- 约束：首轮只使用 `CASE-ONC-001` 和 `CASE-ONC-004`；`CASE-ONC-002/003` 保留为未见回归案例，不在本计划中消耗。
- 约束：搜索会话不能接触目标研究标识、Protocol、manifest、denylist 或隐藏参考 SAP；生成会话只接收目标 Protocol 和已审计的冻结先例包，并关闭网络。
- 约束：参考 SAP 是 held-out comparator，不是绝对标准答案；Protocol 无法支持而参考 SAP 后续确定的内容，应评价 Skill 是否正确提出 `TBD`、Author Query 或合理替代方案。
- 约束：运行记录使用简单标识符和 `locked` 状态，不新增或依赖文件哈希。记录模型名称、推理配置、Skill 版本标签、输入版本标签、先例包标签、时间和联网状态。
- 方案来源：正式头脑风暴；用户于 2026-08-27 确认“自动客观检查 + AI 结构化预审 + 1 名合格统计师最终盲评”的验证路径。
- 头脑风暴记录：生成层保留六个锁定输出；专业 L2 按 `SAP-VALIDATION-GOVERNANCE-V2` 只评 4 个主样本 + 1 个重复样本。统计师不知道运行分组；首轮只作可行性判断，不声称已完成全面专业验证。

## 涉及范围

- **包含**：预注册评分规则和判分锚点；输入/Skill/模型/先例包的简单版本登记；搜索隔离与目标泄漏审计；两案例 6 次独立生成；自动结构和禁止项检查；匿名盲评包装；Protocol/SAP 版本关系核对；AI 结构化差异预审；统计师最终盲评；解盲归因和后续修改建议。
- **包含**：对照与正式运行的先例增益比较；同一正式配置两次运行的关键结论一致性检查；对严重错误、重复缺陷和参考 SAP 后期运营决定分别归因。
- **不包含**：在本计划中修改 `generate-sap`；运行 `CASE-ONC-002/003`；搜索或向生成会话暴露目标研究对应 SAP；患者级数据处理；多评审者一致性研究；以两次重复运行宣称统计意义上的稳定性；构建通用 Agent Workflow 或独立验证平台。
- **与后续计划的边界**：若解盲后存在满足修改门控的问题，另建最小 Skill 修复计划；修复后才使用 `CASE-ONC-002/003` 做未见回归验证。

## 主文档影响

完成后需要更新：

- `PROJECT_SPEC.md`：更新 `generate-sap` 的真实方案可行性验证状态、结论边界和人工审核要求。
- `TEST_GUIDE.md`：增加真实 Protocol 盲测方法、客观检查范围、统计师评分维度、通过标准、泄漏控制和保留回归案例。

`syncs_to` 和本节保持一致；本计划不改变项目架构或代码风格，因此不更新 `PROJECT_GUIDE.md` 和 `CODE_STYLE.md`。

## 验证架构

```text
冻结验证合同、Skill/模型标签与输入标签
  -> 审计并冻结其他研究 precedent bundle
  -> 两案例分别执行：Protocol-only x1 + Protocol/precedent x2
  -> 自动检查结构、追溯字段、引用字段、禁止项和目标泄漏
  -> 以简单 Review ID 匿名包装并标记 locked
  -> 核对 Protocol、amendment 与参考 SAP 的日期/版本关系
  -> 揭示隐藏参考 SAP，AI 只预填事实差异和证据位置
  -> 统计师在不知道运行分组的情况下完成专业评分
  -> 解盲，比较对照/正式运行并完成缺陷归因
  -> 形成“不修改 / 建后续最小修复计划 / 建 P0 安全修复”的决定
```

## 运行矩阵与标识

| 案例 | 对照运行 | 正式运行 | 用途 |
|------|----------|----------|------|
| `CASE-ONC-001` | 1 个匿名主样本 | 1 个匿名主样本 + 1 个匿名重复样本 | 实体瘤 I/II 期主基准与重复性观察 |
| `CASE-ONC-004` | 1 个匿名主样本 | 1 个匿名主样本 | AML 联合治疗压力测试 |

- 评审包只使用简单 `Review ID`，不暴露 Protocol-only / precedent-assisted 标签或重复关系；运行到评审的映射只在解盲时读取。
- 输入使用如 `PROT-ONC001-v1`，先例包使用如 `PB-ONC001-v1`，验证合同使用如 `VAL-P2-v1` 的可读标签。
- `locked` 表示该运行已进入评审，之后不得覆写；如需重跑，必须分配新的 Run ID。

## 评分合同

| 维度 | 权重 |
|------|------|
| Protocol 忠实度 | 25 |
| 统计方法合理性 | 25 |
| SAP 内容完整性 | 15 |
| 缺失信息与不确定性处理 | 15 |
| 外部证据和同类研究使用质量 | 10 |
| 内部一致性与可执行性 | 10 |

通过标准预先冻结为：

- 无目标泄漏、虚构引用、审批/合规冒充或 critical 级关键统计错误。
- 两次正式运行单次总分均不低于 75，同一案例正式运行平均分不低于 80。
- 同一案例两次正式运行不存在无说明的关键设计冲突；合理备选必须在生成证据中明确条件和依据。
- 4+1 治理不改变上述冻结阈值：`CASE-ONC-001` 可评价重复运行门槛；`CASE-ONC-004` 只做单次主样本描述，原“两次正式运行”门槛记为 `not-evaluated`。因此本轮只形成最小临床可行性结论，不宣称完整通过原六样本案例级门槛。
- 相较 Protocol-only 对照，正式运行在证据质量或内容完整性上有可观察增益，且不得增加不适当参数迁移或无依据确定性结论。
- 上述分数是本项目的预注册可行性门槛，不声称是行业标准。

## 差异归因合同

每项与参考 SAP 的差异只能归入以下之一：

1. 与参考一致且证据充分。
2. 与参考不同，但属于有依据的合理替代方案。
3. Protocol 已支持，但 Skill 遗漏或判断错误。
4. 缺乏依据，却生成确定性结论。
5. 参考 SAP 使用了生成时 Protocol 无法获知的后续运营或 Sponsor 决定。
6. 参考 SAP 本身不一致、模糊或具有可争议设计。

## 风险与缓解

| 风险 | 缓解措施 |
|------|----------|
| 搜索阶段意外找到目标 SAP | 搜索者只读取去标识 fingerprint；用 denylist 审计查询、URL 和文档，命中即判该运行无效 |
| 统计师从文件名推断运行分组 | 使用 Review ID 重新命名，隐藏 `C/P` 标识和两次正式运行的关联 |
| AI 预审锚定统计师判断 | AI 只预填事实差异、来源位置和待判断项，不替统计师填写最终专业结论 |
| 参考 SAP 晚于 Protocol，包含不可推导决定 | 比较前建立版本关系表；将后续决定归入差异类别 5，不倒算为 Skill 遗漏 |
| 评分阈值过度解释 | 明确阈值只用于首轮可行性门控；保留逐项严重度和统计师文字判断 |
| 两次生成不足以证明稳定性 | 只报告明显关键结论冲突，不计算或宣称统计稳定性 |
| 盲测过程中为提高得分修改 Skill | P1-P5 全程冻结 Skill；所有修改候选在解盲完成后进入独立计划 |

---

## Phase 总览

| Phase | 目标 | 预估轮次 | 依赖 | 状态 |
|-------|------|----------|------|------|
| P1 | 冻结验证合同、简单标识和客观检查 | 1-2 | - | done |
| P2 | 审计并冻结两个案例的其他研究先例包 | 1-2 | P1 | done |
| P3 | 完成两案例隔离生成与匿名包装 | 2-3 | P2 | done（post-remediation L1 6/6；L2 4+1 匿名包 ready） |
| P4 | 完成版本对齐、AI 预审和统计师盲评 | 2 + 人工评审等待 | P3 | in-progress（P4-A done；P4-B 等待合格统计师） |
| P5 | 解盲归因、形成验证结论并同步文档 | 1-2 | P4 | pending |

---

## P1: 冻结验证合同、简单标识和客观检查

### 输入条件

- 本计划处于 `planning` 并登记到 `docs/dep/PLAN.md`。
- P1 `generate-sap` 初版保持不变；本地盲测语料存在且不进入 Git。
- 用户已确认两案例、每案例 3 次运行、单统计师最终盲评和不使用哈希的记录方式。

### 产出

- 预注册的评测协议、评分维度、判分锚点、hard gates 和差异归因规则。
- Run ID、Review ID、输入标签、先例包标签及状态字段的简单登记格式。
- 只检查客观项目的最小自动检查脚本和固定检查报告格式。
- Protocol/SAP 版本关系登记表；此阶段只登记元数据，不读取隐藏参考 SAP 正文。

### 完成标准

- [x] 评分表包含 6 个加权维度、逐级判分锚点、严重度和统计师文字判断字段。
- [x] 运行登记记录模型、推理配置、Skill 标签、输入标签、先例包标签、时间、联网状态和 `locked` 状态，不新增哈希字段。
- [x] 自动检查仅覆盖 18 个顶层章节、状态/Query ID、Generation Evidence Ledger、Reference 必填字段、禁止项和 denylist 命中，不输出专业统计评分。
- [x] 通过标准和差异归因类别在任何生成开始前冻结为 `VAL-P2-v1`。
- [x] `CASE-ONC-002/003` 被明确标记为 reserved，当前计划不得读取其隐藏参考 SAP 或生成输出。

### 边界（本 Phase 明确不做）

- 不生成 SAP，不阅读隐藏参考 SAP 正文。
- 不为自动检查实现自然语言统计正确性判断或通用验证平台。

### 涉及文件

| 文件 | 操作 | 预计行数 |
|------|------|----------|
| `.validation-work/generate-sap/oncology-phase1-2/comparison/evaluation-protocol.md` | 新建 | ~180 |
| `.validation-work/generate-sap/oncology-phase1-2/comparison/scorecard-template.yaml` | 修改 | +80 |
| `.validation-work/generate-sap/oncology-phase1-2/comparison/run-register.yaml` | 新建 | ~80 |
| `.validation-work/generate-sap/oncology-phase1-2/comparison/version-alignment.yaml` | 新建 | ~40 |
| `.validation-work/generate-sap/oncology-phase1-2/comparison/check_objective_requirements.py` | 新建 | ~180 |

### 关键决策

- 运行身份：文件哈希 / 简单标识符，选择简单标识符和 `locked` 状态；满足本轮审计需要并降低不必要复杂度。
- 自动化边界：自动语义裁判 / 客观结构检查，选择客观结构检查；专业统计判断保留给统计师。

---

## P2: 审计并冻结其他研究先例包

### 输入条件

- P1 Gate 已通过，`VAL-P2-v1` 已冻结。
- 搜索者只可访问对应 `search-packets/CASE-ONC-XXX/fingerprint.yaml`。
- 目标 denylist 仅由审计者持有，不向搜索者或生成者暴露。

### 产出

- `PB-ONC001-v1` 和 `PB-ONC004-v1` 两个已审计先例包。
- 每个先例包的搜索日志、入选/排除理由、直接来源、文档类型、版本/日期、定位信息、相似点和重要差异。
- denylist 审计结果和 `valid / invalid` 状态。

### 完成标准

- [x] 两个先例包中的研究均不是对应目标研究，也不包含目标 denylist 标识或目标 SAP URL。
- [x] 每条入选先例均有可直接访问的原始文档来源和明确文档类型，不使用搜索摘要替代证据。
- [x] 每条先例记录相似点、重要差异和可支持的内容边界，不复制研究特定参数作为当前研究事实。
- [x] 搜索不足、访问失败或相似度有限时如实记录，不用低相似材料凑数。
- [x] 审计通过后先例包标记为 `locked`；后续变更必须创建新包标签，不能覆写 v1。

### 边界（本 Phase 明确不做）

- 不搜索目标研究编号、药物名、Sponsor 或对应 SAP。
- 不把其他研究先例解释为法规要求或当前研究已确认决定。

### 涉及文件

| 文件 | 操作 | 预计行数 |
|------|------|----------|
| `.validation-work/generate-sap/oncology-phase1-2/precedent-bundles/CASE-ONC-001/` | 审计并冻结 | 待定 |
| `.validation-work/generate-sap/oncology-phase1-2/precedent-bundles/CASE-ONC-004/` | 审计并冻结 | 待定 |
| `.validation-work/generate-sap/oncology-phase1-2/search-log/2026-08-26.md` | 更新 | +20-40 |
| `.validation-work/generate-sap/oncology-phase1-2/comparison/run-register.yaml` | 更新包状态 | +10 |

### 关键决策

- 先例输入：运行中实时搜索 / 预先审计并冻结，选择预先冻结；隔离搜索泄漏并确保两次正式运行接收相同证据。

---

## P3: 六次隔离生成与匿名包装

### 输入条件

- P2 Gate 已通过，两个先例包均为 `locked` 且审计有效。
- `generate-sap`、模型和推理配置的简单版本标签已登记并冻结。
- 6 个 Run ID 已创建，输出目录为空且隐藏参考 SAP 对生成者不可见。

### 产出

- post-remediation 六个目标槽的完整 SAP Review Draft、Generation Evidence Ledger、Open Questions and References；L2 按治理文件选择 4 个主样本 + 1 个重复样本。
- 每次运行的客观检查报告和有效性状态。
- 不暴露运行分组的 Review ID 映射及匿名评审包。

### 完成标准

- [x] 每次运行均在独立新会话中显式调用同一冻结 `generate-sap`，使用相同模型和推理配置。
- [x] 对照运行只接收目标 Protocol；正式运行只额外接收对应冻结先例包；所有生成会话均关闭网络。
- [x] 生成者未读取目标隐藏参考 SAP、manifest 或 denylist；运行登记完整记录实际输入和状态。
- [x] 6 份输出均完成客观检查；失败项不静默修补，必须保留原输出并以新 Run ID 重跑或标为 invalid。
- [x] 有效输出标记为 `locked` 后不再覆写，并使用 Review ID 进行匿名包装；5 个 L2 评审包不暴露 `C/P`、Run ID 或重复运行关系。

### Gate 结果（2026-08-27）

- P3 Gate 未通过：6 个目标矩阵运行均已完成生成和客观检查，但只有 `ONC004-C01` 通过并锁定；其余 5 个运行标为 `invalid`，原输出和检查报告均保留。
- 失败集中在客观输出契约：当前 Protocol 或冻结 bundle 被误放入外部 `references`，外部引用字段/枚举不符合冻结 schema，固定章节标题发生漂移，或内容单元引用了未定义的外部 source ID。
- `ONC001-C01/C02/C03` 作为执行通道和早期替代尝试历史继续保留；它们不计入 6 个目标矩阵有效输出。
- 重复缺陷已跨案例和 arm 重现；继续使用完全相同的冻结 Skill/prompt 重跑没有新增信息价值，因此不再创建替代 Run ID。
- 未创建 Review ID 映射或匿名评审包，未读取隐藏参考 SAP，P4 不得启动。该历史 blocker 后续由 [`P0-generate-sap-output-contract.md`](../complete/P0-generate-sap-output-contract.md) 处理；当时在其 Gate 完成前本计划保持 blocked。

### Post-remediation Gate 恢复（2026-08-31）

- `REMEDIATION-16` 的六个目标槽全部通过 Markdown audit、Ledger audit、package validator 和冻结 `VAL-P2-v1`，0 failed checks、0 warnings，L1 达到 6/6 locked。
- 按 `SAP-VALIDATION-GOVERNANCE-V2` 选择 4 个主样本和 1 个 repeatability 样本，创建 `REV-101` 至 `REV-105` 五个匿名包；Run ID、arm 标签和重复关系均未暴露，映射单独锁定。
- 匿名包包含 protocol、三件生成产物、客观报告和空白评分卡；不包含也未读取 hidden reference SAP。P3 Gate 恢复为通过，P4 入口恢复到 `ready-for-blinded-statistician`。
- 旧 2026-08-27 失败结论和产物保持历史有效，不被 post-remediation 结果覆写；本轮不是“未调优首次盲测”。

### 边界（本 Phase 明确不做）

- 不根据自动检查或输出观感修改 Skill、prompt、precedent bundle 或已锁定输出。
- 不阅读参考 SAP，不进行专业统计评分。

### 涉及文件

| 文件 | 操作 | 预计行数 |
|------|------|----------|
| `.validation-work/generate-sap/oncology-phase1-2/outputs/CASE-ONC-001/` | 新增 3 次运行产物 | 待定 |
| `.validation-work/generate-sap/oncology-phase1-2/outputs/CASE-ONC-004/` | 新增 3 次运行产物 | 待定 |
| `.validation-work/generate-sap/oncology-phase1-2/comparison/objective-checks/` | 新增检查报告 | 6 份 |
| `.validation-work/generate-sap/oncology-phase1-2/comparison/review-map.yaml` | 新建、评审时隐藏 | ~30 |
| `.validation-work/generate-sap/oncology-phase1-2/comparison/review-packets/` | 新增匿名评审包 | 6 份 |
| `.validation-work/generate-sap/oncology-phase1-2/comparison/run-register.yaml` | 更新 | +30-60 |

### 关键决策

- 重复性观察：单次正式运行 / 两次独立正式运行，选择两次；只发现明显冲突，不作统计稳定性声明。
- 锁定方式：哈希校验 / 简单标识和状态登记，选择后者；重跑用新 Run ID，禁止覆写。

---

## P4: 版本对齐、AI 预审和统计师盲评

### 输入条件

- P3 Gate 已通过，5 个按治理文件选定的匿名评审包和 Review ID 已锁定。
- 统计师已确认评分合同，并且无法访问 Review ID 到 Run ID 的映射。
- 只有在所有生成输出锁定后，评审阶段才可读取对应隐藏参考 SAP。

### 产出

- 两案例的 Protocol、amendment 和参考 SAP 日期/版本关系说明。
- 5 份 AI 结构化差异预审，包含事实位置、参考位置、差异摘要和待统计师判断项。
- 5 份统计师完成的最终评分表及专业判断说明。

### 最小执行顺序

1. **P4-A — 参考解锁与事实预审（AI 可独立完成）**
   - 只读取 `CASE-ONC-001/004` 的 Protocol 与隐藏参考 SAP，不读取保留案例。
   - 完成两案例的版本关系说明，并为 5 个 Review ID 生成事实型差异预审。
   - 预审只写生成位置、Protocol/参考 SAP 位置、差异摘要和待判断项；不得填写得分、严重度或 disposition。
2. **P4-B — 合格统计师盲评（人工依赖）**
   - 将参考 SAP 和对应 AI 预审加入现有匿名包，不暴露运行 arm、Run ID 或重复关系。
   - 统计师确认或修正预审，完成 6 个维度、hard gates、差异类别、严重度和最终 disposition。
   - 五份 scorecard 全部完成后锁定；锁定前不读取 Review ID 映射，不做 arm 效果比较。

### P4 Gate

- P4-A：两份版本关系说明与 5 份预审齐全；所有差异均有可核验定位；AI 评分字段保持空白。
- P4-B：5 份 scorecard 均完整、可解析且已锁定；统计师提交盲态声明；原生成产物、Skill 和评分合同未修改。
- P4-B 未完成时停在人工评审等待，不新增运行、不增加第二评审者、不建设新工具。

P4-A Gate 于 2026-09-01 通过：两个 active case 的版本关系已完成，5 份预审各含 6 个事实主题且无得分、严重度、差异类别或 disposition；五个匿名包均为 8 个文件并通过盲化标签、Protocol/参考 SAP 对应关系和空白 scorecard 检查。

### 完成标准

- [x] 版本关系说明区分 Protocol 可知信息、后续 Sponsor/运营决定和参考 SAP 的不明确内容。
- [x] AI 预审不读取 Review ID 映射，只预填可核验事实和定位，不替统计师做最终专业评分或 disposition。
- [ ] 统计师不知道对照/正式分组和重复运行关系，并逐项确认或修正 AI 预审。
- [ ] 每份评分表包含 6 个维度得分、hard gates、差异类别、严重度、优点、缺陷和最终 disposition。
- [ ] 评审期间不修改原输出、Skill、评分阈值或判分锚点。

### 边界（本 Phase 明确不做）

- 不把参考 SAP 的每项差异自动判错。
- 不向统计师暴露运行分组，也不在评审完成前做对照/正式效果比较。

### 涉及文件

| 文件 | 操作 | 预计行数 |
|------|------|----------|
| `.validation-work/generate-sap/oncology-phase1-2/comparison/version-alignment.yaml` | 完成 | +40-80 |
| `.validation-work/generate-sap/oncology-phase1-2/comparison/ai-prereview/` | 新增 | 5 份 |
| `.validation-work/generate-sap/oncology-phase1-2/comparison/statistician-review/` | 新增 | 5 份 |

### 关键决策

- 专业评审：AI 自评 / AI 预审加统计师终评 / 双统计师独立评审，选择 AI 预审加 1 名合格统计师终评；在控制成本的同时保留专业责任边界。

---

## P5: 解盲归因、验证结论和文档同步

### 输入条件

- P4 Gate 已通过，5 份统计师评分表均完成且不再修改。
- Review ID 映射仍未用于任何评分调整。

### 产出

- 解盲后的对照/正式运行比较、两次正式运行一致性分析和案例级结果。
- 按 6 类差异合同整理的发现清单、严重度、重复频率和根因归属。
- 首轮验证报告及明确结论：通过可行性门槛、需要后续最小修复，或存在需优先处理的安全缺陷。
- 主文档同步和后续计划建议；`CASE-ONC-002/003` 继续保持未见状态。

### 完成标准

- [ ] 解盲后按预注册公式计算单次分数、案例平均和 hard-gate 结果，不事后修改阈值。
- [ ] 先例价值同时报告有益补充和不当参数迁移；不以措辞接近参考 SAP 作为成功标准。
- [ ] 每个缺陷均关联输入事实、Skill 规则或证据项，并标记为单次、重复、跨案例或 critical。
- [ ] 单次措辞差异、合理替代方案和参考 SAP 后期决定不触发 Skill 修改；重复问题才进入普通修复候选，critical 安全问题可单次触发 P0 建议。
- [ ] 本计划不直接修改 Skill；如需修改，建立独立后续计划并以 `CASE-ONC-002/003` 作为修复后的未见回归集。
- [ ] `PROJECT_SPEC.md` 和 `TEST_GUIDE.md` 已同步真实验证状态、方法、结果和限制；未完成时不得把 `generate-sap` 标为已全面验证。

### 边界（本 Phase 明确不做）

- 不在看过 `CASE-ONC-001/004` 参考答案后直接调优并把同案例重跑结果作为独立验证。
- 不运行保留案例，不扩大疾病和试验设计覆盖声明。

### 涉及文件

| 文件 | 操作 | 预计行数 |
|------|------|----------|
| `.validation-work/generate-sap/oncology-phase1-2/comparison/validation-report.md` | 新建 | ~250 |
| `.validation-work/generate-sap/oncology-phase1-2/comparison/findings.yaml` | 新建 | ~120 |
| `docs/main/PROJECT_SPEC.md` | 修改 | +10-20 |
| `docs/main/TEST_GUIDE.md` | 修改 | +30-50 |
| `docs/dep/PLAN.md` | 更新生命周期 | +/−2 |

### 关键决策

- Skill 修改门控：运行中即时调优 / 解盲归因后另建计划，选择后者；避免目标答案污染和验证、开发职责混合。
- 后续回归：重跑已见案例 / 使用保留案例，选择优先使用 `CASE-ONC-002/003`；已见案例只用于确认具体缺陷修复，不承担独立验证结论。

---

## 执行中发现

> 执行本子计划过程中暴露的问题。每个 Phase Gate 时审查并分类。

| ID | 描述 | 发现于 | 类型 | 处理 |
|----|------|--------|------|------|
| FIND-P2-001 | 通用发现轮次曾返回目标记录；过滤后的非目标材料可通过内容审计，但该轮次不能证明自主盲搜能力 | P2 | validation-integrity | 两个 v1 bundle 标记为可用于生成输入、不可用于独立搜索评价；未来需以真正隔离的新搜索者另跑搜索验证 |
| FIND-P2-002 | 保留候选中没有足够接近 AML 小分子联合去甲基化药物设计的公开先例 | P2 | evidence-gap | `PB-ONC004-v1` 保持 `limited` 且只选 2 项，不用低相似实体瘤材料凑数 |

## 关键决策记录

| 日期 | 决策 | 选项 | 选择 | 理由 |
|------|------|------|------|------|
| 2026-08-27 | 最终评审配置 | 仅 AI / AI 预审 + 1 名统计师 / 双统计师 | AI 预审 + 1 名统计师 | 降低机械比对成本，同时保留专业判断边界 |
| 2026-08-27 | 首轮案例范围 | 单案例 / 两案例 + 两例保留 / 全部四例 | `CASE-ONC-001/004` 首轮，`002/003` 保留 | 同时覆盖实体瘤主基准和 AML 压力测试，避免消耗全部隐藏样本 |
| 2026-08-27 | 运行矩阵 | 每案例单次 / 对照 1 + 正式 2 / 多次统计重复 | 对照 1 + 正式 2 | 同时观察先例增益和明显运行冲突，评审量仍可控 |
| 2026-08-27 | 验证实现 | 仅人工 / 自动客观检查 + 统计师 / 完整评测框架 | 自动客观检查 + AI 预审 + 统计师 | 客观项可复现，专业项不交给自动脚本裁决 |
| 2026-08-27 | 运行锁定记录 | 文件哈希 / 简单标识符 | 简单标识符 | 用户要求最小记录方案；以 Run ID、版本标签和 `locked` 状态防止覆写 |
| 2026-08-27 | P2 搜索与包审计结论 | 将过滤后材料视为完整盲搜通过 / 区分内容有效性与搜索过程有效性 | 区分两者 | 现有材料未命中 denylist，可作冻结生成输入；原发现轮次曾出现目标记录，不能支持独立搜索验证结论 |
| 2026-08-27 | P3 运行配置 | 临时默认 / 锁定本机配置 | `gpt-5.6-sol`、`high`、应用内 Codex CLI 0.150.0-alpha.8 | 直接读取用户当前模型配置并显式传入每次运行；全局 CLI 0.138.0 不支持该模型，不能作为正式执行通道 |
| 2026-08-27 | P3 Gate 失败后的重跑策略 | 无限替代重跑 / 修改冻结输入后继续 / 停止并保留证据 | 停止并保留证据 | 1/6 输出有效，客观契约缺陷已跨案例和 arm 重现；修改 Skill/prompt 会破坏冻结验证，原配置继续重跑没有新增信息价值 |

## 同步记录

| 日期 | 已同步到 | 说明 |
|------|----------|------|
| 待完成 | `PROJECT_SPEC.md`, `TEST_GUIDE.md` | P5 完成后同步真实盲测状态、方法、结果与限制 |
