from __future__ import annotations

import json
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
CATALOG_SUBSET_PATH = PACKAGE_ROOT / "package_assets" / "catalog_subset.json"


def load_catalog_subset() -> dict:
    return json.loads(CATALOG_SUBSET_PATH.read_text(encoding="utf-8"))


def all_items() -> list[dict]:
    return load_catalog_subset()["items"]


def get_item(item_id: str) -> dict | None:
    for item in all_items():
        if item["id"] == item_id:
            return item
    return None


def items_by_section(section: str) -> list[dict]:
    return [item for item in all_items() if item["section"] == section]
