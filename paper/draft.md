# Certified Krasikov–Lagarias predecessor bounds for the 3x+1 problem up to k = 22, with two-sided brackets and machine-checked instances

*Draft 0.1, 2026-10-08. Numbers marked [TBD] are being produced by runs in progress; everything else is from
`RESULTS.md`, `certs/*/cert.json`, `AVENUES.md` and `reports/Collatz adjacent work and references.md`.*

## Abstract

For a ≢ 0 (mod 3) let π_a(x) be the number of n ≤ x whose 3x+1 orbit reaches a. Krasikov and Lagarias (2003)
proved π_a(x) ≥ x^{0.84} for large x from a feasible point of a linear program L^NT_k(λ) on the residue classes
modulo 3^k, at k = 11. We extend the computation to k = 22 (3^{21} ≈ 1.05·10^{10} principal variables) and obtain
π_a(x) ≥ x^γ for every γ < 0.92509. Each level k = 12 … 22 comes with an integer certificate (the float32 solution
vector read as an exact integer vector) checked in int64 arithmetic by two independent programs, and, for
k = 2 … 21, with a second certificate proving that the LP at level k is infeasible slightly above the
certified λ, so that the Krasikov–Lagarias constants λ_k are bracketed to 2·10^{-5} … 10^{-4}. The instances
k = 18, 19 [and 20, TBD] are checked in Lean 4 inside Mazur's formalisation of the Krasikov–Lagarias theorem,
giving machine-checked statements x^{0.903}, x^{0.909} [and x^{0.915}] with a trust base of Lean's three standard
axioms plus two `native_decide` checks per level. We report measurements of the finite-k loss that separates
λ_k from 2, including the first spectrum of the linearised transfer matrix and a calibration run on 5x+1, and
state what they do and do not say about the question λ_k → 2, which is equivalent to π_a(x) ≥ x^{1−ε}.

## 1. Introduction

The 3x+1 map is T(n) = n/2 for even n and (3n+1)/2 for odd n. The predecessor set of a is the set of n whose
orbit passes through a; its counting function π_a(x) is what the "density" line of attack on the Collatz
conjecture measures. The refereed chain of lower bounds runs Crandall (1978, some positive exponent), Sander
(1990, 3/10), Krasikov (1989, 3/7), Wirsching (1993, 0.48), Applegate–Lagarias (1995, 0.65 by tree search and
0.809 by nonlinear programming) and Krasikov–Lagarias (2003, 0.84). Lagarias's 2010 survey still lists 0.84 as
the record and states the open problem π_1(x) > c(ε) x^{1−ε}. Krasikov and Lagarias observe in their §6 that
their constants λ_k are non-decreasing in k and that λ_k → 2 would give exactly that; nothing has been published
on that question since.

Three things changed between 2003 and now. Memory: the LP at level k has 3^{k−1} principal variables, and
3^{21} float32 values are 39 GB, which a single workstation now holds. Verification: a solution found in floating
point can be turned into an integer certificate checked exactly, so the computational part of the proof reduces
to a check anyone can re-run. Formalisation: Mazur's 2026 Lean development replaces the analytic Theorem 2.2 of
Krasikov–Lagarias by a second finite certificate (an "adaptive forced potential" on the same residue classes) and
checks both certificates by compiled evaluation, so that the whole statement for a given k is a Lean theorem.
This paper does all three for k ≤ 22, k ≤ 21 and k ≤ 20 respectively.

Related 2024–2026 work, all of it unrefereed and AI-assisted (see the survey in the repository for provenance):
msharpe248 obtains 0.8676 at k = 14 with a kernel-checked certificate and 0.895 at k = 17 informally; Mazur obtains
0.90 at k = 18 via `native_decide`; Menta2357 reproduces the 0.8418 of k = 11 kernel-clean. The three
implementations agree with ours at equal k to the precision of their respective roundings.

## 2. The Krasikov–Lagarias system

Principal classes are the residues m mod 3^k with m ≡ 2 (mod 3), the classes whose members have an odd
predecessor (2m − 1)/3 besides the even predecessor 2m. Eliminating the classes ≡ 1 and ≡ 0 (mod 3) gives, with
α = log₂ 3 and an unknown c_m ≥ 1 per principal class, the inequalities

- m ≡ 2 (mod 9): c_m ≤ λ^{−2} c_{4m} + λ^{α−2} c̄_{(4m−2)/3}
- m ≡ 5 (mod 9): c_m ≤ λ^{−2} c_{4m}
- m ≡ 8 (mod 9): c_m ≤ λ^{−2} c_{4m} + λ^{α−1} c̄_{(2m−1)/3}

where c̄_r = min(c_r, c_{r+3^{k−1}}, c_{r+2·3^{k−1}}) because the odd predecessor is known only modulo 3^{k−1}.
(The paper's equations (2.13)–(2.14) print 3^k where 3^{k−1} is meant; the reproduction of their Table 2
confirms the correction.) A feasible point for λ gives π_a(x) ≥ x^γ for every γ < log₂ λ and x ≥ x₀(a, γ)
(Theorem 2.2 and §6 of the paper), and the constant is explicit, Δ₁ = 1/(4 max c_m).

With index i for m = 3i + 2 the maps are affine: 4m ↦ (4i + 2) mod N, and the auxiliary index is 4j mod N/3 or
(2j + 1) mod N/3 for i = 3j or 3j + 2. The right-hand side F is monotone and 1-homogeneous, feasibility is
equivalent to r(F_λ) ≥ 1 for the cone spectral radius, and λ_k is the root of log r(F_λ) = 0.

## 3. Computation

Power iteration c ← F(c)/min F(c) with the Collatz–Wielandt bounds min F(c)/c ≤ r ≤ max F(c)/c, a secant method
on λ ↦ log r(F_λ) (3 to 5 evaluations per level), and warm starts by lifting the solution of level k − 1
(c_k[i + j·N_{k−1}] = c_{k−1}[i]). F is one Metal kernel computing all indices per thread in 64-bit integers;
the normalisation is folded into the coefficients so that the iteration needs two vectors. For k = 21 on a
24 GB machine and k = 22 on a 64 GB machine the update is compressed to int8 (c ← (c/m)(ρ₀ + S·d) with
d = round((F(c)/c − ρ₀)/S)), which needs 1.26 vectors; at k = 22 the vector exceeds Metal's single-buffer limit
and is held as three buffers indexed by the top ternary digit. Timings on an Apple M4 Pro (64 GB): k = 19, 40 s;
k = 20, 151 s; k = 21, 382 s; k = 22, 110 min at 49 GiB peak.

| k | N = 3^{k−1} | λ_k (numerical) | λ_cert | γ = log₂ λ_cert | λ_upper (infeasible) |
|---|---|---|---|---|---|
| 11 (K–L 2003) | 59 049 | 1.7922310 | – | 0.84 | 1.79225 |
| 12 | 177 147 | 1.8064236 | 1.8064 | 0.8531 | 1.80644 |
| 13 | 531 441 | 1.8188237 | 1.8188 | 0.8630 | 1.81884 |
| 14 | 1 594 323 | 1.8307723 | 1.8307 | 0.8724 | 1.83079 |
| 15 | 4 782 969 | 1.8419687 | 1.8419 | 0.8812 | 1.84198 |
| 16 | 14 348 907 | 1.8522346 | 1.8522 | 0.8892 | 1.85225 |
| 17 | 43 046 721 | 1.8616888 | 1.8616 | 0.8965 | 1.86170 |
| 18 | 129 140 163 | 1.8703250 | 1.8703 | 0.9033 | 1.87034 |
| 19 | 387 420 489 | 1.8783132 | 1.8783 | 0.9094 | 1.87833 |
| 20 | 1 162 261 467 | 1.8857083 | 1.8857 | 0.9151 | 1.88572 |
| 21 | 3 486 784 401 | 1.8925462 | 1.8925 | 0.9203 | 1.89256 |
| 22 | 10 460 353 203 | 1.8988933 | 1.8988 | 0.9251 | [TBD: 1.89891] |

The increments of γ per level fall from 0.0113 (k = 12) to 0.0048 (k = 22); the geometric fit of
γ_k = γ∞ − A r^k on k = 11 … 22 gives r = 0.919 and predicted γ_22 = 0.925 before the run. We do not read a limit
off such fits (§6).

## 4. Certificates

A feasibility certificate is the float32 vector c itself. With b = 23 − ⌊log₂ min c⌋ every C_i = c_i 2^b is an
exact integer; with λ = P/Q and D = 2^d we take q = ⌊D Q²/P²⌋ and L_j = ⌊D · ℓ_j⌋ where ℓ_j is a rigorous rational
lower bound for λ^{α−j} from interval arithmetic, and check C_m D ≤ q C_{4m} + L_j C̄ in int64 for every m, having
proved beforehand in exact integers that no intermediate can overflow. Since q/D ≤ λ^{−2} and L_j/D ≤ λ^{α−j},
C is feasible. Two programs do this check: `certify_fast.py` (bit operations, NumPy or Metal) and
`verify_cert.py` (float64 scaling, NumPy and mpmath only, no code shared with the search). The check takes
0.3 s at k = 16 and 4 min at k = 22; the certificates carry sha256 hashes of the vectors.

An infeasibility certificate is a positive vector C with F(C) < C strictly, with the coefficients rounded up
instead of down. For a monotone 1-homogeneous F this excludes any feasible d: with s = max d_i/C_i attained at
i*, d ≤ sC gives d_{i*} ≤ F(d)_{i*} ≤ sF(C)_{i*} < sC_{i*} = d_{i*}. The power-iterated vector at λ_k + 10^{−5}
serves directly; the resulting brackets are in the table. Negative controls (certificates with a modified entry,
a raised coefficient, or λ raised by 10^{−4}) are rejected by both verifiers.

## 5. Formal verification

Mazur's development (`collatz_predecessor_090`, ProofAtlas, July 2026) states and proves, for a weights
certificate W and a forced-potential certificate P on the level-k residue classes, that
x^{γ} ≤ π_a(x) eventually for all a ≢ 0 (mod 3). W is our vector rescaled to u32 with minimum 2^{20} (2^{19} at
k = 20) and the coefficients as dyadic lower bounds computed by exact integer root extraction in his
`kl_predecessor_common.py`; P depends only on k and we compute it as the least fixed point of his constraint
system (23–26 iterations), reproducing his k = 18 payload bit for bit. Both are embedded as hex chunks and
checked by `native_decide`; our `LoopCheck.lean` replaces his list-based checker by a tail-recursive loop
proved equivalent, which halves the memory.

| k | γ (p/q) | theorem | potential check | weights check | peak RSS | axioms |
|---|---|---|---|---|---|---|
| 18 | 9032/10000 | x^{903/1000} ≤ π_a(x) | 643 s | 871 s | 14 GB | 3 standard + 2 native_decide |
| 19 | 9093/10000 | x^{909/1000} ≤ π_a(x) | [TBD] | [TBD] | [TBD] | [TBD] |
| 20 | 9150/10000 | x^{915/1000} ≤ π_a(x) | [TBD] | [TBD] | [TBD] | [TBD] |

The vector must be re-tuned at the target λ = 2^{p/q} before export: a vector feasible at λ₁ is not
automatically feasible at λ₂ < λ₁ because λ^{α−1} decreases with λ. Mazur's own Python verifier passes on all
three exports (129 140 163, 387 420 489 and 1 162 261 467 rows). Two caveats on trust. `native_decide` puts the
Lean compiler in the trust base, and a July 2026 kernel soundness bug (fixed in Lean 4.32.2) was exposed by an
AI-assisted Collatz "disproof"; we therefore report `#print axioms` for every theorem and keep the two external
verifiers in the loop. And k = 21, 22 cannot be checked this way on 64 GB (estimated 90 and 270 GiB); a streamed
verified checker in the style of cake_lpr would remove that wall.

## 6. Towards exponent 1: what the data say

Summing the inequalities gives (1 − λ^{−2}) c̄_{k,k} ≤ (1/3)(λ^{α−1} + λ^{α−2}) c̄_{k−1,k}, with c̄_{k−1,k}/c̄_{k,k}
=: ρ_k the mean loss from the minimum over lifts; the inequality is tight on all our solutions (to 10^{−5}), so
λ_k is a function of ρ_k alone and λ_k → 2 ⇔ ρ_k → 1. We measure:

- 1 − ρ_k = 0.0573 (k = 11) … 0.0241 (k = 22), with successive ratios rising monotonically 0.913 → 0.933.
- At λ = 2 the exact identity r_k(F_2) = 1/4 + (3/4)ρ′_k holds (ρ′ the mixing ratio of the λ = 2 vector); 1 − r_k
  has ratios 0.905 (k = 12) → 0.924 (k = 22). Geometric-with-offset (limit 1 − r∞ = 0.0072, i.e. λ∞ < 2) and
  stretched-exponential (limit 0) fits both reach max residual 1.8·10^{−4} on k = 5 … 22; neither is excluded.
- A renormalisation argument (lift c_k to level k + 1, apply F, measure the injected top-digit sensitivity 3/4 s_k
  and its amplification A_k = 1.21 → 1.23) predicts that the ratios keep rising but level off near 0.94 because
  the argmins of the ×4 term and the auxiliary term over the top digit agree on exactly 1/3 of the classes at every k
  (as if independent); if so, 1 − ρ_k eventually decays geometrically and λ_k → 2. k = 22 is consistent (0.933,
  still rising ≈ 0.002 per level).
- The limit object is singular: C_max/C_min grows like 1.52^k, the mass in the top 1 % of classes rises, and the
  Hölder exponent of the digit profile is 0.04–0.09; the boundary layer at distance d from the top digit is
  universal, β(d) = 0.665, 0.401, 0.293, 0.232, 0.194 for every k.
- The spectrum of the linearisation at the Perron vector (dense to k = 9, Arnoldi to k = 15) has a second
  eigenvalue fixed at |λ₂| ≈ 0.865 for k = 8 … 15 with a ring of eigenvalues filling in at that radius
  (4 → 39 within 1 % of |λ₂| among the top 40), and the second eigenvector is delocalised across the 3-adic digits. The gap does not close;
  the k-dependence of the loss is therefore driven by the minimum (argmin switching), not by linear mixing.
- Calibration on 5x+1: the same construction (principal classes a ≡ 3 mod 5, four doublings, five lift cases) is
  validated by a residue-walking LP; λ_k(5) rises from 1.196 (k = 2) to 1.431 (k = 14), i.e. γ = 0.517 against a
  conjectured predecessor exponent η₅ ≈ 0.65 (Kontorovich–Lagarias), and its ratios of 1 − ρ_k rise 0.83 → 0.92,
  faster than for 3x+1. So a rising ratio is not by itself evidence for ρ_k → 1: 5x+1, where the exponent is
  believed to stay below 1, shows the same signature through k = 14.

Our reading: the data to k = 22 cannot decide between a limit exponent below 1 and a slow approach to 1; the
mechanism that would decide it is the alignment of the two argmins, which is a question about the minimum
structure of the limit inequality on Z₃ and is open.

## 7. What this does and does not establish

All of this is density. Even γ → 1 would exclude neither a non-trivial cycle (which by Hercher's work and Barina's
2^{71} verification must have at least 1.4·10^{11} odd terms) nor a divergent orbit, about which no tool says
anything. Conway's undecidability result for the general class of maps linear on residue classes means any proof
must use the specific arithmetic of 2 and 3; the Krasikov–Lagarias system does, but only through the branching
rule mod 3 and the size factors 2 and 3/2, which is why it yields density statements only.

## Data and code

Repository: github.com/dpalmqvist/kollatz (MIT). Certificates `certs/k{k}_{λ}/cert.json` with sha256 of the
vectors (the vectors themselves, 1 GB to 39 GB, are regenerated by the scripts in the README or available on
request); independent verifier `verify_cert.py`; Lean modules and manifests in `lean_formal/`; measurements in
`rho.py`, `holder.py`, `rF2_fit.py`, `renorm2.py`, `spectrum.py`, `kl5.py`. All vectors were produced twice (Apple
M5 24 GB and M4 Pro 64 GB) with identical λ to 7 decimals and certificates differing only in the float32 bits.

## References

- D. Applegate, J. C. Lagarias, Density bounds for the 3x+1 problem I, II, Math. Comp. 64 (1995) 411–426, 427–438.
- D. Barina, Improved verification limit for the convergence of the Collatz conjecture, J. Supercomput. 81:810 (2025).
- J. H. Conway, Unpredictable iterations, Proc. 1972 Number Theory Conf., Boulder, 49–52.
- C. Hercher, There are no Collatz m-cycles with m ≤ 91, J. Integer Seq. 26 (2023) 23.3.5; corrigendum 14 June 2026.
- A. V. Kontorovich, J. C. Lagarias, Stochastic models for the 3x+1 and 5x+1 problems, in The Ultimate Challenge, AMS 2010; arXiv:0910.1944.
- I. Krasikov, How many numbers satisfy the 3x+1 conjecture?, Internat. J. Math. Math. Sci. 12 (1989) 791–796.
- I. Krasikov, J. C. Lagarias, Bounds for the 3x+1 problem using difference inequalities, Acta Arith. 109 (2003) 237–258; arXiv:math/0205002.
- J. C. Lagarias, The 3x+1 problem: an overview, in The Ultimate Challenge, AMS 2010; arXiv:2111.02635.
- J. C. Lagarias, D. Weiss, The 3x+1 problem: two stochastic models, Ann. Appl. Probab. 2 (1992) 229–261.
- L. Mazur, Collatz predecessor 0.90 (Lean development), ProofAtlas, July 2026, commit 5f76a17.
- T. Tao, Almost all orbits of the Collatz map attain almost bounded values, Forum Math. Pi 10 (2022) e12; arXiv:1909.03562.
- G. J. Wirsching, The Dynamical System Generated by the 3n+1 Function, LNM 1681, Springer 1998.
- E. Yolcu, S. Aaronson, M. J. H. Heule, An automated approach to the Collatz conjecture, J. Automated Reasoning 67 (2023) 15; arXiv:2105.14697.
