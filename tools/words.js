// ASCII-only console output. Usage: node tools/words.js "<plan.match regex>"
// Writes tools/_words.txt (UTF-8) listing every item word with its index, so
// plan.json ranges can be chosen by READING THE FILE, never the console.
const fs = require("fs");
const match = process.argv[2];
if (!match) { console.log("usage: node tools/words.js \"Ph.n 1: Cu.c tr\""); process.exit(1); }
const src = fs.readFileSync("content/content-doc.js", "utf8");
const re = new RegExp(
  '( *)\\{type: "p", source: "outline", text: ("' + match + '[^"\\r\\n]*")\\},?\\r?\\n' +
  ' *\\{type: "list"[^\\r\\n]*\\r?\\n((?: *"[^\\r\\n]*\\r?\\n)+) *\\]\\},?(\\r?\\n)', "g");
const hits = [...src.matchAll(re)];
if (hits.length !== 1) { console.log("ABORT: expected 1 match, got " + hits.length); process.exit(1); }
const text = JSON.parse(hits[0][2]);
const items = hits[0][3].split(/\r?\n/).filter(Boolean).map(l => JSON.parse(l.trim().replace(/,$/, "")));
let out = "HEADING: " + text + "\n\n";
items.forEach((it, i) => {
  const w = it.split(/\s+/);
  out += "ITEM " + i + " (" + w.length + " words, last index " + (w.length - 1) + ")\n";
  out += w.map((x, j) => j + ":" + x).join("  ") + "\n\n";
});
fs.writeFileSync("tools/_words.txt", out, "utf8");
console.log("OK: " + items.length + " items -> tools/_words.txt (read it with the Read tool)");
