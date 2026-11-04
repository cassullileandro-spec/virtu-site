// Opt-in drawing layer: no layout changes, tracking or external dependencies.
(() => {
  if (new URLSearchParams(location.search).get('grid') !== '1') return;
  const sections = [...document.querySelectorAll('main > section, .site-footer')];
  const host = document.createElement('div');
  host.id = 'grid-review';
  document.body.append(host);
  const root = host.attachShadow({mode: 'open'});
  root.innerHTML = `<style>
    :host{all:initial;position:fixed;inset:0;z-index:9999;pointer-events:none;font:12px/1.5 system-ui,sans-serif;color:#f8fafc}
    *{box-sizing:border-box}svg{position:absolute;inset:0;width:100%;height:100%;overflow:hidden}
    aside{position:absolute;right:16px;bottom:16px;width:312px;max-width:calc(100vw - 32px);background:#14212bef;border:1px solid #7dd3fc66;border-radius:10px;padding:14px;pointer-events:auto;box-shadow:0 8px 32px #0004}
    header{display:flex;align-items:center;justify-content:space-between;gap:12px}strong{font-size:14px}button,select{font:inherit;color:inherit;background:#223643;border:1px solid #7193a4;border-radius:4px;min-height:32px;padding:4px 8px}
    button{cursor:pointer}select{width:100%;margin:10px 0}label{display:flex;align-items:center;gap:6px;min-height:30px}input{accent-color:#38bdf8}
    .layers{display:grid;grid-template-columns:1fr 1fr;gap:0 8px}p{margin:8px 0 0;color:#d5e4ec}output{display:block;margin-top:8px;font-variant-numeric:tabular-nums;color:#a5e6fc}
    a{color:#a5e6fc}details summary{cursor:pointer;margin-top:8px}button:focus-visible,select:focus-visible,input:focus-visible,a:focus-visible{outline:2px solid #fff;outline-offset:3px}
    [hidden]{display:none!important}@media(max-width:700px){aside{right:8px;bottom:8px;padding:10px;width:280px;max-width:calc(100vw - 16px)}}
  </style><svg aria-hidden="true"></svg><aside aria-label="Revisão visual do layout">
    <header><strong>Grid · Virtù</strong><button type="button" aria-expanded="true">Recolher</button></header>
    <div class="controls"><label for="section">Ir para seção</label><select id="section"></select>
    <div class="layers"><label><input id="columns" type="checkbox" checked>Colunas</label><label><input id="horizontal" type="checkbox" checked>Horizontais</label><label><input id="blocks" type="checkbox" checked>Blocos</label><label><input id="rhythm" type="checkbox">Malha de 8 px</label></div>
    <output></output><details><summary>Como ler o desenho</summary><p>Rosa: colunas. Azul: referências fixas a cada 32 px e subdivisões de 8 px, a partir do início da área interna da seção. Roxo tracejado: limites e padding observados. Verde: caixas medidas.</p><p>Δx é a distância ao eixo global mais próximo, não um erro automático. Cards têm recuos internos; as fotos editoriais ocupam meia tela. As caixas não são o contorno das letras nem a baseline. Textos mantêm sua altura natural; a malha não acompanha cada elemento.</p></details>
    <p><a href="${location.pathname}">Sair da revisão</a> · animações de entrada pausadas</p></div></aside>`;
  const svg = root.querySelector('svg');
  const select = root.querySelector('select');
  const output = root.querySelector('output');
  const ns = 'http://www.w3.org/2000/svg';
  const targets = ':scope > h2, .hero-title-block, .hero-bottom > p, .hero-action, .trust-heading, .logo-strip, .intro-image, .intro-copy > *, .film-top, .film-bottom, .journeys-list, .journey[open] .journey-content, .challenge-slides, .about-photo, .about-copy > *, .quote-layout blockquote, .faq-section .display, .faq-list, .contact-bottom, .footer-top > p, .footer-top > div, .footer-bottom, .page-wrap > *, .content-grid > *';
  let expanded = true;
  let queued = false;
  sections.forEach((section, index) => {
    const option = document.createElement('option');
    option.value = index;
    option.textContent = `${String(index + 1).padStart(2, '0')} · ${section.id || section.classList[0]}`;
    select.append(option);
  });
  function shape(tag, attrs, text) {
    const element = document.createElementNS(ns, tag);
    for (const [name, value] of Object.entries(attrs)) element.setAttribute(name, value);
    if (text) element.textContent = text;
    svg.append(element);
    return element;
  }
  function line(x1, y1, x2, y2, color, dash = '') {
    shape('line', {x1, y1, x2, y2, stroke: color, 'stroke-width': 1, 'stroke-dasharray': dash});
  }
  function label(x, y, text, color = '#38bdf8') {
    const width = text.length * 6.5 + 12;
    x = Math.min(Math.max(2, x), innerWidth - width - 2);
    if (y < 0 || y > innerHeight - 18) return;
    shape('rect', {x, y, width, height: 18, rx: 2, fill: '#13222df2'});
    shape('text', {x: x + 6, y: y + 13, fill: color, 'font-size': 11, 'font-family': 'monospace'}, text);
  }
  function checked(id) { return root.getElementById(id).checked; }
  function draw() {
    queued = false;
    svg.replaceChildren();
    const width = document.documentElement.clientWidth;
    const reference = document.querySelector('.section-pad');
    const margin = parseFloat(getComputedStyle(reference).paddingLeft);
    const gap = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--gap'));
    const count = width <= 700 ? 4 : 12;
    const column = (width - margin * 2 - gap * (count - 1)) / count;
    const starts = Array.from({length: count}, (_, i) => margin + i * (column + gap));
    if (checked('columns')) starts.forEach((x, i) => {
      shape('rect', {x, y: 0, width: column, height: innerHeight, fill: '#f43f5e0b', stroke: '#fb718566', 'stroke-width': .5});
      label(x, 2, String(i + 1), '#fda4af');
    });
    let current = 0;
    sections.forEach((section, index) => {
      const rect = section.getBoundingClientRect();
      if (rect.top <= Math.min(180, innerHeight / 3)) current = index;
      if (rect.bottom < 0 || rect.top > innerHeight) return;
      const style = getComputedStyle(section);
      const top = parseFloat(style.paddingTop), bottom = parseFloat(style.paddingBottom);
      if (checked('rhythm')) {
        const origin = rect.top + top;
        const start = Math.max(0, Math.ceil(-origin / 8));
        for (let i = start; origin + i * 8 < Math.min(rect.bottom, innerHeight); i++) {
          line(margin, origin + i * 8, width - margin, origin + i * 8, i % 4 ? '#38bdf826' : '#0284c799');
        }
      }
      if (checked('horizontal')) {
        [rect.top, rect.top + top, rect.bottom - bottom, rect.bottom].forEach(y => line(0, y, width, y, '#c084fccc', '6 4'));
        if (top) {
          line(margin - 8, rect.top, margin - 8, rect.top + top, '#c084fc');
          label(margin + 4, rect.top + Math.min(top / 2, 40), `padding ↑ ${Math.round(top)} px`, '#c084fc');
        }
        if (bottom) label(margin + 4, rect.bottom - bottom + 8, `padding ↓ ${Math.round(bottom)} px`, '#c084fc');
        const pairs = [['.intro-image', '.intro-copy h3'], ['.about-photo', '.about-copy h2'], ['.faq-section .display', '.faq-list']];
        pairs.forEach(([a, b]) => {
          const first = section.querySelector(a), second = section.querySelector(b);
          if (!first || !second) return;
          const left = first.getBoundingClientRect(), right = second.getBoundingClientRect();
          if (right.left < left.right - 2) return;
          if (Math.max(left.top, right.top) < 0 || Math.min(left.top, right.top) > innerHeight) return;
          const delta = Math.abs(left.top - right.top);
          const color = '#c084fc';
          line(left.left, left.top, right.right, left.top, color, '4 4');
          label(right.left, Math.max(44, Math.min(left.top, right.top) - 40), `topos observados Δy ${Math.round(delta)} px`, color);
        });
      }
      if (checked('blocks')) section.querySelectorAll(targets).forEach(element => {
        const box = element.getBoundingClientRect();
        if (!box.width || !box.height || box.bottom < 0 || box.top > innerHeight || getComputedStyle(element).visibility === 'hidden') return;
        const offset = Math.min(...starts.map(x => Math.abs(x - box.left)));
        const color = '#34d399';
        shape('rect', {x: box.left, y: box.top, width: box.width, height: box.height, fill: 'none', stroke: color, 'stroke-width': 1.5});
        const name = element.id || [...element.classList].find(c => c !== 'display') || element.tagName.toLowerCase();
        const textElement = element.matches('h1,h2,h3,p,blockquote') ? element : element.querySelector('h1,h2,h3,p');
        const textStyle = textElement && getComputedStyle(textElement);
        const leading = checked('rhythm') && textStyle ? ` · fonte ${parseFloat(textStyle.fontSize).toFixed(1)} / linha ${parseFloat(textStyle.lineHeight).toFixed(1)}px` : '';
        label(box.left, Math.max(22, box.top - 19), `${name} · ${Math.round(box.width)}×${Math.round(box.height)}${offset > 2 ? ` · eixo global Δx ${Math.round(offset)}` : ''}${leading}`, color);
      });
    });
    if (root.activeElement !== select) select.value = current;
    const section = sections[current];
    const style = getComputedStyle(section);
    output.textContent = `${width}px · ${count} colunas · gap ${gap}px · margem ${Math.round(margin)}px | ${section.id || section.classList[0]}: padding ${parseFloat(style.paddingTop)}/${parseFloat(style.paddingBottom)}px`;
  }
  function schedule() {
    if (!queued) { queued = true; requestAnimationFrame(draw); }
  }
  select.addEventListener('change', () => sections[Number(select.value)].scrollIntoView({behavior: 'instant', block: 'start'}));
  root.querySelectorAll('input').forEach(input => input.addEventListener('change', schedule));
  root.querySelector('button').addEventListener('click', event => {
    expanded = !expanded;
    root.querySelector('.controls').hidden = !expanded;
    event.currentTarget.textContent = expanded ? 'Recolher' : 'Expandir';
    event.currentTarget.setAttribute('aria-expanded', String(expanded));
  });
  addEventListener('scroll', schedule, {passive: true});
  addEventListener('resize', schedule);
  document.addEventListener('toggle', schedule, true);
  new ResizeObserver(schedule).observe(document.querySelector('main'));
  document.fonts.ready.then(schedule);
  draw();
})();
