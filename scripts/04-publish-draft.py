#!/usr/bin/env python3
"""
发布代理 — 排版 + 图片上传 + 推送草稿箱 + 数据归档
基于 wenyan-cli
"""

import json
import sys
import subprocess
import tempfile
from pathlib import Path

def archive_to_history(client_name, article_data):
    """归档到历史记录"""
    history_path = Path(__file__).parent.parent / "clients" / client_name / "history.yaml"
    
    import yaml
    history = []
    if history_path.exists():
        with open(history_path, "r", encoding="utf-8") as f:
            history = yaml.safe_load(f) or []
    
    history.append(article_data)
    
    with open(history_path, "w", encoding="utf-8") as f:
        yaml.dump(history, f, allow_unicode=True, default_flow_style=False)
    
    print(f"✅ 已归档到：{history_path}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="发布代理 - 排版 + 发布 + 归档")
    parser.add_argument("--article", required=True, help="文章路径")
    parser.add_argument("--cover", required=True, help="封面图路径")
    parser.add_argument("--theme", default="lapis", help="wenyan 主题（lapis/phycat等）")
    parser.add_argument("--client", required=True, help="客户名称")
    parser.add_argument("--title", required=True, help="文章标题")
    parser.add_argument("--highlight", default="solarized-light", help="代码高亮主题")
    
    args = parser.parse_args()
    
    print(f"📤 发布代理启动 · 客户={args.client} · 主题={args.theme}")
    
    # Step 1: 准备带 frontmatter 的临时 Markdown 文件
    article_path = Path(args.article)
    cover_path = Path(args.cover)
    
    # 读取原文
    with open(article_path, "r", encoding="utf-8") as f:
        original_content = f.read()
    
    # 添加 frontmatter
    frontmatter = f"""---
title: {args.title}
cover: {cover_path.absolute()}
---

"""
    temp_content = frontmatter + original_content
    
    # 写入临时文件（放在 output 目录，确保图片路径正确）
    temp_dir = Path(__file__).parent.parent / "output"
    temp_dir.mkdir(parents=True, exist_ok=True)
    temp_path = temp_dir / f"temp-{Path(article_path).stem}.md"
    with open(temp_path, "w", encoding="utf-8") as f:
        f.write(temp_content)
    
    print(f"✅ 临时文件：{temp_path}")
    
    # Step 2: 调用 wenyan-cli 发布
    print("Step 1: 推送草稿箱中...")
    try:
        result = subprocess.run(
            ["wenyan", "publish", "-f", temp_path, "-t", args.theme, "-h", args.highlight],
            capture_output=True,
            text=True,
            check=True
        )
        
        # 解析输出获取 media_id（wenyan-cli 输出 JSON）
        output = result.stdout.strip()
        try:
            publish_result = json.loads(output)
            media_id = publish_result.get("media_id", "")
        except json.JSONDecodeError:
            # 如果不是 JSON，直接用完整输出
            media_id = output[:100]
        
        print(f"✅ Media ID: {media_id}")
        print(f"✅ wenyan 输出: {output[:200]}...")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 发布失败：{e}")
        print(f"❌ stderr: {e.stderr}")
        media_id = ""
    finally:
        # 清理临时文件（可选，保留用于调试）
        # Path(temp_path).unlink(missing_ok=True)
        pass
    
    # Step 3: 归档
    print("Step 2: 数据归档中...")
    archive_data = {
        "date": Path(args.article).stem.split("-")[0],
        "title": args.title,
        "topic_source": "Z5-WeChat-SOP",
        "framework": "自动",
        "word_count": len(original_content),
        "media_id": media_id,
        "theme": args.theme,
        "stats": None
    }
    archive_to_history(args.client, archive_data)
    
    print(f"\n📄 发布代理完成")
    print(f"🔗 草稿箱：https://mp.weixin.qq.com")
    
    return {"status": "success", "media_id": media_id}

if __name__ == "__main__":
    main()
