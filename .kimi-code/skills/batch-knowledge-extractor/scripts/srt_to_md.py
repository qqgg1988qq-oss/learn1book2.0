#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SRT 字幕文件转 Markdown 文本。

用法：
    python3 srt_to_md.py <srt_path_or_folder> [output_dir]
"""

import os
import re
import sys


def srt_to_md(input_path, output_path):
    """将单个 SRT 文件清洗为连续 Markdown 文本。"""
    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()

    blocks = re.split(r"\n\s*\n", content.strip())
    lines = []

    for block in blocks:
        block = block.strip()
        if not block:
            continue
        parts = block.split("\n")
        # 移除序号行和时间码行
        if len(parts) >= 2 and re.match(r"^\d+$", parts[0].strip()):
            parts = parts[2:]
        text = " ".join(parts)
        # 移除 HTML 标签
        text = re.sub(r"<[^>]+>", "", text)
        text = text.strip()
        if text:
            lines.append(text)

    full_text = " ".join(lines)
    full_text = re.sub(r"\s+", " ", full_text)

    base_name = os.path.basename(input_path).replace(".srt", "")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"# {base_name}\n\n")
        f.write(full_text)

    print(f"[DONE] {output_path}")


def batch_convert(folder_path, output_dir=None):
    """批量转换文件夹内所有 SRT 文件。"""
    results = []
    os.makedirs(output_dir, exist_ok=True)
    for fname in sorted(os.listdir(folder_path)):
        if fname.lower().endswith(".srt"):
            input_path = os.path.join(folder_path, fname)
            output_path = os.path.join(output_dir, fname.replace(".srt", ".md"))
            srt_to_md(input_path, output_path)
            results.append(output_path)
    return results


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python srt_to_md.py <srt_path_or_folder> [output_dir]")
        sys.exit(1)

    input_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    if os.path.isdir(input_path):
        batch_convert(input_path, output_dir or input_path)
    else:
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        out_path = (
            os.path.join(output_dir, os.path.basename(input_path).replace(".srt", ".md"))
            if output_dir
            else input_path.replace(".srt", ".md")
        )
        srt_to_md(input_path, out_path)
