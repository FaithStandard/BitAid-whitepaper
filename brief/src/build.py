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
   key=('drone','responder','team'), skip='Skip to the brief'),
 'es': dict(path='brief/es/index.html', up='../../', other='../', other_label='English', lang='es',
   title='Bitaid en dos páginas',
   desc='Ayuda en emergencias, pagada de persona a persona en Bitcoin: el problema, la palanca del seguro, cómo se resuelve un caso, por qué hacer trampa no compensa y lo que ya funciona en la signet pública de Bitcoin.',
   nav=[('Whitepaper', 'index.html'), ('Especificación', 'bitaid_v6_specification.html'), ('Fundamentos', 'bitaid_v6_foundations.html')],
   people='1.000 personas pagando 2 $ al mes', offer='la oferta que cada una puede pedir',
   figcap='Las ofertas en depósito no cuestan nada hasta que se usan, y las emergencias rara vez golpean a las mismas personas a la vez: un mismo depósito respalda muchas ofertas.',
   key=('dron','respondedor','equipo'), skip='Ir al texto'),
}

CSS = r'''
:root{--night:#141a3a;--night2:#1c2350;--grid:#2b3470;--ink:#ecebf6;--soft:#b9bbd6;--amber:#f3a73b;--amber2:#ffcf7a;--strobe:#a9c4ff;--paper:#f6f5fb;--text:#1b1f3d;--muted:#565b7d;--rule:#d9daea;--row:#eeeef7}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--paper:#171b38;--text:#e7e7f3;--muted:#a3a6c6;--rule:#2d3466;--row:#1e2346}}
:root[data-theme="dark"]{--paper:#171b38;--text:#e7e7f3;--muted:#a3a6c6;--rule:#2d3466;--row:#1e2346}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--paper);color:var(--text);font-family:"Literata",Georgia,serif;font-size:19px;line-height:1.62;font-optical-sizing:auto}
a{color:inherit;text-decoration-thickness:1px;text-underline-offset:3px}
a:focus-visible,button:focus-visible{outline:3px solid var(--amber);outline-offset:3px;border-radius:2px}
.skip{position:absolute;left:-9999px}.skip:focus{left:16px;top:16px;z-index:9;background:var(--amber);color:#141a3a;padding:.4em .8em}
/* hero: the night map */
.hero{position:relative;min-height:min(100svh,940px);background:var(--night);color:var(--ink);overflow:hidden;display:flex;flex-direction:column}
.hero svg.map{position:absolute;inset:0;width:100%;height:100%}
.hero nav{position:relative;z-index:2;display:flex;flex-wrap:wrap;gap:.3em 1.4em;padding:22px 28px;font-family:"Big Shoulders Display",sans-serif;font-weight:600;font-size:17px;letter-spacing:.02em}
.hero nav a{text-decoration:none;color:var(--soft)}.hero nav a:hover{color:var(--ink)}
.hero nav .lang{margin-left:auto;color:var(--amber2)}
.hero .words{position:relative;z-index:2;margin-top:auto;padding:0 28px 56px;max-width:1080px}
.hero h1{font-family:"Big Shoulders Display",sans-serif;font-weight:800;font-size:clamp(52px,9.4vw,132px);line-height:.9;letter-spacing:-.005em;margin:0 0 .28em;max-width:11ch;text-wrap:balance}
.hero .lead{font-size:clamp(17px,1.6vw,21px);line-height:1.55;max-width:56ch;color:var(--soft);margin:0}
.hero .by{margin-top:1.4em;font-family:"Big Shoulders Display",sans-serif;font-size:18px;color:var(--soft)}
.hero .by a{color:var(--amber2)}
.hero .key{display:flex;flex-wrap:wrap;gap:.4em 1.2em;align-items:center;margin-top:1.1em;font:600 15px "Big Shoulders Display",sans-serif;color:var(--soft)}
.hero .key span{display:inline-flex;align-items:center;gap:.4em}
.hero .key svg{width:12px;height:12px}
.words>*{opacity:0;transform:translateY(10px);transition:opacity .9s ease,transform .9s ease}
.hero.ready .words>*{opacity:1;transform:none}
.hero.ready .words>*:nth-child(2){transition-delay:.15s}.hero.ready .words>*:nth-child(3){transition-delay:.3s}.hero.ready .words>*:nth-child(4){transition-delay:.45s}
/* the text */
main{max-width:720px;margin:0 auto;padding:64px 24px 96px}
main h2{font-family:"Big Shoulders Display",sans-serif;font-weight:800;font-size:clamp(34px,4.4vw,46px);line-height:1;margin:2.2em 0 .5em;letter-spacing:-.005em}
main h2:first-child{margin-top:0}
main p{margin:0 0 1em;hyphens:auto}
main ol{padding-left:0;list-style:none;counter-reset:step;margin:1.2em 0}
main ol li{counter-increment:step;position:relative;padding-left:3.1em;margin:0 0 1em}
main ol li::before{content:counter(step);position:absolute;left:0;top:-.08em;font:800 1.75em/1 "Big Shoulders Display",sans-serif;color:var(--amber);width:1.4em;text-align:right}
main ul{padding-left:1.1em;margin:1em 0}main ul li{margin:0 0 .75em}main ul li::marker{color:var(--amber)}
main strong{font-weight:650}
.tablewrap{overflow-x:auto;margin:1.6em -24px;padding:0 24px}
table{border-collapse:collapse;width:100%;min-width:640px;font-size:15.5px;line-height:1.45}
th{font-family:"Big Shoulders Display",sans-serif;font-weight:700;font-size:17px;text-align:left;padding:.5em .7em;border-bottom:2px solid var(--text)}
td{padding:.65em .7em;border-bottom:1px solid var(--rule);vertical-align:top}
tbody tr:first-child td{background:var(--row)}
td:last-child{white-space:nowrap}
/* the lever figure */
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
@media (max-width:620px){body{font-size:17.5px}.hero nav{padding:18px 16px}.hero .words{padding:0 16px 64px}main{padding:48px 16px 80px}.tablewrap{margin:1.4em -16px;padding:0 16px}figure.lever{padding:20px}figure.lever .row{grid-template-columns:1fr}figure.lever .offer{width:auto}}
@media (max-width:620px){table{min-width:0}thead{display:none}table,tbody,tr,td{display:block}tr{padding:.9em 0;border-bottom:1px solid var(--rule)}td{border:0;padding:.1em 0}tbody tr:first-child td{background:none}tbody tr:first-child{background:var(--row);margin:0 -16px;padding:.9em 16px}td:nth-child(1),td:nth-child(2){display:inline;font-family:"Big Shoulders Display",sans-serif;font-weight:700;font-size:16px;color:var(--muted)}td:nth-child(1)::after{content:" \2014 "}td:last-child{white-space:normal;font-weight:650;margin-top:.3em}.tablewrap{overflow:visible}}
@media (prefers-reduced-motion:reduce){.words>*{transition:none}}
footer{max-width:720px;margin:0 auto;padding:0 24px 64px;color:var(--muted);font-size:15px}
'''

JS = r'''
(function(){
const svg=document.querySelector('svg.map'),hero=document.querySelector('.hero'),NS='http://www.w3.org/2000/svg';
const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
const AMBER='#f3a73b',STROBE='#a9c4ff',GRID='#2b3470';
let W,H,R,dx,dy,cells=[],free=[],gCells,gMarks,gMove,running=false,visible=true,timer=null,first=true;
function el(n,a,p){const e=document.createElementNS(NS,n);for(const k in a)e.setAttribute(k,a[k]);if(p)p.appendChild(e);return e}
function hexPts(x,y,r){let p=[];for(let i=0;i<6;i++){const a=Math.PI/180*(60*i-30);p.push((x+r*Math.cos(a)).toFixed(1)+','+(y+r*Math.sin(a)).toFixed(1))}return p.join(' ')}
function rand(a,b){return a+Math.random()*(b-a)}
// areas the text covers, so alerts never sit under words
function blocked(){const h=hero.getBoundingClientRect(),out=[];
  hero.querySelectorAll('nav,.words>*').forEach(e=>{const r=e.getBoundingClientRect();if(r.width)out.push({l:r.left-h.left-R,t:r.top-h.top-R,r:r.right-h.left+R,b:r.bottom-h.top+R})});return out}
function build(){
  svg.innerHTML='';cells=[];W=hero.clientWidth;H=hero.clientHeight;R=Math.max(24,Math.min(42,W/34));
  dx=Math.sqrt(3)*R;dy=1.5*R;svg.setAttribute('viewBox','0 0 '+W+' '+H);
  gCells=el('g',{},svg);gMarks=el('g',{},svg);gMove=el('g',{},svg);
  for(let r=-1;r*dy<H+R;r++)for(let c=-1;;c++){const x=c*dx+(r%2?dx/2:0),y=r*dy;if(x>W+R)break;
    cells.push({x,y,p:el('polygon',{points:hexPts(x,y,R*0.94),fill:'none',stroke:GRID,'stroke-width':1},gCells)})}
  const bl=blocked();
  free=cells.filter(c=>c.x>R&&c.x<W-R&&c.y>R&&c.y<H-R&&!bl.some(b=>c.x>b.l&&c.x<b.r&&c.y>b.t&&c.y<b.b));
}
// responder shapes: person (dot), drone (small fast triangle), team (larger square)
function shape(kind,x,y){
  if(kind==='drone')return el('polygon',{points:'0,-6 5.5,4 -5.5,4',fill:STROBE,transform:`translate(${x},${y})`,opacity:0},gMove);
  if(kind==='team')return el('rect',{x:-5.5,y:-5.5,width:11,height:11,rx:2,fill:STROBE,transform:`translate(${x},${y})`,opacity:0},gMove);
  return el('circle',{cx:0,cy:0,r:4.5,fill:STROBE,transform:`translate(${x},${y})`,opacity:0},gMove);
}
function oneCase(){
  if(!free.length)return;
  const c=free[Math.floor(Math.random()*free.length)];
  const cell=el('polygon',{points:hexPts(c.x,c.y,R*0.94),fill:AMBER,'fill-opacity':0,stroke:AMBER,'stroke-opacity':0},gMarks);
  const halo=el('circle',{cx:c.x,cy:c.y,r:R*0.4,fill:'none',stroke:AMBER,'stroke-width':2,opacity:0},gMove);
  // the alert: the cell lights, a pulse rings out through the neighbouring cells
  cell.animate([{fillOpacity:0},{fillOpacity:.95,offset:.15},{fillOpacity:.75}],{duration:1400,fill:'forwards'});
  halo.animate([{r:R*0.5,opacity:.9},{r:R*4.5,opacity:0}],{duration:1700,easing:'ease-out',iterations:2});
  cells.forEach(o=>{const d=Math.hypot(o.x-c.x,o.y-c.y);if(d<R*6)o.p.animate([{stroke:AMBER,strokeOpacity:.85},{stroke:GRID,strokeOpacity:1}],{duration:1100,delay:d*1.8,easing:'ease-out'})});
  // help arrives: a drone first, then people and sometimes a team, from different directions
  const kinds=['drone','person','person'];if(Math.random()<.6)kinds.push('team');
  const base=rand(0,Math.PI*2),movers=[];
  kinds.forEach((k,i)=>{const a=base+i*(Math.PI*2/kinds.length)+rand(-.4,.4),dist=R*(k==='drone'?rand(5,7):rand(3.2,5));
    const sx=c.x+Math.cos(a)*dist,sy=c.y+Math.sin(a)*dist,fx=c.x+Math.cos(a)*R*.42,fy=c.y+Math.sin(a)*R*.42;
    const m=shape(k,sx,sy),rot=k==='drone'?` rotate(${(a*180/Math.PI)-90})`:'';
    const dur=k==='drone'?1500:k==='team'?2600:2300,delay=700+(k==='drone'?0:500+i*260);
    m.animate([{opacity:0,transform:`translate(${sx}px,${sy}px)${rot.replace(/\(([-\d.]+)\)/,'($1deg)')}`},
               {opacity:1,offset:.12,transform:`translate(${sx}px,${sy}px)${rot.replace(/\(([-\d.]+)\)/,'($1deg)')}`},
               {opacity:1,transform:`translate(${fx}px,${fy}px)${rot.replace(/\(([-\d.]+)\)/,'($1deg)')}`}],
              {duration:dur,delay,easing:'cubic-bezier(.3,.1,.2,1)',fill:'forwards'});
    movers.push(m)});
  // the case closes: help leaves, the cell settles into a faint resolved mark that stays
  setTimeout(()=>{movers.forEach(m=>m.animate([{opacity:1},{opacity:0}],{duration:900,fill:'forwards'}));
    cell.animate([{fillOpacity:.75,strokeOpacity:0},{fillOpacity:.07,strokeOpacity:.35}],{duration:1400,fill:'forwards',easing:'ease-out'});
    setTimeout(()=>{movers.forEach(m=>m.remove());halo.remove()},1000);
    // keep only the last dozen resolved marks
    while(gMarks.childNodes.length>12)gMarks.firstChild.remove();
  },5200);
}
function loop(){clearTimeout(timer);if(!running||!visible||document.hidden)return;oneCase();
  timer=setTimeout(loop,first?7600:rand(5800,7800));first=false}
function start(){build();
  if(reduce){ // a still frame: one alert with help on its way, no motion
    hero.classList.add('ready');const c=free[Math.floor(free.length/2)]||cells[0];
    el('polygon',{points:hexPts(c.x,c.y,R*0.94),fill:AMBER,'fill-opacity':.8},gMarks);
    [['drone',-1.2],['person',.9],['person',2.6]].forEach(([k,a])=>{const m=shape(k,c.x+Math.cos(a)*R*1.3,c.y+Math.sin(a)*R*1.3);m.setAttribute('opacity',1)});return}
  running=true;first=true;setTimeout(()=>hero.classList.add('ready'),1500);loop()}
new IntersectionObserver(es=>{const was=visible;visible=es[0].isIntersecting;if(visible&&!was&&running)loop();else if(!visible)clearTimeout(timer)}).observe(hero);
document.addEventListener('visibilitychange',()=>{if(document.hidden)clearTimeout(timer);else if(running&&visible)timer=setTimeout(loop,800)});
let rt;addEventListener('resize',()=>{clearTimeout(rt);rt=setTimeout(()=>{if(Math.abs(hero.clientWidth-W)>40){clearTimeout(timer);start()}},300)});
start();
})();
'''


def lever_svg():
    # 1,000 people: 40 x 25 dots
    s = ['<svg viewBox="0 0 400 250" role="img" aria-hidden="true">']
    for i in range(1000):
        x, y = 5 + (i % 40) * 10, 5 + (i // 40) * 10
        s.append(f'<circle cx="{x}" cy="{y}" r="2.6" fill="#a9c4ff"/>')
    s.append('</svg>')
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
    body = body.replace('<table>', '<div class="tablewrap"><table>').replace('</table>', '</table></div>')
    # the lever figure after the paragraph with the numbers
    fig = (f'<figure class="lever"><div class="row"><div>{lever_svg()}<div class="k"><b>{c["people"]}</b></div></div>'
           f'<div class="offer"><svg viewBox="0 0 100 100" width="96" height="96" aria-hidden="true"><polygon points="50,4 90,27 90,73 50,96 10,73 10,27" fill="#f3a73b"/></svg>'
           f'<div class="big">{"$8,000" if k == "en" else "8.000 $"}</div><div class="k">{c["offer"]}</div></div></div>'
           f'<figcaption>{c["figcap"]}</figcaption></figure>')
    m = re.search(r'<p>[^<]*(?:\$8,000|8\.000 \$)[^<]*</p>', body)
    body = body[:m.end()] + fig + body[m.end():]
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
<nav>{nav}</nav>
<div class="words">
<h1>{title_main}</h1>
<p class="lead">{lead}</p>
<p class="by">{by}</p>
<div class="key" aria-hidden="true"><span><svg viewBox="-6 -7 12 12"><polygon points="0,-6 5.5,4 -5.5,4" fill="#a9c4ff"/></svg>{c['key'][0]}</span><span><svg viewBox="-6 -6 12 12"><circle r="4.5" fill="#a9c4ff"/></svg>{c['key'][1]}</span><span><svg viewBox="-6 -6 12 12"><rect x="-5.5" y="-5.5" width="11" height="11" rx="2" fill="#a9c4ff"/></svg>{c['key'][2]}</span></div>
</div>

</header>
<main id="text">
{body}
</main>
<script>{JS}</script>
</body>
</html>
'''
    out = os.path.join(SITE, c['path'])
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w').write(html)
    print(out, len(html))


for k in L:
    build(k)
