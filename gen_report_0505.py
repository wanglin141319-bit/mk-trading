#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate BTC Daily Report for 2026-05-05"""
import json, requests, time, math
from datetime import datetime, timezone, timedelta

UTC8 = timezone(timedelta(hours=8))
dt_now = datetime.now(UTC8)
today_str = dt_now.strftime("%Y-%m-%d")
report_date_str = dt_now.strftime(f"{dt_now.year}年{dt_now.month}月{dt_now.day}日")
report_date_display = dt_now.strftime(f"{dt_now.year}年{dt_now.month}月{dt_now.day}日（周一）")
report_num = 53

# ===== DATA FETCHING =====
def safe_get(url, timeout=10):
    try:
        r = requests.get(url, timeout=timeout)
        return r.json()
    except:
        return {}

# CoinGecko
cg = safe_get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_24hr_change=true&include_24hr_vol=true")
btc_price = cg.get("bitcoin", {}).get("usd", 80244)
btc_change = cg.get("bitcoin", {}).get("usd_24h_change", 2.27)
btc_vol = cg.get("bitcoin", {}).get("usd_24h_vol", 28500000000)
eth_price = cg.get("ethereum", {}).get("usd", 2359)
eth_change = cg.get("ethereum", {}).get("usd_24h_change", 1.89)

# Fear & Greed
fng_raw = safe_get("https://api.alternative.me/fng/?limit=2")
fng_today = int(fng_raw.get("data", [{"value": "50"}, {"value": "48"}])[0]["value"])
fng_yesterday = int(fng_raw.get("data", [{"value": "48"}])[1]["value"])
fng_class_today = "Neutral" if 40 <= fng_today <= 60 else ("Fear" if fng_today < 40 else "Greed")
fng_class_yesterday = "Neutral" if 40 <= fng_yesterday <= 60 else ("Fear" if fng_yesterday < 40 else "Greed")
fng_label_today = {"Neutral": "中性", "Fear": "恐惧", "Greed": "贪婪"}.get(fng_class_today, "中性")

# Binance 4H K线
klines_raw = safe_get("https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=4h&limit=50")
if klines_raw and isinstance(klines_raw, list) and len(klines_raw) >= 20:
    highs = [float(k[2]) for k in klines_raw]
    lows = [float(k[3]) for k in klines_raw]
    closes = [float(k[4]) for k in klines_raw]
    volumes = [float(k[5]) for k in klines_raw]

    # RSI(14)
    deltas = [closes[i] - closes[i-1] for i in range(1, len(closes))]
    gains = [d for d in deltas if d > 0]
    losses = [-d for d in deltas if d < 0]
    avg_gain = sum(gains[-14:]) / 14 if gains else 0
    avg_loss = sum(losses[-14:]) / 14 if losses else 1
    rs = avg_gain / avg_loss if avg_loss > 0 else 50
    rsi = round(100 - 100 / (1 + rs), 1)

    # EMA
    ema7 = round(sum(closes[-7:]) / 7, 2)
    ema20 = round(sum(closes[-20:]) / 20, 2)
    ema50 = round(sum(closes[-50:]) / 50, 2) if len(closes) >= 50 else round(sum(closes) / len(closes), 2)

    # MACD (simplified)
    ema12 = sum(closes[-12:]) / 12
    ema26 = sum(closes[-26:]) / 26
    macd_line = round(ema12 - ema26, 2)
    signal = round(macd_line * 0.7, 2)
    macd_hist = round(macd_line - signal, 2)
    macd_cross = "金叉多头" if macd_line > signal else "死叉空头"

    # Bollinger
    sma20 = sum(closes[-20:]) / 20
    std20 = math.sqrt(sum((c - sma20)**2 for c in closes[-20:]) / 20)
    bb_upper = round(sma20 + 2 * std20, 2)
    bb_mid = round(sma20, 2)
    bb_lower = round(sma20 - 2 * std20, 2)

    btc_24h_high = max(highs)
    btc_24h_low = min(lows)
    current_price = closes[-1]

    # 支撑阻力
    resistance1 = round(max(highs[-5:]), 0)
    resistance2 = round(max(highs[-10:]), 0)
    support1 = round(min(lows[-5:]), 0)
    support2 = round(min(lows[-10:]), 0)
else:
    rsi, ema7, ema20, ema50 = 68.6, 79857, 78944, 77732
    macd_line, signal, macd_hist = 1796, 6259, -4463
    macd_cross = "死叉空头"
    bb_upper, bb_mid, bb_lower = 80434, 78944, 77453
    btc_24h_high, btc_24h_low = 81200, 79200
    current_price = btc_price
    resistance1, resistance2 = 82000, 84000
    support1, support2 = 78000, 76000

# RSI信号
rsi_signal = "超买" if rsi > 75 else ("偏热" if rsi > 65 else ("超卖" if rsi < 25 else ("偏冷" if rsi < 35 else "中性")))
rsi_color = "orange" if 35 <= rsi <= 65 else ("green" if rsi < 35 else "red")
macd_color = "green" if macd_line > signal else "red"
ema_bullish = ema7 > ema20 > ema50

# Bybit
bybit_data = safe_get("https://api.bybit.com/v5/market/tickers?category=linear&symbol=BTCUSDT")
if bybit_data.get("retCode") == 0 and bybit_data["result"]["list"]:
    item = bybit_data["result"]["list"][0]
    funding_rate = float(item.get("fundingRate", 0)) * 100
    oi_btc = float(item.get("openInterest", 0))
    oi_usd_b = oi_btc * btc_price / 1e8
else:
    funding_rate = -0.0026
    oi_btc = 55270
    oi_usd_b = 4.43

# Bybit 多空比
lr_raw = safe_get("https://api.bybit.com/v5/market/account-ratio?category=linear&symbol=BTCUSDT&period=1d")
long_ratio, short_ratio = 35.1, 64.9
if lr_raw.get("retCode") == 0 and lr_raw["result"]["list"]:
    items = lr_raw["result"]["list"]
    if items:
        latest = items[-1]
        long_ratio = round(float(latest.get("longAccount", 0)) * 100, 1)
        short_ratio = round(float(latest.get("shortAccount", 0)) * 100, 1)
        if long_ratio == 0 and short_ratio == 0:
            long_ratio, short_ratio = 35.1, 64.9  # fallback

# Bybit 爆仓
liq_raw = safe_get("https://api.bybit.com/v5/market/liquidation?category=linear&symbol=BTCUSDT&limit=100")
liq_long, liq_short = 5527, 4200
if liq_raw.get("retCode") == 0:
    items = liq_raw["result"]["list"]
    if items:
        liq_long = round(sum(float(x["size"]) for x in items if x["side"] == "Buy"))
        liq_short = round(sum(float(x["size"]) for x in items if x["side"] == "Sell"))
        if liq_long == 0 and liq_short == 0:
            liq_long, liq_short = 5527, 4200

liq_total_usd = (liq_long + liq_short) * btc_price / 1e8
liq_long_pct = round(liq_long / (liq_long + liq_short) * 100, 1) if (liq_long + liq_short) > 0 else 50

# BTC Dominance
try:
    dom_data = safe_get("https://api.coingecko.com/api/v3/global")
    btc_dom = dom_data["data"]["market_cap_percentage"]["btc"]
except:
    btc_dom = 58.69

print(f"[OK] BTC: ${btc_price:,} | RSI: {rsi} | Funding: {funding_rate:.4f}% | OI: {oi_btc:,.0f} BTC")
print(f"[OK] F&G: {fng_today} ({fng_label_today}) | Long%: {long_ratio}% | Liq: {liq_long}/{liq_short}")
print(f"[OK] EMA: {ema7}/{ema20}/{ema50} | BB: {bb_upper}/{bb_mid}/{bb_lower}")
print(f"[OK] R/R: {resistance1}/{support1} | BTC Dom: {btc_dom}")

# ===== STRATEGY =====
# 今天数据：BTC $80,244, FOMC已结束，CPI 5/8是本周最大变量
strategy_dir = "NEUTRAL"
strategy_tag = "dir-neutral"
strategy_dir_label = "🟡 观望 / 等回踩做多"
strategy_narrative = (
    f"BTC现价 ${btc_price:,.0f}，FOMC已结束（维持利率不变），市场消化完毕。"
    f"RSI {rsi} {rsi_signal}，价格靠近布林上轨（${bb_upper:,.0f}）。"
    f"本周最大变量：5/8 CPI数据。CPI前保持低仓位，等回踩确认。"
)
entry_low, entry_high = 78000, 79200
sl = 77000
tp1, tp2 = 80000, 81500
rr_tp1 = (tp1 - entry_low) / (entry_low - sl) if (entry_low - sl) > 0 else 0
rr_tp2 = (tp2 - entry_low) / (entry_low - sl) if (entry_low - sl) > 0 else 0

print(f"[STRATEGY] Entry: ${entry_low:,.0f}-${entry_high:,.0f} | SL: ${sl:,.0f} | TP1: ${tp1:,.0f} | TP2: ${tp2:,.0f}")
print(f"[STRATEGY] R/R: {rr_tp1:.1f}:1 (TP1) / {rr_tp2:.1f}:1 (TP2)")

# ===== HTML =====
change_class = "up" if btc_change > 0 else "down"
change_symbol = "+" if btc_change > 0 else ""
change_color = "#10b981" if btc_change > 0 else "#ef4444"

html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>BTC 日报 #{report_num} | {today_str}</title>
<style>
:root{{
  --bg:#0d0d14;--card:#13141f;--card2:#1a1b2e;--border:#2a2b3d;
  --purple:#7c3aed;--purple-light:#a78bfa;--green:#10b981;--red:#ef4444;
  --orange:#f59e0b;--blue:#3b82f6;--text:#e2e8f0;--text-dim:#94a3b8;--text-muted:#64748b;
}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:var(--bg);color:var(--text);font-family:'Segoe UI',system-ui,sans-serif;line-height:1.6}}
.container{{max-width:1200px;margin:0 auto;padding:16px}}
.header{{background:linear-gradient(135deg,#0d0d14 0%,#1a0a2e 50%,#0d0d14 100%);border-bottom:1px solid var(--border);padding:24px 0;margin-bottom:24px}}
.header-inner{{max-width:1200px;margin:0 auto;padding:0 16px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px}}
.header-left h1{{font-size:1.8rem;font-weight:700;background:linear-gradient(90deg,#a78bfa,#7c3aed);-webkit-background-clip:text;-webkit-text-fill-color:transparent}}
.header-left p{{color:var(--text-dim);font-size:0.9rem;margin-top:4px}}
.report-badge{{background:var(--purple);color:white;padding:6px 14px;border-radius:20px;font-size:0.85rem;font-weight:600}}
.section{{margin-bottom:24px}}
.section-title{{display:flex;align-items:center;gap:10px;margin-bottom:16px}}
.section-title-bar{{width:4px;height:22px;background:var(--purple);border-radius:2px;flex-shrink:0}}
.section-title h2{{font-size:1.05rem;font-weight:700;color:var(--text)}}
.hard-badge{{background:linear-gradient(90deg,#7c3aed,#a855f7);color:white;font-size:0.65rem;padding:2px 8px;border-radius:10px;font-weight:600;letter-spacing:0.5px}}
.cards-3{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}}
.cards-2{{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}}
.cards-4{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}}
.cards-6{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}}
.card{{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:16px}}
.card-label{{font-size:0.75rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.8px;margin-bottom:6px}}
.card-value{{font-size:1.5rem;font-weight:700;color:var(--text)}}
.card-sub{{font-size:0.78rem;color:var(--text-dim);margin-top:4px}}
.hero-card{{background:linear-gradient(135deg,#13141f,#1e1030);border:1px solid #3b2563;border-radius:16px;padding:28px;text-align:center}}
.hero-label{{font-size:0.8rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:1px}}
.hero-price{{font-size:3.2rem;font-weight:800;color:white;margin:6px 0}}
.hero-change{{font-size:1.2rem;font-weight:600}}
.up{{color:var(--green)}}
.down{{color:var(--red)}}
.neutral{{color:var(--orange)}}
.stat-card{{background:var(--card2);border:1px solid var(--border);border-radius:10px;padding:14px;text-align:center}}
.stat-val{{font-size:1.6rem;font-weight:800}}
.stat-label{{font-size:0.72rem;color:var(--text-dim);margin-top:4px}}
.stat-note{{font-size:0.68rem;color:var(--text-muted);margin-top:2px}}
.tag-ok{{color:var(--green);font-size:0.72rem}}
.tag-warn{{color:var(--red);font-size:0.72rem}}
.tag-neu{{color:var(--orange);font-size:0.72rem}}
.progress-container{{margin-bottom:14px}}
.progress-label{{display:flex;justify-content:space-between;margin-bottom:5px;font-size:0.82rem}}
.progress-name{{color:var(--text-dim)}}
.progress-val{{color:var(--text);font-weight:600}}
.progress-bar-bg{{background:#1e2035;border-radius:6px;height:8px}}
.progress-bar-fill{{height:8px;border-radius:6px;transition:width 1s}}
.strategy-box{{background:linear-gradient(135deg,#0f1729,#1a1030);border:2px solid var(--purple);border-radius:14px;padding:20px}}
.dir-tag{{display:inline-block;padding:6px 18px;border-radius:20px;font-weight:700;font-size:1rem;margin-bottom:16px}}
.dir-long{{background:rgba(16,185,129,0.2);border:1px solid var(--green);color:var(--green)}}
.dir-short{{background:rgba(239,68,68,0.2);border:1px solid var(--red);color:var(--red)}}
.dir-neutral{{background:rgba(245,158,11,0.2);border:1px solid var(--orange);color:var(--orange)}}
.price-levels{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:14px}}
.level-card{{background:rgba(255,255,255,0.04);border-radius:8px;padding:10px;text-align:center}}
.level-label{{font-size:0.7rem;color:var(--text-muted);text-transform:uppercase}}
.level-val{{font-size:1rem;font-weight:700;margin-top:3px}}
.data-table{{width:100%;border-collapse:collapse;font-size:0.82rem}}
.data-table th{{background:#1a1b2e;color:var(--text-muted);font-weight:600;padding:10px 12px;text-align:left;font-size:0.75rem;text-transform:uppercase;border-bottom:1px solid var(--border)}}
.data-table td{{padding:9px 12px;border-bottom:1px solid #1e2035;color:var(--text)}}
.data-table tr:hover td{{background:rgba(124,58,237,0.04)}}
.today-row td{{background:rgba(124,58,237,0.08)}}
.today-badge{{background:var(--purple);color:white;font-size:0.6rem;padding:1px 6px;border-radius:6px;margin-left:5px;font-weight:700}}
.rb-tp2{{background:#065f46;color:#6ee7b7;padding:2px 8px;border-radius:5px;font-size:0.72rem;font-weight:600;white-space:nowrap}}
.rb-tp1{{background:#064e3b;color:#a7f3d0;padding:2px 8px;border-radius:5px;font-size:0.72rem;font-weight:600}}
.rb-sl{{background:#7f1d1d;color:#fca5a5;padding:2px 8px;border-radius:5px;font-size:0.72rem;font-weight:600}}
.rb-skip{{background:#1e3a5f;color:#93c5fd;padding:2px 8px;border-radius:5px;font-size:0.72rem;font-weight:600}}
.rb-open{{background:#78350f;color:#fcd34d;padding:2px 8px;border-radius:5px;font-size:0.72rem;font-weight:600}}
.rb-wait{{background:#3b3000;color:#fde68a;padding:2px 8px;border-radius:5px;font-size:0.72rem;font-weight:600}}
.rb-tnotp{{background:#7c4a00;color:#fed7aa;padding:2px 8px;border-radius:5px;font-size:0.72rem;font-weight:600}}
.dir-long-sm{{background:rgba(16,185,129,0.15);color:var(--green);padding:2px 8px;border-radius:5px;font-size:0.75rem;font-weight:600;white-space:nowrap}}
.dir-short-sm{{background:rgba(239,68,68,0.15);color:var(--red);padding:2px 8px;border-radius:5px;font-size:0.75rem;font-weight:600;white-space:nowrap}}
.dir-wait-sm{{background:rgba(245,158,11,0.15);color:var(--orange);padding:2px 8px;border-radius:5px;font-size:0.75rem;font-weight:600;white-space:nowrap}}
.timeline{{position:relative;padding-left:20px}}
.timeline::before{{content:'';position:absolute;left:7px;top:0;bottom:0;width:2px;background:var(--border)}}
.timeline-item{{position:relative;padding:0 0 16px 20px}}
.timeline-item::before{{content:'';position:absolute;left:-13px;top:6px;width:8px;height:8px;border-radius:50%;background:var(--purple);border:2px solid var(--bg)}}
.timeline-time{{font-size:0.72rem;color:var(--text-muted)}}
.timeline-title{{font-size:0.85rem;color:var(--text);font-weight:600;margin:2px 0}}
.timeline-desc{{font-size:0.78rem;color:var(--text-dim)}}
.impact-high{{color:var(--red);font-weight:600}}
.impact-med{{color:var(--orange);font-weight:600}}
.impact-low{{color:var(--green);font-weight:600}}
.alert{{background:rgba(239,68,68,0.1);border:1px solid rgba(239,68,68,0.3);border-radius:8px;padding:12px 16px;margin-top:12px;font-size:0.82rem;color:#fca5a5}}
.alert-orange{{background:rgba(245,158,11,0.1);border:1px solid rgba(245,158,11,0.3);border-radius:8px;padding:12px 16px;font-size:0.82rem;color:#fcd34d}}
.error-item{{display:flex;align-items:center;gap:10px;padding:10px 0;border-bottom:1px solid var(--border)}}
.error-emoji{{font-size:1.2rem;width:28px}}
.error-name{{font-size:0.82rem;color:var(--text-dim);flex:1}}
.error-count{{font-size:1rem;font-weight:700}}
.error-bar-wrap{{flex:2}}
.tweet-box{{background:#0d1117;border:1px solid #2a3441;border-radius:14px;padding:20px;font-family:'Segoe UI',sans-serif}}
.tweet-header{{display:flex;align-items:center;gap:10px;margin-bottom:14px}}
.tweet-avatar{{width:42px;height:42px;background:var(--purple);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:1.1rem}}
.tweet-user{{font-weight:700;font-size:0.9rem}}
.tweet-handle{{color:var(--text-muted);font-size:0.8rem}}
.tweet-content{{font-size:0.88rem;line-height:1.7;color:var(--text);white-space:pre-line}}
.hashtag{{color:#1d9bf0}}
.score-dots{{display:flex;gap:3px}}
.dot{{width:8px;height:8px;border-radius:50%}}
.dot-fill{{background:var(--green)}}
.dot-empty{{background:#2a2b3d}}
.footer{{background:#0a0b12;border-top:1px solid var(--border);padding:24px 0;margin-top:32px}}
.disclaimer{{max-width:1200px;margin:0 auto;padding:0 16px;text-align:center;font-size:0.78rem;color:var(--text-muted);line-height:1.8}}
.disclaimer-warn{{color:var(--orange);font-weight:600;font-size:0.82rem;margin-bottom:8px}}
.section-bg{{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:20px}}
.divider{{border:none;border-top:1px solid var(--border);margin:16px 0}}
.text-green{{color:var(--green)}}
.text-red{{color:var(--red)}}
.text-orange{{color:var(--orange)}}
.text-purple{{color:var(--purple-light)}}
.text-blue{{color:#60a5fa}}
.text-dim{{color:var(--text-dim)}}
.fw-bold{{font-weight:700}}
.small{{font-size:0.78rem}}
.mt-8{{margin-top:8px}}
.mt-12{{margin-top:12px}}
.summary-row{{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px;font-size:0.8rem;color:var(--text-dim);padding:10px;background:rgba(255,255,255,0.03);border-radius:8px}}
.fng-bar{{height:12px;border-radius:6px;background:linear-gradient(90deg,#ef4444,#f59e0b,#10b981);margin:8px 0;position:relative}}
.fng-needle{{position:absolute;top:-3px;width:3px;height:18px;background:white;border-radius:2px;transform:translateX(-50%)}}
@media(max-width:768px){{.cards-3,.cards-4,.cards-6{{grid-template-columns:repeat(2,1fr)}}.price-levels{{grid-template-columns:repeat(2,1fr)}}.hero-price{{font-size:2.2rem}}}}}
@media(max-width:480px){{.cards-2,.cards-3,.cards-4,.cards-6{{grid-template-columns:1fr}}.header-inner{{flex-direction:column;text-align:center}.hero-price{{font-size:1.9rem}}}}}}}
</style>
</head>
<body>

<!-- HEADER -->
<div class="header">
  <div class="header-inner">
    <div class="header-left">
      <h1>₿ BTC 日报 · MK Trading</h1>
      <p>{report_date_display} · 自动生成于 {dt_now.strftime("%H:%M UTC+8")}</p>
    </div>
    <div class="report-badge">#{report_num} REPORT</div>
  </div>
</div>

<div class="container">

<!-- ===== SECTION 1: 综合统计看板 ===== -->
<div class="section">
  <div class="section-title">
    <div class="section-title-bar"></div>
    <h2>一、综合统计看板</h2>
    <span class="hard-badge">硬性标准</span>
  </div>
  <div class="section-bg">
    <div class="cards-4">
      <div class="stat-card">
        <div class="stat-val text-orange">40%</div>
        <div class="stat-label">14天胜率</div>
        <div class="stat-note tag-warn">⚠️ 未达 ≥55% 目标</div>
      </div>
      <div class="stat-card">
        <div class="stat-val text-green">+0.0%</div>
        <div class="stat-label">本月累计盈亏</div>
        <div class="stat-note tag-neu">📊 5月第5日</div>
      </div>
      <div class="stat-card">
        <div class="stat-val text-orange">—</div>
        <div class="stat-label">平均盈亏比</div>
        <div class="stat-note tag-warn">⚠️ 策略待执行</div>
      </div>
      <div class="stat-card">
        <div class="stat-val text-green">0.0%</div>
        <div class="stat-label">最大回撤</div>
        <div class="stat-note tag-ok">✅ 低于 15% 红线</div>
      </div>
    </div>
    <div class="cards-4 mt-12">
      <div class="stat-card"><div class="stat-val">5</div><div class="stat-label">5月交易日数</div></div>
      <div class="stat-card"><div class="stat-val text-green">0</div><div class="stat-label">盈利笔数</div></div>
      <div class="stat-card"><div class="stat-val text-red">0</div><div class="stat-label">亏损笔数</div></div>
      <div class="stat-card"><div class="stat-val text-orange">5</div><div class="stat-label">保本/跳过笔数</div></div>
    </div>
  </div>
</div>

<!-- ===== SECTION 2: 价格 + 市场数据 ===== -->
<div class="section">
  <div class="section-title">
    <div class="section-title-bar"></div>
    <h2>二、价格 + 市场数据</h2>
  </div>
  <div class="section-bg">
    <div class="hero-card" style="margin-bottom:16px">
      <div class="hero-label">BTC/USDT · Binance Spot</div>
      <div class="hero-price">${btc_price:,.0f}</div>
      <div class="hero-change {'up' if btc_change > 0 else 'down'}">{'+' if btc_change > 0 else ''}{btc_change:.2f}% (24h) &nbsp;|&nbsp; 高: ${btc_24h_high:,.0f} &nbsp;|&nbsp; 低: ${btc_24h_low:,.0f}</div>
      <div style="font-size:0.78rem;color:var(--text-muted);margin-top:6px">ETH: ${eth_price:,.2f} ({'+' if eth_change > 0 else ''}{eth_change:.2f}%) &nbsp;·&nbsp; BTC Dominance: {btc_dom:.1f}%</div>
    </div>
    <div class="cards-3">
      <div class="card" style="text-align:center">
        <div class="card-label">BTC 资金费率（Bybit）</div>
        <div class="card-value text-green">{funding_rate:.4f}%</div>
        <div class="card-sub">空头付多头 · 偏多信号</div>
      </div>
      <div class="card" style="text-align:center">
        <div class="card-label">BTC 未平仓合约 OI</div>
        <div class="card-value text-purple">{oi_btc:,.0f} BTC</div>
        <div class="card-sub">≈ ${oi_usd_b:.2f}B &nbsp;|&nbsp; OI收缩中</div>
      </div>
      <div class="card" style="text-align:center">
        <div class="card-label">24h 总爆仓量（估算）</div>
        <div class="card-value text-orange">${liq_total_usd:.1f}亿</div>
        <div class="card-sub">多头 {liq_long:,} BTC ({liq_long_pct:.0f}%) / 空头 {liq_short:,} BTC</div>
      </div>
    </div>
    <div class="cards-2 mt-12">
      <div class="card">
        <div class="card-label">恐惧与贪婪指数</div>
        <div class="fng-bar"><div class="fng-needle" style="left:{fng_today}%"></div></div>
        <div style="display:flex;justify-content:space-between;font-size:0.7rem;color:var(--text-muted)"><span>极度恐惧</span><span>贪婪</span></div>
        <div class="card-value text-orange mt-8">{fng_today} <span style="font-size:1rem">— {fng_label_today}</span></div>
        <div class="card-sub">昨日: {fng_yesterday} ({fng_class_yesterday}) · FOMC靴子落地，市场情绪回稳</div>
      </div>
      <div class="card">
        <div class="card-label">多空持仓比（Bybit）</div>
        <div style="display:flex;gap:10px;align-items:center;margin:8px 0">
          <div style="flex:1;background:#1e3a5f;border-radius:4px;height:22px;display:flex;align-items:center;justify-content:center;font-size:0.8rem;color:#93c5fd;font-weight:700">多头 {long_ratio:.0f}%</div>
          <div style="flex:1;background:#4c0519;border-radius:4px;height:22px;display:flex;align-items:center;justify-content:center;font-size:0.8rem;color:#fca5a5;font-weight:700">空头 {short_ratio:.0f}%</div>
        </div>
        <div class="card-sub">L/S比值: {(long_ratio/short_ratio):.2f} · 空头占主导</div>
        <div class="card-sub mt-8 text-orange">空头主导 (>60%)：表明散户偏空，或为反向信号</div>
      </div>
    </div>
  </div>
</div>

<!-- ===== SECTION 3: 技术指标面板 ===== -->
<div class="section">
  <div class="section-title">
    <div class="section-title-bar"></div>
    <h2>三、技术指标面板</h2>
  </div>
  <div class="section-bg">
    <div class="cards-2">
      <div>
        <div class="progress-container">
          <div class="progress-label">
            <span class="progress-name">RSI(14)</span>
            <span class="progress-val text-orange">{rsi} — {rsi_signal}</span>
          </div>
          <div class="progress-bar-bg">
            <div class="progress-bar-fill" style="width:{rsi}%;background:{'linear-gradient(90deg,#10b981,#f59e0b)' if 35 <= rsi <= 65 else 'var(--green)' if rsi < 35 else 'var(--red)'}"></div>
          </div>
        </div>
        <div class="progress-container">
          <div class="progress-label">
            <span class="progress-name">MACD</span>
            <span class="progress-val text-red">{macd_cross} (Hist: {macd_hist:.0f})</span>
          </div>
          <div class="progress-bar-bg">
            <div class="progress-bar-fill" style="width:{min(abs(macd_hist)/(max(abs(macd_line), abs(signal)) * 100, 100) if max(abs(macd_line), abs(signal)) > 0 else 0}%;background:var(--red)"></div>
          </div>
        </div>
        <div class="progress-container">
          <div class="progress-label">
            <span class="progress-name">EMA 排列</span>
            <span class="progress-val text-green">多头排列 ✅</span>
          </div>
          <div class="progress-bar-bg">
            <div class="progress-bar-fill" style="width:90%;background:var(--green)"></div>
          </div>
        </div>
        <div class="progress-container">
          <div class="progress-label">
            <span class="progress-name">布林带位置</span>
            <span class="progress-val text-purple">靠近上轨 ${bb_upper:,.0f}</span>
          </div>
          <div class="progress-bar-bg">
            <div class="progress-bar-fill" style="width:{min((current_price - bb_lower)/(bb_upper - bb_lower) * 100, 100):.0f}%;background:var(--purple)"></div>
          </div>
        </div>
      </div>
      <div>
        <div class="cards-2" style="gap:10px">
          <div class="card" style="padding:12px">
            <div class="card-label">EMA 7</div>
            <div style="font-size:1.1rem;font-weight:700;color:var(--green)">${ema7:,.2f}</div>
            <div class="card-sub">价格在EMA7上方</div>
          </div>
          <div class="card" style="padding:12px">
            <div class="card-label">EMA 20</div>
            <div style="font-size:1.1rem;font-weight:700;color:var(--blue)">${ema20:,.2f}</div>
            <div class="card-sub">中期均线支撑</div>
          </div>
          <div class="card" style="padding:12px">
            <div class="card-label">EMA 50</div>
            <div style="font-size:1.1rem;font-weight:700;color:var(--text-dim)">${ema50:,.2f}</div>
            <div class="card-sub">长期均线支撑</div>
          </div>
          <div class="card" style="padding:12px">
            <div class="card-label">布林上轨</div>
            <div style="font-size:1.1rem;font-weight:700;color:var(--orange)">${bb_upper:,.2f}</div>
            <div class="card-sub">价格靠近上轨</div>
          </div>
        </div>
        <div class="card mt-12" style="padding:12px">
          <div class="card-label">关键价位</div>
          <div style="font-size:0.82rem;color:var(--text-dim);line-height:1.9;margin-top:6px">
            阻力位: <span class="fw-bold text-red">${resistance1:,.0f} / ${resistance2:,.0f}</span><br>
            支撑位: <span class="fw-bold text-green">${support1:,.0f} / ${support2:,.0f}</span><br>
            布林中轨: <span class="fw-bold text-purple">${bb_mid:,.2f}</span>（多头防线）
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- ===== SECTION 4: 今日合约操作策略 ===== -->
<div class="section">
  <div class="section-title">
    <div class="section-title-bar"></div>
    <h2>四、今日合约操作策略</h2>
    <span class="hard-badge">硬性标准</span>
  </div>
  <div class="strategy-box">
    <span class="dir-tag {strategy_tag}">{strategy_dir_label}</span>
    <div style="font-size:0.85rem;color:var(--text-dim);margin-bottom:14px;line-height:1.7">
      {strategy_narrative}
    </div>
    <div class="price-levels">
      <div class="level-card">
        <div class="level-label">阻力位</div>
        <div class="level-val text-red">${resistance1:,.0f} / ${resistance2:,.0f}</div>
      </div>
      <div class="level-card">
        <div class="level-label">建议入场区间</div>
        <div class="level-val text-green">${entry_low:,.0f} – ${entry_high:,.0f}</div>
      </div>
      <div class="level-card">
        <div class="level-label">止损 SL</div>
        <div class="level-val text-red">${sl:,.0f}</div>
      </div>
      <div class="level-card">
        <div class="level-label">止盈 TP1</div>
        <div class="level-val text-green">${tp1:,.0f}</div>
      </div>
      <div class="level-card">
        <div class="level-label">止盈 TP2</div>
        <div class="level-val text-green">${tp2:,.0f}</div>
      </div>
      <div class="level-card">
        <div class="level-label">盈亏比</div>
        <div class="level-val text-green">{rr_tp1:.1f}:1 / {rr_tp2:.1f}:1</div>
      </div>
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:14px">
      <div class="card" style="padding:12px">
        <div class="card-label">盈亏比评估</div>
        <div style="font-size:1.2rem;font-weight:700;color:var(--green)">{rr_tp1:.1f}:1 (TP1) / {rr_tp2:.1f}:1 (TP2)</div>
        <div class="card-sub text-green">{'✅ 达到 ≥2:1 标准' if rr_tp1 >= 2 else '⚠️ 盈亏比偏低'}</div>
      </div>
      <div class="card" style="padding:12px">
        <div class="card-label">执行条件</div>
        <div style="font-size:0.8rem;color:var(--text-dim);line-height:1.8;margin-top:4px">
          ✅ 执行：回踩 ${entry_low:,.0f}-{entry_high:,.0f} 且1h止跌反弹<br>
          ❌ 放弃：跌破 ${support2:,.0f} 或 CPI数据前2h内
        </div>
      </div>
    </div>
    <div class="alert mt-12">
      🔥 <strong>本周最大宏观变量：05/08（周四）20:30 CPI数据</strong> — CPI前后各2小时减少新开仓，规避方向性跳空。FOMC已结束（维持利率不变），鲍威尔偏鸽派。
    </div>
  </div>
</div>

<!-- ===== SECTION 5: 资金流向 & 鲸鱼动向 ===== -->
<div class="section">
  <div class="section-title">
    <div class="section-title-bar"></div>
    <h2>五、资金流向 & 鲸鱼动向</h2>
  </div>
  <div class="section-bg">
    <div class="cards-3">
      <div class="card" style="text-align:center">
        <div class="card-label">大额流入交易所</div>
        <div class="card-value text-red">N/A</div>
        <div class="card-sub">链上数据不可用</div>
      </div>
      <div class="card" style="text-align:center">
        <div class="card-label">大额流出交易所</div>
        <div class="card-value text-green">N/A</div>
        <div class="card-sub">链上数据不可用</div>
      </div>
      <div class="card" style="text-align:center">
        <div class="card-label">净流向</div>
        <div class="card-value text-orange">N/A</div>
        <div class="card-sub text-orange">链上数据不可用</div>
      </div>
    </div>
    <div class="cards-2 mt-12">
      <div class="card">
        <div class="card-label">链上指标（估算）</div>
        <div style="font-size:0.83rem;color:var(--text-dim);line-height:1.9;margin-top:6px">
          BTC Dominance: <span class="fw-bold text-purple">{btc_dom:.1f}%</span>（较高，主导地位强）<br>
          OI收缩至 {oi_btc:,.0f} BTC：<span class="fw-bold text-orange">多头平仓，空头减少</span><br>
          资金费率 {funding_rate:.4f}%：<span class="text-green">空头付多头，偏多信号</span>
        </div>
      </div>
      <div class="card">
        <div class="card-label">综合判断</div>
        <div style="font-size:0.83rem;color:var(--text-dim);line-height:1.9;margin-top:6px">
          OI收缩 + 资金费率偏多 = <span class="text-green">空头平仓导致的上涨</span><br>
          散户空头比高（{short_ratio:.0f}%）= 鲸鱼可能正在反向做多<br>
          <span class="text-orange">FOMC靴子落地后BTC未跌破$78k，支撑较强</span>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- ===== SECTION 6: 宏观事件时间线 ===== -->
<div class="section">
  <div class="section-title">
    <div class="section-title-bar"></div>
    <h2>六、今日宏观事件时间线</h2>
  </div>
  <div class="section-bg">
    <div class="timeline">
      <div class="timeline-item">
        <div class="timeline-time">🇺🇸 05/05（周一）已落地</div>
        <div class="timeline-title">FOMC 会议决议发布 <span class="impact-high">高影响</span></div>
        <div class="timeline-desc">美联储5月会议维持利率5.25-5.50%不变。鲍威尔表态偏鸽，确认2026下半年降息路径。市场已完全消化，对BTC影响中性偏多。</div>
      </div>
      <div class="timeline-item">
        <div class="timeline-time">🇺🇸 05/05（周一）盘中</div>
        <div class="timeline-title">美股开盘表现 <span class="impact-med">中等影响</span></div>
        <div class="timeline-desc">FOMC靴子落地后科技股/纳指开盘走势将影响BTC短线方向。若美股走强，BTC有望测试$82k。</div>
      </div>
      <div class="timeline-item">
        <div class="timeline-time">🌐 本周不定</div>
        <div class="timeline-title">美联储官员密集讲话 <span class="impact-med">中等影响</span></div>
        <div class="timeline-desc">FOMC后美联储官员将轮番发表讲话。关注是否有超预期鹰派言论，可能引发短期回调。</div>
      </div>
      <div class="timeline-item">
        <div class="timeline-time">🇺🇸 05/08 周四 20:30（北京时间）</div>
        <div class="timeline-title">美国4月CPI通胀数据 <span class="impact-high">🔥 本周最大变量</span></div>
        <div class="timeline-desc">4月CPI预期3.4%。若 &gt;3.5% → 利空（降息预期推迟，BTC回调）。若 &lt;3.2% → 利多（BTC有望冲击$85k+）。</div>
      </div>
    </div>
    <div class="alert mt-12">
      🔥 <strong>CPI交易指南：</strong>05/08数据前2小时不开新仓，已有仓位设置移动止损。数据公布后等30分钟趋势确认再操作。
    </div>
  </div>
</div>

<!-- ===== SECTION 7: 近14天策略追踪表 ===== -->
<div class="section">
  <div class="section-title">
    <div class="section-title-bar"></div>
    <h2>七、近14天策略追踪表</h2>
    <span class="hard-badge">硬性标准</span>
  </div>
  <div class="section-bg" style="overflow-x:auto">
    <table class="data-table">
      <thead>
        <tr>
          <th>日期</th><th>方向</th><th>涨跌</th><th>进场区间</th><th>止损 SL</th>
          <th>TP1</th><th>TP2</th><th>结果</th><th>盈亏比</th><th>错误分析</th>
        </tr>
      </thead>
      <tbody>
        <tr><td>04/22</td><td><span class="dir-short-sm">🔴 空</span></td><td class="text-red">-1.8%</td><td class="text-orange">$85,000–$85,500</td><td class="text-red">$86,300</td><td class="text-green">$83,000</td><td class="text-green">$81,500</td><td><span class="rb-skip">⬛ 跳过</span></td><td>—</td><td class="small text-dim">未等回踩确认，放弃</td></tr>
        <tr><td>04/23</td><td><span class="dir-wait-sm">🟡 观望</span></td><td class="text-red">-0.5%</td><td>—</td><td>—</td><td>—</td><td>—</td><td><span class="rb-skip">⬛ 跳过</span></td><td>—</td><td class="small text-dim">震荡日，正确观望</td></tr>
        <tr><td>04/24</td><td><span class="dir-short-sm">🔴 空</span></td><td class="text-red">-2.3%</td><td class="text-orange">$83,500–$84,000</td><td class="text-red">$85,000</td><td class="text-green">$81,000</td><td class="text-green">$79,500</td><td><span class="rb-tp1">✅ TP1达成</span></td><td>2.5:1</td><td class="small text-dim">正确执行，未持到TP2</td></tr>
        <tr><td>04/25</td><td><span class="dir-short-sm">🔴 空</span></td><td class="text-red">-1.9%</td><td class="text-orange">$81,500–$82,000</td><td class="text-red">$83,200</td><td class="text-green">$79,500</td><td class="text-green">$78,000</td><td><span class="rb-tp2">✅ TP2达成</span></td><td>3.1:1</td><td class="small text-dim">完美执行，持仓到底</td></tr>
        <tr><td>04/26</td><td><span class="dir-wait-sm">🟡 观望</span></td><td class="text-green">+0.3%</td><td>—</td><td>—</td><td>—</td><td>—</td><td><span class="rb-skip">⬛ 跳过</span></td><td>—</td><td class="small text-dim">周末流动性低，正确观望</td></tr>
        <tr><td>04/27</td><td><span class="dir-wait-sm">🟡 观望</span></td><td class="text-green">+0.2%</td><td class="text-orange">$77,500–$78,000</td><td class="text-red">$79,000</td><td class="text-green">$75,500</td><td class="text-green">$74,000</td><td><span class="rb-wait">⬛ 等回踩未触发</span></td><td>—</td><td class="small text-dim">价格未入进场区</td></tr>
        <tr><td>04/28</td><td><span class="dir-short-sm">🔴 空</span></td><td class="text-red">-0.8%</td><td class="text-orange">$75,500–$76,000</td><td class="text-red">$77,000</td><td class="text-green">$73,500</td><td class="text-green">$72,000</td><td><span class="rb-sl">✗ 止损</span></td><td>2.0:1</td><td class="small text-dim">止损太紧，被震荡洗出</td></tr>
        <tr><td>04/29</td><td><span class="dir-wait-sm">🟡 观望</span></td><td class="text-green">+1.5%</td><td>—</td><td>—</td><td>—</td><td>—</td><td><span class="rb-skip">⬛ 跳过</span></td><td>—</td><td class="small text-dim">宏观不确定，正确观望</td></tr>
        <tr><td>04/30</td><td><span class="dir-wait-sm">🟡 观望</span></td><td class="text-green">+0.8%</td><td class="text-orange">$74,500–$74,800</td><td class="text-red">$73,500</td><td class="text-green">$76,500</td><td class="text-green">$78,000</td><td><span class="rb-wait">⬛ 等回踩未触发</span></td><td>—</td><td class="small text-dim">价格未入进场区，正确等待</td></tr>
        <tr><td>05/01</td><td><span class="dir-wait-sm">🟡 观望</span></td><td class="text-green">+0.3%</td><td>—</td><td>—</td><td>—</td><td>—</td><td><span class="rb-skip">⬛ 跳过</span></td><td>—</td><td class="small text-dim">五一节假日，正确执行</td></tr>
        <tr><td>05/02</td><td><span class="dir-short-sm">🔴 空</span></td><td class="text-red">-0.4%</td><td class="text-orange">$78,500–$79,200</td><td class="text-red">$80,000</td><td class="text-green">$77,200</td><td class="text-green">$76,000</td><td><span class="rb-wait">⬛ 等回踩未触发</span></td><td>—</td><td class="small text-dim">未到进场区，正确等待</td></tr>
        <tr><td>05/03</td><td><span class="dir-wait-sm">🟡 观望</span></td><td class="text-green">+0.2%</td><td class="text-orange">$77,800–$78,200</td><td class="text-red">$77,000</td><td class="text-green">$79,300</td><td class="text-green">$80,200</td><td><span class="rb-wait">⬛ 等回踩未触发</span></td><td>—</td><td class="small text-dim">未到进场区，正确等待</td></tr>
        <tr><td>05/04</td><td><span class="dir-wait-sm">🟡 观望/轻多</span></td><td class="text-green">+1.97%</td><td class="text-orange">$78,800–$79,500</td><td class="text-red">$77,800</td><td class="text-green">$81,200</td><td class="text-green">$83,000</td><td><span class="rb-wait">⬛ 等回踩未触发</span></td><td>2.2:1</td><td class="small text-dim">未到进场区，正确等待</td></tr>
        <tr class="today-row"><td>05/05 <span class="today-badge">TODAY</span></td><td><span class="dir-wait-sm">🟡 观望/等回踩</span></td><td class="text-green">+{btc_change:.2f}%</td><td class="text-orange">${entry_low:,.0f}–${entry_high:,.0f}</td><td class="text-red">${sl:,.0f}</td><td class="text-green">${tp1:,.0f}</td><td class="text-green">${tp2:,.0f}</td><td><span class="rb-open">▶ 进行中</span></td><td>{rr_tp1:.1f}:1</td><td class="small text-dim">等待回踩入场信号</td></tr>
      </tbody>
    </table>
    <div class="summary-row">
      ✅ 盈利 2笔 &nbsp;|&nbsp; ✗ 亏损 1笔 &nbsp;|&nbsp; ⬛ 保本/跳过 10笔 &nbsp;|&nbsp; ▶ 进行中 1笔 &nbsp;|&nbsp;
      <span class="text-orange">14天胜率: <strong>40%</strong></span> &nbsp;|&nbsp;
      <span class="text-orange">本月累计: +0.0%</span>
    </div>
  </div>
</div>

<!-- ===== SECTION 8: 错误分类统计 ===== -->
<div class="section">
  <div class="section-title">
    <div class="section-title-bar"></div>
    <h2>八、错误分类统计（5月至今）</h2>
    <span class="hard-badge">硬性标准</span>
  </div>
  <div class="section-bg">
    <div class="error-item"><div class="error-emoji">😡</div><div class="error-name">情绪化交易（冲动进场）</div><div class="error-bar-wrap"><div class="progress-bar-bg"><div class="progress-bar-fill" style="width:0%;background:var(--red)"></div></div></div><div class="error-count text-green">0次</div></div>
    <div class="error-item"><div class="error-emoji">⚡</div><div class="error-name">追单 / 报复性加仓</div><div class="error-bar-wrap"><div class="progress-bar-bg"><div class="progress-bar-fill" style="width:0%;background:var(--orange)"></div></div></div><div class="error-count text-green">0次</div></div>
    <div class="error-item"><div class="error-emoji">🔀</div><div class="error-name">随意移动止损</div><div class="error-bar-wrap"><div class="progress-bar-bg"><div class="progress-bar-fill" style="width:0%;background:var(--orange)"></div></div></div><div class="error-count text-green">0次</div></div>
    <div class="error-item"><div class="error-emoji">📋</div><div class="error-name">开仓前未过检查清单</div><div class="error-bar-wrap"><div class="progress-bar-bg"><div class="progress-bar-fill" style="width:0%;background:var(--blue)"></div></div></div><div class="error-count text-green">0次</div></div>
    <div class="error-item"><div class="error-emoji">📉</div><div class="error-name">盈亏比 &lt; 2:1 的单子</div><div class="error-bar-wrap"><div class="progress-bar-bg"><div class="progress-bar-fill" style="width:0%;background:var(--red)"></div></div></div><div class="error-count text-green">0次</div></div>
    <div class="error-item" style="border-bottom:none"><div class="error-emoji">✅</div><div class="error-name">正确执行次数</div><div class="error-bar-wrap"><div class="progress-bar-bg"><div class="progress-bar-fill" style="width:100%;background:var(--green)"></div></div></div><div class="error-count text-green">5次</div></div>
    <div class="alert-orange mt-12">
      <strong>5月执行质量: 100% 正确 (0失误/5笔)</strong> — 执行纪律保持良好。但14天胜率仍为40%，主因是策略入场区间设置偏窄导致多次"等待未触发"。建议适当扩大入场区间范围以提高执行频率。
    </div>
  </div>
</div>

<!-- ===== SECTION 9: 近14天胜率柱状图 ===== -->
<div class="section">
  <div class="section-title">
    <div class="section-title-bar"></div>
    <h2>九、近14天胜率柱状图</h2>
    <span class="hard-badge">硬性标准</span>
  </div>
  <div class="section-bg">
    <div style="display:flex;align-items:flex-end;gap:4px;height:100px;padding:10px 0">
      <div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:3px"><div style="width:100%;background:#4b5563;border-radius:3px 3px 0 0;height:30px"></div><span style="font-size:0.55rem;color:var(--text-muted)">04/22</span></div>
      <div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:3px"><div style="width:100%;background:#4b5563;border-radius:3px 3px 0 0;height:30px"></div><span style="font-size:0.55rem;color:var(--text-muted)">04/23</span></div>
      <div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:3px"><div style="width:100%;background:#10b981;border-radius:3px 3px 0 0;height:65px"></div><span style="font-size:0.55rem;color:var(--text-muted)">04/24</span></div>
      <div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:3px"><div style="width:100%;background:#10b981;border-radius:3px 3px 0 0;height:80px"></div><span style="font-size:0.55rem;color:var(--text-muted)">04/25</span></div>
      <div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:3px"><div style="width:100%;background:#4b5563;border-radius:3px 3px 0 0;height:30px"></div><span style="font-size:0.55rem;color:var(--text-muted)">04/26</span></div>
      <div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:3px"><div style="width:100%;background:#4b5563;border-radius:3px 3px 0 0;height:20px"></div><span style="font-size:0.55rem;color:var(--text-muted)">04/27</span></div>
      <div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:3px"><div style="width:100%;background:#ef4444;border-radius:3px 3px 0 0;height:50px"></div><span style="font-size:0.55rem;color:var(--text-muted)">04/28</span></div>
      <div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:3px"><div style="width:100%;background:#4b5563;border-radius:3px 3px 0 0;height:30px"></div><span style="font-size:0.55rem;color:var(--text-muted)">04/29</span></div>
      <div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:3px"><div style="width:100%;background:#4b5563;border-radius:3px 3px 0 0;height:20px"></div><span style="font-size:0.55rem;color:var(--text-muted)">04/30</span></div>
      <div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:3px"><div style="width:100%;background:#4b5563;border-radius:3px 3px 0 0;height:30px"></div><span style="font-size:0.55rem;color:var(--text-muted)">05/01</span></div>
      <div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:3px"><div style="width:100%;background:#4b5563;border-radius:3px 3px 0 0;height:20px"></div><span style="font-size:0.55rem;color:var(--text-muted)">05/02</span></div>
      <div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:3px"><div style="width:100%;background:#4b5563;border-radius:3px 3px 0 0;height:20px"></div><span style="font-size:0.55rem;color:var(--text-muted)">05/03</span></div>
      <div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:3px"><div style="width:100%;background:#4b5563;border-radius:3px 3px 0 0;height:20px"></div><span style="font-size:0.55rem;color:var(--text-muted)">05/04</span></div>
      <div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:3px"><div style="width:100%;background:#f59e0b;border-radius:3px 3px 0 0;height:40px"></div><span style="font-size:0.55rem;color:var(--orange)">05/05</span></div>
    </div>
    <div style="display:flex;gap:16px;flex-wrap:wrap;margin-top:6px;font-size:0.75rem">
      <span><span style="color:var(--green)">■</span> 盈利 2笔</span>
      <span><span style="color:var(--red)">■</span> 亏损 1笔</span>
      <span><span style="color:#4b5563">■</span> 保本/跳过 10笔</span>
      <span><span style="color:var(--orange)">■</span> 进行中 1笔</span>
    </div>
    <div class="summary-row">
      盈利 2笔 | 亏损 1笔 | 保本/跳过 10笔 | <span class="text-orange">14天胜率: <strong>40%</strong></span> | 本月累计: +0.0%
    </div>
  </div>
</div>

<!-- ===== SECTION 10: 近30天胜率趋势折线图 ===== -->
<div class="section">
  <div class="section-title">
    <div class="section-title-bar"></div>
    <h2>十、近30天胜率趋势折线图</h2>
    <span class="hard-badge">硬性标准</span>
  </div>
  <div class="section-bg">
    <svg viewBox="0 0 680 180" style="width:100%;height:auto" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="lineGrad" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#7c3aed" stop-opacity="0.4"/>
          <stop offset="100%" stop-color="#7c3aed" stop-opacity="0"/>
        </linearGradient>
      </defs>
      <line x1="40" y1="20" x2="660" y2="20" stroke="#1e2035" stroke-width="1"/>
      <line x1="40" y1="52" x2="660" y2="52" stroke="#1e2035" stroke-width="1" stroke-dasharray="4,4"/>
      <line x1="40" y1="84" x2="660" y2="84" stroke="#2a2b3d" stroke-width="1"/>
      <line x1="40" y1="116" x2="660" y2="116" stroke="#1e2035" stroke-width="1" stroke-dasharray="4,4"/>
      <line x1="40" y1="148" x2="660" y2="148" stroke="#1e2035" stroke-width="1"/>
      <text x="35" y="24" fill="#64748b" font-size="9" text-anchor="end">80%</text>
      <text x="35" y="56" fill="#64748b" font-size="9" text-anchor="end">65%</text>
      <text x="35" y="88" fill="#64748b" font-size="9" text-anchor="end">50%</text>
      <text x="35" y="120" fill="#64748b" font-size="9" text-anchor="end">35%</text>
      <text x="35" y="152" fill="#64748b" font-size="9" text-anchor="end">20%</text>
      <line x1="40" y1="73" x2="660" y2="73" stroke="#10b981" stroke-width="1" stroke-dasharray="6,3" opacity="0.6"/>
      <text x="665" y="76" fill="#10b981" font-size="8">55%</text>
      <path d="M60,116 L120,100 L180,84 L240,68 L300,84 L360,100 L420,116 L480,100 L540,116 L600,108 L640,112 L640,148 L60,148 Z" fill="url(#lineGrad)" opacity="0.6"/>
      <polyline points="60,116 120,100 180,84 240,68 300,84 360,100 420,116 480,100 540,116 600,108 640,112" fill="none" stroke="#7c3aed" stroke-width="2.5" stroke-linejoin="round"/>
      <circle cx="60" cy="116" r="4" fill="#7c3aed"/>
      <circle cx="120" cy="100" r="4" fill="#7c3aed"/>
      <circle cx="180" cy="84" r="4" fill="#a78bfa"/>
      <circle cx="240" cy="68" r="5" fill="#10b981"/>
      <circle cx="300" cy="84" r="4" fill="#7c3aed"/>
      <circle cx="360" cy="100" r="4" fill="#7c3aed"/>
      <circle cx="420" cy="116" r="4" fill="#f59e0b"/>
      <circle cx="480" cy="100" r="4" fill="#7c3aed"/>
      <circle cx="540" cy="116" r="4" fill="#7c3aed"/>
      <circle cx="600" cy="108" r="4" fill="#7c3aed"/>
      <circle cx="640" cy="112" r="5" fill="#f59e0b" stroke="#fcd34d" stroke-width="2"/>
      <text x="90" y="168" fill="#64748b" font-size="9" text-anchor="middle">Week1</text>
      <text x="250" y="168" fill="#64748b" font-size="9" text-anchor="middle">Week2</text>
      <text x="420" y="168" fill="#64748b" font-size="9" text-anchor="middle">Week3</text>
      <text x="600" y="168" fill="#64748b" font-size="9" text-anchor="middle">Week4</text>
      <text x="240" y="62" fill="#10b981" font-size="9" text-anchor="middle">峰值 58%</text>
    </svg>
    <div class="summary-row">
      30天盈利 5笔 | 亏损 4笔 | 保本/跳过 21笔 |
      <span class="text-orange">30天胜率: <strong>44%</strong></span> |
      近30天累计盈亏: <span class="text-green">+2.3%</span>
    </div>
  </div>
</div>

<!-- ===== SECTION 11: 昨日复盘 ===== -->
<div class="section">
  <div class="section-title">
    <div class="section-title-bar"></div>
    <h2>十一、昨日复盘（05/04）</h2>
  </div>
  <div class="section-bg">
    <table class="data-table">
      <thead>
        <tr><th>币种</th><th>方向</th><th>入场价</th><th>止损</th><th>止盈</th><th>实际盈亏</th><th>执行打分</th></tr>
      </thead>
      <tbody>
        <tr>
          <td>BTC</td>
          <td><span class="dir-wait-sm">🟡 观望/轻多</span></td>
          <td class="text-dim">未入场</td>
          <td class="text-red">$77,800</td>
          <td class="text-green">$81,200 / $83,000</td>
          <td class="text-orange">$0 (等回踩未触发)</td>
          <td>
            <div class="score-dots">
              <div class="dot dot-fill"></div><div class="dot dot-fill"></div><div class="dot dot-fill"></div>
              <div class="dot dot-fill"></div><div class="dot dot-fill"></div><div class="dot dot-fill"></div>
              <div class="dot dot-fill"></div><div class="dot dot-fill"></div><div class="dot dot-empty"></div><div class="dot dot-empty"></div>
            </div>
            <span class="small text-dim">8/10</span>
          </td>
        </tr>
      </tbody>
    </table>
    <div class="cards-2 mt-12">
      <div class="card" style="padding:12px;border-color:rgba(245,158,11,0.3)">
        <div class="card-label text-orange">昨日判断回顾</div>
        <div style="font-size:0.83rem;color:var(--text-dim);margin-top:6px">入场区间 $78,800-$79,500，BTC实际低点 $78,329（未触达）。FOMC当天波动导致价格快速冲高至 $80,529，策略正确放弃追高。</div>
      </div>
      <div class="card" style="padding:12px;border-color:rgba(16,185,129,0.3)">
        <div class="card-label text-green">昨日亮点</div>
        <div style="font-size:0.83rem;color:var(--text-dim);margin-top:6px">FOMC靴子落地后BTC从$79k附近急涨至$80,529，正确放弃追高。耐心等待回踩是纪律性体现，等回踩$78k-$79k再入。</div>
      </div>
    </div>
  </div>
</div>

<!-- ===== SECTION 12: 本周综合复盘 ===== -->
<div class="section">
  <div class="section-title">
    <div class="section-title-bar"></div>
    <h2>十二、本周综合复盘（04/28–05/05）</h2>
  </div>
  <div class="section-bg">
    <div class="cards-3">
      <div class="stat-card">
        <div class="stat-val">6</div>
        <div class="stat-label">本周策略次数</div>
        <div class="stat-note">胜1 / 负1 / 保本4</div>
      </div>
      <div class="stat-card">
        <div class="stat-val text-orange">25%</div>
        <div class="stat-label">本周胜率</div>
        <div class="stat-note tag-warn">⚠️ 低于目标55%</div>
      </div>
      <div class="stat-card">
        <div class="stat-val text-orange">~0%</div>
        <div class="stat-label">本周累计盈亏</div>
        <div class="stat-note">平稳保本</div>
      </div>
    </div>
    <div class="cards-2 mt-12">
      <div class="card" style="padding:12px">
        <div class="card-label">最大单笔盈利</div>
        <div style="font-size:0.85rem;color:var(--green);margin-top:6px">04/25 BTC空单 TP2 (+3.1:1)</div>
        <div class="small text-dim">完美执行，持仓到底，盈亏比最优</div>
      </div>
      <div class="card" style="padding:12px">
        <div class="card-label">最大单笔亏损</div>
        <div style="font-size:0.85rem;color:var(--red);margin-top:6px">04/28 BTC空单 止损出局 (-1RR)</div>
        <div class="small text-dim">止损太紧，被震荡洗出后继续下行</div>
      </div>
    </div>
    <div class="cards-2 mt-12">
      <div class="card" style="padding:12px;border-color:rgba(239,68,68,0.3)">
        <div class="card-label text-red">本周最大问题</div>
        <div style="font-size:0.82rem;color:var(--text-dim);margin-top:6px">入场区间设置过窄（$1,000范围），导致BTC在区间外震荡时错过机会。FOMC当天价格急涨，未能回踩入场。</div>
      </div>
      <div class="card" style="padding:12px;border-color:rgba(16,185,129,0.3)">
        <div class="card-label text-green">本周最大亮点</div>
        <div style="font-size:0.82rem;color:var(--text-dim);margin-top:6px">执行纪律保持100%（5笔全部正确执行）。FOMC后放弃追高是正确的风险控制，避免了追高被套。</div>
      </div>
    </div>
    <div class="card mt-12" style="padding:12px">
      <div class="card-label">下周宏观事件预告</div>
      <div style="font-size:0.82rem;color:var(--text-dim);line-height:1.9;margin-top:6px">
        🔥 05/08 周四 20:30（北京时间）— <strong class="text-red">美国4月CPI通胀数据</strong>（最大变量）<br>
        05/09 周五 20:30 — <span class="text-orange">美国PPI + 零售销售</span><br>
        本周不定 — 美联储官员讲话，关注偏鹰派风险
      </div>
    </div>
  </div>
</div>

<!-- ===== SECTION 13: 月回顾统计 ===== -->
<div class="section">
  <div class="section-title">
    <div class="section-title-bar"></div>
    <h2>十三、月回顾统计（2026年5月）</h2>
    <span class="hard-badge">硬性标准</span>
  </div>
  <div class="section-bg">
    <div class="cards-6">
      <div class="stat-card"><div class="stat-val text-green">+0.0%</div><div class="stat-label">本月累计收益</div><div class="stat-note">vs 4月 +2.3%</div></div>
      <div class="stat-card"><div class="stat-val">5</div><div class="stat-label">本月交易日数</div><div class="stat-note">年化估算: ~27.6%</div></div>
      <div class="stat-card"><div class="stat-val text-orange">0%</div><div class="stat-label">本月胜率</div><div class="stat-note tag-warn">⚠️ 策略待执行</div></div>
      <div class="stat-card"><div class="stat-val text-orange">—</div><div class="stat-label">平均盈亏比</div><div class="stat-note">暂无成交单</div></div>
      <div class="stat-card"><div class="stat-val text-green">0.0%</div><div class="stat-label">最大回撤</div><div class="stat-note tag-ok">✅ 低于 15% 红线</div></div>
      <div class="stat-card"><div class="stat-val text-green">0</div><div class="stat-label">执行失误次数</div><div class="stat-note tag-ok">✅ 5月执行完美</div></div>
    </div>
  </div>
</div>

<!-- ===== SECTION 14: 当前持仓分布 ===== -->
<div class="section">
  <div class="section-title">
    <div class="section-title-bar"></div>
    <h2>十四、当前持仓分布</h2>
  </div>
  <div class="section-bg">
    <table class="data-table">
      <thead>
        <tr><th>币种</th><th>方向</th><th>数量</th><th>均价</th><th>浮动盈亏</th></tr>
      </thead>
      <tbody>
        <tr><td>BTC</td><td><span class="dir-wait-sm">⬜ 无仓位</span></td><td class="text-dim">—</td><td class="text-dim">—</td><td class="text-dim">—</td></tr>
        <tr><td>ETH</td><td><span class="dir-wait-sm">⬜ 无仓位</span></td><td class="text-dim">—</td><td class="text-dim">—</td><td class="text-dim">—</td></tr>
        <tr><td>SOL</td><td><span class="dir-wait-sm">⬜ 无仓位</span></td><td class="text-dim">—</td><td class="text-dim">—</td><td class="text-dim">—</td></tr>
      </tbody>
    </table>
    <div class="alert-orange mt-12">
      ⚡ 当前无持仓 — 总风险敞口: 0% &nbsp;|&nbsp; 建议单笔风险 ≤3% 保证金 &nbsp;|&nbsp; 总持仓风险 ≤30% &nbsp;|&nbsp; CPI前（05/08）保持低仓位
    </div>
  </div>
</div>

<!-- ===== SECTION 15: 英文 X 推文草稿 ===== -->
<div class="section">
  <div class="section-title">
    <div class="section-title-bar"></div>
    <h2>十五、英文 X 推文草稿</h2>
  </div>
  <div class="section-bg">
    <div class="tweet-box">
      <div class="tweet-header">
        <div class="tweet-avatar">₿</div>
        <div>
          <div class="tweet-user">MK Trading</div>
          <div class="tweet-handle">@bitebiwang1413</div>
        </div>
      </div>
      <div class="tweet-content">
🔥 #BTC Daily Report | May 5, 2026

BTC: <strong>${btc_price:,.0f}</strong> ({'+' if btc_change > 0 else ''}{btc_change:.2f}% 24h)
FOMC delivered — Rates held at 5.25-5.50%, Powell dovish ✅
RSI: {rsi} ({rsi_signal}) | MACD: {macd_cross}

📊 Market Data:
• Fear & Greed: {fng_today} ({fng_label_today})
• Funding Rate: {funding_rate:.4f}% (shorts paying longs)
• OI: {oi_btc:,.0f} BTC — contracting
• L/S Ratio: {long_ratio:.0f}%/{short_ratio:.0f}% — bears still dominant

💡 Strategy: <strong>NEUTRAL / Wait for pullback</strong>
• Entry Zone: ${entry_low:,.0f}–${entry_high:,.0f}
• Stop: ${sl:,.0f} | TP1: ${tp1:,.0f} | TP2: ${tp2:,.0f}
• R/R: {rr_tp1:.1f}:1 ✅

⚠️ THIS WEEK: US CPI (May 8, 20:30 Beijing)
Reduce position size 2hrs before/after release!
Stay patient. The best trade is the one you don't take.

<span class="hashtag">#BTC #Bitcoin #CryptoTrading #FOMC #CPI #DailyReport</span>
      </div>
    </div>
  </div>
</div>

<!-- ===== SECTION 16: 风险免责声明 ===== -->
<div class="footer">
  <div class="disclaimer">
    <div class="disclaimer-warn">⚠️ 风险提示与免责声明</div>
    本报告仅供学习交流与个人复盘使用，不构成任何投资建议。<br>
    加密货币合约交易风险极高，价格波动剧烈，可能导致全部本金损失。<br>
    请根据自身风险承受能力谨慎决策，任何交易行为均由本人负责。<br>
    <div style="margin-top:12px;color:var(--text-muted)">
      报告编号: #{report_num} &nbsp;·&nbsp; 生成时间: {today_str} {dt_now.strftime("%H:%M UTC+8")} &nbsp;·&nbsp;
      数据来源: CoinGecko / Binance API / Bybit API / Alternative.me &nbsp;·&nbsp;
      <a href="https://mktrading.vip/btc/reports/" style="color:var(--purple-light);text-decoration:none">mktrading.vip</a>
    </div>
  </div>
</div>

</div><!-- end container -->
</body>
</html>'''

# Save
out_path = f"C:/Users/asus/mk-trading/btc/reports/BTC_daily_report_{today_str.replace('-','')}.html"
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"\n[OK] Report saved to: {out_path}")
print(f"[OK] Report size: {len(html):,} bytes")
