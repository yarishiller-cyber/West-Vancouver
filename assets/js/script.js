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

  /* ---- Reveal on scroll ---- */
  var revealEls = $$(".reveal");
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
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var name = $("#f-name").value.trim();
      var phone = $("#f-phone").value.trim();
      if (!name || !phone) {
        if (!name) $("#f-name").focus(); else $("#f-phone").focus();
        return;
      }
      // Build a mailto fallback so the message can actually be delivered.
      var email = $("#f-email").value.trim();
      var service = $("#f-service").value;
      var msg = $("#f-msg").value.trim();
      var body = "Name: " + name + "%0D%0APhone: " + phone +
        "%0D%0AEmail: " + email + "%0D%0AService: " + service +
        "%0D%0A%0D%0A" + encodeURIComponent(msg);
      var mailto = "mailto:info@northshoregaragedoors.ca?subject=" +
        encodeURIComponent("Quote request from " + name) + "&body=" + body;

      form.style.display = "none";
      if (success) success.classList.add("show");
      // open the user's mail client as a delivery fallback
      try { window.location.href = mailto; } catch (err) {}
    });
  }

  /* ---- Footer year ---- */
  var yr = $("#year");
  if (yr) yr.textContent = new Date().getFullYear();

})();
