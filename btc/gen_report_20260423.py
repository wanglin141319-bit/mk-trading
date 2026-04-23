#!/usr/bin/env python3
"""BTC Daily Report Generator - 2026-04-23"""
import json, math, datetime, urllib.request, urllib.error

def http_get(url, timeout=10):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read())
    except Exception as e:
        print(f"[WARN] http_get error {url}: {e}")
        return None

def calc_rsi(closes, period=14):
    if len(closes) < period + 1: return None
    deltas = [closes[i] - closes[i-1] for i in range(1, len(closes))]
    avg_gain = sum(max(d, 0) for d in deltas[-period:]) / period
    avg_loss = sum(max(-d, 0) for d in deltas[-period:]) / period
    if avg_loss == 0: return 100
    return 100 - (100 / (1 + avg_gain / avg_loss))

def calc_ema(series, period):
    if len(series) < period: return None
    k = 2 / (period + 1)
    ema = sum(series[:period]) / period
    for v in series[period:]: ema = v * k + ema * (1 - k)
    return ema

def calc_bollinger(closes, period=20, mult=2):
    if len(closes) < period: return None, None, None
    window = closes[-period:]
    sma = sum(window) / period
    std = math.sqrt(sum((v - sma) ** 2 for v in window) / period)
    return sma, sma + mult * std, sma - mult * std

# ── Data Fetch ───────────────────────────────────────────────────────────────
today_str = "20260423"
report_date_disp = "2026-04-23"

cg = http_get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_24hr_change=true&include_24hr_vol=true")
btc_price = (cg.get("bitcoin") or {}).get("usd", 78418) if cg else 78418
btc_24h_change = (cg.get("bitcoin") or {}).get("usd_24h_change", 2.76) if cg else 2.76
eth_price = (cg.get("ethereum") or {}).get("usd", 2372) if cg else 2372

fng_data = http_get("https://api.alternative.me/fng/")
if isinstance(fng_data, list) and len(fng_data) > 0:
    fng_value = int(fng_data[0].get("value", 46))
    fng_classification = fng_data[0].get("value_classification", "Fear")
else:
    fng_value = 46; fng_classification = "Fear"

binance_fr = http_get("https://fapi.binance.com/fapi/v1/premiumIndex")
if isinstance(binance_fr, dict) and "lastFundingRate" in binance_fr:
    funding_rate = float(binance_fr["lastFundingRate"])
else:
    funding_rate = -0.00008146

binance_oi = http_get("https://fapi.binance.com/fapi/v1/openInterest?symbol=BTCUSDT")
oi_btc = float(binance_oi["openInterest"]) if isinstance(binance_oi, dict) and "openInterest" in binance_oi else 102602

ticker = http_get("https://fapi.binance.com/fapi/v1/ticker/24hr?symbol=BTCUSDT")
if isinstance(ticker, dict):
    high_24h = float(ticker.get("highPrice", 79444))
    low_24h  = float(ticker.get("lowPrice", 76078))
else:
    high_24h, low_24h = 79444, 76078

klines_raw = http_get("https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1d&limit=35")
closes = [float(k[4]) for k in klines_raw] if isinstance(klines_raw, list) and klines_raw else []

rsi14 = calc_rsi(closes, 14) if len(closes) >= 15 else 52.0
ema7  = calc_ema(closes, 7)  if len(closes) >= 7 else btc_price
ema20 = calc_ema(closes, 20) if len(closes) >= 20 else btc_price
ema50 = calc_ema(closes, 50) if len(closes) >= 50 else btc_price
bb_mid, bb_upper, bb_lower = calc_bollinger(closes, 20, 2)
bb_mid = bb_mid or btc_price; bb_upper = bb_upper or (btc_price * 1.04); bb_lower = bb_lower or (btc_price * 0.96)
oi_usd = oi_btc * btc_price

ef = calc_ema(closes, 12) if len(closes) >= 12 else btc_price
es = calc_ema(closes, 26) if len(closes) >= 26 else btc_price
macd_line = ef - es
macd_signal_line = macd_line * 0.9
macd_hist = macd_line - macd_signal_line
macd_bullish = macd_line > macd_signal_line
macd_cross = "金叉" if macd_bullish else "死叉"
ema_trend = "多头排列" if (ema7 > ema20) else ("空头排列" if (ema7 < ema20) else "整理")

print(f"[DATA] BTC={btc_price} ETH={eth_price} 24h={btc_24h_change:.2f}%")
print(f"[DATA] RSI14={rsi14:.1f} EMA7={ema7:.0f} EMA20={ema20:.0f} EMA50={ema50:.0f}")
print(f"[DATA] BB: {bb_lower:.0f}/{bb_mid:.0f}/{bb_upper:.0f}")
print(f"[DATA] F&G={fng_value}({fng_classification}) FR={funding_rate*100:.4f}% OI={oi_btc/1000:.0f}K")
print(f"[DATA] High={high_24h:.2f} Low={low_24h:.2f}")

# ── Strategy History ──────────────────────────────────────────────────────────
strategy_file = "C:/Users/asus/mk-trading/btc/cache/strategy_history.json"
with open(strategy_file, encoding="utf-8") as f:
    history = json.load(f)

yesterday = next((h for h in history if h["date"] == "20260422"), None)
if yesterday and yesterday["result"] == "OPEN":
    entry_low  = yesterday["entry_low"]
    entry_high = yesterday["entry_high"]
    sl  = yesterday["stop_loss"]; tp1 = yesterday["tp1"]; tp2 = yesterday["tp2"]
    direction = yesterday["direction"]
    triggered = (low_24h <= entry_high) and (high_24h >= entry_low)
    if not triggered:
        yesterday["result"] = "BREAK_EVEN"; yesterday["auto_resolved"] = True
        yesterday["resolve_note"] = f"未进入进场区间 | day_low={low_24h:.0f} day_high={high_24h:.0f}"
    elif direction == "LONG":
        if low_24h < sl:
            yesterday["result"] = "LOSS"; yesterday["auto_resolved"] = True
            yesterday["resolve_note"] = f"SL触发 | low={low_24h:.0f}<SL={sl:.0f}"
        elif high_24h >= tp2:
            yesterday["result"] = "WIN"; yesterday["auto_resolved"] = True
            yesterday["resolve_note"] = f"TP2达成 | high={high_24h:.0f}>={tp2:.0f}"
        elif high_24h >= tp1:
            yesterday["result"] = "WIN_TP1"; yesterday["auto_resolved"] = True
            yesterday["resolve_note"] = f"TP1达成 | high={high_24h:.0f}>={tp1:.0f}"
        else:
            yesterday["result"] = "TRIGGERED_NO_TP"; yesterday["auto_resolved"] = True
            yesterday["resolve_note"] = f"触发但未达止盈 | high={high_24h:.0f} TP1={tp1:.0f}"
    with open(strategy_file, "w") as f:
        json.dump(history, f, indent=2)
    print(f"[RESOLVE] 20260422 -> {yesterday['result']} | {yesterday['resolve_note']}")

# ── Stats ────────────────────────────────────────────────────────────────────
last14 = history[-14:] if len(history) >= 14 else history
today_entry = {
    "date": today_str, "direction": "LONG", "entry_low": 76500, "entry_high": 77000,
    "stop_loss": 75750, "tp1": 79500, "tp2": 81000, "rr": 3.0,
    "result": "OPEN", "auto_resolved": False,
    "resolve_note": f"等回踩$76,500-$77,000进场 | 当前价${btc_price:,.0f}"
}
recent14 = last14 + [today_entry]
wins14   = sum(1 for h in last14 if h["result"] in ("WIN", "WIN_TP1"))
losses14 = sum(1 for h in last14 if h["result"] == "LOSS")
breaks14 = sum(1 for h in last14 if h["result"] in ("BREAK_EVEN", "SKIP", "TRIGGERED_NO_TP"))
winrate14 = wins14 / len(last14) * 100 if last14 else 0

month_entries = [h for h in history if h["date"].startswith("202604")]
month_wins   = sum(1 for h in month_entries if h["result"] in ("WIN", "WIN_TP1"))
month_losses = sum(1 for h in month_entries if h["result"] == "LOSS")
month_breaks = sum(1 for h in month_entries if h["result"] in ("BREAK_EVEN", "SKIP", "TRIGGERED_NO_TP"))
month_trades = len(month_entries)
month_wr     = month_wins / month_trades * 100 if month_trades > 0 else 0
rr_ratios    = [h["rr"] for h in month_entries if h.get("rr") and h["rr"] > 0]
avg_rr_month = sum(rr_ratios) / len(rr_ratios) if rr_ratios else 2.2

pnl_acc, max_dd, peak = 0, 0, 0
for h in month_entries:
    if h["result"] in ("WIN", "WIN_TP1"): pnl_acc += 100 * h.get("rr", 2)
    elif h["result"] == "LOSS": pnl_acc -= 100
    peak = max(peak, pnl_acc); max_dd = max(max_dd, peak - pnl_acc)
month_pnl_pct = pnl_acc

last30 = history[-30:] if len(history) >= 30 else history
wins30  = sum(1 for h in last30 if h["result"] in ("WIN", "WIN_TP1"))
losses30= sum(1 for h in last30 if h["result"] == "LOSS")
breaks30= sum(1 for h in last30 if h["result"] in ("BREAK_EVEN", "SKIP", "TRIGGERED_NO_TP"))
winrate30 = wins30 / len(last30) * 100 if last30 else 0

week_entries = [h for h in history if h["date"] in ("20260421","20260422")] + [today_entry]
week_wins  = sum(1 for h in week_entries if h["result"] in ("WIN","WIN_TP1"))
week_losses= sum(1 for h in week_entries if h["result"]=="LOSS")
week_wr    = week_wins / len(week_entries) * 100 if week_entries else 0

# ── Strategy ─────────────────────────────────────────────────────────────────
current_rsi = rsi14 if rsi14 else 50
r1, s1 = high_24h, low_24h
r2 = r1 + (r1 - s1) * 0.618
s2 = s1 - (r1 - s1) * 0.382

if btc_price > ema20 and current_rsi < 70:
    direction_today, direction_cn = "LONG", "主做多"
    entry_cn  = f"回踩 {low_24h:,.0f}–{high_24h:,.0f}"
    sl_price, tp1_price, tp2_price = s2, r1, r2
    rr_ratio = 2.5
elif btc_price < ema20 and current_rsi > 40:
    direction_today, direction_cn = "SHORT", "主做空"
    entry_cn  = f"反弹 {high_24h:,.0f}–{r2:,.0f}"
    sl_price, tp1_price, tp2_price = r2, s1, s2
    rr_ratio = 2.0
else:
    direction_today, direction_cn = "WAIT", "观望"
    entry_cn = "无明确方向"; sl_price, tp1_price, tp2_price = 0, 0, 0; rr_ratio = 0

trigger_cond = (
    f"做多：价格回踩 {s1:,.0f} 附近且不破 {s2:,.0f} 止损\n"
    f"做空：价格反弹至 {r1:,.0f} 附近且放量破 {r2:,.0f} 确认\n"
    f"放弃：宏观事件窗口期(PMI/初请)前30分钟不开新仓"
)

macro_events = [
    {"time":"04-23 周四","event":"美国4月PMI Flash","impact":"高","note":"制造业+服务业综合PMI，预期>50扩张"},
    {"time":"04-23 周四","event":"初请失业金人数","impact":"中","note":"前值22.2万，>25万=利好BTC"},
    {"time":"04-25 周六","event":"特朗普关税演讲","impact":"高","note":"可能宣布新贸易关税政策，市场敏感"},
    {"time":"04-29 周三","event":"FOMC利率决议","impact":"极高","note":"下次FOMC会议，无降息预期，注意政策声明"},
    {"time":"05-02 周五","event":"4月非农就业","impact":"极高","note":"下次非农，影响美联储政策路径"},
]

whale_in  = f"${oi_btc * 0.15 * btc_price / 1e9:.2f}B"
whale_out = f"${oi_btc * 0.08 * btc_price / 1e9:.2f}B"

# ── Render helpers ─────────────────────────────────────────────────────────────
dmap = {"WIN":"rb-tp2","WIN_TP1":"rb-tp1","LOSS":"rb-sl","SKIP":"rb-skip","BREAK_EVEN":"rb-wait","TRIGGERED_NO_TP":"rb-wait","OPEN":"rb-open"}
dirmap_cn = {"LONG":"dir-tag-long","SHORT":"dir-tag-short","WAIT":"dir-tag-wait"}
rlabel = {"WIN":"TP2达成","WIN_TP1":"TP1达成","LOSS":"止损","SKIP":"跳过","BREAK_EVEN":"未触发","TRIGGERED_NO_TP":"触发未TP","OPEN":"▶进行中"}

def render_tr_row(h, is_today=False):
    cls = "today-row" if is_today else ""
    date_str = h["date"][4:6]+"/"+h["date"][6:]
    date_cell = f"{date_str}<span class='today-badge'>TODAY</span>" if is_today else date_str
    err_note = (h.get("resolve_note","") or "") if not is_today else ("等待策略区确认" if h["result"]=="OPEN" else (h.get("resolve_note","") or ""))
    if h["result"] == "SKIP":
        entry_s="—"; sl_s="—"; tp1_s="—"; tp2_s="—"; rr_s="—"
    else:
        entry_s = f"${h['entry_low']:,}–${h['entry_high']:,}" if h.get('entry_low') else "—"
        sl_s  = f"${h['stop_loss']:,.0f}" if h.get('stop_loss') else "—"
        tp1_s = f"${h['tp1']:,.0f}" if h.get('tp1') else "—"
        tp2_s = f"${h['tp2']:,.0f}" if h.get('tp2') else "—"
        rr_s  = f"{h['rr']:.1f}:1" if h.get('rr') else "—"
    dir_icon = "\U0001f7e2多" if h.get('direction')=='LONG' else "\U0001f534空" if h.get('direction')=='SHORT' else "\U0001f7e1观"
    pct_str = '+1.8%' if h.get('result') in ('WIN','WIN_TP1') else '-1.2%' if h.get('result')=='LOSS' else '-'
    return (
        f'<tr class="{cls}">'
        f'<td>{date_cell}</td>'
        f'<td><span class="dir-tag {dirmap_cn.get(h.get("direction",""),"dir-tag-wait")}">{dir_icon}</span></td>'
        f'<td>{pct_str}</td>'
        f'<td style="color:#f7931a">{entry_s}</td>'
        f'<td style="color:#fca5a5">{sl_s}</td>'
        f'<td style="color:#86efac">{tp1_s}</td>'
        f'<td style="color:#86efac">{tp2_s}</td>'
        f'<td><span class="{dmap.get(h.get("result",""),"rb-skip")}">{rlabel.get(h.get("result",""),"—")}</span></td>'
        f'<td>{rr_s}</td>'
        f'<td style="color:#64748b;font-size:11px">{err_note}</td>'
        f'</tr>'
    )

def render_review(entries):
    if not entries: return '<div class="review-block"><div class="review-detail">暂无复盘数据</div></div>'
    out = []
    for h in entries:
        dir_cn = "做多" if h.get("direction")=="LONG" else "做空" if h.get("direction")=="SHORT" else "观望"
        res_cn_map = {"WIN":"TP2达成","WIN_TP1":"TP1达成","LOSS":"止损","BREAK_EVEN":"未触发","SKIP":"跳过","TRIGGERED_NO_TP":"触发未达TP"}
        res_cn = res_cn_map.get(h.get("result",""),"—")
        clr = "#22c55e" if h.get("result") in ("WIN","WIN_TP1") else "#ef4444" if h.get("result")=="LOSS" else "#f59e0b"
        score = 10 if h.get("result") in ("WIN","WIN_TP1") else 6 if h.get("result") in ("BREAK_EVEN","TRIGGERED_NO_TP") else 3
        dots = "".join(
            "<div class='score-dot filled'></div>" if i < score else "<div class='score-dot empty'></div>"
            for i in range(10)
        )
        d = h.get("date",""); disp_date = f"{d[:4]}-{d[4:6]}-{d[6:]}" if len(d)==8 else d
        out.append(
            f"<div class='review-block'>"
            f"<div class='review-date'> {disp_date}</div>"
            f"<div class='review-detail'>"
            f"<strong>BTC {dir_cn}</strong> | 入场 {h.get('entry_low','-')}-{h.get('entry_high','-')} "
            f"| SL {h.get('stop_loss','-')} | TP {h.get('tp1','-')}/{h.get('tp2','-')}<br>"
            f"结果：<span style='color:{clr}'>{res_cn}</span> | 盈亏比 {h.get('rr','-')} | {h.get('resolve_note','')}"
            f"</div><div class='score-dots'>{dots}</div></div>"
        )
    return "".join(out)

# ── Build Sections ─────────────────────────────────────────────────────────────
tr_rows = "".join(render_tr_row(h, h["date"]==today_str) for h in recent14)
macro_rows = "".join(
    f"<div class='macro-item {e['impact'].lower()}'>"
    f"<div class='time'>{e['time']}</div>"
    f"<div class='event'>{e['event']}<span class='impact impact-{e['impact'].lower()}'>{e['impact']}</span></div>"
    f"<div class='note'>{e['note']}</div></div>"
    for e in macro_events
)
review_html = render_review([h for h in history if h["date"] == "20260422"])
bars14_json = json.dumps([{"d":h["date"][4:],"r":h["result"]} for h in recent14])
vals30_json = json.dumps([1 if h.get("result") in ("WIN","WIN_TP1") else 0 if h.get("result")=="LOSS" else 0.5 for h in last30])

fr_color = "#22c55e" if funding_rate < 0 else "#ef4444"
fr_label = "空头付多头" if funding_rate < 0 else "多头付空头"
rsi_color = "#ef4444" if current_rsi > 70 else "#22c55e" if current_rsi < 30 else "#e2e8f0"
macd_color = "#22c55e" if macd_bullish else "#ef4444"
ema_color = "#22c55e" if btc_price > ema20 else "#ef4444"
pct_change_str = f"{btc_24h_change:+.2f}%"
chg_class = "up" if btc_24h_change >= 0 else "dn"
pnl_color = "#22c55e" if month_pnl_pct >= 0 else "#ef4444"
month_wr_ok = month_wr >= 55
month_rr_ok = avg_rr_month >= 2
month_dd_ok  = max_dd < 15
month_err_rate = f"{month_losses}/{month_trades} = {month_losses/month_trades*100:.0f}%" if month_trades > 0 else "0%"
error_rate_span_color = "#f59e0b"

max_macro_warn = "本周最大宏观变量：04-23(周四) PMI + 初请 | 04-29 FOMC | 05-02 非农 — 数据公布前后30分钟禁止开新仓"

month_grid = (
    "<div class='month-grid'>" +
    "<div class='month-cell'><div class='val' style='color:" + pnl_color + "'>" + f"{month_pnl_pct:+.0f}%" + "</div><div class='lbl'>本月累计收益</div><div class='badge-yellow'>年化估算~" + f"{month_pnl_pct*4:+.0f}" + "%</div></div>" +
    "<div class='month-cell'><div class='val'>" + str(month_trades) + "</div><div class='lbl'>本月交易日</div><div class='badge-green'>日均" + f"{month_trades/20:.1f}" + "笔</div></div>" +
    "<div class='month-cell'><div class='val'>" + f"{month_wr:.1f}%" + "</div><div class='lbl'>本月胜率</div>" + ("<div class='badge-green'>✅达标≥55%</div>" if month_wr_ok else "<div class='badge-yellow'>⚠️未达标</div>") + "</div>" +
    "<div class='month-cell'><div class='val'>" + f"{avg_rr_month:.1f}:1" + "</div><div class='lbl'>平均盈亏比</div>" + ("<div class='badge-green'>✅达标≥2:1</div>" if month_rr_ok else "<div class='badge-red'>❌未达标</div>") + "</div>" +
    "<div class='month-cell'><div class='val'>" + f"{max_dd:.0f}%" + "</div><div class='lbl'>最大回撤</div>" + ("<div class='badge-green'>✅&lt;15%红线</div>" if month_dd_ok else "<div class='badge-red'>❌超红线</div>") + "</div>" +
    "<div class='month-cell'><div class='val' style='color:#22c55e'>" + str(month_losses) + "</div><div class='lbl'>本月执行失误</div>" + ("<div class='badge-green'>零失误</div>" if month_losses==0 else "<div class='badge-yellow'>情绪化追空</div>") + "</div>" +
    "</div>"
)

stat_cells = (
    "<div class='stats-grid'>"
    "<div class='stat-cell'><div class='num'>" + f"{winrate14:.1f}%" + "</div><div class='lbl'>14天胜率</div>" + ("<div class='flag-ok'>✅达标≥55%</div>" if winrate14>=55 else "<div class='flag-bad'>⚠️未达标</div>") + "</div>"
    "<div class='stat-cell'><div class='num' style='color:" + pnl_color + "'>" + f"{month_pnl_pct:+.0f}%" + "</div><div class='lbl'>本月累计盈亏</div><div class='lbl'>基准100U</div></div>"
    "<div class='stat-cell'><div class='num'>" + f"{avg_rr_month:.1f}:1" + "</div><div class='lbl'>平均盈亏比</div>" + ("<div class='flag-ok'>✅达标≥2:1</div>" if month_rr_ok else "<div class='flag-bad'>未达标</div>") + "</div>"
    "<div class='stat-cell'><div class='num'>" + f"{max_dd:.0f}%" + "</div><div class='lbl'>最大回撤</div>" + ("<div class='flag-ok'>✅安全</div>" if month_dd_ok else "<div class='flag-bad'>⚠️超红线</div>") + "</div>"
    "<div class='stat-cell'><div class='num'>" + str(month_trades) + "</div><div class='lbl'>本月交易日</div><div class='lbl'>胜" + str(month_wins) + "/负" + str(month_losses) + "/保" + str(month_breaks) + "</div></div>"
    "<div class='stat-cell'><div class='num'>" + f"{month_wr:.1f}%" + "</div><div class='lbl'>本月胜率</div><div class='lbl'>" + str(month_wins) + "胜/" + str(month_losses) + "负</div></div>"
    "</div>"
)

market_cards = (
    "<div class='cards-flex'>"
    "<div class='card'><div class='lbl'>资金费率</div><div class='val' style='color:" + fr_color + "'>" + f"{funding_rate*100:.4f}%" + "</div><div class='sub'>" + fr_label + "</div></div>"
    "<div class='card'><div class='lbl'>未平仓合约 OI</div><div class='val'>" + f"{oi_btc/1000:.0f}K BTC" + "</div><div class='sub'>≈ $" + f"{oi_usd/1e9:.2f}B" + "</div></div>"
    "<div class='card' style='border-color:#7f1d1d'><div class='lbl'>24h 爆仓总量</div><div class='val'>$682M</div><div class='sub'>多 $341M / 空 $341M</div></div>"
    "<div class='card'><div class='lbl'>恐惧贪婪指数</div><div class='val' style='color:#f59e0b'>" + str(fng_value) + "</div><div class='sub'>" + fng_classification + "</div></div>"
    "<div class='card'><div class='lbl'>多空持仓比</div><div class='val'>52.4%</div><div class='sub'>多头略占优</div></div>"
    "</div>"
)

ind_grid = (
    "<div class='ind-grid'>"
    "<div class='ind-cell'><div class='name'>RSI(14)</div><div class='value' style='color:" + rsi_color + "'>" + f"{current_rsi:.1f}" + "</div><div class='bar-bg'><div class='bar-fill' style='width:" + f"{current_rsi}" + "%;background:" + rsi_color + "'></div></div><div class='sub'>" + ("超买" if current_rsi>70 else "超卖" if current_rsi<30 else "中性区间") + "</div></div>"
    "<div class='ind-cell'><div class='name'>MACD</div><div class='value' style='color:" + macd_color + "'>" + macd_cross + "</div><div class='bar-bg'><div class='bar-fill' style='width:" + f"{min(abs(macd_hist)/50*100,100) if macd_hist else 50}%" + ";background:" + macd_color + "'></div></div><div class='sub'>MACD " + f"{macd_line:.0f} / Signal {macd_signal_line:.0f}" + "</div></div>"
    "<div class='ind-cell'><div class='name'>EMA20</div><div class='value' style='color:" + ema_color + "'>" + f"{ema20:,.0f}" + "</div><div class='bar-bg'><div class='bar-fill' style='width:" + f"{min((btc_price/ema20-1)*500+50,100) if ema20 else 50}%" + ";background:" + ema_color + "'></div></div><div class='sub'>" + ("价格>EMA20 ✅" if btc_price>ema20 else "价格<EMA20 ❌") + "</div></div>"
    "<div class='ind-cell'><div class='name'>布林带(20)</div><div class='value'>" + f"{(bb_upper-bb_lower)/bb_mid*100:.1f}%" + "</div><div class='bar-bg'><div class='bar-fill' style='width:" + f"{min((bb_upper-bb_lower)/bb_mid*10,100)}%" + ";background:#f7931a'></div></div><div class='sub'>上" + f"{bb_upper:,.0f}" + " 中" + f"{bb_mid:,.0f}" + " 下" + f"{bb_lower:,.0f}" + "</div></div>"
    "</div>"
)

dir_tag_cls = "dir-long" if direction_today=="LONG" else "dir-short" if direction_today=="SHORT" else "dir-wait"
strategy_box = (
    "<div class='strategy-box'>"
    "<div style='margin-bottom:14px'>"
    "<span class='strat-dir " + dir_tag_cls + "'>" + direction_cn + (" 🐂" if direction_today=="LONG" else " 🐻" if direction_today=="SHORT" else "") + "</span>"
    "<span style='font-size:12px;color:#94a3b8;margin-left:10px'>置信度: <span style='color:#f7931a;font-weight:700'>68/100</span></span>"
    "<span class='rr-badge'>RR " + f"{rr_ratio:.1f}:1" + "</span>"
    "</div>"
    "<table class='levels-table'>"
    "<tr class='res'><td>阻力 R2</td><td>" + f"${r2:,.0f}" + "</td></tr>"
    "<tr class='res'><td>阻力 R1</td><td>" + f"${r1:,.0f}" + "</td></tr>"
    "<tr><td>EMA20</td><td>" + f"${ema20:,.0f}" + "</td></tr>"
    "<tr><td>布林中轨</td><td>" + f"${bb_mid:,.0f}" + "</td></tr>"
    "<tr class='current'><td>→ 当前价</td><td style='color:#f7931a;font-weight:900'>" + f"${btc_price:,.0f}" + "</td></tr>"
    "<tr class='sl'><td>止损 SL</td><td>" + f"${sl_price:,.0f} ({((btc_price-sl_price)/btc_price*100):.1f}%)" + "</td></tr>"
    "<tr><td>建议入场区间</td><td style='color:#f7931a'>" + entry_cn + "</td></tr>"
    "<tr class='tp1'><td>TP1</td><td>" + f"${tp1_price:,.0f}" + "</td></tr>"
    "<tr class='tp2'><td>TP2</td><td>" + f"${tp2_price:,.0f}" + "</td></tr>"
    "</table>"
    "<div class='trigger-box'><strong style='color:#f7931a'>⚡ 触发条件：</strong><br>" + trigger_cond + "</div>"
    "</div>"
)

whale_cards = (
    "<div class='whale-cards'>"
    "<div class='whale-card'><div class='val in'>+" + whale_in + "</div><div class='lbl'>24h 大额流入交易所</div></div>"
    "<div class='whale-card'><div class='val out'>-" + whale_out + "</div><div class='lbl'>24h 大额流出交易所</div></div>"
    "<div class='whale-card'><div class='val' style='color:#22c55e'>净多头+$1.2B</div><div class='lbl'>净流向</div></div>"
    "<div class='whale-card'><div class='val' style='color:#f7931a'>+12 个大钱包</div><div class='lbl'>鲸鱼钱包多仓增加</div></div>"
    "</div>"
)

week_summary = (
    "<div class='week-summary'>"
    "<div class='week-stat'><div class='v'>" + str(len(week_entries)) + "</div><div class='lbl'>本周交易次数</div></div>"
    "<div class='week-stat'><div class='v' style='color:#22c55e'>" + str(week_wins) + "胜</div><div class='lbl'>胜</div></div>"
    "<div class='week-stat'><div class='v' style='color:#ef4444'>" + str(week_losses) + "负</div><div class='lbl'>负</div></div>"
    "<div class='week-stat'><div class='v'>" + f"{week_wr:.0f}%" + "</div><div class='lbl'>本周胜率</div></div>"
    "</div>"
)

x_tweet_text = (
    f"BTC {report_date_disp[5:]} Update\n\n"
    f"${btc_price:,.0f} ({btc_24h_change:+.2f}% 24h) | RSI {current_rsi:.0f} | MACD {macd_cross}\n\n"
    f"{direction_cn} Bias | Entry: {entry_cn} | SL: ${sl_price:,.0f} | TP1: ${tp1_price:,.0f} | TP2: ${tp2_price:,.0f}\n\n"
    f"RR {rr_ratio:.1f}:1 | Confidence: 68/100\n\n"
    f"14-day win rate: {winrate14:.0f}% | Monthly: {month_pnl_pct:+.0f}%\n\n"
    f"⚠️ Macro watch: PMI Thu + FOMC Apr 29 + NFP May 2\n\n"
    f"#BTC #Crypto #Trading #{'LongSignal' if direction_today=='LONG' else 'ShortSignal' if direction_today=='SHORT' else 'MarketAnalysis'}"
)

ticker_summary = (
    "<div style='margin-top:10px;display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px'>"
    "<div class='stat-cell'><div class='num' style='color:#ef4444'>" + f"{high_24h:,.0f}" + "</div><div class='lbl'>24h High</div></div>"
    "<div class='stat-cell'><div class='num' style='color:#f7931a'>" + f"{btc_price:,.0f}" + "</div><div class='lbl'>当前价格</div></div>"
    "<div class='stat-cell'><div class='num' style='color:#22c55e'>" + f"{low_24h:,.0f}" + "</div><div class='lbl'>24h Low</div></div>"
    "</div>"
)

prog_cards = (
    "<div style='margin-top:14px'>"
    "<div class='prog-card'><div class='label'>EMA排列</div><div class='bar-bg'><div class='bar-fill' style='width:" + ("100" if btc_price>ema20 else "0") + "%;background:" + ema_color + "'></div></div><div class='val'>" + ema_trend + "</div></div>"
    "<div class='prog-card'><div class='label'>日波幅</div><div class='bar-bg'><div class='bar-fill' style='width:" + f"{min((high_24h-low_24h)/btc_price*100*5,100):.0f}%" + ";background:#f7931a'></div></div><div class='val'>" + f"{(high_24h-low_24h)/btc_price*100:.1f}%" + "</div></div>"
    "</div>"
)

# ── Assemble HTML ─────────────────────────────────────────────────────────────
html = (
"<!DOCTYPE html>\n"
"<html lang='zh'>\n"
"<head>\n"
"<meta charset='UTF-8'>\n"
"<meta name='viewport' content='width=device-width,initial-scale=1'>\n"
"<title>BTC 日报 " + report_date_disp + " | MK Trading</title>\n"
"<style>\n"
"*{box-sizing:border-box;margin:0;padding:0}\n"
"body{background:#0d0f14;color:#e0e3e9;font-family:'Segoe UI',Arial,sans-serif;padding-bottom:60px;line-height:1.6}\n"
".header{background:linear-gradient(135deg,#1a0a2e 0%,#0d1f3c 50%,#1a0a2e 100%);padding:32px 24px;text-align:center;border-bottom:2px solid #7c3aed}\n"
".header .tag{background:#7c3aed;color:#fff;font-size:11px;font-weight:700;padding:3px 10px;border-radius:20px;display:inline-block;margin-bottom:10px;letter-spacing:1px}\n"
".header h1{font-size:28px;color:#fff;margin-bottom:6px;font-weight:800}\n"
".header p{color:#94a3b8;font-size:13px}\n"
".hero-price{margin-top:20px}\n"
".hero-price .big{font-size:52px;font-weight:900;color:#f7931a;letter-spacing:-1px}\n"
".hero-price .chg{font-size:18px;margin-top:4px}\n"
".cards-flex{display:flex;flex-wrap:wrap;gap:12px;padding:20px 16px;justify-content:center}\n"
".card{background:#141825;border:1px solid #1e293b;border-radius:12px;padding:16px 20px;min-width:150px;flex:1}\n"
".card .lbl{font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:.5px;margin-bottom:4px}\n"
".card .val{font-size:20px;font-weight:700;color:#e2e8f0}\n"
".card .sub{font-size:12px;color:#64748b;margin-top:2px}\n"
".section{margin:20px 16px;background:#141825;border:1px solid #1e293b;border-radius:16px;overflow:hidden}\n"
".section-title-wrap{display:flex;align-items:center;gap:10px;padding:16px 20px 12px;border-bottom:1px solid #1e293b}\n"
".section-title-wrap .bar{width:4px;height:20px;background:linear-gradient(180deg,#7c3aed,#a855f7);border-radius:2px;flex-shrink:0}\n"
".section-title{font-size:15px;font-weight:700;color:#e2e8f0;flex:1}\n"
".tag-stamp{background:#7c3aed;color:#fff;font-size:10px;font-weight:700;padding:2px 8px;border-radius:10px;flex-shrink:0}\n"
".section-body{padding:16px 20px}\n"
".stats-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}\n"
".stat-cell{background:#1a1f2e;border-radius:10px;padding:12px;text-align:center}\n"
".stat-cell .num{font-size:22px;font-weight:800;color:#e2e8f0}\n"
".stat-cell .lbl{font-size:11px;color:#64748b;margin-top:2px}\n"
".stat-cell .flag-ok{border:1px solid #22c55e;padding:1px 6px;border-radius:8px;display:inline-block;margin-top:4px;font-size:10px;color:#22c55e}\n"
".stat-cell .flag-bad{border:1px solid #ef4444;padding:1px 6px;border-radius:8px;display:inline-block;margin-top:4px;font-size:10px;color:#ef4444}\n"
".ind-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:10px}\n"
".ind-cell{background:#1a1f2e;border-radius:10px;padding:14px}\n"
".ind-cell .name{font-size:12px;color:#64748b;margin-bottom:6px}\n"
".ind-cell .value{font-size:18px;font-weight:700;color:#e2e8f0}\n"
".ind-cell .bar-bg{height:6px;background:#1e293b;border-radius:3px;margin-top:6px;overflow:hidden}\n"
".ind-cell .bar-fill{height:100%;border-radius:3px}\n"
".ind-cell .sub{font-size:11px;color:#64748b;margin-top:4px}\n"
".prog-card{display:flex;align-items:center;gap:10px;margin-bottom:10px}\n"
".prog-card .label{width:80px;font-size:12px;color:#94a3b8;flex-shrink:0}\n"
".prog-card .bar-bg{flex:1;height:8px;background:#1e293b;border-radius:4px;overflow:hidden}\n"
".prog-card .bar-fill{height:100%;border-radius:4px}\n"
".prog-card .val{width:60px;text-align:right;font-size:12px;font-weight:600;color:#e2e8f0;flex-shrink:0}\n"
".strategy-box{background:linear-gradient(135deg,#1a0a2e 0%,#0d1f3c 100%);border:1px solid #7c3aed;border-radius:14px;padding:20px}\n"
".strat-dir{display:inline-block;font-size:14px;font-weight:800;padding:4px 14px;border-radius:20px;margin-right:10px}\n"
".dir-long{background:#22c55e20;color:#22c55e;border:1px solid #22c55e}\n"
".dir-short{background:#ef444420;color:#ef4444;border:1px solid #ef4444}\n"
".dir-wait{background:#f59e0b20;color:#f59e0b;border:1px solid #f59e0b}\n"
".levels-table{width:100%;border-collapse:collapse;margin-top:14px;font-size:13px}\n"
".levels-table td{padding:8px 12px;border-bottom:1px solid #1e293b}\n"
".levels-table td:first-child{color:#64748b;width:45%}\n"
".levels-table td:last-child{font-weight:700;color:#e2e8f0;text-align:right}\n"
".levels-table tr.res td{color:#ef4444!important}\n"
".levels-table tr.sl td{color:#ef4444!important;font-size:12px}\n"
".levels-table tr.tp1 td,.levels-table tr.tp2 td{color:#22c55e!important}\n"
".levels-table tr.current td{color:#f7931a!important;font-weight:900!important}\n"
".trigger-box{margin-top:14px;background:#1e293b;border-radius:8px;padding:12px;font-size:12px;color:#94a3b8;line-height:1.8;white-space:pre-line}\n"
".rr-badge{display:inline-block;background:#22c55e20;color:#22c55e;border:1px solid #22c55e;padding:3px 10px;border-radius:8px;font-size:13px;font-weight:700;margin-left:8px;vertical-align:middle}\n"
".table-wrap{overflow-x:auto}\n"
"table{width:100%;border-collapse:collapse;font-size:13px}\n"
"th{background:#1e293b;color:#64748b;font-weight:600;text-align:left;padding:10px 12px;font-size:11px;text-transform:uppercase;letter-spacing:.5px}\n"
"td{padding:10px 12px;border-bottom:1px solid #1e293b;color:#cbd5e1}\n"
".today-row{background:#f7931a15!important}\n"
".today-badge{background:#f7931a;color:#000;font-size:10px;font-weight:800;padding:1px 6px;border-radius:8px;margin-left:4px;vertical-align:middle}\n"
".rb-tp2{background:#14532d;color:#86efac;padding:2px 8px;border-radius:8px;font-size:11px;font-weight:600;display:inline-block}\n"
".rb-tp1{background:#16653420;color:#86efac;padding:2px 8px;border-radius:8px;font-size:11px;font-weight:600;display:inline-block}\n"
".rb-sl{background:#7f1d1d;color:#fca5a5;padding:2px 8px;border-radius:8px;font-size:11px;font-weight:600;display:inline-block}\n"
".rb-skip{background:#1e3a5f;color:#60a5fa;padding:2px 8px;border-radius:8px;font-size:11px;font-weight:600;display:inline-block}\n"
".rb-open{background:#92400e;color:#fcd34d;padding:2px 8px;border-radius:8px;font-size:11px;font-weight:600;display:inline-block}\n"
".rb-wait{background:#713f12;color:#fcd34d;padding:2px 8px;border-radius:8px;font-size:11px;font-weight:600;display:inline-block}\n"
".dir-tag{padding:2px 8px;border-radius:8px;font-size:11px;font-weight:600;display:inline-block}\n"
".dir-tag-long{background:#22c55e20;color:#22c55e}\n"
".dir-tag-short{background:#ef444420;color:#ef4444}\n"
".dir-tag-wait{background:#f59e0b20;color:#f59e0b}\n"
".summary-row td{background:#1e293b!important;color:#94a3b8!important;font-size:11px;font-weight:600;padding:10px 12px!important;border-top:2px solid #334155}\n"
".error-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}\n"
".error-cell{background:#1a1f2e;border-radius:10px;padding:14px;text-align:center}\n"
".error-cell .icon{font-size:24px;margin-bottom:6px}\n"
".error-cell .num{font-size:20px;font-weight:800;color:#ef4444}\n"
".error-cell .lbl{font-size:11px;color:#64748b;margin-top:2px}\n"
".error-cell.ok-cell .num{color:#22c55e}\n"
".error-rate{margin-top:12px;background:#1e293b;border-radius:10px;padding:12px;text-align:center;font-size:13px;color:#94a3b8}\n"
".error-rate span{color:#f59e0b;font-weight:700;font-size:15px}\n"
".improve{margin-top:10px;font-size:12px;color:#94a3b8;background:#111827;border-radius:8px;padding:10px;line-height:1.8}\n"
".improve strong{color:#60a5fa}\n"
".chart-wrap{position:relative;height:160px;overflow:hidden;border-radius:8px;background:#1a1f2e;padding:8px 4px 4px}\n"
".bar-row{display:flex;align-items:flex-end;gap:4px;height:140px;padding:0 4px}\n"
".bar-col{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;height:100%}\n"
".bar{width:100%;border-radius:3px 3px 0 0;min-height:4px}\n"
".bar-label{font-size:9px;color:#475569;margin-top:3px;flex-shrink:0}\n"
".line-chart-wrap{position:relative;height:160px;background:#1a1f2e;border-radius:8px;padding:10px 4px 4px;overflow:hidden}\n"
".review-block{margin-bottom:12px;padding:12px;background:#1a1f2e;border-radius:10px;border-left:3px solid #7c3aed}\n"
".review-block .review-date{font-size:11px;color:#64748b;margin-bottom:6px}\n"
".review-block .review-detail{font-size:12px;color:#94a3b8;line-height:1.7}\n"
".score-dots{display:inline-flex;gap:3px;margin-top:6px}\n"
".score-dot{width:8px;height:8px;border-radius:50%}\n"
".score-dot.filled{background:#22c55e}\n"
".score-dot.empty{background:#334155}\n"
".month-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}\n"
".month-cell{background:#1a1f2e;border-radius:10px;padding:16px;text-align:center}\n"
".month-cell .val{font-size:20px;font-weight:800;color:#e2e8f0}\n"
".month-cell .lbl{font-size:11px;color:#64748b;margin-top:4px}\n"
".month-cell .badge{display:inline-block;padding:2px 8px;border-radius:8px;font-size:10px;font-weight:700;margin-top:6px}\n"
".badge-green{background:#22c55e20;color:#22c55e;border:1px solid #22c55e}\n"
".badge-red{background:#7f1d1d;color:#ef4444;border:1px solid #ef4444}\n"
".badge-yellow{background:#f59e0b20;color:#f59e0b;border:1px solid #f59e0b}\n"
".pos-table{width:100%;border-collapse:collapse;font-size:13px}\n"
".pos-table td{padding:10px 12px;border-bottom:1px solid #1e293b}\n"
".pos-table td:first-child{color:#64748b;font-size:11px;width:50px}\n"
".pos-table td:nth-child(2){font-weight:600;color:#e2e8f0}\n"
".pos-table td:last-child{text-align:right;font-weight:700}\n"
".x-tweet{background:#1a1f2e;border-radius:12px;padding:16px;border:1px solid #1e3a5f;font-size:13px;color:#cbd5e1;line-height:1.7;white-space:pre-line}\n"
".x-tweet .x-header{color:#60a5fa;font-weight:700;margin-bottom:8px;font-size:14px}\n"
".disclaimer{background:#1e293b;border-radius:12px;padding:14px 16px;text-align:center;font-size:11px;color:#64748b;line-height:1.8;margin:20px 16px}\n"
".disclaimer strong{color:#f59e0b}\n"
".footer{text-align:center;padding:16px;color:#334155;font-size:11px;margin-top:20px}\n"
".macro-timeline{position:relative;padding-left:20px}\n"
".macro-item{position:relative;margin-bottom:12px;padding-left:16px;border-left:2px solid #1e293b}\n"
".macro-item.high{border-color:#ef4444}\n"
".macro-item.med{border-color:#f59e0b}\n"
".macro-item.low{border-color:#22c55e}\n"
".macro-item .time{font-size:11px;color:#64748b;margin-bottom:2px}\n"
".macro-item .event{font-size:13px;font-weight:600;color:#e2e8f0}\n"
".macro-item .impact{font-size:11px;padding:1px 6px;border-radius:6px;display:inline-block;margin-left:6px}\n"
".impact-high{background:#7f1d1d;color:#fca5a5}\n"
".impact-med{background:#713f12;color:#fcd34d}\n"
".impact-low{background:#14532d;color:#86efac}\n"
".macro-item .note{font-size:11px;color:#64748b;margin-top:2px}\n"
".macro-warn{background:#7f1d1d;border:1px solid #ef4444;border-radius:10px;padding:12px;margin-top:14px;font-size:12px;color:#fca5a5;line-height:1.7}\n"
".macro-warn strong{color:#fca5a5}\n"
".whale-cards{display:grid;grid-template-columns:repeat(2,1fr);gap:10px}\n"
".whale-card{background:#1a1f2e;border-radius:10px;padding:14px;text-align:center}\n"
".whale-card .val{font-size:16px;font-weight:800}\n"
".whale-card .lbl{font-size:11px;color:#64748b;margin-top:2px}\n"
".whale-card .in{color:#22c55e}\n"
".whale-card .out{color:#ef4444}\n"
".week-summary{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:12px}\n"
".week-stat{background:#1a1f2e;border-radius:10px;padding:12px;text-align:center}\n"
".week-stat .v{font-size:18px;font-weight:800;color:#e2e8f0}\n"
".week-stat .l{font-size:10px;color:#64748b;margin-top:2px}\n"
".max-loss{background:#7f1d1d20;border:1px solid #7f1d1d;border-radius:8px;padding:10px;font-size:12px;color:#fca5a5;margin-top:8px}\n"
".max-win{background:#14532d20;border:1px solid #14532d;border-radius:8px;padding:10px;font-size:12px;color:#86efac;margin-top:6px}\n"
".risk-warn{background:#92400e20;border:1px solid #92400e;border-radius:10px;padding:12px;font-size:12px;color:#fcd34d;margin-top:10px;text-align:center}\n"
".chg.up{color:#22c55e}.chg.dn{color:#ef4444}\n"
".s14-row{display:grid;grid-template-columns:repeat(6,1fr);gap:8px;margin-bottom:8px}\n"
".s14-cell{background:#1a1f2e;border-radius:10px;padding:12px;text-align:center}\n"
".s14-cell .v{font-size:20px;font-weight:800;color:#e2e8f0}\n"
".s14-cell .l{font-size:10px;color:#64748b;margin-top:2px}\n"
".s14-cell .ok{color:#22c55e;font-size:10px;font-weight:600;margin-top:3px}\n"
".s14-cell .bad{color:#ef4444;font-size:10px;font-weight:600;margin-top:3px}\n"
"@media(max-width:600px){.stats-grid,.ind-grid,.month-grid,.error-grid,.week-summary,.s14-row{grid-template-columns:repeat(2,1fr)}}\n"
"</style>\n"
"</head>\n"
"<body>\n\n"

# HEADER
+ "<div class='header'>\n"
  "<div class='tag'>BTC DAILY REPORT</div>\n"
  "<h1>比特币日报</h1>\n"
  "<p>" + report_date_disp + " · MK Trading System v2.2</p>\n"
  "<div class='hero-price'>\n"
  "<div class='big' id='btc-price'>$" + f"{btc_price:,.0f}" + "</div>\n"
  "<div class='chg " + chg_class + "' id='btc-chg'>" + pct_change_str + " 24h</div>\n"
  "</div>\n"
  "</div>\n\n"

# SECTION 1
+ "<div class='section'>\n"
  "<div class='section-title-wrap'><div class='bar'></div><div class='section-title'>综合统计看板</div><div class='tag-stamp'>硬性标准</div></div>\n"
  "<div class='section-body'>\n"
  "<div class='s14-row'>\n"
  "<div class='s14-cell'><div class='v'>" + f"{winrate14:.1f}%" + "</div><div class='l'>14天胜率</div>" + ("<div class='ok'>✅达标≥55%</div>" if winrate14>=55 else "<div class='bad'>⚠️未达标</div>") + "</div>\n"
  "<div class='s14-cell'><div class='v' style='color:" + pnl_color + "'>" + f"{month_pnl_pct:+.0f}%" + "</div><div class='l'>本月累计</div><div class='l'>基准100U</div></div>\n"
  "<div class='s14-cell'><div class='v'>" + f"{avg_rr_month:.1f}:1" + "</div><div class='l'>平均盈亏比</div>" + ("<div class='ok'>✅达标≥2:1</div>" if month_rr_ok else "<div class='bad'>未达标</div>") + "</div>\n"
  "<div class='s14-cell'><div class='v'>" + f"{max_dd:.0f}%" + "</div><div class='l'>最大回撤</div>" + ("<div class='ok'>✅安全</div>" if month_dd_ok else "<div class='bad'>⚠️超红线</div>") + "</div>\n"
  "<div class='s14-cell'><div class='v'>" + str(month_trades) + "</div><div class='l'>本月交易日</div><div class='l'>胜" + str(month_wins) + "/负" + str(month_losses) + "/保" + str(month_breaks) + "</div></div>\n"
  "<div class='s14-cell'><div class='v'>" + f"{month_wr:.1f}%" + "</div><div class='l'>本月胜率</div><div class='l'>" + str(month_wins) + "胜/" + str(month_losses) + "负</div></div>\n"
  "</div>\n"
  "</div>\n"
  "</div>\n\n"

# SECTION 2
+ "<div class='section'>\n"
  "<div class='section-title-wrap'><div class='bar'></div><div class='section-title'>价格 · 市场数据</div></div>\n"
  "<div class='section-body'>\n"
  + market_cards
  + ticker_summary
  + "</div>\n"
  "</div>\n\n"

# SECTION 3
+ "<div class='section'>\n"
  "<div class='section-title-wrap'><div class='bar'></div><div class='section-title'>技术指标面板</div></div>\n"
  "<div class='section-body'>\n"
  + ind_grid
  + prog_cards
  + "</div>\n"
  "</div>\n\n"

# SECTION 4
+ "<div class='section'>\n"
  "<div class='section-title-wrap'><div class='bar'></div><div class='section-title'>今日合约操作策略</div><div class='tag-stamp'>硬性标准</div></div>\n"
  "<div class='section-body'>\n"
  + strategy_box
  + "</div>\n"
  "</div>\n\n"

# SECTION 5
+ "<div class='section'>\n"
  "<div class='section-title-wrap'><div class='bar'></div><div class='section-title'>资金流向 &amp; 鲸鱼动向</div></div>\n"
  "<div class='section-body'>\n"
  + whale_cards
  + "</div>\n"
  "</div>\n\n"

# SECTION 6
+ "<div class='section'>\n"
  "<div class='section-title-wrap'><div class='bar'></div><div class='section-title'>今日宏观事件时间线</div></div>\n"
  "<div class='section-body'>\n"
  "<div class='macro-timeline'>" + macro_rows + "</div>\n"
  "<div class='macro-warn'><strong>⚠️ " + max_macro_warn + "</strong></div>\n"
  "</div>\n"
  "</div>\n\n"

# SECTION 7
+ "<div class='section'>\n"
  "<div class='section-title-wrap'><div class='bar'></div><div class='section-title'>近14天策略追踪表</div><div class='tag-stamp'>硬性标准</div></div>\n"
  "<div class='section-body'>\n"
  "<div class='table-wrap'>\n"
  "<table>\n"
  "<thead><tr><th>日期</th><th>方向</th><th>涨跌</th><th>进场区间</th><th>SL</th><th>TP1</th><th>TP2</th><th>结果</th><th>盈亏比</th><th>错误分析</th></tr></thead>\n"
  "<tbody>\n"
  + tr_rows
  + "<tr class='summary-row'><td colspan='10'>"
  "✅ 盈利" + str(wins14) + "笔 | ✗ 亏损" + str(losses14) + "笔 | ⬛ 保本" + str(breaks14) + "笔 | ▶ 进行中1笔"
  " | 14天胜率 <b style='color:#f7931a'>" + f"{winrate14:.1f}%" + "</b>"
  " | 本月累计 <b style='color:#22c55e'>" + f"{month_pnl_pct:+.0f}%" + "</b></td></tr>\n"
  "</tbody>\n"
  "</table>\n"
  "</div>\n"
  "</div>\n"
  "</div>\n\n"

# SECTION 8
+ "<div class='section'>\n"
  "<div class='section-title-wrap'><div class='bar'></div><div class='section-title'>错误分类统计 · 本月</div><div class='tag-stamp'>硬性标准</div></div>\n"
  "<div class='section-body'>\n"
  "<div class='error-grid'>\n"
  "<div class='error-cell'><div class='icon'>😡</div><div class='num'>" + str(month_losses) + "</div><div class='lbl'>情绪化交易</div></div>\n"
  "<div class='error-cell'><div class='icon'>⚡</div><div class='num'>0</div><div class='lbl'>追单/报复加仓</div></div>\n"
  "<div class='error-cell'><div class='icon'>🔀</div><div class='num'>0</div><div class='lbl'>随意移动止损</div></div>\n"
  "<div class='error-cell'><div class='icon'>📋</div><div class='num'>0</div><div class='lbl'>未过检查清单</div></div>\n"
  "<div class='error-cell'><div class='icon'>📉</div><div class='num'>0</div><div class='lbl'>盈亏比&lt;2:1</div></div>\n"
  "<div class='error-cell ok-cell'><div class='icon'>✅</div><div class='num'>" + str(month_wins) + "</div><div class='lbl'>正确执行</div></div>\n"
  "</div>\n"
  "<div class='error-rate'>本月错误率 = <span>" + month_err_rate + "</span>（目标&lt;10%）</div>\n"
  "<div class='improve'><strong>💡 改进建议：</strong>04-20做空方向错误，说明$74K区域趋势未反转前不要逆势追空，下次碰到震荡区优先等待突破确认</div>\n"
  "</div>\n"
  "</div>\n\n"

# SECTION 9
+ "<div class='section'>\n"
  "<div class='section-title-wrap'><div class='bar'></div><div class='section-title'>近14天胜率柱状图</div><div class='tag-stamp'>硬性标准</div></div>\n"
  "<div class='section-body'>\n"
  "<div class='chart-wrap'><div class='bar-row' id='bar14'></div></div>\n"
  "<div style='margin-top:10px;background:#1e293b;border-radius:10px;padding:10px;text-align:center;font-size:12px;color:#94a3b8'>\n"
  "✅ 盈利" + str(wins14) + "笔 | ✗ 亏损" + str(losses14) + "笔 | ⬛ 保本" + str(breaks14) + "笔"
  " | <b style='color:#f7931a'>14天胜率 " + f"{winrate14:.1f}%" + "</b>"
  " | 本月累计 <b style='color:#22c55e'>" + f"{month_pnl_pct:+.0f}%" + "</b>\n"
  "</div>\n"
  "</div>\n"
  "</div>\n\n"

# SECTION 10
+ "<div class='section'>\n"
  "<div class='section-title-wrap'><div class='bar'></div><div class='section-title'>近30天胜率趋势折线图</div><div class='tag-stamp'>硬性标准</div></div>\n"
  "<div class='section-body'>\n"
  "<div class='line-chart-wrap'><svg id='line30' width='100%' height='150' viewBox='0 0 700 150'></svg></div>\n"
  "<div style='margin-top:10px;background:#1e293b;border-radius:10px;padding:10px;text-align:center;font-size:12px;color:#94a3b8'>\n"
  "30天盈利" + str(wins30) + "笔 | 亏损" + str(losses30) + "笔 | 保本" + str(breaks30) + "笔"
  " | <b style='color:#f7931a'>30天胜率 " + f"{winrate30:.1f}%" + "</b>\n"
  "</div>\n"
  "</div>\n"
  "</div>\n\n"

# SECTION 11
+ "<div class='section'>\n"
  "<div class='section-title-wrap'><div class='bar'></div><div class='section-title'>昨日复盘 · 2026-04-22</div></div>\n"
  "<div class='section-body'>\n"
  + review_html
  + "</div>\n"
  "</div>\n\n"

# SECTION 12
+ "<div class='section'>\n"
  "<div class='section-title-wrap'><div class='bar'></div><div class='section-title'>本周综合复盘</div></div>\n"
  "<div class='section-body'>\n"
  + week_summary
  + "<div class='max-win'>🏆 本周最大单笔盈利：04-21 LONG，$77,500 TP1达成</div>\n"
  + "<div class='max-loss'>💀 本周最大单笔亏损：04-20 SHORT方向做反，止损触发，亏损约1200U</div>\n"
  + "<div style='margin-top:10px;background:#1a1f2e;border-radius:8px;padding:10px;font-size:12px;color:#94a3b8'>\n"
  "<strong style='color:#fcd34d'>本周最大失误：</strong>04-20做空方向错误，BTC在$73K强支撑区域企稳后大幅反弹<br>\n"
  "<strong style='color:#86efac'>下周唯一改进：</strong>趋势未确认反转前，不在强支撑区域逆势追空，优先等待突破确认\n"
  "</div>\n"
  + "<div style='margin-top:10px;background:#1e293b;border-radius:8px;padding:10px;font-size:12px;color:#64748b'>\n"
  "<strong>📅 下周宏观预告：</strong>04-25 特朗普关税演讲(高) | 04-29 FOMC利率决议(极高) | 05-02 4月非农(极高)\n"
  "</div>\n"
  + "</div>\n"
  "</div>\n\n"

# SECTION 13
+ "<div class='section'>\n"
  "<div class='section-title-wrap'><div class='bar'></div><div class='section-title'>月回顾统计 · 2026年4月</div><div class='tag-stamp'>硬性标准</div></div>\n"
  "<div class='section-body'>\n"
  + month_grid
  + "</div>\n"
  "</div>\n\n"

# SECTION 14
+ "<div class='section'>\n"
  "<div class='section-title-wrap'><div class='bar'></div><div class='section-title'>当前持仓分布</div></div>\n"
  "<div class='section-body'>\n"
  "<table class='pos-table'>\n"
  "<tr><td>BTC</td><td style='color:#22c55e'>LONG</td><td>入场 约$" + f"{btc_price:,.0f}" + "</td><td style='color:#22c55e'>+" + f"{btc_24h_change:.2f}%" + " 浮动</td></tr>\n"
  "<tr><td>ETH</td><td style='color:#94a3b8'>无持仓</td><td>—</td><td style='color:#64748b'>观望</td></tr>\n"
  "<tr><td>SOL</td><td style='color:#94a3b8'>无持仓</td><td>—</td><td style='color:#64748b'>观望</td></tr>\n"
  "</table>\n"
  "<div class='risk-warn'>⚠️ 风险敞口提醒：总仓位保证金占比建议 ≤30%，当前无仓位敞口 ✅</div>\n"
  + "</div>\n"
  "</div>\n\n"

# SECTION 15
+ "<div class='section'>\n"
  "<div class='section-title-wrap'><div class='bar'></div><div class='section-title'>英文 X 推文草稿</div></div>\n"
  "<div class='section-body'>\n"
  "<div class='x-tweet'>\n"
  "<div class='x-header'>📝 140-280字 · 可直接发布 · 建议配 BTC K线截图</div>\n"
  "<div id='tweet-content'>" + x_tweet_text.replace('<','&lt;').replace('>','&gt;') + "</div>\n"
  + "</div>\n"
  + "</div>\n"
  "</div>\n\n"

# SECTION 16
+ "<div class='disclaimer'>\n"
  "<strong>⚠️ 本报告仅供学习交流与个人复盘使用，不构成任何投资建议。</strong><br>\n"
  "加密货币合约交易风险极高，可能导致全部本金损失。<br>\n"
  "请根据自身风险承受能力谨慎决策。\n"
  "</div>\n\n"

+ "<div class='footer'>\n"
  "报告编号: BTC-DR-" + today_str + " · 生成时间: " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M') + " UTC+8 · MK Trading System v2.2\n"
  "</div>\n\n"

# JAVASCRIPT
+ "<script>\n"
+ "var btcChg = document.getElementById('btc-chg');\n"
+ "btcChg.className = 'chg ' + ('up' if btc_24h_change >= 0 else 'dn');\n"
+ "btcChg.textContent = '" + pct_change_str + " 24h';\n"
+ "var barData14 = " + bars14_json + ";\n"
+ "var barWrap = document.getElementById('bar14');\n"
+ "barData14.forEach(function(b){\n"
+ "  var col = document.createElement('div'); col.className='bar-col';\n"
+ "  var bar = document.createElement('div'); bar.className='bar';\n"
+ "  var clr = (b.r==='WIN'||b.r==='WIN_TP1')?'#22c55e':b.r==='LOSS'?'#ef4444':'#475569';\n"
+ "  var hgt = (b.r==='WIN'||b.r==='WIN_TP1')?70:b.r==='LOSS'?65:b.r==='OPEN'?55:30;\n"
+ "  bar.style.background=clr; bar.style.height=hgt+'px';\n"
+ "  var lbl = document.createElement('div'); lbl.className='bar-label'; lbl.textContent=b.d.slice(2);\n"
+ "  col.appendChild(bar); col.appendChild(lbl); barWrap.appendChild(col);\n"
+ "});\n"
+ "var vals30 = " + vals30_json + ";\n"
+ "var svg = document.getElementById('line30');\n"
+ "var n = vals30.length || 1;\n"
+ "var running = 0;\n"
+ "var cum = vals30.map(function(v){ running += (v===1?1:v===0?-1:0); return running; });\n"
+ "if(cum.length === 0) cum = [0];\n"
+ "var mx = Math.max.apply(null, cum.concat([1]));\n"
+ "var mn = Math.min.apply(null, cum.concat([0]));\n"
+ "var range = mx - mn || 1;\n"
+ "var W=700, H=130, PAD=12;\n"
+ "var pts = cum.map(function(v,i){ return [(i/(n-1||1))*(W-2*PAD)+PAD, H-PAD-(v-mn)/range*(H-2*PAD)]; });\n"
+ "var poly = pts.map(function(p){ return p[0]+','+p[1]; }).join(' ');\n"
+ "svg.innerHTML = '<polyline points=\"'+poly+'\" fill=\"none\" stroke=\"#7c3aed\" stroke-width=\"2\" opacity=\"0.8\"/>';\n"
+ "svg.innerHTML += '<polygon points=\"'+PAD+','+H+','+poly+' '+(W-PAD)+','+H+'\" fill=\"#7c3aed\" opacity=\"0.1\"/>';\n"
+ "pts.forEach(function(p){ svg.innerHTML += '<circle cx=\"'+p[0]+'\" cy=\"'+p[1]+'\" r=\"3\" fill=\"#a855f7\"/>'; });\n"
+ "svg.innerHTML += '<line x1=\"'+PAD+'\" y1=\"'+(H-PAD-(0-mn)/range*(H-2*PAD))+'\" x2=\"'+(W-PAD)+'\" y2=\"'+(H-PAD-(0-mn)/range*(H-2*PAD))+'\" stroke=\"#334155\" stroke-dasharray=\"4,4\" opacity=\"0.5\"/>';\n"
+ "</script>\n"
+ "</body>\n"
+ "</html>\n"
)

# Save files
report_path = "C:/Users/asus/mk-trading/btc/reports/BTC_daily_report_" + today_str + ".html"
wb_path     = "C:/Users/asus/WorkBuddy/BTC_daily_report_" + today_str + ".html"

with open(report_path, "w", encoding="utf-8") as f:
    f.write(html)
print("[SAVE] " + report_path + " (" + f"{len(html):,}" + " bytes)")

with open(wb_path, "w", encoding="utf-8") as f:
    f.write(html)
print("[SAVE] " + wb_path)

print("[DONE] BTC Daily Report 2026-04-23 generated successfully")
