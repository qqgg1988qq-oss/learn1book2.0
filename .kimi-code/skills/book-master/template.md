# Book Master 工作流模板

## 输入

- **PDF路径**: `{pdf_path}`
- **输出位置**: `{workspace}/{book_name}/`

## 执行步骤

### Step 1: 创建项目目录

```bash
BOOK_NAME="{从PDF文件名提取的书名}"
mkdir -p "{workspace}/${BOOK_NAME}/chapters"
mkdir -p "{workspace}/${BOOK_NAME}/reports"
```

### Step 2: 拆分书籍

```bash
/book-splitter "{pdf_path}" --output "{workspace}/${BOOK_NAME}/chapters"
```

### Step 3: 验证拆分结果

- [ ] `_index.md` 已生成
- [ ] 章节文件数量与目录一致
- [ ] 无报错信息

### Step 4: 过滤章节

```bash
bash "${CLAUDE_SKILL_DIR}/scripts/filter.sh" "{workspace}/${BOOK_NAME}/chapters"
```

**自动排除**：
- [x] `_index.md`
- [x] `front-*-封面.md`
- [x] `front-*-书名.md`
- [x] `front-*-版权.md`
- [x] `front-*-目录.md`
- [x] `back-*-参考文献.md`
- [x] `back-*-索引.md`
- [x] `back-*-献辞.md`

**手动确认**（如有需要）：
- [ ] `front-*-前言.md` → 保留 / 排除
- [ ] `back-*-注释.md` → 保留 / 排除
- [ ] `back-*-后记.md` → 保留 / 排除

### Step 5: 并行启动子代理（核心）

对过滤后的每个章节，并行启动子代理：

```
Agent 1:
  任务: 对 chapters/chapter-01-xxx.md 调用 /deep-reader 提取知识点
  输出: 写入 reports/chapter-01-xxx-report.md

Agent 2:
  任务: 对 chapters/chapter-02-xxx.md 调用 /deep-reader 提取知识点
  输出: 写入 reports/chapter-02-xxx-report.md

...（最多8个并行）
```

**子代理提示词模板**：
```
你是一个深度精读专家。请对以下文件调用 /deep-reader 进行10维度知识点提取：
文件路径: {chapter_path}
输出路径: {report_path}

要求：
1. 严格遵循 /deep-reader 的10维度分析框架
2. 覆盖元信息、核心论点、关键概念、论据证据、逻辑结构、方法论、隐含假设、重要引用、知识网络、批判性思考
3. 输出必须包含自检清单
4. 将完整报告写入指定的输出路径
```

### Step 6: 等待所有子代理完成

- [ ] 检查所有报告文件是否已生成
- [ ] 检查是否有子代理报错
- [ ] 对失败的任务重新派发

### Step 7: 生成总索引

在主会话中创建 `_master-index.md`：

```markdown
# {书名} — 精读报告总索引

## 书籍信息
- 来源: {pdf-filename}
- 总页数: {total_pages}
- 拆分章节数: {total_chapters}
- 精读章节数: {analyzed_chapters}
- 排除章节: {excluded_chapters}

## 章节精读报告

| 序号 | 章节 | 页码 | 报告 |
|------|------|------|------|
| {i} | {title} | {pages} | [{file}]({path}) |

## 全书核心论点速览

### 中心论点
{central_thesis}

### 分论点汇总
1. {sub_thesis_1}（来自：{chapter}）
2. {sub_thesis_2}（来自：{chapter}）

## 跨章节知识网络

### 核心概念图谱
- {concept_1}: 出现在 {chapters}
- {concept_2}: 出现在 {chapters}

### 章节间逻辑关系
{chapter_relations}

## 自检清单

- [ ] 所有内容章节都已精读
- [ ] 每章报告都包含10维度分析
- [ ] 跨章节的论点一致性已检查
- [ ] 总索引已生成
```

## 输出检查清单

- [ ] `{book-name}/chapters/` 包含所有拆分章节
- [ ] `{book-name}/reports/` 包含所有精读报告
- [ ] `{book-name}/_master-index.md` 已生成
- [ ] 排除的章节（目录、参考文献等）未生成报告
- [ ] 报告命名与章节对应
