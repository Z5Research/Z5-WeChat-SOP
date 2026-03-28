# 🟢 Z5-WeChat-SOP

**微信公众号内容生产标准作业流程** · v1.0.0

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/your-org/Z5-WeChat-SOP)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![WeChat](https://img.shields.io/badge/platform-WeChat-07C160.svg)](https://mp.weixin.qq.com)

> **4 代理流水线 + 智能交互**：采集 → 编辑 → 审核 → 发布
> 
> 整合 wewrite、article-writer-auditor、wechat-publisher 等技能的最佳实践

---

## 🎯 快速理解

**4 代理流水线**：

```
采集代理 → 编辑代理 → 审核代理 → 发布代理
   ↓           ↓           ↓          ↓
热点抓取     文章撰写     3 层审核    排版发布
选题生成     配图生成     数据校验    草稿箱
框架选择     SEO 优化     来源核实    数据归档
             视觉 AI      合规检查    效果复盘
```

**默认全自动**——不要中途停下来问用户选哪个选题、选哪个框架。自动选最优的，一口气跑完全流程。只在出错时才停下来。

**交互模式**——如果用户说"交互模式"、"我要自己选"、"让我看看选题"，才在选题/框架/配图处暂停等确认。

---

## 🚀 三种使用模式

### 模式 1：全自动（默认）

```bash
python3 scripts/main.py --client demo --mode auto
```

**特点**：
- ✅ 自动选择最优选题（综合评分最高）
- ✅ 自动选择最佳框架（推荐指数最高）
- ✅ 自动生图（封面 + 内文 3-6 张）
- ✅ 自动推送草稿箱
- ⚡ 一气呵成

### 模式 2：交互模式

```bash
python3 scripts/main.py --client demo --mode interactive
```

**暂停节点**：
| 节点 | 用户操作 |
|------|---------|
| 选题 | 从 10 个中选 |
| 框架 | 从 5 套中选 |
| 配图 | 确认封面风格 |

### 模式 3：分步执行

```bash
# 单独执行任一步骤
python3 scripts/01-collect-hotspots.py
python3 scripts/02-write-article.py
python3 scripts/03-audit-article.py
python3 scripts/04-publish-draft.py
```

---

## 📋 核心流程

### Step 1: 采集 🔍

- 热点抓取（微博/头条/百度）
- 选题生成（10 个，含 SEO 评分）
- 自动选最优或用户选择

### Step 2: 编辑 ✍️

- 框架选择（5 套类型）
- 文章撰写（1500-3500 字）
- 视觉 AI 配图（封面 +3-6 张）
- SEO 优化（标题/摘要/标签）

### Step 3: 审核 ✅

- 数据校验（A/B/C/D 分级）
- 来源核实（S/A/B/C/D 分级）
- 内容审核（标题/客观性/逻辑/合规）

### Step 4: 发布 📤

- 排版（4 套主题）
- 图片上传
- 推送草稿箱
- 数据归档

---

## 📊 审核标准

| 等级 | 数据可查证 | 来源权威 | 处理 |
|------|----------|---------|------|
| S | 100% | 官方文件 | 直接发布 |
| A | ≥80% | 主流媒体 | 直接发布 |
| B | ≥60% | 一般媒体 | 修改后发布 |
| C | <60% | 不可靠 | 重写或弃用 |

---

## 👤 客户配置

### 目录结构

```
clients/{客户名}/
├── style.yaml     # 风格配置
├── history.yaml   # 发布历史
├── corpus/        # 历史文章
├── playbook.md    # 风格指南
└── lessons/       # 修改记录
```

### style.yaml 示例

```yaml
name: "示例客户"
industry: "行业"
topics:
  - "内容方向 1"
  - "内容方向 2"
tone: "专业、客观"
voice: "第三人称"
content_style: "干货 | 数据 | 案例"
theme: "professional-clean"
author: "编辑部"
```

---

## 🎨 排版主题

| 主题 | 风格 | 适用 |
|------|------|------|
| professional-clean | 专业简洁 | 企业/政府/行业 |
| tech-modern | 科技风 | 科技/互联网/数据 |
| warm-editorial | 暖色编辑 | 故事/人物/生活 |
| minimal | 极简黑白 | 文学/严肃 |

---

## 🔄 学习机制

### 学习人工修改

```bash
python3 scripts/learn_edits.py --client demo --draft draft.md --final final.md
```

**分析内容**：
- 用词替换偏好
- 段落删除/新增
- 结构调整习惯
- 标题风格偏好

### Playbook 自动更新

每积累 5 次修改，自动固化到 playbook.md

---

## 📈 效果复盘

```bash
python3 scripts/fetch_stats.py --client demo --days 7
```

**分析维度**：
- 📊 阅读量 Top3
- 📊 分享率最高选题
- 📊 完读率与标题关系
- 📊 粉丝增长趋势

---

## ⚠️ 错误处理

**原则**：不因任何一步失败而停止全流程

| 问题 | 降级方案 |
|------|---------|
| 热点抓取失败 | WebSearch 替代 |
| 配图生成失败 | 输出提示词 |
| 审核不通过 | 返回修改 |
| 发布失败 | 生成本地 HTML |

---

## 🛠️ 安装部署

### 环境要求

- Python 3.8+
- Node.js 16+（用于 wenyan-cli）
- 微信公众号（服务号/订阅号）

### 快速开始

```bash
# 1. 克隆仓库
git clone https://github.com/your-org/Z5-WeChat-SOP.git
cd Z5-WeChat-SOP

# 2. 安装依赖
pip install -r requirements.txt
npm install -g @wenyan-md/cli

# 3. 配置环境变量
export WECHAT_APP_ID="your_app_id"
export WECHAT_APP_SECRET="your_app_secret"
export BAILIAN_API_KEY="your_api_key"

# 4. 创建客户配置
cp clients/demo/style.yaml clients/your-client/style.yaml

# 5. 运行全流程
python3 scripts/main.py --client your-client --mode auto
```

---

## 📁 项目结构

```
Z5-WeChat-SOP/
├── scripts/              # 执行脚本
│   ├── 01-collect-hotspots.py
│   ├── 02-write-article.py
│   ├── 03-audit-article.py
│   ├── 04-publish-draft.py
│   ├── learn_edits.py
│   └── fetch_stats.py
├── clients/              # 客户配置
│   └── demo/
│       ├── style.yaml
│       └── history.yaml
├── references/           # 参考文档
│   ├── topic-selection.md
│   ├── frameworks.md
│   └── writing-guide.md
├── templates/            # 模板文件
├── output/               # 输出目录
├── README.md
├── REQUIREMENTS.txt
└── LICENSE
```

---

## 🆚 与 wewrite 对比

| 维度 | wewrite | Z5-WeChat-SOP |
|------|---------|---------------|
| 定位 | 写作助手 | 全流程 SOP |
| 审核 | ❌ | ✅ 3 层审核 |
| 学习 | ✅ | ✅ + 自动更新 |
| 适用 | 单篇 | 批量/团队 |

---

## 📝 发布后可继续要求

- "帮我润色/缩写/扩写" → 编辑文章
- "封面换暖色调" → 重新生图
- "用框架 B 重写" → 回到 Step 2
- "换一个选题" → 回到 Step 1
- "看看文章数据" → 效果复盘

---

## 🤝 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 📞 联系方式

- **Issues**: [GitHub Issues](https://github.com/your-org/Z5-WeChat-SOP/issues)
- **邮箱**: your-email@example.com

---

## 🙏 致谢

感谢以下开源项目：

- [wewrite](https://github.com/your-org/wewrite) - 公众号写作助手
- [wenyan-cli](https://github.com/wenyan-md/wenyan) - Markdown 转微信排版
- [qwen-image](https://help.aliyun.com/zh/dashscope/) - 阿里云图像生成

---

_版本：1.0.0 · 创建：2026-03-27 · 更新：2026-03-29_
