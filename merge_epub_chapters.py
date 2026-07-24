#!/usr/bin/env python3
"""
Merge fragmented EPUB xhtml files into logical chapters.
The source EPUB splits each chapter across many small xhtml files;
this script reconstructs full chapters in spine order.
"""

import sys
import os
import re
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup, NavigableString


def html_to_markdown(html_content):
    """Convert EPUB HTML content to clean Markdown text."""
    soup = BeautifulSoup(html_content, 'lxml')

    for tag in soup(['script', 'style', 'nav']):
        tag.decompose()

    def process_element(elem, in_blockquote=False):
        if isinstance(elem, NavigableString):
            text = str(elem)
            text = text.replace('\r\n', ' ').replace('\n', ' ')
            return text

        tag_name = elem.name
        if not tag_name:
            return ''

        if tag_name in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            level = int(tag_name[1])
            text = elem.get_text(strip=True)
            if text:
                return '\n' + '#' * level + ' ' + text + '\n\n'
            return ''

        if tag_name == 'p':
            text = get_inline_text(elem)
            if text.strip():
                return text.strip() + '\n\n'
            return ''

        if tag_name == 'blockquote':
            text = get_inline_text(elem)
            if text.strip():
                quoted = '\n'.join('> ' + line for line in text.strip().split('\n'))
                return quoted + '\n\n'
            return ''

        if tag_name == 'li':
            text = get_inline_text(elem)
            if text.strip():
                return '- ' + text.strip() + '\n'
            return ''

        if tag_name in ('ul', 'ol'):
            result = ''
            for child in elem.children:
                result += process_element(child)
            return result + '\n'

        if tag_name == 'table':
            return process_table(elem)

        if tag_name == 'img':
            alt = elem.get('alt', 'image')
            src = elem.get('src', '')
            return f'![{alt}]({src})\n\n'

        if tag_name == 'a':
            text = get_inline_text(elem)
            href = elem.get('href', '')
            if href.startswith('#') or 'zhu' in href:
                return text
            if text.strip():
                return f'[{text}]({href})'
            return ''

        if tag_name == 'sup':
            return ''

        result = ''
        for child in elem.children:
            result += process_element(child)
        return result

    def get_inline_text(elem):
        result = ''
        for child in elem.children:
            if isinstance(child, NavigableString):
                result += str(child)
            elif child.name == 'br':
                result += '\n'
            elif child.name in ('strong', 'b'):
                result += '**' + get_inline_text(child) + '**'
            elif child.name in ('em', 'i'):
                result += '*' + get_inline_text(child) + '*'
            elif child.name == 'a':
                href = child.get('href', '')
                text = get_inline_text(child)
                if href.startswith('#'):
                    result += text
                else:
                    result += f'[{text}]({href})'
            elif child.name == 'sup':
                result += ''
            elif child.name == 'img':
                alt = child.get('alt', 'image')
                src = child.get('src', '')
                result += f'![{alt}]({src})'
            elif child.name == 'span':
                result += get_inline_text(child)
            else:
                result += get_inline_text(child)
        return result

    def process_table(table):
        rows = []
        for tr in table.find_all('tr'):
            cells = []
            for td in tr.find_all(['td', 'th']):
                cells.append(td.get_text(strip=True))
            if cells:
                rows.append(cells)

        if not rows:
            return ''

        max_cols = max(len(r) for r in rows)
        for r in rows:
            while len(r) < max_cols:
                r.append('')

        result = []
        for i, row in enumerate(rows):
            result.append('| ' + ' | '.join(row) + ' |')
            if i == 0:
                result.append('|' + '|'.join(['---'] * max_cols) + '|')

        return '\n'.join(result) + '\n\n'

    body = soup.find('body')
    if body:
        md = process_element(body)
    else:
        md = process_element(soup)

    md = re.sub(r'\n{3,}', '\n\n', md)
    md = re.sub(r'[ \t]+\n', '\n', md)
    md = md.strip()

    return md


def is_content_boundary(title):
    """Check if a title marks a logical content boundary (chapter/part)."""
    t = title.lower()
    # Explicitly non-content front/back matter
    non_content = ['封面', '书名', '版权', '目录', '献辞', 'references', 'index', 'bibliography']
    if any(kw in t for kw in non_content):
        return False, 'skip'

    # Content boundaries
    chapter_patterns = [
        r'第[一二三四五六七八九十百千万\d]+章',
        r'第[一二三四五六七八九十百千万\d]+部分',
        r'序言|前言|导言|引言|结论|后记|结语|致谢|附录',
    ]
    for pat in chapter_patterns:
        if re.search(pat, title):
            return True, 'chapter'

    return False, 'continue'


def extract_and_merge(epub_path, output_dir):
    book = epub.read_epub(epub_path)

    title = "Unknown"
    for val in book.get_metadata('DC', 'title'):
        if val and val[0]:
            title = val[0]
            break

    # Build TOC mapping
    toc_map = {}
    for item in book.toc:
        if isinstance(item, epub.Link):
            filename = item.href.split('#')[0]
            toc_map[filename] = item.title

    # id -> filename
    id_to_name = {}
    for item in book.items:
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            id_to_name[item.id] = item.get_name()

    # Ordered docs from spine
    ordered_docs = []
    for spine_item in book.spine:
        doc_id = spine_item[0]
        if doc_id in id_to_name:
            ordered_docs.append(id_to_name[doc_id])

    # Get title for each doc
    def get_doc_title(doc_name):
        # Try TOC
        for fname, tname in toc_map.items():
            if doc_name.endswith(fname):
                return tname
        # Try h1
        for item in book.items:
            if item.get_name() == doc_name:
                html = item.get_content().decode('utf-8', errors='replace')
                soup = BeautifulSoup(html, 'lxml')
                h1 = soup.find('h1')
                if h1:
                    return h1.get_text(strip=True)
                break
        # Default
        return os.path.splitext(os.path.basename(doc_name))[0]

    # Group docs into chapters
    groups = []
    current_group = None

    for doc_name in ordered_docs:
        if not doc_name.endswith(('.html', '.xhtml')):
            continue

        doc_title = get_doc_title(doc_name)
        is_bound, kind = is_content_boundary(doc_title)

        if is_bound:
            if current_group is not None:
                groups.append(current_group)
            current_group = {
                'title': doc_title,
                'files': [doc_name],
                'kind': kind,
            }
        else:
            if current_group is None:
                # Front matter before first boundary -> skip
                current_group = {
                    'title': doc_title,
                    'files': [doc_name],
                    'kind': 'skip',
                }
            elif current_group['kind'] == 'skip':
                # Still front matter
                current_group['files'].append(doc_name)
            else:
                current_group['files'].append(doc_name)

    if current_group is not None:
        groups.append(current_group)

    # Filter out skip groups
    content_groups = [g for g in groups if g['kind'] != 'skip']

    # Write merged chapters
    os.makedirs(output_dir, exist_ok=True)

    written_files = []
    chapter_idx = 0
    front_idx = 0
    back_idx = 0

    for group in content_groups:
        doc_title = group['title']
        lower = doc_title.lower()

        # Determine prefix
        if any(kw in lower for kw in ['前言', '导言', '引言', '序言']):
            front_idx += 1
            prefix = f'front-{front_idx:02d}'
        elif any(kw in lower for kw in ['结论', '后记', '结语', '致谢', '附录']):
            back_idx += 1
            prefix = f'back-{back_idx:02d}'
        else:
            chapter_idx += 1
            prefix = f'chapter-{chapter_idx:02d}'

        out_name = f'{prefix}-{doc_title}.md'
        out_path = os.path.join(output_dir, out_name)

        merged_md = ''
        for doc_name in group['files']:
            for item in book.items:
                if item.get_name() == doc_name:
                    html = item.get_content().decode('utf-8', errors='replace')
                    md = html_to_markdown(html)
                    if md.strip():
                        merged_md += md + '\n\n'
                    break

        merged_md = merged_md.strip()
        if not merged_md:
            continue

        frontmatter = f"""---
title: "{doc_title}"
source: "{os.path.basename(epub_path)}"
level: 1
---

"""
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(frontmatter)
            f.write(merged_md)

        written_files.append(out_name)
        print(f'  Written: {out_name} ({len(merged_md)} chars)')

    # Write index
    index_path = os.path.join(output_dir, '_index.md')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(f'# {title}\n\n')
        f.write(f'## 章节列表\n\n')
        for fname in written_files:
            base = os.path.splitext(fname)[0]
            f.write(f'- [{base}]({fname})\n')

    print(f'\nTotal: {len(written_files)} merged chapters written to {output_dir}')


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: merge_epub_chapters.py <epub-file> <output-dir>')
        sys.exit(1)
    extract_and_merge(sys.argv[1], sys.argv[2])
