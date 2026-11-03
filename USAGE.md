# 使用指南

## 前置条件

- Python 3（用于脚手架、校验、索引和打包脚本）
- Windows PowerShell，或 macOS/Linux shell（用于安装 skill 链接）

## 常用命令

```powershell
# 创建新 skill
python scripts/new_skill.py

# 安装单个 skill
.\scripts\install.ps1 -SkillName <skill-name>

# 校验所有 skill
python scripts/validate_all.py

# 更新 skill 索引
python scripts/generate_index.py

# 打包所有 skill
python scripts/package_all.py
```

## 开发流程

1. 使用 `scripts/new_skill.py` 创建顶层 skill 目录。
2. 编辑 `SKILL.md`，按需增加 `references/`、`scripts/`、`assets/` 或 `evals/`。
3. 更新 `.skill-registry.json` 的状态、分类、标签和修改日期。
4. 运行安装、全量校验和索引生成命令。

## 注意事项

- 每个顶层 skill 目录必须包含 `SKILL.md`。
- Skill 元数据用于触发，主体和资源按需加载；避免把全部领域知识写入 `SKILL.md`。
- 安装脚本会尝试链接到本机已存在的多个 agent skill 目录。

## Generate SAP 初版

安装后显式调用：

```text
$generate-sap 根据提供的 Protocol、统计决定和 Sponsor 约定生成一份结构完整、依据可追溯的 SAP review draft。
```

该 skill 当前为 draft。即使输入不完整，也会保留完整 SAP 结构，并在对应章节插入稳定的 TBD、Author Query 或 Conflict。宿主允许网络搜索时，它会查找同类公开 SAP，明确记录直接引用、相似点和差异；检索不可用时会显式降级。输出必须由合格的临床试验统计师审核，不负责 TFL/ADaM 生成或统计编程。

## Review SAP 初版

安装后显式调用：

```text
$review-sap 对照附件 Protocol 审阅这份 SAP，输出 Excel 问题清单。
```

该 skill 当前为 draft，面向外部 SAP。v1 审阅维度为结构完整性、内部一致性、与 Protocol 一致性和可编程性（ADaM/TFL 就绪度），方法学恰当性不在范围内。依赖 Python 3.9+、`openpyxl`、`pyyaml`；生成 docx 批注另需 `python-docx` 1.2+，且仅在用户确认后执行。输出必须由合格统计师复核，不构成批准或合规结论。
