#!/bin/bash

# content-to-script Skill 验证脚本

set -e

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
ERRORS=0

echo "🔍 验证 content-to-script Skill..."
echo "   目录: $SKILL_DIR"
echo ""

# 检查 SKILL.md
echo "📄 检查 SKILL.md..."
if [ -f "$SKILL_DIR/SKILL.md" ]; then
    echo "   ✓ SKILL.md 存在"
    # 检查 frontmatter
    if head -1 "$SKILL_DIR/SKILL.md" | grep -q "^---"; then
        echo "   ✓ Frontmatter 存在"
    else
        echo "   ✗ Frontmatter 缺失（第一行应为 ---）"
        ERRORS=$((ERRORS + 1))
    fi
    # 检查 name 字段
    if grep -q "^name:" "$SKILL_DIR/SKILL.md"; then
        echo "   ✓ name 字段存在"
    else
        echo "   ✗ name 字段缺失"
        ERRORS=$((ERRORS + 1))
    fi
    # 检查 description 字段
    if grep -q "^description:" "$SKILL_DIR/SKILL.md"; then
        echo "   ✓ description 字段存在"
    else
        echo "   ✗ description 字段缺失"
        ERRORS=$((ERRORS + 1))
    fi
else
    echo "   ✗ SKILL.md 不存在"
    ERRORS=$((ERRORS + 1))
fi

echo ""

# 检查 template.md
echo "📄 检查 template.md..."
if [ -f "$SKILL_DIR/template.md" ]; then
    echo "   ✓ template.md 存在"
    # 检查关键章节
    if grep -q "角色设定" "$SKILL_DIR/template.md"; then
        echo "   ✓ 角色设定部分存在"
    else
        echo "   ✗ 角色设定部分缺失"
        ERRORS=$((ERRORS + 1))
    fi
    if grep -q "输出格式" "$SKILL_DIR/template.md"; then
        echo "   ✓ 输出格式部分存在"
    else
        echo "   ✗ 输出格式部分缺失"
        ERRORS=$((ERRORS + 1))
    fi
    if grep -q "待转化内容" "$SKILL_DIR/template.md"; then
        echo "   ✓ 待转化内容占位符存在"
    else
        echo "   ✗ 待转化内容占位符缺失"
        ERRORS=$((ERRORS + 1))
    fi
else
    echo "   ✗ template.md 不存在"
    ERRORS=$((ERRORS + 1))
fi

echo ""

# 检查 examples
echo "📄 检查 examples/sample.md..."
if [ -f "$SKILL_DIR/examples/sample.md" ]; then
    echo "   ✓ examples/sample.md 存在"
    # 检查是否包含输入输出示例
    if grep -q "输入" "$SKILL_DIR/examples/sample.md" && grep -q "输出" "$SKILL_DIR/examples/sample.md"; then
        echo "   ✓ 包含输入输出示例"
    else
        echo "   ✗ 缺少输入或输出示例标记"
        ERRORS=$((ERRORS + 1))
    fi
else
    echo "   ✗ examples/sample.md 不存在"
    ERRORS=$((ERRORS + 1))
fi

echo ""

# 检查目录结构
echo "📁 检查目录结构..."
if [ -d "$SKILL_DIR/examples" ]; then
    echo "   ✓ examples/ 目录存在"
else
    echo "   ✗ examples/ 目录缺失"
    ERRORS=$((ERRORS + 1))
fi
if [ -d "$SKILL_DIR/scripts" ]; then
    echo "   ✓ scripts/ 目录存在"
else
    echo "   ✗ scripts/ 目录缺失"
    ERRORS=$((ERRORS + 1))
fi

echo ""

# 总结
echo "========================================"
if [ $ERRORS -eq 0 ]; then
    echo "✅ 验证通过！content-to-script Skill 结构完整。"
    echo ""
    echo "使用方式:"
    echo "   /content-to-script <精读报告文件路径>"
    echo ""
    echo "或直接粘贴精读报告内容并说'转成口播文案'"
    exit 0
else
    echo "❌ 验证失败，发现 $ERRORS 个问题。"
    exit 1
fi
