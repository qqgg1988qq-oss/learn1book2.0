#!/usr/bin/env bash
# Doc to Chapters Skill 验证脚本
# 检查 Skill 结构完整性

set -e

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ERRORS=0

echo "=== Doc to Chapters Skill 验证 ==="
echo ""

# 检查必需文件
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

# 检查必需目录
check_dir() {
    local dir="$1"
    local desc="$2"
    if [ -d "$SKILL_DIR/$dir" ]; then
        echo "[OK] $desc: $dir/"
    else
        echo "[MISSING] $desc: $dir/"
        ((ERRORS++))
    fi
}

# 检查 SKILL.md frontmatter
check_frontmatter() {
    if [ -f "$SKILL_DIR/SKILL.md" ]; then
        if grep -q "^---$" "$SKILL_DIR/SKILL.md"; then
            echo "[OK] SKILL.md 包含 frontmatter"
        else
            echo "[WARN] SKILL.md 可能缺少 frontmatter"
        fi

        if grep -q "^name:" "$SKILL_DIR/SKILL.md"; then
            echo "[OK] SKILL.md 包含 name 字段"
        else
            echo "[MISSING] SKILL.md 缺少 name 字段"
            ((ERRORS++))
        fi

        if grep -q "^description:" "$SKILL_DIR/SKILL.md"; then
            echo "[OK] SKILL.md 包含 description 字段"
        else
            echo "[MISSING] SKILL.md 缺少 description 字段"
            ((ERRORS++))
        fi
    fi
}

# 检查 Python 脚本依赖
check_python_deps() {
    if python3 -c "import re, subprocess, tempfile" 2>/dev/null || python -c "import re, subprocess, tempfile" 2>/dev/null; then
        echo "[OK] Python 标准库可用"
    else
        echo "[WARN] Python 标准库检查失败"
    fi

    if command -v markitdown >/dev/null 2>&1; then
        echo "[OK] markitdown 已安装"
    else
        echo "[WARN] markitdown 未安装，运行需要: pip install markitdown"
    fi
}

# 执行检查
echo "1. 检查必需文件..."
check_file "SKILL.md" "核心说明"
check_file "template.md" "任务模板"
check_file "scripts/doc_to_chapters.py" "主处理脚本"

echo ""
echo "2. 检查可选文件..."
check_file "examples/sample.md" "使用示例"
check_dir "examples" "示例目录"
check_dir "scripts" "脚本目录"

echo ""
echo "3. 检查 SKILL.md 格式..."
check_frontmatter

echo ""
echo "4. 检查 Python 依赖..."
check_python_deps

echo ""
echo "=== 验证结果 ==="
if [ $ERRORS -eq 0 ]; then
    echo "全部通过！Skill 结构完整。"
    exit 0
else
    echo "发现 $ERRORS 个问题，请修复后再使用。"
    exit 1
fi
