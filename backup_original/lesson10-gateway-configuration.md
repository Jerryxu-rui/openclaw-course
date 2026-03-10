# 第10课：Gateway深度配置 - 稳定性与安全

## 课程目标
- 理解Gateway架构
- 掌握性能优化技巧
- 实现稳定性保障
- 加固系统安全

---

## 第一部分：Gateway架构（30分钟）

### 1.1 Gateway是什么？

#### 核心职责
```
Gateway是OpenClaw的核心服务，负责：
1. 消息路由 - 接收和分发消息
2. 会话管理 - 管理对话上下文
3. 模型调用 - 与AI模型通信
4. 渠道连接 - 连接飞书/Telegram等
5. 工具执行 - 执行文件操作等
```

#### 架构图
```
外部世界
  ↓
[飞书/Telegram/Web]
  ↓
Gateway（网关）
  ↓
├─ 消息路由
├─ 会话管理
├─ 模型调用
├─ 工具执行
└─ 插件系统
  ↓
[AI模型/文件系统/数据库]
```

### 1.2 Gateway工作流程

#### 消息处理流程
```
1. 接收消息
   ↓
2. 识别会话
   ↓
3. 加载上下文
   ↓
4. 调用模型
   ↓
5. 执行工具
   ↓
6. 返回结果
   ↓
7. 更新会话
```

#### 会话生命周期
```
创建 → 活跃 → 空闲 → 压缩 → 归档
```

### 1.3 配置文件结构

#### openclaw.json
```json
{
  "meta": {
    "lastTouchedVersion": "2026.2.26",
    "lastTouchedAt": "2026-03-09T10:00:00.000Z"
  },
  "gateway": {
    "port": 18789,
    "mode": "local",
    "bind": "auto",
    "auth": {
      "mode": "token",
      "token": "your-secure-token"
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "mixai/claude-sonnet-4-6"
      },
      "workspace": "/home/user/.openclaw/workspace",
      "maxConcurrent": 4
    }
  },
  "channels": {
    "feishu": {
      "appId": "cli_xxx",
      "appSecret": "xxx"
    }
  }
}
```

---

## 第二部分：性能优化（40分钟）

### 2.1 上下文管理

#### 问题：上下文过长
```
症状：
- 响应变慢
- Token消耗大
- 成本增加

原因：
- 对话历史累积
- 未及时压缩
- 无效信息保留
```

#### 解决方案1：自动压缩
```json
{
  "agents": {
    "defaults": {
      "compaction": {
        "mode": "safeguard",
        "reserveTokensFloor": 20000
      }
    }
  }
}

效果：
- 自动压缩长对话
- 保留关键信息
- 降低Token消耗
```

#### 解决方案2：缓存策略
```json
{
  "agents": {
    "defaults": {
      "contextPruning": {
        "mode": "cache-ttl",
        "ttl": "1h"
      }
    }
  }
}

效果：
- 缓存常用上下文
- 减少重复加载
- 提升响应速度
```

### 2.2 并发控制

#### 问题：并发过高
```
症状：
- 系统卡顿
- 内存占用高
- API限流

原因：
- 同时处理太多请求
- 资源竞争
- 无限制并发
```

#### 解决方案：限制并发
```json
{
  "agents": {
    "defaults": {
      "maxConcurrent": 4,
      "subagents": {
        "maxConcurrent": 8
      }
    }
  }
}

说明：
- maxConcurrent: 主Agent并发数
- subagents.maxConcurrent: 子Agent并发数
- 根据机器性能调整
```

### 2.3 模型调用优化

#### 问题：模型调用慢
```
症状：
- 等待时间长
- 用户体验差

原因：
- 网络延迟
- 模型响应慢
- 无超时控制
```

#### 解决方案1：超时设置
```json
{
  "models": {
    "providers": {
      "mixai": {
        "timeout": 30000
      }
    }
  }
}

说明：
- timeout: 超时时间（毫秒）
- 超时后自动重试或降级
```

#### 解决方案2：模型降级
```json
{
  "models": {
    "default": "mixai/claude-sonnet-4-6",
    "fallback": "google/gemini-3-flash-preview"
  }
}

策略：
1. 首选Claude（质量高）
2. 超时/失败 → 降级到Gemini（速度快）
3. 仍失败 → 返回错误
```

### 2.4 内存优化

#### 问题：内存占用高
```
症状：
- 系统变慢
- OOM错误
- 频繁GC

原因：
- 会话数据累积
- 缓存过大
- 内存泄漏
```

#### 解决方案1：会话清理
```json
{
  "session": {
    "maxAge": "7d",
    "cleanupInterval": "1h"
  }
}

效果：
- 自动清理旧会话
- 释放内存
- 保持系统健康
```

#### 解决方案2：限制缓存
```json
{
  "cache": {
    "maxSize": "500MB",
    "evictionPolicy": "LRU"
  }
}

策略：
- 限制缓存大小
- LRU淘汰策略
- 定期清理
```

---

## 第三部分：稳定性保障（40分钟）

### 3.1 systemd守护进程

#### 为什么需要守护？
```
问题：
- Gateway崩溃
- 进程意外退出
- 需要手动重启

解决：
- systemd自动守护
- 崩溃自动重启
- 开机自动启动
```

#### 配置systemd服务
```bash
# 创建服务文件
sudo nano /etc/systemd/system/openclaw-gateway.service
```

```ini
[Unit]
Description=OpenClaw Gateway
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/home/youruser/.openclaw
ExecStart=/usr/bin/node /path/to/openclaw-gateway
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

#### 启用服务
```bash
# 重载systemd
sudo systemctl daemon-reload

# 启用服务
sudo systemctl enable openclaw-gateway

# 启动服务
sudo systemctl start openclaw-gateway

# 查看状态
sudo systemctl status openclaw-gateway

# 查看日志
sudo journalctl -u openclaw-gateway -f
```

### 3.2 自动修复脚本

#### 创建修复脚本
```bash
nano ~/.local/bin/openclaw-fix.sh
```

```bash
#!/bin/bash

# OpenClaw自动修复脚本

LOG_FILE="$HOME/.openclaw/fix.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 检查Gateway状态
check_gateway() {
    if pgrep -f "openclaw-gateway" > /dev/null; then
        return 0
    else
        return 1
    fi
}

# 修复Gateway
fix_gateway() {
    log "Gateway未运行，尝试修复..."
    
    # 杀掉僵尸进程
    pkill -9 -f "openclaw-gateway"
    sleep 2
    
    # 重启Gateway
    openclaw gateway restart
    sleep 5
    
    # 验证
    if check_gateway; then
        log "✅ Gateway修复成功"
        return 0
    else
        log "❌ Gateway修复失败"
        return 1
    fi
}

# 主逻辑
if ! check_gateway; then
    fix_gateway
    
    # 如果修复失败，通知用户
    if [ $? -ne 0 ]; then
        # 发送Telegram通知
        openclaw message send --channel telegram \
            --message "⚠️ OpenClaw Gateway修复失败，请检查"
    fi
fi
```

#### 设置定时检查
```bash
# 编辑crontab
crontab -e

# 添加定时任务（每5分钟检查一次）
*/5 * * * * ~/.local/bin/openclaw-fix.sh
```

### 3.3 健康检查

#### 配置健康检查
```json
{
  "gateway": {
    "healthCheck": {
      "enabled": true,
      "interval": "5m",
      "timeout": "10s",
      "checks": [
        "gateway",
        "models",
        "channels",
        "storage"
      ]
    }
  }
}
```

#### 健康检查脚本
```bash
#!/bin/bash

# 健康检查脚本

check_health() {
    # 检查Gateway端口
    if ! nc -z localhost 18789; then
        echo "❌ Gateway端口不可达"
        return 1
    fi
    
    # 检查模型连接
    if ! openclaw chat --model fast "test" > /dev/null 2>&1; then
        echo "❌ 模型连接失败"
        return 1
    fi
    
    # 检查磁盘空间
    DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
    if [ "$DISK_USAGE" -gt 90 ]; then
        echo "⚠️ 磁盘使用率过高：${DISK_USAGE}%"
        return 1
    fi
    
    echo "✅ 系统健康"
    return 0
}

check_health
```

### 3.4 日志管理

#### 配置日志
```json
{
  "logging": {
    "level": "info",
    "file": "~/.openclaw/logs/gateway.log",
    "maxSize": "100MB",
    "maxFiles": 10,
    "compress": true
  }
}
```

#### 日志轮转
```bash
# 使用logrotate
sudo nano /etc/logrotate.d/openclaw
```

```
/home/youruser/.openclaw/logs/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 0640 youruser youruser
}
```

---

## 第四部分：安全加固（30分钟）

### 4.1 认证配置

#### Token认证
```json
{
  "gateway": {
    "auth": {
      "mode": "token",
      "token": "your-secure-token-here"
    }
  }
}

生成安全Token：
openssl rand -hex 32
```

#### IP白名单
```json
{
  "gateway": {
    "auth": {
      "mode": "token",
      "allowedIPs": [
        "127.0.0.1",
        "192.168.1.0/24"
      ]
    }
  }
}
```

### 4.2 数据加密

#### 敏感数据加密
```bash
# 加密API密钥
openclaw config encrypt models.providers.mixai.apiKey

# 加密后的配置
{
  "models": {
    "providers": {
      "mixai": {
        "apiKey": "encrypted:xxx"
      }
    }
  }
}
```

#### 环境变量
```bash
# 使用环境变量存储敏感信息
nano ~/.config/openclaw/gateway.env
```

```bash
# Gateway Token
OPENCLAW_GATEWAY_TOKEN=your-secure-token

# API密钥
MIXAI_API_KEY=sk-xxx
DEEPSEEK_API_KEY=sk-xxx
GEMINI_API_KEY=AIzaSy-xxx

# 飞书凭证
FEISHU_APP_ID=cli_xxx
FEISHU_APP_SECRET=xxx
```

```bash
# 设置权限
chmod 600 ~/.config/openclaw/gateway.env
```

### 4.3 访问控制

#### 限制访问
```json
{
  "gateway": {
    "bind": "127.0.0.1",
    "port": 18789
  }
}

说明：
- bind: "127.0.0.1" - 仅本地访问
- bind: "0.0.0.0" - 允许外部访问（需配合防火墙）
```

#### 防火墙配置
```bash
# 仅允许本地访问
sudo ufw allow from 127.0.0.1 to any port 18789

# 允许特定IP访问
sudo ufw allow from 192.168.1.100 to any port 18789

# 启用防火墙
sudo ufw enable
```

### 4.4 审计日志

#### 配置审计
```json
{
  "audit": {
    "enabled": true,
    "logFile": "~/.openclaw/logs/audit.log",
    "events": [
      "auth",
      "config_change",
      "model_call",
      "tool_exec"
    ]
  }
}
```

#### 审计日志示例
```
[2026-03-09 10:00:00] AUTH user=admin action=login ip=127.0.0.1 result=success
[2026-03-09 10:05:00] CONFIG user=admin action=update key=models.default
[2026-03-09 10:10:00] MODEL user=admin model=claude-sonnet-4-6 tokens=1234
[2026-03-09 10:15:00] TOOL user=admin tool=exec command="ls -la"
```

---

## 第五部分：监控与告警（30分钟）

### 5.1 性能监控

#### 配置监控
```json
{
  "monitoring": {
    "enabled": true,
    "metrics": {
      "cpu": true,
      "memory": true,
      "disk": true,
      "network": true
    },
    "interval": "1m"
  }
}
```

#### 监控脚本
```bash
#!/bin/bash

# 性能监控脚本

# CPU使用率
CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)

# 内存使用率
MEM_USAGE=$(free | grep Mem | awk '{print ($3/$2) * 100.0}')

# 磁盘使用率
DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')

# Gateway进程数
GATEWAY_PROCS=$(pgrep -f "openclaw-gateway" | wc -l)

echo "CPU: ${CPU_USAGE}%"
echo "Memory: ${MEM_USAGE}%"
echo "Disk: ${DISK_USAGE}%"
echo "Gateway Processes: ${GATEWAY_PROCS}"

# 告警阈值
if (( $(echo "$CPU_USAGE > 80" | bc -l) )); then
    echo "⚠️ CPU使用率过高"
fi

if (( $(echo "$MEM_USAGE > 90" | bc -l) )); then
    echo "⚠️ 内存使用率过高"
fi

if [ "$DISK_USAGE" -gt 90 ]; then
    echo "⚠️ 磁盘使用率过高"
fi
```

### 5.2 告警配置

#### Telegram告警
```json
{
  "alerts": {
    "enabled": true,
    "channels": ["telegram"],
    "rules": [
      {
        "name": "high_cpu",
        "condition": "cpu > 80",
        "message": "⚠️ CPU使用率过高：{{value}}%"
      },
      {
        "name": "high_memory",
        "condition": "memory > 90",
        "message": "⚠️ 内存使用率过高：{{value}}%"
      },
      {
        "name": "gateway_down",
        "condition": "gateway_status == down",
        "message": "🚨 Gateway已停止运行"
      }
    ]
  }
}
```

#### 告警脚本
```bash
#!/bin/bash

# 告警脚本

send_alert() {
    local message="$1"
    openclaw message send \
        --channel telegram \
        --message "$message"
}

# 检查并告警
if ! pgrep -f "openclaw-gateway" > /dev/null; then
    send_alert "🚨 OpenClaw Gateway已停止运行"
fi
```

---

## 第六部分：实战配置（30分钟）

### 6.1 生产级配置

#### 完整配置示例
```json
{
  "gateway": {
    "port": 18789,
    "mode": "local",
    "bind": "127.0.0.1",
    "auth": {
      "mode": "token",
      "token": "${OPENCLAW_GATEWAY_TOKEN}"
    },
    "healthCheck": {
      "enabled": true,
      "interval": "5m"
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "mixai/claude-sonnet-4-6",
        "fallback": "google/gemini-3-flash-preview"
      },
      "workspace": "/home/user/.openclaw/workspace",
      "maxConcurrent": 4,
      "compaction": {
        "mode": "safeguard",
        "reserveTokensFloor": 20000
      },
      "contextPruning": {
        "mode": "cache-ttl",
        "ttl": "1h"
      }
    }
  },
  "logging": {
    "level": "info",
    "file": "~/.openclaw/logs/gateway.log",
    "maxSize": "100MB",
    "maxFiles": 10
  },
  "monitoring": {
    "enabled": true,
    "interval": "1m"
  },
  "alerts": {
    "enabled": true,
    "channels": ["telegram"]
  }
}
```

### 6.2 部署检查清单

```markdown
## 部署前检查

### 基础配置
- [ ] Node.js版本 >= 22
- [ ] OpenClaw已安装
- [ ] 配置文件已创建
- [ ] API密钥已配置

### 安全配置
- [ ] Gateway Token已设置
- [ ] 环境变量权限正确（600）
- [ ] 防火墙已配置
- [ ] IP白名单已设置

### 稳定性配置
- [ ] systemd服务已配置
- [ ] 自动修复脚本已部署
- [ ] 健康检查已启用
- [ ] 日志轮转已配置

### 性能配置
- [ ] 并发限制已设置
- [ ] 上下文压缩已启用
- [ ] 缓存策略已配置
- [ ] 超时时间已设置

### 监控配置
- [ ] 性能监控已启用
- [ ] 告警规则已配置
- [ ] Telegram通知已测试
- [ ] 审计日志已启用

### 测试验证
- [ ] Gateway启动正常
- [ ] 模型调用成功
- [ ] 渠道连接正常
- [ ] 工具执行正常
```

---

## 第七部分：作业与练习（课后）

### 作业1：配置systemd守护（必做）

**任务：**
配置systemd服务，实现Gateway自动守护

**要求：**
1. 创建服务文件
2. 启用自动启动
3. 测试崩溃恢复
4. 查看服务日志

**提交：**
- 服务配置文件
- 启动状态截图
- 日志输出

### 作业2：性能优化（必做）

**任务：**
优化Gateway性能配置

**要求：**
1. 配置上下文压缩
2. 设置并发限制
3. 启用缓存策略
4. 测试性能提升

**提交：**
- 优化前后配置对比
- 性能测试数据
- 优化效果分析

### 作业3：安全加固（选做）

**任务：**
加固Gateway安全配置

**要求：**
1. 配置Token认证
2. 设置IP白名单
3. 加密敏感数据
4. 配置防火墙

**提交：**
- 安全配置文件
- 测试结果
- 安全检查报告

---

## 第八部分：常见问题（10分钟）

### Q1：Gateway频繁崩溃？

**A1：**
```
排查步骤：
1. 查看日志
   journalctl -u openclaw-gateway -n 100

2. 检查内存
   free -h

3. 检查磁盘
   df -h

4. 检查进程
   ps aux | grep openclaw

常见原因：
- 内存不足
- 磁盘满
- 配置错误
- 模型调用失败
```

### Q2：如何升级Gateway？

**A2：**
```bash
# 备份配置
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak

# 升级OpenClaw
npm update -g openclaw

# 重启Gateway
openclaw gateway restart

# 验证版本
openclaw --version
```

### Q3：如何迁移到新服务器？

**A3：**
```bash
# 旧服务器
tar -czf openclaw-backup.tar.gz ~/.openclaw

# 传输到新服务器
scp openclaw-backup.tar.gz user@newserver:~

# 新服务器
tar -xzf openclaw-backup.tar.gz
npm install -g openclaw
openclaw gateway start
```

### Q4：如何监控多个Gateway？

**A4：**
```
方案1：集中式监控
- 使用Prometheus + Grafana
- 收集各Gateway指标
- 统一展示和告警

方案2：分布式监控
- 每个Gateway独立监控
- 告警汇总到中心
- 使用统一的告警渠道
```

### Q5：如何处理高并发？

**A5：**
```
策略：
1. 增加并发限制
2. 使用负载均衡
3. 部署多个Gateway
4. 使用消息队列

示例：
# 负载均衡配置
nginx upstream {
    server gateway1:18789;
    server gateway2:18789;
    server gateway3:18789;
}
```

---

## 第九部分：扩展阅读

### 推荐资源

#### 官方文档
- Gateway配置：https://docs.openclaw.ai/gateway/configuration
- 性能优化：https://docs.openclaw.ai/gateway/performance
- 安全指南：https://docs.openclaw.ai/gateway/security

#### 工具
- systemd：https://systemd.io
- logrotate：https://linux.die.net/man/8/logrotate
- Prometheus：https://prometheus.io

### 下节课预告

**第11课：Sub-Agent与多Agent协作**
- Sub-Agent系统
- 多Agent协作
- 任务编排
- ACP集成

---

## 课程总结

### 本节课你学到了：
✅ Gateway架构和工作原理  
✅ 性能优化技巧  
✅ 稳定性保障方案  
✅ 安全加固措施  
✅ 监控和告警配置  

### 关键要点：
1. **systemd守护是稳定性基础**
2. **上下文压缩降低成本**
3. **并发控制保证性能**
4. **Token认证保障安全**
5. **监控告警及时发现问题**

### 下一步：
1. 完成作业1和作业2（必做）
2. 尝试作业3（选做）
3. 部署生产级配置
4. 准备学习第11课（多Agent协作）

---

**课程反馈：**
如有问题或建议，请在GitHub提Issue或加入社区讨论。

**下节课见！** 🚀
