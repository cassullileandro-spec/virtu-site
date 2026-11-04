'use strict';
const $ = (selector, root = document) => root.querySelector(selector);
const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];
const reduced = matchMedia('(prefers-reduced-motion: reduce)');
const gridReview = new URLSearchParams(location.search).get('grid') === '1';
if (gridReview) {
  const script = document.createElement('script');
  script.src = 'grid-review.js';
  document.head.append(script);
}
const menu = $('#menu');
const menuToggle = $('.menu-toggle');
const contactDialog = $('#contact-dialog');
const videoDialog = $('#video-dialog');
const video = videoDialog ? $('video', videoDialog) : null;
let lastFocus;
function openDialog(dialog, trigger) {
  lastFocus = trigger || document.activeElement;
  dialog.showModal();
  if (dialog === menu) menuToggle.setAttribute('aria-expanded', 'true');
  if (!reduced.matches && window.gsap) gsap.fromTo(dialog, {autoAlpha: 0, y: 18}, {autoAlpha: 1, y: 0, duration: .35, ease: 'power2.out'});
}
function closeDialog(dialog) {
  dialog.close();
}
$$('dialog').forEach(dialog => {
  $$('[data-close]', dialog).forEach(button => button.addEventListener('click', () => closeDialog(dialog)));
  dialog.addEventListener('click', e => { if(e.target === dialog && dialog !== menu) {const r=dialog.getBoundingClientRect(); if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom) closeDialog(dialog);}});
  dialog.addEventListener('close', () => {
    if(dialog === menu) menuToggle.setAttribute('aria-expanded', 'false');
    if(dialog === videoDialog) video.pause();
    lastFocus?.focus({preventScroll: true});
  });
});
menuToggle.addEventListener('click', () => openDialog(menu, menuToggle));
$$('a[href^="#"]', menu).forEach(link => link.addEventListener('click', () => closeDialog(menu)));
$$('[data-contact]').forEach(button => button.addEventListener('click', () => {
  const subject = button.dataset.contact;
  $('#interest').value = subject || 'Conversar sobre minha empresa';
  if(!$('#interest').value) $('#interest').selectedIndex = 0;
  openDialog(contactDialog, button);
}));
$('#contact-form')?.addEventListener('submit', e => {
  e.preventDefault();
  const interest = $('#interest').value;
  const message = $('#message').value.trim();
  const body = `Olá, equipe Virtù! Tenho interesse em: ${interest}.${message ? '\n\n' + message : ''}`;
  window.open('https://wa.me/5541999693214?text=' + encodeURIComponent(body), '_blank', 'noopener,noreferrer');
});
$('[data-video]')?.addEventListener('click', e => {
  openDialog(videoDialog, e.currentTarget);
  video.play().catch(() => { /* Browser may require a second click on native play. */ });
});
// The native details remain usable when JavaScript or animation is unavailable.
$$('.journey, .faq, .topic').forEach(details => {
  details.addEventListener('toggle', () => {
    if(details.open) {
      $$(`details[name="${details.name}"]`).filter(other => other !== details).forEach(other => {other.open = false;});
      const content = $('.journey-panel, .faq-answer, .topic-answer', details);
      if(!reduced.matches && window.gsap) gsap.fromTo(content, {autoAlpha: 0, y: 12}, {autoAlpha: 1, y: 0, duration: .45, ease: 'power2.out'});
    }
    window.ScrollTrigger?.refresh();
  });
});
$$('[data-jump-program]').forEach(link => link.addEventListener('click', () => {
  const item = $('#jornada-' + link.dataset.jumpProgram);
  item.open = true;
  requestAnimationFrame(() => item.scrollIntoView({behavior: reduced.matches ? 'instant' : 'smooth', block: 'start'}));
}));
const slides = $$('.challenge-slide');
let activeSlide = 0;
function changeSlide(index) {
  activeSlide = (index + slides.length) % slides.length;
  slides.forEach((slide, i) => {slide.hidden = i !== activeSlide;});
  $('.challenge-numeral').textContent = String(activeSlide + 1).padStart(2, '0');
  $('.challenge-count').textContent = `${String(activeSlide + 1).padStart(2, '0')} / ${String(slides.length).padStart(2, '0')}`;
  $$('[data-slide-to]').forEach((button, i) => button.setAttribute('aria-pressed', String(i === activeSlide)));
  if(!reduced.matches && window.gsap) gsap.fromTo(slides[activeSlide], {autoAlpha: 0, y: 22}, {autoAlpha: 1, y: 0, duration: .5, ease: 'power2.out'});
}
$('[data-prev]')?.addEventListener('click', () => changeSlide(activeSlide - 1));
$('[data-next]')?.addEventListener('click', () => changeSlide(activeSlide + 1));
$$('[data-slide-to]').forEach(button => button.addEventListener('click', () => changeSlide(Number(button.dataset.slideTo))));
function refreshChrome() {
  menuToggle.classList.toggle('scrolled', scrollY > 90);
  const end = $('#contato').getBoundingClientRect().top < innerHeight * .65;
  $('.floating-contact').classList.toggle('is-visible', scrollY > $('.hero').offsetHeight && !end);
  const total = document.documentElement.scrollHeight - innerHeight;
  $('.reading-progress').style.transform = `scaleX(${total ? Math.min(1, scrollY / total) : 0})`;
}
let scrollQueued = false;
addEventListener('scroll', () => {if(!scrollQueued){scrollQueued=true;requestAnimationFrame(()=>{refreshChrome();scrollQueued=false;});}}, {passive:true});
addEventListener('resize', refreshChrome);
refreshChrome();
if(window.gsap && window.ScrollTrigger && !gridReview) {
  gsap.registerPlugin(ScrollTrigger);
  const mm = gsap.matchMedia();
  mm.add('(prefers-reduced-motion: no-preference)', () => {
    if(!document.body.classList.contains('internal')) {
    const intro = gsap.timeline({defaults: {ease: 'power3.out'}});
    intro.from('.hero-image', {scale: 1.035, duration: 1.8})
      .from('.hero-kicker', {autoAlpha: 0, y: 15, duration: .8}, .1)
      .from('.hero h1 .line > span', {yPercent: 110, duration: 1.15, stagger: .12}, .2)
      .from('.hero-bottom', {autoAlpha: 0, y: 20, duration: .8}, .65);
    // Different motion serves different content: editorial text, photo reveals and a film parallax.
    gsap.from('.statement', {y: 35, autoAlpha: 0, duration: 1.05, scrollTrigger: {trigger: '.statement', start: 'top 92%', once: true}});
    $$('.reveal-image').forEach(frame => gsap.from($('img', frame), {scale: 1.09, duration: 1.5, ease: 'power2.out', scrollTrigger: {trigger: frame, start: 'top 85%', once: true}}));
    gsap.from('.journey summary', {autoAlpha: 0, y: 15, duration: .65, stagger: .08, scrollTrigger: {trigger: '.journeys-list', start: 'top 85%', once: true}});
    gsap.from('.quote-layout blockquote', {autoAlpha: 0, y: 25, duration: .9, scrollTrigger: {trigger: '.testimonial', start: 'top 75%', once: true}});
    gsap.from('.contact h2', {y: 35, autoAlpha: 0, duration: 1, scrollTrigger: {trigger: '.contact', start: 'top 70%', once: true}});
    }
  });
  mm.add('(min-width: 701px) and (prefers-reduced-motion: no-preference)', () => {
    if($('.film-visual img')) gsap.to('.film-visual img', {yPercent: 7, ease: 'none', scrollTrigger: {trigger: '.film', start: 'top bottom', end: 'bottom top', scrub: 1}});
  });
  document.fonts.ready.then(() => ScrollTrigger.refresh());

}
