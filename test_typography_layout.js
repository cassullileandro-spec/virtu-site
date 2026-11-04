// Run in a rendered page after its fonts have loaded.
() => {
 const elements = [...document.querySelectorAll('main h1,main h2,main h3,main h4,main p,main blockquote')];
 const width = document.documentElement.clientWidth;
 const issues = [];
 for (const e of elements) {
  const r = e.getBoundingClientRect(), s = getComputedStyle(e);
  if (!r.width || !r.height) continue;
  if (r.left < -1 || r.right > width + 1) issues.push('Overflow: ' + e.textContent.slice(0,50));
  if (s.textBoxTrim !== 'trim-both' || s.textBoxEdge !== 'cap alphabetic') issues.push('Optical trim missing: ' + e.tagName);
 }
 if (issues.length) throw new Error(issues.join(' / '));
 return {page:location.pathname,width,checked:elements.length,passed:true};
}
