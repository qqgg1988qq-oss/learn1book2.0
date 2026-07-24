#!/usr/bin/env python3
"""
合并非行子代理提取的论据 JSON 文件，去重后写入论据库。
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from datetime import datetime

VAULT = "/Users/chouchou/Documents/Obsidian Vault/九局下半怎么破局/参考资料/论据库"
TMP_DIR = Path("/Users/chouchou/Documents/Obsidian Vault/成长计划/读书计划/道德经全解/.evidence-tmp")


def get_next_id(evtype: str) -> int:
    """获取某类型下一个可用编号。"""
    type_map = {"概念": "概念", "数据": "数据", "案例": "案例", "金句": "金句"}
    subdir = Path(VAULT) / type_map.get(evtype, evtype)
    if not subdir.exists():
        return 1
    max_num = 0
    for f in subdir.glob("*.md"):
        m = re.search(r'-(\d+)\.md$', f.name)
        if m:
            max_num = max(max_num, int(m.group(1)))
    return max_num + 1


def check_duplicate(title: str, content: str, evtype: str) -> dict:
    """调用 evidence_dedup.py 检查重复。"""
    script = Path(__file__).parent.parent / "evidence-collector/scripts/evidence_dedup.py"
    try:
        result = subprocess.run(
            [sys.executable, str(script), "--title", title, "--content", content, "--type", evtype],
            capture_output=True, text=True, timeout=60
        )
        return json.loads(result.stdout.strip().split('\n')[-1])
    except Exception as e:
        print(f"去重检查失败: {e}", file=sys.stderr)
        return {"action": "new", "similarity": 0.0}


def to_filename(name: str) -> str:
    name = re.sub(r'[\\/*?:"\u003c\u003e|]', "", name)
    name = re.sub(r'\s+', "_", name.strip())
    return name[:40]


def build_card(ev: dict, ev_id: str, created: str) -> str:
    """根据论据字典生成 Markdown 卡片。"""
    evtype = ev["type"]
    subtype = ev.get("subtype", "")
    title = ev["title"]
    source = ev.get("source", "道德经白话全译")
    author = ev.get("author", "老子/文史哲")
    date = ev.get("date", "2012-07-01")
    topic = ev.get("topic", ["#主题/文化/哲学"])
    scene = ev.get("scene", ["#场景/核心论据"])
    tags = ev.get("tags", [])
    quality = ev.get("quality", 4)
    relevance = ev.get("relevance", 4)
    reliability = ev.get("reliability", 4)
    timeliness = ev.get("timeliness", 3)
    sufficiency = ev.get("sufficiency", 4)
    diversity = ev.get("diversity", 3)
    verifiability = ev.get("verifiability", 4)
    core = ev.get("core", "")
    quote = ev.get("quote", "")
    usage = ev.get("usage", "")
    boundary = ev.get("boundary", "")

    # 格式化列表
    topic_str = str(topic) if isinstance(topic, list) else f"[{topic}]"
    scene_str = str(scene) if isinstance(scene, list) else f"[{scene}]"
    tags_str = str(tags) if isinstance(tags, list) else f"[{tags}]"

    card = f"""---
# 基础信息
id: {ev_id}
type: {evtype}
subtype: {subtype}
title: {title}
source: {source}
author: {author}
url: ""
file: ""
date: {date}
created: {created}
updated: {created}
status: active

# 三维标签
topic: {topic_str}
scene: {scene_str}
tags: {tags_str}

# 六维质量评分（1-5）
quality: {quality}
relevance: {relevance}
reliability: {reliability}
timeliness: {timeliness}
sufficiency: {sufficiency}
diversity: {diversity}
verifiability: {verifiability}
quality_status: ai-estimated
---

## 核心内容

{core}

## 原文摘录

> {quote}

## 适用场景

- {usage}

## 使用提示

{usage}

## 边界与局限

{boundary}

## 关联论据

- 来源章节：{ev.get('chapter', '')}
"""
    return card


def update_index(new_items: list):
    """更新论据库 00-索引.md。"""
    index_path = Path(VAULT) / "00-索引.md"
    today = datetime.now().strftime("%Y-%m-%d")
    entries = []
    for item in new_items:
        entries.append(
            f"- {item['id']} | {item['type']} | {item['title']} | "
            f"质量:{item['quality']} | 来源:{item['source']} | topic:{item['topic']} | scene:{item['scene']} | 日期:{today}\n"
        )

    if index_path.exists():
        text = index_path.read_text(encoding='utf-8')
    else:
        text = "# 论据库索引\n\n"

    text += f"\n## 新增 — 道德经白话全译 ({today})\n\n"
    text += ''.join(entries)
    index_path.write_text(text, encoding='utf-8')


def main():
    if not TMP_DIR.exists():
        print(f"临时目录不存在: {TMP_DIR}")
        return

    all_evidence = []
    for f in sorted(TMP_DIR.glob("batch-*.json")):
        try:
            data = json.loads(f.read_text(encoding='utf-8'))
            all_evidence.extend(data.get('evidence', []))
        except Exception as e:
            print(f"读取 {f} 失败: {e}", file=sys.stderr)

    print(f"共读取 {len(all_evidence)} 条待处理论据")

    # 按类型分别处理编号
    type_counters = {
        "概念": get_next_id("概念") - 1,
        "数据": get_next_id("数据") - 1,
        "案例": get_next_id("案例") - 1,
        "金句": get_next_id("金句") - 1,
    }

    created = datetime.now().strftime("%Y-%m-%d")
    new_items = []
    skipped = 0
    merged = 0

    type_map = {"概念": "概念", "数据": "数据", "案例": "案例", "金句": "金句"}

    for ev in all_evidence:
        evtype = ev.get("type")
        if evtype not in type_map:
            continue

        title = ev.get("title", "")
        core = ev.get("core", "")
        dup = check_duplicate(title, core, evtype)

        if dup.get("action") == "skip":
            skipped += 1
            continue
        if dup.get("action") == "merge":
            # 简单合并：追加来源信息到已有文件
            target_id = dup.get("id")
            subdir = Path(VAULT) / type_map[evtype]
            target_file = subdir / f"{target_id.lower()}.md"
            if target_file.exists():
                text = target_file.read_text(encoding='utf-8')
                chap = ev.get('chapter', '')
                append = f"\n- 补充来源：{chap}\n"
                target_file.write_text(text + append, encoding='utf-8')
            merged += 1
            continue

        type_counters[evtype] += 1
        num = type_counters[evtype]
        ev_id = f"{evtype.upper()}-{num:04d}"
        ev["id"] = ev_id

        card = build_card(ev, ev_id, created)
        subdir = Path(VAULT) / type_map[evtype]
        subdir.mkdir(parents=True, exist_ok=True)
        filename = f"{ev_id.lower()}.md"
        (subdir / filename).write_text(card, encoding='utf-8')
        new_items.append(ev)

    if new_items:
        update_index(new_items)

    print(f"新增: {len(new_items)}, 跳过重复: {skipped}, 合并: {merged}")


if __name__ == "__main__":
    main()
