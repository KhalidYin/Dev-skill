# 项目架构指南

## 概述

Dev-skill 是一个 Codex Skill 工厂，用于创建、维护、校验、安装和打包可复用的技能目录。

## 技术栈

| 层 | 技术 | 版本 | 用途 |
|----|------|------|------|
| 工具链 | Python | 未固定 | 脚手架、校验、索引、打包 |
| 安装 | PowerShell / shell | 未固定 | 将 skill 链接或复制到 agent 的 skills 目录 |
| 内容 | Markdown / JSON / YAML | 未固定 | Skill 指令、评测与元数据 |

## 模块结构

### Skill 目录

- **职责**：每个包含 `SKILL.md` 的顶层目录定义一个可安装 skill。
- **入口**：`<skill-name>/SKILL.md`
- **可选资源**：`references/`、`scripts/`、`assets/`、`evals/`

### 项目工具链

- **职责**：创建、安装、校验、索引和打包 skill。
- **入口**：`scripts/new_skill.py`、`scripts/install.ps1`、`scripts/validate_all.py`、`scripts/generate_index.py`、`scripts/package_all.py`

### 注册表与索引

- **职责**：记录 skill 状态和分类，并生成可读清单。
- **入口**：`.skill-registry.json`、`SKILL_INDEX.md`

### Generate SAP

- **职责**：把研究资料和确认的统计决定转换为结构完整的 SAP review draft，并保留生成依据、Author Query 和明确 Reference。
- **入口**：`generate-sap/SKILL.md`
- **资源**：输入/内容项契约、完整章节映射、核心章节规则、同类研究检索规则和通用模板按需加载。
- **当前切片**：完整通用 SAP 结构；深度覆盖研究设计、Endpoints、Estimands/ICE、Analysis Populations、Primary Efficacy、Missing Data/Sensitivity；对 adaptive/Bayesian 方法要求完整转录当前研究的 prior、阈值和决策规则；安全性仍是基础 authoring 约束，但未确认计数约定必须显式 proposed。
- **边界**：仅属于 Skill Layer；不实现 Workflow、知识图谱、向量库、独立 Validation Engine、GUI、TFL/ADaM 或统计编程。

### Review Protocol

- **职责**为统计师审核现有方案，覆盖研究设计、终点、数据采集、样本量、分析与决策。
- **数据流**从现行方案识别独立统计部分，再以 `assets/checklist.yaml` 路由。判型后查同类方案与适用指南，依次审核章节覆盖、逐项预设和跨章节一致性。独立构建器校验 JSON，输出总览、作者批注、覆盖和分析矩阵四页，可加证据对照页。
- **部署**随项目脚手架安装，运行需要 Python 3.9+、PyYAML 和 openpyxl。

### TFLs-Shell

- **入口**：`tfls-shell/SKILL.md`，来源为 `KhalidYin/TFL-shell` 的 `Skill/tfls-shell/`，固定提交记录在注册表。
- **资源**：保留上游 `docs/`、`package_assets/`、`examples/`、`runtime/` 和 `scripts/` 相对路径；`references/integration.md` 说明迁移、依赖和调用方式。
- **依赖**：Product `tflshell` 在 Skill 外独立安装。脚本兼容源码仓库和已安装 Product，不将生成器代码复制进 Skill。
- **范围**：CSR 14.1、14.2、14.3、14.4 和 16.2。材料归一后推荐 shell，生成 DOCX/XLSX/SOP 并返回契约检查；输出是模板与占位结构。
- **安装**：使用本项目安装脚本；上游历史入口 `tfl-governed-shell-workflow` 不重复注册。
- **交付 v2**：两类入口统一调用 `scripts/delivery.py`，由 agent 将材料和偏好整理为配置。依次执行资料关卡、Product 生成、标题去重与交付适配、配置驱动检查、排他发布；独立检查器通过交付契约复核子集与定制格式。

## 数据流

`scripts/new_skill.py` 创建 skill 并登记注册表，开发者补充指令和资源后运行校验与安装，`scripts/generate_index.py` 根据注册表和 frontmatter 更新索引。

`generate-sap` 由用户或上层 Workflow 显式触发，`agents/openai.yaml` 禁止隐式调用。Skill 先规范化输入并实例化完整 SAP 结构，再按章节读取生成规则；每个内容项记录来源、规则、假设、生成模式和问题。若宿主允许网络访问，Skill 在实质统计章节生成前搜索同类公开 SAP 并形成 Precedent Summary；不可访问时显式降级。

## 目录结构

```text
Dev-skill/
├── <skill-name>/
├── scripts/
├── templates/
├── dist/
├── .skill-registry.json
└── SKILL_INDEX.md
```

## 关键约定

- 新 skill 必须使用项目脚手架创建。
- `SKILL.md` 采用三级渐进式披露，主体不超过 500 行。
- 变更完成后必须安装、全量校验、更新注册表和索引。
