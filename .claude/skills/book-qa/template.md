# Book QA — 问答模板

## 当前书籍上下文

```yaml
book_path: {{book_project_path}}
book_name: {{book_name}}
reports_dir: {{book_project_path}}/reports/
chapters_dir: {{book_project_path}}/chapters/
total_chapters: {{total_reports}}
loaded: {{timestamp}}
```

## 用户问题

{{user_question}}

---

## 检索执行记录

### 第一层：知识点报告检索

- [ ] 扫描 reports/ 目录文件列表
- [ ] 搜索"关键概念与定义"部分
- [ ] 搜索"核心论点"部分
- [ ] 搜索"论据与证据"部分
- [ ] 搜索"重要引用原文"部分
- [ ] 搜索"知识网络与关联"部分
- [ ] 搜索"批判性思考"部分

**检索结果摘要**：
{{reports_search_summary}}

**是否足够回答**：{{yes/no}}

---

### 第二层：原书章节检索（若第一层不足）

- [ ] 根据关键词定位相关章节文件
- [ ] 读取相关章节全文
- [ ] 搜索具体段落

**检索结果摘要**：
{{chapters_search_summary}}

**是否足够回答**：{{yes/no}}

---

### 第三层：网络搜索补充（若前两层均不足）

- [ ] 搜索问题关键词 + 书名
- [ ] 搜索作者相关论述
- [ ] 搜索学术评论/书评

**检索结果摘要**：
{{web_search_summary}}

**是否足够回答**：{{yes/no}}

---

## 最终回答

### 回答正文

{{structured_answer}}

### 信息来源

| 来源层级 | 具体位置 | 引用内容 |
|----------|----------|----------|
| 📄 知识点报告 | {{report_ref}} | {{quote}} |
| 📖 原书章节 | {{chapter_ref}} | {{quote}} |
| 🌐 网络搜索 | {{search_ref}} | {{quote}} |

---

## 相关延伸阅读

（可选，如果用户在问一个可以延伸的主题）

- 书中其他相关章节：{{related_chapters}}
- 可进一步探讨的问题：{{follow_up_questions}}
