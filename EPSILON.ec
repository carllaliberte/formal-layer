(* EPSILON — leftover-hash extractor bound for declared Hmin and ε.
   ε = 0 refused. Zero margin is not a bound.
   Missing ε is not zero ε. Worker 400 EPSILON_MISSING / sdk classique /
   GARDE fail-closed is a consumer split, not a theorem here.
   STATUS: admitted. Not a theorem. *)

require import AllCore Real.

op hmin : real.
op eps : real.

axiom hmin_declared : 0%r <= hmin.

(* ε = 0 refused. Zero margin is not a bound. *)
axiom eps_refused_zero : 0%r < eps.

op leftover_hash_holds : real -> real -> bool.

lemma leftover_hash_bound :
  leftover_hash_holds hmin eps = true.
proof.
  admitted.
qed.

lemma eps_zero_is_not_a_bound :
  leftover_hash_holds hmin 0%r = false.
proof.
  admitted.
qed.
