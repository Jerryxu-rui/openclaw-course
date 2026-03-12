#!/usr/bin/env python3
"""
OpenClaw课程宣传图片生成脚本
使用DALL-E 3 API生成宣传图片
"""

import os
import json
import requests
from datetime import datetime

# 从环境变量获取API密钥
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    print("⚠️ 请设置OPENAI_API_KEY环境变量")
    print("export OPENAI_API_KEY=你的OpenAI API密钥")
    exit(1)

# 图片生成配置
IMAGE_CONFIGS = [
    {
        "name": "course_cover",
        "prompt": "A modern, sleek cover design for an AI assistant course. The title 'OpenClaw Complete Course System' is prominently displayed with a tagline 'From Zero to One, Build Your AI Assistant Ecosystem'. The background features abstract circuit patterns blending with financial charts, representing the fusion of AI and finance. Color scheme: blue and purple gradients with gold accents. Style: professional, tech-focused, clean layout.",
        "size": "1024x1024",
        "description": "课程封面图"
    },
    {
        "name": "tech_architecture",
        "prompt": "An infographic showing the OpenClaw technology stack and architecture. The diagram includes layers: User Interface (Feishu, Telegram, Web), Gateway Layer, Agent System, Model Layer (Claude, GPT, Gemini, DeepSeek), Skills Ecosystem, and Memory System. Arrows show data flow between components. Style: clean technical diagram with icons for each component, monochromatic blue color scheme with highlights.",
        "size": "1024x1024",
        "description": "技术架构图"
    },
    {
        "name": "finance_trading",
        "prompt": "A futuristic trading interface for agentic finance. Multiple screens show Polymarket prediction markets, real-time trading signals, risk metrics, and profit/loss charts. AI agents are visualized as glowing orbs analyzing data streams. The scene has a dark theme with neon blue and green highlights, representing the high-tech nature of algorithmic trading.",
        "size": "1024x1024",
        "description": "金融实战场景图"
    },
    {
        "name": "stock_analysis",
        "prompt": "A smart stock analysis dashboard. The interface displays real-time stock charts with technical indicators (moving averages, RSI, MACD), fundamental data tables, risk assessment metrics, and automated report generation. AI is analyzing patterns and generating buy/sell signals. Style: professional financial software interface, clean white background with data visualizations in corporate blue and green.",
        "size": "1024x1024",
        "description": "股票分析场景图"
    },
    {
        "name": "learning_outcomes",
        "prompt": "A before-and-after comparison showing skill transformation. Left side: a person overwhelmed with manual tasks (emails, reports, data analysis). Right side: the same person efficiently managing everything through AI assistants, with dashboards showing productivity metrics improved by 300%. Style: inspirational, positive, showing tangible results, warm color palette with gold accents for achievement.",
        "size": "1024x1024",
        "description": "学习成果对比图"
    }
]

def generate_image(prompt, size="1024x1024"):
    """使用DALL-E 3生成图片"""
    
    url = "https://api.openai.com/v1/images/generations"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    
    data = {
        "model": "dall-e-3",
        "prompt": prompt,
        "n": 1,
        "size": size,
        "quality": "standard",
        "style": "natural"
    }
    
    try:
        print(f"正在生成图片: {prompt[:50]}...")
        response = requests.post(url, headers=headers, json=data, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        image_url = result["data"][0]["url"]
        
        return {
            "success": True,
            "url": image_url,
            "revised_prompt": result["data"][0].get("revised_prompt", "")
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def save_image_info(image_info, config):
    """保存图片信息到JSON文件"""
    
    info_file = "generated_images_info.json"
    
    if os.path.exists(info_file):
        with open(info_file, "r", encoding="utf-8") as f:
            existing_data = json.load(f)
    else:
        existing_data = {"images": []}
    
    image_data = {
        "name": config["name"],
        "description": config["description"],
        "prompt": config["prompt"],
        "generated_at": datetime.now().isoformat(),
        "url": image_info.get("url", ""),
        "revised_prompt": image_info.get("revised_prompt", ""),
        "success": image_info["success"]
    }
    
    if not image_info["success"]:
        image_data["error"] = image_info.get("error", "")
    
    existing_data["images"].append(image_data)
    
    with open(info_file, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=2)
    
    return image_data

def download_image(url, filename):
    """下载图片到本地"""
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        with open(filename, "wb") as f:
            f.write(response.content)
        
        return True
    except Exception as e:
        print(f"下载失败: {str(e)}")
        return False

def main():
    print("🎨 OpenClaw课程宣传图片生成工具")
    print("=" * 50)
    
    # 创建图片目录
    os.makedirs("promo_images", exist_ok=True)
    
    results = []
    
    for config in IMAGE_CONFIGS:
        print(f"\n📸 生成: {config['description']}")
        print(f"提示词: {config['prompt'][:100]}...")
        
        # 生成图片
        result = generate_image(config["prompt"], config["size"])
        
        # 保存信息
        image_data = save_image_info(result, config)
        
        if result["success"]:
            # 下载图片
            filename = f"promo_images/{config['name']}.png"
            if download_image(result["url"], filename):
                print(f"✅ 成功生成并保存: {filename}")
                image_data["local_path"] = filename
            else:
                print(f"⚠️ 生成成功但下载失败，URL: {result['url']}")
                image_data["local_path"] = None
        else:
            print(f"❌ 生成失败: {result.get('error', '未知错误')}")
        
        results.append(image_data)
    
    # 生成报告
    print("\n" + "=" * 50)
    print("📊 生成结果汇总:")
    
    success_count = sum(1 for r in results if r["success"])
    total_count = len(results)
    
    print(f"✅ 成功: {success_count}/{total_count}")
    print(f"❌ 失败: {total_count - success_count}/{total_count}")
    
    if success_count > 0:
        print("\n📁 生成的图片保存在: promo_images/")
        print("📋 详细信息保存在: generated_images_info.json")
    
    # 创建HTML预览页面
    create_html_preview(results)
    
    print("\n🎉 图片生成完成！")

def create_html_preview(images):
    """创建HTML预览页面"""
    
    html_content = """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>OpenClaw课程宣传图片预览</title>
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
            .subtitle {
                color: #666;
                font-size: 18px;
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
                transition: transform 0.3s ease;
            }
            .image-card:hover {
                transform: translateY(-5px);
            }
            .image-card img {
                width: 100%;
                height: 200px;
                object-fit: cover;
                border-bottom: 1px solid #eee;
            }
            .image-info {
                padding: 15px;
            }
            .image-title {
                font-weight: bold;
                margin-bottom: 8px;
                color: #1d1d1f;
            }
            .image-desc {
                color: #666;
                font-size: 14px;
                margin-bottom: 10px;
            }
            .status {
                display: inline-block;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 12px;
                font-weight: bold;
            }
            .status-success {
                background: #d4edda;
                color: #155724;
            }
            .status-failed {
                background: #f8d7da;
                color: #721c24;
            }
            .prompt {
                background: #f8f9fa;
                padding: 10px;
                border-radius: 6px;
                margin-top: 10px;
                font-size: 12px;
                color: #495057;
                max-height: 100px;
                overflow-y: auto;
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
            <h1>OpenClaw课程宣传图片预览</h1>
            <div class="subtitle">生成时间: """ + datetime.now().strftime("%Y-%m-%d %H:%M") + """</div>
        </div>
        
        <div class="image-grid">
    """
    
    for img in images:
        status_class = "status-success" if img["success"] else "status-failed"
        status_text = "✅ 成功" if img["success"] else "❌ 失败"
        
        image_src = img.get("local_path", "") if img["success"] else "https://via.placeholder.com/300x200?text=生成失败"
        
        html_content += f"""
            <div class="image-card">
                <img src="{image_src}" alt="{img['description']}">
                <div class="image-info">
                    <div class="image-title">{img['description']}</div>
                    <div class="image-desc">{img['name']}</div>
                    <span class="status {status_class}">{status_text}</span>
                    <div class="prompt">{img.get('prompt', '')[:150]}...</div>
                </div>
            </div>
        """
    
    html_content += """
        </div>
        
        <div class="footer">
            <p>OpenClaw课程宣传材料 | 生成工具: DALL-E 3 API</p>
            <p>© 2026 OpenClaw课程团队</p>
        </div>
    </body>
    </html>
    """
    
    with open("promo_images/preview.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print("📄 预览页面已生成: promo_images/preview.html")

if __name__ == "__main__":
    main()