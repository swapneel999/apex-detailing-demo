/* ================================================================
   RGDETAILING — app.js
   GSAP 3.12+ motion layer + form handling
   ================================================================ */

(function () {
  'use strict';

  /* ---------------------------------------------------------------
     GSAP REGISTRATION
  --------------------------------------------------------------- */
  gsap.registerPlugin(ScrollTrigger);

  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------------------------------------------------------------
     SCROLL-TRIGGER REVEALS
  --------------------------------------------------------------- */
  function initScrollAnimations() {

    // Section headers
    gsap.utils.toArray('.section-header').forEach(function (el) {
      gsap.from(el.querySelectorAll('.section-label, .section-title, .section-sub'), {
        autoAlpha: 0,
        y: 32,
        duration: 0.7,
        ease: 'power4.out',
        stagger: 0.1,
        scrollTrigger: {
          trigger: el,
          start: 'top 82%',
          once: true
        }
      });
    });

    // Package cards — staggered entrance
    gsap.from('.package-card', {
      autoAlpha: 0,
      y: 48,
      duration: 0.75,
      ease: 'power4.out',
      stagger: 0.12,
      scrollTrigger: {
        trigger: '.bento-grid',
        start: 'top 80%',
        once: true
      }
    });

    // Process steps
    gsap.from('.process-step', {
      autoAlpha: 0,
      y: 40,
      duration: 0.7,
      ease: 'power4.out',
      stagger: 0.15,
      scrollTrigger: {
        trigger: '.process-grid',
        start: 'top 78%',
        once: true
      }
    });

    // Quote layout
    gsap.from('.quote-info', {
      autoAlpha: 0,
      x: -32,
      duration: 0.75,
      ease: 'power4.out',
      scrollTrigger: {
        trigger: '.quote-layout',
        start: 'top 80%',
        once: true
      }
    });

    gsap.from('.quote-form-wrap', {
      autoAlpha: 0,
      x: 32,
      duration: 0.75,
      ease: 'power4.out',
      scrollTrigger: {
        trigger: '.quote-layout',
        start: 'top 80%',
        once: true
      }
    });

    // Footer
    gsap.from('.footer-inner > *', {
      autoAlpha: 0,
      y: 20,
      duration: 0.6,
      ease: 'power4.out',
      stagger: 0.1,
      scrollTrigger: {
        trigger: '#footer',
        start: 'top 90%',
        once: true
      }
    });
  }

  /* ---------------------------------------------------------------
     NAVIGATION — scroll state + mobile menu
  --------------------------------------------------------------- */
  const nav = document.getElementById('nav');

  function handleNavScroll() {
    if (window.scrollY > 40) {
      nav.classList.add('scrolled');
    } else {
      nav.classList.remove('scrolled');
    }
  }

  window.addEventListener('scroll', handleNavScroll, { passive: true });
  handleNavScroll();

  // Mobile burger
  const burger    = document.getElementById('nav-burger');
  const mobileNav = document.getElementById('nav-mobile');

  if (burger && mobileNav) {
    burger.addEventListener('click', function () {
      const isOpen = burger.classList.toggle('open');
      mobileNav.classList.toggle('open', isOpen);
      burger.setAttribute('aria-expanded', String(isOpen));
      mobileNav.setAttribute('aria-hidden', String(!isOpen));
    });

    // Close on link click
    mobileNav.querySelectorAll('.nav-mobile-link').forEach(function (link) {
      link.addEventListener('click', function () {
        burger.classList.remove('open');
        mobileNav.classList.remove('open');
        burger.setAttribute('aria-expanded', 'false');
        mobileNav.setAttribute('aria-hidden', 'true');
      });
    });
  }

  /* ---------------------------------------------------------------
     CSRF TOKEN (fetched from backend)
  --------------------------------------------------------------- */
  function fetchCsrfToken() {
    const tokenInput = document.getElementById('csrf-token');
    if (!tokenInput) return;

    fetch('/api/csrf-token', { credentials: 'same-origin' })
      .then(function (res) {
        if (!res.ok) return;
        return res.json();
      })
      .then(function (data) {
        if (data && data.token) {
          tokenInput.value = data.token;
        }
      })
      .catch(function () {
        // Backend unavailable in static preview — token remains empty
      });
  }

  fetchCsrfToken();

  /* ---------------------------------------------------------------
     FORM VALIDATION & SUBMISSION
  --------------------------------------------------------------- */
  const form         = document.getElementById('quote-form');
  const submitBtn    = document.getElementById('form-submit');
  const successPanel = document.getElementById('form-success');
  const errorBanner  = document.getElementById('form-error');

  const VALID_PACKAGES = new Set(['CERAMIC_LITE', 'CERAMIC_PRO', 'APEX_CERAMIC']);

  // Field-level validators — mirror backend rules
  const validators = {
    name: function (v) {
      if (!v || v.trim().length < 2) return 'Name must be at least 2 characters.';
      if (v.trim().length > 100)     return 'Name must not exceed 100 characters.';
      return '';
    },
    email: function (v) {
      if (!v || !v.trim()) return 'Email address is required.';
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.trim())) return 'Please enter a valid email address.';
      return '';
    },
    phone: function (v) {
      if (!v || !v.trim()) return 'Phone number is required.';
      var cleaned = v.replace(/[\s\-()]/g, '');
      if (!/^(\+61|0)[2-9]\d{8}$/.test(cleaned)) return 'Please enter a valid Australian phone number.';
      return '';
    },
    vehicle: function (v) {
      if (!v || v.trim().length < 2) return 'Vehicle details must be at least 2 characters.';
      if (v.trim().length > 100)     return 'Vehicle details must not exceed 100 characters.';
      return '';
    },
    package: function (v) {
      if (!v) return 'Please select a package.';
      if (!VALID_PACKAGES.has(v)) return 'Please select a valid package.';
      return '';
    },
    message: function (v) {
      if (v && v.length > 500) return 'Message must not exceed 500 characters.';
      return '';
    }
  };

  function showFieldError(fieldId, message) {
    var input = document.getElementById(fieldId);
    var errorEl = document.getElementById(fieldId + '-error');
    if (!input || !errorEl) return;

    errorEl.textContent = message;
    if (message) {
      input.setAttribute('aria-invalid', 'true');
      input.setAttribute('aria-describedby', fieldId + '-error');
    } else {
      input.removeAttribute('aria-invalid');
    }
  }

  function clearFieldError(fieldId) {
    showFieldError(fieldId, '');
  }

  // Validate on blur for each field
  var fields = ['f-name', 'f-email', 'f-phone', 'f-vehicle', 'f-package'];
  fields.forEach(function (fid) {
    var el = document.getElementById(fid);
    if (!el) return;
    var key = fid.replace('f-', '');
    el.addEventListener('blur', function () {
      var err = validators[key] ? validators[key](el.value) : '';
      showFieldError(fid, err);
    });
  });

  // Character counter for textarea
  var messageInput = document.getElementById('f-message');
  var charCount    = document.getElementById('f-message-count');

  if (messageInput && charCount) {
    messageInput.addEventListener('input', function () {
      var len = messageInput.value.length;
      charCount.textContent = len + ' / 500';
      charCount.classList.toggle('near-limit', len > 450);
      if (len > 500) {
        showFieldError('f-message', 'Message must not exceed 500 characters.');
      } else {
        clearFieldError('f-message');
      }
    });
  }

  function validateAll() {
    var allValid = true;
    var firstInvalidId = null;

    var fieldMap = {
      'f-name':    'name',
      'f-email':   'email',
      'f-phone':   'phone',
      'f-vehicle': 'vehicle',
      'f-package': 'package',
      'f-message': 'message'
    };

    Object.entries(fieldMap).forEach(function (entry) {
      var fid = entry[0];
      var key = entry[1];
      var el  = document.getElementById(fid);
      if (!el || !validators[key]) return;

      var err = validators[key](el.value);
      showFieldError(fid, err);
      if (err) {
        allValid = false;
        if (!firstInvalidId) firstInvalidId = fid;
      }
    });

    if (firstInvalidId) {
      document.getElementById(firstInvalidId).focus();
    }

    return allValid;
  }

  function setSubmitLoading(loading) {
    var textEl    = submitBtn.querySelector('.submit-text');
    var loadingEl = submitBtn.querySelector('.submit-loading');
    submitBtn.disabled = loading;
    if (textEl)    textEl.hidden = loading;
    if (loadingEl) loadingEl.hidden = !loading;
  }

  function showBanner(el, message) {
    el.textContent = message;
    el.hidden = false;
    el.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();

      // Hide any previous banners
      successPanel.hidden = true;
      errorBanner.hidden  = true;

      if (!validateAll()) return;

      setSubmitLoading(true);

      var payload = {
        name:       document.getElementById('f-name').value.trim(),
        email:      document.getElementById('f-email').value.trim().toLowerCase(),
        phone:      document.getElementById('f-phone').value.trim(),
        vehicle:    document.getElementById('f-vehicle').value.trim(),
        package:    document.getElementById('f-package').value.trim().toUpperCase(),
        message:    (messageInput ? messageInput.value.trim() : ''),
        csrf_token: document.getElementById('csrf-token').value
      };

      fetch('/api/quote', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'same-origin',
        body: JSON.stringify(payload)
      })
        .then(function (res) {
          return res.json().then(function (data) {
            return { ok: res.ok, status: res.status, data: data };
          });
        })
        .then(function (result) {
          setSubmitLoading(false);

          if (result.ok) {
            form.reset();
            if (charCount) charCount.textContent = '0 / 500';
            successPanel.hidden = false;
            successPanel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            fetchCsrfToken();
          } else if (result.status === 429) {
            showBanner(errorBanner, 'Too many requests. Please wait a moment before submitting again.');
          } else {
            var msg = (result.data && result.data.error) || 'An error occurred. Please try again.';
            showBanner(errorBanner, msg);
          }
        })
        .catch(function () {
          setSubmitLoading(false);
          showBanner(errorBanner, 'Unable to connect. Please check your connection and try again.');
        });
    });
  }

  /* ---------------------------------------------------------------
     BOOT — scroll animations only; preloader/hero handled by inline script
  --------------------------------------------------------------- */
  document.addEventListener('DOMContentLoaded', function () {
    if (!prefersReducedMotion) {
      initScrollAnimations();
    }
  });

})();
