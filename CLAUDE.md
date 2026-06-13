# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

learnAbook is a Claude Code skill collection covering three workflow domains:

1. **AI Deep Reading** — PDF → chapter splitting → OCR correction → parallel deep analysis → interactive reader → Q&A
2. **AI Video Content Creation** — Article → deep reading → broadcast script → visual scene breakdown → AI image/video generation pipeline
3. **Audio Processing** — Speech-to-text via Xunfei API

All workflows are implemented as slash-command skills under `.claude/skills/`.

## Skill Inventory

### Reading Workflow

| Skill | Purpose |
|-------|---------|
| `book-splitter` | Extract TOC from PDF, split into per-chapter Markdown with YAML frontmatter |
| `ocr-corrector` | Auto-detect and fix 5 classes of OCR errors (garbled text, broken sentences, page number residue, extra blank lines, OCR typos) |
| `deep-reader` | 10-dimension structured analysis of a single chapter/article |
| `book-master` | Orchestrates full pipeline: split → filter → parallel deep-read → master index |
| `book-reader` | Generates interactive HTML reader (left text, right concept cards) |
| `book-qa` | Q&A against extracted knowledge from `reports/` |

### Video Creation Workflow

| Skill | Purpose |
|-------|---------|
| `broadcast-maker` | Article → deep read → broadcast script (one-shot) |
| `content-to-script` | Deep-reader report → video script |
| `content-to-human-script` | Content → human-spoken script with tone annotations |
| `narrative-to-script` | Narrative content → video script |
| `article-to-richpost` | Article → formatted rich text post |
| `article-to-visual-scenes` | Script → visual scene breakdown JSON (for AI image gen) |
| `text-humanizer-zh` | Polish machine-generated Chinese text |
| `toutiao-title-craft` | Generate viral titles for Toutiao |

### Audio Processing

| Skill | Purpose |
|-------|---------|
| `audio2text` | Audio → text via Xunfei speech API (supports 202 dialects, 37 languages, speaker diarization) |

### External Skills (via skills-lock.json)

The `skills-lock.json` references skills from `lijigang/ljg-skills` (ref: `md`). These are auto-fetched and not stored in this repo.

## High-Level Architecture

### Reading Workflow Data Flow

```
Input PDF
    ↓
[book-splitter] — Python script (PyMuPDF/fitz) extracts TOC, splits by chapter
    ↓
chapters/*.md  (YAML frontmatter: title, page_range, level, source)
    ↓
[ocr-corrector] — Fixes scan-PDF OCR errors in-place (optional but recommended)
    ↓
[filter.sh] — Excludes front/back matter by filename keywords
    ↓
Filtered content chapters
    ↓
[Parallel sub-agents, max 8] — each runs /deep-reader on one chapter
    ↓
reports/*.md  (10-dimension structured reports)
    ↓
_master-index.md  (cross-chapter synthesis)
    ↓
[book-reader] — Generates interactive HTML in reader/ directory
    ↓
Sync to Obsidian vault
```

### Video Creation Workflow Data Flow

```
Input article/audio
    ↓
[audio2text] — Optional: audio → text
    ↓
[broadcast-maker] or [content-to-script] — Article → deep read → script
    ↓
[article-to-visual-scenes] — Script → visual scene JSON
    ↓
AI image generation (Lovart/SD) → static frames
    ↓
AI video generation (Seedance) → video clips
    ↓
Post-production
```

## Key Scripts

- **`book-splitter/scripts/split_book.py`** — Core Python script using PyMuPDF. Handles TOC extraction, chapter range building, scan-PDF detection (renders scan pages as PNG images at 200 DPI or optional Tesseract OCR), and Markdown assembly with YAML frontmatter.
- **`book-master/scripts/filter.sh`** — Bash script filtering out non-content chapters by filename keywords (封面, 书名, 版权, 目录, 参考文献, 索引, 献辞, _index.md).
- **`scripts/batch_lovart_vangogh.py`** — Batch image generation utility using LovartClient. Consumes `van_gogh_visual_prompts.json`, outputs to per-scene directories with progress tracking via `_progress.json`.
- **Validation scripts** — Each skill has `scripts/validate.sh` checking skill structure integrity and Python dependencies.

## Configuration

### audio2text API Keys

Create `.env` in project root (already in `.gitignore`):

```bash
XF_APPID=your-appid
XF_API_KEY=your-apikey
XF_API_SECRET=your-apisecret
```

### Lovart Image Generation

`batch_lovart_vangogh.py` uses the global `lovart-image` skill at `~/.claude/skills/lovart-image/scripts/`. Mode controlled via env vars:
- `LOVART_MODE=fast|thinking|unlimited` (default: fast)
- `LOVART_AUTO_CONFIRM=1|0` (default: 1)

## Output Structure

### Book Project

```
{book-name}/
├── chapters/          # Raw output from book-splitter (all PDF-derived files)
│   ├── _index.md
│   ├── front-*.md     # Cover, copyright, preface, etc.
│   ├── chapter-*.md   # Content chapters
│   └── back-*.md      # References, index, postscript, etc.
├── reports/           # Deep-reader output (only for content chapters)
│   └── chapter-*-report.md
├── reader/            # Interactive HTML (from book-reader)
│   ├── index.html
│   └── chapter-*.html
└── _master-index.md   # Synthesized cross-chapter index
```

### Video Project

```
{project-name}/
├── script.md              # Generated broadcast script
├── visual_prompts.json    # Scene breakdown (from article-to-visual-scenes)
├── images/                # Generated static frames
└── videos/                # Generated video clips
```

## Important Constraints

### PDF-Only Input

`book-splitter` only supports PDF. For EPUB files, write a custom extraction script using `ebooklib` + `BeautifulSoup` + `lxml`. After extraction, place files in `{book-name}/chapters/` and proceed directly to filtering + deep-reading steps. Do not invoke `/book-splitter` for EPUBs.

### Parallel Agent Limits

The `book-master` workflow launches sub-agents per chapter. **Cap at 8 parallel agents** to avoid resource exhaustion. Process in batches if more chapters exist.

### Scan PDF Handling

`split_book.py` auto-detects scan PDFs (pages with <10 characters of text). Default mode renders scan pages as embedded PNG images at 200 DPI. OCR mode requires:

```bash
pip install pytesseract pillow
brew install tesseract tesseract-lang   # macOS
```

### ocr-corrector In-Place Modification

`ocr-corrector` modifies `chapters/` source files directly without backup. The 5 fix classes are: garbled text deletion, page number removal, broken sentence merging, extra blank line collapse, and OCR typo correction. Advise git commit before running.

### Deep-Reader Sub-Agent Pattern

Sub-agents must return markdown text in their response; the main session writes files. This is due to permission constraints in some environments. The 10-dimension template is defined in `deep-reader/template.md`.

## Post-Processing: Obsidian Sync

After all reports and `_master-index.md` are generated, copy the entire book project folder:

```bash
TARGET="/Users/chouchou/Documents/Obsidian Vault/成长计划/读书计划"
cp -r "{book-name}" "$TARGET/"
```

For video scripts, sync target is:

```bash
TARGET="/Users/chouchou/Documents/Obsidian Vault/成长计划/博客"
```

## File Organization Rules

- Skill files live under `.claude/skills/{skill-name}/` with mandatory `SKILL.md` (YAML frontmatter), optional `template.md`, `examples/`, and `scripts/`.
- Book outputs are sibling directories in the workspace root, named after the PDF file (extension stripped).
- The `books/` directory is for source PDFs awaiting processing.
- The `Kimi_Agent_书籍拆分技能/` directory is a legacy prototype — do not use for new work.

## Skill Validation

```bash
bash .claude/skills/book-splitter/scripts/validate.sh
bash .claude/skills/book-master/scripts/validate.sh
bash .claude/skills/deep-reader/scripts/validate.sh
```
