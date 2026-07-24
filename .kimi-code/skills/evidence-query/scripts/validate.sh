#!/bin/bash
set -e

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "验证 evidence-query Skill 结构..."
echo ""

# 检查必需文件
for f in "SKILL.md" "template.md"; do
    if [ -f "$SKILL_DIR/$f" ]; then
        echo "✓ $f 存在"
    else
        echo "✗ $f 缺失"
        exit 1
    fi
done

# 检查目录结构
for d in "examples" "scripts"; do
    if [ -d "$SKILL_DIR/$d" ]; then
        echo "✓ $d/ 目录存在"
    else
        echo "✗ $d/ 目录缺失"
        exit 1
    fi
done

# 检查 SKILL.md frontmatter
if head -n 1 "$SKILL_DIR/SKILL.md" | grep -q '^---$'; then
    echo "✓ SKILL.md 包含 YAML frontmatter 开始标记"
else
    echo "✗ SKILL.md 缺少 YAML frontmatter 开始标记"
    exit 1
fi

if grep -q '^name: evidence-query$' "$SKILL_DIR/SKILL.md"; then
    echo "✓ SKILL.md name 字段正确"
else
    echo "✗ SKILL.md name 字段缺失或错误"
    exit 1
fi

if grep -q '^description:' "$SKILL_DIR/SKILL.md"; then
    echo "✓ SKILL.md description 字段存在"
else
    echo "✗ SKILL.md description 字段缺失"
    exit 1
fi

# 检查脚本文件
for f in "scripts/validate.sh" "scripts/evidence_query.py"; do
    if [ -f "$SKILL_DIR/$f" ]; then
        echo "✓ $f 存在"
    else
        echo "✗ $f 缺失"
        exit 1
    fi
done

# 检查示例文件
if [ -f "$SKILL_DIR/examples/sample.md" ]; then
    echo "✓ examples/sample.md 存在"
else
    echo "✗ examples/sample.md 缺失"
    exit 1
fi

echo ""
echo "验证通过。"
