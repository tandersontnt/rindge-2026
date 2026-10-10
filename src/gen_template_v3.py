import ast,re
P=ast.literal_eval(open('/tmp/parts.py').read())
def ic(n,cls='i'): return f'<svg class="{cls}" aria-hidden="true" focusable="false"><use href="#i-{n}"/></svg>'
GROUPS=[('home','Home','home'),('meetings','Meetings','calendar'),('money','Votes &amp; money','coins'),('rules','Issues &amp; rules','scale'),('services','Town services','building'),('documents','Documents','doc')]
SECTIONS={ # id: (group, short title)
 'start':('home','Start here'),'timeline':('meetings','2026 meeting timeline'),'calendar':('meetings','Key dates'),
 'election':('money','March 2026 election'),'numbers':('money','By the numbers'),'budget':('money','Budget and finances'),'trends':('money','Trends since 2011'),
 'topics':('rules','Topics'),'recurring':('rules','Recurring issues'),'laws':('rules','Laws and regulations'),
 'directory':('services','Town directory'),'howto':('services','How do I...?'),'emergency':('services','Emergency and utilities'),'schools':('services','Schools and community'),'facts':('services','Town facts and history'),
 'library':('documents','Document library'),'gaps':('documents','Gaps and conflicts'),'sources':('documents','Sources')}
GN={g:t for g,t,_ in GROUPS}
PLAIN={
 'start':None,
 'timeline':"This list has 70 entries from January 1 to October 9, 2026: board meetings, the Deliberative Session, the election and two school board meetings. Pick a board or search for a road or topic. Every entry says where its information comes from.",
 'calendar':"The next town vote is Tuesday, March 9, 2027. The town has not posted its 2027 calendar yet, so most deadlines here are worked out from state law. Confirm any date with the Town Clerk's office before relying on it.",
 'election':"In March 2026 voters turned down the proposed $5.81 million town budget (707-824), so the $5,654,177 default budget applies. All seven savings-fund articles passed. These results come from newspapers; the town has not posted official results.",
 'numbers':"About 6,500 people live in Rindge. After the 2025 revaluation the tax rate fell to $13.79 per $1,000, because assessed values roughly doubled. That does not mean tax bills were cut in half.",
 'budget':"The town spends about $5.5 to $5.8 million a year on its own operations, before school and county taxes. Voters rejected the proposed budget in 2025 and 2026, so the default budget applies. The largest lines are police, highway and fire.",
 'trends':"Since 2011 voters have approved the town budget in most years but rejected it in 2011, 2021, 2025 and 2026. Zoning changes usually pass. Numbers read from scanned reports are marked so you can check them against the original.",
 'topics':"Short briefings on the subjects that came up most in 2026, such as the budget, ambulance service, zoning, wetlands and elderly exemptions. Select a topic to open it.",
 'recurring':"Some issues come back again and again: lot frontage, back lots, wetlands setbacks, ambulance service, the budget and school costs. Each card shows when an issue first appears in the records and what has happened since.",
 'laws':"Rindge's zoning ordinance sets lot sizes, setbacks and frontage (250 feet on a public road in the residential and village districts). State law sets how rules change: zoning changes and citizen petitions go to voters on the March ballot. This is a summary, not legal advice.",
 'directory':"For most questions, call the Town Offices at (603) 899-5181. In an emergency, dial 911. Each office below lists its phone number, hours and town web page.",
 'howto':"Step-by-step help with common tasks: permits, dog licenses, registering a vehicle, voting, and appealing or lowering a property tax bill. Each guide says who to contact and what to check first.",
 'emergency':"In an emergency, call 911. Ambulance service is due to switch to Peterborough Fire &amp; Rescue on January 1, 2027 (press-reported). No town water or sewer system is listed, so homes generally use private wells and septic (unconfirmed).",
 'schools':"Rindge children attend the Jaffrey-Rindge Cooperative School District (SAU 47): Rindge Memorial School for PreK–5, then Conant Middle and High School in Jaffrey. School budgets are voted separately from the town budget.",
 'facts':"Rindge was incorporated in 1768. It covers about 40 square miles on the Massachusetts border, has many lakes and ponds, and had 6,476 residents in the 2020 Census.",
 'library':"{{NDOCS}} town documents cited in this guide are copied here so they open right inside the site. Search or filter by board, type or year. The originals on rindgenh.org are authoritative.",
 'gaps':"No source is perfect. This part lists where sources disagree and what could not be found, so you know what to double-check.",
 'sources':"Every source used in this guide, grouped by type.",
}
def crumbs(sid):
    g,t=SECTIONS[sid]
    mid='' if g=='home' else '<li><a href="#%s">%s</a></li>'%(g,GN[g])
    return '<nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="#home">Home</a></li>'+mid+'<li><span aria-current="location">'+t+'</span></li></ol></nav>'
def enhance(html,sid):
    m=re.search(r'(<h2 id="[^"]+">.*?</h2>)',html,re.S)
    h2=m.group(1)
    tools=f'<div class="sechead">{h2}<button type="button" class="sharebtn js-only" data-share="{sid}">{ic("link")}<span>Share</span><span class="sr"> a link to this section</span></button></div>'
    pl=PLAIN.get(sid)
    plain=(f'<div class="plain" role="note"><p class="plain-k">{ic("info")}<span>In plain language</span></p><p>{pl}</p></div>' if pl else '')
    return html.replace(h2,crumbs(sid)+tools+plain,1)
def newsec(sid,title,intro,ph):
    return f''' <section class="sec" id="{sid}" aria-labelledby="{sid}-h">
  <h2 id="{sid}-h">{title}</h2>
  {f'<p class="intro">{intro}</p>' if intro else ''}
  {{{{{ph}}}}}
 </section>
'''
def groupbanner(g,title,icon,desc,items):
    lis=''.join(f'<li><a href="#{s}">{SECTIONS[s][1]}</a></li>' for s in items)
    return f'''<div class="groupban" id="{g}" tabindex="-1"><div class="gb-ic">{ic(icon)}</div><div><p class="gb-k">{title}</p><p class="gb-d">{desc}</p><ul class="gb-l">{lis}</ul></div></div>
'''
S=P
budget=newsec('budget','Budget and finances','Department budgets, savings funds, debt and the capital plan, from the town\'s 2024 and 2025 annual reports. 2026 vote results are press-reported.','BUDGET')
directory=newsec('directory','Town directory: who to call','Town offices, departments, boards and committees, with phone numbers, hours and town web pages. Offices are listed by title. Checked Oct 9, 2026.','DIRECTORY')
howto=newsec('howto','How do I...?','','HOWTO')
emerg=newsec('emergency','Emergency and utilities','','EMERG')
schools=newsec('schools','Schools and community','','SCHOOLS')
facts=newsec('facts','Town facts and history','','FACTS')
library=newsec('library','Document library','Every document cited in this guide. Town documents are byte-for-byte copies of what rindgenh.org served on Oct 9, 2026, with a checksum for each in docs/MANIFEST.json. Other sources open in the viewer only if the source allows it; otherwise they open in a new tab.','LIBRARY')
order=[('home',None),('start',S['start']),
 ('G:meetings',groupbanner('meetings','Meetings','calendar','What the town\'s boards did in 2026, and the dates coming up.',['timeline','calendar'])),('timeline',S['tl']),('calendar',S['cal']),
 ('G:money',groupbanner('money','Votes &amp; money','coins','How residents voted, what the town spends, and how taxes have changed since 2011.',['election','numbers','budget','trends'])),('election',S['el']),('numbers',S['num']),('budget',budget),('trends',S['tr']),
 ('G:rules',groupbanner('rules','Issues &amp; rules','scale','The topics that keep coming up, and the local, county and state rules behind them.',['topics','recurring','laws'])),('topics',S['top']),('recurring',S['rc']),('laws',S['lw']),
 ('G:services',groupbanner('services','Town services','building','Who to call, how to get things done, emergencies, schools and community.',['directory','howto','emergency','schools','facts'])),('directory',directory),('howto',howto),('emergency',emerg),('schools',schools),('facts',facts),
 ('G:documents',groupbanner('documents','Documents','doc','Open any cited document inside this site, and see what is missing or disputed.',['library','gaps','sources'])),('library',library),('gaps',S['gp']),('sources',S['sr'])]
body=''
for sid,html in order:
    if sid=='home' or html is None: continue
    if sid.startswith('G:'): body+=html; continue
    body+=enhance(html,sid)
TASKS=[('calendar','When is the next meeting?','Board meetings this fall and the March 2027 ballot calendar.','#calendar'),
 ('vote','What is on the March ballot?','The 2027 warrant is not posted yet. See the deadlines, recurring items and the 2026 results.','#calendar'),
 ('petition','How do I file a petition?','Signatures, deadlines and the steps, in plain language.','#how-file-a-citizen-petition-for-the-march-b'),
 ('frontage','What are the zoning rules for my lot?','Frontage, lot size, setbacks and wetlands, by district.','#laws'),
 ('chart','What happened this year?','Every 2026 meeting, vote and decision, with sources.','#timeline'),
 ('doc','Find a document','Agendas, minutes, ordinances and annual reports, opened right here.','#library')]
MORE=[('phone','Who do I call?','#directory'),('building','How do I get a permit?','#how-get-a-building-permit'),('coins','How does the town spend money?','#budget'),
 ('alert','What do I do in an emergency?','#emergency'),('school','Which schools serve Rindge?','#schools'),('landmark','Town facts and history','#facts')]
tasks=''.join(f'<li><a class="task" href="{h}"><span class="task-ic">{ic(i)}</span><span class="task-t">{t}</span><span class="task-d">{d}</span><span class="task-go">{ic("next")}</span></a></li>' for i,t,d,h in TASKS)
more=''.join(f'<li><a class="mini" href="{h}">{ic(i)}<span>{t}</span></a></li>' for i,t,h in MORE)
rail=''
for g,t,icn in GROUPS:
    items=[s for s,(gg,_) in SECTIONS.items() if gg==g]
    rail+=f'<li><a class="rg" href="#{g}">{ic(icn)}<span>{t}</span></a><ul>'+''.join(f'<li><a href="#{s}">{SECTIONS[s][1]}</a></li>' for s in items)+'</ul></li>'
nav=''.join(f'<li><a href="#{g}" data-group="{g}">{t}</a></li>' for g,t,_ in GROUPS)
bnav=''.join(f'<li><a href="#{g}" data-group="{g}">{ic(i)}<span>{ {"money":"Votes","rules":"Rules","services":"Services","documents":"Docs"}.get(g,t) }</span></a></li>' for g,t,i in GROUPS)
disc=S['disc'].replace('<div class="ic" aria-hidden="true">⚖️</div>','<div class="ic">'+ic('scale')+'</div>')
head=S['head'].replace("<title>Rindge, NH Town Guide: 2026, trends since 2011, and the rules that apply (unofficial)</title>","<title>Rindge Town Guide (unofficial): meetings, votes, budget, rules, services and documents</title>")
head=head.replace("""try{var t=localStorage.getItem('rindgeTheme');if(!t&&window.matchMedia&&matchMedia('(prefers-color-scheme: dark)').matches)t='dark';if(t)d.setAttribute('data-theme',t);}catch(e){}""",
"""try{var t=localStorage.getItem('rindgeTheme')||'auto';if(t==='auto')t=(window.matchMedia&&matchMedia('(prefers-color-scheme: dark)').matches)?'dark':'light';d.setAttribute('data-theme',t);var z=localStorage.getItem('rindgeSize');if(z)d.setAttribute('data-size',z);}catch(e){}""")
tpl=head+'''<style>
{{CSS}}
</style>
</head>
<body>
{{SPRITE}}
<a class="skip" href="#main">Skip to main content</a>
<div id="progress" aria-hidden="true"></div>
<div class="notice" role="note" id="top"><div class="wrap">
 <span><strong>Unofficial community research.</strong> Not affiliated with or endorsed by the Town of Rindge.</span>
 <span>Last updated <time datetime="2026-10-09">Oct 9, 2026</time></span>
</div></div>
<header class="topbar">
 <div class="wrap bar">
  <a class="brand" href="#home"><span class="logo" aria-hidden="true"><svg viewBox="0 0 32 32" width="32" height="32"><rect width="32" height="32" rx="8" fill="currentColor"/><path d="M5 24 12 13l4 5 5-8 6 14z" fill="var(--bg)"/></svg></span><span class="bt">Rindge Town Guide</span><span class="bu">Unofficial</span></a>
  <nav class="mainnav" aria-label="Main"><ul>'''+nav+'''</ul></nav>
  <div class="tools">
   <button type="button" class="toolbtn js-only" id="searchBtn" aria-haspopup="dialog" aria-keyshortcuts="Control+K Meta+K">'''+ic('search')+'''<span class="tlab">Search</span><kbd class="kbd" aria-hidden="true">Ctrl K</kbd></button>
   <button type="button" class="toolbtn js-only" id="displayBtn" aria-expanded="false" aria-controls="displayPanel">'''+ic('text')+'''<span class="tlab">Display</span></button>
  </div>
 </div>
 <div class="popover" id="displayPanel" role="region" aria-label="Display settings" hidden>
  <div class="pop-row"><p class="pop-k" id="sizeK">Text size</p>
   <div class="segctl" role="group" aria-labelledby="sizeK">
    <button type="button" class="segb" data-size="-1" aria-label="Smaller text">A&minus;</button>
    <button type="button" class="segb" data-size="0" aria-label="Default text size">A</button>
    <button type="button" class="segb" data-size="1" aria-label="Larger text">A+</button>
   </div><p class="pop-v" id="sizeV" aria-live="polite"></p></div>
  <div class="pop-row"><p class="pop-k" id="themeK">Colors</p>
   <div class="segctl seg4" role="radiogroup" aria-labelledby="themeK">
    <button type="button" class="segb" role="radio" data-theme-set="light" aria-checked="false">'''+ic('sun')+'''<span>Light</span></button>
    <button type="button" class="segb" role="radio" data-theme-set="dark" aria-checked="false">'''+ic('moon')+'''<span>Dark</span></button>
    <button type="button" class="segb" role="radio" data-theme-set="contrast" aria-checked="false">'''+ic('contrast')+'''<span>High contrast</span></button>
    <button type="button" class="segb" role="radio" data-theme-set="auto" aria-checked="false">'''+ic('grid')+'''<span>Match device</span></button>
   </div></div>
  <p class="note">Settings are saved on this device only.</p>
 </div>
</header>
<div class="layout">
 <aside class="rail" aria-label="Contents"><nav aria-label="Contents"><p class="rail-k">Contents</p><ul>'''+rail+'''</ul></nav></aside>
 <main id="main" tabindex="-1">
  <section class="home" id="home" aria-labelledby="home-h">
   <p class="kick">Town of Rindge · Cheshire County · New Hampshire</p>
   <h1 id="home-h">What would you like to know?</h1>
   <p class="lead">A plain-language guide to Rindge town government: meetings, votes, money, rules, services and documents. Every fact is labeled by source.</p>
   <form class="homesearch js-only" role="search" action="#" onsubmit="return false"><label for="homeq" class="sr">Search the guide</label>'''+ic('search')+'''<input type="search" id="homeq" placeholder="Search meetings, laws, offices, documents…" autocomplete="off"><kbd class="kbd js-only" aria-hidden="true">Ctrl K</kbd></form>
   <ul class="tasks">'''+tasks+'''</ul>
   <h2 class="morek">More questions</h2>
   <ul class="minis">'''+more+'''</ul>
   <ul class="meta" aria-label="At a glance">
    <li>Population 6,502 (2025 estimate)</li>
    <li>2025 tax rate $13.79 per $1,000</li>
    <li>SB2 town · next vote Tue Mar 9, 2027</li>
   </ul>
  </section>
 '''+disc+'''
'''+body+''' </main>
</div>
'''+S['foot']+'''<nav class="bottomnav js-only" aria-label="Main (bottom)"><ul>'''+bnav+'''</ul></nav>
<button type="button" id="toTop" aria-label="Back to top">'''+ic('up')+'''</button>
<div class="viewer" id="viewer" role="dialog" aria-modal="true" aria-labelledby="vTitle" hidden>
 <div class="v-head">
  <div class="v-tl"><p class="v-k" id="vKind"></p><h2 id="vTitle" tabindex="-1"></h2><p class="v-src"><span class="sr">Source: </span><a id="vSrc" href="#" target="_blank" rel="noopener"></a></p></div>
  <div class="v-act">
   <button type="button" class="vbtn" id="vPrev">'''+ic('prev')+'''<span>Previous</span></button>
   <button type="button" class="vbtn" id="vNext"><span>Next</span>'''+ic('next')+'''</button>
   <a class="vbtn" id="vOrig" href="#" target="_blank" rel="noopener">'''+ic('external')+'''<span>Open original on rindgenh.org</span></a>
   <a class="vbtn" id="vDown" href="#" download>'''+ic('download')+'''<span>Download</span></a>
   <button type="button" class="vbtn vclose" id="vClose">'''+ic('close')+'''<span>Close</span></button>
  </div>
 </div>
 <div class="v-body" id="vBody"></div>
 <p class="v-foot" id="vFoot"></p>
</div>
<div class="searchdlg" id="searchDlg" role="dialog" aria-modal="true" aria-labelledby="sdTitle" hidden>
 <div class="sd-box">
  <h2 id="sdTitle" class="sr">Search this guide</h2>
  <div class="sd-in">'''+ic('search')+'''<input type="search" id="sdq" role="combobox" aria-expanded="true" aria-controls="sdres" aria-autocomplete="list" placeholder="Search meetings, issues, laws, offices, documents" autocomplete="off"><button type="button" class="vbtn" id="sdClose">'''+ic('close')+'''<span>Close</span></button></div>
  <p class="sd-hint" id="sdHint" aria-live="polite">Type at least 2 letters. Use the arrow keys to move, Enter to open, Esc to close.</p>
  <ul id="sdres" role="listbox" aria-label="Search results"></ul>
 </div>
</div>
<div id="toast" role="status" aria-live="polite"></div>
<script type="application/json" id="docdata">{{DOCDATA}}</script>
<script type="application/json" id="searchdata">{{SEARCHDATA}}</script>
<script>
{{JS}}
</script>
</body>
</html>
'''
open('/workspace/rindge_2026_site/src/template.html','w').write(tpl)
print(len(tpl))
