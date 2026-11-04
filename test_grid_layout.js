// Run read-only in the rendered home, at each tested viewport and scroll position.
() => {
  const assert = (condition, message) => { if (!condition) throw new Error(message); };
  const width = document.documentElement.clientWidth;
  const bounds = selector => document.querySelector(selector).getBoundingClientRect();
  assert(document.documentElement.scrollWidth <= width + 1, 'Page overflows horizontally');
  const content = [...document.querySelectorAll('main h1, main h2, main h3, main p, main .button')];
  for (const element of content) {
    const rect = element.getBoundingClientRect();
    if (!rect.width || !rect.height) continue;
    assert(rect.left >= -1 && rect.right <= width + 1, `Content outside viewport: ${element.textContent.slice(0, 60)}`);
  }
  const faqDelta = Math.abs(bounds('.faq-section .display').top - bounds('.faq-list').top);
  const titleBreakMargin = getComputedStyle(document.querySelector('.statement span')).marginTop;
  assert(titleBreakMargin === '0px', 'Extra paragraph-like gap inside the intro heading');
  if (width > 900) {
    assert(faqDelta < 1, 'FAQ heading and list do not share top');
    for (const [photo, copy] of [['.intro-image', '.intro-copy'], ['.about-photo', '.about-copy']]) {
      const a = bounds(photo), b = bounds(copy);
      assert(Math.abs(a.top - b.top) < 1, `${photo}: top misalignment`);
      assert(Math.abs(b.left - a.right - 24) < 1, `${photo}: incorrect gutter`);
    }
  }
  const reviewing = new URLSearchParams(location.search).get('grid') === '1';
  const root = document.querySelector('#grid-review')?.shadowRoot;
  assert(Boolean(root) === reviewing, 'Review layer activation mismatch');
  if (root) {
    const svg = root.querySelector('svg');
    assert(svg.children.length > 0, 'Grid is empty');
    assert(getComputedStyle(svg).pointerEvents === 'none', 'Drawing blocks page interactions');
    const photo = bounds('.about-photo');
    if (photo.top >= 0 && photo.top < innerHeight) {
      const drawn = [...svg.querySelectorAll('rect')].some(rect =>
        Math.abs(Number(rect.getAttribute('x')) - photo.x) < 1 &&
        Math.abs(Number(rect.getAttribute('y')) - photo.y) < 1 &&
        Math.abs(Number(rect.getAttribute('width')) - photo.width) < 1 &&
        Math.abs(Number(rect.getAttribute('height')) - photo.height) < 1);
      assert(drawn, 'Photo outline does not match its rendered bounds');
    }
  }
  return {width, height: innerHeight, reviewing, faqDelta, titleBreakMargin, documentHeight: document.documentElement.scrollHeight, passed: true};
}
