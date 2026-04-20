"""清理history重复条目 - 每个日期只保留最后一条"""
import json

HISTORY_FILE = 'c:/Users/asus/mk-trading/btc/cache/strategy_history.json'

with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
    history = json.load(f)

print(f"Before: {len(history)} entries")

# 去重：每个日期只保留最后一条
seen = {}
for h in history:
    d = h['date']
    seen[d] = h  # 后面的覆盖前面的

cleaned = list(seen.values())
# 按日期排序
cleaned.sort(key=lambda x: x['date'])

print(f"After:  {len(cleaned)} entries")
for h in cleaned:
    print(f"  {h['date']} {h.get('direction','')} {h.get('result','')}")

with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
    json.dump(cleaned, f, indent=2, ensure_ascii=False)

print("\n[DONE] History deduplicated.")
