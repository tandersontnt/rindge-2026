"""Structured data for the guide.

1. HOURS: the posted office hours from r3data.DEPTS, re-typed as machine-readable rules (no new facts).
   Each office: list of (days, opens, closes, months). days use 0=Sun..6=Sat; months None = all year.
   'unknown' lists days whose hours the town does not post (shown as "not posted", never guessed).
   'appointment' lists days that are by appointment only.
   Days not covered by a rule or 'unknown' are closed, matching how the town lists them.
2. inject(page): adds the hours JSON for app.js and schema.org JSON-LD for search engines and assistants.
"""
import json, re, html as H
from bs4 import BeautifulSoup
from r3data import DEPTS

BASE = 'https://tandersontnt.github.io/rindge-2026/'
TOWN = {'@type': 'GovernmentOrganization', 'name': 'Town of Rindge, New Hampshire', 'url': 'https://www.rindgenh.org/'}
MON, TUE, WED, THU, FRI, SAT, SUN = 1, 2, 3, 4, 5, 6, 0
NOV_APR, MAY_OCT = [11, 12, 1, 2, 3, 4], [5, 6, 7, 8, 9, 10]

HOURS = {
 "Town Clerk's office": dict(rules=[([MON, WED], '08:00', '13:00', None), ([MON, WED], '13:30', '16:00', None), ([TUE], '12:00', '18:30', None),
                                   ([THU], '07:00', '13:00', None), ([THU], '13:30', '15:30', None)], unknown=[FRI]),
 "Tax Collector": dict(rules=[([MON, TUE, WED, THU], '09:00', '13:00', None), ([MON, TUE, WED, THU], '14:00', '16:00', None)]),
 "Assessing": dict(rules=[([WED, THU], '12:30', '16:30', None)]),
 "Building Department": dict(rules=[([MON, TUE, WED, THU], '13:00', '15:00', None)], label='Office'),
 "Planning Department": dict(rules=[([MON, TUE, WED], '09:00', '16:00', None)], appointment=[THU]),
 "Select Board office / Town Administrator": dict(rules=[([MON, TUE, WED, THU], '09:00', '16:00', None)]),
 "Public Works (Highway)": dict(rules=[([MON, TUE, WED, THU], '07:00', '15:30', NOV_APR), ([MON, TUE, WED, THU], '06:00', '16:30', MAY_OCT),
                                      ([FRI], '07:00', '15:30', NOV_APR)], unknown_months={FRI: MAY_OCT}),
 "Recycling and Transfer Station": dict(rules=[([TUE, THU], '10:00', '19:00', None), ([FRI], '13:00', '19:00', None), ([SAT], '08:00', '15:00', None)]),
 "Police Department": dict(rules=[([MON, TUE, WED, THU, FRI], '08:00', '16:00', None)], label='Office'),
 "Ingalls Memorial Library": dict(rules=[([MON, WED, FRI], '10:00', '17:00', None), ([TUE, THU], '13:00', '20:00', None), ([SAT], '09:00', '12:00', None)]),
}
assert set(HOURS) <= {d[0] for d in DEPTS}, set(HOURS) - {d[0] for d in DEPTS}

DAYNAME = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
STREET = {'Town Offices': '30 Payson Hill Road'}


def tel(s):
    m = re.search(r'\((\d{3})\)\s*(\d{3})-(\d{4})(?:\s*x(\d+))?', s)
    if not m: return None
    return f'+1-{m[1]}-{m[2]}-{m[3]}' + (f' ext. {m[4]}' if m[4] else '')


def address(a):
    street = a.split('(')[0].strip()
    street = STREET.get(street, street)
    if not re.match(r'\d', street): return None
    return {'@type': 'PostalAddress', 'streetAddress': street, 'addressLocality': 'Rindge', 'addressRegion': 'NH', 'postalCode': '03461', 'addressCountry': 'US'}


def opening_spec(h):
    out = []
    for days, o, c, months in h['rules']:
        if months: continue  # seasonal hours stay on the page; schema.org seasonal ranges need exact dates the town does not post
        out.append({'@type': 'OpeningHoursSpecification', 'dayOfWeek': [DAYNAME[d] for d in days], 'opens': o, 'closes': c})
    return out


def offices():
    items = []
    for name, what, phone, email, hours, addr, url, labels, note in DEPTS:
        o = {'@type': 'Library' if 'Library' in name else 'GovernmentOffice', 'name': name if 'Library' in name else f'Rindge {name}',
             'description': what, 'url': url, 'parentOrganization': TOWN}
        t = tel(phone)
        if t: o['telephone'] = t
        if email: o['email'] = email.split('·')[0].strip()
        a = address(addr)
        if a: o['address'] = a
        if name in HOURS:
            spec = opening_spec(HOURS[name])
            if spec: o['openingHoursSpecification'] = spec
        items.append(o)
    return items


def faq(soup):
    """How-to guides as questions; the answer is each guide's own one-line summary (the same text search shows)."""
    idx = json.loads(soup.select_one('#searchdata').string)
    summ = {x['h']: x['s'] for x in idx if x.get('k') == 'How do I'}
    qs = []
    for d in soup.select('details.how'):
        q = d.select_one('summary h3, summary .sum-h, summary')
        a = summ.get('#' + d.get('id', ''))
        if not q or not a: continue
        qt = re.sub(r'\s+', ' ', q.get_text(' ', strip=True))
        qs.append({'@type': 'Question', 'name': qt, 'acceptedAnswer': {'@type': 'Answer', 'text': a, 'url': BASE + '#' + d['id']}})
    return {'@type': 'FAQPage', 'name': 'How do I...? Rindge town services', 'url': BASE + '#howto', 'mainEntity': qs}


def inject(page):
    soup = BeautifulSoup(page, 'html.parser')
    desc = (soup.select_one('meta[name=description]') or {}).get('content', '')
    graph = [
        {'@type': 'WebSite', '@id': BASE + '#site', 'name': 'Rindge Town Guide', 'url': BASE, 'inLanguage': 'en-US', 'description': desc,
         'about': {'@type': 'AdministrativeArea', 'name': 'Rindge, New Hampshire', 'containedInPlace': {'@type': 'State', 'name': 'New Hampshire'}},
         'disclaimer': 'Unofficial community research. Not affiliated with or endorsed by the Town of Rindge. The town\'s own records are authoritative.',
         'potentialAction': {'@type': 'SearchAction', 'target': {'@type': 'EntryPoint', 'urlTemplate': BASE + '?q={search_term_string}'},
                             'query-input': 'required name=search_term_string'}},
        {'@type': 'Dataset', 'name': 'Rindge, NH board meetings, 2026', 'url': BASE + '#timeline',
         'description': 'Board meetings found on the Town of Rindge board pages in 2026, with links to each agenda, minutes and video. Compiled for the unofficial Rindge Town Guide.',
         'temporalCoverage': '2026-01-01/2026-10-09', 'spatialCoverage': 'Rindge, New Hampshire', 'isBasedOn': 'https://www.rindgenh.org/',
         'isAccessibleForFree': True,
         'creator': {'@id': BASE + '#site'},
         'distribution': [{'@type': 'DataDownload', 'encodingFormat': 'application/json', 'contentUrl': BASE + 'meetings.json'}]},
        faq(soup),
    ] + offices()
    ld = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    hours = json.dumps(HOURS, separators=(',', ':'))
    tags = (f'<script type="application/ld+json">{ld}</script>\n'
            f'<script type="application/json" id="hoursdata">{hours}</script>\n')
    assert page.count('</head>') == 1
    return page.replace('</head>', tags + '</head>')
