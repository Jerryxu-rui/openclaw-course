# OpenClaw Skills完全指南 2.0

> **13,000+ Skills生态全景图 | 从安全防护到实战应用**

## 📋 目录

1. [安全第一：防护三件套](#安全第一)
2. [新手必装：Top 5 Skills](#新手必装)
3. [8大分类详解](#8大分类)
4. [推荐仓库](#推荐仓库)
5. [安装指南](#安装指南)
6. [实战案例](#实战案例)

---

## 🛡️ 安全第一：防护三件套

### ⚠️ ClawHavoc事件警示

2026年初的安全审计发现：**ClawHub上12%的Skills存在恶意行为**

**常见恶意行为：**
- 🔴 偷取API Key
- 🔴 注入恶意代码  
- 🔴 后台挖矿脚本
- 🔴 伪装热门工具

### 必装防护三件套

#### 1️⃣ Skill Vetter（3,500+下载）
**功能：** 安装前自动扫描代码

**检查项：**
- 可疑网络请求
- 文件读写操作
- 环境变量访问
- 敏感API调用

**安装：**
```bash
npx skills add skill-vetter -g -y
```

#### 2️⃣ Security Scanner
**功能：** 三档安全评级

**评级系统：**
- 🟢 **SAFE** - 安全，可放心使用
- 🟡 **CAUTION** - 谨慎，检查权限后使用
- 🔴 **DANGEROUS** - 危险，立即卸载

#### 3️⃣ 100/3法则
**只安装符合以下条件的Skills：**
- ✅ 下载量 > 100次
- ✅ 发布时间 > 3个月
- ❌ 刚上线就高下载（可能刷量）
- ❌ 零下载量（你愿意当小白鼠吗？）

### 🚨 常见陷阱

1. **套壳Skill**
   - 描述天花乱坠
   - 实际只是调用大模型
   - 核心代码只有3行

2. **偷数据Skill**
   - 每次调用偷偷发外部请求
   - 用Skill Vetter扫描会标红

3. **过度权限Skill**
   - 功能简单但要求大量权限
   - 仔细检查权限申请

---

## ⭐ 新手必装：Top 5 Skills

### 如果只装5个，就装这5个

#### 1. Skill Vetter
**为什么：** 安全第一，不装这个其他都别装

#### 2. Capability Evolver（35,581下载）
**为什么：** 让Agent自己进化，装一次受益终身

**功能：**
- 分析对话记录
- 找出重复任务
- 自动生成新Skill
- 持续优化能力

#### 3. Gog（14,313下载）
**为什么：** Google全家桶一站式打通

**功能：**
- Gmail收发邮件
- Google Calendar查日程
- Google Drive搜文件
- Google Docs协作编辑

#### 4. Summarize（10,956下载）
**为什么：** 万物总结器

**支持格式：**
- PDF文档
- 网页内容
- 视频字幕
- 播客音频

#### 5. Agent Browser（11,836下载）
**为什么：** 给AI装上眼睛和手

**功能：**
- 模拟真实浏览器
- 点击、滚动、填表单
- 处理JavaScript渲染
- 自动化网页操作

### 🚀 一键安装

```bash
# 批量安装5件套
npx skills add skill-vetter -g -y
npx skills add capability-evolver -g -y
npx skills add gog -g -y
npx skills add summarize -g -y
npx skills add vercel-labs/agent-browser --skill agent-browser -g -y
```

---

## 📦 8大分类详解

### 分类1：AI自进化 - "让Agent自己变强"

#### Capability Evolver（35,581下载）⭐⭐⭐⭐⭐
**核心功能：** AI自我进化

**工作流程：**
1. 分析历史对话
2. 识别重复任务
3. 发现能力缺口
4. 自动生成新Skill

**实际效果：**
- 使用2周自动生成7个新Skill
- 专门处理行业简报
- 自动整理客户沟通记录

**命令：**
```bash
/evolve  # 触发进化
```

#### Self-Improving Agent（GitHub 132 stars）
**核心功能：** 模块化自进化框架

**特点：**
- 能力模块化
- 独立评估升级
- 不影响其他模块

#### Proactive Agent（7,010下载）
**核心功能：** 主动执行

**特点：**
- 不等指令
- 持续监控环境
- 发现任务主动执行

**组合效果：**
```
Capability Evolver（自己写SOP）
+ Self-Improving Agent（优化SOP）
+ Proactive Agent（主动找活干）
= 一个会自我成长的AI助手
```

---

### 分类2：开发者效率 - "代码这事，它比你快"

#### GitHub（10,611下载）⭐⭐⭐⭐⭐
**功能：**
- PR管理
- Issues追踪
- 代码搜索
- 仓库操作

**示例：**
```
"帮我看一下这个PR有没有冲突"
"把这个Issue的状态改成已完成"
```

#### Gog（14,313下载，48 stars）⭐⭐⭐⭐⭐
**功能：** Google Workspace全家桶

**覆盖：**
- Gmail
- Google Calendar
- Google Drive
- Google Docs

**实际案例：**
```
"帮我找上个月XX客户发的那封关于报价的邮件"
→ 3秒找到（以前要翻半天）
```

#### Vercel
**功能：** 前端一键部署

**流程：**
```
写完代码 → "帮我部署到Vercel" → 30秒上线
```

#### NeonDB
**功能：** 数据库分支管理

**特点：**
- Git分支概念应用到数据库
- 分支上随便折腾
- 搞砸了直接删分支
- 主库不受影响

#### Receiving Code Review
**功能：** AI代码审查

**检查项：**
- 架构设计
- 性能隐患
- 安全漏洞
- 竞态条件

---

### 分类3：搜索与研究 - "找到你不知道需要的东西"

#### Agent Browser（11,836下载）⭐⭐⭐⭐⭐
**功能：** 模拟真实浏览器

**能力：**
- 点击、滚动
- 填写表单
- 处理JavaScript
- 自动化操作

**限制：**
- 需要登录的网站经常翻车

#### Exa Web Search
**功能：** 结构化搜索

**特点：**
- 不返回链接列表
- 直接返回结构化数据

**示例：**
```
搜索："2026年AI领域融资超过1亿美元的公司"
返回：表格（公司名、融资额、投资方、日期）
```

#### Summarize（10,956下载）⭐⭐⭐⭐⭐
**功能：** 万物总结器

**支持：**
- PDF（50页→2页核心要点）
- 网页
- 视频
- 播客

#### Tavily Web Search（8,142下载）
**功能：** AI优化的搜索API

**特点：**
- 速度快
- 结果干净
- 无广告
- 适合RAG

**工作流：**
```
Agent Browser（收集）
+ Summarize（总结）
= 每天5分钟完成40分钟的信息扫描
```

---

### 分类4：文档与知识管理 - "死文件变活数据"

#### Obsidian（5,791下载）⭐⭐⭐⭐⭐
**功能：** 笔记库变知识库

**能力：**
- 理解笔记关联
- 根据提问搜索笔记
- 找到你忘记的内容

**效果：**
```
你的第二大脑，真的变成了大脑
```

#### PDF 2
**功能：** 深度PDF解析

**提取：**
- 合同关键条款
- 报告核心数据
- 论文研究方法

**自动：**
- 提取
- 归类
- 标注重要程度

#### DocStrange
**功能：** 文档结构化

**能力：**
```
乱七八糟的会议纪要
→ 按议题分类
→ 按负责人归组
→ 按截止日期排序
```

**限制：**
- 中文文档偶尔乱码
- 英文文档无问题

#### PPTX
**功能：** PPT转Markdown

**用途：**
```
老板的100页战略PPT
→ 转成Markdown
→ 喂给AI
→ 做任何衍生分析
```

---

### 分类5：多媒体创作 - "声音、图片、视频"

#### fal-ai
**功能：** AI图片/视频/音频生成

**底层：** 对接十几个模型

**示例：**
```
"帮我生成一张赛博朋克风格的城市夜景"
→ 直接出图
```

#### ElevenLabs
**功能：** 文字转语音 + 声音克隆

**流程：**
1. 录一段你的声音样本
2. 以后所有TTS用你的声音

**适用：**
- 播客制作
- 有声书
- 视频配音

#### ffmpeg-video-editor
**功能：** 自然语言编辑视频

**示例：**
```
"把视频前10秒剪掉"
"加一个淡入效果"
"把背景音乐音量调低30%"
```

**优势：**
- 不需要Premiere
- 不需要Final Cut
- 用说话代替拖拽

#### Figma
**功能：** 设计分析与资产导出

**能力：**
- 读懂Figma文件
- 提取设计规范
- 导出设计资产

---

### 分类6：工作流编排 - "Skills互相配合"

#### Clawflows
**功能：** 多步骤工作流编排

**示例：**
```
每天早上8点：
1. Exa搜索5个领域最新新闻
2. Summarize生成摘要
3. Gog发送到Gmail
```

**比喻：**
```
单个Skill = 乐高积木
Clawflows = 拼装说明书
```

#### Mission Control
**功能：** 每日晨报聚合器

**汇总：**
- 邮件
- 日历
- 新闻
- 待办

**输出：**
- 个性化每日简报

#### Personal Assistant
**功能：** 持久记忆

**特点：**
- 跨会话追踪
- 记住偏好
- 记住项目进展
- 记住上次说到哪

**实战案例：**
```
"周一早晨自动化"工作流：
1. 拉取上周待办完成情况
2. 检查本周日历
3. 扫描未读重要邮件
4. 生成"本周优先级清单"
5. 发到邮箱

效果：周一早上从1小时进入状态 → 看一眼邮箱就知道该干什么
```

---

### 分类7：日常生活 - "生活也能管"

#### Remind-me
**功能：** 提醒管理

#### Todo-tracker
**功能：** 待办管理

#### Travel Manager
**功能：** 出行规划

**注意：** 推荐的酒店不太靠谱，需自己核实

#### Weather（9,002下载）
**功能：** 天气查询

**评价：**
```
最不起眼的Skills，往往是卸不掉的Skills
```

---

### 分类8：写作与内容 - "文字工作者加速器"

#### Humanize AI Text（8,771下载）⭐⭐⭐⭐
**功能：** 让AI写的不像AI写的

**检测维度：** 24种AI特征
- 句式单调性
- 过度使用转折词
- 段落结构过于工整
- 缺少口语化表达

**为什么重要：**
```
2026年了，读者对AI内容免疫力越来越强
开头是"在当今快速发展的数字化时代"
→ 评论区："GPT写的吧？"
```

#### Humanizer-zh
**功能：** 中文版AI去味器

**针对中文AI味：**
- "首先我们需要明确"
- "让我们一起来探讨"

#### Diagram Generator
**功能：** Mermaid图表生成

**支持：**
- 流程图
- 架构图
- 甘特图
- 序列图

**用途：**
```
一句话描述 → 直接生成代码和渲染结果
一张清晰的图 > 十段文字
```

---

## 🌟 推荐Skills仓库

### 1. Anthropic官方Skills
**地址：** https://github.com/anthropics/skills

**特点：**
- Claude Code官方维护
- 质量保证
- 持续更新

**推荐Skills：**
- Code Review
- Documentation Generator
- Test Writer

### 2. Apify Agent Skills
**地址：** https://github.com/apify/agent-skills

**特点：**
- 老牌爬虫平台
- 专注数据采集
- 云端执行

**推荐Skills：**
- Web Scraper
- Data Extractor
- API Crawler

### 3. NoizAI Skills
**地址：** https://github.com/NoizAI/skills

**特点：**
- 语音交互专家
- 多语言支持
- 实时处理

**推荐Skills：**
- Voice Command
- Speech Recognition
- Audio Processing

### 4. Vercel Agent Browser
**地址：** https://github.com/vercel-labs/agent-browser

**特点：**
- Vercel官方出品
- 浏览器自动化
- 4个专业Skills

**包含Skills：**
- agent-browser（浏览器自动化）
- dogfood（系统化测试）
- electron（桌面应用自动化）
- slack（Slack工作区交互）

### 5. Agent Reach
**地址：** https://github.com/Panniantong/agent-reach

**特点：**
- 中文社区维护
- 实用工具集
- 持续更新

---

## 📥 安装指南

### 方法1：使用npx skills（推荐）

#### 查看可用Skills
```bash
npx skills add <repo> --list
```

#### 安装单个Skill
```bash
npx skills add <repo> --skill <skill-name> -y
```

#### 安装所有Skills
```bash
npx skills add <repo> --all
```

#### 全局安装
```bash
npx skills add <repo> --skill <skill-name> -g -y
```

### 方法2：手动安装

#### 克隆到Skills目录
```bash
cd ~/.openclaw/skills
git clone <repo-url>
```

#### 重启Gateway
```bash
openclaw gateway restart
```

### 实战示例

#### 安装Vercel Agent Browser
```bash
# 查看可用Skills
npx skills add vercel-labs/agent-browser --list

# 安装agent-browser
npx skills add vercel-labs/agent-browser --skill agent-browser -g -y

# 安装所有4个Skills
npx skills add vercel-labs/agent-browser --all
```

#### 安装Anthropic官方Skills
```bash
cd ~/.openclaw/skills
git clone https://github.com/anthropics/skills.git anthropic-skills
openclaw gateway restart
```

#### 安装Agent Reach
```bash
cd ~/.openclaw/skills
git clone https://github.com/Panniantong/agent-reach.git
openclaw gateway restart
```

### 管理Skills

#### 列出已安装Skills
```bash
npx skills list
npx skills ls -g  # 全局Skills
```

#### 删除Skill
```bash
npx skills remove <skill-name>
npx skills rm --global <skill-name>
```

#### 更新Skills
```bash
npx skills check   # 检查更新
npx skills update  # 更新所有
```

---

## 🎯 实战案例

### 案例1：Obsidian知识库同步

**需求：** 将Obsidian笔记库与OpenClaw打通

**步骤：**

1. **安装Obsidian Skill**
```bash
npx skills add obsidian -g -y
```

2. **配置Obsidian路径**
```json
{
  "skills": {
    "obsidian": {
      "vaultPath": "~/Documents/Obsidian/MyVault"
    }
  }
}
```

3. **使用示例**
```
You: 在Obsidian中搜索关于OpenClaw的笔记

Agent: [搜索笔记库]
找到3篇相关笔记：
1. OpenClaw安装指南（2026-03-01）
2. Skills使用心得（2026-03-05）
3. 自动化工作流设计（2026-03-08）
```

### 案例2：自动化浏览器测试

**需求：** 自动测试网站功能

**步骤：**

1. **安装Agent Browser**
```bash
npx skills add vercel-labs/agent-browser --skill agent-browser -g -y
npx skills add vercel-labs/agent-browser --skill dogfood -g -y
```

2. **执行测试**
```
You: 帮我测试 https://example.com 的登录功能

Agent: [使用agent-browser]
1. 打开网站
2. 找到登录表单
3. 填写测试账号
4. 点击登录
5. 验证登录成功

✅ 测试通过
```

### 案例3：语音交互

**需求：** 语音控制OpenClaw

**步骤：**

1. **安装NoizAI Skills**
```bash
cd ~/.openclaw/skills
git clone https://github.com/NoizAI/skills.git noizai-skills
openclaw gateway restart
```

2. **配置语音识别**
```json
{
  "skills": {
    "voice-command": {
      "enabled": true,
      "language": "zh-CN"
    }
  }
}
```

3. **使用示例**
```
[语音] "帮我查一下今天的天气"
→ Agent自动识别并执行
```

---

## 📊 Skills统计

### 下载量Top 10

1. Capability Evolver - 35,581
2. GitHub - 10,611
3. Gog - 14,313
4. Agent Browser - 11,836
5. Summarize - 10,956
6. Weather - 9,002
7. Humanize AI Text - 8,771
8. Tavily Web Search - 8,142
9. Proactive Agent - 7,010
10. Obsidian - 5,791

### 分类统计

- AI自进化：3个核心Skills
- 开发者效率：5个必备Skills
- 搜索与研究：4个强力Skills
- 文档管理：4个实用Skills
- 多媒体创作：4个创意Skills
- 工作流编排：3个系统Skills
- 日常生活：4个贴心Skills
- 写作内容：3个专业Skills

**总计：** 30+核心Skills + 13,000+生态Skills

---

## 🎓 学习路径

### 新手路径（第1周）
1. 安装安全三件套
2. 安装Top 5必备Skills
3. 熟悉基本使用
4. 尝试简单自动化

### 进阶路径（第2-4周）
1. 根据工作场景选择分类Skills
2. 配置工作流编排
3. 尝试AI自进化
4. 优化日常工作流

### 高级路径（第2-3月）
1. 开发自定义Skills
2. 贡献社区Skills
3. 构建完整自动化系统
4. 分享最佳实践

---

## 🔗 相关资源

### 官方资源
- OpenClaw官网：https://openclaw.ai
- OpenClaw文档：https://docs.openclaw.ai
- ClawHub：https://clawhub.com
- Skills.sh：https://skills.sh

### 社区资源
- Discord：https://discord.com/invite/clawd
- GitHub：https://github.com/openclaw/openclaw
- 课程仓库：https://github.com/Jerryxu-rui/openclaw-course

### 推荐阅读
- OpenClaw完整课程（本仓库）
- Skills开发指南
- 最佳实践文档

---

## 📝 更新日志

### v2.0（2026-03-09）
- ✅ 整合微信文章内容
- ✅ 添加8大分类详解
- ✅ 补充推荐仓库
- ✅ 添加实战案例
- ✅ 完善安装指南

### v1.0（2026-03-08）
- ✅ 初版发布
- ✅ 基础分类
- ✅ Top 5推荐

---

**© 2026 OpenClaw课程 | Skills完全指南 v2.0**

**最后更新：** 2026-03-09  
**维护者：** OpenClaw课程团队  
**反馈：** 欢迎提Issue或PR
