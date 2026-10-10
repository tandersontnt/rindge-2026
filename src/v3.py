# v3: icons, round-3 sections, in-site document viewer registry, document library, global search index.
import json, re, html as H
from bs4 import BeautifulSoup
import r3data as R, v3docs as VD

# 24x24 stroke icons (Lucide-style geometry, drawn for this site)
I = {
 'home': '<path d="M3 10.5 12 3l9 7.5"/><path d="M5 9.5V21h14V9.5"/><path d="M10 21v-6h4v6"/>',
 'calendar': '<rect x="3" y="4.5" width="18" height="16.5" rx="2"/><path d="M3 9.5h18M8 2.5v4M16 2.5v4"/>',
 'vote': '<path d="M4 13h16v8H4z"/><path d="m8 11 3 3 6-7"/><path d="M6 13V9M18 13v-2"/>',
 'coins': '<ellipse cx="9" cy="7" rx="6" ry="3"/><path d="M3 7v5c0 1.7 2.7 3 6 3s6-1.3 6-3V7"/><path d="M3 12v5c0 1.7 2.7 3 6 3 1.2 0 2.4-.2 3.3-.5"/><circle cx="17" cy="16" r="4.5"/>',
 'scale': '<path d="M12 3v18M7 21h10M5 7h14"/><path d="m5 7-3 7a3.5 3.5 0 0 0 6 0L5 7zM19 7l-3 7a3.5 3.5 0 0 0 6 0l-3-7z"/>',
 'doc': '<path d="M14 2.5H6.5A1.5 1.5 0 0 0 5 4v16a1.5 1.5 0 0 0 1.5 1.5h11A1.5 1.5 0 0 0 19 20V7.5z"/><path d="M14 2.5v5h5M8.5 13h7M8.5 17h7M8.5 9h2"/>',
 'search': '<circle cx="11" cy="11" r="7"/><path d="m20.5 20.5-4.5-4.5"/>',
 'text': '<path d="M4 7V5h11v2M9.5 5v14M7.5 19h4"/><path d="M14 12v-1.5h7V12M17.5 10.5V19M16 19h3"/>',
 'sun': '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
 'moon': '<path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"/>',
 'contrast': '<circle cx="12" cy="12" r="9"/><path d="M12 3a9 9 0 0 1 0 18z" fill="currentColor"/>',
 'share': '<path d="M12 15V3M7.5 7.5 12 3l4.5 4.5"/><path d="M5 12v7.5A1.5 1.5 0 0 0 6.5 21h11a1.5 1.5 0 0 0 1.5-1.5V12"/>',
 'link': '<path d="M10 14a4.5 4.5 0 0 0 6.4 0l3-3a4.5 4.5 0 0 0-6.4-6.4l-1 1"/><path d="M14 10a4.5 4.5 0 0 0-6.4 0l-3 3a4.5 4.5 0 0 0 6.4 6.4l1-1"/>',
 'close': '<path d="M6 6l12 12M18 6 6 18"/>',
 'prev': '<path d="m15 5-7 7 7 7"/>', 'next': '<path d="m9 5 7 7-7 7"/>', 'chev': '<path d="m6 9 6 6 6-6"/>', 'up': '<path d="M12 19V5M5.5 11.5 12 5l6.5 6.5"/>',
 'download': '<path d="M12 3v12M7.5 10.5 12 15l4.5-4.5"/><path d="M4 17v2.5A1.5 1.5 0 0 0 5.5 21h13a1.5 1.5 0 0 0 1.5-1.5V17"/>',
 'external': '<path d="M14 3h7v7M21 3l-9 9"/><path d="M18 14v5.5a1.5 1.5 0 0 1-1.5 1.5h-12A1.5 1.5 0 0 1 3 19.5v-12A1.5 1.5 0 0 1 4.5 6H10"/>',
 'building': '<path d="M4 21V5.5L12 3l8 2.5V21"/><path d="M2.5 21h19M9 21v-4h6v4M8 8h2M14 8h2M8 12h2M14 12h2"/>',
 'road': '<path d="M8 3 4 21M16 3l4 18M12 4v3M12 10.5v3M12 17v3"/>',
 'water': '<path d="M12 3s6.5 7 6.5 11.5a6.5 6.5 0 0 1-13 0C5.5 10 12 3 12 3z"/>',
 'sign': '<path d="M12 3v18M8 21h8"/><path d="M5 5h12l2.5 3L17 11H5z"/>',
 'fire': '<path d="M12 21.5a6.5 6.5 0 0 0 6.5-6.5c0-4.5-4-7-4.5-11.5-2.5 2-3.5 4.5-3.5 7-1-.6-1.8-1.6-2-3C6.6 9.4 5.5 12 5.5 15a6.5 6.5 0 0 0 6.5 6.5z"/>',
 'dog': '<path d="M10 5.5 7 3 4 6l1.5 4.5M14 5.5 17 3l3 3-1.5 4.5"/><path d="M5.5 10.5C5.5 16 8 20.5 12 20.5s6.5-4.5 6.5-10c0-3-3-5-6.5-5s-6.5 2-6.5 5z"/><path d="M10 12h.01M14 12h.01M10.5 16c1 .8 2 .8 3 0"/>',
 'car': '<path d="M5 16.5V12l2-5.5h10l2 5.5v4.5"/><path d="M3.5 12h17v4.5h-17zM6 16.5V19M18 16.5V19"/><circle cx="7.5" cy="14" r=".6"/><circle cx="16.5" cy="14" r=".6"/>',
 'tax': '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M7 15l5-6M7.5 9.5h.01M11.5 14.5h.01M15 9h3M15 13h3M15 17h3"/>',
 'petition': '<path d="M14 2.5H6.5A1.5 1.5 0 0 0 5 4v16a1.5 1.5 0 0 0 1.5 1.5h11A1.5 1.5 0 0 0 19 20V7.5z"/><path d="M14 2.5v5h5"/><path d="m8.5 15 2 2 5-5"/>',
 'bell': '<path d="M6 16V11a6 6 0 0 1 12 0v5l1.5 2h-15z"/><path d="M10 20.5a2 2 0 0 0 4 0"/>',
 'phone': '<path d="M5 3.5h3.5l1.5 4.5-2 1.5a12 12 0 0 0 6.5 6.5l1.5-2 4.5 1.5V19a1.5 1.5 0 0 1-1.5 1.5A16.5 16.5 0 0 1 3.5 5 1.5 1.5 0 0 1 5 3.5z"/>',
 'mail': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3.5 6 8.5 7 8.5-7"/>',
 'clock': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>',
 'pin': '<path d="M12 21.5s7-6.2 7-12a7 7 0 0 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="9.5" r="2.5"/>',
 'school': '<path d="M2.5 9 12 4.5 21.5 9 12 13.5z"/><path d="M6.5 11v5c0 1.5 2.5 3 5.5 3s5.5-1.5 5.5-3v-5M21.5 9v6"/>',
 'book': '<path d="M4 4.5A1.5 1.5 0 0 1 5.5 3H20v15H5.5A1.5 1.5 0 0 0 4 19.5z"/><path d="M4 19.5A1.5 1.5 0 0 0 5.5 21H20v-3"/>',
 'tree': '<path d="M12 21v-5M12 3 6 11h3l-4 5h14l-4-5h3z"/>',
 'alert': '<path d="M12 3 2 20.5h20z"/><path d="M12 10v4.5M12 17.5h.01"/>',
 'bolt': '<path d="M13 2.5 4.5 13.5H12L11 21.5l8.5-11H12z"/>',
 'info': '<circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7.5h.01"/>',
 'chart': '<path d="M3.5 3.5v17h17"/><path d="M8 16v-5M12.5 16V7M17 16v-8"/>',
 'users': '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/><circle cx="17" cy="9" r="2.5"/><path d="M16.5 14.2A5 5 0 0 1 21.5 19"/>',
 'menu': '<path d="M4 7h16M4 12h16M4 17h16"/>',
 'landmark': '<path d="M3 21h18M5 18h14M6 18v-7M10 18v-7M14 18v-7M18 18v-7M3 9l9-6 9 6z"/>',
 'map': '<path d="m9 4.5-6 2v13l6-2 6 2 6-2v-13l-6 2z"/><path d="M9 4.5v13M15 6.5v13"/>',
 'ambulance': '<path d="M2.5 16.5V7h11v9.5M13.5 10h4l3 3.5v3h-7"/><circle cx="7" cy="17.5" r="2"/><circle cx="17" cy="17.5" r="2"/><path d="M8 9.5v4M6 11.5h4"/>',
 'growth': '<path d="M3.5 20.5h17"/><path d="m4 15 5-5 4 3 7-7"/><path d="M15 6h5v5"/>',
 'leaf': '<path d="M5 19c0-8 5-14 15-15-1 10-7 15-15 15z"/><path d="M5 19 13 11"/>',
 'question': '<circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 1 1 3.5 2.3c-.6.3-1 .9-1 1.6v.6M12 17.5h.01"/>',
 'shield': '<path d="M12 3 4.5 6v6c0 4.5 3.2 7.8 7.5 9 4.3-1.2 7.5-4.5 7.5-9V6z"/>',
 'grid': '<rect x="3.5" y="3.5" width="7" height="7" rx="1.5"/><rect x="13.5" y="3.5" width="7" height="7" rx="1.5"/><rect x="3.5" y="13.5" width="7" height="7" rx="1.5"/><rect x="13.5" y="13.5" width="7" height="7" rx="1.5"/>',
 'frontage': '<path d="M3 20.5h18M5 20.5V11l7-5 7 5v9.5"/><path d="M2.5 16h2M19.5 16h2"/><path d="m3 14-1 2 1 2M21 14l1 2-1 2"/>',
 'elder': '<circle cx="11" cy="4.5" r="2"/><path d="M11 7v6l-3 7.5M11 13l3 7.5M8 10h6M17 10v11"/>',
 'school2': '<path d="M3 21V10l9-6 9 6v11"/><path d="M9 21v-5h6v5M12 8.5v2"/>',
}
EMOJI = {'💰':'coins','🏘':'users','🚑':'ambulance','🏫':'school','📏':'frontage','💧':'water','🌲':'tree','📈':'growth','🧓':'elder','🚧':'alert','🏠':'home','🛤':'road','🏡':'home','🗺':'map','🏛':'landmark'}

I.update({
 'play': '<path d="M8 5.5v13l10.5-6.5z" fill="currentColor" stroke="none"/>',
 'video': '<rect x="3" y="6" width="13" height="12" rx="2.5"/><path d="M16 10.5l5-3v9l-5-3"/>',
 'zin': '<circle cx="11" cy="11" r="6.5"/><path d="M16 16l4.5 4.5M8.5 11h5M11 8.5v5"/>',
 'zout': '<circle cx="11" cy="11" r="6.5"/><path d="M16 16l4.5 4.5M8.5 11h5"/>',
 'fit': '<path d="M4 9V5h4M20 9V5h-4M4 15v4h4M20 15v4h-4"/>',
 'chevup': '<path d="m6 15 6-6 6 6"/>',
 'quote': '<path d="M5 6h14v9H9l-4 3.5z"/><path d="M9 10h6"/>',
})

def sprite():
    return '<svg xmlns="http://www.w3.org/2000/svg" width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">' + ''.join(
        f'<symbol id="i-{k}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{v}</symbol>' for k, v in I.items()) + '</svg>'

def ic(n, cls='i'):
    return f'<svg class="{cls}" aria-hidden="true" focusable="false"><use href="#i-{n}"/></svg>'

def A(url, text, cls=''):
    c = f' class="{cls}"' if cls else ''
    if url.startswith('#'):
        return f'<a href="{H.escape(url)}"{c}>{text}</a>'
    return f'<a href="{H.escape(url)}"{c} target="_blank" rel="noopener">{text}<span class="sr"> (opens in new tab)</span></a>'

def share(sec, label):
    return (f'<div class="sechead-tools js-only"><button type="button" class="sharebtn" data-share="{sec}" aria-label="Share a link to {H.escape(label)}">'
            f'{ic("link")}<span>Share this section</span></button></div>')

def plain(text):
    return f'<div class="plain" role="note"><p class="plain-k">{ic("info")} In plain language</p><p>{text}</p></div>'

def render_r3(badge, E):
    out = {}
    # ---------- Directory
    d = []
    d.append('<div class="grid g3 dir-top">'
             f'<div class="card keycard em"><h3>{ic("alert")} Emergency</h3><p class="big">911</p><p>Police non-emergency (603) 899-5009 · after hours (603) 355-2000. Fire (603) 899-3324.</p></div>'
             f'<div class="card keycard"><h3>{ic("building")} Town Offices</h3><p>{E(R.TOWN["addr"])}</p><p><a class="tel" href="tel:+16038995181">{E(R.TOWN["phone"])}</a> · fax {E(R.TOWN["fax"])}</p><p class="note">{E(R.TOWN["hours"])}</p></div>'
             f'<div class="card keycard"><h3>{ic("grid")} Do it online</h3><ul class="linklist">' + ''.join(f'<li>{A(u, E(t))}</li>' for t, u in R.ONLINE) + '</ul></div></div>')
    d.append('<div class="controls js-only" role="search" aria-label="Filter the directory"><div class="row"><div class="searchwrap field"><label for="dq">Find an office or board</label>'
             '<input type="search" id="dq" placeholder="e.g. dog license, permits, library, taxes" autocomplete="off"></div></div><p class="count" id="dcount" aria-live="polite"></p></div>')
    d.append('<h3 class="subh">Town offices and departments</h3><ul class="dirlist" id="dirlist">')
    for i, (o, what, ph, em, hrs, addr, url, labs, note) in enumerate(R.DEPTS):
        tel = re.search(r'\((\d{3})\) (\d{3})-(\d{4})', ph)
        telhref = f'tel:+1{tel.group(1)}{tel.group(2)}{tel.group(3)}' if tel else ''
        q = E(' '.join([o, what, ph, em, hrs, addr, note]).lower())
        d.append(f'<li class="card dir" id="dir-{i}" data-q="{q}"><h4>{E(o)}</h4><p class="what">{E(what)}</p><dl class="dl">'
                 f'<div><dt>{ic("phone")}<span class="sr">Phone</span></dt><dd>' + (f'<a class="tel" href="{telhref}">{E(ph)}</a>' if telhref else E(ph)) + '</dd></div>'
                 + (f'<div><dt>{ic("mail")}<span class="sr">Email</span></dt><dd>' + ' · '.join(f'<a href="mailto:{E(x.strip())}">{E(x.strip())}</a>' for x in em.split('·')) + '</dd></div>' if em else '')
                 + f'<div><dt>{ic("clock")}<span class="sr">Hours</span></dt><dd>{E(hrs)}</dd></div><div><dt>{ic("pin")}<span class="sr">Where</span></dt><dd>{E(addr)}</dd></div></dl>'
                 + (f'<p class="note">{E(note)}</p>' if note else '') + f'<p class="lsrc">{badge(*labs)} {A(url, "Town page")}</p></li>')
    d.append('</ul><h3 class="subh">Boards and committees</h3><p class="note">Members are listed on each board\'s town page. This guide lists schedules and contacts only.</p><ul class="dirlist">')
    for i, (b, sch, con, url, labs, note) in enumerate(R.BOARDS3):
        q = E(' '.join([b, sch, con, note]).lower())
        d.append(f'<li class="card dir" id="board-{i}" data-q="{q}"><h4>{E(b)}</h4><p>{E(sch)}</p><p class="what">{ic("phone")} {E(con)}</p>'
                 + (f'<p class="note">{E(note)}</p>' if note else '') + f'<p class="lsrc">{badge(*labs)} {A(url, "Town page")}</p></li>')
    d.append('</ul><p class="empty" id="dempty" hidden>No office matches. Try another word, or call the Town Offices at (603) 899-5181.</p>')
    d.append('<div class="card gapcard"><h3>Not confirmed yet</h3><ul class="facts">' + ''.join(f'<li>{E(g)} {badge("unconf")}</li>' for g in R.DIR_GAPS) + '</ul></div>')
    out['DIRECTORY'] = ''.join(d)

    # ---------- How do I
    h = ['<ul class="howgrid" id="howlist">']
    for i, (q, icon, steps, det, who, legal, labs, links, gaps) in enumerate(R.GUIDES):
        gid = 'how-' + re.sub(r'[^a-z]+', '-', q.lower()).strip('-')[:40]
        h.append(f'<li><details class="card how" id="{gid}"><summary>{ic(icon, "i ico")}<h3 class="hq sum-h">How do I {E(q)}</h3>{ic("chev", "i chev")}</summary><div class="body">'
                 '<h4>Steps</h4><ol class="steps">' + ''.join(f'<li>{E(s)}</li>' for s in steps) + '</ol>'
                 + ''.join(f'<p><strong>{E(k)}.</strong> {E(v)}</p>' for k, v in det)
                 + f'<p><strong>Who handles it.</strong> {E(who)}</p>' + (f'<p><strong>Legal basis.</strong> {E(legal)}</p>' if legal else '')
                 + '<p class="lsrc">' + badge(*labs) + ' ' + ' · '.join(A(u, E(t)) for t, u in links) + '</p>'
                 + (('<div class="gapnote"><strong>Check first:</strong><ul>' + ''.join(f'<li>{E(g)}</li>' for g in gaps) + '</ul></div>') if gaps else '')
                 + '</div></details></li>')
    h.append('</ul><p class="note">Summary, not legal advice. Fees and dates were checked on Oct 9, 2026. Confirm with the office named in each guide.</p>')
    out['HOWTO'] = ''.join(h)

    # ---------- Budget
    money = lambda n: f"${n:,.0f}"
    b = ['<div class="grid g4">' + ''.join(f'<div class="card stat"><div class="n">{E(n)}</div><div class="l">{E(l)}</div><div class="s">{badge(*c)}</div></div>' for n, l, c in R.BUDGET_STATS) + '</div>']
    b.append('<div class="card"><h3>Read this first</h3><ul class="facts">' + ''.join(f'<li>{E(t)} {badge(*c)}</li>' for t, c in R.FIN_NOTES) + '</ul></div>')
    top = sorted(R.DEPTBUD, key=lambda r: -r[4])[:10]
    mx = top[0][4]
    b.append(f'<div class="card chart"><h3>Where the 2026 default budget goes: the 10 largest lines {badge("official")}</h3><p class="note" style="margin-top:0">2026 default budget by department, from the 2025 Annual Report. Bars share one scale. The full table of all {len(R.DEPTBUD)} lines is below.</p>')
    for r in top:
        w = r[4] / mx * 100
        b.append(f'<div class="hb lab"><span class="y sm">{E(r[0])}</span><span class="track"><span class="fill f-brand" style="--w:{w:.2f}%"></span></span><span class="v">{money(r[4])} · {r[4]/R.DEPTBUD_TOT[3]*100:.1f}% of total</span></div>')
    b.append('<details class="tabledetails"><summary>Show details: all department lines, 2025 and 2026</summary><div class="tablewrap"><table class="data"><caption>Department budgets (2025 Annual Report, pages 72–83)</caption>'
             '<thead><tr><th scope="col">Department</th><th class="num" scope="col">2025 budget (default)</th><th class="num" scope="col">2025 actual</th><th class="num" scope="col">2026 proposed (failed)</th><th class="num" scope="col">2026 default (in effect)</th></tr></thead><tbody>'
             + ''.join(f'<tr><th scope="row">{E(r[0])}</th>' + ''.join(f'<td class="num">{money(x)}</td>' for x in r[1:]) + '</tr>' for r in R.DEPTBUD)
             + '<tr><th scope="row">Total (as printed)</th>' + ''.join(f'<td class="num"><strong>{money(x)}</strong></td>' for x in R.DEPTBUD_TOT) + '</tr></tbody></table></div>'
             + f'<p class="note">Sum of the lines shown for 2026 default: {money(sum(r[4] for r in R.DEPTBUD))}. Animal Control and ARPA lines print fewer columns and are not shown, so the lines do not add exactly to the printed total.</p></details></div>')
    # reserves chart
    rmx = max(max(r[1], r[2] or 0) for r in R.RESERVES)
    b.append(f'<div class="card chart"><h3>Capital reserve and trust funds, end of 2025 vs end of 2024 {badge("official")}</h3><ul class="keyrow"><li><i style="--sc:var(--brand2)"></i>End 2025</li><li><i style="--sc:var(--neutral2)"></i>End 2024</li></ul>')
    for name, a, p in R.RESERVES:
        b.append(f'<div class="hb lab"><span class="y sm">{E(name)}</span><span class="pair"><span class="track thin"><span class="fill f-brand" style="--w:{a/rmx*100:.2f}%"></span></span>'
                 + (f'<span class="track thin"><span class="fill f-b" style="--w:{p/rmx*100:.2f}%"></span></span>' if p is not None else '<span class="track thin gaptrack"></span>')
                 + f'</span><span class="v">{money(a)} · ' + (f'{money(p)} in 2024' if p is not None else 'new in 2025') + '</span></div>')
    b.append(f'<p class="note">Totals: {money(R.RES_TOT[0])} (2025) vs {money(R.RES_TOT[1])} (2024). End-2023 total was $423,914. Source: 2025 Annual Report pages 40–42; 2024 Annual Report page 41.</p></div>')
    def arts(rows, lab):
        s = ''
        for t, y, n, p in rows:
            s += (f'<div class="bar"><div class="lbl"><span>{E(t)} <span class="result {"r-pass" if p else "r-fail"}">{"Passed" if p else "Failed"}</span></span><b>{y:,}–{n:,}</b></div>'
                  f'<div class="track mid"><span class="fill {"f-yes" if p else "f-no"}" style="--w:{y/(y+n)*100:.2f}%"></span></div></div>')
        return s
    b.append(f'<div class="grid g2"><div class="card chart"><h3>2025 money articles {badge("official")}</h3><p class="note" style="margin-top:0">Share voting yes; the dashed line is 50%.</p>{arts(R.ART25, "official")}</div>'
             f'<div class="card chart"><h3>2026 money articles {badge("press")}</h3><p class="note" style="margin-top:0">All seven fund articles passed. Results are press-reported.</p>{arts(R.ART26, "press")}<p class="note">{E(R.ART26_NOTFOUND)}</p></div></div>')
    b.append('<div class="grid g2"><div class="card"><h3>Debt and the fiber bond</h3><ul class="facts">' + ''.join(f'<li>{E(t)} {badge(*c)}</li>' for t, c in R.DEBT) + '</ul></div>'
             '<div class="card"><h3>Capital Improvement Program (CIP)</h3><ul class="facts">' + ''.join(f'<li>{E(t)} {badge(*c)}</li>' for t, c in R.CIP) + '</ul></div></div>')
    b.append('<div class="card gapcard"><h3>Not found</h3><ul class="facts">' + ''.join(f'<li>{E(g)} {badge("gap")}</li>' for g in R.FIN_GAPS) + '</ul>'
             f'<p class="lsrc">{A(R.AR25, "2025 Annual Report")} · {A(R.AR24, "2024 Annual Report")}</p></div>')
    out['BUDGET'] = ''.join(b)

    # ---------- Schools and community
    s = [f'<div class="grid g2"><div class="card"><h3>{ic("school")} {E(R.SAU[0])} {badge("official")}</h3><p>{E(R.SAU[1])} · {A(R.SAU[2], "sau47.org")}</p><p>{E(R.SAU[3])}</p>'
         '<div class="tablewrap"><table class="data"><caption>Schools serving Rindge (NH DOE); enrollment 2024–25 (NCES)</caption><thead><tr><th scope="col">School</th><th scope="col">Grades</th><th scope="col">Address and phone</th><th class="num" scope="col">Students</th></tr></thead><tbody>'
         + ''.join(f'<tr><th scope="row">{E(n)}</th><td>{E(g)}</td><td>{E(a)}<br>{E(p)}</td><td class="num">{E(c)}</td></tr>' for n, g, a, p, c in R.SCHOOLS)
         + '</tbody></table></div><p class="note">2023–24 enrollment differed (Rindge Memorial 319, Conant High 368, Conant Middle 257). Franklin Pierce University, Hampshire Country School and Heritage Christian School are also listed by the town.</p></div>'
         f'<div class="card"><h3>{ic("vote")} Recent school votes {badge("press")}</h3><ul class="facts">' + ''.join(f'<li>{E(t)} {A(u, "Source")}</li>' for t, u in R.SCHOOL_VOTES)
         + '</ul><p class="note">School budgets are voted separately from the town budget and are not in the town\'s annual report. The Nov 3, 2026 ballot includes the statewide school tax-cap question (HB 1300).</p></div></div>']
    s.append(f'<div class="card"><h3>{ic("calendar")} Coming up in the community</h3><ul class="facts">' + ''.join(f'<li><strong>{E(dt)}.</strong> {E(t)} {badge(*c)}</li>' for dt, t, c in R.EVENTS) + '</ul></div>')
    s.append('<ul class="laws commgrid">' + ''.join(f'<li class="law" style="--c:var(--cc)"><h4>{E(t)}</h4><p>{E(x)}</p><p class="lsrc">{badge(*c)} {A(u, "Website")}</p></li>' for t, x, c, u in R.COMMUNITY) + '</ul>')
    out['SCHOOLS'] = ''.join(s)

    # ---------- Emergency and utilities
    e = [f'<div class="card keycard em big911"><p class="big">911</p><p>Police, fire or medical emergency. Call or text 911.</p></div><div class="grid g2"><div class="card"><h3>{ic("shield")} Emergency services</h3><ul class="facts">'
         + ''.join(f'<li><strong>{E(t)}.</strong> {E(x)} {badge(*c)}' + (f' {A(u, "Source")}' if u else '') + '</li>' for t, x, c, u in R.EMERG)
         + f'</ul></div><div class="card"><h3>{ic("bolt")} Utilities</h3><ul class="facts">'
         + ''.join(f'<li><strong>{E(t)}.</strong> {E(x)} {badge(*c)}' + (f' {A(u, "Source")}' if u else '') + '</li>' for t, x, c, u in R.UTIL) + '</ul></div></div>']
    out['EMERG'] = ''.join(e)

    # ---------- Facts
    f = ['<dl class="factgrid">' + ''.join(f'<div class="card"><dt>{E(t)}</dt><dd>{E(x)} {badge(*c)}</dd></div>' for t, x, c in R.FACTS) + '</dl>'
         '<p class="lsrc">' + ' · '.join(A(u, E(t)) for t, u in R.FACT_LINKS) + '</p>']
    out['FACTS'] = ''.join(f)
    return out

# ---------------- post-processing ----------------
def post(page):
    for k, v in EMOJI.items():
        page = page.replace(k + '\ufe0f', ic(v, 'i')).replace(k, ic(v, 'i'))
    soup = BeautifulSoup(page, 'lxml')
    # collect cited links
    links = [a for a in soup.find_all('a', href=True) if re.match(r'https?://', a['href'])]
    texts = {}
    for a in links:
        t = a.get_text(' ', strip=True)
        t = re.sub(r'\s*\(opens in new tab\)\s*$', '', t)
        if a['href'] not in texts or len(t) > len(texts[a['href']]): texts[a['href']] = t
    urls = sorted(set(a['href'] for a in links))
    reg = VD.registry(urls, texts)
    for a in links:
        e = reg[a['href']]
        a['data-doc'] = e['id']
    # ids for search
    for n, el in enumerate(soup.select('details.topic')):
        el['id'] = el.get('id') or f'topic-{n}'
    for n, el in enumerate(soup.select('#lawlist .law')):
        el['id'] = el.get('id') or f'law-{n}'
    for n, el in enumerate(soup.select('.gl-item')):
        el['id'] = el.get('id') or f'gl-{n}'
    for pre, sel in (('ev', '#tl .ev'), ('up', '#ulist .urow'), ('iss', 'article.issue'), ('how', 'details.how'), ('dir', '.dir')):
        for n, el in enumerate(soup.select(sel)):
            if not el.get('id'): el['id'] = f'{pre}-x{n}'
    idx = []
    def add(kind, title, text, href):
        idx.append(dict(k=kind, t=re.sub(r'\s+', ' ', title).strip()[:140], s=re.sub(r'\s+', ' ', text).strip()[:240], h=href))
    for s in soup.select('section.sec[id]'):
        h2 = s.find('h2')
        if h2: add('Section', h2.get_text(' ', strip=True), (s.select_one('.summary') or s.select_one('.plain p:not(.plain-k)') or s.select_one('.intro') or h2).get_text(' ', strip=True), '#' + s['id'])
    for el in soup.select('#tl .ev'):
        add('Meeting', el.select_one('.date').get_text(' ', strip=True) + ' · ' + el.select_one('.bname').get_text(' ', strip=True), (el.select_one('.ttl').get_text(' ', strip=True) if el.select_one('.ttl') else '') + ' ' + ' '.join(li.get_text(' ', strip=True) for li in el.select('ul > li')), '#' + el['id'])
    for el in soup.select('#ulist .urow'):
        add('Date', el.select_one('.dd').get_text(' ', strip=True), el.select('div')[1].get_text(' ', strip=True), '#' + el['id'])
    for el in soup.select('details.topic'):
        add('Topic', el.select_one('summary').get_text(' ', strip=True), el.select_one('.body').get_text(' ', strip=True)[:240], '#' + el['id'])
    for el in soup.select('article.issue'):
        add('Recurring issue', el.select_one('h3').get_text(' ', strip=True), el.select_one('p').get_text(' ', strip=True), '#' + el['id'])
    for el in soup.select('#lawlist .law'):
        add('Law', el.select_one('h4').get_text(' ', strip=True), (el.select_one('p') or el).get_text(' ', strip=True), '#' + el['id'])
    for el in soup.select('.gl-item'):
        add('Glossary', el.select_one('dt').get_text(' ', strip=True), el.select_one('dd').get_text(' ', strip=True), '#' + el['id'])
    for el in soup.select('details.how'):
        add('How do I', el.select_one('.hq').get_text(' ', strip=True), el.select_one('.steps').get_text(' ', strip=True), '#' + el['id'])
    for el in soup.select('.dir'):
        add('Directory', el.select_one('h4').get_text(' ', strip=True), el.get_text(' ', strip=True)[len(el.select_one('h4').get_text()):], '#' + el['id'])
    for e in reg.values():
        add('Document', e['title'], ' · '.join(str(x) for x in (e.get('board') or e.get('org'), e.get('type'), e.get('year')) if x), 'doc:' + e['id'])
    # library
    lib = library(reg)
    docdata = {e['id']: {k: e.get(k) for k in ('title', 'src', 'kind', 'view', 'file', 'board', 'type', 'year', 'org', 'host', 'hls', 'dur', 'date', 'chapters') if e.get(k) not in (None, [])} for e in reg.values()}
    import v4post; v4post.enhance(soup, reg)
    page = str(soup)
    page = page.replace('{{LIBRARY}}', lib)
    page = page.replace('{{DOCDATA}}', json.dumps(docdata, separators=(',', ':')).replace('</', '<\\/'))
    page = page.replace('{{SEARCHDATA}}', json.dumps(idx, separators=(',', ':')).replace('</', '<\\/'))
    page = page.replace('{{SPRITE}}', sprite())
    page = page.replace('{{NDOCS}}', str(sum(1 for e in reg.values() if e['kind'] in ('pdf', 'word'))))
    # library links need data-doc too (added post-soup)
    return page, reg, idx

KINDLABEL = {'video': 'Plays here', 'large': 'Large scan: opens on rindgenh.org', 'pdf': 'Opens here (copy)', 'word': 'Opens here (converted copy)', 'embed': 'Opens here', 'ext': 'Opens in a new tab', 'missing': 'Not available'}
def library(reg):
    rows = sorted(reg.values(), key=lambda e: (e.get('board') or e.get('org') or '', -(e.get('year') or 0), e.get('date') or '', e['title']))
    boards = sorted(set((e.get('board') or e.get('org') or 'Other') for e in rows))
    types = sorted(set(e.get('type') or 'Other' for e in rows))
    years = sorted(set(e.get('year') for e in rows if e.get('year')), reverse=True)
    opt = lambda vals: ''.join(f'<option value="{H.escape(str(v))}">{H.escape(str(v))}</option>' for v in vals)
    o = [f'<div class="controls js-only" role="search" aria-label="Filter documents"><div class="row">'
         f'<div class="searchwrap field"><label for="libq">Search documents</label><input type="search" id="libq" placeholder="e.g. minutes, zoning ordinance, 2025, wetlands" autocomplete="off"></div>'
         f'<div class="field"><label for="libb">Board or source</label><select id="libb"><option value="">All</option>{opt(boards)}</select></div>'
         f'<div class="field"><label for="libt">Type</label><select id="libt"><option value="">All</option>{opt(types)}</select></div>'
         f'<div class="field"><label for="liby">Year</label><select id="liby"><option value="">All</option>{opt(years)}</select></div></div>'
         f'<p class="count" id="libcount" aria-live="polite"></p></div>'
         '<div class="tablewrap libwrap"><table class="data lib" id="libtable"><caption class="sr">All documents cited on this site</caption><thead><tr><th scope="col">Document</th><th scope="col">Board or source</th><th scope="col">Type</th><th scope="col">Year</th><th scope="col">Open</th></tr></thead><tbody>']
    for e in rows:
        b = e.get('board') or e.get('org') or 'Other'
        view = e.get('view') or e['src']
        kind = e['kind']
        q = H.escape(' '.join(str(x) for x in (e['title'], b, e.get('type'), e.get('year'), e['src']) if x).lower())
        tgt = '' if kind in ('pdf', 'word', 'video') else ' target="_blank" rel="noopener"'
        main = f'<a class="docbtn" href="{H.escape(view)}" data-doc="{e["id"]}"{tgt}>{ic("play" if kind == "video" else ("doc" if kind in ("pdf","word","embed") else "external"))}<span>{"Play" if kind == "video" else ("View" if kind != "missing" else "Details")}</span><span class="sr"> {H.escape(e["title"])}</span></a>'
        orig = f'<a class="origlink" href="{H.escape(e["src"])}" target="_blank" rel="noopener">Original<span class="sr"> on {H.escape(e.get("host",""))} (opens in new tab)</span></a>'
        o.append(f'<tr data-b="{H.escape(b)}" data-t="{H.escape(e.get("type") or "Other")}" data-y="{e.get("year") or ""}" data-q="{q}"><td><span class="dt">{H.escape(e["title"])}</span><span class="dk">{KINDLABEL[kind]}</span></td>'
                 f'<td>{H.escape(b)}</td><td>{H.escape(e.get("type") or "")}</td><td>{e.get("year") or ""}</td><td class="open">{main}{orig}</td></tr>')
    o.append('</tbody></table></div><p class="empty" id="libempty" hidden>No documents match. Try fewer words.</p>')
    return ''.join(o)
