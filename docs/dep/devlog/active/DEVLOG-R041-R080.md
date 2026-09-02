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
