# 第9课：文档处理 - 办公自动化

## 课程目标
- 掌握PDF处理技巧
- 实现Word文档自动化
- 学会Excel数据分析
- 集成飞书文档系统

---

## 第一部分：PDF处理实战（40分钟）

### 1.1 PDF Skill安装

```bash
openclaw skills install pdf
```

### 1.2 基础操作

#### 读取PDF
```
You: 读取 report.pdf 的内容

Agent: [使用pdf skill]
这份报告包含以下内容：

# 2026年度报告

## 执行摘要
本年度公司营收增长25%...

## 市场分析
市场规模达到...

## 财务数据
...
```

#### 提取文本
```
You: 提取 document.pdf 的所有文本并保存

Agent: [提取文本]
✅ 已提取并保存到 document.txt

文件信息：
- 页数：15页
- 字数：约8,500字
- 大小：2.3MB
```

#### 提取表格
```
You: 提取 data.pdf 中的表格

Agent: [提取表格]
找到3个表格：

表格1（第3页）：
| 产品 | 销量 | 收入 |
|------|------|------|
| A | 1000 | ¥50,000 |
| B | 800 | ¥40,000 |

表格2（第5页）：
...

已保存为Excel：data-tables.xlsx
```

### 1.3 PDF合并与拆分

#### 合并PDF
```
You: 把这些PDF合并成一个：
- part1.pdf
- part2.pdf
- part3.pdf

Agent: [合并PDF]
✅ 已合并为 complete.pdf

文件信息：
- part1.pdf: 10页
- part2.pdf: 15页
- part3.pdf: 8页
- 总计: 33页
- 大小: 5.2MB
```

#### 拆分PDF
```
You: 把 document.pdf 拆分：
- 第1-5页 → intro.pdf
- 第6-15页 → content.pdf
- 第16-20页 → conclusion.pdf

Agent: [拆分PDF]
✅ 已拆分完成

---

## 第二部分：实战案例 - 智能股票分析报告自动化生成（45分钟）

### 2.1 案例背景

#### 业务需求
在智能股票分析系统中，需要将分析结果自动生成为专业的投资报告，包括：
1. **每日投资晨报**：Markdown格式，包含技术分析和基本面分析
2. **周度总结报告**：Word格式，包含详细分析和图表
3. **月度投资报告**：PDF格式，专业排版和打印版本
4. **可视化图表**：PNG/JPEG格式，用于演示和分享

#### 传统方式的问题
- 手动编写报告耗时耗力
- 格式不统一，质量参差不齐
- 图表需要手动制作和更新
- 难以实现批量生成和分发

#### OpenClaw解决方案
通过文档处理技能实现：
- 自动生成Markdown分析报告
- 转换为Word/PDF专业格式
- 自动插入图表和数据表格
- 批量生成和分发

### 2.2 报告生成系统架构

```
智能股票分析报告系统
├── 数据输入层
│   ├── 股票分析结果（JSON格式）
│   ├── 技术指标数据
│   └── 财务数据
├── 报告生成层
│   ├── Markdown报告生成器
│   ├── Word文档生成器
│   ├── PDF文档生成器
│   └── 图表生成器
├── 模板管理层
│   ├── 报告模板库
│   ├── 样式配置文件
│   └── 图表模板
├── 输出管理层
│   ├── 格式转换
│   ├── 质量检查
│   └── 版本控制
└── 分发集成层
    ├── 飞书文档集成
    ├── 邮件发送
    └── 文件存储
```

### 2.3 Markdown报告生成

#### 基础报告模板
```markdown
# {{report_title}}

**报告日期**: {{report_date}}
**生成时间**: {{generation_time}}
**分析工具**: OpenClaw智能股票分析系统

## 执行摘要

### 市场概况
{{market_summary}}

### 投资建议
{{investment_advice}}

## 个股分析

{% for stock in stocks %}
### {{stock.name}} ({{stock.code}})

#### 技术分析
{{stock.technical_analysis}}

#### 基本面分析
{{stock.fundamental_analysis}}

#### 风险评估
{{stock.risk_assessment}}

#### 操作建议
{{stock.recommendation}}
{% endfor %}

## 附录

### 技术指标说明
{{technical_indicators_explanation}}

### 免责声明
{{disclaimer}}
```

#### 模板填充实现
```python
# ~/.openclaw/workspace/scripts/report_template_filler.py
import json
from datetime import datetime
from jinja2 import Template

class ReportGenerator:
    def __init__(self, template_path):
        with open(template_path, 'r', encoding='utf-8') as f:
            self.template = Template(f.read())
    
    def generate_report(self, analysis_data, report_type="daily"):
        """生成报告"""
        context = {
            'report_title': self.get_report_title(report_type),
            'report_date': datetime.now().strftime('%Y-%m-%d'),
            'generation_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'market_summary': self.generate_market_summary(analysis_data),
            'investment_advice': self.generate_investment_advice(analysis_data),
            'stocks': self.prepare_stock_data(analysis_data),
            'technical_indicators_explanation': self.get_technical_explanation(),
            'disclaimer': self.get_disclaimer()
        }
        
        report_content = self.template.render(**context)
        
        # 保存报告
        filename = f"{report_type}_report_{datetime.now().strftime('%Y%m%d')}.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        return filename
```

### 2.4 Word文档生成

#### 使用python-docx生成专业报告
```python
# ~/.openclaw/workspace/scripts/word_report_generator.py
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
import matplotlib.pyplot as plt
import io

class WordReportGenerator:
    def __init__(self):
        self.document = Document()
        self.setup_styles()
    
    def setup_styles(self):
        """设置文档样式"""
        # 设置默认字体
        style = self.document.styles['Normal']
        font = style.font
        font.name = '微软雅黑'
        font.size = Pt(10.5)
    
    def add_title(self, title):
        """添加标题"""
        heading = self.document.add_heading(title, 0)
        heading.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    def add_section(self, title, level=1):
        """添加章节"""
        self.document.add_heading(title, level)
    
    def add_table(self, data, headers):
        """添加表格"""
        table = self.document.add_table(rows=1, cols=len(headers))
        table.style = 'Light Grid Accent 1'
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        
        # 添加表头
        header_cells = table.rows[0].cells
        for i, header in enumerate(headers):
            header_cells[i].text = header
            header_cells[i].paragraphs[0].runs[0].font.bold = True
        
        # 添加数据行
        for row_data in data:
            row_cells = table.add_row().cells
            for i, cell_data in enumerate(row_data):
                row_cells[i].text = str(cell_data)
    
    def add_chart(self, chart_image_path, caption=""):
        """添加图表"""
        self.document.add_picture(chart_image_path, width=Inches(6))
        if caption:
            paragraph = self.document.add_paragraph(caption)
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            paragraph.runs[0].italic = True
    
    def generate_stock_report(self, stock_data):
        """生成股票分析报告"""
        # 添加标题
        self.add_title(f"{stock_data['name']} ({stock_data['code']}) 投资分析报告")
        
        # 添加基本信息
        self.add_section("基本信息", 1)
        info_table = [
            ["股票代码", stock_data['code']],
            ["股票名称", stock_data['name']],
            ["当前价格", f"¥{stock_data['price']}"],
            ["分析日期", datetime.now().strftime('%Y-%m-%d')],
            ["分析工具", "OpenClaw智能分析系统"]
        ]
        self.add_table(info_table, ["项目", "数值"])
        
        # 添加技术分析
        self.add_section("技术分析", 1)
        self.add_section("技术指标", 2)
        
        technical_table = [
            ["RSI", f"{stock_data['rsi']:.2f}", self.get_rsi_status(stock_data['rsi'])],
            ["MACD", f"{stock_data['macd']:.4f}", stock_data['macd_signal']],
            ["布林带上轨", f"¥{stock_data['bb_upper']:.2f}", ""],
            ["布林带中轨", f"¥{stock_data['bb_middle']:.2f}", ""],
            ["布林带下轨", f"¥{stock_data['bb_lower']:.2f}", ""],
            ["5日均线", f"¥{stock_data['ma5']:.2f}", ""],
            ["20日均线", f"¥{stock_data['ma20']:.2f}", ""]
        ]
        self.add_table(technical_table, ["指标", "数值", "信号"])
        
        # 添加基本面分析
        self.add_section("基本面分析", 1)
        
        fundamental_table = [
            ["市盈率(PE)", f"{stock_data['pe']:.2f}", f"行业平均: {stock_data['industry_pe']:.2f}"],
            ["市净率(PB)", f"{stock_data['pb']:.2f}", f"行业平均: {stock_data['industry_pb']:.2f}"],
            ["净资产收益率(ROE)", f"{stock_data['roe']:.2f}%", f"行业平均: {stock_data['industry_roe']:.2f}%"],
            ["股息率", f"{stock_data['dividend_yield']:.2f}%", f"行业平均: {stock_data['industry_dividend']:.2f}%"],
            ["营收增长率", f"{stock_data['revenue_growth']:.2f}%", ""],
            ["净利润增长率", f"{stock_data['profit_growth']:.2f}%", ""]
        ]
        self.add_table(fundamental_table, ["财务指标", "数值", "对比"])
        
        # 添加风险评估
        self.add_section("风险评估", 1)
        
        risk_table = [
            ["风险等级", stock_data['risk_level'], ""],
            ["风险评分", f"{stock_data['risk_score']}/100", ""],
            ["主要风险", "\n".join(stock_data['risks'][:3]), ""],
            ["建议操作", stock_data['recommendation'], ""]
        ]
        self.add_table(risk_table, ["项目", "内容", "备注"])
        
        # 添加图表
        self.add_section("技术图表", 1)
        
        # 生成并添加价格走势图
        price_chart_path = self.generate_price_chart(stock_data)
        self.add_chart(price_chart_path, "价格走势与技术指标")
        
        # 添加投资建议
        self.add_section("投资建议", 1)
        self.document.add_paragraph(stock_data['detailed_recommendation'])
        
        # 添加免责声明
        self.add_section("免责声明", 1)
        self.document.add_paragraph(self.get_disclaimer())
        
        # 保存文档
        filename = f"{stock_data['code']}_analysis_{datetime.now().strftime('%Y%m%d')}.docx"
        self.document.save(filename)
        
        return filename
```

### 2.5 PDF文档生成

#### 从Word转换为PDF
```bash
# 使用LibreOffice转换
libreoffice --headless --convert-to pdf report.docx

# 使用python的pdfkit（需要wkhtmltopdf）
import pdfkit

# 从HTML转换
pdfkit.from_file('report.html', 'report.pdf')

# 从URL转换
pdfkit.from_url('http://example.com', 'report.pdf')

# 从字符串转换
pdfkit.from_string('<h1>报告标题</h1>', 'report.pdf')
```

#### 使用reportlab直接生成PDF
```python
# ~/.openclaw/workspace/scripts/pdf_report_generator.py
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

class PDFReportGenerator:
    def __init__(self, filename):
        self.doc = SimpleDocTemplate(
            filename,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
        self.story = []
    
    def setup_custom_styles(self):
        """设置自定义样式"""
        # 标题样式
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            alignment=TA_CENTER,
            spaceAfter=30
        ))
        
        # 章节标题样式
        self.styles.add(ParagraphStyle(
            name='CustomHeading1',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceBefore=12,
            spaceAfter=6
        ))
        
        # 正文样式
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=10,
            leading=14
        ))
    
    def add_title(self, title):
        """添加标题"""
        self.story.append(Paragraph(title, self.styles['CustomTitle']))
        self.story.append(Spacer(1, 0.25*inch))
    
    def add_heading(self, text, level=1):
        """添加标题"""
        if level == 1:
            self.story.append(Paragraph(text, self.styles['CustomHeading1']))
        elif level == 2:
            self.story.append(Paragraph(text, self.styles['Heading2']))
        self.story.append(Spacer(1, 0.1*inch))
    
    def add_paragraph(self, text):
        """添加段落"""
        self.story.append(Paragraph(text, self.styles['CustomBody']))
        self.story.append(Spacer(1, 0.1*inch))
    
    def add_table(self, data, col_widths=None):
        """添加表格"""
        table = Table(data, colWidths=col_widths)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        self.story.append(table)
        self.story.append(Spacer(1, 0.25*inch))
    
    def add_image(self, image_path, width=6*inch):
        """添加图片"""
        img = Image(image_path, width=width, height=3*inch)
        self.story.append(img)
        self.story.append(Spacer(1, 0.25*inch))
    
    def generate_report(self, stock_data):
        """生成PDF报告"""
        # 添加标题
        self.add_title(f"{stock_data['name']} ({stock_data['code']}) 投资分析报告")
        
        # 添加基本信息
        self.add_heading("基本信息", 1)
        info_data = [
            ['项目', '内容'],
            ['股票代码', stock_data['code']],
            ['股票名称', stock_data['name']],
            ['当前价格', f"¥{stock_data['price']}"],
            ['分析日期', datetime.now().strftime('%Y-%m-%d')]
        ]
        self.add_table(info_data, [2*inch, 4*inch])
        
        # 添加技术分析
        self.add_heading("技术分析", 1)
        self.add_paragraph("以下是该股票的技术指标分析：")
        
        tech_data = [
            ['技术指标', '数值', '状态'],
            ['RSI', f"{stock_data['rsi']:.2f}", self.get_rsi_status(stock_data['rsi'])],
            ['MACD', f"{stock_data['macd']:.4f}", stock_data['macd_signal']],
            ['布林带位置', self.get_bollinger_position(stock_data), ''],
            ['5日均线', f"¥{stock_data['ma5']:.2f}", ''],
            ['20日均线', f"¥{stock_data['ma20']:.2f}", '']
        ]
        self.add_table(tech_data, [1.5*inch, 1.5*inch, 3*inch])
        
        # 添加基本面分析
        self.add_heading("基本面分析", 1)
        
        fundamental_data = [
            ['财务指标', '数值', '行业对比'],
            ['市盈率(PE)', f"{stock_data['pe']:.2f}", f"行业: {stock_data['industry_pe']:.2f}"],
            ['市净率(PB)', f"{stock_data['pb']:.2f}", f"行业: {stock_data['industry_pb']:.2f}"],
            ['ROE', f"{stock_data['roe']:.2f}%", f"行业: {stock_data['industry_roe']:.2f}%"],
            ['股息率', f"{stock_data['dividend_yield']:.2f}%", f"行业: {stock_data['industry_dividend']:.2f}%"]
        ]
        self.add_table(fundamental_data, [1.5*inch, 1.5*inch, 3*inch])
        
        # 添加风险评估
        self.add_heading("风险评估", 1)
        
        risk_data = [
            ['风险维度', '评估结果', '说明'],
            ['风险等级', stock_data['risk_level'], ''],
            ['风险评分', f"{stock_data['risk_score']}/100", '分数越高风险越大'],
            ['技术风险', self.get_technical_risk(stock_data), ''],
            ['基本面风险', self.get_fundamental_risk(stock_data), ''],
            ['市场风险', self.get_market_risk(stock_data), '']
        ]
        self.add_table(risk_data, [1.5*inch, 1.5*inch, 3*inch])
        
        # 添加投资建议
        self.add_heading("投资建议", 1)
        self.add_paragraph(stock_data['detailed_recommendation'])
        
        # 添加操作策略
        self.add_heading("操作策略", 2)
        strategy_data = [
            ['时间维度', '策略', '目标'],
            ['短期(1-4周)', stock_data['short_term_strategy'], stock_data['short_term_target']],
            ['中期(1-3月)', stock_data['mid_term_strategy'], stock_data['mid_term_target']],
            ['长期(3-12月)', stock_data['long_term_strategy'], stock_data['long_term_target']]
        ]
        self.add_table(strategy_data, [1.5*inch, 3*inch, 1.5*inch])
        
        # 添加免责声明
        self.add_heading("免责声明", 1)
        self.add_paragraph(self.get_disclaimer())
        
        # 生成PDF
        self.doc.build(self.story)
        
        return self.doc.filename

### 2.6 图表生成与插入

#### 技术图表生成
```python
# ~/.openclaw/workspace/scripts/chart_generator.py
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class StockChartGenerator:
    def __init__(self, style='seaborn'):
        plt.style.use(style)
    
    def generate_price_chart(self, price_data, indicators, save_path):
        """生成价格走势图"""
        fig, axes = plt.subplots(3, 1, figsize=(12, 10), height_ratios=[3, 1, 1])
        
        # 价格走势图
        axes[0].plot(price_data['date'], price_data['close'], label='收盘价', color='blue', linewidth=2)
        axes[0].plot(price_data['date'], price_data['ma5'], label='5日均线', color='orange', alpha=0.7)
        axes[0].plot(price_data['date'], price_data['ma20'], label='20日均线', color='green', alpha=0.7)
        axes[0].fill_between(price_data['date'], indicators['bb_lower'], indicators['bb_upper'], 
                            alpha=0.2, color='gray', label='布林带')
        axes[0].set_title('价格走势与技术指标', fontsize=14, fontweight='bold')
        axes[0].legend(loc='upper left')
        axes[0].grid(True, alpha=0.3)
        
        # 成交量图
        axes[1].bar(price_data['date'], price_data['volume'], color='gray', alpha=0.7)
        axes[1].set_title('成交量', fontsize=12)
        axes[1].grid(True, alpha=0.3)
        
        # RSI图
        axes[2].plot(price_data['date'], indicators['rsi'], label='RSI', color='purple')
        axes[2].axhline(y=70, color='red', linestyle='--', alpha=0.5, label='超买线')
        axes[2].axhline(y=30, color='green', linestyle='--', alpha=0.5, label='超卖线')
        axes[2].set_title('RSI指标', fontsize=12)
        axes[2].legend(loc='upper left')
        axes[2].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return save_path
    
    def generate_financial_chart(self, financial_data, save_path):
        """生成财务分析图"""
        fig, axes = plt.subplots(2, 2, figsize=(12, 8))
        
        # 盈利能力趋势
        axes[0, 0].plot(financial_data['year'], financial_data['net_margin'], 
                       marker='o', label='净利率', color='blue')
        axes[0, 0].plot(financial_data['year'], financial_data['gross_margin'], 
                       marker='s', label='毛利率', color='green')
        axes[0, 0].set_title('盈利能力趋势', fontsize=12)
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # 成长性指标
        x = np.arange(len(financial_data['year']))
        width = 0.35
        axes[0, 1].bar(x - width/2, financial_data['revenue_growth'], width, label='营收增长率')
        axes[0, 1].bar(x + width/2, financial_data['profit_growth'], width, label='净利润增长率')
        axes[0, 1].set_xticks(x)
        axes[0, 1].set_xticklabels(financial_data['year'])
        axes[0, 1].set_title('成长性指标', fontsize=12)
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)
        
        # 财务安全指标
        axes[1, 0].plot(financial_data['year'], financial_data['debt_ratio'], 
                       marker='o', label='资产负债率', color='red')
        axes[1, 0].plot(financial_data['year'], financial_data['current_ratio'], 
                       marker='s', label='流动比率', color='orange')
        axes[1, 0].set_title('财务安全指标', fontsize=12)
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        
        # 估值指标
        axes[1, 1].plot(financial_data['year'], financial_data['pe_ratio'], 
                       marker='o', label='市盈率', color='purple')
        axes[1, 1].plot(financial_data['year'], financial_data['pb_ratio'], 
                       marker='s', label='市净率', color='brown')
        axes[1, 1].set_title('估值指标', fontsize=12)
        axes[1, 1].legend()
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return save_path
```

### 2.7 飞书文档集成

#### 自动上传到飞书文档
```python
# ~/.openclaw/workspace/scripts/feishu_integration.py
import requests
import json
from datetime import datetime

class FeishuDocumentManager:
    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token = self.get_access_token()
    
    def get_access_token(self):
        """获取飞书访问令牌"""
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        headers = {"Content-Type": "application/json; charset=utf-8"}
        data = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        
        response = requests.post(url, headers=headers, json=data)
        return response.json()['tenant_access_token']
    
    def create_document(self, title, content, folder_token=None):
        """创建飞书文档"""
        url = "https://open.feishu.cn/open-apis/docx/v1/documents"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json; charset=utf-8"
        }
        
        data = {
            "title": title,
            "folder_token": folder_token
        }
        
        response = requests.post(url, headers=headers, json=data)
        document_info = response.json()['data']['document']
        
        # 写入内容
        self.write_document_content(document_info['document_id'], content)
        
        return document_info
    
    def write_document_content(self, document_id, content):
        """写入文档内容"""
        url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{document_id}/blocks"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json; charset=utf-8"
        }
        
        # 将Markdown转换为飞书文档格式
        blocks = self.convert_markdown_to_blocks(content)
        
        data = {
            "document_id": document_id,
            "blocks": blocks
        }
        
        response = requests.patch(url, headers=headers, json=data)
        return response.json()
    
    def convert_markdown_to_blocks(self, markdown_content):
        """将Markdown转换为飞书文档块"""
        blocks = []
        lines = markdown_content.split('\n')
        
        for line in lines:
            if line.startswith('# '):
                # 一级标题
                blocks.append({
                    "block_type": 1,
                    "heading1": {
                        "elements": [{
                            "text_run": {
                                "content": line[2:],
                                "text_element_style": {
                                    "bold": True,
                                    "font_size": 24
                                }
                            }
                        }]
                    }
                })
            elif line.startswith('## '):
                # 二级标题
                blocks.append({
                    "block_type": 2,
                    "heading2": {
                        "elements": [{
                            "text_run": {
                                "content": line[3:],
                                "text_element_style": {
                                    "bold": True,
                                    "font_size": 20
                                }
                            }
                        }]
                    }
                })
            elif line.startswith('|'):
                # 表格
                table_data = self.parse_markdown_table(line)
                blocks.append({
                    "block_type": 27,
                    "table": {
                        "cells": table_data,
                        "property": {
                            "column_size": len(table_data[0]),
                            "row_size": len(table_data)
                        }
                    }
                })
            elif line.strip():
                # 普通段落
                blocks.append({
                    "block_type": 3,
                    "paragraph": {
                        "elements": [{
                            "text_run": {
                                "content": line,
                                "text_element_style": {}
                            }
                        }]
                    }
                })
        
        return blocks

#### 自动化报告上传流程
```bash
# 完整的报告生成和上传流程
1. 生成Markdown报告 → 2. 转换为Word格式 → 3. 生成PDF格式 → 4. 上传到飞书 → 5. 发送通知

# 实现脚本
python generate_markdown_report.py    # 生成Markdown报告
python convert_to_word.py             # 转换为Word
python convert_to_pdf.py              # 转换为PDF
python upload_to_feishu.py            # 上传到飞书
python send_notifications.py          # 发送通知
```

### 2.8 自动化工作流配置

#### 完整的工作流脚本
```bash
#!/bin/bash
# ~/.openclaw/workspace/scripts/full_report_workflow.sh

# 配置
STOCK_CODES="600519.SH 000858.SZ 600036.SH"
REPORT_DATE=$(date +%Y%m%d)
REPORT_DIR="/home/jerryxu/.openclaw/stock-analysis/reports/$REPORT_DATE"

echo "开始执行股票分析报告工作流: $REPORT_DATE"

# 1. 创建报告目录
mkdir -p $REPORT_DIR

# 2. 分析每只股票
for CODE in $STOCK_CODES; do
    echo "分析股票: $CODE"
    
    # 获取数据
    python scripts/data_collector.py --code $CODE --output $REPORT_DIR/${CODE}_data.json
    
    # 技术分析
    python scripts/technical_analyzer.py --input $REPORT_DIR/${CODE}_data.json --output $REPORT_DIR/${CODE}_technical.json
    
    # 基本面分析
    python scripts/fundamental_analyzer.py --input $REPORT_DIR/${CODE}_data.json --output $REPORT_DIR/${CODE}_fundamental.json
    
    # 生成图表
    python scripts/chart_generator.py --code $CODE --output $REPORT_DIR/${CODE}_charts/
done

# 3. 生成报告
echo "生成报告..."

# Markdown报告
python scripts/markdown_report_generator.py --date $REPORT_DATE --dir $REPORT_DIR --output $REPORT_DIR/daily_report.md

# Word报告
python scripts/word_report_generator.py --input $REPORT_DIR/daily_report.md --output $REPORT_DIR/daily_report.docx

# PDF报告
python scripts/pdf_report_generator.py --input $REPORT_DIR/daily_report.docx --output $REPORT_DIR/daily_report.pdf

# 4. 上传到飞书
echo "上传到飞书..."
python scripts/feishu_uploader.py --file $REPORT_DIR/daily_report.md --title "每日投资晨报 $REPORT_DATE"

# 5. 发送通知
echo "发送通知..."
python scripts/notification_sender.py --report $REPORT_DIR/daily_report.md --channels feishu,telegram,email

echo "股票分析报告工作流完成"
```

#### 定时任务配置
```bash
# crontab配置
# 每个交易日收盘后执行（15:30）
30 15 * * 1-5 /home/jerryxu/.openclaw/workspace/scripts/full_report_workflow.sh >> /tmp/stock_report.log 2>&1

# 每周五生成周报（17:00）
0 17 * * 5 /home/jerryxu/.openclaw/workspace/scripts/weekly_report_workflow.sh >> /tmp/stock_weekly.log 2>&1

# 每月最后一天生成月报（18:00）
0 18 28-31 * * [ $(date -d tomorrow +\%d) -eq 1 ] && /home/jerryxu/.openclaw/workspace/scripts/monthly_report_workflow.sh >> /tmp/stock_monthly.log 2>&1
```

### 2.9 案例总结

#### 实现效果
1. **全自动报告生成**：从数据到报告的完整自动化流程
2. **多格式支持**：Markdown、Word、PDF多种格式
3. **专业排版**：符合投资报告的专业标准
4. **集成分发**：自动上传和通知

#### 技术要点
1. **模板系统**：Jinja2模板引擎实现灵活的报告生成
2. **文档处理**：python-docx、reportlab等专业库使用
3. **图表生成**：Matplotlib生成专业图表
4. **云集成**：飞书文档API集成

#### 业务价值
1. **效率提升**：节省95%的报告编写时间
2. **质量保证**：统一格式和专业标准
3. **及时性**：实时生成和分发
4. **可追溯**：完整的版本管理和归档

---

## 第三部分：Word文档自动化（30分钟）

生成文件：
- intro.pdf (5页, 800KB)
- content.pdf (10页, 2.1MB)
- conclusion.pdf (5页, 900KB)
```

#### 提取特定页
```
You: 提取 report.pdf 的第3、7、12页

Agent: [提取页面]
✅ 已提取为 report-selected.pdf

包含页面：3, 7, 12
大小：450KB
```

### 1.4 PDF转换

#### PDF转Word
```
You: 把 document.pdf 转成Word

Agent: [转换格式]
✅ 已转换为 document.docx

保留内容：
- ✅ 文本
- ✅ 格式
- ✅ 图片
- ⚠️ 表格（可能需要调整）
```

#### PDF转图片
```
You: 把 slides.pdf 的每一页转成图片

Agent: [转换为图片]
✅ 已生成15张图片

文件列表：
- slide-01.png
- slide-02.png
- ...
- slide-15.png

保存位置：./slides/
```

### 1.5 OCR识别

#### 扫描件识别
```
You: 识别 scanned.pdf 中的文字

Agent: [使用OCR]
正在识别...

✅ 识别完成

识别结果：
这是一份扫描的合同文件...
[完整文本]

准确率：约95%
已保存为：scanned-text.txt
```

#### 图片PDF转可搜索PDF
```
You: 把 scanned.pdf 转成可搜索的PDF

Agent: [OCR + 生成PDF]
✅ 已生成 scanned-searchable.pdf

特点：
- 保留原始图片
- 添加文本层
- 可复制文本
- 可搜索内容
```

### 1.6 PDF编辑

#### 添加水印
```
You: 给 document.pdf 添加水印"机密"

Agent: [添加水印]
✅ 已添加水印

水印设置：
- 文字：机密
- 位置：居中
- 透明度：30%
- 颜色：红色

保存为：document-watermarked.pdf
```

#### 添加页码
```
You: 给 report.pdf 添加页码

Agent: [添加页码]
✅ 已添加页码

页码设置：
- 位置：页脚居中
- 格式：第X页/共Y页
- 起始页：1

保存为：report-numbered.pdf
```

#### 加密PDF
```
You: 给 confidential.pdf 加密

Agent: [加密PDF]
请设置密码：

You: password123

Agent: ✅ 已加密

加密设置：
- 打开密码：已设置
- 权限：禁止打印、复制
- 加密级别：AES-256

保存为：confidential-encrypted.pdf
```

---

## 第二部分：Word文档自动化（40分钟）

### 2.1 Word Skill安装

```bash
openclaw skills install docx
```

### 2.2 创建文档

#### 基础文档
```
You: 创建一个Word文档，内容是：
标题：项目计划
正文：本项目计划于2026年3月启动...

Agent: [创建文档]
✅ 已创建 project-plan.docx

包含：
- 标题（一级标题）
- 正文（正文样式）
```

#### 格式化文档
```
You: 创建一份格式化的报告：
- 标题：年度总结
- 副标题：2026年
- 章节：
  1. 执行摘要
  2. 业务回顾
  3. 财务分析
- 添加目录
- 添加页码

Agent: [创建文档]
✅ 已创建 annual-summary.docx

包含：
- 封面（标题+副标题）
- 目录（自动生成）
- 3个章节（一级标题）
- 页码（页脚）
```

### 2.3 简历生成

#### 自动生成简历
```
You: 帮我生成一份简历：
姓名：张三
职位：全栈工程师
邮箱：zhangsan@example.com
电话：138-0000-0000
技能：Python, JavaScript, React, Node.js, Docker
工作经历：
- ABC公司（2020-2023）高级工程师
- XYZ公司（2018-2020）工程师

Agent: [生成简历]
✅ 已生成 张三-简历.docx

包含：
- 个人信息（表格）
- 求职意向
- 技能清单（图标）
- 工作经历（时间轴）
- 教育背景
- 项目经验

使用模板：专业简洁风格
```

#### 简历优化
```
You: 优化这份简历：
- 突出技术栈
- 量化工作成果
- 添加项目亮点

Agent: [分析简历]
[优化内容]
✅ 已优化

优化内容：
1. 技能部分
   - 添加技能图标
   - 按类别分组
   - 标注熟练度

2. 工作经历
   - 量化成果（提升XX%）
   - 突出技术栈
   - 添加项目链接

3. 项目经验
   - 突出技术难点
   - 展示解决方案
   - 量化影响

保存为：张三-简历-优化版.docx
```

### 2.4 报告生成

#### 自动生成报告
```
You: 根据这些数据生成月度报告：
- 销售额：¥1,234,567
- 增长率：+15%
- 新客户：234个
- 客户满意度：92%

Agent: [生成报告]
✅ 已生成 月度报告-2026-03.docx

包含：
- 封面
- 目录
- 执行摘要
- 数据分析（图表）
- 趋势分析
- 建议措施
- 附录

页数：12页
```

#### 批量生成报告
```
You: 根据这个模板批量生成报告：
模板：monthly-report-template.docx
数据：data.xlsx（包含12个月的数据）

Agent: [批量生成]
正在生成...

✅ 已生成12份报告

文件列表：
- 月度报告-2026-01.docx
- 月度报告-2026-02.docx
- ...
- 月度报告-2026-12.docx

保存位置：./reports/
```

### 2.5 文档编辑

#### 查找替换
```
You: 在 document.docx 中：
- 把"公司A"替换为"公司B"
- 把"2025"替换为"2026"

Agent: [查找替换]
✅ 已完成

替换统计：
- "公司A" → "公司B"：15处
- "2025" → "2026"：8处

保存为：document-updated.docx
```

#### 插入内容
```
You: 在 report.docx 的第3页后插入：
- 新章节：市场分析
- 内容：[从market-analysis.txt读取]

Agent: [插入内容]
✅ 已插入

插入位置：第3页后
新增页数：2页
总页数：15页 → 17页
```

#### 格式调整
```
You: 调整 document.docx 的格式：
- 标题：黑体，18号
- 正文：宋体，12号
- 行距：1.5倍
- 页边距：2.5cm

Agent: [调整格式]
✅ 已调整

应用范围：全文
保存为：document-formatted.docx
```

---

## 第三部分：Excel数据分析（40分钟）

### 3.1 Excel Skill安装

```bash
openclaw skills install xlsx
```

### 3.2 读取数据

#### 基础读取
```
You: 读取 sales.xlsx 的数据

Agent: [读取Excel]
文件信息：
- 工作表：3个（销售数据、客户信息、产品列表）
- 总行数：1,234行
- 总列数：15列

销售数据预览：
| 日期 | 产品 | 数量 | 金额 |
|------|------|------|------|
| 2026-03-01 | A | 10 | ¥1,000 |
| 2026-03-01 | B | 5 | ¥500 |
...
```

#### 数据统计
```
You: 分析 sales.xlsx 的销售数据

Agent: [分析数据]
销售数据分析：

总体统计：
- 总销售额：¥1,234,567
- 总订单数：1,234
- 平均客单价：¥1,001
- 最高单笔：¥15,000

产品排行：
1. 产品A：¥456,789（37%）
2. 产品B：¥345,678（28%）
3. 产品C：¥234,567（19%）

时间趋势：
- 3月上旬：¥400,000
- 3月中旬：¥450,000
- 3月下旬：¥384,567
```

### 3.3 数据处理

#### 数据清洗
```
You: 清洗 data.xlsx：
- 删除空行
- 删除重复数据
- 填充缺失值
- 统一格式

Agent: [清洗数据]
✅ 清洗完成

处理统计：
- 删除空行：23行
- 删除重复：15行
- 填充缺失：8个单元格
- 格式统一：日期、金额

原始数据：1,234行
清洗后：1,196行

保存为：data-cleaned.xlsx
```

#### 数据转换
```
You: 转换 data.xlsx：
- 日期格式：YYYY-MM-DD
- 金额格式：¥X,XXX.XX
- 百分比格式：XX.XX%

Agent: [转换格式]
✅ 转换完成

转换统计：
- 日期：234个单元格
- 金额：456个单元格
- 百分比：89个单元格

保存为：data-formatted.xlsx
```

### 3.4 数据分析

#### 透视表
```
You: 创建透视表分析 sales.xlsx：
- 行：产品类别
- 列：月份
- 值：销售额（求和）

Agent: [创建透视表]
✅ 已创建

透视表预览：
| 类别 | 1月 | 2月 | 3月 | 总计 |
|------|-----|-----|-----|------|
| 电子 | ¥100K | ¥120K | ¥150K | ¥370K |
| 服装 | ¥80K | ¥90K | ¥100K | ¥270K |
| 食品 | ¥60K | ¥70K | ¥80K | ¥210K |

保存为：sales-pivot.xlsx
```

#### 图表生成
```
You: 生成销售趋势图表

Agent: [生成图表]
✅ 已生成

图表类型：
1. 折线图：月度销售趋势
2. 柱状图：产品销售对比
3. 饼图：类别占比

保存为：sales-charts.xlsx
```

### 3.5 公式计算

#### 自动计算
```
You: 在 data.xlsx 中添加计算列：
- 利润 = 收入 - 成本
- 利润率 = 利润 / 收入
- 排名 = RANK(利润)

Agent: [添加公式]
✅ 已添加

新增列：
- D列：利润（公式）
- E列：利润率（公式+百分比格式）
- F列：排名（公式）

自动计算：1,234行

保存为：data-calculated.xlsx
```

#### 条件格式
```
You: 添加条件格式：
- 利润率 > 30%：绿色
- 利润率 20-30%：黄色
- 利润率 < 20%：红色

Agent: [添加条件格式]
✅ 已添加

应用范围：E列（利润率）
规则数：3条

效果：
- 绿色：234行
- 黄色：567行
- 红色：433行
```

### 3.6 批量处理

#### 合并多个Excel
```
You: 合并这些Excel文件：
- sales-jan.xlsx
- sales-feb.xlsx
- sales-mar.xlsx

Agent: [合并文件]
✅ 已合并

合并统计：
- 文件数：3个
- 总行数：3,702行
- 工作表：按月份分组

保存为：sales-q1.xlsx
```

#### 拆分Excel
```
You: 把 data.xlsx 按类别拆分成多个文件

Agent: [拆分文件]
✅ 已拆分

生成文件：
- data-电子.xlsx（234行）
- data-服装.xlsx（456行）
- data-食品.xlsx（544行）

保存位置：./data-split/
```

---

## 第四部分：飞书文档集成（30分钟）

### 4.1 飞书文档操作

#### 读取飞书文档
```
You: 读取这个飞书文档
https://xxx.feishu.cn/docx/xxxxx

Agent: [使用feishu_doc]
文档标题：项目计划

内容：
# 项目概述
本项目旨在...

# 时间安排
- 第一阶段：...
- 第二阶段：...

# 资源分配
...
```

#### 创建飞书文档
```
You: 把这份报告发布到飞书

Agent: [创建飞书文档]
✅ 已创建

文档信息：
- 标题：月度报告-2026-03
- 链接：https://xxx.feishu.cn/docx/xxxxx
- 权限：团队可见
```

#### 更新飞书文档
```
You: 更新飞书文档，添加新章节

Agent: [更新文档]
✅ 已更新

更新内容：
- 添加章节：结论与建议
- 更新时间：2026-03-09 10:00
- 版本：v2
```

### 4.2 飞书知识库

#### 读取知识库
```
You: 读取知识库中的OpenClaw文档

Agent: [使用feishu_wiki]
找到3篇文档：

1. OpenClaw安装指南
   - 链接：https://...
   - 更新：2026-03-01

2. OpenClaw最佳实践
   - 链接：https://...
   - 更新：2026-03-05

3. OpenClaw FAQ
   - 链接：https://...
   - 更新：2026-03-08
```

#### 创建知识库文档
```
You: 在知识库中创建新文档：
标题：OpenClaw课程大纲
内容：[从course-outline.md读取]

Agent: [创建文档]
✅ 已创建

文档信息：
- 位置：技术文档/OpenClaw
- 链接：https://...
- 权限：全员可见
```

### 4.3 飞书多维表格

#### 读取多维表格
```
You: 读取这个多维表格的数据
https://xxx.feishu.cn/base/xxxxx

Agent: [使用feishu_bitable]
表格：项目管理

数据预览：
| 项目名称 | 负责人 | 状态 | 进度 |
|---------|--------|------|------|
| 项目A | 张三 | 进行中 | 80% |
| 项目B | 李四 | 已完成 | 100% |
...

总记录数：45条
```

#### 更新多维表格
```
You: 更新项目A的进度为90%

Agent: [更新记录]
✅ 已更新

更新内容：
- 记录ID：rec_xxx
- 字段：进度
- 原值：80%
- 新值：90%
```

#### 创建记录
```
You: 在多维表格中添加新项目：
- 项目名称：项目C
- 负责人：王五
- 状态：计划中
- 进度：0%

Agent: [创建记录]
✅ 已创建

记录ID：rec_yyy
表格链接：https://...
```

---

## 第五部分：实战项目（30分钟）

### 项目：自动化报告生成系统

#### 需求
1. 从Excel读取数据
2. 分析并生成图表
3. 创建Word报告
4. 发布到飞书

#### 实现

**步骤1：读取数据**
```
You: 读取 sales-data.xlsx 并分析

Agent: [读取Excel]
[分析数据]

数据概况：
- 时间范围：2026-01 ~ 2026-03
- 总销售额：¥3,456,789
- 总订单数：3,456
- 平均客单价：¥1,000

趋势分析：
- 1月：¥1,000,000
- 2月：¥1,200,000（+20%）
- 3月：¥1,256,789（+4.7%）
```

**步骤2：生成图表**
```
Agent: [生成图表]
✅ 已生成3个图表

1. 月度销售趋势（折线图）
2. 产品销售对比（柱状图）
3. 类别占比（饼图）

保存为：sales-charts.xlsx
```

**步骤3：创建Word报告**
```
Agent: [创建报告]
✅ 已生成 Q1销售报告.docx

包含：
- 封面
- 目录
- 执行摘要
- 数据分析（嵌入图表）
- 趋势分析
- 建议措施
- 附录（原始数据）

页数：15页
```

**步骤4：发布到飞书**
```
Agent: [发布到飞书]
✅ 已发布

飞书文档：
- 标题：Q1销售报告
- 链接：https://xxx.feishu.cn/docx/xxxxx
- 权限：管理层可见

同时发送通知到飞书群：
📊 Q1销售报告已发布
- 总销售额：¥3.46M（+15%）
- 查看报告：[链接]
```

---

## 第六部分：作业与练习（课后）

### 作业1：PDF处理（必做）

**任务：**
1. 合并3个PDF
2. 提取特定页面
3. 添加水印
4. 转换为Word

**提交：**
- 处理前后的文件
- 操作命令
- 处理结果截图

### 作业2：Word自动化（必做）

**任务：**
生成一份格式化的简历或报告

**要求：**
- 使用模板或自定义格式
- 包含多个章节
- 添加目录和页码
- 插入图片或表格

**提交：**
- 生成的Word文档
- 生成命令
- 效果截图

### 作业3：Excel分析（必做）

**任务：**
分析一份Excel数据

**要求：**
1. 数据清洗
2. 统计分析
3. 生成图表
4. 创建透视表

**提交：**
- 原始数据
- 处理后的数据
- 分析报告

### 作业4：综合项目（选做）

**任务：**
构建一个自动化报告系统

**要求：**
1. 从Excel读取数据
2. 分析并生成图表
3. 创建Word报告
4. 发布到飞书或邮件

**提交：**
- 完整代码/配置
- 示例数据
- 生成的报告
- 系统说明文档

---

## 第七部分：常见问题（10分钟）

### Q1：PDF转Word格式乱了？

**A1：**
```
原因：
- PDF格式复杂
- 包含特殊元素
- 转换算法限制

解决：
1. 使用OCR模式
2. 手动调整格式
3. 使用专业工具
4. 分段转换
```

### Q2：Excel公式不生效？

**A2：**
```bash
# 检查公式语法
# 确保单元格引用正确
# 检查数据类型

# 手动触发计算
openclaw chat "重新计算Excel公式"
```

### Q3：飞书文档权限不足？

**A3：**
```
检查：
1. 机器人是否添加到文档
2. 是否有编辑权限
3. 文档是否被锁定

解决：
1. 添加机器人为协作者
2. 授予编辑权限
3. 联系文档所有者
```

### Q4：批量处理很慢？

**A4：**
```
优化：
1. 减少文件数量
2. 使用批处理模式
3. 并行处理
4. 缓存中间结果

示例：
# 串行处理（慢）
for file in files:
    process(file)

# 并行处理（快）
parallel_process(files, workers=4)
```

### Q5：如何处理大文件？

**A5：**
```
策略：
1. 分块处理
2. 流式读取
3. 压缩存储
4. 云端处理

示例：
# 分块读取大Excel
for chunk in read_excel_chunks(file, chunk_size=1000):
    process(chunk)
```

---

## 第八部分：扩展阅读

### 推荐资源

#### Skills文档
- pdf：https://clawhub.com/skills/pdf
- docx：https://clawhub.com/skills/docx
- xlsx：https://clawhub.com/skills/xlsx

#### 飞书API
- 文档API：https://open.feishu.cn/document/docx
- 多维表格：https://open.feishu.cn/document/bitable

#### 工具库
- PyPDF2：https://pypdf2.readthedocs.io
- python-docx：https://python-docx.readthedocs.io
- openpyxl：https://openpyxl.readthedocs.io

### 下节课预告

**第10课：Gateway深度配置 - 稳定性与安全**
- Gateway架构
- 性能优化
- 稳定性保障
- 安全加固

---

## 课程总结

### 本节课你学到了：
✅ PDF处理技巧（合并、拆分、OCR）  
✅ Word文档自动化（生成、编辑、格式化）  
✅ Excel数据分析（清洗、统计、图表）  
✅ 飞书文档集成（读写、知识库、多维表格）  
✅ 自动化报告生成系统  

### 关键要点：
1. **PDF适合文档归档和分发**
2. **Word适合报告和简历**
3. **Excel适合数据分析**
4. **飞书适合团队协作**
5. **组合使用效果最好**

### 下一步：
1. 完成作业1-3（必做）
2. 尝试作业4（选做）
3. 探索更多文档处理技巧
4. 准备学习第10课（Gateway深度配置）

---

**恭喜完成第二阶段（进阶应用）！** 🎉

**课程反馈：**
如有问题或建议，请在GitHub提Issue或加入社区讨论。

**下节课见！** 🚀
