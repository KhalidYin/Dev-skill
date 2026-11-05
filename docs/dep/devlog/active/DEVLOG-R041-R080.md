# Dev Log — R041-R080

---

## 2026-08-31

### R041 [20:51] [P0-generate-sap-output-contract] P2: ONC004 P01 通过并启动最后槽 P02

#### Done

- `ONC004-R16-P01` detached 完整结束；controller exit 0、monitor failure none，三件输出齐全且 staging 已清除。
- Markdown audit 以 22 writer pass；Ledger audit 以 71 add + 1 finalize pass，记录构成为 18 section status、18 content unit、21 open question、2 reference、10 consistency finding、1 document、1 search summary。
- 包内 validator 返回 PASS；冻结 `VAL-P2-v1` 为 9/9 pass、0 failed checks、0 warnings，`valid_for_blinded_statistical_review: true`。创建 P01 锁并将 R16 更新为 5/6 locked。
- 对 `ONC004-R16-P02` 执行冻结 preflight：0 output、无既有 launch/exit/events，6 input、27 Skill、10 control；随后 detached 启动，monitor PID 12020 已确认存活并响应。

#### Issues / Blockers

- 当前无 blocker；P02 尚未产生终态，不能提前执行 Gate 或锁定。

#### Next

1. 判定 `ONC004-R16-P02` 终态及四道 L1 Gate。
2. 通过后锁定六槽 6/6，并按治理文件进入 4+1 L2 样本选择与匿名评审包。

#### Files Changed / Commits

- `.validation-work/generate-sap/oncology-phase1-2/remediation-16/`（local ignored P01 evidence/lock and P02 launch evidence, modified）
- `docs/dep/`（modified, uncommitted）

---

### R043 [22:05] [P0-generate-sap-output-contract] P2: 4+1 匿名包与 P2 入口恢复

#### Done

- 按 `SAP-VALIDATION-GOVERNANCE-V2` 固化五个 L2 样本及 `REV-101` 至 `REV-105` 映射；映射文件单独保存并禁止 reviewer 访问。
- 创建五个匿名包，每包包含 protocol、三件生成产物、冻结 objective report 和空白 scorecard；未包含或读取 hidden reference SAP。
- 首次盲化扫描发现派生副本保留 arm 标签；锁定原产物未修改，仅在匿名副本和可复现打包脚本中把两类 arm 标签替换为中性 `blinded-source-set`。
- 最终验证五包各 6 个文件，Run ID、arm 标签和 repeatability 标签扫描 0 命中，scorecard 均为空且可解析；package register 状态为 `ready-for-blinded-statistician`。
- 更新原 `P2-generate-sap-blind-validation`：保留 2026-08-27 首轮失败历史，登记本轮为 post-remediation，P3 Gate 通过并恢复 P4 入口。

#### Issues / Blockers

- 打包脚本首次 dry run 因 `Path.parents` 层级错误未创建包；修复后成功。首个包验证又把合同文件数误写为 7，实际为 6；按合同重验通过。
- 专业统计评分仍必须由合格统计师完成；当前无技术 blocker。

#### Next

1. 合格统计师在盲态下完成并锁定五份 scorecard。
2. 所有评分锁定后，按单独治理授权 reference SAP 比较与解盲归因。

#### Files Changed / Commits

- `.validation-work/generate-sap/oncology-phase1-2/l2-review/`（local ignored anonymous review packages and controls, added）
- `docs/dep/`（modified, uncommitted）

---

### R042 [21:53] [P0-generate-sap-output-contract] P2: R16 L1 六槽 6/6 锁定

#### Done

- `ONC004-R16-P02` detached 完整结束；controller exit 0、monitor failure none，三件输出齐全且 staging 已清除。
- Markdown audit 以 28 writer pass；Ledger audit 以 92 add + 1 finalize pass，记录构成为 18 section status、48 content unit、12 open question、2 reference、10 consistency finding、1 document、1 search summary。
- 包内 validator 返回 PASS；冻结 `VAL-P2-v1` 为 9/9 pass、0 failed checks、0 warnings，`valid_for_blinded_statistical_review: true`。
- 创建 P02 锁并将 R16 根 register 标记为 `l1-locked`；六个目标槽全部锁定，L1 输出合同里程碑达到 6/6。

#### Issues / Blockers

- 当前无 blocker；冻结 checker 只证明结构与可追溯性，不等同于专业统计判断，后续仍需 L2 独立评审。

#### Next

1. 按 `SAP-VALIDATION-GOVERNANCE-V2` 固化 4+1 L2 样本集合。
2. 创建匿名评审包并恢复独立评审入口，不暴露 hidden reference SAP。

#### Files Changed / Commits

- `.validation-work/generate-sap/oncology-phase1-2/remediation-16/`（local ignored P02 evidence/lock and L1 register, modified）
- `docs/dep/`（modified, uncommitted）

---

## 2026-09-01

### R044 [10:21] [P2-generate-sap-blind-validation] P4: 完成版本对齐与五份事实预审

#### Done

- 只读取 `CASE-ONC-001/004` 的 Protocol 和隐藏参考 SAP，完成两案例版本关系：ONC001 参考 SAP 基于同一 Protocol Amendment 8，并识别出后发 Phase I DOR 汇总规格；ONC004 参考 SAP 记录了 expansion 取消、dose escalation 停止和 abbreviated CSR 的后续运营收口。
- 从每个匿名包内 Protocol 独立识别案例，未读取 Review ID 映射；为 `REV-101` 至 `REV-105` 各生成 6 主题事实预审，只含位置、差异摘要、版本归因候选和待统计师判断项。
- 首次盲包复核稳定复现 3 个大小写标签漏点；根因是打包脚本仅作大小写敏感替换。将既定 arm 标签替换改为大小写不敏感，并仅清理匿名派生副本，冻结原输出未修改。
- 各匿名包加入对应 `reference-sap.pdf` 和 `ai-prereview.yaml`；五包均为 8 个文件，Protocol/参考 SAP 对应正确，预审 YAML 可解析且无得分、严重度、差异类别或 disposition，盲化标签 0 命中，scorecard 保持空白。
- P4-A Gate 通过；计划和任务恢复点切换到 P4-B 单统计师盲评。

#### Issues / Blockers

- P4-B 需要 1 名合格统计师完成并签署 5 份 scorecard；AI 不替代专业评分。全部 scorecard 锁定前不得读取映射或执行 P5。
- 版本对齐文件首次尝试以同一路径 delete/add 的单补丁更新，被 `apply_patch` 拒绝；根因是单补丁不允许同一目标的重复操作，改用原位更新后成功，未造成文件损坏。
- 本轮 PDF 临时目录的递归删除被主机安全策略拒绝；未换壳绕过，改为将完整证据目录移动到被忽略的 `.validation-work/.../p4-a-evidence/`，可见工作树不再新增 `tmp/` 文件。

#### Next

1. 合格统计师逐包确认或修正事实预审，完成 6 个评分维度、hard gates、专业差异判断和签署。
2. 五份 scorecard 全部锁定后再读取映射，执行 P5 的 4+1 解盲归因与验证结论。

#### Files Changed / Commits

- `.validation-work/generate-sap/oncology-phase1-2/comparison/`（local ignored version alignment and five factual prereviews, modified/added）— `(uncommitted)`
- `.validation-work/generate-sap/oncology-phase1-2/l2-review/`（local ignored package supplements and case-insensitive blinding fix, modified/added）— `(uncommitted)`
- `docs/dep/PLAN.md`, `docs/dep/TASK_STATE.md`, `docs/dep/plans/ongoing/P2-generate-sap-blind-validation.md`（modified）— `(uncommitted)`
- `docs/dep/devlog/active/DEVLOG-R041-R080.md`, `docs/dep/devlog/INDEX.md`（modified）— `(uncommitted)`

---

## 2026-09-02

### R045 [13:15] Generate SAP 临床评审后最小修复

#### Done

- 将 `sourced` 内容单元携带 `assumptions` 或 `alternatives` 定义为输出合同错误，并以先失败后通过的单元测试固化；要求混合段落拆分为 sourced/proposed，proposed 决策必须在正文显式标识并绑定稳定 query。
- 补齐早期肿瘤 adaptive/Bayesian 生成约束：逐项转录模型参数化、完整先验与混合权重、EWOC/后验阈值、可评估性、升降级/停止、MTD/RP2D 和个体内递增规则，不得以裸 Protocol 引用或无依据 TBD 代替。
- 增加 Protocol 内 arm/sub-arm/cohort、单臂与总样本量一致性检查，并收紧 AE 计数/最差等级等安全性惯例：无当前来源或 Sponsor 确认时只能作为显式 proposed 方案与 query。
- 新增合成早期肿瘤回归 fixture 和第 8 个 eval；12 个单元测试通过，8 个 eval 与 6 个 fixture 均可解析，全部 3 个项目 Skill 和 `generate-sap` 系统 quick validator 通过，安装脚本成功以 Junction 更新本机技能目录。
- 更新项目规范、测试指南、长期记忆、注册信息和 P2 验证说明；`.validation-work`、REV scorecard 和历史生成产物均未修改。

#### Issues / Blockers

- 当前 validator 会拒绝历史 `ONC004-C01` 中一个 `sourced + assumptions` 内容单元。根因是旧合同允许来源事实和设计假设共存；这是新规则捕获到的真实历史缺口，不回写冻结基线。
- P4 评分与聚合报告只代表修复前版本，不能作为当前工作树的前向验证证据。当前无实现 blocker。

#### Next

1. 用未见案例或新增合成案例独立运行当前 Skill，确认 evidence mode、adaptive/Bayesian 参数和内部冲突三类约束在生成产物中实际生效。
2. 若继续 P4-B，只用于完成修复前基线的归因；不要混入当前版本结论。

#### Files Changed / Commits

- `generate-sap/references/`, `generate-sap/scripts/validate_output_contract.py`, `generate-sap/evals/`（modified/added）— `(uncommitted)`
- `tests/test_generate_sap_output_contract.py`（modified）— `(uncommitted)`
- `.skill-registry.json`, `docs/main/`, `docs/dep/`（modified）— `(uncommitted)`

---

## 2026-11-04

### R046 [09:50] Review SAP 审查问题修复

#### Done

- 分别判定 Protocol 变更披露和一致性，更新检查表至 v1.0.0，并在合成案例加入已披露的主要终点差异。
- 支持空设计标签，校验 Critical 对照证据和覆盖双向关联，修正 Word 批注定位及 Excel 原文序列化。
- 新增 7 项脚本回归，全仓测试 39 通过、1 跳过，四个 Skill 通过仓库校验。已更新注册表和索引，并验证 Codex 与 Claude 的安装链接。
- 独立前向审阅合成 SAP 的 PRO 维度，生成含 12 条覆盖记录的 Excel。已披露的主要终点变更在 PRO-02 记为 Critical，PRO-12 仅关联其余未披露差异。保留主分析的 tipping-point 补充分析只记录在 crosswalk。

#### Next

- 按计划运行全套 7 个行为评测并评分。

### R047 [11:29] Review Protocol 初版

#### Done

- 按研究目的、比较结构、实施结构、推断与决策先判型，再应用 38 项核心、条件和专项检查。
- 加入来源分类、公开方案案例和可独立运行的 Excel 构建器。构建前验证研究部分、检查覆盖、证据定位和问题双向链接。
- 三类合成方案通过 CLI 路由、构建和回读，仓库测试 44 通过、1 跳过。更新注册表与索引，核验 Codex 安装。

#### Next

- 独立执行五个行为评测，之后由临床统计师验证实际检出和误报。

### R048 [13:42] Review Protocol v0.2

- 新增章节完整性检查和逐分析矩阵，将方法匹配单独判定。
- 批注必含作者可执行建议、理由与可定位原文，支持一条问题关联章节检查和分析矩阵。
- Excel 固定四页，状态变更联动总览，可选追溯页合并详细对照和来源。46 个测试通过，1 个既有用例跳过，Skill 通过校验并安装。

## 2026-11-05

### R049 [13:27] Review Protocol 审核主线

- 将适用监管依据和方案明确的 estimand 或决策目标写入现有流程，逐段核对设计、数据、估计与决策。
- 明确实践调整对假设和目标的影响，批注直接给出判断、理由和需修改内容。
- 检查表 v0.2.1，7 项相关测试和全部 Skill 校验通过。

---

### R050 [14:17] 整合 TFLs-Shell 技能

#### Done

- 使用项目脚手架，将 `KhalidYin/TFL-shell` 提交 `8d85a4174a40b0b0847875e6411bdf1c278383fa` 的正式 `Skill/tfls-shell/` 导入顶层。保留完整参考资产、契约、示例、脚本和薄封装，不重复导入已标为历史名称的 `tfl-governed-shell-workflow`。
- 修复迁移后脚本强制查找原仓库、wrapper 假设固定目录深度的问题，兼容已安装 Product；保持 catalog、生成逻辑和输出契约不变。当前用户 Python 环境安装 Product 2.1.0，源码在 `~/.codex/dependencies/tflshell-8d85a417`，使用 editable 安装保留普通 wheel 遗漏的领域 JSON 资源。
- 注册为 `draft / clinical-statistics`，记录来源提交与版本，更新技能索引、项目指南、规格和测试说明。补充四个待执行行为用例。
- 四项迁移回归通过：缺失依赖报错、异地推荐与三件套生成、完整 catalog 验证及篡改 ID 拒绝、catalog 导出一致性。全仓运行 51 项测试，50 通过、1 个既有本地盲测回归跳过。6 个技能全量校验、官方 quick validator、上游包结构和基线校验通过。
- 通过本项目安装脚本建立 Codex 与 Claude 的 Junction，均指向本项目。Agents 和 Workbuddy 目标根不存在，安装脚本按约定跳过；Codex 已识别新技能。

#### Issues

- 本次验证覆盖结构与迁移运行；四个行为评测、临床适用性复核和带模拟图的视觉检查尚未执行，技能保持 draft。
- 既有 SAP 盲评与旧技能残留清理检查点保持原样，本次未处理这些任务。

#### Next

- Done — 本次整合、登记、安装和校验已完成。

#### Files Changed / Commits

- `tfls-shell/`、`tests/test_tfls_shell.py`（added）— `(uncommitted)`
- `.skill-registry.json`、`SKILL_INDEX.md`、`docs/main/PROJECT_GUIDE.md`、`docs/main/PROJECT_SPEC.md`、`docs/main/TEST_GUIDE.md`、`docs/dep/devlog/INDEX.md`、`docs/dep/devlog/active/DEVLOG-R041-R080.md`（modified）— `(uncommitted)`

---

### R051 [15:27] TFLs-Shell 交付 v2 与标题去重

#### Done

- 按用户接受的审查方案，统一两类生成入口到交付适配层。研究特定模式缺少分期、领域、终点、分析集、治疗组、时间点或有不可读资料/冲突时返回缺口；只推荐不写文件，通用模板显式选择。补充 PFS/OS 等缩写和常见中文信号，最终 shell 选择及逐项说明由 agent 解释后配置。
- Skill 明确复用材料和已有答案，只集中问询影响交付的未决项；交付配置支持语言、字体、页面、组别列及顺序、标签、研究信息和独立交付版本。单臂/多臂调整保留独立分析列，表头组数与研究组数冲突会阻断。
- 定位重复标题来自 Product 的 Heading 4 与信息块重复编号/名称。交付层移除信息块冗余对，保留单一 Heading 4、书签、目录和页码字段；同步 Protocol 页眉与研究名称。生成器 2.1.0、交付契约 v2、用户交付版本分别记录。
- 中文/双语使用 agent 复核的完整映射，缺少译文仅返回待本地化字符串，不发布半成品；占位值和 ID 保留。Word 字段周围逐 run 适配，避免移动动态页码/目录节点。
- 先临时生成和按本次配置检查，再排他发布业务文件及交付契约，拒绝覆盖既有文件。独立检查器通过交付契约复查研究子集、定制标题/表头、分析集、版本、纸张/方向/字体和 Protocol；篡改 ID 可检出。
- 全仓测试 56 项，55 通过、1 个既有盲测跳过；补充字段和方向检查后九项相关回归再次全部通过。六个技能及官方 quick validator 通过，索引和注册更新到 delivery-v2，Codex/Claude 安装链接重新建立。

#### Issues

- 任意 Sponsor 模板仍需 agent 检查并形成支持字段的映射，脚本明确返回未适配缺口；非英文图内文字须单独适配或关闭图形生成。
- 测试的译文为合成映射，仅证明机械应用；自然译文质量、实际 Office 视觉排版和统计师临床复核未由本次机械回归证明。原始 catalog/Product 基线未修改。
- 其他任务检查点保持原样。

#### Next

- Done — 本次审查方案更新与重复标题修复完成。

#### Files Changed / Commits

- `tfls-shell/SKILL.md`、`tfls-shell/scripts/delivery.py`、两类生成入口、`validate_outputs.py`、`tfls-shell/references/`、`PACKAGE_GUIDE.md`、`evals/evals.json`、`tests/test_tfls_shell.py` — `(uncommitted)`
- `.skill-registry.json`、`SKILL_INDEX.md`、`docs/main/PROJECT_GUIDE.md`、`PROJECT_SPEC.md`、`TEST_GUIDE.md`、`docs/dep/devlog/INDEX.md`、本日志 — `(uncommitted)`
