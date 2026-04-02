#!/usr/bin/env python3
"""
学习机制 — 分析人工修改 + 更新 Playbook
"""

import json
import yaml
import difflib
from pathlib import Path
from datetime import datetime

def load_client_config(client_name):
    """加载客户配置"""
    config_path = Path(__file__).parent.parent / "clients" / client_name / "style.yaml"
    if not config_path.exists():
        return None
    
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

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

def save_lesson(client_name, lesson_data):
    """保存修改记录"""
    lessons_dir = Path(__file__).parent.parent / "clients" / client_name / "lessons"
    lessons_dir.mkdir(parents=True, exist_ok=True)
    
    slug = lesson_data.get("slug", datetime.now().strftime("%Y%m%d-%H%M%S"))
    lesson_path = lessons_dir / f"{slug}-diff.yaml"
    
    with open(lesson_path, "w", encoding="utf-8") as f:
        yaml.dump(lesson_data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
    
    return str(lesson_path)

def analyze_diff(draft_path, final_path):
    """
    分析人工修改内容
    
    分析维度：
    - 用词替换
    - 段落删除
    - 段落新增
    - 结构调整
    - 标题修改
    - 语气调整
    """
    with open(draft_path, "r", encoding="utf-8") as f:
        draft_lines = f.readlines()
    
    with open(final_path, "r", encoding="utf-8") as f:
        final_lines = f.readlines()
    
    diff = list(difflib.unified_diff(
        draft_lines,
        final_lines,
        fromfile="draft",
        tofile="final",
        lineterm=""
    ))
    
    # 分类修改
    changes = {
        "word_replacements": [],  # 用词替换
        "deletions": [],          # 删除内容
        "additions": [],          # 新增内容
        "title_change": None,     # 标题修改
        "structure_changes": []   # 结构调整
    }
    
    draft_text = "".join(draft_lines)
    final_text = "".join(final_lines)
    
    # 检测标题变化
    draft_title = draft_lines[0].strip() if draft_lines else ""
    final_title = final_lines[0].strip() if final_lines else ""
    if draft_title != final_title:
        changes["title_change"] = {
            "from": draft_title,
            "to": final_title
        }
    
    # 分析 diff
    for line in diff[2:]:  # 跳过文件头
        if line.startswith("-") and not line.startswith("---"):
            changes["deletions"].append(line[1:].strip())
        elif line.startswith("+") and not line.startswith("+++"):
            changes["additions"].append(line[1:].strip())
    
    # 提取用词替换模式（简化：找短句替换）
    short_deletions = [d for d in changes["deletions"] if len(d) < 50 and d]
    short_additions = [a for a in changes["additions"] if len(a) < 50 and a]
    
    # 简单匹配替换对
    for i, del_text in enumerate(short_deletions):
        if i < len(short_additions):
            changes["word_replacements"].append({
                "from": del_text,
                "to": short_additions[i]
            })
    
    return {
        "draft_path": str(draft_path),
        "final_path": str(final_path),
        "draft_word_count": len(draft_text),
        "final_word_count": len(final_text),
        "changes": changes
    }

def summarize_patterns(lessons):
    """
    从历史修改中总结模式
    
    找出反复出现的 pattern（≥2 次）
    """
    if not lessons:
        return {}
    
    # 统计用词替换频率
    replacement_counts = {}
    for lesson in lessons:
        changes = lesson.get("changes", {})
        for replacement in changes.get("word_replacements", []):
            key = f"{replacement.get('from', '')} → {replacement.get('to', '')}"
            replacement_counts[key] = replacement_counts.get(key, 0) + 1
    
    # 找出高频模式（≥2 次）
    patterns = {
        "word_replacements": [
            {"pattern": k, "count": v}
            for k, v in replacement_counts.items()
            if v >= 2
        ],
        "total_lessons": len(lessons)
    }
    
    return patterns

def update_playbook(client_name, patterns):
    """
    更新 Playbook
    
    将高频模式固化到 playbook.md
    """
    playbook_path = Path(__file__).parent.parent / "clients" / client_name / "playbook.md"
    
    # 如果 playbook 不存在，创建基础版本
    if not playbook_path.exists():
        playbook_content = f"""# {client_name} Playbook

_基于历史修改记录自动生成 · {datetime.now().strftime("%Y-%m-%d")}

## 用词偏好

"""
        for pattern in patterns.get("word_replacements", []):
            playbook_content += f"- {pattern['pattern']}（出现{pattern['count']}次）\n"
        
        playbook_content += f"""

## 写作风格

（待补充）

## 禁忌

（待补充）

---

_最后更新：{datetime.now().strftime("%Y-%m-%d %H:%M")}
_"""
    else:
        # 更新现有 playbook
        with open(playbook_path, "r", encoding="utf-8") as f:
            playbook_content = f.read()
        
        # 添加新的模式（如果存在）
        if patterns.get("word_replacements"):
            new_section = "\n## 新增用词偏好（本次更新）\n\n"
            for pattern in patterns["word_replacements"]:
                new_section += f"- {pattern['pattern']}（出现{pattern['count']}次）\n"
            
            playbook_content += new_section
            playbook_content += f"\n_最后更新：{datetime.now().strftime("%Y-%m-%d %H:%M")}_"
    
    playbook_path.parent.mkdir(parents=True, exist_ok=True)
    with open(playbook_path, "w", encoding="utf-8") as f:
        f.write(playbook_content)
    
    return str(playbook_path)

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="学习机制 - 分析人工修改 + 更新 Playbook")
    parser.add_argument("--client", required=True, help="客户名称")
    parser.add_argument("--draft", help="修改前草稿路径")
    parser.add_argument("--final", help="修改后终稿路径")
    parser.add_argument("--slug", help="文章标识（用于命名）")
    parser.add_argument("--summarize", action="store_true", help="总结历史模式并更新 Playbook")
    
    args = parser.parse_args()
    
    print(f"🧠 学习机制启动 · 客户={args.client}")
    
    # 模式 1: 学习单次修改
    if args.draft and args.final:
        print("\n📝 模式 1: 学习单次修改")
        print(f"  草稿：{args.draft}")
        print(f"  终稿：{args.final}")
        
        # 分析修改
        print("\nStep 1: 分析修改内容...")
        diff_result = analyze_diff(args.draft, args.final)
        
        print(f"✅ 草稿字数={diff_result['draft_word_count']}")
        print(f"✅ 终稿字数={diff_result['final_word_count']}")
        print(f"✅ 用词替换={len(diff_result['changes']['word_replacements'])} 处")
        print(f"✅ 删除内容={len(diff_result['changes']['deletions'])} 处")
        print(f"✅ 新增内容={len(diff_result['changes']['additions'])} 处")
        
        if diff_result['changes'].get('title_change'):
            tc = diff_result['changes']['title_change']
            print(f"✅ 标题修改：{tc['from']} → {tc['to']}")
        
        # 保存学习记录
        print("\nStep 2: 保存学习记录...")
        lesson_data = {
            "timestamp": datetime.now().isoformat(),
            "client": args.client,
            "slug": args.slug or datetime.now().strftime("%Y%m%d-%H%M%S"),
            **diff_result
        }
        lesson_path = save_lesson(args.client, lesson_data)
        print(f"✅ 已保存：{lesson_path}")
        
        # 加载历史修改记录
        lessons = load_lessons(args.client)
        print(f"\n📚 当前学习记录={len(lessons)} 次")
        
        # 检查是否需要更新 Playbook（每 5 次）
        if len(lessons) % 5 == 0 and len(lessons) > 0:
            print(f"\n🎯 已达到{len(lessons)}次修改，建议更新 Playbook")
            print("运行：python3 scripts/09-learn-edits.py --client {客户} --summarize")
    
    # 模式 2: 总结历史模式并更新 Playbook
    elif args.summarize:
        print("\n📊 模式 2: 总结历史模式")
        
        # 加载历史修改记录
        print("Step 1: 加载历史修改记录...")
        lessons = load_lessons(args.client)
        print(f"✅ 历史修改={len(lessons)} 次")
        
        if not lessons:
            print("⚠️ 无历史修改记录")
            return
        
        # 总结模式
        print("Step 2: 总结模式...")
        patterns = summarize_patterns(lessons)
        print(f"✅ 高频用词替换={len(patterns.get('word_replacements', []))} 个")
        
        # 更新 Playbook
        print("Step 3: 更新 Playbook...")
        playbook_path = update_playbook(args.client, patterns)
        print(f"✅ Playbook 已更新：{playbook_path}")
        
        print(f"\n📄 学习机制完成")
        print(f"💡 下次写作时将参考 Playbook 中的偏好")
    
    else:
        print("⚠️ 请指定 --draft 和 --final，或 --summarize")
        parser.print_help()
    
    return {"status": "success"}

if __name__ == "__main__":
    main()
