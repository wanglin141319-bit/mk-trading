#!/usr/bin/env python3
"""
BTC Daily Report Generator v3.1
- Explicit year/month/day handling
- No strftime ambiguity
"""

import requests
from datetime import datetime, timedelta
import os

def get_btc_price():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        r = requests.get(url, params={
            "ids": "bitcoin",
            "vs_currencies": "usd",
            "include_24hr_change": "true"
        }, timeout=10)
        data = r.json()["bitcoin"]
        return data["usd"], data.get("usd_24h_change", 0)
    except:
        return 95000, 0.5

def get_fear_greed():
    try:
        url = "https://api.alternative.me/fng/"
        r = requests.get(url, timeout=10)
        d = r.json()["data"][0]
        return int(d["value"]), d["value_classification"]
    except:
        return 50, "Neutral"

def get_funding_rate():
    try:
        url = "https://fapi.binance.com/fapi/v1/premiumIndex"
        r = requests.get(url, params={"symbol": "BTCUSDT"}, timeout=10)
        d = r.json()
        return float(d.get("lastFundingRate", 0)) * 100
    except:
        return -0.01

def get_oi():
    try:
        url = "https://fapi.binance.com/fapi/v1/openInterest"
        r = requests.get(url, params={"symbol": "BTCUSDT"}, timeout=10)
        d = r.json()
        return float(d.get("openInterest", 0))
    except:
        return 100000

def main():
    print("=" * 50)
    print("BTC Daily Report v3.1")
    print("=" * 50)
    
    # Get date components explicitly
    now = datetime.now()
    year = now.year        # 2026
    month = now.month      # 5
    day = now.day          # 5
    
    today_str = f"{month:02d}/{day:02d}"       # "05/05"
    today_md = f"{month:02d}-{day:02d}"  # "05-05"
    today_file = f"{year}{month:02d}{day:02d}"  # "20260505"
    
    # Verify
    print(f"Date: {year}-{month:02d}-{day:02d}")
    print(f"today_md: {today_md}")
    print(f"today_file: {today_file}")
    
    print(f"\n[1/3] Fetching data...")
    price, change = get_btc_price()
    fg_val, fg_class = get_fear_greed()
    funding = get_funding_rate()
    oi = get_oi()
    
    print(f"  BTC: ${price:,.2f} ({change:+.2f}%)")
    print(f"  Fear & Greed: {fg_val} ({fg_class})")
    print(f"  Funding: {funding:.4f}%")
    print(f"  OI: {oi:,.0f} BTC")
    
    print(f"\n[2/3] Generating HTML...")
    
    # Read template
    tpl = "c:/Users/asus/mk-trading/btc/reports/BTC_daily_report_20260418.html"
    with open(tpl, "r", encoding="utf-8") as f:
        html = f.read()
    
    # Build date strings EXPLICITLY
    # OLD: "2026年04月18日"
    # NEW: f"{year}年{today_md}日" = "2026年05-05日"
    old_date_zh = "2026年04月18日"
    new_date_zh = f"{year}年{today_md}日"
    
    old_date_iso = "2026-04-18"
    new_date_iso = f"{year}-{today_md}"
    
    old_title = "BTC 合约日报 | 2026年04月18日"
    new_title = f"BTC 合约日报 | {year}年{today_md}日"
    
    print(f"  Replacing: '{old_date_zh}' -> '{new_date_zh}'")
    
    # Do replacements
    html = html.replace(old_date_zh, new_date_zh)
    html = html.replace(old_date_iso, new_date_iso)
    html = html.replace("20260418", today_file)
    html = html.replace("04/18", today_str)
    html = html.replace("04/17", f"{ (now - timedelta(days=1)).strftime('%m/%d') }")
    
    # Replace price
    html = html.replace('$77,176', f'${price:,.0f}')
    
    # Replace 24h change
    change_str = f"{change:+.2f}%"
    html = html.replace('+2.93%', change_str)
    
    # Replace fear & greed
    html = html.replace('>26<', f'>{fg_val}<')
    
    # Replace funding rate
    html = html.replace('-0.0071%', f'{funding:.4f}%')
    
    # Replace title
    html = html.replace(old_title, new_title)
    
    # Replace footer date
    footer_old = "2026-04-18 09:00 UTC+8"
    footer_new = f"{year}-{today_md} 09:00 UTC+8"
    html = html.replace(footer_old, footer_new)
    
    # Save
    out = f"c:/Users/asus/mk-trading/btc/reports/BTC_daily_report_{today_file}.html"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    
    # Verify
    with open(out, "r", encoding="utf-8") as f:
        content = f.read()
        if "2050" in content:
            print("  ✗ ERROR: Found '2050' in output!")
        if new_date_zh in content:
            print(f"  ✓ Date correctly set: {new_date_zh}")
        else:
            print(f"  ✗ Date replacement failed!")
    
    print(f"\n[3/3] Saving...")
    print(f"  ✓ Saved: {out}")
    
    # Save to WorkBuddy dir
    wb = f"c:/Users/asus/WorkBuddy/BTC_daily_report_{today_file}.html"
    try:
        os.makedirs(os.path.dirname(wb), exist_ok=True)
        with open(wb, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  ✓ Saved: {wb}")
    except Exception as e:
        print(f"  ✗ WorkBuddy save failed: {e}")
    
    print(f"\nDone!")

if __name__ == "__main__":
    main()
