# FAMILLE formal layer — EasyCrypt

This repository is the deployable EasyCrypt project for FAMILLE.
It is **not** a machine-checked proof.

Status of every lemma: `admitted`, unless a later commit replaces
the admission with a checked script and a CI log.

Do not write « formally verified » while a lemma is admitted.

## Claims (obligations)

| File | Claim | Status |
|---|---|
| `UFHY1.ec` | AND-combiner of EUF-CMA signatures is EUF-CMA if at least one component is | admitted |
| `EPSILON.ec` | leftover-hash extractor bound for declared Hmin and ε; ε = 0 refused | admitted |
| `MODE.ec` | `quantique` is reachable only if every physical gate holds | admitted |

## Run

```
eval $(opam env)
easycrypt -I . UFHY1.ec
easycrypt -I . EPSILON.ec
easycrypt -I . MODE.ec
python3 juger.py
```

A missing `easycrypt` binary keeps the label honest: the theories
are the specification. They are not theorems until the prover says so.

See [INTERDIT.md](INTERDIT.md).

Après pointe juge.v0 sur quelle : `os` n'est pas quantique. Le formal layer
ne change pas de statut admitted.
