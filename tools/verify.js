// ASCII-only output. Usage: node tools/verify.js
const fs = require("fs");
const vm = require("vm");
let ok = true;
const fail = (m) => { ok = false; console.log("FAIL: " + m); };
const src = fs.readFileSync("content/content-doc.js", "utf8");
const sandbox = { window: {} };
try { vm.runInNewContext(src, sandbox); console.log("PASS: file parses"); } catch (e) { fail("parse error " + e.message); }
let originals = JSON.parse(fs.readFileSync("tools/_original_items.json", "utf8"));
if (Array.isArray(originals)) originals = {};
const found = [];
(function walk(x) {
  if (Array.isArray(x)) x.forEach(walk);
  else if (x && typeof x === "object") { if (x.condensed && x.bullets) found.push(x); Object.values(x).forEach(walk); }
})(sandbox.window.CONTENT);
console.log("condensed blocks: " + found.length);
const norm = (w) => w.toLowerCase().replace(/[.,;:!?"]/g, "");
found.forEach((b, k) => {
  const orig = originals[b.text];
  if (!orig) { fail("block " + k + ": no saved original for heading " + JSON.stringify(b.text.slice(0, 12))); return; }
  if (b.detail !== orig.join("\n")) fail("block " + k + ": detail differs from original");
  else console.log("PASS: detail byte-identical");
  const pool = new Set(b.detail.split(/\s+/).map(norm));
  b.bullets.forEach((s, i) => {
    const w = s.split(/\s+/);
    if (w.length > 20) fail("bullet " + i + " has " + w.length + " words");
    w.forEach(x => { if (!pool.has(norm(x))) fail("bullet " + i + " word not in original: " + x.length + " chars"); });
  });
  console.log("PASS: " + b.bullets.length + " bullets checked (<=20 words, all words from original)");
});
if (/[θΘ]/.test(src)) fail("Greek theta found in file");
console.log(ok ? "ALL OK" : "PROBLEMS FOUND");
process.exit(ok ? 0 : 1);