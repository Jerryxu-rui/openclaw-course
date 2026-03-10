# 第8课：自动化工作流 - 解放双手

## 课程目标
- 理解Heartbeat机制
- 配置Cron定时任务
- 设计自动化工作流
- 实现端到端自动化

---

## 第一部分：Heartbeat机制（30分钟）

### 1.1 什么是Heartbeat？

#### 定义
```
Heartbeat是OpenClaw的周期性检查机制：
- 定期唤醒Agent
- 执行预设任务
- 无需用户触发
- 自动化运行
```

#### 工作原理
```
[每30分钟]
  ↓
[读取HEARTBEAT.md]
  ↓
[执行任务]
  ↓
[返回结果或HEARTBEAT_OK]
```

### 1.2 配置Heartbeat

#### 编辑HEARTBEAT.md
```bash
nano ~/.openclaw/workspace/HEARTBEAT.md
```

#### 示例配置
```markdown
# HEARTBEAT.md

## 任务列表

### 1. 检查邮件
- 每次心跳检查未读邮件
- 如有重要邮件，通知我

### 2. 日程提醒
- 检查未来2小时的日程
- 提前15分钟提醒

### 3. 系统监控
- 检查磁盘使用率
- 超过80%时警告
```

#### 配置检查频率
```json
{
  "agents": {
    "defaults": {
      "heartbeat": {
        "every": "30m"
      }
    }
  }
}
```

**可选值：**
- `"15m"` - 每15分钟
- `"30m"` - 每30分钟（默认）
- `"1h"` - 每小时
- `"2h"` - 每2小时

### 1.3 Heartbeat最佳实践

#### 原则1：批量检查
```markdown
# ❌ 错误：每个任务单独心跳
- 检查邮件（每15分钟）
- 检查日历（每15分钟）
- 检查天气（每15分钟）

# ✅ 正确：批量检查
- 每30分钟检查：邮件、日历、天气
```

#### 原则2：轮换检查
```markdown
# 轮换策略
- 心跳1：检查邮件 + 日历
- 心跳2：检查天气 + 系统
- 心跳3：检查邮件 + 日历
- 心跳4：检查天气 + 系统
```

---

## 第二部分：实战案例 - 智能股票分析自动化系统（45分钟）

### 2.1 案例背景

#### 业务需求
作为投资者，需要：
1. 每日获取关注的股票数据
2. 自动分析技术指标和基本面
3. 生成投资分析报告
4. 实时监控风险并预警

#### 传统方式的问题
- 手动操作耗时耗力
- 容易错过重要信息
- 分析结果主观性强
- 无法实时监控

#### OpenClaw解决方案
通过自动化工作流实现：
- 定时数据获取和分析
- 自动报告生成
- 实时风险监控
- 多渠道预警通知

### 2.2 系统架构设计

```
智能股票分析自动化系统
├── 数据获取层
│   ├── Tushare API（专业数据）
│   └── Akshare（免费数据）
├── 分析处理层
│   ├── 技术分析模块
│   ├── 基本面分析模块
│   └── 风险评估模块
├── 自动化调度层
│   ├── Heartbeat定时任务
│   ├── Cron作业调度
│   └── 实时监控循环
├── 输出报告层
│   ├── Markdown报告
│   ├── Word文档
│   └── 可视化图表
└── 通知预警层
    ├── 飞书通知
    ├── Telegram推送
    └── 邮件提醒
```

### 2.3 Heartbeat配置实现

#### 每日分析任务配置
```markdown
# ~/.openclaw/workspace/HEARTBEAT.md

## 智能股票分析系统

### 每日任务（交易日9:00执行）
1. 获取关注的股票数据
   - 贵州茅台 (600519.SH)
   - 五粮液 (000858.SZ)
   - 招商银行 (600036.SH)
   - 中国平安 (601318.SH)

2. 执行技术分析
   - 计算RSI、MACD、布林带
   - 生成交易信号

3. 执行基本面分析
   - 财务比率分析
   - 估值计算
   - 风险检测

4. 生成投资晨报
   - 汇总分析结果
   - 生成Markdown报告
   - 转换为Word格式

5. 发送通知
   - 飞书群推送报告
   - Telegram发送摘要
```

#### 实时监控配置
```markdown
### 实时监控（每30分钟执行）
1. 监控价格异常
   - 检查价格波动超过5%
   - 检测成交量异常放大

2. 监控技术指标
   - RSI超买超卖预警
   - MACD金叉死叉信号

3. 风险预警
   - 达到止损条件提醒
   - 重大新闻事件监控
```

### 2.4 Cron任务配置

#### 定时任务脚本
```bash
# ~/.openclaw/workspace/scripts/daily_stock_analysis.sh
#!/bin/bash

# 配置
STOCK_LIST="600519.SH 000858.SZ 600036.SH 601318.SH"
ANALYSIS_DIR="/home/jerryxu/.openclaw/stock-analysis/reports"
DATE=$(date +%Y%m%d)

echo "开始执行每日股票分析: $DATE"

# 1. 创建报告目录
mkdir -p $ANALYSIS_DIR/$DATE

# 2. 分析每只股票
for STOCK in $STOCK_LIST; do
    echo "分析: $STOCK"
    
    # 获取数据
    python ~/.openclaw/stock-analysis/scripts/data_fetcher.py \
        --code $STOCK \
        --output $ANALYSIS_DIR/$DATE/${STOCK}_data.json
    
    # 技术分析
    python ~/.openclaw/stock-analysis/scripts/technical_analyzer.py \
        --input $ANALYSIS_DIR/$DATE/${STOCK}_data.json \
        --output $ANALYSIS_DIR/$DATE/${STOCK}_technical.json
    
    # 基本面分析
    python ~/.openclaw/stock-analysis/scripts/fundamental_analyzer.py \
        --input $ANALYSIS_DIR/$DATE/${STOCK}_data.json \
        --output $ANALYSIS_DIR/$DATE/${STOCK}_fundamental.json
    
    # 风险评估
    python ~/.openclaw/stock-analysis/scripts/risk_assessor.py \
        --technical $ANALYSIS_DIR/$DATE/${STOCK}_technical.json \
        --fundamental $ANALYSIS_DIR/$DATE/${STOCK}_fundamental.json \
        --output $ANALYSIS_DIR/$DATE/${STOCK}_risk.json
done

# 3. 生成汇总报告
python ~/.openclaw/stock-analysis/scripts/report_generator.py \
    --date $DATE \
    --dir $ANALYSIS_DIR/$DATE \
    --output $ANALYSIS_DIR/$DATE/daily_report.md

# 4. 发送通知
python ~/.openclaw/stock-analysis/scripts/notification_sender.py \
    --file $ANALYSIS_DIR/$DATE/daily_report.md \
    --title "每日投资晨报 $DATE"

echo "每日股票分析完成"
```

#### Cron配置
```bash
# 编辑crontab
crontab -e

# 添加以下配置
# 每个交易日早上9:00执行分析
0 9 * * 1-5 /home/jerryxu/.openclaw/workspace/scripts/daily_stock_analysis.sh >> /tmp/stock_analysis.log 2>&1

# 每30分钟执行实时监控
*/30 * * * * /home/jerryxu/.openclaw/workspace/scripts/stock_monitor.sh >> /tmp/stock_monitor.log 2>&1

# 每周五下午生成周报
0 17 * * 5 /home/jerryxu/.openclaw/workspace/scripts/weekly_summary.sh >> /tmp/stock_weekly.log 2>&1
```

### 2.5 实时监控系统实现

#### 监控脚本
```python
# ~/.openclaw/workspace/scripts/stock_monitor.py
import time
import json
from datetime import datetime

class StockMonitor:
    def __init__(self, watchlist, alert_channels):
        self.watchlist = watchlist
        self.alert_channels = alert_channels
        self.monitoring = True
    
    def start_monitoring(self, interval=1800):  # 30分钟
        """启动监控"""
        print(f"股票监控系统启动，监控间隔: {interval}秒")
        
        while self.monitoring:
            for stock in self.watchlist:
                self.check_stock(stock)
            
            time.sleep(interval)
    
    def check_stock(self, stock):
        """检查股票状态"""
        # 获取实时数据
        data = self.get_realtime_data(stock['code'])
        
        # 检查价格异常
        if self.is_price_anomaly(stock, data):
            self.send_alert(stock, "价格异常波动", data)
        
        # 检查成交量异常
        if self.is_volume_anomaly(stock, data):
            self.send_alert(stock, "成交量异常放大", data)
        
        # 检查技术指标风险
        if self.is_technical_risk(stock, data):
            self.send_alert(stock, "技术指标风险", data)
    
    def send_alert(self, stock, alert_type, data):
        """发送预警"""
        message = f"""
🚨 股票监控预警
📈 股票: {stock['name']} ({stock['code']})
⚠️ 预警类型: {alert_type}
💰 当前价格: ¥{data['price']}
📊 涨跌幅: {data['change_percent']}%
⏰ 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        # 发送到配置的渠道
        for channel in self.alert_channels:
            if channel['type'] == 'feishu':
                self.send_feishu_alert(channel, message)
            elif channel['type'] == 'telegram':
                self.send_telegram_alert(channel, message)
```

#### 监控配置
```json
{
  "monitoring": {
    "watchlist": [
      {
        "code": "600519.SH",
        "name": "贵州茅台",
        "stop_loss": 1500,
        "take_profit": 2000
      },
      {
        "code": "000858.SZ",
        "name": "五粮液",
        "stop_loss": 120,
        "take_profit": 180
      }
    ],
    "alert_channels": [
      {
        "type": "feishu",
        "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/xxx"
      },
      {
        "type": "telegram",
        "bot_token": "xxx",
        "chat_id": "-100xxx"
      }
    ],
    "check_interval": 1800,
    "price_alert_threshold": 0.05,
    "volume_alert_threshold": 3.0
  }
}
```

### 2.6 自动化报告生成

#### 报告生成脚本
```python
# ~/.openclaw/workspace/scripts/report_generator.py
import json
from datetime import datetime

class ReportGenerator:
    def generate_daily_report(self, analysis_data, date):
        """生成每日报告"""
        report = f"""# 每日投资晨报 - {date}

## 市场概况
- 分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- 关注股票: {len(analysis_data)} 只
- 整体市场情绪: {self.get_market_sentiment(analysis_data)}

## 个股分析

"""
        
        for stock in analysis_data:
            report += self.generate_stock_section(stock)
        
        report += """
## 投资建议

### 今日操作策略
1. **重点关注**: 技术指标良好且估值合理的股票
2. **风险控制**: 设置止损位，控制单只股票仓位
3. **机会把握**: 关注超跌反弹机会

### 风险提示
- 市场波动风险
- 个股基本面变化风险
- 系统性风险

## 免责声明
本报告由自动化系统生成，仅供参考，不构成投资建议。
"""
        
        return report
    
    def generate_stock_section(self, stock_data):
        """生成个股分析部分"""
        return f"""
### {stock_data['name']} ({stock_data['code']})

#### 技术分析
- **当前价格**: ¥{stock_data['price']}
- **RSI**: {stock_data['rsi']} ({self.get_rsi_status(stock_data['rsi'])})
- **MACD**: {stock_data['macd_signal']}
- **布林带位置**: {self.get_bollinger_position(stock_data)}

#### 基本面分析
- **PE**: {stock_data['pe']} (行业平均: {stock_data['industry_pe']})
- **ROE**: {stock_data['roe']}%
- **股息率**: {stock_data['dividend_yield']}%

#### 风险评估
- **风险等级**: {stock_data['risk_level']}
- **主要风险**: {', '.join(stock_data['risks'][:3])}

#### 操作建议
{stock_data['recommendation']}
"""

#### 报告自动化流程
```bash
# 报告生成和发送流程
1. 数据收集 → 2. 分析处理 → 3. 报告生成 → 4. 格式转换 → 5. 多渠道发送

# 具体实现
python collect_data.py          # 收集数据
python analyze_stocks.py        # 分析处理
python generate_report.py       # 生成报告
pandoc report.md -o report.docx # 转换为Word
python send_notifications.py    # 发送通知
```

### 2.7 错误处理与日志管理

#### 错误处理策略
```python
class StockAnalysisErrorHandler:
    def handle_api_error(self, error):
        """处理API错误"""
        if "rate limit" in str(error).lower():
            print("API调用频率限制，等待重试...")
            time.sleep(60)
            return True  # 重试
        elif "network" in str(error).lower():
            print("网络错误，检查连接...")
            return False  # 不重试
        else:
            print(f"未知API错误: {error}")
            return False
    
    def handle_data_error(self, error):
        """处理数据错误"""
        if "missing data" in str(error).lower():
            print("数据缺失，使用默认值...")
            return self.use_default_values()
        else:
            print(f"数据错误: {error}")
            return None
    
    def handle_report_error(self, error):
        """处理报告生成错误"""
        print(f"报告生成错误: {error}")
        # 发送错误通知
        self.send_error_notification(error)
        return None
```

#### 日志管理配置
```python
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/openclaw/stock_analysis.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('stock_analysis')

# 使用示例
logger.info("开始执行每日股票分析")
logger.warning("API调用接近限制")
logger.error("数据获取失败", exc_info=True)
```

### 2.8 性能优化

#### 缓存策略
```python
import redis
import pickle

class DataCache:
    def __init__(self):
        self.redis = redis.Redis(host='localhost', port=6379, db=0)
    
    def get_cached_data(self, key, ttl=3600):
        """获取缓存数据"""
        data = self.redis.get(key)
        if data:
            return pickle.loads(data)
        return None
    
    def set_cached_data(self, key, data, ttl=3600):
        """设置缓存数据"""
        self.redis.setex(key, ttl, pickle.dumps(data))
```

#### 并行处理
```python
from concurrent.futures import ThreadPoolExecutor

class ParallelProcessor:
    def analyze_multiple_stocks(self, stock_codes):
        """并行分析多只股票"""
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {
                executor.submit(self.analyze_stock, code): code
                for code in stock_codes
            }
            
            results = {}
            for future in futures:
                code = futures[future]
                try:
                    results[code] = future.result(timeout=30)
                except Exception as e:
                    print(f"分析{code}失败: {e}")
                    results[code] = None
            
            return results
```

### 2.9 案例总结

#### 实现效果
1. **自动化程度高**：从数据获取到报告生成全自动
2. **实时性强**：30分钟间隔的实时监控
3. **可靠性好**：完善的错误处理和日志管理
4. **扩展性强**：模块化设计，易于扩展

#### 技术要点
1. **多工具整合**：Heartbeat + Cron + 自定义脚本
2. **错误处理**：分级错误处理和重试机制
3. **性能优化**：缓存 + 并行处理
4. **监控告警**：实时监控和预警系统

#### 业务价值
1. **效率提升**：节省90%以上的分析时间
2. **决策支持**：提供数据驱动的投资建议
3. **风险控制**：实时监控和风险预警
4. **知识积累**：自动化的投资知识库

---

## 第三部分：Cron定时任务（30分钟）

#### 原则3：智能过滤
```markdown
# 只在需要时通知
- 邮件：仅重要邮件
- 日历：仅未来2小时
- 天气：仅天气变化
- 系统：仅超过阈值
```

#### 原则4：时间感知
```markdown
# 根据时间调整
- 工作时间（9-18点）：检查邮件、日历
- 休息时间（18-23点）：检查天气、新闻
- 睡眠时间（23-9点）：仅紧急警告
```

### 1.4 实战示例

#### 示例1：邮件监控
```markdown
# HEARTBEAT.md

检查Gmail未读邮件：
- 仅检查重要邮件（标星或来自VIP）
- 生成摘要
- 如有紧急邮件，立即通知Telegram
- 否则返回HEARTBEAT_OK
```

**执行效果：**
```
[心跳触发]
[检查Gmail]
[发现2封重要邮件]

Telegram通知：
📧 新邮件提醒

1. 来自：老板
   主题：项目进度
   摘要：询问本周进展...
   
2. 来自：客户
   主题：紧急需求
   摘要：需要尽快处理...
```

#### 示例2：日程提醒
```markdown
# HEARTBEAT.md

检查飞书日历：
- 查看未来2小时的日程
- 提前15分钟提醒
- 包含会议链接和准备事项
```

**执行效果：**
```
[心跳触发]
[检查日历]
[发现14:00有会议]

Telegram通知（13:45）：
📅 会议提醒

时间：14:00-15:00
主题：项目评审会
地点：3楼会议室
参会人：张三、李四、王五

准备事项：
- 项目进度报告
- Demo演示
- Q&A准备

会议链接：https://...
```

#### 示例3：系统监控
```markdown
# HEARTBEAT.md

监控系统状态：
- 磁盘使用率
- 内存使用率
- CPU温度
- 超过阈值时警告
```

**执行效果：**
```
[心跳触发]
[检查系统]
[磁盘使用率85%]

Telegram通知：
⚠️ 系统警告

磁盘使用率：85%（阈值80%）
剩余空间：15GB
建议：清理临时文件

大文件Top 5：
1. /home/user/Downloads/video.mp4 (5GB)
2. /home/user/.cache (3GB)
3. ...
```

---

## 第二部分：Cron定时任务（30分钟）

### 2.1 Heartbeat vs Cron

#### 对比
```
Heartbeat：
- 周期性检查
- 批量任务
- 上下文共享
- 适合：监控、提醒

Cron：
- 精确时间
- 独立任务
- 隔离执行
- 适合：报告、备份
```

#### 选择建议
```
使用Heartbeat：
- 多个检查批量执行
- 需要对话上下文
- 时间可以漂移

使用Cron：
- 精确时间要求
- 独立任务
- 一次性提醒
```

### 2.2 配置Cron任务

#### 方法1：通过对话配置
```
You: 每天早上9点提醒我查看日程

Agent: ✅ 已设置定时提醒

任务详情：
- 时间：每天09:00
- 内容：查看今日日程
- 通知渠道：Telegram

Cron表达式：0 9 * * *
```

#### 方法2：直接配置
```json
{
  "automation": {
    "cron": {
      "jobs": [
        {
          "name": "daily-report",
          "schedule": "0 9 * * *",
          "task": "生成昨日工作总结并发送到飞书",
          "enabled": true
        },
        {
          "name": "weekly-backup",
          "schedule": "0 0 * * 0",
          "task": "备份workspace到云盘",
          "enabled": true
        }
      ]
    }
  }
}
```

### 2.3 Cron表达式

#### 基本格式
```
* * * * *
│ │ │ │ │
│ │ │ │ └─ 星期 (0-7, 0和7都表示周日)
│ │ │ └─── 月份 (1-12)
│ │ └───── 日期 (1-31)
│ └─────── 小时 (0-23)
└───────── 分钟 (0-59)
```

#### 常用示例
```
每天早上9点：
0 9 * * *

每周一早上9点：
0 9 * * 1

每月1号早上9点：
0 9 1 * *

每小时：
0 * * * *

每30分钟：
*/30 * * * *

工作日早上9点：
0 9 * * 1-5

周末早上10点：
0 10 * * 0,6
```

### 2.4 实战示例

#### 示例1：每日报告
```
任务：每天早上9点生成昨日工作总结

配置：
{
  "name": "daily-report",
  "schedule": "0 9 * * *",
  "task": "生成昨日工作总结",
  "output": "飞书"
}

执行效果：
[每天09:00触发]
[读取昨日记忆]
[生成总结]
[发送到飞书]

飞书消息：
📊 昨日工作总结（2026-03-08）

完成事项：
1. ✅ 完成OpenClaw课程第1-6课
2. ✅ 配置记忆搜索系统
3. ✅ 修复Gateway进程问题

时间分配：
- 课程开发：6小时
- 系统配置：2小时
- 问题排查：1小时

明日计划：
- 完成第7-9课
- 测试记忆蒸馏
- 优化成本配置
```

#### 示例2：周报生成
```
任务：每周一早上9点生成上周工作周报

配置：
{
  "name": "weekly-report",
  "schedule": "0 9 * * 1",
  "task": "生成上周工作周报",
  "output": "飞书+邮件"
}

执行效果：
[每周一09:00触发]
[读取上周记忆]
[分析数据]
[生成周报]

周报内容：
📈 工作周报（2026-03-03 ~ 2026-03-09）

本周成就：
1. ✅ 完成OpenClaw课程开发（6课）
2. ✅ 配置多渠道集成
3. ✅ 优化成本策略

数据统计：
- 对话轮次：234次
- Token消耗：1.2M
- 成本：$12.5
- 节省：87%（vs全用Claude）

下周计划：
- 完成剩余10课
- 发布课程
- 推广宣传
```

#### 示例3：定时备份
```
任务：每天凌晨2点备份workspace

配置：
{
  "name": "backup",
  "schedule": "0 2 * * *",
  "task": "备份workspace到云盘"
}

执行效果：
[每天02:00触发]
[压缩workspace]
[上传到云盘]
[清理旧备份]

Telegram通知（如果失败）：
⚠️ 备份失败

时间：2026-03-09 02:00
原因：网络连接超时
建议：检查网络或手动备份
```

---

## 第三部分：工作流设计（40分钟）

### 3.1 工作流模式

#### 模式1：监控-通知
```
[监控数据源]
  ↓
[检测变化]
  ↓
[生成通知]
  ↓
[发送到渠道]
```

**示例：**
- 邮件监控
- 日程提醒
- 系统警告
- 价格监控

#### 模式2：收集-分析-报告
```
[收集数据]
  ↓
[分析整理]
  ↓
[生成报告]
  ↓
[定时发送]
```

**示例：**
- 每日总结
- 周报生成
- 月度分析
- 竞品监控

#### 模式3：触发-执行-反馈
```
[触发条件]
  ↓
[执行任务]
  ↓
[反馈结果]
```

**示例：**
- 自动回复
- 任务分配
- 数据同步
- 文件处理

### 3.2 工作流设计原则

#### 原则1：单一职责
```
❌ 错误：一个工作流做太多事
- 检查邮件
- 生成报告
- 发送通知
- 备份数据

✅ 正确：拆分为多个工作流
- 工作流1：邮件监控
- 工作流2：报告生成
- 工作流3：通知发送
- 工作流4：数据备份
```

#### 原则2：容错处理
```
工作流应该：
- 处理异常情况
- 重试失败任务
- 记录错误日志
- 通知管理员

示例：
try {
  [执行任务]
} catch (error) {
  [记录日志]
  [重试3次]
  if (仍然失败) {
    [通知管理员]
  }
}
```

#### 原则3：可观测性
```
工作流应该：
- 记录执行日志
- 统计成功率
- 监控性能
- 可视化状态

示例：
工作流执行报告：
- 总执行次数：100
- 成功：95
- 失败：5
- 平均耗时：2.3秒
- 最后执行：2026-03-09 09:00
```

### 3.3 实战工作流

#### 工作流1：智能邮件助手
```
目标：自动处理邮件

步骤：
1. 每30分钟检查新邮件
2. 分类：重要/普通/垃圾
3. 重要邮件：立即通知
4. 普通邮件：每日摘要
5. 垃圾邮件：自动归档

配置：
# HEARTBEAT.md
检查Gmail：
- 重要邮件（标星/VIP）→ 立即通知Telegram
- 普通邮件 → 记录到daily-emails.md
- 垃圾邮件 → 自动归档

# Cron
每天18:00生成邮件摘要：
- 读取daily-emails.md
- 生成摘要
- 发送到飞书
```

#### 工作流2：项目进度跟踪
```
目标：自动跟踪项目进度

步骤：
1. 每天检查GitHub仓库
2. 统计commits、issues、PRs
3. 分析进度
4. 生成报告
5. 发送到团队群

配置：
# Cron: 每天18:00
任务：
1. 获取GitHub数据
   - Commits（今日）
   - Issues（新增/关闭）
   - PRs（新增/合并）
   
2. 分析进度
   - 完成率
   - 延期风险
   - 团队贡献
   
3. 生成报告
   - Markdown格式
   - 包含图表
   - 突出重点
   
4. 发送到飞书群
```

#### 工作流3：知识库自动更新
```
目标：自动更新知识库

步骤：
1. 监控多个信息源
2. 提取关键信息
3. 整理成文档
4. 更新到飞书知识库

配置：
# Heartbeat: 每2小时
监控来源：
- 官方文档
- GitHub Issues
- Discord讨论
- Reddit帖子

处理流程：
1. 检测新内容
2. 提取关键信息
3. 生成Markdown
4. 更新到飞书知识库
5. 通知团队

# Cron: 每周日20:00
生成周报：
- 本周新增内容
- 热门话题
- 待解决问题
```

---

## 第四部分：实战项目（30分钟）

### 项目：个人工作自动化系统

#### 需求
1. 邮件自动处理
2. 日程智能提醒
3. 每日工作总结
4. 周报自动生成

#### 实现

**步骤1：配置Heartbeat**
```markdown
# HEARTBEAT.md

## 邮件监控（每30分钟）
检查Gmail重要邮件：
- 来自老板/客户的邮件
- 标星邮件
- 紧急标记邮件

如有重要邮件：
- 生成摘要
- 通知Telegram
- 标记为已读

否则：
- 返回HEARTBEAT_OK

## 日程提醒（每30分钟）
检查飞书日历：
- 未来2小时的日程
- 提前15分钟提醒

如有日程：
- 生成提醒
- 包含会议链接
- 列出准备事项
- 通知Telegram

否则：
- 返回HEARTBEAT_OK

## 系统监控（每2小时）
检查系统状态：
- 磁盘使用率 > 80%
- 内存使用率 > 90%
- CPU温度 > 80°C

如有异常：
- 生成警告
- 通知Telegram

否则：
- 返回HEARTBEAT_OK
```

**步骤2：配置Cron任务**
```json
{
  "automation": {
    "cron": {
      "jobs": [
        {
          "name": "daily-summary",
          "schedule": "0 18 * * *",
          "task": "生成今日工作总结并发送到飞书",
          "enabled": true
        },
        {
          "name": "weekly-report",
          "schedule": "0 18 * * 5",
          "task": "生成本周工作周报并发送到飞书+邮件",
          "enabled": true
        },
        {
          "name": "morning-briefing",
          "schedule": "0 9 * * 1-5",
          "task": "生成今日简报（天气+日程+待办）并发送到Telegram",
          "enabled": true
        }
      ]
    }
  }
}
```

**步骤3：测试运行**
```
You: 测试一下自动化系统

Agent: [执行测试]

✅ Heartbeat测试
- 邮件监控：正常
- 日程提醒：正常
- 系统监控：正常

✅ Cron任务测试
- 每日总结：已触发（模拟）
- 周报生成：已触发（模拟）
- 早间简报：已触发（模拟）

测试报告：
- 所有任务正常
- 通知渠道畅通
- 数据获取成功

系统已就绪，将按计划自动运行。
```

**步骤4：实际运行效果**
```
[每天09:00 - 早间简报]
Telegram通知：
☀️ 早安！今日简报

天气：多云 15-25°C
空气质量：良

今日日程：
- 10:00 团队站会
- 14:00 项目评审
- 16:00 客户沟通

待办事项：
- [ ] 完成项目报告
- [ ] 回复客户邮件
- [ ] 准备评审材料

[每天18:00 - 每日总结]
飞书消息：
📊 今日工作总结

完成事项：
1. ✅ 完成项目报告
2. ✅ 回复客户邮件
3. ✅ 参加3个会议

时间分配：
- 开发：4小时
- 会议：2小时
- 沟通：1小时

明日计划：
- 继续开发功能X
- 准备周五演示
- 跟进客户反馈

[每周五18:00 - 周报]
飞书+邮件：
📈 本周工作周报

本周成就：
1. ✅ 完成功能A开发
2. ✅ 修复10个Bug
3. ✅ 完成2次客户演示

数据统计：
- Commits：45次
- 代码行数：+2,340
- 会议时间：8小时

下周计划：
- 开发功能B
- 性能优化
- 准备上线
```

---

## 第五部分：作业与练习（课后）

### 作业1：配置Heartbeat（必做）

**任务：**
配置至少2个Heartbeat任务

**推荐任务：**
1. 邮件监控
2. 日程提醒
3. 系统监控
4. 天气查询

**提交：**
- HEARTBEAT.md文件
- 运行截图
- 通知示例

### 作业2：配置Cron任务（必做）

**任务：**
配置至少2个Cron任务

**推荐任务：**
1. 每日总结
2. 周报生成
3. 定时备份
4. 早间简报

**提交：**
- 配置文件
- Cron表达式
- 执行结果

### 作业3：设计工作流（选做）

**任务：**
设计一个完整的自动化工作流

**要求：**
1. 明确目标
2. 设计流程
3. 配置实现
4. 测试验证

**提交：**
- 工作流设计文档
- 配置文件
- 运行截图
- 效果评估

---

## 第六部分：常见问题（10分钟）

### Q1：Heartbeat不执行怎么办？

**A1：**
```bash
# 检查配置
cat ~/.openclaw/openclaw.json | grep heartbeat

# 检查HEARTBEAT.md
cat ~/.openclaw/workspace/HEARTBEAT.md

# 查看日志
openclaw gateway logs | grep heartbeat

# 手动触发测试
openclaw chat "执行HEARTBEAT.md中的任务"
```

### Q2：Cron任务没有触发？

**A2：**
```bash
# 检查Cron配置
cat ~/.openclaw/openclaw.json | grep cron

# 验证Cron表达式
# 使用在线工具：https://crontab.guru

# 查看日志
openclaw gateway logs | grep cron

# 手动触发测试
openclaw cron run daily-summary
```

### Q3：如何调试工作流？

**A3：**
```
1. 添加日志输出
2. 使用测试模式
3. 逐步执行
4. 检查中间结果

示例：
You: 测试邮件监控工作流

Agent: [执行测试]
步骤1：连接Gmail ✅
步骤2：获取邮件列表 ✅
步骤3：筛选重要邮件 ✅
步骤4：生成摘要 ✅
步骤5：发送通知 ✅

测试通过！
```

### Q4：如何优化性能？

**A4：**
```
优化策略：
1. 减少检查频率
2. 使用缓存
3. 批量处理
4. 异步执行

示例：
# 优化前
- 每15分钟检查邮件
- 每15分钟检查日历
- 每15分钟检查天气

# 优化后
- 每30分钟批量检查所有
- 使用缓存避免重复请求
- 异步执行不阻塞
```

### Q5：如何处理失败？

**A5：**
```
容错策略：
1. 重试机制
2. 降级方案
3. 错误通知
4. 日志记录

示例：
try {
  [执行任务]
} catch (error) {
  [记录日志]
  [重试3次]
  if (仍然失败) {
    [使用降级方案]
    [通知管理员]
  }
}
```

---

## 第七部分：扩展阅读

### 推荐资源

#### 官方文档
- Heartbeat：https://docs.openclaw.ai/concepts/heartbeat
- Cron：https://docs.openclaw.ai/automation/cron
- 工作流：https://docs.openclaw.ai/automation/workflows

#### 工具
- Cron表达式：https://crontab.guru
- 工作流设计：https://mermaid.js.org

### 下节课预告

**第9课：文档处理 - 办公自动化**
- PDF处理实战
- Word文档自动化
- Excel数据分析
- 飞书文档集成

---

## 课程总结

### 本节课你学到了：
✅ Heartbeat机制的原理和配置  
✅ Cron定时任务的使用  
✅ 工作流设计原则  
✅ 自动化系统实战  
✅ 容错和优化策略  

### 关键要点：
1. **Heartbeat适合周期性检查**
2. **Cron适合精确时间任务**
3. **工作流要单一职责**
4. **容错处理很重要**
5. **可观测性是关键**

### 下一步：
1. 完成作业1和作业2（必做）
2. 尝试作业3（选做）
3. 设计自己的工作流
4. 准备学习第9课（文档处理）

---

**课程反馈：**
如有问题或建议，请在GitHub提Issue或加入社区讨论。

**下节课见！** 🚀
