'use strict';
// All forms hand a reviewable draft to WhatsApp; the site never sends or stores it.
const inquiry = document.querySelector('#inquiry-form');
if (inquiry) {
  const interest = inquiry.querySelector('#interest');
  const events = inquiry.querySelector('#event-fields');
  const topic = inquiry.querySelector('#theme');
  function updateEventFields() {
    if (!events) return;
    events.hidden = interest.value !== 'Palestra';
    events.querySelectorAll('input,select').forEach(field => { field.disabled = events.hidden; });
  }
  if (interest) {
    const requested = new URLSearchParams(location.search).get('interesse');
    const aliases = {'Palestras':'Palestra','Meta V — Acesso gravado':'Meta V gravado','Super Humanos — Oficina prática':'Oficina Super Humanos'};
    if (requested && [...interest.options].some(o => o.value === (aliases[requested] || requested))) interest.value = aliases[requested] || requested;
    else if (requested && topic && [...topic.options].some(o => o.value === requested)) { interest.value = 'Palestra'; topic.value = requested; }
    interest.addEventListener('change', updateEventFields);
    updateEventFields();
  }
  inquiry.addEventListener('submit', event => {
    event.preventDefault();
    if (!inquiry.reportValidity()) return;
    const lines = [inquiry.dataset.kind === 'trabalhe' ? 'Olá, equipe Virtù! Gostaria de conversar sobre oportunidades de atuação.' : 'Olá, equipe Virtù! Gostaria de conversar sobre meu próximo passo.'];
    inquiry.querySelectorAll('input,select,textarea').forEach(field => {
      if (field.disabled || !field.value.trim()) return;
      const label = field.closest('label');
      const title = label ? [...label.childNodes].filter(n => n.nodeType === Node.TEXT_NODE).map(n => n.textContent.trim()).join(' ') : field.name;
      lines.push(`${title}: ${field.value.trim()}`);
    });
    if (inquiry.dataset.kind === 'trabalhe') lines.push('Posso apresentar meu currículo nesta conversa.');
    window.open('https://wa.me/5541999693214?text=' + encodeURIComponent(lines.join('\n\n')), '_blank', 'noopener,noreferrer');
  });
}
if (window.gsap && window.ScrollTrigger && !gridReview) {
  const motion = gsap.matchMedia();
  motion.add('(prefers-reduced-motion: no-preference)', () => {
    gsap.from('.internal-hero h1', {y:30, autoAlpha:0, duration:1.1, ease:'power3.out'});
    gsap.from('.internal-hero-bottom', {y:20, autoAlpha:0, duration:.9, delay:.25, ease:'power2.out'});
    document.querySelectorAll('.editorial-photo img,.talk-photo img,.approved-media img').forEach(photo => gsap.from(photo, {scale:1.06, duration:1.4, ease:'power2.out', scrollTrigger:{trigger:photo, start:'top 88%', once:true}}));
    document.querySelectorAll('.process-grid,.approved-section > .approved-stack').forEach(group => gsap.from(group.children, {y:24, autoAlpha:0, stagger:.09, duration:.7, scrollTrigger:{trigger:group, start:'top 85%', once:true}}));
  });
}
