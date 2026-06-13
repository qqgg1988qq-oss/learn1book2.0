#!/bin/bash
# text-humanizer-zh Skill 结构验证脚本

set -e

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
ERRORS=0

echo "🔍 验证 text-humanizer-zh Skill 结构..."
echo ""

# 检查必需文件
for file in "SKILL.md" "template.md"; do
    if [ -f "$SKILL_DIR/$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file — 文件不存在"
        ERRORS=$((ERRORS + 1))
    fi
done

# 检查目录结构
for dir in "examples" "scripts"; do
    if [ -d "$SKILL_DIR/$dir" ]; then
        echo "✅ $dir/"
    else
        echo "❌ $dir/ — 目录不存在"
        ERRORS=$((ERRORS + 1))
    fi
done

# 检查 SKILL.md frontmatter
if [ -f "$SKILL_DIR/SKILL.md" ]; then
    if head -5 "$SKILL_DIR/SKILL.md" | grep -q "^---"; then
        echo "✅ SKILL.md frontmatter 格式正确"
    else
        echo "⚠️  SKILL.md 缺少 frontmatter（---）"
    fi

    if grep -q "^name:" "$SKILL_DIR/SKILL.md"; then
        echo "✅ frontmatter 包含 name 字段"
    else
        echo "❌ frontmatter 缺少 name 字段"
        ERRORS=$((ERRORS + 1))
    fi

    if grep -q "^description:" "$SKILL_DIR/SKILL.md"; then
        echo "✅ frontmatter 包含 description 字段"
    else
        echo "❌ frontmatter 缺少 description 字段"
        ERRORS=$((ERRORS + 1))
    fi

    # 检查关键章节是否存在
    for section in "内容模式" "语言和语法模式" "风格模式" "交流模式" "质量评分"; do
        if grep -q "$section" "$SKILL_DIR/SKILL.md"; then
            echo "✅ 章节：$section"
        else
            echo "⚠️  章节缺失：$section"
        fi
    done
fi

echo ""
if [ $ERRORS -eq 0 ]; then
    echo "🎉 验证通过！Skill 结构完整。"
    exit 0
else
    echo "⚠️  发现 $ERRORS 个问题，请修复后重试。"
    exit 1
fi
