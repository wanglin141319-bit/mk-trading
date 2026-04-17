import warnings, sys, os
warnings.filterwarnings('ignore')
sys.path.insert(0, 'C:/Users/asus/mk-trading/btc')
import requests
from fetch_btc_data import retry_fetch

TOKEN = '8626387493:AAE2XCzMzmhDiWRaGKVEjrj2EGLPsDN22-Q'
CHAT_ID = '-1003189007280'

def log(msg, tag='INFO'):
    print(f'[{tag}] {msg}')

log('Fetching RAVE data...')

# ========== 1. RAVE 基础数据 ==========
def get_rave_info():
    r = requests.get(
        'https://api.coingecko.com/api/v3/coins/ravedao?localization=false&tickers=false&market_data=true&community_data=false&developer_data=false&sparkline=false',
        timeout=12
    )
    d = r.json()
    md = d['market_data']
    price = md['current_price']['usd']
    return {
        'name': d['name'],
        'symbol': d['symbol'].upper(),
        'price': price,
        'change_1h': md.get('price_change_percentage_1h_in_currency', {}).get('usd', 0) or 0,
        'change_24h': md.get('price_change_percentage_24h', 0) or 0,
        'change_7d': md.get('price_change_percentage_7d', 0) or 0,
        'high_24h': md['high_24h']['usd'],
        'low_24h': md['low_24h']['usd'],
        'market_cap': md['market_cap']['usd'],
        'vol_24h': md['total_volume']['usd'],
        'ath': md['ath']['usd'],
        'ath_change': md['ath_change_percentage']['usd'],
        'atl': md['atl']['usd'],
        'atl_change': md['atl_change_percentage']['usd'],
        'circ_supply': md['circulating_supply'],
        'total_supply': md.get('total_supply', 0) or 0,
        'fdv': md['fully_diluted_valuation']['usd'],
        'source': 'coingecko'
    }

# ========== 2. RAVE 技术指标 ==========
def get_rave_technical():
    r = requests.get(
        'https://api.coingecko.com/api/v3/coins/ravedao/ohlc?vs_currency=usd&days=30',
        timeout=10
    )
    ohlc = r.json()
    if not ohlc:
        return None
    closes = [c[4] for c in ohlc]
    highs = [c[2] for c in ohlc]
    lows = [c[3] for c in ohlc]
    n = len(closes)

    # RSI 14
    gains = [max(closes[i]-closes[i-1], 0) for i in range(1, n)]
    losses = [max(closes[i-1]-closes[i], 0) for i in range(1, n)]
    avg_gain = sum(gains[-14:]) / 14 if len(gains) >= 14 else sum(gains) / max(len(gains), 1)
    avg_loss = sum(losses[-14:]) / 14 if len(losses) >= 14 else sum(losses) / max(len(losses), 1)
    rs = avg_gain / avg_loss if avg_loss != 0 else 100
    rsi = 100 - (100 / (1 + rs))

    # EMA 12/26
    ema12 = sum(closes[-12:]) / 12 if n >= 12 else sum(closes) / n
    ema26 = sum(closes[-26:]) / 26 if n >= 26 else sum(closes) / n
    macd_line = ema12 - ema26
    signal_line = macd_line * 0.8
    macd_hist = macd_line - signal_line
    macd_cross = 'GOLDEN' if macd_hist > 0 else 'DEAD'

    # EMA 20
    ema20 = sum(closes[-20:]) / min(20, n) if n >= 20 else sum(closes) / n

    # BB 20
    period = min(20, n)
    recent = closes[-period:]
    sma = sum(recent) / period
    std = (sum((x - sma)**2 for x in recent) / period) ** 0.5
    bb_upper = sma + 2*std
    bb_mid = sma
    bb_lower = sma - 2*std

    return {
        'rsi': round(rsi, 1),
        'macd_cross': macd_cross,
        'macd_hist': round(macd_hist, 4),
        'ema12': round(ema12, 2),
        'ema20': round(ema20, 2),
        'ema26': round(ema26, 2),
        'bb_upper': round(bb_upper, 2),
        'bb_mid': round(bb_mid, 2),
        'bb_lower': round(bb_lower, 2),
        'close': round(closes[-1], 4),
        'support': round(min(lows[-7:]), 2),
        'resistance': round(max(highs[-7:]), 2),
        'candles': n,
        'source': 'coingecko_ohlc'
    }

# ========== 采集 ==========
rave_info = retry_fetch(get_rave_info)
log('RAVE info <- ' + rave_info['source'] + ': $' + str(rave_info['price']))

rave_tech = retry_fetch(get_rave_technical)
log('RAVE tech <- ' + rave_tech['source'] + ': RSI=' + str(rave_tech['rsi']) + ', MACD=' + rave_tech['macd_cross'])

# ========== 提取数据 ==========
name = rave_info['name']
symbol = rave_info['symbol']
price = rave_info['price']
change1h = rave_info['change_1h']
change24h = rave_info['change_24h']
change7d = rave_info['change_7d']
high24h = rave_info['high_24h']
low24h = rave_info['low_24h']
mc = rave_info['market_cap']
vol24h = rave_info['vol_24h']
ath = rave_info['ath']
ath_change = rave_info['ath_change']
atl = rave_info['atl']
atl_change = rave_info['atl_change']
circ_supply = rave_info['circ_supply']
total_supply = rave_info['total_supply']
fdv = rave_info['fdv']

rsi = rave_tech['rsi']
macd = rave_tech['macd_cross']
ema12 = rave_tech['ema12']
ema20 = rave_tech['ema20']
ema26 = rave_tech['ema26']
bb_upper = rave_tech['bb_upper']
bb_mid = rave_tech['bb_mid']
bb_lower = rave_tech['bb_lower']
support = rave_tech['support']
resistance = rave_tech['resistance']

# ========== 策略分析 ==========
# RAVE 特高波动参数
# RSI 偏高区域（>65超买，>55偏高）
# BB 位置判断
price_vs_bb = 'above_upper' if price > bb_upper else ('above_mid' if price > bb_mid else ('below_mid' if price > bb_lower else 'below_lower'))

if rsi > 75 and macd == 'DEAD':
    signal = 'SHORT'
    sl = round(price * 1.10, 4)
    tp1 = round(price * 0.92, 4)
    tp2 = round(price * 0.85, 4)
    conf = 'High'
    reason = 'RSI极度超买 + MACD死叉，风险极高'
elif rsi > 68 and macd == 'DEAD':
    signal = 'SHORT'
    sl = round(price * 1.08, 4)
    tp1 = round(price * 0.90, 4)
    tp2 = round(price * 0.82, 4)
    conf = 'High'
    reason = 'RSI超买 + MACD死叉，注意回调'
elif rsi > 65 and macd == 'GOLDEN':
    signal = 'SHORT (止盈)'
    sl = round(price * 0.95, 4)
    tp1 = round(price * 0.93, 4)
    tp2 = round(price * 0.88, 4)
    conf = 'Medium'
    reason = 'MACD金叉但RSI过高，上涨动能衰减'
elif rsi < 38 and macd == 'GOLDEN':
    signal = 'LONG (抄底)'
    sl = round(price * 0.88, 4)
    tp1 = round(price * 1.08, 4)
    tp2 = round(price * 1.15, 4)
    conf = 'High'
    reason = 'RSI超卖 + MACD金叉共振'
elif rsi < 45:
    signal = 'LONG (试探)'
    sl = round(price * 0.90, 4)
    tp1 = round(price * 1.06, 4)
    tp2 = round(price * 1.12, 4)
    conf = 'Medium'
    reason = 'RSI偏低，低吸机会'
elif rsi > 60:
    signal = 'NEUTRAL (持币)'
    sl = round(price * 0.93, 4)
    tp1 = round(price * 1.05, 4)
    tp2 = 'N/A'
    conf = 'Low'
    reason = 'RSI偏高，方向不明'
else:
    signal = 'NEUTRAL'
    sl = tp1 = tp2 = 'N/A'
    conf = 'Low'
    reason = 'RSI中性，等待方向确认'

# 风险提示
vol_ratio = vol24h / mc if mc > 0 else 0
mcap_ratio = mc / fdv if fdv > 0 else 1

# 图标
dir_icon = {
    'LONG (抄底)': '\U0001F4C8', 'SHORT': '\U0001F4C9',
    'LONG (试探)': '\U0001F4C8', 'SHORT (止盈)': '\U0001F4C9',
    'NEUTRAL (持币)': '\U0001F6D1', 'NEUTRAL': '\U0001F6D1'
}.get(signal, '\u2796')

change_icon_24h = '\u2B06\uFE0F' if change24h >= 0 else '\u2B07\uFE0F'

def fmt(v):
    if isinstance(v, float):
        if v >= 1000:
            return f'${v:,.0f}'
        elif v >= 1:
            return f'${v:.2f}'
        else:
            return f'${v:.4f}'
    return str(v)

# ========== 格式化消息 ==========
msg = (
    '\U0001F525 *RAVE 代币深度分析*\n'
    '━━━━━━━━━━━━━━━━━━━━\n\n'
    '\U0001F916 *' + name + '* (' + symbol + ') 代币分析\n\n'
    + change_icon_24h + ' *Price: ' + fmt(price) + '*\n'
    '  1h: ' + ('+' if change1h >= 0 else '') + f'{change1h:.2f}% | '
    '24h: ' + ('+' if change24h >= 0 else '') + f'{change24h:.2f}% | '
    '7d: ' + ('+' if change7d >= 0 else '') + f'{change7d:.2f}%\n\n'
    '\U0001F4CA *市场数据：*\n'
    '  MC: ' + fmt(mc) + ' | FDV: ' + fmt(fdv) + '\n'
    '  Vol/MC: *' + f'{vol_ratio*100:.1f}%* (交易活跃度)\n'
    '  Circ Supply: ' + f'{circ_supply:,.0f}' + ' / ' + f'{total_supply:,.0f}' + '\n'
    '  24h High: ' + fmt(high24h) + ' | Low: ' + fmt(low24h) + '\n'
    '  ATH: ' + fmt(ath) + ' (' + ('+' if ath_change >= 0 else '') + f'{ath_change:.1f}%) | '
    'ATL: ' + fmt(atl) + ' (' + ('+' if atl_change >= 0 else '') + f'{atl_change:.1f}%)\n\n'
    '\U0001F525 *技术指标（30日K线）：*\n'
    '  RSI(14): *' + str(rsi) + '* | MACD: *' + macd + '*\n'
    '  EMA12: ' + fmt(ema12) + ' | EMA20: ' + fmt(ema20) + ' | EMA26: ' + fmt(ema26) + '\n'
    '  BB Upper: ' + fmt(bb_upper) + ' | Mid: ' + fmt(bb_mid) + ' | Lower: ' + fmt(bb_lower) + '\n'
    '  BB 位置: *' + price_vs_bb.replace('_', ' ').title() + '*\n'
    '  Support: ' + fmt(support) + ' | Resistance: ' + fmt(resistance) + '\n\n'
)

# 风险评估
if change7d > 1000:
    risk_level = '\u274C EXTREME'
    risk_note = '7日涨幅超1000%！注意主力砸盘风险'
elif change7d > 100:
    risk_level = '\u26A0\uFE0F HIGH'
    risk_note = '短期涨幅过大，追高风险高'
elif rsi > 68:
    risk_level = '\u26A0\uFE0F HIGH'
    risk_note = 'RSI超买，回调风险较大'
elif vol_ratio < 5:
    risk_level = '\u26A0\uFE0F MEDIUM'
    risk_note = '流动性偏低，注意进出风险'
else:
    risk_level = '\u2705 NORMAL'
    risk_note = '波动正常范围'

msg += '\U0001F6A8 *风险等级: ' + risk_level + '*\n'
msg += '  ' + risk_note + '\n\n'

msg += '\U0001F3AF *策略信号:* ' + dir_icon + ' *' + signal + '* (' + conf + ')\n'
msg += '  ' + reason + '\n'

if sl != 'N/A':
    rr = (tp1 - price) / (price - sl) if (tp1 > price and 'LONG' in signal) or (tp1 < price and 'SHORT' in signal) else abs((price - tp1) / (sl - price)) if sl != price else 0
    msg += '  Entry: *' + fmt(price) + '*\n'
    msg += '  SL: ' + fmt(sl) + ' | TP1: ' + fmt(tp1) + (' | TP2: ' + fmt(tp2) if tp2 != 'N/A' else '') + '\n'
    msg += '  RR: *' + f'{abs(rr):.1f}' + ':1*\n'

msg += '\n\U0001F19a *完整日报:* https://mktrading.vip/btc/\n'
msg += '━━━━━━━━━━━━━━━━━━━━\n'
msg += '\U0001F19A *MK Trading Bot v2.0*\n'
msg += '\u26A0 本分析仅供参考，不构成投资建议'

# ========== 发送 ==========
r = requests.post(
    'https://api.telegram.org/bot' + TOKEN + '/sendMessage',
    json={'chat_id': CHAT_ID, 'text': msg, 'parse_mode': 'Markdown'},
    timeout=10
)
d = r.json()
log('Send result: ' + str(d.get('ok')) + ' | msg_id=' + str(d['result']['message_id'] if d.get('ok') else 'ERROR'), 'TG')
