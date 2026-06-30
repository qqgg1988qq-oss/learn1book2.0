# 示例：将口播文案拆解为视频场景

## 输入示例

用户提供一篇约 5200 字的关于维特根斯坦的口播文案，要求生成视频场景脚本。

```
请把这篇关于维特根斯坦的口播文案做成视频博客分镜，
风格用学术科技风，目标平台是 B 站。

[文案内容约 5200 字……]
```

## Skill 处理流程

1. **分析文章结构**：识别出 9 个章节（开场 / 早期生涯 / 逻辑哲学论 / 沉默十年 / 转向 / 思想史地位 / 私人面 / 思考 / 总结）
2. **规划场景**：决定拆解为 24 个场景，总时长约 18 分钟
3. **生成 JSON**：按 schema 生成每个场景的完整描述
4. **应用风格**：使用 `academic-tech` 预设
5. **输出**：保存到 `references/example-output.json` 并返回路径

## 输出示例

完整输出参见 [../references/example-output.json](../references/example-output.json)

输出片段（第 1 个场景）：

```json
{
  "scene_id": 1,
  "section": "开场",
  "title": "悬念引入：被遗忘的提问",
  "scene_type": "opening_hook",
  "narration": "我们每天都在使用语言，但你有没有想过……",
  "visual_description": "深蓝灰色背景中，无数细小的中文字符粒子悬浮、缓慢旋转……",
  "text_overlay": ["语言", "提问", "被遗忘的"],
  "suggested_graphics": ["粒子文字云", "巨大半透明问号", "低频涟漪环", "频道 logo"],
  "transition_in": "黑场缓缓淡入",
  "transition_out": "粒子向中心聚合，闪光后切到下一场景",
  "duration_estimate": 25,
  "style_override": null
}
```

## 使用产出

设计师/剪辑师拿到这份 JSON 可以：

1. 按 `scene_id` 顺序逐场制作
2. 用 `visual_description` 作为美术参考或 AI 生图 prompt
3. 用 `text_overlay` 作为字幕/动效文字
4. 用 `transition_in/out` 作为剪辑过渡指南
5. 用 `style_config` 锁定整体调性，避免风格漂移

## 常见调用方式

```
# 默认风格
请把这篇文章做成视频分镜

# 指定风格
按文学温暖风（literary-warm）做成 vlog 分镜

# 自定义风格描述
我希望视觉上偏赛博朋克，霓虹色，节奏快一点

# 保存到指定路径
做成视频脚本，保存到 ./scripts/wittgenstein-v1.json
```
