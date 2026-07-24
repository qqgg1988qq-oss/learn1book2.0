#!/usr/bin/env bash
set -e

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKILL_NAME="book-reading-share"

echo "验证 Skill: $SKILL_NAME"
echo "目录: $SKILL_DIR"
echo ""

errors=0

check_file() {
  if [ -f "$1" ]; then
    echo "✓ $1"
  else
    echo "✗ 缺少文件: $1"
    errors=$((errors + 1))
  fi
}

check_file "$SKILL_DIR/SKILL.md"
check_file "$SKILL_DIR/template.md"
check_file "$SKILL_DIR/examples/sample.md"
check_file "$SKILL_DIR/scripts/validate.sh"

if [ -f "$SKILL_DIR/SKILL.md" ]; then
  if grep -q "^name: $SKILL_NAME" "$SKILL_DIR/SKILL.md"; then
    echo "✓ SKILL.md frontmatter 包含正确 name"
  else
    echo "✗ SKILL.md frontmatter 中 name 不匹配"
    errors=$((errors + 1))
  fi

  if grep -q "^description:" "$SKILL_DIR/SKILL.md"; then
    echo "✓ SKILL.md 包含 description"
  else
    echo "✗ SKILL.md 缺少 description"
    errors=$((errors + 1))
  fi
fi

echo ""
if [ "$errors" -eq 0 ]; then
  echo "验证通过 ✓"
  exit 0
else
  echo "发现 $errors 个问题，请修复。"
  exit 1
fi
