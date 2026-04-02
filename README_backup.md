# Z5-WeChat-SOP

**微信公众号内容生产标准作业流程**

自动化 · 标准化 · 可量化 · 持续进化

[![Version](https://img.shields.io/badge/version-v1.1.0-blue.svg)](https://github.com/Z5Research/Z5-WeChat-SOP)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Stars](https://img.shields.io/github/stars/Z5Research/Z5-WeChat-SOP?style=flat)](https://github.com/Z5Research/Z5-WeChat-SOP/stargazers)

---

## 🎯 一句话安装

在 OpenClaw 或 Agent 环境中粘贴以下指令即可安装：

```
请安装 Z5-WeChat-SOP 技能：微信公众号内容生产标准作业流程
```

或手动安装：
```bash
# 克隆仓库
git clone https://github.com/Z5Research/Z5-WeChat-SOP.git

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
export WECHAT_APP_ID=your_app_id
export WECHAT_APP_SECRET=your_app_secret
export VOLC_ACCESS_KEY=your_volc_key
export VOLC_SECRET_KEY=your_volc_secret
```

---

## 📖 简介

Z5-WeChat-SOP 是一套专为微信公众号内容生产设计的端到端自动化解决方案。通过「采集 → 编辑 → 审核 → 发布」四步标准化流程，实现内容生产的自动化、规模化、可复现化。

**设计理念**：
> 源于媒体运营四部策略：选题策划 → 内容生产 → 质量审核 → 分发发布。Z5-SOP 将这四部策略全部自动化，AI 替代人工操作，让内容生产高效且标准化。

---

## ✨ 核心特性

| 特性 | 说明 |
|------|------|
| **4 步标准化流程** | 采集代理 → 编辑代理 → 审核代理 → 发布代理 |
| **3 层审核机制** | 数据校验 / 来源核实 / 合规检查 |
| **AI 配图** | 火山引擎 doubao-seedream + 提示词工程师3轮法 |
| **持续进化** | Playbook 学习机制，越用越懂你的品牌 |
| **零依赖** | 自包含完整技能，不依赖外部技能 |

---

## 📊 工作流程

```
┌─────────────────────────────────────────────────────────────────┐
│                    Z5-WeChat-SOP 工作流程                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐  │
│  │ 采集代理  │ → │ 编辑代理  │ → │ 审核代理  │ → │ 发布代理  │  │
│  │          │    │          │    │          │    │          │  │
│  │ 热点抓取  │    │ 文章撰写  │    │ 数据校验  │    │ 排版优化  │  │
│  │ 选题生成  │    │ AI 配图  │    │ 来源核实  │    │ 草稿推送  │  │
│  │ 关键词库  │    │ SEO 优化  │    │ 合规检查  │    │ 数据归档  │  │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘  │
│                                                                 │
│  微博热搜      AI 写作      S/A/B/C       wenyan-cli  │
│  头条热榜  →   框架模板  →   三层审核  →   草稿箱      │
│  百度热搜      专业配图      合规安全      自动归档      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 快速开始

### 方式 1：全自动模式

```bash
python3 scripts/main.py --client 你的公众号名 --mode auto
```

### 方式 2：交互模式

```bash
python3 scripts/main.py --client 你的公众号名 --mode interactive
```

### 方式 3：分步执行

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
├── scripts/
│   ├── 01-collect-hotspots.py    # 热点采集
│   ├── 02-write-article.py      # 文章撰写
│   ├── 03-audit-article.py     # 内容审核
│   ├── 04-publish-draft.py     # 草稿发布
│   ├── 05-seo-optimize.py       # SEO 优化
│   ├── 06-generate-images.py    # AI 配图
│   ├── 07-archive-data.py      # 数据归档
│   ├── 08-fetch-stats.py        # 数据拉取
│   └── 09-learn-edits.py       # 人工修改学习
├── docs/
│   └── SPEC.md                 # 技术规范文档
├── clients/                     # 客户配置目录
├── README.md
├── LICENSE
├── CHANGELOG.md
├── requirements.txt
└── workflow.png               # 工作流程图
```

---

## 🎨 核心功能

### 提示词工程师3轮法

每张配图必须经过：

1. **理解（Read & Analyze）** - 识别核心信息，确定配图类型
2. **提炼（Extract & Refine）** - 提取关键词，转化为视觉元素
3. **优化（Optimize & Generate）** - 组合完整提示词，规避审核敏感词

### 3 层审核机制

| 审核维度 | 评级 | 说明 |
|---------|------|------|
| **数据校验** | S/A/B/C | 核心数据必须 S/A 级才可发布 |
| **来源核实** | S/A/B/C | 官方/权威/主流/一般 四级 |
| **合规检查** | 通过/不通过 | 标题/客观性/逻辑/法规 |

---

## 📊 效率提升

| 维度 | 传统方式 | Z5-SOP | 提升 |
|------|---------|--------|------|
| 单篇耗时 | 4 小时 | 30 分钟 | **-87.5%** |
| 配图成本 | 200 元/张 | ≈0 元 | **-100%** |
| 发布频率 | 不定期 | 每日稳定 | **可控** |
| 数据校验 | 人工核对 | 3层自动审核 | **标准化** |

---

## ⚙️ 配置

### 环境变量

```bash
# 微信公众号
export WECHAT_APP_ID=your_app_id
export WECHAT_APP_SECRET=your_app_secret

# 火山引擎（配图生成）
export VOLC_ACCESS_KEY=your_access_key
export VOLC_SECRET_KEY=your_secret_key

# 阿里云百炼（备选配图）
export BAILIAN_API_KEY=your_api_key
```

### 客户配置

```yaml
# clients/你的公众号名/style.yaml
name: "你的公众号名"
industry: "行业"
topics:
  - "内容方向 1"
  - "内容方向 2"
tone: "写作风格"
cover_style: "封面风格描述"
author: "署名"
theme: "professional-clean"
```

---

## 📖 文档

- [完整规范文档](docs/SPEC.md) - 详细 SOP 流程说明
- [版本更新日志](CHANGELOG.md) - 版本迭代记录

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

**让内容生产更简单，更高效，更可控。**
