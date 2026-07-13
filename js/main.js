(function () {
  'use strict';

  var root = document.documentElement;
  var THEME_KEY = 'dmorozov-poems-theme';

  function applyStoredTheme() {
    var stored = localStorage.getItem(THEME_KEY);
    if (stored === 'light' || stored === 'dark') {
      root.setAttribute('data-theme', stored);
    }
  }

  function currentTheme() {
    var stored = localStorage.getItem(THEME_KEY);
    if (stored) return stored;
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  function updateToggleLabel(btn) {
    var isDark = currentTheme() === 'dark';
    btn.textContent = isDark ? '☀' : '☽';
    btn.setAttribute('aria-label', isDark ? 'Включить светлую тему' : 'Включить тёмную тему');
  }

  applyStoredTheme();

  document.addEventListener('DOMContentLoaded', function () {
    var themeBtn = document.querySelector('[data-theme-toggle]');
    if (themeBtn) {
      updateToggleLabel(themeBtn);
      themeBtn.addEventListener('click', function () {
        var next = currentTheme() === 'dark' ? 'light' : 'dark';
        root.setAttribute('data-theme', next);
        localStorage.setItem(THEME_KEY, next);
        updateToggleLabel(themeBtn);
      });
    }

    var nav = document.querySelector('[data-nav]');
    var scrim = document.querySelector('[data-nav-scrim]');
    var openBtn = document.querySelector('[data-nav-open]');
    var closeBtn = document.querySelector('[data-nav-close]');

    function openNav() {
      nav.classList.add('is-open');
      scrim.classList.add('is-visible');
    }

    function closeNav() {
      nav.classList.remove('is-open');
      scrim.classList.remove('is-visible');
    }

    if (openBtn) openBtn.addEventListener('click', openNav);
    if (closeBtn) closeBtn.addEventListener('click', closeNav);
    if (scrim) scrim.addEventListener('click', closeNav);

    if (nav) {
      nav.querySelectorAll('a').forEach(function (link) {
        link.addEventListener('click', closeNav);
      });
    }

    var toTop = document.querySelector('[data-to-top]');
    if (toTop) {
      window.addEventListener('scroll', function () {
        if (window.scrollY > 600) {
          toTop.classList.add('is-visible');
        } else {
          toTop.classList.remove('is-visible');
        }
      }, { passive: true });

      toTop.addEventListener('click', function () {
        window.scrollTo({ top: 0, behavior: 'smooth' });
      });
    }
  });
})();
