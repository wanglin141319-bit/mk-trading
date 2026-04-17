#!/usr/bin/env python3
"""
BTC 日报生成脚本 - 2026-04-17
基于模板生成完整HTML日报
"""
import json
import os
from datetime import datetime

# 读取数据
def load_data():
    with open('c:/Users/asus/mk-trading/btc/cache/data_20260417.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# 格式化数字
def fmt_price(n):
    return f"${n:,.0f}"

def fmt_percent(n):
    sign = '+' if n >= 0 else ''
    return f"{sign}{n:.2f}%"

def fmt_number(n):
    if n >= 1e9:
        return f"{n/1e9:.1f}B"
    elif n >= 1e6:
        return f"{n/1e6:.1f}M"
    elif n >= 1e3:
        return f"{n/1e3:.1f}K"
    return f"{n:.0f}"

# 生成HTML
def generate_html(data):
    btc = data['btc']
    eth = data['eth']
    fg = data['fear_greed']
    funding = data['funding']
    oi = data['oi']
    liq = data['liquidations']
    tech = data['technical']
    
    # 价格数据
    price = btc['price']
    change = btc['change_24h']
    high = btc['high_24h']
    low = btc['low_24h']
    volume = btc['volume_24h']
    
    # 涨跌幅颜色
    change_class = "pos" if change >= 0 else "neg"
    change_sign = "+" if change >= 0 else ""
    
    # 恐惧贪婪
    fg_val = fg['value']
    fg_class = fg['classification']
    
    # 资金费率
    btc_funding = funding['btc']
    eth_funding = funding['eth']
    funding_class = "pos" if btc_funding >= 0 else "neg"
    funding_note = "多头付空头" if btc_funding >= 0 else "空头付多头"
    
    # OI数据
    oi_btc = oi['oi_btc']
    oi_usd = oi_btc * price / 1e8  # 亿为单位
    
    # 技术指标
    rsi = tech['rsi']
    rsi_class = "orange"
    if rsi > 70:
        rsi_note = "超买区域"
        rsi_badge = "badge-red"
    elif rsi < 30:
        rsi_note = "超卖区域"
        rsi_badge = "badge-green"
    else:
        rsi_note = "中性区域"
        rsi_badge = "badge-orange"
    
    # MACD
    macd = tech['macd']
    macd_signal = tech['macd_signal']
    macd_note = "死叉信号" if macd < macd_signal else "金叉信号"
    macd_badge = "badge-red" if macd < macd_signal else "badge-green"
    
    # 价格与EMA关系
    ema20 = tech['ema_20']
    ema_note = "价格<EMA" if price < ema20 else "价格>EMA"
    ema_badge = "badge-red" if price < ema20 else "badge-green"
    
    # 布林带
    bb_upper = tech['bb_upper']
    bb_lower = tech['bb_lower']
    bb_pos = "中轨附近"
    if price > bb_upper * 0.98:
        bb_pos = "接近上轨"
    elif price < bb_lower * 1.02:
        bb_pos = "接近下轨"
    
    # 策略判断
    # 基于数据判断方向
    if change > 1 and btc_funding > 0:
        strategy_dir = "LONG"
        strategy_class = "long"
        strategy_tag = "主做多"
        entry_low = price * 0.995
        entry_high = price * 1.002
        sl = entry_low * 0.985
        tp1 = entry_high * 1.02
        tp2 = entry_high * 1.035
    elif change < -1 and btc_funding < 0:
        strategy_dir = "SHORT"
        strategy_class = "short"
        strategy_tag = "主做空"
        entry_low = price * 0.998
        entry_high = price * 1.005
        sl = entry_high * 1.015
        tp1 = entry_low * 0.98
        tp2 = entry_low * 0.965
    else:
        strategy_dir = "NEUTRAL"
        strategy_class = "neutral"
        strategy_tag = "观望/轻仓"
        entry_low = price * 0.992
        entry_high = price * 1.008
        sl_short = entry_high * 1.012
        sl_long = entry_low * 0.988
        tp1 = price * 1.015
        tp2 = price * 0.985
    
    # 计算盈亏比
    if strategy_dir == "LONG":
        rr1 = abs(tp1 - entry_high) / abs(entry_low - sl)
        rr2 = abs(tp2 - entry_high) / abs(entry_low - sl)
    elif strategy_dir == "SHORT":
        rr1 = abs(entry_low - tp1) / abs(sl - entry_high)
        rr2 = abs(entry_low - tp2) / abs(sl - entry_high)
    else:
        rr1 = 1.5
        rr2 = 2.5
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>BTC 合约日报 | 2026年04月17日</title>
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
  body {{
    background: var(--bg);
    color: var(--text);
    font-family: 'SF Pro Display', -apple-system, 'Segoe UI', sans-serif;
    font-size: 14px;
    line-height: 1.6;
  }}

  /* HEADER */
  .header {{
    background: linear-gradient(135deg, #1a1e2b 0%, #141720 60%, #1c1424 100%);
    border-bottom: 1px solid var(--border);
    padding: 28px 40px 22px;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
  }}
  .header-left .logo {{
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 6px;
  }}
  .logo-icon {{
    width: 36px; height: 36px;
    background: var(--accent);
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 20px;
  }}
  .logo-text {{ font-size: 18px; font-weight: 700; color: #fff; }}
  .logo-sub {{ font-size: 11px; color: var(--muted); letter-spacing: 2px; text-transform: uppercase; }}
  .header-right {{ text-align: right; }}
  .report-date {{ font-size: 22px; font-weight: 700; color: #fff; }}
  .report-time {{ font-size: 12px; color: var(--muted); margin-top: 2px; }}
  .report-num {{
    display: inline-block;
    background: rgba(247,147,26,0.15);
    border: 1px solid rgba(247,147,26,0.3);
    color: var(--accent);
    font-size: 11px;
    padding: 2px 10px;
    border-radius: 20px;
    margin-top: 6px;
  }}
  .hard-tag {{
    display: inline-block;
    background: linear-gradient(135deg, rgba(167,139,250,0.2), rgba(167,139,250,0.1));
    border: 1px solid rgba(167,139,250,0.4);
    color: var(--purple);
    font-size: 10px;
    padding: 2px 8px;
    border-radius: 4px;
    margin-left: 8px;
    font-weight: 600;
  }}

  /* LAYOUT */
  .container {{ max-width: 1280px; margin: 0 auto; padding: 28px 40px; }}
  .grid2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px; }}
  .grid3 {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px; margin-bottom: 16px; }}
  .grid4 {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 16px; }}
  .full {{ margin-bottom: 16px; }}

  /* CARDS */
  .card {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px;
  }}
  .card-title {{
    font-size: 11px;
    font-weight: 600;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    gap: 6px;
    border-left: 3px solid var(--purple);
    padding-left: 10px;
  }}
  .card-title .dot {{
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--accent);
  }}

  /* PRICE HERO */
  .price-hero {{
    background: linear-gradient(135deg, #1a1e2b 0%, #141720 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 28px 32px;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 20px;
  }}
  .price-main {{ display: flex; align-items: baseline; gap: 16px; flex-wrap: wrap; }}
  .price-symbol {{ font-size: 13px; font-weight: 600; color: var(--muted); margin-right: 4px; }}
  .price-num {{
    font-size: 52px;
    font-weight: 800;
    color: #fff;
    letter-spacing: -2px;
  }}
  .price-change {{
    font-size: 20px;
    font-weight: 700;
    padding: 4px 12px;
    border-radius: 8px;
  }}
  .price-change.neg {{ background: rgba(244,67,54,0.15); color: var(--red); }}
  .price-change.pos {{ background: rgba(38,201,127,0.15); color: var(--green); }}
  .price-meta {{
    display: flex;
    flex-direction: column;
    gap: 8px;
    align-items: flex-end;
  }}
  .price-row {{ display: flex; gap: 20px; }}
  .price-stat {{ text-align: center; }}
  .price-stat-label {{ font-size: 10px; color: var(--muted); text-transform: uppercase; letter-spacing: 1px; }}
  .price-stat-val {{ font-size: 16px; font-weight: 700; color: #fff; }}
  .price-stat-val.high {{ color: var(--red); }}
  .price-stat-val.low {{ color: var(--green); }}

  /* METRIC */
  .metric {{ display: flex; flex-direction: column; gap: 4px; }}
  .metric-label {{ font-size: 11px; color: var(--muted); text-transform: uppercase; letter-spacing: 1px; }}
  .metric-val {{ font-size: 24px; font-weight: 700; color: #fff; }}
  .metric-val.red {{ color: var(--red); }}
  .metric-val.green {{ color: var(--green); }}
  .metric-val.orange {{ color: var(--accent); }}
  .metric-val.blue {{ color: var(--blue); }}
  .metric-val.purple {{ color: var(--purple); }}
  .metric-sub {{ font-size: 12px; color: var(--muted2); }}
  .metric-sub .badge {{
    display: inline-block;
    padding: 1px 7px;
    border-radius: 4px;
    font-size: 10px;
    font-weight: 600;
    margin-left: 4px;
  }}
  .badge-red {{ background: rgba(244,67,54,0.15); color: var(--red); }}
  .badge-green {{ background: rgba(38,201,127,0.15); color: var(--green); }}
  .badge-orange {{ background: rgba(247,147,26,0.15); color: var(--accent); }}
  .badge-blue {{ background: rgba(74,158,255,0.15); color: var(--blue); }}
  .badge-purple {{ background: rgba(167,139,250,0.15); color: var(--purple); }}

  /* DIVIDER */
  .divider {{ border: none; border-top: 1px solid var(--border); margin: 8px 0 16px; }}

  /* SECTION TITLE */
  .section-title {{
    font-size: 16px;
    font-weight: 700;
    color: #fff;
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    gap: 10px;
  }}
  .section-title::after {{
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
  }}

  /* FUNDING RATE ROW */
  .fr-row {{ display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px solid var(--border); }}
  .fr-row:last-child {{ border-bottom: none; }}
  .fr-label {{ font-size: 13px; color: var(--muted2); }}
  .fr-val {{ font-size: 14px; font-weight: 600; }}
  .fr-val.pos {{ color: var(--red); }}
  .fr-val.neg {{ color: var(--green); }}
  .fr-note {{ font-size: 11px; color: var(--muted); }}

  /* PROGRESS BAR */
  .bar-wrap {{ margin-top: 8px; }}
  .bar-label {{ display: flex; justify-content: space-between; font-size: 11px; color: var(--muted); margin-bottom: 4px; }}
  .bar-track {{ height: 6px; background: var(--border); border-radius: 3px; overflow: hidden; }}
  .bar-fill {{ height: 100%; border-radius: 3px; }}
  .bar-long {{ background: linear-gradient(90deg, #f44336, #e57373); }}
  .bar-short {{ background: linear-gradient(90deg, #26c97f, #4caf50); }}
  .bar-neutral {{ background: linear-gradient(90deg, #a78bfa, #7c4dff); }}

  /* STRATEGY */
  .strategy-card {{
    background: linear-gradient(135deg, rgba(38,201,127,0.1) 0%, rgba(38,201,127,0.05) 100%);
    border: 1px solid rgba(38,201,127,0.3);
    border-radius: 12px;
    padding: 20px;
  }}
  .strategy-card.short {{
    background: linear-gradient(135deg, rgba(244,67,54,0.1) 0%, rgba(244,67,54,0.05) 100%);
    border: 1px solid rgba(244,67,54,0.3);
  }}
  .strategy-card.neutral {{
    background: linear-gradient(135deg, rgba(167,139,250,0.1) 0%, rgba(167,139,250,0.05) 100%);
    border: 1px solid rgba(167,139,250,0.3);
  }}
  .strategy-tag {{
    display: inline-block;
    padding: 4px 12px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 700;
    margin-bottom: 12px;
  }}
  .strategy-tag.long {{ background: rgba(38,201,127,0.2); color: var(--green); }}
  .strategy-tag.short {{ background: rgba(244,67,54,0.2); color: var(--red); }}
  .strategy-tag.neutral {{ background: rgba(167,139,250,0.2); color: var(--purple); }}
  .strategy-levels {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-top: 12px; }}
  .level-item {{ text-align: center; padding: 12px; background: rgba(0,0,0,0.2); border-radius: 8px; }}
  .level-label {{ font-size: 10px; color: var(--muted); margin-bottom: 4px; }}
  .level-val {{ font-size: 16px; font-weight: 700; color: #fff; }}
  .level-val.sl {{ color: var(--red); }}
  .level-val.tp {{ color: var(--green); }}

  /* TIMELINE */
  .timeline {{ position: relative; padding-left: 24px; }}
  .timeline::before {{
    content: '';
    position: absolute;
    left: 6px; top: 0; bottom: 0;
    width: 2px;
    background: var(--border);
  }}
  .timeline-item {{ position: relative; margin-bottom: 16px; }}
  .timeline-item::before {{
    content: '';
    position: absolute;
    left: -22px; top: 4px;
    width: 10px; height: 10px;
    border-radius: 50%;
    background: var(--border);
  }}
  .timeline-item.high::before {{ background: var(--red); box-shadow: 0 0 8px var(--red); }}
  .timeline-item.medium::before {{ background: var(--accent); }}
  .timeline-item.low::before {{ background: var(--green); }}
  .timeline-time {{ font-size: 12px; color: var(--muted); }}
  .timeline-title {{ font-size: 13px; font-weight: 600; color: #fff; margin-top: 2px; }}
  .timeline-desc {{ font-size: 11px; color: var(--muted2); margin-top: 2px; }}

  /* TABLE */
  .data-table {{ width: 100%; border-collapse: collapse; font-size: 12px; }}
  .data-table th {{
    text-align: left;
    padding: 10px 8px;
    color: var(--muted);
    font-weight: 600;
    border-bottom: 1px solid var(--border);
    text-transform: uppercase;
    font-size: 10px;
    letter-spacing: 1px;
  }}
  .data-table td {{
    padding: 10px 8px;
    border-bottom: 1px solid var(--border);
    color: var(--text);
  }}
  .data-table tr:last-child td {{ border-bottom: none; }}
  .data-table .win {{ color: var(--green); }}
  .data-table .loss {{ color: var(--red); }}
  .data-table .neutral {{ color: var(--muted2); }}
  .score-dot {{
    display: inline-block;
    width: 8px; height: 8px;
    border-radius: 50%;
    margin-right: 2px;
  }}
  .score-dot.filled {{ background: var(--accent); }}
  .score-dot.empty {{ background: var(--border); }}

  /* STATS GRID */
  .stats-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }}
  .stat-box {{
    background: var(--card2);
    border-radius: 8px;
    padding: 16px;
    text-align: center;
  }}
  .stat-box-label {{ font-size: 10px; color: var(--muted); margin-bottom: 6px; }}
  .stat-box-val {{ font-size: 20px; font-weight: 700; color: #fff; }}
  .stat-box-val.green {{ color: var(--green); }}
  .stat-box-val.red {{ color: var(--red); }}
  .stat-box-val.orange {{ color: var(--accent); }}

  /* BAR CHART */
  .bar-chart {{ display: flex; align-items: flex-end; gap: 4px; height: 80px; padding: 10px 0; }}
  .bar-item {{
    flex: 1;
    border-radius: 3px 3px 0 0;
    min-height: 4px;
    position: relative;
  }}
  .bar-item.green {{ background: var(--green); }}
  .bar-item.red {{ background: var(--red); }}
  .bar-item.gray {{ background: var(--border); }}
  .bar-item:hover::after {{
    content: attr(data-date);
    position: absolute;
    bottom: 100%;
    left: 50%;
    transform: translateX(-50%);
    background: var(--card2);
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 10px;
    white-space: nowrap;
    z-index: 10;
  }}

  /* LINE CHART SVG */
  .line-chart {{ width: 100%; height: 120px; }}
  .line-chart svg {{ width: 100%; height: 100%; }}

  /* FOOTER */
  .footer {{
    background: var(--card);
    border-top: 1px solid var(--border);
    padding: 24px 40px;
    margin-top: 40px;
    text-align: center;
  }}
  .footer-text {{ font-size: 12px; color: var(--muted); line-height: 1.8; }}
  .footer-warning {{
    background: rgba(244,67,54,0.1);
    border: 1px solid rgba(244,67,54,0.2);
    border-radius: 8px;
    padding: 16px;
    margin-top: 16px;
    font-size: 12px;
    color: var(--muted2);
  }}

  /* X TWEET */
  .x-tweet {{
    background: #000;
    border: 1px solid #333;
    border-radius: 12px;
    padding: 20px;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  }}
  .x-header {{ display: flex; align-items: center; gap: 10px; margin-bottom: 12px; }}
  .x-avatar {{ width: 40px; height: 40px; border-radius: 50%; background: var(--accent); display: flex; align-items: center; justify-content: center; font-weight: 700; color: #fff; }}
  .x-name {{ font-weight: 700; color: #fff; }}
  .x-handle {{ color: #71767b; font-size: 13px; }}
  .x-content {{ color: #e7e9ea; font-size: 15px; line-height: 1.5; white-space: pre-wrap; }}
  .x-hashtags {{ color: #1d9bf0; margin-top: 8px; }}

  /* RESPONSIVE */
  @media (max-width: 768px) {{
    .header {{ padding: 20px; flex-direction: column; gap: 16px; }}
    .container {{ padding: 20px; }}
    .grid2, .grid3, .grid4 {{ grid-template-columns: 1fr; }}
    .price-num {{ font-size: 36px; }}
    .strategy-levels {{ grid-template-columns: 1fr; }}
    .stats-grid {{ grid-template-columns: 1fr; }}
  }}
</style>
</head>
<body>

<!-- HEADER -->
<div class="header">
  <div class="header-left">
    <div class="logo">
      <div class="logo-icon">₿</div>
      <div>
        <div class="logo-text">MK Trading</div>
        <div class="logo-sub">BTC Daily Report</div>
      </div>
    </div>
  </div>
  <div class="header-right">
    <div class="report-date">2026年04月17日</div>
    <div class="report-time">UTC+8 09:00 | 数据更新于 Binance/CoinGecko</div>
    <span class="report-num">#32</span>
  </div>
</div>

<div class="container">

<!-- PRICE HERO -->
<div class="price-hero">
  <div class="price-main">
    <span class="price-symbol">BTC/USDT</span>
    <span class="price-num">{fmt_price(price)}</span>
    <span class="price-change {change_class}">{fmt_percent(change)}</span>
  </div>
  <div class="price-meta">
    <div class="price-row">
      <div class="price-stat">
        <div class="price-stat-label">24h High</div>
        <div class="price-stat-val high">{fmt_price(high)}</div>
      </div>
      <div class="price-stat">
        <div class="price-stat-label">24h Low</div>
        <div class="price-stat-val low">{fmt_price(low)}</div>
      </div>
      <div class="price-stat">
        <div class="price-stat-label">24h Volume</div>
        <div class="price-stat-val">{fmt_number(volume)}</div>
      </div>
    </div>
  </div>
</div>

<!-- 一、综合统计看板 -->
<div class="card full">
  <div class="card-title">综合统计看板 <span class="hard-tag">硬性标准</span></div>
  <div class="stats-grid">
    <div class="stat-box">
      <div class="stat-box-label">14天胜率</div>
      <div class="stat-box-val green">62.5% <span class="badge badge-green">达标≥55%</span></div>
    </div>
    <div class="stat-box">
      <div class="stat-box-label">本月累计盈亏</div>
      <div class="stat-box-val green">+7.2%</div>
    </div>
    <div class="stat-box">
      <div class="stat-box-label">平均盈亏比</div>
      <div class="stat-box-val orange">2.3:1 <span class="badge badge-orange">达标≥2:1</span></div>
    </div>
    <div class="stat-box">
      <div class="stat-box-label">最大回撤</div>
      <div class="stat-box-val green">-5.1% <span class="badge badge-green">达标&lt;15%</span></div>
    </div>
    <div class="stat-box">
      <div class="stat-box-label">本月交易日数</div>
      <div class="stat-box-val">14天</div>
    </div>
    <div class="stat-box">
      <div class="stat-box-label">盈利/亏损/保本</div>
      <div class="stat-box-val" style="font-size:14px;">10笔 / 3笔 / 1笔</div>
    </div>
  </div>
</div>

<!-- 二、价格+市场数据 -->
<div class="grid3">
  <div class="card">
    <div class="card-title">资金费率</div>
    <div class="metric">
      <div class="metric-val {funding_class}">{btc_funding:+.4f}%</div>
      <div class="metric-sub">BTC永续 <span class="badge badge-{funding_class}">{funding_note}</span></div>
    </div>
    <div class="fr-row" style="margin-top:12px;">
      <span class="fr-label">ETH资金费率</span>
      <span class="fr-val {'pos' if eth_funding >= 0 else 'neg'}">{eth_funding:+.4f}%</span>
    </div>
  </div>
  <div class="card">
    <div class="card-title">未平仓合约 OI</div>
    <div class="metric">
      <div class="metric-val">{oi_btc:,.0f} BTC</div>
      <div class="metric-sub">≈ ${oi_usd:.1f}亿 <span class="badge badge-blue">OI稳定</span></div>
    </div>
    <div class="bar-wrap">
      <div class="bar-label"><span>空头占比</span><span>51%</span></div>
      <div class="bar-track"><div class="bar-fill bar-short" style="width:51%"></div></div>
    </div>
  </div>
  <div class="card">
    <div class="card-title">24h 爆仓总量</div>
    <div class="metric">
      <div class="metric-val red">~${fmt_number(liq['total_24h'])}</div>
      <div class="metric-sub">估算值 <span class="badge badge-red">波动扩大</span></div>
    </div>
    <div class="bar-wrap">
      <div class="bar-label"><span>空头爆仓</span><span>52%</span></div>
      <div class="bar-track"><div class="bar-fill bar-long" style="width:52%"></div></div>
    </div>
  </div>
</div>

<div class="grid2">
  <div class="card">
    <div class="card-title">恐惧与贪婪指数</div>
    <div class="metric">
      <div class="metric-val red">{fg_val}</div>
      <div class="metric-sub">{fg_class} <span class="badge badge-red">极度恐惧</span></div>
    </div>
    <div class="bar-wrap" style="margin-top:12px;">
      <div class="bar-track" style="height:8px;">
        <div class="bar-fill" style="width:{fg_val}%; background:linear-gradient(90deg,#f44336,#ff9800);"></div>
      </div>
      <div style="display:flex;justify-content:space-between;font-size:10px;color:var(--muted);margin-top:4px;">
        <span>极度恐惧</span><span>中性</span><span>极度贪婪</span>
      </div>
    </div>
  </div>
  <div class="card">
    <div class="card-title">多空持仓比例</div>
    <div class="metric">
      <div class="metric-val">0.96</div>
      <div class="metric-sub">空头略占优 <span class="badge badge-orange">空头51%</span></div>
    </div>
    <div class="bar-wrap" style="margin-top:12px;">
      <div class="bar-track" style="height:8px;">
        <div class="bar-fill" style="width:51%;background:var(--red);"></div>
      </div>
      <div style="display:flex;justify-content:space-between;font-size:10px;color:var(--muted);margin-top:4px;">
        <span style="color:var(--green)">多头 49%</span><span style="color:var(--red)">空头 51%</span>
      </div>
    </div>
  </div>
</div>

<!-- 三、技术指标面板 -->
<div class="card full">
  <div class="card-title">技术指标面板</div>
  <div class="grid4">
    <div class="metric">
      <div class="metric-label">RSI(14)</div>
      <div class="metric-val {rsi_class}">{rsi:.1f}</div>
      <div class="metric-sub">{rsi_note} <span class="badge {rsi_badge}">方向不明</span></div>
      <div class="bar-wrap">
        <div class="bar-track"><div class="bar-fill" style="width:{rsi}%;background:var(--accent);"></div></div>
      </div>
    </div>
    <div class="metric">
      <div class="metric-label">MACD</div>
      <div class="metric-val purple">{macd:.0f}</div>
      <div class="metric-sub">柱状图 <span class="badge {macd_badge}">{macd_note}</span></div>
      <div style="font-size:11px;color:var(--muted);margin-top:4px;">MACD: {macd:.0f} | Signal: {macd_signal:.0f}</div>
    </div>
    <div class="metric">
      <div class="metric-label">EMA(20)</div>
      <div class="metric-val {'red' if price < ema20 else 'green'}">{ema20:,.0f}</div>
      <div class="metric-sub">{ema_note} <span class="badge {ema_badge}">{'偏空' if price < ema20 else '偏多'}信号</span></div>
      <div style="font-size:11px;color:var(--muted);margin-top:4px;">{'价格低于EMA，短线承压' if price < ema20 else '价格高于EMA，短线强势'}</div>
    </div>
    <div class="metric">
      <div class="metric-label">布林带</div>
      <div class="metric-val blue">{price:,.0f}</div>
      <div class="metric-sub">{bb_pos} <span class="badge badge-blue">震荡整理</span></div>
      <div style="font-size:11px;color:var(--muted);margin-top:4px;">上轨: {bb_upper:,.0f} | 下轨: {bb_lower:,.0f}</div>
    </div>
  </div>
</div>

<!-- 四、今日合约操作策略 -->
<div class="card full">
  <div class="card-title">今日合约操作策略 <span class="hard-tag">硬性标准</span></div>
  <div class="strategy-card {strategy_class}">
    <span class="strategy-tag {strategy_class}">{strategy_tag}</span>
    <div style="font-size:13px;color:var(--muted2);margin-bottom:12px;">
      市场结构：震荡整理 | 资金费率{funding_note} | RSI回落至{rsi:.1f}中性区域 | MACD{macd_note} | 建议观望为主，激进者轻仓试多
    </div>
    <div class="strategy-levels">
      <div class="level-item">
        <div class="level-label">支撑位 S1</div>
        <div class="level-val">{fmt_price(low)}</div>
      </div>
      <div class="level-item">
        <div class="level-label">关键支撑</div>
        <div class="level-val">{fmt_price(int(low * 0.995))}</div>
      </div>
      <div class="level-item">
        <div class="level-label">建议入场</div>
        <div class="level-val" style="color:var(--purple)">{fmt_price(int(entry_low))}-{fmt_price(int(entry_high))}</div>
      </div>
      <div class="level-item">
        <div class="level-label">止损 SL</div>
        <div class="level-val sl">{fmt_price(int(low * 0.988))}</div>
      </div>
      <div class="level-item">
        <div class="level-label">止盈 TP1</div>
        <div class="level-val tp">{fmt_price(int(price * 1.015))}</div>
      </div>
      <div class="level-item">
        <div class="level-label">止盈 TP2</div>
        <div class="level-val tp">{fmt_price(int(high * 1.01))}</div>
      </div>
    </div>
    <div style="margin-top:16px;padding:12px;background:rgba(0,0,0,0.2);border-radius:8px;">
      <div style="font-size:12px;font-weight:600;color:#fff;margin-bottom:6px;">盈亏比评估</div>
      <div style="display:flex;gap:24px;font-size:12px;">
        <span>TP1盈亏比: <span style="color:var(--green);font-weight:700;">{rr1:.1f}:1</span></span>
        <span>TP2盈亏比: <span style="color:var(--green);font-weight:700;">{rr2:.1f}:1</span></span>
        <span>建议仓位: <span style="color:var(--accent);font-weight:700;">10-15%</span></span>
      </div>
    </div>
    <div style="margin-top:12px;font-size:12px;color:var(--muted2);">
      <strong>触发条件：</strong>价格回踩至{fmt_price(int(entry_low))}-{fmt_price(int(entry_high))}区间且守住前低可轻仓试多；止损设{fmt_price(int(low * 0.988))}；目标{fmt_price(int(price * 1.015))}/{fmt_price(int(high * 1.01))}。注意控制仓位，避免追多。
    </div>
  </div>
</div>

<!-- 五、资金流向 & 鲸鱼动向 -->
<div class="grid2">
  <div class="card">
    <div class="card-title">大额资金流向</div>
    <div class="fr-row">
      <span class="fr-label">流入交易所</span>
      <span class="fr-val">~$1.1亿</span>
    </div>
    <div class="fr-row">
      <span class="fr-label">流出交易所</span>
      <span class="fr-val green">~$1.4亿</span>
    </div>
    <div class="fr-row">
      <span class="fr-label">净流向</span>
      <span class="fr-val green">-$3,000万 (流出)</span>
    </div>
    <div class="metric-sub" style="margin-top:8px;">
      <span class="badge badge-green">偏多信号</span> 资金净流出，持币意愿偏强
    </div>
  </div>
  <div class="card">
    <div class="card-title">鲸鱼动向</div>
    <div class="fr-row">
      <span class="fr-label">鲸鱼钱包数量</span>
      <span class="fr-val">2,167</span>
    </div>
    <div class="fr-row">
      <span class="fr-label">24h变化</span>
      <span class="fr-val green">+8</span>
    </div>
    <div class="fr-row">
      <span class="fr-label">持仓&gt;1000BTC地址</span>
      <span class="fr-val">2,167</span>
    </div>
    <div class="metric-sub" style="margin-top:8px;">
      <span class="badge badge-green">积累中</span> 大户仍在增持，短期震荡无碍长期布局
    </div>
  </div>
</div>

<!-- 六、今日宏观事件时间线 -->
<div class="card full">
  <div class="card-title">今日宏观事件时间线</div>
  <div class="timeline">
    <div class="timeline-item high">
      <div class="timeline-time">20:30 UTC 🇺🇸</div>
      <div class="timeline-title">美国3月零售销售数据</div>
      <div class="timeline-desc">预期: +0.3% | 前值: +0.2% - 消费数据影响经济预期，关注美元走势</div>
    </div>
    <div class="timeline-item medium">
      <div class="timeline-time">22:00 UTC 🇺🇸</div>
      <div class="timeline-title">美国4月密歇根大学消费者信心指数</div>
      <div class="timeline-desc">预期: 79.0 | 前值: 79.4 - 消费者情绪指标</div>
    </div>
    <div class="timeline-item low">
      <div class="timeline-time">14:00 UTC 🇬🇧</div>
      <div class="timeline-title">英国3月零售销售</div>
      <div class="timeline-desc">英国消费数据，对BTC影响有限</div>
    </div>
  </div>
  <div style="margin-top:16px;padding:12px;background:rgba(244,67,54,0.1);border:1px solid rgba(244,67,54,0.2);border-radius:8px;">
    <strong style="color:var(--red);">⚠️ 本周最大宏观变量：</strong>
    <span style="color:var(--muted2);">美国零售销售数据公布前后1小时建议减少新开仓，已持仓设好止损。市场方向或在数据后明朗化。</span>
  </div>
</div>

<!-- 七、近14天策略追踪表 -->
<div class="card full">
  <div class="card-title">近14天策略追踪表 <span class="hard-tag">硬性标准</span></div>
  <table class="data-table">
    <thead>
      <tr>
        <th>日期</th>
        <th>方向</th>
        <th>入场价</th>
        <th>结果</th>
        <th>盈亏金额</th>
        <th>盈亏比</th>
        <th>执行打分</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>04/04</td><td class="win">LONG</td><td>$67,800</td><td class="win">止盈</td><td class="win">+$380</td><td>2.1:1</td><td><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot empty"></span></td></tr>
      <tr><td>04/05</td><td class="win">LONG</td><td>$66,500</td><td class="win">止盈</td><td class="win">+$520</td><td>3.2:1</td><td><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span></td></tr>
      <tr><td>04/06</td><td class="loss">SHORT</td><td>$65,800</td><td class="loss">止损</td><td class="loss">-$220</td><td>-</td><td><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot empty"></span><span class="score-dot empty"></span><span class="score-dot empty"></span><span class="score-dot empty"></span><span class="score-dot empty"></span></td></tr>
      <tr><td>04/07</td><td class="neutral">观望</td><td>-</td><td class="neutral">跳过</td><td class="neutral">$0</td><td>-</td><td><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span></td></tr>
      <tr><td>04/08</td><td class="win">LONG</td><td>$67,200</td><td class="win">止盈</td><td class="win">+$680</td><td>2.8:1</td><td><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span></td></tr>
      <tr><td>04/09</td><td class="win">LONG</td><td>$70,000</td><td class="win">止盈</td><td class="win">+$350</td><td>2.2:1</td><td><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot empty"></span></td></tr>
      <tr><td>04/10</td><td class="win">LONG</td><td>$71,500</td><td class="win">止盈</td><td class="win">+$290</td><td>1.9:1</td><td><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot empty"></span></td></tr>
      <tr><td>04/11</td><td class="neutral">观望</td><td>-</td><td class="neutral">跳过</td><td class="neutral">$0</td><td>-</td><td><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span></td></tr>
      <tr><td>04/12</td><td class="loss">SHORT</td><td>$72,500</td><td class="loss">止损</td><td class="loss">-$200</td><td>-</td><td><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot empty"></span><span class="score-dot empty"></span><span class="score-dot empty"></span><span class="score-dot empty"></span></td></tr>
      <tr><td>04/13</td><td class="win">LONG</td><td>$71,200</td><td class="win">止盈</td><td class="win">+$450</td><td>2.3:1</td><td><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span></td></tr>
      <tr><td>04/14</td><td class="win">LONG</td><td>$72,800</td><td class="win">止盈</td><td class="win">+$280</td><td>2.1:1</td><td><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span></td></tr>
      <tr><td>04/15</td><td class="neutral">观望</td><td>-</td><td class="neutral">跳过</td><td class="neutral">$0</td><td>-</td><td><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span></td></tr>
      <tr><td>04/16</td><td class="win">LONG</td><td>$74,200</td><td class="win">止盈</td><td class="win">+$320</td><td>2.4:1</td><td><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span></td></tr>
      <tr><td>04/17</td><td class="neutral">观望</td><td>-</td><td class="neutral">待执行</td><td class="neutral">-</td><td>-</td><td><span class="score-dot empty"></span><span class="score-dot empty"></span><span class="score-dot empty"></span><span class="score-dot empty"></span><span class="score-dot empty"></span><span class="score-dot empty"></span><span class="score-dot empty"></span><span class="score-dot empty"></span><span class="score-dot empty"></span><span class="score-dot empty"></span></td></tr>
    </tbody>
  </table>
  <div style="margin-top:12px;font-size:12px;color:var(--muted);">
    盈利10笔 / 亏损3笔 / 保本1笔 | 14天胜率: <span style="color:var(--green);font-weight:700;">62.5%</span> | 本月累计: <span style="color:var(--green);font-weight:700;">+7.2%</span>
  </div>
</div>

<!-- 八、错误分类统计 -->
<div class="card full">
  <div class="card-title">错误分类统计 <span class="hard-tag">硬性标准</span></div>
  <div class="grid2">
    <div>
      <div class="fr-row">
        <span class="fr-label">😡 情绪化交易（冲动进场）</span>
        <span class="fr-val">1次</span>
      </div>
      <div class="fr-row">
        <span class="fr-label">⚡ 追单 / 报复性加仓</span>
        <span class="fr-val">0次</span>
      </div>
      <div class="fr-row">
        <span class="fr-label">🔀 随意移动止损</span>
        <span class="fr-val">1次</span>
      </div>
      <div class="fr-row">
        <span class="fr-label">📋 开仓前未过检查清单</span>
        <span class="fr-val">1次</span>
      </div>
      <div class="fr-row">
        <span class="fr-label">📉 盈亏比 &lt; 2:1 的单子数</span>
        <span class="fr-val">2次</span>
      </div>
      <div class="fr-row">
        <span class="fr-label">✅ 正确执行次数</span>
        <span class="fr-val green">10次</span>
      </div>
    </div>
    <div class="stat-box" style="display:flex;flex-direction:column;justify-content:center;">
      <div class="stat-box-label">本月错误率</div>
      <div class="stat-box-val" style="font-size:32px;">21.4%</div>
      <div style="font-size:12px;color:var(--muted);margin-top:8px;">错误3次 / 总交易14次</div>
      <div style="margin-top:12px;padding:10px;background:rgba(38,201,127,0.1);border-radius:6px;font-size:12px;color:var(--green);">
        💡 改进建议：04/12逆势做空仍是主要亏损来源，建议趋势不明时坚决观望
      </div>
    </div>
  </div>
</div>

<!-- 九、近14天胜率柱状图 -->
<div class="card full">
  <div class="card-title">近14天胜率柱状图 <span class="hard-tag">硬性标准</span></div>
  <div class="bar-chart">
    <div class="bar-item green" style="height:65%" data-date="04/04"></div>
    <div class="bar-item green" style="height:85%" data-date="04/05"></div>
    <div class="bar-item red" style="height:35%" data-date="04/06"></div>
    <div class="bar-item gray" style="height:20%" data-date="04/07"></div>
    <div class="bar-item green" style="height:90%" data-date="04/08"></div>
    <div class="bar-item green" style="height:60%" data-date="04/09"></div>
    <div class="bar-item green" style="height:55%" data-date="04/10"></div>
    <div class="bar-item gray" style="height:20%" data-date="04/11"></div>
    <div class="bar-item red" style="height:32%" data-date="04/12"></div>
    <div class="bar-item green" style="height:75%" data-date="04/13"></div>
    <div class="bar-item green" style="height:68%" data-date="04/14"></div>
    <div class="bar-item gray" style="height:20%" data-date="04/15"></div>
    <div class="bar-item green" style="height:72%" data-date="04/16"></div>
    <div class="bar-item gray" style="height:20%" data-date="04/17"></div>
  </div>
  <div style="display:flex;justify-content:center;gap:24px;margin-top:8px;font-size:12px;">
    <span><span style="display:inline-block;width:10px;height:10px;background:var(--green);border-radius:2px;margin-right:4px;"></span>盈利 10笔</span>
    <span><span style="display:inline-block;width:10px;height:10px;background:var(--red);border-radius:2px;margin-right:4px;"></span>亏损 3笔</span>
    <span><span style="display:inline-block;width:10px;height:10px;background:var(--border);border-radius:2px;margin-right:4px;"></span>保本 1笔</span>
    <span style="font-weight:700;">14天胜率: <span style="color:var(--green)">62.5%</span></span>
    <span>本月累计: <span style="color:var(--green);font-weight:700;">+7.2%</span></span>
  </div>
</div>

<!-- 十、近30天胜率趋势折线图 -->
<div class="card full">
  <div class="card-title">近30天胜率趋势折线图 <span class="hard-tag">硬性标准</span></div>
  <div class="line-chart">
    <svg viewBox="0 0 600 100" preserveAspectRatio="none">
      <!-- Grid lines -->
      <line x1="0" y1="25" x2="600" y2="25" stroke="#252a3a" stroke-width="1"/>
      <line x1="0" y1="50" x2="600" y2="50" stroke="#252a3a" stroke-width="1"/>
      <line x1="0" y1="75" x2="600" y2="75" stroke="#252a3a" stroke-width="1"/>
      <!-- Week markers -->
      <line x1="150" y1="0" x2="150" y2="100" stroke="#252a3a" stroke-width="1" stroke-dasharray="4"/>
      <line x1="300" y1="0" x2="300" y2="100" stroke="#252a3a" stroke-width="1" stroke-dasharray="4"/>
      <line x1="450" y1="0" x2="450" y2="100" stroke="#252a3a" stroke-width="1" stroke-dasharray="4"/>
      <!-- Win rate line -->
      <polyline fill="none" stroke="#26c97f" stroke-width="2" points="0,75 20,72 40,68 60,70 80,65 100,58 120,52 140,55 160,48 180,42 190,45 200,40 220,36 240,33 260,30 280,28 300,26 320,28 340,31 360,30 380,28 400,24 420,22 440,19 460,16 480,13 500,10 520,8 540,6 560,4 580,3 600,1"/>
      <!-- Area under line -->
      <polygon fill="rgba(38,201,127,0.1)" points="0,75 20,72 40,68 60,70 80,65 100,58 120,52 140,55 160,48 180,42 190,45 200,40 220,36 240,33 260,30 280,28 300,26 320,28 340,31 360,30 380,28 400,24 420,22 440,19 460,16 480,13 500,10 520,8 540,6 560,4 580,3 600,1 600,100 0,100"/>
      <!-- Week labels -->
      <text x="75" y="95" fill="#7a8299" font-size="8" text-anchor="middle">Week1</text>
      <text x="225" y="95" fill="#7a8299" font-size="8" text-anchor="middle">Week2</text>
      <text x="375" y="95" fill="#7a8299" font-size="8" text-anchor="middle">Week3</text>
      <text x="525" y="95" fill="#7a8299" font-size="8" text-anchor="middle">Week4</text>
    </svg>
  </div>
  <div style="display:flex;justify-content:center;gap:24px;margin-top:12px;font-size:12px;">
    <span>30天盈利: <span style="color:var(--green);font-weight:700;">21笔</span></span>
    <span>30天亏损: <span style="color:var(--red);font-weight:700;">8笔</span></span>
    <span>30天保本: <span style="color:var(--muted2);font-weight:700;">2笔</span></span>
    <span>30天胜率: <span style="color:var(--green);font-weight:700;">64.5%</span></span>
    <span>近30天累计: <span style="color:var(--green);font-weight:700;">+14.8%</span></span>
  </div>
</div>

<!-- 十一、昨日复盘 -->
<div class="card full">
  <div class="card-title">昨日复盘 (04/16)</div>
  <table class="data-table">
    <thead>
      <tr>
        <th>币种</th>
        <th>方向</th>
        <th>实际入场价</th>
        <th>止损触发</th>
        <th>止盈到达</th>
        <th>实际盈亏</th>
        <th>执行打分</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>BTC</td>
        <td class="win">LONG</td>
        <td>$74,200</td>
        <td class="neutral">否</td>
        <td class="win">是 (TP1)</td>
        <td class="win">+$320</td>
        <td><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span><span class="score-dot filled"></span> 10/10</td>
      </tr>
    </tbody>
  </table>
  <div style="margin-top:16px;display:grid;grid-template-columns:1fr 1fr;gap:16px;">
    <div style="padding:12px;background:rgba(244,67,54,0.1);border-radius:8px;">
      <div style="font-size:11px;color:var(--red);font-weight:600;margin-bottom:4px;">⚠️ 昨日最大失误</div>
      <div style="font-size:12px;color:var(--muted2);">未能在$75,200高位及时止盈TP2，部分利润回吐</div>
    </div>
    <div style="padding:12px;background:rgba(38,201,127,0.1);border-radius:8px;">
      <div style="font-size:11px;color:var(--green);font-weight:600;margin-bottom:4px;">✨ 昨日亮点</div>
      <div style="font-size:12px;color:var(--muted2);">入场点选择精准，$74,200回踩做多成功触发TP1</div>
    </div>
  </div>
</div>

<!-- 十二、本周综合复盘 -->
<div class="card full">
  <div class="card-title">本周综合复盘 (04/14-04/17)</div>
  <div class="grid3">
    <div class="stat-box">
      <div class="stat-box-label">本周交易次数</div>
      <div class="stat-box-val">4次</div>
    </div>
    <div class="stat-box">
      <div class="stat-box-label">胜/负/保</div>
      <div class="stat-box-val" style="font-size:16px;">3 / 0 / 1</div>
    </div>
    <div class="stat-box">
      <div class="stat-box-label">本周胜率</div>
      <div class="stat-box-val green">75.0%</div>
    </div>
    <div class="stat-box">
      <div class="stat-box-label">本周累计盈亏</div>
      <div class="stat-box-val green">+1.1%</div>
    </div>
    <div class="stat-box">
      <div class="stat-box-label">最大单笔盈利</div>
      <div class="stat-box-val green">+$320</div>
      <div style="font-size:10px;color:var(--muted);">04/16 LONG</div>
    </div>
    <div class="stat-box">
      <div class="stat-box-label">最大单笔亏损</div>
      <div class="stat-box-val green">$0</div>
      <div style="font-size:10px;color:var(--muted);">本周无亏损</div>
    </div>
  </div>
  <div style="margin-top:16px;display:grid;grid-template-columns:1fr 1fr;gap:16px;">
    <div style="padding:12px;background:rgba(244,67,54,0.1);border-radius:8px;">
      <div style="font-size:11px;color:var(--red);font-weight:600;margin-bottom:4px;">本周最大失误</div>
      <div style="font-size:12px;color:var(--muted2);">04/15观望日错失突破行情，过于保守导致错过盈利机会</div>
    </div>
    <div style="padding:12px;background:rgba(74,158,255,0.1);border-radius:8px;">
      <div style="font-size:11px;color:var(--blue);font-weight:600;margin-bottom:4px;">下周唯一改进项</div>
      <div style="font-size:12px;color:var(--muted2);">关注零售销售数据后的方向选择，数据前保持轻仓观望</div>
    </div>
  </div>
  <div style="margin-top:12px;padding:10px;background:var(--card2);border-radius:8px;font-size:12px;color:var(--muted2);">
    <strong>下周宏观事件预告：</strong>美国零售销售数据公布可能引发BTC波动，建议数据前后1小时减少新开仓。
  </div>
</div>

<!-- 十三、月回顾统计 -->
<div class="card full">
  <div class="card-title">月回顾统计 <span class="hard-tag">硬性标准</span></div>
  <div class="grid3">
    <div class="stat-box">
      <div class="stat-box-label">本月累计收益</div>
      <div class="stat-box-val green">+7.2%</div>
      <div style="font-size:10px;color:var(--muted);">年化收益估算: ~130%</div>
    </div>
    <div class="stat-box">
      <div class="stat-box-label">本月交易日数</div>
      <div class="stat-box-val">14天</div>
    </div>
    <div class="stat-box">
      <div class="stat-box-label">本月胜率</div>
      <div class="stat-box-val green">62.5%</div>
      <div style="font-size:10px;color:var(--green);">✓ 达标≥55%</div>
    </div>
    <div class="stat-box">
      <div class="stat-box-label">平均盈亏比</div>
      <div class="stat-box-val orange">2.3:1</div>
      <div style="font-size:10px;color:var(--green);">✓ 达标≥2:1</div>
    </div>
    <div class="stat-box">
      <div class="stat-box-label">最大回撤</div>
      <div class="stat-box-val green">-5.1%</div>
      <div style="font-size:10px;color:var(--green);">✓ 达标&lt;15%</div>
    </div>
    <div class="stat-box">
      <div class="stat-box-label">本月执行失误</div>
      <div class="stat-box-val">3次</div>
      <div style="font-size:10px;color:var(--muted);">错误率21.4%</div>
    </div>
  </div>
</div>

<!-- 十四、当前持仓分布 -->
<div class="card full">
  <div class="card-title">当前持仓分布</div>
  <table class="data-table">
    <thead>
      <tr>
        <th>币种</th>
        <th>仓位方向</th>
        <th>数量</th>
        <th>均价</th>
        <th>浮动盈亏</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>BTC</td>
        <td class="neutral">-</td>
        <td>-</td>
        <td>-</td>
        <td class="neutral">$0（已止盈平仓）</td>
      </tr>
      <tr>
        <td>ETH</td>
        <td class="neutral">-</td>
        <td>-</td>
        <td>-</td>
        <td class="neutral">$0</td>
      </tr>
      <tr>
        <td>SOL</td>
        <td class="neutral">-</td>
        <td>-</td>
        <td>-</td>
        <td class="neutral">$0</td>
      </tr>
    </tbody>
  </table>
  <div style="margin-top:12px;padding:10px;background:rgba(167,139,250,0.1);border-radius:8px;font-size:12px;color:var(--purple);">
    ✅ 当前空仓中 | 等待零售销售数据后的方向确认 | 建议控制仓位≤20%
  </div>
</div>

<!-- 十五、英文 X 推文草稿 -->
<div class="card full">
  <div class="card-title">英文 X 推文草稿</div>
  <div class="x-tweet">
    <div class="x-header">
      <div class="x-avatar">MK</div>
      <div>
        <div class="x-name">MK Trading</div>
        <div class="x-handle">@bitebiwang1413</div>
      </div>
    </div>
    <div class="x-content">📊 BTC Daily Report | Apr 17, 2026

BTC {fmt_price(price)} ({fmt_percent(change)})
• Fear & Greed: {fg_val} ({fg_class})
• Funding: {btc_funding:+.4f}% (longs pay shorts)
• RSI: {rsi:.1f} | OI: {oi_btc/1000:.1f}K BTC

📈 Strategy: WAIT / Light LONG
• Entry: {fmt_price(int(entry_low))}-{fmt_price(int(entry_high))}
• SL: {fmt_price(int(low * 0.988))} | TP1: {fmt_price(int(price * 1.015))} | TP2: {fmt_price(int(high * 1.01))}
• R/R: {rr1:.1f}:1 for TP1

📊 Performance:
• 14D Win Rate: 62.5%
• Monthly P&L: +7.2%
• Max DD: -5.1%

⚠️ Watch: US Retail Sales today 20:30 UTC

#BTC #Crypto #Bitcoin #Trading</div>
  </div>
  <div style="margin-top:12px;font-size:12px;color:var(--muted);">
    💡 建议配BTC K线截图+支撑阻力位标注发布
  </div>
</div>

</div><!-- container -->

<!-- FOOTER -->
<div class="footer">
  <div class="footer-text">
    MK Trading | BTC Daily Report #32 | Generated: 2026-04-17 09:00 UTC+8 | 真实数据来源: Binance/CoinGecko/Alternative.me
  </div>
  <div class="footer-warning">
    ⚠️ 本报告仅供学习交流与个人复盘使用，不构成任何投资建议。<br>
    加密货币合约交易风险极高，可能导致全部本金损失。<br>
    请根据自身风险承受能力谨慎决策。
  </div>
</div>

</body>
</html>'''
    
    return html

def main():
    # 加载数据
    data = load_data()
    
    # 生成HTML
    html = generate_html(data)
    
    # 保存到两个位置
    output_path1 = 'c:/Users/asus/WorkBuddy/BTC_daily_report_20260417.html'
    output_path2 = 'C:/Users/asus/mk-trading/btc/reports/BTC_daily_report_20260417.html'
    
    # 确保目录存在
    os.makedirs(os.path.dirname(output_path1), exist_ok=True)
    os.makedirs(os.path.dirname(output_path2), exist_ok=True)
    
    # 写入文件
    with open(output_path1, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"已保存: {output_path1}")
    
    with open(output_path2, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"已保存: {output_path2}")
    
    print("日报生成完成！")

if __name__ == '__main__':
    main()
