#!/usr/bin/env python3
"""Judge the formal layer. Absence is not a proof."""
from __future__ import annotations
import json, shutil, subprocess
from pathlib import Path
ROOT = Path(__file__).resolve().parent
THEORIES = ("UFHY1.ec", "EPSILON.ec", "MODE.ec")

def main() -> int:
    binary = shutil.which("easycrypt")
    admitted = []
    for t in THEORIES:
        text = (ROOT / t).read_text(encoding="utf-8")
        admitted.append({"file": t, "admitted": text.count("admitted")})
    verdict = {
        "format": "formal.v0",
        "easycrypt": binary or None,
        "theories": admitted,
        "proven": False,
        "decision": "deny" if any(x["admitted"] for x in admitted) or not binary else "allow",
        "note": "admitted lemmas keep the label honest. not formally verified.",
    }
    if binary:
        try:
            out = subprocess.check_output([binary, "-version"], text=True, timeout=20)
            verdict["version"] = out.strip().splitlines()[0] if out.strip() else "unknown"
        except Exception as e:
            verdict["version_error"] = type(e).__name__
    print(json.dumps(verdict, ensure_ascii=False, indent=2))
    return 0 if verdict["decision"] == "allow" else 2

if __name__ == "__main__":
    raise SystemExit(main())
