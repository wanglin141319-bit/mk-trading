"""
Telegram 日报推送模块 - v1.0
配合 BTC 日报自动化使用
"""
import requests
import json
import os
from datetime import datetime

# ============ 配置 ============
# 从配置文件加载 Bot Token 和 Chat ID
CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'telegram_config.json')

def load_config():
    """加载 Telegram 配置"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def save_config(bot_token, chat_id):
    """保存 Telegram 配置"""
    config = {'bot_token': bot_token, 'chat_id': chat_id}
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    print('Config saved to', CONFIG_FILE)

# ============ Bot 操作 ============
def test_bot(bot_token):
    """测试 Bot Token 是否有效"""
    url = f'https://api.telegram.org/bot{bot_token}/getMe'
    r = requests.get(url, timeout=8)
    d = r.json()
    if d.get('ok'):
        return True, '@' + d['result']['username']
    return False, d.get('description', 'Invalid token')

def get_chat_id(bot_token):
    """获取 Bot 已加入群组的 chat_id（需要用户先邀请 Bot 进群/频道）"""
    url = f'https://api.telegram.org/bot{bot_token}/getUpdates'
    r = requests.get(url, timeout=8)
    d = r.json()
    if d.get('ok') and d.get('result'):
        updates = d['result']
        if updates:
            # 从最新消息获取 chat_id
            chat = updates[-1].get('message', {}).get('chat', {})
            return chat.get('id'), chat.get('type'), chat.get('title') or chat.get('username')
    return None, None, None

def send_message(bot_token, chat_id, text, parse_mode='Markdown'):
    """发送文字消息"""
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': parse_mode,
        'disable_web_page_preview': True,
    }
    r = requests.post(url, json=payload, timeout=10)
    d = r.json()
    if d.get('ok'):
        return True, d['result']['message_id']
    return False, d.get('description', 'Send failed')

def send_document(bot_token, chat_id, file_path, caption=None):
    """发送文件（HTML 日报）"""
    url = f'https://api.telegram.org/bot{bot_token}/sendDocument'
    with open(file_path, 'rb') as f:
        files = {'document': (os.path.basename(file_path), f, 'text/html')}
        data = {'chat_id': chat_id}
        if caption:
            data['caption'] = caption
        r = requests.post(url, data=data, files=files, timeout=30)
    d = r.json()
    if d.get('ok'):
        return True, d['result']['message_id']
    return False, d.get('description', 'Send failed')

def send_photo(bot_token, chat_id, file_path, caption=None):
    """发送图片（K线截图）"""
    url = f'https://api.telegram.org/bot{bot_token}/sendPhoto'
    with open(file_path, 'rb') as f:
        files = {'photo': (os.path.basename(file_path), f, 'image/png')}
        data = {'chat_id': chat_id}
        if caption:
            data['caption'] = caption
        r = requests.post(url, data=data, files=files, timeout=30)
    d = r.json()
    if d.get('ok'):
        return True, d['result']['message_id']
    return False, d.get('description', 'Send failed')

# ============ 日报摘要格式化 ============
def format_daily_report(data, strategy):
    """将数据格式化为 Telegram 消息"""
    btc = data.get('btc', {})
    fg = data.get('fear_greed', {})
    tech = data.get('technical', {})
    funding = data.get('funding', {})
    oi = data.get('oi', {})

    price = btc.get('price', 0)
    change = btc.get('change_24h', 0)
    rsi = tech.get('rsi', 0)
    macd = tech.get('macd_cross', 'N/A')
    ema20 = tech.get('ema20', 0)
    fear = fg.get('value', 0)
    fear_class = fg.get('classification', 'N/A')
    funding_rate = funding.get('rate', 0)
    ls_ratio = oi.get('long_short_ratio', 0)
    dir_tag = strategy.get('direction', 'WAIT')
    sl = strategy.get('stop_loss', 0)
    tp1 = strategy.get('tp1', 0)
    rr = strategy.get('rr_ratio', 0)

    change_icon = '\U0001f7e2' if change >= 0 else '\U0001f7e1'
    dir_icon = '\U0001f7e2 LONG' if dir_tag == 'LONG' else '\U0001f534 SHORT' if dir_tag == 'SHORT' else '\U0001f7e0 WAIT'

    msg = (
        "\u26a1 *BTC Daily Report* " + datetime.now().strftime('%m/%d') + "\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        + change_icon + " *BTC $" + f'{price:,.0f}' + "*  (" + ('+' if change >= 0 else '') + f'{change:.2f}%' + " 24h)\n"
        "\U0001f525 RSI: *" + f'{rsi:.1f}' + "* | MACD: *" + macd + "*\n"
        "\U0001f9f9 Fear&Greed: *" + str(fear) + "* (" + fear_class + ")\n"
        "\U0001f4b0 Funding: *" + f'{funding_rate:.4f}' + "%* | OI L/S: *" + f'{ls_ratio:.2f}' + "*\n\n"
        "\U0001f3af *Today's Strategy:* " + dir_icon + "\n"
        "  Entry: $" + f'{price:,.0f}' + "\n"
        "  SL: $" + f'{sl:,.0f}' + " | TP: $" + f'{tp1:,.0f}' + "\n"
        "  RR: *" + f'{rr:.1f}' + ":1*\n\n"
        "\U0001f4c8 EMA20: $" + f'{ema20:,.0f}' + "\n\n"
        "\U0001f6a8 *Full report:* https://mktrading.vip/btc/\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "\U0001f19a *MK Trading Bot v2.0*"
    )
    return msg

# ============ 主动推送函数（供主脚本调用） ============
def notify_telegram(data, strategy, report_path=None):
    """发送日报到 Telegram（由主脚本调用）"""
    config = load_config()
    if not config:
        print('[TG] No config found. Run with --setup-tg to configure.')
        return False, 'No config'

    bot_token = config.get('bot_token', '')
    chat_id = str(config.get('chat_id', ''))

    if not bot_token or not chat_id:
        print('[TG] Bot token or chat_id not configured.')
        return False, 'Missing config'

    # 发送摘要消息
    msg = format_daily_report(data, strategy)
    ok, result = send_message(bot_token, chat_id, msg)

    # 发送 HTML 文件
    if ok and report_path and os.path.exists(report_path):
        caption = '\U0001f4c4 BTC 日报 ' + datetime.now().strftime('%Y-%m-%d') + ' | MK Trading'
        doc_ok, doc_result = send_document(bot_token, chat_id, report_path, caption)
        if doc_ok:
            print('[TG] HTML report sent: message_id=' + str(doc_result))
        else:
            print('[TG] HTML report failed: ' + str(doc_result))

    return ok, result

# ============ 配置向导 ============
def setup_wizard():
    """交互式配置向导"""
    print('=== Telegram Bot Setup Wizard ===')
    print()
    print('Step 1: 创建一个 Telegram Bot')
    print('  1. 打开 @BotFather: https://t.me/BotFather')
    print('  2. 发送 /newbot')
    print('  3. 按提示输入 Bot 名称和用户名')
    print('  4. 复制 Bot Token（格式: 123456789:ABCdefGHI...）')
    print()
    bot_token = input('Paste Bot Token here: ').strip()

    ok, result = test_bot(bot_token)
    if not ok:
        print('X Invalid token:', result)
        return
    print('\u2705 Bot verified: ' + result)

    print()
    print('Step 2: 获取 Chat ID（你的账号或群组 ID）')
    print('  1. 先把你的 Bot 加入你的私聊或频道/群组')
    print('  2. 给 Bot 发一条消息（如果私聊）或等待有消息进来')
    print()

    chat_id, chat_type, chat_title = get_chat_id(bot_token)
    if chat_id:
        print('\u2705 Found chat: type=' + str(chat_type) + ', title=' + str(chat_title) + ', id=' + str(chat_id))
        use_id = input('Use this chat_id? (Y/n): ').strip().lower()
        if use_id != 'n':
            save_config(bot_token, str(chat_id))
            print('\u2705 Config saved!')
            # 发送测试消息
            test_ok, test_result = send_message(bot_token, str(chat_id),
                '\u2705 *MK BTC Bot Connected!*\nDaily reports will be sent here automatically.\n\n\U0001f916 Bot: ' + result)
            if test_ok:
                print('\u2705 Test message sent!')
            else:
                print('X Test message failed:', test_result)
            return

    print()
    print('Step 2b: 手动输入 Chat ID')
    print('  - 私聊: 打开 https://t.me/userinfobot 获取你的 user ID')
    print('  - 频道/群组: 用 @rawdatabot 或 @channelidbot 获取 ID')
    chat_id_input = input('Enter Chat ID: ').strip()
    if chat_id_input:
        save_config(bot_token, chat_id_input)
        print('\u2705 Config saved!')
        test_ok, test_result = send_message(bot_token, chat_id_input,
            '\u2705 *MK BTC Bot Connected!*\nDaily reports will be sent here.')
        if test_ok:
            print('\u2705 Test message sent!')
        else:
            print('X Test failed:', test_result)

if __name__ == '__main__':
    import sys
    if '--setup-tg' in sys.argv or len(sys.argv) == 1:
        setup_wizard()
    elif '--test' in sys.argv:
        config = load_config()
        if config:
            ok, result = send_message(config['bot_token'], str(config['chat_id']),
                '\u2705 Test from MK BTC Bot v2.0')
            print('Send result:', ok, result)
        else:
            print('No config. Run --setup-tg first.')
