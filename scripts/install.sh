#!/usr/bin/env bash
# Install script: symlink project skill directories to ~/.claude/skills/
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CLAUDE_SKILLS="${HOME}/.claude/skills"
SKILL_NAME="${1:-}"

mkdir -p "$CLAUDE_SKILLS"

# Discover skill directories (those with SKILL.md at project root)
skills=()
for dir in "$PROJECT_ROOT"/*/; do
    name=$(basename "$dir")
    # Exclude non-skill directories
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

echo "Linking skill(s) to $CLAUDE_SKILLS..."
echo ""

for name in "${skills[@]}"; do
    source="$PROJECT_ROOT/$name"
    target="$CLAUDE_SKILLS/$name"

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

echo ""
echo "Done. Linked skills are available to Claude Code."
echo "Verify with: ls -la '$CLAUDE_SKILLS'"
