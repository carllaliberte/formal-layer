(* MODE — quantique is reachable only if every physical gate holds.
   os is phone entropy = classique.
   A mode obligation, not a photon and not a seal.
   STATUS: admitted. Not a theorem. *)

require import AllCore Bool.

type quelle.
type carte.
type mode.

op os : quelle.
op qrng : quelle.
op qkd : quelle.

op classique : mode.
op quantique : mode.

op source : carte -> quelle.

op gate_quelle : carte -> bool.
op gate_temoin : carte -> bool.
op gate_epsilon : carte -> bool.
op gate_horizon : carte -> bool.

op gates (c : carte) : bool =
  gate_quelle c && gate_temoin c && gate_epsilon c && gate_horizon c.

op collapse : carte -> mode.

axiom os_is_classique :
  forall (c : carte), source c = os => collapse c = classique.

lemma quantique_only_if_every_gate :
  forall (c : carte),
    collapse c = quantique => gates c = true.
proof.
  admitted.
qed.
