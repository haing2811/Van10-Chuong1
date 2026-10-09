(function () {
  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text !== undefined && text !== null) n.textContent = text;
    return n;
  }
  function renderQuiz(block) {
    var wrap = el("div", "quiz");
    var title = el("p", null, null);
    var strong = el("strong", null, block.title || "Tự kiểm tra");
    title.appendChild(strong);
    wrap.appendChild(title);
    var form = document.createElement("form");
    form.noValidate = true;
    var stateKey = "quiz-" + block.id;
    var saved = window.Store.get(stateKey, {});
    var qObjs = block.questions || [];
    qObjs.forEach(function (qq, qi) {
      var fs = document.createElement("fieldset");
      var lg = document.createElement("legend");
      lg.textContent = (qi + 1) + ". " + qq.q;
      fs.appendChild(lg);
      qq.options.forEach(function (opt, oi) {
        var lab = el("label", "opt");
        var radio = document.createElement("input");
        radio.type = "radio";
        radio.name = block.id + "-" + qi;
        radio.value = String(oi);
        if (saved && saved[qi] === oi) radio.checked = true;
        radio.addEventListener("change", function () {
          saved[qi] = oi;
          window.Store.set(stateKey, saved);
        });
        lab.appendChild(radio);
        lab.appendChild(document.createTextNode(opt));
        fs.appendChild(lab);
      });
      var fb = el("div", "fb");
      fb.id = block.id + "-fb-" + qi;
      fs.appendChild(fb);
      form.appendChild(fs);
    });
    var row = el("div", "row");
    var btn = el("button", "btn-brush", "Chấm điểm");
    btn.type = "button";
    var score = el("span", "score");
    var savedScore = window.Store.get(stateKey + "-score", null);
    if (savedScore !== null) score.textContent = "Đã lưu: " + savedScore + "/" + qObjs.length;
    btn.addEventListener("click", function () {
      var correct = 0;
      qObjs.forEach(function (qq, qi) {
        var fb = form.querySelector("#" + CSS.escape(block.id + "-fb-" + qi));
        var picked = saved[qi];
        if (picked === undefined || picked === null) {
          fb.textContent = "Chưa chọn đáp án.";
          fb.className = "fb no";
          return;
        }
        if (Number(picked) === Number(qq.answer)) {
          correct++;
          fb.textContent = "Đúng. " + (qq.explain || "");
          fb.className = "fb ok";
        } else {
          fb.textContent = "Chưa đúng. " + (qq.explain || "");
          fb.className = "fb no";
        }
      });
      score.textContent = "Kết quả: " + correct + "/" + qObjs.length;
      window.Store.set(stateKey + "-score", correct);
    });
    var reset = el("button", "btn-brush ghost", "Làm lại");
    reset.type = "button";
    reset.addEventListener("click", function () {
      saved = {};
      window.Store.set(stateKey, {});
      form.querySelectorAll('input[type="radio"]').forEach(function (r) { r.checked = false; });
      form.querySelectorAll(".fb").forEach(function (f) { f.textContent = ""; });
      score.textContent = "";
    });
    row.appendChild(btn);
    row.appendChild(reset);
    row.appendChild(score);
    form.appendChild(row);
    wrap.appendChild(form);
    return wrap;
  }
  window.Quiz = { render: renderQuiz };
})();
