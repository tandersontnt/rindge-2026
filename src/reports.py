"""Town reports page: every annual town report found, built from docs/MANIFEST.json (no hand-typed URLs for local copies).
Modern reports (2011-2025) come from the town's Town Reports folder. Older reports are held by outside archives;
only their verified collection pages are linked here, never guessed per-year URLs."""
import json, os, re, html as H

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOWN_FOLDER = 'Town%20Reports/'

# Outside archives with older reports (collection pages confirmed by web search, Oct 11, 2026)
ARCHIVES = [
    ('University of New Hampshire Scholars’ Repository', 'https://scholars.unh.edu/rindge_nh_reports/',
     'About 187 scanned Rindge annual reports, from 1849 to 2024, as PDFs. The largest collection of older reports.'),
    ('HathiTrust Digital Library', 'https://catalog.hathitrust.org/Record/008607781',
     'Catalog record for the bound series "Annual reports of the officers of the town of Rindge, N.H."'),
    ('Internet Archive', 'https://archive.org/search?query=rindge+annual+report',
     'Scans from the UNH Library collection. Search results; years vary.'),
]


def year_of(url):
    from urllib.parse import unquote
    name = unquote(url.rsplit('/', 1)[-1]).replace('102496_', '')
    m = re.search(r'(?<!\d)(20\d\d)(?!\d)', name)
    return int(m.group(1)) if m else None


def render(ic):
    m = json.load(open(os.path.join(ROOT, 'docs', 'MANIFEST.json')))
    rows = []
    for d in m['documents']:
        if TOWN_FOLDER in d['source_url']:
            rows.append((year_of(d['source_url']), d['source_url'], d['bytes'], True))
    for d in m['not_copied']:
        if TOWN_FOLDER in d['source_url']:
            rows.append((year_of(d['source_url']), d['source_url'], d['bytes'], False))
    rows = sorted((r for r in rows if r[0]), key=lambda r: -r[0])
    years = [r[0] for r in rows]
    assert len(years) == len(set(years)), 'duplicate report year'
    first, last = min(years), max(years)
    missing = [y for y in range(first, last + 1) if y not in years]
    tiles = []
    for y, url, size, local in rows:
        mb = size / 1048576
        meta = f'{mb:.0f} MB PDF' if local else f'{mb:.0f} MB \u00b7 town site'
        tiles.append(
            f'<li class="rpt"><span class="rpt-y" aria-hidden="true">{y}</span>'
            f'<a class="rpt-a" href="{H.escape(url)}" target="_blank" rel="noopener"><span class="sr">{y} </span>Annual Town Report</a>'
            f'<span class="rpt-m">{ic("doc" if local else "external")}<span>{meta}</span></span></li>')
    arch = ''.join(
        f'<li class="arch"><a class="arch-a" href="{H.escape(u)}" target="_blank" rel="noopener">{H.escape(n)}</a>'
        f'<span class="arch-d">{H.escape(d)}</span></li>' for n, u, d in ARCHIVES)
    bl = sorted(r[0] for r in rows if not r[3]); big = ', '.join(map(str, bl[:-1])) + ' and ' + str(bl[-1]) if len(bl) > 1 else ''.join(map(str, bl))
    gap = (f'<p class="note">Missing years in this range: {", ".join(map(str, missing))}.</p>' if missing else
           f'<p class="note">Every year from {first} to {last} is here. Reports are copied from the town’s Town Reports page '
           f'(checked Oct 9, 2026); the town’s copy is authoritative.' + (f' The {big} reports are over 25 MB, so they open on the town’s site instead.' if bl else ' Every report opens right here.') + '</p>')
    return (f'<ul class="rpts">{"".join(tiles)}</ul>{gap}'
            f'<h3 class="mt3">Older reports, 1849 to 2010</h3>'
            f'<p>The town’s website posts reports from {first} on. Older reports have been scanned by libraries. '
            f'Select a collection to browse it here.</p>'
            f'<ul class="archs">{arch}</ul>'
            f'<p class="note">The UNH collection says its scans may be used for research, teaching and private study; for other uses, ask the Town of Rindge. '
            f'This guide could not open the collections directly to list each year, so it links to them as a whole.</p>'), len(rows), first, last
