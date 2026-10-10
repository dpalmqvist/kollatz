import Mathlib

/-!
# Krasikov–Lagarias linear programs L^NT_k: structure

Level `k = n + 2`. Principal classes `m ∈ [3^k]` (`m ≡ 2 mod 3`) are indexed by `i : Fin (N n)`,
`N n = 3^(n+1)`, via `m = 3 i + 2`; auxiliary classes `r ∈ [3^(k-1)]` by `s : Fin (M n)`, `M n = 3^n`.
-/

open Finset

namespace KLMono

def N (n : ℕ) : ℕ := 3 ^ (n + 1)
def M (n : ℕ) : ℕ := 3 ^ n

lemma N_eq (n : ℕ) : N n = 3 * M n := by unfold N M; ring
lemma N_eq' (n : ℕ) : N n = M n * 3 := by unfold N M; ring
lemma M_pos (n : ℕ) : 0 < M n := by unfold M; positivity
lemma N_pos (n : ℕ) : 0 < N n := by unfold N; positivity

instance (n : ℕ) : NeZero (N n) := ⟨(N_pos n).ne'⟩
instance (n : ℕ) : NeZero (M n) := ⟨(M_pos n).ne'⟩

/-- index of `4m` -/
def nu {n : ℕ} (i : Fin (N n)) : Fin (N n) := ⟨(4 * i.val + 2) % N n, Nat.mod_lt _ (N_pos n)⟩

/-- auxiliary index of a class-0 row (`m ≡ 2 mod 9`): the class `(4m-2)/3` -/
def auxA {n : ℕ} (i : Fin (N n)) : Fin (M n) := ⟨(4 * (i.val / 3)) % M n, Nat.mod_lt _ (M_pos n)⟩

/-- auxiliary index of a class-2 row (`m ≡ 8 mod 9`): the class `(2m-1)/3` -/
def auxB {n : ℕ} (i : Fin (N n)) : Fin (M n) := ⟨(2 * (i.val / 3) + 1) % M n, Nat.mod_lt _ (M_pos n)⟩

/-- the three lifts `s + u * 3^n` of an auxiliary index -/
def lift {n : ℕ} (s : Fin (M n)) (u : Fin 3) : Fin (N n) :=
  ⟨s.val + M n * u.val, by
    have h1 := s.isLt; have h2 := u.isLt; rw [N_eq]
    have : M n * u.val ≤ M n * 2 := Nat.mul_le_mul_left _ (by omega)
    omega⟩

noncomputable def cbar {n : ℕ} (c : Fin (N n) → ℝ) (s : Fin (M n)) : ℝ :=
  min (c (lift s 0)) (min (c (lift s 1)) (c (lift s 2)))

/-- right-hand side with abstract coefficients `p = λ^-2`, `q = λ^(α-2)`, `r = λ^(α-1)` -/
noncomputable def Fc {n : ℕ} (p q r : ℝ) (c : Fin (N n) → ℝ) (i : Fin (N n)) : ℝ :=
  p * c (nu i) +
    (if i.val % 3 = 0 then q * cbar c (auxA i) else if i.val % 3 = 2 then r * cbar c (auxB i) else 0)

/-! ## structural lemmas -/

lemma cbar_le {n : ℕ} (c : Fin (N n) → ℝ) (s : Fin (M n)) (u : Fin 3) : cbar c s ≤ c (lift s u) := by
  unfold cbar
  fin_cases u <;> simp

lemma cbar_mono {n : ℕ} {x y : Fin (N n) → ℝ} (h : ∀ i, x i ≤ y i) (s : Fin (M n)) :
    cbar x s ≤ cbar y s := by
  unfold cbar
  exact min_le_min (h _) (min_le_min (h _) (h _))

lemma cbar_add {n : ℕ} (x y : Fin (N n) → ℝ) (s : Fin (M n)) :
    cbar x s + cbar y s ≤ cbar (x + y) s := by
  unfold cbar
  simp only [Pi.add_apply]
  refine le_min ?_ (le_min ?_ ?_)
  · exact add_le_add (min_le_left _ _) (min_le_left _ _)
  · exact add_le_add ((min_le_right _ _).trans (min_le_left _ _)) ((min_le_right _ _).trans (min_le_left _ _))
  · exact add_le_add ((min_le_right _ _).trans (min_le_right _ _)) ((min_le_right _ _).trans (min_le_right _ _))

lemma cbar_nonneg {n : ℕ} {x : Fin (N n) → ℝ} (h : ∀ i, 0 ≤ x i) (s : Fin (M n)) : 0 ≤ cbar x s := by
  unfold cbar
  exact le_min (h _) (le_min (h _) (h _))

lemma cbar_pos {n : ℕ} {x : Fin (N n) → ℝ} (h : ∀ i, 0 < x i) (s : Fin (M n)) : 0 < cbar x s := by
  unfold cbar
  exact lt_min (h _) (lt_min (h _) (h _))

section coef
variable {n : ℕ} {p q r : ℝ}

lemma Fc_mono (hp : 0 ≤ p) (hq : 0 ≤ q) (hr : 0 ≤ r) {x y : Fin (N n) → ℝ} (h : ∀ i, x i ≤ y i)
    (i : Fin (N n)) : Fc p q r x i ≤ Fc p q r y i := by
  unfold Fc
  have h1 := mul_le_mul_of_nonneg_left (h (nu i)) hp
  split_ifs
  · exact add_le_add h1 (mul_le_mul_of_nonneg_left (cbar_mono h _) hq)
  · exact add_le_add h1 (mul_le_mul_of_nonneg_left (cbar_mono h _) hr)
  · simpa using h1

lemma Fc_superadd (hp : 0 ≤ p) (hq : 0 ≤ q) (hr : 0 ≤ r) (x y : Fin (N n) → ℝ) (i : Fin (N n)) :
    Fc p q r x i + Fc p q r y i ≤ Fc p q r (x + y) i := by
  unfold Fc
  simp only [Pi.add_apply]
  split_ifs
  · nlinarith [mul_le_mul_of_nonneg_left (cbar_add x y (auxA i)) hq]
  · nlinarith [mul_le_mul_of_nonneg_left (cbar_add x y (auxB i)) hr]
  · linarith

lemma Fc_ge (hq : 0 ≤ q) (hr : 0 ≤ r) {x : Fin (N n) → ℝ} (hx : ∀ i, 0 ≤ x i) (i : Fin (N n)) :
    p * x (nu i) ≤ Fc p q r x i := by
  unfold Fc
  split_ifs
  · nlinarith [mul_nonneg hq (cbar_nonneg hx (auxA i))]
  · nlinarith [mul_nonneg hr (cbar_nonneg hx (auxB i))]
  · simp

lemma Fc_nonneg (hp : 0 ≤ p) (hq : 0 ≤ q) (hr : 0 ≤ r) {x : Fin (N n) → ℝ} (hx : ∀ i, 0 ≤ x i)
    (i : Fin (N n)) : 0 ≤ Fc p q r x i :=
  le_trans (mul_nonneg hp (hx _)) (Fc_ge hq hr hx i)

end coef

/-! ## the ×4 map is a single cycle -/

/-- the residue `3 i + 2 mod 3^(n+2)` of index `i` -/
def res {n : ℕ} (i : Fin (N n)) : ZMod (3 ^ (n + 2)) := ((3 * i.val + 2 : ℕ) : ZMod (3 ^ (n + 2)))

lemma res_nu {n : ℕ} (i : Fin (N n)) : res (nu i) = 4 * res i := by
  unfold res nu
  simp only
  have h : 3 * ((4 * i.val + 2) % N n) = (3 * (4 * i.val + 2)) % 3 ^ (n + 2) := by
    rw [show 3 ^ (n + 2) = 3 * N n by unfold N; ring, Nat.mul_mod_mul_left]
  rw [h]
  rw [show (3 * (4 * i.val + 2)) % 3 ^ (n + 2) + 2 = ((3 * (4 * i.val + 2)) % 3 ^ (n + 2) + 2) from rfl]
  push_cast [ZMod.natCast_mod]
  ring

lemma res_injective {n : ℕ} : Function.Injective (@res n) := by
  intro i j h
  unfold res at h
  rw [ZMod.natCast_eq_natCast_iff'] at h
  have hi := i.isLt; have hj := j.isLt
  unfold N at hi hj
  have h3 : 3 ^ (n + 2) = 3 * 3 ^ (n + 1) := by ring
  rw [Nat.mod_eq_of_lt (by omega), Nat.mod_eq_of_lt (by omega)] at h
  exact Fin.ext (by omega)

lemma res_isUnit {n : ℕ} (i : Fin (N n)) : IsUnit (res i) := by
  unfold res
  rw [ZMod.isUnit_iff_coprime]
  apply Nat.Coprime.pow_right
  rw [Nat.coprime_comm, Nat.Prime.coprime_iff_not_dvd Nat.prime_three]
  omega

lemma res_iterate {n : ℕ} (i : Fin (N n)) (s : ℕ) : res (nu^[s] i) = 4 ^ s * res i := by
  induction s with
  | zero => simp
  | succ s ih => rw [Function.iterate_succ_apply', res_nu, ih]; ring

lemma orderOf_four (n : ℕ) : orderOf (4 : ZMod (3 ^ (n + 2))) = N n := by
  have := ZMod.orderOf_one_add_prime Nat.prime_three (by norm_num) (n + 1)
  unfold N
  rw [← this]
  norm_num

/-- every index is reached from every other by iterating `nu` fewer than `N` times -/
lemma nu_reach {n : ℕ} (i j : Fin (N n)) : ∃ s, s < N n ∧ nu^[s] i = j := by
  let f : Fin (N n) → Fin (N n) := fun s => nu^[s.val] i
  have hf : Function.Injective f := by
    intro s t h
    have h1 : res (nu^[s.val] i) = res (nu^[t.val] i) := congrArg res h
    rw [res_iterate, res_iterate] at h1
    have h2 : (4 : ZMod (3 ^ (n + 2))) ^ s.val = 4 ^ t.val := (res_isUnit i).mul_left_inj.mp h1
    have hfin : IsOfFinOrder (4 : ZMod (3 ^ (n + 2))) := by
      rw [← orderOf_pos_iff, orderOf_four]; exact N_pos n
    rw [hfin.pow_eq_pow_iff_modEq, orderOf_four] at h2
    unfold Nat.ModEq at h2
    rw [Nat.mod_eq_of_lt s.isLt, Nat.mod_eq_of_lt t.isLt] at h2
    exact Fin.ext h2
  obtain ⟨s, hs⟩ := (Finite.injective_iff_surjective.mp hf) j
  exact ⟨s.val, s.isLt, hs⟩


/-! ## propagation along the cycle -/

section prop
variable {n : ℕ} {p q r : ℝ}

lemma Fc_zero (i : Fin (N n)) : Fc p q r (0 : Fin (N n) → ℝ) i = 0 := by
  unfold Fc cbar; simp

lemma Fc_smul {t : ℝ} (ht : 0 ≤ t) (x : Fin (N n) → ℝ) (i : Fin (N n)) :
    Fc p q r (t • x) i = t * Fc p q r x i := by
  have hc : ∀ s, cbar (t • x) s = t * cbar x s := by
    intro s; unfold cbar; simp only [Pi.smul_apply, smul_eq_mul]
    rw [mul_min_of_nonneg _ _ ht, mul_min_of_nonneg _ _ ht]
  unfold Fc
  simp only [Pi.smul_apply, smul_eq_mul, hc]
  split_ifs <;> ring

/-- the gain of `F` at row `i` is at least `p` times the gain at `nu i` -/
lemma Fc_sub_ge (hq : 0 ≤ q) (hr : 0 ≤ r) {x y : Fin (N n) → ℝ} (h : ∀ i, x i ≤ y i) (i : Fin (N n)) :
    p * (y (nu i) - x (nu i)) ≤ Fc p q r y i - Fc p q r x i := by
  unfold Fc
  split_ifs
  · nlinarith [mul_le_mul_of_nonneg_left (cbar_mono h (auxA i)) hq]
  · nlinarith [mul_le_mul_of_nonneg_left (cbar_mono h (auxB i)) hr]
  · nlinarith

variable (hp : 0 < p) (hq : 0 ≤ q) (hr : 0 ≤ r)
include hp hq hr

lemma iter_succ_ge {x : Fin (N n) → ℝ} (hx : ∀ i, x i ≤ Fc p q r x i) (t : ℕ) (i : Fin (N n)) :
    (Fc p q r)^[t] x i ≤ (Fc p q r)^[t + 1] x i := by
  induction t generalizing i with
  | zero => simpa using hx i
  | succ t ih =>
    rw [Function.iterate_succ_apply' _ (t + 1), Function.iterate_succ_apply' _ t]
    exact Fc_mono hp.le hq hr (fun j => by have := ih j; rwa [Function.iterate_succ_apply'] at this) i

lemma iter_mono {x : Fin (N n) → ℝ} (hx : ∀ i, x i ≤ Fc p q r x i) {s t : ℕ} (hst : s ≤ t)
    (i : Fin (N n)) : (Fc p q r)^[s] x i ≤ (Fc p q r)^[t] x i := by
  induction hst with
  | refl => exact le_rfl
  | step _ ih => exact ih.trans (iter_succ_ge hp hq hr hx _ i)

lemma iter_ge {x : Fin (N n) → ℝ} (hx : ∀ i, x i ≤ Fc p q r x i) (t : ℕ) (i : Fin (N n)) :
    x i ≤ (Fc p q r)^[t] x i := by
  simpa using iter_mono hp hq hr hx (Nat.zero_le t) i

/-- strict slack at `j` reaches every row `i` with `nu^[s] i = j` after `s + 1` steps -/
lemma strict_spread {x : Fin (N n) → ℝ} (hx : ∀ i, x i ≤ Fc p q r x i) {j : Fin (N n)}
    (hj : x j < Fc p q r x j) (s : ℕ) :
    ∀ i, nu^[s] i = j → x i < (Fc p q r)^[s + 1] x i := by
  induction s with
  | zero => intro i hi; simp only [Function.iterate_zero, id] at hi; subst hi; simpa using hj
  | succ s ih =>
    intro i hi
    rw [Function.iterate_succ_apply] at hi
    have h1 := ih (nu i) hi
    have hge : ∀ k, x k ≤ (Fc p q r)^[s + 1] x k := iter_ge hp hq hr hx (s + 1)
    have h2 := Fc_sub_ge (p := p) hq hr hge i
    rw [Function.iterate_succ_apply' _ (s + 1)]
    have h3 : 0 < p * ((Fc p q r)^[s + 1] x (nu i) - x (nu i)) := mul_pos hp (by linarith)
    linarith [hx i]

lemma sum_iter_le {x : Fin (N n) → ℝ} (T : ℕ) (i : Fin (N n)) :
    ∑ t ∈ range T, Fc p q r ((Fc p q r)^[t] x) i ≤ Fc p q r (∑ t ∈ range T, (Fc p q r)^[t] x) i := by
  induction T generalizing i with
  | zero => simp [Fc_zero]
  | succ T ih =>
    rw [sum_range_succ, sum_range_succ]
    exact (add_le_add (ih i) le_rfl).trans (Fc_superadd hp.le hq hr _ _ i)

/-- **Lemma 3.** A positive sub-solution with slack somewhere yields a strict sub-solution. -/
theorem exists_strict {x : Fin (N n) → ℝ} (hpos : ∀ i, 0 < x i) (hx : ∀ i, x i ≤ Fc p q r x i)
    {j : Fin (N n)} (hj : x j < Fc p q r x j) :
    ∃ z : Fin (N n) → ℝ, (∀ i, 0 < z i) ∧ ∀ i, z i < Fc p q r z i := by
  set y : ℕ → Fin (N n) → ℝ := fun t => (Fc p q r)^[t] x with hy
  refine ⟨∑ t ∈ range (N n), y t, ?_, ?_⟩
  · intro i
    rw [Finset.sum_apply]
    have h0 : (0 : ℕ) ∈ range (N n) := mem_range.mpr (N_pos n)
    have hnn : ∀ t ∈ range (N n), 0 ≤ y t i := fun t _ =>
      (hpos i).le.trans (iter_ge hp hq hr hx t i)
    have := Finset.single_le_sum hnn h0
    simp only [hy, Function.iterate_zero, id] at this
    linarith [hpos i]
  · intro i
    have h1 := sum_iter_le hp hq hr (x := x) (N n) i
    have h2 : ∑ t ∈ range (N n), Fc p q r (y t) i = ∑ t ∈ range (N n), y (t + 1) i := by
      apply sum_congr rfl; intro t _; simp only [hy]; rw [Function.iterate_succ_apply']
    have h3 : ∑ t ∈ range (N n), y (t + 1) i + y 0 i = ∑ t ∈ range (N n), y t i + y (N n) i := by
      rw [← sum_range_succ' (fun t => y t i), sum_range_succ]
    obtain ⟨s, hs, hsi⟩ := nu_reach i j
    have h4 := strict_spread hp hq hr hx hj s i hsi
    have h5 : (Fc p q r)^[s + 1] x i ≤ y (N n) i := iter_mono hp hq hr hx (by omega) i
    rw [Finset.sum_apply]
    have h6 : y 0 i = x i := by simp [hy]
    simp only [hy] at h1 h2 h3 h5 h6 ⊢
    linarith

/-- **Lemma 4.** A nonzero nonnegative sub-solution yields a positive one. -/
theorem exists_pos {x : Fin (N n) → ℝ} (hnn : ∀ i, 0 ≤ x i) (hx : ∀ i, x i ≤ Fc p q r x i)
    {j : Fin (N n)} (hj : 0 < x j) :
    ∃ z : Fin (N n) → ℝ, (∀ i, 0 < z i) ∧ ∀ i, z i ≤ Fc p q r z i := by
  have hge : ∀ t k, 0 ≤ (Fc p q r)^[t] x k := fun t k => (hnn k).trans (iter_ge hp hq hr hx t k)
  have key : ∀ s, ∀ i, nu^[s] i = j → 0 < (Fc p q r)^[s] x i := by
    intro s
    induction s with
    | zero => intro i hi; simp only [Function.iterate_zero, id] at hi ⊢; subst hi; exact hj
    | succ s ih =>
      intro i hi
      rw [Function.iterate_succ_apply] at hi
      rw [Function.iterate_succ_apply']
      exact lt_of_lt_of_le (mul_pos hp (ih _ hi)) (Fc_ge hq hr (hge s) i)
  refine ⟨(Fc p q r)^[N n] x, ?_, ?_⟩
  · intro i
    obtain ⟨s, hs, hsi⟩ := nu_reach i j
    exact lt_of_lt_of_le (key s i hsi) (iter_mono hp hq hr hx hs.le i)
  · intro i
    have := iter_succ_ge hp hq hr hx (N n) i
    rwa [Function.iterate_succ_apply'] at this

/-- **Lemma 7.** Positive fixed points are unique up to a positive factor. -/
theorem fixed_unique {c c' : Fin (N n) → ℝ} (hc : ∀ i, 0 < c i) (hc' : ∀ i, 0 < c' i)
    (hf : ∀ i, Fc p q r c i = c i) (hf' : ∀ i, Fc p q r c' i = c' i) :
    ∃ t : ℝ, 0 < t ∧ c' = t • c := by
  obtain ⟨i0, -, hi0⟩ := Finset.exists_min_image Finset.univ (fun i => c' i / c i) Finset.univ_nonempty
  set t := c' i0 / c i0 with ht
  have htpos : 0 < t := div_pos (hc' i0) (hc i0)
  set d : Fin (N n) → ℝ := c' - t • c with hd
  have hdnn : ∀ i, 0 ≤ d i := by
    intro i
    have h := hi0 i (Finset.mem_univ _)
    simp only [hd, Pi.sub_apply, Pi.smul_apply, smul_eq_mul]
    rw [le_div_iff₀ (hc i)] at h
    linarith
  have hd0 : d i0 = 0 := by
    simp only [hd, Pi.sub_apply, Pi.smul_apply, smul_eq_mul, ht]
    field_simp [(hc i0).ne']
    ring
  have hFd : ∀ i, Fc p q r d i ≤ d i := by
    intro i
    have h1 := Fc_superadd hp.le hq hr (t • c) d i
    have h2 : t • c + d = c' := by simp [hd]
    rw [h2, hf', Fc_smul htpos.le, hf] at h1
    simp only [hd, Pi.sub_apply, Pi.smul_apply, smul_eq_mul] at h1 ⊢
    linarith
  have hzero : ∀ s, d (nu^[s] i0) = 0 := by
    intro s
    induction s with
    | zero => simpa using hd0
    | succ s ih =>
      rw [Function.iterate_succ_apply']
      have h1 := Fc_ge (p := p) hq hr hdnn (nu^[s] i0)
      have h2 := hFd (nu^[s] i0)
      rw [ih] at h2
      have h3 := hdnn (nu (nu^[s] i0))
      have h4 : p * d (nu (nu^[s] i0)) ≤ 0 := by linarith
      nlinarith
  refine ⟨t, htpos, funext fun i => ?_⟩
  obtain ⟨s, -, hs⟩ := nu_reach i0 i
  have := hzero s
  rw [hs] at this
  simp only [hd, Pi.sub_apply, Pi.smul_apply, smul_eq_mul] at this ⊢
  linarith

end prop

/-! ## index bijections and the summation identity -/

section sums
variable {n : ℕ}

lemma coprime_four_pow (m : ℕ) : Nat.Coprime 4 (3 ^ m) :=
  Nat.Coprime.pow_right _ (by norm_num)

lemma coprime_two_pow (m : ℕ) : Nat.Coprime 2 (3 ^ m) :=
  Nat.Coprime.pow_right _ (by norm_num)

/-- `j ↦ 4 j mod 3^n` -/
def mul4 (j : Fin (M n)) : Fin (M n) := ⟨(4 * j.val) % M n, Nat.mod_lt _ (M_pos n)⟩
/-- `j ↦ 2 j + 1 mod 3^n` -/
def aff2 (j : Fin (M n)) : Fin (M n) := ⟨(2 * j.val + 1) % M n, Nat.mod_lt _ (M_pos n)⟩

lemma mul4_injective : Function.Injective (@mul4 n) := by
  intro a b h
  have h1 : 4 * a.val ≡ 4 * b.val [MOD M n] := by
    unfold mul4 at h; exact Fin.mk.inj_iff.mp h
  have h2 := Nat.ModEq.cancel_left_of_coprime (by unfold M; exact (coprime_four_pow n).symm) h1
  have := Nat.ModEq.eq_of_lt_of_lt h2 a.isLt b.isLt
  exact Fin.ext this

lemma aff2_injective : Function.Injective (@aff2 n) := by
  intro a b h
  have h1 : 2 * a.val + 1 ≡ 2 * b.val + 1 [MOD M n] := by
    unfold aff2 at h; exact Fin.mk.inj_iff.mp h
  have h1' := Nat.ModEq.add_right_cancel' 1 h1
  have h2 := Nat.ModEq.cancel_left_of_coprime (by unfold M; exact (coprime_two_pow n).symm) h1'
  exact Fin.ext (Nat.ModEq.eq_of_lt_of_lt h2 a.isLt b.isLt)

lemma mul4_bijective : Function.Bijective (@mul4 n) :=
  ⟨mul4_injective, Finite.injective_iff_surjective.mp mul4_injective⟩

lemma aff2_bijective : Function.Bijective (@aff2 n) :=
  ⟨aff2_injective, Finite.injective_iff_surjective.mp aff2_injective⟩

lemma nu_injective : Function.Injective (@nu n) := by
  intro a b h
  have h1 := congrArg res h
  rw [res_nu, res_nu] at h1
  have h4 : IsUnit (4 : ZMod (3 ^ (n + 2))) := by
    have := (ZMod.isUnit_iff_coprime 4 (3 ^ (n + 2))).mpr (coprime_four_pow _)
    simpa using this
  exact res_injective (h4.mul_right_inj.mp h1)

lemma nu_bijective : Function.Bijective (@nu n) :=
  ⟨nu_injective, Finite.injective_iff_surjective.mp nu_injective⟩

lemma sum_nu (c : Fin (N n) → ℝ) : ∑ i, c (nu i) = ∑ i, c i :=
  nu_bijective.sum_comp c

/-- the class-0 row `3 j` -/
def row0 (j : Fin (M n)) : Fin (N n) := ⟨3 * j.val, by rw [N_eq]; have := j.isLt; omega⟩
/-- the class-2 row `3 j + 2` -/
def row2 (j : Fin (M n)) : Fin (N n) := ⟨3 * j.val + 2, by rw [N_eq]; have := j.isLt; omega⟩

lemma auxA_row0 (j : Fin (M n)) : auxA (row0 j) = mul4 j := by
  unfold auxA row0 mul4; congr 2; simp only; omega

lemma auxB_row2 (j : Fin (M n)) : auxB (row2 j) = aff2 j := by
  unfold auxB row2 aff2; congr 2; simp only; omega

lemma row0_injective : Function.Injective (@row0 n) := by
  intro a b h; unfold row0 at h; simp only [Fin.mk.injEq] at h; exact Fin.ext (by omega)

lemma row2_injective : Function.Injective (@row2 n) := by
  intro a b h; unfold row2 at h; simp only [Fin.mk.injEq] at h; exact Fin.ext (by omega)

lemma filter_class0 : (univ.filter fun i : Fin (N n) => i.val % 3 = 0) = univ.map ⟨row0, row0_injective⟩ := by
  ext i
  simp only [mem_filter, mem_univ, true_and, mem_map, Function.Embedding.coeFn_mk]
  constructor
  · intro h
    refine ⟨⟨i.val / 3, ?_⟩, ?_⟩
    · have := lt_of_lt_of_eq i.isLt (N_eq n); omega
    · unfold row0; apply Fin.ext; simp only; omega
  · rintro ⟨j, rfl⟩; unfold row0; simp only; omega

lemma filter_class2 : (univ.filter fun i : Fin (N n) => i.val % 3 = 2) = univ.map ⟨row2, row2_injective⟩ := by
  ext i
  simp only [mem_filter, mem_univ, true_and, mem_map, Function.Embedding.coeFn_mk]
  constructor
  · intro h
    refine ⟨⟨i.val / 3, ?_⟩, ?_⟩
    · have := lt_of_lt_of_eq i.isLt (N_eq n); omega
    · unfold row2; apply Fin.ext; simp only; omega
  · rintro ⟨j, rfl⟩; unfold row2; simp only; omega

lemma sum_class0 (g : Fin (M n) → ℝ) :
    ∑ i : Fin (N n), (if i.val % 3 = 0 then g (auxA i) else 0) = ∑ s, g s := by
  rw [← Finset.sum_filter, filter_class0, Finset.sum_map]
  simp only [Function.Embedding.coeFn_mk, auxA_row0]
  exact mul4_bijective.sum_comp g

lemma sum_class2 (g : Fin (M n) → ℝ) :
    ∑ i : Fin (N n), (if i.val % 3 = 2 then g (auxB i) else 0) = ∑ s, g s := by
  rw [← Finset.sum_filter, filter_class2, Finset.sum_map]
  simp only [Function.Embedding.coeFn_mk, auxB_row2]
  exact aff2_bijective.sum_comp g

lemma lift_injective : Function.Injective (fun x : Fin (M n) × Fin 3 => lift x.1 x.2) := by
  rintro ⟨s, u⟩ ⟨s', u'⟩ h
  unfold lift at h
  simp only [Fin.mk.injEq] at h
  have hs := s.isLt; have hs' := s'.isLt
  fin_cases u <;> fin_cases u' <;> simp at h ⊢ <;> first | exact Fin.ext (by omega) | omega

lemma sum_lifts (c : Fin (N n) → ℝ) : ∑ i, c i = ∑ s, ∑ u : Fin 3, c (lift s u) := by
  have hb : Function.Bijective (fun x : Fin (M n) × Fin 3 => lift x.1 x.2) :=
    ⟨lift_injective, by
      have : Fintype.card (Fin (M n) × Fin 3) = Fintype.card (Fin (N n)) := by
        simp [N_eq']
      exact (Fintype.bijective_iff_injective_and_card _).mpr ⟨lift_injective, this⟩ |>.2⟩
  rw [← Fintype.sum_prod_type', hb.sum_comp (fun i => c i)]

variable {p q r : ℝ}

lemma Fc_split (c : Fin (N n) → ℝ) (i : Fin (N n)) :
    Fc p q r c i = p * c (nu i) + (if i.val % 3 = 0 then q * cbar c (auxA i) else 0)
      + (if i.val % 3 = 2 then r * cbar c (auxB i) else 0) := by
  unfold Fc
  split_ifs <;> first | (exfalso; omega) | ring

/-- **Lemma 6** (summation identity). -/
lemma sum_Fc (c : Fin (N n) → ℝ) :
    ∑ i, Fc p q r c i = p * ∑ i, c i + (q + r) * ∑ s, cbar c s := by
  simp_rw [Fc_split, Finset.sum_add_distrib]
  rw [← Finset.mul_sum, sum_nu]
  have h0 := sum_class0 (n := n) (fun s => q * cbar c s)
  have h2 := sum_class2 (n := n) (fun s => r * cbar c s)
  try simp only at h0 h2
  rw [h0, h2, ← Finset.mul_sum, ← Finset.mul_sum]
  ring

lemma sum_cbar_le (c : Fin (N n) → ℝ) : 3 * ∑ s, cbar c s ≤ ∑ i, c i := by
  rw [sum_lifts, Finset.mul_sum]
  apply Finset.sum_le_sum
  intro s _
  rw [Fin.sum_univ_three]
  linarith [cbar_le c s 0, cbar_le c s 1, cbar_le c s 2]

/-- top-digit invariance: `c` takes the same value on the three lifts of every auxiliary class -/
def TopInv (c : Fin (N n) → ℝ) : Prop := ∀ (s : Fin (M n)) (u : Fin 3), c (lift s u) = c (lift s 0)

lemma topInv_of_sum_eq {c : Fin (N n) → ℝ} (h : 3 * ∑ s, cbar c s = ∑ i, c i) : TopInv c := by
  rw [sum_lifts, Finset.mul_sum, eq_comm, ← sub_eq_zero, ← Finset.sum_sub_distrib] at h
  have hnn : ∀ s ∈ (univ : Finset (Fin (M n))), 0 ≤ ∑ u : Fin 3, c (lift s u) - 3 * cbar c s := by
    intro s _
    rw [Fin.sum_univ_three]
    linarith [cbar_le c s 0, cbar_le c s 1, cbar_le c s 2]
  have h0 := (Finset.sum_eq_zero_iff_of_nonneg hnn).mp h
  intro s u
  have hs := h0 s (mem_univ _)
  rw [Fin.sum_univ_three] at hs
  have a0 := cbar_le c s 0; have a1 := cbar_le c s 1; have a2 := cbar_le c s 2
  fin_cases u <;> simp <;> linarith

end sums

/-! ## descent: a tight, top-digit-invariant point is constant (Lemma 8) -/

section descent
variable {n : ℕ} {p q r : ℝ}

/-- `c` depends only on the index modulo `3^d` -/
def Dep (d : ℕ) (c : Fin (N n) → ℝ) : Prop :=
  ∀ i i' : Fin (N n), i.val ≡ i'.val [MOD 3 ^ d] → c i = c i'

lemma M_dvd_N : M n ∣ N n := ⟨3, N_eq' n⟩

lemma dep_of_topInv {c : Fin (N n) → ℝ} (h : TopInv c) : Dep n c := by
  have key : ∀ x : Fin (N n), c x = c (lift ⟨x.val % M n, Nat.mod_lt _ (M_pos n)⟩ 0) := by
    intro x
    have hx3 : x.val / M n < 3 := by
      have := lt_of_lt_of_eq x.isLt (N_eq' n)
      exact Nat.div_lt_of_lt_mul this
    have hx : x = lift ⟨x.val % M n, Nat.mod_lt _ (M_pos n)⟩ ⟨x.val / M n, hx3⟩ := by
      unfold lift; apply Fin.ext; simp only; exact (Nat.mod_add_div _ _).symm
    conv_lhs => rw [hx]
    exact h _ _
  intro i i' hii
  rw [key i, key i']
  congr 2
  exact Fin.ext hii

/-- the integer-lifting step: `x ≡ y [MOD P]` gives `y ≡ x + a P [MOD 3P]` with `a < 3` -/
lemma exists_shift (P x y : ℕ) (h : x ≡ y [MOD P]) : ∃ a, a < 3 ∧ y ≡ x + a * P [MOD 3 * P] := by
  obtain ⟨m, hm⟩ := (Nat.modEq_iff_dvd.mp h)
  refine ⟨(m % 3).toNat, ?_, ?_⟩
  · have h1 : m % 3 < 3 := Int.emod_lt_of_pos m (by norm_num)
    have h2 : 0 ≤ m % 3 := Int.emod_nonneg m (by norm_num)
    omega
  · apply Nat.modEq_of_dvd
    have h2 : 0 ≤ m % 3 := Int.emod_nonneg m (by norm_num)
    have h3 : ((m % 3).toNat : ℤ) = m % 3 := Int.toNat_of_nonneg h2
    refine ⟨-(m / 3), ?_⟩
    push_cast
    rw [h3]
    have h4 := Int.emod_add_mul_ediv m 3
    linear_combination (-1 : ℤ) * hm + (P : ℤ) * h4

lemma descent_step {c : Fin (N n) → ℝ} (hq : q ≠ 0)
    (htight : ∀ i : Fin (N n), i.val % 3 = 0 → Fc p q r c i = c i)
    {e : ℕ} (he : e + 1 ≤ n) (hD : Dep (e + 1) c) : Dep e c := by
  have hQM : 3 ^ (e + 1) ∣ M n := pow_dvd_pow 3 he
  have hQN : 3 ^ (e + 1) ∣ N n := hQM.trans M_dvd_N
  have hPM : 3 ^ e ∣ M n := pow_dvd_pow 3 (by omega)
  have hQ : 3 ^ (e + 1) = 3 * 3 ^ e := by ring
  -- the minimum over the lifts is the value at any lift
  have hcbar : ∀ s : Fin (M n), cbar c s = c (lift s 0) := by
    intro s
    have hl : ∀ u : Fin 3, c (lift s u) = c (lift s 0) := by
      intro u
      apply hD
      unfold lift
      simp only [Fin.val_zero, mul_zero, add_zero]
      have : M n * u.val ≡ 0 [MOD 3 ^ (e + 1)] := Nat.modEq_zero_iff_dvd.mpr (dvd_mul_of_dvd_left hQM _)
      simpa using this.add_left s.val
    unfold cbar
    rw [hl 1, hl 2]
    simp
  -- shifting by 3^e does not change c
  have hshift : ∀ t t' : Fin (N n), t'.val ≡ t.val + 3 ^ e [MOD 3 ^ (e + 1)] → c t = c t' := by
    intro t t' htt
    obtain ⟨j, hj⟩ := mul4_bijective.2 (⟨t.val % M n, Nat.mod_lt _ (M_pos n)⟩ : Fin (M n))
    set j' : Fin (M n) := ⟨(j.val + 3 ^ e) % M n, Nat.mod_lt _ (M_pos n)⟩ with hj'def
    have e0 := htight (row0 j) (by unfold row0; simp)
    have e1 := htight (row0 j') (by unfold row0; simp)
    rw [Fc_split, auxA_row0] at e0 e1
    have c0 : (row0 j).val % 3 = 0 := by unfold row0; simp
    have c1 : (row0 j').val % 3 = 0 := by unfold row0; simp
    simp only [c0, c1, if_true, show ¬ (0 = 2) from by norm_num, if_false, add_zero] at e0 e1
    have hjj : j'.val ≡ j.val + 3 ^ e [MOD M n] := Nat.mod_modEq _ _
    have hjjQ : j'.val ≡ j.val + 3 ^ e [MOD 3 ^ (e + 1)] := hjj.of_dvd hQM
    have hjjP : j'.val ≡ j.val [MOD 3 ^ e] := by
      have := hjj.of_dvd hPM
      exact this.trans (by simp [Nat.ModEq])
    have hrow : (row0 j').val ≡ (row0 j).val [MOD 3 ^ (e + 1)] := by
      unfold row0; simp only
      rw [hQ]; exact hjjP.mul_left' 3
    have hnu : (nu (row0 j')).val ≡ (nu (row0 j)).val [MOD 3 ^ (e + 1)] := by
      unfold nu; simp only
      have a1 := (Nat.mod_modEq (4 * (row0 j').val + 2) (N n)).of_dvd hQN
      have a2 := (Nat.mod_modEq (4 * (row0 j).val + 2) (N n)).of_dvd hQN
      exact a1.trans (((hrow.mul_left 4).add_right 2).trans a2.symm)
    have hc_row : c (row0 j') = c (row0 j) := hD _ _ hrow
    have hc_nu : c (nu (row0 j')) = c (nu (row0 j)) := hD _ _ hnu
    have hcb : cbar c (mul4 j) = cbar c (mul4 j') := by
      rw [hc_nu, hc_row] at e1
      have : q * cbar c (mul4 j) = q * cbar c (mul4 j') := by linarith
      exact mul_left_cancel₀ hq this
    rw [hcbar, hcbar] at hcb
    have ht0 : c t = c (lift (mul4 j) 0) := by
      rw [hj]; apply hD; unfold lift; simp only [Fin.val_zero, mul_zero, add_zero]
      exact ((Nat.mod_modEq t.val (M n)).of_dvd hQM).symm
    have ht1 : c (lift (mul4 j') 0) = c t' := by
      apply hD; unfold lift mul4; simp only [Fin.val_zero, mul_zero, add_zero]
      have b1 := (Nat.mod_modEq (4 * j'.val) (M n)).of_dvd hQM
      have b2 : 4 * j'.val ≡ 4 * (j.val + 3 ^ e) [MOD 3 ^ (e + 1)] := hjjQ.mul_left 4
      have b4 : 4 * j.val ≡ t.val [MOD 3 ^ (e + 1)] := by
        have : 4 * j.val ≡ t.val [MOD M n] := by
          have h := congrArg Fin.val hj; unfold mul4 at h; simp only at h
          exact h
        exact this.of_dvd hQM
      have b5 : 4 * (j.val + 3 ^ e) = 4 * j.val + 3 ^ e + 3 ^ (e + 1) := by ring
      have b6 : 4 * j.val + 3 ^ e + 3 ^ (e + 1) ≡ t.val + 3 ^ e + 0 [MOD 3 ^ (e + 1)] :=
        (b4.add_right _).add (Nat.modEq_zero_iff_dvd.mpr dvd_rfl)
      rw [b5] at b2
      simp only [add_zero] at b6
      exact b1.trans (b2.trans (b6.trans htt.symm))
    rw [ht0, hcb, ht1]
  -- conclude
  intro i i' hii
  obtain ⟨a, ha, hia⟩ := exists_shift (3 ^ e) i.val i'.val hii
  rw [← hQ] at hia
  interval_cases a
  · exact hD _ _ (by simpa using hia.symm)
  · exact hshift _ _ (by simpa using hia)
  · let t1 : Fin (N n) := ⟨(i.val + 3 ^ e) % N n, Nat.mod_lt _ (N_pos n)⟩
    have h1 : t1.val ≡ i.val + 3 ^ e [MOD 3 ^ (e + 1)] := (Nat.mod_modEq _ _).of_dvd hQN
    have h2 : i'.val ≡ t1.val + 3 ^ e [MOD 3 ^ (e + 1)] := by
      have := h1.add_right (3 ^ e)
      rw [show i.val + 3 ^ e + 3 ^ e = i.val + 2 * 3 ^ e by ring] at this
      exact hia.trans this.symm
    exact (hshift i t1 h1).trans (hshift t1 i' h2)

/-- **Lemma 8.** A point whose class-0 rows are tight and which is top-digit invariant is constant. -/
theorem const_of_topInv {c : Fin (N n) → ℝ} (hq : q ≠ 0)
    (htight : ∀ i : Fin (N n), i.val % 3 = 0 → Fc p q r c i = c i) (h : TopInv c) :
    ∀ i i' : Fin (N n), c i = c i' := by
  have key : ∀ m, m ≤ n → Dep (n - m) c := by
    intro m
    induction m with
    | zero => intro _; simpa using dep_of_topInv h
    | succ m ih =>
      intro hm
      have h1 := ih (by omega)
      have h2 : n - m = (n - (m + 1)) + 1 := by omega
      rw [h2] at h1
      exact descent_step hq htight (by omega) h1
  have h0 := key n le_rfl
  simp only [Nat.sub_self] at h0
  exact fun i i' => h0 i i' Nat.modEq_one

/-- the class-1 row `1` (`m = 5`) -/
def row1 : Fin (N n) := ⟨1, by unfold N; have : 3 ≤ 3 ^ (n + 1) := Nat.le_self_pow (by omega) 3; omega⟩

/-- a positive constant vector cannot satisfy the class-1 row with equality unless `p = 1` -/
theorem p_eq_one_of_const {c : Fin (N n) → ℝ} (hpos : ∀ i, 0 < c i) (hconst : ∀ i i', c i = c i')
    (htight : Fc p q r c row1 = c row1) : p = 1 := by
  rw [Fc_split] at htight
  have c1 : (row1 : Fin (N n)).val % 3 = 1 := by unfold row1; simp
  simp only [c1, show ¬ ((1 : ℕ) = 0) from by norm_num, show ¬ ((1 : ℕ) = 2) from by norm_num,
    if_false, add_zero] at htight
  rw [hconst (nu row1) row1] at htight
  have := hpos row1
  have : (p - 1) * c row1 = 0 := by linarith
  rcases mul_eq_zero.mp this with h | h
  · linarith
  · linarith

end descent

/-! ## tiling a level-`k` vector to level `k+1` (Lemma 9) -/

section tiling
variable {n : ℕ} {p q r : ℝ}

lemma N_succ (n : ℕ) : N (n + 1) = 3 * N n := by unfold N; ring
lemma M_succ (n : ℕ) : M (n + 1) = N n := by unfold M N; rfl

/-- the level-`k` index of a level-`(k+1)` index (forget the top digit) -/
def proj (i : Fin (N (n + 1))) : Fin (N n) := ⟨i.val % N n, Nat.mod_lt _ (N_pos n)⟩

/-- `tile c` is `c` repeated three times (`np.tile(c, 3)`) -/
def tile (c : Fin (N n) → ℝ) : Fin (N (n + 1)) → ℝ := fun i => c (proj i)

lemma N_dvd_succ : N n ∣ N (n + 1) := ⟨3, by rw [N_succ]; ring⟩

lemma proj_nu (i : Fin (N (n + 1))) : proj (nu i) = nu (proj i) := by
  unfold proj nu; apply Fin.ext; simp only
  rw [Nat.mod_mod_of_dvd _ N_dvd_succ]
  exact ((Nat.mod_modEq i.val (N n)).symm.mul_left 4).add_right 2

lemma proj_class (i : Fin (N (n + 1))) : (proj i).val % 3 = i.val % 3 := by
  unfold proj; simp only
  exact Nat.mod_mod_of_dvd _ (by unfold N; exact dvd_pow_self 3 (by omega))

lemma cbar_le_self (c : Fin (N n) → ℝ) (x : Fin (N n)) :
    cbar c ⟨x.val % M n, Nat.mod_lt _ (M_pos n)⟩ ≤ c x := by
  have hx3 : x.val / M n < 3 := Nat.div_lt_of_lt_mul (lt_of_lt_of_eq x.isLt (N_eq' n))
  have hx : x = lift ⟨x.val % M n, Nat.mod_lt _ (M_pos n)⟩ ⟨x.val / M n, hx3⟩ := by
    unfold lift; apply Fin.ext; simp only; exact (Nat.mod_add_div _ _).symm
  conv_rhs => rw [hx]
  exact cbar_le c _ _

/-- the index `s` of level `k+1`'s auxiliary vector, read as a level-`k` index -/
def up (s : Fin (M (n + 1))) : Fin (N n) := ⟨s.val, lt_of_lt_of_eq s.isLt (M_succ n)⟩

lemma proj_lift (s : Fin (M (n + 1))) (u : Fin 3) : proj (lift s u) = up s := by
  unfold proj lift up; apply Fin.ext; simp only
  rw [show M (n + 1) * u.val = N n * u.val from by rw [M_succ], Nat.add_mul_mod_self_left]
  exact Nat.mod_eq_of_lt (lt_of_lt_of_eq s.isLt (M_succ n))

lemma cbar_tile (c : Fin (N n) → ℝ) (s : Fin (M (n + 1))) : cbar (tile c) s = c (up s) := by
  unfold cbar tile; rw [proj_lift, proj_lift, proj_lift]; simp

lemma div3_proj (i : Fin (N (n + 1))) : i.val / 3 = (proj i).val / 3 + M n * (i.val / N n) := by
  unfold proj; simp only
  conv_lhs => rw [← Nat.mod_add_div i.val (N n)]
  rw [N_eq n, mul_assoc, Nat.add_mul_div_left _ _ (by norm_num : 0 < 3)]

lemma auxA_up (i : Fin (N (n + 1))) : (up (auxA i)).val % M n = (auxA (proj i)).val := by
  unfold up auxA; simp only
  rw [M_succ, Nat.mod_mod_of_dvd _ M_dvd_N, div3_proj, mul_add, ← mul_assoc, mul_comm 4 (M n),
    mul_assoc, Nat.add_mul_mod_self_left]

lemma auxB_up (i : Fin (N (n + 1))) : (up (auxB i)).val % M n = (auxB (proj i)).val := by
  unfold up auxB; simp only
  rw [M_succ, Nat.mod_mod_of_dvd _ M_dvd_N, div3_proj, mul_add, ← mul_assoc, mul_comm 2 (M n),
    mul_assoc, add_right_comm, Nat.add_mul_mod_self_left]

lemma cbar_le_tile_A (c : Fin (N n) → ℝ) (i : Fin (N (n + 1))) :
    cbar c (auxA (proj i)) ≤ cbar (tile c) (auxA i) := by
  rw [cbar_tile]
  have := cbar_le_self c (up (auxA i))
  have he : (⟨(up (auxA i)).val % M n, Nat.mod_lt _ (M_pos n)⟩ : Fin (M n)) = auxA (proj i) :=
    Fin.ext (auxA_up i)
  rwa [he] at this

lemma cbar_le_tile_B (c : Fin (N n) → ℝ) (i : Fin (N (n + 1))) :
    cbar c (auxB (proj i)) ≤ cbar (tile c) (auxB i) := by
  rw [cbar_tile]
  have := cbar_le_self c (up (auxB i))
  have he : (⟨(up (auxB i)).val % M n, Nat.mod_lt _ (M_pos n)⟩ : Fin (M n)) = auxB (proj i) :=
    Fin.ext (auxB_up i)
  rwa [he] at this

/-- **Lemma 9** (pointwise part): tiling never loses. -/
lemma tile_ge (hq : 0 ≤ q) (hr : 0 ≤ r) (c : Fin (N n) → ℝ) (i : Fin (N (n + 1))) :
    Fc p q r c (proj i) ≤ Fc p q r (tile c) i := by
  rw [Fc_split, Fc_split, proj_class]
  have h1 : tile c (nu i) = c (nu (proj i)) := by unfold tile; rw [proj_nu]
  rw [h1]
  have hA := mul_le_mul_of_nonneg_left (cbar_le_tile_A c i) hq
  have hB := mul_le_mul_of_nonneg_left (cbar_le_tile_B c i) hr
  split_ifs <;> linarith

lemma sum_up (g : Fin (N n) → ℝ) : ∑ s : Fin (M (n + 1)), g (up s) = ∑ x, g x :=
  Fintype.sum_equiv (finCongr (M_succ n)) _ _ (fun s => by congr 1)

lemma sum_proj (g : Fin (N n) → ℝ) : ∑ i : Fin (N (n + 1)), g (proj i) = 3 * ∑ x, g x := by
  rw [sum_lifts]
  simp only [proj_lift, Fin.sum_univ_three]
  rw [← sum_up g, Finset.mul_sum]
  apply Finset.sum_congr rfl; intro s _; ring

lemma sum_tile_gain (c : Fin (N n) → ℝ) :
    ∑ i : Fin (N (n + 1)), (Fc p q r (tile c) i - Fc p q r c (proj i))
      = (q + r) * (∑ x, c x - 3 * ∑ s, cbar c s) := by
  rw [Finset.sum_sub_distrib, sum_Fc, sum_proj (fun x => Fc p q r c x), sum_Fc]
  have h1 : ∑ i : Fin (N (n + 1)), tile c i = 3 * ∑ x, c x := sum_proj c
  have h2 : ∑ s : Fin (M (n + 1)), cbar (tile c) s = ∑ x, c x := by
    simp only [cbar_tile]; exact sum_up c
  rw [h1, h2]; ring

/-- **Lemma 9** (strict part): if `c` is not top-digit invariant, tiling gains strictly somewhere. -/
lemma exists_tile_strict (hq : 0 ≤ q) (hr : 0 ≤ r) (hqr : 0 < q + r) {c : Fin (N n) → ℝ}
    (h : ¬ TopInv c) : ∃ i : Fin (N (n + 1)), Fc p q r c (proj i) < Fc p q r (tile c) i := by
  by_contra hcon
  simp only [not_exists, not_lt] at hcon
  have heq : ∀ i, Fc p q r (tile c) i - Fc p q r c (proj i) = 0 := fun i =>
    le_antisymm (by linarith [hcon i]) (by linarith [tile_ge (p := p) hq hr c i])
  have hsum := sum_tile_gain (p := p) (q := q) (r := r) c
  simp only [heq, Finset.sum_const_zero] at hsum
  have h3 : ∑ x, c x - 3 * ∑ s, cbar c s = 0 := by
    rcases mul_eq_zero.mp hsum.symm with h0 | h0
    · linarith
    · exact h0
  exact h (topInv_of_sum_eq (by linarith))

end tiling

/-! ## the Krasikov–Lagarias coefficients and the main theorems -/

section main
open Filter Topology

/-- `α = log₂ 3` -/
noncomputable def α : ℝ := Real.logb 2 3

noncomputable def pc (lam : ℝ) : ℝ := lam⁻¹ ^ 2
noncomputable def qc (lam : ℝ) : ℝ := lam ^ (α - 2)
noncomputable def rc (lam : ℝ) : ℝ := lam ^ (α - 1)

/-- The right-hand side of `L^NT_k(λ)`, `k = n + 2`:
`F(c)_m = λ^-2 c_{4m} + [m ≡ 2 (9)] λ^(α-2) c̄_{(4m-2)/3} + [m ≡ 8 (9)] λ^(α-1) c̄_{(2m-1)/3}`. -/
noncomputable def F (n : ℕ) (lam : ℝ) (c : Fin (N n) → ℝ) : Fin (N n) → ℝ :=
  Fc (pc lam) (qc lam) (rc lam) c

/-- `L^NT_k(λ)` has a (strictly positive) feasible solution -/
def Feasible (n : ℕ) (lam : ℝ) : Prop :=
  ∃ c : Fin (N n) → ℝ, (∀ i, 0 < c i) ∧ ∀ i, c i ≤ F n lam c i

/-- the admissible parameters in `[1, 2]` (the range of Krasikov–Lagarias, Theorem 2.2) -/
def Lam (n : ℕ) : Set ℝ := {lam | 1 ≤ lam ∧ lam ≤ 2 ∧ Feasible n lam}

/-- `λ_k = sup Λ_k` for `k = n + 2` -/
noncomputable def lamk (n : ℕ) : ℝ := sSup (Lam n)

lemma pc_pos {lam : ℝ} (h : 0 < lam) : 0 < pc lam := by unfold pc; positivity
lemma qc_pos {lam : ℝ} (h : 0 < lam) : 0 < qc lam := Real.rpow_pos_of_pos h _
lemma rc_pos {lam : ℝ} (h : 0 < lam) : 0 < rc lam := Real.rpow_pos_of_pos h _

lemma two_rpow_alpha : (2 : ℝ) ^ α = 3 := Real.rpow_logb (by norm_num) (by norm_num) (by norm_num)

lemma pc_two : pc 2 = 1 / 4 := by unfold pc; norm_num
lemma qc_two : qc 2 = 3 / 4 := by
  unfold qc; rw [Real.rpow_sub (by norm_num), two_rpow_alpha]; norm_num
lemma rc_two : rc 2 = 3 / 2 := by
  unfold rc; rw [Real.rpow_sub (by norm_num), two_rpow_alpha]; norm_num
lemma pc_one : pc 1 = 1 := by unfold pc; norm_num
lemma qc_one : qc 1 = 1 := by unfold qc; simp

lemma pc_eq_one {lam : ℝ} (h : 0 < lam) (h1 : pc lam = 1) : lam = 1 := by
  unfold pc at h1
  have h2 : lam⁻¹ = 1 := (pow_eq_one_iff_of_nonneg (inv_nonneg.mpr h.le) (by norm_num)).mp h1
  exact inv_eq_one.mp h2

lemma continuousAt_F {n : ℕ} {lam0 : ℝ} (h0 : 0 < lam0) (z : Fin (N n) → ℝ) (i : Fin (N n)) :
    ContinuousAt (fun lam => F n lam z i) lam0 := by
  have hp : ContinuousAt pc lam0 := ((continuousAt_inv₀ h0.ne').pow 2)
  have hq : ContinuousAt qc lam0 := Real.continuousAt_rpow_const _ _ (Or.inl h0.ne')
  have hr : ContinuousAt rc lam0 := Real.continuousAt_rpow_const _ _ (Or.inl h0.ne')
  unfold F
  simp_rw [Fc_split]
  apply ContinuousAt.add
  · apply ContinuousAt.add (hp.mul continuousAt_const)
    split_ifs
    · exact hq.mul continuousAt_const
    · exact continuousAt_const
  · split_ifs
    · exact hr.mul continuousAt_const
    · exact continuousAt_const

/-- **Lemma 5** (openness). -/
lemma open_strict {n : ℕ} {lam0 : ℝ} (h0 : 0 < lam0) {z : Fin (N n) → ℝ}
    (hz : ∀ i, z i < F n lam0 z i) : ∃ δ > 0, ∀ lam, |lam - lam0| < δ → ∀ i, z i < F n lam z i := by
  have h1 : ∀ i, ∀ᶠ lam in 𝓝 lam0, z i < F n lam z i := fun i =>
    continuousAt_const.eventually_lt (continuousAt_F h0 z i) (hz i)
  have hall : ∀ᶠ lam in 𝓝 lam0, ∀ i, z i < F n lam z i := Filter.eventually_all.mpr h1
  obtain ⟨δ, hδ, hball⟩ := Metric.eventually_nhds_iff.mp hall
  exact ⟨δ, hδ, fun lam hl => hball (by rwa [Real.dist_eq])⟩

/-- a strict sub-solution at `λ₀ < 2` gives an admissible parameter above `λ₀` -/
lemma exists_mem_above {n : ℕ} {lam0 : ℝ} (h1 : 1 ≤ lam0) (h2 : lam0 < 2) {z : Fin (N n) → ℝ}
    (hzpos : ∀ i, 0 < z i) (hz : ∀ i, z i < F n lam0 z i) : ∃ lam ∈ Lam n, lam0 < lam := by
  obtain ⟨δ, hδ, hball⟩ := open_strict (by linarith) hz
  set lam := lam0 + min (δ / 2) ((2 - lam0) / 2) with hlam
  have hm1 : 0 < min (δ / 2) ((2 - lam0) / 2) := lt_min (by linarith) (by linarith)
  have hm2 : min (δ / 2) ((2 - lam0) / 2) ≤ δ / 2 := min_le_left _ _
  have hm3 : min (δ / 2) ((2 - lam0) / 2) ≤ (2 - lam0) / 2 := min_le_right _ _
  refine ⟨lam, ⟨by linarith, by linarith, z, hzpos, fun i => ?_⟩, by linarith⟩
  have := hball lam (by rw [abs_lt]; constructor <;> linarith) i
  exact this.le

lemma one_mem (n : ℕ) : (1 : ℝ) ∈ Lam n := by
  refine ⟨le_rfl, by norm_num, fun _ => 1, fun _ => one_pos, fun i => ?_⟩
  have := Fc_ge (p := pc 1) (qc_pos one_pos).le (rc_pos one_pos).le (x := fun _ : Fin (N n) => (1 : ℝ))
    (fun _ => zero_le_one) i
  rw [pc_one] at this
  show (1 : ℝ) ≤ Fc (pc 1) (qc 1) (rc 1) (fun _ => 1) i
  rw [pc_one]; linarith

lemma bddAbove_Lam (n : ℕ) : BddAbove (Lam n) := ⟨2, fun _ h => h.2.1⟩

lemma le_lamk {n : ℕ} {lam : ℝ} (h : lam ∈ Lam n) : lam ≤ lamk n := le_csSup (bddAbove_Lam n) h

/-- `λ = 1` admits slack, so `λ_k > 1`. -/
theorem one_lt_lamk (n : ℕ) : 1 < lamk n := by
  have hp := pc_pos (one_pos : (0 : ℝ) < 1)
  have hq := qc_pos (one_pos : (0 : ℝ) < 1)
  have hr := rc_pos (one_pos : (0 : ℝ) < 1)
  set x : Fin (N n) → ℝ := fun _ => 1
  have hx : ∀ i, x i ≤ Fc (pc 1) (qc 1) (rc 1) x i := fun i => by
    have := Fc_ge (p := pc 1) hq.le hr.le (x := x) (fun _ => zero_le_one) i
    simp only [x, pc_one] at this ⊢; linarith
  have hj : x (row0 (0 : Fin (M n))) < Fc (pc 1) (qc 1) (rc 1) x (row0 0) := by
    rw [Fc_split]
    have c0 : (row0 (0 : Fin (M n))).val % 3 = 0 := by unfold row0; simp
    simp only [c0, if_true, show ¬ ((0 : ℕ) = 2) from by norm_num, if_false, add_zero, x, pc_one, qc_one]
    unfold cbar; simp
  obtain ⟨z, hzpos, hz⟩ := exists_strict hp hq.le hr.le (fun _ => one_pos) hx hj
  obtain ⟨lam, hlam, hlt⟩ := exists_mem_above (n := n) le_rfl (by norm_num) hzpos hz
  exact lt_of_lt_of_le hlt (le_lamk hlam)

/-- At `λ = 2` the program is infeasible (summation + descent). -/
theorem not_feasible_two (n : ℕ) : ¬ Feasible n 2 := by
  rintro ⟨c, hpos, hc⟩
  have hsum := sum_Fc (p := pc 2) (q := qc 2) (r := rc 2) c
  rw [pc_two, qc_two, rc_two] at hsum
  have hle := sum_cbar_le c
  have hge : ∑ i, c i ≤ ∑ i, F n 2 c i := Finset.sum_le_sum fun i _ => hc i
  unfold F at hge
  rw [pc_two, qc_two, rc_two] at hge
  -- all inequalities are equalities
  have hsum2 : 3 * ∑ s, cbar c s = ∑ i, c i := by linarith
  have htight : ∀ i, Fc (pc 2) (qc 2) (rc 2) c i = c i := by
    have h0 : ∑ i, (Fc (1 / 4) (3 / 4) (3 / 2) c i - c i) = 0 := by
      rw [Finset.sum_sub_distrib]; linarith
    have hnn : ∀ i ∈ (Finset.univ : Finset (Fin (N n))), 0 ≤ Fc (1 / 4) (3 / 4) (3 / 2) c i - c i := by
      intro i _; have := hc i; unfold F at this; rw [pc_two, qc_two, rc_two] at this; linarith
    intro i
    have := (Finset.sum_eq_zero_iff_of_nonneg hnn).mp h0 i (Finset.mem_univ _)
    rw [pc_two, qc_two, rc_two]; linarith
  have htop := topInv_of_sum_eq hsum2
  have hconst := const_of_topInv (p := pc 2) (q := qc 2) (r := rc 2) (by rw [qc_two]; norm_num)
    (fun i _ => htight i) htop
  have h1 := p_eq_one_of_const hpos hconst (htight row1)
  rw [pc_two] at h1; norm_num at h1

/-- passing to the limit in `x ≤ F_λ x` -/
lemma tendsto_F {n : ℕ} {L : ℝ} (hL : 0 < L) {lam : ℕ → ℝ} {x : ℕ → Fin (N n) → ℝ}
    {xl : Fin (N n) → ℝ} (hlam : Tendsto lam atTop (𝓝 L)) (hx : Tendsto x atTop (𝓝 xl))
    (i : Fin (N n)) : Tendsto (fun k => F n (lam k) (x k) i) atTop (𝓝 (F n L xl i)) := by
  have hp : Tendsto (fun k => pc (lam k)) atTop (𝓝 (pc L)) :=
    ((continuousAt_inv₀ hL.ne').pow 2).tendsto.comp hlam
  have hq : Tendsto (fun k => qc (lam k)) atTop (𝓝 (qc L)) :=
    (Real.continuousAt_rpow_const _ _ (Or.inl hL.ne')).tendsto.comp hlam
  have hr : Tendsto (fun k => rc (lam k)) atTop (𝓝 (rc L)) :=
    (Real.continuousAt_rpow_const _ _ (Or.inl hL.ne')).tendsto.comp hlam
  have hxi : ∀ j, Tendsto (fun k => x k j) atTop (𝓝 (xl j)) := fun j => (tendsto_pi_nhds.mp hx) j
  have hcb : ∀ s, Tendsto (fun k => cbar (x k) s) atTop (𝓝 (cbar xl s)) := by
    intro s; unfold cbar
    exact (hxi _).min ((hxi _).min (hxi _))
  unfold F
  simp_rw [Fc_split]
  apply Tendsto.add
  · apply Tendsto.add (hp.mul (hxi _))
    split_ifs
    · exact hq.mul (hcb _)
    · exact tendsto_const_nhds
  · split_ifs
    · exact hr.mul (hcb _)
    · exact tendsto_const_nhds

/-- **Theorem (i), attainment.** `λ_k ∈ Λ_k`. -/
theorem lamk_mem (n : ℕ) : lamk n ∈ Lam n := by
  have hne : (Lam n).Nonempty := ⟨1, one_mem n⟩
  obtain ⟨u, -, hu, humem⟩ := exists_seq_tendsto_sSup hne (bddAbove_Lam n)
  have hL1 : 1 ≤ lamk n := le_lamk (one_mem n)
  have hL2 : lamk n ≤ 2 := csSup_le hne (fun _ h => h.2.1)
  have hL0 : 0 < lamk n := by linarith
  choose c hcpos hcfeas using fun k => (humem k).2.2
  set S : ℕ → ℝ := fun k => ∑ i, c k i with hS
  have hSpos : ∀ k, 0 < S k := fun k => Finset.sum_pos (fun i _ => hcpos k i) Finset.univ_nonempty
  set x : ℕ → Fin (N n) → ℝ := fun k => (S k)⁻¹ • c k with hx
  have hxfeas : ∀ k i, x k i ≤ F n (u k) (x k) i := by
    intro k i
    have ht : 0 ≤ (S k)⁻¹ := (inv_pos.mpr (hSpos k)).le
    simp only [hx, F]
    rw [Fc_smul ht]
    simp only [Pi.smul_apply, smul_eq_mul]
    exact mul_le_mul_of_nonneg_left (hcfeas k i) ht
  have hxsum : ∀ k, ∑ i, x k i = 1 := by
    intro k; simp only [hx, Pi.smul_apply, smul_eq_mul]
    rw [← Finset.mul_sum]; exact inv_mul_cancel₀ (hSpos k).ne'
  have hxmem : ∀ k, x k ∈ Set.Icc (0 : Fin (N n) → ℝ) 1 := by
    intro k
    constructor
    · intro i; simp only [hx, Pi.smul_apply, smul_eq_mul, Pi.zero_apply]
      exact mul_nonneg (inv_pos.mpr (hSpos k)).le (hcpos k i).le
    · intro i
      have hle : c k i ≤ S k := Finset.single_le_sum (fun j _ => (hcpos k j).le) (Finset.mem_univ i)
      simp only [hx, Pi.smul_apply, smul_eq_mul, Pi.one_apply]
      rw [inv_mul_le_iff₀ (hSpos k)]; linarith
  obtain ⟨xl, hxl, φ, hφ, hlim⟩ := isCompact_Icc.tendsto_subseq hxmem
  have hu' : Tendsto (u ∘ φ) atTop (𝓝 (lamk n)) := hu.comp hφ.tendsto_atTop
  have hlimF : ∀ i, xl i ≤ F n (lamk n) xl i := by
    intro i
    have h1 : Tendsto (fun k => (x ∘ φ) k i) atTop (𝓝 (xl i)) := (tendsto_pi_nhds.mp hlim) i
    have h2 := tendsto_F hL0 hu' hlim i
    exact le_of_tendsto_of_tendsto' h1 h2 (fun k => hxfeas (φ k) i)
  have hxlnn : ∀ i, 0 ≤ xl i := fun i => hxl.1 i
  have hxlsum : ∑ i, xl i = 1 := by
    have h1 : Tendsto (fun k => ∑ i, (x ∘ φ) k i) atTop (𝓝 (∑ i, xl i)) :=
      tendsto_finset_sum _ (fun i _ => (tendsto_pi_nhds.mp hlim) i)
    have h2 : (fun k => ∑ i, (x ∘ φ) k i) = fun _ => (1 : ℝ) := by
      funext k; exact hxsum (φ k)
    rw [h2] at h1
    exact tendsto_nhds_unique h1 tendsto_const_nhds
  obtain ⟨j, hj⟩ : ∃ j, 0 < xl j := by
    by_contra hcon
    simp only [not_exists, not_lt] at hcon
    have : ∑ i, xl i ≤ 0 := Finset.sum_nonpos (fun i _ => hcon i)
    linarith
  obtain ⟨z, hzpos, hz⟩ := exists_pos (pc_pos hL0) (qc_pos hL0).le (rc_pos hL0).le hxlnn hlimF hj
  exact ⟨hL1, hL2, z, hzpos, hz⟩

/-- **Theorem (i).** `1 < λ_k < 2`. -/
theorem lamk_lt_two (n : ℕ) : lamk n < 2 := by
  have h := lamk_mem n
  rcases lt_or_eq_of_le h.2.1 with h2 | h2
  · exact h2
  · exfalso; rw [h2] at h; exact not_feasible_two n h.2.2

/-- **Theorem (ii), tightness.** Every feasible point at `λ_k` satisfies all inequalities with equality. -/
theorem tight {n : ℕ} {c : Fin (N n) → ℝ} (hpos : ∀ i, 0 < c i) (hc : ∀ i, c i ≤ F n (lamk n) c i) :
    ∀ i, F n (lamk n) c i = c i := by
  have hL0 : 0 < lamk n := by linarith [one_lt_lamk n]
  by_contra hcon
  simp only [not_forall] at hcon
  obtain ⟨j, hj⟩ := hcon
  have hj' : c j < F n (lamk n) c j := lt_of_le_of_ne (hc j) (Ne.symm hj)
  obtain ⟨z, hzpos, hz⟩ := exists_strict (pc_pos hL0) (qc_pos hL0).le (rc_pos hL0).le hpos hc hj'
  obtain ⟨lam, hlam, hlt⟩ := exists_mem_above (one_lt_lamk n).le (lamk_lt_two n) hzpos hz
  linarith [le_lamk hlam]

/-- **Theorem (ii), uniqueness.** -/
theorem unique {n : ℕ} {c c' : Fin (N n) → ℝ} (hpos : ∀ i, 0 < c i) (hc : ∀ i, c i ≤ F n (lamk n) c i)
    (hpos' : ∀ i, 0 < c' i) (hc' : ∀ i, c' i ≤ F n (lamk n) c' i) : ∃ t : ℝ, 0 < t ∧ c' = t • c := by
  have hL0 : 0 < lamk n := by linarith [one_lt_lamk n]
  exact fixed_unique (pc_pos hL0) (qc_pos hL0).le (rc_pos hL0).le hpos hpos' (tight hpos hc) (tight hpos' hc')

/-- a tight point at `λ_k` is not top-digit invariant -/
lemma not_topInv {n : ℕ} {c : Fin (N n) → ℝ} (hpos : ∀ i, 0 < c i) (hc : ∀ i, c i ≤ F n (lamk n) c i) :
    ¬ TopInv c := by
  intro htop
  have hL0 : 0 < lamk n := by linarith [one_lt_lamk n]
  have ht := tight hpos hc
  have hconst := const_of_topInv (p := pc (lamk n)) (q := qc (lamk n)) (r := rc (lamk n))
    (qc_pos hL0).ne' (fun i _ => ht i) htop
  have h1 := p_eq_one_of_const hpos hconst (ht row1)
  have := pc_eq_one hL0 h1
  linarith [one_lt_lamk n]

/-- **Theorem (iii).** `λ_k < λ_{k+1}`. -/
theorem lamk_lt_succ (n : ℕ) : lamk n < lamk (n + 1) := by
  have hL0 : 0 < lamk n := by linarith [one_lt_lamk n]
  obtain ⟨-, -, c, hpos, hc⟩ := lamk_mem n
  have ht := tight hpos hc
  have hnt := not_topInv hpos hc
  have hp := pc_pos hL0; have hq := qc_pos hL0; have hr := rc_pos hL0
  set x : Fin (N (n + 1)) → ℝ := tile c
  have hxpos : ∀ i, 0 < x i := fun i => hpos _
  have hx : ∀ i, x i ≤ F (n + 1) (lamk n) x i := by
    intro i
    have h1 := tile_ge (p := pc (lamk n)) hq.le hr.le c i
    have h2 := ht (proj i)
    unfold F at h2 ⊢
    simp only [x, tile] at h1 ⊢
    linarith
  obtain ⟨j, hj⟩ := exists_tile_strict (p := pc (lamk n)) hq.le hr.le (by linarith) hnt
  have hj' : x j < F (n + 1) (lamk n) x j := by
    have h2 := ht (proj j)
    unfold F at h2 ⊢
    simp only [x, tile] at hj ⊢
    linarith
  obtain ⟨z, hzpos, hz⟩ := exists_strict hp hq.le hr.le hxpos hx hj'
  obtain ⟨lam, hlam, hlt⟩ := exists_mem_above (one_lt_lamk n).le (lamk_lt_two n) hzpos hz
  exact lt_of_lt_of_le hlt (le_lamk hlam)

/-- **Main theorem.** The Krasikov–Lagarias constants are strictly increasing. -/
theorem lamk_strictMono : StrictMono lamk := strictMono_nat_of_lt_succ lamk_lt_succ

end main

/-! ## faithfulness: the index encoding is Krasikov–Lagarias' residue encoding -/

section faithful

/-- principal class `m ∈ [3^k]` of index `i`: class `m ≡ 2, 5, 8 (mod 9)` ↔ `i ≡ 0, 1, 2 (mod 3)` -/
lemma class_mod9 {n : ℕ} (i : Fin (N n)) :
    (3 * i.val + 2) % 9 = 3 * (i.val % 3) + 2 := by omega

/-- `nu` is multiplication by 4 on residues mod `3^k` -/
lemma nu_is_times_four {n : ℕ} (i : Fin (N n)) :
    ((3 * (nu i).val + 2 : ℕ) : ZMod (3 ^ (n + 2))) = 4 * ((3 * i.val + 2 : ℕ) : ZMod (3 ^ (n + 2))) :=
  res_nu i

/-- the auxiliary class of a row `m ≡ 2 (mod 9)` is `(4m - 2)/3`: `3 r ≡ 4 m - 2 (mod 3^k)` -/
lemma auxA_is_KL {n : ℕ} (i : Fin (N n)) (hi : i.val % 3 = 0) :
    ((3 * (3 * (auxA i).val + 2) : ℕ) : ZMod (3 ^ (n + 2)))
      = 4 * ((3 * i.val + 2 : ℕ) : ZMod (3 ^ (n + 2))) - 2 := by
  have hj : i.val = 3 * (i.val / 3) := by omega
  set j := i.val / 3
  have h1 : 3 * (3 * (auxA i).val + 2) ≡ 36 * j + 6 [MOD 3 ^ (n + 2)] := by
    unfold auxA; simp only
    have : 9 * ((4 * j) % M n) ≡ 9 * (4 * j) [MOD 9 * M n] := (Nat.mod_modEq _ _).mul_left' 9
    rw [show 3 ^ (n + 2) = 9 * M n by unfold M; ring]
    have h2 := this.add_right 6
    rw [show 3 * (3 * ((4 * j) % M n) + 2) = 9 * ((4 * j) % M n) + 6 by ring]
    rw [show 36 * j + 6 = 9 * (4 * j) + 6 by ring]
    exact h2
  rw [(ZMod.natCast_eq_natCast_iff _ _ _).mpr h1, hj]
  push_cast; ring

/-- the auxiliary class of a row `m ≡ 8 (mod 9)` is `(2m - 1)/3`: `3 r ≡ 2 m - 1 (mod 3^k)` -/
lemma auxB_is_KL {n : ℕ} (i : Fin (N n)) (hi : i.val % 3 = 2) :
    ((3 * (3 * (auxB i).val + 2) : ℕ) : ZMod (3 ^ (n + 2)))
      = 2 * ((3 * i.val + 2 : ℕ) : ZMod (3 ^ (n + 2))) - 1 := by
  have hj : i.val = 3 * (i.val / 3) + 2 := by omega
  set j := i.val / 3
  have h1 : 3 * (3 * (auxB i).val + 2) ≡ 18 * j + 15 [MOD 3 ^ (n + 2)] := by
    unfold auxB; simp only
    have : 9 * ((2 * j + 1) % M n) ≡ 9 * (2 * j + 1) [MOD 9 * M n] := (Nat.mod_modEq _ _).mul_left' 9
    rw [show 3 ^ (n + 2) = 9 * M n by unfold M; ring]
    have h2 := this.add_right 6
    rw [show 3 * (3 * ((2 * j + 1) % M n) + 2) = 9 * ((2 * j + 1) % M n) + 6 by ring]
    rw [show 18 * j + 15 = 9 * (2 * j + 1) + 6 by ring]
    exact h2
  rw [(ZMod.natCast_eq_natCast_iff _ _ _).mpr h1, hj]
  push_cast; ring

/-- the lifts of the auxiliary class `r = 3 s + 2` are `r + u · 3^(k-1)` -/
lemma lift_is_KL {n : ℕ} (s : Fin (M n)) (u : Fin 3) :
    3 * (lift s u).val + 2 = (3 * s.val + 2) + u.val * 3 ^ (n + 1) := by
  unfold lift M; simp only; ring

/-- Krasikov–Lagarias' `L^NT_k(λ)` literally ((2.7)–(2.14)): principal variables `1 ≤ c ≤ C^max`,
auxiliary variables `d` bounded by each of the three lifts, and the principal inequalities (L1)–(L3). -/
def KLFeasible (n : ℕ) (lam : ℝ) : Prop :=
  ∃ (c : Fin (N n) → ℝ) (d : Fin (M n) → ℝ) (Cmax : ℝ),
    (∀ i, 1 ≤ c i ∧ c i ≤ Cmax) ∧
    (∀ s u, d s ≤ c (lift s u)) ∧
    (∀ i : Fin (N n), i.val % 3 = 0 → c i ≤ c (nu i) * lam ^ (-2 : ℤ) + d (auxA i) * lam ^ (α - 2)) ∧
    (∀ i : Fin (N n), i.val % 3 = 1 → c i ≤ c (nu i) * lam ^ (-2 : ℤ)) ∧
    (∀ i : Fin (N n), i.val % 3 = 2 → c i ≤ c (nu i) * lam ^ (-2 : ℤ) + d (auxB i) * lam ^ (α - 1))

lemma zpow_neg_two (lam : ℝ) : lam ^ (-2 : ℤ) = pc lam := by
  unfold pc; rw [zpow_neg, inv_pow]; norm_cast

theorem klFeasible_iff (n : ℕ) {lam : ℝ} (hlam : 0 < lam) : KLFeasible n lam ↔ Feasible n lam := by
  have hq := qc_pos hlam; have hr := rc_pos hlam
  constructor
  · rintro ⟨c, d, Cmax, h0, h4, h1, h2, h3⟩
    refine ⟨c, fun i => by linarith [(h0 i).1], fun i => ?_⟩
    have hd : ∀ s, d s ≤ cbar c s := fun s => by
      unfold cbar; exact le_min (h4 s 0) (le_min (h4 s 1) (h4 s 2))
    unfold F; rw [Fc_split]
    simp only [zpow_neg_two] at h1 h2 h3
    have h3 : i.val % 3 = 0 ∨ i.val % 3 = 1 ∨ i.val % 3 = 2 := by omega
    rcases h3 with h | h | h
    · have := h1 i h
      simp only [h, if_true, show ¬ ((0 : ℕ) = 2) from by norm_num, if_false, add_zero]
      have e : qc lam = lam ^ (α - 2) := rfl
      rw [← e] at this
      nlinarith [mul_le_mul_of_nonneg_left (hd (auxA i)) hq.le]
    · have := h2 i h
      simp only [h, show ¬ ((1 : ℕ) = 0) from by norm_num, show ¬ ((1 : ℕ) = 2) from by norm_num,
        if_false, add_zero]
      linarith
    · have := h3 i h
      simp only [h, show ¬ ((2 : ℕ) = 0) from by norm_num, if_true, if_false]
      have e : rc lam = lam ^ (α - 1) := rfl
      rw [← e] at this
      nlinarith [mul_le_mul_of_nonneg_left (hd (auxB i)) hr.le]
  · rintro ⟨c, hpos, hc⟩
    obtain ⟨i0, -, hi0⟩ := Finset.exists_min_image Finset.univ c Finset.univ_nonempty
    set t := (c i0)⁻¹ with ht
    have htpos : 0 < t := inv_pos.mpr (hpos i0)
    set c' : Fin (N n) → ℝ := t • c with hc'
    have hc'F : ∀ i, c' i ≤ F n lam c' i := by
      intro i; unfold F; rw [hc', Fc_smul htpos.le]
      simp only [Pi.smul_apply, smul_eq_mul]
      exact mul_le_mul_of_nonneg_left (hc i) htpos.le
    obtain ⟨i1, -, hi1⟩ := Finset.exists_max_image Finset.univ c' Finset.univ_nonempty
    refine ⟨c', cbar c', c' i1, fun i => ⟨?_, hi1 i (Finset.mem_univ _)⟩, fun s u => cbar_le c' s u,
      ?_, ?_, ?_⟩
    · simp only [hc', Pi.smul_apply, smul_eq_mul, ht]
      rw [← div_eq_inv_mul, le_div_iff₀ (hpos i0)]
      simpa using hi0 i (Finset.mem_univ _)
    · intro i h
      have := hc'F i; unfold F at this; rw [Fc_split] at this
      simp only [h, if_true, show ¬ ((0 : ℕ) = 2) from by norm_num, if_false, add_zero] at this
      rw [zpow_neg_two]; unfold qc at this; linarith
    · intro i h
      have := hc'F i; unfold F at this; rw [Fc_split] at this
      simp only [h, show ¬ ((1 : ℕ) = 0) from by norm_num, show ¬ ((1 : ℕ) = 2) from by norm_num,
        if_false, add_zero] at this
      rw [zpow_neg_two]; linarith
    · intro i h
      have := hc'F i; unfold F at this; rw [Fc_split] at this
      simp only [h, show ¬ ((2 : ℕ) = 0) from by norm_num, if_true, if_false] at this
      rw [zpow_neg_two]; unfold rc at this; linarith

/-- the admissible parameters of the literal `L^NT_k` -/
def LamKL (n : ℕ) : Set ℝ := {lam | 1 ≤ lam ∧ lam ≤ 2 ∧ KLFeasible n lam}

lemma LamKL_eq (n : ℕ) : LamKL n = Lam n := by
  ext lam
  constructor
  · rintro ⟨h1, h2, h3⟩; exact ⟨h1, h2, (klFeasible_iff n (by linarith)).mp h3⟩
  · rintro ⟨h1, h2, h3⟩; exact ⟨h1, h2, (klFeasible_iff n (by linarith)).mpr h3⟩

/-- **Main theorem, literal form.** With `λ_k := sup {λ ∈ [1,2] : L^NT_k(λ) feasible}` (`k = n + 2`),
`λ_k` is attained, `1 < λ_k < 2`, and `λ_k < λ_{k+1}`. -/
theorem KL_lambda_strictMono :
    StrictMono (fun n => sSup (LamKL n)) ∧
      ∀ n, sSup (LamKL n) ∈ LamKL n ∧ 1 < sSup (LamKL n) ∧ sSup (LamKL n) < 2 := by
  simp only [LamKL_eq]
  exact ⟨lamk_strictMono, fun n => ⟨lamk_mem n, one_lt_lamk n, lamk_lt_two n⟩⟩

/-- **Corollary (exact solution of Krasikov's system `I_k`).** For a feasible `c` at `λ_k`,
`φ_m(y) = c_m λ_k^y` satisfies (D1)–(D3) with equality for every real `y`, where `φ_{k-1}` is the minimum
over the three lifts (2.6). Hence no exponential lower bound with rate above `λ_k` follows from `I_k`. -/
theorem exact_solution {n : ℕ} {c : Fin (N n) → ℝ} (hpos : ∀ i, 0 < c i)
    (hc : ∀ i, c i ≤ F n (lamk n) c i) (y : ℝ) :
    let L := lamk n
    let φ : Fin (N n) → ℝ → ℝ := fun i y => c i * L ^ y
    let φbar : Fin (M n) → ℝ → ℝ := fun s y => min (φ (lift s 0) y) (min (φ (lift s 1) y) (φ (lift s 2) y))
    ∀ i : Fin (N n),
      (i.val % 3 = 0 → φ i y = φ (nu i) (y - 2) + φbar (auxA i) (y + α - 2)) ∧
      (i.val % 3 = 1 → φ i y = φ (nu i) (y - 2)) ∧
      (i.val % 3 = 2 → φ i y = φ (nu i) (y - 2) + φbar (auxB i) (y + α - 1)) := by
  intro L φ φbar i
  have hL0 : 0 < L := by have := one_lt_lamk n; simp only [L]; linarith
  have ht := tight hpos hc i
  unfold F at ht; rw [Fc_split] at ht
  have hbar : ∀ s z, φbar s z = cbar c s * L ^ z := by
    intro s z
    simp only [φbar, φ, cbar]
    have hz : 0 ≤ L ^ z := (Real.rpow_pos_of_pos hL0 z).le
    rw [min_mul_of_nonneg _ _ hz, min_mul_of_nonneg _ _ hz]
  have hy2 : L ^ (y - 2) = L ^ y * pc L := by
    rw [Real.rpow_sub hL0]; unfold pc
    rw [show (2 : ℝ) = ((2 : ℕ) : ℝ) by norm_num, Real.rpow_natCast]; ring
  have hya2 : L ^ (y + α - 2) = L ^ y * qc L := by
    rw [show y + α - 2 = y + (α - 2) by ring, Real.rpow_add hL0]; rfl
  have hya1 : L ^ (y + α - 1) = L ^ y * rc L := by
    rw [show y + α - 1 = y + (α - 1) by ring, Real.rpow_add hL0]; rfl
  refine ⟨fun h => ?_, fun h => ?_, fun h => ?_⟩
  · simp only [h, if_true, show ¬ ((0 : ℕ) = 2) from by norm_num, if_false, add_zero] at ht
    simp only [φ, hbar, hy2, hya2]
    rw [← ht]; ring
  · simp only [h, show ¬ ((1 : ℕ) = 0) from by norm_num, show ¬ ((1 : ℕ) = 2) from by norm_num,
      if_false, add_zero] at ht
    simp only [φ, hy2]
    rw [← ht]; ring
  · simp only [h, show ¬ ((2 : ℕ) = 0) from by norm_num, if_true, if_false] at ht
    simp only [φ, hbar, hy2, hya1]
    rw [← ht]; ring

end faithful

/-! ## the mean loss at `λ_k` has a closed form and is strictly increasing -/

section rho

/-- the mean loss ratio `ρ = 3 Σ c̄ / Σ c` of a vector (`ρ_k` in the notation of Krasikov–Lagarias §6) -/
noncomputable def rhoOf {n : ℕ} (c : Fin (N n) → ℝ) : ℝ := 3 * (∑ s, cbar c s) / ∑ i, c i

/-- `R(λ) = 3 (λ - 1) / λ^α` -/
noncomputable def R (x : ℝ) : ℝ := 3 * (x - 1) / x ^ α

lemma alpha_gt_one : 1 < α := by
  unfold α
  rw [Real.lt_logb_iff_rpow_lt (by norm_num) (by norm_num)]
  norm_num

lemma alpha_lt_two : α < 2 := by
  unfold α
  rw [Real.logb_lt_iff_lt_rpow (by norm_num) (by norm_num)]
  norm_num

lemma coef_identity {lam : ℝ} (h : 0 < lam) : 3 * (1 - pc lam) = R lam * (qc lam + rc lam) := by
  unfold pc qc rc R
  have hα : 0 < lam ^ α := Real.rpow_pos_of_pos h α
  rw [Real.rpow_sub h, Real.rpow_sub h, Real.rpow_one,
    show (2 : ℝ) = ((2 : ℕ) : ℝ) by norm_num, Real.rpow_natCast]
  field_simp
  ring

/-- **Corollary.** At `λ_k` the mean loss of the (unique) solution is `ρ_k = 3 (λ_k - 1) / λ_k^α`. -/
theorem rho_eq {n : ℕ} {c : Fin (N n) → ℝ} (hpos : ∀ i, 0 < c i) (hc : ∀ i, c i ≤ F n (lamk n) c i) :
    rhoOf c = R (lamk n) := by
  have hL0 : 0 < lamk n := by linarith [one_lt_lamk n]
  have ht := tight hpos hc
  have hsum := sum_Fc (p := pc (lamk n)) (q := qc (lamk n)) (r := rc (lamk n)) c
  have h1 : ∑ i, Fc (pc (lamk n)) (qc (lamk n)) (rc (lamk n)) c i = ∑ i, c i :=
    Finset.sum_congr rfl (fun i _ => by have := ht i; unfold F at this; exact this)
  rw [h1] at hsum
  have hS : 0 < ∑ i, c i := Finset.sum_pos (fun i _ => hpos i) Finset.univ_nonempty
  have hqr : 0 < qc (lamk n) + rc (lamk n) := by linarith [qc_pos hL0, rc_pos hL0]
  have hid := coef_identity hL0
  unfold rhoOf
  rw [div_eq_iff hS.ne']
  have : (qc (lamk n) + rc (lamk n)) * (3 * ∑ s, cbar c s)
      = (qc (lamk n) + rc (lamk n)) * (R (lamk n) * ∑ i, c i) := by
    have e1 : (qc (lamk n) + rc (lamk n)) * ∑ s, cbar c s = (1 - pc (lamk n)) * ∑ i, c i := by linarith
    calc (qc (lamk n) + rc (lamk n)) * (3 * ∑ s, cbar c s)
        = 3 * ((qc (lamk n) + rc (lamk n)) * ∑ s, cbar c s) := by ring
      _ = 3 * (1 - pc (lamk n)) * ∑ i, c i := by rw [e1]; ring
      _ = R (lamk n) * (qc (lamk n) + rc (lamk n)) * ∑ i, c i := by rw [hid]
      _ = (qc (lamk n) + rc (lamk n)) * (R (lamk n) * ∑ i, c i) := by ring
  exact mul_left_cancel₀ hqr.ne' this

lemma hasDerivAt_R {x : ℝ} (hx : 0 < x) :
    HasDerivAt R ((3 * x ^ α - 3 * (x - 1) * (α * x ^ (α - 1))) / (x ^ α) ^ 2) x := by
  have h1 : HasDerivAt (fun y => 3 * (y - 1)) 3 x := by
    simpa using ((hasDerivAt_id x).sub_const 1).const_mul 3
  have h2 : HasDerivAt (fun y => y ^ α) (α * x ^ (α - 1)) x := Real.hasDerivAt_rpow_const (Or.inl hx.ne')
  have h3 := h1.div h2 (Real.rpow_pos_of_pos hx α).ne'
  convert h3 using 1 <;> first | rfl | ring

/-- `R` is strictly increasing on `[1, 2]` (indeed on `[1, α/(α-1)]`). -/
lemma R_strictMonoOn : StrictMonoOn R (Set.Icc 1 2) := by
  apply strictMonoOn_of_deriv_pos (convex_Icc 1 2)
  · intro x hx
    have hx0 : 0 < x := by linarith [hx.1]
    have : ContinuousAt R x := (hasDerivAt_R hx0).continuousAt
    exact this.continuousWithinAt
  · intro x hx
    rw [interior_Icc] at hx
    have hx0 : 0 < x := by linarith [hx.1]
    rw [(hasDerivAt_R hx0).deriv]
    have hα1 := alpha_gt_one; have hα2 := alpha_lt_two
    have hxa : 0 < x ^ α := Real.rpow_pos_of_pos hx0 α
    have hsplit : x ^ α = x ^ (α - 1) * x := by
      rw [← Real.rpow_add_one hx0.ne']; ring_nf
    have hxa1 : 0 < x ^ (α - 1) := Real.rpow_pos_of_pos hx0 _
    apply div_pos _ (by positivity)
    rw [hsplit]
    have hkey : 0 < x - α * (x - 1) := by nlinarith [hx.2]
    nlinarith [mul_pos hxa1 hkey]

/-- **Corollary.** The mean loss `1 - ρ_k` of the solution at `λ_k` is strictly decreasing in `k`. -/
theorem rho_strictMono : StrictMono (fun n => R (lamk n)) := by
  intro a b hab
  have ha := lamk_mem a; have hb := lamk_mem b
  exact R_strictMonoOn ⟨ha.1, ha.2.1⟩ ⟨hb.1, hb.2.1⟩ (lamk_strictMono hab)

end rho

end KLMono
