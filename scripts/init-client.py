#!/usr/bin/env python3
"""
客户初始化向导 — 快速创建客户配置
"""

import yaml
from pathlib import Path
from datetime import datetime

def create_client_directory(client_name):
    """创建客户目录结构"""
    base_dir = Path(__file__).parent.parent / "clients" / client_name
    
    dirs = [
        base_dir,
        base_dir / "corpus",
        base_dir / "lessons",
        base_dir / "output"
    ]
    
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
    
    return base_dir

def create_style_yaml(client_name, config):
    """创建 style.yaml 配置文件"""
    style_path = Path(__file__).parent.parent / "clients" / client_name / "style.yaml"
    
    style_content = f"""# 客户配置 — {client_name}

name: "{config.get('name', client_name)}"
industry: "{config.get('industry', '未知')}"
target_audience: "{config.get('target_audience', '未知')}"

# 内容方向
topics:
"""
    
    for topic in config.get('topics', ['行业政策', '地方实践', '案例分析']):
        style_content += f"  - {topic}\n"
    
    style_content += f"""
# 写作风格
tone: "{config.get('tone', '专业、客观、有深度')}"
voice: "{config.get('voice', '第三方观察者视角')}"
word_count: "{config.get('word_count', '1500-3500')}"

# 内容风格（干货/故事/情绪/热点/测评）
content_style: "{config.get('content_style', '干货')}"

# 禁忌
blacklist:
  words: {config.get('blacklist_words', '["震惊", "必看", "不转不是中国人"]')}
  topics: {config.get('blacklist_topics', '["政治敏感", "宗教", "色情"]')}

# 参考账号风格
reference_accounts:
{chr(10).join(['  - "' + acc + '"' for acc in config.get('reference_accounts', ['参考账号 1', '参考账号 2'])])}

# 排版主题（可多选，用于 A/B 测试）
themes:
{chr(10).join(['  - ' + theme for theme in config.get('themes', ['professional-clean'])])}

# 封面
cover_style: "{config.get('cover_style', '专业简洁，信息图风格')}"

# 署名
author: "{config.get('author', client_name + '编辑部')}"

# 发布设置
publish:
  schedule: "{config.get('schedule', 'daily')}"      # 发布频率
  time: "{config.get('time', '16:00')}"              # 发布时间
  auto_publish: {str(config.get('auto_publish', False)).lower()}   # 是否自动发布
"""
    
    with open(style_path, "w", encoding="utf-8") as f:
        f.write(style_content)
    
    return str(style_path)

def create_history_yaml(client_name):
    """创建空的 history.yaml"""
    history_path = Path(__file__).parent.parent / "clients" / client_name / "history.yaml"
    
    with open(history_path, "w", encoding="utf-8") as f:
        f.write("# 发布历史记录\n# 格式：\n# - date: \"2026-03-29\"\n#   title: \"文章标题\"\n#   media_id: \"微信 Media ID\"\n#   stats: {read_count: 1000, share_count: 50}\n")
    
    return str(history_path)

def create_playbook_template(client_name):
    """创建 Playbook 模板"""
    playbook_path = Path(__file__).parent.parent / "clients" / client_name / "playbook.md"
    
    playbook_content = f"""# {client_name} Playbook

_风格指南 · {datetime.now().strftime("%Y-%m-%d")} 创建_

---

## 📋 客户定位

**行业**：待填写

**目标读者**：待填写

**内容方向**：
- 待填写

---

## ✍️ 写作风格

**语气**：待填写

**人称**：待填写

**字数范围**：1500-3500 字

**内容风格**：干货

---

## 📐 文章结构

**推荐结构**：
1. 导读/摘要（100-200 字）
2. 目录（清晰导航）
3. 正文（分章节，每章有小标题）
4. 实用信息
5. 结语（情感共鸣）
6. 信息来源

---

## 📝 用词偏好

*待积累修改记录后自动生成*

---

## ⛔ 禁忌清单

**禁忌词**：
- 震惊
- 必看
- 不转不是中国人

**禁忌话题**：
- 政治敏感
- 宗教
- 色情

---

## 🎨 视觉风格

**封面风格**：专业简洁，信息图风格

**排版主题**：professional-clean

**配图要求**：
- 封面：900x383 像素
- 信息图：1280x720 像素，漫画/插画风格
- 场景图：1280x720 像素，真实有代入感

---

## 📊 审核标准

**数据可查证率**：≥80%（A 级）

**来源权威性**：S+A 级≥50%

**内容审核**：标题准确、内容客观、逻辑清晰、合规

---

## 🔄 更新记录

**创建时间**：{datetime.now().strftime("%Y-%m-%d %H:%M")}

**最后更新**：待更新

**累计学习**：0 次修改记录

---

_本 Playbook 将随着使用自动更新
_"""
    
    with open(playbook_path, "w", encoding="utf-8") as f:
        f.write(playbook_content)
    
    return str(playbook_path)

def interactive_setup():
    """交互式配置向导"""
    print("=" * 60)
    print("🎯 Z5-WeChat-SOP 客户初始化向导")
    print("=" * 60)
    print()
    
    # 基本信息
    client_name = input("客户名称（英文或拼音，如 tlvhui）：").strip()
    if not client_name:
        print("❌ 客户名称不能为空")
        return None
    
    display_name = input(f"客户显示名称（默认{client_name}）：").strip() or client_name
    
    industry = input("行业（如 体育旅游）：").strip() or "未知"
    
    target_audience = input("目标读者（如 25-50 岁体育爱好者）：").strip() or "未知"
    
    # 内容方向
    print("\n内容方向（每行一个，回车结束）：")
    topics = []
    while True:
        topic = input("  - ").strip()
        if not topic:
            break
        topics.append(topic)
    
    if not topics:
        topics = ["行业政策", "地方实践", "案例分析"]
    
    # 写作风格
    print("\n写作风格：")
    tone = input("  语气（如 专业、客观、有深度）：").strip() or "专业、客观、有深度"
    voice = input("  人称（如 第三方观察者视角）：").strip() or "第三方观察者视角"
    word_count = input("  字数范围（如 1500-3500）：").strip() or "1500-3500"
    content_style = input("  内容风格（干货/故事/情绪/热点/测评）：").strip() or "干货"
    
    # 发布设置
    print("\n发布设置：")
    schedule = input("  发布频率（daily/weekly）：").strip() or "daily"
    time = input("  发布时间（如 16:00）：").strip() or "16:00"
    auto_publish = input("  自动发布（true/false，默认 false）：").strip().lower() or "false"
    
    config = {
        "name": display_name,
        "industry": industry,
        "target_audience": target_audience,
        "topics": topics,
        "tone": tone,
        "voice": voice,
        "word_count": word_count,
        "content_style": content_style,
        "schedule": schedule,
        "time": time,
        "auto_publish": auto_publish == "true"
    }
    
    return client_name, config

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="客户初始化向导 - 快速创建客户配置")
    parser.add_argument("--client", help="客户名称（不填则进入交互模式）")
    parser.add_argument("--name", help="客户显示名称")
    parser.add_argument("--industry", help="行业")
    parser.add_argument("--non-interactive", action="store_true", help="非交互模式，使用默认配置")
    
    args = parser.parse_args()
    
    # 交互模式或非交互模式
    if not args.client or not args.non_interactive:
        result = interactive_setup()
        if not result:
            return
        client_name, config = result
    else:
        client_name = args.client
        config = {
            "name": args.name or client_name,
            "industry": args.industry or "未知",
            "target_audience": "未知",
            "topics": ["行业政策", "地方实践", "案例分析"],
            "tone": "专业、客观、有深度",
            "voice": "第三方观察者视角",
            "word_count": "1500-3500",
            "content_style": "干货",
            "schedule": "daily",
            "time": "16:00",
            "auto_publish": False
        }
    
    print("\n" + "=" * 60)
    print(f"🚀 开始初始化客户：{client_name}")
    print("=" * 60)
    
    # Step 1: 创建目录结构
    print("\nStep 1: 创建目录结构...")
    base_dir = create_client_directory(client_name)
    print(f"✅ 目录：{base_dir}")
    print(f"   - corpus/   (历史文章语料)")
    print(f"   - lessons/  (修改记录)")
    print(f"   - output/   (输出文件)")
    
    # Step 2: 创建配置文件
    print("\nStep 2: 创建配置文件...")
    style_path = create_style_yaml(client_name, config)
    print(f"✅ style.yaml: {style_path}")
    
    # Step 3: 创建历史记录
    print("\nStep 3: 创建历史记录...")
    history_path = create_history_yaml(client_name)
    print(f"✅ history.yaml: {history_path}")
    
    # Step 4: 创建 Playbook
    print("\nStep 4: 创建 Playbook...")
    playbook_path = create_playbook_template(client_name)
    print(f"✅ playbook.md: {playbook_path}")
    
    # 完成
    print("\n" + "=" * 60)
    print("✅ 客户初始化完成！")
    print("=" * 60)
    print(f"""
📁 客户目录：{base_dir}
📄 配置文件：{style_path}

🎯 下一步：
1. 编辑 {style_path} 完善配置
2. 将历史文章放入 corpus/ 目录
3. 运行：python3 scripts/main.py --client {client_name} --mode auto

💡 提示：
- 积累 20 篇以上历史文章后，运行 python3 scripts/10-build-playbook.py --client {client_name} 自动生成 Playbook
- 每次人工修改后，运行 python3 scripts/09-learn-edits.py --client {client_name} --draft {client_name}/draft.md --final {client_name}/final.md 学习修改
""")
    
    return {"status": "success", "client": client_name, "directory": str(base_dir)}

if __name__ == "__main__":
    main()
