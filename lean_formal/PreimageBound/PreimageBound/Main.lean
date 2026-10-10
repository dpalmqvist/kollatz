import Mathlib.Algebra.Order.Ring.Pow
import Mathlib.Tactic.FieldSimp
import PreimageBound.R4
import PreimageBound.R5
import PreimageBound.R8
import PreimageBound.R10
import PreimageBound.R12
import PreimageBound.R13
import PreimageBound.R14

/-!
# PreimageBound: uniform lower bounds for 3x+1 preimage counts, kernel-checked

For the 3x+1 map `T n = n/2` (n even), `(3n+1)/2` (n odd), and every `a ≢ 0 (mod 3)`, `k ≥ 0`:

  `c · μ^k ≤ #{n ∈ [1, 2^k a] : T^[k] n = a}`

(the window `[1, 2^k a]` contains every solution of `T^[k] n = a`, see `mem_preimages_iff`), with

| r  | classes   | μ               | c          | theorem                           |
|----|-----------|-----------------|------------|-----------------------------------|
| 4  | 54        | 13215671/10^7   | 3567/10^4  | `preimage_count_lower_bound_R4'`  |
| 5  | 162       | 13258205/10^7   | 3315/10^4  | `preimage_count_lower_bound_R5'`  |
| 8  | 4374      | 13312914/10^7   | 3002/10^4  | `preimage_count_lower_bound_R8'`  |
| 10 | 39366     | 13324254/10^7   | 2915/10^4  | `preimage_count_lower_bound_R10'` |
| 12 | 354294    | 13329408/10^7   | 2871/10^4  | `preimage_count_lower_bound_R12'` |
| 13 | 1062882   | 13330772/10^7   | 2859/10^4  | `preimage_count_lower_bound_R13'` |
| 14 | 3188646   | 13331664/10^7   | 2847/10^4  | `preimage_count_lower_bound_R14'` |

Applegate–Lagarias (Math. Comp. 64 (1995), Theorem 1.1) have `(1.302053)^k ≤ n_k(a)` for all sufficiently large
`k`. The best certificate (r = 14) is restated below as `preimage_count_lower_bound`, and
`preimage_count_ge_pow` puts it in their form.
-/

namespace PreimageBound

/-- **Main theorem.** For every `a ≢ 0 (mod 3)` and every `k ≥ 0`, at least `0.2847 · 1.3331664^k` positive
integers `n ≤ 2^k a` satisfy `T^[k] n = a`, where `T` is the 3x+1 map. -/
theorem preimage_count_lower_bound (a : ℕ) (ha : 0 < a) (ha3 : a % 3 ≠ 0) (k : ℕ) :
    (2847 / 10000 : ℝ) * (13331664 / 10000000 : ℝ) ^ k ≤
      ((Finset.Icc 1 (2 ^ k * a)).filter
        (fun n => (fun m : ℕ => if m % 2 = 0 then m / 2 else (3 * m + 1) / 2)^[k] n = a)).card :=
  preimage_count_lower_bound_R14' a ha ha3 k

/-- From `c·μ^k` to `x^k` for large `k` (Bernoulli's inequality). -/
lemma pow_le_of_bernoulli {c μ x : ℝ} (hx : 0 < x) (hxμ : x ≤ μ) (hc : 0 ≤ c) {K k : ℕ} (hk : K ≤ k)
    (hK : 1 ≤ c * (1 + K * (μ / x - 1))) : x ^ k ≤ c * μ ^ k := by
  have hd : 0 ≤ μ / x - 1 := by rw [sub_nonneg, le_div_iff₀ hx]; linarith
  have hb : 1 + (k : ℝ) * (μ / x - 1) ≤ (μ / x) ^ k := by
    have := one_add_mul_le_pow (a := μ / x - 1) (by linarith) k
    simpa using this
  have hKk : (K : ℝ) ≤ k := by exact_mod_cast hk
  have h1 : 1 ≤ c * (μ / x) ^ k :=
    hK.trans (mul_le_mul_of_nonneg_left
      (le_trans (by nlinarith) hb) hc)
  have hxk : 0 < x ^ k := pow_pos hx k
  calc x ^ k = x ^ k * 1 := (mul_one _).symm
    _ ≤ x ^ k * (c * (μ / x) ^ k) := mul_le_mul_of_nonneg_left h1 hxk.le
    _ = c * μ ^ k := by rw [div_pow]; field_simp

/-- **Applegate–Lagarias form.** For every `a ≢ 0 (mod 3)` and every `k ≥ 20200`, `1.333^k ≤ n_k(a)`
(Applegate–Lagarias 1995, Theorem 1.1: `1.302053^k`, for all sufficiently large `k`). -/
theorem preimage_count_ge_pow (a : ℕ) (ha : 0 < a) (ha3 : a % 3 ≠ 0) (k : ℕ) (hk : 20200 ≤ k) :
    (1333 / 1000 : ℝ) ^ k ≤
      ((Finset.Icc 1 (2 ^ k * a)).filter
        (fun n => (fun m : ℕ => if m % 2 = 0 then m / 2 else (3 * m + 1) / 2)^[k] n = a)).card :=
  (pow_le_of_bernoulli (by norm_num) (by norm_num) (by norm_num) hk (by norm_num)).trans
    (preimage_count_lower_bound a ha ha3 k)

end PreimageBound
