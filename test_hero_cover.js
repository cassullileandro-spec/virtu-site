// Run in the rendered home at desktop, tablet and mobile widths.
() => {
  const assert = (ok, message) => { if (!ok) throw new Error(message); };
  const hero = document.querySelector('.cover-hero');
  const portrait = hero.querySelector('.cover-portrait');
  const title = hero.querySelector('h1');
  const action = hero.querySelector('.button');
  assert(document.documentElement.scrollWidth <= innerWidth + 1, 'Horizontal overflow');
  assert(portrait.complete && portrait.naturalWidth === 1024, 'Original cover portrait missing');
  assert(getComputedStyle(portrait).filter.includes('grayscale(1)'), 'Portrait must match monochrome cover');
  assert(document.fonts.check('400 32px "Editors Note"') && document.fonts.check('italic 400 32px "Editors Note"'), 'Cover fonts missing');
  assert(getComputedStyle(title).fontFamily.includes('Editors Note'), 'Cover title font');
  assert(getComputedStyle(hero).backgroundColor === 'rgb(156, 156, 156)', 'Cover background');
  assert(action.hasAttribute('data-contact'), 'Contact interaction missing');
  for (const el of [...title.children, ...hero.querySelector('.cover-copy').children]) {
    const box = el.getBoundingClientRect();
    assert(box.left >= 0 && box.right <= innerWidth + 1, 'Cover text outside viewport');
    assert(box.bottom <= hero.getBoundingClientRect().bottom, 'Cover content clipped');
  }
  assert(getComputedStyle(hero.querySelector('.cover-wordmark')).zIndex !== '2', 'Wordmark must stay behind portrait');
  for (const el of document.querySelectorAll('.hero-grid,.review-grid,.grid-toggle,#grid-review')) {
    assert(getComputedStyle(el).display === 'none', 'Review grid visible');
  }
  return 'Cover composition, assets, fonts, responsive bounds and CTA passed';
}
