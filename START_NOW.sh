#!/bin/bash
# OpenClaw课程宣传 - 立即启动脚本

echo "🚀 OpenClaw课程宣传启动脚本"
echo "================================"
echo "当前时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# 检查必要文件
echo "📁 检查文件..."
if [ -f "promo_images/GENERATION_PORTAL.html" ]; then
    echo "✅ 图片生成门户: promo_images/GENERATION_PORTAL.html"
else
    echo "❌ 图片生成门户未找到"
fi

if [ -f "promo_quick_start.md" ]; then
    echo "✅ 快速开始指南: promo_quick_start.md"
else
    echo "❌ 快速开始指南未找到"
fi

if [ -f "IMMEDIATE_ACTION_PLAN.md" ]; then
    echo "✅ 立即行动计划: IMMEDIATE_ACTION_PLAN.md"
else
    echo "❌ 立即行动计划未找到"
fi

echo ""
echo "🎯 选择要执行的操作:"
echo "1. 打开图片生成门户"
echo "2. 查看立即行动计划"
echo "3. 查看快速开始指南"
echo "4. 查看所有宣传材料"
echo "5. 开始生成图片工作流"
echo "6. 退出"
echo ""

read -p "请输入选择 (1-6): " choice

case $choice in
    1)
        echo "正在打开图片生成门户..."
        if command -v xdg-open &> /dev/null; then
            xdg-open "promo_images/GENERATION_PORTAL.html"
        elif command -v open &> /dev/null; then
            open "promo_images/GENERATION_PORTAL.html"
        else
            echo "请手动打开: promo_images/GENERATION_PORTAL.html"
        fi
        ;;
    2)
        echo "📋 立即行动计划摘要:"
        echo "========================"
        head -50 IMMEDIATE_ACTION_PLAN.md
        echo ""
        echo "查看完整计划: less IMMEDIATE_ACTION_PLAN.md"
        ;;
    3)
        echo "🚀 快速开始指南摘要:"
        echo "========================"
        head -30 promo_quick_start.md
        echo ""
        echo "查看完整指南: less promo_quick_start.md"
        ;;
    4)
        echo "📚 所有宣传材料清单:"
        echo "========================"
        ls -la *.md *.json *.py 2>/dev/null | grep -E "(promo|guide|plan)" | awk '{print "  " $9}'
        echo ""
        echo "📁 图片生成材料:"
        ls -la promo_images/* 2>/dev/null | awk '{print "  " $9}'
        ;;
    5)
        echo "🎨 开始图片生成工作流"
        echo "========================"
        echo "推荐步骤:"
        echo "1. 访问 https://leonardo.ai"
        echo "2. 注册免费账号"
        echo "3. 使用以下提示词生成图片:"
        echo ""
        echo "📝 关键提示词 (前2张):"
        echo "-----------------------"
        if [ -f "promo_images/leonardo_prompts.md" ]; then
            head -20 promo_images/leonardo_prompts.md
        else
            echo "提示词文件未找到"
        fi
        echo ""
        echo "💡 建议: 先生成封面图和金融实战图"
        ;;
    6)
        echo "退出脚本"
        exit 0
        ;;
    *)
        echo "无效选择"
        ;;
esac

echo ""
echo "================================"
echo "🎉 立即开始行动！"
echo "建议:"
echo "1. 今天上午生成2张关键图片"
echo "2. 今天下午开始预热宣传"
echo "3. 明天正式发布课程"
echo ""
echo "祝推广成功！"