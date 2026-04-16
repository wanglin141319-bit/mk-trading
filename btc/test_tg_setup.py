import requests, warnings, json, os
warnings.filterwarnings('ignore')

TOKEN = '8626387493:AAE2XCzMzmhDiWRaGKVEjrj2EGLPsDN22-Q'
CHAT_ID = '8167434886'

# Save config
config = {'bot_token': TOKEN, 'chat_id': CHAT_ID}
config_path = os.path.join(os.path.dirname(__file__), 'telegram_config.json')
with open(config_path, 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)
print('Config saved to', config_path)

# Test send
msg = '[MK BTC Alert] Bot configured successfully!'
r = requests.post(
    f'https://api.telegram.org/bot{TOKEN}/sendMessage',
    json={'chat_id': CHAT_ID, 'text': msg},
    timeout=8
)
result = r.json()
print('Status:', r.status_code)
print('OK:', result.get('ok'))
if result.get('ok'):
    print('Message ID:', result['result']['message_id'])
else:
    print('Error:', result)
