#!/usr/bin/env python3
# fix_0501_record.py - 修正05/01策略复盘标记

with open('btc/reports/BTC_daily_report_20260502.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 查找05/01那行的内容
idx = content.find('05/01')
if idx >= 0:
    snippet = content[idx:idx+800]
    print("找到05/01，附近内容：")
    print(snippet[:400])
    print("...")
else:
    print("未找到05/01")
