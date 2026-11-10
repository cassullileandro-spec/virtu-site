const $=(s,r=document)=>r.querySelector(s), $$=(s,r=document)=>[...r.querySelectorAll(s)];
function resize(){document.documentElement.style.setProperty('--design-scale',Math.min(1,innerWidth/1920))}
resize();addEventListener('resize',resize);
const menu=$('#site-menu'),videoDialog=$('#site-video'),video=$('video',videoDialog);
let lastFocus=null;
function openDialog(dialog,button){lastFocus=button;dialog.showModal();document.documentElement.style.overflow='hidden'}
function closeDialog(dialog){dialog.close()}
$$('.menu-toggle').forEach(b=>b.addEventListener('click',()=>{openDialog(menu,b);b.setAttribute('aria-expanded','true')}));
$('.close-menu',menu).addEventListener('click',()=>closeDialog(menu));
$$('a',menu).forEach(a=>a.addEventListener('click',()=>closeDialog(menu)));
for(const dialog of [menu,videoDialog]){
 dialog.addEventListener('close',()=>{document.documentElement.style.overflow='';lastFocus?.focus();$$('.menu-toggle').forEach(b=>b.setAttribute('aria-expanded','false'));if(dialog===videoDialog)video.pause()});
 dialog.addEventListener('click',e=>{if(e.target===dialog){const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)closeDialog(dialog)}})
}
$$('[data-play-video]').forEach(b=>b.addEventListener('click',()=>{openDialog(videoDialog,b);video.play().catch(()=>{})}));
$('.close-video',videoDialog).addEventListener('click',()=>closeDialog(videoDialog));
$('.v-form')?.addEventListener('submit',e=>{
 e.preventDefault();const f=e.currentTarget;if(!f.reportValidity())return;
 const rows=[...new FormData(f)].filter(([,v])=>String(v).trim()).map(([k,v])=>k+': '+String(v).trim());
 const topic=document.querySelector('.page').dataset.page==='trabalhe'?'Quero trabalhar com a Virtù.':'Olá, quero conversar com a Virtù.';
 const url='https://wa.me/5541999693214?text='+encodeURIComponent(topic+'\n\n'+rows.join('\n'));
 window.open(url,'_blank','noopener,noreferrer');
});
const stage=$('[data-slides]');
if(stage){
 const slides=JSON.parse(stage.dataset.slides),parts=[...stage.children];let active=0;
 function show(index){active=(index+slides.length)%slides.length;parts[0].textContent=String(active+1).padStart(2,'0');parts[1].textContent=slides[active];$('[data-slide-count]').textContent=String(active+1).padStart(2,'0')+' / '+String(slides.length).padStart(2,'0');$$('[data-slide-to]').forEach((b,i)=>b.setAttribute('aria-pressed',String(i===active)))}
 $$('[data-slide-step]').forEach(b=>b.addEventListener('click',()=>show(active+Number(b.dataset.slideStep))));
 $$('[data-slide-to]').forEach(b=>b.addEventListener('click',()=>show(Number(b.dataset.slideTo))));
}

const topics={'palestra-cinco-dimensoes':'As cinco dimensões da liderança','palestra-influencia-real':'Influência real','palestra-auto-performance':'Auto Performance para times','palestra-eu':'EU — A força inabalável de ser'};
const topic=topics[new URLSearchParams(location.search).get('tema')];
if(topic){const field=$('[name="Tenho interesse em"]');if(field)field.value=topic}
