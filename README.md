# learnAbook — Claude Code 技能集合

基于 Claude Code 的自动化技能集合，覆盖 **AI 深度读书** 和 **AI 视频内容创作** 两大工作流。

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

### 二、AI 视频内容创作工作流

| 技能 | 作用 | 何时使用 |
|------|------|----------|
| `/broadcast-maker` | 文章 → 深度精读 → 口播文案（一站式） | 输入文章，直接输出视频文案 |
| `/content-to-script` | 精读报告 → 口播文案 | 已有精读报告，转为视频脚本 |
| `/content-to-human-script` | 内容 → 人工口播文案 | 需要更口语化、带语气标注的脚本 |
| `/narrative-to-script` | 叙事内容 → 视频脚本 | 故事类内容转视频 |
| `/article-to-richpost` | 文章 → 富文本帖子 | 生成带格式的朋友圈/公众号帖子 |
| `/article-to-visual-scenes` | 文章/文案 → 视觉场景分镜 JSON | 需要为视频制作静态分镜画面 |
| `/text-humanizer-zh` | 中文文本润色 | 让机器生成的文字更自然 |

### 三、音频处理

| 技能 | 作用 | 何时使用 |
|------|------|----------|
| `/audio2text` | 音频文件 → 文本（讯飞语音转写） | 转录播客、会议录音、视频音频 |

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

### 视频内容创作工作流

#### 场景七：文章转视频文案

```
/broadcast-maker ./article.md
```

自动完成：深度精读（10 维度分析）→ 询问视频时长 → 生成口播文案 → 保存到 Obsidian 博客目录。

#### 场景八：已有精读报告转视频文案

```
/content-to-script ./report.md --duration 8min
```

#### 场景九：文案转视觉分镜

```
/article-to-visual-scenes ./script.md
```

输出 JSON 分镜文件，每个场景包含：标题、静态画面描述（背景/主体/构图/色彩/文字），可直接用于 AI 生图。

#### 场景十：中文文本润色

```
/text-humanizer-zh ./draft.md
```

让机器生成的文字更自然、更像人写的。

### 音频处理

#### 场景十一：音频转文字

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

- **EPUB 书籍**：`book-splitter` 只支持 PDF。EPUB 需先用 `ebooklib` + `BeautifulSoup` 提取为 Markdown，按 `chapters/` 格式存放后直接进入过滤+精读步骤
- **并行上限**：子代理最多 8 个并行，超出分批处理
- **超长章节**：单章 >50KB 时，子代理处理时间会增加
- **书名含特殊字符**：确保 PDF 文件名合法（避免 `/` `\` `:` 等字符）
