#!/usr/bin/env python3
"""Batch-packager: creates .skill files for all (or one) skills in the project."""

import sys
import zipfile
import fnmatch
from pathlib import Path

from utils import PROJECT_ROOT, DIST_DIR, get_skill_dirs

EXCLUDE_DIRS = {"__pycache__", "node_modules"}
EXCLUDE_GLOBS = {"*.pyc"}
EXCLUDE_FILES = {".DS_Store"}
ROOT_EXCLUDE_DIRS = {"evals"}


def should_exclude(rel_path, skill_name):
    """Check if a path should be excluded from packaging."""
    parts = rel_path.parts
    if any(part in EXCLUDE_DIRS for part in parts):
        return True
    if len(parts) > 1 and parts[1] in ROOT_EXCLUDE_DIRS:
        return True
    name = rel_path.name
    if name in EXCLUDE_FILES:
        return True
    return any(fnmatch.fnmatch(name, pat) for pat in EXCLUDE_GLOBS)


def package_one(skill_dir, output_dir=None):
    """Package a single skill directory into a .skill file."""
    skill_dir = Path(skill_dir).resolve()
    output_dir = Path(output_dir or DIST_DIR).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    skill_name = skill_dir.name
    output_path = output_dir / f"{skill_name}.skill"

    try:
        with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for file_path in skill_dir.rglob("*"):
                if not file_path.is_file():
                    continue
                arcname = file_path.relative_to(skill_dir.parent)
                if should_exclude(arcname, skill_name):
                    print(f"    Skipped: {arcname}")
                    continue
                zf.write(file_path, arcname)
                print(f"    Added: {arcname}")
        print(f"  -> {output_path}")
        return True
    except Exception as e:
        print(f"  Error: {e}")
        return False


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Package skills into .skill files")
    parser.add_argument("--skill", "-s", help="Package a single skill by name")
    parser.add_argument("--output", "-o", default=str(DIST_DIR), help="Output directory")
    args = parser.parse_args()

    skills = list(get_skill_dirs())
    if not skills:
        print("No skills found.")
        return

    if args.skill:
        skills = [d for d in skills if d.name == args.skill]
        if not skills:
            print(f"Skill '{args.skill}' not found in registry.")
            sys.exit(1)

    print(f"Packaging {len(skills)} skill(s) to {args.output}...\n")
    for skill_dir in sorted(skills):
        print(f"  {skill_dir.name}/")
        package_one(skill_dir, args.output)

    print(f"\nDone. Output: {args.output}")


if __name__ == "__main__":
    main()
