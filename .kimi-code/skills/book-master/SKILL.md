---
name: book-master
description: |
  书籍精读工作流编排器。自动完成"拆分书籍 → 过滤章节 → 并行知识点提取"的完整流程。

  触发场景：
  - "帮我精读这本书"
  - "提取这本书的知识点"
  - "拆分并分析这个PDF"
  - "对这本书做系统性的精读笔记"

  工作流程：
  1. 使用 /book-splitter 将PDF按章节拆分为Markdown
  2. 自动过滤排除目录、参考文献、索引等非内容章节
  3. 使用并行子代理对每个章节调用 /deep-reader 提取知识点
  4. 将所有精读报告汇总到以书名为名的项目文件夹

  输出：{book-name}/ 目录，包含拆分后的章节 + 每章的精读报告 + 总索引。
argument-hint: <pdf-file-path>
allowed-tools: Read, Bash, Write, Edit, Agent
disable-model-invocation: true
---

# Book Master — 书籍精读工作流编排器

将一本书从PDF到结构化知识点笔记的完整自动化流程。

## 使用方式

```
/book-master /path/to/book.pdf
```

## 工作流程

### Step 1: 创建项目文件夹

从PDF文件名提取书名，创建项目目录：
```
{workspace}/{book-name}/
├── chapters/          # book-splitter 输出
└── reports/           # deep-reader 输出
```

### Step 2: 拆分书籍

调用 `/book-splitter` 将PDF拆分为章节Markdown：
```bash
/book-splitter "{pdf-path}" --output "{book-name}/chapters"
```

### Step 3: 过滤章节

自动排除非内容章节：
- `_index.md` — 章节索引
- `front-*-目录.md` — 目录
- `front-*-封面.md` — 封面
- `front-*-书名.md` — 书名页
- `front-*-版权.md` — 版权页
- `back-*-参考文献.md` — 参考文献
- `back-*-索引.md` — 索引
- `back-*-献辞.md` — 献辞

保留内容章节（正文、前言、导言、后记、注释等）。

使用过滤脚本：
```bash
bash "{CLAUDE_SKILL_DIR}/scripts/filter.sh" "{book-name}/chapters"
```

### Step 4: 并行知识点提取（核心）

对过滤后的每个章节文件，**并行启动子代理**调用 `/deep-reader`：

```
并行启动 N 个子代理（N = 章节数量，建议最多8个并行）:

子代理 1: /deep-reader chapters/chapter-01-xxx.md → 输出到 reports/chapter-01-report.md
子代理 2: /deep-reader chapters/chapter-02-xxx.md → 输出到 reports/chapter-02-report.md
...
子代理 N: /deep-reader chapters/chapter-N-xxx.md → 输出到 reports/chapter-N-report.md
```

**子代理配置**：
- 使用 `general-purpose` agent 类型
- 每个子代理独立处理一个章节
- 子代理输出格式必须严格遵循 `/deep-reader` 的10维度模板
- 子代理将报告写入 `{book-name}/reports/` 目录

### Step 5: 汇总索引

所有子代理完成后，在主会话中生成总索引文件：

```markdown
# {书名} — 精读报告总索引

## 书籍信息
- 来源: {pdf-filename}
- 拆分章节数: {total-chapters}
- 精读章节数: {analyzed-chapters}
- 排除章节: {excluded-list}

## 章节精读报告

| 序号 | 章节 | 页码范围 | 精读报告 |
|------|------|----------|----------|
| 1 | {chapter-title} | {pages} | [报告](reports/xxx-report.md) |
| ... | ... | ... | ... |

## 全书核心论点速览
（从各章节报告中提取的中心论点汇总）

## 跨章节知识网络
（连接各章节知识点的关联图谱）
```

## 输出结构

```
{book-name}/
├── chapters/                      # book-splitter 原始输出
│   ├── _index.md
│   ├── front-01-封面.md
│   ├── front-04-前言.md
│   ├── chapter-01-xxx.md
│   ├── ...
│   └── back-03-参考文献.md
├── reports/                       # deep-reader 输出（核心成果）
│   ├── chapter-01-xxx-report.md
│   ├── chapter-02-xxx-report.md
│   ├── ...
│   └── back-02-后记-report.md
└── _master-index.md               # 总索引（由主会话生成）
```

## 注意事项

- 项目文件夹以PDF文件名命名（去除扩展名）
- 过滤是自动的，但用户可以手动调整排除规则
- 并行子代理数量受限于系统资源，建议最多8个
- 如果某章内容过长（>50KB），子代理可能需要更长处理时间
- 所有精读报告统一使用 `/deep-reader` 的10维度格式
