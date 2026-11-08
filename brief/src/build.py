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
   replay='Replay', skip='Skip to the brief'),
 'es': dict(path='brief/es/index.html', up='../../', other='../', other_label='English', lang='es',
   title='Bitaid en dos páginas',
   desc='Ayuda en emergencias, pagada de persona a persona en Bitcoin: el problema, la palanca del seguro, cómo se resuelve un caso, por qué hacer trampa no compensa y lo que ya funciona en la signet pública de Bitcoin.',
   nav=[('Whitepaper', 'index.html'), ('Especificación', 'bitaid_v6_specification.html'), ('Fundamentos', 'bitaid_v6_foundations.html')],
   people='1.000 personas pagando 2 $ al mes', offer='la oferta que cada una puede pedir',
   figcap='Las ofertas en depósito no cuestan nada hasta que se usan, y las emergencias rara vez golpean a las mismas personas a la vez: un mismo depósito respalda muchas ofertas.',
   replay='Repetir', skip='Ir al texto'),
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
.hero button.replay{position:absolute;z-index:2;right:24px;bottom:24px;background:none;border:1px solid var(--grid);color:var(--soft);font:600 15px "Big Shoulders Display",sans-serif;padding:.35em .9em;border-radius:3px;cursor:pointer}
.hero button.replay:hover{color:var(--ink);border-color:var(--soft)}
.words>*{opacity:0;transform:translateY(10px);transition:opacity .9s ease,transform .9s ease}
.hero.ready .words>*{opacity:1;transform:none}
.hero.ready .words>*:nth-child(2){transition-delay:.15s}.hero.ready .words>*:nth-child(3){transition-delay:.3s}
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
let W,H,R,cx,cy,cells=[],timers=[];
function hex(x,y,r){let p=[];for(let i=0;i<6;i++){const a=Math.PI/180*(60*i-30);p.push((x+r*Math.cos(a)).toFixed(1)+','+(y+r*Math.sin(a)).toFixed(1))}return p.join(' ')}
function el(n,a){const e=document.createElementNS(NS,n);for(const k in a)e.setAttribute(k,a[k]);return e}
function build(){
  svg.innerHTML='';cells=[];W=hero.clientWidth;H=hero.clientHeight;R=Math.max(26,Math.min(44,W/34));
  svg.setAttribute('viewBox','0 0 '+W+' '+H);
  const dx=Math.sqrt(3)*R,dy=1.5*R;
  // the alert: upper right on wide screens, upper middle on phones
  const ax=W>760?W*0.68:W*0.8,ay=W>760?H*0.36:Math.min(130,H*0.16);let best=1e9,ac=null;
  const g=el('g',{});svg.appendChild(g);
  for(let r=-1,y=0;y<H+R;r++,y=r*dy){for(let c=-1;;c++){const x=c*dx+(r%2?dx/2:0);if(x>W+R)break;
    const p=el('polygon',{points:hex(x,y,R*0.94),fill:'none',stroke:'#2b3470','stroke-width':1});g.appendChild(p);
    const d=Math.hypot(x-ax,y-ay);cells.push({p,x,y,d});if(d<best){best=d;ac={x,y,p}}}}
  cx=ac.x;cy=ac.y;
  const halo=el('circle',{cx,cy,r:R*0.4,fill:'#f3a73b',opacity:0});svg.appendChild(halo);
  ac.p.setAttribute('fill','#f3a73b');ac.p.setAttribute('fill-opacity','0');
  // three responders, from three directions, a few cells out
  const starts=(W>760?[[-7,3],[6,4],[-2,-5]]:[[-5,4],[1,5],[-6,-1]]).map(([i,j])=>({x:cx+i*dx*0.5*(W>760?1.6:1),y:cy+j*dy*0.55}));
  const dots=starts.map(s=>{const d=el('circle',{cx:s.x,cy:s.y,r:5,fill:'#a9c4ff',opacity:0});svg.appendChild(d);return {d,s}});
  return {ac,halo,dots};
}
function run(){
  timers.forEach(clearTimeout);timers=[];hero.classList.remove('ready');
  const {ac,halo,dots}=build();
  if(reduce){ac.p.setAttribute('fill-opacity','.85');dots.forEach(o=>{o.d.setAttribute('cx',cx+(o.s.x-cx)*.12);o.d.setAttribute('cy',cy+(o.s.y-cy)*.12);o.d.setAttribute('opacity',1)});hero.classList.add('ready');return}
  const t0=performance.now();
  // the pulse: cells light by distance from the alert, then fade
  cells.forEach(c=>{const delay=300+c.d*1.6;if(delay>2600)return;timers.push(setTimeout(()=>{c.p.animate([{stroke:'#f3a73b',strokeOpacity:0.9},{stroke:'#2b3470',strokeOpacity:1}],{duration:1100,easing:'ease-out',fill:'forwards'})},delay))});
  ac.p.animate([{fillOpacity:0},{fillOpacity:.95},{fillOpacity:.55},{fillOpacity:.85}],{duration:1600,delay:150,fill:'forwards'});
  halo.animate([{r:R*0.4,opacity:.55},{r:R*4.2,opacity:0}],{duration:1700,delay:200,easing:'ease-out',iterations:2});
  // responders converge
  dots.forEach((o,i)=>{const fx=cx+(o.s.x-cx)*.12,fy=cy+(o.s.y-cy)*.12;
    o.d.animate([{opacity:0,cx:o.s.x,cy:o.s.y},{opacity:1,cx:o.s.x,cy:o.s.y,offset:.18},{opacity:1,cx:fx,cy:fy}],{duration:2300,delay:900+i*220,easing:'cubic-bezier(.3,.1,.2,1)',fill:'forwards'})});
  timers.push(setTimeout(()=>hero.classList.add('ready'),1500));
}
document.querySelector('button.replay').addEventListener('click',run);
let rt;addEventListener('resize',()=>{clearTimeout(rt);rt=setTimeout(()=>{if(Math.abs(hero.clientWidth-W)>40)run()},300)});
run();
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
</div>
<button class="replay" type="button">{c['replay']}</button>
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
