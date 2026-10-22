/* Accessibility additions scoped to the redesigned homepage. */
document.addEventListener('DOMContentLoaded', () => {
  const modal = document.querySelector('[data-brief-modal]');
  const menu = document.querySelector('[data-mobile-menu]');
  const toggle = document.querySelector('[data-nav-toggle]');
  const mega = document.querySelector('[data-mega-menu]');
  const megaToggle = document.querySelector('[data-mega-toggle]');
  let returnFocus = null;
  const syncMenu = () => {
    const open = menu.classList.contains('is-open');
    menu.setAttribute('aria-hidden', String(!open));
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  };
  document.querySelectorAll('[data-open-brief]').forEach(el => el.addEventListener('click', () => {
    returnFocus = menu.contains(el) ? toggle : el;
    menu.classList.remove('is-open');
    syncMenu();
    document.querySelector('#name').focus();
  }));
  new MutationObserver(() => {
    if (!modal.classList.contains('is-open') && returnFocus) {
      returnFocus.focus();
      returnFocus = null;
    }
  }).observe(modal, {attributes:true, attributeFilter:['class']});
  new MutationObserver(syncMenu).observe(menu, {attributes:true, attributeFilter:['class']});
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') {
      if (modal.classList.contains('is-open')) modal.querySelector('[data-close-brief]').click();
      if (menu.classList.contains('is-open')) {toggle.click(); toggle.focus();}
      if (mega.classList.contains('is-open')) {megaToggle.click(); megaToggle.focus();}
    }
    const active = modal.classList.contains('is-open') ? modal : menu.classList.contains('is-open') ? menu : null;
    if (e.key === 'Tab' && active) {
      const nodes = [...active.querySelectorAll('a[href],button,input,textarea,select')].filter(el => !el.disabled && el.getClientRects().length);
      if (active === menu) nodes.unshift(toggle);
      const first = nodes[0], last = nodes[nodes.length - 1];
      if (e.shiftKey && document.activeElement === first) {e.preventDefault(); last.focus();}
      else if (!e.shiftKey && document.activeElement === last) {e.preventDefault(); first.focus();}
    }
  });
  // Intercept only reduced-motion anchors, ahead of the shared smooth-scroll listener.
  document.addEventListener('click', e => {
    const a = e.target.closest('a[href^="#"]');
    if (!a || a.hasAttribute('data-open-brief') || !matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    const href = a.getAttribute('href');
    if (href.length < 2) return;
    const target = document.getElementById(href.slice(1));
    if (!target) return;
    e.preventDefault(); e.stopImmediatePropagation();
    menu.classList.remove('is-open'); syncMenu(); document.body.style.overflow = '';
    window.scrollTo({top:target.getBoundingClientRect().top + scrollY - document.querySelector('[data-header]').offsetHeight - 20,behavior:'instant'});
  }, true);
  matchMedia('(min-width:961px)').addEventListener('change', e => {
    if (e.matches && menu.classList.contains('is-open')) {menu.classList.remove('is-open'); syncMenu(); document.body.style.overflow='';}
  });

  // Dark Portfolio Pro showcase filter logic
  const filterBtns = document.querySelectorAll('[data-dp-filter]');
  const portfolioItems = document.querySelectorAll('.dp-portfolio-item');
  if (filterBtns.length && portfolioItems.length) {
    filterBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        filterBtns.forEach(b => b.classList.remove('is-active'));
        btn.classList.add('is-active');
        const filter = btn.getAttribute('data-dp-filter');
        portfolioItems.forEach(item => {
          if (filter === '*' || item.getAttribute('data-category') === filter) {
            item.classList.remove('is-hidden');
          } else {
            item.classList.add('is-hidden');
          }
        });
      });
    });
  }
});
