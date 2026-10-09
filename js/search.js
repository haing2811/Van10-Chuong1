(function () {
  function collectText(block) {
    var parts = [];
    if (block.title) parts.push(block.title);
    if (block.text) parts.push(block.text);
    if (block.q) parts.push(block.q);
    if (block.a) parts.push(block.a);
    if (block.prompt) parts.push(block.prompt);
    if (block.items) parts.push(block.items.join(" "));
    if (block.questions) {
      block.questions.forEach(function (qq) {
        parts.push(qq.q + " " + (qq.options || []).join(" "));
      });
    }
    return parts.join(" ");
  }
  function norm(s) {
    return (s || "").toLowerCase();
  }
  function searchAll(query) {
    query = norm(query).trim();
    if (query.length < 2) return [];
    var tabs = { doc: window.CONTENT.doc || [], viet: window.CONTENT.viet || [], noi: window.CONTENT.noi || [] };
    var hits = [];
    var tabNames = { doc: "Đọc", viet: "Viết", noi: "Nói và nghe" };
    Object.keys(tabs).forEach(function (tab) {
      tabs[tab].forEach(function (sec) {
        var hay = norm(sec.title + " " + (sec.blocks || []).map(collectText).join(" "));
        if (hay.indexOf(query) !== -1) {
          hits.push({ tab: tab, tabName: tabNames[tab], id: sec.id, title: sec.title, source: sec.source });
          if (hits.length >= 20) return;
        }
      });
    });
    return hits.slice(0, 20);
  }
  function init(inputEl, resultsEl) {
    if (!inputEl || !resultsEl) return;
    var timer;
    inputEl.addEventListener("input", function () {
      clearTimeout(timer);
      timer = setTimeout(function () {
        var q = inputEl.value;
        resultsEl.innerHTML = "";
        if (norm(q).trim().length < 2) { resultsEl.hidden = true; return; }
        var hits = searchAll(q);
        if (!hits.length) {
          resultsEl.hidden = false;
          resultsEl.textContent = "Không tìm thấy. Thử: thần thoại, Huấn Cao, Hán Việt...";
          return;
        }
        resultsEl.hidden = false;
        var ul = document.createElement("ul");
        hits.forEach(function (h) {
          var li = document.createElement("li");
          var a = document.createElement("a");
          a.href = "#" + h.tab + "/" + h.id;
          a.textContent = h.tabName + " — " + h.title;
          var src = document.createElement("span");
          src.className = "hit-src";
          src.textContent = h.source === "draft" ? " (chưa duyệt)" : "";
          a.appendChild(src);
          li.appendChild(a);
          ul.appendChild(li);
        });
        resultsEl.appendChild(ul);
      }, 200);
    });
    document.addEventListener("click", function (e) {
      if (!resultsEl.contains(e.target) && e.target !== inputEl) resultsEl.hidden = true;
    });
  }
  window.Search = { init: init, searchAll: searchAll };
})();
