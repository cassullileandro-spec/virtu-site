"""Parse approved Figma content for the original responsive site."""
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
