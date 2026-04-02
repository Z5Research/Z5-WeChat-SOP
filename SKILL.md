# Z5-WeChat-SOP

**微信公众号内容生产标准作业流程**

---

## 🎯 一句话安装

复制以下指令，粘贴到 OpenClaw 或 AI Agent 中即可自动安装：

```
请安装 Z5-WeChat-SOP：微信公众号内容生产标准作业流程
开源地址：https://github.com/Z5Research/Z5-WeChat-SOP
文档：https://github.com/Z5Research/Z5-WeChat-SOP/blob/main/SKILL.md
自动化 · 标准化 · 可量化 · 持续进化
```

---

## 📖 简介

Z5-WeChat-SOP 是一套专为微信公众号内容生产设计的端到端自动化解决方案。

**设计理念**：源于媒体运营四部策略——选题策划 → 内容生产 → 质量审核 → 分发发布。Z5-SOP 将这四部策略全部自动化，AI 替代人工操作。

---

## ✨ 核心价值

| 价值 | 说明 |
|------|------|
| **效率提升 87.5%** | 单篇耗时从 4 小时降至 30 分钟 |
| **成本降低 100%** | 配图成本从 200 元/张降至 ≈0 元 |
| **质量标准化** | 3 层自动审核机制 |
| **持续进化** | Playbook 学习机制，越用越懂你的品牌 |

---

## 📊 工作流程

```
采集代理 → 编辑代理 → 审核代理 → 发布代理
   ↓           ↓           ↓          ↓
热点抓取     文章撰写     3 层审核    排版发布
(微博/头条/百度)  AI 配图     数据校验    草稿箱
选题生成     SEO 优化     来源核实    数据归档
关键词库      视觉 AI      合规检查    效果复盘
```

---

## 🚀 快速开始

### 全自动模式

```bash
python3 scripts/main.py --client 你的公众号名 --mode auto
```

### 交互模式

```bash
python3 scripts/main.py --client 你的公众号名 --mode interactive
```

### 分步执行

```bash
# Step 1: 采集热点
python3 scripts/01-collect-hotspots.py --limit 30

# Step 2: 撰写文章
python3 scripts/03-write-article.py --client 你的公众号名 --topic "选题"

# Step 3: 审核文章
python3 scripts/06-audit-article.py --client 你的公众号名

# Step 4: 发布草稿
python3 scripts/07-publish-draft.py --client 你的公众号名
```

---

## 📁 项目结构

```
Z5-WeChat-SOP/
├── scripts/           # 14个Python脚本
├── docs/             # 技术文档
├── cover.png         # 封面图
├── workflow.png      # 工作流程图
├── README.md          # 本文件
├── README_EN.md       # English
├── CHANGELOG.md      # 版本更新
└── requirements.txt # 依赖包
```

---

## 📄 许可证

MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

**让内容生产更简单，更高效，更可控。**
