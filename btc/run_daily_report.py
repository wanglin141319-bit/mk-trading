#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[boot/forwarder] BTC 日报入口 —— 转发到「精准版」
================================================
历史说明:
  本文件原为旧版日报主控脚本 v2.0（模板替换不完整 / 指标口径错误 / 硬编码宏观事件），
  已于 2026-10-04 由「精准版」流水线取代。
  旧版完整源码已备份为: run_daily_report.py.bak-20261004

现在本文件是一个**转发器**：
  Windows 计划任务（每天 10:25）→ run_daily_report.py → precise/run_precise_daily.py

精准版做的事:
  1. Gate.io 实时数据（现货/合约/K线/OI/多空比/强平） + alternative.me 情绪指数
  2. 标准口径指标（Wilder RSI / 柱状图穿越零轴的 MACD 交叉 / 多周期）
  3. 统一价格快照，全篇价格自洽（策略价位贴现价 ±1%）
  4. 策略自动追踪与胜率复盘（记录在 .workbuddy/btc_precise/strategy_log.json）
  5. 输出 btc/reports/BTC_daily_report_YYYYMMDD.html 并更新 btc/index.html，自动 git 推送

如需回滚：把 .bak-20261004 改回 run_daily_report.py 即可。
"""
import os
import sys
import runpy

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(HERE, 'precise', 'run_precise_daily.py')

if not os.path.exists(TARGET):
    print(f"[FATAL] 精准版脚本不存在: {TARGET}", file=sys.stderr)
    print("[HINT] 请恢复 run_daily_report.py.bak-20261004 或重建 precise/run_precise_daily.py", file=sys.stderr)
    sys.exit(1)

# 透传命令行参数（供 --dry-run / --no-push 调试用）
sys.argv = [TARGET] + sys.argv[1:]
runpy.run_path(TARGET, run_name='__main__')
