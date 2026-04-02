#!/usr/bin/env python3
"""
测试脚本 — 验证全流程功能
"""

import sys
import json
from pathlib import Path
from datetime import datetime

def test_environment():
    """测试 1: 环境检查"""
    print("\n" + "=" * 60)
    print("测试 1: 环境检查")
    print("=" * 60)
    
    from check_env import main as check_env_main
    result = check_env_main()
    
    passed = result.get("status") == "passed"
    print(f"结果：{'✅ 通过' if passed else '❌ 失败'}")
    return passed

def test_directory_structure():
    """测试 2: 目录结构"""
    print("\n" + "=" * 60)
    print("测试 2: 目录结构")
    print("=" * 60)
    
    base_dir = Path(__file__).parent.parent
    
    required = [
        "clients",
        "scripts",
        "templates",
        "config",
        "output",
        "references",
        "main.py",
        "SKILL.md",
        "README.md"
    ]
    
    missing = []
    for item in required:
        if not (base_dir / item).exists():
            missing.append(item)
    
    if missing:
        print(f"❌ 缺失：{', '.join(missing)}")
        return False
    else:
        print("✅ 目录结构完整")
        return True

def test_client_config():
    """测试 3: 客户配置"""
    print("\n" + "=" * 60)
    print("测试 3: 客户配置")
    print("=" * 60)
    
    clients_dir = Path(__file__).parent.parent / "clients"
    
    if not clients_dir.exists():
        print("❌ clients 目录不存在")
        return False
    
    # 检查体旅汇配置
    tlvhui_config = clients_dir / "tlvhui" / "style.yaml"
    if not tlvhui_config.exists():
        print("❌ tlvhui/style.yaml 不存在")
        return False
    
    # 验证 YAML 格式
    import yaml
    try:
        with open(tlvhui_config, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        
        required_fields = ["name", "industry", "topics", "tone"]
        missing_fields = [f for f in required_fields if f not in config]
        
        if missing_fields:
            print(f"⚠️ 缺少字段：{', '.join(missing_fields)}")
        else:
            print(f"✅ 客户配置有效：{config['name']}")
        
        return True
    
    except Exception as e:
        print(f"❌ 配置解析失败：{e}")
        return False

def test_scripts():
    """测试 4: 核心脚本"""
    print("\n" + "=" * 60)
    print("测试 4: 核心脚本")
    print("=" * 60)
    
    scripts_dir = Path(__file__).parent
    base_dir = Path(__file__).parent.parent
    
    required_scripts = [
        "01-collect-hotspots.py",
        "02-write-article.py",
        "03-audit-article.py",
        "04-publish-draft.py",
        "05-seo-optimize.py",
        "06-generate-images.py",
        "07-archive-data.py",
        "08-fetch-stats.py",
        "09-learn-edits.py",
        "10-build-playbook.py",
        "init-client.py",
        "check-env.py"
    ]
    
    # main.py 在根目录
    if not (base_dir / "main.py").exists():
        print("❌ 缺失脚本：main.py")
        return False
    
    missing = []
    for script in required_scripts:
        if not (scripts_dir / script).exists():
            missing.append(script)
    
    if missing:
        print(f"❌ 缺失脚本：{', '.join(missing)}")
        return False
    else:
        print(f"✅ 核心脚本完整（{len(required_scripts)} 个）")
        return True

def test_templates():
    """测试 5: 模板文件"""
    print("\n" + "=" * 60)
    print("测试 5: 模板文件")
    print("=" * 60)
    
    templates_dir = Path(__file__).parent.parent / "templates"
    
    if not templates_dir.exists():
        print("❌ templates 目录不存在")
        return False
    
    required_templates = [
        "article-frameworks.md"
    ]
    
    missing = []
    for template in required_templates:
        if not (templates_dir / template).exists():
            missing.append(template)
    
    if missing:
        print(f"❌ 缺失模板：{', '.join(missing)}")
        return False
    else:
        print(f"✅ 模板文件完整（{len(required_templates)} 个）")
        return True

def test_config_files():
    """测试 6: 配置文件"""
    print("\n" + "=" * 60)
    print("测试 6: 配置文件")
    print("=" * 60)
    
    config_dir = Path(__file__).parent.parent / "config"
    
    if not config_dir.exists():
        print("❌ config 目录不存在")
        return False
    
    required_configs = [
        "default.yaml",
        "production.yaml"
    ]
    
    missing = []
    for config in required_configs:
        if not (config_dir / config).exists():
            missing.append(config)
    
    if missing:
        print(f"❌ 缺失配置：{', '.join(missing)}")
        return False
    else:
        print(f"✅ 配置文件完整（{len(required_configs)} 个）")
        
        # 验证 YAML 格式
        import yaml
        for config in required_configs:
            try:
                with open(config_dir / config, "r", encoding="utf-8") as f:
                    yaml.safe_load(f)
            except Exception as e:
                print(f"❌ {config} 解析失败：{e}")
                return False
        
        print("✅ 配置文件格式正确")
        return True

def test_references():
    """测试 7: 参考资料"""
    print("\n" + "=" * 60)
    print("测试 7: 参考资料")
    print("=" * 60)
    
    references_dir = Path(__file__).parent.parent / "references"
    
    if not references_dir.exists():
        print("❌ references 目录不存在")
        return False
    
    required_refs = [
        "example-article-S.md",
        "prompt-library.md"
    ]
    
    missing = []
    for ref in required_refs:
        if not (references_dir / ref).exists():
            missing.append(ref)
    
    if missing:
        print(f"❌ 缺失资料：{', '.join(missing)}")
        return False
    else:
        print(f"✅ 参考资料完整（{len(required_refs)} 个）")
        return True

def test_documentation():
    """测试 8: 文档完整性"""
    print("\n" + "=" * 60)
    print("测试 8: 文档完整性")
    print("=" * 60)
    
    base_dir = Path(__file__).parent.parent
    
    required_docs = [
        "README.md",
        "SKILL.md",
        "CHANGELOG.md",
        "FAQ.md",
        "RELEASE.md"
    ]
    
    missing = []
    for doc in required_docs:
        if not (base_dir / doc).exists():
            missing.append(doc)
    
    if missing:
        print(f"❌ 缺失文档：{', '.join(missing)}")
        return False
    else:
        print(f"✅ 文档完整（{len(required_docs)} 个）")
        return True

def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("🧪 Z5-WeChat-SOP 功能测试")
    print(f"🕐 时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    
    tests = [
        ("环境检查", test_environment),
        ("目录结构", test_directory_structure),
        ("客户配置", test_client_config),
        ("核心脚本", test_scripts),
        ("模板文件", test_templates),
        ("配置文件", test_config_files),
        ("参考资料", test_references),
        ("文档完整性", test_documentation)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed))
        except Exception as e:
            print(f"\n❌ {name} 测试异常：{e}")
            results.append((name, False))
    
    # 总结
    print("\n" + "=" * 60)
    print("📊 测试结果总结")
    print("=" * 60)
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    for name, passed in results:
        status = "✅" if passed else "❌"
        print(f"{status} {name}")
    
    print()
    print(f"总计：{passed_count}/{total_count} 通过")
    
    if passed_count == total_count:
        print("\n🎉 所有测试通过！技能已就绪")
        return True
    else:
        print(f"\n⚠️ {total_count - passed_count} 个测试未通过，请修复")
        return False

def main():
    success = run_all_tests()
    
    # 输出结果
    result = {
        "timestamp": datetime.now().isoformat(),
        "total_tests": 8,
        "passed": success,
        "status": "success" if success else "failed"
    }
    
    # 保存测试结果
    output_dir = Path(__file__).parent.parent / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    result_path = output_dir / f"test-result-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    with open(result_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"\n📄 测试结果：{result_path}")
    
    return result

if __name__ == "__main__":
    result = main()
    sys.exit(0 if result["status"] == "success" else 1)
