## 宏观投资研究工具汇总

GitHub 上围绕政策、央行动作、流动性、股债市场状态、重大事件、美债收益率、美元指数等维度的宏观投研项目调研笔记。目标场景：从宏观大方向给股市投资定调。

---

### 第一梯队：宏观全维度框架

#### Macro Shock Risk Engine

网址：<https://github.com/Josh20241995/Macro-Shocks-Portfolio-Risk-Engine>

量化机构级别的跨资产宏观冲击风控系统。检测 Fed 非交易时段讲话、周末紧急政策、地缘事件，输出 0-100 的综合风险评分。覆盖流动性、波动率、利率冲击、权益下行、信用利差、外汇、大宗商品、政策模糊度共 9 个维度。Python + C++。

#### Capital Markets Intelligence

网址：<https://github.com/DogInfantry/capital-markets-intelligence>

对标高盛 GIR/摩根大通 Country Risk 的投研平台。内置收益率曲线分解、主权风险指数(0-100)、跨资产体制检测(Risk-On/Neutral/Off)、IPO 事件研究等 6 个量化模型。零 API 密钥需求，500 天美债+外汇+VIX+黄金+原油实测数据。

#### Market Intelligence Dashboard

网址：<https://github.com/noivuduc/market-intelligence-dashboard?ref=producthunt>

自托管宏观仪表盘，覆盖 Fed 政策、Treasury 曲线体制、宏观数据惊喜度、流动性压力、权益广度、资金流、期权定位。内置 Regime Engine（政策+流动性+风险+趋势+资金流+持仓综合打分），可选 Claude AI 摘要。Node.js。

---

### 第二梯队：体制切换 / 信号系统

#### Macro Regime-Switching Model

网址：<https://github.com/oj0nathan/Macro_Regime_Switching_Model>

用 Hidden Markov Model 对美国增长和通胀建模，识别 Crisis/Stagnation/Expansion/Boom 四种宏观体制，做 5 资产(SPY/TLT/HYG/DBC/GLD) 的体制感知配置。2007-2025 回测，总回报 349% vs 等权 220%，最大回撤 -15.9% vs -24.4%。

#### Adaptive Regime Strategy (MRS)

网址：<https://github.com/gitmichaelqiu/AdaptiveRegimeStrategy>

机构级量化框架，基于 Adaptive Markets Hypothesis。用 VIX + 10 年期美债收益率变化率计算 Total Stress 分数，GMM 隐马尔可夫模型做体制分类，动态调整仓位。分方向交易(V20)和统计套利(V16)两条线。

#### Macro Signal Builder

网址：<https://github.com/gyimadu/macro-signal-builder>

GDP 增速+CPI+失业率+联邦基金利率驱动 6 种经济体制分类（Recession/Stagflation/Overheating/Expansion 等），对 SPY/TLT/GLD/UUP 输出 Buy/Sell/Hold。Flask + Chart.js，每 5 分钟自动刷新。

---

### 第三梯队：专项工具

| 项目 | 核心能力 | 链接 |
|------|---------|------|
| Macro Sentiment & Financial Indicators | M2 vs 股市、收益率曲线、密歇根消费者信心、ISM、VIX 五项独立分析，Python | <https://github.com/jurchiks33/Macro-Sentiment-and-Financial-Indicators> |
| Regime Shift Detection | FOMC 会议纪要 + 14 变量美债面板数据交叉验证体制拐点，学术论文复现代码 | <https://github.com/mingxuan-yi/regime_shift> |
| Black Swan Radar | Windows 桌面宏观监控，VIX/美债利率/美元/美联储数据常驻显示，不生成信号 | <https://github.com/cometoplay008-commits/Black-Swan-Radar-AI-Ready-Macro-Risk-Dashboard> |
| Market Intelligence MCP | MCP Server，衰退概率(15 组件模型)、行业轮动信号、CFTC 机构持仓、宏观情景级联分析 | <https://github.com/bullrundata/market-intelligence-mcp> |
| FICC Researcher | Agent 导向的固收研究(中债+美债+信用+可转债+利率衍生品)，偏向中国市场 | <https://github.com/Kevin-Zhu-11/FICC_Researcher> |

---

### 国外项目在墙内的痛点

| 痛点 | 具体表现 |
|------|----------|
| 数据断流 | FRED 偶尔抽风，Yahoo Finance 间歇性慢，Bloomberg API 需要机构账号 |
| A 股生态缺失 | 只有美股/美债/美元框架，没有 PBOC 操作、LPR、SHIBOR、北向资金、两融余额 |
| 时效性差距 | 央行报告、宏观数据发布节奏完全不同，国外项目不盯中国宏观日历 |

---

### 国内生态：三套对口方案

#### Hikyuu — 重型武器，策略资产化

网址：<https://github.com/fasiondog/hikyuu>

C++ 核心 + Python 接口，A 股量化领域最成熟的框架之一。把系统性交易拆成市场环境研判、信号指示器、风控、资金管理等独立模块。可用 "宏观环境判断 + 交易信号过滤" 搭建体系：

- 市场环境策略模块专门判断宏观冷暖
- 系统有效条件模块仅在环境偏暖时允许信号通过
- AMD 7950x 实测全市场 1913 万日 K 线计算仅 166ms

#### BAISYS QUANT — 直接有宏观门控

网址：<https://github.com/baisysquant/BAISYS_QUANT>

51 条规则、6 道门控递进评分，其中 Gate 0.5 就是宏观环境注入：

```
Gate 0:   数据质量筛查
Gate 0.5: 宏观环境注入 → 涨跌比驱动等级门槛调节
Gate 1:   入场信号共振
Gate 2:   波动率/背离风险过滤
Gate 3:   资金流修饰
Gate 4:   仓位联动
```

每天自动完成全市场 A 股复盘，数据源 AkShare（免费、国内直连），筹码分布走 AShareHub。配置文件切换短线/中线/长线风格。

#### ashare-mcp — 最轻量的宏观数据入口

网址：<https://github.com/lolifamily/ashare-mcp>

MCP Server 专给 AI Agent 用。封装货币供应量(M0/M1/M2)、存贷款利率、存款准备金率，搭配 LLM 做宏观判断。baostock 免费无需注册，装上 akshare 扩展后可拿东方财富财务报表。

---

### 场景推荐

**轻量日常盯宏观**：ashare-mcp + AkShare 脚本，拉 M2/社融/PMI/美债/美元指数/北向资金，每周产一张仪表盘。

**结合选股**：BAISYS QUANT 做全市场复盘，宏观门控过滤宏观不利时期。

**深度策略**：Hikyuu 搭建自己的市场环境模块，宏观判断作为策略系统有效性的前置条件。

**对标全球**：Capital Markets Intelligence + Macro Shock Risk Engine + Market Intelligence Dashboard 组合使用。

---

### 数据源速查

A 股相关数据源以 AkShare 为核心，覆盖社融、M2、LPR、SHIBOR、PMI、外汇储备、北向资金等指标，免费且国内直连。

---

> 调研时间：2026-07-15
