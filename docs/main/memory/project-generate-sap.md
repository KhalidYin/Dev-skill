---
name: generate-sap-skill
description: SAP初版采用完整结构、逐内容项生成权限、章节内问题和受控同类研究检索
type: project
---

`generate-sap` 是单一显式调用的 SAP authoring Skill，不是 Decision Engine 或 Agent Workflow。

**核心约束：** 无论输入是否充分，先实例化完整 SAP 结构。每个 material content unit 只能使用 `sourced`、`derived`、`proposed`、`tbd`、`conflict` 或 `not-applicable`；缺失和冲突必须在受影响章节以稳定 Query ID 表达，并继续生成无关章节。

**生成依据：** 输出 SAP Review Draft、Generation Evidence Ledger 和 Open Questions/References。结构化依据记录事实、规则、假设、简要推导、先例和问题，不输出原始思维链，也不声称批准或合规。

**同类研究：** 宿主搜索可用时，先形成 Study Fingerprint，再广泛发现、短名单筛选和深入阅读公开 SAP 或替代资料。Trial precedent 与 normative reference 分开；Reference 记录真实文档类型、直接 URL、版本/日期/状态、章节/页码、检索日期、相似点和差异。搜索不可用或证据不足时显式降级。

**边界：** 不实现知识图谱、向量库、搜索服务、独立 Validation Engine、GUI、TFL/ADaM 或统计程序。
