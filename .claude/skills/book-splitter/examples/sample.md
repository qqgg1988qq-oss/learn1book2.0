# Book Splitter 使用示例

## 示例 1: 基础拆分（文本 PDF）

### 输入

```
/book-splitter book.pdf
```

### 输出目录结构

```
book-chapters/
├── _index.md
├── front-01-封面.md
├── front-02-版权.md
├── front-03-前言.md
├── chapter-01-引论.md
├── chapter-02-第一部分_心灵的两个概念.md
├── chapter-03-第一章_心灵的两个概念.md
├── chapter-04-第二章_附随性和解释.md
├── ...
└── back-01-参考文献.md
```

### _index.md 示例

```markdown
---
title: "章节索引"
source: "conscious_mind.pdf"
total_chapters: 15
total_pages: 432
scan_pdf: false
---

# 章节索引

> 来源: conscious_mind.pdf
> 总页数: 432
> 章节数: 15

| 序号 | 章节 | 页码范围 | 文件 |
|------|------|----------|------|
| 1 | 封面 | 1-2 | [front-01-封面.md](front-01-封面.md) |
| 2 | 前言 | 3-8 | [front-02-前言.md](front-02-前言.md) |
| 3 | 引论 | 9-25 | [chapter-01-引论.md](chapter-01-引论.md) |
| 4 | 第一部分 基础 | 26-26 | [chapter-02-第一部分_基础.md](chapter-02-第一部分_基础.md) |
| ... | ... | ... | ... |
```

### 章节文件示例

```markdown
---
title: "第一章 心灵的两个概念"
page_range: [27, 45]
level: 2
source: "conscious_mind.pdf"
---

# 第一章 心灵的两个概念

*页码: 27 - 45*

在哲学史上，关于心灵的本质有着两种根本不同的概念...

[章节正文内容...]
```

## 示例 2: 扫描版 PDF（图片嵌入模式）

### 输入

```
/book-splitter scanned_book.pdf --scan=image
```

### 章节文件示例

扫描版页面的内容会以图片形式嵌入：

```markdown
---
title: "第一章"
page_range: [1, 15]
level: 1
source: "scanned_book.pdf"
---

# 第一章

*页码: 1 - 15*

![Page 1](images/page_0001.png)

![Page 2](images/page_0002.png)

...
```

### images 目录

```
book-chapters/images/
├── page_0001.png
├── page_0002.png
├── page_0003.png
└── ...
```

## 示例 3: 扫描版 PDF（OCR 模式）

### 输入

```
/book-splitter scanned_book.pdf --scan=ocr
```

### 效果

扫描版页面会通过 Tesseract OCR 提取文本，输出与文本 PDF 类似的 Markdown 文件。

**注意**: OCR 质量取决于 PDF 清晰度和 Tesseract 语言包配置。

## 示例 4: 二级章节拆分

### 输入

```
/book-splitter book.pdf --level=2
```

### 效果

除了章级别拆分，还会将节（二级标题）作为独立的 Markdown 文件拆分出来。

```
book-chapters/
├── _index.md
├── chapter-01-引论.md
├── chapter-02-第一章.md
├── section-02-1-第一节.md    # 新增的二级章节
├── section-02-2-第二节.md
├── chapter-03-第二章.md
└── ...
```

## 常见问题

### Q: PDF 没有内置目录怎么办？

A: 脚本会自动回退到基于正则的模式识别。如果仍无法识别，Claude 会读取 PDF 前 30 页内容，手动构建目录映射，并向用户确认。

### Q: 拆分后的文件太大怎么办？

A: 扫描版 PDF 使用图片模式时，images 目录可能很大。可以考虑：
1. 使用 `--scan=ocr` 模式替代图片
2. 降低图片 DPI（修改脚本中的 `dpi` 参数）
3. 使用图片压缩工具处理 images 目录

### Q: 中文 OCR 识别率低怎么办？

A: 确保安装了中文语言包：
- macOS: `brew install tesseract-lang`
- Ubuntu: `sudo apt-get install tesseract-ocr-chi-sim`
- 然后在脚本中使用 `--scan=ocr` 并确保 `lang="chi_sim+eng"`
