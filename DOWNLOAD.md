# Z5-WeChat-SOP 下载说明

## GitHub 仓库

**仓库地址**：https://github.com/Z5Research/Z5-WeChat-SOP

> 如 GitHub 访问不便，可使用以下备用下载方式

---

## 完整源码包下载（test01 镜像）

| 文件 | 大小 | 下载地址 |
|------|------|---------|
| **完整源码包** | ~2MB | http://82.157.178.105/z6/z5-wechat-sop.tar.gz |
| **Bundle（Git导入用）** | ~10KB | http://82.157.178.105/z6/z5-wechat-sop.bundle |

---

## 图片资源下载

| 文件 | 大小 | 下载地址 |
|------|------|---------|
| **封面图** | 549KB | http://82.157.178.105/z6/cover.png |
| **工作流程图** | 780KB | http://82.157.178.105/z6/workflow.png |
| **架构图** | 757KB | http://82.157.178.105/z6/architecture.png |

---

## 快速安装

### 方式 1：下载压缩包

```bash
# 下载完整源码
curl -O http://82.157.178.105/z6/z5-wechat-sop.tar.gz

# 解压
tar -xzf z5-wechat-sop.tar.gz
cd z5-wechat-sop

# 安装依赖
pip install -r requirements.txt
```

### 方式 2：Git Bundle 导入

```bash
# 下载 Bundle
curl -O http://82.157.178.105/z6/z5-wechat-sop.bundle

# 创建仓库
mkdir Z5-WeChat-SOP && cd Z5-WeChat-SOP
git init

# 导入 Bundle
git pull /path/to/z5-wechat-sop.bundle

# 添加远程仓库（可选）
git remote add origin https://github.com/Z5Research/Z5-WeChat-SOP.git
```

---

## 提示

- 图片资源较大，建议单独下载
- 源码包不包含 `.git` 目录
- Bundle 包包含完整 Git 历史
