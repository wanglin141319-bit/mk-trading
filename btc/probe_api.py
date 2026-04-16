"""BTC Data API Probe - 测试可用数据源"""
import requests
import json
import sys
import traceback

requests.packages.urllib3.disable_warnings()

# ========== 1. Gate.io Spot ==========
def test_gate_spot():
    try:
        r = requests.get('https://api.gateio.ws/api/v4/spot/tickers?currency_pair=BTC_USDT', timeout=6)
        d = r.json()[0]
        print('GATE_SPOT: OK')
        print(f'  last={d["last"]}, base_vol={d["base_volume"]}, quote_vol={d["quote_volume"]}, change_24h={d.get("change_24h")}')
        return d
    except Exception as e:
        print(f'GATE_SPOT: FAIL {e}')
        return None

# ========== 2. Gate.io Futures ==========
def test_gate_futures():
    try:
        r = requests.get('https://api.gateio.ws/api/v4/futures/usdt/tickers?contract=BTC_USDT', timeout=6)
        d = r.json()[0]
        print('GATE_FUTURES: OK')
        print(f'  price={d.get("last")}, volume={d.get("volume")}, quote_volume={d.get("quote_volume")}')
        return d
    except Exception as e:
        print(f'GATE_FUTURES: FAIL {e}')
        return None

# ========== 3. Gate.io Funding Rate ==========
def test_gate_funding():
    try:
        r = requests.get('https://api.gateio.ws/api/v4/futures/usdt/contracts/BTC_USDT', timeout=6)
        d = r.json()
        print('GATE_FUNDING: OK')
        print(f'  funding_rate={d.get("funding_rate")}, funding_cap={d.get("funding_cap")}')
        return d
    except Exception as e:
        print(f'GATE_FUNDING: FAIL {e}')
        return None

# ========== 4. Bybit Spot ==========
def test_bybit_spot():
    try:
        r = requests.get('https://api.bybit.com/v5/market/tickers?category=spot&symbol=BTCUSDT', timeout=6)
        d = r.json()
        if d['retCode'] == 0:
            item = d['result']['list'][0]
            print('BYBIT_SPOT: OK')
            print(f'  last={item["lastPrice"]}, 24h_change={item["price24hPcnt"]}')
            return item
        print('BYBIT_SPOT: retCode != 0')
    except Exception as e:
        print(f'BYBIT_SPOT: FAIL {e}')
    return None

# ========== 5. Bybit Linear (USDT futures) ==========
def test_bybit_linear():
    try:
        r = requests.get('https://api.bybit.com/v5/market/tickers?category=linear&symbol=BTCUSDT', timeout=6)
        d = r.json()
        if d['retCode'] == 0:
            item = d['result']['list'][0]
            print('BYBIT_LINEAR: OK')
            print(f'  last={item["lastPrice"]}, 24h_change={item["price24hPcnt"]}, volume24h={item["volume24h"]}')
            return item
        print('BYBIT_LINEAR: retCode != 0')
    except Exception as e:
        print(f'BYBIT_LINEAR: FAIL {e}')
    return None

# ========== 6. Bybit Funding Rate ==========
def test_bybit_funding():
    try:
        r = requests.get('https://api.bybit.com/v5/market/tickers?category=linear&symbol=BTCUSDT', timeout=6)
        d = r.json()
        if d['retCode'] == 0:
            item = d['result']['list'][0]
            print('BYBIT_FUNDING: OK')
            print(f'  funding_rate={item.get("fundingRate")}, next_funding_time={item.get("nextFundingTime")}')
            return item
    except Exception as e:
        print(f'BYBIT_FUNDING: FAIL {e}')
    return None

# ========== 7. Bybit OI (open interest) ==========
def test_bybit_oi():
    try:
        r = requests.get('https://api.bybit.com/v5/market/open-interest?category=linear&symbol=BTCUSDT&intervalDay=1&limit=1', timeout=6)
        d = r.json()
        if d['retCode'] == 0:
            items = d['result']['list']
            print(f'BYBIT_OI: OK, {len(items)} records')
            if items:
                print(f'  latest OI: {items[0]}')
            return items
        print('BYBIT_OI: retCode != 0')
    except Exception as e:
        print(f'BYBIT_OI: FAIL {e}')
    return None

# ========== 8. Fear & Greed Index (alternative.me) ==========
def test_fear_greed():
    try:
        r = requests.get('https://api.alternative.me/fng/?limit=2', timeout=6)
        d = r.json()
        print('FEAR_GREED: OK')
        print(f'  data={json.dumps(d["data"], indent=2)}')
        return d
    except Exception as e:
        print(f'FEAR_GREED: FAIL {e}')
    return None

# ========== 9. Binance (try with verify=False) ==========
def test_binance():
    try:
        r = requests.get(
            'https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT',
            timeout=8,
            verify=False,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        d = r.json()
        print('BINANCE: OK')
        print(f'  last={d["lastPrice"]}, change={d["priceChangePercent"]}%, vol={d["volume"]}')
        return d
    except Exception as e:
        print(f'BINANCE: FAIL {type(e).__name__}: {str(e)[:80]}')
    return None

# ========== 10. Binance Funding Rate ==========
def test_binance_funding():
    try:
        r = requests.get(
            'https://fapi.binance.com/fapi/v1/premiumIndex?symbol=BTCUSDT',
            timeout=8,
            verify=False,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        d = r.json()
        print('BINANCE_FUNDING: OK')
        print(f'  funding_rate={d["lastFundingRate"]}, next_funding={d["nextFundingTime"]}')
        return d
    except Exception as e:
        print(f'BINANCE_FUNDING: FAIL {type(e).__name__}: {str(e)[:80]}')
    return None

# ========== 11. Binance OI ==========
def test_binance_oi():
    try:
        r = requests.get(
            'https://fapi.binance.com/futures/data/globalLongShortAccountRatio?symbol=BTCUSDT&period=1h&limit=1',
            timeout=8,
            verify=False,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        d = r.json()
        print('BINANCE_OI: OK')
        print(f'  data={json.dumps(d[:1], indent=2)}')
        return d
    except Exception as e:
        print(f'BINANCE_OI: FAIL {type(e).__name__}: {str(e)[:80]}')
    return None

# ========== 12. CoinGecko (with verify=False) ==========
def test_coingecko():
    try:
        r = requests.get(
            'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_24hr_change=true&include_24hr_vol=true',
            timeout=8,
            verify=False,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        d = r.json()
        print('COINGECKO: OK')
        btc = d['bitcoin']
        print(f'  usd={btc["usd"]}, change_24h={btc["usd_24h_change"]:.2f}%, vol={btc.get("usd_24h_vol")}')
        return d
    except Exception as e:
        print(f'COINGECKO: FAIL {type(e).__name__}: {str(e)[:80]}')
    return None

# ========== 13. OKX Spot + Funding ==========
def test_okx():
    try:
        r = requests.get('https://www.okx.com/api/v5/market/ticker?instId=BTC-USDT', timeout=6)
        d = r.json()
        if d['code'] == '0':
            item = d['data'][0]
            print('OKX_SPOT: OK')
            print(f'  last={item["last"]}, 24h_change={item["last"]}')
    except Exception as e:
        print(f'OKX: FAIL {e}')
    try:
        r2 = requests.get('https://www.okx.com/api/v5/market/funding-rate?instId=BTC-USD-SWAP', timeout=6)
        d2 = r2.json()
        if d2['code'] == '0':
            item = d2['data'][0]
            print('OKX_FUNDING: OK')
            print(f'  funding_rate={item["fundingRate"]}, next_funding={item["nextFundingTime"]}')
    except Exception as e:
        print(f'OKX_FUNDING: FAIL {e}')
    try:
        r3 = requests.get('https://www.okx.com/api/v5/market/open-interest?instId=BTC-USD-SWAP', timeout=6)
        d3 = r3.json()
        if d3['code'] == '0':
            item = d3['data'][0]
            print('OKX_OI: OK')
            print(f'  oi={item["oi"]}, oi_currency={item["oiCurrency"]}')
    except Exception as e:
        print(f'OKX_OI: FAIL {e}')

# ========== 14. CoinGecko OHLC (for RSI/MACD/EMA) ==========
def test_coingecko_ohlc():
    try:
        r = requests.get(
            'https://api.coingecko.com/api/v3/coins/bitcoin/ohlc?vs_currency=usd&days=60',
            timeout=8,
            verify=False,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        d = r.json()
        print(f'COINGECKO_OHLC: OK, {len(d)} candles')
        if d:
            print(f'  last: {d[-1]}')
            print(f'  60d ago: {d[0]}')
        return d
    except Exception as e:
        print(f'COINGECKO_OHLC: FAIL {type(e).__name__}: {str(e)[:80]}')
    return None

if __name__ == '__main__':
    print('=== BTC API 可用性探测 ===')
    test_gate_spot()
    test_gate_futures()
    test_gate_funding()
    test_bybit_spot()
    test_bybit_linear()
    test_bybit_funding()
    test_bybit_oi()
    test_binance()
    test_binance_funding()
    test_binance_oi()
    test_coingecko()
    test_okx()
    test_fear_greed()
    test_coingecko_ohlc()
    print('=== 探测完毕 ===')
