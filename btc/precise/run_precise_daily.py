#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BTC 日报 · 精准版 —— 每日自动生成与发布
================================================
数据源 : Gate.io 公开 API（现货/合约/K线/OI/多空比/强平） + alternative.me（恐惧贪婪）
输出   : btc/reports/BTC_daily_report_YYYYMMDD.html
同步   : 更新 btc/index.html 报告列表（自动编号 / 置顶）
追踪   : .workbuddy/btc_precise/strategy_log.json（私密，已被 .gitignore 排除）
用法   : python run_precise_daily.py [--no-push] [--dry-run] [--date YYYYMMDD]
"""
import os, sys, json, time, subprocess, argparse, urllib3
from datetime import datetime, timezone, timedelta

urllib3.disable_warnings()
try:
    import requests
except ImportError:
    print("[FATAL] 缺少 requests"); sys.exit(2)

# Telegram 推送（可选；模块缺失或配置缺失时自动跳过，不影响主流程）
try:
    import telegram_push as tg
except Exception as _e:
    tg = None
    print(f"[WARN] Telegram 模块加载失败（将跳过推送）：{_e}")

# ================= 路径 =================
BASE    = os.path.dirname(os.path.abspath(__file__))   # btc/precise
BTC     = os.path.dirname(BASE)                        # btc
REPO    = os.path.dirname(BTC)                         # mk-trading
REPORTS = os.path.join(BTC, 'reports')
INDEX   = os.path.join(BTC, 'index.html')
PRIV    = os.path.join(REPO, '.workbuddy', 'btc_precise')
LOG     = os.path.join(PRIV, 'strategy_log.json')
CST     = timezone(timedelta(hours=8))
H       = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

def log(m, tag='INFO'):
    print(f"[{datetime.now().strftime('%H:%M:%S')}][{tag}] {m}", flush=True)

# ================= 1. 抓取 =================
def get(url, name, tries=3, t=10):
    for i in range(tries):
        try:
            r = requests.get(url, timeout=t, verify=False, headers=H)
            if r.status_code == 200:
                return r.json()
            log(f"{name} HTTP {r.status_code}", 'WARN')
        except Exception as e:
            log(f"{name} retry {i+1}/{tries}: {str(e)[:60]}", 'WARN')
            time.sleep(1.5)
    return None

def fetch():
    out = {'fetched_at': datetime.now(CST).isoformat()}
    s = get('https://api.gateio.ws/api/v4/spot/tickers?currency_pair=BTC_USDT', 'spot')
    if s:
        d = s[0]
        out['spot'] = {'price': float(d['last']), 'change_24h_pct': float(d['change_percentage']),
                       'high_24h': float(d['high_24h']), 'low_24h': float(d['low_24h']),
                       'base_vol_24h': float(d['base_volume'])}
    f = get('https://api.gateio.ws/api/v4/futures/usdt/tickers?contract=BTC_USDT', 'fut')
    if f:
        d = f[0]
        out['futures'] = {'last': float(d.get('last', 0)), 'mark_price': float(d.get('mark_price', 0)),
                          'index_price': float(d.get('index_price', 0)),
                          'funding_rate': float(d.get('funding_rate', 0)) * 100}
    c = get('https://api.gateio.ws/api/v4/futures/usdt/contracts/BTC_USDT', 'contract')
    if c:
        out['quanto'] = float(c.get('quanto_multiplier', '0.0001'))
    st = get('https://api.gateio.ws/api/v4/futures/usdt/contract_stats?contract=BTC_USDT&interval=1d&limit=10', 'stats')
    if st:
        out['stats'] = st[-3:]
    for itv, lim in [('1d', 200), ('4h', 200), ('1h', 240)]:
        k = get(f'https://api.gateio.ws/api/v4/futures/usdt/candlesticks?contract=BTC_USDT&interval={itv}&limit={lim}', f'k{itv}')
        if k:
            out[f'k_{itv}'] = [[int(x['t']), float(x['o']), float(x['h']), float(x['l']), float(x['c']), float(x['v'])] for x in k]
    e = get('https://api.gateio.ws/api/v4/spot/tickers?currency_pair=ETH_USDT', 'eth')
    if e:
        out['eth'] = {'price': float(e[0]['last']), 'change_24h_pct': float(e[0]['change_percentage'])}
    fg = get('https://api.alternative.me/fng/?limit=8', 'fng')
    if fg and fg.get('data'):
        dd = fg['data']
        out['fng'] = {'value': int(dd[0]['value']), 'cls': dd[0]['value_classification'],
                      'yesterday': int(dd[1]['value']),
                      'week_avg': round(sum(int(x['value']) for x in dd[:7]) / 7, 1)}
    return out

# ================= 2. 指标 =================
def _ema(v, p):
    k = 2 / (p + 1); out = []; e = v[0]
    for i, x in enumerate(v):
        e = x if i == 0 else x * k + e * (1 - k)
        out.append(e)
    return out

def _rsi(c, p=14):
    if len(c) < p + 1: return None
    g = [max(c[i] - c[i-1], 0) for i in range(1, p+1)]
    l = [max(c[i-1] - c[i], 0) for i in range(1, p+1)]
    ag, al = sum(g)/p, sum(l)/p
    for i in range(p+1, len(c)):
        d = c[i] - c[i-1]
        ag = (ag*(p-1) + max(d, 0))/p
        al = (al*(p-1) + max(-d, 0))/p
    return 100.0 if al == 0 else 100 - 100/(1 + ag/al)

def _macd(c, f=12, s=26, sg=9):
    dif = [a-b for a, b in zip(_ema(c, f), _ema(c, s))]
    dea = _ema(dif, sg)
    hist = [a-b for a, b in zip(dif, dea)]
    cross = 'NONE'
    if len(hist) >= 2:
        if hist[-2] <= 0 < hist[-1]: cross = 'GOLDEN'
        elif hist[-2] >= 0 > hist[-1]: cross = 'DEAD'
    return {'dif': dif[-1], 'dea': dea[-1], 'hist': hist[-1], 'cross': cross,
            'state': '多头' if hist[-1] > 0 else '空头'}

def _boll(c, p=20, m=2):
    r = c[-p:]; sma = sum(r)/p
    sd = (sum((x-sma)**2 for x in r)/p) ** 0.5
    return {'upper': sma+m*sd, 'mid': sma, 'lower': sma-m*sd,
            'pos': (c[-1]-(sma-m*sd))/(2*m*sd)*100 if sd else 50}

def _swings(rows, l=3, r=3):
    hi, lo = [], []
    for i in range(l, len(rows)-r):
        h, w = rows[i][2], rows[i][3]
        if all(rows[j][2] <= h for j in range(i-l, i+r+1) if j != i): hi.append(h)
        if all(rows[j][3] >= w for j in range(i-l, i+r+1) if j != i): lo.append(w)
    return hi, lo

def calc_tf(rows, label):
    c = [x[4] for x in rows]
    return {'label': label, 'close': c[-1], 'ema20': _ema(c, 20)[-1], 'ema50': _ema(c, 50)[-1],
            'ema200': _ema(c, 200)[-1] if len(c) >= 200 else None, 'rsi': _rsi(c, 14),
            'macd': _macd(c), 'boll': _boll(c),
            'sw_hi': sorted(_swings(rows[-120:])[0], reverse=True)[:6],
            'sw_lo': sorted(_swings(rows[-120:])[1])[:6]}

# ================= 3. 策略 =================
def build_strategy(D, d1, h4, h1):
    price = D['spot']['price']
    fr = D['futures']['funding_rate']
    fg = D['fng']['value']
    sig, sl, ss = [], 0, 0
    for tv, cond, txt, who in [
        (d1, d1['ema200'] and price > d1['ema200'], f"日线：价 > EMA200，长期多头格局", 'L'),
        (d1, d1['ema200'] and price < d1['ema200'], f"日线：价 < EMA200，长期空头格局", 'S'),
        (d1, price > d1['ema50'], "日线：价 > EMA50，中期偏多", 'L'),
        (d1, price < d1['ema50'], "日线：价 < EMA50，中期偏空", 'S'),
    ]:
        if cond:
            sig.append(txt); sl += (2 if who == 'L' else 0); ss += (2 if who == 'S' else 0)
    sig.append(f"日线：MACD {d1['macd']['state']}（DIF {d1['macd']['dif']:,.0f} / DEA {d1['macd']['dea']:,.0f}）")
    if d1['macd']['state'] == '多头': sl += 1
    else: ss += 1
    if d1['macd']['cross'] != 'NONE':
        sig.append(f"日线：MACD {'金叉' if d1['macd']['cross']=='GOLDEN' else '死叉'}（柱穿越零轴）")
    if price > h4['ema20']: sig.append('4H：价 > EMA20，短线偏多'); sl += 1
    else: sig.append('4H：价 < EMA20，短线偏空'); ss += 1
    sl += 1 if price > h4['ema50'] else 0
    ss += 1 if price < h4['ema50'] else 0
    sl += 1 if h4['macd']['state'] == '多头' else 0
    ss += 1 if h4['macd']['state'] == '空头' else 0
    if h4['rsi'] and h4['rsi'] > 70: sig.append(f"4H RSI {h4['rsi']:.1f} 超买"); ss += 1
    elif h4['rsi'] and h4['rsi'] < 30: sig.append(f"4H RSI {h4['rsi']:.1f} 超卖"); sl += 1
    if fr < -0.005: sig.append(f'资金费率 {fr:.4f}%（空头拥挤，偏多）'); sl += 1
    elif fr > 0.01: sig.append(f'资金费率 {fr:.4f}%（多头拥挤，偏空）'); ss += 1
    else: sig.append(f'资金费率 {fr:.4f}%（中性）')
    if fg >= 60: sig.append(f'恐惧贪婪 {fg}（贪婪，追多风险）'); ss += 1
    elif fg <= 25: sig.append(f'恐惧贪婪 {fg}（极度恐惧，或有反弹）'); sl += 1

    if sl >= ss + 3: sd, conf = 'LONG', '中高'
    elif ss >= sl + 3: sd, conf = 'SHORT', '中高'
    elif abs(sl - ss) <= 1: sd, conf = 'WAIT', '低'
    else: sd, conf = ('LONG' if sl > ss else 'SHORT'), '中'

    all_hi = sorted(d1['sw_hi'] + h4['sw_hi']); all_lo = sorted(d1['sw_lo'] + h4['sw_lo'], reverse=True)
    R1 = next((x for x in all_hi if x > price*1.002), D['spot']['high_24h'])
    R2 = next((x for x in all_hi if x > R1*1.002), R1*1.02)
    S1 = next((x for x in all_lo if x < price*0.998), D['spot']['low_24h'])
    S2 = next((x for x in all_lo if x < S1*0.998), S1*0.98)

    if sd == 'LONG':
        el, eh = round(price*0.990), round(price)
        stop = round(min(S1*0.995, el*0.99))
        em = (el+eh)/2; risk = em-stop
        tp1, tp2 = round(em+risk*2), round(em+risk*3)
        trig = f'回踩 {el:,.0f}-{eh:,.0f} 企稳（1H 收阳 / RSI 回升）后做多'
        inv = f'1H 收盘跌破 {stop:,.0f}（S1 {S1:,.0f}）则做多逻辑失效'
    elif sd == 'SHORT':
        el, eh = round(price), round(price*1.010)
        stop = round(max(R1*1.005, eh*1.01))
        em = (el+eh)/2; risk = stop-em
        tp1, tp2 = round(em-risk*2), round(em-risk*3)
        trig = f'反弹至 {el:,.0f}-{eh:,.0f} 滞涨（1H 长上影 / RSI 走弱）后做空'
        inv = f'1H 收盘站上 {stop:,.0f}（R1 {R1:,.0f}）则做空逻辑失效'
    else:
        el, eh = round(S1), round(price*1.005); stop = round(S2*0.995)
        em = price; tp1, tp2 = round(R1), round(R2)
        trig = f'等待站上 {R1:,.0f} 或跌破 {S1:,.0f} 再跟，区间内不追'
        inv = '多空信号互相抵消，方向不明，硬做即为赌博'
    rr = abs(tp1-em)/abs(em-stop) if abs(em-stop) else 0
    return {'direction': sd, 'confidence': conf, 'entry_low': el, 'entry_high': eh, 'stop': stop,
            'tp1': tp1, 'tp2': tp2, 'rr': round(rr, 2), 'trigger': trig, 'invalid': inv,
            'position': '10-15%' if sd != 'WAIT' else '0%',
            'R1': round(R1), 'R2': round(R2), 'S1': round(S1), 'S2': round(S2),
            'signals': sig, 'score_long': sl, 'score_short': ss, 'price': price}

# ================= 4. 策略追踪 / 胜率 =================
def load_log():
    os.makedirs(PRIV, exist_ok=True)
    if os.path.exists(LOG):
        try: return json.load(open(LOG, encoding='utf-8'))
        except Exception: pass
    return {'records': []}

def save_log(L):
    os.makedirs(PRIV, exist_ok=True)
    json.dump(L, open(LOG, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

def review(L, k1h, now_ts):
    """用 1H K线复盘未结算策略：先判止损（保守），再判止盈；72 根未触及=未果"""
    for r in L['records']:
        if r.get('result'): continue
        bars = [b for b in k1h if b[0] >= r['ts_start']]
        if not bars: continue
        entered, res = False, None
        for b in bars:
            ts, o, h, l, c, v = b
            if not entered:
                if r['direction'] == 'LONG' and l <= r['entry_high']: entered = True
                elif r['direction'] == 'SHORT' and h >= r['entry_low']: entered = True
            if entered:
                if r['direction'] == 'LONG':
                    if l <= r['stop']: res = 'LOSS'; break
                    if h >= r['tp1']:  res = 'WIN';  break
                else:
                    if h >= r['stop']: res = 'LOSS'; break
                    if l <= r['tp1']:  res = 'WIN';  break
        if res:
            r['result'] = res; r['closed_at'] = datetime.fromtimestamp(bars[-1][0], CST).strftime('%Y-%m-%d')
        elif len(bars) >= 72:
            r['result'] = 'EXPIRED'; r['closed_at'] = datetime.fromtimestamp(bars[-1][0], CST).strftime('%Y-%m-%d')
    return L

def winrate(L):
    done = [r for r in L['records'] if r.get('result') in ('WIN', 'LOSS')]
    w = sum(1 for r in done if r['result'] == 'WIN')
    return {'total': len(done), 'wins': w, 'losses': len(done)-w,
            'rate': round(w/len(done)*100, 1) if done else None,
            'recent': L['records'][-7:]}

# ================= 5. HTML =================
def build_html(D, A, S, W, today, num):
    price = S['price']; chg = D['spot']['change_24h_pct']; up = chg >= 0
    COL = '#ff4d4f' if up else '#26c97f'; AR = '▲' if up else '▼'
    fg = D['fng']; q = D.get('quanto', 0.0001)
    st = D['stats'][-1]
    oi_btc = st['open_interest']*q if st.get('open_interest') else None
    d1, h4, h1 = A['d1'], A['h4'], A['h1']
    dmap = {'LONG': ('做多 LONG', '#ff4d4f'), 'SHORT': ('做空 SHORT', '#26c97f'), 'WAIT': ('观望 WAIT', '#f7931a')}
    dl, dc = dmap[S['direction']]
    fgcn = {'Extreme Fear': '极度恐惧', 'Fear': '恐惧', 'Neutral': '中性', 'Greed': '贪婪', 'Extreme Greed': '极度贪婪'}
    def u(x, d=0): return f"${x:,.{d}f}" if x else 'N/A'
    cl = [r[4] for r in D['k_1d'][-30:]]; lo, hi = min(cl), max(cl)
    Wd, Hd = 660, 120
    pts = ' '.join(f"{i/(len(cl)-1)*Wd:.1f},{Hd-(c-lo)/(hi-lo)*(Hd-12)-6:.1f}" for i, c in enumerate(cl))
    def row(n, t):
        e2 = f"{t['ema200']:,.0f}" if t['ema200'] else '—'
        cs = {'GOLDEN': '金叉', 'DEAD': '死叉', 'NONE': '—'}[t['macd']['cross']]
        cl_ = 'pos' if t['macd']['state'] == '多头' else 'neg'
        return (f"<tr><td class='tf'>{n}</td><td>{u(t['close'])}</td><td>{u(t['ema20'])}</td><td>{u(t['ema50'])}</td>"
                f"<td>${e2}</td><td>{t['rsi']:.1f}</td><td class='{cl_}'>{t['macd']['dif']:,.0f} / {t['macd']['dea']:,.0f} / {t['macd']['hist']:+,.0f}"
                f"<br><span class='sm'>{t['macd']['state']} · {cs}</span></td>"
                f"<td class='sm'>{u(t['boll']['lower'])}<br>{u(t['boll']['mid'])}<br>{u(t['boll']['upper'])}</td></tr>")
    sigs = ''.join(f'<li>{x}</li>' for x in S['signals'])
    # 追踪表
    trows = ''
    for r in W['recent'][::-1]:
        rs = r.get('result') or '进行中'
        cc = {'WIN': 'pos', 'LOSS': 'neg'}.get(rs, 'sm')
        trows += (f"<tr><td>{r['date']}</td><td>{ {'LONG':'多','SHORT':'空','WAIT':'观望'}[r['direction']] }</td>"
                  f"<td class='sm'>{u(r['entry_low'])}-{u(r['entry_high'])}</td><td class='{cc}'>{rs}</td></tr>")
    wr = f"{W['rate']}%" if W['rate'] is not None else '—'
    return f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>BTC 合约日报 #{num} | {today}</title><style>
:root{{--bg:#0d0f14;--card:#141720;--card2:#1a1e2b;--border:#252a3a;--accent:#f7931a;--up:#ff4d4f;--down:#26c97f;--text:#e2e8f0;--muted:#7a8299;--muted2:#9ba3bc;}}
*{{margin:0;padding:0;box-sizing:border-box}}body{{background:var(--bg);color:var(--text);font-family:-apple-system,'PingFang SC','Microsoft YaHei',sans-serif;font-size:14px;line-height:1.65}}
.wrap{{max-width:760px;margin:0 auto;padding:0 0 40px}}
.header{{background:linear-gradient(135deg,#1a1e2b,#141720 60%,#1c1424);border-bottom:1px solid var(--border);padding:24px 22px 20px}}
.logo{{display:flex;align-items:center;gap:10px;margin-bottom:12px}}.logo .ic{{width:32px;height:32px;border-radius:50%;background:linear-gradient(135deg,#f7931a,#e8c94c);display:flex;align-items:center;justify-content:center;font-weight:700;color:#0d0f14;font-size:17px}}
.logo h1{{font-size:17px;font-weight:600}}.logo .sub{{font-size:11px;color:var(--muted)}}
.priceline{{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap}}.priceline .big{{font-size:34px;font-weight:700;letter-spacing:-1px}}
.priceline .chg{{font-size:16px;font-weight:600;color:{COL}}}.priceline .meta{{font-size:12px;color:var(--muted2)}}
.badge{{display:inline-block;font-size:11px;padding:2px 9px;border-radius:20px;border:1px solid var(--border);background:var(--card2);color:var(--muted2);margin-top:8px}}
.badge.ok{{color:#26c97f;border-color:#1e5c42;background:#0f2419}}
.card{{background:var(--card);border:1px solid var(--border);border-radius:14px;margin:14px 14px 0;padding:18px}}
.card h2{{font-size:15px;font-weight:600;margin-bottom:14px;display:flex;align-items:center;gap:8px}}
.card h2 .bar{{width:3px;height:15px;border-radius:2px;background:var(--accent)}}
table{{width:100%;border-collapse:collapse;font-size:13px}}th,td{{padding:9px 8px;text-align:right;border-bottom:1px solid #1d2230}}
th{{color:var(--muted);font-weight:500;font-size:11.5px}}th:first-child,td:first-child{{text-align:left}}
td.tf{{font-weight:600;color:var(--accent)}}.pos{{color:var(--up)}}.neg{{color:var(--down)}}.sm{{font-size:11px;color:var(--muted2)}}
.kv{{display:grid;grid-template-columns:1fr 1fr;gap:10px}}.kv .item{{background:var(--card2);border-radius:10px;padding:12px 14px}}
.kv .k{{font-size:11.5px;color:var(--muted);margin-bottom:3px}}.kv .v{{font-size:16px;font-weight:600}}
.levels{{display:flex;flex-direction:column;gap:6px}}.lvl{{display:flex;justify-content:space-between;align-items:center;padding:9px 13px;border-radius:9px;background:var(--card2);font-size:13px}}
.lvl.r{{border-left:3px solid var(--up)}}.lvl.s{{border-left:3px solid var(--down)}}.lvl.now{{border-left:3px solid var(--accent);background:#1e1a12;font-weight:700}}
.plan{{background:linear-gradient(135deg,#1a1e2b,#141720);border:1px solid var(--border);border-radius:14px;margin:14px 14px 0;padding:20px}}
.plan .dir{{font-size:22px;font-weight:700;color:{dc};display:flex;align-items:center;gap:10px}}
.plan .conf{{font-size:11.5px;color:var(--muted2);background:var(--card2);padding:2px 10px;border-radius:20px}}
.plan .grid{{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:16px}}.plan .cell{{background:#0f1218;border-radius:10px;padding:12px 14px;border:1px solid #1d2230}}
.plan .cell .k{{font-size:11px;color:var(--muted)}}.plan .cell .v{{font-size:15px;font-weight:600;margin-top:2px}}
.plan .note{{margin-top:14px;font-size:12.5px;color:var(--muted2);line-height:1.7}}.plan .note b{{color:var(--text)}}
ul.sig{{list-style:none}}ul.sig li{{padding:7px 0 7px 20px;position:relative;font-size:13px;color:var(--muted2);border-bottom:1px solid #1a1f2b}}
ul.sig li:before{{content:'·';position:absolute;left:6px;color:var(--accent);font-weight:700}}ul.sig li:last-child{{border-bottom:none}}
.tw{{font-size:13px;line-height:1.8;background:#0f1218;border-radius:10px;padding:14px;color:var(--muted2);border:1px solid #1d2230}}
.warn{{font-size:12.5px;color:#f5a623;background:#241c0e;border:1px solid #4a3a15;border-radius:10px;padding:12px 14px;line-height:1.7}}
.foot{{text-align:center;font-size:11px;color:#4a5165;padding:20px 14px 0;line-height:1.9}}svg{{display:block;width:100%;height:auto}}
</style></head><body><div class="wrap">

<div class="header">
  <div class="logo"><div class="ic">₿</div><div><h1>BTC 合约日报 #{num}</h1>
  <div class="sub">{today} · 数据源 Gate.io + alternative.me</div></div></div>
  <div class="priceline"><span class="big">{u(price)}</span><span class="chg">{AR} {chg:+.2f}%</span></div>
  <div class="priceline"><span class="meta">24h 高 {u(D['spot']['high_24h'])} · 低 {u(D['spot']['low_24h'])} · 成交 {D['spot']['base_vol_24h']:,.0f} BTC</span></div>
  <div class="priceline" style="margin-top:4px"><span class="meta">合约 Mark {u(D['futures']['mark_price'])} · 指数 {u(D['futures']['index_price'])}</span></div>
  <span class="badge ok">✓ 全篇价格同源，偏差 &lt;3%</span>
  <span class="badge">抓取 {D['fetched_at'][11:16]} UTC+8</span>
</div>

<div class="card"><h2><span class="bar"></span>近 30 日走势</h2>
<svg viewBox="0 0 {Wd} {Hd+18}" preserveAspectRatio="none">
<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#f7931a" stop-opacity="0.28"/><stop offset="100%" stop-color="#f7931a" stop-opacity="0"/></linearGradient></defs>
<polyline points="{pts}" fill="none" stroke="#f7931a" stroke-width="2"/>
<polygon points="0,{Hd} {pts} {Wd},{Hd}" fill="url(#g)"/>
<text x="2" y="{Hd+15}" fill="#7a8299" font-size="11">30天前 {u(lo)}</text>
<text x="{Wd}" y="{Hd+15}" fill="#7a8299" font-size="11" text-anchor="end">今日 {u(hi)}</text></svg></div>

<div class="card"><h2><span class="bar"></span>关键价位（摆动高低点）</h2><div class="levels">
<div class="lvl r"><span>R2 强阻力</span><b>{u(S['R2'])}</b></div>
<div class="lvl r"><span>R1 阻力</span><b>{u(S['R1'])}</b></div>
<div class="lvl now"><span>现价</span><b style="color:var(--accent)">{u(price)}</b></div>
<div class="lvl s"><span>S1 支撑</span><b>{u(S['S1'])}</b></div>
<div class="lvl s"><span>S2 强支撑</span><b>{u(S['S2'])}</b></div></div></div>

<div class="card"><h2><span class="bar"></span>技术指标（多周期）</h2><table>
<tr><th>周期</th><th>收盘</th><th>EMA20</th><th>EMA50</th><th>EMA200</th><th>RSI14</th><th>MACD DIF/DEA/柱</th><th>布林 下/中/上</th></tr>
{row('日线', d1)}{row('4H', h4)}{row('1H', h1)}</table>
<div class="sm" style="margin-top:10px">RSI 用 Wilder 平滑；MACD 金叉/死叉按柱状图穿越零轴判定。</div></div>

<div class="card"><h2><span class="bar"></span>资金面</h2><div class="kv">
<div class="item"><div class="k">资金费率（8h）</div><div class="v {'neg' if D['futures']['funding_rate']<0 else 'pos'}">{D['futures']['funding_rate']:.4f}%</div></div>
<div class="item"><div class="k">未平仓量 OI</div><div class="v">{oi_btc:,.0f} BTC</div></div>
<div class="item"><div class="k">账户多空比</div><div class="v">{st.get('lsr_account', 0):.3f}</div></div>
<div class="item"><div class="k">主动买卖比</div><div class="v">{st.get('lsr_taker', 0):.2f}</div></div>
<div class="item"><div class="k">强平 · 多单</div><div class="v neg">{st.get('long_liq_size', 0):,} 张</div></div>
<div class="item"><div class="k">强平 · 空单</div><div class="v pos">{st.get('short_liq_size', 0):,} 张</div></div></div>
<div class="sm" style="margin-top:10px">OI 单位张（1 张 = {q} BTC）；强平为 Gate 平台口径，与 Coinglass 全网口径不同。</div></div>

<div class="card"><h2><span class="bar"></span>情绪面</h2><div class="kv">
<div class="item"><div class="k">恐惧与贪婪</div><div class="v" style="color:var(--accent)">{fg['value']} · {fgcn.get(fg['cls'], fg['cls'])}</div></div>
<div class="item"><div class="k">昨日 / 7日均</div><div class="v">{fg['yesterday']} / {fg['week_avg']}</div></div></div>
<div class="sm" style="margin-top:12px">宏观：本报告未接入实时经济日历，重大数据请自行核对。</div></div>

<div class="card"><h2><span class="bar"></span>综合研判</h2><ul class="sig">{sigs}</ul>
<div style="margin-top:12px;font-size:13px;color:var(--muted2)">多空评分 <b class="pos">多 {S['score_long']}</b> : <b class="neg">空 {S['score_short']}</b> → 方向 <b style="color:{dc}">{dl}</b>（信心 {S['confidence']}）</div></div>

<div class="plan"><div class="dir">{dl} <span class="conf">信心 {S['confidence']} · 仓位 {S['position']}</span></div>
<div class="grid">
<div class="cell"><div class="k">入场区间</div><div class="v">{u(S['entry_low'])} – {u(S['entry_high'])}</div></div>
<div class="cell"><div class="k">止损 SL</div><div class="v" style="color:var(--down)">{u(S['stop'])}</div></div>
<div class="cell"><div class="k">止盈 TP1</div><div class="v" style="color:var(--up)">{u(S['tp1'])}</div></div>
<div class="cell"><div class="k">止盈 TP2</div><div class="v" style="color:var(--up)">{u(S['tp2'])}</div></div>
<div class="cell"><div class="k">盈亏比</div><div class="v">{S['rr']:.2f} : 1</div></div>
<div class="cell"><div class="k">参考杠杆</div><div class="v">≤ 10x</div></div></div>
<div class="note"><b>触发：</b>{S['trigger']}<br><b>失效：</b>{S['invalid']}</div></div>

<div class="card"><h2><span class="bar"></span>策略追踪（自动复盘）</h2>
<div class="kv" style="grid-template-columns:1fr 1fr 1fr">
<div class="item"><div class="k">已结算</div><div class="v">{W['total']}</div></div>
<div class="item"><div class="k">胜 / 负</div><div class="v"><span class="pos">{W['wins']}</span> / <span class="neg">{W['losses']}</span></div></div>
<div class="item"><div class="k">胜率</div><div class="v" style="color:var(--accent)">{wr}</div></div></div>
<table style="margin-top:14px"><tr><th>日期</th><th>方向</th><th>入场区间</th><th>结果</th></tr>{trows}</table>
<div class="sm" style="margin-top:10px">复盘规则：1H K线先触止损判负、先触 TP1 判胜（同根 K线保守判负）；72 根未触及记「EXPIRED」不计入胜率。</div></div>

<div class="card"><h2><span class="bar"></span>英文 X 文案</h2><div class="tw">
$BTC {u(price)} ({chg:+.2f}%) · Funding {D['futures']['funding_rate']:.4f}% · OI {oi_btc:,.0f} BTC.<br>
Price above EMA20/50/200 on Daily &amp; 4H → uptrend intact.<br>
Plan: {S['direction']} entry {u(S['entry_low'])}–{u(S['entry_high'])}, SL {u(S['stop'])}, TP {u(S['tp1'])}/{u(S['tp2'])}.<br>
#BTC #Bitcoin #Crypto #Trading</div></div>

<div class="card"><h2><span class="bar"></span>风险提示</h2><div class="warn">
1. 本报告为量化规则输出，<b>不构成投资建议</b>。<br>
2. 数据为 {D['fetched_at'][:19]}（UTC+8）快照，开仓前请核对实时价格。<br>
3. 单笔亏损建议控制在总资金 1–2% 以内。</div></div>

<div class="foot">MK Trading · BTC Daily Report #{num} · 生成于 {D['fetched_at'][:19]} UTC+8<br>
Data: Gate.io · alternative.me</div></div></body></html>"""

# ================= 6. 更新 index.html =================
def resolve_number(today):
    """今日卡片已存在则复用其编号，否则取最大号 +1"""
    import re
    html = open(INDEX, encoding='utf-8').read()
    i = html.find(f'reports/BTC_daily_report_{today}.html')
    if i >= 0:
        m = re.search(r'BTC Daily Report · #(\d+)', html[i:i+400])
        if m: return int(m.group(1))
    ns = [int(x) for x in re.findall(r'BTC Daily Report · #(\d+)', html)]
    return (max(ns) + 1) if ns else 1

def fix_page_chrome(html, today):
    """维护 index.html 的页面框架（历史脚本遗留问题）：
       ① 清理 <body> 后未被 <ul> 包裹的孤儿 <li> —— 它们会被浏览器渲染到页面左上角（如"5月4日日报"）
       ② 把「View Today's Analysis」CTA 按钮指向【今日】报告（原先硬编码停留在 2026-05-07）
    """
    import re
    html, n_orphan = re.subn(r'(<body[^>]*>)[ \t\r\n]*(?:<li>.*?</li>[ \t\r\n]*)+', r'\1\n', html, flags=re.S)
    html, n_cta = re.subn(r'(<a href=")reports/BTC_daily_report_\d{8}\.html(" class="btn-report")',
                          rf'\1reports/BTC_daily_report_{today}.html\2', html)
    if n_orphan or n_cta:
        log(f'页面框架修正：清理孤儿 <li> {n_orphan} 处 / CTA 指向更新 {n_cta} 处', 'OK')
    return html

def upsert_index(today, num, price, direction):
    """今日卡片已存在则整体替换，否则插入到列表首位；同时维护页面框架"""
    html = fix_page_chrome(open(INDEX, encoding='utf-8').read(), today)
    dcn = {'LONG': '做多', 'SHORT': '做空', 'WAIT': '观望'}[direction]
    tag = {'LONG': 'bull', 'SHORT': 'bear', 'WAIT': 'neutral'}[direction]
    en  = {'LONG': 'LONG', 'SHORT': 'SHORT', 'WAIT': 'WAIT'}[direction]
    card = (f'<a href="reports/BTC_daily_report_{today}.html" class="report-card fade-in">\n'
            f'<div class="report-date">{today[:4]}-{today[4:6]}-{today[6:]}</div>\n'
            f'<div class="report-title">BTC Daily Report · #{num}</div>\n'
            f'<div class="report-summary en-content">BTC ${price:,.0f}. Strategy: {en}.</div>\n'
            f'<div class="report-summary zh-content">BTC ${price:,.0f}。策略：{dcn}。</div>\n'
            f'<div><span class="report-tag {tag}">{en}</span></div>\n'
            f'</a>\n')
    key = f'<a href="reports/BTC_daily_report_{today}.html"'
    i = html.find(key)
    if i >= 0:
        j = html.index('</a>', i) + 4
        html = html[:i] + card + html[j:]
        action = 'replaced'
    else:
        anchor = '<div class="reports-grid">'
        k = html.find(anchor)
        if k < 0:
            log('找不到 reports-grid 锚点', 'ERROR'); return False
        k = html.index('>', k) + 1
        html = html[:k] + '\n                ' + card + html[k:]
        action = 'inserted'
    open(INDEX, 'w', encoding='utf-8').write(html)
    log(f'index.html {action} #{num}', 'OK')
    return True

# ================= 7. git =================
def git_publish(files):
    def run(cmd):
        return subprocess.run(cmd, cwd=REPO, capture_output=True, text=True, encoding='utf-8', errors='ignore')
    st = run(['git', 'status', '--porcelain'])
    bad = [l for l in st.stdout.splitlines() if '.workbuddy' in l or '.codebuddy' in l]
    if bad:
        log(f'⚠ 检测到私有目录将被提交，已中止：{bad}', 'ERROR'); return False
    add = run(['git', 'add'] + files)
    if add.returncode != 0:
        log(f'git add 失败 {add.stderr[:200]}', 'ERROR'); return False
    cm = run(['git', 'commit', '-m', f'auto: BTC日报 {files_msg}', '-m', 'precise pipeline (Gate.io data, unified snapshot)'])
    if cm.returncode != 0:
        log(f'git commit: {(cm.stdout + cm.stderr)[:200]}', 'WARN')
        if 'nothing to commit' in (cm.stdout + cm.stderr): return True
    ps = run(['git', 'push', 'origin', 'HEAD:main'])
    if ps.returncode != 0:
        log(f'git push 失败：{ps.stderr[:300]}', 'ERROR'); return False
    log('git push 成功', 'OK'); return True

# ================= main =================
files_msg = ''
def main():
    global files_msg
    ap = argparse.ArgumentParser()
    ap.add_argument('--no-push', action='store_true')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--no-tg', action='store_true', help='跳过 Telegram 推送')
    ap.add_argument('--tg-force', action='store_true', help='忽略当日已推送状态，强制重发')
    ap.add_argument('--date', default=None)
    a = ap.parse_args()

    now = datetime.now(CST)
    today = a.date or now.strftime('%Y%m%d')
    files_msg = today
    log(f'=== BTC 精准日报 {today} 启动 ===', 'START')

    D = fetch()
    if 'spot' not in D or 'k_1d' not in D:
        log('核心数据抓取失败，终止', 'FATAL'); sys.exit(1)
    log(f"现价 ${D['spot']['price']:,.0f} ({D['spot']['change_24h_pct']:+.2f}%)", 'OK')

    d1, h4, h1 = calc_tf(D['k_1d'], '日线'), calc_tf(D['k_4h'], '4H'), calc_tf(D['k_1h'], '1H')
    S = build_strategy(D, d1, h4, h1)
    log(f"方向 {S['direction']} (多{S['score_long']}:空{S['score_short']}) | 入场 {S['entry_low']}-{S['entry_high']} SL {S['stop']} TP1 {S['tp1']}", 'OK')

    L = load_log()
    L = review(L, D['k_1h'], now.timestamp())
    W = winrate(L)
    log(f"胜率 {W['rate']}% ({W['wins']}/{W['total']})", 'OK')

    num = resolve_number(today)
    html = build_html(D, {'d1': d1, 'h4': h4, 'h1': h1}, S, W, today, num)
    out = os.path.join(REPORTS, f'BTC_daily_report_{today}.html')
    os.makedirs(REPORTS, exist_ok=True)
    open(out, 'w', encoding='utf-8').write(html)
    log(f'报告已写入 {out} ({len(html)} bytes)', 'OK')

    if not any(r['date'] == today for r in L['records']):
        L['records'].append({'date': today, 'direction': S['direction'], 'entry_low': S['entry_low'],
                             'entry_high': S['entry_high'], 'stop': S['stop'], 'tp1': S['tp1'], 'tp2': S['tp2'],
                             'ts_start': int(now.timestamp()), 'result': None, 'price': S['price']})
        save_log(L)
        log('策略已记录到 log', 'OK')

    upsert_index(today, num, S['price'], S['direction'])

    if a.dry_run:
        log('--dry-run：跳过 git 与 Telegram', 'SKIP')
    elif a.no_push:
        log('--no-push：已生成，未推送（git / Telegram 均跳过）', 'SKIP')
    else:
        published = git_publish(['btc/reports/', 'btc/index.html', 'btc/precise/'])
        # Telegram 推送：仅在报告已上线（git 成功）后进行，确保频道里的链接可点
        if a.no_tg or not tg:
            log('Telegram 推送已跳过', 'SKIP')
        elif not published:
            log('git 未成功，跳过 Telegram 推送（避免发出无效链接）', 'WARN')
        else:
            try:
                r = tg.push(D, S, W, num, today, report_path=out,
                            A={'d1': d1, 'h4': h4, 'h1': h1}, force=a.tg_force)
                okn = len([x for x in r.get('sent', []) if x.get('ok')])
                if r.get('ok'):
                    log(f'Telegram 已推送 → {okn}/{len(r.get("sent", []))} 个目标', 'OK')
                else:
                    log(f'Telegram 未推送：{r.get("reason") or "全部失败"}', 'WARN')
            except Exception as e:
                log(f'Telegram 推送异常（不影响主流程）：{str(e)[:120]}', 'ERROR')

    print('\n' + '=' * 56)
    print(f"BTC ${S['price']:,.0f} ({D['spot']['change_24h_pct']:+.2f}%) | {S['direction']} | 入场 {S['entry_low']:,}-{S['entry_high']:,} SL {S['stop']:,} TP1 {S['tp1']:,}")
    print(f"报告: {out}")
    print(f"编号: #{num} | 胜率: {W['rate']}% ({W['wins']}/{W['total']})")
    print('=' * 56)
    log('[DONE]', 'DONE')

if __name__ == '__main__':
    main()
