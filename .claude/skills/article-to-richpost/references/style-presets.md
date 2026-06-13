# 风格预设 — Style Presets

本文件定义8种排版风格的完整CSS样式配置。每种风格包含：配色变量、字体配置、元素样式。

> 所有颜色值必须内联到HTML的 style 属性中。公众号编辑器不支持CSS变量或class。

---

## 风格1：现代简约 — Modern Minimal

**适用场景**：通用型、职场号、观点类、人物专访
**代表号**：插座学院、人物、拾遗
**气质**：清晰、专业、不抢戏

### 配色
| 用途 | 色值 |
|---|---|
| 主文字 | #1a1a1a |
| 正文 | #3f3f3f |
| 次要文字 | #888888 |
| 强调色 | #2c5aa0 |
| 背景色 | #ffffff |
| 引用底色 | #f5f7fa |
| 引用边框 | #2c5aa0 |
| 分割线 | #e8e8e8 |

### 元素样式

**主标题 H1：**
- font-size: 22px
- font-weight: bold
- color: #1a1a1a
- margin: 30px 0 20px
- padding-bottom: 12px
- border-bottom: 2px solid #2c5aa0

**副标题 H2：**
- font-size: 18px
- font-weight: bold
- color: #2c5aa0
- margin: 25px 0 15px
- padding-left: 12px
- border-left: 3px solid #2c5aa0

**正文 P：**
- font-size: 15px
- line-height: 1.75
- color: #3f3f3f
- margin: 20px 0
- text-align: justify

**重点 STRONG：**
- font-weight: bold
- color: #1a1a1a

**引用 BLOCKQUOTE：**
- background: #f5f7fa
- border-left: 3px solid #2c5aa0
- padding: 15px 20px
- margin: 20px 0
- color: #555
- font-size: 14px
- line-height: 1.7

**列表 LI：**
- margin: 10px 0
- padding-left: 5px
- 无序列表前缀：●（color: #2c5aa0）

**分割线 HR：**
- border: none
- border-top: 1px solid #e8e8e8
- margin: 30px 0
- text-align: center
- 可用装饰：· · ·（color: #ccc）

**图片 IMG：**
- max-width: 100%
- border-radius: 6px
- display: inline-block
- margin: 15px 0

---

## 风格2：时尚杂志 — Fashion Magazine

**适用场景**：潮流、穿搭、美妆、生活方式
**代表号**：杜绍斐、一条
**气质**：前卫、视觉冲击、高级感

### 配色
| 用途 | 色值 |
|---|---|
| 主文字 | #000000 |
| 正文 | #333333 |
| 次要文字 | #999999 |
| 强调色 | #d4a574 |
| 背景色 | #ffffff |
| 引用底色 | #faf8f5 |
| 引用边框 | #d4a574 |
| 分割线 | #000000 |

### 元素样式

**主标题 H1：**
- font-size: 26px
- font-weight: bold
- color: #000
- letter-spacing: 2px
- text-transform: uppercase（英文）
- margin: 40px 0 20px
- padding-bottom: 15px
- border-bottom: 3px solid #000

**副标题 H2：**
- font-size: 16px
- font-weight: bold
- color: #d4a574
- letter-spacing: 1px
- margin: 30px 0 15px
- padding: 8px 15px
- border: 1px solid #d4a574
- display: inline-block

**正文 P：**
- font-size: 15px
- line-height: 1.8
- color: #333
- margin: 20px 0
- text-align: justify

**重点 STRONG：**
- font-weight: bold
- color: #000
- background: linear-gradient(transparent 60%, #f0dcc5 60%)
- （注：公众号可能不支持渐变，降级为 border-bottom: 2px solid #d4a574）

**引用 BLOCKQUOTE：**
- background: #faf8f5
- padding: 20px 25px
- margin: 25px 0
- color: #555
- font-size: 15px
- font-style: italic
- line-height: 1.8
- border: none
- border-top: 2px solid #d4a574
- border-bottom: 2px solid #d4a574

**列表 LI：**
- margin: 12px 0
- 无序前缀：—（em dash，color: #d4a574）

**分割线 HR：**
- border: none
- height: 3px
- background: #000
- margin: 35px 20%
- width: 60%

**图片 IMG：**
- max-width: 100%
- border-radius: 0（直角更显时尚）
- margin: 20px 0

---

## 风格3：文艺清新 — Literary Fresh

**适用场景**：文学、情感、生活美学、书评、游记
**代表号**：HANS汉声
**气质**：温暖、治愈、有呼吸感

### 配色
| 用途 | 色值 |
|---|---|
| 主文字 | #2c3e50 |
| 正文 | #4a5568 |
| 次要文字 | #a0aec0 |
| 强调色 | #7ca982 |
| 背景色 | #ffffff |
| 引用底色 | #f8faf8 |
| 引用边框 | #7ca982 |
| 分割线 | #e2e8f0 |

### 元素样式

**主标题 H1：**
- font-size: 22px
- font-weight: normal（轻盈感）
- color: #2c3e50
- margin: 35px 0 20px
- padding-bottom: 10px
- border-bottom: 1px solid #7ca982
- letter-spacing: 1px

**副标题 H2：**
- font-size: 17px
- font-weight: normal
- color: #7ca982
- margin: 25px 0 15px
- padding-bottom: 8px
- border-bottom: 1px dashed #cbd5e0

**正文 P：**
- font-size: 15px
- line-height: 2.0（更大行高，呼吸感）
- color: #4a5568
- margin: 25px 0
- text-align: justify

**重点 STRONG：**
- font-weight: bold
- color: #2c3e50

**引用 BLOCKQUOTE：**
- background: #f8faf8
- border-left: 3px solid #7ca982
- padding: 18px 22px
- margin: 25px 0
- color: #5a6c7d
- font-size: 14px
- line-height: 1.9
- border-radius: 0 6px 6px 0

**列表 LI：**
- margin: 12px 0
- 无序前缀：❀（花朵符号，color: #7ca982）

**分割线 HR：**
- border: none
- text-align: center
- margin: 30px 0
- content: "~ ~ ~"（color: #a0aec0, font-size: 14px）

**图片 IMG：**
- max-width: 100%
- border-radius: 12px（更大圆角，柔和）
- margin: 20px 0
- box-shadow: 0 2px 8px rgba(0,0,0,0.06)（如平台支持）

---

## 风格4：高端商务 — Premium Business

**适用场景**：企业号、财经、职场、品牌宣传
**代表号**：晚点LatePost
**气质**：沉稳、大气、可信赖

### 配色
| 用途 | 色值 |
|---|---|
| 主文字 | #0f172a |
| 正文 | #334155 |
| 次要文字 | #94a3b8 |
| 强调色 | #0f4c81 |
| 背景色 | #ffffff |
| 引用底色 | #f1f5f9 |
| 引用边框 | #0f4c81 |
| 分割线 | #cbd5e1 |

### 元素样式

**主标题 H1：**
- font-size: 24px
- font-weight: bold
- color: #0f172a
- margin: 35px 0 20px
- padding-bottom: 14px
- border-bottom: 2px solid #0f4c81

**副标题 H2：**
- font-size: 18px
- font-weight: 600
- color: #0f4c81
- margin: 25px 0 15px
- padding-left: 15px
- border-left: 4px solid #0f4c81

**正文 P：**
- font-size: 15px
- line-height: 1.75
- color: #334155
- margin: 20px 0
- text-align: justify

**重点 STRONG：**
- font-weight: bold
- color: #0f172a

**引用 BLOCKQUOTE：**
- background: #f1f5f9
- border-left: 4px solid #0f4c81
- padding: 16px 22px
- margin: 20px 0
- color: #475569
- font-size: 14px
- line-height: 1.7

**列表 LI：**
- margin: 10px 0
- 无序前缀：■（实心方块，color: #0f4c81）

**分割线 HR：**
- border: none
- border-top: 1px solid #cbd5e1
- margin: 30px 0

**图片 IMG：**
- max-width: 100%
- border-radius: 4px（轻微圆角）
- margin: 20px 0

---

## 风格5：科技极客 — Tech Geek

**适用场景**：互联网、科技产品、编程、数码评测
**代表号**：极客公园、36氪
**气质**：简洁、高效、信息密度高

### 配色
| 用途 | 色值 |
|---|---|
| 主文字 | #e2e8f0（深色模式！）|
| 正文 | #94a3b8 |
| 次要文字 | #64748b |
| 强调色 | #22d3ee（cyan荧光）|
| 背景色 | #0f172a（深色背景）|
| 引用底色 | #1e293b |
| 引用边框 | #22d3ee |
| 分割线 | #334155 |

> ⚠️ 科技风使用深色模式。公众号编辑器粘贴后背景色会变白，需要在代码中显式设置 section 背景色，或改用浅色版本。

### 元素样式（浅色适配版）

**主标题 H1：**
- font-size: 22px
- font-weight: bold
- color: #0f172a
- margin: 30px 0 20px
- padding-bottom: 12px
- border-bottom: 2px solid #22d3ee
- font-family: -apple-system, BlinkMacSystemFont, sans-serif

**副标题 H2：**
- font-size: 17px
- font-weight: 600
- color: #0ea5e9
- margin: 25px 0 12px
- padding: 5px 12px
- background: #f0f9ff
- border-radius: 4px
- display: inline-block

**正文 P：**
- font-size: 15px
- line-height: 1.75
- color: #334155
- margin: 18px 0
- text-align: justify
- font-family: -apple-system, sans-serif

**重点 STRONG：**
- font-weight: bold
- color: #0f172a
- background: #cffafe（淡青底色高亮）
- padding: 2px 4px
- border-radius: 3px

**引用 BLOCKQUOTE：**
- background: #f8fafc
- border-left: 3px solid #22d3ee
- padding: 15px 20px
- margin: 20px 0
- color: #475569
- font-size: 14px
- line-height: 1.7
- font-family: monospace

**代码 CODE/PRE：**
- background: #0f172a
- color: #e2e8f0
- padding: 15px 18px
- border-radius: 6px
- font-size: 13px
- line-height: 1.6
- overflow-x: auto

**列表 LI：**
- margin: 8px 0
- 无序前缀：›（右尖括号，color: #22d3ee）

**分割线 HR：**
- border: none
- border-top: 1px dashed #cbd5e1
- margin: 25px 0

**图片 IMG：**
- max-width: 100%
- border-radius: 6px
- margin: 15px 0

---

## 风格6：干货科普 — Knowledge Popular

**适用场景**：教育、科普、方法论、技巧分享
**代表号**：好好住
**气质**：活泼、清晰、易于理解

### 配色
| 用途 | 色值 |
|---|---|
| 主文字 | #1e293b |
| 正文 | #475569 |
| 次要文字 | #94a3b8 |
| 强调色 | #f59e0b（琥珀色）|
| 背景色 | #ffffff |
| 引用底色 | #fffbeb |
| 引用边框 | #f59e0b |
| 分割线 | #e2e8f0 |

### 元素样式

**主标题 H1：**
- font-size: 22px
- font-weight: bold
- color: #1e293b
- margin: 30px 0 18px
- padding: 10px 15px
- background: #fffbeb
- border-left: 4px solid #f59e0b

**副标题 H2：**
- font-size: 17px
- font-weight: bold
- color: #d97706
- margin: 22px 0 12px
- padding-bottom: 6px
- border-bottom: 2px solid #fef3c7

**正文 P：**
- font-size: 15px
- line-height: 1.8
- color: #475569
- margin: 18px 0
- text-align: justify

**重点 STRONG：**
- font-weight: bold
- color: #1e293b
- background: #fef3c7（淡黄色底色）
- padding: 2px 6px
- border-radius: 3px

**引用 BLOCKQUOTE：**
- background: #fffbeb
- border-left: 4px solid #f59e0b
- padding: 15px 20px
- margin: 20px 0
- color: #78350f
- font-size: 14px
- line-height: 1.75

**列表 LI：**
- margin: 10px 0
- 无序前缀：✓（对勾，color: #f59e0b）
- 有序前缀使用数字圆圈效果：①②③

**分割线 HR：**
- border: none
- text-align: center
- margin: 25px 0
- content: "—— ✦ ——"（color: #f59e0b）

**图片 IMG：**
- max-width: 100%
- border-radius: 8px
- margin: 18px 0
- border: 1px solid #fef3c7

---

## 风格7：东方美学 — Oriental Aesthetics

**适用场景**：文化、历史、传统艺术、茶道/书法
**代表号**：谁最中国
**气质**：典雅、古朴、东方意境

### 配色
| 用途 | 色值 |
|---|---|
| 主文字 | #2d2a26 |
| 正文 | #5c5650 |
| 次要文字 | #a39e99 |
| 强调色 | #b22222（中国红）|
| 背景色 | #fdfcf8（米白纸张）|
| 引用底色 | #faf7f2 |
| 引用边框 | #b22222 |
| 分割线 | #d4cec6 |

### 元素样式

**主标题 H1：**
- font-size: 24px
- font-weight: bold
- color: #2d2a26
- margin: 35px 0 20px
- padding-bottom: 15px
- border-bottom: 2px solid #b22222
- letter-spacing: 3px（宽字距）

**副标题 H2：**
- font-size: 17px
- font-weight: bold
- color: #8b4513（赭石色）
- margin: 25px 0 15px
- padding-bottom: 8px
- border-bottom: 1px solid #d4cec6
- letter-spacing: 2px

**正文 P：**
- font-size: 16px（稍大，传统阅读感）
- line-height: 2.0
- color: #5c5650
- margin: 25px 0
- text-align: justify
- text-indent: 2em（首行缩进，传统排版）

**重点 STRONG：**
- font-weight: bold
- color: #b22222

**引用 BLOCKQUOTE：**
- background: #faf7f2
- border-left: 3px solid #b22222
- padding: 18px 22px
- margin: 25px 0
- color: #6b6259
- font-size: 15px
- line-height: 1.9
- border-radius: 0 8px 8px 0

**列表 LI：**
- margin: 12px 0
- 无序前缀：◆（菱形，color: #b22222）

**分割线 HR：**
- border: none
- text-align: center
- margin: 30px 0
- content: "· ∿ ∿ ·"（水波纹装饰）

**图片 IMG：**
- max-width: 100%
- border-radius: 4px
- margin: 20px 0
- padding: 6px
- background: #f5f0e8（仿宣纸边框）

---

## 风格8：条漫叙事 — Comic Narrative

**适用场景**：故事、幽默、GQ式叙事、轻松话题
**代表号**：GQ实验室
**气质**：节奏感强、视觉引导、对话感

### 配色
| 用途 | 色值 |
|---|---|
| 主文字 | #000000 |
| 正文 | #333333 |
| 次要文字 | #888888 |
| 强调色 | #000000 |
| 背景色 | #ffffff |
| 引用底色 | #f5f5f5 |
| 引用边框 | #000000 |
| 分割线 | #000000 |

### 元素样式

**主标题 H1：**
- font-size: 28px（更大，冲击力强）
- font-weight: 900（极粗）
- color: #000
- margin: 40px 0 25px
- line-height: 1.3
- letter-spacing: -0.5px

**副标题 H2：**
- font-size: 20px
- font-weight: bold
- color: #000
- margin: 30px 0 15px
- padding: 0

**正文 P：**
- font-size: 16px
- line-height: 2.0（大行高制造呼吸节奏）
- color: #333
- margin: 25px 0
- text-align: left（左对齐，更有对话感）

**短句/强调 STRONG：**
- font-weight: 900
- color: #000
- font-size: 18px
- display: block
- margin: 20px 0
- text-align: center（独句居中，制造停顿）

**引用 BLOCKQUOTE：**
- background: #f5f5f5
- border: 2px solid #000
- padding: 20px 25px
- margin: 25px 0
- color: #000
- font-size: 16px
- font-weight: bold
- line-height: 1.6
- text-align: center

**列表 LI：**
- margin: 15px 0
- font-size: 16px
- 无序前缀：▸（三角，color: #000）

**分割线 HR：**
- border: none
- height: 2px
- background: #000
- margin: 35px 10%
- width: 80%

**图片 IMG：**
- max-width: 100%
- border-radius: 0（直角更锐利）
- margin: 25px 0

---

## 快速选择指南

当用户不确定选什么风格时，根据内容类型推荐：

```
职场/商业/财经/观点 → 1 现代简约 或 4 高端商务
文学/情感/生活美学 → 3 文艺清新
科技/互联网/产品 → 5 科技极客
潮流/时尚/美妆 → 2 时尚杂志
教育/知识/科普 → 6 干货科普
文化/历史/传统 → 7 东方美学
轻松/幽默/故事 → 8 条漫叙事
```
