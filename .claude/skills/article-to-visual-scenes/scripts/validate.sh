#!/usr/bin/env bash
# Skill validation script for article-to-visual-scenes

set -e

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKILL_NAME="article-to-visual-scenes"
ERRORS=0

echo "==> Validating skill: $SKILL_NAME"
echo "    Directory: $SKILL_DIR"
echo ""

check_file() {
  local path="$1"
  local desc="$2"
  if [[ -f "$path" ]]; then
    echo "  [OK] $desc"
  else
    echo "  [MISSING] $desc -> $path"
    ERRORS=$((ERRORS + 1))
  fi
}

check_dir() {
  local path="$1"
  local desc="$2"
  if [[ -d "$path" ]]; then
    echo "  [OK] $desc"
  else
    echo "  [MISSING] $desc -> $path"
    ERRORS=$((ERRORS + 1))
  fi
}

echo "Structure check:"
check_file "$SKILL_DIR/SKILL.md" "SKILL.md"
check_file "$SKILL_DIR/template.md" "template.md"
check_dir  "$SKILL_DIR/examples" "examples/"
check_file "$SKILL_DIR/examples/sample.md" "examples/sample.md"
check_dir  "$SKILL_DIR/references" "references/"
check_file "$SKILL_DIR/references/json-schema.md" "references/json-schema.md"
check_file "$SKILL_DIR/references/style-presets.md" "references/style-presets.md"
check_file "$SKILL_DIR/references/example-output.json" "references/example-output.json"
check_dir  "$SKILL_DIR/scripts" "scripts/"
echo ""

echo "Frontmatter check:"
if head -n 1 "$SKILL_DIR/SKILL.md" | grep -q '^---$'; then
  echo "  [OK] SKILL.md has frontmatter delimiter"
else
  echo "  [MISSING] SKILL.md frontmatter delimiter"
  ERRORS=$((ERRORS + 1))
fi

if grep -q '^name: article-to-visual-scenes' "$SKILL_DIR/SKILL.md"; then
  echo "  [OK] name field present"
else
  echo "  [MISSING] name field"
  ERRORS=$((ERRORS + 1))
fi

if grep -q '^description:' "$SKILL_DIR/SKILL.md"; then
  echo "  [OK] description field present"
else
  echo "  [MISSING] description field"
  ERRORS=$((ERRORS + 1))
fi
echo ""

echo "JSON example validity check:"
if command -v python3 >/dev/null 2>&1; then
  if python3 -c "import json,sys; json.load(open('$SKILL_DIR/references/example-output.json'))" 2>/dev/null; then
    echo "  [OK] example-output.json is valid JSON"
  else
    echo "  [ERROR] example-output.json is NOT valid JSON"
    ERRORS=$((ERRORS + 1))
  fi
else
  echo "  [SKIP] python3 not found, skipping JSON validation"
fi
echo ""

if [[ $ERRORS -eq 0 ]]; then
  echo "Validation PASSED. Skill is ready to use."
  exit 0
else
  echo "Validation FAILED with $ERRORS error(s)."
  exit 1
fi
