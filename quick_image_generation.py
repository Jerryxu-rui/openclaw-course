#!/usr/bin/env python3
"""
快速图片生成工具 - 提供多种生成方案
"""

import os
import json
from datetime import datetime

# 图片配置
IMAGE_CONFIGS = [
    {
        "name": "course_cover",
        "prompt": "A modern, sleek cover design for an AI assistant course. The title 'OpenClaw Complete Course System' is prominently displayed with a tagline 'From Zero to One, Build Your AI Assistant Ecosystem'. The background features abstract circuit patterns blending with financial charts, representing the fusion of AI and finance. Color scheme: blue and purple gradients with gold accents. Style: professional, tech-focused, clean layout.",
        "description": "课程封面图",
        "size": "1024x1024"
    },
    {
        "name": "tech_architecture",
        "prompt": "An infographic showing the OpenClaw technology stack and architecture. The diagram includes layers: User Interface (Feishu, Telegram, Web), Gateway Layer, Agent System, Model Layer (Claude, GPT, Gemini, DeepSeek), Skills Ecosystem, and Memory System. Arrows show data flow between components. Style: clean technical diagram with icons for each component, monochromatic blue color scheme with highlights.",
        "description": "技术架构图",
        "size": "1024x1024"
    },
    {
        "name": "finance_trading",
        "prompt": "A futuristic trading interface for agentic finance. Multiple screens show Polymarket prediction markets, real-time trading signals, risk metrics, and profit/loss charts. AI agents are visualized as glowing orbs analyzing data streams. The scene has a dark theme with neon blue and green highlights, representing the high-tech nature of algorithmic trading.",
        "description": "金融实战场景图",
        "size": "1024x1024"
    },
    {
        "name": "stock_analysis",
        "prompt": "A smart stock analysis dashboard. The interface displays real-time stock charts with technical indicators (moving averages, RSI, MACD), fundamental data tables, risk assessment metrics, and automated report generation. AI is analyzing patterns and generating buy/sell signals. Style: professional financial software interface, clean white background with data visualizations in corporate blue and green.",
        "description": "股票分析场景图",
        "size": "1024x1024"
    },
    {
        "name": "learning_outcomes",
        "prompt": "A before-and-after comparison showing skill transformation. Left side: a person overwhelmed with manual tasks (emails, reports, data analysis). Right side: the same person efficiently managing everything through AI assistants, with dashboards showing productivity metrics improved by 300%. Style: inspirational, positive, showing tangible results, warm color palette with gold accents for achievement.",
        "description": "学习成果对比图",
        "size": "1024x1024"
    }
]

def create_generation_guides():
    """创建生成指南"""
    
    # 创建目录
    os.makedirs("promo_images", exist_ok=True)
    
    # 1. 创建Midjourney提示词文件
    midjourney_prompts = "# Midjourney 提示词\n\n"
    midjourney_prompts += "在Discord中使用 /imagine 命令，添加参数：--ar 16:9 --style raw\n\n"
    
    for config in IMAGE_CONFIGS:
        midjourney_prompts += f"## {config['description']}\n"
        midjourney_prompts += f"```\n{config['prompt']} --ar 16:9 --style raw\n```\n\n"
    
    with open("promo_images/midjourney_prompts.md", "w", encoding="utf-8") as f:
        f.write(midjourney_prompts)
    
    # 2. 创建Leonardo.ai提示词文件
    leonardo_prompts = "# Leonardo.ai 提示词\n\n"
    leonardo_prompts += "访问 https://leonardo.ai，注册免费账号后使用以下提示词：\n\n"
    
    for config in IMAGE_CONFIGS:
        leonardo_prompts += f"## {config['description']}\n"
        leonardo_prompts += f"**提示词**: {config['prompt']}\n"
        leonardo_prompts += f"**尺寸**: {config['size']}\n"
        leonardo_prompts += f"**模型推荐**: Leonardo Diffusion XL\n\n"
    
    with open("promo_images/leonardo_prompts.md", "w", encoding="utf-8") as f:
        f.write(leonardo_prompts)
    
    # 3. 创建Bing Image Creator提示词文件
    bing_prompts = "# Bing Image Creator 提示词\n\n"
    bing_prompts += "访问 https://www.bing.com/images/create，使用微软账号登录\n\n"
    
    for config in IMAGE_CONFIGS:
        bing_prompts += f"## {config['description']}\n"
        bing_prompts += f"{config['prompt']}\n\n"
    
    with open("promo_images/bing_prompts.md", "w", encoding="utf-8") as f:
        f.write(bing_prompts)
    
    # 4. 创建综合指南
    guide_content = f"""# OpenClaw课程宣传图片生成指南

生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M")}

## 🎯 生成目标
需要生成5张专业级宣传图片，用于课程推广。

## 📋 图片清单

"""
    
    for i, config in enumerate(IMAGE_CONFIGS, 1):
        guide_content += f"""### {i}. {config['description']}
- **文件名**: {config['name']}.png
- **尺寸**: {config['size']}
- **用途**: {config['description'].replace('图', '')}
- **优先级**: {'高' if i <= 2 else '中'}

**英文提示词**:
```
{config['prompt']}
```

**中文说明**:
{config['description']}，{config['size']}尺寸，专业品质

---

"""
    
    guide_content += """## 🛠️ 生成工具推荐

### 1. Leonardo.ai (推荐)
- **网址**: https://leonardo.ai
- **优点**: 免费额度充足，质量好，易用
- **步骤**:
  1. 注册免费账号
  2. 选择"AI Image Generation"
  3. 输入提示词
  4. 选择模型: Leonardo Diffusion XL
  5. 生成并下载

### 2. Bing Image Creator (免费)
- **网址**: https://www.bing.com/images/create
- **优点**: 完全免费，无需付费
- **步骤**:
  1. 使用微软账号登录
  2. 输入提示词
  3. 等待生成
  4. 下载图片

### 3. Midjourney (最高质量)
- **网址**: 需要在Discord中使用
- **优点**: 质量最高，专业级
- **步骤**:
  1. 加入Midjourney Discord
  2. 在频道中使用 /imagine 命令
  3. 输入提示词 + --ar 16:9 --style raw
  4. 等待生成并下载

## 🚀 快速开始方案

### 方案A: 快速生成 (今天完成)
1. 使用Leonardo.ai生成封面图和金融实战图
2. 今天下午开始预热宣传
3. 明天生成其余图片

### 方案B: 高质量生成 (1-2天完成)
1. 使用Midjourney生成所有5张图片
2. 确保最高质量
3. 明天正式发布时使用

### 方案C: 混合方案
1. 今天用免费工具生成2张关键图片
2. 开始预热宣传
3. 同时用高级工具生成其余图片

## 📁 文件结构
```
promo_images/
├── course_cover.png      # 封面图 (最高优先级)
├── finance_trading.png   # 金融实战图 (高优先级)
├── tech_architecture.png # 技术架构图
├── stock_analysis.png    # 股票分析图
├── learning_outcomes.png # 学习成果图
└── 各种提示词文件
```

## ⏱️ 时间建议
- **今天上午**: 生成封面图和金融实战图
- **今天下午**: 开始预热宣传，使用生成的图片
- **今天晚上**: 生成其余3张图片
- **明天上午**: 正式发布，使用完整图片集

## 💡 专业建议
1. **保持一致性**: 所有图片使用相似的色彩风格
2. **品牌识别**: 确保OpenClaw品牌元素清晰
3. **专业品质**: 不要使用低质量图片
4. **优化尺寸**: 社交媒体使用1200x630，网站使用1920x1080

## 📞 如有问题
- 查看详细提示词文件
- 尝试不同生成工具
- 调整提示词优化效果

---
**指南版本**: v1.0
**生成时间**: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """
**状态**: ✅ 准备就绪
"""
    
    with open("promo_images/COMPLETE_GUIDE.md", "w", encoding="utf-8") as f:
        f.write(guide_content)
    
    # 5. 创建HTML预览页面
    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OpenClaw课程宣传图片生成</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
        }}
        .container {{
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }}
        .header {{
            text-align: center;
            margin-bottom: 40px;
            padding-bottom: 20px;
            border-bottom: 3px solid #f0f0f0;
        }}
        h1 {{
            color: #0066cc;
            font-size: 36px;
            margin-bottom: 10px;
        }}
        .subtitle {{
            color: #666;
            font-size: 18px;
        }}
        .priority-badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
            margin-left: 10px;
        }}
        .high-priority {{
            background: #ff6b6b;
            color: white;
        }}
        .medium-priority {{
            background: #ffd93d;
            color: #333;
        }}
        .image-card {{
            background: #f8f9fa;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            border-left: 5px solid #0066cc;
        }}
        .image-title {{
            font-size: 20px;
            font-weight: bold;
            color: #1d1d1f;
            margin-bottom: 10px;
        }}
        .prompt-box {{
            background: white;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            line-height: 1.5;
            max-height: 150px;
            overflow-y: auto;
        }}
        .tool-card {{
            background: #e7f5ff;
            border-radius: 12px;
            padding: 20px;
            margin: 20px 0;
            border: 2px solid #339af0;
        }}
        .action-button {{
            display: inline-block;
            background: #0066cc;
            color: white;
            padding: 12px 24px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: bold;
            margin: 10px 5px;
            transition: all 0.3s;
        }}
        .action-button:hover {{
            background: #0052a3;
            transform: translateY(-2px);
        }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #eee;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎨 OpenClaw课程宣传图片生成</h1>
            <div class="subtitle">5张专业宣传图片 | 立即开始生成</div>
            <div style="margin-top: 20px;">
                <a href="#images" class="action-button">查看图片需求</a>
                <a href="#tools" class="action-button">选择生成工具</a>
                <a href="#start" class="action-button">立即开始</a>
            </div>
        </div>
        
        <div id="images">
            <h2>📋 需要生成的图片</h2>
"""
    
    for i, config in enumerate(IMAGE_CONFIGS, 1):
        priority_class = "high-priority" if i <= 2 else "medium-priority"
        priority_text = "高优先级" if i <= 2 else "中优先级"
        
        html_content += f"""
            <div class="image-card">
                <div class="image-title">
                    {i}. {config['description']}
                    <span class="priority-badge {priority_class}">{priority_text}</span>
                </div>
                <div><strong>文件名:</strong> {config['name']}.png</div>
                <div><strong>尺寸:</strong> {config['size']}</div>
                <div style="margin-top: 10px;"><strong>提示词:</strong></div>
                <div class="prompt-box">{config['prompt']}</div>
            </div>
        """
    
    html_content += """
        </div>
        
        <div id="tools" class="tool-card">
            <h2>🛠️ 推荐生成工具</h2>
            <h3>1. Leonardo.ai (最推荐)</h3>
            <p><strong>优点:</strong> 免费额度充足，质量好，易用</p>
            <p><strong>步骤:</strong> 注册 → 选择AI Image Generation → 输入提示词 → 生成</p>
            <a href="https://leonardo.ai" target="_blank" class="action-button">访问 Leonardo.ai</a>
            
            <h3>2. Bing Image Creator (完全免费)</h3>
            <p><strong>优点:</strong> 无需付费，微软账号即可</p>
            <p><strong>步骤:</strong> 登录 → 输入提示词 → 等待生成</p>
            <a href="https://www.bing.com/images/create" target="_blank" class="action-button">访问 Bing Image Creator</a>
            
            <h3>3. Midjourney (最高质量)</h3>
            <p><strong>优点:</strong> 专业级质量，效果最好</p>
            <p><strong>步骤:</strong> Discord中使用 /imagine 命令</p>
        </div>
        
        <div id="start">
            <h2>🚀 立即开始</h2>
            <h3>快速方案 (今天完成):</h3>
            <ol>
                <li>使用Leonardo.ai生成<strong>封面图</strong>和<strong>金融实战图</strong></li>
                <li>保存为PNG格式到 <code>promo_images/</code> 文件夹</li>
                <li>今天下午开始预热宣传</li>
                <li>明天生成其余图片并正式发布</li>
            </ol>
            
            <div style="background: #d4edda; padding: 20px; border-radius: 8px; margin: 20px 0;">
                <h3 style="color: #155724; margin-top: 0;">💡 专业建议</h3>
                <ul>
                    <li><strong>先行动再完美:</strong> 先生成2张关键图片开始宣传</li>
                    <li><strong>保持品牌一致:</strong> 所有图片使用蓝紫色调</li>
                    <li><strong>优化尺寸:</strong> 社交媒体用1200x630，网站用1920x1080</li>
                    <li><strong>测试效果:</strong> 发布后观察用户反馈</li>
                </ul>
            </div>
        </div>
        
        <div class="footer">
            <p>OpenClaw课程宣传材料生成系统</p>
            <p>生成时间: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
            <p>© 2026 OpenClaw课程团队 | 所有提示词已准备就绪</p>
        </div>
    </div>
</body>
</html>
"""
    
    with open("promo_images/GENERATION_PORTAL.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print("✅ 生成指南已创建完成！")
    print("\n📁 生成的文件:")
    print("  - promo_images/midjourney_prompts.md      # Midjourney提示词")
    print("  - promo_images/leonardo_prompts.md       # Leonardo.ai提示词")
    print("  - promo_images/bing_prompts.md           # Bing Image Creator提示词")
    print("  - promo_images/COMPLETE_GUIDE.md         # 完整生成指南")
    print("  - promo_images/GENERATION_PORTAL.html    # HTML生成门户")
    
    print("\n🚀 下一步:")
    print("  1. 打开 promo_images/GENERATION_PORTAL.html")
    print("  2. 选择生成工具")
    print("  3. 开始生成图片！")

def main():
    """主函数"""
    print("🎨 OpenClaw课程宣传图片生成指南创建工具")
    print("=" * 60)
    print("正在创建完整的图片生成指南...")
    
    create_generation_guides()
    
    print("\n" + "=" * 60)
    print("✅ 所有指南已创建完成！")
    print("现在你可以:")
    print("1. 使用免费工具生成图片")
    print("2. 开始预热宣传")
    print("3. 准备正式发布")

if __name__ == "__main__":
    main()