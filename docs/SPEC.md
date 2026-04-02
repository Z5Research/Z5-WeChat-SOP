# Z5-WeChat-SOP 技术规范文档

## 1. 概述

### 1.1 产品定位

Z5-WeChat-SOP 是一套专为微信公众号内容生产设计的端到端自动化解决方案。

**目标用户**：
- 媒体公司每日内容生产
- 企业官方号运营
- 内容代理机构多客户管理
- 自媒体创作者一人内容团队

### 1.2 核心架构

```
采集代理 → 编辑代理 → 审核代理 → 发布代理
   ↓           ↓           ↓          ↓
热点抓取     文章撰写     3 层审核    排版发布
(微博/头条/百度)  AI 配图     数据校验    草稿箱
选题生成     SEO 优化     来源核实    数据归档
框架选择     视觉 AI      合规检查    效果复盘
```

---

## 2. 功能模块

### 2.1 采集代理

**功能**：
- 多平台热点抓取（微博热搜 / 头条热榜 / 百度热搜）
- 关键词库扩展搜索
- AI 选题生成

**输入**：
- 热点平台 API 或爬虫
- 关键词库配置

**输出**：
- 原始热点数据
- 扩展搜索结果
- 候选选题列表（S/A/B/C 级评分）

**脚本**：`scripts/01-collect-hotspots.py`

---

### 2.2 编辑代理

**功能**：
- 框架选择（5 种模板）
- AI 文章撰写
- 配图生成
- SEO 优化

**框架模板**：

| 模板 | 适用场景 |
|------|---------|
| 痛点型 | 解决用户痛点，引发共鸣 |
| 故事型 | 叙事性强，情感共鸣 |
| 清单型 | 实用性强，便于收藏 |
| 对比型 | 突出产品/方案优势 |
| 热点解读型 | 蹭热点，专业分析 |

**配图生成规范**：

> 提示词工程师3轮法

**第1轮：理解（Read & Analyze）**
- 仔细阅读文章核心章节
- 识别核心信息
- 确定配图类型

**第2轮：提炼（Extract & Refine）**
- 提取中文关键词
- 转化为视觉元素
- 确定配色和风格

**第3轮：优化（Optimize & Generate）**
- 组合完整提示词
- 规避审核敏感词
- 生成并检查

**脚本**：
- `scripts/03-write-article.py` - 文章撰写
- `scripts/04-generate-images.py` - 配图生成
- `scripts/05-seo-optimize.py` - SEO 优化

---

### 2.3 审核代理

**功能**：
- 数据校验（S/A/B/C 分级）
- 来源核实（S/A/B/C 分级）
- 合规检查（标题/客观性/逻辑/法规）

**评级标准**：

| 等级 | 数据可查证率 | 来源权威性 | 处理方式 |
|------|------------|-----------|---------|
| S 级 | 100% | 官方文件/权威媒体 | 直接发布 |
| A 级 | ≥80% | 主流媒体/行业报告 | 直接发布 |
| B 级 | ≥60% | 一般媒体/自媒体 | 修改后发布 |
| C 级 | <60% | 不可靠来源 | 重写或弃用 |

**脚本**：`scripts/06-audit-article.py`

---

### 2.4 发布代理

**功能**：
- 多主题排版
- 素材管理
- 草稿推送
- 数据归档

**排版主题**：

| 主题 | 说明 | 适用场景 |
|------|------|---------|
| professional-clean | 专业简洁（默认） | 企业/政府/行业分析 |
| tech-modern | 科技风（蓝紫渐变） | 科技/互联网/数据报告 |
| warm-editorial | 暖色编辑风 | 故事/人物/生活方式 |
| minimal | 极简黑白 | 文学/严肃内容 |

**脚本**：`scripts/07-publish-draft.py`

---

## 3. API 配置

### 3.1 环境变量

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

### 3.2 微信 API

| 接口 | 用途 |
|------|------|
| `/cgi-bin/token` | 获取 Access Token |
| `/cgi-bin/material/add_material` | 上传永久素材 |
| `/cgi-bin/draft/add` | 添加草稿 |
| `/cgi-bin/material/batchget_material` | 获取素材列表 |

---

## 4. 错误处理

### 4.1 常见错误

| 错误码 | 说明 | 解决方案 |
|--------|------|---------|
| 40007 | invalid media_id | 检查素材是否上传成功 |
| 40066 | invalid url | 检查 API URL 是否正确 |
| 42001 | access_token expired | 重新获取 Token |

### 4.2 降级方案

| 环节 | 可能问题 | 降级方案 |
|------|---------|---------|
| 采集 | 热点抓取失败 | WebSearch 替代 |
| 采集 | 选题为空 | 手动给选题 |
| 编辑 | 配图生成失败 | 输出提示词，用户自行生成 |
| 审核 | 审核不通过 | 返回编辑代理修改 |
| 发布 | 推送失败 | 生成本地 HTML，手动操作 |

---

## 5. 客户配置

### 5.1 目录结构

```
clients/{客户名}/
├── style.yaml        # 风格配置
├── history.yaml      # 发布历史
├── corpus/           # 历史文章语料
├── playbook.md       # 风格指南（可选）
└── lessons/          # 人工修改记录
```

### 5.2 style.yaml 模板

```yaml
name: "客户名称"
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

## 6. 学习机制

### 6.1 人工修改学习

当用户说"我改了，学习一下"时，分析：
- 用词替换（AI 用词 → 人工用词）
- 段落删除/新增
- 结构调整
- 标题修改
- 语气调整

### 6.2 Playbook 自动更新

每积累 5 次 lessons，自动更新 playbook：
- 找出反复出现的 pattern（≥2 次）
- 固化到 playbook.md

---

## 7. 部署

### 7.1 服务器部署

```bash
# 打包
tar -czf z5-wechat-sop.tar.gz z5-wechat-sop/

# 上传
scp z5-wechat-sop.tar.gz user@server:/tmp/

# 解压部署
tar -xzf /tmp/z5-wechat-sop.tar.gz -C /opt/
```

### 7.2 Docker 部署（可选）

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "scripts/main.py", "--help"]
```

---

## 8. 扩展开发

### 8.1 添加新平台采集

在 `scripts/01-collect-hotspots.py` 中添加新平台解析逻辑：

```python
def collect_{platform}_hotspots(limit=30):
    """
    采集 {平台} 热搜

    Args:
        limit: 采集数量

    Returns:
        list: 热搜数据列表
    """
    # TODO: 实现采集逻辑
    pass
```

### 8.2 添加新排版主题

在 `scripts/07-publish-draft.py` 中添加新主题配置：

```python
THEMES = {
    "your-theme": {
        "name": "你的主题",
        "description": "主题描述",
        "css": "主题 CSS"
    }
}
```

---

## 9. 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](../LICENSE) 文件
