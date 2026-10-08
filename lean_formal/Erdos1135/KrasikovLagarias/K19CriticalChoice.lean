import Erdos1135.KrasikovLagarias.AdaptiveCriticalChoice
import Erdos1135.KrasikovLagarias.Generated.K19AdaptiveForcedPotential
import Erdos1135.KrasikovLagarias.K19CoefficientBridge
import Erdos1135.KrasikovLagarias.K19SourceBridge

/-!
# The level-19 adaptive retarded system

This is the small integration point between the two checked level-19 finite
certificates and the generic adaptive elimination theorem.
-/

namespace Erdos1135
namespace KrasikovLagarias
namespace K19CriticalChoice

open EliminationResidue
open K19SourceBridge
open K19G9093

local instance principalIndexNonempty : Nonempty (PrincipalIndex 19) :=
  ⟨⟨0, by norm_num [principalCount]⟩⟩

theorem one_le_phiValues19_zero (index : PrincipalIndex 19) :
    (1 : Real) ≤ phiValues19 index 0 := by
  have hpositive := phiValues19_pos index (y := 0) (by norm_num)
  change 0 < (phi 19 (EliminationResidue.residue index) 0 : Real) at hpositive
  have hpositiveNat : 0 < phi 19 (EliminationResidue.residue index) 0 := by
    exact_mod_cast hpositive
  have honeNat : 1 ≤ phi 19 (EliminationResidue.residue index) 0 := by
    omega
  change (1 : Real) ≤
    (phi 19 (EliminationResidue.residue index) 0 : Real)
  exact_mod_cast honeNat

/-- Exact level-19 consequence of the accepted `gamma = 9093 / 10000`
certificate. -/
theorem phiValues19_exponential_lower_bound :
    ∃ constant : Real, 0 < constant ∧
      ∀ index y, 0 ≤ y →
        constant * k19PrincipalWeights index * lambda9093 ^ y ≤
          phiValues19 index y := by
  exact AdaptiveCriticalChoice.exponential_lower_bound
    k19AdaptiveForcedPotential phiValues19 k19PrincipalWeights
    one_lt_lambda9093 phiValues19_isSourceSolution
    (fun index time htime => phiValues19_pos index htime)
    phiValues19_mono k19SourceSystem_isFeasible
    k19PrincipalWeights_pos one_le_phiValues19_zero

end K19CriticalChoice
end KrasikovLagarias
end Erdos1135
