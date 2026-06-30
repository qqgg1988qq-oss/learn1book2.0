---
name: book-splitter
description: |
  PDF 书籍章节拆分专家。将 PDF 书籍按目录结构拆分为独立的 Markdown 文件，
  支持自动 TOC 提取、扫描版 PDF 处理（图片渲染/OCR）、多级章节拆分和索引生成。

  触发场景：
  - "帮我拆分这本 PDF 书"
  - "把这本书按章节导出为 Markdown"
  - "提取 PDF 目录并拆分章节"
  - "将扫描版 PDF 转为 Markdown"

  输出：按章节组织的 Markdown 文件 + 索引文件 _index.md
argument-hint: <pdf-file> [output-dir] [--level=1|2] [--scan=text|image|ocr]
allowed-tools: Read, Bash, Write, Edit
disable-model-invocation: true
---

# Book Splitter — PDF 书籍章节拆分工具

将 PDF 书籍按目录结构拆分为独立的 Markdown 文件，每章一个文件，保留完整的内容层次和格式。

## 工作流程

### 1. 解析参数

从 `$ARGUMENTS` 提取：
- `<pdf-file>`: 输入 PDF 文件路径（必需）
- `[output-dir]`: 输出目录，默认为 `./book-chapters`
- `[--level=1|2]`: 拆分粒度，1=仅一级章节（章），2=包含二级章节（节），默认为 1
- `[--scan=text|image|ocr]`: 扫描版 PDF 处理方式，默认为 image

### 2. 提取目录结构

运行辅助脚本提取 PDF 目录：

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/split_book.py" toc "$PDF_PATH"
```

这会输出 JSON 格式的目录结构。如果 PDF 没有内置 TOC，则需要：
1. 读取 PDF 的前 20-30 页内容
2. 分析页面内容，手动构建目录映射
3. 向用户确认目录结构是否正确

### 3. 按章节拆分

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/split_book.py" split "$PDF_PATH" --output "$OUTPUT_DIR" --level "$LEVEL" --scan "$SCAN_MODE"
```

### 4. 生成索引文件

拆分完成后，在输出目录创建 `_index.md` 索引文件，列出所有章节。

## 扫描版 PDF 处理

扫描版 PDF（无文本层）有三种处理方式：

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| `text` | 仅提取文本，扫描版页面留空 | 纯文字 PDF |
| `image` | 扫描版页面渲染为 PNG 图片嵌入 Markdown | 扫描版书籍（默认） |
| `ocr` | 扫描版页面使用 Tesseract OCR 提取文本 | 需要可搜索文本的扫描版 |

使用 OCR 模式需要安装：
```bash
pip install pytesseract pillow
# macOS: brew install tesseract tesseract-lang
# Ubuntu: sudo apt-get install tesseract-ocr tesseract-ocr-chi-sim
```

## 手动模式（无 TOC 的 PDF）

如果 `split_book.py toc` 返回空或错误的目录：

1. 用 `Read` 工具读取 PDF 文件的前 30 页
2. 从内容中识别章节标题和页码
3. 构建目录列表，格式如下：
   ```
   Chapter 1: Title (Page X)
   Chapter 2: Title (Page Y)
   ```
4. 向用户展示识别的目录，确认无误后继续拆分

## 输出文件结构

```
output-dir/
├── _index.md                 # 章节索引
├── front-01-封面.md          # 封面
├── front-02-书名.md          # 书名页
├── front-03-版权.md          # 版权页
├── front-04-前言.md          # 前言
├── front-05-目录.md          # 目录
├── chapter-01-引论.md        # 第一章
├── chapter-02-第一部分_基础.md
├── chapter-03-第一章_标题.md
├── ...
└── back-01-注释.md           # 注释
```

每个章节文件顶部包含 YAML frontmatter：
```yaml
---
title: "章节标题"
page_range: [起始页, 结束页]
level: 1
source: "book.pdf"
---
```

## 依赖安装

```bash
# 必需
pip install PyMuPDF

# OCR 支持（可选）
pip install pytesseract pillow

# macOS 系统依赖
brew install tesseract tesseract-lang

# Ubuntu 系统依赖
sudo apt-get install tesseract-ocr tesseract-ocr-chi-sim
```

## 注意事项

- 拆分后的 Markdown 保留原文的段落结构和层次
- 章节标题使用 Markdown 标题格式（`# `、`## ` 等）
- 扫描版 PDF 默认渲染为 200 DPI 的 PNG 图片
- 如果章节内容超过 500KB，会提示用户注意文件大小
- 自动识别前置内容（封面、版权、前言）和后置内容（注释、参考文献、索引）
