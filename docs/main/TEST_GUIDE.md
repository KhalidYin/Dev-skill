# 测试指南

## 测试框架

当前没有独立单元测试框架。项目以 Python 校验脚本和每个 skill 的 `evals/evals.json` 为主要验证入口。

## 测试结构

- `scripts/validate_all.py`：全量 frontmatter 和命名校验。
- `<skill-name>/evals/evals.json`：Skill 的正向、负向和行为评测用例。
- `<skill-name>/evals/router-evals.json`：意图路由契约；在显式调用策略下供未来 Workflow Router 验证，不作为 Codex 自动触发测试。
- `<skill-name>/evals/files/`：评测所需的本地输入文件。

## 运行方式

```powershell
python scripts/validate_all.py
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
- `generate-sap` 的 7 个行为评测和 5 个合成 fixture，覆盖完整输入、部分输入、来源冲突、检索不可用、先例引用、下游越界和 clean-draft 未决问题。
- `generate-sap` 的独立前向测试：输入不足仍保留完整结构；先例有直接引用但不被当成规范性要求。

### 未覆盖

- 自动化语义触发评测执行器：当前仅保存 eval 用例，需由 agent 前向测试或后续工具执行。
- 安装到不同 agent 环境后的端到端发现行为：需在目标环境验证。

## 测试约定

- 新 skill 至少包含一个应触发用例、一个不应触发用例和一个输入不足用例。
- 高风险专业 skill 必须验证不伪造证据、不越权给出最终批准结论。
- SAP authoring skill 必须验证18个顶层章节存在，且缺失输入不会省略受影响章节。
- SAP authoring skill 必须验证 `sourced`、`derived`、`proposed`、`tbd`、`conflict` 和 `not-applicable` 的行为边界。
- 同类研究评测必须验证直接文档引用、真实文档类型、相似点/差异和检索失败降级，不得用搜索结果摘要冒充证据。
- Clean Draft 测试必须验证未解决的阻断问题不会被静默删除。
- 路由评测应分别记录 `should_trigger`、`expected_route` 和 `expected_status`，不能把意图匹配与能力覆盖混为一谈。

## 测试数据

评测附件放在对应 skill 的 `evals/files/`，不得提交真实患者数据或未脱敏的受控文档。
