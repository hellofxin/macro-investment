# GitHub 宏观投资研究项目汇总

> 研究政策、央行动作、流动性、股市债市状态、大事件、美债收益率、美元指数等，为股市投资定大方向。

整理时间：2026-07-15

---

## 目录

- [1. 全球宏观研究项目（海外 GitHub）](#1-全球宏观研究项目海外-github)
  - [1.1 macro-signal-builder](#11-macro-signal-builder--首推)
  - [1.2 market-intelligence-dashboard](#12-market-intelligence-dashboard--专业级)
  - [1.3 Macro-AI-Dashboard](#13-macro-ai-dashboard--利率专精)
  - [1.4 Macro Shock Risk Engine](#14-macro-shock-risk-engine--事件驱动)
  - [1.5 量化宏观策略项目](#15-量化宏观策略项目)
  - [1.6 资源聚合类（Awesome Lists）](#16-资源聚合类awesome-lists)
- [2. 国内可用性分析](#2-国内可用性分析)
  - [2.1 海外项目国内适配方案](#21-海外项目国内适配方案)
  - [2.2 核心替代数据源](#22-核心替代数据源)
- [3. 国内原生项目（中国市场专用）](#3-国内原生项目中国市场专用)
  - [3.1 数据基础设施层](#31-数据基础设施层)
  - [3.2 策略/研究层](#32-策略研究层)
  - [3.3 资源索引](#33-资源索引)
- [4. 推荐国内技术方案](#4-推荐国内技术方案)
- [5. 总结](#5-总结)

---

## 1. 全球宏观研究项目（海外 GitHub）

### 1.1 macro-signal-builder ⭐ 首推

- **仓库地址**：<https://github.com/gyimadu/macro-signal-builder>
- **定位**：宏观分析与投资信号生成系统，将经济指标转化为跨资产类别的可执行买卖信号

**覆盖维度：**

| 你的需求 | 覆盖方式 |
|----------|----------|
| 央行动作 | Fed Funds Rate 作为核心指标 |
| 美债收益率 | TLT（20+年美债ETF），含债市评分逻辑 |
| 美元指数 | UUP（美元看多ETF），利率驱动信号 |
| 股市 | SPY、QQQ 多因子打分 |
| 黄金 | GLD 作为通胀/不确定性对冲 |
| 流动性/大事件 | 宏观 regime 分类：滞胀、衰退、通缩、扩张、过热 |

**核心特性：**

- 实时 macro regime 检测（Stagflation, Recession, Disinflation, Expansion, Overheating）
- 实时指标：GDP 增长、CPI 通胀、失业率、联邦基金利率
- 资产信号：SPY（股票）、TLT（债券/国债）、GLD（黄金）、UUP（美元）
- 信号逻辑：GDP 增长利好股市；高通胀/高利率利空债市；联邦基金利率 > 4% → 做多美元
- REST API 端点：当前数据、历史序列、regime 分析
- 数据跨度：2008–2025
- 技术栈：Flask + Chart.js Dashboard

---

### 1.2 market-intelligence-dashboard ⭐ 专业级

- **仓库地址**：<https://github.com/noivuduc/market-intelligence-dashboard>
- **定位**：Bloomberg 终端级别的开源替代品，自托管单人市场情报指挥中心

**模块覆盖：**

| 模块 | 追踪内容 |
|------|----------|
| 央行/政策 | 联邦基金目标利率、缩表/QT 节奏、FOMC 倒计时、政策 stance |
| 美债/利率 | 3M–30Y 全曲线、2s10s / 2s30s 利差、曲线 regime 分类 |
| 宏观 | CPI、Core PCE、非农、GDP、ISM（含超预期值/z-score 分析） |
| 流动性 | SOFR、准备金、ON RRP、NFCI 金融条件指数、HY/IG 信用利差、VIX |
| 股市 | SPX / NDX / RUT、等权指数、板块 52 周位置 |
| 资金流 | ETF 资金流量代理指标 |

**核心特性：**

- Regime engine 含置信度评分
- 阈值触发警报
- 可选 Claude AI 简报生成
- 部署方式：自托管 Web 应用

---

### 1.3 Macro-AI-Dashboard ⭐ 利率专精

- **仓库地址**：<https://github.com/ankit637836/Macro-AI-Dashboard>
- **定位**：由专业 SOFR / Fed Funds 期货交易员构建的利率分析平台

**核心功能：**

- SOFR 曲线可视化（隔夜到 180 天）
- 跨市场反应分析：CPI/NFP/FOMC 公布时，同时观察 WTI、黄金、DXY（美元指数）、SOFR 的联动
- Fed Funds 合约构建器（日历价差、蝴蝶价差）
- AI 评论：Gemini 对 2022 年以来每次宏观事件生成解读

**技术栈：** FastAPI + React + FRED API + Yahoo Finance

---

### 1.4 Macro Shock Risk Engine ⭐ 事件驱动

- **仓库地址**：<https://github.com/Josh20241995/Macro-Shocks-Portfolio-Risk-Engine>
- **定位**：机构级跨资产风险框架，专门检测和应对宏观冲击事件

**核心功能：**

- **事件检测 + NLP**：解析 Fed 会议纪要（鹰鸽评分 + Transformer embedding）
- **缺口风险监控**：特别关注周五盘后/周末缺口风险走廊
- **前置脆弱性分析**：收益率曲线、信用利差、VIX 期限结构
- **情景引擎**：概率加权的冲击路径树
- **投资组合对冲建议**：覆盖股票、固收、外汇、商品

**技术栈：** Python 3.11 / C++17 / C# 10，含实时警报

---

### 1.5 量化宏观策略项目

| 项目 | 核心技术 | 美债 | 央行 | 股市 | 回测效果 |
|------|----------|:--:|:--:|:--:|------|
| [AdaptiveRegimeStrategy](https://github.com/gitmichaelqiu/AdaptiveRegimeStrategy) | GMM + Kalman Filter | ✅ 10Y 利率变化率 | ✅ 利率周期 | ✅ | Sharpe **1.37–1.52** |
| [Macro_Regime_Switching_Model](https://github.com/oj0nathan/Macro_Regime_Switching_Model) | HMM 隐马尔可夫 | ✅ TLT 配置 | ✅ 利率背景 | ✅ 多资产 | 总回报 **349%** vs 基准220% |
| [HMM + MPT 配置](https://github.com/bspreston10/Macro-Regime-and-Allocation-Strategy-HMM) | HMM + 现代组合理论 | ✅ TLT 核心资产 | 间接 | ✅ SPY 核心 | 最大回撤 **-25.6%** vs -54.8% |
| [Macro-Sentiment-Indicators](https://github.com/jurchiks33/Macro-Sentiment-and-Financial-Indicators) | 回归 + 可视化 | ✅ 收益率曲线 | M2/ISM | ✅ S&P 500 | 研究工具包 |

#### AdaptiveRegimeStrategy 详细介绍

- 基于 **适应性市场假说（Adaptive Markets Hypothesis）**
- **Macro Switch**：从 VIX 和 10 年期美债收益率变化率（`^TNX`）计算 `Total_Stress` 分数，高压力→股票卖出信号，通胀资产买入信号
- **Regime Shield**：滚动窗口高斯混合模型（GMM）分类牛/熊/震荡市，熊市否决多头信号
- **Yang-Zhang 波动率目标**：动态仓位管理
- 2022–2024 回测于 NVDA、JPM、TSLA、BABA、XLE——Sharpe 1.37–1.52，最大回撤大幅降低

#### Macro_Regime_Switching_Model 详细介绍

- 用美国工业产值增长和 CPI 通胀训练 HMM，分类 4 种宏观状态：
  - Crisis（危机）/ Stagnation（停滞）/ Expansion-Goldilocks（金发女孩）/ Boom-Overheating（过热）
- 5 资产标的：SPY、TLT、HYG、DBC、GLD
- **关键发现**：股债相关性在不同 regime 下**方向反转**
- 用滤波概率（filtered probabilities）+ 1 个月滞后避免前瞻偏差
- 回测 2007–2025：总回报 349% vs 基准 220%，Sharpe 0.88 vs 0.74，最大回撤 -15.9% vs -24.4%

#### HMM + MPT 配置 详细介绍

- 训练 HMM 于 SPY、TLT、黄金之间的**动态相关性**
- 三 regime 分类：
  - **Divergent Macro（Risk-On）** → 重仓 SPY
  - **Flight to Safety（Risk-Off）** → 偏重 TLT + 黄金
  - **Transition Zone** → 均衡配置
- 用**滚动相关性趋势的一阶导数**加速 regime 检测
- 2003–2024 回测：Sharpe 0.79 vs SPY 0.53，2008 危机周收益 +0.19% vs SPY -0.04%

#### Macro-Sentiment-Indicators 详细介绍

- M2 货币供应 vs S&P 500 回归分析 + 交易信号
- 美债收益率曲线分析：10Y–2Y 利差可视化；标记正常/倒挂/平坦曲线作为衰退/扩张信号
- VIX "恐慌指数" 分析
- ISM 制造业报告爬虫
- 密歇根大学消费者信心指数追踪
- 技术栈：`yfinance`、`pandas_datareader` (FRED)、`matplotlib`、`scipy`

---

### 1.6 资源聚合类（Awesome Lists）

| 项目 | Stars | 说明 |
|------|:-----:|------|
| [awesome-quant](https://github.com/wilsonfreitas/awesome-quant) | 15,750 | 量化金融最全列表 |
| [awesome-systematic-trading](https://github.com/paperswithbacktest/awesome-systematic-trading) | 2,835 | 97 个库 + 40+ 学术策略实现 |
| [awesome-ai-in-finance](https://github.com/georgezouq/awesome-ai-in-finance) | — | AI + 金融 |
| [pysystemtrade](https://github.com/robcarver17/pysystemtrade) | — | Rob Carver《Systematic Trading》配套代码——经典全球宏观/CTA 框架 |

#### 框架推荐
- [QuantConnect (Lean)](https://github.com/QuantConnect/Lean) — C# / Python 机构级引擎
- [nautilus_trader](https://github.com/nautechsystems/nautilus_trader) — Python + Rust 高性能事件驱动
- [vectorbt](https://github.com/polakowo/vectorbt) — Python + Numba 矢量化回测
- [Zipline-Reloaded](https://github.com/stefan-jansen/zipline-reloaded) — Quantopian Zipline 维护分支

#### AI/ML 增强
- [QLib (微软)](https://github.com/microsoft/qlib) — AI 导向量化平台
- [FinRL](https://github.com/AI4Finance-Foundation/FinRL) — 深度强化学习自动交易
- [AI Hedge Fund](https://github.com/virattt/ai-hedge-fund) — 多 Agent AI 交易模拟

---

## 2. 国内可用性分析

### 2.1 海外项目国内适配方案

| 项目 | 国内可用性 | 问题 | 解决方案 |
|------|:---:|------|------|
| **macro-signal-builder** | ⚠️ 需改造 | 依赖 `yfinance` 拉美股数据，国内经常连不上 | 换 AKShare 取美股/ETF 数据 |
| **market-intelligence-dashboard** | ⚠️ 需改造 | FRED API 国内能访问，但 `yfinance` 不稳 | FRED 部分保留，股市部分切 AKShare |
| **Macro-AI-Dashboard** | ⚠️ 部分可用 | FRED API 国内可访问；Gemini API 需要梯子 | Gemini → DeepSeek / 通义千问 / 智谱 API |
| **Macro Shock Risk Engine** | ⚠️ 需改造 | 依赖多个海外 API | 核心逻辑可用，数据源需替换 |
| **所有 HMM/策略回测项目** | ✅ 逻辑可用 | 策略代码本身不依赖网络 | 只需把数据读取层换成国内源 |

> **核心问题就一个：数据源。代码逻辑、模型、可视化都不受墙影响。**

### 2.2 核心替代数据源

```
国外源（可能被墙/慢）           →    国内替代（稳定免费）
──────────────────────────────────────────────────
yfinance (美股行情)             →    AKShare 美股模块
FRED API (美国宏观)             →    AKShare 海外宏观 + 国内宏观
Yahoo Finance (ETF数据)         →    AKShare 基金/ETF 模块
Google Gemini (AI解读)          →    通义千问 / DeepSeek / 智谱 API
```

#### AKShare —— 最核心的国内替代方案

- **仓库地址**：<https://github.com/akfamily/akshare>
- **Stars**：20k+
- **安装**：`pip install akshare`
- **协议**：MIT 开源，完全免费，无需注册 / API Key
- **数据源**：东方财富、新浪财经、腾讯财经、上交所、深交所等

**AKShare 覆盖你需要的全部数据：**

| 数据类别 | 具体覆盖 |
|----------|----------|
| 中国宏观 | CPI / PPI / PMI / M2 / 社融 / LPR / Shibor / 准备金率 / 存贷款利率 |
| 美国宏观 | 美联储利率、美国 CPI、非农、GDP、PMI |
| 美债 | 美国国债收益率曲线（各期限） |
| 美元指数 | 有接口 |
| A股 | 行情、财务、资金流向、龙虎榜 |
| 美股 | 美股历史行情 |
| 债券 | 国债、企业债、可转债 |
| 基金/ETF | 含 SPY / TLT / UUP / GLD 等 |
| 新闻舆情 | 财联社、东方财富等 |

#### 其他国内数据源

| 数据源 | Stars | 特点 |
|------|:-----:|------|
| [TuShare](https://github.com/waditu/tushare) | 15k+ | 财务数据更系统，需注册 token，高级功能需积分 |
| [JoinQuant/jqdatasdk](https://github.com/JoinQuant/jqdatasdk) | — | 聚宽数据 SDK |
| [ashare-mcp](https://github.com/lolifamily/ashare-mcp) | — | 基于 baostock 的 MCP server |

---

## 3. 国内原生项目（中国市场专用）

### 3.1 数据基础设施层

| 项目 | Stars | 说明 |
|------|:-----:|------|
| [AKShare](https://github.com/akfamily/akshare) | 20k+ | **一切数据的来源**——免费、无需 API Key、`pip install akshare` 即用 |
| [akshare-rs](https://github.com/Cricle/akshare-rs) | — | AKShare 的 100% Rust 实现，零 Python 依赖 |
| [FinQ4Cn-mcp-server](https://github.com/jinhongzou/FinQ4Cn-mcp-server) | 新 | 基于 AKShare 的 MCP Server，直接对接 Claude Code 等 AI 工具 |
| [aigroup-market-mcp](https://www.jsdelivr.com/package/npm/aigroup-market-mcp) | — | 基于 Tushare + 百度新闻的金融数据 MCP Server |
| [invest-skills](https://github.com/Veblin/invest-skills) | — | 多源数据采集框架，Tushare + AKShare + FRED 混合配置 |

### 3.2 策略/研究层

| 项目 | Stars | 定位 |
|------|:-----:|------|
| [Qlib (微软)](https://github.com/microsoft/qlib) | 45k | AI 量化研究平台，含 A 股专用 Alpha158/360 因子集 |
| [vnpy](https://github.com/vnpy/vnpy) | 42k | 实盘级量化框架，A 股/期货/期权全覆盖 |
| [QUANTAXIS](https://github.com/yutiansut/QUANTAXIS) | 10k+ | 本地化量化全栈框架（数据/回测/模拟/交易） |
| [RQAlpha](https://github.com/ricequant/rqalpha) | 6k+ | 米筐开源回测框架，事件驱动 |
| [FactorHub](https://github.com/cn-vhql/FactorHub) | 新 | A 股多因子分析平台：因子管理 + IC 分析 + 遗传算法挖掘 + 组合优化 |
| [quant-stock-selector](https://github.com/Brown9487/quant-stock-selector) | — | A 股选股策略：行业趋势 + 动量，AKShare + TuShare 双源 |
| [valueinvest](https://github.com/wangzhe3224/valueinvest) | — | 估值库：Graham / DCF / DDM / PEG 等估值模型，AKShare + yfinance 双源 |

### 3.3 资源索引

| 项目 | 说明 |
|------|------|
| [thuquant/awesome-quant](https://github.com/thuquant/awesome-quant) | 中文 Quant 资源大全——数据源、策略、框架、教程一站式索引 |

---

## 4. 推荐国内技术方案

### 全栈架构建议

```
┌─────────────────────────────────────────────────┐
│  数据层                                          │
│  AKShare (主数据源) + TuShare (财务数据补充)      │
│  覆盖：中国宏观 + 美国宏观 + 美债 + 美元指数 +     │
│  A股行情/财务 + 美股ETF                          │
├─────────────────────────────────────────────────┤
│  分析层                                          │
│  ① 宏观仪表盘 —— market-intelligence-dashboard   │
│     设计思路 + AKShare 数据源                     │
│  ② 策略回测 —— vectorbt / Qlib / RQAlpha        │
│  ③ AI 解读 —— DeepSeek API / 通义千问 / 智谱     │
├─────────────────────────────────────────────────┤
│  输出                                            │
│  宏观 regime 判断 + 股市大方向信号                │
│  + 资产配置建议（股/债/金/现金）                  │
└─────────────────────────────────────────────────┘
```

> 数据获取全部通过 AKShare，一条 `pip install akshare` 搞定，**不翻墙、不注册、不付费**。

### 两条可行路径

**方案 A：改造海外成熟项目**

拿国外成熟项目的"骨架"（如 macro-signal-builder 的信号逻辑、market-intelligence-dashboard 的仪表盘设计），**把数据读取层全部替换成 AKShare**。这些项目的 Python 依赖结构清晰，改数据源通常只需要改几十行 import 和 API 调用。投入小、见效快。

**方案 B：用 AKShare + 国内框架从零搭建**

完全掌控，灵活性最高。推荐技术组合：

```
入门层：AKShare + pandas + backtesting/vectorbt
研究层：AKShare + Qlib（因子/ML）+ RQAlpha（事件回测）
实盘层：vnpy（工程化平台，含风控/数据记录/策略模块）
宏观层：AKShare 宏观模块（替代 FRED 中国部分）
```

---

## 5. 总结

| 使用场景 | 推荐项目 |
|----------|----------|
| 🎯 快速看信号定大方向 | [macro-signal-builder](https://github.com/gyimadu/macro-signal-builder) —— 直接给 SPY/TLT/UUP/GLD 买卖信号 |
| 📊 全面监控宏观全景 | [market-intelligence-dashboard](https://github.com/noivuduc/market-intelligence-dashboard) —— 央行 + 流动性 + 利差 + 股市宽度一个面板 |
| 💹 深入利率和美元 | [Macro-AI-Dashboard](https://github.com/ankit637836/Macro-AI-Dashboard) —— SOFR 曲线 + DXY 联动 + AI 解读 |
| 🧪 跑回测验证策略 | [Macro_Regime_Switching_Model](https://github.com/oj0nathan/Macro_Regime_Switching_Model)、[AdaptiveRegimeStrategy](https://github.com/gitmichaelqiu/AdaptiveRegimeStrategy) |
| ⚡ 监控黑天鹅/大事件 | [Macro Shock Risk Engine](https://github.com/Josh20241995/Macro-Shocks-Portfolio-Risk-Engine) |
| 🇨🇳 国内直接用 | [AKShare](https://github.com/akfamily/akshare) + [Qlib](https://github.com/microsoft/qlib) + [FactorHub](https://github.com/cn-vhql/FactorHub) |
| 📚 找更多资源 | [thuquant/awesome-quant](https://github.com/thuquant/awesome-quant)、[awesome-quant](https://github.com/wilsonfreitas/awesome-quant)、[awesome-systematic-trading](https://github.com/paperswithbacktest/awesome-systematic-trading) |

---

*以上项目均为 GitHub 开源项目，大部分使用 MIT 或 Apache 2.0 协议。整理于 2026-07-15，项目状态和 Star 数以当时为准。*
