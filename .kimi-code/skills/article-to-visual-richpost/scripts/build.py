#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
article-to-visual-richpost 辅助脚本。

功能：
1. 如果 visual-scenes.json 不存在，生成模板框架（需由 AI/用户填写场景内容）
2. 如果 visual-scenes.json 已存在，根据 Markdown 文章和场景文件生成 article.html

用法：
    python3 build.py /path/to/article.md /path/to/output-dir --style 现代简约

依赖：
    无第三方依赖，使用 Python 标准库
"""

import argparse
import json
import re
from datetime import datetime
from pathlib import Path


# 排版风格配置
STYLE_PRESETS = {
    '现代简约': {
        'text_main': '#1a1a1a',
        'text_body': '#3f3f3f',
        'text_secondary': '#888888',
        'accent': '#2c5aa0',
        'bg': '#ffffff',
        'quote_bg': '#f5f7fa',
        'quote_border': '#2c5aa0',
        'divider': '#e8e8e8',
        'h1_size': '22px',
        'h2_size': '18px',
        'p_size': '15px',
    },
    '时尚杂志': {
        'text_main': '#000000',
        'text_body': '#333333',
        'text_secondary': '#999999',
        'accent': '#d4a574',
        'bg': '#ffffff',
        'quote_bg': '#faf8f5',
        'quote_border': '#d4a574',
        'divider': '#000000',
        'h1_size': '26px',
        'h2_size': '16px',
        'p_size': '15px',
    },
    '文艺清新': {
        'text_main': '#2c3e50',
        'text_body': '#4a5568',
        'text_secondary': '#a0aec0',
        'accent': '#7ca982',
        'bg': '#ffffff',
        'quote_bg': '#f8faf8',
        'quote_border': '#7ca982',
        'divider': '#e2e8f0',
        'h1_size': '22px',
        'h2_size': '17px',
        'p_size': '15px',
    },
    '高端商务': {
        'text_main': '#0f172a',
        'text_body': '#334155',
        'text_secondary': '#94a3b8',
        'accent': '#0f4c81',
        'bg': '#ffffff',
        'quote_bg': '#f1f5f9',
        'quote_border': '#0f4c81',
        'divider': '#cbd5e1',
        'h1_size': '24px',
        'h2_size': '18px',
        'p_size': '15px',
    },
    '科技极客': {
        'text_main': '#0f172a',
        'text_body': '#334155',
        'text_secondary': '#64748b',
        'accent': '#22d3ee',
        'bg': '#ffffff',
        'quote_bg': '#f8fafc',
        'quote_border': '#22d3ee',
        'divider': '#cbd5e1',
        'h1_size': '22px',
        'h2_size': '17px',
        'p_size': '15px',
    },
    '干货科普': {
        'text_main': '#1e293b',
        'text_body': '#475569',
        'text_secondary': '#94a3b8',
        'accent': '#f59e0b',
        'bg': '#ffffff',
        'quote_bg': '#fffbeb',
        'quote_border': '#f59e0b',
        'divider': '#e2e8f0',
        'h1_size': '22px',
        'h2_size': '17px',
        'p_size': '15px',
    },
    '东方美学': {
        'text_main': '#2d2a26',
        'text_body': '#5c5650',
        'text_secondary': '#a39e99',
        'accent': '#b22222',
        'bg': '#fdfcf8',
        'quote_bg': '#faf7f2',
        'quote_border': '#b22222',
        'divider': '#d4cec6',
        'h1_size': '24px',
        'h2_size': '17px',
        'p_size': '16px',
    },
    '条漫叙事': {
        'text_main': '#000000',
        'text_body': '#333333',
        'text_secondary': '#888888',
        'accent': '#000000',
        'bg': '#ffffff',
        'quote_bg': '#f5f5f5',
        'quote_border': '#000000',
        'divider': '#000000',
        'h1_size': '28px',
        'h2_size': '20px',
        'p_size': '16px',
    },
}


def parse_markdown(text: str) -> list:
    """解析 Markdown 中的口播文案部分为 HTML 元素列表。"""
    # 提取口播文案部分（从 ## 口播文案 到 ## 视频制作建议/下一个 ## 之间）
    match = re.search(r'##\s*口播文案\s*\n+(.+?)(?=\n+##\s+)', text, re.DOTALL)
    if not match:
        # 兜底：如果没有明确标记，解析全部内容
        match = re.search(r'##\s*口播文案\s*\n+(.+)', text, re.DOTALL)
    content = match.group(1).strip() if match else text

    elements = []
    current_paragraph = []

    def flush_paragraph():
        if current_paragraph:
            para_text = ' '.join(current_paragraph).strip()
            if para_text:
                elements.append(('p', para_text))
            current_paragraph.clear()

    for line in content.split('\n'):
        line = line.strip()
        if not line:
            flush_paragraph()
            continue

        if line.startswith('### '):
            flush_paragraph()
            elements.append(('h2', line[4:].strip()))
        elif line.startswith('---'):
            flush_paragraph()
            elements.append(('hr', ''))
        elif line.startswith('> '):
            flush_paragraph()
            elements.append(('blockquote', line[2:].strip()))
        else:
            current_paragraph.append(line)

    flush_paragraph()
    return elements


def clean_performance_marks(text: str) -> str:
    """去除口播语气标注。"""
    text = re.sub(r'（停顿\d*\.?\d*秒）', '', text)
    text = re.sub(r'（停顿）', '', text)
    text = re.sub(r'（放慢语速）', '', text)
    text = re.sub(r'（笑）', '', text)
    text = re.sub(r'（压低声音）', '', text)
    text = re.sub(r'（提高语调）', '', text)
    return text.strip()


def inline_bold(text: str, text_main: str) -> str:
    """将 **text** 转为加粗。"""
    return re.sub(
        r'\*\*(.+?)\*\*',
        rf'<strong style="font-weight: bold; color: {text_main};">\1</strong>',
        text
    )


def split_sentences(text: str) -> list:
    """按中文标点拆分句子。"""
    parts = re.split(r'([。！？])', text)
    sentences = []
    current = ''
    for part in parts:
        if not part:
            continue
        current += part
        if part in '。！？':
            sentences.append(current.strip())
            current = ''
    if current.strip():
        sentences.append(current.strip())
    return sentences


def find_matching_scenes(text: str, scene_keywords: list, inserted_scenes: set) -> list:
    """找出文本中匹配且未插入的场景，按 scene_id 排序。"""
    matched = []
    for scene_id, scene_title, keywords in scene_keywords:
        if scene_id in inserted_scenes:
            continue
        if keywords is None:
            continue
        if any(kw in text for kw in keywords):
            matched.append((scene_id, scene_title, keywords))
    return sorted(matched, key=lambda x: x[0])


def generate_visual_scenes_template(article_path: Path, output_path: Path):
    """生成 visual-scenes.json 模板框架。"""
    text = article_path.read_text(encoding='utf-8')
    title_match = re.search(r'^#\s+(.+)$', text, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else article_path.stem

    template = {
        "meta": {
            "title": title,
            "source": str(article_path),
            "scene_count": 0,
            "style_summary": "请根据用户选择的视觉风格填写，例如：手绘涂鸦手账风，米黄色笔记本纸张背景...",
            "global_style_prompt": "请填写全局画面基调描述..."
        },
        "prompts": [
            {
                "scene_id": 1,
                "title": "场景标题（与文章段落语义对应）",
                "prompt": "100-200字静态画面描述，包含背景、主体、构图、色彩、文字元素。禁止动画/运动/镜头/特效描述。"
            }
        ]
    }

    output_path.write_text(json.dumps(template, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'已生成模板：{output_path}')
    print('请填写 prompts 数组中的场景内容，确保每个 scene_id 都有对应段落。')


def build_html(elements: list, scenes_data: dict, style_name: str) -> str:
    """根据 Markdown 元素和场景数据生成 HTML。"""
    style = STYLE_PRESETS.get(style_name, STYLE_PRESETS['现代简约'])
    colors = style

    scenes = scenes_data.get('prompts', [])
    title = scenes_data.get('meta', {}).get('title', '文章标题')

    # 构建场景关键词映射
    # 优先使用场景中的 keywords 字段，否则使用 title 及其拆分
    scene_keywords = []
    for scene in scenes:
        scene_id = scene.get('scene_id')
        scene_title = scene.get('title', '')

        # 如果 JSON 中提供了 keywords，优先使用
        if 'keywords' in scene and isinstance(scene['keywords'], list) and scene['keywords']:
            keywords = [k.strip() for k in scene['keywords'] if k.strip()]
        else:
            # 使用场景标题作为关键词，同时提取标题中的核心词
            keywords = [scene_title]
            # 如果标题中有破折号，提取后半部分
            if '——' in scene_title:
                keywords.extend(scene_title.split('——'))
            if '：' in scene_title:
                keywords.extend(scene_title.split('：'))
            # 去重并过滤空字符串
            keywords = list(set([k.strip() for k in keywords if k.strip()]))

        scene_keywords.append((scene_id, scene_title, keywords))

    body_parts = []
    inserted_scenes = set()

    def insert_image(scene_id: int, scene_title: str):
        if scene_id in inserted_scenes:
            return
        inserted_scenes.add(scene_id)
        body_parts.append(
            f'<p style="text-align: center; margin: 25px 0;">\n'
            f'  <img src="images/scene-{scene_id:02d}.jpg" alt="{scene_title}" '
            f'style="max-width: 100%; border-radius: 6px; display: inline-block;">\n'
            f'</p>'
        )
        body_parts.append(
            f'<p style="font-size: 13px; color: {colors["text_secondary"]}; text-align: center; margin: 8px 0 25px;">'
            f'{scene_title}</p>'
        )

    def render_paragraph(text: str) -> str:
        text = clean_performance_marks(text)
        if not text:
            return ''
        text = inline_bold(text, colors['text_main'])
        return (
            f'<p style="font-size: {colors["p_size"]}; line-height: 1.75; color: {colors["text_body"]}; '
            f'margin: 18px 0; text-align: justify;">{text}</p>'
        )

    # 主标题
    body_parts.append(
        f'<h1 style="font-size: {colors["h1_size"]}; font-weight: bold; color: {colors["text_main"]}; '
        f'margin: 20px 0 25px; padding-bottom: 12px; border-bottom: 2px solid {colors["accent"]}; line-height: 1.4;">'
        f'{title}</h1>'
    )

    # 封面图（scene_id=1）默认放在主标题后面
    cover_scene = next((s for s in scene_keywords if s[0] == 1), None)
    if cover_scene:
        insert_image(cover_scene[0], cover_scene[1])
        scene_keywords = [s for s in scene_keywords if s[0] != 1]

    for elem_type, elem_text in elements:
        if elem_type == 'h2' or elem_type == 'h3':
            body_parts.append(
                f'<h2 style="font-size: {colors["h2_size"]}; font-weight: bold; color: {colors["accent"]}; '
                f'margin: 25px 0 15px; padding-left: 12px; border-left: 3px solid {colors["accent"]}; line-height: 1.4;">'
                f'{elem_text}</h2>'
            )
        elif elem_type == 'hr':
            body_parts.append(
                f'<hr style="border: none; border-top: 1px solid {colors["divider"]}; margin: 30px 0;">'
            )
        elif elem_type == 'blockquote':
            text = clean_performance_marks(elem_text)
            text = inline_bold(text, colors['text_main'])
            body_parts.append(
                f'<blockquote style="background: {colors["quote_bg"]}; border-left: 3px solid {colors["quote_border"]}; '
                f'padding: 15px 20px; margin: 20px 0; color: #555; font-size: 14px; line-height: 1.7;">'
                f'{text}</blockquote>'
            )
        else:
            matched_scenes = find_matching_scenes(elem_text, scene_keywords, inserted_scenes)

            if not matched_scenes:
                p_html = render_paragraph(elem_text)
                if p_html:
                    body_parts.append(p_html)
            elif len(matched_scenes) == 1:
                p_html = render_paragraph(elem_text)
                if p_html:
                    body_parts.append(p_html)
                scene_id, scene_title, _ = matched_scenes[0]
                insert_image(scene_id, scene_title)
            else:
                # 多个场景匹配同一段落：按句子拆分，每个句子后插入匹配场景
                sentences = split_sentences(elem_text)
                for sentence in sentences:
                    p_html = render_paragraph(sentence)
                    if p_html:
                        body_parts.append(p_html)
                    sentence_scenes = find_matching_scenes(sentence, scene_keywords, inserted_scenes)
                    if sentence_scenes:
                        scene_id, scene_title, _ = sentence_scenes[0]
                        insert_image(scene_id, scene_title)

    # 兜底：确保每张图都用上
    pending_scenes = [
        (sid, title) for sid, title, _ in scene_keywords if sid not in inserted_scenes
    ]
    if pending_scenes:
        body_parts.append(
            f'<hr style="border: none; border-top: 1px solid {colors["divider"]}; margin: 30px 0;">'
        )
        for scene_id, scene_title in pending_scenes:
            body_parts.append(
                f'<p style="font-size: 14px; line-height: 1.7; color: {colors["text_secondary"]}; '
                f'margin: 15px 0; text-align: center;">（配套画面）</p>'
            )
            insert_image(scene_id, scene_title)

    body_html = '\n'.join(body_parts)

    html = f'''<!--
  排版风格：{style_name}
  生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
  使用说明：
    1. 将本文同级目录下创建 images/ 文件夹
    2. 根据 visual-scenes.json 生成图片，命名为 scene-01.jpg, scene-02.jpg ...
    3. 用浏览器打开 article.html 预览效果
-->
<section style="padding: 16px; font-family: -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Helvetica, Segoe UI, Arial, Roboto, 'PingFang SC', 'miui', 'Hiragino Sans GB', 'Microsoft Yahei', sans-serif; background: {colors['bg']}; color: {colors['text_body']};">
{body_html}
</section>'''

    return html


def main():
    parser = argparse.ArgumentParser(description='文章视觉化+图文排版一站式工具')
    parser.add_argument('article', help='Markdown 文章路径')
    parser.add_argument('output_dir', help='输出目录')
    parser.add_argument('--style', default='现代简约', help='排版风格名称')
    args = parser.parse_args()

    article_path = Path(args.article)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    scenes_path = output_dir / 'visual-scenes.json'
    html_path = output_dir / 'article.html'

    if not scenes_path.exists():
        print(f'未找到 {scenes_path}，正在生成模板...')
        generate_visual_scenes_template(article_path, scenes_path)
        return

    # 读取文章和场景文件
    md_text = article_path.read_text(encoding='utf-8')
    scenes_data = json.loads(scenes_path.read_text(encoding='utf-8'))

    elements = parse_markdown(md_text)
    html = build_html(elements, scenes_data, args.style)

    html_path.write_text(html, encoding='utf-8')
    print(f'已生成：{html_path}')


if __name__ == '__main__':
    main()
