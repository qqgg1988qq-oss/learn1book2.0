#!/bin/bash
# broadcast-maker Skill 结构验证脚本

set -e

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
ERRORS=0

echo "=== broadcast-maker Skill 验证 ==="
echo ""

# 检查 SKILL.md
if [ -f "$SKILL_DIR/SKILL.md" ]; then
    echo "✅ SKILL.md 存在"

    # 检查 frontmatter
    if grep -q "^---" "$SKILL_DIR/SKILL.md"; then
        echo "✅ Frontmatter 存在"
    else
        echo "❌ Frontmatter 缺失"
        ERRORS=$((ERRORS + 1))
    fi

    # 检查 name 字段
    if grep -q "^name:" "$SKILL_DIR/SKILL.md"; then
        echo "✅ name 字段存在"
    else
        echo "❌ name 字段缺失"
        ERRORS=$((ERRORS + 1))
    fi

    # 检查 description 字段
    if grep -q "^description:" "$SKILL_DIR/SKILL.md"; then
        echo "✅ description 字段存在"
    else
        echo "❌ description 字段缺失"
        ERRORS=$((ERRORS + 1))
    fi
else
    echo "❌ SKILL.md 不存在"
    ERRORS=$((ERRORS + 1))
fi

# 检查 template.md
if [ -f "$SKILL_DIR/template.md" ]; then
    echo "✅ template.md 存在"
else
    echo "⚠️ template.md 不存在（可选但推荐）"
fi

# 检查 examples/
if [ -d "$SKILL_DIR/examples" ]; then
    echo "✅ examples/ 目录存在"
    if [ -f "$SKILL_DIR/examples/sample.md" ]; then
        echo "✅ examples/sample.md 存在"
    else
        echo "⚠️ examples/sample.md 不存在"
    fi
else
    echo "⚠️ examples/ 目录不存在"
fi

# 检查 scripts/
if [ -d "$SKILL_DIR/scripts" ]; then
    echo "✅ scripts/ 目录存在"
    if [ -f "$SKILL_DIR/scripts/validate.sh" ]; then
        echo "✅ scripts/validate.sh 存在"
    else
        echo "⚠️ scripts/validate.sh 不存在"
    fi
else
    echo "⚠️ scripts/ 目录不存在"
fi

# 检查输出目录
OUTPUT_DIR="/Users/chouchou/Documents/Obsidian Vault/成长计划/博客"
if [ -d "$OUTPUT_DIR" ]; then
    echo "✅ 输出目录存在: $OUTPUT_DIR"
else
    echo "⚠️ 输出目录不存在，首次运行时会自动创建: $OUTPUT_DIR"
fi

echo ""
if [ $ERRORS -eq 0 ]; then
    echo "=== 验证通过 ✅ ==="
    exit 0
else
    echo "=== 验证失败 ❌ ($ERRORS 个错误) ==="
    exit 1
fi
