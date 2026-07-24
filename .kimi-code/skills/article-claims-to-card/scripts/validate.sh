#!/bin/bash
set -e

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKILL_NAME="article-claims-to-card"

echo "验证 Skill: $SKILL_NAME"
echo "路径: $SKILL_DIR"
echo ""

errors=0

check_file() {
  if [ -f "$1" ]; then
    echo "✅ $1"
  else
    echo "❌ 缺少文件: $1"
    errors=$((errors + 1))
  fi
}

check_dir() {
  if [ -d "$1" ]; then
    echo "✅ 目录存在: $1"
  else
    echo "❌ 缺少目录: $1"
    errors=$((errors + 1))
  fi
}

check_file "$SKILL_DIR/SKILL.md"
check_file "$SKILL_DIR/template.md"
check_file "$SKILL_DIR/examples/sample.md"
check_file "$SKILL_DIR/scripts/validate.sh"

check_dir "$SKILL_DIR/examples"
check_dir "$SKILL_DIR/scripts"

echo ""
echo "检查 SKILL.md frontmatter..."
if grep -q "^---" "$SKILL_DIR/SKILL.md" && grep -q "^name:" "$SKILL_DIR/SKILL.md" && grep -q "^description:" "$SKILL_DIR/SKILL.md"; then
  echo "✅ SKILL.md 包含 name 和 description frontmatter"
else
  echo "❌ SKILL.md frontmatter 不完整"
  errors=$((errors + 1))
fi

echo ""
if [ $errors -eq 0 ]; then
  echo "🎉 Skill 结构验证通过"
  exit 0
else
  echo "⚠️ 发现 $errors 个问题"
  exit 1
fi
