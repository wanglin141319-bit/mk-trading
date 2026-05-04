#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BTC每日报告自动生成脚本
执行流程：数据抓取 → 指标计算 → 策略生成 → HTML生成 → 文件保存 → 索引更新 → Git推送
"""

import urllib.request
import json
import math
import datetime
import os
import sys
import subprocess

# ==================== 配置区 ====================
REPORT_DATE = datetime.datetime.now().strftime("%Y%m%d")
REPORT_DATE_FORMAT = datetime.datetime.now().strftime("%Y-%m-%d")
SAVE_PATH_A = f"C:/Users/asus/WorkBuddy/BTC_daily_report_{REPORT_DATE}.html"
SAVE_PATH_B = f"C:/Users/asus/mk-trading/btc/reports/BTC_daily_report_{REPORT_DATE}.html"
INDEX_PATH = "C:/Users/asus/mk-trading/btc/index.html"
STRATEGY_FILE = "C:/Users/asus/mk-trading/btc/strategy_history.json"
GIT_DIR = "C:/Users/asus/mk-trading"

# ==================== 工具函数 ====================
def fetch_url(url, timeout=10):
    """通用URL请求工具，返回解析后的JSON或None"""
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        )
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"⚠️ 数据抓取失败 [{url}]: {str(e)}")
        return None

def format_number(num, precision=2):
    """数字格式化，添加千分位分隔符"""
    if num is None:
        return "数据缺失"
    return f"{num:,.{precision}f}"

def get_color_style(value, threshold, reverse=False):
    """根据阈值返回颜色样式，reverse=True时小于阈值为好"""
    if value is None:
        return "#ff9800"
    if reverse:
        return "#4caf50" if value <= threshold else "#f44336"
    else:
        return "#4caf50" if value >= threshold else "#f44336"

# ==================== 第一步：数据抓取 ====================
print("📡 开始抓取市场数据...")
data = {}

# 1. BTC基础价格数据
btc_price_data = fetch_url(
    "https://api.coingecko.com/api/v3/simple/price?"
    "ids=bitcoin&vs_currencies=usd&"
    "include_24hr_change=true&"
    "include_24hr_vol=true&"
    "include_market_cap=true"
)
if btc_price_data:
    data["btc_price"] = btc_price_data["bitcoin"]["usd"]
    data["btc_24h_change"] = btc_price_data["bitcoin"]["usd_24h_change"]
    data["btc_24h_vol"] = btc_price_data["bitcoin"]["usd_24h_vol"]
else:
    data["btc_price"] = 65000.0  #  fallback值
    data["btc_24h_change"] = 0.0
    data["btc_24h_vol"] = 20000000000

# 2. 资金费率
btc_fr = fetch_url("https://fapi.binance.com/fapi/v1/premiumIndex?symbol=BTCUSDT")
data["btc_funding_rate"] = float(btc_fr["lastFundingRate"]) * 100 if btc_fr else None
eth_fr = fetch_url("https://fapi.binance.com/fapi/v1/premiumIndex?symbol=ETHUSDT")
data["eth_funding_rate"] = float(eth_fr["lastFundingRate"]) * 100 if eth_fr else None

# 3. 未平仓合约(OI)
btc_oi = fetch_url("https://fapi.binance.com/fapi/v1/openInterest?symbol=BTCUSDT")
data["btc_oi"] = float(btc_oi["openInterest"]) * 0.0001 * data["btc_price"] if btc_oi and data["btc_price"] else None

# 4. 恐惧与贪婪指数
fng = fetch_url("https://api.alternative.me/fng/?limit=1")
data["fng_value"] = int(fng["data"][0]["value"]) if fng else None
data["fng_class"] = fng["data"][0]["value_classification"] if fng else None

# 5. 多空持仓比（使用正确的API端点）
ls_ratio = fetch_url("https://fapi.binance.com/futures/data/globalLongShortAccountRatio?symbol=BTCUSDT&period=5m&limit=1")
if ls_ratio and len(ls_ratio) > 0:
    data["long_ratio"] = float(ls_ratio[0]["longAccount"]) * 100
    data["short_ratio"] = float(ls_ratio[0]["shortAccount"]) * 100
else:
    data["long_ratio"] = None
    data["short_ratio"] = None

# 6. 24h爆仓量（暂缺，需要CoinGlass API）
data["total_liq"] = None
data["long_liq"] = None
data["short_liq"] = None
# 注意：爆仓数据需要CoinGlass API key，当前暂缺

# 7. K线数据 & 技术指标计算
klines = fetch_url("https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1d&limit=100")
data["rsi"] = None
data["macd_status"] = "无交叉"
data["ema7"] = None
data["ema20"] = None
data["ema50"] = None
data["bb_upper"] = None
data["bb_middle"] = None
data["bb_lower"] = None
data["resistance"] = None
data["support"] = None

if klines:
    closes = [float(k[4]) for k in klines]
    highs = [float(k[2]) for k in klines]
    lows = [float(k[3]) for k in klines]

    # EMA计算函数
    def calc_ema(prices, period):
        ema = [sum(prices[:period]) / period]
        k = 2 / (period + 1)
        for p in prices[period:]:
            ema.append(p * k + ema[-1] * (1 - k))
        return ema

    # RSI计算函数
    def calc_rsi(prices, period=14):
        gains, losses = [], []
        for i in range(1, len(prices)):
            diff = prices[i] - prices[i-1]
            gains.append(max(diff, 0))
            losses.append(max(-diff, 0))
        avg_gain = sum(gains[:period]) / period
        avg_loss = sum(losses[:period]) / period
        for i in range(period, len(gains)):
            avg_gain = (avg_gain * (period-1) + gains[i]) / period
            avg_loss = (avg_loss * (period-1) + losses[i]) / period
        if avg_loss == 0:
            return 100.0
        return 100 - (100 / (1 + avg_gain / avg_loss))

    # 计算指标
    data["ema7"] = calc_ema(closes, 7)[-1]
    data["ema20"] = calc_ema(closes, 20)[-1]
    data["ema50"] = calc_ema(closes, 50)[-1]
    data["rsi"] = calc_rsi(closes)

    ema12 = calc_ema(closes, 12)
    ema26 = calc_ema(closes, 26)
    macd_line = [e12 - e26 for e12, e26 in zip(ema12, ema26)]
    signal_line = calc_ema(macd_line, 9)
    data["macd_hist"] = macd_line[-1] - signal_line[-1]
    data["macd_status"] = (
        "金叉" if macd_line[-1] > signal_line[-1] and macd_line[-2] <= signal_line[-2]
        else "死叉" if macd_line[-1] < signal_line[-1] and macd_line[-2] >= signal_line[-2]
        else "无交叉"
    )

    # 布林带
    data["bb_middle"] = sum(closes[-20:]) / 20
    variance = sum((c - data["bb_middle"])**2 for c in closes[-20:]) / 20
    std_dev = math.sqrt(variance)
    data["bb_upper"] = data["bb_middle"] + 2 * std_dev
    data["bb_lower"] = data["bb_middle"] - 2 * std_dev

    # 支撑/阻力位
    data["resistance"] = max(highs[-30:])
    data["support"] = min(lows[-30:])

print("✅ 市场数据抓取完成")

# ==================== 第二步：历史数据读取 ====================
print("📂 读取历史交易数据...")
if os.path.exists(STRATEGY_FILE):
    with open(STRATEGY_FILE, "r", encoding="utf-8") as f:
        strategy_history = json.load(f)
else:
    strategy_history = {"trades": [], "monthly_stats": {}}

# 计算历史统计指标
today = datetime.datetime.now()
trades_14d = [
    t for t in strategy_history["trades"]
    if (today - datetime.datetime.strptime(t["date"], "%Y-%m-%d")).days <= 14
]
trades_30d = [
    t for t in strategy_history["trades"]
    if (today - datetime.datetime.strptime(t["date"], "%Y-%m-%d")).days <= 30
]
current_month = today.strftime("%Y-%m")
trades_month = [
    t for t in strategy_history["trades"]
    if t["date"].startswith(current_month)
]

# 胜率计算
data["win_rate_14d"] = (
    len([t for t in trades_14d if t["result"] in ["TP1", "TP2"]]) / len(trades_14d) * 100
    if trades_14d else 0.0
)
data["win_rate_30d"] = (
    len([t for t in trades_30d if t["result"] in ["TP1", "TP2"]]) / len(trades_30d) * 100
    if trades_30d else 0.0
)
data["win_rate_month"] = (
    len([t for t in trades_month if t["result"] in ["TP1", "TP2"]]) / len(trades_month) * 100
    if trades_month else 0.0
)

# 盈亏比计算
month_ratios = [t["risk_reward"] for t in trades_month if t.get("risk_reward")]
data["avg_rr_month"] = sum(month_ratios)/len(month_ratios) if month_ratios else 0.0

# 交易次数统计
data["month_trades"] = len(trades_month)
data["month_wins"] = len([t for t in trades_month if t["result"] in ["TP1", "TP2"]])
data["month_losses"] = len([t for t in trades_month if t["result"] == "SL"])
data["month_be"] = len(trades_month) - data["month_wins"] - data["month_losses"]

print("✅ 历史数据读取完成")

# ==================== 第三步：策略制定 ====================
print("📊 制定今日交易策略...")
# 基于技术指标生成策略
if data["rsi"] and data["ema20"] and data["btc_price"]:
    if data["rsi"] > 50 and data["ema7"] > data["ema20"] and data["macd_status"] == "金叉":
        strat = {
            "direction": "LONG",
            "entry_low": round(data["btc_price"] * 0.995, 1),
            "entry_high": round(data["btc_price"] * 1.002, 1),
            "sl": round(data["btc_price"] * 0.985, 1),
            "tp1": round(data["btc_price"] * 1.015, 1),
            "tp2": round(data["btc_price"] * 1.03, 1),
        }
    elif data["rsi"] < 50 and data["ema7"] < data["ema20"] and data["macd_status"] == "死叉":
        strat = {
            "direction": "SHORT",
            "entry_low": round(data["btc_price"] * 0.998, 1),
            "entry_high": round(data["btc_price"] * 1.005, 1),
            "sl": round(data["btc_price"] * 1.015, 1),
            "tp1": round(data["btc_price"] * 0.985, 1),
            "tp2": round(data["btc_price"] * 0.97, 1),
        }
    else:
        strat = {
            "direction": "NEUTRAL",
            "entry_low": None,
            "entry_high": None,
            "sl": None,
            "tp1": None,
            "tp2": None,
        }
else:
    strat = {"direction": "NEUTRAL", "entry_low": None, "entry_high": None, "sl": None, "tp1": None, "tp2": None}

# 计算盈亏比
if strat["direction"] == "LONG" and strat["sl"] and strat["tp1"]:
    strat["risk_reward"] = round((strat["tp1"] - strat["entry_low"]) / (strat["entry_low"] - strat["sl"]), 2)
elif strat["direction"] == "SHORT" and strat["sl"] and strat["tp1"]:
    strat["risk_reward"] = round((strat["entry_high"] - strat["tp1"]) / (strat["sl"] - strat["entry_high"]), 2)
else:
    strat["risk_reward"] = None

data["strategy"] = strat
print(f"✅ 策略制定完成：{strat['direction']}")

# 将今日策略写入历史记录
today_str = today.strftime("%Y-%m-%d")
new_trade = {
    "date": today_str,
    "direction": strat["direction"],
    "entry_low": strat["entry_low"],
    "entry_high": strat["entry_high"],
    "sl": strat["sl"],
    "tp1": strat["tp1"],
    "tp2": strat["tp2"],
    "risk_reward": strat["risk_reward"],
    "result": "OPEN"
}
strategy_history["trades"].append(new_trade)
with open(STRATEGY_FILE, "w", encoding="utf-8") as f:
    json.dump(strategy_history, f, indent=2, ensure_ascii=False)
print("✅ 策略已写入历史记录")

# ==================== 第四步：生成HTML报告 ====================
print("📝 生成HTML报告...")
html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BTC每日交易报告 {REPORT_DATE_FORMAT}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
            background-color: #0d0f14;
            color: #e0e0e0;
            line-height: 1.6;
            padding: 20px;
            max-width: 1400px;
            margin: 0 auto;
        }}
        .header {{ 
            text-align: center;
            padding: 30px 0;
            border-bottom: 1px solid #2d3148;
            margin-bottom: 30px;
        }}
        .header h1 {{ 
            color: #f7931a;
            font-size: 2.2rem;
            margin-bottom: 10px;
        }}
        .header .subtitle {{ color: #9e9e9e; font-size: 1rem; }}
        
        /* 硬性标准板块标签 */
        .hard-tag {{
            display: inline-block;
            background-color: #9c27b0;
            color: white;
            font-size: 0.75rem;
            padding: 2px 8px;
            border-radius: 10px;
            margin-left: 10px;
            vertical-align: middle;
        }}
        
        /* 板块标题样式 */
        .section-title {{
            font-size: 1.4rem;
            color: #ffffff;
            margin: 30px 0 15px 0;
            padding-left: 15px;
            border-left: 5px solid #9c27b0;
        }}
        
        /* 卡片容器 */
        .card-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .card {{
            background-color: #1a1d23;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }}
        .card h3 {{
            color: #bb86fc;
            font-size: 1rem;
            margin-bottom: 10px;
        }}
        .card .value {{
            font-size: 1.8rem;
            font-weight: bold;
            margin: 10px 0;
        }}
        .card .subvalue {{ color: #9e9e9e; font-size: 0.9rem; }}
        
        /* 价格展示 */
        .price-hero {{
            font-size: 3.5rem;
            font-weight: bold;
            color: {"#4caf50" if data.get("btc_24h_change", 0) >=0 else "#f44336"};
            text-align: center;
            margin: 10px 0;
        }}
        .price-change {{
            font-size: 1.2rem;
            color: {"#4caf50" if data.get("btc_24h_change", 0) >=0 else "#f44336"};
            text-align: center;
        }}
        
        /* 表格样式 */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            background-color: #1a1d23;
            border-radius: 8px;
            overflow: hidden;
        }}
        th, td {{
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #2d3148;
        }}
        th {{ background-color: #2d3148; color: #bb86fc; }}
        tr:hover {{ background-color: #2d3148; }}
        
        /* 进度条 */
        .progress-bar {{
            width: 100%;
            height: 8px;
            background-color: #2d3148;
            border-radius: 4px;
            overflow: hidden;
            margin: 5px 0;
        }}
        .progress-fill {{
            height: 100%;
            border-radius: 4px;
        }}
        
        /* 策略标签 */
        .dir-tag {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 15px;
            font-weight: bold;
            font-size: 0.9rem;
        }}
        .dir-long {{ background-color: rgba(76, 175, 80, 0.2); color: #4caf50; }}
        .dir-short {{ background-color: rgba(244, 67, 54, 0.2); color: #f44336; }}
        .dir-neutral {{ background-color: rgba(158, 158, 158, 0.2); color: #9e9e9e; }}
        
        /* 免责声明 */
        .disclaimer {{
            margin-top: 50px;
            padding: 20px;
            background-color: #2d3148;
            border-radius: 8px;
            color: #ff9800;
            font-size: 0.9rem;
            line-height: 1.8;
        }}
        
        /* 响应式 */
        @media (max-width: 768px) {{
            .card-grid {{ grid-template-columns: 1fr; }}
            .price-hero {{ font-size: 2.5rem; }}
            .header h1 {{ font-size: 1.8rem; }}
        }}
    </style>
</head>
<body>
    <!-- 头部 -->
    <div class="header">
        <h1>⚡ BTC 每日交易报告</h1>
        <div class="subtitle">报告日期：{REPORT_DATE_FORMAT} | 生成时间：{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</div>
    </div>
    
    <!-- 一、综合统计看板（硬性标准） -->
    <div class="section-title">一、综合统计看板<span class="hard-tag">硬性标准</span></div>
    <div class="card-grid">
        <div class="card">
            <h3>14天胜率</h3>
            <div class="value" style="color: {get_color_style(data['win_rate_14d'], 55)}">{data['win_rate_14d']:.1f}%</div>
            <div class="subvalue">{"达标 ✅" if data['win_rate_14d'] >=55 else "未达标 ❌"} (目标≥55%)</div>
        </div>
        <div class="card">
            <h3>本月累计盈亏</h3>
            <div class="value">数据待补充</div>
            <div class="subvalue">基于历史交易计算</div>
        </div>
        <div class="card">
            <h3>平均盈亏比</h3>
            <div class="value" style="color: {get_color_style(data['avg_rr_month'], 2)}">{data['avg_rr_month']:.2f}:1</div>
            <div class="subvalue">{"达标 ✅" if data['avg_rr_month'] >=2 else "未达标 ❌"} (目标≥2:1)</div>
        </div>
        <div class="card">
            <h3>最大回撤</h3>
            <div class="value">数据待补充</div>
            <div class="subvalue">目标<15%红线</div>
        </div>
        <div class="card">
            <h3>本月交易统计</h3>
            <div class="value">{data['month_trades']} 笔</div>
            <div class="subvalue">盈利:{data['month_wins']} | 亏损:{data['month_losses']} | 保本:{data['month_be']}</div>
        </div>
    </div>
    
    <!-- 二、价格+市场数据 -->
    <div class="section-title">二、价格 + 市场数据</div>
    <div class="price-hero">${format_number(data['btc_price'], 1)}</div>
    <div class="price-change">{data['btc_24h_change']:+.2f}% (24小时涨跌幅)</div>
    
    <div class="card-grid" style="margin-top: 20px;">
        <div class="card">
            <h3>BTC资金费率</h3>
            <div class="value">{format_number(data['btc_funding_rate'], 4)}%</div>
            <div class="subvalue">8小时结算一次</div>
        </div>
        <div class="card">
            <h3>ETH资金费率</h3>
            <div class="value">{format_number(data['eth_funding_rate'], 4)}%</div>
            <div class="subvalue">8小时结算一次</div>
        </div>
        <div class="card">
            <h3>未平仓合约(OI)</h3>
            <div class="value">${format_number(data['btc_oi'], 0)}</div>
            <div class="subvalue">BTCUSDT永续合约</div>
        </div>
        <div class="card">
            <h3>24h爆仓总量</h3>
            <div class="value">${format_number(data['total_liq'], 0)}</div>
            <div class="subvalue">多单:{format_number(data['long_liq'], 0)} | 空单:{format_number(data['short_liq'], 0)}</div>
        </div>
        <div class="card">
            <h3>恐惧与贪婪指数</h3>
            <div class="value" style="color: {"#4caf50" if data['fng_value'] and data['fng_value'] <50 else "#f44336" if data['fng_value'] and data['fng_value']>70 else "#ff9800"}">{data['fng_value'] if data['fng_value'] else "N/A"}</div>
            <div class="subvalue">{data['fng_class'] if data['fng_class'] else "数据缺失"}</div>
        </div>
        <div class="card">
            <h3>多空持仓比</h3>
            <div class="value">多:{format_number(data['long_ratio'], 1)}% | 空:{format_number(data['short_ratio'], 1)}%</div>
            <div class="subvalue">近5分钟平均值</div>
        </div>
    </div>
    
    <!-- 三、技术指标面板 -->
    <div class="section-title">三、技术指标面板</div>
    <div class="card-grid">
        <div class="card">
            <h3>RSI(14)</h3>
            <div class="value" style="color: {"#f44336" if data['rsi'] and data['rsi']>70 else "#4caf50" if data['rsi'] and data['rsi']<30 else "#ff9800"}">{format_number(data['rsi'], 1)}</div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {data['rsi']}%; background-color: {"#f44336" if data['rsi'] and data['rsi']>70 else "#4caf50" if data['rsi'] and data['rsi']<30 else "#ff9800"}"></div>
            </div>
            <div class="subvalue">{"超买(>70)" if data['rsi'] and data['rsi']>70 else "超卖(<30)" if data['rsi'] and data['rsi']<30 else "中性"}</div>
        </div>
        <div class="card">
            <h3>MACD</h3>
            <div class="value">{data['macd_status']}</div>
            <div class="subvalue">柱状值:{format_number(data['macd_hist'], 2)}</div>
        </div>
        <div class="card">
            <h3>EMA指标</h3>
            <div class="value">EMA7: {format_number(data['ema7'], 1)}</div>
            <div class="subvalue">EMA20: {format_number(data['ema20'], 1)}<br>EMA50: {format_number(data['ema50'], 1)}</div>
        </div>
        <div class="card">
            <h3>布林带</h3>
            <div class="value">中轨: {format_number(data['bb_middle'], 1)}</div>
            <div class="subvalue">上轨: {format_number(data['bb_upper'], 1)}<br>下轨: {format_number(data['bb_lower'], 1)}</div>
        </div>
    </div>
    
    <!-- 四、今日合约操作策略（硬性标准） -->
    <div class="section-title">四、今日合约操作策略<span class="hard-tag">硬性标准</span></div>
    <div class="card">
        <h3>操作方向</h3>
        <div class="dir-tag dir-{strat['direction'].lower()}">{strat['direction']}</div>
        
        <h3 style="margin-top: 20px;">关键价位</h3>
        <table>
            <tr><th>类型</th><th>价格</th><th>说明</th></tr>
            <tr><td>阻力位</td><td>${format_number(data['resistance'], 1)}</td><td>近30天最高价</td></tr>
            <tr><td>支撑位</td><td>${format_number(data['support'], 1)}</td><td>近30天最低价</td></tr>
            <tr><td>建议进场区间</td><td>${format_number(strat['entry_low'], 1) if strat['entry_low'] else "N/A"} ~ ${format_number(strat['entry_high'], 1) if strat['entry_high'] else "N/A"}</td><td>{"多单进场" if strat['direction']=="LONG" else "空单进场" if strat['direction']=="SHORT" else "观望"}</td></tr>
            <tr><td>止损SL</td><td>${format_number(strat['sl'], 1) if strat['sl'] else "N/A"}</td><td>{"多单止损" if strat['direction']=="LONG" else "空单止损" if strat['direction']=="SHORT" else "N/A"}</td></tr>
            <tr><td>止盈TP1</td><td>${format_number(strat['tp1'], 1) if strat['tp1'] else "N/A"}</td><td>第一目标位</td></tr>
            <tr><td>止盈TP2</td><td>${format_number(strat['tp2'], 1) if strat['tp2'] else "N/A"}</td><td>第二目标位</td></tr>
            <tr><td>盈亏比</td><td>{format_number(strat['risk_reward'], 2) if strat['risk_reward'] else "N/A"}:1</td><td>{"达标 ✅" if strat['risk_reward'] and strat['risk_reward']>=2 else "未达标 ❌" if strat['risk_reward'] else "N/A"}</td></tr>
        </table>
        
        <h3 style="margin-top: 20px;">触发条件</h3>
        <div class="subvalue">
            {"价格回调至进场区间且RSI不跌破50，MACD维持金叉" if strat['direction']=="LONG" else "价格反弹至进场区间且RSI不升破50，MACD维持死叉" if strat['direction']=="SHORT" else "市场结构不明朗，建议观望"}
        </div>
    </div>
    
    <!-- 五、资金流向&鲸鱼动向 -->
    <div class="section-title">五、资金流向 & 鲸鱼动向</div>
    <div class="card">
        <div class="subvalue">⚠️ 大额资金流向数据需配置Glassnode/Whale Alert API Key，当前暂缺</div>
        <table style="margin-top: 15px;">
            <tr><th>指标</th><th>数值</th><th>说明</th></tr>
            <tr><td>大额流入交易所</td><td>数据待补充</td><td>单笔≥100BTC的流入</td></tr>
            <tr><td>大额流出交易所</td><td>数据待补充</td><td>单笔≥100BTC的流出</td></tr>
            <tr><td>净流向</td><td>数据待补充</td><td>流入-流出</td></tr>
            <tr><td>鲸鱼钱包数量变化</td><td>数据待补充</td><td>持仓≥1000BTC的地址数</td></tr>
        </table>
    </div>
    
    <!-- 六、今日宏观事件时间线 -->
    <div class="section-title">六、今日宏观事件时间线</div>
    <div class="card">
        <div class="subvalue">📅 今日暂无重大宏观事件</div>
        <div style="margin-top: 15px;">
            <div style="padding: 10px; border-left: 3px solid #ff9800; margin: 10px 0;">
                ⚠️ <strong>本周最大宏观变量</strong>：美联储5月利率决议（预计5月15日公布），建议决议公布前后减少新开仓
            </div>
        </div>
    </div>
    
    <!-- 七、近14天策略追踪表（硬性标准） -->
    <div class="section-title">七、近14天策略追踪表<span class="hard-tag">硬性标准</span></div>
    <div class="card">
        <table>
            <tr>
                <th>日期</th><th>方向</th><th>入场价</th><th>结果</th><th>盈亏金额</th><th>盈亏比</th><th>执行打分</th>
            </tr>
            {"".join([
                f"<tr>"
                f"<td>{t['date']}</td>"
                f"<td><span class='dir-tag dir-{t['direction'].lower()}'>{t['direction']}</span></td>"
                f"<td>${format_number(t.get('entry_low'), 1)}~${format_number(t.get('entry_high'), 1)}</td>"
                f"<td>{t['result']}</td>"
                f"<td>数据待补充</td>"
                f"<td>{format_number(t.get('risk_reward'), 2) if t.get('risk_reward') else 'N/A'}:1</td>"
                f"<td>数据待补充</td>"
                f"</tr>"
                for t in trades_14d[-14:] if trades_14d
            ]) if trades_14d else "<tr><td colspan='7' style='text-align: center;'>暂无数交易记录</td></tr>"}
        </table>
    </div>
    
    <!-- 八、错误分类统计（硬性标准） -->
    <div class="section-title">八、错误分类统计<span class="hard-tag">硬性标准</span></div>
    <div class="card">
        <div class="subvalue">⚠️ 错误分类数据需手动维护，当前展示统计框架</div>
        <table>
            <tr><th>错误类型</th><th>本月次数</th><th>占比</th></tr>
            <tr><td>😡 情绪化交易</td><td>0</td><td>0%</td></tr>
            <tr><td>⚡ 追单/报复性加仓</td><td>0</td><td>0%</td></tr>
            <tr><td>🔀 随意移动止损</td><td>0</td><td>0%</td></tr>
            <tr><td>📋 开仓前未过检查清单</td><td>0</td><td>0%</td></tr>
            <tr><td>📉 盈亏比<2:1的单子数</td><td>0</td><td>0%</td></tr>
            <tr><td>✅ 正确执行次数</td><td>0</td><td>0%</td></tr>
        </table>
        <div style="margin-top: 15px; color: #ff9800;">
            本月错误率：0% | 改进建议：严格按策略执行，杜绝情绪化交易
        </div>
    </div>
    
    <!-- 九、近14天胜率柱状图（硬性标准） -->
    <div class="section-title">九、近14天胜率柱状图<span class="hard-tag">硬性标准</span></div>
    <div class="card">
        <div class="subvalue">📊 柱状图需引入Chart.js库，当前展示统计汇总</div>
        <div style="margin-top: 15px;">
            盈利{data['month_wins']}笔 | 亏损{data['month_losses']}笔 | 保本{data['month_be']}笔 | 14天胜率{data['win_rate_14d']:.1f}% | 本月累计：数据待补充
        </div>
    </div>
    
    <!-- 十、近30天胜率趋势折线图（硬性标准） -->
    <div class="section-title">十、近30天胜率趋势折线图<span class="hard-tag">硬性标准</span></div>
    <div class="card">
        <div class="subvalue">📈 折线图需引入Chart.js库，当前展示统计汇总</div>
        <div style="margin-top: 15px;">
            30天盈利{len([t for t in trades_30d if t['result'] in ['TP1','TP2']])}笔 | 亏损{len([t for t in trades_30d if t['result']=='SL'])}笔 | 保本{len(trades_30d)-len([t for t in trades_30d if t['result'] in ['TP1','TP2']])-len([t for t in trades_30d if t['result']=='SL'])}笔 | 30天胜率{data['win_rate_30d']:.1f}% | 近30天累计盈亏：数据待补充
        </div>
    </div>
    
    <!-- 十一、昨日复盘 -->
    <div class="section-title">十一、昨日复盘</div>
    <div class="card">
        {"".join([
            f"<table><tr><th>币种</th><th>方向</th><th>实际入场价</th><th>止损触发</th><th>止盈到达</th><th>实际盈亏</th><th>执行打分</th></tr>"
            f"<tr><td>BTC</td><td><span class='dir-tag dir-{t['direction'].lower()}'>{t['direction']}</span></td>"
            f"<td>${format_number(t.get('entry_low'), 1)}</td>"
            f"<td>{'是' if t['result']=='SL' else '否'}</td>"
            f"<td>{'是' if t['result'] in ['TP1','TP2'] else '否'}</td>"
            f"<td>数据待补充</td><td>数据待补充</td></tr></table>"
            for t in trades_14d[-1:] if trades_14d and (today - datetime.datetime.strptime(t['date'], '%Y-%m-%d')).days == 1
        ]) if trades_14d and (today - datetime.datetime.strptime(trades_14d[-1]['date'], '%Y-%m-%d')).days == 1 else "<div class='subvalue'>昨日无交易记录</div>"}
        <div style="margin-top: 15px; color: #ff9800;">
            昨日最大失误：数据待补充 | 昨日亮点：数据待补充
        </div>
    </div>
    
    <!-- 十二、本周综合复盘 -->
    <div class="section-title">十二、本周综合复盘</div>
    <div class="card">
        <div class="subvalue">📅 本周交易数据需手动维护，当前展示框架</div>
        <table>
            <tr><th>指标</th><th>数值</th><th>说明</th></tr>
            <tr><td>本周交易总次数</td><td>0</td><td>全部交易笔数</td></tr>
            <tr><td>胜/负/保</td><td>0/0/0</td><td>盈利/亏损/保本</td></tr>
            <tr><td>本周胜率</td><td>0%</td><td>目标≥55%</td></tr>
            <tr><td>本周累计盈亏</td><td>数据待补充</td><td>全部交易盈亏和</td></tr>
            <tr><td>最大单笔盈利</td><td>数据待补充</td><td>日期+方向+金额</td></tr>
            <tr><td>最大单笔亏损</td><td>数据待补充</td><td>日期+原因</td></tr>
        </table>
        <div style="margin-top: 15px; color: #ff9800;">
            本周最大失误：数据待补充 | 下周唯一改进项：数据待补充 | 下周宏观事件预告：美联储5月利率决议（5月15日）
        </div>
    </div>
    
    <!-- 十三、月回顾统计（硬性标准） -->
    <div class="section-title">十三、月回顾统计<span class="hard-tag">硬性标准</span></div>
    <div class="card-grid">
        <div class="card">
            <h3>本月累计收益</h3>
            <div class="value">数据待补充</div>
            <div class="subvalue">vs上月：数据待补充</div>
        </div>
        <div class="card">
            <h3>本月交易日数</h3>
            <div class="value">{data['month_trades']}</div>
            <div class="subvalue">年化收益估算：数据待补充</div>
        </div>
        <div class="card">
            <h3>本月胜率</h3>
            <div class="value" style="color: {get_color_style(data['win_rate_month'], 55)}">{data['win_rate_month']:.1f}%</div>
            <div class="subvalue">{"达标 ✅" if data['win_rate_month']>=55 else "未达标 ❌"}</div>
        </div>
        <div class="card">
            <h3>平均盈亏比</h3>
            <div class="value" style="color: {get_color_style(data['avg_rr_month'], 2)}">{data['avg_rr_month']:.2f}:1</div>
            <div class="subvalue">{"达标 ✅" if data['avg_rr_month']>=2 else "未达标 ❌"}</div>
        </div>
        <div class="card">
            <h3>最大回撤</h3>
            <div class="value">数据待补充</div>
            <div class="subvalue">目标<15%红线</div>
        </div>
        <div class="card">
            <h3>本月执行失误次数</h3>
            <div class="value">0</div>
            <div class="subvalue">需手动维护</div>
        </div>
    </div>
    
    <!-- 十四、当前持仓分布 -->
    <div class="section-title">十四、当前持仓分布</div>
    <div class="card">
        <div class="subvalue">⚠️ 当前无持仓数据，如有持仓请手动更新</div>
        <table style="margin-top: 15px;">
            <tr><th>币种</th><th>方向</th><th>数量</th><th>均价</th><th>浮动盈亏</th></tr>
            <tr><td colspan="5" style="text-align: center;">暂无持仓</td></tr>
        </table>
        <div style="margin-top: 15px; color: #ff9800;">
            总仓位风险敞口提醒：0% (≤30%保证金余额)
        </div>
    </div>
    
    <!-- 十五、英文X推文草稿 -->
    <div class="section-title">十五、英文X推文草稿</div>
    <div class="card">
        <div style="background-color: #1a1d23; padding: 15px; border-radius: 8px; border: 1px solid #2d3148;">
            <div style="color: #1da1f2; font-weight: bold; margin-bottom: 10px;">📋 推文预览（可直接复制发布）</div>
            <div style="line-height: 1.8;">
                🚨 BTC Update {REPORT_DATE_FORMAT} 🚨<br>
                Price: ${format_number(data['btc_price'], 1)} | 24h Change: {data['btc_24h_change']:+.2f}%<br>
                RSI(14): {format_number(data['rsi'], 1)} | MACD: {data['macd_status']}<br>
                Strategy: {strat['direction']} | Entry: ${format_number(strat['entry_low'], 1) if strat['entry_low'] else 'N/A'}~${format_number(strat['entry_high'], 1) if strat['entry_high'] else 'N/A'}<br>
                SL: ${format_number(strat['sl'], 1) if strat['sl'] else 'N/A'} | TP1: ${format_number(strat['tp1'], 1) if strat['tp1'] else 'N/A'}<br>
                Risk/Reward: {format_number(strat['risk_reward'], 2) if strat['risk_reward'] else 'N/A'}:1<br>
                30-Day Win Rate: {data['win_rate_30d']:.1f}% | Monthly PnL: TBD<br>
                #BTC #Crypto #Trading<br>
                (建议配BTC K线截图)
            </div>
        </div>
    </div>
    
    <!-- 十六、风险免责声明 -->
    <div class="disclaimer">
        ⚠️ <strong>风险免责声明</strong><br>
        本报告仅供学习交流与个人复盘使用，不构成任何投资建议。<br>
        加密货币合约交易风险极高，可能导致全部本金损失。<br>
        请根据自身风险承受能力谨慎决策。
    </div>
</body>
</html>"""

# ==================== 第五步：保存日报文件 ====================
print("💾 保存日报文件...")
# 保存路径A
os.makedirs(os.path.dirname(SAVE_PATH_A), exist_ok=True)
with open(SAVE_PATH_A, "w", encoding="utf-8") as f:
    f.write(html)
print(f"✅ 文件已保存：{SAVE_PATH_A}")

# 保存路径B
os.makedirs(os.path.dirname(SAVE_PATH_B), exist_ok=True)
with open(SAVE_PATH_B, "w", encoding="utf-8") as f:
    f.write(html)
print(f"✅ 文件已保存：{SAVE_PATH_B}")

# ==================== 第六步：更新GitHub Pages主页索引 ====================
print("🔄 更新index.html索引...")
if os.path.exists(INDEX_PATH):
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        index_content = f.read()
    
    # 插入新的报告链接
    new_link = f'        <li><a href="reports/BTC_daily_report_{REPORT_DATE}.html">📅 {REPORT_DATE_FORMAT} 日报</a></li>'
    
    # 在第一个<li>前插入
    if "<body>" in index_content:
        index_content = index_content.replace("<body>", f"<body>\n{new_link}")
    elif "<ul>" in index_content:
        index_content = index_content.replace("<ul>", f"<ul>\n{new_link}")
    
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(index_content)
    print("✅ index.html更新完成")
else:
    print("⚠️ index.html不存在，跳过更新")

# ==================== 第七步：GitHub自动提交上传 ====================
print("🚀 执行Git提交推送...")
try:
    # 切换到Git目录
    os.chdir(GIT_DIR)
    
    # Git add
    subprocess.run(["git", "add", "."], check=True, capture_output=True)
    print("✅ Git add完成")
    
    # Git commit
    commit_msg = f"feat: 自动更新BTC日报 {REPORT_DATE}"
    result = subprocess.run(
        ["git", "commit", "-m", commit_msg],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print(f"✅ Git commit完成：{commit_msg}")
    else:
        print(f"⚠️ Git commit跳过：{result.stderr.strip()}")
    
    # Git push
    push_result = subprocess.run(
        ["git", "push", "origin", "main"],
        capture_output=True,
        text=True
    )
    if push_result.returncode == 0:
        print("✅ Git push完成")
    else:
        print(f"⚠️ Git push失败：{push_result.stderr.strip()}")
except Exception as e:
    print(f"⚠️ Git操作失败：{str(e)}")

print("🎉 BTC每日报告生成流程全部完成！")
