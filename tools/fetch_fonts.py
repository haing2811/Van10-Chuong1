# tools/fetch_fonts.py — download self-hosted woff2 subsets from Google Fonts
# and emit the @font-face block for thu-quan-tokens.css.
# Run: python tools/fetch_fonts.py
import os, re, sys, urllib.request

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "css", "fonts")
SUBSETS = ("vietnamese", "latin-ext", "latin")

FAMILIES = [
    ("Be Vietnam Pro", "BeVietnamPro", "wght@400;500;700"),
    ("Noto Serif", "NotoSerif", "wght@400;600;700"),
    ("Playfair Display", "PlayfairDisplay", "wght@600;700"),
]


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def parse_faces(css_text):
    """Yield dicts: subset, family, weight, url, unicode_range, style."""
    text = css_text.decode("utf-8")
    faces = []
    # blocks look like:  /* vietnamese */\n@font-face { ... }
    for m in re.finditer(r"/\*\s*([a-z-]+)\s*\*/\s*@font-face\s*\{(.*?)\}", text, re.S):
        subset, body = m.group(1), m.group(2)
        def grab(pat):
            mm = re.search(pat, body)
            return mm.group(1).strip() if mm else ""
        faces.append({
            "subset": subset,
            "family": grab(r"font-family:\s*'([^']+)'"),
            "weight": grab(r"font-weight:\s*([\d\s]+);"),
            "style": grab(r"font-style:\s*(\w+)"),
            "url": grab(r"src:\s*url\(([^)]+)\)"),
            "unicode_range": grab(r"unicode-range:\s*([^;]+);"),
        })
    return faces


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    kept = []
    for family, slug, axes in FAMILIES:
        url = f"https://fonts.googleapis.com/css2?family={family.replace(' ', '+')}:{axes}&display=swap"
        css = fetch(url)
        for f in parse_faces(css):
            if f["subset"] not in SUBSETS or f["style"] != "normal":
                continue
            weight = f["weight"].split()[0]
            name = f"{slug}-{weight}-{f['subset']}.woff2"
            path = os.path.join(OUT_DIR, name)
            data = fetch(f["url"])
            with open(path, "wb") as fh:
                fh.write(data)
            kept.append({**f, "weight": weight, "file": name, "bytes": len(data)})
            print(f"  {name:44s} {len(data):>7d} bytes")

    # Emit @font-face rules, Vietnamese subset first so its range wins overlaps.
    lines = ["/* Self-hosted fonts (tools/fetch_fonts.py). Vietnamese + Latin subsets.",
             "   Do not edit by hand — rerun the script to refresh. */", ""]
    order = {s: i for i, s in enumerate(("vietnamese", "latin-ext", "latin"))}
    kept.sort(key=lambda f: (f["family"], f["weight"], order[f["subset"]]))
    for f in kept:
        lines += [
            "@font-face {",
            f"  font-family: \"{f['family']}\";",
            f"  font-style: normal;",
            f"  font-weight: {f['weight']};",
            "  font-display: swap;",
            f"  src: url('fonts/{f['file']}') format('woff2');",
            f"  unicode-range: {f['unicode_range']};",
            "}",
        ]
    out = os.path.join(os.path.dirname(__file__), "font-faces.css")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print(f"\n{len(kept)} files downloaded; @font-face block -> tools/font-faces.css")


if __name__ == "__main__":
    main()
