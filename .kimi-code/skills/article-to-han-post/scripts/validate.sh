#!/bin/bash
# Article to Han Post Skill — 结构验证脚本
set -e

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKILL_NAME="$(basename "$SKILL_DIR")"
ERRORS=0

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

check() {
    local desc="$1"
    local condition="$2"
    if eval "$condition"; then
        echo -e "  ${GREEN}✓${NC} $desc"
    else
        echo -e "  ${RED}✗${NC} $desc"
        ERRORS=$((ERRORS + 1))
    fi
}

echo "============================================"
echo "  Article to Han Post — Skill 验证"
echo "  路径: $SKILL_DIR"
echo "============================================"
echo ""

echo "📁 文件结构"
check "SKILL.md 存在" '[ -f "$SKILL_DIR/SKILL.md" ]'
check "template.md 存在" '[ -f "$SKILL_DIR/template.md" ]'
check "examples/ 目录存在" '[ -d "$SKILL_DIR/examples" ]'
check "examples/sample.md 存在" '[ -f "$SKILL_DIR/examples/sample.md" ]'
check "scripts/ 目录存在" '[ -d "$SKILL_DIR/scripts" ]'
echo ""

echo "📝 SKILL.md 内容"
check "YAML frontmatter" 'head -1 "$SKILL_DIR/SKILL.md" | grep -q "^---$"'
check "name: article-to-han-post" 'grep -q "^name: article-to-han-post" "$SKILL_DIR/SKILL.md"'
check "description 字段" 'grep -q "^description:" "$SKILL_DIR/SKILL.md"'
check "包含 Stage 1: article-viral-hook" 'grep -q "article-viral-hook" "$SKILL_DIR/SKILL.md"'
check "包含 Stage 2: han-han-perspective" 'grep -q "han-han-perspective" "$SKILL_DIR/SKILL.md"'
check "包含 Stage 3: text-humanizer-zh" 'grep -q "text-humanizer-zh" "$SKILL_DIR/SKILL.md"'
check "包含韩寒风格约束" 'grep -q "不使用韩寒.*个人经历\|不使用韩寒.*真实经历\|不用韩寒本人经历" "$SKILL_DIR/SKILL.md"'
check "包含输出位置规则" 'grep -q "源文件同目录\|同目录" "$SKILL_DIR/SKILL.md"'
check "包含质量自检清单" 'grep -q "自检清单" "$SKILL_DIR/SKILL.md"'
check "包含完整执行流程" 'grep -q "Step [0-4]" "$SKILL_DIR/SKILL.md"'
echo ""

echo "📋 template.md 内容"
check "包含三阶段工作区" 'grep -q "Stage [1-3]" "$SKILL_DIR/template.md"'
check "包含 placeholder" 'grep -q "{{.*}}" "$SKILL_DIR/template.md"'
check "包含韩寒改写检查清单" 'grep -q "韩寒.*检查\|韩寒.*改写\|大白话" "$SKILL_DIR/template.md"'
echo ""

echo "📖 examples/sample.md"
check "包含三阶段示例" 'grep -q "Stage [1-3]" "$SKILL_DIR/examples/sample.md"'
check "包含正确/错误用法对比" 'grep -q "❌\|✅\|错误\|正确" "$SKILL_DIR/examples/sample.md"'
check "包含韩寒经历约束示例" 'grep -q "三重门\|赛车\|韩寒.*经历" "$SKILL_DIR/examples/sample.md"'
echo ""

echo "============================================"
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✅ 验证通过 — 0 错误${NC}"
    exit 0
else
    echo -e "${RED}❌ 验证失败 — $ERRORS 错误${NC}"
    exit 1
fi
echo "============================================"
