#!/usr/bin/env python3
"""
从各章节精读报告中提取关键信息，生成全书总索引 _master-index.md。
"""
import re
from pathlib import Path


def extract_frontmatter(text: str) -> dict:
    if text.startswith('---'):
        end = text.find('---', 3)
        if end != -1:
            fm_text = text[3:end].strip()
            data = {}
            for line in fm_text.splitlines():
                if ':' in line:
                    k, v = line.split(':', 1)
                    data[k.strip()] = v.strip().strip('"').strip("'")
            return data
    return {}


# 中文数字映射
CN_NUMBERS = '一二三四五六七八九十'


def cn_num_pattern() -> str:
    """生成匹配中文数字加顿号的正则，如一、二、三、..."""
    chars = ''.join(CN_NUMBERS)
    return f'[{chars}]+、'


def extract_section(text: str, heading: str) -> str:
    """提取某个二级标题下的内容，直到下一个同级或更高级标题。
    标题可能带编号：## 1. 元信息 或 ## 一、元信息。
    """
    cn = cn_num_pattern()
    pattern = rf'##\s+(?:(?:\d+\.\s+)|(?:{cn}))?{re.escape(heading)}\s*\n(.*?)(?=\n##\s+|\Z)'
    m = re.search(pattern, text, re.DOTALL)
    return m.group(1).strip() if m else ""


def extract_field(section_text: str, field_name: str) -> str:
    """从 section 文本中提取 **字段名**：值 或 - 字段名：值 形式的字段。"""
    # 匹配加粗字段名或列表字段名，后跟中文/英文冒号
    pattern = rf'(?:^|\n)\s*(?:[-*]\s+)?\*\*{re.escape(field_name)}\*\*\s*[:：]\s*(.*?)(?=\n|$)'
    m = re.search(pattern, section_text)
    if m:
        value = m.group(1).strip()
        # 截断
        if len(value) > 150:
            value = value[:150] + "……"
        return value
    return ""


def extract_concepts(section_text: str, limit: int = 8) -> list:
    """从关键概念与定义 section 提取概念名。"""
    concepts = []
    for line in section_text.splitlines():
        line = line.strip()
        if line.startswith('- ') or line.startswith('* '):
            item = line[2:].strip()
            # 匹配 **概念名**：解释
            m = re.match(r'\*\*(.+?)\*\*\s*[:：](.+)', item)
            if m:
                name = m.group(1).strip()
                desc = m.group(2).strip()
                if name and name not in ('术语名称', '文中定义', '解释', '通俗解释', '关联概念'):
                    concepts.append((name, desc[:120]))
                    if len(concepts) >= limit:
                        break
    return concepts


def main():
    base = Path("/Users/chouchou/Documents/Obsidian Vault/成长计划/读书计划/道德经全解")
    reports_dir = base / "reports"
    chapters_dir = base / "chapters"
    output = base / "_master-index.md"

    report_files = sorted(reports_dir.glob("chapter-*-report.md"),
                          key=lambda p: int(re.search(r'chapter-(\d+)-', p.name).group(1)))

    lines = [
        "# 道德经白话全译 — 精读报告总索引\n",
        "## 书籍信息\n",
        "- 来源: 道德经白话全译（文史哲，立信会计出版社，2012）\n",
        f"- 拆分章节数: {len(report_files)}\n",
        f"- 精读章节数: {len(report_files)}\n",
        "- 排除章节: 无\n\n",
        "## 章节精读报告\n\n",
        "| 序号 | 章节 | 核心主题 | 精读报告 |\n",
        "|------|------|----------|----------|\n",
    ]

    core_themes = []
    key_concepts_all = []

    for rf in report_files:
        num = int(re.search(r'chapter-(\d+)-', rf.name).group(1))
        text = rf.read_text(encoding='utf-8')
        fm = extract_frontmatter(text)
        title = fm.get('title', f'第{num}章')

        # 尝试提取核心主题
        meta_section = extract_section(text, '元信息')
        theme = extract_field(meta_section, '核心主题')
        if not theme:
            thesis_section = extract_section(text, '核心论点')
            # 尝试提取中心论点
            theme = extract_field(thesis_section, '中心论点')
        if not theme:
            theme = "—"
        core_themes.append((num, title, theme))

        # 提取关键概念
        concepts_section = extract_section(text, '关键概念与定义')
        concept_items = extract_concepts(concepts_section, 5)
        for name, desc in concept_items:
            key_concepts_all.append((num, title, name, desc))

        lines.append(f"| {num} | {title} | {theme} | [报告](reports/{rf.name}) |\n")

    lines.append("\n## 全书核心论点速览\n\n")
    for num, title, theme in core_themes:
        lines.append(f"- **{title}**：{theme}\n")

    lines.append("\n## 跨章节核心概念网络\n\n")
    # 统计概念出现频次
    concept_counts = {}
    concept_refs = {}
    for num, title, name, desc in key_concepts_all:
        if name not in concept_counts:
            concept_counts[name] = 0
            concept_refs[name] = []
        concept_counts[name] += 1
        if num not in concept_refs[name]:
            concept_refs[name].append(num)

    # 列出出现2次及以上的概念
    multi_concepts = {k: v for k, v in concept_counts.items() if v >= 2}
    for name in sorted(multi_concepts.keys()):
        refs = sorted(concept_refs[name])
        ref_str = ", ".join([f"第{n}章" for n in refs[:8]])
        if len(refs) > 8:
            ref_str += f" 等（共{len(refs)}章）"
        lines.append(f"- **{name}**：{ref_str}\n")

    lines.append("\n## 单章核心概念精选\n\n")
    for num, title, theme in core_themes[:10]:
        chapter_concepts = [name for n, t, name, d in key_concepts_all if n == num][:5]
        if chapter_concepts:
            lines.append(f"- **{title}**：{', '.join(chapter_concepts)}\n")

    lines.append("\n## 跨章节知识关联图谱\n\n")
    lines.append("```\n")
    lines.append("道 —— 无名/无为/自然 —— 贯穿全书\n")
    lines.append("德 —— 上德不德/含德之厚 —— 下篇主线\n")
    lines.append("柔弱胜刚强 —— 水/婴儿/雌柔 —— 多章呼应\n")
    lines.append("反者道之动 —— 祸福/有无/难易 —— 辩证结构\n")
    lines.append("治国 —— 无为而治/小国寡民 —— 政治哲学\n")
    lines.append("修身 —— 知足/知止/清静 —— 个人修养\n")
    lines.append("```\n")

    output.write_text(''.join(lines), encoding='utf-8')
    print(f"总索引已生成: {output}")
    print(f"章节数: {len(report_files)}")
    print(f"重复出现核心概念数: {len(multi_concepts)}")


if __name__ == "__main__":
    main()
