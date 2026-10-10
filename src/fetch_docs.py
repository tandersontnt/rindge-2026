# Download cited, publicly posted town documents (rindgenh.org/.gov) that are not yet in docs/. Never edits files.
# Usage: python3 src/fetch_docs.py   (then rebuild with python3 src/build.py)
import json, os, re, subprocess, hashlib, urllib.parse, datetime, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, 'docs'); M = os.path.join(D, 'MANIFEST.json')
SKIP_OVER = 25_000_000  # skip single files over 25 MB (link out instead)
man = json.load(open(M)); have = {d['source_url'] for d in man['documents']} | {d['source_url'] for d in man.get('not_copied', [])}
page = open(os.path.join(ROOT, 'index.html')).read()
urls = sorted(set(u.replace('&amp;', '&') for u in re.findall(r'href="(https?://(?:www\.)?rindgenh\.(?:org|gov)/[^"]+)"', page)))
added = []
for u in urls:
    if u in have or not re.search(r'\.(pdf|docx?)(\?|$)', u, re.I): continue
    hd = subprocess.run(['curl', '-s', '-I', '-L', '--max-time', '30', '-A', 'Mozilla/5.0', u], capture_output=True, text=True).stdout.replace('\r', '')
    st = re.findall(r'^HTTP/\S+ (\d+)', hd, re.M); ln = re.findall(r'(?im)^content-length:\s*(\d+)', hd); ct = re.findall(r'(?im)^content-type:\s*(\S+)', hd)
    if not st or st[-1] != '200': print('skip (status', st[-1:] , ')', u); continue
    if ln and int(ln[-1]) > SKIP_OVER: print('skip (too large)', u); continue
    p = urllib.parse.urlparse(u); b = urllib.parse.unquote(p.path.rsplit('/', 1)[-1]); b = re.sub(r'[^A-Za-z0-9._-]+', '_', b).strip('_')
    stem, ext = os.path.splitext(b); fn = f"{stem[:70]}_{hashlib.sha1(u.encode()).hexdigest()[:6]}{ext.lower()}"
    subprocess.run(['curl', '-s', '-L', '--max-time', '300', '-A', 'Mozilla/5.0', '-o', os.path.join(D, fn), u], check=True)
    data = open(os.path.join(D, fn), 'rb').read()
    if ext.lower() == '.pdf' and not data.startswith(b'%PDF'): os.remove(os.path.join(D, fn)); print('skip (not a PDF)', u); continue
    d = dict(file=fn, source_url=u, sha256=hashlib.sha256(data).hexdigest(), bytes=len(data), content_type=(ct[-1] if ct else '').split(';')[0],
             retrieved=datetime.datetime.now().astimezone().isoformat(timespec='seconds'))
    if ext.lower() in ('.doc', '.docx'):
        os.makedirs(os.path.join(D, 'converted'), exist_ok=True)
        subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', '--outdir', os.path.join(D, 'converted'), os.path.join(D, fn)], capture_output=True, timeout=180)
        c = 'converted/' + stem[:70] + '_' + hashlib.sha1(u.encode()).hexdigest()[:6] + '.pdf'
        if os.path.exists(os.path.join(D, c)):
            d.update(converted=c, converted_sha256=hashlib.sha256(open(os.path.join(D, c), 'rb').read()).hexdigest(),
                     converted_note='PDF rendering made with LibreOffice for in-site viewing only; the original Word file is the copy of record.')
    man['documents'].append(d); added.append(fn); print('added', fn, len(data))
man['documents'].sort(key=lambda d: d['file'].lower()); man['count'] = len(man['documents']); man['total_bytes'] = sum(d['bytes'] for d in man['documents'])
json.dump(man, open(M, 'w'), indent=1)
print('added', len(added), 'total', man['count'], round(man['total_bytes'] / 1e6, 1), 'MB')
