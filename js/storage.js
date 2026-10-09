window.Store = (function () {
  var mem = {};
  var ok = true;
  try {
    var k = "__bai1_test__";
    window.localStorage.setItem(k, "1");
    window.localStorage.removeItem(k);
  } catch (e) { ok = false; }
  function get(key, fallback) {
    try {
      if (!ok) return (key in mem) ? mem[key] : fallback;
      var raw = window.localStorage.getItem("bai1-" + key);
      if (raw === null || raw === undefined) return fallback;
      return JSON.parse(raw);
    } catch (e) {
      return (key in mem) ? mem[key] : fallback;
    }
  }
  function set(key, val) {
    mem[key] = val;
    try {
      if (!ok) return;
      window.localStorage.setItem("bai1-" + key, JSON.stringify(val));
    } catch (e) { /* localStorage disabled: memory only */ }
  }
  return { get: get, set: set, persistent: function () { return ok; } };
})();
