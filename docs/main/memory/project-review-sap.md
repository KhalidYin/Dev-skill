---
name: review-sap-skill
description: 外部 SAP 审阅 skill：四维度 v1 范围、版本化检查表、逐条 JSON 暂存生成 Excel 问题清单、docx 批注需确认
type: project
---

`review-sap` 是显式调用的外部 SAP 审阅 Skill，不改写 SAP、不出具批准或合规结论，与 `generate-sap`（撰写）分工。

**范围（2026-11-03 用户确认）：** 主要对象为外部 SAP；v1 覆盖 STR 结构完整性、INT 内部一致性、PRO 与 Protocol 一致性、PRG 可编程性。方法学恰当性后续单独模块细化，v1 仅记为 `out-of-scope-observation`（severity n/a）。

**检查表** `assets/review-checklist.yaml` v1.0.0 将变更披露与一致性分别判定。检查表以 Gamble 2017 为 STR 主干，辅以 Homer 2022 早期研究扩展（主题级映射）、ICH E9/E9(R1)、SPIRIT 2025、ICH M11 和 CDISC ADaM 原则。NMPA 2016、ADaM、FDA TCG 仍待核验，待核验来源不可单独支撑 Critical 或 Major。

**输出：** Excel 问题清单为主（Read Me、Summary 公式汇总、Findings 含跟踪列、Checklist Coverage、Protocol-SAP Crosswalk、Documents、Basis）。docx 批注仅在用户明确确认后由 `annotate_docx.py --confirmed` 生成新文件。

**可靠性约束** 逐条校验 JSON 后暂存。`check` 校验适用检查项的唯一覆盖结论、对照证据和问题与覆盖的双向关联。无专用设计标签时用空列表。Excel 将输入证据保留为文本，Word 将无法唯一定位的批注报告为未锚定。
