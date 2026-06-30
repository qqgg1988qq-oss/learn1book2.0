#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将 Markdown 口播文案转换为公众号/头条号富文本 HTML
风格：干货科普（Knowledge Popular）
"""

import re
import os
import html
from datetime import datetime

# 尝试导入 opencc
try:
    import opencc
    converter = opencc.OpenCC('tw2s')  # 台湾繁体转大陆简体
except Exception as e:
    print(f"opencc 导入失败: {e}")
    converter = None


def convert_to_simplified(text):
    if converter:
        return converter.convert(text)
    return text


def escape_html(text):
    return html.escape(text).replace(' ', '&nbsp;')  # 保留空格用于缩进控制


def parse_inline(text):
    """解析行内 **bold** 为 <strong>"""
    # 先处理加粗
    parts = re.split(r'\*\*(.*?)\*\*', text)
    result = []
    for i, part in enumerate(parts):
        if i % 2 == 0:
            result.append(html.escape(part))
        else:
            result.append(f'<strong style="font-weight: bold; color: #1e293b; background: #fef3c7; padding: 2px 6px; border-radius: 3px;">{html.escape(part)}</strong>')
    return ''.join(result)


def build_wechat_html(markdown_lines, title, meta):
    """构建公众号版 HTML"""
    sections = []
    i = 0
    n = len(markdown_lines)

    while i < n:
        line = markdown_lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        # H1
        if stripped.startswith('# '):
            text = stripped[2:].strip()
            sections.append(
                f'<h1 style="font-size: 22px; font-weight: bold; color: #1e293b; margin: 30px 0 18px; padding: 10px 15px; background: #fffbeb; border-left: 4px solid #f59e0b;">'
                f'{parse_inline(text)}</h1>'
            )
            i += 1
            continue

        # H2
        if stripped.startswith('## '):
            text = stripped[3:].strip()
            sections.append(
                f'<h2 style="font-size: 17px; font-weight: bold; color: #d97706; margin: 22px 0 12px; padding-bottom: 6px; border-bottom: 2px solid #fef3c7;">'
                f'{parse_inline(text)}</h2>'
            )
            i += 1
            continue

        # Blockquote
        if stripped.startswith('>'):
            quote_lines = []
            while i < n and markdown_lines[i].strip().startswith('>'):
                qline = markdown_lines[i].strip()
                # 去掉开头的 > 和可能的前导空格
                qline = re.sub(r'^>\s?', '', qline)
                quote_lines.append(qline)
                i += 1
            quote_text = '\n'.join(quote_lines)
            # 处理内部的 **
            quote_html = parse_inline(quote_text).replace('\n', '<br>')
            sections.append(
                f'<blockquote style="background: #fffbeb; border-left: 4px solid #f59e0b; padding: 15px 20px; margin: 20px 0; color: #78350f; font-size: 14px; line-height: 1.75;">'
                f'{quote_html}</blockquote>'
            )
            continue

        # Unordered list
        if stripped.startswith('- ') or stripped.startswith('* '):
            list_items = []
            while i < n and (markdown_lines[i].strip().startswith('- ') or markdown_lines[i].strip().startswith('* ')):
                item_text = markdown_lines[i].strip()[2:]
                list_items.append(
                    f'<li style="margin: 10px 0; color: #475569; font-size: 15px; line-height: 1.8;">'
                    f'<span style="color: #f59e0b; font-weight: bold; margin-right: 8px;">✓</span>'
                    f'{parse_inline(item_text)}</li>'
                )
                i += 1
            sections.append(
                f'<ul style="margin: 18px 0; padding-left: 20px; list-style: none;">'
                f'{"".join(list_items)}</ul>'
            )
            continue

        # Horizontal rule
        if stripped == '---':
            sections.append(
                f'<p style="text-align: center; margin: 25px 0; color: #f59e0b; font-size: 14px; letter-spacing: 2px;">—— ✦ ——</p>'
            )
            i += 1
            continue

        # Regular paragraph
        para_lines = []
        while i < n and markdown_lines[i].strip() and not markdown_lines[i].strip().startswith(('#', '>', '- ', '* ', '---')):
            para_lines.append(markdown_lines[i].strip())
            i += 1
        para_text = ''.join(para_lines)
        sections.append(
            f'<p style="font-size: 15px; line-height: 1.8; color: #475569; margin: 18px 0; text-align: justify;">'
            f'{parse_inline(para_text)}</p>'
        )

    body_content = '\n'.join(sections)

    html_template = f'''<!-- 
  排版风格：干货科普（Knowledge Popular）
  目标平台：微信公众号
  生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
  使用说明：全选复制 → 粘贴到公众号编辑器
-->
<section style="margin: 0; padding: 16px; background: #ffffff; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;">
{body_content}
</section>'''

    return html_template


def build_toutiao_html(markdown_lines, title, meta):
    """构建头条号版 HTML（结构更简化）"""
    sections = []
    i = 0
    n = len(markdown_lines)

    while i < n:
        line = markdown_lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        if stripped.startswith('# '):
            text = stripped[2:].strip()
            sections.append(
                f'<h1 style="font-size: 22px; font-weight: bold; color: #1e293b; margin: 25px 0 15px; padding: 10px 12px; background: #fffbeb; border-left: 4px solid #f59e0b;">'
                f'{parse_inline(text)}</h1>'
            )
            i += 1
            continue

        if stripped.startswith('## '):
            text = stripped[3:].strip()
            sections.append(
                f'<h2 style="font-size: 17px; font-weight: bold; color: #d97706; margin: 20px 0 10px; padding-bottom: 6px; border-bottom: 2px solid #fef3c7;">'
                f'{parse_inline(text)}</h2>'
            )
            i += 1
            continue

        if stripped.startswith('>'):
            quote_lines = []
            while i < n and markdown_lines[i].strip().startswith('>'):
                qline = re.sub(r'^>\s?', '', markdown_lines[i].strip())
                quote_lines.append(qline)
                i += 1
            quote_html = parse_inline('\n'.join(quote_lines)).replace('\n', '<br>')
            sections.append(
                f'<blockquote style="background: #fffbeb; border-left: 4px solid #f59e0b; padding: 12px 16px; margin: 15px 0; color: #78350f; font-size: 14px; line-height: 1.7;">'
                f'{quote_html}</blockquote>'
            )
            continue

        if stripped.startswith('- ') or stripped.startswith('* '):
            list_items = []
            while i < n and (markdown_lines[i].strip().startswith('- ') or markdown_lines[i].strip().startswith('* ')):
                item_text = markdown_lines[i].strip()[2:]
                list_items.append(
                    f'<li style="margin: 8px 0; color: #475569; font-size: 15px; line-height: 1.7;">'
                    f'<span style="color: #f59e0b; margin-right: 6px;">✓</span>'
                    f'{parse_inline(item_text)}</li>'
                )
                i += 1
            sections.append(f'<ul style="margin: 15px 0; padding-left: 18px; list-style: none;">{"".join(list_items)}</ul>')
            continue

        if stripped == '---':
            sections.append('<p style="text-align: center; margin: 20px 0; color: #f59e0b; font-size: 14px;">—— ✦ ——</p>')
            i += 1
            continue

        para_lines = []
        while i < n and markdown_lines[i].strip() and not markdown_lines[i].strip().startswith(('#', '>', '- ', '* ', '---')):
            para_lines.append(markdown_lines[i].strip())
            i += 1
        para_text = ''.join(para_lines)
        sections.append(
            f'<p style="font-size: 15px; line-height: 1.75; color: #475569; margin: 15px 0; text-align: justify;">'
            f'{parse_inline(para_text)}</p>'
        )

    return f'''<!-- 
  排版风格：干货科普（Knowledge Popular）
  目标平台：今日头条号
  生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
  使用说明：全选复制 → 粘贴到头条号编辑器
-->
<section style="margin: 0; padding: 14px; background: #ffffff; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
{"\n".join(sections)}
</section>'''


def build_preview_html(wechat_html, title):
    """构建本地预览版 HTML"""
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(title)}</title>
  <style>
    body {{ margin: 0; padding: 20px; background: #f5f5f5; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }}
    .phone {{ max-width: 414px; margin: 0 auto; background: #ffffff; box-shadow: 0 4px 20px rgba(0,0,0,0.08); border-radius: 12px; overflow: hidden; }}
  </style>
</head>
<body>
  <div class="phone">
    {wechat_html}
  </div>
</body>
</html>'''


def main():
    src_path = '/Users/chouchou/Documents/Obsidian Vault/成长计划/图文发布/有趣文章/世界杯主题/看世界杯要花费多少钱/调研简报-中国大陆居民赴美看世界杯成本分析-script.md'
    output_dir = os.path.dirname(src_path)
    base_name = '调研简报-中国大陆居民赴美看世界杯成本分析'

    # 读取并转换
    with open(src_path, 'r', encoding='utf-8') as f:
        content = f.read()

    content_simplified = convert_to_simplified(content)

    # 截断：只保留正文内容，去掉视频制作建议
    marker = '## 视频制作建议'
    if marker in content_simplified:
        content_simplified = content_simplified.split(marker)[0].strip()

    lines = content_simplified.split('\n')

    # 提取标题和元信息
    title = ''
    meta = {}
    for line in lines:
        if line.strip().startswith('# '):
            title = line.strip()[2:]
            break

    wechat_html = build_wechat_html(lines, title, meta)
    toutiao_html = build_toutiao_html(lines, title, meta)
    preview_html = build_preview_html(wechat_html, title)

    # 写入文件
    wechat_path = os.path.join(output_dir, f'{base_name}_wechat.html')
    toutiao_path = os.path.join(output_dir, f'{base_name}_toutiao.html')
    preview_path = os.path.join(output_dir, f'{base_name}_preview.html')

    with open(wechat_path, 'w', encoding='utf-8') as f:
        f.write(wechat_html)

    with open(toutiao_path, 'w', encoding='utf-8') as f:
        f.write(toutiao_html)

    with open(preview_path, 'w', encoding='utf-8') as f:
        f.write(preview_html)

    print(f'已生成文件：')
    print(f'  - {wechat_path}')
    print(f'  - {toutiao_path}')
    print(f'  - {preview_path}')


if __name__ == '__main__':
    main()
