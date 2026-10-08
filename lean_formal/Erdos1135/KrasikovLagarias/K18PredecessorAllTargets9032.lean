import Erdos1135.KrasikovLagarias.K18PredecessorBridge9032
import Erdos1135.KrasikovLagarias.K18PrincipalIndex
import Erdos1135.KrasikovLagarias.PeriodicTargetReduction

/-!
# The level-18 predecessor bound for every eligible target

This module assembles the checked level-18 certificate, the critical-choice
elimination theorem, and the target-reduction layer.  It improves the source
paper's exponent `0.84` to `0.903` for every positive target not divisible by
`3`.
-/

namespace Erdos1135
namespace KrasikovLagarias
namespace K18PredecessorAllTargets9032

open EliminationResidue
open Filter

/-- Every positive target not divisible by `3` is reached by an admissible
target represented by a level-18 principal residue. -/
theorem exists_principal_admissible_reaches {target : Nat}
    (htarget : 0 < target) (hmod : target % 3 ≠ 0) :
    ∃ (index : PrincipalIndex 18) (source : Nat),
      AdmissibleTarget 18 (residue index) source ∧ Reaches source target := by
  obtain ⟨source, hsourcePos, hsourceMod, hsourceNonperiodic, hreach⟩ :=
    exists_nonperiodic_mod_two_reaches_of_pos_mod_three_ne_zero htarget hmod
  obtain ⟨index, hsourceResidue⟩ :=
    K18PrincipalIndex.exists_modEq_residue source hsourceMod
  exact ⟨index, source, ⟨hsourcePos, hsourceResidue, hsourceNonperiodic⟩, hreach⟩

/-- Exact certificate consequence: every eligible fixed target has a
positive-constant `x^(9032/10000)` predecessor lower bound. -/
theorem eventually_const_mul_rpow_9032_10000_le_predecessorCountReal
    {target : Nat} (htarget : 0 < target) (hmod : target % 3 ≠ 0) :
    ∃ constant : Real, 0 < constant ∧
      ∀ᶠ x in atTop,
        constant * x ^ ((9032 : Real) / 10000) ≤
          (predecessorCountReal target x : Real) := by
  obtain ⟨index, source, hadmissible, hreach⟩ :=
    exists_principal_admissible_reaches htarget hmod
  exact K18PredecessorBridge9032.eventually_const_mul_rpow_9032_10000_le_predecessorCountReal
    index hadmissible hreach

/-- Publication-facing theorem: for every positive target not divisible by
`3`, the predecessor count is eventually at least `x^(903/1000) = x^0.903`. -/
theorem eventually_rpow_903_1000_le_predecessorCountReal
    {target : Nat} (htarget : 0 < target) (hmod : target % 3 ≠ 0) :
    ∀ᶠ x in atTop,
      x ^ ((903 : Real) / 1000) ≤ (predecessorCountReal target x : Real) := by
  obtain ⟨index, source, hadmissible, hreach⟩ :=
    exists_principal_admissible_reaches htarget hmod
  exact K18PredecessorBridge9032.eventually_rpow_903_1000_le_predecessorCountReal
    index hadmissible hreach

/-- Natural-cutoff form of the publication-facing theorem. -/
theorem eventually_natCast_rpow_903_1000_le_predecessorCount
    {target : Nat} (htarget : 0 < target) (hmod : target % 3 ≠ 0) :
    ∀ᶠ cutoff : Nat in atTop,
      (cutoff : Real) ^ ((903 : Real) / 1000) ≤
        (predecessorCount target cutoff : Real) := by
  have hreal := eventually_rpow_903_1000_le_predecessorCountReal htarget hmod
  filter_upwards [tendsto_natCast_atTop_atTop.eventually hreal] with cutoff hcutoff
  simpa [predecessorCountReal] using hcutoff

end K18PredecessorAllTargets9032
end KrasikovLagarias
end Erdos1135
