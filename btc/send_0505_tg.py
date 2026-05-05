#!/usr/bin/env python3
"""Send 20260505 report to Telegram (fixed)"""
import sys
import os
import requests
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))
from telegram_notify import send_message, send_document, load_config

config = load_config()
if not config:
    print("ERROR: No telegram config found")
    sys.exit(1)

bot_token = config['bot_token']
chat_id = str(config['chat_id'])

# Send text summary (plain text, no Markdown parsing issues)
msg = (
    "\u26a1 BTC Daily Report 05/05\n"
    "========================\n"
    "✅ Report #53 generated\n"
    "\U0001f4c4 Full report: https://mktrading.vip/btc/reports/BTC_daily_report_20260505.html\n"
    "\U0001f553 Next report: tomorrow 10:25 UTC+8\n"
    "========================\n"
    "\U0001f19a MK Trading Bot v3.1"
)

print("[TG] Sending message...")
ok, result = send_message(bot_token, chat_id, msg, parse_mode='')
if ok:
    print(f"[TG] Message sent: message_id={result}")
else:
    print(f"[TG] Message failed: {result}")

# Send HTML file (no caption to avoid Unicode issue)
report_path = os.path.join(os.path.dirname(__file__), 'reports', 'BTC_daily_report_20260505.html')
if os.path.exists(report_path):
    print(f"[TG] Sending document: {report_path}")
    # Use ASCII-only caption to avoid Unicode error
    caption = 'BTC Daily Report 2026-05-05 | MK Trading'
    doc_ok, doc_result = send_document(bot_token, chat_id, report_path, caption)
    if doc_ok:
        print(f'[TG] Document sent: message_id={doc_result}')
    else:
        print(f'[TG] Document failed: {doc_result}')
else:
    print(f'[TG] Report file not found: {report_path}')

print('[TG] Done.')
