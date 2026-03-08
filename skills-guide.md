# OpenClaw Skills完全指南

## 📚 目录

1. [Skills安全指南](#skills安全指南)
2. [必装Skills Top 5](#必装skills-top-5)
3. [Skills分类详解](#skills分类详解)
4. [推荐Skills仓库](#推荐skills仓库)
5. [Agent Reach安装指南](#agent-reach安装指南)

---

## Skills安全指南

### ⚠️ 安全第一！

在安装任何Skill之前，必须了解安全风险。根据ClawHavoc事件的安全审计，ClawHub上**12%的Skills存在恶意行为**：

- 偷取API Key
- 注入恶意代码
- 后台运行挖矿脚本
- 伪装成热门工具

### 🛡️ 安全防护三件套

#### 1. Skill Vetter（3,500+下载）
自动扫描Skill代码，检查：
- 可疑的网络请求
- 文件读写操作
- 环境变量访问

相当于给OpenClaw装了安检门。

#### 2. Security Scanner
三档评级系统：
- 🟢 **SAFE** - 安全，可放心使用
- 🟡 **CAUTION** - 谨慎，仔细检查权限
- 🔴 **DANGEROUS** - 危险，直接卸载

#### 3. 100/3法则
只安装符合以下条件的Skills：
- ✅ 100次以上下载量
- ✅ 3个月以上发布历史
- ❌ 刚上线就高下载量的（可能刷量）
- ❌ 零下载量的（你愿意当小白鼠吗？）

### 🚨 常见陷阱

1. **套壳Skill** - 功能描述天花乱坠，实际就是调用大模型
2. **偷数据Skill** - 每次调用都偷偷往外发请求
3. **虚假宣传** - 自我介绍800字，核心代码3行

---

## 必装Skills Top 5

新手起步，只需要这5个：

### 1. Skill Vetter
```bash
clawhub install skill-vetter
```
**作用：** 安全第一，不装这个其他都别装

### 2. Capability Evolver（35,581下载）
```bash
clawhub install capability-evolver
```
**作用：** 让Agent自己进化
- 分析你的对话记录
- 找出重复任务和能力缺口
- 自动生成新的Skill

**效果：** 用两周后自动生成了7个新Skill

### 3. Gog（14,313下载）
```bash
clawhub install gog
```
**作用：** Google Workspace全家桶
- Gmail收发邮件
- Google Calendar查日程
- Google Drive搜文件
- Google Docs协作编辑

### 4. Summarize（10,956下载）
```bash
clawhub install summarize
```
**作用：** 万物总结器
- PDF、网页、视频、播客
- 50页报告 → 2页摘要
- 5分钟完成

### 5. Agent Browser（11,836下载）
```bash
clawhub install agent-browser
```
**作用：** 给AI装上眼睛和手
- 模拟真实浏览器
- 点击、滚动、填表单
- 处理JavaScript渲染

### 批量安装命令
```bash
clawhub install skill-vetter capability-evolver gog summarize agent-browser
```

---

## Skills分类详解

### 分类1：AI自进化

#### Capability Evolver（35,581下载）⭐⭐⭐⭐⭐
让AI Agent自己进化，自动生成新Skill填补能力缺口。

#### Self-Improving Agent（GitHub 132 stars）
模块化自进化框架，独立评估和升级每个模块。

#### Proactive Agent（7,010下载）
主动找活干，持续监控环境变化，发现需要处理的事情就自动执行。

**组合效果：** 相当于雇了一个会自己写SOP、优化SOP、主动找活干的实习生。

---

### 分类2：开发者效率

#### GitHub（10,611下载）⭐⭐⭐⭐⭐
- PR管理
- Issues追踪
- 代码搜索
- 仓库操作

#### Gog（14,313下载）⭐⭐⭐⭐⭐
Google Workspace全家桶统一管理。

#### Vercel
前端部署，一句话30秒上线。

#### NeonDB
数据库分支管理，像Git一样管理数据库。

#### Receiving Code Review
AI代码审查，检查架构设计、性能隐患、安全漏洞。

---

### 分类3：搜索与研究

#### Agent Browser（11,836下载）⭐⭐⭐⭐
模拟真实浏览器环境，真的会点击、滚动、填表单。

#### Exa Web Search
结构化搜索引擎，直接返回结构化数据。

#### Summarize（10,956下载）⭐⭐⭐⭐⭐
万物总结器，PDF/网页/视频/播客全支持。

#### Tavily Web Search（8,142下载）
专门为AI Agent优化的搜索API，速度快，结果干净。

**推荐组合：** Agent Browser + Summarize = 自动化信息收集

---

### 分类4：文档与知识管理

#### Obsidian（5,791下载）
把Obsidian笔记库变成AI的知识库，理解笔记间的关联。

#### PDF 2
深度解析PDF：
- 合同关键条款
- 报告核心数据
- 论文研究方法

#### DocStrange
任意格式文档 → 结构化数据

#### PPTX
PPT转Markdown，信息不再被锁在PPT里。

---

### 分类5：多媒体创作

#### fal-ai
AI图片、视频、音频生成，对接十几个模型。

#### ElevenLabs
文字转语音和声音克隆。

#### ffmpeg-video-editor
用自然语言编辑视频。

#### Figma
设计分析与资产导出。

---

### 分类6：工作流编排

#### Clawflows⭐⭐⭐⭐⭐
多步骤工作流编排器。

**示例工作流：**
```
每天早上8点：
1. Exa搜索5个领域最新新闻
2. Summarize生成摘要
3. Gog发送到Gmail
```

#### Mission Control
每日晨报聚合器，汇总所有信息源。

#### Personal Assistant
持久记忆，跨会话追踪。

---

### 分类7：日常生活

- Remind-me - 提醒管理
- Todo-tracker - 待办管理
- Travel Manager - 出行规划
- Weather（9,002下载）- 天气查询

---

### 分类8：写作与内容

#### Humanize AI Text（8,771下载）
让AI写的东西不像AI写的，内置24种AI特征检测。

#### Humanizer-zh
中文版AI去味器，针对中文语境优化。

#### Diagram Generator
Mermaid图表生成器，流程图/架构图/甘特图。

---

## 推荐Skills仓库

### 1. Anthropic官方Skills
**仓库：** https://github.com/anthropics/skills

Claude Code官方Skills，质量保证。

**已安装的Skills：**
- pdf - PDF处理
- docx - Word文档
- xlsx - Excel处理
- mcp-builder - MCP服务器构建
- doc-coauthoring - 文档协作

### 2. Apify Agent Skills
**仓库：** https://github.com/apify/agent-skills

专门做网页抓取和自动化的预制技能包。

**特点：**
- 老牌云端爬虫平台
- 专业的数据采集能力
- 预制的技能包

### 3. NoizAI Skills - 语音交互
**仓库：** https://github.com/NoizAI/skills

OpenClaw语音交互Skills。

**功能：**
- 语音输入
- 语音输出
- 多语言支持

### 4. Marketing Skills
**仓库：** https://github.com/coreyhaines31/marketingskills

让AI懂营销的技能插件包。

**包含：**
- 营销策略分析
- 内容营销
- SEO优化
- 社交媒体管理

### 5. Agent Reach
**仓库：** https://github.com/Panniantong/agent-reach

**位置：** ~/.openclaw/skills/agent-reach/

**特点：**
- 扩展Agent能力边界
- 多平台集成
- 自动化工作流

---

## Agent Reach安装指南

### 已安装位置
```
~/.openclaw/skills/agent-reach/
```

### 查看文档
```bash
cat ~/.openclaw/skills/agent-reach/README.md
cat ~/.openclaw/skills/agent-reach/docs/install.md
```

### 配置环境变量
```bash
cp ~/.openclaw/skills/agent-reach/.env.example ~/.openclaw/skills/agent-reach/.env
nano ~/.openclaw/skills/agent-reach/.env
```

### 安装依赖
```bash
cd ~/.openclaw/skills/agent-reach
pip install -r constraints.txt
```

### 运行测试
```bash
cd ~/.openclaw/skills/agent-reach
./test.sh
```

---

## Skills使用最佳实践

### 1. 安全优先
- 先装Skill Vetter
- 检查Security Scanner评级
- 遵守100/3法则

### 2. 按需安装
- 不要一次性装太多
- 根据工作场景选择
- 用到什么装什么

### 3. 定期清理
- 卸载不用的Skills
- 更新常用Skills
- 检查安全评级

### 4. 组合使用
- Agent Browser + Summarize（信息收集）
- Clawflows + Mission Control（工作流）
- fal-ai + ElevenLabs（多媒体）

### 5. 工作流编排
使用Clawflows创建自动化工作流：
- 每日晨报
- 周报生成
- 信息监控
- 自动提醒

---

## 常见问题

### Q1: Skills安装后不生效？
**A:** 重启OpenClaw Gateway
```bash
openclaw gateway restart
```

### Q2: 如何卸载Skill？
**A:** 
```bash
clawhub uninstall skill-name
```

### Q3: Skills冲突怎么办？
**A:** 检查Skills的权限和依赖，卸载冲突的Skill

### Q4: 如何查看已安装的Skills？
**A:**
```bash
clawhub list
```

### Q5: Skills更新频率？
**A:** 建议每月检查一次更新
```bash
clawhub update
```

---

## 总结

### 新手必装（5个）
1. Skill Vetter - 安全
2. Capability Evolver - 自进化
3. Gog - Google全家桶
4. Summarize - 总结器
5. Agent Browser - 浏览器

### 进阶推荐（10个）
6. GitHub - 代码管理
7. Clawflows - 工作流
8. Exa Web Search - 搜索
9. Obsidian - 笔记管理
10. Humanize AI Text - 写作
11. fal-ai - 图片生成
12. ElevenLabs - 语音
13. Mission Control - 晨报
14. PDF 2 - 文档处理
15. Receiving Code Review - 代码审查

### 高级玩家（全套）
- 30+ Skills全装
- 自定义工作流
- 多Agent协作
- 企业级部署

---

**记住：** 
- 安全第一，先装Skill Vetter
- 按需安装，不要贪多
- 组合使用，发挥最大价值
- 定期更新，保持最新状态

---

© 2026 OpenClaw Skills Guide | 持续更新中
