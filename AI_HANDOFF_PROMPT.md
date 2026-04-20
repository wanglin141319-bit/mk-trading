# BTC 日报系统 v2.2 — AI 代理执行手册
> 本文件是完整的 AI-to-AI 操作指令集。直接将本文件内容（不含本行）复制给另一个 AI，即可让它理解并维护本系统。

---

## 【系统定位】

你是 MK Trading 的 BTC 日报自动化系统。系统每天 10:25 自动运行，生成 BTC 合约日报，推送到 Telegram 频道 `@bitebiwanglin`，并同步到 GitHub Pages。

**核心原则**：永远不写虚构数据。所有数字必须来自 API 或 JSON 文件。

---

## 【文件架构】

```
项目根目录：C:/Users/asus/mk-trading/btc/

核心文件：
├── run_daily_report.py          # ⭐ 主控脚本（所有业务逻辑，1260+行）
├── fetch_btc_data.py            # 数据采集（Binance/CoinGecko API）
├── telegram_notify.py            # Telegram 推送模块
├── index.html                    # 日报存档首页
├── cache/
│   ├── strategy_history.json     # 📊 历史策略记录（近30天，自动维护）
│   ├── prev_strategy.json        # 📌 昨日策略快照（今天写入，明天复盘用）
│   └── btc_latest.json          # 最新价格数据缓存
└── reports/
    └── BTC_daily_report_20260415_PROFESSIONAL.html  # 📄 日报模板（含8个占位符）
```

---

## 【每日自动执行流程（9步）】

```
每天 10:25 定时触发（或手动运行 python run_daily_report.py）

Step 1  检查重复
        检查 btc/reports/BTC_daily_report_YYYYMMDD.html 是否已存在
        → 已存在则跳过本次执行

Step 2  数据采集
        fetch_btc_data.fetch_all()
        → 返回 dict，含 btc/eth/funding/oi/fear_greed/technical/macro 等子数据

Step 3  策略制定
        generate_strategy(data)
        → 返回策略 dict：direction/LONG/SHORT/WAIT、stop_loss/tp1/tp2/entry区间/rr_ratio/confidence

Step 4  自动复盘（核心机制）
        auto_resolve_yesterday(data, prev_strategy, history)
        → 读取 cache/prev_strategy.json（昨天的策略）
        → 用今天的价格数据（high_24h / low_24h）判断昨天的交易结果
        → 自动更新 strategy_history.json 中最后一条记录的 result 字段

Step 5  生成日报
        generate_html(data, strategy, history)
        → 读取模板，替换全部8个占位符，生成 BTC_daily_report_YYYYMMDD.html

Step 6  保存快照
        → 将今天的策略写入 cache/prev_strategy.json（供明天复盘）
        → 将今日策略追加到 strategy_history.json（标记 result=OPEN，等明天结算）

Step 7  保存文件
        → BTC_daily_report_YYYYMMDD.html → btc/reports/
        → 同时复制到 C:/Users/asus/WorkBuddy/（用户直接访问）

Step 8  Git 提交推送
        → git add . → git commit → git push origin main
        → ⚠️ commit 前必须检查文件大小 > 0

Step 9  Telegram 推送
        → 等 Step 8（Git push）完成后再推送
        → 确保日报已在 GitHub Pages 上线，用户点击链接能访问

```

---

## 【自动复盘机制（最重要）】

### 什么是自动复盘？

今天运行脚本时，系统**不需要用户手动输入**昨天的结果。
它自动做这件事：
> "昨天策略里写了做多，SL=74800，TP1=78000，TP2=79500。
> 今天最高涨到 77200，最低跌到 75655。
> → TP1/TP2 都未触及 → 持仓中，未平仓 → result=BREAK_EVEN"

### 判断逻辑（`auto_resolve_yesterday` 函数）

**多头 LONG**：
```
if today_low < SL       → 止损出局 → result = 'LOSS'
elif today_high >= TP2  → TP2达成 → result = 'WIN'
elif today_high >= TP1  → TP1达成 → result = 'WIN'
else                     → 未触及任一 → result = 'BREAK_EVEN'
```

**空头 SHORT**：
```
if today_high > SL      → 止损出局 → result = 'LOSS'
elif today_low <= TP2    → TP2达成 → result = 'WIN'
elif today_low <= TP1    → TP1达成 → result = 'WIN'
else                     → 未触及任一 → result = 'BREAK_EVEN'
```

**观望 WAIT**：跳过，不更新。

复盘结果写入 `strategy_history.json` 最后一条：
```json
{
  "result": "BREAK_EVEN",
  "auto_resolved": true,
  "resolve_note": "Today H=77200 L=75655 | SL=74800 TP1=78000 TP2=79500 → BREAK_EVEN"
}
```

---

## 【数据结构】

### `strategy_history.json`（历史记录）

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
    "result": "BREAK_EVEN",
    "auto_resolved": true,
    "resolve_note": "Today H=77200 L=75655 | SL=74800 TP1=78000 TP2=79500 → BREAK_EVEN"
  }
]
```

**result 字段枚举**：

| 值 | 含义 | 盈亏（R） |
|----|------|---------|
| `WIN` | TP2 达成，全胜 | +2.0R |
| `WIN_TP1` | TP1 达成，半胜 | +1.0R |
| `LOSS` | 止损出局 | -1.0R |
| `BREAK_EVEN` | 未触及任一目标（持仓中） | 0 |
| `OPEN` | 当天新建，等明天自动结算 | 待定 |
| `SKIP` | 观望策略，不执行 | 0 |

### `prev_strategy.json`（昨日策略快照）

由今天写入，明天自动复盘时读取：
```json
{
  "direction": "LONG",
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

## 【模板占位符系统】

日报模板 `BTC_daily_report_20260415_PROFESSIONAL.html` 中的8个硬编码板块全部替换为占位符：

```html
<!-- {{SECTION1_STATS}} -->
<!-- {{SECTION7_TRACKING}} -->
<!-- {{SECTION8_ERROR_STATS}} -->
<!-- {{SECTION9_BARS}} -->
<!-- {{SECTION10_LINE}} -->
<!-- {{SECTION11_YESTERDAY_REVIEW}} -->
<!-- {{SECTION12_WEEK_REVIEW}} -->
<!-- {{SECTION13_MONTH_REVIEW}} -->
```

`generate_html()` 中的替换顺序：
```python
section1  = gen_section1_stats(history, date_display)
section7  = gen_section7_tracking_table(history, date_str)
section8  = gen_section8_error_stats(history)
section9  = gen_section9_bars(history)
section10 = gen_section10_line(history)
section11 = gen_section11_yesterday_review(prev_strategy, history, data, yesterday_display)
section12 = gen_section12_week_review(history)
section13 = gen_section13_month_review(history)

html = html.replace('<!-- {{SECTION1_STATS}} -->', section1)
html = html.replace('<!-- {{SECTION7_TRACKING}} -->', section7)
# ... 其余同理
```

---

## 【8个动态板块生成函数】

### 1. `gen_section1_stats(history, date_display)`
- 数据源：`strategy_history.json`
- 逻辑：取最后14条，计算胜率/盈亏比/最大回撤/交易天数
- 输出：6个统计卡片（14天胜率、本月累计盈亏、平均盈亏比、最大回撤、交易日数、盈亏笔数）
- 硬性标准：胜率≥55%（绿色徽章），盈亏比≥2:1（橙色），回撤<15%（绿色）

### 2. `gen_section7_tracking_table(history, today_str)`
- 数据源：`strategy_history.json`（最后14条）
- 逻辑：生成10列表格
- 特殊处理：今日行加 `class="today-row"` + 橙色 TODAY 徽章
- 底部汇总：`✅ 盈利N笔 | ✗ 亏损N笔 | ⬛ 保本N笔 | ▶ 进行中1笔 | 14天胜率XX%`

### 3. `gen_section8_error_stats(history)`
- 数据源：`strategy_history.json`（最后14条）
- 分类统计：情绪化交易/追单/移动止损/未过清单/盈亏比<2:1
- 正确执行次数 = WIN + WIN_TP1 笔数
- 错误率 = 亏损笔数 / 总交易笔数 × 100%

### 4. `gen_section9_bars(history)`
- 数据源：`strategy_history.json`（最后14条）
- 每条记录 → 1根柱状图
- 颜色：绿色=盈利，红色=亏损，灰色=保本/观望
- 高度：WIN=75px高，LOSS=35px，SKIP=20px

### 5. `gen_section10_line(history)`
- 数据源：`strategy_history.json`（最后30条）
- 逻辑：从第1条到第N条逐步计算**累计胜率**，绘制 SVG 折线图
- X轴：4等分（Week1~Week4），Y轴：胜率 0~100%

### 6. `gen_section11_yesterday_review(prev_strategy, history, data, today_display)`
- 数据源：`prev_strategy.json`（昨日策略）+ 今日 API 价格数据
- 逻辑：见"自动复盘机制"
- 输出：复盘表格（币种/方向/入场价/SL触发/TP/盈亏/打分）
- 包含：最大失误 + 亮点 + 执行打分（★/☆）
- 底部附复盘依据价格区间

### 7. `gen_section12_week_review(history)`
- 数据源：`strategy_history.json`（最后7条）
- 汇总：本週交易次数/胜负/胜率/最大单笔盈亏/失误
- 底部：本周最大失误 + 下周唯一改进项

### 8. `gen_section13_month_review(history)`
- 数据源：`strategy_history.json`（全部近30天）
- **盈亏计算**（v2.2 修复）：
  - 有 `pnl` 字段 → 直接用
  - 无 pnl → WIN=+2.0R / WIN_TP1=+1.0R / LOSS=-1.0R / 其他=0
- 输出：6个卡片（本月累计盈亏/交易日数/胜率/盈亏比/最大回撤/胜负保）
- 硬性标准：胜率≥55%、盈亏比≥2:1、回撤<1.5R

---

## 【策略生成规则（`generate_strategy` 函数）】

### 信号维度与方向权重

| 维度 | 看多（+分） | 看空（+分） |
|------|-----------|-----------|
| 恐惧指数 < 30 + RSI < 40 | 超卖反弹机会（+20） | — |
| MACD 金叉 | 方向=LONG（+30） | — |
| MACD 死叉 | — | 方向=SHORT（+20） |
| 资金费率 < -0.01% | 做多加分（+10） | 做空加分（+10） |
| 价格 > EMA20 | 趋势偏多（+10） | — |
| 价格 < EMA20 | — | 趋势偏空（+10） |
| 价格 < EMA50 | — | 中期偏空（+10） |
| 价格触及布林下轨 | 超卖（+15） | — |
| 价格触及布林上轨 | — | 超买（-15） |

### 方向决策

- `confidence >= 40` 或 `>= 20` → 按信号方向（LONG/SHORT）
- 否则 → `WAIT`（观望）

### 关键价位计算

```
做多 LONG：
  进场区间 = [max(price*0.995, bb_middle), price]
  止损     = bb_lower（下轨）
  TP1      = min(price*1.035, ema20)
  TP2      = min(price*1.06, bb_upper)

做空 SHORT：
  进场区间 = [price*0.995, min(price*1.008, ema20)]
  止损     = max(price*1.018, bb_upper)
  TP1      = price*0.965
  TP2      = price*0.94
```

---

## 【Telegram 推送配置】

```python
Bot Token : 8626387493:AAE2XCzMzmhDiWRaGKVEjrj2EGLPsDN22-Q
Bot名称   : @MK_BTC_Alert_Bot
频道      : @bitebiwanglin（比特币王林公开频道）
Chat ID   : -1003189007280
配置文件  : btc/telegram_config.json
```

**时序要求**：必须等 Git push 完成后才推送，确保日报已在 GitHub Pages 上线。

---

## 【Git 管理规范】

```
仓库   : github.com/wanglin141319-bit/mk-trading
分支   : main
commit : feat: auto BTC daily report YYYYMMDD

⚠️ 每次 commit 前必须：
1. 检查文件大小 Get-Item 确认 Length > 0
2. 防止 commit 空文件（历史事故：commit 4c8d506 提交了 0 bytes 空文件）
```

---

## 【当你接手这个系统时】

### 永远遵守的规则

1. **不写虚构数据**。所有日报数字必须来自 API 或 JSON。
2. **昨日复盘永远是自动生成的**，基于当天价格 + 昨日策略判断，不是手动编的。
3. **当天行标记 `result=OPEN`**，等明天自动结算后才更新为真实结果。
4. **修改任何逻辑后必须验证**：运行 `python run_daily_report.py`，检查日报输出。
5. **Git commit 前检查文件大小**。
6. **每次修改后同步更新本手册**，保持版本一致。

### 常见任务操作指引

**Q: 要修改策略追踪表的列结构？**
→ 改 `gen_section7_tracking_table()` 函数中的 HTML 生成逻辑

**Q: 要增加新的技术指标？**
→ 在 `fetch_btc_data.py` 中添加 API 调用，在 `generate_strategy()` 中添加信号逻辑

**Q: 要修改月回顾的盈亏计算规则？**
→ 改 `gen_section13_month_review()` 中的 pnl_values 估算逻辑

**Q: 要修改模板样式？**
→ 改 `BTC_daily_report_20260415_PROFESSIONAL.html`，保持占位符位置不变

**Q: 策略历史数据有误，要手动修正？**
→ 直接编辑 `btc/cache/strategy_history.json`，下次生成日报时自动读取

---

## 【版本历史】

| 版本 | 日期 | 变更内容 |
|------|------|---------|
| v1.0 | 2026-04-15 | 初始16板块模板，策略追踪表7列 |
| v2.0 | 2026-04-18 | 策略追踪表升级为10列，彩色标签+TODAY徽章 |
| v2.1 | 2026-04-19 | 模板硬编码→占位符，8个动态生成函数，禁止虚构数据 |
| v2.2 | 2026-04-19 | gen_section13_month_review 盈亏计算：WIN=+2R/WIN_TP1=+1R/LOSS=-1R，新增最大回撤字段 |

---

> 📌 本手册与 `run_daily_report.py` 保持同步更新。
> 如有修改，请在版本历史中记录变更日期和内容。
