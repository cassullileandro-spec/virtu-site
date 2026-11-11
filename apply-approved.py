"""Apply approved editorial content to the original responsive site and interactions."""
from pathlib import Path
from bs4 import BeautifulSoup,Tag
from html import escape
import runpy,re,json
P=Path(__file__).resolve().parent
C=runpy.run_path(str(P/'sync-figma.py'))
def parse(s):return BeautifulSoup(s,'html.parser')
def text(n):return re.sub(r'\s+',' ',n.get_text(' ',strip=True)).strip() if n else ''
def cls(n,c):n['class']=n.get('class',[])+[c]
def dimension(n,key):
 m=re.search(r'(?:^| )'+key+r'-\[([\d.]+)px\]', ' '.join(n.get('class',[])))
 return float(m[1]) if m else None
def tags(n):return [c for c in n.children if isinstance(c,Tag)]
def css(n):
 out={}
 for c in n.get('class',[]):
  for pair in C['utility'](c).split(';'):
   if ':' in pair:
    k,v=pair.split(':',1);out[k]=v
 for pair in n.get('style','').split(';'):
  if ':' in pair:
   k,v=pair.split(':',1);out[k.strip()]=v
 return out
def fluid(section):
 """Translate editorial columns into real fluid grid tracks; artwork keeps its crop."""
 allnodes=[section,*section.find_all(True)]
 original={id(n):(n.get('class',[])[:],css(n),dimension(n,'w'),dimension(n,'h')) for n in allnodes}
 for n in allnodes:
  if 'approved-client-logos' in n.get('class',[]) or n.find_parent(class_='approved-client-logos'):continue
  classes,st,w,h=original[id(n)];st=st.copy()
  istext=n.name in ('p','h1','h2','h3','span') and text(n)
  art=n.name in ('img','picture','source') or (not text(n) and st.get('position')=='absolute')
  media=not text(n) and n.name=='div' and n.find('img') is not None and st.get('position')!='absolute' and st.get('display')!='flex'
  card='v-photo-card' in classes
  for k in ['flex-shrink','min-width']:st.pop(k,None)
  if art:
   cls(n,'approved-art')
   if n.parent is section and n.name=='div':
    st['height']='100%'
    st['width']=f'{(w or 1920)/1920*100:g}%'
    if re.fullmatch(r'[\d.]+px',st.get('left','')):st['left']=f'{float(st["left"][:-2])/1920*100:g}%'
    if n.find('img') and st.get('left') not in ('0%','0',None):cls(n,'approved-side-art')
  if n is section:
   st.update(width='100%',height='auto')
   st.pop('min-height',None)
   if not card:st.update({'padding-left':'var(--gutter)','padding-right':'var(--gutter)'})
   else:
    right=float(st.get('padding-left','0').removesuffix('px'))>960 or n.get('data-node-id')=='792:1787'
    st.update({'padding-left':'calc(50% + 32px)' if right else 'var(--gutter)','padding-right':'var(--gutter)'})
    cls(n,'approved-cover')
   for k in ['padding-top','padding-bottom']:
    if k in st and float(st[k].removesuffix('px'))>=64:st[k]='var(--section-space)'
  elif not art:
   if n.name=='div':st['width']='100%'
   for k in ['height','min-height','max-height','left','top','right','bottom','margin-left','margin-right']:
    st.pop(k,None)
   if st.get('position')=='absolute':
    st['position']='relative';st.pop('transform',None)
   if n.parent is section:
    st['width']='100%';st['max-width']=str(min(w or 1280,1280))+'px';st['margin-inline']='auto'
   elif w and w<=64:st['width']=str(w)+'px'
   # Large canvas margins become the same live container inset as the old site.
   for k in ['padding-left','padding-right']:
    if re.fullmatch(r'[\d.]+px',st.get(k,'')) and float(st[k][:-2])>96:st[k]='max(32px,calc((100vw - 1280px)/2))'
   st.pop('overflow',None)
  if st.get('display')=='grid':
   cls(n,'approved-stack');cls(n,'approved-placed-grid')
  if n is not section and any(float(st.get(k,'0').removesuffix('px'))>=64 for k in ['padding-top','padding-bottom'] if re.fullmatch(r'[\d.]+px',st.get(k,'0'))):
   cls(n,'approved-inset-block')
   if not original[id(section)][1].get('padding-top') and 'v-photo-card' not in original[id(section)][0]:cls(section,'approved-inner-spacing')
  if re.fullmatch(r'[\d.]+px',st.get('gap','')) and float(st['gap'][:-2])>32:
   cls(n,'approved-wide-gap')
  if 'parágrafos' in n.get('data-name',''):
   cls(n,'approved-prose')
  if media:
   if 'box-shadow' in st:
    cls(n,'approved-shadow');st['--mobile-shadow']=st['box-shadow'].replace('20px','8px')
   st.update(width='100%',height='auto',overflow='hidden')
   st['aspect-ratio']=f'{w or 640}/{h}' if h else '4/3'
   cls(n,'approved-media')
  if card:
   st['overflow']='hidden';st['isolation']='isolate'
   st['min-height']=f'{min(h or 600,800)}px';st['height']='auto'
   cls(n,'approved-photo')
  if n.name=='img':
   originals={'a25d7fa7-ba25-4643-93d3-4c8145c14919.png':'curadoria-secondary-virtu-8.jpg','9f4bded1-197b-433a-9bc3-f3d3e6665850.png':'curadoria-secondary-mentoria-7.jpg','48f871d1-9c64-461b-900f-64d566899759.png':'curadoria-secondary-veridiana-2.jpg','f32bbae8-6a42-49da-991d-7ff947ddf594.png':'curadoria-secondary-veridiana-6.jpg','57e021ac-d5ca-4fe8-a9eb-1da56b9ccacf.png':'curadoria-secondary-veridiana-7.jpg','aed3ed65-4cf5-4662-ac38-f0a4287047dd.png':'curadoria-secondary-mentoria-7.jpg','dbef1ae2-e569-4e2b-88e0-ff49c3b23fd7.png':'curadoria-secondary-virtu-3.jpg'}
   if Path(n.get('src','')).name in originals:
    n['src']='assets/'+originals[Path(n['src']).name];st['filter']='grayscale(1)'
   st.update(width='100%',height='100%',left='0',top='0');st['object-fit']='cover'
   n['loading']='lazy';n['decoding']='async'
  if istext:
   st.pop('width',None);st.pop('height',None);st.pop('white-space',None);st.pop('word-break',None)
   st.pop('margin-bottom',None)
   size=float(st.get('font-size','0').removesuffix('px')) if re.fullmatch(r'[\d.]+px',st.get('font-size','0')) else 0
   if size>=40:st['font-size']='var(--type-title)';st['line-height']='var(--line-title)';cls(n,'approved-heading')
   elif size>=28:st['font-size']='var(--type-subtitle)';st['line-height']='var(--line-subtitle)'
   elif size>=16:st['font-size']='var(--type-body)';st['line-height']='var(--leading-body)'
   elif size:st['font-size']='var(--type-small)';st['line-height']='var(--line-small)'
   elif st.get('line-height')=='0':st['line-height']='inherit'
   if 'font-family' in st:st['font-family']='var(--font-heading)' if "Editor" in st['font-family'] else 'var(--font-body)'
   if n.name in ('h1','h2','h3') or size>=28:st['text-wrap']='balance'
  if n.name=='span' and n.find_parent(['h2','h3','p']):
   st.pop('line-height',None);st.pop('font-size',None)
  children=[c for c in tags(n) if original.get(id(c),([],{},None,None))[1].get('position')!='absolute' and c.name not in ('source',)]
  row=st.get('display')=='flex' and st.get('flex-direction')!='column' and len(children)>1
  if row and n.name not in ('a','button','summary') and not art:
   widths=[original.get(id(c),([],{},None,None))[2] or 600 for c in children]
   st['display']='grid';st.pop('flex-direction',None)
   st['grid-template-columns']=' '.join(f'{x}px' if x<=64 else f'minmax(0,{x}fr)' for x in widths)
   cls(n,'approved-row')
   if all(c.name in ('p','h2','h3','span') for c in children) and all(x>100 for x in widths):cls(n,'approved-copy-row')
   if len(widths)==2 and widths[0]<=64 and re.fullmatch(r'\d{1,2}',text(children[0])):cls(n,'approved-number-row')
   if all(x>100 for x in widths):cls(n,'approved-stack')
   if len(widths)>=4 and all(x>100 for x in widths):cls(n,'approved-four')
  if n.name in ('a','button') and text(n):
   st['display']='inline-flex';st['align-items']='center';st['gap']='24px';st['width']='fit-content';st['max-width']='100%';st['white-space']='normal';st['min-height']='48px'
   cls(n,'approved-action')
  # Manually positioned Figma text rows become ordinary, content-sized site rows.
  manual=[c for c in tags(n) if text(c) and original.get(id(c),([],{},None,None))[1].get('position')=='absolute']
  if n.name=='div' and text(n) and not st.get('display'):
   st.update(display='flex',**{'flex-direction':'column','gap':'16px'})
   if card:st['justify-content']='flex-end'
  if n.get('data-name')=='feature' and manual:
   st['padding-block']='24px'
   if len(manual)>=3 and re.fullmatch(r'\d{1,2}',text(manual[0])):
    st.update(display='grid',**{'grid-template-columns':'32px minmax(0,5fr) minmax(0,6fr)','gap':'24px','align-items':'start'})
    st.pop('flex-direction',None);cls(n,'approved-list-row')
  if st.get('display')=='flex' and st.get('flex-direction')=='column' and len(children)>1 and not st.get('gap'):
   cls(n,'approved-tight-stack')
  if n.name=='details':cls(n,'faq')
  if n.name=='summary':
   st['display']='flex';st['gap']='24px';st['align-items']='center';st['justify-content']='space-between'
  if 'v-answer' in classes:
   st.update({'padding':'24px','font-size':'var(--type-body)','line-height':'var(--leading-body)'})
   cls(n,'faq-answer')
  # Keep semantic hooks only; the original page CSS must not see exported canvas utilities.
  n['class']=[c for c in n.get('class',[]) if c.startswith('approved-') or c in ['faq','faq-answer']]
  n['style']=';'.join(k+':'+v for k,v in st.items())
  n.attrs.pop('data-design-class',None)
 cls(section,'approved-section')
 return section
def footer(source):
 groups=source.select('.footer-nav > div')
 nav=[]
 for g in groups:
  links=g.select('a')
  label=next((text(p) for p in g.select('p') if not p.find_parent('a')), '')
  nav.append('<div><h3>'+escape(label)+'</h3>'+''.join('<a href="'+escape(a['href'],quote=True)+'">'+escape(text(a))+'</a>' for a in links)+'</div>')
 intro=source.select_one('.footer-intro')
 heads=intro.select('p,h2,h3') if intro else []
 return parse('<footer class="site-footer footer-v2 section-pad"><div class="footer-v2-brand"><a href="index.html" aria-label="Virtù — início"><img src="assets/logo-claro.svg" alt="Virtù" width="480" height="165"></a><div>'+''.join('<'+('h2' if i==0 else 'p')+'>'+escape(text(p))+'</'+('h2' if i==0 else 'p')+'>' for i,p in enumerate(heads))+'</div></div><nav class="footer-v2-nav" aria-label="Navegação do rodapé">'+''.join(nav)+'</nav><div class="footer-v2-bottom"><span>© Virtù · Educação corporativa</span><span>Desenvolvimento Manta</span><a href="#inicio">Voltar ao topo ↑</a></div></footer>').footer
MOBILE={x['slug']:x for x in json.loads((P/'sources/figma/mobile-backgrounds.json').read_text())}
MOBILE_ART=json.loads((P/'sources/figma/mobile-art-direction.json').read_text())
ART_SOURCES={ref:x for x in MOBILE_ART for ref in [x['reference'],*x.get('aliases',[])]}
def apply_mobile_art(doc):
 for im in list(doc.select('main img')):
  if 'cover-portrait' in im.get('class',[]):continue
  entry=ART_SOURCES.get(im.get('src'))
  if not entry and im.find_parent(class_=['journey-panel','journey-thumb']):
   route=im.find_parent('details').select_one('.journey-content a')['href'].removesuffix('.html')
   entry=next((x for x in MOBILE_ART if x['slug']==route),None)
  if not entry:continue
  if entry.get('scope')=='cover' and not im.find_parent(class_='approved-cover'):continue
  path=entry['path']
  pic=im.parent if im.parent.name=='picture' else doc.new_tag('picture')
  if pic is not im.parent:im.wrap(pic)
  cls(pic,'mobile-art-picture')
  for source in list(pic.select('source')):source.decompose()
  pic.insert(0,doc.new_tag('source',media='(max-width: 700px)',srcset=path))
  container=im.find_parent(class_=lambda c:c and c in ['hero','approved-photo','home-talk-card','journey-panel','journey-thumb'])
  if container:cls(container,'mobile-art-directed')

for f in sorted((P/'sources/figma').glob('*.tsx')):
 slug=f.stem;source=C['fragment'](f.read_text());root=C['classify'](source,slug);root=C['enhance'](source,root,slug)
 doc=parse((P/'dist'/f'{slug}.html').read_text())
 doc.head.append(parse('<link rel="stylesheet" href="approved.css?v=20261111-home-figma">').link)
 # Original shell, navigation, dialogs, forms and animation runtime remain in place.
 doc.select_one('footer').replace_with(footer(root.select_one('footer')))
 for n in doc.select('.eyebrow'):
  if n.get('id')=='menu-title':n['class']=['sr-only']
  elif n.name=='a':n['class']=['talk-back']
  else:n.decompose()
 if slug=='index':
  cards=doc.select('.home-talk-card-copy')
  approved=root.select('.talk-card-copy')
  for target,new in zip(cards,approved):
   body=next((p for p in new.select('p') if 'text-[16px]' in p.get('class',[])),None)
   if body:target.h3.insert_after(parse('<p>'+escape(text(body))+'</p>').p)
  film=doc.select_one('.film-bottom')
  film.append(parse('<span class="film-duration">TEASER DE LIDERANÇA · 2 MIN 22 S</span>').span)
  approved_logos=root.select_one('[data-node-id="792:3827"]').select('img')
  for old,new in zip(doc.select('.logo-strip img'),approved_logos):old['src']=new['src']
  doc.select_one('.logo-strip .sicoob img')['src']='assets/logo-sicoob.png'
 else:
  main=doc.select_one('main');oldhero=main.select_one('.hero');newhero=root.select_one('.hero')
  # Keep the old responsive hero layout and type, only updating its approved copy/media.
  newtitle=newhero.select_one('h1')
  if newtitle:oldhero.h1.clear();oldhero.h1.append(text(newtitle))
  photo=next((im for im in newhero.select('img') if '/mobile/' not in im.get('src','')),None)
  oldphoto=oldhero.select_one('.hero-image')
  if photo and oldphoto:
   if not slug.startswith('palestra-'):
    oldphoto['src']=photo['src'];oldphoto['style']=photo.get('style','')
   pic=doc.new_tag('picture');pic['class']=['approved-hero-picture'];oldphoto.wrap(pic)
   pic.insert(0,doc.new_tag('source',media='(max-width: 700px)',srcset='assets/mobile/'+slug+'.png'))
   cls(oldhero,'approved-hero')
   c=MOBILE[slug]['color'];oldhero['style']='--hero-tone:rgb('+','.join(str(round(c[k]*255)) for k in ['r','g','b'])+')'
  # The existing form and FAQ components already cover keyboard and interaction states.
  old_form=main.select_one('.form-section')
  old_faq=main.select_one('.page-faq')
  for n in list(main.children):
   if isinstance(n,Tag) and n is not oldhero:n.extract()
  anchor=doc.new_tag('div',id='pagina');main.append(anchor)
  for sec in root.select(':scope > section')[1:]:
   logos=sec.find(attrs={'data-node-id':'792:1627'})
   if logos:
    mark=parse('<div class="approved-client-logos"></div>').div
    for im in logos.select('img'):
     mark.append(parse('<img src="'+im['src']+'" alt="'+escape(im.get('alt',''),quote=True)+'" loading="lazy">').img)
    logos.replace_with(mark)
   if sec.select_one('form') and old_form:
    main.append(old_form);continue
   if sec.select_one('details') and old_faq:
    old_faq['id']='duvidas';main.append(old_faq);continue
   transformed=fluid(sec.extract())
   if sec.get('data-name','').lower().startswith(('convite','contato')) or sec.get('data-node-id') in ['921:2574','922:2321']:
    transformed['id']='contato'
   main.append(transformed)
  if not main.select_one('#contato'):main.append(doc.new_tag('div',id='contato'))
  # Match current contact query links to the original form's topic handling.
  for a in doc.select('a[href*="?tema="]'):
   route=a['href'].split('?tema=')[1]
   labels={t['slug']:t['title'] for t in json.loads((P/'sources/talks.json').read_text())['talks']}
   from urllib.parse import quote
   a['href']='contato.html?interesse='+quote(labels.get(route,route))
  for a in doc.select('a[href="#inquiry-form"]'):a['href']='#'+('candidatura' if slug=='trabalhe' else 'formulario')
 for a in doc.select('footer a[href="#duvidas"]'):
  if not doc.select_one('#duvidas'):a['href']='index.html#duvidas'
 apply_mobile_art(doc)
 (P/'dist'/f'{slug}.html').write_text(str(doc))
print('Applied approved content to 16 original responsive pages.')
