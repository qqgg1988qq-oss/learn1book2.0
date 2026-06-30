#!/bin/bash
# Hot Pain Match Skill — 结构验证脚本
set -e

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKILL_NAME="$(basename "$SKILL_DIR")"
ERRORS=0

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
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

warn() {
    echo -e "  ${YELLOW}⚠${NC} $1"
}

echo "============================================"
echo "  Hot Pain Match — Skill 验证"
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
check "name: hot-pain-match" 'grep -q "^name: hot-pain-match" "$SKILL_DIR/SKILL.md"'
check "description 字段" 'grep -q "^description:" "$SKILL_DIR/SKILL.md"'
check "包含 tophub-trends 引用" 'grep -q "tophub-trends" "$SKILL_DIR/SKILL.md"'
check "包含痛点图谱路径" 'grep -q "40岁中年危机痛点图谱" "$SKILL_DIR/SKILL.md"'
check "包含 20 个痛点速查" 'grep -q "35岁就业年龄歧视\|年龄歧视" "$SKILL_DIR/SKILL.md"'
check "包含匹配算法" 'grep -q "创作价值分\|匹配算法\|匹配度" "$SKILL_DIR/SKILL.md"'
check "包含 Step 1-3 工作流" 'grep -q "Step [1-3]" "$SKILL_DIR/SKILL.md"'
check "包含匹配精度等级" 'grep -q "⭐⭐⭐\|匹配精度" "$SKILL_DIR/SKILL.md"'
check "包含输出结构" 'grep -q "🥇\|🥈\|🥉" "$SKILL_DIR/SKILL.md"'
check "包含质量自检清单" 'grep -q "自检清单" "$SKILL_DIR/SKILL.md"'
check "包含注意事项" 'grep -q "娱乐八卦过滤\|政治敏感" "$SKILL_DIR/SKILL.md"'
echo ""

echo "📋 template.md 内容"
check "包含模板变量" 'grep -q "{{.*}}" "$SKILL_DIR/template.md"'
check "包含匹配计算工作表" 'grep -q "匹配计算\|创作价值分" "$SKILL_DIR/template.md"'
check "包含内容切入点模板" 'grep -q "APAG\|切入点" "$SKILL_DIR/template.md"'
check "包含 API 调用示例" 'grep -q "curl.*tophubdata\|curl.*Authorization" "$SKILL_DIR/template.md"'
echo ""

echo "📖 examples/sample.md"
check "包含使用示例" 'grep -q "示例 [1-9]" "$SKILL_DIR/examples/sample.md"'
check "包含匹配计算过程" 'grep -q "匹配度\|创作价值分" "$SKILL_DIR/examples/sample.md"'
check "包含输出样例" 'grep -q "🔥.*痛点匹配报告\|今日最佳借势" "$SKILL_DIR/examples/sample.md"'
check "包含内容建议" 'grep -q "内容方向\|创作建议\|切入点" "$SKILL_DIR/examples/sample.md"'
echo ""

echo "🔗 依赖检查"
check "tophub-trends skill 存在" '[ -d "$HOME/.claude/skills/tophub-trends" ]'
check "tophub-trends config.env 存在" '[ -f "$HOME/.claude/skills/tophub-trends/scripts/config.env" ]'

PAIN_REPORT="/Users/chouchou/Documents/Obsidian Vault/九局下半怎么破局/参考资料/40岁中年危机痛点图谱_完整报告.md"
if [ -f "$PAIN_REPORT" ]; then
    echo -e "  ${GREEN}✓${NC} 痛点图谱存在: $PAIN_REPORT"
else
    warn "痛点图谱文件不存在: $PAIN_REPORT"
fi
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
