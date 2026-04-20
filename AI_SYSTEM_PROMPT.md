# BTC 日报系统 v2.1 — AI 操作提示词手册

> **目标**：让另一个 AI 能够完整理解、执行、维护这个 BTC 日报自动化系统。
> **适用场景**：接手该项目 / 继续开发 / 排查问题 / 继续迭代功能。
> **最后更新**：2026-04-19

---

## 一、系统架构总览

```
用户触发（定时 10:25 / 手动运行）
        │
        ▼
┌─────────────────────────────────┐
│   run_daily_report.py (主脚本)    │
├─────────────────────────────────┤
│ Step1: 检查今天是否已生成日报      │
│ Step2: fetch_btc_data.py 采集数据  │
│ Step3: generate_strategy() 制定策略│
│ Step4: auto_resolve_yesterday()   │
│        用今天价格自动复盘昨天交易    │
│ Step5: generate_html() 生成日报    │
│ Step6: 保存 .html 文件             │
│ Step7: 更新 index.html             │
│ Step8: Git commit + push           │
│ Step9: Telegram 推送              │
└─────────────────────────────────┘
        │
        ▼
日报输出: btc/reports/BTC_daily_report_YYYYMMDD.html
GitHub Pages: https://mktrading.vip/btc/reports/
```

---

## 二、文件清单

| 文件路径 | 作用 |
|----------|------|
| `btc/run_daily_report.py` | **主控脚本**，包含所有业务逻辑（1163行） |
| `btc/fetch_btc_data.py` | 数据采集：从 Binance/CoinGecko/API 获取实时数据 |
| `btc/telegram_notify.py` | Telegram 推送模块 |
| `btc/reports/BTC_daily_report_20260415_PROFESSIONAL.html` | **日报模板**，含8个占位符 |
| `btc/cache/strategy_history.json` | **历史策略记录**，近30天，由脚本自动维护 |
| `btc/cache/prev_strategy.json` | **昨日策略快照**，今天运行时写入，明天自动复盘用 |
| `btc/index.html` | 日报存档首页，展示所有历史日报列表 |
| `MEMORY.md` | 长期规范文档，记录版本历史和硬性标准 |

---

## 三、核心概念：自动复盘机制（最重要）

### 3.1 为什么要自动复盘？

**问题**：用户不想每次手动填昨天的复盘结果，也不想每天改报告。
**解决方案**：今天的脚本运行时，用"今天的价格数据"和"昨天日报里记录的策略"做对比，自动判断昨天那笔交易的结果。

### 3.2 判断规则（`auto_resolve_yesterday` 函数）

```
昨天策略记录：direction, stop_loss, tp1, tp2
今天价格数据：high_24h（24h最高）, low_24h（24h最低）

【多头 LONG】
  if today_low < SL      → 止损出局 → result = 'LOSS'
  elif today_high >= TP2 → TP2达成 → result = 'WIN'
  elif today_high >= TP1 → TP1达成 → result = 'WIN'
  else                   → 未触及任一目标 → result = 'BREAK_EVEN'

【空头 SHORT】
  if today_high > SL     → 止损出局 → result = 'LOSS'
  elif today_low <= TP2  → TP2达成 → result = 'WIN'
  elif today_low <= TP1   → TP1达成 → result = 'WIN'
  else                    → 未触及任一目标 → result = 'BREAK_EVEN'
```

### 3.3 日志写入

复盘结果更新到 `strategy_history.json` 最后一条记录，同时写入：
- `result`：最终结果标签
- `auto_resolved: True`：标记为自动复盘
- `resolve_note`：记录判断依据（如 `Today H=77200 L=75655 | SL=74800 TP1=78000 TP2=79500 → WIN`）

---

## 四、数据存储结构

### 4.1 `strategy_history.json`（历史记录）

```json
[
  {
    "date": "20260418",
    "direction": "LONG",
    "entry_low": 76000,
    "entry_high": 76500,
    "stop_loss": 74800,
    "tp1": 78000,
    "tp2": 79500,
    "rr": 2.6,
    "result": "BREAK_EVEN",       // WIN | WIN_TP1 | LOSS | BREAK_EVEN | OPEN | SKIP
    "auto_resolved": true,
    "resolve_note": "Today H=77200 L=75655 | SL=74800 TP1=78000 TP2=79500 → BREAK_EVEN"
  }
]
```

**result 字段枚举**：
| 值 | 含义 |
|----|------|
| `WIN` | TP2 达成（全胜） |
| `WIN_TP1` | TP1 达成（半胜） |
| `LOSS` | 止损出局 |
| `BREAK_EVEN` | 未触及任一目标（等回踩/持仓中） |
| `OPEN` | 当天新建的交易，等明天自动结算 |
| `SKIP` | 观望策略，不执行 |

### 4.2 `prev_strategy.json`（昨日策略快照）

```json
{
  "date": "04/18",
  "direction": "LONG",
  "confidence": 50,
  "signals": ["MACD 金叉，看多", "价格 > EMA20"],
  "entry_low": 76000,
  "entry_high": 76500,
  "stop_loss": 74800,
  "tp1": 78000,
  "tp2": 79500,
  "rr_ratio": 2.6,
  "position_size": "10-15%"
}
```

---

## 五、模板系统（v2.1 核心）

### 5.1 模板文件

`btc/reports/BTC_daily_report_20260415_PROFESSIONAL.html`

### 5.2 模板中的 8 个占位符

HTML 模板里的硬编码板块全部替换为注释占位符，格式：`<!-- {{SECTION_X}} -->`：

| 占位符 | 对应板块 | 生成函数 | 数据来源 |
|--------|----------|----------|----------|
| `<!-- {{SECTION1_STATS}} -->` | 一、综合统计看板 | `gen_section1_stats()` | `strategy_history.json` |
| `<!-- {{SECTION7_TRACKING}} -->` | 七、近14天策略追踪表 | `gen_section7_tracking_table()` | `strategy_history.json` |
| `<!-- {{SECTION8_ERROR_STATS}} -->` | 八、错误分类统计 | `gen_section8_error_stats()` | `strategy_history.json` |
| `<!-- {{SECTION9_BARS}} -->` | 九、近14天胜率柱状图 | `gen_section9_bars()` | `strategy_history.json` |
| `<!-- {{SECTION10_LINE}} -->` | 十、近30天胜率趋势折线图 | `gen_section10_line()` | `strategy_history.json` |
| `<!-- {{SECTION11_YESTERDAY_REVIEW}} -->` | 十一、昨日复盘 | `gen_section11_yesterday_review()` | prev_strategy.json + 今日价格 |
| `<!-- {{SECTION12_WEEK_REVIEW}} -->` | 十二、本周综合复盘 | `gen_section12_week_review()` | `strategy_history.json` |
| `<!-- {{SECTION13_MONTH_REVIEW}} -->` | 十三、月回顾统计 | `gen_section13_month_review()` | `strategy_history.json` |

### 5.3 `generate_html()` 中的替换流程

```python
# 1. 加载昨日策略（来自 cache/prev_strategy.json）
prev_strategy = load_prev_strategy()

# 2. 调用8个生成函数
section1  = gen_section1_stats(history, date_display)
section7  = gen_section7_tracking_table(history, date_str)
section8  = gen_section8_error_stats(history)
section9  = gen_section9_bars(history)
section10 = gen_section10_line(history)
section11 = gen_section11_yesterday_review(prev_strategy, history, data, yesterday_display)
section12 = gen_section12_week_review(history)
section13 = gen_section13_month_review(history)

# 3. 一次性替换全部占位符
html = html.replace('<!-- {{SECTION1_STATS}} -->', section1)
html = html.replace('<!-- {{SECTION7_TRACKING}} -->', section7)
# ... 其余同理
```

---

## 六、每日完整执行流程

```
T-1 天（昨天）结束时：
  → cache/prev_strategy.json 已包含昨天的策略

T 天 10:25 定时触发（或手动运行）：
  Step 1: 检查今天日报是否已存在 → 存在则跳过
  Step 2: fetch_btc_data.fetch_all() → 获取实时数据（BTC价格/资金费率/OI/RSI/MACD/布林带等）
  Step 3: generate_strategy(data) → 基于数据生成今日策略
  Step 4: 读取 prev_strategy.json → auto_resolve_yesterday(data, prev_strategy, history)
           → 自动更新 strategy_history.json 中昨天那笔的 result
  Step 5: generate_html() → 读取模板，替换全部占位符，生成今日日报
  Step 6: 写入 cache/prev_strategy.json（今天的策略快照，供明天复盘用）
  Step 7: 追加今日策略到 strategy_history.json（标记 result=OPEN）
  Step 8: 保存 BTC_daily_report_YYYYMMDD.html 到 btc/reports/
  Step 9: 更新 btc/index.html（插入今日日报卡片）
  Step 10: Git add → commit → push
  Step 11: Telegram 推送日报链接到频道 @bitebiwanglin
```

---

## 七、8个动态生成函数详解

### `gen_section1_stats(history, date_display)`
- 输入：`strategy_history.json` 全部记录
- 逻辑：取最后14条，计算胜率/盈亏比/最大回撤/交易天数
- 输出：综合统计看板 HTML（6个数据卡片）

### `gen_section7_tracking_table(history, today_str)`
- 输入：最后14条记录 + 今天日期字符串
- 逻辑：生成14行表格，今日行加 `class="today-row"` + TODAY 橙色徽章
- 输出：10列表格（日期/方向/涨跌/进场区间/SL/TP1/TP2/结果/盈亏比/错误分析）

### `gen_section8_error_stats(history)`
- 输入：最后14条记录
- 逻辑：统计各类错误（情绪化/追单/移动止损/未过清单/盈亏比<2:1）
- 输出：错误分类统计 HTML + 改进建议

### `gen_section9_bars(history)`
- 输入：最后14条记录
- 逻辑：每条记录对应一根柱状图，绿色=盈利，红色=亏损，灰色=保本
- 输出：柱状图 HTML

### `gen_section10_line(history)`
- 输入：最后30条记录
- 逻辑：从第1条到第N条逐步计算累计胜率，绘制 SVG 折线图
- 输出：SVG 折线图 + 面积填充 HTML

### `gen_section11_yesterday_review(prev_strategy, history, data, today_display)`
- 输入：昨日策略快照 + 今日实时价格数据
- 逻辑：见"三、核心概念：自动复盘机制"
- 输出：昨日复盘表格（含最大失误/亮点/执行打分）

### `gen_section12_week_review(history)`
- 输入：最后7条记录
- 逻辑：本周汇总统计 + 最大单笔盈利/亏损 + 改进建议
- 输出：本周复盘 HTML

### `gen_section13_month_review(history)`
- 输入：全部历史记录（近30天）
- 逻辑：本月汇总 + 胜率达标判断 + 盈亏比达标判断 + 错误率
- 输出：月回顾统计 HTML

---

## 八、策略生成规则（`generate_strategy` 函数）

### 8.1 信号维度

| 维度 | 看多条件 | 看空条件 |
|------|----------|----------|
| 恐惧贪婪 | 指数 < 30 + RSI < 40 | 指数 > 70 |
| MACD | 金叉 (GOLDEN) | 死叉 (DEAD) |
| 资金费率 | 费率 < -0.01%（空头付多头） | 费率 > +0.01% |
| EMA20 | 价格 > EMA20 | 价格 < EMA20 |
| EMA50 | 价格 > EMA50 | 价格 < EMA50 |
| 布林带 | 价格触及下轨（超卖） | 价格触及上轨（超买） |

### 8.2 方向决策

- `confidence >= 40` 或 `>= 20` → 按信号方向执行（LONG/SHORT）
- 否则 → `WAIT`（观望）

### 8.3 关键价位计算

```
做多 LONG：
  进场区间 = [max(price*0.995, bb_middle), price]
  止损 = bb_lower（下轨）
  TP1 = min(price*1.035, ema20)
  TP2 = min(price*1.06, bb_upper)

做空 SHORT：
  进场区间 = [price*0.995, min(price*1.008, ema20)]
  止损 = max(price*1.018, bb_upper)
  TP1 = price*0.965
  TP2 = price*0.94
```

---

## 九、Telegram 推送配置

- Bot：`@MK_BTC_Alert_Bot`
- Token：`8626387493:AAE2XCzMzmhDiWRaGKVEjrj2EGLPsDN22-Q`
- 推送频道：`@bitebiwanglin`（比特币王林公开频道）
- Chat ID：`-1003189007280`
- 配置文件：`btc/telegram_config.json`
- **时序要求**：必须等 Git push 完成后才推送，确保日报在 GitHub Pages 上可访问

---

## 十、Git 管理规范

- 仓库：`wanglin141319-bit/mk-trading`
- 分支：main
- **每次 commit 前必须检查文件大小**：`Get-Item` 确认 Length > 0，避免 commit 空文件
- commit message 格式：`feat: auto BTC daily report YYYYMMDD`

---

## 十一、硬性标准（日报模板要求）

日报中的以下板块必须满足硬性标准：

| 标准 | 达标值 |
|------|--------|
| 14天胜率 | ≥ 55% |
| 平均盈亏比 | ≥ 2:1 |
| 最大回撤 | < 15% |

这三个指标在统计看板中会显示绿色/红色徽章。

---

## 十二、版本历史

| 版本 | 日期 | 核心变更 |
|------|------|----------|
| v1.0 | 2026-04-15 | 初始16板块模板，策略追踪表7列 |
| v2.0 | 2026-04-18 | 策略追踪表升级为10列，增加彩色标签和TODAY徽章 |
| v2.1 | 2026-04-19 | **彻底修复虚构数据**：模板硬编码→占位符，8个动态生成函数，数据100%来自API和JSON，禁止虚构复盘结果 |
| v2.2 | 2026-04-19 | 修复 `gen_section13_month_review` 累计盈亏逻辑：原硬编码"待核实"→基于 pnl 字段或 rr 估算计算；新增最大单笔回撤字段；盈亏单位统一用 R（风险倍数） |

---

## 十三、AI 接手时的关键注意事项

1. **永远不要在日报里写模拟/虚构数据**。所有数字必须来自 `strategy_history.json` 或实时 API。
2. **昨日复盘永远是自动生成的**，基于当天价格 + 昨日策略判断，不是手动编的。
3. **当天行标记为 `result=OPEN`**，等明天自动结算后再更新为真实结果。
4. **修改任何逻辑后必须验证**：运行 `python run_daily_report.py`，确认日报生成成功且数据正确。
5. **Git commit 前检查文件大小**，防止 commit 空文件。
