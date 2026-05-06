#!/usr/bin/env python3
"""Fetch all BTC market data for daily report - robust version"""
import requests, json, time, sys

headers = {'User-Agent':'Mozilla/5.0'}
data = {}

# ===== 1. BTC Price from Binance =====
print('=== Fetching BTC Price (Binance) ===')
try:
    r = requests.get('https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT', timeout=10)
    d = r.json()
    data['btc_price'] = float(d['lastPrice'])
    data['btc_change_24h'] = float(d['priceChangePercent'])
    data['btc_high_24h'] = float(d['highPrice'])
    data['btc_low_24h'] = float(d['lowPrice'])
    data['btc_volume_24h'] = float(d['quoteVolume'])
    print(f"BTC: ${data['btc_price']:,.0f} | 24h: {data['btc_change_24h']:+.2f}%")
except Exception as e:
    print(f'Binance BTC error: {e}')
    sys.exit(1)

# ===== 2. ETH Price =====
print('=== Fetching ETH Price ===')
try:
    r = requests.get('https://api.binance.com/api/v3/ticker/24hr?symbol=ETHUSDT', timeout=10)
    d = r.json()
    data['eth_price'] = float(d['lastPrice'])
    data['eth_change_24h'] = float(d['priceChangePercent'])
    print(f"ETH: ${data['eth_price']:,.0f} | 24h: {data['eth_change_24h']:+.2f}%")
except Exception as e:
    print(f'ETH error: {e}')
    data['eth_price'] = 0
    data['eth_change_24h'] = 0

# ===== 3. SOL Price =====
print('=== Fetching SOL Price ===')
try:
    r = requests.get('https://api.binance.com/api/v3/ticker/24hr?symbol=SOLUSDT', timeout=10)
    d = r.json()
    data['sol_price'] = float(d['lastPrice'])
    data['sol_change_24h'] = float(d['priceChangePercent'])
    print(f"SOL: ${data['sol_price']:,.2f} | 24h: {data['sol_change_24h']:+.2f}%")
except Exception as e:
    print(f'SOL error: {e}')
    data['sol_price'] = 0
    data['sol_change_24h'] = 0

# ===== 4. Fear & Greed Index =====
print('=== Fetching Fear & Greed ===')
try:
    r = requests.get('https://api.alternative.me/fng/?limit=1', headers=headers, timeout=10)
    fng = r.json()['data'][0]
    data['fng_value'] = int(fng['value'])
    data['fng_class'] = fng['value_classification']
    print(f"FnG: {data['fng_value']} ({data['fng_class']})")
except Exception as e:
    print(f'FnG error: {e}')
    data['fng_value'] = 50
    data['fng_class'] = 'Neutral'

# ===== 5. Funding Rate =====
print('=== Fetching Funding Rate ===')
try:
    r = requests.get('https://fapi.binance.com/fapi/v1/fundingRate?symbol=BTCUSDT&limit=1', timeout=10)
    data['fr_btc'] = float(r.json()[0]['fundingRate']) * 100
    print(f"BTC FR: {data['fr_btc']:+.4f}%")
except Exception as e:
    print(f'BTC FR error: {e}')
    data['fr_btc'] = 0.01

try:
    r = requests.get('https://fapi.binance.com/fapi/v1/fundingRate?symbol=ETHUSDT&limit=1', timeout=10)
    data['fr_eth'] = float(r.json()[0]['fundingRate']) * 100
    print(f"ETH FR: {data['fr_eth']:+.4f}%")
except Exception as e:
    print(f'ETH FR error: {e}')
    data['fr_eth'] = 0.01

# ===== 6. Open Interest =====
print('=== Fetching OI ===')
try:
    r = requests.get('https://fapi.binance.com/fapi/v1/openInterest?symbol=BTCUSDT', timeout=10)
    data['oi_btc'] = float(r.json()['openInterest'])
    data['oi_usd'] = data['oi_btc'] * data['btc_price']
    print(f"OI: {data['oi_btc']:,.0f} BTC (~${data['oi_usd']/1e9:.2f}B)")
except Exception as e:
    print(f'OI error: {e}')
    data['oi_btc'] = 0
    data['oi_usd'] = 0

# ===== 7. Long/Short Ratio =====
print('=== Fetching Long/Short Ratio ===')
try:
    r = requests.get('https://fapi.binance.com/futures/data/globalLongShortAccountRatio?symbol=BTCUSDT&period=5m&limit=1', timeout=10)
    ls_data = r.json()[0]
    data['long_pct'] = float(ls_data['longAccount']) * 100
    data['short_pct'] = float(ls_data['shortAccount']) * 100
    data['ls_ratio'] = float(ls_data['longShortRatio'])
    print(f"Long: {data['long_pct']:.1f}% | Short: {data['short_pct']:.1f}% | Ratio: {data['ls_ratio']:.2f}")
except Exception as e:
    print(f'LS Ratio error: {e}')
    data['long_pct'] = 50
    data['short_pct'] = 50
    data['ls_ratio'] = 1.0

# ===== 8. Klines for Technical Indicators =====
print('=== Fetching Klines ===')
closes = []
try:
    # Get 100 daily klines
    r = requests.get('https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1d&limit=100', timeout=15)
    klines = r.json()
    closes = [float(k[4]) for k in klines]
    print(f'Klines data points: {len(closes)}, last close: ${closes[-1]:,.0f}')
except Exception as e:
    print(f'Klines error: {e}')
    # Fallback to CoinGecko OHLC
    try:
        r = requests.get('https://api.coingecko.com/api/v3/coins/bitcoin/ohlc?vs_currency=usd&days=365', headers=headers, timeout=15)
        ohlc = r.json()
        closes = [float(c[4]) for c in ohlc]
        print(f'CoinGecko OHLC fallback: {len(closes)} points')
    except Exception as e2:
        print(f'All OHLC failed: {e2}')

# ===== 9. Technical Indicators =====
def calc_ema(data_list, period):
    if len(data_list) < period:
        return None
    multiplier = 2 / (period + 1)
    ema = sum(data_list[:period]) / period
    for price in data_list[period:]:
        ema = (price - ema) * multiplier + ema
    return ema

def calc_rsi(data_list, period=14):
    if len(data_list) < period + 1:
        return None
    gains, losses = [], []
    for i in range(1, len(data_list)):
        change = data_list[i] - data_list[i-1]
        gains.append(max(0, change))
        losses.append(max(0, -change))
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period
    if avg_loss == 0:
        return 100
    for i in range(period, len(gains)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period
    rs = avg_gain / avg_loss if avg_loss != 0 else 999
    return 100 - (100 / (1 + rs))

def calc_macd(data_list, fast=12, slow=26, signal=9):
    ema_fast = calc_ema(data_list, fast)
    ema_slow = calc_ema(data_list, slow)
    if ema_fast is None or ema_slow is None:
        return None, None, None
    macd_line = ema_fast - ema_slow
    # Calculate MACD series for signal line
    if len(data_list) >= slow + signal:
        macd_vals = []
        for i in range(slow, len(data_list)):
            ef = calc_ema(data_list[:i+1], fast)
            es = calc_ema(data_list[:i+1], slow)
            if ef is not None and es is not None:
                macd_vals.append(ef - es)
        if len(macd_vals) >= signal:
            signal_line = sum(macd_vals[-signal:]) / signal
        else:
            signal_line = macd_line * 0.8
    else:
        signal_line = macd_line * 0.8
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram

def calc_bollinger(data_list, period=20, std_dev=2):
    if len(data_list) < period:
        return None, None, None
    recent = data_list[-period:]
    sma = sum(recent) / period
    variance = sum((x - sma) ** 2 for x in recent) / period
    std = variance ** 0.5
    upper = sma + std_dev * std
    lower = sma - std_dev * std
    return upper, sma, lower

if closes:
    data['rsi'] = calc_rsi(closes) or 50
    data['ema7'] = calc_ema(closes, 7) or closes[-1]
    data['ema20'] = calc_ema(closes, 20) or closes[-1]
    data['ema50'] = calc_ema(closes, 50) or closes[-1]
    ml, ms, mh = calc_macd(closes)
    data['macd_line'] = ml or 0
    data['macd_signal'] = ms or 0
    data['macd_hist'] = mh or 0
    bu, bm, bl = calc_bollinger(closes)
    data['bb_upper'] = bu or closes[-1] * 1.03
    data['bb_mid'] = bm or closes[-1]
    data['bb_lower'] = bl or closes[-1] * 0.97
    data['closes_last'] = closes[-30:]
    
    print(f"RSI(14): {data['rsi']:.1f}")
    print(f"EMA7: ${data['ema7']:,.0f} | EMA20: ${data['ema20']:,.0f} | EMA50: ${data['ema50']:,.0f}")
    print(f"MACD: {data['macd_line']:.0f} | Signal: {data['macd_signal']:.0f} | Hist: {data['macd_hist']:.0f}")
    print(f"BB: ${data['bb_upper']:,.0f} / ${data['bb_mid']:,.0f} / ${data['bb_lower']:,.0f}")
else:
    data['rsi'] = 50
    data['ema7'] = data['btc_price']
    data['ema20'] = data['btc_price']
    data['ema50'] = data['btc_price']
    data['macd_line'] = 0
    data['macd_signal'] = 0
    data['macd_hist'] = 0
    data['bb_upper'] = data['btc_price'] * 1.03
    data['bb_mid'] = data['btc_price']
    data['bb_lower'] = data['btc_price'] * 0.97
    data['closes_last'] = []
    print('No OHLC data, using defaults')

# ===== Save =====
data['btc_market_cap'] = data.get('btc_market_cap', data['btc_price'] * 19700000)
data['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S')

with open('c:/Users/asus/mk-trading/btc/_api_data_20260506.json', 'w') as f:
    json.dump(data, f, indent=2, default=str)
print('=== All data saved ===')
