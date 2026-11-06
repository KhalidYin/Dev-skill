---
phase_index: 5
status: done
created: 2026-11-06
updated: 2026-11-06
priority: 2
estimated_rounds: 1
depends_on: []
tags: [tfl-review, footnotes, excel]
syncs_to: [PROJECT_SPEC.md, PROJECT_GUIDE.md, TEST_GUIDE.md]
---

# TFL Mock Shell 审核初版

## 目标与授权

按用户本轮确认实施初版。审核已有 T/F/L，以 SAP 为直接分析规格，追溯 Protocol 中 estimand 或决策目标；不限定随机设计或试验分期。重点覆盖分析完整性、歧义、脚注及可执行性。

## 范围和交付

- 七组固定检查：覆盖、SAP 一致性、行列与统计定义、脚注说明、数据支持、T/F/L 专项和跨输出／视觉检查。
- 可选 CRF 与外部规范补足采集证据；全局约定与派生规则按实际适用性判断。
- 三页 Excel、九列批注，作者修改建议、理由、定位和来源同条保留。分析与 Shell 多对多，缺失输出仍可挂到分析 ID。
- 单独 JSON 审查记录支持研究专项扩展及可选检查明细，源文件只读，不覆盖已有交付。

## Phase

| Phase | 完成标准 | 状态 |
|---|---|---|
| P1 | Skill、检查表、输出构建器、合成评测材料、验证及安装 | done |

## 验证口径

机械测试验证输出合同与路由。六份 clean/seeded 合成材料用于十个待执行行为用例，不将代码测试计作专业检出率。行为评分答案键与输入分开。实际病例与 Office 渲染验证留待后续运行。

## 同步记录

2026-11-06：主文档、注册表、索引和安装随本版同步；运行结果见 R052。
