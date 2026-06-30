#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""doc-to-chapters — 任意文档 → Markdown → 按章节拆分。

组合 markitdown 与 Markdown 标题拆分，将 PDF/EPUB/DOCX/PPTX/图片等文件
转换为结构化的章节 Markdown，输出结构与 book-splitter 保持一致。
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


# 前置/后置内容关键词
FRONT_KEYWORDS = ["目录", "landmarks", "封面", "书名", "版权", "前言", "序言", "序章", "序", "献辞"]
BACK_KEYWORDS = ["后记", "注释", "参考文献", "索引", "附录", "致谢"]


def sanitize_filename(name: str) -> str:
    """将章节标题转换为安全的文件名。"""
    name = re.sub(r'[\\/*?:"<>|]', "", name)
    name = re.sub(r"\s+", "_", name.strip())
    return name[:80]


def find_markitdown() -> str:
    """查找可用的 markitdown 命令。"""
    for cmd in ["markitdown", "python -m markitdown", "python3 -m markitdown"]:
        if shutil.which(cmd.split()[0]):
            return cmd
    raise RuntimeError("未找到 markitdown 命令，请先安装：pip install markitdown")


def convert_to_markdown(input_path: Path, output_path: Path) -> None:
    """调用 markitdown 将输入文件转换为 Markdown。"""
    cmd = find_markitdown()
    full_cmd = f'{cmd} "{input_path}" -o "{output_path}"'
    print(f"[convert] {full_cmd}")
    result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"markitdown 转换失败：\n{result.stderr}")
    if not output_path.exists():
        raise RuntimeError(f"markitdown 未生成输出文件：{output_path}")


def classify_section(title: str, section_type_counter: dict) -> tuple:
    """根据标题判断章节类型并生成文件名。

    返回 (section_type, filename)。
    """
    title_stripped = title.strip()
    title_lower = title_stripped.lower()

    # 前置内容
    is_front = any(kw in title_lower for kw in FRONT_KEYWORDS)
    # 后置内容
    is_back = any(kw in title_lower for kw in BACK_KEYWORDS)

    if is_front:
        section_type = "front"
    elif is_back:
        section_type = "back"
    else:
        section_type = "chapter"

    section_type_counter[section_type] += 1
    seq = section_type_counter[section_type]
    filename = f"{section_type}-{seq:02d}-{sanitize_filename(title_stripped)}.md"
    return section_type, filename


def extract_summary(lines: list) -> str:
    """提取段落第一行非空内容作为摘要。"""
    for line in lines:
        stripped = line.strip()
        if stripped:
            return stripped.lstrip("#* -•").strip()
    return ""


def split_markdown(input_path: Path, output_dir: Path, heading_level: int = 1) -> list:
    """按指定标题级别拆分 Markdown 文件。

    返回章节信息列表，每项为 dict：
    {type, filename, title, summary}。
    """
    text = input_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    heading_pattern = re.compile(rf"^#{{{heading_level}}}\s+")

    sections = []
    current_title = None
    current_lines = []

    for line in lines:
        if heading_pattern.match(line):
            if current_title is not None:
                sections.append((current_title, current_lines))
            current_title = heading_pattern.sub("", line).strip()
            current_lines = []
        else:
            current_lines.append(line)

    if current_title is not None:
        sections.append((current_title, current_lines))

    if not sections:
        raise ValueError(f"未找到任何 H{heading_level} 标题，无法拆分。")

    section_type_counter = {"front": 0, "chapter": 0, "back": 0}
    index_entries = []

    for title, content_lines in sections:
        section_type, filename = classify_section(title, section_type_counter)

        # 移除末尾空行
        while content_lines and content_lines[-1].strip() == "":
            content_lines.pop()

        summary = extract_summary(content_lines)

        frontmatter = f"""---
title: "{title}"
level: {heading_level}
source: "{input_path.name}"
---

"""
        file_content = frontmatter + "\n".join(content_lines)
        if not file_content.endswith("\n"):
            file_content += "\n"

        output_path = output_dir / filename
        output_path.write_text(file_content, encoding="utf-8")
        print(f"[split] {output_path}")

        index_entries.append({
            "type": section_type,
            "filename": filename,
            "title": title,
            "summary": summary,
        })

    return index_entries


def generate_index(output_dir: Path, source_name: str, entries: list) -> None:
    """生成 _index.md 索引文件。"""
    index_lines = [
        "---",
        f'title: "{source_name}"',
        f'source: "{source_name}"',
        "---",
        "",
        f"# {source_name}",
        "",
        "## 章节索引",
        "",
    ]

    for entry in entries:
        title = entry["title"]
        filename = entry["filename"]
        summary = entry["summary"]
        index_lines.append(f"- [{title}](./{filename})")
        if summary:
            snippet = summary[:80] + "..." if len(summary) > 80 else summary
            index_lines.append(f"  - {snippet}")

    index_lines.append("")
    index_path = output_dir / "_index.md"
    index_path.write_text("\n".join(index_lines), encoding="utf-8")
    print(f"[index] {index_path}")


def main():
    parser = argparse.ArgumentParser(
        description="任意文档 → Markdown → 按章节拆分",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("input", help="输入文件路径（支持 PDF/EPUB/DOCX/PPTX/图片/Markdown 等）")
    parser.add_argument("output", nargs="?", help="输出目录，默认为输入文件同名文件夹")
    parser.add_argument(
        "--heading-level",
        type=int,
        choices=[1, 2],
        default=1,
        help="按 H1 或 H2 拆分，默认 H1",
    )
    parser.add_argument(
        "--keep-md",
        action="store_true",
        help="保留中间生成的 .md 文件到输出目录",
    )
    args = parser.parse_args()

    input_path = Path(args.input).resolve()
    if not input_path.exists():
        print(f"错误：输入文件不存在：{input_path}", file=sys.stderr)
        sys.exit(1)

    # 输出目录默认与源文件同名
    if args.output:
        output_dir = Path(args.output).resolve()
    else:
        output_dir = input_path.parent / input_path.stem
    output_dir.mkdir(parents=True, exist_ok=True)

    # 若输入已是 Markdown，直接拆分；否则先转换
    if input_path.suffix.lower() == ".md":
        md_path = input_path
    else:
        if args.keep_md:
            md_path = output_dir / f"{input_path.stem}.md"
        else:
            temp_dir = tempfile.mkdtemp(prefix="doc-to-chapters-")
            md_path = Path(temp_dir) / f"{input_path.stem}.md"
        convert_to_markdown(input_path, md_path)

    try:
        entries = split_markdown(md_path, output_dir, heading_level=args.heading_level)
        generate_index(output_dir, input_path.stem, entries)
    finally:
        # 清理临时 md 文件
        if not args.keep_md and input_path.suffix.lower() != ".md" and md_path.exists():
            try:
                md_path.unlink()
                md_path.parent.rmdir()
            except OSError:
                pass

    print(f"\n完成：{len(entries)} 个章节已输出到 {output_dir}")


if __name__ == "__main__":
    main()
