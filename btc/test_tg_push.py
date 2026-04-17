import warnings, json, os, sys
warnings.filterwarnings('ignore')

sys.path.insert(0, os.path.dirname(__file__))
from fetch_btc_data import load_cache, fetch_all
from telegram_notify import notify_telegram

# Load or fetch data
data = load_cache()
if not data:
    print('Fetching fresh data...')
    data = fetch_all()
    print('Data fetched')

# Quick strategy from data
price = data['btc']['price']
rsi = round(data['technical']['rsi'], 1)
macd = data['technical']['macd_cross']
fg = data['fear_greed']['value']
fg_class = data['fear_greed']['classification']
funding = round(data['funding']['rate'], 4)
oi_ratio = data['oi'].get('long_short_ratio', 'N/A')

# Simple strategy
if rsi < 35 and macd == 'GOLDEN':
    signal = 'LONG'
    sl = round(price * 0.97, 0)
    tp = round(price * 1.05, 0)
elif rsi > 65 and macd == 'DEAD':
    signal = 'SHORT'
    sl = round(price * 1.03, 0)
    tp = round(price * 0.95, 0)
else:
    signal = 'NEUTRAL'
    sl = tp = 'N/A'

strategy = {
    'signal': signal,
    'entry': price,
    'stop_loss': sl,
    'take_profit': tp,
    'confidence': 'medium',
    'reason': f'RSI={rsi}, MACD={macd}, Fear={fg}({fg_class})'
}

print(f'Signal: {signal}, Price: {price}, RSI: {rsi}, MACD: {macd}')
print(f'Funding: {funding}%, OI Long/Short: {oi_ratio}')
print(f'SL: {sl}, TP: {tp}')

# Send Telegram
ok, result = notify_telegram(data, strategy, None)
print(f'Telegram result: ok={ok}, msg_id={result}')
