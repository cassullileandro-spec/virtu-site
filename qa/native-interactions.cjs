const assert=require('assert/strict'),fs=require('fs'),puppeteer=require(process.env.PUPPETEER_MODULE||'/Users/leandrocassulli/.npm/_npx/0f94ee7615faf582/node_modules/puppeteer-core');
(async()=>{const b=await puppeteer.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});const errors=[];const p=await b.newPage();p.on('pageerror',e=>errors.push(e.message));const base=process.env.QA_URL||'http://127.0.0.1:4180';
try{
 const width=Number(process.env.QA_WIDTH||1440);await p.setViewport({width,height:844,deviceScaleFactor:2,isMobile:width<=700,hasTouch:width<=700});
 for(const file of fs.readdirSync('dist').filter(f=>f.endsWith('.html'))){
  await p.goto(base+'/'+file,{waitUntil:'networkidle0'});await p.evaluate(()=>document.fonts.ready);
  const state=await p.evaluate(()=>({zoom:getComputedStyle(document.querySelector('main')).zoom,body:getComputedStyle(document.querySelector('main p')).fontSize,gsap:!!window.gsap,animations:gsap.globalTimeline.getChildren().length}));
  if(width<=700){
   await p.evaluate(()=>scrollTo(0,document.body.scrollHeight));await new Promise(r=>setTimeout(r,1600));
   const hidden=await p.evaluate(()=>[...document.querySelectorAll('.approved-stack>*')].filter(n=>getComputedStyle(n).visibility==='hidden'||Number(getComputedStyle(n).opacity)<.99).length);
   assert.equal(hidden,0,file+' content remains visible after scroll');
  }
  assert.equal(state.zoom,'1',file);assert.equal(state.body,width<=700?'16px':'18px',file);assert(state.gsap&&state.animations>0,file+' original motion active');
 }
 await p.goto(base+'/index.html',{waitUntil:'networkidle0'});await (width<=700?p.tap('.menu-toggle'):p.click('.menu-toggle'));assert(await p.$eval('#menu',d=>d.open));await p.keyboard.press('Escape');assert.equal(await p.$eval('#menu',d=>d.open),false);
 await p.$eval('.journey summary',n=>n.click());assert(await p.$eval('.journey',n=>n.open));
 await p.$eval('.faq summary',n=>n.click());assert(await p.$eval('.faq',n=>n.open));
 await p.$eval('[data-next]',n=>n.click());assert((await p.$eval('.challenge-count',n=>n.textContent)).startsWith('02'));
 await p.$eval('[data-video]',n=>n.click());assert(await p.$eval('#video-dialog',n=>n.open));await p.$eval('#video-dialog [data-close]',n=>n.click());await p.waitForFunction(()=>document.querySelector('#video-dialog video').paused);
 await p.$eval('[data-contact]',n=>n.click());assert(await p.$eval('#contact-dialog',n=>n.open));await p.keyboard.press('Escape');
 for(const slug of ['contato','trabalhe']){
  await p.goto(base+'/'+slug+'.html',{waitUntil:'networkidle0'});
  const valid=await p.$eval('#inquiry-form',f=>f.checkValidity());assert.equal(valid,false);
  await p.evaluate(()=>{window.open=url=>{window.__draft=url};const form=document.querySelector('#inquiry-form');for(const n of form.elements){if(n.disabled||!n.name)continue;if(n.tagName==='SELECT'){const o=[...n.options].find(x=>x.value);if(o)n.value=o.value;}else if(n.type!=='submit')n.value=n.type==='email'?'teste@example.com':n.type==='tel'?'41999999999':n.type==='url'?'https://example.com':n.type==='date'?'2026-12-01':'Teste de validação';}form.requestSubmit()});
  assert((await p.evaluate(()=>window.__draft))?.startsWith('https://wa.me/5541999693214?text='));
 }
 assert.deepEqual(errors,[]);
 console.log('PASS: Retina '+width+'px, 16 motion runtimes, menu, FAQ, journeys, carousel, video, contact dialog and forms without sending.');
}finally{await b.close()}})().catch(e=>{console.error(e);process.exit(1)});
