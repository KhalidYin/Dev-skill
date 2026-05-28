#!/usr/bin/env python3
"""Validate all skills in the project using skill-creator's validation rules.

Falls back to built-in validation if quick_validate.py is not importable.
"""

import sys
from pathlib import Path

from utils import get_skill_dirs

SKILL_CREATOR_VALIDATE = (
    Path.home() / ".claude" / "skills" / "skill-creator" / "scripts" / "quick_validate.py"
)


def builtin_validate(skill_dir):
    """Built-in validation matching quick_validate.py rules (no pyyaml needed)."""
    import re
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return False, "SKILL.md not found"

    content = skill_md.read_text(encoding="utf-8")
    if not content.startswith("---"):
        return False, "No YAML frontmatter found"

    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"

    frontmatter_text = match.group(1)

    # Try pyyaml first, then simple parser
    try:
        import yaml
        frontmatter = yaml.safe_load(frontmatter_text)
    except ImportError:
        frontmatter = {}
        for line in frontmatter_text.strip().split("\n"):
            m = re.match(r'^(\w[\w-]*)\s*:\s*(.*)', line.strip())
            if m:
                val = m.group(2).strip().strip('"').strip("'")
                frontmatter[m.group(1)] = val

    if not isinstance(frontmatter, dict):
        return False, "Frontmatter must be a YAML dictionary"

    ALLOWED = {"name", "description", "license", "allowed-tools", "metadata", "compatibility"}
    unexpected = set(frontmatter.keys()) - ALLOWED
    if unexpected:
        return False, (
            f"Unexpected key(s): {', '.join(sorted(unexpected))}. "
            f"Allowed: {', '.join(sorted(ALLOWED))}"
        )

    if "name" not in frontmatter:
        return False, "Missing 'name' in frontmatter"
    if "description" not in frontmatter:
        return False, "Missing 'description' in frontmatter"

    name = frontmatter.get("name", "")
    if not isinstance(name, str):
        return False, f"Name must be a string, got {type(name).__name__}"
    name = name.strip()
    if name:
        if not re.match(r"^[a-z0-9-]+$", name):
            return False, f"Name '{name}' should be kebab-case"
        if name.startswith("-") or name.endswith("-") or "--" in name:
            return False, f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens"
        if len(name) > 64:
            return False, f"Name too long ({len(name)} chars). Max 64."

    description = frontmatter.get("description", "")
    if not isinstance(description, str):
        return False, f"Description must be a string, got {type(description).__name__}"
    if "<" in description or ">" in description:
        return False, "Description cannot contain angle brackets (< or >)"
    if len(description) > 1024:
        return False, f"Description too long ({len(description)} chars). Max 1024."

    return True, "Skill is valid!"


def main():
    skills = list(get_skill_dirs())
    if not skills:
        print("No skills found.")
        return

    # Try to use the official validator, fall back to builtin
    validate_fn = builtin_validate
    if SKILL_CREATOR_VALIDATE.exists():
        sys.path.insert(0, str(SKILL_CREATOR_VALIDATE.parent))
        try:
            from quick_validate import validate_skill
            validate_fn = validate_skill
        except ImportError as e:
            print(f"Note: skill-creator validator unavailable ({e}), using builtin.\n")

    all_valid = True
    for skill_dir in sorted(skills):
        try:
            valid, message = validate_fn(skill_dir)
        except UnicodeDecodeError as e:
            if validate_fn is builtin_validate:
                raise
            print(
                f"Note: skill-creator validator encoding error for {skill_dir.name} "
                f"({e}), using builtin."
            )
            valid, message = builtin_validate(skill_dir)

        status = "PASS" if valid else "FAIL"
        print(f"  [{status}] {skill_dir.name}: {message}")
        if not valid:
            all_valid = False

    print()
    if all_valid:
        print(f"All {len(skills)} skill(s) validated successfully.")
    else:
        print("Some skills have validation errors. Fix them before packaging.")
        sys.exit(1)


if __name__ == "__main__":
    main()
