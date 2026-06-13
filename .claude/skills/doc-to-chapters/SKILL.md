---
name: doc-to-chapters
description: |
  任意文档 → Markdown → 按章节拆分的一站式工具。

  先调用 Microsoft MarkItDown 将 PDF、EPUB、Word、PPT、Excel、图片等文件
  转换为 Markdown，再按一级标题拆分为 front/chapter/back 章节文件，并生成
  _index.md 索引。输出结构与 book-splitter 保持一致。

  触发场景：
  - "把这本书按章节拆分成 Markdown"
  - "PDF 转章节 Markdown"
  - "EPUB 拆分章节"
  - "文档转章节笔记"

  输出：按章节组织的 Markdown 文件 + 索引文件 _index.md
argument-hint: <file-path> [output-dir] [--heading-level=1|2] [--keep-md]
allowed-tools: Read, Bash, Write, Edit
disable-model-invocation: true
---

# Doc to Chapters — 文档转章节 Markdown

将任意文档（PDF/EPUB/DOCX/PPTX/XLSX/图片/Markdown 等）自动转换为结构化的章节 Markdown，便于后续 `deep-reader` 精读或放入 Obsidian 知识库。

## 工作流程

### 1. 解析参数

从 `$ARGUMENTS` 提取：

- `<file-path>`: 输入文件路径（必需）
- `[output-dir]`: 输出目录，默认为 `./{文件名}`
- `[--heading-level=1|2]`: 拆分粒度，1=按 H1 拆分，2=按 H2 拆分，默认 1
- `[--keep-md]`: 保留中间生成的完整 `.md` 文件到输出目录

### 2. 转换为 Markdown

如果输入文件不是 `.md`，调用 `markitdown` 进行转换：

```bash
markitdown "<file-path>" -o "<temp-output>.md"
```

### 3. 按章节拆分

运行辅助脚本：

```bash
python "${CLAUDE_SKILL_DIR}/scripts/doc_to_chapters.py" \
  "<input-file>" \
  "<output-dir>" \
  --heading-level 1
```

### 4. 生成索引

拆分完成后，在输出目录创建 `_index.md` 索引文件。

## 输出文件结构

```
output-dir/
├── _index.md                 # 章节索引
├── front-01-目录.md          # 目录等前置内容
├── front-02-前言.md
├── chapter-01-标题.md        # 第一章
├── chapter-02-标题.md
├── ...
└── back-01-后记.md           # 后记等后置内容
```

每个章节文件顶部包含 YAML frontmatter：

```yaml
---
title: "章节标题"
level: 1
source: "原始文件名"
---
```

## 章节类型识别规则

根据 H1 标题自动分类：

| 类型 | 识别关键词 | 文件名前缀 |
|------|-----------|-----------|
| 前置内容 | 目录、Landmarks、封面、书名、版权、前言、序言、序章、序、献辞 | `front-NN-` |
| 正文 | 其他所有标题 | `chapter-NN-` |
| 后置内容 | 后记、注释、参考文献、索引、附录、致谢 | `back-NN-` |

## 依赖安装

```bash
# 必需：Markdown 转换
pip install markitdown

# 可选：OCR 支持（扫描版 PDF / 图片）
pip install markitdown[ocr]
```

## 使用方法

### 单文件转换并拆分

```bash
/doc-to-chapters /path/to/book.epub
```

### 指定输出目录

```bash
/doc-to-chapters /path/to/book.pdf /path/to/output-dir
```

### 按 H2 拆分

```bash
/doc-to-chapters /path/to/article.docx --heading-level 2
```

### 保留中间 Markdown 文件

```bash
/doc-to-chapters /path/to/book.epub --keep-md
```

## 注意事项

- 文档必须包含清晰的一级标题（`# 标题`），否则无法自动拆分。
- 扫描版 PDF 建议安装 `markitdown[ocr]` 以获得可搜索文本。
- 输出目录结构与 `book-splitter` 保持一致，可与 `book-master`、`deep-reader` 流程无缝衔接。
- 如果输入文件已是 Markdown，则跳过转换直接拆分。
