import warnings, json, os, sys
warnings.filterwarnings('ignore')
sys.path.insert(0, 'C:/Users/asus/mk-trading/btc')
from fetch_btc_data import fetch_all

print('Fetching fresh data...')
data = fetch_all()
print('Done')

btc = data['btc']
eth = data['eth']
funding = data['funding']
fg = data['fear_greed']
tech = data['technical']
oi = data['oi']
liq = data['liquidation']

price = btc['price']
change = btc['change_24h']
rsi = round(tech['rsi'], 1)
macd = tech['macd_cross']
ema20 = round(tech['ema20'], 0)
ema50 = round(tech['ema50'], 0)
bb_upper = round(tech['bb_upper'], 0)
bb_lower = round(tech['bb_lower'], 0)
funding_rate = round(funding['rate'], 4)
ls_ratio = oi.get('long_short_ratio', 'N/A')
fear = fg['value']
fear_class = fg['classification']
long_ratio = liq.get('long_ratio', 'N/A')
short_ratio = liq.get('short_ratio', 'N/A')
eth_price = eth['price']

# Strategy logic
if rsi < 35 and macd == 'GOLDEN':
    signal = 'LONG'
    sl = round(price * 0.97, 0)
    tp1 = round(price * 1.03, 0)
    tp2 = round(price * 1.05, 0)
    conf = 'High'
    reason = 'RSI超卖 + MACD金叉共振'
elif rsi > 68 and macd == 'DEAD':
    signal = 'SHORT'
    sl = round(price * 1.03, 0)
    tp1 = round(price * 0.97, 0)
    tp2 = round(price * 0.95, 0)
    conf = 'High'
    reason = 'RSI超买 + MACD死叉共振'
elif rsi < 45:
    signal = 'LONG (试探)'
    sl = round(price * 0.96, 0)
    tp1 = round(price * 1.02, 0)
    tp2 = round(price * 1.04, 0)
    conf = 'Medium'
    reason = 'RSI偏低，MACD未确认方向'
elif rsi > 58:
    signal = 'SHORT (试探)'
    sl = round(price * 1.02, 0)
    tp1 = round(price * 0.98, 0)
    tp2 = round(price * 0.96, 0)
    conf = 'Medium'
    reason = 'RSI偏高，MACD未确认方向'
else:
    signal = 'NEUTRAL'
    sl = tp1 = tp2 = 'N/A'
    conf = 'Low'
    reason = 'RSI中性，MACD中性，方向不明'

# Direction emoji
dir_icon = {'LONG': '\U0001F4C8', 'SHORT': '\U0001F4C9', 'NEUTRAL': '\U0001F6D1'}.get(signal, '\u2796')
dir_icon2 = {'LONG (试探)': '\U0001F4C8', 'SHORT (试探)': '\U0001F4C9'}.get(signal, dir_icon)
if '试探' in signal:
    dir_icon = '\U0001F53A'

change_icon = '\u2B06\uFE0F' if change >= 0 else '\u2B07\uFE0F'

# Format message
msg = (
    '\u26A1 *实时行情播报* ' + '\n'
    '━━━━━━━━━━━━━━━━━━━━\n\n'
    + change_icon + ' *BTC $' + f'{price:,.0f}' + '*  (' + ('+' if change >= 0 else '') + f'{change:.2f}%)\n'
    '\u20AC ETH $' + f'{eth_price:,.0f}' + '\n\n'
    '\U0001F525 RSI: *' + str(rsi) + '* | MACD: *' + macd + '*\n'
    '\U0001F9F9 Fear&Greed: *' + str(fear) + '* (' + fear_class + ')\n'
    '\U0001F4B0 Funding: *' + f'{funding_rate:.4f}' + '%*\n\n'
    '\U0001F4CA 多空清算比：\n'
    '  Long: *' + str(long_ratio) + '%* | Short: *' + str(short_ratio) + '%*\n'
    '  L/S Ratio: *' + str(ls_ratio) + '*\n\n'
    '\U0001F4C8 EMA: 20=' + f'${ema20:,.0f}' + ' | 50=' + f'${ema50:,.0f}' + '\n'
    '\U0001F536 Bollinger: $' + f'{bb_lower:,.0f}' + ' - $' + f'{bb_upper:,.0f}' + '\n\n'
    '\U0001F3AF *今日策略:* ' + dir_icon2 + ' *' + signal + '* (' + conf + ')\n'
    '  ' + reason + '\n'
)
if sl != 'N/A':
    msg += '  Entry: *$' + f'{price:,.0f}' + '*\n'
    msg += '  SL: *$' + f'{sl:,.0f}' + ' | TP1: *$' + f'{tp1:,.0f}' + '*\n'
    rr = (tp1 - price) / (price - sl) if signal.startswith('LONG') else (price - tp1) / (sl - price)
    msg += '  TP2: *$' + f'{tp2:,.0f}' + ' | RR: *' + f'{abs(rr):.1f}' + ':1*\n'

msg += '\n\U0001F6A8 *完整日报:* https://mktrading.vip/btc/\n'
msg += '━━━━━━━━━━━━━━━━━━━━\n'
msg += '\U0001F19A *MK Trading Bot v2.0*'

# Send to channel
TOKEN = '8626387493:AAE2XCzMzmhDiWRaGKVEjrj2EGLPsDN22-Q'
CHAT_ID = '-1003189007280'

import requests
r = requests.post(
    'https://api.telegram.org/bot' + TOKEN + '/sendMessage',
    json={'chat_id': CHAT_ID, 'text': msg, 'parse_mode': 'Markdown'},
    timeout=10
)
d = r.json()
print('\n--- Send Result ---')
print('OK:', d.get('ok'))
if d.get('ok'):
    print('Msg ID:', d['result']['message_id'])
else:
    print('Error:', d)
