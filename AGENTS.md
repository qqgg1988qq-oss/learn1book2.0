# AGENTS.md — learnAbook 项目指南

本文件面向后续维护或扩展本项目的 AI coding agent。阅读前默认你对本项目一无所知；以下内容全部基于仓库实际文件与目录结构整理，不做推测。

---

## 项目概述

**learnAbook** 是一个 Claude Code 技能集合（skill collection），不是传统意义上的 Web 应用或服务。它通过 Claude Code 的 slash-command skill 机制，把两条 AI 辅助工作流自动化：

1. **AI 深度读书工作流**：PDF → 按目录拆分为章节 Markdown → OCR 校正 → 自动过滤非内容章节 → 并行深度精读 → 生成总索引 → 可选交互式 HTML 阅读页面 → 基于知识点的问答。
2. **AI 视频内容创作工作流**：文章/音频 → 深度精读 → 口播文案 → 视觉场景分镜 JSON → 批量图片生成 → 后续视频制作。

此外还有一个独立的 **音频转写技能**，调用讯飞语音转写大模型 API 将音频转为带时间戳的文本。

项目根目录同时充当**工作空间（workspace）**：书籍拆分后的章节、精读报告、HTML 阅读页都会以书名为目录名直接生成在根目录下。

---

## 仓库结构与代码组织

```
learnAbook-master/
├── .claude/
│   ├── settings.json              # Claude Code 权限配置（允许 Write/Edit/Bash）
│   └── skills/                    # 所有 slash-command skill 定义
│       ├── article-to-richpost/   # 文章 → 公众号/头条号富文本 HTML
│       ├── article-to-visual-scenes/  # 文案 → 静态视觉分镜 JSON
│       ├── article-viral-hook/    # 文章 → 引流短帖
│       ├── audio2text/            # 音频 → 文本（讯飞 API）
│       ├── batch-content-to-script/   # 批量把 reports 转成口播文案
│       ├── book-master/           # 完整读书工作流编排
│       ├── book-qa/               # 基于 reports/ 的问答
│       ├── book-reader/           # 生成交互式 HTML 阅读页
│       ├── book-splitter/         # PDF 按目录拆分为 Markdown
│       ├── broadcast-maker/       # 文章 → 深度精读 → 口播文案（一站式）
│       ├── content-to-human-script/   # 精读报告 → 更口语化的脚本
│       ├── content-to-script/     # 精读报告 → 口播文案
│       ├── deep-reader/           # 单篇文章/章节的 10 维度精读
│       ├── markitdown/            # 通用文件转 Markdown
│       ├── narrative-to-script/   # 叙事内容 → 视频解说稿
│       ├── ocr-corrector/         # 修复扫描版 OCR 错误
│       ├── text-humanizer-zh/     # 中文文本去 AI 腔
│       ├── text-to-image-prompt/  # 短文 → 写实场景生图提示词
│       └── toutiao-title-craft/   # 今日头条爆款标题 + 标签
├── scripts/
│   └── batch_lovart_vangogh.py    # 基于 LovartClient 批量生成静态场景图
├── skills-lock.json               # 引用外部 ljg-skills（lijigang/ljg-skills）的锁定文件
├── README.md                      # 面向用户的中文使用说明
├── CLAUDE.md                      # 面向 Claude Code 的英文项目指南
├── .gitignore                     # 忽略 PDF 源文件、生成的书籍目录、.env 等
│
├── 仿生人会梦见电子羊吗/          # 已处理书籍输出示例
├── 我们何以成为后人类/            # 已处理书籍输出示例
├── 有意识的心灵：一种基础理论研究/ # 已处理书籍输出示例（含 reader/）
└── 未处理书籍/                    # 等待处理的 EPUB 源文件
```

### Skill 目录约定

每个 skill 目录内部结构基本一致：

```
.claude/skills/{skill-name}/
├── SKILL.md                       # 核心说明，必须包含 YAML frontmatter（name / description / allowed-tools 等）
├── template.md                    # 任务输出模板（deep-reader、content-to-script 等需要）
├── examples/
│   └── sample.md                  # 使用示例
├── scripts/                       # 该 skill 的辅助脚本
│   ├── *.py / *.sh
│   └── validate.sh                # 检查 skill 结构完整性和依赖
└── references/                    # 参考资料（可选，如 style-presets、formula_library）
```

### 工作空间输出约定

每本书处理完成后，会在项目根目录生成以 PDF 文件名（去扩展名）命名的目录：

```
{book-name}/
├── chapters/          # book-splitter 原始输出
│   ├── _index.md      # 章节索引
│   ├── front-*.md     # 封面、版权、目录等前置内容
│   ├── chapter-*.md   # 正文内容章节
│   └── back-*.md      # 参考文献、索引、后记等后置内容
├── reports/           # deep-reader 输出的 10 维度精读报告
│   └── chapter-*-report.md
├── reader/            # book-reader 输出的交互式 HTML（可选）
│   ├── index.html
│   └── chapter-*.html
└── _master-index.md   # 全书总索引
```

---

## 技术栈

- **运行环境**：Python 3 + Bash（Claude Code 内部执行）。
- **PDF 处理**：PyMuPDF（`fitz`）。
- **OCR（可选）**：`pytesseract` + `Pillow` + 系统级 Tesseract 及语言包。
- **EPUB 处理（可选）**：`ebooklib` + `BeautifulSoup` + `lxml`。
- **交互式阅读页**：纯静态 HTML/CSS/JS（无前端框架、无构建步骤），由 `book-reader/scripts/generate.py` 直接生成。
- **配置**：YAML frontmatter 用于章节文件和 SKILL.md；JSON 用于 skills-lock、进度状态、视觉分镜输出；`.env` 用于 API 密钥。
- **版本控制**：Git；大型 PDF 与生成书籍目录已加入 `.gitignore`。

**注意**：本仓库没有 `pyproject.toml`、`package.json`、`Cargo.toml`、`requirements.txt`、`Makefile` 等传统构建或依赖清单文件。依赖通过各 skill 的 `validate.sh` 和 README/CLAUDE.md 中的说明手动安装。

---

## 关键脚本与运行方式

### 1. 读书工作流

```bash
# 完整流程（最常用）
/book-master /path/to/book.pdf

# 仅拆分 PDF
python3 .claude/skills/book-splitter/scripts/split_book.py split /path/to/book.pdf -o ./book-name/chapters --level 1 --scan image

# 过滤非内容章节
bash .claude/skills/book-master/scripts/filter.sh ./book-name/chapters

# 生成交互式阅读页
python3 .claude/skills/book-reader/scripts/generate.py ./book-name
```

`split_book.py` 支持的参数：
- `--level 1|2`：按一级或二级目录拆分。
- `--scan text|image|ocr`：扫描版 PDF 处理方式（默认 `image`，即渲染为 200 DPI PNG 嵌入 Markdown；`ocr` 需要 Tesseract）。

### 2. EPUB 预处理

`book-splitter` 本身只支持 PDF。EPUB 需先用辅助脚本转换：

```bash
python3 .claude/skills/book-master/scripts/extract_epub.py /path/to/book.epub ./book-name/chapters
```

### 3. 视频创作工作流

```bash
# 一站式
/broadcast-maker ./article.md

# 已有精读报告转文案
python3 # 该 skill 主要是 prompt 驱动，无独立脚本

# 批量 Lovart 生图
python3 scripts/batch_lovart_vangogh.py
```

`batch_lovart_vangogh.py` 依赖全局 skill `lovart-image`（路径硬编码为 `/Users/chouchou/.claude/skills/lovart-image/scripts`），并通过环境变量控制行为：
- `LOVART_MODE=fast|thinking|unlimited`（默认 `fast`）
- `LOVART_AUTO_CONFIRM=1|0`（默认 `1`）

### 4. 音频转写

```bash
/audio2text ./recording.mp3 --language autodialect
```

需要项目根目录 `.env`：

```bash
XF_APPID=your-appid
XF_API_KEY=your-apikey
XF_API_SECRET=your-apisecret
```

---

## 开发与扩展约定

### 新增或修改 skill 时

1. **必须文件**：`SKILL.md`（含 YAML frontmatter，至少包含 `name`、`description`、`allowed-tools`）。
2. **可选但建议**：`template.md` 用于固定输出格式；`examples/sample.md` 提供示例；`scripts/validate.sh` 做结构检查。
3. **Frontmatter 规范**：skill 的 `SKILL.md` 以 `---` 开头和结尾；章节 Markdown 文件也使用 YAML frontmatter（`title`、`page_range`、`level`、`source`）。
4. **脚本风格**：Python 脚本使用 UTF-8 编码、中文注释、命令行参数用 `argparse`；Bash 脚本使用 `set -e`。
5. **输出目录命名**：自动以源文件名（去扩展名）作为书籍项目目录名，直接放在项目根目录下。

### 过滤规则

`book-master/scripts/filter.sh` 按文件名关键字排除非内容章节：

```
_index.md / 封面 / 书名 / 版权 / 目录 / 参考文献 / 索引 / 献辞
```

保留：正文、前言、导言、后记、注释等。

### 并行限制

`book-master` 在调用 `/deep-reader` 时，最多并行启动 **8 个子代理**；超出需分批处理，避免资源耗尽。

### OCR 校正注意

`ocr-corrector` 会直接原地修改 `chapters/` 下的源文件，不会备份。运行前建议先用 Git 提交。

---

## 测试与验证

没有单元测试框架。每个核心 skill 提供结构验证脚本：

```bash
bash .claude/skills/book-splitter/scripts/validate.sh
bash .claude/skills/book-master/scripts/validate.sh
bash .claude/skills/deep-reader/scripts/validate.sh
```

`validate.sh` 通常检查：
- 必需文件是否存在（`SKILL.md`、`template.md`、核心脚本等）
- `SKILL.md` 是否包含正确的 YAML frontmatter
- Python 依赖是否已安装（如 `fitz`、`pytesseract`）

---

## 安全与敏感信息

- **API 密钥**：`.env` 文件已加入 `.gitignore`，用于存放讯飞语音转写密钥。不要将其提交到 Git。
- **外部 skill 依赖**：`skills-lock.json` 引用了 `lijigang/ljg-skills` 的远程 skill，由 Claude Code 自动拉取，不存储在本仓库。
- **第三方 AI 图片生成**：`batch_lovart_vangogh.py` 会调用远程 Lovart 服务并自动确认图片生成任务；脚本内置黑名单，拒绝视频/音频/媒体类工具调用。
- **大文件管理**：PDF 源文件放在 `books/`（未在根目录显示但 README 中提及），该目录整体被 `.gitignore` 忽略；生成的书籍目录同样被忽略。

---

## 部署说明

本项目**不是可部署服务**。所有产物是静态 Markdown/HTML 文件，最终通过手动复制同步到 Obsidian 知识库：

```bash
# 读书项目
TARGET="/Users/chouchou/Documents/Obsidian Vault/成长计划/读书计划"
cp -r "{book-name}" "$TARGET/"

# 视频文案/博客项目
TARGET="/Users/chouchou/Documents/Obsidian Vault/成长计划/博客"
```

交互式阅读页面 `reader/index.html` 直接用浏览器打开即可，无需服务器。

---

## 常见注意事项

- **PDF-only**：`book-splitter` 只支持 PDF；EPUB 先用 `extract_epub.py` 预处理。
- **扫描版 PDF**：默认渲染为图片；如需可搜索文本，安装 Tesseract 后用 `--scan ocr`。
- **超长章节**：单章超过 50KB 时，子代理处理时间会显著增加。
- **书名特殊字符**：避免在 PDF 文件名中使用 `/ \ :` 等非法字符。
- **外部路径硬编码**：`batch_lovart_vangogh.py` 和 README/CLAUDE.md 中的 Obsidian 路径包含 macOS 用户路径 `/Users/chouchou/`，在 Windows 或其他机器上需相应调整。
