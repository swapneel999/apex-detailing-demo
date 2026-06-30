/* ================================================================

   RGDETAILING — app.js

   UI interactions: nav, tabs, scroll-reveal, form validation

   Note: GSAP animations are injected post-audit by the pipeline.

   ================================================================ */



(function () {

  'use strict';



  /* ---------------------------------------------------------------

     NAV — scroll state + mobile menu

  --------------------------------------------------------------- */

  const nav    = document.getElementById('nav');

  const toggle = document.getElementById('navToggle');

  const mobile = document.getElementById('navMobile');



  function onScroll() {

    nav.classList.toggle('scrolled', window.scrollY > 20);

  }

  window.addEventListener('scroll', onScroll, { passive: true });

  onScroll();



  toggle.addEventListener('click', () => {

    const open = toggle.getAttribute('aria-expanded') === 'true';

    const next = !open;

    toggle.setAttribute('aria-expanded', String(next));

    mobile.setAttribute('aria-hidden',   String(!next));

    mobile.classList.toggle('open', next);

  });



  // Close mobile menu when any link inside is clicked

  mobile.querySelectorAll('a').forEach(link => {

    link.addEventListener('click', () => {

      toggle.setAttribute('aria-expanded', 'false');

      mobile.setAttribute('aria-hidden',   'true');

      mobile.classList.remove('open');

    });

  });



  /* ---------------------------------------------------------------

     PACKAGE TABS

  --------------------------------------------------------------- */

  const tabs   = document.querySelectorAll('.pkg-tab');

  const panels = document.querySelectorAll('.pkg-panel');



  tabs.forEach(tab => {

    tab.addEventListener('click', () => {

      const targetId = tab.getAttribute('aria-controls');



      tabs.forEach(t => {

        t.classList.remove('pkg-tab--active');

        t.setAttribute('aria-selected', 'false');

      });

      panels.forEach(p => {

        p.classList.remove('pkg-panel--active');

        p.hidden = true;

      });



      tab.classList.add('pkg-tab--active');

      tab.setAttribute('aria-selected', 'true');



      const panel = document.getElementById(targetId);

      if (panel) {

        panel.classList.add('pkg-panel--active');

        panel.hidden = false;

      }

    });

  });



  /* ---------------------------------------------------------------

     GSAP PREMIUM ANIMATIONS

     Targets: hero text, process steps, package cards.

     Service cards keep the IntersectionObserver path below.

  --------------------------------------------------------------- */

  if (window.gsap && window.ScrollTrigger) {

    gsap.registerPlugin(ScrollTrigger);



    // Set hero elements invisible immediately so there's no flash of

    // visible content before the entrance timeline fires.

    gsap.set(

      '.hero-eyebrow, .ht-line, .hero-sub, .hero-actions, .hero-stats',

      { opacity: 0, y: 32 }

    );



    // Hero entrance — staggered word-by-word title reveal

    gsap.timeline({ defaults: { ease: 'power3.out' }, delay: 0.15 })

      .to('.hero-eyebrow', { opacity: 1, y: 0, duration: 0.75 })

      .to('.ht-line',      { opacity: 1, y: 0, duration: 1.0,  stagger: 0.13 }, '-=0.45')

      .to('.hero-sub',     { opacity: 1, y: 0, duration: 0.75 }, '-=0.5')

      .to('.hero-actions', { opacity: 1, y: 0, duration: 0.65 }, '-=0.35')

      .to('.hero-stats',   { opacity: 1, y: 0, duration: 0.65 }, '-=0.25');



    // Process steps — ScrollTrigger stagger

    // (data-reveal stripped from these elements; GSAP owns them)

    gsap.from('.process-step', {

      scrollTrigger: { trigger: '.process-grid', start: 'top 78%' },

      opacity: 0,

      y: 48,

      duration: 0.9,

      ease: 'power3.out',

      stagger: 0.2,

    });



    // Package cards — ScrollTrigger stagger

    gsap.from('.pkg-card', {

      scrollTrigger: { trigger: '#packages .section-header', start: 'top 65%' },

      opacity: 0,

      y: 32,

      duration: 0.75,

      ease: 'power3.out',

      stagger: 0.13,

    });

    // Hero image parallax
    gsap.to('.hero-img', {
      scrollTrigger: {
        trigger: '#hero',
        start: 'top top',
        end: 'bottom top',
        scrub: 1.8,
      },
      y: '16%',
      ease: 'none',
    });

    // Section header choreography
    gsap.utils.toArray('.section-header').forEach(function (header) {
      var els = [
        header.querySelector('.section-label'),
        header.querySelector('.section-title'),
        header.querySelector('.section-sub'),
      ].filter(Boolean);
      if (els.length === 0) return;
      gsap.from(els, {
        scrollTrigger: { trigger: header, start: 'top 82%' },
        opacity: 0,
        y: 22,
        duration: 0.72,
        ease: 'power3.out',
        stagger: 0.16,
      });
    });
  }



  /* ---------------------------------------------------------------

     SCROLL REVEAL (IntersectionObserver)

     Handles [data-reveal] elements: service cards, suburb grid, etc.

  --------------------------------------------------------------- */

  const revealEls = document.querySelectorAll('[data-reveal]');



  if (revealEls.length && 'IntersectionObserver' in window) {

    const io = new IntersectionObserver(entries => {

      entries.forEach(entry => {

        if (entry.isIntersecting) {

          entry.target.classList.add('visible');

          io.unobserve(entry.target);

        }

      });

    }, { threshold: 0.12 });



    revealEls.forEach(el => io.observe(el));

  } else {

    // Fallback: show everything immediately

    revealEls.forEach(el => el.classList.add('visible'));

  }



  /* ---------------------------------------------------------------

     TEXTAREA CHARACTER COUNTER

  --------------------------------------------------------------- */

  const msgField = document.getElementById('f-message');

  const msgCount = document.getElementById('msg-count');



  if (msgField && msgCount) {

    msgField.addEventListener('input', () => {

      msgCount.textContent = msgField.value.length + ' / 500';

    });

  }



  /* ---------------------------------------------------------------

     QUOTE FORM — validation + submission

  --------------------------------------------------------------- */

  const form = document.getElementById('quoteForm');

  if (!form) return;



  const EMAIL_RE = /^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$/;

  // Australian phone: +61 or 0, then [2-9], then 8 digits

  const PHONE_RE = /^(\+61|0)[2-9]\d{8}$/;



  function fieldEl(id)    { return document.getElementById(id); }

  function errorEl(id)    { return document.getElementById('err-' + id); }



  function setError(id, msg) {

    const input = fieldEl('f-' + id);

    const err   = errorEl(id);

    if (err)   err.textContent = msg;

    if (input) {

      input.classList.toggle('is-error', Boolean(msg));

      input.setAttribute('aria-invalid', Boolean(msg).toString());

    }

  }



  function clearError(id) { setError(id, ''); }



  function validate(data) {

    let ok = true;



    if (!data.name || data.name.length < 2) {

      setError('name', 'Please enter your full name (at least 2 characters).');

      ok = false;

    } else { clearError('name'); }



    if (!data.email || !EMAIL_RE.test(data.email)) {

      setError('email', 'Please enter a valid email address.');

      ok = false;

    } else { clearError('email'); }



    const phone = (data.phone || '').replace(/[\s\-()]/g, '');

    if (!phone || !PHONE_RE.test(phone)) {

      setError('phone', 'Enter a valid Australian phone number (e.g. 0412 345 678).');

      ok = false;

    } else { clearError('phone'); }



    if (!data.vehicle || data.vehicle.length < 2) {

      setError('vehicle', 'Please describe your vehicle (make and model).');

      ok = false;

    } else { clearError('vehicle'); }



    if (!data.package) {

      setError('package', 'Please select a package.');

      ok = false;

    } else { clearError('package'); }



    return ok;

  }



  // Live clear errors on input

  ['name', 'email', 'phone', 'vehicle', 'package'].forEach(id => {

    const el = fieldEl('f-' + id);

    if (el) el.addEventListener('input', () => clearError(id));

  });



  form.addEventListener('submit', async e => {

    e.preventDefault();



    const submitBtn = document.getElementById('submitBtn');

    const status    = document.getElementById('formStatus');



    const data = {

      name:    (fieldEl('f-name')    ? fieldEl('f-name').value.trim()          : ''),

      email:   (fieldEl('f-email')   ? fieldEl('f-email').value.trim().toLowerCase() : ''),

      phone:   (fieldEl('f-phone')   ? fieldEl('f-phone').value.trim()         : ''),

      vehicle: (fieldEl('f-vehicle') ? fieldEl('f-vehicle').value.trim()       : ''),

      package: (fieldEl('f-package') ? fieldEl('f-package').value              : ''),

      message: (fieldEl('f-message') ? fieldEl('f-message').value.trim()       : ''),

    };



    if (!validate(data)) return;



    // Loading state

    submitBtn.classList.add('loading');

    submitBtn.disabled = true;

    status.textContent = '';

    status.className   = 'form-status';



    try {

      // Attempt CSRF token fetch (non-fatal if backend not running)

      let csrf = '';

      try {

        const csrfRes = await fetch('/api/csrf-token', { credentials: 'same-origin' });

        if (csrfRes.ok) {

          const csrfJson = await csrfRes.json();

          csrf = csrfJson.token || '';

        }

      } catch (_) { /* CSRF optional during local dev */ }



      const res  = await fetch('/api/quote', {

        method:      'POST',

        credentials: 'same-origin',

        headers:     { 'Content-Type': 'application/json' },

        body:        JSON.stringify({ ...data, csrf_token: csrf }),

      });



      const json = await res.json().catch(() => ({}));



      if (res.ok && json.success) {

        status.textContent = 'Quote request sent! We will be in touch within 24 hours.';

        status.className   = 'form-status is-success';

        form.reset();

        if (msgCount) msgCount.textContent = '0 / 500';

      } else {

        status.textContent = json.error || 'Something went wrong. Please try again or call us on 0438 781 340.';

        status.className   = 'form-status is-error';

      }

    } catch (_) {

      status.textContent = 'Network error. Please check your connection or call us on 0438 781 340.';

      status.className   = 'form-status is-error';

    } finally {

      submitBtn.classList.remove('loading');

      submitBtn.disabled = false;

    }

  });



}());

