#!/usr/bin/env python3
"""
Book Reader HTML Generator
将已完成 book-master 工作流的书籍项目生成为交互式 HTML 阅读页面。

用法:
    python3 generate.py /path/to/book-project

输出:
    {book-path}/reader/
    ├── index.html      # 入口：书籍概览 + 章节导航
    ├── chapter-XX.html # 每章一个阅读页面
    └── ...
"""

import sys
import os
import re
import json
import html as html_module
from pathlib import Path
from datetime import datetime

# === 配置 ===
CONCEPT_COLORS = [
    "#e8d5c4", "#d4e5d7", "#d5dce8", "#e8d5e0",
    "#e0e8d5", "#d5e0e8", "#e8e0d5", "#d5e8e0",
    "#e0d5e8", "#d8e8d5", "#e8d8d5", "#d5d8e8",
]

CSS_STYLES = """
:root {
  --bg: #faf9f7; --text: #2d2d2d; --text-secondary: #666;
  --border: #e0ddd8; --sidebar-bg: #f5f3f0; --card-bg: #fff;
  --accent: #c75b39; --progress: #c75b39; --tooltip-bg: #2d2d2d;
  --tooltip-text: #fff;
}
@media (prefers-color-scheme: dark) {
  :root { --bg: #1a1a1a; --text: #e0e0e0; --text-secondary: #999;
    --border: #333; --sidebar-bg: #222; --card-bg: #2a2a2a; }
}
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family:"Noto Serif SC","PingFang SC","Microsoft YaHei",serif;
  background:var(--bg); color:var(--text); line-height:1.8; }

/* Header */
.header { position:fixed; top:0; left:0; right:0; height:52px;
  background:var(--card-bg); border-bottom:1px solid var(--border);
  display:flex; align-items:center; justify-content:space-between;
  padding:0 20px; z-index:100; }
.book-title { font-size:14px; font-weight:600; color:var(--accent); white-space:nowrap; overflow:hidden; text-overflow:ellipsis; max-width:40%; }
.chapter-nav { display:flex; gap:6px; align-items:center; overflow-x:auto; scrollbar-width:none; max-width:55%; }
.chapter-nav::-webkit-scrollbar { display:none; }
.chapter-nav a { padding:4px 10px; border-radius:4px; font-size:12px;
  text-decoration:none; color:var(--text-secondary); border:1px solid var(--border);
  transition:all 0.2s; white-space:nowrap; flex-shrink:0; }
.chapter-nav a:hover, .chapter-nav a.active { background:var(--accent); color:#fff; border-color:var(--accent); }

/* Progress */
.progress-bar { position:fixed; top:52px; left:0; right:0; height:2px; background:var(--border); z-index:99; }
.progress-bar .fill { height:100%; background:var(--progress); width:0%; transition:width 0.1s; }

/* Main layout */
.main { display:grid; grid-template-columns:1fr 380px; margin-top:54px; min-height:calc(100vh - 54px); }

/* Content */
.content { padding:40px 48px; max-width:800px; margin:0 auto; }
.content h1 { font-size:28px; margin-bottom:8px; }
.content h2 { font-size:20px; margin:32px 0 16px; padding-bottom:8px; border-bottom:1px solid var(--border); }
.content h3 { font-size:16px; margin:24px 0 12px; color:var(--text-secondary); }
.content p { margin-bottom:16px; text-align:justify; }
.content blockquote { margin:16px 0; padding:12px 20px; border-left:3px solid var(--accent);
  background:var(--sidebar-bg); font-style:italic; color:var(--text-secondary); }
.content ul, .content ol { margin:12px 0 12px 24px; }
.content li { margin-bottom:6px; }
.content hr { border:none; border-top:1px solid var(--border); margin:24px 0; }
.content table { width:100%; border-collapse:collapse; margin:16px 0; font-size:14px; }
.content th, .content td { border:1px solid var(--border); padding:8px 12px; text-align:left; }
.content th { background:var(--sidebar-bg); font-weight:600; }
.content img { max-width:100%; height:auto; display:block; margin:16px auto; }

/* Concept highlights */
mark.concept { background:linear-gradient(transparent 60%, var(--hl) 60%);
  cursor:pointer; border-radius:2px; padding:0 2px; transition:background 0.2s; }
mark.concept:hover { background:var(--hl); }
mark.concept.active { background:var(--accent) !important; color:#fff; }

/* Tooltip */
.tooltip { position:fixed; background:var(--tooltip-bg); color:var(--tooltip-text);
  padding:10px 14px; border-radius:6px; font-size:13px; line-height:1.6;
  max-width:320px; pointer-events:none; opacity:0; transition:opacity 0.2s;
  z-index:200; box-shadow:0 4px 12px rgba(0,0,0,0.15); }
.tooltip.visible { opacity:1; }

/* Sidebar */
.sidebar { background:var(--sidebar-bg); border-left:1px solid var(--border);
  padding:20px; overflow-y:auto; height:calc(100vh - 54px); position:sticky; top:54px; }
.sidebar-title { font-size:14px; font-weight:600; margin-bottom:16px;
  color:var(--text-secondary); display:flex; align-items:center; gap:6px; }

/* Concept cards */
.concept-card { background:var(--card-bg); border-radius:8px; padding:14px 16px;
  margin-bottom:10px; border:1px solid var(--border); transition:all 0.2s; cursor:pointer; }
.concept-card:hover { border-color:var(--accent); transform:translateX(-2px); }
.concept-card.active { border-color:var(--accent); box-shadow:0 0 0 2px rgba(199,91,57,0.15); }
.concept-card .card-title { font-size:14px; font-weight:600; margin-bottom:6px; }
.concept-card .card-layman { font-size:12px; color:var(--text-secondary); line-height:1.7; }
.concept-card .card-details { display:none; margin-top:10px; padding-top:10px;
  border-top:1px dashed var(--border); font-size:12px; color:var(--text-secondary); }
.concept-card .card-details.visible { display:block; }
.concept-card .detail-label { font-weight:600; color:var(--text); margin:8px 0 4px; }

/* Footer nav */
.footer-nav { display:flex; justify-content:space-between; align-items:center;
  padding:20px 48px; border-top:1px solid var(--border); max-width:800px; margin:0 auto; }
.footer-nav a { color:var(--accent); text-decoration:none; font-size:14px; }
.footer-nav a:hover { text-decoration:underline; }

/* Index page */
.index-page { max-width:900px; margin:0 auto; padding:60px 24px; }
.index-page h1 { font-size:32px; margin-bottom:8px; }
.index-page .subtitle { color:var(--text-secondary); margin-bottom:32px; }
.index-page .chapter-list { display:grid; gap:8px; }
.index-page .chapter-item { display:flex; align-items:center; gap:16px;
  padding:14px 20px; background:var(--card-bg); border:1px solid var(--border);
  border-radius:8px; text-decoration:none; color:var(--text); transition:all 0.2s; }
.index-page .chapter-item:hover { border-color:var(--accent); transform:translateX(4px); }
.index-page .chapter-num { font-size:12px; color:var(--accent); font-weight:600; min-width:32px; }
.index-page .chapter-title { flex:1; font-size:15px; }
.index-page .chapter-arrow { color:var(--text-secondary); font-size:12px; }
.index-page .section-title { font-size:18px; margin:32px 0 16px; padding-bottom:8px;
  border-bottom:1px solid var(--border); }

/* Responsive */
@media (max-width:1024px) {
  .main { grid-template-columns:1fr; }
  .sidebar { display:none; }
  .content { padding:24px; }
}
"""

JS_SCRIPT = """
(function() {
  const tooltip = document.getElementById('tooltip');
  const progressFill = document.getElementById('progressFill');
  const conceptData = window.__CONCEPTS__ || {};

  // Tooltip
  document.querySelectorAll('mark.concept').forEach(mark => {
    const name = mark.dataset.concept;
    const c = conceptData[name];
    if (!c) return;
    mark.addEventListener('mouseenter', e => {
      tooltip.textContent = (c.layman || c.definition || c.explanation || '').slice(0, 200);
      tooltip.classList.add('visible');
      positionTooltip(e);
    });
    mark.addEventListener('mousemove', positionTooltip);
    mark.addEventListener('mouseleave', () => tooltip.classList.remove('visible'));
    mark.addEventListener('click', () => activateConcept(name));
  });

  function positionTooltip(e) {
    let x = e.clientX + 12, y = e.clientY - 12;
    if (x + 320 > window.innerWidth) x = e.clientX - 332;
    if (y < 10) y = e.clientY + 20;
    tooltip.style.left = x + 'px';
    tooltip.style.top = y + 'px';
  }

  function activateConcept(name) {
    document.querySelectorAll('mark.concept').forEach(m => m.classList.remove('active'));
    document.querySelectorAll('.concept-card').forEach(c => c.classList.remove('active'));
    document.querySelectorAll(`mark.concept[data-concept="${name}"]`).forEach(m => m.classList.add('active'));
    const card = document.querySelector(`.concept-card[data-concept="${name}"]`);
    if (card) {
      card.classList.add('active');
      card.scrollIntoView({ behavior:'smooth', block:'center' });
      card.querySelector('.card-details')?.classList.add('visible');
    }
  }

  // Card click
  document.querySelectorAll('.concept-card').forEach(card => {
    card.addEventListener('click', () => {
      const name = card.dataset.concept;
      const details = card.querySelector('.card-details');
      const isVisible = details?.classList.contains('visible');
      document.querySelectorAll('.concept-card .card-details').forEach(d => d.classList.remove('visible'));
      if (!isVisible) {
        details?.classList.add('visible');
        activateConcept(name);
      }
    });
  });

  // Progress bar
  const content = document.getElementById('content');
  if (content) {
    window.addEventListener('scroll', () => {
      const scrollTop = window.scrollY;
      const docHeight = document.documentElement.scrollHeight - window.innerHeight;
      progressFill.style.width = Math.min(100, Math.max(0, (scrollTop / docHeight) * 100)) + '%';
    });
  }

  // Scroll sync: highlight concepts in viewport
  const paragraphs = document.querySelectorAll('#content p, #content h2, #content h3');
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const marks = entry.target.querySelectorAll('mark.concept');
        document.querySelectorAll('.concept-card').forEach(c => c.classList.remove('active'));
        marks.forEach(m => {
          const card = document.querySelector(`.concept-card[data-concept="${m.dataset.concept}"]`);
          if (card) card.classList.add('active');
        });
      }
    });
  }, { rootMargin: '-30% 0px -50% 0px', threshold: 0 });
  paragraphs.forEach(p => observer.observe(p));
})();
"""


def parse_concepts_from_report(report_path: str) -> dict:
    """从精读报告中提取关键概念。"""
    concepts = {}
    try:
        with open(report_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"  Warning: cannot read {report_path}: {e}")
        return concepts

    # 找到 "## 关键概念与定义" 部分
    section_match = re.search(r'## 关键概念与定义\s*\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
    if not section_match:
        return concepts

    section = section_match.group(1)

    # 匹配每个概念块
    concept_blocks = re.split(r'\n### 概念\d+[:：]\s*', section)
    for block in concept_blocks[1:]:  # 第一个是空或标题前内容
        lines = block.strip().split('\n')
        if not lines:
            continue

        title_line = lines[0].strip()
        concept = {
            'title': title_line,
            'term': '',
            'definition': '',
            'explanation': '',
            'layman': '',
            'related': '',
        }

        current_key = None
        for line in lines[1:]:
            line = line.strip()
            if line.startswith('- **术语名称**：') or line.startswith('- **术语名称**:'):
                concept['term'] = re.sub(r'^-\s*\*\*术语名称\*\*[:：]\s*', '', line)
            elif line.startswith('- **文中定义**：') or line.startswith('- **文中定义**:'):
                concept['definition'] = re.sub(r'^-\s*\*\*文中定义\*\*[:：]\s*', '', line)
            elif line.startswith('- **解释**：') or line.startswith('- **解释**:'):
                concept['explanation'] = re.sub(r'^-\s*\*\*解释\*\*[:：]\s*', '', line)
            elif line.startswith('- **通俗解释**：') or line.startswith('- **通俗解释**:'):
                concept['layman'] = re.sub(r'^-\s*\*\*通俗解释\*\*[:：]\s*', '', line)
            elif line.startswith('- **关联概念**：') or line.startswith('- **关联概念**:'):
                concept['related'] = re.sub(r'^-\s*\*\*关联概念\*\*[:：]\s*', '', line)

        # 使用 title 作为 key
        key = title_line.split('(')[0].strip() if '(' in title_line else title_line
        if not key:
            key = concept['term'].split('/')[0].strip() if concept['term'] else title_line

        # 尝试提取中文名称
        cn_name = ''
        if concept['term']:
            parts = concept['term'].split('/')
            cn_name = parts[0].strip()
        if not cn_name:
            cn_name = key

        concept['key'] = cn_name
        concepts[cn_name] = concept

    return concepts


def annotate_text(text: str, concepts: dict) -> str:
    """在原文中标注概念。"""
    if not concepts:
        return text

    # 按名称长度降序排列（优先匹配较长的术语）
    sorted_keys = sorted(concepts.keys(), key=len, reverse=True)

    # 为每个概念分配颜色
    color_map = {}
    for i, key in enumerate(sorted_keys):
        color_map[key] = CONCEPT_COLORS[i % len(CONCEPT_COLORS)]

    # 将原文分段处理（按段落）
    paragraphs = text.split('\n\n')
    annotated_paragraphs = []

    for para in paragraphs:
        if not para.strip():
            annotated_paragraphs.append(para)
            continue

        # 跳过 Markdown 标题和代码块
        if para.strip().startswith('#') or para.strip().startswith('```'):
            annotated_paragraphs.append(para)
            continue

        annotated = para
        # 对每个概念，在段落中标注（只标第一次出现）
        for key in sorted_keys:
            if not key or len(key) < 2:
                continue

            # 检查是否已包含在 mark 标签内
            # 使用简单的字符串替换，但避免替换已标记的内容
            color = color_map[key]
            pattern = re.compile(re.escape(key))

            # 找到第一个不在 mark 标签内的匹配
            def replace_first(match):
                pos = match.start()
                # 检查是否在 mark 标签内（简单检查：前面有 <mark 后面有 >）
                before = annotated[:pos]
                after = annotated[pos:]
                # 如果前面有未闭合的 <mark...> 标签，跳过
                open_tags = before.count('<mark') - before.count('</mark>')
                if open_tags > 0:
                    return match.group(0)
                return f'<mark class="concept" data-concept="{key}" style="--hl:{color}">{match.group(0)}</mark>'

            annotated = pattern.sub(replace_first, annotated, count=1)

        annotated_paragraphs.append(annotated)

    return '\n\n'.join(annotated_paragraphs)


def markdown_to_html(md: str) -> str:
    """简单的 Markdown 转 HTML。"""
    text = md

    # 代码块
    text = re.sub(r'```(\w+)?\n(.*?)```', lambda m: f'<pre><code>{html_module.escape(m.group(2))}</code></pre>', text, flags=re.DOTALL)

    # 行内代码
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)

    # 标题
    text = re.sub(r'^###### (.+)$', r'<h6>\1</h6>', text, flags=re.MULTILINE)
    text = re.sub(r'^##### (.+)$', r'<h5>\1</h5>', text, flags=re.MULTILINE)
    text = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', text, flags=re.MULTILINE)
    text = re.sub(r'^### (.+)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.+)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'^# (.+)$', r'<h1>\1</h1>', text, flags=re.MULTILINE)

    # 粗体、斜体
    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)

    # 引用块
    def blockquote_repl(m):
        lines = m.group(1).strip().split('\n')
        inner = '\n'.join(line.lstrip('>').lstrip() for line in lines)
        return f'<blockquote>{markdown_to_html(inner)}</blockquote>'

    text = re.sub(r'(^> .+(?:\n^> .+)*)', blockquote_repl, text, flags=re.MULTILINE)

    # 链接
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)

    # 图片
    text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<img alt="\1" src="\2">', text)

    # 水平线
    text = re.sub(r'^---+\s*$', '<hr>', text, flags=re.MULTILINE)

    # 表格（简单处理）
    lines = text.split('\n')
    new_lines = []
    in_table = False
    table_rows = []

    for line in lines:
        if '|' in line and not line.strip().startswith('<'):
            cells = [c.strip() for c in line.split('|')]
            cells = [c for c in cells if c]  # 去除空
            if cells and all(c.replace('-', '').replace(':', '') == '' for c in cells):
                # 分隔行，跳过
                continue
            if cells:
                table_rows.append(cells)
                in_table = True
        else:
            if in_table and table_rows:
                # 输出表格
                new_lines.append('<table>')
                for i, row in enumerate(table_rows):
                    tag = 'th' if i == 0 else 'td'
                    new_lines.append('<tr>' + ''.join(f'<{tag}>{markdown_to_html(c)}</{tag}>' for c in row) + '</tr>')
                new_lines.append('</table>')
                table_rows = []
                in_table = False
            new_lines.append(line)

    if in_table and table_rows:
        new_lines.append('<table>')
        for i, row in enumerate(table_rows):
            tag = 'th' if i == 0 else 'td'
            new_lines.append('<tr>' + ''.join(f'<{tag}>{markdown_to_html(c)}</{tag}>' for c in row) + '</tr>')
        new_lines.append('</table>')

    text = '\n'.join(new_lines)

    # 列表
    text = re.sub(r'(^\s*[-*+] .+(?:\n\s*[-*+] .+)*)', lambda m: '<ul>' + ''.join(f'<li>{line.lstrip().lstrip("-*+ ")}</li>' for line in m.group(1).strip().split('\n')) + '</ul>', text, flags=re.MULTILINE)

    # 段落
    paragraphs = text.split('\n\n')
    new_paragraphs = []
    for p in paragraphs:
        p = p.strip()
        if not p:
            continue
        if p.startswith('<') and not p.startswith('<mark'):
            new_paragraphs.append(p)
        else:
            new_paragraphs.append(f'<p>{p}</p>')
    text = '\n'.join(new_paragraphs)

    return text


def generate_chapter_html(chapter_file: str, report_file: str, book_title: str,
                          chapter_title: str, prev_info: dict, next_info: dict,
                          all_chapters: list) -> str:
    """生成单章 HTML。"""
    # 读取原文
    with open(chapter_file, 'r', encoding='utf-8') as f:
        md_text = f.read()

    # 移除 frontmatter
    md_text = re.sub(r'^---\s*\n.*?\n---\s*\n', '', md_text, flags=re.DOTALL, count=1)

    # 提取概念
    concepts = parse_concepts_from_report(report_file) if os.path.exists(report_file) else {}
    print(f"    Extracted {len(concepts)} concepts")

    # 标注原文
    annotated_md = annotate_text(md_text, concepts)

    # 转 HTML
    html_content = markdown_to_html(annotated_md)

    # 生成概念卡片 HTML
    concept_cards_html = ''
    for i, (key, c) in enumerate(concepts.items()):
        color = CONCEPT_COLORS[i % len(CONCEPT_COLORS)]
        layman = c.get('layman', '')
        definition = c.get('definition', '')
        explanation = c.get('explanation', '')
        related = c.get('related', '')

        details = []
        if definition:
            details.append(f'<div class="detail-label">文中定义</div><div>{html_module.escape(definition[:300])}</div>')
        if explanation:
            details.append(f'<div class="detail-label">解释</div><div>{html_module.escape(explanation[:300])}</div>')
        if related:
            details.append(f'<div class="detail-label">关联概念</div><div>{html_module.escape(related[:200])}</div>')

        details_html = '\n'.join(details)

        concept_cards_html += f'''
<div class="concept-card" data-concept="{key}" style="border-left:3px solid {color}">
  <div class="card-title">{html_module.escape(key)}</div>
  <div class="card-layman">{html_module.escape(layman[:250] if layman else (definition[:200] if definition else ''))}</div>
  <div class="card-details">{details_html}</div>
</div>
'''

    if not concept_cards_html:
        concept_cards_html = '<div style="color:var(--text-secondary);font-size:12px;padding:20px;text-align:center;">本章暂无提取的概念</div>'

    # 生成顶部章节导航
    nav_html = ''
    for ch in all_chapters:
        num = ch['num']
        title = ch['title'][:8] + '...' if len(ch['title']) > 8 else ch['title']
        active = ' active' if ch['title'] == chapter_title else ''
        nav_html += f'<a href="{ch["file"]}" class="{active}">{num}</a>'

    # 底部导航
    prev_link = f'<a href="{prev_info["file"]}">&larr; {html_module.escape(prev_info["title"][:20])}</a>' if prev_info else '<span></span>'
    next_link = f'<a href="{next_info["file"]}">{html_module.escape(next_info["title"][:20])} &rarr;</a>' if next_info else '<span></span>'

    # 概念 JSON
    concept_json = json.dumps(concepts, ensure_ascii=False)

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html_module.escape(book_title)} - {html_module.escape(chapter_title)}</title>
<style>{CSS_STYLES}</style>
</head>
<body>
<header class="header">
  <div class="book-title">📖 {html_module.escape(book_title)}</div>
  <nav class="chapter-nav">{nav_html}</nav>
</header>
<div class="progress-bar"><div class="fill" id="progressFill"></div></div>
<div class="main">
  <article class="content" id="content">
    <h1>{html_module.escape(chapter_title)}</h1>
{html_content}
  </article>
  <aside class="sidebar" id="sidebar">
    <div class="sidebar-title">💡 本章概念 ({len(concepts)}个)</div>
    <div id="conceptList">
{concept_cards_html}
    </div>
  </aside>
</div>
<nav class="footer-nav">
  {prev_link}
  <span style="color:var(--text-secondary);font-size:12px;">{html_module.escape(chapter_title)}</span>
  {next_link}
</nav>
<div class="tooltip" id="tooltip"></div>
<script>
window.__CONCEPTS__ = {concept_json};
{JS_SCRIPT}
</script>
</body>
</html>'''


def generate_index_html(book_title: str, chapters: list) -> str:
    """生成入口页面。"""
    chapter_list = ''
    for i, ch in enumerate(chapters):
        chapter_list += f'''
<a href="{ch["file"]}" class="chapter-item">
  <span class="chapter-num">{ch["num"]}</span>
  <span class="chapter-title">{html_module.escape(ch["title"])}</span>
  <span class="chapter-arrow">&rarr;</span>
</a>
'''

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html_module.escape(book_title)} - 阅读</title>
<style>{CSS_STYLES}
.index-page {{ padding-top: 80px !important; }}
</style>
</head>
<body>
<header class="header">
  <div class="book-title">📖 {html_module.escape(book_title)}</div>
  <nav class="chapter-nav"></nav>
</header>
<div class="index-page">
  <h1>{html_module.escape(book_title)}</h1>
  <div class="subtitle">交互式阅读页面 &mdash; 左栏原文，右栏概念</div>

  <div class="section-title">📑 章节列表</div>
  <div class="chapter-list">
{chapter_list}
  </div>

  <div style="margin-top:48px;padding-top:24px;border-top:1px solid var(--border);color:var(--text-secondary);font-size:12px;text-align:center;">
    Generated by book-reader skill &middot; {datetime.now().strftime('%Y-%m-%d')}
  </div>
</div>
</body>
</html>'''


def main():
    if len(sys.argv) < 2:
        print("用法: python3 generate.py /path/to/book-project")
        sys.exit(1)

    book_path = Path(sys.argv[1]).resolve()
    chapters_dir = book_path / 'chapters'
    reports_dir = book_path / 'reports'
    reader_dir = book_path / 'reader'

    if not chapters_dir.exists():
        print(f"错误: chapters/ 目录不存在: {chapters_dir}")
        sys.exit(1)

    print(f"📚 书籍路径: {book_path}")
    print(f"📖 章节目录: {chapters_dir}")
    print(f"📊 报告目录: {reports_dir}")
    print()

    # 从 _index.md 或文件名中提取书籍标题和章节顺序
    book_title = book_path.name
    index_file = chapters_dir / '_index.md'

    # 读取章节列表
    chapter_files = sorted([f for f in chapters_dir.iterdir()
                            if f.name.startswith('chapter-') and f.suffix == '.md'])

    if not chapter_files:
        print("错误: 未找到内容章节文件 (chapter-*.md)")
        sys.exit(1)

    # 构建章节信息
    chapters = []
    for i, cf in enumerate(chapter_files):
        # 从文件名提取标题
        title_match = re.match(r'chapter-\d+[-_](.+)\.md', cf.name)
        title = title_match.group(1).replace('_', ' ').replace('-', ' ') if title_match else cf.name

        # 提取章节编号
        num_match = re.match(r'chapter-(\d+)', cf.name)
        num = num_match.group(1) if num_match else str(i + 1)

        # 找到对应的报告文件
        report_file = reports_dir / f"{cf.stem}-report.md"
        if not report_file.exists():
            # 尝试其他命名模式
            alt = reports_dir / f"{cf.stem.replace('_', '_')}-report.md"
            if alt.exists():
                report_file = alt

        chapters.append({
            'file': f"chapter-{num}.html",
            'source': str(cf),
            'report': str(report_file) if report_file.exists() else None,
            'title': title,
            'num': num,
        })

    print(f"找到 {len(chapters)} 个内容章节")
    print()

    # 创建 reader 目录
    reader_dir.mkdir(exist_ok=True)

    # 生成每章 HTML
    for i, ch in enumerate(chapters):
        print(f"  生成章节 {ch['num']}: {ch['title']}")

        prev_info = chapters[i - 1] if i > 0 else None
        next_info = chapters[i + 1] if i < len(chapters) - 1 else None

        prev_dict = {'file': prev_info['file'], 'title': prev_info['title']} if prev_info else None
        next_dict = {'file': next_info['file'], 'title': next_info['title']} if next_info else None

        html = generate_chapter_html(
            ch['source'],
            ch['report'] or '',
            book_title,
            ch['title'],
            prev_dict,
            next_dict,
            [{'num': c['num'], 'title': c['title'], 'file': c['file']} for c in chapters]
        )

        output_file = reader_dir / ch['file']
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"    -> {output_file}")

    # 生成入口页面
    print()
    print("  生成入口页面...")
    index_html = generate_index_html(book_title, chapters)
    index_path = reader_dir / 'index.html'
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_html)
    print(f"    -> {index_path}")

    print()
    print(f"✅ 完成！共生成 {len(chapters)} 章 + 1 入口页面")
    print(f"📂 输出目录: {reader_dir}")
    print(f"🌐 在浏览器中打开: file://{reader_dir}/index.html")


if __name__ == '__main__':
    main()
