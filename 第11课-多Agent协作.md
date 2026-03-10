# 第11课：Sub-Agent与多Agent协作

## 课程目标
- 理解Sub-Agent系统
- 掌握多Agent协作
- 学会任务编排
- 集成ACP（Codex/Claude Code）

---

## 第一部分：Sub-Agent系统（30分钟）

### 1.1 什么是Sub-Agent？

Sub-Agent是独立的Agent实例，用于：
- 并行处理任务
- 隔离执行环境
- 专业化分工
- 后台长时间任务

### 1.2 创建Sub-Agent

```
You: 创建一个研究Agent，帮我调研Rust语言

Agent: [创建Sub-Agent]
✅ Sub-Agent已创建

Agent ID: research-001
任务：调研Rust语言
状态：运行中

完成后会通过Telegram通知你
```

### 1.3 管理Sub-Agent

```bash
# 列出所有Sub-Agent
openclaw subagents list

# 查看Sub-Agent状态
openclaw subagents status research-001

# 停止Sub-Agent
openclaw subagents kill research-001
```

---

## 第二部分：多Agent协作（40分钟）

### 2.1 协作模式

#### 模式1：流水线
```
Agent1（数据收集）
  ↓
Agent2（数据分析）
  ↓
Agent3（报告生成）
```

#### 模式2：并行
```
Agent1（任务A）
Agent2（任务B）  → 汇总
Agent3（任务C）
```

#### 模式3：主从
```
主Agent（协调）
  ├─ 从Agent1（执行）
  ├─ 从Agent2（执行）
  └─ 从Agent3（执行）
```

### 2.2 实战案例

#### 案例：竞品分析系统
```
主Agent：协调任务
├─ Agent1：收集产品信息
├─ Agent2：分析价格策略
├─ Agent3：监控用户反馈
└─ Agent4：生成分析报告
```

---

## 第三部分：ACP集成（30分钟）

### 3.1 什么是ACP？

ACP（Agent Coding Protocol）是代码生成协议，支持：
- Codex（OpenAI）
- Claude Code（Anthropic）
- 其他代码Agent

### 3.2 使用Codex

```
You: 使用Codex帮我开发一个React组件

Agent: [启动Codex]
✅ Codex任务已启动

任务：开发React组件
预计耗时：5-10分钟
完成后会通知你
```

### 3.3 使用Claude Code

```
You: 使用Claude Code审查这段代码

Agent: [启动Claude Code]
正在审查...

发现问题：
1. 内存泄漏风险（第23行）
2. 并发安全问题（第45行）
3. 性能优化建议（第67行）
```

---

## 第四部分：任务编排（30分钟）

### 4.1 编排策略

#### 串行执行
```yaml
tasks:
  - name: collect_data
    agent: data_collector
  - name: analyze_data
    agent: data_analyzer
    depends_on: collect_data
  - name: generate_report
    agent: report_generator
    depends_on: analyze_data
```

#### 并行执行
```yaml
tasks:
  - name: task_a
    agent: agent_a
  - name: task_b
    agent: agent_b
  - name: task_c
    agent: agent_c
  - name: merge
    agent: merger
    depends_on: [task_a, task_b, task_c]
```

---

## 第五部分：实战项目（30分钟）

### 项目：自动化代码审查系统

```
主Agent：接收PR
├─ Agent1：代码风格检查
├─ Agent2：安全漏洞扫描
├─ Agent3：性能分析
└─ Agent4：生成审查报告
```

---

## 作业与练习

### 作业1：创建Sub-Agent（必做）
创建一个Sub-Agent执行后台任务

### 作业2：多Agent协作（必做）
设计一个多Agent协作场景

### 作业3：ACP集成（选做）
使用Codex或Claude Code完成代码任务

---

## 课程总结

### 本节课你学到了：
✅ Sub-Agent系统的使用  
✅ 多Agent协作模式  
✅ ACP集成方法  
✅ 任务编排策略  

### 关键要点：
1. **Sub-Agent适合后台任务**
2. **多Agent提高并行效率**
3. **ACP专注代码生成**
4. **任务编排需要合理设计**

---

**下节课见！** 🚀
