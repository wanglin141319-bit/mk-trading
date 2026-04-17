import warnings, sys, os
warnings.filterwarnings('ignore')
sys.path.insert(0, 'C:/Users/asus/mk-trading/btc')
import requests
from fetch_btc_data import retry_fetch

TOKEN = '8626387493:AAE2XCzMzmhDiWRaGKVEjrj2EGLPsDN22-Q'
CHAT_ID = '-1003189007280'

def log(msg, tag='INFO'):
    print(f'[{tag}] {msg}')

# ========== SOL 数据采集 ==========
log('Fetching SOL data...')

def get_sol_price():
    r = requests.get(
        'https://api.binance.com/api/v3/ticker/24hr?symbol=SOLUSDT',
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

def get_sol_funding():
    r = requests.get(
        'https://fapi.binance.com/fapi/v1/premiumIndex?symbol=SOLUSDT',
        timeout=8, verify=False,
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    d = r.json()
    return {
        'rate': float(d['lastFundingRate']) * 100,
        'mark_price': float(d['markPrice']),
        'index_price': float(d['indexPrice']),
        'source': 'binance'
    }

def get_sol_ls_ratio():
    r = requests.get(
        'https://fapi.binance.com/futures/data/globalLongShortAccountRatio?symbol=SOLUSDT&period=1h&limit=1',
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

def get_sol_technical():
    # CoinGecko OHLC for SOL (7 days)
    r = requests.get(
        'https://api.coingecko.com/api/v3/coins/solana/ohlc?vs_currency=usd&days=7',
        timeout=8,
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    ohlc = r.json()
    if not ohlc:
        return None

    closes = [c[4] for c in ohlc]
    highs = [c[2] for c in ohlc]
    lows = [c[3] for c in ohlc]
    n = len(closes)

    # RSI 14
    gains = [max(closes[i] - closes[i-1], 0) for i in range(1, n)]
    losses = [max(closes[i-1] - closes[i], 0) for i in range(1, n)]
    avg_gain = sum(gains[-14:]) / 14 if len(gains) >= 14 else sum(gains) / max(len(gains), 1)
    avg_loss = sum(losses[-14:]) / 14 if len(losses) >= 14 else sum(losses) / max(len(losses), 1)
    rs = avg_gain / avg_loss if avg_loss != 0 else 100
    rsi = 100 - (100 / (1 + rs))

    # EMA 12/26
    ema12 = sum(closes[-12:]) / 12 if len(closes) >= 12 else sum(closes) / n
    ema26 = sum(closes[-26:]) / 26 if len(closes) >= 26 else sum(closes) / n
    macd_line = ema12 - ema26
    signal_line = macd_line * 0.8
    macd_hist = macd_line - signal_line
    macd_cross = 'GOLDEN' if macd_hist > 0 else 'DEAD'

    # EMA 20
    ema20 = sum(closes[-20:]) / min(20, n) if n >= 20 else sum(closes) / n

    # Bollinger Bands 20
    period = min(20, n)
    recent = closes[-period:]
    sma = sum(recent) / period
    std = (sum((x - sma) ** 2 for x in recent) / period) ** 0.5
    bb_upper = sma + 2 * std
    bb_lower = sma - 2 * std

    # 支撑/阻力
    resistance = max(highs)
    support = min(lows)

    return {
        'rsi': round(rsi, 1),
        'macd_cross': macd_cross,
        'macd_hist': round(macd_hist, 4),
        'ema20': round(ema20, 0),
        'bb_upper': round(bb_upper, 0),
        'bb_lower': round(bb_lower, 0),
        'resistance': round(resistance, 0),
        'support': round(support, 0),
        'close': closes[-1],
        'candles': len(closes),
        'source': 'coingecko_ohlc'
    }

def get_sol_sentiment():
    r = requests.get('https://api.alternative.me/fng/', timeout=8)
    d = r.json()
    fg_val = int(d['data'][0]['value'])
    fg_class = d['data'][0]['value_classification']
    return {'fear_greed': fg_val, 'classification': fg_class}

# ========== 采集 ==========
sol_price = retry_fetch(get_sol_price)
log('SOL price <- ' + sol_price['source'] + ': $' + str(round(sol_price['price'], 2)))

sol_funding = retry_fetch(get_sol_funding)
log('SOL funding <- ' + sol_funding['source'] + ': ' + str(round(sol_funding['rate'], 4)) + '%')

sol_ls = retry_fetch(get_sol_ls_ratio)
log('SOL L/S <- ' + sol_ls['source'] + ': long=' + str(sol_ls['long_ratio']) + '% / short=' + str(sol_ls['short_ratio']) + '%')

sol_tech = retry_fetch(get_sol_technical)
log('SOL tech <- ' + sol_tech['source'] + ': RSI=' + str(sol_tech['rsi']) + ', MACD=' + sol_tech['macd_cross'])

sol_sentiment = retry_fetch(get_sol_sentiment)
log('SOL sentiment <- fear_greed: ' + str(sol_sentiment['fear_greed']))

# ========== 提取数据 ==========
price = sol_price['price']
change = sol_price['change_24h']
rsi = sol_tech['rsi']
macd = sol_tech['macd_cross']
funding_rate = sol_funding['rate']
ls_ratio = sol_ls['long_short_ratio']
long_ratio = sol_ls['long_ratio']
short_ratio = sol_ls['short_ratio']
fear = sol_sentiment['fear_greed']
fear_class = sol_sentiment['classification']
ema20 = sol_tech['ema20']
bb_upper = sol_tech['bb_upper']
bb_lower = sol_tech['bb_lower']
resistance = sol_tech['resistance']
support = sol_tech['support']

# ========== 策略计算 ==========
# SOL 特调参数（波动更大，阈值适当放宽）
if rsi < 38 and macd == 'GOLDEN':
    signal = 'LONG'
    sl = round(price * 0.94, 0)
    tp1 = round(price * 1.04, 0)
    tp2 = round(price * 1.08, 0)
    conf = 'High'
    reason = 'RSI超卖 + MACD金叉共振'
elif rsi > 70 and macd == 'DEAD':
    signal = 'SHORT'
    sl = round(price * 1.06, 0)
    tp1 = round(price * 0.96, 0)
    tp2 = round(price * 0.92, 0)
    conf = 'High'
    reason = 'RSI超买 + MACD死叉共振'
elif rsi < 48:
    signal = 'LONG (试探)'
    sl = round(price * 0.93, 0)
    tp1 = round(price * 1.03, 0)
    tp2 = round(price * 1.06, 0)
    conf = 'Medium'
    reason = 'RSI偏低，低吸机会'
elif rsi > 60:
    signal = 'SHORT (试探)'
    sl = round(price * 1.05, 0)
    tp1 = round(price * 0.97, 0)
    tp2 = round(price * 0.94, 0)
    conf = 'Medium'
    reason = 'RSI偏高，注意回调风险'
else:
    signal = 'NEUTRAL'
    sl = tp1 = tp2 = 'N/A'
    conf = 'Low'
    reason = 'RSI中性，方向不明'

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
    '\U0001F4E3 *SOL 行情播报*\n'
    '━━━━━━━━━━━━━━━━━━━━\n\n'
    + change_icon + ' *SOL $' + f'{price:,.0f}' + '*  (' + ('+' if change >= 0 else '') + f'{change:.2f}%)\n'
    '\u2B07 Low 24h: $' + f'{sol_price["low_24h"]:,.0f}' + ' | \u2B06 High 24h: $' + f'{sol_price["high_24h"]:,.0f}' + '\n\n'
    '\U0001F525 RSI: *' + str(rsi) + '* | MACD: *' + macd + '*\n'
    '\U0001F9F9 Fear&Greed: *' + str(fear) + '* (' + fear_class + ')\n'
    '\U0001F4B0 Funding: *' + f'{funding_rate:.4f}' + '%*\n\n'
    '\U0001F4CA 多空清算比：\n'
    '  Long: *' + str(long_ratio) + '%* | Short: *' + str(short_ratio) + '%*\n'
    '  L/S Ratio: *' + str(ls_ratio) + '*\n\n'
    '\U0001F4C8 EMA20: ' + fmt(ema20) + '\n'
    '\U0001F536 Bollinger: ' + fmt(bb_lower) + ' - ' + fmt(bb_upper) + '\n'
    '\u26A0 Support: ' + fmt(support) + ' | Resistance: ' + fmt(resistance) + '\n\n'
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
