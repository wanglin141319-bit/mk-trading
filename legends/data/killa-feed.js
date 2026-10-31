/* ============================================================
 * Killa (@KillaXBT) 动态追踪数据
 * ------------------------------------------------------------
 * 本文件由「Killa 动态每日追踪」自动化任务维护。
 * 页面 killa.html 通过 <script src> 读取本文件并渲染「最新动态」区块。
 *
 * 取数通道（2026-09-27 升级）：
 *   通过 CDP 连接本机带登录态的 Edge（--remote-debugging-port=9222，
 *   持久化档案 C:\Users\asus\.workbuddy\x-session\profile）直读 X 原推，
 *   取一手原文 + 真实时间戳 + 推文 ID。不要再依赖中文媒体转载
 *   （实测媒体通道会漏报整批推文、并把日期错标 3 天）。
 *
 * 维护规则（自动化任务请严格遵守）：
 *   1. entries 按 date 倒序排列（最新在最前）。
 *   2. 新增动态前，必须先比对现有 entries 的 src 推文 ID，已存在则跳过。
 *   3. 每条必须包含 date / title / quote / read / tags / src 六个字段。
 *      - quote：他的原话或图表结论的忠实转述（不要加工成自己的判断）
 *      - read ：解读——这条改动了他哪一条既有判断，对价格/仓位意味着什么
 *   4. 只收录有可靠来源的信息；来源不明或二手猜测标注 src 并加 tags:"存疑"。
 *   5. 本文件保持纯 ASCII 标点，避免编码问题（中文内容用 UTF-8 正常写）。
 *   6. 推文详情页的 time 字段不可靠，一律以列表页时间线为准（已多次验证）。
 * ============================================================ */

window.KILLA_FEED = {
  // 最近一次扫描时间（自动化任务每次运行后更新）
  lastScan: "2026-10-31T15:08:00+08:00",
  // 累计收录条数
  total: 218,
  // 数据来源说明，显示在页面底部
  sources: "X 一手原文（直读 @KillaXBT 主页，含推文 ID 与真实时间戳）为主；2026-09-22 及更早的条目仍为中文加密媒体转载",

  entries: [
    {
      date: "2026-10-31",
      title: "「周线 50MA 下偏即投降」：加仓从十倍单换成现货",
      quote: "\"Back in 2023, once $BTC flipped the 50MA on the weekly, it pretty much respected it throughout the entire bull market. We've flipped the MA, and now we're deviating slightly below it, as we've seen many times before. These deviations have typically marked capitulation, with the deviations getting bought up quickly. That's why I decided to add to my spot bags from 65K for the first time since we tested 87K. Do as you wish with this information.\"（<b>2023 年 BTC 周线翻上 50MA 之后，整轮牛市基本都尊重它</b>。我们的均线已经翻转，<b>现在略微偏离到它下方</b>，这种情况以前见过很多次。<b>这类偏离通常标志着投降，而且偏离很快就被买回</b>。所以我决定<b>从 65K 起加现货，这是自 87K 那次测试以来第一次</b>。这些信息你爱怎么用怎么用。）——配图为周线蜡烛 + 一条均线，用多个黑点标出历次向下偏离（含最右侧现价处那一个），图上无日期刻度。",
      read: "改动的是<b>加仓用什么工具</b>——10-25 到 10-30 他的加仓计划一直是<b>杠杆</b>（82.8K 十倍单「将在 74K 被打掉」、插针 74K「再开一笔十倍」），本条改成<b>现货</b>，并把 2023 年周线 50MA 当成论据。同日 23:14 那条补上了持仓结构：65K 起已重仓、全部成交后现货均价约 <b>67–68K</b>。⚠️分析：① 用 <b>2023 年单一样本</b>外推「50MA 偏离=投降」，且没给偏离幅度上限——按他的说法跌破越多反而越是买点，属<b>不可证伪</b>；② 「from 65K」措辞有歧义，可读成「从 65K 开始建仓」也可读成「在 65K 加仓」，结合后一条「均价会升到 67–68K」，应是前者；③ 读图确认：黑点确实都落在均线下方、事后价格都弹回均线上方，<b>但图上没有日期刻度</b>，无法核对 2023 那几段偏离的深度与本轮是否同量级——本轮只偏离「slightly」，与 2023 的偏离幅度可比性存疑。失效条件：① <b>周线连续两周收在 50MA 下方且偏离继续扩大</b>（不被买回），「偏离=投降」当场作废；② 若他随后又在 74K 开十倍多单，「改用现货」的降杠杆口径自破；③ 现货均价 67–68K 是心理成本线，<b>日线收在 67K 下方</b>则「低价筹码」叙事变成深度套牢。",
      tags: ["仓位建议", "关键价位", "失效条件"],
      src: "X 原文 @KillaXBT · 2116304891991695857"
    },
    {
      date: "2026-10-31",
      title: "「60% 的市场在赌 7 万以下」：情绪论据首次给比例",
      quote: "\"Every cycle, it's the same story. They've been trying to kill $BTC since 2009, and it's still here. 60% of the market is betting on sub $70K. I wonder how this plays out...\"（<b>每个周期都是同一个故事</b>。他们<b>从 2009 年就想弄死 BTC</b>，它还在。<b>市场上有 60% 在赌 7 万以下</b>。我倒想看看这怎么收场……）——本条无配图，纯文字。",
      read: "改动的是<b>情绪指标的可量化程度</b>——10-29 他说「这里的情绪比 62K 那会儿还差」是纯定性、零数字；本条第一次给出 <b>60% 押注 7 万下方</b>这个比例，把「多数人看空」变成可以对照的仓位事实。⚠️分析：① <b>60% 的口径没交代</b>——是持仓人数占比、还是某个预测市场/投票的赔率？无出处即无法核对，属他惯用的「借群体仓位给自己背书」；② 「since 2009 一直想弄死它」是纯叙事，不含价格信息，实际功能是给「反着大众站队」提供情绪合法性；③ 这条与同日 23:14「我继续加现货」拼成完整的<b>逆向交易链条</b>，但逆向交易成立的前提是那 60% 真错了，他没有任何证据说明这 60% 是「散户噪音」而不是「聪明钱」。失效条件：① 若 BTC <b>日线收破 70,000</b>，这 60% 就是对的，「反着大众」变成站错边；② 若他始终说不出 60% 的统计来源，按他自己「只收录可靠来源」的标准，本条应降级为<b>存疑</b>；③ 立即检验窗口在 11 月初（见同日 02:01 那条的月初反弹规律），若月初不涨，他的逆向底气就没有任何短期支撑。",
      tags: ["情绪指标", "存疑", "基准剧本"],
      src: "X 原文 @KillaXBT · 2116273646784405564"
    },
    {
      date: "2026-10-31",
      title: "「我的 FOMC 枢轴这次没成」：首次认错，剧本挪到月初",
      quote: "\"Monthly close for $BTC is approaching soon. Over the past 4 months, we've seen a rally at the start of the month. It'll be interesting to see whether we get a similar move again, especially with the noticeably bearish narrative going into it. Unfortunately, my FOMC pivot didn't work this time around. There's no excuse, not even with the binance news. As I always say, everything is priced in. It's just ironic how the FUD showed up afterwards. It's a game of probabilities. Now that we have the monthly close approaching, it'll be interesting to see if we get a move to the upside at the start of next month.\"（<b>月线收盘快到了</b>。<b>过去 4 个月，月初都出现过一波上涨</b>。这次进场前看空叙事这么明显，还能不能有同样的走势，值得看。<b>不幸的是，我的 FOMC 枢轴这次没成</b>。<b>没有借口，就算拿 Binance 的消息也说不过去</b>。我一直说，<b>一切都被计价了</b>。讽刺的是 FUD 是事后才出现的。这是个概率游戏。月线快收了，下个月初会不会来一波上行，值得看。）——本条无配图，纯文字。",
      read: "改动的是<b>「枢轴已触发」这条判断的存废</b>——10-29 他宣布「大周期枢轴刚刚触发，时候到了」，同一天还给了「收复 83–84K → 下一站 90K」的路径；本条第一次白纸黑字写 <b>my FOMC pivot didn't work</b>，而且<b>主动关掉甩锅通道</b>（not even with the binance news）。这是本库近 50 天里他第一次<b>不带条件地承认一条判断失败</b>。⚠️分析：① 认错后立刻用「everything is priced in」把自己捞回来——同一句话 10-14、10-29 用来解释「跌了也不该跌」，现在用来解释「我错了但框架没错」，属<b>框架自保</b>；② 替代剧本换成<b>月度季节性：过去 4 个月月初都涨</b>，样本只有 4 个、还都是同一轮行情里的月份，统计意义极弱；③ 时点选得巧——10-31 发帖，11-01 就是月初，<b>24 小时内即可验收</b>，是本轮最容易被证伪的一条。失效条件：① <b>11-01 至 11-03 没有月初上行</b>，「过去 4 个月月初都涨」当场作废，他也失去最后一个短期看多抓手；② 10-30 收 77,368、10-31 现价约 77,380，月线大概率是<b>连续第二根阴线</b>，「月初反弹」的历史前提本身就不成立；③ 若「everything is priced in」继续被用来解释每一次超预期下跌，他将不存在任何可被证伪的宏观判断。",
      tags: ["战绩复盘", "周期判断", "失效条件"],
      src: "X 原文 @KillaXBT · 2116229046761660526"
    },
    {
      date: "2026-10-30",
      title: "「扫 74K 我再买现货」：现货满仓均价 67–68K",
      quote: "\"Bought some more $BTC spot here. I have been progressively adding exposure on each of these drops & will continue to do so. If we sweep 74K, I'll be buying more spot. I'm already heavily exposed from 65K, and if I'm fully filled, my average spot entry will move up to around 67–68K.\"（<b>这里又买了些 BTC 现货</b>。<b>每一波下跌我都在逐步加仓，还会继续加</b>。<b>如果扫到 74K，我会买更多现货</b>。<b>我从 65K 起就已经重仓了</b>，如果全部成交，<b>我的现货均价会抬到 67–68K 左右</b>。）——本条无配图，纯文字。",
      read: "改动的是 <b>74K 这个价位的用途</b>——10-30 00:43 他写的是「82.8K 那笔十倍<b>将在 74K 被打掉</b>，插针 74K 我会<b>再开一笔十倍多单</b>」；本条同一价位改成了<b>买现货</b>，杠杆口径整体降级。同时首次披露现货持仓结构：<b>65K 起已重仓，全部成交后均价约 67–68K</b>。⚠️分析：① 74K 现在同时承担三个角色——十倍单爆仓价、现货加仓点、他的心理支撑，<b>一个价位绑三件事，一次插针会连锁触发全部</b>；② 「均价会抬到 67–68K」是反向信息：现价 77.4K 继续买只会推高成本，说明他<b>预期还要往下买好几档</b>，即他自己也不认为 77K 是底；③ 与同日「不会跌 20%（按 84,898 折约 67.9K）」并读，<b>67–68K 的满仓均价正好压在「不会跌到」的下沿</b>，等于把全部子弹押在一个他自己说不该到的价位。失效条件：① <b>日线收在 67,000 下方</b>，「不会跌 20%」与「满仓均价 67–68K」同时破产；② 若 74K 真被扫而他没加现货，「分批加仓」退回口头；③ 若他在 74K 以下重新开十倍多单，「从杠杆转现货」的降风险叙事作废。",
      tags: ["仓位建议", "关键价位", "失效条件"],
      src: "X 原文 @KillaXBT · 2116187036424065195"
    },
    {
      date: "2026-10-30",
      title: "「FTX 崩盘是底，Binance 被黑也会是底」：事故当引擎",
      quote: "\"FTX collapse marked the bottom. So will the Binance hack. The best way to recoup losses is to send prices significantly higher, not lower. Do not think for one moment that Binance won't do exactly that. They hold multiple billions in $BTC and have the firepower to execute multibillion dollar longs that aren't visible to retail. Not to mention, they probably made $1B in liquidations, slippage, and fees anyway. It might just take some time for the market to rebalance after the temporary damage. But after that, I think it's crystal clear where we are headed on the HTF.\"（<b>FTX 崩盘标记了底部，Binance 被黑也会一样</b>。<b>弥补损失最好的办法是把价格大幅推高，而不是压低</b>。<b>别以为 Binance 不会这么干</b>。他们手里有<b>几十亿的 BTC</b>，有火力执行<b>散户看不见的十亿美元级多单</b>。更别说他们大概已经靠清算、滑点和手续费<b>赚了 10 亿美元</b>。暂时的损伤之后，市场可能需要一点时间再平衡。但之后，<b>大周期往哪走我觉得再清楚不过了</b>。）——本条无配图，纯文字。",
      read: "改动的是<b>交易所事故在剧本里的角色</b>——10-29 20:57 他只说 Binance 不会倒、「$2B 对他们是零钱」（防守性判断）；本条升级成<b>主动看多论据</b>：被黑之后 Binance 有动机把价格<b>推高</b>来补损失，而且它有「散户看不见的十亿级多单」火力。⚠️分析：① 这是本库<b>第一次出现「交易所会拉盘自救」这类阴谋论式推理</b>，既无法证实也无法证伪，但功能是把利空直接翻译成利多，与 10-29「坏消息在牛市推高价格」是同一套不可证伪框架的延伸；② 「FTX 崩盘是底」这个类比本身有硬伤——FTX 是<b>信用毁灭 + 强制清算</b>，底部来自彻底出清；Binance 若只是被盗，出清程度完全不同，两者不能直接对照；③ 「他们赚了 10 亿清算/滑点/手续费」逻辑上站得住，但这恰恰等于<b>承认散户在被吃</b>，是风险描述而非利好。失效条件：① 出现<b>提币暂停、稳定币在 Binance 折价、链上净流出激增</b>任一硬信号，「Binance 没事」当场作废；② 若 11 月中旬前 BTC 未能收复 <b>83–84K</b>（他自己 10-29 给 90K 设的开关），「事故即反转引擎」没有任何价格证据；③ 若 Binance 公布的实际损失远超 $2B，本条的成本假设失效。",
      tags: ["宏观驱动", "存疑", "基准剧本"],
      src: "X 原文 @KillaXBT · 2116136817263054937"
    },
    {
      date: "2026-10-30",
      title: "「还在 76.4K 多单里，回吐 15%」：首次承认浮盈归零，74K 才是加仓点",
      quote: "\"I am still in my $BTC long from 76.4K. The plan has not changed at all. Unfortunately, I'm round-tripping a 15% move. But when I took this position, I wasn't aiming for 15%, I was aiming for 75-100%... In regards to the 10x long strategy, the aggressive re-entry at 82.8K will be taken out at 74K. If we get a wick to 74K, I will re-evaluate and look to enter another 10x long... This is, indeed, most likely going to be the last significant low before we trend significantly higher. We are now 13% off the highs. The biggest retrace we saw back in 2022, based on a 77% drawdown, was 22%. I do not think we will drop 20%... Nonetheless, still long & will either hold till my target or SL.\"（<b>我还在 76.4K 的多单里</b>，计划完全没变。不幸的是，<b>我正在回吐一段 15% 的行情</b>。但我当初进场不是为了 15%，<b>我要的是 75-100%</b>……<b>82.8K 那笔激进的十倍多单将在 74K 被打掉</b>；如果插针到 74K，我会<b>重新评估、再开一笔十倍多单</b>……这很可能<b>就是我们大幅上行前的最后一个重要低点</b>。<b>现在距高点已跌 13%</b>，2022 年那轮最大回撤（在 77% 熊市里）也只有 22%，<b>我不认为会跌 20%</b>……无论如何，<b>还是多，要么拿到目标，要么打到止损</b>。）——本条无配图，纯文字。",
      read: "改动的是<b>「爆仓价」与「加仓价」的关系</b>——10-25 他说 74,000 插针即爆仓、爆仓后「在原失效位再开一笔更小的十倍」，当时读起来像被动挨打；本条把它改写成<b>主动计划</b>：82.8K 那笔十倍<b>「将在 74K 被打掉」</b>，并会重新评估、再开一笔。第二处新增是用 <b>2022 年 22% 最大回撤</b>给本轮 <b>13%</b> 定性，把「最后一跌」从口号变成了带百分比的论据。⚠️分析：①「<b>round-tripping 15%</b>」口径对不上——10-21 高点 84,898 距 76.4K 仅 <b>+11%</b>，按 15% 反推需要约 <b>87.9K</b> 的高点，本库无此记录，<b>存疑</b>；②把 74K 同时当「爆仓价」和「理想加仓价」，本质是<b>承认短期还要再跌约 6%</b>，与他 10-29「枢轴已触发、下一站 90K」<b>直接冲突</b>；③13% vs 22% 的对比给的是<b>跌幅百分比而不是价位</b>——按 84,898 算 20% 是 <b>67.9K</b>，远低于他自己 74K 的爆仓价，等于立了一个自己活不到的容错区间。失效条件：① <b>日线收在 74,000 下方</b>，「不会跌 20%」+「最后一跌」两条同时破产；② 若 74K 真插针而<b>他没按计划再开十倍</b>，「有计划」就退回「被动扛单」；③「hold till target or SL」意味着 <b>126K 之前不主动减仓</b>，任何中途止盈都算自破。",
      tags: ["仓位建议", "失效条件", "周期判断"],
      src: "X 原文 @KillaXBT · 2115967897126293585"
    },
    {
      date: "2026-10-30",
      title: "「Binance 的 FUD 就是为了制造低点」：把交易所危机纳入筑底叙事",
      quote: "\"If you're genuinely naive enough to think Binance is going to fall, you're probably in the lower IQ bracket of X... And what better way to put in a low than to make everyone shit their pants first? The matrix is getting creative with the fud this cycle, respect it.\"（<b>如果你真天真到认为 Binance 会倒</b>，那你大概在 X 上属于智商偏低那档……<b>还有比先吓得所有人尿裤子更好的筑底方式吗？</b>这个周期的 FUD 越来越有创意了，得服。）——同线程另有一条：\"It's just fud. @Binance are good.\"（<b>只是 FUD，Binance 没事</b>。）",
      read: "改动的是<b>利空清单的边界</b>——10-29 21:20 那份十项清单里<b>没有任何交易所风险项</b>，本条新增「Binance FUD」，并把它直接解释成<b>有人刻意制造恐慌来完成筑底</b>。⚠️分析：①这是本库<b>第一次出现交易所信用风险话题</b>，他给的是结论（不会倒）而不是证据；②「$2B 对他们是零钱」用的是<b>自营深度</b>，跟<b>偿付能力</b>不是一回事，两个论据被他当成一个用；③把 FUD 预设成筑底工具，等于<b>把所有负面消息预先归入利好</b>，此后无论跌多少都能自圆其说，属不可证伪框架——这类叙事在他 10-14「一切已计价」时已经出现过一次。失效条件：① 出现<b>链上净流出激增 / 稳定币折价 / 提币暂停</b>任一硬信号，「只是 FUD」当场失效；② 若 BTC 在这轮 Binance 风波后仍<b>跌破 74,000</b>，说明这不是筑底而是真实的流动性收缩；③「低点已经做出来了」若两周内不成立，本条按他自己的框架也该作废。",
      tags: ["宏观驱动", "情绪指标", "存疑"],
      src: "X 原文 @KillaXBT · 2115910800905035843"
    },
    {
      date: "2026-10-30",
      title: "「FOMC 影线回测被拒，回到区间」：90K 从下一站退回待定",
      quote: "\"Unfortunately, we rejected the FOMC wick on the retest. Back to the range it is. It's pretty obvious what they're trying to do here, bait shorts, build liquidity and hunt internal range longs. All this PA does is frustrate $BTC longs before the next 10% move. After this many hunts, not many people will have the conviction to hold their positions.\"（不幸的是，<b>回测时我们被 FOMC 那根影线打回来了</b>，<b>又回到区间里</b>。他们想干什么很明显：<b>诱空、堆流动性、再扫掉区间内的多头</b>。这些价格行为唯一的作用就是<b>在下一次 10% 移动之前把多头磨到没信心</b>。扫了这么多次之后，没多少人还有信念拿住仓位了。）",
      read: "改动的是<b>10-29 23:59 那条路径图</b>——当时他给的顺序是「收复 83–84K → 下一站 90K」，本条<b>承认回测被拒、退回区间</b>，把当下走势重新解释成「诱空 + 扫区间内多头」。⚠️分析：①「back to the range」等于<b>自己放弃了 83–84K 的即时突破预期</b>，但<b>没有撤回 90K 目标</b>，只把时间往后推——这是他惯用的「目标不动、路径改口」；②「before the next 10% move」<b>已经有方向模糊性</b>：10-28 他说的是「向上 10%+」，这里只写「下一次 10% 移动」，<b>没有写方向</b>，措辞在退守；③「扫掉区间内多头」与他同日 08:43「我还在 76.4K 多单里」并存，<b>等于承认自己就是被扫的那批人</b>。失效条件：① <b>79–80K 区间下沿收破</b>（10-29 已收 77,991），「回到区间」里的「区间」这个词就没法再用；② 若「下一次 10% 移动」在 <b>11-04–11-07</b> 窗口内没出现，10-28 那条同时到期作废。",
      tags: ["关键价位", "趋势切换", "失效条件"],
      src: "X 原文 @KillaXBT · 2115882578712608889"
    },
    {
      date: "2026-10-29",
      title: "「收复 83–84K 才是 90K 的开关」：首次给上行路径加前置条件",
      quote: "\"$BTC We're back to testing the FOMC wick high, a critical LTF area. Bulls ideally need to flip this high with force to trigger a nice squeeze into the 83Ks. If they can't reclaim this high, we could easily flop back down to the 79–80Ks. Flip the 83–84K area, and 90K is next.\"（$BTC <b>我们又回到测试 FOMC 影线高点</b>，这是一个关键的<b>低周期区域</b>。多头最好<b>用力度翻上这个高点</b>，从而触发一波<b>冲向 83K 的挤空</b>；<b>如果收复不了，很容易直接摔回 79–80K</b>。<b>翻上 83–84K 区域，下一站就是 90K</b>。）",
      read: "改动的是<b>90K 的成立方式</b>——10-28 他说「未来 7–10 天最小 10%+，主预期进 90Ks」，是<b>无条件预测</b>；本条第一次把它拆成「<b>先收复 83–84K，否则跌回 79–80K</b>」的二选一。⚠️分析：①这是他近期少见的<b>把上下两边都写清</b>的路径图，可证伪性最高；②结果在约 8 小时后揭晓：<b>10-29 日线最低 77,910、收 77,991</b>，79–80K 下沿被直接击穿，按他自己的规则「flop back down」成立、90K 路径作废；③值得注意这 79–80K 与 10-19 划的周线低 <b>79,813</b>、10-23 的「<b>80K is the area</b>」完全重合——<b>三条支撑在同一晚一起破</b>，不是三个独立假设同时错。失效条件：本条自身已给出（<b>收复不了即回落</b>）且已在 10-29 兑现；后续若要再谈 90K，<b>必须先重新收复 83–84K</b>，否则纯口头。",
      tags: ["关键价位", "目标价", "失效条件"],
      src: "X 原文 @KillaXBT · 2115835902111174869"
    },
    {
      date: "2026-10-29",
      title: "「十项利空压不住，这本身就是牛市证据」：利空清单扩到史上最长",
      quote: "\"You'd expect it to be trading a lot lower... We're definitely in the process of establishing a major pivot low soon. Bearish FOMC, with rates held (priced in), Rising oil prices, Hot CPI data, Global bond yields surging, DXY rallying, Ledger wallet hack, Relentless FUD around the pivot to AI, MSTR delisting fears — Yet despite all of this, Bitcoin is quite literally holding its range... Bad news in a bear market pushes prices lower, bad news in a bull market pushes prices higher. Sometimes strength isn't about how much an asset rallies on good news. It's about how well it holds up when everything seems to be going against it.\"（<b>你会以为它该跌得更多</b>……我们<b>肯定正在形成一个重要的周期低点</b>。利空清单：<b>鹰派 FOMC</b>（利率按兵不动、已被计价）、<b>油价上涨</b>、<b>CPI 偏热</b>、<b>全球债券收益率飙升</b>、<b>DXY 反弹</b>、<b>Ledger 钱包被盗</b>、<b>围绕 AI 枢纽的持续 FUD</b>、<b>MSTR 退市担忧</b>——<b>尽管如此，比特币就是literally 守住了区间</b>……<b>熊市里坏消息砸价格，牛市里坏消息推价格</b>。有时候强势不在于好消息涨多少，而在于<b>四面楚歌时它有多抗跌</b>。）",
      read: "改动的是<b>利空清单的长度与用法</b>——10-14 那条只有「一切已计价」的抽象说法，10-26 列过 4 项，本条扩到 <b>10 项</b>（首次出现 <b>Ledger 被盗、MSTR 退市担忧、AI 叙事分流、全球债券收益率、DXY、油价、CPI</b>），并把「抗跌」正式升格为<b>牛市判据</b>。⚠️分析：①「<b>坏消息在牛市推高价格</b>」是本轮最锋利也最危险的一句：它<b>把所有下跌都解释成洗盘</b>，等于<b>取消止损</b>；②判据在 <b>12 小时内</b>就出现裂缝——本条发于 21:20，之后 10-29 日线收 <b>77,991（-4.1%）</b>、10-30 盘中最低 <b>76,500</b>，正是他口中「早就该在 70K 下方」的那种跌幅；③他说「holding its range」，但当天区间下沿 79,710 已破。失效条件：① <b>76,500 已于 10-30 出现</b>，「抗跌」叙事第一道裂缝成立；② 若 <b>74,000 被扫</b>，「坏消息=牛市洗盘」必须改写成「坏消息=趋势转折」；③ 他承诺「<b>major pivot low soon</b>」，若 <b>11-07</b> 前不出现像样的低点反转，这条按他自己的时间框架到期。",
      tags: ["宏观驱动", "情绪指标", "基准剧本"],
      src: "X 原文 @KillaXBT · 2115795810461819353"
    },
    {
      date: "2026-10-29",
      title: "「这里的情绪比 62K 还差」：把 80K 的情绪面直接对标熊市底",
      quote: "\"Sentiment worse here than 62K.\"（<b>这里的情绪比 62K 那会儿还差</b>。）——本条无配图，纯文字。",
      read: "改动的是<b>情绪指标的标尺</b>——10-25 他说「<b>-9% 已是牛市里不错的回撤</b>」、10-27 说「<b>熊市 PTSD 是一种病</b>」，那两句都只是<b>定性别人过度悲观</b>；本条第一次把当前情绪<b>对标到 62K 那个真实底部</b>，等于宣布「悲观程度已到历史级」。⚠️ 分析：① 62K 是他反复引用的「90% 的人盯着更低」的现场，拿它当情绪标尺<b>在叙事上很顺，但不可证伪</b>——情绪没有公开指数可核对；② 价格侧并不支持「比 62K 更差」：10-29 盘中最低 <b>79,710</b>，距 10-21 高点 84,898 仅 <b>-6%</b>，而 62K 那轮是从 10 万上方跌下来的；③ 这句话的真实功能是<b>给自己 95% 的敞口找情绪背书</b>。失效条件：① 若价格继续阴跌到 <b>74,000</b>（他的十倍爆仓价）而「情绪极差」之后仍无反弹，说明他读错了情绪；② 若「情绪比 62K 更差」之后 <b>7–10 个交易日内没有 10%+ 上行</b>，这条按他自己的框架就是反向指标失效。",
      tags: ["情绪指标", "基准剧本", "失效条件"],
      src: "X 原文 @KillaXBT · 2115657906611970434"
    },
    {
      date: "2026-10-29",
      title: "「我们已经在为中期选举去风险」：把事件前下跌重新定义成利好前置",
      quote: "\"Pretty rough if you ask me... Midterms next week & $BTC looks like this. Zero reason to be bearish after either. Few more days left & we are already derisking into it.\"（要我说，<b>相当难看</b>……<b>中期选举就在下周</b>，而 $BTC 走成这个样子。<b>这两件事之后都没有看空的理由</b>。还剩几天，<b>我们已经在为它去风险了</b>。）——配图未读。",
      read: "改动的是<b>中期选举的方向定性</b>——10-04 他引用「每个中期选举周期 BTC 在选举后表现不佳」，把选举<b>之后</b>划成偏空窗口；本条<b>180 度反转</b>成「选举前后都没有看空理由」，并把当下下跌重新解释为<b>市场提前去风险（pricing in）</b>，逻辑是「跌在事件前 → 事件落地即利空出尽」。⚠️ 分析：① 同一段下跌，10-04 叫「选举前谨慎」、10-29 叫「去风险已完成」，属<b>证据重新归因</b>；② 「we are already derisking」把主语从市场偷换成「我们」，读起来像他也在减仓，但他同日又强调 <b>95% 敞口、不减仓</b>，<b>两条互相矛盾</b>；③ 选举日 <b>11-03</b>，验收窗口极短、极易核对。失效条件：① 选举落地后 BTC <b>不涨反破 79,200 / 74,000</b>，「利空出尽」当场变成「利空刚开始」；② 若他选举前真的减了仓，与 10-28「95% risk-on」冲突，属<b>口径不一致</b>。",
      tags: ["宏观驱动", "周期判断", "失效条件"],
      src: "X 原文 @KillaXBT · 2115567224530559201"
    },
    {
      date: "2026-10-29",
      title: "「我不做牛市空单」：正式注销 93.6K 对冲，首次承认漏掉 87K→79K",
      quote: "\"You won't see me shorting a bull market unless I believe it's absolutely necessary... The time to be aggressive with shorts was when $BTC lost 100K. Since 57K was tested, I haven't shared a single short position, and I don't plan to share any for a while... I'm 95% exposed to the market. I'm fully risk-on... I missed the drop from 87K to 79K, and that's completely fine.\"（<b>除非我认为绝对必要，否则你不会看到我在牛市里做空</b>……<b>该激进做空的时候是 BTC 丢掉 100K 那一刻</b>。<b>自从 57K 被测试之后，我没公开过一笔空单，一段时间内也不打算公开</b>……<b>我 95% 敞口、完全 risk-on</b>……<b>我漏掉了 87K 到 79K 这段下跌，这完全没关系</b>。）",
      read: "改动的是<b>对冲空单这条线的存废</b>——09-25 他给「唯一做空位 $93.6K」，09-29 下调到「低 90K」，10-04 后置到「中期选举临近再考虑」，本条直接宣布<b>牛市不做空、一段时间内不公开任何空单</b>，等于<b>注销</b>而不是继续推迟。同时<b>第一次公开承认漏单</b>（87K→79K）。⚠️ 分析：① 这是本库 40 多天来第一次把这条空单从「推迟」改成「作废」，此后每一段回调都归入「不做」；② 「95% 敞口」与 10-25 自曝的三笔多单（62.6K / 76K / 82.8K 十倍）对得上，但<b>在 79.7K 这个位置喊 fully risk-on 是极高风险的自证</b>；③ 承认漏单是加分项，但他同时立「不追已走完的行情」为原则，与 10-25「宁愿提前入场」并列后，<b>等于任何位置都能自圆其说</b>。失效条件：① 他后续若公开任何空单，「牛市不做空」作废；② 若跌破 <b>74,000</b> 而仍未减仓，「95% risk-on」就从信念变成<b>无法执行的固执</b>；③ 「漏掉 87K→79K」意味着这轮回撤<b>没有任何高位对冲收益</b>，全靠低成本多单硬扛。",
      tags: ["仓位建议", "战绩复盘", "趋势切换"],
      src: "X 原文 @KillaXBT · 2115515697790906380"
    },
    {
      date: "2026-10-29",
      title: "「大周期枢轴刚刚触发，时候到了」：时点宣布，但 5% 上行条件未兑现",
      quote: "\"My major cycle pivot for $BTC has just triggered. It's time.\"（我的 $BTC <b>大周期枢轴刚刚触发</b>。<b>时候到了</b>。）——本条无配图，纯文字。",
      read: "改动的是<b>枢轴的触发条件</b>——10-23 他给的量化口径是「600+ 天周期、<b>11/11 反向</b>、<b>至少 5%</b>」，10-24 折算约 <b>84,650</b>（按 80,621 起算）；本条宣布「已触发」，但 <b>10-28 最高只到 81,823</b>，从未接近 84.6K。<b>要么枢轴改成时间驱动（日期到就算），要么那个 5% 条件被静默删掉了</b>——两种解释他都没说。⚠️ 分析：① 他 10-28 20:46 刚说「未来 7–10 天最小 10%+ 波动」，本条紧随其后，属<b>先喊「时候到了」、再补量化</b>；② 「It's time」是本库最模糊的重仓信号之一，<b>无方向、无幅度、无价位</b>，只能靠上下文推成向上；③ 相比 10-24 的「11/11 反向」，<b>提前两周宣布</b>，把可验证的日历条件换成了主观感受。失效条件：① <b>11-07 前</b>（他自己的 7–10 天窗口）没有出现 <b>±10%</b> 单边扩张 → 「已触发」被证伪；② 若向下走满 10%（约 <b>72–73K</b>），枢轴虽触发但方向判错，且直接击穿 74K 十倍爆仓价。",
      tags: ["周期判断", "趋势切换", "失效条件"],
      src: "X 原文 @KillaXBT · 2115480545933025720"
    },
    {
      date: "2026-10-28",
      title: "拿 1978 年以来中期选举后 6 个月均值 11.79% 反驳看空者",
      quote: "\"For all the dumbasses thinking midterms are bearish. Since 1978, the average return in 6 months after midterms is 11.79%. But I'm sure $BTC is gonna fall off a cliff, right?\"（<b>给那些觉得中期选举是利空的蠢货</b>：<b>自 1978 年以来，中期选举后 6 个月的平均回报是 11.79%</b>。但我猜 $BTC 肯定要跳崖，对吧？）",
      read: "改动的是<b>中期选举的证据类型</b>——10-04 他用「选举后表现不佳」这个<b>无出处的印象</b>支持偏空，本条反过来用<b>1978 年以来的均值 11.79%</b> 支持偏多。同一个宏观事件，三周内被两套相反的说法各自背书。⚠️ 分析：① 样本绝大部分<b>落在 BTC 诞生之前</b>（1978–2008 是股指/宏观资产），拿它推 BTC 属<b>跨资产外推</b>；② 只给均值，<b>没给中位数、没给负收益年份占比</b>，单点统计撑不起方向；③ 语气攻击性明显上升（dumbasses / 蠢货），是<b>情绪化加仓期的典型话术</b>，通常出现在他自己也承压的时候。失效条件：① 若选举后 6 个月内 BTC 收益为负，这条统计被他自己的标的否掉；② 更近的验收：<b>11-03 之后两周</b>内若 BTC 跌破 79,200，本条从论据变成反向指标。",
      tags: ["宏观驱动", "周期判断", "存疑"],
      src: "X 原文 @KillaXBT · 2115443327676154343"
    },
    {
      date: "2026-10-28",
      title: "「7–10 天至少 10%」：首次双向量化，主预期把 BTC 带进 90K 区间",
      quote: "\"$BTC is on the verge of a major move. With FOMC today, we know the drill... The minimum expected move over the next 7–10 days is 10%+. ... Since we're derisking into the date, I'm leaning toward a bullish reaction afterwards, potentially taking BTC into the 90Ks. If things go the other way, we could see another 10% drop from current prices. That's not my main expectation... For now, I'm bullish & remain bullish.\"（$BTC <b>正处在一次大行情的边缘</b>……<b>未来 7–10 天的最小预期波动是 10% 以上</b>。……既然大家在事件前就去风险，<b>我倾向事件后是看多反应，有可能把 BTC 带进 90K 区间</b>。走反了的话<b>现价再跌 10%</b> 也有可能，但那不是我的主预期……<b>目前我看多，并继续看多</b>。）",
      read: "改动的是<b>近期目标位的上限</b>——10-25 到 10-27 他的近期口径是「守住 80K、等 126K」，从没给过 90K 这种<b>周级别的中间目标</b>；本条第一次把 7–10 天的路径量化成「<b>上行 10%+ → 89K 上方（90Ks）</b>」，并把下跌 10%（约 <b>73K</b>）标为「有点极端、不是主预期」。⚠️ 分析：① 这是本库<b>最可证伪的一条</b>：从 10-28 起 7–10 天即 <b>11-04 至 11-07</b>，要么出现 10% 单边，要么作废；② 「事件前去风险 → 事件后反弹」是<b>经典逆向押注</b>，前提是事件前真跌透了，但 10-28 收 <b>81,343</b>，比他 10-25 说的「-9%」还高，<b>并未跌透</b>；③ 73K 这个下行位<b>低于他自己 74,000 的十倍爆仓价</b>，等于承认「极端情形下我先被扫出去，然后才反弹」。失效条件：① <b>11-07 前</b>没有 ±10% 扩张 → 量化失效；② 没到 89K 却先破 79,200 → 「看多反应」判错；③ 破 74,000 → 先爆仓，判断对错已无意义。",
      tags: ["目标价", "宏观驱动", "失效条件"],
      src: "X 原文 @KillaXBT · 2115424973007307159"
    },
    {
      date: "2026-10-28",
      title: "80,800 处给出三档带天数目标：100K/160 天、126K/280 天、160K/500 天",
      quote: "\"A few months later, $BTC is at $80800. I will see you at $100,000 in 160 days. I will see you at $126,000 in 280 days. I will see you at $160,000 in less than 500 days.\"（几个月之后，$BTC 在 <b>80,800</b>。<b>160 天后见你到 $100,000；280 天后见你到 $126,000；不到 500 天见你到 $160,000</b>。）",
      read: "改动的是<b>目标位的可验收性</b>——此前 126K / 160–180K 一直是「本周期」「未来 3–4 年」这种<b>无到期日</b>的说法（同日凌晨他还写「3–4 年内 160–180K」），本条第一次把它们<b>换算成具体天数</b>。⚠️ 分析：① 按 10-27 起算：<b>100K ≈ 2027-04-05、126K ≈ 2027-08-03、160K ≈ 2028-03-10</b>，这是他给过的最硬的日历承诺；② 但「160K 不到 500 天」与同日「3–4 年内 160–180K」<b>口径不一致</b>（500 天 < 2 年），说明他手上至少有两套时间表；③ 60% 涨幅摊到 160 天，折年化约 <b>170%</b>，对 BTC 不算离谱，但<b>前提是 74K 不破、不回 70K 下方</b>。失效条件：① <b>2027-04-05 前</b>未见 100K → 三档全部顺延，「160 天」这个数作废；② 期间跌破 <b>74,000</b> 触发十倍仓清算，时间表要整体重写；③ 两套时间表并存时<b>以哪套为准，他从未说明</b>。",
      tags: ["目标价", "周期判断", "存疑"],
      src: "X 原文 @KillaXBT · 2115215729586786538"
    },
    {
      date: "2026-10-28",
      title: "「FUD 之年」长文：把弱势归因为叙事操盘，重申 3–4 年 160–180K",
      quote: "\"I said this in February. What are we seeing now? The year of FUD. The year of bad news. The year of bearish narratives. Every excuse in the book will be deployed to keep you from buying... And when the moment to buy finally arrives, it won't feel like opportunity. It will feel like risk... I remain positioned for 160–180K within the next 3–4 years. You won't recognize the bottom when it's here.\"（我二月就说过。<b>FUD 之年、坏消息之年、看空叙事之年</b>，<b>所有借口都会被搬出来阻止你买</b>……<b>真正能买的那一刻到来时，它不会像机会，只会像风险</b>……<b>我的仓位仍是为未来 3–4 年 160–180K 而设</b>。<b>底在那儿的时候你认不出来</b>。）",
      read: "改动的是<b>看多的因果链</b>——10-20 他用资金面（USDC 增发）、10-22 用 USDT.D 结构、本条换成<b>纯叙事论</b>：跌是因为有人刻意制造 FUD，不是结构变坏，等于把所有反向证据<b>预先解释掉</b>。⚠️ 分析：① 「底你认不出来」与 10-24「<b>那就是底</b>」（Déjà vu 那条）是<b>两种互斥的底论</b>——一个说底不可识别、一个说底已确认；② 「3–4 年 160–180K」与 6 小时前「500 天内 160K」再次撞车；③ 这类长文通常出现在<b>浮亏扩大、需要稳心态</b>的位置，10-27 收 80,909 已跌破他 10-23 的「80K is the area」上沿。失效条件：① 若「FUD 只是叙事」而价格<b>周线收在 74,000 下方</b>，说明不是叙事而是趋势；② 「认不出来的底」让本条<b>永远无法被证伪</b>，属情绪条目而非判断。",
      tags: ["情绪指标", "周期判断", "存疑"],
      src: "X 原文 @KillaXBT · 2115135187298242989"
    },
    {
      date: "2026-10-28",
      title: "「我还在 76.4K 的多单里」：明确拒绝把止损移到成本价",
      quote: "\"I am still in my $BTC long from 76.4K. The plan has not changed at all... I will not be moving my SL to entry. I will hold until either my target is reached or I am stopped out... has the structure shifted, and has the plan changed? Absolutely not. So there is 0 panic in my mind.\"（<b>我还在 76.4K 那笔 $BTC 多单里，计划一点没变</b>……<b>我不会把止损移到成本价</b>，会一直拿到目标达成或被止损……结构变了吗？计划变了吗？<b>完全没有</b>。所以我脑子里<b>零恐慌</b>。）",
      read: "改动的是<b>成本与风控口径</b>——10-25 媒体转述的成本是「62,600 / 76,000 / 82,800 十倍」，本条<b>首次由他本人把第二笔说成 76.4K</b>，并<b>首次明确不做保本止损</b>。⚠️ 分析：① 76.4K 距 10-29 盘中低点 <b>79,710</b> 只有 <b>-4.1%</b>，距 74,000 只有 -3.2%，<b>这笔多单已贴近无效区</b>；② 「不把 SL 移到成本」听着有信念，实质是<b>主动放弃一个零成本的风险控制动作</b>——价格回到 76.4K 时本可无损离场，现在选择承受全部回撤；③ 与 10-24「杠杆把人毁了」「只有现货才是真多头」并读，<b>他一边骂杠杆一边裸扛杠杆单</b>。失效条件：① 触及 <b>76.4K</b> → 这笔归零，「计划没变」变成「计划失效」；② 若他在 76.4K 之前移了止损或减仓，本条的承诺作废；③ 「目标」仍未明说（126K？90Ks？），<b>无法按目标验收</b>。",
      tags: ["仓位建议", "关键价位", "失效条件"],
      src: "X 原文 @KillaXBT · 2115113694711390331"
    },
    {
      date: "2026-10-27",
      title: "「熊市 PTSD 是一种病」：把看空者定性成心理问题",
      quote: "\"Bear market PTSD is an illness. We are in a bull market and people are still trading as if we are in a bear market. Very unfortunate.\"（<b>熊市 PTSD 是一种病</b>。<b>我们身处牛市</b>，人们却还在按熊市的方式交易。<b>非常不幸</b>。）",
      read: "改动的是<b>反驳方式</b>——此前他对看空者的回应是给数据（USDT.D、USDC 增发、中期选举统计），本条换成<b>给对方贴心理标签</b>：不是你的论据错，是你有病。⚠️ 分析：① 这是<b>论据退化的信号</b>：结构证据开始不利时（10-27 收 80,909，连续 4 日收在 83.7K 之下），话术从「看数据」转向「看心态」；② 与 10-24「杠杆客都是小丑」同属<b>人格化攻击</b>，近一周已出现 3 次，频率明显上升；③ 无价位、无仓位，属纯情绪条目。失效条件：① 若 BTC 出现<b>周线级下跌结构</b>（收在 74K 下方），「牛市」前提被价格否掉，PTSD 的说法反过来成立；② 纯定性，<b>无可验收内容</b>。",
      tags: ["情绪指标", "存疑"],
      src: "X 原文 @KillaXBT · 2115053670559859187"
    },
    {
      date: "2026-10-27",
      title: "「83.7K 被拒绝」：确认关卡失守，但把扫针定性成「定价最坏」",
      quote: "\"$BTC rejected the 83.7K region. Now we're sweeping the previous wick lows, liquidating billions, with FOMC, a new monthly open, midterms and Anthropic all ahead. They're quite literally pricing in the worst before continuation. This is not the time to turn bearish, especially with BTC sweeping the lows.\"（$BTC <b>被 83.7K 区域拒绝</b>。<b>我们正在扫掉之前的下影线低点、清算数十亿</b>，前面还有 FOMC、新月开盘、中期选举和 Anthropic。<b>他们简直是在为后续行情提前定价最坏情形</b>。<b>这不是转空的时候</b>。）",
      read: "改动的是<b>83.7K 的角色</b>——10-24 他还把 83.7K 当成「<b>要收复的关卡</b>」，本条正式承认<b>被拒绝</b>（rejected），并把后续下跌定义为「<b>扫掉前影线低点</b>」而非趋势转折。⚠️ 分析：① 这是本库第一次由他本人确认「83.7K 失守」，<b>等于把 10-21 定的 83.7–84.2K 区间上沿彻底让出</b>；② 「扫低点」有明确价格含义：10-17 周线低 <b>79,813</b>、10-24 低 <b>79,220</b>、10-27 低 <b>79,506</b>，<b>影线低点已被扫过三次</b>；③ 「pricing in the worst before continuation」是他<b>把下跌解释成洗盘</b>的固定句式，10-04 已用过一次（「垂直吸筹」）。失效条件：① 扫完不回收、<b>日线收在 79,200 下方</b> → 「扫针」变「破位」；② 破 <b>74,000</b> → 连「洗盘」都无法自圆；③ 他提到的「Anthropic」未说明是什么事件，<b>无法核对</b>。",
      tags: ["关键价位", "基准剧本", "失效条件"],
      src: "X 原文 @KillaXBT · 2114869434443784200"
    },
    {
      date: "2026-10-27",
      title: "「真熊出柜了，记住他们的名字」：开始给看空者记名单",
      quote: "\"Now you're starting to see the true bears come out of their closets. Just make sure to remember all their names.\"（现在你开始看到<b>真正的熊从柜子里出来了</b>。<b>记得把他们所有人的名字都记下来</b>。）",
      read: "改动的是<b>与看空阵营的关系</b>——此前他对空头多是嘲讽（flip floppers、clowns），本条升级为<b>公开记名单</b>，把观点分歧转成人身对赌。⚠️ 分析：① 「记住名字」这类号召通常出现在<b>他自己承压最大</b>的阶段，是<b>为事后正确性铺路</b>——涨上来可清算名单，跌下去则被反向引用；② 与 10-24「别把话给我说歪了」同属<b>叙事防御</b>，一周内第 2 次；③ 零信息量，无价位无仓位。失效条件：① 若跌破 <b>74,000</b>，名单反过来变成<b>记录他自己</b>的证据；② 若他在更低位置转空，这条会被当作「双标」证据。",
      tags: ["情绪指标", "存疑"],
      src: "X 原文 @KillaXBT · 2114840219581026396"
    },
    {
      date: "2026-10-27",
      title: "「为省 10% 错过 57% 值吗」：建仓口径从精确价位退回「建敞口」",
      quote: "\"I remember making this exact post at 60K, saying the same thing I'm saying now. Are you really willing to risk missing a 57%+ move because you're fixated on being 10% lower? I know I'm not. And I know the big players aren't either. You should be building $BTC exposure.\"（我记得在 <b>60K</b> 时发过一模一样的帖。<b>你真的愿意为了等再低 10%，去冒错过 57%+ 行情的风险吗</b>？我不愿意，大玩家也不愿意。<b>你现在就该建立 $BTC 敞口</b>。）",
      read: "改动的是<b>建仓方式的表述</b>——10-21 给网格 76.8–80.8K、10-23 说「80K is the area，long the sweeps」、10-25 说「未来几周 DCA」，全是<b>带条件的具体动作</b>；本条退回「<b>build exposure</b>」这种<b>无价位、无节奏</b>的口号，并首次给出 <b>57%+ vs 10%</b> 的赔率框架。⚠️ 分析：① 57% 对应约 <b>126K</b>（80K×1.575），10% 对应约 <b>72K</b>——<b>两头他都不打算等</b>，属自我说服；② 「我在 60K 发过一模一样的帖」是<b>用历史成功案例背书</b>，但那次是底部区域，这次是 80K、距高点只跌 6%；③ 与同日 20:11「熊市 PTSD」并读，当天是<b>连续三条情绪型劝导</b>，没有一条带风控。失效条件：① 若真跌到 <b>72K</b>，「为省 10% 错过 57%」的算术反转成「为抢 57% 先亏 10%」；② 破 74,000 → 十倍仓爆，赔率框架失效。",
      tags: ["仓位建议", "目标价", "失效条件"],
      src: "X 原文 @KillaXBT · 2114784746051883019"
    },
    {
      date: "2026-10-27",
      title: "用 USDT.D 周/月线 BOS 回踩，给出首个非价格失效开关",
      quote: "\"Structure is king. Forget the $BTC LTF chop for a moment and look at where USDT.D is positioned. It's bearish and retesting a BOS on the weekly and monthly... As long as USDT.D stays below this red boundary, BTC remains bullish and in an uptrend... This is still a bull market retracement until proven otherwise.\"（<b>结构为王</b>。先别管 $BTC 的低周期震荡，看 <b>USDT.D 在哪</b>：<b>它是看空结构，正在回踩周线和月线的 BOS</b>……<b>只要 USDT.D 守在这条红线之下，BTC 就仍是多头、仍在上升趋势里</b>……<b>在证明不是之前，这仍然只是牛市回撤</b>。）",
      read: "改动的是<b>失效条件的载体</b>——此前他的失效位全部是 BTC 价格（74K / 79.8K / 76.8K），本条第一次给出<b>一个非价格、可独立观察的开关</b>：USDT.D 是否守在红线下方。⚠️ 分析：① 这是他近期<b>最像交易系统的一条</b>（有明确定义的条件句），值得单独跟踪；② 但「红线」的具体数值没给、<b>只在图上</b>，第三方无法复现，可验证性大打折扣；③ 「仍只是牛市回撤」与 10-25「-10% 已接近回撤尾声」连成一条线：<b>回撤论是他 10-21 以来所有判断的地基</b>，一旦幅度超模型，整套要重算。失效条件：① <b>USDT.D 上破那条红线</b>（周线/月线 BOS 回踩失败）→ 按他自己的规则，BTC 多头论点作废；② BTC 日线收在 <b>79,200</b> 下方并扩张 → 「回撤」定性失效；③ 若他后续不再提 USDT.D，说明这个开关被弃用。",
      tags: ["链上数据", "基准剧本", "失效条件"],
      src: "X 原文 @KillaXBT · 2114764745182265551"
    },
    {
      date: "2026-10-26",
      title: "FOMC 双情景量化：上行 10%→86K、15%→90K，下行 72K / 67K",
      quote: "\"Billions liquidated, FOMC is priced in, and we're heading into the monthly close pivot + major cycle pivot + Midterms. Every directional move around FOMC has been around 10–15%. ... a 10% move would take us to 86K, while 15% would put us above 90K. On the other hand, the bearish side would mean 72K at -10% and 67K at -15%. I think a 15% drop is way too extreme and pretty unlikely. ... I always trade against the narrative building into these dates, and right now it's clearly more bearish. That's why I'm leaning bullish on $BTC\"（<b>数十亿被清算，FOMC 已被定价</b>，我们正走向<b>月线收盘枢轴 + 大周期枢轴 + 中期选举</b>。<b>FOMC 前后的方向性波动历来都在 10–15%</b>……<b>10% 能到 86K，15% 则站上 90K</b>；空头方向 <b>-10% 是 72K、-15% 是 67K</b>。<b>我认为 -15% 太极端、很不现实</b>……<b>我总是在这些日期前反向交易叙事</b>，现在叙事明显偏空，<b>这就是我倾向看多的原因</b>。）",
      read: "改动的是<b>下行情景的下限</b>——此前最低口径是 10-19「never sub 70K」、10-25「10–15% 回撤」（约 72–76K），本条<b>第一次把 67K 写进自己的情景表</b>，虽然立刻标注「太极端」。⚠️ 分析：① 66–67K <b>已经侵入「永不破 70K」的禁区</b>，说明他内部算过更深的路径；② 「我总在事件前反向交易叙事」是<b>可证伪的方法论声明</b>，这次下注是「叙事偏空 → 我做多」，标的是 80K 附近；③ 两套情景<b>概率一个都没给</b>，只有定性偏向，等价于不可验收；④ 与 10-23「5 个交易日内 ≥5% 上行至 84.6K」并读，<b>同一个 FOMC 窗口被赋予两套不同幅度预期</b>。失效条件：① FOMC 后走 <b>-10% → 72K</b>，「反向交易叙事」这一次就错了，且逼近十倍爆仓价；② 走 <b>+10% → 86K</b> 但站不住，同样无效；③ 67K 一旦真实出现，「never sub 70K」整条基线作废。",
      tags: ["宏观驱动", "目标价", "失效条件"],
      src: "X 原文 @KillaXBT · 2114725754193776908"
    },
    {
      date: "2026-10-26",
      title: "长文：80K 一定会去 126K，到达之前「没有任何理由止盈」",
      quote: "\"Bitcoin is at $80,000 a coin. It's going to $126,000. There's absolutely no reason to take profits before that region is reached. ... I spend 14–16 hours a day in one of my rooms, religiously watching charts, with 7-figure exposure in the market.\"（<b>比特币现在 80,000 一枚，它会去 126,000</b>。<b>在那个区域到达之前，绝对没有任何理由止盈</b>……<b>我每天在房间里盯盘 14–16 小时，市场里有七位数敞口</b>。）",
      read: "改动的是<b>止盈纪律</b>——10-21 他把 126K 从「终点」降级为「起跑线」、把目标抬到 150K+；本条<b>退回「126K 之前不止盈」</b>，是近一周最明确的持仓纪律，同时<b>首次给出敞口规模（七位数）</b>。⚠️ 分析：① 「126K 前不止盈」与 10-25「74K 爆仓就在原失效位再开十倍」组合，形成<b>满仓、止损不上移、不止盈</b>的三重放开；② 七位数敞口（≥100 万美元）与「95% risk-on」互相印证，也意味着<b>这轮 79.7K 的回撤对他不是纸面数字</b>；③ 长文前半骂 KOL 造假、后半自证「每天盯盘 14–16 小时」，属<b>用勤奋替代论据</b>。失效条件：① 到 <b>126K</b> 前若他止盈/减仓，本条纪律作废；② 若在 <b>74,000</b> 被清算，「没有理由止盈」就变成<b>没有机会止盈</b>；③ 「七位数敞口」无第三方可核，属自述。",
      tags: ["仓位建议", "目标价", "存疑"],
      src: "X 原文 @KillaXBT · 2114461741752979801"
    },
    {
      date: "2026-10-26",
      title: "首次给山寨目标：SOL 91–101 收，看 140–150",
      quote: "\"Sell me all your $SOL at 91-101 & f*ck off. I will see you at 140-150 in due time.\"（<b>把你所有的 $SOL 在 91–101 卖给我，然后滚蛋</b>。<b>到时候 140–150 见</b>。）",
      read: "改动的是<b>标的范围</b>——本库近 30 条几乎全是 BTC（USDT.D 只是参照），本条第一次给出<b>山寨的具体买区与目标</b>：91–101 建仓、140–150 目标（约 +40%~+55%）。⚠️ 分析：① 这是典型的<b>牛市扩散（alt rotation）下注</b>，与他 10-04「中期选举后去风险」的宏观谨慎<b>方向相反</b>；② 91–101 区间宽度 11%，属「<b>区间扫货</b>」而非精确点位，可执行性比他的 BTC 喊单强；③ 没给时间窗（in due time），<b>等于不可验收</b>；④ 与「95% 敞口全在 BTC」的自述冲突——真 95% 风险敞口的话，这笔 SOL 的钱从哪来他没说。失效条件：① SOL 跌破 <b>91</b> 且不回 → 买区失效；② 后续不再提 SOL，说明是情绪化喊单；③ 时间无限期，<b>无法判定对错</b>。",
      tags: ["山寨", "目标价", "存疑"],
      src: "X 原文 @KillaXBT · 2114435576028172336"
    },
    {
      date: "2026-10-26",
      title: "「想象一下在 ATH 之下止盈」：把唯一的止盈起点钉在历史高点区",
      quote: "\"Imagine taking profits below ATH.\"（<b>想象一下在历史新高之下止盈</b>。）",
      read: "改动的是<b>止盈的合法性</b>——把「ATH 之下卖出」直接定性为荒谬，等于把 126K（历史高点区）设成<b>唯一合理的止盈起点</b>。⚠️ 分析：① 与同日「126K 前没有任何理由止盈」是同一立场的两次表达，<b>密度说明他在反复自我确认</b>；② 逻辑漏洞明显：<b>不给定 ATH 具体值，所有止盈都会被这句否掉</b>，而他自己的 ATH 口径在 126K / 150K / 160–180K 之间来回；③ 零信息量，属情绪条目。失效条件：① 若他在 126K 之下任何位置减仓，本条作废；② 若 ATH 实际高于 126K（如 160K+），126K 止盈也落在「ATH 之下」，<b>他的规则自相矛盾</b>。",
      tags: ["仓位建议", "情绪指标"],
      src: "X 原文 @KillaXBT · 2114401853777813529"
    },
    {
      date: "2026-10-25",
      title: "回撤模型：上轮 77% 熊市对应 22% 回撤，本轮 54% 熊市只该跌 10–15%",
      quote: "\"Last cycle, the largest drawdown before the run to 126K was 22% based on a 77% bear market. With a 54% bear market drawdown this cycle, that points to a 10–15% retracement. We're already down 10% from the highs, so we could be nearing the end of this pullback before the next leg higher.\"（上一轮，<b>冲向 126K 之前的最大回撤是 22%</b>，对应 <b>77% 的熊市</b>。本轮熊市回撤 <b>54%</b>，按比例只对应 <b>10–15% 的回撤</b>。<b>我们已经从高点跌了 10%</b>，所以这轮回调<b>可能已接近尾声</b>。）",
      read: "改动的是<b>回撤上限的定量依据</b>——此前「-10% 是不错的回撤」只是形容词，本条给出<b>可计算的模型</b>：熊市深度与牛市回撤成比例，54%/77%×22% ≈ <b>15.4%</b>。⚠️ 分析：① 这是<b>两点拟合的线性模型</b>（历史样本 n=1），统计上极弱；② 按 84,898 高点算，-15% 是 <b>72,163</b>，<b>低于他 74,000 的十倍爆仓价</b>——模型允许的底部先爆他的仓；③ 「已跌 10%」的基线是他自己口径（从 87K 段算），从 10-21 高 84,898 只跌 <b>-6%</b>，<b>分母被放大了</b>；④ 与同日「不必重演极端低点」是同一论证的两条腿。失效条件：① 回撤超过 <b>15%</b>（约 72K）→ 模型失效，且十倍仓已爆；② 若实际只从 84,898 跌 6% 而他按 10% 算，<b>「接近尾声」的时间点被系统性提前</b>。",
      tags: ["周期判断", "目标价", "失效条件"],
      src: "X 原文 @KillaXBT · 2114373165342130507"
    },
    {
      date: "2026-10-25",
      title: "「下周会是多头行情」：一句无条件的周级方向判断",
      quote: "\"Next week will be bullish.\"（<b>下周会是多头行情</b>。）",
      read: "改动的是<b>时间维度的承诺</b>——此前他给的是价位（74K / 79.8K / 80K）和更长周期（126K / 160K），本条是近一个月<b>最短、最硬的时间判断</b>：10-26 至 11-01 这一周偏多。⚠️ 分析：① 事实上这一周<b>没兑现，但也谈不上明显错</b>：10-26 开 80,154、10-29 12:45 约 <b>80,214</b>，七天几乎原地；② 期间先上到 81,823（10-28）再砸到 79,710（10-29），<b>振幅不到 2%</b>，与「bullish」的常规含义（上涨）不符；③ 这条与 10-28 那条「7–10 天 10%+」形成<b>两条并行时间线</b>。失效条件：① 10-26 至 11-01 周线收在 <b>80,154</b>（周开）之下 → 无条件判断落空；② 若该周收平或小跌而他仍称「符合预期」，说明其时间判断<b>不可验收</b>。",
      tags: ["周期判断", "失效条件"],
      src: "X 原文 @KillaXBT · 2114271469987631118"
    },
    {
      date: "2026-10-25",
      title: "「周末破低就是操纵」：用 62K/74K 两次先例给假突破定性",
      quote: "\"They chose to break the lows over the weekend. The easiest time to manipulate price. When the orderbooks are thin & when everyone is likely AFK... The same thing happened at 62K, when 90% were fixated on lower. The same thing happened at 74K, when everyone wanted 72K. The market has a funny way of front running the ideal scenario.\"（<b>他们选择在周末跌破低点</b>——最容易操纵价格的时段，<b>订单簿最薄、大家都在摸鱼</b>的时候……<b>62K 时发生过一次</b>，当时 90% 的人盯着更低；<b>74K 时也发生过</b>，人人都想要 72K。<b>市场总爱抢跑那个「理想剧本」</b>。）",
      read: "改动的是<b>破位的解释权</b>——10-24 他还说「守住前区间、74K 之上做更高低点」，本条把已经发生的<b>周末破低（10-24 低 79,220）</b>定性为「<b>操纵 + 抢跑</b>」，而不是结构破坏。⚠️ 分析：① 这是<b>不可证伪的归因</b>：跌了是操纵，涨了是应验；② 他举的 62K / 74K 两个先例都发生在<b>他自己的建仓区</b>，用「我当时也对」给当前位置背书，属<b>幸存者偏差</b>；③ 「市场总抢跑理想剧本」在逻辑上<b>与他「等更低再接」的策略冲突</b>——若市场总抢跑，他自己 74K 的加仓单同样接不到。失效条件：① 若<b>工作日</b>（量能正常）连续收在 79,200 下方，「周末操纵」说法不成立；② 跌破 <b>74,000</b> → 所有「假突破」先例作废，因为这次成了真突破。",
      tags: ["关键价位", "失效条件", "存疑"],
      src: "X 原文 @KillaXBT · 2114028522746314849"
    },
    {
      date: "2026-10-25",
      title: "「74,000 就是我的爆仓价」：首晒三条成本，跌到就再开十倍",
      quote: "媒体编译稿（非逐字原话，一手原文已核对一致）：「其当前仍持有比特币多头仓位，包括在 62,600 美元、76,000 美元建立的多单，以及在 82,800 美元建立的 10 倍杠杆多单。若 BTC 向下插针并跌至 74,000 美元，导致该 10 倍杠杆多单被平仓，计划在此前设定的失效位再次建立 10 倍杠杆多单，但仓位规模会更小，因为其在该价格区域已有较多敞口。」「若没有已经持有大量多单和现货，他会在当前价位积极买入……他宁愿提前入场，也不愿错过后续更大的行情。」——配图未逐张读取。",
      read: "改动的是 <b>74K 的角色</b>——10-19 他说的是「<b>我不认为会看到扫 74K</b>」，那是一句口头判断；本条等于承认 <b>74,000 就是他 82,800 十倍仓的爆仓线</b>（10 倍、-10% 即约 74.5K，与 74,000 基本吻合），而且不是止损离场、是<b>在同一个失效位再开一笔「更小的」十倍</b>。失效位被正式改写成<b>加仓位</b>，这是本库第一次出现他对自己亏钱的仓位给<b>二次加杠杆预案</b>。⚠️ 分析：① <b>价格已经先一步破了他的说法</b>：币安日线 10-24 最低 <b>79,220</b>、10-25 最低 <b>79,845</b>、10-26 盘中最低 <b>79,368</b>，他 10-19 划的周线低 <b>79,813</b> 与 10-23 说的「<b>80K is the area</b>」都已被扫穿，只剩收盘没收下去；② 62,600 / 76,000 两笔成本极低，他确实扛得住，但 82,800 那笔正在浮亏，<b>公开爆仓价等于把自己的容错边界交给市场</b>；③ 「仓位更小」听着像风控，实质是<b>同一区域二次上杠杆</b>——真跌到 74K 后若继续去 70K 一带，两笔十倍同时亏，与他自己「never sub 70K」直接对撞；④ 「宁愿提前入场」是他<b>第一次承认自己的入场上限偏早</b>，此前他只讲「扫针就接」，不讲成本。失效条件：① 日线<b>收在 74,000 下方</b>且不插针回收 → 他按自己的说法要再开十倍，那就是在下跌趋势里加仓，不是风控；② 价格真到 74K 而他<b>没有</b>再开，「说到做到」这条先作废（比价格更先可验证）；③ 若价格不回 74K 一路上行，本条无法被价格检验，只能当<b>仓位透明度</b>记录。",
      tags: ["仓位建议", "关键价位", "失效条件"],
      src: "X 原文 @KillaXBT · 2114345985862209893（原按媒体稿录入，本轮补齐一手 ID）"
    },
    {
      date: "2026-10-25",
      title: "「极端低点未必重演」：把 -9% 定性成好回撤，改推分周定投",
      quote: "媒体编译稿（非逐字原话，一手原文已核对一致）：「除非接下来出现更多负面消息，否则不应将比特币此前的极端低点视为必然会再次触及的目标，历史走势也不一定会简单重演。」「当时的『清算下影线』出现于多重利空集中爆发之际，比如美联储释放鹰派暂停加息信号等，第四季度买家似乎仍在等待更低的入场价格。」「建议投资者在未来几周继续通过定投（DCA）买入 BTC，比特币目前已回调约 9%，在他看来，这已是牛市中的一次不错的回撤。」——配图未逐张读取。",
      read: "改动的是<b>入场方式与「等成本」的逻辑</b>——10-21 到 10-24 他给的全是<b>精确价位</b>（76.8–80.8K 网格、80K is the area、扫针就接），本条把动作换成<b>时间维度</b>：「未来几周继续定投」。同时把「此前那根极端低点的清算下影线」从「可能再摸」降级为「<b>多重利空同时爆发才形成、不必重演</b>」——这句话表面在讲历史，实际是给<b>自己 74K 那条不留退路的仓位减压</b>：先论证那个价不必再去，后面的爆仓线就没那么可怕。⚠️ 分析：① 「<b>回调约 9%</b>」的基线他没给，无法核对——从 10-21 高点 84,898 到 10-25 低 79,845 只有 <b>-6%</b>，从 87K 段算才接近 -9%，取哪个高点决定这句话成不成立；② 「<b>除非出现更多负面消息</b>」等于把失效条件外包给新闻流，而本周正好是<b>美联储 / 欧央行 / 日本央行三场议息 + 油价高位</b>的窗口，「更多负面消息」出现的概率并不低；③ 与他 10-23「低点总在多数人以为要破的时候被守住」并列已经不成立——<b>79,813 已经破了</b>（10-24 低 79,220），规律本身被价格否掉。失效条件：① 本周央行放鹰、BTC 日线<b>收在 79,200 下方</b>，「-9% 是不错回撤」当场变成下跌中段的自我安慰，DCA 就是逆势摊平；② 若价格真回到 74K 一带，这句「不必重演」直接翻车，并同步引爆十倍仓；③ 他没给 DCA 的<b>节奏、总额、止损</b>，属于纯口号，无法验收。",
      tags: ["仓位建议", "周期判断", "存疑"],
      src: "X 原文 @KillaXBT · 2114316038200578293（原按媒体稿录入，本轮补齐一手 ID）"
    },
    {
      date: "2026-10-24",
      title: "「Long. The. Sweep.」：逐字确认扫针接多",
      quote: "\"Long. The. Sweep.\"（<b>做多。这波。扫针。</b>）——本条无配图，纯文字，单词逐点强调。",
      read: "改动的是<b>动作的确定性</b>——10-23 说「80K is the area」是区域、10-24 说「可能还有一次扫针」是预期；本条在周末破低（低 79,220）之后，用<b>三段式断句</b>把「扫针 → 做多」定成已执行的动作。⚠️ 分析：① 这是本库少数<b>把执行时点写进原文</b>的条目，可与价格直接对齐：10-24 低 79,220、收 80,888，<b>当周确实收在 79.2K 之上</b>；② 但没说仓位、没说杠杆、没说止损，<b>不可复制</b>；③ 与 10-13 的 82,860 十倍单、10-25 的 74K 爆仓线并读，<b>「long the sweep」很可能就是那笔十倍单的加仓</b>（他后来自述 82.8K 是「激进十倍」）。失效条件：① 若扫针之后未能站稳 <b>79,200</b>，「扫针接多」变成接刀；② 破 <b>74,000</b> → 本条动作被清算，判断与执行双输。",
      tags: ["仓位建议", "关键价位", "战绩复盘"],
      src: "X 原文 @KillaXBT · 2114022315532972372"
    },
    {
      date: "2026-10-24",
      title: "「和 2023 一模一样」：复刻剧本首次点名 74K 之上的更高低点",
      quote: "\"Spitting image of 2023. Once $BTC broke above the range and printed a weekly higher high, it never fell back below the previous high. Instead, it went on to form a higher low. If we see a similar pattern this time, there's a scenario where BTC holds above the previous range and forms a higher low above the 74K low. The trend remains very much bullish.\"（<b>和 2023 年一模一样</b>。当年 BTC <b>突破区间、打出周线更高高点</b>之后，<b>再也没跌回前一个高点下方</b>，而是继续<b>做出一个更高的低点</b>。如果这次重复同样的形态，那么存在这样的情形：BTC <b>守住前一个区间</b>，并在 <b>74K 这个低点之上</b>形成更高的低点。<b>趋势仍然非常看多</b>。）——本条无配图，纯文字。",
      read: "改动的是他<b>2023 复刻剧本的验收门槛</b>——10-13 的说法是「必须在 <b>75.5K 上方</b>形成更高低点、最好守住 80K」；本条把参照低点从 75.5K <b>下移到 74K</b>，并把「复刻」拆成两个条件（守住前区间 + 在 74K 之上做更高低点）。等于用更低的门槛换更大的成立概率。⚠️ 分析：① <b>74K 这个数字他没说明对应哪一段的低点</b>，本轮日线最低只到 <b>80,451</b>（10-24），无法核对 74K 从哪来；② 「spitting image」是形态类比，样本只有 2023 一次，<b>n=1 不构成统计证据</b>；③ 与他 10-19「never sub 70K」、10-21「76.8–80.8K 网格」拼起来，<b>74K 正好卡在网格下沿之下、70K 之上</b>，同时贴着 10 倍仓失效价 <b>74,550</b>。失效条件：① 周线收在 <b>80K</b> 下方并继续走低，「holds above the previous range」的前提直接不成立；② 跌破 <b>74K</b> → 「在 74K 之上做更高低点」被价格否定，同时触发他自家 10 倍仓的失效线；③ 他没给时间窗，这个类比从 10-13 讲到 10-24 已 11 天，可无限顺延。",
      tags: ["基准剧本", "关键价位", "周期判断"],
      src: "X 原文 @KillaXBT · 2113941069599588836"
    },
    {
      date: "2026-10-24",
      title: "「别把话说歪了」：自证熊市全程看空、底部翻多、现在仍多",
      quote: "\"Talk all you want. I was bearish throughout the entire $BTC bear market, then bullish right at the bottom. I'm still bullish. Don't get things twisted.\"（<b>随你们怎么说</b>。整段 BTC 熊市里我<b>一直是空头</b>，然后<b>正好在底部翻多</b>。我现在<b>仍然看多</b>，<b>别把话给我说歪了</b>。）——本条无配图，纯文字。",
      read: "改动的是<b>叙事归属权</b>而不是价位——把「Killa 是个死多头」的质疑改写成「我在熊市全程看空、在底部精准翻多」，用<b>择时能力</b>给自己的持仓背书。可核对的部分只有一半：他 10-18 / 10-19 确实公开看多，但「整个熊市都在看空」在本库 <b>180+ 条收录里找不到对应原文</b>，反而他 10-11 就给过「2029 年 160–180K 顶部」这种跨周期看多判断。⚠️ 分析：这条出现在价格从 84,898 跌回 <b>80,451</b> 的档口，功能是<b>稳心态、稳住跟随者</b>，不是新信息。失效条件：① 若价格跌破 <b>74K</b> 而他仍在喊多，「right at the bottom」的定性被价格直接否掉；② 纯立场声明，<b>无价位、无仓位、无时间</b>，按他自己的验收标准完全不可执行。",
      tags: ["战绩复盘", "存疑"],
      src: "X 原文 @KillaXBT · 2113737979479065069"
    },
    {
      date: "2026-10-24",
      title: "「Déjà vu」：把 10 月低点直接定性成「那就是底」",
      quote: "\"Déjà vu is like your brain remembering a moment that hasn't happened before. Trust your gut... cause that was indeed, the bottom.\"（<b>既视感</b>就像大脑在<b>回忆一件还没发生过的事</b>。<b>相信你的直觉</b>……因为<b>那就是底</b>。）——配图状态未取到（详情页探测中断）。",
      read: "改动的是<b>底部确认的状态</b>——10-19 他给 83.6K 时用的是「<b>区间式投降 / 反转</b>」的二值开关，意思是<b>还没确认反转</b>；本条直接宣布「<b>that was indeed the bottom</b>」，从「等确认」跳到「已确认」。而中间<b>没有任何新的价格证据</b>：10-22 收 81,416、10-23 收 81,189，比 10-21 的 84,093 低了约 3%。⚠️ 分析：① 「déjà vu」是<b>不可证伪的知觉</b>，用它替代结构证据，等于把判断降级成感觉；② 与同日 18:30 那条「74K 之上做更高低点」并置看，是<b>先宣布底、再补条件</b>，顺序反了。失效条件：① 日线收在 <b>80,451</b>（10-24 低点）之下并继续扩张，「那就是底」被自己的区间下沿否掉；② 若真跌到 74K，底的位置要整体下移一档，这条须自我修订。",
      tags: ["情绪指标", "周期判断", "存疑"],
      src: "X 原文 @KillaXBT · 2113694190441759045"
    },
    {
      date: "2026-10-24",
      title: "「还要涨很多」：把看多身份绑到「只有现货才算多头」",
      quote: "\"All you need to know is, We're going a lot fucking higher. Leverage has ruined people. Nobody's holding $BTC spot. They're all overleveraged, PA chasing, adrenaline chasing clowns. That's why you see flip floppers everywhere. Nobody wants price to move in a straight line because they know they won't catch it with leverage. The only people who are genuinely bullish are the ones who actually hold spot.\"（你只需要知道一件事：<b>我们还要涨很多</b>。<b>杠杆把人毁了</b>。<b>没人拿现货</b>，全是<b>过度杠杆、追价格行为、追肾上腺素的小丑</b>——所以你到处看到<b>立场翻来覆去的人</b>。没人希望价格<b>走直线</b>，因为他们知道自己<b>用杠杆根本吃不到</b>。真正看多的人，<b>只有那些真拿着现货的</b>。）——配图为图表（已确认带图，未逐张读图）。",
      read: "改动的是<b>看多论据的类型</b>——10-20 他用资金面（USDC 月增发 52 亿）、10-22 用 USDT.D 结构，本条换成<b>持仓者结构论</b>：只有现货持有者才是真多头，杠杆客都是噪音。实际功能是把「为什么还没涨」解释成「杠杆太多、没人愿意直线拉升」，属<b>不可证伪的归因</b>——涨了是他对，不涨是杠杆客的错。⚠️ 分析：① 「going a lot fucking higher」<b>无幅度、无时间、无价位</b>；② 与他自己的操作矛盾——他 10-13 开的是 <b>10 倍杠杆</b>（82.860 那笔），本条却骂杠杆客，属<b>双标</b>；③ 「只有现货才真看多」在逻辑上把他自己也排除在外。失效条件：① 若后续放量直线上涨而 OI 同步创新高，「杠杆毁人」的框架自破；② 若他再公开晒杠杆加仓，这条的立场声明失效。",
      tags: ["情绪指标", "仓位建议", "存疑"],
      src: "X 原文 @KillaXBT · 2113662734092865690"
    },
    {
      date: "2026-10-23",
      title: "「80K 就是那个区域」：区间底确立，改成只做多扫针",
      quote: "\"I've said this plenty of times before, in a bull market, you long the sweeps within the range. But people keep failing to do it. They're fixated on the corrective scenario because we've only just come out of a bear market full of fakeouts. Now they assume every rally is going to result with a fakeout. The range and base are established. 80K is the area. Could we see another sweep? Possibly. But eventually, we won't, and $BTC will move higher without you. Trade the fucking trend.\"（这话我说过很多次：<b>牛市里，就在区间内做多扫针</b>。但人总是做不到。他们死盯着<b>回调剧本</b>，因为刚从一个充满假突破的熊市里出来，于是假设<b>每一次拉升都是假突破</b>。<b>区间和底部已经确立了</b>，<b>80K 就是那个区域</b>。还会不会有再一次扫针？<b>有可能</b>。但最终不会有了，<b>BTC 会在你没有仓位的时候往上走</b>。<b>顺着趋势做</b>。）——配图为图表（已确认带图，未逐张读图）。",
      read: "改动的是<b>入场方式与区间定义</b>——10-21 他给的是 <b>76.8–80.8K 的网格区间</b>，本条把区域收窄成一个点「<b>80K is the area</b>」，动作也从「网格收租」换成「<b>long the sweeps</b>」（扫针就接、不挂网格）。同时首次<b>承认还可能再扫一次</b>，等于给 80K 下方留了缓冲带。⚠️ 分析：① 「could we see another sweep? Possibly」是他给自己留的<b>免责口</b>——扫了不算错、不扫也不算错；② 「eventually, we won't」<b>没有任何时间约束</b>，与他同日「枢轴就在几天内」的时间表不匹配；③ 80K 这条线 10-15 已被盘中插到 <b>80,226</b>，10-24 再创 <b>80,451</b>，实际是<b>贴着 80K 反复磨</b>，不是「确立后向上」。失效条件：① 日线<b>收在 80K 下方</b>且不收回，「the area」被破，多头框架失去锚；② 他没给扫针深度，79.8K、76.8K 都算「扫针」，执行上无法界定仓位与止损。",
      tags: ["关键价位", "仓位建议", "基准剧本"],
      src: "X 原文 @KillaXBT · 2113634799386824991"
    },
    {
      date: "2026-10-23",
      title: "周期枢轴首次量化：11/11 反向、至少 5% 向上",
      quote: "\"The next major cycle pivot is approaching in a few days. Its consistency has proven itself across 600+ days of price action. 11 out of 11 times, we've seen an inverse move in $BTC against the narrative. Clinical cycles. We're still building a noticeably bearish narrative into this pivot. If it follows the pattern of every pivot before it, that points to an inverse move to the upside for BTC, likely at least 5% in the opposite direction. We might not see a major move just yet, but this is what I'll be watching when the time comes.\"（<b>下一个重要的周期枢轴，就在几天之内</b>。它的稳定性已经在 <b>600 多天</b>的价格行为里被验证：<b>11 次里有 11 次</b>，BTC 都走出一段<b>与叙事相反的行情</b>。临床级的周期。这次进入枢轴时，市场仍在<b>堆积明显偏空的叙事</b>。如果它重复此前每一次枢轴的形态，那就指向 BTC <b>向上反向运动</b>，幅度<b>很可能至少 5%</b>。也许<b>暂时还看不到大行情</b>，但时间到了，这就是我要盯的东西。）——配图为<b>黑点标注的摆动结构图</b>：纵轴约 75K–105K，最后一个黑点（预期枢轴）落在现价右上方，<b>无日期刻度可读</b>。",
      read: "改动的是「<b>拐点就在这几天</b>」这句的<b>可验收性</b>——10-21 他只说 a few more days，本条第一次给出<b>样本（600+ 天、11/11）、方向（反向于叙事 = 向上）、幅度（至少 5%）</b>，是近期最接近可量化的表述。但两个问题没解决：<b>「几天」是滚动的</b>——10-21 说几天、10-23 还说几天，窗口在往后推；<b>日期依旧没给</b>，配图只有黑点、没有时间轴。⚠️ 分析：① 「11 out of 11」是<b>样本内回测</b>，600 天里只出现 11 次枢轴，<b>样本量不足以支撑「临床级」的说法</b>；② 他自己留了后门「might not see a major move just yet」，事后可解释成「枢轴还没到」；③ 按 10-24 收盘 <b>80,621</b> 算，5% 上行要到约 <b>84,650</b>，正好压在他 10-21 设的 <b>83.7–84.2K</b> 关卡上沿之上——两个预测在这里<b>可交叉验证</b>，是本库少见的能对齐之处。失效条件：① 从 10-24 起<b>5 个交易日内</b>未出现 ≥5% 单边上行（未站上 84.6K），「11/11」的样本外预测失败；② 若枢轴以<b>向下</b>方式兑现（跌破 80,451 加速），他可以说「拐点到了、只是方向向下」，表述两头可解释；③ 跌破 <b>76.8K</b> 网格下沿，「周期枢轴」的看多含义彻底反转。",
      tags: ["周期判断", "目标价", "失效条件"],
      src: "X 原文 @KillaXBT · 2113611898633486717"
    },
    {
      date: "2026-10-23",
      title: "「反复坐电梯才是洗人」：拿 62.6K 十次试探做类比",
      quote: "\"Nothing is more frustrating than watching your position constantly round trip. And this is precisely the type of price action that causes 90% of people to close their winning positions too early. We saw the same thing when price kept bouncing off 62.6k, testing that level at least 10 times before finally making its next leg higher. After rejecting the highs repeatedly, people start losing confidence in their swings. Instead of holding their positions, they begin aggressively scalping the range. Closing, opening, closing, opening. Sure, they might make some money along the way. But when the range finally breaks, they end up missing the very move that would have been the most profitable. This is exactly how the market wears down your conviction. Repeated rejections make you question your positioning, and eventually, you start reacting to every minor fluctuation instead of focusing on the bigger picture. The reality is that catching the larger moves is far more profitable than constantly scalping for peanuts. Stop letting short term price action distract you from what actually matters.\"（没什么比看着持仓<b>反复坐电梯</b>更难受。而这种价格行为，正是让 <b>90% 的人过早平掉盈利仓位</b>的原因。当年价格反复在 <b>62.6K</b> 附近被弹回、<b>至少测试了 10 次</b>才走出下一段，我们见过同样的事。<b>反复被高点拒绝</b>之后，人开始<b>怀疑自己的波段仓位</b>，于是不再持有，而是<b>在区间里疯狂 scalping</b>——平了又开、开了又平。他们当然能赚点钱，但<b>区间最终突破时，他们错过了最赚钱的那一段</b>。市场就是这样<b>磨掉你的信念</b>：反复被拒让你怀疑持仓，最后你对每一个小波动都反应过度，而不看大图。<b>吃大行情远比抠小钱赚钱</b>。别让短期价格行为分散你对真正重要的事的注意力。）——本条无配图，纯文字。",
      read: "改动的是<b>他给持有者的操作指令</b>——10-20 他还在公开教「<b>周一扫针后做空吃 1–3%</b>」，本条反过来骂「<b>在区间里反复 scalping 的人会错过突破</b>」，指令从「做区间」翻转成「别做区间、拿住波段」。⚠️ 分析：① 这条与他<b>自己 10-21 给的 76.8–80.8K 网格</b>直接冲突——网格本身就是机械化高频进出，正是他这里骂的行为；同一账号在 48 小时内既劝人挂网格、又骂人 scalping；② 62.6K 的类比属<b>事后挑选成功样本</b>：那次确实在第 10 次试探后突破，但他没提历史上还有多少次「试探 10 次后直接破位」。失效条件：① 若区间再横 2–3 周不破，「拿住」的机会成本持续放大，而网格反而在赚钱，本条实操价值归零；② 若价格跌破 <b>80,451</b> 向下扩张，「反复被拒后向上突破」的类比方向就反了。",
      tags: ["仓位建议", "周期判断", "存疑"],
      src: "X 原文 @KillaXBT · 2113586518996423078"
    },
    {
      date: "2026-10-23",
      title: "「挂网格、接低点、别看小周期」：把中期选举当前提",
      quote: "\"Lots of people are waiting for $BTC to sweep the lows. Let's see if a systematic algo steps in and front runs those orders again. That's been the pattern for a while now: the lows get defended just when most people expect them to break. The next couple of weeks should be interesting, especially with the midterms approaching. You already know my view. Set up a grid bot, bid the lows, and completely ignore the LTF price action.\"（很多人在等 BTC <b>去扫低点</b>。看看这次会不会又有<b>系统性算法</b>插进来，<b>抢在他们前面吃掉这些挂单</b>。这阵子的规律一直是这样：<b>就在多数人以为要破的时候，低点被守住</b>。<b>接下来几周会很有意思</b>，尤其是<b>中期选举</b>临近。我的观点你早就知道：<b>挂个网格机器人，在低点挂买单，完全无视小周期价格行为</b>。）——配图为图表（已确认带图，未逐张读图）。",
      read: "改动的是<b>执行工具与近期催化剂</b>——首次明确让人「<b>set up a grid bot</b>」，并首次把<b>中期选举（≈11-03）</b>写进近期剧本，替代 10-20 的「CPI」和 10-15 的「14 号枢轴」当主催化剂。同时把「低点总在多数人以为要破的时候被守住」提炼成<b>可重复的规律</b>。⚠️ 分析：① 与同日 19:01「别在区间里 scalping、要拿住」<b>正面冲突</b>——网格就是机械 scalping，两条间隔仅 3 小时；② 网格<b>没给上下沿</b>，等于没给风险边界，与 10-21 明确写 76.8–80.8K 的版本相比是倒退；③ 「低点被守住」是<b>结果论</b>，10-24 已到 80,451，离 10-17 周线低点 <b>79,813</b> 只剩 0.8%。失效条件：① 日线收在 <b>79,813</b> 下方 → 「lows get defended」的规律当场破；② 中期选举后若继续走弱，「next couple of weeks」的时间窗作废；③ 若他自己不真跑网格，「my advice」就只是话术。",
      tags: ["仓位建议", "宏观驱动", "关键价位"],
      src: "X 原文 @KillaXBT · 2113327422812672438"
    },
    {
      date: "2026-10-23",
      title: "「还在翻转过的周线高点上方」：用 FUD 清单当抗跌证据",
      quote: "\"Despite all the chatter, we're still trading above the same weekly highs we flipped. They're throwing every bit of FUD in the book at the market, and this is still what the chart looks like. Not to mention, we are literally in a bull market. $BTC\"（<b>外面吵得再厉害</b>，我们<b>仍然在那些被我们翻转的周线高点上方</b>交易。他们把<b>书上所有 FUD 都扔向市场</b>了，而图表还是这个样子。更别说，我们<b>实打实处在牛市里</b>。$BTC）——配图为图表（已确认带图，未逐张读图）。",
      read: "改动的是<b>抗跌论据的层级</b>——10-16 至 10-20 他用的是「利空清单 + 价格没跌」这种<b>情绪面抗跌论</b>，本条升级成「<b>结构未破</b>」：价格仍在翻转过的周线高点之上。⚠️ 关键问题：<b>他没说是哪一条周线高点</b>，无法核对——10-19 那周周线开盘是 <b>83,774</b>，10-21 日线收 84,093（在其上），但 10-22 收 <b>81,416</b>、10-23 收 <b>81,189</b>，<b>已经落回 83.7K 周开下方</b>。若他指的就是这一条，本句在发出时已不成立。② 「literally in a bull market」是<b>定义之争</b>，不是证据。失效条件：① 若所指为 <b>83.6–84.2K</b> 那条（10-21 刚「翻转」的），本句已被 10-22 收盘否定；② 若指更低的 80K 一带区间高点，则「仍在牛市」要等 <b>80K 日线收破</b>才被证伪；③ 无价位、无图注，属不可核实表述，收录按<b>存疑</b>处理更稳妥。",
      tags: ["关键价位", "存疑", "趋势切换"],
      src: "X 原文 @KillaXBT · 2113317046310072628"
    },
    {
      date: "2026-10-22",
      title: "一句话嘲讽：「上次 75K 没人做多，现在又想要了」",
      quote: "\"They didn't long 75K the last time, now they want it again.\"（<b>上次 75K 他们没做多，现在又想要了</b>。）——本条无配图，纯文字。",
      read: "改动的是<b>他对 75K 的定位</b>——10-15 他还把「也许会测 75K」写成<b>平等可能</b>（并劝人别等回调），本条把 75K 定性成「<b>上次白给、没人要，现在又来求</b>」的错失位，等于<b>明确不打算再等 75K</b>。⚠️ 分析：74–75K 现在被他自己架在<b>夹层</b>里——既是 10-24 那句「74K 之上做更高低点」的下沿，也是 10 倍仓失效价 <b>74,550</b> 所在；嘴上说这是「不该等的价」，仓位却在这里失效，<b>话术与风控分离</b>。失效条件：① 若价格真回到 75K 一带（距 10-24 低点 80,451 约 <b>6.8%</b>），这条从预警变成事后嘲讽，且他必须在 74,550 认输；② 纯一句话，<b>无价位、无仓位</b>，不可执行。",
      tags: ["关键价位", "情绪指标"],
      src: "X 原文 @KillaXBT · 2113279201499590963"
    },
    {
      date: "2026-10-22",
      title: "承认 PWO 翻转失败：仍在区间，建议照旧接扫针",
      quote: "\"Unfortunately $BTC was unable to flip the PWO. Not the strongest candle. We're still range-bound. They're definitely making things uncomfortable for anyone trying to catch the next move. My advice is the same, just keep bidding the sweeps.\"（很遗憾，BTC <b>没能翻转 PWO（上周开盘价）</b>。<b>不是一根强 K</b>。我们<b>仍在区间里</b>。他们确实在<b>让所有想抓下一波的人难受</b>。我的建议照旧：<b>继续在扫针处挂买单</b>。）——配图为图表（已确认带图，未逐张读图）。",
      read: "改动的是<b>他 10-21「开始吃空头」那波的验收结论</b>——10-21 他把 <b>83.7–84.2K</b> 设成「第一道重要关卡」，说翻转成功才谈回前高；本条由他本人承认 <b>PWO 没翻转</b>，并把定性退回「<b>still range-bound</b>」。这是三天里第一次<b>自我确认突破失败</b>。⚠️ 分析：① 承认失败的同时仍维持「<b>keep bidding the sweeps</b>」，即<b>结论不改、只改措辞</b>，10-19 那个判定开关形同虚设；② 10-19 那周周线开盘 <b>83,774</b>，10-22 收 <b>81,416</b>，差 2.8%，这条的承认是诚实的；③ 「they're making things uncomfortable」把区间震荡归因于<b>对手方操纵</b>，是熟悉的<b>责任外化</b>套路。失效条件：① 下周（10-26 起）PWO 仍未被收复，区间剧本延续，他 10-23「枢轴 5% 上行」须另找理由；② 若 80K 收破，「bidding the sweeps」变成<b>接飞刀</b>。",
      tags: ["关键价位", "失效条件", "基准剧本"],
      src: "X 原文 @KillaXBT · 2113261734572245287"
    },
    {
      date: "2026-10-22",
      title: "USDT.D 破位首次日线 BOS 回测：守住则看 87K 以上",
      quote: "\"For bears, the major area held. For bulls, will the major area reject? Let's see. So far, USDT.D has broken down and is now coming into its first BOS retest on the daily TF. Technically speaking, if it remains below this orange area, $BTC could make a leg up to new highs above 87K. Losing this area would mean we remain rangebound and likely take liquidity at the highs on USDT.D, while BTC revisits the lows yet again. Overall, this is the key area for bulls to watch if we're going to maintain the uptrend.\"（对空头来说，<b>关键区域守住了</b>。对多头来说，<b>这个关键区域会不会反过来压制？</b>拭目以待。到目前为止，<b>USDT.D 已经破位</b>，现在正走<b>日线级别第一次 BOS 回测</b>。技术上讲，<b>只要它待在这个橙色区下方，BTC 就可能走出向上一段、创出 87K 以上的新高</b>。<b>丢掉这个区域</b>，就意味着<b>继续区间震荡</b>，USDT.D 大概率去取上方流动性，而 BTC <b>再一次回探低点</b>。总体而言，这是多头要盯的<b>关键区域</b>——如果我们想维持上行趋势的话。）——配图为 USDT.D 图表（已确认带图，未逐张读图）。",
      read: "改动的是<b>目标价的重新挂出</b>——把 10-14 说过的「上方猎 <b>87–88K</b>」重新摆上台面，并首次给出<b>可核对的触发器</b>：USDT.D 留在橙色区下方 → BTC 上攻 87K+；丢区 → 区间延续 + BTC 再探低。这是他近期<b>少见的双向条件式</b>表述，比同期单边喊多可验收得多。⚠️ 分析：① 87K 与他 10-21 的 126K / 150K 目标之间<b>没有中间路径</b>，属不同时间尺度混用；② 「orange area」的数值只在图上，文字没给，<b>外部无法独立核对</b>。失效条件：① USDT.D 站回橙色区上方 → 87K 目标作废，回到区间下沿剧本；② 若 USDT.D 在区下方而 BTC 仍跌破 80,451，说明<b>跷跷板关系已断</b>，整个框架失效；③ 87K 若在 11 月前未触及，「a leg up」的时效性消失。",
      tags: ["目标价", "关键价位", "失效条件"],
      src: "X 原文 @KillaXBT · 2113109977439068212"
    },
    {
      date: "2026-10-22",
      title: "USDT.D 第一道关口被测：空头不愿见它破",
      quote: "\"The first major barrier has now been tested. This is a critical level for bears. They don't want to see it break, because that could open the door for $BTC to trend toward a new high, and potentially push even higher. USDT.D could see a dead cat bounce from here, but the broader trend remains bearish. Observe.\"（<b>第一道主要关口现在已经被测试过了</b>。对空头来说这是<b>关键位</b>——他们<b>不希望看到它被跌破</b>，因为一旦破，就可能为 BTC <b>打开通往新高的门</b>，甚至<b>推得更高</b>。USDT.D 从这里可能出现<b>死猫跳</b>，但<b>更大级别的趋势仍然是向下的</b>。<b>观察</b>。）——配图为图表（已确认带图，未逐张读图）。",
      read: "改动的是<b>USDT.D 在他框架里的权重</b>——10-17 他只是拿 USDT.D 讲「74K 上方更高低点」，本条把它升级成<b>BTC 方向的先行指标</b>（空头的关键位、破了就开新高的门）。这是他叙事里少见的<b>可跨品种独立核对</b>的条件。⚠️ 分析：① 他自己先说「可能有死猫跳」，等于给反弹<b>预留免责</b>——弹了是死猫跳、不弹是趋势延续，两头都对；② 「barrier」的价位只在图上，文字没给；③ 本条与同日 87K 目标那条是<b>同一条逻辑的两步</b>，不是两个独立信号，别重复计权。失效条件：① 若 USDT.D 反弹后<b>站稳</b>在关口上方，BTC 新高的门就没打开，本条作废；② 若 USDT.D 继续跌而 BTC 也跌，说明<b>相关性断裂</b>，该框架整体失效。",
      tags: ["宏观驱动", "关键价位", "存疑"],
      src: "X 原文 @KillaXBT · 2113046102236713163"
    },
    {
      date: "2026-10-22",
      title: "「黑色星期一在哪」：拿空头的崩盘剧本开嘲讽",
      quote: "\"Is black Monday in the room with us?\"（<b>「黑色星期一」是跟我们待在同一个房间吗？</b>）——本条无配图，纯文字。",
      read: "改动的是<b>他对空头叙事的处理方式</b>——10-21 他还在用 ANSEM 归零案做<b>信用修补</b>，本条直接把「黑色星期一」当笑话讲，等于宣告<b>空头那个崩盘剧本已被价格否掉</b>（10-21 收 <b>84,093</b>，是 10-18 以来最高收盘）。⚠️ 分析：这条<b>零信息量</b>，唯一价值是<b>时间标记</b>——他把 10-20 至 10-21 的下跌定性成「没发生过的事」。按收录惯例保留，但只作情绪取样。失效条件：① 若随后出现单日大幅下跌，「黑色星期一」的嘲讽<b>反成反向指标</b>；② 无价位、无仓位，不可执行。",
      tags: ["情绪指标", "存疑"],
      src: "X 原文 @KillaXBT · 2113009643983130999"
    },
    {
      date: "2026-10-21",
      title: "14 号枢轴自评兑现：「又一次证明谁在掌控这游戏」",
      quote: "\"I remember how many people questioned my 14th pivot. They lost conviction. They started second guessing, thinking, 'Surely Killa will be wrong this time?' Yet again, we saw a clear bearish move into my date, followed shortly after by the inverse move. Once again, I've shown you who runs this game... $BTC\"（我记得<b>有多少人质疑我 14 号那个枢轴</b>。他们<b>丢了信念</b>，开始自我怀疑，心想「<b>这次 Killa 总该错了吧</b>？」结果又一次：<b>进入我给的日期时是明确的下跌，随后不久就走出了反向行情</b>。又一次，我让你们看到<b>谁在掌控这个游戏</b>……$BTC）——本条无配图，纯文字。",
      read: "改动的是<b>他的战绩叙事</b>——把 10-14 那个枢轴（当时他说「14 号之后更可能看多、延续到本月剩余时间」）记为<b>已兑现</b>。可核对的一半成立：10-14 收 <b>81,682</b> → 10-21 收 <b>84,093</b>，确实是上行；但「<b>跌进日期后马上反向</b>」的机制仍然只是<b>事后叙事</b>，没有事前定义的判定标准。⚠️ 分析：① 「很多人质疑我」属<b>不可核实的群体指称</b>，无法查证；② 这条是他 10-23 那套「<b>11/11 枢轴必反向</b>」统计说法的<b>情绪铺垫</b>——先立人设、再上数据；③ 「谁在掌控这个游戏」是典型<b>权威型话术</b>，不提供任何可操作信息。失效条件：① 若「延续到本月剩余时间」被否定（10-24 已跌到 80,621，本月只剩一周），战绩认定要打折；② 下一个枢轴若失败，「11/11」变「11/12」，整套框架的权威性受损。",
      tags: ["战绩复盘", "周期判断"],
      src: "X 原文 @KillaXBT · 2112936647557877878"
    },
    {
      date: "2026-10-21",
      title: "多空带大幅张开：预告「显著波动很快要来」",
      quote: "\"$BTC Significant volatility should be approaching soon. The long and short bands have widened considerably, creating a much larger gap between them.\"（$BTC <b>显著的波动应该很快就要来了</b>。<b>多空带已经大幅张开</b>，两者之间的<b>差距被拉得很大</b>。）——配图为带多空带的 BTC 图表（已确认带图，未逐张读图）。",
      read: "改动的是<b>他支撑「要动了」的论据类型</b>——同日白天他用的是<b>周期样本</b>（「下一周期拐点就在这几天」），本条换成<b>波动率结构</b>（多空带张开 = 压缩转扩张）。论据的独立性比「11/11」那个样本内回测更强一点。⚠️ 分析：① 只给<b>波动</b>不给<b>方向</b>，技术上可以两头解释（暴涨或暴跌都算「显著波动」）；② 「soon」没有时间上限，比「a few days」更模糊；③ 本条是同日三连发（波动将至 → 吃空头 → 枢轴复盘）的<b>第一环</b>，是那波判断的<b>技术依据</b>而非独立观点。失效条件：① 若带宽继续扩大而价格继续横 1–2 周，「压缩-扩张」的因果不成立；② 若波动以向下方式出现（跌破 80,451 加速），他可以说「波动来了、方向是下」，本条免责；③ 无价位，不可执行。",
      tags: ["周期判断", "失效条件", "存疑"],
      src: "X 原文 @KillaXBT · 2112924116265337294"
    },
    {
      date: "2026-10-21",
      title: "开始吃空头：第一道关卡 83.7–84.2K，翻不上去就继续区间",
      quote: "\"「That means there's a good chance we start taking the other side next week.」 Indeed, we're taking out $BTC shorts now. Our first significant barrier is around 83.7-84.2K. If we fail to flip this area, expect more range bound price action. Reclaim it, and the chances of revisiting the highs increase.\"（「<b>这意味着下周我们很可能开始吃另一侧</b>。」没错，<b>我们现在正在吃 BTC 的空头</b>。<b>第一道重要关卡大概在 83.7–84.2K</b>。<b>翻不上去</b>，就继续<b>区间震荡</b>；<b>收回来</b>，<b>回前高的概率就上升</b>。）——配图为图表（已确认带图，未逐张读图）。",
      read: "改动的是<b>10-19 那个 83.6K 开关的具体形式</b>——从<b>单点 83.6K</b> 扩成 <b>83.7–84.2K 的带状关卡</b>，并首次明确<b>二值结果</b>（reclaim → 回前高概率升 / fail → 继续区间）。开头引用的「下周吃另一侧」是他 10-19 自己说过的话，属<b>承诺兑现</b>而非新判断。⚠️ 实盘核对：10-21 日线高 <b>84,898</b>、收 <b>84,093</b>（收盘落在带内），10-22 收 <b>81,416</b>、10-23 收 <b>81,189</b> → <b>翻转只维持了一个交易日</b>。按他自己的规则，10-22 之后应预期「more range bound」，这与他 10-23 起「还要涨很多」的表述<b>互相打脸</b>。失效条件：① 已部分发生——连续两日收在 83.7K 下方，「reclaim」不成立；② 若之后收盘重回 <b>84.2K</b> 上方，本条重新激活，仍是他手上最干净的一条判定规则；③ 若跌破 <b>80,451</b>，「回前高」整条路径作废。",
      tags: ["关键价位", "仓位建议", "失效条件"],
      src: "X 原文 @KillaXBT · 2112897692573610375"
    },
    {
      date: "2026-10-21",
      title: "USDT.D 看跌回测成型：宏观下行 + BTC 宏观上行 = 更看多",
      quote: "\"Well, well, well... Looks like a bearish retest to me. The structure is confirming a breakdown from 1D/1W resistance, with USDT.D still in a macro downtrend while $BTC remains in a macro uptrend. We retested the BOS, formed yet another lower high, and now the structure is pointing towards a corrective move lower in USDT.D, which would mean further upside for BTC. Let's see if we can keep this trajectory. Trend is your friend.\"（好、好、好……在我看来这像是一次<b>看跌回测</b>。结构正在确认<b>从日线/周线阻力位向下破位</b>，同时 <b>USDT.D 仍在宏观下行趋势</b>里，而 <b>BTC 仍在宏观上行趋势</b>里。我们回测了 <b>BOS</b>，<b>又形成一个更低的高点</b>，现在结构指向 USDT.D 的<b>一轮向下修正</b>——那意味着 <b>BTC 还有上行空间</b>。看看我们能不能保持这条轨迹。<b>趋势是你的朋友</b>。）——配图为 USDT.D 图表（已确认带图，未逐张读图）。",
      read: "改动的是<b>多空归因框架</b>——从「BTC 自身结构」切换到「<b>USDT.D 宏观下行 / BTC 宏观上行</b>」的跷跷板叙事，这是他 10-17 以来 USDT.D 系列表述里<b>第一次完整成型</b>。⚠️ 分析：① 10-21 当天 BTC 先冲到 84,898 再回落，跷跷板<b>当日成立</b>；10-22 收 81,416、10-24 收 80,621，BTC 下行而 USDT.D 是否同步走强<b>本轮未独立核对</b>，若 USDT.D 也跌，框架当场失效；② 他给的是 <b>1D/1W 级别</b>判断，3 天内的波动不构成证伪，属<b>低可验收性</b>表述。失效条件：① USDT.D 反而走强（资金回流美元）→ BTC 上行结论反转；② 若 BTC 跌破 <b>80,451</b> 而 USDT.D 仍在跌，「macro uptrend」的定性被否定；③ 「trend is your friend」是口号，不构成条件。",
      tags: ["宏观驱动", "周期判断", "存疑"],
      src: "X 原文 @KillaXBT · 2112881376986808801"
    },
    {
      date: "2026-10-21",
      title: "「ANSEM 已 -75%」：借别人的票爆掉，划清「交易员 vs 提取者」界线",
      quote: "\"The $ANSEM rug pull. Handed to you on a silver platter. Down -75% since. I tried to warn you, these people are max extractors. They are not traders lmao.\"（<b>$ANSEM 的抽地毯</b>。当初是<b>端到你面前的银盘子</b>。从那之后已经<b>跌了 75%</b>。我<b>警告过你</b>——这帮人是<b>极致的提取者</b>，他们<b>根本不是交易员</b>，笑死。）——本条无配图，纯文字。",
      read: "改动的是他<b>给标的的方式</b>——10-17 他给的是一份自己挑的买区清单（SOL 97–103 / LTC 56–59 / ASTER 0.66–0.7 / BNB 722–680），每条都有价位可执行；本条第一次把<b>别人喊的票</b>拿出来当反面标本，等于给「跟谁做」划线：<b>跟结构，别跟喊单的人</b>。⚠️ 分析：① 现有 160 条收录里<b>没有任何 ANSEM 的推荐或预警记录</b>，「I tried to warn you」在公开时间线上<b>找不到对应原文</b>，属自述口径、不可核实；② 「max extractors」把亏损归因于<b>对手方动机</b>而不是自己的判断，是典型的<b>责任外化</b>，与他 10-18「讲不通才涨」同属不可证伪叙事；③ 这条真正的功能是<b>信用修补</b>——在连续十天死扛的区间里，用别人的惨案反衬自己「没接山寨垃圾」。失效条件：① 若 ANSEM 从 -75% 位置反弹数倍，「rug」的定性被价格否定；② 本条<b>无任何价位与仓位指向</b>，按他自己的验收标准完全不可执行，只能当立场声明；③ 若他随后自己推荐的同类低市值标的也爆掉，「提取者」的指控反噬自身。",
      tags: ["山寨", "战绩复盘", "存疑"],
      src: "X 原文 @KillaXBT · 2112638478400008459"
    },
    {
      date: "2026-10-21",
      title: "「126K 只是起跑线」：目标抬到 150K+，顺手给下轮熊市定底",
      quote: "\"The funny part is when $BTC blasts through 126K. You will never see it trade under 100K again. The math checks out, especially if this cycle bottomed after -54%. BTC only needs to test 150K+ this cycle for the bear-market retrace to potentially be just 40–45%. So whoever's been mindlessly TWAP selling this range, I can assure you, you'll be buying my bags when BTC is 0.15M per coin.\"（好笑的是等 <b>BTC 冲穿 126K</b> 之后——你就<b>再也见不到它在 100K 以下成交</b>了。这笔账<b>算得通</b>，尤其是本周期已经在 <b>-54%</b> 就见底的前提下。BTC 本周期<b>只需要摸到 150K 以上</b>，下一轮熊市的回撤就可能<b>只有 40–45%</b>。所以那些在这个区间里<b>无脑 TWAP 卖</b>的人，我可以保证：等 BTC <b>15 万美元一枚</b>时，<b>你买的正是我的货</b>。）——本条无配图，纯文字。",
      read: "这条同时改了他<b>两个层级的数</b>：① <b>126K 从终点降级为起点</b>——10-18 他的承诺是「<b>126K 之前一分钱不平</b>」，言下之意 126K 就是出货区；本条改成「冲穿 126K」只是入场券，真正的本周期目标是 <b>150K+（0.15M）</b>，比他 10-11 给的「2029 年 160–180K 顶部」整整提前了一个周期。② 首次把<b>回撤深度</b>从论据变成<b>预测工具</b>：150K ×（1−45%）≈ <b>82.5K</b>，等于他提前给下一轮熊市定了 <b>82–90K</b> 的底——而这个数字<b>正好是他现在被套的区间</b>。⚠️ 分析：① 「never trade under 100K again」是<b>带条件的</b>（前提是先冲穿 126K），不是新的绝对底，别和 10-18 的「never sub 70K」混为一谈；② 「the math checks out」只算了幅度没算时间，他原文用的是 <b>only needs to test</b>（只需摸到），语气是必要条件而非承诺；③ 同一天早些时候他刚给出 <b>76.8–80.8K 的网格区间</b>，与本条「马上冲 126K」是两套时间尺度的剧本：前者管本周怎么做，后者管本周期去哪，读的时候不能混。失效条件：① 若价格先跌破 <b>76.8K</b>（他自己网格的下沿），「冲穿 126K」的路径被打断，「never under 100K」的前提<b>根本不会成立</b>；② 150K 若在 2026 年内未触及，与他自己的「周期提前」时间表冲突；③ 「你在 0.15M 买我的货」属仓位炫耀，无凭据、<b>不可核实</b>。",
      tags: ["目标价", "周期判断", "关键价位"],
      src: "X 原文 @KillaXBT · 2112602017692889402"
    },
    {
      date: "2026-10-21",
      title: "「下一个周期拐点就在这几天」：把 due time 收紧成可验收窗口",
      quote: "\"In due time, $BTC will make its move. The next major cycle pivot is in a few more days.\"（<b>时机到了</b>，BTC 自然会动。<b>下一个重要的周期拐点，就在这几天之内</b>。）——本条无配图，纯文字。",
      read: "改动的是他<b>给自己剧本设的时间约束</b>——10-19 的说法是「时间型投降……<b>它还会再来一次，只是时间问题（in due time）</b>」，in due time 是个<b>无期限</b>的挡箭牌；本条第一次给同一个词接上具体窗口「<b>a few more days</b>」，并把「make its move」升级成「<b>cycle pivot</b>」（周期拐点），措辞从「会涨」变成「<b>周期要转向</b>」。⚠️ 分析：① 这是他连续十天情绪贴里<b>第一条可以被时间证伪的表述</b>，信息价值高于前面所有喊话；② 但「cycle pivot」<b>没定义方向</b>——拐点可以是向上收复 83.6K，也可以是向下破 79.8K 转熊，他默认读者理解成向上，表述本身是空的；③ 真要验收的不是「几天」，而是配套 10-18 的判定开关：<b>83.6K 有没有被收复</b>。失效条件：① 3–5 个交易日内价格既未收复 <b>83.6K</b>、也未跌破 <b>79.8K</b>，「这几天」自动降级为又一次无限期推迟，与 10-19 的 due time 再无区别；② 若拐点以<b>向下</b>方式出现（跌破 79.8K 并向下扩张），他这句话可以两头解释，等于免责；③ 若 <b>76.8K</b> 网格下沿被击穿，「周期拐点」的看多含义彻底反转。",
      tags: ["周期判断", "失效条件", "基准剧本"],
      src: "X 原文 @KillaXBT · 2112576818629005687"
    },
    {
      date: "2026-10-20",
      title: "「99% 会在区间里失控，只有 1% 吃到下一段」：把死扛说成筛选",
      quote: "\"They're doing a great job of making 99% of the market lose their shit in this range. Only 1% will catch the next leg. Holding through this kind of crap is brutal... but this is what it takes to stay positioned for the big moves. It'll be worth it in the end. Pay-tience.\"（他们把 <b>99% 的市场</b>在这个区间里<b>逼到心态爆炸</b>这件事做得非常成功，<b>只有 1% 能吃到下一段</b>。<b>扛过这种垃圾行情</b>很残酷……但想留在大行情的车上，这就是必须付的代价。<b>最后会值的。耐心（pay-tience）</b>。）——本条无配图，纯文字。",
      read: "改动的是他<b>对「扛」的定义</b>——10-19 他把这段行情叫「时间型投降」，主语是<b>市场在洗人</b>；本条把「扛住」升级成<b>身份筛选</b>（99% vs 1%），等于给持仓加了一层道德光环：亏不是判断错了，是你<b>不够格</b>。⚠️ 分析：① 「pay-tience」是他自造的谐音（pay＝付出代价），把<b>等待的成本</b>明说了，是近十天里少见的诚实；② 全文<b>零数据、零价位</b>，纯心理建设，这类发言通常出现在持仓承压、需要社群一起撑的阶段；③ 与同一天中午的 <b>76.8–80.8K 网格</b>直接矛盾——网格是<b>在区间里持续高抛低吸</b>，「holding through this crap」是<b>一动不动</b>，两种做法不可能同时是他给的建议。失效条件：① 若他自己在 80K 下方用网格减过仓，「holding」当场自我否定；② 若区间最终<b>向下</b>解决，这「1%」就是被套的那批人，本条从鼓励变成安慰剂；③ 无任何可验收指标，按他自己的标准属<b>不可执行发言</b>。",
      tags: ["情绪指标", "仓位建议"],
      src: "X 原文 @KillaXBT · 2112565774615466408"
    },
    {
      date: "2026-10-20",
      title: "「谁都别说话」：一天第五条，情绪贴里的纯留白",
      quote: "\"Nobody say a word.\"（<b>谁都别说话。</b>）——抓取未取到配图，按不猜测原则不补充图像内容，仅记文字。",
      read: "改动的是<b>发帖节奏</b>而不是判断——这是 10-20 当天第 <b>5</b> 条（前四条依次是网格区间、USDC 增发、扫针看多、99%/1%），本条没有任何论点、价位或数据，属典型的<b>晒图后留白</b>（配图未抓到）。⚠️ 分析：① 单看文字<b>零信息量</b>，不作为任何判断依据；② 高频连续发帖本身就是信号——他 10-15 至 10-17 的安静期与 10-18 起的密集输出形成对照，密集期通常对应<b>仓位压力最大</b>的阶段；③ 不要从「谁都别说话」反推他看多或看空，那是评论区互动话术。失效条件：不适用——本条不含任何可验证主张，只作发帖节奏记录。",
      tags: ["情绪指标", "存疑"],
      src: "X 原文 @KillaXBT · 2112548599154233690"
    },
    {
      date: "2026-10-20",
      title: "「在 76.8–80.8K 挂网格」：首次把「最坏情形」改成可交易区间",
      quote: "\"You want to outperform during environments like this? Set a grid bot on $BTC between 76.8-80.8K. Thank me later\"（想在<b>这种行情</b>里跑赢？在 BTC 的 <b>76.8–80.8K</b> 之间<b>挂一个网格机器人</b>。<b>回头谢我。</b>）——本条无配图，纯文字。",
      read: "改动的是他对 <b>76–78K 的定性</b>——10-18 他明说「对多头来说<b>绝对最坏的情形</b>是偏离到 76–78 区域」，那是个要避免的分支；本条把 <b>76.8–80.8K</b> 划成一个<b>要主动进去收租</b>的区间，等于承认价格会走进他自己定义的「最坏情形」，而且要在那里<b>机械低买高卖</b>。⚠️ 分析：① 这是收录以来他给的<b>第一个低于现价的机械交易区间</b>（此前区间都在 80–84K），下沿 76.8K 已逼近他「不认为会扫 74K」的容忍边界，缓冲只剩 <b>2.8K</b>；② 网格与他 10-18「<b>126K 之前一分钱不平</b>」在机制上冲突——网格每一次上轨卖出<b>都是在平仓</b>，两套说法不能同时成立；③ 他没给资金占比、格数、止损，属<b>口号式策略</b>，照搬会在他自己划的失效下沿无限接盘；④ 时点值得注意：这条发于 10-20 中午，<b>早于「99% 被洗」「拐点就在这几天」</b>，是他当天最落地的一条。失效条件：① 价格直接<b>收复 83.6K</b> 且不再回 80.8K，网格只吃到上半段，机会成本极高；② 若<b>跌破 76.8K</b>（网格下沿），网格从收租变成<b>被套接盘</b>，离他「never sub 70K」只剩 6.8K；③ 若他自己不实盘跑这个网格（「Thank me later」是零成本喊话），本条按话术处理。",
      tags: ["仓位建议", "关键价位", "失效条件"],
      src: "X 原文 @KillaXBT · 2112526662923690379"
    },
    {
      date: "2026-10-20",
      title: "「本月 USDC 增发 52 亿」：首次用稳定币供给给看多找资金面依据",
      quote: "\"USDC Treasury has minted 5.2B $USDC this month. If you know, you know… OG stuff.\"（USDC 发行方本月已经<b>增发 52 亿 USDC</b>。懂的自然懂……<b>老玩家的东西</b>。）——本条无配图，纯文字。",
      read: "改动的是他<b>看多论据的来源</b>——此前十天他的多头理由全部是价格结构（周线 100/200 EMA 翻转、扫针、-54% 回撤深度、清算位置），本条第一次把<b>稳定币增发量</b>当论据，等于给上行补了一条资金面支线。⚠️ 分析：① 「Treasury minted」只统计<b>铸造动作</b>，包含跨链换手与赎回后重铸，不等于净新增买盘，他没给总市值变化做交叉；② 「OG stuff」暗示他把这当成前几轮牛市启动前的老信号，但他既没给历史对照数据，也没说这 52 亿相对月均是多还是少；③ 与他 10-18 的「利空全是燃料」框架互补——那边解释「为什么不跌」，这边解释「钱从哪来」，两条合起来是一套完整的不可证伪叙事。失效条件：① 若随后两周 USDC 总市值没有等幅增长（说明是换手不是增量），这条论据自动作废；② 若流动性改善而 BTC 仍在 82K 下方横盘、ETF 现货延续净流出，资金面逻辑被价格否定；③ 52 亿这个数字无来源引用，口径不可核，只能当他自述。",
      tags: ["宏观驱动", "链上数据", "存疑"],
      src: "X 原文 @KillaXBT · 2112343952053739529"
    },
    {
      date: "2026-10-20",
      title: "「LTC 总有一天干一票大的，而且没人有仓」——首次点名赌单币脉冲",
      quote: "\"I'm not sure when or how, But I've got a gut feeling that @litecoin pulls off something like this one day, and absolutely nobody will be positioned for it.\"（我不确定<b>什么时候</b>、也<b>不知道会怎么发生</b>，但我有个直觉——@litecoin 总有一天会干出这种事，而且<b>绝对没有人会提前布好仓</b>。）——配图为 LTC 长周期 K 线：左侧自约 240–300 的高位一路走低，中段数次反弹后继续下移，近段长期在 <b>40–100</b> 区间横盘；图右侧是他手绘的一条白色直线，从低位近乎垂直拉升至约 <b>240</b>。",
      read: "改动的是他谈山寨的<b>方式</b>——10-17 他给的是一份带买区的清单（SOL 97–103 / LTC 56–59 / ASTER 0.66–0.7 / BNB 722–680），每条都有价位可执行；本条第一次出现<b>无买区、纯直觉、「总有一天」</b>的标的，等于把 LTC 从「按区间埋伏」改成「赌一次性脉冲」。⚠️ 分析：① 他自己写了不确定时间、不确定方式，是近期唯一<b>主动放弃时间与路径</b>的判断，按他自己的验收标准这条无法被证伪；② 手绘拉升线画到约 240，相对现价约 3–4 倍，但图上没有任何结构、量能或催化剂支撑，纯示意；③ 与 10-17「BTC 到 126K 山寨涨 50–75%」口径冲突——本条隐含 LTC 涨 300%+，远超他给的山寨弹性区间，两套说法不能同时当基准。失效条件：① LTC 跌破他 10-17 自己划的 <b>56–59</b> 买区，「长期横盘蓄势」叙事作废；② 若 12 周内他不再提 LTC，本条按一次性情绪贴处理；③ 他把「没人有仓」当利好前提，但无人持仓同时意味着<b>没有承接盘</b>，若真出现垂直拉升也可能是无法出货的孤岛行情。",
      tags: ["山寨", "目标价", "存疑"],
      src: "X 原文 @KillaXBT · 2112325775894384768"
    },
    {
      date: "2026-10-20",
      title: "空头 delta 持续堆积而 BTC 波动压缩，他把卖压读成逼空燃料",
      quote: "\"The short delta continues to pile as $BTC compresses.\"（在 BTC <b>波动持续压缩</b>的同时，<b>空头 delta 还在不断堆积</b>。）——配图为 Delta 类指标柱状图：横轴价格约 82,000–89,000，纵轴为 delta 成交量；左侧早期以蓝绿柱为主，右侧最新一段在 <b>82,000 附近出现两根极高的红色柱</b>，当前价以竖虚线标在约 <b>82,000</b>；上方价格线整体自左上向右下走低。",
      read: "改动的是他证明「空头拥挤」的<b>取数口径</b>——10-18 他用的是账户多空比（自称 62% 净空，但那张配图写的是 42.77%，数字对不上），本条第一次改用<b>主动成交 delta</b>（卖方主动成交持续占优）作为证据，是同一结论换了更硬的数据源。⚠️ 分析：① 这里有一个关键跳跃——delta 持续为负只证明<b>卖压持续存在</b>，并不等于「空头仓位堆满、随时被挤」，他把「卖压」直接等同于「待挤空头」；② 图上的红柱正好集中在 <b>82,000</b>、也就是他成本区附近，这既可能真是空头在堆，也可能是<b>有人在往他怀里派发</b>，单看 delta 无法区分；③ 与 10-19「底部已数月、-54% 即底」并列，他必须在「底部已成」和「卖压持续堆积」之间架桥，那座桥就是「卖压＝待挤空头」这个未经验证的假设。失效条件：① 价格在 82,000 下方继续放量下行且红柱不减——堆积就不叫「待挤」，而是趋势性派发；② <b>83.6K 被收复后 delta 仍为负</b>，说明卖压不是被挤掉而是继续新增，他的挤空剧本缺少价格确认；③ 若波动压缩以<b>向下</b>的方式解决（跌破 79,813 并扩张），压缩本身就成了看空信号。",
      tags: ["情绪指标", "关键价位", "仓位建议"],
      src: "X 原文 @KillaXBT · 2112258555063497080"
    },
    {
      date: "2026-10-20",
      title: "「时间型投降」：把 62K–66K 的折磨形态套到当前区间，时间改成不定期的 due time",
      quote: "\"This is the kind of PA you orchestrate when you want to make sure nobody catches the next move. Timebased capitulation. Multiple messy hunts. Internal structure breaking and reclaiming like it's nothing. Add a little FUD to the mix and you've got the perfect environment for people to capitulate, short the lows, and miss the move when it finally comes. Uncomfortable lows. Uncomfortable news. Uncomfortable positioning. That's usually where the most profitable trades are. You get comfortable shorting every high and low, then one candle wipes out weeks of gains. $BTC did the same between 62K and 66K for weeks... And it will happen again. In due time.\"（这就是那种<b>刻意做出来</b>的价格行为——目的就是确保没人抓到下一段行情。<b>时间型投降</b>、反复的<b>混乱扫针</b>、内部结构破了又像没事一样收回来。再掺一点 FUD，你就得到了最完美的环境：让人<b>投降、在低点做空、然后在行情真正启动时错过它</b>。不舒服的低点、不舒服的消息、不舒服的持仓——那通常正是<b>最赚钱的交易所在</b>。等你习惯了在每一个高点和低点做空，<b>一根 K 线就能抹掉几周的利润</b>。BTC 在 <b>62K 到 66K 之间</b>就这么磨了好几周……<b>它还会再来一次，只是时间问题（in due time）</b>。）——配图为 BTC 走势图（无坐标标注）：一段高位震荡后逐级下移，中段多次<b>插针后立即拉回</b>，右端在低位反复拉锯，整体呈下降通道内的反复扫针形态。",
      read: "改动的是他对当前区间的<b>定义与时间预期</b>——10-18 周线复盘他用的是「区间式投降（range-based capitulation）」，并说「下周很可能开始吃另一侧」，把转机押在<b>一周内</b>；本条把同一个词升级为「<b>时间型</b>投降」，且明确写 in due time，等于<b>把上一轮自己给的时间表往后推</b>。⚠️ 分析：① 62K–66K 那次磨完确实向上突破，但当时周线结构完整、没有 87 段被拒 + 连续两周更低的高点，形态并不等价，类比属于选择性取样；② 「一根 K 线抹掉几周利润」是他近期第一次承认<b>双向都能杀人</b>，比 10-18「趋势是你的朋友」温和许多，语气明显从进攻转向忍耐；③ 整段把「不舒服」当成看多理由，逻辑上仍是不可证伪的元叙事——涨了是「你被洗掉了」，跌了是「时间型投降还没结束」。失效条件：① 区间<b>向下</b>扩张（周线收破 79,813 后连续新低），压缩以向下解决，「磨完向上」整个类比反转；② 若 3–4 周内仍未离开 80–84K，他的「due time」就等于无限期拖延，与 10-17「Q3 即新 Q1、Q4 要 pump」的时间表冲突；③ 一旦他自己在这个区间减仓，「不舒服就是最赚钱的地方」当场自我否定。",
      tags: ["周期判断", "基准剧本", "关键价位"],
      src: "X 原文 @KillaXBT · 2112216886263890295"
    },
    {
      date: "2026-10-19",
      title: "首次公开教「周一扫针后做空吃 1–3%」，与他自己的禁空令直接冲突",
      quote: "\"Monday doing the same old algo. Retracing almost every pump to the upside. Funny how I've been pointing this out since August 2025 and they still haven't changed the algo. You could've looked to short $BTC on Monday after the sweeps and caught multiple 1-3% drops.\"（<b>周一</b>又在跑那套老算法：<b>几乎每一次拉升都被回吐</b>。有意思的是我从 <b>2025 年 8 月</b>就一直在指出这一点，他们还是没改算法。<b>你本可以在周一扫针之后找机会做空 BTC，吃到好几段 1–3% 的下跌。</b>）——配图为 BTC K 线图，用<b>六个红色圆点</b>标出每个周一所在位置，每个点旁标注 Monday，全部落在<b>局部高点或冲高回落处</b>；纵轴约 79,000–87,000，最右一个红点在约 82,000 附近。",
      read: "改动的是他的<b>立场一致性</b>——10-19 凌晨他才说「趋势是你的朋友」，10-14 更明说「不该在 ATH 下方做任何空」，本条却公开给出<b>周一扫针后做空</b>的具体打法，这是他第一次在公开贴里教做空。⚠️ 分析：① 双轨表述本身可以自洽（大周期多、日内空），但他此前用的是「不该做空」的绝对措辞，不是「可以做但要小」，口径确实变了；② 配图六个 Monday 红点全部标在<b>已发生的局部顶</b>，是事后标注，没有给出事前如何识别扫针完成——按他自己的标准，这属于「看图说话」而非可执行信号；③ 「since August 2025」是他首次交代这个规律的观察跨度（约 14 个月），但没给胜率、样本数、平均回撤，与他平时强调的「数据说话」不符。失效条件：① 出现一个周一<b>单边上行不回头</b>（扫针后不再回落），规律当周即破；② 与他 10-18「多头侧已被猎、下周轮到空头」的轮动判断冲突——若真开始挤空，周一做空就是逆着自己的主剧本；③ 若他自己在周一做空后被扫，这条立刻从「规律」降级为嘴上技巧。",
      tags: ["仓位建议", "周期判断", "存疑"],
      src: "X 原文 @KillaXBT · 2112180385279000829"
    },
    {
      date: "2026-10-19",
      title: "「底部已数月」：首次用 -54% 回撤幅度论证周期不同",
      quote: "\"$BTC bottom has been in for months. Market bottomed at -54%. Not -75%+. Good luck thinking we are going to do the same bull market retracements as previous cycles. But what do I know. Just a random guy who happened to short 123K and long 62K\"（BTC 的<b>底部已经在了、而且已经好几个月</b>。市场在 <b>-54%</b> 就见底了，不是 -75% 以上。祝你好运——如果你还指望我们重复前几个周期的牛市回撤幅度。不过我又懂什么呢？我只是个碰巧<b>在 123K 做空、62K 做多</b>的普通人。）——本条转推他自己更早的「三次主要低点」长帖，引文为 \"In every major $BTC bear market, we've seen 3 significant lows. The third major low this cycle was the $57K low.\"（每轮 BTC 大熊市我们都见到三个显著低点，本轮第三个主要低点是 <b>57K</b>）。配图为该长帖用的四宫格对照图——四段历史走势各自标出三个低点、最后一个标注为 capitulation low（投降低点），当前周期一段同样标出三点。",
      read: "改动的是他<b>定义底部的方式</b>——此前他靠失效价框住下行（74,550 的 10 倍仓、never sub 70K），本条第一次改用<b>回撤幅度百分比</b>论证：本轮只跌 54%，所以不会重复历史周期 75%+ 的深度。⚠️ 分析：① -54% 隐含他把 <b>126K</b> 当作本轮顶部（126K×0.46≈58K，与 57K 第三低点吻合），也就是说「-75%」对应的<b>约 31.5K</b> 被他彻底排除，比「never sub 70K」更激进；② 这是他「周期不同论」的第三次升级：10-17 用季节性（Q3=新Q4）、10-18 用绝对化措辞（never sub 70K），本条换成<b>可量化的深度差</b>，是三次里唯一有数字支撑的；③ 「short 123K / long 62K」是他首次在同一句里给出双向完整战绩，但<b>无截图、无交易所凭据</b>，属自述口径，不可核实。失效条件：① 周线收盘跌回 <b>57K 下方</b>（回撤 >55%）——「-54% 即本轮底」作废，同时「三次低点已完成」的形态被打散、需要第四次低点；② 若 8 周内未创出高于 87–88K 的段高，「底部已数月」从「已成底」退化为长期区间；③ 他也可能用「-54%」偷换口径（从 126K 起算还是从最高收盘起算未说明），口径一变结论就变。",
      tags: ["周期判断", "目标价", "战绩复盘"],
      src: "X 原文 @KillaXBT · 2111944574839001275"
    },
    {
      date: "2026-10-19",
      title: "把空头比作「下一个 Michael Burry」，收尾一句「趋势是你的朋友」",
      quote: "\"Mfs really trying to be the next Michael burry. Humble yourself. The trend is your friend.\"（这些人真的在努力当<b>下一个 Michael Burry</b>。谦虚点吧。<b>趋势是你的朋友</b>。）",
      read: "改动的是他对空头的<b>表述层级</b>——10-18 凌晨他还在用「62% 净空」这种数据口径论证逼空，本条只剩姿态与嘲讽，没有给任何价位、任何数据，是连续五天里第一条<b>纯情绪贴</b>。⚠️ 分析：① 作用是社群认同与心理加固，这类发言通常出现在持仓承压、需要外部确认的时候；② 「趋势是你的朋友」的前提是趋势已翻转为上行，而这恰是他与空头的核心分歧（他用周线 100/200 EMA 翻转论证，空头用 87 段被拒论证），本条<b>完全没有回应这个分歧</b>；③ 把对手盘比作 Burry，等于把「看空」框定为偏执，属修辞先手，不构成论据。失效条件：① 若 BTC 周线收盘跌破 <b>79,813</b>（本周低）并继续下探 76–78，「趋势」在本级别上并非上行，这句话直接反噬；② 他趋势论证的真正根是<b>周线 100/200 EMA 翻转</b>，若周线重新收在该均线带下方，趋势论点从根上失效。",
      tags: ["情绪指标", "趋势切换"],
      src: "X 原文 @KillaXBT · 2111856501031583983"
    },
    {
      date: "2026-10-18",
      title: "周线复盘：多头侧已被猎，83.6K 定为区间投降的判定开关",
      quote: "\"There's always a story to tell when looking at weekly candles. Last week, $BTC had a rejection from the 87s down to the 80s. After recovering 50% of the dump, the next weekly candle opened, our current one... that weekly candle started the week pushing up on Monday, constantly rejecting the weekly open, and ultimately leading to a sweep of the previous weekly low at 80K. So far, the side that's been hunted has been the long side. That means there's a good chance we start taking the other side next week, though I'd keep an eye out in case we get another sweep of this week's low at 79.8K. If we do, look for longs. If we don't, then 83.6K is the area to observe yet again. If we can't flip that area, we remain in range-based capitulation. If we can... well then up lol. So, in short, we hunted the PWL. Maintain above it or see any sweeps, look for longs. Watch for the next weekly candle to start pushing upwards and take out some late shorts who chased this move down. Absolute worst case scenario for bulls would be deviating to the 76-78 region. I do not see a sweep of 74K happening.\"（上周 BTC 从 87 段被拒、跌到 80 段；收复这波跌幅的 50% 之后，本周这根周线开盘了……它周一先冲高、但持续被周开压制，最终扫掉上周低点 80K。<b>到目前为止被猎杀的是多头一侧</b>，这意味着<b>下周我们很可能开始吃另一侧</b>，不过我会盯着本周低点 <b>79.8K</b> 会不会再被扫一次。如果被扫，就找做多机会；如果没有，那 <b>83.6K</b> 又是要观察的区域——<b>翻不上去，我们就还在区间式投降里</b>；翻上去了……那就涨呗。总之我们扫了 PWL（上周低点）：守住它上方、或者看到任何扫针，都找多。注意下一根周线是否开始向上发力、把追这波下跌的<b>晚到空头</b>打掉。对多头来说<b>绝对最坏的情形</b>是偏离到 <b>76–78</b> 区域。我<b>不认为会看到扫 74K</b> 这件事发生。）——配图为他自制的周线图，标注 <b>WEEKLY OPEN 83,774.2</b>、<b>PWL HUNTED 80,413.6</b>、<b>CURRENT WEEKLY LOW 79,813.4</b>，另有一条 77,703.0 横线；图中现价标记约 <b>82,065</b>。",
      read: "这一条同时改了他三条既有判断：① 10-17 的「最坏 76–78」从<b>假设分支</b>升格为「绝对最坏情形」，并第一次明说「<b>不认为会扫 74K</b>」——等于把他自己 74,550 的失效线往前收了一格；② <b>83.6K 从「观察区」升级为二值判定开关</b>：翻上＝上行、翻不上＝继续「区间式投降」，这是他第一次给自己的看多加上可验收的条件；③ 新增「<b>多头侧已被猎 → 下周轮到另一侧</b>」的对称轮动判断，是 10-18「62% 净空」那条的机制化版本（下一步是挤空）。⚠️ 分析：① 他把 80,413.6 标为「PWL HUNTED」，但本周实际低点是 <b>79,813.4</b> 更低——「守住 PWL 上方」已被他自己的数据打破，他真正依赖的是本周低 79,813，只是嘴上仍说 PWL；② 83.6K 与周开 83,774.2 只差约 170 美元，把判断押在这么窄的带上，容错极低；③ 「不认为扫 74K」与「绝对最坏 76–78」之间留了 2K 无剧本空白，这段若被击穿他无预案。失效条件：① <b>79,813 被周线收破且不收回</b>，「守住/扫针找多」整条作废；② 74K 真被扫，「不认为扫 74K」直接打脸，同时 74,550 的 10 倍仓失效、按其规则还要开第二个 10 倍；③ 83.6K 连续两周上不去，「区间式投降」升为主剧本，他的看多从「即将突破」降级为「继续磨」。",
      tags: ["关键价位", "基准剧本", "失效条件"],
      src: "X 原文 @KillaXBT · 2111834694018834435"
    },
    {
      date: "2026-10-18",
      title: "重发「一切已计价」图：把利空清单升级成跨周期框架",
      quote: "\"I think this is worth reposting for people to study. Bad news during a bull market = fuels continuation. We've seen wave after wave of 'bad' news and events, and it lines up with what we've seen in every cycle $BTC before.\"（我认为这张图值得重发让大家研究。<b>牛市里的坏消息＝续涨的燃料</b>。我们已经看到一波接一波的「坏」消息和事件，而<b>这与 BTC 之前每个周期里发生的事完全对得上</b>。）——转推的是他自己此前那条 「The 'Everything Is Priced In' chart」长帖，引文说这张图记录了各周期的重大催化剂与消息事件、以及它们之后通常发生什么；配图即该图表。",
      read: "改动的是<b>论据的性质</b>——10-16 他给的是一份一次性利空清单（油涨 / MSTR 退市担忧 / CPI 走热 / 加息 / 债券收益率飙升 / 美元新高 / Ledger 被盗），本条把它收束成一张<b>跨周期可复用的历史图表</b>，等于宣称「利空不改方向」是统计规律、不是他的个人判断。⚠️ 分析：① 这是本轮唯一带方法论野心的动作，但图是<b>他自制</b>的——选哪些事件、怎么对齐「之后发生什么」全由他定，<b>选择偏差</b>无法排除；② 该框架的致命处是<b>不区分噪音级与结构性利空</b>：MSTR 真被摘牌、ETF 连续大额净流出这类会改变资金结构的事件，在这套框架里和「Ledger 被盗」同级；③ 它与 10-18「62% 净空」、10-19「趋势是你的朋友」拼成完整闭环——利空多 → 大家看空 → 空头拥挤 → 逼空，四步全部不可证伪。失效条件：① 出现<b>结构性利空且被价格确认</b>（ETF 连续两周净流出、MSTR 实际摘牌、美联储真加息）后 BTC 仍下跌，「利空是燃料」被证伪；② 若他自己在下跌中减仓，等于亲手否定这套框架。",
      tags: ["宏观驱动", "基准剧本", "存疑"],
      src: "X 原文 @KillaXBT · 2111804741605060626"
    },
    {
      date: "2026-10-18",
      title: "「讲不通才涨」＋首次承诺 126K 前不平仓、清算价为 0",
      quote: "\"It doesn't go up because it makes sense. It goes up because it doesn't make sense. If the market always made sense and every move could be justified by logic, everyone would make money. That's simply not how the $BTC works. Still long. Will close nothing until 126K. Liquidation is 0.\"（它上涨不是因为讲得通，而是因为<b>讲不通</b>。如果市场永远讲得通、每一步都能用逻辑解释，那所有人都会赚钱。BTC 根本不是这样运作的。<b>我仍然做多。126K 之前一分钱都不平。清算价是 0。</b>）——本条转推他 10-18 凌晨那条「never sub 70K / 从现价涨 75%」的推文。",
      read: "改动的是<b>持仓承诺的口径</b>——10-14 他对那笔成本 2.08–2.33 万的长线仓说的是「<b>到 15 万美元前不平</b>」，本条换成「<b>126K 之前不平</b>」，两个平仓目标位不一致：要么是不同仓位、要么他把目标下调了，他没有说明是哪一种。同时首次给出<b>清算价为 0</b>——这才是他敢喊「never sub 70K」、敢在 80K 下方继续接多的结构性原因：<b>他可以零成本扛任何回撤</b>。⚠️ 分析：① 「清算价 0」意味着无杠杆或极低杠杆，与他 10-13 那笔 <b>82,860 的 10 倍仓</b>不是同一笔，两条承诺不能互相担保；② 「讲不通才涨」是对「利空这么多为什么还涨」的事后解释，属<b>不可证伪的元叙事</b>，与他 10-17「坏消息全是噪音」是同一件事的两种说法；③ 126K 是他自 9 月起的固定目标位，本条把「不平仓」的时点锚在它上面，等于把 126K 变成可验收的<b>持仓终点</b>。失效条件：① 他在 126K 之前平掉任何一笔，该承诺作废（最容易验证的一条）；② 126K 在 2026 年内未触及，「126K 前不平」就从承诺变成长期扛单，机会成本由他自己承担；③ 若他后续改口说「126K 是减仓不是清仓」，承诺同样作废。",
      tags: ["仓位建议", "目标价", "关键价位"],
      src: "X 原文 @KillaXBT · 2111778314444587186"
    },
    {
      date: "2026-10-18",
      title: "「永不再破 70K」：首次用绝对化措辞，并放话从现价涨 75%",
      quote: "\"We are never going sub 70K again. We are going to pump 75% from current prices. Yet -9% on $BTC is simply not satisifying enough. Imagine. You are literally willing to miss a 100% move, for the possibility of 5-10% lower? Do you know how retarded that is?\"（我们<b>再也不会</b>跌到 70K 下方。我们要从现价<b>涨 75%</b>。可 BTC 只跌了 9% 你就已经受不了了。想想看——你宁愿<b>错过 100% 的行情</b>，只为赌还能再低 5–10%？你知道这有多蠢吗？）",
      read: "改动的是他的<b>下行底线与上行幅度</b>——此前他对下行的约束是「74K 上方形成更高低点」（10-17）、10 倍仓失效价 74,550，本条第一次用 <b>never</b> 把 70K 说成不可再破的绝对底，同时把上行从「126K 目标」换成<b>相对现价的百分比</b>：涨 75%（按 10-18 现价约 81.7K 折算约 <b>143K</b>，比 126K 高约 13%）。⚠️ 分析：① 这是他迄今最强的单边表述，也是第一次出现绝对化措辞，可证伪性极高；② 「错过 100% 的行情」隐含他看到约 <b>163K</b>，恰与他 10-11「2029 年 160–180K」的顶部区间接上；③ 本条是 10-17「Q4 是新的 Q1」那套周期提前论的情绪版，<b>没有新增任何技术论据</b>，属喊话而非分析。失效条件：① 日线<b>收破 70K</b>，「never sub 70K」直接作废（届时 74,550 的 10 倍仓早已被扫、且按他自己的规则要再开第二个 10 倍）；② 若 4–6 周内未启动上行、或 126K 之前的关键位 87–88K 反复失败，「涨 75%」的时点预期落空。",
      tags: ["目标价", "关键价位", "失效条件"],
      src: "X 原文 @KillaXBT · 2111625255727087848"
    },
    {
      date: "2026-10-18",
      title: "一句「非常看多扫针」，用上一区间并排对照当前结构",
      quote: "\"Very bullish on sweeps... $BTC\"（对<b>扫针（sweeps）非常看多</b>……）（配图为左右并排的两幅走势对照：左幅为上一区间、右幅为当前结构，两图内部均以黑点标注连续被扫的低点，右幅另有一条横线标出现价所在区间；图上价位刻度过于模糊，无法辨认具体数值，按不猜测原则不转述。）",
      read: "改动的是他<b>「逢扫低点做多」这条规则的可视化举证</b>——10-16 他只用文字把「牛市要接被扫的低点」写成规则，本条第一次把<b>上一区间与当前结构并排</b>摆出来，指两者都在低位反复被扫后向上扩张。⚠️ 分析：① 论证方式是<b>类比而非新数据</b>，右幅当前结构能否复制左幅，图本身不提供证据；② 与 10-16「76K 接过多单」、10-17「扫针规则」构成同一条规则的第三次重复，属<b>规则固化</b>而非新判断；③ 关键风险在于这条规则没有任何对冲分支——扫针向下失败时它会连续给出买入信号。失效条件：① 当前区间低点（80,819 / 79,800）被<b>日线收破且不收回</b>，「扫针即扩张」的类比失效；② 若他自己在下次扫低后减仓，规则自我否定。",
      tags: ["基准剧本", "关键价位", "存疑"],
      src: "X 原文 @KillaXBT · 2111575894884008050"
    },
    {
      date: "2026-10-18",
      title: "首次给多空持仓比：62% 净空，「坏消息这么多还能怎样」",
      quote: "\"More people are short than long... $BTC 38% of people are net long. 62% of people are net short. With all this bad news, what could possibly go wrong?\"（做空的人比做多的人多……<b>38% 的人净多、62% 的人净空</b>。这么多坏消息摆在面前，还能出什么岔子？）（配图为第三方持仓追踪面板截图：774 个钱包、总仓位 48.7 亿美元，多头 18.6 亿、空头 26.1 亿，多头钱包占比显示 <b>42.77%</b>——与他正文的 38%/62% <b>并不完全对齐</b>，数据来源与统计口径均未标注。）",
      read: "改动的是他的<b>论据类型</b>——此前看多的支撑是技术面（周线均线翻转）、订单簿（买墙被吸）、情绪（贪婪可维持数月）、宏观（利空是噪音），本条第一次引入<b>仓位拥挤度</b>。「多数人在做空」被当作反向指标。⚠️ 分析：① 这是典型的<b>逼空燃料</b>逻辑，与 10-12/10-13「86–88K 上方有 5B+ 空头清算池」同向叠加，但两组数据来自不同来源、他自己没有对齐；② 配图是 42.77% 多头钱包、18.6 亿 vs 26.1 亿美元，正文却写 38%/62%，<b>偏差不小且未解释</b>，说明数字可能取自不同快照或口径，可信度应打折；③ 与 10-17「坏消息全是噪音」拼成「越多人看空越该做多」的闭环，同样不可证伪。失效条件：① 若价格<b>日线收破 80K</b> 而空头并未回补、净空比例继续上升，「空头拥挤＝利多」被证伪（说明空头是对的）；② 若他日后改用另一套持仓数据得出相反结论，以最新口径为准。",
      tags: ["情绪指标", "基准剧本", "存疑"],
      src: "X 原文 @KillaXBT · 2111540187742261497"
    },
    {
      date: "2026-10-18",
      title: "罕见谈 ETH：BTC 在 90K 段时，ETH 应进 3,000 美元区",
      quote: "\"I rarely speak about $ETH, But if BTC can hold its range structure, I'd expect ETH to make a move into the 3,000s while BTC is trading in the 90Ks. May take time to develop, and we could see a few more hunts along the way, but overall, ETH is looking okay-ish\"（我很少谈 ETH。但如果 BTC 能<b>守住区间结构</b>，我预期 <b>BTC 在 90K 段交易的时候，ETH 会走到 3,000 美元区间</b>。可能需要时间发酵，途中还会有几次<b>猎杀</b>，但总体 ETH 看起来还算可以。）",
      read: "改动的是他的<b>覆盖面</b>——这是本 feed 收录以来他第一次给 <b>$ETH 的价位映射</b>（此前只谈 BTC，10-07 提过一次 LTC）。⚠️ 分析：① 真正的信息不在 ETH，而在<b>把 BTC 的 90K 段当成了会发生的事</b>——比 10-12「86–88K 空头池」、10-14「往 87–88K 上方猎」又推高一档，90K 从「可能」变成「前提」；② 「ETH 进 3,000 段」既没给起止价、也没给 ETH 现价基准，属<b>弱可验收</b>表述；③ 「途中还会有几次猎杀」是标准免责垫，把路径上的下跌预先解释掉。失效条件：① BTC <b>守不住区间结构</b>（以他 10-17「74K 上方更高低点」或 80K 日线为准），本条前提消失、自动作废；② 若 BTC 真进入 90K 段而 ETH 明显落后（未进 3,000），相对强弱判断失效。",
      tags: ["山寨", "目标价", "关键价位"],
      src: "X 原文 @KillaXBT · 2111528216728928370"
    },
    {
      date: "2026-10-17",
      title: "周末反而看涨：把「周一反转」改成双向条件",
      quote: "\"$BTC has pumped over the last 3 weekends, only to reverse on Monday. When we see more downside pressure over the weekend, though, we often get the inverse move. So if we pump into the weekly close, Monday is worth watching closely. If we start dumping over the weekend… well, the last time that happened, BTC legged up.\"（BTC 最近<b>三个周末都在拉</b>，然后周一反转。但如果周末<b>承压下跌</b>，我们常常看到反向走势。所以如果拉到周线收盘，周一要盯紧；如果周末开始跌……上次那样的时候，BTC 直接向上抬了一段。）（配图为日线图，用 1 个红框 + 3 个绿框圈出各周末前后的价格窗口，框内均为先下探再上抬的结构；图上刻度无法辨认，不转述价位。）",
      read: "改动的是他对<b>周末效应的用法</b>——10-05 他把周末拉升当作利多确认（「神烛」），本条把拉升<b>降级为反向信号</b>（拉高→周一反转），同时把「周末下跌」升级为看涨条件。⚠️ 分析：① 这是标准的<b>双向条件式</b>：涨了要提防周一、跌了反而看多，两种结果都能落回他的多头叙事，可证伪性很低；② 内部张力在于——同日 20:22 他刚用「季节性整体移位、Q4 是新的 Q1」这种年级别框架，本条又退回到样本仅 3 次的周末规律；③ 实盘对照：10-18（周六）BTC 开 82,078、最低 81,403、现约 81,7K（Binance），属<b>小幅走弱而非明显抛售</b>，正落在他「跌了则反向」的模糊地带，暂不给答案。失效条件：① 若本周末<b>拉到周线收盘</b>且周一继续上涨，「拉高→周一反转」的前提被打破；② 若周末明显下跌而周一继续跌，「下跌→反向抬升」失效。",
      tags: ["周期判断", "基准剧本", "失效条件"],
      src: "X 原文 @KillaXBT · 2111472936771031476"
    },
    {
      date: "2026-10-17",
      title: "「600 天摆动规律」：看空叙事越堆，下一段越可能向上",
      quote: "\"This is what happens when you spend 1/3rd of your life staring at charts. You start spotting patterns most never see. Just look at the PA. For more than a year, $BTC has kept repeating the same swing-high, swing-low pattern. If we continue building a clear bearish narrative next week, the next phase will likely result in higher. It's only based on 600 days of price action, right. Would you bet against a pattern that's been this consistent?\"（这就是把 1/3 的人生盯着图表的结果……看价格行为。<b>一年多以来，BTC 一直在重复同一个摆动高点—摆动低点的形态</b>。如果下周我们继续堆积清晰的<b>看空叙事</b>，下一阶段很可能会<b>向上</b>。毕竟这只是基于 600 天的价格行为嘛。这么一致的形态，你敢赌它不成立？）（本条引用的是他自己 10-16「市场按 mini-cycle 走」那条。配图为日线图，黑点标注各摆动高低点，最右侧一个孤立黑点悬在现价上方——即他画出的下一个预期摆动高点；纵轴刻度无法辨认，不转述具体价位。）",
      read: "改动的是 <b>10-11「14 号日历枢轴」模型</b>——从「某个具体日期会反向」，扩展成「<b>看空叙事堆积＝下一段向上</b>」的可循环规则，并首次给这套模型标注样本依据「600 天价格行为」。⚠️ 分析：① 这是他第一次为枢轴模型说样本量（600 天 ≈ 一年多），但 600 天里有多少次<b>可比的摆动—反向样本</b>，他没给；② 规则的单边化很明显：10-08 他讲枢轴时是双向的（看空叙事→涨、看多情绪→跌），本条只剩「看空→涨」这半边；③ 配图最右侧那个孤立黑点是他亲手画的<b>预期下一个高点</b>，位置明显高于现价，但刻度不可读，<b>不能当点位用</b>。失效条件：① 若下周继续堆积看空叙事而价格<b>创出更低的摆动低点</b>（跌破 80,819 / 79,800 且不收回），「叙事越空越涨」失效；② 若 600 天的摆动结构被一根趋势性下跌打破，整套类比作废。",
      tags: ["周期判断", "基准剧本", "存疑"],
      src: "X 原文 @KillaXBT · 2111435762063274281"
    },
    {
      date: "2026-10-17",
      title: "「Q3 是新的 Q4、Q4 是新的 Q1」：季节钟整体提前一季",
      quote: "\"$BTC usually bottoms in Q4. This time, it bottomed in Q3. Q3 is the new Q4, and Q4 is the new Q1. What usually happens after BTC usually bottoms in Q4? It pumps in Q1. As I said, young ones: Q4 is the new Q1 this cycle as seasonality has shifted.\"（BTC 通常<b>在 Q4 见底</b>。这次它在 <b>Q3 就见底了</b>。<b>Q3 是新的 Q4，Q4 是新的 Q1</b>。BTC 在 Q4 见底之后通常会怎样？<b>Q1 拉升</b>。我说过了，小鬼们：这个周期里 <b>Q4 就是新的 Q1</b>，季节性已经移位。）（本条引用的是他自己 10-17 早上那条「Q4 pump. Q1 derisks. Q2 accumulates. Q3 Expansion.」）",
      read: "改动的是他<b>自己今早那份季度剧本的时间轴</b>——早上他写「Q4 拉升、Q1 去风险、Q2 吸筹、Q3 扩张」，本条把整套季节性<b>整体前移一个季度</b>：Q3 顶替 Q4 的「见底」、Q4 顶替 Q1 的「拉升」。⚠️ 分析：① 若季节钟真的前移一季，那么「Q1 去风险」这个减仓窗口在逻辑上就该顺延到 <b>2027 Q2</b>——<b>他没说这一步</b>，但这是该论断唯一的自洽推论，等于把去风险时点又往后推一季；② 论据只有一条「这次底在 Q3 而不是 Q4」，属<b>单点观察改日历</b>，无统计检验；③ 同一套逻辑完全可以反读（底提前＝顶也可能提前），他只取了利多那一半。失效条件：① 若 <b>2027 Q1</b> 并未出现去风险式回调、或 Q4 2026 没走出他所说的「新 Q1 拉升」行情，季节移位论作废；② 若他之后悄悄把「Q1 derisks」也一并挪动而不说明理由，这份季度表不再具备验收价值。",
      tags: ["周期判断", "基准剧本", "存疑"],
      src: "X 原文 @KillaXBT · 2111432669414178850"
    },
    {
      date: "2026-10-17",
      title: "「Q4 拉升、Q1 去风险」：首次给出季度级减仓时间表",
      quote: "\"Q4 pump. Q1 derisks. Q2 accumulates. Q3 Expansion.\"（Q4 拉升。Q1 去风险。Q2 吸筹。Q3 扩张。）",
      read: "改动的是他<b>整条周期剧本的颗粒度</b>——此前他只有「2027 创新高」「126K 目标」这类长期口径（10-08 / 10-15），本条首次把周期切成<b>四个季度阶段</b>，并第一次给出明确的<b>去风险窗口：Q1</b>。⚠️ 分析：① 这是他公开口径里最接近「何时卖」的一次表述——此前所有发言都在讲别做空、别踏空，本条等于承认<b>他自己预设了减仓时点</b>；② 「Q2 accumulates」隐含 Q1 去风险后价格回落、Q2 再接回，即他预期的路径是<b>先涨、回调、再涨</b>，与他 10-11「选举后 75% 概率出现偏空行为」的回调预期可拼合；③ 本条无价位、无验收开关，季度划分短期不可证伪。失效条件：若 Q1 之前价格就已见顶回落、或 Q1 之后仍在创新高而他并不减仓，该季度表作废；若他后续给出不同的阶段划分，以最新口径为准。",
      tags: ["周期判断", "目标价", "基准剧本"],
      src: "X 原文 @KillaXBT · 2111257729407029475"
    },
    {
      date: "2026-10-17",
      title: "利空清单加码到七项，定性为「猎流动性」并预告暴力拉升",
      quote: "\"A reminder. Oil surging. MSTR delisting fears. Hot CPI. Rate hikes. Global bond yields going parabolic. DXY printing new highs. Ledger wallet hacks. They really don't want you to be long... Brother, we are dropping cause we are hunting liquidity. Nothing more. Nothing less... None of my predictions or trades have ever been based on the news. None. Its, all, fucking, noise.\"（提醒一下。油价飙升。MSTR 退市恐慌。CPI 超热。加息。全球债收益率进入抛物线。DXY 创新高。Ledger 钱包被黑。他们真不想你做多、真想你恐慌……兄弟，我们下跌是因为<b>在猎流动性</b>，没别的……我的预测和交易<b>从来没有一条基于新闻</b>……全是噪音。）",
      read: "改动的是他对<b>利空清单的规模与解释</b>——10-16 他列四项宏观利空当「抗跌证据」，本条扩到<b>七项</b>（新增油价、MSTR 退市恐慌、CPI 超热），并把下跌成因从「杂音」升级为单一机制「猎流动性」，同时放话「下一根 face ripping leg（暴力拉升）会让人说不出话」。⚠️ 分析：① 「face ripping leg」是他第一次在本轮回调里对<b>上行力度</b>给出定性（快而猛），与 10-14「87–88K 上方空头池」方向一致；② 「从未基于新闻交易」把宏观叙事整体贬为噪音，但他 10-16 自己把宏观利空当抗跌论据——<b>宏观对他「是证据还是噪音」随论点切换</b>，属口径自相矛盾点；③ 发布时 BTC 已从 10-16 低点 80,809 收回 81,615（Binance），他是在反弹初段喊话。失效条件：① 日线<b>收破 80K</b>，「猎流动性即将反向」的机制解读作废；② 若一周内价格仍在 81K 下方徘徊、拉升不来，「暴力拉升」的时点预期落空。",
      tags: ["情绪指标", "宏观驱动", "失效条件"],
      src: "X 原文 @KillaXBT · 2111196292626198901"
    },
    {
      date: "2026-10-17",
      title: "罕见点名山寨买区：SOL/LTC/ASTER/BNB，看 +50–75% 弹性",
      quote: "\"I rarely share my thoughts on altcoins... A lot of coins flushed 20–30% during this BTC drop, which is substantial considering BTC itself only fell around 8%. In the early stages of a bull cycle, I'd rather be positioned in these coins before BTC makes new highs. SOL, LTC, ASTER, BNB all look interesting to bid here. SOL 97-103 / LTC 56-59 / ASTER 0.66-0.7 / BNB 722-680. There may still be some more temporary downside, but I think the RR is starting to look attractive. If BTC makes its move towards 126K, I believe many of these coins will rally 50-75% from current prices.\"（我很少谈山寨，但很多币位置不错。这轮 BTC 只跌约 8%，很多山寨跌了 20–30%。牛市早期，我更愿意在 BTC 创新高前先埋伏这些币。四个币现在可以出价的区间：SOL 97–103 / LTC 56–59 / ASTER 0.66–0.7 / BNB 722–680。可能还有短暂下行，但盈亏比开始有吸引力。如果 BTC 走向 126K，我相信很多山寨会从现价再涨 50–75%。）",
      read: "改动的是他的<b>覆盖范围与相对强弱判断</b>——这是本 feed 收录以来他第一次公开给<b>具体山寨币买区</b>（此前只谈 BTC）。⚠️ 分析：① 核心论点「山寨跌幅大于 BTC＝牛市早期先埋伏山寨」隐含<b>山寨补涨</b>判断，是对他此前「只看 BTC 大周期」口径的一次扩圈；② 「BTC 先到 126K、山寨再涨 50–75%」把山寨行情<b>从属于 BTC 新高</b>——主逻辑未变，山寨只是更高弹性的表达；③ 本条给了可验收的具体区间（如 SOL 97–103），是近期少有的可打分条目。失效条件：① 若 BTC 跌破 80K 拖垮山寨、SOL 深跌穿 97 且他不认错，该买区作废；② 若 BTC 先创 126K 新高而山寨没涨 50–75%，相对强弱判断失效；③ 若他中途改推另一篮子币，以最新口径为准。",
      tags: ["山寨", "关键价位", "目标价"],
      src: "X 原文 @KillaXBT · 2111177575934673239"
    },
    {
      date: "2026-10-17",
      title: "USDT.D 剧本：74K 上方形成更高低点，回撤没那么深",
      quote: "\"Everyone wants the upside. Few are willing to buy the blood that comes before it. USDT.D is showcasing a scenario where BTC creates a higher low above 74K, while USDT.D continues to respect its macro downtrend. Which would imply the retrace down might not be as deep as you think.\"（人人都想要涨幅，没几个人愿意买涨幅之前的血。USDT.D（泰达市占率）正在展示这样一种情景：BTC 在 <b>74K 上方形成更高的低点</b>，同时 USDT.D 继续尊重其宏观下降趋势。这意味着<b>回撤可能没有你想的那么深</b>。）（配图为 BTC 日线，右侧 83–84K 一带有一处矩形标注区并写有 The higher low 相关字样、另有一条向右下的虚线标注，图上小字无法完全辨认，按不猜测原则不转述细节。）",
      read: "改动的是他对<b>本轮低点位置的定量预期</b>——10-13 给的下行分支是 76–78K、10-15 劝人「别执着再低 7%」，本条首次把「更高低点」的锚放到 <b>74K 上方</b>，比此前口径又放宽了 2K 左右，同时借 USDT.D 的宏观下降趋势论证「跌不深」。⚠️ 分析：① 与 10-13「2023 复刻必须在 75.5K 上方形成更高低点」基本同源，本条把要求从 75.5K 放宽到 74K 上方；② <b>74K 与他 10 倍仓失效价 74,550 几乎重合</b>——「更高低点在 74K 上方」的另一面是承认最深可接受回撤就贴着爆仓线上沿；③ 实测 10-16 低点 80,809（Binance）、10-17 现价约 81,7K，距 74K 尚有约 9%。失效条件：① 日线<b>收破 74K</b>（同时触发他 10 倍仓失效），本条「更高低点」剧本作废；② 若 USDT.D 反转走强（资金回流稳定币避险），「跌不深」的论据失效。",
      tags: ["基准剧本", "关键价位", "失效条件"],
      src: "X 原文 @KillaXBT · 2111141615788028394"
    },
    {
      date: "2026-10-16",
      title: "「市场按 mini-cycle 走」：配图标注摆动点，留悬念不展开",
      quote: "\"You have alot to learn.... Study time, not just price. The market moves in mini-cycles most people never notice. If only you knew what I know... $BTC\"（你还有很多要学……研究的是<b>时间</b>，不只是价格。市场按<b>大多数人注意不到的小周期</b>在走。要是你知道我知道的就好了。）（配图为连续黑点标注摆动高低点的走势图，疑似 mini-cycle 枢轴标记，纵轴数值无法辨认，按不猜测原则不转述。）",
      read: "改动的是他 <b>10-11「14 号日历枢轴」模型的表达方式</b>——从具体的「14 号」日期锚，泛化成「时间维度上有隐秘小周期」的神秘化表述，配图当证据但不给解读。⚠️ 分析：① 「Study time, not just price」呼应 10-11 枢轴模型的核心（时间锚先于价位），本条属该模型<b>给自己立信用的二次营销</b>；② 「If only you knew what I know」是知识垄断话术，无任何可验收内容。失效条件：本条无具体价位/日期，无独立失效开关；真正的检验仍是 14 号枢轴后是否出现他预期的向上反应——若 10 月下旬仍未出现，这套「时间周期」叙事整体降级。",
      tags: ["周期判断", "存疑"],
      src: "X 原文 @KillaXBT · 2111099094823252111"
    },
    {
      date: "2026-10-16",
      title: "一句生活鸡汤，无市场内容",
      quote: "\"Comparison is the thief of joy. Be grateful for what you have, never compare yourself to anyone, and be humble. Karma has a funny way of coming back to you.\"（比较是快乐的贼。感恩你拥有的，别和任何人比，保持谦逊。因果自有回报方式。）",
      read: "本条<b>不含任何市场判断、不含价位、不含仓位信息</b>，属纯心态箴言，与他 10-15 的 GM 鸡汤同属安抚型输出。⚠️ 分析：收录价值仅在计时——发帖时点在 10-16 BTC 收阴（81,615，Binance）当晚，他仍用「别比较、保持谦逊」的调子讲话，与同日「猎流动性」「暴力拉升预告」的多头冲锋口径并存，无新增信号。失效条件：本条无市场内容，不存在价位或方向上的失效条件。",
      tags: ["情绪指标"],
      src: "X 原文 @KillaXBT · 2111075039965573624"
    },
    {
      date: "2026-10-16",
      title: "「牛市要接被扫的低点」：自曝上一区间 76K 接过多单",
      quote: "\"You long sweeps in a bull market. I've been saying this since the previous range, where I took a long at 76K. It keeps working because every time we approach or sweep the lows, people lower their targets and start expecting the worst. You should know this by now...\"（牛市里就要在<b>扫低点</b>的时候做多。上一轮区间我就在 <b>76K</b> 接了多。它一直有效，因为每次接近或扫破低点，人们就下调目标、往最坏处想。你现在该懂了……）",
      read: "改动的是他的<b>操作手法自述</b>——本条是他本轮回调中第一次把「逢扫低点做多」上升为<b>显式规则</b>，并自曝上一区间（57K→76K 那段）在 76K 接过多单。⚠️ 分析：① 76K 这笔与 10-13 披露的 82.86K 十倍仓不同，属更早的另一笔——他的持仓拼图又补上一块；② 「每次扫低点都该接多」与 10-15「Delta 全红只需接多」同构，都是<b>单边化的指标读法</b>，规则在任何下跌里都指向买入、无失效分支；③ 隐含操作预期：若再扫 80–81K，他视为买点而非破位。失效条件：① 若下一次扫低后<b>没有反弹</b>（连续 2–3 根日线收在扫低点下方），该规则在本区间失效；② 若他自己在低点被扫后减仓，规则自我否定。",
      tags: ["仓位建议", "关键价位", "基准剧本"],
      src: "X 原文 @KillaXBT · 2111054445349855256"
    },
    {
      date: "2026-10-16",
      title: "买墙在低位被吸：需求充足、上方卖压很少",
      quote: "\"During this entire drop for BTC, we've seen some nice buy walls get absorbed, similar to what we saw in the previous range before expansion... Whales wait for the range to establish, then place bids around the lows where we are likely to see manipulation... one thing is clear, there's plenty of demand, and very few asks above us.\"（这整轮下跌里，我们看到一些漂亮的<b>买单墙被吸收</b>，和上一轮区间扩张前类似。鲸鱼等区间确立后就在低点附近挂买单——那正是最容易看到操纵的地方……有一点很明确：<b>下方需求充足，上方卖压很少</b>。）（配图为暗色流动性/清算热力图，上下布满黄色流动性条带，现价位于中部偏下，图上数值无法辨认。）",
      read: "改动的是他对<b>当前区间性质的定性</b>——10-16 凌晨他把下跌定性为「猎流动性」，本条给出同方向的<b>订单簿证据</b>（买墙被吸＝真实需求在接），并把当前结构直接类比「上一轮扩张前」，隐含<b>横盘后向上扩张</b>的预期。⚠️ 分析：① 「very few asks above us」是他第一次对上方卖压给定性判断——若成立则反弹阻力小，与 10-14「87–88K 上方空头池」不矛盾（池在 87K 以上，81–87K 之间真空）；② 「买墙被吸」是交易所订单簿快照，第三方无法独立验证，属自述证据。失效条件：① 若价格再破 80,809（10-16 低点，Binance）并逼近 80K，「需求充足」作废；② 若反弹在 84–85K 一带被明显卖压打回，「上方没卖压」证伪。",
      tags: ["基准剧本", "关键价位", "存疑"],
      src: "X 原文 @KillaXBT · 2111021836200825091"
    },
    {
      date: "2026-10-16",
      title: "「坏消息是故意放大的」：把每根阴线都解读为吓出筹码",
      quote: "\"Every time $BTC drops, there's suddenly a reason not to buy. In a bull market, bad news is deliberately amplified to scare people out of their positions. Scared money doesn't make money. Greed can stay elevated for months while the market keeps pushing higher. Study.\"（每次 BTC 下跌，就会突然冒出一个「不该买」的理由。在牛市里，坏消息是<b>被故意放大</b>的，目的就是把人从仓位里吓出去。<b>胆小的钱赚不到钱</b>。<b>贪婪可以维持数月</b>而市场继续走高。研究一下。）（配图为一张与正文论点配套的图片，无独立价位信息。）",
      read: "改动的是他对<b>下跌成因的解释框架</b>——从 10-13「买方必须亮底牌」这类结构化条件，滑向「下跌＝坏消息被故意放大＝洗筹码」的<b>纯叙事解读</b>。⚠️ 分析：① 「贪婪可以维持数月」有实质含义——他在提前给「情绪过热不等于见顶」<b>铺垫免责</b>，即未来即使恐惧贪婪指数长期高位也不构成减仓理由，与 10-12「别被恐惧贪婪指数骗」一脉相承；② 本条无价位无条件，属持有型叙事的第 7 次情绪取样。失效条件：① 若出现一次<b>与坏消息无关、且日线收破 80K / 逼近 74,550</b> 的下跌，本条「坏消息放大论」无法解释，需回到他的结构分支；② 若他本人在坏消息出现后减仓，本条自我否定。",
      tags: ["情绪指标", "基准剧本", "存疑"],
      src: "X 原文 @KillaXBT · 2110829936218935509"
    },
    {
      date: "2026-10-16",
      title: "守住 80K 的条件剧本：配图为左右形态对照，未标价位",
      quote: "\"If $BTC manages to hold above 80K, I expect this to happen:\"（如果 BTC 能<b>守住 80K 上方</b>，我预期会发生以下情况：）（配图为左右两幅并排的 K 线形态对照图，右侧图带一个标注约 83.2K 的标记框；图上<b>无完整价位刻度可读</b>，按不猜测原则不作形态细节转述。）",
      read: "改动的是他把 <b>80K 从「跌破就加仓的触发位」（10-13）升级为「整份剧本的前提条件」</b>——10-15 实盘盘中曾插到 <b>79,800（Binance）/ 79,676（Coinbase）</b>、日线收回 82,246，他随后在 80K 上方重申这份条件剧本，等于<b>把盘中破位定性为可忽略的插针</b>。⚠️ 分析：① 本条只给前提、结果细节全在图里（图不可读），可验收的只有「80K 守住与否」这一个开关；② 与他 10-13「跌破 80K 就加现货加多单、目标 95K+」对照，<b>80K 现在同时承担「守住则看涨」和「跌破则加仓」两种相反含义</b>，双向口径并存。失效条件：① 日线<b>有效收在 80K 下方</b>（10-15 那种盘中插针收回不算），本条剧本前提直接作废；② 若他后续给出与配图形态不同的另一套走势，以最新口径为准。",
      tags: ["基准剧本", "关键价位", "失效条件"],
      src: "X 原文 @KillaXBT · 2110804712719306952"
    },
    {
      date: "2026-10-16",
      title: "「所有看跌理由都是借口」：牛市延续前的标准杂音",
      quote: "\"Seems to me they are using every excuse in the book to justify why BTC should go lower. This is exactly the type of shit you see in a bull market before continuation.\"（在我看来，他们正把<b>能找到的每一个借口</b>都拿来论证 BTC 该跌。这恰恰是牛市在<b>延续之前</b>你会看到的那种东西。）",
      read: "改动的是他对<b>本轮利空清单的定性</b>——同日凌晨（00:27）他刚列举「加息、全球债收益率垂直拉升、DXY 新高、Ledger 钱包被黑」四项利空，两分钟后把这批利空统一定性为「牛市延续前的标准杂音」，即<b>利空密集≠顶部、反而佐证牛市</b>。⚠️ 分析：① 这把他 10-03「在牛市里」的框架进一步固化成<b>不可证伪结构</b>——利空被解释成牛市证据，利多自然也是证据；② 与他 10-11 自认「选举后有 75% 概率出现偏空行为」仍有未调和的张力。失效条件：① 若价格在利空密集期<b>日线收破 80K</b>，本条「杂音论」作废；② 若他本人随后承认某个利空有实质影响（例如为此调整仓位），本条被自我否定。",
      tags: ["情绪指标", "宏观驱动"],
      src: "X 原文 @KillaXBT · 2110771027827675612"
    },
    {
      date: "2026-10-16",
      title: "四重宏观利空压顶，「BTC 仍守在 80K 上方」当抗跌证据",
      quote: "\"Rate hikes. Global bond yields going vertical. DXY printing new highs. Ledger wallet hacks. And yet $BTC is still holding above 80K.\"（加息。<b>全球债券收益率垂直拉升</b>。<b>DXY 创新高</b>。<b>Ledger 钱包被黑</b>。然而 BTC <b>仍守在 80K 上方</b>。）",
      read: "改动的是他的<b>抗跌论证来源</b>——此前论据主要是技术结构（清算池、USDT.D、Delta），本条首次把<b>宏观利空清单</b>整体搬出来当「BTC 强势」的反衬，并把 80K 明确标为当下的<b>事实防守线</b>。⚠️ 分析：① 关键背景：10-15 日内 BTC 曾跌到 <b>79,800（Binance）/ 79,676（Coinbase）</b>，他说「仍守在 80K 上方」依据的是收回后的价位（收盘 82,246）——严格说 80K 已被盘中击穿过一次，他的表述<b>选择性忽略了插针</b>；② 本条等于把 80K 的意义从「他自设的加仓触发位」升格为「市场已被验证的支撑」，但验证方式恰是一次盘中破位，属<b>带瑕疵的证据</b>。失效条件：① 日线<b>收在 80K 下方</b>即直接推翻本条；② 若 DXY/收益率继续走高压垮风险偏好、BTC 再度插针 80K 下方，「抗跌」叙事失效；③ 若他不再提 80K 或把防线悄悄下移，说明该位已被他放弃。",
      tags: ["宏观驱动", "关键价位"],
      src: "X 原文 @KillaXBT · 2110769622731329607"
    },
    {
      date: "2026-10-15",
      title: "「激动时刻快到了」：让他们继续预期最坏",
      quote: "\"Exciting times soon. Let them expect the worst... $BTC\"（激动人心的时刻快到了。让他们继续往最坏处预期……）（配图为左右两幅带圆点标注的历史走势对照图，圆点标记转折位，图上数值无法辨认，按不猜测原则不转述。）",
      read: "改动的是他对<b>近期时点的信心表达</b>——发布于 10-15 晚上（14 号枢轴兑现当晚），可视为对枢轴模型反向拉升预期的<b>二次确认</b>：看空叙事浓＝他反着押。⚠️ 分析：① 本条是 10-15 至 10-17 一连串多头口径（枢轴兑现→猎流动性→买墙被吸→暴力拉升预告）的<b>最早一环</b>，整条时间线方向一致、逐步加码；② 无价位、无时间窗，「soon」不可验收。失效条件：① 若 10 月下旬前没有出现他暗示的向上反应，与枢轴模型一同落空；② 若他随后改口「还需要更多时间筑底」，视为口径漂移。",
      tags: ["周期判断", "情绪指标"],
      src: "X 原文 @KillaXBT · 2110722605527486961"
    },
    {
      date: "2026-10-15",
      title: "「距 75K 仅 7%、距 126K 有 56%」：劝人别为抄底踏空",
      quote: "\"We're 7% away from 75K. We're 56% away from 126K. Maybe we test 75K, maybe we don't. Nobody can say with 100% certainty, not even me. So humble yourself and ask, are you really willing to risk missing a 56% move to new highs because you're fixated on buying 7% lower? I said the same thing when $BTC was at 60K. People were waiting for 50K, trying to squeeze out another 10%, and ended up missing the entire move. The market has a funny way of never giving you exactly what you want. And even when it does, people move the goalposts and ask for more.\"（我们<b>距 75K 只有 7%</b>，<b>距 126K 有 56%</b>。也许会测 75K，也许不会。没人能 100% 确定，我也不能。所以谦逊一点，问问自己：你真的愿意因为执着于<b>再低 7% 买入</b>，而去冒<b>错过 56% 涨向新高</b>的风险吗？BTC 在 60K 时我说过同样的话。人们等着 50K，想再挤 10%，结果错过了整段行情。市场总有不按你要的价位给你的方式。就算给了，人们又会移动球门柱、要求更多。）",
      read: "改动的是他对<b>下行空间的公开口径</b>——10-09 他说「再测 75K 都算礼物」是拒绝性表述，本条首次把「<b>也许会测 75K、也许不会</b>」写成平等的两种可能，并用 60K→126K 的赔率对比劝人别等回调，等于把 75K 从「不太会到的位」降级为「可接受的小回撤」。⚠️ 分析：① 数字上最要命的一点：<b>75K 距他 10 倍仓失效价 74,550 只有约 450 美元</b>——他一边劝人「别等 75K」，一边自己的杠杆仓死线就贴在 75K 下方，若真去测 75K，10 倍仓会被一起带走并触发「失效即再开第二个 10 倍」的叠加规则；② 这是典型的<b>踏空焦虑叙事</b>（与 10-05「等再低 2–3% 的人全被抢跑」同源），出现频率上升通常伴随他对持仓浮亏的敏感；③ 126K 引用与 10-08「126,000 next year」一致，未变。失效条件：① 若价格<b>跌破 75K 甚至 74,550</b>，本条「7% 小回撤」定性失效，同时触发 10 倍仓失效与加仓规则——将是整套剧本最重的一次压力测试；② 若他接下来在更低位置减仓而非加仓，本条劝多口径自我否定。",
      tags: ["目标价", "关键价位", "仓位建议"],
      src: "X 原文 @KillaXBT · 2110710451281543632"
    },
    {
      date: "2026-10-15",
      title: "个人消息门槛上抬：做体量的可私信，公开剧本继续发",
      quote: "\"If anyone is trading size, DM me personally. Wanna connect.\"（任何在<b>做体量</b>的人，可以直接私信我，想认识一下。）",
      read: "改动的是他此前的<b>对外沟通口径</b>——从「公开发推 + 公开置顶视频」的单向输出，第一次<b>主动开放大资金交易者的私下连接</b>。⚠️ 分析：本条<b>不含任何市场判断、不含任何价位</b>，属关系/资源动作而非观点。放在同一天「Outlook 视频 + 图表长文」之后看，可理解为在公开叙事之外另开一条不公开的沟通渠道——需注意这类私信邀请在加密领域常伴随付费社群、信号群或分成合作的后续动作，本轮无任何证据说明性质，<b>不作任何推测</b>。失效条件：本条无可验收市场内容；唯一需盯的是他后续是否把私信渠道变成收费服务——若如此，则其公开表态与付费内容的关系需要重新评估（公开部分是否仍完整）。",
      tags: ["存疑"],
      src: "X 原文 @KillaXBT · 2110511287906258998"
    },
    {
      date: "2026-10-15",
      title: "用 Delta 全红论证「自 57K 以来只需逢跌接多」",
      quote: "\"$BTC delta is extended red. Pretty much, all you've had to do is bid and build longs during these extended periods of stops being taken out. That's been the case since $57K.\"（BTC 的 <b>Delta 已经极度偏红</b>（卖方成交占绝对主导）。基本上，在这些<b>止损被打掉的延长时段</b>里，你唯一需要做的就是<b>接货、建多单</b>。从 <b>57K</b> 以来一直是这样。）（配图为他自制的 Delta／累计成交量差指标图：价格下方用矩形框标出几处「Delta 极红」的时段，红绿柱为成交量差，2026 年年中至 10 月这段的柱体明显偏绿（正 Delta）、价格同期上行。）",
      read: "改动的是他 <b>10-09 长文里「更广泛的回调会发生在 92–95K」</b>那条——本条把「回调」重新定性为<b>逢跌买入窗口</b>，并把这条规则<b>回溯到 57K</b>（他 09-27 自设的周期失效位），等于把 57K→当前 的整段下跌都用「止损被打掉 = 接货点」解释掉。⚠️ 分析：这是一条<b>事后归因式</b>表述——Delta 全红本身是客观指标读数，但「只需接多」是把指标读法绑定到了单一方向；把起点定在 57K（几乎等于他模型的最低位）会让这条规则<b>在任何一次回调中都能自称成立</b>，可证伪性低。它与同日「只要高周期就只会更高」、以及 10-14「几个月后要记住所有空头」构成同一天的三连<b>持有型叙事</b>。失效条件：① 若价格有效跌破他 10-13 自设的 <b>76–78K</b> 分支、并朝他 10 倍仓失效价 <b>74,550</b> 去，那么「从 57K 以来只需接多」就等于把一整段亏损区间认下来，这条将首次被反向检验；② 若他随后在回调中改为<b>减仓或做空</b>（例如此前多次预告的对冲），本条规则自我否定。",
      tags: ["情绪指标", "仓位建议", "存疑"],
      src: "X 原文 @KillaXBT · 2110474017211928870"
    },
    {
      date: "2026-10-15",
      title: "喊话记住所有空头：几个月后回看，「场边人」到处都是",
      quote: "\"A few months from now, make sure to remember all the bears. I know I won't forget. You can smell sideliners everywhere.\"（几个月之后，记得<b>把当时所有看空的人记下来</b>。我知道我不会忘。你到处都能闻到<b>场边观望者</b>的味道。）",
      read: "改动的是他 <b>10-08 以来对空方叙事的处理方式</b>——此前是针对具体观点逐条反驳（如 10-09「等 70K 的人可能永远等不到」），本条升级为<b>提前记账式的信誉对赌</b>：把「看空的人」整体标记为未来会被证明错误的一方。⚠️ 分析：① 这是典型的<b>不可证伪的立场表态</b>——「记住空头」没有时间点、没有价位、没有失效条件；② 它与他 10-11「选举后有 75% 概率出现偏空行为」<b>存在自我矛盾</b>：他一边承认选举后大概率回调、一边要求所有人记住看空者的错误；③ 从沟通策略看，这类发言通常出现在<b>持仓承压、需要稳住跟随者情绪</b>的时点——本条发布于价格自 10-12 的 84,352 回落、10-14 收阴之后。失效条件：本条本身不可验收。真正能反过来打脸的场景只有一个——若未来几个月 BTC 确实创出显著新低，那么「记住所有空头」的记账对象会变成他自己；反之若如他所料走高，这条也只是口号兑现，不构成任何新的分析依据。",
      tags: ["情绪指标", "战绩复盘"],
      src: "X 原文 @KillaXBT · 2110438190389620986"
    },
    {
      date: "2026-10-15",
      title: "14 号枢轴兑现：跌进枢轴＝反向拉升，再摸 87–88K 也可能",
      quote: "\"Seems like we're dumping into the 14th. You know the drill. We've seen this play out many times before, when a bearish narrative builds into this date, $BTC has a habit of doing the opposite. Let's see if we get that same PA again. Its only been happening for 1 year +\"（看起来我们正在<b>跌进 14 号</b>。你知道套路。我们以前见过很多次——当<b>看空叙事在 14 号之前堆积起来</b>时，BTC 的习惯是<b>反着走</b>。看看这次会不会是同样的价格行为。这已经持续了一年多。）",
      read: "改动的是他 <b>10-11「第 14 个日历枢轴」</b>与 <b>10-13「14 号前的叙事明显偏空」</b>两条——本条是枢轴模型的<b>兑现确认</b>：他认定「跌进 14 号」这个条件已成立，因此按模型应出现反向（向上）反应，并给出一致的方向读法（但本条未给价位）。⚠️ 分析：① 模型口径<b>前后自洽</b>——10-11 他就说过自己偏好「先盘底、枢轴后再上」，本条之前的下跌正好落在这条偏好路径上，属<b>事后吻合</b>而非新信息；② 但「Its only been happening for 1 year +」把样本期缩到一年多，与他 10-11 自称「追踪一年半」略有出入，属口径微调；③ 本条与他 10-13 同时给出的 <b>87–88K 上方空头池</b>互相支撑，构成「跌完再摸上方」的完整路径。⚠️ 与之矛盾的一面：他 10-13 凌晨曾说本轮「最后一次扫低已在 81K 完成」，而 10-14 至 10-15 又出现更低点（81,444 / 80,226），说明「低点已完成」的判断至少被延后了一次。失效条件：① 枢轴模型失效＝14 号之后<b>没有出现向上反应</b>、反而延续跌势有效跌破 80K；② 时间上，他说的是「14 号前后不久」——若这波反向拉升拖到 10 月下旬仍未发生，则该模型至少这一轮落空；③ 若他自己在枢轴兑现后改口「本次是例外」，模型即失效。",
      tags: ["周期判断", "关键价位", "失效条件"],
      src: "X 原文 @KillaXBT · 2110422812150435998"
    },
    {
      date: "2026-10-15",
      title: "发布视频版「临选举，我的计划」，正文仍不给数字",
      quote: "\"Outlook for $BTC. Midterms approaching. My plans.\"（BTC 展望。<b>中期选举临近</b>。我的计划。）（推文正文仅此一句；<b>正文本身不含任何价位或结论</b>。经工具探测确认：本条附带的是<b>视频</b>（含 amplify 视频缩略图 / videoPlayer 组件），并同时带一张固定图表（tweetPhoto），与他 10-09 那条 8 分 38 秒视频《Update for \$BTC — Plans, scenarios, expecations.》结构相同，属同一系列的更新版。<b>视频内容无法转写</b>，按「不猜测」原则不作任何转述。）",
      read: "改动的是他对外沟通的<b>形式与节奏</b>——把「中期选举」这个锚点从零散推文（10-04 / 10-11 / 10-14 的选举推）收束成一条<b>带视频的系统性剧本更新</b>，与 10-09 那条置顶视频形成「每几天一次」的完整更新节奏。⚠️ 分析：本条<b>不能当作方向或点位依据</b>——正文只有一句话，所有信息都在视频里；唯一可用信息是「他围绕选举重新发布了一份完整计划」这一事实，说明他仍把 11 月初的选举当作未来几周的核心变量。⚠️ 同日另有一条<b>底部评论区堆叠</b>：他 10-14 的选举推下有人追问「你字里行间在暗示新低、那 57K 是什么」，他回复「<b>我不是在暗示跌破 57K 形成新低，我是在暗示形成一个更高的低点，而且更快</b>」——这条回复才是本条视频的口径注脚，方向仍是偏多。失效条件：本条无可验收内容；可追踪的是视频里的具体剧本，若他随后在公开文本里给出与本系列视频不一致的价位（例如从「更高低点」改口为新低），则以最新公开文本为准。建议直接在 X 上观看该视频核对。",
      tags: ["宏观驱动", "基准剧本", "存疑"],
      src: "X 原文 @KillaXBT · 2110406783550546330"
    },
    {
      date: "2026-10-15",
      title: "中期选举底部模型升级：低点来得越来越早，最快选举前见底",
      quote: "\"In 2014, BTC bottomed 71 days after the midterms. In 2018, BTC bottomed 39 days after the midterms. In 2022, BTC bottomed 13 days after the midterms. In 2026, the midterms are in 3 weeks. The pattern suggests that we are bottoming sooner an sooner. 71 - 39 = 32 days quicker. 39-13 = 26 days quicker. So maybe, just maybe, $BTC bottoms before the midterms. Instead of derisking afterwards, we could simply continue the uptrend.\"（2014 年，BTC 在中期选举<b>之后 71 天</b>见底。2018 年，<b>之后 39 天</b>。2022 年，<b>之后 13 天</b>。2026 年，中期选举还有 <b>3 周</b>。这个规律显示我们见底<b>越来越早</b>。71 − 39 = 提前 32 天；39 − 13 = 提前 26 天。所以，也许、只是也许，<b>BTC 会在中期选举之前就见底</b>。那么我们就<b>不需要在选举之后去风险</b>，而是可以<b>直接延续上升趋势</b>。） 他随后另发一条澄清：\"I am not implying we form a new low below 57K. I am implying we form a higher low instead. Sooner.\"（<b>我不是在暗示我们会跌破 57K 形成新低</b>。我是在暗示我们会<b>形成一个更高的低点，而且更快</b>。）（配图为他自制的统计图《Bitcoin bottoms after US midterms are arriving sooner》——三张并列周期图，纵轴为「距中期选举的天数」，2014 标注 Nov 04、底部 Jan 14-15 的 \$176（−47%）；2018 标注 Nov 06、底部 Dec 15-18 的 \$3,185（−51%）；2022 标注 Nov 08、底部 Nov 21-22 的 \$15,778（−15%）；图下注明数据来自 Coin Metrics 每日 ETHUSD 参考价、阴影为「选举→周期低点」区间、非投资建议。）",
      read: "改动的是他 <b>10-11「选举后回调只做更高低点 + 去风险在选举之后」</b>这条的核心时间结构——本轮<b>把「去风险」这一步从时间轴上挪走了</b>：他本来主张「先上推、选举后再去风险」，现在改说「底部来得越来越早、可能选举前就见底，那就不需要选举后去风险」。⚠️ 分析：① 这是<b>从 10-11 的双分支剧本向单边乐观的收敛</b>——10-11 还保留「跌进选举」的分支，本条把「选举前见底 → 直接续涨」提升为主推演；② 方法上有明显问题：他取自制的「71 / 39 / 13 天」递减数列（斜体趋势线，无统计检验）外推为「早晚会到负数」，属<b>三点外推</b>，且样本仅 3 次、选举日期与周期位置都不同；③ 与他 <b>09-29 专门写长文否定历史分形</b>、此后又反复使用分形（2023 类比、本条选举递推）的摇摆一致，<b>「反分形 → 用分形」的模式又一次出现</b>；④ 澄清条（「不是新低、是更高低点、更快」）说明他清楚这条容易被读成看空，因此主动堵漏——这与他 10-13「76–78K」的下行分支同时存在，两套口径并未统一。失效条件：① 时间验收——中期选举（约 11-03）前若<b>没有形成他所说的「更高的低点」</b>，而是继续走低，本条「选举前见底」落空，回到 10-11 的「选举后去风险」分支；② 价格验收——若出现<b>跌破 80K 并朝 76–78K / 74,550 去</b>的走势，则「更高低点」与「不创周期新低」同时失效；③ 若选举后他仍按 10-11 说的「去风险」执行，说明本条只是修辞而非剧本更替。",
      tags: ["周期判断", "宏观驱动", "基准剧本"],
      src: "X 原文 @KillaXBT · 2110360470410416202"
    },
    {
      date: "2026-10-15",
      title: "20 亿多单在 CPI 前被扫光，反问「接下来会发生什么」",
      quote: "\"2 billion longs taken out. Directly into CPI. In a bullish trend. In a bull market. I wonder what happens next\"（<b>20 亿美元</b>的多头被打掉。直冲 <b>CPI</b>。<b>在上涨趋势里</b>。<b>在牛市里</b>。我很好奇接下来会发生什么）",
      read: "改动的是他 <b>10-12 深夜「买方必须亮底牌、否则 80K 防御可能只是诱多」</b>那条的偏空语气——本条把同样一笔清算<b>重新叙述成利多前置条件</b>：多头被扫光 → 卖压释放 → 在牛市结构里，下一站应是反弹。⚠️ 分析：① 属他惯用的「<b>杠杆出清即利多</b>」框架（与 10-10「长头清算潮＝局部底」同源），本次新增的变量是 <b>CPI 数据</b>，即他预期的催化剂是一个<b>外部宏观事件</b>而非技术结构；② 「20 亿」这个数字与 10-11「近 20 亿」、10-14 的清算图数据连续出现，互为引用，但均为<b>自述口径、无独立来源</b>（本机第三方数据不可得，已标注）；③ 本条<b>不含价位、不含止损、不含目标</b>，属情绪铺垫条。失效条件：① CPI 公布后<b>若价格没有按他的方向反弹、反而延续下跌</b>，则「清算即利多 + 牛市结构」这条双重前提至少被打断一条；② 若随后再次出现同量级的多头清算（说明「扫干净」是错的），本条逻辑需要重新表述；③ 本条自身的验收点只有「他预期的反弹是否出现」，无具体价位。",
      tags: ["情绪指标", "宏观驱动", "失效条件"],
      src: "X 原文 @KillaXBT · 2110344400434082076"
    },
    {
      date: "2026-10-15",
      title: "一句 GM + 鸡汤，无市场内容",
      quote: "\"GM. Fear kills more dreams than failure ever will.\"（早上好。<b>恐惧毁掉的梦想，比失败毁掉的还多</b>。）",
      read: "本条<b>不含任何市场判断、不含价位、不含仓位信息</b>，属日常问候 + 心态箴言，与他 10-12「别像苍蝇一样吃、像大象一样拉」那条同属<b>心态类输出</b>。⚠️ 分析：收录它的唯一价值是<b>计时</b>——说明 10-14 上午他仍在按「长期持有、别被波动干扰」的调子在跟社区讲话，与同期「20 亿多单被扫」「跌进 14 号」的偏空实况并存，属<b>安抚型发言</b>。失效条件：本条无市场内容，不存在价位或方向上的失效条件；后续若他改用「警惕 / 减仓」类措辞，才是可注意的口径变化信号。",
      tags: ["情绪指标"],
      src: "X 原文 @KillaXBT · 2110327330208170035"
    },
    {
      date: "2026-10-14",
      title: "14 号枢轴兑现首日：两次探 81K 被秒买，看多反应延续全月",
      quote: "\"$BTC The narrative into the 14th is definitely more bearish than bullish. We've seen two hunts of 81K. The latest came late last night during the Asian session and was bought up almost immediately after stops were taken below the lows. That makes me think we're more likely to see a bullish reaction shortly after the 14th, carrying through the rest of the month. Another hunt of the highs toward 87-88K is possible.\"（BTC：<b>进入 14 号的叙事明显偏空多于偏多</b>。我们已经看到<b>两次对 81K 的猎杀</b>。最近一次发生在<b>昨夜亚洲时段</b>，在<b>低点下方扫掉止损之后被几乎立刻买回</b>。这让我认为，<b>14 号之后不久更可能看到一波看多反应，并延续到本月剩余时间</b>。而<b>再一次向 87–88K 的高点猎杀也是可能的</b>。（本条为回复式推文，引的是他自己 10-11 的「第 14 个日历枢轴」。））（配图为他自制的走势图：价格下方用绿点标注两处清算位置，附文字 <b>2.5B+ LIQUIDATED AT THE LOWS INTO THE 14TH, LONGS TAKEN OUT</b>；图上价格在 81K–85K 之间来回，右端一条虚线延伸向 14 号。）",
      read: "改动的是他 <b>10-11「第 14 个日历枢轴」</b>——本条是枢轴模型的<b>方向落点</b>：他首次给出「14 号之后不久看多、并延续到月底」这一<b>带时间跨度的方向判断</b>，同时把上方目标锁定在 <b>87–88K</b>（与他 10-12「上方只剩 86–88K 空头」、10-13「87K 挂着 5B 清算」完全对齐）。⚠️ 分析：① 三条不同日期的推文（10-12 / 10-13 / 10-14）已把 <b>86–88K 同一个带区</b>分别讲成「空头在哪」「空头有多少」「要再猎一次」，<b>叙事高度一致</b>，这是本轮最连贯的一条链；② 但他引用的「两次探 81K」与实际数据存在差异：Binance 日线显示 10-13 低点 <b>81,033</b>、10-14 低点 <b>81,444</b>，属「两次探 81K 附近」的上沿口径，<b>未构成夸报但也不精确</b>；③ 真正与当时不一致的是「被几乎立刻买回」——10-14 收在 <b>81,682</b>（当日开盘 84,146，收阴），10-15 进一步下探 <b>80,226</b>，「立刻买回」只在小周期成立。失效条件：① 时间验收——他给的是「14 号之后不久、延续到本月剩余时间」，若 10 月剩余的交易日<b>没能走出上行并靠近 87–88K</b>，本条落空；② 价格验收——若有效跌破 <b>80K</b>（他自己说过「多头真的不想丢掉 80K」），则本条「两次探底被买回」的读法反转为他 10-13 的 76–78K 分支；③ 若他向 87–88K 的猎杀未出现挤压、反而成为新一轮下跌起点，则该区间「燃料池」的性质需要重估。",
      tags: ["周期判断", "关键价位", "情绪指标"],
      src: "X 原文 @KillaXBT · 2110082903443116269"
    },
    {
      date: "2026-10-14",
      title: "反向押注预测市场：断言 2027 年必创新高，称 30% 概率「疯了」",
      quote: "\"There's absolutely no fucking way this doesn't hit 100%. I'm telling you now with confidence $BTC makes a new ATH in 2027. 30% odds is insane. People are way to fucking bearish. I already calculated the math...\"（这<b>绝对不可能不到 100%</b>。我现在就明确告诉你，我有信心：<b>BTC 会在 2027 年创出新的历史高点</b>。<b>30% 的概率？这太离谱了</b>。人们<b>太他妈的看空了</b>。我已经算过数学了……）（引推为一条新闻/市场贴：\"BREAKING: 30% chance Bitcoin hits a new all-time high within the next year\"（快讯：比特币在<b>未来一年内创下历史新高</b>的概率为 <b>30%</b>）。）（配图三张，均已读取：① 一张 <b>Kalshi Pro</b> 的周线 BTC 图表，右侧列出多个市场报价——包含「2026 bottom?」「2027 bottom?」「Next ATH?」等区间与概率，图上还用竖条标出 2027 / 2028 的预测窗口，其余小字分辨率不足无法逐一确认；② 一张 BTC 图标；③ 一张 <b>Kalshi</b> 市场截图：《When will Bitcoin hit \$130k?》——「<b>By Jul 8, 2027</b>」的概率为 <b>30%</b>，附该市场的概率历史走势曲线。）",
      read: "改动的是他 <b>10-05「4/26–8/2 破 ATH 窗口（2027）」</b>与 <b>10-11「2029 年见 160-180K」</b>这组时间表——本条第一次把长周期目标<b>拿去和预测市场的报价正面对撞</b>，并给出自己的概率判断：Kalshi 给「2027-07-08 前见 130K」是 30%，他认为<b>这个概率太低、实际应接近 100%</b>。⚠️ 分析：① 这是本轮<b>第一次出现「外部可结算市场」作为对照物</b>——Kalshi 的 30% 是真实赔率，可独立核验，比他自己给的「75% 拒绝概率」「2029 年 160-180K」这类自设数字更硬；② 需要注意他<b>混淆了两个不同的命题</b>：他断言的是「<b>2027 年内创新高</b>」，而引推说的是「<b>未来一年内创新高</b>」（即到 2027 年 10 月），配图③又是「<b>2027-07-08 前见 130K</b>」——三者时间窗与价格门槛都不同，他并未区分，属<b>口径混用</b>；③ 「我已经算过数学」未给任何计算过程，属<b>不可核查的自信表述</b>；④ 与 10-11「2029 年 160-180K」相比，本条的 2027 创新高是<b>更早、更硬的时间承诺</b>——两条并行等于他把 2027（创新高 / 126K）与 2029（160-180K）排成阶梯，加上本条就把 2027 这条压到了「接近确定」的强度。失效条件：① 最直接的验收点——<b>2027 年内若未创出历史新高，本条（以及他「30% 太低」的判断）被市场公开打脸</b>；② 更近的检验是引推本身的时间窗，即未来一年内（至 2027 年 10 月）能否创新高；③ 若他在此期间把口径改回 10-11 的「2029 年 160-180K」而不提 2027，说明本条是其表述中弹性最大的一条。",
      tags: ["目标价", "周期判断", "宏观驱动"],
      src: "X 原文 @KillaXBT · 2110064229625536521"
    },
    {
      date: "2026-10-14",
      title: "长线多单更新：周线 HH + 100/200 EMA 交叉，收复全部均线，底部确认",
      quote: "\"Well, it's been a while since I've updated this position. This was one of my boldest positions. Longing the $BTC bottom publicly. There's not much to update apart from the fact that we're going a lot higher on the HTF. We've formed a weekly HH, flipped the 100 and 200 EMAs on the weekly and are forming a crossover. We've also flipped almost every single moving average metric, confirming that the bottom is in. The only difference is seasonality. The only thing making people question this is the fact that we didn't bottom in Q4. Did you really have to be that naive to think we'd follow the exact same pattern every single cycle forever? That's just not logical. Markets evolve. BTC is evolving. As for my target, it's still the same. In fact, we could go higher. But I won't be closing anything from this particular long position until we're trading above $0.15M per coin. We're still 60% away from the ATH. There's still money to be made, even if you didn't get the best entry. Till then, the trend is your friend. You shouldn't be taking any shorts below ATH.\"（好吧，这笔仓位有一段时间没更新了。<b>这是我最大胆的仓位之一</b>——公开做多 BTC 的底部。除了「我们在高周期上还会走<b>高得多</b>」之外，没什么可更新的：我们做出了<b>周线更高的高点</b>、<b>翻转了周线 100 和 200 EMA</b>并正在形成<b>金叉</b>；我们还几乎<b>翻转了每一项均线指标</b>，这<b>确认了底部已经形成</b>。唯一的差别是季节性——唯一让人质疑的原因，是我们<b>没有在 Q4 见底</b>。你真的天真到以为我们会在每一个周期里都<b>照搬一模一样的形态</b>吗？这根本不合逻辑。市场在演化，BTC 也在演化。至于我的目标——<b>还是不变，事实上可能更高</b>。但在 BTC <b>交易到 0.15M（15 万美元）以上</b>之前，这个特定的多单仓位我<b>一分钱都不会平</b>。我们距历史高点还有 <b>60%</b> 的空间。即使你没拿到最好的入场价，<b>还有钱可赚</b>。在那之前，<b>趋势是你的朋友。你不该在历史高点下方做任何空</b>。）引推是他自己 2025 年那条：「I am officially swing long on $BTC. Invalidation 31950. Target 160,000. I will see you in 1-2 years from now.」（我正式波段做多 BTC。<b>失效 31,950。目标 160,000</b>。1–2 年后见。））（配图两张，均已读取：① 一张周线 BTC 图，价格自 4 万下方一路上行至 12 万+，右侧 <b>SWING ENTRY 3X LEVERAGE</b> 标注的入场带在 <b>20,766–23,332</b> 附近，白色方框自入场带向右延伸——<b>即这笔仓位的实际成本在 2 万–2.3 万美元区间，而非此前推文里提到的 6 万+/7 万+/8 万美元那几笔</b>；② 另一版本同图，白框范围相同。注：入场带文字的精确读数受截图分辨率限制，方向确定、具体上下沿可能有数百美元的误差。）",
      read: "改动的是他 <b>09-29 以来对外披露的「三笔多单」结构</b>——此前他反复点名的持仓是 <b>62.6K / 76.4K / 82.860（10 倍）</b>，本条首次把一笔<b>更早、更低成本的长线仓位</b>（引推标 <b>3 倍杠杆、入场约 2.08 万–2.33 万、失效 31,950、目标 160,000</b>）重新拿出来更新。⚠️ 分析：① 这条<b>大幅改写了他的持仓叙事</b>——按图上的成本带，这笔仓位的浮盈是数倍级别，这才是他「心态稳、敢满仓、敢扛回撤」的真实底层；此前对外只讲 6 万以上的几笔，容易让跟随者低估其实际成本优势与风险承受力；② 技术判据上，他给的「周线 HH + 100/200 EMA 翻转并金叉 + 几乎所有均线指标翻转」是一组<b>可核验的趋势级证据</b>，是他近期最硬的一条多头论据；③ 但「<b>0.15M 之前不平任何一笔</b>」是一个<b>极高的承诺门槛</b>——按 10-14 的 8 万上下算，距离 15 万还有近 <b>90%</b>；④ 「唯一让人质疑的是季节性／我们没在 Q4 见底」直接<b>否定了季节性框架</b>（他 10-01 曾用「所有关键 HTF 均线」替换季节性判定，本条又在同一条上加固），并再次使用「市场在演化」这种<b>不可证伪的解释</b>；⑤ 「不该在历史高点下方做任何空」与他 10-06 曾给出 <b>89.4–90.6K 对冲空单</b>直接冲突——那条计划在本条口径下等于被正式废除。失效条件：① 硬失效——他引推里写明的 <b>31,950</b>（该仓位的原始失效位）；② 目标失效——若 BTC 未走到 <b>150,000</b> 而他在其下方平掉这笔仓位（哪怕部分），则本条承诺作废；③ 论据失效——「周线 HH + 100/200 EMA 金叉 + 底部已成」若被价格打破（例如周线重新跌破并形成更低低点），这套趋势判据需要重写。",
      tags: ["仓位建议", "周期判断", "目标价"],
      src: "X 原文 @KillaXBT · 2110049995160162484"
    },
    {
      date: "2026-10-14",
      title: "回怼低周期交易者：别为几个点翻来覆去，只看高周期",
      quote: "\"Don't eat like a fly and shit like an elephant. Too many people scalp peanuts on LTF moves, flipping their bias every day, only to get wiped out by one big move because they're deluded into thinking they can catch every $BTC movement. It's okay not to catch every move. It's okay not to open a new position every day. Just chill. Focus on what matters. the HTF.\"（<b>别像苍蝇一样吃、像大象一样拉</b>。太多人在低周期上来回抠那点蝇头小利、天天翻自己的方向，结果被一个大波动带走——因为他们自欺欺人地以为能抓住 BTC 的<b>每一次</b>波动。<b>抓不到每一次也没关系，不是每天都必须开新仓。</b>放松点，盯着真正重要的东西：<b>高周期</b>。）",
      read: "改动的是他 <b>10-12「自夸周一高点枢轴策略、区间震荡里抓 2–3% 反向波」</b>那条——本条实际上是<b>对自己那套短线打法的自我否定</b>：他前一天还在炫耀低周期枢轴策略，本条却把「在低周期抠点」讲成会被一次大波动清掉的坏习惯。⚠️ 分析：① 这是本轮最明显的<b>内部不一致</b>之一（同一周内既推低周期枢轴、又劝人别看低周期）；② 更可能的解释是他把<b>对外沟通的对象做了区分</b>——短线工具留给自己/小圈子，公开口径统一压到「长期持有」上，这与他 10-14 同一时段「0.15M 前不平任何一笔」「不该在 ATH 下方做空」的持有型叙事一致；③ 本条<b>不含价位、不含方向</b>，属方法论表态。失效条件：本条无市场内容可验收；可追踪的是——若他随后继续高频发布低周期枢轴/日内判断并以此邀功，本条「只看 HTF」的劝告即被自己证伪。",
      tags: ["周期判断", "情绪指标"],
      src: "X 原文 @KillaXBT · 2110003846067974192"
    },
    {
      date: "2026-10-14",
      title: "给出 2023 复刻的启动条件：先做 75.5K 上方更高低点、守住 80K",
      quote: "\"If $BTC is going to follow this schematic, It needs to form a HL above 75.5K and, ideally, hold above the 80K lows. That would be similar to 2023, when we formed a weekly HH, then came back to retest and respect the range. That probably explains why the LTF action feels so hunt heavy, aggressive and algorithmic. We reclaimed internal structure in the 82Ks, came down to retest it, broke structure again, then reclaimed it once more. It feels like the market is working hard to bait people. I'll admit, that initial move back down into the 81Ks didn't look great from a structure perspective. But around that time, a lot of shorts were piling in at the lows, which helps explain the reaction. Another interesting detail is only around 300M in longs were liquidated on the move from 84.1K to 81K, compared with more than 2B on the move from 86.8K to 80.6K. That decline in long liquidations suggests the market is becoming less long-dominant than it was before. Interesting times. We need to form a higher low and leg up from here. Otherwise, this correction could take us below 80K. For now, the plunge protection team is doing a good job of maintaining price while fucking with the LTF internal range.\"（如果 BTC 要走<b>这套示意结构</b>，它需要<b>在 75.5K 上方形成一个更高低点</b>，并且<b>最好守住 80K 的低点</b>。那就类似于 <b>2023 年</b>——当时我们先做出周线更高的高点，然后回来<b>回测并尊重那个区间</b>。这大概也解释了为什么<b>低周期的走势感觉如此猎杀式、凶悍、算法化</b>：我们在 <b>82K 段</b>收复了内部结构、下来回测、再次破结构、然后又一次收复。<b>感觉市场在很努力地钓人。</b>我承认，最初那次跌回 <b>81K 段</b>从结构上看并不好看。但大约在那时，<b>很多空头在低点堆积</b>，这有助于解释随后的反应。另一个有意思的细节：从 <b>84.1K 跌到 81K</b> 的过程中只有约 <b>3 亿美元</b>多头被清算，而从 <b>86.8K 跌到 80.6K</b> 时是<b>超过 20 亿美元</b>。多头清算量的下降说明<b>市场的多头主导程度不如从前了</b>。有意思。我们<b>需要形成一个更高的低点、并从那里向上抬腿</b>，否则这轮回调<b>可能把我们带到 80K 以下</b>。目前<b>护盘队</b>在一边维持价格、一边折腾低周期内部区间，干得不错。）（本条为回复式推文，引的是他自己 10-11 那条「Simulation. Is. Real...」的并排形态对照图。）（配图两张，均已读取：① 一张 BTC 走势图，图上用<b>绿点标出两处低点</b>（约 6.7 万–7 万与 7 万上方一带，位于整段上涨之前）、<b>红点标出一处高点</b>（约 9.5 万）、<b>橙点标出最高点</b>（约 9.8 万附近）、<b>粉点标出一处次高点</b>（约 9.5 万），整体为「两个低点 → 抬升 → 三个摆动高点」的结构，纵轴标注到 12 万；② 一张与前图相似的辅助图，未逐点读取。）",
      read: "改动的是他 <b>10-13「需要形成 75.5K 上方的更高低点」</b>与 <b>10-12 深夜「Simulation. Is. Real...」形态暗示</b>两条——本轮把两条合并，给出<b>可验收的启动条件</b>：① 必须在 <b>75.5K 上方</b>形成更高低点；② 最好<b>守住 80K</b>；③ 否则回调<b>可能跌破 80K</b>。同时他首次把 <b>2023 年</b>明确定义为这套示意的原型（周线 HH → 回测并尊重区间）。⚠️ 分析：① 这是本轮<b>最具体、最可验收</b>的一条——它把此前「更高低点」的抽象说法钉到了 <b>75.5K</b> 这个具体价位上；② 但 75.5K 与他 <b>10-13 给的 76–78K 下行分支</b>、<b>10 倍仓失效价 74,550</b> 几乎连成一条线，意味着：若价格真的去测 75.5K 一带，他会同时面临「更高低点是否成立」与「10 倍仓是否失效」的双重压力——<b>这两件事在同一价格带被绑死了</b>；③ 「<b>多头清算量从 20 亿降到 3 亿</b>」是他本轮新的<b>可核查观察</b>（虽为自述口径，但方向与「杠杆多头已被清得差不多」一致），他把它读成「市场不再多头主导」——这个读法本身是<b>中性偏空</b>的，却被他用于支撑「该反弹了」，属选择性解读；④ 结尾的「护盘队」暗示他认为有<b>人为托底</b>，与 10-13「市场在很努力钓人」同源，属不可证伪的解释性话语；⑤ 与同批「0.15M 前不平仓」「不该在 ATH 下方做空」相比，本条是<b>唯一给了下行价位的</b>，两套口径并存说明他的公开叙事里长期看多与短期风险同时存在。失效条件：① 硬失效——若<b>有效跌破 80K</b>，则他自己写明「回调可能把我们带到 80K 以下」，直接接入 76–78K 分支；② 结构失效——若价格不去 75.5K 一带而直接上行，则「2023 复刻」这条示意（需要回测）被跳过；③ 若他在 75.5K 一带既宣称「更高低点成立」又眼看着 74,550 被打穿，这套结构定义将自相矛盾。",
      tags: ["关键价位", "失效条件", "基准剧本"],
      src: "X 原文 @KillaXBT · 2109978457665155159"
    },
    {
      date: "2026-10-14",
      title: "反问「这图怎么看空」，核心理由是 BTC 仍在 ATH 之下",
      quote: "\"How can 1 be bearish on this chart? $BTC is still below ATH.\"（看着<b>这张图</b>，一个人<b>怎么可能看空</b>？BTC <b>仍然在历史高点下方</b>。）（配图为一张 BTC 历史走势图（未标周期，按形态为多年周线/月线级）：价格自接近 0 的极低位一路上行至约 <b>12.6 万</b>的顶部，随后回落，当前价格标记约 <b>8 万</b>附近，纵轴最高刻度 150,000。）",
      read: "改动的是他 <b>10-01「Q4 看新低是纯粹自我安慰」</b>与 <b>10-13「用 Delta 论证只需接多」</b>这一系列底部论——本条给出的是<b>最简化的版本</b>：只要价格还在 ATH 下方，长期方向就只能向上。⚠️ 分析：① 这是一条<b>循环论证</b>——「在 ATH 下方」本身既可以是看多理由（还有空间），也完全可以被读成看空理由（正在下跌、趋势可能已反转），他省略了「为什么 ATH 必然被突破」这一步；② 值得注意的是他回答的语气（反问式）而非论据式，与他 10-12 的自夸、10-14 的「记住所有空头」属同一族的<b>立场强化型</b>发言，通常出现在价格走弱、需要给跟随者定心的时点；③ 实盘对照：本条发布于 10-13 晚间（GMT+8 10-13 18:36），当时价格自 10-12 的 84,352 已回落到 82K 附近，此后进一步下探 81,033（10-13）、81,444（10-14）、80,226（10-15）——<b>发声后价格继续走低</b>。失效条件：① 该论点的隐含前提是「本周期必然重新站上并突破 ATH」；若价格长期无法回到 ATH 上方（例如 2027 年仍未突破），本条与他 10-14「2027 必创新高」的承诺一起作废；② 更近的检验——若跌破 80K 并朝 76–78K 去，则「这图怎么看空」在短期完全被现实否定。",
      tags: ["趋势切换", "周期判断", "存疑"],
      src: "X 原文 @KillaXBT · 2109956554091036875"
    },
    {
      date: "2026-10-13",
      title: "量化上方空头：87K 挂着 50 亿美元以上可见清算",
      quote: "\"We have 5B+ in visible $BTC liquidations sitting at 87K.\"（我们有 <b>50 亿美元以上</b>的 BTC <b>可见清算</b>就挂在 <b>87K</b> 上。）（配图为他贴出的一张清算地图（Liquidation Map）：图上标注 <b>累计清算区域 $5.01B</b>、当前标记价位处预计清算 <b>$2.28B</b>，交易所分布 Binance 41.8% / OKX 17% / Bybit 15% 等；图表坐标轴分辨率不足，无法独立读出这 5.01B 具体压在哪个价位的哪一段。）",
      read: "改动的是他 <b>10-12 凌晨「上方只剩 86–88K 的空头」</b>——当时只有定性判断与他自制热力图的色块；本条第一次用<b>第三方清算地图</b>把 87K 一带的空头暴露量<b>量化成 50 亿美元级</b>，把 87K 从「目标区」正式讲成<b>上方燃料池</b>。⚠️ 分析：与 10-12 凌晨的 86–88K 属同一条上行链条，但含义不同——86–88K 讲的是「谁在场」，本条讲的是「有多少钱在那儿」，为他「先冲上去扫空头、再谈回调」的口径提供了可引用的数字。需留意 <b>87K 一带同时压着他 10-05 设过、10-08 亲口判失败的周线死线</b>，也紧贴 10-06 对冲空单 89.4–90.6K 的下沿——他反复强调上方空头，等于为「冲向该区域」造势。失效条件：① 若价格上到 86–88K 却没有出现对应的挤压/清算（说明那些只是挂单而非真实可触发仓位），本条的量级判断落空；② 若他随后在该区间转为<b>做空或对冲</b>，「上方是燃料」的读法自我否定。",
      tags: ["关键价位", "目标价"],
      src: "X 原文 @KillaXBT · 2109750791049453971"
    },
    {
      date: "2026-10-13",
      title: "给 80K 划红线：丢了就看 76–78K，跌破反而加仓看 95K",
      quote: "\"There are really only 2 short term scenarios for $BTC. Either we derisk into the midterms and establish a low before, or we rally into the midterms and derisk afterwards. Let's just say bulls really don't want to lose 80K. If they do, I'm afraid we could see a deeper correction towards 76K-78K. That's not my preferred scenario, I'm looking for a larger correction from the 90Ks back into the low 80s. A move to 76K would also mean round tripping my 76K long, which I'm still holding at full size.\"（BTC 短期其实只有 <b>两种剧本</b>：要么我们在中期选举前就去风险、并在此之前先做出一个低点；要么我们<b>顶着选举往上拉</b>、选举之后再<b>去风险</b>。这么说吧，<b>多头真的不想丢掉 80K</b>。一旦丢掉，我担心会看到一次<b>更深的回调、朝 76K–78K 去</b>。这不是我偏好的情形——我本来在等的是<b>从 90K 段回调到低 80K</b>。而走到 76K 也意味着把我 <b>76K 那笔多单原路打回</b>，那笔我仍然满仓持有。）\" 后半段：\"The best case scenario for bulls from here is to start pushing higher into the midterms, break out of the range and make a new high, then see the classic post midterm derisking. For that scenario to play out, BTC needs to start bouncing soon. If BTC does dip below 80K, I'll be looking to add to my spot position, increase my longs and target a move towards 95K and beyond.\"（对多头而言最好的情形是：开始<b>顶着选举往上推</b>、<b>突破区间创出新高</b>，然后出现经典的<b>选举后去风险</b>。这个剧本要成立，<b>BTC 必须很快开始反弹</b>。而如果 BTC 真的<b>跌破 80K</b>，我会考虑<b>加现货、加多单</b>，并把目标放在<b>朝 95K 甚至更高</b>的一波上。）",
      read: "改动的是他 <b>10-11「选举后回调不会创周期新低、只做更高低点」</b>这条——本轮第一次把 <b>76–78K</b> 明确写成<b>他需要提前承认的可能性</b>，虽然同时标注为「非偏好」。⚠️ 分析：这条一次讲清两件事——① 他<b>偏好的路径仍是「先到 90K 段、再回调到低 80K」</b>，即上行为主、回调可控；② 但他第一次给「丢掉 80K」配了具体后果（76–78K），而这个区间<b>正好落在他 10-03 亲手量出的 74–77K 投降区里</b>，与 10-11「不创周期新低」的承诺存在明显张力。仓位面：首次把 <b>76K 那笔多单</b>与「被原路打回（round trip）」挂钩，等于承认该笔在 76K 一带将<b>回到盈亏平衡</b>；同时重申「跌破 80K 就加仓」，与他 10-08 已写明的「10 倍仓失效即再开第二个 10 倍」构成 <b>下行加仓叠加</b>。失效条件：① 偏好路径失效——若价格没有先去 90K 段、而是<b>直接跌破 80K</b>，则「更想看到 90K→低 80K 的回调」这条口径作废，切换为他自给的 76–78K 分支；② 承诺失效——若真走到 76–78K 而他一改常态不加仓、反而减仓，则「跌破 80K 就加」这条规则作废；③ 若 76K long 真被 round trip 打回且未按计划加仓，其「满仓」叙事需要重新核对。",
      tags: ["基准剧本", "关键价位", "仓位建议"],
      src: "X 原文 @KillaXBT · 2109689403224297605"
    },
    {
      date: "2026-10-12",
      title: "买盘必须现身：否则 80K 防御只是把人骗进区间",
      quote: "\"You want to see $BTC bulls step in here. Otherwise, we risk a more corrective move below 80K. We closed above the range, and now we're retesting its structural integrity. If price breaks back below and fails to reclaim it, that compromises the range. We don't need another sweep of the lows to find liquidity, we've already seen around $2B in liquidations. That would actually signal more weakness than strength in my eyes. What we need now is strength. Buyers have to show their hand. Otherwise, the defence of 80K may have just baited people into the range before a move towards 76-78K. This is a key area if we are going higher.\"（你会想在这里看到 BTC <b>多头现身</b>。否则我们就有风险走出一波<b>更深的回调到 80K 下方</b>。我们<b>收在区间之上</b>，现在正在回测这个区间的<b>结构完整性</b>。如果价格重新跌回区间内、并且<b>收不回来</b>，那这个区间就被破坏了。我们<b>不需要再扫一次低点</b>去找流动性——<b>大约 20 亿美元</b>的清算我们已经见过了。在我眼里，那反而会<b>更像疲弱而不是强势</b>的信号。现在需要的是强势，<b>买方必须亮出底牌</b>。否则，<b>80K 的防御</b>可能只是把人们<b>骗进区间</b>，然后再朝 <b>76–78K</b> 去。如果我们要往上走，这就是关键的价位。）（本条为回复式推文，引的是他自己 3 小时前的「82.5–81.9K 必须守住」那条；配图两张走势图标注，未逐一读取。）",
      read: "改动的是他 <b>10-12 凌晨「低杠杆多单已被打掉、上方只剩 86–88K 空头」</b>那条——当时的读法是「<b>清完杠杆就该上</b>」；本条把他自己 3 小时前的 82.5–81.9K 防守区摊开检验，并首次承认「<b>再扫一次低点反而代表更弱</b>」，等于把框架从「<b>扫针即利多</b>」下调为「<b>需要买方自证</b>」。⚠️ 分析：这是本轮少见的<b>偏空语气条</b>——他连续给出两个「非偏好」的下行参照：跌破 80K → 76–78K；并第一次说「80K 的防御可能只是诱多」。与同日凌晨 04:59 那条「上方 87K 挂着 50 亿清算」并列，他同一天里既强调上方燃料、又承认下方脆弱，属<b>双向条件式</b>表述。失效条件：① 若买方确实在该区现身、价格收回 84K 上方，「诱多」的担心解除，本条回到上行口径；② 若价格<b>跌回 82K 下方并站不住</b>，则他同日 18:00 给的「守住 82.5–81.9K」与他自己的多头剧本同时进入验证；③ 他所说「约 20 亿美元清算」为自述口径，无法独立核验，本条不作为规模依据。",
      tags: ["失效条件", "关键价位", "情绪指标"],
      src: "X 原文 @KillaXBT · 2109650303691772014"
    },
    {
      date: "2026-10-12",
      title: "用 STH 供给过热反证底部已成，并点名别信恐惧贪婪指数",
      quote: "\"Funny how STH supply reached overheated levels last cycle after breaking away from the macro bottom, just like it has this cycle. That's another sign the bottom is in. Even after reaching those levels in 2023, $BTC still continued to grind higher while respecting the HTF trend. That's exactly what we're seeing now. Don't get fooled by the Fear & Greed Index. The market can stay irrational far longer than most people expect.\"（有意思的是，上个周期 <b>STH（短期持有者）供给</b>在脱离宏观底部之后来到了<b>过热</b>水平，这个周期也是一样。<b>这是底部已经形成的又一个信号</b>。即便在 2023 年达到那些水平之后，BTC 依然<b>在尊重高周期趋势的前提下继续往上磨</b>——这正是我们现在看到的。别被<b>恐惧贪婪指数</b>骗了，市场保持非理性的时间可以比大多数人预期的长得多。）（配图为一张 STH 供给走势图，未读取。）",
      read: "改动的是他 <b>10-01「所有关键 HTF 均线指向底部已成」</b>那条底部判定——本轮第一次把 <b>STH（短期持有者）供给</b>这个链上指标纳入「底部已成」的证据链，并用 <b>2023 年同形态继续上行</b>做先例。⚠️ 分析：① 属<b>叙事加固</b>而非新增价位，与前一日「自证 USDT.D」同类；② 需注意他这里用的是 <b>2023 类比</b>——他在 09-29 曾专门写长文<b>否定 2023 分形</b>，此后 10-06、10-09、10-11 又反复把该分形摆回桌面，本条已是第 N 次引用 2023，<b>「反分形 → 用分形」的摇摆仍在继续</b>；③ 「别被恐惧贪婪指数骗」是他近期第 6 次<b>反向情绪论据</b>（前有 disbelief、讥讽空仓盼暴跌等），一贯用来为「继续持有」提供情绪层支撑。失效条件：① STH 供给口径<b>未给数值、未给来源</b>，无法独立验收，只能视作叙事；② 若此后价格<b>跌破 80K 并朝 76–78K 去</b>，则「底部已成」与「像 2023 那样继续磨高」同时被打断；③ 若他随后在下跌中改口「底部未成」，本条自证为事后叙事。",
      tags: ["链上数据", "基准剧本", "存疑"],
      src: "X 原文 @KillaXBT · 2109630168247529707"
    },
    {
      date: "2026-10-12",
      title: "自夸周一高点枢轴again：区间震荡里抓 2–3% 反向波",
      quote: "\"My $BTC monday high pivot strategy is proving itself yet again. I've been posting about this for 1.5 years straight, and it keeps playing out. It's most consistent in ranging markets, where it catches those 2-3% inverse moves. This is the result of relentless backtesting which is why you haven't seen this mentioned anywhere else before...\"（我的 BTC <b>「周一高点枢轴」策略</b>又一次自我应验了。我<b>连续 1.5 年</b>都在讲这个，它一直在兑现。它在<b>区间震荡市</b>里最稳定，能抓到那种 <b>2–3% 的反向波动</b>。这是<b>海量回测</b>的结果——也是为什么你在别处没见过有人提这个……）（配图为一张标注过的走势图，未读取。）",
      read: "改动的是他 <b>10-11「第 14 个日历枢轴」</b>模型——本条是同一套「<b>日历/日枢轴 + 反向叙事</b>」思路的<b>战绩自证版</b>，把 10-12（周一）高点 84,352 之后那波回落说成策略命中。⚠️ 分析：① 这是本轮<b>第 2 条自证类</b>发言（前有「自证 USDT.D」），与其 10-11 那条「People might call me cocky」的心态长文连起来看，属<b>连贯的信誉维护动作</b>；② 值得注意的自我设限：他明说该策略「<b>在区间震荡市里最稳定</b>」——等于承认<b>趋势行情下这套东西会失灵</b>，与他同期「底部已成、要上 90–95K」的<b>趋势级多头口径存在内部不一致</b>（若真进入趋势，按他自己的说法这套就不适用了）；③ 实盘对照：10-12 周一高点 84,352 → 10-13 低点 81,033，幅度约 <b>−3.9%</b>，比他自述的 2–3% 略大，方向一致。失效条件：① 该策略无公开规则、无公开回测，<b>不可独立验收</b>，只能看他后续是否继续宣称命中；② 若市场从区间转入单边趋势（他本人预期是向上突破），则该策略按他自述会失效，届时看他是否还继续用它解释行情；③ 本条未含任何交易价位，不构成操作依据。",
      tags: ["战绩复盘", "周期判断", "存疑"],
      src: "X 原文 @KillaXBT · 2109599968579219618"
    },
    {
      date: "2026-10-12",
      title: "周线收在前影低点上方，但 82.5–81.9K 必须守住",
      quote: "\"$BTC closed the week above the prior wick lows. If we come back down to the 82.5–81.9K region, it's vital that bulls defend this area. We don't have to retest it, but with the 14th approaching, it's definitely possible. This is the area where you want to see buyers step in and confirm that we've reclaimed the range. Anything below equals danger.\"（BTC <b>周线收在前一根影线的低点之上</b>。如果我们重新下探到 <b>82.5–81.9K 区域</b>，多头<b>守住这个区域是至关重要的</b>。我们不一定非得回测它，但<b>随着 14 号临近</b>，这完全有可能。这就是你希望看到买方现身、<b>确认我们已经收回区间</b>的位置。<b>跌破这里就等于危险。</b>）（配图为一张标注 82.5–81.9K 的走势图，未读取。）",
      read: "改动的是他 <b>10-11「本周收盘价高于上一周低点即看多」</b>——本条是那条判据的<b>兑现与落地</b>：周线确实收在前影低点上方，他随即把「看多」这个抽象条件<b>换算成一个具体防守带 82.5–81.9K</b>。⚠️ 分析：① 相比 10-10 他给的「守住 82.8K（≈10 倍仓成本线）」，本轮防守区<b>整体下移约 0.3–0.9K</b>、下沿压到 81.9K —— 这是他在维持「不预期新低」口径的同时，对下方容忍度的一次<b>小幅放宽</b>；② 本条与他同日 22:20 那条「买方必须现身、否则 80K 防御可能是诱多」<b>互相咬合</b>：先给防守带、再给它加「必须自证」的条件，属<b>事前免责式框架</b>（守住了=我说对了，守不住=我说过要买方现身）；③ 实盘对照：10-12 日低 <b>81,750</b>、10-13 日低 <b>81,033</b>，<b>两度向下穿破 81.9K</b>，其中 10-13 更低 —— 他说的「跌破这里等于危险」已被<b>触发过</b>，随后价格迅速收回 83K 上方，可视为「当天收回」而非有效跌破。失效条件：① 若日线<b>收在 81.9K 之下并连续站不回来</b>，则本条「收回区间」的确认失败，直接接入他 10-13 给的 76–78K 分支；② 若 14 号枢轴前后价格<b>没有回测该区就一路走高</b>，则本条的防守意义自然消退（他自己也说「不一定非得回测」）；③ 82.5–81.9K 若被他后续上调或下调，本条具体价位作废，须以其最新表述为准。",
      tags: ["关键价位", "失效条件", "周期判断"],
      src: "X 原文 @KillaXBT · 2109584967822921878"
    },
    {
      date: "2026-10-12",
      title: "定调：低杠杆多单已出清，上方只剩 86–88K 的空头",
      quote: "\"Seems like this move did exactly what it needed to do. Take out a bunch of low leverage $BTC longs. Now it's just shorts between 86-88K.\"（这波走势看起来正好做了它该做的事——把一批<b>低杠杆</b>的 BTC <b>多单</b>打掉。现在剩下的，就只有 <b>86–88K</b> 之间的<b>空头</b>了。）（配图为他自己的清算热力图：<b>绿色流动性簇密集分布在 86,000–88,500</b> 区间，而 <b>80,000–82,000</b> 下方的紫色/蓝色簇明显稀疏。）",
      read: "改动的是他 <b>10-09「下方没有支撑、买盘集中在低 80K」</b>与 10-10「下方流动性很少」那套——本条把「多单被打掉」从风险兑现<b>翻转成利多燃料</b>：低杠杆多头出清之后，他首次用<b>具体数字</b>把 86–88K 写成<b>仅剩的空头暴露区</b>，等于给 10-10 的「上方 EQH 买侧流动性池」钉上价位。⚠️ 分析：这条与 10-10「破 6.56% 上看 90-95K」是同一条上行链条的两段；但要留意 <b>86–88K 恰好压在他 10-06 给对冲空单的 89.4–90.6K 下方一档</b>，而 87K 又是他 10-05 设过、10-08 亲口判失败的周线死线——同一带区间被他反复赋予「<b>目标 / 失效 / 对冲</b>」三重身份，口径存在重叠。失效条件：① 价格若冲到 86–88K 后被压回、并有效跌回 <b>82.8K</b>（其 10 倍仓成本线）下方，「空头被取」的假设反转；② 若他随后开始在该区间<b>布空</b>而不是等空头被挤，「空头暴露」的读法作废。",
      tags: ["关键价位", "仓位建议", "趋势切换"],
      src: "X 原文 @KillaXBT · 2109408661609074733"
    },
    {
      date: "2026-10-12",
      title: "自证 USDT.D：宏观下行 + 首度回测 BOS，「这张图最重要」",
      quote: "\"I did say this was one of the most important charts to observe.... $BTC\"（我早就说过，这是最值得观察的图之一……）（引推是他自己 10-08 的原帖：\"Study January 2024 $BTC This is one of the most important charts to watch. USDT.D remains in a significant macro downtrend and is now making its first major retest of that BOS, the exact same playbook we saw last cycle.\" 即——研究 <b>2024 年 1 月</b>的 BTC；USDT.D 仍处在一个<b>显著的宏观下行趋势</b>中，现在正在对这个 <b>BOS（结构破位）</b>做<b>第一次重大回测</b>，与我们上一轮周期见过的剧本<b>一模一样</b>。）",
      read: "改动的是他 <b>10-09 至 10-10 的 USDT.D 双向框架</b>——本条本身不新增价位，属<b>自引式再确认</b>：他把 10-08「USDT.D 首度回测 BOS + 2024 年 1 月类比」这张图<b>重新置顶为「最重要」</b>，等于在 10-11 那根插针、约 2B 多单清算之后，公开宣告「图还没坏、剧本仍在」。⚠️ 分析：这是他自 10-06 起<b>第 5 次</b>围绕 USDT.D 发言，但**只表态、不给数字**（6.7% / 6.56% 两个关键位仍是 10-10 的旧值），属于叙事维护而非新增信息；把它与同日「上方只剩 86–88K 空头」并列看，他的多头叙事在 10-11 插针后**不降反增**。失效条件：本条的可检验点仍只有 USDT.D 的 <b>6.7% / 6.56%</b>——USDT.D 站上并站稳 <b>6.7%</b>，则「宏观下行 + 首度回测」的整条类比作废（与 10-10 那条免责推同源）。",
      tags: ["链上数据", "战绩复盘"],
      src: "X 原文 @KillaXBT · 2109326604702978153"
    },
    {
      date: "2026-10-11",
      title: "第 14 个日历枢轴将至：更希望先盘底再涨，先急涨反要谨慎",
      quote: "\"My 14th pivot is approaching next week. It's a date I've been tracking and talking about since $BTC first surpassed 100K, around a year and a half ago. The pivot has been consistent, and right now we're seeing a more bearish narrative build into it. If that continues, I'd be looking for an inverse move back upwards, as we've seen in the last 3 instances: a bullish move following a bearish narrative. For continuation, it may actually be better to see price consolidate around the lows before pushing higher after the 14th. If we start pushing up aggressively into the date, I'd be more cautious, as that could set up an inverse move back down aswell. Works both ways.\"（我的<b>第 14 个枢轴</b>下周就到。这是我自 BTC 首次突破 100K 起、大约<b>一年半</b>前就在追踪和谈论的一个日期。这个枢轴一直很稳定，而现在我们看到<b>一个更偏空的叙事正在向它聚集</b>。若这种情况延续，我会预期一次<b>向上的反向移动</b>——前 3 次就是这样：<b>看空叙事之后跟着一根上涨</b>。若要延续，更好的情形其实是价格在低点附近<b>先盘整</b>、等 14 号之后再往上推；若在到达该日期前就开始<b>猛烈上攻</b>，我反而会更谨慎，因为那也可能同样搭出一个<b>向下的反向移动</b>。两个方向都成立。）",
      read: "改动的是他 <b>10-08 首次提出的「14 号枢轴制造反向叙事行情」</b>——本轮把它从单条观察<b>升级为带序号、带历史样本的日历模型</b>（自称第 14 个枢轴、前 3 次均为「先空叙事 → 后上涨」），并首次给出<b>条件化的双向解读</b>：<b>先盘底再上</b>是他偏好的路径，<b>提前急涨</b>反而触发他的反向警报。⚠️ 分析：这是他近期少见的<b>对称表述</b>（\"Works both ways\"），可与 10-08 的 10-14 日历节点对照——下周恰好覆盖 10-14，两条可视为同一模型的不同说法。但正因双向，本条的<b>可证伪性很低</b>：涨也能对、跌也能对。失效条件：真正能推翻它的是<b>枢轴日期本身落空</b>——即下周（10-12 起那一周）过去后，市场既未按其偏好先盘底、也未出现叙事反转，枢轴计数「一年半来一直稳定」的说法就需要重新核对；此外若他在枢轴兑现后转而宣称「本次是例外」，则说明该模型已无法自我结算。",
      tags: ["周期判断", "失效条件"],
      src: "X 原文 @KillaXBT · 2109297721798447498"
    },
    {
      date: "2026-10-11",
      title: "选举剧本细化：去风险在选举之后，三笔多单满仓未动",
      quote: "\"The ideal scenario would be for $BTC to push higher into the midterms, build a bullish narrative and sweep the highs. Then, as in previous cycles, we get a corrective move after the midterms. This time though, that correction wouldn't lead to a new cycle low. It would establish a higher low instead. That feels like the most plausible scenario to me. If we dump into the midterms, I think we're more likely to pump afterwards towards 95K.\"（最理想的情形是：BTC <b>顶着中期选举往上推</b>、把看多叙事做起来、<b>扫掉高点</b>；然后像前几个周期一样，选举之后出现一次<b>回调</b>。但这次不同——那次回调<b>不会创出新的周期低点</b>，而是做出一个<b>更高低点</b>。这在我看来是最合理的情形。如果我们<b>跌进选举</b>，我反而认为之后更可能<b>拉升到 95K</b>。）\"同上，后半段：\"Nearly 2B in longs have just been liquidated, and the midterms are only 3 weeks away... it looks like shorts are more exposed than longs right now. 3/4 midterms were followed by bearish price action one to two months later. Based on that historical sample, the odds are 75%... So i think we only get the derisking after, not before the midterms. I'm still holding the 10x long, along with the longs I posted at 62.6K and 76.4K. All positions remain open at full size.\"（刚刚有近 <b>20 亿美元</b>的多头被清算，而中期选举只剩 <b>3 周</b>……就当前价格行为、情绪、以及<b>一方叙事已被打掉</b>这几点看，现在<b>空头比多头更暴露</b>。<b>4 次中期选举里有 3 次</b>都在之后一到两个月出现偏空的价格行为，按这个样本，概率是 <b>75%</b>。我不反对市场上涨，但我交易的是统计和数据，不是我希望的结果。所以我认为<b>去风险只会发生在选举之后，而不是之前</b>。我仍然持有那笔 <b>10 倍多单</b>，以及我在 <b>62.6K</b> 和 <b>76.4K</b> 发的多单。<b>所有仓位维持满仓、全部在场</b>。）",
      read: "改动的是他 <b>10-06「本季度 75% 概率出现某种形式的拒绝」</b>与 <b>10-04 首次引入的中期选举锚点</b>——本轮把两者<b>合并成一个带结构的双分支剧本</b>：① 乐观路径＝选举前上推扫高 → 选举后回调但<b>只做更高低点、不创新低</b>；② 悲观路径＝跌进选举 → <b>之后反而拉到 95K</b>。⚠️ 分析：两条路径<b>结局都指向更高</b>（更高低点 / 拉到 95K），这是一套<b>「无论怎样都偏多」的条件结构</b>——真正的空头情形（选举后创出新周期低）被他明确排除，而这正是他 10-03 亲手量出的 74–77K 投降区所在的位置，两套口径存在张力。同条还首次把 <b>75% 这个数字的来源讲清楚</b>（4 次中 3 次、选举后 1–2 个月偏空），比 10-06 只丢数字更可核查。仓位面：首次在一条推里<b>同时点名三笔多单并声明满仓未动</b>（10 倍仓 + 62.6K + 76.4K），与 10-08「10 倍仓 82.860 重开」接得上。失效条件：① 他的「更长周期不创新低」前提被打破——有效跌破 <b>74,550</b>（其 10 倍仓失效价）并触及 <b>74–77K</b> 投降区；② 时间上，<b>11-03 前后</b>若出现他所说的「选举后回调」但直接创出新周期低点，则本条的核心修正（\"wouldn't lead to a new cycle low\"）作废。",
      tags: ["宏观驱动", "基准剧本", "仓位建议"],
      src: "X 原文 @KillaXBT · 2109277589068013744"
    },
    {
      date: "2026-10-11",
      title: "放两张并排走势图：「模拟是真的」暗示形态重演（未标周期）",
      quote: "\"Simulation. Is. Real... $BTC\" / \"Would be funny if?\"（<b>模拟是真的</b>……BTC。／要是（真那样）就有意思了？）（配图为两张走势图<b>并排比对</b>：用彩色圆点标注出彼此相似的摆动结构，右侧一段呈现<b>先深跌后 V 型反转</b>的形态。他未在正文里说明这两张图分别对应哪个周期/标的。）",
      read: "改动的是他 <b>09-29 专门写长文否定 2023 分形</b>、<b>10-06 又把该分形「摆回桌面」</b>这条反复摇摆的线索——本条虽无文字结论，但配图做成<b>并排形态对照 + 彩色打点</b>，且用「would be funny if?」的反问句式，等于<b>在图上暗示当前走势正在重复某个历史结构</b>。⚠️ 分析：本条属<b>图表暗示而非明确观点</b>，两个对比周期均未标注，<b>不做任何推演</b>；其价值仅在于印证「分形重演」这条思路在他 10-11 的发言里<b>仍在活跃</b>，与他同日「更高低点、选举后回调不创新低」的乐观口径方向一致（右侧图是先跌后 V 反）。<b>按不猜测原则，本条标 存疑，不作为任何价位依据。</b>失效条件：本条无可验收内容；唯一可追的是——若他随后明确说出对比的两个时段、且实际走势与之背离，这条暗示即被他自己推翻。",
      tags: ["周期判断", "存疑"],
      src: "X 原文 @KillaXBT · 2109250113444921738"
    },
    {
      date: "2026-10-11",
      title: "长期目标首次钉死年份：160-180K 见，2029 年",
      quote: "\"I will see you at 160-180K for 1 $BTC in 2029.\"（我会在 <b>2029 年</b>、在 <b>160-180K</b> 的位置见到你——用 1 枚 BTC 来换。）（配图未读取，正文无额外数字。）",
      read: "改动的是他 <b>09-29 首次给出的「顶部区间 160K–180K」</b>——当时只给区间、不给年份；10-05 又把破 ATH 的窗口定在「2027 年 Q2–Q3」。本条首次把 <b>160-180K 与具体年份 2029 绑定</b>，等于把「本轮顶部」在时间轴上再推后约两年，与 10-08「126,000 <b>next year</b>（=2027）」形成 <b>2027 → 2029 的阶梯式目标</b>。⚠️ 分析：这是一条<b>无中间路径、无下行失效价</b>的超长周期口号式表述，不可独立验收，也不构成任何短期交易依据；「for 1 $BTC」的措辞更像把 1 枚 BTC 当长期持有凭证，而非当前仓位的止盈位。<b>需注意内部张力</b>：他在同一天凌晨刚说 82.2K 或成更高低点、上方看 90-95K，同日又抛出 2029 年的 160-180K——短/中/长三套口径彼此不冲突，但<b>越往后的目标越不具备可证伪性</b>。失效条件：本条唯一可检验的前提是「他仍相信本轮周期会长到 2029」；若他 10-03 / 10-09 亲自量出的投降区（<b>74-77K</b>，乃至「低 70K」）被实质打穿、或自家 10 倍仓失效位 <b>74,550</b> 被打穿且他转为长期看空，这条 2029 目标即自行作废。",
      tags: ["目标价", "周期判断", "存疑"],
      src: "X 原文 @KillaXBT · 2108978618361676225"
    },
    {
      date: "2026-10-10",
      title: "长头清算即局部底：区间没丢，上方 EQH 堆买侧流动性",
      quote: "\"The last time we saw a comparable wave of long liquidations on the HTF, $BTC marked a local bottom. We've now cleared out significant long leverage without losing the range. There's very little liquidity below us, while multiple EQHs are building a clear pool of buy-side liquidity above.\"（上一次我们在高周期上见到可比规模的多头清算潮时，BTC 标记了一个<b>局部底部</b>。我们现在已经清掉了大量多头杠杆，而且<b>没有丢掉区间</b>。我们下方的流动性非常少，而上方多个 <b>EQH（等高等高点）</b>正在堆积出一个明确的<b>买侧流动性池</b>。）（引推是他自己更早一条：「区间中部的顶……BTC 被夹在两个低周期流动性簇之间。若扫掉前周低点，那才是我会考虑做多的位置；若没扫掉而开始推回高点，就我个人而言不会考虑做空。月线与季线收盘临近。」）",
      read: "改动的是他 10-09 晚间「下方没有支撑、买盘集中在低 80K」那条——本轮首次把「<b>下方流动性很少</b>」从 <b>风险</b>（一旦失守下跌会很快）<b>翻转成利多论据</b>（下行杠杆已清、抛压已释放、区间未丢），并给出「上一次可比清算潮 = 局部底」的历史类比。新增关键概念：<b>上方多个 EQH 构成买侧流动性池</b>——他首次明确指认上方存在<b>可被扫的目标区</b>（EQH 常作流动性诱饵，被突破后易加速），与同日「USDT.D 破 6.56% 则上看 90-95K」互相印证。⚠️ 分析：本条是<b>自引原帖的二次确认</b>，属叙事强化而非新增信息；且引推里他自己已写明「若不扫前周低点就直接上推，我不会做空」——等于<b>空头路径被他预先排除</b>，属事后免责式框架。失效条件：① 区间失守——有效跌破 10-08 低点 <b>80,393</b> 一线，「清杠杆而没丢区间」的前提作废，「局部底」不成立；② 上方 EQH 被扫过后无法延续（冲高即回落）——则「买侧流动性池」从利多燃料改读为出货区。",
      tags: ["关键价位", "仓位建议", "情绪指标"],
      src: "X 原文 @KillaXBT · 2108944896329666811"
    },
    {
      date: "2026-10-10",
      title: "自设免责：USDT.D 若守不住，整套剧本作废",
      quote: "\"Again, this is just a schematic I am observing. We need to see USDT.D maintain below otherwise we break away from the pattern & likely do something different.\"（再说一次，这只是我在观察的一张<b>示意图</b>。我们需要看到 USDT.D <b>维持在下方</b>，否则我们就脱离了形态，大概率会走出完全不同的走势。）",
      read: "改动的是他<b>同日 21:58 刚发的</b>「USDT.D 兑现 → 82.2K 更高低点 → 破 6.56% 上看 90-95K」——本条是紧接 <b>2 分钟后</b>的免责补丁：首次明确承认整套 USDT.D 判读<b>只是一个「示意图」</b>，并把它成立的条件写成一句可验收的话——<b>USDT.D 必须维持在关键位下方</b>。⚠️ 分析：这是他自 10-06 起<b>第 4 次围绕 USDT.D 发言</b>，也是第一次主动给这套逻辑<b>装上自毁开关</b>；好处是口径变清晰（脱离形态即作废），代价是他把「<b>大概率走完全不同的走势</b>」提前写成免责，未来判断出错时可归因于「形态失效」而非判断失误。失效条件：本条本身无价位数，<b>「关键位」应读作同日给出的 6.7% / 6.56%</b> ——即 USDT.D 站上并维持在 <b>6.7% 上方</b>，本条所述的「示意形态」即作废。",
      tags: ["链上数据", "失效条件", "存疑"],
      src: "X 原文 @KillaXBT · 2108920541398843522"
    },
    {
      date: "2026-10-10",
      title: "USDT.D 兑现：82.2K 或成更高低点，破 6.56% 上看 90-95K",
      quote: "\"So far, USDT.D is playing out well. We saw the deviation followed by a retest, suggesting $BTC may have put in a higher low at 82.2K. Any sweeps into next week are worth watching. As long as dominance stays below 6.7%, a break below 6.56% will mean BTC legs upto 90-95K.\"（到目前为止，USDT.D 表现得不错。我们看到了偏离高点之后的回测，这暗示 BTC 可能已经在 <b>82.2K</b> 做出了一个<b>更高低点</b>。下周任何扫针都值得关注。只要市占率维持在 <b>6.7%</b> 下方，跌破 <b>6.56%</b> 就意味着 BTC 有望<b>上攻至 90-95K</b>。）（引推是他 10-09 的 USDT.D 双向框架原帖。）",
      read: "改动的是他 10-09「USDT.D 关键位 <b>6.57%</b>，破位则冲 <b>87K</b>」——本轮一次性做了三处调整：数字更新为 <b>6.7%（上沿）/ 6.56%（下沿）</b>；把「更高低点」<b>首次落到具体价格 82.2K</b>；上行目标从 87K <b>上调到 90-95K</b>。⚠️ 分析：三处调整<b>方向一致地偏向乐观</b>——① 上沿容忍度从 6.57% 抬到 6.7%（对空方更宽容）；② 触发位从 6.57% 微调到 6.56%（更容易被触发）；③ 目标从 87K 提到 90-95K。属典型的「条件放宽 + 目标上移」。需要盯住的一处自相咬合：<b>90-95K 与他 10-09 长文里「92-95K 才是更有意义、更广泛回调的发生区」高度重叠</b>——同一区间既是他的上限目标、又是他预期的回调区。核验（Binance 实测）：10-10 日低 <b>82,545.82</b>、10-11 迄今低 <b>82,804.65</b>，与他说 82.2K 相差约 300-600 美元（口径可能来自其他交易所或不同周期，未构成夸报）。失效条件：若 USDT.D <b>站上并维持 6.7% 上方</b>（或收复前高），则本条「更高低点 + 90-95K」直接作废，回到他 10-09 的 <b>76-78K</b>、乃至「低 70K」分支——而 76-78K 已贴近其 10 倍仓失效线 <b>74,550</b>。",
      tags: ["链上数据", "目标价", "关键价位"],
      src: "X 原文 @KillaXBT · 2108920202687840278"
    },
    {
      date: "2026-10-10",
      title: "讥讽场外者盼「双十暴跌」：又一笔情绪采样",
      quote: "\"Ironic that it's 10/10 today, yet people are hoping for a 10/10 dip simply because they're sidelined. What if...nvm.\"（讽刺的是今天是 10/10，人们却因为自己<b>空仓在场外</b>而盼着一次「10/10 式的暴跌」。要是……算了。）",
      read: "不改变任何价位判断，属他自 09-25 以来的<b>第 5 次反向情绪采样</b>。改动的是他 10-09「等再低 2-3% 的人全被抢跑」那条叙事的<b>情绪对象</b>：从「等 70K 的人」换成「因空仓而盼跌的人」，逻辑仍是同一套——<b>盼跌的声音来自场外，说明筹码在多头手里</b>。⚠️ 分析：内容很薄（无价位、无指标），只能当<b>情绪面记录</b>，不能当交易依据；「What if...nvm」是被他主动掐掉的半句，按不猜测原则不做补全。失效条件：本条无失效条件（纯态度条），证据强度<b>存疑级</b>，仅用于观察他的情绪面是否持续亢奋。",
      tags: ["情绪指标", "存疑"],
      src: "X 原文 @KillaXBT · 2108864540817424779"
    },
    {
      date: "2026-10-10",
      title: "周线验收标准下调：收盘高于前周低点即算看多",
      quote: "\"Lets keep it simple. If the current weekly candle can close above the previous weekly low, that seems pretty bullish to me. If anything, it would look like a typical stop hunt below the lows before accepting back into the range... $BTC\"（说简单点。如果当前这根<b>周线能收在上一周低点之上</b>，在我看来就相当看多了。如果非要说什么，那看起来像是一次典型的前低下方<b>止损猎杀</b>，之后重新被区间接受…… $BTC）（配图未读取。）",
      read: "改动的是他 <b>10-05 定下的「本周周线必须突破 87K」死线</b>——该死线在 10-08 已被他自己判为失败（\"failed to break 87K yet again\"），本条把验收标准<b>大幅放宽</b>：不再要求站上 87K，只要<b>本周收盘价高于上一周低点</b>即算看多。⚠️ 分析：这是他连续第二轮为同一根周线下调门槛，属典型的「死线软化」；同时首次把「跌破前低」<b>预定义为止损猎杀（stop hunt）而非趋势转弱</b>——与他 10-06「大级别启动前必先插一根清算插针」的定律、10-09「偏离高点后回归区间」的解释框架同源，等于为「再扫一次低点」提前买好了故事。失效条件：若本周（10-12 前结算）收盘价<b>低于上一周低点</b>，本条看多判据直接反向，并会与他 10-09「无法收复 84-85K 则下看 <b>76-78K</b>」串联成下行链条。核验（Binance 实测）：本周（10-05 起）已刷出低点 <b>80,393.56</b>（10-08），10-11 最新价约 <b>83,200</b>。",
      tags: ["周期判断", "关键价位", "失效条件"],
      src: "X 原文 @KillaXBT · 2108833022275383709"
    },
    {
      date: "2026-10-10",
      title: "低80K区接盘密集，称市场下方几乎无支撑",
      quote: "\"Buyers are clearly stepping in on this move down. We saw something very similar during the previous range as well. There appears to be very little support beneath current price, which suggests a high concentration of bids and conviction around the low 80Ks, most likely reinforced by it being a key psychological level for $BTC. Interesting times.\"（买家显然正在这波下跌中进场。我们在上一个震荡区间也见过非常相似的情况。当前价格下方似乎几乎没有支撑，这说明买盘和高信念仓位高度集中在<b>低 80K 区域</b>，很可能还因为那里是 BTC 的关键心理关口而被强化。有意思的时期。）",
      read: "改成的是他 10-08「这里该开始接货／别被羊群吓退」那条的<b>论据</b>——从喊口号升级为盘口结构描述：他不是说「80K 是价值区」，而是说「下方没有支撑＝买盘全都堆在低 80K」。⚠️ 分析：这是一句<b>无价位、无新点位</b>的定性判断，且逻辑上是「双刃」——「下方无支撑」同时也可以读成「一旦低 80K 失守，下跌会很快」（这正是他 10-09 自己写的「无法突破就下看 76-78K」的前提）。所以本条不能单独当看多证据，只能当<b>他指出买盘挂单集中区在低 80K</b> 这一事实记录。配图（一张低 80K 区间走势图）已读取，仅重复文本含义，无额外数字。失效条件：价价格有效跌破低 80K（约 80,000–80,500）并加速下行，则「买盘高度集中于此、下方无支撑」的整个表述反转为利空证据；反之若他在此逐步加仓，则本条即为其加仓前的口径铺垫。",
      tags: ["关键价位", "仓位建议", "情绪指标"],
      src: "X 原文 @KillaXBT · 2108620452335632385"
    },
    {
      date: "2026-10-10",
      title: "距中期选举24天，给出选举前后两套互斥剧本",
      quote: "\"We are now 24 days away from the midterms. Historically, $BTC has reacted negatively afterwards in 3/4 instances. My view therefore remains unchanged: any meaningful de-risking is more likely to begin after the midterms rather than before them. I do not expect a new bear market low. However, I do expect a higher low to form after the midterms, potentially an important established low before the next leg towards new highs. There are two main scenarios I'm observing: 1.) BTC pumps into the midterms, followed by a 10%+ correction afterwards. 2.) BTC sells off into the midterms, then begins trending higher shortly after.\"（我们现在距中期选举还有 24 天。历史上，BTC 在选举之后有 3/4 次是负面反应。所以我的看法不变：任何有意义的<b>去风险更可能发生在选举之后</b>，而不是之前。我不预期出现新的熊市低点。但我确实预期选举后会形成一个<b>更高的低点</b>，那可能是在奔赴新高之前一个重要的确立低点。我目前在观察两个主要情形：1.) BTC 在选举前上涨，选举后出现 10%+ 的回调；2.) BTC 在选举前下跌，随后不久开始走高。）（引推是他自己更早一条：「如果 BTC 就一直涨到中期选举呢？每个中期选举周期我们都看到 BTC 在选举之后表现负面。所以为什么不等到中期选举真正临近时再对价格行动做出反应。至少，这就是我在做的。」）",
      read: "改成的是他 10-04 首次提出的「中期选举」锚点——把它从「一句宏观背景」升级为<b>带两套互斥剧本的前瞻框架</b>，并给出<b>「选举后见更高低点」这一可验收的时间与形态双重判据</b>（「higher low after the midterms」是他首次把形态词与日历事件绑死）。⚠️ 分析：两套剧本<b>互相覆盖了所有方向</b>（涨也对他有用、跌也对他有用），属典型的事后免责式框架，本身不构成方向证据；但他明确的、不可改口的锚点是「<b>不预期新熊市低点</b>」+「<b>选举后更可能去风险</b>」两句。配图（4 张历史周期图 + 选举日竖线）已读取，<b>视觉上确实呈现 3/4 次选举后回落</b>，与全文数字自洽。失效条件：① 若在<b>选举之前</b>就出现大规模去风险（如跌破 76-78K 并加速），则「去风险更可能在选举之后」的时间判断失效；② 若选举后形成的不是「更高低点」而是创出<b>新低</b>，则「不预期新熊市低点」与「higher low」同时失效。",
      tags: ["宏观驱动", "周期判断", "关键价位"],
      src: "X 原文 @KillaXBT · 2108593070065209423"
    },
    {
      date: "2026-10-09",
      title: "用USDT.D定生死：企稳则筑更高低点冲90K，破位则回低70K",
      quote: "\"It is extremely important that... if we are following the 2023 fractal, USDT.D now shows acceptance back within the range on the LTFs after deviating above the highs. Right now, USDT.D has also deviated above its highs, similar to what we saw in 2023, and is now pushing back up for a retest. If this retest forms a lower high, it would strongly suggest USDT.D is continuing its macro downtrend. That would support the idea that BTC is forming a higher low here before expanding towards 90K. What we do not want to see is USDT.D reclaiming those highs and holding above them with no sign of rejection. If that happens, it would suggest BTC is likely headed back towards the low 70Ks. These are the key levels to watch now in determining whether this low is truly in... or not.\"（极其重要的一点……如果我们遵循 2023 分形，USDT.D 在低周期上<b>偏离高点后已回归区间内并获接受</b>。现在 USDT.D 也已偏离其高点，与 2023 年所见相似，并正反弹回来做一次回测。如果这次回测形成<b>更低的高点</b>，就强烈暗示 USDT.D 在延续其宏观下行趋势。那将支持「BTC 正在此处筑<b>更高低点</b>、随后向 90K 扩张」的思路。我们不希望看到的是 USDT.D <b>重新站上那些高点并站稳、毫无拒绝迹象</b>。若发生那种情况，就暗示 BTC 很可能下探<b>低 70K</b>。这些就是当下判断这个低点是否真正成立的关键位。）（同日 22:17 他另发一条更正：原文第一行把 USDT.D 误写成 BTC，实为「USDT.D 在低周期上回归区间」——即本条的指标主体全为 USDT.D。）",
      read: "改成的是他 10-08「Study January 2024／USDT.D 处于宏观下行趋势」这条<b>只给类比、不给数值</b>的模糊论证——本轮首次把 USDT.D 变成<b>带双向触发条件的可验收判据</b>：看多触发 = USDT.D 回测形成更低高点（继续宏观下行）→ 支持 BTC 筑更高低点冲 <b>90K</b>；看空触发 = USDT.D 收复前高并站稳 → BTC 回<b>低 70K</b>。⚠️ 分析：这是他自 10-06 起<b>第 3 次围绕 USDT.D 发言</b>（10-08 上午首提、下午补 6.57% 关键位、本条给双向框架），说明这是他现在主打的分析抓手；但全文<b>只给形态、不给 USDT.D 具体数值</b>（6.57% 在另一条），故仍属「有条件、不可独立验收」的判据。注意本条同时把他 10-09 早间「无法突破 84-85K 则下看 76-78K」与「低 70K」串成了一条<b>下行升级链条</b>。失效条件：① 若 USDT.D 收复前高并站稳（看空触发兑现），则「BTC 筑更高低点冲 90K」作废，且他 10-09 早间的 76-78K 会进一步下修到低 70K；② 反之若 USDT.D 的 6.57% 被跌破（见同日另一条），则本条的看空分支被排除，利多分支激活。",
      tags: ["链上数据", "周期判断", "关键价位"],
      src: "X 原文 @KillaXBT · 2108557868890779936"
    },
    {
      date: "2026-10-09",
      title: "USDT.D关键位6.57%：不破则10倍多单继续持有",
      quote: "\"This is one of the most important charts to watch. USDT.D has respected its HTF macro downtrend, rejecting in a very similar fashion to what we saw in 2023. The first key point of interest sits at 6.57%. If USDT.D bounces from there, $BTC will likely see a short term LTF rejection. However, if USDT.D breaks below this level, it would confirm that the recent move was simply a bearish retest, opening the door for BTC to reclaim and push above $87K. Until 6.57% breaks, we are not fully out of the woods. But so far, so good. The 10x long lives.\"（这是最值得看的图表之一。USDT.D 一直尊重其高周期宏观下行趋势，拒绝的方式与我们 2023 年所见非常相似。第一个关键关注位在 <b>6.57%</b>。如果 USDT.D 从那里反弹，BTC 可能会看到一次短期低周期拒绝。但如果 USDT.D 跌破该位，就确认最近这波只是<b>一次看跌回测</b>，为 BTC 重新收复并推上 <b>$87K</b> 打开大门。在 6.57% 被跌破之前，我们还没有完全脱离险境。但到目前为止，还不错。<b>10 倍多单继续活着。</b>）（引推为他 10-08 的「Study January 2024」原帖。）",
      read: "改成的是他 10-07 开的那笔 <b>82.860 的 10 倍多单</b>的处境定性——首次给出这笔仓位的<b>外部（非价格）失效判据</b>：不看 BTC 价，改看 <b>USDT.D 的 6.57%</b>。⚠️ 分析：这解决了此前一个矛盾——10-09 早间他刚说「无法突破就下看 76-78K」，若跌到 76-78K 则 74,550 的失效线近在咫尺；本条等于给这笔 10 倍仓<b>加了一层他自认更灵敏的前置指标</b>，把「BTC 价格止损」部分替换为「USDT.D 跌破 6.57% 才真正开门」。同时「<b>The 10x long lives</b>」是他对该仓位<b>首次公开强调仍持有</b>（此前多轮只提 62.6K/76.4K，未明确 10 倍仓是否还在）。失效条件：USDT.D <b>跌破 6.57%</b>即触发利多（BTC 可冲 87K）；反之 USDT.D 从 6.57% 反弹并站稳，则他会预期 BTC 出现短期低周期拒绝，并很可能按 10-09 早间的预案把目标下调至 76-78K——即这笔 10 倍仓的 BU 价 74,550 将首次进入真实施压区。",
      tags: ["链上数据", "关键价位", "仓位建议"],
      src: "X 原文 @KillaXBT · 2108526625612558560"
    },
    {
      date: "2026-10-09",
      title: "承认低周期结构转弱：先站回84-85K否则下看76-78K",
      quote: "\"I may be bullish, but I'm not oblivious to the current LTF market structure. $BTC is now coming back into the previous May range high, an area it broke back below. If this isn't simply deviation above the highs, followed by acceptance back into the range and a move lower, then we need to see a reclaim fairly quickly. Ideally, BTC pushes back above the 84-85K region, then retests and respects the previous range lows around 82.8K. If that happens, the structure is back in place for us to trend higher. On the other hand, if we cannot break this barrier... then we can push to 76-78K. Relatively straightforward.\"（我可能看多，但我并非无视当前的<b>低周期市场结构</b>。BTC 现在正回到此前 5 月区间的高点，一个它刚跌破回去的区域。如果这不只是「偏离高点后回归区间并走低」的假动作，那我们就需要看到<b>相当快地重新收复</b>。理想情况是 BTC 推回 <b>84-85K 区域</b>之上，然后回测并尊重前区间低点约 <b>82.8K</b>。若如此，结构就重新就位，可以继续走高。另一方面，若我们无法突破这道屏障……那我们就可能推向 <b>76-78K</b>。相对直白。）",
      read: "改成的是他 10-08 那条「牛市中的 FUD 只会变成上涨燃料」的<b>单边乐观口径</b>——本条首次公开承认<b>低周期结构已经转弱</b>，并给出明确的双向路径与价位：乐观路径 = 收复 <b>84-85K</b> 并守住 <b>82.8K</b>；悲观路径 = 无法突破则下看 <b>76-78K</b>。⚠️ 分析：这是他自 10-08 以来<b>首次为由多转空预留价位</b>，且 76-78K 与他 10-03 提的「74-77K 投降底」、10-07 的 10 倍仓失效价 74,550 形成下拉链条，实际等于把「下行目标」与「自家仓位风险区」并到了同一个价格带。同时 82.8K 这个「前区间低点」与他自己 82.860 的 10 倍进场价几乎重合——<b>他要守住的结构位就是他自己的成本线</b>，两者已被绑死。失效条件：① 若 BTC 无法收复 84-85K 且跌破 82.8K，则本条悲观分支激活（下看 76-78K），并直接威胁其 10 倍仓 74,550 的失效线；② 若 BTC 快速收复 84-85K 并回踩 82.8K 成功，则结构修复、继续维持其看多主线。",
      tags: ["周期判断", "关键价位", "失效条件"],
      src: "X 原文 @KillaXBT · 2108474403474252110"
    },
    {
      date: "2026-10-09",
      title: "首次量化本轮最大回撤约14%：87K到75K，70K或永不再来",
      quote: "\"A lot of people are posting previous cycle corrections as though Bitcoin is guaranteed to mirror them perfectly. That is a big mistake… We have retraced roughly 50% of the entire bear market decline, something we have never seen before. Add in the largest short-liquidation event from 62K to 80K, and the context is completely different. You cannot compare cycles that saw 77-80% drawdowns and then expect the same depth of corrections now. We bottomed around -54%. … In 2023, BTC dropped 77%. During the recovery from 16K to 69K, the deepest correction was roughly 21%. This cycle, BTC only dropped 54%, around one third less severe. Applying that same logic, a 21% correction reduced by one-third would put the largest pullback closer to 14%. A 14% drop from the 87K highs puts $BTC almost precisely at 75K. And thats if we get the full blown corrrection from 87K. It could be from 95K down to 80K. It's to soon to say. … Are you really willing to miss a potential 60% move higher because you are waiting for an extra 6% lower? I wouldn't be. Larger capital clearly isn't either. I still believe the 92-95K region is where we could see a more meaningful, broader correction, but it may simply take time to get there. For those still waiting on 70K: based on the maths, the context, and the way this cycle has behaved, there is a real chance we never see it again. Even another test of 75K would be a gift. … This is Wall Street's asset now.\"（很多人把历史周期的回调拿来发帖，好像比特币就一定会完美复制它们。这是个巨大的错误……我们已经收复了整个熊市跌幅的大约 50%，这是我们从未见过的。再加上 62K 到 80K 那次史上最大的空头清算事件，语境完全不同。你不能拿那些曾出现 77-80% 跌幅的周期来比较，然后指望现在的回调深度一样。我们的底部大约只跌了 -54%……2023 年 BTC 跌了 77%，而在 16K 涨到 69K 的复苏过程中，最深的一次回调大约是 21%。本轮 BTC 只跌了 54%，严重程度大约少了三分之一。套用同样逻辑，把 21% 的回调减少三分之一，最大回撤会更接近 14%。从 87K 高点跌 14%，BTC 几乎正好落在 75K。而这还是假设我们从 87K 就展开完整回调。也可能从 95K 跌到 80K，现在说还太早……你真的愿意为了多等 6% 的下跌，而错过潜在 60% 的上涨吗？我不会。大资金显然也不会。我仍然认为 92-95K 区域才是我们可能看到一次更有意义、更广泛回调的地方，但走到那里可能只是需要时间。对于那些还在等 70K 的人：基于这套数学、语境和本轮周期的表现方式，我们真的有再也不会见到它的可能。就算再测一次 75K，那也算是一份礼物……现在这是华尔街的资产了。）"
,
      read: "这条一次性改动了他<b>三条既有判断</b>：① 把 10-03 那句含糊的「Q4 若真投降会加更多多单」量化成<b>本轮最大回撤≈14%</b>（87K→约 75K），并首次把「一次更有意义、更广泛的回调」的<b>发生区上移到 92-95K</b>——这等于把 10-05/10-06「年内上限压到 95K 下方、余下时间区间震荡」改写成「先上到 92-95K，再谈更大回调」，口径由守转攻；② 「等 70K 的人可能永远等不到」「再测 75K 都算礼物」——这句对他在 10-07 亲手写的 10 倍仓失效价 <b>74.550</b> 构成暗示：他认为那根线不该被碰到；③ 首次把「<b>这是华尔街的资产</b>」当成结构性论据，用来解释为什么回调应该更浅（此前 10-04 只提过「机构垂直吸筹」）。⚠️ 分析：14% 那步算式本身可复核（87,000×0.86≈74,820，与他 74.550 的失效位几乎重合，属自洽）；但「已收复熊市跌幅 50%」与「底部 -54%」两个数字仍无法与 87K 独立对齐（10-07 已标注同一问题），属不可独立验证的自述口径。另注意他此处<b>自己在用历史分形做线性外推</b>（2023 的 21% 回调减三分之一），而他在 10-06 曾专门否定别人用 2023 分形——属同一手法的双标使用。失效条件：① <b>数学失效</b>——若自 87K 的回撤超过 14%（即跌破约 74,800），或「95K→80K」那条路径实际演变成「87K→70K 下方」，「比上一轮浅三分之一」整套推演作废；② <b>硬位失效</b>——74,550（他自家 10 倍仓维持保证金失效位）被打穿，则「75K 是礼物／70K 见不到」同时失效，并触发他 10-07 写明的「失效即再开第二个 10 倍」加仓规则。",
      tags: ["周期判断", "目标价", "失效条件"],
      src: "X 原文 @KillaXBT · 2108302262401376433"
    },
    {
      date: "2026-10-09",
      title: "发布8分半视频版「计划·情形·预期」并置顶",
      quote: "\"Update for $BTC — Plans, scenarios, expecations.\"（BTC 更新——计划、情形、预期。原文拼写即为 expecations。）推文本身只带一段时长约 517.6 秒（8 分 38 秒）的自制视频，并引用了他自己早前那条同样是视频的 \"Current outlook for $BTC.\"。<b>视频与引推内容本轮均无法转写</b>，按「不猜测」原则不作任何转述。",
      read: "改动的是他对外沟通的<b>形式</b>而非方向判断——他把此前零散、逐条发出的表态收束成一条<b>置顶的完整视频更新</b>（计划／情形／预期三件套），发布后约 1 小时又用一条长文（见同日「14% 回撤」那条）补上了其中的回撤幅度部分。分析：置顶意味着这是他现在的主页门面，8 分半的体量说明这是一次系统性表态；但他<b>没有在正文里给任何数字</b>，因此本条不能当作点位或方向依据，可用信息仅是「他放出了一份完整剧本更新」这一事实。⚠️ 本条已标 <b>存疑</b>：存疑的是「视频内容」而非来源，来源是一手原推。失效条件：本条不含可验收的价位或方向；唯一风险是把「发布长视频」误读成看多或看空信号——它两者都不是。建议直接在 X 上观看该视频核对。",
      tags: ["基准剧本", "存疑"],
      src: "X 原文 @KillaXBT · 2108286922283987415"
    },
    {
      date: "2026-10-09",
      title: "立场自白：赢家常是黑羊，人人都同意就没有优势",
      quote: "\"To win in a game where 90% fail, you are often the black sheep. You have to be prepared to be misunderstood. If everyone agreed with what I do, there's a good chance my edge wouldn't exist.\"（在一个 90% 的人都会输的游戏里，想赢你往往得当那只黑羊。你得准备好被误解。如果所有人都认同我做的事，那我的优势很可能根本不存在。）",
      read: "纯立场自白，<b>无点位、无方向</b>；改动的不是判断，而是为前一日「这里该开始接货／别被羊群吓退」（10-08 凌晨）提供<b>自我解释</b>——把「与大众共识相反」本身当成 edge 的论据。⚠️ 分析：这类表述的实际作用是把「被市场证伪」预先重新定义为「黑羊的正常处境」，属<b>不可证伪</b>的话术，不应计入任何方向性证据，仅可作为情绪取样（这是他近期第 N 次围绕「羊群／共识」发言）。失效条件：本条不含价位；可观察的反向信号是——若他此后开始强调「我和大多数人看法一致」，这套「逆共识」自我定位即被自己放弃。",
      tags: ["情绪指标", "基准剧本"],
      src: "X 原文 @KillaXBT · 2108271148207346081"
    },
    {
      date: "2026-10-09",
      title: "驳「78K 崩盘」预测：牛市中的 FUD 只会变成上涨燃料",
      quote: "\"Not like we haven't seen before. More $BTC FUD, right in the middle of a bull market. What have I said repeatedly? FUD during a bullish macro trend ultimately becomes fuel for higher prices on the HTFs. And once again, the fear is building while the macro structure remains firmly bullish. Oh well. Some people never learn. I will let them be. Time will prove who is right.\"（又不是没见过。牛市正中间，又来了更多 BTC 的 FUD。我反复说过什么？宏观多头趋势里的 FUD，最终会变成更高周期上涨的燃料。又一次，恐惧在累积，而宏观结构依然坚定看多。算了，有些人永远学不会，随他们去。时间会证明谁对。）所引推文内容为：\"BREAKING: US Government just transferred out $1B worth of Bitcoin / Our traders forecast $BTC will crash to $78,000 this month\"（突发：美国政府刚转出价值 10 亿美元的比特币／我们的交易员预测 BTC 本月将崩至 78,000。）",
      read: "改动的是他处理<b>具体利空信息</b>的口径——把「美国政府转出 10 亿美元 BTC + 某机构预测本月崩到 78,000」这类可验证的利空，整体归类为「牛市中的 FUD」，并重申 FUD 是 HTF 上涨燃料（与 09-26 同源的又一次复述）。⚠️ 关键分析：他<b>没有逐条回应 78,000 这个数字</b>，而是用「宏观结构依然坚定看多」直接压过去；而按他本人 10-03 给的投降底 74–77K、以及同日长文给的「87K 回撤 14%≈75K」，<b>78K 恰好落在他自己认可的回撤区间内</b>——也就是说他反驳的是「崩盘」这个定性，而不是 78K 这个价位，两者并不矛盾。失效条件：① <b>实质失效</b>——若 10 月内价格真的下探 78K 并继续走低（跌破约 74,800），「FUD 会自动变成燃料」在本轮被实测打脸；② 更弱的失效是 FUD 之后价格长期横盘不涨（燃料未点火）。",
      tags: ["情绪指标", "宏观驱动", "失效条件"],
      src: "X 原文 @KillaXBT · 2108229866726269230"
    },
    {
      date: "2026-10-08",
      title: "首次把 USDT 市占率破位回踩纳入判断依据",
      quote: "\"Study January 2024 $BTC. This is one of the most important charts to watch. USDT.D remains in a significant macro downtrend and is now making its first major retest of that BOS, the exact same playbook we saw last cycle.\"（研究一下 2024 年 1 月。这是最值得看的图表之一。USDT.D（USDT 市占率）仍处在显著的宏观下行趋势中，现在正在进行对该破位（BOS，结构破坏）的第一次重要回踩——和上一轮周期我们看到的剧本一模一样。）",
      read: "这是<b>本轮首次出现的新分析维度</b>——此前 feed 里从未有过他用稳定币市占率作论据的记录。他用「USDT.D 宏观下行 + 破位后首次回踩」类比 2023–2024 年初，隐含结论是资金将从稳定币流向加密资产。改动的是他论证的<b>证据类型</b>：从纯价格结构／情绪，扩展到<b>资金面指标</b>。⚠️ 分析：他<b>只给了类比、没给任何数值</b>（未说 USDT.D 当前水平、也未给回踩目标位），因此这条<b>不可独立验收</b>，只能当作他的定性倾向记录；另外他此处用的又是历史分形类比（2024 年 1 月），与他在 10-06 专门否定别人用分形的态度存在张力。失效条件：USDT.D 若在该破位位止跌回升（稳定币市占率重回上行），「资金流向加密」这条资金面论据即作废；对价格的方向性判断仍以 10-03 的 97K／74–77K 与 10-09 的「14%≈75K」为准，本条不提供独立价位。",
      tags: ["链上数据", "周期判断"],
      src: "X 原文 @KillaXBT · 2108224103333216707"
    },
    {
      date: "2026-10-08",
      title: "复盘空头：从67K一路空到87K的人，现在为小回撤欢呼",
      quote: "\"The same people who shorted $BTC all the way from 67K to 87K are now celebrating because the price is finally seeing a small correction. They convince themselves they're just looking for a bullish retest, but deep down, all they really want is to make back everything they lost in one trade. And the irony is that their inability to control their own greed is exactly what got them fucked in the first place. They haven't learned a damn thing. And that's exactly why the same shit will happen again.\"（那些从 67K 一路空到 87K 的人，现在因为价格终于出现小回撤而在庆祝。他们说服自己只是在等一个看涨回踩，但内心深处，他们真正想要的是一笔单子把亏掉的全部赚回来。而讽刺的是，他们控制不住自己的贪婪，正是一开始把他们搞死的原因。他们什么都没学到。这也正是同样的破事会再次发生的原因。）",
      read: "改动的是他对<b>对手盘结构</b>的描述——把当前这波回撤的卖方定性为「在 67K→87K 全程做空、急需一笔单子回本的亏损者」，等于宣告 80K 一带的抛压来自<b>急于回本的高杠杆空头</b>而不是趋势资金。这条与同日凌晨那条「这里该开始接货／别被羊群吓退」构成一组：凌晨先给建议，晚间再定义对手是谁，为「与对手反向操作」补上叙事。⚠️ 分析：这是他 10-04「踏空者被抢跑」的升级版——从嘲笑观望者转为嘲笑做空者，语气更硬，但<b>无任何新增点位或方向改动</b>，属情绪层条目。失效条件：若价格继续下破（失守 10-08 日低 80,393 并走向 75K），「抛压来自需要回本的空头、他们会被挤」这套叙事将失去解释力——持续创新低通常意味着更强的现货卖压，而非空头回补。",
      tags: ["情绪指标", "战绩复盘"],
      src: "X 原文 @KillaXBT · 2108164103097213373"
    },
    {
      date: "2026-10-08",
      title: "首次把当前价位定性为「挂单接货区」：别被羊群吓退",
      quote: "This is where you start bidding, anon. But let the herd scare you into believing otherwise. In due time, I’ll see you on the other side, just like every single time before.（匿名者，这里就是你该开始挂单接货的地方。但就让羊群吓你、让你相信相反的事吧。时候到了，我会像之前每一次那样，在对岸见你。）随推附一张图，图内内容未读取，未作转述。",
      read: "改动的是他 10-07 深夜那笔 82.86K 的 10 倍多单的<b>性质</b>——2 小时前那只是一笔个人交易（entry 82.860），这条第一次把它升格为面向所有人的<b>公开挂单建议</b>：这里是「开始接货」的位置。它同时把 10-05「82.5K 是决策线」和 10-07「80–82K 是我要重建 10 倍仓的区间」两条收束成一句话——他不再等 80–82K 的下沿，而是把当前 82.8K 附近直接当成建仓区。⚠️ 分析：正文<b>没有给出任何具体价位</b>，「这里」究竟指 82.8K 还是 82.2K 无法从文本独立确认（配图未读取），故这条只能作为<b>口径</b>而非点位引用；另注意按 10-08 实际盘面，日低已到 82,227、现价约 82,9xx，他的挂单区已被向下穿过一次。失效条件：与他自己的 82.5K 绑定——若 82.5K 被有效失守并向 80–82K 甚至 74–77K 延伸，「这里该开始接货」就变成接刀；反向的验证是价格不再探 80–82K 而直接从 82.8K 一线起涨，则这条升格成立。",
      tags: ["仓位建议", "关键价位", "情绪指标"],
      src: "X 原文 @KillaXBT · 2108049404863074707"
    },
    {
      date: "2026-10-08",
      title: "纯图卡片：先掌握耐心，才谈得上掌握交易",
      quote: "纯图片推文，正文为空；图内文字为：To master the art of trading, you must first master the art of patience.（要掌握交易这门艺术，你必须先掌握耐心这门艺术。）",
      read: "纯励志卡片，<b>无点位、无新增条件</b>。作用是把 6 小时前那条「this is LTF chop & I am a HTF trader（这是低周期噪音，我是高周期交易者）」的立场再确认一次，属情绪层表述而非市场判断。这条也是本次扫描中唯一一条没有文字的推文（其余抓取到的均已取到正文）。无失效条件（本条不含任何价位）。",
      tags: ["情绪指标"],
      src: "X 原文 @KillaXBT · 2108041077017968925"
    },
    {
      date: "2026-10-08",
      title: "首次给出日历反指节点 10-14：叙事往哪走就打反向",
      quote: "October 14th is the date to watch for $BTC My 14th pivots have been producing inverse narrative moves. We saw the same setup around 75K before the move into 87K, a move I was long on. If a bearish narrative develops into October 14th, I will be looking for the inverse: a move higher. If bullish sentiment takes over into that date, then I would anticipate the opposite, a potential bearish move.（10 月 14 日是 BTC 要盯的日期。我的 14 号枢轴一直在制造反向的叙事行情。75K 附近我们见过同样的设置，之后就是涨向 87K 那一波——那波我做多了。如果到 10 月 14 日之前发展出看空叙事，我就找它的反面：向上。如果到那天看多情绪占了上风，那我预期相反的方向，可能是一波下跌。）随推附一张图，图内内容未读取，未作转述。",
      read: "改动的是 09-26「月度开盘枢轴、跌进月开历史偏多」那套<b>季节性反指</b>的颗粒度——他把笼统的「月开附近」换成<b>具体的日历日 10-14</b>，并明确规则是<b>情绪反指</b>：看空叙事 → 看涨，看多情绪 → 看跌。这是他第一次把方向的决定权完全交给「届时的市场叙事」而不是价位，与 10-04「中期选举后走弱」、10-07「人们想要更低价」属同一套逆向框架。⚠️ 注意性质：这是<b>条件式表述而非单向预测</b>——他没说 10-14 会涨或会跌，只说会反向，因此它不能被当成看多信号使用；且他自述该模式在 75K 附近兑现过，属战绩复盘口径。失效条件：到 10-14 时情绪没有形成明确单边（既不成看空叙事、也无看多情绪）→ 反指无从取用；更硬的失效是<b>叙事与走势同向</b>（看空叙事下继续下跌），届时「14 号枢轴反指」这套用法本轮作废。",
      tags: ["周期判断", "情绪指标", "失效条件"],
      src: "X 原文 @KillaXBT · 2107923667061772539"
    },
    {
      date: "2026-10-08",
      title: "自认改计划：不等 80–82K，提前 0.75% 就重新上 10 倍多",
      quote: "Plans change. That is trading. Initially, I was prepared to sit out and wait for the 80-82K area. However, seeing sentiment completely fall apart while we are still holding the exact same range is telling. We have also just wiped out roughly 750M in longs on this move down. To me, this looks like a healthy market cleanse, a brief deleveraging event. We dropped 6% from the highs, so I have decided to re-enter with a 10x long. In bull markets, the \"ideal\" sweep or perfect entry often never comes. The level everyone is waiting for is the one price does not need to revisit. From experience, I would rather position slightly ahead of the herd than be left waiting for a level that doesn't have to be tested. That is why I have re-entered the position just 0.75% lower.（计划会变，这就是交易。本来我准备按兵不动、等 80–82K 区域。但看到情绪彻底崩掉、而我们还卡在完全相同的区间里，这很说明问题。这波下跌里我们刚刚清掉了大约 7.5 亿美元的多头。在我看来，这像一次健康的市场清洗、一次短暂的去杠杆事件。我们从高点跌了 6%，所以我决定用 10 倍杠杆重新进场。牛市里，「理想」的扫针或完美入场往往永远不来。所有人都在等的那个价位，正是价格不需要回去的价位。凭经验，我宁愿比羊群稍微提前一点点建仓，也不愿干等一个未必会被测试的位置。这就是我只低了 0.75% 就重新进场的原因。）引推是他本人 2 小时前的原帖：Entry is 82.860. Invalidation is 74.550（入场 82.860，失效 74.550）。",
      read: "<b>这条是本轮最该警惕的一条：他当场推翻了自己 2 小时前刚说出口的计划。</b>10-07 21:12 他明确讲「80–82K 是我要重建那笔激进 10 倍仓的区间、此刻没有理由急着开新多」，23:07 就在 82.86K 进场，这条再把改计划的理由摊开。改动的是 10-05「不等回踩、分批部署」以及 10-07「等 80–82K」这两条<b>可执行性</b>——把「等更低」用「情绪崩塌 + 7.5 亿美元多头被清算 + 自高点回落 6%」解释成「健康清洗、短暂去杠杆」，与 09-25「该爆的都爆了、杠杆已重置」是同一套论证。⚠️ 两处需注意（分析）：① 这是他<b>连续第二次</b>宣布要等更低、又提前进场（10-05 说等 80–82K → 10-06 在 83.5K 建仓；10-07 又说不急 → 当晚 82.86K 进场），说明「等回踩」在他这里系统性不可信；② 按 10-08 实际盘面，从 10-05 高点 86,999 到日低 82,227 约 −5.5%，与他说的「跌 6%」基本吻合（若按 10-02 插针 87,220 算约 −5.7%），未构成夸报；但「7.5 亿美元多头清算」为他的自述口径，无法独立核验。失效条件：若价格继续下破并触及他自己给的 74,550 失效线，「健康清洗」的定性当场反转成趋势转弱，这笔提前进场会被套在区间上沿之上；反向若 82.8K 一线直接止跌起涨，则「提前 0.75%」被证明是对的。",
      tags: ["仓位建议", "链上数据", "失效条件"],
      src: "X 原文 @KillaXBT · 2107892993831440645"
    },
    {
      date: "2026-10-07",
      title: "止损当晚重开 10 倍多：入场 82.86K，失效 74.55K，目标 126K",
      quote: "I have decided to activate into another 10x long position on $BTC here. Entry is 82.860. Invalidation is 74.550 with maintaince margin. In the event invalidation is hit, I will long a second entry on 10x. This is again, a seperate position from my current longs from 62.600 & 76400. The objective of this trade is simple. Utilize leverage to capitalize on bitcoins movement to 126,000 next year.（我已决定在这里再开一笔 10 倍 BTC 多单。入场价 82.860。按维持保证金计算的失效位是 74.550。若失效被触发，我会再开第二个 10 倍入场。这一笔同样与他 62.600 和 76400 的现有持仓相互独立。这笔交易的目标很简单：用杠杆去吃下比特币明年走向 126,000 的这段行情。）引推是他本人同日 21:12 的原帖（即 83.5K 那笔已在保本位被止损、80–82K 是他要重建的区间）。",
      read: "改动的是 09-29「第三笔多单开在 83.5K」那条的<b>三代持仓结构</b>——83.5K 那笔已于当晚在保本位被止损，取而代之的是 <b>82.860 的新一笔 10 倍</b>，与 62.6K / 76.4K 并列、并声明相互独立。三个新参数值得记：① <b>首次给 10 倍仓写明硬失效价 74.550</b>（此前 09-29 只推算「约 −10% ≈ 75K」），且这个价位与他 10-03 给出的「74K–77K 投降底」基本重合，等于把失效线压在投降底的下沿；② 首次明确<b>失效即加仓</b>——「若失效被触发，我会再开第二个 10 倍入场」，把 09-29「第一笔失效即换更低位再入」从口头逻辑正式写成执行规则，属金字塔式补仓（不是止损离场）；③ 目标首次写成「126,000 <b>next year</b>」，与 10-04「Q2–Q3 交易在 126K 上方」口径一致，把 126K 明确放到 2027 年。⚠️ 分析：入场 82.860 比他 2 小时前自己说的 80–82K 区间<b>上沿还高</b>，只比被止损的 83.5K 低 0.75%，等于「等更低」实际上没等。失效条件：价格触及 74,550（维持保证金线）→ 该仓失效，且按他的规则会再加一笔 10 倍（风险叠加而非收敛），届时 74–77K 投降底情景直接对撞；反向若 82.86 站住并向上攻破 87K，这笔即被他定义为抢跑成功。",
      tags: ["仓位建议", "关键价位", "失效条件"],
      src: "X 原文 @KillaXBT · 2107850216044917032"
    },
    {
      date: "2026-10-07",
      title: "一句情绪条：这点跌幅也叫跌？把图拉远",
      quote: "Dip? What dip, for ants? When in doubt, zoom out... $BTC You can tell everyone is glued to the 5 minute TF clicking buttons for dopamine.（跌？什么跌，给蚂蚁看的？有疑问的时候，就把图拉远……BTC。你一眼就能看出，所有人都黏在 5 分钟级别上点按钮找多巴胺。）随推附一张图，图内内容未读取，未作转述。",
      read: "纯态度条，<b>无点位、无新条件</b>。是把 10-07「这是低周期噪音，我是高周期交易者」的立场在情绪层面再确认一次——按 10-08 实际盘面，从 10-05 高点 86,999 到日低 82,227 约 −5.5%，他把它定性为「给蚂蚁看的跌幅」，等于预先否认这根回撤具备结构性意义。与他 09-30「低周期都是噪音」、10-02「把牛市里的事搞复杂」同源，属同一套「不做短周期、不加解释」框架的又一次取样。无失效条件（本条不含任何价位）。",
      tags: ["情绪指标"],
      src: "X 原文 @KillaXBT · 2107845824445321621"
    },
    {
      date: "2026-10-07",
      title: "83.5K 那笔 10 倍在保本位被止损，改等 80–82K 重建",
      quote: "GM. We failed to break 87K yet again. In due time we will, but that wasn't the thesis behind this trade. So as mentioned in my previous post, the 10x long was stopped at BE. It was an aggressive continuation long, anticipating a breakout on the second test of the highs. Since the break failed and we're back at entry, 80-82K is now the range I'll be watching to rebuild that aggressive 10x long. For now, I'm holding my 62.6K and 76.4K entries. I see no reason to rush into new longs at the moment, though the 10x strategy will definitely work for anyone who is underexposed. Risk management is vital, and I already hold enough BTC as it stands. I am still bullish, still expecting higher, this is LTF chop & I am a HTF trader.（早上好。我们再一次没能突破 87K。迟早会破的，但那并不是这笔交易的论点。所以正如上一条所说，那笔 10 倍多单在保本位被止损了。它是一笔激进的延续多单，赌的是第二次测试高点时突破。既然突破失败、我们又回到了入场价，80–82K 就是我现在盯着的、用来重建那笔激进 10 倍多单的区间。眼下我持有 62.6K 和 76.4K 两笔。此刻我看不出有什么理由急着开新多，不过对于敞口不足的人来说，这套 10 倍策略肯定有效。风控至关重要，而我现在手上的 BTC 已经足够多了。我依然看涨、依然预期更高——这只是低周期噪音，而我是做高周期的。）引推是他本人 10-05 的原帖（83.5K 那笔止损上移到入场价，并给 87K 破位设了「必须在这一根周线内」的死线）。",
      read: "改动的是 10-06「83.5K 那笔止损上移到成本价、自称 risk free trade」那条的<b>最终结果</b>——他确认这笔在保本位被止损离场，也就是 09-24 以来那笔号称浮盈 25 万美元的激进 10 倍仓，以零盈亏结束。同时改动的是 10-05 那张时间表的<b>结算</b>：「87K 必须在这一根周线内突破」的死线被判失败（「failed to break 87K yet again」），他照自己预设的失败分支切换到「回踩 80–82K 重建 10 倍仓」。需要留意（分析）：① 他这次公开说了「<b>此刻没有理由急着开新多</b>」，但 2 小时后就在 82.86K 建了仓（见同日 23:07 那条），这两句直接冲突；② 62.6K / 76.4K 两笔仍不动，说明减风险只发生在最激进的那一笔；③「这只是 LTF 噪音、我是 HTF 交易者」是<b>事后免责</b>式措辞，把择时失败归入周期噪音。失效条件：若价格不回落 80–82K 就重新站上 87K，他「等 80–82K 重建」的计划又落空一次（与 10-06 同类情形重演）；反向若 82.5K 有效失守并深入 80–82K 下方，则他 10-03 的 74–77K 投降底剧本被激活，重建区本身也要重估。",
      tags: ["仓位建议", "关键价位", "失效条件"],
      src: "X 原文 @KillaXBT · 2107821439688516081"
    },
    {
      date: "2026-10-07",
      title: "纯情绪条：他们要更低，等真低了又想要更低",
      quote: "They want lower until lower actually comes, then they want even lower.（他们想要更低的价格，直到更低真的来了，然后他们又想要更低。）",
      read: "纯情绪／态度条，<b>无点位、无新条件</b>。是把 09-28「希望这是假突破的人越多、说明空仓越多」、10-04「等回踩 2–3% 的人全被抢跑」那套<b>逆向情绪读数</b>的第四次取样，对象这次是「盼跌心态永不满足」。作用在于把「多数人没有正确持仓」这个前提再确认一次，为次日凌晨「情绪彻底崩掉 = 健康清洗」的判断做了铺垫。无失效条件（本条不含任何价位）。",
      tags: ["情绪指标"],
      src: "X 原文 @KillaXBT · 2107814460324810778"
    },
    {
      date: "2026-10-07",
      title: "插针砸到 83.5K 后喊话：不敢买血的人不配吃涨",
      quote: "If you can’t buy the blood, you don’t deserve the green.（如果你不敢在血流成河时买入，你就不配享受绿色的上涨。）",
      read: "这条本身不新增点位，但它的<b>时间点</b>是全部价值所在：按 10-07 实际盘面，GMT+8 09:00–10:00 价格从 85.6K 急挫至 <b>83,577</b>，而这正是他 09-29 那笔 10 倍多单的成本线 $83.5K；他在 10:08 发出这句「买血」。改动的是 10-02「任何下行都应该凶狠而迅速地买入」与 09-27「牛市不给你理想回踩」那条的<b>兑现状态</b>——从「将来遇到跌要快接」变成「此刻这根针就是我说的那种机会」，也是 10-06「本季度 75% 会出现某种形式的拒绝」那条第一次<b>从概率变成正在发生的事件</b>，且形式正是他预判的「插针」。失效条件：如果这根本轮「血」不是洗盘而是趋势转弱的起点——即 82.5K 有效失守并向 80–82K 延伸而不快速收回——「买血」就变成接刀，他 10-05 的 80–82K 扫针情景同步升级为 10-03 的 74–77K 投降底情景。",
      tags: ["情绪指标", "仓位建议", "失效条件"],
      src: "X 原文 @KillaXBT · 2107654199228150010"
    },
    {
      date: "2026-10-07",
      title: "「即将来临」：引自己插针定律，预告大级别波动将至",
      quote: "Coming soon... $BTC（正文仅此两词加标签；引推为他本人 10-06 的原话：Before any big correction/impulse their is always a liquidation wick. 即「在任何大级别回调或推动之前，总会先有一根清算插针。」）",
      read: "改动的是 10-06「本季度 75% 概率出现拒绝」那条的<b>时间颗粒度</b>——从「本季度内」压缩到「即将（coming soon）」，并预设其形式是<b>先插针、再出方向</b>。把它与同批「NY 开盘拉高再全数回吐、把空头养肥后一根插针爆掉」并读，等于给「拒绝」配了一套入场前的固定动作：插针即起点。分析（事后校验）：他发出这条约 1 小时后，GMT+8 09:00–10:00 价格即从 85.6K 插至 83,577，插针确实出现，这条在事后获得实证，但他<b>未说出方向</b>——插针之后是向上爆空还是向下破位，才是真正的验收点。失效条件：若插针之后价格既未有效上破 87K、也未有效下破 82.5K，而是重新陷入窄幅横盘，「插针=大行情前奏」这一用法本轮落空。",
      tags: ["关键价位", "情绪指标", "失效条件"],
      src: "X 原文 @KillaXBT · 2107623471824138680"
    },
    {
      date: "2026-10-07",
      title: "长文：已收复熊市跌幅一半却零热度，最大痛感向上",
      quote: "你大概会以为，在收复了整个熊市跌幅的一半之后，人们会看多。然而现在是零热度。没有兴奋、没有头条。只有那些因为太固执、太贪婪而在价格更低时不肯买入、因而错过了底部的场外观望者。如今趋势已明确转变，他们还在求更低的价，还在等那个完美的回踩来做多。他们要么是在场外观望并自我安慰，要么是过早平掉了多单，现在需要价格回到某个特定水平来给自己的入场一个「说法」。我不为任何事情找理由，我反应的是当下的价格行为（PA），不是我希望价格去到的位置。正是这种思维让我抓到了底部，而别人没有。市场不会奖励那些要求完美入场的人。它用持续走高和浅回踩来惩罚他们，而他们就坐在那里把每一根绿K叫作陷阱。牛市不会把完美的买入机会递给你，正如熊市不会把完美的回测卖出机会递给你。不管你喜不喜欢，BTC 的最大痛感是向上的。",
      read: "改动的是 09-27「你不会有理想回踩、提前建仓最聪明」与 10-03「买血要凶狠迅速」那条的<b>论证素材</b>——他第一次给出一个可验证的量化说法：<b>已经收复整个熊市跌幅的一半</b>，并以此反驳「市场缺乏热度」的情绪面。这也是本轮唯一一次把<b>零热度、零头条当作利多</b>（热度还没到 = 空间还在），与 09-25「所有人都想要更低的价」、09-28「希望是假突破的人越多说明空仓越多」同源，属同一框架的又一次取样。⚠️ 分析：他所谓「收复熊市跌幅一半」是<b>自设基准、未给起止点</b>——按他 09-29 自述本轮熊市跌 54% 的口径，与当前 83.5K–86.6K 的实际区间无法直接对齐，属<b>不可独立验证的表述</b>，不宜当作事实引用。失效条件：若价格在 82.5K 下方有效失守，「趋势已明确转变」这个全篇前提作废，整段「零热度=还有空间」的推论随之反转；反之若真的在零热度中继续走高，这条会成为他 10-04「机构已拿到结构确认」的补强证据。",
      tags: ["情绪指标", "周期判断", "失效条件"],
      src: "X 原文 @KillaXBT · 2107607778353414344"
    },
    {
      date: "2026-10-07",
      title: "定义当下为「垂直吸筹」：未扫的低点与难受的区间",
      quote: "Study vertical accumulation.... $BTC Unswept lows, uncomfortable ranges, shitty price action, and constant contemplation over what happens next. Disbelief.（研究一下垂直吸筹……BTC。未被扫掉的低点、让人难受的区间、糟糕的价格行为，以及对下一步会怎样反复琢磨。怀疑（disbelief）。）随推附一张图，图内内容无法读取，未作转述。",
      read: "改动的是 10-03 首次提出的「机构资金垂直吸筹」那条的<b>特征清单</b>——当时他只拿它解释压缩、假突破和反复被拒，这条第一次把「<b>未被扫掉的低点（unswept lows）</b>」列为吸筹的构成标志，等于提前为「不扫前低就直接向上」留好了说法，与他 09-29「即使回撤到前区间高点下方，也不必出现跌破低点的扫针」直接咬合。按 10-07 实际盘面，日低 83,577 确实高于他 10-05 反复强调要盯的 82.5K 决策线，因此「未扫的低点」暂时成立。同时「disbelief（怀疑）」是他 09-27「不敢相信阶段」以来的<b>第四次取样</b>，作用只是把「大多数人不在场」这个前提再确认一次。失效条件：若价格真的向下扫掉前低（有效跌破 82.5K 并触及 80–82K 或更低），「低点不会被扫」的假设当场失效；反之若插针后收复 85K 上方，本条定义成立。",
      tags: ["趋势切换", "情绪指标", "失效条件"],
      src: "X 原文 @KillaXBT · 2107556294710186232"
    },
    {
      date: "2026-10-07",
      title: "新增山寨喊单：$LTC 将插出神烛冲 100 美元",
      quote: "When $LTC randomly prints a god candle to $100, don’t act surprised. This dinosaur coin has been sleeping for far too long.（当 LTC 突然打出一根冲向 100 美元的神烛时，别表现得惊讶。这枚恐龙币已经沉睡太久了。）引推是他本人早前的原话：Decided to lob $50K into $LTC. Do not disappoint in 2–3 years from now, sir. @litecoin（我决定往 LTC 里砸 5 万美元。两三年后别让我失望，先生。）随推附两张图，图内内容无法读取，未作转述。",
      read: "改动的是 09-26「$SOL 自公开入场已涨 75%」那条的<b>山寨清单</b>——除了 SOL，这条第一次把 <b>LTC</b> 写进他的公开持仓与目标：目标位 100 美元、持有期自述 2–3 年、已投入 5 万美元，并预期一根「神烛」。这是本轮<b>唯一一条非 BTC 的价位判断</b>，也给 09-18 基准剧本里「山寨已提前见底、进入轮动布局期」补上了一个具体标的。⚠️ 注意口径：100 美元相对 LTC 的历史区间属<b>长周期目标</b>而非短线喊单，与他的 BTC 剧本不在同一时间尺度上，不能与其他条目的失效条件混用。失效条件：LTC 在所述 2–3 年内未走向 100 美元、或跌破这笔 5 万美元建仓的成本区，「沉睡太久」的判断及该笔布局即告失效——但这是长期口径，短期内无法证伪。",
      tags: ["山寨", "目标价"],
      src: "X 原文 @KillaXBT · 2107537490349330595"
    },
    {
      date: "2026-10-07",
      title: "区间内固定剧本：NY 开盘拉高再全数回吐，养肥空头后插掉",
      quote: "Rinse and repeat throughout this entire range. Pump NY open, then reverse the entire move. Their intentions are pretty obvious. Make $BTC shorts comfortable enough to keep pressing entries, then wick price back up and blow them out in one candle, just like every previous range.（在整个区间里一遍遍重复：抬高纽约开盘，然后把整段涨幅全部回吐。他们的意图相当明显——让 BTC 空头舒服到不断加仓，然后一根插针把价格拉回去、一次爆掉他们，就像之前每一个区间那样。）随推附一张图，图内内容无法读取，未作转述。",
      read: "改动的是 10-05「周末拉升成生死局」那条的<b>失败分支的解释权</b>——当时「周末拉盘失败、直接回落低 80K」被他自己列为一种真实风险，这条把它重新定义为<b>做市方的刻意为之一</b>（先养肥空头、再一根插针爆掉），等于给短期回落预置了一个「这是洗盘不是转弱」的说法，手法与 09-30「季线月线收盘会有操纵」、10-03「垂直吸筹」同源。⚠️ 分析：这条的内在方向是<b>偏多</b>（他预期最终是被向上插针、空头被爆），因此与他 10-06「本季度 75% 会出现拒绝」存在张力——同一个区间，他一边说会被拒绝、一边说是诱空。失效条件：若价格在区间内被<b>向下解决</b>（有效跌破 82.5K 且不快速收回），「一根插针爆空头」的剧本要改写成「空头拿到了真正的趋势」；反之若再现一次向上插针，本条得到印证。",
      tags: ["关键价位", "情绪指标", "失效条件"],
      src: "X 原文 @KillaXBT · 2107502905179984356"
    },
    {
      date: "2026-10-06",
      title: "提定律：任何大回调或大推动之前，总会先有一根清算插针",
      quote: "Before any big correction/impulse their is always a liquidation wick.（在任何大级别回调或推动之前，总会先出现一根清算插针。）",
      read: "改动的是「扫针」在他体系里的<b>性质</b>——09-30「扫针就是做多」把它当成单向的接多信号，这条把它升级为<b>双向事件的前置条件</b>：插针本身不指向方向，只说明「大动作要来了」。这直接为次日 10-07 08:06 那条「Coming soon...」做了铺垫，也与同日「拉高再回吐、把空头养肥」构成同一套读法。⚠️ 分析：这条是<b>纯前设、无价位、无方向</b>，它的用处在于事后可以用「有没有出现插针」来校验收紧跟随后续判断的起点是否成立——按 10-07 实际盘面（85.6K → 83,577），前提确实兑现。失效条件：一次大级别回调或推动在<b>没有前置插针</b>的情况下直接发生，这条定律即被打破；它本身不含任何可交易的价位或方向。",
      tags: ["周期判断", "情绪指标", "失效条件"],
      src: "X 原文 @KillaXBT · 2107466096726921307"
    },
    {
      date: "2026-10-06",
      title: "首次松口考虑 2023 分形：会不会先抢跑多头与前低",
      quote: "Wait a minute... I have seen this story before... $BTC Lets see if we follow the same 2023 pattern. Front running all longs & the lows.（等一下……这个剧本我见过……BTC。看看我们会不会重演 2023 年那套模式：先抢跑所有多头、再抢跑低点。）随推附一张图，图内内容无法读取，未作转述。",
      read: "<b>这是本轮最值得盯的一条，因为它直接回到他自己否定过的那条判断上。</b>09-29 他专门用一条长文反驳 2023 分形，理由是「BTC 已形成周线更高高点、动力学完全不同」，并断言即使照搬该分形也<b>不一定会出现跌破低点的扫针</b>。这条第一次把同一个分形重新摆上桌，且用了<b>开放式措辞（Wait a minute / Let's see / 会不会）</b>，等于把 09-29 的「已排除」降级为「待观察」。改动的是九月底那套「递减回报 + 更浅回踩、不必跌破低点」框架的<b>置信度</b>；落到价位上，就是 09-29 他自己量化的 $78K（−10%）/ $74K（−15%）这条更深回踩路径<b>重新具备被激活的可能</b>。失效条件：若价格不扫前低（不有效跌破 82.5K / 80–82K）就直接向上突破 87K，2023 分形被证伪、他 09-29 的原判成立；反之若真的先抢跑低点再拉升，他 09-29 那段反驳需要重写。",
      tags: ["趋势切换", "失效条件", "周期判断"],
      src: "X 原文 @KillaXBT · 2107437715734343854"
    },
    {
      date: "2026-10-06",
      title: "首次给出概率：本季度 75% 会出现一次拒绝，但 87.2K 下方不做空",
      quote: "我的计划很简单。我们刚刚走完一个非常强的季度收盘。在我看来，这个新季度内有 75% 的概率 $BTC 会经历某种形式的拒绝（rejection）。就个人而言，我和很多在做的人不一样，我对在 87.2K 高点下方做空毫无兴趣——那是在捡芝麻。我更偏好为更大的行情去布局，那才是我最擅长的。随着季度推进，我会留意价格偏离进入这个框（box）的机会，用来对冲掉一部分我的延续多单。除此之外，除非价格扫进这个区域，我根本不打算进场。",
      read: "这是本轮<b>第一次把主观判断量化成概率</b>——「本季度 75% 会出现某种形式的拒绝」，也是他罕见地把一个负面情景（拒绝/回落）写进了自己的多头剧本。改动的是 09-25「唯一做空位 \$93.6K」那条的<b>空头纪律</b>：现在他明确划定 87.2K 下方<b>完全不做空</b>，并在同一条里给出替代动作——等价格偏离进入框体内，用对冲替代做空。这与同日「对冲 76.4K 那笔、失效 92.8K」互相咬合，构成一套完整方案：<b>不下空单，改用对冲承接回撤</b>。失效条件：若 2026 Q4 全程没有出现任何形式的拒绝或回撤（单边直上），75% 这个概率判断落空；反向的失效点是价格在 87.2K 下方持续阴跌而非「拒绝后重拾升势」，那样他预期的「拒绝」性质就从洗盘变成了趋势转弱。",
      tags: ["周期判断", "失效条件", "仓位建议"],
      src: "X 原文 @KillaXBT · 2107232068673392647"
    },
    {
      date: "2026-10-06",
      title: "对冲方案补全：对 76.4K 多单等额对冲，失效位下移到 92.8K",
      quote: "我会在这个框（box）内对我从 76.4K 建的 $BTC 多单做对冲。这会是一笔等额对冲（equal hedge），失效位设在 92.8K。",
      read: "这条把同日「对冲 76.4K 那笔」的方案<b>补上了失效位</b>，也再次确认是等额（equal）而非全额对冲。改动的是 09-25「对冲空单入场位上移到 \$93.6K、到位后对冲 100% 敞口、失效位 \$99–100K」那条的<b>三个参数</b>：入场位从 93.6K 下移到 89.4–90.6K 框内、规模从「100% 敞口」降为「等额单腿」、失效位从 99–100K 下移到 <b>92.8K</b>（下移约 6–7K）。这是对冲计划连续多轮后置之后<b>第一次真正开工</b>，但同时也明显缩水——他不再打算对冲全部敞口。失效条件：价格有效站上 92.8K，这笔对冲作废；注意 92.8K 之上对他而言等于「不回调直接走」，与「本季度 75% 会有拒绝」的判断相互矛盾。",
      tags: ["仓位建议", "关键价位", "失效条件"],
      src: "X 原文 @KillaXBT · 2107195230663421984"
    },
    {
      date: "2026-10-06",
      title: "年内区间上限再压缩到 95K 下方，用 2023 年 3 万下方盘整作类比",
      quote: "我们会在 95K 下方盘整，就像 2023 年我们在 30K 下方盘整那样。在一段以时间换空间的震荡与整固之后，$BTC 会突破到新的历史新高。（引推为媒体标题：BREAKING: Our traders forecast Bitcoin will hit $95,000 this year）",
      read: "改动的是 10-03「今年最高看 97K、余下时间在 97K 下方区间震荡」那条的<b>区间上限</b>——从 97K 再压低到 <b>95K 下方</b>，并且第一次给出这段盘整的<b>历史类比</b>（2023 年在 30K 下方盘整数月后向上突破）。把它与 10-04 的「2027 Q2–Q3 交易在 126K 上方」「4/26–8/2 破 ATH」串起来看，这条是在为那段跨年上涨补一个前置条件：<b>先有一段以时间换空间的整固，才会有突破</b>。含义是他把未来数月的横盘重新定义为「常态」而非「转弱」。失效条件：若在 95K 下方盘整期间价格先有效跌破 80K 结构（盘整实质上变成下跌），2023 年的类比对不上；反向失效是价格不做盘整直接冲上 95K，这条「95K 下方整固」被跳过。",
      tags: ["周期判断", "目标价", "基准剧本"],
      src: "X 原文 @KillaXBT · 2107170248717742542"
    },
    {
      date: "2026-10-05",
      title: "首次给出对冲结构：89.4–90.6K 只对冲 76.4K 多单，现货与 62.6K 不动",
      quote: "我预期 $BTC 会去测试 89.4–90.6K。我会对我从 76.4K 建的 BTC 多单做等额对冲。我从 65K 的现货和从 62.6K 的多单不会被对冲。",
      read: "这是他<b>第一次把对冲计划说成结构而不是一个价位</b>：触碰区间 89.4–90.6K、对冲标的只有 76.4K 那一笔延续多单、而 65K 现货与 62.6K 多单明确豁免。改动的是 09-25 那条「到位后对冲 100% 的敞口——包括现货、延续多单和波段多单」——现在<b>现货被主动排除在对冲之外</b>，等于他在下跌情景里选择继续全额持有现货。价位上则回到 09-28 的「\$89.2–90.6K 潜在拒绝区」，说明这个区间被他反复引用、稳定性相对较高。失效条件：价格未触及 89.4–90.6K 就直接跌破 82.5K，这套「等到高位才对冲」的安排会滞后一拍；反向失效是有效站上 92.8K，对冲作废。",
      tags: ["关键价位", "仓位建议", "失效条件"],
      src: "X 原文 @KillaXBT · 2107119996123902441"
    },
    {
      date: "2026-10-05",
      title: "83.5K 多单止损上移到成本价，并给 87K 破位加上「本周K线」死线",
      quote: "$BTC 距 83.5K 那笔激进多单入场已上涨 4.5%。我现在把这笔延续多单的止损上移到入场价。如果 BTC 要突破 87K，那就必须发生在这一根周线上；否则，我预期会重新回踩 80–82K。如果真出现那种情况，我会考虑在更低的几个百分点处部署那套激进的 10 倍多单策略。除此之外，这就是一笔无风险交易了。（引推为他自己 09-29 的原帖：I longed 62.6K. I longed 76.4K. Now I am long again from 83.5K on 10x.）",
      read: "本轮<b>最实质的一次风控变更</b>：他把 83.5K 那笔的止损上移到入场价，并自称「无风险交易（risk free trade）」——改动的是 09-29「三笔多单全部打开、什么都没变」那条的<b>持仓状态</b>，这笔激进的 10 倍仓从「全额承担风险」变成「保本持有」，容错空间被他自己主动关掉。同时他给 09-30「下周突破 87K+」那张时间表补上了<b>明确死线：必须在这一根周线内完成</b>，否则转为回踩 80–82K 的情景，并在那条情景里打算「在更低几个百分点处」重新部署 10 倍多单——这是对 10-02「7–10 倍接多」的执行补充。需注意（分析）：按 10-05 盘中高点 86,999 与其 83.5K 成本计算约 +4.2%，与他说的 4.5% 基本吻合；但 87K 至今仍未站上（10-02 曾插针 87,220）。失效条件：本周周线收完仍不能站上 87K，则「破 87K」路径本轮失效、切换为 80–82K 回踩；再往下 82.5K 有效失守，则 80–82K 情景本身也需重估。",
      tags: ["仓位建议", "失效条件", "关键价位"],
      src: "X 原文 @KillaXBT · 2107098902532882654"
    },
    {
      date: "2026-10-05",
      title: "引自己 09-30 原帖喊「Told ya」：宣布 87K 突破已兑现",
      quote: "Told ya.（正文仅此两词；引推是他本人 2026-09-30 的原帖：Translation: Next week $BTC is breaking out to 87K+，即中文版「翻译一下：下周 BTC 突破 87K 以上」。随推附有一张走势图，图内内容无法读取，未作转述。）",
      read: "一条<b>战绩复盘</b>——他把自己 09-30 那条「下周 BTC 突破 \$87K 以上」的原帖翻出来，只用两个词宣布己方兑现。改动的是 10-05「周末拉升成生死局」那条的<b>状态</b>：当时他给的是对称二选一（打出神烛 or 直接回落低 80K），这条等于宣告<b>「神烛」分支已触发</b>，并把 10-05 那条里「守 82K → 看 87K → 破 87K → 90Ks 重新上桌」的三段式推进到第三段，也把 09-30 那张时间表从「待验收」结算为「已兑付」。需要注意的是（分析）：按 10-05 01:00 UTC 前的实际盘面，周末这波把价格从 84,719 的日低推到 86,999 的盘中高点、贴着 87K 而未真正站稳（10-02 曾插针至 87,220），因此这更像一次<b>提前的胜利宣告</b>，而非对「站稳 87K 上方」的确认。失效条件：若价格不能有效站上 87K 并重新跌回 82.5K 下方，「神烛已触发」与「87K 已兑现」两说同时作废，剧本回到 80–82K 扫针情景；反向的下一验收点是他自己给的「破 87K → 90K 区间重新上桌」。",
      tags: ["战绩复盘", "目标价", "关键价位"],
      src: "X 原文 @KillaXBT · 2106918427701215360"
    },
    {
      date: "2026-10-05",
      title: "周末拉升成生死局：要么打出神烛，要么直落低 80K",
      quote: "对 $BTC 来说这是生死时刻。要么我们利用周末动能和稀薄的订单簿打出一根神烛（god candle），要么这轮周末拉盘失败、我们直接回落进低 80K 区间。（引推为他自己 09-26 的原话：「一旦开始出现周末拉升，你就知道我们身处牛市。周末抢跑 legacy 资金，一直是个很有说服力的信号。」）",
      read: "改动的是 09-26「周末拉升＝牛市特征」那条——当时它是一条<b>单向看涨的行为信号</b>，这条第一次给它加上<b>明确的失败分支</b>：如果周末拉盘不成立，他预期「直接回落进低 80K 区间」。这是本轮他首次把短线剧本写成对称的双向结构（神烛 or 回落），等于把 09-26 那条信号从「已经确认的牛市证据」降级为<b>需要本周兑付的待验证假设</b>。失效条件：周末动能在周初被吞没、价格跌回低 80K（约 80–82K），则「周末拉升＝牛市」这条行为信号本轮作废；反之若真打出放量长阳，则 82.5K 上方的 87K 路径被激活。",
      tags: ["趋势切换", "关键价位", "失效条件"],
      src: "X 原文 @KillaXBT · 2106877551402418613"
    },
    {
      date: "2026-10-05",
      title: "情绪读数：高杠杆把所有人变成追涨杀跌的变色龙",
      quote: "我记得以前人们是真的会为价格上涨而庆祝的……现在看来，是过度杠杆把所有人都变成了变色龙，追着低周期的每一点波动跑。",
      read: "纯态度／情绪条，<b>无点位、无新条件</b>。是他 10-02「跌的时候庆祝的人比涨的时候还多」的<b>续写</b>——同一次观察延展到「高杠杆导致短周期情绪紊乱」。作用是把「多数人没有正确的持仓心态、不该盯 LTF」这个前提再确认一次，与他 09-30「当你做的是高周期，大部分低周期的价格行为都只是噪音」同源。无失效条件（本条不含任何价位）。",
      tags: ["情绪指标"],
      src: "X 原文 @KillaXBT · 2106855655680233535"
    },
    {
      date: "2026-10-05",
      title: "决策线下移到 82.5K：守住看 87K，丢了扫 80–82K",
      quote: "又一根周线收在 81K 上方，看起来是大概率。如果我们丢掉 82.5K，那我会去找一次向 80–82K 区域的扫针。这里是很明显的不确定（indecision）：我们扫了低点、看到向上强势反应，然后又被拒回周线开盘位。这告诉我两种可能之一：1）我们还没准备好突破；或者 2）我们在下一腿向上之前诱空。不管哪种，都要紧盯 82K 这一带。如果我们继续守在它上方，我预期还有一次向 87K 高点的推进。如果那（87K）被有效攻破，那么 90K 区间就重新回到桌面上。",
      read: "改动的是 10-02「85K 关口已翻多」那条的<b>决策线</b>——当时他把防守参考放在 <b>84.6–85.2K</b>，现在整体下移到 <b>82.5K / 82K</b>，等于承认 85K 并未真正守住（价格被打回周线开盘位）。同时他把 09-30「下周突破 87K 上方」那张时间表重新<b>条件化</b>：87K 不再是默认会到，而要先看能否守住 82K；并把 87K 之上接续到「90K 区间重新上桌」，与 09-27「本腿理想延伸 92–94K」衔接。失效条件：<b>82.5K 被有效跌破</b>，则「87K 推进」路径暂告失效、切换为 80–82K 扫针情景；反向失效线是价格持续守在 82K 上方却始终推不进 87K，说明「诱空后再上」这条分支也不成立。",
      tags: ["关键价位", "趋势切换", "失效条件"],
      src: "X 原文 @KillaXBT · 2106816025173930138"
    },
    {
      date: "2026-10-04",
      title: "给出跨年时间表：Q2–Q3 交易在 126K 上方，Q4 不会见顶",
      quote: "我们在 7 月见底，在 Q4 之前两个月。所以，就像我说过的，我认为 BTC 会在 Q2–Q3 交易在 126K 上方。结果 Q4 是去风险（de-risking）而不是抛物线式上涨。所有人都困惑，想着『接下来呢？我们都瞎了吗？』不，是你们瞎了，我没有。$BTC 这个周期不会在 Q4 见顶。",
      read: "改动的是 10-02「年内上限 97K、余下时间在 97K 下方震荡」那条的<b>时间坐标</b>——他把 97K 上限明确标定为<b>仅限 2026 年</b>，并把 126K 的到达时间从 09-27 的含糊表述落到 <b>Q2–Q3（按语境为 2027 年）</b>，同时否定「Q4 见顶」并把 Q4 定性为去风险期。这与他 09-25「新高会早于减半出现」形成呼应，等于把长线剧本的验收点整体推到明年上半年。失效条件：若 2027 年 Q2–Q3 未能交易到 126K 上方，这条跨年时间表作废；更近的失效点是 <b>2026 年 Q4 出现抛物线式上涨并直接创新高</b>，那会同时推翻「Q4 去风险」这个定性。",
      tags: ["周期判断", "目标价", "基准剧本"],
      src: "X 原文 @KillaXBT · 2106757104526643459"
    },
    {
      date: "2026-10-04",
      title: "首次给出 ATH 突破窗口：4/26–8/2，称比所有人预期更快",
      quote: "$BTC 会在 4 月 26 日到 8 月 2 日之间突破历史新高（ATH）。我说过我们会更早见底，我们做到了。现在，我们会比所有人的预期更快地做出新的 ATH。也许你该开始听一听了。",
      read: "这是本轮<b>最硬的一条长线时间承诺</b>——把 09-27「到 126K 的上涨应该是猛烈且快速的」从形容词落成了<b>可上日历验收的窗口（4/26–8/2）</b>，并与同批那条「Q2–Q3 交易在 126K 上方」互相咬合（推文未标年份，按语境为 2027 年）。它替换的是 09-18 基准剧本「2026 年摸不到 10 万」的旧口径（此前已被 10-03 的 97K 上限取代）。注意属性：这条一半是<b>对未来行情的预测，一半是对自己「更早见底」前设的自我背书</b>，可证伪点比结构判断远得多——窗口内未破 ATH 即当场打脸。失效条件：窗口内未突破历史新高；或期间价格先有效跌破 80K 结构，那连「更早见底」的前设一起作废。",
      tags: ["目标价", "周期判断", "失效条件"],
      src: "X 原文 @KillaXBT · 2106737639726645418"
    },
    {
      date: "2026-10-04",
      title: "对冲空单再后置：要等中期选举临近才考虑",
      quote: "我不需要说那些显而易见的事：我显然不预期新低。话虽如此，中期选举之后我们仍可能看到某种去风险（de-risking）。所以眼下最聪明的做法是：等到那个时间窗口临近，再考虑任何对冲空单。这正是我目前仍然持有多头仓位的原因。",
      read: "改动的是 09-25「对冲空单上移至 $93.6K」→ 09-29「低 90K 区间」那条的<b>触发条件</b>——此前是纯价格条件（到 90–93K 才对冲），现在叠加了一个<b>宏观时间条件：等中期选举临近再考虑</b>。等于把对冲计划整体后置，并首次承认「中期选举后可能出现去风险」。同时他明确「不预期新低」+「我仍然持有的是多单」，说明这轮改口<b>没有带来任何减仓</b>。失效条件：若中期选举前价格直接有效跌破 80–83K 关键区，「等选举后再对冲」就变成滞后一拍，对冲窗口直接错过。",
      tags: ["仓位建议", "宏观驱动", "失效条件"],
      src: "X 原文 @KillaXBT · 2106540270854582439"
    },
    {
      date: "2026-10-04",
      title: "首次引入宏观锚点：中期选举后 BTC 历史走弱",
      quote: "如果 $BTC 就这么一路涨到中期选举呢？每一个中期选举周期，我们都看到 BTC 在选举之后表现不佳。那为什么不干脆等中期选举真正临近，再对价格行为做出反应？至少，我目前就是这么做的。",
      read: "这是他<b>第一次把「中期选举」当成行情变量写进剧本</b>——此前他的驱动项只有均线/结构、月开季节性、流动性和机构资金。改动的是 09-27「周期低点已确认、熊市只剩 10 天」之后的<b>中短期节奏</b>：他现在承认短期可以继续涨（甚至一路涨到选举），但把选举之后标为偏空窗口。与同日那条「对冲推迟到选举后」互相咬合，等于给这轮上涨挂了一个<b>日历上的上限</b>。失效条件：若中期选举结束后 BTC 并未走弱、反而继续创高，这条历史规律本轮失效，届时他的「宏观锚点」需要重新找。",
      tags: ["宏观驱动", "周期判断", "失效条件"],
      src: "X 原文 @KillaXBT · 2106539562814030174"
    },
    {
      date: "2026-10-04",
      title: "复盘踏空者：等回踩 2–3% 的人全被抢跑",
      quote: "事后诸葛亮真让人难受。人们一直在等 $BTC 再低 2–3% 才做多。结果他们全被抢跑了。现在这批人还坐在不敢置信里，在每一次回撤上都喊局部顶部。",
      read: "这是他 09-27 长文「你不会拿到理想回踩，提前建仓永远最聪明」的<b>实盘兑现版</b>——把「等再低 2–3% 的人被抢跑」当作自己那条论断的证据，属战绩复盘。同时它也构成对 09-27「等扫掉 PWL 才考虑做多」那条的<b>自我修正</b>：那次他说自己也会等一次扫前周低点，这条等于宣布那次等待没等到、提前进场的人赢了。失效条件：若价格确实回踩到 2–3% 更低的位置并站稳，这条「抢跑」叙事反转；结构参照仍是 84.6–85.2K。",
      tags: ["战绩复盘", "情绪指标", "趋势切换"],
      src: "X 原文 @KillaXBT · 2106478595669426372"
    },
    {
      date: "2026-10-04",
      title: "月度季节性序列：10 月见顶、更高低点见底？",
      quote: "12 月见顶，12 月见底。11 月见顶，11 月见底。10 月见顶，更高低点见底？",
      read: "改动的是 09-26「月度开盘枢轴、7 次里 6 次在月开附近拉升」那条的<b>论证素材</b>——他从单一的「月开拉升」扩展成一条<b>月度季节性序列</b>（顶底落在同一个月），用来支撑「10 月这一轮是更高低点」。含义：他把当前回调重新定义为<b>月内顶底同月结构</b>，而非趋势转弱，等于给「不创新低」再补一条统计依据。注意末尾是<b>问号</b>，性质是假设不是断言，证据强度明显低于他同期其他条目。失效条件：10 月收在 9 月低点 75.4K 下方，「更高低点」的假设即被证伪。",
      tags: ["基准剧本", "周期判断", "关键价位"],
      src: "X 原文 @KillaXBT · 2106434911779291244"
    },
    {
      date: "2026-10-03",
      title: "长文：机构资金已拿到结构确认，三笔多单全在",
      quote: "交易者有不同类型：技术确认派、突破派，还有宏观确认派。多数人要等趋势明确转向后才行动，而不是提前布局去吃掉更大的行情。我抓到了那次转向、吃到了 50% 的上涨。现在趋势已真正改变、价格在关键区域上方交易，此时还假设大型机构资金不会开始进场，就太天真了。人们为了一个小回撤去做空，而更大的资金已经拿到了结构确认。……牛市里的垂直吸筹（vertical accumulation）是真实存在的。假突破、反复被拒、压缩区间，就是为了让所有人难受、把脆弱仓位洗出去。到这个阶段，它更偏心理层面而非纯技术层面。趋势已经亮牌了。很难说严肃资金会把这里视为「过热」，而价格还在持续收复关键结构。62.6K 的多单还在。76.4K 的多单还在。83.5K 的多单还在。目标不变。短期震荡和小规模流动性猎杀，只是用来清掉那些用高 lev（原文末尾截断）。",
      read: "改动的是 10-03「年内上限 97K + 区间震荡」那条的<b>资金面依据</b>——他第一次把「机构/大资金进场」写进论证，并把当下的压缩、假突破、反复被拒定性为<b>垂直吸筹</b>，属于典型的事前免责式解释框架（回调与横盘都被预先解释成洗盘）。更关键的是他重申三笔多单（62.6K / 76.4K / 83.5K）一个没动、目标不变，说明 10-03 的改口<b>只改了说法、没改仓位</b>。失效条件：若价格在关键区域上方继续被反复拒绝并最终有效跌破 84.6K → 80–83K，「机构已结构性确认」这一前提落空。",
      tags: ["仓位建议", "宏观驱动", "趋势切换"],
      src: "X 原文 @KillaXBT · 2106402732030546312"
    },
    {
      date: "2026-10-03",
      title: "纯情绪读数：跌的时候庆祝的人比涨的时候还多",
      quote: "有意思的时刻。我看到价格下跌时庆祝的人，比上涨时还多。",
      read: "又一次逆向情绪读数，对象是<b>「盼跌情绪」的浓度</b>——与他 09-25「所有人都想要更低的价」、09-28「希望这是假突破的人越多、说明空仓的人越多」同源，属于同一框架的第三次取样。本条无点位、无新条件，作用只是把「多数人空仓 / 盼跌」这个前提再确认一次。无失效条件（不含任何价位）。",
      tags: ["情绪指标"],
      src: "X 原文 @KillaXBT · 2106102155589369899"
    },
    {
      date: "2026-10-03",
      title: "年内上限首次改口：最高看 97K，投降底 74–77K",
      quote: "我看 $BTC 最高会走到 97K。我认为我们可能在今年剩下的时间里继续在 97K 下方区间震荡。话虽如此，这一轮周期已经比前几轮走得更抛物线、也更早。80K–83K 是关键，它比大多数人意识到的更重要：如果我们有效跌破它，下一个可能区域是 74K–77K。那很可能是最终走向 97K 之前的投降底。不过，如果这股动能延续下去，回撤可能会浅得多，也许只到低 80K 区，然后再走出下一腿。这就是我持有那笔 83.5K 十倍多单的原因，我公开放过话。如果我们真的在 Q4 出现某种形式的投降，我很可能会加更多 BTC 现货和多单。",
      read: "改动的是他 09-27「到 126K 的整段上涨应该是猛烈且快速的」那条的<b>时间表</b>——第一次给出<b>年内上限 97K</b>，等于把 126K 明确推到今年之外，短期从「一杆子到 126K」降级为「今年在 97K 下方震荡」。同时把 09-30 的「82.5K 确立低点」重新定性：它不再是底，而是<b>防守线</b>，有效跌破后的下一站是 74K–77K，并首次把那里命名为「投降底」。但注意他<b>并未减仓</b>——反而说 Q4 若真投降会加更多现货与多单，等于把下行当成加仓机会，相比 09-29「不接 80K 下方」是明显放宽。失效条件：<b>80K–83K 被有效跌破</b>，则「低 80K 就止跌反身」的浅回撤分支作废，目标切换为 74K–77K；反之若真在低 80K 反身向上，97K 这一段才成立。",
      tags: ["目标价", "关键价位", "失效条件"],
      src: "X 原文 @KillaXBT · 2106071714186866781"
    },
    {
      date: "2026-10-02",
      title: "85K 关口已翻多：站住看 89–90K+，丢 84.6K 就扫 80–82K",
      quote: "BTC 到了做决定的时候。我们已经翻上了 85K 这道关口。现在关键是要守住它，才能看到向 89–90K 以上的推进。有一点我可以向你保证……如果我们丢掉 84.6–85.2K 这个区域，向 80–82K 的一次扫针完全不会让我意外。",
      read: "这是对同日早些那条「85.2K 是当前壁垒」的<b>结果确认</b>——原来给的是两条互斥路径（收复 85K → 挤压回高位 / 丢 82.5K → 回测投降插针区），这条宣布<b>收复路径已触发</b>，并把上沿目标从含糊的「高位」具体化为 89–90K+。同时新增一条更近的防守线 <b>84.6–85.2K</b>（比他 09-30 用的 82.5K 高了约 2.5K），说明他把失效参照整体上移了。失效条件：跌回 84.6K 下方即触发「80–82K 扫针」情景，89–90K+ 的推进路径暂告失效。",
      tags: ["关键价位", "趋势切换", "失效条件"],
      src: "X 原文 @KillaXBT · 2106043183738110004"
    },
    {
      date: "2026-10-02",
      title: "纯态度条：市场很简单，是人的心理把它搞复杂",
      quote: "就像我说的，它真的就这么简单。那么多自称『天才』的人，试图去战胜一个简单的市场。心理是交易中最重要的部分。在 X 上花 5 分钟你就会发现，很少有人具备驾驭它的纪律或情绪控制力。",
      read: "纯态度条，<b>无点位、无新条件</b>。与他 09-25「别把牛市里的事情搞复杂了」、09-30「扫针就是做多，真的就这么简单」同源，把「简单执行、别自作聪明」的方法论再强调一次。无失效条件。",
      tags: ["情绪指标"],
      src: "X 原文 @KillaXBT · 2106027422605021258"
    },
    {
      date: "2026-10-02",
      title: "月开剧本第三次兑现，但他同步改口「要谨慎、别贪」",
      quote: "不是一次，不是两次，而是三次，我都从月度开盘里吃到了机会。这一次同样出现了月开拉盘并扫掉高点。不过我仍会保持谨慎——我们需要看到的是一次真正的收复并站在这批高点之上，而不是又一次单纯的扫针。否则我们仍然只是在同一个既有区间里交易。跟随这个设置本可以吃到 $BTC 约 4% 的一波行情。别贪。从这里我们依然可能继续区间震荡，尽管那不是我最想看到的结果。",
      read: "改动的是 09-29「跌进月开 → 历史上偏多」那条的<b>完成度与权重</b>——从「剧本已触发」升级为「已第三次兑现（月开拉盘并扫高点）」，算一次战绩复盘；但同一条里他把「月开拉盘 = 看涨」降级为<b>「还要看到真正收复并站稳，否则仍只是区间内的一次扫针」</b>，并首次主动说「别贪」「还可能继续区间震荡」。这与同日 97K 上限、区间震荡的判断互相印证，等于把月开的信号强度从趋势级下调为短线级。失效条件：若月开拉盘后站不稳这批高点上方，这条统计规律只能算一次约 4% 的日内机会，不构成趋势信号。",
      tags: ["基准剧本", "关键价位", "战绩复盘"],
      src: "X 原文 @KillaXBT · 2106000689386197502"
    },
    {
      date: "2026-10-02",
      title: "回踩要「凶狠且迅速」地接：首次给出 7-10 倍与 82.5K 偏离假设",
      quote: "看着 BTC 涨而自己没上车，没有比这更糟的感觉了。不幸的是，尽管趋势已经明显转向，我们仍处在「怀疑」的峰值阶段。任何下行都应该凶狠而迅速地买入。保持低杠杆。……2023 年那轮牛市里，如果你在每一次扫前低时做多，最深的一次偏离也只有 8%，有些只有 4-5% 就推回去了。这意味着在前期低点附近用 7-10 倍做多、去做向历史新高的那一段，相对是安全的，前提是风险管理得当。这是数学。我们当前确立的低点是 82.5K，按历史行为，预期偏差应该很小。",
      read: "改动的是 09-30「扫针就是做多」那条的<b>执行细节</b>——从「什么价位接」升级到「用什么杠杆接」：他第一次给出具体倍数 <b>7-10 倍</b>，并以自设的 82.5K 确立低点作为偏离参照，用 2023 年牛市「每次扫前低最浅偏离 4-5%、最深 8%」当数学依据。同时把 09-30「叙事偏空反而更可能反向走高」这句情绪判断，落成了一条可验收的操作指令。失效条件：<b>82.5K 被有效跌破</b>——按他自己给的 8% 上限推算约 $75.9K，与他口中的九月低点 75.4K 基本是同一片区域；一旦回落进下方框体，这条「偏离很小」的假设会连同 7-10 倍仓位一起失效。",
      tags: ["仓位建议", "关键价位", "失效条件"],
      src: "X 原文 @KillaXBT · 2105754694308028822"
    },
    {
      date: "2026-10-02",
      title: "首次给出明确关卡：85.2K 是当前壁垒，站不住就往下趋势",
      quote: "BTC 当前壁垒是 85.2K。我们在它下方持续压缩、多次被拒。昨天插针的流动性已经被扫掉了，所以如果不能收复并站稳 85K 上方，我预计价格会重新向下趋势。现在看来 BTC 被压在一个很紧的区间里蓄流动性、让大多数人难受。如果扫掉 82.5K，我会转而寻找进入下方框体的走势，回测投降插针区。反过来，如果强势收复 85K，我认为会激进挤压回高位。",
      read: "这是 09-30 那条「叙事偏空、反向走高」的<b>条件化版本</b>——他第一次把方向拆成两条互斥路径并各自给出触发价：<b>站稳 85K -> 挤压回高位</b>；<b>丢 82.5K -> 回测投降插针区</b>。改动的是 09-30 那条的含糊之处：「反向走高」不再是默认结论，而要等收复 85K 才成立。与之配套的是他同批另一条里 7-10 倍的接多指令——两条合起来，等于把 82.5K-85.2K 定义成一个必须选边的压缩区。失效条件：若在 85K 下方被反复拒绝而他仍持多仓，压缩大概率向下解决；反之若放量收复 85K 上沿，「回测投降插针区」这条路径当场作废。",
      tags: ["关键价位", "趋势切换", "失效条件"],
      src: "X 原文 @KillaXBT · 2105742119214166309"
    },
    {
      date: "2026-10-02",
      title: "长周期目标首次量化：160-180K，并断言五位数 BTC 是最后一次",
      quote: "记住是谁第一个说的。这是你最后一次能在 100K 以下买到 BTC 了。回看的话 84K 很便宜。如果 -54% 就是本轮的底部，那下一轮熊市大概率只有 -40%。也就是说如果我们走到 160-180K，你再也买不到五位数（低于 100K）的 BTC 了。所以我建议你趁还来得及之前重新评估。",
      read: "改动的是他此前只说到「ATH / 高位」的模糊表述——本轮第一次给出<b>具体长周期目标区间 160-180K</b>，并把论证从「均线 / 结构」换成<b>周期回撤幅度递减</b>（-54% -> -40%）。同时把 84K 直接定性为「便宜」，等于给 10-01 那笔 83.5K 多单补了一条长周期持有理由，而不是只靠短线结构。失效条件：整条推理的前提到「本轮底部已成立（-54%）」上——若 82.5K 失守并跌破九月低点 75.4K，-54% 这个前提本身就不成立，160-180K 随之作废。这是一条<b>依赖前史的历史类比判断</b>，不是价格结构判断，可证伪点比前两条远得多。",
      tags: ["目标价", "周期判断", "基准剧本"],
      src: "X 原文 @KillaXBT · 2105711354665714108"
    },
    {
      date: "2026-10-01",
      title: "纯态度条：趋势是你的朋友",
      quote: "你想要的一切都在恐惧的另一面。趋势是你的朋友。",
      read: "纯态度条，<b>无新增点位与条件</b>，是把同日「结构已转看涨」的结论在情绪层面再确认一次。无失效条件。",
      tags: ["情绪指标"],
      src: "X 原文 @KillaXBT · 2105665775814250963"
    },
    {
      date: "2026-10-01",
      title: "承认结构转多：周线月线阻力已收在上方，但预警先反手猎杀杠杆",
      quote: "在扫掉 75.4K 附近的九月低点之后，我们收在了此前的周线与月线阻力上方。结构是看涨的。正因如此，我们可能看到一次快速的向下猎杀、打掉一些杠杆，然后再向上推。这通常就是趋势转换后的那根收盘之后会发生的事。",
      read: "改动的是他对九月低点 <b>75.4K</b> 的定性——从「被打穿的支撑」改写成「被扫掉、并借此完成趋势转换」，据此宣布<b>结构转为看涨</b>。这是本轮第一次出现「结构看涨」的正面表述（此前是 09-30 那条高周期均线论证）。同时他提前为一次向下插针<b>预留了解释权</b>（扫杠杆），手法与 09-30「季线月线收盘会有操纵行情」同源。失效条件：<b>回踩不能跌破 75.4K</b>；一旦回到该区域下方，那就不是「扫杠杆」而是趋势转换失败，他刚宣布的「结构看涨」直接作废。",
      tags: ["趋势切换", "关键价位", "失效条件"],
      src: "X 原文 @KillaXBT · 2105627665772245232"
    },
    {
      date: "2026-10-01",
      title: "月开季开收盘前改口：看空叙事转浓，反向走高概率反而更大",
      quote: "BTC 拉了 3%，然后回吐了几乎 80% 的涨幅。临近月度与季度收盘，市场叙事现在明显更偏空、而不是偏多。这让反向走势更有可能——尤其是如果我们先扫掉流动性、而结构继续保持。我仍然持有最近分享的那笔 83.5K 十倍多单。",
      read: "这是本轮唯一一条把「叙事偏空」直接当作看涨理由的短线表述，也是他第一次把方向判断挂到<b>月线/季线收盘</b>这个具体节点上。改动的是 09-30「下周 BTC 突破 87K 上方」那张时间表——现在多了一个前置条件：<b>先扫流动性、再反向走高</b>，收盘前的走势被定义为「叙事」而非「结构」。同时他<b>重申仍在这笔 $83.5K 的 10 倍多单里</b>，确认 09-24 那笔激进仓位到 10-01 凌晨未动。失效条件：若扫完流动性后结构没能保持（例如跌破 $83.5K 成本线并收在下方），「反向走势」即落空，而这笔 10 倍仓位同时进入强平压力区。",
      tags: ["仓位建议", "情绪指标", "关键价位"],
      src: "X 原文 @KillaXBT · 2105375753789378612"
    },
    {
      date: "2026-09-30",
      title: "给 Q4 创新低的人下判决：所有高周期均线都指向底部已成",
      quote: "我真心为那些还在押注 Q4 创新低的人感到难过。从价格行为的角度看，每一条关键的高周期均线都指向 BTC 的底部已经形成。不是季节性因素，是价格本身。到这个阶段还认为不是，纯粹是自我安慰。",
      read: "这是他对 09-18 基准剧本里「2026 年摸不到 10 万、真正新高等 2027」那条最直接的否定。改动的是<b>底部判定的依据</b>——从「周期天数 / 季节性」换成<b>高周期均线的价格行为</b>，方法论上更可证伪，但也意味着他把论证锚点交给了他自己的图表。同时把 09-26 单一结构点「周线更高高点」扩展成「所有关键 HTF 均线」。失效条件：锚点既已押在周线级别均线上，<b>周线均线被跌破（对应价格约 $80K 下方）</b>就是这条判断的硬失效线；若 Q4 真的出现新低，这条「纯粹是自我安慰」的措辞会构成他最直接的一次翻车记录。",
      tags: ["周期判断", "趋势切换", "失效条件"],
      src: "X 原文 @KillaXBT · 2105313570669941147"
    },
    {
      date: "2026-09-30",
      title: "季线月线收盘会有操纵行情，但明确不改多头立场",
      quote: "季度和月度收盘。当然会有各种操纵和假动作。但这不影响一个事实：我在 BTC 上依然坚定做多。耐心在这场游戏里就是一切。当你做的是高周期，大部分低周期的价格行为都只是噪音。",
      read: "这条等于给收盘窗口的短线波动<b>提前预留了免责空间</b>——他把季线/月线收盘可能出现的下插定性为操纵（fuckery），宣告收盘前的下跌不算数。改动的是 09-30「扫针就是做多」那条的<b>可验收性</b>：只要波动落在这个窗口内，他都可以归入噪音，外界很难拿单日价格行为去证伪他。失效条件：若季线收盘后价格没有快速收复、而是延续下行（跌破 $80K 并周线收在下方），「低周期都是噪音」就不再是解释而是借口。",
      tags: ["周期判断", "情绪指标", "仓位建议"],
      src: "X 原文 @KillaXBT · 2105293060292657530"
    },
    {
      date: "2026-09-30",
      title: "补理论：大级别回调只发生在价格发现阶段，现在不是",
      quote: "更大级别的回调，发生在 BTC 处于价格发现（price discovery）阶段的时候。我们现在不在那个阶段。有时候把事情说得这么简单，才是在趋势市里赚到最多钱的方式。",
      read: "这是对 09-27「本轮牛市最大回撤只有 10%–15%」那条的<b>理论补丁</b>——此前他只有结论（波动率压缩、回撤上限 15%），这条第一次给出原因：因为价格还没进入价格发现（历史新高区）。含义很关键：<b>一旦 BTC 进入价格发现（约 $126K 以上），他这套浅回撤框架就自动失效</b>，深回撤会被他视为合法。等于他提前为「新高之后的大回调」打了预防针，短期这条可以用来解释当下为什么不跌。失效条件：在尚未创新高的这一段里出现超过 15% 的回撤（即跌破约 $74K），该理论即不成立。",
      tags: ["失效条件", "周期判断", "趋势切换"],
      src: "X 原文 @KillaXBT · 2105260937011941474"
    },
    {
      date: "2026-09-30",
      title: "重申多头原则：牛市里就是在扫针之后做多",
      quote: "在 BTC 牛市里，你就是在扫针（sweeps）之后做多。真的就这么简单……但话又说回来，总有人能找到卖出的理由，对吧？我是说，拜托……你不会天真到那个地步吧。",
      read: "这条把他 09-26「牛市不需要健康回调」和 09-27「扫掉前周低点才是我会考虑做多的位置」并成了一句原则：<b>回调不是风险，而是入场机会</b>。改动的是 09-25「唯一做空位」框架的残余——在低 90K 之前，<b>扫针同样只被他当成做多的理由，而不是做空的理由</b>。失效条件：若扫针之后价格无法收复该位置、而是持续下行（例如跌破 $80K 并收在下方），「扫针=做多」的前提即失效。",
      tags: ["仓位建议", "趋势切换", "情绪指标"],
      src: "X 原文 @KillaXBT · 2105044956813648079"
    },
    {
      date: "2026-09-30",
      title: "给出时间+价位：下周 BTC 突破 $87K 上方",
      quote: "翻译一下：下周 BTC 突破 87K 以上。（引推正文为二进制编码 01101110 01100101 01111000 01110100 00100000 01110111 01100101 01100101 01101011，即英文 next week）",
      read: "这是本轮唯一把<b>时间窗（下周）和价位（$87K 上方）绑在一起</b>的一条，也是他少见的短期择时表述。改动的是 09-27「本腿理想延伸 $92K–$94K」的性质——$92–94K 仍是更远的目标，但短期要先过 $87K 这道关，等于<b>把一个中期目标拆成了两步</b>。失效条件：下周没能站上 $87K，或先跌回 $80K 下方，这张时间表即落空。",
      tags: ["目标价", "关键价位", "周期判断"],
      src: "X 原文 @KillaXBT · 2105005838540915006"
    },
    {
      date: "2026-09-29",
      title: "月开剧本已触发：跌进 10 月开盘，历史上偏多",
      quote: "套路你懂的。从 3 月以来，往下砸进一个全新的月度开盘，对 BTC 一直是个看涨信号。看看这次会不会不一样。我们正在形成一套清晰的看空叙事。",
      read: "这条把 09-26「月度开盘枢轴」从<b>条件假设变成了已触发状态</b>：当时的说法是「如果是跌进 10 月，我会预期之后有一波上行」，现在确认走的正是「跌进月开」这条路径。改动的是他对当前回调性质的定性——不是趋势转弱，而是<b>月开前的季节性砸盘</b>。他补的那句「我们正在形成一套清晰的看空叙事」，等于把市场的看空叙事收编进自己的看多框架，判断依据仍是统计规律而非价格结构。失效条件：10 月开盘后一周内价格未能转为上行、并收在 $80K 下方，则「跌进月开=看涨」的历史规律这一轮失效。",
      tags: ["基准剧本", "关键价位", "情绪指标"],
      src: "X 原文 @KillaXBT · 2104958759470592403"
    },
    {
      date: "2026-09-29",
      title: "逐条反驳 2023 分形：现在是周线更高高点，性质不同",
      quote: "既然所有人都错过了「Q4 底部」，这个剧本就成了大家现在盯着的、盼着的新共识情景。……2023 年 BTC 涨到 25K 时，它形成了等高点之后就拒绝了：没有有效收在该位上方，没有在 25K 上方建立显著高点，几乎是立刻被拒绝，只是在局部更低高点上方偏离了一下、形成等高点。而眼下 BTC 已经形成了周线更高高点——这是完全不同的市场结构转变。我们现在是在先前的翻转高点上方区间整理，动力学跟 2023 年完全不同。另外，那一轮熊市回撤约 77%，这一轮约 54%。如果套用同样的递减回报、更浅回踩逻辑，本轮牛市的最大回调大概会在 10%–15%，一路直到 126K。10% 的回调把 BTC 带到约 78K，15% 到约 74K。所以即使完全照搬这个分形，也不一定会出现 2023 年那种跌破低点的有效扫针。……不管怎样，我确信大量观望的交易者会很乐意拿到那个他们错过的区域来建多。市场有个有趣的方式，就是不给人想要的东西。在 OI 重置、价格在先高上方区间整理的背景下，市场在我看来是健康的。这不是我布局的情形——我仍然看向 90K 那一带。",
      read: "这是本轮<b>信息量最大的一条</b>，他正面拆解了空头最常引用的 2023 分形（先砸破前影线低点再拉升）。改动的是 09-24 那条剧本的<b>概率权重与量化下沿</b>：原文说「若 $87K 成局部高点、深回撤到 7 万低段，那里就是地板」，这条把同一路径明确成 $78K（−10%）与 $74K（−15%），并直言<b>即使回撤到前区间高点下方，也不必出现跌破低点的扫针</b>。同时他把「人人都想要的那个低点」直接定性为不会兑现，属于典型的逆向情绪论。失效条件：若回撤幅度显著超过 15%（即跌破约 $74K），或周线更高高点被有效跌破，整条「递减回报 + 更浅回踩」框架作废。",
      tags: ["趋势切换", "失效条件", "周期判断"],
      src: "X 原文 @KillaXBT · 2104946217700446260"
    },
    {
      date: "2026-09-29",
      title: "对冲位由 $93.6K 放宽到「低 90K」，明确不接 80K 下方的机会",
      quote: "最大的痛感，就是看着价格一路走高而你在场外。我在 BTC 上寻找的是低 90K 区间的对冲机会。在我看来，中间的一切都是噪音。我没兴趣去捕捉可能出现的、跌破 80K 的那一段行情，我更愿意顺着趋势做。我看到很多人把当前价格行为跟 2023 年周期作比较——那时 BTC 先砸破前一根影线低点、再往上推，对应到这里就是 75K 之后 90K。这确实在可能性范围之内，但我不会对这个想法死心塌地。周期在逐步移位，这一轮熊市在下跌 54% 之后见底，上一轮大约 76%，动力学已经实质不同。这只是我个人的预期。",
      read: "这条<b>修改了 09-25 的对冲计划</b>：当时是「把对冲空单入场位上移到 $93.6K」，现在放宽成「低 90K 区间」——对冲带整体下移，说明他不再死等 $93.6K 这个精确点位，而是接受更早的 90–93K。更关键的是新增了一条明确的不做项：<b>他公开放弃捕捉「跌破 80K」的那段行情</b>，等于把 09-24 剧本里「回撤到 7 万低段再加仓」的路径主动删掉。失效条件：若价格真的先跌破 $80K，他这条「只顺势、不接下方」的取舍会明显跑输给自己留了低位加仓的版本；反向的失效线是他自己给的 $74K（−15%）。",
      tags: ["关键价位", "仓位建议", "失效条件"],
      src: "X 原文 @KillaXBT · 2104909717675929791"
    },
    {
      date: "2026-09-29",
      title: "纯态度条：把 believe 写成 bullieve",
      quote: "要成就伟大的事，我们不仅要去行动，还要去梦想；不仅要去计划，还要去「bullieve」。",
      read: "纯情绪表态，把 believe 拼成 bullieve（bull + believe），<b>无新增点位、无新增条件</b>。作用只是把同期「扫针就是做多」「月开历史偏多」的多头口径在态度层面再确认一次，不构成独立信号。无失效条件（本条不含任何价位）。",
      tags: ["情绪指标"],
      src: "X 原文 @KillaXBT · 2104891198838362566"
    },
    {
      date: "2026-09-29",
      title: "自认这腿风险最高：只等 6% 回撤就上 10 倍杠杆",
      quote: "我觉得很有必要把话说清楚：这一笔多单比我之前分享过的那些风险更高。BTC 已经从低点涨了 50%、刚形成周线更高高点，而我只等一个 6% 的回撤就进场。我用 10 倍杠杆来放大仓位，是在我认为可能正在筑底的阶段——因为我预计本轮周期的跌幅只有 10% 到 20%。我的逻辑很简单：如果第一笔 10 倍多单错了，它的失效本身就完成了使命，让我有机会在更低位再入。从数学上说，那一笔再入更可能是能一路拿到 ATH 的那一笔，前提是宏观底部已经成立。我从 62K 的 2 倍波段多单、和从 76.4K 的延续多单，在我看来明显安全得多。但牛市里的回撤可以很浅，随着周期推移，想精准择时抓到底部越来越难。执行这套方法能保证：如果趋势真的切换了，我全程都在场。这是数学方法，不是技术方法。要说明的是，这笔延续多单风险更高、更激进。但手上浮盈有 25 万，我准备承担更激进的风险去把收益做大。",
      read: "这是他<b>第一次给激进仓位做风险披露</b>，也把 09-24「启动 10 倍多单」的隐含假设摊开：他预期本轮只有 10–20% 的跌幅，所以用 10 倍杠杆放大仓位、并以「第一笔失效即换更低位再入」取代分批建仓。改动的是 09-25「每周部署 10%、两个月建满」的<b>匀速定投口径</b>——真实做法是跳点式加杠杆，不是摊平成本。同时新增一个可核验的数据点：他自称浮动盈亏 25 万美元（说明仓位规模不小）。失效条件：第一笔 10 倍多单被打掉后价格继续下破、不给更低的站得住的位置，则「再入即持有到 ATH」的数学前提不成立；另一条更硬的失效线是他自己给的假设——若本轮跌幅明显超过 20%，整条杠杆化逻辑作废。",
      tags: ["仓位建议", "失效条件", "周期判断"],
      src: "X 原文 @KillaXBT · 2104705982496456960"
    },
    {
      date: "2026-09-29",
      title: "第三笔多单开在 $83.5K（10 倍）：62.6K → 76.4K → 83.5K",
      quote: "我在 62.6K 做过多。我在 76.4K 做过多。现在我又在 83.5K 用 10 倍杠杆做多。所有仓位完全打开。什么都没变。这是一套激进的策略，但鉴于我确信 BTC 的底部已经形成，我认为它是能奏效的。是时候去折腾一下、看看结果了。",
      read: "这条首次披露了他 09-24 那笔「10 倍多单」的<b>实际入场价 $83.5K</b>，把此前只有方向、没有价位的实盘动作补成了可核验的点位。改动的是入场结构：不是 09-25 说的「每周 10% 匀速建仓」，而是三个跳点（$62.6K / $76.4K / $83.5K），并且明确「所有仓位完全打开」= 已无余量。对判断他可信度最有用的一点是：<b>$83.5K 就是他自己的成本线</b>，跌回该位下方并站不住，就是他这套剧本的第一次真实考验。失效条件：按 10 倍杠杆计算，从 $83.5K 起算约 −10% 即为强平区（约 $75K 一线），因此跌破 $80K 并收在下方，这笔仓位的容错空间基本消失。",
      tags: ["仓位建议", "关键价位", "战绩复盘"],
      src: "X 原文 @KillaXBT · 2104688297494917542"
    },
    {
      date: "2026-09-29",
      title: "只放图不解释：BTC 周线下降楔形",
      quote: "不作评论。BTC 的周线下降楔形。",
      read: "周线下降楔形是看涨反转形态，与他 09-26「周线更高高点已形成」互为印证，也把 09-27「周线 50/100 翻转就做多」的条件从「等翻转」提前到「形态已具备」。但要注意：<b>下降楔形描述的是此前那段下跌收敛过程</b>，属于事后确认而非新的前瞻信号；他刻意「不作评论」，是把结论完全交给图形。无可验收的新点位。失效条件：楔形上沿被跌穿、周线收在 $80K 下方，形态判定作废。",
      tags: ["趋势切换", "周期判断"],
      src: "X 原文 @KillaXBT · 2104646481567461508"
    },
    {
      date: "2026-09-29",
      title: "重申到 126K 还有钱赚，但别当过度杠杆的赌徒",
      quote: "永远不要听别人说它「看起来太容易」所以不会发生。有时候它真的就是这么容易。不要把高周期的仓位管理搞复杂。只要你不是一个过度加杠杆的赌徒，到 126K 这一段还有的是钱可赚。",
      read: "表面看是复读 09-26 长文，但多了一句此前没有的<b>风险分层</b>：同一段行情里，结果由仓位规模决定，而不是由方向决定。这与他同日凌晨那条「这笔多单风险更高」放在一起读，含义很明确——<b>他知道自己站在激进的一侧，并提前把「别学我上杠杆」说出口</b>，属于对追随者的免责式提示。无可验收的新点位。失效条件：对应的仍是 $80K 结构线。",
      tags: ["仓位建议", "情绪指标"],
      src: "X 原文 @KillaXBT · 2104615175395668464"
    },
    {
      date: "2026-09-28",
      title: "下一轮熊市或再也回不到 10 万下方（顶部估 160K–180K）",
      quote: "有件事值得深思……下一轮 BTC 熊市，我们可能再也见不到 10 万美元下方。本轮只比前高偏离了 16%。如果 BTC 在 16 万到 18 万见顶，即便出现类似幅度的偏离，下一轮熊市的低点也会保持在 10 万上方。这很可能真的是你最后一次能在 10 万以下买到 BTC。",
      read: "这是他第一次给出<b>顶部区间估计 160K–180K</b>——此前只说长线目标 160K，既没有上沿，也没有推算过「见顶之后下一轮会落在哪」。改动的是 09-18 基准剧本里的时间锚：长线叙事从「这一轮能到多少」推进到「这一轮之后你还有没有上车机会」，副作用是把「嫌贵不买」直接定性为永久性错误。失效条件：本轮顶部显著低于 160K（例如 $126K 附近就转熊），或下一轮熊市低点跌破 10 万，该推算即作废。",
      tags: ["目标价", "周期判断", "基准剧本"],
      src: "X 原文 @KillaXBT · 2104584345407136029"
    },
    {
      date: "2026-09-28",
      title: "希望这是假突破的人越多，说明空仓的人越多",
      quote: "有那么多人希望这只是一次向上偏离高点、好让价格重新跌回 7 万下方，这件事本身就很说明问题。它暴露出还有多少人完全没有建仓。",
      read: "又一次逆向情绪读数，但观察对象换了：从 09-25 的「所有人都想要更低的价格」，变成了<b>「希望这是假突破」的心理人数</b>——他把「假突破论」的流行程度直接当成空仓比例的代理指标。改动的是他对潜在回调性质的定性：跌回 7 万下方不是行情的需要，而是空仓者的一厢情愿。失效条件：价格真的跌回 7 万下方，那这套「空仓者自我安慰」的框架就反过来被证伪。",
      tags: ["情绪指标", "趋势切换"],
      src: "X 原文 @KillaXBT · 2104554849014784430"
    },
    {
      date: "2026-09-28",
      title: "本腿理想延伸 $92K–$94K，$89.2–90.6K 是潜在拒绝区",
      quote: "整体来看，这个计划走得非常漂亮——从吸筹区突破、在前高下方盘整，然后扩张到下一个目标。除了 89.2K 到 90.6K 是一个不错的小周期区域、可能看到拒绝之外，这一段行情理想的延伸位大约在 92K 到 94K。如果这是一次真正的推动式突破、我们正在转入更高的区间，我会预期动能继续，而不是在这里形成新的区间。市场应该利用这股动能继续推高。时间比预期更快，但我已经为这波行情建好仓位，所以乐意接受。",
      read: "这条把他 09-25 提出的<b>唯一做空位 $93.6K</b> 的性质改掉了：同一个价位区间现在被描述为「本腿的目标延伸区」，而可能的拒绝区被下移到 $89.2–90.6K 并降级为小周期（LTF）。等于他<b>把 126K 的长线结论拆出了一个可验收的中途目标</b>，同时承认短期有回落可能。失效条件：若在 $89.2–90.6K 遭拒后跌回 $86K 下方并横住，则「推动式突破、动能继续」被证伪。",
      tags: ["目标价", "关键价位", "趋势切换"],
      src: "X 原文 @KillaXBT · 2104300431920833008"
    },
    {
      date: "2026-09-28",
      title: "周线 50/100 翻转即做多，目标 160K，不在此处做空",
      quote: "有疑问的时候，就把图拉远。一旦周线 50/100 翻转，你就是做多。把图拉远看，在这些低位区做短线空头显得很可笑。想象一下一两年后回头看，BTC 在 160K，而你意识到自己是在这里做空——那画面真是让人心酸。我会用多单敞口 + 现货敞口跟随这波上涨，我相信靠「做得更少」就能跑赢 99% 的人。",
      read: "他把 06-04 那条置顶的<b>长线目标 $160,000 重新挂回当前动作</b>，并明确公开自己现在是「多单 + 现货」双敞口、以年为单位持有。改动的是 09-25 自设的对冲空单框架——他说在这些低位做空「很可笑」，等于主动削弱自己那套 $93.6K 对冲计划的优先级。失效条件：周线 50/100 未完成翻转且价格跌回 $80K 下方，「拉远看只会涨」即不成立。",
      tags: ["趋势切换", "目标价", "仓位建议"],
      src: "X 原文 @KillaXBT · 2104257952446095412"
    },
    {
      date: "2026-09-27",
      title: "区间中段顶部：扫 PWL 才做多，明确不追空",
      quote: "区间中段的顶部……BTC 被夹在两个小周期流动性簇之间。如果我们扫掉 PWL（前周低点），那才是我会考虑做多的位置。反过来说，如果我们没有扫、而是开始重新推向高点，我个人不会考虑做空。月线收盘与季度收盘临近，猎杀行情有可能出现。",
      read: "这是他在 9 月这一腿里<b>第一次给出「向下扫流动性才建多」的具体前置条件</b>，与他 09-26 长文「不会给你理想回踩、提前建仓最聪明」的口径出现松动——他承认当前位置不是理想入场点，愿意等一次扫前周低点。同时「不会做空」再次确认 $93.6K 之前的空头立场没有启用。失效条件：若价格不扫 PWL 而直接向上突破 $90.6K，这条「等扫 PWL」的计划就落空（他自己在长文里已事先提示过这个风险）。",
      tags: ["关键价位", "仓位建议", "失效条件"],
      src: "X 原文 @KillaXBT · 2104228076003455382"
    },
    {
      date: "2026-09-27",
      title: "本轮熊市只跌 53%，25–30% 的深回撤不会再来",
      quote: "这轮熊市我们只跌了 53%。所以你以为前几轮牛市里那种 25–30% 的回撤还会出现？它们不会来了，波动率压缩。研究一下——我的朋友们，那种东西已经成为过去。让我觉得好笑的是，还有人拿 2014 年或 2018 年跟现在比。那时 BTC 只是个几十亿美元的资产，今天市值约 1.5 万亿美元。你不能把一个已经发生如此动态转变的资产拿来做对比，这就像拿一只小盘股跟全球超大盘股比、还期待同样的表现。要我给真正有价值的建议？从这里一直到 126K，你不会拿到超过 15% 的下跌来建立你的多单。动力学变了，可惜人没变。",
      read: "他把 09-25 的「周期加速论」从<b>时间维度扩展到波动率维度</b>：不只是周期走得更快，回撤幅度也在系统性收窄（本轮熊市只跌 53%，牛市回撤上限 15%）。后果是把 09-24 那句「牛市最大回撤 10%–15%」从描述升级成<b>硬上限</b>，并直接否定 25%–30% 级别的深回撤，也否定用 2014/2018 做类比。失效条件：出现一次从高点算起超过 15%、并跌破 $80K 的回撤，「波动率压缩」框架即作废。",
      tags: ["周期判断", "失效条件", "趋势切换"],
      src: "X 原文 @KillaXBT · 2104193410781397075"
    },
    {
      date: "2026-09-27",
      title: "区间在更高处：人们还没准备好",
      quote: "区间在更高处，不是在更低处……人们还没准备好。",
      read: "一句话结论条，回应「等更低价」的普遍预期——他认为价格重心已经上移，下方回踩不会再来。无新增点位，作用是把同日凌晨「熊市只剩 10 天」的判断再压实一次。失效：跌回 83K 下方并站稳，则「区间更高」不成立。",
      tags: ["趋势切换", "情绪指标"],
      src: "X 原文 @KillaXBT · 2103972710783349085"
    },
    {
      date: "2026-09-27",
      title: "熊市只剩 10 天：周期低点已确认，除非跌破 $57K",
      quote: "这轮 BTC 熊市只剩 10 天了。对照前几轮周期，周期低点实际上已经确认——除非 BTC 在未来 10 天内以某种方式崩到 57K 以下。每一轮熊市周期持续 365 天，我们现在在第 355 天。结束了。",
      read: "这是他<b>时间维度最硬的一条判断</b>：给出 365 天熊市周期模型 + 当前第 355 天 + 明确失效位 $57K + 明确期限（约 2026-10-07 前），可以直接在日历上验收。注意它与 09-26「再也看不到 5 万 6 万」存在张力——$57K 才是他给的实际下限，比口头断言低约 3K。失效：10 天内跌破 57K，周期模型作废。",
      tags: ["周期判断", "失效条件", "基准剧本"],
      src: "X 原文 @KillaXBT · 2103916811011965125"
    },
    {
      date: "2026-09-27",
      title: "长文：牛市不需要「健康回调」，别等理想回踩",
      quote: "凭大量经验说一句——每一轮周期这种话我听得太多了：『它需要一次健康回调』『它需要吃掉下方的流动性』。我可以向你保证，它不需要。它不需要做任何事，不需要『健康』回调，更不需要吃掉我们下方的流动性。人们总是在市场处于『不敢相信』的阶段说这些话，而我们现在恰恰就在这个位置：不敢相信。现在大家唯一想要的就是一次像样的回踩、一次扎实的确认，然后才肯开心地做多。但很遗憾，这不是牛市运行方式的固有特征，尤其我们距离 126K 还远得很。到 126K 的整段上涨应该是猛烈且相对快速的。你不会拿到理想回踩，也不会拿到理想回踩确认——所以提前建仓永远是最聪明的。市场不会同情你，也不欠你任何东西。因为现在如果你还空仓，你只可能在做两件事：1）找理由说服自己为什么必须回踩来成全你的多单；2）因为踏空而赌气做空、盼着回踩到你的位置。而这正是 90% 的人会犯的错。低位多单往往会过早平仓——60K 的多单大概率早平了，76K 的多单也一样。你可能觉得从低点涨了 50% 市场就严重超多了，但你没算进市场在人们过早止盈时的自然再平衡，尤其我们只跌了 10 个月。牛市里不需要动脑子，你买回踩就行。就这么简单。",
      read: "这是他<b>最完整的方法论表述</b>，也是对「等回踩再进场」思路的直接反驳。核心三点：① 回调不是牛市的前提条件，别把它当必选项；② 到 126K 的上涨会是猛烈且快速的，不会给理想入场位；③ 低位多单早已止盈离场，市场并没有表面看起来那么多头。失效：价格跌破前周线区间高点（约 80–83K）并站稳下方，届时「不需要回踩」的论断不成立。",
      tags: ["仓位建议", "趋势切换", "情绪指标"],
      src: "X 原文 @KillaXBT · 2103885090984005875"
    },
    {
      date: "2026-09-26",
      title: "周线更高高点已形成 + 仓位完全重置：没有看空理由",
      quote: "它真的只能往上走。人们在把一件很简单的事搞复杂，因为如果它看起来太明显，那它就不会发生。我们已经形成了周线级别的更高高点，同时仓位已完全重置。真的没有任何看空的理由。",
      read: "把<b>技术结构（周线更高高点）+ 仓位状态（完全重置）</b>两个条件并列，给出「无看空理由」的结论，是他看多论证的最后一块拼图。失效：周线更高高点被跌破（约 80–83K 一带），技术条件即失效。",
      tags: ["趋势切换", "链上数据"],
      src: "X 原文 @KillaXBT · 2103861370298990720"
    },
    {
      date: "2026-09-26",
      title: "「顽固的空头从来不会变」—— 纯态度条",
      quote: "顽固的空头……他们从来不会变。懂的都懂。",
      read: "纯情绪表态，<b>无新增点位、无新增条件</b>。作用只是把同日「周线更高高点 + 仓位完全重置」的结论在态度层面再确认一次，不构成独立信号。无失效条件（本条不含任何价位）。",
      tags: ["情绪指标"],
      src: "X 原文 @KillaXBT · 2103829761789215163"
    },
    {
      date: "2026-09-26",
      title: "公开喊单复盘：$SOL 自公开入场已涨 75%",
      quote: "$SOL 自我公开分享入场以来已经涨了 75%。你可以看多也可以看空，但真正的问题是——你是在自己真正执行的那一刻就告诉了别人，还是等行情走完之后才发那些老生常谈的马后炮？",
      read: "这不是观点而是<b>可核验的战绩</b>：他公开喊过的 $SOL 入场单已浮盈 75%，用来反击事后诸葛亮式的分析。对你的意义在于，他的喊单带公开时间戳，可以回看验证——这是把他和纯嘴炮区分开的关键证据。同时也说明他<b>不只做 BTC</b>，山寨（SOL）同样在他的公开记录里。",
      tags: ["战绩复盘", "山寨"],
      src: "X 原文 @KillaXBT · 2103801206095360472"
    },
    {
      date: "2026-09-26",
      title: "周末拉升＝牛市特征，判断已在「抢跑下一腿」",
      quote: "一旦开始出现周末拉升，你就知道我们身处牛市。周末抢跑 legacy 资金，一直是个很有说服力的信号。",
      read: "这是他对 09-22「趋势已切向牛市」的<b>行为层面再确认</b>——从「事件驱动」转向「资金行为」佐证。失效条件很直白：若周末拉升后一周内被快速吞没、跌回 83K 下方，这条行为信号即作废。",
      tags: ["周期判断", "趋势切换"],
      src: "X 原文 @KillaXBT · 2103599172096258511"
    },
    {
      date: "2026-09-26",
      title: "月度开盘枢轴临近：7 次里 6 次在月开附近拉升",
      quote: "月度开盘枢轴快到了。7 次里有 6 次，BTC 都在月度开盘附近出现拉升，通常是因为此前的价格走势偏空。所以如果我们是跌进 10 月，我会预期之后有一波上行；若是涨进 10 月，我反而会更谨慎。",
      read: "他给了一个<b>可证伪的短期剧本</b>：跌进月开→看涨，涨进月开→谨慎。这改动了他的「单边顺势」口径，引入<b>节奏依赖</b>。失效条件：月开前后走势与统计规律背离（涨进月开却继续逼空）。",
      tags: ["关键价位", "基准剧本"],
      src: "X 原文 @KillaXBT · 2103550601774919856"
    },
    {
      date: "2026-09-26",
      title: "断言底部区间不可再现：5 万、6 万都不再会有",
      quote: "我们再也看不到 5 万了，也再也看不到 6 万了。能再看到 7 万下方都算你走运。BTC 每一次创出新的周线高点，趋势就发生转移——凭什么认为这次会不一样？",
      read: "这是他<b>对回撤下限最硬的一次封口</b>，等于把 09-18 基准剧本里「可能下探 7 万低段」的概率进一步压到接近零。失效条件：跌破前周线区间高点（约 80–83K 一带），届时「不再回到 6 字头」的断言直接破产。",
      tags: ["目标价", "失效条件"],
      src: "X 原文 @KillaXBT · 2103536004384878933"
    },
    {
      date: "2026-09-25",
      title: "杠杆已重置：该爆的都爆了，最大痛感在上不在下",
      quote: "该问的问题是：谁被打爆了？哪些仓位被平了？主趋势是什么？仓位是否真的过热？结论已经很清楚——追多的被清洗、杠杆多头投降、仓位重置，而高周期趋势仍为多头，且我们在 83K 下方盘整三周后仍站在前周线区间高点之上。需要清洗的仓位已经清洗完了，最大痛感还会是向下吗？",
      read: "这是他<b>论证最完整的一条</b>，把「看多」从情绪变成了仓位结构的判断。与他 09-21「对冲带 $82–84K」并不冲突，但把该区间的性质从「对冲区」改成了<b>已验证的支撑</b>。失效条件：链上杠杆重新堆积到过热（OI 快速回升而价格不创新高）。",
      tags: ["链上数据", "仓位建议"],
      src: "X 原文 @KillaXBT · 2103512277315920295"
    },
    {
      date: "2026-09-25",
      title: "最大痛感在上不在下：所有人都想要更低的价",
      quote: "看看四周吧。所有人都想要更低的价，而不是更高的价。最大痛感在上，不在下。",
      read: "这是<b>逆向情绪指标</b>的浓缩版：他把一致预期的方向当作反向指标。与同日那条「谁被打爆了」的长文互为佐证。失效条件：市场情绪转为一致看多、杠杆重新堆高，届时最大痛感的方向会翻转。",
      tags: ["情绪指标", "趋势切换"],
      src: "X 原文 @KillaXBT · 2103502063489646849"
    },
    {
      date: "2026-09-25",
      title: "「别把牛市里的事情搞复杂了」",
      quote: "令人兴奋的时刻即将到来……别把牛市里的事情搞复杂了。",
      read: "一句态度表态，<b>无新增点位</b>。价值仅在于确认他此刻没有转向，且明确反对过度交易。可作背景处理，不构成独立信号。",
      tags: ["情绪指标"],
      src: "X 原文 @KillaXBT · 2103497502020559092"
    },
    {
      date: "2026-09-25",
      title: "周期在加速：底部回撤 54%，新高会先于减半出现",
      quote: "很多人没准备好这一轮周期会推进得多快。周期正在加速，这是我一直在验证的理论——随着时间推移，BTC 会越来越像指数资产，下行波动越来越小。在 54% 回撤处见底就是这件事正在提前发生的明确信号，我几乎可以确定我们会在减半之前创出新高。减半牛市年可能会逐渐成为历史，最终一切只取决于流动性。",
      read: "这是他<b>框架层面的升级</b>：从「周期定位」转向「周期加速论」，并用 54% 的回撤幅度作为证据。它改动的是 09-18「2027 年才创新高」的时间表——现在认为新高会提前。失效条件：若本轮在减半窗口前未能创新高，加速论即被证伪。",
      tags: ["周期判断", "宏观驱动"],
      src: "X 原文 @KillaXBT · 2103478124990386645"
    },
    {
      date: "2026-09-25",
      title: "对冲空单上移至 $93,600，失效位 $99–100K",
      quote: "我已决定把 BTC 对冲空单的入场位上移到 93.6K。到位后我会对冲 100% 的敞口——包括现货、延续多单和波段多单，失效位约在 99–100K，目标是抓一段 10–15% 的回调。如果走势变化我会调整计划。",
      read: "这是<b>最关键的一次点位修正</b>：他此前唯一的做空参考位是 $90K，现在上移到 $93.6K 并给出了完整风控（失效 99–100K、目标回撤 10–15%）。意味着在 93.6K 之前，他<b>不会站空头</b>。失效条件：站稳 99–100K 上方，对冲逻辑作废。",
      tags: ["关键价位", "失效条件"],
      src: "X 原文 @KillaXBT · 2103449727299702828"
    },
    {
      date: "2026-09-25",
      title: "给踏空者的仓位方案：每周部署 10%，两个月建满",
      quote: "如果你现在还空仓，我的做法是每周部署约 10% 的资金，在未来两个月里逐步建到满仓。别做那个一两年后回头看、因为固执不敢扣扳机、一直在等可能永远不会到来的更低价格而后悔的人。",
      read: "这是罕见的<b>可执行节奏建议</b>（不是点位），说明他已经从「等回踩」转为「不等回踩」。与他自己 09-24 启动 10 倍杠杆长线策略互相印证。失效条件：价格跌破 80–83K 的前周线区间高点，届时他的「分批建仓」逻辑需要重估。",
      tags: ["仓位建议", "趋势切换"],
      src: "X 原文 @KillaXBT · 2103291834080309616"
    },
    {
      date: "2026-09-25",
      title: "断言不再回 $60K：熊市底部总是抢跑主要流动性",
      quote: "这不是会不会的问题，而是什么时候的问题。BTC 不会再回到 6 万。熊市底部几乎总是抢跑主要流动性。最可能的情形是：在经历足够多把人吓破胆的洗盘之后，我们最终会去吃掉上方的流动性。",
      read: "他把「洗盘」定性为<b>上涨前的必要过程而非趋势反转</b>，这直接削弱了 09-18 基准剧本里「先破 7 万再上 9 万」的必要性。失效条件：跌破 80K 并站稳下方，意味着他所说的「洗盘」实为趋势破坏。",
      tags: ["趋势切换", "失效条件"],
      src: "X 原文 @KillaXBT · 2103219771441561802"
    },
    {
      date: "2026-09-25",
      title: "波段空单布在 $89–92K，失效位 $96K（次日上移至 $93.6K）",
      quote: "过去 360 多天我分享的每一笔波段交易都完全按计划走出来了。我的下一笔波段空单布在 $89–92K 区间，失效位在 $96K 上方。我会耐心等价格到我的位置再执行。我没兴趣去抓每一次小的上下波动，我只关注更干净的 10%–30% 的波段。",
      read: "这条是<b>次日「对冲空单上移至 $93.6K」的前身</b>——把两条串起来能看到他的空单点位在一天内上移约 3.5K（89–92K → 93.6K），失效位同步从 $96K 抬到 $99–100K。说明<b>价格结构在往对他不利的方向走、他被迫上移</b>，这是判断他看多程度的侧面指标。另注：他自称 360 多天的波段喊单全部按计划兑现，属可核验战绩。",
      tags: ["关键价位", "失效条件", "战绩复盘"],
      src: "X 原文 @KillaXBT · 2103168995859841403"
    },
    {
      date: "2026-09-24",
      title: "一句话定调：越早接受底部已成越好",
      quote: "你越早接受底部已经形成，对你越好。",
      read: "一句话态度条，<b>无新增点位</b>。作用是把同日那条长文（底部已在 / 目标 $126K）的结论再压实一次，属信心表达而非新信息。",
      tags: ["趋势切换"],
      src: "X 原文 @KillaXBT · 2103143922084229513"
    },
    {
      date: "2026-09-24",
      title: "实盘动作：启动 10 倍 BTC 多头策略，目标 $126K",
      quote: "正在部署我的 10 倍 BTC 多头策略。计划分 3 次入场，目标 126K。机构级别的仓位配置。子账户已启用，第一笔按市价进场。",
      read: "从观点到<b>真金白银的实盘落地</b>——他把 09-21「目标 $126,000」从预测变成了持仓计划，且明确用 10 倍杠杆、分三次入场。这是判断他可信度最硬的一条：错了会实打实亏钱。失效条件：价格跌破前周线区间高点前，若他主动止损离场，说明他自己否定了这个剧本。",
      tags: ["仓位建议", "目标价"],
      src: "X 原文 @KillaXBT · 2103082226334249426"
    },
    {
      date: "2026-09-24",
      title: "「非常重要的长文」：底部已在，牛市最大回撤仅 10%–15%",
      quote: "这条非常重要，我建议你至少读 10 遍。我相信底部已经形成。从这里到 $126K，我预计本轮牛市最大的回撤大约只有 10%–15%。也就是说，如果 $87K 是本轮的局部高点、之后深回撤到 7 万低段，那里就是比特币找到地板的位置；真到了那里，我会大幅加仓延续多单。我多次说过，牛市里我极少做空，除非价格在测试一个很强、很明确的位置。眼下比特币正在测试 8 万这个关键区间，只要守住我们翻转过来的前区间高点，向上延续的可能性就非常真实。所以回撤可能发生，但下行空间有限。我唯一会觉得舒服的做空位置在 9 万区间。",
      read: "这条是<b>整套剧本的原文出处</b>——此前中文媒体把同一条内容标成 09-21，实际发表于 09-24，滞后 3 天且被大幅压缩。一手原文比转载版多出两个硬信息：① $87K 若成局部高点、回撤到 7 万低段就是地板，且他会在那里加仓；② $90K 区间是他唯一认可的做空位。失效条件：跌破 8 万的前区间高点且站不回来。",
      tags: ["趋势切换", "目标价", "关键价位"],
      src: "X 原文 @KillaXBT · 2103074401830768804"
    },
    {
      date: "2026-09-24",
      title: "未平仓合约已清洗到 $76K 时的水平，而价格还在 $84K",
      quote: "我觉得这挺夸张的。未平仓合约已经完全回落到 BTC 还在 76K 时的水平，但价格却在 84K。在我看来，这非常健康。",
      read: "用<b>链上杠杆数据</b>佐证「底部已成」：同样的价格位置，杠杆却少了整整一个台阶，说明上涨不是靠杠杆堆出来的。这条为后面 09-25「杠杆已重置」的结论埋了伏笔。失效条件：OI 快速回升而价格滞涨，健康度信号即反转。",
      tags: ["链上数据", "趋势切换"],
      src: "X 原文 @KillaXBT · 2102917704814321905"
    },
    {
      date: "2026-09-22",
      title: "「一切已计价」：利空反应转正，判定趋势已切向牛市",
      quote: "比特币在熊市里被利空压着走，进入牛市后同样的负面消息会变成『牛市 FUD』——用来逼人在上涨前割肉。本轮已经历加息、Clarity Act 炒作失败、『第三次世界大战』叙事，BTC 却扫清低点后走强，这是趋势转变最明确的信号之一。本轮的确认催化剂是 Clarity Act，上一轮是现货 ETF 获批。",
      read: "这是他从「等更低点」到「承认趋势反转」的口径变化，属于框架层面的转向而非点位调整。注意他的验证锚点是<b>事件驱动</b>（Clarity Act 立法进程），不是价格——意味着这条判断的失效条件也很清晰：法案再失败一次，逻辑就要重估。",
      tags: ["趋势切换", "宏观驱动"],
      src: "金色财经 / 凤凰网 / 币圈子（转载，尚无一手原文）"
    },
    {
      date: "2026-09-21",
      title: "目标上移至 $88,000，同时否定快速回测 $70,000",
      quote: "比特币下一步目标可看高至 $88,000 区间；若快速回落 $80,000 下方，则可能测试 $70,000 低点，但基于成交量分析，此情景当前不太可能。",
      read: "他第一次给这一腿设了明确上沿（$88,000），并把先前「可能探 7 万低段」的概率主动下调。这是<b>减仓空头情绪、转向顺势</b>的标志。可执行含义：$80,000 是他这条判断的失效线，跌破则他的乐观情景作废。",
      tags: ["目标价", "失效条件"],
      src: "区块链周刊（转载，尚无一手原文）"
    },
    {
      date: "2026-09-21",
      title: "建议 $82,000–$84,000 区间对冲，$85,000–$86,000 为关键阻力",
      quote: "$82,000–$84,000 是潜在对冲区与中间阻力，对没有盘整的上涨保持谨慎；$85,000–$86,000 是关键阻力区，需要持续突破，站稳后焦点转向 $88,000–$95,000。$80,000 是看涨旗形突破位，突破后目标 $82,250–$98,000。",
      read: "这是同期最「可执行」的一条——他罕见地给了<b>进攻方向 + 防守区间</b>的完整结构，而不是只给方向。注意它与「目标 $88,000」并不矛盾：$82–84K 是他的对冲带，$85–86K 才是要真突破的门槛。",
      tags: ["关键价位", "仓位建议"],
      src: "币市通（转载，尚无一手原文）"
    },
    {
      date: "2026-09-18",
      title: "定调：先做更高低点，2026 年摸不到 10 万",
      quote: "先走一个更高的低点（可能下探 7 万低段），再走一腿到 9 万。2026 年内碰不到 10 万，真正的新高要等 2027 年，最终目标仍是 $160,000。山寨币（SOL / HYPE / ASTER）已提前见底，进入轮动布局期。",
      read: "这是他 9 月中旬的<b>基准剧本</b>，也是后面几条更新的对照物。看动态时要拿这条当锚：凡是偏离「先破 7 万再上 9 万」的表态，都是他在改剧本。",
      tags: ["基准剧本", "周期判断"],
      src: "综合中文加密媒体报道（转载，尚无一手原文）"
    }
  ]
};
