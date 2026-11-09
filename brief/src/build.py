"""Builds the two-page brief as designed pages: brief/index.html (English) and brief/es/index.html (Spanish),
from en.md / es.md beside this script. Usage: python3 build.py <site repo dir>"""
import markdown, re, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = sys.argv[1]

L = {
 'en': dict(path='brief/index.html', up='../', other='es/', other_label='Español', lang='en',
   title='Bitaid in two pages',
   desc="Emergency help, paid peer to peer on Bitcoin: the problem, the insurance lever, how a case runs, why cheating does not pay, and what already runs on Bitcoin's public signet.",
   nav=[('Whitepaper', 'index.html'), ('Specification', 'bitaid_v6_specification.html'), ('Foundations', 'bitaid_v6_foundations.html')],
   people='1,000 people paying $2 a month', offer='the offer each of them can summon',
   figcap='Escrowed offers cost nothing until used, and emergencies rarely strike the same people at once: one pooled stake stands behind many offers.',
   down='Read', key=('caller','drone','person','team'), skip='Skip to the brief', events=('incident signed','evidence anchored','payouts settled','offer escrowed','bond posted'), block='block',
   quote='Give me a place to stand, and I will move the earth.', cite='Archimedes'),
 'es': dict(path='brief/es/index.html', up='../../', other='../', other_label='English', lang='es',
   title='Bitaid en dos páginas',
   desc='Ayuda en emergencias, pagada de persona a persona en Bitcoin: el problema, la palanca del seguro, cómo se resuelve un caso, por qué hacer trampa no compensa y lo que ya funciona en la signet pública de Bitcoin.',
   nav=[('Whitepaper', 'index.html'), ('Especificación', 'bitaid_v6_specification.html'), ('Fundamentos', 'bitaid_v6_foundations.html')],
   people='1.000 personas pagando 2 $ al mes', offer='la oferta que cada una puede pedir',
   figcap='Las ofertas en depósito no cuestan nada hasta que se usan, y las emergencias rara vez golpean a las mismas personas a la vez: un mismo depósito respalda muchas ofertas.',
   down='Leer', key=('quien llama','dron','persona','equipo'), skip='Ir al texto', events=('incidente firmado','pruebas ancladas','pagos liquidados','oferta depositada','fianza depositada'), block='bloque',
   quote='Dadme un punto de apoyo y moveré el mundo.', cite='Arquímedes'),
}

CSS = r'''
:root{--night:#141a3a;--night2:#1c2350;--grid:#2b3470;--ink:#ecebf6;--soft:#b9bbd6;--amber:#f3a73b;--amber2:#ffcf7a;--strobe:#a9c4ff;--paper:#f6f5fb;--text:#1b1f3d;--muted:#565b7d;--rule:#d9daea;--row:#eeeef7}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--paper:#171b38;--text:#e7e7f3;--muted:#a3a6c6;--rule:#2d3466;--row:#1e2346}}
:root[data-theme="dark"]{--paper:#171b38;--text:#e7e7f3;--muted:#a3a6c6;--rule:#2d3466;--row:#1e2346}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;scrollbar-width:thin;scrollbar-color:#3a4386 transparent;scroll-behavior:smooth}
::-webkit-scrollbar{width:8px;height:8px}::-webkit-scrollbar-track{background:transparent}::-webkit-scrollbar-thumb{background:#3a4386;border-radius:8px}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
body{margin:0;background:var(--paper);color:var(--text);font-family:"Literata",Georgia,serif;font-size:19px;line-height:1.62;font-optical-sizing:auto}
a{color:inherit;text-decoration-thickness:1px;text-underline-offset:3px}
a:focus-visible,button:focus-visible{outline:3px solid var(--amber);outline-offset:3px;border-radius:2px}
.skip{position:absolute;left:-9999px}.skip:focus{left:16px;top:16px;z-index:9;background:var(--amber);color:#141a3a;padding:.4em .8em}
/* hero: the night map */
.hero{position:relative;min-height:min(100svh,1200px);background:radial-gradient(ellipse 70% 60% at 68% 42%,#232b63 0%,rgba(35,43,99,0) 70%),linear-gradient(180deg,#1a2050 0%,#141a3a 55%,#0f1330 100%);color:var(--ink);overflow:hidden;display:flex;flex-direction:column}
.hero svg.map{position:absolute;inset:0;width:100%;height:100%}
.hero nav{position:relative;z-index:2;display:flex;flex-wrap:wrap;gap:.3em 1.4em;padding:22px 28px;font-family:"Big Shoulders Display",sans-serif;font-weight:600;font-size:17px;letter-spacing:.02em}
.hero nav a{text-decoration:none;color:var(--soft)}.hero nav a:hover{color:var(--ink)}
.hero nav .lang{margin-left:auto;color:var(--amber2)}
.hero .words{position:relative;z-index:2;margin-top:auto;padding:0 28px 56px;max-width:1080px}
.hero h1{font-family:"Big Shoulders Display",sans-serif;font-weight:800;font-size:clamp(44px,min(9vw,10.5vh),128px);line-height:.9;letter-spacing:-.005em;margin:0 0 .28em;max-width:12ch;text-wrap:balance}
html[lang="es"] .hero h1{max-width:16ch;font-size:clamp(40px,min(8vw,9vh),116px)}
@media (max-height:700px) and (min-width:621px){.hero nav{padding-top:14px;padding-bottom:10px}.hero .words{padding-bottom:30px!important}.hero .key{margin-top:.6em}.hero .by{margin-top:.6em!important}}
@media (max-height:820px) and (min-width:621px){.hero .lead{font-size:16.5px;line-height:1.5}.hero .words{padding-bottom:44px}.hero .by{margin-top:1em}}
.hero .lead{font-size:clamp(17px,1.6vw,21px);line-height:1.55;max-width:56ch;color:var(--soft);margin:0}
.hero .by{margin-top:1.4em;font-family:"Big Shoulders Display",sans-serif;font-size:18px;color:var(--soft)}
.hero .by a{color:var(--amber2)}
a.down{transition:opacity .4s;position:absolute;z-index:3;left:50%;bottom:18px;transform:translateX(-50%);display:flex;flex-direction:column;align-items:center;gap:2px;color:var(--soft);text-decoration:none;font:600 15px "Big Shoulders Display",sans-serif;padding:6px 12px}
a.down:hover{color:var(--ink)}a.down svg{width:22px;height:14px;animation:nudge 2.4s ease-in-out 3s 3}
@keyframes nudge{0%,100%{transform:none}50%{transform:translateY(5px)}}
@media (prefers-reduced-motion:reduce){a.down svg{animation:none}}
.hero .key{display:flex;flex-wrap:wrap;gap:.4em 1.2em;align-items:center;margin-top:1.1em;font:600 15px "Big Shoulders Display",sans-serif;color:var(--soft)}
.hero .key span{display:inline-flex;align-items:center;gap:.4em}
.hero .key svg{width:12px;height:12px}
.words>*{opacity:0;transform:translateY(10px);transition:opacity .9s ease,transform .9s ease}
.hero.ready .words>*{opacity:1;transform:none}
.hero.ready .words>*:nth-child(2){transition-delay:.15s}.hero.ready .words>*:nth-child(3){transition-delay:.3s}.hero.ready .words>*:nth-child(4){transition-delay:.45s}
/* the text */
main{max-width:1100px;margin:0 auto;padding:104px 32px 120px}
main section{display:grid;grid-template-columns:250px minmax(0,690px);gap:0 64px;padding:64px 0;border-top:1px solid var(--rule)}
main section:first-child{border-top:0;padding-top:0}
main section>.side{position:sticky;top:28px;align-self:start}
main section>.side h2{font-family:"Big Shoulders Display",sans-serif;font-weight:800;font-size:clamp(34px,3.6vw,46px);line-height:.98;margin:0;text-wrap:balance}
main p{margin:0 0 1em;hyphens:auto}
.wrench,.archimedes svg{display:block;width:170px;height:auto;margin-top:34px;color:var(--text)}
.archimedes{margin:0}.archimedes .globe{stroke:var(--amber)}
.archimedes blockquote{margin:16px 0 0;font-style:italic;font-size:16px;line-height:1.45;color:var(--muted);max-width:22ch}
.archimedes cite{display:block;margin-top:6px;font:700 15px "Big Shoulders Display",sans-serif;font-style:normal;color:var(--muted)}
.wrench .tag{fill:var(--amber)}
.wrench text{font:800 15px "Big Shoulders Display",sans-serif;fill:#141a3a}
@media (max-width:900px){.wrench,.archimedes svg{width:120px;margin:14px 0 6px}.archimedes blockquote{max-width:none;margin-top:8px}}
p.statement{font:800 clamp(30px,3.4vw,44px)/1.05 "Big Shoulders Display",sans-serif;margin:1.4em 0 .2em;padding-left:22px;border-left:5px solid var(--amber);text-wrap:balance;hyphens:manual}
main strong{font-weight:650}
main section:first-child .body>p:first-child{font-size:1.32em;line-height:1.45}
/* the steps, as a route of numbered cells */
ol.steps{list-style:none;padding:0;margin:.4em 0 0;counter-reset:step}
ol.steps li{counter-increment:step;position:relative;padding:0 0 1.5em 66px;min-height:52px}
ol.steps li::before{content:counter(step);position:absolute;left:0;top:-4px;width:44px;height:50px;display:grid;place-items:center;font:800 22px/1 "Big Shoulders Display",sans-serif;color:#141a3a;background:var(--amber);clip-path:polygon(50% 0,100% 25%,100% 75%,50% 100%,0 75%,0 25%)}
ol.steps{position:relative}
ol.steps .route{position:absolute;left:21px;top:30px;bottom:44px;width:2px;background:repeating-linear-gradient(to bottom,var(--amber) 0 3px,transparent 3px 7px);opacity:.4}
ol.steps .fill{position:absolute;left:21px;top:30px;width:2px;height:0;background:var(--amber)}
ol.steps li{z-index:1}
ol.steps li::before{transition:filter .5s,opacity .5s}
.js ol.steps li:not(.on)::before{filter:saturate(.15);opacity:.45}
/* the claims, side by side */
ul.claims{list-style:none;padding:0;margin:.4em 0 0;display:grid;grid-template-columns:1fr 1fr;gap:30px 40px}
ul.claims li{margin:0}
ul.claims li strong{display:block;font:800 23px/1.05 "Big Shoulders Display",sans-serif;margin-bottom:.35em;letter-spacing:.005em}
main ul{padding-left:1.1em;margin:.4em 0 1em}main ul li{margin:0 0 .75em}main ul li::marker{color:var(--amber)}
/* what already runs: each run with its score */
ol.runs{list-style:none;padding:0;margin:1.2em 0 0;border-top:2px solid var(--text)}
ol.runs li{display:grid;grid-template-columns:150px 1fr;gap:6px 28px;padding:22px 0;border-bottom:1px solid var(--rule)}
ol.runs .score{font:800 58px/.9 "Big Shoulders Display",sans-serif;text-decoration:none}
ol.runs .score small{display:block;margin-top:6px;font:600 16px/1.15 "Big Shoulders Display",sans-serif;color:var(--muted)}
ol.runs .score.text{font-size:24px;line-height:1.05}
ol.runs .score.pending{color:var(--amber)}
ol.runs a.score:hover small{color:var(--text)}
ol.runs .meta{font:700 17px/1.25 "Big Shoulders Display",sans-serif;color:var(--muted);margin-bottom:.3em}
ol.runs .what{font-size:.95em;line-height:1.5}
@media (max-width:900px){main{padding:72px 24px 96px}main section{grid-template-columns:1fr;padding:48px 0}main section>.side{position:static;margin-bottom:.55em}}
@media (max-width:620px){ul.claims{grid-template-columns:1fr;gap:22px}ol.runs li{grid-template-columns:1fr}ol.runs .score{font-size:46px}main{padding:56px 16px 80px}}
/* the lever figure */
figure.lever .offer svg polygon{transition:opacity .7s .9s,transform .7s .9s;transform-origin:50% 50%;transform-box:fill-box}
.js figure.lever:not(.on) .offer svg polygon{opacity:.15;transform:scale(.7)}
figure.lever{margin:2em 0 2.2em;padding:28px;background:var(--night);color:var(--ink);border-radius:4px}
figure.lever .row{display:grid;grid-template-columns:1fr auto;gap:22px;align-items:center}
figure.lever svg{width:100%;height:auto;display:block}
figure.lever .k{font-family:"Big Shoulders Display",sans-serif;font-weight:700;font-size:20px;line-height:1.15;margin-top:12px;color:var(--soft)}
figure.lever .k b{color:var(--strobe);font-weight:700}
figure.lever .offer{text-align:center;width:170px}
figure.lever .offer svg{width:96px;height:96px;margin:0 auto}
figure.lever .offer .big{font:800 54px/1 "Big Shoulders Display",sans-serif;color:var(--amber)}
figure.lever .offer .k{color:var(--amber2);font-size:17px}
figure.lever figcaption{margin-top:18px;font-size:15.5px;line-height:1.5;color:var(--soft)}
.hero .chain{position:absolute;z-index:1;right:28px;top:84px;height:calc(min(100svh,1200px) - 112px);width:112px;display:flex;flex-direction:column;justify-content:flex-end;overflow:hidden;font:600 13px/1.2 "Big Shoulders Display",sans-serif;color:var(--soft);-webkit-mask-image:linear-gradient(to bottom,transparent,#000 22%);mask-image:linear-gradient(to bottom,transparent,#000 22%)}
.chain .b{flex:none;position:relative;width:112px;height:112px;display:flex;flex-direction:column;justify-content:space-between;border:1px solid #3a4386;background:#171d45;border-radius:3px;padding:7px 8px;margin-top:18px}
.chain .b::before{content:"";position:absolute;left:50%;top:-19px;height:18px;border-left:1px solid #3a4386}
.chain .b{overflow:visible}
.chain .b .h{color:#7c82b3;font-weight:600;letter-spacing:.02em}
.chain .b .e{color:var(--ink);font-size:15px;line-height:1.1}
.chain .b.reg{border-color:#5d6bb8}
.chain .b.reg .e{color:var(--strobe)}
.chain .b.ev{border-color:var(--amber)}
.chain .b.ev .e{color:var(--amber2)}
@media (max-width:900px){.hero .chain{display:none}}
@media (max-width:620px){body{font-size:17.5px}.hero nav{padding:18px 16px}.hero .words{padding:0 16px 64px}figure.lever{padding:20px}figure.lever .row{grid-template-columns:1fr}figure.lever .offer{width:auto}}
@media (prefers-reduced-motion:reduce){.words>*{transition:none}}
footer{max-width:720px;margin:0 auto;padding:0 24px 64px;color:var(--muted);font-size:15px}
'''

JS = r'''
(function(){
const svg=document.querySelector('svg.map'),hero=document.querySelector('.hero'),NS='http://www.w3.org/2000/svg';
const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
const AMBER='#f3a73b',STROBE='#a9c4ff',GRID='#2b3470';
let W,H,R,dx,dy,cells=[],free=[],gCells,gMarks,gUsers,gMove,running=false,visible=true,timer=null,rtimer=null,first=true;
function el(n,a,p){const e=document.createElementNS(NS,n);for(const k in a)e.setAttribute(k,a[k]);if(p)p.appendChild(e);return e}
function hexPts(x,y,r){let p=[];for(let i=0;i<6;i++){const a=Math.PI/180*(60*i-30);p.push((x+r*Math.cos(a)).toFixed(1)+','+(y+r*Math.sin(a)).toFixed(1))}return p.join(' ')}
function rand(a,b){return a+Math.random()*(b-a)}
// areas the text covers, so alerts never sit under words
function blocked(){const h=hero.getBoundingClientRect(),out=[];
  hero.querySelectorAll('nav,.words>*,.chain').forEach(e=>{const r=e.getBoundingClientRect();if(r.width)out.push({l:r.left-h.left-R*1.4,t:r.top-h.top-R*1.5,r:r.right-h.left+R*1.4,b:r.bottom-h.top+R*1.4})});return out}
function build(){
  svg.innerHTML='';cells=[];W=hero.clientWidth;H=hero.clientHeight;R=Math.max(24,Math.min(42,W/34));
  dx=Math.sqrt(3)*R;dy=1.5*R;svg.setAttribute('viewBox','0 0 '+W+' '+H);
  gCells=el('g',{},svg);gMarks=el('g',{},svg);gUsers=el('g',{},svg);gMove=el('g',{},svg);
  for(let r=-1;r*dy<H+R;r++)for(let c=-1;;c++){const x=c*dx+(r%2?dx/2:0),y=r*dy;if(x>W+R)break;
    cells.push({x,y,p:el('polygon',{points:hexPts(x,y,R*0.94),fill:'none',stroke:GRID,'stroke-width':1},gCells)})}
  const bl=blocked();
  free=cells.filter(c=>c.x>R&&c.x<W-R&&c.y>R&&c.y<H-R&&!bl.some(b=>c.x>b.l&&c.x<b.r&&c.y>b.t&&c.y<b.b));
}
// responder shapes: person (dot), drone (small fast triangle), team (larger square)
function shape(kind,x,y){
  if(kind==='drone')return el('polygon',{points:'0,-6 5.5,4 -5.5,4',fill:STROBE,transform:`translate(${x},${y})`,opacity:0},gMove);
  if(kind==='team')return el('rect',{x:-5.5,y:-5.5,width:11,height:11,rx:2,fill:STROBE,transform:`translate(${x},${y})`,opacity:0},gMove);
  if(kind==='caller')return el('circle',{cx:0,cy:0,r:4.2,fill:'none',stroke:AMBER,'stroke-width':1.8,transform:`translate(${x},${y})`,opacity:0},gMove);
  return el('circle',{cx:0,cy:0,r:4.5,fill:STROBE,transform:`translate(${x},${y})`,opacity:0},gMove);
}
const chain=document.querySelector('.chain'),EV=chain.dataset.events.split('|'),BL=chain.dataset.block;
let height=329840,queue=[],regq=[],btimer=null,lastEv=false;
function block(ev,animate){
  if(getComputedStyle(chain).display==='none')return;
  const b=document.createElement('div');b.className='b'+(ev==null?'':ev<3?' ev':' reg');
  b.innerHTML='<div class="h">'+BL+' '+(height++).toLocaleString(document.documentElement.lang)+'</div>'+(ev!=null?'<div class="e">'+EV[ev]+'</div>':'');
  chain.appendChild(b);
  if(animate){const h=b.offsetHeight;b.animate([{marginTop:(-h)+'px',opacity:0},{marginTop:'18px',opacity:1}],{duration:700,easing:'cubic-bezier(.3,.1,.2,1)'});
    if(ev!=null&&ev<3)b.animate([{boxShadow:'0 0 0 3px rgba(243,167,59,.55)'},{boxShadow:'0 0 0 0 rgba(243,167,59,0)'}],{duration:1600,delay:300})}
  while(chain.children.length>9)chain.firstChild.remove();
}
// someone joins, before any emergency: a caller escrows an offer, a responder posts a bond. The cell
// outline lights blue (alerts light amber), the icon pops in, and then stays on the map as one of the
// people already there, fading slowly; the deposit lands in the chain column
function register(k,already){
  if(!free.length)return;const c=free[Math.floor(Math.random()*free.length)];
  const x=c.x+rand(-R*.3,R*.3),y=c.y+rand(-R*.3,R*.3);
  const m=shape(k,x,y);gUsers.appendChild(m);
  if(already){const d=rand(12000,26000);m.animate([{opacity:.35},{opacity:0}],{duration:d,fill:'forwards'});setTimeout(()=>m.remove(),d+200);return}
  c.p.animate([{stroke:STROBE,strokeOpacity:.9},{stroke:GRID,strokeOpacity:1}],{duration:2200,easing:'ease-out'});
  m.animate([{opacity:0,transform:`translate(${x}px,${y}px) scale(0)`},{opacity:1,offset:.06,transform:`translate(${x}px,${y}px) scale(1.5)`},
             {opacity:1,offset:.12,transform:`translate(${x}px,${y}px) scale(1)`},{opacity:.9,offset:.2,transform:`translate(${x}px,${y}px) scale(1)`},
             {opacity:.35,offset:.32,transform:`translate(${x}px,${y}px) scale(1)`},{opacity:0,transform:`translate(${x}px,${y}px) scale(1)`}],
            {duration:28000,easing:'linear',fill:'forwards'});
  setTimeout(()=>m.remove(),28200);
  while(gUsers.childNodes.length>18)gUsers.firstChild.remove();
}
function joins(){clearTimeout(rtimer);if(!running||!visible||document.hidden)return;
  if(regq.length<2)regq.push(['caller','caller','person','person','person','drone','team'][Math.floor(Math.random()*7)]);rtimer=setTimeout(joins,rand(2200,4200))}
function tick(){clearTimeout(btimer);if(!running||!visible||document.hidden)return;
  // most blocks carry nothing of Bitaid's; never two events in a row
  let ev=null;if(!lastEv){if(queue.length&&Math.random()<.7)ev=queue.shift();else if(regq.length){const k=regq.shift();register(k);ev=k==='caller'?3:4}}
  lastEv=ev!=null;block(ev,true);btimer=setTimeout(tick,rand(1300,1800))}
function oneCase(){
  if(!free.length)return;
  // weighted toward the middle of the open area, so wide screens are not all right-side
  const xs=free.map(f=>f.x),lo=Math.min(...xs),hi=Math.max(...xs),mid=lo+(hi-lo)*.42,spread=Math.max(R*3,(hi-lo)*.32);
  const w=free.map(f=>Math.exp(-(((f.x-mid)/spread)**2))),tot=w.reduce((a,b)=>a+b,0);let rr=Math.random()*tot,c=free[0];
  for(let k=0;k<free.length;k++){rr-=w[k];if(rr<=0){c=free[k];break}}
  const cell=el('polygon',{points:hexPts(c.x,c.y,R*0.94),fill:AMBER,'fill-opacity':0,stroke:AMBER,'stroke-opacity':0},gMarks);
  const halo=el('circle',{cx:c.x,cy:c.y,r:R*0.4,fill:'none',stroke:AMBER,'stroke-width':2,opacity:0},gMove);
  // the alert: the cell lights, a pulse rings out through the neighbouring cells
  cell.animate([{fillOpacity:0},{fillOpacity:.95,offset:.15},{fillOpacity:.75}],{duration:1400,fill:'forwards'});
  setTimeout(()=>queue.push(0),900);setTimeout(()=>queue.push(1),3300);
  halo.animate([{r:R*0.5,opacity:.9},{r:R*4.5,opacity:0}],{duration:1700,easing:'ease-out',iterations:2});
  cells.forEach(o=>{const d=Math.hypot(o.x-c.x,o.y-c.y);if(d<R*6)o.p.animate([{stroke:AMBER,strokeOpacity:.85},{stroke:GRID,strokeOpacity:1}],{duration:1100,delay:d*1.8,easing:'ease-out'})});
  // help arrives: a drone first, then people and sometimes a team, from different directions
  const kinds=['drone','person','person'];if(Math.random()<.6)kinds.push('team');
  const base=rand(0,Math.PI*2),movers=[];
  // each starts wherever it happened to be, near or far; the nearest arrive first
  kinds.forEach((k,i)=>{const a=base+i*(Math.PI*2/kinds.length)+rand(-.4,.4),dist=R*(k==='drone'?rand(2.5,7):k==='team'?rand(2.2,6):rand(1.1,5.5));
    const sx=c.x+Math.cos(a)*dist,sy=c.y+Math.sin(a)*dist,fx=c.x+Math.cos(a)*R*.42,fy=c.y+Math.sin(a)*R*.42;
    const m=shape(k,sx,sy),rot=k==='drone'?` rotate(${(a*180/Math.PI)-90})`:'';
    const dur=Math.max(650,dist/(k==='drone'?R/230:k==='team'?R/520:R/560)),delay=700+(k==='drone'?0:rand(250,900));
    m.animate([{opacity:0,transform:`translate(${sx}px,${sy}px)${rot.replace(/\(([-\d.]+)\)/,'($1deg)')}`},
               {opacity:1,offset:.12,transform:`translate(${sx}px,${sy}px)${rot.replace(/\(([-\d.]+)\)/,'($1deg)')}`},
               {opacity:1,transform:`translate(${fx}px,${fy}px)${rot.replace(/\(([-\d.]+)\)/,'($1deg)')}`}],
              {duration:dur,delay,easing:'cubic-bezier(.3,.1,.2,1)',fill:'forwards'});
    movers.push(m)});
  // the case closes: help leaves, the cell settles into a faint resolved mark that stays
  setTimeout(()=>{queue.push(2);movers.forEach(m=>m.animate([{opacity:1},{opacity:0}],{duration:900,fill:'forwards'}));
    cell.animate([{fillOpacity:.75,strokeOpacity:0},{fillOpacity:.07,strokeOpacity:.35}],{duration:1400,fill:'forwards',easing:'ease-out'});
    setTimeout(()=>{movers.forEach(m=>m.remove());halo.remove()},1000);
    // keep only the last dozen resolved marks
    while(gMarks.childNodes.length>12)gMarks.firstChild.remove();
  },5200);
}
function loop(){clearTimeout(timer);if(!running||!visible||document.hidden)return;oneCase();
  timer=setTimeout(loop,first?7600:rand(5800,7800));first=false}
function start(){build();chain.innerHTML='';queue=[];regq=[];['caller','person','person','drone','team','caller'].forEach(k=>register(k,true));height=329840;[4,null,null,3,null,null].forEach(e=>block(e,false));
  if(reduce){ // a still frame: one alert with help on its way, no motion
    hero.classList.add('ready');const c=free[Math.floor(free.length/2)]||cells[0];
    el('polygon',{points:hexPts(c.x,c.y,R*0.94),fill:AMBER,'fill-opacity':.8},gMarks);
    [['drone',-1.2],['person',.9],['person',2.6]].forEach(([k,a])=>{const m=shape(k,c.x+Math.cos(a)*R*1.3,c.y+Math.sin(a)*R*1.3);m.setAttribute('opacity',1)});
    [3,4,0,null,1,2].forEach(e=>block(e,false));return}
  running=true;first=true;setTimeout(()=>hero.classList.add('ready'),1500);loop();btimer=setTimeout(tick,1200);rtimer=setTimeout(joins,600)}
new IntersectionObserver(es=>{const was=visible;visible=es[0].isIntersecting;if(visible&&!was&&running){loop();tick();joins()}else if(!visible){clearTimeout(timer);clearTimeout(btimer);clearTimeout(rtimer)}}).observe(hero);
document.addEventListener('visibilitychange',()=>{if(document.hidden){clearTimeout(timer);clearTimeout(btimer);clearTimeout(rtimer)}else if(running&&visible){timer=setTimeout(loop,800);btimer=setTimeout(tick,1200);rtimer=setTimeout(joins,600)}});
let rt;addEventListener('resize',()=>{clearTimeout(rt);rt=setTimeout(()=>{if(Math.abs(hero.clientWidth-W)>40){clearTimeout(timer);clearTimeout(btimer);clearTimeout(rtimer);start()}},300)});
start();
const dn=document.querySelector('a.down');addEventListener('scroll',()=>{dn.style.opacity=scrollY>40?0:1},{passive:true});
})();
'''


WRENCH = (
    '<svg class="wrench" viewBox="0 0 200 150" role="img" aria-label="a $5 wrench">'
    '<g fill="none" stroke="currentColor" stroke-width="3" stroke-linejoin="round" stroke-linecap="round">'
    '<path d="M48 104 L132 40"/><path d="M56 114 L140 50"/>'
    '<path d="M48 104 C30 104 18 114 20 128 L34 122 L42 132 L30 142 C46 146 60 132 56 114"/>'
    '<path d="M132 40 C130 26 142 14 156 16 C170 18 178 32 172 46 C166 58 150 60 140 50"/>'
    '<circle cx="156" cy="35" r="9"/>'
    '<path d="M150 58 C146 72 140 80 128 88" stroke-width="1.6"/>'
    '</g>'
    '<g transform="rotate(-12 116 102)"><path class="tag" d="M100 88 L136 88 L146 100 L136 112 L100 112 Z"/>'
    '<circle cx="134" cy="100" r="3" fill="#141a3a"/>'
    '<text x="104" y="106">$5</text></g>'
    '</svg>')

# Archimedes' lever, in the wrench's line: a long beam pressed down at the left, a fulcrum near the
# right, and the earth (in amber, as the wrench's tag) on the short end
LEVER = (
    '<svg viewBox="2 14 196 118" role="img" aria-label="a lever moving the earth">'
    '<g fill="none" stroke="currentColor" stroke-width="3" stroke-linejoin="round" stroke-linecap="round">'
    '<path d="M10 126 C40 122 70 128 100 124 C130 120 160 127 192 124"/>'
    '<path d="M18 54 L176 116"/><path d="M15 61 L173 123" stroke-width="1.6"/>'
    '<path d="M137 125 L149 106 L161 125"/>'
    '<path d="M18 22 L18 44 M11 36 L18 45 L25 36" stroke-width="2.2"/>'
    '</g>'
    '<g class="globe" fill="none" stroke-width="3"><circle cx="164" cy="84" r="25"/>'
    '<ellipse cx="164" cy="84" rx="11" ry="25" stroke-width="1.8"/><path d="M139 84 L189 84 M143 71 L185 71 M143 97 L185 97" stroke-width="1.8"/></g>'
    '</svg>')

JS2 = r'''
(function(){
const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
document.documentElement.classList.add('js');
const ol=document.querySelector('ol.steps'),fill=ol&&ol.querySelector('.fill'),lis=ol?[...ol.querySelectorAll('li')]:[];
function route(){if(!ol)return;const r=ol.getBoundingClientRect(),y=innerHeight*0.6;
  const rt=ol.querySelector('.route'),total=rt.offsetHeight;let h=Math.max(0,Math.min(total,y-r.top-30));
  if(reduce)h=total;fill.style.height=h+'px';lis.forEach(li=>{li.classList.toggle('on',reduce||li.getBoundingClientRect().top<y)})}
addEventListener('scroll',route,{passive:true});addEventListener('resize',route);route();
const fig=document.querySelector('figure.lever'),sweep=fig&&fig.querySelector('.sweep');
const nums=[...document.querySelectorAll('ol.runs .score')].map(e=>{const t=e.firstChild;const n=t&&t.nodeType===3?parseInt(t.textContent,10):NaN;return isNaN(n)?null:{e,t,n}}).filter(Boolean);
if(reduce){if(fig)fig.classList.add('on');return}
const io=new IntersectionObserver(es=>es.forEach(en=>{if(!en.isIntersecting)return;io.unobserve(en.target);
  if(en.target===fig){fig.classList.add('on');const t0=performance.now();(function f(t){const k=Math.min(1,(t-t0)/1400);sweep.setAttribute('width',(400*(1-Math.pow(1-k,3))).toFixed(1));if(k<1)requestAnimationFrame(f)})(t0)}
  else{const o=nums.find(o=>o.e===en.target);if(!o)return;const t0=performance.now();
    (function f(t){const k=Math.min(1,(t-t0)/900);o.t.textContent=Math.round(o.n*(1-Math.pow(1-k,3)));if(k<1)requestAnimationFrame(f)})(t0)}}),{threshold:.35});
if(fig){sweep.setAttribute('width','0');io.observe(fig)}
nums.forEach(o=>{o.t.textContent='0';io.observe(o.e)});
})();
'''


def lever_svg():
    # 1,000 people: 40 x 25 dots
    s = ['<svg viewBox="0 0 400 250" role="img" aria-hidden="true"><defs><clipPath id="sw"><rect class="sweep" x="0" y="0" height="250" width="400"/></clipPath></defs><g clip-path="url(#sw)">']
    for i in range(1000):
        x, y = 5 + (i % 40) * 10, 5 + (i // 40) * 10
        s.append(f'<circle cx="{x}" cy="{y}" r="2.6" fill="#a9c4ff"/>')
    s.append('</g></svg>')
    return ''.join(s)


def build(k):
    c = L[k]
    md = open(os.path.join(HERE, k + '.md')).read()
    lines = md.split('\n')
    title = lines[0].lstrip('# ').strip()
    rest = '\n'.join(lines[1:]).strip().split('\n\n')
    byline_md, lead_md, body_md = rest[0], rest[1], '\n\n'.join(rest[2:])
    title_main = title.split(': ', 1)[1] if ': ' in title else title
    title_main = title_main[0].upper() + title_main[1:]
    md_ = lambda t: markdown.markdown(t, extensions=['tables'])
    by = md_(byline_md)[3:-4]
    lead = md_(lead_md)[3:-4]
    body = md_(body_md)
    # what already runs: the table becomes a list of runs, each led by its score
    rows = [r for r in body_md.split('\n') if r.startswith('|')][2:]
    items = []
    for r in rows:
        date, where, what, res = [x.strip() for x in r.strip('|').split('|')]
        link = re.match(r'\[(.+?)\]\((.+?)\)', res)
        text, href = (link.group(1), link.group(2)) if link else (res, None)
        n = re.match(r'(\d+) (passed|superadas), (0 (?:failed|fallidas))', text)
        if n:
            inner = f'{n.group(1)}<small>{n.group(2)}, {n.group(3)}</small>'; cls = 'score'
        else:
            inner = text; cls = 'score text' + (' pending' if text in ('Running now', 'En curso') else '')
        score = f'<a class="{cls}" href="{href}">{inner}</a>' if href else f'<div class="{cls}">{inner}</div>'
        items.append(f'<li>{score}<div><div class="meta">{date}, {where}</div><div class="what">{md_(what)[3:-4]}</div></div></li>')
    body = re.sub(r'<table>.*?</table>', '<ol class="runs">' + ''.join(items) + '</ol>', body, flags=re.S)
    body = body.replace('<ol>', '<ol class="steps">', 1)
    # the claims (the list of the section on cheating) side by side
    sec = body.split('<h2>')
    for i, part in enumerate(sec):
        if part.startswith(('Why cheating', 'Por qué hacer trampa')):
            sec[i] = part.replace('<ul>', '<ul class="claims">', 1)
    body = '<h2>'.join(sec)
    # the lever figure after the paragraph with the numbers
    fig = (f'<figure class="lever"><div class="row"><div>{lever_svg()}<div class="k"><b>{c["people"]}</b></div></div>'
           f'<div class="offer"><svg viewBox="0 0 100 100" width="96" height="96" aria-hidden="true"><polygon points="50,4 90,27 90,73 50,96 10,73 10,27" fill="#f3a73b"/></svg>'
           f'<div class="big">{"$8,000" if k == "en" else "8.000 $"}</div><div class="k">{c["offer"]}</div></div></div>'
           f'<figcaption>{c["figcap"]}</figcaption></figure>')
    m = re.search(r'<p>[^<]*(?:\$8,000|8\.000 \$)[^<]*</p>', body)
    body = body[:m.end()] + fig + body[m.end():]
    # each section: its heading in the left column, its text in the right
    parts = body.split('<h2>')[1:]
    def side(x, i):
        art = WRENCH if i == 0 else (f'<figure class="archimedes">{LEVER}<blockquote>{c["quote"]}<cite>{c["cite"]}</cite></blockquote></figure>' if i == 1 else '')
        return '<section><div class="side"><h2>' + x.replace('</h2>', '</h2>' + art + '</div><div class="body">', 1) + '</div></section>'
    body = ''.join(side(x, i) for i, x in enumerate(parts))
    body = re.sub(r'<p>(Bitaid (?:does not declare|no decreta)[^<]*)</p>', r'<p class="statement">\1</p>', body)
    body = body.replace('<ol class="steps">', '<ol class="steps"><span class="route" aria-hidden="true"></span><span class="fill" aria-hidden="true"></span>', 1)
    up = c['up']
    nav = ''.join(f'<a href="{up}{h}">{t}</a>' for t, h in c['nav']) + f'<a class="lang" href="{c["other"]}" hreflang="{"es" if k == "en" else "en"}">{c["other_label"]}</a>'
    url = 'https://bitaid-whitepaper.pages.dev/' + c['path'].replace('index.html', '')
    html = f'''<!DOCTYPE html>
<html lang="{c['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{c['title']}</title>
<meta name="description" content="{c['desc']}">
<meta property="og:title" content="{c['title']}">
<meta property="og:description" content="{c['desc']}">
<meta property="og:type" content="article">
<meta property="og:url" content="{url}">
<meta name="twitter:card" content="summary">
<meta name="twitter:site" content="@fiatstandard">
<meta name="theme-color" content="#141a3a">
<link rel="alternate" hreflang="en" href="https://bitaid-whitepaper.pages.dev/brief/">
<link rel="alternate" hreflang="es" href="https://bitaid-whitepaper.pages.dev/brief/es/">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@600;700;800&family=Literata:opsz,wght@7..72,400;7..72,650&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<a class="skip" href="#text">{c['skip']}</a>
<header class="hero">
<svg class="map" aria-hidden="true"></svg>
<div class="chain" aria-hidden="true" data-events="{'|'.join(c['events'])}" data-block="{c['block']}"></div>
<nav>{nav}</nav>
<div class="words">
<h1>{title_main}</h1>
<p class="lead">{lead}</p>
<p class="by">{by}</p>
<div class="key" aria-hidden="true"><span><svg viewBox="-6 -6 12 12"><circle r="4.2" fill="none" stroke="#f3a73b" stroke-width="1.8"/></svg>{c['key'][0]}</span><span><svg viewBox="-6 -7 12 12"><polygon points="0,-6 5.5,4 -5.5,4" fill="#a9c4ff"/></svg>{c['key'][1]}</span><span><svg viewBox="-6 -6 12 12"><circle r="4.5" fill="#a9c4ff"/></svg>{c['key'][2]}</span><span><svg viewBox="-6 -6 12 12"><rect x="-5.5" y="-5.5" width="11" height="11" rx="2" fill="#a9c4ff"/></svg>{c['key'][3]}</span></div>
</div>

<a class="down" href="#text">{c['down']}<svg viewBox="0 0 22 14" aria-hidden="true"><polyline points="2,2 11,11 20,2" fill="none" stroke="currentColor" stroke-width="2.2"/></svg></a>
</header>
<main id="text">
{body}
</main>
<script>{JS}</script>
<script>{JS2}</script>
</body>
</html>
'''
    out = os.path.join(SITE, c['path'])
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w').write(html)
    print(out, len(html))


for k in L:
    build(k)
