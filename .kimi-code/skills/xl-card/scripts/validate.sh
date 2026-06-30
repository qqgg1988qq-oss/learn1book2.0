#!/bin/bash
# xl-card Skill 结构验证脚本
set -e

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PASS=0
FAIL=0

check() {
    local desc="$1"; shift
    if "$@"; then
        echo "  ✅ $desc"
        PASS=$((PASS + 1))
    else
        echo "  ❌ $desc"
        FAIL=$((FAIL + 1))
    fi
}

echo "🔍 验证 xl-card Skill 结构"
echo "   路径: $SKILL_DIR"
echo ""

# SKILL.md
check "SKILL.md 存在"             test -f "$SKILL_DIR/SKILL.md"
check "SKILL.md 有 frontmatter"   head -1 "$SKILL_DIR/SKILL.md" | grep -q "^---$" 2>/dev/null
check "SKILL.md 有 name 字段"     grep -q "name:" "$SKILL_DIR/SKILL.md" 2>/dev/null
check "SKILL.md 有 description"   grep -q "description:" "$SKILL_DIR/SKILL.md" 2>/dev/null

# template.md
check "template.md 存在"          test -f "$SKILL_DIR/template.md"

# examples/
check "examples/ 目录存在"        test -d "$SKILL_DIR/examples"
check "examples/sample.md 存在"   test -f "$SKILL_DIR/examples/sample.md"

# scripts/
check "scripts/ 目录存在"         test -d "$SKILL_DIR/scripts"
check "scripts/validate.sh 存在"  test -f "$SKILL_DIR/scripts/validate.sh"

# references/
check "references/ 目录存在"      test -d "$SKILL_DIR/references"
check "references/taste.md 存在"  test -f "$SKILL_DIR/references/taste.md"
check "references/mode-long.md"   test -f "$SKILL_DIR/references/mode-long.md"
check "references/mode-concept.md" test -f "$SKILL_DIR/references/mode-concept.md"
check "references/mode-quote.md"  test -f "$SKILL_DIR/references/mode-quote.md"

echo ""
echo "──────────────────────────────────────"
echo " 通过: $PASS  失败: $FAIL"
echo "──────────────────────────────────────"

[ "$FAIL" -eq 0 ] && echo "✅ 验证通过" || echo "❌ 验证失败"
exit $FAIL
