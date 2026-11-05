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

from tflshell.data.definitions import build_catalog  # noqa: E402


GOVERNED_SECTIONS = ["14.1", "14.2", "14.3", "14.4", "16.2"]


def build_export_payload() -> dict:
    catalog = build_catalog()
    items = []
    for item in catalog.all():
        items.append(
            {
                "id": item.id,
                "display_label": item.display_label,
                "title": item.title,
                "type": item.tfl_type.value,
                "section": item.section.number,
                "shell_family": item.shell_family_label,
                "study_phase_scope": item.study_phase_scope_label,
                "coverage_summary": item.coverage_summary_label,
                "population": item.population,
                "applicability": item.applicability_label,
                "source_listing": item.source_listing,
            }
        )
    return {
        "catalog_version": "product-aligned-subset-v1",
        "governed_sections": GOVERNED_SECTIONS,
        "item_count": len(items),
        "items": items,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="从 Product 导出 Skill 包使用的最小 catalog 子集。")
    parser.add_argument(
        "--output",
        default=str(Path(__file__).resolve().parents[1] / "package_assets" / "catalog_subset.json"),
    )
    args = parser.parse_args(argv)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(build_export_payload(), indent=2, ensure_ascii=False), encoding="utf-8")
    print(output_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
