---
phase_index: 0
status: in-progress
created: 2026-08-27
updated: 2026-08-31
priority: 1
estimated_rounds: 2-4
depends_on: []
tags:
  - clinical-statistics
  - sap
  - skill-repair
  - output-contract
syncs_to:
  - PROJECT_SPEC.md
  - TEST_GUIDE.md
---

# Generate SAP 输出契约修复与客观 Gate 重验

> Lifecycle rule: this file's directory and `status` must match.
> `plans/backlog/` = `planning`; `plans/ongoing/` = `in-progress`; `plans/complete/` = `done`; `plans/deferred/` = `deferred`.

## 目标

对 `generate-sap` 做最小、机器可检查的输出契约修复，消除 P3 中重复出现的 References、固定章节标题、Source ID 和搜索状态错误；使用新版本标签重新执行隔离客观 Gate，通过后再恢复原盲评计划。

## 背景

- 当前状态：`P2-generate-sap-blind-validation` 的 P3 已完成两案例 6 个目标运行，但只有 `ONC004-C01` 通过客观检查；其余 5 个输出因结构或证据账本契约错误标为 `invalid`。
- 已确认根因：现有 Skill 分散描述了 Evidence Class、Content Unit、Precedent 和模板，却没有一处明确区分“当前研究来源”与“外部 Reference”的完整输出合同；固定通用章节标题和允许枚举也未形成可执行校验。
- 约束：隐藏参考 SAP 尚未读取；冻结的 `VAL-P2-v1` objective checker 不得为迁就现有输出而放宽；旧输出、报告和运行登记保持只读。
- 方案来源：用户于 2026-08-27 接受最小修复建议；采用轻量规划，不进行架构头脑风暴。
- Skill 设计原则：继续作为固定内容与逐项证据约束包，不增加 Agent Workflow、搜索服务、审批能力或专业统计裁决。

## 涉及范围

- **包含**：通用模板 18 个顶层章节标题的精确合同；当前研究事实与外部 Reference 的集合边界；外部 Reference 和 trial precedent 的必填字段与允许枚举；Content Unit 的 Source ID/Reference ID 引用完整性；`search_summary.status` 允许值；纯本地输出校验脚本；合成与既有失败产物回归；新版本隔离客观 Gate。
- **不包含**：读取隐藏参考 SAP；修改统计方法、Estimand、缺失数据、安全分析等专业规则；增加疾病或设计类型；修改先例包内容；放宽 `VAL-P2-v1` checker；静默后处理或手工修补生成结果；消耗 `CASE-ONC-002/003`；新增 MCP、GUI、知识库或 Agent Workflow。
- **与 P2 的边界**：本计划修复并以六个目标槽重验客观输出合同，同时从中收集后续专业盲评所需的 4+1 最小有效样本。执行层健康只冻结一次；六槽完成 L1 后再进入匿名包装和 L2 专业质量评审。

## 主文档影响

完成后需要更新：

- `PROJECT_SPEC.md`：在“接口契约”和“非功能需求”中补充当前研究来源与外部 Reference 分离、固定通用标题、允许枚举和输出自检边界。
- `TEST_GUIDE.md`：增加机器可检查输出合同、失败产物回归、新版本 6 次隔离客观 Gate 和不得放宽独立 checker 的测试约定。

`syncs_to` 和本节保持一致；本计划不改变项目架构或代码风格，因此不更新 `PROJECT_GUIDE.md` 和 `CODE_STYLE.md`。

---

## Phase 总览

| Phase | 目标 | 预估轮次 | 依赖 | 状态 |
|-------|------|----------|------|------|
| P1 | 固化机器可检查的输出契约并完成回归测试 | R007-R008 | - | done |
| P2 | 六槽完成 L1 输出合同 Gate，并以其中 4 个主样本 + 1 个重复样本恢复盲评入口 | R009-R043 | P1 | done（R16 L1 6/6 locked；L2 5 packages ready） |

---

## P1: 固化输出契约与回归测试

### 输入条件

- P3 的 6 份目标输出、客观检查报告和 `ONC001-C03` 早期失败报告保持原样，可用于客观结构回归，但不得读取隐藏参考 SAP。
- `generate-sap` 仍为 `draft`，当前触发策略、18 节总体结构和专业规则范围不变。
- `VAL-P2-v1` checker 作为独立验收基准保持冻结；修复不能通过修改 checker 达成。

### 产出

- 一个由 `SKILL.md` 每次调用加载的精简 `output-contract.md`，集中定义通用模板标题、Ledger 集合边界、字段、枚举和引用完整性。
- 更新后的 Generation Evidence Ledger 模板，清楚示范当前研究事实与外部 Reference 的分离，不留下可被复制成假证据的占位 Reference。
- 一个纯本地、无网络、无生成能力的输出校验脚本；只检查结构、标识符、枚举和追溯关系，不判断统计方法是否合理。
- 合成正负测试和既有 P3 产物回归，覆盖本轮全部客观失败类别。

### 完成标准

- [x] 使用 generic 模板时，18 个顶层章节标题必须与 `sap-template.md` / `section-map.md` 完全一致；Sponsor 模板存在时才允许按已提供模板变化。
- [x] 当前 Protocol、修订、已确认决定和 Sponsor 约定只通过 `document.source_versions` / `source_facts` 表达，不进入外部 `references`；冻结 bundle 是输入容器，不是 Reference。
- [x] `references` 只允许 `normative_reference`、`trial_precedent`、`method_reference`，并对 generic/precedent 两种记录执行完整字段、URL、日期和允许枚举检查。
- [x] `ContentUnit.references` 只引用已定义的外部 Reference ID；当前研究 Source ID 留在 `source_facts`，两类 ID 不混用。
- [x] `search_summary.status` 只允许 `completed`、`limited`、`unavailable`、`prohibited`、`not-run`；冻结包输入使用既有允许状态和明确限制，不新增临时枚举。
- [x] 新校验脚本对 `ONC004-C01` 返回通过，并对其余 5 个目标 invalid 输出及 `ONC001-C03` 返回失败；失败原因覆盖各自已有 objective report，不通过修改旧输出实现。
- [x] 合成测试至少覆盖：当前研究标识可出现在 Draft/Source Fact 但不得出现在外部搜索/Reference、bundle 不得成为 Reference、章节标题漂移、未定义 Source/Reference ID、非法 precedent/search 枚举。
- [x] `generate-sap/SKILL.md` 保持 500 行以内、渐进式披露和原显式调用边界；项目校验、Skill quick validator、相关测试、索引生成和安装均通过。

### P1 Gate（2026-08-27）

- `output-contract.md` 已集中定义标题、当前研究 Source、外部 Reference、ID 闭合与搜索状态；`SKILL.md` 每次调用加载，仍为 72 行。
- 包内校验器只读检查 Draft/Ledger，不联网、不生成、不改写，也不判断统计方法。
- 7 个测试通过；本地既有产物回归保持 `ONC004-C01` 通过、其余 5 个目标输出及 `ONC001-C03` 失败，且覆盖原 objective report 的失败类别。
- 项目 3/3 Skill 校验、官方 quick validator、索引生成、安装和 `git diff --check` 均通过；P2 尚未启动。

### 边界（本 Phase 明确不做）

- 不根据任何目标研究隐藏 SAP 或专业比较结果调整规则。
- 不增加新的统计分析建议、治疗领域特例、模板章节或搜索来源。
- 不把校验脚本扩展成生成器、工作流、审批器或专业 Validation Engine。
- 不自动改写不合格输出；脚本只能报告失败并返回非零状态。

### 涉及文件

| 文件 | 操作 | 预计行数 |
|------|------|----------|
| `generate-sap/SKILL.md` | 修改 | +10-20 |
| `generate-sap/references/output-contract.md` | 新建 | ~120-180 |
| `generate-sap/assets/generation-record-template.yaml` | 修改 | +20-40 |
| `generate-sap/scripts/validate_output_contract.py` | 新建 | 464 |
| `generate-sap/evals/evals.json` | 修改 | +3 expectations |
| `tests/test_generate_sap_output_contract.py` | 新建 | 244 |
| `.skill-registry.json` | 更新版本日期/状态 | +/−2 |
| `SKILL_INDEX.md` | 重新生成 | generated |

### 关键决策

- 修复形态：继续增加分散提示 / 集中输出合同 / 引入运行时 schema 服务，选择“集中输出合同 + 包内纯校验脚本”；P3 已证明分散提示和模型自检不足，而独立服务超出 Skill Layer。
- 当前研究来源建模：与外部 References 合并 / 分离，选择分离；避免目标研究标识进入外部搜索与泄漏审计范围，同时保持事实追溯。
- 验收基准：修改 `VAL-P2-v1` / 保持冻结，选择保持冻结；防止事后移动 Gate。

---

## P2: 新版本隔离客观 Gate

### 输入条件

- P1 全部完成标准通过，修复后的 Skill 已获得新的简单版本标签并安装；旧版本和旧输出保持只读。
- 新校验脚本与冻结 `VAL-P2-v1` checker 对合成回归的通过/失败结论一致。
- 两个目标 Protocol 和两个冻结先例包未变化；隐藏参考 SAP、manifest 和 denylist 仍不向生成会话暴露。

### 产出

- 新版本的六个 L1 目标槽：每案例 1 次 Protocol-only、2 次 Protocol + 原冻结先例包，全部完成独立四道 Gate。
- L2 使用四个主样本（两个案例分别各 1 次 Protocol-only 和 1 次 precedent）及一个预注册重复样本（`ONC001` precedent repeat）评估关键决策和结构稳定性。
- 每个目标槽的独立 objective report、运行登记和只读输出；旧 P3 Run ID、输出和报告不覆写。
- 六槽 L1 锁定后的 Review ID 映射、匿名评审包和 4+1 跨 case 质量比较，并将原 P2 计划恢复到专业评审阶段。

### 完成标准

- [x] L0 技术健康检查已通过并冻结；writer、builder、auditor、validator 和 checker 不再作为每个临床样本的重复验证目标。
- [ ] 6 个目标槽均使用相同的新 Skill 标签、`gpt-5.6-sol`、`high` 和独立 ephemeral 会话；生成会话继续禁用外部网络工具、插件、Apps、浏览器和 MCP。
- [ ] 每次运行只读取该 arm 允许的目标 Protocol 和冻结先例包；未读取旧输出、隐藏参考 SAP、manifest、denylist 或其他运行目录。
- [ ] 每份有效输出先通过包内校验脚本，再由未修改的 `VAL-P2-v1` checker 独立检查；随后进入独立临床质量评审。
- [ ] 产品失败原样保留并计入 Skill 验证；capacity、CLI、宿主中断、缺少辅助可执行文件或 auditor 实现缺陷标记为 infrastructure invalid-run，不进入 Skill 质量分母，只替换受影响样本且不重置已通过样本。
- [x] 有效输出标记为 `locked`，匿名评审包不暴露 C/P、Run ID、bundle 标签或重复关系；映射文件仅供后续评审控制者使用。
- [x] 更新原 `P2-generate-sap-blind-validation`：明确本轮为 post-remediation 客观重验，不把它表述为未调优的首次盲测；P3 Gate 通过并恢复 P4 入口。
- [ ] 同步 `PROJECT_SPEC.md`、`TEST_GUIDE.md` 和项目记忆；项目全量校验、相关测试和 `git diff --check` 通过。

### P2 Gate 结果（2026-08-27）

- `REMEDIATION-01` 已冻结 `GSAP-OC1-20260827`、`VAL-P2-v1`、6 个新矩阵槽及各自隔离输入；隐藏参考 SAP、旧输出、manifest 和 denylist 均未暴露给生成会话。
- `ONC001-R1-C01` 在任何输出产生前因 Windows 写入通道失败而失效；依照每槽最多一次替代规则启动 `ONC001-R1-C02`。
- 替代运行生成了三件套，但主稿只成功写入第 1–6 节。第 7–18 节的长 PowerShell 追加命令失败，导致包内校验器和冻结 `VAL-P2-v1` checker 均失败；客观报告为 2 个失败检查、0 个警告，且目标泄漏检查通过。
- 该失败发生在内容已存在之后，因此产物和报告原样保留，剩余 5 个矩阵槽标记为 `not-run-phase-stopped`；未修改 Skill、prompt、validator、checker 或失败输出，未创建匿名包，未启动 P4。
- 当前结论只说明本轮生成执行通道不能可靠落盘长文档；尚不能据此否定 P1 的输出合同修复，也不能宣称 post-remediation 客观 Gate 已通过。

### P2 后续写入通道修复（正式 Gate 外，2026-08-27）

- 未修改 `remediation-01`、失败输出、Skill、validator 或冻结 checker；新的 helper 和候选控制器单独保存在本地忽略的 `write-channel-smoke/`。
- helper 只允许三个既定 artifact 名称，单块最多 3,500 字符；候选提示进一步限制为 3,000 字符，正文经标准输入写入，禁止把长正文作为 PowerShell 参数或使用临时落盘方案。
- 本地 smoke 将 102,200 字符按 2,400 字符块完整重组，并确认超限块和路径逃逸被拒绝。
- 首次真实 CLI smoke 因误触发全局 `personal-assistant`、读取用户目录而标记 invalid 并单独保留；修正为纯执行协议且禁用 Skill 搜索后的第二次 smoke 通过，生成 24,417 字符、18 个标题，最大命令长度 1,520 字符，未出现被禁写法或外部路径读取。
- 候选控制器在生成会话完全退出后才运行包内结构校验，因此首次非零校验发生时生成者已无法现场改写；新的临床 Gate 尚未启动。

### P2 第二次 Gate 结果（2026-08-28）

- `REMEDIATION-02` 冻结新 Run ID、同一 `GSAP-OC1-20260827` Skill、未修改的 `VAL-P2-v1` checker、通过 smoke 的 helper/控制器及 6 个新隔离输入包。
- `ONC001-R2-C01` 在模型调用前因 Codex 应用更新移除旧 build 路径而失败；只重钉同版本 CLI 0.150.0-alpha.8 的新路径，并使用该槽唯一替代 `ONC001-R2-C02`。
- 替代运行只读取 run-local Protocol、Skill 和 control，未读取隐藏 SAP、旧输出、全局 Skill 或网络资源；生成了完整大小的三件套，单个 helper payload 上限也确实生效。
- 包内 validator 在会话退出后发现 Ledger YAML 无效：`--strip-pipeline-newline` 删除块尾换行，而后续块没有独立分隔符，导致相邻 sequence entry 拼接在第 25 行。冻结 checker 因同一解析错误无法进入客观检查逻辑。
- 该失败发生在三件套已存在之后，按预注册规则将运行标记为 `invalid-content-failure`，原样保留输出与事件日志并停止其余 5 槽；未修改失败输出、Skill、prompt、validator 或 checker，未创建匿名包或启动 P4。
- 执行审计另发现模型虽然把每个 payload 控制在上限内，仍把多个 helper 调用聚合为单条 shell 命令，最大 29,444 字符；这不构成本轮隔离泄漏，但说明上一轮 smoke 未覆盖真实 YAML 边界和“每命令单次写入”约束。

### P2 第二次写入通道修复（正式 Gate 外，2026-08-28）

- 保持 `remediation-02`、失败三件套、Skill、prompt、validator 和冻结 checker 不变；新候选单独保存在本地忽略的 `write-channel-smoke-v2/`，标签为 `CTRL-STDIN-02` / `WRITE-CHUNK-02`。
- helper 在 append 时检查文件尾和 payload 首字符；只有两侧都没有换行时插入一个 `\n`，不改写块内部内容，也不要求模型承担 YAML/Markdown 连接边界。
- 控制提示固定完整 UTF-8 命令模板，并要求每条 shell command 恰好一次 `$chunk` 与一次 helper 调用；会话后审计拒绝多次 writer、超过 6,000 字符、失败 writer、被禁写法、外部路径和网络命令。
- 本地 smoke 将 102,199 字符按完整行边界重组一致，四段无首尾连接换行的 YAML 可解析；超限块和路径逃逸继续被拒绝。
- 旧 `ONC001-R2-C02` 事件回放按预期失败：检测到 9 条聚合 writer 命令、8 条超长命令和 1 条失败 writer，证明审计器覆盖已知失效模式。
- 首次真实 CLI smoke 因提示未给出精确 helper 参数和 UTF-8 模板而产生多次失败 writer，保留为 `agent-attempt-01` invalid；补齐固定模板后的全新 `agent-attempt-02` 通过：60 项 UTF-8 YAML、6 条独立 writer 命令、最大 1,114 字符，0 聚合、失败、越权或网络命令。
- 当前只证明写入与审计通道满足技术合同，未启动新 remediation、临床生成或统计内容验证。

### P2 第三次 Gate 结果（2026-08-28）

- `REMEDIATION-03` 冻结全新 R3 Run ID、同一 `GSAP-OC1-20260827` Skill、未修改的包内 validator 与 `VAL-P2-v1` checker，以及通过 v2 smoke 的 `CTRL-STDIN-02` / `WRITE-CHUNK-02`；6 个输出目录初始为空。
- 首槽 `ONC001-R3-C01` 完成 Protocol-only 生成并产出 36,662 字节 Draft、38,416 字节 Ledger 和 10,567 字节 Open Questions/References；生成会话未使用网络、外部路径或全局 Skill。
- 会话后写命令审计通过：40 条独立 writer 命令，最大 3,509 字符，0 条聚合、超长、失败、被禁写、外部路径或网络命令。v2 技术通道在真实临床长文档上通过。
- 包内 validator 随后在 Ledger 第 417 行停止：`assumptions` 流式 sequence 以 `}` 而非 `]` 结束，导致 YAML 不可解析。冻结 checker 按校验顺序未运行。
- 该错误发生在三件套已存在后，属于内容契约失败；运行标记为 `invalid-content-failure`，其余 5 槽标记 `not-run-phase-stopped`。失败输出、Skill、prompt、helper、auditor、validator 和 checker 均未修改。
- 当前根因已与 Windows 写入链路分离：受控写入和命令审计有效，但让模型手写 38 KB 结构化 YAML 仍会产生单字符语法错误。不能把 R3 计为 Gate 通过，也不能通过修补该字符继续矩阵。

### P2 第三次 Ledger 序列化修复（正式 Gate 外，2026-08-28）

- 事件日志证明 R3 的错误 `}` 在进入 writer 前已存在；因此保持 `remediation-03`、失败输出、validator 和冻结 checker 不变，只修改 Skill 包的机械序列化边界。
- 新增 `build_evidence_ledger.py`：模型每次提交一个不超过 3,500 字符的 JSON object；脚本在写入私有 JSONL 暂存前检查语法、单例、稳定 ID、重复和固定输出路径，最终按固定顶层顺序一次性生成 UTF-8 YAML 并删除暂存。
- builder 不解释临床内容、不补写缺失字段、不修复统计语义，也不取代 `validate_output_contract.py`；最终文件存在时拒绝覆盖。
- 测试先行确认脚本缺失时失败；实现后 4 个 builder 测试及项目 11 个单元测试通过。本地 smoke 组装 18 节、60 内容项、25 问题和 25 一致性项，错误 JSON 被拒绝且暂存未变化。
- 真实 CLI 非临床 smoke 完成 60 条目标记录和一次 finalize，最终 YAML 可解析、稳定 ID 顺序正确、暂存已清除，最大命令 566 字符，未使用网络、外部路径或被禁写法。代理首次误用 `question_id`，builder 安全拒绝后以 `query_id` 重试，因此审计为 `pass_with_recovery`，不是零错误通过。
- 本轮没有创建新 remediation、临床 Run ID、匿名包或专业评审；是否重新启动 6/6 临床客观 Gate 仍需单独决定。

### P2 第四次 Gate 预注册（2026-08-28）

- 用户确认继续后建立 `REMEDIATION-04`，冻结 `GSAP-OC2-20260828`、`CTRL-LEDGER-01`、`WRITE-CHUNK-02-MD`、`LEDGER-RECORD-01` 和未修改的 `VAL-P2-v1` checker；不使用哈希标识。
- 六个全新 Run ID 为 `ONC001-R4-C01/P01/P02` 与 `ONC004-R4-C01/P01/P02`。输入分别与 R3 冻结输入逐文件、逐字节一致；Skill 与当前已验证包逐文件、逐字节一致；初始输出均为空。
- Markdown Draft 与 Open Questions/References 继续使用受限分块 writer；writer 明确拒绝 Ledger 目标。Ledger 只允许逐条 JSON 进入 builder，要求 18 条 `section_status`、唯一 singleton/稳定 ID、所有命令成功和一次 finalize。
- builder 任一拒绝即停止，不得在正式运行内重试或改变记录；生成会话退出后依次执行 Markdown 命令审计、Ledger 命令审计、包内 validator 和冻结 objective checker。
- 隐藏 SAP、旧输出、manifest、denylist、run register 和 comparison 材料均不进入生成工作区；首个内容或通道失败仍原样停止整个 Phase。

### P2 第四次 Gate 结果（2026-08-28）

- `ONC001-R4-C01` 只读取 run-local Skill 和 Protocol；外部路径、网络、全局 Skill 和 Ledger builder 命令均为 0。Protocol 文本层通过本地 `fitz` 读取，未安装依赖或写临时解析文件。
- Draft 首块 2,989 字符成功；第二块为 3,238 字符，超过 register 与提示冻结的 3,000 字符模型上限，但低于 helper 的 3,500 字符上限，因此 writer 返回成功并把部分 Draft 写至 6,244 字节。
- 控制者在观察到该差异后立即终止生成，CLI 退出 1；Ledger 和 Open Questions/References 尚未创建，双通道审计、包内 validator 与 objective checker 均未进入正式顺序。
- 会话后只读审计确认 30 条完成命令、2 条成功 writer、最大 writer 命令 3,580 字符、0 外部路径和 0 网络命令。冻结 writer auditor 返回 pass，进一步证明它只检查命令长度而未执行 3,000 字符 payload 合同。
- 运行标记 `invalid-execution-control-failure`，部分 Draft、events 和独立 violation report 原样保留；剩余 5 槽标记 `not-run-phase-stopped`。R4 helper、auditor、输出、Skill、validator 和 checker 未修改。

### P2 第四次写入控制修复（正式 Gate 外，2026-08-28）

- 在独立忽略目录 `write-channel-smoke-v3/` 复制 R4 helper，先添加精确边界测试。原实现对 3,001 字符返回成功，测试按预期失败；这复现了同一根因而不是 R4 的偶发症状。
- 候选 `WRITE-CHUNK-03` 只把 helper 的硬上限从 3,500 收敛为 3,000，不修改连接换行、目标白名单、写入方式或 artifact 内容。
- 修复后 3,000 字符成功，3,001 字符在文件创建前拒绝，2/2 测试和 Python 编译通过。未来控制器应只注册一个 3,000 字符硬合同；提示可以建议更短目标块，但不能另设一个未执行的合格上限。
- 当前未建立新 remediation 或临床 Run ID；R4 和此前失败证据保持冻结。

### P2 第五次 Gate 预注册（2026-08-28）

- 用户确认继续后建立 `REMEDIATION-05`，冻结全新 R5 Run ID、`CTRL-LEDGER-02`、`WRITE-CHUNK-03`、原 `LEDGER-RECORD-01`、`GSAP-OC2-20260828` 和未修改的 `VAL-P2-v1` checker。
- 六个输入包与 R4 对应输入逐文件、逐字节一致，Skill 与当前已验证包逐文件、逐字节一致；checker、denylist 和双通道 auditor 与 R4 完全一致，6 个初始输出均为空。
- Markdown helper 将唯一硬上限直接设为 3,000 字符；3,000/3,001 精确边界测试通过。提示仅建议按不超过约 2,400 字符组织内容，不把建议值注册为第二个合格阈值。
- Ledger 继续逐记录 JSON、所有 add 成功、18 条 `section_status` 和一次 finalize；验证顺序与 R4 不变。任何 helper/builder 拒绝、命令审计失败或内容失败均停止并保留。
- R4 部分 Draft、events、run register 和 violation report 保持只读；隐藏 SAP、旧输出、manifest、denylist 和 comparison 材料不进入 R5 生成工作区。

### P2 第五次 Gate 结果与审计缺陷复现（2026-08-28）

- `ONC001-R5-C01` 生成会话成功产生三件套：Draft 28,870 bytes、Ledger 32,823 bytes、Open Questions/References 8,008 bytes。16 条 Markdown writer 的最大 payload 为 2,886 字符；63 次 Ledger add 和唯一一次 finalize 均成功，暂存文件已清除。
- 冻结 Markdown auditor 随后把 `item_48` 判为“Ledger sent through Markdown writer”并返回非零。实际命令的 `--target` 是 `sap-review-draft.md`；只因 Draft payload 的附录文字提到独立文件名 `generation-evidence-ledger.yaml`，整命令字符串包含该名称而触发误报。
- 按预注册顺序，R5 标记 `stopped-execution-control-failure`，三件套、events 和 audit report 原样保留；Ledger auditor、包内 validator、冻结 objective checker 以及剩余 5 槽均未运行。后验确认误报不改变正式 Gate 结果。
- 在正式 Gate 外建立 `write-channel-audit-smoke-v4/`。冻结 auditor 对“payload 仅提到 Ledger 名称”和“实际 Ledger target”两例只通过 1/2；候选 auditor 只解析 writer 调用后的 `--target` 实参，2/2 通过，并对 R5 events 只读回放为 pass。
- 当前未建立新的 remediation 或临床 Run ID；候选回放不计入 R5，不得据此补跑 R5 validator/checker 或恢复剩余矩阵。

### P2 第六次 Gate 预注册（2026-08-28）

- Goal 模式授权持续推进后建立 `REMEDIATION-06`，冻结 6 个全新 R6 Run ID、`CTRL-LEDGER-03`、`WRITE-CHUNK-03`、`WRITE-AUDIT-02`、`LEDGER-RECORD-01`、`GSAP-OC2-20260828` 和未修改的 `VAL-P2-v1` checker。
- R6 只把 Markdown auditor 从“整命令文件名子串”改为“解析唯一 writer 调用后的 `--target` 实参”；controller、writer、Ledger auditor/builder、validator、checker、denylist、提示和统计内容规则与 R5 逐字节一致。
- target 检测合成测试覆盖无引号、双引号、单引号和 `--target=`：冻结 R5 auditor 为 3/5，R6 auditor 为 5/5；R6 auditor 对 R5 events 的只读回放为 pass。writer 的 3,000/3,001 精确边界仍为 2/2。
- 六个 R6 输入与 R5 对应输入逐文件、逐字节一致，Skill 与当前已验证树一致；输入文件数为 1/8/8/1/6/6，Skill 均为 27 个文件，所有输出目录为空。
- 验证顺序不变：生成退出 → Markdown audit → Ledger audit → package validator → frozen objective checker。任一正式失败仍停止并保留，不使用后验候选替换同一 Gate。

### P2 第六次 Gate 结果与分块控制候选（2026-08-28）

- `ONC001-R6-C01` 首个 Draft 块以 2,941 字符成功写入；第二块把顶层 Section 5 和 6 合并为 3,605 字符，被 `WRITE-CHUNK-03` 在写入前安全拒绝。输出保持仅 2,943 bytes 的首块 Draft，Ledger 与 Open Questions/References 未开始。
- 冻结提示只对 Ledger add 明确写了“拒绝即停止”，生成者因此声称 Markdown 拒绝可以拆块重试并启动 `item_29`。控制者按正式 Gate 规则中断；该命令只有 started、没有 completed，输出大小未变化。
- 后验冻结 auditor 正确报告 `failed writer commands: item_27`；21 条完成命令中无外部路径或网络命令。R6 标记 `stopped-execution-control-failure`，其余 5 槽、Ledger audit、validator 和 checker 均未运行。
- Gate 外 `write-channel-smoke-v5` 先对 R6 controller 复现两项缺失指令为 0/2；候选只新增“每个 Markdown 块最多一个编号顶层章节，超长章节提交前按子节/段落拆分”和“任何 Markdown writer 拒绝立即停止且不得重试”，随后 2/2 与 PowerShell 语法通过。
- 当前候选未回填 R6；下一 remediation 继续使用原 3,000 硬限，不建立第二个合格阈值，也不修改统计内容规则。

### P2 第七次 Gate 预注册（2026-08-28）

- 建立并冻结 `REMEDIATION-07`、6 个全新 R7 Run ID、`CTRL-LEDGER-04`、原 `WRITE-CHUNK-03` / `WRITE-AUDIT-02` / `LEDGER-RECORD-01`、`GSAP-OC2-20260828` 和未修改的 `VAL-P2-v1`。
- R7 输入、Skill 和除 controller 外的全部控制与 R6 对应项逐文件、逐字节一致；controller 只新增 v5 已验证的两条 Markdown 分块/停止指令，未改提示其他内容、验证顺序或 shell 模板。
- 冻结前 writer 边界 2/2、target 检测 5/5、controller Markdown policy 2/2、Python/PowerShell 语法和六个空输出目录全部通过；输入文件数与 Skill 文件数仍为 1/8/8/1/6/6 和每槽 27。
- 正式失败处理不变；R6 首块/事件/报告保持只读，R7 不读取或复用其内容。

### P2 第七次 Gate 结果与 Ledger auditor 候选（2026-08-28）

- `ONC001-R7-C01` 与 `ONC001-R7-P01` 均完成三件套、Markdown audit、Ledger audit、package validator 和冻结 `VAL-P2-v1` checker；两槽均为 0 failed checks、0 warnings，已分别锁定。
- `ONC001-R7-P02` 完成三件套后，冻结 Ledger auditor 把只读命令 `Get-Content .../build_evidence_ledger.py` 计为非法 builder 调用 `item_66`。正式 Ledger audit 因此失败；validator/checker 与 ONC004 三槽未运行，失败产物和报告原样保留。
- Gate 外 `ledger-auditor-smoke-v1` 以“只读源码、正文提及、实际 add、实际 finalize、非法子命令”五例复现：冻结检测 3/5，候选 5/5。候选仅识别由 Python 实际执行的 builder，并对 R7 C01/P01/P02 events 只读回放全部通过。
- 该结果仅证明冻结 auditor 的调用识别误报，不改变 R7 的正式失败结论，也不补跑 R7 后续 Gate。

### P2 第八次 Gate 预注册（2026-08-28）

- 建立并冻结 `REMEDIATION-08` 与六个全新 R8 Run ID。唯一批准增量为 `LEDGER-AUDIT-02` 的 builder 调用识别；controller、Markdown writer/auditor、Ledger builder、validator、checker、denylist、提示及统计规则均与 R7 一致。
- 六槽输入与 Skill 同 R7 对应槽逐文件、逐字节一致；输入数仍为 1/8/8/1/6/6，Skill 每槽 27 个文件，全部输出目录为空。
- 冻结测试为 detection 5/5、R7 三组 events 回放 pass、Python/PowerShell 语法 pass；执行顺序和失败即停规则不变。

### P2 第八次 Gate 结果与宿主中断（2026-08-31）

- `ONC001-R8-C01` 完成三件套并依次通过 Markdown audit、Ledger audit、包内 validator 和冻结 `VAL-P2-v1` checker；结果为 0 failed checks、0 warnings，已锁定。
- `ONC001-R8-P01` 在 12 次 Markdown writer 成功后保留了 17,597 bytes 的部分 Draft；Ledger 与 Open Questions/References 尚未创建，事件流没有 `turn.completed` 或 `turn.failed`，末尾为 response stream disconnect。
- 恢复时原冻结构建 `CODEX-BUILD-D5F4` 已从宿主移除，控制器无法再次启动。该运行已产生输出，不符合“输出前最多一次替代”条件，因此标记为 `invalid-execution-interruption`，部分产物与事件原样保留，其余 R8 槽停止。
- 没有观察到 Skill 内容失败、writer/builder 拒绝、双审计失败、包内合同失败或 objective failure；这些 Gate 均未在 P01 启动。R8 失败归类为宿主执行环境中断，不据此修改 SAP 规则或输出。

### P2 第九次 Gate 预注册（2026-08-31）

- 建立并冻结 `REMEDIATION-09` 与六个全新 R9 Run ID。唯一批准变化是将已不可用的 CLI 0.150.0-alpha.8 构建替换为当前 bundled CLI 0.150.0-alpha.12.2，并登记 `CTRL-CLI-05` / `CODEX-BUILD-D664`。
- 当前 CLI 使用同一模型、推理配置、隔离参数和禁用项完成无工具 smoke，返回 `BUILD_READY`。controller 除可执行文件路径外与 R8 一致，PowerShell 语法通过。
- 六槽输入与 Skill 同 R8 对应槽逐文件逐字节一致；输入数仍为 1/8/8/1/6/6，Skill 每槽 27 个文件，输出目录全部为空。writer、双 auditor、Ledger builder、validator、checker、denylist、提示和统计规则均未修改。
- 正式顺序与失败即停策略不变；R8 的锁定/部分输出不会进入 R9 生成会话或计入 R9 的 6/6。

### P2 第九次 Gate 结果与 writer 样板修复（2026-08-31）

- `ONC001-R9-C01` 前 7 条 Markdown writer 成功，第 8 条命令把冻结样板中的 `$OutputEncoding` 表达式误写为多一个 `]`，PowerShell 在 helper 启动前返回 ParserError。生成者按规则停止且未重试。
- 冻结 Markdown audit 报告 `item_63` 为 failed writer；部分 Draft 7,533 bytes 原样保留，Ledger、Open Questions/References、Ledger audit、validator、checker 及其余 R9 槽均未运行。
- Gate 外 `writer-boilerplate-smoke-v1` 稳定复现同一 ParserError。删除重复的 `$OutputEncoding` / `PYTHONIOENCODING` 赋值后，同一 PowerShell 7 与 `python -X utf8` 通道对 Markdown 和 Ledger 多语言内容均逐字通过。
- 根因是模型在每条写命令中重复手抄非必要编码样板，不是 writer、builder、artifact schema 或统计内容失败。

### P2 第十次 Gate 预注册（2026-08-31）

- 建立并冻结 `REMEDIATION-10`、六个全新 R10 Run ID 和 `CTRL-BOILERPLATE-06`。controller 仅从 Markdown/Ledger 两个固定模板删除四行重复编码赋值，并明确禁止重新添加；helper 调用、参数、限制、拒绝停止和验证顺序不变。
- 六槽输入与 Skill 同 R9 对应槽逐文件逐字节一致；输入数为 1/8/8/1/6/6、Skill 每槽 27，输出均为空。除 controller 批准增量外，writer、双 auditor、builder、validator、checker 和 denylist 一致。
- 冻结测试包括原错误样板 fail-as-expected、Markdown UTF-8 pass、Ledger UTF-8 pass、controller PowerShell 语法 pass 和精确 diff 审计。

### P2 第十次 Gate 结果与 detached launcher 修复（2026-08-31）

- `ONC001-R10-C01` 成功越过 R9 的样板失败点，连续完成 16 条 Markdown writer 并保留 25,726 bytes Draft；无 failed writer，最后完成内容已进入 Section 12。
- 当前交互 turn 中断后，统一执行句柄消失；事件日志没有 `turn.completed` / `turn.failed`，Ledger、Open Questions/References 和全部后置 Gate 未开始。部分输出与 events 原样保留，R10 标记为 `invalid-execution-interruption`，其余槽停止。
- 这证明 `CTRL-BOILERPLATE-06` 的模板简化有效，但前台控制器仍与交互 turn 生命周期耦合。该问题与 R8 的输出后中断同类，不据此修改 Skill、提示内容或统计规则。
- Gate 外 `background-launcher-smoke-v1` 先证明隐藏子进程在启动调用返回后继续运行，再以两层 launcher/monitor 模拟正式控制器：前台立即返回，monitor 独立等待 12 秒并写出 `controller_exit_code: 0`。

### P2 第十一次 Gate 预注册（2026-08-31）

- 建立并冻结 `REMEDIATION-11`、六个全新 R11 Run ID、`DETACHED-LAUNCH-01` 与 `DETACHED-MONITOR-01`。唯一批准增量是用隐藏后台 monitor 启动并等待未修改的 `CTRL-BOILERPLATE-06`，同时记录 launch PID、控制器 stdout/stderr 和终止 exit code。
- 六槽输入、Skill 和生成控制器与 R10 对应槽逐文件逐字节一致；输入数为 1/8/8/1/6/6、Skill 每槽 27，输出均为空。writer、双 auditor、builder、validator、checker、denylist、提示和统计规则未修改。
- launcher/monitor PowerShell 语法、前台返回、后台生存和终止状态记录均通过。正式 Gate 仍由原控制器按既定顺序执行，后台层不读取临床输入或生成产物内容。

### P2 第十一次 Gate 结果与第十二次预注册（2026-08-31）

- `ONC001-R11-C01` 的 detached monitor 正常启动并在约 4 秒后记录 `controller_exit_code: 1`；控制器在生成前检查到冻结的 `CODEX-BUILD-D664` 已被桌面应用更新清理。输出文件数为 0，四道正式 Gate 均未开始，R11 现场原样保留且同 Run ID 不重启。
- Gate 外 `CLI-BUILD-SMOKE-03` 使用当前 `CODEX-BUILD-B993`（CLI `0.151.0-alpha.7.2`）和正式模型、隔离、禁网、功能禁用参数完成真实 roundtrip：退出码 0、`turn.completed` 完整、返回 `CLI_BUILD_SMOKE_OK`。
- 建立并冻结 `REMEDIATION-12` 与六个全新 R12 Run ID。唯一批准增量是把控制器可执行路径从已不存在的 D664 重钉到已通过 smoke 的 B993；R11 的 detached launcher/monitor、输入、Skill、提示、writer、双 auditor、builder、validator、denylist 和 `VAL-P2-v1` checker 均保持不变。
- 六槽输入数仍为 1/8/8/1/6/6，Skill 每槽 27 个文件，输出均为空；生成控制器除可执行路径外与 R11 一致且 PowerShell 语法通过。

### P2 第十二次 Gate 执行进度（2026-08-31）

- `ONC001-R12-C01` 由 detached monitor 完整运行至 `controller_exit_code: 0`。三件套齐全，临时 Ledger staging 已清除。
- Markdown audit 为 pass（31 次 writer、最大命令 2,514 字符）；Ledger audit 为 pass（68 次 add、1 次 finalize）；包内 validator 为 pass；冻结 `VAL-P2-v1` 为 9/9 pass、0 warning。该槽已锁定。
- `ONC001-R12-P01` 亦完成四道 Gate：Markdown audit 36 次 writer；Ledger audit 78 add + 1 finalize（含 3 条 reference）；包 validator 与冻结 checker 全通过，0 warning，已锁定。
- `ONC001-R12-P02` 独立完成四道 Gate：Markdown audit 29 次 writer；Ledger audit 73 add + 1 finalize（含 3 条 reference）；包 validator 与冻结 checker 全通过，0 warning，已锁定。
- CASE-ONC-001 三槽达到 3/3 locked；`ONC004-R12-C01` 随后完成三件套并通过 Markdown audit，但 Ledger audit 检出一次额外的实际 builder 探查调用：`build_evidence_ledger.py --help`。
- 该调用不属于允许的 record add 或唯一 finalize，冻结 auditor 正确返回 fail；包 validator、objective checker 与余下两个槽均未运行。R12 失败产物、事件和报告原样保留，不沿用前三槽通过结果。

### P2 第十三次 Gate 预注册（2026-08-31）

- Gate 外 `LEDGER-PROMPT-SMOKE-01` 首次因简化提示遗漏正式隔离条款而在写入前中止；补齐正式控制器已有的全局 Skill/外部路径禁令后，以当前 B993、`gpt-5.6-sol/high` 和禁网配置完成 21 次 add 与 1 次 finalize。
- 冻结 Ledger auditor 对第二次 smoke 返回 pass：18 个 `section_status`、1 个 `document`、1 个 `content_unit`、1 个 `search_summary`，unexpected/failed/external/network 均为 0。
- 建立 `REMEDIATION-13` 与六个全新 R13 Run ID。唯一批准增量是在 Ledger 指令中明确：builder 只可执行逐记录 add 和一次 finalize，禁止 `--help`、无子命令及 inspection/testing 调用；auditor、builder、Skill、统计规则、writer、validator、denylist、checker、launcher/monitor 和运行时均不变。
- 六槽输入与 R12 对应槽逐文件内容一致，文件数为 1/8/8/1/6/6；每槽 Skill 27 个文件，输出均为空。控制器逐行确认只有上述一条新增指令，其他控制文件一致，PowerShell/YAML 语法与固定 B993 可用性检查通过。

### P2 第十三次 Gate 结果与第十四次预注册（2026-08-31）

- `ONC001-R13-C01` 完成 7 次受控 Draft writer 后，后端返回 `Selected model is at capacity` 并产生 `turn.failed`；monitor 记录控制器退出码 1。仅保留 8,373 bytes 部分 Draft，Ledger 未开始，四道正式 Gate 均未运行。
- R13 同 Run ID 不重试、其余五槽不运行；该失败不归因于 Skill、统计内容、writer、Ledger 指令或 auditor。
- Gate 外 `CLI-CAPACITY-SMOKE-01` 随后以同一 B993、`gpt-5.6-sol/high`、ephemeral/禁网参数返回 `CAPACITY_READY`，具有完整 `turn.completed` 且退出码 0。
- 建立并冻结 `REMEDIATION-14` 与六个新 R14 Run ID，不含任何功能性增量。生成控制器和所有运行控制与 R13 内容一致；输入/Skill 与对应槽一致，计数仍为 1/8/8/1/6/6 和每槽 27，输出全为空；PowerShell/YAML、运行控制同步及 B993 可用性检查通过。

### P2 第十四次 Gate 结果与第十五次预注册（2026-08-31）

- `ONC001-R14-C01` 完成 Draft 与 Open Questions/References，共 28 次 Markdown writer 且 Markdown audit 通过；随后连续完成 21 次 Ledger add。
- 第 22 次实际 builder 命令 `item_87`（记录 `SAP-13-002`）在命令执行层返回 `status: failed`、`exit_code: null` 且无输出，staging 未变化。生成者按冻结规则停止、不重试、不 finalize；Ledger audit 因 22 add / 0 finalize 返回 fail，package validator 与 `VAL-P2-v1` 未运行，R14 其余五槽停止并保留现场。
- Gate 外 `LEDGER-COMMAND-REPLAY-01` 中，attempt-01 因重放脚本缩进无效，attempt-02 在命令前遭模型 capacity，均不作为结果；相同记录和命令在本地直接重放及 attempt-03 的同一 B993/模型/隔离 CLI 命令工具中均返回 `STAGED content_unit`、退出码 0，后者具有完整 `turn.completed`。
- 因而 R14 归类为瞬时命令执行层失败，而不是 payload、builder、提示或 auditor 缺陷。建立并冻结 `REMEDIATION-15` 与六个全新 R15 Run ID，不含功能性增量；输入计数仍为 1/8/8/1/6/6、每槽 Skill 27 个文件、输出为空，R14/R15 输入、Skill、controller 与运行控制内容一致，PowerShell/YAML 和固定 B993 可用性检查通过。

### P2 第十五次 Gate 执行进度（2026-08-31）

- `ONC001-R15-C01` detached 完整结束，monitor 记录 `controller_exit_code: 0` 与 `monitor_failure: none`；三件套齐全且 Ledger staging 已由正式 YAML 替换。
- Markdown audit 为 pass：27 次 writer、无失败/越界/超长命令；Ledger audit 为 pass：63 次 add、唯一一次 finalize，record counts 为 18 section status、18 content unit、15 open question、10 consistency finding、1 document、1 search summary。
- 包内 validator 为 pass；冻结 `VAL-P2-v1` 为 9/9 pass、0 failed checks、0 warnings，且 `valid_for_blinded_statistical_review: true`。该槽已锁定，R15 当前 1/6。
- 该运行成功越过 R14 的第 22 次 add 历史失败点且未修改任何冻结控制，进一步支持 R14 的 host-execution 分类；不据此改变 Skill 或统计规则。
- `ONC001-R15-P01` 随后在任何输出、writer 或 builder 命令开始前收到 `Selected model is at capacity` 并 `turn.failed`；monitor 记录退出码 1、无 monitor failure，输出目录为空。按每个矩阵槽最多一次输出前替代规则，该运行标记 invalid 且保留，不能计入 6/6。
- 建立全新替代 Run ID `ONC001-R15-P03`，明确 `replaces_run_id: ONC001-R15-P01`。其 8 个输入、27 个 Skill 文件和 10 个运行控制与 P01 内容一致，输出为空，PowerShell/YAML 与固定 B993 检查通过；未改 frozen Skill、提示、checker 或统计规则。
- 启动替代前，Gate 外 `CLI-CAPACITY-SMOKE-02` 以同一 B993、`gpt-5.6-sol/high`、ephemeral/禁网配置返回 `CAPACITY_READY`、完整 `turn.completed` 和退出码 0；随后 detached 启动 P03。该 smoke 只验证宿主恢复，不计入正式 Gate。
- P03 完成 10 次 run-local 辅助读取命令后，在零输出状态再次收到模型 capacity 并 `turn.failed`；monitor 记录退出码 1、无 monitor failure。此前 `item_27` 尝试不存在的 `pdftotext` 并退出 1，但它既不是 writer/builder，也未触发冻结停止规则；终止态由后续模型 capacity 明确给出。
- P01→P03 已消耗该目标槽唯一的输出前替代额度，因此 R15 在 1/6 locked 处停止；P02 与 ONC004 三槽标记 `not-run-phase-stopped`，C01 锁与两次失败现场均保持原样，不能带入下一 remediation。

### P2 第十六次 Gate 预注册（2026-08-31）

- Gate 外 `CLI-CAPACITY-SMOKE-03` 在 P03 终止后以相同 B993、`gpt-5.6-sol/high`、ephemeral/禁网配置再次返回 `CAPACITY_READY`、完整 `turn.completed` 和退出码 0，支持瞬时模型容量分类。
- 环境复核确认 `pdftotext` 不可用、Python `pypdf` 可用；R15 C01 已在同一冻结控制中以 `pypdf` 完整通过，而 P03 的明确终止事件为后续 capacity。故不为一次可恢复辅助命令失败修改 Skill、controller 或 PDF 规则。
- 建立并冻结 `REMEDIATION-16` 与六个全新 R16 Run ID，不含功能性增量。输入计数为 1/8/8/1/6/6，每槽 Skill 27、control 10、output 0；R15/R16 输入、Skill 和 8 个 operational controls 内容一致，root/run controls 同步，PowerShell/YAML 与固定 B993 检查通过。
- R15 的 C01 锁、P01/P03 失败和 smoke 证据继续只读；R16 从 0/6 独立执行，不沿用 R15 的 1 个通过槽。

### P2 第十六次 Gate 执行进度（2026-08-31）

- `ONC001-R16-C01` 在一次 run-local 文件枚举后、任何输出前收到模型 capacity 并 `turn.failed`；monitor 记录退出码 1、无 monitor failure，输出目录为空。该运行标记 invalid，不计入 6/6。
- 按每槽一次输出前替代规则，建立 `ONC001-R16-C02`；其 1 个输入、27 个 Skill 文件和 10 个控制文件与 C01 内容一致，输出为空，PowerShell/YAML 检查通过，无功能增量。
- 因先前单句 recovery smoke 无法预测多轮会话，Gate 外 `CLI-CAPACITY-SOAK-01` 连续执行 10 个独立 shell tool boundary；10/10 退出码 0，经历一次 stream disconnect 后同一会话恢复，最终返回 `CAPACITY_SOAK_READY`、`turn.completed` 和退出码 0。
- 在 soak 通过后 detached 启动 C02；该槽替代额度已耗尽，C02 若终止则 R16 停止。
- C02 完成三件套并由 monitor 记录 `controller_exit_code: 0`、`monitor_failure: none`。Markdown audit 为 30 writer pass；Ledger audit 为 64 add + 1 finalize pass，含 18 section status、26 content unit、8 open question、10 consistency finding、1 document、1 search summary。
- 包内 validator 为 pass；冻结 `VAL-P2-v1` 为 9/9 pass、0 failed checks、0 warnings，`valid_for_blinded_statistical_review: true`。C02 作为 control 目标槽的有效替代已锁定，R16 达到 1/6。

### P2 验证治理收敛（2026-08-31）

- 根据用户指定的验证复盘，前述 R4-R16 已足够暴露并修复执行链路问题；继续要求任一 host-execution 失败使整轮从零开始，会把 Skill 质量与 CLI、PowerShell、writer、auditor、宿主和 capacity 的联合可靠性混为一谈。
- 冻结独立外层治理 `SAP-VALIDATION-GOVERNANCE-V2`，不修改正在运行的 R16 controller、prompt、Skill、validator、checker 或输出。L0 技术健康只认一次冻结证据；L1 对每个有效产物执行合同检查；L2 聚焦统计决策、unsupported assumption、query handling、traceability 与 repeatability。
- L1 仍保留原六个目标槽并要求 6/6 locked，以满足输出契约修复里程碑；L2 只选取 `ONC001`/`ONC004` 各自 protocol-only 与一个 precedent 四个主样本，加 `ONC001` precedent repeat 一个重复样本。既有 `ONC001-R16-C02` 继续锁定，当前 P01 不被中断。
- 基础设施异常只标记 invalid-run、排除出 Skill 质量分母并局部替换；产品内容、证据、统计逻辑或冻结合同失败才计为 Skill 验证失败。该变更只调整验证归因与汇总，不允许现场修补失败输出或读取隐藏参考 SAP。
- `ONC001-R16-P01` detached 完整结束，controller exit 0、monitor failure none。Markdown audit 28 writer pass；Ledger audit 60 add + 1 finalize pass，含 18 section status、18 content unit、9 open question、3 reference、10 consistency finding、1 document、1 search summary。
- P01 包内 validator PASS；冻结 `VAL-P2-v1` 为 9/9 pass、0 failed checks、0 warnings，已创建只读锁并使 R16 达到 2/6。随后在空输出、8 input、27 Skill、10 control 验证后 detached 启动 `ONC001-R16-P02`，monitor PID 9336。
- `ONC001-R16-P02` detached 完整结束，controller exit 0、monitor failure none。Markdown audit 30 writer pass；Ledger audit 76 add + 1 finalize pass，含 18 section status、25 content unit、18 open question、3 reference、10 consistency finding、1 document、1 search summary。
- P02 包内 validator PASS；冻结 `VAL-P2-v1` 为 9/9 pass、0 failed checks、0 warnings，已创建只读锁并使 R16 达到 3/6。下一槽为 `ONC004-R16-C01`。
- 验证 `ONC004-R16-C01` 为 0 output、1 input、27 Skill、10 control 且无既有 launch/exit 证据后 detached 启动，monitor PID 16344。
- `ONC004-R16-C01` detached 完整结束，controller exit 0、monitor failure none。Markdown audit 29 writer pass；Ledger audit 67 add + 1 finalize pass，包 validator 与冻结 checker 均通过，9/9、0 warning，已锁定为 4/6。
- 验证 `ONC004-R16-P01` 为 0 output、6 input、27 Skill、10 control 且无既有 launch/exit 证据后 detached 启动，monitor PID 2992。
- `ONC004-R16-P01` detached 完整结束，controller exit 0、monitor failure none。Markdown audit 22 writer pass；Ledger audit 71 add + 1 finalize pass，含 2 条 reference；包 validator 与冻结 checker 均通过，9/9、0 warning，已锁定为 5/6。
- 验证 `ONC004-R16-P02` 为 0 output、6 input、27 Skill、10 control 且无既有 launch/exit 证据后 detached 启动，monitor PID 12020。
- `ONC004-R16-P02` detached 完整结束，controller exit 0、monitor failure none。Markdown audit 28 writer pass；Ledger audit 92 add + 1 finalize pass，含 2 条 reference；包 validator 与冻结 checker 均通过，9/9、0 warning。创建锁后 R16 L1 达到 6/6。

### 边界（本 Phase 明确不做）

- 不读取或比较隐藏参考 SAP，不执行 AI 统计预审或统计师评分。
- 不把 6 次重验用于宣称统计稳定性，也不掩盖它是在 P3 客观失败后进行的修复验证。
- 不运行或消耗 `CASE-ONC-002/003`；它们继续作为未见回归案例。
- 不因单次失败现场修改规则或手工修补输出后继续计入同一 Gate。

### 涉及文件

| 文件 | 操作 | 预计行数 |
|------|------|----------|
| `.validation-work/generate-sap/oncology-phase1-2/remediation-01/` | 新增隔离运行包、输出、报告和匿名包 | local ignored |
| `.validation-work/generate-sap/oncology-phase1-2/write-channel-smoke/` | 新增受控写入 helper、候选控制器和非临床 smoke 证据 | local ignored |
| `docs/dep/plans/ongoing/P2-generate-sap-blind-validation.md` | 更新 post-remediation 状态和 P3 Gate | +15-30 |
| `docs/main/PROJECT_SPEC.md` | 同步接口契约 | +8-15 |
| `docs/main/TEST_GUIDE.md` | 同步验证方法与边界 | +15-25 |
| `docs/main/memory/project-generate-sap.md` | 记录输出契约与验证边界 | +8-15 |
| `docs/dep/PLAN.md` | 更新两个计划生命周期 | +/−3 |

### 关键决策

- 重验目录：复用旧输出目录 / 新建 `remediation-01`，选择新建；旧证据不可覆写，且新 Skill 版本必须与原 P3 结果清晰分开。
- 失败处理：运行中即时修补 / 单次内容失败即停止，选择单次内容失败即停止；避免新的适应性调优污染 Gate。
- 保留案例：立即使用 `CASE-ONC-002/003` / 继续保留，选择继续保留；本轮只验证已知客观契约修复，未见案例留给后续专业回归。

---

## 执行中发现

> 执行本子计划过程中暴露的问题。每个 Phase Gate 时审查并分类。

| ID | 描述 | 发现于 | 类型 | 处理 |
|----|------|--------|------|------|
| P0-F01 | 合成结构用例可直接由测试 helper 构造，无需新增重复 YAML fixture；既有盲测产物只在本地存在时执行回归 | P1 | 简化 | 已采纳，避免扩大 skill 运行时资源 |
| P0-F02 | Windows 隔离 CLI 的直接文件写入和长 `apply_patch` 命令均不可靠；短 `Set-Content` 可写入，但长 `Add-Content` 片段仍会失败 | P2 | execution-channel | 原样保留失败输出并停止 Phase；受控 STDIN 分块 helper 已通过本地与真实 CLI smoke，待新 remediation 冻结后使用 |
| P0-F03 | 生成会话在校验失败后尝试修复输出，与冻结 Gate 的“内容失败即停止”规则冲突 | P2 | validation-control | 失败产物保持第 1–6 节原状；候选控制器已把校验移到生成会话退出后，待新 remediation 重验 |
| P0-F04 | 纯技术 CLI smoke 会把“读取 helper”误判为编码任务并触发全局 `personal-assistant`，造成外部路径读取 | P2 | isolation-control | 首次 smoke 标记 invalid 并保留；第二次改为纯执行协议、禁止全局 Skill 并禁用 Skill 搜索后通过，临床提示继续只授权 run-local `generate-sap` |
| P0-F05 | `--strip-pipeline-newline` 同时删除了 YAML 分块所需的记录分隔换行，使相邻块拼接为无效 YAML | P2 | execution-channel | `remediation-02` 原样停止；v2 helper 已接管缺失边界换行并通过 YAML 跨块 smoke，待新 remediation 冻结后使用 |
| P0-F06 | 每块 payload 小于 3,000 字符，但模型把多个 helper 调用聚合进最长 29,444 字符的单条 shell 命令 | P2 | execution-channel | v2 提示固定单命令单块，外层审计设 6,000 字符上限；真实 CLI smoke 最大 1,114 字符，待新 remediation 冻结后使用 |
| P0-F07 | 首次 v2 agent smoke 未给出精确 helper 参数和 UTF-8 模板，导致模型猜测 CLI 并产生多次失败 writer | P2 | execution-control | attempt-01 保留为 invalid；控制提示补齐固定参数、`python -X utf8` 与 PowerShell/Python UTF-8 设置后，独立 attempt-02 通过 |
| P0-F08 | v2 写入审计在真实临床首槽通过，但模型手写长 Ledger 时把一个 flow sequence 的 `]` 写成 `}`，导致 38 KB YAML 整体不可解析 | P2 | content-serialization | `remediation-03` 原样停止；下一步只评估最小的结构化序列化约束，不修补失败输出或放宽 Gate |
| P0-F09 | 真实 CLI smoke 首条 `open_question` 使用 `question_id` 而合同要求 `query_id`；builder 在暂存前拒绝，重试后最终 60 条记录完整 | P2 | schema-guidance | 保留拒绝事件并将结果标为 `pass_with_recovery`；未来控制提示明确字段名，builder 继续拒绝而不猜测或改写语义 |
| P0-F10 | R4 提示/注册的模型块上限为 3,000，但 helper 允许 3,500 且 auditor 只检查 6,000 字符命令长度；3,238 字符块因此被接受 | P2 | execution-control | R4 原样停止；候选 helper 将唯一硬上限收敛到 3,000，精确边界测试 2/2 通过，待新 remediation 冻结后使用 |
| P0-F11 | R5 Markdown auditor 以整条命令是否包含 Ledger 文件名代替实际 `--target` 判断，Draft 正文提及独立 Ledger 名称时产生误报 | P2 | audit-control | R5 原样停止；Gate 外候选改为解析 writer 调用后的 `--target`，合成相反用例 2/2 与 R5 只读回放通过，待新 remediation 冻结后使用 |
| P0-F12 | R6 模型把两个顶层章节组合为 3,605 字符块；helper 正确拒绝，但提示未要求 Markdown 拒绝即停止，生成者准备拆块重试 | P2 | execution-control | R6 原样停止；候选限制每块最多一个顶层章节，并统一 Markdown/Ledger 拒绝停止语义，静态失败/通过测试为 0/2 → 2/2 |
| P0-F13 | R7 Ledger auditor 以 builder 文件名子串识别调用，把只读 `Get-Content` 源码查看误判为非法 builder 命令 | P2 | audit-control | R7 原样停止；候选仅识别 Python 实际执行 builder 的命令，合成检测 3/5 → 5/5，R7 三槽只读回放均通过 |
| P0-F14 | R8 P01 输出中途 response stream 断开，恢复时冻结 CLI 构建已被宿主更新移除 | P2 | host-execution | P01 部分 Draft/events 原样保留并停止 R8；当前 bundled CLI 以同配置 smoke 通过，R9 只重钉版本/路径并使用全新 Run ID |
| P0-F15 | R9 模型在第 8 条 writer 命令把重复的 `$OutputEncoding` 样板多写一个 `]`，helper 启动前即 ParserError | P2 | execution-control | R9 原样停止；Gate 外证明 PowerShell 7 + `python -X utf8` 无需两行赋值且 Markdown/Ledger UTF-8 逐字通过，R10 仅简化固定模板 |
| P0-F16 | R10 已连续完成 16 条 writer，但交互 turn 中断同时终止前台控制器，事件无终止态 | P2 | host-execution | R10 部分 Draft/events 原样保留；Gate 外验证隐藏 detached monitor 可在启动调用结束后独立完成并记录 exit code，R11 只增加启动层 |
| P0-F17 | R11 后台层正常记录退出，但冻结的 D664 Codex 构建在生成前已被桌面更新清理 | P2 | host-execution | R11 无输出且四道 Gate 未开始；Gate 外当前 B993 同配置真实 smoke 通过，R12 仅重钉可执行路径并使用全新 Run ID |
| P0-F18 | R12 ONC004 control 运行实际执行 builder `--help`，违反只允许 add/finalize 的冻结命令集合 | P2 | execution-control | R12 在 Ledger audit 失败处原样停止；Gate 外 21 add + 1 finalize 真实 agent smoke 通过，R13 只增加禁止 help/裸调用/探查执行的一条提示约束 |
| P0-F19 | R13 首槽在 7 次成功 writer 后收到 `gpt-5.6-sol` capacity 并 `turn.failed` | P2 | host-execution | 部分 Draft 原样保留，四道 Gate 未开始且 R13 停止；同模型同配置 Gate 外 roundtrip 随后恢复，R14 无功能改动，仅使用全新 Run ID |
| P0-F20 | R14 在 21 次成功 Ledger add 后，第 22 次 `item_87` 命令被执行层以 failed/null exit/no output 拒绝 | P2 | host-execution | R14 原样停止；完全相同记录与命令在本地和同一 CLI 命令工具中均通过，R15 不做功能改动，仅使用六个全新 Run ID |

## 关键决策记录

| 日期 | 决策 | 选项 | 选择 | 理由 |
|------|------|------|------|------|
| 2026-08-27 | 修复计划边界 | 直接修改原 P2 / 独立 P0 | 独立 P0 | 保留原冻结验证证据和失败结论，避免在同一计划中事后调参 |
| 2026-08-27 | 修复深度 | 仅提示词补丁 / 机器可检查合同 / 外部 Validation Engine | 机器可检查合同 | 最小化改动，同时解决 P3 中模型自检无法可靠执行精确 schema 的问题 |
| 2026-08-27 | 隐藏参考 SAP | 先解盲归因 / 保持封存 | 保持封存 | 当前失败均为客观结构问题，不需要专业答案即可修复；继续保留后续盲评价值 |
| 2026-08-27 | P2 首个内容失败后的处理 | 现场补写后继续 / 新建更多替代运行 / 原样保留并停止 | 原样保留并停止 | 冻结合同明确规定内容失败阻断 Phase；现场修稿或再次替代都会污染客观 Gate |
| 2026-08-27 | 长文档落盘机制 | 单条 PowerShell 正文 / 模型自由选写法 / 受控 STDIN 小块 | 受控 STDIN 小块 | 把正文限制在短块并由固定 helper 校验目标、大小和模式，避免 Windows 命令长度成为 SAP 内容 Gate 的混杂因素 |
| 2026-08-27 | 校验执行时点 | 生成会话内自检 / 生成会话退出后外层校验 | 生成会话退出后外层校验 | 首次非零校验时生成者已结束，确保失败产物不能在同一会话中被修补 |
| 2026-08-28 | `remediation-02` 内容失败处理 | 修补换行后继续 / 原样停止 | 原样停止 | 三件套已经产生，YAML 解析失败属于客观内容合同失败；继续会违反预注册停止规则 |
| 2026-08-28 | v2 分块边界所有权 | 由模型携带换行 / helper 自动补缺失分隔 | helper 自动补缺失分隔 | 内容块内部保持原样，同时消除 PowerShell 管道和 here-string 对跨块 YAML 语义的影响 |
| 2026-08-28 | 单命令大小控制 | 仅提示 / 会话后机器审计 | 提示 + 会话后机器审计 | 提示约束降低聚合概率，独立审计保证超长或多 writer 命令不能进入有效结果 |
| 2026-08-28 | `remediation-03` 单字符 YAML 失败处理 | 修补后继续 / 原样停止 | 原样停止 | 三件套已存在且包内 validator 返回非零；预注册合同禁止内容失败后修稿或继续矩阵 |
| 2026-08-28 | Ledger 序列化所有权 | 模型手写完整 YAML / 逐记录 JSON + 确定性组装 | 逐记录 JSON + 确定性组装 | 只机械保证语法、顺序和 ID 唯一性，避免把长 YAML 配对正确性交给模型，同时保留语义审核边界 |
| 2026-08-28 | Markdown 块大小合同 | 提示 3,000 + helper 3,500 / 单一 helper 硬上限 3,000 | 单一 helper 硬上限 3,000 | R4 证明提示上限不能作为可执行 Gate；在写入边界直接拒绝才能保证合同不漂移 |
| 2026-08-28 | Markdown writer 的 Ledger 目标检测 | 整命令文本包含文件名 / 解析 writer 的 `--target` 实参 | 解析 `--target` 实参 | payload 是自由正文，文件名出现不能证明写入目标；目标参数才是通道边界 |
| 2026-08-28 | Markdown 分块控制 | 仅建议较短块 / 每块最多一个顶层章节并统一拒绝停止 | 每块最多一个顶层章节并统一拒绝停止 | 不引入第二个数值 Gate，同时减少多章节合并超限，并让生成行为与冻结停止政策一致 |
| 2026-08-31 | 输出后宿主中断 | 续写原输出 / 重启同 Run ID / 原样停止并新 remediation | 原样停止并新 remediation | 已产生部分 Draft，任何续写或同 ID 重启都会破坏不可覆写和独立运行边界；新轮只接受明确登记的宿主 CLI 变化 |
| 2026-08-31 | 重复编码样板 | 修正失败命令后续写 / 保留赋值并强调拼写 / 删除冗余赋值 | 删除冗余赋值 | PowerShell 7 默认管道编码配合 `python -X utf8` 已通过两通道多语言逐字测试；减少每条命令的可错语法面比继续提示手抄更可靠 |
| 2026-08-31 | 长运行生命周期 | 继续前台等待 / 续写中断输出 / detached monitor + 新 Run ID | detached monitor + 新 Run ID | 两次输出后中断证明前台进程与交互 turn 耦合；后台 monitor 只改变宿主启动方式，并保留不可覆写与正式 Gate 顺序 |

## 同步记录

| 日期 | 已同步到 | 说明 |
|------|----------|------|
| 2026-08-28 | `PROJECT_SPEC.md` | 同步固定标题、当前研究/外部 Reference 分离及逐记录确定性 Ledger 序列化边界 |
| 2026-08-28 | `TEST_GUIDE.md` | 同步 11 个单元测试、builder 失败边界和真实 CLI `pass_with_recovery` 口径 |
