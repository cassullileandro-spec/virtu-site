// Run in the rendered internal page, with fonts loaded and ?grid=1.
() => {
 const issues = [], width = document.documentElement.clientWidth;
 const near = (a, b, label) => { if (Math.abs(a - b) > 1) issues.push(`${label}: ${a} / ${b}`); };
 if (document.fonts.status !== 'loaded') issues.push('Fonts not loaded');
 for (const e of document.querySelectorAll('main h1, main h2, main h3, main p')) {
  const box = e.getBoundingClientRect();
  if (!box.width || !box.height) continue;
  const range = document.createRange(); range.selectNodeContents(e);
  if ([...range.getClientRects()].some(r => r.width && (r.left < box.left - 2 || r.right > box.right + 2)))
   issues.push('Text outside column: ' + e.textContent.slice(0, 65));
 }
 const hero = document.querySelector('.internal-hero-bottom');
 const action = hero?.querySelector('.actions');
 if (hero && action && innerHeight > 450) {
  const r = hero.getBoundingClientRect(), a = action.getBoundingClientRect();
  near(a.left, r.left, 'Hero action axis');
 }
 for (const section of document.querySelectorAll('.closing-section')) {
  const copy = section.querySelector('.closing-copy'), action = section.querySelector('.actions');
  if (copy && action && width > 900) near(copy.getBoundingClientRect().bottom, action.getBoundingClientRect().bottom, 'Closing content baseline');
 }
 for (const section of document.querySelectorAll('.page-section')) {
  const s = getComputedStyle(section), r = section.getBoundingClientRect();
  const wrap = section.querySelector('.page-wrap').getBoundingClientRect();
  if (!section.matches('.image-section,.speaker-section')) near(wrap.left, r.left + Number.parseFloat(s.paddingLeft), 'Section container axis');

 }
 if (issues.length) throw new Error(issues.join(' / '));
 return {page:location.pathname,width,height:innerHeight,passed:true};
}
