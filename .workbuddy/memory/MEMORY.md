# MK Trading 长期记忆

> 最后更新：2026-04-15

---

## BTC日报模板规范（最高优先级）

**模板文件**：`c:/Users/asus/mk-trading/btc/reports/BTC_daily_report_20260415_PROFESSIONAL.html`

**重要**：这是唯一正确的日报模板。每次生成新日报时：
1. **直接复制此文件的 HTML/CSS 结构**
2. **替换当天日期和真实API数据**
3. **禁止使用其他任何模板文件**

### 模板核心特征（必须严格遵守）
- 主色调：`#f7931a`（Bitcoin橙），背景深黑 `#0d1117`
- 布局：**固定grid布局**，禁止使用 `auto-fit grid` / `minmax` 自适应网格
- CSS架构：与 0414 报告一致，16个板块结构（区块标题 + 渐变装饰条 + 数字卡片）
- 所有数据必须来自**实时API**，禁止使用模拟/虚构数据
- 策略标签：`LONG` / `SHORT` / `NEUTRAL`，根据实际信号填写

### Git操作安全规范
- **每次 `git commit` 前必须确认文件 `Length > 0`**
- 使用 `Get-Item` 检查文件大小后再提交
- 参考：2026-04-15 事故（commit 4c8d506 提交了 0 bytes 空文件）

### 输出文件规范
- 本地存档：`c:/Users/asus/mk-trading/btc/reports/BTC_daily_report_YYYYMMDD.html`
- GitHub Pages：`https://mktrading.vip/btc/reports/`
- 同步更新 `btc/index.html` 存档摘要

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

_此文件为核心规范。遇到冲突时以此文件为准。_
