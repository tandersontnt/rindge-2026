import json, html, calendar, datetime, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from data import NOTES, EXTRA, UPCOMING
import v2, v3
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = lambda s: html.escape(str(s), quote=True)
TODAY = "2026-10-09"

BOARDS = {"sb":("Select Board","var(--sb)"),"pb":("Planning Board","var(--pb)"),"zba":("Zoning Board of Adjustment","var(--zba)"),
 "cc":("Conservation Commission","var(--cc)"),"bac":("Budget Advisory Committee","var(--bac)"),"school":("School Board (JRCSD)","var(--school)"),"town":("Town Meeting / Election","var(--town)")}
SHORT = {"sb":"Select Board","pb":"Planning","zba":"ZBA","cc":"Conservation","bac":"Budget Advisory","school":"School","town":"Town Meeting"}

LABEL = {
 "official":("b-official","Official"),
 "draft":("b-draft","Official · draft minutes"),
 "agenda":("b-agenda","Official agenda · outcome not verified"),
 "press":("b-press","Press-reported"),
 "audio":("b-audio","Unofficial, from meeting audio · approximate until minutes are posted"),
 "auto":("b-auto","Automated summary · unconfirmed"),
 "statute":("b-statute","State law"),
 "derived":("b-derived","Derived from statute / NHMA calendar · not posted by town"),
 "statutory":("b-statutory","Statutory, not confirmed by the town"),
 "inferred":("b-inferred","Unofficial / inferred"),
 "gap":("b-gap","Gap"),
 "conf":("b-conf","Confirmed"),
 "unconf":("b-unconf","Unconfirmed"),
 "posted":("b-official","Official · posted"),
 "text":("b-text","Official · text-extracted · verify against PDF"),
 "scan":("b-scan","Official · scan, verify against PDF"),
 "kw":("b-auto","Automated keyword count of official documents"),
 "assoc":("b-press","State / association summary, not the statute"),
 "withheld":("b-gap","Withheld: suspect duplicate tally"),
 "stale":("b-gap","Stale town page · check with the office"),
 "infer":("b-inferred","Inference, not stated by the town"),
 "role":("b-official","Official · town department page"),
}
def badge(*codes):
    out=[]
    for c in codes:
        cls,t = LABEL[c]; out.append(f'<span class="bdg {cls}">{E(t)}</span>')
    return "".join(out)
VER = '<span class="bdg b-verify">Tally from minutes text; verify against the PDF</span>'
def fact(text, *codes, v=False, raw=False):
    return f'<li>{text if raw else E(text)} {badge(*codes)}{VER if v else ""}</li>'

def fmt(d, wd=True):
    dt = datetime.date.fromisoformat(d)
    s = dt.strftime("%a, %b %-d, %Y") if wd else dt.strftime("%b %-d, %Y")
    return s

# ---------------- events ----------------
meetings = json.load(open(os.path.join(ROOT,"meetings.json")))
events=[]
for m in meetings:
    notes = NOTES.get(m["board"]+"|"+m["date"], [])
    docs=[(d["label"],d["url"]) for d in m["docs"]]
    events.append(dict(board=m["board"],date=m["date"],titles=m["titles"],docs=docs,video=m.get("video"),
        minutes=m["minutes"],draft=m["draft"],src="official",notes=notes))
for x in EXTRA:
    events.append(dict(board=x["board"],date=x["date"],titles=x["titles"],docs=x["docs"],video=None,minutes=None,draft=False,src=x["src"],notes=x["notes"]))
events.append(dict(board="school",date="2026-09-14",titles=["Jaffrey-Rindge Cooperative School Board"],docs=[("MyTownView listing (automated)","https://mytownview.com/new-hampshire/cheshire/rindge/")],video=None,minutes=None,draft=False,src="auto",
    notes=[("An automated summary reports the board directed the superintendent to pursue buying or leasing two 15-passenger vans, amid CTE transportation costs it put at about $930,000. Not verified against district minutes.","auto",0)]))
events.append(dict(board="school",date="2026-10-05",titles=["Jaffrey-Rindge Cooperative School Board"],docs=[("MyTownView listing (automated)","https://mytownview.com/new-hampshire/cheshire/rindge/"),("Ledger-Transcript 10/6/2026","https://ledgertranscript.com/2026/10/06/conant-cte-budget-concerns/")],video=None,minutes=None,draft=False,src="auto",
    notes=[("An automated summary reports a briefing on the HB 1300 school property-tax cap question on the Nov 3 ballot. Not verified against district minutes.","auto",0)]))
events.sort(key=lambda e:(e["date"],list(BOARDS).index(e["board"])))

def ev_html(e):
    name,c = BOARDS[e["board"]]
    up = e["date"]>TODAY
    if e["src"]=="official":
        st = badge("official")
        if e["minutes"]:
            st += '<span class="bdg b-draft">Draft minutes posted</span>' if e["draft"] else '<span class="bdg b-conf">Minutes posted</span>'
        else:
            st += '<span class="bdg b-unconf">No minutes posted</span>'
    else:
        st = badge(e["src"])
    if up: st += '<span class="bdg b-derived">Upcoming</span>'
    srcs = {e["src"]} | {n[1] for n in e["notes"]}
    notes = "".join(f'<li>{E(t)} {badge(s)}{VER if v else ""}</li>' for t,s,v in e["notes"])
    notes = f"<ul>{notes}</ul>" if notes else ""
    docs = "".join(f'<a href="{E(u)}" target="_blank" rel="noopener">{E(l)}<span class="sr"> (opens in new tab)</span></a>' for l,u in e["docs"])
    if e["video"]: docs += f'<a href="{E(e["video"])}" target="_blank" rel="noopener">Video (Town Hall Streams)<span class="sr"> (opens in new tab)</span></a>'
    search = " ".join([name, " ".join(e["titles"]), " ".join(n[0] for n in e["notes"]), fmt(e["date"])]).lower()
    mins = "na" if e["minutes"] is None else ("yes" if e["minutes"] else "no")
    return (f'<li class="card ev{" up" if up else ""}" style="--c:{c}" id="ev-{e["board"]}-{e["date"]}" data-board="{e["board"]}" data-base="{e["src"]}" data-src="{" ".join(sorted(srcs))}" '
            f'data-min="{mins}" data-q="{E(search)}"><div class="hd"><span class="date"><time datetime="{e["date"]}">{fmt(e["date"])}</time></span>'
            f'<span class="bname">{E(name)}</span>{st}</div><p class="ttl">{E(" · ".join(e["titles"]))}</p>{notes}'
            f'{"<div class=docs>"+docs+"</div>" if docs else ""}</li>')

tl=[]; cur=None
for e in events:
    mn = datetime.date.fromisoformat(e["date"]).strftime("%B %Y")
    if mn!=cur: cur=mn; tl.append(f'<li class="month" data-month="{mn}" aria-hidden="false">{mn}</li>')
    tl.append(ev_html(e))
TIMELINE = "\n".join(tl)
counts = {k:sum(1 for e in events if e["board"]==k) for k in BOARDS}
CHIPS = "".join(f'<button type="button" class="chip" aria-pressed="true" data-b="{k}" style="--c:{c}"><span class="dot" aria-hidden="true"></span>{E(n)} <span class="n">({counts[k]})</span></button>' for k,(n,c) in BOARDS.items())

# ---------------- upcoming ----------------
STB = {"posted":("posted","conf"),"inferred":("inferred","unconf"),"press":("press",),"derived":("derived","unconf"),"statutory":("statutory",)}
UPROWS=[]; byday={}
for i,(d,t,b,st,key,end) in enumerate(UPCOMING):
    kind = "meet" if b in ("sb","pb","zba","cc","bac") else "sb2"
    rid=f"up-{d}"
    if d not in byday: byday[d]=(b,[])
    byday[d][1].append(t)
    rid_attr = f' id="{rid}"' if sum(1 for x in UPCOMING[:i] if x[0]==d)==0 else ""
    dd = fmt(d) + (f" – {fmt(end)}" if end else "")
    UPROWS.append(f'<li class="card urow{" key" if key else ""}" style="--c:{BOARDS[b][1]}"{rid_attr} data-kind="{kind}"><div class="dd">{dd}</div>'
                  f'<div>{"<strong>Key date. </strong>" if key else ""}{E(t)} <span class="who">· {E(BOARDS[b][0])}</span></div><div>{badge(*STB[st])}</div></li>')
UPLIST="\n".join(UPROWS)
def month_grid(y,m):
    cal = calendar.Calendar(firstweekday=6)
    rows=[]
    for wk in cal.monthdatescalendar(y,m):
        cells=[]
        for d in wk:
            if d.month!=m: cells.append("<td></td>"); continue
            ds=d.isoformat(); cls=' class="today"' if ds==TODAY else ""
            if ds in byday:
                b,ts=byday[ds]
                lab=f'{fmt(ds)}: '+"; ".join(ts)
                cells.append(f'<td{cls}><a class="d" href="#up-{ds}" style="--c:{BOARDS[b][1]}" aria-label="{E(lab)}" title="{E(lab)}">{d.day}</a></td>')
            else: cells.append(f'<td{cls}><span class="d">{d.day}</span></td>')
        rows.append("<tr>"+"".join(cells)+"</tr>")
    title=datetime.date(y,m,1).strftime("%B %Y")
    head="".join(f'<th scope="col"><abbr title="{n}">{n[0]}</abbr></th>' for n in ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"])
    return f'<div class="card mcal"><h3>{title}</h3><table><caption class="sr">{title}: highlighted days have entries</caption><thead><tr>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>'
CALGRID="".join(month_grid(y,m) for y,m in [(2026,10),(2026,11),(2026,12),(2027,1),(2027,2),(2027,3)])

# ---------------- election charts ----------------
def pct(a,b): return a/(a+b)*100
def yn(title, yes, no, labels=("Yes","No"), cls=("f-yes","f-no"), passed=None, note="", codes=("press",)):
    tot=yes+no; py=pct(yes,no); pn=100-py
    res = "" if passed is None else (f'<span class="result {"r-pass" if passed else "r-fail"}">{"Passed" if passed else "Failed"}</span>')
    bars=""
    for lab,val,p,c in [(labels[0],yes,py,cls[0]),(labels[1],no,pn,cls[1])]:
        bars+=(f'<div class="bar"><div class="lbl"><span>{E(lab)}</span><b>{val:,} · {p:.1f}%</b></div>'
               f'<div class="track" role="img" aria-label="{E(lab)}: {val:,} votes, {p:.1f} percent of {tot:,}"><span class="fill {c}" style="--w:{p:.2f}%"></span></div></div>')
    return (f'<div class="card chart"><h3>{E(title)} {res}</h3>{badge(*codes)}{bars}'
            f'<p class="note">{tot:,} votes on this question. Bars show share of yes + no votes.{(" "+E(note)) if note else ""}</p></div>')
def multi(title, rows, seats, note, codes=("press",)):
    mx=max(v for _,v in rows); tot=sum(v for _,v in rows)
    bars=""
    for i,(n,v) in enumerate(sorted(rows,key=lambda r:-r[1])):
        w=v/mx*100; won=i<seats
        bars+=(f'<div class="bar"><div class="lbl"><span>{E(n)}{" <strong>(elected)</strong>" if won else ""}</span><b>{v:,}</b></div>'
               f'<div class="track" role="img" aria-label="{E(n)}: {v:,} votes"><span class="fill {"f-a" if won else "f-b"}" style="--w:{w:.2f}%"></span></div></div>')
    return f'<div class="card chart"><h3>{E(title)}</h3>{badge(*codes)}{bars}<p class="note">{E(note)} Bar length is relative to the top vote-getter ({mx:,}).</p></div>'
ELEC = "".join([
 yn("Article 3: Town operating budget ($5.81M as amended)",707,824,passed=False,note="The default budget applies: $5,654,177 per the official warrant (press reported $5.64M and $5.7M)."),
 multi("Select Board (one seat, 3-year term)",[("Bob Hamilton",832),("Bob Martin",661)],1,"Incumbent re-elected."),
 multi("Planning Board (two seats)",[("Joel Aho",684),("Jennifer Helsel",683),("Roberta Oeser",671),("Mark Hower",508)],2,"Four candidates for two seats."),
 yn("Article 15: \"Protect the Taxpayer\" (by petition)",1041,486,passed=True,note="Advisory resolution to the Legislature and Governor."),
 yn("Article 16: Rescind ninth police officer position (by petition)",914,619,passed=True,note="Returns authority over the number of full-time officers to the Select Board."),
 yn("Stay with SB2 (official ballot) form of government",278,197,labels=("Stay with SB2","Change"),cls=("f-a","f-b"),note="As reported; question wording not in sources. The low vote total is as reported."),
 yn("Switch to electronic voting machines",198,283,passed=False,note="As reported; the low vote total is as reported."),
 yn("Continue hand-counting ballots",270,207,passed=True,note="As reported."),
])
CRF=[("Art. 4 Highway Department CRF",185000,1004,526),("Art. 5 Fire Department Equipment CRF",125000,1082,446),("Art. 6 Ambulance Service ETF",40000,1307,230),
     ("Art. 7 Building Maintenance CRF",35000,1060,465),("Art. 8 Recreation Facilities CRF",25000,1095,438),("Art. 9 Meetinghouse Maintenance ETF",25000,996,535),("Art. 10 Ingalls Memorial Library ETF",20000,1171,361)]
crf_rows="".join(f'<tr><th scope="row">{E(n)}</th><td class="num">${a:,}</td><td class="num">{y:,}</td><td class="num">{no:,}</td><td class="num">{pct(y,no):.1f}%</td></tr>' for n,a,y,no in CRF)
CRFTABLE=(f'<div class="card"><h3>Capital reserve and trust fund articles (all passed) {badge("press")}</h3><div class="tablewrap"><table class="data"><caption class="sr">2026 capital reserve and expendable trust fund article results</caption>'
 f'<thead><tr><th scope="col">Article</th><th scope="col" class="num">Amount</th><th scope="col" class="num">Yes</th><th scope="col" class="num">No</th><th scope="col" class="num">Yes %</th></tr></thead><tbody>{crf_rows}</tbody></table></div>'
 f'<p class="note">Amounts from the official 2026 warrant (2025 Annual Report); vote counts from the Ledger-Transcript, 3/11/2026. The Recreation article\'s amount was not stated in the press report; $25,000 is the warrant amount.</p></div>')

# ---------------- tax chart ----------------
TAX={2020:(3.88,13.08,1.85,3.64),2021:(3.78,13.43,1.81,3.63),2022:(3.88,14.15,1.31,3.69),2023:(3.75,15.71,1.82,3.76),2024:(4.09,15.70,1.83,3.69),2025:(2.44,8.36,0.98,2.01)}
COMP=[("Town","var(--t-town)"),("Local school","var(--t-local)"),("State education","var(--t-state)"),("County","var(--t-county)")]
AXMAX=30.0
trows=""
for y,(town,loc,st,co) in TAX.items():
    tot=round(town+loc+st+co,2)
    vals=[town,loc,st,co]
    segs="".join(f'<span class="seg" style="--w:{v/AXMAX*100:.3f}%;--sc:{COMP[i][1]}" title="{COMP[i][0]} ${v:.2f}"></span>' for i,v in enumerate(vals))
    al=f"{y}: total ${tot:.2f} per $1,000; town ${town:.2f}, local school ${loc:.2f}, state education ${st:.2f}, county ${co:.2f}"
    trows+=f'<div class="trow"><span class="y">{y}</span><div class="ttrack" role="img" aria-label="{E(al)}">{segs}</div><span class="tot">${tot:.2f}</span></div>'
TAXCHART=(f'<div class="taxchart">{trows}<div class="axis" aria-hidden="true"><span></span><div class="ticks"><span>$0</span><span>$10</span><span>$20</span><span>$30</span></div><span></span></div>'
  '<ul class="keyrow">'+"".join(f'<li><i style="--sc:{c}"></i>{n}</li>' for n,c in COMP)+'</ul></div>')
taxrows="".join(f'<tr><th scope="row">{y}</th>'+"".join(f'<td class="num">${v:.2f}</td>' for v in vals)+f'<td class="num"><strong>${sum(vals):.2f}</strong></td></tr>' for y,vals in TAX.items())
TAXTABLE=('<details class="tabledetails"><summary>Show the data table</summary><div class="tablewrap"><table class="data"><caption class="sr">Rindge tax rate per $1,000 by component, 2020-2025</caption>'
 '<thead><tr><th scope="col">Year</th><th scope="col" class="num">Town</th><th scope="col" class="num">Local school</th><th scope="col" class="num">State ed.</th><th scope="col" class="num">County</th><th scope="col" class="num">Total</th></tr></thead>'
 f'<tbody>{taxrows}</tbody></table></div></details>')
SH25 = {n:round(v/13.79*100,1) for n,v in zip(["Town","Local school","State education","County"],TAX[2025])}

# ---------------- topics ----------------
T=[]
T.append(("🏡","var(--cc)","Elderly exemption: current limits and how changes are made", f'''
<p class="callout">Summary, not legal advice. Read the statutes and the town's figures at the linked sources, and confirm with the Town Clerk or Assessing Office.</p>
<div class="tablewrap"><table class="data"><caption>Current Rindge elderly exemption (2025 Annual Report, MS-1 Elderly Exemption Report) {badge("official","conf")}</caption>
<thead><tr><th scope="col">Age</th><th scope="col" class="num">Exemption from assessed value</th><th scope="col" class="num">Recipients</th><th scope="col" class="num">Total granted</th></tr></thead><tbody>
<tr><th scope="row">65–74</th><td class="num">$100,000</td><td class="num">20</td><td class="num">$1,876,600</td></tr>
<tr><th scope="row">75–79</th><td class="num">$140,000</td><td class="num">13</td><td class="num">$1,726,500</td></tr>
<tr><th scope="row">80+</th><td class="num">$200,000</td><td class="num">19</td><td class="num">$2,956,000</td></tr>
<tr><th scope="row">Total</th><td></td><td class="num"><strong>52</strong></td><td class="num"><strong>$6,559,100</strong></td></tr></tbody></table></div>
<ul class="facts">
{fact("Income limits: $35,000 single, $49,000 married. Asset limits: $150,000 single, $150,000 married. The disabled exemption uses the same limits.","official","conf")}
{fact("The deadline to file for exemptions (elderly, disabled and others) was April 15, 2026, per the town calendar in the Annual Report.","official")}
{fact("These income limits were set by a March 2012 petition (Art 20, passed 615-492; digits read from a scan), which raised them from $25,000 single and $35,000 married.","scan")}
{fact("The 2025 report prints the married income limit as $49,000; the 2020 report printed $50,000. Ask the Assessing Office which figure is current.","official","unconf")}
{fact("March 2021, Art 19: the Deliberative Session amended a proposal to lower the limits into a committee to study it (18-6). The 748-376 vote was on that study article, and the exemption did not change. The annual report prints the original wording.","text")}
{fact("March 2022, Art 11: a petition to lower the limits failed 395-601.","official")}
{fact("Recipients by year (MS-1 reports): 91 (2020), 92 (2021), 89 (2022), 88 (2023), 44 (2024) and 52 (2025). The drop followed the 2024 assessor review. Assessed value exempted was $11.07M in 2020 and $6.56M in 2025.","official")}
{fact("The 2026 warrant had no elderly-exemption article. No elderly or disabled exemption discussion was found in the 2026 agendas and minutes reviewed (175 documents) or in the Select Board meetings of Sept 9 to Oct 7.","official")}
{fact("The only related 2026 article was the veterans' disability tax credit increase to $4,500 (Article 12 on the final warrant; numbered Article 11 in the Jan 7 draft). It passed, per press reports.","official","press")}
</ul>
<h4>How exemptions are set under state law</h4>
<ul class="facts">
{fact("RSA 72:39-b: towns set separate exemption amounts for ages 65–74, 75–79 and 80+. Minimums: income limits of at least $13,400 single / $20,400 married; asset limits of at least $35,000 (excluding the residence); each exemption at least $5,000.","statute")}
{fact("RSA 72:39-a: \"net income from all sources\"; three consecutive years of NH residency before April 1; assets exclude the residence and up to the greater of 2 acres or the minimum lot size.","statute")}
{fact("RSA 72:27-a: adopting or changing an exemption requires a town meeting vote, with the article placed on the warrant by the Select Board or by voter petition (RSA 39:3). The vote must state the exemption's provisions and amounts.","statute")}
</ul>
<h4>Petitioned warrant articles in general</h4>
<ul class="facts">
{fact("RSA 39:3: a petitioned article needs the signatures of 25 registered voters or 2% of registered voters, whichever is less (never fewer than 10). The Select Board may make only minor textual changes.","statute")}
{fact("Rindge is an SB2 town. Under RSA 40:13 II-a, petitions are due the second Tuesday in January: Tue Jan 12, 2027 (the preceding Friday, Jan 8, for bond articles).","statutory")}
{fact("At the Deliberative Session, articles may be amended but not to eliminate their subject (RSA 40:13 IV(c)).","statute")}
</ul>'''))
T.append(("🗺️","var(--pb)","March 2027 zoning: wetlands setback, back lots, frontage, condominiums, Class VI roads", f'''
<p class="callout">As of Oct 9, 2026, no amendment text or hearing notice has been posted. The Oct 6 Planning Board agenda lists "Possible Ordinance changes for March 2027 warrant" {badge("agenda")}. Which amendments will go forward is not known.</p>
<h4>Wetlands septic setback: 100 ft to 75 ft (under discussion)</h4>
<ul class="facts">
{fact("Current rule (Wetlands Conservation District Ordinance, amended March 28, 2023): no septic tank or effluent disposal area for a new or expanded building within 100 ft of surface waters or vegetated wetlands; piping 50 ft. The 75 ft figure matches the State standard.","official")}
{fact("June 2 Planning Board: a Zoning Subcommittee member proposed meeting the Conservation Commission about changing the 100 ft setback.","official")}
{fact("June 8 Conservation Commission: concerns raised; under the current rule, builders can seek a ZBA variance below 100 ft. No vote.","official")}
{fact("July 23 Conservation Commission: $2,500 from the Conservation Fund for LEC Environmental Consultants to review the proposal, 5-0-1.","official",v=True)}
{fact("Aug 10 Conservation Commission: report expected by 8/21, with a summary to the Select Board targeted for 9/1. No Commission vote or position on 75 ft appears in posted minutes.","official")}
{fact("An automated meeting summary says the Conservation Commission opposes the change and that a December hearing is planned. Neither is confirmed by an official record.","auto")}
{fact("No article changing the setback from 100 ft to 75 ft has appeared on any Rindge ballot in the annual reports read (2011–2025).","official")}
</ul>
<h4>Residential interior (back) lots</h4>
<ul class="facts">
{fact("The March 2025 zoning ordinance has no interior-lot or flag-lot provision.","official")}
{fact("A subcommittee met March 16 and April 6. Ideas reported to the Planning Board on March 17: 300 ft frontage, no access across wetlands, owner occupancy of one lot. A draft was handed out April 7 and presented to the Conservation Commission June 8. No wording has been posted. The March 8, 2016 back-lot article failed 439-774, so a 2027 article would be a repeat attempt.","official")}
</ul>
<h4>Frontage, condominiums, private and Class VI roads</h4>
<ul class="facts">
{fact("Aug 4 Planning Board: listed as items to address. Not confirmed as warrant articles.","official","unconf")}
{fact("The current minimum frontage is 250 ft, on a town- or state-maintained public right of way (or a Planning Board-approved subdivision) \"to which the lot has legal right of access.\"","official")}
{fact("Frontage was the issue in five 2026 ZBA cases (2026-01, -06, -08, -09, -12).","draft")}
</ul>
<h4>Process and dates</h4>
<ul class="facts">
{fact("Citizen zoning petitions: accepted Nov 9 to Dec 9, 2026 (RSA 675:4).","derived")}
{fact("Planning Board hearings must be publicly noticed (RSA 675:7). Final hearing by Jan 25, 2027; the official copy goes to the Town Clerk by Feb 2, 2027.","derived")}
{fact("2025 precedent: the phasing-table amendment failed 757-805; the other zoning amendments passed.","official")}
</ul>'''))
T.append(("💰","var(--bac)","Budget, revaluation and capital reserves", f'''
<div class="compare" role="group" aria-label="2026 operating budget figures">
 <div><div class="big">$5.81M</div><div class="note">Proposed, as amended Jan 31</div></div><div aria-hidden="true">vs</div>
 <div><div class="big">$5,654,177</div><div class="note">Default budget now in effect</div></div></div>
<ul class="facts">
{fact("Select Board proposed $5,670,000 for 2026 (Jan 7, 3-0).","official",v=True)}
{fact("Deliberative Session (Jan 31): +$40,000 for ambulance (unanimous) and +$100,000 for police staffing (85-50, secret ballot), for $5.81M.","press")}
{fact("March 10: the budget failed 707-824, so the default budget applies. The official warrant gives the default as $5,654,177; press reports gave $5.64M and $5.7M.","press","official")}
{fact("2025 precedent: the 2025 operating budget ($5,625,278) failed 783-850, and the $5,487,882 default applied.","official")}
</ul>
<h4>Revaluation</h4>
<ul class="facts">
{fact("March 11, 2025, Article 15: $25,000 to the Revaluation Capital Reserve Fund for the 2025 revaluation. Passed 872-736.","official")}
{fact("The Jan 7, 2026 draft warrant included another $25,000 Revaluation CRF article. It was pulled on Jan 21: \"The revaluation article was taken off the warrant as requested.\"","official")}
{fact("The 2025 revaluation raised residential values an average of 89.6%. The tax rate fell from $25.31 to $13.79 because assessed values rose; the town advises that bills may stay the same or decrease only if a property's value rose less than about 89.6%.","official")}
</ul>
<h4>Capital items voted in 2026</h4>
<ul class="facts">
{fact("Capital reserve and trust fund articles passed March 10, including Highway CRF $185,000 and Fire CRF $125,000 (see the Election section).","press","official")}
{fact("Aug 12: brush truck purchase from the Fire Department CRF, $162,626, 2-1. June 3: police cruiser, $64,963.50, 2-1. May 20: paving bid at $103.45/ton, 2-0-1.","official",v=True)}
{fact("Highway garage bond: unconfirmed, automated-only. It appears only in an automated summary of a fall budget meeting; no official agenda, minutes or article has been found. Bond-article petitions would be due Fri Jan 8, 2027.","auto","unconf")}
{fact("Budget Advisory Committee: no 2026 minutes have been posted (agendas for July 22 and Aug 19 only).","gap")}
</ul>'''))
T.append(("🏘️","var(--zba)","Subdivisions: Dolly Lane and Forristall Road", f'''
<h4>Dolly Lane: Halliday Trust 5-lot major subdivision (Map 3 Lot 8-5-1)</h4>
<ul class="facts">
{fact("Jan 6: conceptual consultation before the Planning Board.","official")}
{fact("July 7: application accepted as complete (7-0-0) and continued.","official",v=True)}
{fact("Aug 4: continued to Sept 1 (6-0-0). Issues raised: waivers, drainage, maintenance agreement, fire-apparatus road width; possible site walk.","official",v=True)}
{fact("Sept 1 and Oct 6 agendas list the continued hearing. Minutes not yet approved; outcome not verified.","agenda")}
</ul>
<h4>668 Forristall Road (Map 2 Lot 61-2)</h4>
<ul class="facts">
{fact("July 7 and Aug 4: the related minor subdivision was continued by the Planning Board.","official")}
{fact("Sept 22 ZBA, Case 2026-12: frontage variance (85.3 ft on Forristall Rd) approved 4-1.","draft",v=True)}
{fact("Oct 7 Select Board: voted 3-0 to request a ZBA rehearing on the variance.","audio")}
{fact("Oct 12 Conservation Commission agenda: notice of the minor subdivision.","agenda")}
</ul>
<h4>Other large 2026 approvals</h4>
<ul class="facts">
{fact("Boardwalk in Rindge Realty (Map 4 Lot 3-1, Route 119): ZBA special exceptions (April 28), Planning Board major subdivision approved 6-0-0 with 12 conditions (Aug 4).","official","draft",v=True)}
{fact("\"Heidi's Way\": Planning Board approval 7-0-0 with 10 conditions (May 5); ZBA approval with conditions 5-0 (July 28).","official","draft",v=True)}
</ul>'''))
T.append(("🚑","var(--sb)","Ambulance service and the Peterborough contract", f'''
<ul class="facts">
{fact("January: the Select Board discussed a $27,000 disputed invoice with Jaffrey-Rindge Memorial Ambulance (JRMA).","official")}
{fact("Late January: the town announced a resolution with JRMA for the coming year; the Deliberative Session added $40,000 to reach JRMA's requested $125,000.","press")}
{fact("Feb 25: $13,000 withdrawn from the Ambulance Expendable Trust Fund, 3-0.","official",v=True)}
{fact("March 10: Article 6, $40,000 to the Ambulance Service ETF, passed 1,307-230.","press")}
{fact("Sept 9 agenda: \"Review of ambulance services contracts.\"","agenda")}
{fact("Sept 9: the Select Board voted 2-0-1 to end the JRMA arrangement and contract with Peterborough Fire & Rescue from Jan 1, 2027, at about $280,217 a year. The five-year contract is subject to voter approval.","press")}
</ul>
<h4>Peterborough contract cost</h4>
<div class="compare" role="group" aria-label="Approximate Peterborough contract cost">
 <div><div class="big">$280,217</div><div class="note">per year, years 1–2 (press)</div></div><div aria-hidden="true">→</div>
 <div><div class="big">~$370K</div><div class="note">estimated, year 3 (meeting audio)</div></div></div>
<ul class="facts">
{fact("Sept 9 (meeting audio): the Fire Chief recommended Peterborough and estimated year 3 at about $370,000. Whether it appears as a March 2027 warrant article is not confirmed.","audio","unconf")}
{fact("Oct 7: the Fire Chief said no contract has been signed yet.","audio")}
</ul>'''))
T.append(("🏫","var(--school)","School district (Jaffrey-Rindge Cooperative School District)", f'''
<ul class="facts">
{fact("The school district is separate from the town government. District agendas and minutes were not reviewed for this site.","gap")}
{fact("Local school is the largest part of the tax rate: $8.36 of $13.79 in 2025 (60.6%).","official")}
{fact("March 2026: per Select Board minutes, the school district budget went to default in Rindge by about 70 votes (it passed in Jaffrey).","official")}
{fact("The Nov 3, 2026 ballot reportedly includes a question on the HB 1300 school property-tax cap; press coverage (Oct 6) discussed Conant CTE budget concerns.","press")}
{fact("Automated summaries of Sept 14 and Oct 5 board meetings mention van purchases, CTE transportation costs and an HB 1300 briefing. Unconfirmed.","auto")}
</ul>'''))
T.append(("🏛️","var(--town)","Other Select Board business", f'''
<ul class="facts">
{fact("Feb 25: 13 solar exemptions approved (RSA 72:62), 3-0.","official",v=True)}
{fact("2026 warrant: farm structure exemption (RSA 79-F, Article 13) and Land Use Change Tax share to the Conservation Fund (Article 14, amended from 20% to 99%) passed, per press reports.","official","press")}
{fact("July 15: no-thru-truck signs on Old Cathedral/Fitzgerald and Drag Hill/Woodbound, 3-0.","official",v=True)}
{fact("Sept 9: BS&A financial software renewal, about $58,820, 3-0.","audio")}
{fact("Oct 7: the town will replace Town Hall Streams with its own camera and an official town YouTube channel; the Executive Secretary position returns to full-time; the Police Chief job description was tabled.","audio")}
{fact("Select Board: Chair Bob Hamilton, Vice Chair Tom Coneys, Larry Cleveland.","official")}
</ul>'''))
TOPICS="".join(f'<details class="card topic" style="--c:{c}"><summary><span class="ico" aria-hidden="true">{i}</span><h3 class="sum-h">{E(t)}</h3><svg class="i chev" aria-hidden="true" focusable="false"><use href="#i-chev"/></svg></summary><div class="body">{b}</div></details>' for i,c,t,b in T)

CONFLICTS=[
 ("Forristall Rd variance (Case 2026-12)","The ZBA's Sept 22 draft minutes show the variance granted 4-1. On Oct 7 the Select Board voted 3-0 to request a rehearing (from meeting audio; unofficial). Neither the ZBA nor the Select Board has posted a record of the request yet."),
 ("Default budget amount","The official warrant gives $5,654,177. The Ledger-Transcript reported $5.64M (and $5.65M in January); the Keene Sentinel reported $5.7M. This site uses the warrant figure."),
 ("Draft vs. final 2026 warrant","The Jan 7 draft had a $25,000 Revaluation CRF (pulled Jan 21), a $150,000 Highway CRF (the final article was $185,000), a Land Use Change Tax share of 20% (amended to 99% at the Deliberative Session), and different article numbers (the veterans' credit was Art. 11 in the draft and Art. 12 on the final warrant)."),
 ("Deliberative Session timing","The Town Clerk's elections page describes the session as typically the first Saturday of February, but the 2026 session was Sat Jan 31, the earliest legal date. The 2027 date (between Jan 30 and Feb 6) has not been posted."),
 ("Petition deadline","The general RSA 39:3 \"fifth Tuesday\" rule would give Feb 2, 2027, but SB2 towns follow RSA 40:13: the second Tuesday in January (Jan 12, 2027). The town has not posted this date."),
 ("Election results source","The town's results page (news item T2_R44) returned 404 on Oct 9. The Ledger-Transcript and Keene Sentinel report the same tallies; the Sentinel lists the budget as 824-707 (no-yes)."),
 ("Conservation Commission position on 75 ft","\"Opposes\" appears only in an automated summary. Official minutes show concerns and a consultant review, but no vote or position."),
 ("2023 and 2024 budget tallies","The 2023 and 2024 annual reports both print 497-256 for the operating budget, and 2024 Articles 5 and 9 (zoning Amendments 4 and 8) both print 666-237. These tallies are withheld here until the Town Clerk confirms them."),
 ("2018 Article 13 (250th Anniversary trust fund)","Unresolved. The typed minutes show a 715-715 tie (a tie fails), but a handwritten recount note on the ballot page reads 711-707. Later records show the fund existed."),
 ("Elderly married income limit","The 2025 MS-1 report prints $49,000 (the figure set by the 2012 petition); the 2020 MS-1 printed $50,000. Single ($35,000) and asset ($150,000) limits match."),
 ("2021 elderly exemption article","The 2021 report prints the original Article 19 wording (lowering the limits). The Deliberative Session had amended it into a study committee, and the 748-376 vote was on the study article."),
 ("2023 zoning vote date","The 2023 report gives March 14, 2023; the Wetlands Ordinance cover and the amendment list say March 28, 2023."),
 ("2016 Deliberative Session date","The 2016 report (scan) says Sat Jan 30, 2016; an unofficial copy of the minutes says Sat Feb 6, 2016."),
 ("2025 default budget","Select Board minutes and the 2025 report give $5,487,882; the Ledger-Transcript reported $4.49M. The Select Board later found errors and filed an amended default (Nov 12, 2025)."),
 ("2025 revaluation increase","The town's reassessment page gives an average residential increase of 89.6%; Select Board minutes cite about 96.7%. They may measure different things."),
]
GAPS=[
 "Select Board minutes not posted: Apr 15, Apr 22, May 6, Aug 26, Sept 9, Sept 23, Oct 7. The Mar 25 minutes link does not open a PDF.",
 "Planning Board minutes for Sept 1 and Oct 6 not yet approved; no subcommittee minutes after Apr 6. No recording of the Oct 6 meeting was found.",
 "Conservation Commission minutes for Aug 27 and Sept 24 not posted; Sept 24 and Oct 12 outcomes unknown. The LEC review report itself was not found.",
 "Budget Advisory Committee: no 2026 minutes posted. A joint Select Board/BAC FY28 budget meeting (Sept 22 or 28; sources disagree) has no official agenda or minutes, and its recording was not reviewed.",
 "Non-public sessions are not recorded or summarized.",
 "School district: agendas, minutes, enrollment and budget figures not reviewed.",
 "No March 2027 zoning amendment text or hearing notice posted.",
 "No Rindge-posted 2027 election calendar, petition deadline or Deliberative Session date.",
 "The town's official 2026 election results page returned 404 on Oct 9, so election tallies here are press-reported. Tallies for Articles 12-14 were not found.",
 "Several approved ZBA minutes are image scans; the text of the corresponding draft minutes was used. Case 2026-05 was not located.",
 "Sept 9, Sept 23 and Oct 7 Select Board items come from machine speech-to-text of the meeting audio; names, amounts and outcomes are approximate until minutes are posted.",
 "The Wetlands Conservation District Ordinance file is dated 2023; later amendments were not confirmed.",
 "The town ZBA index also lists 2024-2025 documents with ambiguous dates; only 2026-folder documents are shown here.",
 "The town's online agendas and minutes start in Sept 2024. Older minutes need a records request to the Executive Secretary or Town Administrator, so any \"first found\" date before Sept 2024 comes from annual reports or press and is an upper bound.",
 "Annual reports for 2011–2014, 2016 and 2021 are scans. Tallies read from them are marked \"scan, verify against PDF\". 2018 zoning tallies are cropped in the scan, and illegible digits are not shown.",
 "March 2026 results are not in any annual report yet; the 2026 figures on this site are press-reported.",
 "Turnout for 2021–2026 and elderly exemption totals for 2016 and 2021–2024 were not found.",
]
CONF_HTML="".join(f'<div class="gapitem"><span class="bdg b-auto">Conflict</span><div><strong>{E(a)}.</strong> {E(b)}</div></div>' for a,b in CONFLICTS)
GAP_HTML="".join(f'<div class="gapitem"><span class="bdg b-gap">Gap</span><div>{E(g)}</div></div>' for g in GAPS)

SRC={
 "Official: Town of Rindge":[
  ("Select Board agendas & minutes","https://www.rindgenh.org/boards_commission/board_of_selectmen/agendas_minutes.php"),
  ("Planning Board agendas & minutes","https://www.rindgenh.org/boards_commission/planning_board/agendas_minutes.php"),
  ("Zoning Board of Adjustment agendas & minutes","https://www.rindgenh.org/boards_commission/zoning_board_of_adjustment/agendas_minutes.php"),
  ("Conservation Commission agendas & minutes","https://www.rindgenh.org/boards_commission/conservation_commission/agendas_minutes.php"),
  ("Budget Advisory Committee agendas & minutes","https://www.rindgenh.org/boards_commission/budget_advisory_committee/agendas_minutes.php"),
  ("2025 Annual Report (2026 warrant, 2025 results, tax-rate history, exemption report)","https://www.rindgenh.org/Documents/How%20Do%20I/Town%20Reports/0%202025%20Annual%20Report%20for%20the%20Town%20of%20Rindge.pdf"),
  ("Tax Collector: 2025 and 2024 tax rates","https://www.rindgenh.gov/departments/tax_collector/index.php"),
  ("Calculating Tax Impact for 2025 (revaluation, +89.6%)","https://rindgenh.gov/news_detail_T2_R16.php"),
  ("2025 Reassessment page","https://www.rindgenh.gov/departments/assessing/2025_reassessment.php"),
  ("Town Clerk: Local Elections (SB2 schedule)","https://rindgenh.gov/departments/town_clerk/elections-draft/local_elections.php"),
  ("Zoning Ordinances index","https://www.rindgenh.org/boards_commission/planning_board/zoning_ordinances.php"),
  ("Zoning Ordinance, amended March 11, 2025","https://www.rindgenh.org/Documents/Boards%20Commission/Planning%20Board/Zoning%20Ordinances/Zoning_Ordinance%20Amended%20March%2011,%202025.pdf"),
  ("Wetlands Conservation District Ordinance, amended March 28, 2023","https://www.rindgenh.org/Documents/Boards%20Commission/Planning%20Board/Zoning%20Ordinances/wetlands_conservation_district_ordinance_amended_march_28_2023.pdf"),
  ("Select Board meeting video (Town Hall Streams)","https://townhallstreams.com/towns/rindge_nh")],
 "Official: Town annual reports (2011–2025)":[
  ("Town Reports page (all annual reports)","https://www.rindgenh.org/how_do_i/town_reports.php"),
  ("2024 Annual Report","https://www.rindgenh.org/Documents/How%20Do%20I/Town%20Reports/2024%20Annual%20Report-Town%20of%20Rindge-Final%20Print.pdf"),
  ("2021 Annual Report (scan)","https://www.rindgenh.org/Documents/How%20Do%20I/Town%20Reports/102496_rindge_2021_annual_report_rev2_proof_-_optimized.pdf"),
  ("2020 Annual Report","https://www.rindgenh.org/Documents/How%20Do%20I/Town%20Reports/2020%20Annual%20Report.pdf"),
  ("2016 Annual Report (scan)","https://www.rindgenh.org/Documents/How%20Do%20I/Town%20Reports/2016_Annual%20Report%20of%20the%20Town%20of%20Rindge%20New%20Hampshire.pdf"),
  ("Regulations index (Planning Board)","https://www.rindgenh.org/boards_commission/planning_board/regulations.php")],
 "Official: State & federal":[
  ("RSA 72:39-b (elderly exemption)","https://www.gencourt.state.nh.us/rsa/html/V/72/72-39-b.htm"),("RSA 72:39-a (eligibility)","https://www.gencourt.state.nh.us/rsa/html/V/72/72-39-a.htm"),
  ("RSA 72:27-a (adoption procedure)","https://www.gencourt.state.nh.us/rsa/html/V/72/72-27-a.htm"),("RSA 39:3 (petitioned articles)","https://www.gencourt.state.nh.us/rsa/html/III/39/39-3.htm"),
  ("RSA 40:13 (SB2 official ballot)","https://www.gencourt.state.nh.us/rsa/html/III/40/40-13.htm"),
  ("NH DRA 2025 municipal tax rates","https://www.revenue.nh.gov/sites/g/files/ehbemt736/files/documents/2025-municipal-tax-rates.pdf"),
  ("US Census QuickFacts: Rindge town","https://www.census.gov/quickfacts/fact/table/rindgetowncheshirecountynewhampshire/HSG010225"),
  ("NHMA 2027 March SB2 calendar (generic dates)","https://www.nhmunicipal.org/sites/default/files/uploads/calendars/2027-march-sb2-calendar.pdf")],
 "Annual town reports (official; source of the Trends section)":[
  ("2011 Annual Report of the Town of Rindge","https://www.rindgenh.org/Documents/How%20Do%20I/Town%20Reports/2011_Annual%20Report%20of%20the%20Town%20of%20Rindge%20New%20Hampshire.pdf"),
  ("2012 Annual Report of the Town of Rindge","https://www.rindgenh.org/Documents/How%20Do%20I/Town%20Reports/2012_Annual%20Report%20of%20the%20Town%20of%20Rindge%20New%20Hampshire.pdf"),
  ("2013 Annual Report of the Town of Rindge","https://www.rindgenh.org/Documents/How%20Do%20I/Town%20Reports/2013_Annual%20Report%20of%20the%20Town%20of%20Rindge%20New%20Hampshire.pdf"),
  ("2014 Annual Report of the Town of Rindge","https://www.rindgenh.org/Documents/How%20Do%20I/Town%20Reports/2014_Annual%20Report%20of%20the%20Town%20of%20Rindge%20New%20Hampshire.pdf"),
  ("2015 Annual Report of the Town of Rindge","https://www.rindgenh.org/Documents/How%20Do%20I/Town%20Reports/2015_Annual%20report%20of%20the%20Town%20of%20Rindge%20New%20Hampshire.pdf"),
  ("2016 Annual Report of the Town of Rindge","https://www.rindgenh.org/Documents/How%20Do%20I/Town%20Reports/2016_Annual%20Report%20of%20the%20Town%20of%20Rindge%20New%20Hampshire.pdf"),
  ("2017 Annual Report of the Town of Rindge","https://www.rindgenh.org/Documents/How%20Do%20I/Town%20Reports/2017_Annual%20Report%20of%20the%20Town%20of%20Rindge%20New%20Hampshire.pdf"),
  ("2018 Annual Report of the Town of Rindge","https://www.rindgenh.org/Documents/How%20Do%20I/Town%20Reports/2018_Annual%20Report%20of%20the%20Town%20of%20Rindge%20New%20Hampshire.pdf"),
  ("2019 Annual Report of the Town of Rindge","https://www.rindgenh.org/Documents/How%20Do%20I/Town%20Reports/2019_Annual%20Report%20of%20the%20Town%20of%20Rindge%20New%20Hampsire.pdf"),
  ("2020 Annual Report of the Town of Rindge","https://www.rindgenh.org/Documents/How%20Do%20I/Town%20Reports/2020%20Annual%20Report.pdf"),
  ("2021 Annual Report of the Town of Rindge","https://www.rindgenh.org/Documents/How%20Do%20I/Town%20Reports/102496_rindge_2021_annual_report_rev2_proof_-_optimized.pdf"),
  ("2022 Annual Report of the Town of Rindge","https://www.rindgenh.org/Documents/How%20Do%20I/Town%20Reports/Annual%20Report%20of%20the%20Town%20of%20Rindge%20New%20Hampshire%202022.pdf"),
  ("2023 Annual Report of the Town of Rindge","https://www.rindgenh.org/Documents/How%20Do%20I/Town%20Reports/2023%20Town%20Report.pdf"),
  ("2024 Annual Report of the Town of Rindge","https://www.rindgenh.org/Documents/How%20Do%20I/Town%20Reports/2024%20Annual%20Report-Town%20of%20Rindge-Final%20Print.pdf"),
  ("2025 Annual Report of the Town of Rindge","https://www.rindgenh.org/Documents/How%20Do%20I/Town%20Reports/0%202025%20Annual%20Report%20for%20the%20Town%20of%20Rindge.pdf")],
 "Press":[
  ("Ledger-Transcript, 1/31/2026: Deliberative Session","https://ledgertranscript.com/2026/01/31/rindge-voters-approve-budget-increase/"),
  ("Ledger-Transcript, 3/11/2026: election results","https://ledgertranscript.com/2026/03/11/hamilton-retains-select-board/"),
  ("Keene Sentinel, 3/10/2026: election results","https://www.keenesentinel.com/news/local/town-and-school-election-results-march-10/article_6dcaaa56-eace-4031-9f74-812d06b64e12.html"),
  ("Ledger-Transcript, 10/6/2026: Conant CTE budget","https://ledgertranscript.com/2026/10/06/conant-cte-budget-concerns/"),
  ("Ledger-Transcript, 2/9/2022: elderly exemptions","https://ledgertranscript.com/2022/02/09/towns-consider-their-elderly-tax-exemptions-44955643/"),
  ("Ledger-Transcript, 9/14/2026: Rindge ends JRMA contract","https://ledgertranscript.com/2026/09/14/rindge-ends-jrma-contract/"),
  ("Keene Sentinel, 3/11/2026: where zoning changes passed and failed","https://www.keenesentinel.com/news/local/where-key-zoning-changes-passed-and-failed-in-the-monadnock-region-nh/article_a1157345-1244-4711-bf2e-526605ec08e7.html"),
  ("NH Municipal Association: 2026 land use updates (association summary)","https://www.nhmunicipal.org/sites/default/files/uploads/Guidance_Documents/land_use_updates_2026.pdf"),
  ("Keene Sentinel: March 8, 2022 results","https://www.keenesentinel.com/news/local/town-meeting-election-results-march-8/article_5802b31b-120a-599e-a198-146db1467fb6.html")],
 "Automated / unofficial (not relied on for facts)":[
  ("MyTownView: Rindge (AI meeting summaries)","https://mytownview.com/new-hampshire/cheshire/rindge/"),
  ("Citizen Portal: FY28 budget meeting (AI summary)","https://citizenportal.ai/source/10354672/september-22-2026-fy28-budget-advisory-committeespecial-selectboard-meeting")],
}
ndocs=sum(len(e["docs"])+(1 if e["video"] else 0) for e in events)
SRC_HTML="".join(f'<h3>{E(g)}</h3><ul>'+"".join(f'<li><a href="{E(u)}" target="_blank" rel="noopener">{E(t)}<span class="sr"> (opens in new tab)</span></a></li>' for t,u in l)+"</ul>" for g,l in SRC.items())
SRC_HTML+=f'<p class="note">Plus {ndocs} agenda, minutes, notice and video links on individual timeline entries. Select Board audio items come from machine transcription of the Town Hall Streams recordings linked on the Sept 9, Sept 23 and Oct 7 entries.</p>'

V2=v2.render(badge,E,fmt,BOARDS,UPCOMING,TODAY)
R3=v3.render_r3(badge,E)
tpl=open(os.path.join(os.path.dirname(__file__),"template.html")).read()
css=open(os.path.join(os.path.dirname(__file__),"style.css")).read()
js=open(os.path.join(os.path.dirname(__file__),"app.js")).read()
out=tpl
for k,v in dict(CSS=css,JS=js,TIMELINE=TIMELINE,CHIPS=CHIPS,NEV=str(len(events)),UPLIST=UPLIST,CALGRID=CALGRID,ELEC=ELEC,CRFTABLE=CRFTABLE,TAXCHART=TAXCHART,TAXTABLE=TAXTABLE,
    TOPICS=TOPICS,CONF=CONF_HTML,GAPS=GAP_HTML,SOURCES=SRC_HTML,SH_TOWN=str(SH25["Town"]),SH_LOCAL=str(SH25["Local school"]),SH_STATE=str(SH25["State education"]),SH_COUNTY=str(SH25["County"]),**V2,**R3).items():
    out=out.replace("{{"+k+"}}",v)
out,REG,IDX=v3.post(out)
assert "{{" not in out, out[out.find("{{"):out.find("{{")+40]
open(os.path.join(ROOT,"index.html"),"w").write(out)
print("events",len(events),"bytes",len(out),"docs",len(REG),"index",len(IDX))
