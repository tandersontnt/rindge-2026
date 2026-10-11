import datetime
# v3: document registry. Classifies every cited URL, titles it, and records local copies.
import json, re, os, urllib.parse, datetime, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DOCS = os.path.join(ROOT, 'docs')
MANIFEST = os.path.join(DOCS, 'MANIFEST.json')
COPY_DATE = "Oct 9, 2026"
MON = ['January','February','March','April','May','June','July','August','September','October','November','December']
MABBR = {m[:3].lower(): i+1 for i, m in enumerate(MON)}
WD = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']

# Hosts whose pages loaded inside a frame in the Oct 9 header + headless Chrome test.
EMBED_HOSTS = {'ledgertranscript.com', 'www.keenesentinel.com', 'www.nhmunicipal.org'}
HOSTNAME = {
 'www.gencourt.state.nh.us': ('NH General Court (RSA text)', 'State law'), 'gc.nh.gov': ('NH General Court (RSA text)', 'State law'),
 'townhallstreams.com': ('Town Hall Streams', 'Video'), 'ledgertranscript.com': ('Monadnock Ledger-Transcript', 'Press article'),
 'www.keenesentinel.com': ('Keene Sentinel', 'Press article'), 'www.nhmunicipal.org': ('NH Municipal Association', 'Association guide'),
 'citizenportal.ai': ('Citizen Portal (automated summary)', 'Automated summary'), 'co.cheshire.nh.us': ('Cheshire County', 'Web page'),
 'mytownview.com': ('MyTownView (automated)', 'Automated summary'), 'www.census.gov': ('US Census Bureau', 'Data'),
 'www.nhdeeds.org': ('Cheshire County Registry of Deeds', 'Web page'), 'www.revenue.nh.gov': ('NH Dept. of Revenue Administration', 'Data'),
 'www.rindgenh.org': ('Town of Rindge', 'Town web page'), 'www.rindgenh.gov': ('Town of Rindge', 'Town web page'), 'rindgenh.gov': ('Town of Rindge', 'Town web page'),
}

def fmt_date(y, m, d):
    try:
        dt = datetime.date(y, m, d)
    except ValueError:
        return None
    return dt, f"{WD[dt.weekday()]}, {MON[m-1][:3]} {d}, {y}"

def parse_date(name, path):
    n = name
    for rx, order in [(r'(20\d\d)-(\d\d)-(\d\d)', 'ymd'), (r'(?<!\d)(\d{1,2})\.(\d{1,2})\.(20\d\d|\d\d)(?!\d)', 'mdy'),
                      (r'RCC[ _](?:Agenda|Minutes)[ _](\d\d)(\d\d)(\d\d)', 'mdy'), (r'(\d{1,2})_(\d{1,2})_(20\d\d)', 'mdy')]:
        m = re.search(rx, n)
        if m:
            a, b, c = m.groups()
            if order == 'ymd': y, mo, d = int(a), int(b), int(c)
            else:
                mo, d, y = int(a), int(b), int(c)
                if y < 100: y += 2000
            r = fmt_date(y, mo, d)
            if r: return r
    m = re.search(r'(January|February|March|April|May|June|July|August|September|October|November|December)(?:[ _]?(\d{1,2})(?!\d))?,?[ _]?(20\d\d)?', n, re.I)
    if m:
        mo = MON.index(m.group(1).capitalize()) + 1
        yy = re.search(r'/(20\d\d)/', path)
        y = int(m.group(3) or (yy.group(1) if yy else 2026))
        if m.group(2):
            r = fmt_date(y, mo, int(m.group(2)))
            if r: return r
        return datetime.date(y, mo, 1), f"{MON[mo-1]} {y}"
    m = re.search(r'(?<![\d])(\d{1,2})[ _](JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)', n, re.I)
    if m:
        yy = re.search(r'/(20\d\d)/', path)
        return fmt_date(int(yy.group(1)) if yy else 2026, MABBR[m.group(2)[:3].lower()], int(m.group(1)))
    return None

BOARDS = [('Board%20of%20Selectmen', 'Select Board'), ('Planning%20Board', 'Planning Board'), ('Zoning%20Board%20of%20Adjustment', 'Zoning Board of Adjustment'),
          ('Conservation%20Commission', 'Conservation Commission'), ('Budget%20Advisory', 'Budget Advisory Committee'), ('Town%20Reports', 'Town of Rindge')]

ORD_TITLES = {
 'Zoning_Ordinance_Amended_March_11_2025': 'Zoning Ordinance (amended March 11, 2025)',
 'aquifer_ordinance_amended_march_11_2014': 'Aquifer Protection Ordinance (amended March 11, 2014)',
 'blasting_and_heavy_construction_site_plan_regulations': 'Blasting and Heavy Construction Site Plan Regulations',
 'driveway_regulations_amended_december_5_2017': 'Driveway Regulations (amended Dec 5, 2017)',
 'excavate2006': 'Excavation Regulations (2006)',
 'floodplain_management_ordinance_-_changes_adopted_2006': 'Floodplain Management Ordinance (2006 changes)',
 'gravelroadpolicy.22': 'Gravel Road Policy',
 'planned_unit_residential_development_regulations_march_2_2021': 'Planned Unit Residential Development Regulations (March 2, 2021)',
 'rindge_class_vi_road_waiver_20200329': 'Class VI Road Waiver form (2020)',
 'sexually_oriented_bus_2006': 'Sexually Oriented Business Ordinance (2006)',
 'sign_ordinance_amended_march_12_2024': 'Sign Ordinance (amended March 12, 2024)',
 'site_plan_regulations_amended_april_152025': 'Site Plan Regulations (amended April 15, 2025)',
 'small_wind_energy_final_approved_by_voters_march_12_2013': 'Small Wind Energy Ordinance (March 12, 2013)',
 'subdivision_regulations_adopted_09_20_11': 'Subdivision Regulations (adopted Sept 20, 2011)',
 'telecommunication_ordinance_2011': 'Wireless Telecommunication Ordinance (2011)',
 'underground_storage_tank_2006': 'Underground Storage Tank Ordinance (2006)',
 'wetlands_conservation_district_ordinance_amended_march_28_2023': 'Wetlands Conservation District Ordinance (amended March 28, 2023)',
 'Accessory_Dwelling_Unit_Ordinance_2026': 'Accessory Dwelling Unit Ordinance (2026)',
 '2018-08-07_master_plan_pdf_to_print': 'Master Plan (Aug 7, 2018)',
 '2025_ZoningMap_36x24': 'Zoning Map (2025)',
 'ZBA_ROP_APPROVED_09-28-2021': 'ZBA Rules of Procedure (approved Sept 28, 2021)',
}

def classify_type(name):
    n = name.lower()
    if 'nonpublic' in n: return 'Notice'
    if 'agenda' in n: return 'Agenda'
    if 'minutes' in n: return 'Draft minutes' if 'draft' in n else 'Minutes'
    if 'notice' in n: return 'Public notice'
    if 'annual' in n: return 'Annual report'
    if 'map' in n: return 'Map'
    if 'master_plan' in n: return 'Plan'
    if 'rop' in n: return 'Rules of procedure'
    return 'Ordinance or regulation'

def town_meta(url, fname):
    p = urllib.parse.urlparse(url)
    base = urllib.parse.unquote(p.path.rsplit('/', 1)[-1])
    stem = re.sub(r'_[0-9a-f]{6}$', '', os.path.splitext(fname)[0])
    board = next((b for k, b in BOARDS if k in p.path), None)
    if not board:
        board = 'Planning Board' if re.search(r'(PB|Approved(%20)+Minutes)', p.path) else 'Town of Rindge'
    typ = 'Annual report' if 'Town%20Reports' in p.path else classify_type(stem)
    if 'Regulations' in p.path or 'Zoning%20Ordinances' in p.path or stem in ORD_TITLES:
        if stem in ORD_TITLES and typ not in ('Agenda', 'Minutes', 'Draft minutes'):
            typ = classify_type(stem) if stem in ('2025_ZoningMap_36x24', '2018-08-07_master_plan_pdf_to_print', 'ZBA_ROP_APPROVED_09-28-2021') else 'Ordinance or regulation'
            return dict(title=ORD_TITLES[stem], board='Planning Board' if board != 'Zoning Board of Adjustment' else board, type=typ, year=_year(stem, p.path), date=None)
    if typ == 'Annual report':
        y = re.search(r'(20\d\d)', base)
        y = int(y.group(1)) if y else None
        return dict(title=f"{y} Annual Report of the Town of Rindge", board='Town of Rindge', type=typ, year=y, date=None)
    mm = re.search(r'meeting[ _](January|February|March|April|May|June|July|August|September|October|November|December)[ _](\d{1,2})(?:[ ,_]+(20\d\d))?', base, re.I)
    dd = fmt_date(int(mm.group(3) or 2026), MON.index(mm.group(1).capitalize()) + 1, int(mm.group(2))) if mm else parse_date(base, p.path)
    if mm and typ == 'Public notice': typ = 'Public notice'
    extra = ''
    if 'subcommittee' in base.lower(): extra = ' (Alternative Lot / Back Lot subcommittee)'; board = 'Planning Board'
    if 'special' in base.lower(): extra = ' (special meeting)'
    if 'nonpublic' in base.lower(): extra = ' (non-public session notice)'
    if re.search(r'UPDATE|rev1', base): extra += ' (updated)'
    tl = {'Agenda': 'agenda', 'Minutes': 'minutes', 'Draft minutes': 'draft minutes', 'Public notice': 'public hearing notice' + (' for the meeting of' if mm else ''), 'Notice': 'notice'}.get(typ, typ.lower())
    if dd:
        date, label = dd
        return dict(title=f"{board} {tl}{extra}: {label}", board=board, type=typ, year=date.year, date=date.isoformat())
    return dict(title=f"{board} {tl}{extra}", board=board, type=typ, year=_year(base, p.path), date=None)

def _year(s, path):
    m = re.search(r'(20\d\d)', s) or re.search(r'/(20\d\d)/', path)
    return int(m.group(1)) if m else None

def load():
    return json.load(open(MANIFEST))['documents'] if os.path.exists(MANIFEST) else []
def not_copied():
    return {d['source_url'] for d in json.load(open(MANIFEST)).get('not_copied', [])} if os.path.exists(MANIFEST) else set()

VIDEOS = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'videodata.json'))) if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'videodata.json')) else {}

PAGES_M = os.path.join(DOCS, 'pages', 'MANIFEST.json')
def pages_manifest():
    return json.load(open(PAGES_M)) if os.path.exists(PAGES_M) else {'pages': {}, 'frame': {}}

def registry(urls, link_text):
    """Return {url: entry}. Every entry has id, kind (pdf|word|missing|embed|ext), title, board, type, year, src."""
    man = {d['source_url']: d for d in load()}
    big = not_copied()
    reg = {}
    for i, u in enumerate(sorted(urls)):
        host = urllib.parse.urlparse(u).netloc
        e = dict(id=f"d{i}", src=u, host=host)
        if u in man:
            d = man[u]
            e.update(town_meta(u, d['file']))
            e['file'] = 'docs/' + d['file']
            e['bytes'] = d['bytes']
            if d.get('converted'):
                e['kind'] = 'word'; e['view'] = 'docs/' + d['converted']
            else:
                e['kind'] = 'pdf'; e['view'] = e['file']
        else:
            org, typ = HOSTNAME.get(host, (host, 'Web page'))
            txt = link_text.get(u, '').strip()
            missing = u in MISSING
            if 'rindgenh' in host and ('.pdf' in u.lower()):
                e.update(town_meta(u, urllib.parse.unquote(urllib.parse.urlparse(u).path.rsplit('/', 1)[-1])))
                e['kind'] = 'large' if u in big else 'missing'
            else:
                title = txt if txt and txt.lower() not in ('source', 'link', 'video', 'agenda', 'minutes', 'here') else _page_title(u, org)
                if host.endswith('gencourt.state.nh.us'):
                    m = re.search(r'/(\d+[A-Z]?)-([\w-]+)\.htm', u)
                    if m: title = f"RSA {m.group(1)}:{m.group(2)}"
                if host == 'townhallstreams.com': title = txt if len(txt) > 8 else 'Meeting video (Town Hall Streams)'
                e.update(title=title, board=org, type=typ, year=_year(u, u), date=None)
                e['kind'] = 'missing' if missing else ('embed' if host in EMBED_HOSTS else 'ext')
                pmf = pages_manifest()
                snap = pmf['pages'].get(u); fr = pmf['frame'].get(u)
                gf = pmf.get('files', {}).get(u)
                if e['kind'] == 'ext' and gf:  # state agency PDF saved by the snapshot workflow
                    e.update(kind='pdf', file='docs/' + gf['file'], view='docs/' + gf['file'], bytes=gf['bytes'], captured=gf['captured'][:10])
                elif e['kind'] == 'ext' and snap:  # saved copy of a public government page, shown inside the site
                    e.update(kind='page', view='docs/' + snap['file'], captured=snap['captured'][:10])
                    if not txt or txt.lower() in ('source', 'link', 'here', 'town page', 'website', 'web page') or txt.lower().startswith('source for'): e['title'] = snap['title']
                elif e['kind'] == 'ext' and re.search(r'pay\.|eb2gov|citizen_request_center|enotify', u):
                    e['kind'] = 'service'  # payments and sign-up forms stay on the official secure site
                elif e['kind'] == 'ext' and host == 'townhallstreams.com':
                    e['kind'] = 'channel'  # every recorded Select Board meeting already plays in this site's player
                elif e['kind'] == 'ext' and fr and fr.get('frameable') and fr.get('status') == 200:
                    e['kind'] = 'embed'  # the site allows framing (checked by the snapshot workflow)
                v = VIDEOS.get(u)
                if v:  # Town Hall Streams blocks framing; its public HLS stream (CORS *) plays in our own player
                    dt = datetime.date.fromisoformat(v['date'])
                    e.update(kind='video', hls=v['hls'], dur=v.get('dur'), date=v['date'], year=dt.year, board='Select Board', type='Video',
                             title=f"Select Board meeting video: {dt.strftime('%a, %b')} {dt.day}, {dt.year}", chapters=v.get('chapters') or [])
            e['org'] = org
        reg[u] = e
    return reg

MISSING = {"https://www.rindgenh.org/Documents/Boards%20Commission/Board%20of%20Selectmen/Agendas%20Minutes/2026/03%20Minutes/03.25.2026_BOS_minutes.pdf?t=202607091428060",
           "https://rindgenh.gov/news_detail_T2_R16.php"}

def _page_title(u, org):
    p = urllib.parse.urlparse(u)
    seg = [s for s in p.path.split('/') if s and s not in ('index.php',)]
    if not seg: return org + ' home page'
    last = urllib.parse.unquote(seg[-1])
    last = re.sub(r'\.(php|html?|pdf|aspx)$', '', last)
    last = re.sub(r'article_[0-9a-f-]+', '', last)
    if len(seg) > 1 and len(last) < 4: last = urllib.parse.unquote(seg[-2])
    t = re.sub(r'[_-]+', ' ', last).strip()
    t = re.sub(r'\b\d{6,}\b', '', t).strip()
    return (t[:1].upper() + t[1:]) if t else org
