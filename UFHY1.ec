(* UFHY1 — AND-combiner of two EUF-CMA signatures.
   Ed25519 /\ ML-DSA-65.
   Today both must verify. The hypothesis is future survival.
   STATUS: admitted. Not a theorem. *)

require import AllCore Bool.

type pkey_ed, skey_ed, sig_ed.
type pkey_ml, skey_ml, sig_ml.
type msg.

op ed_kg : pkey_ed * skey_ed.
op ed_sign : skey_ed -> msg -> sig_ed.
op ed_verify : pkey_ed -> msg -> sig_ed -> bool.

op ml_kg : pkey_ml * skey_ml.
op ml_sign : skey_ml -> msg -> sig_ml.
op ml_verify : pkey_ml -> msg -> sig_ml -> bool.

axiom ed_correct :
  forall m, ed_verify (fst ed_kg) m (ed_sign (snd ed_kg) m) = true.

axiom ml_correct :
  forall m, ml_verify (fst ml_kg) m (ml_sign (snd ml_kg) m) = true.

op ufhy1_verify
  (pk_ed : pkey_ed) (pk_ml : pkey_ml)
  (m : msg) (s_ed : sig_ed) (s_ml : sig_ml) : bool =
  ed_verify pk_ed m s_ed && ml_verify pk_ml m s_ml.

lemma ufhy1_correct :
  forall m,
    ufhy1_verify
      (fst ed_kg) (fst ml_kg) m
      (ed_sign (snd ed_kg) m)
      (ml_sign (snd ml_kg) m)
    = true.
proof.
  admitted.
qed.

axiom euf_cma_ed : true.
axiom euf_cma_ml : true.

lemma ufhy1_euf_cma : euf_cma_ed \/ euf_cma_ml => true.
proof.
  admitted.
qed.
