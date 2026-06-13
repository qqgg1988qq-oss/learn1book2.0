# 风格预设库

本文件定义可选的视觉风格预设。生成 `style_config` 时，可基于这些预设的字段填充。

用户可以：
1. 直接指定预设名（如 `academic-tech`）
2. 描述风格意图，由 Claude 匹配最接近的预设并微调
3. 完全自定义

---

## 1. `academic-tech` —— 学术科技风（默认）

适合：哲学思辨、学术解读、深度内容、思想史回顾

```json
{
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
    "quote_font": "FZ Kai Z03 / 方正楷体"
  },
  "visual_mood": "深邃、思辨、略带冷峻；以深蓝灰为底，金色与暖红作点缀；图形以几何线条和信息图为主；画面简洁克制",
  "music_mood": "氛围电子 + 弦乐铺底，节奏舒缓",
  "pacing": "slow"
}
```

---

## 2. `literary-warm` —— 文学温暖风

适合：文学解读、散文、人物故事、温情叙事

```json
{
  "preset_name": "literary-warm",
  "color_scheme": {
    "primary": "#8B4513",
    "secondary": "#D2A679",
    "accent": "#C97B4F",
    "background": "#F5EFE0",
    "text": "#3A2E20",
    "highlight": "#A0522D"
  },
  "typography": {
    "heading_font": "FZ Song Z02 / 方正宋刻本秀楷",
    "body_font": "Source Han Serif / 思源宋体",
    "quote_font": "FZ Kai Z03 / 方正楷体"
  },
  "visual_mood": "复古纸张、暖黄光线、手写笔触；插画风为主，弱化数字感；画面温馨有呼吸感",
  "music_mood": "钢琴 + 木吉他，民谣或新古典氛围",
  "pacing": "slow"
}
```

---

## 3. `cyber-glitch` —— 赛博故障风

适合：批判性内容、技术反思、亚文化、科幻思辨

```json
{
  "preset_name": "cyber-glitch",
  "color_scheme": {
    "primary": "#00FFD1",
    "secondary": "#FF00A8",
    "accent": "#FFE600",
    "background": "#0A0A12",
    "text": "#E0E0FF",
    "highlight": "#FF3860"
  },
  "typography": {
    "heading_font": "Orbitron / 方正粗黑",
    "body_font": "JetBrains Mono / 等距更纱黑体",
    "quote_font": "Press Start 2P"
  },
  "visual_mood": "霓虹色调、暗黑背景、数字噪点、终端美学；高对比度、视觉冲击力强",
  "music_mood": "Synthwave / Cyberpunk 电子，带失真和工业感",
  "pacing": "fast"
}
```

---

## 4. `documentary-grey` —— 纪实灰调风

适合：历史回顾、调查报道、严肃新闻、社会观察

```json
{
  "preset_name": "documentary-grey",
  "color_scheme": {
    "primary": "#2C2C2C",
    "secondary": "#6B6B6B",
    "accent": "#B8860B",
    "background": "#1C1C1C",
    "text": "#E8E8E8",
    "highlight": "#CD5C5C"
  },
  "typography": {
    "heading_font": "Source Han Sans Heavy / 思源黑体 Heavy",
    "body_font": "Source Han Sans / 思源黑体",
    "quote_font": "FZ Song / 方正书宋"
  },
  "visual_mood": "黑白灰为主，偶现暖色点缀；档案照片、时间轴、文献质感；写实克制",
  "music_mood": "管弦低音 + 不安和声；纪录片配乐式",
  "pacing": "medium"
}
```

---

## 5. `minimalist-zen` —— 极简禅意风

适合：哲学冥想、东方思想、生活美学、心理学

```json
{
  "preset_name": "minimalist-zen",
  "color_scheme": {
    "primary": "#2F2F2F",
    "secondary": "#A8A39B",
    "accent": "#C8B273",
    "background": "#F8F5EF",
    "text": "#2F2F2F",
    "highlight": "#8B0000"
  },
  "typography": {
    "heading_font": "FZ Kai / 方正楷体",
    "body_font": "Source Han Serif Light / 思源宋体 Light",
    "quote_font": "FZ Kai Z03 / 方正楷体"
  },
  "visual_mood": "宣纸质感、水墨笔触、大量留白；东方美学；色彩克制；画面宁静",
  "music_mood": "古琴、尺八、雨声；环境音 + 极简旋律",
  "pacing": "slow"
}
```

---

## 6. `vibrant-pop` —— 鲜活流行风

适合：科普轻量、生活方式、年轻向、Vlog

```json
{
  "preset_name": "vibrant-pop",
  "color_scheme": {
    "primary": "#FF6B9D",
    "secondary": "#4ECDC4",
    "accent": "#FFE66D",
    "background": "#FFFFFF",
    "text": "#1A1A2E",
    "highlight": "#FF4757"
  },
  "typography": {
    "heading_font": "Alibaba PuHuiTi Heavy / 阿里巴巴普惠体 Heavy",
    "body_font": "Alibaba PuHuiTi / 阿里巴巴普惠体",
    "quote_font": "HYWenHei / 汉仪文黑"
  },
  "visual_mood": "高饱和色块、扁平插画、潮流元素、贴纸表情；画面活泼明快",
  "music_mood": "City Pop / Indie Pop / Electro，节奏明亮",
  "pacing": "fast"
}
```

---

## 风格匹配建议

| 内容类型 | 推荐预设 |
|---------|---------|
| 哲学/思想史 | `academic-tech` 或 `minimalist-zen` |
| 文学解读 | `literary-warm` |
| 科技批判/亚文化 | `cyber-glitch` |
| 历史/纪实 | `documentary-grey` |
| 东方哲学/禅意 | `minimalist-zen` |
| 科普/生活 | `vibrant-pop` |

## 自定义建议

若用户提供文字描述，按以下关键词识别预设：

- 出现"学术""深度""思辨""哲学" → `academic-tech`
- 出现"文学""散文""温暖""怀旧""手绘" → `literary-warm`
- 出现"赛博""未来""故障""科幻""黑客" → `cyber-glitch`
- 出现"纪录片""历史""档案""黑白" → `documentary-grey`
- 出现"禅意""水墨""留白""东方""极简" → `minimalist-zen`
- 出现"年轻""活泼""轻松""日常""vlog" → `vibrant-pop`

无明确匹配时，默认使用 `academic-tech`。
