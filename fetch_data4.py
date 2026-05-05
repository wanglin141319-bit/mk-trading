import requests
import statistics

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

results = {}

# 1. CoinGecko BTC market data with all details
try:
    cg = requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=bitcoin&order=market_cap_desc&sparkline=false&price_change_percentage=24h,7d,30d', timeout=15)
    d = cg.json()
    if d:
        item = d[0]
        results['markets'] = {
            'price': item.get('current_price'),
            'change_24h': item.get('price_change_percentage_24h'),
            'change_7d': item.get('price_change_percentage_7d_in_currency'),
            'change_30d': item.get('price_change_percentage_30d_in_currency'),
            'high_24h': item.get('high_24h'),
            'low_24h': item.get('low_24h'),
            'volume_24h': item.get('total_volume'),
            'mcap': item.get('market_cap'),
            'ath': item.get('ath'),
            'ath_change_pct': item.get('ath_change_percentage'),
        }
except Exception as e:
    results['markets_error'] = str(e)

# 2. Bybit liquidation data (try)
try:
    r = requests.get('https://api.bybit.com/v5/market/liquidation?category=linear&symbol=BTCUSDT&startTime=0&limit=1', timeout=15)
    results['liq_status'] = r.status_code
    results['liq_text'] = r.text[:300]
except Exception as e:
    results['liq_error'] = str(e)

# 3. Whale alert / glassnode alternative - CoinGecko global data
try:
    cg2 = requests.get('https://api.coingecko.com/api/v3/global', timeout=15)
    g = cg2.json().get('data', {})
    results['global'] = {
        'btc_dominance': g.get('market_cap_percentage', {}).get('btc'),
        'total_mcap': g.get('total_market_cap', {}).get('usd'),
        'volume_24h': g.get('total_volume', {}).get('usd'),
        'active_crypto': g.get('active_cryptocurrencies'),
    }
except Exception as e:
    results['global_error'] = str(e)

# 4. Binance alternative - try public API with different host
try:
    r4 = requests.get('https://data-api.binance.vision/api/v3/klines?symbol=BTCUSDT&interval=1d&limit=30', timeout=15)
    results['binance_vision_status'] = r4.status_code
    if r4.status_code == 200:
        klines = r4.json()
        closes = [float(k[4]) for k in klines]
        results['vision_closes'] = closes[-5:]
except Exception as e:
    results['bv_error'] = str(e)

# 5. Try alternative liquidation API
try:
    r5 = requests.get('https://api.alternative.me/v2/tickers/?limit=5', timeout=15)
    results['alt_tickers'] = r5.json()
except Exception as e:
    results['alt_tickers_error'] = str(e)

# 6. Check CoinGecko OHLC for current day (for today's data)
try:
    cg3 = requests.get('https://api.coingecko.com/api/v3/coins/bitcoin/ohlc?vs_currency=usd&days=1', timeout=15)
    results['ohlc_today'] = cg3.json()
except Exception as e:
    results['ohlc_error'] = str(e)

print(results)
