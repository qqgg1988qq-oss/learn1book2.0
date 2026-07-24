# AGENTS.md — learnAbook 项目指南

本文件面向后续维护或扩展本项目的 AI coding agent。阅读前默认你对本项目一无所知；以下内容全部基于仓库实际文件与目录结构整理，不做推测。

---

## 项目概述

**learnAbook**（工作目录名为 `learn1book2.0`）是一个 Claude Code / Kimi Code 技能集合（skill collection），不是传统意义上的 Web 应用、服务或需要编译的软件项目。它通过 slash-command skill 机制，把三类 AI 辅助工作流自动化：

1. **AI 深度读书工作流**：PDF/EPUB → 按目录拆分为章节 Markdown → OCR 校正 → 自动过滤非内容章节 → 并行深度精读 → 生成总索引 → 基于知识点的问答。
2. **AI 视频/图文内容创作工作流**：文章/音频 → 深度精读 → 口播文案 → 视觉场景分镜 JSON → 批量图片生成 → 后续视频制作；以及头条引流帖、爆款标题、评论、概念卡片等配套生成器。
3. **音频转写**：调用讯飞语音转写大模型 API 将音频转为带时间戳的文本。

项目根目录同时充当**工作空间（workspace）**：书籍拆分后的章节、精读报告、论据文件都会以书名为目录名直接生成在根目录下（这些目录已被 `.gitignore` 忽略）。

---

## 关键配置文件

本仓库**没有** `pyproject.toml`、`package.json`、`Cargo.toml`、`requirements.txt`、`Makefile` 等传统构建或依赖清单文件。实际起作用的是：

| 文件 | 作用 |
|------|------|
| `.kimi-code/settings.json` | Kimi Code 权限配置（允许 Write/Edit/Bash/Read/Agent） |
| `.claude/settings.json` | Claude Code 权限配置（内容同上） |
| `skills-lock.json` | 锁定 20 个外部 skill（全部来自 GitHub `lijigang/ljg-skills`，ref 为 `md`，含 `computedHash`），由 Claude Code 自动拉取，不存储在本仓库 |
| `.gitignore` | 忽略 PDF/ZIP 源文件、生成的书籍目录、`.env`、`.claude/skills`、`__pycache__` 等 |
| `.env`（未入库） | 讯飞 API 密钥，见"安全与敏感信息" |
| `.venv/` | 项目根目录下的本地 Python 虚拟环境 |

每个 skill 的 `SKILL.md` 顶部的 YAML frontmatter（`name` / `description` / `allowed-tools`）同时充当该技能的"配置"。

---

## 仓库结构与代码组织

```
learn1book2.0/
├── .kimi-code/
│   ├── settings.json              # Kimi Code 权限配置
│   └── skills/                    # 全部 33 个 slash-command skill 定义（见下表）
├── .claude/
│   ├── settings.json              # Claude Code 权限配置
│   └── skills/                    # .kimi-code/skills 的本地镜像副本（已被 .gitignore 忽略，勿手动改）
├── scripts/
│   └── batch_lovart_vangogh.py    # 基于 LovartClient 批量生成静态场景图
├── extract_reports.py             # 一次性工具：从批量精读报告提取指定章节合并为摘要（路径硬编码）
├── generate_richpost.py           # 一次性工具：Markdown 口播文案 → 公众号/头条号富文本 HTML
├── merge_epub_chapters.py         # 一次性工具：合并被拆碎的 EPUB xhtml 为完整章节
├── skills-lock.json               # 外部 ljg-skills 锁定文件
├── README.md                      # 面向用户的中文使用说明
├── CLAUDE.md                      # 面向 Claude Code 的英文项目指南
├── AGENTS.md                      # 本文件
├── .venv/                         # 本地 Python 虚拟环境
├── 未处理书籍/                     # 等待处理的 EPUB 源文件
│
└── {book-name}/                   # 已处理书籍输出目录（工作区产物，被 .gitignore 忽略）
    ├── chapters/                  # 拆分后的原始章节
    ├── reports/                   # deep-reader 输出的 10 维度精读报告
    ├── evidence/                  # evidence-collector 输出的论据卡片（可选，如《思考，快与慢》）
    └── _master-index.md           # 全书总索引
```

### 技能清单（.kimi-code/skills/，共 33 个）

**读书工作流**

| 技能 | 作用 |
|------|------|
| `book-splitter` | 将 PDF 按目录拆分为章节 Markdown（核心脚本 `scripts/split_book.py`） |
| `ocr-corrector` | 自动检测并修复扫描版 OCR 的 5 类错误，直接原地修改源文件 |
| `deep-reader` | 单篇文章/章节的 10 维度结构化精读 |
| `book-master` | 完整读书工作流编排：拆分 → 过滤 → 并行精读 → 总索引 |
| `book-reader` | 生成左右分栏交互式 HTML 阅读页（核心脚本 `scripts/generate.py`，纯静态无构建） |
| `book-qa` | 基于 `reports/` 的问答（要求完整绝对路径） |
| `book-reading-share` | 读书分享口播文案一站式：book-master → evidence-collector → broadcast-maker |
| `batch-knowledge-extractor` | 批量精读多个文件（PDF/MD/TXT/SRT）并整合总报告（脚本 `extract_pdf_text.py`、`srt_to_md.py`） |
| `evidence-collector` | 从材料提取概念/数据/案例/金句存入论据库（脚本 `evidence_dedup.py`、`evidence_migrate.py`） |
| `evidence-query` | 按主题/场景/质量分从论据库检索写作素材（脚本 `evidence_query.py`） |

**视频/图文创作工作流**

| 技能 | 作用 |
|------|------|
| `broadcast-maker` | 文章 → 深度精读 → 口播文案（一站式） |
| `content-to-script` | 精读报告 → 口播文案 |
| `batch-content-to-script` | 批量把多份精读报告转成口播文案 |
| `content-to-human-script` | 内容 → 更口语化、带语气标注的脚本 |
| `narrative-to-script` | 叙事内容 → 视频解说稿 |
| `story-narration-script` | 剧情类内容 → 口播讲解稿（情节拆解→知识补全→大纲重构→成稿） |
| `article-to-richpost` | 文章 → 公众号/头条号富文本 HTML |
| `article-to-visual-richpost` | 文章 → 视觉场景 JSON + 排版好的富文本 HTML（脚本 `scripts/build.py`） |
| `article-to-visual-scenes` | 文案 → 静态视觉分镜 JSON |
| `text-to-image-prompt` | 短文 → 写实场景 AI 生图提示词（图中不带文字） |
| `text-humanizer-zh` | 中文文本去 AI 腔 |

**头条/引流/写作配套**

| 技能 | 作用 |
|------|------|
| `article-viral-hook` | 文章 → 痛点匹配 + AA/AG 两段式引流短帖 + 爆款标题候选 |
| `article-to-han-post` | 文章 → 韩寒风格引流帖（viral-hook → 韩寒口吻改写 → 去 AI 味 三阶段流水线） |
| `toutiao-title-craft` | 今日头条爆款标题 + 标签（含 `references/` 参考资料库和 `scripts/save_titles.py`） |
| `toutiao-comment-generator` | 按话题 + 目标情绪生成头条高互动评论 |
| `hot-pain-match` | 抓取今日头条 + 微信热搜，与 40 岁中年危机痛点图谱匹配 |
| `apag-writing-outline` | 按 Attention→Perspective→Advantage→Amplify/Gamify 框架生成说服性写作大纲 |
| `article-claims-extractor` | 提取文章的核心观点、分论点和隐含主张 |
| `article-claims-to-card` | 观点提取 + 调用 xl-card 铸卡一站式 |
| `xl-card` | 文案 → 结构化 JSON 概念卡片（供 Lovart/ljg-card 等生图工具渲染） |

**其他**

| 技能 | 作用 |
|------|------|
| `audio2text` | 音频 → 文本（讯飞 API；转写代码以内嵌 Python 形式写在 SKILL.md 中，无独立脚本） |
| `council` | Council of High Intelligence：多历史思想家角色对复杂问题做结构化审议 |
| `markitdown` | ⚠️ 空目录占位，技能已移除，勿引用其中的脚本 |

### Skill 目录约定

每个 skill 目录内部结构基本一致：

```
.kimi-code/skills/{skill-name}/
├── SKILL.md                       # 核心说明，必须包含 YAML frontmatter（name / description / allowed-tools 等）
├── template.md                    # 任务输出模板（deep-reader、content-to-script 等需要）
├── examples/
│   └── sample.md                  # 使用示例
├── scripts/                       # 该 skill 的辅助脚本（可选）
│   ├── *.py / *.sh
│   └── validate.sh                # 检查 skill 结构完整性和依赖
└── references/                    # 参考资料（可选，如 toutiao-title-craft）
```

### 工作空间输出约定

每本书处理完成后，会在项目根目录生成以源文件名（去扩展名）命名的目录：

```
{book-name}/
├── chapters/          # book-splitter / extract_epub.py 等原始输出
│   ├── _index.md      # 章节索引
│   ├── front-*.md     # 封面、版权、目录等前置内容
│   ├── chapter-*.md   # 正文内容章节
│   └── back-*.md      # 参考文献、索引、后记等后置内容
├── reports/           # deep-reader 输出的 10 维度精读报告
│   └── chapter-*-report.md
├── evidence/          # evidence-collector 的论据卡片（可选）
└── _master-index.md   # 全书总索引
```

非书籍类批量任务（如 `数字经济学02/`）由 `batch-knowledge-extractor` 产生 `extracted/`（文本提取结果）+ `reports/`（精读报告）结构。

---

## 技术栈

- **运行环境**：Python 3 + Bash（在 Claude Code / Kimi Code 内部执行）；根目录有本地虚拟环境 `.venv/`。
- **PDF 处理**：PyMuPDF（`fitz`）。
- **OCR（可选）**：`pytesseract` + `Pillow` + 系统级 Tesseract 及语言包。
- **EPUB 处理（可选）**：`ebooklib` + `BeautifulSoup` + `lxml`。
- **富文本转换（可选）**：`opencc`（`generate_richpost.py` 用于繁转简，缺库时降级为不转换）。
- **交互式阅读页**：纯静态 HTML/CSS/JS（无前端框架、无构建步骤），由 `book-reader/scripts/generate.py` 直接生成。
- **配置格式**：YAML frontmatter 用于章节文件和 SKILL.md；JSON 用于 skills-lock、权限设置、视觉分镜；`.env` 用于 API 密钥。
- **版本控制**：Git；大型 PDF/ZIP 与生成的书籍目录已加入 `.gitignore`。

依赖通过各 skill 的 `validate.sh` 和 README/CLAUDE.md 中的说明手动安装，没有统一依赖清单。

---

## 关键脚本与运行方式

### 1. 读书工作流

```bash
# 完整流程（最常用）
/book-master /path/to/book.pdf

# 仅拆分 PDF
python3 .kimi-code/skills/book-splitter/scripts/split_book.py split /path/to/book.pdf -o ./book-name/chapters --level 1 --scan image

# 过滤非内容章节
bash .kimi-code/skills/book-master/scripts/filter.sh ./book-name/chapters
```

`split_book.py` 支持的参数：
- `--level 1|2`：按一级或二级目录拆分。
- `--scan text|image|ocr`：扫描版 PDF 处理方式（默认 `image`，即渲染为 200 DPI PNG 嵌入 Markdown；`ocr` 需要 Tesseract）。

### 2. EPUB 预处理

`book-splitter` 本身只原生支持 PDF。EPUB 可用：

```bash
# 专用 EPUB 提取脚本
python3 .kimi-code/skills/book-master/scripts/extract_epub.py /path/to/book.epub ./book-name/chapters

# 若 EPUB 的每章被拆成大量碎 xhtml 文件，用根目录的一次性脚本合并
python3 merge_epub_chapters.py /path/to/book.epub ./book-name/chapters
```

注意：旧文档提到的 `markitdown_book.py` 与 `doc-to-chapters` 技能已从仓库移除，不要再引用。

### 3. 视频创作工作流

```bash
# 一站式
/broadcast-maker ./article.md

# 已有精读报告转文案
/content-to-script ./report.md --duration 8min

# 文案转视觉分镜
/article-to-visual-scenes ./script.md

# 批量 Lovart 生图
python3 scripts/batch_lovart_vangogh.py
```

`batch_lovart_vangogh.py` 依赖全局 skill `lovart-image`（路径硬编码为 `/Users/chouchou/.claude/skills/lovart-image/scripts`），消费 `van_gogh_visual_prompts.json` 并按场景分目录输出，用 `_progress.json` 记录进度；通过环境变量控制行为：
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
6. **同步镜像**：`.claude/skills/` 是 `.kimi-code/skills/` 的本地镜像（被 git 忽略），修改 skill 时以 `.kimi-code/skills/` 为准。

### 过滤规则

`book-master/scripts/filter.sh` 按文件名关键字排除非内容章节：

```
_index.md / 封面 / 书名 / 版权 / 目录 / 参考文献 / 索引 / 献辞
```

保留：正文、前言、导言、后记、注释等。

### 并行限制

`book-master` 与 `ocr-corrector` 在调用子代理时，最多并行启动 **8 个子代理**；超出需分批处理，避免资源耗尽。

### 子代理写文件模式

`deep-reader` 等子代理只在响应中返回 Markdown 文本，由主会话负责写文件（部分环境下子代理没有写权限）。10 维度模板定义在 `deep-reader/template.md`。

### OCR 校正注意

`ocr-corrector` 会直接原地修改 `chapters/` 下的源文件，不会备份。运行前建议先用 Git 提交。

---

## 测试与验证

没有单元测试框架。多数核心 skill 提供结构验证脚本：

```bash
bash .kimi-code/skills/book-splitter/scripts/validate.sh
bash .kimi-code/skills/book-master/scripts/validate.sh
bash .kimi-code/skills/deep-reader/scripts/validate.sh
bash .kimi-code/skills/book-reader/scripts/validate.sh
bash .kimi-code/skills/evidence-collector/scripts/validate.sh
```

`validate.sh` 通常检查：
- 必需文件是否存在（`SKILL.md`、`template.md`、核心脚本等）
- `SKILL.md` 是否包含正确的 YAML frontmatter
- Python 依赖是否已安装（如 `fitz`、`pytesseract`）

目前 33 个 skill 中 28 个带 `validate.sh`；以下 skill 没有：`article-to-visual-richpost`、`batch-knowledge-extractor`、`story-narration-script`、`toutiao-title-craft`、`markitdown`（空目录）。

---

## 安全与敏感信息

- **API 密钥**：`.env` 文件已加入 `.gitignore`，用于存放讯飞语音转写密钥。不要将其提交到 Git。
- **外部 skill 依赖**：`skills-lock.json` 锁定了 20 个 `lijigang/ljg-skills` 的远程 skill（`ljg-card`、`ljg-read`、`ljg-think` 等），由 Claude Code 自动拉取，不存储在本仓库。
- **第三方 AI 图片生成**：`batch_lovart_vangogh.py` 会调用远程 Lovart 服务并自动确认图片生成任务；脚本内置黑名单，拒绝视频/音频/媒体类工具调用。
- **硬编码个人路径**：多处脚本和 skill 含 macOS 用户路径，移植时需调整：
  - `batch_lovart_vangogh.py` → `/Users/chouchou/.claude/skills/lovart-image/scripts`
  - `extract_reports.py` → Obsidian 库内 `数字经济学04` 报告目录
  - `evidence-collector` / `evidence-query` → 论据库 `/Users/chouchou/Documents/Obsidian Vault/九局下半怎么破局/参考资料/论据库/`
  - `xl-card` → 输出目录 `/Users/chouchou/Documents/Obsidian Vault/九局下半怎么破局/概念卡片`
- **大文件管理**：PDF/ZIP 源文件与生成的书籍目录均被 `.gitignore` 忽略。

---

## 部署说明

本项目**不是可部署服务**。所有产物是静态 Markdown/HTML/JSON 文件，最终通过手动复制同步到 Obsidian 知识库：

```bash
# 读书项目
TARGET="/Users/chouchou/Documents/Obsidian Vault/成长计划/读书计划"
cp -r "{book-name}" "$TARGET/"

# 视频文案/博客项目
TARGET="/Users/chouchou/Documents/Obsidian Vault/成长计划/博客"
```

---

## 常见注意事项

- **PDF-only 原生支持**：`book-splitter` 只原生支持 PDF；EPUB 用 `book-master/scripts/extract_epub.py` 或根目录 `merge_epub_chapters.py`（碎 xhtml 场景）。
- **扫描版 PDF**：默认渲染为图片；如需可搜索文本，安装 Tesseract 后用 `--scan ocr`。
- **超长章节**：单章超过 50KB 时，子代理处理时间会显著增加。
- **书名特殊字符**：避免在源文件名中使用 `/ \ :` 等非法字符。
- **`/book-qa` 路径**：必须提供书籍目录的完整绝对路径，不能只写书名。
- **根目录一次性脚本**：`extract_reports.py`、`generate_richpost.py`、`merge_epub_chapters.py` 是为特定任务写的临时工具，含硬编码路径，复用前先检查并修改。
- **`book-master/scripts/merge_naval_chapters.py`**：针对特定书籍的一次性合并脚本，非通用流程的一部分。
