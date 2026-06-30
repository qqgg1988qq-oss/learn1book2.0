#!/usr/bin/env bash
# Deep Reader Skill 验证脚本

set -e

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ERRORS=0

echo "=== Deep Reader Skill 验证 ==="
echo ""

check_file() {
    local file="$1"
    local desc="$2"
    if [ -f "$SKILL_DIR/$file" ]; then
        echo "[OK] $desc: $file"
    else
        echo "[MISSING] $desc: $file"
        ((ERRORS++))
    fi
}

check_frontmatter() {
    if [ -f "$SKILL_DIR/SKILL.md" ]; then
        if grep -q "^---$" "$SKILL_DIR/SKILL.md"; then
            echo "[OK] SKILL.md 包含 frontmatter"
        else
            echo "[WARN] SKILL.md 可能缺少 frontmatter"
        fi

        for field in "name:" "description:"; do
            if grep -q "^$field" "$SKILL_DIR/SKILL.md"; then
                echo "[OK] SKILL.md 包含 $field 字段"
            else
                echo "[MISSING] SKILL.md 缺少 $field 字段"
                ((ERRORS++))
            fi
        done
    fi
}

echo "1. 检查必需文件..."
check_file "SKILL.md" "核心说明"
check_file "template.md" "分析模板"

echo ""
echo "2. 检查可选文件..."
check_file "examples/sample.md" "使用示例"

echo ""
echo "3. 检查 SKILL.md 格式..."
check_frontmatter

echo ""
echo "=== 验证结果 ==="
if [ $ERRORS -eq 0 ]; then
    echo "全部通过！Skill 结构完整。"
    exit 0
else
    echo "发现 $ERRORS 个问题。"
    exit 1
fi
