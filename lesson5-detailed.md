# 第5课：模型选择策略 - 性价比最大化

## 课程目标
- 理解不同AI模型的特点和差异
- 掌握国内模型生态
- 学会根据任务选择合适的模型
- 实现成本优化策略

---

## 第一部分：主流模型对比（30分钟）

### 1.1 模型分类

#### 顶级模型（Tier 1）
**Claude Sonnet 4**
- 提供商：Anthropic
- 上下文：200K tokens
- 特点：推理能力最强，代码生成优秀
- 成本：高（$3/1M input, $15/1M output）
- 适用：复杂任务、代码审查、创意写作

**GPT-4 Turbo**
- 提供商：OpenAI
- 上下文：128K tokens
- 特点：通用能力强，知识面广
- 成本：高（$10/1M input, $30/1M output）
- 适用：复杂分析、多步推理

**Gemini 1.5 Pro**
- 提供商：Google
- 上下文：2M tokens（最长）
- 特点：超长上下文，多模态
- 成本：中（$1.25/1M input, $5/1M output）
- 适用：长文档分析、视频理解

#### 中端模型（Tier 2）
**Claude Haiku**
- 提供商：Anthropic
- 上下文：200K tokens
- 特点：快速、便宜、质量不错
- 成本：低（$0.25/1M input, $1.25/1M output）
- 适用：日常对话、简单任务

**Gemini Flash**
- 提供商：Google
- 上下文：1M tokens
- 特点：极快、极便宜
- 成本：极低（$0.075/1M input, $0.3/1M output）
- 适用：快速查询、批量处理

**DeepSeek Chat**
- 提供商：DeepSeek（国内）
- 上下文：64K tokens
- 特点：性价比之王
- 成本：极低（$0.14/1M input, $0.28/1M output）
- 适用：代码生成、日常对话

#### 专用模型（Specialized）
**DeepSeek Coder**
- 专注：代码生成和理解
- 特点：代码能力接近GPT-4
- 成本：极低
- 适用：编程任务

**Minimax M2.5**
- 提供商：Minimax（国内）
- 特点：推理能力强
- 成本：中等
- 适用：复杂推理、数学问题

### 1.2 详细对比表

| 模型 | 上下文 | 输入成本 | 输出成本 | 速度 | 质量 | 推荐场景 |
|------|--------|---------|---------|------|------|---------|
| Claude Sonnet 4 | 200K | $3 | $15 | 中 | ⭐⭐⭐⭐⭐ | 复杂任务、代码审查 |
| GPT-4 Turbo | 128K | $10 | $30 | 慢 | ⭐⭐⭐⭐⭐ | 深度分析、创意 |
| Gemini Pro | 2M | $1.25 | $5 | 中 | ⭐⭐⭐⭐ | 长文档、多模态 |
| Claude Haiku | 200K | $0.25 | $1.25 | 快 | ⭐⭐⭐⭐ | 日常对话 |
| Gemini Flash | 1M | $0.075 | $0.3 | 极快 | ⭐⭐⭐ | 快速查询 |
| DeepSeek Chat | 64K | $0.14 | $0.28 | 快 | ⭐⭐⭐⭐ | 代码、对话 |
| Minimax M2.5 | 200K | $0.3 | $1.2 | 中 | ⭐⭐⭐⭐ | 推理任务 |

**成本单位：** 美元/百万tokens

### 1.3 实际测试对比

#### 测试任务1：写一首诗
```
提示词：请用中文写一首关于春天的诗

Claude Sonnet 4：
春风拂面暖如酥，
万物复苏展新图。
桃李争妍竞芳菲，
莺歌燕舞乐无虞。
（质量：⭐⭐⭐⭐⭐ 耗时：3.2秒 成本：$0.0015）

DeepSeek Chat：
春风送暖入屠苏，
万物复苏展新图。
桃红柳绿满园春，
莺歌燕舞乐悠悠。
（质量：⭐⭐⭐⭐ 耗时：1.8秒 成本：$0.0002）

Gemini Flash：
春风吹拂大地，
万物开始复苏。
花儿绽放笑脸，
鸟儿欢快歌唱。
（质量：⭐⭐⭐ 耗时：0.9秒 成本：$0.00008）
```

**结论：** 创意任务选Claude，日常任务选DeepSeek，快速查询选Gemini Flash

#### 测试任务2：代码生成
```
提示词：写一个Python快速排序算法

Claude Sonnet 4：
✅ 代码正确
✅ 注释详细
✅ 包含测试用例
✅ 时间复杂度分析
（质量：⭐⭐⭐⭐⭐ 成本：$0.002）

DeepSeek Chat：
✅ 代码正确
✅ 注释清晰
✅ 简洁高效
（质量：⭐⭐⭐⭐⭐ 成本：$0.0003）

Gemini Flash：
✅ 代码正确
⚠️ 注释较少
（质量：⭐⭐⭐⭐ 成本：$0.0001）
```

**结论：** 代码任务DeepSeek性价比最高

---

## 第二部分：国内模型生态（30分钟）

### 2.1 MixAI（Claude代理）

#### 什么是MixAI？
- 国内Claude API代理
- 支持Claude全系列模型
- 无需科学上网
- 价格比官方便宜

#### 价格对比
```
官方Claude Sonnet 4：
- 输入：$3/1M tokens
- 输出：$15/1M tokens

MixAI Claude Sonnet 4：
- 输入：¥15/1M tokens（约$2.1）
- 输出：¥75/1M tokens（约$10.5）
- 节省：30%
```

#### 配置方法
```json
{
  "models": {
    "providers": {
      "mixai": {
        "apiKey": "sk-xxx",
        "baseURL": "https://mixai.cc/v1"
      }
    },
    "aliases": {
      "claude-sonnet-4-6": "mixai/claude-sonnet-4-6"
    }
  }
}
```

#### 优势
- ✅ 国内访问快
- ✅ 支持支付宝/微信支付
- ✅ 价格便宜
- ✅ API兼容OpenAI格式

### 2.2 DeepSeek（性价比之王）

#### 特点
- 国产大模型
- 代码能力强
- 价格极低
- 支持中文

#### 模型系列
```
DeepSeek Chat：
- 通用对话模型
- 64K上下文
- $0.14/$0.28 per 1M tokens

DeepSeek Coder：
- 专注代码
- 支持多种编程语言
- 代码补全、生成、解释

DeepSeek Math：
- 数学推理
- 解题能力强
```

#### 配置方法
```json
{
  "models": {
    "providers": {
      "deepseek": {
        "apiKey": "sk-xxx",
        "baseURL": "https://api.deepseek.com"
      }
    }
  }
}
```

#### 实际案例
```
任务：生成一个React组件

DeepSeek Coder：
- 代码质量：⭐⭐⭐⭐⭐
- 响应时间：2.1秒
- 成本：$0.0003
- 结论：完美替代GPT-4 Turbo

成本对比：
- GPT-4 Turbo：$0.015
- DeepSeek Coder：$0.0003
- 节省：98%
```

### 2.3 Minimax（推理专家）

#### 特点
- 国产大模型
- 推理能力强
- 支持长上下文（200K）
- 价格适中

#### 配置方法
```json
{
  "models": {
    "providers": {
      "minimax": {
        "apiKey": "xxx",
        "baseURL": "https://api.minimax.chat/v1"
      }
    }
  }
}
```

#### 适用场景
- 复杂推理任务
- 数学问题
- 逻辑分析
- 战略规划

### 2.4 其他国内模型

#### 通义千问（阿里）
- 通用能力强
- 多模态支持
- 企业级服务

#### 文心一言（百度）
- 中文理解好
- 知识图谱丰富
- 搜索增强

#### 智谱AI（GLM）
- 学术背景强
- 推理能力好
- 开源友好

---

## 第三部分：模型选择策略（40分钟）

### 3.1 按任务类型选择

#### 复杂任务 → Claude Sonnet 4
```
适用场景：
- 代码审查
- 架构设计
- 战略分析
- 创意写作
- 复杂推理

示例：
You: 帮我审查这段代码，找出潜在问题

Agent: [使用Claude Sonnet 4]
发现以下问题：
1. 内存泄漏风险（第23行）
2. 并发安全问题（第45行）
3. 性能优化建议（第67行）
...
```

#### 日常任务 → DeepSeek Chat
```
适用场景：
- 日常对话
- 简单查询
- 文本总结
- 翻译
- 格式转换

示例：
You: 总结一下这篇文章

Agent: [使用DeepSeek Chat]
文章主要讲述了...
核心观点包括：
1. ...
2. ...
```

#### 快速查询 → Gemini Flash
```
适用场景：
- 快速问答
- 信息查询
- 简单计算
- 格式检查

示例：
You: 北京今天天气怎么样？

Agent: [使用Gemini Flash]
北京今天多云，15-25°C
```

#### 代码任务 → DeepSeek Coder
```
适用场景：
- 代码生成
- Bug修复
- 代码解释
- 重构建议

示例：
You: 写一个二叉树遍历算法

Agent: [使用DeepSeek Coder]
```python
def inorder_traversal(root):
    """中序遍历二叉树"""
    if not root:
        return []
    return (inorder_traversal(root.left) + 
            [root.val] + 
            inorder_traversal(root.right))
```
```

### 3.2 按成本预算选择

#### 预算充足（>$100/月）
```
主力模型：Claude Sonnet 4
备用模型：GPT-4 Turbo
快速查询：Gemini Flash

配置：
{
  "models": {
    "default": "mixai/claude-sonnet-4-6"
  }
}
```

#### 预算中等（$20-100/月）
```
主力模型：DeepSeek Chat
复杂任务：Claude Sonnet 4（限量使用）
快速查询：Gemini Flash

配置：
{
  "models": {
    "default": "deepseek/deepseek-chat",
    "fallback": "google/gemini-3-flash-preview"
  }
}
```

#### 预算紧张（<$20/月）
```
主力模型：DeepSeek Chat
快速查询：Gemini Flash
代码任务：DeepSeek Coder

配置：
{
  "models": {
    "default": "deepseek/deepseek-chat"
  }
}

预计成本：
- 每天100次对话
- 平均每次1K tokens
- 月成本：~$4
```

### 3.3 智能路由配置

#### 方案1：按任务类型路由
```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "deepseek/deepseek-chat",
        "routing": {
          "rules": [
            {
              "pattern": "代码|code|编程|bug",
              "model": "deepseek/deepseek-coder"
            },
            {
              "pattern": "复杂|分析|审查|设计",
              "model": "mixai/claude-sonnet-4-6"
            },
            {
              "pattern": "快速|简单|查询",
              "model": "google/gemini-3-flash-preview"
            }
          ]
        }
      }
    }
  }
}
```

#### 方案2：按Token长度路由
```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "deepseek/deepseek-chat",
        "routing": {
          "byTokens": {
            "0-1000": "google/gemini-3-flash-preview",
            "1000-10000": "deepseek/deepseek-chat",
            "10000+": "mixai/claude-sonnet-4-6"
          }
        }
      }
    }
  }
}
```

#### 方案3：按时间路由
```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "deepseek/deepseek-chat",
        "routing": {
          "byTime": {
            "workHours": "mixai/claude-sonnet-4-6",
            "offHours": "deepseek/deepseek-chat"
          }
        }
      }
    }
  }
}
```

### 3.4 成本优化技巧

#### 技巧1：使用缓存
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
- 重复查询直接返回缓存
- 节省API调用
- 响应更快
```

#### 技巧2：压缩上下文
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

#### 技巧3：记忆蒸馏
```
定期蒸馏记忆：
- 每10-15条消息
- 或上下文>15K时
- 压缩40-50%

成本对比：
优化前：17K tokens → $0.255/请求
优化后：9.3K tokens → $0.0007/请求
节省：99.7%
```

#### 技巧4：模型降级
```
策略：
1. 首次尝试用便宜模型
2. 如果质量不够，升级到贵模型
3. 记录成功率，优化策略

示例：
You: 写一个排序算法

Agent: [尝试Gemini Flash]
[检查代码质量]
[如果不够好，切换到DeepSeek Coder]
```

---

## 第四部分：实战配置（30分钟）

### 4.1 个人用户配置

#### 场景：日常使用 + 偶尔复杂任务
```json
{
  "models": {
    "default": "deepseek/deepseek-chat",
    "providers": {
      "deepseek": {
        "apiKey": "sk-xxx",
        "baseURL": "https://api.deepseek.com"
      },
      "google": {
        "apiKey": "AIzaSy-xxx"
      },
      "mixai": {
        "apiKey": "sk-xxx",
        "baseURL": "https://mixai.cc/v1"
      }
    },
    "aliases": {
      "fast": "google/gemini-3-flash-preview",
      "smart": "mixai/claude-sonnet-4-6",
      "code": "deepseek/deepseek-coder"
    }
  }
}

使用方式：
- 默认：DeepSeek Chat（日常对话）
- 快速：openclaw chat --model fast "天气"
- 复杂：openclaw chat --model smart "审查代码"
- 代码：openclaw chat --model code "写算法"

预计成本：$5-10/月
```

### 4.2 开发者配置

#### 场景：大量代码生成 + 文档处理
```json
{
  "models": {
    "default": "deepseek/deepseek-coder",
    "providers": {
      "deepseek": {
        "apiKey": "sk-xxx"
      },
      "mixai": {
        "apiKey": "sk-xxx"
      }
    },
    "routing": {
      "rules": [
        {
          "pattern": "代码|code|bug|算法",
          "model": "deepseek/deepseek-coder"
        },
        {
          "pattern": "文档|总结|翻译",
          "model": "deepseek/deepseek-chat"
        },
        {
          "pattern": "架构|设计|审查",
          "model": "mixai/claude-sonnet-4-6"
        }
      ]
    }
  }
}

预计成本：$10-20/月
```

### 4.3 企业用户配置

#### 场景：团队协作 + 高质量要求
```json
{
  "models": {
    "default": "mixai/claude-sonnet-4-6",
    "providers": {
      "mixai": {
        "apiKey": "sk-xxx"
      },
      "deepseek": {
        "apiKey": "sk-xxx"
      }
    },
    "routing": {
      "byUser": {
        "admin": "mixai/claude-sonnet-4-6",
        "developer": "deepseek/deepseek-coder",
        "support": "deepseek/deepseek-chat"
      }
    }
  }
}

预计成本：$50-200/月（按团队规模）
```

---

## 第五部分：作业与练习（课后）

### 作业1：模型对比测试（必做）

**任务：**
用相同的3个任务测试不同模型：

**任务列表：**
1. 写一首诗
2. 生成Python代码
3. 总结一篇文章

**测试模型：**
- Claude Sonnet 4（或MixAI代理）
- DeepSeek Chat
- Gemini Flash

**记录指标：**
- 响应时间
- 质量评分（1-5星）
- Token消耗
- 成本估算

**提交格式：**
```markdown
## 模型对比报告

### 任务1：写诗
| 模型 | 时间 | 质量 | Tokens | 成本 |
|------|------|------|--------|------|
| Claude | 3.2s | ⭐⭐⭐⭐⭐ | 150 | $0.0015 |
| DeepSeek | 1.8s | ⭐⭐⭐⭐ | 120 | $0.0002 |
| Gemini | 0.9s | ⭐⭐⭐ | 100 | $0.00008 |

### 结论
...
```

### 作业2：配置智能路由（必做）

**任务：**
根据自己的使用场景，配置智能路由

**要求：**
1. 至少配置3个模型
2. 设置路由规则
3. 测试路由效果
4. 记录成本节省

**提交：**
- 配置文件（openclaw.json）
- 测试截图
- 成本分析报告

### 作业3：成本优化方案（选做）

**任务：**
设计一个月成本<$10的使用方案

**要求：**
1. 估算每日使用量
2. 选择合适的模型组合
3. 配置优化策略
4. 计算预期成本

**提交：**
- 使用场景描述
- 模型选择方案
- 配置文件
- 成本计算表

---

## 第六部分：常见问题（10分钟）

### Q1：如何选择主力模型？

**A1：**
```
考虑因素：
1. 预算：有限选DeepSeek，充足选Claude
2. 任务：代码选DeepSeek Coder，创意选Claude
3. 速度：要快选Gemini Flash
4. 质量：要好选Claude Sonnet 4

推荐组合：
- 预算<$20：DeepSeek + Gemini Flash
- 预算$20-100：DeepSeek + Claude（限量）
- 预算>$100：Claude + GPT-4
```

### Q2：MixAI靠谱吗？

**A2：**
```
优点：
✅ 国内访问快
✅ 价格便宜30%
✅ API兼容性好
✅ 支持国内支付

注意：
⚠️ 第三方代理，有风险
⚠️ 可能有限流
⚠️ 建议小额充值测试

替代方案：
- 官方Claude API（需科学上网）
- 其他国内代理
```

### Q3：DeepSeek和GPT-4差距大吗？

**A3：**
```
代码任务：
- DeepSeek Coder ≈ GPT-4 Turbo
- 成本：DeepSeek便宜98%

通用任务：
- DeepSeek Chat < GPT-4
- 但对于日常对话足够用

建议：
- 代码任务：优先DeepSeek
- 复杂推理：使用GPT-4/Claude
```

### Q4：如何监控成本？

**A4：**
```bash
# 查看使用统计
openclaw status

# 查看详细成本
openclaw usage --detailed

# 设置预算警告
openclaw config set budget.monthly 50
openclaw config set budget.alert 0.8
```

### Q5：模型切换会影响对话吗？

**A5：**
```
不会影响：
- 对话历史保留
- 记忆系统独立
- 上下文继续

注意：
- 不同模型风格可能不同
- 建议同一任务用同一模型
- 切换时可能需要重新解释上下文
```

---

## 第七部分：扩展阅读

### 推荐资源

#### 模型文档
- Claude：https://docs.anthropic.com
- OpenAI：https://platform.openai.com/docs
- Gemini：https://ai.google.dev/docs
- DeepSeek：https://platform.deepseek.com/docs

#### 价格对比
- OpenRouter：https://openrouter.ai/models
- Artificial Analysis：https://artificialanalysis.ai

#### 国内平台
- MixAI：https://mixai.cc
- DeepSeek：https://platform.deepseek.com
- Minimax：https://www.minimaxi.com

### 下节课预告

**第6课：记忆系统 - 让AI真正了解你**
（已完成，可直接学习）

---

## 课程总结

### 本节课你学到了：
✅ 主流AI模型的特点和差异  
✅ 国内模型生态（MixAI/DeepSeek/Minimax）  
✅ 按任务类型选择模型的策略  
✅ 智能路由和成本优化技巧  
✅ 实战配置方案  

### 关键要点：
1. **没有最好的模型，只有最合适的模型**
2. **DeepSeek是性价比之王**（代码任务）
3. **Gemini Flash是速度之王**（快速查询）
4. **Claude Sonnet 4是质量之王**（复杂任务）
5. **智能路由可以节省90%+成本**

### 成本优化总结：
```
优化前（全用Claude）：
- 每天100次对话
- 月成本：~$150

优化后（智能路由）：
- 80%用DeepSeek：$4
- 15%用Gemini Flash：$0.5
- 5%用Claude：$7.5
- 月成本：~$12
- 节省：92%
```

### 下一步：
1. 完成作业1和作业2（必做）
2. 尝试作业3（选做）
3. 配置自己的模型组合
4. 监控实际成本
5. 继续学习第6课（记忆系统）

---

**课程反馈：**
如有问题或建议，请在GitHub提Issue或加入社区讨论。

**恭喜完成第一阶段（基础入门）！** 🎉
