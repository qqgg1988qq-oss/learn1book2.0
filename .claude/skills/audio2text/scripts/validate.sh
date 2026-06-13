#!/bin/bash
# Audio2Text Skill 验证脚本

set -e

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
ERRORS=0

echo "=== Audio2Text Skill 验证 ==="
echo ""

# 检查 SKILL.md
if [ -f "$SKILL_DIR/SKILL.md" ]; then
    echo "[✓] SKILL.md 存在"
    # 检查 frontmatter
    if grep -q "^---$" "$SKILL_DIR/SKILL.md" && grep -q "^name:" "$SKILL_DIR/SKILL.md" && grep -q "^description:" "$SKILL_DIR/SKILL.md"; then
        echo "[✓] SKILL.md frontmatter 完整"
    else
        echo "[✗] SKILL.md frontmatter 不完整（需要 name 和 description）"
        ERRORS=$((ERRORS + 1))
    fi
else
    echo "[✗] SKILL.md 不存在"
    ERRORS=$((ERRORS + 1))
fi

# 检查 template.md
if [ -f "$SKILL_DIR/template.md" ]; then
    echo "[✓] template.md 存在"
else
    echo "[!] template.md 不存在（可选）"
fi

# 检查 examples/
if [ -d "$SKILL_DIR/examples" ]; then
    echo "[✓] examples/ 目录存在"
    if [ -f "$SKILL_DIR/examples/sample.md" ]; then
        echo "[✓] examples/sample.md 存在"
    else
        echo "[!] examples/sample.md 不存在（可选）"
    fi
else
    echo "[!] examples/ 目录不存在（可选）"
fi

# 检查 scripts/
if [ -d "$SKILL_DIR/scripts" ]; then
    echo "[✓] scripts/ 目录存在"
    if [ -f "$SKILL_DIR/scripts/validate.sh" ]; then
        echo "[✓] scripts/validate.sh 存在"
        if [ -x "$SKILL_DIR/scripts/validate.sh" ]; then
            echo "[✓] scripts/validate.sh 可执行"
        else
            echo "[!] scripts/validate.sh 不可执行（建议 chmod +x）"
        fi
    fi
else
    echo "[!] scripts/ 目录不存在（可选）"
fi

echo ""
if [ $ERRORS -eq 0 ]; then
    echo "=== 验证通过 ==="
    exit 0
else
    echo "=== 验证失败，发现 $ERRORS 个错误 ==="
    exit 1
fi
