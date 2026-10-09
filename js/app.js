(function () {
  "use strict";
  var TABS = [
    { key: "doc", label: "Đọc", get: function () { return window.CONTENT.doc || []; } },
    { key: "viet", label: "Viết", get: function () { return window.CONTENT.viet || []; } },
    { key: "noi", label: "Nói và nghe", get: function () { return window.CONTENT.noi || []; } }
  ];
  var view = document.getElementById("view");
  var tabBtns = Array.prototype.slice.call(document.querySelectorAll('[role="tab"]'));

  function esc(s) { return String(s === null || s === undefined ? "" : s); }

  // Exactly one stamp per top-level section, driven by data-source="draft".
  function draftStamp() {
    var c = document.createElement("span");
    c.className = "stamp-draft";
    c.textContent = "Nháp - cần duyệt";
    return c;
  }

  function sectionIsDraft(s) {
    return s.source === "draft" ||
      (s.blocks || []).some(function (b) { return b.source === "draft"; });
  }

  function renderBlock(block) {
    var A = window.Activities, Q = window.Quiz;
    switch (block.type) {
      case "p": {
        var p = document.createElement("p");
        p.textContent = esc(block.text);
        return p;
      }
      case "list": {
        var ul = document.createElement("ul");
        (block.items || []).forEach(function (it) {
          var li = document.createElement("li");
          li.textContent = esc(it);
          ul.appendChild(li);
        });
        return ul;
      }
      case "h3": {
        var h = document.createElement("h3");
        h.className = "subhead";
        h.textContent = esc(block.text);
        return h;
      }
      case "qa": return A.renderQa(block);
      case "quiz": return Q.render(block);
      case "checklist": return A.renderChecklist(block);
      case "tablefill": return A.renderTableFill(block);
      case "write150": return A.renderWrite150(block);
      case "outlinebuilder":
      case "talkbuilder": return A.renderBuilder(block);
      case "speechtools": return A.renderSpeechTools(block);
      case "reviewtable": return A.renderReviewTable(block);
      case "img": return A.renderImg(block);
      default: {
        var d = document.createElement("p");
        d.textContent = esc(block.text || "");
        return d;
      }
    }
  }

  function currentRoute() {
    var h = (location.hash || "").replace(/^#/, "");
    var parts = h.split("/");
    var tab = parts[0] || window.Store.get("last-tab", "doc");
    if (!TABS.some(function (t) { return t.key === tab; })) tab = "doc";
    return { tab: tab, section: parts[1] || null };
  }

  var currentTab = null;
  var spy = null;
  var railLinks = {};
  var activeWarn = null;
  var reduceMotion = !!(window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches);

  function setActive(id) {
    Object.keys(railLinks).forEach(function (k) {
      var a = railLinks[k];
      if (!a) return;
      if (k === id) a.setAttribute("aria-current", "true");
      else a.removeAttribute("aria-current");
    });
  }

  function scrollToSection(id, smooth) {
    var behavior = (smooth && !reduceMotion) ? "smooth" : "auto";
    var target = id ? document.getElementById("sec-" + id) : null;
    if (!target) {
      if (behavior === "smooth") window.scrollTo({ top: 0, behavior: "smooth" });
      else window.scrollTo(0, 0);
      return;
    }
    target.scrollIntoView({ behavior: behavior, block: "start" });
  }

  function buildCard(tabKey, s) {
    var card = document.createElement("section");
    card.className = "card scroll-paper grain";
    card.id = "sec-" + s.id;
    card.setAttribute("aria-labelledby", "h-" + s.id);
    var isDraft = sectionIsDraft(s);
    if (isDraft) card.setAttribute("data-source", "draft");
    var h2 = document.createElement("h2");
    h2.id = "h-" + s.id;
    h2.textContent = s.title;
    if (isDraft) h2.appendChild(draftStamp());
    card.appendChild(h2);
    (s.blocks || []).forEach(function (b) {
      try { card.appendChild(renderBlock(b)); }
      catch (e) {
        var err = document.createElement("p");
        err.textContent = "Không hiển thị được một khối nội dung.";
        card.appendChild(err);
      }
    });
    var back = document.createElement("p");
    var toplink = document.createElement("a");
    toplink.href = "#" + tabKey + "/" + s.id;
    toplink.textContent = "Liên kết tới mục này";
    toplink.className = "tag-src";
    back.appendChild(toplink);
    card.appendChild(back);
    return card;
  }

  function render() {
    var route = currentRoute();
    tabBtns.forEach(function (b) {
      b.setAttribute("aria-selected", String(b.dataset.tab === route.tab));
    });
    document.documentElement.setAttribute("data-tab", route.tab);
    window.Store.set("last-tab", route.tab);
    var tab = TABS.filter(function (t) { return t.key === route.tab; })[0];
    var sections = tab.get();
    var known = !route.section || sections.some(function (s) { return s.id === route.section; });
    var fresh = (currentTab !== route.tab);

    if (fresh) {
      currentTab = route.tab;
      if (spy) { spy.disconnect(); spy = null; }
      railLinks = {};
      view.innerHTML = "";
      var layout = document.createElement("div");
      layout.className = "tab-layout";
      var nav = document.createElement("nav");
      nav.className = "side-rail";
      nav.setAttribute("aria-label", "Các mục trong tab " + tab.label);
      var ul = document.createElement("ul");
      sections.forEach(function (s) {
        var li = document.createElement("li");
        var a = document.createElement("a");
        a.href = "#" + tab.key + "/" + s.id;
        a.textContent = s.title;
        li.appendChild(a);
        ul.appendChild(li);
        railLinks[s.id] = a;
      });
      nav.appendChild(ul);
      layout.appendChild(nav);
      var list = document.createElement("div");
      list.className = "tab-sections";
      activeWarn = document.createElement("p");
      activeWarn.className = "route-warn";
      activeWarn.hidden = true;
      list.appendChild(activeWarn);
      sections.forEach(function (s) {
        list.appendChild(buildCard(tab.key, s));
      });
      layout.appendChild(list);
      view.appendChild(layout);
      if ("IntersectionObserver" in window) {
        spy = new IntersectionObserver(function (entries) {
          entries.forEach(function (en) {
            if (en.isIntersecting) setActive(en.target.id.replace(/^sec-/, ""));
          });
        }, { rootMargin: "-30% 0px -60% 0px", threshold: 0 });
        Array.prototype.forEach.call(list.querySelectorAll(".card"), function (c) { spy.observe(c); });
      }
    }

    if (activeWarn) {
      if (route.section && !known) {
        activeWarn.hidden = false;
        activeWarn.textContent = "Không tìm thấy mục này. Hiện toàn bộ tab " + tab.label + ".";
      } else {
        activeWarn.hidden = true;
      }
    }
    if (route.section && known) {
      setActive(route.section);
      scrollToSection(route.section, !fresh);
    } else if (!route.section) {
      if (sections.length) setActive(sections[0].id);
      if (fresh) window.scrollTo(0, 0);
    } else {
      scrollToSection(null, !fresh);
    }
  }

  function initDisplay() {
    var root = document.documentElement;
    root.setAttribute("data-theme", window.Store.get("theme", "light"));
    root.setAttribute("data-fs", window.Store.get("fs", "medium"));
    var bt = document.getElementById("btn-theme");
    var up = document.getElementById("btn-fs-up");
    var down = document.getElementById("btn-fs-down");
    function syncTheme() {
      var dark = root.getAttribute("data-theme") === "dark";
      bt.textContent = dark ? "Sáng" : "Tối";
      bt.setAttribute("aria-pressed", String(dark));
    }
    syncTheme();
    if (bt) bt.addEventListener("click", function () {
      var next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      window.Store.set("theme", next);
      syncTheme();
    });
    var order = ["small", "medium", "large"];
    function step(d) {
      var i = order.indexOf(root.getAttribute("data-fs"));
      i = Math.max(0, Math.min(order.length - 1, i + d));
      root.setAttribute("data-fs", order[i]);
      window.Store.set("fs", order[i]);
    }
    if (up) up.addEventListener("click", function () { step(1); });
    if (down) down.addEventListener("click", function () { step(-1); });
  }

  function init() {
    initDisplay();
    tabBtns.forEach(function (b) {
      b.addEventListener("click", function () {
        location.hash = "#" + b.dataset.tab;
      });
    });
    window.addEventListener("hashchange", function () {
      var r = currentRoute();
      if (r.section) window.Store.set("last-section-" + r.tab, r.section);
      render();
    });
    var si = document.getElementById("search-input");
    var sr = document.getElementById("search-results");
    if (window.Search) window.Search.init(si, sr);
    if (!location.hash) {
      var lastTab = window.Store.get("last-tab", "doc");
      var lastSec = window.Store.get("last-section-" + lastTab, null);
      location.hash = "#" + lastTab + (lastSec ? "/" + lastSec : "");
    }
    render();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
