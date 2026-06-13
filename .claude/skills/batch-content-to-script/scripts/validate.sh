#!/bin/bash
# batch-content-to-script Skill 结构验证脚本

set -e

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ERRORS=0

echo "========================================"
echo "Validating batch-content-to-script Skill"
echo "========================================"
echo ""

# 检查 SKILL.md
echo "[1/5] Checking SKILL.md..."
if [ ! -f "$SKILL_DIR/SKILL.md" ]; then
    echo "  ❌ SKILL.md not found"
    ERRORS=$((ERRORS + 1))
else
    echo "  ✅ SKILL.md exists"

    # 检查 frontmatter
    if head -5 "$SKILL_DIR/SKILL.md" | grep -q "^---"; then
        echo "  ✅ Frontmatter present"
    else
        echo "  ⚠️  Frontmatter may be missing"
    fi

    # 检查关键字段
    if grep -q "name:" "$SKILL_DIR/SKILL.md"; then
        echo "  ✅ 'name' field found"
    else
        echo "  ❌ 'name' field missing"
        ERRORS=$((ERRORS + 1))
    fi

    if grep -q "description:" "$SKILL_DIR/SKILL.md"; then
        echo "  ✅ 'description' field found"
    else
        echo "  ❌ 'description' field missing"
        ERRORS=$((ERRORS + 1))
    fi
fi
echo ""

# 检查 template.md
echo "[2/5] Checking template.md..."
if [ ! -f "$SKILL_DIR/template.md" ]; then
    echo "  ❌ template.md not found"
    ERRORS=$((ERRORS + 1))
else
    echo "  ✅ template.md exists"
fi
echo ""

# 检查 examples
echo "[3/5] Checking examples/..."
if [ ! -d "$SKILL_DIR/examples" ]; then
    echo "  ❌ examples/ directory not found"
    ERRORS=$((ERRORS + 1))
else
    echo "  ✅ examples/ directory exists"

    if [ -f "$SKILL_DIR/examples/sample.md" ]; then
        echo "  ✅ sample.md exists"
    else
        echo "  ⚠️  sample.md not found (optional but recommended)"
    fi
fi
echo ""

# 检查 scripts
echo "[4/5] Checking scripts/..."
if [ ! -d "$SKILL_DIR/scripts" ]; then
    echo "  ❌ scripts/ directory not found"
    ERRORS=$((ERRORS + 1))
else
    echo "  ✅ scripts/ directory exists"

    if [ -f "$SKILL_DIR/scripts/validate.sh" ]; then
        echo "  ✅ validate.sh exists"
        if [ -x "$SKILL_DIR/scripts/validate.sh" ]; then
            echo "  ✅ validate.sh is executable"
        else
            echo "  ⚠️  validate.sh is not executable (run: chmod +x)"
        fi
    else
        echo "  ⚠️  validate.sh not found"
    fi
fi
echo ""

# 检查依赖 Skill
echo "[5/5] Checking dependency (content-to-script)..."
CONTENT_TO_SCRIPT="$(cd "$SKILL_DIR/../content-to-script" && pwd)"
if [ -d "$CONTENT_TO_SCRIPT" ] && [ -f "$CONTENT_TO_SCRIPT/SKILL.md" ]; then
    echo "  ✅ content-to-script skill found"
    echo "      Location: $CONTENT_TO_SCRIPT"
else
    echo "  ❌ content-to-script skill not found!"
    echo "      Expected at: $SKILL_DIR/../content-to-script/"
    echo "      This skill depends on content-to-script."
    ERRORS=$((ERRORS + 1))
fi
echo ""

# 总结
echo "========================================"
if [ $ERRORS -eq 0 ]; then
    echo "✅ All checks passed!"
    exit 0
else
    echo "❌ $ERRORS error(s) found"
    exit 1
fi
