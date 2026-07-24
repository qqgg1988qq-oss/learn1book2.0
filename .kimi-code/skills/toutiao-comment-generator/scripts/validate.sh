#!/usr/bin/env bash
# 验证 toutiao-comment-generator Skill 结构完整性

set -e

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKILL_NAME="toutiao-comment-generator"
PAINS_FILE="/Users/chouchou/Documents/Obsidian Vault/九局下半怎么破局/参考资料/40岁中年危机痛点图谱_完整报告.md"

echo "🔍 验证 Skill: $SKILL_NAME"
echo "📁 路径: $SKILL_DIR"
echo ""

# 检查必需文件
required_files=(
    "SKILL.md"
    "template.md"
    "examples/sample.md"
    "scripts/validate.sh"
)

for file in "${required_files[@]}"; do
    if [[ -f "$SKILL_DIR/$file" ]]; then
        echo "✅ $file 存在"
    else
        echo "❌ $file 缺失"
        exit 1
    fi
done

# 检查 SKILL.md 是否包含 frontmatter
if head -n 1 "$SKILL_DIR/SKILL.md" | grep -q '^---$'; then
    echo "✅ SKILL.md 包含 YAML frontmatter 起始标记"
else
    echo "❌ SKILL.md 缺少 YAML frontmatter 起始标记"
    exit 1
fi

# 检查 frontmatter 中是否包含 name 和 description
if grep -q '^name:' "$SKILL_DIR/SKILL.md"; then
    echo "✅ frontmatter 包含 name"
else
    echo "❌ frontmatter 缺少 name"
    exit 1
fi

if grep -q '^description:' "$SKILL_DIR/SKILL.md"; then
    echo "✅ frontmatter 包含 description"
else
    echo "❌ frontmatter 缺少 description"
    exit 1
fi

# 检查痛点图谱文件是否存在（运行时依赖）
if [[ -f "$PAINS_FILE" ]]; then
    echo "✅ 痛点图谱文件可访问: $PAINS_FILE"
else
    echo "⚠️  痛点图谱文件不存在或路径不可访问: $PAINS_FILE"
    echo "   运行时可能无法完成痛点匹配，请检查路径。"
fi

echo ""
echo "🎉 Skill 结构验证通过"
