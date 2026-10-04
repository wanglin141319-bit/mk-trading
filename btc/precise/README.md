# BTC 日报 · 精准版 —— 系统规范

> 版本：v1.1（2026-10-04 更新）
> 主程序：`btc/precise/run_precise_daily.py`
> 推送模块：`btc/precise/telegram_push.py`
> 网站：https://mktrading.vip/btc/
> 频道：https://t.me/bitebiwanglin

---

## 0. 系统概览

```
Windows 计划任务 BTC_Daily_Report_Auto（每天 10:25）
WorkBuddy 自动化「BTC 精准日报」（每天 09:30）
        ↓
btc/precise/run_precise_daily.py    ← 主程序（唯一入口）
        ↓
① 抓取 Gate.io 实时数据      ② 计算标准口径指标
③ 复盘历史策略 → 胜率         ④ 生成 HTML 日报
        ↓
btc/reports/BTC_daily_report_YYYYMMDD.html   ← 报告文件
btc/index.html                                ← 报告列表（自动置顶）
        ↓
git add → commit → push origin main           ← 发布到 GitHub Pages
        ↓
telegram_push.py → 频道 @bitebiwanglin         ← 推送（需本地代理）
```

**私密数据（严禁发布）**，全部存于 `mk-trading/.workbuddy/btc_precise/`：

| 文件 | 内容 |
|---|---|
| `strategy_log.json` | 每日策略记录 + 复盘结果 |
| `telegram_config.json` | Bot Token / 目标 chat_id / 代理 |
| `push_state.json` | 推送幂等状态（记录已推送日期） |

> 🔴 `.workbuddy/` 已被 `.gitignore` 排除。**本仓库为 PUBLIC，严禁提交其中任何文件。**

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

### 3.3 页面框架自动维护（`fix_page_chrome`）

历史脚本在 `index.html` 留下过两类坏结构，脚本每日自动修复：

1. `<body>` 之后**未被 `<ul>` 包裹的孤儿 `<li>`** → 浏览器会渲染到页面左上角（即用户看到的「5 月 4 日日报」）。
2. 「View Today's Analysis」CTA 按钮 href 硬编码停留在旧日期 → 自动改为指向当日报告。

### 3.4 Git 发布流程

1. **安全前置检查**：`git status --porcelain` 中出现 `.workbuddy` / `.codebuddy` → **立即中止**（PUBLIC 仓库）。
2. `git add btc/reports/ btc/index.html btc/precise/`
3. `git commit -m "auto: BTC日报 YYYYMMDD"`
4. `git push origin HEAD:main`
5. 失败时保留本地文件，打印错误，不抛出（报告本地已生成）。

> 调度：Windows 计划任务 `BTC_Daily_Report_Auto` 已**直接指向** `precise/run_precise_daily.py`
> （旧的转发器 `btc/run_daily_report.py` 已删除；旧版源码备份 `run_daily_report.py.bak-20261004` 保留在本机，未入库）。

---

## 四、Telegram 推送要求

### 4.1 目标与身份

| 项目 | 值 |
|---|---|
| Bot | `@MK_BTC_Alert_Bot`（id 8626387493） |
| 目标频道 | **比特币王林公开频道** `@bitebiwanglin`（id `-1003189007280`） |
| 凭证文件 | `.workbuddy/btc_precise/telegram_config.json`（**私密，绝不入库**） |

### 4.2 配置格式

```json
{
  "bot_token": "123456:ABC...",
  "chat_ids": ["-1003189007280"],
  "proxy": "http://127.0.0.1:33210",
  "enabled": true,
  "attach_html": false
}
```

- **`chat_ids` 为数组 → 群发**：可同时填频道、群组、私聊（各自的 chat_id），一次推送全部送达。
- `proxy`：留空则自动探测；本机实测可用端口为 clash 的 `33210`(HTTP) / `33211`(SOCKS5)。
- `attach_html: true` → 额外把 HTML 报告作为文件附件发送（默认关闭，频道阅读以文本卡片为主）。

### 4.3 网络要求（关键）

> ⚠️ **Telegram API 在本机直连不可达**（`api.telegram.org` 直连/沙箱代理均超时）。
> 必须经**本地代理**（clash）转发。脚本按以下顺序自动解决：
> 1. 用配置里的 `proxy`（若实测可达）；
> 2. 否则扫描常见代理端口（`33210/33211/7890/7897/10809/1080/2080/4780…`）并逐个实测；
> 3. 均不可用 → 记 WARN 并跳过推送（**不影响报告生成与网站发布**）。

### 4.4 幂等规则（重要）

你有两个调度入口（Windows 10:25 + WorkBuddy 09:30），若不做处理频道每天会收到**两条重复推送**。

- `push_state.json` 记录 `last_date`；同一日期再次运行时 → **跳过推送**。
- 仅在**至少一个目标发送成功**时才写入状态（失败允许下次重试）。
- 需要手动重发（如修正内容后）→ 加 `--tg-force`。

### 4.5 消息格式规范

- 解析模式：**HTML**（`<b>` / `<i>`），必须对 `&` `<` `>` 做转义（模块内 `_esc()` 已处理）。
- 固定结构：标题（#编号 · 日期）→ 分隔线 → 现价与涨跌（🟢/🔴 + ▲/▼）→ RSI/MACD → 恐惧贪婪 + 资金费 → OI → 今日策略（方向/入场/SL/TP1/TP2/盈亏比/仓位）→ 多空评分 → 触发/失效 → 完整日报链接 → 历史胜率 → 署名分隔线。
- 颜色与符号语义：涨用 🟢▲、跌用 🔴▼；多 = 🟢、空 = 🔴、观望 = 🟡。
- 链接指向**当日线上报告**，因此推送必须在 **git 发布成功之后**执行（避免发出无效链接）。

### 4.6 安全要点

- **Token 只存在于私密配置文件中**，任何情况下不得写入仓库内文件、日志或提交历史。
- 历史上 Token 曾随 `btc/telegram_config.json` 泄露于 PUBLIC 仓库（2026-04-16 起）。
  **在 BotFather 执行 `/revoke` 换新 Token 后**，只需更新私密配置里的 `bot_token` 字段即可，
  脚本无需改动：

  ```bash
  python -c "import json,io; p=r'C:/Users/asus/mk-trading/.workbuddy/btc_precise/telegram_config.json'; c=json.load(open(p,encoding='utf-8')); c['bot_token']='新Token'; json.dump(c,open(p,'w',encoding='utf-8'),ensure_ascii=False,indent=2)"
  ```

---

## 五、运维手册

```bash
PY=C:/Users/asus/.workbuddy/binaries/python/versions/3.13.12/python.exe

# 正式运行（生成 + 发布网站 + 推送频道）
$PY C:/Users/asus/mk-trading/btc/precise/run_precise_daily.py

# 只生成，不推送任何地方
$PY .../run_precise_daily.py --no-push

# 完全演练（不碰 git / Telegram）
$PY .../run_precise_daily.py --dry-run

# 生成并发布网站，但不推 Telegram
$PY .../run_precise_daily.py --no-tg

# 强制重发今日推送到频道（忽略幂等）
$PY .../run_precise_daily.py --tg-force

# 补跑指定日期（回填）
$PY .../run_precise_daily.py --date 20261004

# Telegram 模块自检（只读，不发消息）
$PY C:/Users/asus/mk-trading/btc/precise/telegram_push.py --check

# Telegram 连通性测试（会向所有目标发一条测试消息）
$PY .../telegram_push.py --test
```

- 解释器：`C:/Users/asus/.workbuddy/binaries/python/versions/3.13.12/python.exe`
- 依赖：`requests`（已装）；`urllib3` 关闭证书告警。
- 日志：stdout，`[DONE]` 表示成功；各步骤带 `[OK]/[WARN]/[ERROR]/[SKIP]` 标签。
- 私密目录：`mk-trading/.workbuddy/btc_precise/`

---

## 六、变更记录

| 日期 | 版本 | 变更 |
|---|---|---|
| 2026-10-04 | v1.0 | 新建精准版流水线；数据源切至 Gate.io；修正 MACD/RSI 口径、价格自洽、OI/强平标签；新增策略追踪与胜率；旧脚本改为转发器 |
| 2026-10-04 | v1.1 | ① 计划任务直接指向新脚本，删除旧转发器；② 修复 index.html 孤儿 `<li>` 与 CTA 硬编码；③ **新增 Telegram 推送**（@bitebiwanglin 频道、本地代理自动探测、多目标群发、当日幂等）；④ 清理仓库历史遗留文件 |

---

*本规范与 `run_precise_daily.py` / `telegram_push.py` 同步维护：改脚本必改此文档，反之亦然。*
