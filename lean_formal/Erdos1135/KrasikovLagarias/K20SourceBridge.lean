import Erdos1135.KrasikovLagarias.EliminationSourceSystem
import Erdos1135.KrasikovLagarias.K20PowerOfTwoTargets

/-!
# The exact level-20 source-envelope bridge

This module packages the level-20 Krasikov--Lagarias envelopes as real-valued
functions on the principal finite indices and proves that they satisfy the
one-level source difference system.
-/

namespace Erdos1135
namespace KrasikovLagarias
namespace K20SourceBridge

open EliminationResidue
open EliminationSourceSystem
open K20PowerOfTwoTargets

/-- The level-20 source envelopes, indexed by the finite principal classes. -/
noncomputable def phiValues20 (index : PrincipalIndex 20) (y : Real) : Real :=
  (phi 20 (residue index) y : Real)

/-- Every level-20 principal envelope is positive at nonnegative times. -/
theorem phiValues20_pos (index : PrincipalIndex 20) {y : Real} (hy : 0 <= y) :
    0 < phiValues20 index y := by
  change 0 < (phi 20 (residue index) y : Real)
  exact_mod_cast phi_pos (principal_targetClassNonempty index) hy

/-- Every level-20 principal envelope is monotone in time. -/
theorem phiValues20_mono (index : PrincipalIndex 20) :
    Monotone (phiValues20 index) := by
  intro lower upper htime
  change (phi 20 (residue index) lower : Real) <=
    (phi 20 (residue index) upper : Real)
  exact_mod_cast phi_mono (principal_targetClassNonempty index) htime

private theorem phiValues20_fourIndex (index : PrincipalIndex 20) (y : Real) :
    phiValues20 (fourIndex (by norm_num : 1 <= 20) index) y =
      (phi 20 (4 * residue index) y : Real) := by
  change (phi 20 (residue (fourIndex (by norm_num : 1 <= 20) index)) y : Real) =
    (phi 20 (4 * residue index) y : Real)
  exact_mod_cast phi_congr_residue y (by
    rw [residue_fourIndex]
    simp [fourTarget, principalModulus, Nat.ModEq])

private theorem phi_d1Auxiliary_eq_min (index : PrincipalIndex 20)
    (hrow : rowKind index = FiniteCertificate.RowKind.l1) (y : Real) :
    (phi 19 ((4 * residue index - 2) / 3) y : Real) =
      Min.min
        (phiValues20 (d1PrincipalLift (by norm_num) index hrow (0 : LiftIndex)) y)
        (Min.min
          (phiValues20 (d1PrincipalLift (by norm_num) index hrow (1 : LiftIndex)) y)
          (phiValues20 (d1PrincipalLift (by norm_num) index hrow (2 : LiftIndex)) y)) := by
  have hclass0 : TargetClassNonempty 20 (d1AuxiliaryBase 20 index).val := by
    simpa [auxiliaryModulus] using
      principal_targetClassNonempty
        (d1PrincipalLift (by norm_num) index hrow (0 : LiftIndex))
  have hclass1 :
      TargetClassNonempty 20 ((d1AuxiliaryBase 20 index).val + 3 ^ 19) := by
    simpa [auxiliaryModulus] using
      principal_targetClassNonempty
        (d1PrincipalLift (by norm_num) index hrow (1 : LiftIndex))
  have hclass2 :
      TargetClassNonempty 20 ((d1AuxiliaryBase 20 index).val + 2 * 3 ^ 19) := by
    simpa [auxiliaryModulus] using
      principal_targetClassNonempty
        (d1PrincipalLift (by norm_num) index hrow (2 : LiftIndex))
  have hreduce :
      phi 19 ((4 * residue index - 2) / 3) y =
        phi 19 (d1AuxiliaryBase 20 index).val y :=
    phi_congr_residue y (by
      simp [d1AuxiliaryBase, auxiliaryModulus, Nat.ModEq])
  have hlevel := phi_level_min (k := 20)
    (residue := (d1AuxiliaryBase 20 index).val) y
    (by norm_num) (d1AuxiliaryBase 20 index).isLt hclass0 hclass1 hclass2
  have hnat :
      phi 19 ((4 * residue index - 2) / 3) y =
        min
          (min (phi 20 (d1AuxiliaryBase 20 index).val y)
            (phi 20 ((d1AuxiliaryBase 20 index).val + 3 ^ 19) y))
          (phi 20 ((d1AuxiliaryBase 20 index).val + 2 * 3 ^ 19) y) :=
    hreduce.trans hlevel
  have hreal :
      (phi 19 ((4 * residue index - 2) / 3) y : Real) =
        min
          (min (phi 20 (d1AuxiliaryBase 20 index).val y : Real)
            (phi 20 ((d1AuxiliaryBase 20 index).val + 3 ^ 19) y : Real))
          (phi 20 ((d1AuxiliaryBase 20 index).val + 2 * 3 ^ 19) y : Real) := by
    exact_mod_cast hnat
  simpa [phiValues20, residue_d1PrincipalLift, auxiliaryModulus, min_assoc] using hreal

private theorem phi_d3Auxiliary_eq_min (index : PrincipalIndex 20)
    (hrow : rowKind index = FiniteCertificate.RowKind.l3) (y : Real) :
    (phi 19 ((2 * residue index - 1) / 3) y : Real) =
      Min.min
        (phiValues20 (d3PrincipalLift (by norm_num) index hrow (0 : LiftIndex)) y)
        (Min.min
          (phiValues20 (d3PrincipalLift (by norm_num) index hrow (1 : LiftIndex)) y)
          (phiValues20 (d3PrincipalLift (by norm_num) index hrow (2 : LiftIndex)) y)) := by
  have hclass0 : TargetClassNonempty 20 (d3AuxiliaryBase 20 index).val := by
    simpa [auxiliaryModulus] using
      principal_targetClassNonempty
        (d3PrincipalLift (by norm_num) index hrow (0 : LiftIndex))
  have hclass1 :
      TargetClassNonempty 20 ((d3AuxiliaryBase 20 index).val + 3 ^ 19) := by
    simpa [auxiliaryModulus] using
      principal_targetClassNonempty
        (d3PrincipalLift (by norm_num) index hrow (1 : LiftIndex))
  have hclass2 :
      TargetClassNonempty 20 ((d3AuxiliaryBase 20 index).val + 2 * 3 ^ 19) := by
    simpa [auxiliaryModulus] using
      principal_targetClassNonempty
        (d3PrincipalLift (by norm_num) index hrow (2 : LiftIndex))
  have hreduce :
      phi 19 ((2 * residue index - 1) / 3) y =
        phi 19 (d3AuxiliaryBase 20 index).val y :=
    phi_congr_residue y (by
      simp [d3AuxiliaryBase, auxiliaryModulus, Nat.ModEq])
  have hlevel := phi_level_min (k := 20)
    (residue := (d3AuxiliaryBase 20 index).val) y
    (by norm_num) (d3AuxiliaryBase 20 index).isLt hclass0 hclass1 hclass2
  have hnat :
      phi 19 ((2 * residue index - 1) / 3) y =
        min
          (min (phi 20 (d3AuxiliaryBase 20 index).val y)
            (phi 20 ((d3AuxiliaryBase 20 index).val + 3 ^ 19) y))
          (phi 20 ((d3AuxiliaryBase 20 index).val + 2 * 3 ^ 19) y) :=
    hreduce.trans hlevel
  have hreal :
      (phi 19 ((2 * residue index - 1) / 3) y : Real) =
        min
          (min (phi 20 (d3AuxiliaryBase 20 index).val y : Real)
            (phi 20 ((d3AuxiliaryBase 20 index).val + 3 ^ 19) y : Real))
          (phi 20 ((d3AuxiliaryBase 20 index).val + 2 * 3 ^ 19) y : Real) := by
    exact_mod_cast hnat
  simpa [phiValues20, residue_d3PrincipalLift, auxiliaryModulus, min_assoc] using hreal

/-- The exact level-20 envelopes satisfy the exact one-level source system. -/
theorem phiValues20_isSourceSolution :
    Retarded.DifferenceSystem.IsSolution
      (sourceSystem (k := 20) (by norm_num)) 2 phiValues20 := by
  intro index y hy
  cases hrow : rowKind index with
  | l1 =>
      rw [sourceSystem_eval_l1 (by norm_num) index hrow]
      rw [phiValues20_fourIndex]
      have hd1 := difference_d1 (k := 20) (residue := residue index)
        (by norm_num) ((rowKind_l1_iff_residue_mod_nine index).mp hrow)
        (principal_targetClassNonempty index) hy
      have hd1Real :
          (phi 20 (4 * residue index) (y - 2) : Real) +
              (phi 19 ((4 * residue index - 2) / 3) (y + alpha - 2) : Real) <=
            (phi 20 (residue index) y : Real) := by
        exact_mod_cast hd1
      rw [phi_d1Auxiliary_eq_min index hrow] at hd1Real
      simpa [phiValues20] using hd1Real
  | l2 =>
      rw [sourceSystem_eval_l2 (by norm_num) index hrow]
      rw [phiValues20_fourIndex]
      have hd2 := difference_d2 (k := 20) (residue := residue index)
        (principal_targetClassNonempty index) hy
      have hd2Real :
          (phi 20 (4 * residue index) (y - 2) : Real) <=
            (phi 20 (residue index) y : Real) := by
        exact_mod_cast hd2
      simpa [phiValues20] using hd2Real
  | l3 =>
      rw [sourceSystem_eval_l3 (by norm_num) index hrow]
      rw [phiValues20_fourIndex]
      have hd3 := difference_d3 (k := 20) (residue := residue index)
        (by norm_num) ((rowKind_l3_iff_residue_mod_nine index).mp hrow)
        (principal_targetClassNonempty index) hy
      have hd3Real :
          (phi 20 (4 * residue index) (y - 2) : Real) +
              (phi 19 ((2 * residue index - 1) / 3) (y + alpha - 1) : Real) <=
            (phi 20 (residue index) y : Real) := by
        exact_mod_cast hd3
      rw [phi_d3Auxiliary_eq_min index hrow] at hd3Real
      simpa [phiValues20] using hd3Real

end K20SourceBridge
end KrasikovLagarias
end Erdos1135
