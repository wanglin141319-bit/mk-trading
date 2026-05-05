import requests
import statistics

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

results = {}

# 1. Funding rate alternative - try CoinGecko
try:
    r = requests.get('https://api.coingecko.com/api/v3/coins/bitcoin?localization=false&tickers=true&community_data=false&developer_data=false', timeout=15)
    d = r.json()
    tickers = d.get('tickers', [])
    for t in tickers:
        if 'Binance' in t.get('market', {}).get('name', '') and 'perpetual' in str(t):
            results['binance_perp'] = {'base': t.get('base'), 'target': t.get('target'), 'last': t.get('last'), 'funding_rate': t.get('funding_rate')}
            break
except Exception as e:
    results['cg_error'] = str(e)

# 2. Try Bybit for funding rate
try:
    r2 = requests.get('https://api.bybit.com/v5/market/tickers?category=linear&symbol=BTCUSDT', timeout=15)
    d2 = r2.json()
    if d2.get('retCode') == 0:
        item = d2.get('result', {}).get('list', [{}])[0]
        results['bybit'] = {
            'funding_rate': item.get('fundingRate'),
            'mark_price': item.get('markPrice'),
            'last_price': item.get('lastPrice'),
            'open_interest': item.get('openInterest'),
            '24h_volume': item.get('volume24h'),
        }
except Exception as e:
    results['bybit_error'] = str(e)

# 3. Try Bybit long short ratio
try:
    r3 = requests.get('https://api.bybit.com/v5/market/long-short-ratio?category=linear&symbol=BTCUSDT&period=8h&limit=3', timeout=15)
    d3 = r3.json()
    if d3.get('retCode') == 0:
        results['bybit_ls'] = d3.get('result', {}).get('list', [])
except Exception as e:
    results['bybit_ls_error'] = str(e)

# 4. CoinGecko funding rate
try:
    cg = requests.get('https://api.coingecko.com/api/v3/coins/bitcoin/contract_detail?contract_address=0x0000000000000000000000000000000000000000', timeout=15)
    results['cg_detail'] = cg.json()[:2] if cg.text else None
except:
    pass

# 5. Try Binance funding rate with /futures/data/
try:
    r4 = requests.get('https://fapi.binance.com/futures/data/fundingRate?symbol=BTCUSDT&limit=3', timeout=15)
    results['fr2_status'] = r4.status_code
    results['fr2_text'] = r4.text[:200]
except Exception as e:
    results['fr2_error'] = str(e)

# 6. CoinGecko global data
try:
    cg2 = requests.get('https://api.coingecko.com/api/v3/global', timeout=15)
    g = cg2.json().get('data', {})
    results['global'] = {
        'btc_dominance': g.get('market_cap_percentage', {}).get('btc'),
        'total_mcap': g.get('total_market_cap', {}).get('usd'),
        'volume_24h': g.get('total_volume', {}).get('usd'),
    }
except Exception as e:
    results['global_error'] = str(e)

# 7. Liquidation data (CoinGecko market data)
try:
    cg3 = requests.get('https://api.coingecko.com/api/v3/coins/bitcoin?localization=false&market_data=true&community_data=false&developer_data=false', timeout=15)
    mkt = cg3.json().get('market_data', {})
    results['market_data'] = {
        'total_volume': mkt.get('total_volume', {}).get('usd'),
        'market_cap': mkt.get('market_cap', {}).get('usd'),
        'ath_change': mkt.get('ath_change_percentage', {}).get('usd'),
    }
except Exception as e:
    results['mkt_error'] = str(e)

print(results)
