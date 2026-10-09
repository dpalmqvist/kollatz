# Avenues: what could be explored next, and where each stands

Living document. Each entry: the question, why it matters, what exists in this repository, how to pick it up,
and an honest estimate of the payoff. Dates are when the entry was last touched. See `CLAUDE.md` for the
technical state of the code and `RESULTS.md` for the certified results. A referenced literature survey of
everything adjacent (cycle bounds, predecessor density, the long shots, formal verification) is in
`reports/Collatz adjacent work and references.md` (2026-10-08, notes in `research_notes/`).

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
| 13 | m-cycle bounds with the 2^71 verified range | publishable increment on Hercher's m ≤ 91 | open in print; one unrefereed Lean repo claims m ≥ 102 (lit. search 2026-10-08) |
| 14 | Matrix interpretations for the rewriting system | a success would be a proof; odds very low | proposed 2026-10-08 |
| 15 | Applegate–Lagarias extremal trees to depth 45–50 | direct test of Conjectures C / C′ | proposed 2026-10-08 |
| 16 | Spectrum, gap and traces of the K–L transfer matrix | mixing rate vs k; cycle footprints | first results 2026-10-08 (`spectrum.py`, k ≤ 15): gap does NOT close, see §16 |
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
| all levels 6 … k (6 seeds) | 13 | −8.9e-3 ± 1e-3 | 0.05119 / 0.04818 (+6 %) | 0.922 ± 0.02 / 0.920 |
| all levels 3 … k (3 seeds) | 11 | −4e-2 ± 1e-2 | +27 % | – |

Reading: (i) scrambling the top level alone costs nothing measurable from k = 9 on (at k = 13 the random
alignment is even marginally better); σ-only and π-only behave the same. (ii) Scrambling every fine level from 9
up costs ≈ 3·10^{−4} in λ per level, about 2 % of the per-level gain Δλ_k ≈ 0.013, and raises 1 − ρ by 1.6 % at
k = 14, with the decay ratio q_k unchanged within seed noise (0.005). (iii) The coarse levels carry real
arithmetic: scrambling from level 6 costs 10^{−2}, from level 3 several 10^{−2}, and the cost decays only slowly
with k (ratio ≈ 0.9). **So λ_k and the loss ratio q_k are mean-field quantities to ≈ 1 % in the loss and 2 % in the
per-level gain: the arithmetic of 2 and 3 enters through the coarse residues (mod 3^8, say) and the weights, and
the fine alignment can be replaced by independent uniform randomness.** Random K–L model := the exact system up
to level K0, lifted with i.i.d. uniform top-digit bijections above it. The question λ_k → 2 ⇔ q_k → q∞ < 1 can
therefore be posed in that model, which has no number theory left above K0: it is a random monotone
1-homogeneous recursion on a 3-adic tree, i.e. a quenched-versus-annealed question of the type studied for
branching random walks (Kontorovich–Lagarias's η_BP is the annealed rate). Caveats: the exact system is
*better* than random by a small offset, and no comparison theorem is known; and the residual per-level cost
(3·10^{−4}) has not been shown to vanish with k (runs to k = 15 pending).
**Next:** (a) a distributional (population-dynamics) formulation of the random model, which would allow k ≫ 22 at
fixed cost and decide q∞ for the model numerically; the ×4 transport makes each level a fixed-point equation for
the triple-shape law rather than a one-step map, so the formulation needs the cavity-style self-consistency;
(b) a proof of q∞ < 1 for the random model, if (a) says so.

**How to pick up.**
1. Measure convergence of the mass distribution μ_k(class) = c_m / Σc on 3-adic balls across k (total variation
   between level-j marginals of consecutive k). If it converges, a limit measure exists.
2. Compare the Perron vector of F at λ = 2 (finite k, spectral radius < 1 but the eigenvector exists) with c_k at
   λ_k. If the shapes agree, the limit object is the λ = 2 eigenmeasure of the 3-adic operator.
3. ✅ (2026-10-09) The boundary layer is the 1 − ρ_k sequence through R; the defect D_k is measured (`defect.py`).
   ✅ The recursion's mean-field character is tested directly (`meanfield.py`): random alignments reproduce λ_k, q_k.
   Next: distributional (population-dynamics) formulation of the random K–L model to reach k ≫ 22.
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

## Not avenues

- Scaling k: +0.005 in γ per level for 3× memory. Stopped at 21; 22 needs 64 GB, 23 needs 192 GB.
- Compressing c or refining sparsely: both tested and rejected (CLAUDE.md "Gränser", `adaptive.py`).
- Proving the conjecture through any of the above: all are density or cycle statements; none touches divergent orbits.
- Chamberland's real extension, the Berg–Meinardus functional equations and the Bernstein–Lagarias 2-adic
  conjugacy: compute produces data on objects no easier than Collatz itself (2026-10-08).
- Independently re-verifying Barina's 2^71 range on one machine: uncompetitive by orders of magnitude.
