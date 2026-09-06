#!/usr/bin/env python3
"""Honesty tests for the public door. Not an EasyCrypt check."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
THEORIES = ("UFHY1.ec", "EPSILON.ec", "MODE.ec")
FORBIDDEN = "formally verified"


def _fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def test_theories_on_disk() -> None:
    makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
    if "THEORIES = UFHY1.ec EPSILON.ec MODE.ec" not in makefile:
        _fail("Makefile THEORIES does not match the three named files")
    for name in THEORIES:
        path = ROOT / name
        if not path.is_file():
            _fail(f"missing theory file {name}")
        text = path.read_text(encoding="utf-8")
        if "admitted" not in text:
            _fail(f"{name} has no admitted obligation")


def test_juger_json_unproven() -> None:
    proc = subprocess.run(
        [sys.executable, str(ROOT / "juger.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode != 2:
        _fail(f"juger.py exit {proc.returncode}, expected 2 (deny)")
    try:
        verdict = json.loads(proc.stdout)
    except json.JSONDecodeError as e:
        _fail(f"juger.py stdout is not JSON: {e}")
    if verdict.get("format") != "formal.v0":
        _fail(f"format {verdict.get('format')!r}, expected formal.v0")
    if verdict.get("proven") is not False:
        _fail("juger JSON proven must be false")
    if verdict.get("decision") != "deny":
        _fail(f"decision {verdict.get('decision')!r}, expected deny")
    present = {row["file"] for row in verdict.get("theories", []) if row.get("present")}
    if present != set(THEORIES):
        _fail(f"juger present theories {present}, expected {set(THEORIES)}")


def test_missing_theory_denies_without_crash() -> None:
    sys.path.insert(0, str(ROOT))
    import juger

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        shutil.copy(ROOT / "UFHY1.ec", root / "UFHY1.ec")
        try:
            verdict = juger.judge(root, THEORIES)
        except Exception as e:
            _fail(f"missing theory must deny, not raise {type(e).__name__}: {e}")
    if verdict.get("format") != "formal.v0":
        _fail("missing-file verdict must keep format formal.v0")
    if verdict.get("proven") is not False:
        _fail("missing theory must set proven false")
    if verdict.get("decision") != "deny":
        _fail("missing theory must deny")
    missing = set(verdict.get("missing") or [])
    if "EPSILON.ec" not in missing or "MODE.ec" not in missing:
        _fail(f"expected EPSILON.ec and MODE.ec missing, got {missing}")


def test_epsilon_zero_refused_in_source() -> None:
    text = (ROOT / "EPSILON.ec").read_text(encoding="utf-8")
    if "ε = 0 refused" not in text and "eps_refused_zero" not in text:
        _fail("EPSILON.ec must refuse ε = 0 in source")
    if "0%r < eps" not in text:
        _fail("EPSILON.ec must state 0%r < eps")
    if "leftover_hash" not in text or "hmin" not in text:
        _fail("EPSILON.ec must name leftover-hash and hmin")
    if "0%r = eps" in text or "eps = 0%r => true" in text:
        _fail("EPSILON.ec must not treat ε = 0 as a bound")


def test_copy_forbids_formally_verified() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    interdit = (ROOT / "INTERDIT.md").read_text(encoding="utf-8")
    schema = (ROOT / "SCHEMA.md").read_text(encoding="utf-8")
    if FORBIDDEN not in readme:
        _fail("README.md must still name and forbid « formally verified »")
    if "Do not write" not in readme:
        _fail("README.md must forbid writing « formally verified »")
    if "obligations only" not in readme:
        _fail("README.md must state obligations only")
    if "product claim" not in readme:
        _fail("README.md must forbid « formally verified » as a product claim")
    if "while a lemma is admitted" in readme:
        _fail("README.md must not limit the ban to admitted lemmas")
    if FORBIDDEN not in interdit:
        _fail("INTERDIT.md must still forbid « formally verified »")
    if "product claim" not in interdit:
        _fail("INTERDIT.md must forbid the phrase as a product claim")
    if "while a lemma is admitted" in interdit or "while a lemma is `admitted`" in interdit:
        _fail("INTERDIT.md must not limit the ban to admitted lemmas")
    if "obligations only" not in interdit:
        _fail("INTERDIT.md must state obligations only")
    if "Obligations only" not in schema:
        _fail("SCHEMA.md must state obligations only")


def test_product_files_do_not_claim_verified() -> None:
    """Name the interdiction in the door copy. Never assert it as fact."""
    may_name = {"README.md", "INTERDIT.md", "test_door.py"}
    phrases = ("formally verified", "formal verification")
    claimed = (
        "is formally verified",
        "are formally verified",
        "has been formally verified",
        "was formally verified",
    )
    for path in sorted(p for p in ROOT.iterdir() if p.is_file()):
        if path.name in {"LICENSE"} or path.name.startswith("."):
            continue
        text = path.read_text(encoding="utf-8")
        lower = text.lower()
        if path.name not in may_name:
            for phrase in phrases:
                if phrase in lower:
                    _fail(f"{path.name} must not contain {phrase!r}")
        if path.name != "test_door.py":
            for needle in claimed:
                if needle in lower:
                    _fail(f"{path.name} must not claim {needle!r}")
    juger_src = (ROOT / "juger.py").read_text(encoding="utf-8")
    if '"proven": False' not in juger_src:
        _fail("juger.py must keep proven False in source")
    if '"proven": True' in juger_src or '"proven": true' in juger_src:
        _fail("juger.py must never set proven true")


def main() -> int:
    test_theories_on_disk()
    test_juger_json_unproven()
    test_missing_theory_denies_without_crash()
    test_epsilon_zero_refused_in_source()
    test_copy_forbids_formally_verified()
    test_product_files_do_not_claim_verified()
    print("door tests: ok — files exist, proven false, ε=0 refused, obligations only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
