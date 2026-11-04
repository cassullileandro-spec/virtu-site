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
  const near = (a, b) => Math.abs(a - b) < 1;
  assert(near(bounds('.hero h1').top - bounds('.hero-kicker').bottom, 24), 'Hero kicker gap');
  assert(near(bounds('.hero-bottom').top - bounds('.hero h1').bottom, 32), 'Hero description gap');
  assert(bounds('.hero .button').bottom <= bounds('.hero').bottom - 48, 'Hero CTA clipped');
  if (width <= 700) assert(near(bounds('.hero .button').top - bounds('.hero-bottom > p').bottom, 24), 'Hero CTA gap');
  for (const section of document.querySelectorAll('main > .section-pad')) {
    const css = getComputedStyle(section), expected = width <= 700 ? '64px' : width <= 1100 ? '80px' : '96px';
    assert(css.paddingTop === expected && css.paddingBottom === expected, 'Inconsistent section padding');
  }
  for (const heading of document.querySelectorAll('.intro-copy h3,.about-copy h2,.journey h3')) {
    const style = getComputedStyle(heading);
    assert(style.lineHeight === style.fontSize, 'Inconsistent compact heading leading');
    assert(style.textBoxTrim === 'trim-both', 'Optical top alignment is not active in this browser');
  }
  const aboutHeading = document.querySelector('.about-copy h2');
  assert(getComputedStyle(aboutHeading).lineHeight === getComputedStyle(aboutHeading.querySelector('span')).lineHeight, 'Different leading at the colored title break');
  for (const row of document.querySelectorAll('.journey summary')) {
    const thumbnail = row.querySelector('.journey-thumb').getBoundingClientRect();
    if (thumbnail.width) assert(near(thumbnail.top, row.querySelector('h3').getBoundingClientRect().top), 'Journey image/title top mismatch');
  }
  if (width > 900) assert(near(bounds('.about-photo').bottom, bounds('.about-copy > .button').bottom), 'Portrait and CTA bottom mismatch');
  for (const block of document.querySelectorAll('.intro-copy,.about-copy')) {
    const heading = block.querySelector('h2,h3'), paragraphs = [...block.querySelectorAll('p')];
    assert(near(paragraphs[0].getBoundingClientRect().top - heading.getBoundingClientRect().bottom, 32), 'Heading/body gap mismatch');
    for (let i = 1; i < paragraphs.length; i++) assert(near(paragraphs[i].getBoundingClientRect().top - paragraphs[i-1].getBoundingClientRect().bottom, 24), 'Paragraph gap mismatch');
    if (width <= 900) assert(near(block.querySelector('.button').getBoundingClientRect().top - paragraphs[paragraphs.length-1].getBoundingClientRect().bottom, 32), 'Body/CTA margins accumulated');
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
