"""Fetch BTC market data from Binance and calculate technical indicators"""
import requests
import json
import sys

def fetch_data():
    results = {}
    
    # 1. 资金费率
    try:
        r = requests.get('https://fapi.binance.com/fapi/v1/fundingRate?symbol=BTCUSDT&limit=3', timeout=10)
        results['funding_rate'] = r.json()
        print('=== FUNDING RATE ===')
        print(json.dumps(results['funding_rate'], indent=2))
    except Exception as e:
        print(f'Funding rate error: {e}')
        results['funding_rate'] = []

    # 2. OI (Open Interest)
    try:
        r = requests.get('https://fapi.binance.com/fapi/v1/openInterest?symbol=BTCUSDT', timeout=10)
        results['oi'] = r.json()
        print('\n=== OPEN INTEREST ===')
        print(json.dumps(results['oi'], indent=2))
    except Exception as e:
        print(f'OI error: {e}')
    
    # 3. K线数据 - 60天日线用于技术指标计算
    try:
        r = requests.get('https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1d&limit=60', timeout=15)
        klines = r.json()
        ohlcv = []
        for k in klines:
            ohlcv.append({
                'time': k[0],
                'open': float(k[1]),
                'high': float(k[2]),
                'low': float(k[3]),
                'close': float(k[4]),
                'volume': float(k[5])
            })
        results['klines'] = ohlcv
        
        print('\n=== KLINES (last 20) ===')
        import datetime
        for o in ohlcv[-20:]:
            ts = datetime.datetime.fromtimestamp(o['time']/1000).strftime('%Y-%m-%d')
            print(f"{ts} O={o['open']:.0f} H={o['high']:.0f} L={o['low']:.0f} C={o['close']:.0f}")
        
        # 计算技术指标
        closes = [c['close'] for c in ohlcv]
        highs = [c['high'] for c in ohlcv]
        lows = [c['low'] for c in ohlcv]
        
        # RSI(14)
        def calc_rsi(closes, period=14):
            if len(closes) < period + 1:
                return 50
            deltas = [closes[i] - closes[i-1] for i in range(1, len(closes))]
            gains = [d if d > 0 else 0 for d in deltas]
            losses = [-d if d < 0 else 0 for d in deltas]
            
            avg_gain = sum(gains[-period:]) / period
            avg_loss = sum(losses[-period:]) / period
            
            # Wilder平滑
            for i in range(period, len(gains)):
                avg_gain = (avg_gain * (period - 1) + gains[i]) / period
                avg_loss = (avg_loss * (period - 1) + losses[i]) / period
            
            if avg_loss == 0:
                return 100
            rs = avg_gain / avg_loss
            return round(100 - (100 / (1 + rs)), 1)
        
        # EMA
        def calc_ema(data, period):
            if len(data) < period:
                return data[-1] if data else 0
            ema = sum(data[:period]) / period
            multiplier = 2 / (period + 1)
            for price in data[period:]:
                ema = (price - ema) * multiplier + ema
            return round(ema, 0)
        
        # MACD
        def calc_macd(closes, fast=12, slow=26, signal=9):
            ema_fast = calc_ema_list(closes, fast)
            ema_slow = calc_ema_list(closes, slow)
            macd_line = [ef - es for ef, es in zip(ema_fast, ema_slow)]
            
            # Signal line (EMA of MACD)
            signal_line = calc_ema_list(macd_line, signal)
            
            current_macd = round(macd_line[-1], 2)
            current_signal = round(signal_line[-1], 2)
            histogram = round(current_macd - current_signal, 2)
            
            # 判断金叉/死叉
            if len(macd_line) >= 2 and len(signal_line) >= 2:
                prev_diff = macd_line[-2] - signal_line[-2]
                curr_diff = macd_line[-1] - signal_line[-1]
                cross = "GOLDEN" if prev_diff <= 0 and curr_diff > 0 else ("DEAD" if prev_diff >= 0 and curr_diff < 0 else "NONE")
            else:
                cross = "UNKNOWN"
            
            return {'macd': current_macd, 'signal': current_signal, 'histogram': histogram, 'cross': cross}
        
        def calc_ema_list(data, period):
            if len(data) < period:
                return [data[-1]] * len(data)
            ema_values = []
            ema = sum(data[:period]) / period
            ema_values.extend([0] * (period - 1))
            ema_values.append(ema)
            multiplier = 2 / (period + 1)
            for price in data[period:]:
                ema = (price - ema) * multiplier + ema
                ema_values.append(ema)
            return ema_values
        
        # 布林带
        def calc_bollinger(closes, period=20, std_dev=2):
            if len(closes) < period:
                return {'upper': 0, 'middle': 0, 'lower': 0}
            sma = sum(closes[-period:]) / period
            variance = sum((x - sma) ** 2 for x in closes[-period:]) / period
            std = variance ** 0.5
            return {
                'upper': round(sma + std_dev * std, 0),
                'middle': round(sma, 0),
                'lower': round(sma - std_dev * std, 0),
                'bandwidth': round((sma + std_dev * std - sma + std_dev * std) / sma * 100, 1) if sma > 0 else 0
            }
        
        # 支撑阻力位 (基于近期高低点)
        def calc_support_resistance(highs, lows, closes, lookback=14):
            recent_highs = highs[-lookback:]
            recent_lows = lows[-lookback:]
            resistance_levels = sorted(set(recent_highs), reverse=True)[:4]
            support_levels = sorted(set(recent_lows))[:4]
            
            # 找关键阻力位（最近的高点区域）
            key_resistance = max(recent_highs)
            key_support = min(recent_lows)
            current_price = closes[-1]
            
            return {
                'resistance_1': round(key_resistance * 1.01, 0),  # 紧密阻力
                'resistance_2': round(key_resistance * 1.03, 0),  # 强阻力
                'support_1': round(key_support * 0.99, 0),       # 紧密支撑
                'support_2': round(key_support * 0.97, 0),       # 强支撑
                'pivot': round((key_resistance + key_support) / 2, 0)
            }
        
        rsi_val = calc_rsi(closes)
        ema7 = calc_ema(closes, 7)
        ema20 = calc_ema(closes, 20)
        ema50 = calc_ema(closes, 50)
        macd_data = calc_macd(closes)
        boll = calc_bollinger(closes)
        sr = calc_support_resistance(highs, lows, closes)
        
        print('\n=== TECHNICAL INDICATORS ===')
        print(json.dumps({
            'RSI_14': rsi_val,
            'EMA_7': ema7,
            'EMA_20': ema20,
            'EMA_50': ema50,
            'MACD': macd_data,
            'Bollinger': boll,
            'Support_Resistance': sr,
            'Current_Close': closes[-1],
        }, indent=2))
        
        results['indicators'] = {
            'RSI_14': rsi_val,
            'EMA_7': ema7,
            'EMA_20': ema20,
            'EMA_50': ema50,
            'MACD': macd_data,
            'Bollinger': boll,
            'Support_Resistance': sr,
            'Current_Close': closes[-1],
        }
        
    except Exception as e:
        print(f'Klines error: {e}')
        import traceback
        traceback.print_exc()
    
    # 4. 多空持仓比
    try:
        ls = requests.get('https://fapi.binance.com/fapi/v1/globalLongShortAccountRatio?symbol=BTCUSDT&period=4h&limit=5', timeout=10)
        results['long_short_ratio'] = ls.json()
        print('\n=== LONG SHORT RATIO ===')
        print(json.dumps(results['long_short_ratio'], indent=2))
    except Exception as e:
        print(f'L/S ratio error: {e}')
    
    # 5. 爆仓量 (24h估算)
    try:
        liq = requests.get('https://fapi.binance.com/futures/data/topLongShortPositionRatio?symbol=BTCUSDT&period=1h&limit=24', timeout=10)
        results['liq_data'] = liq.json()
    except Exception as e:
        print(f'Liquidation data error: {e}')

    # 6. ETH资金费率
    try:
        fr_eth = requests.get('https://fapi.binance.com/fapi/v1/fundingRate?symbol=ETHUSDT&limit=1', timeout=10)
        results['eth_funding_rate'] = fr_eth.json()
        print('\n=== ETH FUNDING RATE ===')
        print(json.dumps(results['eth_funding_rate'], indent=2))
    except Exception as e:
        print(f'ETH FR error: {e}')
    
    return results

if __name__ == '__main__':
    fetch_data()
