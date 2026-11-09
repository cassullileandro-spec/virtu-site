from typography import finish_typography
"""Build the eleven internal pages from the approved copy snapshot."""
from pathlib import Path
from bs4 import BeautifulSoup
from html import escape as e
from urllib.parse import quote
import json,re,subprocess,sys
P=Path(__file__).parent
subprocess.run([sys.executable,str(P/'build.py')],check=True)
TALKS=json.loads((P/'sources/talks.json').read_text())['talks']
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
 for s in doc.select('script[src^="app.js"]'):s.insert_after(frag('<script defer src="pages.js?v=20261104-all-pages"></script>'))
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
 hero=f'<section class="hero internal-hero editorial-hero" id="inicio" aria-labelledby="hero-title"><div class="internal-hero-content"><p class="eyebrow hero-kicker">VIRTÙ / {e(NAMES[key])}</p><h1 id="hero-title">{e(h1)}</h1><div class="internal-hero-bottom"><div class="hero-description">{str(paras[0]) if paras else ""}</div>{str(actions) if actions else ""}</div></div><figure class="hero-portrait"><img class="hero-image" src="assets/curadoria-heroes-{key}.jpg" alt="Veridiana Cavalheri" fetchpriority="high"></figure></section>'
 main.append(frag(hero));main.append(frag('<div id="pagina"></div>'))
 if len(paras)>1:main.append(frag('<section class="hero-deck"><div class="content-grid"><p class="eyebrow">'+e(NAMES[key])+'</p><div>'+''.join(map(str,paras[1:]))+'</div></div></section>'))
 for idx,source in enumerate(sections[1:],1):
  sec=soup(source['html']).section;links(sec);sec['class']=['page-section'];sec['id']=source['id'] or 'bloco-'+str(idx+1).zfill(2)
  wrap=sec.select_one('.wrap');wrap['class']=['page-wrap']
  title=sec.h2
  if title:title['class']=['section-title']
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
   sec['class']+=['talk-section']
   sec.select_one('.talk-shade').decompose()
   talk=TALKS[idx-2]
   sec['class']+=['catalog-talk','theme-'+talk['theme']]
   photo=frag('<figure class="talk-photo"><a href="'+talk['slug']+'.html" aria-label="'+e(talk['title'],quote=True)+'"><img src="assets/'+talk['heroImage']+'" alt="'+e(talk['title'],quote=True)+'" loading="lazy"></a></figure>');wrap.insert(0,photo)
   sec.select_one('.talk-copy').insert(0,frag('<p class="eyebrow">'+e(talk['title'])+'</p>'))
   sec.select_one('.actions').insert(0,frag(link('Conhecer a palestra',talk['slug']+'.html')))
  elif grid:
   features=grid.select(':scope > article');gridclasses=grid.get('class',[])
   for i,a in enumerate(features):
    if not a.select_one('.index'):a.insert(0,frag(f'<span class="index">{i+1:02d}</span>'))
   if 'solutions' in gridclasses:
    sec['class']+=['solution-section'];grid['class']=['solution-grid'];grid.attrs.pop('style',None)
    dests=['gravado','oficina','mentoria'] if idx==2 else ['phd','vanguard']
    for a,dest in zip(features,dests):
     a.insert(0,frag('<figure>'+img('curadoria-heroes-'+dest,NAMES[dest])+'</figure>'));a.select_one('a')['href']=dest+'.html'
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
   wrap.insert(0,frag('<figure class="editorial-photo">'+img(file,alt)+'</figure>'))
   # Put all text into a real column; copied layout wrappers are removed.
   column=frag('<div class="editorial-content"></div>')
   for child in list(wrap.contents)[1:]:column.append(child.extract())
   wrap.append(column)
   if idx%2==0:sec['class']+=['image-reverse']
  elif 'dark' in source['classes']:
   sec['class']+=['closing-section'];sec['id']='contato'
  else:sec['class']+=['editorial-section']
  # Preserve the approved words while giving distinct content its own reading structure.
  approved_words=sec.get_text(' ',strip=True).split()
  if key in ('virtu','veridiana') and grid and len(grid.select(':scope > article'))==4:
   grid['class']+=['pillar-rows']
  if key=='virtu' and sec['id']=='bloco-05':sec['class']+=['purpose-section']
  if key=='virtu' and sec['id']=='bloco-07':
   copy=sec.select_one('.editorial-copy');paragraphs=copy.select(':scope > p')
   for i in (1,3,5):
    item=frag('<article class="service-summary"></article>')
    paragraphs[i].insert_before(item);paragraphs[i].name='h3'
    item.append(paragraphs[i].extract());item.append(paragraphs[i+1].extract())
  if key=='veridiana' and sec['id']=='bloco-03':
   pull_quote=sec.select_one('.editorial-copy').select('p')[-1].extract()
   pull_quote.name='blockquote';pull_quote['class']=['editorial-pullquote'];wrap.append(pull_quote)
  if key=='veridiana' and sec['id']=='bloco-07':
   sec.select('.editorial-content p')[3].name='h3'
  if key=='veridiana' and sec['id']=='bloco-08':
   intro=sec.select_one('.center-intro');intro['class']=['section-intro']
   copy=frag('<div class="editorial-copy"></div>')
   for paragraph in intro.select('p'):copy.append(paragraph.extract())
   intro.insert_after(copy)
  if 'index-section' in sec['class']:
   sec.select_one('.topic')['open']=''
  # Text and its action stay in one flow instead of inheriting the adjacent title's height.
  if 'editorial-section' in sec['class'] and wrap.select(':scope > p'):
   copy=frag('<div class="editorial-copy"></div>')
   direct=wrap.select(':scope > p, :scope > .actions')
   direct[0].insert_before(copy)
   for child in direct:copy.append(child.extract())
  if 'closing-section' in sec['class']:
   inner=sec.select_one('.cta-inner')
   paragraphs=inner.select(':scope > p')
   if paragraphs:
    copy=frag('<div class="closing-copy"></div>');paragraphs[0].insert_before(copy)
    for paragraph in paragraphs:copy.append(paragraph.extract())
  assert sec.get_text(' ',strip=True).split()==approved_words, f'Copy changed in {key}/{sec["id"]}'
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
 (P/'dist'/f'{key}.html').write_text(finish_typography(str(doc)),encoding='utf-8')
print('Generated',len(DATA),'internal pages from approved source')

# Individual talks reuse the site's navigation, contact flow and type scale.
for talk in TALKS:
 doc=soup((P/'dist/palestras.html').read_text());doc.title.string=talk['title']+' · Virtù'
 doc.body['class']=['internal','talk-detail','theme-'+talk['theme']]
 doc.select_one('meta[name="description"]')['content']=talk['heroSupport']
 doc.select_one('link[rel="preload"][as="image"]')['href']='assets/'+talk['heroImage']
 main=doc.select_one('main');main.clear()
 contact_url='contato.html?interesse='+quote(talk['interest'])
 action=link('Levar esta palestra ao meu evento',contact_url)
 main.append(frag('<section class="hero internal-hero talk-hero" id="inicio"><img class="hero-image" src="assets/'+talk['heroImage']+'" alt="Veridiana Cavalheri" fetchpriority="high"><div class="talk-hero-shade"></div><div class="internal-hero-content"><a class="eyebrow talk-back" href="palestras.html">← Palestras com Veridiana</a><h1 id="hero-title">'+e(talk['title'])+'</h1><div class="internal-hero-bottom"><div class="hero-description"><p>'+e(talk['heroBody'])+'</p><p>'+e(talk['heroSupport'])+'</p></div><div class="actions">'+action+'</div></div></div></section>'))
 main.append(frag('<section class="page-section talk-intro" id="pagina"><div class="page-wrap"><h2 class="section-title">'+e(talk['intro']['title'])+'</h2><div class="editorial-copy"><p>'+e(talk['intro']['body'])+'</p></div></div></section>'))
 topics=''.join('<article><span class="index">'+str(i+1).zfill(2)+'</span><div><h3>'+e(item['title'])+'</h3><p>'+e(item['body'])+'</p></div></article>' for i,item in enumerate(talk['topics']))
 main.append(frag('<section class="page-section talk-topics"><div class="page-wrap"><div class="talk-topics-intro"><p class="eyebrow">Conteúdo da palestra</p><h2 class="section-title">O que vamos colocar em conversa.</h2><figure><img src="assets/'+talk['detailImage']+'" alt="Composição editorial da palestra '+e(talk['title'],quote=True)+'" loading="lazy"></figure></div><div class="talk-topic-list">'+topics+'</div></div></section>'))
 experience=''.join('<article><h3>'+e(item['title'])+'</h3><p>'+e(item['body'])+'</p></article>' for item in talk['experience'])
 main.append(frag('<section class="page-section talk-experience"><div class="page-wrap"><div><p class="eyebrow">A experiência</p><h2 class="section-title">Uma conversa que continua depois do encontro.</h2></div><div class="experience-list">'+experience+'</div></div></section>'))
 main.append(frag('<section class="page-section speaker-section"><div class="page-wrap"><figure><img src="assets/curadoria-heroes-veridiana.jpg" alt="Veridiana Cavalheri" loading="lazy"></figure><div><p class="eyebrow">Quem conduz essa conversa</p><h2 class="section-title">Veridiana Cavalheri</h2><p>Fundadora da Virtù, palestrante, consultora, mentora e autora de Antifraca.</p>'+link('Conheça sua trajetória','veridiana.html')+'</div></div></section>'))
 main.append(frag('<section class="page-section closing-section" id="contato"><div class="page-wrap"><h2 class="section-title">'+e(talk['closing']['title'])+'</h2><div class="closing-copy"><p>'+e(talk['closing']['body'])+'</p></div><div class="actions">'+action+'</div></div></section>'))
 (P/'dist'/f'{talk["slug"]}.html').write_text(finish_typography(str(doc)),encoding='utf-8')
print('Generated',len(TALKS),'individual talk pages')
