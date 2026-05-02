#!/usr/bin/env python3
# 更新index.html，在第一个报告卡片前插入今日报告

index_path = r"c:\Users\asus\mk-trading\btc\index.html"
new_report = '''                <a href="reports/BTC_daily_report_20260502.html" class="report-card fade-in">
<div class="report-date">2026-05-02</div>
<div class="report-title">BTC Daily Report · #48</div>
<div class="report-summary en-content">BTC $76,589 (+0.33%). FGI 26 Extreme Fear. RSI 48.4. MACD Bearish. Strategy: NEUTRAL / Light Short on bounce to $76,500-$76,800. SL $77,500 / TP1 $75,500 / TP2 $74,900 (R:R 2.0:1). ⚠️ US Nonfarm Payrolls today.</div>
<div class="report-summary zh-content">BTC $76,589(+0.33%)，恐贪26极度恐惧，RSI 48.4。策略：观望/轻仓做空（反弹至$76,500-$76,800）。SL $77,500 / TP1 $75,500 / TP2 $74,900（盈亏比2.0:1）。⚠️ 今日美国非农就业数据。</div>
<div><span class="report-tag neutral">NEUTRAL</span></div>
</a>

'''

with open(index_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 在第424行之前插入（行号从1开始，索引从0开始）
insert_idx = 423  # 第424行的索引

# 插入新内容
new_lines = new_report.splitlines(keepends=True)
for i, line in enumerate(new_lines):
    lines.insert(insert_idx + i, line)

# 写回文件
with open(index_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("✅ index.html 已更新，插入了2026-05-02报告卡片")
