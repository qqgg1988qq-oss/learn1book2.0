#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
今日头条标题生成结果的保存工具。

将 AI 生成的标题候选内容保存到输入文件同一目录，
文件命名为：{输入文件名（去扩展名）}_titles.md

用法：
    python3 save_titles.py /path/to/article.md

然后从标准输入粘贴 Markdown 内容，按 Ctrl+D 结束。

或者：
    cat titles.md | python3 save_titles.py /path/to/article.md
"""

import sys
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("用法：python3 save_titles.py /path/to/article.md")
        sys.exit(1)

    input_path = Path(sys.argv[1]).resolve()
    if not input_path.exists():
        print(f"错误：输入文件不存在：{input_path}")
        sys.exit(1)

    output_path = input_path.parent / f"{input_path.stem}_titles.md"

    print(f"等待输入 Markdown 内容...（输入结束后按 Ctrl+D）")
    content = sys.stdin.read()

    if not content.strip():
        print("错误：输入内容为空")
        sys.exit(1)

    output_path.write_text(content, encoding='utf-8')
    print(f"已保存：{output_path}")


if __name__ == '__main__':
    main()
