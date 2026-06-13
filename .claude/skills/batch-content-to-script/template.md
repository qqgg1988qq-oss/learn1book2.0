# 批量文案生成任务模板

## 主会话任务清单

### Phase 1 — 准备阶段

- [ ] 确认目标目录存在且包含 `reports/` 子目录
- [ ] 扫描并列出所有 `*-report.md` 文件
- [ ] 询问用户时长策略（统一/分别/智能推荐）
- [ ] 创建 `scripts/` 输出目录

### Phase 2 — 并行分发

- [ ] 计算并行批次（每批最多8个子代理）
- [ ] 为每份报告启动子代理，传入以下参数：
  - 报告文件路径
  - 时长策略
  - 输出文件路径（scripts/目录下）

### Phase 3 — 汇总阶段

- [ ] 等待所有子代理完成
- [ ] 统计生成结果（成功/失败/字数）
- [ ] 生成 `_script-index.md` 总索引

---

## 子代理任务模板

### 子代理接收的参数

```yaml
input_report: "{book-name}/reports/chapter-XX-xxx-report.md"
output_script: "{book-name}/scripts/chapter-XX-xxx-script.md"
duration_strategy: "short|medium|long|auto"
chapter_title: "章节标题"
```

### 子代理执行步骤

1. **读取报告**：使用 Read 工具读取指定的 report 文件
2. **调用 skill**：在子代理内部执行 `/content-to-script` 逻辑
3. **生成文案**：按照时长策略生成口播文案
4. **写入文件**：将文案写入指定的 script 文件路径
5. **返回结果**：向主会话报告完成状态和字数统计

### 子代理返回格式

```yaml
status: "success|error"
input: "chapter-01-xxx-report.md"
output: "chapter-01-xxx-script.md"
word_count: 1234
duration: "medium"
error_message: ""  # 如果 status 为 error
```

---

## 主会话与子代理通信协议

### 主会话发给子代理的提示词模板

```
你是一个口播文案生成子代理。你的任务是：

1. 读取这份精读报告：{input_report}
2. 将其转化为时长为 {duration} 的口播文案
3. 文案保存到：{output_script}

时长策略：
- short: 300-500字，保留1个核心论点+1个类比+金句结尾
- medium: 1200-3500字，保留3-5个分论点+完整起承转合
- long: 3500-10000字，覆盖所有重要分论点+深层逻辑推理

文案格式要求：
- 开头钩子（前30秒抓住注意力）
- 主体内容（分段展开，有过渡句）
- 结尾引导（总结+互动）
- 语气标注（停顿、重音、情绪提示）

完成后请告诉我：
- 生成的字数
- 使用的时长策略
- 文件保存路径
```

---

## 总索引模板

```markdown
# {书名} — 口播文案总索引

## 项目信息
- 来源书籍: {book-name}
- 报告总数: {total}
- 文案总数: {completed}/{total}
- 生成日期: {date}
- 时长策略: {strategy}

## 文案目录

| 序号 | 章节 | 时长 | 字数 | 状态 | 文案文件 | 对应报告 |
|------|------|------|------|------|----------|----------|
| 1 | {title} | {dur} | {wc} | ✅ | [文案]({script}) | [报告]({report}) |

## 全系列核心论点速览

{从各章文案中提取的核心观点}

## 发布规划建议

### 推荐发布顺序
1. ...

### 适合做独立视频的重点章节
- ...

### 适合做系列连播的章节组
- ...
```
