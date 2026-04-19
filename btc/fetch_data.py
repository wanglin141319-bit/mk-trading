"""
BTC Daily Report Data Fetcher
Fetches real-time data from free APIs: CoinGecko, Binance, Fear & Greed
"""
import requests
import json
import sys
from datetime import datetime

BASE_URL = "https://api.coingecko.com/api/v3"
BINANCE_URL = "https://fapi.binance.com"
ALTERNATIVE_URL = "https://api.alternative.me/fng"

def get_btc_price():
    """Get BTC current price and 24h change from CoinGecko"""
    try:
        url = f"{BASE_URL}/simple/price"
        params = {"ids": "bitcoin", "vs_currencies": "usd", "include_24hr_change": "true", "include_24hr_vol": "true"}
        resp = requests.get(url, params=params, timeout=15)
        data = resp.json()
        btc = data["bitcoin"]
        return {
            "price": btc["usd"],
            "change_24h": btc["usd_24h_change"],
            "volume_24h": btc["usd_24h_vol"]
        }
    except Exception as e:
        print(f"[ERROR] CoinGecko BTC price: {e}", file=sys.stderr)
        return None

def get_eth_price():
    """Get ETH current price and 24h change from CoinGecko"""
    try:
        url = f"{BASE_URL}/simple/price"
        params = {"ids": "ethereum", "vs_currencies": "usd", "include_24hr_change": "true", "include_24hr_vol": "true"}
        resp = requests.get(url, params=params, timeout=15)
        data = resp.json()
        eth = data["ethereum"]
        return {
            "price": eth["usd"],
            "change_24h": eth["usd_24h_change"],
            "volume_24h": eth["usd_24h_vol"]
        }
    except Exception as e:
        print(f"[ERROR] CoinGecko ETH price: {e}", file=sys.stderr)
        return None

def get_binance_funding_rate():
    """Get BTC and ETH perpetual funding rates from Binance"""
    try:
        url = f"{BINANCE_URL}/fapi/v1/premiumIndex"
        resp = requests.get(url, timeout=15)
        data = resp.json()
        result = {}
        for item in data:
            symbol = item.get("symbol", "")
            if symbol == "BTCUSDT":
                result["btc_funding"] = float(item.get("lastFundingRate", 0)) * 100
            elif symbol == "ETHUSDT":
                result["eth_funding"] = float(item.get("lastFundingRate", 0)) * 100
        return result
    except Exception as e:
        print(f"[ERROR] Binance funding rate: {e}", file=sys.stderr)
        return {}

def get_binance_oi():
    """Get open interest for BTCUSDT from Binance"""
    try:
        url = f"{BINANCE_URL}/fapi/v1/openInterest"
        params = {"symbol": "BTCUSDT"}
        resp = requests.get(url, params=params, timeout=15)
        data = resp.json()
        oi_btc = float(data.get("openInterest", 0))
        return oi_btc
    except Exception as e:
        print(f"[ERROR] Binance OI: {e}", file=sys.stderr)
        return None

def get_binance_long_short_ratio():
    """Get top traders long/short ratio from Binance"""
    try:
        url = f"{BINANCE_URL}/futures/data/topLongShortPositionRatio"
        params = {"symbol": "BTCUSDT", "period": "1h", "limit": 1}
        resp = requests.get(url, params=params, timeout=15)
        data = resp.json()
        if data:
            item = data[-1]
            return {
                "long_ratio": float(item.get("longAccount", 0)) * 100,
                "short_ratio": float(item.get("shortAccount", 0)) * 100,
            }
        return None
    except Exception as e:
        print(f"[ERROR] Binance long/short ratio: {e}", file=sys.stderr)
        return None

def get_binance_liquidation():
    """Get recent liquidation data (approximation via latest candlestick trades)"""
    try:
        # Use recent trades to estimate liquidation pressure
        url = f"{BINANCE_URL}/fapi/v1/trades"
        params = {"symbol": "BTCUSDT", "limit": 100}
        resp = requests.get(url, params=params, timeout=15)
        trades = resp.json()
        buy_vol = sum(float(t["qty"]) for t in trades if t["isBuyerMaker"] == False)
        sell_vol = sum(float(t["qty"]) for t in trades if t["isBuyerMaker"] == True)
        return {"buy_vol_100": buy_vol, "sell_vol_100": sell_vol}
    except Exception as e:
        print(f"[ERROR] Binance trades: {e}", file=sys.stderr)
        return None

def get_fear_greed():
    """Get Fear & Greed Index"""
    try:
        resp = requests.get(ALTERNATIVE_URL, timeout=15)
        data = resp.json()
        items = data.get("data", [])
        if items:
            item = items[0]
            return {
                "value": int(item.get("value", 50)),
                "classification": item.get("value_classification", "Neutral")
            }
        return None
    except Exception as e:
        print(f"[ERROR] Fear & Greed: {e}", file=sys.stderr)
        return None

def get_btc_ohlc():
    """Get OHLC data for technical indicators from CoinGecko"""
    try:
        url = f"{BASE_URL}/coins/bitcoin/ohlc"
        params = {"vs_currency": "usd", "days": "30"}
        resp = requests.get(url, params=params, timeout=15)
        data = resp.json()  # list of [timestamp, open, high, low, close]
        return data
    except Exception as e:
        print(f"[ERROR] BTC OHLC: {e}", file=sys.stderr)
        return None

def compute_technical_indicators(ohlc_data):
    """Calculate RSI(14), EMA, Bollinger Bands from OHLC data"""
    if not ohlc_data or len(ohlc_data) < 20:
        return None

    closes = [c[4] for c in ohlc_data]

    # RSI(14)
    def calc_rsi(prices, period=14):
        deltas = [prices[i] - prices[i-1] for i in range(1, len(prices))]
        gains = [d if d > 0 else 0 for d in deltas]
        losses = [-d if d < 0 else 0 for d in deltas]
        avg_gain = sum(gains[:period]) / period
        avg_loss = sum(losses[:period]) / period
        for i in range(period, len(deltas)):
            avg_gain = (avg_gain * (period - 1) + gains[i]) / period
            avg_loss = (avg_loss * (period - 1) + losses[i]) / period
        if avg_loss == 0:
            return 100
        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))

    # EMA
    def calc_ema(prices, period):
        k = 2 / (period + 1)
        ema = sum(prices[:period]) / period
        for p in prices[period:]:
            ema = p * k + ema * (1 - k)
        return ema

    # Bollinger Bands
    def calc_bb(prices, period=20):
        sma = sum(prices[-period:]) / period
        variance = sum((p - sma) ** 2 for p in prices[-period:]) / period
        std = variance ** 0.5
        return {"upper": sma + 2 * std, "middle": sma, "lower": sma - 2 * std}

    # MACD (12, 26, 9)
    def calc_macd(prices):
        ema12 = calc_ema(prices, 12)
        ema26 = calc_ema(prices, 26)
        macd = ema12 - ema26
        signal = macd  # simplified
        return macd

    current_price = closes[-1]
    ema7 = calc_ema(closes, 7)
    ema20 = calc_ema(closes, 20)
    ema50 = calc_ema(closes, min(50, len(closes)))
    rsi = calc_rsi(closes, 14)
    bb = calc_bb(closes)
    macd_val = calc_macd(closes)

    return {
        "price": current_price,
        "ema7": round(ema7, 2),
        "ema20": round(ema20, 2),
        "ema50": round(ema50, 2),
        "rsi": round(rsi, 1),
        "bb_upper": round(bb["upper"], 2),
        "bb_middle": round(bb["middle"], 2),
        "bb_lower": round(bb["lower"], 2),
        "macd": round(macd_val, 2),
        "macd_histogram": round(macd_val, 2),  # simplified
    }

def main():
    print("=" * 60)
    print(f"BTC Daily Report Data Fetch — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    result = {}

    # BTC Price
    btc_price = get_btc_price()
    if btc_price:
        result["btc_price"] = btc_price["price"]
        result["btc_change"] = round(btc_price["change_24h"], 2)
        result["btc_volume"] = btc_price["volume_24h"]
        print(f"BTC: ${btc_price['price']:,.0f} ({btc_price['change_24h']:+.2f}%)")

    # ETH Price
    eth_price = get_eth_price()
    if eth_price:
        result["eth_price"] = eth_price["price"]
        result["eth_change"] = round(eth_price["change_24h"], 2)
        print(f"ETH: ${eth_price['price']:,.0f} ({eth_price['change_24h']:+.2f}%)")

    # Binance Funding
    funding = get_binance_funding_rate()
    if funding:
        result["btc_funding"] = funding.get("btc_funding", 0)
        result["eth_funding"] = funding.get("eth_funding", 0)
        print(f"BTC Funding: {funding.get('btc_funding', 0):.4f}%")
        print(f"ETH Funding: {funding.get('eth_funding', 0):.4f}%")

    # OI
    oi = get_binance_oi()
    if oi:
        result["btc_oi"] = oi
        print(f"BTC OI: {oi:,.0f} BTC")

    # Long/Short Ratio
    ls_ratio = get_binance_long_short_ratio()
    if ls_ratio:
        result["long_ratio"] = ls_ratio["long_ratio"]
        result["short_ratio"] = ls_ratio["short_ratio"]
        print(f"Long Ratio: {ls_ratio['long_ratio']:.1f}% / Short: {ls_ratio['short_ratio']:.1f}%")

    # Fear & Greed
    fg = get_fear_greed()
    if fg:
        result["fear_greed"] = fg["value"]
        result["fear_greed_class"] = fg["classification"]
        print(f"Fear & Greed: {fg['value']} ({fg['classification']})")

    # Technical Indicators
    ohlc = get_btc_ohlc()
    if ohlc:
        ti = compute_technical_indicators(ohlc)
        if ti:
            result["technical"] = ti
            print(f"RSI(14): {ti['rsi']}")
            print(f"EMA7: {ti['ema7']} | EMA20: {ti['ema20']} | EMA50: {ti['ema50']}")
            print(f"BB Upper: {ti['bb_upper']} | Middle: {ti['bb_middle']} | Lower: {ti['bb_lower']}")
            print(f"MACD: {ti['macd']}")

    print("=" * 60)
    print("Data fetch complete.")
    print(json.dumps(result, indent=2))
    return result

if __name__ == "__main__":
    main()
