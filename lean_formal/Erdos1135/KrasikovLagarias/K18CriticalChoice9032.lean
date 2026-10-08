import Erdos1135.KrasikovLagarias.AdaptiveCriticalChoice
import Erdos1135.KrasikovLagarias.Generated.K18AdaptiveForcedPotential
import Erdos1135.KrasikovLagarias.K18CoefficientBridge9032
import Erdos1135.KrasikovLagarias.K18SourceBridge

/-!
# The level-18 adaptive retarded system

This is the small integration point between the two checked level-18 finite
certificates and the generic adaptive elimination theorem.
-/

namespace Erdos1135
namespace KrasikovLagarias
namespace K18CriticalChoice9032

open EliminationResidue
open K18SourceBridge
open K18G9032

local instance principalIndexNonempty : Nonempty (PrincipalIndex 18) :=
  ⟨⟨0, by norm_num [principalCount]⟩⟩

theorem one_le_phiValues18_zero (index : PrincipalIndex 18) :
    (1 : Real) ≤ phiValues18 index 0 := by
  have hpositive := phiValues18_pos index (y := 0) (by norm_num)
  change 0 < (phi 18 (EliminationResidue.residue index) 0 : Real) at hpositive
  have hpositiveNat : 0 < phi 18 (EliminationResidue.residue index) 0 := by
    exact_mod_cast hpositive
  have honeNat : 1 ≤ phi 18 (EliminationResidue.residue index) 0 := by
    omega
  change (1 : Real) ≤
    (phi 18 (EliminationResidue.residue index) 0 : Real)
  exact_mod_cast honeNat

/-- Exact level-18 consequence of the accepted `gamma = 9032 / 10000`
certificate. -/
theorem phiValues18_exponential_lower_bound :
    ∃ constant : Real, 0 < constant ∧
      ∀ index y, 0 ≤ y →
        constant * k18PrincipalWeights index * lambda9032 ^ y ≤
          phiValues18 index y := by
  exact AdaptiveCriticalChoice.exponential_lower_bound
    k18AdaptiveForcedPotential phiValues18 k18PrincipalWeights
    one_lt_lambda9032 phiValues18_isSourceSolution
    (fun index time htime => phiValues18_pos index htime)
    phiValues18_mono k18SourceSystem_isFeasible
    k18PrincipalWeights_pos one_le_phiValues18_zero

end K18CriticalChoice9032
end KrasikovLagarias
end Erdos1135
