# Z5-WeChat-SOP GitHub 导入指南

## 方式一：本地导入（推荐）

### 步骤 1：下载项目

从 test01 下载：
```bash
scp -r z6@82.157.178.105:/www/wwwroot/z6/z5-wechat-sop .
```

或下载 bundle 文件：
```bash
scp z6@82.157.178.105:/path/to/z5-wechat-sop.bundle .
```

### 步骤 2：创建 GitHub 仓库

1. 登录 GitHub：https://github.com/new
2. 仓库名称：`Z5-WeChat-SOP`
3. 描述：`微信公众号内容生产标准作业流程`
4. 选择 Private 或 Public
5. 点击 "Create repository"

### 步骤 3：推送代码

```bash
cd z5-wechat-sop

# 初始化（如果需要）
git init
git add -A
git commit -m "feat: Z5-WeChat-SOP v4.3.0"

# 添加远程仓库
git remote add origin git@github.com:你的用户名/Z5-WeChat-SOP.git

# 推送
git push -u origin main
```

---

## 方式二：GitHub CLI

```bash
# 安装 gh
brew install gh

# 登录
gh auth login

# 创建仓库
gh repo create Z5-WeChat-SOP --public --clone

# 进入目录
cd Z5-WeChat-SOP

# 复制文件并推送
cp -r /path/to/z5-wechat-sop/* .
git add -A
git commit -m "feat: Z5-WeChat-SOP v4.3.0"
git push
```

---

## 方式三：直接上传

1. 下载 test01 上的项目
2. 在 GitHub 点击 "Create new file"
3. 将文件内容粘贴进去

---

## 验证

推送成功后，访问：
```
https://github.com/你的用户名/Z5-WeChat-SOP
```

应该看到：
- README.md
- LICENSE
- CHANGELOG.md
- docs/SPEC.md
- requirements.txt
