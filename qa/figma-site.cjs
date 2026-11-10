const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const puppeteer=require(process.env.PUPPETEER_MODULE||'puppeteer-core');
const root=path.resolve(__dirname,'..'),out=process.env.QA_OUTPUT||path.join(root,'qa/artifacts');
const base=process.env.QA_URL||'http://127.0.0.1:4180';
const slugs=fs.readdirSync(path.join(root,'dist')).filter(f=>f.endsWith('.html')).map(f=>f.slice(0,-5));
(async()=>{fs.mkdirSync(out,{recursive:true});const browser=await puppeteer.launch({headless:true,executablePath:process.env.CHROME_BIN||'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});let errors=[],results=[];
try{
 if(process.env.QA_INTERACTIONS_ONLY)results=JSON.parse(fs.readFileSync(path.join(out,'layout-results.json')));
 else await Promise.all([390,1440,1920].map(async width=>{
  const p=await browser.newPage();await p.setViewport({width,height:1000});p.on('pageerror',e=>errors.push(e.message));
  for(const slug of slugs){
   const response=await p.goto(base+'/'+slug+'.html',{waitUntil:'networkidle0'});assert([200,304].includes(response.status()));
   await p.evaluate(async()=>{await document.fonts.ready;document.querySelectorAll('img').forEach(i=>i.loading='eager');await Promise.all([...document.images].map(i=>i.decode().catch(()=>{})))});
   const state=await p.evaluate(({slug,width})=>{
    const visible=n=>n.getClientRects().length&&!n.closest('dialog:not([open]),details:not([open])>.v-answer');
    const outside=[...document.querySelectorAll('p,h1,h2,label,input,textarea')].filter(visible).map(n=>{const r=n.getBoundingClientRect();return {id:n.dataset.nodeId||n.id,t:n.textContent.trim().slice(0,60),x:Math.round(r.x),w:Math.round(r.width),h:Math.round(r.height)}}).filter(r=>r.x< -2||r.x+r.w>width+2);
    const nestedLinks=document.querySelectorAll('a a').length;
    const headings=[...document.querySelectorAll('h1')].filter(visible);
    const badImages=[...document.images].filter(i=>!i.naturalWidth).map(i=>i.currentSrc);
    const tiny=[...document.querySelectorAll('.action>p:first-child')].filter(visible).filter(n=>n.getBoundingClientRect().width<20&&n.textContent.trim().length>8).map(n=>n.dataset.nodeId);
    return {slug,width,height:document.body.scrollHeight,scrollWidth:document.documentElement.scrollWidth,outside,nestedLinks,headings:headings.length,badImages,tiny}
   },{slug,width});
   results.push(state);
   if(width!==1440)await p.screenshot({path:path.join(out,slug+'-'+width+'.png'),fullPage:true});
   assert.equal(state.scrollWidth,width,slug+' horizontal overflow '+width);
   assert.deepEqual(state.outside,[],slug+' content outside viewport '+width);
   assert.deepEqual(state.badImages,[],slug+' broken images');
   assert.deepEqual(state.tiny,[],slug+' collapsed button labels');
   assert.equal(state.nestedLinks,0,slug+' nested links');
   assert.equal(state.headings,1,slug+' visible h1');
  }
  await p.close()
 }));
 const p=await browser.newPage();p.on('pageerror',e=>errors.push(e.message));await p.setViewport({width:390,height:844});
 await p.goto(base+'/',{waitUntil:'networkidle0'});await p.click('.menu-toggle');assert(await p.$eval('#site-menu',n=>n.open));await p.keyboard.press('Escape');assert.equal(await p.$eval('#site-menu',n=>n.open),false);
 await p.$eval('.v-details summary',n=>n.click());assert(await p.$eval('.v-details',n=>n.open));
 await p.$eval('[data-name="faq-list"] summary',n=>n.click());assert(await p.$eval('[data-name="faq-list"] details',n=>n.open));
 await p.$eval('[data-slide-step="1"]',n=>n.click());assert((await p.$eval('[data-slide-count]',n=>n.textContent)).startsWith('02'));
 await p.$eval('[data-play-video]',n=>n.click());assert(await p.$eval('#site-video',n=>n.open));await p.$eval('.close-video',n=>n.click());await p.waitForFunction(()=>document.querySelector('video').paused);
 for(const slug of ['contato','trabalhe']){
  await p.goto(base+'/'+slug+'.html?tema=palestra-influencia-real',{waitUntil:'networkidle0'});
  assert.equal(await p.$eval('form',f=>f.checkValidity()),false,'required form validation');
  await p.evaluate(()=>{window.open=(url)=>{window.__opened=url;return null};for(const f of document.querySelector('form').elements){if(!f.name)continue;f.value=f.type==='email'?'teste@example.com':f.type==='tel'?'41999999999':f.type==='url'?'https://example.com/curriculo':'Teste de validação'}document.querySelector('form').requestSubmit()});
  const url=await p.evaluate(()=>window.__opened);assert(url?.startsWith('https://wa.me/5541999693214?text='),'WhatsApp handoff');assert(decodeURIComponent(url).includes('Teste de validação'));
 }
 assert.deepEqual(errors,[]);
 fs.writeFileSync(path.join(out,'report.json'),JSON.stringify({passed:true,layouts:results,interactions:['menu','FAQ','jornadas','carrossel','vídeo','formulários validados sem envio']},null,2));
 console.log(JSON.stringify({passed:true,pages:slugs.length,layouts:results.length,interactions:7,output:out}));
}finally{await browser.close();if(results.length)fs.writeFileSync(path.join(out,'layout-results.json'),JSON.stringify(results,null,2))}
})().catch(e=>{console.error(e);process.exit(1)});
