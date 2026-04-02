#!/usr/bin/env python3
"""
效果复盘 — 拉取文章数据 + 分析建议
"""

import json
import yaml
from pathlib import Path
from datetime import datetime, timedelta

def load_client_config(client_name):
    """加载客户配置"""
    config_path = Path(__file__).parent.parent / "clients" / client_name / "style.yaml"
    if not config_path.exists():
        return None
    
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_history(client_name):
    """加载历史记录"""
    history_path = Path(__file__).parent.parent / "clients" / client_name / "history.yaml"
    if not history_path.exists():
        return []
    
    with open(history_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or []

def fetch_wechat_stats(media_ids, days=7):
    """
    从微信后台拉取统计数据
    
    TODO: 集成微信 API
    当前返回模拟数据
    """
    stats = {}
    
    for media_id in media_ids:
        # 模拟数据
        stats[media_id] = {
            "read_count": 1000,
            "share_count": 50,
            "like_count": 80,
            "comment_count": 10,
            "completion_rate": 0.65,
            "fetch_time": datetime.now().isoformat()
        }
    
    return stats

def analyze_stats(history, stats):
    """分析数据并生成建议"""
    if not history:
        return {"error": "无历史数据"}
    
    # 阅读量 Top3
    articles_with_stats = []
    for article in history:
        media_id = article.get("media_id")
        if media_id and media_id in stats:
            article_stats = stats[media_id]
            articles_with_stats.append({
                **article,
                "stats": article_stats
            })
    
    # 按阅读量排序
    top_reads = sorted(
        articles_with_stats,
        key=lambda x: x["stats"]["read_count"],
        reverse=True
    )[:3]
    
    # 按分享率排序
    top_shares = sorted(
        articles_with_stats,
        key=lambda x: x["stats"]["share_count"] / max(x["stats"]["read_count"], 1),
        reverse=True
    )[:3]
    
    # 按完读率排序
    top_completion = sorted(
        articles_with_stats,
        key=lambda x: x["stats"]["completion_rate"],
        reverse=True
    )[:3]
    
    # 生成建议
    suggestions = []
    
    if top_reads:
        top_title = top_reads[0]["title"]
        suggestions.append(f"📈 阅读量最高：《{top_title}》- 可参考其选题方向")
    
    if top_shares:
        top_title = top_shares[0]["title"]
        suggestions.append(f"🔄 分享率最高：《{top_title}》- 可参考其内容结构")
    
    if top_completion:
        top_title = top_completion[0]["title"]
        suggestions.append(f"✅ 完读率最高：《{top_title}》- 可参考其叙事节奏")
    
    # 发布时段分析（简化）
    suggestions.append("⏰ 建议发布时段：16:00-17:00（根据历史数据）")
    
    # 选题方向建议
    topics = {}
    for article in articles_with_stats:
        topic = article.get("topic_source", "未知")
        if topic not in topics:
            topics[topic] = {"count": 0, "total_reads": 0}
        topics[topic]["count"] += 1
        topics[topic]["total_reads"] += article["stats"]["read_count"]
    
    if topics:
        best_topic = max(topics.items(), key=lambda x: x[1]["total_reads"])
        suggestions.append(f"🎯 最佳选题方向：{best_topic[0]}（平均阅读{best_topic[1]['total_reads']//best_topic[1]['count']}）")
    
    return {
        "total_articles": len(articles_with_stats),
        "top_reads": [{"title": a["title"], "reads": a["stats"]["read_count"]} for a in top_reads],
        "top_shares": [{"title": a["title"], "shares": a["stats"]["share_count"]} for a in top_shares],
        "top_completion": [{"title": a["title"], "rate": a["stats"]["completion_rate"]} for a in top_completion],
        "suggestions": suggestions
    }

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="效果复盘 - 拉取数据 + 分析建议")
    parser.add_argument("--client", required=True, help="客户名称")
    parser.add_argument("--days", type=int, default=7, help="统计天数")
    parser.add_argument("--output", default="stats.json", help="输出文件")
    
    args = parser.parse_args()
    
    print(f"📊 效果复盘启动 · 客户={args.client} · 统计={args.days} 天")
    
    # Step 1: 加载历史记录
    print("Step 1: 加载历史记录...")
    history = load_history(args.client)
    print(f"✅ 历史文章={len(history)} 篇")
    
    # Step 2: 提取 Media ID
    media_ids = [
        article.get("media_id")
        for article in history
        if article.get("media_id")
    ]
    print(f"✅ 有数据的文章={len(media_ids)} 篇")
    
    # Step 3: 拉取微信数据
    print("Step 2: 拉取微信数据...")
    stats = fetch_wechat_stats(media_ids, args.days)
    print(f"✅ 获取到={len(stats)} 篇文章数据")
    
    # Step 4: 分析数据
    print("Step 3: 分析数据...")
    analysis = analyze_stats(history, stats)
    
    if "error" in analysis:
        print(f"⚠️ {analysis['error']}")
    else:
        print(f"✅ 分析完成")
        print(f"\n📈 阅读量 Top3:")
        for i, item in enumerate(analysis["top_reads"], 1):
            print(f"  {i}. 《{item['title']}》- {item['reads']} 阅读")
        
        print(f"\n📊 建议:")
        for suggestion in analysis["suggestions"]:
            print(f"  {suggestion}")
    
    # Step 5: 更新历史记录
    print("\nStep 4: 更新历史记录...")
    for article in history:
        media_id = article.get("media_id")
        if media_id and media_id in stats:
            article["stats"] = stats[media_id]
            article["stats_updated"] = datetime.now().isoformat()
    
    # 保存更新后的历史
    history_path = Path(__file__).parent.parent / "clients" / args.client / "history.yaml"
    with open(history_path, "w", encoding="utf-8") as f:
        yaml.dump(history, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
    print(f"✅ 历史记录已更新")
    
    # Step 6: 输出报告
    output = {
        "timestamp": datetime.now().isoformat(),
        "client": args.client,
        "days": args.days,
        "total_articles": len(history),
        "articles_with_stats": len(media_ids),
        "analysis": analysis
    }
    
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n📄 输出：{output_path}")
    
    return output

if __name__ == "__main__":
    main()
