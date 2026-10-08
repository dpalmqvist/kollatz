import Erdos1135.KrasikovLagarias.K18PredecessorAllTargets9032

/-!
# A certified (Palmqvist k = 18 certificate, gamma = 9032/10000) x^0.903 Collatz predecessor lower bound

This module provides short public names for the principal checked results.
The definitions are aliases of the exact definitions used by the proof.
-/

namespace CollatzPredecessor0903

open Filter

abbrev accelerated := Erdos1135.Terras.accelerated
abbrev Reaches := Erdos1135.KrasikovLagarias.Reaches
noncomputable abbrev predecessorCount :=
  Erdos1135.KrasikovLagarias.predecessorCount
noncomputable abbrev predecessorCountReal :=
  Erdos1135.KrasikovLagarias.predecessorCountReal

/-- Every eligible fixed target has an eventual `x^0.903` predecessor lower bound. -/
theorem predecessor_count_lower_bound_0903 {target : Nat}
    (htarget : 0 < target) (hmod : target % 3 ≠ 0) :
    ∀ᶠ x in atTop,
      x ^ ((903 : Real) / 1000) ≤ (predecessorCountReal target x : Real) :=
  Erdos1135.KrasikovLagarias.K18PredecessorAllTargets9032.eventually_rpow_903_1000_le_predecessorCountReal
    htarget hmod

/-- The same result at natural cutoffs. -/
theorem predecessor_count_lower_bound_0903_nat {target : Nat}
    (htarget : 0 < target) (hmod : target % 3 ≠ 0) :
    ∀ᶠ cutoff : Nat in atTop,
      (cutoff : Real) ^ ((903 : Real) / 1000) ≤
        (predecessorCount target cutoff : Real) :=
  Erdos1135.KrasikovLagarias.K18PredecessorAllTargets9032.eventually_natCast_rpow_903_1000_le_predecessorCount
    htarget hmod

/-- The stronger certificate exponent, with a target-dependent positive constant. -/
theorem predecessor_count_lower_bound_09032 {target : Nat}
    (htarget : 0 < target) (hmod : target % 3 ≠ 0) :
    ∃ constant : Real, 0 < constant ∧
      ∀ᶠ x in atTop,
        constant * x ^ ((9032 : Real) / 10000) ≤
          (predecessorCountReal target x : Real) :=
  Erdos1135.KrasikovLagarias.K18PredecessorAllTargets9032.eventually_const_mul_rpow_9032_10000_le_predecessorCountReal
    htarget hmod

end CollatzPredecessor0903
