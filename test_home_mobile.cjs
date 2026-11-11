const assert=require('node:assert/strict'),fs=require('node:fs'),puppeteer=require('/Users/leandrocassulli/.npm/_npx/0f94ee7615faf582/node_modules/puppeteer-core');
const base=process.env.QA_URL||'http://127.0.0.1:4180',out='/tmp/virtu-home-review';
(async()=>{fs.mkdirSync(out,{recursive:true});const b=await puppeteer.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});const results=[];try{
for(const width of (process.env.QA_WIDTHS||'360,390,430,700,701,768,1440').split(',').map(Number)){
 const p=await b.newPage(),errors=[];p.on('pageerror',e=>errors.push(e.message));
 await p.setViewport({width,height:844,isMobile:width<=700,hasTouch:width<=700});
 await p.goto(base+'/index.html',{waitUntil:'networkidle0'});
 await p.evaluate(async()=>{await document.fonts.ready;document.documentElement.style.scrollBehavior='auto';document.querySelectorAll('img').forEach(i=>i.loading='eager');await Promise.all([...document.images].map(i=>i.decode().catch(()=>{})))});
 await new Promise(r=>setTimeout(r,2000));
 for(const selector of ['.cover-hero','.trust','.impact','.intro','.film','.home-talks','.journeys','.challenges','.about','.testimonial','.faq-section','.contact','.site-footer']){
  await p.$eval(selector,n=>n.scrollIntoView());await new Promise(r=>setTimeout(r,160));
 }
 await new Promise(r=>setTimeout(r,1600));
 const state=await p.evaluate(()=>{
  const visible=n=>{for(let x=n;x;x=x.parentElement){const s=getComputedStyle(x);if(s.visibility==='hidden'||s.display==='none'||+s.opacity===0)return false}return true};
  const imgs=[...document.querySelectorAll('main img')].filter(n=>!n.closest('details'));
  const buttons=[...document.querySelectorAll('main .button')].filter(n=>!n.closest('details'));
  return {width:innerWidth,overflow:document.documentElement.scrollWidth-innerWidth,missing:imgs.filter(n=>!n.naturalWidth||!visible(n)||(n.closest('.intro-image,.about-photo')?.getBoundingClientRect().height??1)<1).map(n=>n.src),buttons:buttons.map(n=>({text:n.querySelector('span').textContent,visible:visible(n),fits:n.scrollWidth<=n.clientWidth+2})),images:imgs.map(n=>({src:n.currentSrc.split('/').pop(),ratio:n.offsetWidth/n.offsetHeight,natural:n.naturalWidth/n.naturalHeight,fit:getComputedStyle(n).objectFit})),heroCopy:document.querySelector('.cover-copy').textContent};
 });
 assert.equal(state.overflow,0,'overflow '+width);assert.deepEqual(state.missing,[],'missing images '+width);
 assert(state.buttons.every(n=>n.visible&&n.fits&&n.text.trim()),'CTA '+width);
 const cover=await p.evaluate(()=>{const hero=document.querySelector('.cover-hero'),im=hero.querySelector('.cover-portrait'),art=hero.querySelector('.cover-art').getBoundingClientRect(),copy=hero.querySelector('.cover-copy').getBoundingClientRect();return {bg:getComputedStyle(hero).backgroundColor,src:im.currentSrc,filter:getComputedStyle(im).filter,overlap:art.bottom>copy.top+1,wordmark:getComputedStyle(hero.querySelector('.cover-wordmark')).display}});
 assert.equal(cover.bg,'rgb(156, 156, 156)');assert(cover.src.endsWith('hero-cover-portrait.png'));assert(cover.filter.includes('grayscale(1)'));assert.notEqual(cover.wordmark,'none');if(width<=700)assert(!cover.overlap,'home cover copy must follow the artwork');
 assert(state.heroCopy.includes('Sua estratégia ganha força')&&state.heroCopy.includes('Quero conversar sobre minha empresa'));
 if(width<=700) for(const im of state.images.filter(n=>!n.src.includes('logo')&&!n.src.includes('.png')))assert(im.fit==='contain'||Math.abs(im.ratio-im.natural)<.02,'distorted/cropped '+im.src);
 if(width===390){
  await p.evaluate(()=>scrollTo(0,0));await new Promise(r=>setTimeout(r,600));await p.screenshot({path:out+'/hero.png'});
  for(const sel of ['.cover-copy','.intro','.film','.home-talks','.about','.site-footer']){await p.$eval(sel,n=>n.scrollIntoView());await new Promise(r=>setTimeout(r,600));await p.screenshot({path:out+'/'+sel.slice(1)+'.png'});}
 }
 for(let i=0;i<6;i++){
  const sel='#jornada-'+i;await p.$eval(sel+' summary',n=>n.click());await new Promise(r=>setTimeout(r,550));
  const panel=await p.$eval(sel+' .journey-panel',n=>{const im=n.querySelector('img');return {src:im.currentSrc,w:im.offsetWidth,h:im.offsetHeight,natural:im.naturalWidth/im.naturalHeight,scroll:n.scrollHeight,height:n.clientHeight,text:n.querySelector('.button').textContent}});
  assert(panel.height>=panel.scroll-2,'clipped journey '+i);
  assert.equal((panel.text.match(/↗/g)||[]).length,1,'duplicate CTA arrow');
  if(width<=700){assert(panel.src.includes('-art-v2.jpg'));assert(Math.abs(panel.w/panel.h-panel.natural)<.02);}
  if(width===390&&[0,1,3,5].includes(i)){await p.$eval(sel+' .journey-panel',n=>n.scrollIntoView());await new Promise(r=>setTimeout(r,600));await p.screenshot({path:out+'/journey-'+i+'.png'});}
  await p.$eval(sel+' summary',n=>n.click());
 }
 await p.$eval('.cover-copy .button',n=>n.click());assert(await p.$eval('#contact-dialog',n=>n.open));await p.keyboard.press('Escape');
 await p.click('.menu-toggle');assert(await p.$eval('#menu',n=>n.open));await p.keyboard.press('Escape');
 await p.$eval('.faq summary',n=>n.click());assert(await p.$eval('.faq',n=>n.open));
 await p.$eval('[data-video]',n=>n.click());assert(await p.$eval('#video-dialog',n=>n.open));await p.keyboard.press('Escape');
 await p.$eval('[data-next]',n=>n.click());assert((await p.$eval('.challenge-count',n=>n.textContent)).startsWith('02'));
 assert.deepEqual(errors,[]);results.push(state);console.log('PASS home '+width+'px: images, copy, CTAs, 6 journeys, menu, FAQ, video and carousel');await p.close();
}
fs.writeFileSync(out+'/results.json',JSON.stringify(results,null,2));
}finally{await b.close()}})().catch(e=>{console.error(e);process.exitCode=1});
