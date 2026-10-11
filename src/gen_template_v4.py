# v4 template generator: one navigation pattern (slim sticky top bar + Menu sheet),
# Start-here home with task cards, breadcrumbs, one-sentence summaries.
# Run: python3 src/gen_template_v4.py  (writes src/template.html), then python3 src/build.py
import os, html as H
OUT = os.path.join(os.path.dirname(__file__), 'template.html')
def ic(n, cls='i'): return f'<svg class="{cls}" aria-hidden="true" focusable="false"><use href="#i-{n}"/></svg>'

# ---- navigation model: (group id, label, icon, one-line description, [(section id, label)])
GROUPS = [
 ('start-group', 'Start here', 'home', 'How this guide works, and the basics about Rindge.',
   [('home', 'Home'), ('start', 'How this guide works'), ('glossary', 'Glossary of terms'), ('facts', 'Town facts and history')]),
 ('happening', "What's happening", 'chart', 'The issues of 2026, the March election, and the questions that keep coming back.',
   [('topics', '2026 topics'), ('election', 'March 2026 election'), ('recurring', 'Issues that keep coming up')]),
 ('meetdocs', 'Meetings and dates', 'calendar', 'Every 2026 meeting, and the dates and deadlines ahead.',
   [('timeline', '2026 meeting timeline'), ('calendar', 'Upcoming dates and deadlines')]),
 ('documents', 'Documents', 'doc', 'Agendas, minutes, ordinances and annual reports, opened right here.',
   [('library', 'Document library')]),
 ('reports', 'Town reports', 'book', 'Every annual town report, from 2025 back to the 1800s.',
   [('townreports', 'Annual town reports')]),
 ('money', 'Money and taxes', 'coins', 'Tax rates, the town budget, and how votes and taxes have changed since 2011.',
   [('numbers', 'Rindge by the numbers'), ('budget', 'Budget and finances'), ('trends', 'Trends since 2011')]),
 ('rules', 'Laws and rules', 'scale', 'Zoning, regulations and the state laws behind them, in plain language.',
   [('laws', 'Laws and regulations')]),
 ('howdoi', 'How do I...', 'question', 'Step-by-step help, emergencies and utilities, and schools.',
   [('howto', 'How do I...? guides'), ('emergency', 'Emergency and utilities'), ('schools', 'Schools and community')]),
 ('contacts', 'Contacts', 'phone', 'Who to call: town offices, departments and boards.',
   [('directory', 'Town directory')]),
 ('about', 'About this guide', 'info', 'What is missing, where sources disagree, and every source link.',
   [('gaps', 'Gaps and conflicts'), ('sources', 'Sources')]),
]
TOPLINKS = [('happening', "What's happening"), ('meetdocs', 'Meetings'), ('documents', 'Documents'), ('money', 'Money'), ('rules', 'Laws &amp; rules'), ('howdoi', 'How do I'), ('contacts', 'Contacts')]
SEC_GROUP = {sid: (gid, glab) for gid, glab, _, _, secs in GROUPS for sid, _ in secs}
SEC_LABEL = {sid: lab for _, _, _, _, secs in GROUPS for sid, lab in secs}

def menu_groups(prefix):
    out = []
    for gid, glab, gic, gdesc, secs in GROUPS:
        items = ''.join(f'<li><a href="#{sid}" data-nav="{sid}">{H.escape(lab)}{ic("chev","i mchev")}</a></li>' for sid, lab in secs)
        out.append(f'<section class="mgroup" aria-labelledby="{prefix}-{gid}"><h3 id="{prefix}-{gid}" class="mg-h">{ic(gic)}<span>{H.escape(glab)}</span></h3><ul>{items}</ul></section>')
    return ''.join(out)

def footer_map():
    cols = []
    for gid, glab, gic, gdesc, secs in GROUPS:
        cols.append(f'<div><h3><a href="#{gid}">{H.escape(glab)}</a></h3><ul>' + ''.join(f'<li><a href="#{sid}">{H.escape(lab)}</a></li>' for sid, lab in secs) + '</ul></div>')
    return ''.join(cols)

def crumbs(sid):
    gid, glab = SEC_GROUP[sid]
    return (f'<nav class="crumbs" aria-label="Breadcrumb"><ol><li><a class="crumb-home" href="#home">{ic("prev")}<span>Home</span></a></li>'
            f'<li><a href="#{gid}">{H.escape(glab)}</a></li><li><span aria-current="location">{H.escape(SEC_LABEL[sid])}</span></li></ol></nav>')

def sec(sid, hid, title, summary, body, plain=None, intro=None):
    it = f'<p class="intro">{intro}</p>' if intro else ''
    p = f'<div class="plain" role="note"><p class="plain-k">{ic("info")}<span>In plain language</span></p><p>{plain}</p>{it}</div>' if plain else ''
    if plain: it = ''
    return (f'<section class="sec" id="{sid}" aria-labelledby="{hid}">{crumbs(sid)}'
            f'<div class="sechead"><h2 id="{hid}">{title}</h2><button type="button" class="sharebtn js-only" data-share="{sid}">{ic("link")}<span>Share</span><span class="sr"> a link to this section</span></button></div>'
            f'<p class="summary">{summary}</p>{p}{it}{body}</section>\n')

def groupban(gid):
    for g, glab, gic, gdesc, secs in GROUPS:
        if g == gid:
            links = ''.join(f'<li><a href="#{sid}">{H.escape(lab)}</a></li>' for sid, lab in secs)
            return (f'<div class="groupban" id="{gid}" tabindex="-1" role="group" aria-label="{H.escape(glab)}"><div class="gb-ic">{ic(gic)}</div>'
                    f'<div class="gb-txt"><p class="gb-k">{H.escape(glab)}</p><p class="gb-d">{H.escape(gdesc)}</p><ul class="gb-l">{links}</ul></div></div>\n')
    raise KeyError(gid)

TASKS = [
 ('timeline', 'chart', 'What happened this year?', 'Every 2026 meeting, vote and decision, with sources.'),
 ('calendar', 'calendar', 'When is the next meeting?', 'Board meetings this fall and the March 2027 ballot calendar.'),
 ('library', 'doc', 'Find a document', 'Agendas, minutes, ordinances and annual reports, opened right here.'),
 ('howto', 'question', 'How do I...?', 'Permits, licenses, voting and property tax questions, step by step.'),
 ('directory', 'phone', 'Who do I call?', 'Town offices and boards, with phone numbers and hours.'),
 ('numbers', 'tax', 'Taxes and exemptions', 'The tax rate, the 2025 revaluation and elderly exemptions.'),
]
MINIS = [
 ('election', 'vote', 'How did the March 2026 vote go?'),
 ('calendar', 'vote', 'What is on the March 2027 ballot?'),
 ('how-file-a-citizen-petition-for-the-march-ba', 'petition', 'How do I file a petition?'),
 ('laws', 'frontage', 'What are the zoning rules for my lot?'),
 ('budget', 'coins', 'How does the town spend money?'),
 ('townreports', 'book', 'Where are the annual town reports?'),
 ('emergency', 'alert', 'What do I do in an emergency?'),
 ('schools', 'school', 'Which schools serve Rindge?'),
 ('topics', 'elder', 'Elderly exemption limits'),
]
tasks = ''.join(f'<li><a class="task" href="#{h}"><span class="task-ic">{ic(i)}</span><span class="task-t">{H.escape(t)}</span><span class="task-d">{H.escape(d)}</span><span class="task-go">{ic("chev")}</span></a></li>' for h, i, t, d in TASKS)
minis = ''.join(f'<li><a class="mini" href="#{h}">{ic(i)}<span>{H.escape(t)}</span></a></li>' for h, i, t in MINIS)

HOME = f'''<section class="home" id="home" aria-labelledby="home-h">
 <p class="kick"><span class="kick-pill">Unofficial</span> Community research about the Town of Rindge, New Hampshire. Not affiliated with or endorsed by the Town.</p>
 <h1 id="home-h">What would you like to know?</h1>
 <p class="lead">A plain-language guide to Rindge town government: meetings, votes, money, rules, services and documents. Every fact is labeled by source.</p>
 <div class="homesearch js-only" role="search"><button type="button" class="hs-btn" id="homeSearch" aria-haspopup="dialog">{ic("search")}<span class="hs-ph">Search meetings, laws, offices, documents…</span><kbd class="kbd" aria-hidden="true">Ctrl K</kbd></button></div>
 <ul class="quickcall" aria-label="Phone numbers">
  <li><a class="qc qc-911" href="tel:911">{ic("alert")}<span class="qc-t">Emergency</span><span class="qc-n">911</span></a></li>
  <li><a class="qc" href="tel:+16038995009">{ic("shield")}<span class="qc-t">Police, non-emergency</span><span class="qc-n">(603) 899-5009</span></a></li>
  <li><a class="qc" href="tel:+16038995181">{ic("building")}<span class="qc-t">Town Offices</span><span class="qc-n">(603) 899-5181</span></a></li>
 </ul>
 <h2 class="sr">Popular tasks</h2>
 <ul class="tasks">{tasks}</ul>
 <h2 class="morek">More questions</h2>
 <ul class="minis">{minis}</ul>
 <ul class="meta" aria-label="At a glance">
  <li>Population 6,502 (2025 estimate)</li>
  <li>2025 tax rate $13.79 per $1,000</li>
  <li>SB2 town · next vote Tue Mar 9, 2027</li>
  <li>Last updated <time datetime="2026-10-09">Oct 9, 2026</time></li>
 </ul>
 <div class="card disclaimer" role="note" aria-labelledby="disc-h">
  <div class="ic">{ic("scale")}</div>
  <div>
   <h2 id="disc-h" class="disc-h">Before you rely on anything here</h2>
   <p><strong>Summary, not legal advice.</strong> Compiled from public sources: town agendas and minutes, state statutes, census and tax data, news reports, and a small number of clearly labeled unofficial sources. This is not an official town record. Vote tallies come from minutes text and should be checked against the linked PDFs. Before relying on any item, verify it with the <strong>Rindge Town Clerk</strong>, the <strong>Planning Department</strong>, Town Counsel or the <strong>NH Department of Revenue Administration</strong>.</p>
   <ul class="legend" aria-label="Source labels">
    <li><span class="bdg b-official">Official</span> approved minutes or official document</li>
    <li><span class="bdg b-draft">Official · draft minutes</span> posted, not yet approved</li>
    <li><span class="bdg b-agenda">Official agenda</span> outcome not verified</li>
    <li><span class="bdg b-press">Press-reported</span></li>
    <li><span class="bdg b-audio">Unofficial, from meeting audio</span> approximate</li>
    <li><span class="bdg b-auto">Automated summary</span> unconfirmed</li>
    <li><span class="bdg b-derived">Derived / statutory</span> not posted by the town</li>
    <li><span class="bdg b-conf">Confirmed</span> <span class="bdg b-unconf">Unconfirmed</span></li>
   </ul>
   <p class="note">Official votes shown are from approved minutes through Aug 12 (Select Board), Aug 4 (Planning Board) and Aug 10 (Conservation Commission), plus ZBA draft minutes. Later outcomes are labeled by source.</p>
  </div>
 </div>
</section>
'''

S = {}
S['start'] = sec('start', 'st-h', 'How this guide works',
 'This guide gathers Rindge town government records in one place and labels every fact by where it came from.',
 f'''<ol class="parts">
   <li><a href="#timeline"><span class="pn">1</span><strong>2026 so far</strong><span>Meetings, the March election, tax numbers and the big topics.</span></a></li>
   <li><a href="#trends"><span class="pn">2</span><strong>Patterns over the years</strong><span>Budget votes, zoning, tax rates and caseloads since 2011, plus the issues that keep coming up.</span></a></li>
   <li><a href="#laws"><span class="pn">3</span><strong>The rules</strong><span>Rindge's zoning and regulations, and the state and county laws behind them, in plain language.</span></a></li>
   <li><a href="#gaps"><span class="pn">4</span><strong>Check it yourself</strong><span>What's missing, where sources disagree, and every source link.</span></a></li>
  </ol>
  <div class="grid g2 mt3">
   <div class="card"><h3>How to read the labels</h3>
    <ul class="facts">
     <li><span class="bdg b-official">Official</span> A town, state or federal document, such as approved minutes or an annual report.</li>
     <li><span class="bdg b-text">Official · text-extracted · verify against PDF</span> <span class="bdg b-scan">Official · scan, verify against PDF</span> Numbers that software read from a PDF or scan. Check the original before quoting.</li>
     <li><span class="bdg b-draft">Official · draft minutes</span> Posted but not yet approved.</li>
     <li><span class="bdg b-press">Press-reported</span> From a newspaper or a state or association summary.</li>
     <li><span class="bdg b-audio">Unofficial, from meeting audio</span> <span class="bdg b-auto">Automated summary</span> Context only, and approximate.</li>
     <li><span class="bdg b-derived">Derived / statutory</span> Dates computed from state law. The town has not posted them.</li>
     <li><span class="bdg b-gap">Gap</span> <span class="bdg b-gap">Withheld</span> Not found, or held back because the printed figure looks wrong.</li>
    </ul></div>
   <div class="card coming"><h3>What's coming up</h3>
    <ol class="cu">{{{{COMING}}}}</ol>
    <p class="note">The full list is in <a href="#calendar">Upcoming dates and deadlines</a>.</p></div>
  </div>
  <div class="card mt3" id="glossary"><h3>Glossary</h3><dl class="gloss">{{{{GLOSS}}}}</dl>
   <p class="note">Plain-language summaries, not legal advice. See the <a href="#laws">Laws</a> section for sources.</p></div>''',
 intro='The guide is organized by question. Use the <strong>Menu</strong> button at the top of the screen to see every part, or <strong>Search</strong> (Ctrl+K, or Cmd+K on a Mac) to find anything.')
S['facts'] = sec('facts', 'facts-h', 'Town facts and history',
 'Rindge, incorporated in 1768, is a town of about 6,500 people with many lakes and ponds on the Massachusetts border.',
 '{{FACTS}}',
 plain='It covers about 40 square miles and had 6,476 residents in the 2020 Census.')
S['topics'] = sec('topics', 'top-h', 'Topics',
 'Short briefings on the subjects that came up most in 2026.',
 '{{TOPICS}}',
 plain='They cover the budget, ambulance service, zoning, wetlands, elderly exemptions and more. Select a topic to open it.',
 intro='Each item carries its source label.')
S['election'] = sec('election', 'el-h', 'March 2026 election',
 'Voters turned down the proposed town budget in March 2026, so the $5,654,177 default budget applies.',
 '<div class="grid g3" id="elecCharts">{{ELEC}}</div><div class="mt2">{{CRFTABLE}}</div>',
 plain='The proposed budget was $5.81 million and lost 707-824. All seven savings-fund articles passed. These results come from newspapers; the town has not posted official results.',
 intro='The Deliberative Session was Sat Jan 31, 2026 <span class="bdg b-official">Official</span> and voting was Tue Mar 10, 2026 (7am–7pm, Rindge Memorial School). The town\'s results page returned an error on Oct 9, so the tallies are as reported by the Monadnock Ledger-Transcript and the Keene Sentinel, both re-checked online on Oct 9. They are not yet in any annual report.')
S['recurring'] = sec('recurring', 'rc-h', 'Things that keep coming up',
 'Some issues, such as lot frontage, wetlands setbacks and the budget, return year after year.',
 '<div class="callout"><strong>About the dates.</strong> The town\'s online agendas and minutes begin in <strong>Sept 2024</strong>. Earlier history here comes from annual reports and press, so "first found" is the earliest record found, not necessarily when an issue first arose. For older minutes, submit a records request to the Executive Secretary or Town Administrator at the Town Offices.</div>{{ISSUES}}',
 plain='The list also covers back lots, ambulance service and school costs. Each card shows when an issue first appears in the records and what has happened since.')
S['timeline'] = sec('timeline', 'tl-h', 'Meeting timeline, January 1 – October 9, 2026',
 'Every 2026 board meeting found on the town\'s pages, with links to its agenda, minutes and video.',
 '''<div class="controls js-only" role="search" aria-label="Filter meetings">
   <div class="chips" role="group" aria-label="Filter by board">
    <button type="button" class="chip" aria-pressed="true" data-b="__all" style="--c:var(--accent)">All boards</button>
    {{CHIPS}}
   </div>
   <div class="row">
    <div class="searchwrap field"><label for="q">Search the timeline</label><input type="search" id="q" placeholder="e.g. Dolly Lane, wetlands, ambulance" autocomplete="off"></div>
    <div class="field"><label for="srcSel">Source</label><select id="srcSel">
     <option value="all">All sources</option><option value="official">Official records only</option><option value="press">Press-reported</option><option value="unofficial">Unofficial (audio, automated)</option></select></div>
    <div class="field"><label for="minSel">Minutes</label><select id="minSel">
     <option value="all">Any</option><option value="yes">Minutes posted</option><option value="no">No minutes posted</option></select></div>
   </div>
   <p class="count" id="count" aria-live="polite">Showing all {{NEV}} entries</p>
  </div>
  <ol class="tl" id="tl">
{{TIMELINE}}
  </ol>
  <p class="empty" id="empty" hidden>No entries match these filters.</p>''',
 plain='There are 70 entries from January 1 to October 9, 2026, including the Deliberative Session, the election and two school board meetings. Pick a board or search for a road or topic. Every entry says where its information comes from.')
S['calendar'] = sec('calendar', 'cal-h', 'Key dates: fall 2026 and the March 2027 ballot',
 'The next town vote is Tuesday, March 9, 2027, and most deadlines before it are worked out from state law rather than posted by the town.',
 '''<div class="segfilter js-only" role="group" aria-label="Filter key dates">
   <button type="button" class="tab" aria-pressed="true" data-f="all">All</button>
   <button type="button" class="tab" aria-pressed="false" data-f="sb2">Election &amp; warrant deadlines</button>
   <button type="button" class="tab" aria-pressed="false" data-f="meet">Board meetings</button>
  </div>
  <div class="calgrid">{{CALGRID}}</div>
  <ol class="ulist" id="ulist">
{{UPLIST}}
  </ol>''',
 plain='The town has not posted its 2027 calendar. Dates here come from regular meeting patterns (labeled unofficial / inferred) or from state law and the NH Municipal Association\'s generic 2027 SB2 calendar (labeled derived). Confirm any date with the Town Clerk\'s office before relying on it.')
S['library'] = sec('library', 'library-h', 'Document library',
 'Open any of the {{NDOCS}} town documents cited in this guide right here, without leaving the site.',
 '{{LIBRARY}}',
 plain='Search or filter by board, type or year. The originals on rindgenh.org are authoritative.',
 intro='Town documents are byte-for-byte copies of what rindgenh.org served on Oct 9, 2026, with a checksum for each in docs/MANIFEST.json. Other sources open in the viewer only if the source allows it; otherwise they open in a new tab.')
S['townreports'] = sec('townreports', 'tr2-h', 'Annual town reports',
 'Every annual report of the Town of Rindge from {{RPT_FIRST}} to {{RPT_LAST}}, in one place, plus where to find the older ones.',
 '{{TOWNREPORTS}}',
 plain='Each spring the town publishes a report on the year before: the budget and what was spent, the town meeting results, tax rates, and a report from every department and board. Select a year to read it here.')
S['numbers'] = sec('numbers', 'num-h', 'Rindge by the numbers',
 'The key figures, including the 2025 tax rate of $13.79 per $1,000 and the elderly exemption count.',
 '''<div class="grid g4">
   <div class="card stat"><div class="n" data-count="6476">6,476</div><div class="l">Population, 2020 Census</div><div class="s"><span class="bdg b-official">Official · US Census</span></div></div>
   <div class="card stat"><div class="n" data-count="6502">6,502</div><div class="l">Population estimate, July 1, 2025</div><div class="s"><span class="bdg b-official">Official · US Census</span></div></div>
   <div class="card stat"><div class="n">$13.79</div><div class="l">2025 tax rate per $1,000 (2024: $25.31)</div><div class="s"><span class="bdg b-official">Official · Town / NH DRA</span></div></div>
   <div class="card stat"><div class="n">+89.6%</div><div class="l">Average residential value change, 2025 revaluation</div><div class="s"><span class="bdg b-official">Official · Town</span></div></div>
   <div class="card stat"><div class="n">$19,904,756</div><div class="l">2025 total property tax commitment</div><div class="s"><span class="bdg b-official">Official · NH DRA</span></div></div>
   <div class="card stat"><div class="n">$5,654,177</div><div class="l">2026 default operating budget (in effect after the proposed budget failed)</div><div class="s"><span class="bdg b-official">Official · 2026 warrant</span></div></div>
   <div class="card stat"><div class="n" data-count="52">52</div><div class="l">Elderly exemptions in 2025, totaling $6,559,100 of assessed value</div><div class="s"><span class="bdg b-official">Official · MS-1</span></div></div>
   <div class="card stat"><div class="n" data-count="13">13</div><div class="l">Solar exemptions approved by the Select Board, Feb 25</div><div class="s"><span class="bdg b-official">Official · minutes</span></div></div>
  </div>
  <div class="card chart mt2" id="taxcard">
   <h3>Tax rate per $1,000 of assessed value, 2020–2025 <span class="bdg b-official">Official · 2025 Annual Report</span></h3>
   <p class="note">Each bar is the total rate split into its four parts, on a common $0–$30 scale. The 2025 drop reflects the revaluation: assessed values roughly doubled, so the rate per $1,000 fell. It does not mean every tax bill fell. In 2025, local school was {{SH_LOCAL}}% of the rate, town {{SH_TOWN}}%, county {{SH_COUNTY}}% and state education {{SH_STATE}}%.</p>
   {{TAXCHART}}
   {{TAXTABLE}}
  </div>''',
 plain='About 6,500 people live in Rindge. After the 2025 revaluation the tax rate fell to $13.79 per $1,000, because assessed values roughly doubled. That does not mean tax bills were cut in half.')
S['budget'] = sec('budget', 'budget-h', 'Budget and finances',
 'The town spends about $5.5 to $5.8 million a year on its own operations, before school and county taxes.',
 '{{BUDGET}}',
 plain='Voters rejected the proposed budget in 2025 and 2026, so the default budget applies. The largest lines are police, highway and fire.',
 intro='Department budgets, savings funds, debt and the capital plan, from the town\'s 2024 and 2025 annual reports. 2026 vote results are press-reported.')
S['trends'] = sec('trends', 'tr-h', 'Trends, 2011–2026',
 'How budget votes, zoning changes and tax rates have moved since 2011.',
 '{{TRENDS}}',
 plain='Voters have approved the town budget in most years since 2011, but rejected it in 2011, 2021, 2025 and 2026. Zoning changes usually pass.',
 intro='Built from the town\'s annual reports (2011–2025), the town\'s board index pages and press reports for 2026. Every value is labeled. Values read from scans are marked "verify against PDF", and figures that look like printing errors are withheld.')
S['laws'] = sec('laws', 'lw-h', 'Laws and regulations that apply in Rindge',
 'Plain-language notes on Rindge\'s zoning, its regulations and the state laws behind them, each linked to the official text.',
 '''<p class="callout"><strong>Summary, not legal advice.</strong> These plain-language notes point to the official text. Laws change; read the linked source and check with the Planning Department, Town Clerk or a lawyer before acting.</p>
  {{FLOWS}}
  <div class="mt2">{{DIMS}}</div>
  <div class="controls js-only mt3" role="search" aria-label="Filter laws">
   <div class="chips" role="group" aria-label="Filter by level of government">{{LAWCHIPS}}</div>
   <div class="row"><div class="searchwrap field"><label for="lq">Search laws and rules</label><input type="search" id="lq" placeholder="e.g. frontage, ADU, wetlands, petition" autocomplete="off"></div></div>
   <p class="count" id="lcount" aria-live="polite">Showing all {{NLAW}} entries</p>
  </div>
  <div id="lawlist">{{LAWS}}</div>
  <p class="empty" id="lempty" hidden>No entries match. Try another word.</p>
  <div class="mt2">{{RECENT}}</div>''',
 plain='Rindge\'s zoning ordinance sets lot sizes, setbacks and frontage (250 feet on a public road in the residential and village districts). State law sets how rules change: zoning changes and citizen petitions go to voters on the March ballot. This is a summary, not legal advice.')
S['howto'] = sec('howto', 'howto-h', 'How do I...?',
 'Step-by-step help with common tasks, from permits and licenses to property tax bills.',
 '{{HOWTO}}',
 plain='Guides cover permits, dog licenses, registering a vehicle, voting, and appealing or lowering a property tax bill. Each one says who to contact and what to check first.')
S['emergency'] = sec('emergency', 'emergency-h', 'Emergency and utilities',
 'In an emergency, call 911.',
 '{{EMERG}}',
 plain='Ambulance service is due to switch to Peterborough Fire &amp; Rescue on January 1, 2027 (press-reported). No town water or sewer system is listed, so homes generally use private wells and septic (unconfirmed).')
S['schools'] = sec('schools', 'schools-h', 'Schools and community',
 'Rindge children attend the Jaffrey-Rindge Cooperative School District (SAU 47), whose budget is voted separately from the town\'s.',
 '{{SCHOOLS}}',
 plain='Rindge Memorial School serves PreK–5, then students go to Conant Middle and High School in Jaffrey.')
S['directory'] = sec('directory', 'directory-h', 'Town directory: who to call',
 'For most questions, call the Town Offices at (603) 899-5181; in an emergency, dial 911.',
 '{{DIRECTORY}}',
 plain='Each office below lists its phone number, hours and town web page. Offices are listed by title. Checked Oct 9, 2026.')
S['gaps'] = sec('gaps', 'gap-h', 'Known gaps and conflicts',
 'Where sources disagree and what could not be found, so you know what to double-check.',
 '''<div class="grid g2">
   <div class="card"><h3>Conflicts between sources</h3>{{CONF}}</div>
   <div class="card"><h3>Gaps: not found or not posted</h3>{{GAPS}}</div>
  </div>''',
 plain='No source is perfect. Check these items before relying on them. Current as of Oct 9, 2026.')
S['sources'] = sec('sources', 'src-h', 'Sources',
 'Every source used in this guide, grouped by type.',
 '<div class="card srcgrp">{{SOURCES}}</div>',
 intro='The town website is rindgenh.org / rindgenh.gov. Town documents open inside this site from copies; other sources open in the document viewer when the source allows it, otherwise in a new tab.')

body = [HOME]
for gid, glab, gic, gdesc, secs in GROUPS:
    body.append(groupban(gid))
    for sid, _ in secs:
        if sid in S: body.append(S[sid])
MAIN = ''.join(body)

toplinks = ''.join(f'<li><a href="#{g}" data-nav="{g}">{t}</a></li>' for g, t in TOPLINKS)

TPL = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Rindge Town Guide (unofficial): meetings, votes, budget, rules, services and documents</title>
<meta name="description" content="Unofficial community research summary of Rindge, New Hampshire town government in 2026: meetings, votes, the March election, tax rates, zoning and key dates for the March 2027 ballot. Every fact is source-labeled.">
<meta name="color-scheme" content="light dark">
<meta name="theme-color" media="(prefers-color-scheme: light)" content="#f5f5f7">
<meta name="theme-color" media="(prefers-color-scheme: dark)" content="#000000">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%230a5cb8'/%3E%3Cpath d='M8 50 L24 26 L32 36 L42 18 L56 50Z' fill='%23ffffff'/%3E%3C/svg%3E">
<script>
(function(){{var d=document.documentElement;d.classList.add('js');
try{{var t=localStorage.getItem('rindgeTheme');if(t&&t!=='auto')d.setAttribute('data-theme',t);var z=localStorage.getItem('rindgeSize');if(z&&z!=='0')d.setAttribute('data-size',z);}}catch(e){{}}
if(!(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches)&&'IntersectionObserver' in window)d.classList.add('anim');}})();
</script>
<style>
{{{{CSS}}}}
</style>
</head>
<body>
{{{{SPRITE}}}}
<a class="skip" href="#main">Skip to main content</a>
<header class="topbar" id="top">
 <div class="bar">
  <a class="brand" href="#home"><span class="logo" aria-hidden="true"><svg viewBox="0 0 32 32" width="30" height="30"><rect width="32" height="32" rx="8" fill="currentColor"/><path d="M5 24 12 13l4 5 5-8 6 14z" fill="#fff"/></svg></span><span class="bt-wrap"><span class="bt">Rindge Town Guide</span><span class="bu">Unofficial · not a Town site</span></span></a>
  <nav class="toplinks" aria-label="Main"><ul>{toplinks}</ul></nav>
  <div class="tools">
   <button type="button" class="toolbtn js-only" id="searchBtn" aria-haspopup="dialog" aria-keyshortcuts="Control+K Meta+K">{ic("search")}<span class="tlab">Search</span><span class="sr"> this guide</span></button>
   <button type="button" class="toolbtn menubtn js-only" id="menuBtn" aria-haspopup="dialog" aria-expanded="false" aria-controls="menu">{ic("menu")}<span class="tlab-m">Menu</span></button>
   <a class="toolbtn menubtn nojs-only" href="#sitemap">{ic("menu")}<span class="tlab-m">Menu</span></a>
  </div>
 </div>
 <div id="progress" aria-hidden="true"></div>
</header>
<main id="main" tabindex="-1">
{MAIN}
</main>
<footer class="foot" id="sitemap">
 <div class="foot-in">
  <h2 class="foot-h">Everything in this guide</h2>
  <nav class="sitemap" aria-label="Site map">{footer_map()}</nav>
  <div class="grid g3 foot-about">
   <div><h3>About</h3><p>Unofficial community research, not affiliated with the Town of Rindge. Summary, not legal advice. Last updated <time datetime="2026-10-09">Oct 9, 2026</time>.</p></div>
   <div><h3>Report a correction</h3><p>If you spot an error, please let the publisher of this page know. To verify official records, contact the Planning Department or the Town Clerk at the Rindge Town Offices, 30 Payson Hill Road, Rindge, NH 03461, (603) 899-5181.</p></div>
   <div><h3>Official sources first</h3><p>Approved minutes on the town website are the official record. Items labeled unofficial, automated or inferred are provided for context only.</p></div>
  </div>
 </div>
</footer>
<button type="button" id="toTop" class="js-only" aria-label="Back to top">{ic("up")}<span class="tt-l" aria-hidden="true">Top</span></button>
<div class="menu" id="menu" role="dialog" aria-modal="true" aria-labelledby="menuTitle" hidden>
 <div class="m-scrim" data-close="menu"></div>
 <div class="m-sheet">
  <div class="m-head"><h2 id="menuTitle">Menu</h2><button type="button" class="vbtn m-close" id="menuClose">{ic("close")}<span>Close</span></button></div>
  <div class="m-scroll">
   <button type="button" class="hs-btn m-search" id="menuSearch">{ic("search")}<span class="hs-ph">Search this guide</span></button>
   <nav aria-label="All sections">{menu_groups("mg")}</nav>
   <section class="mgroup m-display" aria-labelledby="dispK"><h3 class="mg-h" id="dispK">{ic("text")}<span>Display</span></h3>
    <div class="pop-row"><p class="pop-k" id="sizeK">Text size</p>
     <div class="segctl" role="group" aria-labelledby="sizeK">
      <button type="button" class="segb" data-size="-1" aria-label="Smaller text">A&minus;</button>
      <button type="button" class="segb" data-size="0" aria-label="Default text size">A</button>
      <button type="button" class="segb" data-size="1" aria-label="Larger text">A+</button>
     </div><p class="pop-v" id="sizeV" aria-live="polite"></p></div>
    <div class="pop-row"><p class="pop-k" id="themeK">Appearance</p>
     <div class="segctl seg4" role="radiogroup" aria-labelledby="themeK">
      <button type="button" class="segb" role="radio" data-theme-set="auto" aria-checked="false">{ic("grid")}<span>Automatic</span></button>
      <button type="button" class="segb" role="radio" data-theme-set="light" aria-checked="false">{ic("sun")}<span>Light</span></button>
      <button type="button" class="segb" role="radio" data-theme-set="dark" aria-checked="false">{ic("moon")}<span>Dark</span></button>
      <button type="button" class="segb" role="radio" data-theme-set="contrast" aria-checked="false">{ic("contrast")}<span>High contrast</span></button>
     </div></div>
    <p class="note">Settings are saved on this device only.</p>
   </section>
   <p class="m-foot">Unofficial community research. Not affiliated with or endorsed by the Town of Rindge.</p>
  </div>
 </div>
</div>
<div class="viewer" id="viewer" role="dialog" aria-modal="true" aria-labelledby="vTitle" hidden>
 <div class="v-head">
  <button type="button" class="vbtn vclose" id="vClose">{ic("close")}<span>Close</span></button>
  <div class="v-tl"><p class="v-k" id="vKind"></p><h2 id="vTitle" tabindex="-1"></h2><p class="v-src"><span class="sr">Source: </span><a id="vSrc" href="#" target="_blank" rel="noopener"></a></p></div>
  <div class="v-act">
   <a class="vbtn" id="vOrig" href="#" target="_blank" rel="noopener">{ic("external")}<span class="lg">Open original on rindgenh.org</span><span class="sh" aria-hidden="true">Original</span></a>
   <a class="vbtn" id="vDown" href="#" download>{ic("download")}<span>Download</span></a>
  </div>
 </div>
 <div class="v-tools" id="vTools" role="toolbar" aria-label="Page and zoom controls" hidden>
  <div class="vt-g"><button type="button" class="vtb" id="pgPrev" aria-label="Previous page">{ic("chevup")}</button><label class="vt-pg"><span class="sr">Page number</span><input id="pgNum" type="text" inputmode="numeric" autocomplete="off" value="1" aria-describedby="pgOf"></label><span class="vt-of" id="pgOf">of 1</span><button type="button" class="vtb" id="pgNext" aria-label="Next page">{ic("chev")}</button></div>
  <div class="vt-g"><button type="button" class="vtb" id="zOut" aria-label="Zoom out">{ic("zout")}</button><output class="vt-z" id="zVal" aria-live="polite">100%</output><button type="button" class="vtb" id="zIn" aria-label="Zoom in">{ic("zin")}</button><button type="button" class="vtb" id="zFit" aria-label="Fit page width" aria-pressed="true">{ic("fit")}</button></div>
 </div>
 <div class="v-body" id="vBody"></div>
 <div class="v-bar">
  <button type="button" class="vbtn" id="vPrev" aria-label="Previous document">{ic("prev")}<span>Previous</span></button>
  <p class="v-foot" id="vFoot"></p>
  <button type="button" class="vbtn" id="vNext" aria-label="Next document"><span>Next</span>{ic("next")}</button>
 </div>
</div>
<div class="searchdlg" id="searchDlg" role="dialog" aria-modal="true" aria-labelledby="sdTitle" hidden>
 <div class="sd-scrim" data-close="search"></div>
 <div class="sd-box">
  <h2 id="sdTitle" class="sr">Search this guide</h2>
  <div class="sd-in">{ic("search")}<label for="sdq" class="sr">Search this guide</label><input type="search" id="sdq" role="combobox" aria-expanded="true" aria-controls="sdres" aria-autocomplete="list" aria-describedby="sdHint" placeholder="Search meetings, laws, offices, documents" autocomplete="off" enterkeyhint="search"><button type="button" class="vbtn" id="sdClose">{ic("close")}<span>Close</span></button></div>
  <p class="sd-hint" id="sdHint" aria-live="polite">Type at least 2 letters, or pick a suggestion.</p>
  <div class="sd-scroll">
   <div class="sd-sugg" id="sdSugg"></div>
   <ul id="sdres" role="listbox" aria-label="Search results"></ul>
  </div>
 </div>
</div>
<div id="toast" role="status" aria-live="polite"></div>
<script type="application/json" id="docdata">{{{{DOCDATA}}}}</script>
<script type="application/json" id="searchdata">{{{{SEARCHDATA}}}}</script>
<script>
{{{{JS}}}}
</script>
</body>
</html>
'''
open(OUT, 'w').write(TPL)
print('wrote', OUT, len(TPL))
