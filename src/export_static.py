"""static.html: the built page with no JavaScript (everything expanded, all details open), for reading offline or printing.
rindge_2026_briefing.pdf is printed from it by headless Chrome (see bottom)."""
import re, os, subprocess
from bs4 import BeautifulSoup
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s = BeautifulSoup(open(os.path.join(ROOT, 'index.html')).read(), 'lxml')
for sc in s.find_all('script'):
    if sc.get('type') == 'application/json' or sc.get('id') in ('docdata', 'searchdata'): sc.decompose(); continue
    sc.decompose()
for d in s.find_all('details'): d['open'] = ''
for el in s.select('.js-only, #viewer, #searchDlg, #menu, #toast, #toTop, #progress'): el.decompose()
note = s.new_tag('p'); note['class'] = 'callout'
note.string = 'Static copy of the Rindge Town Guide (unofficial; not affiliated with the Town of Rindge), generated Oct 10, 2026 from the same build as the interactive site. Search, filters and the in-site document and video viewer are not available in this copy; links open the original sources.'
main = s.find('main'); main.insert(0, note)
open(os.path.join(ROOT, 'static.html'), 'w').write(str(s))
print('static.html', os.path.getsize(os.path.join(ROOT, 'static.html')))
pdf = os.path.join(ROOT, 'rindge_2026_briefing.pdf')
subprocess.run(['google-chrome', '--headless=new', '--no-sandbox', '--disable-gpu', '--no-pdf-header-footer', f'--print-to-pdf={pdf}', '--virtual-time-budget=8000',
                'file://' + os.path.join(ROOT, 'static.html')], check=True, capture_output=True, timeout=180)
print('pdf', os.path.getsize(pdf))
