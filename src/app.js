(function(){
"use strict";
var d=document, root=d.documentElement, W=window;
var reduce = W.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
function $(s,c){return (c||d).querySelector(s);} function $$(s,c){return Array.prototype.slice.call((c||d).querySelectorAll(s));}
function store(k,v){try{if(v===undefined)return localStorage.getItem(k);localStorage.setItem(k,v);}catch(e){return null;}}
var toastT; function toast(msg){var t=$('#toast');t.textContent=msg;t.classList.add('show');clearTimeout(toastT);toastT=setTimeout(function(){t.classList.remove('show');},2600);}
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
function icon(n){return '<svg class="i" aria-hidden="true" focusable="false"><use href="#i-'+n+'"/></svg>';}

/* ---------- display settings: text size + theme ---------- */
var dBtn=$('#displayBtn'), dPan=$('#displayPanel'), SIZES=[-1,0,1,2,3], SIZEL={'-1':'Small (16 px)','0':'Standard (18 px)','1':'Large (20 px)','2':'Larger (22 px)','3':'Largest (24 px)'};
function curSize(){var z=parseInt(root.getAttribute('data-size')||'0',10);return isNaN(z)?0:z;}
function setSize(z){z=Math.max(-1,Math.min(3,z));if(z===0)root.removeAttribute('data-size');else root.setAttribute('data-size',String(z));store('rindgeSize',String(z));syncDisplay();}
function themePref(){return store('rindgeTheme')||'auto';}
function applyTheme(p){var t=p;if(p==='auto')t=(W.matchMedia&&matchMedia('(prefers-color-scheme: dark)').matches)?'dark':'light';root.setAttribute('data-theme',t);}
function syncDisplay(){var z=curSize();$$('.segb[data-size]').forEach(function(b){var v=b.getAttribute('data-size');b.setAttribute('aria-pressed',(v==='0'&&z===0)?'true':'false');b.disabled=(v==='-1'&&z<=-1)||(v==='1'&&z>=3);});
 $('#sizeV').textContent='Text size: '+SIZEL[String(z)];var p=themePref();$$('.segb[data-theme-set]').forEach(function(b){b.setAttribute('aria-checked',b.getAttribute('data-theme-set')===p?'true':'false');});}
$$('.segb[data-size]').forEach(function(b){b.addEventListener('click',function(){var v=parseInt(b.getAttribute('data-size'),10);setSize(v===0?0:curSize()+v);});});
$$('.segb[data-theme-set]').forEach(function(b){b.addEventListener('click',function(){var p=b.getAttribute('data-theme-set');store('rindgeTheme',p);applyTheme(p);syncDisplay();});
 b.addEventListener('keydown',function(e){if(e.key==='ArrowRight'||e.key==='ArrowLeft'||e.key==='ArrowDown'||e.key==='ArrowUp'){var all=$$('.segb[data-theme-set]'),i=all.indexOf(b),n=all[(i+(e.key==='ArrowRight'||e.key==='ArrowDown'?1:all.length-1))%all.length];n.focus();n.click();e.preventDefault();}});});
if(W.matchMedia){var mq=matchMedia('(prefers-color-scheme: dark)');var onmq=function(){if(themePref()==='auto')applyTheme('auto');};if(mq.addEventListener)mq.addEventListener('change',onmq);}
function openPanel(o){dPan.hidden=!o;dBtn.setAttribute('aria-expanded',o?'true':'false');if(o){syncDisplay();var f=$('.segb',dPan);if(f)f.focus();}}
dBtn.addEventListener('click',function(){openPanel(dPan.hidden);});
d.addEventListener('click',function(e){if(!dPan.hidden&&!dPan.contains(e.target)&&!dBtn.contains(e.target))openPanel(false);});
dPan.addEventListener('keydown',function(e){if(e.key==='Escape'){openPanel(false);dBtn.focus();}});
syncDisplay();

/* ---------- navigation state (rail, top nav, bottom nav) ---------- */
var secGroup={};
$$('.rail nav > ul > li').forEach(function(li){var g=$('a.rg',li).getAttribute('href').slice(1);secGroup[g]=g;$$('ul a',li).forEach(function(a){secGroup[a.getAttribute('href').slice(1)]=g;});});
secGroup.home='home';
function setCurrent(id){var g=secGroup[id];if(!g)return;
 $$('.rail ul ul a').forEach(function(a){if(a.getAttribute('href')==='#'+id)a.setAttribute('aria-current','true');else a.removeAttribute('aria-current');});
 $$('.mainnav a,.bottomnav a').forEach(function(a){if(a.getAttribute('data-group')===g)a.setAttribute('aria-current','true');else a.removeAttribute('aria-current');});}
if('IntersectionObserver' in W){var so=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting)setCurrent(en.target.id);});},{rootMargin:'-35% 0px -60% 0px'});
 $$('section.sec[id], section.home, .groupban').forEach(function(s){so.observe(s);});}
setCurrent('home');

/* ---------- hash targets: open enclosing details, focus, flash ---------- */
function reveal(el){var p=el;while(p&&p!==d.body){if(p.tagName==='DETAILS')p.open=true;p=p.parentElement;}if(el.tagName==='DETAILS')el.open=true;}
function goTo(id,focus){var el=d.getElementById(id);if(!el)return;reveal(el);
 el.scrollIntoView({behavior:reduce?'auto':'smooth',block:'start'});
 if(focus!==false){var f=el.matches('section,.groupban')?($('h2',el)||el):(el.matches('details')?$('summary',el):el);if(!f.hasAttribute('tabindex')&&!/^(A|BUTTON|SUMMARY|INPUT)$/.test(f.tagName))f.setAttribute('tabindex','-1');f.focus({preventScroll:true});}
 if(!reduce&&!el.matches('section,.groupban')){el.classList.remove('flash');void el.offsetWidth;el.classList.add('flash');}}
W.addEventListener('hashchange',function(){var h=location.hash.slice(1);if(h)goTo(decodeURIComponent(h));});
if(location.hash.length>1){var h0=decodeURIComponent(location.hash.slice(1));var t0=d.getElementById(h0);if(t0){reveal(t0);setTimeout(function(){goTo(h0,false);},60);}}
d.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[href^="#"]');if(!a||e.defaultPrevented)return;var id=decodeURIComponent(a.getAttribute('href').slice(1));if(!id)return;var el=d.getElementById(id);if(!el)return;
 e.preventDefault();if(location.hash!=='#'+id)history.pushState(null,'','#'+id);goTo(id);});

/* ---------- share links ---------- */
$$('.sharebtn').forEach(function(b){b.addEventListener('click',function(){var id=b.getAttribute('data-share'),url=location.href.split('#')[0]+'#'+id,title=(($('#'+id+' h2')||{}).textContent||'Rindge Town Guide');
 if(navigator.share&&W.matchMedia&&matchMedia('(pointer: coarse)').matches){navigator.share({title:title,url:url}).catch(function(){});return;}
 var done=function(){toast('Link copied: '+title);};
 if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(url).then(done,function(){fallbackCopy(url);done();});}else{fallbackCopy(url);done();}});});
function fallbackCopy(t){var x=d.createElement('textarea');x.value=t;x.setAttribute('readonly','');x.style.position='fixed';x.style.opacity='0';d.body.appendChild(x);x.select();try{d.execCommand('copy');}catch(e){}d.body.removeChild(x);}

/* ---------- timeline filters ---------- */
var chips=$$('.chip[data-b]'), boards={};
chips.forEach(function(c){if(c.dataset.b!=='__all')boards[c.dataset.b]=true;});
var items=$$('#tl .ev'), months=$$('#tl .month'), q=$('#q'), srcSel=$('#srcSel'), minSel=$('#minSel'), count=$('#count'), empty=$('#empty');
var total=items.length;
function allOn(){for(var k in boards)if(!boards[k])return false;return true;}
function apply(){
 var qs=(q.value||'').trim().toLowerCase(), s=srcSel.value, m=minSel.value, shown=0;
 items.forEach(function(it){
  var src=' '+it.dataset.src+' ', ok=boards[it.dataset.board];
  if(ok&&s==='official')ok=it.dataset.base==='official';
  if(ok&&s==='press')ok=/ press /.test(src);
  if(ok&&s==='unofficial')ok=/ (audio|auto) /.test(src);
  if(ok&&m!=='all')ok=it.dataset.min===m;
  if(ok&&qs)ok=it.dataset.q.indexOf(qs)>-1;
  it.hidden=!ok; if(ok)shown++;
 });
 months.forEach(function(mo){var n=mo.nextElementSibling,vis=false;while(n&&!n.classList.contains('month')){if(!n.hidden){vis=true;break;}n=n.nextElementSibling;}mo.hidden=!vis;});
 empty.hidden=shown>0;
 count.textContent=shown===total?('Showing all '+total+' entries'):('Showing '+shown+' of '+total+' entries');
}
chips.forEach(function(c){c.addEventListener('click',function(){
 var k=c.dataset.b;
 if(k==='__all'){var on=!allOn();for(var b in boards)boards[b]=on;} else boards[k]=!boards[k];
 chips.forEach(function(x){var kk=x.dataset.b;x.setAttribute('aria-pressed',(kk==='__all'?allOn():boards[kk])?'true':'false');});
 apply();
});});
var tmr; q.addEventListener('input',function(){clearTimeout(tmr);tmr=setTimeout(apply,120);});
srcSel.addEventListener('change',apply); minSel.addEventListener('change',apply);

/* ---------- law filter ---------- */
var lchips=$$('.chip[data-lv]'), laws=$$('#lawlist .law'), lgrps=$$('#lawlist .lawgrp'), lq=$('#lq'), lcount=$('#lcount'), lempty=$('#lempty'), lv='all';
function lapply(){var qs=(lq.value||'').trim().toLowerCase(),n=0;
 laws.forEach(function(x){var ok=(lv==='all'||x.dataset.lv===lv)&&(!qs||x.dataset.q.indexOf(qs)>-1);x.hidden=!ok;if(ok)n++;});
 lgrps.forEach(function(g){g.hidden=!$$('.law',g).some(function(x){return !x.hidden;});});
 lempty.hidden=n>0;lcount.textContent=n===laws.length?('Showing all '+n+' entries'):('Showing '+n+' of '+laws.length+' entries');}
lchips.forEach(function(c){c.addEventListener('click',function(){lv=c.dataset.lv;lchips.forEach(function(x){x.setAttribute('aria-pressed',x===c?'true':'false');});lapply();});});
var ltm; if(lq)lq.addEventListener('input',function(){clearTimeout(ltm);ltm=setTimeout(lapply,120);});

/* ---------- directory filter ---------- */
var dq=$('#dq'), dirs=$$('.dir'), dcount=$('#dcount'), dempty=$('#dempty');
function dapply(){var qs=(dq.value||'').trim().toLowerCase().split(/\s+/).filter(Boolean),n=0;dirs.forEach(function(x){var ok=qs.every(function(w){return x.dataset.q.indexOf(w)>-1;});x.hidden=!ok;if(ok)n++;});
 dempty.hidden=n>0;dcount.textContent=n===dirs.length?('Showing all '+n+' offices and boards'):('Showing '+n+' of '+dirs.length);}
if(dq){dq.addEventListener('input',dapply);dapply();}

/* ---------- document library filter ---------- */
var libq=$('#libq'),libb=$('#libb'),libt=$('#libt'),liby=$('#liby'),librows=$$('#libtable tbody tr'),libcount=$('#libcount'),libempty=$('#libempty');
function libapply(){var qs=(libq.value||'').trim().toLowerCase().split(/\s+/).filter(Boolean),b=libb.value,t=libt.value,y=liby.value,n=0;
 librows.forEach(function(r){var ok=(!b||r.dataset.b===b)&&(!t||r.dataset.t===t)&&(!y||r.dataset.y===y)&&qs.every(function(w){return r.dataset.q.indexOf(w)>-1;});r.hidden=!ok;if(ok)n++;});
 libempty.hidden=n>0;libcount.textContent=n===librows.length?('Showing all '+n+' documents'):('Showing '+n+' of '+librows.length+' documents');}
if(libq){[libq].forEach(function(x){x.addEventListener('input',libapply);});[libb,libt,liby].forEach(function(x){x.addEventListener('change',libapply);});libapply();}

/* ---------- key-date tabs ---------- */
var tabs=$$('.tab'), rows=$$('#ulist .urow');
tabs.forEach(function(t){t.addEventListener('click',function(){
 tabs.forEach(function(x){x.setAttribute('aria-selected',x===t?'true':'false');});
 var f=t.dataset.f; rows.forEach(function(r){r.hidden=!(f==='all'||r.dataset.kind===f);});
});});

/* ---------- document viewer ---------- */
var DOCS={};try{DOCS=JSON.parse($('#docdata').textContent);}catch(e){}
var V=$('#viewer'),vBody=$('#vBody'),vTitle=$('#vTitle'),vKind=$('#vKind'),vSrc=$('#vSrc'),vOrig=$('#vOrig'),vDown=$('#vDown'),vPrev=$('#vPrev'),vNext=$('#vNext'),vFoot=$('#vFoot'),vClose=$('#vClose');
var seq=[],pos=0,lastFocus=null,pushed=false;
var CREDIT='Public record, copied from rindgenh.org on Oct 9, 2026; the original is authoritative.';
var KINDS={pdf:'Town document · copy',word:'Town document · converted copy for viewing',embed:'Outside source',ext:'Outside source',large:'Town document · large scan',missing:'Town document · not available'};
function hostLabel(e){return /rindgenh/.test(e.host||'')?'rindgenh.org':(e.host||'').replace(/^www\./,'');}
function card(h,p,btns){return '<div class="v-card" role="note"><h3>'+icon('info')+esc(h)+'</h3><p>'+p+'</p><p>'+btns+'</p></div>';}
function btn(href,label,ic,primary,dl){return '<a class="vbtn'+(primary?' primary':'')+'" href="'+esc(href)+'"'+(dl?' download':' target="_blank" rel="noopener"')+'>'+icon(ic)+'<span>'+esc(label)+'</span>'+(dl?'':'<span class="sr"> (opens in new tab)</span>')+'</a>';}
function render(){var id=seq[pos],e=DOCS[id];if(!e)return;
 vTitle.textContent=e.title;vKind.textContent=KINDS[e.kind]+(seq.length>1?' · '+(pos+1)+' of '+seq.length:'');
 vSrc.textContent=e.src.replace(/^https?:\/\//,'').replace(/\?t=\d+$/,'');vSrc.href=e.src;
 vOrig.href=e.src;$('span',vOrig).textContent='Open original on '+hostLabel(e);
 var local=e.kind==='pdf'||e.kind==='word';vDown.hidden=!local;if(local){vDown.href=e.file;vDown.setAttribute('download','');}
 vPrev.disabled=pos<=0;vNext.disabled=pos>=seq.length-1;
 var canPdf=navigator.pdfViewerEnabled!==false;
 var html='';
 if(local&&canPdf){html='<iframe title="'+esc(e.title)+'" src="'+esc(e.view)+'#view=FitH"></iframe>';}
 else if(local){html=card('This device cannot show PDFs inside the page','Your browser opens PDF files in their own viewer. Use one of these buttons instead.',btn(e.view,'Open the copy','doc',true)+btn(e.src,'Open original on '+hostLabel(e),'external')+btn(e.file,'Download','download',false,true));}
 else if(e.kind==='embed'&&navigator.onLine!==false){html='<iframe title="'+esc(e.title)+'" src="'+esc(e.src)+'" sandbox="allow-scripts allow-same-origin allow-popups allow-forms" referrerpolicy="no-referrer-when-downgrade"></iframe>';}
 else if(e.kind==='embed'){html=card('You appear to be offline','This outside source needs an internet connection.',btn(e.src,'Open in a new tab','external',true));}
 else if(e.kind==='large'){html=card('Large scan: opens on the town website','This annual report is a very large scanned file, so this guide links to the town\'s copy instead of storing one.',btn(e.src,'Open on rindgenh.org','external',true));}
 else if(e.kind==='missing'){html=card('This document is not available right now','The town website returned "not found" for this link when it was checked on Oct 9, 2026. The file may have moved. Try the board\'s agendas and minutes page, or ask the Town Offices at (603) 899-5181.',btn(e.src,'Try the original link','external',true));}
 else {html=card('Opens in a new tab',esc(e.org||hostLabel(e))+' does not allow its pages to be shown inside other websites, so this one opens in a new browser tab.',btn(e.src,'Open '+hostLabel(e)+' in a new tab','external',true));}
 vBody.innerHTML=html;
 vFoot.innerHTML=local?(esc(CREDIT)+(e.kind==='word'?' This is a PDF rendering of a Word file; Download gives the original Word file.':'')+' Document not showing? <a href="'+esc(e.view)+'" target="_blank" rel="noopener">Open the copy in a new tab</a>.'):(e.kind==='embed'?'Shown from '+esc(hostLabel(e))+'. If it does not load, use "Open original".':'');
}
function openDoc(id,list){if(!DOCS[id])return false;seq=list&&list.length?list:[id];pos=Math.max(0,seq.indexOf(id));lastFocus=d.activeElement;
 V.hidden=false;d.body.classList.add('noscroll');render();vTitle.focus();
 if(!pushed&&!ignorePop){try{history.pushState({viewer:1},'',location.href);pushed=true;}catch(e){}}return true;}
var ignorePop=0;
function closeDoc(fromPop){if(V.hidden)return;V.hidden=true;vBody.innerHTML='';d.body.classList.remove('noscroll');
 if(pushed&&!fromPop){ignorePop++;try{history.back();}catch(e){ignorePop--;}}pushed=false;
 if(lastFocus&&lastFocus.focus)lastFocus.focus();}
W.addEventListener('popstate',function(){if(ignorePop>0){ignorePop--;return;}if(!V.hidden)closeDoc(true);});
vClose.addEventListener('click',function(){closeDoc();});
vPrev.addEventListener('click',function(){if(pos>0){pos--;render();}});
vNext.addEventListener('click',function(){if(pos<seq.length-1){pos++;render();}});
function trap(box,e){var f=$$('a[href]:not([hidden]),button:not([disabled]):not([hidden]),input,iframe,[tabindex="0"]',box).filter(function(x){return x.offsetParent!==null||x.tagName==='IFRAME';});if(!f.length)return;
 var first=f[0],last=f[f.length-1];if(e.shiftKey&&(d.activeElement===first||d.activeElement===vTitle)){last.focus();e.preventDefault();}else if(!e.shiftKey&&d.activeElement===last){first.focus();e.preventDefault();}}
V.addEventListener('keydown',function(e){if(e.key==='Escape'){e.preventDefault();closeDoc();}else if(e.key==='Tab')trap(V,e);
 else if((e.key==='ArrowRight'||e.key==='ArrowLeft')&&e.altKey){(e.key==='ArrowRight'?vNext:vPrev).click();}});
function seqFor(a){var c=a.closest('#libtable tbody')||a.closest('.ev')||a.closest('section')||d.body,ids=[];
 $$('a[data-doc]',c).forEach(function(x){if(x.closest('tr[hidden],.ev[hidden],.law[hidden],.dir[hidden]'))return;var i=x.getAttribute('data-doc');if(ids.indexOf(i)<0)ids.push(i);});return ids;}
d.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[data-doc]');if(!a||e.defaultPrevented||e.button!==0||e.metaKey||e.ctrlKey||e.shiftKey||e.altKey)return;if(V.contains(a))return;
 if(openDoc(a.getAttribute('data-doc'),seqFor(a)))e.preventDefault();});

/* ---------- global search ---------- */
var IDX=[];try{IDX=JSON.parse($('#searchdata').textContent);}catch(e){}
IDX.forEach(function(x){x.n=(x.t+' '+x.s).toLowerCase();x.tl=x.t.toLowerCase();});
var SD=$('#searchDlg'),sdq=$('#sdq'),sdres=$('#sdres'),sdHint=$('#sdHint'),sdLast=null,sel=-1,results=[];
var ORDER=['Section','How do I','Directory','Meeting','Date','Topic','Recurring issue','Law','Glossary','Document'],KIC={'Section':'grid','How do I':'question','Directory':'phone','Meeting':'calendar','Date':'calendar','Topic':'info','Recurring issue':'growth','Law':'scale','Glossary':'book','Document':'doc'};
function hi(t,ws){var s=esc(t);ws.forEach(function(w){if(w.length<2)return;s=s.replace(new RegExp('('+w.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+')','ig'),'<mark>$1</mark>');});return s;}
function runSearch(){var v=sdq.value.trim().toLowerCase(),ws=v.split(/\s+/).filter(Boolean);sdres.innerHTML='';results=[];sel=-1;sdq.removeAttribute('aria-activedescendant');
 if(v.length<2){sdHint.textContent='Type at least 2 letters. Use the arrow keys to move, Enter to open, Esc to close.';return;}
 var hits=IDX.filter(function(x){return ws.every(function(w){return x.n.indexOf(w)>-1;});}).map(function(x){var sc=0;ws.forEach(function(w){if(x.tl.indexOf(w)>-1)sc+=3;if(x.tl.indexOf(w)===0)sc+=2;});return {x:x,sc:sc};});
 hits.sort(function(a,b){return b.sc-a.sc;});
 var groups={};hits.forEach(function(h){(groups[h.x.k]=groups[h.x.k]||[]).push(h.x);});
 var html='',n=0;ORDER.forEach(function(k){var g=groups[k];if(!g)return;html+='<li class="sg" role="presentation">'+esc(k)+(g.length>8?' ('+g.length+')':'')+'</li>';
  g.slice(0,8).forEach(function(x){results.push(x);html+='<li role="option" id="sr'+n+'" aria-selected="false" data-i="'+n+'">'+icon(KIC[k]||'info')+'<span class="st">'+hi(x.t,ws)+'</span><span class="ss">'+hi(x.s,ws)+'</span></li>';n++;});});
 sdres.innerHTML=html;sdHint.textContent=hits.length?(hits.length+' result'+(hits.length===1?'':'s')+(hits.length>n?', showing the best '+n:'')+'.'):'No results. Try a different word, such as "budget", "permit" or "wetlands".';
 if(n)move(0);}
function move(i){var opts=$$('[role=option]',sdres);if(!opts.length)return;sel=(i+opts.length)%opts.length;opts.forEach(function(o,j){o.setAttribute('aria-selected',j===sel?'true':'false');});sdq.setAttribute('aria-activedescendant','sr'+sel);opts[sel].scrollIntoView({block:'nearest'});}
function activate(i){var x=results[i];if(!x)return;closeSearch(false);
 if(x.h.indexOf('doc:')===0){openDoc(x.h.slice(4),[x.h.slice(4)]);}
 else{var id=x.h.slice(1);history.pushState(null,'','#'+id);goTo(id);}}
function openSearch(v){sdLast=d.activeElement;SD.hidden=false;d.body.classList.add('noscroll');sdq.value=v||'';sdq.focus();runSearch();}
function closeSearch(restore){if(SD.hidden)return;SD.hidden=true;d.body.classList.remove('noscroll');if(restore!==false&&sdLast&&sdLast.focus)sdLast.focus();}
var stm;sdq.addEventListener('input',function(){clearTimeout(stm);stm=setTimeout(runSearch,80);});
sdq.addEventListener('keydown',function(e){if(e.key==='ArrowDown'){move(sel+1);e.preventDefault();}else if(e.key==='ArrowUp'){move(sel-1);e.preventDefault();}else if(e.key==='Enter'){if(sel>-1)activate(sel);e.preventDefault();}});
sdres.addEventListener('click',function(e){var o=e.target.closest('[role=option]');if(o)activate(+o.getAttribute('data-i'));});
SD.addEventListener('keydown',function(e){if(e.key==='Escape'){e.preventDefault();closeSearch();}else if(e.key==='Tab')trap(SD,e);});
SD.addEventListener('click',function(e){if(e.target===SD)closeSearch();});
$('#sdClose').addEventListener('click',function(){closeSearch();});
$('#searchBtn').addEventListener('click',function(){openSearch('');});
var hq=$('#homeq');if(hq){hq.addEventListener('input',function(){var v=hq.value;hq.value='';openSearch(v);});hq.addEventListener('keydown',function(e){if(e.key==='Enter'){e.preventDefault();openSearch(hq.value);hq.value='';}});}
if(/Mac|iPhone|iPad/.test(navigator.platform||''))$$('.kbd').forEach(function(k){k.textContent='⌘ K';});
d.addEventListener('keydown',function(e){var k=(e.key||'').toLowerCase();var typing=/^(INPUT|TEXTAREA|SELECT)$/.test((d.activeElement||{}).tagName||'');
 if((e.metaKey||e.ctrlKey)&&k==='k'){e.preventDefault();if(SD.hidden&&V.hidden)openSearch('');else if(!SD.hidden)closeSearch();}
 else if(k==='/'&&!typing&&SD.hidden&&V.hidden){e.preventDefault();openSearch('');}});

/* ---------- charts: animate once when scrolled into view ---------- */
var charts=$$('.chart'), pending=charts.slice();
function revealC(c){if(!c.classList.contains('in'))c.classList.add('in');}
function checkCharts(){if(!pending.length)return;var vh=innerHeight||d.documentElement.clientHeight;
 pending=pending.filter(function(c){var r=c.getBoundingClientRect();if(r.top<vh*0.92&&r.bottom>0){revealC(c);return false;}return true;});}
if(root.classList.contains('anim')){
 if('IntersectionObserver' in W){var io=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){revealC(en.target);io.unobserve(en.target);pending=pending.filter(function(x){return x!==en.target;});}});},{threshold:.2});charts.forEach(function(c){io.observe(c);});}
 addEventListener('scroll',function(){requestAnimationFrame(checkCharts);},{passive:true});
 addEventListener('resize',checkCharts);
 checkCharts();
}else{charts.forEach(revealC);}
var nums=$$('[data-count]');
if(root.classList.contains('anim')){
 var fmt=function(n){return n.toLocaleString('en-US');};
 var co=new IntersectionObserver(function(es){es.forEach(function(en){if(!en.isIntersecting)return;co.unobserve(en.target);
  var el=en.target,end=+el.dataset.count,t0=null,dur=900;
  function step(ts){if(!t0)t0=ts;var p=Math.min(1,(ts-t0)/dur),e=1-Math.pow(1-p,3);el.textContent=fmt(Math.round(end*e));if(p<1)requestAnimationFrame(step);else el.textContent=fmt(end);}
  requestAnimationFrame(step);});},{threshold:.5});
 nums.forEach(function(n){co.observe(n);});
}

/* ---------- progress, back to top ---------- */
var prog=$('#progress'), tt=$('#toTop'), ticking=false;
function onScroll(){ticking=false;var h=d.documentElement.scrollHeight-innerHeight;var p=h>0?Math.min(1,Math.max(0,scrollY/h)):0;prog.style.transform='scaleX('+p+')';tt.classList.toggle('show',scrollY>700);}
addEventListener('scroll',function(){if(!ticking){ticking=true;requestAnimationFrame(onScroll);}},{passive:true});
onScroll();
tt.addEventListener('click',function(){scrollTo({top:0,behavior:reduce?'auto':'smooth'});var m=$('#home-h');if(m){m.setAttribute('tabindex','-1');m.focus({preventScroll:true});}});

/* ---------- print: open everything ---------- */
var opened=[];
addEventListener('beforeprint',function(){charts.forEach(revealC);opened=$$('details:not([open])');opened.forEach(function(x){x.open=true;});});
addEventListener('afterprint',function(){opened.forEach(function(x){x.open=false;});});
W.RindgeGuide={openDoc:openDoc,closeDoc:closeDoc,openSearch:openSearch};
})();
