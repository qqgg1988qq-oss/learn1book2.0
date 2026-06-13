#!/bin/bash
# article-to-richpost Skill 结构验证脚本

set -e

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
ERRORS=0

echo "🔍 验证 article-to-richpost Skill 结构..."
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
for dir in "examples" "scripts" "references"; do
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
fi

# 检查参考文件
for ref in "references/platform-specs.md" "references/style-presets.md"; do
    if [ -f "$SKILL_DIR/$ref" ]; then
        echo "✅ $ref"
    else
        echo "⚠️  $ref — 参考文件不存在（可选）"
    fi
done

echo ""
if [ $ERRORS -eq 0 ]; then
    echo "🎉 验证通过！Skill 结构完整。"
    exit 0
else
    echo "⚠️  发现 $ERRORS 个问题，请修复后重试。"
    exit 1
fi
