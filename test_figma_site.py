"""Source fidelity, local assets, destinations, and form contracts."""
from pathlib import Path
from urllib.parse import urlsplit,unquote
import re,runpy
from bs4 import BeautifulSoup
P=Path(__file__).resolve().parent
compiler=runpy.run_path(str(P/'sync-figma.py'))
norm=lambda s:re.sub(r'\s+',' ',s).strip()
pages={f.name:BeautifulSoup(f.read_text(),'html.parser') for f in (P/'dist').glob('*.html')}
assert len(pages)==16
for name,s in pages.items():
 assert len(s.select('h1'))==1,(name,'heading')
 assert len(s.select('.site-footer'))==1,(name,'footer')
 assert len(s.select('.footer-nav a'))==13,(name,'footer navigation')
 assert not s.select('a a'),(name,'nested links')
 for n in s.select('[src],[href],source[srcset]'):
  value=n.get('src') or n.get('href') or n.get('srcset')
  if not value or value.startswith(('http:','https:','data:','mailto:','tel:')):continue
  u=urlsplit(value);target=unquote(u.path)
  if target:assert (P/'dist'/target).is_file(),(name,target)
  if u.fragment and (not target or target.endswith('.html')):
   doc=pages[target] if target else s
   assert doc.find(id=u.fragment),(name,value,'missing anchor')
 original=compiler['fragment']((P/'sources/figma'/name.replace('.html','.tsx')).read_text())
 rendered=norm(s.select_one('main').get_text(' ',strip=True)+' '+' '.join(n.get('placeholder','') for n in s.select('input,textarea')))
 for n in original.select('p'):
  needed=norm(n.get_text(' ',strip=True))
  if needed:assert needed in rendered,(name,'lost copy',needed)
 assert len(s.select('.v-mobile-art source'))==1
for route in ['palestra-cinco-dimensoes','palestra-influencia-real','palestra-auto-performance','palestra-eu']:
 assert pages['palestras.html'].select(f'a[href="{route}.html"]')
 assert pages['index.html'].select(f'a[href="{route}.html"]')
 assert pages[route+'.html'].select(f'a[href="contato.html?tema={route}"]')
for name in ['contato.html','trabalhe.html']:
 s=pages[name];assert s.select('form input[required][type="email"]')
 assert s.select('form button[type="submit"]')
 assert all(n.get('for') for n in s.select('form label'))
assert 'function open(' not in (P/'dist/figma-site.js').read_text()
assert 'figma.com/api/mcp/asset/' not in ''.join(f.read_text() for f in (P/'sources/figma').glob('*.tsx'))
assert len(list((P/'dist/assets/mobile').glob('*.png')))==17
print('PASS: 16 pages, source copy, assets, destinations, 17 mobile backgrounds and form contracts.')
