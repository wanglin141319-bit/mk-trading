import requests, json
from datetime import datetime

results = {}

# BTC 24h klines for high/low
try:
    r = requests.get('https://api.binance.com/api/v3/klines', params={'symbol':'BTCUSDT','interval':'1d','limit':3}, timeout=10)
    d = r.json()
    for k in d:
        dt = datetime.fromtimestamp(k[0]/1000)
        ds = dt.strftime('%Y-%m-%d')
        results[f'daily_{ds}'] = {'O':float(k[1]),'H':float(k[2]),'L':float(k[3]),'C':float(k[4]),'V':float(k[5])}
        print(f'DAILY {ds}: O={k[1]} H={k[2]} L={k[3]} C={k[4]}')
except Exception as e:
    print('KLINE ERR:', e)

# BTC 4h klines for RSI/MACD/EMA/Bollinger
try:
    r = requests.get('https://api.binance.com/api/v3/klines', params={'symbol':'BTCUSDT','interval':'4h','limit':50}, timeout=10)
    d = r.json()
    closes = [float(k[4]) for k in d]
    highs = [float(k[2]) for k in d]
    lows = [float(k[3]) for k in d]
    
    # RSI(14)
    deltas = [closes[i]-closes[i-1] for i in range(1,len(closes))]
    gains = [d if d>0 else 0 for d in deltas]
    losses_v = [-d if d<0 else 0 for d in deltas]
    avg_gain = sum(gains[:14])/14
    avg_loss = sum(losses_v[:14])/14
    for i in range(14, len(gains)):
        avg_gain = (avg_gain*13+gains[i])/14
        avg_loss = (avg_loss*13+losses_v[i])/14
    rs = avg_gain/avg_loss if avg_loss!=0 else 100
    rsi = 100 - 100/(1+rs)
    results['rsi'] = round(rsi, 1)
    print(f'RSI(14)={rsi:.1f}')
    
    # EMA
    def ema(data, period):
        result = [data[0]]
        k = 2/(period+1)
        for i in range(1, len(data)):
            result.append(data[i]*k + result[-1]*(1-k))
        return result
    
    ema7 = ema(closes, 7)
    ema20 = ema(closes, 20)
    ema50 = ema(closes, 50) if len(closes)>=50 else None
    results['ema7'] = round(ema7[-1])
    results['ema20'] = round(ema20[-1])
    results['ema50'] = round(ema50[-1]) if ema50 else None
    print(f'EMA7={ema7[-1]:.0f} EMA20={ema20[-1]:.0f}')
    if ema50:
        print(f'EMA50={ema50[-1]:.0f}')
    
    # MACD (12, 26, 9)
    ema12 = ema(closes, 12)
    ema26 = ema(closes, 26)
    macd_line = [ema12[i]-ema26[i] for i in range(len(closes))]
    signal = ema(macd_line, 9)
    hist = [macd_line[i]-signal[i] for i in range(len(closes))]
    results['macd'] = round(macd_line[-1])
    results['signal'] = round(signal[-1])
    results['hist'] = round(hist[-1])
    macd_cross = 'Bullish' if hist[-1]>0 and hist[-2]<=0 else ('Bearish' if hist[-1]<0 and hist[-2]>=0 else ('Bullish' if hist[-1]>0 else 'Bearish'))
    results['macd_signal'] = macd_cross
    print(f'MACD={macd_line[-1]:.0f} Signal={signal[-1]:.0f} Hist={hist[-1]:.0f} Cross={macd_cross}')
    
    # Bollinger Bands (20, 2)
    bb_middle = ema20[-1]
    bb_std = (sum((c-bb_middle)**2 for c in closes[-20:])/20)**0.5
    bb_upper = bb_middle + 2*bb_std
    bb_lower = bb_middle - 2*bb_std
    bb_width = (bb_upper-bb_lower)/bb_middle*100
    results['bb_upper'] = round(bb_upper)
    results['bb_middle'] = round(bb_middle)
    results['bb_lower'] = round(bb_lower)
    results['bb_width'] = round(bb_width, 1)
    print(f'BB: upper={bb_upper:.0f} middle={bb_middle:.0f} lower={bb_lower:.0f} width={bb_width:.1f}%')
    
    # Support/Resistance
    recent_highs = highs[-10:]
    recent_lows = lows[-10:]
    r1 = max(recent_highs)
    s1 = min(recent_lows)
    pc = closes[-1]
    pivot = (r1 + s1 + pc) / 3
    r2 = 2*pivot - s1
    s2 = 2*pivot - r1
    results['r1'] = round(r1)
    results['r2'] = round(r2)
    results['s1'] = round(s1)
    results['s2'] = round(s2)
    results['pivot'] = round(pivot)
    print(f'Pivot={pivot:.0f} R1={r1:.0f} R2={r2:.0f} S1={s1:.0f} S2={s2:.0f}')

    # EMA alignment
    if ema50:
        results['ema_alignment'] = 'bullish' if ema7[-1]>ema20[-1]>ema50[-1] else ('bearish' if ema7[-1]<ema20[-1]<ema50[-1] else 'mixed')
    else:
        results['ema_alignment'] = 'bullish' if ema7[-1]>ema20[-1] else 'bearish'
    ea = results["ema_alignment"]
    print(f'EMA alignment: {ea}')

except Exception as e:
    print('TECH ERR:', e)

# Taker buy/sell volume for liquidation estimate
try:
    r = requests.get('https://fapi.binance.com/futures/data/takerlongshortRatio', params={'symbol':'BTCUSDT','period':'1h','limit':24}, timeout=10)
    d = r.json()
    # Estimate long/short liquidations from the ratio
    longs = sum(float(x['buyVol']) for x in d)
    shorts = sum(float(x['sellVol']) for x in d)
    total = longs + shorts
    long_pct = longs/total*100 if total>0 else 50
    results['taker_long_pct'] = round(long_pct, 1)
    print(f'Taker buy/sell 24h: long={long_pct:.1f}% short={100-long_pct:.1f}%')
except Exception as e:
    print('TAKER ERR:', e)

# Save results
with open('c:/Users/asus/mk-trading/btc/cache/daily_data_20260424.json', 'w') as f:
    json.dump(results, f, indent=2)
print('DATA SAVED OK')
