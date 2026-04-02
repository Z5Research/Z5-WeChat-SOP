# Z5-WeChat-SOP

**微信公众号内容生产标准作业流程**

简体中文 | [English](README_EN.md)

---

## 🎯 一句话安装

在 OpenClaw 或 AI Agent 环境中粘贴以下指令即可安装此技能：

```
请安装 Z5-WeChat-SOP：微信公众号内容生产标准作业流程
自动化 · 标准化 · 可量化 · 持续进化
```

---

## 📖 简介

Z5-WeChat-SOP 是一套专为微信公众号内容生产设计的端到端自动化解决方案。通过「采集 → 编辑 → 审核 → 发布」四步标准化流程，实现内容生产的自动化、规模化、可复现化。

**设计理念**：源于媒体运营四部策略——选题策划 → 内容生产 → 质量审核 → 分发发布。Z5-SOP 将这四部策略全部自动化，AI 替代人工操作，让内容生产高效且标准化。

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

![工作流程图](workflow.png)

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
│   ├── 01-collect-hotspots.py   # 热点采集
│   ├── 02-write-article.py     # 文章撰写
│   ├── 03-audit-article.py    # 内容审核
│   └── 04-publish-draft.py    # 草稿发布
├── docs/             # 技术文档
├── README.md          # 本文件
├── README_EN.md       # English
├── CHANGELOG.md      # 版本更新
├── cover.png         # 封面图
├── workflow.png      # 工作流程图
└── requirements.txt # 依赖包
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

MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

**让内容生产更简单，更高效，更可控。**
