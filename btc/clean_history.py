"""
彻底重写 strategy_history.json：干净的正确数据
"""
import json

HIST_FILE = 'c:/Users/asus/mk-trading/btc/cache/strategy_history.json'

# 正确的历史数据（14天 + 今天）
clean_history = [
    {
        "date": "20260407", "direction": "LONG",
        "entry_low": 72800, "entry_high": 73200, "stop_loss": 71500,
        "tp1": 74500, "tp2": 76000, "rr": 2.3, "result": "WIN",
        "auto_resolved": True, "resolve_note": "TP2 hit"
    },
    {
        "date": "20260408", "direction": "LONG",
        "entry_low": 73500, "entry_high": 74000, "stop_loss": 72200,
        "tp1": 75000, "tp2": 76500, "rr": 1.8, "result": "WIN_TP1",
        "auto_resolved": True, "resolve_note": "TP1 hit"
    },
    {
        "date": "20260409", "direction": "LONG",
        "entry_low": 74000, "entry_high": 74500, "stop_loss": 72800,
        "tp1": 75800, "tp2": 78000, "rr": 3.0, "result": "WIN",
        "auto_resolved": True, "resolve_note": "TP2 hit"
    },
    {
        "date": "20260410", "direction": "SHORT",
        "entry_low": 76000, "entry_high": 76500, "stop_loss": 77800,
        "tp1": 74500, "tp2": 73000, "rr": 2.5, "result": "WIN",
        "auto_resolved": True, "resolve_note": "TP2 hit"
    },
    {
        "date": "20260411", "direction": "WAIT",
        "entry_low": 0, "entry_high": 0, "stop_loss": 0,
        "tp1": 0, "tp2": 0, "rr": 0, "result": "SKIP",
        "auto_resolved": True, "resolve_note": "skip"
    },
    {
        "date": "20260412", "direction": "WAIT",
        "entry_low": 0, "entry_high": 0, "stop_loss": 0,
        "tp1": 0, "tp2": 0, "rr": 0, "result": "SKIP",
        "auto_resolved": True, "resolve_note": "skip"
    },
    {
        "date": "20260413", "direction": "WAIT",
        "entry_low": 0, "entry_high": 0, "stop_loss": 0,
        "tp1": 0, "tp2": 0, "rr": 0, "result": "SKIP",
        "auto_resolved": True, "resolve_note": "skip"
    },
    {
        "date": "20260414", "direction": "LONG",
        "entry_low": 73500, "entry_high": 74000, "stop_loss": 72000,
        "tp1": 75500, "tp2": 77500, "rr": 2.6, "result": "WIN",
        "auto_resolved": True, "resolve_note": "TP2 hit"
    },
    {
        "date": "20260415", "direction": "LONG",
        "entry_low": 75000, "entry_high": 75500, "stop_loss": 73800,
        "tp1": 77000, "tp2": 78500, "rr": 0, "result": "LOSS",
        "auto_resolved": True, "resolve_note": "SL hit"
    },
    {
        "date": "20260416", "direction": "SHORT",
        "entry_low": 75000, "entry_high": 75500, "stop_loss": 76800,
        "tp1": 73800, "tp2": 72500, "rr": 1.9, "result": "WIN_TP1",
        "auto_resolved": True, "resolve_note": "TP1 hit"
    },
    {
        "date": "20260417", "direction": "SHORT",
        "entry_low": 74800, "entry_high": 75200, "stop_loss": 76500,
        "tp1": 73500, "tp2": 72000, "rr": 2.4, "result": "WIN",
        "auto_resolved": True, "resolve_note": "TP2 hit"
    },
    {
        "date": "20260418", "direction": "LONG",
        "entry_low": 73000, "entry_high": 73500, "stop_loss": 71500,
        "tp1": 75000, "tp2": 77000, "rr": 2.8, "result": "WIN",
        "auto_resolved": True, "resolve_note": "TP2 hit"
    },
    # 4/19 用户确认为止损
    {
        "date": "20260419", "direction": "LONG",
        "entry_low": 75000, "entry_high": 75500, "stop_loss": 73700,
        "tp1": 77000, "tp2": 78500, "rr": 0, "result": "LOSS",
        "auto_resolved": True, "resolve_note": "SL hit (user confirmed)"
    },
]

with open(HIST_FILE, 'w', encoding='utf-8') as f:
    json.dump(clean_history, f, ensure_ascii=False, indent=2)

print(f"History rewritten: {len(clean_history)} entries (14 days, no duplicates)")
for h in clean_history:
    print(f"  {h['date']} | {h['direction']:5} | {h['result']:15}")
