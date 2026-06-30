#!/bin/bash
set -e

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKILL_NAME="$(basename "$SKILL_DIR")"

echo "验证 Skill: $SKILL_NAME"
echo "路径: $SKILL_DIR"
echo ""

errors=0

# 检查 SKILL.md
if [ ! -f "$SKILL_DIR/SKILL.md" ]; then
  echo "❌ 缺少 SKILL.md"
  errors=$((errors + 1))
else
  echo "✅ SKILL.md 存在"
  # 检查 frontmatter
  if grep -q "^---" "$SKILL_DIR/SKILL.md"; then
    echo "✅ SKILL.md 包含 frontmatter 分隔符"
  else
    echo "❌ SKILL.md 缺少 frontmatter 分隔符"
    errors=$((errors + 1))
  fi
  if grep -q "^name:" "$SKILL_DIR/SKILL.md"; then
    echo "✅ SKILL.md 包含 name 字段"
  else
    echo "❌ SKILL.md 缺少 name 字段"
    errors=$((errors + 1))
  fi
  if grep -q "^description:" "$SKILL_DIR/SKILL.md"; then
    echo "✅ SKILL.md 包含 description 字段"
  else
    echo "❌ SKILL.md 缺少 description 字段"
    errors=$((errors + 1))
  fi
fi

# 检查 template.md
if [ ! -f "$SKILL_DIR/template.md" ]; then
  echo "❌ 缺少 template.md"
  errors=$((errors + 1))
else
  echo "✅ template.md 存在"
fi

# 检查 examples/sample.md
if [ ! -f "$SKILL_DIR/examples/sample.md" ]; then
  echo "❌ 缺少 examples/sample.md"
  errors=$((errors + 1))
else
  echo "✅ examples/sample.md 存在"
fi

# 检查 scripts/validate.sh
if [ ! -x "$SKILL_DIR/scripts/validate.sh" ]; then
  echo "⚠️  scripts/validate.sh 不存在或不可执行"
else
  echo "✅ scripts/validate.sh 存在且可执行"
fi

echo ""
if [ "$errors" -eq 0 ]; then
  echo "🎉 Skill 结构验证通过"
  exit 0
else
  echo "❌ 发现 $errors 个问题"
  exit 1
fi
