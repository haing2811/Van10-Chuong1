// ASCII-only. Usage (from project folder): node tools/build.js
// Reads tools/plan.json: numeric [item, firstWord, lastWord] ranges only.
const fs = require("fs");
const plan = JSON.parse(fs.readFileSync("tools/plan.json", "utf8"));
const file = "content/content-doc.js";
const src = fs.readFileSync(file, "utf8");
const eol = src.includes("\r\n") ? "\r\n" : "\n";
const re = new RegExp(
  '( *)\\{type: "p", source: "outline", text: ("' + plan.match + '[^"\\r\\n]*")\\},?\\r?\\n' +
  ' *\\{type: "list"[^\\r\\n]*\\r?\\n((?: *"[^\\r\\n]*\\r?\\n)+) *\\]\\},?(\\r?\\n)', "g");
const hits = [...src.matchAll(re)];
if (hits.length !== 1) { console.log("ABORT: expected 1 match, got " + hits.length); process.exit(1); }
const m = hits[0];
const indent = m[1];
const text = JSON.parse(m[2]);
const items = m[3].split(/\r?\n/).filter(Boolean).map(l => JSON.parse(l.trim().replace(/,$/, "")));
const bullets = plan.bullets.map(parts => {
  let s = parts.map(([i, a, b]) => items[i].split(/\s+/).slice(a, b + 1).join(" ")).join(" ");
  s = s.replace(/[,;:]+$/, "");
  s = s.charAt(0).toUpperCase() + s.slice(1);
  if (!/[.!?"]$/.test(s)) s += ".";
  return s;
});
const detail = items.join("\n");
const block = indent + "{type: \"p\", source: \"outline\", text: " + JSON.stringify(text) + "," + eol +
  indent + "  bullets: [" + eol + bullets.map(b => indent + "    " + JSON.stringify(b)).join("," + eol) + eol + indent + "  ]," + eol +
  indent + "  detail: " + JSON.stringify(detail) + "," + eol +
  indent + "  condensed: true}," + m[4];
fs.writeFileSync(file, src.slice(0, m.index) + block + src.slice(m.index + m[0].length), "utf8");
const origFile = "tools/_original_items.json";
let originals = {};
try { originals = JSON.parse(fs.readFileSync(origFile, "utf8")); } catch (e) {}
if (Array.isArray(originals)) originals = {}; // old single-list format
originals[text] = items;
fs.writeFileSync(origFile, JSON.stringify(originals), "utf8");
console.log("OK: wrote " + bullets.length + " bullets; items=" + items.length);