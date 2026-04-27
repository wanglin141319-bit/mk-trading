"""Telegram推送 - 2026-04-26"""
import requests, json

TOKEN = "8626387493:AAE2XCzMzmhDiWRaGKVEjrj2EGLPsDN22-Q"
CHAT_ID = "-1003189007280"

msg = (
    "*BTC Daily Report | 2026-04-26 (Sunday)*\n\n"
    "*Strategy: WAIT*\n\n"
    "- BTC: $77,505 (+0.02%)\n"
    "- RSI(14): 71.5 (Overbought)\n"
    "- MACD: Golden Cross (hist=183)\n"
    "- Fear Index: 33 (Fear)\n\n"
    "Key Levels:\n"
    "R2: $80,000 | R1: $79,597\n"
    "Current: $77,505\n"
    "S1: $74,890 | S2: $72,325\n\n"
    "Short Setup:\n"
    "Entry: $79,500-$80,000\n"
    "SL: $80,500 | TP1: $76,500 | TP2: $75,000\n"
    "R/R: 3:1\n\n"
    "FOMC 04-29: Keep positions small (<15% margin)\n\n"
    "14D Win Rate: 35.7% | Month: 9W-3L\n\n"
    "Link: https://mktrading.vip/btc/reports/BTC_daily_report_20260426.html"
)

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
data = {"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}
r = requests.post(url, data=data, timeout=15)
result = r.json()
print(result)
if result.get('ok'):
    print(f"Telegram sent successfully! message_id={result['result']['message_id']}")
else:
    print(f"Telegram error: {result.get('description', 'unknown')}")
