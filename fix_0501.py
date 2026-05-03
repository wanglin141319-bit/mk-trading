#!/usr/bin/env python3
# fix_0501.py - 修正05/01复盘标记

with open('btc/reports/BTC_daily_report_20260502.html', 'r', encoding='utf-8') as f:
    content = f.read()

old = ('05/01</td><td><span class="tag tag-neutral">🟡观望</span></td>'
       '<td class="up">+0.3%</td>'
       '<td style="color:var(--orange)">$76,500-$76,800</td>'
       '<td style="color:var(--red)">$77,500</td>'
       '<td style="color:var(--green)">$75,500</td>'
       '<td style="color:var(--green)">$74,900</td>'
       '<td><span class="tag tag-skip">⬛ 跳过</span></td>'
       '<td>-</td>'
       '<td style="color:var(--muted);font-size:0.8em">五一节假日，正确跳过</td>')

new = ('05/01</td><td><span class="tag tag-neutral">🟡观望</span></td>'
       '<td class="up">+0.3%</td>'
       '<td style="color:var(--orange)">$76,500-$76,800</td>'
       '<td style="color:var(--red)">$77,500</td>'
       '<td style="color:var(--green)">$75,500</td>'
       '<td style="color:var(--green)">$74,900</td>'
       '<td><span class="tag tag-skip">⬛ 未触发</span></td>'
       '<td>-</td>'
       '<td style="color:var(--muted);font-size:0.8em">'
       '价格未到进场区；实际大涨+2.52%，偏空方向判断错误</td>')

if old in content:
    content = content.replace(old, new)
    with open('btc/reports/BTC_daily_report_20260502.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print('✅ 已更新05/01记录：跳过 → 未触发 + 方向判断错误标注')
else:
    print('❌ 未找到匹配内容，手动检查')
    idx = content.find('05/01')
    if idx >= 0:
        print('附近内容：')
        print(repr(content[idx:idx+600]))
