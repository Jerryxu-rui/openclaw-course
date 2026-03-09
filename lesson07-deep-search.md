# 第7课：深度搜索 - 超越Google的信息获取

## 课程目标
- 掌握OpenClaw的内置搜索工具
- 配置和使用Codex Deep Search
- 安装和使用agent-browser
- 构建自动化信息收集流程

---

## 第一部分：内置搜索工具（30分钟）

### 1.1 web_fetch - 基础网页抓取

#### 功能介绍
```
web_fetch是OpenClaw的内置工具，用于：
- 抓取网页内容
- 自动提取正文
- 转换为Markdown
- 过滤广告和无关内容
```

#### 基本用法
```bash
openclaw chat "获取 https://docs.openclaw.ai 的内容"
```

#### 提取模式
```
markdown模式（默认）：
- 保留标题层级
- 保留链接
- 保留代码块
- 适合文档和文章

text模式：
- 纯文本
- 无格式
- 适合简单提取
```

#### 实战示例

**示例1：抓取文档**
```
You: 获取OpenClaw官方文档的安装指南
https://docs.openclaw.ai/install

Agent: [使用web_fetch]
# OpenClaw安装指南

## 系统要求
- Node.js 18+
- 2GB RAM
- 500MB磁盘空间

## 安装步骤
1. 安装Node.js
2. 运行 npm install -g openclaw
3. 初始化配置
...
```

**示例2：抓取新闻**
```
You: 总结一下这篇新闻
https://example.com/news/ai-breakthrough

Agent: [使用web_fetch]
[提取正文]
[生成摘要]

这篇新闻报道了AI领域的最新突破：
1. 新模型性能提升50%
2. 成本降低80%
3. 预计明年商用
```

**示例3：批量抓取**
```
You: 帮我抓取这些网站的内容并对比：
- https://site1.com
- https://site2.com
- https://site3.com

Agent: [批量抓取]
[对比分析]

对比结果：
| 网站 | 主要观点 | 数据支持 |
|------|---------|---------|
| Site1 | ... | ... |
| Site2 | ... | ... |
| Site3 | ... | ... |
```

#### 限制和注意事项
```
限制：
- 无法处理JavaScript渲染
- 无法登录
- 无法处理验证码
- 可能被反爬虫拦截

解决方案：
- JavaScript渲染 → 使用browser工具
- 需要登录 → 使用agent-browser
- 反爬虫 → 添加延迟、更换User-Agent
```

### 1.2 browser - 浏览器控制

#### 功能介绍
```
browser工具可以：
- 控制真实浏览器
- 处理JavaScript渲染
- 支持点击、输入、截图
- 保持登录态
```

#### 基本操作

**打开网页**
```
You: 打开 https://github.com

Agent: [使用browser]
[打开浏览器]
[导航到GitHub]
✅ 已打开
```

**截图**
```
You: 截图保存

Agent: [截图]
✅ 已保存到 screenshot.png
```

**交互操作**
```
You: 在GitHub上搜索 openclaw

Agent: [点击搜索框]
[输入 "openclaw"]
[按回车]
[等待加载]
✅ 搜索完成

找到以下结果：
1. openclaw/openclaw - 官方仓库
2. ...
```

#### 高级功能

**快照（snapshot）**
```
You: 获取页面结构

Agent: [使用browser.snapshot]
页面结构：
- 导航栏
  - Logo
  - 搜索框
  - 用户菜单
- 主内容区
  - 仓库列表
  - 侧边栏
...
```

**自动化流程**
```
You: 帮我在GitHub上创建一个Issue

Agent: [打开仓库]
[点击 Issues]
[点击 New Issue]
[填写标题和内容]
[点击 Submit]
✅ Issue已创建
```

---

## 第二部分：Codex Deep Search（40分钟）

### 2.1 什么是Codex Deep Search？

#### 功能特点
```
Codex Deep Search是一个强大的搜索skill：
- 多源信息综合
- 深度内容分析
- 后台执行
- Telegram回调
- 自动生成报告
```

#### 与普通搜索的区别
```
普通搜索（web_fetch）：
- 单个网页
- 表面信息
- 即时返回

Codex Deep Search：
- 多个来源
- 深度分析
- 后台执行
- 综合报告
```

### 2.2 安装和配置

#### 安装skill
```bash
openclaw skills install codex-deep-search
```

#### 配置Codex CLI
```bash
# 安装Codex CLI
npm install -g @codexai/cli

# 配置API密钥
codex config set apiKey YOUR_API_KEY
```

**注意：** Codex CLI需要Anthropic官方API密钥，不支持MixAI等代理。

#### 配置Telegram回调（可选）
```json
{
  "channels": {
    "telegram": {
      "token": "YOUR_TELEGRAM_BOT_TOKEN"
    }
  },
  "skills": {
    "entries": {
      "codex-deep-search": {
        "notifyChannel": "telegram",
        "notifyUser": "YOUR_TELEGRAM_USER_ID"
      }
    }
  }
}
```

### 2.3 使用方法

#### 基本搜索
```
You: 深度搜索：OpenClaw的最佳实践

Agent: [启动Codex Deep Search]
✅ 搜索任务已启动
预计耗时：2-5分钟
完成后会通过Telegram通知你

[后台执行]
1. 搜索相关网页
2. 抓取内容
3. 分析整理
4. 生成报告

[Telegram通知]
🔍 深度搜索完成

OpenClaw最佳实践报告：

1. 模型选择
   - 日常任务用DeepSeek
   - 复杂任务用Claude
   - 来源：docs.openclaw.ai

2. 记忆管理
   - 定期蒸馏
   - 分层存储
   - 来源：github.com/openclaw

3. 成本优化
   - 智能路由
   - 缓存策略
   - 来源：community.openclaw.ai

完整报告已保存到：
~/.openclaw/workspace/reports/openclaw-best-practices.md
```

#### 高级搜索
```
You: 深度搜索并对比：
- Claude vs GPT-4
- 性能、成本、适用场景
- 包含最新数据

Agent: [启动深度搜索]
✅ 任务已启动

[搜索策略]
1. 官方文档
2. 技术博客
3. Reddit讨论
4. Twitter观点
5. Benchmark数据

[生成报告]
# Claude vs GPT-4 深度对比

## 性能对比
| 指标 | Claude Sonnet 4 | GPT-4 Turbo |
|------|----------------|-------------|
| 代码生成 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 推理能力 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 创意写作 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

## 成本对比
...

## 社区观点
...

## 推荐场景
...
```

### 2.4 实战案例

#### 案例1：技术调研
```
任务：调研Rust语言的学习路径

You: 深度搜索：Rust语言学习路径
要求：
- 初学者友好
- 包含实战项目
- 推荐学习资源

Agent: [深度搜索]
[综合多个来源]
[生成学习路线图]

Rust学习路径报告：

第一阶段：基础入门（2-4周）
- 官方教程：The Rust Book
- 练习平台：Rustlings
- 视频课程：...

第二阶段：进阶实战（1-2个月）
- 项目1：CLI工具
- 项目2：Web服务
- 项目3：系统编程

第三阶段：深入专题（持续）
- 异步编程
- 宏系统
- 不安全代码

推荐资源：
1. 官方文档：...
2. 社区论坛：...
3. 开源项目：...
```

#### 案例2：市场分析
```
任务：分析AI助手市场现状

You: 深度搜索：AI助手市场分析
包含：
- 主要玩家
- 市场规模
- 发展趋势
- 竞争格局

Agent: [深度搜索]
[收集数据]
[分析整理]

AI助手市场分析报告：

市场规模：
- 2024年：$XX亿
- 预计2026年：$XX亿
- 年增长率：XX%

主要玩家：
1. ChatGPT（OpenAI）
   - 市场份额：XX%
   - 特点：...
   
2. Claude（Anthropic）
   - 市场份额：XX%
   - 特点：...

3. Gemini（Google）
   - 市场份额：XX%
   - 特点：...

发展趋势：
1. 多模态融合
2. 垂直领域深化
3. 成本持续下降
4. 开源生态繁荣

竞争格局：
...
```

---

## 第三部分：agent-browser（30分钟）

### 3.1 什么是agent-browser？

#### 功能特点
```
agent-browser是一个增强的浏览器工具：
- 自动化网页操作
- 登录态保持
- 复杂交互
- 数据提取
```

#### 与browser的区别
```
browser（内置）：
- 基础浏览器控制
- 简单交互
- 无状态

agent-browser（skill）：
- 高级自动化
- 会话保持
- 智能等待
- 错误重试
```

### 3.2 安装和配置

#### 安装Chromium
```bash
# Linux
sudo apt install chromium-browser

# macOS
brew install chromium

# 或使用系统Chrome
# agent-browser会自动检测
```

#### 安装skill
```bash
openclaw skills install agent-browser
```

#### 配置
```json
{
  "skills": {
    "entries": {
      "agent-browser": {
        "browserPath": "/usr/bin/chromium",
        "userDataDir": "~/.openclaw/browser-data",
        "headless": false
      }
    }
  }
}
```

### 3.3 使用方法

#### 登录网站
```
You: 帮我登录GitHub

Agent: [使用agent-browser]
[打开GitHub登录页]
请输入用户名和密码

You: 
用户名：myusername
密码：mypassword

Agent: [填写表单]
[点击登录]
[等待跳转]
✅ 登录成功

会话已保存，下次无需重新登录
```

#### 自动化操作
```
You: 在GitHub上给openclaw/openclaw仓库点Star

Agent: [使用agent-browser]
[打开仓库页面]
[查找Star按钮]
[点击]
✅ 已点Star

当前Stars：1,234 → 1,235
```

#### 数据提取
```
You: 抓取GitHub Trending的前10个仓库

Agent: [使用agent-browser]
[打开Trending页面]
[提取数据]

GitHub Trending Top 10：

1. user/repo1
   - Stars: 1,234
   - Language: Python
   - Description: ...

2. user/repo2
   - Stars: 987
   - Language: JavaScript
   - Description: ...

...

数据已保存到：trending.json
```

### 3.4 高级功能

#### 表单填写
```
You: 帮我填写这个表单
https://example.com/form

数据：
- 姓名：张三
- 邮箱：zhangsan@example.com
- 电话：138-0000-0000

Agent: [使用agent-browser]
[打开表单]
[自动填写]
[提交]
✅ 表单已提交
```

#### 定时任务
```
You: 每天早上9点检查GitHub通知

Agent: [配置定时任务]
✅ 已设置

任务详情：
- 时间：每天09:00
- 操作：登录GitHub → 检查通知 → 发送摘要
- 通知渠道：Telegram
```

---

## 第四部分：自动化信息收集（30分钟）

### 4.1 RSS订阅监控

#### 配置RSS源
```json
{
  "automation": {
    "rss": {
      "feeds": [
        {
          "url": "https://blog.openclaw.ai/feed",
          "name": "OpenClaw Blog",
          "checkInterval": "1h"
        },
        {
          "url": "https://news.ycombinator.com/rss",
          "name": "Hacker News",
          "checkInterval": "30m"
        }
      ]
    }
  }
}
```

#### 自动摘要
```
[定时检查RSS]
[发现新文章]
[自动抓取内容]
[生成摘要]
[发送通知]

Telegram通知：
📰 OpenClaw Blog 更新

标题：OpenClaw 2.0发布
摘要：
- 新增多Agent协作
- 性能提升50%
- 支持更多模型

阅读全文：https://...
```

### 4.2 网站变化监控

#### 监控配置
```json
{
  "automation": {
    "monitor": {
      "sites": [
        {
          "url": "https://docs.openclaw.ai",
          "selector": ".content",
          "checkInterval": "6h",
          "notifyOnChange": true
        }
      ]
    }
  }
}
```

#### 变化通知
```
[检测到变化]
[对比差异]
[生成报告]

Telegram通知：
🔔 网站更新检测

网站：OpenClaw文档
变化：
+ 新增：记忆系统配置指南
+ 更新：模型选择策略
- 删除：旧版安装指南

查看详情：...
```

### 4.3 竞品监控

#### 监控策略
```
监控内容：
1. 产品更新
2. 价格变化
3. 功能对比
4. 用户反馈

数据来源：
- 官网
- 博客
- Twitter
- Reddit
- GitHub
```

#### 自动报告
```
每周竞品分析报告：

本周更新：
1. ChatGPT
   - 新增：语音对话
   - 价格：保持不变
   
2. Claude
   - 新增：200K上下文
   - 价格：下调20%

3. Gemini
   - 新增：视频理解
   - 价格：保持不变

趋势分析：
- 上下文长度竞赛
- 价格持续下降
- 多模态成标配

建议：
...
```

---

## 第五部分：实战项目（30分钟）

### 项目：自动化技术资讯收集系统

#### 需求
1. 监控多个技术网站
2. 自动抓取和分析
3. 生成每日摘要
4. 发送到Telegram

#### 实现步骤

**步骤1：配置数据源**
```json
{
  "sources": [
    {
      "name": "Hacker News",
      "url": "https://news.ycombinator.com",
      "type": "rss"
    },
    {
      "name": "GitHub Trending",
      "url": "https://github.com/trending",
      "type": "scrape"
    },
    {
      "name": "Reddit r/programming",
      "url": "https://reddit.com/r/programming",
      "type": "api"
    }
  ]
}
```

**步骤2：设置抓取规则**
```
You: 帮我设置自动化资讯收集

Agent: [配置规则]
✅ 已设置

收集规则：
1. 每天早上8点抓取
2. 筛选热门内容（>100赞）
3. 生成摘要
4. 发送到Telegram

数据源：
- Hacker News（RSS）
- GitHub Trending（Scrape）
- Reddit Programming（API）
```

**步骤3：测试运行**
```
You: 测试一下

Agent: [执行抓取]
[分析内容]
[生成报告]

📰 今日技术资讯（测试）

Hacker News Top 3：
1. 新AI模型突破
   - 赞：234
   - 评论：89
   - 链接：...

2. Rust 1.75发布
   - 赞：189
   - 评论：45
   - 链接：...

GitHub Trending：
1. user/awesome-project
   - Stars：+1,234 today
   - Language：Python
   
Reddit热议：
1. 讨论：AI的未来
   - 赞：567
   - 评论：123

完整报告：...
```

**步骤4：自动化运行**
```
[每天8:00自动执行]
[收集数据]
[生成报告]
[发送通知]

Telegram每日推送：
📰 今日技术资讯

[内容摘要]
...

查看完整报告：
~/.openclaw/workspace/reports/tech-news-2026-03-09.md
```

---

## 第六部分：作业与练习（课后）

### 作业1：使用web_fetch（必做）

**任务：**
1. 抓取3个不同类型的网页
2. 提取关键信息
3. 生成对比报告

**网页类型：**
- 技术文档
- 新闻文章
- 博客文章

**提交：**
- 抓取命令
- 提取结果
- 对比报告

### 作业2：配置Codex Deep Search（必做）

**任务：**
1. 安装并配置Codex Deep Search
2. 执行一次深度搜索
3. 分析搜索结果

**搜索主题（任选一个）：**
- AI模型对比
- 编程语言学习路径
- 技术栈选择

**提交：**
- 配置截图
- 搜索结果
- 分析报告

### 作业3：自动化信息收集（选做）

**任务：**
设计一个自动化信息收集系统

**要求：**
1. 至少3个数据源
2. 自动抓取和分析
3. 定时生成报告
4. 通知推送

**提交：**
- 系统设计文档
- 配置文件
- 运行截图
- 示例报告

---

## 第七部分：常见问题（10分钟）

### Q1：web_fetch抓取失败怎么办？

**A1：**
```
常见原因：
1. 网站反爬虫
2. 需要JavaScript渲染
3. 需要登录
4. 网络问题

解决方案：
1. 反爬虫 → 添加延迟、更换User-Agent
2. JavaScript → 使用browser工具
3. 需要登录 → 使用agent-browser
4. 网络问题 → 检查连接、使用代理
```

### Q2：Codex Deep Search很慢？

**A2：**
```
原因：
- 需要搜索多个来源
- 需要深度分析
- 后台执行

优化：
1. 使用Telegram回调，不用等待
2. 缩小搜索范围
3. 限制来源数量
4. 使用缓存
```

### Q3：agent-browser无法登录？

**A3：**
```bash
# 检查浏览器
which chromium

# 检查配置
cat ~/.openclaw/openclaw.json | grep agent-browser

# 手动测试
chromium --version

# 查看日志
openclaw gateway logs | grep agent-browser
```

### Q4：如何避免被封IP？

**A4：**
```
策略：
1. 添加随机延迟
2. 使用代理IP池
3. 模拟真实用户行为
4. 遵守robots.txt
5. 降低请求频率

配置：
{
  "scraping": {
    "delay": "2-5s",
    "userAgent": "Mozilla/5.0...",
    "respectRobotsTxt": true
  }
}
```

### Q5：如何提高搜索质量？

**A5：**
```
技巧：
1. 明确搜索目标
2. 使用关键词
3. 指定数据源
4. 设置筛选条件
5. 多次迭代优化

示例：
You: 深度搜索：Rust学习路径
要求：
- 针对初学者
- 包含实战项目
- 来源：官方文档+社区推荐
- 排除：过时内容
```

---

## 第八部分：扩展阅读

### 推荐资源

#### 工具文档
- web_fetch：https://docs.openclaw.ai/tools/web-fetch
- browser：https://docs.openclaw.ai/tools/browser
- Codex CLI：https://docs.codex.ai

#### Skills
- codex-deep-search：https://github.com/openclaw/skills
- agent-browser：https://clawhub.com

#### 爬虫技术
- Playwright：https://playwright.dev
- Puppeteer：https://pptr.dev
- Scrapy：https://scrapy.org

### 下节课预告

**第8课：自动化工作流 - 解放双手**
- Heartbeat机制
- Cron任务
- 工作流设计
- 实战案例

---

## 课程总结

### 本节课你学到了：
✅ 内置搜索工具（web_fetch/browser）  
✅ Codex Deep Search的配置和使用  
✅ agent-browser的高级功能  
✅ 自动化信息收集系统  
✅ 实战项目开发  

### 关键要点：
1. **web_fetch适合简单抓取**
2. **browser适合JavaScript渲染**
3. **Codex Deep Search适合深度研究**
4. **agent-browser适合复杂自动化**
5. **组合使用效果最好**

### 下一步：
1. 完成作业1和作业2（必做）
2. 尝试作业3（选做）
3. 探索更多搜索技巧
4. 准备学习第8课（自动化工作流）

---

**课程反馈：**
如有问题或建议，请在GitHub提Issue或加入社区讨论。

**下节课见！** 🚀
