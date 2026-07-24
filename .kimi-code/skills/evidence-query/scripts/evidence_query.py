#!/usr/bin/env python3
"""
evidence_query.py — 本地论据库检索脚本（v2）

用法：
  python evidence_query.py "中年失业后的出路"
  python evidence_query.py "习惯养成的方法" --top 10
  python evidence_query.py "复利效应" --rebuild
  python evidence_query.py "中年失业" --type 数据 --min-quality 4
  python evidence_query.py "AI" --topic "主题/科技" --scene "场景/核心论据" --sort quality

说明：
- 默认读取 /Users/chouchou/Documents/Obsidian Vault/九局下半怎么破局/参考资料/论据库/
- 支持关键词 + TF-IDF 语义 + 字段加权 + 质量分加成的混合排序
- 支持按 --type / --topic / --scene / --min-quality / --sort 筛选
- 无需安装 PyTorch 或深度学习库，依赖仅为 scikit-learn
"""

import os
import re
import sys
import json
import argparse
import hashlib
from pathlib import Path

# 默认论据库路径
DEFAULT_VAULT = "/Users/chouchou/Documents/Obsidian Vault/九局下半怎么破局/参考资料/论据库"
CACHE_FILE = os.path.join(DEFAULT_VAULT, ".evidence_tfidf_cache.json")


def get_md_files(vault_dir):
    """获取论据库中所有 markdown 文件"""
    files = []
    for subdir in ["概念", "数据", "案例", "金句"]:
        d = Path(vault_dir) / subdir
        if d.exists():
            files.extend(sorted(d.glob("*.md")))
    return files


def parse_frontmatter(text):
    """解析 YAML frontmatter"""
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
            fm[key.strip()] = val.strip()
    return fm, body


def extract_list_field(fm, key):
    """提取形如 [#主题/商业, #主题/心理] 的列表"""
    raw = fm.get(key, "")
    return re.findall(r"#([\u4e00-\u9fa5a-zA-Z0-9_/]+)", raw)


def load_evidence(vault_dir):
    """加载所有论据文件"""
    items = []
    for f in get_md_files(vault_dir):
        text = f.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(text)
        if not fm.get("id"):
            continue
        title = fm.get("title", f.stem)
        source = fm.get("source", "")
        tags = extract_list_field(fm, "tags")
        topics = extract_list_field(fm, "topic")
        scenes = extract_list_field(fm, "scene")

        # 质量分，兼容旧格式
        try:
            quality = int(float(fm.get("quality", "3")))
        except ValueError:
            quality = 3

        # 加权拼接：标题、topic、tags 权重更高
        content = " ".join([
            title, title,
            source,
            " ".join(topics), " ".join(topics),
            " ".join(scenes),
            " ".join(tags), " ".join(tags),
            body[:1200]
        ])
        items.append({
            "id": fm.get("id"),
            "type": fm.get("type", "未知"),
            "subtype": fm.get("subtype", ""),
            "title": title,
            "source": source,
            "path": str(f),
            "tags": tags,
            "topic": topics,
            "scene": scenes,
            "quality": quality,
            "body": body[:800],
            "content": content
        })
    return items


def file_hash(path):
    """计算文件内容 hash"""
    return hashlib.md5(Path(path).read_bytes()).hexdigest()


def extract_summary(body):
    """从 body 中提取核心内容段落作为摘要"""
    m = re.search(r'## 核心内容\s*\n+(.+?)(?:\n##|\Z)', body, re.S)
    if m:
        s = m.group(1).strip().replace('\n', ' ')
        return s[:200] + '...' if len(s) > 200 else s
    # 兜底：去掉 markdown 标记
    s = re.sub(r'[#*>\[\]\-`]', '', body).replace('\n', ' ').strip()
    return s[:200] + '...' if len(s) > 200 else s


def ensure_sklearn():
    """确保 scikit-learn 已安装"""
    try:
        import sklearn
        return True
    except ImportError:
        print("正在安装 scikit-learn...")
        code = os.system(f"{sys.executable} -m pip install scikit-learn -q")
        if code != 0:
            print("安装 scikit-learn 失败，将仅使用关键词检索。")
            return False
        return True


def build_tfidf(items, force=False):
    """生成或加载 TF-IDF 缓存"""
    cache_exists = os.path.exists(CACHE_FILE)
    cache = {}
    if cache_exists and not force:
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                loaded = json.load(f)
            if isinstance(loaded, dict) and "matrix" in loaded:
                cache = loaded
        except Exception:
            cache = {}

    # 检查是否需要重建
    current_hashes = {it["id"]: file_hash(it["path"]) for it in items}
    cache_hashes = {}
    if isinstance(cache.get("items"), list):
        cache_hashes = {it.get("id", ""): it.get("hash", "") for it in cache["items"]}
    need_rebuild = force or current_hashes != cache_hashes

    if not need_rebuild:
        return cache

    if not ensure_sklearn():
        return None

    from sklearn.feature_extraction.text import TfidfVectorizer

    texts = [it["content"] for it in items]
    vectorizer = TfidfVectorizer(
        analyzer='char_wb',
        ngram_range=(2, 4),
        lowercase=False,
        max_df=0.95,
        min_df=1
    )
    try:
        matrix = vectorizer.fit_transform(texts)
        feature_names = vectorizer.get_feature_names_out().tolist()
        dense = matrix.toarray()
        cache = {
            "vectorizer": feature_names,
            "matrix": dense.tolist(),
            "items": [
                {
                    "id": it["id"],
                    "hash": file_hash(it["path"])
                }
                for it in items
            ]
        }
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False)
    except Exception as e:
        print(f"TF-IDF 构建失败: {e}")
        return None

    return cache


def cosine_similarity(a, b):
    import math
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0
    return dot / (norm_a * norm_b)


def vectorize_query(query, feature_names):
    """把查询词转成与缓存同维度的向量"""
    vec = [0.0] * len(feature_names)
    for i, feat in enumerate(feature_names):
        if feat in query:
            vec[i] += query.count(feat)
    return vec


def keyword_score(query, item):
    """关键词匹配得分"""
    q = query.lower()
    score = 0
    fields = [
        (item["title"], 3),
        (item["source"], 1),
        (" ".join(item["tags"]), 2),
        (" ".join(item["topic"]), 3),
        (" ".join(item["scene"]), 2),
        (item["body"], 1)
    ]
    for field, weight in fields:
        f = field.lower()
        if q in f:
            score += f.count(q) * weight
    # 也支持分词后的单字匹配
    for token in re.findall(r"[\u4e00-\u9fa5]{2,}", q):
        for field, weight in fields:
            f = field.lower()
            if token in f:
                score += f.count(token) * weight * 0.5
    return score


def filter_items(items, evtype=None, topic=None, scene=None, min_quality=None):
    """按类型/主题/场景/质量分筛选"""
    result = items
    if evtype:
        result = [it for it in result if it["type"] == evtype]
    if topic:
        # 支持部分匹配，如 "主题/商业" 可匹配 "主题/商业/营销"
        result = [it for it in result if any(topic in t for t in it["topic"])]
    if scene:
        result = [it for it in result if any(scene in s for s in it["scene"])]
    if min_quality is not None:
        result = [it for it in result if it["quality"] >= min_quality]
    return result


def search(query, vault_dir, top_n=5, force=False, evtype=None, topic=None, scene=None, min_quality=None, sort_by="relevance"):
    items = load_evidence(vault_dir)
    if not items:
        print("论据库为空，请先收集一些论据。")
        return

    # 先筛选
    filtered = filter_items(items, evtype, topic, scene, min_quality)
    if not filtered:
        print("筛选后无匹配论据，请放宽条件。")
        return

    cache = build_tfidf(items, force=force)

    query_vec = None
    if cache and "matrix" in cache:
        query_vec = vectorize_query(query, cache["vectorizer"])

    # 构建原 items 到 cache index 的映射
    item_index_map = {it["id"]: idx for idx, it in enumerate(items)}

    results = []
    for item in filtered:
        sem_score = 0
        idx = item_index_map.get(item["id"])
        if query_vec and cache and "matrix" in cache and idx is not None:
            doc_vec = cache["matrix"][idx]
            sem_score = cosine_similarity(query_vec, doc_vec)
        kw_score = keyword_score(query, item)
        quality_bonus = (item["quality"] - 3) * 0.05  # 质量分 3 为基准，±0.05

        # 混合分数：语义 0.5 + 关键词 0.3 + 质量分加成 0.2
        final_score = sem_score * 0.5 + min(kw_score * 0.05, 1.0) * 0.3 + (0.5 + quality_bonus) * 0.2

        results.append((final_score, item))

    if sort_by == "quality":
        results.sort(key=lambda x: (x[1]["quality"], x[0]), reverse=True)
    elif sort_by == "date":
        # 按 id 编号近似排序（编号越大越新）
        results.sort(key=lambda x: x[1]["id"], reverse=True)
    else:
        results.sort(key=lambda x: x[0], reverse=True)

    filter_desc = []
    if evtype:
        filter_desc.append(f"type={evtype}")
    if topic:
        filter_desc.append(f"topic={topic}")
    if scene:
        filter_desc.append(f"scene={scene}")
    if min_quality is not None:
        filter_desc.append(f"quality>={min_quality}")

    print(f"\n查询：{query}")
    if filter_desc:
        print(f"筛选条件：{' | '.join(filter_desc)}")
    print(f"共找到 {len(items)} 条论据，筛选后 {len(filtered)} 条，返回 TOP {top_n}:\n")
    print("-" * 60)

    for rank, (score, item) in enumerate(results[:top_n], 1):
        print(f"\n【{rank}】{item['id']}｜{item['type']}｜质量 {item['quality']} 分｜相关度 {score:.3f}")
        print(f"标题：{item['title']}")
        print(f"来源：{item['source']}")
        print(f"主题：{', '.join(item['topic']) or '无'}")
        print(f"场景：{', '.join(item['scene']) or '无'}")
        print(f"标签：{', '.join(item['tags']) or '无'}")
        print(f"路径：{item['path']}")
        body = extract_summary(item['body'])
        print(f"摘要：{body}")
        print("-" * 60)


def main():
    parser = argparse.ArgumentParser(description="论据库检索")
    parser.add_argument("query", help="查询主题")
    parser.add_argument("--top", type=int, default=5, help="返回结果数量")
    parser.add_argument("--rebuild", action="store_true", help="强制重建缓存")
    parser.add_argument("--vault", default=DEFAULT_VAULT, help="论据库路径")
    parser.add_argument("--type", choices=["概念", "数据", "案例", "金句"], help="按素材类型筛选")
    parser.add_argument("--topic", help="按主题领域筛选（如：主题/商业）")
    parser.add_argument("--scene", help="按应用场景筛选（如：场景/核心论据）")
    parser.add_argument("--min-quality", type=int, help="最低质量分")
    parser.add_argument("--sort", choices=["relevance", "quality", "date"], default="relevance", help="排序方式")
    args = parser.parse_args()

    search(
        args.query,
        args.vault,
        top_n=args.top,
        force=args.rebuild,
        evtype=args.type,
        topic=args.topic,
        scene=args.scene,
        min_quality=args.min_quality,
        sort_by=args.sort
    )


if __name__ == "__main__":
    main()
