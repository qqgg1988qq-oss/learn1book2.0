---
name: markitdown
description: |
  通用文件转 Markdown 工具。调用 Microsoft MarkItDown 将用户上传的 PDF、Word、PowerPoint、Excel、图片等文件转换为 Markdown 格式。

  触发场景：
  - "帮我把这个 PDF 转成 Markdown"
  - "把这个文件转成 md"
  - "转换 PDF/Word/PPT 为 Markdown"
  - "提取这个文档的文本内容"
  - "上传了文件，帮我转成 Markdown"

  输出：转换后的 Markdown 文件，默认与源文件同名、扩展名改为 .md
argument-hint: <file-path> [output-path]
allowed-tools: Read, Bash, Write, Edit
disable-model-invocation: true
---

# MarkItDown — 文件转 Markdown

将 Microsoft Office 文档、PDF、图片、音频、HTML 等多种格式转换为 Markdown，便于后续精读、引用或索引。

## 支持格式

- PDF（含扫描版，可选 OCR）
- Microsoft Word（.doc/.docx）
- Microsoft PowerPoint（.ppt/.pptx）
- Microsoft Excel（.xls/.xlsx）
- 图片（jpg、png、gif 等，依赖 OCR）
- HTML
- ZIP（自动解压并转换内部文件）
- 文本文件（txt、csv、json、xml 等）

## 使用方法

### 单文件转换

```bash
markitdown "<file-path>" -o "<output-path>"
```

例如：

```bash
markitdown "/path/to/report.pdf" -o "/path/to/report.md"
```

### 读取 stdin

```bash
cat "example.pdf" | markitdown -o "example.md"
```

### 批量转换

当前目录下所有 PDF：

```bash
for f in *.pdf; do
  markitdown "$f" -o "${f%.pdf}.md"
done
```

## 参数说明

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

## 依赖安装

如果当前环境未安装 markitdown，使用以下命令安装：

```bash
pip install markitdown
```

OCR 支持（可选，用于图片/扫描版 PDF）：

```bash
pip install markitdown[ocr]
```

## 输出约定

1. 默认输出文件与源文件同名，扩展名改为 `.md`。
2. 如果用户未指定输出路径，使用 `文件名.md` 保存到源文件所在目录。
3. 转换完成后，向用户报告输出路径和文件大小。
4. 如果转换失败（如缺少依赖、加密 PDF、扫描版无 OCR），说明原因并给出解决建议。

## 注意事项

- 加密/权限受限的 PDF 需先解密再转换。
- 扫描版 PDF 默认可能只输出空文本，建议开启 OCR 或将页面作为图片处理。
- 大文件转换可能耗时较长，建议先告知用户预计等待时间。
- 图片默认会被转为 Markdown 图片链接；使用 `--keep-data-uris` 可保留内嵌 base64。
