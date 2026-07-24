# book-reading-share 任务模板

## 任务输入

- 书籍文件路径：`{{book_path}}`
- 期望时长（可选）：`{{duration}}`
- 目标风格（可选）：`{{style}}`

## 执行步骤

### 步骤 1：深度读书

调用项目 skill `book-master` 处理输入书籍：

```bash
/book-master {{book_path}}
```

确认输出目录结构：

```
{{book_name}}/
├── chapters/
├── reports/
│   └── chapter-*-report.md
└── _master-index.md
```

### 步骤 2：论据收集

对 `reports/` 下每个 `chapter-*-report.md` 调用 `evidence-collector`：

```bash
/evidence-collector {{book_name}}/reports/chapter-*-report.md
```

记录每条论据的：
- 来源章节
- 对应知识点
- 类型（概念 / 数据 / 案例 / 金句）
- 质量分

### 步骤 3：生成读书分享口播文案

读取 `_master-index.md`，调用 `broadcast-maker`，并显式引用步骤 2 收集的论据：

```bash
/broadcast-maker {{book_name}}/_master-index.md
```

生成文件：`{{book_name}}-reading-share-script.md`

## 输出格式

最终口播文案应包含：

1. **开头钩子**：用书中一个反直觉观点或精彩案例抓住注意力。
2. **书籍定位**：一句话说明这本书在回答什么问题。
3. **核心脉络**：按章节/主题顺序展开，每段融入 1-2 个论据。
4. **个人 takeaway**：提炼一个可带走的精神内核。
5. **结尾引导**：自然收尾，可留讨论问题或行动建议。

语气要求：自然、口语化、有节奏，避免 AI 腔。
