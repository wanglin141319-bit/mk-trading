"""
BTC/ETH/SOL 每日策略推送脚本
每天早上9点自动发送策略方向信号到Telegram频道
"""
import requests
import json
import os
from datetime import datetime

# 代理配置：优先使用环境变量，回退到常用本地代理端口
def _setup_proxy():
    """自动检测并设置代理"""
    if os.environ.get('HTTPS_PROXY') or os.environ.get('https_proxy'):
        return  # 环境变量已设置，跳过
    for port in [33210, 7890, 7891, 10808, 10809]:
        try:
            test = requests.get('https://api.coingecko.com/api/v3/ping',
                                proxies={'https': f'http://127.0.0.1:{port}'}, timeout=3)
            if test.status_code == 200:
                os.environ['HTTP_PROXY'] = f'http://127.0.0.1:{port}'
                os.environ['HTTPS_PROXY'] = f'http://127.0.0.1:{port}'
                return
        except Exception:
            continue

_setup_proxy()

CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'telegram_config.json')

def load_config():
    """加载配置"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def fetch_crypto_data():
    """获取BTC/ETH/SOL实时数据，CoinGecko优先，Binance回退"""
    data = _fetch_coingecko()
    if data:
        return data
    print("[WARN] CoinGecko失败，切换Binance API...")
    return _fetch_binance()

def _fetch_coingecko():
    """CoinGecko数据源"""
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            'ids': 'bitcoin,ethereum,solana',
            'vs_currencies': 'usd',
            'include_24hr_change': 'true',
            'include_24hr_vol': 'true'
        }
        r = requests.get(url, params=params, timeout=10)
        data = r.json()
        
        # 恐惧贪婪指数
        fear_greed = _fetch_fear_greed()
        
        return {
            'btc': {
                'price': data['bitcoin']['usd'],
                'change': data['bitcoin'].get('usd_24h_change', 0),
            },
            'eth': {
                'price': data['ethereum']['usd'],
                'change': data['ethereum'].get('usd_24h_change', 0),
            },
            'sol': {
                'price': data['solana']['usd'],
                'change': data['solana'].get('usd_24h_change', 0),
            },
            'fear_greed': fear_greed
        }
    except Exception as e:
        print(f"[WARN] CoinGecko获取失败: {e}")
        return None

def _fetch_binance():
    """Binance数据源（备用）"""
    try:
        symbols = {'btc': 'BTCUSDT', 'eth': 'ETHUSDT', 'sol': 'SOLUSDT'}
        result = {}
        for key, symbol in symbols.items():
            url = f"https://api.binance.com/api/v3/ticker/24hr"
            r = requests.get(url, params={'symbol': symbol}, timeout=10)
            d = r.json()
            result[key] = {
                'price': float(d['lastPrice']),
                'change': float(d['priceChangePercent']),
            }
        
        fear_greed = _fetch_fear_greed()
        result['fear_greed'] = fear_greed
        return result
    except Exception as e:
        print(f"[ERROR] Binance获取失败: {e}")
        return None

def _fetch_fear_greed():
    """获取恐惧贪婪指数"""
    try:
        fg_url = "https://api.alternative.me/fng/?limit=1"
        fg_r = requests.get(fg_url, timeout=10)
        fg_data = fg_r.json()
        return fg_data['data'][0] if fg_data.get('data') else {'value': 50, 'value_classification': 'Neutral'}
    except Exception as e:
        print(f"[WARN] 恐惧贪婪指数获取失败: {e}")
        return {'value': 50, 'value_classification': 'Neutral'}

def analyze_strategy(data):
    """基于数据生成策略方向"""
    btc_change = data['btc']['change']
    eth_change = data['eth']['change']
    sol_change = data['sol']['change']
    fg_value = int(data['fear_greed'].get('value', 50))
    
    # 策略逻辑
    strategies = {}
    
    # BTC策略
    if fg_value < 25:  # 极度恐惧 -> 反弹机会
        strategies['btc'] = {'direction': 'LONG', 'confidence': '中', 'reason': '极度恐惧，关注反弹'}
    elif fg_value > 75:  # 极度贪婪 -> 回调风险
        strategies['btc'] = {'direction': 'SHORT', 'confidence': '中', 'reason': '极度贪婪，警惕回调'}
    elif btc_change < -3:
        strategies['btc'] = {'direction': 'LONG', 'confidence': '中', 'reason': '跌幅较大，超跌反弹'}
    elif btc_change > 3:
        strategies['btc'] = {'direction': 'SHORT', 'confidence': '低', 'reason': '涨幅较大，谨慎追高'}
    else:
        strategies['btc'] = {'direction': 'WAIT', 'confidence': '-', 'reason': '震荡整理，观望为主'}
    
    # ETH策略（跟随BTC但波动更大）
    if eth_change < btc_change - 1:
        strategies['eth'] = {'direction': 'LONG', 'confidence': '中', 'reason': '相对BTC超跌'}
    elif eth_change > btc_change + 1:
        strategies['eth'] = {'direction': 'SHORT', 'confidence': '低', 'reason': '相对BTC超涨'}
    else:
        strategies['eth'] = strategies['btc'].copy()
        strategies['eth']['reason'] = '跟随BTC趋势'
    
    # SOL策略（高波动）
    if abs(sol_change) > 5:
        strategies['sol'] = {'direction': 'SHORT' if sol_change > 0 else 'LONG', 'confidence': '高', 'reason': '高波动，反向操作'}
    else:
        strategies['sol'] = strategies['btc'].copy()
        strategies['sol']['reason'] = '跟随大盘'
    
    return strategies

def format_alert_message(data, strategies):
    """格式化Telegram消息"""
    now = datetime.now().strftime('%m月%d日 %H:%M')
    fg_value = data['fear_greed'].get('value', 50)
    fg_text = data['fear_greed'].get('value_classification', 'Neutral')
    
    # 情绪emoji
    def mood_emoji(val):
        val = int(val)
        if val >= 75: return "😱"
        if val >= 55: return "😃"
        if val >= 45: return "😐"
        if val >= 25: return "😰"
        return "😨"
    
    # 方向emoji
    def dir_emoji(d):
        return "🟢 做多" if d == 'LONG' else "🔴 做空" if d == 'SHORT' else "🟡 观望"
    
    btc = data['btc']
    eth = data['eth']
    sol = data['sol']
    
    msg = f"""⚡ *MK每日策略信号* | {now}
━━━━━━━━━━━━━━━━━━━━

📊 *市场情绪* {mood_emoji(fg_value)}
恐惧贪婪指数: *{fg_value}* ({fg_text})

💰 *行情速览*
BTC: `${btc['price']:,.0f}` ({btc['change']:+.2f}%)
ETH: `${eth['price']:,.0f}` ({eth['change']:+.2f}%)
SOL: `${sol['price']:,.0f}` ({sol['change']:+.2f}%)

🎯 *今日策略方向*

*BTC:* {dir_emoji(strategies['btc']['direction'])}
├ 信心: {strategies['btc']['confidence']}
└ {strategies['btc']['reason']}

*ETH:* {dir_emoji(strategies['eth']['direction'])}
├ 信心: {strategies['eth']['confidence']}
└ {strategies['eth']['reason']}

*SOL:* {dir_emoji(strategies['sol']['direction'])}
├ 信心: {strategies['sol']['confidence']}
└ {strategies['sol']['reason']}

⚠️ *风险提示*
以上信号仅供参考，不构成投资建议。
请结合自身风控谨慎决策。

📈 完整日报: https://mktrading.vip/btc/
━━━━━━━━━━━━━━━━━━━━
🤖 MK Trading Bot v2.1"""
    
    return msg

def send_telegram_message(bot_token, chat_id, text):
    """发送Telegram消息"""
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'Markdown',
        'disable_web_page_preview': True,
    }
    try:
        r = requests.post(url, json=payload, timeout=10)
        result = r.json()
        if result.get('ok'):
            print(f"[OK] 消息已发送, message_id={result['result']['message_id']}")
            return True
        else:
            print(f"[ERROR] 发送失败: {result}")
            return False
    except Exception as e:
        print(f"[ERROR] 请求异常: {e}")
        return False

def main():
    """主函数"""
    print(f"\n{'='*50}")
    print(f"BTC/ETH/SOL 每日策略推送")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}\n")
    
    # 加载配置
    config = load_config()
    if not config:
        print("[ERROR] 未找到配置文件，请先运行 telegram_notify.py --setup-tg")
        return False
    
    bot_token = config.get('bot_token')
    chat_id = config.get('chat_id')
    
    if not bot_token or not chat_id:
        print("[ERROR] 配置不完整，缺少bot_token或chat_id")
        return False
    
    print(f"[INFO] 目标频道: {config.get('channel_username', chat_id)}")
    
    # 获取数据
    print("[INFO] 正在获取市场数据...")
    data = fetch_crypto_data()
    if not data:
        print("[ERROR] 数据获取失败")
        return False
    
    print(f"[OK] BTC: ${data['btc']['price']:,.0f} ({data['btc']['change']:+.2f}%)")
    print(f"[OK] ETH: ${data['eth']['price']:,.0f} ({data['eth']['change']:+.2f}%)")
    print(f"[OK] SOL: ${data['sol']['price']:,.0f} ({data['sol']['change']:+.2f}%)")
    
    # 分析策略
    strategies = analyze_strategy(data)
    print(f"\n[INFO] 策略分析完成:")
    print(f"  BTC: {strategies['btc']['direction']} | ETH: {strategies['eth']['direction']} | SOL: {strategies['sol']['direction']}")
    
    # 格式化消息
    message = format_alert_message(data, strategies)
    
    # 发送消息
    print(f"\n[INFO] 正在发送Telegram消息...")
    success = send_telegram_message(bot_token, chat_id, message)
    
    if success:
        print(f"\n[OK] 策略推送完成!")
    else:
        print(f"\n[ERROR] 推送失败")
    
    return success

if __name__ == '__main__':
    main()
