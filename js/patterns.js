/* patterns.js — background pattern life.
   Two jobs, both tiny: pause the drift while the page is hidden, and
   drive the scroll-parallax custom property only on browsers that lack
   CSS scroll-driven animations (patterns.css owns the rest; motion is
   transform-only and entirely off under prefers-reduced-motion). */
(function () {
  "use strict";

  var reduce = !!(window.matchMedia &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches);

  var root = document.querySelector(".bg-pattern");
  if (root) {
    document.addEventListener("visibilitychange", function () {
      root.classList.toggle("is-paused", document.hidden);
    });
  }

  if (reduce || !window.CSS || !window.CSS.supports ||
      window.CSS.supports("animation-timeline", "scroll()")) {
    return; // parallax comes from CSS scroll-driven animation
  }

  var ticking = false;
  function update() {
    ticking = false;
    var y = window.scrollY || window.pageYOffset || 0;
    // Tiny, against the content (the pattern sinks as the page rises),
    // capped so long pages stop shifting it.
    var shift = Math.min(24, y * 0.03);
    document.documentElement.style.setProperty("--bg-shift", shift.toFixed(1) + "px");
  }
  window.addEventListener("scroll", function () {
    if (!ticking) {
      ticking = true;
      window.requestAnimationFrame(update);
    }
  }, { passive: true });
  update();
})();
