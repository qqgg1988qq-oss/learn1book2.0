---
name: book-reading-share
description: |
  读书分享口播文案生成器。对一本书走完整读书工作流：
  1) 调用 book-master 生成各章节深度精读报告；
  2) 对各章节报告调用 evidence-collector 收集概念/数据/案例/金句；
  3) 基于全书 _master-index.md 调用 broadcast-maker，并融合步骤 2 收集的论据，生成一篇有“人味”的读书分享口播文案。

  触发场景：
  - "帮我做一期这本书的读书分享"
  - "把这本书转成口播文案"
  - "/book-reading-share /path/to/book.pdf"
  - 任何需要将一本书加工成视频/音频口播读书分享的场景

  输出：项目目录下的 reports/、evidence/（或论据库对应位置）、以及最终的读书分享口播文案文件。
allowed-tools: [Read, Bash, Agent]
---

# book-reading-share

## 功能定位

把一本书（PDF/EPUB 等）自动加工成可直接录制的读书分享口播文案。

## 工作流程

1. **深度读书**
   - 调用项目内 skill `book-master` 处理用户提供的书籍文件。
   - 生成标准书籍项目结构：
     ```
     {book-name}/
     ├── chapters/
     ├── reports/chapter-*-report.md
     └── _master-index.md
     ```

2. **论据收集**
   - 遍历 `reports/` 目录下的所有章节精读报告。
   - 对每个章节报告调用 `evidence-collector`。
   - 将提取的概念、数据、案例、金句沉淀到论据库，并记录每条论据与章节/知识点的对应关系。

3. **口播文案生成**
   - 读取全书的 `_master-index.md` 作为整体结构输入。
   - 调用 `broadcast-maker`，在生成文案时主动引用步骤 2 中收集的各章节论据。
   - **默认生成「长视频」口播文案**（15-40 分钟，3500-10000 字），覆盖全书更多核心观点与细节；用户可在触发时通过 `--duration` 指定短视频或中视频。
   - 输出一篇有钩子、有节奏、有具体细节、去 AI 味的读书分享口播文案。

## 使用方法

```bash
/book-reading-share /path/to/book.pdf
```

可选参数：
- `--duration 短视频|中视频|长视频`：控制口播文案时长。**默认值为「长视频」（15-40 分钟，3500-10000 字）**，以覆盖全书更多核心观点与细节。
- `--style 轻松|严肃|故事`：控制文案风格。

## 输入要求

- 必须提供书籍文件的绝对路径。
- 支持 PDF、EPUB 以及 TXT 等可被拆分为章节的格式。

## 输出说明

- 书籍项目目录：`{book-name}/`
- 章节深度报告：`{book-name}/reports/chapter-*-report.md`
- 全书总索引：`{book-name}/_master-index.md`
- 最终口播文案：`{book-name}/{book-name}-reading-share-script.md`

## 注意事项

- 步骤 1 `book-master` 可能耗时较长，取决于书籍长度和目录层级。
- 步骤 2 会并行处理多个章节报告，但建议一次不超过 8 个并行子代理。
- 最终文案会保存到书籍项目目录下，不会被提交到 Git（目录已在 `.gitignore` 中）。
