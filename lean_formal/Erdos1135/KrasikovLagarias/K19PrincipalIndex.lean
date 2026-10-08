import Erdos1135.KrasikovLagarias.EliminationResidue

/-!
# Level-19 principal indices for source residues

Every natural number congruent to `2` modulo `3` determines a principal
residue class modulo `3^19`.
-/

namespace Erdos1135
namespace KrasikovLagarias
namespace K19PrincipalIndex

open EliminationResidue

/-- The level-19 principal index represented by a source congruent to `2`
modulo `3`. -/
def ofSource (source : Nat) : PrincipalIndex 19 := by
  let reduced := source % 3 ^ 19
  have hreducedLt : reduced < principalModulus 19 := by
    dsimp [reduced, principalModulus]
    exact Nat.mod_lt _ (by norm_num)
  refine ⟨reduced / 3, ?_⟩
  rw [Nat.div_lt_iff_lt_mul (by norm_num : 0 < 3), mul_comm]
  rw [← principalModulus_eq_three_mul_count (k := 19) (by norm_num)]
  exact hreducedLt

@[simp]
theorem residue_ofSource (source : Nat) (hsource : source % 3 = 2) :
    residue (ofSource source) = source % 3 ^ 19 := by
  let reduced := source % 3 ^ 19
  have hreducedMod : reduced % 3 = 2 := by
    calc
      reduced % 3 = source % 3 := by
        dsimp [reduced]
        exact Nat.mod_mod_of_dvd source (by norm_num : 3 ∣ 3 ^ 19)
      _ = 2 := hsource
  have hdecompose := Nat.mod_add_div reduced 3
  change 3 * (reduced / 3) + 2 = reduced
  omega

/-- Every source congruent to `2` modulo `3` is represented by a level-19
principal index. -/
theorem exists_modEq_residue (source : Nat) (hsource : source % 3 = 2) :
    ∃ index : PrincipalIndex 19,
      Nat.ModEq (3 ^ 19) source (residue index) := by
  refine ⟨ofSource source, ?_⟩
  unfold Nat.ModEq
  rw [residue_ofSource source hsource]
  rw [Nat.mod_mod]

end K19PrincipalIndex
end KrasikovLagarias
end Erdos1135
