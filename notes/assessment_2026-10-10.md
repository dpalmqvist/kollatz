# Overall assessment of the project (2026-10-10)

A stock-take after the push of 2026-10-09/10. It covers what is proved, what is only numerical, what was tried and
failed, and what to do next. Details live in the files referenced; `AVENUES.md` is the living plan, `RESULTS.md`
the certified record, `notes/limit_function.md` the latest research log.

## 1. The goal, and how the targets nest

- **Collatz itself.** Since Mazur's positive-density theorem (formally verified, §2), Collatz is equivalent to "the
  set of integers whose orbit reaches 1 has upper density 1". Every counting method (Terras, Tao, Krasikov–Lagarias,
  Applegate–Lagarias, Mazur) produces "almost all" statements. None touches a single divergent orbit, and by
  Conway's undecidability any proof must use the specific arithmetic of 2 and 3. Nothing in this project is a route
  to the conjecture itself; that was clear before, and it remains so.
- **What our methods can reach:**
  - **uniform** predecessor exponents: Krasikov–Lagarias λ_k → 2 ⇔ ρ_k → 1 (avenue 1);
  - the uniform preimage-count conjectures of Applegate–Lagarias (B, C′), together with their Limit Function
    Conjecture (avenue 28);
  - explicit, uniform constants (avenues 17, 24);
  - conditional formal records for cycles (avenues 13, 26).

## 2. What is established (rigorous)

| Result | Status | Where |
|---|---|---|
| L^NT_k structure theorem: λ_k attained, 1 < λ_k < 2, tight and unique at λ_k, λ_k < λ_{k+1}, ρ_k = 3(λ_k − 1)/λ_k^α with 1 − ρ_k strictly decreasing. Settles K–L 2003's open problem and A–L 1995 Conj. 4.1. | proved; Lean 4, standard axioms only, `leanchecker`, independent kernel nanoda (v4.30 and v4.35) | `notes/strict_monotonicity.md`, `lean_formal/KLMonotone/`, `paper/monotone.md` |
| Certified K–L brackets for k ≤ 22: γ_22 ∈ [0.92509, 0.92517]. Lean instances at k = 18, 19, 20 (x^{0.914} ≤ π_a(x)). | exact integer certificates, two independent verifiers; Lean via `native_decide` | `RESULTS.md`, `certs/`, `lean_formal/` |
| Explicit uniform bounds: π_a(x) ≥ 0.7146 (x/a)^{0.848} for x ≥ 2^{6.25} a (a ≡ 2 mod 3, not on a cycle), and an explicit envelope up to the k = 22 exponent | rigorous (an earlier 0.865 was corrected to 0.8435) | `RESULTS.md`, `base_lift_chunked.py`, `certs/spread_k*` |
| Uniform preimage bounds: 0.2847·1.3331664^k ≤ n_k(a) for all a, k (Lean, `decide +kernel`, r = 14); 0.2822·1.3333119^k ≤ N*_k(a) ≤ 3.557·1.3333567^k (exact integer check, r = 19); exact extremal trees N^± to k = 59/55. Improves A–L 1995 Thm 1.1 (1.302/1.358). | proved / certified | `lean_formal/PreimageBound/`, `notes/extremal_trees.md`, `paper/preimage.md` |
| Audits of external work: Mazur's positive-density theorem (verified, including nanoda); the m ≥ 102 m-cycle repository; our extension to m ≤ 104 (≥ 105 local minima, given 2^71 and Rhin's bound), checked twice by Lean's kernel and once by nanoda | verified | `notes/m2_audit.md`, `notes/mcycles_102_audit.md`, `notes/mcycles_extension.md` |
| Limit measure. Consistency/martingale and a.e. limit W_∞ — **Applegate–Lagarias 1995, Thms 6.1, 6.3** (not ours). New: W_∞·Haar is the stationary law ν_{1/4} of x ↦ x/2, (3x+1)/2 with probabilities 3/4, 1/4; class averages of (3/4)^k N*_k → h_r; **Prop. 6: the A–L Limit Function Conjecture alone implies C′**; K–L at λ = 2 with mean instead of min is exactly Tao's Syracuse measure (p = 1/2); the density is unbounded on every ball for p > 1/3 | proved (short arguments) | `paper/preimage.md` §7, `paper/draft.md` §6.8 |

## 3. What is known only numerically (strong evidence, no proof)

- **λ_k → 2.** Undecided. 1 − ρ_k decays with a ratio creeping from 0.913 to 0.933 (k ≤ 22). Models with limits
  0.97 and 1 fit equally well.
  - New explanation: the linear version sits exactly at the L²-critical point (diagonal factor 3p/(2−p) = 1 at
    p = 1/2).
  - Its linear analogue is Tao's fine-scale mixing, which is proved. The difficulty is the minimum, at criticality.
- **A–L Limit Function and Extremal Limit Conjectures.** Strongly supported:
  - h_17 has 1/min = 2.0387 and max = 1.7386, against the exact extremal limits 2.039 and 1.742;
  - all L^q norms decay fast enough for a continuous density (Hölder exponent about 0.25).
- **The L² law.** ‖δ_n‖₂ shrinks by √(3p/(2−p)) per level (the diagonal term is exact; cross terms vanish
  numerically). This explains the 0.65-per-digit loss of the depth system.
- **Exponential Fourier decay of ν_{1/4}.** The true worst case is 0.64 per level. Tao's conditioning on triples, as
  a positive majorant over all characters, gives 0.72–0.75 per level for n ≤ 17. The extremisers are exactly the
  pure 2-power characters ±2^L/3^n.

## 4. What does not work, and why (do not re-try without a new idea)

- **Operator-norm certificates on arbitrary martingale differences.** The one-step norm is 1.0356 > 1, and m-step
  norms rise with the level. The decay is arithmetic, not a contraction property.
- **Transferring Tao's §6 to p = 1/4.** It relies on h(1/2) = 1 bit per unit of 2-adic size; p = 1/4 leaves a
  2^{0.30n} entropy deficit. It would need exponential Fourier decay below 0.84 per level, which Tao's §7 does not
  give.
- **Positive majorant certificates:**
  - pairs: borderline (0.85 per level on odd n);
  - distance-binned sup: 0.93 per level;
  - unweighted ℓ²: norm 1.07 at n = 13, rising;
  - budget-weighted ℓ²: worse.

  One mechanism defeats all of them. Along the pure 2-power chain near the identity the weights tend to 1, and its
  far lifts inherit large coefficients (the cosine factors are fixed values on the 27th roots of unity, about
  0.3–0.5).
- **Earlier dead ends (CLAUDE.md, AVENUES):**
  - scaling k beyond 22, because memory grows ×3 per level for +0.005 in γ;
  - compressing the vector, adaptive or sparse refinement, and the eliminated system L^EL at small k;
  - Hercher-style m-cycle bounds at 2^71 give exactly m ≤ 91, so progress there comes from new arguments, not
    from the verified range.

## 5. Assessment of the open targets

| Target | Difficulty | Realistic outlook |
|---|---|---|
| A–L Limit Function Conjecture ⇒ C′ (avenue 28) | best-placed theorem target; sub-goal 1 is absolute continuity of ν_{1/4}, sub-goal 2 is continuity | Absolute continuity: plausible, multi-day to multi-week. Needs a sharper majorant (longer blocks or the exact Fourier recursion; truth 0.38 vs majorant 0.56 per level in the typical case) or the analytic "digit budget" argument (no k buys more black steps than its n·log₂3 free bits; Baker-type bounds on returns near the identity). Continuity is harder still. |
| λ_k → 2 (avenue 1) | hardest; the minimum at the critical point | Low probability in the near term. The p = 1/4 work is the template; do it first. |
| Effective constants in Conjecture A (avenue 24) | technical | Possible, but Mazur's constants are tower-sized; moderate value. |
| m-cycles m = 105 (avenue 26) | computational, about 45 GB and 2 h of Lean | Incremental record; low priority. |
| Density one / Collatz | out of reach | Not a target. |

## 6. Recommendations, in order

1. **Consolidate and publish.**
   - `paper/monotone.md`: the structure theorem, self-contained and machine-checked; the fastest uncontested
     result.
   - `paper/preimage.md`: uniform preimage bounds, exact extremal data, and Prop. 6, crediting A–L 1995.
   - The main preprint `paper/draft.md`, repositioned around uniformity and explicitness (see
     `paper/repositioning_proposal.md`).
2. **Contact J. C. Lagarias** (co-author of both K–L 2003 and A–L 1995) with the structure theorem and the
   preimage paper. The 1995 conjectures are exactly what this work bears on.
3. **Avenue 28 as a longer research project.** First the sharper majorant (concrete and computational), then the
   digit-budget/Baker argument. Keep `notes/limit_function.md` as the log.
4. **Do not** pursue the dead ends of §4.

## 7. Trust, corrections and lessons

- Every claimed theorem is either machine-checked or a short written proof. Every computation is an exact
  integer certificate with an independent verifier. External, AI-generated or unrefereed claims (Mazur,
  msharpe248, the m ≥ 102 repository) were audited, not cited on trust.
- Corrections made during this push, all recorded in the respective files:
  - the base-lift constant 0.865 → 0.8435 (grid minimum vs rigorous infimum);
  - "Tao's method transfers to p = 1/4" was retracted after reading his §6;
  - "Proposition 5 appears new" was retracted once A–L 1995 §6 turned up.
- **Lesson:** check the specific prior literature, here A–L 1995 *The distribution of 3x+1 trees*, before calling
  an identification new. The cheapest check (one paper) came after the write-up, not before.

## Addendum (2026-10-10, late)

- **Avenue 29 (new): the 0.05-bit wall.** Cycles, divergence and density one all fail at the same constant,
  η = 1 − H(log 2/log 3) ≈ 0.050 bits per step. A counterexample lives where the random model predicts fewer than
  one integer, and counting methods cannot prove that such a count is zero. To be written as Theorem 4 of
  `notes/no_go_theorems.md`.
- **Avenue 25 downgraded.** A counterexample's component has density ≈ c/a (a = its least element), so an averaging
  proof of density one would need error o(1/a).
- **Avenue 30 (new): explicit ε.** Make Tao explicit with the 2^71 range: the non-convergent set has log density
  ≤ ε. First data (`syracuse_fourier.py`): the worst Fourier coefficient of Tao's ν_{1/2} is not exponentially
  small for n ≤ 17 (locally ≈ n^{−2.1}, maximiser ±2^L), unlike ν_{1/4}. Expect a modest ε.
- The recommended order (publish → Lagarias → avenue 28) is unchanged; avenue 30 is the natural proof-directed
  project after that, since it shares its hard lemma with avenue 28.
