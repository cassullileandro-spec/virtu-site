const assert=require('node:assert/strict'),fs=require('node:fs'),puppeteer=require('/Users/leandrocassulli/.npm/_npx/0f94ee7615faf582/node_modules/puppeteer-core');
const base=process.env.QA_URL||'http://127.0.0.1:4180';
const slugs=fs.readdirSync(__dirname+'/sources/figma').filter(x=>x.endsWith('.tsx')&&x!=='index.tsx').map(x=>x.slice(0,-4));
(async()=>{const b=await puppeteer.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});let checked=0;try{
 const p=await b.newPage();
 for(const width of (process.env.QA_WIDTHS||'360,390,430,700,701,768,1440').split(',').map(Number)){
  await p.setViewport({width,height:844,isMobile:width<=700,hasTouch:width<=700});
  for(const slug of slugs){
   await p.goto(base+'/'+slug+'.html',{waitUntil:'load'});
   await p.evaluate(async()=>{await document.fonts.ready;document.querySelectorAll('img').forEach(i=>i.loading='eager');await Promise.all([...document.images].map(i=>i.decode().catch(()=>{})));window.gsap?.globalTimeline.progress(1)});
   const issues=await p.evaluate(()=>{
    const errors=[],visible=n=>n.getClientRects().length&&!n.closest('dialog:not([open]),.sr-only,details:not([open]) .faq-answer');
    if(document.documentElement.scrollWidth>innerWidth)errors.push('horizontal overflow');
    for(const im of document.querySelectorAll('main img')){
     if(!im.naturalWidth)errors.push('missing image: '+im.src);
     if(innerWidth<=700&&im.closest('.approved-media')){
      const r=im.getBoundingClientRect();if(Math.abs(r.width/r.height-im.naturalWidth/im.naturalHeight)>.02)errors.push('photo crop: '+im.src);
     }
    }
    for(const n of document.querySelectorAll('main h1,main h2,main h3,main p,main a')){
     if(!visible(n))continue;
     if(n.scrollWidth>n.clientWidth+2)errors.push('text overflow: '+n.textContent);
     if(n.scrollHeight>n.clientHeight+3&&getComputedStyle(n).overflowY==='hidden')errors.push('clipped text: '+n.textContent);
    }
    if(innerWidth<=700){
     const h=document.querySelector('.internal-hero-content'),s=getComputedStyle(h);
     if(s.minHeight!=='0px')errors.push('fixed hero height: '+s.minHeight);
     const first=h.firstElementChild.getBoundingClientRect(),r=h.getBoundingClientRect();
     if(first.top-r.top-parseFloat(s.paddingTop)>32)errors.push('empty space before title');
    }
    return errors;
   });
   assert.deepEqual(issues,[],slug+' @ '+width);checked++;
  }
  console.log('PASS: 15 internal pages @ '+width+'px');
 }
}finally{await b.close()}console.log('PASS: '+checked+' layouts; photos, hero spacing, text and buttons.');})().catch(e=>{console.error(e);process.exit(1)});

