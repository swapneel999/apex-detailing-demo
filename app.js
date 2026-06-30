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
     NAV SCROLL-SPY — highlight the link for the visible section
  --------------------------------------------------------------- */
  (function () {
    var navLinks = document.querySelectorAll('.nav-link[data-section]');
    var sections = Array.from(navLinks).map(function (a) {
      return document.getElementById(a.getAttribute('data-section'));
    });
    var ACTIVE  = ['active-nav-blue', 'text-a0c9ff'];
    var INACTIVE = 'text-on-surface-variant';
    function setActive(id) {
      navLinks.forEach(function (a) {
        var isActive = a.getAttribute('data-section') === id;
        ACTIVE.forEach(function (c) { a.classList.toggle(c, isActive); });
        a.classList.toggle(INACTIVE, !isActive);
      });
    }
    function onSpyScroll() {
      var scrollY = window.scrollY + 120; // offset for fixed nav height
      var active = null;
      // Sort by page position so the deepest visible section wins
      var sorted = sections.filter(Boolean).slice().sort(function (a, b) {
        return a.offsetTop - b.offsetTop;
      });
      sorted.forEach(function (sec) {
        if (sec.offsetTop <= scrollY) { active = sec.id; }
      });
      setActive(active);
    }
    window.addEventListener('scroll', onSpyScroll, { passive: true });
    onSpyScroll();
  }());
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
     GSAP PREMIUM ANIMATIONS — Stitch Tailwind DOM
  --------------------------------------------------------------- */
  if (window.gsap && window.ScrollTrigger) {
    gsap.registerPlugin(ScrollTrigger);

    // --- Hero image: cinematic bloom on load ---
    gsap.set('.hero-img', { opacity: 0, scale: 1.08 });

    // --- Hero text: hide immediately to prevent FOUC ---
    gsap.set('.hero-eyebrow, .ht-line, .hero-sub, .hero-actions, .hero-stats', { opacity: 0, y: 32 });

    // --- Hero entrance timeline ---
    var heroTl = gsap.timeline({ defaults: { ease: 'power3.out' }, delay: 0.1 });
    heroTl
      .to('.hero-img',     { opacity: 1, scale: 1, duration: 1.6, ease: 'power2.out' }, 0)
      .to('.hero-eyebrow', { opacity: 1, y: 0, duration: 0.75 }, 0.25)
      .to('.ht-line',      { opacity: 1, y: 0, duration: 1.0, stagger: 0.13 }, '-=0.45')
      .to('.hero-sub',     { opacity: 1, y: 0, duration: 0.75 }, '-=0.5')
      .to('.hero-actions', { opacity: 1, y: 0, duration: 0.65 }, '-=0.35')
      .to('.hero-stats',   { opacity: 1, y: 0, duration: 0.65 }, '-=0.25');

    // --- Hero image parallax scrub ---
    gsap.to('.hero-img', {
      scrollTrigger: {
        trigger: 'section.relative.h-screen',
        start: 'top top',
        end: 'bottom top',
        scrub: 1.8,
      },
      y: '16%',
      ease: 'none',
    });

    // --- Package cards: clip-path wipe reveal ---
    gsap.set('#packages .glass-card', { clipPath: 'inset(100% 0% 0% 0%)', opacity: 1 });
    gsap.to('#packages .glass-card', {
      scrollTrigger: { trigger: '#packages', start: 'top 72%' },
      clipPath: 'inset(0% 0% 0% 0%)',
      duration: 0.9,
      ease: 'power3.out',
      stagger: 0.15,
    });

    // --- Service cards: rotateX reveal ---
    gsap.set('#services .glass-card', { opacity: 0, rotateX: 8, transformOrigin: 'top center', y: 40 });
    gsap.to('#services .glass-card', {
      scrollTrigger: { trigger: '#services', start: 'top 75%' },
      opacity: 1,
      rotateX: 0,
      y: 0,
      duration: 0.85,
      ease: 'power3.out',
      stagger: 0.18,
    });

    // --- Section heading cascade (h2 tags in packages, services, contact) ---
    ['#packages h2', '#services h2', '#contact h2'].forEach(function (sel) {
      var el = document.querySelector(sel);
      if (!el) return;
      gsap.from(el, {
        scrollTrigger: { trigger: el, start: 'top 85%' },
        opacity: 0,
        y: 22,
        duration: 0.72,
        ease: 'power3.out',
      });
    });

    // --- Upgrade items: horizontal slide-in ---
    gsap.from('#packages ~ section .glass-card', {
      scrollTrigger: { trigger: '#packages ~ section', start: 'top 78%' },
      opacity: 0,
      x: -32,
      duration: 0.8,
      ease: 'power3.out',
      stagger: 0.2,
    });

    // --- Suburb chips: back.out cascade ---
    var chips = gsap.utils.toArray('#about span[class*="bg-surface-container"]');
    if (chips.length) {
      gsap.from(chips, {
        scrollTrigger: { trigger: '#about', start: 'top 80%' },
        opacity: 0,
        scale: 0.8,
        duration: 0.45,
        ease: 'back.out(1.7)',
        stagger: 0.055,
      });
    }
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
