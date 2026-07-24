#!/usr/bin/env python3
"""
将纯文本书籍按章节拆分为 Markdown。
支持《道德经白话全译》这类以“第 X 章 标题”为分隔的文本。
"""
import argparse
import os
import re
from pathlib import Path


def sanitize_filename(name: str) -> str:
    name = re.sub(r'[\\/*?:"<>|]', "", name)
    name = re.sub(r'\s+', "_", name.strip())
    return name[:80]


def cn_number_to_int(text: str) -> int:
    """将中文数字转换为整数，支持一到八十一。"""
    cn_nums = {
        '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
        '六': 6, '七': 7, '八': 8, '九': 9, '十': 10,
        '百': 100, '千': 1000, '两': 2
    }
    if not text:
        return 0
    # 处理纯中文数字
    total = 0
    cur = 0
    for ch in text:
        if ch not in cn_nums:
            continue
        v = cn_nums[ch]
        if v >= 10:
            if cur == 0:
                cur = 1
            total += cur * v
            cur = 0
        else:
            cur = cur * 10 + v if cur else v
    total += cur
    return total


def split_book(input_path: str, output_dir: str):
    input_path = Path(input_path)
    output_dir = Path(output_dir)
    chapters_dir = output_dir / "chapters"
    chapters_dir.mkdir(parents=True, exist_ok=True)

    text = input_path.read_text(encoding='utf-8')
    lines = text.splitlines()

    # 章节标题正则：第[中文数字]+章 [标题]
    chapter_re = re.compile(r'^(第[一二三四五六七八九十百千零]+章)\s+(.*)$')

    sections = []  # (prefix, title, start_line, content_lines)
    current_prefix = None
    current_title = None
    current_start = 0
    current_lines = []

    for i, line in enumerate(lines):
        m = chapter_re.match(line.strip())
        if m:
            # 保存上一个 section
            if current_prefix is not None:
                sections.append((current_prefix, current_title, current_start, current_lines))
            current_prefix = m.group(1)
            current_title = m.group(2).strip()
            current_start = i + 1  # 行号从1开始
            current_lines = []
        else:
            current_lines.append(line)

    if current_prefix is not None:
        sections.append((current_prefix, current_title, current_start, current_lines))

    # 写入章节文件
    written = []
    for prefix, title, start_line, content_lines in sections:
        # 去除首尾空行
        while content_lines and content_lines[0].strip() == '':
            content_lines.pop(0)
        while content_lines and content_lines[-1].strip() == '':
            content_lines.pop()

        num = cn_number_to_int(prefix[1:-1])
        safe_title = sanitize_filename(title)
        filename = f"chapter-{num:02d}-{safe_title}.md"
        filepath = chapters_dir / filename

        frontmatter = f"""---
title: "{prefix} {title}"
source: "{input_path.name}"
line_start: {start_line}
chapter_number: {num}
---

"""
        filepath.write_text(frontmatter + '\n'.join(content_lines), encoding='utf-8')
        written.append((num, prefix, title, filename))

    # 写入索引
    index_path = chapters_dir / "_index.md"
    index_lines = ["# 章节索引\n", f"- 来源: {input_path.name}\n", f"- 章节数: {len(written)}\n\n"]
    for num, prefix, title, filename in sorted(written, key=lambda x: x[0]):
        index_lines.append(f"- [{prefix} {title}]({filename})\n")
    index_path.write_text(''.join(index_lines), encoding='utf-8')

    # 复制原文件为完整 markdown 副本
    full_md = output_dir / (output_dir.name + ".md")
    full_md.write_text(text, encoding='utf-8')

    print(f"已拆分 {len(written)} 章到 {chapters_dir}")
    print(f"索引文件: {index_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="将中文 TXT 书籍按章节拆分")
    parser.add_argument("input", help="输入 TXT 文件路径")
    parser.add_argument("output", help="输出书籍项目目录")
    args = parser.parse_args()
    split_book(args.input, args.output)
