#!/usr/bin/env python3
"""
SEO 优化 — 生成标题/摘要/标签
"""

import json
import yaml
from pathlib import Path
from datetime import datetime

def load_article(article_path):
    """加载文章内容"""
    with open(article_path, "r", encoding="utf-8") as f:
        return f.read()

def load_client_config(client_name):
    """加载客户配置"""
    config_path = Path(__file__).parent.parent / "clients" / client_name / "style.yaml"
    if not config_path.exists():
        return None
    
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def generate_seo(article_content, client_config):
    """
    生成 SEO 优化数据
    
    返回：
    - title: 标题（≤20 字）
    - digest: 摘要（≤54 字）
    - tags: 标签（5 个）
    - keywords: 关键词（3-5 个）
    """
    # TODO: 调用 LLM 生成 SEO 数据
    # 这里使用简化版本
    
    lines = article_content.strip().split("\n")
    title = lines[0].lstrip("# ").strip() if lines else "未命名文章"
    
    # 生成摘要（从正文前 200 字提取）
    body = "\n".join([l for l in lines if not l.startswith("#") and l.strip()])
    digest = body[:200].strip() + "..." if len(body) > 200 else body.strip()
    
    # 限制摘要长度（微信要求≤54 字）
    if len(digest) > 54:
        digest = digest[:53] + "…"
    
    # 生成标签（基于客户配置和文章关键词）
    topics = client_config.get("topics", []) if client_config else []
    tags = topics[:5] if topics else ["体育", "旅游", "产业", "政策", "案例"]
    
    # 提取关键词（简化：从标题提取）
    keywords = title.split()[:5] if " " in title else [title[:2], title[2:4], title[4:6]]
    
    return {
        "title": title[:20],
        "digest": digest,
        "tags": tags[:5],
        "keywords": keywords[:5],
        "word_count": len(body)
    }

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="SEO 优化 - 生成标题/摘要/标签")
    parser.add_argument("--article", required=True, help="文章路径")
    parser.add_argument("--client", required=True, help="客户名称")
    parser.add_argument("--output", default="seo.json", help="输出文件")
    
    args = parser.parse_args()
    
    print(f"🔍 SEO 优化启动 · 文章={args.article}")
    
    # Step 1: 加载文章
    print("Step 1: 加载文章中...")
    article_content = load_article(args.article)
    print(f"✅ 文章长度={len(article_content)} 字")
    
    # Step 2: 加载配置
    print("Step 2: 加载客户配置...")
    client_config = load_client_config(args.client)
    if client_config:
        print(f"✅ 客户={client_config.get('name')}")
    else:
        print("⚠️ 客户配置不存在，使用默认配置")
    
    # Step 3: 生成 SEO 数据
    print("Step 3: 生成 SEO 数据...")
    seo_data = generate_seo(article_content, client_config)
    print(f"✅ 标题={seo_data['title']}")
    print(f"✅ 摘要={seo_data['digest'][:30]}...")
    print(f"✅ 标签={', '.join(seo_data['tags'])}")
    print(f"✅ 字数={seo_data['word_count']}")
    
    # Step 4: 输出
    output = {
        "timestamp": datetime.now().isoformat(),
        "article": args.article,
        "client": args.client,
        "seo": seo_data
    }
    
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n📄 输出：{output_path}")
    
    return output

if __name__ == "__main__":
    main()
