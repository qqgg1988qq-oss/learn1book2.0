#!/bin/bash
# Book Reader Skill 验证脚本

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
ERRORS=0

echo "🔍 Validating book-reader skill..."
echo ""

# 检查 SKILL.md
if [ ! -f "$SKILL_DIR/SKILL.md" ]; then
  echo "❌ Missing SKILL.md"
  ERRORS=$((ERRORS + 1))
else
  echo "✅ SKILL.md exists"
fi

# 检查 frontmatter
if grep -q "^---$" "$SKILL_DIR/SKILL.md" 2>/dev/null; then
  echo "✅ Frontmatter present"
else
  echo "❌ Missing YAML frontmatter in SKILL.md"
  ERRORS=$((ERRORS + 1))
fi

# 检查 name
if grep -q "^name:" "$SKILL_DIR/SKILL.md" 2>/dev/null; then
  echo "✅ Name field present"
else
  echo "❌ Missing 'name' in frontmatter"
  ERRORS=$((ERRORS + 1))
fi

# 检查 description
if grep -q "^description:" "$SKILL_DIR/SKILL.md" 2>/dev/null; then
  echo "✅ Description field present"
else
  echo "❌ Missing 'description' in frontmatter"
  ERRORS=$((ERRORS + 1))
fi

# 检查 template.md
if [ ! -f "$SKILL_DIR/template.md" ]; then
  echo "❌ Missing template.md"
  ERRORS=$((ERRORS + 1))
else
  echo "✅ template.md exists"
fi

# 检查 examples
if [ ! -d "$SKILL_DIR/examples" ]; then
  echo "❌ Missing examples/ directory"
  ERRORS=$((ERRORS + 1))
else
  echo "✅ examples/ directory exists"
fi

# 检查 scripts
if [ ! -d "$SKILL_DIR/scripts" ]; then
  echo "❌ Missing scripts/ directory"
  ERRORS=$((ERRORS + 1))
else
  echo "✅ scripts/ directory exists"
fi

echo ""
if [ $ERRORS -eq 0 ]; then
  echo "✅ All checks passed! Skill is valid."
  exit 0
else
  echo "❌ $ERRORS error(s) found."
  exit 1
fi
