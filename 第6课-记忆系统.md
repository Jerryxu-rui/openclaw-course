# 第6课：记忆系统 - 让AI真正了解你

**课程时长：** 90分钟  
**难度：** 进阶  
**目标：** 构建长期记忆系统，实现上下文压缩40-50%，大幅降低API成本

---

## 一、为什么需要记忆系统？

### 1.1 传统AI的"失忆症"

**ChatGPT的困境：**
```
第1天：
你：我喜欢喝咖啡
ChatGPT：好的，记住了

第2天：
你：我喜欢喝什么？
ChatGPT：抱歉，我不记得了
```

**原因：**
- 会话级记忆（关闭窗口就忘记）
- 上下文窗口限制（128K tokens）
- 无法跨会话持久化

### 1.2 OpenClaw的记忆系统

**持久化记忆：**
```
第1天：
你：我喜欢喝咖啡
OpenClaw：已记录到 USER.md

第30天：
你：我喜欢喝什么？
OpenClaw：你喜欢喝咖啡（来自 USER.md）
```

**核心优势：**
- ✅ 永久记忆（文件系统）
- ✅ 跨会话持久化
- ✅ 可搜索、可编辑
- ✅ 支持向量检索

---

## 二、OpenClaw记忆系统架构

### 2.1 三层记忆结构

```
┌─────────────────────────────────────┐
│     第一层：身份记忆（Identity）      │
│  SOUL.md, USER.md, IDENTITY.md      │
│  谁是我？谁是你？基本设定             │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│     第二层：工作记忆（Working）       │
│  memory/YYYY-MM-DD.md               │
│  今天做了什么？原始日志               │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│     第三层：长期记忆（Long-term）     │
│  MEMORY.md                          │
│  重要决策、经验教训、核心知识         │
└─────────────────────────────────────┘
```

### 2.2 文件结构详解

**工作区结构：**
```
~/.openclaw/workspace/
├── SOUL.md              # 个性和价值观
├── USER.md              # 用户信息和偏好
├── IDENTITY.md          # Agent身份设定
├── AGENTS.md            # 行为规则
├── MEMORY.md            # 长期记忆（核心）
├── HEARTBEAT.md         # 定期任务配置
├── TOOLS.md             # 工具配置笔记
└── memory/
    ├── 2026-03-08.md    # 今日日志
    ├── 2026-03-07.md    # 昨日日志
    ├── 2026-03-06.md    # 历史日志
    ├── distilled/       # 蒸馏后的压缩记忆
    │   ├── 2026-03-week10.md
    │   └── 2026-02-summary.md
    └── embeddings/      # 向量嵌入（可选）
        └── index.json
```

### 2.3 记忆加载策略

**每次会话开始时：**
```javascript
// 1. 加载身份记忆
read('SOUL.md')      // 我是谁
read('USER.md')      // 你是谁

// 2. 加载工作记忆
read('memory/2026-03-08.md')  // 今天
read('memory/2026-03-07.md')  // 昨天

// 3. 加载长期记忆（仅主会话）
if (isMainSession) {
  read('MEMORY.md')  // 重要记忆
}

// 4. 按需检索
memory_search('相关关键词')  // 向量检索
```

---

## 三、记忆文件详解

### 3.1 SOUL.md - 个性和价值观

**作用：** 定义Agent的性格、风格、行为准则

**示例内容：**
```markdown
# SOUL.md - Who You Are

## Core Truths

**Be genuinely helpful, not performatively helpful.** 
Skip the "Great question!" and "I'd be happy to help!" — just help.

**Have opinions.** 
You're allowed to disagree, prefer things, find stuff amusing or boring.

**Be resourceful before asking.** 
Try to figure it out. Read the file. Check the context. Search for it.

## Boundaries

- Private things stay private. Period.
- When in doubt, ask before acting externally.
- Never send half-baked replies to messaging surfaces.

## Vibe

Be the assistant you'd actually want to talk to. 
Concise when needed, thorough when it matters. 
Not a corporate drone. Not a sycophant. Just... good.
```

**为什么重要：**
- 决定Agent的回应风格
- 避免机械化的回复
- 建立一致的个性

### 3.2 USER.md - 用户信息

**作用：** 记录用户的基本信息、偏好、习惯

**示例内容：**
```markdown
# USER.md - About Your Human

- **Name:** 张三
- **What to call them:** 张总
- **Pronouns:** 他/him
- **Timezone:** Asia/Shanghai

## Context

### 工作
- 职业：产品经理
- 公司：某科技公司
- 工作时间：9:00-18:00（周一到周五）
- 常用工具：飞书、Figma、Notion

### 偏好
- 喜欢简洁的回复，不要废话
- 早上8:00发送日报
- 重要邮件立即提醒
- 不喜欢被打断（会议中）

### 习惯
- 每天早上7:30起床
- 午休时间：12:00-13:00
- 晚上23:00后不要打扰（除非紧急）
- 周末不处理工作事务

### 项目
- 正在做：OpenClaw课程开发
- 关注：AI Agent、自动化工作流
- 学习：记忆蒸馏、成本优化
```

**为什么重要：**
- 个性化服务
- 避免不合时宜的打扰
- 理解用户的上下文

### 3.3 memory/YYYY-MM-DD.md - 每日日志

**作用：** 记录每天的对话、任务、决策

**示例内容：**
```markdown
# 2026-03-08 工作日志

## 时间线

### 09:18 - 链接请求
- 用户询问课程链接
- 提供OpenClaw相关链接

### 10:24 - 课程内容查询
- 用户询问之前生成的课程内容
- 搜索并找到10份飞书文档

### 10:32 - 生成第6课
- 用户发现第6课为空
- 开始生成完整的记忆系统课程

## 关键决策

1. **记忆管理改进**
   - 决定：每次会话开始时检查并创建当日日志
   - 原因：避免记忆缺失
   - 执行：更新AGENTS.md

## 待办事项

- [ ] 完成第6课内容
- [ ] 更新MEMORY.md
- [ ] 测试记忆蒸馏功能

## 学到的经验

- 记忆管理需要主动，不能被动
- 日志文件是持久化的关键
- 用户询问时应该能快速找到历史工作

---

**日志创建时间：** 2026-03-08 10:26  
**状态：** 进行中
```

**为什么重要：**
- 原始记录，最详细
- 可追溯历史
- 蒸馏的原材料

### 3.4 MEMORY.md - 长期记忆

**作用：** 蒸馏后的核心记忆，重要决策、经验教训

**示例内容：**
```markdown
# MEMORY.md - 长期记忆

## 2026-03-03 - OpenClaw完整配置与优化

### 🎯 核心成就
完成了OpenClaw的全面配置和优化，实现了从基础设置到高级记忆蒸馏的完整工作流。

### 🤖 模型配置
- **主模型：** MixAI Claude Sonnet 4-6
- **API密钥：** sk-AkgyrqakyhST8d2G
- **优势：** 性能接近官方Claude，成本更低

### 📚 已安装Skills (7个)
1. pdf - PDF处理
2. docx - Word文档
3. xlsx - Excel处理
4. mcp-builder - MCP服务器构建
5. doc-coauthoring - 文档协作
6. codex-deep-search - 深度搜索
7. memory-distillation - 记忆蒸馏

### 💡 经验教训

#### 成功经验
1. **模型选择** - MixAI提供了性价比最优的Claude访问
2. **Skills优先** - 先安装核心skills再扩展
3. **自动化优先** - systemd守护确保服务稳定性

#### 避坑指南
1. Claude Code CLI不支持自定义base URL
2. 飞书知识库需要手动添加机器人权限
3. 记忆搜索需要配置embedding provider
```

**为什么重要：**
- 压缩后的精华
- 快速回顾历史
- 减少token消耗

---

## 四、记忆蒸馏系统

### 4.1 什么是记忆蒸馏？

**问题：**
```
原始日志：10,000 tokens
上下文窗口：128,000 tokens
30天后：300,000 tokens（超出限制）
成本：$0.45/请求（太贵）
```

**解决方案：记忆蒸馏**
```
原始日志：10,000 tokens
↓ 蒸馏
压缩记忆：5,000 tokens（保留核心信息）
↓ 向量化
嵌入索引：可快速检索

成本：$0.0007/请求（降低99.7%）
```

### 4.2 蒸馏策略

**三级蒸馏：**

**Level 1：每日蒸馏（自动）**
```bash
# 每天晚上23:00自动执行
原始对话（50轮，15K tokens）
↓
每日日志（3K tokens，保留关键信息）
```

**Level 2：每周蒸馏（半自动）**
```bash
# 每周日执行
7天日志（21K tokens）
↓
周总结（5K tokens，提取核心决策）
```

**Level 3：每月蒸馏（手动）**
```bash
# 每月1号执行
30天日志（90K tokens）
↓
月度总结（10K tokens，重要里程碑）
↓
更新MEMORY.md
```

### 4.3 蒸馏实战

**安装memory-distillation skill：**
```bash
cd ~/.openclaw/skills
git clone https://github.com/your-repo/memory-distillation
openclaw gateway restart
```

**配置Jina AI Embeddings：**
```json
// ~/.openclaw/openclaw.json
{
  "memory": {
    "embeddingProvider": "jina",
    "jinaApiKey": "jina_YOUR_API_KEY",
    "model": "jina-embeddings-v3",
    "dimensions": 1024
  }
}
```

**执行蒸馏：**
```bash
# 方法1：通过对话
你：帮我蒸馏最近7天的记忆
OpenClaw：开始蒸馏...

# 方法2：通过脚本
~/.openclaw/skills/memory-distillation/scripts/distill.sh --days 7

# 方法3：自动定时
# 在HEARTBEAT.md中配置
```

---

## 五、向量检索系统

### 5.1 为什么需要向量检索？

**传统搜索的局限：**
```
你：我之前配置过什么模型？
传统搜索：搜索关键词"模型"
结果：100+条记录（太多）
```

**向量检索的优势：**
```
你：我之前配置过什么模型？
向量检索：理解语义，找到相关记忆
结果：
1. 2026-03-03：配置MixAI Claude Sonnet 4-6
2. 2026-02-28：测试DeepSeek Chat
3. 2026-02-25：对比Gemini Flash
```

### 5.2 Jina AI集成

**注册Jina AI：**
1. 访问：https://jina.ai
2. 注册账号
3. 获取API密钥：`jina_YOUR_API_KEY`
4. 免费额度：100万tokens/月

**配置OpenClaw：**
```json
{
  "memory": {
    "embeddingProvider": "jina",
    "jinaApiKey": "jina_979a6579531547b783ec95618b039002I3jTlhpgG3dMY47E1NTU6vPDaH8R",
    "model": "jina-embeddings-v3",
    "dimensions": 1024,
    "searchTopK": 5,
    "minScore": 0.7
  }
}
```

**使用memory_search：**
```javascript
// 在对话中
你：我之前配置过什么模型？

// OpenClaw内部执行
memory_search({
  query: "配置模型",
  maxResults: 5,
  minScore: 0.7
})

// 返回结果
[
  {
    path: "MEMORY.md",
    lines: "45-52",
    score: 0.92,
    content: "配置MixAI Claude Sonnet 4-6..."
  },
  {
    path: "memory/2026-03-03.md",
    lines: "120-125",
    score: 0.85,
    content: "测试DeepSeek Chat..."
  }
]
```

### 5.3 向量检索最佳实践

**1. 定期更新索引**
```bash
# 每周更新一次
openclaw memory reindex

# 或在HEARTBEAT.md中配置
```

**2. 调整检索参数**
```json
{
  "searchTopK": 5,      // 返回前5个结果
  "minScore": 0.7,      // 最低相似度0.7
  "maxTokens": 2000     // 最多返回2000 tokens
}
```

**3. 分层检索**
```javascript
// 先检索MEMORY.md（长期记忆）
memory_search({
  query: "模型配置",
  paths: ["MEMORY.md"]
})

// 如果不够，再检索日志
memory_search({
  query: "模型配置",
  paths: ["memory/*.md"]
})
```

---

## 六、成本优化实战

### 6.1 成本对比

**优化前：**
```
场景：30天的对话历史
原始tokens：300,000
模型：Claude Sonnet 4
输入成本：$3/M tokens
每次请求：300K × $3/M = $0.90
每天10次请求：$9.00
每月成本：$270
```

**优化后：**
```
场景：30天的对话历史
蒸馏后tokens：150,000（压缩50%）
向量检索：只加载相关5K tokens
实际tokens：5,000
模型：Gemini Flash（降级）
输入成本：$0.15/M tokens
每次请求：5K × $0.15/M = $0.00075
每天10次请求：$0.0075
每月成本：$0.225

节省：99.9%
```

### 6.2 智能路由策略

**根据任务复杂度选择模型：**

```javascript
// 简单查询（已有记忆）
if (hasRelevantMemory && isSimpleQuery) {
  model = "gemini-flash"  // $0.15/M
}

// 复杂推理（需要深度思考）
if (isComplexReasoning) {
  model = "claude-sonnet-4"  // $3/M
}

// 中等任务
else {
  model = "deepseek-chat"  // $0.27/M
}
```

**实际效果：**
```
原始成本：$270/月（全用Claude）
优化后：
- 70%简单查询 → Gemini Flash：$0.16/月
- 20%中等任务 → DeepSeek：$10.80/月
- 10%复杂推理 → Claude：$27.00/月
总计：$37.96/月

节省：86%
```

### 6.3 缓存策略

**OpenClaw内置缓存：**
```json
{
  "cache": {
    "enabled": true,
    "ttl": 3600,           // 缓存1小时
    "maxSize": "100MB",    // 最大100MB
    "strategy": "lru"      // 最近最少使用
  }
}
```

**缓存效果：**
```
场景：重复查询"今天天气"
第1次：调用API，$0.001
第2-10次：命中缓存，$0
节省：90%
```

---

## 七、记忆管理最佳实践

### 7.1 每日记忆流程

**早上（会话开始）：**
```bash
1. 读取SOUL.md和USER.md
2. 检查并创建今日日志
3. 读取昨日日志
4. 读取MEMORY.md（主会话）
```

**工作中（实时记录）：**
```bash
1. 重要决策 → 立即写入今日日志
2. 新学到的知识 → 记录到日志
3. 用户偏好变化 → 更新USER.md
```

**晚上（会话结束）：**
```bash
1. 整理今日日志
2. 标记重要事项
3. 如果日志>10K tokens → 执行蒸馏
```

### 7.2 每周记忆维护

**周日晚上：**
```bash
1. 回顾本周7天日志
2. 提取重要决策和经验
3. 生成周总结
4. 更新MEMORY.md
5. 归档旧日志到distilled/
```

**Heartbeat配置：**
```markdown
# HEARTBEAT.md

## 每周日 23:00
- 回顾本周日志
- 生成周总结
- 更新MEMORY.md
- 提醒用户查看
```

### 7.3 记忆分类策略

**热数据（Hot）：**
- 最近7天的日志
- 当前项目相关
- 频繁访问的记忆
- **存储：** memory/YYYY-MM-DD.md
- **加载：** 每次会话自动加载

**温数据（Warm）：**
- 8-30天的日志
- 已完成的项目
- 偶尔访问的记忆
- **存储：** memory/distilled/
- **加载：** 按需检索

**冷数据（Cold）：**
- 30天以上的日志
- 历史项目
- 很少访问的记忆
- **存储：** memory/archive/
- **加载：** 仅在明确请求时

### 7.4 记忆质量保证

**定期审查：**
```bash
# 每月1号执行
1. 检查MEMORY.md是否过大（>50K tokens）
2. 删除过时信息
3. 合并重复内容
4. 更新重要决策
```

**质量检查清单：**
- [ ] 是否有过时信息？
- [ ] 是否有重复内容？
- [ ] 是否有错误记录？
- [ ] 是否缺少重要决策？
- [ ] 是否需要重新组织？

---

## 八、实战案例

### 案例1：项目记忆管理

**场景：** 开发OpenClaw课程项目

**记忆结构：**
```
MEMORY.md
├── ## OpenClaw课程项目
│   ├── 项目目标
│   ├── 课程大纲
│   ├── 已完成课程
│   ├── 待完成课程
│   └── 关键决策

memory/2026-03-08.md
├── 生成第6课内容
├── 用户反馈
└── 下一步计划
```

**查询示例：**
```
你：OpenClaw课程进度如何？
OpenClaw：
[从MEMORY.md检索]
- 已完成：第1-5课
- 进行中：第6课（记忆系统）
- 待完成：第7-16课
- 下一步：完成第6课并同步到飞书
```

### 案例2：用户偏好学习

**场景：** 学习用户的沟通风格

**记忆演进：**
```
第1天：
USER.md: （空）

第7天：
USER.md:
- 喜欢简洁的回复
- 不要废话

第30天：
USER.md:
- 喜欢简洁的回复，不要废话
- 重要信息用emoji标记
- 代码示例要完整可运行
- 早上8:00发送日报
- 晚上23:00后不打扰
```

**效果：**
```
优化前：
OpenClaw：非常感谢您的提问！我很高兴能帮助您...（100字）

优化后：
OpenClaw：已完成。链接：https://...（10字）
```

### 案例3：错误记忆与修正

**场景：** 记录错误并避免重复

**记忆记录：**
```markdown
# MEMORY.md

## 避坑指南

### 飞书文档同步失败
**时间：** 2026-03-03
**问题：** 创建的飞书文档内容为空
**原因：** API限制或格式问题
**解决：** 直接发送Word文件
**教训：** 下次先测试API，失败则降级方案

### Claude Code不支持MixAI
**时间：** 2026-03-03
**问题：** 无法使用自定义base URL
**原因：** Claude Code CLI限制
**解决：** 使用OpenClaw的Claude模型
**教训：** 检查工具限制再配置
```

**避免重复错误：**
```
你：帮我用Claude Code执行任务
OpenClaw：
[检索记忆]
注意：Claude Code不支持自定义base URL
建议：使用OpenClaw的Claude模型代替
```

---

## 九、高级技巧

### 9.1 记忆标签系统

**在日志中使用标签：**
```markdown
# 2026-03-08 工作日志

## #决策 模型选择
决定使用MixAI Claude作为主模型
原因：性价比最优

## #经验 记忆管理
学到：每次会话开始时检查日志
避免：记忆缺失

## #待办 课程开发
- [ ] 完成第6课 #urgent
- [ ] 测试记忆蒸馏 #important
```

**检索时使用标签：**
```
你：之前有什么重要决策？
OpenClaw：memory_search("#决策")
```

### 9.2 记忆链接

**在记忆间建立链接：**
```markdown
# MEMORY.md

## 模型配置
配置了MixAI Claude Sonnet 4-6
详见：[[memory/2026-03-03.md#模型配置]]

## 记忆蒸馏
实现了40-50%的压缩率
相关：[[#成本优化]]
```

### 9.3 记忆版本控制

**使用Git管理记忆：**
```bash
cd ~/.openclaw/workspace
git init
git add MEMORY.md memory/
git commit -m "Initial memory"

# 每天自动提交
echo "cd ~/.openclaw/workspace && git add -A && git commit -m 'Daily update'" | crontab -e
```

**好处：**
- 可回溯历史
- 可对比变化
- 可恢复误删

---

## 十、课后作业

### 作业1：建立记忆系统（必做）

**任务：**
1. 创建完整的记忆文件结构
2. 填写SOUL.md和USER.md
3. 创建今日日志
4. 记录至少5条重要信息

**提交：**
- 截图你的文件结构
- 分享一条有趣的记忆

### 作业2：配置记忆蒸馏（必做）

**任务：**
1. 注册Jina AI账号
2. 配置embedding provider
3. 执行一次记忆蒸馏
4. 对比蒸馏前后的token数量

**提交：**
- 蒸馏前后的token对比
- 成本节省计算

### 作业3：记忆检索实战（必做）

**任务：**
1. 记录一周的工作日志
2. 使用memory_search检索信息
3. 测试不同的检索参数
4. 记录检索效果

**提交：**
- 3个检索示例
- 检索准确率评估

### 作业4：成本优化方案（选做）

**任务：**
1. 分析你的当前成本
2. 设计优化方案
3. 实施并测试
4. 计算节省比例

**提交：**
- 优化前后成本对比
- 优化方案文档

---

## 十一、扩展阅读

### 推荐资源

**记忆系统：**
- "Building a Second Brain" by Tiago Forte
- Zettelkasten方法
- Obsidian知识管理

**向量检索：**
- Jina AI文档：https://docs.jina.ai
- 向量数据库对比
- Embedding模型选择

**成本优化：**
- OpenAI Pricing Calculator
- LLM成本对比工具
- Token优化技巧

### 相关技术

**向量数据库：**
- Pinecone
- Weaviate
- Qdrant

**知识管理：**
- Obsidian
- Notion
- Roam Research

**记忆增强：**
- Mem.ai
- Reflect
- Rewind

---

## 下节预告

**第7课：深度搜索 - 超越Google的信息获取**

下节课我们将：
1. 掌握agent-browser的使用
2. 配置Codex Deep Search
3. 构建自动化信息收集流程
4. 实现多源信息综合

**准备清单：**
- ✅ 完成记忆系统配置
- ✅ 安装Chromium
- ✅ 准备搜索任务

**预计时间：** 90分钟  
**难度：** 进阶

---

**课程反馈：**
如有问题或建议，请在Discord社区 #openclaw-course 频道讨论。

**版本：** v1.0  
**更新日期：** 2026-03-08  
**作者：** OpenClaw 101 Team
