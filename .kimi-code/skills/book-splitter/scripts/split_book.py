#!/usr/bin/env python3
"""
Book Splitter — PDF 书籍章节拆分辅助脚本
支持 TOC 提取、按章节拆分、Markdown 导出
特性：
  - 自动检测扫描版PDF（无文本层）
  - 扫描版PDF：页面渲染为图片嵌入Markdown
  - 可选OCR文本提取（需安装tesseract及语言包）
  - 支持多级章节拆分
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print("Error: PyMuPDF (fitz) is required. Install with: pip install PyMuPDF")
    sys.exit(1)

# 可选的OCR支持
try:
    import pytesseract
    from PIL import Image
    HAS_OCR = True
except ImportError:
    HAS_OCR = False


def sanitize_filename(name: str) -> str:
    """将章节标题转换为安全的文件名"""
    name = re.sub(r'[\\/*?:"<>|]', "", name)
    name = re.sub(r'\s+', "_", name.strip())
    return name[:80]


def extract_toc(pdf_path: str) -> list:
    """提取 PDF 的目录结构"""
    doc = fitz.open(pdf_path)
    toc = doc.get_toc()
    doc.close()
    
    result = []
    for level, title, page in toc:
        result.append({
            "level": level,
            "title": title.strip(),
            "page": page
        })
    return result


def is_scan_page(page: fitz.Page) -> bool:
    """检测页面是否为扫描版（无文本层）"""
    text = page.get_text().strip()
    return len(text) < 10  # 少于10个字符视为无文本层


def render_page_to_image(doc: fitz.Document, page_num: int, output_dir: str, dpi: int = 200) -> str:
    """将页面渲染为PNG图片，返回相对路径"""
    page = doc[page_num]
    mat = fitz.Matrix(dpi/72, dpi/72)  # 转换DPI
    pix = page.get_pixmap(matrix=mat)
    
    img_dir = os.path.join(output_dir, "images")
    os.makedirs(img_dir, exist_ok=True)
    
    img_name = f"page_{page_num + 1:04d}.png"
    img_path = os.path.join(img_dir, img_name)
    pix.save(img_path)
    
    return f"images/{img_name}"


def ocr_page(page: fitz.Page, lang: str = "chi_sim+eng") -> str:
    """对页面进行OCR，返回提取的文本"""
    if not HAS_OCR:
        return ""
    
    try:
        # 渲染页面为图片
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        img_data = pix.tobytes("png")
        
        # 使用PIL打开
        from PIL import Image
        import io
        img = Image.open(io.BytesIO(img_data))
        
        # OCR
        text = pytesseract.image_to_string(img, lang=lang)
        return text.strip()
    except Exception as e:
        print(f"    OCR warning: {e}")
        return ""


def extract_page_content(doc: fitz.Document, page_num: int, output_dir: str, 
                         scan_mode: str = "image") -> str:
    """
    提取页面内容为Markdown格式
    
    Args:
        scan_mode: "text" | "image" | "ocr"
            - text: 仅文本提取（遇到扫描版返回空）
            - image: 扫描版渲染为图片嵌入
            - ocr: 扫描版进行OCR提取文本
    """
    page = doc[page_num]
    
    # 尝试文本提取
    blocks = page.get_text("blocks")
    text_lines = []
    for block in sorted(blocks, key=lambda b: (b[1], b[0])):
        text = block[4].strip()
        if text:
            text_lines.append(text)
    
    extracted_text = "\n\n".join(text_lines)
    
    # 如果提取到足够文本，直接返回
    if len(extracted_text) > 50:
        return extracted_text
    
    # 扫描版PDF处理
    if scan_mode == "text":
        return ""  # 纯文本模式，扫描版返回空
    
    elif scan_mode == "ocr" and HAS_OCR:
        ocr_text = ocr_page(page)
        if ocr_text:
            return ocr_text
        # OCR失败时fallback到图片
    
    # image模式或OCR失败：渲染为图片
    img_rel_path = render_page_to_image(doc, page_num, output_dir)
    return f"![Page {page_num + 1}]({img_rel_path})"


def build_chapter_ranges(toc: list, total_pages: int, split_level: int = 1) -> list:
    """
    根据目录构建章节的页码范围
    """
    chapters = []
    
    for i, item in enumerate(toc):
        level = item["level"]
        title = item["title"]
        page = item["page"]
        
        if level > split_level:
            continue
        
        # 确定结束页码
        end_page = total_pages
        for next_item in toc[i+1:]:
            if next_item["level"] <= split_level:
                end_page = next_item["page"] - 1
                break
        
        # 智能分类：前置 matter / 正文章节 / 后置 matter
        title_lower = title.lower()
        is_front = any(k in title_lower for k in ["封面", "书名", "版权", "前言", "序言", "目录", "献辞"])
        is_back = any(k in title_lower for k in ["注释", "参考文献", "索引", "附录", "后记", "致谢"])
        
        if is_front:
            prefix = "front"
        elif is_back:
            prefix = "back"
        else:
            prefix = "chapter"
        
        seq = sum(1 for c in chapters if c["prefix"] == prefix) + 1
        
        chapters.append({
            "title": title,
            "start_page": page - 1,
            "end_page": end_page - 1,
            "level": level,
            "prefix": prefix,
            "filename": f"{prefix}-{seq:02d}-{sanitize_filename(title)}.md"
        })
    
    if not chapters:
        chapters = fallback_chapter_detection(toc, total_pages)
    
    return chapters


def fallback_chapter_detection(toc: list, total_pages: int) -> list:
    """当标准TOC提取失败时的备用方案"""
    chapters = []
    for i, item in enumerate(toc):
        title = item["title"]
        page = item["page"]
        
        if re.search(r'(第[一二三四五六七八九十\d]+章|Chapter\s+\d+|Part\s+\d+)', title, re.IGNORECASE):
            end_page = total_pages
            for next_item in toc[i+1:]:
                if re.search(r'(第[一二三四五六七八九十\d]+章|Chapter\s+\d+|Part\s+\d+)', next_item["title"], re.IGNORECASE):
                    end_page = next_item["page"] - 1
                    break
            
            chapters.append({
                "title": title,
                "start_page": page - 1,
                "end_page": end_page - 1,
                "level": 1,
                "prefix": "chapter",
                "filename": f"chapter-{len(chapters)+1:02d}-{sanitize_filename(title)}.md"
            })
    
    return chapters


def split_book(pdf_path: str, output_dir: str, split_level: int = 1, scan_mode: str = "image"):
    """
    主拆分函数
    
    Args:
        pdf_path: PDF文件路径
        output_dir: 输出目录
        split_level: 拆分粒度 (1=一级章节, 2=二级章节)
        scan_mode: 扫描版处理方式 ("text" | "image" | "ocr")
    """
    pdf_path = os.path.abspath(pdf_path)
    output_dir = os.path.abspath(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    
    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    
    # 检测是否为扫描版PDF
    scan_check_count = min(5, total_pages)
    scan_pages = sum(1 for i in range(scan_check_count) if is_scan_page(doc[i]))
    is_scan_pdf = scan_pages >= scan_check_count // 2
    
    if is_scan_pdf:
        print(f"Detected SCANNED PDF ({scan_pages}/{scan_check_count} pages have no text layer)")
        print(f"Scan mode: {scan_mode}")
        if scan_mode == "ocr" and not HAS_OCR:
            print("Warning: OCR requested but pytesseract not available. Falling back to image mode.")
            scan_mode = "image"
    else:
        print("Detected TEXT-BASED PDF")
    
    print(f"PDF: {os.path.basename(pdf_path)}")
    print(f"Total pages: {total_pages}")
    
    # 提取目录
    toc = extract_toc(pdf_path)
    print(f"TOC entries: {len(toc)}")
    
    # 构建章节范围
    chapters = build_chapter_ranges(toc, total_pages, split_level)
    
    if not chapters:
        print("Warning: No chapters detected from TOC. Creating single file for entire book.")
        chapters = [{
            "title": os.path.splitext(os.path.basename(pdf_path))[0],
            "start_page": 0,
            "end_page": total_pages - 1,
            "level": 1,
            "prefix": "book",
            "filename": "book-full.md"
        }]
    
    print(f"Chapters to extract: {len(chapters)}")
    
    # 提取并保存每个章节
    index_entries = []
    for ch_idx, ch in enumerate(chapters):
        start = ch["start_page"]
        end = min(ch["end_page"] + 1, total_pages)
        page_count = end - start
        
        print(f"  [{ch_idx+1}/{len(chapters)}] {ch['title']} (pages {start+1}-{end}, {page_count} pages)")
        
        content_parts = []
        for page_num in range(start, end):
            content = extract_page_content(doc, page_num, output_dir, scan_mode)
            if content.strip():
                content_parts.append(content)
        
        # 组装 Markdown 文件
        chapter_md_parts = [f"---"]
        chapter_md_parts.append(f'title: "{ch["title"]}"')
        chapter_md_parts.append(f"page_range: [{ch['start_page']+1}, {min(ch['end_page']+1, total_pages)}]")
        chapter_md_parts.append(f"level: {ch['level']}")
        chapter_md_parts.append(f'source: "{os.path.basename(pdf_path)}"')
        chapter_md_parts.append(f"---")
        chapter_md_parts.append("")
        chapter_md_parts.append(f"# {ch['title']}")
        chapter_md_parts.append("")
        chapter_md_parts.append(f"*页码: {ch['start_page']+1} - {min(ch['end_page']+1, total_pages)}*")
        chapter_md_parts.append("")
        
        if content_parts:
            chapter_md_parts.append("\n\n".join(content_parts))
        else:
            chapter_md_parts.append("*（本章内容为空或需要OCR处理）*")
        
        chapter_md = "\n".join(chapter_md_parts)
        
        output_path = os.path.join(output_dir, ch["filename"])
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(chapter_md)
        
        file_size = os.path.getsize(output_path)
        print(f"    -> {ch['filename']} ({file_size:,} bytes)")
        
        index_entries.append({
            "title": ch["title"],
            "file": ch["filename"],
            "pages": f"{ch['start_page']+1}-{min(ch['end_page']+1, total_pages)}"
        })
    
    doc.close()
    
    # 生成索引文件
    index_md = f"""---
title: "章节索引"
source: "{os.path.basename(pdf_path)}"
total_chapters: {len(chapters)}
total_pages: {total_pages}
scan_pdf: {str(is_scan_pdf).lower()}
---

# 章节索引

> 来源: {os.path.basename(pdf_path)}  
> 总页数: {total_pages}  
> 章节数: {len(chapters)}

| 序号 | 章节 | 页码范围 | 文件 |
|------|------|----------|------|
"""
    for i, entry in enumerate(index_entries, 1):
        index_md += f"| {i} | {entry['title']} | {entry['pages']} | [{entry['file']}]({entry['file']}) |\n"
    
    index_path = os.path.join(output_dir, "_index.md")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(index_md)
    
    print(f"\n{'='*60}")
    print(f"Done! Output: {output_dir}")
    print(f"Index: {index_path}")
    print(f"Total chapters: {len(chapters)}")
    
    # 列出images目录大小
    img_dir = os.path.join(output_dir, "images")
    if os.path.exists(img_dir):
        img_count = len(os.listdir(img_dir))
        img_size = sum(os.path.getsize(os.path.join(img_dir, f)) for f in os.listdir(img_dir))
        print(f"Images: {img_count} files ({img_size/1024/1024:.1f} MB)")


def main():
    parser = argparse.ArgumentParser(
        description="Book Splitter — PDF 书籍章节拆分工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 提取目录
  python3 split_book.py toc book.pdf

  # 拆分（一级章节，文本模式）
  python3 split_book.py split book.pdf -o ./chapters

  # 拆分（含二级章节，扫描版渲染为图片）
  python3 split_book.py split book.pdf -o ./chapters --level 2 --scan image

  # 拆分（扫描版使用OCR）
  python3 split_book.py scan book.pdf -o ./chapters --scan ocr

扫描版处理模式:
  text   - 仅提取文本，扫描版页面留空
  image  - 扫描版页面渲染为图片嵌入Markdown（默认）
  ocr    - 扫描版页面使用Tesseract OCR提取文本（需安装语言包）
""")
    
    subparsers = parser.add_subparsers(dest="command", help="子命令")
    
    # toc 子命令
    toc_parser = subparsers.add_parser("toc", help="提取目录结构（JSON输出）")
    toc_parser.add_argument("pdf", help="PDF 文件路径")
    
    # split 子命令
    split_parser = subparsers.add_parser("split", help="按章节拆分")
    split_parser.add_argument("pdf", help="PDF 文件路径")
    split_parser.add_argument("--output", "-o", default="./book-chapters", help="输出目录 (默认: ./book-chapters)")
    split_parser.add_argument("--level", "-l", type=int, default=1, choices=[1, 2], help="拆分粒度: 1=一级章节, 2=含二级章节 (默认: 1)")
    split_parser.add_argument("--scan", "-s", default="image", choices=["text", "image", "ocr"], 
                              help="扫描版PDF处理方式 (默认: image)")
    
    args = parser.parse_args()
    
    if args.command == "toc":
        toc = extract_toc(args.pdf)
        print(json.dumps(toc, ensure_ascii=False, indent=2))
    elif args.command == "split":
        split_book(args.pdf, args.output, args.level, args.scan)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
