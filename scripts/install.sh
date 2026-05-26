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

link_skills() {
    local target_dir="$1"

    mkdir -p "$target_dir"

    for name in "${skills[@]}"; do
        source="$PROJECT_ROOT/$name"
        target="$target_dir/$name"

        if [ -L "$target" ]; then
            current_target=$(readlink "$target")
            if [ "$current_target" = "$source" ]; then
                echo "  [$name] Already linked - skipping"
                continue
            else
                echo "  [$name] Link exists but points elsewhere ($current_target). Replacing..."
                rm "$target"
            fi
        elif [ -d "$target" ]; then
            echo "  WARNING: [$name] Real directory exists at $target"
            echo "  Remove it manually if you want to replace it: rm -rf '$target'"
            continue
        fi

        ln -s "$source" "$target"
        echo "  [$name] Linked"
    done
}

for target_dir in "${TARGET_DIRS[@]}"; do
    echo "Linking skill(s) to $target_dir..."
    echo ""
    link_skills "$target_dir"
    echo ""
done

echo "Done. Linked skills are available to Claude Code and Codex."
echo "Verify with: ls -la '${TARGET_DIRS[0]}'"
