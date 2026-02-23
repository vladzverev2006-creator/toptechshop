// Theme toggle
const themeToggle = document.querySelector('[data-theme-toggle]');
const savedTheme = localStorage.getItem('theme') || 'light';
document.documentElement.dataset.theme = savedTheme;
if (themeToggle) {
  themeToggle.addEventListener('click', () => {
    const current = document.documentElement.dataset.theme || 'light';
    const next = current === 'light' ? 'dark' : 'light';
    document.documentElement.dataset.theme = next;
    localStorage.setItem('theme', next);
  });
}

// Scroll to top
const toTop = document.querySelector('[data-scroll-top]');
if (toTop) {
  toTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
}

// Live search filter
const liveSearch = document.querySelector('[data-live-search]');
if (liveSearch) {
  liveSearch.addEventListener('input', (e) => {
    const term = e.target.value.toLowerCase();
    document.querySelectorAll('[data-search-item]').forEach((el) => {
      el.style.display = el.textContent.toLowerCase().includes(term) ? '' : 'none';
    });
  });
}

// Modal
const modal = document.querySelector('[data-modal]');
const modalOpen = document.querySelectorAll('[data-modal-open]');
const modalClose = document.querySelectorAll('[data-modal-close]');
modalOpen.forEach((btn) => btn.addEventListener('click', () => {
  if (modal) modal.classList.add('is-open');
}));
modalClose.forEach((btn) => btn.addEventListener('click', () => {
  if (modal) modal.classList.remove('is-open');
}));

// FAQ accordion
document.querySelectorAll('[data-accordion] button').forEach((btn) => {
  btn.addEventListener('click', () => {
    const item = btn.closest('[data-accordion-item]');
    if (item) item.classList.toggle('is-open');
  });
});

// Rating selector
document.querySelectorAll('[data-rating] input').forEach((input) => {
  input.addEventListener('change', () => {
    const ratingValue = document.querySelector('[data-rating-value]');
    if (ratingValue) ratingValue.textContent = input.value;
  });
});

// File preview
const fileInput = document.querySelector('[data-file-input]');
if (fileInput) {
  fileInput.addEventListener('change', (e) => {
    const file = e.target && e.target.files ? e.target.files[0] : null;
    const fileName = file ? file.name : '';
    const fileNameTarget = document.querySelector('[data-file-name]');
    if (fileNameTarget) fileNameTarget.textContent = fileName;
  });
}

// Password toggle
document.querySelectorAll('[data-password-toggle]').forEach((btn) => {
  btn.addEventListener('click', () => {
    const target = document.querySelector(btn.dataset.passwordToggle);
    if (target) target.type = target.type === 'password' ? 'text' : 'password';
  });
});

// Quantity control
document.querySelectorAll('[data-qty-btn]').forEach((btn) => {
  btn.addEventListener('click', () => {
    const input = document.querySelector(btn.dataset.target);
    if (!input) return;
    const delta = parseInt(btn.dataset.delta, 10);
    input.value = Math.max(1, parseInt(input.value || '1', 10) + delta);
  });
});

// Copy to clipboard (delegated)
document.addEventListener('click', async (e) => {
  const btn = e.target.closest('[data-copy]');
  if (!btn) return;
  e.preventDefault();
  const text = btn.dataset.copy || '';
  if (!text) return;
  try {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(text);
    } else {
      const temp = document.createElement('textarea');
      temp.value = text;
      temp.setAttribute('readonly', '');
      temp.style.position = 'absolute';
      temp.style.left = '-9999px';
      document.body.appendChild(temp);
      temp.select();
      document.execCommand('copy');
      document.body.removeChild(temp);
    }
    btn.textContent = 'Скопировано';
  } catch (err) {
    btn.textContent = 'Не удалось';
  }
});

// Tabs
document.querySelectorAll('[data-tab] button').forEach((btn) => {
  btn.addEventListener('click', () => {
    const target = btn.dataset.tabTarget;
    document.querySelectorAll('[data-tab-content]').forEach((el) => (el.style.display = 'none'));
    document.querySelector(target).style.display = 'block';
  });
});

function showToast(message) {
  const toast = document.querySelector('[data-toast-box]');
  if (!toast) return;
  if (message) toast.textContent = message;
  toast.classList.add('is-show');
  if (toast._toastTimer) clearTimeout(toast._toastTimer);
  toast._toastTimer = setTimeout(() => toast.classList.remove('is-show'), 2000);
}

// Toast
const toastTrigger = document.querySelector('[data-toast]');
if (toastTrigger) {
  toastTrigger.addEventListener('click', () => {
    showToast('Готово');
  });
}

// No-rights popup
document.addEventListener('click', (e) => {
  const blocked = e.target.closest('[data-no-rights]');
  if (!blocked) return;
  e.preventDefault();
  showToast('Недостаточно прав');
});

// Favorite toggle
document.querySelectorAll('[data-favorite]').forEach((btn) => {
  btn.addEventListener('click', () => {
    btn.classList.toggle('is-active');
  });
});

// Dropdown toggle
document.querySelectorAll('[data-dropdown-toggle]').forEach((btn) => {
  btn.addEventListener('click', () => {
    const menu = document.querySelector(btn.dataset.dropdownToggle);
    if (menu) menu.classList.toggle('is-open');
  });
});

// Preloader
window.addEventListener('load', () => {
  const preloader = document.querySelector('[data-preloader]');
  if (preloader) preloader.classList.add('is-hidden');
});

// Simple form validation
document.querySelectorAll('[data-validate]').forEach((form) => {
  form.addEventListener('submit', (e) => {
    const required = form.querySelectorAll('[data-required]');
    let valid = true;
    required.forEach((field) => {
      if (!field.value.trim()) {
        field.classList.add('is-invalid');
        valid = false;
      }
    });
    if (!valid) e.preventDefault();
  });
});
