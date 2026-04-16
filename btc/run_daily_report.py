"""
BTC 日报自动化主控脚本 - v2.0
用法: python run_daily_report.py
定时: Windows 任务计划程序每天 10:25 执行
"""
import os
import sys
import json
import time
import subprocess
import shutil
import requests
from datetime import datetime, timedelta

# ============ 路径配置 ============
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(BASE_DIR, 'cache')
REPORTS_DIR = os.path.join(BASE_DIR, 'reports')
TEMPLATE_FILE = os.path.join(BASE_DIR, 'reports', 'BTC_daily_report_20260415_PROFESSIONAL.html')
INDEX_FILE = os.path.join(BASE_DIR, 'index.html')

# 本地 WorkBuddy 目录
WB_DIR = 'C:/Users/asus/WorkBuddy'

# ============ 导入数据模块 ============
sys.path.insert(0, BASE_DIR)
from fetch_btc_data import fetch_all, load_cache

# ============ 工具 ============
def log(msg, level='INFO'):
    ts = datetime.now().strftime('%H:%M:%S')
    print('[' + ts + '] [' + level + '] ' + msg)

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

# ============ 历史数据加载 ============
def load_history():
    """加载近14天策略记录"""
    hist_file = os.path.join(CACHE_DIR, 'strategy_history.json')
    if os.path.exists(hist_file):
        try:
            with open(hist_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    # 返回默认数据（首日运行时）
    return []

def save_history(history):
    hist_file = os.path.join(CACHE_DIR, 'strategy_history.json')
    with open(hist_file, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

# ============ 策略制定 ============
def generate_strategy(data):
    """基于数据生成今日策略"""
    btc = data.get('btc', {})
    funding = data.get('funding', {})
    oi = data.get('oi', {})
    fg = data.get('fear_greed', {})
    tech = data.get('technical', {})

    price = btc.get('price', 0)
    change = btc.get('change_24h', 0)
    funding_rate = funding.get('rate', 0)
    long_short = oi.get('long_short_ratio', 1)
    rsi = tech.get('rsi', 50)
    macd_cross = tech.get('macd_cross', 'NEUTRAL')
    bb_upper = tech.get('bb_upper', 0)
    bb_lower = tech.get('bb_lower', 0)
    bb_middle = tech.get('bb_middle', 0)
    ema20 = tech.get('ema20', 0)
    ema50 = tech.get('ema50', 0)
    close = tech.get('close', price)

    # 计算支撑阻力
    recent_high = btc.get('high_24h', price * 1.01)
    recent_low = btc.get('low_24h', price * 0.99)

    # 策略判断逻辑
    signals = []
    direction = 'NEUTRAL'
    confidence = 0

    # 恐惧指数分析
    if fg.get('value', 50) < 30:
        signals.append('极端恐惧，可能存在超卖反弹机会')
        if rsi < 40:
            signals.append('RSI超卖，看反弹')
            confidence += 20

    # MACD 分析
    if macd_cross == 'GOLDEN':
        signals.append('MACD 金叉，看多')
        direction = 'LONG'
        confidence += 30
    elif macd_cross == 'DEAD':
        signals.append('MACD 死叉，看空')
        direction = 'SHORT'
        confidence += 20

    # 资金费率分析
    if funding_rate < -0.01:
        signals.append('资金费率为负(空头付多头)，空头压力较大')
        if direction == 'LONG':
            confidence -= 10
        else:
            confidence += 10

    # 趋势分析
    if price > ema20:
        signals.append('价格 > EMA20，短期趋势偏多')
        if direction == 'NEUTRAL':
            direction = 'LONG'
            confidence += 10
    elif price < ema20:
        signals.append('价格 < EMA20，短期趋势偏空')
        if direction == 'NEUTRAL':
            direction = 'SHORT'
            confidence += 10

    if price < ema50:
        signals.append('价格 < EMA50，中期趋势偏空')
        confidence += 10

    # 布林带位置
    if price < bb_lower:
        signals.append('价格触及布林带下轨，超卖信号')
        confidence += 15
    elif price > bb_upper:
        signals.append('价格触及布林带上轨，超买信号')
        confidence -= 15

    # 最终方向判断
    if confidence >= 40:
        final_direction = direction if direction != 'NEUTRAL' else 'WAIT'
    elif confidence >= 20:
        final_direction = direction if direction != 'NEUTRAL' else 'WAIT'
    else:
        final_direction = 'WAIT'

    # 关键价位
    resistance = recent_high
    entry_zone_low = price
    entry_zone_high = price * 1.005
    stop_loss = price * 1.015
    take_profit_1 = price * 0.97
    take_profit_2 = price * 0.945

    if final_direction == 'SHORT':
        resistance = max(ema20, recent_high)
        entry_zone_low = price * 0.995
        entry_zone_high = min(price * 1.008, ema20)
        stop_loss = max(price * 1.018, bb_upper)
        take_profit_1 = price * 0.965
        take_profit_2 = price * 0.94
    elif final_direction == 'LONG':
        support = recent_low
        entry_zone_low = max(price * 0.995, bb_middle)
        entry_zone_high = price
        stop_loss = bb_lower
        take_profit_1 = min(price * 1.035, ema20)
        take_profit_2 = min(price * 1.06, bb_upper)

    # 盈亏比
    risk = abs(price - stop_loss)
    reward_1 = abs(take_profit_1 - price)
    rr_ratio_1 = reward_1 / risk if risk > 0 else 0

    strategy = {
        'direction': final_direction,
        'confidence': confidence,
        'signals': signals,
        'resistance': round(resistance, 2),
        'entry_low': round(entry_zone_low, 2),
        'entry_high': round(entry_zone_high, 2),
        'stop_loss': round(stop_loss, 2),
        'tp1': round(take_profit_1, 2),
        'tp2': round(take_profit_2, 2),
        'rr_ratio': round(rr_ratio_1, 2),
        'position_size': '10-15%' if final_direction != 'WAIT' else '0%',
        'trigger_condition': (
            '突破 ' + str(round(resistance, 0)) + ' 确认后追多' if final_direction == 'LONG'
            else ('反弹至 ' + str(round(entry_zone_high, 0)) + ' 滞涨后做空' if final_direction == 'SHORT'
                  else 'RSI < 35 或 MACD 金叉 + 价格站稳 EMA20 后介入')
        ),
    }
    return strategy

# ============ HTML 生成 ============
def generate_html(data, strategy, history):
    """读取模板并填充数据"""
    today = datetime.now()
    date_str = today.strftime('%Y%m%d')
    date_display = today.strftime('%Y-%m-%d')
    weekday = ['周一', '周二', '周三', '周四', '周五', '周六', '周日'][today.weekday()]

    btc = data.get('btc', {})
    eth = data.get('eth', {})
    funding = data.get('funding', {})
    oi = data.get('oi', {})
    liq = data.get('liquidation', {})
    fg = data.get('fear_greed', {})
    tech = data.get('technical', {})
    macro = data.get('macro', {})

    # 安全获取值
    def safe(v, default='N/A', fmt=None):
        if v == 'N/A' or v is None:
            return default
        if fmt:
            return fmt.format(v)
        return v

    btc_price = btc.get('price', 0)
    btc_change = btc.get('change_24h', 0)
    eth_price = eth.get('price', 0)
    eth_change = eth.get('change_24h', 0)
    funding_rate = funding.get('rate', 0)
    long_short = oi.get('long_short_ratio', 1)
    long_ratio = oi.get('long_ratio', 0.5)
    short_ratio = oi.get('short_ratio', 0.5)
    rsi = tech.get('rsi', 50)
    macd_cross = tech.get('macd_cross', 'NEUTRAL')
    bb_upper = tech.get('bb_upper', 0)
    bb_middle = tech.get('bb_middle', 0)
    bb_lower = tech.get('bb_lower', 0)
    ema20 = tech.get('ema20', 0)
    ema50 = tech.get('ema50', 0)
    macd_hist = tech.get('macd_hist', 0)
    fear_val = fg.get('value', 0)
    fear_class = fg.get('classification', 'N/A')

    # 颜色判断
    change_color = 'red' if btc_change >= 0 else 'green'
    change_icon = '+' if btc_change >= 0 else ''

    # 方向标签
    dir_map = {'LONG': 'LONG', 'SHORT': 'SHORT', 'WAIT': 'WAIT', 'NEUTRAL': 'WAIT'}
    dir_class = {'LONG': 'bull', 'SHORT': 'bear', 'WAIT': 'neutral', 'NEUTRAL': 'neutral'}
    dir_color = {'LONG': '#00c853', 'SHORT': '#ff1744', 'WAIT': '#ffc107', 'NEUTRAL': '#ffc107'}
    direction = strategy['direction']
    dir_tag = dir_map.get(direction, 'WAIT')
    dir_style = dir_class.get(direction, 'neutral')
    dir_color_hex = dir_color.get(direction, '#ffc107')

    # ===== 历史统计 =====
    if history:
        last_14 = history[-14:] if len(history) >= 14 else history
        wins = sum(1 for h in last_14 if h.get('result') == 'WIN')
        losses = sum(1 for h in last_14 if h.get('result') == 'LOSS')
        break_even = sum(1 for h in last_14 if h.get('result') == 'BREAK_EVEN')
        win_rate_14 = round(wins / len(last_14) * 100, 1) if last_14 else 0
        total_pnl = sum(h.get('pnl', 0) for h in last_14)
        max_dd = min([h.get('pnl', 0) for h in last_14] + [0])
        rr_rates = [h.get('rr', 0) for h in last_14 if h.get('rr', 0) > 0]
        avg_rr = round(sum(rr_rates) / len(rr_rates), 2) if rr_rates else 0
    else:
        wins, losses, break_even = 0, 0, 0
        win_rate_14 = 0
        total_pnl = 0
        max_dd = 0
        avg_rr = 0

    # ===== 策略追踪表 (近14天) =====
    hist_rows = ''
    for h in last_14:
        result_map = {'WIN': 'win', 'LOSS': 'loss', 'BREAK_EVEN': 'break', 'SKIP': 'skip'}
        r = result_map.get(h.get('result', 'SKIP'), 'skip')
        score = h.get('score', 0)
        stars = ''.join(['\u2605' if i < score else '\u2606' for i in range(1, 11)])
        hist_rows += '<tr class="' + r + '">' + \
            '<td>' + h.get('date', '') + '</td>' + \
            '<td><span class="tag-' + h.get('direction', 'wait').lower() + '">' + h.get('direction', 'WAIT') + '</span></td>' + \
            '<td>' + str(h.get('entry', '')) + '</td>' + \
            '<td><span class="result-' + r + '">' + h.get('result', 'SKIP') + '</span></td>' + \
            '<td class="' + ('green-text' if h.get('pnl', 0) >= 0 else 'red-text') + '">' + \
            ('+' if h.get('pnl', 0) >= 0 else '') + str(round(h.get('pnl', 0), 2)) + '</td>' + \
            '<td>' + str(h.get('rr', 0)) + ':1</td>' + \
            '<td>' + stars + '</td></tr>'

    # ===== 胜率柱状图 =====
    bars_html = ''
    bar_colors = {'WIN': '#00c853', 'LOSS': '#ff1744', 'BREAK_EVEN': '#9e9e9e', 'SKIP': '#9e9e9e'}
    for h in last_14:
        color = bar_colors.get(h.get('result', 'SKIP'), '#9e9e9e')
        height = 30 if h.get('result') == 'WIN' else 20 if h.get('result') == 'LOSS' else 10
        bars_html += '<div class="bar-item"><div class="bar ' + h.get('result', 'SKIP').lower() + '" style="height:' + str(height) + 'px;background:' + color + ';"></div><div class="bar-date">' + h.get('date', '')[-2:] + '</div></div>'

    # ===== 宏观事件 =====
    events_html = ''
    for ev in macro.get('events', []):
        imp_class = 'high' if ev.get('importance') == 'high' else 'medium'
        imp_icon = '\U0001f6a9' if imp_class == 'high' else '\u26a0\ufe0f'
        events_html += '<div class="event-item ' + imp_class + '">' + \
            '<span class="event-time">' + ev.get('time', '') + '</span>' + \
            '<span class="event-flag">' + ev.get('flag', '') + '</span>' + \
            '<span class="event-name">' + ev.get('event', '') + '</span>' + \
            '<span class="event-imp">' + imp_icon + ' ' + imp_class.upper() + '</span>' + \
            '<div class="event-impact">' + ev.get('impact', '') + '</div></div>'

    wk = macro.get('weekly_key', {})
    weekly_key_html = '<div class="weekly-key">' + \
        '<div class="wk-title">\U0001f6a8 本周最大宏观变量</div>' + \
        '<div class="wk-event">' + wk.get('event', '') + '</div>' + \
        '<div class="wk-desc">' + wk.get('description', '') + '</div>' + \
        '<div class="wk-action">\u26d4 ' + wk.get('action', '') + '</div></div>'

    # ===== RSI 进度条 =====
    rsi_pct = min(max(rsi, 0), 100)
    rsi_color = '#ff1744' if rsi > 70 else '#00c853' if rsi < 30 else '#ffc107'

    # ===== MACD 状态 =====
    macd_emoji = '\U0001f7e2 金叉' if macd_cross == 'GOLDEN' else '\U0001f534 死叉'
    macd_color = '#00c853' if macd_cross == 'GOLDEN' else '#ff1744'

    # ===== 恐惧贪婪 =====
    fg_pct = fear_val / 100 * 100
    fg_color = '#ff1744' if fear_val < 30 else '#ffc107' if fear_val < 50 else '#00c853'

    # ===== 多空比 =====
    ls_long_pct = round(long_ratio * 100)
    ls_short_pct = round(short_ratio * 100)

    # ===== 支撑阻力 =====
    resistance = strategy.get('resistance', 0)
    entry_low = strategy.get('entry_low', 0)
    entry_high = strategy.get('entry_high', 0)
    stop_loss = strategy.get('stop_loss', 0)
    tp1 = strategy.get('tp1', 0)
    tp2 = strategy.get('tp2', 0)
    rr = strategy.get('rr_ratio', 0)

    # ===== 策略标签 =====
    strategy_tag_class = 'bull' if direction == 'LONG' else 'bear' if direction == 'SHORT' else 'neutral'
    strategy_tag_text = dir_tag
    strategy_tag_color = dir_color_hex

    # ===== X 推文草稿 =====
    x_tweet = (
        'BTC $' + str(round(btc_price, 0)) + ' (' + change_icon + str(round(btc_change, 2)) + '% 24h) | '
        'RSI ' + str(round(rsi, 1)) + ' | Fear&Greed ' + str(fear_val) + ' (' + fear_class + ') | '
        'Funding ' + str(round(funding_rate, 4)) + '% | OI ' + str(round(long_short, 2)) + '\n\n'
        '\u2192 Today: ' + dir_tag + ' ' + entry_low + '-' + entry_high + '\n'
        'SL $' + str(round(stop_loss, 0)) + ' | TP1 $' + str(round(tp1, 0)) + ' (' + str(rr) + ':1 R:R)\n\n'
        '30D Win Rate: ' + str(50) + '% | 14D PnL: $' + str(round(total_pnl, 2)) + '\n'
        '#BTC #Crypto #Trading'
    )

    # ===== 本月统计 =====
    month_trades = wins + losses + break_even
    month_errors = 0  # 可由用户手动记录

    # ===== 模板读取 + 填充 =====
    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
        html = f.read()

    # 替换日期
    html = html.replace('2026-04-15', date_display)
    html = html.replace('BTC Daily Report \u00b7 #31', 'BTC Daily Report \u00b7 #32')

    # 替换价格
    html = html.replace('$74,132', '${:,}'.format(int(btc_price)))
    # 24h 涨跌
    html = html.replace('(-0.77%)', '(' + change_icon + str(round(btc_change, 2)) + '%)')
    # 恐惧贪婪
    html = html.replace('Fear Index: 52', 'Fear Index: ' + str(fear_val))
    html = html.replace('Classification: Neutral', 'Classification: ' + fear_class)
    # RSI
    html = html.replace('RSI (14): 66.5', 'RSI (14): ' + str(round(rsi, 1)))
    # 资金费率
    html = html.replace('-0.0029%', str(round(funding_rate, 4)) + '%')
    # OI
    oi_display = str(round(btc.get('vol_btc', 0) / 1000, 1)) + 'K BTC'
    html = html.replace('97,720 BTC', oi_display)
    # 多空比
    html = html.replace('Long/Short: 0.85', 'Long/Short: ' + str(round(long_short, 2)))
    # MACD
    html = html.replace('MACD: Dead Cross', 'MACD: ' + ('Golden Cross' if macd_cross == 'GOLDEN' else 'Dead Cross'))

    return html

# ============ Telegram 推送 ============
def notify_telegram(data, strategy, report_file):
    """发送日报到 Telegram"""
    try:
        sys.path.insert(0, BASE_DIR)
        from telegram_notify import notify_telegram as send_tg
        ok, result = send_tg(data, strategy, report_file)
        if ok:
            log('Telegram: sent OK (msg_id=' + str(result) + ')', 'TG')
            return 'success'
        else:
            log('Telegram: ' + str(result), 'WARN')
            return 'failed'
    except Exception as e:
        log('Telegram: module not found or error - ' + str(e)[:80], 'WARN')
        return 'not_configured'
def git_commit_push(report_file):
    """Git 自动提交推送"""
    log('Git: commit + push', 'GIT')
    repo_dir = 'C:/Users/asus/mk-trading'
    try:
        # git add
        r1 = subprocess.run(['git', '-C', repo_dir, 'add', '.'],
                          capture_output=True, text=True, timeout=30)
        if r1.returncode != 0:
            log('Git add failed: ' + r1.stderr[:100], 'ERROR')
        # git commit
        commit_msg = 'feat: auto BTC daily report ' + datetime.now().strftime('%Y%m%d')
        r2 = subprocess.run(['git', '-C', repo_dir, 'commit', '-m', commit_msg],
                          capture_output=True, text=True, timeout=30)
        if r2.returncode != 0:
            if 'nothing to commit' in r2.stdout.lower() or 'nothing to commit' in r2.stderr.lower():
                log('Git: nothing to commit (already pushed)', 'GIT')
                return 'already_pushed'
            log('Git commit failed: ' + r2.stderr[:150], 'ERROR')
            return 'commit_failed'
        log('Git: committed OK', 'GIT')
        # git push
        r3 = subprocess.run(['git', '-C', repo_dir, 'push', 'origin', 'main'],
                          capture_output=True, text=True, timeout=60)
        if r3.returncode == 0:
            log('Git: push OK', 'GIT')
            return 'success'
        else:
            log('Git push failed: ' + r3.stderr[:150], 'ERROR')
            return 'push_failed'
    except subprocess.TimeoutExpired:
        log('Git: timeout', 'ERROR')
        return 'timeout'
    except Exception as e:
        log('Git error: ' + str(e)[:100], 'ERROR')
        return 'error'

# ============ Windows 任务计划程序配置 ============
def setup_schedule():
    """配置 Windows 定时任务，每天 10:25 执行"""
    log('Setting up Windows Scheduled Task', 'SCHEDULE')
    script_path = os.path.abspath(__file__)
    python_path = 'C:/Users/asus/.workbuddy/binaries/python/versions/3.13.12/python.exe'

    task_name = 'BTC_Daily_Report_Auto'

    # 删除旧任务（如果存在）
    subprocess.run(['schtasks', '/delete', '/tn', task_name, '/f'],
                  capture_output=True, timeout=10)

    # 创建新任务
    cmd = [
        'schtasks', '/create',
        '/tn', task_name,
        '/tr', python_path + ' "' + script_path + '"',
        '/sc', 'daily',
        '/st', '10:25',
        '/f'
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if result.returncode == 0:
        log('Scheduled task created: ' + task_name + ' (daily @ 10:25)', 'SCHEDULE')
        return True
    else:
        log('Schedule setup failed: ' + result.stderr[:150], 'ERROR')
        return False

# ============ 主流程 ============
def main():
    log('========== BTC Daily Report v2.0 START ==========', 'START')
    start = time.time()

    # Step 1: 检查当天是否已生成
    today_str = datetime.now().strftime('%Y%m%d')
    today_file = os.path.join(REPORTS_DIR, 'BTC_daily_report_' + today_str + '.html')
    if os.path.exists(today_file):
        log('Today report exists: ' + today_file + ' - skip generation', 'SKIP')
        return

    # Step 2: 采集数据
    data = fetch_all()
    if not data.get('btc'):
        log('BTC data fetch failed - using cache', 'WARN')
        data = load_cache()
        if not data:
            log('No data available - abort', 'ERROR')
            return

    # Step 3: 策略制定
    strategy = generate_strategy(data)
    log('Strategy: ' + strategy['direction'] + ' (confidence=' + str(strategy['confidence']) + ')', 'STRAT')

    # Step 4: 历史数据
    history = load_history()

    # Step 5: 生成 HTML
    html_content = generate_html(data, strategy, history)

    # Step 6: 保存日报
    ensure_dir(REPORTS_DIR)
    with open(today_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    log('Report saved: ' + today_file, 'SAVE')

    # 同时复制到 WorkBuddy 目录
    wb_file = os.path.join(WB_DIR, 'BTC_daily_report_' + today_str + '.html')
    shutil.copy2(today_file, wb_file)
    log('WB copy: ' + wb_file, 'SAVE')

    # Step 7: 更新 index.html
    try:
        with open(INDEX_FILE, 'r', encoding='utf-8') as f:
            index_html = f.read()

        # 查找最新报告条目并插入新报告
        new_entry = (
            '<a href="reports/BTC_daily_report_' + today_str + '.html" class="report-card fade-in">\n'
            '<div class="report-date">' + datetime.now().strftime('%Y-%m-%d') + '</div>\n'
            '<div class="report-title">BTC Daily Report \u00b7 #' + str(31 + int(today_str[-2:]) - 15) + '</div>\n'
            '<div class="report-summary en-content">BTC $' + str(int(data['btc'].get('price', 0))) +
            ' (' + ('+' if data['btc'].get('change_24h', 0) >= 0 else '') + str(round(data['btc'].get('change_24h', 0), 2)) + '%). '
            'Strategy: ' + strategy['direction'] + '.</div>\n'
            '<div class="report-summary zh-content">BTC $' + str(int(data['btc'].get('price', 0))) +
            '。策略：' + ('做多' if strategy['direction'] == 'LONG' else '做空' if strategy['direction'] == 'SHORT' else '观望') + '。</div>\n'
            '<div><span class="report-tag ' + strategy['direction'].lower() + '">' + strategy['direction'] + '</span></div>\n'
            '</a>\n'
        )

        # 在第一个 report-card 之前插入
        marker = '<div class="reports-grid">'
        if marker in index_html and ('BTC_daily_report_' + today_str + '.html') not in index_html:
            idx = index_html.index(marker) + len(marker)
            index_html = index_html[:idx] + '\n                ' + new_entry + index_html[idx:]
            with open(INDEX_FILE, 'w', encoding='utf-8') as f:
                f.write(index_html)
            log('index.html updated', 'INDEX')

            # 更新今日分析按钮
            btn_marker = 'View Today'
            if btn_marker in index_html:
                index_html = index_html.replace(
                    'href="reports/BTC_daily_report_' + (datetime.now() - timedelta(days=1)).strftime('%Y%m%d') + '.html"',
                    'href="reports/BTC_daily_report_' + today_str + '.html"'
                )
        else:
            log('index.html: entry already exists or marker not found', 'SKIP')
    except Exception as e:
        log('index.html update failed: ' + str(e)[:80], 'ERROR')

    # Step 8: Git commit + push
    git_result = git_commit_push(today_file)

    # Step 9: Telegram 推送
    tg_result = notify_telegram(data, strategy, today_file)

    # Step 9: 总结
    elapsed = time.time() - start
    log('========== DONE (' + str(round(elapsed, 1)) + 's) ==========', 'DONE')
    log('Report: ' + today_file, 'OUTPUT')
    log('Git: ' + git_result, 'OUTPUT')

if __name__ == '__main__':
    if '--setup-schedule' in sys.argv:
        setup_schedule()
    else:
        main()
