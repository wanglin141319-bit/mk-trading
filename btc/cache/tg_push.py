import requests

token = '8626387493:AAE2XCzMzmhDiWRaGKVEjrj2EGLPsDN22-Q'
chat_id = '-1003189007280'

lines = [
    "\U0001f4ca BTC \u65e5\u62a5 2026-04-24 | MK Trading v2.2",
    "",
    "\U0001f4b0 BTC $78,375 (-0.04% 24h)",
    "\U0001f4c9 ETH $2,332 (-1.69%) | SOL $86.20 (-0.73%)",
    "",
    "\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501",
    "\U0001f522 \u5e02\u573a\u6570\u636e",
    "\u2022 \u8d44\u91d1\u8d39\u7387: -0.0038% (\u7a7a\u4ed8\u591a)",
    "\u2022 OI: 99.3K BTC (\u2248$7.78B)",
    "\u2022 \u6050\u60e7\u8d2a\u5a6a: 39 Fear",
    "\u2022 \u591a\u7a7a\u6bd4: 40.2% (\u7a7a\u5934\u5360\u4f18)",
    "",
    "\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501",
    "\U0001f4c8 \u6280\u672f\u6307\u6807",
    "\u2022 RSI(14): 58.6 \u4e2d\u6027\u504f\u591a",
    "\u2022 MACD: \u91d1\u53c9",
    "\u2022 EMA: 7>20>50 \u591a\u5934\u6392\u5217",
    "\u2022 \u5e03\u6797\u5e26: 79,855 / 77,488 / 75,120",
    "",
    "\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501",
    "\U0001f3af \u4eca\u65e5\u7b56\u7565: \u505a\u591a",
    "\u2022 \u5165\u573a: \u56de\u8e29 $77,100-$77,500",
    "\u2022 \u6b62\u635f: $76,200 (2.8%)",
    "\u2022 TP1: $79,500 | TP2: $81,000",
    "\u2022 \u76c8\u4e8f\u6bd4: 2.7:1",
    "\u2022 \u7f6e\u4fe1\u5ea6: 60/100",
    "",
    "\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501",
    "\U0001f4cb \u6628\u65e5\u590d\u76d8 04-23",
    "LONG 76,500-77,000 | SL 75,750",
    "\u2192 \u89e6\u53d1\u4f46\u672a\u8fbe\u6b62\u76c8 (TP1=79,500\u672a\u89e6\u53ca)",
    "\u6267\u884c\u6253\u5206: 7/10",
    "",
    "\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501",
    "\U0001f4ca 14\u5929\u80dc\u7387: 50% (7\u80dc3\u8d1f4\u4fdd)",
    "\U0001f4c8 \u672c\u6708\u7d2f\u8ba1: +1910%",
    "\U0001f3c6 \u6708\u80dc\u7387: 52.9% | \u76c8\u4e8f\u6bd4: 2.2:1",
    "",
    "\u26a0\ufe0f \u5b8f\u89c2: 04-25 \u7279\u6717\u666e\u5173\u7a0e\u6f14\u8bb2(\u6781\u9ad8) | 04-29 FOMC | 05-02 \u975e\u519c",
    "\U0001f512 \u5173\u7a0e\u524d2h\u7981\u6b62\u5f00\u65b0\u4ed3",
    "",
    "\U0001f310 \u65e5\u62a5: https://mktrading.vip/btc/reports/BTC_daily_report_20260424.html",
]

text = "\n".join(lines)

url = f"https://api.telegram.org/bot{token}/sendMessage"
payload = {
    "chat_id": chat_id,
    "text": text,
    "disable_web_page_preview": True
}
r = requests.post(url, json=payload, timeout=15)
print("TG STATUS:", r.status_code)
print(r.json())
