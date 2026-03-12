#!/usr/bin/env python3
"""
使用Gemini API生成课程宣传文案 - 简化版本
"""

import requests
import json

def generate_with_gemini(prompt):
    """使用Gemini API生成内容"""
    
    API_KEY = "AIzaSyC0SyDgrI8nRfWlCw78duUzcmxWFteecdU"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={API_KEY}"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    data = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        if "candidates" in result and len(result["candidates"]) > 0:
            return result["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return "生成失败：API返回格式错误"
            
    except Exception as e:
        return f"生成失败：{str(e)}"

def generate_promo_content():
    """生成宣传文案"""
    
    prompt = """
    请为OpenClaw课程生成宣传文案和图片描述。
    
    课程信息：
    - 课程名称：OpenClaw完整课程体系
    - 课程口号：从零到一，打造你的专属AI助手生态
    - 课程特点：实战导向、成本优化、生产级实践
    - 目标学员：开发者、产品经理、AI从业者、投资者
    
    课程亮点：
    1. 国内首个系统性OpenClaw课程
    2. 实战经验总结（基于高强度使用经验）
    3. 成本优化专家（如何用最少的钱获得最好的效果）
    4. 生产级部署（不是玩具，是真正可用的系统）
    5. 金融实战案例（智能体金融+智能股票分析）
    
    请生成：
    1. 课程宣传标语（3-5个版本）
    2. 社交媒体宣传文案（适合微博、微信朋友圈）
    3. 课程亮点描述（用于宣传页面）
    4. 宣传图片描述（用于AI生成图片，描述课程核心场景）
    5. 目标学员吸引文案
    
    要求：简洁有力，突出实战和金融特色，吸引技术用户和投资者。
    """
    
    return generate_with_gemini(prompt)

def generate_image_prompts():
    """生成图片提示词"""
    
    prompt = """
    为OpenClaw课程生成5个宣传图片的AI生成提示词。
    
    课程主题：AI助手开发 + 金融实战
    风格要求：现代、科技感、专业、简洁
    
    需要5个不同的场景：
    1. 课程封面图：突出"从零到一，打造AI助手生态"主题
    2. 技术架构图：展示OpenClaw的技术栈和架构
    3. 金融实战场景：展示智能体金融交易界面
    4. 股票分析场景：展示智能股票分析系统
    5. 学习成果图：展示学员学完后的技能提升
    
    每个提示词需要：
    - 英文描述（适合AI生成）
    - 中文说明（场景描述）
    - 风格建议（色彩、构图等）
    
    要求：专业、美观、有吸引力，适合用于课程宣传。
    """
    
    return generate_with_gemini(prompt)

def main():
    print("正在生成OpenClaw课程宣传内容...")
    print("=" * 50)
    
    # 生成宣传文案
    print("\n📝 宣传文案生成结果：")
    promo_content = generate_promo_content()
    print(promo_content)
    
    print("\n" + "=" * 50)
    
    # 生成图片提示词
    print("\n🎨 宣传图片提示词：")
    image_prompts = generate_image_prompts()
    print(image_prompts)
    
    # 保存结果
    output = {
        "promo_content": promo_content,
        "image_prompts": image_prompts,
        "generated_at": "2026-03-12"
    }
    
    with open("./openclaw-course/promo_content.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print("\n✅ 内容已保存到 promo_content.json")

if __name__ == "__main__":
    main()