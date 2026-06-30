---
name: markitdown
description: |
  通用文件转 Markdown 工具 + 书籍预处理入口。

  1) 单文件转换：调用 Microsoft MarkItDown 将 PDF、Word、PowerPoint、Excel、
     图片、HTML 等文件转换为 Markdown。
  2) 书籍预处理：将 PDF/EPUB/DOCX 等书籍按章节拆分为结构化 Markdown，输出
     结构与 book-splitter 保持一致，可直接衔接 book-master / deep-reader 工作流。

  触发场景：
  - "帮我把这个 PDF 转成 Markdown"
  - "把这本书按章节拆分成 Markdown"
  - "PDF/EPUB/DOCX 转章节笔记"
  - "先用 markitdown 预处理这本书"

  输出：
  - 单文件模式：转换后的 Markdown 文件
  - 书籍模式：{book-name}/chapters/ 下的 front/chapter/back 章节文件 + _index.md
argument-hint: <file-path> [output-path-or-dir] [--book] [--heading-level=1|2] [--keep-md]
allowed-tools: Read, Bash, Write, Edit
disable-model-invocation: true
---

# MarkItDown — 文件转 Markdown 与书籍预处理

将 Microsoft Office 文档、PDF、EPUB、图片、音频、HTML 等多种格式转换为 Markdown，并支持按章节拆分书籍，便于后续精读、引用或索引。

## 两种工作模式

### 模式一：单文件转换（默认）

将任意支持的文件转换为单个 Markdown 文件。

```bash
/markitdown "<file-path>" -o "<output.md>"
```

例如：

```bash
/markitdown "/path/to/report.pdf" -o "/path/to/report.md"
```

### 模式二：书籍预处理（`--book`）

将书籍文件转换为 Markdown 后，按一级标题拆分为章节，生成与 `book-splitter` 兼容的目录结构。

```bash
/markitdown "<book-file>" --book [output-dir] [--heading-level=1|2] [--keep-md]
```

例如：

```bash
/markitdown "/path/to/book.epub" --book
/markitdown "/path/to/book.pdf" --book "/path/to/book-name" --heading-level 1
```

书籍模式输出结构：

```
{book-name}/
├── chapters/
│   ├── _index.md                 # 章节索引
│   ├── front-01-目录.md
│   ├── front-02-前言.md
│   ├── chapter-01-标题.md
│   ├── chapter-02-标题.md
│   ├── ...
│   └── back-01-后记.md
└── {book-name}.md                # 仅当 --keep-md 时保留完整 Markdown
```

每个章节文件顶部包含 YAML frontmatter：

```yaml
---
title: "章节标题"
level: 1
source: "原始文件名"
---
```

## 支持格式

- PDF（文本型 PDF 直接转换；扫描版需配合 OCR 或 Azure Document Intelligence）
- EPUB / MOBI 等电子书
- Microsoft Word（.doc/.docx）
- Microsoft PowerPoint（.ppt/.pptx）
- Microsoft Excel（.xls/.xlsx）
- 图片（jpg、png、gif 等，依赖 OCR）
- HTML / ZIP / 文本文件

## 单文件转换参数

```bash
markitdown "<file-path>" -o "<output.md>"
```

| 参数 | 说明 |
|------|------|
| `-o <path>` | 输出 Markdown 文件路径 |
| `-x <ext>` | 指定文件扩展名提示（用于 stdin） |
| `-m <mime>` | 指定 MIME 类型提示 |
| `-c <charset>` | 指定字符集（如 UTF-8） |
| `-d` | 使用 Azure Document Intelligence（需配合 `-e`） |
| `-e <endpoint>` | Document Intelligence Endpoint |
| `-p` | 启用第三方插件 |
| `--keep-data-uris` | 保留图片的 base64 data URI |

## 书籍预处理参数

调用辅助脚本：

```bash
python "${CLAUDE_SKILL_DIR}/scripts/markitdown_book.py" \
  "<input-file>" \
  "<output-dir>" \
  --heading-level 1
```

| 参数 | 说明 |
|------|------|
| `<input>` | 输入文件路径（必需） |
| `[output]` | 输出目录，默认为 `./{文件名}` |
| `--heading-level 1\|2` | 按 H1 或 H2 拆分，默认 1 |
| `--keep-md` | 保留中间生成的完整 `.md` 文件 |
| `--no-chapters-dir` | 不创建 chapters/ 子目录，直接输出到根目录 |

## 章节类型识别规则

根据 H1/H2 标题自动分类：

| 类型 | 识别关键词 | 文件名前缀 |
|------|-----------|-----------|
| 前置内容 | 目录、Landmarks、封面、书名、版权、前言、序言、序章、序、献辞、译者序、作者序、推荐序、引言 | `front-NN-` |
| 正文 | 其他所有标题 | `chapter-NN-` |
| 后置内容 | 后记、注释、参考文献、索引、附录、致谢、结语、跋、出版说明、编后记 | `back-NN-` |

## 依赖安装

```bash
# 必需
pip install markitdown

# 如果需要更好的 PDF/图片 OCR 支持，可配合 Azure Document Intelligence 使用：
# markitdown -d -e <endpoint> "file.pdf"
```

## 输出约定

1. **单文件模式**：默认输出文件与源文件同名，扩展名改为 `.md`；用户指定 `-o` 时按指定路径保存。
2. **书籍模式**：默认以输入文件名（去扩展名）创建项目目录，章节文件放在 `chapters/` 子目录下，并生成 `_index.md`。
3. 转换完成后，向用户报告输出路径、章节数量和文件大小。
4. 如果转换结果为空或极短（常见于扫描版 PDF 未启用 OCR），主动提示用户并给出解决建议。

## 与 book-master 的衔接

书籍预处理完成后，目录结构已与 `book-splitter` 输出保持一致，可直接进入 `book-master` 的 Step 3（过滤）和 Step 4（并行深度精读）：

```bash
# 1. 预处理
/markitdown "/path/to/book.pdf" --book "/path/to/book-name"

# 2. 过滤非内容章节
bash ".kimi-code/skills/book-master/scripts/filter.sh" "/path/to/book-name/chapters"

# 3. 并行深度精读（由 book-master 自动完成）
```

## 注意事项

- 加密/权限受限的 PDF 需先解密再转换。
- 扫描版 PDF 默认可能只输出空文本；建议使用 Azure Document Intelligence（`-d -e`）或先用 Tesseract OCR 处理。
- 大文件转换可能耗时较长，建议先告知用户预计等待时间。
- 图片默认会被转为 Markdown 图片链接；使用 `--keep-data-uris` 可保留内嵌 base64。
- 拆分依赖清晰的一级标题（`# 标题`），若书籍目录层级混乱，可尝试 `--heading-level 2`。
