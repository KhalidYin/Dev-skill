#!/usr/bin/env python3
"""Scaffold a new skill directory from templates."""

import re
import sys
import shutil
from pathlib import Path

from utils import (
    PROJECT_ROOT,
    REGISTRY_PATH,
    TEMPLATES_DIR,
    load_registry,
    save_registry,
)


def validate_name(name):
    """Validate kebab-case skill name. Returns (valid, error_message)."""
    if not name:
        return False, "Name cannot be empty."
    if not re.match(r"^[a-z0-9-]+$", name):
        return False, "Name must be kebab-case (lowercase letters, digits, hyphens only)."
    if name.startswith("-") or name.endswith("-") or "--" in name:
        return False, "Name cannot start/end with hyphen or contain consecutive hyphens."
    if len(name) > 64:
        return False, f"Name is too long ({len(name)} chars). Maximum is 64."
    return True, ""


def skill_exists(name):
    """Check if a skill directory already exists."""
    return (PROJECT_ROOT / name).exists()


def scaffold(name, description):
    """Create a new skill directory from template."""
    skill_dir = PROJECT_ROOT / name
    if skill_dir.exists():
        print(f"Error: Directory already exists: {skill_dir}")
        return False

    # Derive title: convert kebab-case to Title Case
    title = " ".join(word.capitalize() for word in name.split("-"))

    # Create directory and SKILL.md from template
    skill_dir.mkdir(parents=True)
    template_path = TEMPLATES_DIR / "SKILL.md.template"
    if template_path.exists():
        content = template_path.read_text(encoding="utf-8")
        content = content.replace("{{SKILL_NAME}}", name)
        content = content.replace("{{SKILL_DESCRIPTION}}", description)
        content = content.replace("{{SKILL_TITLE}}", title)
    else:
        content = f'---\nname: {name}\ndescription: "{description}"\n---\n\n# {title}\n'

    (skill_dir / "SKILL.md").write_text(content, encoding="utf-8")

    # Create evals/ from template
    evals_dir = skill_dir / "evals"
    evals_dir.mkdir()
    evals_template = TEMPLATES_DIR / "evals.json.template"
    if evals_template.exists():
        evals_content = evals_template.read_text(encoding="utf-8")
        evals_content = evals_content.replace("{{SKILL_NAME}}", name)
        (evals_dir / "evals.json").write_text(evals_content, encoding="utf-8")
        (evals_dir / "files").mkdir()

    # Register in .skill-registry.json
    registry = load_registry()
    registry["skills"][name] = {
        "status": "draft",
        "category": "",
        "last_modified": "",
        "has_evals": True,
        "tags": [],
    }
    save_registry(registry)

    print(f"\nCreated skill: {skill_dir}")
    print(f"  SKILL.md   - edit this to define the skill behavior")
    print(f"  evals/     - add test cases in evals.json")
    print(f"\nRegistered in {REGISTRY_PATH}")
    print(f"\nNext steps:")
    print(f"  1. Edit {skill_dir / 'SKILL.md'} to define your skill")
    print(f"  2. Run install script to link into ~/.claude/skills/")
    print(f"  3. Test the skill in another project")
    return True


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Scaffold a new Claude Code skill")
    parser.add_argument("--name", "-n", help="Skill name (kebab-case)")
    parser.add_argument("--description", "-d", help="One-line skill description")
    args = parser.parse_args()

    name = args.name
    if not name:
        name = input("Skill name (kebab-case, e.g. my-awesome-skill): ").strip()

    valid, error = validate_name(name)
    if not valid:
        print(f"Error: {error}")
        sys.exit(1)

    if skill_exists(name):
        print(f"Error: A file or directory named '{name}' already exists.")
        sys.exit(1)

    description = args.description
    if not description:
        description = input("One-line description: ").strip()

    if not description:
        print("Error: Description cannot be empty.")
        sys.exit(1)

    if "<" in description or ">" in description:
        print("Error: Description cannot contain angle brackets (< or >).")
        sys.exit(1)

    if len(description) > 1024:
        print(f"Error: Description too long ({len(description)} chars). Maximum is 1024.")
        sys.exit(1)

    success = scaffold(name, description)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
