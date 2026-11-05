from __future__ import annotations

import json
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PACKAGE_ASSETS = {
    "contract_registry": PACKAGE_ROOT / "package_assets" / "contract_registry.json",
    "catalog_subset": PACKAGE_ROOT / "package_assets" / "catalog_subset.json",
    "output_manifest": PACKAGE_ROOT / "package_assets" / "output_manifest.json",
    "minimal_runtime_requirements": PACKAGE_ROOT / "package_assets" / "minimal_runtime_requirements.txt",
    "example_requests": PACKAGE_ROOT / "examples" / "recommend_then_generate_non_oncology.json",
    "product_alignment_contract": PACKAGE_ROOT / "docs" / "product_alignment_contract.md",
    "docx_shell_contract": PACKAGE_ROOT / "docs" / "docx_shell_contract.md",
    "xlsx_workbook_contract": PACKAGE_ROOT / "docs" / "xlsx_workbook_contract.md",
    "sop_contract": PACKAGE_ROOT / "docs" / "sop_contract.md",
    "table_layout_contract": PACKAGE_ROOT / "docs" / "table_layout_contract.md",
    "catalog_schema_contract": PACKAGE_ROOT / "docs" / "catalog_schema_contract.md",
}


def get_required_asset_paths() -> dict[str, Path]:
    return dict(REQUIRED_PACKAGE_ASSETS)


def describe_package_bundle() -> dict:
    inventory: dict[str, dict] = {}
    all_present = True

    for key, asset_path in REQUIRED_PACKAGE_ASSETS.items():
        present = asset_path.exists()
        all_present = all_present and present
        inventory[key] = {
            "present": present,
            "path": str(asset_path),
            "relative_path": str(asset_path.relative_to(PACKAGE_ROOT)).replace("\\", "/"),
        }

    contract_registry_path = REQUIRED_PACKAGE_ASSETS["contract_registry"]
    if contract_registry_path.exists():
        registry = json.loads(contract_registry_path.read_text(encoding="utf-8"))
        inventory["contract_registry"]["entry_count"] = len(registry.get("contracts", {}))

    catalog_subset_path = REQUIRED_PACKAGE_ASSETS["catalog_subset"]
    if catalog_subset_path.exists():
        catalog_subset = json.loads(catalog_subset_path.read_text(encoding="utf-8"))
        inventory["catalog_subset"]["item_count"] = len(catalog_subset.get("items", []))
        inventory["catalog_subset"]["governed_sections"] = catalog_subset.get("governed_sections", [])

    output_manifest_path = REQUIRED_PACKAGE_ASSETS["output_manifest"]
    if output_manifest_path.exists():
        output_manifest = json.loads(output_manifest_path.read_text(encoding="utf-8"))
        inventory["output_manifest"]["manifest_version"] = output_manifest.get("manifest_version")
        inventory["output_manifest"]["product_version"] = output_manifest.get("product_version")

    return {
        "package_root": str(PACKAGE_ROOT),
        "self_contained_ready": all_present,
        **inventory,
    }
