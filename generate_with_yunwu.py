#!/usr/bin/env python3
"""
使用云悟API生成OpenClaw课程宣传图片
API: https://yunwu.ai
模型: Sora2, Nano Banana 2, Veo等先进模型
"""

import os
import json
import requests
import time
from datetime import datetime

# 云悟API配置
YUNWU_API_KEY = "sk-wGqBV0IREwCVg0fLt0Kntavxbgh5iQPUtinvUroUPyWRR5BN"
YUNWU_BASE_URL = "https://yunwu.ai"

# 图片生成配置
IMAGE_CONFIGS = [
    {
        "name": "course_cover",
        "prompt": "A modern, sleek cover design for an AI assistant course. The title 'OpenClaw Complete Course System' is prominently displayed with a tagline 'From Zero to One, Build Your AI Assistant Ecosystem'. The background features abstract circuit patterns blending with financial charts, representing the fusion of AI and finance. Color scheme: blue and purple gradients with gold accents. Style: professional, tech-focused, clean layout.",
        "description": "课程封面图",
        "model": "sora2",  # 使用Sora2模型生成高质量图片
        "size": "1024x1024"
    },
    {
        "name": "tech_architecture",
        "prompt": "An infographic showing the OpenClaw technology stack and architecture. The diagram includes layers: User Interface (Feishu, Telegram, Web), Gateway Layer, Agent System, Model Layer (Claude, GPT, Gemini, DeepSeek), Skills Ecosystem, and Memory System. Arrows show data flow between components. Style: clean technical diagram with icons for each component, monochromatic blue color scheme with highlights.",
        "description": "技术架构图",
        "model": "nano-banana-2",  # 使用Nano Banana 2模型
        "size": "1024x1024"
    },
    {
        "name": "finance_trading",
        "prompt": "A futuristic trading interface for agentic finance. Multiple screens show Polymarket prediction markets, real-time trading signals, risk metrics, and profit/loss charts. AI agents are visualized as glowing orbs analyzing data streams. The scene has a dark theme with neon blue and green highlights, representing the high-tech nature of algorithmic trading.",
        "description": "金融实战场景图",
        "model": "sora2",
        "size": "1024x1024"
    },
    {
        "name": "stock_analysis",
        "prompt": "A smart stock analysis dashboard. The interface displays real-time stock charts with technical indicators (moving averages, RSI, MACD), fundamental data tables, risk assessment metrics, and automated report generation. AI is analyzing patterns and generating buy/sell signals. Style: professional financial software interface, clean white background with data visualizations in corporate blue and green.",
        "description": "股票分析场景图",
        "model": "nano-banana-2",
        "size": "1024x1024"
    },
    {
        "name": "learning_outcomes",
        "prompt": "A before-and-after comparison showing skill transformation. Left side: a person overwhelmed with manual tasks (emails, reports, data analysis). Right side: the same person efficiently managing everything through AI assistants, with dashboards showing productivity metrics improved by 300%. Style: inspirational, positive, showing tangible results, warm color palette with gold accents for achievement.",
        "description": "学习成果对比图",
        "model": "sora2",
        "size": "1024x1024"
    }
]

def generate_image_with_yunwu(prompt, model="sora2", size="1024x1024"):
    """使用云悟API生成图片"""
    
    # 云悟API端点（根据实际API文档调整）
    # 注意：需要查看云悟API文档确定正确的端点
    url = f"{YUNWU_BASE_URL}/api/v1/images/generate"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {YUNWU_API_KEY}"
    }
    
    # 根据云悟API文档调整请求格式
    data = {
        "model": model,
        "prompt": prompt,
        "size": size,
        "num_images": 1,
        "quality": "high",
        "style": "professional"
    }
    
    try:
        print(f"正在使用{model}模型生成图片...")
        print(f"提示词: {prompt[:80]}...")
        
        response = requests.post(url, headers=headers, json=data, timeout=120)
        response.raise_for_status()
        
        result = response.json()
        
        # 根据云悟API响应格式调整
        if "images" in result and len(result["images"]) > 0:
            image_url = result["images"][0]["url"]
            return {
                "success": True,
                "url": image_url,
                "model": model,
                "api_response": result
            }
        elif "data" in result and len(result["data"]) > 0:
            image_url = result["data"][0]["url"]
            return {
                "success": True,
                "url": image_url,
                "model": model,
                "api_response": result
            }
        else:
            print(f"API响应格式异常: {result}")
            return {
                "success": False,
                "error": "API响应格式异常",
                "api_response": result
            }
            
    except requests.exceptions.RequestException as e:
        print(f"API请求失败: {str(e)}")
        return {
            "success": False,
            "error": f"API请求失败: {str(e)}"
        }
    except Exception as e:
        print(f"生成失败: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

def download_image(url, filename):
    """下载图片到本地"""
    
    try:
        print(f"正在下载图片: {filename}")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        with open(filename, "wb") as f:
            f.write(response.content)
        
        file_size = os.path.getsize(filename)
        print(f"✅ 下载成功: {filename} ({file_size/1024:.1f} KB)")
        return True
    except Exception as e:
        print(f"❌ 下载失败: {str(e)}")
        return False

def save_generation_info(config, result, local_path=None):
    """保存生成信息到JSON文件"""
    
    info_file = "yunwu_generated_images.json"
    
    if os.path.exists(info_file):
        with open(info_file, "r", encoding="utf-8") as f:
            existing_data = json.load(f)
    else:
        existing_data = {"generations": []}
    
    generation_info = {
        "name": config["name"],
        "description": config["description"],
        "prompt": config["prompt"],
        "model": config["model"],
        "size": config["size"],
        "generated_at": datetime.now().isoformat(),
        "success": result["success"]
    }
    
    if result["success"]:
        generation_info["image_url"] = result["url"]
        generation_info["model_used"] = result["model"]
        if local_path:
            generation_info["local_path"] = local_path
    else:
        generation_info["error"] = result.get("error", "未知错误")
    
    existing_data["generations"].append(generation_info)
    
    with open(info_file, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=2)
    
    return generation_info

def create_fallback_images():
    """创建备用图片（如果API调用失败）"""
    
    print("\n⚠️ API调用可能失败，创建备用方案...")
    
    # 创建图片目录
    os.makedirs("promo_images", exist_ok=True)
    
    # 创建HTML预览页面
    html_content = """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>OpenClaw课程宣传图片 - 备用方案</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background: #f5f5f7;
                color: #1d1d1f;
            }
            .header {
                text-align: center;
                margin-bottom: 40px;
                padding: 20px;
                background: white;
                border-radius: 12px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            }
            h1 {
                color: #0066cc;
                margin-bottom: 10px;
            }
            .warning {
                background: #fff3cd;
                border: 1px solid #ffeaa7;
                color: #856404;
                padding: 15px;
                border-radius: 8px;
                margin-bottom: 20px;
            }
            .image-grid {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                gap: 20px;
                margin-bottom: 40px;
            }
            .image-card {
                background: white;
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                padding: 20px;
            }
            .image-title {
                font-weight: bold;
                margin-bottom: 10px;
                color: #1d1d1f;
                font-size: 18px;
            }
            .image-desc {
                color: #666;
                margin-bottom: 15px;
                font-size: 14px;
            }
            .prompt-box {
                background: #f8f9fa;
                padding: 12px;
                border-radius: 6px;
                font-size: 12px;
                color: #495057;
                margin-top: 10px;
                border-left: 4px solid #0066cc;
            }
            .action-box {
                background: #e7f5ff;
                padding: 15px;
                border-radius: 8px;
                margin-top: 20px;
                border-left: 4px solid #339af0;
            }
            .footer {
                text-align: center;
                margin-top: 40px;
                padding: 20px;
                color: #666;
                font-size: 14px;
                border-top: 1px solid #eee;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>OpenClaw课程宣传图片生成指南</h1>
            <div class="subtitle">生成时间: """ + datetime.now().strftime("%Y-%m-%d %H:%M") + """</div>
        </div>
        
        <div class="warning">
            <strong>⚠️ 注意：</strong>云悟API调用可能需要手动配置。以下是5张宣传图片的生成提示词，你可以使用以下工具手动生成：
        </div>
        
        <div class="action-box">
            <h3>🎨 推荐生成工具：</h3>
            <ol>
                <li><strong>Midjourney</strong> - 最高质量，在Discord中使用 /imagine 命令</li>
                <li><strong>Leonardo.ai</strong> - 免费额度，高质量生成</li>
                <li><strong>Bing Image Creator</strong> - 完全免费，需微软账号</li>
                <li><strong>DALL-E 3</strong> - 通过ChatGPT Plus使用</li>
            </ol>
        </div>
        
        <div class="image-grid">
    """
    
    for config in IMAGE_CONFIGS:
        html_content += f"""
            <div class="image-card">
                <div class="image-title">{config['description']}</div>
                <div class="image-desc">文件名: {config['name']}.png | 推荐模型: {config['model']}</div>
                <div class="prompt-box">
                    <strong>英文提示词：</strong><br>
                    {config['prompt']}
                </div>
                <div style="margin-top: 10px; font-size: 12px; color: #666;">
                    <strong>尺寸建议：</strong> {config['size']}<br>
                    <strong>风格：</strong> {config['description'].split('图')[0]}
                </div>
            </div>
        """
    
    html_content += """
        </div>
        
        <div class="action-box">
            <h3>🚀 立即行动：</h3>
            <ol>
                <li>选择1-2个最重要的图片（建议：封面图 + 金融实战场景图）</li>
                <li>使用推荐工具生成图片</li>
                <li>保存为PNG格式，命名为对应的文件名</li>
                <li>放入 <code>promo_images/</code> 文件夹</li>
                <li>开始使用图片进行宣传！</li>
            </ol>
        </div>
        
        <div class="footer">
            <p>OpenClaw课程宣传材料 | 备用生成方案</p>
            <p>© 2026 OpenClaw课程团队 | 生成时间: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
        </div>
    </body>
    </html>
    """
    
    with open("promo_images/image_generation_guide.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    # 创建文本指南
    text_guide = "# OpenClaw课程宣传图片生成指南\n\n"
    text_guide += "## 5张宣传图片提示词\n\n"
    
    for config in IMAGE_CONFIGS:
        text_guide += f"### {config['description']}\n"
        text_guide += f"- **文件名**: {config['name']}.png\n"
        text_guide += f"- **推荐模型**: {config['model']}\n"
        text_guide += f"- **尺寸**: {config['size']}\n"
        text_guide += f"- **提示词**:\n```\n{config['prompt']}\n```\n\n"
    
    text_guide += "## 生成工具推荐\n"
    text_guide += "1. **Midjourney** - 最高质量，使用 /imagine 命令\n"
    text_guide += "2. **Leonardo.ai** - 免费额度，注册即用\n"
    text_guide += "3. **Bing Image Creator** - 完全免费\n"
    text_guide += "4. **DALL-E 3** - 通过ChatGPT Plus\n\n"
    
    text_guide += "## 立即行动\n"
    text_guide += "1. 先生成封面图和金融实战场景图\n"
    text_guide += "2. 保存为PNG格式到 promo_images/ 文件夹\n"
    text_guide += "3. 开始使用图片进行宣传\n"
    
    with open("promo_images/GENERATION_GUIDE.md", "w", encoding="utf-8") as f:
        f.write(text_guide)
    
    print("✅ 备用方案已创建:")
    print("   - promo_images/image_generation_guide.html")
    print("   - promo_images/GENERATION_GUIDE.md")
    print("   - 5个专业提示词已准备就绪")

def main():
    print("🎨 OpenClaw课程宣传图片生成工具")
    print("=" * 60)
    print("使用云悟API生成高质量宣传图片")
    print(f"API密钥: {YUNWU_API_KEY[:20]}...")
    print(f"基础URL: {YUNWU_BASE_URL}")
    print("=" * 60)
    
    # 创建图片目录
    os.makedirs("promo_images", exist_ok=True)
    
    results = []
    success_count = 0
    
    for i, config in enumerate(IMAGE_CONFIGS, 1):
        print(f"\n[{i}/{len(IMAGE_CONFIGS)}] 生成: {config['description']}")
        print(f"模型: {config['model']}")
        
        # 生成图片
        result = generate_image_with_yunwu(
            prompt=config["prompt"],
            model=config["model"],
            size=config["size"]
        )
        
        if result["success"]:
            # 下载图片
            filename = f"promo_images/{config['name']}.png"
            if download_image(result["url"], filename):
                success_count += 1
                local_path = filename
            else:
                local_path = None
            
            # 保存生成信息
            gen_info = save_generation_info(config, result, local_path)
            results.append(gen_info)
            
            print(f"✅ 成功生成: {config['description']}")
            if local_path:
                print(f"   保存到: {local_path}")
        else:
            # 保存失败信息
            gen_info = save_generation_info(config, result)
            results.append(gen_info)
            
            print(f"❌ 生成失败: {config['description']}")
            print(f"   错误: {result.get('error', '未知错误')}")
    
    # 生成报告
    print("\n" + "=" * 60)
    print("📊 生成结果汇总:")
    print(f"✅ 成功: {success_count}/{len(IMAGE_CONFIGS)}")
    print(f"❌ 失败: {len(IMAGE_CONFIGS) - success_count}/{len(IMAGE_CONFIGS)}")
    
    if success_count > 0:
        print(f"\n📁 生成的图片保存在: promo_images/