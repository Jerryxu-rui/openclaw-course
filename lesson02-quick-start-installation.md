# 第2课：快速上手 - 安装与基础配置

## 课程目标
- 完成OpenClaw环境搭建
- 理解核心概念（Gateway、Agent、Session、Workspace）
- 掌握基础配置方法
- 配置至少2个AI模型并测试

---

## 第一部分：安装部署（30分钟）

### 1.1 系统要求

#### 最低配置
- **操作系统**：Linux/macOS/Windows 10+
- **Node.js**：v18.0.0 或更高
- **内存**：2GB RAM
- **磁盘**：500MB 可用空间
- **网络**：稳定的互联网连接

#### 推荐配置
- **操作系统**：Ubuntu 22.04 / macOS 13+ / Windows 11
- **Node.js**：v22.x（最新LTS版本）
- **内存**：4GB+ RAM
- **磁盘**：2GB+ 可用空间
- **网络**：支持访问国际API（或使用国内代理）

### 1.2 安装Node.js

#### Linux (Ubuntu/Debian)
```bash
# 使用nvm安装（推荐）
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc
nvm install 22
nvm use 22

# 验证安装
node --version  # 应显示 v22.x.x
npm --version   # 应显示 10.x.x
```

#### macOS
```bash
# 使用Homebrew安装
brew install node@22

# 或使用nvm（推荐）
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.zshrc
nvm install 22
nvm use 22
```

#### Windows
```powershell
# 下载并安装Node.js
# 访问：https://nodejs.org/
# 下载LTS版本（v22.x）并安装

# 验证安装
node --version
npm --version
```

### 1.3 安装OpenClaw

#### 全局安装（推荐）
```bash
npm install -g openclaw

# 验证安装
openclaw --version
```

#### 常见问题排查

**问题1：权限错误（Linux/macOS）**
```bash
# 错误：EACCES: permission denied
# 解决：使用nvm或修改npm全局目录
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

**问题2：网络超时**
```bash
# 使用国内镜像
npm config set registry https://registry.npmmirror.com
npm install -g openclaw
```

**问题3：Node版本过低**
```bash
# 升级Node.js
nvm install 22
nvm use 22
nvm alias default 22
```

### 1.4 初始化工作区

```bash
# 创建工作目录
mkdir -p ~/.openclaw/workspace
cd ~/.openclaw/workspace

# 初始化配置
openclaw init

# 查看目录结构
tree ~/.openclaw
```

**预期输出：**
```
~/.openclaw/
├── openclaw.json          # 主配置文件
├── workspace/             # 工作区
│   ├── AGENTS.md         # Agent行为指南
│   ├── SOUL.md           # 个性配置
│   ├── USER.md           # 用户信息
│   ├── IDENTITY.md       # Agent身份
│   ├── TOOLS.md          # 工具配置
│   ├── HEARTBEAT.md      # 心跳任务
│   ├── BOOTSTRAP.md      # 首次启动指南
│   └── MEMORY.md         # 长期记忆
└── skills/               # 技能目录
```

---

## 第二部分：核心概念（20分钟）

### 2.1 Gateway（网关）

#### 什么是Gateway？
Gateway是OpenClaw的核心服务，负责：
- 接收和分发消息
- 管理Agent会话
- 处理API调用
- 连接外部服务（飞书、Telegram等）

#### Gateway架构
```
外部世界（飞书/Telegram/Web）
         ↓
    Gateway（网关）
         ↓
    Agent（智能体）
         ↓
    Tools（工具）
         ↓
    外部API（OpenAI/Claude/DeepSeek）
```

#### 启动Gateway
```bash
# 启动Gateway
openclaw gateway start

# 查看状态
openclaw gateway status

# 查看日志
openclaw gateway logs

# 停止Gateway
openclaw gateway stop

# 重启Gateway
openclaw gateway restart
```

### 2.2 Agent（智能体）

#### 什么是Agent？
Agent是你的AI助手，具有：
- **记忆**：记住你的对话和偏好
- **工具**：可以执行文件操作、网页抓取等
- **技能**：通过Skills扩展能力
- **个性**：可以自定义性格和行为

#### Agent的核心文件
```markdown
SOUL.md       # 定义Agent的个性和价值观
USER.md       # 记录用户信息和偏好
MEMORY.md     # 长期记忆存储
AGENTS.md     # Agent行为规则
IDENTITY.md   # Agent的身份信息
```

#### Agent的生命周期
```
启动 → 读取配置 → 加载记忆 → 处理请求 → 更新记忆 → 休眠
```

### 2.3 Session（会话）

#### 什么是Session？
Session是一次完整的对话上下文，包含：
- 对话历史
- 上下文信息
- 临时状态
- Token使用统计

#### Session类型
- **主会话**：与用户的直接对话
- **子会话**：Sub-Agent创建的独立会话
- **后台会话**：定时任务或自动化流程

#### 查看Session
```bash
# 列出所有会话
openclaw sessions list

# 查看会话历史
openclaw sessions history <session-key>

# 发送消息到会话
openclaw sessions send <session-key> "你好"
```

### 2.4 Workspace（工作区）

#### 什么是Workspace？
Workspace是Agent的工作目录，存储：
- 配置文件
- 记忆文件
- 临时文件
- 生成的文档

#### Workspace结构
```
~/.openclaw/workspace/
├── AGENTS.md              # Agent行为指南
├── SOUL.md                # 个性配置
├── USER.md                # 用户信息
├── MEMORY.md              # 长期记忆
├── TOOLS.md               # 工具配置
├── HEARTBEAT.md           # 心跳任务
├── memory/                # 记忆目录
│   ├── 2026-03-09.md     # 每日日志
│   ├── distilled/        # 蒸馏后的记忆
│   └── embeddings/       # 向量嵌入
└── projects/             # 项目文件
```

#### Workspace最佳实践
1. **定期备份**：使用git管理workspace
2. **清理临时文件**：定期删除不需要的文件
3. **组织记忆**：按日期和主题分类
4. **版本控制**：重要配置使用git追踪

---

## 第三部分：基础配置（40分钟）

### 3.1 配置文件结构

#### openclaw.json 核心配置
```json
{
  "gateway": {
    "port": 3000,
    "host": "localhost",
    "token": "your-gateway-token"
  },
  "models": {
    "default": "mixai/claude-sonnet-4-6",
    "providers": {
      "mixai": {
        "apiKey": "sk-xxx",
        "baseURL": "https://mixai.cc/v1"
      },
      "deepseek": {
        "apiKey": "sk-xxx",
        "baseURL": "https://api.deepseek.com"
      }
    }
  },
  "workspace": {
    "path": "~/.openclaw/workspace"
  }
}
```

### 3.2 模型配置实战

#### 配置MixAI（Claude代理）

**步骤1：获取API密钥**
1. 访问 https://mixai.cc
2. 注册账号
3. 充值（建议先充值50元测试）
4. 复制API密钥

**步骤2：配置模型**
```bash
# 编辑配置文件
nano ~/.openclaw/openclaw.json
```

```json
{
  "models": {
    "default": "mixai/claude-sonnet-4-6",
    "providers": {
      "mixai": {
        "apiKey": "sk-AkgyrqakyhST8d2G",
        "baseURL": "https://mixai.cc/v1"
      }
    },
    "aliases": {
      "claude-sonnet-4-6": "mixai/claude-sonnet-4-6"
    }
  }
}
```

**步骤3：测试连接**
```bash
# 重启Gateway
openclaw gateway restart

# 测试对话
openclaw chat "你好，请介绍一下自己"
```

#### 配置DeepSeek（性价比之王）

**步骤1：获取API密钥**
1. 访问 https://platform.deepseek.com
2. 注册账号
3. 创建API密钥
4. 充值（建议先充值10元测试）

**步骤2：添加配置**
```json
{
  "models": {
    "providers": {
      "deepseek": {
        "apiKey": "sk-xxx",
        "baseURL": "https://api.deepseek.com"
      }
    },
    "aliases": {
      "deepseek-chat": "deepseek/deepseek-chat"
    }
  }
}
```

**步骤3：测试**
```bash
openclaw chat --model deepseek-chat "写一个Python快速排序"
```

#### 配置Gemini（Google）

**步骤1：获取API密钥**
1. 访问 https://aistudio.google.com/apikey
2. 创建API密钥
3. 复制密钥

**步骤2：配置**
```json
{
  "models": {
    "providers": {
      "google": {
        "apiKey": "AIzaSy-xxx"
      }
    },
    "aliases": {
      "gemini": "google/gemini-3-pro-preview",
      "gemini-flash": "google/gemini-3-flash-preview"
    }
  }
}
```

### 3.3 多模型配置示例

```json
{
  "models": {
    "default": "mixai/claude-sonnet-4-6",
    "providers": {
      "mixai": {
        "apiKey": "sk-xxx",
        "baseURL": "https://mixai.cc/v1"
      },
      "deepseek": {
        "apiKey": "sk-xxx",
        "baseURL": "https://api.deepseek.com"
      },
      "google": {
        "apiKey": "AIzaSy-xxx"
      },
      "minimax": {
        "apiKey": "xxx",
        "baseURL": "https://api.minimax.chat/v1"
      }
    },
    "aliases": {
      "claude-sonnet-4-6": "mixai/claude-sonnet-4-6",
      "deepseek-chat": "deepseek/deepseek-chat",
      "gemini": "google/gemini-3-pro-preview",
      "gemini-flash": "google/gemini-3-flash-preview",
      "minimax": "minimax/MiniMax-M2.5"
    }
  }
}
```

### 3.4 创建第一个Agent

#### 方法1：使用BOOTSTRAP.md（推荐）

```bash
# 启动Gateway
openclaw gateway start

# 首次对话会触发BOOTSTRAP.md
openclaw chat "你好"
```

Agent会引导你完成：
1. 选择名字
2. 定义个性
3. 配置用户信息
4. 选择emoji

#### 方法2：手动配置

**编辑IDENTITY.md**
```markdown
# IDENTITY.md - Who Am I?

- **Name:** Kiro
- **Creature:** AI助手
- **Vibe:** 专业、友好、高效
- **Emoji:** 🤖
- **Avatar:** https://example.com/avatar.png
```

**编辑SOUL.md**
```markdown
# SOUL.md - Who You Are

## Core Truths

**Be genuinely helpful, not performatively helpful.**
直接帮助，不要废话。

**Have opinions.**
可以有自己的观点和偏好。

**Be resourceful before asking.**
先尝试解决，再寻求帮助。
```

**编辑USER.md**
```markdown
# USER.md - About Your Human

- **Name:** Jerry
- **What to call them:** Jerry
- **Timezone:** Asia/Shanghai
- **Notes:** 喜欢简洁高效的回复
```

---

## 第四部分：实战演示（30分钟）

### 4.1 测试不同模型

#### 测试Claude Sonnet 4
```bash
openclaw chat --model claude-sonnet-4-6 "请用中文写一首关于春天的诗"
```

#### 测试DeepSeek
```bash
openclaw chat --model deepseek-chat "请用中文写一首关于春天的诗"
```

#### 测试Gemini Flash
```bash
openclaw chat --model gemini-flash "请用中文写一首关于春天的诗"
```

#### 对比结果
| 模型 | 响应速度 | 质量 | 成本 | 适用场景 |
|------|---------|------|------|---------|
| Claude Sonnet 4 | 中等 | 最高 | 高 | 复杂任务、创意写作 |
| DeepSeek Chat | 快 | 高 | 极低 | 日常对话、代码生成 |
| Gemini Flash | 最快 | 中等 | 低 | 快速查询、简单任务 |

### 4.2 配置验证

#### 检查Gateway状态
```bash
openclaw gateway status
```

**预期输出：**
```
✅ Gateway is running
   PID: 12345
   Port: 3000
   Uptime: 5 minutes
   Memory: 150MB
```

#### 检查模型配置
```bash
openclaw models list
```

**预期输出：**
```
Available models:
  ✅ mixai/claude-sonnet-4-6 (default)
  ✅ deepseek/deepseek-chat
  ✅ google/gemini-3-pro-preview
  ✅ google/gemini-3-flash-preview

Aliases:
  claude-sonnet-4-6 → mixai/claude-sonnet-4-6
  deepseek-chat → deepseek/deepseek-chat
  gemini → google/gemini-3-pro-preview
  gemini-flash → google/gemini-3-flash-preview
```

#### 检查工作区
```bash
ls -la ~/.openclaw/workspace/
```

**预期输出：**
```
AGENTS.md
SOUL.md
USER.md
IDENTITY.md
TOOLS.md
HEARTBEAT.md
MEMORY.md
memory/
```

### 4.3 第一次完整对话

```bash
# 启动交互式对话
openclaw chat
```

**示例对话：**
```
You: 你好，请介绍一下自己

Agent: 你好！我是Kiro，你的AI助手。我可以帮你：
- 处理文档（Word、PDF、Excel）
- 搜索和整理信息
- 编写和调试代码
- 自动化日常任务
- 管理知识和记忆

我使用Claude Sonnet 4模型，擅长复杂推理和创意任务。
有什么我可以帮你的吗？

You: 帮我创建一个待办事项列表

Agent: 好的，我会在workspace中创建一个待办事项文件。

[Agent创建文件：~/.openclaw/workspace/todo.md]

✅ 已创建待办事项列表：~/.openclaw/workspace/todo.md

你可以随时让我添加、修改或查看待办事项。

You: 谢谢！

Agent: 不客气！有需要随时找我。
```

---

## 第五部分：常见问题（20分钟）

### 5.1 安装问题

#### Q1：npm install -g openclaw 失败
**A1：**
```bash
# 方案1：使用国内镜像
npm config set registry https://registry.npmmirror.com
npm install -g openclaw

# 方案2：使用cnpm
npm install -g cnpm --registry=https://registry.npmmirror.com
cnpm install -g openclaw

# 方案3：使用yarn
npm install -g yarn
yarn global add openclaw
```

#### Q2：Gateway启动失败
**A2：**
```bash
# 检查端口占用
lsof -i :3000

# 杀死占用进程
kill -9 <PID>

# 或更换端口
openclaw gateway start --port 3001
```

#### Q3：找不到openclaw命令
**A3：**
```bash
# 检查PATH
echo $PATH

# 添加npm全局bin到PATH
echo 'export PATH="$HOME/.npm-global/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# 或使用npx
npx openclaw --version
```

### 5.2 配置问题

#### Q1：API密钥无效
**A1：**
```bash
# 检查配置文件
cat ~/.openclaw/openclaw.json

# 验证API密钥
curl -H "Authorization: Bearer sk-xxx" \
     https://mixai.cc/v1/models

# 重新配置
openclaw config set models.providers.mixai.apiKey "sk-new-key"
```

#### Q2：模型调用失败
**A2：**
```bash
# 查看详细日志
openclaw gateway logs --level debug

# 测试网络连接
curl https://mixai.cc/v1/models

# 检查余额
# 访问对应平台查看账户余额
```

#### Q3：配置文件损坏
**A3：**
```bash
# 备份当前配置
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak

# 重新初始化
openclaw init --force

# 恢复配置
# 手动编辑 ~/.openclaw/openclaw.json
```

### 5.3 使用问题

#### Q1：Agent不记得之前的对话
**A1：**
```bash
# 检查MEMORY.md是否存在
ls ~/.openclaw/workspace/MEMORY.md

# 检查memory目录
ls ~/.openclaw/workspace/memory/

# 手动创建记忆文件
touch ~/.openclaw/workspace/MEMORY.md
mkdir -p ~/.openclaw/workspace/memory
```

#### Q2：响应速度慢
**A2：**
```bash
# 切换到更快的模型
openclaw chat --model gemini-flash "你好"

# 或配置默认模型为Gemini Flash
openclaw config set models.default "google/gemini-3-flash-preview"
```

#### Q3：Token消耗过快
**A3：**
```bash
# 查看Token使用统计
openclaw status

# 启用记忆蒸馏（第6课详细讲解）
# 切换到更便宜的模型
openclaw config set models.default "deepseek/deepseek-chat"
```

---

## 第六部分：作业与练习（课后）

### 作业1：完成安装配置（必做）

**任务：**
1. 安装OpenClaw
2. 配置至少2个AI模型（推荐：MixAI + DeepSeek）
3. 完成首次对话
4. 截图提交

**验收标准：**
- Gateway成功启动
- 至少2个模型可用
- 完成10轮以上对话

### 作业2：模型对比测试（必做）

**任务：**
用相同的问题测试不同模型，对比：
- 响应速度
- 回答质量
- Token消耗
- 成本估算

**测试问题：**
1. "请用中文写一首关于春天的诗"
2. "写一个Python快速排序算法"
3. "总结一下《三体》的主要情节"

**提交格式：**
```markdown
## 模型对比报告

### 测试1：写诗
- Claude Sonnet 4：[响应时间] [质量评分] [Token数]
- DeepSeek Chat：[响应时间] [质量评分] [Token数]
- Gemini Flash：[响应时间] [质量评分] [Token数]

### 测试2：代码生成
...

### 结论
...
```

### 作业3：自定义Agent（选做）

**任务：**
根据自己的需求，自定义Agent的：
- 名字和emoji
- 个性和风格
- 用户信息

**提交：**
- IDENTITY.md
- SOUL.md
- USER.md

---

## 第七部分：扩展阅读

### 推荐资源

#### 官方文档
- OpenClaw官方文档：https://docs.openclaw.ai
- GitHub仓库：https://github.com/openclaw/openclaw
- Discord社区：https://discord.com/invite/clawd

#### 模型平台
- MixAI：https://mixai.cc
- DeepSeek：https://platform.deepseek.com
- Google AI Studio：https://aistudio.google.com
- Minimax：https://www.minimaxi.com

#### 学习资源
- OpenClaw Skills Hub：https://clawhub.com
- 本课程GitHub：https://github.com/Jerryxu-rui/openclaw-course

### 下节课预告

**第3课：核心功能 - 工具与技能系统**
- 内置工具详解（read/write/exec/browser）
- Skills系统深度解析
- 常用Skills推荐与实战
- 飞书/Telegram集成预览

---

## 课程总结

### 本节课你学到了：
✅ OpenClaw的安装部署  
✅ 核心概念（Gateway、Agent、Session、Workspace）  
✅ 基础配置方法  
✅ 多模型配置与测试  
✅ 常见问题排查  

### 下一步：
1. 完成作业1和作业2
2. 熟悉OpenClaw的基本操作
3. 准备学习第3课（工具与技能系统）

### 学习建议：
- 多动手实践，不要只看不做
- 遇到问题先查文档，再问社区
- 记录自己的配置和经验
- 加入Discord/飞书群交流

---

**课程反馈：**
如有问题或建议，请在GitHub提Issue或加入社区讨论。

**下节课见！** 🚀
