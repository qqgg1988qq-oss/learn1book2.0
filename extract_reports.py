#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 batch-knowledge-extractor 生成的 10 维度精读报告中，
提取指定章节并合并为临时摘要文件，供后续人工/AI 整合使用。
"""

import os
import re
from pathlib import Path

REPORTS_DIR = Path("/Users/chouchou/Documents/Obsidian Vault/九局下半怎么破局/项目/读书分享/DanKoe课程/数字经济学04/批量精读报告/reports")
OUTPUT_FILE = Path("/Users/chouchou/Desktop/myProject/learn1book2.0/temp_summary.md")

# 目标章节关键词（按优先级匹配）
TARGET_SECTIONS = [
    ("元信息", ["元信息"]),
    ("核心论点", ["核心论点"]),
    ("关键概念与定义", ["关键概念", "关键概念与定义"]),
    ("方法论", ["方法论", "方法 / 流程", "方法/流程"]),
    ("知识网络与关联", ["知识网络", "知识关联", "知识网络与关联"]),
    ("批判性思考", ["批判性思考", "批判性"]),
]


def normalize_heading(line: str) -> str:
    """去掉 Markdown 标题标记、序号、首尾空白，方便匹配。"""
    # 先去掉前导的 # 和空格
    line = re.sub(r"^#+\s*", "", line)
    # 去掉 1) / 1. / 1.1 / 6.1 / (1) 这类序号
    line = re.sub(r"^\(?[0-9]+(?:\.[0-9]+)*\)?[.\)\s]+", "", line)
    return line.strip()


def match_section(title: str, keywords: list[str]) -> bool:
    """判断一个标题是否命中某章节关键词。"""
    norm = normalize_heading(title)
    for kw in keywords:
        if kw in norm:
            return True
    return False


def extract_sections(text: str) -> dict[str, list[str]]:
    """
    从 Markdown 文本中提取目标章节。
    按二级标题 ## 切分；对每个目标章节，收集其下所有子标题与正文，
    直到下一个同层级或更高层级标题。
    """
    # 把文本按行切分，但保留标题行以便识别
    lines = text.splitlines()

    # 先找到所有二级标题位置
    section_blocks = []  # [(heading_line, start_index, end_index)]
    heading_indices = []
    for i, line in enumerate(lines):
        if re.match(r"^##\s+", line):
            heading_indices.append(i)

    for idx, start in enumerate(heading_indices):
        end = heading_indices[idx + 1] if idx + 1 < len(heading_indices) else len(lines)
        section_blocks.append((lines[start], start, end))

    results: dict[str, list[str]] = {name: [] for name, _ in TARGET_SECTIONS}

    for heading, start, end in section_blocks:
        for sec_name, keywords in TARGET_SECTIONS:
            if match_section(heading, keywords):
                content = lines[start:end]
                # 清理空行但保留段落结构
                cleaned = []
                for line in content:
                    cleaned.append(line)
                results[sec_name].extend(cleaned)
                results[sec_name].append("")  # 段间隔
                break

    return results


def derive_display_name(filename: str) -> str:
    """从 report 文件名还原源文件标题。"""
    # 去掉 .report.md 后缀
    name = re.sub(r"\.report\.md$", "", filename)
    # 如果文件名本身以 .md 结尾（源文件是 markdown），再去掉一层 .md
    name = re.sub(r"\.md$", "", name)
    return name


def main():
    report_files = sorted([f for f in REPORTS_DIR.iterdir() if f.is_file() and f.suffix == ".md"])
    if not report_files:
        raise RuntimeError(f"在 {REPORTS_DIR} 下未找到 .md 报告文件")

    with OUTPUT_FILE.open("w", encoding="utf-8") as out:
        out.write("# 批量精读报告临时摘要\n\n")
        out.write(f"来源目录：`{REPORTS_DIR}`\n\n")
        out.write(f"共提取 {len(report_files)} 份报告，目标章节：")
        out.write(", ".join([s[0] for s in TARGET_SECTIONS]))
        out.write("\n\n---\n\n")

        for report_file in report_files:
            display_name = derive_display_name(report_file.name)
            out.write(f"# {display_name}\n\n")
            out.write(f"**源报告文件名**：`{report_file.name}`\n\n")

            text = report_file.read_text(encoding="utf-8")
            sections = extract_sections(text)

            for sec_name, _ in TARGET_SECTIONS:
                content = sections[sec_name]
                out.write(f"## {sec_name}\n\n")
                if not content or all(line.strip() == "" for line in content):
                    out.write("*（本报告未识别到该章节内容）*\n\n")
                else:
                    for line in content:
                        out.write(line + "\n")
                    out.write("\n")

            out.write("---\n\n")

    print(f"已生成临时摘要文件：{OUTPUT_FILE}")
    print(f"共处理 {len(report_files)} 份报告")


if __name__ == "__main__":
    main()
