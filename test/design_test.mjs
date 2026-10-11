// Design test for the Rindge Town Guide.
// Usage: node test/design_test.mjs [path/to/index.html]  (needs playwright + axe-core resolvable; see test/README.md)
// Checks every chapter, phone and desktop, light and dark:
//  1. axe-core WCAG 2.2 A/AA rules (expanded cards included)
//  2. readability: no text under 12px, warn under 14px; line length <= 90 characters
//  3. touch targets: controls >= 24px (WCAG 2.5.8 AA), goal >= 44px (Apple HIG); inline text links exempt
//  4. reflow: no sideways page scroll at 320px wide (WCAG 1.4.10) and at 200% text size
//  5. text spacing override (WCAG 1.4.12): no clipped text
//  6. structure: exactly one visible h1 per view, no skipped heading levels
//  7. keyboard: every tab stop shows a visible focus indicator
//  8. findability: common resident questions answered within 1 tap from Home and by the first search result
//  9. charts: every bar with a value draws (catches layout collisions that hide data)
// 10. data: schema.org JSON-LD is valid; open/closed status is right at fixed times; countdowns, grid totals, sorting and ?q= work
import { createRequire } from 'module';
import path from 'path';
import fs from 'fs';
const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PLAYWRIGHT || 'playwright');
const AXE = fs.readFileSync(require.resolve(process.env.AXE || 'axe-core/axe.min.js'), 'utf8');
const FILE = 'file://' + path.resolve(process.argv[2] || 'index.html');

const VIEWS = ['home', 'start-group', 'happening', 'meetdocs', 'documents', 'reports', 'money', 'rules', 'howdoi', 'contacts', 'about'];
const CONFIGS = [
  { name: 'phone-light', w: 390, h: 844, dark: false },
  { name: 'phone-dark', w: 390, h: 844, dark: true },
  { name: 'desktop-light', w: 1280, h: 900, dark: false },
  { name: 'desktop-dark', w: 1280, h: 900, dark: true },
];
// question -> search text, sections that count as the answer, chapter Home must link to in one tap
const TASKS = [
  ['Who do I call at the Town Offices?', 'town clerk', ['directory'], 'contacts'],
  ['Police non-emergency number', 'police', ['directory', 'emergency'], 'contacts'],
  ['When is the transfer station open?', 'transfer station', ['emergency', 'directory'], 'howdoi'],
  ['How do I license my dog?', 'dog license', ['howto'], 'howdoi'],
  ['How do I get a building permit?', 'building permit', ['howto'], 'howdoi'],
  ['How do I vote absentee?', 'absentee', ['howto'], 'howdoi'],
  ['How do I get a burn permit?', 'burn permit', ['howto'], 'howdoi'],
  ['What is the tax rate?', 'tax rate', ['numbers', 'budget', 'trends'], 'money'],
  ['What happened with the town budget?', 'budget', ['budget', 'election', 'topics'], 'money'],
  ['When does the Select Board meet?', 'select board', ['timeline', 'calendar', 'directory', 'howto'], 'meetdocs'],
  ['When is the next town vote?', 'next vote', ['calendar', 'election'], 'meetdocs'],
  ['Find meeting minutes', 'minutes', ['library', 'timeline'], 'documents'],
  ['What are the frontage rules for my lot?', 'frontage', ['laws', 'recurring', 'topics'], 'rules'],
  ['What is happening with the ambulance?', 'ambulance', ['topics', 'emergency'], 'happening'],
  ['Where are the annual town reports?', 'town report', ['townreports'], 'reports'],
  ['Elderly exemption limits', 'elderly exemption', ['topics', 'numbers', 'howto'], 'money'],
  ['Which schools serve Rindge?', 'school', ['schools', 'topics'], 'howdoi'],
];

const results = { file: FILE, when: new Date().toISOString(), checks: {}, failures: [], warnings: [] };
const fail = (check, where, msg) => { results.failures.push({ check, where, msg }); };
const warn = (check, where, msg) => { results.warnings.push({ check, where, msg }); };
const count = (k) => { results.checks[k] = (results.checks[k] || 0) + 1; };

async function show(p, view) {
  await p.goto(FILE + (view === 'home' ? '' : '#' + view));
  await p.waitForTimeout(350);
  await p.evaluate(() => { document.querySelectorAll('.anim').forEach(e => e.classList.remove('anim')); });
}
async function expandAll(p) {
  await p.evaluate(() => {
    document.querySelectorAll('#main > :not(.pg-off) details').forEach(d => d.open = true);
    document.querySelectorAll('#main > :not(.pg-off) .xc-tog[aria-expanded="false"]').forEach(b => b.click());
  });
  await p.waitForTimeout(250);
  await p.evaluate(() => window.scrollTo({ top: 0, behavior: 'instant' }));
}

const b = await chromium.launch();
for (const c of CONFIGS) {
  const ctx = await b.newContext({ viewport: { width: c.w, height: c.h }, colorScheme: c.dark ? 'dark' : 'light', reducedMotion: 'reduce' });
  const p = await ctx.newPage();
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  for (const v of VIEWS) {
    const where = `${c.name} #${v}`;
    await show(p, v);
    // 6. structure
    const hs = await p.evaluate(() => [...document.querySelectorAll('h1,h2,h3,h4,h5,h6,[role=heading]')]
      .filter(e => e.offsetParent !== null || e.getClientRects().length).map(e => +((e.getAttribute('aria-level')) || e.tagName[1])));
    count('structure');
    const h1 = hs.filter(x => x === 1).length;
    if (h1 !== 1) fail('structure', where, `${h1} visible h1 headings (want exactly 1)`);
    for (let i = 1; i < hs.length; i++) if (hs[i] > hs[i - 1] + 1) { fail('structure', where, `heading level jumps from h${hs[i - 1]} to h${hs[i]}`); break; }

    // 7. keyboard focus (first 30 tab stops), desktop light only to keep runtime sane
    if (c.name === 'desktop-light') {
      await p.evaluate(() => { document.activeElement && document.activeElement.blur(); window.scrollTo(0, 0); });
      await p.mouse.click(1, 300).catch(() => {});
      for (let i = 0; i < 30; i++) {
        await p.keyboard.press('Tab');
        const r = await p.evaluate(() => {
          const e = document.activeElement; if (!e || e === document.body) return null;
          const s = getComputedStyle(e); const ring = (s.outlineStyle !== 'none' && parseFloat(s.outlineWidth) >= 2) || /rgb|#/.test(s.boxShadow) && s.boxShadow !== 'none';
          return { ring, d: (e.id ? '#' + e.id : e.tagName.toLowerCase() + '.' + [...e.classList].join('.')) + ' "' + (e.textContent || e.value || '').trim().slice(0, 30) + '"' };
        });
        if (!r) continue; count('focus');
        if (!r.ring) fail('focus', where, 'no visible focus indicator on ' + r.d);
      }
      await show(p, v);
    }

    await expandAll(p);
    // 1. axe
    await p.addScriptTag({ content: AXE });
    const ax = await p.evaluate(async () => {
      const r = await axe.run({ include: [['#main'], ['.topbar'], ['footer']], exclude: [['.pg-off']] }, { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'] }, resultTypes: ['violations'] });
      return r.violations.map(v => ({ id: v.id, impact: v.impact, n: v.nodes.length, ex: v.nodes.slice(0, 3).map(n => n.target.join(' ') + ' :: ' + (n.failureSummary || '').split('\n').slice(1, 2).join('')) }));
    });
    count('axe');
    ax.forEach(v => fail('axe', where, `${v.id} (${v.impact}) x${v.n}: ${v.ex.join(' | ')}`));

    // 2 + 3. readability and targets
    const m = await p.evaluate(() => {
      const vis = e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0 && getComputedStyle(e).visibility !== 'hidden'; };
      const small = [], tiny = [], longLines = [], targets = [];
      const root = document.querySelectorAll('#main > :not(.pg-off), .topbar, footer');
      const tw = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      const inScope = el => [...root].some(r => r.contains(el));
      let n;
      while ((n = tw.nextNode())) {
        const t = n.textContent.trim(); if (!t) continue; const el = n.parentElement; if (!el || !inScope(el) || !vis(el)) continue;
        if (el.closest('.sr,[aria-hidden=true],svg,kbd,.v-foot')) continue;
        const fs = parseFloat(getComputedStyle(el).fontSize);
        const d = el.tagName.toLowerCase() + '.' + [...el.classList].join('.') + ' "' + t.slice(0, 24) + '"';
        if (fs < 12) tiny.push(fs.toFixed(1) + 'px ' + d); else if (fs < 14) small.push(fs.toFixed(1) + 'px ' + d);
      }
      document.querySelectorAll('#main > :not(.pg-off) p').forEach(pp => {
        if (!vis(pp)) return; const fs = parseFloat(getComputedStyle(pp).fontSize); const cpl = pp.clientWidth / (fs * 0.5);
        if (cpl > 95 && pp.textContent.length > 120) longLines.push(Math.round(cpl) + 'ch p.' + [...pp.classList].join('.') + ' "' + pp.textContent.trim().slice(0, 24) + '"');
      });
      document.querySelectorAll('a[href],button,input:not([type=hidden]),select,summary,[role=button],[tabindex="0"]').forEach(e => {
        if (!inScope(e) || !vis(e)) return; if (e.closest('[hidden],.pg-off')) return;
        const s = getComputedStyle(e); const r = e.getBoundingClientRect();
        const inline = s.display === 'inline' && e.parentElement && /^(P|LI|TD|DD|SPAN|EM|STRONG|SMALL|DIV)$/.test(e.parentElement.tagName) && e.parentElement.textContent.trim().length > e.textContent.trim().length + 3;
        if (inline) return;
        const mn = Math.min(r.width, r.height);
        if (mn < 44) targets.push({ mn: Math.round(mn), d: e.tagName.toLowerCase() + '.' + [...e.classList].join('.') + ' "' + (e.textContent || e.getAttribute('aria-label') || '').trim().slice(0, 24) + '"' });
      });
      return { small, tiny, longLines, targets };
    });
    // 9. charts: every bar that has a value actually draws
    const empty = await p.evaluate(() => [...document.querySelectorAll('#main > :not(.pg-off) .fill, #main > :not(.pg-off) .seg')]
      .filter(f => f.offsetParent !== null && parseFloat(f.style.getPropertyValue('--w')) > 0.5 && f.getBoundingClientRect().width < 1)
      .map(f => (f.closest('.chart,.card')?.querySelector('h3,h4')?.textContent || '').trim().slice(0, 40)));
    count('charts');
    if (empty.length) fail('charts', where, `${empty.length} chart bars draw at zero width, e.g. ${[...new Set(empty)].slice(0, 3).join(' | ')}`);
    count('readability'); count('targets');
    if (m.tiny.length) fail('readability', where, `${m.tiny.length} text runs under 12px, e.g. ${m.tiny.slice(0, 4).join(' | ')}`);
    if (m.small.length) warn('readability', where, `${m.small.length} text runs 12-14px, e.g. ${m.small.slice(0, 4).join(' | ')}`);
    if (m.longLines.length) warn('readability', where, `${m.longLines.length} paragraphs over 95 characters per line, e.g. ${m.longLines.slice(0, 2).join(' | ')}`);
    const t24 = m.targets.filter(t => t.mn < 24), t44 = m.targets.filter(t => t.mn >= 24);
    if (t24.length) fail('targets', where, `${t24.length} controls under 24px, e.g. ${t24.slice(0, 4).map(t => t.mn + 'px ' + t.d).join(' | ')}`);
    if (t44.length) warn('targets', where, `${t44.length} controls 24-43px, e.g. ${t44.slice(0, 4).map(t => t.mn + 'px ' + t.d).join(' | ')}`);
  }
  if (errs.length) fail('errors', c.name, 'JavaScript errors: ' + [...new Set(errs)].join(' | '));
  await ctx.close();
}

// 4 + 5. reflow at 320px, 200% text, and text spacing
for (const [label, setup] of [
  ['320px', async p => {}],
  ['200% text', async p => p.evaluate(() => { document.documentElement.setAttribute('data-size', '3'); document.documentElement.style.fontSize = '200%'; })],
  ['text spacing', async p => p.addStyleTag({ content: '*{line-height:1.5!important;letter-spacing:.12em!important;word-spacing:.16em!important}p{margin-bottom:2em!important}' })],
]) {
  const ctx = await b.newContext({ viewport: { width: label === '320px' || label === 'text spacing' ? 320 : 640, height: 800 }, reducedMotion: 'reduce' });
  const p = await ctx.newPage();
  for (const v of VIEWS) {
    await show(p, v); await setup(p); await expandAll(p); await p.waitForTimeout(150);
    const r = await p.evaluate(() => {
      const W = document.documentElement.clientWidth, over = [];
      document.querySelectorAll('#main > :not(.pg-off) *, .topbar *').forEach(e => {
        const rc = e.getBoundingClientRect(); if (!rc.width) return;
        if (rc.right > W + 1 && !e.closest('.tblwrap,.is-scroll,[class*=scroll],.localnav ul,pre,table,.chips') ) over.push(e.tagName.toLowerCase() + '.' + [...e.classList].join('.') + ' right=' + Math.round(rc.right));
      });
      const clipped = [];
      document.querySelectorAll('#main > :not(.pg-off) *, .topbar *').forEach(e => {
        const s = getComputedStyle(e); if (s.overflow !== 'hidden' && s.overflowY !== 'hidden') return; if (!e.textContent.trim()) return;
        if (e.matches('.xc-body,.xc-clamp,.xc-peek,svg,.sr,.chart *') || e.closest('.sr,[aria-hidden=true],.xc:not(.open) .xc-body')) return;
        if (e.scrollHeight > e.clientHeight + 4 && e.clientHeight > 0 && s.textOverflow !== 'ellipsis' && !/-webkit-box/.test(s.display)) clipped.push(e.tagName.toLowerCase() + '.' + [...e.classList].join('.'));
      });
      return { sw: document.documentElement.scrollWidth, W, over: over.slice(0, 4), clipped: clipped.slice(0, 4), nclip: clipped.length };
    });
    count('reflow');
    if (r.sw > r.W + 1) fail('reflow', `${label} #${v}`, `page scrolls sideways (${r.sw}px > ${r.W}px): ${r.over.join(' | ')}`);
    else if (r.over.length) warn('reflow', `${label} #${v}`, `elements past the edge: ${r.over.join(' | ')}`);
    if (label === 'text spacing' && r.nclip) fail('reflow', `${label} #${v}`, `${r.nclip} boxes clip text: ${r.clipped.join(' | ')}`);
  }
  await ctx.close();
}

// 8. findability
{
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, reducedMotion: 'reduce' });
  const p = await ctx.newPage();
  await show(p, 'home');
  const homeLinks = await p.evaluate(() => [...document.querySelectorAll('#home a[href^="#"]')].map(a => a.getAttribute('href').slice(1)));
  const secOf = await p.evaluate(() => { const m = {}; document.querySelectorAll('.groupban').forEach(g => { m[g.id] = g.id; g.querySelectorAll('.gb-l a').forEach(a => m[a.getAttribute('href').slice(1)] = g.id); }); return m; });
  for (const [q, text, want, chap] of TASKS) {
    count('findability');
    const chapsFromHome = new Set(homeLinks.map(id => secOf[id] || (secOf[id] === undefined ? null : id)).filter(Boolean));
    const direct = homeLinks.some(id => want.includes(id) || secOf[id] === chap) || homeLinks.includes(chap);
    if (!direct) warn('findability', q, `Home has no one-tap link to the "${chap}" chapter`);
    await show(p, 'home');
    await p.keyboard.press('Control+k'); await p.keyboard.type(text); await p.waitForTimeout(200);
    const top = await p.evaluate(() => [...document.querySelectorAll('#sdres [role=option]')].slice(0, 3).map(o => o.textContent.trim().slice(0, 60)));
    await p.keyboard.press('Enter'); await p.waitForTimeout(450);
    const landed = await p.evaluate(() => { const v = document.getElementById('viewer'); if (v && !v.hidden) return { id: 'viewer', sec: 'library' }; const id = decodeURIComponent(location.hash.slice(1)); const el = document.getElementById(id); const s = el && el.closest('section.sec,section.home,.groupban'); return { id, sec: s ? s.id : null }; });
    if (landed.id === 'viewer') await p.keyboard.press('Escape');
    if (!want.includes(landed.sec) && !want.includes(landed.id)) fail('findability', q, `search "${text}" first result went to #${landed.id} (section ${landed.sec}); top results: ${top.join(' / ')}`);
  }
  await ctx.close();
}
// 10. data: machine-readable structure and the smart views built from it
{
  const ctx = await b.newContext({ viewport: { width: 1280, height: 900 }, reducedMotion: 'reduce' });
  const p = await ctx.newPage();
  await show(p, 'home');
  // schema.org JSON-LD
  const ld = await p.evaluate(() => [...document.querySelectorAll('script[type="application/ld+json"]')].map(s => { try { return JSON.parse(s.textContent); } catch (e) { return { error: e.message }; } }));
  count('data');
  if (!ld.length) fail('data', 'json-ld', 'no schema.org JSON-LD found');
  for (const doc of ld) {
    if (doc.error) { fail('data', 'json-ld', 'JSON-LD does not parse: ' + doc.error); continue; }
    const g = doc['@graph'] || [doc];
    const site = g.find(x => x['@type'] === 'WebSite');
    if (!site || !site.name || !site.url) fail('data', 'json-ld', 'WebSite needs name and url');
    else if (!site.potentialAction || !/\{search_term_string\}/.test(site.potentialAction.target?.urlTemplate || '')) fail('data', 'json-ld', 'WebSite SearchAction is missing its url template');
    const offices = g.filter(x => /GovernmentOffice|Library/.test(x['@type']));
    if (offices.length < 10) fail('data', 'json-ld', `only ${offices.length} offices described`);
    for (const o of offices) {
      count('data');
      if (!o.name || !(o.telephone || o.url)) fail('data', 'json-ld', `office missing name/telephone: ${JSON.stringify(o).slice(0, 80)}`);
      if (o.telephone && !/^\+1-\d{3}-\d{3}-\d{4}( ext\. \d+)?$/.test(o.telephone)) fail('data', 'json-ld', `bad telephone ${o.telephone} (${o.name})`);
      for (const h of o.openingHoursSpecification || []) {
        if (!(h.dayOfWeek || []).length || !/^\d\d:\d\d$/.test(h.opens) || !/^\d\d:\d\d$/.test(h.closes) || h.opens >= h.closes) fail('data', 'json-ld', `bad hours on ${o.name}: ${JSON.stringify(h)}`);
      }
    }
    const faq = g.find(x => x['@type'] === 'FAQPage');
    if (!faq || (faq.mainEntity || []).length < 10) fail('data', 'json-ld', 'FAQPage missing or too short');
    else for (const q of faq.mainEntity) if (!q.name || !q.acceptedAnswer?.text || q.acceptedAnswer.text.length < 30) fail('data', 'json-ld', `weak FAQ answer: ${q.name}`);
  }
  await ctx.close();

  // open/closed status at fixed moments (Rindge time). Expected text comes straight from the posted hours.
  const CASES = [
    ['2026-10-13T15:20:00Z', 'Tue 11:20am', { 'Recycling and Transfer Station': 'Open · until 7 pm', "Town Clerk's office": 'Closed · opens noon', 'Tax Collector': 'Open · until 1 pm', 'Ingalls Memorial Library': 'Closed · opens 1 pm' }],
    ['2026-10-16T14:00:00Z', 'Fri 10:00am', { "Town Clerk's office": 'Today’s hours not posted', 'Recycling and Transfer Station': 'Closed · opens 1 pm', 'Public Works (Highway)': 'Today’s hours not posted' }],
    ['2026-10-18T16:00:00Z', 'Sun noon', { 'Recycling and Transfer Station': 'Closed · opens Tue 10 am', 'Ingalls Memorial Library': 'Closed · opens tomorrow 10 am', 'Police Department': 'Closed · opens tomorrow 8 am' }],
    ['2026-10-15T14:00:00Z', 'Thu 10:00am', { 'Planning Department': 'By appointment today', 'Assessing': 'Closed · opens 12:30 pm' }],
    ['2026-11-20T15:00:00Z', 'Fri Nov 20 10:00am', { 'Public Works (Highway)': 'Open · until 3:30 pm', "Town Clerk's office": 'Today’s hours not posted' }],
    ['2026-07-14T10:30:00Z', 'Tue Jul 14 6:30am', { 'Public Works (Highway)': 'Open · until 4:30 pm' }],
  ];
  for (const [iso, label, want] of CASES) {
    const c2 = await b.newContext({ viewport: { width: 1280, height: 900 }, reducedMotion: 'reduce' });
    const q = await c2.newPage();
    await q.clock.install({ time: new Date(iso) });
    await q.goto(FILE + '#directory'); await q.waitForTimeout(300);
    const got = await q.evaluate(() => { const o = {}; document.querySelectorAll('#directory .dir').forEach(c => { const h = c.querySelector('h4'), s = c.querySelector('.openst'); if (h && s) o[h.textContent.trim()] = s.textContent.replace(/\u00a0/g, ' ').trim(); }); return o; });
    for (const [k, v] of Object.entries(want)) { count('data'); if (got[k] !== v) fail('data', `hours ${label}`, `${k}: expected "${v}", got "${got[k]}"`); }
    if (iso.startsWith('2026-10-13')) {
      await q.goto(FILE); await q.waitForTimeout(300);
      const first = await q.evaluate(() => { const a = document.querySelector('.rightnow .rn-up'); return a ? a.textContent.replace(/\s+/g, ' ').trim() : null; });
      count('data'); if (!first || !/^Wed, Oct 21\s+In 8 days/.test(first)) fail('data', 'coming up', `on Tue Oct 13 the first upcoming date should be Wed Oct 21 (in 8 days), got "${first}"`);
    }
    await c2.close();
  }

  // at-a-glance totals match the board filter counts; sorting orders numbers; ?q= opens search
  const c3 = await b.newContext({ viewport: { width: 1280, height: 900 }, reducedMotion: 'reduce' });
  const r = await c3.newPage();
  await r.goto(FILE + '#timeline'); await r.waitForTimeout(300);
  const mism = await r.evaluate(() => { const out = []; const chips = {}; document.querySelectorAll('.chip[data-b]').forEach(c => { const m = c.textContent.match(/\((\d+)\)/); if (m) chips[c.textContent.replace(/\(\d+\)/, '').trim()] = +m[1]; });
    document.querySelectorAll('table.gl tbody tr').forEach(tr => { const n = tr.querySelector('th').textContent.trim(), t = +tr.querySelector('.gl-t').textContent; if (chips[n] !== t) out.push(`${n}: grid ${t} vs filter ${chips[n]}`); }); return out; });
  count('data'); if (mism.length) fail('data', 'at a glance', mism.join(' | '));
  await r.goto(FILE + '#numbers'); await r.waitForTimeout(300);
  await r.evaluate(() => { document.querySelectorAll('#numbers details').forEach(d => d.open = true); });
  const sorted = await r.evaluate(() => { const t = [...document.querySelectorAll('#numbers table')].find(x => x.querySelector('.th-sort')); if (!t) return 'no sortable table';
    const btn = t.querySelectorAll('thead th .th-sort'); const last = btn[btn.length - 1]; last.click(); last.click();
    const v = [...t.tBodies[0].rows].map(r => parseFloat(r.cells[r.cells.length - 1].textContent.replace(/[$,]/g, ''))); for (let i = 1; i < v.length; i++) if (v[i] > v[i - 1]) return 'not descending: ' + v.join(','); return null; });
  count('data'); if (sorted) fail('data', 'sorting', sorted);
  await r.goto(FILE + '?q=dog'); await r.waitForTimeout(400);
  const qs = await r.evaluate(() => { const d = document.getElementById('searchDlg'); return d && !d.hidden ? document.querySelectorAll('#sdres [role=option]').length : -1; });
  count('data'); if (qs < 1) fail('data', '?q=', `opening ?q=dog should show search results (got ${qs})`);
  await c3.close();
}

await b.close();

const cats = ['axe', 'structure', 'focus', 'readability', 'targets', 'reflow', 'charts', 'findability', 'data', 'errors'];
console.log('\nDESIGN TEST  ' + results.file);
for (const k of cats) {
  const f = results.failures.filter(x => x.check === k).length, w = results.warnings.filter(x => x.check === k).length;
  console.log(`${f ? 'FAIL' : 'PASS'}  ${k.padEnd(12)} checks:${String(results.checks[k] || 0).padStart(4)}  failures:${String(f).padStart(3)}  warnings:${String(w).padStart(3)}`);
}
const out = process.env.OUT || 'test/design_results.json';
fs.mkdirSync(path.dirname(out), { recursive: true }); fs.writeFileSync(out, JSON.stringify(results, null, 1));
console.log(`\n${results.failures.length} failures, ${results.warnings.length} warnings. Details: ${out}`);
process.exit(results.failures.length ? 1 : 0);
