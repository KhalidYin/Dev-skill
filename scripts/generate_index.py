#!/usr/bin/env python3
"""Generate SKILL_INDEX.md from .skill-registry.json + SKILL.md frontmatter."""

from pathlib import Path

from utils import PROJECT_ROOT, load_registry, parse_frontmatter


def generate():
    registry = load_registry()
    skills_meta = registry.get("skills", {})

    lines = [
        "# Skill Index",
        "",
        "| Skill | Status | Category | Description |",
        "|-------|--------|----------|-------------|",
    ]

    for name, meta in sorted(skills_meta.items()):
        skill_dir = PROJECT_ROOT / name
        skill_md = skill_dir / "SKILL.md"

        status = meta.get("status", "draft")
        category = meta.get("category", "-")
        description = "-"

        if skill_md.exists():
            fm = parse_frontmatter(skill_md)
            if fm and fm.get("description"):
                desc = fm["description"]
                # Truncate for table readability
                if len(desc) > 120:
                    desc = desc[:117] + "..."
                description = desc

        status_emoji = {"stable": "✅", "draft": "🔨", "deprecated": "⚠️", "archived": "📦"}
        emoji = status_emoji.get(status, "❓")
        lines.append(f"| [{name}]({name}/SKILL.md) | {emoji} {status} | {category} | {description} |")

    lines.extend([
        "",
        "---",
        "",
        f"*Total: {len(skills_meta)} skill(s)*",
        "",
        "**Status legend:** 🔨 draft · ✅ stable · ⚠️ deprecated · 📦 archived",
    ])

    output_path = PROJECT_ROOT / "SKILL_INDEX.md"
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Generated {output_path}")


if __name__ == "__main__":
    generate()
