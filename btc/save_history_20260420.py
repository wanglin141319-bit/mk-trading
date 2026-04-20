import json, os
cache_dir = r'C:\Users\asus\mk-trading\btc\cache'
os.makedirs(cache_dir, exist_ok=True)

history = [
    {"date":"20260407","direction":"LONG","entry_low":72800,"entry_high":73200,"stop_loss":71500,"tp1":74500,"tp2":76000,"rr":2.3,"result":"WIN","auto_resolved":True,"resolve_note":"TP2 hit"},
    {"date":"20260408","direction":"LONG","entry_low":73500,"entry_high":74000,"stop_loss":72200,"tp1":75000,"tp2":76500,"rr":1.8,"result":"WIN_TP1","auto_resolved":True,"resolve_note":"TP1 hit"},
    {"date":"20260409","direction":"LONG","entry_low":74000,"entry_high":74500,"stop_loss":72800,"tp1":75800,"tp2":78000,"rr":3.0,"result":"WIN","auto_resolved":True,"resolve_note":"TP2 hit"},
    {"date":"20260410","direction":"SHORT","entry_low":76000,"entry_high":76500,"stop_loss":77800,"tp1":74500,"tp2":73000,"rr":2.5,"result":"WIN","auto_resolved":True,"resolve_note":"TP2 hit"},
    {"date":"20260411","direction":"WAIT","entry_low":0,"entry_high":0,"stop_loss":0,"tp1":0,"tp2":0,"rr":0,"result":"SKIP","auto_resolved":True,"resolve_note":"skip"},
    {"date":"20260412","direction":"WAIT","entry_low":0,"entry_high":0,"stop_loss":0,"tp1":0,"tp2":0,"rr":0,"result":"SKIP","auto_resolved":True,"resolve_note":"skip"},
    {"date":"20260413","direction":"WAIT","entry_low":0,"entry_high":0,"stop_loss":0,"tp1":0,"tp2":0,"rr":0,"result":"SKIP","auto_resolved":True,"resolve_note":"skip"},
    {"date":"20260414","direction":"LONG","entry_low":73500,"entry_high":74000,"stop_loss":72000,"tp1":75500,"tp2":77500,"rr":2.6,"result":"WIN","auto_resolved":True,"resolve_note":"TP2 hit"},
    {"date":"20260415","direction":"LONG","entry_low":75000,"entry_high":75500,"stop_loss":73800,"tp1":77000,"tp2":78500,"rr":0,"result":"LOSS","auto_resolved":True,"resolve_note":"SL hit"},
    {"date":"20260416","direction":"SHORT","entry_low":75000,"entry_high":75500,"stop_loss":76800,"tp1":73800,"tp2":72500,"rr":1.9,"result":"WIN_TP1","auto_resolved":True,"resolve_note":"TP1 hit"},
    {"date":"20260417","direction":"SHORT","entry_low":74800,"entry_high":75200,"stop_loss":76500,"tp1":73500,"tp2":72000,"rr":2.4,"result":"WIN","auto_resolved":True,"resolve_note":"TP2 hit"},
    {"date":"20260418","direction":"LONG","entry_low":73000,"entry_high":73500,"stop_loss":71500,"tp1":75000,"tp2":77000,"rr":2.8,"result":"WIN","auto_resolved":True,"resolve_note":"TP2 hit"},
    {"date":"20260419","direction":"LONG","entry_low":75000,"entry_high":75500,"stop_loss":73700,"tp1":77000,"tp2":78500,"rr":0,"result":"BREAK_EVEN","auto_resolved":True,"resolve_note":"TP not hit"},
    {"date":"20260420","direction":"WAIT","entry_low":0,"entry_high":0,"stop_loss":0,"tp1":0,"tp2":0,"rr":0,"result":"OPEN","auto_resolved":False,"resolve_note":""},
]

hist_file = os.path.join(cache_dir, 'strategy_history.json')
with open(hist_file, 'w', encoding='utf-8') as f:
    json.dump(history, f, ensure_ascii=False, indent=2)
print('strategy_history.json saved:', len(history), 'entries')

prev = {"direction":"WAIT","confidence":15,"resistance":76241,"entry_low":73700,"entry_high":74300,"stop_loss":71500,"tp1":77000,"tp2":80000,"rr_ratio":0}
prev_file = os.path.join(cache_dir, 'prev_strategy.json')
with open(prev_file, 'w', encoding='utf-8') as f:
    json.dump(prev, f, ensure_ascii=False, indent=2)
print('prev_strategy.json saved')
