#!/usr/bin/env bash
# KS Cognitive Engine — Automated Installer
set -euo pipefail

SKILL_NAME="ks-cognitive-engine"
TARGET_DIR="${HOME}/.agents/skills/${SKILL_NAME}"
GITHUB_RAW="https://raw.githubusercontent.com/rbgroupsolutionsllc-eng/ks-cognitive-engine/master"

echo "🧠 Installing KS Cognitive Engine into ${TARGET_DIR}..."

mkdir -p "${TARGET_DIR}"

if [ -f "SKILL.md" ]; then
    cp SKILL.md "${TARGET_DIR}/SKILL.md"
else
    curl -fsSL "${GITHUB_RAW}/SKILL.md" -o "${TARGET_DIR}/SKILL.md"
fi

echo "✅ KS Cognitive Engine successfully installed!"
echo "👉 Your agents (Claude Code, Antigravity, OpenCode, Codex) will now automatically adhere to KS operational rules."
