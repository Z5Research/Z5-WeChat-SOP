# 更新日志

All notable changes to this project will be documented in this file.

## [4.3.0] - 2026-04-02

### 新增
- 微信公众号发布 40007 错误处理规范
- 配图方案：必须上传到永久素材库获取 URL
- 审核报告留存规范（每篇必须留存 Markdown + HTML）

### 修复
- HTML 编码规范（UTF-8 with BOM）
- test01 部署检查流程

## [4.2.0] - 2026-04-02

### 新增
- 火山引擎图像生成技能集成（doubao-seedream-4-5-251128）
- 生图环节双引擎配置（火山引擎优先，千问备选）
- 提示词工程师3轮法

## [4.0.0] - 2026-04-01

### 新增
- 集成热点抓取（微博/头条/百度）
- 全面关键词库（10大类200+关键词）
- 千问生图集成（qwen-image-max-2025-12-30）
- 采集库管理工具（list/show/merge/report）
- 不依赖外部技能，全部自包含

### 变更
- 完全重写架构，变为自包含技能

## [3.0.0] - 2026-03-31

### 新增
- 自包含完整技能，不依赖外部技能
- 配图标准更新为3张（封面 + 2张信息图）
- 发布代理基于 wenyan-cli，支持一键推送

## [2.0.0] - 2026-03-29

### 变更
- 整合 wewrite、article-writer-auditor、wechat-publisher
- 初始版本

---

## 贡献者

- Z5 Research Team

## 许可证

本项目采用 MIT 许可证
