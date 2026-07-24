# learnAbook — Claude Code / Kimi Code 技能集合

基于 Claude Code / Kimi Code 的自动化技能集合（共 33 个 skill），覆盖 **AI 深度读书**、**AI 视频/图文内容创作** 和 **音频转写** 三大工作流。

---

## 技能总览

### 一、AI 深度读书工作流

| 技能 | 作用 | 何时使用 |
|------|------|----------|
| `/book-splitter` | 将 PDF 按目录拆分为章节 Markdown | 拿到一本新书，先拆 |
| `/ocr-corrector` | 自动检测并修复扫描 PDF 的 OCR 排版错误 | 拆分后发现乱码、断裂句子、页码残留 |
| `/deep-reader` | 单章精读，10 维度提取知识点 | 对单篇文章/章节做精读 |
| `/book-master` | 一键完成：拆分 → 过滤 → 并行精读 | 完整精读一本书（推荐） |
| `/book-reader` | 生成左右分栏交互式 HTML 阅读页面 | 想在浏览器中高亮概念、滚动阅读 |
| `/book-qa` | 基于已提取的知识点回答提问 | 读完后有问题想问 |
| `/book-reading-share` | 读书分享口播文案一站式（精读 → 论据收集 → 口播） | 把整本书做成一期读书分享 |
| `/batch-knowledge-extractor` | 批量精读多个文件（PDF/MD/TXT/SRT）并整合总报告 | 处理一批资料而非一本书 |
| `/evidence-collector` | 从材料提取概念/数据/案例/金句存入论据库 | 读完想沉淀写作素材 |
| `/evidence-query` | 按主题/场景/质量分从论据库检索素材 | 写作前找论据支撑 |

### 二、AI 视频/图文内容创作工作流

| 技能 | 作用 | 何时使用 |
|------|------|----------|
| `/broadcast-maker` | 文章 → 深度精读 → 口播文案（一站式） | 输入文章，直接输出视频文案 |
| `/content-to-script` | 精读报告 → 口播文案 | 已有精读报告，转为视频脚本 |
| `/batch-content-to-script` | 批量把多份精读报告转成口播文案 | 一次处理整本书的报告 |
| `/content-to-human-script` | 内容 → 人工口播文案 | 需要更口语化、带语气标注的脚本 |
| `/narrative-to-script` | 叙事内容 → 视频脚本 | 故事类内容转视频 |
| `/story-narration-script` | 剧情类内容 → 口播讲解稿 | 小说/剧情解说（情节拆解→成稿） |
| `/article-to-richpost` | 文章 → 公众号/头条号富文本 HTML | 直接粘贴到编辑器排版发布 |
| `/article-to-visual-richpost` | 文章 → 视觉场景 JSON + 图文排版 HTML | 图文混排一站式产出 |
| `/article-to-visual-scenes` | 文章/文案 → 视觉场景分镜 JSON | 需要为视频制作静态分镜画面 |
| `/text-to-image-prompt` | 短文 → 写实场景 AI 生图提示词（图中不带文字） | 给文章/短文配图 |
| `/text-humanizer-zh` | 中文文本润色 | 让机器生成的文字更自然 |

### 三、头条/引流/写作配套

| 技能 | 作用 | 何时使用 |
|------|------|----------|
| `/article-viral-hook` | 文章 → 痛点匹配 + AA/AG 两段式引流短帖 + 爆款标题 | 给文章写推广引流帖 |
| `/article-to-han-post` | 文章 → 韩寒风格引流帖（三阶段流水线） | 要韩寒口语化风格的二创 |
| `/toutiao-title-craft` | 今日头条爆款标题 + 标签（也可做公众号 SEO 标题） | 发布前起标题 |
| `/toutiao-comment-generator` | 按话题/文章 + 目标情绪生成高互动头条评论 | 评论区引流、蹭热点 |
| `/hot-pain-match` | 抓取今日头条 + 微信热搜，匹配 40 岁痛点图谱 | 找当日借势热点切入点 |
| `/apag-writing-outline` | APAG 框架生成说服性写作大纲 | 写销售页/Newsletter/口播大纲 |
| `/article-claims-extractor` | 提取文章的核心观点、分论点和隐含主张 | 做评论、摘要、知识整理 |
| `/article-claims-to-card` | 观点提取 + 调用 xl-card 铸卡一站式 | 把文章观点做成概念卡 |
| `/xl-card` | 文案 → 结构化 JSON 概念卡片 | 供 Lovart/ljg-card 等生图工具渲染 |

### 四、其他

| 技能 | 作用 | 何时使用 |
|------|------|----------|
| `/audio2text` | 音频文件 → 文本（讯飞语音转写） | 转录播客、会议录音、视频音频 |
| `/council` | 多历史思想家角色对复杂问题做结构化审议 | 需要多角度深度分析 |

## 快速开始

### 读书工作流

#### 场景一：完整精读一本书（最常用）

```
/book-master /Users/chouchou/Desktop/myProject/learnAbook/books/有意识的心灵：一种基础理论研究.pdf
```

自动完成：
1. 按目录拆分 PDF 为章节文件
2. 过滤掉封面、目录、参考文献等非内容章节
3. 并行启动子代理，逐章调用 `/deep-reader`
4. 生成总索引 `_master-index.md`

耗时取决于章节数量和每章长度，全自动无需干预。

### 场景二：只拆分书籍

```
/book-splitter /Users/chouchou/Desktop/myProject/learnAbook/books/xxxxx.pdf --level=1
```

参数：
- `--level=1` — 仅按章拆分（默认）
- `--level=2` — 按章+节拆分
- `--scan=image` — 扫描版 PDF 渲染为图片（默认）
- `--scan=ocr` — 扫描版 PDF OCR 提取文字

### 场景三：校正 OCR 错误

扫描版 PDF 拆分后常有乱码、断裂句子、页码残留等问题：

```
/ocr-corrector /Users/chouchou/Desktop/myProject/learnAbook/有意识的心灵：一种基础理论研究
```

自动修复 5 类问题：乱码片段、断裂句子、多余空行、页码残留、OCR 错字。直接修改 `chapters/` 下的源文件。

### 场景四：生成交互式阅读页面

在浏览器中阅读原文，左侧正文、右侧概念卡片：

```
/book-reader /Users/chouchou/Desktop/myProject/learnAbook/有意识的心灵：一种基础理论研究
```

特性：概念高亮、点击关联、滚动联动、进度追踪、暗色模式。

### 场景五：精读单篇文章

```
/deep-reader ./article.md
```

或直接粘贴文本：

```
/deep-reader
[粘贴文章全文]
```

输出 10 维度结构化精读报告。

### 场景六：读完后的问答

```
/book-qa /Users/chouchou/Desktop/myProject/learnAbook/有意识的心灵：一种基础理论研究
```

然后直接提问：

```
用户：作者如何定义"有意识的心灵"？
Claude: [基于 reports/ 中的知识点回答]

用户：那和笛卡尔的心身二元论有什么关系？
Claude: [整合多章知识回答]
```

> ⚠️ `/book-qa` 必须提供**完整绝对路径**，不能只写书名。

### 场景七：整本书做成读书分享口播

```
/book-reading-share /Users/chouchou/Desktop/myProject/learnAbook/某本书
```

自动完成：各章节深度精读 → 收集概念/数据/案例/金句论据 → 融合全书总索引生成一篇有人味的读书分享口播文案。

### 场景八：沉淀与检索论据库

```
/evidence-collector ./report.md        # 把材料里的概念/数据/案例/金句存进论据库
/evidence-query 中年失业               # 写作前按主题检索素材
```

论据库统一存放在 Obsidian 参考资料目录，入库前自动去重/合并。

### 视频内容创作工作流

#### 场景九：文章转视频文案

```
/broadcast-maker ./article.md
```

自动完成：深度精读（10 维度分析）→ 检索本地论据库补充素材 → 询问视频时长 → 生成口播文案 → 保存到 Obsidian 博客目录。

#### 场景十：已有精读报告转视频文案

```
/content-to-script ./report.md --duration 8min
```

#### 场景十一：文案转视觉分镜

```
/article-to-visual-scenes ./script.md
```

输出 JSON 分镜文件，每个场景包含：标题、静态画面描述（背景/主体/构图/色彩/文字），可直接用于 AI 生图。

#### 场景十二：文章一站式图文排版

```
/article-to-visual-richpost ./article.md
```

先拆解为视觉场景 JSON，再按场景位置生成排好版的富文本 HTML，可直接粘贴进公众号/头条号编辑器。

#### 场景十三：中文文本润色

```
/text-humanizer-zh ./draft.md
```

让机器生成的文字更自然、更像人写的。

### 头条引流工作流

#### 场景十四：热搜找切入点

```
/hot-pain-match
```

自动抓取今日头条 + 微信实时热搜，与 40 岁中年危机痛点图谱（20 个痛点）交叉匹配，输出「最具创作价值」的热搜排行和切入角度。

#### 场景十五：起标题 + 写引流帖

```
/toutiao-title-craft ./article.md      # 至少 10 个爆款标题候选 + 推荐标签
/article-viral-hook ./article.md       # 痛点匹配 + AA/AG 两段式引流短帖
/toutiao-comment-generator             # 按话题/文章生成 5 种风格的高互动评论
```

### 音频处理

#### 场景十六：音频转文字

```
/audio2text ./recording.mp3
/audio2text ./meeting.wav --language autodialect
```

基于讯飞语音转写大模型，支持：
- 中英 + 202 种方言免切换识别（`autodialect`）
- 37 个语种识别（`autominor`）
- 角色分离（多说话人）
- 口语规整与顺滑处理

**配置**：在项目根目录创建 `.env` 文件存放 API 密钥（已加入 `.gitignore`）：

```bash
# .env
XF_APPID=your-appid
XF_API_KEY=your-apikey
XF_API_SECRET=your-apisecret
```

## 完整工作流

### 读书工作流

```
输入 PDF
    ↓
/book-splitter 拆分为章节 Markdown
    ↓
chapters/ 目录（含 _index.md + 各章文件）
    ↓
/ocr-corrector 校正 OCR 错误（扫描版必需）
    ↓
过滤非内容章节（封面/版权/目录/参考文献/索引）
    ↓
并行 /deep-reader 逐章精读（最多 8 个并行）
    ↓
reports/ 目录（每章一份 10 维度报告）
    ↓
生成 _master-index.md 总索引
    ↓
/book-reader 生成交互式 HTML 阅读页面
    ↓
/book-qa 随时提问
    ↓
/evidence-collector 沉淀论据库（可选）
    ↓
同步到 Obsidian 知识库
```

### 视频内容创作工作流

```
输入文章/音频
    ↓
（可选）/audio2text 音频 → 文本
    ↓
/broadcast-maker 文章 → 深度精读 → 口播文案
    ↓
/content-to-script 精读报告 → 视频脚本（含时长选择）
    ↓
/article-to-visual-scenes 脚本 → 视觉分镜 JSON
    ↓
AI 生成静态画面（基于 JSON 描述）
    ↓
视频制作（画面 + 配音/字幕）
    ↓
发布
```

### 头条引流工作流

```
/hot-pain-match 找当日热点切入点
    ↓
写文章/口播文案（broadcast-maker 等）
    ↓
/toutiao-title-craft 起标题 + 标签
    ↓
/article-viral-hook 生成引流短帖
    ↓
/toutiao-comment-generator 评论区互动文案
    ↓
/article-to-richpost 排版发布
```

## 输出结构

```
{book-name}/
├── chapters/               # 拆分后的原始章节（OCR 校正后）
│   ├── _index.md           # 章节索引
│   ├── front-01-封面.md    # 封面等前置内容
│   ├── chapter-01-xxx.md   # 第一章正文
│   ├── chapter-02-xxx.md
│   └── back-03-参考文献.md # 后置内容
│
├── reports/                # 精读报告（仅内容章节）
│   ├── chapter-01-xxx-report.md
│   ├── chapter-02-xxx-report.md
│   └── ...
│
├── evidence/               # 论据卡片（可选，evidence-collector 输出）
│
└── _master-index.md        # 总索引（书籍信息 + 章节速览 + 跨章知识网络）
```

## 依赖安装

```bash
# 必需
pip install PyMuPDF

# OCR 支持（扫描版 PDF 需要）
pip install pytesseract pillow
brew install tesseract tesseract-lang        # macOS
sudo apt-get install tesseract-ocr tesseract-ocr-chi-sim  # Ubuntu

# EPUB 处理（可选）
pip install ebooklib beautifulsoup4 lxml

# 富文本繁转简（可选，generate_richpost.py 用，缺库时自动降级）
pip install opencc
```

## 扫描版 PDF 处理

| 模式 | 说明 |
|------|------|
| `image`（默认）| 扫描页渲染为 200 DPI 的 PNG 图片嵌入 Markdown |
| `ocr` | 使用 Tesseract 提取文字（可搜索） |
| `text` | 仅提取文本层，扫描页留空 |

## 同步到 Obsidian

所有报告和索引生成后，复制整个项目文件夹到 Obsidian 知识库：

```bash
TARGET="/Users/chouchou/Documents/Obsidian Vault/成长计划/读书计划"
cp -r "{book-name}" "$TARGET/"
```

## 扫描版 PDF 注意事项

扫描版 PDF 经 OCR 拆分后常见 5 类问题，`/ocr-corrector` 可自动修复：

| 问题类型 | 示例 | 修复后 |
|---------|------|--------|
| 乱码片段 | `GB wenwor`、`a7` | 删除 |
| 页码残留 | `40 一`、`— 123 —` | 删除 |
| 断裂句子 | 一行被截断为多行 | 合并为连续段落 |
| 多余空行 | 5 个连续空行 | 合并为 2 个 |
| OCR 错字 | `氨今`、`错情`、`哥德巴幸` | `迄今`、`错愕`、`哥德巴赫` |

> **重要**：校正直接修改 `chapters/` 源文件，不会备份。建议校正前用 Git 提交。

## 注意事项

- **EPUB 书籍**：`book-splitter` 只支持 PDF。EPUB 用 `python3 .kimi-code/skills/book-master/scripts/extract_epub.py book.epub ./book-name/chapters` 提取；若每章被拆成大量碎 xhtml，改用根目录的 `merge_epub_chapters.py`
- **并行上限**：子代理最多 8 个并行，超出分批处理
- **超长章节**：单章 >50KB 时，子代理处理时间会增加
- **书名含特殊字符**：确保 PDF 文件名合法（避免 `/` `\` `:` 等字符）
- **论据库路径**：`evidence-collector` / `evidence-query` / `xl-card` 的输出目录硬编码为 Obsidian 库内路径，换机器需相应调整
