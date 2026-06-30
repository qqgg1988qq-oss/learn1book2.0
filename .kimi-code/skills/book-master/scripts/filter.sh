#!/usr/bin/env bash
# Book Master — 章节过滤脚本
# 自动识别并排除非内容章节（目录、参考文献、索引、封面等）

set -e

CHAPTERS_DIR="$1"

if [ -z "$CHAPTERS_DIR" ]; then
    echo "Usage: filter.sh <chapters-dir>"
    exit 1
fi

# 排除关键词（小写匹配）
EXCLUDE_PATTERNS=(
    "_index.md"
    "封面"
    "书名"
    "版权"
    "目录"
    "参考文献"
    "索引"
    "献辞"
)

# 遍历所有 .md 文件，输出应保留的文件列表
for f in "$CHAPTERS_DIR"/*.md; do
    [ -f "$f" ] || continue
    basename=$(basename "$f")
    skip=false

    for pattern in "${EXCLUDE_PATTERNS[@]}"; do
        if echo "$basename" | grep -qi "$pattern"; then
            skip=true
            break
        fi
    done

    if [ "$skip" = false ]; then
        echo "$f"
    fi
done
