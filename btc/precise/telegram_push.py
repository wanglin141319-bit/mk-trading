#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram 推送模块 —— BTC 精准日报
================================================
用途 : 把当日日报推送到 Telegram（频道 / 群组 / 私聊，支持多目标群发）
凭证 : 存放在【仓库外】的私密文件 .workbuddy/btc_precise/telegram_config.json
       （.workbuddy/ 已被 .gitignore 排除，绝不会进公开仓库）
代理 : 本机 Telegram API 直连不可达（GFW），需经本地代理（clash 等）。
       优先用配置里的 proxy，未配置则自动扫描常见代理端口。
用法 : from telegram_push import push
       push(D, S, W, num, report_path)
"""
import os, json, socket, time, urllib3
from datetime import datetime, timezone, timedelta

urllib3.disable_warnings()
try:
    import requests
except ImportError:
    raise SystemExit("[TG][FATAL] 缺少 requests 模块")

# ================= 路径 =================
BASE = os.path.dirname(os.path.abspath(__file__))          # btc/precise
REPO = os.path.dirname(os.path.dirname(BASE))              # mk-trading
PRIV = os.path.join(REPO, '.workbuddy', 'btc_precise')     # 私密目录（gitignore）
CFG_PATH = os.path.join(PRIV, 'telegram_config.json')
CST = timezone(timedelta(hours=8))

# 常见代理端口（用于自动探测；clash/v2ray 默认端口）
PROXY_PORTS = [33210, 33211, 7890, 7897, 7891, 10809, 10808, 1080, 2080, 4780, 8889, 7899]

def log(m, tag='TG'):
    print(f"[{datetime.now().strftime('%H:%M:%S')}][{tag}] {m}", flush=True)

# ================= 配置 =================
def load_config():
    """读取私密配置；兼容旧的单 chat_id 格式"""
    if not os.path.exists(CFG_PATH):
        return None
    try:
        cfg = json.load(open(CFG_PATH, encoding='utf-8'))
    except Exception as e:
        log(f'配置读取失败：{e}', 'ERROR')
        return None
    if 'chat_ids' not in cfg:
        cfg['chat_ids'] = [cfg['chat_id']] if cfg.get('chat_id') else []
    cfg['chat_ids'] = [str(c) for c in cfg.get('chat_ids', [])]
    return cfg

def save_config(cfg):
    os.makedirs(PRIV, exist_ok=True)
    json.dump(cfg, open(CFG_PATH, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

# ================= 代理 =================
def _port_open(port, host='127.0.0.1'):
    s = socket.socket(); s.settimeout(0.4)
    try:
        return s.connect_ex((host, port)) == 0
    finally:
        s.close()

def _proxy_dict(url):
    return {'http': url, 'https': url}

def _probe(url):
    """测试某代理能否到达 Telegram"""
    try:
        r = requests.get('https://api.telegram.org', timeout=8,
                         proxies=_proxy_dict(url), verify=False)
        return r.status_code < 500
    except Exception:
        return False

def resolve_proxies(cfg):
    """确定可用代理：配置优先 → 端口扫描 → 直连(None)
       返回 (proxies_dict_or_None, 描述)"""
    p = (cfg or {}).get('proxy')
    if p:
        if _probe(p):
            return _proxy_dict(p), p
        log(f'配置代理 {p} 不通，转自动探测', 'WARN')
    for port in PROXY_PORTS:
        if _port_open(port):
            for scheme in ('http', 'socks5h'):
                url = f'{scheme}://127.0.0.1:{port}'
                try:
                    if _probe(url):
                        log(f'自动探测到可用代理 {url}', 'OK')
                        return _proxy_dict(url), url
                except Exception:
                    continue
    log('未探测到可用代理，尝试直连', 'WARN')
    return None, 'direct'

# ================= API =================
def _call(cfg, proxies, method, data=None, files=None, timeout=20):
    url = f"https://api.telegram.org/bot{cfg['bot_token']}/{method}"
    try:
        if files:
            r = requests.post(url, data=data or {}, files=files,
                              timeout=timeout, proxies=proxies, verify=False)
        else:
            r = requests.post(url, json=data or {},
                              timeout=timeout, proxies=proxies, verify=False)
        d = r.json()
        return bool(d.get('ok')), d
    except Exception as e:
        return False, {'description': str(e)[:160]}

def send_text(cfg, proxies, chat_id, text, disable_preview=True):
    ok, d = _call(cfg, proxies, 'sendMessage', {
        'chat_id': chat_id, 'text': text,
        'parse_mode': 'HTML', 'disable_web_page_preview': disable_preview})
    mid = d.get('result', {}).get('message_id') if ok else None
    return ok, (mid or d.get('description'))

def send_document(cfg, proxies, chat_id, path, caption=None):
    if not path or not os.path.exists(path):
        return False, 'file not found'
    fn = os.path.basename(path)
    with open(path, 'rb') as f:
        files = {'document': (fn, f, 'text/html')}
        data = {'chat_id': chat_id}
        if caption:
            data['caption'] = caption
        ok, d = _call(cfg, proxies, 'sendDocument', data, files=files, timeout=60)
    mid = d.get('result', {}).get('message_id') if ok else None
    return ok, (mid or d.get('description'))

# ================= 消息构建 =================
def _esc(s):
    return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def build_message(D, S, W, num, today, report_url):
    """构建频道推送文案（HTML 模式）"""
    price = S['price']
    chg = D['spot']['change_24h_pct']
    up = chg >= 0
    dot = '🟢' if up else '🔴'
    arrow = '▲' if up else '▼'

    dmap = {'LONG': ('🟢 做多 LONG', 'bull'), 'SHORT': ('🔴 做空 SHORT', 'bear'), 'WAIT': ('🟡 观望 WAIT', 'wait')}
    dtxt, _ = dmap[S['direction']]

    fg = D.get('fng', {})
    fgcn = {'Extreme Fear': '极度恐惧', 'Fear': '恐惧', 'Neutral': '中性',
            'Greed': '贪婪', 'Extreme Greed': '极度贪婪'}.get(fg.get('cls', ''), fg.get('cls', 'N/A'))
    fg_icon = '😱' if fg.get('value', 50) >= 75 else '😃' if fg.get('value', 50) >= 55 \
        else '😐' if fg.get('value', 50) >= 45 else '😰' if fg.get('value', 50) >= 25 else '😨'

    h4 = None  # RSI/MACD 展示用（由调用方传 A 亦可，此处简化取日线）
    d1 = (D.get('_tf') or {}).get('d1') or {}
    rsi_txt = f"{d1['rsi']:.1f}" if d1.get('rsi') else 'N/A'
    macd_txt = d1.get('macd', {}).get('state', 'N/A') if d1 else 'N/A'

    fdr = D['futures']['funding_rate']
    q = D.get('quanto', 0.0001)
    st = D['stats'][-1] if D.get('stats') else {}
    oi = st.get('open_interest', 0) * q if st.get('open_interest') else 0

    def u(v, d=0):
        try: return f"${v:,.{d}f}"
        except Exception: return 'N/A'

    wr = f"{W['rate']}%" if W.get('rate') is not None else '—'

    lines = [
        f"⚡ <b>BTC 合约日报 #{num}</b> · {today[:4]}-{today[4:6]}-{today[6:]}",
        "━━━━━━━━━━━━━━━━━━━━",
        "",
        f"{dot} <b>BTC {u(price)}</b>  {arrow} {chg:+.2f}% <i>(24h)</i>",
        f"🔥 RSI {rsi_txt} · MACD {macd_txt}",
        f"{fg_icon} 恐惧贪婪 <b>{fg.get('value','N/A')}</b>（{fgcn}） · 资金费 {fdr:.4f}%",
        f"📦 未平仓 OI <b>{oi:,.0f} BTC</b>",
        "",
        f"🎯 <b>今日策略：{dtxt}</b>（信心 {S['confidence']}）",
        f"├ 入场：<b>{u(S['entry_low'])} – {u(S['entry_high'])}</b>",
        f"├ 止损：{u(S['stop'])}",
        f"├ 止盈：TP1 {u(S['tp1'])} / TP2 {u(S['tp2'])}",
        f"└ 盈亏比 {S['rr']:.1f}:1 · 仓位 {S['position']}",
        "",
        f"⚖️ 多空评分 多 {S['score_long']} : 空 {S['score_short']}",
        f"✅ 触发：{_esc(S['trigger'])}",
        f"⚠️ 失效：{_esc(S['invalid'])}",
        "",
        f"📈 完整日报 → {report_url}",
        f"📊 历史胜率 {wr}（{W['wins']}/{W['total']}）",
        "━━━━━━━━━━━━━━━━━━━━",
        "🤖 MK Trading Bot · 数据 Gate.io",
    ]
    return "\n".join(lines)

# ================= 推送入口 =================
def push(D, S, W, num, today, report_path=None, report_url=None, A=None, cfg=None):
    """推送日报到所有配置的目标。返回 dict 结果。失败不抛异常（不影响主流程）"""
    cfg = cfg or load_config()
    if not cfg:
        return {'ok': False, 'reason': 'no config', 'sent': []}
    if cfg.get('enabled') is False:
        return {'ok': False, 'reason': 'disabled', 'sent': []}
    tok = cfg.get('bot_token')
    if not tok or not cfg.get('chat_ids'):
        return {'ok': False, 'reason': 'missing token/chat', 'sent': []}

    proxies, pdesc = resolve_proxies(cfg)
    log(f'代理：{pdesc}')

    if A:
        D['_tf'] = A
    url = report_url or f"https://mktrading.vip/btc/reports/BTC_daily_report_{today}.html"
    text = build_message(D, S, W, num, today, url)

    sent, ok_any = [], False
    for cid in cfg['chat_ids']:
        ok, info = send_text(cfg, proxies, cid, text)
        sent.append({'chat_id': cid, 'ok': ok, 'info': str(info)})
        if ok:
            ok_any = True
            log(f'已推送 → {cid} (msg_id={info})', 'OK')
        else:
            log(f'推送失败 → {cid}: {info}', 'ERROR')

        # 可选：附上 HTML 文件
        if ok and cfg.get('attach_html') and report_path:
            dok, dinfo = send_document(cfg, proxies, cid, report_path,
                                       caption=f"📄 BTC 日报 {today[:4]}-{today[4:6]}-{today[6:]}")
            sent[-1]['doc'] = {'ok': dok, 'info': str(dinfo)}

    return {'ok': ok_any, 'proxy': pdesc, 'sent': sent}

# ================= 独立测试 =================
if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser(description='Telegram 推送自检')
    ap.add_argument('--test', action='store_true', help='发送一条连通性测试消息')
    ap.add_argument('--check', action='store_true', help='仅检查 token/chat/代理')
    a = ap.parse_args()
    cfg = load_config()
    if not cfg:
        print('未找到配置：', CFG_PATH); raise SystemExit(1)
    proxies, pdesc = resolve_proxies(cfg)
    ok, d = _call(cfg, proxies, 'getMe')
    print('代理:', pdesc)
    print('getMe:', 'OK -> @' + d.get('result', {}).get('username', '?') if ok else f'FAIL {d.get("description")}')
    for cid in cfg['chat_ids']:
        ok2, d2 = _call(cfg, proxies, 'getChat', {'chat_id': cid})
        c = d2.get('result', {})
        print(f'  chat {cid}: ' + (f"{c.get('type')} 「{c.get('title')}」 @{c.get('username')}" if ok2 else f"FAIL {d2.get('description')}"))
    if a.test:
        for cid in cfg['chat_ids']:
            ok3, info = send_text(cfg, proxies, cid,
                                  '✅ <b>MK Trading Bot 已接通</b>\nBTC 精准日报将每日自动推送至此。')
            print(f'  测试消息 → {cid}: ' + ('OK' if ok3 else f'FAIL {info}'))
