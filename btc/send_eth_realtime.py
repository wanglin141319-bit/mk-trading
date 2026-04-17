import warnings, json, os, sys
warnings.filterwarnings('ignore')
sys.path.insert(0, 'C:/Users/asus/mk-trading/btc')
import requests
from fetch_btc_data import retry_fetch

TOKEN = '8626387493:AAE2XCzMzmhDiWRaGKVEjrj2EGLPsDN22-Q'
CHAT_ID = '-1003189007280'

def log(msg, tag='INFO'):
    print(f'[{tag}] {msg}')

# ========== ETH 数据采集 ==========
log('Fetching ETH data...')

# 1. ETH 价格
def get_eth_price():
    r = requests.get(
        'https://api.binance.com/api/v3/ticker/24hr?symbol=ETHUSDT',
        timeout=8, verify=False,
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    d = r.json()
    return {
        'price': float(d['lastPrice']),
        'change_24h': float(d['priceChangePercent']),
        'high_24h': float(d['highPrice']),
        'low_24h': float(d['lowPrice']),
        'volume': float(d['quoteVolume']),
        'source': 'binance'
    }

# 2. ETH 资金费率
def get_eth_funding():
    r = requests.get(
        'https://fapi.binance.com/fapi/v1/premiumIndex?symbol=ETHUSDT',
        timeout=8, verify=False,
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    d = r.json()
    return {
        'rate': float(d['lastFundingRate']) * 100,
        'next_funding': d.get('nextFundingTime', 'N/A'),
        'mark_price': float(d['markPrice']),
        'index_price': float(d['indexPrice']),
        'source': 'binance'
    }

# 3. ETH 多空比
def get_eth_ls_ratio():
    r = requests.get(
        'https://fapi.binance.com/futures/data/globalLongShortAccountRatio?symbol=ETHUSDT&period=1h&limit=1',
        timeout=8, verify=False,
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    d = r.json()
    latest = d[-1]
    return {
        'long_ratio': round(float(latest['longAccount']) * 100, 1),
        'short_ratio': round(float(latest['shortAccount']) * 100, 1),
        'long_short_ratio': round(float(latest['longShortRatio']), 3),
        'source': 'binance'
    }

# 4. ETH 技术指标（从 CoinGecko K线计算）
def get_eth_technical():
    r = requests.get(
        'https://api.coingecko.com/api/v3/coins/ethereum/ohlc?vs_currency=usd&days=7',
        timeout=8,
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    ohlc = r.json()  # [timestamp, open, high, low, close]
    if not ohlc:
        return None

    closes = [c[4] for c in ohlc]
    highs = [c[2] for c in ohlc]
    lows = [c[3] for c in ohlc]

    n = len(closes)
    # RSI (14)
    gains = [max(closes[i] - closes[i-1], 0) for i in range(1, n)]
    losses = [max(closes[i-1] - closes[i], 0) for i in range(1, n)]
    avg_gain = sum(gains[-14:]) / 14 if len(gains) >= 14 else sum(gains) / max(len(gains), 1)
    avg_loss = sum(losses[-14:]) / 14 if len(losses) >= 14 else sum(losses) / max(len(losses), 1)
    rs = avg_gain / avg_loss if avg_loss != 0 else 100
    rsi = 100 - (100 / (1 + rs))

    # EMA
    ema12 = sum(closes[-12:]) / 12 if len(closes) >= 12 else sum(closes) / n
    ema26 = sum(closes[-26:]) / 26 if len(closes) >= 26 else sum(closes) / n
    macd_line = ema12 - ema26
    signal_line = macd_line * 0.8  # 简化 signal
    macd_hist = macd_line - signal_line

    # 布林带（20周期）
    period = min(20, n)
    recent = closes[-period:]
    sma = sum(recent) / period
    std = (sum((x - sma) ** 2 for x in recent) / period) ** 0.5
    bb_upper = sma + 2 * std
    bb_lower = sma - 2 * std

    # MACD 方向
    if macd_hist > 0:
        macd_cross = 'GOLDEN'
    else:
        macd_cross = 'DEAD'

    return {
        'rsi': round(rsi, 1),
        'macd_cross': macd_cross,
        'macd_hist': round(macd_hist, 4),
        'ema20': round(sum(closes[-20:]) / min(20, n) if n >= 20 else sma, 0),
        'bb_upper': round(bb_upper, 0),
        'bb_lower': round(bb_lower, 0),
        'close': closes[-1],
        'source': 'coingecko_ohlc'
    }

# 5. ETH 恐惧贪婪（用 BTC 指数近似，用 ETH/BTC 相关性调整）
def get_eth_sentiment():
    r = requests.get('https://api.alternative.me/fng/', timeout=8)
    d = r.json()
    fg_val = int(d['data'][0]['value'])
    fg_class = d['data'][0]['value_classification']
    return {'fear_greed': fg_val, 'classification': fg_class}

# ========== 采集 ==========
eth_price = retry_fetch(get_eth_price)
log('ETH price <- ' + eth_price['source'] + ': $' + str(round(eth_price['price'], 2)))

eth_funding = retry_fetch(get_eth_funding)
log('ETH funding <- ' + eth_funding['source'] + ': ' + str(round(eth_funding['rate'], 4)) + '%')

eth_ls = retry_fetch(get_eth_ls_ratio)
log('ETH L/S <- ' + eth_ls['source'] + ': long=' + str(eth_ls['long_ratio']) + '% / short=' + str(eth_ls['short_ratio']) + '%')

eth_tech = retry_fetch(get_eth_technical)
if eth_tech:
    log('ETH tech <- ' + eth_tech['source'] + ': RSI=' + str(eth_tech['rsi']) + ', MACD=' + eth_tech['macd_cross'])

eth_sentiment = retry_fetch(get_eth_sentiment)
log('ETH sentiment <- fear_greed: ' + str(eth_sentiment['fear_greed']))

# ========== 策略计算 ==========
price = eth_price['price']
change = eth_price['change_24h']
rsi = eth_tech['rsi']
macd = eth_tech['macd_cross']
funding_rate = eth_funding['rate']
ls_ratio = eth_ls['long_short_ratio']
long_ratio = eth_ls['long_ratio']
short_ratio = eth_ls['short_ratio']
fear = eth_sentiment['fear_greed']
fear_class = eth_sentiment['classification']
ema20 = eth_tech['ema20']
bb_upper = eth_tech['bb_upper']
bb_lower = eth_tech['bb_lower']
close = eth_tech['close']

# 策略
if rsi < 35 and macd == 'GOLDEN':
    signal = 'LONG'
    sl = round(price * 0.96, 0)
    tp1 = round(price * 1.03, 0)
    tp2 = round(price * 1.06, 0)
    conf = 'High'
    reason = 'RSI超卖 + MACD金叉共振'
elif rsi > 68 and macd == 'DEAD':
    signal = 'SHORT'
    sl = round(price * 1.04, 0)
    tp1 = round(price * 0.97, 0)
    tp2 = round(price * 0.94, 0)
    conf = 'High'
    reason = 'RSI超买 + MACD死叉共振'
elif rsi < 45:
    signal = 'LONG (试探)'
    sl = round(price * 0.95, 0)
    tp1 = round(price * 1.025, 0)
    tp2 = round(price * 1.05, 0)
    conf = 'Medium'
    reason = 'RSI偏低，低吸机会'
elif rsi > 58:
    signal = 'SHORT (试探)'
    sl = round(price * 1.03, 0)
    tp1 = round(price * 0.975, 0)
    tp2 = round(price * 0.95, 0)
    conf = 'Medium'
    reason = 'RSI偏高，注意回调风险'
else:
    signal = 'NEUTRAL'
    sl = tp1 = tp2 = 'N/A'
    conf = 'Low'
    reason = 'RSI中性，方向不明'

# 图标
dir_icon = {
    'LONG': '\U0001F4C8', 'SHORT': '\U0001F4C9',
    'LONG (试探)': '\U0001F4C8', 'SHORT (试探)': '\U0001F4C9',
    'NEUTRAL': '\U0001F6D1'
}.get(signal, '\u2796')
if '试探' in signal:
    dir_icon = '\U0001F53A'

change_icon = '\u2B06\uFE0F' if change >= 0 else '\u2B07\uFE0F'

def fmt(v):
    return f'${v:,.0f}' if isinstance(v, (int, float)) else v

# ========== 格式化消息 ==========
msg = (
    '\U0001F4E3 *ETH 行情播报*\n'
    '━━━━━━━━━━━━━━━━━━━━\n\n'
    + change_icon + ' *ETH $' + f'{price:,.0f}' + '*  (' + ('+' if change >= 0 else '') + f'{change:.2f}%)\n'
    '\u2B07 Low 24h: $' + f'{eth_price["low_24h"]:,.0f}' + ' | \u2B06 High 24h: $' + f'{eth_price["high_24h"]:,.0f}' + '\n\n'
    '\U0001F525 RSI: *' + str(rsi) + '* | MACD: *' + macd + '*\n'
    '\U0001F9F9 Fear&Greed: *' + str(fear) + '* (' + fear_class + ')\n'
    '\U0001F4B0 Funding: *' + f'{funding_rate:.4f}' + '%*\n\n'
    '\U0001F4CA 多空清算比：\n'
    '  Long: *' + str(long_ratio) + '%* | Short: *' + str(short_ratio) + '%*\n'
    '  L/S Ratio: *' + str(ls_ratio) + '*\n\n'
    '\U0001F4C8 EMA20: ' + fmt(ema20) + '\n'
    '\U0001F536 Bollinger: ' + fmt(bb_lower) + ' - ' + fmt(bb_upper) + '\n\n'
    '\U0001F3AF *今日策略:* ' + dir_icon + ' *' + signal + '* (' + conf + ')\n'
    '  ' + reason + '\n'
)
if sl != 'N/A':
    rr = (tp1 - price) / (price - sl) if signal.startswith('LONG') else (price - tp1) / (sl - price)
    msg += '  Entry: *$' + f'{price:,.0f}' + '*\n'
    msg += '  SL: ' + fmt(sl) + ' | TP1: ' + fmt(tp1) + ' | TP2: ' + fmt(tp2) + '\n'
    msg += '  RR: *' + f'{abs(rr):.1f}' + ':1*\n'

msg += '\n\U0001F6A8 *完整日报:* https://mktrading.vip/btc/\n'
msg += '━━━━━━━━━━━━━━━━━━━━\n'
msg += '\U0001F19A *MK Trading Bot v2.0*'

# ========== 发送到 Telegram ==========
r = requests.post(
    'https://api.telegram.org/bot' + TOKEN + '/sendMessage',
    json={'chat_id': CHAT_ID, 'text': msg, 'parse_mode': 'Markdown'},
    timeout=10
)
d = r.json()
log('Send result: ' + str(d.get('ok')) + ' | msg_id=' + str(d['result']['message_id'] if d.get('ok') else 'ERROR'), 'TG')
