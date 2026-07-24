#!/usr/bin/env python3
"""Merge EPUB-extracted part files for Naval Almanack into logical chapters."""

import os
import sys
import re
import shutil


def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def merge_files(chapters_dir, output_name, source_files, remove_sources=True):
    """Merge a list of source markdown files into one output file."""
    out_path = os.path.join(chapters_dir, output_name)
    parts = []
    for src in source_files:
        src_path = os.path.join(chapters_dir, src)
        if not os.path.exists(src_path):
            print(f"  Warning: {src} not found, skipping")
            continue
        content = read_file(src_path)
        # Strip YAML frontmatter from merged sources except the first one
        if parts:
            content = re.sub(r'^---\s*\n.*?---\s*\n', '', content, count=1, flags=re.DOTALL)
        parts.append(content)

    merged = "\n\n---\n\n".join(parts)
    # Build a simple frontmatter for the merged file
    title = output_name.replace('.md', '').replace('chapter-', '第').replace('-', ' ')
    frontmatter = f"""---
title: "{title}"
source: "merged from EPUB parts"
level: 1
---

"""
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(frontmatter)
        f.write(merged)

    print(f"  Written: {output_name} ({len(frontmatter) + len(merged)} chars)")

    if remove_sources:
        for src in source_files:
            src_path = os.path.join(chapters_dir, src)
            if os.path.exists(src_path):
                os.remove(src_path)


def main(book_dir):
    chapters_dir = os.path.join(book_dir, 'chapters')
    if not os.path.isdir(chapters_dir):
        print(f"Chapters directory not found: {chapters_dir}")
        sys.exit(1)

    # Backup original extraction by copying to a subfolder
    backup_dir = os.path.join(book_dir, 'chapters_raw_backup')
    if os.path.exists(backup_dir):
        shutil.rmtree(backup_dir)
    shutil.copytree(chapters_dir, backup_dir)
    print(f"Backed up raw chapters to {backup_dir}")

    # Define merge groups based on the table of contents
    merge_groups = [
        ('front-matter.md', [
            'front-07-关于本书的重要说明 DISCLAIMER.md',
            'chapter-01-推荐序一 财富与幸福源自选择.md',
            'chapter-02-推荐序二 一场反直觉的精神瑜伽.md',
            'chapter-03-序 PROLOGUE.md',
            'front-08-埃里克的笔记（关于这本书）.md',
            'front-09-纳瓦尔·拉维坎特经历表.md',
            'front-10-纳瓦尔亲述.md',
        ]),
        ('chapter-01-积累财富.md', [
            'front-12-part0013.md',
            'front-13-part0014.md',
            'front-14-part0015.md',
            'chapter-04-part0016.md',
            'chapter-05-part0017.md',
            'chapter-06-part0018.md',
            'chapter-07-part0019.md',
            'chapter-08-part0020.md',
            'chapter-09-part0021.md',
            'chapter-10-part0022.md',
            'chapter-11-part0023.md',
            'chapter-12-part0024.md',
        ]),
        ('chapter-02-增强判断力.md', [
            'chapter-13-part0025.md',
            'chapter-14-part0026.md',
            'chapter-15-part0027.md',
            'chapter-16-part0028.md',
            'chapter-17-part0029.md',
            'chapter-18-part0030.md',
            'chapter-19-part0031.md',
        ]),
        ('chapter-03-学习幸福.md', [
            'chapter-20-第二部分　幸福.md',
            'chapter-21-part0033.md',
            'chapter-22-part0034.md',
            'chapter-23-part0035.md',
            'chapter-24-part0036.md',
            'chapter-25-part0037.md',
            'chapter-26-part0038.md',
            'chapter-27-part0039.md',
            'chapter-28-part0040.md',
            'chapter-29-part0041.md',
            'chapter-30-part0042.md',
        ]),
        ('chapter-04-自我救赎.md', [
            'chapter-31-part0043.md',
            'chapter-32-part0044.md',
            'chapter-33-part0045.md',
            'chapter-34-part0046.md',
            'chapter-35-part0047.md',
            'chapter-36-part0048.md',
            'back-01-part0049.md',
        ]),
        ('chapter-05-哲学.md', [
            'back-02-part0050.md',
            'back-03-part0051.md',
            'back-04-part0052.md',
            'back-05-part0053.md',
            'back-06-part0054.md',
        ]),
        ('back-01-纳瓦尔的推荐读物与原则.md', [
            'back-08-额外推荐.md',
            'back-09-part0057.md',
            'back-10-part0058.md',
            'back-11-part0059.md',
            'back-12-part0060.md',
            'back-13-part0061.md',
            'back-14-part0062.md',
        ]),
        ('back-02-致谢.md', [
            'chapter-37-致谢.md',
        ]),
        ('back-03-附录.md', [
            'chapter-38-附录.md',
        ]),
    ]

    for output_name, sources in merge_groups:
        merge_files(chapters_dir, output_name, sources, remove_sources=True)

    # Remove leftover tiny divider files that are not in any group
    leftovers = [
        'front-01-titlepage.md',
        'front-02-书名页.md',
        'front-03-版权信息.md',
        'front-04-目录.md',
        'front-05-part0003.md',
        'front-06-part0004.md',
        'front-11-第一部分　财富.md',
        'back-07-part0055.md',
    ]
    for f in leftovers:
        fpath = os.path.join(chapters_dir, f)
        if os.path.exists(fpath):
            os.remove(fpath)
            print(f"  Removed leftover: {f}")

    # Rewrite _index.md to reflect merged chapters
    merged_files = [g[0] for g in merge_groups]
    index_path = os.path.join(chapters_dir, '_index.md')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write("# 纳瓦尔宝典：财富与幸福指南\n\n## 章节列表\n\n")
        for fname in merged_files:
            base = os.path.splitext(fname)[0]
            f.write(f"- [{base}]({fname})\n")
    print(f"Updated {index_path}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: merge_naval_chapters.py <book-dir>")
        sys.exit(1)
    main(sys.argv[1])
