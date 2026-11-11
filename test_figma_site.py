"""Contracts for the original responsive site plus approved Figma content."""
from pathlib import Path
from urllib.parse import urlsplit,unquote
from bs4 import BeautifulSoup
import runpy,re,json
P=Path(__file__).resolve().parent
C=runpy.run_path(str(P/'sync-figma.py'))
norm=lambda s:re.sub(r'\s+',' ',s).strip()
pages={f.name:BeautifulSoup(f.read_text(),'html.parser') for f in (P/'dist').glob('*.html')}
assert len(pages)==16
for name,s in pages.items():
 assert len(s.select('main h1'))==1,(name,'heading')
 assert len(s.select('.footer-v2-nav a'))==13,(name,'footer')
 assert not s.select('a a'),(name,'nested anchors')
 assert s.select('script[src^="app.js"]') and s.select('script[src*="gsap.min.js"]'),name
 assert not s.select('[href*="figma-site.css"],[src*="figma-site.js"],[href^="responsive.css"]'),name
 for n in s.select('[src],[href],source[srcset]'):
  v=n.get('src') or n.get('href') or n.get('srcset')
  if not v or v.startswith(('http:','https:','data:','mailto:','tel:')):continue
  u=urlsplit(v);path=unquote(u.path)
  if path:assert (P/'dist'/path).is_file(),(name,path)
  if u.fragment and (not path or path.endswith('.html')):
   assert (pages[path] if path else s).find(id=u.fragment),(name,v)
 original=C['fragment']((P/'sources/figma'/name.replace('.html','.tsx')).read_text())
 rendered=norm(s.get_text(' ',strip=True)+' '+' '.join(n.get('placeholder','') for n in s.select('input,textarea')))
 for n in original.select('p'):
  t=norm(n.get_text(' ',strip=True))
  if len(t)>30:assert t in rendered,(name,'missing copy',t)
 if name!='index.html':assert s.select('picture source[srcset^="assets/mobile/"]'),name
for name in ['contato.html','trabalhe.html']:
 assert pages[name].select('form input[type="email"][required]'),name
 assert pages[name].select('form button[type="submit"]'),name
css=(P/'dist/approved.css').read_text()
assert 'zoom:' not in css and '--design-scale' not in css
assert '--content:1280px' in css
print('PASS: 16 routes, original interaction runtime, approved copy, assets, links, forms and fluid grid.')

art=json.loads((P/'sources/figma/mobile-art-direction.json').read_text())
assert len(art)==20
for item in art:
 if item.get('scope')=='cover':continue
 doc=pages[item['slug']+'.html']
 if item['slug']=='index':
  assert doc.select_one('.hero img[src="assets/hero-cover-portrait.png"]')
 else:assert doc.select_one('.hero picture source[srcset="'+item['path']+'"]'),item['slug']
 assert (P/'dist'/item['path']).is_file(),item['path']
 assert item['prompt'] and item['reference']!=item['path']
for name,count in [('palestras.html',4),('empresas.html',5),('index.html',4)]:
 selector='.home-talk-card' if name=='index.html' else '.approved-photo'
 assert len(pages[name].select(selector+'.mobile-art-directed picture source[srcset*="-art-v2"]'))==count,name
print('PASS: 15 recomposed mobile heroes, original home cutout and all 13 repeated talk/journey covers.')

for name in ['virtu.html','mentoria.html','phd.html']:
 for cover in pages[name].select('.approved-cover'):
  assert cover.select_one('picture source[srcset*="-art-v2"]'),(name,cover.get('data-node-id'))
