# Z5-WeChat-SOP

**微信公众号内容生产标准作业流程**

[English](README_EN.md) | 简体中文

[![Version](https://img.shields.io/badge/version-v1.1.0-blue.svg)](https://github.com/Z5Research/Z5-WeChat-SOP)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Stars](https://img.shields.io/github/stars/Z5Research/Z5-WeChat-SOP?style=flat)](https://github.com/Z5Research/Z5-WeChat-SOP/stargazers)

---

## 🎯 一句话安装

复制以下指令，粘贴到 AI Agent 中即可自动安装：

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
| **持续进化** | Playbook 学习机制 |

---

## 📊 工作流程

![工作流程](workflow.png)

---

## 🚀 快速开始

### 全自动模式

```bash
python3 scripts/main.py --client 你的公众号名 --mode auto
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

## 📖 文档

- [SKILL.md](SKILL.md) - 一句话安装文件
- [完整规范](docs/SPEC.md) - 技术规范文档
- [版本更新](CHANGELOG.md) - 版本日志

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可证

MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

**让内容生产更简单，更高效，更可控。**
