# BTC Daily Report Automation - btc-2

## 执行记录

### 2026-04-11
- 状态: ✅ 成功
- 报告: BTC_daily_report_20260411.html (#27)
- BTC 价格: $73,019 (OI: 96,867 BTC)
- F&G: 15 (Extreme Fear，极度恐惧持续)
- 资金费率 BTC/ETH: ~0%（多空均衡，无明显偏向）
- Git push: ✅

### 2026-04-10
- 状态: ✅ 成功
- 报告: BTC_daily_report_20260410.html (#26)
- BTC 价格: $72,171 (+1.62%)
- OI: 94,320 BTC (较昨日 +2,848 BTC)
- F&G: 16 (极度恐惧，连续第25日 ≤20)
- 资金费率 BTC: +0.0037% (多头付费)
- Git push: ✅ d23a225 → 1c13e5f
- 报告已插入 index.html 顶部

### 关键文件
- 生成器: btc/btc_report_generator.py
- 今日报告: btc/reports/BTC_daily_report_{YYYYMMDD}.html
- 报告索引: btc/index.html

### 技术说明
- 使用 managed Python 3.13.12 + requests
- 数据源: CoinGecko (价格) + Binance (OI/资金费率) + Alternative.me (F&G)
- 报告跳过逻辑: 如已存在今日报告则跳过
- 编码: sys.stdout.reconfigure(encoding="utf-8") 解决 Windows GBK 问题
- Git commit message: feat: Auto BTC daily {date}
- EXEC_NUM 每次运行前手动 +1（需改为自动追踪或持久化）
