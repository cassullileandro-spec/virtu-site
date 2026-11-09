"""Check source copy, linked lecture routes and the contact handoff."""
import json
from pathlib import Path
from urllib.parse import urlsplit, unquote, parse_qs
from bs4 import BeautifulSoup

ROOT=Path(__file__).parent
TALKS=json.loads((ROOT/'sources/talks.json').read_text())['talks']
def normalized(value):return ' '.join(value.split())

def test_lecture_pages():
 catalog=BeautifulSoup((ROOT/'dist/palestras.html').read_text(),'html.parser')
 contact=BeautifulSoup((ROOT/'dist/contato.html').read_text(),'html.parser')
 themes={o.get('value',o.text) for o in contact.select('#theme option')}
 for talk in TALKS:
  route=talk['slug']+'.html'
  assert catalog.select_one(f'a[href="{route}"]'),route
  page=BeautifulSoup((ROOT/'dist'/route).read_text(),'html.parser')
  assert len(page.select('h1'))==1
  text=normalized(page.main.get_text(' ',strip=True))
  values=[talk['title'],talk['heroBody'],talk['heroSupport']]
  for item in [talk['intro'],*talk['topics'],*talk['experience'],talk['closing']]:values.extend(item.values())
  for value in values:assert normalized(value) in text,(route,value)
  assert talk['interest'] in themes
  for a in page.select('.talk-hero .button,.closing-section .button'):
   assert parse_qs(urlsplit(a['href']).query)['interesse']==[talk['interest']]


def test_local_links_and_media():
 for path in (ROOT/'dist').glob('*.html'):
  page=BeautifulSoup(path.read_text(),'html.parser')
  for node in page.select('[href],[src]'):
   value=node.get('href') or node.get('src')
   parsed=urlsplit(value)
   if parsed.scheme or parsed.netloc or not parsed.path:continue
   target=path.parent/unquote(parsed.path)
   assert target.exists(),(path.name,value)
  assert not page.select('script[src*="mcp.figma.com"]'),path.name

if __name__=='__main__':
 test_lecture_pages();test_local_links_and_media();print('Lecture copy, catalog, contact interests, local links and media: passed')
