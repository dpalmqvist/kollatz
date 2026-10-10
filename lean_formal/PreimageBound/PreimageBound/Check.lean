import PreimageBound.Basic
import PreimageBound.Kernel

/-!
# Soundness of the kernel-evaluated certificate check

`classOk_sound` translates `classOk … c = true` (see `PreimageBound.Kernel`) into the hypotheses of
`residue_class_bound_real`. A certificate is checked in chunks: one theorem `allRange f S (j·S) = true` per chunk,
so that each kernel check stays small. `cover_step` chains the chunks, and `lower_bound_of_check` gives the final
bound.
-/

namespace PreimageBound

lemma bcond_eq {α : Sort _} (b : Bool) (x y : α) : bcond b x y = cond b x y := by cases b <;> rfl
lemma band_eq (a b : Bool) : band a b = (a && b) := by cases a <;> rfl
lemma bor_eq (a b : Bool) : bor a b = (a || b) := by cases a <;> rfl

lemma bmin_eq (a b : ℕ) : bmin a b = min a b := by
  unfold bmin
  cases h : Nat.ble a b
  · have : ¬ a ≤ b := fun h' => by simp [Nat.ble_eq_true_of_le h'] at h
    simp [min_eq_right (by omega : b ≤ a)]
  · have : a ≤ b := Nat.le_of_ble_eq_true h
    simp [min_eq_left this]

lemma nat_beq_decide (x y : ℕ) : Nat.beq x y = decide (x = y) := by
  cases h : Nat.beq x y
  · exact (decide_eq_false (Nat.ne_of_beq_eq_false h)).symm
  · exact (decide_eq_true (Nat.eq_of_beq_eq_true h)).symm

theorem classOk_sound {r M t P Q Vmin Vmax : ℕ} {V : ℕ → ℕ} (hM : M = 3 ^ r) (ht : t = 3 ^ (r - 1))
    {c : ℕ} (h : classOk M t P Q Vmin Vmax V c = true) (hc : c % 3 ≠ 0) :
    Vmin ≤ V c ∧ V c ≤ Vmax ∧ P * V c ≤ Q * Phi r V c := by
  subst hM ht
  have h3 : Nat.beq (Nat.mod c 3) 0 = false := by
    rw [nat_beq_decide]; exact decide_eq_false hc
  simp only [classOk, bcond_eq, band_eq, bor_eq, h3, cond_false, Bool.and_eq_true, Nat.ble_eq,
    nat_beq_decide, ← Bool.decide_or, Bool.cond_decide, bmin_eq] at h
  obtain ⟨⟨h1, h2⟩, h4⟩ := h
  refine ⟨h1, h2, h4.trans (le_of_eq ?_)⟩
  simp only [Phi, lift, zero_mul, add_zero, one_mul]
  rfl

theorem allRange_spec (f : ℕ → Bool) (n : ℕ) :
    ∀ lo, allRange f n lo = true → ∀ i, lo ≤ i → i < lo + n → f i = true := by
  induction n with
  | zero => intro lo _ i h1 h2; omega
  | succ n ih =>
    intro lo h i h1 h2
    have h' : band (f lo) (allRange f n (lo + 1)) = true := h
    rw [band_eq, Bool.and_eq_true] at h'
    rcases Nat.eq_or_lt_of_le h1 with h1 | h1
    · subst h1; exact h'.1
    · exact ih (lo + 1) h'.2 i h1 (by omega)

theorem cover_step {f : ℕ → Bool} {n S : ℕ} (h : ∀ c < n, f c = true) (h' : allRange f S n = true) :
    ∀ c < n + S, f c = true := by
  intro c hc
  rcases Nat.lt_or_ge c n with h1 | h1
  · exact h c h1
  · exact allRange_spec f S n h' c h1 hc

theorem cover_zero (f : ℕ → Bool) : ∀ c < 0, f c = true := fun c hc => absurd hc (Nat.not_lt_zero c)

/-- A certificate that passes `classOk` on every residue below `3^r` gives
`(Vmin/Vmax)·(P/Q)^k ≤ #{n ∈ [1, 2^k a] : T^[k] n = a}` for every `a ≢ 0 (mod 3)` and every `k`. -/
theorem lower_bound_of_check {r M t P Q Vmin Vmax : ℕ} {V : ℕ → ℕ} (hr : 2 ≤ r) (hM : M = 3 ^ r)
    (ht : t = 3 ^ (r - 1)) (hQ : 0 < Q) (hVmax : 0 < Vmax)
    (h : ∀ c < M, classOk M t P Q Vmin Vmax V c = true) (a : ℕ) (ha3 : a % 3 ≠ 0) (k : ℕ) :
    ((Vmin : ℝ) / Vmax) * ((P : ℝ) / Q) ^ k ≤
      ((Finset.Icc 1 (2 ^ k * a)).filter (fun n => T^[k] n = a)).card := by
  have hs : ∀ c < 3 ^ r, c % 3 ≠ 0 → Vmin ≤ V c ∧ V c ≤ Vmax ∧ P * V c ≤ Q * Phi r V c :=
    fun c hc h3 => classOk_sound hM ht (h c (hM ▸ hc)) h3
  exact residue_class_bound_nk hr V P Q Vmin Vmax hQ hVmax (fun c hc h3 => (hs c hc h3).2.2)
    (fun c hc h3 => (hs c hc h3).2.1) (fun c hc h3 => (hs c hc h3).1) k a ha3

end PreimageBound
