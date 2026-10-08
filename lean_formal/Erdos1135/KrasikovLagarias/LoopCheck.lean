import Erdos1135.KrasikovLagarias.Certificate
import Erdos1135.KrasikovLagarias.AdaptiveForcedPotentialCertificate

/-!
# Loop-based finite checkers (memory-lean replacements for the `List.range` checkers)

`FiniteCertificate.check` and `AdaptiveForcedPotentialCertificate.check` materialise a list with one
cell per principal residue (`List.range` / `List.finRange`).  For k = 19 (387 million residues) that
list alone costs several GB.  The checkers below iterate with a tail-recursive counter instead and are
proved equivalent to the original `Valid` predicates, so the downstream theorems can be fed
`valid_of_checkLoop` in place of `valid_of_check`.  (D. Palmqvist, 2026-10-08, add-on to L. Mazur's
development.)
-/

namespace Erdos1135
namespace KrasikovLagarias

/-- Tail-recursive conjunction of `p i` for `i < m`, accumulating into `acc`. -/
def allBelowGo (p : Nat → Bool) : Nat → Bool → Bool
  | 0, acc => acc
  | m + 1, acc => allBelowGo p m (acc && p m)

/-- `allBelow p n = true ↔ ∀ i < n, p i = true`, computed by a loop (no list). -/
def allBelow (p : Nat → Bool) (n : Nat) : Bool :=
  allBelowGo p n true

theorem allBelowGo_eq_true_iff (p : Nat → Bool) :
    ∀ (m : Nat) (acc : Bool),
      allBelowGo p m acc = true ↔ (acc = true ∧ ∀ i, i < m → p i = true) := by
  intro m
  induction m with
  | zero =>
    intro acc
    simp [allBelowGo]
  | succ m ih =>
    intro acc
    rw [allBelowGo, ih]
    constructor
    · rintro ⟨hacc, hall⟩
      rw [Bool.and_eq_true] at hacc
      refine ⟨hacc.1, ?_⟩
      intro i hi
      rcases Nat.lt_succ_iff_lt_or_eq.mp hi with hlt | heq
      · exact hall i hlt
      · rw [heq]; exact hacc.2
    · rintro ⟨hacc, hall⟩
      refine ⟨?_, fun i hi => hall i (Nat.lt_succ_of_lt hi)⟩
      rw [Bool.and_eq_true]
      exact ⟨hacc, hall m (Nat.lt_succ_self m)⟩

theorem allBelow_eq_true_iff (p : Nat → Bool) (n : Nat) :
    allBelow p n = true ↔ ∀ i, i < n → p i = true := by
  unfold allBelow
  rw [allBelowGo_eq_true_iff]
  simp

namespace FiniteCertificate

/-- Executable finite checker without the `List.range` allocation. -/
def checkLoop (cert : FiniteCertificate) : Bool :=
  decide cert.MetadataValid &&
    allBelow (fun index => decide (cert.RowValid index)) cert.principalCount

theorem checkLoop_eq_true_iff (cert : FiniteCertificate) :
    cert.checkLoop = true ↔ cert.Valid := by
  simp [checkLoop, Valid, allBelow_eq_true_iff]

theorem valid_of_checkLoop {cert : FiniteCertificate} (hcheck : cert.checkLoop = true) :
    cert.Valid :=
  (cert.checkLoop_eq_true_iff).mp hcheck

end FiniteCertificate

namespace AdaptiveForcedPotentialCertificate

open EliminationResidue

def rowsCheckLoop (cert : AdaptiveForcedPotentialCertificate)
    (hmeta : cert.MetadataValid) : Bool :=
  allBelow
    (fun i => if h : i < principalCount cert.k then
        decide (cert.RowValid hmeta ⟨i, h⟩) else true)
    (principalCount cert.k)

theorem rowsCheckLoop_eq_true_iff (cert : AdaptiveForcedPotentialCertificate)
    (hmeta : cert.MetadataValid) :
    cert.rowsCheckLoop hmeta = true ↔
      ∀ index : PrincipalIndex cert.k, cert.RowValid hmeta index := by
  rw [rowsCheckLoop, allBelow_eq_true_iff]
  constructor
  · intro hall index
    have hi := hall index.val index.isLt
    rw [dif_pos index.isLt] at hi
    exact of_decide_eq_true hi
  · intro hall i hi
    rw [dif_pos hi]
    exact decide_eq_true (hall ⟨i, hi⟩)

def checkLoop (cert : AdaptiveForcedPotentialCertificate) : Bool :=
  if hcheck : cert.metadataCheck = true then
    cert.rowsCheckLoop ((cert.metadataCheck_eq_true_iff).mp hcheck)
  else
    false

theorem valid_of_checkLoop {cert : AdaptiveForcedPotentialCertificate}
    (hcheck : cert.checkLoop = true) : cert.Valid := by
  by_cases hmeta : cert.metadataCheck = true
  · rw [checkLoop, dif_pos hmeta] at hcheck
    exact ⟨(cert.metadataCheck_eq_true_iff).mp hmeta,
      (cert.rowsCheckLoop_eq_true_iff _).mp hcheck⟩
  · rw [checkLoop, dif_neg hmeta] at hcheck
    exact absurd hcheck Bool.false_ne_true

def forcedPotential_of_checkLoop {cert : AdaptiveForcedPotentialCertificate}
    (hcheck : cert.checkLoop = true) :
    AdaptiveEliminationPolicy.ForcedPotential cert.k
      (cert.valid_of_checkLoop hcheck).metadata.1 :=
  (cert.valid_of_checkLoop hcheck).toForcedPotential

end AdaptiveForcedPotentialCertificate

end KrasikovLagarias
end Erdos1135
