# Catalog Schema 契约

## 1. 范围

Skill 包在以下位置携带 Product 对齐的 catalog 子集：

- `package_assets/catalog_subset.json`

该子集是推荐、生成说明与输出验证所需的最小可迁移 catalog 表面。

## 2. 受控章节

受控章节为：

- `14.1`
- `14.2`
- `14.3`
- `14.4`
- `16.2`

## 3. 必需字段

catalog 子集中的每个 item 必须包含：

- `id`
- `display_label`
- `title`
- `type`
- `section`
- `shell_family`
- `study_phase_scope`
- `coverage_summary`
- `population`
- `applicability`
- `source_listing`

这些字段对应 DOCX、XLSX、SOP 与验证 helper 使用的 Product catalog 字段。

## 4. 受控取值

`type` must be one of:

- `Table`
- `Figure`
- `Listing`

`applicability` must be one of:

- `General`
- `Oncology only`
- `Non-Oncology only`

## 5. Identity 规则

display label 由 internal ID 稳定派生：

- `T14.2.11` becomes `Table 14.2.11`
- `F14.2.4` becomes `Figure 14.2.4`
- `L16.2.3` becomes `Listing 16.2.3`

Skill 不得静默改写 ID 或 display label。
