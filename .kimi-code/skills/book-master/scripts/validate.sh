#!/usr/bin/env bash
set -e
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ERRORS=0
check_file() {
    if [ -f "$SKILL_DIR/$1" ]; then echo "[OK] $2"; else echo "[MISSING] $2"; ((ERRORS++)); fi
}
check_file "SKILL.md" "核心说明"
check_file "template.md" "工作流模板"
check_file "scripts/filter.sh" "过滤脚本"
if [ $ERRORS -eq 0 ]; then echo "全部通过！"; exit 0; else echo "发现 $ERRORS 个问题"; exit 1; fi
