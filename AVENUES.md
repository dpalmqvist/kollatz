# Avenues: what could be explored next, and where each stands

Living document. Each entry: the question, why it matters, what exists in this repository, how to pick it up,
and an honest estimate of the payoff. Dates are when the entry was last touched. See `CLAUDE.md` for the
technical state of the code and `RESULTS.md` for the certified results. A referenced literature survey of
everything adjacent (cycle bounds, predecessor density, the long shots, formal verification) is in
`reports/Collatz adjacent work and references.md` (2026-10-08, notes in `research_notes/`).

## Strategic update 2026-10-10: Conjecture A is formally verified (Mazur)

The ProofAtlas formalisation "Positive Lower Density of Collatz Predecessors" (L. Mazur, Sept 2026, AI-generated,
unrefereed) was audited overnight. Details in `notes/m2_audit.md`; build tree in `~/devel/mazur_dl/m2/`.
- Rebuilt cold from the published sources; the sha256 values match.
- `leanchecker` and `leanchecker --fresh` pass.
- Only the three standard axioms are used.
- An independent restatement, with our own Collatz map and a `Finset` count, is derived in Lean
  (`m2/audit/AuditMain.lean`, `AuditM2.conjectureA`); I re-ran it myself.
- An **independent kernel** (nanoda 0.4.17, Rust) replayed the full exported closure: 43 862 declarations, no
  errors (2026-10-10). This also rules out the pre-fix Lean kernel bug #14576 (addendum in `notes/m2_audit.md`).

So, unless Lean's kernel is unsound: for every a ≢ 0 (mod 3), π_a(x) ≥ c_a·x for x ≥ X0(a), with c_a ineffective.
Also formal (their Cor. 1.2): if any n fails to reach 1, the non-convergent starts have positive lower density.
Hence Collatz ⇔ P(1) has upper density 1.

Consequences for this document:
- **Superseded as statements about π_a:** every x^γ bound (ours included) for each *fixed* a.
- **Not superseded: uniformity in a.** Mazur's c_a depends on a in an ineffective way. K–L bounds are uniform:
  φ_k^m(y) = inf over all a ≡ m (mod 3^k) of π*_a(2^y a) ≥ Δ c^m λ^y, so π_a(x) ≥ Δ (x/a)^γ for all a at once.
  Whether the *uniform* exponent is 1, i.e. inf_a log π*_a(2^y a)/y → 1, is still open and is exactly what
  λ_k → 2 would give (avenue 1). Applegate–Lagarias Conjectures B/C (uniform (4/3)^k tree counts) are of this
  uniform type. Avenue 1 therefore keeps its meaning, as the uniform-in-a question.
- **Avenue 6 (Wirsching):** its goal, positive predecessor density, is reached by a different route.
- **Avenue 17:** its (A) is done. The three-statement decomposition collapses to the single statement
  "P(1) has upper density 1". Cycles need not be excluded separately, because a cycle's predecessors would be
  non-convergent with positive density.
- **Still ours:**
  - the structure theorem of avenue 22 (proved and machine-checked);
  - explicit uniform-in-a bounds with small cutoffs (avenue 17: π_a(x) ≥ 0.7146·(x/a)^{0.848} for x ≥ 2^{6.25} a, 2026-10-10);
  - effective c_a (Mazur's are ineffective for general a and tower-sized for a = 1);
  - the cycle track.

New avenues 23–25 below follow from this.

## Status board

| # | Avenue | Kind of payoff | Status (2026-10-08) |
|---|---|---|---|
| 1 | Prove λ_k → 2 (exponent 1 − ε) via the limit object | theorem about the method | theory started 2026-10-09: boundary layer reduced to 1 − ρ_k (`boundary_layer.py`); defect D_k measured, exact identity δ_k = g(ρ_k − ρ′_k), argmins independent (`defect.py`); λ_k and q_k are mean-field: random fine alignments change λ_14 by −2e-3 and q_k not at all (`meanfield.py`) |
| 2 | Stronger inequality systems at small k | could change the slope of the whole program | started 2026-10-08, see below |
| 3 | The 3x+d family | publishable computations, sanity checks | not started |
| 4 | Cycle block search with residue dismissal | bits of verification range | designed, not started |
| 5 | Formalise k = 20, 21 in Lean | record becomes formal | needs 30 / 90 GiB machine or a collaborator |
| 6 | Wirsching's positive-density program | numerical test of an open conjecture | not started |
| 7 | Divergent orbits | new theorem, no known tool | not started, no concrete idea |
| 8 | 5x+1 as a calibration case for avenue 1 | second instance of the same question | k ≤ 14 done; REFRAMED 2026-10-09: the K–L ceiling for 5x+1 is the branching exponent 0.650919, so it is not a known-answer case (§8) |
| 9 | Dual certificates: λ_k is optimal at level k | exact λ_k, confirms K–L's optimality belief | DONE for k = 2 … 22 (2026-10-08/09): `certify_fast.py --upper`, `kl_split.py certify --upper`, brackets in RESULTS.md |
| 10 | Explicit constants in the predecessor bound | tables comparable with real counts | proposed 2026-10-08 |
| 11 | 3x+d cycle census at scale | tests Belaga–Mignotte conjectures | proposed 2026-10-08 |
| 12 | Terras's coefficient stopping time conjecture | compute upgrade | largely pre-empted: Rozier–Terracol 2026 reach 2.8·10^19 (lit. search 2026-10-08) |
| 13 | m-cycle bounds with the 2^71 verified range | publishable increment on Hercher's m ≤ 91 | DONE 2026-10-10 (`mcycles.py`, `notes/mcycles_2_71.md`): negative. X0 = 2^71 still gives exactly m ≤ 91; m = 92 needs X0 ≥ 2^73.87. Hercher and SdW reproduced, with two misprints found. The unrefereed m ≥ 102 claim rests on a new argument, not on the range; the unrefereed m ≥ 102 Lean repository AUDITED: formally valid given 2^71 + Rhin (leanchecker + nanoda; `notes/mcycles_102_audit.md`); EXTENDED to m ≤ 104 (≥ 105 local minima) in Lean, conditional on 2^71 + Rhin (`notes/mcycles_extension.md`) |
| 14 | Matrix interpretations for the rewriting system | a success would be a proof; odds very low | proposed 2026-10-08 |
| 15 | Applegate–Lagarias extremal trees to depth 45–50 | direct test of Conjectures C / C′ | DONE 2026-10-10 (`extremal_trees.py`, `notes/extremal_trees.md`): exact N^−(k) to k = 59, N^+(k) to 55; Thm 1.1 → (1.317329)^k … (1.346858)^k; residue-class certificate gives UNIFORM 0.2822·(1.3333119)^k ≤ N*_k(a) ≤ 3.556·(1.3333567)^k (independently re-checked at r = 13) |
| 16 | Spectrum, gap and traces of the K–L transfer matrix | mixing rate vs k; cycle footprints | first results 2026-10-08 (`spectrum.py`, k ≤ 15): gap does NOT close, see §16 |
| 17 | Three-statement decomposition: Conjecture A + density-1 boundedness + no cycles ⇒ Collatz | a full proof from three density/Diophantine statements | started 2026-10-09: minimal spread at fixed λ is bounded in k (`spread_iter.py`), t*_∞(λ) ~ (2 − λ)^{−2}; lifted base case (`base_lift.py`) removes most of the spread penalty: certified π_a(x) ≥ 0.865 (x/a)^{0.799} for x ≥ 64a; Conjecture A ⇐ λ_k → 2 + uniform base constant |
| 18 | No divergence as an arithmetic property of the 2-adic parity map (Q(ℤ) ⊆ ℚ) | settles divergence for integers | first data run 2026-10-09 (`parity_stats.py`, n < 2^32, in progress); by Terras the local gap statistics carry no information, see §18 |
| 19 | All cycles by equidistribution of numerators mod 2^n − 3^k | settles cycles for all m | first step done 2026-10-09 (`cycle_numerators.py`, n ≤ 32): equidistributed at random level exactly where m ≪ 2^n (the cycle regime); intrinsic bias for m ≈ 2^n |
| 20 | Adelic ℤ₂ × ℤ₃ picture and a Furstenberg-type rigidity theorem | explains the difficulty and would kill divergent orbits | proposed 2026-10-09 |
| 21 | Map the no-go theorems; termination with residue-labelled K–L orderings | delimits where a proof can live; one mechanical route | (i) done 2026-10-09: `notes/no_go_theorems.md` (Theorems 1–3 from Terras: no residue-class, bounded-lookahead or residue-monotone potential, violations of positive density); (ii) not started |
| 22 | Structure theorems for L^NT_k: attainment, tightness, uniqueness, strict increase | first theorems of the project; settles K–L 2003's open problem and A–L 1995 Conj. 4.1 | PROVED and machine-checked 2026-10-10 (`notes/strict_monotonicity.md`, `monotone_check.py`, `lean_formal/KLMonotone/`, standard axioms only); quantitative version = avenue 1 |
| 23 | Mazur's seed averaging vs the K–L minimum: an LP for a chosen seed class | effective Conjecture A | proposed 2026-10-10 |
| 24 | Effective constants for Conjecture A (verification range 2^71 as input) | explicit c_a | proposed 2026-10-10 |
| 25 | Density one of P(1), the single remaining statement (Mazur Cor. 1.2) | Collatz | proposed 2026-10-10 |
| 26 | Generalise the two-rise bound (r-rise, LP over shapes) for formal m-cycle records | conditional formal m-cycle record | proposed 2026-10-10 |
| 27 | Primitive-necklace heuristic with local factors for cycle counts (test on 3x+d) | falsifiable cycle model | proposed 2026-10-10 |
| 28 | Depth K–L system: prove ρ_r → 1 (faster-mixing model of avenue 1) ⇒ Conjectures B, C′ | theorem; testbed for avenue 1 | certified bounds to r = 19; 2026-10-10: Perron vectors = marginals of one 3-adic stationary measure (p = 1/4; K–L = Tao's p = 1/2), rate 0.65 = √(3/7) explained, C′ reduced to continuity of its density (`syracuse_measure.py`) |
| — | Scaling k further | +0.005 in γ per step | k = 22 certified 2026-10-08 (γ = 0.9251) plus upper certificate; k = 23 needs ~192 GB |

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
  the mixing rate of the linearised dynamics. **Revised 2026-10-08 (§16):** the second eigenvalue stays at ≈ 0.865 for
  k = 8 … 14 while the per-digit factor drifts upward, and v₂ is delocalised across digits; the linear mixing rate is
  therefore not what sets the k-dependence of 1 − ρ_k — the argmin/alignment mechanism below is. Spectral radius of F at λ = 2: 0.861, 0.880, 0.895, 0.910, 0.919,
  0.927, 0.933 (k = 5 … 11); 1 − r(F_2) shrinks by ~0.86–0.91 per level. Since lifting preserves feasibility,
  r_k(F_2) is monotone with limit r∞ ≤ 1, and λ_k → 2 ⇔ r∞ = 1. This is a cleaner sequence to extrapolate than
  λ_k; values for k = 12 … 21: 0.93984, 0.94505, 0.94998, 0.95450, 0.95852, 0.96209, 0.96524, 0.96807, 0.97062,
  0.97291 (`rF2_fit.py`). Successive ratios of 1 − r_k rise monotonically from 0.905 (k = 12) to 0.922 (k = 21).
  Geometric-with-offset (limit r∞ = 0.9929, i.e. λ∞ < 2) and stretched-exponential (r∞ = 1) fit all 17 points to
  1.6–1.8e-4; fitted on k ≤ 16 both under-predict the slowing at k = 21 (errors −3.6e-4 and −5.9e-4), the offset
  model less so. Verdict as of 2026-10-08: the data lean slightly towards "the approach to 1 keeps slowing", but
  cannot distinguish a limit below 1 from a sub-geometric approach to 1. More k will not settle it; theory must.
  **k = 22 added (2026-10-08 evening, `kl_split.py rate 22 2`):** r_22(F_2) = 0.974971, ρ at λ = 2 is 0.966628 and
  the identity r = 1/4 + (3/4)ρ′ holds to 7 decimals at N = 10^10. Ratio of 1 − r_k: 0.9239 (k = 21: 0.9221, k = 20:
  0.9202) — still rising by ≈ 0.0018 per level, no levelling yet. Fits on k = 5 … 22: geometric + offset (limit
  1 − r∞ = 0.0072) and stretched exponential (limit 0) both at max residual 1.8e-4; blind from k ≤ 16 the offset model
  misses k = 22 by −4.3e-4, the stretched by −7.5e-4, pure geometric by −1.5e-3. The renormalisation prediction of
  §1 (ratios level off near 0.94) is not contradicted: at the current rate 0.94 would be reached around k = 31.
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

**Related literature (corrected 2026-10-08, see `reports/Collatz adjacent work and references.md`).** In
Applegate–Lagarias, "Density bounds for the 3x+1 problem I", Math. Comp. 64 (1995) 411–426, Conjecture A is
*positive density* (π_a(x) ≥ c_a x); the (4/3)^k statements are Conjecture B (n_k(a) = (4/3)^{k(1+o(1))},
Lagarias–Weiss), C (both extremal pruned-tree counts N^±(k) are (4/3)^{k(1+o(1))}) and C′ (bounded max/min ratio),
and they note C′ fails for the random branching models. The 2026 GitHub repo neljaouh/ConjectureA (Lean, kernel-clean)
derives Conjecture A and the Kontorovich–Lagarias growth-exponent conjecture entirely from Mazur's unreviewed ProofAtlas
"positive lower density" theorem (6 Sep 2026); if that upstream is sound it supersedes every x^γ statement, so it is the
one external claim worth a human expert's attention. No refereed or preprint progress on K–L §6 (λ_k → 2) exists;
Lagarias's overview (arXiv:2111.02635) still lists π_1(x) > c(ε)x^{1−ε} as open.

**Boundary layer explained to first order (2026-10-09, `boundary_layer.py`).** Let R(c) be c minimised over
its top ternary digit and renormalised to mean 1 (a vector on level k − 1). Then R(c_k) ≈ c_{k−1}. The TV distance is
0.0126 (k = 8) → 0.0045 (k = 17), four times smaller than TV(c_k, tile c_{k−1}), and it decays with 1 − ρ_k (ratio
≈ 0.13 throughout). R² behaves the same way against c_{k−2}. Consequence: the ball oscillation with d free top
digits equals the d-step loss of the chain c_k → c_{k−1} → …, so osc_k(d) ≈ Σ_{i<d} (1 − ρ_{k−i}). At k = 17:
osc = 0.0347, 0.0720, 0.1118, 0.1543, 0.1991 against partial sums 0.0347, 0.0722, 0.1129, 0.1571, 0.2053. The
"universal" exponents are then β(d) = log_3(S(d+1)/S(d)) of these partial sums. With 1 − ρ_k ≈ q^k they are
log_3((1 + … + q^−d)/(1 + … + q^−(d−1))): about log_3 2, log_3 1.5, … pulled up slightly by q ≈ 0.92. The model gives
0.668, 0.407, 0.301, 0.243 against the observed 0.665, 0.401, 0.293, 0.232. It is right to 0.003–0.011, with the
error growing in d. **So the boundary layer is not an independent fixed point. It is the 1 − ρ_k sequence seen
through the coarse-graining R**, and the five numbers carry no information beyond the ratios of 1 − ρ_k. Two caveats.
The observed β(d) are k-independent to three decimals, while the partial-sum model drifts by ~0.005 over k = 11 … 17,
so a second-order effect makes the exact profile more universal than the model. And R(c_k) is *not* feasible at
level k − 1: min over the top digit of a sum is at least the sum of the mins, which is the wrong direction. The defect
is the ×4/aux misalignment of `renorm2.py`. This is where the theory has to go: the exact relation between R(c_k) and
c_{k−1}, i.e. the size of R(F_k(c)) − F_{k−1}(R c), now decides whether 1 − ρ_k → 0.

**The defect measured (2026-10-09, `defect.py`, k = 6 … 19 in float64; k = 20, 21 means only).** Write D_k =
R(F_k c_k) − F_{k−1}(R c_k) with R = min over the top digit (so R c_k = c̄, the auxiliary vector, a level-(k − 1)
vector) and both maps at λ_k. Exact facts first. For level-(k − 1) index r the three level-k rows r + tN/3 have ×4 term
λ^{−2} c[lift_s(4r+2)] and aux term L_j c̄[lift_{s′}(aux r)], with s, s′ permutations of t; hence D_k ≥ 0 pointwise,
D_k = 0 on class 5 and wherever the two argmins agree, and D_k is exactly the ×4/aux misalignment of `renorm2.py`.
Since F_k c_k = c_k, c̄ = F_{k−1}(c̄) + D_k: c̄ is a strict super-solution at level k − 1. Taking means with the
summation identity at level k − 1 gives the **exact identity**

  δ_k := mean D_k / mean c̄ = g(λ_k) (ρ_k − ρ′_k),   g = (λ^{α−1} + λ^{α−2})/3,   ρ′_k = mean(R² c_k)/mean(R c_k),

verified to all printed digits at every k. With q_k = (1 − ρ_k)/(1 − ρ_{k−1}) and the second-level excess
e_k = ρ_{k−1} − ρ′_k (R c_k is lossier at its top digit than c_{k−1} is) this reads
δ_k /(g(1 − ρ_k)) = (1 − q_k)/q_k + e_k/(1 − ρ_k). **So the mean defect is bookkeeping: it carries nothing beyond the
loss sequence and e_k.** Data:

| k | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 |
|---|---|---|---|---|---|---|---|---|---|---|
| q_k | 0.913 | 0.920 | 0.919 | 0.920 | 0.922 | 0.924 | 0.927 | 0.928 | 0.930 | 0.931 |
| e_k ×10³ | 2.49 | 2.30 | 1.79 | 1.47 | 1.29 | 1.13 | 1.03 | 0.92 | 0.82 | 0.75 |
| e_k/(1 − ρ_k) | 0.048 | 0.048 | 0.040 | 0.036 | 0.034 | 0.033 | 0.032 | 0.031 | 0.030 | 0.029 |
| δ_k/(1 − ρ_k) | 0.104 | 0.099 | 0.095 | 0.091 | 0.088 | 0.085 | 0.082 | 0.080 | – | – |

e_k decays at the same rate as 1 − ρ_k (ratio 0.89–0.92) and its share falls slowly; q_k rises by ≈ 0.002 per level
with no sign of levelling off (linear continuation would reach 1 near k ≈ 60). The question is still q_k → q∞ < 1
(geometric, ρ_k → 1) or q_k → 1 (sub-geometric: offset or stretched exponential, undecided).

The **pointwise structure** is where the new information is, and it is clean:
- The two argmins are independent. P(agree) = 0.332 for k ≥ 13 (class 2: 0.328, class 8: 0.334), both marginals
  uniform to 0.001, max |joint − product| = 0.002. Which lift wins is a fine-digit property: given the lowest four
  digits of r the best guess of either argmin is right 0.337 of the time (1/3 = uninformative).
- The expected size of the defect is a coarse-residue property. The conditional mean of D given the top digit is
  uniform to 10^{−3} at every k ≥ 15; the spread of the conditional mean over a single digit, relative to δ_k, is 2.17
  (digit 0, i.e. the class), 0.60, 0.31, 0.21 for digits 1–3 and below 0.06 from digit 4 on. The lowest 8 digits
  explain 24 % of the variance of D, the top 6 digits 0.04 %.
- The excess splits 64–65 % ×4 term, 35 % aux term, constant in k. Given misalignment, D/c̄ averages 0.008 (k = 15);
  the 99 % quantile of D/c̄ is 0.022 and the maximum 0.24 at k = 19. The defect is uncorrelated with the local spread
  of c over the three lifts (correlation −0.02 → −0.013).
So the defect is the product of two independent fine-scale choices whose expected size is fixed by the residue
mod 3^4: exactly the mean-field structure `renorm2.py` assumed, now seen pointwise. **Where the theory has to go:**
derive the one-step recursion for 1 − ρ_{k+1} from level-k quantities under the independence hypothesis (the aux term
injects second-digit sensitivity, the ×4 term transports top-digit sensitivity, the minimum removes a fraction) and
test it against q_k and e_k; a proof of independence plus a contraction estimate for that recursion would give
q∞ < 1 and hence λ_k → 2. Scaling the full analysis beyond k = 19 needs a chunked rewrite (50 GB RSS at k = 19).

**λ_k is a mean-field quantity (2026-10-09, `meanfield.py`).** The index maps are recursive in the top digit:
nxt_k(i_low + t·N/3) = nxt_{k−1}(i_low) + σ_{i_low}(t)·N/3 and aux_k(i_low + t·N/3) = aux_{k−1}(i_low) + π_{i_low}(t)·N/9,
with σ a cyclic shift and π a shift or reflection of {0, 1, 2} fixed by the arithmetic of 2 and 3 (verified: the
recursive build reproduces `kl.structure` exactly). The alignment of σ and π is what the defect measures. The test:
replace σ, π by i.i.d. uniform random bijections and recompute λ_k and ρ_k. nxt stays a bijection and aux 3-to-1,
so the summed identity and the ceiling λ = 2 are untouched; only the fine alignment arithmetic is destroyed.

| scrambled levels | k | Δλ (model − exact) | 1 − ρ model / exact | q_k model / exact |
|---|---|---|---|---|
| top level only (8 seeds) | 9 … 12 | −3e-4 … −4e-4 (± 3e-4 … 1e-3) | +0.2 … +0.3 % | same within 0.003 |
| top level only | 13 | +1.8e-4 ± 2e-4 | −0.1 % | 0.916 / 0.920 |
| all levels 9 … k (6 seeds) | 14 | −2.1e-3 ± 4e-4 | 0.04495 / 0.04426 (+1.6 %) | 0.925 ± 0.004 / 0.919 |
| all levels 9 … k (6 seeds) | 15 | −2.1e-3 ± 5e-4 | 0.04136 / 0.04070 (+1.6 %) | 0.920 / 0.920 |
| all levels 12 … k (6 seeds) | 15 | −7.8e-4 ± 9e-5 | 0.04094 / 0.04070 (+0.6 %) | 0.923 / 0.920 |
| all levels 6 … k (6 seeds) | 13 | −8.9e-3 ± 1e-3 | 0.05119 / 0.04818 (+6 %) | 0.922 ± 0.02 / 0.920 |
| all levels 3 … k (3 seeds) | 11 | −4e-2 ± 1e-2 | +27 % | – |

Reading: (i) scrambling the top level alone costs nothing measurable from k = 9 on (at k = 13 the random
alignment is even marginally better); σ-only and π-only behave the same. (ii) Scrambling every fine level from 9
up costs −1.6e-3 (k = 11), −2.1e-3 (k = 14) and −2.1e-3 (k = 15): the cost **saturates** at about 2·10^{−3} (15 % of
one level's gain Δλ_k ≈ 0.013) instead of growing with the number of scrambled levels, so the per-level increments
Δλ_k of the random model equal the exact ones from k = 14 on; 1 − ρ is 1.6 % higher throughout and q_k agrees to
≤ 0.005 (K0 = 9) resp. 0.003 (K0 = 12, where the seed noise on 1 − ρ_15 is 3·10^{−5}).
Scrambling from level 12 up costs −7.8e-4 ± 9e-5 at k = 15 (0.6 % in 1 − ρ). (iii) The coarse levels carry real
arithmetic: scrambling from level 6 costs 10^{−2}, from level 3 several 10^{−2}, and the cost decays only slowly
with k (ratio ≈ 0.9). **So λ_k and the loss ratio q_k are mean-field quantities to ≈ 1 % in the loss and 2 % in the
per-level gain: the arithmetic of 2 and 3 enters through the coarse residues (mod 3^8, say) and the weights, and
the fine alignment can be replaced by independent uniform randomness.** Random K–L model := the exact system up
to level K0, lifted with i.i.d. uniform top-digit bijections above it. The question λ_k → 2 ⇔ q_k → q∞ < 1 can
therefore be posed in that model, which has no number theory left above K0: it is a random monotone
1-homogeneous recursion on a 3-adic tree, i.e. a quenched-versus-annealed question of the type studied for
branching random walks (Kontorovich–Lagarias's η_BP is the annealed rate). Caveats: the exact system is
*better* than random by a small offset, and no comparison theorem is known; and the residual per-level cost
is bounded (≈ 2·10^{−3} from K0 = 9) and the increments agree from k = 14 on; whether the offset itself
shrinks with k is not resolved (it would need k ≥ 16, ≈ 20 min per seed at k = 16).
**Next:** (a) a distributional (population-dynamics) formulation of the random model, which would allow k ≫ 22 at
fixed cost and decide q∞ for the model numerically; the ×4 transport makes each level a fixed-point equation for
the triple-shape law rather than a one-step map, so the formulation needs the cavity-style self-consistency;
(b) a proof of q∞ < 1 for the random model, if (a) says so.

**Population dynamics for the random model: not predictive (2026-10-09, `popdyn.py`).** Typed cavity model: pools of
sibling triples Ξ_{k+1}(w) per level-8 residue class (2187 types, 300 samples each), ×4 source an independent draw
from the pool of type nxt(τ) with a random permutation, auxiliary injection = sibling magnitudes (c_k(w_s))_s from
the level-k pool (exact sibling correlation kept) times a loss factor c̄_{k+1}/c_k, λ_{k+1} from the summed identity.
Initialised from the exact random model at k = 12, 13 (same seeds as `meanfield_all9b.json`), validated against it at
k = 14, 15. The result hinges on how the loss factor is closed:

| closure of c̄_{k+1}(w_s)/c_k(w_s) | 1 − ρ_15 (random model: 0.0414) | q at k = 16–25 | q at k = 51–60 | λ_60 |
|---|---|---|---|---|
| independent min/mean draws per sibling ("draw") | 0.0479 | 1.006 | > 1 (loss grows) | – |
| constant = pool mean ("const") | 0.0382 | 0.911 | 0.951 | 1.9917 |
| ρ(1 + ε), rel. std ε = 0.33(1 − ρ), sibling corr 0.35 (calibrated on the exact system) | 0.0397 | 0.927 | 0.955 | 1.9857 |
| ρ(1 + ε), rel. std 0.5(1 − ρ), no sibling corr | 0.0444 | 0.966 | 0.987 | 1.926 |

In the exact system the loss factor c̄_k(w)/c_{k−1}(w) has relative std 0.0136 (k = 15) and 0.0097 (k = 19), one third
of 1 − ρ_k at both levels, with sibling correlation 0.35; the triple's own min/mean fluctuates more (0.022, 0.017)
because the triple mean deviates from the parent value by 2.5 % while the min stays within 1.4 % of ρ·parent (this
is R c_k ≈ c_{k−1} again: the minimum is the stable quantity). The independent-draw closure injects this larger,
uncorrelated noise at every level and pins the loss at a floor; the constant closure removes a real source of
spread and decays too fast; the calibrated closure sits between and matches the random model to 4 % at k = 15.
**All closures with bounded noise give λ_k ↑ and q_k rising with k**, as in the exact system, and the rise is driven
by the broadening of the pool's magnitude distribution (C_max/C_min grows to 10^3–10^4): with wider magnitude
ratios more nodes are dominated by either the ×4 transport (no contraction) or the injection, which lowers the
contraction per level. But the asymptotic value of q at k = 60 ranges from 0.95 to 0.99 depending on the closure
parameter, i.e. the model cannot decide q∞ < 1 versus q∞ = 1: the closure error is of the size of the effect.
A depth-2 (sibling-of-sibling) cavity would push the same closure one level down without removing it, because the
loss-factor fluctuation is a fixed fraction of the loss at every level.

**What the exact vectors say about the mechanism (`weights.py` → `weights_stats.json`, k = 8 … 21, chunked).** The ×4
weight a_w = λ^{−2} c(nxt w)/c(w) (= 1 on class 5, so that the injection weight is b = 1 − a) has mean 0.52 at every k;
its spread within class 2 grows 0.227 → 0.264 and within class 8 0.119 → 0.137 from k = 8 to 21, with increments
that shrink geometrically (0.0049 → 0.0015, ratio 0.91, max residual 1e-4), extrapolating to 0.278 resp. 0.145. The naive variance recursion
q² = E[b²]/(1 − E[a²]) gives q = 0.81 → 0.83 (0.85 → 0.89 magnitude-weighted), far below the actual 0.91 → 0.93
(the min is not additive) but rising at the same rate, so the rising q_k is the polarisation of the weights. The
typical magnitude spread saturates too: std(log c) = 0.714 (k = 8) → 0.913 (k = 21) with increments 0.024 → 0.0092,
ratio 0.93 (limit 1.03, max residual 6e-4); the growth of C_max/C_min ∝ 1.52^k is in the extreme tail only. If the
weight distribution converges, the per-level contraction converges and q∞ < 1 follows heuristically, with the
crude extrapolations landing at q∞ ≈ 0.94–0.95 (then 1 − ρ_k → 0 geometrically and λ_k → 2). The measured q_k is
linear in k over k = 12 … 21 (slope 0.0018 per level, max residual 0.003, zero curvature) and does not yet show the
deceleration that the saturating weight spread predicts (the magnitude-weighted naive q's increments shrink with ratio
0.91, limit 0.909 against 0.891 now), so this remains a mechanism-based expectation, not a measurement.

**How to pick up.**
1. Measure convergence of the mass distribution μ_k(class) = c_m / Σc on 3-adic balls across k (total variation
   between level-j marginals of consecutive k). If it converges, a limit measure exists.
2. Compare the Perron vector of F at λ = 2 (finite k, spectral radius < 1 but the eigenvector exists) with c_k at
   λ_k. If the shapes agree, the limit object is the λ = 2 eigenmeasure of the 3-adic operator.
3. ✅ (2026-10-09) The boundary layer is the 1 − ρ_k sequence through R; the defect D_k is measured (`defect.py`).
   ✅ The recursion's mean-field character is tested directly (`meanfield.py`): random alignments reproduce λ_k, q_k.
   ✅ Population dynamics tried (`popdyn.py`): reproduces the mechanism (rising q from weight polarisation) but the
   asymptotics depend on the loss-factor closure (q_60 = 0.95 … 0.99) – not predictive. Next: a controlled
   closure (depth-2 with the measured sibling correlation) or a direct estimate of the weight-distribution limit.
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

## 8. 5x+1 as a calibration case for avenue 1

**Question.** Avenue 1 asks whether λ_k reaches the critical value 2 of the limit inequality. For 5x+1 the same
construction has a critical value strictly below 2 (integrating the limit inequality with the 5-adic branching
gives a different equation), almost all orbits are believed to diverge, and the predecessor-tree exponent is
below 1 by the standard heuristic. So 5x+1 is a case where the analogue of "λ∞ = critical value?" has a
predictable answer. [Corrected 2026-10-09, see the end of this section: the K–L ceiling for 5x+1 is exactly the
heuristic exponent 0.650919, so the predicted answer is "ρ_k → 1" here as well.]

**Why.** If the extrapolation models that disagree on 3x+1 (geometric with offset vs stretched exponential vs
power law, CLAUDE.md "Blandningskvoten") can be told apart on 5x+1, where the true limit can be computed from
the heuristic, that calibrates which model to trust on 3x+1. It also shows whether the universal boundary layer
(β(d) = 0.665, 0.401, …) is specific to 3x+1 or a general feature of "append a digit, then minimise".

**What exists.** `kl_d.py` (3x+d indexing, d coprime to 6) is the template; 5x+1 changes the class structure
(residues mod 5^k instead of 3^k, lifts over five digits) so the index formulas must be re-derived and checked
against a brute-force LP as in `lp_check.py`. Memory per k grows 5× per level, so k ≤ 13 or so on this machine.

**How to pick up.** (1) Derive the 5x+1 difference inequalities (K–L §2 with 5 in place of 3) and the limit
inequality, solve for the critical λ. (2) Independent LP (HiGHS) for k ≤ 6, then GPU iteration. (3) Fit the same
models to λ_k(5) and compare with the critical value. Days.

**Payoff.** Evidence for or against our extrapolation on 3x+1, where the question is otherwise undecidable from
data (CLAUDE.md: "More k will not settle it; theory must"). Literature (2026-10-08): no explicit K–L-type exponent
for 5x+1 exists. Kontorovich–Lagarias, "Stochastic models for the 3x+1 and 5x+1 problems", arXiv:0910.1944 (AMS 2010),
Theorem 7.6 gives π_{a,5}(x) ≥ x^{c1} with c1 unspecified and Conjecture 7.2 predicts a limit exponent η5 ≈ 0.649
(Volkov, SPA 116 (2006) ≈ 0.678, "some controversy"). An explicit certified bound would be new and could discriminate
the two heuristics.

**Results (2026-10-08, `kl5.py`, `kl5_mlx.py`, `kl5.json`).** Derivation in the docstring of `kl5.py`: principal
classes a ≡ 3 (mod 5), four doublings to return (λ^-4 c_{16a}), odd preimage b = (2a−1)/5 with weight
λ^(β−1−d) (d = 0, 1, 2, 3 doublings by a mod 25, or dropped), minimum over the 5 lifts. Checked by a generic
residue-walking LP (HiGHS) that reproduces K–L Table 2 for p = 3 to 1e-6 and matches the 5x+1 index formulas to
1e-8 (k ≤ 6); the Metal kernel matches the numpy map to 1e-7 (k ≤ 10). Note first: integrating the limit inequality
gives 1 ≤ λ^-4 + (λ^β/5)(λ^-1 + … + λ^-4), equality at λ = 2 — the same mass-conservation identity as for 3x+1,
so λ = 2 is formally critical for 5x+1 as well, while its predecessor exponent is believed to be η5 ≈ 0.65. Hence the
finite-k loss 1 − ρ_k(5) must NOT vanish if the heuristic is right: 5x+1 is a case where "λ∞ < 2" is the expected
truth.

| k | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| γ_k(5) | 0.258 | 0.298 | 0.333 | 0.381 | 0.411 | 0.433 | 0.449 | 0.464 | 0.477 | 0.489 | 0.499 | 0.508 | 0.517 |
| 1 − ρ_k(5) | 0.354 | 0.291 | 0.240 | 0.182 | 0.150 | 0.128 | 0.113 | 0.101 | 0.090 | 0.082 | 0.074 | 0.068 | 0.063 |
| ratio | – | 0.82 | 0.83 | 0.76 | 0.83 | 0.86 | 0.88 | 0.89 | 0.90 | 0.90 | 0.91 | 0.915 | 0.919 |

The summed inequality is tight at every k (λ_k is a function of ρ_k alone, as for 3x+1). What the data show so far:
γ_13(5) = 0.508 is well below 2^η5 ⇒ λ ≈ 1.57, consistent; but the successive ratios of 1 − ρ_k rise
monotonically (0.83 → 0.91), exactly the pattern seen on 3x+1 (0.91 → 0.93), i.e. the *finite-k data of 5x+1 do not
visibly show the "1 − ρ bounded away from 0" behaviour that the η5 heuristic requires*. Either the approach to the
limit is slow enough that k ≤ 13 cannot see it (geometric-with-offset fit on k ≥ 6: offset 0.047, r = 0.80, residual
1e-3 — poor), or the K–L exponent for 5x+1 eventually exceeds the η5 heuristic (which would be a surprise about
5x+1, not about the method). Either way the calibration point stands: a rising ratio of 1 − ρ_k is *not* evidence
for ρ_k → 1. k = 14 (2026-10-08, `kl5_mlx.py`, 495 s, 10 GB): γ = 0.5166, 1 − ρ = 0.0626, ratio 0.919 — still rising at ≈ 0.004 per
level, faster than 3x+1's ≈ 0.002. Next: k = 15 (N = 6.1e9, needs a split-buffer version of `kl5_mlx.py`, 48 GB);
the question is whether the 5x+1 ratio crosses 0.93 (3x+1 at k = 21) or saturates.

**CORRECTION 2026-10-09 (`boundary_layer.py`): the framing above is wrong; 5x+1 is NOT a "λ∞ < ceiling" case.**
Since cbar ≤ c pointwise, ρ ≤ 1, and the summed inequality then caps λ_k at the *smallest* root > 1 of
(1 − λ^-4) = (λ^β/5)(λ^-1 + … + λ^-4). That root is not 2: the function changes sign at λ* = 1.5701677 and again at 2,
and λ ∈ (λ*, 2) is infeasible at every k even with ρ = 1. Factoring 1 − λ^-4 = (1 − 1/λ)(1 + λ^-1 + λ^-2 + λ^-3), the
equation at ρ = 1 is exactly 1/λ + λ^(β−1)/5 = 1, the Malthusian equation of the naive backward branching walk.
Its root, γ* = log2 λ* = 0.650919, is Kontorovich–Lagarias's η_{5,BP} ≈ 0.650919 (arXiv:0910.1944, Thm 8.10), to
every digit they print. (Their "η5 ≈ 0.649" in Conj. 7.2 is the rounded value. Volkov's 0.678 is *above* the K–L
ceiling, so this method can never certify it.) For 3x+1 the same factoring gives 1/λ + λ^(α−1)/3 = 1, whose only
root is λ = 2. So in both systems:
  **λ_k → (Malthusian root of the branching model) ⇔ ρ_k → 1**,
and for 5x+1 the heuristic prediction is the ceiling itself, with 1 − ρ_k(5) → 0, just as for 3x+1. The 5x+1 data
(ratios rising 0.83 → 0.919) are therefore the *same* open question in a second system, not a calibration against a
known "no". What 5x+1 still offers: the gap to the ceiling is similar at equal k (0.134 at k = 14, against 0.128 for
3x+1), so the two sequences can be compared. Any proof of ρ_k → 1 must work for 5x+1 too, which rules out arguments
that use the contracting drift of 3x+1 (5x+1 expands). Equivalently, ρ_k → 1 says the deterministic residue system
realises the *annealed* (first-moment) growth rate of the branching walk. A true "known no" calibration would need a
map whose deterministic predecessor exponent is provably below its Malthusian root. None is known to us.

## 9. Dual certificates: λ_k is optimal at level k

**Question.** We certify feasibility of L^NT_k at λ_cert. Is λ_k also the largest feasible λ at level k? K–L
believe so (optimum with all inequalities tight). A dual (Farkas) certificate at λ slightly above λ_k would
prove it, making λ_k an exact rational-bounded number rather than a numerical one.

**What exists.** `lp_check.py` solves the LP with HiGHS for k ≤ 9 and already reports infeasibility at λ_k + 1e-4;
HiGHS can return the dual ray. For large k the dual is the Perron vector of the adjoint operator (the summed
inequality being tight suggests the dual is close to uniform), which the GPU power iteration can compute. The
rigorous check is the same kind of int64 streaming check as `certify_fast.py`, applied to the dual inequality.

**Done (2026-10-08).** No dual ray needed: for the monotone 1-homogeneous F, a positive C with F(C) < C strictly
proves infeasibility (Collatz–Wielandt upper bound; proof in RESULTS.md). `certify_fast.py --upper` rounds the
coefficients up and checks the strict reverse inequality in int64; `verify_cert.py` verifies the `-upper` format.
Brackets [λ_cert, λ_upper] of width 2e-5 … 1e-4 for k = 2 … 22, all verified (k = 22: 1.89891, slack 1.6e-6). The
power-iterated vector at λ_k + 1e-5 serves directly as the upper certificate (float32 noise permitting; k = 3 needed
+2e-4). λ_k is thus a rigorously two-sided number at every level we have.

**Payoff.** Closes the gap between "feasible at 1.8925" and "λ_21 = 1.89254…"; confirms K–L's optimality belief
numerically at every k we have. Modest, but it makes the table in `RESULTS.md` two-sided.

## 10. Explicit constants in the predecessor bound

**Question.** Theorem 2.2 gives φ^m_k(y) ≥ Δ1 c_m λ^y with Δ1 = 1/(4 max c_m), so the certified bound is fully
explicit, not only eventual. What does it say numerically, and how far is it from reality?

**What exists.** Every certificate has C_max/C_min (6457 at k = 21), so Δ1 is known. Barina's verification and
Roosendaal's tables give actual counts of n ≤ 2^y reaching 1.

**How to pick up.** Tabulate the explicit lower bound for π_1(x) at x = 2^40 … 2^70 from each certificate,
compare with actual counts, and note at which x the bound first exceeds trivial bounds. Half a day. Check the
exact statement of Theorem 2.2 (the range of y for which the inequality holds) before claiming anything.

**Payoff.** A concrete, checkable statement for `RESULTS.md`; shows how the growth of C_max/C_min with k eats
into the constant while the exponent improves.

## 11. 3x+d cycle census at scale

**Question.** Lagarias, "The set of rational cycles for the 3x+1 problem", Acta Arith. 56 (1990) 33–53, relates
primitive cycles of 3x+d to rational cycles and conjectures every d ≡ ±1 (mod 6) has one. Belaga–Mignotte,
Experimental Math. 7 (1998) 145–151, bound the number of cycles with ≤ k odd elements by d·k^c; their Strasbourg
preprint 2000-18 (hal-00129656, 57 pp.) lists primitive cycles for all 6667 values 1 ≤ d ≤ 19 999, with a 400-page
table (hal-00129727, 2006). The only independent recount is Morley 2013 (OEIS A226607, A226613, A226662, A226663,
A226670): 42 757 primitive cycles for d < 20 000 (Belaga–Mignotte's 42 765 is 8 too high), partial sweep to
d < 158 195. Nothing beyond d < 20 000 since 2013. A GPU census to d ~ 10^6 with minimal elements up to ~10^9 is a
new dataset; Cox, JIS 15 (2012) 12.5.2 (Poisson model for cycle counts) is the conjecture to test.

**What exists.** `cycles_d.py` (brute force, d ≤ 29, minima ≤ 3·10^5) and the generalised Eliahou inequality it
checks. The 3x+13 example (seven 8-cycles with one (n, k)) shows what structure to count.

**How to pick up.** Port the cycle search to the GPU (each d independent, minima enumerated by residue class),
store (d, n, k, min, max) per cycle, then study #cycles(d), the distribution of (n, k), and whether the
Eliahou bounds are attained. Days to a week.

**Payoff.** Publishable data; a direct test of old conjectures; a test bed for avenue 4 (any cycle method must
reproduce this list).

## 12. Terras's coefficient stopping time conjecture (1976)

**Question.** Terras, Acta Arith. 30 (1976) 241–252, conjectured that the coefficient stopping time κ(n) equals
the stopping time σ(n) for every n ≥ 2 (implies no nontrivial cycles) and proved it for κ(n) ≤ 2593; Garner, Proc.
AMS 82 (1981) 19–22, for κ(n) < 105 000. **Status (lit. search 2026-10-08): largely pre-empted.** Rozier–Terracol,
"Paradoxical behavior in Collatz sequences", Discrete Math. 349 (2026) 115167 (arXiv:2502.00948), find exactly 593
paradoxical sequences with start ≤ 4614 (exhaustive to 10^9) and prove t(n) = τ(n) for all 2 ≤ n ≤ 2.8·10^19
(Corollary 5.4) from the Oliveira e Silva / Roosendaal record tables. A new computation must start beyond that,
with Barina's 2^71 as the natural input; the gain is ~2 orders of magnitude, not 14.

**Why now.** A Barina-style sieve adapted to this statement could push the verified range from 2.8·10^19 towards
2^71 on one GPU, since it is a per-n check with early exit.

**How to pick up.** (1) Literature check: last verified bound, and whether any later work subsumes it.
(2) Formulate the per-n test; (3) GPU sieve over residue classes mod 2^j with Barina's pruning. Days.

**Payoff.** No new theorem about Collatz, but a forgotten statement with an obvious compute upgrade; the kind of
result that gets cited in surveys.

## 13. m-cycle bounds with the 2^71 verified range

**Question.** Simons–de Weger, Acta Arith. 117 (2005) 51–70, exclude m-cycles (m = number of local minima) for
m ≤ 68 (X0 ≈ 3.4·10^17); their web version v1.44 (2010) reaches m ≤ 75 with X0 = 5·2^60. Hercher, JIS 26 (2023)
23.3.5 (arXiv:2201.00406), proves m ≥ 92 with **X0 = 695·2^60 ≈ 2^69.4** (not 2^68); 3·2^69 is only the hypothesis
of his Corollary 29 (K > 1.375·10^11), which Barina's 2^71 (J. Supercomput. 81:810, 2025; milestone 2025-01-15)
makes unconditional: K ≥ 137 528 045 312, T-period ≥ 217 976 794 617. A corrigendum (14 June 2026) repairs
Theorem 21; the result stands. Nobody has published a re-run of Hercher's iteration with X0 = 2^71; the only claim
(m ≥ 102) is an unrefereed GitHub Lean repository (justinalick, 2026) assuming 2^71 and Rhin's bound. The
transcendence input is still Rhin 1987; Gouillon 2006 is unapplied and would move m only logarithmically.
Barina's project page shows 2075·2^60 ≈ 2^71.02 verified (2026-10-08), no 2^72 announcement; Angeltveit
(arXiv:2602.10466, Feb 2026) proposes a faster algorithm but reports no run.

**What exists.** Hercher's paper (scratchpad, needs re-downloading), `cycles.py` for the admissible (n, k) pairs,
`cycle_harmonic.py` / `cycle_lp.py` for our own refinements. The method is continued fractions plus bounded
enumeration, modest compute.

**How to pick up.** Re-run Simons–de Weger / Hercher with X0 = 2^71; check whether anyone has already done so
since January 2025. Days.

**Payoff.** A clean, publishable increment if it is still open.

**Done 2026-10-10 (`mcycles.py`, `notes/mcycles_2_71.md`; reproduced by the main session).**

The method was re-implemented from [H] and [SdW]: the K1/J2/K2 upper bounds, the generalised Crandall lemma, the
lattice enumeration and Hercher's Theorem 16/23 bootstrap. `mcycles.py validate` (60 s) reproduces:
- Hercher's Theorem 23 sequence and Table 1 exactly;
- SdW's tables and both of their results (m ≤ 68 at 301·2^50, m ≤ 75 at 5·2^60).

It also found two misprints:
- Hercher Table 1 prints 4.68e18 for 4.64e18;
- SdW v1.44 lists 12 candidates at m = 80, where there are 13.

Neither changes a result.

**Result at X0 = 2^71 (and at 2075·2^60): exactly m ≤ 91, no gain.**
- For m = 92 the bootstrap stalls at K ≥ 2.0563·10^20 < K2(92) = 3.42·10^20. A genuine shape satisfies Hercher's
  inequality there, and the lattice enumeration finds surviving shapes for every m = 92 … 101.
- Excluding m = 92 by this method needs X0 ≥ 14948·2^60 ≈ 2^73.87; m ≤ 101 needs ≈ 2^76.07; m = 102 needs
  ≈ 2^81.05.
- By-product: improved K lower bounds at 2^71 (K ≥ 2.06·10^20 for 92 ≤ m ≤ 100).

The unrefereed Lean repository claiming m ≥ 102 (justinalick, Sept 2026) assumes 2^71. It does not re-run Hercher:
it excludes the surviving shapes with a new "two-rise"/"chain" argument. Its listed shapes agree with our survivors,
but the new argument is unverified.

So avenue 13 is closed as a pure re-run. The open item is that new argument (verify it, or find a counterexample
shape), or verification to about 2^74 (Barina's campaign).

**The m ≥ 102 repository audited (2026-10-10, `notes/mcycles_102_audit.md`; build in `~/devel/mazur_dl/m102/`).**

Checks:
- Plain declarative lakefile; no IO, meta code, `sorry`, `axiom` or `native_decide`; 431 `decide +kernel` calls.
- Built from source (Lean v4.35.0-rc3, Mathlib at its tag). `#print axioms` shows the three standard axioms.
- `leanchecker` passes on all 49 modules.
- The independent Rust kernel **nanoda** accepts the whole exported closure (30 298 declarations).
- An independent restatement with our own definitions (T map, minimal period, local minima, raw Rhin form)
  is derived in Lean (`AuditM102.no_small_m_cycle`; I re-ran it).

**So: every nontrivial T-cycle has ≥ 102 local minima, conditional on**
- (i) every n ≤ 2^71 reaches 1 (Barina 2025);
- (ii) Rhin's bound in the form of Simons–de Weger Lemma 12. Rhin's paper itself could not be obtained, so any
  height threshold in it is unchecked.

The new ingredients:
- **Two-rise bound.** For odd n < 2^N, the first two ascents total ≤ B. It was recomputed independently by a 2-adic
  search and is sharp, e.g. B = 84 for N = 72–77, attained by n = 3 603 960 565 806 965 719 039.
- **Chain argument.** All 120 shape certificates were recomputed in exact arithmetic and pass. The worst case
  reaches 0.798 of what a cycle needs (m = 101). Without the two-rise bound, 111 of them would survive.
- The repository's shapes are a superset of our `mcycles.py survivors`.

Caveats: unrefereed, AI-produced, and no human-readable proof. Extending past 101 needs a larger two-rise grid
(about 2.6× kernel time per m).

Correction to `notes/mcycles_2_71.md` §6: log δ = 0.4605607, so SdW's constant 0.46057 is safely rounded.

**Extended to m ≤ 103 (2026-10-10, `notes/mcycles_extension.md`; build in `~/devel/mazur_dl/m102/extend/`).**
- New two-rise grid points: N = 32 955 and 36 150 for m = 102; 52 248 and 57 314 for m = 103. B = N + 30, kernel
  checked.
- Chain certificates for 62 (m = 102) and 103 (m = 103) shapes, from our own generator. The generator reproduces the
  repository's m = 92 and m = 101 data exactly.
- `Collatz.no_103_cycle_2_71` holds, with standard axioms only; leanchecker passes per module on the post-fix Lean
  v4.35.0-rc3.
- An independent restatement `AuditExt.no_small_m_cycle` (re-run by the main session) states: given every
  n ≤ 2^71 reaches 1 and Rhin's bound, **every nontrivial cycle has ≥ 104 local minima**.
- nanoda passed the m ≤ 102 closure (30 290 declarations) and, re-run by the main session with more memory, the
  **m ≤ 103 closure: 30 446 declarations, no errors** (20 min, 31 GB peak).
- The repository is Apache-2.0, and this extension is attributed in the note.
- **m = 104 certified too (05:45–06:30).** Grid points N = 87 660 and 90 960, plus 153 shapes (worst ratio 0.7988).
  The data module took 842 s with a 27.7 GB peak; the kernel needed `maxHeartbeats 0`, a resource limit only.
  `Collatz.no_104_cycle_2_71` and the restatement `AuditExt104` state **≥ 105 local minima**, with standard axioms
  and per-module leanchecker.
  - nanoda for m ≤ 104 is still to do (it needs about 45 GB).
  - m = 105 would need grid points near N ≈ 139 000/144 000 and a data check of about 40–45 GB.
- A useful finding for the original author: their checker's pattern width E1 = 16 makes some grid points about
  100× slower; E1 = 32 fixes it.

## 14. Matrix interpretations for the rewriting system

**Question.** Yolcu, Aaronson, Heule, "An automated approach to the Collatz conjecture", CADE-28, LNCS 12699 (2021);
J. Automated Reasoning 67, art. 15 (2023); arXiv:2105.14697. An 11-rule string rewriting system T is terminating iff
Collatz holds (Theorem 3.17). They prove termination automatically (natural/arctic/tropical matrix interpretations,
CaDiCaL) for all 11 single-rule-deleted subsystems, all residue classes mod 4 and classes 2, 3, 4, 6 mod 8; the
classes 1, 5, 7 mod 8 carry $500 prizes each and remain open; Zantema's unary system admits no natural-matrix proof
even with dependency pairs. Code: github.com/emreyolcu/rewriting-collatz. No termination-tool follow-up exists
(2026-10-08). Could larger SAT or LP searches, or interpretations of a different shape (higher dimension, different
semirings), settle one of the three open residue classes?

**Why.** It is the only route on this list where success is a proof rather than a bound, and the only
reformulation where our GPU/LP competence transfers directly (CLAUDE.md "Omvärld").

**How to pick up.** Reproduce their weakened-variant results from their repository, then scale the search
(dimension, coefficient range, solver time) and record where it fails. The expected outcome is a negative
result with a map of what was tried. Weeks.

**Payoff.** Very low odds; a negative result is still informative about where the obstruction sits.

## 15. Applegate–Lagarias extremal trees to depth 45–50

**Question.** Applegate–Lagarias, Math. Comp. 64 (1995) 411–426, Conjectures C and C′ (see avenue 1 for the exact
statements; Conjecture A is positive density): the extremal pruned-tree leaf counts N^±(k) are (4/3)^{k(1+o(1))},
and C′ asks for a bounded ratio N^+/N^−, which is false for the random branching models. Theorem 1.1 gives
(1.302053)^k ≤ n_k(a) ≤ (1.358386)^k; extremal counts were computed for all k ≤ 30 and never extended. Exact
extremal statistics to depth 45–50 are feasible now and bear directly on whether λ_k → 2.

**What exists.** `tree_growth.py` (exact BFS per residue class, k = 9, trees ≤ 9 M nodes) and the observation
that every class grows with exponent ≈ 1 at that depth. A 2026 repository (neljaouh/ConjectureA) claims Lean
proofs of Conjecture A, unverified.

**How to pick up.** Extend the BFS to a GPU DFS over the pruned tree (nodes ≈ (4/3)^k, so depth 50 is ~10^6
nodes per root but all roots must be covered via residue classes mod 3^{k+1}), compute N^±(k) per depth, and
test C′ (bounded ratio) against the branching-model prediction. Days.

**Payoff.** Direct evidence on Conjectures C / C′; if the extremal ratio stays bounded, λ_k → 2 is the expected
consequence and avenue 1 gains support from a second direction.

**Done 2026-10-10 (background agent; `extremal_trees.py`, `extremal_trees_core.c`, `notes/extremal_trees.md`).**

*Extremal counts.* A depth-first branch and bound over the 3-adic digits of a (chain decomposition, lazy subtree
bounds from exhaustive tables at depth 18–19) gives exact N^−(k) to k = 59 and N^+(k) to k = 55.
- Validated: it reproduces A–L's printed g^±(30) and γ*_30, brute force for k ≤ 13, unpruned enumeration for k ≤ 36
  (Σ N*_k = 2·4^k), and witness residues.
- From k = 25 on, (4/3)^k/N^−(k) ∈ [2.033, 2.048] and N^+(k)/(4/3)^k ∈ [1.738, 1.748]. That is strong evidence for
  Conjecture C′ (bounded ratio), which the random branching models violate.
- A–L Theorem 1.1 improves from (1.302053)^k ≤ n_k(a) ≤ (1.358386)^k to **(1.317329)^k … (1.346858)^k**.

*Residue-class certificates (the stronger result).* Track the class mod 3^r of every node. Let φ_n(c) be the
minimum of N*_n over b ≡ c. Then φ_{n+1} ≥ Φ(φ_n), with Φ(v)(c) = v(2c) + [c ≡ 2, 8 (9)]·min over lifts of
v((2c−1)/3). This is the K–L method for depth counts, and it has no λ-dependent weights. A positive V with
Φ(V) ≥ μV gives N*_n(a) ≥ (V_min/V_max) μ^n for **every** a and n; the upper bound uses max. Results:
- Certified in exact integer arithmetic for r ≤ 19 (774 M classes): **0.2822·(1.3333119)^k ≤ N*_k(a) ≤
  3.556·(1.3333567)^k**. Since n_k(a) ≥ N*_k(a) and n_k(a) ≤ (k+1) N*_k(a) [A–L §2], the uniform growth constant of
  n_k(a) lies in [1.3333119, 1.3333567], within 3·10^{−5} of 4/3. A–L's Conjecture B asserts exactly 4/3.
- My independent re-implementation reproduces r = 13 (μ ≥ 1.333075, μ′ ≤ 1.333637) and r = 16 (μ ≥ 1.333259,
  μ′ ≤ 1.333416, 28.7 M classes), all certified in exact integer arithmetic.
- The losses 4 − 3μ_r and 3μ′_r − 4 decay geometrically, with ratio ≈ 0.65 per digit. The K–L analogue 1 − ρ_k
  decays only at 0.93 per digit.
- The certificate spread V_max/V_min stays ≈ 3.5 at every r. If both persist, μ_r, μ′_r → 4/3 (Conjecture B,
  uniformly) and the ratio stays bounded (Conjecture C′).

**Formalised (2026-10-10, `lean_formal/PreimageBound/`).** `PreimageBound.preimage_count_lower_bound`:
for every a ≢ 0 (mod 3) and every k, 0.2847·(1.3331664)^k ≤ #{n ∈ [1, 2^k a] : T^k(n) = a}. The r = 14 certificate is
checked by the kernel itself (`decide +kernel`); standard axioms only, leanchecker passes, and nanoda passes.

Literature check (2026-10-10, main session): the best published rigorous constants found are still A–L's
1.302053/1.358386. One caveat: the unrefereed neljaouh/ConjectureA repository claims the growth-exponent conjecture
for each fixed a from Mazur's M2. Our bounds differ in kind: explicit, uniform in a, valid for every k.

**Next:** see avenue 28.

## 16. Spectrum, spectral gap and traces of the K–L transfer matrix

**Question.** The LP only uses the leading eigenvalue of the weighted backward transfer matrix M_λ on residues mod
3^k (at the Perron vector the minimum in each row is attained by a fixed lift, so F is linear there; `jacobian.py`
builds that sparse matrix). What do the rest of the spectrum and the traces say?

**What exists.** `jacobian.py`, k ≤ 11: second eigenvalue modulus 0.754, 0.838, 0.824, 0.857, 0.865, 0.861, 0.865
(k = 5 … 11), complex, on top of a dense cluster; it matches the per-digit sensitivity decay (0.83 → 0.875 for
k = 12 … 19) and is rising with k. The power iteration at k = 22 needed several hundred iterations from a warm
start (effective contraction ≈ 0.97), so the gap keeps closing. Literature: nothing on this matrix; the nearest
objects are Tao's equidistribution of Syracuse orbits mod 3^n (a forward transfer-operator spectral bound via
characters), Kontorovich–Sinai's 3-adic mixing (2002), and Berg–Meinardus's eigenfunction formulation (1994).

**Why.** (i) The spectral gap 1 − |λ₂|(k) is the quantitative form of "how fast does top-digit sensitivity decay",
i.e. avenue 1's open item (ii); its scaling in k (does it close like a power of k, or geometrically, or to a
positive limit?) is a cleaner observable than ρ_k. If the limit operator on Z₃ has continuous spectrum, the gap
→ 0 and the rate says how. (ii) Traces tr(M^j) are weighted sums over closed walks of length j in the residue
graph; an integer cycle of length j is a closed walk mod 3^k for every k with a specific weight, so the small-j
traces as functions of k are a cycle statistic that joins the density track to the cycle track (Artin–Mazur zeta
function 1/det(1 − zM)). (iii) The bulk of the spectrum shows whether M behaves like a random sparse nonnegative
matrix (eigenvalues filling a disc) or has arithmetic structure; outliers above the bulk and their k-scaling are
the "modes" of the renormalisation picture (avenue 1).

**Dynamics reading.** M_λ^j e_a is the weighted count of predecessors j (double-)steps below a; M^j → r^j v wᵀ with
corrections decaying like (|λ₂|/r)^j, which is why counts become c_m λ^y with a transient that sets the constant
x0 but not the exponent. Σ_j M_λ^j converges iff r(M_λ) < 1, so λ_k is the zero of the pressure function
P(λ) = log r(M_λ) — Bowen's equation for the growth exponent of the weighted tree. The forward map on single
integers has no interesting spectrum (M e_n = e_{T n}, a path); all information is in the aggregated backward
operator.

**Infinite-operator reading (2026-10-08).** Functions on Z/3^k are the locally constant functions of level k on
Z₃, an invariant subspace of the (linearised, min-free) backward operator, so the finite matrices are exact
restrictions: eigenvalues that stabilise in k are eigenvalues of the infinite operator, those that keep moving are
the finite-k shadow of its essential spectrum. Ruelle quasi-compactness needs backward contraction; here the odd
branch m ↦ (2m−1)/3 expands (mixes) but the doubling branch m ↦ 4m is an isometry of Z₃ (mixes nothing) with weight
1/4 at λ = 2, so on Hölder-α functions the essential radius should be ≈ 1/4 + (3/4)·3^(−α) → 1 as α → 0; with the
measured Hölder exponents 0.04–0.09 of the limit vector the gap is essentially zero — the spectral form of "the ×4
term recirculates top-digit information without loss" (§1). Isolated outer eigenvalues could also be obtained from
the dynamical determinant det(1 − zM) via the traces (Jenkinson–Pollicott style), if any exist outside the bulk.

**Results (2026-10-08 evening, `spectrum.py`, `spectrum.json`; dense spectra k ≤ 9, ARPACK top-40 for k = 10 … 15,
at λ = λ_k and λ = 2).**

| k | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| \|λ₂\| at λ_k | 0.754 | 0.838 | 0.824 | 0.857 | 0.865 | 0.861 | 0.865 | 0.861 | 0.865 | 0.867 | 0.865 |
| # eigenvalues within 1 % of \|λ₂\| (of top 40) | 4 | 1 | 2 | 4 | 4 | 6 | 6 | 20 | 27 | 25 | 39 |
| \|λ₂\|/λ₁ at λ = 2 | 0.903 | 0.849 | 0.835 | 0.884 | 0.884 | 0.887 | 0.880 | 0.892 | 0.880 | 0.874 | 0.876 |
| top-digit energy of v₂ (λ_k) | 0.64 | 0.82 | 0.69 | 0.65 | 0.71 | 0.67 | 0.72 | 0.62 | 0.57 | 0.71 | 0.67 |
| top-digit energy of Perron vector | 0.017 | 0.014 | 0.011 | 0.010 | 0.008 | 0.007 | 0.006 | 0.006 | 0.005 | 0.004 | 0.004 |

1. **The spectral gap of the linearisation does not close.** \|λ₂\| at λ_k is flat at 0.86–0.87 from k = 8 to 14
   (and 0.87–0.89 relative to λ₁ at λ = 2). What changes with k is the *density* at that radius: the number of
   eigenvalues within 1 % of \|λ₂\| grows from 4 (k = 9) to 25–27 (k = 13, 14), i.e. a ring at radius ≈ 0.865 is
   filling in — the finite-k shadow of the essential spectrum's edge, exactly the "discrete levels merging into a
   band" picture, but with the band edge fixed, not drifting towards 1.
2. **The slow modes are delocalised, not top-digit modes.** The digit-energy profile of v₂ at k = 14 is 0.667 at every
   digit position (a vector with no digit structure has exactly 1 − 1/3 = 0.667) and 0.71 at the top digit; the
   Perron vector's profile decays geometrically from 0.38 to 0.004. λ₂ is complex with an argument that jumps
   between levels (rotational modes). So the second eigenvector is "white noise" across the 3-adic digits with a mild
   top-digit excess — not the top-digit perturbation that §1 imagined relaxing at rate \|λ₂\|.
3. **Consequence for avenue 1.** The per-digit sensitivity factor of the Perron vector (0.83 → 0.875 for k = 12 … 19)
   is numerically close to \|λ₂\| ≈ 0.865 but *drifts* while \|λ₂\| does not; and the power iteration's slowdown
   (effective contraction ≈ 0.97 at k = 22, vs 0.865 here) cannot come from the linear spectrum. Both must come from
   the nonlinearity (argmin switching of the min over lifts as the iterate moves) and/or non-normal transients. This
   favours the renormalisation / alignment-efficiency mechanism of §1 (the fraction e_k of ×4-term variation that
   survives the min) over a linear mixing-rate explanation: the question λ_k → 2 is a question about the min, not
   about the spectrum of the linearisation at the fixed point.
4. **Bulk.** For k ≤ 9 the radii containing 50 / 90 / 99 % of the eigenvalues are ≈ 0.37–0.41 / 0.64–0.71 / 0.80,
   slowly shrinking in k, while the 40th eigenvalue rises (0.41 → 0.82): the spectrum is a filled disc of radius
   ≈ 0.8 with a thin outer ring at 0.865 and the isolated Perron root at 1.
5. **Traces.** tr(J) = 0 at every k (the trivial cycle's self-loop at residue 2 is never the argmin lift, so the min
   masks it); the unweighted closed-walk counts (tr B^j = 0, 2, 3, 10, … at k = 5) are dominated by accidental
   congruences that disappear at larger k (tr B² = 2 for k ≤ 8, 0 at k = 9), and the weighted traces stay O(1)
   (Σ λ_i^j → 1). No usable cycle statistic at these k; an integer cycle would have to show as a closed walk present
   at *every* k with the right weight, and the only one there is (the trivial cycle) is removed by the min. Dropped
   as a cycle tool unless done on the min-free operator G_k.

Full run k = 5 … 15: 26 min on the CPU (k = 15 Perron vectors dominate).

**How to pick up.** (1) Dense spectrum for k ≤ 9 (N ≤ 6561), ARPACK top-50 eigenvalues for k ≤ 15 (sparse, ≤ 2
entries per row), at λ = λ_k and at λ = 2; plot |λ_i| vs k, fit the gap. (2) tr(M^j) for j ≤ 300 by sparse
products at k ≤ 19 (vectors in RAM); compare with the closed-walk count of the unweighted residue graph; look for
the footprint of the trivial cycle and test whether the weights distinguish "integer-realisable" closed walks.
(3) Relate the second eigenvector to the digit profile of `holder.py`. Hours, CPU only.

**Payoff.** A spectral-gap scaling law in k would be the most concrete input to a proof of λ_k → 2 we could offer;
the trace statistic is a new (if long-shot) bridge to cycles.

## Towards a full proof (avenues 17–21, added 2026-10-09)

Everything above is a density or a cycle statement. The five avenues below aim at the conjecture itself. Whether
an avenue fits the current machinery is not a criterion: if a new machine is needed, it gets built. Each entry says
what would be proved, why it is well posed, and the first concrete step. None is likely to succeed; each is a
mathematical target rather than a wish.

## 17. Three-statement decomposition: Conjecture A + density-1 boundedness + no cycles ⇒ Collatz

**Claim.** Collatz follows from (A) every a ≢ 0 (mod 3) has a predecessor set of positive lower natural density
(Applegate–Lagarias Conjecture A, Wirsching's program, avenue 6), (B) the set of integers with bounded orbit has
natural density 1, and (C) there is no nontrivial cycle. Proof: if n diverged, its predecessor set would consist of
divergent numbers and have positive lower density by (A), contradicting (B); cycles are excluded by (C). None of the
three says "for every n": (A) and (B) are density statements, (C) is Diophantine.

**Where each stands.** (A): our K–L program gives x^γ with γ → 1 at best, and we now know exactly why it cannot
give positive density: the limit object is unbounded (C_max/C_min ∝ 1.52^k, avenue 1), so the constant
Δ₁ = 1/(4 max c) in Theorem 2.2 vanishes even for an exact solution at λ = 2. A proof of (A) needs an inequality
system whose limit solution stays bounded. (B) is one step beyond Tao (arXiv:1909.03562): from "attains almost
bounded values" in logarithmic density to "bounded" in natural density; Tao's own remarks explain why his method
stops short. (C) is avenue 19.

**First steps.** (A): design a weighted K–L system (classes weighted by 3-adic depth, or a system with the ×4
chain summed out) and test at k ≤ 12 whether its solution has bounded spread while keeping λ_k → 2; the mean-field
structure found in avenue 1 says which quantities such a system must control (the ×4 weight distribution). (B):
read Tao's proof for the exact point where logarithmic density enters (the Syracuse random variables' approximate
invariance) and list what a natural-density version would need. Months for either; (A) is where our tools apply.

**Payoff.** A full proof from three statements each of which is the kind of thing analytic number theory proves.

**First step done (2026-10-09): bounded spread at fixed λ, and what it buys.** K–L's own linear program L^NT_k(λ) is
"minimise C_max subject to 1 ≤ c ≤ C_max and feasibility" (their (2.7)–(2.14)), so their Table 2 column C_k^max is the
*minimal* spread at λ_k, and they note it grows exponentially in k. Theorem 2.2 then gives, for every feasible point,
φ_k^m(y) ≥ c^m λ^y/(4 max c) for **all y ≥ 0** (Δ = λ^{−ν} min φ(0)/max c with ν ≤ 2, φ(0) ≥ 1; no threshold), and
φ_k^m(y) is by definition the infimum of π*_a(2^y a) over a ≡ m (mod 3^k) not in a cycle. Hence a feasible point with
1 ≤ c ≤ t at level k and parameter λ proves, with no x₀ at all,

  π_a(x) ≥ (x/a)^{log₂ λ} / (4t)   for every x ≥ a and every a ≢ 0 (mod 3) not in a cycle.

What K–L did not look at is the spread at *fixed* λ < 2 as k grows. Measured (`spread_lp.py` with HiGHS, k ≤ 9;
`spread_iter.py`, the greatest fixed point of c ↦ min(t, F(c)) with bisection on t, identical to the LP to 4 decimals
and instant to k = 16): t*(k, λ) is nonincreasing in k (lifting) and **converges**:

| k \ λ | 1.60 | 1.65 | 1.70 | 1.75 | 1.78 | 1.80 |
|---|---|---|---|---|---|---|
| 7 | 4.448 | – | 8.529 | – | – | – |
| 9 | 4.448 | – | 7.752 | – | – | – |
| 11 | 4.448 | 5.551 | 7.613 | 11.707 | 18.193 | – |
| 12 | 4.448 | 5.545 | 7.600 | 11.344 | 16.308 | 27.172 |
| 13 | 4.448 | 5.543 | 7.580 | 11.157 | 15.416 | 20.883 |
| 14 | 4.448 | 5.542 | 7.571 | 11.017 | 15.000 | 19.347 |
| 15 | 4.448 | 5.539 | 7.560 | 10.912 | 14.708 | 18.629 (1.82: 26.09) |
| 16 | 4.448 | 5.539 | 7.556 | 10.850 | 14.547 | 18.164 (1.82: 24.01) |
| Perron C_max | – | – | – | – | – | 147 (k = 12) … 1594 (k = 16) |

At λ = 1.60 the level-5 solution is already optimal (t* = 4.4475 for all k ≥ 5). Extrapolating the decrements
geometrically (k ≤ 16): t*_∞ ≈ 4.45, 5.54, 7.55, 10.7, 14.3, 17.6 for λ = 1.60 … 1.80, which fits
t*_∞ ≈ C (2 − λ)^{−a} with a = 2.0–2.1 (max residual 0.02–0.03 in log t*; local exponents 1.64, 2.01, 1.93, 2.24,
2.19, drifting slightly upward), while an exponential in λ fits worse (0.085). Points within 0.01 of λ_k converge
too slowly in k to be useful (the k = 15, λ = 1.84 iteration was stopped).

**Consequences.** (i) *Explicit bounds, certified.* `spread_iter.py --slack=1e-5` produces a feasible point with
relative slack 10^{−5} in every row, `certify_spread.py` checks it in int64 with rounded-down coefficients and writes
`certs/spread_k{k}_{λ}/` (format /2), verified by the independent `verify_cert.py`:
k = 9, λ = 1.70, t = 7.753: π_a(x) ≥ (x/a)^{0.7655}/31.01; k = 14, λ = 1.78, t = 15.003: (x/a)^{0.8319}/60.01;
**k = 14, λ = 1.80, t = 19.353: π_a(x) ≥ (x/a)^{0.8480}/77.41 for all x ≥ a** — the first K–L bounds with explicit
constants and no x₀ (avenue 10 done as a by-product). The certified Perron vector at k = 22 gives
(x/a)^{0.9251}/39404, which overtakes the k = 14 bound only for x/a > 10^{35}.
(ii) *Conjecture A reduces, up to log powers, to the growth of t*_∞(λ) as λ → 2.* With λ = λ(x) → 2 chosen to balance
x^{−(2−λ)/(2 ln 2)} against 1/t*_∞(λ): if t*_∞(λ) ≤ C(2 − λ)^{−a} then π_a(x) ≥ c_a x/(log x)^a; if t*_∞ stays bounded,
positive density. The current fit (a ≈ 2) would give π_a(x) ≫ x/(log x)². This also needs λ_k → 2 (avenue 1), since
t*_∞(λ) = ∞ for λ > lim λ_k. The extrapolation λ → 2 is a limit-object statement and must be proved, not fitted; but
every finite λ gives a rigorous certified bound today.

**Structure of the minimal-spread solutions (2026-10-09, `spread_structure.py`, k = 14, λ = 1.78 and 1.80).** They are
*coarse*: the lowest four ternary digits explain 95 % of the variance of log c, the lowest eight 99.5 %, the top
digits 0 %; the top-digit loss profile 1 − ρ_j falls geometrically from 0.62 to 0.008 (Perron vector: 0.68 to 0.044).
No class sits at the floor 1; 4–6 % sit at the cap t, almost all in class 8 mod 9 (11–16 % of that class) and none in
class 5 (whose values are small, mean 2.3–2.5, since c_m = λ^{−2} c_{4m} there); 94–96 % of the rows are tight, the
slack rows being the capped ones. The solution is the Perron-like fixed point with its upper tail cut off, and the two
λ's correlate at 0.996 in log c (0.95–0.97 with the Perron vector). So the bounded limit object is close to a locally
constant function on ℤ₃ and needs no re-weighting to be nice; the "weighted system" idea is dropped for that reason.

**Next (spread).** k = 16 at λ = 1.85; the exponent a of t*_∞ ≈ (2 − λ)^{−a} from the λ ≥ 1.80 points; the theory of
the capped fixed point as λ → 2 on ℤ₃.
**Lifting the base case (2026-10-09, `base_lift.py`): the spread penalty is not intrinsic.** K–L's constant
Δ = λ^{−ν} min φ(0)/max c (Thm 5.1, (5.2)) comes from starting the induction at y = 0, where every class has count 1,
so the capped classes (c = t) cost the factor 1/t. The induction (their proof of Thm 5.1) works from any base
window [Y − ν, Y] with Δ_Y := min over m and y ∈ [Y − 2, Y] of φ_k^m(y)/(c^m λ^y), and for y up to about k the counts
φ_k^m(y) = inf_a π*_a(2^y a) are bounded below by the **guaranteed tree** of the class: predecessors 2n (always) and
(2n − 1)/3 iff n ≡ 2 (mod 3), decidable while the residue is known mod 3^{k−j} after j odd steps; values bounded by
a 2^e (2/3)^j so the path-maximum condition is implied. Exact enumeration (DFS per class, seconds to k = 9); checked
against brute-force pruned trees of random integers in the class, 225 cases, always ≤ and tight (ratio 1.000) for
some a, as the infimum must be.

| k, solution | max c = t | K–L Δ₁ = 1/(4t) | best Y | Δ_Y | gain | corr(log counts at Y, log c) |
|---|---|---|---|---|---|---|
| 6, Perron λ₆ | 12.9 | 0.019 | 5 | 0.83 | 43× | 0.98 |
| 7, Perron λ₇ | 20.2 | 0.012 | 5 | 0.68 | 55× | 0.98 |
| 8, Perron λ₈ | 29.1 | 0.0086 | 5 | 0.54 | 63× | 0.98 |
| 9, Perron λ₉ | 43.3 | 0.0058 | 5–6 | 0.38 | 67× | 0.98 |
| 8, bounded λ = 1.70 | 7.9 | 0.032 | 6 | 1.36 | 43× | 0.98 |
| 8, bounded λ = 1.74 (certified) | 14.3 | 0.018 | 6 | 0.865 | 49× | 0.985 |

The guaranteed counts correlate with c at 0.98 in log at every level: the LP vector *is* the tree-density profile
(confirmed independently by the empirical predecessor densities, `pred_density.py`/`pred_compare.py`: class means of
d_a·a correlate with the Perron vector at 0.90–0.93 already at X = 2^20). The argmin for Y ≥ 6 is always the
largest-c class, because the guaranteed tree (≤ k odd steps) undercounts most for the densest classes; this is why
Δ_Y peaks at Y ≈ 5–6 and why Δ_best still decays slowly with k for the Perron vectors (0.83 → 0.38, ≈ 0.8 per
level, i.e. like t^{−1/2} instead of t^{−1}). **Certified explicit bound:** with the int64-verified vector
`certs/spread_k8_1.74/` and the exact counts, for every a ≢ 0 (mod 3) not in a cycle,

  π_a(x) ≥ 0.865 · (x/a)^{0.7991}   for all x ≥ 2^6 a,

which beats (x/a)^{0.848}/77.4 (k = 14) up to x/a ≈ 10^{37} and the k = 22 Perron bound up to x/a ≈ 10^{40}.
**CORRECTED and IMPROVED 2026-10-10 (`base_lift_chunked.py`).** The 0.865 was the minimum at 0.25-grid points only.
The rigorous infimum over the window uses L(y_i)/(cλ^{y_{i+1}}), which gives Δ = 0.8435 on a 1/64 grid (x ≥ 2^4 a).
The certified k = 14, λ = 1.80 vector with base window Y = 8.25 gives

  π_a(x) ≥ 0.7146 · (x/a)^{0.848}   for x ≥ 2^{6.25} a   (a ≡ 2 mod 3; a ≡ 1: divide by 1.8, x ≥ 2^{7.25} a),

the best explicit bound for 2^{6.25} ≤ x/a ≤ 2^{20.8}. The certified k = 15, λ = 1.82 vector
(`certs/spread_k15_1.82/`) gives π_a(x) ≥ 0.5681 (x/a)^{0.8639} for x ≥ 2^{6.25} a, which is best for
2^{20.8} ≤ x/a ≤ 2^{251}, above which k = 22 takes over. **k = 16, λ = 1.83** (certified,
`certs/spread_k16_1.83`): 0.5514 (x/a)^{0.8718} for x ≥ 2^{6.25} a. It dominates k = 15 everywhere and k = 14 from
2^{15.7}, and is best up to 2^{288}. A k = 17, λ = 1.84 vector was started the same night. Δ_Y for this vector peaks at
Y ≈ 8–9 (0.66–0.71), with the argmin moving from dense classes (Y ≤ 8) to the capped class c = 17.8 (Y ≥ 9).

**Empirical densities (`pred_density.py`, n < 2^32, 68 min on the GPU).** π_a(X)/X for a < 3^8 is converged to
three decimals between X = 2^20 and 2^32 (a = 5: 0.9378 → 0.9379; 7: 0.1916 → 0.1912; 11: 0.4440 → 0.4458;
13: 0.4749 → 0.4765; 16: 0.0622 → 0.0621): Conjecture A is numerically solid for small a, and d_a·a ≥ 0.67 over
a ≡ 2 (mod 3), a < 6561 (median 7.2), consistent with the lifted constants Δ ≈ 1 (the argument above predicts
d_a ≥ Δ₀/a). Class means of d_a·a correlate with the Perron vector at 0.92–0.93 (log, k = 4 … 6) and 0.90 (k = 8),
unchanged from X = 2^20 (`pred_compare.py`); with the bounded λ = 1.60 solution 0.76–0.91. The empirical spread of
the class means (51 → 2713 for k = 4 → 8) is far larger than any LP profile's because d_a·a carries the a-dependence
within a class, not only the class dependence.

**Why this matters beyond constants.** If Δ_best(k) stayed bounded below as k → ∞ (for the Perron vectors at λ_k),
then π_a(x) ≥ Δ₀ (x/a)^{γ_k} for x ≥ a 2^{Y(k)} with Y(k) ≈ k, and choosing k ≈ log₂(x/a) gives
π_a(x) ≥ Δ₀ (x/a) exp(−(1 − γ_k) ln(x/a)): with 1 − γ_k ≈ A q^k (geometric, q < 1) the exponent tends to 0 and
**positive density follows from λ_k → 2 alone**; with sub-geometric decay 1 − γ_k ≈ k^{−b} one still gets
x/exp((log x)^{1−b}). So Conjecture A reduces to (a) λ_k → 2 (avenue 1) and (b) a uniform base constant, i.e. the
guaranteed trees of all classes tracking c^m λ^y to height ≈ k — a finite statement at each k.

**Finer residues (`base_lift_fine.py`, same day).** With residues mod 3^{k′} the guaranteed trees decide k′ odd
steps and the base constant uses the min over the fine classes inside each coarse class. Δ_best (Perron vectors):

| k | k′ = k | k′ = k + 2 | k′ = k + 4 | k′ = k + 6 (30 worst classes only) | k′ = k + 8 (30 worst) |
|---|---|---|---|---|---|
| 6 | 0.83 | – | – | 1.18 (10 worst) | 1.41 (10 worst) |
| 7 | 0.68 | 0.93 | 1.17 | 1.25 | 1.33 |
| 8 | 0.54 | 0.75 | 0.99 | 0.99 (no gain) | – |
| 9 | 0.38 | 0.60 | 0.80 | 0.80 (no gain) | – |

Refining only the worst 30 classes helps at k ≤ 7 and not at k ≥ 8: the limiting set is broad (many classes sit
near the minimum), so uniform refinement is needed, and it costs 10× per two levels (k = 9, k′ = 13: 5·10⁹ nodes,
8 min in numpy). At fixed offset k′ − k = 4 the constant is 1.17, 0.99, 0.80 for k = 7, 8, 9, still falling ≈ 17 %
per level; the mean ratio over classes stays ≈ 1.5–1.7, so it is the dense tail that limits Δ. Whether k′ − k has to
grow with k to keep Δ_best bounded is unresolved; this is the computation that decides (b), and it needs a GPU
enumeration for k ≥ 10 (3^{k′−1} fine classes with 10³–10⁴ nodes each).

**Next.** GPU version of the fine enumeration; Δ_best(k) at k′ = k + 6 uniformly for k = 8 … 11; certify lifted
bounds at k = 12–14 for the explicit table.


## 18. No divergence as an arithmetic property of the 2-adic parity map

**Claim.** Let Q: ℤ₂ → ℤ₂ be the parity-vector map (Bernstein–Lagarias conjugacy of T with the shift). Q(n)'s
digits are the parities along the orbit of n, and the inverse is the explicit 2-adically convergent series
Φ(s) = −Σ_{i≥0} 2^{a_i} 3^{−(i+1)}, a_i = position of the i-th odd step. An integer n has a divergent orbit iff Q(n)
is not eventually periodic. Lagarias's periodicity conjecture is "Q maps rationals to rationals"; no divergence for
integers is its special case Q(ℤ) ⊆ ℚ. In this form the problem is an irrationality/transcendence statement about a
series in which 2 and 3 enter only through 2^{a_i} 3^{−i}: if Σ 2^{a_i} 3^{−i−1} is an integer, then (a_i) is
eventually arithmetic (gaps 2, the trivial cycle) after a finite prefix.

**Why well posed.** Terras: the first L parities are a bijective function of n mod 2^L, and for an integer n the
residues n mod 2^L are n itself once 2^L > n, so the whole parity sequence is a property of a single 2-adic number
with finite expansion. The "no-go" facts (avenue 21) show a proof must use unbounded lookahead and the specific pair
(2, 3); this formulation contains exactly that and nothing else. p-adic Mahler-type methods (functional equations
Q(2x) = 2Q(x), Q(x) = 1 + 2Q((3x+1)/2) for odd x) have not been applied to it as far as we know; the functional
equation is affine rather than a power map, which is what makes it hard.

**First steps.** Compute (a_i) for all n ≤ 2^40 (the gap sequences a_{i+1} − a_i), tabulate their statistics as a
subset of sequences of density θ = log 2/log 3, and look for any rigidity that distinguishes integer-generated
sequences from random ones (e.g. constraints on prefixes mod 3^j from n being an integer: 3^{m} n ≡
−Σ_{i<m} 2^{a_i} 3^{m−1−i} mod 2^{a_m}). Then survey transcendence methods for 2-adic series with 3-adic
denominators. Compute days; mathematics months.

**Payoff.** Settles divergence for integers; with avenue 19 (cycles) this is the conjecture.

**First step in progress (2026-10-09, `parity_stats.py`, `analyse_parity.py`).** For all n < 2^32 on the GPU: total
stopping time, odd-step count, height, the last time the orbit is at or above n, gap histograms and gap-pair
transition counts in three regimes (the window t < 32, where Terras makes the parities exactly i.i.d. fair bits; gaps
starting at values ≥ 2^24 beyond the window; and the small-value descent). Already clear from the test runs: the
local statistics cannot show "integer rigidity" at all — for any set of values x the next gap is 1 + v₂(3x+1),
geometric by Terras, so deviations from the random model are selection effects (which orbits are sampled, and how
often a segment is counted through merging) and end effects of the descent to 1. The content of avenue 18 is global
(the series Φ and eventual periodicity), not local; the run is kept for the excursion records.

## 19. All cycles by equidistribution of numerators modulo 2^n − 3^k

**Claim.** A cycle of length n with k odd steps corresponds to a parity vector v with k ones whose numerator
N(v) = Σ_j 3^{k−1−j} 2^{a_j} must be divisible by 2^n − 3^k (then x = N(v)/(2^n − 3^k) is the cycle element).
There are binom(n, k) ≈ 2^{0.951 n} vectors (k ≈ 0.63 n) and the modulus is ≈ 2^n, so if N(v) were equidistributed
modulo 2^n − 3^k the expected number of integer cycles of length n would be ≈ 2^{−0.049 n}, summable: finitely many
cycles, and none beyond the known ones once n exceeds a computable bound. A proof is an exponential-sum
(Weyl/large-sieve) statement over the combinatorial family of parity vectors, with Baker's method covering the
vectors with few local minima (the regime where Simons–de Weger and Hercher work, avenues 4 and 13).

**Why well posed.** The question is purely about the distribution of a specific additive function of subsets
modulo a specific integer; nothing about orbits is needed. The known theory (Eliahou, Simons–de Weger, Hercher)
is the sparse-local-minima end of the same count.

**First steps.** Compute the exact distribution of N(v) mod (2^n − 3^k) over all vectors for n ≤ 40 (GPU; 2^{38}
vectors at n = 40) and measure the discrepancy against uniform, by n and by number of local minima; find whether
the discrepancy decays like a power of the modulus. Then attempt the exponential-sum bound for the family.
Compute days; mathematics months to a year.

**Payoff.** Settles cycles for all m, which no verification range can; with avenue 18 this is the conjecture.

**First step done (2026-10-09, `cycle_numerators.py`, `cycle_analysis.py`; n ≤ 32, all 2^n parity vectors per n on
the GPU, 104 s in total).** (i) Zeros: for every n ≤ 32 the only v with N(v) ≡ 0 (mod 2^n − 3^k) are the all-even
vector (x₀ = 0) and, for even n, the two rotations of the trivial cycle (10)^{n/2}: no other cycle of length ≤ 32,
as known. (ii) Weyl sums S_h = Σ_v e(h N(v)/m)/binom(n, k), h ≤ 8: at the largest admissible k (the cycle-relevant
regime, where m = 2^n − 3^k ≪ 2^n) they sit at the random level, |S_h|·√binom = 0.6 (n = 24), 1.3 (n = 32); one and
two steps below k_max the ratio is 18 and 89 at n = 32, and for k ≤ n/2 the h = 1 sum is of order 1 at every n
(0.27 at k = n/4, 0.027 at k = n/2 for n = 32) and does not decay with n. The latter is intrinsic and not about
cycles: for m ≈ 2^n the fraction N(v)/m ≈ Σ_i 3^{o_i} 2^{i−n} is dominated by the few top set bits of v, so it is far
from uniform mod 1; equidistribution holds exactly where the modulus is small relative to 2^n, which is where n/k
approximates log₂ 3 and where large cycles would have to live. The quality tracks m/2^n: at n = 30 (m/2^n = 0.64)
the ratio at k_max is 6.9, at n = 24 (0.14) 0.6, at n = 32 (0.19) 1.3. So the heuristic count binom(n, k)/m is
supported in the relevant regime, and the exponential-sum statement a proof needs can be formulated as: for n/k a
convergent-type approximation of log₂ 3, the numerators are equidistributed modulo 2^n − 3^k with error O(binom^{1/2+ε}).
**Next:** push n to 40 at k near k_max only (binom(40, 25) = 4·10^{10}, GPU hours), and test the dependence of the
error on the quality of n/k as an approximation to log₂ 3.

**Step 2 (2026-10-10, `cycle_numerators_k.py` → `cycle_numerators_k.json`).**

A GPU kernel enumerates only weight-k parity vectors: each thread unranks a combination in colex order, then steps
with Gosper's hack. N(v) mod m is built from a term table 3^cnt 2^i mod m, and h·N mod m is exact in uint64. It agrees
with the all-vector run of step 1 for n ≤ 24 (zeros identical, Weyl sums to 5·10^{−8}), at about 1.5·10^9
vectors/s.

Results:
- n = 25 … 40 for k = k_max, k_max − 1, k_max − 2, and n = 41 … 45 for k = k_max. That is up to binom(45, 28) ≈
  1.1·10^{12} vectors per (n, k).
- **No nontrivial zero** anywhere. The expected counts binom/m are 0.07–1.7 per (n, k).
- **Weyl sums at k_max are governed by m/2^n:**
  - when m/2^n ≲ 0.3, |S_h|·√binom stays at the random level: 0.99 (n = 35, m/2^n = 0.087), 1.70 (n = 27, 0.038),
    1.72 (n = 43, 0.133), 3.5 (n = 40, 0.23);
  - when m/2^n ≈ 0.35–0.66 it grows with n: 6.9 (n = 30), 15 (n = 36), 55 (n = 38), 86 (n = 41), 139 (n = 44,
    0.567), 17 (n = 45, 0.350);
  - at k_max − 1 and k_max − 2 (m/2^n ≈ 0.7–0.96) it grows much faster (up to ~10^3 at n = 38).
- The bias is the low-frequency one identified in step 1: N(v)/m is dominated by the top bits when m is comparable
  to 2^n.
- Large cycles need n/k close to log₂ 3, i.e. m/2^n small. That is exactly the regime where the data stay at the
  random level, and it now holds to n = 45.

**What this does and does not show.** It supports the heuristic count binom(n, k)/m in the cycle-relevant regime.
The quantity a proof needs is a fine-scale (all h ≤ m) equidistribution statement uniformly in n; small-h Weyl sums
only probe large scales. **Next:**
- (a) probe fine scales: zero counts in residue classes modulo divisors of m, or the distribution of N(v) mod m in
  short windows;
- (b) restrict to the convergent-type pairs (n, k) = (q_j-multiples) where m/2^n is smallest;
- (c) the theory side: the exponential-sum statement for the family of parity vectors.

**Step 3 (2026-10-10, `cycle_numerators_fine.py` → `cycle_numerators_fine.json`; validated exactly against brute
force at n = 24).**

Fine-scale tests at k_max, n = 24 … 40. Two kinds of count:
- **Windows next to 0:** #{v : N(v) mod m < m/2^{10j}} and just below m, for j = 1, 2, 3. These are at the random
  level everywhere (|z| ≲ 3).
- **Divisibility by prime factors p | m:** #{v : N(v) ≡ 0 (mod p)}. This is often far from binom/p:
  - ×11.4 for p = 186793 at n = 24 (m = 13·p);
  - ×4.4 for p = 14753 at n = 26 (m = 1631·p);
  - ×1.77 for p = 24917 at n = 32 (m = 32435·p);
  - small but highly significant deviations for p = 5 (−0.25 % at n = 37, +0.7 % at n = 32).

Explanation (checked by brute force at n = 24: the 80 zeros mod 186793 are 7 rotation orbits of size 8 plus one
of size 24):
- **(1) Algebraic factors from periodic vectors — the large anomalies.** If d = gcd(n, k) > 1 then
  2^n − 3^k = (2^{n/d} − 3^{k/d}) · Φ with Φ = Σ_{t<d} 2^{(n/d)t} 3^{(k/d)(d−1−t)}. Every d-periodic parity vector
  v = w^d has N(v) = N(w)·Φ, so it is ≡ 0 modulo every prime factor of Φ. Examples:
  - n = 24, k = 15: Φ = 2^16 + 2^8 3^5 + 3^10 = 186793 = p, and the 7 necklaces of w (length 8, weight 5) give the
    excess.
  - n = 26, k = 16: Φ = 2^13 + 3^8 = 14753 = p, and the binom(13, 8) = 1287 periodic vectors explain
    1599 ≈ 360 + 1287.
  - n = 32, k = 20: the biased primes 499 = 2^8 + 3^5 and 24917 | 2^16 + 3^10 = 5·24917 come from the factorisation
    (2^8 − 3^5)(2^8 + 3^5)(2^16 + 3^10).

  Periodic vectors only repeat a shorter pattern, so they never produce a new cycle (x₀ = N(w)/(2^{n/d} − 3^{k/d})).
- **(2) Small primes with small orders.** For example p = 5 with ord₅2 = ord₅3 = 4, even at gcd(n, k) = 1 (n = 27).
  N mod p is then a sum over a short Markov chain and is slightly non-uniform. The deviation decays with n:
  −2 % at n = 27, −0.25 % at n = 37.
- **(3) Rotation clustering (variance).** For p | m, rotating v multiplies N(v) by a unit mod p, so zeros mod p come
  in whole rotation orbits. The Poisson z-scores therefore overstate significance by up to √n.

Equivalently, in Fourier terms: #{N ≡ 0 mod p}/(binom/p) − 1 = Σ_{j=1}^{p−1} S_{j·m/p}, i.e. the Weyl sums at
frequencies (m/p)ℤ. These are low frequencies exactly when the cofactor m/p is small.

**Check with periodic vectors removed** (`cycle_numerators_fine.py … --aperiodic` → `cycle_numerators_fine_aper.json`,
n = 24 … 40; the expected count uses the Möbius count of aperiodic vectors):
- Every large anomaly disappears. At n = 26, p = 14753 goes from ×4.4 to ×0.87 (z = −0.5 per necklace). At
  n = 24, p = 186793 leaves a single genuine rotation orbit (one necklace against 0.29 expected).
- The only remaining deviations with |z| > 4 per necklace are:
  - p = 5 (ord 4 for both 2 and 3): ×0.98 … ×1.008 at n = 25, 27, 30, 32, 37, shrinking with n;
  - p = 499 = 2^8 + 3^5 at n = 32: ×1.035. 499 divides 2^16 − 3^10, so this is likely the same algebra one level
    finer.

**Consequence for the heuristic.** For the cycle count, the periodic vectors must be removed: they belong to
(n/d, k/d). After that, the only local corrections are mild small-prime effects. Under that reading, the
equidistribution heuristic for primitive parity vectors survives every fine-scale test to n = 40. The aggregate near 0, which is what a cycle needs, is
consistent with uniform at the scales tested (down to m/2^{30}). The open question for a proof is the full
zero-frequency aggregate (all h). That is a statement about Σ_{h mod m} S_h, i.e. it again needs the fine-scale
exponential sum bound.

## 20. The adelic picture: ℤ₂ × ℤ₃ and a Furstenberg-type rigidity theorem

**Claim.** The forward dynamics is a 2-adic object (parity, Q on ℤ₂), the backward branching a 3-adic one (the
residue classes mod 3^k of Krasikov–Lagarias, our limit measure on ℤ₃), and the integers are the diagonal
ℤ ⊂ ℤ₂ × ℤ₃. The orbit closure of a hypothetical divergent orbit is a closed subset of ℤ₂ × ℤ₃ carrying both a
×3-type structure (the odd step) and a ÷2-type structure (the even step). Furstenberg's ×2 ×3 theorem says that
closed sets invariant under two multiplicatively independent maps are either finite or everything; a rigidity
statement of this kind for the Collatz pair would force the orbit closure to be either small (contradicting the
Terras uniformity of parity vectors along a divergent orbit) or everything (contradicting the density facts of
avenue 17). It would also explain why the problem is hard: it sits exactly on the 2-adic/3-adic transversality
that makes ×2 ×3 rigidity deep.

**Why well posed.** Both codings are explicit, our limit measure on ℤ₃ is the first concrete object on the 3-adic
side, and the rigidity literature (Furstenberg, Rudolph, Johnson, Host, Lindenstrauss) is a developed theory
with known obstacles (entropy assumptions) that can be tested against Collatz data.

**First steps.** Write the two codings down jointly (for n: the parity sequence in ℤ₂ and the predecessor-tree
address in ℤ₃), compute them for n ≤ 2^30, and measure how the 3-adic limit measure and the 2-adic parity structure
correlate along orbits; then identify which rigidity theorem's hypotheses (invariance, entropy) the Collatz orbit
closure can be shown to satisfy. Compute weeks; mathematics a year.

**Payoff.** Would kill divergent orbits and explain the difficulty at once.

## 21. Map the no-go theorems, then try the one mechanical route not excluded

**Claim.** Terras's theorem (all parity vectors of length L occur, as n mod 2^L) implies that no potential
V(n mod M) can decrease along every orbit, and the same argument excludes bounded lookahead (V depending on n mod M
and the next L parities): for every L there are n with L odd steps ahead, growing by (3/2)^L. Conway's
undecidability excludes methods uniform over generalised Collatz maps; Yolcu–Aaronson–Heule show matrix
interpretations only prove weakenings. Stated and proved cleanly, these delimit where a proof can live: it must use
the specific pair (2, 3) and unbounded lookahead, which is what avenues 18–20 do. The one mechanical route not
excluded is termination of the Yolcu–Aaronson–Heule rewriting system with semantic labelling by residues mod 3^k
and the K–L weights as the ordering, which supplies exactly the unbounded-residue information that plain matrix
interpretations lack.

**First steps.** (i) ✅ `notes/no_go_theorems.md` (2026-10-09): Theorems 1–3 with proofs from Terras's lemma — any
potential that is a function of n mod M, or of n mod M plus L parities of lookahead, or monotone in n within residue
classes mod M, fails on a set of positive lower density (the all-odd runs n ≡ −1 mod 2^L); this covers the
"bounded multiplicative potentials" claimed excluded elsewhere. (ii) Build the labelled rewriting
system with residues mod 3^k for k ≤ 6 and search for a certificate with a termination tool (AProVE/TTT2) or our
own LP over the labelled rules; the expected outcome is a precise statement of what fails, which sharpens (i).
Weeks.

**Payoff.** A map of the negative space, and the only avenue where compute alone could produce a proof.

## 22. Structure theorems for L^NT_k: attainment, tightness, uniqueness, strict increase (PROVED 2026-10-09)

**Statement** (`notes/strict_monotonicity.md`). For every k ≥ 2, with λ_k := sup{λ ∈ [1, 2] : L^NT_k(λ) feasible}:
(i) the supremum is attained and 1 < λ_k < 2;
(ii) every feasible point at λ_k satisfies all principal inequalities with equality, and it is unique up to scaling;
(iii) λ_k < λ_{k+1}.
Consequences:
- c·λ_k^y is an exact positive monotone solution of Krasikov's I_k, so no exponent above log₂ λ_k can be extracted
  from I_k. This was K–L's stated belief after their Theorem 2.2.
- Every Applegate–Lagarias splitting/truncation LP has λ* ≤ λ_k ([AL2, Conjecture 4.1]).

**Literature status.**
- [AL2] (1995) called (iii) "easy to prove", with a sketch that shows only that the lifted solution has a strict
  inequality somewhere.
- [KL] (2003) writes "It remains an open problem to show that the values λ_k are strictly increasing in k", and
  calls (i), (ii) "likely … but this may be difficult to prove".

**Key idea.** m ↦ 4m is a single cycle of length 3^{k−1} on the principal classes (lifting the exponent:
v₃(4^n − 1) = 1 + v₃(n)), and every row contains λ^{−2} c_{4m} without a minimum. So the monotone, homogeneous,
superadditive map F_λ is irreducible:
- slack in one row spreads backwards to all rows in N steps (Lemma 3);
- zeros spread forwards (Lemma 7, uniqueness).

Tightness then follows from maximality plus continuity in λ. Strict increase follows because the tiled solution
gains slack exactly where it is not constant across its top digit, and a tight fixed point never is (the A–L descent
argument).

**Checks** (`monotone_check.py`, k ≤ 9): the gain is zero on class 5 and positive on 2/3 of classes 2 and 8; the
Collatz–Wielandt vectors give r_{k+1}(λ_k) ≥ 1.104 … 1.0059; random starts converge to the same fixed point.
Observed but unproved: r_k(λ) is decreasing on [1, 2], and L^NT_k is infeasible for λ ∈ [4, 1000] (k ≤ 7).

**What it does not give: a rate.** Slack travels along the ×4 cycle with factor λ^{−2} per step, so the δ in
λ_{k+1} ≥ λ_k + δ is exponentially small in k. The quantitative form λ_{k+1} − λ_k ≥ κ(2 − λ_k), with κ
independent of k, is equivalent to geometric convergence λ_k → 2 (by tightness, 2 − λ_k ≍ 1 − ρ_k). That is avenue 1
in a sharper form. The gain must be spread by the auxiliary (expanding, mixing) branch, whose min-switching is
exactly the alignment question of §1.

**Corollary (2026-10-10, Lean `rho_eq`, `rho_strictMono`).** ρ_k = 3(λ_k − 1)/λ_k^α exactly, and 1 − ρ_k is
strictly decreasing in k. So the ρ_k table of §1 is an exact reparametrisation of λ_k.
**Done 2026-10-10.** (a) Lean 4 formalisation: `lean_formal/KLMonotone/Basic.lean`, ≈1250 lines, 10 s, standard
axioms only. It covers (i)–(iii), uniqueness, the exact solution of I_k, equivalence with K–L's literal (2.7)–(2.14),
and residue-faithfulness of all index maps (`KLMono.KL_lambda_strictMono`). (b) Preprint §2.4 (draft 0.9).
**Next.** (c) Try the quantitative version with a Poisson-equation test vector
z = tile(c) + h: the superadditivity bound F(x + h) ≥ F(x) + F(h) needs h nearly constant over lifts, and the
spectral gap of §16 does not close (|λ₂| ≈ 0.865), which is the input such an argument would need.

## 23. Mazur's seed averaging versus the K–L minimum (proposed 2026-10-10)

**Observation.** The entire finite-k loss of the K–L program is the minimum over the three lifts (1 − ρ_k).
Mazur's positivity step does the opposite: it averages a backward mark over unit residues, *chooses* a residue class
with mark ≥ 255/256, and only then picks a seed in that class (`notes/m2_audit.md` §7).

**Question.** Is there a K–L-type linear system for one well-chosen seed class per level, with the minimum
replaced by a choice? Such a system would certify exponent 1, or positive density, with explicit constants. A
candidate: certify a lower bound only for a set of residue classes closed under the backward maps that the
argument actually follows, rather than for all classes.

**Why.** It would give an effective, explicit Conjecture A, which Mazur's proof does not provide.

**First step.** Write down which inequalities of I_k remain valid when φ is replaced by the count for a fixed seed
class, and whether the resulting system is still monotone and homogeneous (then avenue 22's machinery applies).

## 24. Effective constants for Conjecture A (proposed 2026-10-10)

Mazur's c_a is ineffective for general a. (The seed is bounded by the largest element of a hypothetical cycle
through the odd part of a.) For a = 1 it is explicit but tower-sized. Questions:
- Can verification to 2^71, which bounds any cycle's minimum, make c_a effective for all a < 2^71?
- What is the best explicit c_1 obtainable by re-running his constants with modern numerical inputs (Tao's mixing
  constant, the b = 2^80 scale)?

Compare with the empirical d_a·a ≥ 0.67 (`pred_density.py`, a < 3^8, n < 2^32).

## 25. Density one of P(1) (proposed 2026-10-10)

By Mazur's Cor. 1.2 (formal), Collatz ⇔ upper density of P(1) = 1. Known nearby results:
- Tao (log density): almost all orbits fall below any f(n) → ∞.
- Mazur's base paper: positive density of n reaching 1 within 10.46 ln n steps.

The precise gap is Tao's theorem with f constant (= 2^71) in natural, or even just lower logarithmic, density.
Log density 0 of the non-convergent set forces lower natural density 0, which contradicts Cor. 1.2 unless there is
no counterexample.

**First step.** Read where Tao's argument needs f → ∞ (his remarks after Thm 1.3) and whether Mazur's seed-mass
method could replace it for the fixed target set [1, 2^71]. Theory; months; long odds, but this is now *the*
statement.

## 26. Formal m-cycle bounds: generalise the "two-rise" bound (proposed 2026-10-10)

**Background.** The audited repository (avenue 13, `notes/mcycles_102_audit.md`) gets past Hercher's bootstrap with
two elementary ingredients:
- the **two-rise bound**: for odd n < 2^N, the first two ascents total ≤ B(N), with B sharp, computed by a 2-adic
  search;
- a chain argument over the local minima of a candidate shape.

Both are kernel-checked as certificates. It stops at m = 101 only for compute reasons.

**Questions.**
- (a) r-rise bounds for r ≥ 3: the first r ascents total ≤ B_r(N). These are again 2-adic searches, cheap on the GPU
  (our `cycle_dip.py` / `cycle_lp.py` machinery already enumerates residue classes with exact linear forms).
- (b) Do r-rise bounds push m much further than larger two-rise grids do?
- (c) Can the chain argument be phrased as an LP over shapes, like our `cycle_lp.py`, so that one certificate covers
  many m?

**Payoff.** A formally verified, conditional record on m-cycles, with our existing tools. It is also a bridge between
the cycle track and certificate checking at scale (avenue 5's Lean machinery). Days.

## 27. Primitive-necklace heuristic for cycle counts (proposed 2026-10-10)

**Observation** (avenue 19, step 3). When g = gcd(n, k) > 1, 2^n − 3^k factors cyclotomically, and every periodic
parity vector w^d has N(w^d) = N(w)·Φ_d. These vectors produce all the large divisibility anomalies, but never a new
cycle.

**Proposal.** State the cycle heuristic for **primitive necklaces**: count aperiodic vectors up to rotation, with
local factors only at the small primes where 2 and 3 have small order. Test it as a prediction:
- the number of 3x+d cycles for small d (avenue 11 data, `cycles_d.py`), where many (n, k) admit cycles;
- the 3x+13 cluster of seven 8-cycles (avenue 3).

**Payoff.** A sharper, falsifiable model for cycle counts across the 3x+d family, which is the testbed any cycle
argument must pass.

**First data (2026-10-10, `cycles_by_length.py` → `cycles_by_length.json`).** This is an exact census of all cycles
of T_d of length ≤ 34, for all 67 d < 200 with gcd(d, 6) = 1. The GPU enumerates every parity vector, and a cycle
exists iff (2^n − 3^k) | d·N(v), since the 2-adic parity map is a bijection on periodic points. It finds cycles
whatever the size of their elements, about 10 s per d.
- **Validation.** It reproduces `cycles_d.py`'s brute-force lists exactly for d ≤ 29 at length ≤ 24, and recovers the
  27-step 3x+5 cycles through 187 and 347.
- **Long cycles.** 72 cycles of length ≥ 22, e.g.:
  - five 27-step cycles for d = 71, because 71 | 2^27 − 3^17 = 5·71·14303; the necklace model predicts 4.4;
  - a 34-step cycle for d = 173 with minimum 7;
  - 29-step cycles for d = 137 (three of them).
- **Clusters are algebraic.** The seven 8-cycles of 3x+13 are all 7 necklaces of (8, 5), because
  2^8 − 3^5 = 13 = d, so every parity vector gives an integer x₀.
- **Uniform necklace model** E = Σ (aperiodic necklaces)·gcd(m, d)/m. It overestimates the totals:
  - lengths 10…34: observed 127 vs 280 (ratio 0.45, χ²/dof = 1.6);
  - lengths 16…34: 92 vs 182 (0.50, χ²/dof = 1.05);
  - lengths 22…34: 72 vs 110 (0.65, χ²/dof = 0.70).

  The deficit shrinks with length. A likely cause: for small k/n, N(v) ranges over less than one period of m, so
  "uniform mod m" overcounts; the right model conditions on the range of N(v)/m.

Where the deficit sits (all d, lengths 10–34, observed/expected by k/n):

| k/n | < 0.40 | 0.40–0.50 | 0.50–0.56 | 0.56–0.60 | 0.60–0.62 | 0.62–log₃2 |
|---|---|---|---|---|---|---|
| observed / expected | 11 / 37.8 | 23 / 72.0 | 27 / 75.4 | 19 / 31.1 | 8 / 35.8 | **39 / 27.8** |

- At small k/n the model fails (ratio 0.2–0.6). There m ≈ 2^n and N(v) mostly doesn't wrap modulo m (the top-bit
  bias of avenue 19), so "uniform mod m" is the wrong model.
- In the cycle-relevant regime k/n → log₃ 2, where m ≪ 2^n, it is roughly right (ratio 1.4). The excess there
  includes algebraic clusters such as d | 2^n − 3^k.

That is consistent with the Weyl-sum picture: equidistribution holds where large cycles would have to live.

Extended to length ≤ 38 for d ∈ {5, 7, 11, 13, 17, 19, 23, 25, 29, 71} (`cycles_by_length_n38.json`, about 160 s
per d): **no cycles of length 35–38**. The cycle lists of these d are complete up to length 38, whatever the size
of the elements.

**Next.** Model the small-k/n regime by the actual distribution of N(v)/m instead of a uniform one.

## 28. The depth K–L system: a faster-mixing model of avenue 1, and a route to Conjectures B / C′ (proposed 2026-10-10)

The residue-class system for pruned-tree depth counts (avenue 15) is the K–L construction without the ×4 drift:
Φ(v)(c) = v(2c) + β(c) min_t v(l_t(c)) on classes mod 3^r. Summing gives μ_r = 1 + ρ_r/3 exactly, the analogue of
K–L's summed inequality, so μ_r → 4/3 ⇔ ρ_r → 1. Its loss decays at ≈ 0.65 per digit (K–L: ≈ 0.93), and its
certificate spread stays bounded (≈ 3.5; K–L: ∝ 1.52^k).

Questions:
- (a) Prove ρ_r → 1 here, a strictly easier instance of avenue 1. The avenue 22 machinery (single-cycle
  irreducibility via the doubling map c ↦ 2c, tightness, uniqueness, strict monotonicity in r) should transfer
  verbatim. The quantitative step is the open one.
- (b) Explain why the decay is 0.65 here and 0.93 for K–L. The difference is the ×4 transport: K–L's isometric
  branch carries top-digit information with weight 1/4, while here the doubling edge has weight 1 but the depth
  index advances.
- (c) A bounded spread of the extremal certificates would give Conjecture C′, uniform in r.
- (d) The limit object is the 3-adic operator L v(c) = v(2c) + [c ≡ 2, 8 (9)] v((2c−1)/3) on ℤ₃^×. It sums over the
  T-preimages; T acts 3-adically as an isometry on the even branch and as a 1/3-contraction on the odd one.
  Integrating against Haar measure gives eigenvalue 4/3. The bounded certificate spread and the 0.65-per-digit decay
  suggest a continuous, Hölder eigenfunction with exponent ≈ −log₃ 0.65 ≈ 0.39; the K–L limit object has
  0.04–0.09 and is unbounded. Proving such an eigenfunction exists, with a quantitative modulus, would give
  ρ_r → 1 at a geometric rate. Since 2 is a primitive root mod 3^r, c ↦ 2c is a single cycle, so the avenue 22
  machinery (irreducibility, tightness, uniqueness, strict monotonicity in r) transfers verbatim.

**Results 2026-10-10 (morning): one limit measure, and why 0.65** (`depth_system.py`, `syracuse_measure.py`).

1. *Consistency (exact, proved).* Let A_r be the min-free operator, A_r v(c) = v(2c) + β(c)·mean_u v(l_u(c)), and E_{r−1}
   the average over the top digit. Then E_{r−1}A_r = A_{r−1}E_{r−1} for r ≥ 3:
   - the doubling term commutes with E because ×2 maps fibres onto fibres;
   - in the aux term β depends on c mod 9, and the three top-digit lifts of c send (2c−1)/3 mod 3^{r−1} to the three
     lifts of (2s−1)/3 mod 3^{r−2}.

   Haar is a positive left eigenvector with eigenvalue 4/3. A_r is primitive: c ↦ 2c is a single cycle, and c = −1
   has a self-loop, since (2·(−1)−1)/3 = −1. So the Perron vectors h_r (mean 1) satisfy E_{r−1}h_r = h_{r−1} exactly
   (checked to 3e-15 for r ≤ 17). By Kolmogorov they are the level-r densities of a single probability measure ν on
   ℤ₃^×. The eigen-equation says that ν is the stationary law of the random walk
     x ↦ x/2 with probability 1 − p,   x ↦ (3x+1)/2 with probability p,   p = 1/4,
   i.e. the law of X = Σ_{j≥1} 3^{j−1} 2^{−(a_1+…+a_j)} with a_j i.i.d., P(a = m) = p(1−p)^{m−1}.

   **p = 1/2 is Tao's Syracuse random variable** (Forum Math. Pi 10 (2022) e12, Remark 1.13 identifies it as the
   stationary measure of x ↦ (3x+1)/2^a). The level-r marginals obey h_r = (1−p)·h_r∘(×2) + 3p·β·h_{r−1}∘σ, solved
   along the doubling cycle. No power iteration is needed; r = 17 takes 35 s.

2. *The K–L system is the p = 1/2 case.* K–L's operator at λ = 2, with min replaced by mean, has as Perron vector
   exactly Tao's Syracuse density restricted to m ≡ 2 (mod 3). Use h(2c) = h(4c)/2 for c ≡ 2 (mod 3), and for
   c ≡ 2 (mod 9) the aux class (2c−1)/3 ≡ 1 (mod 3) has h = h((4c−2)/3)/2, which gives weights 1/4, 3/4, 3/2.
   Checked to 1e-15 for k ≤ 12. So K–L size-counting is the fair-coin walk (Tao), and depth-counting is the p = 1/4
   walk. The actual c_k (at λ_k, with min) differs from Tao's density: TV 0.14 and log-correlation 0.987 at k = 12.

3. *The L² law (diagonal term exact).* Write δ_r = h_r − h_{r−1}∘proj (martingale difference). Then
   δ_r(c) = Σ_{j≥0} 3p(1−p)^j β(2^j c)·δ_{r−1}(σ(2^j c)). The diagonal part of E[δ_r²] is exactly
   (3p/(2−p))·E[δ_{r−1}²]. The cross terms are correlations E[δ_{r−1}(y)·δ_{r−1}(S_d y)] with
   S_d(y) = 2^d(y + 1/3) − 1/3, d even. Numerically they vanish, and the L² ratios converge to √(3p/(2−p)):

   | p | √(3p/(2−p)) | L² ratio r = 15 | L¹ ratio r = 15 |
   |---|---|---|---|
   | 1/4 | 0.6547 | 0.6503 | 0.6501 |
   | 1/3 | 0.7746 | 0.7722 | 0.7656 |
   | 0.4 | 0.8660 | 0.8652 | 0.8435 |
   | 1/2 | 1 | 1.0006 | 0.9279 |

   **This explains the depth loss rate 0.65 = √(3/7)** (4 − 3μ_r ratios 0.652–0.656; question (b) answered). It also
   puts K–L/Tao at the critical point. At p = 1/2 the diagonal factor is exactly 1, the density is (numerically) not
   in L², and all L¹ decay comes from cancellation. The L¹ ratio creeps up, 0.926 (r = 14), 0.928, 0.929, 0.931
   (r = 17), at the same pace as K–L's 1 − ρ_k ratios (0.919 at k = 14 … 0.933 at k = 22). Tao proves this L¹ decay
   is faster than any power (Prop. 1.14, Osc_{m,n} ≪_A m^{−A}; he predicts exp(−cm), Remark 1.15). That is the
   linear analogue of ρ_k → 1, and it implies ν_{1/2} is absolutely continuous.

4. *Threshold p = 1/3 for a bounded density.* −1 is the fixed point of x ↦ (3x+1)/2 (the trivial negative cycle),
   which contracts by 1/3. So the density at −1 is multiplied by 3p per level: measured 1.21 at p = 0.4 and 1.50 at
   p = 1/2, and argmax h = −1 for p ≥ 0.4. Spread at r = 13:

   | p | 0.2 | 0.25 | 0.3 | 1/3 | 0.36 | 0.4 | 0.5 |
   |---|---|---|---|---|---|---|---|
   | spread | 2.30 | 3.53 | 7.3 | 15 | 31 | 114 | 5678 |

   The spread is bounded for p < 1/3 and grows ~1.6^r at p = 1/2. That growth is the origin of K–L's
   C_max ~ 1.52^k. The min over the top digit removes the spike at −1 itself (argmax c_k ≠ −1), but not the growth.

5. *p = 1/4: the density looks continuous.*
   - Sup top-digit oscillation ratio ≈ 0.76 (Hölder exponent ≈ 0.25).
   - L^q ratios at r = 17: 0.6525 (q = 4), 0.658 (q = 6), 0.668 (q = 8), all below 3^{−1/q} (0.760, 0.833, 0.872),
     so Σ_r 3^{r/q}‖δ_r‖_q converges. Kurtosis is stable near 6.8.
   - Spread 3.5445 at r = 17, still rising (→ ≈ 3.552).
   - 1/min h_r = 2.03874 and max h_r = 1.73859 at r = 17, still rising. The exact extremal counts give
     (4/3)^k/N^−(k) → 2.0390–2.0395 (k = 48–59) and N^+(k)/(4/3)^k → 1.7420 (k = 48–55).

   So the extremal trees are, to about 2·10^{−4}, the min and max of one continuous function on ℤ₃^×. The
   normalised counts (3/4)^k N*_k converge to ν weakly: class-wise averages tend to h_r. This is a theorem, because
   E_r[(3/4)^k N*_k] = ((3/4)A_r)^k 1 → h_r by primitivity.

6. *Conditional theorem.* If ν_{1/4} has a continuous density (equivalently Σ_r ‖δ_r‖_∞ < ∞, or uniform convergence
   of h_r), then Conjecture C′ holds.
   - A continuous solution is positive: h ≥ (3/4)·h∘(×2), so a zero would propagate along the dense orbit 2^j x.
   - Collatz–Wielandt with V = h_r gives μ_r ≥ 4/3 − δ*_r, where δ*_r = max_c β(c)(mean − min over lifts)/h_r(c)
     ≤ ‖δ_r‖_∞/min h. Also V_min/V_max = 1/spread.
   - For each k pick r with δ*_r ≤ 1/k. Then N*_k(b) ≥ e^{−3/4}(4/3)^k/spread for all b and k, and symmetrically
     with max.

   The data suggest the sharp constants are min h and max h.

   **Proof programme:** a moment recursion. The diagonal coefficients are exact (for q = 2: 3p/(2−p)). What needs
   bounding is the decorrelation of the top-digit triples of δ_{r−1} under y ↦ 2^d(y + 1/3) − 1/3. A bound giving
   ‖δ_r‖_4 ≤ Cθ^r with θ < 3^{−1/4} proves C′. The same scheme at p = 1/2 is critical. There the min-system question
   (ρ_k → 1) asks for more than Tao's L¹ statement, but the obstacle is now located: cancellation at a critical
   point, not a missing estimate.

   **Check first (novelty):** Wirsching, LNM 1681 (1998), studies a 3-adic Markov process for the inverse map
   (Tao's footnote 5). The identification in item 1 may be in his framework.

Payoff: a publishable improvement now (A–L Theorem 1.1 from 1.302/1.358 to within 3·10^{−5} of 4/3), and a cleaner
testbed for the λ_k → 2 problem.

## Not avenues

- Scaling k: +0.005 in γ per level for 3× memory. Stopped at 21; 22 needs 64 GB, 23 needs 192 GB.
- Compressing c or refining sparsely: both tested and rejected (CLAUDE.md "Gränser", `adaptive.py`).
- Proving the conjecture through avenues 1–16: all are density or cycle statements; none touches divergent orbits.
  Avenues 17–21 are the ones aimed at the conjecture itself.
- Chamberland's real extension and the Berg–Meinardus functional equations: compute produces data on objects no
  easier than Collatz itself (2026-10-08). The Bernstein–Lagarias 2-adic conjugacy was listed here too; as a theory
  target rather than a compute target it is now avenue 18.
- Independently re-verifying Barina's 2^71 range on one machine: uncompetitive by orders of magnitude.
