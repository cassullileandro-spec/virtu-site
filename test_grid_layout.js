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
      assert(Math.abs(b.left - a.right - Number.parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--gap'))) < 1, `${photo}: incorrect gutter`);
    }
  }
  const near = (a, b) => Math.abs(a - b) < 1;
  if (width > 700 && width <= 1100) {
    assert(near(bounds('.journeys-list').left, bounds('#journeys-title').left), 'Hidden guide leaves empty columns before journeys');
  }
  if (width <= 700) {
    const footer = document.querySelector('.footer-top');
    assert(near(bounds('.footer-top>div').top - bounds('.footer-top>p').bottom, Number.parseFloat(getComputedStyle(footer).rowGap)), 'Footer gap includes a leftover paragraph margin');
  }
  assert(bounds('.hero .button').bottom <= bounds('.hero').bottom - 32, 'Hero CTA clipped');
  assert(near(bounds('.hero .button').top - bounds('.cover-copy > p:last-of-type').bottom, width <= 700 ? 24 : 28), 'Hero CTA gap');
  for (const section of document.querySelectorAll('main > .section-pad')) {
    const css = getComputedStyle(section), expected = width <= 700 ? '64px' : width <= 1100 ? '80px' : '96px';
    assert(css.paddingTop === expected && css.paddingBottom === expected, 'Inconsistent section padding');
  }
  for (const heading of document.querySelectorAll('.intro-copy h3,.about-copy h2')) {
    const style = getComputedStyle(heading);
    assert(style.lineHeight === getComputedStyle(document.documentElement).getPropertyValue('--line-title').trim(), 'Inconsistent section heading leading');
    assert(style.textBoxTrim === 'trim-both', 'Optical top alignment is not active in this browser');
  }
  const bodyStyles = [...document.querySelectorAll('.intro-copy p,.about-copy p')].map(el => {const s=getComputedStyle(el);return s.fontSize+'/'+s.lineHeight;});
  assert(new Set(bodyStyles).size === 1, 'Body copy uses competing size/leading roles');
  const aboutHeading = document.querySelector('.about-copy h2');
  assert(getComputedStyle(aboutHeading).lineHeight === getComputedStyle(aboutHeading.querySelector('span')).lineHeight, 'Different leading at the colored title break');
  for (const row of document.querySelectorAll('.journey summary')) {
    const thumbnail = row.querySelector('.journey-thumb').getBoundingClientRect();
    if (thumbnail.width) assert(near(thumbnail.top, row.querySelector('h3').getBoundingClientRect().top), 'Journey image/title top mismatch');
  }
  if (width > 900) {
    for (const [photo, copy] of [['.intro-image','.intro-copy'],['.about-photo','.about-copy']]) {
      const gap = Number.parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--gap'));
      assert(near(bounds(photo).width,(width-gap)/2), 'Editorial photo must end at column 6');
      for (const element of document.querySelector(copy).children) assert(near(element.getBoundingClientRect().left,(width+gap)/2), 'Editorial text/CTA must start at column 7');
      assert(near(bounds(photo).left,0), 'Editorial photo does not reach page edge');
      const inset=width<=1100?80:96;
      assert(near(bounds(photo).bottom-bounds(copy+' > .button').bottom,inset), 'Editorial bottom inset mismatch');
    }
  }
  for (const block of document.querySelectorAll('.intro-copy,.about-copy')) {
    const heading = block.querySelector('h2,h3'), paragraphs = [...block.querySelectorAll('p')];
    assert(near(paragraphs[0].getBoundingClientRect().top - heading.getBoundingClientRect().bottom, 32), 'Heading/body gap mismatch');
    for (let i = 1; i < paragraphs.length; i++) assert(near(paragraphs[i].getBoundingClientRect().top - paragraphs[i-1].getBoundingClientRect().bottom, 24), 'Paragraph gap mismatch');
    assert(near(block.querySelector('.button').getBoundingClientRect().top - paragraphs[paragraphs.length-1].getBoundingClientRect().bottom, width > 900 ? 64 : 48), 'Body/CTA margins accumulated');
  }
  const reviewing = new URLSearchParams(location.search).get('grid') === '1';
  const root = document.querySelector('#grid-review')?.shadowRoot;
  assert(Boolean(root) === reviewing, 'Review layer activation mismatch');
  if (root) {
    const svg = root.querySelector('svg');
    assert(svg.children.length > 0, 'Grid is empty');
    assert(getComputedStyle(svg).pointerEvents === 'none', 'Drawing blocks page interactions');
    const reference = document.querySelector('.section-pad');
    const margin = Number.parseFloat(getComputedStyle(reference).paddingLeft);
    const gap = Number.parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--gap'));
    const count = width <= 700 ? 4 : 12;
    const columns = [...svg.querySelectorAll('rect')].filter(r => r.getAttribute('fill') === '#f43f5e0b');
    if (root.querySelector('#columns').checked) {
      assert(columns.length === count, 'Wrong number of guide columns');
      for (let i = 0; i < count; i++) assert(near(Number(columns[i].getAttribute('x')), margin + i * ((width - 2 * margin + gap) / count)), 'Column guide differs from layout tracks');
    }
    const strong = [...svg.querySelectorAll('line')].filter(l => l.getAttribute('stroke') === '#0284c799');
    for (const l of strong) {
      const y = Number(l.getAttribute('y1'));
      assert([...document.querySelectorAll('main>section,.site-footer')].some(section => {
        const box = section.getBoundingClientRect(), origin = box.top + Number.parseFloat(getComputedStyle(section).paddingTop);
        return y >= origin - .1 && y <= box.bottom && near((y-origin)/32, Math.round((y-origin)/32));
      }), 'Strong guide follows an element instead of the fixed 32px reference');
    }
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
