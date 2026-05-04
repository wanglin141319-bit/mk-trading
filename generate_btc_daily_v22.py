#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BTC每日报告自动生成脚本 v2.2
执行流程：数据抓取 → 指标计算 → 策略生成 → HTML生成 → 文件保存 → 索引更新 → Git推送
符合规范：16板块全覆盖 + 硬性标准标签 + 深色主题
"""
import urllib.request
import json
import math
import datetime
import os
import sys
import subprocess
import threading

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
    if isinstance(num, float):
        return f"{num:,.{precision}f}"
    return f"{num:,}"

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
    "include_24hr_vol=true"
)
if btc_price_data:
    data["btc_price"] = btc_price_data["bitcoin"]["usd"]
    data["btc_24h_change"] = btc_price_data["bitcoin"]["usd_24h_change"]
    data["btc_24h_vol"] = btc_price_data["bitcoin"].get("usd_24h_vol", 0)
else:
    data["btc_price"] = 65000.0
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

# 6. 24h爆仓量（使用正确的API）
try:
    liqs = fetch_url("https://fapi.binance.com/futures/data/takerlongshortRatio?symbol=BTCUSDT&period=1d&limit=1")
    data["long_short_ratio_24h"] = float(liqs[0]["longShortRatio"]) if liqs and len(liqs) > 0 else None
except:
    data["long_short_ratio_24h"] = None

data["total_liq"] = None  # 需要CoinGlass API，暂时留空
data["long_liq"] = None
data["short_liq"] = None

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
data["month_be"] = data["month_trades"] - data["month_wins"] - data["month_losses"]

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
print("📝 生成HTML报告（v2.2完整版）...")

# 颜色辅助函数
def price_color(change):
    return "#4caf50" if change >= 0 else "#f44336"

def rsi_color(rsi):
    if rsi is None:
        return "#ff9800"
    if rsi > 70:
        return "#f44336"
    if rsi < 30:
        return "#4caf50"
    return "#ff9800"

def fng_color(value):
    if value is None:
        return "#ff9800"
    if value < 50:
        return "#4caf50"
    if value > 70:
        return "#f44336"
    return "#ff9800"

# HTML模板 - 完整16板块
html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BTC每日交易报告 {REPORT_DATE_FORMAT}</title>
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
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
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
        
        /* HARD TAG */
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
        
        /* CONTAINER */
        .container {{ max-width: 1280px; margin: 0 auto; padding: 28px 40px; }}
        .grid2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px; }}
        .grid3 {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px; margin-bottom: 16px; }}
        .grid4 {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 16px; }}
        .full {{ margin-bottom: 16px; }}
        
        /* CARD */
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
        
        /* METRIC */
        .metric {{ display: flex; flex-direction: column; gap: 4px; }}
        .metric-label {{ font-size: 11px; color: var(--muted); text-transform: uppercase; letter-spacing: 1px; }}
        .metric-val {{ font-size: 24px; font-weight: 700; color: #fff; }}
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
        
        /* SECTION TITLE */
        .section-title {{
            font-size: 16px;
            font-weight: 700;
            color: #fff;
            margin: 30px 0 14px 0;
            display: flex;
            align-items: center;
            gap: 10px;