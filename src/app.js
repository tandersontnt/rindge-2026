(function(){
"use strict";
var d=document, root=d.documentElement, W=window;
var mqReduce=W.matchMedia?matchMedia('(prefers-reduced-motion: reduce)'):null;
function reduce(){return !!(mqReduce&&mqReduce.matches);}
function $(s,c){return (c||d).querySelector(s);} function $$(s,c){return Array.prototype.slice.call((c||d).querySelectorAll(s));}
function store(k,v){try{if(v===undefined)return localStorage.getItem(k);localStorage.setItem(k,v);}catch(e){return null;}}
var toastT; function toast(msg){var t=$('#toast');t.textContent=msg;t.classList.add('show');clearTimeout(toastT);toastT=setTimeout(function(){t.classList.remove('show');},2600);}
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
function icon(n){return '<svg class="i" aria-hidden="true" focusable="false"><use href="#i-'+n+'"/></svg>';}
function focusables(box){return $$('a[href],button:not([disabled]),input,select,iframe,video,[tabindex="0"]',box).filter(function(x){return x.getAttribute('tabindex')!=='-1'&&!x.closest('[hidden]')&&(x.offsetParent!==null||x.tagName==='IFRAME')&&getComputedStyle(x).visibility!=='hidden';});}
function trap(box,e){var f=focusables(box);if(!f.length)return;var first=f[0],last=f[f.length-1],a=d.activeElement;
 if(e.shiftKey&&(a===first||!box.contains(a)||a===box.querySelector('h2'))){last.focus();e.preventDefault();}
 else if(!e.shiftKey&&(a===last||!box.contains(a))){first.focus();e.preventDefault();}}
/* scroll lock shared by menu, search and viewer */
var locks=0;function lock(on){locks=Math.max(0,locks+(on?1:-1));root.classList.toggle('noscroll',locks>0);d.body.classList.toggle('noscroll',locks>0);}

/* ---------- display settings: text size + appearance ---------- */
var SIZEL={'-1':'Small','0':'Standard','1':'Large','2':'Larger','3':'Largest'};
function curSize(){var z=parseInt(root.getAttribute('data-size')||'0',10);return isNaN(z)?0:z;}
function setSize(z){z=Math.max(-1,Math.min(3,z));if(z===0)root.removeAttribute('data-size');else root.setAttribute('data-size',String(z));store('rindgeSize',String(z));syncDisplay();checkTables();}
function themePref(){return store('rindgeTheme')||'auto';}
function applyTheme(p){if(p==='auto')root.removeAttribute('data-theme');else root.setAttribute('data-theme',p);}
function syncDisplay(){var z=curSize();$$('.segb[data-size]').forEach(function(b){var v=b.getAttribute('data-size');b.setAttribute('aria-pressed',(v==='0'&&z===0)?'true':'false');b.disabled=(v==='-1'&&z<=-1)||(v==='1'&&z>=3);});
 var sv=$('#sizeV');if(sv)sv.textContent='Text size: '+SIZEL[String(z)];var p=themePref();$$('.segb[data-theme-set]').forEach(function(b){b.setAttribute('aria-checked',b.getAttribute('data-theme-set')===p?'true':'false');b.tabIndex=b.getAttribute('data-theme-set')===p?0:-1;});}
$$('.segb[data-size]').forEach(function(b){b.addEventListener('click',function(){var v=parseInt(b.getAttribute('data-size'),10);setSize(v===0?0:curSize()+v);});});
$$('.segb[data-theme-set]').forEach(function(b){b.addEventListener('click',function(){var p=b.getAttribute('data-theme-set');store('rindgeTheme',p);applyTheme(p);syncDisplay();});
 b.addEventListener('keydown',function(e){if(/^Arrow/.test(e.key)){var all=$$('.segb[data-theme-set]'),i=all.indexOf(b),n=all[(i+(e.key==='ArrowRight'||e.key==='ArrowDown'?1:all.length-1))%all.length];n.focus();n.click();e.preventDefault();}});});
applyTheme(themePref());syncDisplay();

/* ---------- menu sheet ---------- */
var M=$('#menu'),mBtn=$('#menuBtn'),mLast=null;
function openMenu(){if(!M.hidden)return;mLast=d.activeElement;M.hidden=false;lock(true);mBtn.setAttribute('aria-expanded','true');syncDisplay();
 var cur=$('.mgroup a[aria-current=true]',M);setTimeout(function(){($('#menuClose')).focus();if(cur)cur.scrollIntoView({block:'center'});},0);}
function closeMenu(restore){if(M.hidden)return;M.hidden=true;lock(false);mBtn.setAttribute('aria-expanded','false');if(restore!==false&&mLast&&mLast.focus)mLast.focus();}
mBtn.addEventListener('click',function(){M.hidden?openMenu():closeMenu();});
$('#menuClose').addEventListener('click',function(){closeMenu();});
M.addEventListener('click',function(e){if(e.target.getAttribute&&e.target.getAttribute('data-close')==='menu')closeMenu();});
M.addEventListener('keydown',function(e){if(e.key==='Escape'){e.preventDefault();e.stopPropagation();closeMenu();}else if(e.key==='Tab')trap(M,e);});
$('#menuSearch').addEventListener('click',function(){closeMenu(false);openSearch('');});

/* ---------- where am I: highlight current group/section in top bar and menu ---------- */
var secGroup={};
$$('.groupban').forEach(function(g){secGroup[g.id]=g.id;$$('.gb-l a',g).forEach(function(a){secGroup[a.getAttribute('href').slice(1)]=g.id;});});
secGroup.home='start-group';
function setCurrent(id){var g=secGroup[id];if(!g)return;
 $$('.mgroup a[data-nav]').forEach(function(a){if(a.getAttribute('data-nav')===id)a.setAttribute('aria-current','true');else a.removeAttribute('aria-current');});
 $$('.toplinks a').forEach(function(a){if(a.getAttribute('data-nav')===g)a.setAttribute('aria-current','true');else a.removeAttribute('aria-current');});}
if('IntersectionObserver' in W){var so=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting)setCurrent(en.target.id);});},{rootMargin:'-30% 0px -65% 0px'});
 $$('section.sec[id], section.home, .groupban').forEach(function(s){so.observe(s);});}
setCurrent('home');

/* ---------- in-page links: open enclosing details, scroll below the bar, move focus ---------- */
function reveal(el){var p=el;while(p&&p!==d.body){if(p.tagName==='DETAILS')p.open=true;if(p.classList&&p.classList.contains('xc')&&typeof xcSet==='function')xcSet(p,true,{noscroll:true});p=p.parentElement;}}
function goTo(id,focus){var el=d.getElementById(id);if(!el)return false;reveal(el);
 el.scrollIntoView({behavior:reduce()?'auto':'smooth',block:'start'});
 if(focus!==false){var f=el.matches('section,.groupban')?($('h1,h2',el)||el):(el.matches('details')?$('summary',el):(el.matches('.xc')?$('.xc-tog',el):el));if(!f.hasAttribute('tabindex')&&!/^(A|BUTTON|SUMMARY|INPUT)$/.test(f.tagName))f.setAttribute('tabindex','-1');f.focus({preventScroll:true});}
 if(!reduce()&&!el.matches('section,.groupban')){el.classList.remove('flash');void el.offsetWidth;el.classList.add('flash');}
 setCurrent(el.closest('section.sec,section.home,.groupban')?el.closest('section.sec,section.home,.groupban').id:id);return true;}
W.addEventListener('hashchange',function(){var h=location.hash.slice(1);if(h)goTo(decodeURIComponent(h));});
if(location.hash.length>1){var h0=decodeURIComponent(location.hash.slice(1));var t0=d.getElementById(h0);if(t0){reveal(t0);setTimeout(function(){goTo(h0,false);},60);}}
d.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[href^="#"]');if(!a||e.defaultPrevented||e.metaKey||e.ctrlKey)return;var id=decodeURIComponent(a.getAttribute('href').slice(1));if(!id)return;var el=d.getElementById(id);if(!el)return;
 e.preventDefault();var fromMenu=M.contains(a),fromSearch=SD.contains(a);if(fromMenu)closeMenu(false);if(fromSearch)closeSearch(false);
 if(location.hash!=='#'+id)history.pushState(null,'','#'+id);goTo(id);});

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
if(libq){libq.addEventListener('input',libapply);[libb,libt,liby].forEach(function(x){x.addEventListener('change',libapply);});libapply();}

/* ---------- key-date filter (segmented control) ---------- */
var tabs=$$('.segfilter .tab'), rows=$$('#ulist .urow');
tabs.forEach(function(t){t.addEventListener('click',function(){
 tabs.forEach(function(x){x.setAttribute('aria-pressed',x===t?'true':'false');});
 var f=t.dataset.f; rows.forEach(function(r){r.hidden=!(f==='all'||r.dataset.kind===f);});
});});

/* ---------- wide tables: visible "scroll sideways" hint only when needed ---------- */
var wraps=$$('.tablewrap');
wraps.forEach(function(w){var h=d.createElement('p');h.className='scrollhint';h.setAttribute('aria-hidden','true');h.innerHTML=icon('next')+'<span>Swipe or scroll sideways to see the whole table</span>';w.parentNode.insertBefore(h,w.nextSibling);});
function checkTables(){wraps.forEach(function(w){if(!w.offsetParent)return;var s=w.scrollWidth>w.clientWidth+2;w.classList.toggle('is-scroll',s);if(s){w.setAttribute('tabindex','0');w.setAttribute('role','region');if(!w.getAttribute('aria-label')){var c=$('caption',w);w.setAttribute('aria-label',(c?c.textContent.trim():'Table')+' (scrolls sideways)');}}});}
var rzT;addEventListener('resize',function(){clearTimeout(rzT);rzT=setTimeout(checkTables,150);});
d.addEventListener('toggle',function(){checkTables();},true);
checkTables();

/* ---------- document and video viewer: one full-screen sheet ---------- */
var DOCS={};try{DOCS=JSON.parse($('#docdata').textContent);}catch(e){}
var V=$('#viewer'),vBody=$('#vBody'),vTitle=$('#vTitle'),vKind=$('#vKind'),vSrc=$('#vSrc'),vOrig=$('#vOrig'),vDown=$('#vDown'),vPrev=$('#vPrev'),vNext=$('#vNext'),vFoot=$('#vFoot'),vClose=$('#vClose'),vBar=$('.v-bar'),vTools=$('#vTools');
var pgPrev=$('#pgPrev'),pgNext=$('#pgNext'),pgNum=$('#pgNum'),pgOf=$('#pgOf'),zOut=$('#zOut'),zIn=$('#zIn'),zFit=$('#zFit'),zVal=$('#zVal');
var seq=[],pos=0,lastFocus=null,pushed=false,token=0;
var CREDIT='Public record, copied from rindgenh.org on Oct 9, 2026; the original is authoritative.';
var KINDS={pdf:'Town document · copy',word:'Town document · converted copy for viewing',embed:'Outside source',ext:'Outside source',large:'Town document · large scan',missing:'Town document · not available',video:'Meeting video · Town Hall Streams'};
function hostLabel(e){return /rindgenh/.test(e.host||'')?'rindgenh.org':(e.host||'').replace(/^www\./,'');}
function card(h,p,btns,cls){return '<div class="v-card'+(cls?' '+cls:'')+'" role="note"><h3>'+icon('info')+'<span>'+esc(h)+'</span></h3><p>'+p+'</p><div class="v-btns">'+btns+'</div></div>';}
function btn(href,label,ic,primary,dl){return '<a class="vbtn'+(primary?' primary':'')+'" href="'+esc(href)+'"'+(dl?' download':' target="_blank" rel="noopener"')+'>'+icon(ic)+'<span>'+esc(label)+'</span>'+(dl?'':'<span class="sr"> (opens in new tab)</span>')+'</a>';}
function hms(s){s=Math.max(0,Math.round(s||0));var h=Math.floor(s/3600),m=Math.floor(s%3600/60),x=s%60;return (h?h+':'+(m<10?'0':''):'')+m+':'+(x<10?'0':'')+x;}
function dur(s){var h=Math.floor(s/3600),m=Math.round(s%3600/60);return h?(h+'\u00a0hr '+m+'\u00a0min'):(m+'\u00a0min');}
function loader(msg){return '<div class="v-load" id="vLoad" role="status"><span class="spin" aria-hidden="true"></span><span class="v-lmsg">'+esc(msg)+'</span><span class="v-lmore" hidden></span></div>';}

/* --- PDF engine: bundled PDF.js (vendor/pdfjs), loaded on first use --- */
var pdfP=null,PDF=null,PDFBASE='';
function loadPdfjs(){if(pdfP)return pdfP;var base=new URL('vendor/pdfjs/',location.href).href;
 try{pdfP=(new Function('u','return import(u)'))(base+'pdf.min.mjs').then(function(m){m.GlobalWorkerOptions.workerSrc=base+'pdf.worker.min.mjs';PDFBASE=base;return m;});}
 catch(e){pdfP=Promise.reject(e);}
 pdfP.catch(function(){pdfP=null;});return pdfP;}
var P=null; /* current pdf state */
function pdfFail(e,id,why){if(id!==token)return;P=null;vTools.hidden=true;V.classList.remove('pdfmode');
 var local=e.kind==='pdf'||e.kind==='word';
 vBody.innerHTML=card(why==='slow'?'This document is taking a long time':'This document could not be shown here',
  (why==='slow'?'It may be very large or the connection may be slow. ':'Your browser could not draw it inside this page. ')+'You can still read it in your device\'s own viewer, download it, or open the original.',
  btn(e.view,'Open the document','doc',true)+(local?btn(e.file,'Download','download',false,true):'')+btn(e.src,'Open original on '+hostLabel(e),'external'));}
function renderPdf(e,id){
 vTools.hidden=false;V.classList.add('pdfmode');pgNum.value='1';pgOf.textContent='of …';zVal.textContent='Fit';
 P={id:id,e:e};
 vBody.innerHTML=loader('Loading document…')+'<div class="pdfpages" id="pdfPages" aria-label="'+esc(e.title)+'"></div>';
 var slowT=setTimeout(function(){var m=$('.v-lmore',vBody);if(m&&id===token){m.hidden=false;m.innerHTML='Still loading. <a href="'+esc(e.view)+'" target="_blank" rel="noopener">Open it in a new tab</a> instead.';}},9000);P.slowT=slowT;
 loadPdfjs().then(function(m){if(id!==token)return;PDF=m;
  var task=m.getDocument({url:new URL(e.view,location.href).href,cMapUrl:PDFBASE+'cmaps/',cMapPacked:true,standardFontDataUrl:PDFBASE+'standard_fonts/',isEvalSupported:false});
  if(!P||P.id!==id)return;P.task=task;
  return task.promise.then(function(doc){if(id!==token){doc.destroy();return;}P.doc=doc;P.n=doc.numPages;pgOf.textContent='of '+doc.numPages;
   return doc.getPage(1).then(function(pg){if(id!==token)return;P.vp1=pg.getViewport({scale:1});setupPages();});});
 }).catch(function(err){clearTimeout(slowT);if(id!==token)return;
  /* PDF.js unavailable (e.g. opened from a file on disk): use the browser's own viewer if it has one, else offer buttons */
  if(navigator.pdfViewerEnabled!==false&&!smallTouch()&&location.protocol==='file:'){vTools.hidden=true;V.classList.remove('pdfmode');
   vBody.innerHTML=loader('Loading document…')+'<iframe title="'+esc(e.title)+'" src="'+esc(e.view)+'#view=FitH"></iframe>';var fr=$('iframe',vBody);fr.addEventListener('load',function(){var l=$('#vLoad');if(l)l.classList.add('done');});return;}
  pdfFail(e,id);});
}
function smallTouch(){return W.matchMedia&&matchMedia('(pointer: coarse)').matches&&Math.min(screen.width,innerWidth)<700;}
function fitW(){return Math.max(200,Math.min(920,vBody.clientWidth-(innerWidth<600?16:48)));}
function setupPages(){var box=$('#pdfPages');if(!box||!P)return;P.zoom=P.zoom||0;/* 0 = fit width */
 var html='';for(var i=1;i<=P.n;i++)html+='<div class="pdfpage" data-p="'+i+'" role="img" aria-label="Page '+i+' of '+P.n+'"><span class="pp-n" aria-hidden="true">'+i+'</span></div>';box.innerHTML=html;
 P.pages=$$('.pdfpage',box);sizePages();
 if(P.io)P.io.disconnect();
 P.io=new IntersectionObserver(function(es){es.forEach(function(en){var el=en.target,p=+el.dataset.p;if(en.isIntersecting)drawPage(p);else freePage(p);});},{root:vBody,rootMargin:'150% 0px'});
 P.pages.forEach(function(el){P.io.observe(el);});
 if(P.cur)P.cur.disconnect();
 P.cur=new IntersectionObserver(function(){updCur();},{root:vBody,threshold:[0,.25,.5,.75,1]});P.pages.forEach(function(el){P.cur.observe(el);});
 updZoom();}
function scale(){var base=fitW()/P.vp1.width;return P.zoom?base*P.zoom:base;}
function sizePages(){var s=scale(),w=Math.round(P.vp1.width*s),h=Math.round(P.vp1.height*s);P.pages.forEach(function(el){if(!el._vp){el.style.width=w+'px';el.style.height=h+'px';}else{el.style.width=Math.round(el._vp.width*s)+'px';el.style.height=Math.round(el._vp.height*s)+'px';}});}
function drawPage(p){var el=P.pages[p-1];if(!el||el._busy)return;var s=scale();if(el._drawn===s)return;el._busy=true;var id=P.id,doc=P.doc;
 doc.getPage(p).then(function(pg){if(!P||P.id!==id){el._busy=false;return;}var vp1=pg.getViewport({scale:1});el._vp=vp1;
  var css=pg.getViewport({scale:s}),dpr=Math.min(W.devicePixelRatio||1,2),max=4096*4096;var k=dpr;if(css.width*css.height*k*k>max)k=Math.sqrt(max/(css.width*css.height));
  var vp=pg.getViewport({scale:s*k}),c=d.createElement('canvas');c.width=Math.floor(vp.width);c.height=Math.floor(vp.height);c.style.width=Math.round(css.width)+'px';c.style.height=Math.round(css.height)+'px';c.setAttribute('aria-hidden','true');
  el.style.width=Math.round(css.width)+'px';el.style.height=Math.round(css.height)+'px';
  return pg.render({canvasContext:c.getContext('2d'),viewport:vp}).promise.then(function(){if(!P||P.id!==id)return;var old=$('canvas',el);if(old)old.remove();el.appendChild(c);el._drawn=s;el.classList.add('drawn');
   if(p===1){var l=$('#vLoad');if(l)l.classList.add('done');clearTimeout(P.slowT);}
   if(!el._txt){el._txt=1;pg.getTextContent().then(function(tc){var t=tc.items.map(function(x){return x.str;}).join(' ').replace(/\s+/g,' ').trim();if(t){var sr=d.createElement('div');sr.className='sr';sr.textContent=t;el.appendChild(sr);}}).catch(function(){});}
  });}).catch(function(){var l=$('#vLoad');if(p===1&&l&&P)pdfFail(P.e,P.id);}).then(function(){el._busy=false;if(P&&el._drawn!==scale()&&isNear(el))drawPage(p);});}
function isNear(el){var r=el.getBoundingClientRect(),b=vBody.getBoundingClientRect();return r.bottom>b.top-b.height*1.5&&r.top<b.bottom+b.height*1.5;}
function freePage(p){var el=P&&P.pages[p-1];if(!el)return;var c=$('canvas',el);if(c){c.width=0;c.height=0;c.remove();}el._drawn=null;el.classList.remove('drawn');}
function updCur(){if(!P||!P.pages)return;var b=vBody.getBoundingClientRect(),best=1,bv=-1;P.pages.forEach(function(el,i){var r=el.getBoundingClientRect();var v=Math.min(r.bottom,b.bottom)-Math.max(r.top,b.top);if(v>bv){bv=v;best=i+1;}});P.at=best;if(d.activeElement!==pgNum)pgNum.value=String(best);pgPrev.disabled=best<=1;pgNext.disabled=best>=P.n;}
function goPage(n){if(!P||!P.pages)return;n=Math.max(1,Math.min(P.n,n|0));var el=P.pages[n-1];vBody.scrollTo({top:el.offsetTop-8,behavior:reduce()?'auto':'smooth'});P.at=n;pgNum.value=String(n);pgPrev.disabled=n<=1;pgNext.disabled=n>=P.n;}
function updZoom(){if(!P)return;zVal.textContent=P.zoom?Math.round(P.zoom*100)+'%':'Fit';zFit.setAttribute('aria-pressed',P.zoom?'false':'true');zOut.disabled=!!P.zoom&&P.zoom<=.5;zIn.disabled=!!P.zoom&&P.zoom>=4;}
function setZoom(z){if(!P||!P.pages)return;var at=P.at||1,el=P.pages[at-1],off=el?(vBody.scrollTop-el.offsetTop)/Math.max(1,el.offsetHeight):0;
 P.zoom=z;sizePages();updZoom();el=P.pages[at-1];if(el)vBody.scrollTop=el.offsetTop+off*el.offsetHeight;
 P.pages.forEach(function(x,i){if(isNear(x))drawPage(i+1);});}
var ZS=[.5,.75,1,1.25,1.5,2,3,4];
function zoomStep(dir){if(!P)return;var cur=P.zoom||1,i;if(dir>0){for(i=0;i<ZS.length&&ZS[i]<=cur+.01;i++);setZoom(ZS[Math.min(i,ZS.length-1)]);}else{for(i=ZS.length-1;i>=0&&ZS[i]>=cur-.01;i--);setZoom(ZS[Math.max(i,0)]);}}
zIn.addEventListener('click',function(){zoomStep(1);});zOut.addEventListener('click',function(){zoomStep(-1);});zFit.addEventListener('click',function(){setZoom(0);});
pgPrev.addEventListener('click',function(){goPage((P&&P.at||1)-1);});pgNext.addEventListener('click',function(){goPage((P&&P.at||1)+1);});
pgNum.addEventListener('keydown',function(e){if(e.key==='Enter'){e.preventDefault();goPage(parseInt(pgNum.value,10)||1);}});
pgNum.addEventListener('change',function(){goPage(parseInt(pgNum.value,10)||1);});
pgNum.addEventListener('focus',function(){pgNum.select();});
var vrz;addEventListener('resize',function(){clearTimeout(vrz);vrz=setTimeout(function(){if(P&&P.pages&&!V.hidden)setZoom(P.zoom||0);},180);});
function stopPdf(){if(P){clearTimeout(P.slowT);if(P.io)P.io.disconnect();if(P.cur)P.cur.disconnect();try{if(P.doc)P.doc.destroy();else if(P.task)P.task.destroy();}catch(e){}}P=null;vTools.hidden=true;V.classList.remove('pdfmode');}

/* --- video: Town Hall Streams refuses to be framed, so its public stream plays in our own player --- */
var hlsP=null;
function loadHls(){if(hlsP)return hlsP;hlsP=new Promise(function(ok,no){if(W.Hls){ok(W.Hls);return;}var s=d.createElement('script');s.src='vendor/hls/hls.light.min.js';s.onload=function(){W.Hls?ok(W.Hls):no();};s.onerror=no;d.head.appendChild(s);});hlsP.catch(function(){hlsP=null;});return hlsP;}
var VID=null;
function stopVid(){if(VID){try{VID.v.pause();}catch(e){}if(VID.hls)try{VID.hls.destroy();}catch(e){}clearTimeout(VID.t);}VID=null;}
function renderVideo(e,id){var dt=e.date?new Date(e.date+'T12:00:00'):null;var when=dt?dt.toLocaleDateString('en-US',{weekday:'short',month:'short',day:'numeric',year:'numeric'}):'';
 var ch=e.chapters||[],evid=e.date?('ev-sb-'+e.date):'';var hasEv=evid&&d.getElementById(evid);
 var h='<div class="vid"><div class="vid-stage" id="vidStage"><button type="button" class="vid-poster" id="vidPlay"><span class="vp-ic">'+icon('play')+'</span><span class="vp-t">Play the video here</span><span class="vp-s">Select Board · '+esc(when)+(e.dur?' · '+dur(e.dur):'')+'</span></button></div>'
  +'<div class="vid-info"><p class="vid-badges"><span class="bdg b-official">Official recording · Town Hall Streams</span></p>'
  +'<p class="vid-note">The video streams from Town Hall Streams, the town\'s meeting video service. This guide does not host or edit it. If it will not play, use "Open on Town Hall Streams".</p>';
 if(ch.length){h+='<h3 class="vid-h" id="chH">Jump to a topic</h3><p class="vid-badges"><span class="bdg b-audio">Unofficial · own transcription</span></p>'
  +'<p class="vid-note">Topic times and the short excerpts below come from this guide\'s own automatic speech-to-text of the recording\'s audio. They are not official, were not checked against the video, and may get words, names and numbers wrong. The minutes, once posted, are the record.</p><ol class="chaps" aria-labelledby="chH">';
  ch.forEach(function(c){h+='<li><button type="button" class="chap" data-t="'+c.t+'"><span class="ct">'+hms(c.t)+'</span><span class="cl">'+esc(c.label)+'</span>'+icon('play')+'<span class="sr"> (play from '+hms(c.t)+')</span></button>'+(c.text?'<blockquote class="cx"><p>"'+esc(c.text)+'"</p></blockquote>':'')+'</li>';});h+='</ol>';}
 else h+='<p class="vid-note">No transcript or topic list for this meeting. The official minutes, when posted, are the record of what was decided.</p>';
 if(hasEv)h+='<p><a class="xc-link" href="#'+evid+'" data-close="viewer">'+icon('calendar')+'<span>This meeting\'s agenda, minutes and notes</span></a></p>';
 h+='</div></div>';vBody.innerHTML=h;
 $('#vidPlay').addEventListener('click',function(){playVid(e,id,0);});
 $$('.chap',vBody).forEach(function(b){b.addEventListener('click',function(){playVid(e,id,+b.dataset.t);});});}
var vRetry={};
function vidErr(e,id,msg){if(id!==token)return;var t=VID&&VID.v?VID.v.currentTime||VID.want||0:0;
 if(!vRetry[e.hls]){vRetry[e.hls]=1;stopVid();setTimeout(function(){if(id===token)playVid(e,id,t);},1500);return;}
 stopVid();var st=$('#vidStage');if(!st)return;
 st.innerHTML=card('The video could not play here',esc(msg||'Town Hall Streams did not send the video to this page.')+' You can watch it on the Town Hall Streams site instead.',btn(e.src,'Watch on Town Hall Streams','external',true),'vid-err');}
function playVid(e,id,t){var st=$('#vidStage');if(!st)return;
 if(VID&&VID.id===id){seekVid(t);return;}
 st.innerHTML=loader('Loading video…')+'<video id="vidEl" controls playsinline preload="auto" aria-label="'+esc(e.title)+'"></video>';
 var v=$('#vidEl'),ld=$('#vLoad');VID={v:v,id:id,want:t};
 var ready=function(){if(ld)ld.classList.add('done');clearTimeout(VID&&VID.t);};
 v.addEventListener('loadedmetadata',function(){ready();if(VID&&VID.want){try{v.currentTime=VID.want;}catch(x){}VID.want=0;}var p=v.play();if(p&&p.catch)p.catch(function(){});});
 v.addEventListener('error',function(){vidErr(e,id);});
 VID.t=setTimeout(function(){if(v.readyState<1)vidErr(e,id,'The video did not start loading.');},20000);
 if(v.canPlayType('application/vnd.apple.mpegurl')){v.src=e.hls;}
 else loadHls().then(function(Hls){if(!VID||VID.id!==id)return;if(!Hls.isSupported()){vidErr(e,id,'This browser cannot play this kind of video stream.');return;}
  var hl=new Hls({maxBufferLength:30});VID.hls=hl;hl.on(Hls.Events.ERROR,function(_,dd){if(dd&&dd.fatal)vidErr(e,id);});hl.loadSource(e.hls);hl.attachMedia(v);},function(){vidErr(e,id,'The video player could not load.');});
 v.focus({preventScroll:true});}
function seekVid(t){if(!VID)return;var v=VID.v;if(v.readyState<1){VID.want=t;return;}try{v.currentTime=t;}catch(x){}var p=v.play();if(p&&p.catch)p.catch(function(){});$('#vidStage').scrollIntoView({block:'nearest',behavior:reduce()?'auto':'smooth'});}

function render(){var id=seq[pos],e=DOCS[id];if(!e)return;token++;var my=token;stopPdf();stopVid();
 vTitle.textContent=e.title;vKind.textContent=KINDS[e.kind]+(seq.length>1?' · '+(pos+1)+' of '+seq.length:'');
 vSrc.textContent=e.src.replace(/^https?:\/\//,'').replace(/\?t=\d+$/,'');vSrc.href=e.src;
 vOrig.href=e.src;$('.lg',vOrig).textContent=e.kind==='video'?'Open on Town Hall Streams':'Open original on '+hostLabel(e);$('.sh',vOrig).textContent=e.kind==='video'?'Open on Town Hall Streams':'Original';
 var local=e.kind==='pdf'||e.kind==='word';vDown.hidden=!local;if(local){vDown.href=e.file;vDown.setAttribute('download','');}
 vPrev.disabled=pos<=0;vNext.disabled=pos>=seq.length-1;vBar.classList.toggle('single',seq.length<2);
 V.classList.toggle('vidmode',e.kind==='video');V.classList.remove('carded');vBody.scrollTop=0;
 if(local)renderPdf(e,my);
 else if(e.kind==='video'&&e.hls)renderVideo(e,my);
 else if(e.kind==='embed'&&navigator.onLine!==false){vBody.innerHTML=loader('Loading page…')+'<iframe title="'+esc(e.title)+'" src="'+esc(e.src)+'" sandbox="allow-scripts allow-same-origin allow-popups allow-forms" referrerpolicy="no-referrer-when-downgrade"></iframe>';
  var fr=$('iframe',vBody),ld=$('#vLoad');fr.addEventListener('load',function(){if(ld)ld.classList.add('done');});
  setTimeout(function(){if(my===token&&ld&&!ld.classList.contains('done')){var m=$('.v-lmore',vBody);m.hidden=false;m.innerHTML='Still loading. <a href="'+esc(e.src)+'" target="_blank" rel="noopener">Open it in a new tab</a>.';}},8000);}
 else{V.classList.add('carded');
  if(e.kind==='embed')vBody.innerHTML=card('You appear to be offline','This outside source needs an internet connection.',btn(e.src,'Open in a new tab','external',true));
  else if(e.kind==='large')vBody.innerHTML=card('Large scan: opens on the town website','This annual report is a very large scanned file, so this guide links to the town\'s copy instead of storing one.',btn(e.src,'Open on rindgenh.org','external',true));
  else if(e.kind==='missing')vBody.innerHTML=card('This document is not available right now','The town website returned "not found" for this link when it was checked on Oct 9, 2026. The file may have moved. Try the board\'s agendas and minutes page, or ask the Town Offices at (603) 899-5181.',btn(e.src,'Try the original link','external',true));
  else vBody.innerHTML=card('Opens in a new tab',esc(e.org||hostLabel(e))+' does not allow its pages to be shown inside other websites, so this one opens in a new browser tab.',btn(e.src,'Open '+hostLabel(e)+' in a new tab','external',true));}
 vFoot.innerHTML=local?(esc(CREDIT)+(e.kind==='word'?' This is a PDF rendering of a Word file; Download gives the original Word file.':'')):(e.kind==='embed'?'Shown from '+esc(hostLabel(e))+'. If it does not load, use "Open original".':(e.kind==='video'?'Recording: Town Hall Streams. Transcript excerpts, where shown, are unofficial.':''));
}
function openDoc(id,list,trigger){if(!DOCS[id])return false;seq=list&&list.length?list:[id];pos=Math.max(0,seq.indexOf(id));if(V.hidden)lastFocus=trigger||d.activeElement;
 var was=V.hidden;V.hidden=false;if(was)lock(true);render();vTitle.focus();
 if(!pushed&&!ignorePop){try{history.pushState({viewer:1},'',location.href);pushed=true;}catch(e){}}return true;}
var ignorePop=0;
function closeDoc(fromPop,noRestore){if(V.hidden)return;token++;stopPdf();stopVid();V.hidden=true;vBody.innerHTML='';lock(false);
 if(pushed&&!fromPop){ignorePop++;try{history.back();}catch(e){ignorePop--;}}pushed=false;
 if(!noRestore&&lastFocus&&lastFocus.focus&&d.contains(lastFocus)){lastFocus.focus({preventScroll:true});refocus=lastFocus;}}
var refocus=null;
W.addEventListener('popstate',function(){if(ignorePop>0){ignorePop--;var r=refocus;refocus=null;if(r){var fix=function(){if((d.activeElement===d.body||!d.activeElement)&&d.contains(r)&&V.hidden)r.focus({preventScroll:true});};fix();setTimeout(fix,0);setTimeout(fix,80);}return;}if(!V.hidden)closeDoc(true);});
vClose.addEventListener('click',function(){closeDoc();});
vPrev.addEventListener('click',function(){if(pos>0){pos--;render();}});
vNext.addEventListener('click',function(){if(pos<seq.length-1){pos++;render();}});
vBody.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[data-close="viewer"]');if(a){var h=a.getAttribute('href');e.preventDefault();e.stopPropagation();closeDoc(false,true);setTimeout(function(){history.pushState(null,'',h);goTo(h.slice(1));},30);}});
V.addEventListener('keydown',function(e){var typing=e.target===pgNum;
 if(e.key==='Escape'){e.preventDefault();e.stopPropagation();closeDoc();}else if(e.key==='Tab')trap(V,e);
 else if((e.key==='ArrowRight'||e.key==='ArrowLeft')&&e.altKey){(e.key==='ArrowRight'?vNext:vPrev).click();}
 else if(P&&P.pages&&!typing&&!e.target.closest('video')){if(e.key==='+'||e.key==='='){zoomStep(1);e.preventDefault();}else if(e.key==='-'){zoomStep(-1);e.preventDefault();}else if(e.key==='0'){setZoom(0);e.preventDefault();}
  else if(e.key==='PageDown'&&e.altKey){goPage((P.at||1)+1);e.preventDefault();}else if(e.key==='PageUp'&&e.altKey){goPage((P.at||1)-1);e.preventDefault();}}});
function seqFor(a){var c=a.closest('#libtable tbody')||a.closest('.ev')||a.closest('section')||d.body,ids=[];
 $$('a[data-doc]',c).forEach(function(x){if(x.closest('tr[hidden],.ev[hidden],.law[hidden],.dir[hidden]'))return;var i=x.getAttribute('data-doc');if(ids.indexOf(i)<0)ids.push(i);});return ids;}
d.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[data-doc]');if(!a||e.defaultPrevented||e.button!==0||e.metaKey||e.ctrlKey||e.shiftKey||e.altKey)return;if(V.contains(a))return;
 if(openDoc(a.getAttribute('data-doc'),seqFor(a),a))e.preventDefault();});

/* ---------- expandable cards: tap the card or its Details button; Esc closes; links deep-link and open them ---------- */
function xcSet(c,open,opts){var b=$('.xc-tog',c);if(!b)return;var was=c.classList.contains('open');if(was===open)return;
 c.classList.toggle('open',open);b.setAttribute('aria-expanded',open?'true':'false');
 if(open&&opts&&opts.hash&&c.id){try{history.replaceState(history.state,'','#'+c.id);}catch(e){}}
 if(!open&&c.contains(d.activeElement)&&d.activeElement!==b)b.focus({preventScroll:true});
 if(open&&!(opts&&opts.noscroll)){setTimeout(function(){var r=c.getBoundingClientRect();if(r.bottom>innerHeight-16){c.scrollIntoView({block:r.height>innerHeight-80?'start':'end',behavior:reduce()?'auto':'smooth'});}},reduce()?0:230);}
 checkTables();}
d.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('.xc-tog');var c;
 if(b){c=b.closest('.xc');xcSet(c,!c.classList.contains('open'),{hash:true});return;}
 c=e.target.closest&&e.target.closest('.xc');if(!c||e.defaultPrevented)return;
 if(e.target.closest('a,button,input,select,textarea,label,summary,video,.xc-body'))return;
 var sel=W.getSelection&&String(W.getSelection());if(sel&&sel.length>2)return;
 xcSet(c,!c.classList.contains('open'),{hash:true});});
d.addEventListener('keydown',function(e){if(e.key!=='Escape')return;var c=d.activeElement&&d.activeElement.closest&&d.activeElement.closest('.xc.open');if(c&&V.hidden&&SD.hidden&&M.hidden){xcSet(c,false);$('.xc-tog',c).focus();}});

/* ---------- global search with suggestions ---------- */
var IDX=[];try{IDX=JSON.parse($('#searchdata').textContent);}catch(e){}
IDX.forEach(function(x){x.n=(x.t+' '+x.s).toLowerCase();x.tl=x.t.toLowerCase();});
var SD=$('#searchDlg'),sdq=$('#sdq'),sdres=$('#sdres'),sdHint=$('#sdHint'),sdSugg=$('#sdSugg'),sdLast=null,sel=-1,results=[];
var ORDER=['Section','How do I','Directory','Meeting','Date','Topic','Recurring issue','Law','Glossary','Document'],KIC={'Section':'grid','How do I':'question','Directory':'phone','Meeting':'calendar','Date':'calendar','Topic':'info','Recurring issue':'growth','Law':'scale','Glossary':'book','Document':'doc'};
var SUGG=['budget','building permit','elderly exemption','tax rate','wetlands','ambulance','petition','dog license','Town Offices','zoning ordinance','Select Board minutes','frontage'];
var JUMP=[['#calendar','calendar','Upcoming dates and deadlines'],['#library','doc','Document library'],['#howto','question','How do I...? guides'],['#directory','phone','Town directory'],['#numbers','tax','Taxes and exemptions']];
function hits(v){var ws=v.toLowerCase().split(/\s+/).filter(Boolean);return IDX.filter(function(x){return ws.every(function(w){return x.n.indexOf(w)>-1;});});}
sdSugg.innerHTML='<h3 id="sgK">Try searching for</h3><ul class="sd-chips" aria-labelledby="sgK">'+SUGG.filter(function(s){return hits(s).length>0;}).map(function(s){return '<li><button type="button" class="sd-chip" data-q="'+esc(s)+'">'+icon('search')+esc(s)+'</button></li>';}).join('')+'</ul>'
 +'<h3 id="jpK">Or jump to</h3><ul class="sd-jump" aria-labelledby="jpK">'+JUMP.map(function(j){return '<li><a href="'+j[0]+'">'+icon(j[1])+'<span>'+esc(j[2])+'</span></a></li>';}).join('')+'</ul>';
sdSugg.addEventListener('click',function(e){var b=e.target.closest('.sd-chip');if(!b)return;sdq.value=b.getAttribute('data-q');runSearch();sdq.focus();});
function hi(t,ws){var s=esc(t);ws.forEach(function(w){if(w.length<2)return;s=s.replace(new RegExp('('+w.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+')','ig'),'<mark>$1</mark>');});return s;}
function runSearch(){var v=sdq.value.trim().toLowerCase(),ws=v.split(/\s+/).filter(Boolean);sdres.innerHTML='';results=[];sel=-1;sdq.removeAttribute('aria-activedescendant');
 if(v.length<2){sdSugg.hidden=false;sdq.setAttribute('aria-expanded','false');sdHint.textContent='Type at least 2 letters, or pick a suggestion. Use the arrow keys to move, Enter to open, Esc to close.';return;}
 sdSugg.hidden=true;sdq.setAttribute('aria-expanded','true');
 var hs=hits(v).map(function(x){var sc=0;ws.forEach(function(w){if(x.tl.indexOf(w)>-1)sc+=3;if(x.tl.indexOf(w)===0)sc+=2;});return {x:x,sc:sc};});
 hs.sort(function(a,b){return b.sc-a.sc;});
 var groups={};hs.forEach(function(h){(groups[h.x.k]=groups[h.x.k]||[]).push(h.x);});
 var html='',n=0;ORDER.forEach(function(k){var g=groups[k];if(!g)return;html+='<li class="sg" role="presentation">'+esc(k)+(g.length>8?' ('+g.length+')':'')+'</li>';
  g.slice(0,8).forEach(function(x){results.push(x);html+='<li role="option" id="sr'+n+'" aria-selected="false" data-i="'+n+'">'+icon(KIC[k]||'info')+'<span class="st">'+hi(x.t,ws)+'</span><span class="ss">'+hi(x.s,ws)+'</span></li>';n++;});});
 sdres.innerHTML=html;sdHint.textContent=hs.length?(hs.length+' result'+(hs.length===1?'':'s')+(hs.length>n?', showing the best '+n:'')+'.'):'No results. Try a different word, such as "budget", "permit" or "wetlands".';
 if(n)move(0);}
function move(i){var opts=$$('[role=option]',sdres);if(!opts.length)return;sel=(i+opts.length)%opts.length;opts.forEach(function(o,j){o.setAttribute('aria-selected',j===sel?'true':'false');});sdq.setAttribute('aria-activedescendant','sr'+sel);opts[sel].scrollIntoView({block:'nearest'});}
function activate(i){var x=results[i];if(!x)return;closeSearch(false);
 if(x.h.indexOf('doc:')===0){openDoc(x.h.slice(4),[x.h.slice(4)]);}
 else{var id=x.h.slice(1);history.pushState(null,'','#'+id);goTo(id);}}
function openSearch(v){if(!SD.hidden){sdq.focus();return;}sdLast=d.activeElement;SD.hidden=false;lock(true);sdq.value=v||'';sdq.focus();runSearch();}
function closeSearch(restore){if(SD.hidden)return;SD.hidden=true;lock(false);if(restore!==false&&sdLast&&sdLast.focus)sdLast.focus();}
var stm;sdq.addEventListener('input',function(){clearTimeout(stm);stm=setTimeout(runSearch,80);});
sdq.addEventListener('keydown',function(e){if(e.key==='ArrowDown'){move(sel+1);e.preventDefault();}else if(e.key==='ArrowUp'){move(sel-1);e.preventDefault();}else if(e.key==='Enter'){if(sel>-1)activate(sel);e.preventDefault();}});
sdres.addEventListener('click',function(e){var o=e.target.closest('[role=option]');if(o)activate(+o.getAttribute('data-i'));});
SD.addEventListener('keydown',function(e){if(e.key==='Escape'){e.preventDefault();e.stopPropagation();closeSearch();}else if(e.key==='Tab')trap(SD,e);});
SD.addEventListener('click',function(e){if(e.target.getAttribute&&e.target.getAttribute('data-close')==='search')closeSearch();});
$('#sdClose').addEventListener('click',function(){closeSearch();});
$('#searchBtn').addEventListener('click',function(){openSearch('');});
var hs=$('#homeSearch');if(hs)hs.addEventListener('click',function(){openSearch('');});
if(/Mac|iPhone|iPad/.test(navigator.platform||''))$$('.kbd').forEach(function(k){k.textContent='⌘ K';});
d.addEventListener('keydown',function(e){var k=(e.key||'').toLowerCase();var typing=/^(INPUT|TEXTAREA|SELECT)$/.test((d.activeElement||{}).tagName||'');
 if((e.metaKey||e.ctrlKey)&&k==='k'){e.preventDefault();if(!V.hidden)return;if(SD.hidden){closeMenu(false);openSearch('');}else closeSearch();}
 else if(k==='/'&&!typing&&SD.hidden&&V.hidden&&M.hidden){e.preventDefault();openSearch('');}});

/* ---------- charts: animate once when scrolled into view (exact widths come from --w) ---------- */
var charts=$$('.chart'), pending=charts.slice();
function revealC(c){if(!c.classList.contains('in'))c.classList.add('in');}
function checkCharts(){if(!pending.length)return;var vh=innerHeight||root.clientHeight;
 pending=pending.filter(function(c){var r=c.getBoundingClientRect();if(r.top<vh*0.95&&r.bottom>0){revealC(c);return false;}return true;});}
if(root.classList.contains('anim')){
 if('IntersectionObserver' in W){var io=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){revealC(en.target);io.unobserve(en.target);pending=pending.filter(function(x){return x!==en.target;});}});},{threshold:.15});charts.forEach(function(c){io.observe(c);});}
 addEventListener('scroll',function(){requestAnimationFrame(checkCharts);},{passive:true});
 addEventListener('resize',checkCharts);
 checkCharts();
}else{charts.forEach(revealC);}
var nums=$$('[data-count]');
if(root.classList.contains('anim')&&'IntersectionObserver' in W){
 var fmt=function(n){return n.toLocaleString('en-US');};
 var co=new IntersectionObserver(function(es){es.forEach(function(en){if(!en.isIntersecting)return;co.unobserve(en.target);
  var el=en.target,end=+el.dataset.count,t0=null,dur=700;
  function step(ts){if(!t0)t0=ts;var p=Math.min(1,(ts-t0)/dur),e=1-Math.pow(1-p,3);el.textContent=fmt(Math.round(end*e));if(p<1)requestAnimationFrame(step);else el.textContent=fmt(end);}
  requestAnimationFrame(step);});},{threshold:.5});
 nums.forEach(function(n){co.observe(n);});
}

/* ---------- reading progress, back to top ---------- */
var prog=$('#progress'), tt=$('#toTop'), ticking=false;
function onScroll(){ticking=false;var h=root.scrollHeight-innerHeight;var p=h>0?Math.min(1,Math.max(0,scrollY/h)):0;prog.style.transform='scaleX('+p+')';tt.classList.toggle('show',scrollY>Math.max(600,innerHeight));}
addEventListener('scroll',function(){if(!ticking){ticking=true;requestAnimationFrame(onScroll);}},{passive:true});
onScroll();
tt.addEventListener('click',function(){scrollTo({top:0,behavior:reduce()?'auto':'smooth'});if(location.hash)history.pushState(null,'',location.pathname+location.search);var m=$('#home-h');if(m){m.setAttribute('tabindex','-1');m.focus({preventScroll:true});}});

/* ---------- print: open everything ---------- */
var opened=[];
addEventListener('beforeprint',function(){charts.forEach(revealC);opened=$$('details:not([open])');opened.forEach(function(x){x.open=true;});});
addEventListener('afterprint',function(){opened.forEach(function(x){x.open=false;});});
W.RindgeGuide={openDoc:openDoc,closeDoc:closeDoc,openSearch:openSearch,closeSearch:closeSearch,openMenu:openMenu,closeMenu:closeMenu};
})();
