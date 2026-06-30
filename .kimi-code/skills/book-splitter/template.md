# Book Splitter 任务模板

## 任务描述

拆分 PDF 书籍 `{book_name}` 为章节 Markdown 文件。

## 输入

- PDF 路径: `{pdf_path}`
- 输出目录: `{output_dir}` （默认: `./book-chapters`）
- 拆分粒度: `{split_level}` （1=一级章节, 2=含二级章节）
- 扫描模式: `{scan_mode}` （text=纯文本, image=图片嵌入, ocr=OCR识别）

## 执行步骤

### Step 1: 提取目录

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/split_book.py" toc "{pdf_path}"
```

### Step 2: 确认目录结构

向用户展示提取的目录，确认是否需要调整。

### Step 3: 执行拆分

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/split_book.py" split "{pdf_path}" \
  --output "{output_dir}" \
  --level {split_level} \
  --scan {scan_mode}
```

### Step 4: 验证输出

- 检查 `_index.md` 是否正确生成
- 确认章节文件数量和命名
- 验证内容是否完整

## 输出检查清单

- [ ] `_index.md` 索引文件已生成
- [ ] 章节数量与目录一致
- [ ] 每个章节文件包含 YAML frontmatter
- [ ] 扫描版 PDF 的图片已正确渲染（如适用）
- [ ] 文件命名符合规范（`{prefix}-{seq}-{title}.md`）
