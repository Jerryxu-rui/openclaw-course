# 金融实战案例2：智能股票分析系统

## 案例背景

在智能体金融（Agentic Finance）的浪潮中，除了高频交易和预测市场套利，另一个重要方向是**智能投资分析**。传统的股票分析需要投资者花费大量时间研究财务报表、技术指标和市场数据，而OpenClaw可以自动化这一过程。

本案例将展示如何利用OpenClaw构建一个完整的智能股票分析系统，整合两个核心skills：
1. **tushare-stock-skill** - 专业股票数据获取与技术分析
2. **china-stock-analysis** - 价值投资导向的基本面分析

---

## 第一部分：系统架构设计

### 1.1 整体架构

```
智能股票分析系统架构
├── 数据层
│   ├── tushare-stock-skill (专业数据)
│   └── china-stock-analysis (免费数据)
├── 分析层
│   ├── 技术分析模块
│   ├── 基本面分析模块
│   └── 风险评估模块
├── 决策层
│   ├── 投资建议生成
│   └── 风险预警系统
├── 报告层
│   ├── 自动报告生成
│   └── 可视化展示
└── 监控层
    ├── 定时监控
    └── 实时预警
```

### 1.2 技术选型对比

| 维度 | tushare-stock-skill | china-stock-analysis | 整合优势 |
|------|-------------------|---------------------|---------|
| **数据源** | Tushare Pro API | Akshare免费数据 | 专业+免费互补 |
| **分析重点** | 技术指标、实时数据 | 财务分析、估值模型 | 技术面+基本面结合 |
| **使用成本** | 需要API Token | 完全免费 | 成本可控 |
| **数据深度** | 全面专业 | 基础实用 | 深度+广度 |
| **适用场景** | 量化交易、高频监控 | 价值投资、长期分析 | 多策略覆盖 |

### 1.3 系统工作流程

```
1. 数据获取 → 2. 技术分析 → 3. 基本面分析 → 4. 风险评估 → 5. 投资建议 → 6. 报告生成
```

---

## 第二部分：环境配置与安装

### 2.1 基础环境准备

```bash
# 1. 创建专用工作目录
mkdir -p ~/.openclaw/stock-analysis
cd ~/.openclaw/stock-analysis

# 2. 安装Python环境（如果尚未安装）
python3 -m venv venv
source venv/bin/activate

# 3. 安装基础依赖
pip install pandas numpy matplotlib seaborn
```

### 2.2 安装tushare-stock-skill

```bash
# 1. 克隆skill仓库
git clone https://github.com/Magica-Chen/tushare-stock-skill.git
cd tushare-stock-skill

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置Tushare Token
# 获取Token：访问 https://tushare.pro 注册并获取API Token
export TUSHARE_TOKEN="你的Tushare Pro Token"

# 4. 可选：设置缓存目录
export TUSHARE_STOCK_CACHE_DIR="~/.openclaw/stock-analysis/cache"
mkdir -p ~/.openclaw/stock-analysis/cache

# 5. 测试安装
python scripts/tushare_stock.py run --text "测试连接"
```

### 2.3 安装china-stock-analysis

```bash
# 1. 返回工作目录
cd ~/.openclaw/stock-analysis

# 2. 安装Akshare及相关依赖
pip install akshare

# 3. 创建技能目录结构
mkdir -p china-stock-analysis/{scripts,templates,data}

# 4. 创建主脚本（简化版）
cat > china-stock-analysis/scripts/stock_analyzer.py << 'EOF'
#!/usr/bin/env python3
import akshare as ak
import pandas as pd
import json
import sys

def get_stock_basic(code):
    """获取股票基本信息"""
    stock_info = ak.stock_individual_info_em(symbol=code)
    return stock_info

def get_financial_report(code):
    """获取财务报表"""
    # 这里简化实现，实际需要更复杂的逻辑
    pass

if __name__ == "__main__":
    if len(sys.argv) > 1:
        code = sys.argv[1]
        info = get_stock_basic(code)
        print(json.dumps(info.to_dict(), ensure_ascii=False, indent=2))
EOF

chmod +x china-stock-analysis/scripts/stock_analyzer.py
```

### 2.4 OpenClaw集成配置

```json
// ~/.openclaw/openclaw.json 添加配置
{
  "skills": {
    "entries": {
      "tushare-stock": {
        "path": "/home/jerryxu/.openclaw/stock-analysis/tushare-stock-skill",
        "env": {
          "TUSHARE_TOKEN": "你的Token",
          "TUSHARE_STOCK_CACHE_DIR": "/home/jerryxu/.openclaw/stock-analysis/cache"
        }
      },
      "china-stock": {
        "path": "/home/jerryxu/.openclaw/stock-analysis/china-stock-analysis"
      }
    }
  }
}
```

---

## 第三部分：核心功能实现

### 3.1 数据获取模块

#### Tushare数据获取
```python
# scripts/data_fetcher_tushare.py
import tushare as ts
import pandas as pd
import json

class TushareDataFetcher:
    def __init__(self, token):
        ts.set_token(token)
        self.pro = ts.pro_api()
    
    def get_daily_data(self, ts_code, start_date, end_date):
        """获取日线数据"""
        df = self.pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
        return df
    
    def get_basic_data(self, ts_code):
        """获取股票基本信息"""
        df = self.pro.daily_basic(ts_code=ts_code)
        return df
    
    def get_financial_data(self, ts_code):
        """获取财务数据"""
        df = self.pro.income(ts_code=ts_code)
        return df
```

#### Akshare数据获取
```python
# scripts/data_fetcher_akshare.py
import akshare as ak
import pandas as pd

class AkshareDataFetcher:
    def get_stock_info(self, symbol):
        """获取股票基本信息"""
        return ak.stock_individual_info_em(symbol=symbol)
    
    def get_historical_data(self, symbol, period="daily", adjust=""):
        """获取历史数据"""
        return ak.stock_zh_a_hist(symbol=symbol, period=period, adjust=adjust)
    
    def get_financial_report(self, symbol, indicator="资产负债表"):
        """获取财务报表"""
        return ak.stock_financial_report_sina(symbol=symbol, indicator=indicator)
```

### 3.2 技术分析模块

```python
# scripts/technical_analyzer.py
import pandas as pd
import numpy as np
import talib

class TechnicalAnalyzer:
    def __init__(self, data):
        self.data = data
    
    def calculate_indicators(self):
        """计算技术指标"""
        close = self.data['close'].values
        
        # RSI
        self.data['rsi'] = talib.RSI(close, timeperiod=14)
        
        # MACD
        macd, signal, hist = talib.MACD(close)
        self.data['macd'] = macd
        self.data['macd_signal'] = signal
        self.data['macd_hist'] = hist
        
        # 布林带
        upper, middle, lower = talib.BBANDS(close)
        self.data['bb_upper'] = upper
        self.data['bb_middle'] = middle
        self.data['bb_lower'] = lower
        
        # 移动平均线
        self.data['ma5'] = talib.SMA(close, timeperiod=5)
        self.data['ma10'] = talib.SMA(close, timeperiod=10)
        self.data['ma20'] = talib.SMA(close, timeperiod=20)
        
        return self.data
    
    def generate_signals(self):
        """生成交易信号"""
        signals = []
        
        # RSI超买超卖信号
        if self.data['rsi'].iloc[-1] > 70:
            signals.append("RSI超买，注意回调风险")
        elif self.data['rsi'].iloc[-1] < 30:
            signals.append("RSI超卖，可能存在机会")
        
        # MACD金叉死叉信号
        if self.data['macd'].iloc[-1] > self.data['macd_signal'].iloc[-1]:
            signals.append("MACD金叉，短期看涨")
        else:
            signals.append("MACD死叉，短期看跌")
        
        # 布林带突破信号
        current_close = self.data['close'].iloc[-1]
        if current_close > self.data['bb_upper'].iloc[-1]:
            signals.append("突破布林带上轨，强势但可能回调")
        elif current_close < self.data['bb_lower'].iloc[-1]:
            signals.append("跌破布林带下轨，弱势但可能反弹")
        
        return signals
```

### 3.3 基本面分析模块

```python
# scripts/fundamental_analyzer.py
import pandas as pd
import numpy as np

class FundamentalAnalyzer:
    def __init__(self, financial_data):
        self.data = financial_data
    
    def calculate_ratios(self):
        """计算财务比率"""
        ratios = {}
        
        # 盈利能力
        if 'net_profit' in self.data and 'revenue' in self.data:
            ratios['net_margin'] = self.data['net_profit'] / self.data['revenue'] * 100
        
        # 成长性
        if 'revenue_growth' in self.data:
            ratios['revenue_growth_rate'] = self.data['revenue_growth']
        
        # 估值
        if 'pe_ratio' in self.data:
            ratios['pe'] = self.data['pe_ratio']
        
        return ratios
    
    def dcf_valuation(self, cash_flows, discount_rate=0.1, terminal_growth=0.03):
        """DCF估值模型"""
        pv_cash_flows = 0
        for i, cf in enumerate(cash_flows):
            pv_cash_flows += cf / ((1 + discount_rate) ** (i + 1))
        
        terminal_value = cash_flows[-1] * (1 + terminal_growth) / (discount_rate - terminal_growth)
        pv_terminal = terminal_value / ((1 + discount_rate) ** len(cash_flows))
        
        total_value = pv_cash_flows + pv_terminal
        return total_value
    
    def detect_anomalies(self):
        """财务异常检测"""
        anomalies = []
        
        # 检测应收账款异常
        if 'receivables_growth' in self.data and 'revenue_growth' in self.data:
            if self.data['receivables_growth'] > self.data['revenue_growth'] * 1.5:
                anomalies.append("应收账款增速异常，可能虚增收入")
        
        # 检测现金流异常
        if 'net_profit' in self.data and 'operating_cash_flow' in self.data:
            if self.data['net_profit'] > 0 and self.data['operating_cash_flow'] < 0:
                anomalies.append("净利润与经营现金流背离，盈利质量存疑")
        
        return anomalies
```

### 3.4 风险评估模块

```python
# scripts/risk_assessor.py
class RiskAssessor:
    def __init__(self, technical_signals, fundamental_ratios, anomalies):
        self.technical = technical_signals
        self.fundamental = fundamental_ratios
        self.anomalies = anomalies
    
    def assess_risk_level(self):
        """评估风险等级"""
        risk_score = 0
        
        # 技术面风险
        if "RSI超买" in self.technical:
            risk_score += 2
        if "MACD死叉" in self.technical:
            risk_score += 1
        
        # 基本面风险
        if 'pe' in self.fundamental and self.fundamental['pe'] > 50:
            risk_score += 2
        if 'net_margin' in self.fundamental and self.fundamental['net_margin'] < 5:
            risk_score += 1
        
        # 财务异常风险
        risk_score += len(self.anomalies) * 2
        
        # 确定风险等级
        if risk_score >= 5:
            return "🔴 高风险", risk_score
        elif risk_score >= 3:
            return "🟡 中风险", risk_score
        else:
            return "🟢 低风险", risk_score
    
    def generate_warnings(self):
        """生成风险警告"""
        warnings = []
        
        if self.anomalies:
            warnings.extend(self.anomalies)
        
        if 'pe' in self.fundamental and self.fundamental['pe'] > 50:
            warnings.append("市盈率过高，估值风险较大")
        
        return warnings
```

---

## 第四部分：自动化工作流

### 4.1 定时分析任务

```bash
# scripts/daily_analysis.sh
#!/bin/bash

# 每日股票分析脚本
STOCKS="600519.SH 000858.SZ 002304.SZ"
ANALYSIS_DIR="/home/jerryxu/.openclaw/stock-analysis/reports"
DATE=$(date +%Y%m%d)

mkdir -p $ANALYSIS_DIR/$DATE

for STOCK in $STOCKS; do
    echo "分析股票: $STOCK"
    
    # 1. 获取数据
    python scripts/data_fetcher_tushare.py --code $STOCK --output $ANALYSIS_DIR/$DATE/${STOCK}_data.json
    
    # 2. 技术分析
    python scripts/technical_analyzer.py --input $ANALYSIS_DIR/$DATE/${STOCK}_data.json --output $ANALYSIS_DIR/$DATE/${STOCK}_technical.json
    
    # 3. 基本面分析
    python scripts/fundamental_analyzer.py --input $ANALYSIS_DIR/$DATE/${STOCK}_data.json --output $ANALYSIS_DIR/$DATE/${STOCK}_fundamental.json
    
    # 4. 风险评估
    python scripts/risk_assessor.py --technical $ANALYSIS_DIR/$DATE/${STOCK}_technical.json --fundamental $ANALYSIS_DIR/$DATE/${STOCK}_fundamental.json --output $ANALYSIS_DIR/$DATE/${STOCK}_risk.json
    
    # 5. 生成报告
    python scripts/report_generator.py --stock $STOCK --date $DATE --output $ANALYSIS_DIR/$DATE/${STOCK}_report.md
    
    echo "完成: $STOCK"
done

# 6. 汇总报告
python scripts/summary_generator.py --date $DATE --output $ANALYSIS_DIR/$DATE/summary.md
```

### 4.2 OpenClaw Heartbeat集成

```bash
# HEARTBEAT.md配置
# 每日股票分析任务
0 9 * * * /home/jerryxu/.openclaw/stock-analysis/scripts/daily_analysis.sh >> /tmp/stock-analysis.log 2>&1

# 实时监控任务（每30分钟）
*/30 * * * * /home/jerryxu/.openclaw/stock-analysis/scripts/monitor_alerts.sh >> /tmp/stock-monitor.log 2>&1
```

### 4.3 实时监控与预警

```python
# scripts/monitor_alerts.py
import time
import json
from datetime import datetime

class StockMonitor:
    def __init__(self, alert_thresholds):
        self.thresholds = alert_thresholds
        self.alerts = []
    
    def monitor_price(self, symbol, current_price, historical_data):
        """监控价格异常"""
        avg_price = historical_data['close'].mean()
        std_price = historical_data['close'].std()
        
        if abs(current_price - avg_price) > 2 * std_price:
            self.alerts.append(f"{symbol} 价格异常波动: {current_price} (平均: {avg_price:.2f})")
    
    def monitor_volume(self, symbol, current_volume, avg_volume):
        """监控成交量异常"""
        if current_volume > avg_volume * 3:
            self.alerts.append(f"{symbol} 成交量异常放大: {current_volume} (平均: {avg_volume:.0f})")
    
    def send_alerts(self):
        """发送预警"""
        if self.alerts:
            alert_message = "股票监控预警:\n" + "\n".join(self.alerts)
            # 发送到飞书/Telegram
            self.send_to_feishu(alert_message)
            self.send_to_telegram(alert_message)
            
    def send_to_feishu(self, message):
        """发送到飞书"""
        # 飞书Webhook集成
        pass
    
    def send_to_telegram(self, message):
        """发送到Telegram"""
        # Telegram Bot集成
        pass
```

---

## 第五部分：报告生成与可视化

### 5.1 自动报告生成

```python
# scripts/report_generator.py
import json
from datetime import datetime

class ReportGenerator:
    def __init__(self, stock_data, technical_analysis, fundamental_analysis, risk_assessment):
        self.stock = stock_data
        self.technical = technical_analysis
        self.fundamental = fundamental_analysis
        self.risk = risk_assessment
        self.date = datetime.now().strftime("%Y-%m-%d")
    
    def generate_markdown_report(self):
        """生成Markdown格式报告"""
        report = f"""# 股票分析报告 - {self.stock['name']} ({self.stock['code']})

**报告日期**: {self.date}
**分析工具**: OpenClaw智能股票分析系统

## 执行摘要

### 投资建议
- **综合评分**: {self.risk.get('score', 'N/A')}/100
- **风险等级**: {self.risk.get('level', 'N/A')}
- **操作建议**: {self.get_recommendation()}

### 关键指标
| 指标 | 数值 | 行业平均 | 状态 |
|------|------|---------|------|
| 当前价格 | ¥{self.stock.get('price', 'N/A')} | - | - |
| 市盈率(PE) | {self.fundamental.get('pe', 'N/A')} | {self.fundamental.get('industry_pe', 'N/A')} | {self.get_pe_status()} |
| 市净率(PB) | {self.fundamental.get('pb', 'N/A')} | {self.fundamental.get('industry_pb', 'N/A')} | {self.get_pb_status()} |
| ROE | {self.fundamental.get('roe', 'N/A')}% | {self.fundamental.get('industry_roe', 'N/A')}% | {self.get_roe_status()} |
| 股息率 | {self.fundamental.get('dividend_yield', 'N/A')}% | {self.fundamental.get('industry_dividend', 'N/A')}% | {self.get_dividend_status()} |

## 技术分析

### 技术指标状态
{self.generate_technical_summary()}

### 交易信号
{self.generate_trading_signals()}

## 基本面分析

### 财务健康度
{self.generate_financial_health()}

### 成长性分析
{self.generate_growth_analysis()}

### 估值分析
{self.generate_valuation_analysis()}

## 风险评估

### 风险提示
{self.generate_risk_warnings()}

### 财务异常检测
{self.generate_anomaly_detection()}

## 投资结论

### 优势
{self.generate_strengths()}

### 风险
{self.generate_risks()}

### 操作建议
1. **短期操作**: {self.get_short_term_advice()}
2. **中期策略**: {self.get_mid_term_advice()}
3. **长期投资**: {self.get_long_term_advice()}

## 免责声明
本报告由OpenClaw智能分析系统自动生成，仅供参考，不构成投资建议。投资有风险，入市需谨慎。
"""
        return report
    
    def generate_word_report(self):
        """生成Word格式报告（使用python-docx）"""
        # 这里可以扩展为生成Word文档
        pass
    
    def generate_pdf_report(self):
        """生成PDF格式报告"""
        # 这里可以扩展为生成PDF文档
        pass

### 5.2 数据可视化

```python
# scripts/visualization.py
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class StockVisualizer:
    def __init__(self, data):
        self.data = data
        plt.style.use('seaborn-v0_8-darkgrid')
    
    def plot_price_chart(self, save_path=None):
        """绘制价格图表"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # 价格走势
        axes[0, 0].plot(self.data['date'], self.data['close'], label='收盘价', color='blue')
        axes[0, 0].plot(self.data['date'], self.data['ma5'], label='5日均线', color='orange', alpha=0.7)
        axes[0, 0].plot(self.data['date'], self.data['ma20'], label='20日均线', color='green', alpha=0.7)
        axes[0, 0].set_title('价格走势与均线')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # 成交量
        axes[0, 1].bar(self.data['date'], self.data['volume'], color='gray', alpha=0.7)
        axes[0, 1].set_title('成交量')
        axes[0, 1].grid(True, alpha=0.3)
        
        # RSI指标
        axes[1, 0].plot(self.data['date'], self.data['rsi'], label='RSI', color='purple')
        axes[1, 0].axhline(y=70, color='red', linestyle='--', alpha=0.5, label='超买线')
        axes[1, 0].axhline(y=30, color='green', linestyle='--', alpha=0.5, label='超卖线')
        axes[1, 0].set_title('RSI指标')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        
        # MACD指标
        axes[1, 1].plot(self.data['date'], self.data['macd'], label='MACD', color='blue')
        axes[1, 1].plot(self.data['date'], self.data['macd_signal'], label='信号线', color='red')
        axes[1, 1].bar(self.data['date'], self.data['macd_hist'], label='柱状图', color='gray', alpha=0.5)
        axes[1, 1].set_title('MACD指标')
        axes[1, 1].legend()
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def plot_financial_ratios(self, save_path=None):
        """绘制财务比率图表"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # 盈利能力趋势
        axes[0, 0].plot(self.data['year'], self.data['net_margin'], marker='o', label='净利率')
        axes[0, 0].plot(self.data['year'], self.data['gross_margin'], marker='s', label='毛利率')
        axes[0, 0].set_title('盈利能力趋势')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # 成长性指标
        axes[0, 1].bar(self.data['year'], self.data['revenue_growth'], label='营收增长率')
        axes[0, 1].bar(self.data['year'], self.data['profit_growth'], label='净利润增长率', alpha=0.7)
        axes[0, 1].set_title('成长性指标')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)
        
        # 财务安全指标
        axes[1, 0].plot(self.data['year'], self.data['debt_ratio'], marker='o', label='资产负债率')
        axes[1, 0].plot(self.data['year'], self.data['current_ratio'], marker='s', label='流动比率')
        axes[1, 0].set_title('财务安全指标')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        
        # 估值指标
        axes[1, 1].plot(self.data['year'], self.data['pe_ratio'], marker='o', label='市盈率')
        axes[1, 1].plot(self.data['year'], self.data['pb_ratio'], marker='s', label='市净率')
        axes[1, 1].set_title('估值指标')
        axes[1, 1].legend()
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
```

### 5.3 报告模板系统

```python
# templates/report_template.md
# 股票分析报告模板

## 报告信息
- **股票名称**: {{stock_name}}
- **股票代码**: {{stock_code}}
- **报告日期**: {{report_date}}
- **分析周期**: {{analysis_period}}

## 核心结论
{{summary}}

## 详细分析

### 技术分析
{{technical_analysis}}

### 基本面分析
{{fundamental_analysis}}

### 风险评估
{{risk_assessment}}

## 投资建议
{{investment_advice}}

## 附录
{{appendix}}
```

---

## 第六部分：OpenClaw集成与自动化

### 6.1 OpenClaw技能封装

```python
# openclaw_skill.py
import subprocess
import json
import os

class StockAnalysisSkill:
    def __init__(self, config_path="~/.openclaw/stock-analysis/config.json"):
        self.config = self.load_config(config_path)
    
    def load_config(self, path):
        """加载配置"""
        with open(os.path.expanduser(path), 'r') as f:
            return json.load(f)
    
    def analyze_stock(self, stock_code, analysis_type="full"):
        """分析股票"""
        # 调用tushare技能
        tushare_result = self.call_tushare_skill(stock_code)
        
        # 调用akshare技能
        akshare_result = self.call_akshare_skill(stock_code)
        
        # 整合分析结果
        combined_result = self.combine_results(tushare_result, akshare_result)
        
        # 生成报告
        report = self.generate_report(combined_result)
        
        return report
    
    def call_tushare_skill(self, stock_code):
        """调用tushare技能"""
        cmd = [
            "python", "scripts/tushare_stock.py",
            "analyze",
            "--text", f"分析{stock_code}的估值、财务质量和趋势"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        return json.loads(result.stdout)
    
    def call_akshare_skill(self, stock_code):
        """调用akshare技能"""
        cmd = [
            "python", "scripts/stock_analyzer.py",
            stock_code
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        return json.loads(result.stdout)
    
    def combine_results(self, tushare_data, akshare_data):
        """整合分析结果"""
        combined = {
            "technical": tushare_data.get("technical", {}),
            "fundamental": {
                **tushare_data.get("fundamental", {}),
                **akshare_data.get("fundamental", {})
            },
            "valuation": tushare_data.get("valuation", {}),
            "risk": akshare_data.get("risk", {})
        }
        return combined
    
    def generate_report(self, data):
        """生成报告"""
        # 使用报告生成器
        from scripts.report_generator import ReportGenerator
        
        generator = ReportGenerator(
            stock_data=data.get("basic", {}),
            technical_analysis=data.get("technical", {}),
            fundamental_analysis=data.get("fundamental", {}),
            risk_assessment=data.get("risk", {})
        )
        
        return generator.generate_markdown_report()
```

### 6.2 自然语言接口

```python
# nlp_interface.py
import re

class StockNLPInterface:
    def __init__(self, skill):
        self.skill = skill
    
    def process_query(self, query):
        """处理自然语言查询"""
        # 提取股票代码
        stock_code = self.extract_stock_code(query)
        
        # 确定分析类型
        analysis_type = self.determine_analysis_type(query)
        
        # 执行分析
        result = self.skill.analyze_stock(stock_code, analysis_type)
        
        return result
    
    def extract_stock_code(self, query):
        """从查询中提取股票代码"""
        # 匹配A股代码模式：6位数字 + .SH/.SZ
        pattern = r'(\d{6})\.(SH|SZ)'
        match = re.search(pattern, query)
        
        if match:
            return f"{match.group(1)}.{match.group(2)}"
        
        # 匹配纯数字代码
        pattern = r'(\d{6})'
        match = re.search(pattern, query)
        
        if match:
            # 默认上海交易所
            return f"{match.group(1)}.SH"
        
        # 匹配股票名称
        stock_names = {
            "贵州茅台": "600519.SH",
            "五粮液": "000858.SZ",
            "招商银行": "600036.SH",
            "中国平安": "601318.SH",
            "宁德时代": "300750.SZ"
        }
        
        for name, code in stock_names.items():
            if name in query:
                return code
        
        return None
    
    def determine_analysis_type(self, query):
        """确定分析类型"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ["技术", "指标", "k线", "均线"]):
            return "technical"
        elif any(word in query_lower for word in ["财务", "估值", "pe", "roe"]):
            return "fundamental"
        elif any(word in query_lower for word in ["风险", "安全", "预警"]):
            return "risk"
        else:
            return "full"
```

### 6.3 OpenClaw命令集成

```bash
# 创建OpenClaw命令别名
alias stock-analyze="python ~/.openclaw/stock-analysis/openclaw_skill.py analyze"
alias stock-monitor="python ~/.openclaw/stock-analysis/scripts/monitor_alerts.py"
alias stock-report="python ~/.openclaw/stock-analysis/scripts/report_generator.py"

# OpenClaw配置文件添加技能
cat >> ~/.openclaw/openclaw.json << 'EOF'
{
  "commands": {
    "stock": {
      "analyze": "分析股票",
      "monitor": "监控股票",
      "report": "生成报告"
    }
  }
}
EOF
```

---

## 第七部分：实战应用案例

### 7.1 案例：每日投资晨报系统

#### 系统功能
1. **自动数据收集**：每日开盘前收集关注的股票数据
2. **智能分析**：技术面+基本面综合分析
3. **风险预警**：自动检测异常信号
4. **报告生成**：生成每日投资晨报
5. **自动推送**：通过飞书/Telegram推送报告

#### 实现代码
```bash
# scripts/daily_morning_report.sh
#!/bin/bash

# 配置
STOCK_LIST="600519.SH 000858.SZ 002304.SZ 600036.SH 601318.SH"
REPORT_DIR="/home/jerryxu/.openclaw/stock-analysis/reports/daily"
DATE=$(date +%Y%m%d)

echo "开始生成每日投资晨报: $DATE"

# 1. 创建报告目录
mkdir -p $REPORT_DIR/$DATE

# 2. 分析每只股票
for STOCK in $STOCK_LIST; do
    echo "分析: $STOCK"
    python openclaw_skill.py analyze --stock $STOCK --output $REPORT_DIR/$DATE/${STOCK}_analysis.json
done

# 3. 生成汇总报告
python scripts/summary_generator.py --date $DATE --dir $REPORT_DIR/$DATE --output $REPORT_DIR/$DATE/morning_report.md

# 4. 转换为Word格式
pandoc $REPORT_DIR/$DATE/morning_report.md -o $REPORT_DIR/$DATE/morning_report.docx

# 5. 发送到飞书
python scripts/feishu_sender.py --file $REPORT_DIR/$DATE/morning_report.md --title "每日投资晨报 $DATE"

echo "每日投资晨报生成完成"
```

#### 定时任务配置
```bash
# crontab配置
# 每个交易日早上8:30生成晨报
30 8 * * 1-5 /home/jerryxu/.openclaw/stock-analysis/scripts/daily_morning_report.sh >> /tmp/morning_report.log 2>&1
```

### 7.2 案例：智能选股系统

#### 系统功能
1. **条件筛选**：按估值、成长性、盈利能力等条件筛选
2. **综合评分**：对筛选出的股票进行综合评分
3. **投资组合建议**：生成投资组合建议
4. **风险分散**：考虑行业分散和风险控制

#### 实现代码
```python
# scripts/stock_screener_system.py
import pandas as pd
import numpy as np

class IntelligentStockScreener:
    def __init__(self, criteria):
        self.criteria = criteria
    
    def screen_stocks(self, stock_universe):
        """筛选股票"""
        screened_stocks = []
        
        for stock in stock_universe:
            score = self.evaluate_stock(stock)
            if score >= self.criteria['min_score']:
                screened_stocks.append({
                    'code': stock['code'],
                    'name': stock['name'],
                    'score': score,
                    'details': self.get_evaluation_details(stock)
                })
        
        # 按评分排序
        screened_stocks.sort(key=lambda x: x['score'], reverse=True)
        
        return screened_stocks[:self.criteria.get('max_results', 10)]
    
    def evaluate_stock(self, stock):
        """评估股票"""
        score = 0
        
        # 估值评分（越低越好）
        if stock['pe'] < 20:
            score += 30
        elif stock['pe'] < 30:
            score += 20
        elif stock['pe'] < 40:
            score += 10
        
        # 盈利能力评分
        if stock['roe'] > 20:
            score += 25
        elif stock['roe'] > 15:
            score += 15
        elif stock['roe'] > 10:
            score += 5
        
        # 成长性评分
        if stock['revenue_growth'] > 20:
            score += 25
        elif stock['revenue_growth'] > 10:
            score += 15
        elif stock['revenue_growth'] > 0:
            score += 5
        
        # 财务安全评分
        if stock['debt_ratio'] < 40:
            score += 10
        elif stock['debt_ratio'] < 60:
            score += 5
        
        # 股息评分
        if stock['dividend_yield'] > 3:
            score += 10
        elif stock['dividend_yield'] > 2:
            score += 5
        
        return score
    
    def generate_portfolio(self, screened_stocks, capital=100000):
        """生成投资组合"""
        portfolio = []
        total_score = sum(stock['score'] for stock in screened_stocks)
        
        for stock in screened_stocks:
            weight = stock['score'] / total_score
            allocation = capital * weight
            
            portfolio.append({
                'code': stock['code'],
                'name': stock['name'],
                'score': stock['score'],
                'weight': f"{weight*100:.1f}%",
                'allocation': f"¥{allocation:,.0f}",
                'shares': int(allocation / stock['price'])
            })
        
        return portfolio

### 7.3 案例：风险监控与预警系统

#### 系统功能
1. **实时监控**：监控持仓股票的价格和成交量
2. **异常检测**：自动检测异常波动
3. **风险预警**：及时发送风险预警
4. **自动止损**：达到止损条件自动提示

#### 实现代码
```python
# scripts/risk_monitoring_system.py
import time
import threading
from datetime import datetime, timedelta

class RiskMonitoringSystem:
    def __init__(self, watchlist, alert_channels):
        self.watchlist = watchlist
        self.alert_channels = alert_channels
        self.monitoring = False
        self.alerts_sent = {}
    
    def start_monitoring(self, interval=300):  # 5分钟间隔
        """启动监控"""
        self.monitoring = True
        print(f"风险监控系统启动，监控间隔: {interval}秒")
        
        while self.monitoring:
            for stock in self.watchlist:
                self.check_stock_risk(stock)
            
            time.sleep(interval)
    
    def check_stock_risk(self, stock):
        """检查股票风险"""
        # 获取实时数据
        current_data = self.get_realtime_data(stock['code'])
        
        # 检查价格异常
        if self.check_price_anomaly(stock, current_data):
            self.send_alert(stock, "价格异常波动", current_data)
        
        # 检查成交量异常
        if self.check_volume_anomaly(stock, current_data):
            self.send_alert(stock, "成交量异常放大", current_data)
        
        # 检查技术指标风险
        if self.check_technical_risk(stock, current_data):
            self.send_alert(stock, "技术指标风险", current_data)
        
        # 检查止损条件
        if self.check_stop_loss(stock, current_data):
            self.send_alert(stock, "达到止损条件", current_data)
    
    def send_alert(self, stock, alert_type, data):
        """发送预警"""
        alert_key = f"{stock['code']}_{alert_type}_{datetime.now().strftime('%Y%m%d')}"
        
        # 避免重复发送相同预警
        if alert_key in self.alerts_sent:
            return
        
        alert_message = f"""
🚨 风险预警: {stock['name']} ({stock['code']})
📊 预警类型: {alert_type}
💰 当前价格: ¥{data['price']}
📈 涨跌幅: {data['change_percent']}%
📊 成交量: {data['volume']}
⏰ 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        # 发送到所有配置的渠道
        for channel in self.alert_channels:
            if channel['type'] == 'feishu':
                self.send_to_feishu(channel['webhook'], alert_message)
            elif channel['type'] == 'telegram':
                self.send_to_telegram(channel['bot_token'], channel['chat_id'], alert_message)
        
        self.alerts_sent[alert_key] = datetime.now()
```

---

## 第八部分：课程整合方案

### 8.1 适合的课程模块

#### 1. 第9课：文档处理 - 办公自动化
- **应用**：自动生成股票分析报告（Word/PDF格式）
- **案例**：每日投资晨报自动生成系统

#### 2. 第8课：自动化工作流
- **应用**：定时股票分析任务
- **案例**：每日/每周自动化分析工作流

#### 3. 第15课：AI驱动的工作助手
- **应用**：智能投资分析助手
- **案例**：自然语言股票查询系统

#### 4. 第14课：个人知识管理系统
- **应用**：投资决策知识库
- **案例**：股票分析结果归档和检索系统

#### 5. 实战项目课程
- **应用**：完整的智能投资分析系统
- **案例**：从数据获取到报告生成的完整解决方案

### 8.2 教学大纲设计

#### 模块1：基础篇（2课时）
1. 股票分析基础概念
2. 数据源介绍：Tushare vs Akshare
3. 环境配置与技能安装
4. 基础数据获取实践

#### 模块2：技术分析篇（3课时）
1. 技术指标原理与应用
2. Python技术分析库使用
3. 交易信号生成
4. 技术分析实战案例

#### 模块3：基本面分析篇（3课时）
1. 财务报表分析基础
2. 财务比率计算与分析
3. 估值模型应用
4. 财务异常检测

#### 模块4：系统集成篇（3课时）
1. OpenClaw技能封装
2. 自动化工作流设计
3. 报告生成与可视化
4. 风险监控系统

#### 模块5：实战项目篇（4课时）
1. 每日投资晨报系统
2. 智能选股系统
3. 风险监控预警系统
4. 完整系统集成与部署

### 8.3 课程作业设计

#### 基础作业
1. 配置股票分析环境
2. 获取并分析一只股票的基本数据
3. 生成简单的分析报告

#### 进阶作业
1. 构建自动化分析脚本
2. 实现多股票对比分析
3. 开发风险预警功能

#### 高级作业
1. 构建完整的智能分析系统
2. 集成自然语言查询接口
3. 部署生产环境并优化性能

### 8.4 考核标准

#### 知识掌握（40%）
- 股票分析基本概念理解
- 技术指标和财务比率掌握
- 数据获取和处理能力

#### 技能应用（40%）
- Python编程能力
- 系统设计和实现能力
- 问题解决和调试能力

#### 创新实践（20%）
- 系统优化和创新功能
- 用户体验改进
- 实际应用价值

---

## 第九部分：安全与合规

### 9.1 数据安全

#### API密钥管理
```python
# 安全存储API密钥
import os
from cryptography.fernet import Fernet

class SecureConfig:
    def __init__(self, key_file="~/.openclaw/keys/encryption.key"):
        self.key = self.load_or_generate_key(key_file)
        self.cipher = Fernet(self.key)
    
    def encrypt_token(self, token):
        """加密Token"""
        return self.cipher.encrypt(token.encode()).decode()
    
    def decrypt_token(self, encrypted_token):
        """解密Token"""
        return self.cipher.decrypt(encrypted_token.encode()).decode()
```

#### 数据访问控制
- 限制数据访问频率
- 实现请求限流
- 监控异常访问模式

### 9.2 合规要求

#### 投资建议免责
所有分析报告必须包含免责声明：
```
免责声明：本报告由自动化系统生成，仅供参考，不构成投资建议。
投资者应独立判断，自行承担投资风险。
```

#### 数据使用合规
- 遵守Tushare/Akshare数据使用协议
- 不传播未公开信息
- 不进行市场操纵

#### 用户隐私保护
- 不存储用户敏感信息
- 加密存储用户配置
- 定期清理临时数据

### 9.3 风险控制

#### 系统风险
- 实现故障恢复机制
- 定期备份配置和数据
- 监控系统运行状态

#### 操作风险
- 设置操作确认机制
- 实现操作日志记录
- 提供撤销操作功能

#### 市场风险
- 强调投资风险教育
- 提供风险提示功能
- 设置风险控制参数

---

## 第十部分：总结与展望

### 10.1 案例价值总结

#### 技术价值
1. **数据整合能力**：展示OpenClaw整合多数据源的能力
2. **分析自动化**：实现复杂的股票分析流程自动化
3. **智能决策支持**：提供基于数据的投资决策支持
4. **系统集成**：展示完整的系统设计和实现能力

#### 教学价值
1. **实战导向**：基于真实需求的完整案例
2. **循序渐进**：从基础到高级的完整学习路径
3. **技能全面**：覆盖数据分析、系统开发、自动化部署
4. **行业相关**：紧密结合金融科技发展趋势

#### 商业价值
1. **个人投资者**：提供专业的投资分析工具
2. **金融机构**：可作为内部分析系统原型
3. **教育机构**：优秀的金融科技教学案例
4. **开发者**：展示OpenClaw的商业应用潜力

### 10.2 技术发展趋势

#### 短期发展（1年内）
1. **数据源扩展**：集成更多数据源（港股、美股）
2. **分析模型优化**：引入机器学习模型
3. **用户体验提升**：更好的交互界面和可视化

#### 中期发展（1-3年）
1. **实时分析能力**：实现秒级数据分析和预警
2. **个性化服务**：基于用户风险偏好的个性化分析
3. **生态整合**：与交易系统、资讯系统深度整合

#### 长期发展（3-5年）
1. **AI驱动决策**：完全由AI驱动的投资决策系统
2. **区块链集成**：基于区块链的投资记录和验证
3. **全球化服务**：支持全球主要市场的分析服务

### 10.3 课程发展建议

#### 内容扩展
1. **专题深化**：增加量化交易、期权分析等专题
2. **案例丰富**：增加更多行业和场景的案例
3. **工具完善**：开发更多教学辅助工具

#### 形式创新
1. **互动学习**：增加交互式学习环节
2. **实战竞赛**：组织股票分析实战竞赛
3. **社区建设**：建立学员交流和分享社区

#### 服务升级
1. **个性化指导**：提供一对一的学习指导
2. **就业支持**：提供金融科技就业指导
3. **持续更新**：定期更新课程内容和案例

### 10.4 结语

智能股票分析系统案例展示了OpenClaw在金融科技领域的强大应用潜力。通过整合专业的股票分析skills，我们可以构建从数据获取到决策支持的完整自动化系统。

这个案例不仅具有教学价值，更具有实际应用价值。学员通过学习这个案例，可以掌握：

1. **金融数据分析**：理解股票市场数据结构和分析方法
2. **系统开发能力**：掌握完整的系统设计和开发流程
3. **自动化技术**：学习如何实现复杂流程的自动化
4. **风险控制意识**：培养金融风险识别和控制能力

随着AI技术的不断发展，智能投资分析将成为金融科技的重要方向。OpenClaw作为强大的AI助手平台，为这一领域的发展提供了有力的技术支撑。

**案例口号**：让AI成为你的智能投资顾问，让数据驱动你的投资决策！

---

**案例完成时间**：2026-03-10  
**案例适用课程**：第8、9、14、15课及实战项目课程  
**案例难度等级**：⭐⭐⭐⭐  
**预计学习时间**：15-20小时  
**配套资源**：完整代码库、配置文件、教学视频、练习题库
