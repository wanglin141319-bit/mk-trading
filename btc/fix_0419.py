"""手动修正 4/19 为 LOSS + 重新生成推送"""
import json
import subprocess
from datetime import datetime

HISTORY_FILE = 'c:/Users/asus/mk-trading/btc/cache/strategy_history.json'

with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
    history = json.load(f)

for h in history:
    if h['date'] == '20260419':
        print("=== 修正前 ===")
        print(json.dumps(h, ensure_ascii=False))
        h['result'] = 'LOSS'
        h['auto_resolved'] = False
        h['resolve_note'] = '用户确认为止损 | manual override - DO NOT OVERWRITE'
        h['pnl'] = -1800  # LONG $75,250 avg entry -> SL $73,700 = -$1,550 approx
        print("\n=== 修正后 ===")
        print(json.dumps(h, ensure_ascii=False))
        break

with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
    json.dump(history, f, indent=2, ensure_ascii=False)

print(f"\n[DONE] History saved, total {len(history)} entries")
