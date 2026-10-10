# Renders v2 sections. Called from build.py with badge(), E(), fmt(), BOARDS, UPCOMING, TODAY.
from v2data import *
from lawdata import L as LAW, RECENT, DIMS, ZFLOW, PFLOW, ZO

def render(badge, E, fmt, BOARDS, UPCOMING, TODAY):
    out = {}
    pct = lambda a,b: a/(a+b)*100
    def details_table(cap, head, rows):
        h = "".join(f'<th scope="col"{" class=num" if i else ""}>{E(x)}</th>' for i,x in enumerate(head))
        b = "".join("<tr>"+"".join((f'<th scope="row">{c}</th>' if i==0 else f'<td class="num">{c}</td>') for i,c in enumerate(r))+"</tr>" for r in rows)
        return (f'<details class="tabledetails"><summary>Show the data table</summary><div class="tablewrap"><table class="data">'
                f'<caption class="sr">{E(cap)}</caption><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div></details>')
    def mini(code): return badge(code)
    CH = {}
    # ---- budget yes share ----
    rows=""; trs=[]
    for y,yes,no,ok,lab,note in BUDGET:
        if yes is None:
            rows += (f'<div class="hb"><span class="y">{y}</span><div class="track gaptrack" role="img" aria-label="{y}: tally withheld"><span class="gl">Tally withheld</span></div>'
                     f'<span class="v">{badge(lab)}</span></div>')
            trs.append([str(y),"withheld","","",E(note)]); continue
        p=pct(yes,no)
        al=f"{y}: {'passed' if ok else 'failed'} {yes:,} to {no:,}, {p:.1f} percent yes"
        rows += (f'<div class="hb"><span class="y">{y}</span><div class="track mid" role="img" aria-label="{E(al)}"><span class="fill {"f-yes" if ok else "f-no"}" style="--w:{p:.2f}%"></span></div>'
                 f'<span class="v"><b>{yes:,}–{no:,}</b> · {p:.1f}% {"" if ok else "<em class=fl>failed</em>"} {badge(lab)}</span></div>')
        trs.append([str(y),f"{yes:,}",f"{no:,}",f"{p:.1f}%",("Passed" if ok else "Failed")+(". "+E(note) if note else "")])
    CH["budget"]=(f'<div class="card chart wide" id="ch-budget"><h3>Town operating budget: share voting yes, 2011–2026</h3>'
        f'<p class="note" style="margin-top:0">Green = passed, orange = failed (the default budget applied). The dashed line marks 50%. Labels show where each tally comes from.</p>{rows}'
        +details_table("Operating budget votes by year",["Year","Yes","No","Yes %","Result / note"],trs)+'</div>')
    # ---- zoning articles ----
    MX=12; rows=""; trs=[]
    for y,pa,fa,lab,note in ZONING:
        segs=f'<span class="seg" style="--w:{pa/MX*100:.3f}%;--sc:var(--yes)"></span><span class="seg" style="--w:{fa/MX*100:.3f}%;--sc:var(--no)"></span>'
        al=f"{y}: {pa} passed, {fa} failed"
        rows+=(f'<div class="hb"><span class="y">{y}</span><div class="ttrack sm" role="img" aria-label="{E(al)}">{segs}</div>'
               f'<span class="v"><b>{pa}</b> passed{f" · <b>{fa}</b> failed" if fa else ""}{" · none" if pa+fa==0 else ""} {badge(lab)}</span></div>')
        trs.append([str(y),str(pa),str(fa),E(note)])
    CH["zoning"]=(f'<div class="card chart" id="ch-zoning"><h3>Zoning amendments on the March ballot</h3><ul class="keyrow" style="margin-top:0"><li><i style="--sc:var(--yes)"></i>Passed</li><li><i style="--sc:var(--no)"></i>Failed</li></ul>{rows}'
        '<p class="note">Most housekeeping amendments pass with 60–80%. Failures cluster on loosening lot rules (2014), back lots (2016), map changes the Planning Board opposed (2021) and the 2025 phasing table.</p>'
        +details_table("Zoning amendments by year",["Year","Passed","Failed","Note"],trs)+'</div>')
    # ---- turnout ----
    MX=1700; rows=""; trs=[]
    for y,v,lab in TURNOUT:
        if v is None:
            rows+=f'<div class="hb"><span class="y">{y}</span><div class="track gaptrack" role="img" aria-label="{y}: not found"><span class="gl">Not found</span></div><span class="v">{badge("gap")}</span></div>'
            trs.append([str(y),"not found"]); continue
        rows+=(f'<div class="hb"><span class="y">{y}</span><div class="track" role="img" aria-label="{y}: {v:,} ballots"><span class="fill f-a" style="--w:{v/MX*100:.2f}%"></span></div>'
               f'<span class="v"><b>{v:,}</b> {badge(lab)}</span></div>'); trs.append([str(y),f"{v:,}"])
    CH["turnout"]=(f'<div class="card chart" id="ch-turnout"><h3>Ballots cast at the March town election</h3>{rows}'
        '<p class="note">2013 is the number printed as "voters attending second meeting". The 2018–2020 reports print the same checklist size (4,398), possibly carried over. 2023 has an unlabeled "777" on the results sheet, which is not shown. Results PDFs for 2024 and 2026 are scanned ballots.</p>'
        +details_table("Ballots cast",["Year","Ballots"],trs)+'</div>')
    # ---- tax total ----
    MX=30; rows=""; trs=[]
    for y,v,lab in TAXTOT:
        rv = y in REVAL
        rows+=(f'<div class="hb"><span class="y">{y}</span><div class="track" role="img" aria-label="{y}: ${v:.2f} per $1,000{", revaluation year" if rv else ""}"><span class="fill {"f-no" if rv else "f-brand"}" style="--w:{v/MX*100:.2f}%"></span></div>'
               f'<span class="v"><b>${v:.2f}</b>{" <em class=rv>revaluation</em>" if rv else ""} {badge(lab)}</span></div>')
        trs.append([str(y),f"${v:.2f}","yes" if rv else ""])
    CH["tax"]=(f'<div class="card chart" id="ch-tax"><h3>Total tax rate per $1,000 of assessed value, 2010–2025</h3>{rows}'
        '<p class="note">Totals are the sum of the printed town, local school, state education and county rates. In revaluation years (2015, 2020, 2025) assessed values were reset, so the rate per $1,000 dropped. That does not mean bills fell by the same amount. The parts of the rate for 2020–2025 are in the Numbers section.</p>'
        +details_table("Total tax rate by year",["Year","Rate","Revaluation"],trs)+'</div>')
    # ---- elderly ----
    MX=12_000_000; rows=""; trs=[]
    for y,v,n in ELDERLY:
        if v is None:
            rows+=f'<div class="hb"><span class="y">{y}</span><div class="track gaptrack" role="img" aria-label="{y}: value exempted not extracted{f", {n} recipients" if n else ""}"><span class="gl">Value not extracted</span></div><span class="v">{f"<b>{n}</b> people " if n else ""}{badge("official") if n else ""}{badge("gap")}</span></div>'
            trs.append([str(y),"not extracted",str(n or "")]); continue
        rows+=(f'<div class="hb"><span class="y">{y}</span><div class="track" role="img" aria-label="{y}: ${v:,} exempted{f", {n} recipients" if n else ""}"><span class="fill f-cc" style="--w:{v/MX*100:.2f}%"></span></div>'
               f'<span class="v"><b>${v/1e6:.2f}M</b>{f" · <b>{n}</b> people" if n else ""} {badge("official")}</span></div>')
        trs.append([str(y),f"${v:,}",str(n or "")])
    CH["elderly"]=(f'<div class="card chart" id="ch-elderly"><h3>Elderly exemption: assessed value exempted (MS-1 reports)</h3>{rows}'
        '<p class="note">Recipients by year: 91 (2020), 92 (2021), 89 (2022), 88 (2023), 44 (2024) and 52 (2025). The drop followed the 2024 assessor review (the required five-year review, when several owners no longer qualified). The value exempted for 2016 and 2021–2024 was not located in the text; 2016 and 2021 are scanned reports.</p>'
        +details_table("Elderly exemption value",["Year","Value exempted","Recipients"],trs)+'</div>')
    # ---- reval CRF ----
    rows=""; trs=[]
    for y,yes,no,lab,amt in REVALCRF:
        p=pct(yes,no)
        rows+=(f'<div class="hb"><span class="y">{y}</span><div class="track mid" role="img" aria-label="{y}: {yes:,} to {no:,}, {p:.1f} percent yes"><span class="fill f-yes" style="--w:{p:.2f}%"></span></div>'
               f'<span class="v"><b>{yes:,}–{no:,}</b> · {p:.1f}% · {E(amt)} {badge(lab)}</span></div>'); trs.append([str(y),f"{yes:,}",f"{no:,}",f"{p:.1f}%",E(amt)])
    CH["reval"]=(f'<div class="card chart" id="ch-reval"><h3>Revaluation reserve articles: share voting yes</h3>{rows}'
        '<p class="note">Every one passed. The "no" share was highest in 2025 (45.8%). There was no article in 2020, and the 2026 article was pulled from the warrant on Jan 21, 2026.</p>'
        +details_table("Revaluation CRF votes",["Year","Yes","No","Yes %","Amount"],trs)+'</div>')
    # ---- cadence ----
    MX=40; rows=""; trs=[]
    for b,a,c,d in CADENCE:
        n,col=BOARDS[b]
        rows+=f'<div class="grp" style="--c:{col}"><div class="gname">{E(n)}</div>'
        for lab,v in (("2024 (Sep–Dec)",a),("2025",c),("2026 to Oct 12",d)):
            rows+=(f'<div class="hb lab"><span class="y sm">{lab}</span><div class="track" role="img" aria-label="{E(n)} {lab}: {v} dates"><span class="fill f-board" style="--w:{v/MX*100:.2f}%"></span></div>'
                   f'<span class="v"><b>{v}</b></span></div>')
        rows+='</div>'; trs.append([E(n),str(a),str(c),str(d)])
    CH["cadence"]=(f'<div class="card chart" id="ch-cadence"><h3>Meeting dates posted per board {badge("official")}</h3>{rows}'
        '<p class="note">Distinct dates on each board\'s town index page. Some are notices or cancellations. The online index starts in Sept 2024. Earlier counts are only fragments in web archives, so they are lower bounds and are not charted. The Select Board meets most Wednesdays at 6pm; the Planning Board meets the 1st and 3rd Tuesday at 7pm.</p>'
        +details_table("Meeting dates by board",["Board","2024 Sep–Dec","2025","2026 to Oct 12"],trs)+'</div>')
    # ---- caseload ----
    MX=25; rows=""; trs=[]
    for y,p_,z in CASELOAD:
        def tr(v,cls,nm):
            if v is None: return f'<div class="track thin gaptrack" role="img" aria-label="{y} {nm}: not reported"></div>'
            return f'<div class="track thin" role="img" aria-label="{y} {nm}: {v}"><span class="fill {cls}" style="--w:{v/MX*100:.2f}%"></span></div>'
        rows+=(f'<div class="hb"><span class="y">{y}</span><div class="pair">{tr(p_,"f-pb","Planning Board")}{tr(z,"f-zba","ZBA")}</div>'
               f'<span class="v">PB <b>{p_ if p_ is not None else "—"}</b> · ZBA <b>{z if z is not None else "—"}</b></span></div>')
        trs.append([str(y),str(p_ if p_ is not None else "—"),str(z if z is not None else "—")])
    CH["caseload"]=(f'<div class="card chart" id="ch-caseload"><h3>Planning Board applications and ZBA cases per year {badge("official")}</h3>'
        '<ul class="keyrow" style="margin-top:0"><li><i style="--sc:var(--pb)"></i>Planning Board applications reviewed</li><li><i style="--sc:var(--zba)"></i>ZBA cases</li></ul>'
        f'{rows}<p class="note">From each year\'s annual report board sections. 2016 ZBA (10) is derived from the 2017 report\'s wording. 2021 Planning Board (23) is stated in the 2024 report. 2024 Planning Board is 7 per the 2025 report. 2025 Planning Board adds 4 conceptual consultations. A dash means not reported.</p>'
        +details_table("Caseload",["Year","Planning Board","ZBA"],trs)+'</div>')
    # ---- 3/5 notes ----
    tf="".join(f'<li><strong>{E(a)}.</strong> {E(b)} {badge(c)}</li>' for a,b,c in THREEFIFTHS)
    CH["threefifths"]=(f'<div class="card"><h3>Near misses: articles that needed a 3/5 (60%) vote</h3><ul class="facts">{tf}</ul>'
        '<p class="note">Bond and some lease articles need 60% yes. Percentages are computed from the printed tallies.</p></div>')
    # ---- heatmap ----
    head="".join(f'<th scope="col" class="num">{str(y)[2:]}</th>' for y in KWYEARS)
    body=""
    for t,vals in KW:
        cells=""
        for y,v in zip(KWYEARS,vals):
            if v is None: cells+=f'<td class="hm na" title="{y}: scanned report">·</td>'; continue
            i=min(v,10)/10*100
            cells+=f'<td class="hm{" hi" if i>=50 else ""}" style="--i:{i:.0f}%" title="{y}: {v} pages">{v}</td>'
        body+=f'<tr><th scope="row">{E(t)}</th>{cells}</tr>'
    CH["heat"]=(f'<div class="card" id="ch-heat"><h3>How often each issue appears in the annual reports, 2013–2025 {badge("kw")}</h3>'
        '<p class="note" style="margin-top:0">Number of pages in each year\'s town report mentioning the topic (darker = more). This is a rough gauge, not a case count. "·" = scanned report (2016, 2021), not counted. The years run \'13 to \'25.</p>'
        f'<div class="tablewrap"><table class="data heat"><caption class="sr">Annual report pages mentioning each topic, 2013 to 2025</caption><thead><tr><th scope="col">Topic</th>{head}</tr></thead><tbody>{body}</tbody></table></div></div>')
    out["TRENDS"]=(f'<div class="grid g2">{CH["budget"]}</div>'
        f'<div class="grid g2" style="margin-top:16px">{CH["zoning"]}{CH["turnout"]}</div>'
        f'<div class="grid g2" style="margin-top:16px">{CH["tax"]}{CH["elderly"]}</div>'
        f'<div class="grid g2" style="margin-top:16px">{CH["reval"]}{CH["threefifths"]}</div>'
        f'<div class="grid g2" style="margin-top:16px">{CH["caseload"]}{CH["cadence"]}</div>'
        f'<div style="margin-top:16px">{CH["heat"]}</div>')
    # ---- recurring issues ----
    cards=""; nav=""
    for k,ic,col,title,summ,first,latest,evs in ISSUES:
        li="".join(f'<li><span class="mw">{E(w)}</span><span class="mt">{E(t)} {badge(l)}</span></li>' for w,t,l in evs)
        cards+=(f'<article class="card issue" id="iss-{k}" style="--c:{col}"><header><span class="ico" aria-hidden="true">{ic}</span><h3>{E(title)}</h3></header>'
                f'<p>{E(summ)}</p><dl class="fl2"><div><dt>First found</dt><dd>{E(first)}</dd></div><div><dt>Most recent</dt><dd>{E(latest)}</dd></div></dl>'
                f'<ol class="mtl">{li}</ol></article>')
        nav+=f'<a href="#iss-{k}" style="--c:{col}"><span aria-hidden="true">{ic}</span> {E(title)}</a>'
    out["ISSUES"]=f'<nav class="issnav" aria-label="Jump to an issue">{nav}</nav><div class="grid g2 issues">{cards}</div>'
    # ---- law reference ----
    groups={}; order=[]
    for lv,g,t,pl,ri,labs,url in LAW:
        key=(lv,g)
        if key not in groups: groups[key]=[]; order.append(key)
        groups[key].append((t,pl,ri,labs,url))
    LV={"local":("Local","var(--pb)"),"county":("County","var(--bac)"),"state":("State","var(--sb)")}
    html=""
    for lv,g in order:
        n,col=LV[lv]
        items=""
        for t,pl,ri,labs,url in groups[(lv,g)]:
            q=E((n+" "+g+" "+t+" "+pl+" "+ri).lower())
            items+=(f'<li class="law" data-lv="{lv}" data-q="{q}" style="--c:{col}"><div class="lh"><span class="lvl">{n}</span><h4>{E(t)}</h4></div>'
                    f'<p>{E(pl)}</p>{f"<p class=rin><strong>What it means for Rindge:</strong> {E(ri)}</p>" if ri else ""}'
                    f'<p class="lsrc">{badge(*labs)} <a href="{E(url)}" target="_blank" rel="noopener">Source<span class="sr"> for {E(t)} (opens in new tab)</span></a></p></li>')
        html+=f'<div class="lawgrp" data-lv="{lv}"><h3 class="lgh" style="--c:{col}">{n} · {E(g)}</h3><ul class="laws">{items}</ul></div>'
    nlaw=len(LAW)
    cnt={k:sum(1 for x in LAW if x[0]==k) for k in LV}
    dims="".join(f'<tr><th scope="row">{E(a)}</th><td>{E(b)}</td><td>{E(c)}</td><td>{E(d)}</td><td>{E(e)}</td></tr>' for a,b,c,d,e in DIMS)
    out["DIMS"]=(f'<div class="card"><h3>Dimensional table: Zoning Ordinance as amended March 11, 2025 {badge("official")}</h3><div class="tablewrap"><table class="data"><caption class="sr">Minimum frontage, lot size and setbacks by district</caption>'
        '<thead><tr><th scope="col">District (Article)</th><th scope="col">Min. frontage</th><th scope="col">Min. lot area</th><th scope="col">Setback from road</th><th scope="col">Setback from abutter</th></tr></thead>'
        f'<tbody>{dims}</tbody></table></div><p class="note">Also: no building within 50 ft of a water body\'s high-water line (Art. III.G.4); no new septic system within 100 ft of wetlands or surface waters (Wetlands Ordinance §5.B); height limit 45 ft. The ZBA can grant variances, and the Planning Board can modify frontage in the Gateway districts and in PURDs. <a href="{ZO}" target="_blank" rel="noopener">Ordinance PDF<span class="sr"> (opens in new tab)</span></a>. The PDF was not re-issued after the March 2026 ADU vote; follow the separate 2026 ADU Ordinance for ADUs.</p></div>')
    out["LAWS"]=html; out["NLAW"]=str(nlaw)
    out["LAWCHIPS"]=('<button type="button" class="chip" aria-pressed="true" data-lv="all" style="--c:var(--brand2)">All levels <span class="n">('+str(nlaw)+')</span></button>'
        + "".join(f'<button type="button" class="chip" aria-pressed="false" data-lv="{k}" style="--c:{c}"><span class="dot" aria-hidden="true"></span>{n} <span class="n">({cnt[k]})</span></button>' for k,(n,c) in LV.items()))
    rec="".join(f'<tr><th scope="row">{E(a)}</th><td>{E(b)}</td><td>{E(c)} {badge(l)}</td></tr>' for a,b,c,l in RECENT)
    out["RECENT"]=(f'<div class="card"><h3>Recent state law changes (2024–2026)</h3><div class="tablewrap"><table class="data"><caption class="sr">Recent state land-use law changes</caption>'
        f'<thead><tr><th scope="col">Bill</th><th scope="col">What it did</th><th scope="col">Status</th></tr></thead><tbody>{rec}</tbody></table></div>'
        '<p class="note">Bills listed only from association or State summaries were not checked against the statute pages. Bills that did not become law are not listed.</p></div>')
    def flow(steps, title, fid):
        DB=badge("derived","unconf")
        li="".join('<li><span class="sn" aria-hidden="true">'+str(i+1)+'</span><div><strong>'+E(a)+'</strong><p>'+E(b)+'</p>'+(('<p class="fd">'+E(c)+' '+DB+'</p>') if c else '')+'</div></li>' for i,(a,b,c) in enumerate(steps))
        return f'<div class="card flowcard" id="{fid}"><h3>{E(title)}</h3><ol class="flow">{li}</ol></div>'
    out["FLOWS"]=('<div class="grid g2">'+flow(ZFLOW,"How a zoning change becomes law","flow-zoning")+flow(PFLOW,"How a citizen petition works","flow-petition")+'</div>'
        '<p class="note">Dates are computed from state law for a Tue Mar 9, 2027 vote. They are statutory-derived and unconfirmed by the town for 2027, so check them with the Town Clerk.</p>')
    # ---- start here: coming up + glossary ----
    pick={"2026-10-12","2026-10-21","2026-11-09","2026-12-09","2027-01-12","2027-01-30","2027-03-09"}
    STB={"posted":("posted","conf"),"inferred":("inferred","unconf"),"press":("press",),"derived":("derived","unconf"),"statutory":("statutory",)}
    cu=""
    for d,t,b,st,key,end in UPCOMING:
        if d in pick or (d=="2026-11-03" and b=="town"):
            dt=fmt(d,False)
            cu+=(f'<li style="--c:{BOARDS[b][1]}"><span class="cd"><time datetime="{d}">{dt}</time></span><span>{E(t)}</span><span>{badge(*STB[st])}</span></li>')
    out["COMING"]=cu
    out["GLOSS"]="".join(f'<div class="gl-item"><dt>{E(a)}</dt><dd>{E(b)} <span class="cite">{E(c)}</span></dd></div>' for a,b,c in GLOSSARY)
    return out
