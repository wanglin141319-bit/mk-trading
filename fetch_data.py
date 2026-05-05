import sys
sys.path.insert(0, r'C:\Users\asus\.workbuddy\binaries\python\envs\default\Lib\site-packages')

import requests

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

# 1. BTC/ETH Price
r1 = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_24hr_change=true', timeout=15)
print('PRICE:', r1.json())

# 2. BTC Funding Rate
r2 = requests.get('https://fapi.binance.com/fapi/v1/premiumIndex/BTCUSDT', timeout=15)
d2 = r2.json()
print('FR:', d2.get('lastFundingRate'), 'Mark:', d2.get('markPrice'))

# 3. BTC OI
r3 = requests.get('https://fapi.binance.com/fapi/v1/openInterest/BTCUSDT', timeout=15)
d3 = r3.json()
print('OI:', d3)

# 4. Fear & Greed
r4 = requests.get('https://api.alternative.me/fng/?limit=2', headers=headers, timeout=15)
print('FG:', r4.json())

# 5. Long/Short Ratio
r5 = requests.get('https://fapi.binance.com/futures/data/globalLongShortAccountRatio?symbol=BTCUSDT&period=8h&limit=3', timeout=15)
print('LS:', r5.json()[-1] if r5.json() else 'empty')

# 6. BTC OHLC for indicators
r6 = requests.get('https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1d&limit=60', timeout=15)
klines = r6.json()
closes = [float(k[4]) for k in klines]
highs = [float(k[2]) for k in klines]
lows = [float(k[3]) for k in klines]
print('CLOSE:', closes[-3:])

# RSI
def calc_rsi(prices, period=14):
    deltas = [prices[i] - prices[i-1] for i in range(1, len(prices))]
    gains = [d if d > 0 else 0 for d in deltas]
    losses = [-d if d < 0 else 0 for d in deltas]
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    if avg_loss == 0:
        return 100
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

rsi = calc_rsi(closes)
print('RSI14:', round(rsi, 1))

# EMA
def ema(prices, n):
    k = 2 / (n + 1)
    ema_val = prices[0]
    for p in prices[1:]:
        ema_val = p * k + ema_val * (1 - k)
    return ema_val

ema7 = ema(closes, 7)
ema20 = ema(closes, 20)
ema50 = ema(closes, 50)
print('EMA7:', round(ema7, 2))
print('EMA20:', round(ema20, 2))
print('EMA50:', round(ema50, 2))

# MACD (12, 26, 9)
ema12 = ema(closes, 12)
ema26 = ema(closes, 26)
macd_line = ema12 - ema26
# Signal = EMA of MACD line (use last 9 close prices as proxy)
macd_vals = [closes[i] * (2/13) - closes[i] * (2/27) for i in range(26, len(closes))]
signal = ema(macd_vals, 9) if len(macd_vals) >= 9 else 0
hist = macd_line - signal
print('MACD:', round(macd_line, 2), 'Signal:', round(signal, 2), 'Hist:', round(hist, 2))

# Bollinger Bands
import statistics
recent = closes[-20:]
mid = statistics.mean(recent)
std = statistics.stdev(recent)
bb_upper = mid + 2 * std
bb_lower = mid - 2 * std
print('BB Upper:', round(bb_upper, 2), 'Mid:', round(mid, 2), 'Lower:', round(bb_lower, 2))
