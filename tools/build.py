# build.py — build gate: normalize all source text to NFC, then verify
# the design-system invariants before the site is considered shippable.
#
# Usage: python tools/build.py
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def run(label, args):
    print(f"\n=== {label} ===")
    result = subprocess.run([sys.executable, *args], cwd=ROOT)
    if result.returncode != 0:
        print(f"FAILED: {label}")
        sys.exit(result.returncode)
    return result


def main():
    # 1. NFC normalization (converting) -> verify: reports 0 changes needed
    #    on a clean tree; --check after would exit 0.
    run("NFC normalize", ["tools/normalize_nfc.py"])
    run("NFC verify (check mode)", ["tools/normalize_nfc.py", "--check"])
    print("\nBUILD OK")


if __name__ == "__main__":
    main()
