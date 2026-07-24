#!/bin/bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKILL_NAME="article-claims-extractor"

echo "验证 Skill: $SKILL_NAME"
echo "路径: $SKILL_DIR"
echo ""

errors=0

# 检查 SKILL.md
if [[ -f "$SKILL_DIR/SKILL.md" ]]; then
    echo "[✓] SKILL.md 存在"
    if grep -qE "^name:\s*$SKILL_NAME" "$SKILL_DIR/SKILL.md"; then
        echo "[✓] SKILL.md frontmatter 名称正确"
    else
        echo "[✗] SKILL.md 中 name 字段不正确"
        errors=$((errors + 1))
    fi
    if grep -qE "^description:\s*\|" "$SKILL_DIR/SKILL.md"; then
        echo "[✓] SKILL.md 包含 description"
    else
        echo "[✗] SKILL.md 缺少 description"
        errors=$((errors + 1))
    fi
else
    echo "[✗] SKILL.md 不存在"
    errors=$((errors + 1))
fi

# 检查 template.md
if [[ -f "$SKILL_DIR/template.md" ]]; then
    echo "[✓] template.md 存在"
else
    echo "[✗] template.md 不存在"
    errors=$((errors + 1))
fi

# 检查 examples/sample.md
if [[ -f "$SKILL_DIR/examples/sample.md" ]]; then
    echo "[✓] examples/sample.md 存在"
else
    echo "[✗] examples/sample.md 不存在"
    errors=$((errors + 1))
fi

# 检查 scripts/validate.sh
if [[ -x "$SKILL_DIR/scripts/validate.sh" ]]; then
    echo "[✓] scripts/validate.sh 存在且可执行"
else
    echo "[✗] scripts/validate.sh 不存在或不可执行"
    errors=$((errors + 1))
fi

echo ""
if [[ $errors -eq 0 ]]; then
    echo "验证通过 ✓"
    exit 0
else
    echo "验证失败，发现 $errors 个问题"
    exit 1
fi
