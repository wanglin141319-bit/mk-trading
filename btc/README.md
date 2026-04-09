# MK Trading - BTC Analysis

GitHub Repo: https://github.com/wanglin141319-bit/mk-trading
Local Clone: C:/Users/asus/mk-trading

## BTC子网结构
- /btc/index.html          → 比特币行情分析机入口页（首页）
- /btc/reports/            → 每日报告HTML存放目录
- /btc/reports/BTC_daily_report_YYYYMMDD.html  → 每日日报

## 上传规范
每次生成日报后：
1. 将 BTC_daily_report_YYYYMMDD.html 复制到本地克隆仓库的 /btc/reports/ 目录
2. 更新 /btc/index.html 的报告列表（自动生成）
3. git add + git commit + git push

## GitHub Pages 访问路径
https://wanglin141319-bit.github.io/mk-trading/btc/
