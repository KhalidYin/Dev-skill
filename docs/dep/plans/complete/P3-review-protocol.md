---
phase_index: 3
status: done
created: 2026-11-04
updated: 2026-11-04
priority: 2
estimated_rounds: 1
depends_on: []
tags: [clinical-statistics, protocol-review]
syncs_to: [PROJECT_SPEC.md, PROJECT_GUIDE.md, TEST_GUIDE.md]
---

# Review Protocol 初版

## 目标

按统计设计识别审查范围，并生成可追溯的临床试验方案审核 Excel。

## 背景

沿用 review-sap 的证据和覆盖合同。2026-11-04 用户确认先判型，再选择通用、条件或专项检查，按类型参考同类方案和指南。

## 涉及范围

包含判型、版本化检查表、来源映射、审核工作簿和三类方案验收。方法选择交统计师复核，方案源文件保持只读。

## 主文档影响

- `PROJECT_SPEC.md` 增加审核能力和输出合同。
- `PROJECT_GUIDE.md` 增加审核数据流。
- `TEST_GUIDE.md` 增加路由和输出验证。

## Phase 总览

| Phase | 目标 | 预估轮次 | 依赖 | 状态 |
|---|---|---|---|---|
| P1 | 实现、验证和安装初版 | R047 | - | done |

## P1 实现与验收

### 输入条件

- 用户确认初版设计，仓库提供脚手架与审核输出先例。

### 产出

- `review-protocol/` 及配套测试、安装和项目索引。

### 完成标准

- [x] 随机对照、单臂探索、剂量递增加扩展三个合成用例均走通分层检查和 Excel 输出。
- [x] 校验证据和覆盖关系，区分不适用、附件缺失和需要专项复核。
- [x] 全量校验、测试、索引和安装完成。

### 边界

- 初版的结构和行为验收使用合成案例，临床专业验证单独记录。

### 涉及文件

| 文件 | 操作 |
|---|---|
| `review-protocol/`、`tests/test_review_protocol.py` | 新增 |
| `.skill-registry.json`、`SKILL_INDEX.md`、`docs/` | 同步 |

### 关键决策

- 按研究部分独立启用检查项，以独立输出脚本保持 Skill 可单独安装。

## 执行中发现

- 三种合成设计以人工构造的结构化记录跑通 CLI。五个行为评测已登记，独立前向评测和临床统计师验证留作后续。

## 决策记录

- 2026-11-04 用户确认设计并授权实施初版。

## 同步记录

- 已更新项目规范、架构指南、测试指南、注册表和索引，并核验 Codex 安装链接及已安装入口。
