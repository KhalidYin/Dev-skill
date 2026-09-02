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
