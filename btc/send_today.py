import requests, json
import sys
sys.stdout.reconfigure(encoding='utf-8')

# 加载配置
with open('C:/Users/asus/mk-trading/btc/telegram_config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)
bot_token = config['bot_token']
chat_id = config['chat_id']

btc_price = 78377.42
btc_chg = 2.618
eth_price = 2370.50
eth_chg = 1.908
sol_price = 86.82
sol_chg = 0.405
fg_value = 46
fg_text = 'Fear'

def mood_emoji(val):
    if val >= 75: return '😱'
    if val >= 55: return '😃'
    if val >= 45: return '😐'
    if val >= 25: return '😰'
    return '😨'

def dir_emoji(d):
    return '🟢 做多' if d == 'LONG' else '🔴 做空' if d == 'SHORT' else '🟡 观望'

strategies = {
    'btc': {'direction': 'WAIT', 'confidence': '-', 'reason': '震荡整理，观望为主'},
    'eth': {'direction': 'WAIT', 'confidence': '-', 'reason': '跟随BTC趋势'},
    'sol': {'direction': 'WAIT', 'confidence': '-', 'reason': '跟随大盘'},
}

msg = f"""⚡ *MK每日策略信号* | 04月23日 09:00
━━━━━━━━━━━━━━━━━━━━

📊 *市场情绪* {mood_emoji(fg_value)}
恐惧贪婪指数: *{fg_value}* ({fg_text})

💰 *行情速览*
BTC: ${btc_price:,.0f} ({btc_chg:+.2f}%)
ETH: ${eth_price:,.0f} ({eth_chg:+.2f}%)
SOL: ${sol_price:,.0f} ({sol_chg:+.2f}%)

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

url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
payload = {'chat_id': chat_id, 'text': msg, 'parse_mode': 'Markdown', 'disable_web_page_preview': True}
r = requests.post(url, json=payload, timeout=15)
result = r.json()
print(json.dumps(result, indent=2, ensure_ascii=False))
