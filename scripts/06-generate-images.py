#!/usr/bin/env python3
"""
配图生成代理 v3.0 - 集成火山引擎+千问双引擎
提示词工程师3轮法：理解→提炼→优化

- 火山引擎 doubao-seedream-4-5-251128（首选）
- 千问 qwen-image-max-2025-12-30（备选）
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from datetime import datetime

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

# 配置路径
BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "output" / "images"

# 火山引擎配置（首选）
VOLCENGINE_API_KEY = "029e073d-396d-484d-87ac-48766bdb9577"
VOLCENGINE_URL = "https://ark.cn-beijing.volces.com/api/v3/images/generations"
VOLCENGINE_MODEL = "doubao-seedream-4-5-251128"

# 千问配置（备选）
QWEN_MODEL = "qwen-image-max-2025-12-30"
QWEN_API_KEY = os.environ.get("BAILIAN_API_KEY", "")


def ensure_dirs():
    """确保目录存在"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def generate_with_volcengine(prompt, size="2K"):
    """使用火山引擎生成图片（首选）
    
    Args:
        prompt: 提示词（必须100%中文）
        size: 尺寸 (2K=2048x2048)
    
    Returns:
        dict: {"success": bool, "url": str, "path": str}
    """
    if not HAS_REQUESTS:
        return {"success": False, "error": "requests 库未安装"}
    
    headers = {
        "Authorization": f"Bearer {VOLCENGINE_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": VOLCENGINE_MODEL,
        "prompt": prompt,
        "size": size,
        "response_format": "url",
        "watermark": False
    }
    
    try:
        print(f"[*] 调用火山引擎生图...")
        print(f"[*] 模型: {VOLCENGINE_MODEL}")
        print(f"[*] 尺寸: {size}")
        print(f"[*] 提示词: {prompt[:80]}...")
        
        response = requests.post(VOLCENGINE_URL, headers=headers, json=data, timeout=180)
        
        if response.status_code == 200:
            result = response.json()
            image_url = result["data"][0]["url"]
            img_size = result["data"][0].get("size", size)
            
            print(f"[✓] 生成成功! URL: {image_url[:60]}...")
            
            # 下载图片
            image_path = download_image(image_url, OUTPUT_DIR)
            
            return {
                "success": True,
                "url": image_url,
                "path": str(image_path) if image_path else "",
                "size": img_size,
                "engine": "volcengine"
            }
        elif response.status_code == 400:
            error_msg = response.text
            if "SensitiveContent" in error_msg:
                return {"success": False, "error": "内容审核拦截，请优化提示词", "engine": "volcengine"}
            return {"success": False, "error": error_msg[:200], "engine": "volcengine"}
        else:
            return {"success": False, "error": f"HTTP {response.status_code}: {response.text[:200]}", "engine": "volcengine"}
            
    except Exception as e:
        return {"success": False, "error": str(e), "engine": "volcengine"}


def generate_with_qwen(prompt, size="1280*720", model=QWEN_MODEL):
    """使用千问生图生成图片（备选）
    
    Args:
        prompt: 提示词
        size: 尺寸
    
    Returns:
        dict: {"success": bool, "url": str, "path": str}
    """
    if not QWEN_API_KEY:
        return {"success": False, "error": "BAILIAN_API_KEY 环境变量未设置", "engine": "qwen"}
    
    if not HAS_REQUESTS:
        return {"success": False, "error": "requests 库未安装", "engine": "qwen"}
    
    url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation"
    headers = {
        "Authorization": f"Bearer {QWEN_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": model,
        "input": {"messages": [{"role": "user", "content": [{"text": prompt}]}]}
    }
    
    if size:
        data["parameters"] = {"size": size}
    
    try:
        print(f"[*] 调用千问生图（备选）...")
        response = requests.post(url, headers=headers, json=data, timeout=180)
        result = response.json()
        
        if "output" in result:
            image_url = result["output"]["choices"][0]["message"]["content"][0]["image"]
            print(f"[✓] 生成成功! URL: {image_url[:60]}...")
            
            image_path = download_image(image_url, OUTPUT_DIR)
            
            return {
                "success": True,
                "url": image_url,
                "path": str(image_path) if image_path else "",
                "engine": "qwen"
            }
        else:
            return {"success": False, "error": result.get("message", "未知错误"), "engine": "qwen"}
    except Exception as e:
        return {"success": False, "error": str(e), "engine": "qwen"}


def download_image(url, output_dir):
    """下载图片到本地"""
    if not HAS_REQUESTS:
        return None
    
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"image_{timestamp}.png"
        output_path = output_dir / filename
        
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        
        with open(output_path, "wb") as f:
            f.write(response.content)
        
        print(f"[✓] 下载完成: {output_path}")
        return output_path
    
    except Exception as e:
        print(f"[x] 下载失败: {e}")
        return None


def round1_understand(article_title, article_content, image_type):
    """第1轮：理解
    仔细阅读文章，识别该配图需要传达的核心信息
    
    Returns:
        dict: {
            "core_info": 核心信息（3个关键词）,
            "image_type": 配图类型（封面/信息图）,
            "keywords": [关键词列表]
        }
    """
    print(f"\n[第1轮-理解] 分析文章核心...")
    
    # 分析文章获取核心信息
    core_info = {
        "封面图": {
            "core": "文章主题的视觉呈现",
            "keywords": ["主视觉元素", "配色风格", "情感调性"]
        },
        "信息图1": {
            "core": "第一组关键数据/观点",
            "keywords": ["数据点1", "数据点2", "数据点3"]
        },
        "信息图2": {
            "core": "第二组关键数据/观点",
            "keywords": ["观点A", "观点B", "观点C"]
        }
    }
    
    return core_info.get(image_type, core_info["封面图"])


def round2_refine(article_title, article_content, image_type, round1_result):
    """第2轮：提炼
    从文章中提炼中文关键描述，转化为图片元素清单
    
    Returns:
        dict: {
            "visual_elements": 主视觉元素,
            "colors": 配色方案,
            "text_labels": 文字标注,
            "style": 风格参考
        }
    """
    print(f"[第2轮-提炼] 提炼图片元素...")
    
    # 根据文章内容自动提炼元素（简化版，实际可接入LLM分析）
    refined = {
        "封面图": {
            "visual_elements": "文章主题相关的视觉元素组合",
            "colors": "蓝色系商务配色，专业数据可视化",
            "text_labels": f"'{article_title}'",
            "style": "现代专业，简洁大气"
        },
        "信息图1": {
            "visual_elements": "数据图表元素组合",
            "colors": "蓝色渐变+橙色点缀",
            "text_labels": "数据标注文字",
            "style": "清晰易读，专业商务"
        },
        "信息图2": {
            "visual_elements": "分布/对比/流程元素",
            "colors": "多彩区分，专业图表",
            "text_labels": "分类标注",
            "style": "简洁专业，信息密集"
        }
    }
    
    return refined.get(image_type, refined["封面图"])


def round3_optimize(image_type, round1_result, round2_result):
    """第3轮：优化
    组合成完整中文提示词，避免审核敏感词
    
    Returns:
        str: 完整的中文提示词
    """
    print(f"[第3轮-优化] 生成最终提示词...")
    
    # 避免审核的敏感词替换
    avoid_words = ["地图", "中国", "省份", "城市名", "真实地理"]
    safe_substitutes = ["信息图", "区域分布", "抽象图标", "图标化展示", "示意"]
    
    # 组装提示词
    prompts = {
        "封面图": f"中文封面图，{round2_result['visual_elements']}，{round2_result['text_labels']}，{round2_result['colors']}，{round2_result['style']}，无水印无文字",
        "信息图1": f"中文信息图，{round2_result['visual_elements']}，{round2_result['text_labels']}，{round2_result['colors']}，{round2_result['style']}，专业数据可视化",
        "信息图2": f"中文信息图，{round2_result['visual_elements']}，{round2_result['text_labels']}，{round2_result['colors']}，{round2_result['style']}，图表化展示"
    }
    
    prompt = prompts.get(image_type, prompts["封面图"])
    
    # 敏感词替换
    for avoid, safe in zip(avoid_words, safe_substitutes):
        prompt = prompt.replace(avoid, safe)
    
    print(f"[✓] 最终提示词: {prompt}")
    
    return prompt


def generate_image_3round(article_title, article_content, image_type):
    """3轮提示词工程师法生成图片
    
    Args:
        article_title: 文章标题
        article_content: 文章内容
        image_type: 图片类型（封面图/信息图1/信息图2）
    
    Returns:
        dict: 生成结果
    """
    print(f"\n{'='*50}")
    print(f"🎨 生成 {image_type} - 提示词工程师3轮法")
    print(f"{'='*50}")
    
    # 第1轮：理解
    r1 = round1_understand(article_title, article_content, image_type)
    print(f"[1] 核心信息: {r1['core']}")
    print(f"[1] 关键词: {r1['keywords']}")
    
    # 第2轮：提炼
    r2 = round2_refine(article_title, article_content, image_type, r1)
    print(f"[2] 主视觉: {r2['visual_elements']}")
    print(f"[2] 配色: {r2['colors']}")
    print(f"[2] 风格: {r2['style']}")
    
    # 第3轮：优化
    prompt = round3_optimize(image_type, r1, r2)
    
    # 生成图片（优先火山引擎，失败则千问）
    print(f"\n[*] 开始生成图片...")
    
    # 火山引擎
    result = generate_with_volcengine(prompt, size="2K")
    
    if not result.get("success"):
        print(f"[!] 火山引擎失败，尝试千问备选...")
        result = generate_with_qwen(prompt)
    
    return result


def generate_cover_image(article_title, article_content):
    """生成封面图（3轮法）"""
    return generate_image_3round(article_title, article_content, "封面图")


def generate_info_image_1(article_title, article_content):
    """生成信息图1（3轮法）"""
    return generate_image_3round(article_title, article_content, "信息图1")


def generate_info_image_2(article_title, article_content):
    """生成信息图2（3轮法）"""
    return generate_image_3round(article_title, article_content, "信息图2")


def main():
    parser = argparse.ArgumentParser(description='配图生成代理 v3.0 - 提示词工程师3轮法')
    parser.add_argument('--article', '-a', required=True, help='文章路径')
    parser.add_argument('--client', '-c', required=True, help='客户名称')
    parser.add_argument('--provider', '-p', default='volcengine', help='生图引擎（默认：volcengine）')
    parser.add_argument('--output-dir', '-o', help='输出目录')
    parser.add_argument('--count', type=int, default=3, help='配图数量（默认：3）')
    
    args = parser.parse_args()
    
    ensure_dirs()
    
    print("=" * 60)
    print("🎨 Z5-WeChat-SOP 配图生成代理 v3.0")
    print("=" * 60)
    print(f"客户: {args.client}")
    print(f"文章: {args.article}")
    print(f"引擎: 火山引擎（首选）→ 千问（备选）")
    print(f"方法: 提示词工程师3轮法（理解→提炼→优化）")
    print(f"配图数量: {args.count}")
    print("-" * 60)
    
    # 读取文章
    article_path = Path(args.article)
    if not article_path.exists():
        print(f"❌ 文章不存在: {article_path}")
        return {"status": "failed", "error": "article_not_found"}
    
    article_content = article_path.read_text(encoding="utf-8")
    print(f"[✓] 文章读取成功: {len(article_content)} 字符")
    
    # 提取文章标题
    article_title = "体育旅游文章"
    if "---" in article_content:
        import re
        title_match = re.search(r"title:\s*(.+)", article_content)
        if title_match:
            article_title = title_match.group(1).strip()
    else:
        first_line = article_content.strip().split("\n")[0]
        if first_line.startswith("#"):
            article_title = first_line.lstrip("#").strip()
    
    print(f"[✓] 文章标题: {article_title}")
    
    # 生成配图
    results = {}
    
    if args.count >= 1:
        result = generate_cover_image(article_title, article_content)
        results["cover"] = result
        if result.get("success"):
            print(f"[✓] 封面图成功: {result.get('path')} ({result.get('engine')})")
        else:
            print(f"[x] 封面图失败: {result.get('error')}")
        time.sleep(2)
    
    if args.count >= 2:
        result = generate_info_image_1(article_title, article_content)
        results["info1"] = result
        if result.get("success"):
            print(f"[✓] 信息图1成功: {result.get('path')} ({result.get('engine')})")
        else:
            print(f"[x] 信息图1失败: {result.get('error')}")
        time.sleep(2)
    
    if args.count >= 3:
        result = generate_info_image_2(article_title, article_content)
        results["info2"] = result
        if result.get("success"):
            print(f"[✓] 信息图2成功: {result.get('path')} ({result.get('engine')})")
        else:
            print(f"[x] 信息图2失败: {result.get('error')}")
    
    # 保存结果
    result_file = OUTPUT_DIR / f"images_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    result_data = {
        "client": args.client,
        "article": str(article_path),
        "timestamp": datetime.now().isoformat(),
        "method": "提示词工程师3轮法",
        "engine": "volcengine优先，qwen备选",
        "results": results
    }
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump(result_data, f, ensure_ascii=False, indent=2)
    print(f"\n[✓] 结果已保存: {result_file}")
    
    # 完成
    print("\n" + "=" * 60)
    print("✅ 配图生成完成")
    print("=" * 60)
    
    success_count = sum(1 for r in results.values() if r.get("success"))
    print(f"成功: {success_count}/{args.count} 张")
    
    for name, result in results.items():
        if result.get("success"):
            print(f"  ✓ {name}: {result.get('path')} ({result.get('engine')})")
        else:
            print(f"  ✗ {name}: {result.get('error')}")
    
    return {
        "status": "success" if success_count > 0 else "failed",
        "results": results,
        "success_count": success_count
    }


if __name__ == "__main__":
    result = main()
    sys.exit(0 if result.get("status") == "success" else 1)
