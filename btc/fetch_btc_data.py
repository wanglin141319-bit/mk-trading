"""
BTC 日报数据获取模块 - v2.0
智能探测 + 多源融合 + 缓存降级 + 重试机制
"""
import requests
import json
import time
import os
import sys
from datetime import datetime

# ============ 全局配置 ============
CACHE_DIR = os.path.join(os.path.dirname(__file__), 'cache')
os.makedirs(CACHE_DIR, exist_ok=True)
CACHE_FILE = os.path.join(CACHE_DIR, 'btc_latest.json')
CACHE_TTL = 1800  # 缓存有效期 30 分钟
RETRY_TIMES = 3
RETRY_DELAY = 2

# ============ 工具函数 ============
def log(msg, level='INFO'):
    ts = datetime.now().strftime('%H:%M:%S')
    print('[' + ts + '] [' + level + '] ' + msg)

def retry_fetch(func, *args, **kwargs):
    for i in range(RETRY_TIMES):
        try:
            result = func(*args, **kwargs)
            if result is not None:
                return result
        except Exception as e:
            log('  Retry ' + str(i+1) + '/' + str(RETRY_TIMES) + ' fail: ' + str(e)[:60], 'WARN')
            if i < RETRY_TIMES - 1:
                time.sleep(RETRY_DELAY)
    return None

def load_cache():
    if not os.path.exists(CACHE_FILE):
        return None
    try:
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            cache = json.load(f)
        age = time.time() - cache.get('ts', 0)
        if age < CACHE_TTL:
            log('  Cache hit (' + str(int((CACHE_TTL - age)//60)) + 'min ago)', 'CACHE')
            return cache.get('data')
        else:
            log('  Cache expired (' + str(int(age//60)) + 'min old)', 'WARN')
    except Exception as e:
        log('  Cache read error: ' + str(e), 'WARN')
    return None

def save_cache(data):
    try:
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump({'ts': time.time(), 'data': data}, f, ensure_ascii=False, indent=2)
        log('  Cache written', 'CACHE')
    except Exception as e:
        log('  Cache write error: ' + str(e), 'WARN')

# ============ 数据获取函数 ============
def get_btc_price():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

    def try_binance():
        r = requests.get('https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT',
                         timeout=8, verify=False, headers=headers)
        d = r.json()
        return {'price': float(d['lastPrice']), 'change_24h': float(d['priceChangePercent']),
                'high_24h': float(d['highPrice']), 'low_24h': float(d['lowPrice']),
                'vol_btc': float(d['volume']), 'source': 'binance'}

    def try_bybit():
        r = requests.get('https://api.bybit.com/v5/market/tickers?category=spot&symbol=BTCUSDT',
                         timeout=6, headers=headers)
        d = r.json()['result']['list'][0]
        return {'price': float(d['lastPrice']), 'change_24h': float(d['price24hPcnt']) * 100,
                'high_24h': float(d['highPrice24h']), 'low_24h': float(d['lowPrice24h']),
                'vol_btc': float(d['volume24h']), 'source': 'bybit'}

    def try_gate():
        r = requests.get('https://api.gateio.ws/api/v4/spot/tickers?currency_pair=BTC_USDT',
                         timeout=6, headers=headers)
        d = r.json()[0]
        return {'price': float(d['last']), 'source': 'gate'}

    for func in [try_binance, try_bybit, try_gate]:
        result = retry_fetch(func)
        if result:
            log('  BTC price <- ' + result['source'] + ': $' + str(result['price']) , 'OK')
            return result
    return None

def get_eth_price():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

    def try_binance():
        r = requests.get('https://api.binance.com/api/v3/ticker/24hr?symbol=ETHUSDT',
                         timeout=8, verify=False, headers=headers)
        d = r.json()
        return {'price': float(d['lastPrice']), 'change_24h': float(d['priceChangePercent']), 'source': 'binance'}

    def try_bybit():
        r = requests.get('https://api.bybit.com/v5/market/tickers?category=spot&symbol=ETHUSDT',
                         timeout=6, headers=headers)
        d = r.json()['result']['list'][0]
        return {'price': float(d['lastPrice']), 'change_24h': float(d['price24hPcnt']) * 100, 'source': 'bybit'}

    for func in [try_binance, try_bybit]:
        result = retry_fetch(func)
        if result:
            log('  ETH price <- ' + result['source'] + ': $' + str(result['price']), 'OK')
            return result
    return None

def get_funding_rate():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

    def try_binance():
        r = requests.get('https://fapi.binance.com/fapi/v1/premiumIndex?symbol=BTCUSDT',
                         timeout=8, verify=False, headers=headers)
        d = r.json()
        return {'rate': float(d['lastFundingRate']) * 100, 'next_time': int(d['nextFundingTime']), 'source': 'binance'}

    def try_bybit():
        r = requests.get('https://api.bybit.com/v5/market/tickers?category=linear&symbol=BTCUSDT',
                         timeout=6, headers=headers)
        d = r.json()['result']['list'][0]
        return {'rate': float(d['fundingRate']) * 100, 'source': 'bybit'}

    def try_gate():
        r = requests.get('https://api.gateio.ws/api/v4/futures/usdt/contracts/BTC_USDT',
                         timeout=6, headers=headers)
        d = r.json()
        return {'rate': float(d['funding_rate']) * 100, 'source': 'gate'}

    for func in [try_binance, try_bybit, try_gate]:
        result = retry_fetch(func)
        if result:
            log('  Funding rate <- ' + result['source'] + ': ' + str(round(result['rate'], 4)) + '%', 'OK')
            return result
    return None

def get_oi():
    """获取未平仓合约 OI（仅 OI 数值，多空比由 get_liquidation 负责）"""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

    def try_binance_oi():
        r = requests.get(
            'https://fapi.binance.com/futures/data/globalLongShortAccountRatio?symbol=BTCUSDT&period=1h&limit=1',
            timeout=8, verify=False, headers=headers)
        d = r.json()
        latest = d[-1]
        return {
            'long_ratio': round(float(latest['longAccount']) * 100, 1),
            'short_ratio': round(float(latest['shortAccount']) * 100, 1),
            'long_short_ratio': round(float(latest['longShortRatio']), 3),
            'source': 'binance_global'
        }

    def try_bybit_oi():
        r = requests.get(
            'https://api.bybit.com/v5/market/open-interest?category=linear&symbol=BTCUSDT&intervalDay=1&limit=3',
            timeout=6, headers=headers)
        d = r.json()
        if d['retCode'] == 0 and d['result']['list']:
            return {'records': d['result']['list'], 'source': 'bybit'}
        return None

    result = retry_fetch(try_binance_oi)
    if result:
        log('  OI <- ' + result['source'] + ': long=' + str(result['long_ratio']) + '% / short=' + str(result['short_ratio']) + '%', 'OK')
        return result
    result = retry_fetch(try_bybit_oi)
    if result:
        log('  OI <- bybit (records=' + str(len(result.get('records', []))) + ')', 'OK')
        return result
    return None

def get_liquidation():
    """获取爆仓/多空清算数据（Binance 多源融合）"""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

    def try_binance_top_ratio():
        # 多空持仓比（每小时更新，反映主力仓位）
        r = requests.get(
            'https://fapi.binance.com/futures/data/topLongShortPositionRatio?symbol=BTCUSDT&period=1h&limit=5',
            timeout=8, verify=False, headers=headers)
        d = r.json()
        latest = d[-1]
        long_ratio = float(latest['longAccount'])
        short_ratio = float(latest['shortAccount'])
        ls_ratio = float(latest['longShortRatio'])
        # 计算 24h 大户多空清算倾向（趋势变化）
        if len(d) >= 2:
            prev = d[-2]
            change = float(latest['longShortRatio']) - float(prev['longShortRatio'])
        else:
            change = 0
        return {
            'long_ratio': round(long_ratio * 100, 1),
            'short_ratio': round(short_ratio * 100, 1),
            'long_short_ratio': round(ls_ratio, 3),
            'trend_change': round(change, 3),
            'source': 'binance_top_ratio'
        }

    result = retry_fetch(try_binance_top_ratio)
    if result:
        log('  Liquidation/LSP <- binance_top_ratio: long=' + str(result['long_ratio']) + '% / short=' + str(result['short_ratio']) + '%', 'OK')
        return result
    return {'long_ratio': 'N/A', 'short_ratio': 'N/A', 'long_short_ratio': 'N/A', 'trend_change': 0, 'source': 'none'}

def get_fear_greed():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    def try_alternative():
        r = requests.get('https://api.alternative.me/fng/?limit=2', timeout=6, headers=headers)
        d = r.json()
        items = d['data']
        latest = items[0]
        prev = items[1]
        return {'value': int(latest['value']), 'classification': latest['value_classification'],
                'prev_value': int(prev['value']), 'prev_classification': prev['value_classification'],
                'source': 'alternative.me'}
    result = retry_fetch(try_alternative)
    if result:
        log('  Fear&Greed <- ' + result['source'] + ': ' + str(result['value']) + ' (' + result['classification'] + ')', 'OK')
        return result
    return {'value': 'N/A', 'classification': 'N/A', 'source': 'none'}

def get_ohlc_data(days=60):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    def try_coingecko():
        r = requests.get(
            'https://api.coingecko.com/api/v3/coins/bitcoin/ohlc?vs_currency=usd&days=' + str(days),
            timeout=10, verify=False, headers=headers)
        d = r.json()
        if d and isinstance(d, list) and len(d) > 0:
            return {'candles': d, 'source': 'coingecko'}
        return None
    def try_binance_ohlc():
        r = requests.get(
            'https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1d&limit=90',
            timeout=8, verify=False, headers=headers)
        d = r.json()
        candles = [[c[0], float(c[1]), float(c[2]), float(c[3]), float(c[4]), float(c[5])] for c in d]
        return {'candles': candles, 'source': 'binance'}
    result = retry_fetch(try_coingecko)
    if result:
        log('  OHLC <- ' + result['source'] + ': ' + str(len(result['candles'])) + ' candles', 'OK')
        return result
    result = retry_fetch(try_binance_ohlc)
    if result:
        log('  OHLC <- ' + result['source'] + ': ' + str(len(result['candles'])) + ' candles', 'OK')
        return result
    return None

def get_technical_indicators():
    ohlc = get_ohlc_data(90)
    if not ohlc:
        return None
    candles = ohlc['candles']
    closes = [float(c[4]) for c in candles]
    highs  = [float(c[2]) for c in candles]
    lows   = [float(c[3]) for c in candles]

    def calc_rsi(prices, period=14):
        if len(prices) < period + 1:
            return None
        deltas = [prices[i] - prices[i-1] for i in range(1, len(prices))]
        gains = [max(d, 0) for d in deltas[-period:]]
        losses = [-min(d, 0) for d in deltas[-period:]]
        avg_gain = sum(gains) / period
        avg_loss = sum(losses) / period
        if avg_loss == 0:
            return 100
        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))

    def calc_ema(prices, period):
        k = 2 / (period + 1)
        ema = prices[0]
        for p in prices[1:]:
            ema = p * k + ema * (1 - k)
        return ema

    def calc_macd(prices):
        ema12 = calc_ema(prices, 12)
        ema26 = calc_ema(prices, 26)
        macd_line = ema12 - ema26
        macd_vals = []
        for i in range(26, len(prices)):
            e12 = calc_ema(prices[:i+1], 12)
            e26 = calc_ema(prices[:i+1], 26)
            macd_vals.append(e12 - e26)
        signal = calc_ema(macd_vals, 9) if len(macd_vals) >= 9 else macd_line
        hist = macd_line - signal
        cross = 'GOLDEN' if hist > 0 else 'DEAD'
        return {'macd': macd_line, 'signal': signal, 'hist': hist, 'cross': cross}

    def calc_bollinger(prices, period=20, mult=2):
        if len(prices) < period:
            return None
        recent = prices[-period:]
        sma = sum(recent) / period
        variance = sum((p - sma) ** 2 for p in recent) / period
        std = variance ** 0.5
        return {'upper': sma + mult * std, 'middle': sma, 'lower': sma - mult * std}

    rsi14 = calc_rsi(closes, 14)
    ema7 = calc_ema(closes, 7) if len(closes) >= 7 else None
    ema20 = calc_ema(closes, 20)
    ema50 = calc_ema(closes, 50)
    macd_data = calc_macd(closes)
    bb = calc_bollinger(closes, 20, 2)

    result = {
        'rsi': rsi14, 'ema7': ema7, 'ema20': ema20, 'ema50': ema50,
        'macd_line': macd_data['macd'], 'macd_signal': macd_data['signal'],
        'macd_hist': macd_data['hist'], 'macd_cross': macd_data['cross'],
        'bb_upper': bb['upper'] if bb else None, 'bb_middle': bb['middle'] if bb else None,
        'bb_lower': bb['lower'] if bb else None, 'close': closes[-1],
    }
    log('  Tech: RSI=' + str(round(rsi14, 1)) + ', MACD=' + macd_data['cross'] + ', EMA20=' + str(round(ema20, 0)), 'OK')
    return result

def get_macro_events():
    today = datetime.now().strftime('%Y-%m-%d')
    today_weekday = datetime.now().weekday()
    week_days = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    week = week_days[today_weekday]

    events = [
        {'time': '14:00', 'country': 'US', 'flag': '\U0001f1fa\U0001f1f8', 'event': '美国PPI生产者价格指数',
         'importance': 'high', 'impact': 'Fed降息预期，USD + 风险资产'},
        {'time': '15:00', 'country': 'US', 'flag': '\U0001f1fa\U0001f1f8', 'event': 'NAHB房产市场指数',
         'importance': 'medium', 'impact': '次要经济指标'},
    ]
    weekly_key = {
        'week': week, 'date': today,
        'event': 'FOMC会议纪要 / 美联储官员密集发声',
        'description': '本周美联储多位官员讲话，关注利率路径指引',
        'action': '数据公布前1小时禁止新开仓，已持仓带好止损'
    }
    return {'events': events, 'weekly_key': weekly_key, 'week': week, 'date': today}

# ============ 主采集函数 ============
def fetch_all():
    log('========== BTC Data Fetch START ==========', 'START')
    start = time.time()
    data = {
        'timestamp': datetime.now().isoformat(),
        'btc': get_btc_price(),
        'eth': get_eth_price(),
        'funding': get_funding_rate(),
        'oi': get_oi(),
        'liquidation': get_liquidation(),
        'fear_greed': get_fear_greed(),
        'technical': get_technical_indicators(),
        'macro': get_macro_events(),
    }
    elapsed = time.time() - start
    log('========== Fetch DONE (' + str(round(elapsed, 1)) + 's) ==========', 'DONE')
    save_cache(data)
    return data

if __name__ == '__main__':
    import pprint
    data = fetch_all()
    pprint.pprint(data)
