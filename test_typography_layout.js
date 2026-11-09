// Run in each rendered page after fonts and images have loaded.
() => {
 const width = document.documentElement.clientWidth;
 const root = getComputedStyle(document.documentElement);
 const sizes = new Set(['hero','title','subtitle','body','small'].map(role => root.getPropertyValue('--type-'+role).trim()));
 const elements = [...document.querySelectorAll('main h1,main h2,main h3,main h4,main p,main blockquote,.button,.text-link,.menu-main a,.menu-side>a,input,select,textarea')];
 const issues = [], used = new Set();
 for (const e of elements) {
  const r = e.getBoundingClientRect(), s = getComputedStyle(e);
  if (!r.width || !r.height || e.closest('.sr-only') || s.visibility === 'hidden') continue;
  if (r.left < -1 || r.right > width + 1) issues.push('Overflow: ' + e.textContent.slice(0,50));
  if (!sizes.has(s.fontSize)) issues.push('Size outside five roles: '+s.fontSize+' '+e.textContent.slice(0,40));
  const heading = e.matches('h1,h2,h3,h4,blockquote,.menu-main a') && !e.matches('.faq h3');
  const expected = heading ? 'Editors Note' : 'Geist';
  if (!s.fontFamily.includes(expected)) issues.push('Wrong family: '+e.tagName+' '+s.fontFamily);
  if(e.matches('main p') && !e.matches('.eyebrow,.micro,.small,.form-note,.privacy-note,.footer-mission')) {
   if(s.fontSize !== root.getPropertyValue('--type-body').trim()) issues.push('Body text uses a different size: '+e.textContent.slice(0,40));
  }
  used.add(s.fontSize);
 }
 const hero = document.querySelector('.hero'), heroBox = hero.getBoundingClientRect();
 for (const e of hero.querySelectorAll('h1,p,.button')) {
  const r=e.getBoundingClientRect();
  if(r.top<heroBox.top || r.bottom>heroBox.bottom+1)issues.push('Hero text clipped: '+e.textContent.slice(0,40));
 }
 if(document.documentElement.scrollWidth>width+1)issues.push('Page overflow');
 if(issues.length)throw new Error(issues.join(' / '));
 return {page:location.pathname,width,sizes:[...used],checked:elements.length,passed:true};
}
