# 示例：将一篇读书笔记排版为公众号文章

## 输入

**用户说：** "帮我排版这篇文章，做成公众号格式"

**文章内容：**
```markdown
# 深度工作：在碎片化时代找回专注力

在这个信息爆炸的时代，我们的注意力被无限分割。

## 什么是深度工作

深度工作是指在无干扰的状态下进行专注的职业活动，这种活动能够将你的认知能力推向极限。

> 深度工作的能力日益稀缺，而其价值在经济中日益增长。

## 为什么深度工作很重要

1. 高质量工作产出 = 时间 × 专注度
2. 深度工作能帮助你快速掌握复杂技能
3. 深度工作能帮助你实现精英级的产出

## 如何培养深度工作能力

**第一步：选择你的深度工作哲学**

- 禁欲主义哲学：完全切断 shallow work
- 双峰哲学：将时间分为深度和浅度两块
- 节奏哲学：养成固定做深度工作的习惯
- 新闻记者哲学：随时抓住机会进入深度状态

---

**关键结论**：深度工作不是奢侈品，而是必需品。
```

**用户选择：** 风格3 文艺清新

---

## 输出示例

### 生成文件

```
output/
├── deep-work_wechat.html
├── deep-work_toutiao.html
└── deep-work_preview.html
```

### 公众号版本片段 (deep-work_wechat.html)

```html
<!--
  排版风格：文艺清新
  目标平台：微信公众号
  生成时间：2026-05-25 14:30
-->
<section style="margin: 0; padding: 16px; font-family: -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Helvetica, Segoe UI, Arial, Roboto, 'PingFang SC', 'miui', 'Hiragino Sans GB', 'Microsoft Yahei', sans-serif; background: #ffffff; color: #4a5568;">

  <h1 style="font-size: 22px; font-weight: normal; color: #2c3e50; margin: 35px 0 20px; padding-bottom: 10px; border-bottom: 1px solid #7ca982; letter-spacing: 1px;">
    深度工作：在碎片化时代找回专注力
  </h1>

  <p style="font-size: 15px; line-height: 2.0; color: #4a5568; margin: 25px 0; text-align: justify;">
    在这个信息爆炸的时代，我们的注意力被无限分割。
  </p>

  <h2 style="font-size: 17px; font-weight: normal; color: #7ca982; margin: 25px 0 15px; padding-bottom: 8px; border-bottom: 1px dashed #cbd5e0;">
    什么是深度工作
  </h2>

  <p style="font-size: 15px; line-height: 2.0; color: #4a5568; margin: 25px 0; text-align: justify;">
    深度工作是指在无干扰的状态下进行专注的职业活动，这种活动能够将你的认知能力推向极限。
  </p>

  <blockquote style="background: #f8faf8; border-left: 3px solid #7ca982; padding: 18px 22px; margin: 25px 0; color: #5a6c7d; font-size: 14px; line-height: 1.9; border-radius: 0 6px 6px 0;">
    深度工作的能力日益稀缺，而其价值在经济中日益增长。
  </blockquote>

  <h2 style="font-size: 17px; font-weight: normal; color: #7ca982; margin: 25px 0 15px; padding-bottom: 8px; border-bottom: 1px dashed #cbd5e0;">
    为什么深度工作很重要
  </h2>

  <ul style="margin: 15px 0; padding-left: 20px;">
    <li style="margin: 12px 0; color: #4a5568; font-size: 15px; line-height: 2.0;"><span style="color: #7ca982;">❀</span> 高质量工作产出 = 时间 × 专注度</li>
    <li style="margin: 12px 0; color: #4a5568; font-size: 15px; line-height: 2.0;"><span style="color: #7ca982;">❀</span> 深度工作能帮助你快速掌握复杂技能</li>
    <li style="margin: 12px 0; color: #4a5568; font-size: 15px; line-height: 2.0;"><span style="color: #7ca982;">❀</span> 深度工作能帮助你实现精英级的产出</li>
  </ul>

  <hr style="border: none; text-align: center; margin: 30px 0;">
  <p style="text-align: center; color: #a0aec0; font-size: 14px; margin: 0;">~ ~ ~</p>

  <p style="font-size: 15px; line-height: 2.0; color: #4a5568; margin: 25px 0; text-align: justify;">
    <strong style="font-weight: bold; color: #2c3e50;">关键结论</strong>：深度工作不是奢侈品，而是必需品。
  </p>

</section>
```

### 使用方式

1. 用浏览器打开 `deep-work_preview.html` 预览效果
2. 打开 `deep-work_wechat.html`，全选复制 → 粘贴到公众号编辑器
3. 打开 `deep-work_toutiao.html`，全选复制 → 粘贴到头条号编辑器
