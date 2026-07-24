#!/usr/bin/env python3
"""
evidence_migrate.py — 批量迁移现有论据卡片到新字段体系

用法：
  python evidence_migrate.py --dry-run          # 预览变更，不写入
  python evidence_migrate.py                    # 执行迁移
  python evidence_migrate.py --vault /path      # 指定论据库路径

功能：
1. 为缺少 topic 的卡片，根据旧 topics / tags / title / 内容推断嵌套主题标签
2. 为缺少 scene 的卡片，根据 type 和标题推断应用场景
3. 为缺少六维评分的卡片，做 AI 自动初评（quality_status = ai-estimated）
4. 补充 subtype、date、status、updated 等字段
5. 不修改 id、文件名和核心正文，保持 Obsidian 双向链接有效
6. 生成迁移报告
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

DEFAULT_VAULT = "/Users/chouchou/Documents/Obsidian Vault/九局下半怎么破局/参考资料/论据库"

# 旧 topics/tags 到新 topic 嵌套标签的推断映射
TOPIC_MAP = {
    # 心理/个人成长
    "个人成长": "#主题/心理/个人成长",
    "自我管理": "#主题/心理/自我管理",
    "自我认知": "#主题/心理/认知",
    "自我反思": "#主题/心理/认知",
    "自我教育": "#主题/心理/个人成长",
    "自我修正": "#主题/心理/个人成长",
    "自我维护": "#主题/心理/自我管理",
    "身份": "#主题/心理/自我认同",
    "身份认同": "#主题/心理/自我认同",
    "身份负债": "#主题/心理/自我认同",
    "人生设计": "#主题/心理/个人成长",
    "成长型思维": "#主题/心理/个人成长",
    "长期主义": "#主题/心理/个人成长",
    "坚持": "#主题/心理/意志力",
    "耐心": "#主题/心理/意志力",
    "意志力": "#主题/心理/意志力",
    "动力": "#主题/心理/动机",
    "激情": "#主题/心理/动机",
    "热情": "#主题/心理/动机",
    "乐趣": "#主题/心理/动机",
    "心流": "#主题/心理/心流",
    "专注": "#主题/心理/注意力",
    "注意力": "#主题/心理/注意力",
    "心理能量": "#主题/心理/能量管理",
    "心理熵": "#主题/心理/能量管理",
    "情绪": "#主题/心理/情绪",
    "痛苦": "#主题/心理/情绪",
    "困难": "#主题/心理/情绪",
    "心理健康": "#主题/心理/情绪",
    "心理资本": "#主题/心理/情绪",
    "认知": "#主题/心理/认知",
    "决策": "#主题/心理/决策",
    "意图": "#主题/心理/决策",
    "选择": "#主题/心理/决策",
    "行为": "#主题/心理/行为",
    "习惯": "#主题/心理/习惯",
    "多巴胺": "#主题/心理/习惯",
    "廉价多巴胺": "#主题/心理/习惯",
    "反馈": "#主题/心理/习惯",
    "失败": "#主题/心理/ resilience",
    "错误": "#主题/心理/ resilience",
    "试错": "#主题/心理/ resilience",
    "低谷": "#主题/心理/ resilience",
    "挣扎": "#主题/心理/ resilience",
    "愿景": "#主题/心理/目标管理",
    "目标": "#主题/心理/目标管理",
    "目标设定": "#主题/心理/目标管理",
    "标准": "#主题/心理/目标管理",
    "使命": "#主题/心理/目标管理",
    "项目": "#主题/心理/目标管理",
    "杠杆": "#主题/心理/方法论",
    "优先级": "#主题/心理/方法论",
    "优先阶梯": "#主题/心理/方法论",
    "时间管理": "#主题/心理/方法论",
    "深度工作": "#主题/心理/方法论",
    "深潜": "#主题/心理/方法论",
    "基本功": "#主题/心理/方法论",
    "原理": "#主题/心理/方法论",
    "基本原理": "#主题/心理/方法论",
    "方法论": "#主题/心理/方法论",
    "实验": "#主题/心理/方法论",
    "迭代": "#主题/心理/方法论",
    "挑战": "#主题/心理/成长",
    "好奇心": "#主题/心理/成长",
    "限制": "#主题/心理/创造力",
    "routine": "#主题/心理/习惯",
    "行动": "#主题/心理/行动力",
    "行动号召": "#主题/心理/行动力",
    "消失": "#主题/心理/专注力",
    "投资": "#主题/经济/投资",
    "消费主义": "#主题/经济/消费",
    # 商业/创业
    "创业": "#主题/商业/创业",
    "被动收入": "#主题/商业/创业",
    "一人商业": "#主题/商业/创业",
    "创作者": "#主题/商业/创业",
    "产品": "#主题/商业/产品",
    "流量": "#主题/商业/营销",
    "报价": "#主题/商业/营销",
    "机会识别": "#主题/商业/战略",
    "商业": "#主题/商业",
    "营销": "#主题/商业/营销",
    "管理": "#主题/商业/管理",
    "战略": "#主题/商业/战略",
    "创新": "#主题/商业/创新",
    "精通": "#主题/商业/职业",
    # 科技
    "AI": "#主题/科技/AI",
    "人工智能": "#主题/科技/AI",
    "算法": "#主题/科技/AI",
    "互联网": "#主题/科技/互联网",
    "科技": "#主题/科技",
    # 社会
    "社会": "#主题/社会",
    "就业": "#主题/社会/就业",
    "中年失业": "#主题/社会/就业",
    "中年转型": "#主题/社会/中年转型",
    "80后": "#主题/社会/代际",
    "教育": "#主题/社会/教育",
    "社会认知": "#主题/社会/社会认知",
    "社会剧本": "#主题/社会/社会认知",
    "劳动力市场": "#主题/经济/劳动力市场",
    "失业": "#主题/社会/就业",
    "失业率": "#主题/社会/就业",
    "再就业": "#主题/社会/就业",
    "招聘": "#主题/商业/管理",
    "求职": "#主题/社会/就业",
    "责任": "#主题/心理/责任感",
    "心智成长": "#主题/心理/个人成长",
    "抗压": "#主题/心理/ resilience",
    "压力": "#主题/心理/ resilience",
    # 文化/哲学
    "文化": "#主题/文化",
    "历史": "#主题/文化/历史",
    "哲学": "#主题/文化/哲学",
    "秩序": "#主题/文化/哲学",
    "熵增": "#主题/文化/哲学",
    # 经济
    "经济": "#主题/经济",
    "宏观经济": "#主题/经济/宏观经济",
    "金融": "#主题/经济/金融",
    "消费": "#主题/经济/消费",
}

# 根据 type 推断默认 subtype
SUBTYPE_DEFAULT = {
    "概念": "思维框架",
    "数据": "统计数据",
    "案例": "人物故事",
    "金句": "书籍摘录"
}

# 根据 type 推断默认 scene
SCENE_DEFAULT = {
    "概念": "#场景/核心论据",
    "数据": "#场景/核心论据",
    "案例": "#场景/核心论据",
    "金句": "#场景/开头吸引"
}


def get_md_files(vault_dir):
    files = []
    for subdir in ["概念", "数据", "案例", "金句"]:
        d = Path(vault_dir) / subdir
        if d.exists():
            files.extend(sorted(d.glob("*.md")))
    return files


def parse_frontmatter(text):
    if not text.startswith("---"):
        return None, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None, text
    return parts[1].strip(), parts[2].strip()


def fm_to_dict(fm_text):
    """简单 YAML 解析，保留列表字面量字符串"""
    result = {}
    if not fm_text:
        return result
    for line in fm_text.split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, val = line.split(":", 1)
        result[key.strip()] = val.strip()
    return result


def parse_old_list(raw):
    """解析旧 frontmatter 中的列表字段，如 [a, b, c]"""
    if not raw:
        return []
    # 先取中括号内的内容
    m = re.search(r"\[(.*?)\]", raw)
    if not m:
        return []
    inner = m.group(1)
    # 按逗号分割，并处理中文逗号
    items = re.split(r"[,，]", inner)
    return [item.strip().strip('"').strip("'") for item in items if item.strip()]


def extract_old_topics(fm):
    """从旧 topics 字段提取列表"""
    return parse_old_list(fm.get("topics", ""))


def extract_old_tags(fm):
    return parse_old_list(fm.get("tags", ""))


def infer_topic(fm, title, body):
    """根据旧 topics/tags/title/source 推断新的 topic 嵌套标签"""
    topics = set()
    for t in extract_old_topics(fm):
        mapped = TOPIC_MAP.get(t.strip())
        if mapped:
            topics.add(mapped)
    for t in extract_old_tags(fm):
        mapped = TOPIC_MAP.get(t.strip())
        if mapped:
            topics.add(mapped)

    # 根据标题关键词兜底
    title_lower = title.lower()
    keyword_map = {
        "失业": "#主题/社会/就业",
        "求职": "#主题/社会/就业",
        "招聘": "#主题/商业/管理",
        "心理": "#主题/心理/情绪",
        "习惯": "#主题/心理/习惯",
        "决策": "#主题/心理/决策",
        "认知": "#主题/心理/认知",
        "AI": "#主题/科技/AI",
        "人工智能": "#主题/科技/AI",
        "互联网": "#主题/科技/互联网",
        "商业": "#主题/商业",
        "营销": "#主题/商业/营销",
        "创业": "#主题/商业/创业",
        "经济": "#主题/经济",
        "社会": "#主题/社会",
        "文化": "#主题/文化",
        "历史": "#主题/文化/历史",
    }
    for kw, mapped in keyword_map.items():
        if kw in title_lower:
            topics.add(mapped)

    # 如果仍无主题，根据来源推断（如 Dan Koe 课程默认心理/个人成长）
    source = fm.get("source", "")
    if not topics:
        if "Dan Koe" in source or "DanKoe" in source:
            topics.add("#主题/心理/个人成长")
        elif "Council" in source:
            topics.add("#主题/心理/情绪")
        elif "网络综合" in source or "新浪" in source or "微信" in source:
            topics.add("#主题/社会")
        else:
            topics.add("#主题/未分类")

    return list(topics)[:3]


def infer_scene(fm, evtype, title):
    """推断应用场景"""
    # 如果标题含某些关键词，优先判断
    if any(k in title for k in ["不是", "反而", "醒", "丢人", " ashamed"]):
        return ["#场景/开头吸引"]
    if any(k in title for k in ["建议", "行动", "步骤", "明天", "今天", "如何做"]):
        return ["#场景/结尾升华"]
    return [SCENE_DEFAULT.get(evtype, "#场景/核心论据")]


def infer_subtype(fm, evtype):
    """推断 subtype"""
    return fm.get("subtype", SUBTYPE_DEFAULT.get(evtype, ""))


def ai_estimate_scores(fm, title, body):
    """基于简单启发规则做六维初评，返回分数字典"""
    source = fm.get("source", "")
    has_url = bool(fm.get("url", "").strip())
    has_date = bool(fm.get("date", "").strip())
    core_match = re.search(r'## 核心内容\s*\n+(.+?)(?:\n##|\Z)', body, re.S)
    core_text = core_match.group(1).strip() if core_match else ""
    core_len = len(core_text)

    # reliability
    if "课程" in source or "书" in source or "《" in source:
        reliability = 4
    elif "网络" in source or "自述" in source or source == "":
        reliability = 2
    else:
        reliability = 3
    if has_url:
        reliability = min(5, reliability + 1)

    # relevance: 默认较高，因为已入库
    relevance = 4

    # timeliness
    if has_date:
        timeliness = 4
    elif "2024" in source or "2023" in source:
        timeliness = 4
    elif "课程" in source or "《" in source:
        timeliness = 4
    else:
        timeliness = 3

    # sufficiency
    if core_len > 100:
        sufficiency = 4
    elif core_len > 50:
        sufficiency = 3
    else:
        sufficiency = 2

    # diversity
    diversity = 3

    # verifiability
    verifiability = 4 if has_url else 3

    scores = {
        "relevance": relevance,
        "reliability": reliability,
        "timeliness": timeliness,
        "sufficiency": sufficiency,
        "diversity": diversity,
        "verifiability": verifiability,
    }
    scores["quality"] = round(sum(scores.values()) / 6)
    return scores


def build_new_frontmatter(fm, evtype, title, body, today):
    """构建新的 frontmatter 字典"""
    new_fm = {}
    # 保留已有字段
    for k in ["id", "type", "title", "source", "author", "url", "file", "date"]:
        if k in fm and fm[k]:
            new_fm[k] = fm[k]

    # 确保基础字段存在
    new_fm["type"] = evtype
    new_fm["subtype"] = infer_subtype(fm, evtype)
    if "id" not in new_fm:
        new_fm["id"] = ""

    # 三维标签
    topic_list = infer_topic(fm, title, body)
    scene_list = infer_scene(fm, evtype, title)
    new_fm["topic"] = topic_list
    new_fm["scene"] = scene_list

    # tags 保留并去重
    old_tags = extract_old_tags(fm)
    # 过滤掉已被 topic 映射的 tags
    topic_kw = set()
    for t in topic_list:
        topic_kw.update(t.replace("#主题/", "").split("/"))
    tags = [t for t in old_tags if t not in topic_kw][:5]
    new_fm["tags"] = tags if tags else []

    # 六维评分
    if "quality" in fm and fm["quality"]:
        try:
            new_fm["quality"] = int(float(fm["quality"]))
            for dim in ["relevance", "reliability", "timeliness", "sufficiency", "diversity", "verifiability"]:
                if dim in fm:
                    new_fm[dim] = int(float(fm[dim]))
                else:
                    new_fm[dim] = new_fm["quality"]
            new_fm["quality_status"] = fm.get("quality_status", "human-confirmed")
        except ValueError:
            scores = ai_estimate_scores(fm, title, body)
            new_fm.update(scores)
            new_fm["quality_status"] = "ai-estimated"
    else:
        scores = ai_estimate_scores(fm, title, body)
        new_fm.update(scores)
        new_fm["quality_status"] = "ai-estimated"

    # 管理字段
    new_fm["status"] = fm.get("status", "active")
    new_fm["created"] = fm.get("created", today)
    new_fm["updated"] = today

    return new_fm


def format_frontmatter(new_fm):
    """把 frontmatter 字典格式化为 YAML 文本"""
    lines = ["---"]

    def fmt_val(v):
        if isinstance(v, list):
            if not v:
                return "[]"
            return "[" + ", ".join(str(x) for x in v) + "]"
        if isinstance(v, str):
            return v
        return str(v)

    # 分组输出
    lines.append("")
    lines.append("# 基础信息")
    for k in ["id", "type", "subtype", "title", "source", "author", "url", "file", "date"]:
        if k in new_fm:
            lines.append(f"{k}: {fmt_val(new_fm[k])}")

    lines.append("")
    lines.append("# 管理字段")
    for k in ["status", "created", "updated"]:
        if k in new_fm:
            lines.append(f"{k}: {fmt_val(new_fm[k])}")

    lines.append("")
    lines.append("# 三维标签")
    for k in ["topic", "scene", "tags"]:
        if k in new_fm:
            lines.append(f"{k}: {fmt_val(new_fm[k])}")

    lines.append("")
    lines.append("# 六维质量评分（1-5）")
    lines.append(f"quality: {fmt_val(new_fm.get('quality', 3))}")
    for dim in ["relevance", "reliability", "timeliness", "sufficiency", "diversity", "verifiability"]:
        lines.append(f"{dim}: {fmt_val(new_fm.get(dim, 3))}")
    lines.append(f"quality_status: {fmt_val(new_fm.get('quality_status', 'ai-estimated'))}")

    lines.append("---")
    return "\n".join(lines)


def migrate_file(path, dry_run=False, today=None):
    text = path.read_text(encoding="utf-8")
    fm_text, body = parse_frontmatter(text)
    if fm_text is None:
        return {"path": str(path), "status": "skip_no_frontmatter"}

    fm = fm_to_dict(fm_text)
    evtype = fm.get("type", path.parent.name.replace("s", ""))
    # 兼容英文 type
    type_map = {"concept": "概念", "data": "数据", "case": "案例", "quote": "金句"}
    evtype = type_map.get(evtype, evtype)
    title = fm.get("title", path.stem)

    new_fm = build_new_frontmatter(fm, evtype, title, body, today)
    new_text = format_frontmatter(new_fm) + "\n\n" + body.strip() + "\n"

    if not dry_run:
        path.write_text(new_text, encoding="utf-8")

    return {
        "path": str(path),
        "status": "migrated",
        "id": new_fm.get("id"),
        "topic": new_fm.get("topic"),
        "scene": new_fm.get("scene"),
        "quality": new_fm.get("quality"),
        "quality_status": new_fm.get("quality_status")
    }


def main():
    parser = argparse.ArgumentParser(description="论据库批量迁移")
    parser.add_argument("--vault", default=DEFAULT_VAULT, help="论据库路径")
    parser.add_argument("--dry-run", action="store_true", help="预览变更，不写入")
    args = parser.parse_args()

    today = datetime.now().strftime("%Y-%m-%d")
    files = get_md_files(args.vault)
    report = []
    stats = {"migrated": 0, "skipped": 0, "ai_estimated": 0}

    for f in files:
        result = migrate_file(f, dry_run=args.dry_run, today=today)
        report.append(result)
        if result["status"] == "migrated":
            stats["migrated"] += 1
            if result.get("quality_status") == "ai-estimated":
                stats["ai_estimated"] += 1
        else:
            stats["skipped"] += 1

    # 输出报告
    mode = "【预览模式】" if args.dry_run else "【已执行】"
    print(f"{mode} 共处理 {len(files)} 个文件")
    print(f"  迁移：{stats['migrated']}")
    print(f"  跳过（无 frontmatter）：{stats['skipped']}")
    print(f"  AI 初评需复核：{stats['ai_estimated']}")
    print()

    report_path = Path(args.vault) / "迁移报告.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"迁移报告已保存：{report_path}")

    if not args.dry_run:
        print("\n注意：quality_status=ai-estimated 的条目建议人工复核。")


if __name__ == "__main__":
    main()
