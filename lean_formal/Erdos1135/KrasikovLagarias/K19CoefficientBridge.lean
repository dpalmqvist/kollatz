import Erdos1135.KrasikovLagarias.EliminationSourceSystem
import Erdos1135.KrasikovLagarias.Generated.K19Gamma9093

/-!
# The exact k = 19 source-system coefficient bridge

This module interprets the accepted `gamma = 9093 / 10000` certificate as a
positive feasible point of the original one-level KL source system.  It does
not perform elimination or assert an asymptotic consequence.
-/

namespace Erdos1135
namespace KrasikovLagarias
namespace K19G9093

open EliminationResidue
open EliminationSourceSystem
open Retarded

/-- The reserve exponent used by the accepted `k = 19` certificate. -/
noncomputable def gamma9093 : Real :=
  (9093 : Real) / 10000

/-- The original-source LP base corresponding to `gamma9093`. -/
noncomputable def lambda9093 : Real :=
  (2 : Real) ^ gamma9093

/-- The principal certificate weights, interpreted over the reals. -/
noncomputable def k19PrincipalWeights (index : PrincipalIndex 19) : Real :=
  k19Gamma9093EncodedCertificate.weight index.val

theorem gamma9093_pos : 0 < gamma9093 := by
  norm_num [gamma9093]

theorem lambda9093_pos : 0 < lambda9093 := by
  simpa [lambda9093] using Real.rpow_pos_of_pos (by norm_num : (0 : Real) < 2) gamma9093

theorem one_lt_lambda9093 : 1 < lambda9093 := by
  simpa [lambda9093] using
    Real.one_lt_rpow (by norm_num : (1 : Real) < 2) gamma9093_pos

private theorem ratio_three_pow_two_pow_eq_two_rpow
    (p d : Nat) :
    ((3 ^ p : Nat) : Real) / ((2 ^ d : Nat) : Real) =
      (2 : Real) ^ ((p : Real) * alpha - d) := by
  rw [Real.rpow_sub (by norm_num)]
  have hpalpha : (p : Real) * alpha = alpha * p := by ring
  rw [hpalpha, Real.rpow_mul_natCast (by norm_num), two_rpow_alpha,
    Real.rpow_natCast]
  norm_num only [Nat.cast_pow, Nat.cast_ofNat]

private theorem rationalRoot_three_pow_two_pow (p d q : Nat) :
    rationalRoot (3 ^ p) (2 ^ d) q =
      (2 : Real) ^ (((p : Real) * alpha - d) * ((1 : Real) / q)) := by
  rw [rationalRoot, ratio_three_pow_two_pow_eq_two_rpow,
    ← Real.rpow_mul (by norm_num)]

/-- The certificate's first real coefficient is exactly `lambda9093 ^ (-2)`. -/
theorem lambda9093_rpow_neg_two :
    lambda9093 ^ (-2 : Real) =
      (realCoefficients 9093 10000).lambdaNeg2 := by
  rw [lambda9093, ← Real.rpow_mul (by norm_num)]
  change (2 : Real) ^ (gamma9093 * (-2 : Real)) =
    rationalRoot 1 (2 ^ (2 * 9093)) 10000
  change (2 : Real) ^ (gamma9093 * (-2 : Real)) =
    rationalRoot (3 ^ 0) (2 ^ (2 * 9093)) 10000
  rw [rationalRoot_three_pow_two_pow]
  congr 1
  norm_num [gamma9093]

/-- The certificate's second real coefficient is exactly
`lambda9093 ^ (alpha - 2)`. -/
theorem lambda9093_rpow_alpha_minus_two :
    lambda9093 ^ (alpha - 2) =
      (realCoefficients 9093 10000).lambdaAlphaMinus2 := by
  rw [lambda9093, ← Real.rpow_mul (by norm_num)]
  change (2 : Real) ^ (gamma9093 * (alpha - 2)) =
    rationalRoot (3 ^ 9093) (2 ^ (2 * 9093)) 10000
  rw [rationalRoot_three_pow_two_pow]
  congr 1
  norm_num [gamma9093]
  ring

/-- The certificate's third real coefficient is exactly
`lambda9093 ^ (alpha - 1)`. -/
theorem lambda9093_rpow_alpha_minus_one :
    lambda9093 ^ (alpha - 1) =
      (realCoefficients 9093 10000).lambdaAlphaMinus1 := by
  rw [lambda9093, ← Real.rpow_mul (by norm_num)]
  change (2 : Real) ^ (gamma9093 * (alpha - 1)) =
    rationalRoot (3 ^ 9093) (2 ^ 9093) 10000
  rw [rationalRoot_three_pow_two_pow]
  congr 1
  norm_num [gamma9093]
  ring

private theorem k19Index_lt_certificatePrincipalCount
    (index : PrincipalIndex 19) :
    index.val < k19Gamma9093EncodedCertificate.principalCount := by
  simpa [EliminationResidue.principalCount, FiniteCertificate.principalCount,
    k19Gamma9093EncodedCertificate] using index.isLt

/-- Exact principal-child index agreement with the certificate checker. -/
theorem k19FourIndex_eq_certificate (index : PrincipalIndex 19) :
    (fourIndex (by norm_num : 1 <= 19) index).val =
      k19Gamma9093EncodedCertificate.fourIndex index.val := by
  exact fourIndex_eq_certificate k19Gamma9093EncodedCertificate
    k19Gamma9093EncodedCertificate_valid.1 index

/-- Exact D1 lift-index agreement with the certificate checker. -/
theorem k19D1PrincipalLift_eq_certificate (index : PrincipalIndex 19)
    (hrow : rowKind index = FiniteCertificate.RowKind.l1)
    (lift : LiftIndex) :
    (d1PrincipalLift (by norm_num : 2 <= 19) index hrow lift).val =
      k19Gamma9093EncodedCertificate.l1AuxiliaryIndex index.val +
        lift.val * k19Gamma9093EncodedCertificate.auxiliaryCount := by
  rfl

/-- Exact D3 lift-index agreement with the certificate checker. -/
theorem k19D3PrincipalLift_eq_certificate (index : PrincipalIndex 19)
    (hrow : rowKind index = FiniteCertificate.RowKind.l3)
    (lift : LiftIndex) :
    (d3PrincipalLift (by norm_num : 2 <= 19) index hrow lift).val =
      k19Gamma9093EncodedCertificate.l3AuxiliaryIndex index.val +
        lift.val * k19Gamma9093EncodedCertificate.auxiliaryCount := by
  rfl

@[simp]
theorem k19PrincipalWeights_fourIndex (index : PrincipalIndex 19) :
    k19PrincipalWeights (fourIndex (by norm_num : 1 <= 19) index) =
      k19Gamma9093EncodedCertificate.weight
        (k19Gamma9093EncodedCertificate.fourIndex index.val) := by
  simp [k19PrincipalWeights, k19FourIndex_eq_certificate]

/-- The three D1 source lifts are exactly the certificate's minimum auxiliary
weight. -/
theorem k19PrincipalWeights_d1_min (index : PrincipalIndex 19)
    (hrow : rowKind index = FiniteCertificate.RowKind.l1) :
    min
        (k19PrincipalWeights
          (d1PrincipalLift (by norm_num) index hrow (0 : LiftIndex)))
        (min
          (k19PrincipalWeights
            (d1PrincipalLift (by norm_num) index hrow (1 : LiftIndex)))
          (k19PrincipalWeights
            (d1PrincipalLift (by norm_num) index hrow (2 : LiftIndex)))) =
      k19Gamma9093EncodedCertificate.auxiliaryWeight
        (k19Gamma9093EncodedCertificate.l1AuxiliaryIndex index.val) := by
  simp [k19PrincipalWeights, k19D1PrincipalLift_eq_certificate,
    FiniteCertificate.auxiliaryWeight]

/-- The three D3 source lifts are exactly the certificate's minimum auxiliary
weight. -/
theorem k19PrincipalWeights_d3_min (index : PrincipalIndex 19)
    (hrow : rowKind index = FiniteCertificate.RowKind.l3) :
    min
        (k19PrincipalWeights
          (d3PrincipalLift (by norm_num) index hrow (0 : LiftIndex)))
        (min
          (k19PrincipalWeights
            (d3PrincipalLift (by norm_num) index hrow (1 : LiftIndex)))
          (k19PrincipalWeights
            (d3PrincipalLift (by norm_num) index hrow (2 : LiftIndex)))) =
      k19Gamma9093EncodedCertificate.auxiliaryWeight
        (k19Gamma9093EncodedCertificate.l3AuxiliaryIndex index.val) := by
  simp [k19PrincipalWeights, k19D3PrincipalLift_eq_certificate,
    FiniteCertificate.auxiliaryWeight]

private theorem min_three_mul_of_nonneg (a b c factor : Real)
    (hfactor : 0 <= factor) :
    min (a * factor) (min (b * factor) (c * factor)) =
      factor * min a (min b c) := by
  rw [← min_mul_of_nonneg b c hfactor,
    ← min_mul_of_nonneg a (min b c) hfactor]
  ring

/-- On every principal index, the source expression has exactly the real RHS
already certified by the generated certificate. -/
theorem k19SourceCoefficientValue_eq_realRowRhs (index : PrincipalIndex 19) :
    (sourceSystem (by norm_num : 2 <= 19) index).coefficientValue
        k19PrincipalWeights lambda9093 =
      k19Gamma9093EncodedCertificate.realRowRhs
        (realCoefficients 9093 10000) index.val := by
  cases hrow : rowKind index with
  | l1 =>
      have hrowCertificate :
          FiniteCertificate.rowKind index.val = FiniteCertificate.RowKind.l1 := by
        simpa [EliminationResidue.rowKind] using hrow
      rw [sourceSystem_coefficientValue_l1 (by norm_num) index hrow]
      rw [min_three_mul_of_nonneg _ _ _ _
        (Real.rpow_nonneg lambda9093_pos.le (alpha - 2))]
      rw [k19PrincipalWeights_d1_min index hrow]
      rw [k19PrincipalWeights_fourIndex, lambda9093_rpow_neg_two,
        lambda9093_rpow_alpha_minus_two]
      simp only [FiniteCertificate.realRowRhs, hrowCertificate]
      ring
  | l2 =>
      have hrowCertificate :
          FiniteCertificate.rowKind index.val = FiniteCertificate.RowKind.l2 := by
        simpa [EliminationResidue.rowKind] using hrow
      rw [sourceSystem_coefficientValue_l2 (by norm_num) index hrow]
      rw [k19PrincipalWeights_fourIndex, lambda9093_rpow_neg_two]
      simp only [FiniteCertificate.realRowRhs, hrowCertificate]
      ring
  | l3 =>
      have hrowCertificate :
          FiniteCertificate.rowKind index.val = FiniteCertificate.RowKind.l3 := by
        simpa [EliminationResidue.rowKind] using hrow
      rw [sourceSystem_coefficientValue_l3 (by norm_num) index hrow]
      rw [min_three_mul_of_nonneg _ _ _ _
        (Real.rpow_nonneg lambda9093_pos.le (alpha - 1))]
      rw [k19PrincipalWeights_d3_min index hrow]
      rw [k19PrincipalWeights_fourIndex, lambda9093_rpow_neg_two,
        lambda9093_rpow_alpha_minus_one]
      simp only [FiniteCertificate.realRowRhs, hrowCertificate]
      ring

theorem k19PrincipalWeights_pos (index : PrincipalIndex 19) :
    0 < k19PrincipalWeights index := by
  have hweight := k19Gamma9093EncodedCertificate_valid.weight_pos
    (k19Index_lt_certificatePrincipalCount index)
  change (0 : Real) <
    (k19Gamma9093EncodedCertificate.weight index.val : Real)
  exact_mod_cast hweight

/-- The accepted exact certificate is a positive feasible point of the
original `k = 19` source LP. -/
theorem k19SourceSystem_isFeasible :
    DifferenceSystem.IsFeasible
      (sourceSystem (by norm_num : 2 <= 19)) k19PrincipalWeights lambda9093 := by
  intro index
  rw [k19SourceCoefficientValue_eq_realRowRhs]
  simpa [FiniteCertificate.RealRowValid, k19PrincipalWeights] using
    (k19Gamma9093EncodedCertificate_realRowValid
      (k19Index_lt_certificatePrincipalCount index))

end K19G9093
end KrasikovLagarias
end Erdos1135
