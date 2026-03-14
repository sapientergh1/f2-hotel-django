/* =====================================================
   F2 HOTEL — Main JavaScript
   ===================================================== */

document.addEventListener('DOMContentLoaded', function () {

  // ── Navbar scroll effect ──────────────────────────
  const nav = document.getElementById('mainNav');
  if (nav) {
    window.addEventListener('scroll', () => {
      nav.classList.toggle('scrolled', window.scrollY > 50);
    });
  }

  // ── Set min dates for booking inputs ──────────────
  const today = new Date().toISOString().split('T')[0];
  document.querySelectorAll('input[type="date"]').forEach(input => {
    if (!input.min) input.min = today;
  });

  // ── Check-in / check-out date sync ────────────────
  const checkIn  = document.getElementById('id_check_in')  || document.querySelector('[name="check_in"]');
  const checkOut = document.getElementById('id_check_out') || document.querySelector('[name="check_out"]');

  if (checkIn && checkOut) {
    checkIn.addEventListener('change', function () {
      const nextDay = new Date(this.value);
      nextDay.setDate(nextDay.getDate() + 1);
      checkOut.min = nextDay.toISOString().split('T')[0];
      if (checkOut.value && checkOut.value <= this.value) {
        checkOut.value = nextDay.toISOString().split('T')[0];
      }
      updatePricePreview();
    });
    checkOut.addEventListener('change', updatePricePreview);
  }

  function updatePricePreview() {
    const priceEl    = document.getElementById('price-preview');
    const nightsEl   = document.getElementById('nights-count');
    const pricePerNight = parseFloat(document.getElementById('price-per-night')?.value || 0);

    if (!priceEl || !checkIn?.value || !checkOut?.value) return;

    const nights = Math.round(
      (new Date(checkOut.value) - new Date(checkIn.value)) / (1000 * 60 * 60 * 24)
    );
    if (nights > 0) {
      if (nightsEl) nightsEl.textContent = nights;
      priceEl.textContent = 'GHS ' + (nights * pricePerNight).toLocaleString('en-GH', {minimumFractionDigits: 2});
    }
  }

  // ── Scroll reveal (fade-up) ────────────────────────
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.fade-up').forEach(el => observer.observe(el));

  // ── Gallery filter ────────────────────────────────
  document.querySelectorAll('[data-filter]').forEach(btn => {
    btn.addEventListener('click', function () {
      document.querySelectorAll('[data-filter]').forEach(b => b.classList.remove('active'));
      this.classList.add('active');
      const filter = this.dataset.filter;
      document.querySelectorAll('.gallery-item-wrap').forEach(item => {
        if (filter === 'all' || item.dataset.category === filter) {
          item.style.display = '';
        } else {
          item.style.display = 'none';
        }
      });
    });
  });

  // ── Auto-dismiss alerts ───────────────────────────
  setTimeout(() => {
    document.querySelectorAll('.alert.alert-success').forEach(el => {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(el);
      bsAlert?.close();
    });
  }, 5000);

  // ── Booking search form hero ───────────────────────
  const searchForm = document.getElementById('heroSearchForm');
  if (searchForm) {
    searchForm.addEventListener('submit', function (e) {
      const ci = this.querySelector('[name="check_in"]')?.value;
      const co = this.querySelector('[name="check_out"]')?.value;
      if (ci && co && new Date(co) <= new Date(ci)) {
        e.preventDefault();
        alert('Check-out date must be after check-in date.');
      }
    });
  }

  // ── Counter animation for hero stats ─────────────
  function animateCounter(el) {
    const target = parseInt(el.dataset.target || el.textContent);
    const suffix = el.dataset.suffix || '';
    let current = 0;
    const increment = target / 60;
    const timer = setInterval(() => {
      current += increment;
      if (current >= target) {
        current = target;
        clearInterval(timer);
      }
      el.textContent = Math.floor(current) + suffix;
    }, 20);
  }

  const counters = document.querySelectorAll('[data-counter]');
  if (counters.length) {
    const counterObserver = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          animateCounter(entry.target);
          counterObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.5 });
    counters.forEach(c => counterObserver.observe(c));
  }

  // ── Smooth scroll for anchor links ────────────────
  document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener('click', function (e) {
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

});
