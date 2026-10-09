# glyph_test.py — verify each family+weight can render the full Vietnamese
# test string across its three self-hosted subsets (the browser unions
# vietnamese + latin-ext + latin via unicode-range, so we do too).
#
# Run: python tools/glyph_test.py   (exit 1 if any face fails)
# Output uses only ASCII (U+XXXX codepoints) so any console can show it.
from pathlib import Path
import sys

from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "css" / "fonts"

# NFC precomposed Vietnamese with stacked tone marks, plus the bare
# vowel/consonant bases that carry them.
TEST = "ầếềấểờỗựậịọớợồổỹẽđĐĂÂÊÔƠƯ"
FACES = [
    ("BeVietnamPro", [400, 500, 700]),
    ("NotoSerif", [400, 600, 700]),
    ("PlayfairDisplay", [600, 700]),
]


def main():
    failures = 0
    for slug, weights in FACES:
        for w in weights:
            cmap = {}
            files = sorted(FONTS.glob(f"{slug}-{w}-*.woff2"))
            if not files:
                failures += 1
                print(f"  FAIL {slug}-{w}: no woff2 files found")
                continue
            for p in files:
                cmap.update(TTFont(str(p)).getBestCmap())
            missing = [f"U+{ord(c):04X}" for c in TEST if ord(c) not in cmap]
            if missing:
                failures += 1
                print(f"  FAIL {slug}-{w}: missing {', '.join(missing)}")
            else:
                print(f"  OK   {slug}-{w}: all {len(TEST)} codepoints "
                      f"in union of {len(files)} subsets")
    print()
    if failures:
        print(f"{failures} face(s) FAILED the Vietnamese glyph test")
        sys.exit(1)
    print("All faces pass: full Vietnamese test string renderable.")


if __name__ == "__main__":
    main()
