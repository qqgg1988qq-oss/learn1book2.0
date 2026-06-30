# 平台规范 — Platform Specifications

本文档记录微信公众号和头条号编辑器的HTML/CSS兼容性规范，所有输出必须严格遵循。

---

## 微信公众号

### HTML标签白名单

以下标签在公众号编辑器中安全可用：

| 标签 | 用途 | 备注 |
|---|---|---|
| `<section>` | 区块容器 | 最外层容器推荐 |
| `<p>` | 段落 | 主要文本容器 |
| `<span>` | 行内文本 | 用于局部样式 |
| `<div>` | 通用容器 | 部分属性会被过滤 |
| `<h1>`-`<h6>` | 标题 | h1-h3最常用 |
| `<ul>`, `<ol>`, `<li>` | 列表 | 支持良好 |
| `<blockquote>` | 引用块 | 支持良好 |
| `<strong>` | 加粗 | 推荐替代 `<b>` |
| `<em>` | 斜体 | 推荐替代 `<i>` |
| `<a>` | 链接 | 外部链接需完整URL |
| `<img>` | 图片 | 必须使用微信图床URL |
| `<br>` | 换行 | 单标签 |
| `<pre>` | 预格式化 | 代码块 |
| `<code>` | 行内代码 | 配合pre使用 |
| `<hr>` | 分割线 | 支持 |

**被过滤/不推荐使用的标签：**
```
<style>, <script>, <iframe>, <form>, <input>, <table>, <tr>, <td>, <th>,
<article>, <aside>, <header>, <footer>, <nav>, <main>, <figure>, <figcaption>
```

> 特别注意：`<table>` 在公众号中会被过滤或显示异常，一律用 `<p>` 模拟表格。

### CSS兼容性

**只支持行内 style 属性。** 所有CSS必须写成：
```html
<p style="font-size: 15px; color: #333;">文本</p>
```

**安全CSS属性（可靠支持）：**

```
/* 字体与文本 */
font-size, font-weight, font-family, font-style, line-height
color, text-align, text-decoration, letter-spacing

/* 盒模型 */
margin, margin-top, margin-bottom, margin-left, margin-right
padding, padding-top, padding-bottom, padding-left, padding-right
width, max-width, height

/* 边框 */
border, border-top, border-bottom, border-left, border-right
border-radius

/* 背景 */
background, background-color

/* 显示 */
display (block, inline, inline-block, none)

/* 定位 */
text-align (left, center, right, justify)
vertical-align
```

**部分支持/不稳定的CSS属性：**
```
box-shadow — 部分版本支持，不建议依赖
position — 会被重置为 static
float — 不可靠
overflow — 可能被忽略
```

### 图片规范

| 项目 | 规格 |
|---|---|
| 封面图（头条） | 900×383px，≤5MB |
| 封面图（次条） | 200×200px 或 300×300px |
| 正文图片 | ≤1080px宽，≤5MB |
| 支持格式 | bmp, png, jpeg, jpg, gif |
| 图片上传 | 必须先上传到微信图床 |

**图片在HTML中的写法：**
```html
<p style="text-align: center; margin: 20px 0;">
  <img src="https://mmbiz.qpic.cn/xxxxx/0?wx_fmt=png" 
       data-src="https://mmbiz.qpic.cn/xxxxx/0?wx_fmt=png"
       style="max-width: 100%; border-radius: 6px; display: inline-block;"
       alt="图片描述">
</p>
```

### 公众号HTML模板框架

```html
<section style="margin: 0; padding: 16px; font-family: -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Helvetica, Segoe UI, Arial, Roboto, 'PingFang SC', 'miui', 'Hiragino Sans GB', 'Microsoft Yahei', sans-serif; background: #ffffff; color: #3f3f3f;">
  
  <!-- 标题区 -->
  <h1 style="font-size: 22px; font-weight: bold; color: #1a1a1a; margin: 20px 0 25px; padding-bottom: 12px; border-bottom: 2px solid #2c5aa0; line-height: 1.4;">
    文章主标题
  </h1>
  
  <!-- 正文区 -->
  <p style="font-size: 15px; line-height: 1.75; color: #3f3f3f; margin: 20px 0; text-align: justify;">
    正文段落...
  </p>
  
  <!-- 更多内容... -->
  
</section>
```

---

## 今日头条号

### 与公众号的主要差异

| 特性 | 公众号 | 头条号 |
|---|---|---|
| 图片上传 | 必须微信图床 | 头条自动处理 |
| HTML标签 | 严格白名单 | 更宽松 |
| CSS支持 | 仅行内style | 部分class支持 |
| 表格支持 | 不支持 | 有限支持 |
| 代码块 | 需要自定义样式 | 自带代码高亮 |
| 外部链接 | 支持 | 自动转为纯文本 |

### 头条号适配要点

1. **简化嵌套**：头条号编辑器处理复杂嵌套不稳定，层级不超过3层
2. **链接处理**：头条号会过滤外部链接，重要链接用文字说明
3. **代码块**：头条号自带代码块样式，使用 `<pre>` 即可
4. **表格**：可用 `<table>` 但样式有限，建议用列表替代

### 头条号HTML模板框架

```html
<section style="padding: 16px;">
  <h1 style="font-size: 24px; font-weight: bold; color: #222; margin: 20px 0;">
    文章标题
  </h1>
  <p style="font-size: 16px; line-height: 1.8; color: #333; margin: 18px 0;">
    正文内容...
  </p>
</section>
```

---

## 双平台通用规则

为确保同一份HTML在两个平台都能正常显示：

1. **使用 section + p 为主结构**，避免复杂嵌套
2. **所有CSS行内化**，不使用class或id
3. **字体栈使用系统字体**，不引用外部字体文件
4. **颜色使用具体色值**，不使用CSS变量
5. **图片使用通用路径**，用户在各平台编辑器中替换为实际图床链接
6. **避免使用**：
   - position, float, z-index
   - CSS动画和过渡
   - 自定义字体（@font-face）
   - JavaScript
   - iframe

### 系统字体栈（推荐）

```
-apple-system, BlinkMacSystemFont, 'Helvetica Neue', Helvetica, Segoe UI, Arial, Roboto, 'PingFang SC', 'miui', 'Hiragino Sans GB', 'Microsoft Yahei', sans-serif
```
