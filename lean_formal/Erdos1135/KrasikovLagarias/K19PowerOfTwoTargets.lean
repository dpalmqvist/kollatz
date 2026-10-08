import Erdos1135.KrasikovLagarias.EliminationResidue
import Erdos1135.KrasikovLagarias.Envelope
import Mathlib.RingTheory.ZMod.UnitsCyclic

/-!
# Power-of-two targets in every level-19 KL class

The level-19 certificate uses every residue congruent to `2 mod 3` modulo
`3^19`.  This module proves that every such class contains a nonperiodic
power-of-two target.  The arithmetic input is that `2` generates the unit
group modulo `3^19`.
-/

namespace Erdos1135
namespace KrasikovLagarias
namespace K19PowerOfTwoTargets

open EliminationResidue

private abbrev modulus : Nat := 3 ^ 19

local instance modulusFact : Fact (1 < modulus) := ⟨by norm_num [modulus]⟩

/-- The unit represented by `2` modulo `3^19`. -/
private def twoUnit : (ZMod modulus)ˣ :=
  ZMod.unitOfCoprime 2 (by norm_num [modulus])

private theorem orderOf_negTwo :
    orderOf (-2 : ZMod modulus) = 3 ^ 18 := by
  convert ZMod.orderOf_one_add_mul_prime Nat.prime_three (by norm_num)
    (-1) (by norm_num) 18 using 1 <;> norm_num [modulus]

private theorem orderOf_two_zmod :
    orderOf (2 : ZMod modulus) = 2 * 3 ^ 18 := by
  have hnegOne : orderOf (-1 : ZMod modulus) = 2 := by
    rw [orderOf_neg_one, ringChar.eq (ZMod modulus) modulus,
      if_neg (by norm_num [modulus])]
  have hcoprime : Nat.Coprime
      (orderOf (-1 : ZMod modulus)) (orderOf (-2 : ZMod modulus)) := by
    rw [hnegOne, orderOf_negTwo]
    norm_num
  calc
    orderOf (2 : ZMod modulus) =
        orderOf ((-1 : ZMod modulus) * (-2 : ZMod modulus)) := by norm_num
    _ = orderOf (-1 : ZMod modulus) * orderOf (-2 : ZMod modulus) :=
      (Commute.all _ _).orderOf_mul_eq_mul_orderOf_of_coprime hcoprime
    _ = 2 * 3 ^ 18 := by rw [hnegOne, orderOf_negTwo]

private theorem orderOf_twoUnit : orderOf twoUnit = 2 * 3 ^ 18 := by
  rw [← orderOf_units]
  simpa [twoUnit, ZMod.coe_unitOfCoprime] using orderOf_two_zmod

private theorem card_units : Nat.card (ZMod modulus)ˣ = 2 * 3 ^ 18 := by
  rw [Nat.card_eq_fintype_card, ZMod.card_units_eq_totient]
  convert Nat.totient_prime_pow_succ Nat.prime_three 18 using 1 <;>
    norm_num [modulus]

/-- `2` generates all invertible residue classes modulo `3^19`. -/
private theorem zpowers_twoUnit : Subgroup.zpowers twoUnit = ⊤ := by
  apply Subgroup.eq_top_of_card_eq (Subgroup.zpowers twoUnit)
  rw [Nat.card_zpowers, orderOf_twoUnit, card_units]

/-- Every unit residue modulo `3^19` is represented by a power of two whose
exponent is at least two. -/
theorem exists_power_two_modEq_of_coprime (residue : Nat)
    (hcoprime : Nat.Coprime residue modulus) :
    ∃ exponent : Nat, 2 ≤ exponent ∧ Nat.ModEq modulus (2 ^ exponent) residue := by
  let residueUnit : (ZMod modulus)ˣ := ZMod.unitOfCoprime residue hcoprime
  have hmemZ : residueUnit ∈ Subgroup.zpowers twoUnit := by
    rw [zpowers_twoUnit]
    exact Subgroup.mem_top _
  have hmem : residueUnit ∈ Submonoid.powers twoUnit :=
    mem_powers_iff_mem_zpowers.mpr hmemZ
  obtain ⟨exponent, hexponent⟩ :=
    (Submonoid.mem_powers_iff residueUnit twoUnit).mp hmem
  let largeExponent := exponent + orderOf twoUnit
  have hlarge : 2 ≤ largeExponent := by
    dsimp [largeExponent]
    rw [orderOf_twoUnit]
    omega
  have hpow : twoUnit ^ largeExponent = residueUnit := by
    dsimp [largeExponent]
    rw [pow_add, pow_orderOf_eq_one, mul_one, hexponent]
  refine ⟨largeExponent, hlarge, ?_⟩
  apply (ZMod.natCast_eq_natCast_iff (2 ^ largeExponent) residue modulus).mp
  have hcoe := congrArg (fun unit : (ZMod modulus)ˣ => (unit : ZMod modulus)) hpow
  simpa [twoUnit, residueUnit, ZMod.coe_unitOfCoprime, Nat.cast_pow] using hcoe

/-- Powers `2^n` with `n ≥ 2` are not periodic points of the accelerated map. -/
theorem pow_two_not_inAcceleratedCycle {exponent : Nat} (hexponent : 2 ≤ exponent) :
    ¬ InAcceleratedCycle (2 ^ exponent) := by
  obtain ⟨extra, rfl⟩ := Nat.exists_eq_add_of_le hexponent
  clear hexponent
  induction extra with
  | zero => simpa using four_not_inAcceleratedCycle
  | succ extra ih =>
      simpa [show 2 + Nat.succ extra = Nat.succ (2 + extra) by omega,
        pow_succ, mul_comm] using two_mul_not_inAcceleratedCycle ih

/-- Every principal level-19 residue class has an admissible power-of-two target. -/
theorem principal_targetClassNonempty (index : PrincipalIndex 19) :
    TargetClassNonempty 19 (EliminationResidue.residue index) := by
  have hnotDvd : ¬3 ∣ EliminationResidue.residue index := by
    intro hdvd
    have hzero : EliminationResidue.residue index % 3 = 0 :=
      Nat.mod_eq_zero_of_dvd hdvd
    rw [EliminationResidue.residue_mod_three] at hzero
    omega
  have hcoprimeThree : Nat.Coprime (EliminationResidue.residue index) 3 :=
    (Nat.prime_three.coprime_iff_not_dvd.mpr hnotDvd).symm
  have hcoprime : Nat.Coprime (EliminationResidue.residue index) modulus :=
    hcoprimeThree.pow_right 19
  obtain ⟨exponent, hexponent, hmod⟩ :=
    exists_power_two_modEq_of_coprime _ hcoprime
  exact ⟨2 ^ exponent, by
    refine ⟨pow_pos (by norm_num) _, hmod, ?_⟩
    exact pow_two_not_inAcceleratedCycle hexponent⟩

end K19PowerOfTwoTargets
end KrasikovLagarias
end Erdos1135
