# article-claims-to-card 使用示例

## 示例 1：处理本地 Markdown 文章

### 用户输入

```
/article-claims-to-card /Users/chouchou/Documents/article.md
```

### 执行流程

1. 调用 `/article-claims-extractor /Users/chouchou/Documents/article.md`
2. 生成 `/Users/chouchou/Documents/article-claims.md`
3. 读取 claims 文件，提取核心论点与分论点
4. 格式化输出：

```
1.论点A:解释A;2.论点B:解释B;3.论点C:解释C.....
```

5. 调用 `/xl-card` 生成 JSON 卡片（仅对核心论点，先写入 xl-card 默认目录）
6. 将生成的卡片复制到源文件同目录：`/Users/chouchou/Documents/超专注系统.json`

### 预期输出

```markdown
已提取观点并生成卡片：

观点提取报告：/Users/chouchou/Documents/article-claims.md

格式化观点（核心论点 + 分论点）：
1.你不需要更多时间，你需要更多专注:人们常把低效归咎于时间不足，真正缺的是把注意力押到一件事上的能力;
2.专注是工作的力量乘数:做正确的事比做很多事更重要;
3.大脑是一台内存有限的电脑:杂念和未完成任务会拖慢认知性能;
4.分心是挑战与技能没对齐的信号:焦虑说明任务太难，无聊说明任务太简单;
5.超专注需要一套系统:身份、项目、截止日期、时间块、杠杆任务、例行程序、休息共同支撑。

卡片文件（仅核心论点，已复制到源目录）：
- /Users/chouchou/Documents/超专注系统.json
```

---

## 示例 2：用户粘贴文本

### 用户输入

```
/article-claims-to-card
（粘贴长文本）
```

### 执行流程

1. 将文本保存为 `{当前工作目录}/.article-claims-temp.md`
2. 调用 `/article-claims-extractor` 处理临时文件
3. 生成 `{当前工作目录}/article-claims.md`
4. 格式化观点并调用 `/xl-card` 铸卡
5. 删除临时文件 `.article-claims-temp.md`

---

## 示例 3：处理网页链接

### 用户输入

```
/article-claims-to-card https://example.com/article
```

### 执行流程

1. 尝试 FetchURL 获取正文
2. 若成功，保存为临时 Markdown 文件
3. 调用 `/article-claims-extractor` 提取观点
4. 格式化并铸卡
5. 若无法获取，请用户复制粘贴正文
