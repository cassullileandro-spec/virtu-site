"""Render the approved Figma snapshots as static HTML and CSS."""
from pathlib import Path
from html import escape
import json,re,runpy
from bs4 import BeautifulSoup,Tag
P=Path(__file__).resolve().parent
D=P/'dist';S=P/'sources/figma'
enhance=runpy.run_path(str(P/'enhance-figma.py'))['enhance']
ASSETS=json.loads((S/'assets.json').read_text())
ROUTES={'Home':'index.html','A Virtù':'virtu.html','Veridiana Cavalheri':'veridiana.html','Trabalhe conosco':'trabalhe.html','Palestras':'palestras.html','Meta V — Acesso gravado':'gravado.html','Super Humanos — Oficina':'oficina.html','Mentoria Meta V':'mentoria.html','PHD':'phd.html','Vanguard':'vanguard.html','Visão geral das jornadas':'empresas.html','Fale conosco':'contato.html','Dúvidas frequentes':'#duvidas','Voltar ao topo ↑':'#inicio'}
TALKS={'dimensões':'palestra-cinco-dimensoes.html','Influência':'palestra-influencia-real.html','Performance':'palestra-auto-performance.html','inabalável':'palestra-eu.html'}
styles={};unknown=set()
def norm(s):return re.sub(r'\s+',' ',s).strip()
def value(v):return v.replace('_',' ')
def utility(c):
 fixed={'absolute':'position:absolute','relative':'position:relative','flex':'display:flex','grid':'display:grid','inline-grid':'display:inline-grid','block':'display:block','contents':'display:contents','flex-col':'flex-direction:column','flex-row':'flex-direction:row','shrink-0':'flex-shrink:0','items-start':'align-items:flex-start','items-center':'align-items:center','items-end':'align-items:flex-end','justify-between':'justify-content:space-between','justify-center':'justify-content:center','justify-end':'justify-content:flex-end','self-stretch':'align-self:stretch','content-stretch':'align-content:stretch','place-items-start':'place-items:start','justify-self-start':'justify-self:start','justify-self-end':'justify-self:end','justify-self-stretch':'justify-self:stretch','overflow-hidden':'overflow:hidden','overflow-clip':'overflow:clip','max-w-none':'max-width:none','w-full':'width:100%','h-full':'height:100%','size-full':'width:100%;height:100%','min-w-full':'min-width:100%','min-w-px':'min-width:1px','w-px':'width:1px','h-px':'height:1px','inset-0':'inset:0','top-0':'top:0','left-0':'left:0','right-0':'right:0','ml-0':'margin-left:0','mt-0':'margin-top:0','mb-0':'margin-bottom:0','pt-px':'padding-top:1px','pb-px':'padding-bottom:1px','border':'border-width:1px','border-t':'border-top-width:1px','border-b':'border-bottom-width:1px','border-l':'border-left-width:1px','border-r':'border-right-width:1px','border-solid':'border-style:solid','font-normal':'font-weight:400','font-semibold':'font-weight:600','font-bold':'font-weight:700','italic':'font-style:italic','not-italic':'font-style:normal','text-center':'text-align:center','text-right':'text-align:right','text-white':'color:white','uppercase':'text-transform:uppercase','whitespace-nowrap':'white-space:nowrap','whitespace-pre-wrap':'white-space:pre-wrap','pointer-events-none':'pointer-events:none','cursor-pointer':'cursor:pointer','object-cover':'object-fit:cover','object-contain':'object-fit:contain','object-bottom':'object-position:center bottom','mix-blend-color':'mix-blend-mode:color','opacity-72':'opacity:.72','-translate-x-1/2':'transform:translateX(-50%)','mask-alpha':'mask-mode:alpha','mask-intersect':'mask-composite:intersect','mask-no-clip':'mask-clip:no-clip','mask-no-repeat':'mask-repeat:no-repeat','via-1/2':'--via-pos:50%'}
 if c in fixed:return fixed[c]
 if c.startswith('bg-gradient-to-'):return 'background-image:linear-gradient(to '+{'b':'bottom','t':'top','r':'right'}[c[-1]]+',var(--from-color,transparent) var(--from-pos,0%),var(--via-color,var(--to-color,transparent)) var(--via-pos,100%),var(--to-color,transparent) var(--to-pos,100%))'
 if re.fullmatch(r'(col|row)-\d',c):return ('grid-column' if c.startswith('col') else 'grid-row')+':'+c[-1]
 if c.startswith('[') and c.endswith(']'):return value(c[1:-1])
 m=re.fullmatch(r'(.+?)-\[(.*)\]',c)
 if not m:unknown.add(c);return ''
 k,v=m.groups();v=value(v)
 if k=='font':
  family=v.strip("'").split(':')[0]
  return 'font-family:'+('"Editor\'s Note"' if family=="Editor's Note" else '"Geist"')+',sans-serif'
 if k=='text':return ('font-size:' if re.fullmatch(r'[\d.]+px',v) else 'color:')+v.removeprefix('color:')
 if k in ('from','via','to'):return '--'+k+('-pos:' if v.endswith('%') else '-color:')+v
 props={'bg':'background-color','border':'border-color','w':'width','h':'height','min-w':'min-width','max-w':'max-width','min-h':'min-height','max-h':'max-height','gap':'gap','gap-x':'column-gap','gap-y':'row-gap','left':'left','top':'top','right':'right','bottom':'bottom','leading':'line-height','tracking':'letter-spacing','rounded':'border-radius','shadow':'box-shadow','flex':'flex','grid-cols':'grid-template-columns','grid-rows':'grid-template-rows','col':'grid-column','row':'grid-row','inset':'inset','mask-size':'mask-size'}
 if k in props:return props[k]+':'+v
 if k in ['p','px','py','pt','pb','pl','pr','m','mx','my','mt','mb','ml','mr']:
  base='padding' if k[0]=='p' else 'margin'
  sides={'x':['left','right'],'y':['top','bottom'],'t':['top'],'b':['bottom'],'l':['left'],'r':['right']}
  return ';'.join(base+('-'+s if s else '')+':'+v for s in sides.get(k[1:],['']))
 unknown.add(c);return ''
def decode_js(s):
 if s.startswith(chr(96)):return s[1:-1]
 if s.startswith('"'):return json.loads(s)
 if s.startswith("'"):return s[1:-1]
 raise ValueError(s)
def fragment(code):
 constants=dict(re.findall(r'const (\w+) = "([^"]+)";',code))
 funcs={}
 matches=list(re.finditer(r'(export default )?function (\w+)\([^\n]*\) \{\n  return \(\n([\s\S]*?)\n  \);\n\}',code))
 assert matches,'No JSX functions'
 for m in matches:funcs[m[2]]=m[3]
 main=next(m[2] for m in matches if m[1])
 def expand(src,override=None):
  src=re.sub(r'className=\{className \|\| ("(?:[^"\\]|\\.)*")\}',lambda m:'className='+json.dumps(override if override is not None else json.loads(m[1])),src)
  def comp(m):
   name=m[1];attrs=m[2];a=re.search(r'className="([^"]*)"',attrs)
   assert name in funcs,name
   return expand(funcs[name],a[1] if a else None)
  src=re.sub(r'<([A-Z]\w*)\b([^<>]*?)/>',comp,src)
  def inline_style(m):
   result=[]
   for key,val in re.findall(r'(\w+):\s*("(?:[^"\\]|\\.)*"|\x60[^\x60]*\x60)',m[1]):
    val=decode_js(val)
    val=re.sub(r'\$\{(\w+)\}',lambda x:constants[x[1]],val)
    for url,path in ASSETS.items():val=val.replace(url,path)
    result.append(re.sub(r'[A-Z]',lambda x:'-'+x[0].lower(),key)+':'+val)
   assert result,m[0]
   return 'style="'+escape(';'.join(result),quote=True)+'"'
  src=re.sub(r'style=\{\{([\s\S]*?)\}\}',inline_style,src)
  src=re.sub(r'\{(\x60[^\x60]*\x60|"(?:[^"\\]|\\.)*"|\'[^\']*\')\}',lambda m:escape(decode_js(m[1])),src)
  src=re.sub(r'=\{(\w+)\}',lambda m:'="'+escape(ASSETS.get(constants[m[1]],constants[m[1]]),quote=True)+'"',src)
  src=src.replace('className=','class=')
  src=re.sub(r'<(div|p|span)(\s[^<>]*?)/>',lambda m:'<'+m[1]+m[2]+'></'+m[1]+'>',src)
  return src
 soup=BeautifulSoup(expand(funcs[main]),'html.parser')
 # JSX indentation is not rendered text; keep intentional internal line breaks.
 for string in list(soup.find_all(string=True)):
  if '\n' in string:
   clean=str(string).strip()
   if clean:string.replace_with(clean)
   else:string.extract()
 return soup
def addclass(n,*classes):n['class']=n.get('class',[])+list(classes)
def link(n,url):
 if n.find_parent('a'):return
 n.name='a';n['href']=url;addclass(n,'action')
 # Figma may already link the label inside a clickable container.
 for child in n.find_all('a'):
  child.name='span';child.attrs.pop('href',None)
def classify(soup,slug):
 root=soup.find(recursive=False)
 root.name='main';root['id']='conteudo';addclass(root,'page');root['data-page']=slug
 sections=[n for n in root.children if isinstance(n,Tag)]
 for i,n in enumerate(sections):
  if n.get('data-name')=='Cabeçalho':n.name='header';addclass(n,'site-header')
  elif n.get('data-node-id')=='998:1108':n.name='footer';addclass(n,'site-footer')
  else:
   n.name='section';addclass(n,'section');n['data-section-index']=str(i)
   if i==0:n['id']='inicio';addclass(n,'hero')
 for n in list(root.find_all(True)):
  if not n.parent:continue
  name=n.get('data-name','');text=norm(n.get_text(' ',strip=True));cl=n.get('class',[])
  for nm,css in [('Marca e mensagem','footer-brand-row'),('Navegação · quatro grupos','footer-nav'),('Logo Virtù · vetor integral','footer-logo'),('Apresentação da marca','footer-intro'),('Créditos','footer-credits')]:
   if name==nm:addclass(n,css)
  if name.startswith('Link · '):link(n,ROUTES.get(name[7:],'contato.html'))
  if n.name=='p' and text=='Voltar ao topo ↑':link(n,'#inicio')
  if name=='BUTTON · MENU' or (text=='MENU' and n.name=='p'):
   target=n if name=='BUTTON · MENU' else n.parent
   target.name='button';target['type']='button';target['aria-controls']='site-menu';target['aria-expanded']='false';addclass(target,'menu-toggle')
  if name.startswith('Botão · ') or name=='text-link' or name in ['Conhecer a palestra','Conheça o gravado','Conheça a oficina','Conheça a mentoria','Conheça o PHD','Conheça o Vanguard']:
   url='contato.html';parenttext=norm(n.parent.get_text(' ',strip=True))
   if 'palestra' in text.lower():
    for term,route in TALKS.items():
     if term.lower() in parenttext.lower():url=route;break
    if text.lower().startswith(('levar','quero','solicitar')):url='contato.html?tema='+slug
   else:
    for term,route in [('gravado','gravado.html'),('oficina','oficina.html'),('mentoria','mentoria.html'),('PHD','phd.html'),('Vanguard','vanguard.html'),('trajetória','veridiana.html'),('Virtù','virtu.html')]:
     if term.lower() in text.lower():url=route;break
    if any(t in text.lower() for t in ['conversar','solicitar','empresa','contato']):url='contato.html'
    if 'jornada' in text.lower():url='empresas.html'
   link(n,url)
  if name=='Texto e chamada':addclass(n,'talk-card-copy');addclass(n.parent,'talk-card')
  if name in ['Linha 1','Linha 2']:addclass(n,'talk-card-row')
  if n.name=='img':
   n['decoding']='async';n['loading']='eager' if n.find_parent(class_='hero') else 'lazy'
   if not n.get('alt'):
    parent=n.find_parent(attrs={'data-name':True});pn=parent.get('data-name','') if parent else ''
    n['alt']='' if pn in ['Group','Fotografia','Foto','Logo Virtù · vetor integral'] else pn
  if n.name=='p':
   sz=next((float(re.search(r'[\d.]+',c)[0]) for c in cl if re.fullmatch(r'text-\[[\d.]+px\]',c)),None)
   if sz and sz>=32:addclass(n,'heading')
 for n in root.select('.section'):
  txt=norm(n.get_text(' ',strip=True))
  if 'Dúvidas frequentes' in txt and len(txt)<2200:n['id']='duvidas'
  if n.get('data-name')=='contato':n['id']='contato'
 for n in root.find_all('p'):
  txt=norm(n.get_text(' ',strip=True))
  if txt.startswith('← PALESTRAS'):link(n,'palestras.html')
  elif txt in ['Quero conversar com a Virtù','Conversar com a Virtù','Conversar sobre meu evento']:link(n.parent,'contato.html')
 return root
BASE="""@font-face{font-family:'Geist';src:url('assets/geist-regular.woff2') format('woff2');font-style:normal;font-weight:100 900;font-display:swap}
@font-face{font-family:"Editor's Note";src:url('assets/editors-note-regular.woff2') format('woff2');font-style:normal;font-weight:400;font-display:swap}
@font-face{font-family:"Editor's Note";src:url('assets/editors-note-italic.woff2') format('woff2');font-style:italic;font-weight:400;font-display:swap}
*,*::before,*::after{box-sizing:border-box;border-width:0;border-style:solid}html{scroll-behavior:smooth}body{margin:0;font-family:Geist,sans-serif;background:#fafafa;color:#262626}p,h1,h2,h3,h4,figure{margin:0;font-weight:inherit}img{display:block;max-width:100%}a{color:inherit;text-decoration:none}button,input,textarea,select{font:inherit;color:inherit}button{cursor:pointer;background:none}button:focus-visible,a:focus-visible{outline:2px solid #f1c284;outline-offset:5px}.page{margin:0 auto}.action{cursor:pointer;transition:color .15s,opacity .15s}.action:hover{opacity:.85}.site-footer .action:hover,.site-footer .action:focus-visible{color:#f4f4f4;opacity:1}.site-footer .action:hover p{color:inherit}.skip-link{position:fixed;left:20px;top:-100px;z-index:99;background:white;color:black;padding:12px}.skip-link:focus{top:20px}dialog{border:0}dialog::backdrop{background:#0009}.menu-dialog{position:fixed;inset:0;max-width:none;max-height:none;width:100vw;height:100dvh;background:#0b0b0b;color:#f5f5f5;padding:64px max(24px,calc((100vw - 1280px)/2));z-index:99}.menu-dialog nav{display:grid;grid-template-columns:1fr 1fr;gap:16px 64px;margin-top:64px}.menu-dialog nav a{font-family:"Editor's Note";font-size:36px}.close-menu{position:absolute;right:48px;top:40px;font-size:20px}.media-dialog{padding:24px;background:#0b0b0b;color:white;width:min(1100px,95vw)}.media-dialog video{width:100%;max-height:80vh}.media-dialog button{display:block;margin:0 0 20px auto}@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
"""
def build():
 reports=[];outputs={}
 for path in sorted(S.glob('*.tsx')):
  soup=fragment(path.read_text());root=classify(soup,path.stem);root=enhance(soup,root,path.stem)
  for n in [root,*root.find_all(True)]:
   cls=n.get('class',[])
   for c in cls:
    if c not in styles:
     css=utility(c)
     if css:styles[c]=(f'u{len(styles)}',css)
   n['data-design-class']=' '.join(cls)
   n['class']=[styles[c][0] if c in styles else c for c in cls]
  menu='<dialog id="site-menu" class="menu-dialog" aria-label="Navegação"><button class="close-menu" aria-label="Fechar menu">Fechar ×</button><nav>'+''.join(f'<a href="{r}">{escape(t)}</a>' for t,r in ROUTES.items() if not r.startswith('#'))+'</nav></dialog>'
  video='<dialog id="site-video" class="media-dialog"><button class="close-video">Fechar ×</button><video controls playsinline preload="none"><source src="assets/teaser-lideranca.mp4" type="video/mp4"><track kind="captions" src="assets/teaser-pt.vtt" srclang="pt-BR" label="Português"></video></dialog>'
  titles={'index':'O lado humano do negócio','virtu':'A Virtù','veridiana':'Veridiana Cavalheri','empresas':'Soluções para empresas','palestras':'Palestras','gravado':'Meta V — Acesso gravado','oficina':'Super Humanos — Oficina','mentoria':'Mentoria Meta V','phd':'PHD','vanguard':'Vanguard','contato':'Fale conosco','trabalhe':'Trabalhe conosco','palestra-cinco-dimensoes':'As cinco dimensões da liderança','palestra-influencia-real':'Influência real','palestra-auto-performance':'Auto Performance para times','palestra-eu':'EU — A força inabalável de ser'}
  title='Virtù — '+titles[path.stem]
  html='<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>'+title+'</title><link rel="stylesheet" href="figma-site.css"><link rel="stylesheet" href="responsive.css"><script src="figma-site.js" defer></script></head><body><a class="skip-link" href="#conteudo">Pular para o conteúdo</a>'+str(root)+menu+video+'</body></html>'
  assert 'figma.com/api/mcp' not in html
  outputs[path.stem+'.html']=html
  reports.append({'page':path.stem,'images':len(root.find_all('img')),'nodes':len(root.find_all(True))})
 intentional={'page','section','hero','site-header','site-footer','footer-brand-row','footer-nav','footer-logo','footer-intro','footer-credits','action','menu-toggle','talk-card','talk-card-copy','talk-card-row','heading'}
 missing={c for c in unknown-intentional if not c.startswith('v-') and c not in {'faq-answer','journey-panel','topic-answer','text-link','arrow','journey-tag'}}
 assert not missing,'Unmapped design classes: '+str(sorted(missing))
 for name,html in outputs.items():(D/name).write_text(html)
 (D/'figma-site.css').write_text(BASE+'\n'+'\n'.join('.'+name+'{'+css+'}' for name,css in styles.values()))
 (S/'build-report.json').write_text(json.dumps(reports,indent=2))
 print(json.dumps({'pages':len(reports),'css_rules':len(styles),'assets':len(ASSETS)}))
if __name__=='__main__':
 assert utility('px-[24px]')=='padding-left:24px;padding-right:24px'
 assert utility('text-[color:var(--footer-link,#999)]')=='color:var(--footer-link,#999)'
 build()
