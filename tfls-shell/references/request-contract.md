# 输入和交付契约 v2

Agent 解释材料，复用已有答案并集中询问关键缺口。研究特定模式缺少分期、领域、终点、分析集、治疗组、时间点或存在不可读资料/冲突时返回 `needs_information`，退出码 2，不发布业务文件。仅当用户要求通用模板或接受通用模板时使用 `--generic-template`。

## 配置

```json
{
  "study": {
    "phase": "phase-ii",
    "area": "oncology",
    "endpoints": ["PFS"],
    "populations": ["ITT", "Safety Population"],
    "groups": ["Active", "Placebo"],
    "timepoints": ["Baseline", "Week 12"],
    "shell_ids": ["T14.1.1"],
    "shell_overrides": {
      "T14.1.1": {"population": "ITT", "table_notes": "Baseline assessment"}
    }
  },
  "delivery": {
    "document_version": "1.0",
    "language": "en",
    "paper": "a4",
    "orientation": "landscape",
    "margin_inches": 0.75,
    "font": "Times New Roman",
    "presentation_profile": "csr_standard",
    "sponsor": "Example Sponsor",
    "protocol": "STUDY-001",
    "study_title": "Example study",
    "group_labels": ["Active", "Placebo"],
    "header_labels": {"Overall": "Total"}
  },
  "translations": {}
}
```

- `study` 还接受 `sections`；分期为 `phase-i/phase-ii/phase-iii/mixed/unknown`，领域为 `oncology/non-oncology/all/unknown`。未知键、无效 ID 和重复 ID 拒绝。
- `shell_ids` 为 agent 复核后的实际选择，优先于自动候选。`shell_overrides` 仅接受选中 ID 的 `title/population/table_notes`。收集的时间点不会自动修改全部 shell，应按材料映射到对应 shell 说明。
- `group_labels` 按顺序改写通用治疗列，支持一个或多个组，保留 Overall/HR 等独立列；N 继续用 XX。特殊表头需单独复核。
- `language` 为 `en/zh/bilingual`；纸张 `letter/a4`；方向 `landscape/portrait`；字体使用系统可用字体。
- `presentation_profile` 为 `csr_standard/compact_review/authoring_shell`，控制 DOCX 间距。纸张、边距和字体适配三类产物，XLSX 对应打印设置。
- `header_labels` 为精确标签替换。Sponsor 模板先由 agent 检查并映射；配置 `sponsor_template` 表示尚待映射，脚本返回缺口，不自动导入模板。
- 语言和格式优先用用户要求。获准采用默认时明确说明：英文、Letter 横向、0.75 英寸、Times New Roman、标准间距、版本 `0.1-draft`。

## 调用

```powershell
python -X utf8 tfls-shell/scripts/recommend_then_generate.py --config request.json --mode recommend --no-figures --json
python -X utf8 tfls-shell/scripts/recommend_then_generate.py --config request.json --type all --no-figures --output-dir ./delivery-1 --json
python -X utf8 tfls-shell/scripts/validate_outputs.py --contract ./delivery-1/delivery-contract_v1.0.json --json
```

完整通用 catalog 用 `generate_project_aligned_outputs.py --generic-template`。推荐入口的通用模式仍按候选筛选。只推荐不创建输出目录。`--text` 与 UTF-8 `--input-file` 继续支持，常见中文信号及 PFS/OS 缩写仅辅助 agent 全文理解。

## 本地化

非英文模式先在临时目录生成，收集可见文本。缺少精确翻译映射时返回 `needs_localization` 和 `localization_strings`，不发布半成品。Agent 将完整字符串逐一翻译到 `translations`；不得用空值或原文冒充译文。双语按源文加换行译文输出。

译文包括标题、说明、脚注、表格标签、页眉页脚和 XLSX 可见文本。ID 和内部工作表名称保持稳定。机械检查只验证映射应用，语义和可读性由 agent 复核。图形内文字未覆盖，非英文模式应关闭图形生成或报告适配缺口。

## 发布和检查

- 状态为 `recommended/generated/needs_information/needs_localization/validation_failed/error`。仅前两种退出码 0。
- 输出记录生成器版本和独立交付版本。契约记录当前选择、格式及预期标题/表头，业务文件与契约一起保留。
- 检查标题顺序、无重复标题、列结构、XLSX ID/标题及字体、DOCX/SOP 版本及页面、Protocol 页眉。按本次配置检查，不能用固定英文基线判定定制交付。
- 先暂存并验证，再排他创建最终文件，已存在则拒绝。发布失败只清理本次创建的文件。
- Word 打开后更新目录字段；移除冗余标题不会删除 Heading 4 或书签。
- 带 `--contract` 检查本次交付；无该参数仍是原始 Product 基线检查。
