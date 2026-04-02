#!/usr/bin/env python3
"""
环境检查脚本 — 验证运行环境是否就绪
"""

import sys
import subprocess
from pathlib import Path

def check_python_version():
    """检查 Python 版本"""
    version = sys.version_info
    required = (3, 8)
    
    if version >= required:
        return True, f"Python {version.major}.{version.minor}.{version.micro}"
    else:
        return False, f"Python {version.major}.{version.minor}.{version.micro} (需要{'.'.join(map(str, required))}+)"

def check_dependencies():
    """检查依赖包"""
    required_packages = [
        "yaml",      # PyYAML
        "requests",  # requests
    ]
    
    missing = []
    installed = []
    
    for package in required_packages:
        try:
            __import__(package)
            installed.append(package)
        except ImportError:
            missing.append(package)
    
    return missing, installed

def check_directory_structure():
    """检查目录结构"""
    base_dir = Path(__file__).parent.parent
    
    required_dirs = [
        "clients",
        "scripts",
        "templates",
        "config",
        "output",
        "references"
    ]
    
    missing_dirs = []
    existing_dirs = []
    
    for dir_name in required_dirs:
        dir_path = base_dir / dir_name
        if dir_path.exists():
            existing_dirs.append(dir_name)
        else:
            missing_dirs.append(dir_name)
    
    return missing_dirs, existing_dirs

def check_client_configs():
    """检查客户配置"""
    clients_dir = Path(__file__).parent.parent / "clients"
    
    if not clients_dir.exists():
        return [], ["clients 目录不存在"]
    
    clients = []
    issues = []
    
    for client_dir in clients_dir.iterdir():
        if client_dir.is_dir():
            style_yaml = client_dir / "style.yaml"
            if style_yaml.exists():
                clients.append(client_dir.name)
            else:
                issues.append(f"{client_dir.name}: 缺少 style.yaml")
    
    return clients, issues

def check_scripts():
    """检查核心脚本"""
    scripts_dir = Path(__file__).parent
    
    required_scripts = [
        "01-collect-hotspots.py",
        "02-write-article.py",
        "03-audit-article.py",
        "04-publish-draft.py",
        "main.py"
    ]
    
    missing = []
    existing = []
    
    for script in required_scripts:
        script_path = scripts_dir / script
        if script_path.exists():
            existing.append(script)
        else:
            missing.append(script)
    
    return missing, existing

def check_api_keys():
    """检查 API 密钥（可选）"""
    issues = []
    
    # 检查微信配置
    wechat_app_id = subprocess.getoutput("echo $WECHAT_APP_ID")
    wechat_app_secret = subprocess.getoutput("echo $WECHAT_APP_SECRET")
    
    if not wechat_app_id or wechat_app_id.startswith("$"):
        issues.append("未设置 WECHAT_APP_ID 环境变量")
    
    if not wechat_app_secret or wechat_app_secret.startswith("$"):
        issues.append("未设置 WECHAT_APP_SECRET 环境变量")
    
    return issues

def main():
    print("=" * 60)
    print("🔍 Z5-WeChat-SOP 环境检查")
    print("=" * 60)
    print()
    
    all_passed = True
    
    # 1. Python 版本
    print("1️⃣ Python 版本")
    passed, message = check_python_version()
    status = "✅" if passed else "❌"
    print(f"   {status} {message}")
    if not passed:
        all_passed = False
    print()
    
    # 2. 依赖包
    print("2️⃣ 依赖包")
    missing, installed = check_dependencies()
    if missing:
        print(f"   ❌ 缺失：{', '.join(missing)}")
        print(f"   💡 安装：pip install {' '.join(missing)}")
        all_passed = False
    else:
        print(f"   ✅ 已安装：{', '.join(installed)}")
    print()
    
    # 3. 目录结构
    print("3️⃣ 目录结构")
    missing_dirs, existing_dirs = check_directory_structure()
    if missing_dirs:
        print(f"   ⚠️ 缺失：{', '.join(missing_dirs)}")
        print(f"   💡 运行：mkdir -p {' '.join(missing_dirs)}")
    else:
        print(f"   ✅ 完整：{', '.join(existing_dirs)}")
    print()
    
    # 4. 客户配置
    print("4️⃣ 客户配置")
    clients, issues = check_client_configs()
    if clients:
        print(f"   ✅ 已配置：{', '.join(clients)}")
    else:
        print(f"   ⚠️ 无客户配置")
        print(f"   💡 运行：python3 scripts/init-client.py")
    
    if issues:
        for issue in issues:
            print(f"   ⚠️ {issue}")
    print()
    
    # 5. 核心脚本
    print("5️⃣ 核心脚本")
    missing_scripts, existing_scripts = check_scripts()
    if missing_scripts:
        print(f"   ❌ 缺失：{', '.join(missing_scripts)}")
        all_passed = False
    else:
        print(f"   ✅ 完整：{', '.join(existing_scripts)}")
    print()
    
    # 6. API 密钥（可选）
    print("6️⃣ API 密钥（可选）")
    api_issues = check_api_keys()
    if api_issues:
        for issue in api_issues:
            print(f"   ⚠️ {issue}")
        print(f"   💡 在 ~/.zshrc 或 ~/.bashrc 中添加：")
        print(f"      export WECHAT_APP_ID=your_app_id")
        print(f"      export WECHAT_APP_SECRET=your_app_secret")
    else:
        print(f"   ✅ 已配置")
    print()
    
    # 总结
    print("=" * 60)
    if all_passed:
        print("✅ 环境检查通过！可以开始使用")
        print()
        print("🚀 快速开始：")
        print("   python3 scripts/main.py --client {客户名} --mode auto")
    else:
        print("❌ 环境检查未通过，请先修复上述问题")
    print("=" * 60)
    
    return {"status": "passed" if all_passed else "failed"}

if __name__ == "__main__":
    result = main()
    sys.exit(0 if result["status"] == "passed" else 1)
