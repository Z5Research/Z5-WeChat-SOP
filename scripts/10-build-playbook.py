#!/usr/bin/env python3
"""
Playbook 生成器 — 基于历史文章自动生成风格指南
"""

import yaml
import json
from pathlib import Path
from datetime import datetime
from collections import Counter

def load_client_config(client_name):
    """加载客户配置"""
    config_path = Path(__file__).parent.parent / "clients" / client_name / "style.yaml"
    if not config_path.exists():
        return None
    
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_corpus(client_name):
    """加载历史文章语料"""
    corpus_dir = Path(__file__).parent.parent / "clients" / client_name / "corpus"
    if not corpus_dir.exists():
        return []
    
    articles = []
    for article_file in corpus_dir.glob("*.md"):
        with open(article_file, "r", encoding="utf-8") as f:
            articles.append({
                "file": str(article_file),
                "content": f.read()
            })
    
    return articles

def load_lessons(client_name):
    """加载历史修改记录"""
    lessons_dir = Path(__file__).parent.parent / "clients" / client_name / "lessons"
    if not lessons_dir.exists():
        return []
    
    lessons = []
    for lesson_file in lessons_dir.glob("*.yaml"):
        with open(lesson_file, "r", encoding="utf-8") as f:
            lessons.append(yaml.safe_load(f))
    
    return lessons

def analyze_word_frequency(articles):
    """分析高频用词"""
    word_counts = Counter()
    
    for article in articles:
        content = article["content"]
        # 简单分词（中文按字符）
        words = content.split()
        word_counts.update(words)
    
    # 返回 Top 20
    return word_counts.most_common(20)

def analyze_structure(articles):
    """分析文章结构"""
    structures = []
    
    for article in articles:
        content = article["content"]
        lines = content.split("\n")
        
        # 提取标题层级
        h1 = [l for l in lines if l.startswith("# ")]
        h2 = [l for l in lines if l.startswith("## ")]
        h3 = [l for l in lines if l.startswith("### ")]
        
        structures.append({
            "h1_count": len(h1),
            "h2_count": len(h2),
            "h3_count": len(h3),
            "total_lines": len(lines)
        })
    
    # 计算平均值
    avg_h2 = sum(s["h2_count"] for s in structures) / len(structures) if structures else 0
    avg_h3 = sum(s["h3_count"] for s in structures) / len(structures) if structures else 0
    
    return {
        "avg_h2_sections": round(avg_h2, 1),
        "avg_h3_subsections": round(avg_h3, 1)
    }

def summarize_lessons(lessons):
    """总结修改记录中的模式"""
    if not lessons:
        return {}
    
    # 统计用词替换
    replacements = []
    for lesson in lessons:
        changes = lesson.get("changes", {})
        replacements.extend(changes.get("word_replacements", []))
    
    # 统计频率
    replacement_counts = Counter()
    for r in replacements:
        key = f"{r.get('from', '')} → {r.get('to', '')}"
        replacement_counts[key] += 1
    
    # 返回高频模式（≥2 次）
    return {
        "word_replacements": [
            {"pattern": k, "count": v}
            for k, v in replacement_counts.most_common(10)
            if v >= 2
        ],
        "total_lessons": len(lessons)
    }

def generate_playbook(client_name, corpus, lessons):
    """生成 Playbook"""
    config = load_client_config(client_name)
    
    # 分析语料
    word_freq = analyze_word_frequency(corpus) if corpus else []
    structure = analyze_structure(corpus) if corpus else {}
    
    # 分析修改记录
    lessons_summary = summarize_lessons(lessons)
    
    # 生成 Playbook 内容
    playbook = f"""# {client_name} Playbook

_自动生成 · {datetime.now().strftime("%Y-%m-%d")} · 基于{len(corpus)}篇文章 + {len(lessons)}次修改记录_

---

## 📋 客户定位

**行业**：{config.get('industry', '未知') if config else '未知'}

**目标读者**：{config.get('target_audience', '未知') if config else '未知'}

**内容方向**：
"""
    
    if config and config.get('topics'):
        for topic in config['topics']:
            playbook += f"- {topic}\n"
    
    playbook += f"""
---

## ✍️ 写作风格

**语气**：{config.get('tone', '未知') if config else '未知'}

**人称**：{config.get('voice', '未知') if config else '未知'}

**字数范围**：{config.get('word_count', '1500-3500') if config else '1500-3500'}

**内容风格**：{config.get('content_style', '干货') if config else '干货'}

---

## 📐 文章结构

"""
    
    if structure:
        playbook += f"""**平均章节数**：{structure.get('avg_h2_sections', 'N/A')} 个 H2 章节

**平均小节数**：{structure.get('avg_h3_subsections', 'N/A')} 个 H3 小节

"""
    
    playbook += """**推荐结构**：
1. 导读/摘要（100-200 字）
2. 目录（清晰导航）
3. 正文（分章节，每章有小标题）
4. 实用信息（交通、住宿、消费预算等）
5. 结语（情感共鸣）
6. 信息来源（标注数据来源）

---

## 📝 用词偏好

"""
    
    if lessons_summary.get('word_replacements'):
        playbook += "**高频修改模式**（人工修改习惯）：\n\n"
        for pattern in lessons_summary['word_replacements']:
            playbook += f"- {pattern['pattern']}（{pattern['count']}次）\n"
    else:
        playbook += "*暂无数据（积累 5 次以上修改记录后自动生成）*\n"
    
    playbook += f"""
---

## ⛔ 禁忌清单

**禁忌词**：
"""
    
    if config and config.get('blacklist', {}).get('words'):
        for word in config['blacklist']['words']:
            playbook += f"- {word}\n"
    else:
        playbook += "- （暂无）\n"
    
    playbook += """
**禁忌话题**：
"""
    
    if config and config.get('blacklist', {}).get('topics'):
        for topic in config['blacklist']['topics']:
            playbook += f"- {topic}\n"
    else:
        playbook += "- （暂无）\n"
    
    playbook += f"""
---

## 🎨 视觉风格

**封面风格**：{config.get('cover_style', '专业简洁') if config else '专业简洁'}

**排版主题**：{', '.join(config.get('themes', ['professional-clean'])) if config and config.get('themes') else 'professional-clean'}

**配图要求**：
- 封面：900x383 像素，专业简洁
- 信息图：1280x720 像素，漫画/插画风格
- 场景图：1280x720 像素，真实有代入感

---

## 📊 审核标准

**数据可查证率**：≥80%（A 级）

**来源权威性**：S+A 级≥50%

**内容审核**：标题准确、内容客观、逻辑清晰、合规

---

## 🔄 更新记录

"""
    
    if lessons:
        latest_lesson = max(lessons, key=lambda x: x.get('timestamp', ''))
        playbook += f"**最后学习**：{latest_lesson.get('timestamp', '未知')[:10]}\n\n"
        playbook += f"**累计学习**：{len(lessons)} 次修改记录\n"
    else:
        playbook += "*暂无学习记录*\n"
    
    playbook += f"""
**下次更新**：积累到{5 - (len(lessons) % 5)}次新修改后自动更新

---

_本 Playbook 由 Z5-WeChat-SOP 自动生成
最后更新：{datetime.now().strftime("%Y-%m-%d %H:%M")}
_"""
    
    return playbook

def save_playbook(client_name, playbook_content):
    """保存 Playbook"""
    playbook_path = Path(__file__).parent.parent / "clients" / client_name / "playbook.md"
    playbook_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(playbook_path, "w", encoding="utf-8") as f:
        f.write(playbook_content)
    
    return str(playbook_path)

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Playbook 生成器 - 基于历史文章自动生成风格指南")
    parser.add_argument("--client", required=True, help="客户名称")
    parser.add_argument("--output", help="输出文件路径（默认保存到 clients/{客户}/playbook.md）")
    
    args = parser.parse_args()
    
    print(f"📚 Playbook 生成器启动 · 客户={args.client}")
    
    # Step 1: 加载语料
    print("Step 1: 加载历史文章语料...")
    corpus = load_corpus(args.client)
    print(f"✅ 加载到 {len(corpus)} 篇文章")
    
    if len(corpus) < 5:
        print(f"⚠️ 建议至少 20 篇文章，当前{len(corpus)}篇，生成效果可能不佳")
    
    # Step 2: 加载修改记录
    print("Step 2: 加载历史修改记录...")
    lessons = load_lessons(args.client)
    print(f"✅ 加载到 {len(lessons)} 次修改记录")
    
    # Step 3: 生成 Playbook
    print("Step 3: 生成 Playbook...")
    playbook_content = generate_playbook(args.client, corpus, lessons)
    
    # Step 4: 保存
    print("Step 4: 保存 Playbook...")
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(playbook_content)
        playbook_path = str(output_path)
    else:
        playbook_path = save_playbook(args.client, playbook_content)
    
    print(f"✅ Playbook 已保存：{playbook_path}")
    
    print(f"\n📄 Playbook 生成完成")
    print(f"💡 下次写作时将自动参考此 Playbook")
    
    return {"status": "success", "playbook_path": playbook_path}

if __name__ == "__main__":
    main()
