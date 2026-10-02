/* Killa 动态追踪 · 渲染冒烟测试
 * 1) 载入 legends/data/killa-feed.js（假 window）
 * 2) 抽出 legends/killa.html 里「最新动态渲染」那段 IIFE，用假 document 执行
 * 3) 断言：条目数 == total、无 undefined、div 开闭平衡、日期倒序、无重复推文 ID
 */
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const DATA = path.join(__dirname, 'killa-feed.js');
const HTML = path.join(__dirname, '..', 'killa.html');

const errs = [];
const notes = [];

/* ---------- 1. 载入数据文件 ---------- */
const win = {};
const ctx = vm.createContext({ window: win });
vm.runInContext(fs.readFileSync(DATA, 'utf8'), ctx, { filename: 'killa-feed.js' });
const F = win.KILLA_FEED;
if (!F) errs.push('window.KILLA_FEED 未定义');
if (!Array.isArray(F && F.entries)) errs.push('entries 不是数组');

/* ---------- 2. 抽出并执行渲染 IIFE ---------- */
const html = fs.readFileSync(HTML, 'utf8');
const marker = '最新动态渲染';
const start = html.indexOf(marker);
if (start < 0) errs.push('killa.html 中找不到「最新动态渲染」区块');
const tail = html.slice(start);
const end = tail.indexOf('})();');
const renderSrc = end >= 0 ? tail.slice(tail.indexOf('(function () {'), end + 5) : '';
if (!renderSrc) errs.push('未能抽出渲染 IIFE 源码');

/* 假 DOM：只实现渲染代码用到的最小面 */
const captured = {};
function makeEl(id) {
  return {
    id,
    _html: '',
    set innerHTML(v) { this._html = v; captured[id] = v; },
    get innerHTML() { return this._html; },
    set textContent(v) { this._text = v; captured[id + '__text'] = v; },
    get textContent() { return this._text; },
  };
}
const els = { feedList: makeEl('feedList'), scanTime: makeEl('scanTime'), feedSrc: makeEl('feedSrc') };
const fakeDoc = { getElementById: (id) => els[id] || null };

let renderErr = null;
try {
  const rctx = vm.createContext({ window: win, document: fakeDoc, Date, String, isFinite, console });
  vm.runInContext(renderSrc, rctx, { filename: 'killa.html#render' });
} catch (e) {
  renderErr = e;
}
if (renderErr) errs.push('渲染函数抛错: ' + renderErr.message);

/* ---------- 3. 断言 ---------- */
const out = captured['feedList'] || '';
const cardCount = (out.match(/<div class="fi[ "]/g) || []).length;
const divOpen = (out.match(/<div/g) || []).length;
const divClose = (out.match(/<\/div>/g) || []).length;

if (!renderErr) {
  if (!out) errs.push('feedList.innerHTML 为空（渲染未产出）');
  if (cardCount !== F.entries.length) errs.push(`卡片数 ${cardCount} != entries ${F.entries.length}`);
  if (F.total !== F.entries.length) errs.push(`total(${F.total}) != entries 实际条数(${F.entries.length})`);
  if (divOpen !== divClose) errs.push(`div 不配对: 开 ${divOpen} / 闭 ${divClose}`);
  if (/undefined|NaN|\[object Object\]/.test(out)) errs.push('渲染输出含 undefined/NaN');
  if (!/累计收录 \d+ 条/.test(captured['scanTime__text'] || '')) errs.push('scanTime 文案异常: ' + captured['scanTime__text']);
  if (!/信息来源/.test(captured['feedSrc'] || '')) errs.push('feedSrc 文案异常');
}

/* 数据本身的质量断言 */
const REQUIRED = ['date', 'title', 'quote', 'read', 'tags', 'src'];
const dates = [];
(F.entries || []).forEach((e, i) => {
  REQUIRED.forEach(k => { if (!e[k]) errs.push(`entries[${i}] 缺字段 ${k}`); });
  if (!Array.isArray(e.tags) || !e.tags.length) errs.push(`entries[${i}] tags 为空`);
  if (e.date && !/^\d{4}-\d{2}-\d{2}$/.test(e.date)) errs.push(`entries[${i}] date 异常 ${e.date}`);
  dates.push(e.date);
});
for (let i = 1; i < dates.length; i++) {
  if (dates[i] > dates[i - 1]) errs.push(`日期未倒序: [${i - 1}]${dates[i - 1]} < [${i}]${dates[i]}`);
}
const ids = (F.entries || []).map(e => (String(e.src).match(/(\d{10,})/) || [])[1]).filter(Boolean);
const dup = ids.filter((v, i) => ids.indexOf(v) !== i);
if (dup.length) errs.push('重复推文 ID: ' + [...new Set(dup)].join(','));
if (!/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+08:00$/.test(F.lastScan || '')) errs.push('lastScan 格式异常: ' + F.lastScan);

console.log('数据文件   : killa-feed.js (' + fs.statSync(DATA).size + ' B)');
console.log('entries    :', (F.entries || []).length, '条 | total:', F.total);
console.log('lastScan   :', F.lastScan);
console.log('最新/最旧  :', dates[0], '/', dates[dates.length - 1]);
console.log('渲染卡片数 :', cardCount, '| div 开/闭:', divOpen + '/' + divClose);
console.log('scanTime   :', captured['scanTime__text']);
console.log('X 一手 ID  :', ids.length, '| 重复:', dup.length ? dup : '无');
console.log('今日新增   :', dates.filter(d => d === '2026-10-02').length, '条');
console.log('---');
if (errs.length) { console.log('❌ 冒烟失败:'); errs.forEach(x => console.log('   -', x)); process.exit(1); }
console.log('✅ 渲染冒烟通过：条目数==total、div 平衡、无 undefined、日期倒序、无重复 ID');
