# Z5-WeChat-SOP

**微信公众号内容生产标准作业流程**

A standardized workflow for automated WeChat Official Account content production.

[![Version](https://img.shields.io/badge/version-4.3.0-blue.svg)](https://github.com/Z5Research/Z5-WeChat-SOP)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 🎯 简介

Z5-WeChat-SOP 是一套专为微信公众号内容生产设计的端到端自动化解决方案。通过「采集 → 编辑 → 审核 → 发布」四步标准化流程，实现内容生产的自动化、规模化、可复现化。

**适用场景**：
- 媒体公司每日内容生产
- 企业官方号运营
- 内容代理机构多客户管理
- 自媒体创作者一人内容团队

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

## 📋 工作流程

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  采集代理   │ → │  编辑代理   │ → │  审核代理   │ → │  发布代理   │
│             │    │             │    │             │    │             │
│ 热点抓取    │    │ 文章撰写    │    │ 数据校验    │    │ 排版优化    │
│ 选题生成    │    │ AI 配图    │    │ 来源核实    │    │ 草稿推送    │
│ 关键词库    │    │ SEO 优化    │    │ 合规检查    │    │ 数据归档    │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

### Step 1：采集代理

- 多平台热点抓取（微博热搜 / 头条热榜 / 百度热搜）
- 关键词库扩展搜索（支持行业关键词定制）
- AI 选题生成（S/A/B/C 四级评分）

### Step 2：编辑代理

- 5 种框架模板（痛点型 / 故事型 / 清单型 / 对比型 / 热点解读型）
- AI 文章撰写（1500-3500 字）
- 专业配图生成（封面 × 1 + 信息图 × 2）
- SEO 优化（标题 / 摘要 / 标签）

### Step 3：审核代理

| 审核维度 | 评级标准 |
|---------|---------|
| **数据校验** | S(100%) / A(≥80%) / B(≥60%) / C(<60%) |
| **来源核实** | S(官方) / A(权威媒体) / B(一般媒体) / C(不可靠) |
| **合规检查** | 标题 / 客观性 / 逻辑 / 法规四维审核 |

### Step 4：发布代理

- 多主题排版（专业简洁 / 科技风 / 暖色编辑 / 极简黑白）
- 永久素材库管理
- 草稿箱推送
- 发布数据归档

---

## 🚀 快速开始

### 方式 1：全自动模式

```bash
# 一句话启动全流程
python3 scripts/main.py --client 你的公众号名 --mode auto
```

### 方式 2：交互模式

```bash
# 在关键节点暂停确认
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
z5-wechat-sop/
├── scripts/
│   ├── 01-collect-hotspots.py    # 热点采集
│   ├── 02-generate-topics.py      # 选题生成
│   ├── 03-write-article.py       # 文章撰写
│   ├── 04-generate-images.py      # 配图生成
│   ├── 05-seo-optimize.py        # SEO 优化
│   ├── 06-audit-article.py        # 内容审核
│   └── 07-publish-draft.py        # 草稿发布
├── clients/
│   └── demo/                     # 示例客户配置
├── docs/
│   └── SPEC.md                   # 详细规范文档
├── README.md
├── LICENSE
└── requirements.txt
```

---

## ⚙️ 配置

### 客户配置示例

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
```

### 提示词工程师3轮法

每张配图必须经过：

1. **理解** - 识别核心信息，确定配图类型
2. **提炼** - 提取关键词，转化为视觉元素
3. **优化** - 组合完整提示词，规避审核敏感词

---

## 📊 效率提升

| 维度 | 传统方式 | Z5-SOP | 提升 |
|------|---------|--------|------|
| 单篇耗时 | 4 小时 | 30 分钟 | **-87.5%** |
| 配图成本 | 200 元/张 | ≈0 元 | **-100%** |
| 发布频率 | 不定期 | 每日稳定 | **可控** |
| 数据校验 | 人工核对 | 3层自动审核 | **标准化** |

---

## 🔧 API 配置

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

## 🔗 相关链接

- [GitHub Issues](https://github.com/Z5Research/Z5-WeChat-SOP/issues)
- [版本更新日志](CHANGELOG.md)

---

**让内容生产更简单、更高效、更可控。**
