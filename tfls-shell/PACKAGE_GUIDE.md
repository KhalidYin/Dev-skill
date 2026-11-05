# TFLs-Shell SKILL 包说明

本目录已整合到 Dev-skill。运行依赖、固定来源版本和本项目安装命令以
[迁移与运行说明](references/integration.md) 为准；下文仓库级安装与基线脚本指上游仓库工具。

交付 v2 的输入关卡、偏好配置、独立版本、语言适配、标题去重及验证以
[输入和交付契约](references/request-contract.md) 为准。下文对旧入口及固定输出的描述仅保留为上游背景。

## 1. 目的

本文件说明 `TFLs-Shell SKILL` 的包结构与维护方式，避免再次把 Skill 误解为
“只有一个 `SKILL.md` 文件”或“等同于某个仓库实现文件”。

## 2. 包结构原则

一个可复用 Skill 的最小入口是 `SKILL.md`，但为了提高调用可靠性，Skill 包
可以同时包含：

- 包说明文档
- 开发规则文档
- 示例
- 术语映射
- 辅助脚本
- 参考资产

因此，`SKILL.md` 是主入口，但不是全部。

## 3. 当前包内文件

当前包内建议至少包含：

- `SKILL.md`：定义用途、触发条件、工作流、输出边界
- `PACKAGE_GUIDE.md`：说明 Skill 包的结构与定位
- `DEVELOPMENT_RULES.md`：约束后续如何制定、扩展和维护这个 Skill
- `scripts/alignment_contracts.py`：沉淀从上游项目提炼出的稳定输出细节 contract、检查 helper 与声明引用元信息
- `scripts/package_bundle.py`：声明并检查 Skill 包的自包含资产是否齐备
- `scripts/generate_project_aligned_outputs.py`：生成与当前项目一致命名和结构的正式输出
- `scripts/recommend_then_generate.py`：从输入文本直接完成推荐并生成项目一致输出
- `scripts/export_catalog_subset.py`：从 Product 受控导出 Skill 包使用的 catalog 子集
- `scripts/export_product_contracts.py`：从 Product 当前实现导出 Skill 包使用的输出契约资产
- `scripts/validate_outputs.py`：验证 DOCX / XLSX / SOP 是否符合包内 Product 对齐契约
- `package_assets/contract_registry.json`：受控细节 contract 注册表
- `package_assets/catalog_subset.json`：为跨项目复用准备的最小 catalog 子集
- `package_assets/output_manifest.json`：当前 Product 输出结构的机器可读 manifest
- `package_assets/minimal_runtime_requirements.txt`：最小运行依赖清单
- `examples/recommend_then_generate_non_oncology.json`：可执行样例请求
- `runtime/catalog_loader.py`：读取 Skill 包内 catalog 子集
- `runtime/registry_loader.py`：读取 Skill 包内 contract registry
- `runtime/wrappers/`：统一封装 `docx / xlsx / sop` 输出调用接口
- `docs/product_alignment_contract.md`：Product 对齐总契约
- `docs/catalog_schema_contract.md`：catalog schema 契约
- `docs/docx_shell_contract.md`：DOCX shell 契约
- `docs/xlsx_workbook_contract.md`：XLSX workbook 契约
- `docs/sop_contract.md`：SOP 契约
- `docs/table_layout_contract.md`：table layout 契约

当前仓库已提供基础校验脚本：

- `scripts/validate_skill_package.py`
- `scripts/validate_skill_baseline.py`
- `scripts/install_skill_to_agents.py`

`validate_skill_package.py` 用于校验正式 Skill 包的目录结构、主文件 frontmatter、
必需配套文件与明显错误表述，并检查最小自包含资产是否齐备。

`validate_skill_baseline.py` 用于校验 `output_manifest.json`、`contract_registry.json`
和生成/验证脚本清单是否仍与 Product 当前实现一致。

安装脚本用于把仓库内 `Skill/tfls-shell/` 安装到 agent skills 目录。默认目标为
项目本地 `.agent/skills/tfls-shell`，也可通过 `--target-root $HOME/.agents`
安装到当前用户全局 agent skills 目录。

后续可按需要加入：

- `examples/`
- `references/`
- `assets/`
- `scripts/`

## 4. 与 Product 的关系

`TFLs-Shell SKILL` 面向大众，是独立的应用层交付物。

它可以吸收部分真实项目经验，但只应吸收“可复用子集”，例如：

- workflow 片段
- 规则摘要
- 模板片段
- 样例
- 字段说明
- 辅助脚本

不应把整个上游项目、完整实现层或完整文档体系直接搬入 Skill 包。

## 5. 输出物区分

请始终区分：

- `SKILL Package Files`：Skill 包自身文件
- `Upstream Source Assets`：可被提炼进入 Skill 的上游经验、脚本、模板或文档细节
- `Governance Docs`：项目规范与设计说明
- `Formal Outputs`：正式业务输出文件

Skill 包不应被某个项目实现替代，也不应被业务输出覆盖。

## 5.1 当前生成脚本

当前正式生成脚本位于：

- `scripts/generate_project_aligned_outputs.py`
- `scripts/recommend_then_generate.py`

它们分别用于：

- 直接生成项目一致输出
- 从输入文本出发先 recommend，再生成项目一致输出

其中：

- `generate_project_aligned_outputs.py` 偏向直接输出执行
- `recommend_then_generate.py` 偏向 schema-first 工作流执行，会返回中间状态、
  推荐状态、生成结果与验证摘要
- `alignment_contracts.py` 偏向把三类正式输出的细节规则做成可复用 helper，
  供脚本显式引用，而不是把这些细节散落在入口脚本里
- `package_bundle.py` 偏向暴露 Skill 包当前是否已具备跨项目复用所需的最小资产
- `runtime/` 偏向提供包内最小运行层，让入口脚本优先走 Skill 自身携带的 loader 与 wrapper
- `export_catalog_subset.py` 偏向建立 Product -> Skill 的受控同步入口
- `export_product_contracts.py` 偏向建立 Product 输出结构 -> Skill contract 的受控同步入口
- `validate_outputs.py` 偏向作为 Skill 包迁移到其他项目后的输出防漂移检查入口

当前支持：

- `docx`
- `xlsx`
- `sop`
- `all`

当前 `validation_results` 除返回检查结果外，还会返回：

- `declared_references`

该字段用于声明本次脚本实际引用了哪些细节 contract、由哪个 helper 模块提供、
以及当前引用的是哪一组稳定字段或结构约束。

当前顶层返回结果还会包含：

- `package_bundle`
- `runtime_summary`

该字段用于声明当前 Skill 包自身是否已经具备最小自包含运行条件。

`runtime_summary` 用于声明本次执行优先走的是哪一层运行路径，以及当前引用的
catalog / registry / wrapper 来源。

`output_manifest.json` 用于声明当前 Product 版本下 DOCX / XLSX / SOP 的可观察输出结构，
包括 workbook sheet、catalog 字段、DOCX heading/layout、SOP 头表和 appendix 结构。

## 6. 维护原则

- package-first
- boundary-first
- reliability-first
- reusable-subset-only

如果某个需求只影响上游项目实现，不一定改 Skill 包。
如果某个需求改变了应用层触发条件、边界或输出契约，必须同步更新 Skill 包。

## 6.1 快速安装

从仓库根目录运行：

```powershell
python scripts\install_skill_to_agents.py --force
```

安装到当前用户全局 `.agents` 目录：

```powershell
python scripts\install_skill_to_agents.py --target-root $HOME\.agents --force
```

预览安装动作：

```powershell
python scripts\install_skill_to_agents.py --dry-run
```

## 7. 边界守卫：SKILL 不是软件包

本 SKILL 的定位是 **AI 调用的规范文档 + 参考资产**，不是需要独立运行的程序包。

### 7.1 SKILL 是什么
- `SKILL.md` — AI 读取的工作流规范
- `docs/` — AI 参考的契约文档和格式规则
- `package_assets/` — AI 做推荐和验证时的元数据参考
- `examples/` — AI 学习的输入输出样例
- `scripts/` — AI 调用的辅助工具（依赖 Product）
- `runtime/` — Product 生成器的薄封装层（不是独立替代品）

### 7.2 SKILL 不是什么
- ❌ 不是独立可运行的软件包
- ❌ 不是 Product 的替代品或竞争对手
- ❌ 不需要自己的命名工具、版本读取器、运行模式检测
- ❌ 不需要 `setup.py`、`pyproject.toml` 或独立依赖管理

### 7.3 脚本依赖 Product 是设计如此
脚本中 `from tflshell import ...` 的模式是**正确的**，不是待解决的耦合问题。
如果要跨项目生成文件，正确做法是 `pip install tflshell`，而不是把 Product 代码复制进 SKILL 包。

### 7.4 自包含 ≠ 代码独立
SKILL 的"自包含"指**参考资产**随包携带（catalog 子集、contract 文档、示例），
不是为了"让脚本在没有 Product 的环境下也能跑"。这两个概念不可混淆。
