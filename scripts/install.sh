#!/usr/bin/env bash
# Install script: symlink project skill directories to ~/.claude/skills/ and ~/.codex/skills/
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TARGET_DIRS=("${HOME}/.claude/skills" "${HOME}/.codex/skills")
SKILL_NAME="${1:-}"

# Discover skill directories (those with SKILL.md at project root)
skills=()
for dir in "$PROJECT_ROOT"/*/; do
    name=$(basename "$dir")
    case "$name" in
        scripts|templates|dist|.git) continue ;;
    esac
    if [ -f "$dir/SKILL.md" ]; then
        skills+=("$name")
    fi
done

if [ -n "$SKILL_NAME" ]; then
    skills=("$SKILL_NAME")
fi

if [ ${#skills[@]} -eq 0 ]; then
    echo "No skill directories found in project root."
    exit 0
fi

for target_dir in "${TARGET_DIRS[@]}"; do
    mkdir -p "$target_dir"
    echo "Linking skill(s) to $target_dir..."
    echo ""
    for name in "${skills[@]}"; do
        source="$PROJECT_ROOT/$name"
        target="$target_dir/$name"

        # Remove existing target if present
        if [ -e "$target" ] || [ -L "$target" ]; then
            rm -rf "$target"
            echo "  [$name] Removed old link"
        fi

        ln -s "$source" "$target"
        echo "  [$name] Linked"
    done
    echo ""
done

echo "Done. Linked skills are available to Claude Code and Codex."
