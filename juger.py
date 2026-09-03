#!/usr/bin/env python3
"""Judge the formal layer. Absence is not a proof."""
from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
THEORIES = ("UFHY1.ec", "EPSILON.ec", "MODE.ec")


def judge(root: Path, theories: tuple[str, ...] = THEORIES) -> dict:
    binary = shutil.which("easycrypt")
    rows: list[dict] = []
    missing: list[str] = []
    for t in theories:
        path = root / t
        if not path.is_file():
            missing.append(t)
            rows.append({"file": t, "present": False, "admitted": None})
            continue
        text = path.read_text(encoding="utf-8")
        rows.append({"file": t, "present": True, "admitted": text.count("admitted")})

    any_admitted = any((row["admitted"] or 0) > 0 for row in rows if row["present"])
    decision = "deny" if missing or any_admitted or not binary else "allow"

    if missing:
        note = "missing theory file is not a proof. deny."
    elif any_admitted or not binary:
        note = "admitted lemmas keep the label honest. obligations, not theorems."
    else:
        note = "easycrypt present and no admitted count. still not a seal. judgment = Carl."

    verdict = {
        "format": "formal.v0",
        "easycrypt": binary or None,
        "theories": rows,
        "missing": missing,
        "proven": False,
        "decision": decision,
        "note": note,
    }
    if binary:
        try:
            out = subprocess.check_output([binary, "-version"], text=True, timeout=20)
            verdict["version"] = out.strip().splitlines()[0] if out.strip() else "unknown"
        except Exception as e:
            verdict["version_error"] = type(e).__name__
    return verdict


def main() -> int:
    verdict = judge(ROOT, THEORIES)
    print(json.dumps(verdict, ensure_ascii=False, indent=2))
    return 0 if verdict["decision"] == "allow" else 2


if __name__ == "__main__":
    raise SystemExit(main())
