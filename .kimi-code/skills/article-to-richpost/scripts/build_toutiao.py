#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
根据 Markdown 文章和 visual-scenes.json 生成头条号富文本 HTML。
风格：现代简约

图片标注规则（严格遵循）：
1. visual-scenes.json 中的每个场景都必须生成对应的 [图片X：场景标题] 标注
2. 标注位置必须与 JSON 设计时的段落位置一致
3. 两个图片标注之间必须至少间隔一个正文段落，禁止连续堆叠
"""

import json
import re
from datetime import datetime
from pathlib import Path


def parse_markdown(text: str) -> list:
    """解析口播文案部分为 HTML 元素列表。"""
    # 提取口播文案部分
    match = re.search(r'## 口播文案\n+(.+?)\n+---\n+## 视频制作建议', text, re.DOTALL)
    if not match:
        # 兜底：尝试从正文开始提取
        match = re.search(r'## 口播文案\n+(.+)', text, re.DOTALL)
    content = match.group(1).strip() if match else text

    elements = []
    current_paragraph = []

    def flush_paragraph():
        if current_paragraph:
            text = ' '.join(current_paragraph).strip()
            if text:
                elements.append(('p', text))
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
        else:
            # 段落内容：合并到当前段落
            current_paragraph.append(line)

    flush_paragraph()
    return elements


def clean_performance_marks(text: str) -> str:
    """去除语气标注，保留口语感。"""
    # 去除括号内的语气标注
    text = re.sub(r'（停顿\d*\.?\d*秒）', '', text)
    text = re.sub(r'（停顿）', '', text)
    text = re.sub(r'（放慢语速）', '', text)
    text = re.sub(r'（笑）', '', text)
    text = re.sub(r'（压低声音）', '', text)
    text = re.sub(r'（提高语调）', '', text)
    return text.strip()


def inline_bold(text: str) -> str:
    """将 **text** 转为 <strong>。"""
    return re.sub(r'\*\*(.+?)\*\*', r'<strong style="font-weight: bold; color: #1a1a1a;">\1</strong>', text)


def split_sentences(text: str) -> list:
    """按中文标点拆分句子，保留标点。"""
    # 先按句号、问号、感叹号切分
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


def render_paragraph(text: str, colors: dict) -> str:
    """渲染一个正文段落。"""
    text = clean_performance_marks(text)
    if not text:
        return ''
    text = inline_bold(text)
    return (
        f'<p style="font-size: 16px; line-height: 1.8; color: {colors["text_body"]}; '
        f'margin: 18px 0; text-align: justify;">{text}</p>'
    )


def render_scene_annotation(scene_id: int, scene_title: str) -> str:
    """渲染图片文字标注。"""
    return (
        f'<p style="font-size: 14px; line-height: 2.0; color: #a39e99; '
        f'margin: 25px 0; text-align: center; font-style: italic;">'
        f'[图片{scene_id}：{scene_title}]</p>'
    )


def build_html(elements: list, scenes: list, title: str, style_name: str) -> str:
    """构建头条号 HTML。"""
    # 现代简约配色
    colors = {
        'text_main': '#1a1a1a',
        'text_body': '#3f3f3f',
        'text_secondary': '#888888',
        'accent': '#2c5aa0',
        'bg': '#ffffff',
        'quote_bg': '#f5f7fa',
        'quote_border': '#2c5aa0',
        'divider': '#e8e8e8',
    }

    body_parts = []

    # 主标题
    body_parts.append(
        f'<h1 style="font-size: 24px; font-weight: bold; color: {colors["text_main"]}; '
        f'margin: 20px 0 25px; padding-bottom: 12px; border-bottom: 2px solid {colors["accent"]}; line-height: 1.4;">'
        f'{title}</h1>'
    )

    # 副标题/引导语
    body_parts.append(
        f'<p style="font-size: 14px; line-height: 1.7; color: {colors["text_secondary"]}; margin: 0 0 25px;">'
        f'作者：尤瓦尔·赫拉利 &nbsp;|&nbsp; 出处：《人类简史》第九章</p>'
    )

    # 场景标注插入规则：根据段落文本关键词匹配
    scene_keywords = [
        (1, '视频封面标题', None),  # 放在开头主标题后，已单独处理
        (2, '文化符号拼贴', ['文化到底是什么', '是长城', '是京剧']),
        (3, '旧观点：文化是固定本质', ['文化就是一种本质', '千百年来基本不变']),
        (4, '文化是角色扮演游戏', ['角色扮演游戏']),
        (5, '矛盾的剧本', ['中世纪欧洲的贵族']),
        (6, '自由 vs 平等', ['自由和 equality', '自由和equality']),
        (7, '矛盾是feature不是bug', ['这不是 bug', '这是 feature', '文化的引擎']),
        (8, '不协和音推动音乐', ['音乐里的不协和音']),
        (9, '历史方向提问', ['文化是流动的', '随机流动']),
        (10, '间谍卫星视角', ['间谍卫星']),
        (11, '文明数量递减时间线', ['公元前一万年', '公元前两千年', '只剩几百个']),
        (12, '亚非世界扩张地图', ['公元1450年', '九成人类', '亚非世界']),
        (13, '分久必合金句', ['合久必分只是一时', '改写了《三国演义》']),
        (14, '三类推动者', ['三类人', '商人、征服者、先知']),
        (15, '货币秩序打破边界', ['商人用货币']),
        (16, '帝国秩序扩张', ['征服者用帝国']),
        (17, '宗教秩序普世价值', ['先知则用宗教']),
        (18, '纯正文化是幻觉', ['可能有人要反驳', '纯正文化是幻觉']),
        (19, '哥伦布大交换', ['意大利面里的西红柿', '马铃薯、辣椒、可可']),
        (20, '文化如河流结尾', ['文化更像一条河', '文化是一条河']),
    ]

    inserted_scenes = set()

    def insert_scene_annotation(scene_id: int, scene_title: str):
        if scene_id in inserted_scenes:
            return
        inserted_scenes.add(scene_id)
        body_parts.append(render_scene_annotation(scene_id, scene_title))

    # 第一个场景标注放在引导语后面
    insert_scene_annotation(1, '视频封面标题')

    for elem_type, elem_text in elements:
        if elem_type == 'h2':
            body_parts.append(
                f'<h2 style="font-size: 18px; font-weight: bold; color: {colors["accent"]}; '
                f'margin: 25px 0 15px; padding-left: 12px; border-left: 3px solid {colors["accent"]}; line-height: 1.4;">'
                f'{elem_text}</h2>'
            )
        elif elem_type == 'hr':
            body_parts.append(
                f'<hr style="border: none; border-top: 1px solid {colors["divider"]}; margin: 30px 0;">'
            )
        else:
            matched_scenes = find_matching_scenes(elem_text, scene_keywords, inserted_scenes)

            if not matched_scenes:
                # 没有匹配场景，直接输出段落
                p_html = render_paragraph(elem_text, colors)
                if p_html:
                    body_parts.append(p_html)
            elif len(matched_scenes) == 1:
                # 只匹配一个场景，输出段落后插入标注
                p_html = render_paragraph(elem_text, colors)
                if p_html:
                    body_parts.append(p_html)
                scene_id, scene_title, _ = matched_scenes[0]
                insert_scene_annotation(scene_id, scene_title)
            else:
                # 匹配多个场景：按句子拆分段落，为每个句子匹配场景
                # 确保图片标注之间至少间隔一个句子（文字）
                sentences = split_sentences(elem_text)
                for sentence in sentences:
                    p_html = render_paragraph(sentence, colors)
                    if p_html:
                        body_parts.append(p_html)

                    # 为当前句子找匹配场景，优先 scene_id 小的未插入场景
                    sentence_scenes = find_matching_scenes(sentence, scene_keywords, inserted_scenes)
                    if sentence_scenes:
                        scene_id, scene_title, _ = sentence_scenes[0]
                        insert_scene_annotation(scene_id, scene_title)

    # 兜底：如果还有场景没插入，必须确保每张图都用上
    # 在文章末尾追加未插入的场景标注，但用过渡文字隔开避免连续
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
                f'margin: 15px 0; text-align: center;">（以下为配套画面）</p>'
            )
            insert_scene_annotation(scene_id, scene_title)

    # 结尾引导
    body_parts.append(
        f'<hr style="border: none; border-top: 1px solid {colors["divider"]}; margin: 30px 0;">'
    )
    body_parts.append(
        f'<p style="font-size: 14px; line-height: 1.7; color: {colors["text_secondary"]}; margin: 20px 0; text-align: center;">'
        f'— 长按二维码，关注更多精彩 —</p>'
    )

    body_html = '\n'.join(body_parts)

    html = f'''<!--
  排版风格：{style_name}
  目标平台：今日头条号
  生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
  使用说明：
    1. 全选复制 → 粘贴到今日头条号编辑器
    2. 将 [图片X：...] 文字标注替换为实际配图
-->
<section style="padding: 16px; font-family: -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Helvetica, Segoe UI, Arial, Roboto, 'PingFang SC', 'miui', 'Hiragino Sans GB', 'Microsoft Yahei', sans-serif; background: #ffffff; color: #3f3f3f;">
{body_html}
</section>'''

    return html


def main():
    base_dir = Path('/Users/chouchou/Documents/Obsidian Vault/成长计划/图文发布/读书系列/人类简史/09')
    md_path = base_dir / 'chapter-09-script.md'
    scenes_path = base_dir / 'visual-scenes.json'
    output_path = base_dir / 'chapter-09-script_toutiao.html'

    md_text = md_path.read_text(encoding='utf-8')
    scenes_data = json.loads(scenes_path.read_text(encoding='utf-8'))
    scenes = scenes_data.get('prompts', [])

    title = scenes_data.get('meta', {}).get('title', '《人类简史》第九章：历史的方向')
    style_name = '现代简约'

    elements = parse_markdown(md_text)
    html = build_html(elements, scenes, title, style_name)

    output_path.write_text(html, encoding='utf-8')
    print(f'已生成：{output_path}')


if __name__ == '__main__':
    main()
