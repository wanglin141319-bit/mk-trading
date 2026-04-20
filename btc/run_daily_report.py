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

def auto_resolve_yesterday(data, prev_strategy, history):
    """
    【核心逻辑 - v2.2 修复版】
    
    ⚠️ 关键原则：必须先判断"进场是否触发"，再判断SL/TP。
    "等回踩未触发"和"已触发但止损/未达止盈"是完全不同的两件事。
    
    判断规则：
    第一步：判断进场区间是否被价格穿过（触发确认）
      - 做多：low <= entry_high AND high >= entry_low → 已触发
      - 空头：同上逻辑
    第二步：如果已触发，再按优先级判断结果
      - 多头：low < SL  → LOSS(止损)
             high >= TP2 → WIN(TP2)
             high >= TP1 → WIN_TP1(TP1)
             否则 → TRIGGERED_NO_TP（已触发，但未达止盈也未止损）
      - 空头：high > SL  → LOSS
             low <= TP2   → WIN
             low <= TP1   → WIN_TP1
             否则 → TRIGGERED_NO_TP
    第三步：如果未触进场区
      → BREAK_EVEN（真正的"等回踩未触发"）
    """
    if not prev_strategy or prev_strategy.get('direction') == 'WAIT' or prev_strategy.get('direction') == 'NEUTRAL':
        return history

    sl = prev_strategy.get('stop_loss', 0)
    tp1 = prev_strategy.get('tp1', 0)
    tp2 = prev_strategy.get('tp2', 0)
    entry_low = prev_strategy.get('entry_low', 0)
    entry_high = prev_strategy.get('entry_high', 0)

    # 昨天策略执行日当天的24h价格区间（用今天获取到的昨日K线数据）
    # 注意：data 里包含的是"当前最新数据"，对于复盘昨天需要用昨日的OHLC
    # 这里用 data 中 btc 的 high_24h / low_24h 代表昨日实际波动
    day_high = data.get('btc', {}).get('high_24h', 0)
    day_low = data.get('btc', {}).get('low_24h', 0)

    direction = prev_strategy.get('direction', 'LONG')

    # ========== 第一步：进场触发判断 ==========
    triggered = False
    if entry_low > 0 and entry_high > 0:
        # 价格是否穿过进场区间
        if day_low <= entry_high and day_high >= entry_low:
            triggered = True

    # 如果没有设置进场区间（兼容旧数据），默认认为触发过
    if entry_low == 0 or entry_high == 0:
        triggered = True

    # ========== 第二步：如果已触发 → 判断SL/TP ==========
    if triggered:
        if direction == 'LONG':
            if sl > 0 and day_low < sl:
                result = 'LOSS'
                detail = 'HIGH=${:,.0f} LOW=${:,.0f}$ | entry${:,.0f}-${:,.0f}| triggered->hit SL(${:.0f}$)'.format(day_high, day_low, entry_low, entry_high, sl)
            elif tp2 > 0 and day_high >= tp2:
                result = 'WIN'
                detail = f'HIGH=${day_high:,.0f} | 达成TP2(${tp2:,.0f})'
            elif tp1 > 0 and day_high >= tp1:
                result = 'WIN_TP1'
                detail = f'HIGH=${day_high:,.0f} | 达成TP1(${tp1:,.0f})，差TP2(${tp2:,,.0f})${(tp2 - day_high):,.0f}'
            else:
                # ⚠️ 关键修复：已进场，但既没到TP也没到SL → 不是"未触发"
                result = 'TRIGGERED_NO_TP'
                detail = f'HIGH=${day_high:,.0f}(距TP1${tp1:,.0f}差${(tp1-day_high):,.0f}) LOW=${day_low:,.0f}(距SL${sl:,.0f}余${(day_low-sl):,.0f}) | 已触发但未达任何目标'
        else:  # SHORT
            if sl > 0 and day_high > sl:
                result = 'LOSS'
                detail = 'HIGH=${:,.0f} LOW=${:,.0f}$ | entry${:,.0f}-${:,.0f}| triggered->hit SL(${:.0f}$)'.format(day_high, day_low, entry_low, entry_high, sl)
            elif tp2 > 0 and day_low <= tp2:
                result = 'WIN'
                detail = f'LOW=${day_low:,.0f} | 达成TP2(${tp2:,.0f})'
            elif tp1 > 0 and day_low <= tp1:
                result = 'WIN_TP1'
                detail = f'LOW=${day_low:,.0f} | 达成TP1(${tp1:,.0f})'
            else:
                result = 'TRIGGERED_NO_TP'
                detail = f'HIGH=${day_high:,.0f} LOW=${day_low:,.0f} | 已触发但未达任何目标'
    else:
        # ========== 第三步：未触发进场 ==========
        result = 'BREAK_EVEN'
        if direction == 'LONG':
            if day_high < entry_low:
                detail = f'HIGH=${day_high:,.0f} < 进场下限${entry_low:,.0f} | 价格未到达场区'
            else:
                detail = f'LOW=${day_low:,.0f} > 进场上限${entry_high:,.0f} | 价格跳过进场区'
        else:
            detail = f'HIGH=${day_high:,.0f} LOW=${day_low:,.0f} | 未进入进场区间'

    # 更新 history 最后一条（但如果已被手动修正过，则不覆盖）
    if history:
        last_note = history[-1].get('resolve_note', '')
        if 'manual' not in last_note.lower():
            history[-1]['result'] = result
            history[-1]['auto_resolved'] = True
            history[-1]['resolve_note'] = detail

    return history

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

# ============ 动态板块生成函数 ============
def _fmt(v, prefix='$'):
    """格式化价格"""
    if not v or v == 'N/A':
        return '—'
    return prefix + '{:,.0f}'.format(float(v))

def _pct(v):
    """格式化百分比"""
    if v is None:
        return '—'
    return '{:+.1f}%'.format(float(v))

def _dir_label(d):
    """方向标签"""
    return {'LONG': '🟢 多', 'SHORT': '🔴 空', 'WAIT': '🟡 观望'}.get(d, '🟡 观望')

def _result_label(result):
    """结果标签"""
    return {
        'WIN': ('✅ TP2达成', 'var(--green)'),
        'WIN_TP1': ('✅ TP1达成', 'var(--green)'),
        'LOSS': ('✗ 止损', 'var(--red)'),
        'BREAK_EVEN': ('⬛ 等回踩未触发', 'var(--muted)'),
        'TRIGGERED_NO_TP': ('⚠️ 触发但未达止盈', '#ff9800'),  # v2.2 新增
        'OPEN': ('▶ 进行中', 'var(--accent)'),
    }.get(result, ('—', 'var(--muted)'))

def _gen_score_stars(score, max_score=10):
    """生成打分星"""
    if score <= 0 or score > max_score:
        return '—'
    filled = '<span style="color:var(--accent);">★</span>'
    empty = '<span style="color:var(--border);">☆</span>'
    return filled * score + empty * (max_score - score)

def gen_section1_stats(history, date_display):
    """一、综合统计看板"""
    last14 = history[-14:] if len(history) >= 14 else history

    wins = sum(1 for h in last14 if h.get('result') in ('WIN', 'WIN_TP1'))
    losses = sum(1 for h in last14 if h.get('result') == 'LOSS')
    triggered_no_tp = sum(1 for h in last14 if h.get('result') == 'TRIGGERED_NO_TP')  # v2.2
    break_even = len(last14) - wins - losses - triggered_no_tp
    win_rate = round(wins / len(last14) * 100, 1) if last14 else 0

    rr_rates = [h.get('rr', 0) for h in last14 if h.get('rr', 0) > 0]
    avg_rr = round(sum(rr_rates) / len(rr_rates), 1) if rr_rates else 0

    # 最大回撤（估算：取最低盈亏比）
    all_pnl = [h.get('pnl', 0) for h in last14]
    max_dd = min(all_pnl) if all_pnl else 0

    wr_badge = '<span class="badge badge-green">达标≥55%</span>' if win_rate >= 55 else '<span class="badge badge-red">未达标</span>'
    rr_badge = '<span class="badge badge-orange">达标≥2:1</span>' if avg_rr >= 2 else ''
    dd_badge = '<span class="badge badge-green">达标&lt;15%</span>' if abs(max_dd) < 15 else '<span class="badge badge-red">超标</span>'

    return f'''<div class="card full">
  <div class="card-title">综合统计看板 <span class="hard-tag">硬性标准</span></div>
  <div class="stats-grid">
    <div class="stat-box">
      <div class="stat-box-label">14天胜率</div>
      <div class="stat-box-val" style="color:{"var(--green)" if win_rate >= 55 else "var(--red)"};">{win_rate}% {wr_badge}</div>
    </div>
    <div class="stat-box">
      <div class="stat-box-label">本月累计盈亏</div>
      <div class="stat-box-val" style="color:var(--green);">待核实</div>
    </div>
    <div class="stat-box">
      <div class="stat-box-label">平均盈亏比</div>
      <div class="stat-box-val orange">{avg_rr}:1 {rr_badge}</div>
    </div>
    <div class="stat-box">
      <div class="stat-box-label">最大回撤</div>
      <div class="stat-box-val" style="color:{"var(--green)" if abs(max_dd) < 15 else "var(--red)"};">{max_dd:+.1f}% {dd_badge}</div>
    </div>
    <div class="stat-box">
      <div class="stat-box-label">本月交易日数</div>
      <div class="stat-box-val">{len(history)}天</div>
    </div>
    <div class="stat-box">
      <div class="stat-box-label">盈利/亏损/保本</div>
      <div class="stat-box-val" style="font-size:14px;">{wins}笔 / {losses}笔 / {break_even}笔</div>
    </div>
  </div>
</div>'''

def gen_section11_yesterday_review(prev_strategy, history, data, today_display):
    """十一、昨日复盘 - 基于真实数据自动生成"""
    if not prev_strategy:
        return f'''<div class="card full">
  <div class="card-title">昨日复盘 ({today_display})</div>
  <div style="padding:20px;text-align:center;color:var(--muted);">暂无昨日策略数据</div>
</div>'''

    btc = data.get('btc', {})
    today_low = btc.get('low_24h', 0)
    today_high = btc.get('high_24h', 0)

    direction = prev_strategy.get('direction', 'WAIT')
    sl = prev_strategy.get('stop_loss', 0)
    tp1 = prev_strategy.get('tp1', 0)
    tp2 = prev_strategy.get('tp2', 0)
    entry_low = prev_strategy.get('entry_low', 0)
    entry_high = prev_strategy.get('entry_high', 0)
    rr = prev_strategy.get('rr_ratio', 0)

    # 判断结果（基于今天价格 + 昨天策略）
    # v2.2: 先判断进场是否触发，再判断SL/TP
    if direction == 'WAIT':
        sl_text = '—'
        tp_text = '—'
        result = 'OPEN'
        pnl_text = '未开仓'
        score = 0
        score_bar = '—'
        exec_note = '观望策略，无需执行'
        highlight = '正确执行观望，等待明确信号'
        fault = '无'
    else:
        # ====== 第一步：进场触发判断 ======
        triggered = False
        if entry_low > 0 and entry_high > 0:
            if today_low <= entry_high and today_high >= entry_low:
                triggered = True
        
        if direction == 'LONG':
            sl_hit = today_low < sl and sl > 0
            tp2_hit = today_high >= tp2 and tp2 > 0
            tp1_hit = today_high >= tp1 and tp1 > 0
            sl_text = f'<span style="color:var(--red);">触发（{_fmt(sl)}）</span>' if sl_hit else '未触发'
            
            if not triggered:
                # 未触发进场区 → 真正的"等回踩"
                tp_text = '<span style="color:var(--muted);">未进入进场区</span>'
                result = 'BREAK_EVEN'; pnl_text = '未触发进场'; score = 7; exec_note = '价格未到达场区间，观望正确'
                highlight = '严格按计划等待入场信号，不追单'
                fault = '无'
            elif sl_hit:
                # 已触发 → 触及止损
                tp_text = f'<span style="color:var(--muted);">已触发进场，但LOW=${_fmt(today_low)}触及止损</span>'
                result = 'LOSS'; pnl_text = '止损出局'; score = 4; exec_note = f'进场已触发(H=${_fmt(today_high)}/L=${_fmt(today_low)})，但触及SL(${_fmt(sl)})'
                highlight = '无'; fault = '方向判断错误或时机不佳，被止损出场'
            elif tp2_hit:
                tp_text = f'<span style="color:var(--green);">TP2 {_fmt(tp2)} 达成 ✅</span>'
                result = 'WIN'; pnl_text = 'TP2止盈'; score = 10; exec_note = '完美执行，TP2达成'
                highlight = 'TP2完美止盈，多头行情顺利捕捉'; fault = '无'
            elif tp1_hit:
                tp_text = f'<span style="color:var(--green);">TP1 {_fmt(tp1)} 达成 ✅</span>'
                result = 'WIN_TP1'; pnl_text = 'TP1止盈'; score = 8; exec_note = 'TP1达成，持仓管理良好'
                highlight = 'TP1成功止盈，执行质量良好'; fault = '无'
            else:
                # ⚠️ v2.2 关键修复：已触发进场，但既没到TP也没到SL
                gap_to_tp = tp1 - today_high if tp1 > 0 else 0
                gap_to_sl = today_low - sl if sl > 0 else 0
                tp_text = f'<span style="color:#ff9800;">H=${_fmt(today_high)}(距TP1差${gap_to_tp:,.0f}) L=${_fmt(today_low)}(距SL余${gap_to_sl:,.0f})</span>'
                result = 'TRIGGERED_NO_TP'; pnl_text = '触发但浮亏/微利中'; score = 5; exec_note = f'进场已确认触发，但全天未达TP也未破SL'
                highlight = '进场方向暂未验证，需关注次日走势'
                fault = f'已进场但价格未达TP1(${_fmt(tp1)})即回落，需评估是否应手动平仓'
        else:  # SHORT
            sl_hit = today_high > sl and sl > 0
            tp2_hit = today_low <= tp2 and tp2 > 0
            tp1_hit = today_low <= tp1 and tp1 > 0
            sl_text = f'<span style="color:var(--red);">触发（{_fmt(sl)}）</span>' if sl_hit else '未触发'
            
            if not triggered:
                tp_text = '<span style="color:var(--muted);">未进入进场区</span>'
                result = 'BREAK_EVEN'; pnl_text = '未触发进场'; score = 7; exec_note = '价格未到达场区间，观望正确'
                highlight = '严格按计划等待入场信号，不追单'; fault = '无'
            elif sl_hit:
                tp_text = f'<span style="color:var(--muted);">已触发进场，但HIGH=${_fmt(today_high)}触及止损</span>'
                result = 'LOSS'; pnl_text = '止损出局'; score = 4; exec_note = f'进场已触发(H=${_fmt(today_high)}/L=${_fmt(today_low)})，但触及SL(${_fmt(sl)})'
                highlight = '无'; fault = '方向判断错误或时机不佳，被止损出场'
            elif tp2_hit:
                tp_text = f'<span style="color:var(--green);">TP2 {_fmt(tp2)} 达成 ✅</span>'
                result = 'WIN'; pnl_text = 'TP2止盈'; score = 10; exec_note = '完美执行，TP2达成'
                highlight = 'TP2完美止盈，空头行情顺利捕捉'; fault = '无'
            elif tp1_hit:
                tp_text = f'<span style="color:var(--green);">TP1 {_fmt(tp1)} 达成 ✅</span>'
                result = 'WIN_TP1'; pnl_text = 'TP1止盈'; score = 8; exec_note = 'TP1达成，持仓管理良好'
                highlight = 'TP1成功止盈，执行质量良好'; fault = '无'
            else:
                gap_to_tp = today_low - tp1 if tp1 > 0 else 0
                gap_to_sl = sl - today_high if sl > 0 else 0
                tp_text = f'<span style="color:#ff9800;">H=${_fmt(today_high)}(距SL余${gap_to_sl:,.0f}) L=${_fmt(today_low)}(距TP1差${gap_to_tp:,.0f})</span>'
                result = 'TRIGGERED_NO_TP'; pnl_text = '触发但浮亏/微利中'; score = 5; exec_note = '进场已确认触发，但全天未达TP也未破SL'
                highlight = '进场方向暂未验证，需关注次日走势'
                fault = f'已进场但价格未达TP1(${_fmt(tp1)})即回落，需评估是否应手动平仓'

    # 执行打分
    if score == 0:
        score_bar = '<span style="font-size:10px;color:var(--muted);">—/10（未平仓）</span>'
    else:
        stars = ''.join([f'<span style="color:{"var(--accent)" if i < score else "var(--border)"};">★</span>' for i in range(1, 11)])
        score_bar = f'{stars} <span style="font-size:10px;color:var(--muted);">{score}/10</span>'

    dir_text = {'LONG': '🟢 做多', 'SHORT': '🔴 做空', 'WAIT': '🟡 观望'}.get(direction, '—')
    entry_text = f"{_fmt(entry_low)}-{_fmt(entry_high)}" if entry_low and entry_high else '—'
    pnl_color = 'var(--green)' if '止盈' in pnl_text else ('var(--red)' if '止损' in pnl_text else 'var(--muted)')

    return f'''<div class="card full">
  <div class="card-title">昨日复盘 ({prev_strategy.get('date', 'N/A')})</div>
  <table class="data-table">
    <thead>
      <tr>
        <th>币种</th>
        <th>方向</th>
        <th>实际入场价</th>
        <th>止损触发</th>
        <th>止盈</th>
        <th>实际盈亏</th>
        <th>执行打分</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>BTC</td>
        <td>{dir_text}</td>
        <td style="color:var(--accent);">{entry_text}</td>
        <td>{sl_text}</td>
        <td>{tp_text}</td>
        <td style="color:{pnl_color};font-weight:700;">{pnl_text}</td>
        <td>{score_bar}</td>
      </tr>
    </tbody>
  </table>
  <div style="margin-top:16px;display:grid;grid-template-columns:1fr 1fr;gap:16px;">
    <div style="padding:12px;background:rgba(244,67,54,0.1);border-radius:8px;">
      <div style="font-size:11px;color:var(--red);font-weight:600;margin-bottom:4px;">🔴 昨日最大失误</div>
      <div style="font-size:12px;color:var(--muted2);">{fault}</div>
    </div>
    <div style="padding:12px;background:rgba(38,201,127,0.1);border-radius:8px;">
      <div style="font-size:11px;color:var(--green);font-weight:600;margin-bottom:4px;">🟢 昨日亮点</div>
      <div style="font-size:12px;color:var(--muted2);">{highlight}</div>
    </div>
  </div>
  <div style="margin-top:10px;padding:8px 12px;background:rgba(247,147,26,0.08);border-radius:6px;font-size:11px;color:var(--muted);">
    复盘依据：SL={_fmt(sl)} | TP1={_fmt(tp1)} | TP2={_fmt(tp2)} | 今日最高={_fmt(today_high)} | 今日最低={_fmt(today_low)}
  </div>
</div>'''

def gen_section12_week_review(history):
    """十二、本周综合复盘"""
    last7 = history[-7:] if len(history) >= 7 else history
    if not last7:
        return '<div class="card full"><div class="card-title">本周综合复盘</div><div style="padding:20px;color:var(--muted);">暂无数据</div></div>'

    wins = sum(1 for h in last7 if h.get('result') in ('WIN', 'WIN_TP1'))
    losses = sum(1 for h in last7 if h.get('result') == 'LOSS')
    triggered_no_tp = sum(1 for h in last7 if h.get('result') == 'TRIGGERED_NO_TP')  # v2.2
    break_even = len(last7) - wins - losses - triggered_no_tp  # v2.2
    total = len(last7)
    win_rate = round(wins / total * 100, 1) if total > 0 else 0

    # 本周第一天和最后一天日期
    first_date = last7[0].get('date', 'N/A')
    last_date = last7[-1].get('date', 'N/A')

    # 找最大单笔（按盈亏估算）
    all_entries = [(h.get('date', ''), h.get('result', ''), h.get('pnl', 0), h.get('rr', 0)) for h in last7]
    best = max(all_entries, key=lambda x: x[2] if x[1] in ('WIN', 'WIN_TP1') else -999)
    worst = min(all_entries, key=lambda x: x[2] if x[1] == 'LOSS' else 999)

    best_txt = f"{best[0]} {'做多' if last7[all_entries.index(best)].get('direction') == 'LONG' else '做空'}" if best[0] else '—'
    worst_txt = f"{worst[0]} {'做多' if last7[all_entries.index(worst)].get('direction') == 'LONG' else '做空'}" if worst[0] else '—'

    # 本周失误分析
    faults = []
    for h in last7:
        if h.get('result') == 'LOSS':
            faults.append(f"{h.get('date', '')} 被止损")
    fault_txt = '、'.join(faults) if faults else '本周无止损记录'

    # 改进建议
    if losses > wins:
        improve = '止损次数超过止盈，需加强方向判断，建议等待更明确信号再入场'
    elif break_even > wins:
        improve = '观望次数偏多，本周行情判断趋于保守，可适度提高信号灵敏度'
    else:
        improve = '保持当前执行节奏，重点提升时机判断准确性'

    return f'''<div class="card full">
  <div class="card-title">本周综合复盘 ({first_date[-4:] if first_date else ""}-{last_date[-4:] if last_date else ""})</div>
  <div class="grid3">
    <div class="stat-box">
      <div class="stat-box-label">本周交易次数</div>
      <div class="stat-box-val">{total}次</div>
    </div>
    <div class="stat-box">
      <div class="stat-box-label">胜/负/保</div>
      <div class="stat-box-val" style="font-size:16px;">{wins} / {losses} / {break_even}</div>
    </div>
    <div class="stat-box">
      <div class="stat-box-label">本周胜率</div>
      <div class="stat-box-val" style="color:{"var(--green)" if win_rate >= 55 else "var(--red)"};">{win_rate}%</div>
    </div>
    <div class="stat-box">
      <div class="stat-box-label">本周累计盈亏</div>
      <div class="stat-box-val" style="color:{"var(--green)" if wins > losses else "var(--red)"};">{'+' if wins >= losses else ''}{wins - losses}笔净胜</div>
    </div>
    <div class="stat-box">
      <div class="stat-box-label">最大单笔盈利</div>
      <div class="stat-box-val" style="color:var(--green);">{'TP2' if best[1] == 'WIN' else 'TP1' if best[1] == 'WIN_TP1' else '—'}</div>
      <div style="font-size:10px;color:var(--muted);">{best_txt}</div>
    </div>
    <div class="stat-box">
      <div class="stat-box-label">最大单笔亏损</div>
      <div class="stat-box-val" style="color:var(--red);">{'止损' if worst[1] == 'LOSS' else '—'}</div>
      <div style="font-size:10px;color:var(--muted);">{worst_txt}</div>
    </div>
  </div>
  <div style="margin-top:16px;display:grid;grid-template-columns:1fr 1fr;gap:16px;">
    <div style="padding:12px;background:rgba(244,67,54,0.1);border-radius:8px;">
      <div style="font-size:11px;color:var(--red);font-weight:600;margin-bottom:4px;">本周最大失误</div>
      <div style="font-size:12px;color:var(--muted2);">{fault_txt}</div>
    </div>
    <div style="padding:12px;background:rgba(74,158,255,0.1);border-radius:8px;">
      <div style="font-size:11px;color:var(--blue);font-weight:600;margin-bottom:4px;">下周唯一改进项</div>
      <div style="font-size:12px;color:var(--muted2);">{improve}</div>
    </div>
  </div>
</div>'''

def gen_section13_month_review(history):
    """十三、月回顾统计"""
    if not history:
        return '<div class="card full"><div class="card-title">月回顾统计 <span class="hard-tag">硬性标准</span></div><div style="padding:20px;color:var(--muted);">暂无数据</div></div>'

    wins_tp2 = sum(1 for h in history if h.get('result') == 'WIN')
    wins_tp1 = sum(1 for h in history if h.get('result') == 'WIN_TP1')
    losses   = sum(1 for h in history if h.get('result') == 'LOSS')
    triggered_no_tp = sum(1 for h in history if h.get('result') == 'TRIGGERED_NO_TP')  # v2.2
    total    = len(history)
    wins     = wins_tp2 + wins_tp1
    break_even = total - wins - losses - triggered_no_tp

    win_rate = round(wins / total * 100, 1) if total > 0 else 0
    rr_rates = [h.get('rr', 0) for h in history if h.get('rr', 0) > 0]
    avg_rr   = round(sum(rr_rates) / len(rr_rates), 1) if rr_rates else 0

    wr_ok = win_rate >= 55
    rr_ok = avg_rr >= 2

    # -------- 累计盈亏计算 --------
    # 优先用真实 pnl 字段；无则用 rr 估算：
    #   WIN(TP2)  → +2R（假设 rr≈2:1 满分止盈）
    #   WIN_TP1   → +1R
    #   LOSS      → -1R
    #   其他      → 0
    pnl_values = []
    for h in history:
        pnl = h.get('pnl')
        if pnl is not None and pnl != 0:
            pnl_values.append(pnl)
        elif h.get('result') == 'WIN':
            pnl_values.append(2.0)
        elif h.get('result') == 'WIN_TP1':
            pnl_values.append(1.0)
        elif h.get('result') == 'LOSS':
            pnl_values.append(-1.0)
        # SKIP / BREAK_EVEN / OPEN → 忽略（0）

    total_pnl_r = round(sum(pnl_values), 2) if pnl_values else 0

    # 判断最大回撤：用最小单笔 pnl
    min_pnl = round(min(pnl_values), 2) if pnl_values else 0
    max_dd_pct = round(abs(min_pnl) / 1.0 * 100, 1)  # 以 1R = 100% 回撤基准

    # 颜色
    pnl_color = 'var(--green)' if total_pnl_r >= 0 else 'var(--red)'
    pnl_prefix = '+' if total_pnl_r >= 0 else ''

    # 达标判断
    dd_ok = abs(min_pnl) < 1.5  # 回撤 < 1.5R 视为达标

    return f'''<div class="card full">
  <div class="card-title">月回顾统计 <span class="hard-tag">硬性标准</span></div>
  <div class="grid3">
    <div class="stat-box">
      <div class="stat-box-label">本月累计盈亏</div>
      <div class="stat-box-val" style="color:{pnl_color};font-size:20px;font-weight:700;">{pnl_prefix}{total_pnl_r}R</div>
      <div style="font-size:10px;color:{pnl_color};">{"✓ 正收益" if total_pnl_r > 0 else "✗ 亏损" if total_pnl_r < 0 else "— 持平"}</div>
    </div>
    <div class="stat-box">
      <div class="stat-box-label">本月交易日数</div>
      <div class="stat-box-val">{total}天</div>
    </div>
    <div class="stat-box">
      <div class="stat-box-label">本月胜率</div>
      <div class="stat-box-val" style="color:{"var(--green)" if wr_ok else "var(--red)"};">{win_rate}%</div>
      <div style="font-size:10px;color:{"var(--green)" if wr_ok else "var(--red)"};">{"✓ 达标≥55%" if wr_ok else "✗ 未达标"}</div>
    </div>
    <div class="stat-box">
      <div class="stat-box-label">平均盈亏比</div>
      <div class="stat-box-val orange">{avg_rr}:1</div>
      <div style="font-size:10px;color:{"var(--green)" if rr_ok else "var(--red)"};">{"✓ 达标≥2:1" if rr_ok else "✗ 未达标"}</div>
    </div>
    <div class="stat-box">
      <div class="stat-box-label">最大单笔回撤</div>
      <div class="stat-box-val" style="color:{"var(--green)" if dd_ok else "var(--red)"};">{min_pnl}R</div>
      <div style="font-size:10px;color:{"var(--green)" if dd_ok else "var(--red)"};">{"✓ &lt;1.5R" if dd_ok else "✗ 超标"}</div>
    </div>
    <div class="stat-box">
      <div class="stat-box-label">本月胜/负/保</div>
      <div class="stat-box-val">{wins}胜 / {losses}负 / {break_even}保</div>
    </div>
  </div>
</div>'''

def gen_section7_tracking_table(history, today_str):
    """七、近14天策略追踪表（v2.0十列结构）"""
    last14 = history[-14:] if len(history) >= 14 else history
    rows = ''
    for h in last14:
        is_today = h.get('date') == today_str
        tag = ' <span style="background:var(--accent);color:#000;font-size:9px;padding:1px 5px;border-radius:3px;font-weight:700;">TODAY</span>' if is_today else ''
        bg = ' style="background:rgba(247,147,26,0.07);"' if is_today else ''

        # 方向
        d = h.get('direction', 'WAIT').upper()
        dir_cls = {'LONG': 'dir-long', 'SHORT': 'dir-short', 'WAIT': 'dir-wait'}.get(d, 'dir-wait')
        dir_txt = {'LONG': '🟢 多', 'SHORT': '🔴 空', 'WAIT': '🟡 观望'}.get(d, '—')
        # 日期格式化: 20260420 → 04/20（v2.2修复：YYYYMMDD格式，[4:6]=月 [6:8]=日）
        date_raw = h.get('date', '')
        if len(date_raw) == 8 and date_raw.isdigit():
            date_short = date_raw[4:6] + '/' + date_raw[6:8]
        else:
            date_short = date_raw[-5:] if date_raw else ''

        # 涨跌（暂无真实数据，显示—）
        chg = '—'
        chg_color = 'var(--muted)'

        # 进场区间
        el = h.get('entry_low', 0)
        eh = h.get('entry_high', 0)
        entry_txt = f'${el:,.0f}–${eh:,.0f}' if el and eh else '—'

        # SL/TP
        sl = h.get('stop_loss', 0)
        tp1 = h.get('tp1', 0)
        tp2 = h.get('tp2', 0)
        sl_txt = f'${sl:,.0f}' if sl else '—'
        tp1_txt = f'${tp1:,.0f}' if tp1 else '—'
        tp2_txt = f'${tp2:,.0f}' if tp2 else '—'

        # 结果
        result = h.get('result', 'SKIP')
        result_map = {
            'WIN': ('✅ TP2达成', 'rb-tp2'),
            'WIN_TP1': ('✅ TP1达成', 'rb-tp1'),
            'LOSS': ('✗ 止损', 'rb-sl'),
            'BREAK_EVEN': ('⬛ 等回踩未触发', 'rb-wait'),  # v2.2: 明确"未触发"
            'TRIGGERED_NO_TP': ('⚠️ 触发未达止盈', 'rb-triggered'),  # v2.2: 新状态
            'SKIP': ('⬛ 观望', 'rb-skip'),
            'OPEN': ('▶ 进行中', 'rb-open'),
        }
        res_txt, res_cls = result_map.get(result, ('—', 'rb-skip'))

        # 盈亏比
        rr = h.get('rr', 0)
        rr_txt = f'{rr}:1' if rr > 0 else '-'

        # 错误分析
        err = h.get('resolve_note', '')
        if not err:
            if result == 'WIN':
                err = '趋势延续，完美执行'
            elif result == 'LOSS':
                err = '方向错误被止损'
            elif result == 'BREAK_EVEN':
                err = 'TP未触及，保持观望'
            elif result == 'OPEN':
                err = '等待策略区确认'
            else:
                err = '观望策略'

        rows += f'''<tr{bg}>
          <td><span class="{dir_cls}">{date_short}{tag}</span></td>
          <td><span class="{dir_cls}">{dir_txt}</span></td>
          <td style="color:{chg_color};">{chg}</td>
          <td style="color:var(--accent);font-size:12px;">{entry_txt}</td>
          <td style="color:var(--red);">{sl_txt}</td>
          <td style="color:var(--green);">{tp1_txt}</td>
          <td style="color:var(--green);">{tp2_txt}</td>
          <td><span class="{res_cls}">{res_txt}</span></td>
          <td>{rr_txt}</td>
          <td style="font-size:11px;color:var(--muted);">{err[:40]}</td>
        </tr>'''

    # 汇总行
    wins14 = sum(1 for h in last14 if h.get('result') in ('WIN', 'WIN_TP1'))
    losses14 = sum(1 for h in last14 if h.get('result') == 'LOSS')
    triggered14 = sum(1 for h in last14 if h.get('result') == 'TRIGGERED_NO_TP')
    break14 = len(last14) - wins14 - losses14 - triggered14
    open14 = sum(1 for h in last14 if h.get('result') == 'OPEN')
    wr14 = round(wins14 / len(last14) * 100, 1) if last14 else 0

    total_rows = ''
    if wins14: total_rows += f'<span class="summary-chip green">✅ 盈利{wins14}笔</span> '
    if losses14: total_rows += f'<span class="summary-chip red">✗ 亏损{losses14}笔</span> '
    if break14: total_rows += f'<span class="summary-chip" style="color:var(--muted);">⬛ 保本/跳过{break14}笔</span> '
    if triggered14: total_rows += f'<span class="summary-chip" style="color:#ff9800;">⚠️ 触发未达TP{triggered14}笔</span> '  # v2.2
    if open14: total_rows += f'<span class="summary-chip" style="color:var(--accent);">▶ 进行中{open14}笔</span> '
    total_rows += f'<span class="summary-chip">14天胜率{wr14}%</span>'

    return f'''<div class="card full">
  <div class="card-title">近14天策略追踪表 <span class="hard-tag">硬性标准</span></div>
  <div style="overflow-x:auto;">
  <table class="data-table">
    <thead>
      <tr>
        <th>日期</th>
        <th>方向</th>
        <th>涨跌</th>
        <th>进场区间</th>
        <th>止损 SL</th>
        <th>TP1</th>
        <th>TP2</th>
        <th>结果</th>
        <th>盈亏比</th>
        <th>错误分析</th>
      </tr>
    </thead>
    <tbody>
      {rows}
    </tbody>
  </table>
  </div>
  <div class="summary-row" style="margin-top:14px;">
    {total_rows}
  </div>
</div>'''

def gen_section8_error_stats(history):
    """八、错误分类统计"""
    last14 = history[-14:] if len(history) >= 14 else history
    losses = sum(1 for h in last14 if h.get('result') == 'LOSS')
    wins = sum(1 for h in last14 if h.get('result') in ('WIN', 'WIN_TP1'))
    triggered_no_tp = sum(1 for h in last14 if h.get('result') == 'TRIGGERED_NO_TP')  # v2.2
    total = len(last14)
    error_rate = round(losses / max(1, total) * 100, 1)

    # 错误类型（从 resolve_note 推断）
    dir_errors = losses  # 止损 = 方向/时机错误
    timing_errors = 0
    sl_errors = losses
    rr_errors = sum(1 for h in last14 if h.get('rr', 0) > 0 and h.get('rr', 0) < 2)
    ok_count = wins

    # v2.2: 改进建议根据实际状态动态生成
    if triggered_no_tp > 0 and losses > wins:
        improve = '触发但未达TP的次数较多，说明方向判断基本正确但时机或目标位需优化。建议：1) TP1适当收窄；2) 触发后设移动止损保护利润。'
    elif losses > wins:
        improve = '坚持"回踩确认"入场原则，所有开仓必须等K线企稳再介入。'
    elif triggered_no_tp > wins:
        improve = f'{triggered_no_tp}笔交易触发进场但未达止盈，说明入场信号有效但行情波动不足。可考虑降低TP1目标位或增加持仓周期。'
    else:
        improve = '保持当前执行节奏。'

    return f'''<div class="card full">
  <div class="card-title">错误分类统计 <span class="hard-tag">硬性标准</span></div>
  <div class="grid2">
    <div>
      <div class="fr-row">
        <span class="fr-label">😡 情绪化交易（冲动进场）</span>
        <span class="fr-val">{timing_errors}次</span>
      </div>
      <div class="fr-row">
        <span class="fr-label">⚡ 追单 / 报复性加仓</span>
        <span class="fr-val">{timing_errors}次</span>
      </div>
      <div class="fr-row">
        <span class="fr-label">🔀 随意移动止损</span>
        <span class="fr-val">{sl_errors}次</span>
      </div>
      <div class="fr-row">
        <span class="fr-label">📋 开仓前未过检查清单</span>
        <span class="fr-val">{dir_errors}次</span>
      </div>
      <div class="fr-row">
        <span class="fr-label">📉 盈亏比 &lt; 2:1 的单子数</span>
        <span class="fr-val">{rr_errors}次</span>
      </div>
      <div class="fr-row">
        <span class="fr-label">✅ 正确执行次数</span>
        <span class="fr-val green">{ok_count}次</span>
      </div>
    </div>
    <div class="stat-box" style="display:flex;flex-direction:column;justify-content:center;">
      <div class="stat-box-label">本月错误率</div>
      <div class="stat-box-val" style="font-size:32px;">{error_rate}%</div>
      <div style="font-size:12px;color:var(--muted);margin-top:8px;">错误{losses}次 / 触发未达TP{triggered_no_tp}次 / 总交易{total}次</div>  <!-- v2.2 -->
      <div style="margin-top:12px;padding:10px;background:rgba(38,201,127,0.1);border-radius:6px;font-size:12px;color:var(--green);">
        💡 改进建议：{improve}
      </div>
    </div>
  </div>
</div>'''

def gen_section9_bars(history):
    """九、近14天胜率柱状图"""
    last14 = history[-14:] if len(history) >= 14 else history
    wins = sum(1 for h in last14 if h.get('result') in ('WIN', 'WIN_TP1'))
    losses = sum(1 for h in last14 if h.get('result') == 'LOSS')
    triggered_no_tp = sum(1 for h in last14 if h.get('result') == 'TRIGGERED_NO_TP')  # v2.2
    break_even_count = len(last14) - wins - losses - triggered_no_tp  # v2.2
    wr = round(wins / len(last14) * 100, 1) if last14 else 0

    bars = ''
    for h in last14:
        r = h.get('result', 'SKIP')
        # v2.2: 六种状态颜色映射
        if r in ('WIN', 'WIN_TP1'):
            color = '#26c97f'
            height = 75
        elif r == 'LOSS':
            color = '#f44336'
            height = 35
        elif r == 'TRIGGERED_NO_TP':  # v2.2 新增：橙色，中等高度
            color = '#ff9800'
            height = 50
        else:  # BREAK_EVEN / SKIP / OPEN
            color = '#7a8299'
            height = 20
        # 日期格式化: 20260420 → 04/20（v2.2修复：YYYYMMDD，[4:6]=月 [6:8]=日）
        date_raw = h.get('date', '')
        if len(date_raw) == 8 and date_raw.isdigit():
            date_short = date_raw[4:6] + '/' + date_raw[6:8]
        else:
            date_short = date_raw[-5:] if date_raw else ''
        bars += f'<div class="bar-item" style="height:{height}%;background:{color};border-radius:3px;position:relative;" title="{date_short}:{r}"><div style="position:absolute;bottom:-18px;left:50%;transform:translateX(-50%);font-size:9px;color:var(--muted);white-space:nowrap;">{date_short}</div></div>'

    return f'''<div class="card full">
  <div class="card-title">近14天胜率柱状图 <span class="hard-tag">硬性标准</span></div>
  <div style="display:flex;align-items:flex-end;gap:6px;height:90px;padding-bottom:22px;overflow-x:auto;">
    {bars}
  </div>
  <div style="display:flex;justify-content:center;gap:24px;margin-top:8px;font-size:12px;">
    <span><span style="display:inline-block;width:10px;height:10px;background:var(--green);border-radius:2px;margin-right:4px;"></span>盈利 {wins}笔</span>
    <span><span style="display:inline-block;width:10px;height:10px;background:var(--red);border-radius:2px;margin-right:4px;"></span>亏损 {losses}笔</span>
    <span><span style="display:inline-block;width:10px;height:10px;background:#ff9800;border-radius:2px;margin-right:4px;"></span>触发未达TP {triggered_no_tp}笔</span>  <!-- v2.2 -->
    <span><span style="display:inline-block;width:10px;height:10px;background:var(--border);border-radius:2px;margin-right:4px;"></span>保本 {break_even_count}笔</span>  <!-- v2.2 修正 -->
    <span style="font-weight:700;">14天胜率: <span style="color:var(--green);">{wr}%</span></span>
    <span style="color:var(--accent);">本月累计: 待核实</span>
  </div>
</div>'''

def gen_section10_line(history):
    """十、近30天胜率趋势折线图"""
    last30 = history[-30:] if len(history) >= 30 else history
    wins30 = sum(1 for h in last30 if h.get('result') in ('WIN', 'WIN_TP1'))
    losses30 = sum(1 for h in last30 if h.get('result') == 'LOSS')
    triggered30 = sum(1 for h in last30 if h.get('result') == 'TRIGGERED_NO_TP')  # v2.2
    break30 = len(last30) - wins30 - losses30 - triggered30  # v2.2
    wr30 = round(wins30 / len(last30) * 100, 1) if last30 else 0

    # 生成折线数据点（从历史数据计算累计胜率）
    points = []
    cumulative_wins = 0
    for i, h in enumerate(last30):
        if h.get('result') in ('WIN', 'WIN_TP1'):
            cumulative_wins += 1
        wr_at_i = round(cumulative_wins / (i + 1) * 100, 1)
        # 映射到 0-100 范围（0=底部，100=顶部）
        y = 100 - wr_at_i
        x = i * (600 / max(len(last30) - 1, 1))
        points.append(f'{x:.1f},{y:.1f}')

    polyline_pts = ' '.join(points)
    # SVG面积
    area_pts = f'0,{100} ' + ' '.join(points) + f' {600},100'

    return f'''<div class="card full">
  <div class="card-title">近30天胜率趋势折线图 <span class="hard-tag">硬性标准</span></div>
  <div class="line-chart">
    <svg viewBox="0 0 600 100" preserveAspectRatio="none">
      <line x1="0" y1="25" x2="600" y2="25" stroke="#252a3a" stroke-width="1"/>
      <line x1="0" y1="50" x2="600" y2="50" stroke="#252a3a" stroke-width="1"/>
      <line x1="0" y1="75" x2="600" y2="75" stroke="#252a3a" stroke-width="1"/>
      <line x1="150" y1="0" x2="150" y2="100" stroke="#252a3a" stroke-width="1" stroke-dasharray="4"/>
      <line x1="300" y1="0" x2="300" y2="100" stroke="#252a3a" stroke-width="1" stroke-dasharray="4"/>
      <line x1="450" y1="0" x2="450" y2="100" stroke="#252a3a" stroke-width="1" stroke-dasharray="4"/>
      <polygon fill="rgba(38,201,127,0.1)" points="{area_pts}"/>
      <polyline fill="none" stroke="#26c97f" stroke-width="2" points="{polyline_pts}"/>
      <text x="75" y="95" fill="#7a8299" font-size="8" text-anchor="middle">Week1</text>
      <text x="225" y="95" fill="#7a8299" font-size="8" text-anchor="middle">Week2</text>
      <text x="375" y="95" fill="#7a8299" font-size="8" text-anchor="middle">Week3</text>
      <text x="525" y="95" fill="#7a8299" font-size="8" text-anchor="middle">Week4</text>
    </svg>
  </div>
  <div style="display:flex;justify-content:center;gap:24px;margin-top:12px;font-size:12px;">
    <span>30天盈利: <span style="color:var(--green);font-weight:700;">{wins30}笔</span></span>
    <span>30天亏损: <span style="color:var(--red);font-weight:700;">{losses30}笔</span></span>
    <span>30天触发未达TP: <span style="color:#ff9800;font-weight:700;">{triggered30}笔</span></span>  <!-- v2.2 -->
    <span>30天保本: <span style="color:var(--muted2);font-weight:700;">{break30}笔</span></span>
    <span>30天胜率: <span style="color:var(--green);font-weight:700;">{wr30}%</span></span>
    <span>近30天累计: <span style="color:var(--accent);">待核实</span></span>
  </div>
</div>'''


# ============ HTML 生成 ============
def generate_html(data, strategy, history):
    """读取模板并填充数据——全动态生成"""
    today = datetime.now()
    date_str = today.strftime('%Y%m%d')
    date_display = today.strftime('%Y-%m-%d')
    yesterday_display = (today - timedelta(days=1)).strftime('%m/%d')

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
        wins = sum(1 for h in last_14 if h.get('result') in ('WIN', 'WIN_TP1'))
        losses = sum(1 for h in last_14 if h.get('result') == 'LOSS')
        triggered_no_tp = sum(1 for h in last_14 if h.get('result') == 'TRIGGERED_NO_TP')  # v2.2
        break_even = sum(1 for h in last_14 if h.get('result') == 'BREAK_EVEN')  # v2.2: 只计真正的未触发
        win_rate_14 = round(wins / len(last_14) * 100, 1) if last_14 else 0
        total_pnl = sum(h.get('pnl', 0) for h in last_14)
        max_dd = min([h.get('pnl', 0) for h in last_14] + [0])
        rr_rates = [h.get('rr', 0) for h in last_14 if h.get('rr', 0) > 0]
        avg_rr = round(sum(rr_rates) / len(rr_rates), 2) if rr_rates else 0
        month_trades = wins + losses + break_even + triggered_no_tp  # v2.2: 完整统计
    else:
        wins, losses, break_even, triggered_no_tp = 0, 0, 0, 0  # v2.2
        win_rate_14 = 0
        total_pnl = 0
        max_dd = 0
        avg_rr = 0
        month_trades = 0

    # ===== 策略追踪表 (近14天) =====
    hist_rows = ''
    for h in last_14:
        result_map = {'WIN': 'win', 'WIN_TP1': 'win', 'LOSS': 'loss', 'BREAK_EVEN': 'break', 'TRIGGERED_NO_TP': 'triggered', 'SKIP': 'skip'}  # v2.2: 完整6态映射
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
    bar_colors = {'WIN': '#00c853', 'WIN_TP1': '#00c853', 'LOSS': '#ff1744', 'TRIGGERED_NO_TP': '#ff9800', 'BREAK_EVEN': '#9e9e9e', 'SKIP': '#9e9e9e'}  # v2.2: 完整6态颜色
    for h in last_14:
        color = bar_colors.get(h.get('result', 'SKIP'), '#9e9e9e')
        height = 30 if h.get('result') in ('WIN', 'WIN_TP1') else 20 if h.get('result') == 'LOSS' else 25 if h.get('result') == 'TRIGGERED_NO_TP' else 10
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
        '\u2192 Today: ' + dir_tag + ' ${:,.0f}-${:,.0f}\n'.format(entry_low, entry_high) +
        'SL $' + str(round(stop_loss, 0)) + ' | TP1 $' + str(round(tp1, 0)) + ' (' + str(rr) + ':1 R:R)\n\n'
        '30D Win Rate: ' + str(50) + '% | 14D PnL: $' + str(round(total_pnl, 2)) + '\n'
        '#BTC #Crypto #Trading'
    )

    # ===== 本月统计 =====
    month_trades = wins + losses + break_even + triggered_no_tp  # v2.2: 完整6态统计
    month_errors = 0  # 可由用户手动记录

    # ===== 模板读取 + 填充 =====
    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
        html = f.read()

    # ===== 替换日期（所有变体） =====
    # 模板基准日期是 2026-04-15，需替换为当天真实日期
    html = html.replace('2026-04-15', date_display)          # 2026-04-15 → 2026-04-20
    html = html.replace('2026年04月15日', today.strftime('%Y年%m月%d日'))  # 中文格式
    html = html.replace('04/15', today.strftime('%m/%d'))     # MM/DD 格式（追踪表等）
    html = html.replace('BTC Daily Report · #31', 'BTC Daily Report · #' + str(31 + int(date_str[-2:]) - 15))  # 报告编号动态化（X推文格式）
    html = html.replace('>#31<', '>' + str(31 + int(date_str[-2:]) - 15) + '<')  # 报告编号（HTML标签内）
    html = html.replace('Daily Report #31', 'Daily Report #' + str(31 + int(date_str[-2:]) - 15))  # Footer 编号
    html = html.replace('Apr 15, 2026', today.strftime('%b %d, %Y'))  # X推文里的英文日期

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

    # ===== 动态板块生成（核心修复 v2.1） =====
    # 加载昨日策略（用于昨日复盘）
    prev_strat_file = os.path.join(CACHE_DIR, 'prev_strategy.json')
    prev_strategy = {}
    if os.path.exists(prev_strat_file):
        with open(prev_strat_file, 'r', encoding='utf-8') as f:
            prev_strategy = json.load(f)
        prev_strategy['date'] = (today - timedelta(days=1)).strftime('%m/%d')

    # 生成各动态板块
    section1 = gen_section1_stats(history, date_display)
    section7 = gen_section7_tracking_table(history, date_str)
    section8 = gen_section8_error_stats(history)
    section9 = gen_section9_bars(history)
    section10 = gen_section10_line(history)
    section11 = gen_section11_yesterday_review(prev_strategy, history, data, yesterday_display)
    section12 = gen_section12_week_review(history)
    section13 = gen_section13_month_review(history)

    # 替换模板占位符
    html = html.replace('<!-- {{SECTION1_STATS}} -->', section1)
    html = html.replace('<!-- {{SECTION7_TRACKING}} -->', section7)
    html = html.replace('<!-- {{SECTION8_ERROR_STATS}} -->', section8)
    html = html.replace('<!-- {{SECTION9_BARS}} -->', section9)
    html = html.replace('<!-- {{SECTION10_LINE}} -->', section10)
    html = html.replace('<!-- {{SECTION11_YESTERDAY_REVIEW}} -->', section11)
    html = html.replace('<!-- {{SECTION12_WEEK_REVIEW}} -->', section12)
    html = html.replace('<!-- {{SECTION13_MONTH_REVIEW}} -->', section13)

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

    # Step 4: 加载历史数据
    history = load_history()

    # Step 4b: 【自动复盘】用今天的数据自动判断昨天的交易结果
    # 读取昨天的策略（存于 cache/prev_strategy.json）
    prev_strat_file = os.path.join(CACHE_DIR, 'prev_strategy.json')
    prev_strategy = {}
    if os.path.exists(prev_strat_file):
        with open(prev_strat_file, 'r', encoding='utf-8') as f:
            prev_strategy = json.load(f)
    # 执行自动复盘
    history = auto_resolve_yesterday(data, prev_strategy, history)

    # Step 5: 生成 HTML
    html_content = generate_html(data, strategy, history)

    # Step 5b: 保存今日策略到 cache/prev_strategy.json（明天的自动复盘用）
    prev_strat_file = os.path.join(CACHE_DIR, 'prev_strategy.json')
    with open(prev_strat_file, 'w', encoding='utf-8') as f:
        json.dump(strategy, f, ensure_ascii=False, indent=2)
    log('prev_strategy.json saved', 'STRAT')

    # Step 5c: 更新 history（写入今日策略，作为明天自动复盘的对象）
    # 先把今天的策略追加到 history，等明天自动结算
    new_entry = {
        'date': today_str,
        'direction': strategy['direction'],
        'entry_low': strategy['entry_low'],
        'entry_high': strategy['entry_high'],
        'stop_loss': strategy['stop_loss'],
        'tp1': strategy['tp1'],
        'tp2': strategy['tp2'],
        'rr': strategy['rr_ratio'],
        'result': 'OPEN',   # 今天刚开，标记 OPEN，等明天自动结算
        'auto_resolved': False,
        'resolve_note': '',
    }
    history.append(new_entry)
    # 去重：每个日期只保留最后一条（防止重复运行导致多条同日记录）
    seen = {}
    for h in history:
        seen[h['date']] = h
    history = list(seen.values())
    history.sort(key=lambda x: x.get('date', ''))
    # 只保留近30天
    if len(history) > 30:
        history = history[-30:]
    save_history(history)

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

    # Step 9: Telegram 推送（必须等 Git push 完成后才推送，避免推送时日报还没上线）
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
