import Erdos1135.KrasikovLagarias.K18CriticalChoice9032

/-!
# From level-18 envelopes to fixed-target predecessor counts

The level-18 envelope theorem is evaluated at
`y = log_2 (x / target)`.  This makes its scaled cutoff exactly `x` and
converts `lambda9032 ^ y` to a target-dependent positive constant times
`x ^ gamma9032`.  Reachability then transfers the count from the admissible
target to any downstream target.
-/

namespace Erdos1135
namespace KrasikovLagarias
namespace K18PredecessorBridge9032

open EliminationResidue
open Filter
open K18CriticalChoice9032
open K18G9032
open K18SourceBridge

theorem predecessorCountReal_le_of_reaches {firstTarget secondTarget : Nat}
    (hreach : Reaches firstTarget secondTarget) (x : Real) :
    predecessorCountReal firstTarget x ≤ predecessorCountReal secondTarget x :=
  predecessorCount_le_of_reaches hreach

/-- Any admissible target represented by a principal level-18 index transfers
the exact certificate exponent to every target it reaches. -/
theorem eventually_const_mul_rpow_9032_10000_le_predecessorCountReal
    (index : PrincipalIndex 18) {sourceTarget target : Nat}
    (hadmissible : AdmissibleTarget 18 (residue index) sourceTarget)
    (hreach : Reaches sourceTarget target) :
    ∃ constant : Real, 0 < constant ∧
      ∀ᶠ x in atTop,
        constant * x ^ ((9032 : Real) / 10000) ≤
          (predecessorCountReal target x : Real) := by
  obtain ⟨envelopeConstant, henvelopeConstant, henvelope⟩ :=
    phiValues18_exponential_lower_bound
  have hsourcePositive : 0 < (sourceTarget : Real) := by
    exact_mod_cast hadmissible.1
  let constant : Real :=
    envelopeConstant * k18PrincipalWeights index /
      (sourceTarget : Real) ^ gamma9032
  have hconstant : 0 < constant := by
    dsimp [constant]
    exact div_pos (mul_pos henvelopeConstant (k18PrincipalWeights_pos index))
      (Real.rpow_pos_of_pos hsourcePositive _)
  refine ⟨constant, hconstant, ?_⟩
  filter_upwards [eventually_ge_atTop (sourceTarget : Real)] with x hx
  have hxPositive : 0 < x := hsourcePositive.trans_le hx
  have hratioPositive : 0 < x / (sourceTarget : Real) :=
    div_pos hxPositive hsourcePositive
  have hratioOne : (1 : Real) ≤ x / (sourceTarget : Real) := by
    exact (le_div_iff₀ hsourcePositive).2 (by simpa using hx)
  let y : Real := Real.logb 2 (x / (sourceTarget : Real))
  have hy : 0 ≤ y := by
    exact Real.logb_nonneg (by norm_num) hratioOne
  have hpow : (2 : Real) ^ y = x / (sourceTarget : Real) := by
    exact Real.rpow_logb (by norm_num) (by norm_num) hratioPositive
  have hcutoff : (2 : Real) ^ y * (sourceTarget : Real) = x := by
    rw [hpow]
    exact div_mul_cancel₀ x hsourcePositive.ne'
  have henvelopeAt := henvelope index y hy
  have hphiTargetNat := phi_le_predecessorCountReal (k := 18)
    (residue := residue index) (target := sourceTarget) y hadmissible
  have hphiTarget : phiValues18 index y ≤
      (predecessorCountReal sourceTarget x : Real) := by
    change (phi 18 (residue index) y : Real) ≤ _
    rw [← hcutoff]
    exact_mod_cast hphiTargetNat
  have htargetTransfer :
      (predecessorCountReal sourceTarget x : Real) ≤
        (predecessorCountReal target x : Real) := by
    exact_mod_cast predecessorCountReal_le_of_reaches hreach x
  have hlambda : lambda9032 ^ y =
      (x / (sourceTarget : Real)) ^ gamma9032 := by
    rw [lambda9032, ← Real.rpow_mul (by norm_num)]
    rw [show gamma9032 * y = y * gamma9032 by ring,
      Real.rpow_mul (by norm_num), hpow]
  have hpowerIdentity :
      constant * x ^ gamma9032 =
        envelopeConstant * k18PrincipalWeights index * lambda9032 ^ y := by
    rw [hlambda]
    dsimp [constant]
    rw [Real.div_rpow hxPositive.le hsourcePositive.le]
    ring
  rw [gamma9032] at hpowerIdentity
  rw [hpowerIdentity]
  exact henvelopeAt.trans (hphiTarget.trans htargetTransfer)

/-- The positive exponent reserve turns the exact `0.9032` consequence into
the displayed eventual unit-coefficient `0.903` predecessor bound. -/
theorem eventually_rpow_903_1000_le_predecessorCountReal
    (index : PrincipalIndex 18) {sourceTarget target : Nat}
    (hadmissible : AdmissibleTarget 18 (residue index) sourceTarget)
    (hreach : Reaches sourceTarget target) :
    ∀ᶠ x in atTop,
      x ^ ((903 : Real) / 1000) ≤ (predecessorCountReal target x : Real) := by
  obtain ⟨constant, hconstant, hbound⟩ :=
    eventually_const_mul_rpow_9032_10000_le_predecessorCountReal
      index hadmissible hreach
  exact eventually_rpow_le_of_const_mul_rpow_le hconstant (by norm_num) hbound

end K18PredecessorBridge9032
end KrasikovLagarias
end Erdos1135
