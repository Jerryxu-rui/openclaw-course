# 第4课：多渠道接入 - 让AI无处不在

## 课程目标
- 完成飞书集成的完整配置
- 创建并配置Telegram Bot
- 了解WhatsApp/Discord接入方法
- 实现多渠道消息同步

---

## 第一部分：飞书集成完整配置（40分钟）

### 1.1 创建飞书应用

#### 步骤1：注册飞书开发者账号
1. 访问 https://open.feishu.cn
2. 使用飞书账号登录
3. 进入"开发者后台"

#### 步骤2：创建企业自建应用
```
开发者后台 → 创建应用 → 企业自建应用
- 应用名称：OpenClaw Bot
- 应用描述：AI助手
- 应用图标：上传logo
```

#### 步骤3：获取凭证
```
应用详情 → 凭证与基础信息
- App ID：cli_xxxxxxxxx
- App Secret：xxxxxxxxx
```

**保存这两个值，后面配置需要用到！**

### 1.2 配置应用权限

#### 必需权限（Scopes）
```
消息与群组：
- im:message（发送消息）
- im:message.group_at_msg（接收群聊@消息）
- im:message.p2p_msg（接收私聊消息）
- im:chat（获取群信息）

通讯录：
- contact:user.base（获取用户基本信息）

云文档：
- docx:document（文档读写）
- wiki:wiki（知识库访问）
- drive:drive（云空间操作）
- bitable:app（多维表格）
```

#### 配置步骤
```
应用详情 → 权限管理 → 添加权限
1. 搜索并勾选上述权限
2. 点击"申请权限"
3. 等待管理员审批（如果你是管理员，直接通过）
```

### 1.3 配置事件订阅

#### 方式1：WebSocket（推荐）
```
事件与回调 → 订阅方式 → 使用长连接接收事件/回调
```

**优点：**
- 无需公网IP
- 无需配置回调URL
- 实时接收消息
- 适合本地开发

#### 方式2：Webhook
```
事件与回调 → 订阅方式 → 配置请求网址URL
- 请求网址：https://your-domain.com/feishu/webhook
- 加密方式：不加密（或选择加密）
```

**需要：**
- 公网可访问的域名
- HTTPS证书
- 配置反向代理

#### 订阅事件
```
事件与回调 → 事件订阅 → 添加事件
必选事件：
- 接收消息（im.message.receive_v1）
- 消息已读（im.message.message_read_v1）

可选事件：
- 群聊信息变更（im.chat.updated_v1）
- 用户进出群（im.chat.member.user.added_v1）
```

### 1.4 OpenClaw配置

#### 编辑配置文件
```bash
nano ~/.openclaw/openclaw.json
```

#### 添加飞书配置
```json
{
  "channels": {
    "feishu": {
      "appId": "cli_xxxxxxxxx",
      "appSecret": "xxxxxxxxx",
      "respondToAll": false,
      "mode": "websocket"
    }
  }
}
```

**配置说明：**
- `appId`: 飞书应用ID
- `appSecret`: 飞书应用密钥
- `respondToAll`: 是否响应所有消息（false=仅响应@消息）
- `mode`: 连接模式（websocket或webhook）

#### 重启Gateway
```bash
openclaw gateway restart
```

#### 验证连接
```bash
# 查看日志
openclaw gateway logs | grep feishu

# 应该看到类似输出：
# [feishu] feishu[default]: WebSocket client started
# [feishu] feishu[default]: bot open_id resolved
```

### 1.5 测试飞书集成

#### 测试1：私聊
```
1. 在飞书中搜索你的Bot名称
2. 发送消息："你好"
3. Bot应该回复
```

#### 测试2：群聊
```
1. 创建一个测试群
2. 添加Bot到群
3. @Bot 发送消息："介绍一下自己"
4. Bot应该回复
```

#### 测试3：文档操作
```
在飞书中对Bot说：
"读取这个文档的内容"
[分享一个飞书文档链接]

Bot应该能读取并总结文档内容
```

### 1.6 飞书高级功能

#### 消息卡片
```json
{
  "msg_type": "interactive",
  "card": {
    "header": {
      "title": {
        "content": "任务提醒",
        "tag": "plain_text"
      }
    },
    "elements": [
      {
        "tag": "div",
        "text": {
          "content": "你有3个待办任务",
          "tag": "plain_text"
        }
      },
      {
        "tag": "action",
        "actions": [
          {
            "tag": "button",
            "text": {
              "content": "查看详情",
              "tag": "plain_text"
            },
            "type": "primary"
          }
        ]
      }
    ]
  }
}
```

#### 文件上传
```
You: [上传文件到飞书]
请帮我分析这个Excel

Agent: [下载文件]
[分析数据]
这个Excel包含...
```

---

## 第二部分：Telegram集成（30分钟）

### 2.1 创建Telegram Bot

#### 步骤1：找到BotFather
```
1. 在Telegram中搜索 @BotFather
2. 发送 /start
3. 发送 /newbot
```

#### 步骤2：配置Bot
```
BotFather: What name would you like for your bot?
You: OpenClaw Assistant

BotFather: What username would you like for your bot?
You: openclaw_assistant_bot

BotFather: Done! Here's your token:
123456789:ABCdefGHIjklMNOpqrsTUVwxyz
```

**保存这个Token！**

#### 步骤3：配置Bot设置
```
/setdescription - 设置Bot描述
/setabouttext - 设置关于文本
/setuserpic - 设置头像
/setcommands - 设置命令列表
```

**推荐命令列表：**
```
start - 开始使用
help - 帮助信息
status - 查看状态
reset - 重置对话
```

### 2.2 OpenClaw配置

#### 添加Telegram配置
```json
{
  "channels": {
    "telegram": {
      "token": "123456789:ABCdefGHIjklMNOpqrsTUVwxyz",
      "mode": "polling"
    }
  }
}
```

**配置说明：**
- `token`: BotFather提供的Token
- `mode`: polling（轮询）或webhook（需要公网IP）

#### 重启Gateway
```bash
openclaw gateway restart
```

### 2.3 测试Telegram Bot

#### 测试1：基本对话
```
You: /start
Bot: 你好！我是OpenClaw助手。

You: 你好
Bot: 你好！有什么可以帮你的吗？
```

#### 测试2：文件处理
```
You: [发送PDF文件]
请总结这个文档

Bot: [处理文件]
这是一份关于...的文档
```

#### 测试3：命令
```
You: /status
Bot: 
📊 系统状态
- 模型：Claude Sonnet 4
- 会话：活跃
- Token使用：1,234
```

### 2.4 Telegram高级功能

#### 内联键盘
```python
# OpenClaw会自动处理，你只需要在回复中包含选项
Agent: 请选择操作：
1. 查看文档
2. 生成报告
3. 数据分析
```

#### 文件下载
```
You: 帮我生成一份报告

Agent: [生成报告]
✅ 报告已生成
[发送文件：report.pdf]
```

---

## 第三部分：其他渠道接入（20分钟）

### 3.1 WhatsApp集成

#### 前置要求
- WhatsApp Business账号
- Meta开发者账号
- 验证的电话号码

#### 配置步骤
```json
{
  "channels": {
    "whatsapp": {
      "phoneNumberId": "123456789",
      "accessToken": "your-access-token",
      "webhookVerifyToken": "your-verify-token"
    }
  }
}
```

#### 特点
- 支持文本、图片、文档
- 支持模板消息
- 需要Meta审核
- 适合客服场景

### 3.2 Discord集成

#### 创建Discord Bot
```
1. 访问 https://discord.com/developers
2. 创建应用
3. 添加Bot
4. 复制Token
```

#### OpenClaw配置
```json
{
  "channels": {
    "discord": {
      "token": "your-discord-bot-token",
      "clientId": "your-client-id"
    }
  }
}
```

#### 邀请Bot到服务器
```
https://discord.com/api/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=8&scope=bot
```

### 3.3 Slack集成

#### 创建Slack App
```
1. 访问 https://api.slack.com/apps
2. 创建新应用
3. 配置Bot Token
4. 订阅事件
```

#### OpenClaw配置
```json
{
  "channels": {
    "slack": {
      "token": "xoxb-your-bot-token",
      "signingSecret": "your-signing-secret"
    }
  }
}
```

### 3.4 iMessage集成（macOS）

#### 前置要求
- macOS系统
- iMessage已登录
- 安装OpenClaw节点

#### 配置步骤
```bash
# 在macOS上安装OpenClaw节点
npm install -g openclaw-node

# 配置iMessage
openclaw node setup --channel imessage
```

---

## 第四部分：多渠道消息同步（20分钟）

### 4.1 统一会话管理

#### 会话隔离
```
每个渠道的会话是独立的：
- 飞书会话：feishu:user:ou_xxx
- Telegram会话：telegram:user:123456
- Discord会话：discord:user:789012
```

#### 跨渠道同步（可选）
```json
{
  "session": {
    "dmScope": "per-user",
    "crossChannel": true
  }
}
```

**效果：**
- 在飞书发送的消息，Telegram也能看到历史
- 跨渠道共享记忆

### 4.2 消息路由

#### 场景1：工作用飞书，个人用Telegram
```json
{
  "channels": {
    "feishu": {
      "enabled": true,
      "workHours": "09:00-18:00"
    },
    "telegram": {
      "enabled": true,
      "workHours": "always"
    }
  }
}
```

#### 场景2：紧急消息多渠道通知
```javascript
// Agent可以同时发送到多个渠道
message({
  action: "send",
  targets: ["feishu:user:xxx", "telegram:user:123"],
  message: "⚠️ 紧急：服务器CPU使用率超过90%"
});
```

### 4.3 渠道特性适配

#### 飞书特性
- ✅ 富文本消息
- ✅ 消息卡片
- ✅ 文档集成
- ✅ 多维表格

#### Telegram特性
- ✅ Markdown格式
- ✅ 内联键盘
- ✅ 文件传输
- ✅ 群组管理

#### Discord特性
- ✅ Embed消息
- ✅ Slash命令
- ✅ 语音频道
- ✅ 角色管理

---

## 第五部分：实战项目（30分钟）

### 项目：多渠道工作助手

#### 需求
1. 飞书接收工作消息
2. Telegram接收个人提醒
3. 自动同步重要信息

#### 实现步骤

**步骤1：配置多渠道**
```json
{
  "channels": {
    "feishu": {
      "appId": "cli_xxx",
      "appSecret": "xxx",
      "respondToAll": false
    },
    "telegram": {
      "token": "123:ABC",
      "mode": "polling"
    }
  }
}
```

**步骤2：设置工作流**
```
在飞书中：
You: 帮我每天早上9点在Telegram提醒我今天的日程

Agent: 好的，我会：
1. 每天9:00读取飞书日历
2. 生成日程摘要
3. 发送到你的Telegram
```

**步骤3：测试同步**
```
在飞书中：
You: 提醒我下午3点开会

Agent: ✅ 已设置提醒
- 时间：今天15:00
- 内容：开会
- 通知渠道：飞书 + Telegram
```

**步骤4：跨渠道查询**
```
在Telegram中：
You: 我今天在飞书上说了什么？

Agent: [搜索飞书会话历史]
今天你在飞书上：
1. 09:30 - 询问项目进度
2. 11:00 - 请求生成报告
3. 14:00 - 设置会议提醒
```

---

## 第六部分：作业与练习（课后）

### 作业1：配置飞书集成（必做）

**任务：**
1. 创建飞书应用
2. 配置权限和事件订阅
3. 在OpenClaw中配置
4. 测试私聊和群聊

**验收标准：**
- 能在飞书中与Bot对话
- Bot能正确响应@消息
- 截图提交对话记录

### 作业2：配置Telegram Bot（必做）

**任务：**
1. 通过BotFather创建Bot
2. 配置OpenClaw
3. 测试基本功能
4. 尝试发送文件

**验收标准：**
- Bot能正常响应
- 能处理文件
- 截图提交对话记录

### 作业3：多渠道工作流（选做）

**任务：**
设计一个多渠道工作流，例如：

**示例1：跨渠道提醒系统**
- 在飞书设置任务
- Telegram接收提醒
- 完成后同步状态

**示例2：文档协作**
- 飞书创建文档
- Telegram查看摘要
- Discord讨论内容

**提交：**
- 工作流设计文档
- 配置文件
- 运行截图

---

## 第七部分：常见问题（10分钟）

### Q1：飞书Bot无法接收消息？

**A1：**
```bash
# 检查权限
1. 确认已添加 im:message 权限
2. 确认权限已审批通过
3. 确认事件订阅已配置

# 检查连接
openclaw gateway logs | grep feishu

# 应该看到：
# [feishu] WebSocket client started
# [feishu] bot open_id resolved
```

### Q2：Telegram Bot响应慢？

**A2：**
```json
// 切换到webhook模式（需要公网IP）
{
  "channels": {
    "telegram": {
      "mode": "webhook",
      "webhookUrl": "https://your-domain.com/telegram"
    }
  }
}

// 或优化polling间隔
{
  "channels": {
    "telegram": {
      "mode": "polling",
      "pollingInterval": 1000
    }
  }
}
```

### Q3：如何在群聊中只响应@消息？

**A3：**
```json
// 飞书
{
  "channels": {
    "feishu": {
      "respondToAll": false  // 仅响应@消息
    }
  }
}

// Telegram
{
  "channels": {
    "telegram": {
      "respondToAll": false,
      "requireMention": true
    }
  }
}
```

### Q4：如何限制某些用户访问？

**A4：**
```json
{
  "channels": {
    "feishu": {
      "allowlist": [
        "ou_user1",
        "ou_user2"
      ]
    }
  }
}
```

### Q5：消息发送失败怎么办？

**A5：**
```bash
# 查看详细日志
openclaw gateway logs --level debug

# 检查API配额
# 飞书：https://open.feishu.cn/app
# Telegram：通常无限制

# 检查网络连接
curl https://open.feishu.cn
curl https://api.telegram.org
```

---

## 第八部分：扩展阅读

### 推荐资源

#### 官方文档
- 飞书开放平台：https://open.feishu.cn/document
- Telegram Bot API：https://core.telegram.org/bots/api
- Discord Developer：https://discord.com/developers/docs
- Slack API：https://api.slack.com

#### OpenClaw文档
- 渠道配置：https://docs.openclaw.ai/channels
- 消息工具：https://docs.openclaw.ai/tools/message
- 会话管理：https://docs.openclaw.ai/concepts/sessions

### 下节课预告

**第5课：模型选择策略 - 性价比最大化**
- 模型对比（Claude/GPT/Gemini/DeepSeek）
- 国内模型生态
- 成本优化策略
- 模型路由配置

---

## 课程总结

### 本节课你学到了：
✅ 飞书集成的完整配置流程  
✅ Telegram Bot的创建和配置  
✅ 其他渠道（WhatsApp/Discord/Slack）的接入方法  
✅ 多渠道消息同步策略  
✅ 跨渠道工作流设计  

### 关键要点：
1. **飞书适合企业** - 文档集成、权限管理完善
2. **Telegram适合个人** - 轻量、快速、跨平台
3. **多渠道互补** - 工作用飞书，个人用Telegram
4. **统一管理** - OpenClaw统一处理所有渠道

### 下一步：
1. 完成作业1和作业2（必做）
2. 尝试作业3（选做）
3. 探索更多渠道
4. 准备学习第5课（模型选择策略）

---

**课程反馈：**
如有问题或建议，请在GitHub提Issue或加入社区讨论。

**下节课见！** 🚀
