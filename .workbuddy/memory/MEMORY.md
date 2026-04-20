# MK Trading 长期记忆

> 最后更新：2026-04-19

---

## BTC日报模板规范（最高优先级）

> **当前版本：v2.2**（2026-04-20 升级）
> **版本说明**：v2.2 在 v2.1 基础上修复了自动复盘逻辑的核心缺陷——**进场触发判断缺失**，新增 TRIGGERED_NO_TP 结果状态。

**参考文件**：`c:/Users/asus/mk-trading/btc/reports/BTC_daily_report_20260418.html`（v2.0基准文件）

**重要**：每次生成新日报时：
1. **以 20260418 报告为基准模板**，复制其 HTML/CSS 结构
2. **替换当天日期和真实API数据**
3. **禁止降级回旧版结构**

### 模板核心特征（必须严格遵守）
- 主色调：`#f7931a`（Bitcoin橙），背景深黑 `#0d0f14`
- 布局：**固定grid布局**，禁止使用 `auto-fit grid` / `minmax` 自适应网格
- CSS架构：16个板块结构（区块标题 + 渐变装饰条 + 数字卡片）
- 所有数据必须来自**实时API**，禁止使用模拟/虚构数据
- 策略标签：`LONG` / `SHORT` / `NEUTRAL`，根据实际信号填写

---

### 【v2.0 完整16板块结构】

| 序号 | 板块名称 | 说明 | 硬性标准 |
|------|----------|------|----------|
| 1 | 综合统计看板 | 14天胜率/本月盈亏/盈亏比/最大回撤/交易日数/盈利亏损笔数 | ✅ |
| 2 | 价格+市场数据 | 资金费率/OI/爆仓量/恐惧贪婪指数/多空持仓比 | - |
| 3 | 技术指标面板 | RSI/MACD/EMA20/布林带 | - |
| 4 | 今日合约操作策略 | 主方向标签+进场区间+SL+TP1+TP2+盈亏比评估 | ✅ |
| 5 | 资金流向 & 鲸鱼动向 | 大额流入流出/净流向/鲸鱼钱包数量变化 | - |
| 6 | 今日宏观事件时间线 | 时间线组件展示重要宏观事件 | - |
| 7 | **近14天策略追踪表** | **v2.0核心升级模块** | ✅ |
| 8 | 错误分类统计 | 情绪化/追单/移动止损/检查清单/盈亏比<2:1/正确执行 | ✅ |
| 9 | 近14天胜率柱状图 | 14根柱状图展示每日盈亏状态 | ✅ |
| 10 | 近30天胜率趋势折线图 | SVG折线图+面积填充 | ✅ |
| 11 | 昨日复盘 | 币种/方向/入场价/止损/止盈/盈亏/执行打分 | - |
| 12 | 本周综合复盘 | 本周交易次数/胜负/胜率/盈亏/最大单笔/亮点改进 | - |
| 13 | 月回顾统计 | 本月收益/交易日/胜率/盈亏比/回撤/失误 | ✅ |
| 14 | 当前持仓分布 | BTC/ETH/SOL持仓表格+浮动盈亏 | - |
| 15 | 英文 X 推文草稿 | X风格推文预览，含策略信号 | - |
| 16 | Footer | 报告编号/生成时间/免责声明 | - |

---

### 【v2.0 核心升级】近14天策略追踪表规范

**版本说明**：2026-04-18 按用户提供的参考图片重构，此为正式模板标准。

#### 表格列结构（共10列，固定）
| 列名 | 内容规范 |
|------|------|
| 日期 | MM/DD 格式，今日行加 TODAY 橙色徽章 |
| 方向 | 彩色标签色块：🟢多（dir-long）/ 🔴空（dir-short）/ 🟡观望（dir-wait） |
| 涨跌 | 当日BTC涨跌幅，正数绿色、负数红色 |
| 进场区间 | 区间格式，如 `$76,000–$76,500`，橙色显示 |
| 止损 SL | 红色显示 |
| TP1 | 绿色显示（第一目标位） |
| TP2 | 绿色显示（第二目标位） |
| 结果 | 五种彩色标签（见下方） |
| 盈亏比 | 如 `2.6:1`，止损行填 `-` |
| 错误分析 | 一句话，灰色小字 |

#### 结果标签五种样式（CSS class 对应）
- `rb-tp2`：✅ TP2达成（深绿背景）
- `rb-tp1`：✅ TP1达成（浅绿背景）
- `rb-sl`：✗ 方向错误止损（红色背景）
- `rb-skip`：⬛ 跳过（蓝色背景）
- `rb-open`：▶ 进行中（橙色背景，仅当天行使用）
- `rb-wait`：⬛ 等回踩未触发（黄色背景）

#### 今日行特殊处理
- 整行加 `class="today-row"`（橙色低透明度背景）
- 日期格式：`MM/DD` + `<span class="today-badge">TODAY</span>`（橙色实心徽章）
- 结果列：`rb-open` 标签，显示"▶ 进行中"
- 错误分析列：显示"等待策略区确认"

#### 近14天滚动规则
- **必须以报告日期为终点**，往前数14天动态滚动，不能固定在月初
- 底部汇总格式：`✅ 盈利N笔 | ✗ 亏损N笔 | ⬛ 保本/跳过N笔 | ▶ 进行中1笔 | 14天胜率XX% | 本月累计+X%`

---

### 输出文件规范
- 本地存档：`c:/Users/asus/mk-trading/btc/reports/BTC_daily_report_YYYYMMDD.html`
- GitHub Pages：`https://mktrading.vip/btc/reports/`
- 同步更新 `btc/index.html` 存档摘要

### Git 安全规范
- **每次 `git commit` 前必须确认文件 `Length > 0`**
- 使用 `Get-Item` 检查文件大小后再提交
- 参考：2026-04-15 事故（commit 4c8d506 提交了 0 bytes 空文件）

### 版本历史
| 版本 | 日期 | 主要变更 |
|------|------|------|
| v1.0 | 2026-04-15 | 初始16板块模板，策略追踪表为7列（日期/方向/入场价/结果/盈亏金额/盈亏比/执行打分） |
| v2.0 | 2026-04-18 | **在v1.0基础上升级**：策略追踪表重构为10列（日期/方向/涨跌/进场区间/SL/TP1/TP2/结果/盈亏比/错误分析），增加彩色方向标签、结果标签、TODAY徽章 |
| v2.1 | 2026-04-19 | **彻底修复虚构数据问题**：模板硬编码 → 占位符，7个动态生成函数全重构，数据100%来自真实API和strategy_history.json，auto_resolve逻辑固化 |
| v2.2 | 2026-04-20 | **修复自动复盘进场触发判断缺失**：新增三步判断（触发确认→SL/TP→TRIGGERED_NO_TP），区分"未触发"和"触发但未达止盈"，结果状态从5种→6种 |

### 模板占位符规范（v2.1）
模板 `BTC_daily_report_20260415_PROFESSIONAL.html` 中硬编码板块已全部替换为占位符：

| 占位符 | 对应板块 | 生成函数 |
|--------|----------|----------|
| `{{SECTION1_STATS}}` | 综合统计看板 | `gen_section1_stats()` |
| `{{SECTION7_TRACKING}}` | 近14天策略追踪表 | `gen_section7_tracking_table()` |
| `{{SECTION8_ERROR_STATS}}` | 错误分类统计 | `gen_section8_error_stats()` |
| `{{SECTION9_BARS}}` | 近14天胜率柱状图 | `gen_section9_bars()` |
| `{{SECTION10_LINE}}` | 近30天胜率趋势折线图 | `gen_section10_line()` |
| `{{SECTION11_YESTERDAY_REVIEW}}` | 昨日复盘 | `gen_section11_yesterday_review()` |
| `{{SECTION12_WEEK_REVIEW}}` | 本周综合复盘 | `gen_section12_week_review()` |
| `{{SECTION13_MONTH_REVIEW}}` | 月回顾统计 | `gen_section13_month_review()` |

### 自动复盘逻辑（v2.2 新增，2026-04-20 升级）
> **核心原则**：追踪表里的历史结果必须基于真实价格数据判断，禁止虚构。
> **v2.2 核心修复**：必须先判断"进场是否触发"，再判断SL/TP。"等回踩未触发"和"已触发但止损"是完全不同的两件事。

**自动复盘算法**（`auto_resolve_yesterday` 函数）：

#### 三步判断法（v2.2 严格版）
1. **进场触发确认**
   - 做多/做空：`low <= entry_high AND high >= entry_low` → 已触发
   - 若未触 → 直接 `BREAK_EVEN`（真正的"等回踩未触发"）
2. **若已触发 → 按优先级判断结果**
   - 多头：`low < SL` → LOSS | `high >= TP2` → WIN | `high >= TP1` → WIN_TP1 | 否则 → **TRIGGERED_NO_TP**
   - 空头：`high > SL` → LOSS | `low <= TP2` → WIN | `low <= TP1` → WIN_TP1 | 否则 → **TRIGGERED_NO_TP**
3. **新状态 TRIGGERED_NO_TP（v2.2新增）**
   - 含义：价格确实穿过了进场区间，但全天既没到TP也没破SL
   - 颜色：橙色(#ff9800)，标签："⚠️ 触发但未达止盈"
   - 与 BREAK_EVEN 的本质区别：BREAK_EVEN=没进场，TRIGGERED_NO_TP=进了场但在中间晃

**Telegram 时序**（v2.1 新增）：
- Step 8: Git push → Step 9: Telegram 推送
- 必须等 push 完成才推送，确保日报在 GitHub Pages 上可访问

---

## 项目结构

- 主仓库：`C:/Users/asus/mk-trading`（wanglin141319-bit/mk-trading）
- BTC日报目录：`btc/reports/`
- 自动化任务 ID：`mk-trading-b-t-c-1-0`

---

## MK 基本信息

- 交易：BTS/ETH/SOL 合约，主力 BTC
- 策略目标：胜率≥55%，盈亏比≥2:1
- 自媒体：币圈内容，Twitter/电报
- 偏好：结论先行、结构清晰、干脆直接
- 沟通：中文为主

---

## Polymarket 配置

- 推荐规模：50U 起步（Gas合理），理想 200U+
- 策略：气温/天气市场（10U可用）、事件驱动套利（50U+）
- Telegram：https://t.me/bitebiwang1413
- 频道：https://t.me/bitebiwanglin

---

## Telegram Bot 配置（2026-04-16）

- Bot：[@MK_BTC_Alert_Bot](https://t.me/MK_BTC_Alert_Bot)
- Token：`8626387493:AAE2XCzMzmhDiWRaGKVEjrj2EGLPsDN22-Q`
- Chat ID：`8167434886`（比特币王林）→ **已切换为频道**
- 频道：`@bitebiwanglin`（比特币王林公开频道，ID: -1003189007280）
- 配置文件：`c:/Users/asus/mk-trading/btc/telegram_config.json`
- 模块：`c:/Users/asus/mk-trading/btc/telegram_notify.py`
- 每天 10:25 定时推送日报 + 策略信号到频道

---

_此文件为核心规范。遇到冲突时以此文件为准。_
