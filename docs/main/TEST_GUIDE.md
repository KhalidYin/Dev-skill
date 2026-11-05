# 测试指南

## 测试框架

项目使用 Python `unittest`、项目校验脚本和每个 skill 的 `evals/evals.json`。单元测试负责可确定执行的结构与序列化合同；eval 用例保留需要 agent 判断的行为期望。

## 测试结构

- `scripts/validate_all.py`：全量 frontmatter 和命名校验。
- `tests/`：输出合同、Ledger 记录组装和既有失败回归测试。
- `<skill-name>/evals/evals.json`：Skill 的正向、负向和行为评测用例。
- `<skill-name>/evals/router-evals.json`：意图路由契约；在显式调用策略下供未来 Workflow Router 验证，不作为 Codex 自动触发测试。
- `<skill-name>/evals/files/`：评测所需的本地输入文件。

## 运行方式

```powershell
python scripts/validate_all.py
python -X utf8 -m unittest discover -s tests -v
python scripts/generate_index.py
```

新增或修改 skill 后，还应运行：

```powershell
.\scripts\install.ps1 -SkillName <skill-name>
```

## 覆盖范围

### 已覆盖

- Skill frontmatter、name 和 description 基础规则。
- 注册表驱动的 skill 发现和索引生成。
- `generate-sap` 的 8 个行为评测和 6 个合成 fixture，覆盖完整输入、部分输入、来源冲突、检索不可用、先例引用、下游越界、clean-draft 未决问题，以及 early-phase adaptive/Bayesian 参数、决策规则、样本量冲突和安全性 proposed convention。
- `generate-sap` 的独立前向测试：输入不足仍保留完整结构；先例有直接引用但不被当成规范性要求。
- `generate-sap` 的 12 个单元测试：8 个输出合同测试和 4 个 Ledger builder 测试；覆盖确定性组装、UTF-8、重复 ID/单例拒绝、错误 JSON 不污染暂存、必需单例、禁止覆盖最终文件、`sourced` 模式夹带 assumptions/alternatives 的拒绝，以及既有盲测产物的新规则回放。
- Ledger 序列化非临床 smoke：本地大记录集通过；真实 CLI 生成 60 条目标记录，最终 YAML 可解析且暂存已清除。真实 CLI 曾把 `question_id` 写成 `query_id` 合同以外字段，构建器安全拒绝后以相同语义重试，因此结果记为 `pass_with_recovery`，不是零错误通过。

- `review-sap` 的单元测试覆盖空设计标签、Critical 对照证据、检查表版本、缺少 Protocol 时的覆盖、问题与覆盖双向关联、Excel 原文保留和拒绝覆盖、Word 批注定位及确认、检查表与评测答案键完整性。
- `review-sap` 的 7 个行为评测和合成 fixture：含 10 个植入缺陷与 1 个已声明变更诱饵的 SAP、对照用干净 SAP、Protocol 摘录和答案键 `seeded-answer-key.yaml`。
- `tfls-shell` 的 `tests/test_tfls_shell.py` 使用固定提交 Product，验证空材料/文件缺失不生成、PFS 和中文信号不漏疗效、研究缺口关卡、三件套的独立版本/A4/字体/多臂表头/标题去重、防覆盖、交付契约独立复查与篡改 ID 拒绝、单臂列结构、中文翻译完整后发布、双语保留 ID、未适配模板与无效配置的明确拒绝。测试使用临时目录及合成译文，只验证机械映射，不能证明翻译质量或临床适用性。

### 未覆盖

- 自动化语义触发评测执行器：当前仅保存 eval 用例，需由 agent 前向测试或后续工具执行。
- 安装到不同 agent 环境后的端到端发现行为：需在目标环境验证。
- `review-sap` 全套行为评测待执行。检出率和误报率需按答案键评分并由合格统计师复核。
- `tfls-shell` 的六个行为用例已定义；九项机械回归不代替 agent 前向执行、统计师复核、自然译文质量和带模拟图的视觉检查。

## 测试约定

- 新 skill 至少包含一个应触发用例、一个不应触发用例和一个输入不足用例。
- 高风险专业 skill 必须验证不伪造证据、不越权给出最终批准结论。
- SAP authoring skill 必须验证18个顶层章节存在，且缺失输入不会省略受影响章节。
- SAP authoring skill 必须验证 `sourced`、`derived`、`proposed`、`tbd`、`conflict` 和 `not-applicable` 的行为边界。
- `sourced` 内容项夹带 assumption 或 alternative 时 validator 必须失败；安全性计数等未确认约定必须以 proposed + Query 表达。
- Early-phase adaptive/Bayesian 行为评测必须验证附录中的 prior/阈值不被降级为 TBD，MTD/升降级规则被完整保留，以及 arm/cohort/sample-size 冲突不被静默解决。
- 同类研究评测必须验证直接文档引用、真实文档类型、相似点/差异和检索失败降级，不得用搜索结果摘要冒充证据。
- Clean Draft 测试必须验证未解决的阻断问题不会被静默删除。
- Ledger builder 测试必须验证单条 JSON 在进入暂存前完成语法、大小、单例和稳定 ID 检查；builder 只负责机械组装，不能代替输出合同校验器或专业审核。
- 真实 CLI 序列化 smoke 必须保留被拒绝记录和重试审计，分别报告 `pass`、`pass_with_recovery` 或 `fail`，不得把恢复后的结果表述为从未失败。
- 路由评测应分别记录 `should_trigger`、`expected_route` 和 `expected_status`，不能把意图匹配与能力覆盖混为一谈。

- SAP 审阅 skill 用植入缺陷验证检出率，用干净 SAP 检查 Critical/Major 误报。已披露的主要终点变更仍应进入对应 PRO 检查项，保留原计划分析的补充分析则单独检查披露。

## 测试数据

评测附件放在对应 skill 的 `evals/files/`，不得提交真实患者数据或未脱敏的受控文档。
