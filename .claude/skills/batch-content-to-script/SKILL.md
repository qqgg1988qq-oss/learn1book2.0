---
name: batch-content-to-script
description: |
  批量将多份深度精读报告转化为口播文案脚本。

  触发场景：
  - "帮我把这本书的所有精读报告转成文案"
  - "批量生成口播文案"
  - "把 reports 目录下的所有报告都转成视频脚本"
  - 任何需要将多份精读报告批量转化为口播文案的请求

  工作流程：
  1. 自动发现指定目录下的所有精读报告（*-report.md）
  2. 并行启动子代理，每个子代理对一份报告调用 /content-to-script
  3. 收集所有文案输出到 scripts/ 目录
  4. 生成文案总索引 _script-index.md

  输出：scripts/ 目录下的所有口播文案 + 总索引文件
argument-hint: <book-project-directory>
allowed-tools: Read, Bash, Write, Edit, Agent
disable-model-invocation: true
---

# batch-content-to-script — 批量文案生成器

一键将整本书（或任意项目）的所有精读报告批量转化为口播文案脚本。

## 使用方式

```
/batch-content-to-script <书籍项目目录>
```

例如：
```
/batch-content-to-script 弥散的心智
```

## 前置要求

- 目标目录必须包含 `reports/` 子目录
- `reports/` 中必须有 `*-report.md` 格式的精读报告文件
- 这些报告应是由 `/deep-reader` 生成的标准10维度分析报告

## 工作流程

### Step 1: 发现报告文件

自动扫描 `{book-name}/reports/` 目录，发现所有精读报告：

```
reports/
├── chapter-01-xxx-report.md
├── chapter-02-xxx-report.md
├── ...
└apter-chapter-NN-xxx-report.md
```

**自动排除**：
- `_master-index.md` — 总索引文件
- 非 `*-report.md` 结尾的文件

### Step 2: 确认时长策略

询问用户需要的视频时长策略：

| 选项 | 策略 | 说明 |
|------|------|------|
| 统一时长 | 所有章节使用相同时长 | 适合系列视频，保持风格一致 |
| 分别指定 | 每个章节单独选择时长 | 适合重点章节做长、次要章节做短 |
| 智能推荐 | 根据章节内容量自动选择 | 内容少的章节→短视频，内容多的→中/长视频 |

**时长选项**（与 `/content-to-script` 一致）：

| 选项 | 时长 | 字数范围 | 适用场景 |
|------|------|---------|---------|
| 短视频 | 1-2分钟 | 300-500字 | 快知识/预告片 |
| 中视频 | 5-15分钟 | 1200-3500字 | 标准知识视频 |
| 长视频 | 15-40分钟 | 3500-10000字 | 深度解析/讲座 |

### Step 3: 创建输出目录

创建 `scripts/` 目录存放所有文案输出：

```
{book-name}/
├── chapters/          # 原始章节
├── reports/           # 精读报告（输入）
├── scripts/           # 口播文案（输出）← 新建
└── _script-index.md   # 文案总索引 ← 新建
```

### Step 4: 并行文案生成（核心）

对每份报告文件，**并行启动子代理**调用 `/content-to-script`：

```
并行启动 N 个子代理（N = 报告数量，最多8个并行）:

子代理 1: /content-to-script reports/chapter-01-xxx-report.md → scripts/chapter-01-xxx-script.md
子代理 2: /content-to-script reports/chapter-02-xxx-report.md → scripts/chapter-02-xxx-script.md
...
子代理 N: /content-to-script reports/chapter-NN-xxx-report.md → scripts/chapter-NN-xxx-script.md
```

**子代理配置**：
- 使用 `general-purpose` agent 类型
- 每个子代理独立处理一份报告
- 子代理需要告知用户选择的时长策略
- 子代理将文案输出写入 `scripts/` 目录

### Step 5: 生成文案总索引

所有子代理完成后，在主会话中生成文案总索引：

```markdown
# {书名} — 口播文案总索引

## 项目信息
- 来源书籍: {book-name}
- 报告总数: {total-reports}
- 文案总数: {total-scripts}
- 生成日期: {date}
- 统一时长策略: {duration-strategy}

## 文案目录

| 序号 | 章节 | 时长 | 字数 | 文案文件 |
|------|------|------|------|----------|
| 1 | {chapter-title} | {duration} | {word-count} | [文案](scripts/xxx-script.md) |
| ... | ... | ... | ... | ... |

## 全系列核心论点速览
（从各章文案中提取的核心观点汇总，用于系列视频规划）

## 内容发布建议
- 发布顺序建议
- 章节之间的引用关系
- 适合做预告片的章节
```

## 输出结构

```
{book-name}/
├── chapters/                      # 原始章节文件
├── reports/                       # 精读报告（输入）
│   ├── chapter-01-xxx-report.md
│   ├── chapter-02-xxx-report.md
│   └── ...
├── scripts/                       # 口播文案（输出）
│   ├── chapter-01-xxx-script.md
│   ├── chapter-02-xxx-script.md
│   └── ...
├── reader/                        # 交互式阅读页面（如有）
├── _master-index.md               # 精读报告总索引
└── _script-index.md               # 口播文案总索引
```

## 注意事项

- 并行子代理数量最多8个，超出则分批处理
- 每份子代理任务独立，单个子代理失败不影响其他任务
- 文案文件命名规则：`{原报告名去掉-report后缀}-script.md`
- 如果 `scripts/` 目录已存在，会追加新文案并更新索引
- 生成的文案遵循 `/content-to-script` 的格式标准（钩子、主体、结尾、语气标注）
- 子代理在生成文案时会自动将时长策略传递给 `/content-to-script`
