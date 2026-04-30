"""Shared utilities for Dev-skill tooling."""

import json
import os
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = PROJECT_ROOT / ".skill-registry.json"
TEMPLATES_DIR = PROJECT_ROOT / "templates"
DIST_DIR = PROJECT_ROOT / "dist"
CLAUDE_SKILLS_DIR = Path.home() / ".claude" / "skills"


def load_registry():
    """Load .skill-registry.json. Returns empty dict if missing."""
    if not REGISTRY_PATH.exists():
        return {"version": "1", "skills": {}}
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_registry(registry):
    """Save .skill-registry.json with sorted keys."""
    with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)
        f.write("\n")


def get_skill_dirs():
    """Yield Paths to all skill directories in the project (by registry or scan).

    Falls back to scanning for SKILL.md in immediate subdirectories.
    """
    registry = load_registry()
    if registry.get("skills"):
        for name in registry["skills"]:
            skill_dir = PROJECT_ROOT / name
            if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                yield skill_dir
    else:
        for entry in PROJECT_ROOT.iterdir():
            if entry.is_dir() and (entry / "SKILL.md").exists():
                yield entry


def parse_frontmatter(filepath):
    """Parse YAML frontmatter from a SKILL.md file. Returns dict or None.

    Uses a minimal regex parser to avoid pyyaml dependency.
    Falls back to yaml.safe_load if available.
    """
    content = Path(filepath).read_text(encoding="utf-8")
    if not content.startswith("---"):
        return None
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return None
    frontmatter_text = match.group(1)
    try:
        import yaml
        return yaml.safe_load(frontmatter_text)
    except ImportError:
        return _parse_simple_yaml(frontmatter_text)


def _parse_simple_yaml(text):
    """Minimal YAML parser for skill frontmatter (handles quoted strings)."""
    result = {}
    for line in text.strip().split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = re.match(r'^(\w[\w-]*)\s*:\s*(.*)', line)
        if m:
            key = m.group(1)
            value = m.group(2).strip()
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            result[key] = value
    return result
