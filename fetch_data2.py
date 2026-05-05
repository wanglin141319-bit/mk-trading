import requests
import statistics

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

results = {}

# 1. BTC/ETH Price
try:
    r1 = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_24hr_change=true', timeout=15)
    results['price'] = r1.json()
except Exception as e:
    results['price'] = str(e)

# 2. BTC Funding Rate (try alternative endpoint)
try:
    r2 = requests.get('https://fapi.binance.com/fapi/v1/premiumIndex/BTCUSDT', timeout=15)
    results['fr_status'] = r2.status_code
    results['fr_text'] = r2.text[:200]
    if r2.text.strip():
        d2 = r2.json()
        results['funding_rate'] = d2.get('lastFundingRate')
        results['mark_price'] = d2.get('markPrice')
except Exception as e:
    results['fr_error'] = str(e)

# 3. OI
try:
    r3 = requests.get('https://fapi.binance.com/fapi/v1/openInterest/BTCUSDT', timeout=15)
    results['oi_status'] = r3.status_code
    results['oi_text'] = r3.text[:200]
except Exception as e:
    results['oi_error'] = str(e)

# 4. Fear & Greed
try:
    r4 = requests.get('https://api.alternative.me/fng/?limit=2', headers=headers, timeout=15)
    results['fg'] = r4.json()
except Exception as e:
    results['fg_error'] = str(e)

# 5. Long/Short Ratio
try:
    r5 = requests.get('https://fapi.binance.com/futures/data/globalLongShortAccountRatio?symbol=BTCUSDT&period=8h&limit=3', timeout=15)
    results['ls_status'] = r5.status_code
    results['ls_text'] = r5.text[:200]
except Exception as e:
    results['ls_error'] = str(e)

# 6. BTC OHLC
try:
    r6 = requests.get('https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1d&limit=60', timeout=15)
    results['kline_status'] = r6.status_code
    results['kline_text'] = r6.text[:200]
    if r6.text.strip():
        klines = r6.json()
        closes = [float(k[4]) for k in klines]
        results['closes'] = closes[-3:]
        
        # RSI
        def calc_rsi(prices, period=14):
            deltas = [prices[i] - prices[i-1] for i in range(1, len(prices))]
            gains = [d if d > 0 else 0 for d in deltas]
            losses = [-d if d < 0 else 0 for d in deltas]
            avg_gain = sum(gains[-period:]) / period
            avg_loss = sum(losses[-period:]) / period
            if avg_loss == 0:
                return 100
            return 100 - (100 / (1 + avg_gain/avg_loss))
        
        def ema(prices, n):
            k = 2/(n+1)
            e = prices[0]
            for p in prices[1:]:
                e = p*k + e*(1-k)
            return e
        
        results['rsi14'] = round(calc_rsi(closes), 1)
        results['ema7'] = round(ema(closes, 7), 2)
        results['ema20'] = round(ema(closes, 20), 2)
        results['ema50'] = round(ema(closes, 50), 2)
        
        # MACD
        e12 = ema(closes, 12)
        e26 = ema(closes, 26)
        macd = e12 - e26
        # proxy signal: EMA of closes price diff over 9 periods
        macd_series = [closes[i]*2/13 - closes[i]*2/27 for i in range(26, len(closes))]
        signal = ema(macd_series, 9)
        results['macd'] = round(macd, 2)
        results['macd_signal'] = round(signal, 2)
        results['macd_hist'] = round(macd - signal, 2)
        
        # Bollinger
        recent = closes[-20:]
        mid = statistics.mean(recent)
        std = statistics.stdev(recent)
        results['bb_upper'] = round(mid + 2*std, 2)
        results['bb_mid'] = round(mid, 2)
        results['bb_lower'] = round(mid - 2*std, 2)
except Exception as e:
    results['kline_error'] = str(e)

print(results)
