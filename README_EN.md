# Z5-WeChat-SOP

**WeChat Official Account Content Production Standard Operating Procedure**

Automated · Standardized · Quantifiable · Continuously Evolving

[![Version](https://img.shields.io/badge/version-v1.1.0-blue.svg)](https://github.com/Z5Research/Z5-WeChat-SOP)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Stars](https://img.shields.io/github/stars/Z5Research/Z5-WeChat-SOP?style=flat)](https://github.com/Z5Research/Z5-WeChat-SOP/stargazers)

---

## 🎯 One-Click Installation

Install directly in OpenClaw or Agent environment:

```
Please install Z5-WeChat-SOP: WeChat Official Account Content Production SOP
```

Or manual installation:

```bash
# Clone repository
git clone https://github.com/Z5Research/Z5-WeChat-SOP.git

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
export WECHAT_APP_ID=your_app_id
export WECHAT_APP_SECRET=your_app_secret
export VOLC_ACCESS_KEY=your_volc_key
export VOLC_SECRET_KEY=your_volc_secret
```

---

## 📖 Introduction

Z5-WeChat-SOP is a comprehensive automated solution designed specifically for WeChat Official Account content production. Through the "Collection → Editing → Audit → Publishing" four-step standardized workflow, it achieves automated, scalable, and reproducible content production.

**Design Philosophy**:
> Originated from the four strategies of media operations: Topic Planning → Content Production → Quality Audit → Distribution Publishing. Z5-SOP automates all four strategies, with AI replacing manual operations, enabling efficient and standardized content production.

---

## ✨ Core Features

| Feature | Description |
|---------|-------------|
| **4-Step Standardized Workflow** | Collection → Editing → Audit → Publishing |
| **3-Layer Audit Mechanism** | Data Verification / Source Verification / Compliance Check |
| **AI Image Generation** | Volcano Engine doubao-seedream + 3-Round Prompt Engineering |
| **Continuous Learning** | Playbook mechanism, improving with usage |
| **Zero Dependencies** | Self-contained, no external skills required |

---

## 📊 Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                  Z5-WeChat-SOP Workflow                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐  │
│  │Collection│ → │ Editing │ → │  Audit  │ → │Publishing│  │
│  │  Agent   │    │  Agent   │    │  Agent   │    │  Agent   │  │
│  │          │    │          │    │          │    │          │  │
│  │Hotspot   │    │Article   │    │Data      │    │Formatting│  │
│  │Collection│    │Writing   │    │Verification│   │Publishing│  │
│  │Topic     │    │AI Images │    │Source    │    │Draft     │  │
│  │Generation │    │SEO       │    │Compliance│    │Archive   │  │
│  │          │    │Optimization│   │          │    │          │  │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘  │
│                                                                 │
│  Weibo          AI Writing       S/A/B/C      wenyan-cli  │
│  Toutiao     →   Framework  →   3-Layer  →   Draft Box    │
│  Baidu           Templates        Audit        Auto-Archive  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Mode 1: Full Auto

```bash
python3 scripts/main.py --client your_account --mode auto
```

### Mode 2: Interactive

```bash
python3 scripts/main.py --client your_account --mode interactive
```

### Mode 3: Step by Step

```bash
# Step 1: Collect hotspots
python3 scripts/01-collect-hotspots.py --limit 30

# Step 2: Write article
python3 scripts/03-write-article.py --client your_account --topic "Topic"

# Step 3: Audit article
python3 scripts/06-audit-article.py --client your_account

# Step 4: Publish draft
python3 scripts/07-publish-draft.py --client your_account
```

---

## 📁 Project Structure

```
Z5-WeChat-SOP/
├── scripts/
│   ├── 01-collect-hotspots.py    # Hotspot collection
│   ├── 02-write-article.py      # Article writing
│   ├── 03-audit-article.py     # Content audit
│   ├── 04-publish-draft.py     # Draft publishing
│   ├── 05-seo-optimize.py       # SEO optimization
│   ├── 06-generate-images.py    # AI image generation
│   ├── 07-archive-data.py      # Data archiving
│   ├── 08-fetch-stats.py        # Stats fetching
│   └── 09-learn-edits.py       # Learning from edits
├── docs/
│   └── SPEC.md                   # Technical specification
├── clients/                      # Client configurations
├── README.md
├── LICENSE
├── CHANGELOG.md
├── requirements.txt
└── workflow.png               # Workflow diagram
```

---

## 🎨 Core Functions

### 3-Round Prompt Engineering

Each image requires:

1. **Understand (Read & Analyze)** - Identify core info, determine image type
2. **Extract (Extract & Refine)** - Extract keywords, transform to visual elements
3. **Optimize (Optimize & Generate)** - Combine complete prompt, avoid sensitive content

### 3-Layer Audit Mechanism

| Audit Dimension | Rating | Description |
|-----------------|--------|-------------|
| **Data Verification** | S/A/B/C | Core data must be S/A to publish |
| **Source Verification** | S/A/B/C | Official/Authoritative/Mainstream/General |
| **Compliance Check** | Pass/Fail | Title/Objectivity/Logic/Legal |

---

## 📊 Efficiency Improvement

| Dimension | Traditional | Z5-SOP | Improvement |
|-----------|-------------|---------|-------------|
| Time per Article | 4 hours | 30 minutes | **-87.5%** |
| Image Cost | 200 yuan/piece | ≈0 yuan | **-100%** |
| Publishing Frequency | Irregular | Daily stable | **Controllable** |
| Data Verification | Manual | 3-layer auto | **Standardized** |

---

## ⚙️ Configuration

### Environment Variables

```bash
# WeChat Official Account
export WECHAT_APP_ID=your_app_id
export WECHAT_APP_SECRET=your_app_secret

# Volcano Engine (Image Generation)
export VOLC_ACCESS_KEY=your_access_key
export VOLC_SECRET_KEY=your_secret_key

# Alibaba Cloud Bailian (Backup)
export BAILIAN_API_KEY=your_api_key
```

### Client Configuration

```yaml
# clients/your_account/style.yaml
name: "Your Account"
industry: "Industry"
topics:
  - "Content Direction 1"
  - "Content Direction 2"
tone: "Writing Style"
cover_style: "Cover Style Description"
author: "Signature"
theme: "professional-clean"
```

---

## 📖 Documentation

- [Technical Specification](docs/SPEC.md) - Detailed SOP documentation
- [Changelog](CHANGELOG.md) - Version updates

---

## 🤝 Contributing

Issues and Pull Requests are welcome!

---

## 📄 License

MIT License - See [LICENSE](LICENSE)

---

**Making content production simpler, more efficient, and more controllable.**
