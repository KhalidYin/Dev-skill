# Product 对齐契约

## 1. 目的

本文档定义 Skill 包对当前 TFLs-Shell Product 输出行为的对齐承诺。

Skill 包不应要求调用者阅读上游 Product 代码。它必须随包携带稳定、可观察、可验证的生成契约，以便在其他项目中复现 Product 对齐输出。

## 2. 对齐层级

本包追求 contract-level alignment，不追求文件字节级完全一致。

契约级一致意味着：

- 表达同一组受控章节。
- 保留同一组 catalog identity 与 metadata 字段。
- 生成同一类 DOCX / XLSX / SOP 结构。
- 应用同一组 table layout 与 placeholder 语义。
- 生成物可由 Skill 包内 helper 进行验证。

## 3. 正式输出

对齐输出集包括：

- `TFL_Shell_Template_v<version>.docx`
- `TFL_TOC_v<version>.xlsx`
- `TFL_Shell_SOP_v<version>.docx`

当前 Product 对齐的机器可读摘要存放于：

- `package_assets/output_manifest.json`

当前验证入口为：

- `scripts/validate_outputs.py`

## 4. 契约来源

包内契约分布在：

- `docs/catalog_schema_contract.md`
- `docs/docx_shell_contract.md`
- `docs/xlsx_workbook_contract.md`
- `docs/sop_contract.md`
- `docs/table_layout_contract.md`
- `package_assets/contract_registry.json`
- `scripts/alignment_contracts.py`

## 5. 防漂移规则

当 Product 生成器、catalog 字段、输出命名、sheet 结构、DOCX layout、SOP 文案或 table layout 发生变化时，维护者必须在同一轮变更中更新 Skill 包。

建议维护闭环：

1. 更新 Product 实现或 catalog。
2. 运行 `scripts/export_catalog_subset.py`。
3. 运行 `scripts/export_product_contracts.py`。
4. 生成 DOCX / XLSX / SOP 输出。
5. 运行 `scripts/validate_outputs.py`。
6. 运行仓库测试。
