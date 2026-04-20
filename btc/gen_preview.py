"""
预览版日报生成脚本 - 输出到 preview_YYYYMMDD.html，不覆盖正式文件
用法: python gen_preview.py
"""
import os
import sys
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPORTS_DIR = os.path.join(BASE_DIR, 'reports')
CACHE_DIR = os.path.join(BASE_DIR, 'cache')

sys.path.insert(0, BASE_DIR)

from run_daily_report import (
    fetch_all, load_cache, generate_strategy,
    load_history, auto_resolve_yesterday, generate_html
)
from datetime import datetime

def main():
    print("=" * 50)
    print("PREVIEW REPORT GENERATOR")
    print("=" * 50)

    # Step 1: 采集数据
    print("[1/5] Fetching data...")
    data = fetch_all()
    if not data.get('btc'):
        print("  -> Using cache...")
        data = load_cache()
        if not data:
            print("ERROR: No data available")
            return

    btc_price = data['btc'].get('price', 0)
    btc_change = data['btc'].get('change_24h', 0)
    print(f"  BTC: ${btc_price:,.0f} ({btc_change:+.2f}%)")

    # Step 2: 策略制定
    print("[2/5] Generating strategy...")
    strategy = generate_strategy(data)
    print(f"  Direction: {strategy['direction']}")
    print(f"  Entry: ${strategy['entry_low']:,.0f}-${strategy['entry_high']:,.0f}")
    print(f"  SL: ${strategy['stop_loss']:,.0f} | TP1: ${strategy['tp1']:,.0f} | TP2: ${strategy['tp2']:,.0f}")

    # Step 3: 加载历史 + 自动复盘
    print("[3/5] Loading history & auto-resolving...")
    history = load_history()
    
    prev_strat_file = os.path.join(CACHE_DIR, 'prev_strategy.json')
    prev_strategy = {}
    if os.path.exists(prev_strat_file):
        with open(prev_strat_file, 'r', encoding='utf-8') as f:
            prev_strategy = json.load(f)
    
    history = auto_resolve_yesterday(data, prev_strategy, history)
    print(f"  History entries: {len(history)}")

    # Step 4: 生成 HTML（不追加今日OPEN条目，用当前history直接生成预览）
    print("[4/5] Generating HTML preview...")
    html_content = generate_html(data, strategy, history)

    # Step 5: 保存为预览文件
    today_str = datetime.now().strftime('%Y%m%d')
    preview_path = os.path.join(REPORTS_DIR, f'preview_{today_str}.html')
    
    with open(preview_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    file_size = os.path.getsize(preview_path)
    print(f"[5/5] Preview saved!")
    print()
    print(f"  File: {preview_path}")
    print(f"  Size: {file_size:,} bytes ({file_size//1024}KB)")
    print()
    print("=" * 50)
    print("DONE - Open in browser to preview")
    print("=" * 50)
    
    return preview_path

if __name__ == '__main__':
    main()
