from __future__ import annotations

import json
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = PACKAGE_ROOT / "package_assets" / "contract_registry.json"


def load_contract_registry() -> dict:
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def get_contract(name: str) -> dict:
    return load_contract_registry()["contracts"][name]


def list_contracts() -> list[str]:
    return sorted(load_contract_registry()["contracts"].keys())
