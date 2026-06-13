#!/bin/bash
set -e

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKILL_NAME="narrative-to-script"

echo "=== Validating $SKILL_NAME skill ==="
echo ""

errors=0

# Check SKILL.md exists
if [ ! -f "$SKILL_DIR/SKILL.md" ]; then
    echo "❌ SKILL.md not found"
    errors=$((errors + 1))
else
    echo "✅ SKILL.md exists"
fi

# Check frontmatter
if [ -f "$SKILL_DIR/SKILL.md" ]; then
    if head -1 "$SKILL_DIR/SKILL.md" | grep -q "^---"; then
        echo "✅ Frontmatter present"
    else
        echo "❌ Frontmatter missing (must start with ---)"
        errors=$((errors + 1))
    fi

    if grep -q "^name:" "$SKILL_DIR/SKILL.md"; then
        echo "✅ 'name' field in frontmatter"
    else
        echo "❌ 'name' field missing in frontmatter"
        errors=$((errors + 1))
    fi

    if grep -q "^description:" "$SKILL_DIR/SKILL.md"; then
        echo "✅ 'description' field in frontmatter"
    else
        echo "❌ 'description' field missing in frontmatter"
        errors=$((errors + 1))
    fi
fi

# Check template.md
if [ ! -f "$SKILL_DIR/template.md" ]; then
    echo "❌ template.md not found"
    errors=$((errors + 1))
else
    echo "✅ template.md exists"
fi

# Check examples directory
if [ ! -d "$SKILL_DIR/examples" ]; then
    echo "❌ examples/ directory not found"
    errors=$((errors + 1))
else
    echo "✅ examples/ directory exists"
    if [ -f "$SKILL_DIR/examples/sample.md" ]; then
        echo "✅ examples/sample.md exists"
    else
        echo "⚠️  examples/sample.md not found (optional)"
    fi
fi

# Check scripts directory
if [ ! -d "$SKILL_DIR/scripts" ]; then
    echo "❌ scripts/ directory not found"
    errors=$((errors + 1))
else
    echo "✅ scripts/ directory exists"
fi

echo ""
if [ $errors -eq 0 ]; then
    echo "✅ All checks passed! Skill is valid."
    exit 0
else
    echo "❌ $errors error(s) found. Please fix above issues."
    exit 1
fi
