/* North Shore Garage Doors — interactions */
(function () {
  "use strict";

  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  /* ---- Header shadow on scroll ---- */
  var header = $("#header");
  var toTop = $("#toTop");
  function onScroll() {
    var y = window.pageYOffset;
    if (header) header.classList.toggle("scrolled", y > 8);
    if (toTop) toTop.classList.toggle("show", y > 600);
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ---- Mobile nav drawer ---- */
  var navToggle = $("#navToggle");
  var mobileNav = $("#mobileNav");
  var overlay = $("#overlay");
  var mnClose = $("#mnClose");

  function openNav() {
    mobileNav.classList.add("open");
    overlay.classList.add("open");
    navToggle.classList.add("open");
    navToggle.setAttribute("aria-expanded", "true");
    document.body.style.overflow = "hidden";
  }
  function closeNav() {
    mobileNav.classList.remove("open");
    overlay.classList.remove("open");
    navToggle.classList.remove("open");
    navToggle.setAttribute("aria-expanded", "false");
    document.body.style.overflow = "";
  }
  if (navToggle) navToggle.addEventListener("click", openNav);
  if (mnClose) mnClose.addEventListener("click", closeNav);
  if (overlay) overlay.addEventListener("click", closeNav);
  $$(".mobile-nav a").forEach(function (a) { a.addEventListener("click", closeNav); });

  /* ---- Opener "show all" toggle ---- */
  var openerToggle = $("#openerToggle");
  var openerMore = $("#openerMore");
  if (openerToggle && openerMore) {
    openerToggle.addEventListener("click", function () {
      var shown = openerMore.classList.toggle("show");
      openerToggle.setAttribute("aria-expanded", shown ? "true" : "false");
      $(".ot-text", openerToggle).textContent = shown ? "Show fewer openers" : "Show all 7 openers";
      $(".ot-chev", openerToggle).style.transform = shown ? "rotate(180deg)" : "";
      if (shown) {
        // reveal newly shown cards smoothly
        $$(".opener-card", openerMore).forEach(function (c, i) {
          c.style.opacity = 0; c.style.transform = "translateY(16px)";
          setTimeout(function () {
            c.style.transition = "opacity .4s ease, transform .4s ease";
            c.style.opacity = 1; c.style.transform = "none";
          }, 40 * i);
        });
      }
    });
  }

  /* ---- FAQ accordion ---- */
  $$(".faq-item").forEach(function (item) {
    var q = $(".faq-q", item);
    var a = $(".faq-a", item);
    q.addEventListener("click", function () {
      var isOpen = item.classList.contains("open");
      // close others
      $$(".faq-item").forEach(function (other) {
        other.classList.remove("open");
        $(".faq-a", other).style.maxHeight = null;
      });
      if (!isOpen) {
        item.classList.add("open");
        a.style.maxHeight = a.scrollHeight + "px";
      }
    });
  });

  /* ---- Reveal on scroll (with stagger) ---- */
  var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var revealEls = $$(".reveal");
  // stagger items that share a parent so grids cascade in
  if (!reduceMotion) {
    var groups = {};
    revealEls.forEach(function (el) {
      var p = el.parentNode;
      if (!p.__rk) { p.__rk = "g" + Math.random().toString(36).slice(2); }
      (groups[p.__rk] = groups[p.__rk] || []).push(el);
    });
    Object.keys(groups).forEach(function (k) {
      groups[k].forEach(function (el, i) {
        if (groups[k].length > 1) el.style.setProperty("--d", Math.min(i * 75, 450) + "ms");
      });
    });
  }
  if ("IntersectionObserver" in window && revealEls.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add("in"); });
  }

  /* ---- Animated number count-up ---- */
  function countUp(el) {
    var target = parseFloat(el.getAttribute("data-count"));
    if (isNaN(target)) return;
    var dec = parseInt(el.getAttribute("data-decimals") || "0", 10);
    var suffix = el.getAttribute("data-suffix") || "";
    var sufHtml = suffix ? '<span class="count-suffix">' + suffix + "</span>" : "";
    if (reduceMotion) { el.innerHTML = target.toFixed(dec) + sufHtml; return; }
    var start = null, dur = 1300;
    function step(ts) {
      if (!start) start = ts;
      var p = Math.min((ts - start) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      el.innerHTML = (target * eased).toFixed(dec) + sufHtml;
      if (p < 1) requestAnimationFrame(step);
      else el.innerHTML = target.toFixed(dec) + sufHtml;
    }
    requestAnimationFrame(step);
  }
  var counters = $$(".count");
  if ("IntersectionObserver" in window && counters.length) {
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { countUp(e.target); cio.unobserve(e.target); }
      });
    }, { threshold: 0.5 });
    counters.forEach(function (el) { cio.observe(el); });
  } else {
    counters.forEach(countUp);
  }

  /* ---- Back to top ---- */
  if (toTop) toTop.addEventListener("click", function () {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });

  /* ---- Contact form (front-end demo handler) ----
     No backend yet. To receive submissions, connect this form to a service
     like Formspree, Netlify Forms, or your own endpoint. For now it validates,
     shows a success message, and offers a mailto fallback. */
  var form = $("#quoteForm");
  var success = $("#formSuccess");
  // Where leads are delivered. FormSubmit relays this to the inbox (no backend
  // needed). NOTE: the first real submission triggers a one-time activation
  // email to this address — click that link once and every future lead arrives.
  var LEAD_EMAIL = "info@northshoregaragedoors.ca";
  var FORM_ENDPOINT = "https://formsubmit.co/ajax/" + LEAD_EMAIL;

  function showSuccess() {
    if (form) form.style.display = "none";
    if (success) success.classList.add("show");
    if (success) success.scrollIntoView({ behavior: "smooth", block: "center" });
  }
  function mailtoFallback(name, phone, email, service, msg) {
    var body = "Name: " + name + "\r\nPhone: " + phone +
      "\r\nEmail: " + email + "\r\nService: " + service + "\r\n\r\n" + msg;
    var mailto = "mailto:" + LEAD_EMAIL + "?subject=" +
      encodeURIComponent("Quote request from " + name) +
      "&body=" + encodeURIComponent(body);
    try { window.location.href = mailto; } catch (err) {}
  }

  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var name = $("#f-name").value.trim();
      var phone = $("#f-phone").value.trim();
      if (!name || !phone) {
        if (!name) $("#f-name").focus(); else $("#f-phone").focus();
        return;
      }
      var email = $("#f-email").value.trim();
      var service = $("#f-service").value;
      var msg = $("#f-msg").value.trim();
      var honey = $("#f-company"); // honeypot — bots fill this, humans don't
      if (honey && honey.value) { showSuccess(); return; }

      var btn = form.querySelector('button[type="submit"]');
      var label = btn ? btn.textContent : "";
      if (btn) { btn.disabled = true; btn.textContent = "Sending…"; }

      var payload = {
        name: name, phone: phone, email: email,
        service: service, message: msg,
        _subject: "New quote request — North Shore Garage Doors website",
        _template: "table"
      };

      fetch(FORM_ENDPOINT, {
        method: "POST",
        headers: { "Content-Type": "application/json", "Accept": "application/json" },
        body: JSON.stringify(payload)
      }).then(function (r) {
        return r.json().catch(function () { return {}; }).then(function (data) {
          return { ok: r.ok, data: data };
        });
      }).then(function (res) {
        if (res.ok) { showSuccess(); }
        else { showSuccess(); mailtoFallback(name, phone, email, service, msg); }
      }).catch(function () {
        // network/endpoint issue — still confirm to the user and open their mail app
        showSuccess();
        mailtoFallback(name, phone, email, service, msg);
      }).then(function () {
        if (btn) { btn.disabled = false; btn.textContent = label; }
      });
    });
  }

  /* ---- Footer year ---- */
  var yr = $("#year");
  if (yr) yr.textContent = new Date().getFullYear();

})();
