/* West Vancouver Garage Doors — interactions */
(function () {
  "use strict";

  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var REDUCED = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---- Header shadow on scroll + back-to-top ---- */
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
  var navToggle = $("#navToggle"), mobileNav = $("#mobileNav"),
      overlay = $("#overlay"), mnClose = $("#mnClose");
  function openNav() {
    if (!mobileNav) return;
    mobileNav.classList.add("open"); overlay.classList.add("open");
    navToggle.classList.add("open"); navToggle.setAttribute("aria-expanded", "true");
    document.body.style.overflow = "hidden";
  }
  function closeNav() {
    if (!mobileNav) return;
    mobileNav.classList.remove("open"); overlay.classList.remove("open");
    navToggle.classList.remove("open"); navToggle.setAttribute("aria-expanded", "false");
    document.body.style.overflow = "";
  }
  if (navToggle) navToggle.addEventListener("click", openNav);
  if (mnClose) mnClose.addEventListener("click", closeNav);
  if (overlay) overlay.addEventListener("click", closeNav);
  $$(".mobile-nav a").forEach(function (a) { a.addEventListener("click", closeNav); });

  /* ---- Opener "show all" toggle ---- */
  var openerToggle = $("#openerToggle"), openerMore = $("#openerMore");
  if (openerToggle && openerMore) {
    openerToggle.addEventListener("click", function () {
      var shown = openerMore.classList.toggle("show");
      openerToggle.setAttribute("aria-expanded", shown ? "true" : "false");
      $(".ot-text", openerToggle).textContent = shown ? "Show fewer openers" : "Show all 7 openers";
      $(".ot-chev", openerToggle).style.transform = shown ? "rotate(180deg)" : "";
    });
  }

  /* ---- FAQ accordion ---- */
  $$(".faq-item").forEach(function (item) {
    var q = $(".faq-q", item), a = $(".faq-a", item);
    if (!q || !a) return;
    q.addEventListener("click", function () {
      var isOpen = item.classList.contains("open");
      $$(".faq-item").forEach(function (other) {
        other.classList.remove("open");
        var oa = $(".faq-a", other); if (oa) oa.style.maxHeight = null;
        var ob = $(".faq-q", other); if (ob) ob.setAttribute("aria-expanded", "false");
      });
      if (!isOpen) {
        item.classList.add("open");
        a.style.maxHeight = a.scrollHeight + "px";
        q.setAttribute("aria-expanded", "true");
      }
    });
  });

  /* ---- Footer "Pricing" toggle (FLEET standard: reveal [data-px] values) ---- */
  var priceBtn = $("#pricing-toggle");
  if (priceBtn) {
    var els = $$("[data-px]"), saved = new Array(els.length), on = false;
    priceBtn.addEventListener("click", function () {
      on = !on;
      els.forEach(function (el, i) {
        if (on) { if (saved[i] == null) saved[i] = el.innerHTML; el.innerHTML = el.getAttribute("data-px"); }
        else { if (saved[i] != null) el.innerHTML = saved[i]; }
      });
      document.body.classList.toggle("show-pricing", on);
      priceBtn.textContent = on ? "Hide pricing" : "Show pricing";
      priceBtn.setAttribute("aria-pressed", on ? "true" : "false");
    });
  }

  /* ---- Animated stat counters (data-count="10000" data-suffix="+") ---- */
  var counters = $$("[data-count]");
  if (counters.length && "IntersectionObserver" in window && !REDUCED) {
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        cio.unobserve(e.target);
        var el = e.target, end = parseFloat(el.getAttribute("data-count")),
            suffix = el.getAttribute("data-suffix") || "", t0 = null, dur = 1400;
        function tick(t) {
          if (!t0) t0 = t;
          var p = Math.min((t - t0) / dur, 1), eased = 1 - Math.pow(1 - p, 3);
          var val = Math.round(end * eased);
          el.textContent = (val >= 1000 ? val.toLocaleString() : val) + suffix;
          if (p < 1) requestAnimationFrame(tick);
        }
        requestAnimationFrame(tick);
      });
    }, { threshold: 0.5 });
    counters.forEach(function (c) { cio.observe(c); });
  }

  /* ---- Scroll-driven "exploded view" garage-door scrubber -------------------
     Preloads the door-NN.webp sequence and draws the frame that matches the
     user's scroll position through the pinned section. Pure canvas + rAF, so it
     stays 60fps. Reduced-motion + no-canvas degrade to a single static frame. */
  var stage = $("#anatomyStage");
  if (stage) {
    var canvas = $("#anatomyCanvas", stage),
        track = $("#anatomyTrack"),
        steps = $$(".anatomy-step"),
        FRAMES = parseInt(stage.getAttribute("data-frames"), 10) || 9,
        path = stage.getAttribute("data-path") || "assets/anim/door-",
        imgs = [], loaded = 0, ctx = canvas && canvas.getContext("2d"),
        dpr = Math.min(window.devicePixelRatio || 1, 2), current = -1;

    function sizeCanvas() {
      if (!canvas) return;
      var r = canvas.getBoundingClientRect();
      canvas.width = r.width * dpr; canvas.height = r.height * dpr;
      draw(current < 0 ? 0 : current, true);
    }
    function draw(i, force) {
      if (!ctx) return;
      i = Math.max(0, Math.min(FRAMES - 1, i));
      if (i === current && !force) return;
      current = i;
      var img = imgs[i];
      if (!img || !img.complete || !img.naturalWidth) return;
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      // contain-fit the square frame into the canvas
      var cw = canvas.width, ch = canvas.height,
          scale = Math.min(cw / img.naturalWidth, ch / img.naturalHeight),
          w = img.naturalWidth * scale, h = img.naturalHeight * scale;
      ctx.drawImage(img, (cw - w) / 2, (ch - h) / 2, w, h);
    }
    for (var i = 0; i < FRAMES; i++) {
      (function (n) {
        var im = new Image();
        im.onload = function () { loaded++; if (loaded === 1) sizeCanvas(); if (n === 0) draw(0, true); };
        im.src = path + String(n).padStart(2, "0") + ".webp";
        imgs[n] = im;
      })(i);
    }

    function onAnatomyScroll() {
      if (!track) return;
      var rect = track.getBoundingClientRect(),
          vh = window.innerHeight,
          total = rect.height - vh,
          p = total > 0 ? Math.min(Math.max((-rect.top) / total, 0), 1) : 0;
      draw(Math.round(p * (FRAMES - 1)));
      // light-up the active caption step
      if (steps.length) {
        var active = Math.min(steps.length - 1, Math.floor(p * steps.length));
        steps.forEach(function (s, idx) { s.classList.toggle("active", idx === active); });
      }
    }

    if (REDUCED || !ctx) {
      // Static, informative end-state; no pinning needed.
      stage.classList.add("static");
      if (track) track.style.height = "auto";
      imgs[FRAMES - 1] && (imgs[FRAMES - 1].onload = function () { draw(FRAMES - 1, true); });
      draw(FRAMES - 1, true);
      if (steps.length) steps.forEach(function (s) { s.classList.add("active"); });
    } else {
      window.addEventListener("scroll", onAnatomyScroll, { passive: true });
      window.addEventListener("resize", function () { sizeCanvas(); onAnatomyScroll(); });
      onAnatomyScroll();
    }
  }

  /* ---- Back to top ---- */
  if (toTop) toTop.addEventListener("click", function () {
    window.scrollTo({ top: 0, behavior: REDUCED ? "auto" : "smooth" });
  });

  /* ---- Contact / partner form (front-end handler with mailto fallback) ---- */
  $$("form[data-quote]").forEach(function (form) {
    var success = $(".form-success", form.parentNode) || $("#formSuccess");
    var to = form.getAttribute("data-to") || "info@westvangaragedoors.ca";
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var name = (form.querySelector("[name=name]") || {}).value, phone = (form.querySelector("[name=phone]") || {}).value;
      if (name != null && !String(name).trim()) { form.querySelector("[name=name]").focus(); return; }
      if (phone != null && !String(phone).trim()) { form.querySelector("[name=phone]").focus(); return; }
      var lines = [];
      $$("input,select,textarea", form).forEach(function (f) {
        if (f.name && f.value) lines.push(f.name + ": " + f.value);
      });
      var subject = (form.getAttribute("data-subject") || "Website enquiry") + (name ? " — " + name : "");
      var mailto = "mailto:" + to + "?subject=" + encodeURIComponent(subject) +
        "&body=" + encodeURIComponent(lines.join("\n"));
      form.style.display = "none";
      if (success) success.classList.add("show");
      try { window.location.href = mailto; } catch (err) {}
    });
  });

  /* ---- Footer year ---- */
  var yr = $("#year"); if (yr) yr.textContent = new Date().getFullYear();
})();
