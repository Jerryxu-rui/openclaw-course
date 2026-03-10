# 第14课：综合项目1 - 个人知识管理系统

## 项目概述

**项目名称：** SmartKnowledge - 智能知识管理系统  
**项目时长：** 120分钟  
**难度等级：** ⭐⭐⭐⭐  
**适合人群：** 完成前13课的学员

### 项目目标
构建一个完整的个人知识管理系统，实现：
- 自动收集多源信息
- 智能分类与标签
- 知识提取与总结
- 定期复习提醒
- 多平台同步

---

## 第一部分：需求分析（20分钟）

### 1.1 用户故事

**作为一个知识工作者，我希望：**
1. 自动收集我关注的信息源（RSS/邮件/网页）
2. 系统能自动分类和打标签
3. 生成简洁的摘要，节省阅读时间
4. 定期提醒我复习重要内容
5. 在多个平台（本地/飞书/Notion）同步

### 1.2 功能需求

#### 核心功能
```
1. 信息收集
   - RSS订阅监控
   - 邮件自动抓取
   - 浏览器书签同步
   - 手动添加文档

2. 智能处理
   - 内容提取（去广告）
   - 自动分类（技术/生活/工作）
   - 标签生成（关键词提取）
   - 摘要生成（AI总结）

3. 知识存储
   - 本地Markdown文件
   - 飞书知识库
   - 向量数据库（语义搜索）

4. 知识应用
   - 全文搜索
   - 语义搜索
   - 定期复习提醒
   - 知识图谱可视化
```

#### 非功能需求
```
- 性能：处理速度 < 5秒/篇
- 可靠性：99%成功率
- 可用性：7x24小时运行
- 成本：< $10/月
```

### 1.3 技术选型

```
核心技术：
- OpenClaw（AI处理）
- Markdown（知识存储）
- 飞书API（云端同步）
- Jina AI（向量搜索）

辅助工具：
- feedparser（RSS解析）
- BeautifulSoup（网页提取）
- SQLite（元数据存储）
```

---

## 第二部分：系统设计（30分钟）

### 2.1 系统架构

```
┌─────────────────────────────────────────────┐
│              信息源层                        │
├─────────────────────────────────────────────┤
│  RSS订阅  │  Gmail  │  浏览器  │  手动上传  │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│            OpenClaw处理层                    │
├─────────────────────────────────────────────┤
│  内容提取  │  分类  │  标签  │  摘要生成    │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│              存储层                          │
├─────────────────────────────────────────────┤
│  本地MD  │  飞书  │  向量DB  │  元数据DB   │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│              应用层                          │
├─────────────────────────────────────────────┤
│  搜索  │  复习  │  统计  │  可视化         │
└─────────────────────────────────────────────┘
```

### 2.2 数据模型

#### 知识条目（Article）
```json
{
  "id": "uuid",
  "title": "文章标题",
  "url": "原始链接",
  "source": "来源（rss/email/bookmark）",
  "content": "正文内容",
  "summary": "AI生成的摘要",
  "category": "分类（tech/life/work）",
  "tags": ["标签1", "标签2"],
  "created_at": "2026-03-09T10:00:00Z",
  "reviewed_at": null,
  "review_count": 0,
  "importance": 3,
  "status": "unread"
}
```

#### 分类体系
```
技术（tech）
├─ AI/ML
├─ 编程语言
├─ 工具效率
└─ 架构设计

生活（life）
├─ 健康
├─ 理财
└─ 兴趣爱好

工作（work）
├─ 项目管理
├─ 团队协作
└─ 职业发展
```

### 2.3 工作流设计

#### 流程1：自动收集
```
[定时触发：每2小时]
  ↓
[检查RSS更新]
  ↓
[提取新文章]
  ↓
[去重检查]
  ↓
[保存到待处理队列]
```

#### 流程2：智能处理
```
[从队列取出文章]
  ↓
[提取正文（去广告）]
  ↓
[AI分类]
  ↓
[AI生成标签]
  ↓
[AI生成摘要]
  ↓
[保存到知识库]
  ↓
[生成向量嵌入]
  ↓
[通知用户]
```

#### 流程3：定期复习
```
[每周日20:00触发]
  ↓
[查询本周新增知识]
  ↓
[查询待复习知识]
  ↓
[生成复习清单]
  ↓
[发送到Telegram]
```

---

## 第三部分：实现步骤（50分钟）

### 3.1 环境准备

#### 创建项目目录
```bash
mkdir -p ~/.openclaw/workspace/knowledge-system
cd ~/.openclaw/workspace/knowledge-system

# 创建目录结构
mkdir -p {config,data,scripts,knowledge/{tech,life,work}}
```

#### 配置文件
```bash
# config/sources.json
cat > config/sources.json << 'EOF'
{
  "rss": [
    {
      "name": "Hacker News",
      "url": "https://news.ycombinator.com/rss",
      "category": "tech"
    },
    {
      "name": "OpenClaw Blog",
      "url": "https://blog.openclaw.ai/feed",
      "category": "tech"
    }
  ],
  "email": {
    "enabled": true,
    "labels": ["学习", "技术", "AI"],
    "max_age_days": 7
  },
  "bookmarks": {
    "enabled": false,
    "browser": "chrome"
  }
}
EOF
```

### 3.2 实现信息收集

#### RSS收集脚本
```bash
# scripts/collect_rss.sh
cat > scripts/collect_rss.sh << 'EOF'
#!/bin/bash

# RSS收集脚本

SOURCES_FILE="config/sources.json"
DATA_DIR="data/queue"

mkdir -p "$DATA_DIR"

# 读取RSS源并收集
openclaw chat << 'PROMPT'
读取 config/sources.json 中的RSS源
对每个RSS源：
1. 抓取最新文章（最近24小时）
2. 提取：标题、链接、发布时间
3. 保存到 data/queue/rss_YYYYMMDD.json

格式：
{
  "articles": [
    {
      "title": "...",
      "url": "...",
      "source": "Hacker News",
      "category": "tech",
      "published_at": "2026-03-09T10:00:00Z"
    }
  ]
}
PROMPT

echo "✅ RSS收集完成"
EOF

chmod +x scripts/collect_rss.sh
```

#### 邮件收集脚本
```bash
# scripts/collect_email.sh
cat > scripts/collect_email.sh << 'EOF'
#!/bin/bash

# 邮件收集脚本

openclaw chat << 'PROMPT'
检查Gmail中的邮件：
- 标签：学习、技术、AI
- 时间：最近7天
- 状态：未读

对每封邮件：
1. 提取：标题、正文、发件人、时间
2. 判断是否包含有价值的内容
3. 如果有价值，保存到 data/queue/email_YYYYMMDD.json

格式同RSS
PROMPT

echo "✅ 邮件收集完成"
EOF

chmod +x scripts/collect_email.sh
```

### 3.3 实现智能处理

#### 处理脚本
```bash
# scripts/process_articles.sh
cat > scripts/process_articles.sh << 'EOF'
#!/bin/bash

# 文章处理脚本

QUEUE_DIR="data/queue"
KNOWLEDGE_DIR="knowledge"

for file in "$QUEUE_DIR"/*.json; do
    [ -f "$file" ] || continue
    
    openclaw chat << PROMPT
处理文章队列：$file

对每篇文章：
1. 提取正文（使用web_fetch）
2. AI分类（tech/life/work + 子分类）
3. AI生成标签（3-5个关键词）
4. AI生成摘要（100-200字）
5. 保存到对应分类目录

文件命名：
knowledge/{category}/{subcategory}/YYYYMMDD-{title-slug}.md

Markdown格式：
---
title: 文章标题
url: 原始链接
source: 来源
category: 分类
tags: [标签1, 标签2]
created_at: 2026-03-09T10:00:00Z
---

# 文章标题

## 摘要
[AI生成的摘要]

## 正文
[提取的正文]

## 标签
#标签1 #标签2

## 来源
[原始链接]
PROMPT

    # 处理完成后移动到已处理目录
    mv "$file" "$QUEUE_DIR/processed/"
done

echo "✅ 文章处理完成"
EOF

chmod +x scripts/process_articles.sh
```

### 3.4 配置自动化

#### Heartbeat配置
```markdown
# ~/.openclaw/workspace/HEARTBEAT.md

## 知识收集（每2小时）

执行脚本：
1. ~/.openclaw/workspace/knowledge-system/scripts/collect_rss.sh
2. ~/.openclaw/workspace/knowledge-system/scripts/collect_email.sh

如有新文章：
- 通知：发现X篇新文章
- 返回：HEARTBEAT_OK

如无新文章：
- 返回：HEARTBEAT_OK
```

#### Cron配置
```json
{
  "automation": {
    "cron": {
      "jobs": [
        {
          "name": "process-articles",
          "schedule": "0 */3 * * *",
          "task": "执行 ~/.openclaw/workspace/knowledge-system/scripts/process_articles.sh",
          "enabled": true
        },
        {
          "name": "weekly-review",
          "schedule": "0 20 * * 0",
          "task": "生成本周知识复习清单",
          "enabled": true
        }
      ]
    }
  }
}
```

### 3.5 实现搜索功能

#### 全文搜索
```bash
# scripts/search.sh
cat > scripts/search.sh << 'EOF'
#!/bin/bash

QUERY="$1"
KNOWLEDGE_DIR="knowledge"

if [ -z "$QUERY" ]; then
    echo "用法: ./search.sh <关键词>"
    exit 1
fi

echo "🔍 搜索：$QUERY"
echo ""

# 使用grep搜索
grep -r -i "$QUERY" "$KNOWLEDGE_DIR" --include="*.md" | \
    head -20 | \
    while IFS=: read -r file line; do
        echo "📄 $file"
        echo "   $line"
        echo ""
    done
EOF

chmod +x scripts/search.sh
```

#### 语义搜索
```bash
openclaw chat << 'PROMPT'
实现语义搜索功能：

1. 使用memory_search搜索知识库
2. 返回最相关的5篇文章
3. 显示：标题、摘要、相关度

示例：
You: 搜索关于OpenClaw成本优化的内容

Agent: [使用memory_search]
找到5篇相关文章：

1. OpenClaw成本优化实战（相关度：95%）
   摘要：通过记忆蒸馏和模型选择...
   
2. 模型选择策略（相关度：87%）
   摘要：不同模型的成本对比...
PROMPT
```

### 3.6 实现复习提醒

#### 复习脚本
```bash
# scripts/weekly_review.sh
cat > scripts/weekly_review.sh << 'EOF'
#!/bin/bash

KNOWLEDGE_DIR="knowledge"
REPORT_FILE="data/review_$(date +%Y%m%d).md"

openclaw chat << PROMPT
生成本周知识复习报告：

1. 统计本周新增文章数量（按分类）
2. 列出重要文章（importance >= 4）
3. 列出待复习文章（review_count < 2）
4. 生成学习建议

保存到：$REPORT_FILE

然后发送到Telegram
PROMPT

echo "✅ 复习报告已生成：$REPORT_FILE"
EOF

chmod +x scripts/weekly_review.sh
```

---

## 第四部分：测试与优化（15分钟）

### 4.1 功能测试

#### 测试清单
```markdown
## 信息收集测试
- [ ] RSS收集正常
- [ ] 邮件收集正常
- [ ] 去重功能正常

## 智能处理测试
- [ ] 正文提取准确
- [ ] 分类准确率 > 90%
- [ ] 标签相关性高
- [ ] 摘要质量好

## 存储测试
- [ ] 本地文件保存正常
- [ ] 飞书同步成功
- [ ] 向量搜索可用

## 应用测试
- [ ] 全文搜索快速
- [ ] 语义搜索准确
- [ ] 复习提醒及时
```

### 4.2 性能优化

#### 优化策略
```
1. 批量处理
   - 每次处理10篇文章
   - 减少API调用次数

2. 缓存机制
   - 缓存已处理的URL
   - 避免重复处理

3. 异步处理
   - 收集和处理分离
   - 使用队列机制

4. 成本控制
   - 使用便宜模型处理简单任务
   - 仅复杂任务使用贵模型
```

### 4.3 监控与告警

```bash
# scripts/monitor.sh
cat > scripts/monitor.sh << 'EOF'
#!/bin/bash

# 监控脚本

# 检查队列积压
QUEUE_COUNT=$(ls data/queue/*.json 2>/dev/null | wc -l)
if [ "$QUEUE_COUNT" -gt 50 ]; then
    openclaw message send --channel telegram \
        --message "⚠️ 知识系统：队列积压${QUEUE_COUNT}篇文章"
fi

# 检查今日处理量
TODAY=$(date +%Y%m%d)
PROCESSED_TODAY=$(find knowledge -name "${TODAY}*.md" | wc -l)
echo "📊 今日已处理：${PROCESSED_TODAY}篇"

# 检查磁盘空间
DISK_USAGE=$(df -h knowledge | awk 'NR==2 {print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -gt 80 ]; then
    openclaw message send --channel telegram \
        --message "⚠️ 知识系统：磁盘使用率${DISK_USAGE}%"
fi
EOF

chmod +x scripts/monitor.sh
```

---

## 第五部分：部署与使用（5分钟）

### 5.1 部署清单

```markdown
## 部署前检查
- [ ] OpenClaw已安装
- [ ] 配置文件已创建
- [ ] 脚本权限已设置
- [ ] Heartbeat已配置
- [ ] Cron任务已设置

## 首次运行
1. 手动执行收集脚本测试
2. 手动执行处理脚本测试
3. 检查生成的文件
4. 验证搜索功能
5. 测试复习提醒

## 日常维护
- 每周检查队列积压
- 每月清理旧文件
- 定期备份知识库
- 优化分类体系
```

### 5.2 使用指南

#### 日常使用
```bash
# 手动添加文章
openclaw chat "添加文章到知识库：https://example.com/article"

# 搜索知识
./scripts/search.sh "OpenClaw"

# 查看统计
openclaw chat "统计知识库：按分类显示文章数量"

# 生成复习清单
./scripts/weekly_review.sh
```

#### 高级功能
```bash
# 导出知识库
tar -czf knowledge-backup-$(date +%Y%m%d).tar.gz knowledge/

# 同步到飞书
openclaw chat "同步knowledge/tech目录到飞书知识库"

# 生成知识图谱
openclaw chat "分析knowledge目录，生成知识图谱"
```

---

## 第六部分：扩展功能（可选）

### 6.1 知识图谱

```
实现知识之间的关联：
- 提取文章中的实体（人名、技术、概念）
- 建立实体之间的关系
- 可视化展示

工具：
- NetworkX（图计算）
- Pyvis（可视化）
```

### 6.2 智能推荐

```
基于已有知识推荐新内容：
- 分析用户阅读偏好
- 推荐相关文章
- 发现知识盲区

算法：
- 协同过滤
- 内容相似度
- 主题模型
```

### 6.3 多人协作

```
团队知识共享：
- 共享知识库
- 协作标注
- 评论讨论

平台：
- 飞书知识库
- Notion
- Confluence
```

---

## 项目交付物

### 必需交付
1. ✅ 完整的项目代码
2. ✅ 配置文件
3. ✅ 部署文档
4. ✅ 使用手册

### 可选交付
5. 演示视频
6. 效果报告
7. 优化建议
8. 扩展计划

---

## 评估标准

### 功能完整性（40分）
- 信息收集：10分
- 智能处理：15分
- 知识存储：10分
- 应用功能：5分

### 自动化程度（30分）
- 自动收集：10分
- 自动处理：10分
- 自动提醒：10分

### 用户体验（20分）
- 界面友好：5分
- 响应速度：5分
- 搜索准确：10分

### 文档质量（10分）
- 代码注释：3分
- 部署文档：4分
- 使用手册：3分

---

## 常见问题

### Q1：如何处理大量积压？
```
策略：
1. 增加处理频率
2. 批量处理
3. 优先处理重要来源
4. 临时增加并发数
```

### Q2：如何提高分类准确率？
```
方法：
1. 提供更多示例
2. 优化分类提示词
3. 使用更好的模型
4. 人工校正后反馈
```

### Q3：如何控制成本？
```
优化：
1. 使用便宜模型（DeepSeek）
2. 批量处理减少调用
3. 缓存重复内容
4. 仅处理高价值内容
```

---

## 项目总结

### 学到的技能
✅ 自动化信息收集  
✅ AI内容处理  
✅ 知识库管理  
✅ 系统集成  
✅ 性能优化  

### 实际价值
- 节省阅读时间：70%
- 提高知识留存：3倍
- 建立知识体系：系统化
- 提升学习效率：显著

### 下一步
1. 持续优化分类体系
2. 扩展信息源
3. 改进搜索算法
4. 开发移动端

---

**🎉 恭喜完成个人知识管理系统项目！**

**下一个项目：** 第15课 - AI驱动的工作助手

---

© 2026 OpenClaw课程 | 实战项目系列
