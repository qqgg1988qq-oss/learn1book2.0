# xl-card JSON Schema v1

本文件是 `xl-card` 技能的 JSON 输出规范。生图工具（Lovart 等）按此 schema 解析渲染。

## 顶层结构

```json
{
  "schema": "xl-card/v1",
  "cardType": "long",
  "totalCards": 1,
  "cards": [ ... ]
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `schema` | `string` | ✅ | 固定值 `"xl-card/v1"` |
| `cardType` | `enum` | ✅ | `"long"` \| `"concept"` \| `"quote"` \| `"multi"` |
| `totalCards` | `number` | ✅ | 卡片总数 |
| `cards` | `array` | ✅ | 卡片对象数组 |

## Card 对象

```json
{
  "id": 1,
  "type": "long",
  "title":     { "text": "...", "maxChars": 20, "role": "primary-heading" },
  "subtitle":  { "text": "...", "maxChars": 30, "role": "secondary-heading" },
  "highlight": { "text": "...", "style": "quote-bar" },
  "body":      ["段落1", "段落2"],
  "items":     [{ "label": "...", "text": "..." }],
  "action":    { "text": "..." },
  "footer":    { "signature": "八零后阿力的觉醒日记", "source": "..." }
}
```

### 字段详情

| 字段 | 类型 | 必填 | 长文 | 概念 | 金句 |
|------|------|------|:----:|:----:|:----:|
| `title.text` | `string` | ✅ | ≤20字 | ≤10字 | ≤30字 |
| `subtitle.text` | `string` | ❌ | ≤30字 | ≤25字 | ≤30字 |
| `highlight.text` | `string` | ✅(长文/概念) | 金句 | 大白话 | — |
| `body` | `string[]` | ✅ | 3-5段 | 1段 | 1段(≤50字) |
| `items` | `array` | ❌ | ≤5个 | 固定3个 | — |
| `action.text` | `string` | ❌ | 可选 | — | — |
| `footer.signature` | `string` | ✅ | 固定值 | 固定值 | 固定值 |
| `footer.source` | `string` | ✅ | 来源 | 来源 | 来源 |

### 渲染提示

生图工具按 `type` 选择布局模板：

| `type` | 布局要点 |
|--------|---------|
| `long` | 主标题大字位 → 副标题轻字重 → 金句左侧强调线 → 正文段落 → 条目列表 → 行动提示 → 底部署名 |
| `concept` | 概念名大字位 → 定义副标题 → 类比段落 → 三个递进要点 → 底部署名 |
| `quote` | 金句最大字位(全卡视觉焦点) → 出处轻字 → 解读小字 → 底部署名 |

- `null` 字段表示该卡不需要对应区域，直接跳过不渲染
- `items` 内 `label` 建议加粗/着色，`text` 为常规字重
- `highlight.style: "quote-bar"` 建议左侧加竖线或底色块
