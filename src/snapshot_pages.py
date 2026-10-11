# Saves in-site copies of cited outside material so it opens inside the guide. Runs in GitHub Actions
# (.github/workflows/snapshot.yml), because the authoring environment cannot reach these hosts.
#   1. Large town PDFs listed in MANIFEST.json "not_copied" are downloaded byte for byte (GitHub's per-file limit is 100 MB).
#   2. Public GOVERNMENT web pages are saved as readable copies in docs/pages/ (main text only, scripts removed,
#      links made absolute, a banner naming the source, capture date and the original link). Copies are labeled; the original is authoritative.
#   3. Every other outside link is header-checked; hosts that allow framing are recorded so the viewer can show them live.
# Private and commercial sites (news, businesses, payment and registration services) are never copied.
# Usage: python3 src/snapshot_pages.py [index.html]
import json, os, re, sys, hashlib, datetime, urllib.parse, urllib.request, html as H, ssl
from bs4 import BeautifulSoup

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, 'docs'); P = os.path.join(D, 'pages'); M = os.path.join(D, 'MANIFEST.json')
PM = os.path.join(P, 'MANIFEST.json')
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36'
NOW = datetime.datetime.now().astimezone()
GOV = ('rindgenh.org', 'rindgenh.gov', 'gencourt.state.nh.us', 'gc.nh.gov', 'des.nh.gov', 'revenue.nh.gov', 'sos.nh.gov',
       'nhes.nh.gov', 'dncr.nh.gov', 'census.gov', 'co.cheshire.nh.us')
NEVER = ('pay.', 'recdesk.com', 'genasys.com', 'avitarassociates.com', 'mytownview.com', 'nhdeeds.org', 'citizenportal.ai', 'townhallstreams.com')
ARCHIVE_PAGES = ('scholars.unh.edu', 'catalog.hathitrust.org', 'archive.org')  # library catalogs: frame-check only


def is_gov(host): return any(host == g or host.endswith('.' + g) for g in GOV)


def fetch(url, timeout=60, head=False):
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': 'text/html,application/xhtml+xml,application/pdf;q=0.9,*/*;q=0.8', 'Accept-Language': 'en-US,en;q=0.9'}, method='HEAD' if head else 'GET')
    with urllib.request.urlopen(req, timeout=timeout, context=ssl.create_default_context()) as r:
        return r.status, dict((k.lower(), v) for k, v in r.headers.items()), (b'' if head else r.read()), r.geturl()


def frameable(headers):
    xfo = headers.get('x-frame-options', '').lower()
    csp = headers.get('content-security-policy', '').lower()
    if 'deny' in xfo or 'sameorigin' in xfo: return False
    m = re.search(r'frame-ancestors([^;]*)', csp)
    if m and '*' not in m.group(1): return False
    return True


def slug(url):
    p = urllib.parse.urlparse(url)
    s = re.sub(r'[^a-z0-9]+', '-', (p.netloc + p.path).lower()).strip('-')[:70]
    return f"{s}-{hashlib.sha1(url.encode()).hexdigest()[:6]}.html"


def main_content(soup):
    for t in soup(['script', 'style', 'noscript', 'iframe', 'form', 'nav', 'header', 'footer', 'aside', 'svg', 'button', 'input', 'select', 'link', 'meta']):
        t.decompose()
    for sel in ['[role=navigation]', '[role=banner]', '[role=contentinfo]', '.breadcrumb', '.breadcrumbs', '#breadcrumbs', '.skip', '.sr-only',
                '#header', '#footer', '#nav', '.nav', '.menu', '#menu', '.sidebar', '#sidebar', '.social', '.share', '.cookie', '#cookie']:
        for t in soup.select(sel): t.decompose()
    cand = soup.select_one('main, [role=main], #main, #content, #main-content, .main-content, #maincontent, article, .content')
    if cand and len(cand.get_text(' ', strip=True)) > 200: return cand
    best, score = soup.body or soup, 0
    for div in soup.find_all(['div', 'section', 'td']):
        txt = div.get_text(' ', strip=True); n = len(txt) - 3 * len(' '.join(a.get_text(' ', strip=True) for a in div.find_all('a')))
        if n > score: best, score = div, n
    return best


PAGE_CSS = """:root{color-scheme:light dark;--bg:#fff;--ink:#1d1d1f;--muted:#55555c;--line:#d8d8de;--accent:#0a5cb8;--band:#f5f5f7}
@media (prefers-color-scheme:dark){:root{--bg:#1c1c1e;--ink:#f5f5f7;--muted:#b4b4bc;--line:#38383c;--accent:#5aa9ff;--band:#2c2c2e}}
html{font:18px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink)}
.band{background:var(--band);border-bottom:1px solid var(--line);padding:14px 20px;font-size:.88rem;color:var(--muted)}
.band b{color:var(--ink)}.band a{color:var(--accent)}
main{max-width:72ch;margin:0 auto;padding:24px 20px 64px;overflow-wrap:anywhere}
h1{font-size:1.7rem;line-height:1.2;letter-spacing:-.02em;margin:.2em 0 .6em}h2{font-size:1.3rem}h3{font-size:1.1rem}
a{color:var(--accent)}img{max-width:100%;height:auto}
table{border-collapse:collapse;width:100%;font-size:.9rem;display:block;overflow-x:auto}td,th{border:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top}
pre{white-space:pre-wrap}"""


CTRL = re.compile('[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f\ufffd]')


def save_page(url, raw, final):
    soup = BeautifulSoup(raw, 'lxml')
    title = re.sub(r'\s+', ' ', (soup.title.get_text() if soup.title else '') or url).strip()
    title = re.sub(r'\s*[|\-–]\s*(Rindge, NH|Town of Rindge.*|NH General Court.*)$', '', title, flags=re.I) or title
    body = main_content(soup)
    # menu leftovers: tables and lists made only of a few links
    for t in body.find_all(['table', 'ul']):
        links = ' '.join(a.get_text(' ', strip=True) for a in t.find_all('a'))
        if links and len(t.get_text(' ', strip=True)) <= len(links) + 3 and len(links.split()) < 12: t.decompose()
    first = body.find(['h1', 'h2'])
    if first and (re.fullmatch(r'(Rindge, ?NH|Town of Rindge.*|Home)', title, re.I) or first.get_text(' ', strip=True).lower() == title.lower()):
        title = first.get_text(' ', strip=True) or title
        first.decompose()
    for a in body.find_all('a', href=True):
        a['href'] = urllib.parse.urljoin(final, a['href']); a['target'] = '_blank'; a['rel'] = 'noopener'
    for img in body.find_all('img', src=True):
        img['src'] = urllib.parse.urljoin(final, img['src']); img['loading'] = 'lazy'
        for k in list(img.attrs):
            if k not in ('src', 'alt', 'width', 'height', 'loading'): del img[k]
    for t in body.find_all(True):
        for k in list(t.attrs):
            if k.startswith('on') or k in ('style', 'class', 'id'): del t[k]
    text = body.get_text(' ', strip=True)
    if len(text) < 60: return None
    host = urllib.parse.urlparse(url).netloc
    when = NOW.strftime('%b %-d, %Y')
    doc = (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
           f'<meta name="robots" content="noindex"><link rel="canonical" href="{H.escape(url)}"><title>{H.escape(title)}</title><style>{PAGE_CSS}</style></head><body>'
           f'<div class="band"><b>Saved copy</b> of a page from {H.escape(host)}, captured {when}. The original page is authoritative and may have changed. '
           f'<a href="{H.escape(url)}" target="_blank" rel="noopener">Open the original</a></div>'
           f'<main><h1>{H.escape(title)}</h1>{CTRL.sub(" ", body.decode_contents())}</main></body></html>')
    fn = slug(url)
    data = doc.encode('utf-8')
    open(os.path.join(P, fn), 'wb').write(data)
    return dict(file='pages/' + fn, title=title, sha256=hashlib.sha256(data).hexdigest(), bytes=len(data), words=len(text.split()),
                captured=NOW.isoformat(timespec='seconds'), final_url=final)


def main():
    os.makedirs(P, exist_ok=True)
    man = json.load(open(M))
    pm = json.load(open(PM)) if os.path.exists(PM) else {'pages': {}, 'frame': {}, 'errors': {}}
    log = []
    # 1. large PDFs
    keep = []
    for d in man.get('not_copied', []):
        u = d['source_url']
        try:
            st, hd, data, final = fetch(u, timeout=600)
            if st == 200 and data.startswith(b'%PDF') and len(data) < 95_000_000:
                b = urllib.parse.unquote(urllib.parse.urlparse(u).path.rsplit('/', 1)[-1]); b = re.sub(r'[^A-Za-z0-9._-]+', '_', b).strip('_')
                stem, ext = os.path.splitext(b); fn = f"{stem[:70]}_{hashlib.sha1(u.encode()).hexdigest()[:6]}{ext.lower()}"
                open(os.path.join(D, fn), 'wb').write(data)
                man['documents'].append(dict(file=fn, source_url=u, sha256=hashlib.sha256(data).hexdigest(), bytes=len(data),
                                             content_type='application/pdf', retrieved=NOW.isoformat(timespec='seconds')))
                log.append(f'PDF saved {fn} {len(data)}'); continue
            log.append(f'PDF not saved (status {st}, {len(data)} bytes) {u}')
        except Exception as e:
            log.append(f'PDF error {u}: {e}')
        keep.append(d)
    man['not_copied'] = keep
    man['documents'].sort(key=lambda d: d['file'].lower()); man['count'] = len(man['documents']); man['total_bytes'] = sum(d['bytes'] for d in man['documents'])
    json.dump(man, open(M, 'w'), indent=1)
    # 2 + 3. outside links cited on the page
    page = open(sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'index.html')).read()
    have = {d['source_url'] for d in man['documents']}
    urls = sorted(set(u.replace('&amp;', '&') for u in re.findall(r'href="(https?://[^"#]+)"', page)) - have)
    for u in urls:
        host = urllib.parse.urlparse(u).netloc
        if re.search(r'\.(pdf|docx?|xlsx?|zip|mp4|m3u8)(\?|$)', u, re.I): continue
        try:
            st, hd, raw, final = fetch(u)
            ct = hd.get('content-type', '')
            pm['frame'][u] = dict(status=st, frameable=frameable(hd), xfo=hd.get('x-frame-options', ''), checked=NOW.isoformat(timespec='seconds'))
            if is_gov(host) and not any(n in host for n in NEVER) and st == 200 and 'html' in ct:
                e = save_page(u, raw, final)
                if e: pm['pages'][u] = e; log.append(f'page saved {e["file"]} {e["words"]} words')
                else: log.append(f'page too short to save {u}')
            pm['errors'].pop(u, None)
        except Exception as ex:
            pm['errors'][u] = f'{type(ex).__name__}: {ex}'[:200]; log.append(f'error {u}: {ex}')
    pm['captured'] = NOW.isoformat(timespec='seconds')
    json.dump(pm, open(PM, 'w'), indent=1, sort_keys=True)
    print('\n'.join(log))
    print(f"pages saved {len(pm['pages'])}, frame-checked {len(pm['frame'])}, errors {len(pm['errors'])}, large PDFs left {len(man['not_copied'])}")


if __name__ == '__main__':
    main()
