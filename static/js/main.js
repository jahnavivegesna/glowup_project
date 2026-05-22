/**
 * GLOW UP - Main JavaScript
 * Handles: dark mode, navbar, cart AJAX, wishlist, animations, search overlay, toast notifications
 */

// ─── DOM Ready ─────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', function () {
  initPageLoader();
  initDarkMode();
  initNavbar();
  initSearchOverlay();
  initScrollAnimations();
  initScrollTop();
  initQuantityControls();
  initToasts();
  initProductGallery();
  initCartAjax();
  initWishlistAjax();
  initCouponAjax();
  initNewsletterForm();
  initStarRating();
});

// ─── Page Loader ────────────────────────────────────────────────────────────────
function initPageLoader() {
  const loader = document.querySelector('.page-loader');
  if (!loader) return;
  window.addEventListener('load', () => {
    setTimeout(() => loader.classList.add('loaded'), 400);
  });
}

// ─── Dark Mode ──────────────────────────────────────────────────────────────────
function initDarkMode() {
  const toggle = document.querySelector('.dark-toggle');
  const root = document.documentElement;

  // Load saved preference
  const saved = localStorage.getItem('glowup-theme') || 'light';
  root.setAttribute('data-theme', saved);
  updateToggleIcon(saved);

  if (toggle) {
    toggle.addEventListener('click', () => {
      const current = root.getAttribute('data-theme');
      const next = current === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      localStorage.setItem('glowup-theme', next);
      updateToggleIcon(next);
    });
  }
}

function updateToggleIcon(theme) {
  const thumb = document.querySelector('.dark-toggle .toggle-thumb');
  if (thumb) {
    thumb.textContent = theme === 'dark' ? '🌙' : '☀️';
  }
}

// ─── Navbar ─────────────────────────────────────────────────────────────────────
function initNavbar() {
  const navbar = document.querySelector('.navbar');
  const hamburger = document.querySelector('.hamburger');
  const menu = document.querySelector('.navbar-menu');

  // Sticky scroll effect
  window.addEventListener('scroll', () => {
    if (navbar) {
      navbar.classList.toggle('scrolled', window.scrollY > 20);
    }
  });

  // Mobile menu toggle
  if (hamburger && menu) {
    hamburger.addEventListener('click', () => {
      const isOpen = menu.classList.toggle('open');
      hamburger.setAttribute('aria-expanded', isOpen);
      document.body.style.overflow = isOpen ? 'hidden' : '';
    });

    // Close on outside click
    document.addEventListener('click', (e) => {
      if (!hamburger.contains(e.target) && !menu.contains(e.target)) {
        menu.classList.remove('open');
        document.body.style.overflow = '';
      }
    });
  }

  // Mark active nav link
  const currentPath = window.location.pathname;
  document.querySelectorAll('.nav-link').forEach(link => {
    if (link.getAttribute('href') === currentPath) {
      link.classList.add('active');
    }
  });
}

// ─── Search Overlay ─────────────────────────────────────────────────────────────
function initSearchOverlay() {
  const searchBtn = document.querySelector('.search-trigger');
  const overlay = document.querySelector('.search-overlay');
  const closeBtn = document.querySelector('.search-close');
  const input = document.querySelector('.search-input');

  if (!searchBtn || !overlay) return;

  searchBtn.addEventListener('click', () => {
    overlay.classList.add('active');
    setTimeout(() => input && input.focus(), 100);
    document.body.style.overflow = 'hidden';
  });

  function closeSearch() {
    overlay.classList.remove('active');
    document.body.style.overflow = '';
  }

  if (closeBtn) closeBtn.addEventListener('click', closeSearch);

  overlay.addEventListener('click', (e) => {
    if (e.target === overlay) closeSearch();
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeSearch();
    if (e.key === '/' && !overlay.classList.contains('active')) {
      e.preventDefault();
      overlay.classList.add('active');
      setTimeout(() => input && input.focus(), 100);
    }
  });
}

// ─── Scroll Animations (Intersection Observer) ──────────────────────────────────
function initScrollAnimations() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target); // Animate once
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.fade-up').forEach(el => observer.observe(el));
}

// ─── Scroll to Top ──────────────────────────────────────────────────────────────
function initScrollTop() {
  const btn = document.querySelector('.scroll-top');
  if (!btn) return;

  window.addEventListener('scroll', () => {
    btn.classList.toggle('visible', window.scrollY > 400);
  });

  btn.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
}

// ─── Quantity Controls ──────────────────────────────────────────────────────────
function initQuantityControls() {
  document.querySelectorAll('.qty-control').forEach(control => {
    const minusBtn = control.querySelector('.qty-minus');
    const plusBtn = control.querySelector('.qty-plus');
    const valueEl = control.querySelector('.qty-value');
    const max = parseInt(control.dataset.max || 99);
    const min = parseInt(control.dataset.min || 1);

    if (!minusBtn || !plusBtn || !valueEl) return;

    minusBtn.addEventListener('click', () => {
      let val = parseInt(valueEl.value || valueEl.textContent);
      if (val > min) {
        val--;
        valueEl.value = val;
        valueEl.textContent = val;
        triggerQuantityChange(control, val);
      }
    });

    plusBtn.addEventListener('click', () => {
      let val = parseInt(valueEl.value || valueEl.textContent);
      if (val < max) {
        val++;
        valueEl.value = val;
        valueEl.textContent = val;
        triggerQuantityChange(control, val);
      }
    });

    if (valueEl.tagName === 'INPUT') {
      valueEl.addEventListener('change', () => {
        let val = parseInt(valueEl.value);
        if (isNaN(val) || val < min) val = min;
        if (val > max) val = max;
        valueEl.value = val;
        triggerQuantityChange(control, val);
      });
    }
  });
}

function triggerQuantityChange(control, quantity) {
  const updateUrl = control.dataset.updateUrl;
  const itemId = control.dataset.itemId;
  if (!updateUrl) return;

  const csrfToken = getCsrfToken();

  fetch(updateUrl, {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrfToken,
      'X-Requested-With': 'XMLHttpRequest',
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: `quantity=${quantity}`
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      // Update item total
      const itemTotal = document.querySelector(`[data-item-total="${itemId}"]`);
      if (itemTotal) itemTotal.textContent = `₹${data.item_total.toFixed(2)}`;

      // Update cart subtotal
      const cartSubtotal = document.querySelector('.cart-subtotal');
      if (cartSubtotal) cartSubtotal.textContent = `₹${data.cart_subtotal.toFixed(2)}`;

      // Update cart count badge
      updateCartBadge(data.cart_count);
    }
  })
  .catch(err => console.error('Cart update error:', err));
}

// ─── Toast Notifications ────────────────────────────────────────────────────────
function initToasts() {
  // Auto-dismiss Django messages
  const alerts = document.querySelectorAll('.django-message');
  alerts.forEach(alert => {
    setTimeout(() => {
      alert.style.opacity = '0';
      alert.style.transform = 'translateY(-10px)';
      setTimeout(() => alert.remove(), 300);
    }, 4000);
  });
}

function showToast(message, type = 'success') {
  const container = document.querySelector('.toast-container') || createToastContainer();
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.innerHTML = `
    <span>${type === 'success' ? '✓' : '✕'}</span>
    <span>${message}</span>
  `;
  container.appendChild(toast);
  setTimeout(() => toast.remove(), 3000);
}

function createToastContainer() {
  const div = document.createElement('div');
  div.className = 'toast-container';
  document.body.appendChild(div);
  return div;
}

// ─── Product Gallery ────────────────────────────────────────────────────────────
function initProductGallery() {
  const mainImg = document.querySelector('.gallery-main img');
  const thumbs = document.querySelectorAll('.gallery-thumb');

  if (!mainImg || !thumbs.length) return;

  thumbs.forEach((thumb, index) => {
    thumb.addEventListener('click', () => {
      const src = thumb.querySelector('img')?.src;
      if (src) {
        mainImg.src = src;
        mainImg.style.opacity = '0';
        mainImg.style.transform = 'scale(0.95)';
        setTimeout(() => {
          mainImg.style.opacity = '1';
          mainImg.style.transform = 'scale(1)';
        }, 50);
        document.querySelector('.gallery-thumb.active')?.classList.remove('active');
        thumb.classList.add('active');
      }
    });
  });

  // Set first thumb active
  thumbs[0]?.classList.add('active');

  // Transition for image
  mainImg.style.transition = 'opacity 0.3s, transform 0.3s';
}

// ─── Cart AJAX ──────────────────────────────────────────────────────────────────
function initCartAjax() {
  document.querySelectorAll('.add-to-cart-btn').forEach(btn => {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      const url = this.dataset.url;
      const productName = this.dataset.name || 'Product';

      if (!url) return;

      // Show loading
      const originalHTML = this.innerHTML;
      this.innerHTML = '<span class="loading-spinner"></span>';
      this.disabled = true;

      fetch(url, {
        method: 'GET',
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
        }
      })
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          showToast(`${productName} added to cart! 🛒`, 'success');
          updateCartBadge(data.cart_count);
        } else {
          showToast(data.message || 'Could not add to cart', 'error');
        }
      })
      .catch(() => {
        // Fallback: redirect to add URL
        window.location.href = url;
      })
      .finally(() => {
        this.innerHTML = originalHTML;
        this.disabled = false;
      });
    });
  });
}

function updateCartBadge(count) {
  document.querySelectorAll('.cart-badge').forEach(badge => {
    badge.textContent = count;
    badge.style.display = count > 0 ? 'flex' : 'none';
    // Pulse animation
    badge.classList.remove('pulse');
    void badge.offsetWidth; // Reflow
    badge.classList.add('pulse');
  });
}

// ─── Wishlist AJAX ──────────────────────────────────────────────────────────────
function initWishlistAjax() {
  document.querySelectorAll('.wishlist-btn').forEach(btn => {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      const url = this.dataset.url;
      if (!url) return;

      const csrfToken = getCsrfToken();

      fetch(url, {
        method: 'GET',
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
      })
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          const isAdded = data.action === 'added';
          this.classList.toggle('wishlisted', isAdded);
          this.querySelector('i')?.classList.toggle('fas', isAdded);
          this.querySelector('i')?.classList.toggle('far', !isAdded);
          showToast(
            isAdded ? '💖 Added to wishlist!' : 'Removed from wishlist',
            isAdded ? 'success' : 'success'
          );
          // Update wishlist badge
          document.querySelectorAll('.wishlist-badge').forEach(badge => {
            badge.textContent = data.wishlist_count;
          });
        }
      })
      .catch(() => { window.location.href = url; });
    });
  });
}

// ─── Coupon AJAX ────────────────────────────────────────────────────────────────
function initCouponAjax() {
  const couponForm = document.getElementById('coupon-form');
  if (!couponForm) return;

  couponForm.addEventListener('submit', function (e) {
    e.preventDefault();
    const code = document.getElementById('coupon-input')?.value;
    const csrfToken = getCsrfToken();

    fetch('/apply-coupon/', {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrfToken,
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Requested-With': 'XMLHttpRequest',
      },
      body: `code=${encodeURIComponent(code)}`
    })
    .then(res => res.json())
    .then(data => {
      const msgEl = document.getElementById('coupon-message');
      if (msgEl) {
        msgEl.textContent = data.message;
        msgEl.className = `mt-2 text-sm ${data.success ? 'text-green' : 'text-danger'}`;
      }
      if (data.success) {
        // Update discount display
        const discountEl = document.getElementById('discount-amount');
        if (discountEl) discountEl.textContent = `-₹${data.discount.toFixed(2)}`;

        const totalEl = document.getElementById('order-total');
        if (totalEl) {
          const subtotal = parseFloat(totalEl.dataset.subtotal || 0);
          const shipping = parseFloat(totalEl.dataset.shipping || 0);
          totalEl.textContent = `₹${(subtotal + shipping - data.discount).toFixed(2)}`;
        }

        // Store coupon in hidden input
        const hiddenInput = document.createElement('input');
        hiddenInput.type = 'hidden';
        hiddenInput.name = 'coupon_code';
        hiddenInput.value = code;
        couponForm.appendChild(hiddenInput);

        showToast(data.message, 'success');
      }
    });
  });
}

// ─── Newsletter Form ────────────────────────────────────────────────────────────
function initNewsletterForm() {
  const form = document.querySelector('.newsletter-form-ajax');
  if (!form) return;

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    const email = form.querySelector('input[type="email"]')?.value;
    const btn = form.querySelector('button');
    const originalText = btn?.textContent;

    if (btn) btn.textContent = 'Subscribing...';

    fetch('/newsletter/subscribe/', {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCsrfToken(),
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: `email=${encodeURIComponent(email)}`
    })
    .then(() => {
      showToast('🌿 Thanks for subscribing!', 'success');
      form.reset();
    })
    .finally(() => {
      if (btn) btn.textContent = originalText;
    });
  });
}

// ─── Star Rating ────────────────────────────────────────────────────────────────
function initStarRating() {
  const ratingInputs = document.querySelectorAll('.star-rating-input input[type="radio"]');
  ratingInputs.forEach(input => {
    input.addEventListener('change', function () {
      const val = parseInt(this.value);
      ratingInputs.forEach((inp, i) => {
        const label = document.querySelector(`label[for="${inp.id}"]`);
        if (label) {
          label.style.color = i <= val - 1 ? 'var(--gold)' : 'var(--border)';
        }
      });
    });
  });
}

// ─── Utility: Get CSRF Token ────────────────────────────────────────────────────
function getCsrfToken() {
  return document.querySelector('[name=csrfmiddlewaretoken]')?.value ||
    document.cookie.split(';').find(c => c.trim().startsWith('csrftoken='))?.split('=')[1] || '';
}

// ─── Price Range Filter ─────────────────────────────────────────────────────────
const priceRange = document.querySelector('.price-range');
const priceDisplay = document.querySelector('.price-display');
if (priceRange && priceDisplay) {
  priceRange.addEventListener('input', function () {
    priceDisplay.textContent = `₹0 - ₹${this.value}`;
  });
}

// ─── Product Image Zoom ─────────────────────────────────────────────────────────
const galleryMain = document.querySelector('.gallery-main');
if (galleryMain) {
  galleryMain.addEventListener('mousemove', function (e) {
    const img = this.querySelector('img');
    if (!img) return;
    const { left, top, width, height } = this.getBoundingClientRect();
    const x = ((e.clientX - left) / width) * 100;
    const y = ((e.clientY - top) / height) * 100;
    img.style.transformOrigin = `${x}% ${y}%`;
    img.style.transform = 'scale(1.5)';
  });

  galleryMain.addEventListener('mouseleave', function () {
    const img = this.querySelector('img');
    if (img) {
      img.style.transform = 'scale(1)';
      img.style.transformOrigin = 'center center';
    }
  });
}

// ─── Trending Products Carousel (Auto Scroll) ────────────────────────────────────
const carousel = document.querySelector('.trending-carousel');
if (carousel) {
  let isPaused = false;
  let scrollSpeed = 1;

  function autoScroll() {
    if (!isPaused && carousel.scrollLeft < carousel.scrollWidth - carousel.clientWidth) {
      carousel.scrollLeft += scrollSpeed;
    } else if (!isPaused) {
      carousel.scrollLeft = 0;
    }
    requestAnimationFrame(autoScroll);
  }

  carousel.addEventListener('mouseenter', () => isPaused = true);
  carousel.addEventListener('mouseleave', () => isPaused = false);
  requestAnimationFrame(autoScroll);
}

// ─── Filter Form Auto-Submit ────────────────────────────────────────────────────
document.querySelectorAll('.filter-auto-submit').forEach(input => {
  input.addEventListener('change', () => {
    const form = input.closest('form');
    if (form) form.submit();
  });
});

// ─── Badge Pulse Animation ──────────────────────────────────────────────────────
const style = document.createElement('style');
style.textContent = `
  @keyframes badge-pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.4); }
    100% { transform: scale(1); }
  }
  .badge-count.pulse { animation: badge-pulse 0.3s ease; }
`;
document.head.appendChild(style);
