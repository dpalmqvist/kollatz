import Mathlib.Data.Real.Basic
import Mathlib.Order.Interval.Finset.Nat
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.IntervalCases
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.GCongr
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum

/-!
# Uniform lower bounds for 3x+1 preimage counts via residue-class certificates

* `T` is the 3x+1 map, `T n = n/2` for even `n` and `(3n+1)/2` for odd `n`.
* `preimages k a = {n ∈ [1, 2^k a] : T^[k] n = a}` and `nk k a` is its cardinality (Applegate–Lagarias' n_k(a)).
  `mem_preimages_iff` shows the window `[1, 2^k a]` loses nothing: it contains every `n` with `T^[k] n = a`.
* `pruned k a = {n : T^[k] n = a, T^[j] n ≢ 0 (mod 3) for all j ≤ k}` and `prunedCount k a` is its cardinality,
  the number of depth-`k` nodes of the pruned tree T*_k(a) (Applegate–Lagarias' N*_k(a)). `prunedCount_le` gives
  `prunedCount k a ≤ nk k a`, and `prunedCount_succ` is the tree recursion
  `N*_{k+1}(b) = N*_k(2b) + [b ≡ 2, 8 (mod 9)] · N*_k((2b-1)/3)`.
* `residue_class_bound`: a positive vector `V` on the classes mod `3^r` with `P·V ≤ Q·Φ(V)` gives
  `P^k · V(b mod 3^r) ≤ V_max · Q^k · N*_k(b)` for all `k` and all `b ≢ 0 (mod 3)`.
-/

namespace PreimageBound

/-- The 3x+1 map. -/
def T (n : ℕ) : ℕ := if n % 2 = 0 then n / 2 else (3 * n + 1) / 2

/-- `{n ∈ [1, 2^k a] : T^[k] n = a}`. -/
def preimages (k a : ℕ) : Finset ℕ := (Finset.Icc 1 (2 ^ k * a)).filter (fun n => T^[k] n = a)

/-- `n_k(a)`, the number of `n ≥ 1` with `T^[k] n = a`. -/
def nk (k a : ℕ) : ℕ := (preimages k a).card

/-- The depth-`k` nodes of the pruned preimage tree of `a`: `T^[k] n = a` and no iterate `T^[j] n`, `j ≤ k`,
is divisible by 3. -/
def pruned (k a : ℕ) : Finset ℕ :=
  (Finset.Icc 1 (2 ^ k * a)).filter (fun n => T^[k] n = a ∧ ∀ j ≤ k, T^[j] n % 3 ≠ 0)

/-- `N*_k(a)`. -/
def prunedCount (k a : ℕ) : ℕ := (pruned k a).card

/-! ## Elementary facts about `T` -/

lemma le_two_mul_T (n : ℕ) : n ≤ 2 * T n := by
  unfold T; split_ifs <;> omega

lemma le_two_pow_mul_iterate (k n : ℕ) : n ≤ 2 ^ k * T^[k] n := by
  induction k generalizing n with
  | zero => simp
  | succ k ih =>
    rw [Function.iterate_succ_apply]
    have h1 := le_two_mul_T n
    have h2 := ih (T n)
    calc n ≤ 2 * T n := h1
      _ ≤ 2 * (2 ^ k * T^[k] (T n)) := Nat.mul_le_mul_left 2 h2
      _ = 2 ^ (k + 1) * T^[k] (T n) := by ring

lemma T_zero : T 0 = 0 := by simp [T]

lemma iterate_T_zero (k : ℕ) : T^[k] 0 = 0 := Function.iterate_fixed T_zero k

/-- The window `[1, 2^k a]` in `preimages` contains every solution of `T^[k] n = a` (for `a ≥ 1`). -/
theorem mem_preimages_iff {k a : ℕ} (ha : 0 < a) (n : ℕ) : n ∈ preimages k a ↔ T^[k] n = a := by
  simp only [preimages, Finset.mem_filter, Finset.mem_Icc]
  constructor
  · exact fun h => h.2
  · intro h
    refine ⟨⟨?_, ?_⟩, h⟩
    · rcases Nat.eq_zero_or_pos n with h0 | h0
      · subst h0; rw [iterate_T_zero] at h; omega
      · exact h0
    · simpa [h] using le_two_pow_mul_iterate k n

theorem pruned_subset (k a : ℕ) : pruned k a ⊆ preimages k a := by
  intro n hn
  simp only [pruned, preimages, Finset.mem_filter] at hn ⊢
  exact ⟨hn.1, hn.2.1⟩

theorem prunedCount_le (k a : ℕ) : prunedCount k a ≤ nk k a :=
  Finset.card_le_card (pruned_subset k a)

/-! ## The tree recursion for `N*_k` -/

/-- The predecessors of `b` under `T`. -/
lemma T_eq_iff (m b : ℕ) : T m = b ↔ m = 2 * b ∨ (m % 2 = 1 ∧ 3 * m + 1 = 2 * b) := by
  unfold T; split_ifs <;> omega

/-- The predecessors of `b ≢ 0 (mod 3)` that are themselves `≢ 0 (mod 3)`: `2b` always, and `(2b-1)/3` iff
`b ≡ 2, 8 (mod 9)`. -/
lemma pred_iff {b : ℕ} (hb : b % 3 ≠ 0) (m : ℕ) :
    (T m = b ∧ m % 3 ≠ 0) ↔ (m = 2 * b ∨ ((b % 9 = 2 ∨ b % 9 = 8) ∧ m = (2 * b - 1) / 3)) := by
  rw [T_eq_iff]; omega

lemma mem_pruned_succ {k b : ℕ} (hb : b % 3 ≠ 0) (n : ℕ) :
    n ∈ pruned (k + 1) b ↔ ∃ m, (T m = b ∧ m % 3 ≠ 0) ∧ n ∈ pruned k m := by
  simp only [pruned, Finset.mem_filter, Finset.mem_Icc]
  constructor
  · rintro ⟨⟨h1, _⟩, hT, hall⟩
    refine ⟨T^[k] n, ⟨?_, hall k (by omega)⟩, ⟨h1, le_two_pow_mul_iterate k n⟩, rfl, ?_⟩
    · rw [← Function.iterate_succ_apply' T k n]; exact hT
    · intro j hj; exact hall j (by omega)
  · rintro ⟨m, ⟨hTm, _⟩, ⟨h1, h2⟩, hk, hall⟩
    have hTk : T^[k + 1] n = b := by rw [Function.iterate_succ_apply', hk, hTm]
    have hm : m ≤ 2 * b := by have := le_two_mul_T m; rw [hTm] at this; exact this
    refine ⟨⟨h1, ?_⟩, hTk, ?_⟩
    · calc n ≤ 2 ^ k * m := h2
        _ ≤ 2 ^ k * (2 * b) := Nat.mul_le_mul_left _ hm
        _ = 2 ^ (k + 1) * b := by ring
    · intro j hj
      rcases Nat.lt_or_ge j (k + 1) with hj' | hj'
      · exact hall j (by omega)
      · have : j = k + 1 := by omega
        subst this; rw [hTk]; exact hb

lemma pruned_disjoint {k x y : ℕ} (hxy : x ≠ y) : Disjoint (pruned k x) (pruned k y) := by
  rw [Finset.disjoint_left]
  intro n hx hy
  simp only [pruned, Finset.mem_filter] at hx hy
  exact hxy (hx.2.1.symm.trans hy.2.1)

/-- The recursion `N*_{k+1}(b) = N*_k(2b) + [b ≡ 2, 8 (mod 9)] · N*_k((2b-1)/3)` (Applegate–Lagarias (2.2)). -/
theorem prunedCount_succ {b : ℕ} (hb : b % 3 ≠ 0) (k : ℕ) :
    prunedCount (k + 1) b =
      prunedCount k (2 * b) + if b % 9 = 2 ∨ b % 9 = 8 then prunedCount k ((2 * b - 1) / 3) else 0 := by
  unfold prunedCount
  split_ifs with hβ
  · have hset : pruned (k + 1) b = pruned k (2 * b) ∪ pruned k ((2 * b - 1) / 3) := by
      ext n
      rw [mem_pruned_succ hb, Finset.mem_union]
      constructor
      · rintro ⟨m, hm, hn⟩
        rcases (pred_iff hb m).1 hm with h | h
        · left; rw [← h]; exact hn
        · right; rw [← h.2]; exact hn
      · rintro (hn | hn)
        · exact ⟨2 * b, (pred_iff hb _).2 (Or.inl rfl), hn⟩
        · exact ⟨_, (pred_iff hb _).2 (Or.inr ⟨hβ, rfl⟩), hn⟩
    rw [hset, Finset.card_union_of_disjoint (pruned_disjoint (by omega))]
  · have hset : pruned (k + 1) b = pruned k (2 * b) := by
      ext n
      rw [mem_pruned_succ hb]
      constructor
      · rintro ⟨m, hm, hn⟩
        rcases (pred_iff hb m).1 hm with h | h
        · rw [← h]; exact hn
        · exact absurd h.1 hβ
      · intro hn
        exact ⟨2 * b, (pred_iff hb _).2 (Or.inl rfl), hn⟩
    rw [hset, Nat.add_zero]

theorem prunedCount_zero {b : ℕ} (hb : b % 3 ≠ 0) : prunedCount 0 b = 1 := by
  have : pruned 0 b = {b} := by
    ext n
    simp only [pruned, Finset.mem_filter, Finset.mem_Icc, Function.iterate_zero, id_eq, pow_zero,
      one_mul, Finset.mem_singleton, Nat.le_zero]
    constructor
    · exact fun h => h.2.1
    · intro h; subst h
      refine ⟨⟨by omega, le_rfl⟩, rfl, ?_⟩
      intro j hj; subst hj; simpa using hb
  rw [prunedCount, this, Finset.card_singleton]

/-! ## The residue-class system -/

/-- The three lifts of the class `c` (for `c ≡ 2 mod 3`): `(2c-1)/3 + u·3^(r-1) mod 3^r`, `u = 0, 1, 2`. -/
def lift (r c u : ℕ) : ℕ := ((2 * c - 1) / 3 + u * 3 ^ (r - 1)) % 3 ^ r

/-- `Φ(V)(c) = V(2c mod 3^r) + β(c) · min_u V(lift_u(c))`, `β(c) = [c ≡ 2, 8 (mod 9)]`. -/
def Phi (r : ℕ) (V : ℕ → ℕ) (c : ℕ) : ℕ :=
  V (2 * c % 3 ^ r) +
    if c % 9 = 2 ∨ c % 9 = 8 then min (V (lift r c 0)) (min (V (lift r c 1)) (V (lift r c 2))) else 0

/-- `(2b-1)/3 mod 3^r` is one of the three lifts of `b mod 3^r`. -/
lemma lift_cover {r : ℕ} (hr : 1 ≤ r) {b : ℕ} (hb : b % 3 = 2) :
    ∃ u < 3, (2 * b - 1) / 3 % 3 ^ r = lift r (b % 3 ^ r) u := by
  obtain ⟨s, rfl⟩ : ∃ s, r = s + 1 := ⟨r - 1, by omega⟩
  simp only [lift, Nat.add_sub_cancel]
  set t := 3 ^ s with ht
  have hM : 3 ^ (s + 1) = 3 * t := by rw [pow_succ]; ring
  rw [hM]
  set c := b % (3 * t) with hc
  set q := b / (3 * t) with hq
  have hbq : b = c + 3 * (t * q) := by
    have := Nat.mod_add_div b (3 * t); rw [← hc, ← hq] at this; rw [← this]; ring
  have hc3 : c % 3 = 2 := by
    rw [hc, Nat.mod_mul_right_mod]; exact hb
  set x := (2 * c - 1) / 3 with hx
  have hdiv : (2 * b - 1) / 3 = x + 2 * (t * q) := by
    rw [hx]; generalize t * q = z at hbq; omega
  refine ⟨2 * q % 3, Nat.mod_lt _ (by norm_num), ?_⟩
  rw [hdiv]
  have h2q : 2 * q = 2 * q % 3 + 3 * (2 * q / 3) := (Nat.mod_add_div (2 * q) 3).symm
  have : x + 2 * (t * q) = x + 2 * q % 3 * t + 3 * t * (2 * q / 3) := by
    calc x + 2 * (t * q) = x + t * (2 * q) := by ring
      _ = x + t * (2 * q % 3 + 3 * (2 * q / 3)) := by rw [← h2q]
      _ = x + 2 * q % 3 * t + 3 * t * (2 * q / 3) := by ring
  rw [this, Nat.add_mul_mod_self_left]

/-- **Residue-class bound.** If `V` satisfies `P·V(c) ≤ Q·Φ(V)(c)` and `V(c) ≤ Vmax` on every class `c mod 3^r`
with `c ≢ 0 (mod 3)`, then `P^k · V(b mod 3^r) ≤ Vmax · Q^k · N*_k(b)` for every `k` and every `b ≢ 0 (mod 3)`. -/
theorem residue_class_bound {r : ℕ} (hr : 2 ≤ r) (V : ℕ → ℕ) (P Q Vmax : ℕ)
    (hcert : ∀ c < 3 ^ r, c % 3 ≠ 0 → P * V c ≤ Q * Phi r V c)
    (hmax : ∀ c < 3 ^ r, c % 3 ≠ 0 → V c ≤ Vmax) :
    ∀ k b, b % 3 ≠ 0 → P ^ k * V (b % 3 ^ r) ≤ Vmax * Q ^ k * prunedCount k b := by
  have h3 : 3 ∣ 3 ^ r := dvd_pow_self 3 (by omega)
  have h9 : 9 ∣ 3 ^ r := by
    have : (9 : ℕ) = 3 ^ 2 := by norm_num
    rw [this]; exact pow_dvd_pow 3 hr
  have hpos : 0 < 3 ^ r := by positivity
  intro k
  induction k with
  | zero =>
    intro b hb
    simp only [prunedCount_zero hb, pow_zero, one_mul, mul_one]
    exact hmax _ (Nat.mod_lt _ hpos) (by rw [Nat.mod_mod_of_dvd _ h3]; exact hb)
  | succ k ih =>
    intro b hb
    set c := b % 3 ^ r with hc
    have hcM : c < 3 ^ r := Nat.mod_lt _ hpos
    have hc3 : c % 3 = b % 3 := Nat.mod_mod_of_dvd _ h3
    have hc9 : c % 9 = b % 9 := Nat.mod_mod_of_dvd _ h9
    have key := hcert c hcM (by rw [hc3]; exact hb)
    have h2c : 2 * c % 3 ^ r = 2 * b % 3 ^ r := by rw [hc, Nat.mul_mod, Nat.mod_mod, ← Nat.mul_mod]
    have ih2 := ih (2 * b) (by omega)
    rw [Phi, h2c, hc9] at key
    rw [prunedCount_succ hb, pow_succ, pow_succ]
    split_ifs at key ⊢ with hβ
    · set m := (2 * b - 1) / 3 with hm
      have ihm := ih m (by omega)
      obtain ⟨u, hu, hlift⟩ := lift_cover (r := r) (by omega) (b := b) (by omega)
      have hmin : min (V (lift r c 0)) (min (V (lift r c 1)) (V (lift r c 2))) ≤ V (m % 3 ^ r) := by
        rw [hlift, ← hc]
        interval_cases u <;> simp
      calc P ^ k * P * V c = P ^ k * (P * V c) := by ring
        _ ≤ P ^ k * (Q * (V (2 * b % 3 ^ r) + V (m % 3 ^ r))) := by
          apply Nat.mul_le_mul_left
          calc P * V c ≤ _ := key
            _ ≤ _ := by gcongr
        _ = Q * (P ^ k * V (2 * b % 3 ^ r) + P ^ k * V (m % 3 ^ r)) := by ring
        _ ≤ Q * (Vmax * Q ^ k * prunedCount k (2 * b) + Vmax * Q ^ k * prunedCount k m) := by
          gcongr
        _ = Vmax * (Q ^ k * Q) * (prunedCount k (2 * b) + prunedCount k m) := by ring
    · calc P ^ k * P * V c = P ^ k * (P * V c) := by ring
        _ ≤ P ^ k * (Q * (V (2 * b % 3 ^ r) + 0)) := Nat.mul_le_mul_left _ key
        _ = Q * (P ^ k * V (2 * b % 3 ^ r)) := by ring
        _ ≤ Q * (Vmax * Q ^ k * prunedCount k (2 * b)) := Nat.mul_le_mul_left _ ih2
        _ = Vmax * (Q ^ k * Q) * (prunedCount k (2 * b) + 0) := by ring

/-- Real form: `(Vmin/Vmax) · (P/Q)^k ≤ N*_k(b) ≤ n_k(b)`. -/
theorem residue_class_bound_real {r : ℕ} (hr : 2 ≤ r) (V : ℕ → ℕ) (P Q Vmin Vmax : ℕ)
    (hQ : 0 < Q) (hVmax : 0 < Vmax)
    (hcert : ∀ c < 3 ^ r, c % 3 ≠ 0 → P * V c ≤ Q * Phi r V c)
    (hmax : ∀ c < 3 ^ r, c % 3 ≠ 0 → V c ≤ Vmax)
    (hmin : ∀ c < 3 ^ r, c % 3 ≠ 0 → Vmin ≤ V c)
    (k b : ℕ) (hb : b % 3 ≠ 0) :
    ((Vmin : ℝ) / Vmax) * ((P : ℝ) / Q) ^ k ≤ prunedCount k b := by
  have h3 : 3 ∣ 3 ^ r := dvd_pow_self 3 (by omega)
  have hpos : 0 < 3 ^ r := by positivity
  have hnat := residue_class_bound hr V P Q Vmax hcert hmax k b hb
  have hm := hmin (b % 3 ^ r) (Nat.mod_lt _ hpos) (by rw [Nat.mod_mod_of_dvd _ h3]; exact hb)
  have hnat' : Vmin * P ^ k ≤ Vmax * Q ^ k * prunedCount k b :=
    calc Vmin * P ^ k ≤ V (b % 3 ^ r) * P ^ k := Nat.mul_le_mul_right _ hm
      _ = P ^ k * V (b % 3 ^ r) := by ring
      _ ≤ _ := hnat
  have hreal : (Vmin : ℝ) * (P : ℝ) ^ k ≤ (Vmax : ℝ) * (Q : ℝ) ^ k * (prunedCount k b : ℝ) := by
    exact_mod_cast hnat'
  have hden : (0 : ℝ) < (Vmax : ℝ) * (Q : ℝ) ^ k := by positivity
  rw [div_pow, div_mul_div_comm, div_le_iff₀ hden]
  linarith

theorem residue_class_bound_nk {r : ℕ} (hr : 2 ≤ r) (V : ℕ → ℕ) (P Q Vmin Vmax : ℕ)
    (hQ : 0 < Q) (hVmax : 0 < Vmax)
    (hcert : ∀ c < 3 ^ r, c % 3 ≠ 0 → P * V c ≤ Q * Phi r V c)
    (hmax : ∀ c < 3 ^ r, c % 3 ≠ 0 → V c ≤ Vmax)
    (hmin : ∀ c < 3 ^ r, c % 3 ≠ 0 → Vmin ≤ V c)
    (k b : ℕ) (hb : b % 3 ≠ 0) :
    ((Vmin : ℝ) / Vmax) * ((P : ℝ) / Q) ^ k ≤ nk k b :=
  (residue_class_bound_real hr V P Q Vmin Vmax hQ hVmax hcert hmax hmin k b hb).trans
    (by exact_mod_cast prunedCount_le k b)

end PreimageBound
