from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _bootstrap_repo_imports() -> None:
    current_path = Path(__file__).resolve()
    repo_root = next(
        (
            parent
            for parent in current_path.parents
            if (parent / "pyproject.toml").exists() and (parent / "src" / "tflshell").exists()
        ),
        None,
    )
    package_root = current_path.parents[1]
    if str(package_root) not in sys.path:
        sys.path.insert(0, str(package_root))
    if repo_root is not None:
        src_path = repo_root / "src"
        if str(src_path) not in sys.path:
            sys.path.insert(0, str(src_path))
    else:
        from importlib.util import find_spec

        if find_spec("tflshell") is None:
            raise RuntimeError(
                "缺少 tflshell Product 依赖；请按 Skill references/integration.md 安装上游 Product。"
            )

_bootstrap_repo_imports()

from tflshell import __version__  # noqa: E402
from tflshell.data.definitions import build_catalog  # noqa: E402
from alignment_contracts import (  # noqa: E402
    DOCX_EXPECTED_MARGIN_INCHES,
    DOCX_EXPECTED_PAGE_HEIGHT_INCHES,
    DOCX_EXPECTED_PAGE_WIDTH_INCHES,
    DOCX_EXPECTED_SECTION_COUNT,
    DOCX_REQUIRED_INTRO_TEXT,
    DOCX_TEMPLATE_HEADING1,
    DOCX_TEMPLATE_INTRO_HEADINGS,
    SOP_APPENDIX_HEADINGS,
    SOP_GOVERNED_SCOPE_TEXT,
    SOP_HEADER_TABLE_LABELS,
    SOP_REQUIRED_HEADINGS,
    SOP_TEMPLATE_TITLE,
    XLSX_CATALOG_COLUMNS,
    XLSX_CHANGE_LOG_COLUMNS,
    XLSX_EXPECTED_SHEETS,
    XLSX_USAGE_TOPICS,
)


PACKAGE_ROOT = Path(__file__).resolve().parents[1]


def build_output_manifest() -> dict:
    catalog = build_catalog()
    section_summary = catalog.section_summary()
    return {
        "manifest_version": "product-aligned-output-contract-v1",
        "product_version": __version__,
        "governed_sections": ["14.1", "14.2", "14.3", "14.4", "16.2"],
        "catalog_summary": catalog.summary_stats(),
        "section_summary": section_summary,
        "formal_outputs": {
            "docx_shell_template": {
                "file_name_pattern": f"TFL_Shell_Template_v{__version__}.docx",
                "page_setup": {
                    "section_count": DOCX_EXPECTED_SECTION_COUNT,
                    "width_inches": DOCX_EXPECTED_PAGE_WIDTH_INCHES,
                    "height_inches": DOCX_EXPECTED_PAGE_HEIGHT_INCHES,
                    "margin_inches": DOCX_EXPECTED_MARGIN_INCHES,
                },
                "heading_contract": {
                    "heading_1": sorted(DOCX_TEMPLATE_HEADING1),
                    "intro_heading_2": sorted(DOCX_TEMPLATE_INTRO_HEADINGS),
                    "tfl_shell_heading_style": "Heading 4",
                    "tfl_shell_heading_count": len(catalog.all()),
                },
                "body_contract": {
                    "table_and_listing_body_table_count": len([
                        item for item in catalog.all()
                        if item.tfl_type.value in ("Table", "Listing")
                    ]),
                    "required_intro_text": DOCX_REQUIRED_INTRO_TEXT,
                    "controlled_group_headers": ["Group 1", "Group 2"],
                    "separate_expansion_column": "...",
                },
            },
            "xlsx_toc_workbook": {
                "file_name_pattern": f"TFL_TOC_v{__version__}.xlsx",
                "sheet_names": XLSX_EXPECTED_SHEETS,
                "catalog_columns": XLSX_CATALOG_COLUMNS,
                "section_sheet_row_counts": {
                    sheet_name: section_summary[section_number]["total"]
                    for sheet_name, section_number in {
                        "14.1_Demographics": "14.1",
                        "14.2_Efficacy": "14.2",
                        "14.3_Safety": "14.3",
                        "14.4_Special": "14.4",
                        "16.2_Listings": "16.2",
                    }.items()
                },
                "field_definition_count": len(XLSX_CATALOG_COLUMNS),
                "usage_topics": sorted(XLSX_USAGE_TOPICS),
                "change_log_columns": XLSX_CHANGE_LOG_COLUMNS,
            },
            "sop_governance_doc": {
                "file_name_pattern": f"TFL_Shell_SOP_v{__version__}.docx",
                "title": SOP_TEMPLATE_TITLE,
                "scope_text": SOP_GOVERNED_SCOPE_TEXT,
                "header_table_labels": sorted(SOP_HEADER_TABLE_LABELS),
                "required_headings": sorted(SOP_REQUIRED_HEADINGS),
                "appendix_headings": sorted(SOP_APPENDIX_HEADINGS),
            },
        },
        "validation_entrypoint": "scripts/validate_outputs.py",
    }


def build_contract_registry() -> dict:
    return {
        "package_name": "tfls-shell",
        "registry_version": "1.1.0",
        "contracts": {
            "xlsx_master_sheet": {
                "helper_module": "scripts/alignment_contracts.py",
                "detail_keys": [
                    "TFL ID",
                    "Display Label",
                    "Type",
                    "Section",
                    "Shell Family",
                    "Study Phase Scope",
                    "Coverage Summary",
                    "Population",
                    "Applicability",
                    "Row Count",
                ],
                "notes": [
                    "用于声明 workbook 主表的稳定治理字段 contract。",
                    "字段命名与 TOC_Master 表头保持对齐。",
                ],
            },
            "xlsx_workbook": {
                "helper_module": "scripts/alignment_contracts.py",
                "detail_keys": [
                    "Workbook Sheets",
                    "Catalog Sheet Columns",
                    "Section Sheet Row Counts",
                    "Field Definitions",
                    "Usage Guide",
                    "Change Log",
                ],
                "notes": [
                    "用于声明完整 XLSX workbook 的可观察结构 contract。",
                    "覆盖 sheet 名、字段、解释页、使用说明和变更记录。",
                ],
            },
            "docx_shell_template": {
                "helper_module": "scripts/alignment_contracts.py",
                "detail_keys": [
                    "Heading 4",
                    "Section Heading",
                    "Display Label",
                    "Title",
                    "Analysis Set",
                    "Protocol",
                    "Sponsor",
                ],
                "notes": [
                    "用于声明 shell 模板 heading 与 header block 的稳定 contract。",
                    "当前顺序与项目内 DOCX 生成逻辑保持一致。",
                ],
            },
            "docx_layout": {
                "helper_module": "scripts/alignment_contracts.py",
                "detail_keys": [
                    "Landscape Letter Page Setup",
                    "Margins",
                    "Introduction Headings",
                    "Usage Notes",
                    "Body Table Count",
                    "Group Headers",
                ],
                "notes": [
                    "用于声明 DOCX 主模板页面、说明文本和表格 layout contract。",
                    "覆盖 Product 已实现的三线表和受控组别展示语义。",
                ],
            },
            "sop_governance_doc": {
                "helper_module": "scripts/alignment_contracts.py",
                "detail_keys": [
                    "Title",
                    "Scope",
                    "Cross-Output Alignment",
                    "Quality Gates",
                    "Classification",
                    "Appendix A",
                    "Appendix B",
                ],
                "notes": [
                    "用于声明 SOP 治理文档的稳定结构与关键文案 contract。",
                    "当前聚焦头表、scope、quality gate 和 appendix 层。",
                ],
            },
        },
    }


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="从 Product 当前实现导出 Skill 包使用的输出契约资产。")
    parser.add_argument(
        "--manifest-output",
        default=str(PACKAGE_ROOT / "package_assets" / "output_manifest.json"),
    )
    parser.add_argument(
        "--registry-output",
        default=str(PACKAGE_ROOT / "package_assets" / "contract_registry.json"),
    )
    args = parser.parse_args(argv)

    manifest_path = Path(args.manifest_output)
    registry_path = Path(args.registry_output)
    _write_json(manifest_path, build_output_manifest())
    _write_json(registry_path, build_contract_registry())
    print(manifest_path)
    print(registry_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
