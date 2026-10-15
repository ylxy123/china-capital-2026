"""Verify the published manuscript/PDF against their recorded SHA-256 hashes."""
# SPDX-License-Identifier: MIT
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]

def main():
    record = json.loads((ROOT / "research/deliverable_sha256.json").read_text(encoding="utf-8"))
    failures = []
    for name, expected in record["files"].items():
        actual = hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
        if actual != expected:
            failures.append(name)
        print(f"{'OK' if actual == expected else 'MISMATCH'} {name}: {actual}")
    if failures:
        raise SystemExit("Published snapshot differs: " + ", ".join(failures))

if __name__ == "__main__":
    main()
