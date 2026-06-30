#!/usr/bin/env python3
"""
EPUB to Markdown extractor for book-master workflow.
Converts EPUB HTML chapters to Markdown with YAML frontmatter.
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

    # Remove script and style elements
    for tag in soup(['script', 'style', 'nav']):
        tag.decompose()

    lines = []
    current_paras = []

    def process_element(elem, in_blockquote=False):
        """Recursively process HTML elements."""
        if isinstance(elem, NavigableString):
            text = str(elem)
            # Collapse multiple whitespace but keep newlines for paragraph breaks
            text = text.replace('\r\n', ' ').replace('\n', ' ')
            return text

        tag_name = elem.name
        if not tag_name:
            return ''

        # Headings
        if tag_name in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            level = int(tag_name[1])
            text = elem.get_text(strip=True)
            if text:
                return '\n' + '#' * level + ' ' + text + '\n\n'
            return ''

        # Paragraph
        if tag_name == 'p':
            text = get_inline_text(elem)
            if text.strip():
                return text.strip() + '\n\n'
            return ''

        # Blockquote
        if tag_name == 'blockquote':
            text = get_inline_text(elem)
            if text.strip():
                quoted = '\n'.join('> ' + line for line in text.strip().split('\n'))
                return quoted + '\n\n'
            return ''

        # List items
        if tag_name == 'li':
            text = get_inline_text(elem)
            if text.strip():
                return '- ' + text.strip() + '\n'
            return ''

        # Unordered list
        if tag_name in ('ul', 'ol'):
            result = ''
            for child in elem.children:
                result += process_element(child)
            return result + '\n'

        # Tables - convert to simple markdown
        if tag_name == 'table':
            return process_table(elem)

        # Images
        if tag_name == 'img':
            alt = elem.get('alt', 'image')
            src = elem.get('src', '')
            return f'![{alt}]({src})\n\n'

        # Links - keep as markdown links
        if tag_name == 'a':
            text = get_inline_text(elem)
            href = elem.get('href', '')
            # Skip internal footnote anchors
            if href.startswith('#') or 'zhu' in href:
                return text
            if text.strip():
                return f'[{text}]({href})'
            return ''

        # Superscript (footnotes) - strip them to keep text clean
        if tag_name == 'sup':
            return ''

        # Span, div, section - recurse
        result = ''
        for child in elem.children:
            result += process_element(child)
        return result

    def get_inline_text(elem):
        """Extract inline text from an element, handling formatting."""
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
                result += ''  # Skip footnote refs
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
        """Convert HTML table to Markdown table."""
        rows = []
        for tr in table.find_all('tr'):
            cells = []
            for td in tr.find_all(['td', 'th']):
                cells.append(td.get_text(strip=True))
            if cells:
                rows.append(cells)

        if not rows:
            return ''

        # Find max column count
        max_cols = max(len(r) for r in rows)

        # Pad rows
        for r in rows:
            while len(r) < max_cols:
                r.append('')

        result = []
        for i, row in enumerate(rows):
            result.append('| ' + ' | '.join(row) + ' |')
            if i == 0:
                result.append('|' + '|'.join(['---'] * max_cols) + '|')

        return '\n'.join(result) + '\n\n'

    # Process body content
    body = soup.find('body')
    if body:
        md = process_element(body)
    else:
        md = process_element(soup)

    # Clean up
    md = re.sub(r'\n{3,}', '\n\n', md)  # Collapse multiple blank lines
    md = re.sub(r'[ \t]+\n', '\n', md)  # Remove trailing spaces
    md = md.strip()

    return md


def extract_epub(epub_path, output_dir):
    """Extract EPUB to Markdown chapters."""
    book = epub.read_epub(epub_path)

    # Get book title
    title = "Unknown"
    for val in book.get_metadata('DC', 'title'):
        if val and val[0]:
            title = val[0]
            break

    # Build TOC mapping: filename -> title
    toc_map = {}
    toc_order = []
    for item in book.toc:
        if isinstance(item, epub.Link):
            href = item.href
            filename = href.split('#')[0]
            toc_map[filename] = item.title
            toc_order.append((filename, item.title))

    # Build spine to filename mapping
    spine_files = []
    for item in book.items:
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            spine_files.append(item)

    # Create id -> filename mapping
    id_to_name = {}
    for item in book.items:
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            id_to_name[item.id] = item.get_name()

    # Build ordered list of document files from spine
    ordered_docs = []
    for spine_item in book.spine:
        doc_id = spine_item[0]
        if doc_id in id_to_name:
            name = id_to_name[doc_id]
            ordered_docs.append(name)

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Classify and name files
    file_entries = []

    # Build filename -> TOC title mapping for spine docs
    for i, doc_name in enumerate(ordered_docs):
        # Skip non-content docs (CSS, etc.)
        if not doc_name.endswith(('.html', '.xhtml')):
            continue

        # Get TOC title
        toc_title = None
        for fname, tname in toc_map.items():
            if doc_name.endswith(fname):
                toc_title = tname
                break

        # If no TOC match, extract from content
        if not toc_title:
            for item in book.items:
                if item.get_name() == doc_name:
                    html = item.get_content().decode('utf-8', errors='replace')
                    soup = BeautifulSoup(html, 'lxml')
                    h1 = soup.find('h1')
                    if h1:
                        toc_title = h1.get_text(strip=True)
                    break

        # Default title
        if not toc_title:
            base = os.path.splitext(os.path.basename(doc_name))[0]
            toc_title = base

        file_entries.append((doc_name, toc_title, i))

    # Generate output filenames
    chapter_idx = 0
    front_idx = 0
    back_idx = 0

    written_files = []

    for doc_name, toc_title, spine_pos in file_entries:
        # Determine prefix based on TOC classification
        is_front = False
        is_back = False
        is_chapter = False

        # Check TOC title patterns
        lower_title = toc_title.lower()
        if any(kw in lower_title for kw in ['版权', '目录', '封面', '献辞', '书名']):
            is_front = True
        elif any(kw in toc_title for kw in ['参考文献', '索引']):
            is_back = True
        elif toc_title.startswith('第') and '章' in toc_title:
            is_chapter = True
        elif any(kw in lower_title for kw in ['引言', '前言', '序', '结论', '后记', '致谢', '译后记', '附录']):
            # These are content chapters that should be read
            is_chapter = True
        elif spine_pos < len(file_entries) * 0.25:
            is_front = True
        elif spine_pos > len(file_entries) * 0.75:
            is_back = True
        else:
            is_chapter = True

        if is_front:
            front_idx += 1
            out_name = f"front-{front_idx:02d}-{toc_title}.md"
        elif is_back:
            back_idx += 1
            out_name = f"back-{back_idx:02d}-{toc_title}.md"
        elif is_chapter:
            chapter_idx += 1
            out_name = f"chapter-{chapter_idx:02d}-{toc_title}.md"
        else:
            chapter_idx += 1
            out_name = f"chapter-{chapter_idx:02d}-{toc_title}.md"

        # Extract and convert content
        for item in book.items:
            if item.get_name() == doc_name:
                html = item.get_content().decode('utf-8', errors='replace')
                md = html_to_markdown(html)

                # Build YAML frontmatter
                frontmatter = f"""---
title: "{toc_title}"
source: "{os.path.basename(epub_path)}"
level: 1
---

"""
                # Write file
                out_path = os.path.join(output_dir, out_name)
                with open(out_path, 'w', encoding='utf-8') as f:
                    f.write(frontmatter)
                    f.write(md)

                written_files.append(out_name)
                print(f"  Written: {out_name} ({len(md)} chars)")
                break

    # Write index file
    index_path = os.path.join(output_dir, '_index.md')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(f"# {title}\n\n")
        f.write("## 章节列表\n\n")
        for fname in written_files:
            base = os.path.splitext(fname)[0]
            f.write(f"- [{base}]({fname})\n")

    print(f"\nTotal: {len(written_files)} chapters written to {output_dir}")


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: extract_epub.py <epub-file> <output-dir>")
        sys.exit(1)

    extract_epub(sys.argv[1], sys.argv[2])
