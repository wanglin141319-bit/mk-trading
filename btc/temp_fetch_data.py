#!/usr/bin/env python3
import requests
import json

# 获取Binance数据
print("=== Binance Data ===")

# 1. 资金费率
try:
    url = 'https://fapi.binance.com/fapi/v1/premiumIndex?symbol=BTCUSDT'
    r = requests.get(url, timeout=30)
    data = r.json()
    print(f"markPrice: {data.get('markPrice', 'N/A')}")
    print(f"lastFundingRate: {data.get('lastFundingRate', 'N/A')}")
except Exception as e:
    print(f"Funding error: {e}")

# 2. OI数据
try:
    url = 'https://fapi.binance.com/fapi/v1/openInterest?symbol=BTCUSDT'
    r = requests.get(url, timeout=30)
    data = r.json()
    print(f"openInterest: {data.get('openInterest', 'N/A')}")
except Exception as e:
    print(f"OI error: {e}")

# 3. 24h ticker
try:
    url = 'https://fapi.binance.com/fapi/v1/ticker/24hr?symbol=BTCUSDT'
    r = requests.get(url, timeout=30)
    data = r.json()
    print(f"highPrice: {data.get('highPrice', 'N/A')}")
    print(f"lowPrice: {data.get('lowPrice', 'N/A')}")
    print(f"volume: {data.get('volume', 'N/A')}")
    print(f"priceChangePercent: {data.get('priceChangePercent', 'N/A')}")
except Exception as e:
    print(f"24h error: {e}")

# 4. ETH资金费率
try:
    url = 'https://fapi.binance.com/fapi/v1/premiumIndex?symbol=ETHUSDT'
    r = requests.get(url, timeout=30)
    data = r.json()
    print(f"ethFundingRate: {data.get('lastFundingRate', 'N/A')}")
except Exception as e:
    print(f"ETH funding error: {e}")

# 5. 技术指标计算
print("\n=== Technical Indicators ===")
try:
    url = 'https://fapi.binance.com/fapi/v1/klines?symbol=BTCUSDT&interval=1d&limit=100'
    r = requests.get(url, timeout=30)
    data = r.json()
    closes = [float(k[4]) for k in data]
    
    # RSI
    def calculate_rsi(prices, period=14):
        deltas = [prices[i] - prices[i-1] for i in range(1, len(prices))]
        gains = [d if d > 0 else 0 for d in deltas]
        losses = [-d if d < 0 else 0 for d in deltas]
        avg_gain = sum(gains[:period]) / period
        avg_loss = sum(losses[:period]) / period
        for i in range(period, len(gains)):
            avg_gain = (avg_gain * (period-1) + gains[i]) / period
            avg_loss = (avg_loss * (period-1) + losses[i]) / period
        rs = avg_gain / avg_loss if avg_loss != 0 else 0
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    rsi = calculate_rsi(closes)
    print(f"RSI14: {rsi:.1f}")
    
    # EMA
    def calculate_ema(prices, period):
        multiplier = 2 / (period + 1)
        ema = prices[0]
        for price in prices[1:]:
            ema = (price - ema) * multiplier + ema
        return ema
    
    print(f"EMA7: {calculate_ema(closes, 7):.2f}")
    print(f"EMA20: {calculate_ema(closes, 20):.2f}")
    print(f"EMA50: {calculate_ema(closes, 50):.2f}")
    
    # 布林带
    import statistics
    period = 20
    recent = closes[-period:]
    sma = sum(recent) / period
    std = statistics.stdev(recent)
    print(f"BB_middle: {sma:.2f}")
    print(f"BB_upper: {sma + 2*std:.2f}")
    print(f"BB_lower: {sma - 2*std:.2f}")
    
    # MACD
    def calculate_ema_list(prices, period):
        multiplier = 2 / (period + 1)
        ema_list = [prices[0]]
        for price in prices[1:]:
            ema = (price - ema_list[-1]) * multiplier + ema_list[-1]
            ema_list.append(ema)
        return ema_list
    
    ema12 = calculate_ema_list(closes, 12)
    ema26 = calculate_ema_list(closes, 26)
    macd_line = [ema12[i] - ema26[i] for i in range(len(ema12))]
    signal_line = calculate_ema_list(macd_line, 9)
    histogram = [macd_line[i] - signal_line[i] for i in range(len(macd_line))]
    print(f"MACD: {macd_line[-1]:.2f}")
    print(f"Signal: {signal_line[-1]:.2f}")
    print(f"Histogram: {histogram[-1]:.2f}")
    
except Exception as e:
    print(f"Indicators error: {e}")

# 6. 多空持仓比
try:
    url = 'https://fapi.binance.com/fapi/v1/openInterestStatistics?symbol=BTCUSDT&period=5m&limit=1'
    r = requests.get(url, timeout=30)
    data = r.json()
    if data:
        print(f"longShortRatio: {data[0].get('longShortRatio', 'N/A')}")
except Exception as e:
    print(f"LS ratio error: {e}")
