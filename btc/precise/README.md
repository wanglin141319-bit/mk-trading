# BTC 日报 · 精准版 —— 系统规范

> 版本：v1.0（2026-10-04 建立）
> 入口：`btc/run_daily_report.py`（转发器） → `btc/precise/run_precise_daily.py`（主程序）
> 网站：https://mktrading.vip/btc/

---

## 0. 系统概览

```
Windows 计划任务（每天 10:25）
        ↓
btc/run_daily_report.py          ← 转发器（旧版已弃用，保留备份 .bak-20261004）
        ↓
btc/precise/run_precise_daily.py ← 主程序
        ↓
① 抓取 Gate.io 实时数据     ② 计算标准口径指标
③ 复盘历史策略 → 胜率        ④ 生成 HTML 日报
        ↓
btc/reports/BTC_daily_report_YYYYMMDD.html   ← 报告文件
btc/index.html                                ← 报告列表（自动置顶）
        ↓
git add → commit → push origin main           ← 发布到 GitHub Pages
        ↓
https://mktrading.vip/btc/reports/BTC_daily_report_YYYYMMDD.html
```

私密数据（不发布）：策略日志存于 `mk-trading/.workbuddy/btc_precise/strategy_log.json`
（`.workbuddy/` 已被 `.gitignore` 排除，**本仓库为 PUBLIC，严禁提交**）。

---

## 一、数据与提示词要求（铁律）

### 1.1 数据源（本机实测唯一可用通道）

| 数据项 | 来源 | 状态 |
|---|---|---|
| 现货价 / 24h 涨跌 / 24h 高低 / 成交量 | Gate.io `/spot/tickers?currency_pair=BTC_USDT` | ✅ |
| 合约价 / Mark / 指数 / 资金费率 | Gate.io `/futures/usdt/tickers?contract=BTC_USDT` | ✅ |
| K 线（1d / 4h / 1h） | Gate.io `/futures/usdt/candlesticks` | ✅ |
| 真实 OI + 账户多空比 + 主动买卖比 + 强平 | Gate.io `/futures/usdt/contract_stats` | ✅ |
| 恐惧与贪婪指数 | `api.alternative.me/fng` | ✅ |
| ~~Binance / Bybit / OKX / Bitget / CoinGecko~~ | — | ❌ 全部超时，**禁用** |

> ⚠️ **禁止**再把 Binance 当主数据源（旧版就是这么错的，一直在走降级路径）。

### 1.2 价格自洽铁律

1. **单一价格基准**：全篇所有价位必须来自同一时点快照。
2. **策略价位必须贴现价**：做多入场 = 现价 0 ~ −1%；做空入场 = 现价 0 ~ +1%。
   **禁止出现偏离现价 >3% 的入场价**（旧版出现 +17% 的入场价，即为模板残留）。
3. **禁止模板残留**：不得沿用任何固定示例数字。
4. **禁止编造**：抓不到写 `N/A`，不许用「估算值」冒充。
5. **标签必须准确**：
   - 「强平/爆仓」= 实际强平量，**不能**拿多空比顶替；
   - 「OI」= 合约持仓**张数**（1 张 = `quanto_multiplier` = 0.0001 BTC），**不能**拿账户多空比顶替；
   - 「大户多空比」与「全局账户多空比」是两个指标，分开标注。
6. 每个关键数值标注来源与抓取时间（UTC+8）。

### 1.3 指标计算口径

| 指标 | 正确口径 | 旧版错误 |
|---|---|---|
| RSI(14) | **Wilder 平滑**（指数平滑），非简单算术平均 | 用简单平均 |
| MACD(12,26,9) | 金叉/死叉 = **柱状图穿越零轴的交叉事件** | 用「柱 > 0」当金叉 → 方向判反 |
| 布林带(20,2) | 20 周期 SMA ± 2 倍标准差 | 同 |
| EMA | 日线 EMA20/50/200、4H EMA20/50、1H EMA20/50 | 用了模板残留值 |
| 支撑/阻力 | **摆动高低点**（swing high/low，左右各 3 根确认） | 直接用 24h 高低点 |
| 多周期 | 日线定方向 → 4H 定结构 → 1H 定入场 | 只用日线 |

### 1.4 策略生成规则

- 多空打分：日线 EMA/结构（权重 2）、MACD（1）、4H 结构（1）、资金费率（1）、恐惧贪婪（1）。
- 方向判定：`多 ≥ 空+3 → LONG`；`空 ≥ 多+3 → SHORT`；`|多−空| ≤ 1 → WAIT`；否则按多数方向（信心中）。
- **硬约束**：入场贴现价；止损/止盈基于真实结构位；盈亏比目标 ≥ 2:1。
- 指标矛盾、周期不共振 → **必须输出「观望 WAIT」**，不许硬凑方向。

### 1.5 策略追踪与胜率

- 每日策略写入 `strategy_log.json`（含日期/方向/入场区间/SL/TP1/TP2/时间戳）。
- **自动复盘**：用 1H K 线逐根检查 —— 先触止损判 `LOSS`，先触 TP1 判 `WIN`
  （同一根 K 线内两者都触及 → 保守判 `LOSS`）；72 根（约 3 天）未触及 → `EXPIRED`，不计入胜率。
- 胜率 = WIN / (WIN + LOSS)，展示在报告「策略追踪」区块。

---

## 二、版面要求（HTML 报告）

- **风格**：深色卡片式（`--bg:#0d0f14` / `--card:#141720` / 主色 `#f7931a` 比特币橙）。
- **适配**：手机优先，单列，`max-width:760px` 居中；字号 14px / 行高 1.65。
- **颜色语义（中国习惯）**：**涨/盈利 = 红 `#ff4d4f`**，**跌/亏损 = 绿 `#26c97f`**，观望 = 金 `#f7931a`。
- **区块顺序（固定）**：
  1. 头部（标题 #编号 / 日期 / 现价大字 / 24h 涨跌 / 24h 高低 / Mark & 指数 / 同源校验徽章 / 抓取时间）
  2. 近 30 日走势（内联 SVG 折线 + 渐变填充）
  3. 关键价位（R2 / R1 / 现价 / S1 / S2 阶梯）
  4. 技术指标面板（日线 / 4H / 1H 三行表格）
  5. 资金面（资金费率 / OI / 账户多空比 / 主动买卖比 / 强平多空）
  6. 情绪面（恐惧贪婪 + 昨日 / 7 日均）
  7. 综合研判（信号清单 + 多空评分 + 方向）
  8. **交易计划**（方向 / 信心 / 仓位 + 入场 / SL / TP1 / TP2 / 盈亏比 / 杠杆 + 触发 + 失效）
  9. **策略追踪**（已结算 / 胜负数 / 胜率 + 最近 7 条明细）
  10. 英文 X 文案（社媒用）
  11. 风险提示
  12. 页脚（生成时间 + 数据源）
- **技术要求**：单文件、无外部依赖（除系统字体）；`<div>` 标签必须闭合；不得出现 `undefined` / `None`。

---

## 三、网站发布要求

### 3.1 仓库与路径

- 仓库：`https://github.com/wanglin141319-bit/mk-trading`（**PUBLIC**）
- 站点：GitHub Pages → `mktrading.vip`
- 报告路径：`btc/reports/BTC_daily_report_YYYYMMDD.html`（**文件名必须保持此格式**，URL 才稳定）

### 3.2 index.html 列表更新

- 文件：`btc/index.html`，插入锚点：`<div class="reports-grid">`
- 卡片结构（**必须完全一致**）：
  ```html
  <a href="reports/BTC_daily_report_YYYYMMDD.html" class="report-card fade-in">
  <div class="report-date">YYYY-MM-DD</div>
  <div class="report-title">BTC Daily Report · #编号</div>
  <div class="report-summary en-content">BTC $价格. Strategy: LONG|SHORT|WAIT.</div>
  <div class="report-summary zh-content">BTC $价格。策略：做多|做空|观望。</div>
  <div><span class="report-tag bull|bear|neutral">LONG|SHORT|WAIT</span></div>
  </a>
  ```
- **编号规则**：今日卡片已存在 → 复用其编号；否则取页面最大编号 +1。
- **置顶规则**：新卡片插入到 `reports-grid` 之后（列表最顶部）。
- **幂等**：同日重复运行 → **整体替换**当日卡片，不重复插入。
- ⚠️ tag 必须用 `bull` / `bear` / `neutral`（站点 CSS 只定义了这三个；
  **旧版用的 `short` 类没有样式**，属遗留 bug）。

### 3.3 Git 发布流程

1. **安全前置检查**：`git status --porcelain` 中出现 `.workbuddy` / `.codebuddy` → **立即中止**（PUBLIC 仓库）。
2. `git add btc/reports/ btc/index.html btc/precise/ btc/run_daily_report.py`
3. `git commit -m "auto: BTC日报 YYYYMMDD"`
4. `git push origin HEAD:main`
5. 失败时保留本地文件，打印错误，不抛出（报告本地已生成）。

### 3.4 冲突处理（重要）

- Windows 计划任务原先 10:25 调用 `btc/run_daily_report.py`（旧版）。
- 现已把该文件改为**转发器**，转调 `precise/run_precise_daily.py`，
  因此**旧任务无需改动即可产出精准版**。
- 旧版源码备份：`btc/run_daily_report.py.bak-20261004`（如需回滚，改回原名即可）。

---

## 四、运维手册

```bash
# 正式运行（生成 + 发布）
python C:/Users/asus/mk-trading/btc/precise/run_precise_daily.py

# 只生成不推送
python .../run_precise_daily.py --no-push

# 完全演练（不碰 git）
python .../run_precise_daily.py --dry-run

# 补跑指定日期（用于回填）
python .../run_precise_daily.py --date 20261004
```

- 解释器：`C:/Users/asus/.workbuddy/binaries/python/versions/3.13.12/python.exe`
- 依赖：`requests`（已装）；`urllib3` 关闭证书告警。
- 日志：stdout，`[DONE]` 表示成功。
- 私密日志：`mk-trading/.workbuddy/btc_precise/strategy_log.json`

---

## 五、变更记录

| 日期 | 版本 | 变更 |
|---|---|---|
| 2026-10-04 | v1.0 | 新建精准版流水线；数据源切至 Gate.io；修正 MACD/RSI 口径、价格自洽、OI/强平标签；新增策略追踪与胜率；旧脚本改为转发器 |

---

*本规范与 `run_precise_daily.py` 同步维护：改脚本必改此文档，反之亦然。*
