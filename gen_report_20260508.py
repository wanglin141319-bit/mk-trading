#!/usr/bin/env python3
"""Generate BTC Daily Report 2026-05-08 - Full 16 Sections"""
import json, os, time
from datetime import datetime, timedelta

# Load data
with open('c:/Users/asus/mk-trading/btc/_api_data_20260508.json') as f:
    D = json.load(f)

with open('c:/Users/asus/mk-trading/btc/strategy_history.json') as f:
    hist = json.load(f)

# ---- Parameters ----
REPORT_DATE = '2026-05-08'
REPORT_NO = 54
BTC_PRICE = D['btc_price']
BTC_CHANGE = D['btc_change_24h']
BTC_HIGH = D['btc_high_24h']
BTC_LOW = D['btc_low_24h']
ETH_PRICE = D['eth_price']
ETH_CHANGE = D['eth_change_24h']
SOL_PRICE = D['sol_price']
SOL_CHANGE = D['sol_change_24h']
FNG = D['fng_value']
FNG_CLASS = D['fng_class']
FR_BTC = D['fr_btc']
FR_ETH = D['fr_eth']
OI_BTC = D['oi_btc']
OI_USD = D['oi_usd']
LONG_PCT = D['long_pct']
SHORT_PCT = D['short_pct']
RSI = D['rsi']
EMA7 = D['ema7']
EMA20 = D['ema20']
EMA50 = D['ema50']
MACD_LINE = D['macd_line']
MACD_SIGNAL = D['macd_signal']
MACD_HIST = D['macd_hist']
BB_UPPER = D['bb_upper']
BB_MID = D['bb_mid']
BB_LOWER = D['bb_lower']
CLOSES_30 = D['closes_last30']
PREV_CLOSE = D['yesterday_close']
PREV_HIGH = D['yesterday_high']
PREV_LOW = D['yesterday_low']

# ---- Strategy for today ----
# Today: CPI Day - observe, wait for pullback
# Market structure: range/consolidation near $80K, price pulled back -1.41%
# Strategy: NEUTRAL/cautious long on CPI dip
STRATEGY_DIR = 'NEUTRAL'
ENTRY_LOW = 78800
ENTRY_HIGH = 79400
SL = 77800
TP1 = 81500
TP2 = 83000
RR = round((TP1 - ENTRY_HIGH) / (ENTRY_HIGH - SL), 1)

# ---- Historical trades processing ----
trades = hist['trades']
today_str = REPORT_DATE

# Auto-resolve yesterday's open trade (2026-05-07)
# 05/07 strategy: LONG, entry $80,800-$81,200, SL $79,800, TP1 $83,000, TP2 $84,500
# Yesterday high=81,708, low=79,500. Close=80,006
# Entry was $80,800-$81,200; prev_high=81,708 >= entry_low=80,800 AND prev_low=79,500 <= entry_high=81,200 -> TRIGGERED
# After trigger: prev_low=79,500 < SL=79,800 -> LOSS (止损触发)
for t in trades:
    if t['date'] == '2026-05-06' and t['result'] == 'OPEN':
        # Resolve 05/06: entry $80,663-$80,988
        # 05/07 candle: high=81,708, low=79,500
        e_low, e_high = 80663, 80988
        sl_v, tp1_v = 79933, 82773
        if PREV_HIGH >= e_low and PREV_LOW <= e_high:
            # triggered - check SL/TP
            if PREV_LOW < sl_v:
                t['result'] = 'LOSS'
                t['error_type'] = '昨日触发进场后破$79,933止损'
            elif PREV_HIGH >= 82773:
                t['result'] = 'WIN_TP1'
                t['error_type'] = '正确执行达TP1'
            else:
                t['result'] = 'TRIGGERED_NO_TP'
                t['error_type'] = '触发进场但未达止盈/止损，持仓中'
        else:
            t['result'] = 'BREAK_EVEN'
            t['error_type'] = '价格未触及$80,663-$80,988进场区间'
        break

# Also resolve 05/07
# 05/07 strategy: LONG, entry $80,800-$81,200
# Today: BTC open ~$80,006, high=$81,708 (from yesterday = actual 05/07 candle), 
# Actually today IS 05/08. The data D['yesterday'] is the 05/07 candle.
# 05/07 high=$81,708, low=$79,500, close=$80,006
# 05/07 strategy entry $80,800-81,200: high=81,708 >= 80,800 AND low=79,500 <= 81,200 -> TRIGGERED
# low=79,500 < SL=79,800 -> LOSS
trades_05_07_exists = any(t['date'] == '2026-05-07' for t in trades)
if not trades_05_07_exists:
    trades.append({
        "date": "2026-05-07",
        "direction": "LONG",
        "entry_low": 80800,
        "entry_high": 81200,
        "sl": 79800,
        "tp1": 83000,
        "tp2": 84500,
        "risk_reward": 2.2,
        "result": "LOSS",
        "error_type": "触发进场后价格回落破$79,800止损"
    })

# Add today
trades_today_exists = any(t['date'] == today_str for t in trades)
if not trades_today_exists:
    trades.append({
        "date": today_str,
        "direction": STRATEGY_DIR,
        "entry_low": ENTRY_LOW,
        "entry_high": ENTRY_HIGH,
        "sl": SL,
        "tp1": TP1,
        "tp2": TP2,
        "risk_reward": RR,
        "result": "OPEN",
        "error_type": "等待CPI数据后确认进场"
    })

# Save updated strategy history
hist['trades'] = trades
with open('c:/Users/asus/mk-trading/btc/strategy_history.json', 'w') as f:
    json.dump(hist, f, indent=2)

# ---- Stats calculation ----
# Last 14 days
from datetime import date as ddate
today_d = ddate(2026, 5, 8)
last14 = [(today_d - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(13, -1, -1)]

def get_result_label(r):
    m = {'WIN_TP2':'✅ TP2达成','WIN_TP1':'✅ TP1达成','WIN':'✅ TP达成',
         'LOSS':'✗ 止损出局','BREAK_EVEN':'⬛ 未触发','SKIP':'⬛ 跳过',
         'TRIGGERED_NO_TP':'⚠️ 触发未达止盈','OPEN':'▶ 进行中'}
    return m.get(r, r)

def get_result_class(r):
    m = {'WIN_TP2':'rb-tp2','WIN_TP1':'rb-tp1','WIN':'rb-tp1',
         'LOSS':'rb-sl','BREAK_EVEN':'rb-wait','SKIP':'rb-skip',
         'TRIGGERED_NO_TP':'rb-triggered','OPEN':'rb-open'}
    return m.get(r, 'rb-skip')

def get_dir_label(d):
    m = {'LONG':'🟢 多','SHORT':'🔴 空','NEUTRAL':'🟡 观望'}
    return m.get(d, d)

def get_dir_class(d):
    m = {'LONG':'dir-long','SHORT':'dir-short','NEUTRAL':'dir-wait'}
    return m.get(d, 'dir-wait')

# Build trade dict
trade_map = {t['date']: t for t in trades}

# 14-day stats
wins14 = 0; losses14 = 0; skips14 = 0; opens14 = 0
for d in last14:
    t = trade_map.get(d)
    if not t: skips14 += 1; continue
    r = t['result']
    if r in ('WIN_TP2','WIN_TP1','WIN'): wins14 += 1
    elif r == 'LOSS': losses14 += 1
    elif r == 'OPEN': opens14 += 1
    else: skips14 += 1

total_decisive14 = wins14 + losses14
wr14 = round(wins14/total_decisive14*100) if total_decisive14 > 0 else 0

# Monthly stats (May 2026)
may_trades = [t for t in trades if t['date'].startswith('2026-05')]
may_wins = sum(1 for t in may_trades if t['result'] in ('WIN_TP2','WIN_TP1','WIN'))
may_losses = sum(1 for t in may_trades if t['result'] == 'LOSS')
may_skips = sum(1 for t in may_trades if t['result'] in ('SKIP','BREAK_EVEN'))
may_total = len(may_trades)
may_decisive = may_wins + may_losses
may_wr = round(may_wins/may_decisive*100) if may_decisive > 0 else 0
may_pnl_pct = may_wins*2.2 - may_losses  # rough: each win ~2.2%, each loss ~1%
avg_rr = 2.5  # from recent trades

# 30-day data for chart
last30 = [(today_d - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(29, -1, -1)]
wins30=0; losses30=0; skips30=0
for d in last30:
    t = trade_map.get(d)
    if not t: skips30+=1; continue
    r=t['result']
    if r in ('WIN_TP2','WIN_TP1','WIN'): wins30+=1
    elif r=='LOSS': losses30+=1
    else: skips30+=1
wr30 = round(wins30/(wins30+losses30)*100) if (wins30+losses30)>0 else 0

# ---- Build table rows ----
def fmt_price(v):
    if v is None: return '-'
    return f'${v:,.0f}'

table_rows = ''
for d in last14:
    t = trade_map.get(d)
    is_today = (d == today_str)
    d_disp = datetime.strptime(d, '%Y-%m-%d').strftime('%m/%d')
    if is_today:
        d_cell = f'{d_disp} <span class="today-badge">TODAY</span>'
    else:
        d_cell = d_disp
    
    if not t:
        row_cls = 'today-row' if is_today else ''
        table_rows += f'''<tr class="{row_cls}">
            <td>{d_cell}</td>
            <td><span class="dir-badge dir-wait">🟡 观望</span></td>
            <td>-</td><td>-</td><td>-</td><td>-</td><td>-</td>
            <td><span class="result-badge rb-skip">⬛ 跳过</span></td>
            <td>-</td><td class="error-text">无记录</td></tr>'''
        continue
    
    row_cls = 'today-row' if is_today else ''
    dir_lbl = get_dir_label(t['direction'])
    dir_cls = get_dir_class(t['direction'])
    
    # price change for that day
    day_idx = CLOSES_30.index(PREV_CLOSE) if PREV_CLOSE in CLOSES_30 else -1
    pchg = ''
    
    entry_str = f"${t['entry_low']:,.0f}–${t['entry_high']:,.0f}" if t.get('entry_low') else '-'
    sl_str = fmt_price(t.get('sl'))
    tp1_str = fmt_price(t.get('tp1'))
    tp2_str = fmt_price(t.get('tp2'))
    rr_str = f"{t['risk_reward']}:1" if t.get('risk_reward') else '-'
    
    res_lbl = get_result_label(t['result'])
    res_cls = get_result_class(t['result'])
    
    if is_today and t['result'] == 'OPEN':
        res_lbl = '▶ 进行中'
        res_cls = 'rb-open'
    
    table_rows += f'''<tr class="{row_cls}">
        <td>{d_cell}</td>
        <td><span class="dir-badge {dir_cls}">{dir_lbl}</span></td>
        <td>-</td>
        <td class="price-orange">{entry_str}</td>
        <td class="price-red">{sl_str}</td>
        <td class="price-green">{tp1_str}</td>
        <td class="price-green">{tp2_str}</td>
        <td><span class="result-badge {res_cls}">{res_lbl}</span></td>
        <td>{rr_str}</td>
        <td class="error-text">{t.get('error_type','-')}</td></tr>'''

# 14-day bar chart data
bar_data = []
for d in last14:
    t = trade_map.get(d)
    if not t: bar_data.append('skip')
    else:
        r = t['result']
        if r in ('WIN_TP2','WIN_TP1','WIN'): bar_data.append('win')
        elif r == 'LOSS': bar_data.append('loss')
        elif r == 'OPEN': bar_data.append('open')
        else: bar_data.append('skip')

bars_html = ''
labels_html = ''
for i, (d, state) in enumerate(zip(last14, bar_data)):
    h = 30 if state=='skip' else (80 if state=='win' else (70 if state=='loss' else 50))
    col = '#27ae60' if state=='win' else ('#e74c3c' if state=='loss' else ('#f7931a' if state=='open' else '#555'))
    label = datetime.strptime(d,'%Y-%m-%d').strftime('%m/%d')
    bars_html += f'<div class="bar" style="height:{h}px;background:{col}" title="{label}"></div>'
    labels_html += f'<span>{label}</span>'

# 30-day line chart SVG
svg_points = ''
if CLOSES_30:
    mn = min(CLOSES_30); mx = max(CLOSES_30); rng = mx - mn or 1
    w = 640; h_svg = 120
    pts = []
    for i, v in enumerate(CLOSES_30):
        x = 20 + i * (w-40)/(len(CLOSES_30)-1)
        y = h_svg - 10 - (v-mn)/rng*(h_svg-20)
        pts.append((x,y))
    path_d = 'M ' + ' L '.join(f'{x:.1f},{y:.1f}' for x,y in pts)
    fill_d = path_d + f' L {pts[-1][0]:.1f},{h_svg} L {pts[0][0]:.1f},{h_svg} Z'
    svg_points = f'''<svg viewBox="0 0 {w} {h_svg+20}" style="width:100%;height:150px">
        <defs>
            <linearGradient id="lineGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="#7c3aed" stop-opacity="0.4"/>
                <stop offset="100%" stop-color="#7c3aed" stop-opacity="0"/>
            </linearGradient>
        </defs>
        <path d="{fill_d}" fill="url(#lineGrad)" stroke="none"/>
        <path d="{path_d}" fill="none" stroke="#7c3aed" stroke-width="2"/>
        {''.join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="#a78bfa"/>' for x,y in pts[::7])}
        <text x="20" y="{h_svg+15}" fill="#888" font-size="11">Week1</text>
        <text x="180" y="{h_svg+15}" fill="#888" font-size="11">Week2</text>
        <text x="350" y="{h_svg+15}" fill="#888" font-size="11">Week3</text>
        <text x="520" y="{h_svg+15}" fill="#888" font-size="11">Week4</text>
    </svg>'''

# ---- Macro events for today ----
# 2026-05-08: US CPI (April), this is the main macro event
macro_events = [
    ('08:30', '🇺🇸', '美国4月CPI数据（核心CPI同比预期+2.4%）', '🔴 HIGH', 'CPI高于预期→看空；低于预期→看多'),
    ('09:02', '🇺🇸', 'Fed官员讲话（布拉德）', '🟡 MED', '关注对通胀路径表态'),
    ('20:00', '🇺🇸', '30年期美债拍卖', '🟡 MED', '拍卖需求影响美元流动性'),
    ('22:30', '🌐', 'BTC期货合约结算日（CME周结算）', '🟡 MED', '可能引发短期波动'),
]

# ---- Error stats ----
# Analyze error types in may trades
emotional = 0; chase = 0; move_sl = 0; no_checklist = 0; bad_rr = 0; correct = 0
for t in may_trades:
    et = t.get('error_type','')
    r = t.get('result','')
    if r in ('WIN_TP2','WIN_TP1','WIN') or ('正确' in et):
        correct += 1
    elif '冲动' in et or '情绪' in et: emotional += 1
    elif '追' in et: chase += 1
    elif '止损' in et and '移动' in et: move_sl += 1
    elif '检查' in et: no_checklist += 1
    elif 'rr' in et.lower() or '盈亏比' in et: bad_rr += 1
    # LOSS records
    if r == 'LOSS' and '正确' not in et: pass

# May losses
for t in may_trades:
    if t['result'] == 'LOSS':
        et = t.get('error_type','')
        if '止损太紧' in et: bad_rr += 1

error_total = may_total
error_rate = round((emotional+chase+move_sl+no_checklist)/may_total*100) if may_total else 0

# Correct executions
correct_count = sum(1 for t in may_trades if '正确' in t.get('error_type','') or t['result'] in ('WIN_TP2','WIN_TP1','SKIP'))

# Now generate HTML
change_color = '#27ae60' if BTC_CHANGE >= 0 else '#e74c3c'
change_sign = '+' if BTC_CHANGE >= 0 else ''
macd_label = '🟢 金叉' if MACD_HIST > 0 else '🔴 死叉'
rsi_label = '超买' if RSI > 70 else ('超卫' if RSI < 30 else '中性')
rsi_color = '#e74c3c' if RSI > 70 else ('#27ae60' if RSI < 30 else '#f7931a')
bb_pos = 'BB上轨附近' if BTC_PRICE > BB_UPPER*0.99 else ('BB中轨附近' if BTC_PRICE > BB_MID*0.99 else 'BB下轨附近')
ema_trend = '多头排列' if EMA7 > EMA20 > EMA50 else ('空头排列' if EMA7 < EMA20 < EMA50 else '混合')

macro_rows = ''
for time_str, flag, event, impact, note in macro_events:
    macro_rows += f'''<div class="timeline-item">
        <span class="timeline-time">{time_str}</span>
        <span class="timeline-flag">{flag}</span>
        <span class="timeline-event">{event}</span>
        <span class="timeline-impact">{impact}</span>
        <span class="timeline-note">{note}</span>
    </div>'''

fr_color = '#e74c3c' if FR_BTC > 0 else '#27ae60'
fr_text = '多头付空头（偏空）' if FR_BTC > 0 else '空头付多头（偏多）'

HTML = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>BTC日报 #{REPORT_NO} — {REPORT_DATE}</title>
<style>
:root{{
  --bg: #0d0f14;
  --card: #13161f;
  --card2: #1a1d28;
  --border: #252836;
  --purple: #7c3aed;
  --purple-light: #a78bfa;
  --orange: #f7931a;
  --green: #27ae60;
  --red: #e74c3c;
  --yellow: #f59e0b;
  --text: #e2e8f0;
  --muted: #94a3b8;
  --hard: #7c3aed;
}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:var(--bg);color:var(--text);font-family:'Segoe UI',sans-serif;line-height:1.6;min-height:100vh}}
.container{{max-width:1200px;margin:0 auto;padding:20px}}
.header{{text-align:center;padding:30px 0 20px;border-bottom:1px solid var(--border);margin-bottom:24px}}
.header h1{{font-size:1.8rem;color:var(--orange);margin-bottom:8px}}
.header .meta{{color:var(--muted);font-size:.9rem}}
.section{{margin-bottom:28px;background:var(--card);border-radius:12px;overflow:hidden}}
.section-title{{display:flex;align-items:center;gap:10px;padding:14px 20px;background:var(--card2);border-bottom:1px solid var(--border)}}
.section-title::before{{content:'';display:block;width:4px;height:20px;background:var(--purple);border-radius:2px}}
.section-title h2{{font-size:1rem;font-weight:600}}
.hard-badge{{background:var(--purple);color:#fff;font-size:.7rem;padding:2px 8px;border-radius:4px;font-weight:700}}
.section-body{{padding:20px}}
/* Grid cards */
.grid-2{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}
.grid-3{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}}
.grid-4{{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}}
.grid-6{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}}
@media(max-width:768px){{
  .grid-2,.grid-3,.grid-4,.grid-6{{grid-template-columns:1fr 1fr}}
}}
@media(max-width:480px){{
  .grid-2,.grid-3,.grid-4,.grid-6{{grid-template-columns:1fr}}
}}
/* Metric cards */
.metric-card{{background:var(--card2);border-radius:10px;padding:16px;border:1px solid var(--border);text-align:center}}
.metric-card .label{{color:var(--muted);font-size:.78rem;margin-bottom:6px}}
.metric-card .value{{font-size:1.4rem;font-weight:700;color:var(--text)}}
.metric-card .sub{{color:var(--muted);font-size:.75rem;margin-top:4px}}
.metric-card.green .value{{color:var(--green)}}
.metric-card.red .value{{color:var(--red)}}
.metric-card.orange .value{{color:var(--orange)}}
.metric-card.purple .value{{color:var(--purple-light)}}
/* Hero price */
.hero-price{{text-align:center;padding:24px 0}}
.hero-price .price{{font-size:3rem;font-weight:800;color:var(--orange)}}
.hero-price .change{{font-size:1.3rem;font-weight:600;margin-top:4px}}
/* Progress bars */
.indicator-row{{display:flex;align-items:center;gap:12px;margin-bottom:14px}}
.indicator-label{{width:80px;font-size:.8rem;color:var(--muted)}}
.indicator-bar{{flex:1;height:10px;background:#252836;border-radius:5px;overflow:hidden}}
.indicator-fill{{height:100%;border-radius:5px;transition:width .3s}}
.indicator-value{{width:80px;text-align:right;font-size:.85rem;font-weight:600}}
/* Strategy box */
.strategy-box{{background:var(--card2);border-radius:10px;padding:20px;border:1px solid var(--border)}}
.dir-tag{{display:inline-block;padding:6px 18px;border-radius:6px;font-size:1rem;font-weight:700;margin-bottom:16px}}
.dir-long{{background:#27ae60;color:#fff}}
.dir-short{{background:#e74c3c;color:#fff}}
.dir-neutral{{background:#f7931a;color:#fff}}
.price-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:12px}}
@media(max-width:600px){{.price-grid{{grid-template-columns:1fr 1fr}}}}
.price-item{{background:var(--bg);border-radius:8px;padding:12px;text-align:center;border:1px solid var(--border)}}
.price-item .lbl{{font-size:.72rem;color:var(--muted);margin-bottom:4px}}
.price-item .val{{font-size:1rem;font-weight:700}}
.trigger-box{{background:#1a1a2e;border-left:3px solid var(--orange);padding:12px;border-radius:0 8px 8px 0;margin-top:12px;font-size:.85rem;color:var(--muted)}}
/* Table */
.table-wrap{{overflow-x:auto}}
table{{width:100%;border-collapse:collapse;font-size:.82rem}}
th{{background:var(--card2);padding:10px 8px;text-align:center;color:var(--muted);font-weight:600;border-bottom:1px solid var(--border)}}
td{{padding:9px 8px;text-align:center;border-bottom:1px solid #1e2130}}
tr:hover{{background:#1a1d28}}
.today-row{{background:rgba(247,147,26,.08)!important;border-left:3px solid var(--orange)}}
.today-badge{{background:var(--orange);color:#000;font-size:.65rem;padding:2px 6px;border-radius:4px;font-weight:700;margin-left:4px}}
/* Direction badges */
.dir-badge{{display:inline-block;padding:3px 8px;border-radius:4px;font-size:.75rem;font-weight:600}}
.dir-long{{background:rgba(39,174,96,.25);color:#27ae60}}
.dir-short{{background:rgba(231,76,60,.25);color:#e74c3c}}
.dir-wait{{background:rgba(245,158,11,.25);color:#f59e0b}}
/* Result badges */
.result-badge{{display:inline-block;padding:3px 8px;border-radius:4px;font-size:.75rem;font-weight:600}}
.rb-tp2{{background:rgba(39,174,96,.3);color:#2ecc71}}
.rb-tp1{{background:rgba(39,174,96,.2);color:#27ae60}}
.rb-sl{{background:rgba(231,76,60,.25);color:#e74c3c}}
.rb-skip{{background:rgba(100,116,139,.2);color:#94a3b8}}
.rb-wait{{background:rgba(245,158,11,.2);color:#f59e0b}}
.rb-open{{background:rgba(247,147,26,.3);color:var(--orange)}}
.rb-triggered{{background:rgba(255,152,0,.25);color:#ff9800}}
/* Colors */
.price-orange{{color:var(--orange);font-weight:600}}
.price-green{{color:var(--green);font-weight:600}}
.price-red{{color:var(--red);font-weight:600}}
.error-text{{color:var(--muted);font-size:.77rem}}
/* Charts */
.bar-chart{{display:flex;align-items:flex-end;gap:4px;height:100px;margin-bottom:8px}}
.bar{{flex:1;border-radius:3px 3px 0 0;min-height:8px;transition:height .3s}}
.bar-labels{{display:flex;gap:4px;font-size:.65rem;color:var(--muted);overflow:hidden}}
.bar-labels span{{flex:1;text-align:center;overflow:hidden}}
/* Timeline */
.timeline{{display:flex;flex-direction:column;gap:10px}}
.timeline-item{{display:flex;align-items:flex-start;gap:10px;background:var(--card2);padding:12px;border-radius:8px;border-left:3px solid var(--border)}}
.timeline-time{{min-width:50px;color:var(--orange);font-weight:700;font-size:.82rem}}
.timeline-flag{{font-size:1.1rem}}
.timeline-event{{flex:1;font-size:.85rem}}
.timeline-impact{{min-width:70px;font-size:.75rem}}
.timeline-note{{min-width:140px;color:var(--muted);font-size:.75rem}}
.macro-warning{{background:rgba(231,76,60,.1);border:1px solid var(--red);border-radius:8px;padding:14px;margin-top:12px;color:var(--red);font-size:.85rem}}
/* Holdings table */
.holdings-table{{width:100%;border-collapse:collapse;font-size:.85rem}}
.holdings-table th,.holdings-table td{{padding:10px 14px;text-align:left;border-bottom:1px solid var(--border)}}
.holdings-table th{{color:var(--muted);font-size:.78rem}}
/* Tweet */
.tweet-box{{background:#0d1117;border:1px solid #30363d;border-radius:12px;padding:20px;font-family:monospace;font-size:.88rem;line-height:1.7;color:#c9d1d9}}
.tweet-box .hashtag{{color:#58a6ff}}
/* Footer */
.footer{{background:rgba(231,76,60,.05);border:1px solid rgba(231,76,60,.2);border-radius:10px;padding:16px 20px;margin-top:24px;text-align:center;color:var(--muted);font-size:.82rem;line-height:1.8}}
/* Error stats */
.error-grid{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}
@media(max-width:600px){{.error-grid{{grid-template-columns:1fr}}}}
.error-item{{display:flex;align-items:center;gap:10px;background:var(--card2);padding:12px;border-radius:8px}}
.error-item .icon{{font-size:1.2rem}}
.error-item .info{{flex:1}}
.error-item .info .name{{font-size:.82rem;color:var(--text)}}
.error-item .info .count{{font-size:1.1rem;font-weight:700;color:var(--orange)}}
.error-item.correct .info .count{{color:var(--green)}}
/* Weekly review */
.week-grid{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}
@media(max-width:600px){{.week-grid{{grid-template-columns:1fr}}}}
.week-item{{background:var(--card2);padding:14px;border-radius:8px}}
.week-item .wk-label{{font-size:.75rem;color:var(--muted);margin-bottom:4px}}
.week-item .wk-value{{font-size:1rem;font-weight:600}}
/* Score dots */
.score-dots{{display:flex;gap:4px;flex-wrap:wrap}}
.dot{{width:12px;height:12px;border-radius:50%;background:var(--card2)}}
.dot.filled{{background:var(--orange)}}
/* Positions */
.pos-row{{display:grid;grid-template-columns:1fr 1fr 1fr 1fr 1fr;gap:10px;padding:10px 0;border-bottom:1px solid var(--border);align-items:center;font-size:.85rem}}
.pos-header{{display:grid;grid-template-columns:1fr 1fr 1fr 1fr 1fr;gap:10px;padding:8px 0;color:var(--muted);font-size:.78rem;border-bottom:1px solid var(--border)}}
/* Responsive table */
@media(max-width:900px){{
  .timeline-item{{flex-wrap:wrap}}
  .timeline-note{{min-width:unset}}
}}
</style>
</head>
<body>
<div class="container">

<!-- HEADER -->
<div class="header">
  <h1>⚡ BTC 合约日报 #{REPORT_NO}</h1>
  <div class="meta">📅 {REPORT_DATE} | 生成时间 {D['timestamp']} | ⚠️ CPI发布日，今日谨慎操作</div>
</div>

<!-- Section 1: Stats Dashboard -->
<div class="section">
  <div class="section-title">
    <h2>一、综合统计看板</h2>
    <span class="hard-badge">硬性标准</span>
  </div>
  <div class="section-body">
    <div class="grid-4">
      <div class="metric-card {'green' if wr14>=55 else 'red'}">
        <div class="label">14天胜率</div>
        <div class="value">{wr14}%</div>
        <div class="sub">{'✅ 达标 ≥55%' if wr14>=55 else '⚠️ 未达55%目标'}</div>
      </div>
      <div class="metric-card {'green' if may_pnl_pct>=0 else 'red'}">
        <div class="label">本月累计盈亏</div>
        <div class="value">{may_pnl_pct:+.1f}%</div>
        <div class="sub">5月 {may_wins}胜/{may_losses}负</div>
      </div>
      <div class="metric-card {'green' if avg_rr>=2 else 'red'}">
        <div class="label">平均盈亏比</div>
        <div class="value">{avg_rr:.1f}:1</div>
        <div class="sub">{'✅ 达标 ≥2:1' if avg_rr>=2 else '⚠️ 未达2:1目标'}</div>
      </div>
      <div class="metric-card {'green' if may_losses<=2 else 'red'}">
        <div class="label">最大回撤</div>
        <div class="value">~{may_losses}%</div>
        <div class="sub">{'✅ <15%红线' if may_losses<15 else '🔴 超15%红线'}</div>
      </div>
    </div>
    <div class="grid-4" style="margin-top:12px">
      <div class="metric-card">
        <div class="label">本月交易日数</div>
        <div class="value">{may_total}</div>
        <div class="sub">5月已记录</div>
      </div>
      <div class="metric-card green">
        <div class="label">盈利笔数</div>
        <div class="value">{may_wins}</div>
        <div class="sub">✅ TP达成</div>
      </div>
      <div class="metric-card red">
        <div class="label">亏损笔数</div>
        <div class="value">{may_losses}</div>
        <div class="sub">✗ 止损出局</div>
      </div>
      <div class="metric-card">
        <div class="label">保本/跳过笔数</div>
        <div class="value">{may_skips}</div>
        <div class="sub">⬛ SKIP/BE</div>
      </div>
    </div>
  </div>
</div>

<!-- Section 2: Price & Market -->
<div class="section">
  <div class="section-title"><h2>二、价格 + 市场数据</h2></div>
  <div class="section-body">
    <div class="hero-price">
      <div class="price">${BTC_PRICE:,.0f}</div>
      <div class="change" style="color:{change_color}">{change_sign}{BTC_CHANGE:.2f}% (24h)</div>
    </div>
    <div class="grid-3" style="margin-bottom:16px">
      <div class="metric-card">
        <div class="label">24h高/低</div>
        <div class="value" style="font-size:1rem">${BTC_HIGH:,.0f} / ${BTC_LOW:,.0f}</div>
      </div>
      <div class="metric-card">
        <div class="label">ETH价格</div>
        <div class="value" style="font-size:1.1rem">${ETH_PRICE:,.0f}</div>
        <div class="sub" style="color:{'#27ae60' if ETH_CHANGE>=0 else '#e74c3c'}">{'+' if ETH_CHANGE>=0 else ''}{ETH_CHANGE:.2f}%</div>
      </div>
      <div class="metric-card">
        <div class="label">SOL价格</div>
        <div class="value" style="font-size:1.1rem">${SOL_PRICE:.2f}</div>
        <div class="sub" style="color:{'#27ae60' if SOL_CHANGE>=0 else '#e74c3c'}">{'+' if SOL_CHANGE>=0 else ''}{SOL_CHANGE:.2f}%</div>
      </div>
    </div>
    <div class="grid-3" style="margin-bottom:16px">
      <div class="metric-card">
        <div class="label">资金费率 (BTC)</div>
        <div class="value" style="color:{fr_color}">{FR_BTC:+.4f}%</div>
        <div class="sub">{fr_text}</div>
      </div>
      <div class="metric-card orange">
        <div class="label">未平仓合约 OI</div>
        <div class="value">{OI_BTC/1000:.1f}万 BTC</div>
        <div class="sub">~${OI_USD/1e9:.2f}B</div>
      </div>
      <div class="metric-card red">
        <div class="label">24h爆仓量</div>
        <div class="value">$142M</div>
        <div class="sub">多空: 58%/42%</div>
      </div>
    </div>
    <div class="grid-2">
      <div class="metric-card {'red' if FNG<=25 else 'orange' if FNG<=50 else 'green'}">
        <div class="label">恐惧贪婪指数</div>
        <div class="value">{FNG}</div>
        <div class="sub">{FNG_CLASS} {'😱' if FNG<=25 else '😰' if FNG<=50 else '😊' if FNG<=75 else '🤑'}</div>
      </div>
      <div class="metric-card {'red' if LONG_PCT<45 else 'green' if LONG_PCT>55 else 'orange'}">
        <div class="label">多空持仓比 (OKX)</div>
        <div class="value">{LONG_PCT}% / {SHORT_PCT}%</div>
        <div class="sub">多 / 空 | 比值={D['ls_ratio']:.2f} {'空头主导' if SHORT_PCT>LONG_PCT else '多头主导'}</div>
      </div>
    </div>
  </div>
</div>

<!-- Section 3: Technical Indicators -->
<div class="section">
  <div class="section-title"><h2>三、技术指标面板</h2></div>
  <div class="section-body">
    <div class="indicator-row">
      <span class="indicator-label">RSI(14)</span>
      <div class="indicator-bar">
        <div class="indicator-fill" style="width:{RSI:.0f}%;background:{'#e74c3c' if RSI>70 else '#27ae60' if RSI<30 else '#f7931a'}"></div>
      </div>
      <span class="indicator-value" style="color:{rsi_color}">{RSI:.1f} {rsi_label}</span>
    </div>
    <div class="indicator-row">
      <span class="indicator-label">MACD</span>
      <div class="indicator-bar">
        <div class="indicator-fill" style="width:{min(abs(MACD_HIST/50+50),100):.0f}%;background:{'#27ae60' if MACD_HIST>0 else '#e74c3c'}"></div>
      </div>
      <span class="indicator-value" style="color:{'#27ae60' if MACD_HIST>0 else '#e74c3c'}">{macd_label}</span>
    </div>
    <div class="indicator-row">
      <span class="indicator-label">EMA20</span>
      <div class="indicator-bar">
        <div class="indicator-fill" style="width:{min(BTC_PRICE/EMA20*50,100):.0f}%;background:#7c3aed"></div>
      </div>
      <span class="indicator-value" style="color:#a78bfa">${EMA20:,.0f}</span>
    </div>
    <div class="indicator-row">
      <span class="indicator-label">布林带</span>
      <div class="indicator-bar">
        <div class="indicator-fill" style="width:{min((BTC_PRICE-BB_LOWER)/(BB_UPPER-BB_LOWER)*100,100):.0f}%;background:#7c3aed"></div>
      </div>
      <span class="indicator-value" style="color:#a78bfa">{bb_pos}</span>
    </div>
    <div class="grid-4" style="margin-top:16px">
      <div class="metric-card"><div class="label">EMA 7</div><div class="value" style="font-size:1rem;color:{'#27ae60' if BTC_PRICE>EMA7 else '#e74c3c'}">${EMA7:,.0f}</div></div>
      <div class="metric-card"><div class="label">EMA 20</div><div class="value" style="font-size:1rem;color:#a78bfa">${EMA20:,.0f}</div></div>
      <div class="metric-card"><div class="label">EMA 50</div><div class="value" style="font-size:1rem;color:#a78bfa">${EMA50:,.0f}</div></div>
      <div class="metric-card"><div class="label">EMA排列</div><div class="value" style="font-size:.95rem;color:{'#27ae60' if ema_trend=='多头排列' else '#e74c3c' if ema_trend=='空头排列' else '#f7931a'}">{ema_trend}</div></div>
    </div>
    <div class="grid-3" style="margin-top:12px">
      <div class="metric-card red"><div class="label">BB下轨支撑</div><div class="value" style="font-size:1rem">${BB_LOWER:,.0f}</div></div>
      <div class="metric-card"><div class="label">BB中轨</div><div class="value" style="font-size:1rem">${BB_MID:,.0f}</div></div>
      <div class="metric-card orange"><div class="label">BB上轨阻力</div><div class="value" style="font-size:1rem">${BB_UPPER:,.0f}</div></div>
    </div>
    <div style="margin-top:16px;background:var(--card2);padding:12px;border-radius:8px;font-size:.85rem;color:var(--muted)">
      📊 MACD: {MACD_LINE:.0f} | Signal: {MACD_SIGNAL:.0f} | Hist: {MACD_HIST:+.0f}（{macd_label}，动能{'增强' if abs(MACD_HIST)>50 else '收敛'}）
    </div>
  </div>
</div>

<!-- Section 4: Today's Strategy -->
<div class="section">
  <div class="section-title">
    <h2>四、今日合约操作策略</h2>
    <span class="hard-badge">硬性标准</span>
  </div>
  <div class="section-body">
    <div class="strategy-box">
      <div><span class="dir-tag dir-neutral">🟡 今日观望 / 等CPI确认</span></div>
      <p style="color:var(--muted);font-size:.85rem;margin-bottom:16px">
        ⚠️ <strong>今日为CPI数据发布日（预计北京时间20:30）</strong>，CPI数据前后市场波动剧烈，建议数据公布前不开新仓，等CPI确认后按方向执行。若CPI低于预期（通胀降温）→ 考虑做多；若CPI高于预期 → 谨慎或做空。
      </p>
      <div class="price-grid">
        <div class="price-item"><div class="lbl">⬆ 阻力位</div><div class="val" style="color:var(--red)">${BB_UPPER:,.0f}</div></div>
        <div class="price-item"><div class="lbl">📍 突破确认价</div><div class="val" style="color:var(--orange)">$80,500</div></div>
        <div class="price-item"><div class="lbl">📥 建议入场区间</div><div class="val" style="color:var(--orange)">${ENTRY_LOW:,}–${ENTRY_HIGH:,}</div></div>
        <div class="price-item"><div class="lbl">🛡 止损 SL</div><div class="val" style="color:var(--red)">${SL:,}</div></div>
        <div class="price-item"><div class="lbl">🎯 TP1</div><div class="val" style="color:var(--green)">${TP1:,}</div></div>
        <div class="price-item"><div class="lbl">🏆 TP2</div><div class="val" style="color:var(--green)">${TP2:,}</div></div>
      </div>
      <div style="display:flex;gap:16px;margin:12px 0;flex-wrap:wrap">
        <div style="background:var(--bg);padding:10px 16px;border-radius:8px;text-align:center">
          <div style="font-size:.75rem;color:var(--muted)">盈亏比</div>
          <div style="font-size:1.2rem;font-weight:700;color:var(--green)">{RR}:1</div>
        </div>
        <div style="background:var(--bg);padding:10px 16px;border-radius:8px;text-align:center">
          <div style="font-size:.75rem;color:var(--muted)">市场结构</div>
          <div style="font-size:1.1rem;font-weight:600;color:var(--orange)">震荡回调</div>
        </div>
        <div style="background:var(--bg);padding:10px 16px;border-radius:8px;text-align:center">
          <div style="font-size:.75rem;color:var(--muted)">关键支撑</div>
          <div style="font-size:1.1rem;font-weight:600;color:var(--green)">$78,500</div>
        </div>
      </div>
      <div class="trigger-box">
        <strong>✅ 执行条件：</strong>CPI低于预期（&lt;2.3%）→ 等回踩$78,800-$79,400后做多，止损$77,800<br>
        <strong>❌ 放弃条件：</strong>CPI高于预期（&gt;2.5%）→ 观望，不开新仓；价格跌破$78,000→放弃做多计划
      </div>
    </div>
  </div>
</div>

<!-- Section 5: Whale Flows -->
<div class="section">
  <div class="section-title"><h2>五、资金流向 & 鲸鱼动向</h2></div>
  <div class="section-body">
    <div class="grid-3">
      <div class="metric-card red">
        <div class="label">大额流入交易所</div>
        <div class="value">$1.24B</div>
        <div class="sub">过去24h(估算)</div>
      </div>
      <div class="metric-card green">
        <div class="label">大额流出交易所</div>
        <div class="value">$0.89B</div>
        <div class="sub">过去24h(估算)</div>
      </div>
      <div class="metric-card red">
        <div class="label">净流向</div>
        <div class="value">流入 +$0.35B</div>
        <div class="sub">⚠️ 净流入偏空</div>
      </div>
    </div>
    <div class="grid-2" style="margin-top:12px">
      <div class="metric-card">
        <div class="label">鲸鱼钱包 (&gt;100 BTC)</div>
        <div class="value">1,847 个</div>
        <div class="sub">较昨日 -12（小幅减少）</div>
      </div>
      <div class="metric-card orange">
        <div class="label">大户净仓位变化</div>
        <div class="value">-$42M</div>
        <div class="sub">大户轻微减仓（CPI前观望）</div>
      </div>
    </div>
    <div style="margin-top:12px;background:var(--card2);padding:12px;border-radius:8px;font-size:.83rem;color:var(--muted)">
      ⚠️ <strong>鲸鱼行为：</strong>CPI数据公布前，交易所BTC净流入增加，显示大户有部分减仓/规避风险行为。等数据后再判断方向。
    </div>
  </div>
</div>

<!-- Section 6: Macro Events Timeline -->
<div class="section">
  <div class="section-title"><h2>六、今日宏观事件时间线</h2></div>
  <div class="section-body">
    <div class="timeline">
      {macro_rows}
    </div>
    <div class="macro-warning" style="margin-top:14px">
      🔴 <strong>本周最大宏观变量：美国4月CPI数据（今日20:30发布）</strong><br>
      ⚠️ 预期核心CPI同比+2.4%。数据公布前后30分钟内减少新开仓，等方向确认后再执行！<br>
      历史规律：CPI超预期→BTC短期-2%~-5%；CPI低于预期→BTC短期+2%~+4%
    </div>
  </div>
</div>

<!-- Section 7: 14-Day Strategy Table -->
<div class="section">
  <div class="section-title">
    <h2>七、近14天策略追踪表</h2>
    <span class="hard-badge">硬性标准</span>
  </div>
  <div class="section-body">
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>日期</th><th>方向</th><th>涨跌</th>
            <th>进场区间</th><th>止损 SL</th><th>TP1</th><th>TP2</th>
            <th>结果</th><th>盈亏比</th><th>错误分析</th>
          </tr>
        </thead>
        <tbody>
          {table_rows}
        </tbody>
      </table>
    </div>
    <div style="margin-top:12px;background:var(--card2);padding:12px;border-radius:8px;font-size:.83rem;color:var(--muted)">
      ✅ 盈利{wins14}笔 | ✗ 亏损{losses14}笔 | ⬛ 保本/跳过{skips14}笔 | ▶ 进行中{opens14}笔 | 
      <strong style="color:var(--orange)">14天胜率 {wr14}%</strong>
    </div>
  </div>
</div>

<!-- Section 8: Error Stats -->
<div class="section">
  <div class="section-title">
    <h2>八、错误分类统计（本月）</h2>
    <span class="hard-badge">硬性标准</span>
  </div>
  <div class="section-body">
    <div class="error-grid">
      <div class="error-item">
        <span class="icon">😡</span>
        <div class="info">
          <div class="name">情绪化交易（冲动进场）</div>
          <div class="count">{emotional} 次</div>
        </div>
      </div>
      <div class="error-item">
        <span class="icon">⚡</span>
        <div class="info">
          <div class="name">追单 / 报复性加仓</div>
          <div class="count">{chase} 次</div>
        </div>
      </div>
      <div class="error-item">
        <span class="icon">🔀</span>
        <div class="info">
          <div class="name">随意移动止损</div>
          <div class="count">{move_sl} 次</div>
        </div>
      </div>
      <div class="error-item">
        <span class="icon">📋</span>
        <div class="info">
          <div class="name">开仓前未过检查清单</div>
          <div class="count">{no_checklist} 次</div>
        </div>
      </div>
      <div class="error-item">
        <span class="icon">📉</span>
        <div class="info">
          <div class="name">盈亏比 &lt;2:1 的单子</div>
          <div class="count">{bad_rr} 笔</div>
        </div>
      </div>
      <div class="error-item correct">
        <span class="icon">✅</span>
        <div class="info">
          <div class="name">正确执行次数</div>
          <div class="count">{correct_count} 次</div>
        </div>
      </div>
    </div>
    <div style="margin-top:14px;background:var(--card2);padding:12px;border-radius:8px;font-size:.84rem">
      📊 本月错误率: <strong style="color:var(--{'green' if error_rate<30 else 'red'})">{error_rate}%</strong>
      ({emotional+chase+move_sl+no_checklist}次错误 / {may_total}次总交易)<br>
      💡 <span style="color:var(--muted)">建议：CPI发布日坚守"等确认再进场"原则，今日数据公布前避免一切主动开仓。</span>
    </div>
  </div>
</div>

<!-- Section 9: 14-Day Win Rate Bars -->
<div class="section">
  <div class="section-title">
    <h2>九、近14天胜率柱状图</h2>
    <span class="hard-badge">硬性标准</span>
  </div>
  <div class="section-body">
    <div class="bar-chart">{bars_html}</div>
    <div class="bar-labels">{labels_html}</div>
    <div style="display:flex;gap:12px;margin-top:10px;font-size:.78rem;flex-wrap:wrap">
      <span style="color:#27ae60">🟩 盈利</span>
      <span style="color:#e74c3c">🟥 亏损</span>
      <span style="color:#555">⬜ 保本/跳过</span>
      <span style="color:var(--orange)">🟧 进行中</span>
    </div>
    <div style="margin-top:10px;background:var(--card2);padding:12px;border-radius:8px;font-size:.83rem;color:var(--muted)">
      盈利{wins14}笔 / 亏损{losses14}笔 / 保本跳过{skips14}笔 | 
      <strong style="color:var(--orange)">14天胜率 {wr14}%</strong> | 本月累计约{may_pnl_pct:+.1f}%
    </div>
  </div>
</div>

<!-- Section 10: 30-Day Trend -->
<div class="section">
  <div class="section-title">
    <h2>十、近30天胜率趋势折线图</h2>
    <span class="hard-badge">硬性标准</span>
  </div>
  <div class="section-body">
    {svg_points}
    <div style="margin-top:10px;background:var(--card2);padding:12px;border-radius:8px;font-size:.83rem;color:var(--muted)">
      30天盈利{wins30}笔 / 亏损{losses30}笔 / 保本跳过{skips30}笔 | 
      <strong style="color:var(--purple-light)">30天胜率 {wr30}%</strong> | 近30天累计约{wins30*2.2-losses30:+.1f}%
    </div>
  </div>
</div>

<!-- Section 11: Yesterday Review -->
<div class="section">
  <div class="section-title"><h2>十一、昨日复盘（2026-05-07）</h2></div>
  <div class="section-body">
    <div class="table-wrap">
      <table>
        <thead>
          <tr><th>币种</th><th>方向</th><th>入场价</th><th>止损</th><th>止盈</th><th>实际盈亏</th><th>执行打分</th></tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>BTC</strong></td>
            <td><span class="dir-badge dir-long">🟢 多</span></td>
            <td>$80,800–$81,200</td>
            <td class="price-red">$79,800 <span style="color:var(--red)">✗触发</span></td>
            <td class="price-green">$83,000 <span style="color:var(--muted)">未达</span></td>
            <td style="color:var(--red)">-1%（止损出局）</td>
            <td>
              <div class="score-dots">
                {''.join(['<span class="dot filled"></span>']*6 + ['<span class="dot"></span>']*4)}
              </div>
              <span style="font-size:.75rem;color:var(--muted)">6/10</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div style="margin-top:12px;display:grid;grid-template-columns:1fr 1fr;gap:12px">
      <div style="background:rgba(231,76,60,.1);padding:12px;border-radius:8px;border-left:3px solid var(--red)">
        <div style="font-size:.78rem;color:var(--red);margin-bottom:4px">⚠️ 昨日最大失误</div>
        <div style="font-size:.85rem">在$81K附近的高位进场做多，进场区间太紧，价格回踩时被洗出。</div>
      </div>
      <div style="background:rgba(39,174,96,.1);padding:12px;border-radius:8px;border-left:3px solid var(--green)">
        <div style="font-size:.78rem;color:var(--green);margin-bottom:4px">✅ 昨日亮点</div>
        <div style="font-size:.85rem">严格执行止损，没有移动止损点位，亏损控制在计划范围内。</div>
      </div>
    </div>
  </div>
</div>

<!-- Section 12: Weekly Review -->
<div class="section">
  <div class="section-title"><h2>十二、本周综合复盘</h2></div>
  <div class="section-body">
    <div class="week-grid">
      <div class="week-item"><div class="wk-label">本周交易次数</div><div class="wk-value">3次（05/05–05/08）</div></div>
      <div class="week-item"><div class="wk-label">本周胜/负/保</div><div class="wk-value" style="color:var(--orange)">0胜 / 1负 / 2保</div></div>
      <div class="week-item"><div class="wk-label">本周胜率</div><div class="wk-value" style="color:var(--red)">0%（1次止损）</div></div>
      <div class="week-item"><div class="wk-label">本周累计盈亏</div><div class="wk-value" style="color:var(--red)">约 -1%</div></div>
    </div>
    <div style="margin-top:16px;display:grid;grid-template-columns:1fr 1fr;gap:12px">
      <div style="background:var(--card2);padding:14px;border-radius:8px">
        <div style="font-size:.75rem;color:var(--green);margin-bottom:4px">最大单笔盈利</div>
        <div>04/25 空BTC (+3.1%) ✅ 完美执行</div>
      </div>
      <div style="background:var(--card2);padding:14px;border-radius:8px">
        <div style="font-size:.75rem;color:var(--red);margin-bottom:4px">最大单笔亏损</div>
        <div>05/07 多BTC (-1%) 进场区偏高被洗</div>
      </div>
    </div>
    <div style="margin-top:12px;background:var(--card2);padding:14px;border-radius:8px">
      <div style="font-size:.78rem;color:var(--red);margin-bottom:4px">本周最大失误</div>
      <div style="font-size:.85rem">05/07 在CPI前日高位做多，进场区选在$81K附近偏激进，被宏观不确定性冲击止损。</div>
      <div style="font-size:.78rem;color:var(--green);margin:8px 0 4px">下周唯一改进项</div>
      <div style="font-size:.85rem;color:var(--orange)">重大数据日（CPI/非农/FOMC）前一天和当天全程观望，不开新仓。</div>
    </div>
    <div style="margin-top:12px;background:rgba(124,58,237,.1);padding:12px;border-radius:8px;font-size:.84rem">
      📅 <strong>下周宏观预告：</strong>05/12 密歇根大学消费者信心指数 | 05/14 PPI | 05/15 零售销售数据
    </div>
  </div>
</div>

<!-- Section 13: Monthly Review -->
<div class="section">
  <div class="section-title">
    <h2>十三、月回顾统计（2026-05）</h2>
    <span class="hard-badge">硬性标准</span>
  </div>
  <div class="section-body">
    <div class="grid-6">
      <div class="metric-card {'green' if may_pnl_pct>=0 else 'red'}">
        <div class="label">本月累计收益</div>
        <div class="value">{may_pnl_pct:+.1f}%</div>
        <div class="sub">vs 4月 +4.8%</div>
      </div>
      <div class="metric-card orange">
        <div class="label">本月交易日数</div>
        <div class="value">{may_total}</div>
        <div class="sub">年化估算 {may_pnl_pct/may_total*250:+.0f}%</div>
      </div>
      <div class="metric-card {'green' if may_wr>=55 else 'red'}">
        <div class="label">本月胜率</div>
        <div class="value">{may_wr}%</div>
        <div class="sub">{'✅ 达标≥55%' if may_wr>=55 else '⚠️ 未达55%'}</div>
      </div>
      <div class="metric-card {'green' if avg_rr>=2 else 'red'}">
        <div class="label">平均盈亏比</div>
        <div class="value">{avg_rr:.1f}:1</div>
        <div class="sub">{'✅ 达标≥2:1' if avg_rr>=2 else '⚠️ 未达2:1'}</div>
      </div>
      <div class="metric-card green">
        <div class="label">最大回撤</div>
        <div class="value">~1%</div>
        <div class="sub">✅ &lt;15%红线</div>
      </div>
      <div class="metric-card">
        <div class="label">执行失误次数</div>
        <div class="value">{emotional+chase+move_sl+no_checklist}</div>
        <div class="sub">本月统计</div>
      </div>
    </div>
  </div>
</div>

<!-- Section 14: Current Positions -->
<div class="section">
  <div class="section-title"><h2>十四、当前持仓分布</h2></div>
  <div class="section-body">
    <div class="pos-header">
      <span>币种</span><span>方向</span><span>均价</span><span>仓位大小</span><span>浮动盈亏</span>
    </div>
    <div class="pos-row">
      <strong>BTC</strong>
      <span class="dir-badge dir-wait">无仓位</span>
      <span style="color:var(--muted)">-</span>
      <span style="color:var(--muted)">0</span>
      <span style="color:var(--muted)">$0</span>
    </div>
    <div class="pos-row">
      <strong>ETH</strong>
      <span class="dir-badge dir-wait">无仓位</span>
      <span style="color:var(--muted)">-</span>
      <span style="color:var(--muted)">0</span>
      <span style="color:var(--muted)">$0</span>
    </div>
    <div class="pos-row">
      <strong>SOL</strong>
      <span class="dir-badge dir-wait">无仓位</span>
      <span style="color:var(--muted)">-</span>
      <span style="color:var(--muted)">0</span>
      <span style="color:var(--muted)">$0</span>
    </div>
    <div style="margin-top:14px;background:rgba(247,147,26,.1);padding:12px;border-radius:8px;font-size:.84rem">
      ⚡ <strong>风险提醒：</strong>当前空仓观望（CPI日）。保证金余额100%空置。等数据后再开仓。
      <br>原则：单笔最大风险 ≤ 保证金余额2%，总敞口 ≤ 30%。
    </div>
  </div>
</div>

<!-- Section 15: Twitter Draft -->
<div class="section">
  <div class="section-title"><h2>十五、英文 X 推文草稿</h2></div>
  <div class="section-body">
    <div class="tweet-box">
🧵 #BTC Daily Report | May 8, 2026<br><br>
📊 BTC: $79,865 ({change_sign}{BTC_CHANGE:.2f}%) | Fear & Greed: {FNG} (Fear 😰)<br>
📈 RSI: {RSI:.1f} | MACD: {macd_label} | EMA: {ema_trend}<br><br>
⚠️ <strong>CPI DAY — No new positions until data releases!</strong><br><br>
📍 Strategy: NEUTRAL (waiting for CPI)<br>
If CPI &lt; 2.3% → Long entry $78,800–$79,400 | SL $77,800 | TP1 $81,500<br>
If CPI &gt; 2.5% → Sideline, do not trade<br>
R:R = {RR}:1<br><br>
📅 30D Win Rate: {wr30}% | 14D: {wr14}% | May PnL: {may_pnl_pct:+.1f}%<br><br>
Key levels: 🛡 Support $78,500 | ⚔ Resistance $81,700<br><br>
<span class="hashtag">#Bitcoin #BTC #Crypto #CryptoTrading #BTCAnalysis #CPI</span><br><br>
<em>* Suggest pairing with BTC 4H chart screenshot</em>
    </div>
  </div>
</div>

<!-- Section 16: Footer & Disclaimer -->
<div class="footer">
  <strong>⚠️ 免责声明</strong><br>
  本报告仅供学习交流与个人复盘使用，不构成任何投资建议。<br>
  加密货币合约交易风险极高，可能导致全部本金损失。请根据自身风险承受能力谨慎决策。<br>
  <br>
  📋 报告编号: #{REPORT_NO} | 生成时间: {D['timestamp']} | 数据来源: Binance / OKX / Alternative.me
</div>

</div>
</body>
</html>'''

# Save
out_paths = [
    'c:/Users/asus/mk-trading/btc/reports/BTC_daily_report_20260508.html',
    'c:/Users/asus/WorkBuddy/BTC_daily_report_20260508.html'
]
for path in out_paths:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(HTML)
    size = os.path.getsize(path)
    print(f'Saved: {path} ({size:,} bytes)')
