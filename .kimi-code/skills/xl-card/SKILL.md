---
name: xl-card
description: |
  文案卡片结构化工具。将内容铸成结构清晰的 JSON 文案卡片，供 Lovart 等生图工具直接解析渲染。
  输出纯 JSON 文件，统一保存到 `/Users/chouchou/Documents/Obsidian Vault/九局下半怎么破局/概念卡片`，不输出 HTML、不截图、不画 ASCII 框。

  与 ljg-card 的关系：xl-card 出文案 JSON → ljg-card 或其他生图工具出图。

  触发词："写张卡"、"文案卡片"、"结构化这张卡"、"卡片文案"、"做成卡"、"提炼成卡片"、
  "铸文案"、"文案铸卡"、"概念卡文案"、"金句卡"

  四种模具：
  -l（默认）长文卡：文章→结构化卡片 JSON
  -c 概念卡：单个概念→定义+类比+要点 JSON
  -q 金句卡：一句话→视觉化文案 JSON
  -m 多卡：长内容→多张卡片序列 JSON
---

# xl-card: 文案铸卡

将内容铸成结构化文案卡片。内容进去，结构清晰的文案描述出来。模具决定组织形式。

**与 ljg-card 的本质区别**：xl-card 输出结构化 JSON 文案数据，供生图工具（Lovart 等）直接解析渲染。不生成 HTML，不截图。

## 参数

| 参数 | 模具 | 说明 |
|------|------|------|
| `-l`（默认） | 长文卡 | 文章→一张结构化阅读卡。提取标题、金句、条目、行动要点 |
| `-c` | 概念卡 | 单个概念→名称+一句话定义+类比+三个要点 |
| `-q` | 金句卡 | 一句话/一段话→主视觉文案+来源标注 |
| `-m` | 多卡 | 长内容自动切分为多张卡片序列，每张独立成卡 |

## 共享基础

### 获取内容

- URL → WebFetch 获取
- 粘贴文本 → 直接使用
- 文件路径 → Read 获取

### 文件命名与输出路径

**输出目录固定为**：`/Users/chouchou/Documents/Obsidian Vault/九局下半怎么破局/概念卡片`

**文件名**：从卡片内容提取概念名或核心标题作为 `{name}`，保存为 `{name}.json`。

命名规则：
- 中文直接用，去标点，≤ 20 字符。
- 空格、特殊符号替换为下划线 `_`。
- 多卡模式（`-m`）下，每张卡单独保存，文件名为 `卡{N}_{name}.json`。

不同模具的 `{name}` 来源：
- `-l` 长文卡：取 `cards[0].title.text`（主标题）
- `-c` 概念卡：取 `cards[0].title.text`（概念名）
- `-q` 金句卡：取金句核心词或 `cards[0].title.text` 的前 20 字符
- `-m` 多卡：每张卡取各自的 `title.text`

### 署名

卡片底部署名「八零后阿力的觉醒日记」。右侧标注内容来源（可选）。

---

## 品味准则（文案版）

**所有模具共享**。执行任何模具前，先 Read `references/taste.md`。

核心：反 AI 文案腔。禁用词："赋能""无缝""释放""下一代""解锁""助力""打造""引领"。
用具体动词，用真实数据（不用 99.99% 式假数据），用有创意的人名（不用 John Doe）。

## 执行

根据参数选择模具，Read `references/taste.md` + 对应的 mode 文件，按步骤执行：

### -l（默认）：长文卡

Read `references/mode-long.md`，按其步骤执行。

输出结构：主标题 → 副标题（可选）→ 金句高亮 → 正文段落 → 条目组（可选）→ 行动提示（可选）→ 署名行

### -c：概念卡

Read `references/mode-concept.md`，按其步骤执行。

输出结构：概念名 → 一句话定义 → 通俗类比 → 三个要点 → 署名行

### -q：金句卡

Read `references/mode-quote.md`，按其步骤执行。

输出结构：金句正文（大字位）→ 出处/作者 → 一句解读（可选）→ 署名行

### -m：多卡

Read `references/mode-long.md`（每张卡按长文卡规则），按其步骤执行。

输出结构：每张卡独立标注「卡 1/N」「卡 2/N」……，各卡内容不重复，逻辑递进。

---

## 输出格式（JSON Schema）

所有模具统一输出以下 JSON 结构。生图工具按 `cardType` 选择渲染模板，按 `elements` 中的字段逐层排版。

### 保存规则

1. 先生成完整 JSON 内容。
2. 按上述命名规则确定文件名。
3. 将 JSON 文件写入固定输出目录：`/Users/chouchou/Documents/Obsidian Vault/九局下半怎么破局/概念卡片`。
4. 目录不存在时自动创建。
5. 保存后向用户报告文件完整路径。

### JSON Schema 定义

```json
{
  "schema": "xl-card/v1",
  "cardType": "long",
  "totalCards": 1,
  "cards": [
    {
      "id": 1,
      "type": "long",
      "title": {
        "text": "主标题文案",
        "maxChars": 20,
        "role": "primary-heading"
      },
      "subtitle": {
        "text": "副标题文案",
        "maxChars": 30,
        "role": "secondary-heading"
      },
      "highlight": {
        "text": "金句文案",
        "style": "quote-bar"
      },
      "body": [
        "段落1文案",
        "段落2文案",
        "段落3文案"
      ],
      "items": [
        { "label": "条目标题", "text": "条目正文" }
      ],
      "action": {
        "text": "行动引导文案"
      },
      "footer": {
        "signature": "八零后阿力的觉醒日记",
        "source": "Dan Koe"
      }
    }
  ]
}
```

### 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `schema` | string | ✅ | 固定值 `"xl-card/v1"`，生图工具用于校验版本 |
| `cardType` | string | ✅ | `"long"` / `"concept"` / `"quote"` / `"multi"` |
| `totalCards` | number | ✅ | 卡片总数，`-m` 多卡模式 > 1 |
| `cards` | array | ✅ | 卡片数组，单卡模式长度为 1 |
| `cards[].id` | number | ✅ | 卡片序号，从 1 开始 |
| `cards[].type` | string | ✅ | 该卡的实际类型，多卡模式下每张可以不同 |
| `cards[].title` | object | ✅ | 主标题，`text` 为文案，`maxChars` 为字数上限，`role` 标识层级 |
| `cards[].subtitle` | object | ❌ | 副标题，选填时 `text` 为空字符串 |
| `cards[].highlight` | object | ✅ | 金句/高亮文案，`style` 建议渲染风格 |
| `cards[].body` | string[] | ✅ | 正文段落数组，每段一句话或一个意群 |
| `cards[].items` | array | ❌ | 条目组，每个条目含 `label`（≤8字标题）和 `text`（1-2句正文） |
| `cards[].action` | object | ❌ | 行动提示，引导读者下一步动作 |
| `cards[].footer` | object | ✅ | 署名行，`signature` 固定为「八零后阿力的觉醒日记」，`source` 为内容来源 |

### 各模具的字段映射

#### -l 长文卡

```json
{
  "type": "long",
  "title":        { "text": "≤20字观点性标题", "maxChars": 20, "role": "primary-heading" },
  "subtitle":     { "text": "≤30字语境补充", "maxChars": 30, "role": "secondary-heading" },
  "highlight":    { "text": "最有冲击力的一句话", "style": "quote-bar" },
  "body":         ["段落1", "段落2", "段落3"],
  "items":        [{ "label": "≤8字", "text": "1-2句解释" }],
  "action":       { "text": "一句动作引导" },
  "footer":       { "signature": "八零后阿力的觉醒日记", "source": "Dan Koe" }
}
```

- `title.text` ≤20 字，观点性或悬念性，不能用原文标题
- `body` 3-5 段，压缩率 70-80%
- `items` ≤5 个，超过需合并
- `action.text` 收在具体动作，不做解释

#### -c 概念卡

```json
{
  "type": "concept",
  "title":        { "text": "概念名称", "maxChars": 10, "role": "primary-heading" },
  "subtitle":     { "text": "一句话定义", "maxChars": 25, "role": "secondary-heading" },
  "highlight":    { "text": "大白话金句", "style": "quote-bar" },
  "body":         ["日常生活类比（1-2句）"],
  "items":        [
    { "label": "≤8字要点1", "text": "知道层面" },
    { "label": "≤8字要点2", "text": "理解层面" },
    { "label": "≤8字要点3", "text": "应用层面" }
  ],
  "action":       null,
  "footer":       { "signature": "八零后阿力的觉醒日记", "source": "Dan Koe" }
}
```

- `title.text` ≤10 字，概念名称
- `body` 只有 1 段，用日常场景类比
- `items` 固定 3 个，递进：知道 → 理解 → 应用
- `action` 为空

#### -q 金句卡

```json
{
  "type": "quote",
  "title":        { "text": "金句原文", "maxChars": 30, "role": "primary-heading" },
  "subtitle":     { "text": "——《出处》作者", "maxChars": 30, "role": "secondary-heading" },
  "highlight":    null,
  "body":         ["一句延伸解读（≤50字），不是翻译是追问"],
  "items":        null,
  "action":       null,
  "footer":       { "signature": "八零后阿力的觉醒日记", "source": "Dan Koe" }
}
```

- `title.text` ≤30 字，原文金句一字不改
- `body` 只有 1 段，加一层追问而非解释
- `highlight` / `items` / `action` 均为空

#### -m 多卡

```json
{
  "cardType": "multi",
  "totalCards": 6,
  "cards": [
    { "id": 1, "type": "concept", ... },
    { "id": 2, "type": "concept", ... },
    ...
  ]
}
```

- `cardType` 为 `"multi"`
- `totalCards` 为实际卡片总数
- 每张卡独立成对象，各自遵循对应模具的字段规则
- 各卡内容不重复，按逻辑递进排列

### 输出规则总结

| 规则 | 适用范围 | 说明 |
|------|---------|------|
| `title.text` 字数上限 | 长文 20 / 概念 10 / 金句 30 | 超限截断或重写 |
| `body` 段数 | 长文 3-5 段 / 概念 1 段 / 金句 1 段 | 每段 1-3 句 |
| `items` 个数 | ≤5（概念卡固定 3） | 超过合并 |
| `items[].label` | ≤8 字 | 短标题 |
| 总字数 | 长文 200-500 / 概念 100-200 / 金句 ≤100 | 整个 cards[].body + items 的总字数 |
| `footer.signature` | 固定值 | 「八零后阿力的觉醒日记」 |
| `footer.source` | 必填 | 从内容中提取来源 |

---

## 质量自检清单

输出前检查：
- [ ] JSON 结构完整（schema / cardType / totalCards / cards 四字段不缺）？
- [ ] `title.text` 字数是否在对应模具的上限内？
- [ ] 金句是否能独立传播（`highlight.text` 截出来就能用）？
- [ ] 正文是否有段落节奏（`body` 数组内长短段交替）？
- [ ] 是否避免了 AI 文案腔（赋能/无缝/释放/打造/引领等禁用词）？
- [ ] `items` 数量是否在限制内？
- [ ] `footer.signature` 是否为「八零后阿力的觉醒日记」？
- [ ] `footer.source` 是否已标注？
- [ ] 多卡模式下 `totalCards` 是否与 `cards` 数组长度一致？
- [ ] JSON 是否合法（无 trailing commas，双引号正确）？
- [ ] 文件是否已保存到 `/Users/chouchou/Documents/Obsidian Vault/九局下半怎么破局/概念卡片`？
- [ ] 文件名是否使用了卡片概念名（中文、去标点、≤20字符）？
