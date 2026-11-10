"""Semantic controls and responsive hooks for the approved static Figma layout."""
import json,re
from bs4 import BeautifulSoup,Tag
from pathlib import Path
P=Path(__file__).resolve().parent
DATA=json.loads((P/'sources/figma/interactions.json').read_text())
RECOVERY=json.loads((P/'sources/figma/recovered-assets.json').read_text())
MOBILE=json.loads((P/'sources/figma/mobile-backgrounds.json').read_text())
MOBILE_MATCH=json.loads((P/'sources/figma/mobile-source-matches.json').read_text())
EMPTY='data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7'
def text(n):return re.sub(r'\s+',' ',n.get_text(' ',strip=True)).strip()
def cls(n,c):n['class']=n.get('class',[])+[c]
def normalized(s):return re.sub(r'\W','',s.casefold())
def enhance(soup,root,slug):
 # Preserve the original site answers, which are not present in collapsed Figma frames.
 old=DATA[slug]['details']
 for sm in list(root.select('[data-name="summary"]')):
  title=text(sm);match=next((d for d in old if normalized(title).endswith(normalized(d['title'])) or normalized(d['title']).endswith(normalized(title))),None)
  if not match:
   # Journey numbers and images are decorative parts of the Figma summary.
   title=re.sub(r'^\d+\s*','',title)
   match=next((d for d in old if normalized(title) in normalized(d['title']) or normalized(d['title']) in normalized(title)),None)
  assert match,(slug,title,'missing accordion content')
  box=sm.parent;box.name='details';cls(box,'v-details');sm.name='summary';cls(sm,'v-summary')
  existing=[c for c in box.children if isinstance(c,Tag) and c is not sm]
  if existing:
   box['open']='';panel=soup.new_tag('div');cls(panel,'v-answer');cls(panel,'v-answer-designed')
   for c in existing:panel.append(c.extract())
  else:
   panel=BeautifulSoup(match['content'],'html.parser').find()
   assert panel is not None and panel.name!='none',(slug,title)
   cls(panel,'v-answer')
  for child in ([] if existing else [panel,*panel.find_all(True)]):
   child['class']=['v-'+c for c in child.get('class',[]) if not c.startswith('v-')]+[c for c in child.get('class',[]) if c.startswith('v-')]
  box.append(panel)
 for n in list(root.select('[data-name="inquiry-form"]')):
  n.name='form';n['id']='inquiry-form';cls(n,'v-form')
  for i,box in enumerate(n.select('[data-name="label"]')):
   label=box.find('p',recursive=False)
   field=box.find(attrs={'data-name':re.compile('^Campo')})
   if field is None:continue
   title=text(label) if label else field.get('data-name','').replace('Campo · ','')
   id='field-'+str(i);label.name='label';label['for']=id
   placeholder=text(field)
   isarea='objetivo' in title.lower() or 'mensagem' in title.lower() or 'apresent' in title.lower()
   field.name='textarea' if isarea else 'input';field.clear()
   field['id']=id;field['name']=title;field['aria-label']=title;field['placeholder']=placeholder;field['maxlength']='1500' if isarea else '200'
   if not isarea:
    field['type']='email' if 'mail' in title.lower() else 'tel' if any(k in title.lower() for k in ['whatsapp','telefone']) else 'url' if any(k in title.lower() for k in ['linkedin','portfólio','currículo']) else 'text'
   if any(k in title.lower() for k in ['nome','mail','whatsapp']):field['required']=''
   cls(field,'v-input')
  submit=n.find(attrs={'data-name':re.compile('Botão')})
  if submit:
   submit.name='button';submit.attrs.pop('href',None);submit['type']='submit';cls(submit,'v-submit')
  note=next((x for x in n.find_all('p',recursive=False) if 'mensagem' in text(x).lower()),None)
  if note:cls(note,'v-form-note')
 for n in root.select('.action'):
  name=n.get('data-name','').lower();t=text(n).lower()
  if slug=='contato' and 'iniciar uma conversa' in t:n['href']='#inquiry-form'
  if slug=='trabalhe' and any(k in t for k in ['candidat','currículo','fazer parte','equipe']):n['href']='#inquiry-form'
  if any(k in t for k in ['soluções para empresas','conhecer as jornadas']):n['href']='empresas.html'
  if 'whatsapp' in t and n.name=='a':n['href']='https://wa.me/5541999693214'
  exact_links={'CONVERSE COM A VIRTÙ':'contato.html','Falar com a Virtù':'contato.html','CONHEÇA VERIDIANA CAVALHERI':'veridiana.html','CONHEÇA AS PALESTRAS':'palestras.html','Consultar oportunidades':'#inquiry-form','Saber mais sobre o gravado':'contato.html?tema=gravado'}
 for n in root.select('a.action'):
  label=text(n).replace('↗','').strip()
  if label in exact_links:n['href']=exact_links[label]
  if slug=='palestras' and label in ['Conhecer a palestra','Quero esta palestra']:
   target={'792:1755':'palestra-cinco-dimensoes','792:1771':'palestra-influencia-real','792:1787':'palestra-auto-performance','792:1803':'palestra-eu'}[n.find_parent('section')['data-node-id']]
   n['href']=target+'.html' if label=='Conhecer a palestra' else 'contato.html?tema='+target
  if slug in ['index','empresas'] and label in ['Encontre sua jornada','Quero encontrar a jornada certa']:
   n['href']='#jornadas'
   section=root.select_one('[data-node-id="792:1006"]') if slug=='empresas' else root.select_one('[data-name="jornadas"]')
   section['id']='jornadas'
 for n in root.select('[data-name="Marca Virtù"]'):
  n.name='a';n['href']='index.html';n['aria-label']='Virtù — início'
 # Recover image-fill treatments omitted in the generated asset placeholders.
 for a in RECOVERY:
  if a['rendered']:continue
  for im in root.select('img'):
   if im.get('src')!=a['path']:continue
   f=a['fill'];fil=f.get('filters',{});style='filter:saturate('+str(1+fil.get('saturation',0))+') contrast('+str(1+fil.get('contrast',0))+');'
   if f['scaleMode']=='CROP':
    m=f['imageTransform'];x,y=m[0][0],m[1][1]
    style+=f'width:{100/x}%;height:{100/y}%;left:{-100*m[0][2]/x}%;top:{-100*m[1][2]/y}%;object-fit:fill;'
   im['style']=im.get('style','')+style
 # Tag layout roles once; desktop dimensions stay in the generated CSS.
 for n in [root,*root.find_all(True)]:
  cl=n.get('class',[]);s=' '.join(cl)
  if n.find_parent(class_='footer-logo') or n.find_parent(class_='site-header'):continue
  if n.name in ['p','div'] and re.search(r"text-\[(?:3[2-9]|[4-9]\d|1\d\d)(?:\.\d+)?px\]",s):
   cls(n,'v-heading')
  if n.name=='div' and text(n):
   cls(n,'v-flow')
  if n.name in ['p','a'] and 'absolute' in cl and text(n) and not n.find_parent(['header','summary']) and not n.find_parent(class_='footer-logo'):
   cls(n,'v-positioned-text')
  if n.name=='div' and n.find('img') and not text(n):
   # Frame wrappers with no own size are image-fill layers, not standalone media.
   has_size=bool(re.search(r'\bh-\[[\d.]+px\]',s))
   cls(n,'v-media' if has_size else 'v-image-layer')
  if n.name in ['section','div'] and text(n) and n.find('img',recursive=False):
   cls(n,'v-photo-card')
  if n.name in ['section','div'] and text(n):
   direct=[c for c in n.children if isinstance(c,Tag)]
   if any('absolute' in c.get('class',[]) and c.find('img') and not text(c) for c in direct):
    cls(n,'v-photo-card')
 for n in root.select('.hero'):
  cls(n,'v-hero')
  bg=n.find('img')
  if bg:
   art=soup.new_tag('div');art['class']=['v-mobile-art'];art['aria-hidden']='true'
   im=soup.new_tag('img',src='assets/mobile/'+slug+'.png',alt='');im['fetchpriority']='high';art.append(im);n.insert(0,art)
   meta=next(x for x in MOBILE if x['slug']==slug);c=meta['color'];n['style']=n.get('style','')+';--hero-tone:rgb('+','.join(str(round(c[k]*255)) for k in ['r','g','b'])+');'

 for n in root.select('[data-name="play-button"],[data-node-id="792:3859"]'):
  n.name='button';n['type']='button';n['aria-label']='Assistir ao teaser de liderança';n['data-play-video']=''
 # Correct document outline while retaining individual line wrappers.
 heading=root.select_one('[data-node-id=\"792:3819\"]') if slug=='index' else root.select_one('.hero .v-heading')
 if heading:
  heading.name='h1'
  for child in heading.find_all('p',recursive=False):child.name='span';child['style']='display:block'
 for h in root.select('.v-heading'):
  if h is heading or h.find_parent(class_='v-heading'):continue
  if h.name=='p':h.name='h2'
  elif h.name=='div' and all(c.name=='p' for c in h.children if isinstance(c,Tag)):
   h.name='h2'
   for child in h.find_all('p',recursive=False):child.name='span';child['style']='display:block'
 for f in root.select('.site-footer [href="#duvidas"]'):
  if not root.select_one('#duvidas'):f['href']='index.html#duvidas'
 for sm in root.select('.v-summary'):
  for im in sm.select('img'):im['alt']=''
 if slug=='index':
  stage=root.select_one('[data-name="challenge-stage"]');stage['aria-live']='polite'
  stage['data-slides']=json.dumps(DATA[slug]['challenges'],ensure_ascii=False)
  controls=root.select_one('[data-name="challenge-controls"]')
  for i,n in enumerate(controls.find_all('p',recursive=False)):
   if i==1:n['data-slide-count']=''
   else:n.name='button';n['type']='button';n['data-slide-step']='-1' if i==0 else '1';n['aria-label']='Desafio anterior' if i==0 else 'Próximo desafio'
  for i,n in enumerate(root.select_one('[data-name="challenge-dots"]').find_all('div',recursive=False)):
   n.name='button';n['type']='button';n['data-slide-to']=str(i);n['aria-label']='Desafio '+str(i+1);n['aria-pressed']='true' if i==0 else 'false'
 # Picture sources keep the desktop compositions and choose purpose-made mobile art.
 matches={asset:key for key,assets in MOBILE_MATCH.items() for asset in assets}
 for im in list(root.select('img')):
  art=im.find_parent(class_='v-mobile-art');hero=im.find_parent(class_='hero')
  key=matches.get(im.get('src'))
  if im.get('src')=='assets/figma/6389a00f-5662-4835-8312-68b05bce7453.png':key='teaser'
  if art or hero or (key and im.find_parent(class_='v-photo-card') and not im.find_parent('summary')):
   picture=soup.new_tag('picture');picture['style']='display:contents';source=soup.new_tag('source')
   source['media']='(min-width: 1200px)' if art else '(max-width: 1199px)'
   source['srcset']=EMPTY if art or hero else 'assets/mobile/'+key+'.png'
   im.wrap(picture);picture.insert(0,source)
   if key and not hero:cls(im,'v-mobile-photo')
 return root
