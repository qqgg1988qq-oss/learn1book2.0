#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
SKILL_FILE="$SKILL_DIR/SKILL.md"
AGENTS_DIR="$SKILL_DIR/agents"
CONFIGS_DIR="$SKILL_DIR/configs"

errors=0

check_file() {
  if [[ -f "$1" ]]; then
    echo "  ✓ $1"
  else
    echo "  ✗ $1 (missing)"
    ((errors+=1))
  fi
}

check_dir() {
  if [[ -d "$1" ]]; then
    echo "  ✓ $1/"
  else
    echo "  ✗ $1/ (missing)"
    ((errors+=1))
  fi
}

echo "Validating Council of High Intelligence skill..."
echo "Skill directory: $SKILL_DIR"
echo

echo "Checking required files:"
check_file "$SKILL_FILE"

echo
echo "Checking SKILL.md frontmatter:"
if grep -qE '^---\s*$' "$SKILL_FILE" 2>/dev/null && \
   grep -qE '^name:\s+' "$SKILL_FILE" 2>/dev/null && \
   grep -qE '^description:\s+' "$SKILL_FILE" 2>/dev/null; then
  echo "  ✓ Frontmatter contains name and description"
else
  echo "  ✗ Frontmatter missing or incomplete"
  ((errors+=1))
fi

echo
echo "Checking agents directory:"
check_dir "$AGENTS_DIR"
agent_count=$(find "$AGENTS_DIR" -maxdepth 1 -name 'council-*.md' -type f 2>/dev/null | wc -l | tr -d ' ')
if [[ "$agent_count" -eq 18 ]]; then
  echo "  ✓ Found $agent_count council agents"
else
  echo "  ✗ Expected 18 council agents, found $agent_count"
  ((errors+=1))
fi

echo
echo "Checking scripts directory:"
check_file "$SKILL_DIR/scripts/detect-providers.sh"
check_file "$SKILL_DIR/scripts/council-simulation-checklist.sh"

echo
echo "Checking configs directory:"
check_dir "$CONFIGS_DIR"

echo
if [[ "$errors" -eq 0 ]]; then
  echo "Validation passed. Skill is ready to use."
  exit 0
else
  echo "Validation failed with $errors error(s)."
  exit 1
fi
