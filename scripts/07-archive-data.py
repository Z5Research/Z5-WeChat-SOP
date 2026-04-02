#!/usr/bin/env python3
"""
数据归档 — 写入历史记录 + 备份
"""

import json
import yaml
import shutil
from pathlib import Path
from datetime import datetime

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

def save_history(client_name, history):
    """保存历史记录"""
    history_path = Path(__file__).parent.parent / "clients" / client_name / "history.yaml"
    history_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(history_path, "w", encoding="utf-8") as f:
        yaml.dump(history, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

def archive_article(client_name, article_data):
    """归档文章数据"""
    history = load_history(client_name)
    
    # 添加新记录
    history.append(article_data)
    
    # 保存
    save_history(client_name, history)
    
    return len(history)

def backup_archive(client_name, backup_dir):
    """备份归档数据"""
    backup_path = Path(backup_dir) / f"{client_name}-backup-{datetime.now().strftime('%Y%m%d-%H%M%S')}.yaml"
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    
    history_path = Path(__file__).parent.parent / "clients" / client_name / "history.yaml"
    if history_path.exists():
        shutil.copy2(history_path, backup_path)
        return str(backup_path)
    return None

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="数据归档 - 写入历史记录 + 备份")
    parser.add_argument("--client", required=True, help="客户名称")
    parser.add_argument("--article", required=True, help="文章路径")
    parser.add_argument("--title", required=True, help="文章标题")
    parser.add_argument("--topic", default="", help="选题来源")
    parser.add_argument("--framework", default="自动", help="写作框架")
    parser.add_argument("--media-id", default="", help="微信 Media ID")
    parser.add_argument("--theme", default="professional-clean", help="排版主题")
    parser.add_argument("--backup", action="store_true", help="同时备份")
    parser.add_argument("--backup-dir", default="backups", help="备份目录")
    
    args = parser.parse_args()
    
    print(f"📚 数据归档启动 · 客户={args.client}")
    
    # Step 1: 准备归档数据
    print("Step 1: 准备归档数据...")
    article_path = Path(args.article)
    
    # 计算字数
    with open(article_path, "r", encoding="utf-8") as f:
        content = f.read()
        body = "\n".join([l for l in content.split("\n") if not l.startswith("#") and l.strip()])
        word_count = len(body)
    
    archive_data = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "timestamp": datetime.now().isoformat(),
        "title": args.title,
        "article_file": str(article_path),
        "topic_source": args.topic,
        "framework": args.framework,
        "word_count": word_count,
        "media_id": args.media_id,
        "theme": args.theme,
        "status": "published" if args.media_id else "draft",
        "stats": None  # 后续更新
    }
    
    print(f"✅ 标题={args.title}")
    print(f"✅ 字数={word_count}")
    print(f"✅ 状态={archive_data['status']}")
    
    # Step 2: 写入历史记录
    print("Step 2: 写入历史记录...")
    total_count = archive_article(args.client, archive_data)
    print(f"✅ 已归档 · 历史文章总数={total_count}")
    
    # Step 3: 备份（可选）
    if args.backup:
        print("Step 3: 备份归档数据...")
        backup_path = backup_archive(args.client, args.backup_dir)
        if backup_path:
            print(f"✅ 备份：{backup_path}")
        else:
            print("⚠️ 无历史数据可备份")
    
    # Step 4: 输出归档数据
    output = {
        "timestamp": datetime.now().isoformat(),
        "client": args.client,
        "archive": archive_data,
        "history_count": total_count
    }
    
    print(f"\n📄 数据归档完成")
    
    return output

if __name__ == "__main__":
    main()
