# Avenues: what could be explored next, and where each stands

Living document. Each entry: the question, why it matters, what exists in this repository, how to pick it up,
and an honest estimate of the payoff. Dates are when the entry was last touched. See `CLAUDE.md` for the
technical state of the code and `RESULTS.md` for the certified results.

## Status board

| # | Avenue | Kind of payoff | Status (2026-10-08) |
|---|---|---|---|
| 1 | Prove λ_k → 2 (exponent 1 − ε) via the limit object | theorem about the method | measurements done, theory not started |
| 2 | Stronger inequality systems at small k | could change the slope of the whole program | started 2026-10-08, see below |
| 3 | The 3x+d family | publishable computations, sanity checks | not started |
| 4 | Cycle block search with residue dismissal | bits of verification range | designed, not started |
| 5 | Formalise k = 20, 21 in Lean | record becomes formal | needs 30 / 90 GiB machine or a collaborator |
| 6 | Wirsching's positive-density program | numerical test of an open conjecture | not started |
| 7 | Divergent orbits | new theorem, no known tool | not started, no concrete idea |
| — | Scaling k further | +0.005 in γ per step | stopped deliberately at k = 21 |

## 1. Prove that the Krasikov–Lagarias exponent tends to 1

**Question.** Does λ_k → 2? Krasikov–Lagarias (§6) show this is equivalent to π_a(x) ≥ x^(1−ε) for every ε, and
that it follows from ρ_k → 1, where ρ_k = (mean over auxiliary classes of the minimum over the three lifts) /
(mean of c). The summed inequality is tight on all our solutions, so λ_k is a function of ρ_k alone (`rho.py`).

**What we know numerically** (`rho.py`, `holder.py`, CLAUDE.md "Gränsobjektet").
- 1 − ρ_k falls from 0.0573 (k = 11) to 0.0258 (k = 21) with a successive ratio rising 0.913 → 0.931. Geometric,
  geometric-with-offset, stretched-exponential and power-law fits agree to 1e-4 and disagree on the limit
  (0.971, 1, 1). The data cannot decide.
- Dependence of c on ternary digit j decays geometrically in j; the per-digit factor in the bulk rises with k,
  0.828 (k = 12) → 0.875 (k = 19), increments halving every ~4 levels, extrapolating to roughly 0.94.
- Universal boundary layer: the Hölder exponent at distance d from the top digit is 0.665, 0.401, 0.293, 0.232,
  0.194 for d = 1 … 5, identical for every k to three decimals. Looks like a fixed point of "append a digit, then
  minimise over it". This is the most promising thing to try to prove.
- The limit is unbounded: max c / min c grows like 1.52^k; mass in the top 1 % of classes rises slowly. Any limit
  theory must work with measures / L¹, not bounded continuous functions.
- Limit inequality on X = {m ∈ Z_3 : m ≡ 2 mod 3} with Haar measure: c(m) ≤ λ^−2 c(4m) + λ^(α−2) c((4m−2)/3)·1[m≡2 (9)]
  + λ^(α−1) c((2m−1)/3)·1[m≡8 (9)]. Integrating gives 1 ≤ λ^−2 + ⅓(λ^(α−2) + λ^(α−1)) with equality exactly at λ = 2.
  So λ = 2 is the critical value of the limit problem and the finite-k deficit is precisely the min-loss 1 − ρ_k.

**Added 2026-10-08 (`limit_measure.py`).**
- Mass convergence: the total variation between the level-j marginals of μ_k and μ_{k+1} decays geometrically in
  k with ratio ≈ 0.91–0.93 (j = 4: 5.9e-3 at k = 12 → 3.6e-3 at k = 18), larger at finer j. Summable, so a limit
  measure on Z_3 exists (weak convergence at every fixed scale), approached at the same ~0.92 rate as 1 − ρ_k.
- The Perron vector of F at λ = 2 (finite k) and c_k at λ_k have log-correlation 0.9967 → 0.9978 and TV distance
  0.085 → 0.075 from k = 8 to 13, i.e. slowly converging shapes. The λ = 2 vector is 3× more spread and has
  larger digit oscillations, but a similar top-layer structure. Working hypothesis: the limit object is the λ = 2
  eigenmeasure of the 3-adic operator, and c_k → it.
- Linearisation (`jacobian.py`): at the Perron vector F is linear (the lift attaining each minimum is fixed), and
  the second eigenvalue modulus of that sparse matrix is 0.754, 0.838, 0.824, 0.857, 0.865, 0.861, 0.865 for
  k = 5 … 11, complex (rotational), with a dense cluster just below. This matches the per-digit decay factor
  (0.83 at k = 12 rising to 0.875 at k = 19), not the ~0.92 per-level rate, suggesting: digit influence decays at
  the mixing rate of the linearised dynamics. Spectral radius of F at λ = 2: 0.861, 0.880, 0.895, 0.910, 0.919,
  0.927, 0.933 (k = 5 … 11); 1 − r(F_2) shrinks by ~0.86–0.91 per level. Since lifting preserves feasibility,
  r_k(F_2) is monotone with limit r∞ ≤ 1, and λ_k → 2 ⇔ r∞ = 1. This is a cleaner sequence to extrapolate than
  λ_k; values for k = 12 … 21: 0.93984, 0.94505, 0.94998, 0.95450, 0.95852, 0.96209, 0.96524, 0.96807, 0.97062,
  0.97291 (`rF2_fit.py`). Successive ratios of 1 − r_k rise monotonically from 0.905 (k = 12) to 0.922 (k = 21).
  Geometric-with-offset (limit r∞ = 0.9929, i.e. λ∞ < 2) and stretched-exponential (r∞ = 1) fit all 17 points to
  1.6–1.8e-4; fitted on k ≤ 16 both under-predict the slowing at k = 21 (errors −3.6e-4 and −5.9e-4), the offset
  model less so. Verdict as of 2026-10-08: the data lean slightly towards "the approach to 1 keeps slowing", but
  cannot distinguish a limit below 1 from a sub-geometric approach to 1. More k will not settle it; theory must.
- Exact identity (checked to 7 decimals, k = 8 … 13): r_k(F_2) = 1/4 + (3/4)·ρ'_k, where ρ'_k is the mixing ratio
  of the λ = 2 Perron vector itself. So "λ_k → 2" ⇔ "r_k(F_2) → 1" ⇔ "the λ = 2 eigenvector becomes insensitive
  to its top digit in the mean". The λ = 2 eigenvector is the natural object: a sufficient condition is that the
  Perron vector v_k of the exact (min-free) operator G_k, which is column-stochastic with spectral radius exactly 1
  at λ = 2, has uniformly vanishing top-digit sensitivity, since F_2(v_k) ≥ (1 − max_i loss_i/v_i) v_k
  (Collatz–Wielandt). The ×4 term carries top-digit information without loss; the aux term maps the new top
  digit of m to the top digit of the aux class at the level below; the min destroys it. Deriving the recursion
  for the top-digit sensitivity profile across levels is the concrete next analytic step.

**Renormalisation of top-digit sensitivity (2026-10-08, `renorm.py`).** Tile c_k to level k+1 (sensitivity 0),
apply F once: the injected top-digit sensitivity is exactly (3/4)·s_k at λ = 2 (0.69–0.71 at λ_k), because the
mean of F(tile c) is preserved and only the aux term (mass fraction 3/4) selects lifts by the new digit. Iterating
to the fixed point c_{k+1} amplifies it by A_k = s_{k+1}/((3/4)s_k) = 1.199, 1.212, 1.210, 1.206, 1.218 for
k = 8 … 12 (λ = 2), and from the r_k(F_2) series A_k rises to 1.229 at k = 21. The per-level ratio of 1 − r_k is
(3/4)·A_k. Hence: λ_k → 2 iff A∞ < 4/3; the ratio → 1 (and λ∞ < 2) iff A_k → 4/3. The amplification comes from the
×4 term re-circulating top-digit variation with weight 1/4 (A = 1/(1 − e/4) if a fraction e of it survives), and
e < 1 only because the ×4-term and aux-term variations over the top digit are not aligned (min of a sum exceeds
the sum of mins). So the question is whether the two terms' argmins become aligned as k → ∞ (`renorm2.py`).
The whole digit profile shifts up by factors 1.01 (bottom) … 1.4 (top) when a level is added.

**Alignment efficiency (2026-10-08, `renorm2.py`, λ = 2).** Write the fixed point as c = P + Q with P the ×4
term (mass fraction 0.275 → 0.262 for k = 8 … 15, tending to 1/4) and Q the aux term. The fraction e_k of the
×4 term's top-digit variation that survives in the sum is 0.614, 0.666, 0.692, 0.705, 0.715, 0.724, 0.731, 0.737
(k = 8 … 15), then 0.742, 0.746 (k = 16, 17); increments shrinking roughly geometrically (0.013, 0.010, 0.010,
0.007, 0.006, 0.005, 0.004), A_k = 1.213, 1.216, 1.219 for k = 15 … 17. The argmins of P
and Q over the top digit agree on 0.33 of the classes, i.e. exactly as if independent, and this does not drift.
So e stays below 1 for a structural reason (two independent-looking variations of comparable size, s(Q)/s(c) ≈ 1.09),
and the per-level ratio of 1 − r_k should saturate at (3/4)/(1 − e∞/4). With e∞ ≈ 0.78–0.80 that is ≈ 0.935–0.94,
below 1. **Prediction:** the observed ratios (0.905 → 0.922 at k = 21) keep rising but level off near 0.94 rather
than approaching 1; then 1 − r_k decays geometrically and λ_k → 2. This is the first mechanistic argument for
exponent 1, and it is testable at k = 22–23 on a larger machine (two more ratios). What a proof would need: show
that the argmin agreement stays bounded away from 1 and the variations of P and Q stay comparable, in the limit measure.
At λ_k from the certified vectors (k = 12 … 18): e_k = 0.678, 0.689, 0.697, 0.704, 0.710, 0.716, 0.721, argmin
agreement 0.332–0.333 throughout; extrapolations e∞ = 0.753 (geometric), 0.807 (1/k), 0.754 (1/k²). The
first-order model ratio (mQ/mc)/(1 − e·mP/mc) gives 0.875 → 0.900 against observed 0.920 → 0.928, so the model
under-predicts by ≈ 0.03 (higher-order recirculation through the second digit is missing); the asymptotic ratio is
therefore likely ≈ 0.95–0.97, still below 1 as long as e∞ < 1. The structural reason e∞ < 1 is the independence of
the two argmins (agreement exactly 1/3 at every k). Caveat: a heuristic, not a proof; the offset-model fit of
1 − r_k (limit 0.0071) remains numerically indistinguishable from this picture up to k = 21.

**Related literature.** Applegate–Lagarias "Density bounds I" conjecture (Conjecture A) that all predecessor trees
have leaf counts growing like (4/3)^k uniformly; a 2026 GitHub repo (neljaouh/ConjectureA) claims Lean proofs of
"Conjecture A and the 3x+1 growth exponent conjecture" — unverified, but if true it would make λ_k → 2 plausible.

**How to pick up.**
1. Measure convergence of the mass distribution μ_k(class) = c_m / Σc on 3-adic balls across k (total variation
   between level-j marginals of consecutive k). If it converges, a limit measure exists.
2. Compare the Perron vector of F at λ = 2 (finite k, spectral radius < 1 but the eigenvector exists) with c_k at
   λ_k. If the shapes agree, the limit object is the λ = 2 eigenmeasure of the 3-adic operator.
3. Write the top-digit renormalisation map explicitly (c_k ↦ profile of oscillation at distance d from the top) and
   look for its fixed point analytically; the five universal numbers are the target.
4. Decide whether the per-digit factor converges to r∞ < 1. If so, 1 − ρ_k eventually decays geometrically and
   λ_k → 2 follows from the summed inequality.

**Payoff.** The goal Applegate–Lagarias set in 1995. Hard; nobody else is attacking it from the Perron-vector side.

## 2. Stronger inequality systems at small k

**Question.** Krasikov–Lagarias believe L^NT_k extracts everything from their inequalities I_k. But I_k is one
choice of what to count. Is there a different finite system, valid by the same kind of argument, with a larger λ at
equal k? If yes, the slope of the whole program changes; if no, that is worth knowing too.

**Structural note (2026-10-08).** The K–L recursion is exact except at two points: the infimum over the residue
class (uniformity over a within a class mod 3^k) and the minimum over the three lifts. Both are finite-k
truncation effects. Counting π_a (all paths) instead of π*_a (paths staying ≤ x) gives the same recursion
because the predecessor tree partitions exactly. Weighting counts by (n/x)^s changes nothing because every subtree
is weighted relative to the same x. Residues mod 2^j add nothing because the branching depends on m mod 3 only.
Non-uniform refinement (adaptive tree) was tested and rejected (`adaptive.py`). So within "count predecessors by
residue class", the system is canonical, and the open question is only how much the truncation costs.

**Experiment.** Measure actual predecessor-tree growth for integers a in the extremal classes (smallest and
largest c_m at k = 11) by exact BFS up to 2^28 and compare the fitted exponents with γ_11 = 0.8418
(`tree_growth.py`). If real trees in the worst class grow like x^0.99, the truncation loss is what remains and is
shrinking; if some class grows like x^0.9, the uniform bound is near its ceiling.

**Result (2026-10-08, `tree_growth.py 9 13`).** Exact BFS of predecessor trees for a in the two lowest-weight
classes (c_m ≈ 1), the three highest (c_m ≈ 43) and two random classes at k = 9, three a per class, trees up to
a·2^13 (≤ 9 million nodes), exponent fitted over y ∈ [7, 13]: every class grows with exponent 0.94–1.08, i.e.
≈ 1 within the noise of this short range, against γ_9 = 0.8168 from the LP. The lowest-weight classes have trees
50–200× thinner in absolute count but the same exponent. So the LP exponent is far below the real growth of
every class, and the gap is the finite-k truncation (the two losses named above), not a weakness in what is
counted. Avenue 2 therefore collapses into avenue 1: there is no stronger system at fixed k to look for; the
question is how fast truncation loss vanishes with k. The ratio count/(c_m·λ_k^y) varies by a factor ~50 across
classes, so the LP weights c_m are not predictive of individual tree sizes, only a certificate.

**How to pick up.** Only if one wants the certificate itself sharper at fixed k: consider the L^EL_k (elimination) system of K–L §3–4 for k ≤ 9 with
`lp_check.py` as a template; K–L saw no gain for k ≤ 5.

## 3. The 3x+d family

**Question.** For T_d(n) = n/2 or (3n+d)/2 with gcd(d, 6) = 1, cycles exist (several for d = 5, 7, …) and are
conjectured finite in number for each d. Do the predecessor exponents λ_k(d) and the cycle bounds behave like d = 1?

**Why.** Everything here transfers with small changes: `kl.py`/`kl_mlx.py` (indexing changes with d), `cycles.py`
(Eliahou's inequality with d), `cycle_dip.py`. A classification of cycles and predecessor exponents across d is
publishable and tests which features are special to d = 1. It is also a sanity check for any claimed argument:
if it would prove something false for 3x+5, it is wrong.

**Results (2026-10-08).**
- `kl_d.py`: the K–L LP for 3x+d is isomorphic to the d = 1 LP under m ↦ d·m′ (the class conditions
  m ≡ −d, 2d, 5d (mod 9) map to 2, 2·… exactly), so λ_k(d) = λ_k(1) for every d, confirmed numerically to
  7 decimals for d = 1, 5, 7, 11, 13 and k ≤ 7 with an independently coded d-structure. The method is blind to d:
  it measures tree growth exponents, which are 1 for every d, not densities or cycle structure.
- `cycles_d.py`: brute-force cycle catalogue for d ≤ 29 (minimum ≤ 3·10^5). Every cycle satisfies the generalised
  Eliahou inequality k·log2(1 + d/(3M)) ≤ n − k·log2 3 ≤ k·log2(1 + d/(3m)), with the trivial 2-cycle {d, 2d}
  sitting exactly on the upper bound. Several d have many cycles sharing one (n, k): 3x+13 has seven 8-step cycles
  with 5 odd steps and distinct minima 211 … 319, so the cycle equation m(2^n − 3^k) = S(v) has many solutions
  at the same (n, k). This is the right test bed for the cycle block search (avenue 4): a method that cannot
  reproduce the 3x+13 cycle list is wrong.

**How to pick up.** Tree-growth exponents for 3x+d (expected 1), cycle bounds à la Hercher for d = 5, 7, and the
question which (n, k) pairs admit cycles for which d.

## 4. Cycle block search with residue dismissal

**Question.** Hercher (2023) excludes the first admissible cycle length with verification to 3·2^69 by a five-week
case analysis. Can a block search with our exact linear forms, the height and dip bounds and his residue
dismissal gain two to three bits, bringing the next pair within reach of a continued verification campaign?

**What exists.** `cycles.py` (Eliahou's bound reproduced exactly; admissible pairs at 2^40, 2^60, 2^68, 2^71),
`cycle_harmonic.py` (height DP, f = 0.72, 0.47 bits), `cycle_dip.py` (off-cycle predecessor dips per residue
class), `cycle_lp.py` (joint flow LP, saturates at 0.38 bits). Hercher's paper text is in the scratchpad; the key
ingredient we lack is: a parity pattern of length j is realised only by one residue class mod 2^j, and when its
smallest member exceeds the needed bound the case is dismissed (Lemma 8: k consecutive odd steps ⇒ n ≡ −1 mod 2^k).

**Numbers.** Excluding pair 2 (217 976 794 617 steps) needs X0 ≥ 2^75.4 crudely, 2^74.1 at Hercher's level; the
verified range is 2^71. Each bit halves the remaining verification work.

**Payoff.** Service to the field, not a theorem. Days to weeks, parallelisable.

## 5. Formalise k = 20 and 21

Our vectors are in Mazur's format (`export_mazur.py`), the potentials are generated (`potential.py`, k = 20 done,
max 38; k = 21 needs ~14 GB RAM to generate) and the loop checker (`LoopCheck.lean`) is proved. Memory for the
native_decide checks: ~30 GiB (k = 20), ~90 GiB (k = 21). Either rent a machine or send the vectors and
`lean_formal/` to Mazur or msharpe248. The re-tuning lesson applies: the vector must be power-iterated at the
target λ = 2^(p/q) before export.

## 6. Wirsching's positive-density program

Wirsching (2003) gave five conjectures whose conjunction implies positive predecessor density for every target.
Tavares (arXiv:2608.27617, Aug 2026, unrefereed) claims two of them. The remaining ones concern asymptotics of
path-counting generators that our GPU code could test numerically to high precision. A careful numerical check of
an open conjecture in an unrefereed preprint is useful even if it proves nothing.

## 7. Divergent orbits

Nothing known excludes a single divergent orbit; Tao leaves them as a logarithmic-density-zero set. The only solid
structural fact: a divergent orbit must have odd-step density exactly log 2 / log 3, so its parity sequence is
Sturmian-like (critical). Do not start here without a specific idea; the territory is full of failed attempts.

## Not avenues

- Scaling k: +0.005 in γ per level for 3× memory. Stopped at 21; 22 needs 64 GB, 23 needs 192 GB.
- Compressing c or refining sparsely: both tested and rejected (CLAUDE.md "Gränser", `adaptive.py`).
- Proving the conjecture through any of the above: all are density or cycle statements; none touches divergent orbits.
