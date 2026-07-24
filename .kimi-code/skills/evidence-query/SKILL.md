---
name: evidence-query
description: |
  论据查询器。根据用户提供的写作主题或关键词，从论据资料库中检索最相关的概念、数据、案例、金句。
  支持按素材类型、主题领域（#主题/...）、应用场景（#场景/...）、质量分等多维度筛选，
  返回 TOP-N 结果作为写作上下文。

  触发场景：
  - "帮我查一下论据库里有关于中年失业的素材"
  - "写这篇文章需要一些论据支持"
  - "检索关于习惯养成的概念和金句"
  - "给我找几个适合开头的金句"
  - 任何需要从已有资料库中找写作素材的请求

  输出：按相关度/质量分排序的 N 条论据，包含标题、来源、主题、场景、质量分、摘要、路径。
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# 论据查询器

> **用途**：写东西时快速从自己的论据库中捞出**高质量、用得上的弹药**。

---

## 一、使用流程

### 用户提供查询主题

可以直接输入主题、关键词或一句话描述：

```
/evidence-query "中年失业后的出路"
/evidence-query "习惯养成的方法"
/evidence-query "写一篇文章论证坚持的价值"
/evidence-query "找几个适合开头的金句"
```

或自然语言：

```
帮我查一下论据库里关于中年危机的素材
写这篇文章需要一些论据支持
检索关于复利效应的金句
```

---

## 二、工作流

### 步骤 1：理解查询意图

从用户输入中提取：
- 核心主题
- 需要的论据类型（可选）：概念 / 数据 / 案例 / 金句 / 全部
- 应用场景（可选）：开头吸引 / 核心论据 / 反面论证 / 结尾升华
- 质量要求（可选）：高质量（quality ≥ 4）/ 合格（quality ≥ 3）/ 全部

### 步骤 2：调用检索脚本

运行本地检索脚本：

```bash
# 基础查询
python /Users/chouchou/.agents/skills/evidence-query/scripts/evidence_query.py "查询主题"

# 返回更多结果
python /Users/chouchou/.agents/skills/evidence-query/scripts/evidence_query.py "查询主题" --top 10

# 按类型筛选
python /Users/chouchou/.agents/skills/evidence-query/scripts/evidence_query.py "查询主题" --type 金句

# 按主题领域筛选
python /Users/chouchou/.agents/skills/evidence-query/scripts/evidence_query.py "查询主题" --topic "主题/社会/就业"

# 按应用场景筛选
python /Users/chouchou/.agents/skills/evidence-query/scripts/evidence_query.py "查询主题" --scene "场景/开头吸引"

# 按最低质量分筛选
python /Users/chouchou/.agents/skills/evidence-query/scripts/evidence_query.py "查询主题" --min-quality 4

# 按质量分排序
python /Users/chouchou/.agents/skills/evidence-query/scripts/evidence_query.py "查询主题" --sort quality

# 强制重建缓存
python /Users/chouchou/.agents/skills/evidence-query/scripts/evidence_query.py "查询主题" --rebuild
```

### 步骤 3：整理并输出结果

将检索到的论据按相关度排序，以清晰的格式呈现给用户。每条论据包含：
- 排名
- ID 和类型
- 标题
- 来源
- 主题领域（topic）
- 应用场景（scene）
- 质量分（quality）
- 标签
- 路径
- 核心内容摘要

---

## 三、输出格式

```markdown
## 查询：{主题}

共找到 {N} 条相关论据（已应用筛选条件），返回 TOP {M}：

### 1. {ID}｜{类型}｜质量 {Q} 分｜相关度 {分数}

- 标题：{标题}
- 来源：{来源}
- 主题：{topic}
- 场景：{scene}
- 标签：{标签}
- 摘要：{核心内容}
- 文件：{路径}

### 2. ...

---

## 使用建议

- 可直接引用金句作为文章开头或结尾
- 概念和数据可用于支撑论点
- 案例可用于增强可读性和代入感
- 优先使用 quality ≥ 4 的素材
```

---

## 四、检索脚本说明

脚本路径：

```
/Users/chouchou/.agents/skills/evidence-query/scripts/evidence_query.py
```

参数：

```bash
python evidence_query.py "查询主题"            # 默认返回 TOP 5
python evidence_query.py "查询主题" --top 10   # 返回 TOP 10
python evidence_query.py "查询主题" --type 概念 # 仅返回概念
python evidence_query.py "查询主题" --topic "主题/商业"  # 按主题筛选
python evidence_query.py "查询主题" --scene "场景/核心论据"  # 按场景筛选
python evidence_query.py "查询主题" --min-quality 4  # 最低质量分 4
python evidence_query.py "查询主题" --sort quality   # 按质量分排序
python evidence_query.py "查询主题" --rebuild  # 强制重建缓存
```

特点：
- 无需 PyTorch / 深度学习库
- 依赖 scikit-learn（首次自动安装）
- 基于 TF-IDF + 字符 ngram + 关键词匹配 + 字段权重 + 质量分加成
- 标题、topic、tags 字段权重更高
- 支持按类型/主题/场景/质量分筛选
- 可同时返回多条相关论据，供写作上下文使用

---

## 五、Obsidian Dataview 补充检索

在 Obsidian 中，可通过 Dataview 插件实现更灵活的检索。常用查询模板见论据库中的 `常用检索.md`。

**示例 1：按主题+质量分检索**

```dataview
TABLE type, scene, quality, source
FROM "论据库"
WHERE contains(topic, "商业") AND quality >= 4
SORT quality DESC, date DESC
```

**示例 2：按应用场景检索**

```dataview
LIST
FROM "论据库"
WHERE contains(scene, "开头吸引") AND contains(topic, "科技")
SORT quality DESC
LIMIT 10
```

**示例 3：待优化素材清单**

```dataview
TABLE type, topic, quality, source
FROM "论据库"
WHERE quality <= 2 OR status = "review"
SORT quality ASC
```

---

## 六、质量标准

- [ ] 查询主题理解准确
- [ ] 正确识别用户隐含的类型/场景/质量要求
- [ ] 返回结果按相关度或质量分排序
- [ ] 每条论据信息完整（标题、来源、主题、场景、质量分、摘要、路径）
- [ ] 给出明确的使用建议
- [ ] 若结果不足，提示用户补充资料库

---

## 七、触发示例

```
/evidence-query "中年失业后的出路"
/evidence-query "复利效应"
帮我查一下论据库里关于习惯养成的素材
给我找几个适合开头的金句
```

---

## 八、关联 Skill

- **evidence-collector**：用于从新材料中提取论据并写入资料库
