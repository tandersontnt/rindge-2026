"""v4: expandable cards (accordion in place) + video link labels. Runs on the BeautifulSoup tree in v3.post.
Rules: a card becomes expandable only when it has content beyond its visible summary (no dead cards).
Without JavaScript every card simply shows everything (CSS: html:not(.js))."""
import re, copy, html as H
from bs4 import BeautifulSoup, NavigableString

def ic(n): return f'<svg class="i" aria-hidden="true" focusable="false"><use href="#i-{n}"/></svg>'
def frag(soup, s): return BeautifulSoup(s, 'html.parser')
def txt(el): return re.sub(r'\s+', ' ', el.get_text(' ', strip=True)) if el else ''
def plural(n, w): return f"{n} {w}{'' if n == 1 else 's'}"
def clip(s, n=150):
    s = re.sub(r'\s+', ' ', s).strip()
    return s if len(s) <= n else s[:n].rsplit(' ', 1)[0].rstrip(',;:') + '…'

def make(soup, card, head_keep, body_nodes, title, meta, peek=None, extra_html=''):
    """card: element. head_keep: nodes that stay visible. body_nodes: nodes moved into the collapsible body."""
    if not card.get('id'):
        make.n = getattr(make, 'n', 0) + 1; card['id'] = f'card-{make.n}'
    cid = card['id']
    bid = cid + '-more'
    card['class'] = (card.get('class') or []) + ['xc']
    body = soup.new_tag('div', attrs={'class': 'xc-body', 'id': bid, 'role': 'region', 'aria-label': 'Details: ' + clip(title, 80)})
    inner = soup.new_tag('div', attrs={'class': 'xc-in'})
    body.append(inner)
    for n in body_nodes: inner.append(n.extract())
    if extra_html: inner.append(frag(soup, extra_html))
    tog = frag(soup, f'<button type="button" class="xc-tog js-only" aria-expanded="false" aria-controls="{bid}">'
                     f'<span class="xc-l"><span class="xc-open">Details</span><span class="xc-close">Hide details</span></span>'
                     f'{"<span class=xc-meta>" + H.escape(meta) + "</span>" if meta else ""}{ic("chev")}</button>')
    last = head_keep[-1] if head_keep else None
    if peek:
        p = frag(soup, f'<p class="xc-peek js-only" aria-hidden="true">{H.escape(peek)}</p>')
        if last: last.insert_after(p); last = card.select_one('.xc-peek')
        else: card.insert(0, p)
    if last: last.insert_after(tog)
    else: card.append(tog)
    card.select_one('.xc-tog').insert_after(body)

def docs_meta(card):
    a = card.select('.docs a[data-doc], a[data-doc]')
    names = []
    for x in a:
        t = txt(x).replace('(opens in new tab)', '').strip()
        t = 'Video' if 'Video' in t or 'video' in t else t
        if t and t not in names: names.append(t)
    return names

def enhance(soup, reg):
    byid = {e['id']: e for e in reg.values()}
    # video links: clear label + play icon (JS opens the in-site player; no-JS opens Town Hall Streams)
    for a in soup.select('a[data-doc]'):
        e = byid.get(a['data-doc'])
        if e and e['kind'] == 'video' and not a.find_parent(class_='docbtn') and 'docbtn' not in (a.get('class') or []):
            a['class'] = (a.get('class') or []) + ['vidlink']
            sr = a.select_one('.sr')
            for c in list(a.contents):
                if c is not sr: c.extract()
            a.insert(0, frag(soup, ic('play') + '<span>Watch the video</span>'))
    # ---------------- timeline meetings
    for ev in soup.select('#tl .ev'):
        hd, ttl = ev.select_one('.hd'), ev.select_one('.ttl')
        ul, dc = ev.select_one(':scope > ul'), ev.select_one(':scope > .docs')
        body = [x for x in (ul, dc) if x]
        if not body: continue
        notes = len(ul.find_all('li', recursive=False)) if ul else 0
        names = docs_meta(ev)
        meta = ' · '.join(([plural(notes, 'note')] if notes else []) + names[:4])
        peek = clip(txt(ul.find('li')), 140) if ul else None
        if dc:
            h = frag(soup, '<p class="xc-k">Documents and video</p>' if 'Video' in names else '<p class="xc-k">Documents</p>')
            dc.insert_before(h)
            body = [x for x in (ul, ev.select_one('.xc-k'), dc) if x]
        extra = f'<p class="xc-foot"><a class="xc-link" href="#{ev["id"]}">{ic("link")}<span>Link to this meeting</span></a></p>'
        make(soup, ev, [ttl or hd], body, txt(ev.select_one('.bname')) + ' ' + txt(ev.select_one('.date')), meta, peek, extra)
    # ---------------- recurring issues
    for iss in soup.select('article.issue'):
        ol = iss.select_one('ol.mtl')
        if not ol: continue
        head = [x for x in (iss.select_one('header'), iss.select_one(':scope > p'), iss.select_one('dl.fl2')) if x]
        rest = [x for x in iss.find_all(recursive=False) if x not in head]
        n = len(ol.find_all('li', recursive=False))
        extra = f'<p class="xc-foot"><a class="xc-link" href="#{iss.get("id","")}">{ic("link")}<span>Link to this issue</span></a></p>'
        make(soup, iss, head, rest, txt(iss.select_one('h3')), plural(n, 'event') + ' with sources', None, extra)
    # ---------------- laws
    for law in soup.select('li.law'):
        ps = law.find_all('p', recursive=False)
        h = law.select_one(':scope > .lh') or law.select_one(':scope > h4')
        if not ps: continue
        first = ps[0]
        rest = [x for x in law.find_all(recursive=False) if x not in (h, first)]
        if not rest: continue
        first['class'] = (first.get('class') or []) + ['xc-clamp']
        what = 'What it means for Rindge · source' if law.select_one('.rin') else 'Source'
        make(soup, law, [h, first], rest, txt(law.select_one('h4')), what)
    # ---------------- directory
    for dr in soup.select('li.dir'):
        dl = dr.select_one('dl.dl')
        h4, what = dr.select_one('h4'), dr.select_one('.what')
        rows = dl.find_all('div', recursive=False) if dl else []
        phone = [r for r in rows if r.select_one('a.tel')]
        others = [r for r in rows if r not in phone]
        tail = [x for x in dr.find_all(recursive=False) if x not in (h4, what, dl)]
        if not others and not tail: continue
        head = [x for x in (h4, what) if x]
        if phone:
            pdl = soup.new_tag('dl', attrs={'class': 'dl dl-main'})
            for r in phone: pdl.append(r.extract())
            (what or h4).insert_after(pdl); head.append(pdl)
        labels = [txt(r.select_one('dt .sr')) for r in others]
        meta = ', '.join(x for x in labels if x) + (' · source' if tail else '')
        body = ([dl] if others else []) + tail
        if not others and dl: dl.decompose()
        make(soup, dr, head, body, txt(h4), meta[:1].upper() + meta[1:])
    # ---------------- calendar rows: related meeting record, the board's regular details, related rules and guides
    dirs = {txt(d.select_one('h4')).lower(): d for d in soup.select('li.dir')}
    laws = soup.select('li.law')
    hows = soup.select('details.how')
    for row in soup.select('#ulist .urow'):
        cells = row.find_all('div', recursive=False)
        if len(cells) < 2: continue
        who = txt(row.select_one('.who')).lstrip('· ').strip()
        text = txt(cells[1]).replace(txt(row.select_one('.who')), '')
        parts = []
        m = re.match(r'up-(\d{4}-\d\d-\d\d)', row['id'])
        ev = None
        if m:
            for e in soup.select(f'#tl .ev[id$="{m.group(1)}"]'):
                if e.get('style') == row.get('style'): ev = e
        if ev:
            items = ''.join(str(li) for li in ev.select('.xc-in > ul > li'))
            dl = ev.select_one('.xc-in .docs')
            parts.append('<p class="xc-k">From the meeting record</p>' + (f'<ul>{items}</ul>' if items else '') + (str(dl) if dl else '') +
                         f'<p><a class="xc-link" href="#{ev["id"]}">{ic("calendar")}<span>See this meeting in the timeline</span></a></p>')
        d = dirs.get(who.lower()) or next((v for k, v in dirs.items() if who and (k.startswith(who.lower()) or who.lower() in k)), None)
        if d:
            rows = d.select('dl div')
            lines = ''.join(f'<li>{txt(r.select_one("dt .sr"))}: {r.select_one("dd").decode_contents()}</li>' for r in rows if r.select_one('dd') and r.select_one('dt .sr'))
            parts.append(f'<p class="xc-k">About the {H.escape(txt(d.select_one("h4")))}</p><ul class="xc-facts">{lines}</ul>'
                         f'<p><a class="xc-link" href="#{d["id"]}">{ic("phone")}<span>Contact details in the directory</span></a></p>')
        rel = []
        for rsa in re.findall(r'RSA (\d+(?:-[A-Z])?:\d+(?:-[a-z])?)', text):
            for l in laws:
                if (rsa.lower() in (l.get('data-q') or '')) and l['id'] not in [x[0] for x in rel]:
                    rel.append((l['id'], txt(l.select_one('h4')), 'scale'))
        kw = [('petition', 'petition'), ('zoning', 'zoning'), ('election', 'vote'), ('ballot', 'vote'), ('voting', 'vote'), ('candidate', 'office')]
        for k, hk in kw:
            if k in text.lower():
                for h in hows:
                    q = txt(h.select_one('.hq'))
                    if hk in q.lower() and h['id'] not in [x[0] for x in rel]: rel.append((h['id'], q, 'question'))
        # topic relations (keyword -> existing law / guide / topic on this site)
        TOP = [(r'zoning', ['law-47', 'law-49', 'topic-1']), (r'deliberative|warrant', ['law-55', 'law-56']), (r'budget and bond hearing', ['law-57', 'topic-2']),
               (r'candidate', ['how-register-to-vote-or-vote-absentee']), (r'voting session|election', ['how-register-to-vote-or-vote-absentee', 'law-55']),
               (r'select board|planning board|zoning board|conservation', ['how-go-to-or-watch-a-meeting'])]
        for rx, ids in TOP:
            if re.search(rx, text.lower() + (' ' + who.lower() if 'board' in rx else '')):
                for i in ids:
                    el = soup.find(id=i)
                    if el is None or i in [x[0] for x in rel]: continue
                    t = el.select_one('.hq') if i.startswith('how') else (el.select_one('summary .sum-h') or el.select_one('summary') if i.startswith('topic') else el.select_one('h4'))
                    rel.append((i, txt(t), 'scale' if i.startswith('law') else ('question' if i.startswith('how') else 'info')))
        if rel:
            parts.append('<p class="xc-k">Related rules and guides</p><ul class="xc-rel">' + ''.join(
                f'<li><a class="xc-link" href="#{i}">{ic(c)}<span>{H.escape(clip(t, 90))}</span></a></li>' for i, t, c in rel[:5]) + '</ul>')
        if not parts: continue
        meta = ' · '.join(x for x in (('Meeting record' if ev else ''), ('Board details' if d else ''), (plural(len(rel[:5]), 'related link') if rel else '')) if x)
        make(soup, row, cells, [], txt(cells[0]) + ' ' + clip(text, 60), meta, None, ''.join(parts))
    # ---------------- stat cards: where the number comes from and where to see more
    STAT = [
        ('Population, 2020 Census', ['d47', 'd46'], [('#facts', 'Town facts and history')]),
        ('Population estimate', ['d47', 'd46'], [('#facts', 'Town facts and history')]),
        ('2025 tax rate', ['d93', 'd133'], [('#taxcard', 'Tax rate chart, 2020–2025'), ('#ch-tax', 'Tax rate trend since 2011')]),
        ('Average residential value change', ['d19'], [('#ch-reval', 'Revaluation chart'), ('#trends', 'Trends')]),
        ('total property tax commitment', ['d93'], [('#budget', 'Budget and spending')]),
        ('2026 default operating budget', [], [('#budget', 'Budget and spending'), ('#election', 'March 2026 election results')]),
        ('Elderly exemptions in 2025', ['d119'], [('#ch-elderly', 'Elderly exemptions by year'), ('#numbers', 'Rindge by the numbers')]),
        ('Solar exemptions', ['d176'], [('#ev-sb-2026-02-25', 'The Feb 25, 2026 Select Board meeting')]),
        ('2026 default budget', ['d292'], [('#election', 'March 2026 election results')]),
        ('2025 actual spending', ['d292'], []), ('Capital reserves', ['d292'], []), ('debt service', ['d292'], []),
    ]
    for n, st in enumerate(soup.select('.card.stat')):
        lab = txt(st.select_one('.l'))
        spec = next((s for s in STAT if s[0].lower() in lab.lower()), None)
        if not spec: continue
        st['id'] = st.get('id') or f'stat-{n}'
        src = [byid[i] for i in spec[1] if i in byid]
        links = [(h, t) for h, t in spec[2] if h == '#numbers' or soup.find(id=h[1:]) is not None]
        if not src and not links: continue
        out = []
        if src:
            out.append('<p class="xc-k">Where to check this number</p><ul class="xc-rel">' + ''.join(
                f'<li><a class="xc-link" href="{H.escape(e["src"])}" data-doc="{e["id"]}" target="_blank" rel="noopener">{ic("doc" if e["kind"] in ("pdf", "word") else "external")}<span>{H.escape(clip(e["title"], 90))}</span><span class="sr"> (opens in new tab)</span></a></li>' for e in src) + '</ul>')
        if links:
            out.append('<p class="xc-k">See more on this site</p><ul class="xc-rel">' + ''.join(
                f'<li><a class="xc-link" href="{h}">{ic("next")}<span>{H.escape(t)}</span></a></li>' for h, t in links) + '</ul>')
        make(soup, st, [st.select_one('.s') or st.select_one('.l')], [], lab, 'Source' + (' and more' if links else ''), None, ''.join(out))
