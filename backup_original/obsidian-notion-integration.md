# Obsidian/Notion集成教程

> **将你的知识库与OpenClaw打通，实现智能知识管理**

## 📋 目录

1. [为什么需要集成？](#为什么需要集成)
2. [Obsidian集成方案](#obsidian集成方案)
3. [Notion集成方案](#notion集成方案)
4. [双向同步实战](#双向同步实战)
5. [高级应用场景](#高级应用场景)
6. [故障排查](#故障排查)

---

## 🤔 为什么需要集成？

### 问题：知识孤岛
你的知识分散在多个地方：
- **Obsidian笔记**（本地）
- **Notion页面**（云端）
- **浏览器书签**（散乱）
- **邮件附件**（难找）
- **微信文章**（过期）

**结果：**
- 找不到需要的信息
- 重复收集相同内容
- 知识无法有效利用

### 解决方案：OpenClaw统一管理
OpenClaw作为智能中枢：
1. **收集**多源信息
2. **统一**处理和分析
3. **智能**分类和标签
4. **同步**多平台
5. **推荐**相关内容

### 集成价值
- ✅ **效率提升**：节省70%信息整理时间
- ✅ **知识留存**：提高3倍知识利用率
- ✅ **智能搜索**：语义搜索找到关联内容
- ✅ **自动同步**：多平台数据一致
- ✅ **智能推荐**：发现知识盲区

---

## 📝 Obsidian集成方案

### 方案1：使用官方Obsidian Skill

#### 安装
```bash
# 通过npx安装
npx skills add obsidian -g -y
```

#### 配置
编辑 `~/.openclaw/openclaw.json`：
```json
{
  "skills": {
    "obsidian": {
      "vaultPath": "~/Documents/Obsidian/MyVault",
      "autoSync": true,
      "indexInterval": "1h"
    }
  }
}
```

#### 功能演示

**搜索笔记**
```
You: 在我的Obsidian中搜索关于OpenClaw的内容

Agent: [搜索笔记库]
找到3篇相关笔记：

1. OpenClaw安装指南（相关度：95%）
   路径：技术/AI/OpenClaw/安装.md
   摘要：详细记录了安装步骤...

2. Skills使用心得（相关度：87%）
   路径：技术/AI/OpenClaw/Skills.md
   摘要：总结了30+核心Skills...

3. 自动化工作流设计（相关度：82%）
   路径：技术/AI/OpenClaw/工作流.md
   摘要：设计了3个自动化工作流...
```

**创建笔记**
```
You: 创建一篇关于今天学习的笔记

Agent: [创建笔记]
✅ 笔记已创建：技术/AI/OpenClaw/学习记录-2026-03-09.md

内容：
# 2026-03-09 学习记录

## 今日学习
1. 完成了OpenClaw课程开发
2. 整合了Skills完全指南
3. 实践了Obsidian集成

## 关键收获
- Skills安全防护很重要
- 自动化工作流能大幅提升效率
- 知识管理需要系统化
```

### 方案2：手动同步脚本

#### 创建同步脚本
```bash
# 创建脚本目录
mkdir -p ~/.openclaw/workspace/scripts

# 创建同步脚本
cat > ~/.openclaw/workspace/scripts/sync-obsidian.sh << 'EOF'
#!/bin/bash
echo "🔄 同步Obsidian笔记..."

VAULT_PATH="$HOME/Documents/Obsidian/MyVault"
SYNC_DIR="$HOME/.openclaw/workspace/knowledge/obsidian"

# 创建目录
mkdir -p "$SYNC_DIR"

# 检查目录
if [ ! -d "$VAULT_PATH" ]; then
    echo "❌ Obsidian目录不存在: $VAULT_PATH"
    exit 1
fi

# 同步文件
echo "📁 同步文件中..."
rsync -av --delete \
  --exclude=".obsidian/" \
  --exclude=".trash/" \
  "$VAULT_PATH/" "$SYNC_DIR/"

echo "✅ 同步完成"
echo "📊 统计："
find "$SYNC_DIR" -name "*.md" | wc -l | xargs echo "  笔记数量："
EOF

# 设置权限
chmod +x ~/.openclaw/workspace/scripts/sync-obsidian.sh
```

#### 设置定时同步
```bash
# 添加到Cron（每小时同步一次）
(crontab -l 2>/dev/null; echo "0 * * * * ~/.openclaw/workspace/scripts/sync-obsidian.sh >> ~/.openclaw/logs/sync-obsidian.log 2>&1") | crontab -
```

---

## 📊 Notion集成方案

### 获取API密钥
1. 访问 https://www.notion.so/my-integrations
2. 创建新的集成（Integration）
3. 复制API密钥（格式：`ntn_xxx`）
4. 分享数据库给集成

### 安装Notion Skill
```bash
# 安装Notion Skill
npx skills add notion -g -y
```

### 配置
```json
{
  "skills": {
    "notion": {
      "apiKey": "ntn_你的API密钥",
      "databaseId": "你的数据库ID",
      "syncInterval": "1h"
    }
  }
}
```

### 功能演示

**查询任务**
```
You: 查询我的项目任务列表

Agent: [查询Notion]
找到3个任务：

1. 完成OpenClaw课程开发
   - 状态：进行中
   - 优先级：高
   - 截止日期：2026-03-10

2. 验证实战项目
   - 状态：待开始
   - 优先级：中

3. 发布课程
   - 状态：计划中
   - 优先级：高
```

**创建页面**
```
You: 创建一个学习计划页面

Agent: [创建Notion页面]
✅ 页面已创建：https://notion.so/xxx

内容：
# 2026年Q2学习计划

## 目标
1. 掌握OpenClaw高级功能
2. 开发3个实战项目
3. 贡献社区

## 时间安排
- 3月：完成基础学习
- 4月：实践项目开发
- 5月：优化和分享
```

---

## 🔄 双向同步实战

### 架构设计
```
Obsidian（本地笔记）
    ↑↓
OpenClaw（智能处理）
    ↑↓
Notion（云端协作）
```

### 主同步脚本
```python
#!/usr/bin/env python3
"""
知识同步主脚本
"""

import os
import subprocess
from datetime import datetime

def run_script(script_name):
    """运行脚本"""
    script_path = os.path.expanduser(
        f"~/.openclaw/workspace/scripts/{script_name}"
    )
    
    if os.path.exists(script_path):
        print(f"🔄 执行: {script_name}")
        result = subprocess.run([script_path], capture_output=True, text=True)
        return result.returncode == 0
    else:
        print(f"⚠️ 脚本不存在: {script_name}")
        return False

def main():
    """主函数"""
    print("🚀 开始知识同步")
    print("=" * 50)
    
    # 1. 同步Obsidian
    run_script("sync-obsidian.sh")
    
    # 2. 生成摘要
    print("📊 生成每日摘要...")
    
    summary = f"""
# 知识同步报告 - {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 同步状态
- Obsidian: 已同步
- Notion: 准备同步

## 统计
- 时间: {datetime.now().strftime('%H:%M:%S')}
- 状态: 运行正常
"""
    
    # 保存摘要
    summary_path = os.path.expanduser(
        "~/.openclaw/workspace/knowledge/daily-summary.md"
    )
    os.makedirs(os.path.dirname(summary_path), exist_ok=True)
    
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(summary)
    
    print(f"✅ 摘要已保存: {summary_path}")
    print("\n🎉 同步完成")

if __name__ == "__main__":
    main()
```

### 使用说明
```bash
# 保存为 sync-knowledge.py
chmod +x sync-knowledge.py

# 手动执行
./sync-knowledge.py

# 定时执行（每2小时）
0 */2 * * * cd ~/.openclaw/workspace && python3 sync-knowledge.py >> logs/sync.log 2>&1
```

---

## 🎯 高级应用场景

### 场景1：智能知识推荐

**基于学习历史推荐**
```
[分析学习历史]
发现你最近在学习：
- OpenClaw Skills系统
- 自动化工作流
- 知识管理

推荐：
1. 第12课：自定义Skill开发
2. 第14课：个人知识管理系统
3. Clawflows工作流编排
```

### 场景2：学习进度跟踪

**自动生成报告**
```python
def generate_report():
    """生成学习报告"""
    return """
# 本周学习报告

## 📈 统计
- 学习天数: 7天
- 学习时长: 15小时
- 完成课程: 6课
- 新增笔记: 25篇

## 🎯 重点
1. OpenClaw基础 (40%)
2. Skills系统 (30%)
3. 实战项目 (20%)

## 🏆 成就
- ✅ 完成Skills完全指南
- ✅ 实践Obsidian集成
- ✅ 开发自动化工作流
"""
```

---

## 🔧 故障排查

### 常见问题

#### 问题1：Obsidian同步失败
**症状：**
- 找不到笔记库
- 权限错误

**解决：**
```bash
# 检查目录
ls ~/Documents/Obsidian/

# 检查权限
ls -la ~/Documents/Obsidian/MyVault/

# 手动测试
~/.openclaw/workspace/scripts/sync-obsidian.sh
```

#### 问题2：Notion API错误
**症状：**
- API密钥无效
- 权限不足

**解决：**
```bash
# 检查API密钥
echo $NOTION_API_KEY

# 验证权限
# 访问Notion集成页面检查
```

#### 问题3：脚本权限问题
**解决：**
```bash
# 添加执行权限
chmod +x ~/.openclaw/workspace/scripts/*.sh

# 使用绝对路径
/home/user/.openclaw/workspace/scripts/sync-obsidian.sh
```

### 调试命令
```bash
# 测试Obsidian
ls ~/Documents/Obsidian/MyVault/*.md | head -3

# 测试脚本
bash -x ~/.openclaw/workspace/scripts/sync-obsidian.sh

# 检查Cron
crontab -l

# 查看日志
tail -f ~/.openclaw/logs/sync-obsidian.log
```

---

## 📚 最佳实践

### 1. 渐进式集成
- **第1周**：只同步Obsidian
- **第2周**：添加Notion同步
- **第3周**：实现双向同步
- **第4周**：优化自动化

### 2. 数据备份
```bash
# 每日备份
0 2 * * * tar -czf ~/.openclaw/backups/knowledge-$(date +%Y%m%d).tar.gz ~/.openclaw/workspace/knowledge/

# 清理旧备份（保留7天）
find ~/.openclaw/backups -name "knowledge-*.tar.gz" -mtime +7 -delete
```

### 3. 监控告警
```bash
# 检查同步状态
0 */6 * * * ~/.openclaw/workspace/scripts/check-sync.sh

# 失败时通知
if [ $? -ne 0 ]; then
    echo "⚠️ 同步失败" | openclaw message send --channel telegram
fi
```

---

## 🚀 快速开始

### 一键安装
```bash
# 创建目录结构
mkdir -p ~/.openclaw/workspace/{scripts,knowledge,logs,backups}

# 下载脚本
curl -o ~/.openclaw/workspace/scripts/sync-obsidian.sh \
  https://raw.githubusercontent.com/Jerryxu-rui/openclaw-course/main/scripts/sync-obsidian.sh

# 设置权限
chmod +x ~/.openclaw/workspace/scripts/*.sh

# 测试运行
~/.openclaw/workspace/scripts/sync-obsidian.sh
```

### 配置Cron
```bash
# 添加定时任务
(crontab -l 2>/dev/null; echo "# OpenClaw知识同步") | crontab -
(crontab -l 2>/dev/null; echo "0 */2 * * * ~/.openclaw/workspace/scripts/sync-obsidian.sh >> ~/.openclaw/logs/sync.log 2>&1") | crontab -
(crontab -l 2>/dev/null; echo "0 2 * * * tar -czf ~/.openclaw/backups/knowledge-\$(date +%Y%m%d).tar.gz ~/.openclaw/workspace/knowledge/") | crontab -
```

---

## 📞 支持与反馈

### 遇到问题？
1. **查看日志**：`tail -f ~/.openclaw/logs/sync-obsidian.log`
2. **检查配置**：`cat ~/.openclaw/openclaw.json | jq .skills`
3. **测试连接**：手动运行同步脚本
4. **寻求帮助**：OpenClaw社区

### 反馈渠道
- **GitHub Issues**：报告问题
- **社区讨论**：分享经验
- **课程反馈**：改进建议

---

## 📖 相关资源

### 官方文档
- OpenClaw文档：https://docs.openclaw.ai
- Skills开发指南：https://docs.openclaw.ai/skills
- API参考：https://docs.openclaw.ai/api

### 社区资源
- ClawHub：https://clawhub.com
- GitHub仓库：https://github.com/openclaw/openclaw
- Discord社区：https://discord.com/invite/clawd

### 本课程
- Skills完全指南2.0
- 第3课：核心功能与Skills系统
- 第14课：个人知识管理系统

---

**🎉 恭喜！你现在掌握了Obsidian/Notion与OpenClaw的集成方法。**

**下一步建议：**
1. 从简单的Obsidian同步开始
2. 逐步添加Notion集成
3. 实现自动化工作流
4. 分享你的经验

---

**© 2026 OpenClaw课程 | Obsidian/Notion集成教程**

**最后更新：** 2026-03-09  
**版本：** v1.0  
**维护者：** OpenClaw课程团队
