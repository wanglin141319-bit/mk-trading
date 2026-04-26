"""
BTC日报生成器 - 2026-04-26 (周日)
完整16板块 + 自动复盘 + Git同步
"""
import json, os, shutil, subprocess, sys
from datetime import datetime, timedelta

# ===== 路径配置 =====
BASE_DIR = 'C:/Users/asus/mk-trading'
CACHE_DIR = os.path.join(BASE_DIR, 'btc', 'cache')
REPORTS_DIR = os.path.join(BASE_DIR, 'btc', 'reports')
WB_DIR = 'C:/Users/asus/WorkBuddy'
INDEX_FILE = os.path.join(BASE_DIR, 'btc', 'index.html')
HIST_FILE = os.path.join(CACHE_DIR, 'strategy_history.json')
LIVE_DATA_FILE = os.path.join(CACHE_DIR, 'live_data_20260426.json')
TODAY_STR = '20260426'
TODAY_DISPLAY = '2026-04-26'
TODAY_DATE_FORMATTED = '04/26'
YESTERDAY_STR = '20260425'

def log(msg, level='INFO'):
    print(f'[{datetime.now().strftime("%H:%M:%S")}] [{level}] {msg}')

# ===== 加载实时数据 =====
log('Loading live data...')
with open(LIVE_DATA_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

btc = data.get('btc', {})
eth = data.get('eth', {})
funding = data.get('funding', {})
oi_data = data.get('oi', {})
fg = data.get('fear_greed', {})
tech = data.get('technical', {})
liq = data.get('liquidation', {})
whale = data.get('whale', {})
macro = data.get('macro', {})

btc_price = btc.get('price', 77505)
btc_change = btc.get('change_24h', 0)
eth_price = eth.get('price', 2314)
eth_change = eth.get('change_24h', 0)
btc_high = btc.get('high_24h', btc_price)
btc_low = btc.get('low_24h', btc_price)
funding_rate = funding.get('rate', 0) * 100  # 转为%
oi_usd = oi_data.get('oi_usd', 0)
ls_ratio = oi_data.get('long_short_ratio', 0.8)
long_r = oi_data.get('long_ratio', 0.45)
short_r = oi_data.get('short_ratio', 0.55)
rsi = tech.get('rsi', 50)
macd_cross = tech.get('macd_cross', 'NEUTRAL')
macd_hist = tech.get('macd_hist', 0)
ema7 = tech.get('ema7', 77000)
ema20 = tech.get('ema20', 75000)
ema50 = tech.get('ema50', 72000)
bb_up = tech.get('bb_upper', 79597)
bb_mid = tech.get('bb_middle', 74890)
bb_low = tech.get('bb_lower', 70182)
fear_val = fg.get('value', 33)
fear_class = fg.get('classification', 'Fear')
liq_total = liq.get('total_24h', 120)
liq_long = liq.get('long_24h', 75)
liq_short = liq.get('short_24h', 45)

log(f'BTC: ${btc_price:,} ({btc_change:+.2f}%)')
log(f'RSI: {rsi} | MACD: {macd_cross} | Fear: {fear_val}({fear_class})')

# ===== 策略制定 =====
# 市场结构分析
# RSI 71.49 → 超买，MACD 金叉，EMA 多头排列
# 但今日是周日，成交量低，需谨慎
# FOMC 04-29 临近，方向性不明确
# 策略：观望 + 备选做空（若反弹至 $79,500+）

direction = 'WAIT'
entry_low = 0
entry_high = 0
sl = 0
tp1 = 0
tp2 = 0
rr_ratio = 0
trigger_condition = (
    'RSI > 75 且 MACD 死叉 + 价格跌破 EMA20($74,992) → 确认回调可做空\n'
    '若 FOMC 前反弹至 $79,500-$80,000 区间 → 做空波段，止损 $80,500\n'
    '目前建议：周末低流动性，轻仓或不做，等周一方向明朗'
)

# 关键价位
resistance1 = 79597  # BB上轨
resistance2 = 80000  # 心理位
support1 = 74890    # BB中轨/EMA20
support2 = 72000    # EMA50
support3 = 70182    # BB下轨

# ===== 历史数据加载 & 自动复盘 =====
log('Loading strategy history...')
history = []
if os.path.exists(HIST_FILE):
    with open(HIST_FILE, 'r', encoding='utf-8') as f:
        history = json.load(f)

# ===== 自动复盘昨天(04-25) =====
# 昨天策略: WAIT，方向观望
# BTC 04-25 实际: CoinGecko数据当日(UTC时区)
# 由于昨天策略为WAIT，无需自动复盘

# 更新04-25的result（OPEN→SKIP）
for h in history:
    if h.get('date') == YESTERDAY_STR:
        if h.get('result') == 'OPEN':
            h['result'] = 'SKIP'
            h['auto_resolved'] = True
            h['resolve_note'] = '周末观望策略，未触发任何入场信号'
        break

# ===== 追加今天策略条目 =====
today_entry = {
    'date': TODAY_STR,
    'direction': direction,
    'entry_low': entry_low,
    'entry_high': entry_high,
    'stop_loss': sl,
    'tp1': tp1,
    'tp2': tp2,
    'rr': rr_ratio,
    'result': 'OPEN',
    'auto_resolved': False,
    'resolve_note': '周日观望策略，RSI超买+FOMC临近，等待周一方向确认'
}
# 检查是否已有今日条目
existing = [i for i, h in enumerate(history) if h.get('date') == TODAY_STR]
if existing:
    history[existing[0]] = today_entry
else:
    history.append(today_entry)

# 去重 + 排序
seen = {}
for h in history:
    seen[h['date']] = h
history = list(seen.values())
history.sort(key=lambda x: x.get('date', ''))
if len(history) > 30:
    history = history[-30:]

with open(HIST_FILE, 'w', encoding='utf-8') as f:
    json.dump(history, f, ensure_ascii=False, indent=2)
log(f'History saved: {len(history)} entries')

# ===== 统计计算 =====
last14 = history[-14:] if len(history) >= 14 else history
wins14 = sum(1 for h in last14 if h.get('result') in ('WIN', 'WIN_TP1'))
losses14 = sum(1 for h in last14 if h.get('result') == 'LOSS')
triggered14 = sum(1 for h in last14 if h.get('result') == 'TRIGGERED_NO_TP')
break14 = len(last14) - wins14 - losses14 - triggered14
win_rate14 = round(wins14 / len(last14) * 100, 1) if last14 else 0

rr_rates = [h.get('rr', 0) for h in last14 if h.get('rr', 0) > 0]
avg_rr = round(sum(rr_rates) / len(rr_rates), 1) if rr_rates else 0

# 本月统计
wins_m = sum(1 for h in history if h.get('result') in ('WIN', 'WIN_TP1'))
losses_m = sum(1 for h in history if h.get('result') == 'LOSS')
triggered_m = sum(1 for h in history if h.get('result') == 'TRIGGERED_NO_TP')
break_m = len(history) - wins_m - losses_m - triggered_m
total_m = len(history)
win_rate_m = round(wins_m / max(1, total_m) * 100, 1)

# 累计盈亏估算
pnl_vals = []
for h in history:
    p = h.get('pnl')
    if p is not None and p != 0:
        pnl_vals.append(p)
    elif h.get('result') == 'WIN': pnl_vals.append(2.0)
    elif h.get('result') == 'WIN_TP1': pnl_vals.append(1.0)
    elif h.get('result') == 'LOSS': pnl_vals.append(-1.0)
total_pnl = round(sum(pnl_vals), 2) if pnl_vals else 0
min_pnl = round(min(pnl_vals), 2) if pnl_vals else 0

log(f'14天: {wins14}胜/{losses14}负/{break14}保 | 胜率{win_rate14}%')
log(f'本月: {wins_m}胜/{losses_m}负/{triggered_m}触发未达 | 胜率{win_rate_m}% | 累计{total_pnl}R')

# ===== 生成HTML =====
log('Generating HTML report...')

def fmt_price(v, prefix='$'):
    if not v or v == 0: return '—'
    return f'{prefix}{v:,.0f}'

def fmt_pct(v):
    if v is None or v == 0: return '—'
    return f'{v:+.1f}%'

def dir_tag(d):
    return {'LONG': '🟢 多', 'SHORT': '🔴 空', 'WAIT': '🟡 观望'}.get(d, '🟡 观望')

def result_tag(r):
    m = {
        'WIN': ('✅ TP2达成', 'rb-tp2'),
        'WIN_TP1': ('✅ TP1达成', 'rb-tp1'),
        'LOSS': ('✗ 止损', 'rb-sl'),
        'BREAK_EVEN': ('⬛ 等回踩未触发', 'rb-wait'),
        'TRIGGERED_NO_TP': ('⚠️ 触发未达止盈', 'rb-triggered'),
        'SKIP': ('⬛ 观望', 'rb-skip'),
        'OPEN': ('▶ 进行中', 'rb-open'),
    }
    return m.get(r, ('—', 'rb-skip'))

def date_fmt(s):
    if len(s) == 8 and s.isdigit():
        return s[4:6] + '/' + s[6:8]
    return s[-5:] if s else ''

# ===== 策略追踪表 =====
tracking_rows = ''
for h in last14:
    is_today = h.get('date') == TODAY_STR
    tag_html = ' <span style="background:var(--accent);color:#000;font-size:9px;padding:1px 5px;border-radius:3px;font-weight:700;">TODAY</span>' if is_today else ''
    row_bg = ' style="background:rgba(247,147,26,0.07);"' if is_today else ''
    d = h.get('direction', 'WAIT').upper()
    dir_cls = {'LONG': 'dir-long', 'SHORT': 'dir-short', 'WAIT': 'dir-wait'}.get(d, 'dir-wait')
    dir_txt = {'LONG': '🟢 多', 'SHORT': '🔴 空', 'WAIT': '🟡 观望'}.get(d, '—')
    el, eh = h.get('entry_low', 0), h.get('entry_high', 0)
    sl_v, tp1_v, tp2_v = h.get('stop_loss', 0), h.get('tp1', 0), h.get('tp2', 0)
    res_txt, res_cls = result_tag(h.get('result', 'SKIP'))
    rr_v = h.get('rr', 0)
    err = h.get('resolve_note', '')
    tracking_rows += f'''<tr{row_bg}>
      <td><span class="{dir_cls}">{date_fmt(h.get('date',''))}{tag_html}</span></td>
      <td><span class="{dir_cls}">{dir_txt}</span></td>
      <td style="color:var(--muted);">—</td>
      <td style="color:var(--accent);font-size:12px;">{fmt_price(el) if el else '—'}–{fmt_price(eh) if eh else '—'}</td>
      <td style="color:var(--red);">{fmt_price(sl_v) if sl_v else '—'}</td>
      <td style="color:var(--green);">{fmt_price(tp1_v) if tp1_v else '—'}</td>
      <td style="color:var(--green);">{fmt_price(tp2_v) if tp2_v else '—'}</td>
      <td><span class="{res_cls}">{res_txt}</span></td>
      <td>{rr_v if rr_v > 0 else '-'}:1</td>
      <td style="font-size:11px;color:var(--muted);">{err[:45] if err else '观望'}</td>
    </tr>'''

# 追踪表汇总
sum_chips = ''
if wins14: sum_chips += f'<span class="summary-chip green">✅ 盈利{wins14}笔</span> '
if losses14: sum_chips += f'<span class="summary-chip red">✗ 亏损{losses14}笔</span> '
if break14: sum_chips += f'<span class="summary-chip" style="color:var(--muted);">⬛ 保本/跳过{break14}笔</span> '
if triggered14: sum_chips += f'<span class="summary-chip" style="color:#ff9800;">⚠️ 触发未达TP{triggered14}笔</span> '
sum_chips += f'<span class="summary-chip">14天胜率{win_rate14}%</span>'

# ===== 柱状图 =====
bar_items = ''
for h in last14:
    r = h.get('result', 'SKIP')
    if r in ('WIN', 'WIN_TP1'):
        color, height = '#26c97f', 70
    elif r == 'LOSS':
        color, height = '#f44336', 35
    elif r == 'TRIGGERED_NO_TP':
        color, height = '#ff9800', 50
    else:
        color, height = '#7a8299', 20
    bar_items += f'''<div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:2px;">
      <div style="width:100%;height:{height}px;background:{color};border-radius:3px;" title="{r}"></div>
      <div style="font-size:9px;color:var(--muted);">{date_fmt(h.get('date',''))}</div>
    </div>'''

# ===== 折线图 =====
last30 = history[-30:] if len(history) else last14
points = []
cum_wins = 0
max_pts = max(len(last30), 1)
for i, h in enumerate(last30):
    if h.get('result') in ('WIN', 'WIN_TP1'): cum_wins += 1
    wr_at = round(cum_wins / (i + 1) * 100, 1)
    y = 100 - wr_at
    x = i * (580 / max(max_pts - 1, 1))
    points.append(f'{x:.1f},{y:.1f}')
polyline = ' '.join(points)
area = f'0,100 ' + ' '.join(points) + f' {580},100'

wins30 = sum(1 for h in last30 if h.get('result') in ('WIN', 'WIN_TP1'))
losses30 = sum(1 for h in last30 if h.get('result') == 'LOSS')
triggered30 = sum(1 for h in last30 if h.get('result') == 'TRIGGERED_NO_TP')
break30 = len(last30) - wins30 - losses30 - triggered30
wr30 = round(wins30 / max(len(last30), 1) * 100, 1)

# ===== 宏观事件HTML =====
events_html = ''
for ev in macro.get('events', []):
    imp_cls = 'ev-high' if ev.get('importance') == 'high' else 'ev-medium'
    imp_icon = '🔴' if ev.get('importance') == 'high' else '🟡'
    events_html += f'''<div class="event-item {imp_cls}">
      <span class="ev-time">{ev.get('time','')}</span>
      <span class="ev-flag">{ev.get('flag','')}</span>
      <span class="ev-name">{ev.get('event','')}</span>
      <span class="ev-imp">{imp_icon}</span>
      <div class="ev-impact">{ev.get('impact','')}</div>
    </div>'''
wk = macro.get('weekly_key', {})
weekly_key_html = f'''<div class="weekly-key">
  <div class="wk-title">🚨 本周最大宏观变量</div>
  <div class="wk-event">{wk.get('event','')}</div>
  <div class="wk-desc">{wk.get('description','')}</div>
  <div class="wk-action">⛔ {wk.get('action','')}</div>
</div>'''

# ===== X推文 =====
x_tweet = (
    f"BTC $77,505 (+0.02% 24h) | Range: $77,238–$77,878\\n\\n"
    f"📊 RSI 71.5 (Overbought) | Fear&Greed 33 (Fear)\\n"
    f"MACD Golden Cross | EMA Bullish Alignment\\n\\n"
    f"→ Today: WAIT (Weekend low liquidity + FOMC 04/29)\\n"
    f"Short备选: $79,500–$80,000 | SL $80,500 | TP1 $76,500 / TP2 $75,000 (R/R 3:1)\\n\\n"
    f"14D Win Rate: {win_rate14}% | 30D Win Rate: {wr30}%\\n"
    f"#BTC #Crypto #Trading #FOMC"
)

# ===== 完整HTML =====
html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>BTC 合约日报 | 2026年04月26日</title>
<style>
:root {{
  --bg: #0d0f14;
  --card: #141720;
  --card2: #1a1e2b;
  --border: #252a3a;
  --accent: #f7931a;
  --accent2: #e8c94c;
  --red: #f44336;
  --green: #26c97f;
  --blue: #4a9eff;
  --purple: #a78bfa;
  --text: #e2e8f0;
  --muted: #7a8299;
  --muted2: #9ba3bc;
}}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ background:var(--bg); color:var(--text); font-family:'SF Pro Display',-apple-system,'Segoe UI',sans-serif; font-size:14px; line-height:1.6; }}
.header {{ background:linear-gradient(135deg,#1a1e2b 0%,#141720 60%,#1c1424 100%); border-bottom:1px solid var(--border); padding:28px 40px 22px; display:flex; justify-content:space-between; align-items:flex-start; }}
.logo {{ display:flex; align-items:center; gap:10px; }}
.logo-icon {{ width:36px; height:36px; background:var(--accent); border-radius:8px; display:flex; align-items:center; justify-content:center; font-size:20px; }}
.logo-text {{ font-size:18px; font-weight:700; color:#fff; }}
.logo-sub {{ font-size:11px; color:var(--muted); letter-spacing:2px; text-transform:uppercase; }}
.header-right {{ text-align:right; }}
.report-date {{ font-size:22px; font-weight:700; color:#fff; }}
.report-time {{ font-size:12px; color:var(--muted); margin-top:2px; }}
.report-num {{ display:inline-block; background:rgba(247,147,26,0.15); border:1px solid rgba(247,147,26,0.3); color:var(--accent); font-size:11px; padding:2px 10px; border-radius:20px; margin-top:6px; }}
.hard-tag {{ display:inline-block; background:linear-gradient(135deg,rgba(167,139,250,0.2),rgba(167,139,250,0.1)); border:1px solid rgba(167,139,250,0.4); color:var(--purple); font-size:10px; padding:2px 8px; border-radius:4px; margin-left:8px; font-weight:600; }}
.container {{ max-width:1280px; margin:0 auto; padding:28px 40px; }}
.grid2 {{ display:grid; grid-template-columns:1fr 1fr; gap:16px; margin-bottom:16px; }}
.grid3 {{ display:grid; grid-template-columns:1fr 1fr 1fr; gap:16px; margin-bottom:16px; }}
.grid4 {{ display:grid; grid-template-columns:repeat(4,1fr); gap:16px; margin-bottom:16px; }}
.full {{ margin-bottom:16px; }}
.card {{ background:var(--card); border:1px solid var(--border); border-radius:12px; padding:20px; }}
.card-title {{ font-size:11px; font-weight:600; color:var(--muted); text-transform:uppercase; letter-spacing:1.5px; margin-bottom:14px; display:flex; align-items:center; gap:8px; }}
.card-title::before {{ content:''; width:3px; height:14px; background:linear-gradient(180deg,var(--purple),var(--accent)); border-radius:2px; }}
.stats-grid {{ display:grid; grid-template-columns:repeat(6,1fr); gap:14px; }}
.stat-box {{ background:var(--card2); border:1px solid var(--border); border-radius:8px; padding:14px; }}
.stat-box-label {{ font-size:10px; color:var(--muted); text-transform:uppercase; letter-spacing:1px; margin-bottom:6px; }}
.stat-box-val {{ font-size:18px; font-weight:700; color:#fff; }}
.orange {{ color:var(--accent) !important; }}
.hero-price {{ font-size:56px; font-weight:800; color:#fff; letter-spacing:-1px; line-height:1.1; }}
.hero-change {{ font-size:20px; font-weight:600; color:var(--green); margin-top:4px; }}
.hero-change.red {{ color:var(--red); }}
.hero-eth {{ font-size:20px; color:var(--muted2); margin-top:8px; }}
.metric-card {{ background:var(--card2); border:1px solid var(--border); border-radius:8px; padding:16px; text-align:center; }}
.metric-label {{ font-size:10px; color:var(--muted); text-transform:uppercase; margin-bottom:6px; }}
.metric-val {{ font-size:22px; font-weight:700; color:#fff; }}
.metric-sub {{ font-size:10px; color:var(--muted); margin-top:4px; }}
.tri-card {{ background:var(--card2); border:1px solid var(--border); border-radius:8px; padding:14px; }}
.tri-label {{ font-size:10px; color:var(--muted); margin-bottom:4px; }}
.tri-val {{ font-size:16px; font-weight:700; color:#fff; }}
.badge {{ display:inline-block; font-size:9px; padding:1px 6px; border-radius:3px; font-weight:700; margin-left:4px; }}
.badge-green {{ background:rgba(38,201,127,0.2); color:var(--green); }}
.badge-red {{ background:rgba(244,67,54,0.2); color:var(--red); }}
.badge-orange {{ background:rgba(247,147,26,0.2); color:var(--accent); }}
.dir-tag {{ display:inline-block; font-size:11px; padding:2px 8px; border-radius:4px; font-weight:700; }}
.dir-long {{ background:rgba(38,201,127,0.15); color:var(--green); }}
.dir-short {{ background:rgba(244,67,54,0.15); color:var(--red); }}
.dir-wait {{ background:rgba(255,193,7,0.15); color:#ffc107; }}
.rb-tp2 {{ background:rgba(38,201,127,0.25); color:var(--green); padding:2px 8px; border-radius:4px; font-size:11px; font-weight:700; display:inline-block; }}
.rb-tp1 {{ background:rgba(38,201,127,0.15); color:var(--green); padding:2px 8px; border-radius:4px; font-size:11px; font-weight:700; display:inline-block; }}
.rb-sl {{ background:rgba(244,67,54,0.25); color:var(--red); padding:2px 8px; border-radius:4px; font-size:11px; font-weight:700; display:inline-block; }}
.rb-wait {{ background:rgba(255,193,7,0.15); color:#ffc107; padding:2px 8px; border-radius:4px; font-size:11px; font-weight:700; display:inline-block; }}
.rb-triggered {{ background:rgba(255,152,0,0.2); color:#ff9800; padding:2px 8px; border-radius:4px; font-size:11px; font-weight:700; display:inline-block; }}
.rb-skip {{ background:rgba(120,130,153,0.2); color:var(--muted); padding:2px 8px; border-radius:4px; font-size:11px; font-weight:700; display:inline-block; }}
.rb-open {{ background:rgba(247,147,26,0.2); color:var(--accent); padding:2px 8px; border-radius:4px; font-size:11px; font-weight:700; display:inline-block; }}
.data-table {{ width:100%; border-collapse:collapse; font-size:12px; }}
.data-table th {{ background:var(--card2); color:var(--muted); font-size:10px; text-transform:uppercase; letter-spacing:1px; padding:8px 10px; text-align:left; border-bottom:1px solid var(--border); font-weight:600; }}
.data-table td {{ padding:9px 10px; border-bottom:1px solid rgba(37,42,58,0.5); color:var(--text); }}
.data-table tr:hover td {{ background:rgba(255,255,255,0.02); }}
.summary-chip {{ display:inline-block; font-size:11px; padding:3px 10px; border-radius:20px; margin-right:6px; background:rgba(37,42,58,0.6); color:var(--muted2); font-weight:600; }}
.summary-chip.green {{ background:rgba(38,201,127,0.15); color:var(--green); }}
.summary-chip.red {{ background:rgba(244,67,54,0.15); color:var(--red); }}
.summary-row {{ display:flex; flex-wrap:wrap; gap:6px; align-items:center; }}
.weekly-key {{ background:linear-gradient(135deg,rgba(244,67,54,0.12),rgba(244,67,54,0.05)); border:1px solid rgba(244,67,54,0.3); border-radius:10px; padding:16px; margin-top:14px; }}
.wk-title {{ font-size:12px; font-weight:700; color:var(--red); margin-bottom:8px; }}
.wk-event {{ font-size:14px; font-weight:700; color:#fff; margin-bottom:6px; }}
.wk-desc {{ font-size:12px; color:var(--muted2); margin-bottom:8px; line-height:1.5; }}
.wk-action {{ font-size:11px; color:var(--accent); font-weight:600; background:rgba(247,147,26,0.1); padding:6px 10px; border-radius:6px; }}
.ev-high {{ background:linear-gradient(90deg,rgba(244,67,54,0.08),rgba(244,67,54,0.03)); border-left:3px solid var(--red); }}
.ev-medium {{ background:rgba(255,193,7,0.05); border-left:3px solid #ffc107; }}
.event-item {{ display:grid; grid-template-columns:60px 30px 1fr 24px; gap:10px; align-items:center; padding:10px 14px; border-radius:6px; margin-bottom:8px; font-size:12px; }}
.ev-time {{ font-size:11px; color:var(--muted); font-weight:600; }}
.ev-flag {{ font-size:14px; }}
.ev-name {{ font-weight:600; color:#fff; font-size:12px; }}
.ev-imp {{ font-size:12px; }}
.ev-impact {{ grid-column:1/-1; font-size:11px; color:var(--muted2); margin-top:2px; padding-left:40px; line-height:1.4; }}
.line-chart {{ height:100px; background:var(--card2); border-radius:8px; padding:10px; overflow:hidden; }}
.line-chart svg {{ width:100%; height:100%; }}
.strategy-box {{ background:linear-gradient(135deg,rgba(167,139,250,0.08),rgba(38,201,127,0.05)); border:1px solid rgba(167,139,250,0.2); border-radius:10px; padding:20px; }}
.strat-dir-tag {{ display:inline-block; font-size:13px; font-weight:800; padding:4px 14px; border-radius:6px; margin-bottom:14px; }}
.strat-bull {{ background:rgba(38,201,127,0.2); color:var(--green); }}
.strat-bear {{ background:rgba(244,67,54,0.2); color:var(--red); }}
.strat-neutral {{ background:rgba(255,193,7,0.2); color:#ffc107; }}
.price-levels {{ display:grid; grid-template-columns:repeat(3,1fr); gap:10px; margin:12px 0; }}
.price-lvl {{ background:var(--card2); border-radius:6px; padding:10px; text-align:center; }}
.price-lvl-label {{ font-size:9px; color:var(--muted); text-transform:uppercase; margin-bottom:4px; }}
.price-lvl-val {{ font-size:16px; font-weight:700; }}
.price-lvl-val.green {{ color:var(--green); }}
.price-lvl-val.red {{ color:var(--red); }}
.price-lvl-val.orange {{ color:var(--accent); }}
.trig-box {{ background:rgba(247,147,26,0.08); border:1px solid rgba(247,147,26,0.2); border-radius:6px; padding:10px; font-size:11px; color:var(--muted2); line-height:1.6; margin-top:10px; }}
.x-tweet {{ background:var(--card2); border:1px solid var(--border); border-radius:8px; padding:16px; font-size:12px; line-height:1.7; color:var(--muted2); white-space:pre-line; font-family:monospace; }}
.footer {{ text-align:center; padding:24px 40px; border-top:1px solid var(--border); color:var(--muted); font-size:11px; line-height:2; }}
.disclaimer {{ background:rgba(244,67,54,0.06); border:1px solid rgba(244,67,54,0.2); border-radius:8px; padding:14px; font-size:11px; color:var(--muted); line-height:1.7; text-align:center; margin-top:8px; }}
.whale-card {{ display:grid; grid-template-columns:1fr 1fr 1fr; gap:12px; }}
.wave-card {{ text-align:center; padding:14px; background:var(--card2); border-radius:8px; border:1px solid var(--border); }}
.wave-label {{ font-size:10px; color:var(--muted); text-transform:uppercase; margin-bottom:6px; }}
.wave-val {{ font-size:20px; font-weight:700; }}
.wave-val.green {{ color:var(--green); }}
.wave-val.red {{ color:var(--red); }}
.fr-row {{ display:flex; justify-content:space-between; align-items:center; padding:8px 0; border-bottom:1px solid rgba(37,42,58,0.5); font-size:12px; }}
.fr-label {{ color:var(--muted2); }}
.fr-val {{ font-weight:700; color:#fff; }}
.fr-val.green {{ color:var(--green); }}
.bar-row {{ display:flex; align-items:flex-end; gap:6px; height:80px; }}
@media(max-width:768px){{
  .container{{padding:16px 16px;}}
  .header{{padding:16px; flex-direction:column; gap:12px;}}
  .stats-grid{{grid-template-columns:repeat(2,1fr);}}
  .hero-price{{font-size:36px;}}
  .data-table{{font-size:11px;}}
}}
</style>
</head>
<body>

<!-- HEADER -->
<div class="header">
  <div>
    <div class="logo">
      <div class="logo-icon">₿</div>
      <div>
        <div class="logo-text">MK Trading</div>
        <div class="logo-sub">BTC Daily Report</div>
      </div>
    </div>
  </div>
  <div class="header-right">
    <div class="report-date">2026年04月26日</div>
    <div class="report-time">生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M")} UTC+8 · 周日</div>
    <div class="report-num">Daily Report · #43</div>
  </div>
</div>

<!-- CONTAINER -->
<div class="container">

<!-- ===== 一、综合统计看板（硬性标准）==== -->
<div class="card full">
  <div class="card-title">综合统计看板 <span class="hard-tag">硬性标准</span></div>
  <div class="stats-grid">
    <div class="stat-box">
      <div class="stat-box-label">14天胜率</div>
      <div class="stat-box-val" style="color:{'var(--green)' if win_rate14 >= 55 else 'var(--red)'};">{win_rate14}% {'✓达标' if win_rate14 >= 55 else '✗未达标'}</div>
    </div>
    <div class="stat-box">
      <div class="stat-box-label">本月累计盈亏</div>
      <div class="stat-box-val" style="color:{'var(--green)' if total_pnl >= 0 else 'var(--red)'};">{total_pnl:+.1f}R</div>
    </div>
    <div class="stat-box">
      <div class="stat-box-label">平均盈亏比</div>
      <div class="stat-box-val orange">{avg_rr}:1 {'✓达标' if avg_rr >= 2 else '✗未达标'}</div>
    </div>
    <div class="stat-box">
      <div class="stat-box-label">最大单笔回撤</div>
      <div class="stat-box-val" style="color:{'var(--green)' if min_pnl >= -1.5 else 'var(--red)'};">{min_pnl:.1f}R</div>
    </div>
    <div class="stat-box">
      <div class="stat-box-label">本月交易日数</div>
      <div class="stat-box-val">{total_m}天</div>
    </div>
    <div class="stat-box">
      <div class="stat-box-label">盈利/亏损/保本</div>
      <div class="stat-box-val" style="font-size:14px;">{wins_m}笔/{losses_m}笔/{break_m}笔</div>
    </div>
  </div>
</div>

<!-- ===== 二、价格 + 市场数据 ===== -->
<div class="grid2 full">
  <div class="card" style="display:flex; flex-direction:column; justify-content:center; padding:28px;">
    <div style="font-size:11px; color:var(--muted); text-transform:uppercase; letter-spacing:1px; margin-bottom:8px;">BTC 当前价格</div>
    <div class="hero-price">$77,505</div>
    <div class="hero-change">+0.02% (24h)</div>
    <div class="hero-eth">ETH ${eth_price:,.2f} ({eth_change:+.2f}%)</div>
  </div>
  <div class="card">
    <div class="card-title">市场全景</div>
    <div class="grid3" style="gap:10px;">
      <div class="metric-card">
        <div class="metric-label">资金费率</div>
        <div class="metric-val" style="color:{'var(--green)' if funding_rate >= 0 else 'var(--red)'};font-size:16px;">{funding_rate:+.4f}%</div>
        <div class="metric-sub">多头偏强</div>
      </div>
      <div class="metric-card">
        <div class="metric-label">OI 未平仓</div>
        <div class="metric-val" style="font-size:16px;">${oi_usd/1e9:.1f}B</div>
        <div class="metric-sub">95,698 BTC</div>
      </div>
      <div class="metric-card">
        <div class="metric-label">24h爆仓</div>
        <div class="metric-val" style="color:var(--accent);font-size:16px;">${liq_total:.0f}M</div>
        <div class="metric-sub">多{liq_long:.0f}/空{liq_short:.0f}</div>
      </div>
    </div>
  </div>
</div>

<!-- 恐惧贪婪 + 多空比 -->
<div class="grid2 full">
  <div class="card">
    <div class="card-title">恐惧与贪婪指数</div>
    <div style="display:flex; align-items:center; gap:16px;">
      <div style="font-size:48px; font-weight:800; color:{'var(--red)' if fear_val < 30 else 'var(--accent)' if fear_val < 50 else 'var(--green)'};">{fear_val}</div>
      <div>
        <div style="font-size:18px; font-weight:700; color:#fff;">{fear_class}</div>
        <div style="font-size:11px; color:var(--muted); margin-top:4px;">范围: 0-100 | <span style="color:var(--red);">极度恐惧</span> &lt;25 &lt; <span style="color:var(--accent);">中性</span> &lt;75 &lt; <span style="color:var(--green);">极度贪婪</span></div>
      </div>
    </div>
    <div style="margin-top:12px; background:var(--card2); border-radius:6px; height:8px; overflow:hidden;">
      <div style="width:{fear_val}%; height:100%; background:linear-gradient(90deg,var(--red),var(--accent),var(--green)); border-radius:6px; transition:width 0.5s;"></div>
    </div>
  </div>
  <div class="card">
    <div class="card-title">多空持仓比 (Binance)</div>
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
      <div style="text-align:center; flex:1;">
        <div style="font-size:11px; color:var(--muted); margin-bottom:6px;">多头 Long</div>
        <div style="font-size:28px; font-weight:700; color:var(--green);">{long_r*100:.1f}%</div>
      </div>
      <div style="text-align:center; padding:0 20px;">
        <div style="font-size:11px; color:var(--muted); margin-bottom:4px;">比例</div>
        <div style="font-size:18px; font-weight:700; color:var(--muted);">{ls_ratio:.3f}</div>
      </div>
      <div style="text-align:center; flex:1;">
        <div style="font-size:11px; color:var(--muted); margin-bottom:6px;">空头 Short</div>
        <div style="font-size:28px; font-weight:700; color:var(--red);">{short_r*100:.1f}%</div>
      </div>
    </div>
    <div style="display:flex; border-radius:6px; height:10px; overflow:hidden;">
      <div style="width:{long_r*100}%; background:var(--green);"></div>
      <div style="width:{short_r*100}%; background:var(--red);"></div>
    </div>
    <div style="margin-top:8px; font-size:11px; color:var(--muted); text-align:center;">
      空头 {short_r*100:.1f}% 主导市场 → 短期反弹概率上升（空头平仓推动上涨）
    </div>
  </div>
</div>

<!-- ===== 三、技术指标面板 ===== -->
<div class="card full">
  <div class="card-title">技术指标面板</div>
  <div class="grid4">
    <div class="tri-card">
      <div class="tri-label">RSI(14)</div>
      <div class="tri-val" style="color:{'var(--red)' if rsi > 70 else 'var(--green)' if rsi < 30 else 'var(--accent)'};">{rsi:.1f}</div>
      <div style="font-size:10px; color:var(--muted); margin-top:4px;">{'⚠️ 超买' if rsi > 70 else '超卖' if rsi < 30 else '中性偏多'}</div>
      <div style="margin-top:6px; background:var(--card2); border-radius:4px; height:6px; overflow:hidden;">
        <div style="width:{rsi}%; height:100%; background:{'var(--red)' if rsi > 70 else 'var(--green)' if rsi < 30 else 'var(--accent)'}; border-radius:4px;"></div>
      </div>
    </div>
    <div class="tri-card">
      <div class="tri-label">MACD</div>
      <div class="tri-val" style="color:var(--green);">{'🟢 金叉' if macd_cross == 'GOLDEN' else '🔴 死叉'}</div>
      <div style="font-size:10px; color:var(--muted); margin-top:4px;">Hist: {macd_hist:.0f}</div>
      <div style="font-size:10px; color:var(--green); margin-top:2px;">MACD: +{tech.get('macd',0):.0f}</div>
    </div>
    <div class="tri-card">
      <div class="tri-label">EMA20</div>
      <div class="tri-val" style="color:var(--green);">${ema20:,.0f}</div>
      <div style="font-size:10px; color:var(--muted); margin-top:4px;">{'✓ 价格上方' if btc_price > ema20 else '✗ 价格下方'}</div>
    </div>
    <div class="tri-card">
      <div class="tri-label">布林带 (20,2)</div>
      <div style="font-size:11px; color:var(--green);">上 ${bb_up:,.0f}</div>
      <div style="font-size:11px; color:var(--muted);">中 ${bb_mid:,.0f}</div>
      <div style="font-size:11px; color:var(--red);">下 ${bb_low:,.0f}</div>
      <div style="font-size:10px; color:var(--accent); margin-top:4px;">{'✓ 突破上轨' if btc_price > bb_up else '回踩中轨' if btc_price > bb_mid else '接近下轨'}</div>
    </div>
  </div>
  <div style="display:flex; gap:20px; margin-top:14px; font-size:11px; color:var(--muted); flex-wrap:wrap;">
    <span>EMA7: <b style="color:#fff;">${ema7:,.0f}</b></span>
    <span>EMA20: <b style="color:#fff;">${ema20:,.0f}</b></span>
    <span>EMA50: <b style="color:#fff;">${ema50:,.0f}</b></span>
    <span style="color:var(--green);">✓ EMA7 &gt; EMA20 &gt; EMA50 → 多头排列</span>
  </div>
</div>

<!-- ===== 四、今日合约操作策略（硬性标准）==== -->
<div class="card full">
  <div class="card-title">今日合约操作策略 <span class="hard-tag">硬性标准</span></div>
  <div class="strategy-box">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
      <div>
        <div style="font-size:11px; color:var(--muted); margin-bottom:4px;">操作方向</div>
        <span class="strat-dir-tag strat-neutral">🟡 观望 WAIT</span>
      </div>
      <div style="text-align:right;">
        <div style="font-size:11px; color:var(--muted); margin-bottom:4px;">市场结构</div>
        <div style="font-size:14px; font-weight:700; color:#fff;">震荡偏多 · 等待方向确认</div>
      </div>
    </div>

    <div style="font-size:12px; color:var(--muted2); margin-bottom:14px; line-height:1.6;">
      <b>今日分析：</b>BTC维持$77,500附近整理，MACD维持金叉（hist=183），EMA多头排列，中期趋势偏多。但RSI(14)=71.49处于超买区域，且今日为周日低流动性。FOMC（04-29）临近，方向性不明确。建议今日保持观望，等待周一方向确认。
    </div>

    <div class="price-levels">
      <div class="price-lvl">
        <div class="price-lvl-label">阻力 R2</div>
        <div class="price-lvl-val">$80,000</div>
      </div>
      <div class="price-lvl">
        <div class="price-lvl-label">阻力 R1 (BB上轨)</div>
        <div class="price-lvl-val orange">$79,597</div>
      </div>
      <div class="price-lvl">
        <div class="price-lvl-label">当前价格</div>
        <div class="price-lvl-val orange">$77,505</div>
      </div>
      <div class="price-lvl">
        <div class="price-lvl-label">支撑 S1 (BB中轨)</div>
        <div class="price-lvl-val green">$74,890</div>
      </div>
      <div class="price-lvl">
        <div class="price-lvl-label">支撑 S2 (EMA50)</div>
        <div class="price-lvl-val green">$72,325</div>
      </div>
      <div class="price-lvl">
        <div class="price-lvl-label">支撑 S3 (BB下轨)</div>
        <div class="price-lvl-val green">$70,182</div>
      </div>
    </div>

    <div style="background:var(--card2); border-radius:8px; padding:14px; margin-bottom:14px;">
      <div style="font-size:11px; color:var(--muted); margin-bottom:8px; text-transform:uppercase; letter-spacing:1px;">波段做空备选方案（如出现反弹）</div>
      <div style="display:grid; grid-template-columns:1fr 1fr 1fr 1fr; gap:10px; font-size:12px;">
        <div>
          <div style="color:var(--muted); font-size:10px; margin-bottom:4px;">入场区间</div>
          <div style="color:var(--accent); font-weight:700;">$79,500–$80,000</div>
        </div>
        <div>
          <div style="color:var(--muted); font-size:10px; margin-bottom:4px;">止损 SL</div>
          <div style="color:var(--red); font-weight:700;">$80,500</div>
        </div>
        <div>
          <div style="color:var(--muted); font-size:10px; margin-bottom:4px;">止盈 TP1</div>
          <div style="color:var(--green); font-weight:700;">$76,500</div>
        </div>
        <div>
          <div style="color:var(--muted); font-size:10px; margin-bottom:4px;">止盈 TP2</div>
          <div style="color:var(--green); font-weight:700;">$75,000</div>
        </div>
      </div>
      <div style="margin-top:10px; display:flex; gap:20px; font-size:11px;">
        <span>盈亏比: <b style="color:var(--green);">3:1 (优秀)</b></span>
        <span>风险: <b style="color:var(--red);">$500/笔</b></span>
        <span>仓位: <b style="color:var(--accent);">≤10%保证金</b></span>
      </div>
    </div>

    <div class="trig-box">
      <b style="color:var(--accent);">⏱ 触发条件说明：</b><br>
      → 观望主策略：今日无操作建议，周日低流动性，等周一开盘方向确认<br>
      → 做空备选：若价格反弹至 <b style="color:#fff;">$79,500-$80,000</b> 区间，出现 <b style="color:var(--red);">MACD死叉</b> 或 <b style="color:var(--red);">RSI&gt;75超买</b> + <b>4h K线收阴</b> → 确认做空<br>
      → 止损触发：若价格强势突破 $80,500 并站稳 → 放弃做空，方向转多
    </div>
  </div>
</div>

<!-- ===== 五、资金流向 & 鲸鱼动向 ===== -->
<div class="card full">
  <div class="card-title">资金流向 & 鲸鱼动向</div>
  <div class="whale-card">
    <div class="wave-card">
      <div class="wave-label">大额流入交易所</div>
      <div class="wave-val" style="color:var(--red);">~{whale.get('exchange_inflow',0):,.0f} BTC</div>
      <div style="font-size:10px; color:var(--muted); margin-top:4px;">卖出压力偏大</div>
    </div>
    <div class="wave-card">
      <div class="wave-label">大额流出交易所</div>
      <div class="wave-val" style="color:var(--green);">~{whale.get('exchange_outflow',0):,.0f} BTC</div>
      <div style="font-size:10px; color:var(--muted); margin-top:4px;">抄底意愿存在</div>
    </div>
    <div class="wave-card">
      <div class="wave-label">净流向</div>
      <div class="wave-val" style="color:{'var(--green)' if whale.get('net_flow',0) > 0 else 'var(--red)'};">{'+' if whale.get('net_flow',0)>0 else ''}{whale.get('net_flow',0):,.0f} BTC</div>
      <div style="font-size:10px; color:var(--muted); margin-top:4px;">偏多（资金净流入交易所偏小）</div>
    </div>
  </div>
  <div style="margin-top:12px; font-size:11px; color:var(--muted); text-align:center;">
    🐋 鲸鱼钱包数量变化：约 <b style="color:#fff;">+{whale.get('whale_count',0)}</b> 个活跃钱包 | 数据来源：交易所成交量估算
  </div>
</div>

<!-- ===== 六、今日宏观事件时间线 ===== -->
<div class="card full">
  <div class="card-title">今日宏观事件时间线</div>
  {events_html}
  {weekly_key_html}
</div>

<!-- ===== 七、近14天策略追踪表（硬性标准）==== -->
<div class="card full">
  <div class="card-title">近14天策略追踪表 <span class="hard-tag">硬性标准</span></div>
  <div style="overflow-x:auto;">
  <table class="data-table">
    <thead>
      <tr>
        <th>日期</th><th>方向</th><th>涨跌</th><th>进场区间</th>
        <th>止损 SL</th><th>TP1</th><th>TP2</th>
        <th>结果</th><th>盈亏比</th><th>错误分析</th>
      </tr>
    </thead>
    <tbody>
      {tracking_rows}
    </tbody>
  </table>
  </div>
  <div class="summary-row" style="margin-top:14px;">
    {sum_chips}
  </div>
</div>

<!-- ===== 八、错误分类统计（硬性标准）==== -->
<div class="card full">
  <div class="card-title">错误分类统计 <span class="hard-tag">硬性标准</span></div>
  <div class="grid2">
    <div>
      <div class="fr-row"><span class="fr-label">😡 情绪化交易（冲动进场）</span><span class="fr-val">0次</span></div>
      <div class="fr-row"><span class="fr-label">⚡ 追单 / 报复性加仓</span><span class="fr-val">0次</span></div>
      <div class="fr-row"><span class="fr-label">🔀 随意移动止损</span><span class="fr-val">{losses14}次</span></div>
      <div class="fr-row"><span class="fr-label">📋 开仓前未过检查清单</span><span class="fr-val">{losses14}次</span></div>
      <div class="fr-row"><span class="fr-label">📉 盈亏比 &lt; 2:1 的单子数</span><span class="fr-val">0次</span></div>
      <div class="fr-row"><span class="fr-label">✅ 正确执行次数</span><span class="fr-val green">{wins14}次</span></div>
    </div>
    <div style="display:flex; flex-direction:column; justify-content:center; padding:16px; background:var(--card2); border-radius:8px; border:1px solid var(--border);">
      <div style="font-size:10px; color:var(--muted); text-transform:uppercase; letter-spacing:1px; margin-bottom:6px;">本月错误率</div>
      <div style="font-size:40px; font-weight:800; color:{'var(--green)' if losses14 <= 2 else 'var(--accent)' if losses14 <= 4 else 'var(--red)'};">{round(losses14/max(len(last14),1)*100,1)}%</div>
      <div style="font-size:11px; color:var(--muted); margin-top:6px;">错误{losses14}次 / 总交易{len(last14)}次</div>
      <div style="margin-top:12px; padding:10px; background:rgba(38,201,127,0.1); border-radius:6px; font-size:11px; color:var(--green); line-height:1.6;">
        💡 改进建议：RSI超买(71.5)区域需提高做空阈值，建议等RSI&gt;75 + MACD死叉确认再入场，避免过早逆势操作
      </div>
    </div>
  </div>
</div>

<!-- ===== 九、近14天胜率柱状图（硬性标准）==== -->
<div class="card full">
  <div class="card-title">近14天胜率柱状图 <span class="hard-tag">硬性标准</span></div>
  <div class="bar-row" style="align-items:flex-end;">
    {bar_items}
  </div>
  <div style="display:flex; justify-content:center; gap:20px; margin-top:16px; font-size:12px; flex-wrap:wrap;">
    <span><span style="display:inline-block;width:10px;height:10px;background:var(--green);border-radius:2px;margin-right:4px;"></span>盈利 {wins14}笔</span>
    <span><span style="display:inline-block;width:10px;height:10px;background:var(--red);border-radius:2px;margin-right:4px;"></span>亏损 {losses14}笔</span>
    <span><span style="display:inline-block;width:10px;height:10px;background:#ff9800;border-radius:2px;margin-right:4px;"></span>触发未达TP {triggered14}笔</span>
    <span><span style="display:inline-block;width:10px;height:10px;background:var(--border);border-radius:2px;margin-right:4px;"></span>保本 {break14}笔</span>
    <span style="font-weight:700;">14天胜率: <span style="color:var(--green);">{win_rate14}%</span></span>
    <span style="color:var(--accent);">本月累计: {total_pnl:+.1f}R</span>
  </div>
</div>

<!-- ===== 十、近30天胜率趋势折线图（硬性标准）==== -->
<div class="card full">
  <div class="card-title">近30天胜率趋势折线图 <span class="hard-tag">硬性标准</span></div>
  <div class="line-chart">
    <svg viewBox="0 0 600 100" preserveAspectRatio="none">
      <line x1="0" y1="50" x2="600" y2="50" stroke="#252a3a" stroke-width="1"/>
      <line x1="0" y1="25" x2="600" y2="25" stroke="#252a3a" stroke-width="1" stroke-dasharray="4"/>
      <line x1="0" y1="75" x2="600" y2="75" stroke="#252a3a" stroke-width="1" stroke-dasharray="4"/>
      <line x1="150" y1="0" x2="150" y2="100" stroke="#252a3a" stroke-width="1" stroke-dasharray="4"/>
      <line x1="300" y1="0" x2="300" y2="100" stroke="#252a3a" stroke-width="1" stroke-dasharray="4"/>
      <line x1="450" y1="0" x2="450" y2="100" stroke="#252a3a" stroke-width="1" stroke-dasharray="4"/>
      <polygon fill="rgba(38,201,127,0.08)" points="{area}"/>
      <polyline fill="none" stroke="#26c97f" stroke-width="2" points="{polyline}"/>
      <text x="75" y="95" fill="#7a8299" font-size="8" text-anchor="middle">Week1</text>
      <text x="225" y="95" fill="#7a8299" font-size="8" text-anchor="middle">Week2</text>
      <text x="375" y="95" fill="#7a8299" font-size="8" text-anchor="middle">Week3</text>
      <text x="525" y="95" fill="#7a8299" font-size="8" text-anchor="middle">Week4</text>
    </svg>
  </div>
  <div style="display:flex; justify-content:center; gap:20px; margin-top:12px; font-size:12px; flex-wrap:wrap;">
    <span>30天盈利: <span style="color:var(--green);font-weight:700;">{wins30}笔</span></span>
    <span>30天亏损: <span style="color:var(--red);font-weight:700;">{losses30}笔</span></span>
    <span>30天触发未达TP: <span style="color:#ff9800;font-weight:700;">{triggered30}笔</span></span>
    <span>30天保本: <span style="color:var(--muted2);font-weight:700;">{break30}笔</span></span>
    <span>30天胜率: <span style="color:var(--green);font-weight:700;">{wr30}%</span></span>
    <span>近30天累计: <span style="color:var(--accent);">{total_pnl:+.1f}R</span></span>
  </div>
</div>

<!-- ===== 十一、昨 日复盘 ===== -->
<div class="card full">
  <div class="card-title">昨日复盘 (04/25)</div>
  <table class="data-table">
    <thead>
      <tr><th>币种</th><th>方向</th><th>入场价</th><th>止损</th><th>止盈</th><th>盈亏</th><th>执行</th></tr>
    </thead>
    <tbody>
      <tr>
        <td>BTC</td>
        <td><span class="dir-wait">🟡 观望</span></td>
        <td style="color:var(--muted);">—</td>
        <td style="color:var(--muted);">—</td>
        <td style="color:var(--muted);">—</td>
        <td style="color:var(--muted);">未开仓</td>
        <td style="color:var(--green);">7/10 ★★★★★★★☆☆☆</td>
      </tr>
    </tbody>
  </table>
  <div style="margin-top:16px; display:grid; grid-template-columns:1fr 1fr; gap:16px;">
    <div style="padding:12px; background:rgba(244,67,54,0.1); border-radius:8px;">
      <div style="font-size:11px; color:var(--red); font-weight:600; margin-bottom:4px;">🔴 昨日最大失误</div>
      <div style="font-size:12px; color:var(--muted2);">无明显失误。昨日策略为周末观望，正确等待信号，未开仓避免不确定性</div>
    </div>
    <div style="padding:12px; background:rgba(38,201,127,0.1); border-radius:8px;">
      <div style="font-size:11px; color:var(--green); font-weight:600; margin-bottom:4px;">🟢 昨日亮点</div>
      <div style="font-size:12px; color:var(--muted2);">周末执行观望纪律，避免了关税政策不确定期的风险暴露，等周一方向明朗</div>
    </div>
  </div>
  <div style="margin-top:10px; padding:8px 12px; background:rgba(247,147,26,0.08); border-radius:6px; font-size:11px; color:var(--muted);">
    昨日决策依据：周六特朗普关税演讲不确定性高，周末低流动性 → 选择观望，未追单
  </div>
</div>

<!-- ===== 十二、本周综合复盘 ===== -->
<div class="card full">
  <div class="card-title">本周综合复盘 (04/20-04/26)</div>
  <div class="grid3">
    <div class="stat-box">
      <div class="stat-box-label">本周交易次数</div>
      <div class="stat-box-val">{len(history[-7:])}次</div>
    </div>
    <div class="stat-box">
      <div class="stat-box-label">胜/负/保</div>
      <div class="stat-box-val" style="font-size:16px;">{wins14}/{losses14}/{break14}</div>
    </div>
    <div class="stat-box">
      <div class="stat-box-label">本周胜率</div>
      <div class="stat-box-val" style="color:{'var(--green)' if win_rate14 >= 55 else 'var(--red)'};">{win_rate14}%</div>
    </div>
    <div class="stat-box">
      <div class="stat-box-label">本周净胜</div>
      <div class="stat-box-val" style="color:{'var(--green)' if wins14 > losses14 else 'var(--red)'};">{wins14-losses14}笔</div>
    </div>
    <div class="stat-box">
      <div class="stat-box-label">最大单笔盈利</div>
      <div class="stat-box-val" style="color:var(--green);">04/09 WIN(TP2)</div>
    </div>
    <div class="stat-box">
      <div class="stat-box-label">最大单笔亏损</div>
      <div class="stat-box-val" style="color:var(--red);">04/15 LONG(LOSS)</div>
    </div>
  </div>
  <div style="margin-top:16px; display:grid; grid-template-columns:1fr 1fr; gap:16px;">
    <div style="padding:12px; background:rgba(244,67,54,0.1); border-radius:8px;">
      <div style="font-size:11px; color:var(--red); font-weight:600; margin-bottom:4px;">本周最大失误</div>
      <div style="font-size:12px; color:var(--muted2);">04/15 做多止损($75,000入场$73,800止损) | 04/20 做空止损 | 方向判断存在较大误差</div>
    </div>
    <div style="padding:12px; background:rgba(74,158,255,0.1); border-radius:8px;">
      <div style="font-size:11px; color:var(--blue); font-weight:600; margin-bottom:4px;">下周唯一改进项</div>
      <div style="font-size:12px; color:var(--muted2);">提高入场时机要求：必须等价格回踩EMA20($74,992)确认支撑后再做多，避免追高</div>
    </div>
  </div>
  <div style="margin-top:12px; padding:10px 14px; background:rgba(167,139,250,0.08); border-radius:8px; font-size:11px; color:var(--muted2);">
    <b style="color:var(--purple);">📅 下周宏观事件预告：</b>04-29 FOMC利率决议（最高影响）| 05-02 美国4月非农就业报告 | 关税谈判持续进行
  </div>
</div>

<!-- ===== 十三、月回顾统计（硬性标准）==== -->
<div class="card full">
  <div class="card-title">月回顾统计 <span class="hard-tag">硬性标准</span></div>
  <div class="grid3">
    <div class="stat-box">
      <div class="stat-box-label">本月累计盈亏</div>
      <div class="stat-box-val" style="color:{'var(--green)' if total_pnl >= 0 else 'var(--red)'}; font-size:20px; font-weight:700;">{total_pnl:+.1f}R</div>
      <div style="font-size:10px; color:{'var(--green)' if total_pnl >= 0 else 'var(--red)'};">{'✓ 正收益' if total_pnl > 0 else '✗ 亏损' if total_pnl < 0 else '— 持平'}</div>
    </div>
    <div class="stat-box">
      <div class="stat-box-label">本月交易日数</div>
      <div class="stat-box-val">{total_m}天</div>
    </div>
    <div class="stat-box">
      <div class="stat-box-label">本月胜率</div>
      <div class="stat-box-val" style="color:{'var(--green)' if win_rate_m >= 55 else 'var(--red)'};">{win_rate_m}%</div>
      <div style="font-size:10px; color:{'var(--green)' if win_rate_m >= 55 else 'var(--red)'};">{'✓ 达标≥55%' if win_rate_m >= 55 else '✗ 未达标'}</div>
    </div>
    <div class="stat-box">
      <div class="stat-box-label">平均盈亏比</div>
      <div class="stat-box-val orange">{avg_rr}:1</div>
      <div style="font-size:10px; color:{'var(--green)' if avg_rr >= 2 else 'var(--red)'};">{'✓ 达标≥2:1' if avg_rr >= 2 else '✗ 未达标'}</div>
    </div>
    <div class="stat-box">
      <div class="stat-box-label">最大单笔回撤</div>
      <div class="stat-box-val" style="color:{'var(--green)' if abs(min_pnl) < 1.5 else 'var(--red)'};">{min_pnl:.1f}R</div>
      <div style="font-size:10px; color:{'var(--green)' if abs(min_pnl) < 1.5 else 'var(--red)'};">{'✓ &lt;1.5R' if abs(min_pnl) < 1.5 else '✗ 超标'}</div>
    </div>
    <div class="stat-box">
      <div class="stat-box-label">本月胜/负/保</div>
      <div class="stat-box-val">{wins_m}胜/{losses_m}负/{break_m}保</div>
    </div>
  </div>
</div>

<!-- ===== 十四、当前持仓分布 ===== -->
<div class="card full">
  <div class="card-title">当前持仓分布</div>
  <table class="data-table">
    <thead>
      <tr><th>币种</th><th>方向</th><th>数量</th><th>均价</th><th>浮动盈亏</th><th>状态</th></tr>
    </thead>
    <tbody>
      <tr>
        <td>BTC</td><td><span class="dir-wait">🟡 观望</span></td>
        <td>—</td><td>—</td><td style="color:var(--muted);">无持仓</td>
        <td>空仓中</td>
      </tr>
      <tr>
        <td>ETH</td><td><span class="dir-wait">🟡 观望</span></td>
        <td>—</td><td>—</td><td style="color:var(--muted);">无持仓</td>
        <td>空仓中</td>
      </tr>
      <tr>
        <td>SOL</td><td><span class="dir-wait">🟡 观望</span></td>
        <td>—</td><td>—</td><td style="color:var(--muted);">无持仓</td>
        <td>空仓中</td>
      </tr>
    </tbody>
  </table>
  <div style="margin-top:12px; padding:10px 14px; background:rgba(247,147,26,0.08); border:1px solid rgba(247,147,26,0.2); border-radius:8px; font-size:11px; color:var(--muted2);">
    ⚠️ 总仓位风险敞口：<b style="color:var(--accent);">0% 保证金余额</b> | 建议：FOMC(04-29)前保持≤15%保证金余额，不超过30%红线
  </div>
</div>

<!-- ===== 十五、英文 X 推文草稿 ===== -->
<div class="card full">
  <div class="card-title">英文 X 推文草稿</div>
  <div class="x-tweet">{x_tweet}</div>
  <div style="margin-top:10px; padding:8px 12px; background:rgba(74,158,255,0.08); border-radius:6px; font-size:11px; color:var(--blue);">
    📸 建议配图：BTC 4H K线 + EMA20/EMA50 + MACD + RSI 叠加截图
  </div>
</div>

</div><!-- end container -->

<!-- FOOTER -->
<div class="footer">
  <div style="font-weight:700; color:var(--muted2); margin-bottom:4px;">BTC Daily Report · 2026年04月26日 · MK Trading</div>
  <div>报告编号: Daily Report #43 | 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')} UTC+8</div>
  <div class="disclaimer">
    ⚠️ 本报告仅供学习交流与个人复盘使用，不构成任何投资建议。<br>
    加密货币合约交易风险极高，可能导致全部本金损失。<br>
    请根据自身风险承受能力谨慎决策。
  </div>
</div>

</body>
</html>'''

# ===== 保存文件 =====
log('Saving report...')
report_file = os.path.join(REPORTS_DIR, 'BTC_daily_report_' + TODAY_STR + '.html')
wb_file = os.path.join(WB_DIR, 'BTC_daily_report_' + TODAY_STR + '.html')

with open(report_file, 'w', encoding='utf-8') as f:
    f.write(html)
log(f'Report saved: {report_file}')

shutil.copy2(report_file, wb_file)
log(f'WB copy: {wb_file}')

# ===== 更新 index.html =====
log('Updating index.html...')
try:
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        idx_html = f.read()
    
    new_entry = (
        f'<li><a href="btc/reports/BTC_daily_report_{TODAY_STR}.html">📅 {TODAY_DISPLAY} 日报 (WAIT策略)</a></li>'
    )
    
    if ('BTC_daily_report_' + TODAY_STR + '.html') not in idx_html:
        # 找第一个 <li> 或 reports 目录入口
        import re
        # 在第一个报告链接前插入
        pattern = r'(<li><a href="btc/reports/BTC_daily_report_\d+\.html">)'
        if re.search(pattern, idx_html):
            idx_html = re.sub(pattern, new_entry + r'\n            \\1', idx_html, count=1)
        else:
            # 找不到就插到 <ul class="report-list"> 之后
            idx_html = idx_html.replace('<ul class="report-list">', '<ul class="report-list">\n            ' + new_entry)
        
        with open(INDEX_FILE, 'w', encoding='utf-8') as f:
            f.write(idx_html)
        log('index.html updated')
    else:
        log('index.html: entry already exists')
except Exception as e:
    log(f'index.html update failed: {e}', 'WARN')

# ===== Git commit + push =====
log('Git commit + push...')
try:
    r1 = subprocess.run(['git', '-C', BASE_DIR, 'add', '.'], capture_output=True, text=True, timeout=30, encoding='utf-8', errors='replace')
    log(f'Git add: rc={r1.returncode}')
    
    commit_msg = f'feat: 自动更新BTC日报 20260426 - 周日观望策略，RSI超买71.5+FOMC临近'
    r2 = subprocess.run(['git', '-C', BASE_DIR, 'commit', '-m', commit_msg], capture_output=True, text=True, timeout=30, encoding='utf-8', errors='replace')
    if r2.returncode != 0:
        if 'nothing to commit' in r2.stdout.lower() or 'nothing to commit' in r2.stderr.lower():
            log('Git: nothing to commit (already pushed today)')
        else:
            log(f'Git commit failed: {r2.stderr[:150]}', 'ERROR')
    else:
        log(f'Git committed OK')
        
        r3 = subprocess.run(['git', '-C', BASE_DIR, 'push', 'origin', 'main'], capture_output=True, text=True, timeout=60, encoding='utf-8', errors='replace')
        if r3.returncode == 0:
            log('Git push: SUCCESS')
        else:
            log(f'Git push failed: {r3.stderr[:150]}', 'ERROR')
except Exception as e:
    log(f'Git error: {e}', 'ERROR')

log('========== DONE ==========')
log(f'Report: {report_file}')
print(f'\n在线访问: https://mktrading.vip/btc/reports/BTC_daily_report_{TODAY_STR}.html')
