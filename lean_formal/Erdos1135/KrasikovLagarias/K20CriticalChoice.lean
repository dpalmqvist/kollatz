import Erdos1135.KrasikovLagarias.Generated.K20Gamma9150
-- ^ first on purpose: the 9.3 GB olean must be mapped before Mathlib-heavy modules (address-range collision)
import Erdos1135.KrasikovLagarias.AdaptiveCriticalChoice
import Erdos1135.KrasikovLagarias.Generated.K20Potential10
import Erdos1135.KrasikovLagarias.K20CoefficientBridge
import Erdos1135.KrasikovLagarias.K20SourceBridge

set_option maxRecDepth 100000  -- the 139-chunk certificate array exceeds the default simp recursion depth

/-!
# The level-20 adaptive retarded system

This is the small integration point between the two checked level-20 finite
certificates and the generic adaptive elimination theorem.
-/

namespace Erdos1135
namespace KrasikovLagarias
namespace K20CriticalChoice

open EliminationResidue
open K20SourceBridge
open K20G9150

local instance principalIndexNonempty : Nonempty (PrincipalIndex 20) :=
  ⟨⟨0, by norm_num [principalCount]⟩⟩

theorem one_le_phiValues20_zero (index : PrincipalIndex 20) :
    (1 : Real) ≤ phiValues20 index 0 := by
  have hpositive := phiValues20_pos index (y := 0) (by norm_num)
  change 0 < (phi 20 (EliminationResidue.residue index) 0 : Real) at hpositive
  have hpositiveNat : 0 < phi 20 (EliminationResidue.residue index) 0 := by
    exact_mod_cast hpositive
  have honeNat : 1 ≤ phi 20 (EliminationResidue.residue index) 0 := by
    omega
  change (1 : Real) ≤
    (phi 20 (EliminationResidue.residue index) 0 : Real)
  exact_mod_cast honeNat

/-- Exact level-20 consequence of the accepted `gamma = 9150 / 10000`
certificate. -/
theorem phiValues20_exponential_lower_bound :
    ∃ constant : Real, 0 < constant ∧
      ∀ index y, 0 ≤ y →
        constant * k20PrincipalWeights index * lambda9150 ^ y ≤
          phiValues20 index y := by
  exact AdaptiveCriticalChoice.exponential_lower_bound
    k20AdaptiveForcedPotential phiValues20 k20PrincipalWeights
    one_lt_lambda9150 phiValues20_isSourceSolution
    (fun index time htime => phiValues20_pos index htime)
    phiValues20_mono k20SourceSystem_isFeasible
    k20PrincipalWeights_pos one_le_phiValues20_zero

end K20CriticalChoice
end KrasikovLagarias
end Erdos1135
