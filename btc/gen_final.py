"""
生成最终版日报 + Git Push
- 删除旧的 20260420 正式版（如果有）
- 用最新代码重新生成
- Git commit + push 到 GitHub Pages
"""
import os, sys, json, time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPORTS_DIR = os.path.join(BASE_DIR, 'reports')
CACHE_DIR = os.path.join(BASE_DIR, 'cache')
TEMPLATE_FILE = os.path.join(REPORTS_DIR, 'BTC_daily_report_20260415_PROFESSIONAL.html')

sys.path.insert(0, BASE_DIR)
from run_daily_report import (
    fetch_all, load_cache, generate_strategy,
    load_history, auto_resolve_yesterday, generate_html,
    save_history, git_commit_push,
    notify_telegram, log
)
from datetime import datetime
import shutil

# ===== Step 0: 清理旧文件 =====
today_str = datetime.now().strftime('%Y%m%d')
today_file = os.path.join(REPORTS_DIR, f'BTC_daily_report_{today_str}.html')
preview_file = os.path.join(REPORTS_DIR, f'preview_{today_str}.html')

if os.path.exists(today_file):
    os.remove(today_file)
    print(f"Removed old: {today_file}")

# ===== Step 1: 采集数据 =====
print("[1/6] Fetching data...")
data = fetch_all()
if not data.get('btc'):
    print("  Using cache...")
    data = load_cache()
    if not data:
        print("ERROR: No data!")
        sys.exit(1)

btc_price = data['btc'].get('price', 0)
print(f"  BTC: ${btc_price:,.0f} ({data['btc'].get('change_24h', 0):+.2f}%)")

# ===== Step 2: 策略 =====
print("[2/6] Generating strategy...")
strategy = generate_strategy(data)
print(f"  Direction: {strategy['direction']} | Entry: ${strategy['entry_low']:,.0f}-${strategy['entry_high']:,.0f}")
print(f"  SL: ${strategy['stop_loss']:,.0f} | TP1: ${strategy['tp1']:,.0f} | TP2: ${strategy['tp2']:,.0f}")

# ===== Step 3: 历史 + 自动复盘 =====
print("[3/6] Loading history & auto-resolve...")
history = load_history()

prev_strat_file = os.path.join(CACHE_DIR, 'prev_strategy.json')
prev_strategy = {}
if os.path.exists(prev_strat_file):
    with open(prev_strat_file, 'r', encoding='utf-8') as f:
        prev_strategy = json.load(f)

history = auto_resolve_yesterday(data, prev_strategy, history)
print(f"  History: {len(history)} entries")

# ===== Step 4: 保存策略到 cache（明天复盘用）=====
with open(prev_strat_file, 'w', encoding='utf-8') as f:
    json.dump(strategy, f, ensure_ascii=False, indent=2)

# 追加今日OPEN条目到history
new_entry = {
    'date': today_str,
    'direction': strategy['direction'],
    'entry_low': strategy['entry_low'],
    'entry_high': strategy['entry_high'],
    'stop_loss': strategy['stop_loss'],
    'tp1': strategy['tp1'],
    'tp2': strategy['tp2'],
    'rr': strategy['rr_ratio'],
    'result': 'OPEN',
    'auto_resolved': False,
    'resolve_note': '',
}
history.append(new_entry)
if len(history) > 30:
    history = history[-30:]
save_history(history)
print(f"  Today's strategy saved as OPEN entry")

# ===== Step 5: 生成 HTML + 保存 =====
print("[4/6] Generating final HTML...")
html_content = generate_html(data, strategy, history)

with open(today_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

file_size = os.path.getsize(today_file)
print(f"  Saved: {today_file} ({file_size:,} bytes / {file_size//1024}KB)")

# 安全检查
if file_size == 0:
    print("ERROR: File is EMPTY! Aborting git push.")
    sys.exit(1)

# 复制预览版也更新一份
shutil.copy2(today_file, preview_file)
print(f"  Preview updated: {preview_file}")

# ===== Step 6: Git Commit + Push =====
print("[5/6] Git commit & push...")
git_result = git_commit_push(today_file)
print(f"  Git: {git_result}")

# ===== Step 7: Telegram 通知 =====
print("[6/6] Sending to Telegram...")
try:
    tg_result = notify_telegram(data, strategy, today_file)
    print(f"  Telegram: {tg_result}")
except Exception as e:
    print(f"  Telegram error (non-fatal): {e}")

elapsed_time = time.time() - time.time()
print()
print("=" * 55)
print(f"DONE! Final report generated and pushed.")
print(f"File: {today_file}")
print(f"Online: https://mktrading.vip/btc/reports/BTC_daily_report_{today_str}.html")
print("=" * 55)
