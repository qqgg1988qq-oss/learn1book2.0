#!/usr/bin/env python3
"""
evidence_dedup.py — 论据库去重与合并（v2）

用法：
  python evidence_dedup.py --title "复利效应" --content "每天进步1%..." --type 概念
  python evidence_dedup.py --title "失败组合" --content "主动积累可控的小失败" --type 概念 --threshold 0.7

返回 JSON：
  {"action": "skip", "id": "CONCEPT-0001", "similarity": 0.92}
  {"action": "merge", "id": "CONCEPT-0001", "similarity": 0.65}
  {"action": "new", "similarity": 0.0}

说明：
- 使用 TF-IDF + 字符 ngram 计算相似度
- 无需 PyTorch，依赖 scikit-learn（首次自动安装）
- 只与同类型的已有论据比较
- v2 增强：把 topic、scene、title 一并纳入去重文本，降低同义不同场景的误合并
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path

DEFAULT_VAULT = "/Users/chouchou/Documents/Obsidian Vault/九局下半怎么破局/参考资料/论据库"


def get_md_files(vault_dir, evtype):
    """获取某类型下所有 markdown 文件"""
    type_map = {
        "概念": "概念",
        "数据": "数据",
        "案例": "案例",
        "金句": "金句"
    }
    subdir = type_map.get(evtype, evtype)
    d = Path(vault_dir) / subdir
    if d.exists():
        return sorted(d.glob("*.md"))
    return []


def parse_frontmatter(text):
    """解析 YAML frontmatter，保留列表字面量"""
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    fm_text = parts[1].strip()
    body = parts[2].strip()
    fm = {}
    for line in fm_text.split("\n"):
        if ":" in line and not line.strip().startswith("#"):
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip()
            fm[key] = val
    return fm, body


def extract_list_field(fm, key):
    """从 frontmatter 字符串中提取形如 [#主题/商业, #主题/心理] 的列表"""
    raw = fm.get(key, "")
    return re.findall(r"#([\u4e00-\u9fa5a-zA-Z0-9_/]+)", raw)


def load_items(vault_dir, evtype):
    """加载某类型的所有论据"""
    items = []
    for f in get_md_files(vault_dir, evtype):
        text = f.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(text)
        if not fm.get("id"):
            continue
        title = fm.get("title", f.stem)
        tags = extract_list_field(fm, "tags")
        topics = extract_list_field(fm, "topic")
        scenes = extract_list_field(fm, "scene")
        # 提取核心内容，加权构建去重文本
        core_match = re.search(r'## 核心内容\s*\n+(.+?)(?:\n##|\Z)', body, re.S)
        core_text = core_match.group(1).strip().replace('\n', ' ') if core_match else body[:400]

        content = " ".join([
            title, title, title,
            core_text, core_text,
            fm.get("source", ""),
            " ".join(topics), " ".join(topics),
            " ".join(scenes),
            " ".join(tags),
            body[:300]
        ])
        items.append({
            "id": fm.get("id"),
            "title": title,
            "path": str(f),
            "content": content,
            "topics": topics,
            "scenes": scenes
        })
    return items


def ensure_sklearn():
    try:
        import sklearn
        return True
    except ImportError:
        print("正在安装 scikit-learn...", file=sys.stderr)
        code = os.system(f"{sys.executable} -m pip install scikit-learn -q")
        if code != 0:
            print("安装 scikit-learn 失败。", file=sys.stderr)
            return False
        return True


def cosine_similarity(a, b):
    import math
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0
    return dot / (norm_a * norm_b)


def check_duplicate(title, content, evtype, vault_dir, threshold_high=0.80, threshold_merge=0.50):
    """检查新论据是否与已有论据重复或相近"""
    items = load_items(vault_dir, evtype)
    if not items:
        return {"action": "new", "similarity": 0.0}

    if not ensure_sklearn():
        return {"action": "new", "similarity": 0.0, "note": "sklearn 不可用，跳过去重"}

    from sklearn.feature_extraction.text import TfidfVectorizer

    new_text = " ".join([title, title, content])
    all_texts = [it["content"] for it in items] + [new_text]

    vectorizer = TfidfVectorizer(
        analyzer='char_wb',
        ngram_range=(2, 4),
        lowercase=False,
        max_df=0.95,
        min_df=1
    )
    try:
        matrix = vectorizer.fit_transform(all_texts).toarray()
    except Exception:
        return {"action": "new", "similarity": 0.0}

    new_vec = matrix[-1]
    best_sim = 0
    best_item = None
    for i, item in enumerate(items):
        sim = cosine_similarity(new_vec, matrix[i])
        if sim > best_sim:
            best_sim = sim
            best_item = item

    if best_sim >= threshold_high:
        return {"action": "skip", "id": best_item["id"], "title": best_item["title"], "similarity": round(best_sim, 3)}
    elif best_sim >= threshold_merge:
        return {"action": "merge", "id": best_item["id"], "title": best_item["title"], "similarity": round(best_sim, 3)}
    else:
        return {"action": "new", "similarity": round(best_sim, 3)}


def main():
    parser = argparse.ArgumentParser(description="论据库去重检查")
    parser.add_argument("--title", required=True, help="新论据标题")
    parser.add_argument("--content", required=True, help="新论据核心内容")
    parser.add_argument("--type", required=True, choices=["概念", "数据", "案例", "金句"], help="论据类型")
    parser.add_argument("--vault", default=DEFAULT_VAULT, help="论据库路径")
    parser.add_argument("--threshold-high", type=float, default=0.80, help="视为重复的阈值")
    parser.add_argument("--threshold-merge", type=float, default=0.50, help="视为可合并的阈值")
    args = parser.parse_args()

    result = check_duplicate(
        args.title,
        args.content,
        args.type,
        args.vault,
        threshold_high=args.threshold_high,
        threshold_merge=args.threshold_merge
    )
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
