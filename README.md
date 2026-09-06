# FAMILLE formal layer — EasyCrypt

This repository is the public door for the FAMILLE EasyCrypt layer.
It names obligations. It does not close them.

Judgment = Carl. Preview of a claim is not a proof.

Status of every lemma: `admitted`, unless a later commit replaces
the admission with a checked script and a CI log.

This layer carries obligations only. Do not write « formally verified » as a product claim. Formal verification is not a fact this door asserts.

## Claims (obligations)

| File | Claim | Status |
|---|---|
| `UFHY1.ec` | AND-combiner of EUF-CMA signatures is EUF-CMA if at least one component is | admitted |
| `EPSILON.ec` | leftover-hash extractor bound for declared Hmin and ε; ε = 0 refused | admitted |
| `MODE.ec` | `quantique` is reachable only if every physical gate holds | admitted |

Makefile: `THEORIES = UFHY1.ec EPSILON.ec MODE.ec`. Those three files must exist on disk. A cited name that is not on disk is a 404, not a proof.

## Admitted vs theorem

An `admitted` lemma is a named obligation. It is not a theorem.
A theorem would be a script EasyCrypt closes, plus a CI log of that check.
There is no such log in this repository.

## Verified vs assumed

Nothing here is checked by a prover.
Ops and axioms are assumed names. Lemmas stay `admitted`.
A missing `easycrypt` binary keeps that label honest.
A missing theory file is not a proof: `python3 juger.py` prints
`format: formal.v0` with `proven: false` and `decision: deny`.

ε = 0 is refused in `EPSILON.ec`. Zero margin is not a bound.
Missing ε is not zero ε — that split belongs to consumers, not this theory.
`os` is phone entropy = classique. `quantique` is a mode, not a photon.

## Run

```
python3 juger.py
make admitted
python3 test_door.py
```

Optional, if the binary is installed:

```
eval $(opam env)
make check
```

`make check` exits 2 when `easycrypt` is absent. That is honest, not a pass.

See [INTERDIT.md](INTERDIT.md).

After [famille juge.v0](https://github.com/carllaliberte/famille/blob/main/schema/juge.v0.json), `quelle: os` is classique, not quantique. This layer stays `admitted`.
