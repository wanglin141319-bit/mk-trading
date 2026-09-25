# 加密交易圈名人榜 · 维护说明

访问路径：`https://mktrading.vip/legends/`

## 目录结构

```
legends/
├── index.html       榜单主页（列表 + 筛选 + 收录标准）
├── killa.html       Killa @KillaXBT 详情页
└── README.md        本文件
```

## 如何新增一位名人

只需两步。

### 第一步：建详情页

复制 `killa.html` 改名为 `<id>.html`（例如 `james-wynn.html`），替换其中的内容。
详情页的固定骨架是这几块，照着改就行：

| 区块 | 内容 |
|---|---|
| Hero | 头像字母、名字、handle、一句话定位、4 个关键数据 |
| THE CALL | 他最出名的那一次判断，以及事后验证结果 |
| TIMELINE | 完整判断轨迹，含命中和失误 |
| METHODOLOGY | 他的方法论拆解 |
| TRACK RECORD | 双栏：命中的判断 / 失误与瑕疵 |
| CRITIQUE | 争议与质疑 |
| LEVELS | 当前立场与关键价位 |
| TAKEAWAYS | 对交易者的启示 |

### 第二步：在榜单主页登记

打开 `legends/index.html`，找到 `LEGENDS` 数组，加一条对象：

```js
{
  rank: "02",                    // 榜单序号，字符串
  id: "james-wynn",
  name: "James Wynn",
  handle: "@JamesWynnReal",
  avatar: "J",                   // 头像里显示的字母
  url: "james-wynn.html",        // 详情页文件名
  tagline: "一句话总结这个人是谁、因为什么出名。",
  tags: [
    { text: "高杠杆", cls: "" },      // cls 可选：c / g / p，留空为默认灰
    { text: "BTC", cls: "c" }
  ],
  cat: ["btc", "ta"],            // 分类，见下方
  record: [
    { label: "标签文字", value: "数值", cls: "green" }  // cls 可选：green / red / gold
  ]
}
```

`cat` 支持的值：`btc`(BTC 专项) / `cycle`(周期模型) / `onchain`(链上数据) / `ta`(技术分析) / `macro`(宏观驱动)

如果新分类不在筛选器里，去改 `CATEGORIES` 数组，加一项即可：

```js
{ key: "macro", label: "宏观驱动" }
```

## 注意事项

- **HTML 文件必须是 UTF-8 编码。** 用记事本另存时注意选编码，否则中文会变乱码。
- 榜单主页的「已收录」计数是自动算的（只统计非 `soon` 的条目），不用手动改。
- 想要只显示「即将上线」的占位卡片，保留 `soon: true` 那条即可。
- 详情页顶部导航里的返回链接用的是相对路径 `./`，不要改成绝对路径，否则本地预览会断。

## 收录标准（写新条目时保持一致）

1. 必须有能被检索到的公开判断记录（具体日期 + 具体观点 + 可拆解的逻辑）。
2. 战绩和失误都要写，只写高光没有阅读价值。
3. 明确区分「阶段判断」和「可执行策略」—— 方向对不等于能赚钱。
