(function () {
  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text !== undefined && text !== null) n.textContent = text;
    return n;
  }
  function renderQa(block) {
    var box = el("div", "qa");
    box.appendChild(el("span", "box-label", "Câu hỏi"));
    box.appendChild(el("p", "q", block.q));
    var ta = document.createElement("textarea");
    ta.setAttribute("aria-label", "Câu trả lời của em");
    ta.placeholder = "Em gõ câu trả lời của mình ở đây (tự động lưu)...";
    var key = "qa-" + block.id;
    ta.value = window.Store.get(key, "");
    var saveNote = el("span", "tag-src", window.Store.persistent() ? "" : "Bản lưu tạm (trình duyệt chặn lưu trữ).");
    var typing;
    ta.addEventListener("input", function () {
      clearTimeout(typing);
      typing = setTimeout(function () { window.Store.set(key, ta.value); }, 300);
    });
    var qField = el("div", "field");
    qField.appendChild(ta);
    box.appendChild(qField);
    var row = el("div", "row");
    var btn = el("button", "btn-brush ghost", "Xem gợi ý");
    btn.type = "button";
    btn.setAttribute("aria-expanded", "false");
    var ans = el("div", "answer");
    ans.hidden = true;
    ans.appendChild(el("div", "lbl", "Gợi ý (tham khảo)"));
    ans.appendChild(el("p", null, block.a || ""));
    btn.addEventListener("click", function () {
      ans.hidden = !ans.hidden;
      btn.textContent = ans.hidden ? "Xem gợi ý" : "Ẩn gợi ý";
      btn.setAttribute("aria-expanded", String(!ans.hidden));
    });
    var clear = el("button", "btn-brush ghost", "Xoá bài của em");
    clear.type = "button";
    clear.addEventListener("click", function () {
      ta.value = "";
      window.Store.set(key, "");
    });
    row.appendChild(btn);
    row.appendChild(clear);
    row.appendChild(saveNote);
    box.appendChild(row);
    box.appendChild(ans);
    return box;
  }

  function renderChecklist(block) {
    var box = el("div", "qa");
    box.appendChild(el("p", "q", block.title || "Danh sách kiểm tra"));
    var key = "check-" + block.id;
    var saved = window.Store.get(key, {});
    (block.items || []).forEach(function (item, i) {
      var lab = el("label", "opt");
      lab.style.display = "block";
      lab.style.padding = ".4rem 0";
      var cb = document.createElement("input");
      cb.type = "checkbox";
      cb.checked = !!saved[i];
      cb.style.width = "1.2rem";
      cb.style.height = "1.2rem";
      cb.style.marginRight = ".5rem";
      cb.setAttribute("aria-label", item);
      cb.addEventListener("change", function () {
        saved[i] = cb.checked;
        window.Store.set(key, saved);
      });
      lab.appendChild(cb);
      lab.appendChild(document.createTextNode(item));
      box.appendChild(lab);
    });
    return box;
  }

  function renderTableFill(block) {
    var box = el("div", "exercise");
    box.appendChild(el("p", "q", block.title || "Bảng tự điền"));
    var key = "table-" + block.id;
    var saved = window.Store.get(key, null);
    var table = el("table", "fill");
    var thead = document.createElement("thead");
    var hr = document.createElement("tr");
    (block.columns || []).forEach(function (c) { hr.appendChild(el("th", null, c)); });
    thead.appendChild(hr);
    table.appendChild(thead);
    var tbody = document.createElement("tbody");
    var inputs = [];
    (block.rows || []).forEach(function (row, ri) {
      var tr = document.createElement("tr");
      row.forEach(function (cell, ci) {
        var td = document.createElement("td");
        if (cell === null || cell === undefined) {
          var inp = document.createElement(ci === 0 ? "input" : "textarea");
          inp.value = (saved && saved[ri] && saved[ri][ci]) || "";
          inp.setAttribute("aria-label", (block.columns || [])[ci] + " hàng " + (ri + 1));
          inp.addEventListener("input", function () {
            var cur = window.Store.get(key, {});
            if (!cur[ri]) cur[ri] = {};
            cur[ri][ci] = inp.value;
            window.Store.set(key, cur);
          });
          inputs.push(inp);
          td.appendChild(inp);
        } else {
          td.textContent = cell;
        }
        tr.appendChild(td);
      });
      tbody.appendChild(tr);
    });
    table.appendChild(tbody);
    box.appendChild(table);
    if (block.suggested) {
      var btn = el("button", "btn-brush ghost", "Đối chiếu gợi ý");
      btn.type = "button";
      var sug = el("div", "answer");
      sug.hidden = true;
      btn.addEventListener("click", function () {
        sug.hidden = !sug.hidden;
        btn.textContent = sug.hidden ? "Đối chiếu gợi ý" : "Ẩn gợi ý";
        if (!sug.hidden && !sug.hasChildNodes()) {
          var t2 = el("table", "fill");
          var h2 = document.createElement("tr");
          (block.columns || []).forEach(function (c) { h2.appendChild(el("th", null, c)); });
          t2.appendChild(h2);
          block.suggested.forEach(function (row) {
            var tr = document.createElement("tr");
            row.forEach(function (c) { tr.appendChild(el("td", null, c || "")); });
            t2.appendChild(tr);
          });
          sug.appendChild(t2);
        }
      });
      box.appendChild(btn);
      box.appendChild(sug);
    }
    return box;
  }

  function countWords(s) {
    s = (s || "").trim();
    if (!s) return 0;
    return s.split(/\s+/).length;
  }

  function renderWrite150(block) {
    var box = el("div", "exercise");
    box.appendChild(el("p", "q", block.prompt));
    var key = "write-" + block.id;
    var ta = document.createElement("textarea");
    ta.value = window.Store.get(key, "");
    ta.setAttribute("aria-label", "Bài viết khoảng 150 chữ");
    var counter = el("div", "counter", countWords(ta.value) + " từ (mục tiêu khoảng 150)");
    ta.addEventListener("input", function () {
      var n = countWords(ta.value);
      counter.textContent = n + " từ (mục tiêu khoảng 150)" + (n < 130 ? " — còn thiếu" : n > 170 ? " — hơi dài" : " — đạt");
      window.Store.set(key, ta.value);
    });
    var wField = el("div", "field");
    wField.appendChild(ta);
    box.appendChild(wField);
    box.appendChild(counter);
    var row = el("div", "row");
    var clr = el("button", "btn-brush ghost", "Xoá bản nháp");
    clr.type = "button";
    clr.addEventListener("click", function () {
      ta.value = "";
      window.Store.set(key, "");
      counter.textContent = "0 từ (mục tiêu khoảng 150)";
    });
    row.appendChild(clr);
    box.appendChild(row);
    return box;
  }

  function renderBuilder(block) {
    var box = el("div", "exercise");
    box.appendChild(el("p", "q", block.title || "Công cụ lập dàn ý"));
    var key = "builder-" + block.id;
    var saved = window.Store.get(key, {});
    var areas = {};
    (block.fields || []).forEach(function (f) {
      box.appendChild(el("p", null, f.label));
      var ta = document.createElement("textarea");
      ta.placeholder = f.hint || "";
      ta.value = saved[f.key] || "";
      ta.setAttribute("aria-label", f.label);
      ta.addEventListener("input", function () {
        saved[f.key] = ta.value;
        window.Store.set(key, saved);
      });
      areas[f.key] = ta;
      var fWrap = el("div", "field");
      fWrap.appendChild(ta);
      box.appendChild(fWrap);
    });
    var row = el("div", "row");
    var copy = el("button", "btn-brush ghost", "Sao chép dàn ý");
    copy.type = "button";
    copy.addEventListener("click", function () {
      var text = (block.fields || []).map(function (f) {
        return f.label + "\n" + (areas[f.key].value || "") + "\n";
      }).join("\n");
      function done() { copy.textContent = "Đã sao chép"; setTimeout(function () { copy.textContent = "Sao chép dàn ý"; }, 1500); }
      function fallback() {
        var tmp = document.createElement("textarea");
        tmp.value = text;
        document.body.appendChild(tmp);
        tmp.select();
        try { document.execCommand("copy"); done(); } catch (e) { /* clipboard unavailable */ }
        document.body.removeChild(tmp);
      }
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(done, function () { fallback(); });
      } else { fallback(); }
    });
    var dl = el("button", "btn-brush ghost", "Tải file .txt");
    dl.type = "button";
    dl.addEventListener("click", function () {
      var text = (block.fields || []).map(function (f) {
        return f.label + "\n" + (areas[f.key].value || "") + "\n";
      }).join("\n");
      var blob = new Blob([text], { type: "text/plain;charset=utf-8" });
      var a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      a.download = block.id + ".txt";
      document.body.appendChild(a);
      a.click();
      setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 500);
    });
    row.appendChild(copy);
    row.appendChild(dl);
    box.appendChild(row);
    return box;
  }

  function renderSpeechTools(block) {
    var box = el("div", "qa");
    box.appendChild(el("p", "q", block.title || "Đồng hồ bấm giờ"));
    var label = el("label", null, "Số phút: ");
    var num = document.createElement("input");
    num.type = "number";
    num.min = "1";
    num.max = "15";
    num.value = "5";
    num.style.width = "4rem";
    label.appendChild(num);
    box.appendChild(label);
    var disp = el("div", "timer", "05:00");
    disp.setAttribute("aria-live", "polite");
    box.appendChild(disp);
    var row = el("div", "row");
    var start = el("button", "btn-brush", "Bắt đầu");
    start.type = "button";
    var stop = el("button", "btn-brush ghost", "Dừng");
    stop.type = "button";
    var reset = el("button", "btn-brush ghost", "Đặt lại");
    reset.type = "button";
    var total = 5 * 60, left = total, timer = null;
    function fmt(s) {
      var m = Math.floor(s / 60), ss = s % 60;
      return (m < 10 ? "0" + m : "" + m) + ":" + (ss < 10 ? "0" + ss : "" + ss);
    }
    function tick() {
      left--;
      if (left <= 0) {
        left = 0;
        clearInterval(timer);
        timer = null;
        start.textContent = "Bắt đầu";
        disp.textContent = "Hết giờ";
        return;
      }
      disp.textContent = fmt(left);
    }
    start.addEventListener("click", function () {
      if (timer) return;
      total = Math.max(1, Math.min(15, Number(num.value) || 5)) * 60;
      if (left <= 0 || left > total || disp.textContent === "05:00" || disp.textContent === "Hết giờ") left = total;
      disp.textContent = fmt(left);
      timer = setInterval(tick, 1000);
      start.textContent = "Đang chạy...";
    });
    stop.addEventListener("click", function () {
      if (timer) { clearInterval(timer); timer = null; start.textContent = "Tiếp tục"; }
    });
    reset.addEventListener("click", function () {
      if (timer) { clearInterval(timer); timer = null; }
      total = Math.max(1, Math.min(15, Number(num.value) || 5)) * 60;
      left = total;
      disp.textContent = fmt(left);
      start.textContent = "Bắt đầu";
    });
    num.addEventListener("change", function () {
      total = Math.max(1, Math.min(15, Number(num.value) || 5)) * 60;
      left = total;
      disp.textContent = fmt(left);
    });
    row.appendChild(start);
    row.appendChild(stop);
    row.appendChild(reset);
    box.appendChild(row);
    return box;
  }

  function renderReviewTable(block) {
    var box = el("div", "qa");
    box.appendChild(el("p", "q", block.title || "Tự đánh giá"));
    var key = "review-" + block.id;
    var saved = window.Store.get(key, {});
    var table = el("table", "fill review");
    var hr = document.createElement("tr");
    hr.appendChild(el("th", null, "Tiêu chí"));
    hr.appendChild(el("th", null, "Đạt"));
    hr.appendChild(el("th", null, "Chưa đạt"));
    table.appendChild(hr);
    (block.criteria || []).forEach(function (c, i) {
      var tr = document.createElement("tr");
      tr.appendChild(el("td", null, c));
      ["dat", "chuadat"].forEach(function (val, vi) {
        var td = document.createElement("td");
        var r = document.createElement("input");
        r.type = "radio";
        r.name = block.id + "-" + i;
        r.value = val;
        r.checked = saved[i] === val;
        r.setAttribute("aria-label", c + ": " + (vi === 0 ? "Đạt" : "Chưa đạt"));
        r.addEventListener("change", function () {
          saved[i] = val;
          window.Store.set(key, saved);
        });
        td.appendChild(r);
        tr.appendChild(td);
      });
      table.appendChild(tr);
    });
    box.appendChild(table);
    return box;
  }

  function renderImg(block) {
    var box = el("div", "img-slot");
    var meta = (window.IMAGES && window.IMAGES[block.file]) || {};
    var ph = el("div", null, null);
    // ph.appendChild(el("div", "ph-brief", meta.brief || "Minh hoạ cho bài học. Mở IMAGES_NEEDED.md để xem mô tả ảnh cần tìm."));
    // Add Source line under each image — user will replace the link
    var sourceAnchor = el("a", "ph-source", "Nguồn");
    sourceAnchor.href = (window.IMAGES[block.file] && window.IMAGES[block.file].sourceUrl) || "https://example.com";
    sourceAnchor.target = "_blank";
    sourceAnchor.rel = "noopener noreferrer";
    ph.appendChild(sourceAnchor);
    box.appendChild(ph);
    var img = new Image();
    // No loading="lazy" here: this Image is detached until onload fires, and a
    // detached lazy image never starts loading (load never fires, the box would
    // stay a placeholder forever). Eager is fine — six small local files.
    img.alt = meta.alt || block.file;
    img.onload = function () {
      img.style.maxWidth = "100%";
      img.style.height = "auto";
      box.insertBefore(img, ph);
      // Keep ph visible so the Source line remains under the image
    };
    img.src = "images/" + block.file;
    return box;
  }

  window.Activities = {
    renderQa: renderQa,
    renderChecklist: renderChecklist,
    renderTableFill: renderTableFill,
    renderWrite150: renderWrite150,
    renderBuilder: renderBuilder,
    renderSpeechTools: renderSpeechTools,
    renderReviewTable: renderReviewTable,
    renderImg: renderImg
  };
})();
