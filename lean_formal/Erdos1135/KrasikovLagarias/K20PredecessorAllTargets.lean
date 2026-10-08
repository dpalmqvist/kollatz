import Erdos1135.KrasikovLagarias.Generated.K20Gamma9150
-- ^ first on purpose: the 9.3 GB olean must be mapped before Mathlib-heavy modules (address-range collision)
import Erdos1135.KrasikovLagarias.K20PredecessorBridge
import Erdos1135.KrasikovLagarias.K20PrincipalIndex
import Erdos1135.KrasikovLagarias.PeriodicTargetReduction

set_option maxRecDepth 100000  -- the 139-chunk certificate array exceeds the default simp recursion depth

/-!
# The level-20 predecessor bound for every eligible target

This module assembles the checked level-20 certificate, the critical-choice
elimination theorem, and the target-reduction layer.  It improves the source
paper's exponent `0.84` to `0.915` for every positive target not divisible by
`3`.
-/

namespace Erdos1135
namespace KrasikovLagarias
namespace K20PredecessorAllTargets

open EliminationResidue
open Filter

/-- Every positive target not divisible by `3` is reached by an admissible
target represented by a level-20 principal residue. -/
theorem exists_principal_admissible_reaches {target : Nat}
    (htarget : 0 < target) (hmod : target % 3 ≠ 0) :
    ∃ (index : PrincipalIndex 20) (source : Nat),
      AdmissibleTarget 20 (residue index) source ∧ Reaches source target := by
  obtain ⟨source, hsourcePos, hsourceMod, hsourceNonperiodic, hreach⟩ :=
    exists_nonperiodic_mod_two_reaches_of_pos_mod_three_ne_zero htarget hmod
  obtain ⟨index, hsourceResidue⟩ :=
    K20PrincipalIndex.exists_modEq_residue source hsourceMod
  exact ⟨index, source, ⟨hsourcePos, hsourceResidue, hsourceNonperiodic⟩, hreach⟩

/-- Exact certificate consequence: every eligible fixed target has a
positive-constant `x^(9150/10000)` predecessor lower bound. -/
theorem eventually_const_mul_rpow_9150_10000_le_predecessorCountReal
    {target : Nat} (htarget : 0 < target) (hmod : target % 3 ≠ 0) :
    ∃ constant : Real, 0 < constant ∧
      ∀ᶠ x in atTop,
        constant * x ^ ((9150 : Real) / 10000) ≤
          (predecessorCountReal target x : Real) := by
  obtain ⟨index, source, hadmissible, hreach⟩ :=
    exists_principal_admissible_reaches htarget hmod
  exact K20PredecessorBridge.eventually_const_mul_rpow_9150_10000_le_predecessorCountReal
    index hadmissible hreach

/-- Publication-facing theorem: for every positive target not divisible by
`3`, the predecessor count is eventually at least `x^(915/1000) = x^0.915`. -/
theorem eventually_rpow_915_1000_le_predecessorCountReal
    {target : Nat} (htarget : 0 < target) (hmod : target % 3 ≠ 0) :
    ∀ᶠ x in atTop,
      x ^ ((915 : Real) / 1000) ≤ (predecessorCountReal target x : Real) := by
  obtain ⟨index, source, hadmissible, hreach⟩ :=
    exists_principal_admissible_reaches htarget hmod
  exact K20PredecessorBridge.eventually_rpow_915_1000_le_predecessorCountReal
    index hadmissible hreach

/-- Natural-cutoff form of the publication-facing theorem. -/
theorem eventually_natCast_rpow_915_1000_le_predecessorCount
    {target : Nat} (htarget : 0 < target) (hmod : target % 3 ≠ 0) :
    ∀ᶠ cutoff : Nat in atTop,
      (cutoff : Real) ^ ((915 : Real) / 1000) ≤
        (predecessorCount target cutoff : Real) := by
  have hreal := eventually_rpow_915_1000_le_predecessorCountReal htarget hmod
  filter_upwards [tendsto_natCast_atTop_atTop.eventually hreal] with cutoff hcutoff
  simpa [predecessorCountReal] using hcutoff

end K20PredecessorAllTargets
end KrasikovLagarias
end Erdos1135
