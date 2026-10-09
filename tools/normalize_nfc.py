# normalize_nfc.py — NFC-normalize Vietnamese text so stacked diacritics
# render as precomposed glyphs (detached tone marks come from NFD text
# hitting fonts without decomposed forms).
#
# Usage:
#   python tools/normalize_nfc.py           # convert, report changed files/strings
#   python tools/normalize_nfc.py --check   # exit 1 if any file needs conversion
#
# Reads bytes and decodes UTF-8 (preserves CRLF line endings on Windows).
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXTS = {".html", ".js", ".css", ".md", ".json", ".txt", ".py"}
SKIP_DIRS = {"fonts", ".git", "node_modules", ".claude"}


def iter_files():
    for p in sorted(ROOT.rglob("*")):
        if not p.is_file() or p.suffix.lower() not in EXTS:
            continue
        if any(part in SKIP_DIRS for part in p.relative_to(ROOT).parts):
            continue
        yield p


def main():
    check_only = "--check" in sys.argv
    changed_files = 0
    changed_strings = 0

    for p in iter_files():
        raw = p.read_bytes()
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            print(f"SKIP (not utf-8): {p.relative_to(ROOT)}")
            continue

        # Normalize line endings back after unicodedata (it does not touch \r\n,
        # but normalize() on str keeps them; no re-encode surprises).
        norm = unicodedata.normalize("NFC", text)
        if norm == text:
            continue

        # Report which strings changed (line-level, first difference per line).
        lines_old = text.split("\n")
        lines_new = norm.split("\n")
        diffs = [
            (i + 1, o, n)
            for i, (o, n) in enumerate(zip(lines_old, lines_new))
            if o != n
        ]
        changed_files += 1
        changed_strings += len(diffs)
        print(f"{'NEEDS' if check_only else 'FIXED'}: {p.relative_to(ROOT)}")
        for lineno, o, n in diffs:
            print(f"  line {lineno}:")
            print(f"    before: {o.strip()!r}")
            print(f"    after:  {n.strip()!r}")

        if not check_only:
            p.write_bytes(norm.encode("utf-8"))

    print(f"\n{changed_files} file(s), {changed_strings} string line(s) "
          f"{'need' if check_only else 'changed'} NFC normalization.")
    if check_only and changed_files:
        sys.exit(1)


if __name__ == "__main__":
    main()
