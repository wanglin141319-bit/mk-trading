import requests

TOKEN = '8626387493:AAE2XCzMzmhDiWRaGKVEjrj2EGLPsDN22-Q'
CHAT = '-1003189007280'

msg = """📊 BTC 合约日报 #44 | 2026-04-27

💰 BTC: $79,306 (+2.28% 24h)
🔷 ETH: $2,396 (+3.14%)

📈 技术信号:
• RSI(14): 43.0 中性
• 资金费率: -0.0213%（空头付多头）
• OI: $7.64B | 多空比 0.737

🎯 今日策略: 观望（等回踩）
📍 入场区间: $76,000–$76,500
🛑 止损: $75,000
🎯 TP1: $79,500 | TP2: $81,000
⚖️ 盈亏比: 3:1

⚠️ 本周最大宏观风险:
04-29（周三）FOMC利率决议
公布前建议减少新开仓！

📉 本月统计:
胜率 45% | 盈亏比 2.6:1
本月累计: -2986.0R

🔗 https://mktrading.vip/btc/reports/BTC_daily_report_20260427.html"""

url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
r = requests.post(url, data={'chat_id': CHAT, 'text': msg}, timeout=15)
print('TG Status:', r.status_code)
print('TG Response:', r.text[:500])
