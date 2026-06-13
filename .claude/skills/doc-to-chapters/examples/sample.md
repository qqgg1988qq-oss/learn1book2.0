# Doc to Chapters 使用示例

## 示例 1：EPUB 转章节 Markdown

```bash
/doc-to-chapters /path/to/道德经说什么.epub
```

输出：

```
道德经说什么/
├── _index.md
├── front-01-目录.md
├── front-02-landmarks.md
├── front-03-序_我背后的高人.md
├── front-04-序章.md
├── chapter-01-一.md
├── chapter-02-二.md
├── ...
└── back-01-后记.md
```

## 示例 2：PDF 指定输出目录

```bash
/doc-to-chapters /path/to/book.pdf /path/to/output-dir
```

## 示例 3：按二级标题拆分

```bash
/doc-to-chapters /path/to/article.docx --heading-level 2
```

## 示例 4：直接拆分已有 Markdown 文件

```bash
/doc-to-chapters /path/to/book.md --keep-md
```

由于输入已是 Markdown，`--keep-md` 在此处无实际作用，但保留完整 `.md` 副本。
