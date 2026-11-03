"""Build the eleven internal pages from the approved copy snapshot."""
from pathlib import Path
from bs4 import BeautifulSoup
from html import escape as e
from urllib.parse import quote
import json,re,subprocess,sys
P=Path(__file__).parent
subprocess.run([sys.executable,str(P/'build.py')],check=True)
DATA=json.loads((P/'sources/approved-pages.json').read_text())['pages']
NAMES={'virtu':'A Virtù','veridiana':'Veridiana Cavalheri','trabalhe':'Trabalhe conosco','palestras':'Palestras','gravado':'Meta V — Acesso gravado','oficina':'Super Humanos — Oficina prática','mentoria':'Mentoria Meta V','phd':'PHD','vanguard':'Vanguard','empresas':'Soluções para empresas','contato':'Fale conosco'}
home=BeautifulSoup((P/'dist/index.html').read_text(),'html.parser')
ARROW='<span class="arrow" aria-hidden="true">↗</span>'
def soup(html):return BeautifulSoup(html,'html.parser')
def frag(html):return soup(html).find()
def txt(n):return n.get_text(' ',strip=True) if n else ''
def img(file,alt='',cls=''):
 return f'<img src="assets/{file}.jpg" alt="{e(alt)}" class="{cls}" loading="lazy" decoding="async">'
def link(label,url):return f'<a class="button" href="{e(url,quote=True)}"><span>{e(label)}</span>{ARROW}</a>'
def links(sec):
 for a in sec.select('a'):
  match=re.search(r"go\('([^']+)'\s*,\s*'([^']*)'",a.get('onclick',''))
  if match:
   dest,interest=match.groups();a['href']=dest+'.html'+('?interesse='+quote(interest) if interest else '')
  elif a.get('href','').startswith('#') and a['href'][1:] in NAMES:a['href']=a['href'][1:]+'.html'
  a.attrs.pop('onclick',None)
  for span in a.select('[aria-hidden]'):span.decompose()
  a.append(frag(ARROW))
 for el in sec.find_all():
  for attr in list(el.attrs):
   if attr.startswith('on'):del el[attr]
for key,sections in DATA.items():
 doc=soup(str(home));doc.title.string=NAMES[key]+' · Virtù';doc.body['class']=['internal','page-'+key]
 doc.select_one('meta[name="description"]')['content']=txt(soup(sections[0]['html']).select_one('p'))
 doc.select_one('link[rel="preload"][as="image"]')['href']=f'assets/curadoria-heroes-{key}.jpg'
 for s in doc.select('script[src="app.js"]'):s.insert_after(frag('<script defer src="pages.js"></script>'))
 header=doc.select_one('.brand');header['href']='index.html'
 menu=doc.select_one('#menu');menu.select_one('a[href="#filme"]')['href']='index.html#filme'
 side=menu.select_one('.menu-side');side.insert(-1,frag('<a class="menu-careers" href="trabalhe.html">Trabalhe conosco</a>'))
 for a in menu.select('a'):
  if a.get('href')==key+'.html':a['aria-current']='page'
 footer=doc.select_one('footer')
 for a in footer.select('a[href^="#"]'):
  a['href']='index.html'+a['href'] if a['href']!='#inicio' else '#inicio'
 doc.select_one('.floating-contact')['href']='contato.html'
 for d in doc.select('#contact-dialog,#video-dialog'):d.decompose()
 main=doc.select_one('main');main.clear()
 # Full viewport opening, retaining every paragraph in the immediately following deck if needed.
 oldhero=soup(sections[0]['html']);links(oldhero);h1=txt(oldhero.h1);paras=oldhero.select('.hero-copy > p') or oldhero.select('.wrap > p');actions=oldhero.select_one('.actions')
 if key=='contato':actions=frag('<div class="actions">'+link('Iniciar uma conversa','#formulario')+'</div>')
 if key=='trabalhe':
  for a in actions.select('a'):a['href']='#candidatura'
 hero=f'<section class="hero internal-hero" id="inicio" aria-labelledby="hero-title"><img class="hero-image" src="assets/curadoria-heroes-{key}.jpg" alt="Veridiana Cavalheri" fetchpriority="high"><div class="hero-shade"></div><div class="hero-grid" aria-hidden="true"></div><div class="internal-hero-content"><p class="eyebrow hero-kicker">VIRTÙ / {e(NAMES[key])}</p><h1 id="hero-title">{e(h1)}</h1><div class="internal-hero-bottom"><div class="hero-description">{str(paras[0]) if paras else ""}</div>{str(actions) if actions else ""}</div></div><a class="scroll-cue" href="#pagina" aria-label="Explorar esta página">↓</a></section>'
 main.append(frag(hero));main.append(frag('<div id="pagina"></div>'))
 if len(paras)>1:main.append(frag('<section class="hero-deck"><div class="content-grid"><p class="eyebrow">'+e(NAMES[key])+'</p><div>'+''.join(map(str,paras[1:]))+'</div></div></section>'))
 for idx,source in enumerate(sections[1:],1):
  sec=soup(source['html']).section;links(sec);sec['class']=['page-section'];sec['id']=source['id'] or 'bloco-'+str(idx+1).zfill(2)
  wrap=sec.select_one('.wrap');wrap['class']=['page-wrap']
  title=sec.h2
  if title:title['class']=['section-title']
  # Insert a quiet chapter number into each section without changing approved headings.
  wrap.insert(0,frag(f'<p class="chapter eyebrow">{idx:02d} / {e(NAMES[key])}</p>'))
  grid=sec.select_one('.card-grid');checks=sec.select_one('.check-list');faqs=sec.select('.faq');form=sec.select_one('form')
  original=source['html']
  if form:
   sec['class']+=['form-section'];sec['id']='candidatura' if key=='trabalhe' else 'formulario'
   for n in sec.select('.prototype-note,.privacy-placeholder,#demo-message,.upload-field'):n.decompose()
   form['id']='inquiry-form';form['data-kind']=key
   for i,field in enumerate(form.select('input,select,textarea')):
    field['name']=field.get('name') or 'field-'+str(i)
    if field.name!='select':field['maxlength']='2000' if field.name=='textarea' else '200'
   if key=='contato':
    form.select_one('#interest')['name']='interest';form.select_one('#theme')['name']='theme'
   submit=form.select_one('[type="submit"]');submit.clear();submit.append('Continuar no WhatsApp ');submit.append(frag(ARROW))
   note='Sua mensagem será aberta no WhatsApp para revisão. Você poderá anexar o currículo na conversa com a equipe.' if key=='trabalhe' else 'Sua mensagem será aberta no WhatsApp para você revisar e enviar à equipe Virtù.'
   form.append(frag('<p class="form-note">'+note+'</p>'))
  elif faqs:
   sec['class']+=['page-faq'];group=sec.new_tag('div') if hasattr(sec,'new_tag') and callable(sec.new_tag) else frag('<div class="page-faq-list"></div>')
   group['class']=['page-faq-list']
   for f in faqs:
    f['name']='faq-'+key;q=f.summary
    for span in q.select('span'):span.decompose()
    question=txt(q);q.clear();q.append(frag('<h3>'+e(question)+'</h3>'));q.append(frag('<span class="plus" aria-hidden="true"></span>'))
    answer=frag('<div class="faq-answer"></div>')
    for p in f.select('p'):answer.append(p.extract())
    f.append(answer);group.append(f.extract())
   wrap.append(group)
  elif 'talk-immersive' in source['classes']:
   sec['class']+=['talk-section'];label=['As cinco dimensões da liderança','Influência real','Auto Performance','EU — A força inabalável de ser'][idx-2]
   sec.select_one('.talk-shade').decompose()
   photo=frag('<figure class="talk-photo">'+img('curadoria-talks-'+str(idx+1),'Veridiana em sua trajetória profissional')+'</figure>');wrap.insert(1,photo)
   sec.select_one('.chapter').string=f'{idx:02d} / {label}'
  elif grid:
   features=grid.select(':scope > article');gridclasses=grid.get('class',[])
   for i,a in enumerate(features):
    if not a.select_one('.index'):a.insert(0,frag(f'<span class="index">{i+1:02d}</span>'))
   if 'solutions' in gridclasses:
    sec['class']+=['solution-section'];grid['class']=['solution-grid']
    dests=['gravado','oficina','mentoria'] if idx==2 else ['phd','vanguard']
    for a,dest in zip(features,dests):
     a.insert(0,frag('<figure>'+img(dest,NAMES[dest])+'</figure>'));a.select_one('a')['href']=dest+'.html'
   elif 'farm-grid' in gridclasses or 'steps' in gridclasses or (key in ['mentoria','vanguard'] and idx in ([3] if key=='mentoria' else [4])):
    sec['class']+=['process-section'];grid['class']=['process-grid']
   elif len(features)>4:
    sec['class']+=['index-section'];grid['class']=['topic-index']
    for a in features:
     heading=a.h3;body=''.join(str(p) for p in a.select('p'));number=txt(a.select_one('.index'))
     a.replace_with(frag(f'<details class="topic" name="topics-{idx}"><summary><span class="index">{number}</span><h3>{e(txt(heading))}</h3><span class="plus" aria-hidden="true"></span></summary><div class="topic-answer">{body}</div></details>'))
   else:
    sec['class']+=['pillar-section'];grid['class']=['pillar-grid'];grid['data-count']=str(len(features))
    if (key=='virtu' and idx==5) or (key=='veridiana' and idx==3):sec['class']+=['wine-section']
  elif checks:
   sec['class']+=['check-section']
   for i,c in enumerate(checks.select(':scope > div')):
    check=c.select_one('.check')
    if check:check.clear();check.string=str(i+1).zfill(2)
  elif 'image-split' in original:
   sec['class']+=['image-section']
   identifier=f'{key}-{idx+1}';file='curadoria-secondary-'+identifier
   if not (P/'dist/assets'/f'{file}.jpg').exists():file='retrato'
   alt='Veridiana Cavalheri e sua trajetória' if key!='oficina' else 'Registro de atuação de Veridiana'
   wrap.insert(1,frag('<figure class="editorial-photo">'+img(file,alt)+'</figure>'))
   # Put all text into a real column; copied layout wrappers are removed.
   column=frag('<div class="editorial-content"></div>')
   for child in list(wrap.contents)[2:]:column.append(child.extract())
   wrap.append(column)
   if idx%2==0:sec['class']+=['image-reverse']
  elif 'dark' in source['classes']:
   sec['class']+=['closing-section'];sec['id']='contato'
  else:sec['class']+=['editorial-section']
  # Keep context logos from the approved page as readable names, including image-only logos.
  logos=sec.select_one('.logos')
  if logos:
   logos.clear()
   for label in source.get('logos',[]):
    if label:logos.append(frag('<span>'+e(label)+'</span>'))
  # Strip leftover decorative empty wrappers from the copy snapshot.
  for empty in sec.select('.feature-icon'):empty.decompose()
  main.append(sec)
 # Give every route a contact target for shared floating CTA visibility logic.
 if not main.select('#contato'):main.append(frag('<div id="contato"></div>'))
 for a in doc.select('a[href="index.html"]'):
  if a.find_parent('footer'):a['href']='index.html'
 (P/'dist'/f'{key}.html').write_text(str(doc),encoding='utf-8')
print('Generated',len(DATA),'internal pages from approved source')
