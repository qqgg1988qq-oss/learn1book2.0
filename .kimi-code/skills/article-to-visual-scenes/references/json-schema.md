# JSON Schema 定义

## 顶层结构

```json
{
  "meta": { ... },
  "style_config": { ... },
  "scenes": [ ... ]
}
```

## `meta` 对象

```json
{
  "meta": {
    "title": "视频标题",
    "source_article": "源文章标识或路径",
    "total_duration_estimate": 1200,
    "scene_count": 24,
    "target_platform": ["bilibili", "youtube"],
    "language": "zh-CN",
    "created_at": "2026-05-24",
    "version": "1.0"
  }
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `title` | string | 视频标题 |
| `source_article` | string | 源文章路径或标识 |
| `total_duration_estimate` | number | 预估总时长（秒） |
| `scene_count` | number | 场景总数 |
| `target_platform` | array | 目标平台 |
| `language` | string | 语言代码 |
| `created_at` | string | 创建日期（YYYY-MM-DD） |
| `version` | string | 脚本版本 |

## `style_config` 对象

```json
{
  "style_config": {
    "preset_name": "academic-tech",
    "color_scheme": {
      "primary": "#1A2B4C",
      "secondary": "#4A6FA5",
      "accent": "#E8B547",
      "background": "#0F1419",
      "text": "#F5F5F0",
      "highlight": "#FF6B6B"
    },
    "typography": {
      "heading_font": "Source Han Serif / 思源宋体",
      "body_font": "Source Han Sans / 思源黑体",
      "quote_font": "FZ Kai Z03 / 方正楷体",
      "code_font": "JetBrains Mono"
    },
    "visual_mood": "深邃、思辨、略带冷峻；以深蓝灰为底，金色和暖红作点缀；图形以几何线条和信息图为主。",
    "music_mood": "氛围电子 + 弦乐铺底，节奏舒缓",
    "pacing": "slow",
    "aspect_ratio": "16:9",
    "resolution": "1920x1080"
  }
}
```

### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `preset_name` | string | 预设名称（参考 style-presets.md） |
| `color_scheme.primary` | hex | 主色 |
| `color_scheme.secondary` | hex | 辅色 |
| `color_scheme.accent` | hex | 强调色 |
| `color_scheme.background` | hex | 背景色 |
| `color_scheme.text` | hex | 主要文字色 |
| `color_scheme.highlight` | hex | 高亮色（关键词强调） |
| `typography.heading_font` | string | 标题字体 |
| `typography.body_font` | string | 正文字体 |
| `typography.quote_font` | string | 引文字体 |
| `typography.code_font` | string | 等宽字体（可选） |
| `visual_mood` | string | 整体视觉氛围描述（静态画面风格） |
| `music_mood` | string | 配乐氛围建议 |
| `pacing` | enum | `slow` / `medium` / `fast` |
| `aspect_ratio` | string | 画幅比例 |
| `resolution` | string | 输出分辨率 |

> **注意**：`style_config` 中**不包含** `animation_style` 字段。本 skill 只生成静态画面描述。

## `scenes[]` 数组

每个场景对象结构：

```json
{
  "scene_id": 1,
  "section": "开场",
  "title": "悬念引入：被遗忘的提问",
  "scene_type": "opening_hook",
  "narration": "我们每天都在使用语言，但你有没有想过……",
  "visual_description": "深蓝灰色背景，中央是一个由无数细小中文字符组成的问号轮廓，字符呈金色，问号外圈微微发光。画面右下角有频道 logo。整体氛围神秘、思辨。色调以深蓝为底，文字带金色高光。",
  "text_overlay": ["语言", "提问", "被遗忘的"],
  "suggested_graphics": [
    "文字粒子云（中文字符为单位）",
    "巨大半透明问号",
    "频道 logo"
  ],
  "transition_note": "黑场 → 本画面",
  "duration_estimate": 25,
  "style_override": null
}
```

### 字段详解

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `scene_id` | integer | 是 | 从 1 开始递增 |
| `section` | string | 是 | 对应文章段落标题 |
| `title` | string | 是 | 场景标题（10-20 字） |
| `scene_type` | enum | 是 | 见下方枚举值 |
| `narration` | string | 是 | 对应口播旁白（可以是完整段落） |
| `visual_description` | string | 是 | **核心字段**，100-200 字静态画面描述，只描述画面里有什么、在什么位置、什么颜色、什么构图。禁止任何动画/运动/特效描述。 |
| `text_overlay` | string[] | 是 | 画面关键词，0-5 个 |
| `suggested_graphics` | string[] | 是 | 静态图形元素清单，不含任何动态/动画词汇 |
| `transition_note` | string | 是 | 简单切换说明，如"切至""叠化""淡入淡出"，不涉及具体动画 |
| `duration_estimate` | integer | 是 | 预估秒数（20-80） |
| `style_override` | object\|null | 否 | 场景级风格覆盖 |

### `scene_type` 枚举值

- `opening_hook` —— 开头钩子
- `concept_explanation` —— 概念解释
- `story_narrative` —— 故事叙述
- `historical_review` —— 历史回顾
- `quote_display` —— 引用展示
- `critical_analysis` —— 批判性分析
- `interactive_question` —— 互动提问
- `summary` —— 总结
- `closing_cta` —— 结尾引导

### `style_override`（可选）

仅在该场景需要偏离整体风格时使用，结构与 `style_config` 子集相同：

```json
{
  "style_override": {
    "color_scheme": {
      "background": "#FFFFFF",
      "text": "#000000"
    },
    "visual_mood": "复古档案风，暖棕色调"
  }
}
```

## 完整最小示例

```json
{
  "meta": {
    "title": "示例视频",
    "source_article": "demo.md",
    "total_duration_estimate": 60,
    "scene_count": 2,
    "target_platform": ["bilibili"],
    "language": "zh-CN",
    "created_at": "2026-05-24",
    "version": "1.0"
  },
  "style_config": { ... },
  "scenes": [
    { "scene_id": 1, ... },
    { "scene_id": 2, ... }
  ]
}
```

## 校验要点

- 所有 `scene_id` 必须连续且唯一
- `duration_estimate` 求和应接近 `meta.total_duration_estimate`
- `scene_count` 必须等于 `scenes` 数组长度
- 颜色字段必须是合法 HEX 格式（`#RRGGBB`）
- `scene_type` 必须是枚举值之一
- `visual_description` 中不得出现动画/运动/特效描述（参见 SKILL.md 禁止词汇表）
