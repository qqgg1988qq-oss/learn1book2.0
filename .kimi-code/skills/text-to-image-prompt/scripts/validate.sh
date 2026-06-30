#!/bin/bash
set -e

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKILL_NAME="text-to-image-prompt"
ERRORS=0

echo "=== Validating skill: $SKILL_NAME ==="
echo ""

# Check SKILL.md exists
if [ ! -f "$SKILL_DIR/SKILL.md" ]; then
    echo "[FAIL] SKILL.md not found"
    ERRORS=$((ERRORS + 1))
else
    echo "[PASS] SKILL.md exists"
fi

# Check frontmatter
if [ -f "$SKILL_DIR/SKILL.md" ]; then
    if head -5 "$SKILL_DIR/SKILL.md" | grep -q "^---"; then
        echo "[PASS] Frontmatter delimiter found"
    else
        echo "[FAIL] Frontmatter delimiter (---) not found"
        ERRORS=$((ERRORS + 1))
    fi

    if grep -q "^name:" "$SKILL_DIR/SKILL.md"; then
        echo "[PASS] 'name' field found in frontmatter"
    else
        echo "[FAIL] 'name' field missing in frontmatter"
        ERRORS=$((ERRORS + 1))
    fi

    if grep -q "^description:" "$SKILL_DIR/SKILL.md"; then
        echo "[PASS] 'description' field found in frontmatter"
    else
        echo "[FAIL] 'description' field missing in frontmatter"
        ERRORS=$((ERRORS + 1))
    fi
fi

# Check template.md
if [ ! -f "$SKILL_DIR/template.md" ]; then
    echo "[WARN] template.md not found (optional)"
else
    echo "[PASS] template.md exists"
fi

# Check examples directory
if [ ! -d "$SKILL_DIR/examples" ]; then
    echo "[WARN] examples/ directory not found (optional)"
else
    echo "[PASS] examples/ directory exists"
    if [ -f "$SKILL_DIR/examples/sample.md" ]; then
        echo "[PASS] examples/sample.md exists"
    else
        echo "[WARN] examples/sample.md not found"
    fi
fi

# Check scripts directory
if [ ! -d "$SKILL_DIR/scripts" ]; then
    echo "[WARN] scripts/ directory not found (optional)"
else
    echo "[PASS] scripts/ directory exists"
fi

echo ""
if [ $ERRORS -eq 0 ]; then
    echo "=== Validation PASSED ==="
    exit 0
else
    echo "=== Validation FAILED with $ERRORS error(s) ==="
    exit 1
fi
