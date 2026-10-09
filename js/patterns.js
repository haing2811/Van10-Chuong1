/* patterns.js — background pattern life.
   Two jobs, both tiny: pause the drift while the page is hidden, and
   drive the scroll-parallax custom property only on browsers that lack
   CSS scroll-driven animations (patterns.css owns the rest; motion is
   transform-only and entirely off under prefers-reduced-motion). The
   media query is re-read live so a mid-session OS motion toggle stays
   in sync without a reload. */
(function () {
  "use strict";

  var root = document.querySelector(".bg-pattern");
  if (root) {
    document.addEventListener("visibilitychange", function () {
      root.classList.toggle("is-paused", document.hidden);
    });
  }

  // Parallax comes from CSS scroll-driven animation when supported —
  // nothing to do here in that case.
  if (!window.CSS || !window.CSS.supports ||
      window.CSS.supports("animation-timeline", "scroll()")) {
    return;
  }

  var mq = window.matchMedia &&
    window.matchMedia("(prefers-reduced-motion: reduce)");
  var listening = false;
  var ticking = false;

  function update() {
    ticking = false;
    var y = window.scrollY || window.pageYOffset || 0;
    // Tiny, against the content (the pattern sinks as the page rises),
    // capped so long pages stop shifting it.
    var shift = Math.min(24, y * 0.03);
    document.documentElement.style.setProperty("--bg-shift", shift.toFixed(1) + "px");
  }
  function onScroll() {
    if (!ticking) {
      ticking = true;
      window.requestAnimationFrame(update);
    }
  }
  function apply() {
    if (mq && mq.matches) {
      if (listening) {
        window.removeEventListener("scroll", onScroll);
        listening = false;
      }
      document.documentElement.style.removeProperty("--bg-shift");
    } else if (!listening) {
      window.addEventListener("scroll", onScroll, { passive: true });
      listening = true;
      update();
    }
  }

  if (mq) {
    if (mq.addEventListener) mq.addEventListener("change", apply);
    else if (mq.addListener) mq.addListener(apply); // older Safari/Edge
  }
  apply();
})();
