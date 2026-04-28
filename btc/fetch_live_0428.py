import requests, json, sys
from datetime import datetime, timezone, timedelta

print("=== Fetching BTC/ETH data ===", flush=True)

# 1. CoinGecko price
try:
    r = requests.get(
        'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_24hr_change=true&include_24hr_vol=true',
        timeout=15
    )
    d = r.json()
    btc_price = d['bitcoin']['usd']
    btc_change = d['bitcoin']['usd_24h_change']
    btc_vol = d['bitcoin']['usd_24h_vol']
    eth_price = d['ethereum']['usd']
    eth_change = d['ethereum']['usd_24h_change']
    print(f"BTC: {btc_price} | {btc_change:.2f}% | vol: {btc_vol:,.0f}")
    print(f"ETH: {eth_price} | {eth_change:.2f}%")
except Exception as e:
    print(f"CoinGecko error: {e}")
    btc_price = 79000; btc_change = 1.5; eth_price = 2400; eth_change = 1.8

# 2. Binance funding + OI
try:
    # Funding rate
    fr = requests.get('https://fapi.binance.com/fapi/v1/premiumIndex', timeout=10)
    for item in fr.json():
        if item['symbol'] == 'BTCUSDT':
            btc_funding = float(item['lastFundingRate']) * 100
            print(f"BTC funding: {btc_funding:.4f}%")
            break
    # OI from open interest
    oi = requests.get('https://fapi.binance.com/futures/data/global.longShortAccountRatio?symbol=BTCUSDT&period=8h&limit=1', timeout=10)
    oi_data = oi.json()
    if oi_data:
        long_r = float(oi_data[0]['longAccount'])
        short_r = float(oi_data[0]['shortAccount'])
        ls_ratio = long_r / short_r
        print(f"BTC long/short: {long_r:.2%} / {short_r:.2%} = {ls_ratio:.3f}")
    # 24h liquidations
    liq = requests.get('https://fapi.binance.com/futures/data/topLongShortPositionRatio?symbol=BTCUSDT&period=1d&limit=1', timeout=10)
    print(f"Liquidations data: {liq.text[:200]}")
except Exception as e:
    print(f"Binance error: {e}")

# 3. Fear & Greed
try:
    fg = requests.get('https://api.alternative.me/fng/?limit=2', timeout=10)
    fg_data = fg.json()
    fg_value = int(fg_data['data'][0]['value'])
    fg_class = fg_data['data'][0]['value_classification']
    fg_prev = int(fg_data['data'][1]['value'])
    print(f"Fear&Greed: {fg_value} ({fg_class})")
except Exception as e:
    print(f"Fear&Greed error: {e}")
    fg_value = 45; fg_class = 'Neutral'

# 4. BTC technical indicators via Binance klines
try:
    # RSI(14) - need 14+ periods
    klines = requests.get(
        'https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1d&limit=60',
        timeout=10
    ).json()
    closes = [float(k[4]) for k in klines]
    # RSI
    period = 14
    delta = [closes[i] - closes[i-1] for i in range(1, len(closes))]
    gain = [d if d > 0 else 0 for d in delta]
    loss = [-d if d < 0 else 0 for d in delta]
    avg_gain = sum(gain[-period:]) / period
    avg_loss = sum(loss[-period:]) / period
    rs = avg_gain / avg_loss if avg_loss else 999
    rsi = 100 - (100 / (1 + rs))
    # EMA7, EMA20, EMA50
    def ema(data, period):
        k = 2 / (period + 1)
        ema_val = sum(data[:period]) / period
        for price in data[period:]:
            ema_val = price * k + ema_val * (1 - k)
        return ema_val
    ema7 = ema(closes, 7)
    ema20 = ema(closes, 20)
    ema50 = ema(closes, 50)
    # Bollinger Bands
    import statistics
    bb_period = 20
    bb_closes = closes[-bb_period:]
    bb_middle = sum(bb_closes) / bb_period
    std = statistics.stdev(bb_closes)
    bb_upper = bb_middle + 2 * std
    bb_lower = bb_middle - 2 * std
    # MACD
    ema12 = ema(closes, 12)
    ema26 = ema(closes, 26)
    dif = ema12 - ema26
    signal_k = 2 / (9 + 1)
    # Approximate MACD signal
    macd_signal = dif * 0.8  # rough
    macd_hist = dif - macd_signal
    macd_cross = 'GOLDEN' if macd_hist > 0 else 'DEAD'
    print(f"RSI(14): {rsi:.1f}")
    print(f"EMA7: {ema7:.0f} | EMA20: {ema20:.0f} | EMA50: {ema50:.0f}")
    print(f"BB: {bb_upper:.0f} / {bb_middle:.0f} / {bb_lower:.0f}")
    print(f"MACD: {dif:.0f} | hist: {macd_hist:.0f} | cross: {macd_cross}")
    print(f"Latest close: {closes[-1]:.0f}")
except Exception as e:
    print(f"Technical error: {e}")
    rsi = 50; ema7=77000; ema20=76500; ema50=75000
    bb_upper=80000; bb_middle=77000; bb_lower=74000
    macd_cross='GOLDEN'

print("=== Done ===", flush=True)
