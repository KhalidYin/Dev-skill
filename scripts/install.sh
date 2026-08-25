#!/usr/bin/env bash
# Install script: symlink project skill directories to Claude, Codex, Agents, and Workbuddy skill roots.
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TARGET_DIRS=("${HOME}/.claude/skills" "${HOME}/.codex/skills" "${HOME}/.agents/skills" "${HOME}/.workbuddy/skills")
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
    if [ ! -d "$target_dir" ]; then
        echo "Skipping $target_dir (not found)"
        continue
    fi
    echo "Linking skill(s) to $target_dir..."
    echo ""

    # Phase 1: Remove all existing skill links/copies
    echo "Removing existing skills..."
    for name in "${skills[@]}"; do
        target="$target_dir/$name"
        if [ -e "$target" ] || [ -L "$target" ]; then
            # Skip if target is the source directory (prevent deleting project files)
            if [ "$(realpath "$target")" = "$(realpath "$PROJECT_ROOT/$name")" ]; then
                echo "  [$name] Skipped (source directory)"
                continue
            fi
            rm -rf "$target"
            echo "  [$name] Removed"
        fi
    done

    # Phase 2: Install new skill links
    echo "Installing new skills..."
    for name in "${skills[@]}"; do
        source="$PROJECT_ROOT/$name"
        target="$target_dir/$name"

        ln -s "$source" "$target"
        echo "  [$name] Linked"
    done
    echo ""
done

echo "Done. Linked skills are available to Claude Code, Codex, Agents, and Workbuddy."
