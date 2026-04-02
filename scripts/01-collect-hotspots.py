#!/usr/bin/env python3
"""
体育旅游产业生态信息采集脚本 v2.2
- 集成热点抓取（微博/头条/百度）
- 全面关键词库搜索
- 去重、分类、质量评分
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

# 配置路径
CONFIG_DIR = Path.home() / ".sport-tourism-intelligence"
CONFIG_FILE = CONFIG_DIR / "config.json"
DATA_DIR = CONFIG_DIR / "data"
SKILL_DIR = Path(__file__).parent.parent

# 加载关键词库
def load_keywords_library():
    """加载全面关键词库"""
    keywords_file = SKILL_DIR / "references" / "keywords-library.json"
    if keywords_file.exists():
        try:
            return json.load(open(keywords_file, 'r', encoding='utf-8'))
        except Exception as e:
            print(f"[warn] 加载关键词库失败: {e}", file=sys.stderr)
    return None

KEYWORDS_LIBRARY = load_keywords_library()

# 9省配置
PROVINCES = {
    "海南": {"priority": 1, "keywords": ["海南体育旅游", "海南自贸港体育", "体旅融合示范省", "免税+体育", "海南户外运动", "海南潜水", "海南冲浪"]},
    "浙江": {"priority": 1, "keywords": ["浙江体育旅游", "浙江户外运动", "杭州亚运遗产", "莫干山户外", "浙江露营", "浙江徒步"]},
    "四川": {"priority": 1, "keywords": ["四川体育旅游", "四川登山徒步", "四姑娘山", "川西户外", "四川露营", "四川滑雪"]},
    "贵州": {"priority": 1, "keywords": ["贵州体育旅游", "贵州山地运动", "村超", "村BA", "遵义体育", "贵州露营"]},
    "云南": {"priority": 2, "keywords": ["云南体育旅游", "云南户外运动", "大理体育旅游", "香格里拉徒步", "云南露营", "云南登山"]},
    "广东": {"priority": 2, "keywords": ["广东体育旅游", "粤港澳大湾区体育", "广东体育科技", "深圳体育旅游", "广东露营", "广东水上运动"]},
    "江苏": {"priority": 2, "keywords": ["江苏体育旅游", "江苏体育制造", "南京体育旅游", "苏州体育旅游", "江苏露营", "江苏骑行"]},
    "山东": {"priority": 2, "keywords": ["山东体育旅游", "青岛帆船", "山东水上运动", "山东体育培训", "山东露营", "山东登山"]},
    "福建": {"priority": 2, "keywords": ["福建体育旅游", "福建海洋运动", "厦门体育旅游", "武夷山户外", "福建露营", "福建潜水"]},
}

# 体育旅游关键词过滤（从关键词库获取）
if KEYWORDS_LIBRARY:
    SPORT_TOURISM_KEYWORDS = KEYWORDS_LIBRARY["categories"]["core_industry"]["keywords"] + \
                               KEYWORDS_LIBRARY["categories"]["policy"]["keywords"] + \
                               KEYWORDS_LIBRARY["categories"]["sports_types"]["keywords"] + \
                               KEYWORDS_LIBRARY["categories"]["industry_elements"]["keywords"] + \
                               KEYWORDS_LIBRARY["categories"]["events"]["keywords"] + \
                               KEYWORDS_LIBRARY["categories"]["business"]["keywords"]
else:
    # 降级方案
    SPORT_TOURISM_KEYWORDS = [
        "体育旅游", "体旅融合", "户外运动", "体育公园", "户外营地",
        "马拉松", "滑雪", "登山", "徒步", "骑行", "露营",
        "赛事", "体育场馆", "全民健身", "体育培训", "体育设施",
        "村超", "村BA", "体育产业", "旅游+体育", "体育+旅游"
    ]

# HTTP 请求配置
TIMEOUT = 10
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
}


def ensure_dirs():
    """确保目录存在"""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_config():
    """加载配置"""
    if CONFIG_FILE.exists():
        return json.load(open(CONFIG_FILE))
    return {
        "provinces": list(PROVINCES.keys()),
        "priority": "high",
        "output_format": "markdown",
        "auto_report": True,
        "sources": ["hotspots", "websearch"]
    }


def fetch_weibo():
    """Fetch Weibo hot search."""
    if not HAS_REQUESTS:
        return []
    try:
        resp = requests.get(
            "https://weibo.com/ajax/side/hotSearch",
            headers={**HEADERS, "Referer": "https://weibo.com/"},
            timeout=TIMEOUT,
        )
        data = resp.json()
        items = []
        for entry in data.get("data", {}).get("realtime", []):
            note = entry.get("note", "")
            if not note:
                continue
            items.append({
                "title": note,
                "source": "微博",
                "hot": entry.get("num", 0),
                "url": f"https://s.weibo.com/weibo?q=%23{note}%23",
                "description": entry.get("label_name", ""),
            })
        return items
    except Exception as e:
        print(f"[warn] weibo failed: {e}", file=sys.stderr)
        return []


def fetch_toutiao():
    """Fetch Toutiao hot board."""
    if not HAS_REQUESTS:
        return []
    try:
        resp = requests.get(
            "https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc",
            headers=HEADERS,
            timeout=TIMEOUT,
        )
        data = resp.json()
        items = []
        for entry in data.get("data", []):
            title = entry.get("Title", "")
            if not title:
                continue
            items.append({
                "title": title,
                "source": "今日头条",
                "hot": int(entry.get("HotValue", 0) or 0),
                "url": entry.get("Url", ""),
                "description": "",
            })
        return items
    except Exception as e:
        print(f"[warn] toutiao failed: {e}", file=sys.stderr)
        return []


def fetch_baidu():
    """Fetch Baidu hot search."""
    if not HAS_REQUESTS:
        return []
    try:
        resp = requests.get(
            "https://top.baidu.com/api/board?platform=wise&tab=realtime",
            headers=HEADERS,
            timeout=TIMEOUT,
        )
        data = resp.json()
        items = []
        for card in data.get("data", {}).get("cards", []):
            top_content = card.get("content", [])
            if not top_content:
                continue
            entries = top_content[0].get("content", []) if isinstance(top_content[0], dict) else top_content
            for entry in entries:
                word = entry.get("word", "")
                if not word:
                    continue
                items.append({
                    "title": word,
                    "source": "百度",
                    "hot": int(entry.get("hotScore", 0) or 0),
                    "url": entry.get("url", ""),
                    "description": "",
                })
        return items
    except Exception as e:
        print(f"[warn] baidu failed: {e}", file=sys.stderr)
        return []


def filter_sport_tourism(items):
    """过滤体育旅游相关内容"""
    filtered = []
    for item in items:
        title = item.get("title", "").lower()
        desc = item.get("description", "").lower()
        text = title + " " + desc
        
        matched = []
        for keyword in SPORT_TOURISM_KEYWORDS:
            if keyword.lower() in text:
                matched.append(keyword)
        
        if matched:
            item["matched_keywords"] = matched
            item["source_type"] = "hotspot"
            item["category"] = "热点"
            filtered.append(item)
    
    return filtered


def deduplicate(items):
    """去重"""
    seen = set()
    result = []
    for item in items:
        key = item.get("title", "").strip()
        if key and key not in seen:
            seen.add(key)
            result.append(item)
    return result


def save_collection(data, filename=None):
    """保存采集结果"""
    if not filename:
        filename = f"collection_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    output_path = DATA_DIR / filename
    json.dump(data, open(output_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print(f"[✓] 采集结果已保存: {output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(description='体育旅游产业信息采集 v2.1')
    parser.add_argument('--province', '-p', help='指定省份采集')
    parser.add_argument('--category', '-c', help='采集类别: hotspots/websearch/all')
    parser.add_argument('--days', '-d', type=int, default=1, help='采集天数范围')
    parser.add_argument('--full', '-f', action='store_true', help='全量采集')
    parser.add_argument('--output', '-o', help='输出文件名')
    
    args = parser.parse_args()
    
    ensure_dirs()
    
    print("=" * 60)
    print("📥 Z5-WeChat-SOP 采集代理 v2.2")
    print("=" * 60)
    print(f"采集时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"采集范围: {args.days} 天")
    if args.province:
        print(f"指定省份: {args.province}")
    print("-" * 60)
    
    all_items = []
    sources_ok = []
    sources_fail = []
    
    # Step 1: 抓取多平台热点
    print("[*] 抓取微博热搜...")
    weibo_items = fetch_weibo()
    if weibo_items:
        print(f"[✓] 微博: {len(weibo_items)} 条")
        sources_ok.append("微博")
    else:
        print("[x] 微博抓取失败")
        sources_fail.append("微博")
    
    print("[*] 抓取今日头条热榜...")
    toutiao_items = fetch_toutiao()
    if toutiao_items:
        print(f"[✓] 今日头条: {len(toutiao_items)} 条")
        sources_ok.append("今日头条")
    else:
        print("[x] 今日头条抓取失败")
        sources_fail.append("今日头条")
    
    print("[*] 抓取百度热搜...")
    baidu_items = fetch_baidu()
    if baidu_items:
        print(f"[✓] 百度: {len(baidu_items)} 条")
        sources_ok.append("百度")
    else:
        print("[x] 百度抓取失败")
        sources_fail.append("百度")
    
    # 合并所有热点
    raw_hotspots = weibo_items + toutiao_items + baidu_items
    print(f"[*] 原始热点总数: {len(raw_hotspots)}")
    
    # 过滤体育旅游相关
    hotspot_items = filter_sport_tourism(raw_hotspots)
    print(f"[✓] 体育旅游相关热点: {len(hotspot_items)} 条")
    all_items.extend(hotspot_items)
    
    # Step 2: 生成 web 搜索查询词
    queries = []
    date_start = (datetime.now() - timedelta(days=args.days)).strftime("%Y-%m-%d")
    
    # 全国性关键词
    national_keywords = [
        "全国体育旅游", "体育旅游产业", "体育旅游政策", "体育旅游赛事",
        "体育旅游项目", "体育旅游路线", "体育旅游数据", "体育旅游报告",
        "体育旅游最新", "体旅融合最新", "户外运动最新", "体育赛事最新"
    ]
    
    for keyword in national_keywords:
        queries.append({
            "province": "全国",
            "keyword": keyword,
            "date_start": date_start,
            "priority": 1
        })
    
    # 省份关键词
    if args.province and args.province in PROVINCES:
        # 特定省份查询
        for keyword in PROVINCES[args.province]["keywords"]:
            queries.append({
                "province": args.province,
                "keyword": keyword,
                "date_start": date_start,
                "priority": PROVINCES[args.province]["priority"]
            })
    else:
        # 全量查询
        for prov, info in PROVINCES.items():
            for keyword in info["keywords"]:
                queries.append({
                    "province": prov,
                    "keyword": keyword,
                    "date_start": date_start,
                    "priority": info["priority"]
                })
    
    # 保存查询词
    queries_file = DATA_DIR / f"queries_{datetime.now().strftime('%Y%m%d')}.json"
    json.dump(queries, open(queries_file, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print(f"[✓] 搜索查询词已保存: {queries_file}")
    print(f"[*] 建议搜索关键词: {len(queries)} 个")
    if queries:
        print("-" * 40)
        for q in queries[:10]:
            print(f"  - {q['province']}: {q['keyword']}")
        if len(queries) > 10:
            print(f"  ... 还有 {len(queries) - 10} 个")
        print("-" * 40)
    
    # 去重、排序
    all_items = deduplicate(all_items)
    all_items.sort(key=lambda x: int(x.get("hot", 0) or 0), reverse=True)
    
    # Step 3: 生成选题
    topics = []
    
    # 基于热点生成选题
    if all_items:
        for i, item in enumerate(all_items[:10]):
            title = item.get("title", "")
            matched = item.get("matched_keywords", [])
            topic_title = f"{title}：从热点看体育旅游的机遇"
            topics.append({
                "id": i + 1,
                "title": topic_title,
                "score": 8.5 - i * 0.3,
                "seo_score": 7.0,
                "framework": "热点解读型",
                "keywords": matched,
                "source": item.get("source", ""),
                "hot": item.get("hot", 0)
            })
    
    # 补充默认选题
    default_topics = [
        {
            "id": len(topics) + 1,
            "title": "世界杯48队出炉！从体育赛事看体育旅游的全球化机遇",
            "score": 9.5,
            "seo_score": 8.5,
            "framework": "热点解读型",
            "keywords": ["世界杯", "体育旅游", "体旅融合"],
            "source": "系统推荐",
            "hot": 9999999
        },
        {
            "id": len(topics) + 2,
            "title": "村超村BA启示：草根赛事如何点燃城市体育旅游热情",
            "score": 9.0,
            "seo_score": 8.0,
            "framework": "案例解读型",
            "keywords": ["村超", "村BA", "体育旅游"],
            "source": "系统推荐",
            "hot": 8888888
        }
    ]
    topics.extend(default_topics)
    topics = topics[:20]
    
    print(f"[✓] 选题生成: {len(topics)} 个")
    
    # 整理最终结果
    tz = timezone(timedelta(hours=8))
    all_results = {
        "meta": {
            "collection_time": datetime.now(tz).isoformat(),
            "version": "2.2",
            "days": args.days,
            "province": args.province,
            "category": args.category,
            "sources_ok": sources_ok,
            "sources_fail": sources_fail
        },
        "summary": {
            "total_items": len(all_items),
            "hotspot_items": len(hotspot_items),
            "websearch_items": 0,
            "search_queries": len(queries),
            "topics_count": len(topics)
        },
        "data": all_items,
        "search_queries": queries,
        "topics": topics
    }
    
    # 保存结果
    output_file = save_collection(all_results, args.output)
    
    print("-" * 60)
    print(f"[✓] 采集完成!")
    print(f"输出文件: {output_file}")
    print(f"总条目: {len(all_items)}")
    print(f"热点来源: {len(hotspot_items)}")
    print(f"待搜索: {len(queries)} 个关键词")
    print("=" * 60)
    
    # 打印结果
    if all_items:
        print("\n[采集结果]")
        for i, item in enumerate(all_items[:10]):
            matched = ",".join(item.get("matched_keywords", []))
            print(f"{i+1}. [{item['source']}] {item['title'][:50]}... (匹配: {matched})")
    else:
        print("\n[!] 暂无体育旅游相关热点，建议使用搜索关键词手动搜索")
    
    # 打印选题
    if topics:
        print("\n[前5个选题]")
        for i, topic in enumerate(topics[:5]):
            title = topic.get('title', '')[:60]
            print(f"{i+1}. [{topic.get('score', 0)}分] {title}...")
    
    return all_results


if __name__ == "__main__":
    result = main()
    # 输出 JSON 供 main.py 调用
    import json
    print(json.dumps(result, ensure_ascii=False))
