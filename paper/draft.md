# Certified Krasikov–Lagarias predecessor bounds for the 3x+1 problem to k = 22: two-sided brackets, machine-checked instances, and the finite-level loss

*Draft 0.10, 2026-10-10. Daniel Palmqvist, with Claude (Anthropic). All numbers are taken from `RESULTS.md`,
`certs/*/cert.json`, `AVENUES.md`, `spectrum.json`, `kl5.json`, `syracuse_measure.json` and the literature survey
`reports/Collatz adjacent work and references.md`.*

## Abstract

For a positive integer a ≢ 0 (mod 3), let π_a(x) be the number of n ≤ x whose 3x+1 orbit passes through a.
Krasikov and Lagarias (Acta Arith. 109, 2003) proved π_a(x) ≥ x^{0.84} for x ≥ x₀(a) from a feasible point of a
linear program L^NT_k(λ) on the residue classes modulo 3^k, at k = 11. We carry the computation to k = 22, where
the program has 3^{21} ≈ 1.05·10^{10} principal variables, and obtain

  π_a(x) ≥ x^γ for every γ < 0.92509 and x ≥ x₀(a, γ).

Every level k = 12, …, 22 comes with an integer certificate, the float32 solution vector read as an exact integer
vector, verified in int64 arithmetic by two programs that share no code; the verification of the k = 22
certificate (39 GB) takes four minutes. For k = 2, …, 22 we also give infeasibility certificates, positive
vectors C with F(C) < C strictly for the right-hand side map F, which prove that the program at level k is
infeasible slightly above the certified λ; the Krasikov–Lagarias constants λ_k are thereby bracketed to widths
between 2·10^{−5} and 10^{−4}, confirming their numerical values to four or five decimals. The levels k = 18, 19 and
20 are machine-checked in Lean 4 inside L. Mazur's formalisation of the Krasikov–Lagarias argument, giving
theorems x^{0.903} ≤ π_a(x), x^{0.909} ≤ π_a(x) and x^{0.914} ≤ π_a(x) for large x, each resting on Lean's three
standard axioms and two compiled finite checks. We prove for every k that λ_k is attained, that every
solution at λ_k is unique up to scaling and has all inequalities tight, and that λ_k < λ_{k+1}. Strict increase is
stated as an open problem by Krasikov and Lagarias. The proof rests on the fact that m ↦ 4m is a single cycle on the
principal classes, and it is machine-checked in Lean. It also shows that L^NT_k extracts the optimal exponent from
Krasikov's inequalities. The question whether λ_k → 2, equivalent to
π_a(x) ≥ x^{1−ε} for every ε, reduces to whether a single number, the mean loss ρ_k from the minimum over three
lifts, tends to 1. We report ρ_k to k = 22, the spectral radius at λ = 2, and the spectrum of the linearised transfer
matrix, whose gap does not close with k. We then show that the finite-level loss is a mean-field quantity: replacing
the top-digit alignments fixed by the arithmetic of 2 and 3 by independent random ones above level 9 changes λ_15 by
2·10^{−3} and leaves the decay ratio of 1 − ρ_k unchanged, so the limit question can be posed for a random model
with no number theory above a fixed level. The decay ratio rises with k because the distribution of the ×4 weight
λ^{−2} c(4m)/c(m) broadens; that distribution converges with geometrically shrinking increments up to k = 21, which
heuristically gives geometric decay of the loss and λ_k → 2, although the ratio itself shows no deceleration yet.
The same construction on 5x+1 has the branching-walk exponent 0.6509 of Kontorovich–Lagarias as its ceiling and
poses the same question. The data to k = 22 are consistent with λ_k → 2 but do not establish it; we state what a
proof would need.

Two developments of 2026 frame these results.
- Mazur's formal proof of positive lower density, π_a(x) ≥ c_a x for every a ≢ 0 (mod 3) (Conjecture A of
  Applegate–Lagarias), supersedes every bound of the form x^γ for a fixed a. We re-checked that proof independently.
  Its constants are ineffective and not uniform in a.
- With the minimum replaced by the mean, the Perron vector of the λ = 2 operator is exactly the density of Tao's
  Syracuse random variable. Its level-to-level corrections do not shrink in L²: the diagonal contraction factor is
  exactly 1. So the question λ_k → 2 sits at a critical point. We propose this as the reason for the slow, drifting decay of 1 − ρ_k (§6.8).

The Krasikov–Lagarias bounds are uniform over residue classes and, at moderate k, fully explicit. Certified points of
bounded spread with a lifted base case give π_a(x) ≥ 0.7146 (x/a)^{0.848} for all x ≥ 2^{6.25} a, for every
a ≡ 2 (mod 3) not on a cycle, and an explicit envelope up to the k = 22 exponent (§4.4).

## 1. Introduction

The 3x+1 map is T(n) = n/2 for even n and (3n+1)/2 for odd n. The Collatz conjecture asserts that every orbit
reaches 1. The predecessor set of a is {n : T^j(n) = a for some j ≥ 0}; its counting function π_a(x) measures how
much of [1, x] lies in the tree below a, and the conjecture is equivalent to π_1(x) = ⌊x⌋.

Lower bounds of the form π_a(x) ≥ x^γ have a forty-year history. Crandall (1978) showed some γ > 0 exists; Sander
(1990) reached 3/10; Krasikov (1989) introduced difference inequalities on residue classes modulo 3^k and obtained
3/7; Wirsching (1993) 0.48; Applegate and Lagarias (1995) 0.65 by exhaustive tree search to depth 30 and 0.809 by
a nonlinear program on about 20 000 variables; and Krasikov and Lagarias (2003) 0.84, from a linear program
with 3^{10} principal variables. Lagarias's 2010 overview lists 0.84 as the record and states as open that
π_1(x) > c(ε) x^{1−ε} for every ε > 0. Krasikov and Lagarias observe in their §6 that their constants λ_k satisfy
λ_k ≤ λ_{k+1} and that λ_k → 2 would give the x^{1−ε} bound; no progress on that had appeared before 2026.

Three things changed between 2003 and 2026, and this paper uses all three.

*Memory.* The level-k program has N = 3^{k−1} principal variables and a right-hand side map that needs no stored
index arrays: all index maps are affine in the residue. A float32 vector at k = 22 is 39 GB, which a single
workstation with unified memory holds, and the map evaluates in seconds on its GPU.

*Certification.* A solution found in floating point is turned into an integer certificate and checked in exact
integer arithmetic; the mathematics of the bound is the Krasikov–Lagarias theorem, and the computation reduces to a
check that anyone can re-run in minutes. We add the reverse certificate: because the right-hand side map is
monotone and 1-homogeneous, a vector with F(C) < C strictly proves infeasibility, so λ_k becomes a two-sided
number.

*Formalisation.* Mazur's 2026 Lean 4 development replaces the analytic step of Krasikov–Lagarias (their Theorem 2.2)
by a second finite certificate, an "adaptive forced potential" on the same residue classes, and checks both
certificates by compiled evaluation (`native_decide`), so that the statement for a given k is a Lean theorem.
We feed our certificates through that development for k = 18, 19 and 20.

*Positive density.* In September 2026 Mazur released a Lean formalisation of positive lower density:
π_a(x) ≥ c_a x for every a ≢ 0 (mod 3) and all large x. This is Conjecture A of Applegate and Lagarias, and in
particular it answers the x^{1−ε} question for each fixed a. The method differs from ours: a weighted backward-tree
mass from one seed, with an explicit-constant form of Tao's fine-scale mixing as the analytic input (see §6.8 for how
that mixing relates to the present system). We rebuilt it from source and replayed every module through Lean's own
kernel and through the independent kernel nanoda. The statement is faithful, and the axioms are the standard three.
The work is not refereed.

For a fixed a it supersedes every bound of the form x^γ, including those of this paper. What it does not give is
uniformity and explicitness. Its constant c_a is ineffective for general a, while a feasible point of L^NT_k bounds
π_a for all a in a residue class at once, with a computable constant. This paper therefore addresses three questions:
- explicit uniform bounds (§4.4);
- the exact structure and capacity of the method (Theorem 1 and §6);
- certified computation at scale (§§3–5).

Related work, 2024–2026. Several AI-assisted Lean projects pursue the same program; none is refereed. msharpe248
obtains π_1(x) = Ω(x^{0.8676}) at k = 14 with a kernel-checked certificate (29 h, 37 GB) and 0.895 at k = 17
informally; Mazur obtains 0.90 and 0.901 at k = 18 via `native_decide`; Menta2357 reproduces the k = 11 value
0.8418 kernel-clean. At equal k these agree with ours to the precision of their respective roundings
(msharpe248's values are lower at equal k because of an integer-grid weakening of the weights). On the cycle side,
Barina's verification of convergence for all n < 2^{71} (2025) makes Hercher's conditional result unconditional:
a nontrivial cycle has at least 1.375·10^{11} odd terms. Our survey of the primary sources, with provenance for
every number, is in the repository.

## 2. The Krasikov–Lagarias system

### 2.1 Difference inequalities

Fix k ≥ 2. A residue class m mod 3^k with m ≡ 2 (mod 3) is *principal*: its members have two predecessors under
T, the even predecessor 2m and the odd predecessor (2m − 1)/3. Classes ≡ 1 (mod 3) have only the even predecessor,
and classes ≡ 0 (mod 3) have only the chain {2^j m}, which contributes O(log x) to any count and is dropped.
Writing φ_m(y) for the infimum over a in class m of the number of predecessors of a not exceeding 2^y a, the tree
structure gives φ_m(y) ≥ φ_{2m}(y − 1) + φ_{(2m−1)/3}(y − 1 + α) with α = log₂ 3, and eliminating the
non-principal classes yields, for each principal m,

- m ≡ 2 (mod 9): φ_m(y) ≥ φ_{4m}(y − 2) + φ̄_{(4m−2)/3}(y + α − 2),
- m ≡ 5 (mod 9): φ_m(y) ≥ φ_{4m}(y − 2),
- m ≡ 8 (mod 9): φ_m(y) ≥ φ_{4m}(y − 2) + φ̄_{(2m−1)/3}(y + α − 1),

where φ̄_r is the infimum over the three classes mod 3^k lying above the class r mod 3^{k−1}, because the odd
predecessor is known only modulo 3^{k−1}. (The paper's equations (2.13)–(2.14) print 3^k where 3^{k−1} is meant;
the reproduction of their Table 2 to seven decimals, §3.3, confirms the correction.)

### 2.2 The linear program and its map

The ansatz φ_m(y) ≥ c_m λ^y turns the inequalities into the linear system L^NT_k(λ): for principal m,

- m ≡ 2 (mod 9): c_m ≤ λ^{−2} c_{4m} + λ^{α−2} c̄_{(4m−2)/3},
- m ≡ 5 (mod 9): c_m ≤ λ^{−2} c_{4m},
- m ≡ 8 (mod 9): c_m ≤ λ^{−2} c_{4m} + λ^{α−1} c̄_{(2m−1)/3},
- c_m ≥ 1, with c̄_r = min(c_r, c_{r+3^{k−1}}, c_{r+2·3^{k−1}}).

**Theorem (Krasikov–Lagarias, Thm 2.2 and §6).** If L^NT_k(λ) is feasible then for every a ≢ 0 (mod 3) and every
γ < log₂ λ there is x₀(a, γ) with π_a(x) ≥ x^γ for x ≥ x₀. The constant is explicit: φ_m(y) ≥ Δ₁ c_m λ^y with
Δ₁ = 1/(4 max_m c_m).

Let F_λ be the right-hand side map, F(c)_m = λ^{−2} c_{4m} + λ^{α−j} c̄_{r(m)}. F is monotone and positively
1-homogeneous on the positive cone, so it has a cone spectral radius r(F_λ) (Collatz–Wielandt), and L^NT_k(λ) is
feasible iff r(F_λ) ≥ 1: a feasible c satisfies c ≤ F(c), which forces r ≥ 1, and conversely an eigenvector with
F(c) = rc, r ≥ 1, is feasible after scaling. We define λ_k := sup{λ ∈ [1, 2] : L^NT_k(λ) feasible}, where [1, 2]
is the range of the theorem above. Numerically r(F_λ) is decreasing on [1, 2] (checked on a grid for k ≤ 7), which
would make λ_k the unique root of log r(F_λ) = 0 there, but we do not need or prove this.

### 2.3 Indexing

With N = 3^{k−1} and index i ∈ [0, N) for m = 3i + 2, every map is affine: 4m ↦ (4i + 2) mod N; the class of m
mod 9 is i mod 3 (0 ↔ 2, 1 ↔ 5, 2 ↔ 8); the auxiliary index is 4j mod N/3 for i = 3j and (2j + 1) mod N/3 for
i = 3j + 2; and c̄[r] = min(c[r], c[r + N/3], c[r + 2N/3]). The ternary digits of i are the digits of m above the
lowest, and the top digit is the one the minimum ranges over. Lifting a level-(k−1) vector to level k is
c_k[i + j N_{k−1}] = c_{k−1}[i], which preserves feasibility (this is the monotonicity λ_k ≤ λ_{k+1}).

### 2.4 Structure of L^NT_k: attainment, tightness, strict increase

Krasikov and Lagarias leave three questions about L^NT_k open:
- in their §6, *"It remains an open problem to show that the values λ_k are strictly increasing in k"*;
- whether (1) the supremum λ_k is attained and (2) at λ_k some solution has all principal inequalities tight,
  which they consider *"likely … but this may be difficult to prove"*;
- whether L^NT_k extracts the best exponential bound from I_k, which they believe "although we have no proof".

Applegate–Lagarias (Density bounds II, 1995, §4) had called strict increase easy. Their sketch shows that the lifted solution has a
strict inequality somewhere, but for a parametric linear program that alone does not allow λ to increase.

**Theorem 1.** For every k ≥ 2:
(i) λ_k is attained, and 1 < λ_k < 2;
(ii) every feasible point at λ_k satisfies all principal inequalities with equality, and it is unique up to a
positive factor;
(iii) λ_k < λ_{k+1}.
Consequently c_m λ_k^y solves Krasikov's system I_k with equality, so no exponential rate above λ_k can be derived
from I_k, and every linear program obtained from I_k by the splitting and truncation of Applegate–Lagarias has λ* ≤ λ_k
(their Conjecture 4.1).

The proof rests on one arithmetic fact and some elementary nonlinear Perron–Frobenius theory:

- *The arithmetic fact.* m ↦ 4m permutes the principal classes as a single cycle of length 3^{k−1}, because 4 has
  order 3^{k−1} modulo 3^k. Every principal inequality contains λ^{−2} c_{4m} with no minimum.
- *Slack spreads.* If c > 0, F(c) ≥ c and F(c) ≠ c, the set of rows with F^n(c) > c grows by one ×4-preimage per
  iteration, so F^N(c) > c everywhere. Superadditivity of F (a minimum of linear forms) then makes
  z = Σ_{n<N} F^n(c) strictly sub-invariant, F(z) > z.
- *Openness.* By continuity in λ, a strictly sub-invariant z stays feasible slightly above the current λ.
- *Tightness.* Applied at the supremum, this rules out slack, which gives (ii).
- *Attainment and λ_k < 2.* Attainment follows from compactness of the normalised feasible sets; zeros of a limit
  vector are removed by the same propagation. Summing all inequalities at λ = 2 forces both tightness and top-digit
  invariance. The descent argument of Applegate–Lagarias then shows a tight top-digit-invariant vector is constant, which the
  m ≡ 5 rows exclude.
- *Strict increase.* The tiled vector tile(c_k) gains slack exactly where c_k varies over its top digit. That is
  somewhere, by the same descent, so (iii) follows from the spreading step.

Uniqueness: zeros of c′ − t c propagate forwards along the cycle.

The complete argument is in `notes/strict_monotonicity.md`. It is formalised in Lean 4 with Mathlib
(`lean_formal/KLMonotone/`, about 1340 lines, no certificates, only the three standard axioms). The formalisation
includes the equivalence with the program exactly as printed in Krasikov–Lagarias (2.7)–(2.14) and the residue form
of all index maps. A corollary gives the loss of §6.1 in closed form, ρ_k = 3(λ_k − 1)/λ_k^α, and shows that
1 − ρ_k is strictly decreasing.

The development builds standalone and passes `leanchecker`. It was also replayed in the independent kernel nanoda:
29 202 declarations on Lean v4.30, and 30 006 declarations, Mathlib included, after a port to v4.35. The v4.35
toolchain postdates the fix of kernel bug #14576 (§5.4).

The theorem gives no rate. The slack travels with factor λ^{−2} per step along the ×4 cycle, so the increment it
certifies is exponentially small in k. A uniform version, λ_{k+1} − λ_k ≥ κ(2 − λ_k), is equivalent to geometric
convergence λ_k → 2 and is the open problem of §6.

## 3. Computation

### 3.1 Power iteration and secant search

We compute λ_k by a secant method on λ ↦ log r(F_λ), with r estimated as the midpoint of the Collatz–Wielandt
bounds min_i F(c)_i/c_i ≤ r ≤ max_i F(c)_i/c_i after power iteration c ← F(c)/min F(c). Each λ evaluation is
warm-started from the previous iterate, and each level from the lifted solution of the level below; three to five
λ values suffice. The secant stops when its step falls below the noise level (hi − lo)/(2|slope|), which is where
float32 stops determining λ_k; the slope d log r/dλ ≈ −0.27 means a gap of 10^{−6} in r leaves λ undetermined
to about 4·10^{−6}. Certified λ values are rounded down to four decimals, well inside the noise.

### 3.2 Memory

F is one Metal kernel (Apple MLX): each thread computes its indices in 64-bit integers, reads three lifts and one
quadruple index, and writes one output; no index arrays exist. The normalisation 1/min c is folded into the
coefficients (F is 1-homogeneous), so the iteration holds two vectors. The Collatz–Wielandt bounds are computed in
chunks. For k ≥ 21 the vector exceeds 2^{31} entries and is stored with shape (3, N/3) because MLX shapes are
32-bit.

When two vectors do not fit (k = 21 on 24 GB, k = 22 on 64 GB) the update is compressed: a kernel computes
ρ_i = F(c)_i/c_i exactly in float32 together with per-threadgroup minima and maxima, stores
d_i = round((ρ_i − ρ₀)/S) as int8 with ρ₀ and S from the previous iteration's bounds (S = 1.25(hi − lo)/254), and
the update c ← (c/m)(ρ₀ + S d) reuses c's buffer. The quantisation perturbs the iterate by at most S/2, which is
irrelevant because certification checks the final vector exactly; it raises the floor of hi − lo to about
2·10^{−6}. Peak memory is 1.26 vectors.

At k = 22 the vector (39.0 GB) exceeds Metal's single-buffer limit (38.9 GiB on the M4 Pro). We hold it as three
buffers indexed by the top ternary digit, c[i] = c_j[i − j N/3]; the lift minimum becomes min(c₀[r], c₁[r], c₂[r])
and the warm start from level 21 is three copies of that vector. The split kernel agrees with the single-buffer
kernel bit for bit at k ≤ 10.

### 3.3 Results

| k | N = 3^{k−1} | λ_k (numerical) | λ_cert | γ_cert = log₂ λ_cert | Δγ | λ_upper (infeasible) |
|---|---|---|---|---|---|---|
| 2–11 | 3 … 59 049 | Table 2 of K–L reproduced to 10^{−6} … 10^{−7} | – | 0.8418 at k = 11 | – | 1.35342 … 1.79225 |
| 12 | 177 147 | 1.8064236 | 1.8064 | 0.8531 | 0.0113 | 1.80644 |
| 13 | 531 441 | 1.8188237 | 1.8188 | 0.8630 | 0.0099 | 1.81884 |
| 14 | 1 594 323 | 1.8307723 | 1.8307 | 0.8724 | 0.0094 | 1.83079 |
| 15 | 4 782 969 | 1.8419687 | 1.8419 | 0.8812 | 0.0088 | 1.84198 |
| 16 | 14 348 907 | 1.8522346 | 1.8522 | 0.8892 | 0.0080 | 1.85225 |
| 17 | 43 046 721 | 1.8616888 | 1.8616 | 0.8965 | 0.0073 | 1.86170 |
| 18 | 129 140 163 | 1.8703250 | 1.8703 | 0.9033 | 0.0068 | 1.87034 |
| 19 | 387 420 489 | 1.8783132 | 1.8783 | 0.9094 | 0.0061 | 1.87833 |
| 20 | 1 162 261 467 | 1.8857083 | 1.8857 | 0.9151 | 0.0057 | 1.88572 |
| 21 | 3 486 784 401 | 1.8925462 | 1.8925 | 0.9203 | 0.0052 | 1.89256 |
| 22 | 10 460 353 203 | 1.8988933 | 1.8988 | 0.9251 | 0.0048 | 1.89891 |

An independent implementation (HiGHS on the explicit LP, constraints written out from residues in exact integers,
no code shared with the search) reproduces λ_k to 10^{−6} for k ≤ 9, and its LP solutions at λ_k − 2·10^{−6}
verify exactly in rational arithmetic. Timings on an Apple M4 Pro (64 GB): k = 19, 40 s; k = 20, 151 s; k = 21,
382 s; k = 22, 110 min for three λ evaluations at 49.0 GiB peak, plus 39 min to re-tune at λ_cert. All vectors were
produced on two machines (M5 24 GB, M4 Pro 64 GB) with λ_k agreeing to seven decimals.

The increments Δγ fall from 0.0113 to 0.0048 with successive ratios near 0.92. A geometric fit γ_k ≈ γ∞ − A r^k on
k = 11 … 22 gives r = 0.919 and γ∞ ≈ 0.980 with maximal residual 2·10^{−4}, and predicted both γ_21 and γ_22 blind
to within 10^{−4}. We do not read a limit off it: the ratios drift upward, and models with limits 0.97 and 1 fit
the same data equally well (§6).

## 4. Certificates

### 4.1 Feasibility certificates

Let c be the float32 vector after power iteration at λ = P/Q. With b = 23 − ⌊log₂ min c⌋, every C_i = c_i 2^b is
an exact integer for every positive normal float32 c_i ≥ min c. Choose D = 2^d with d such that max C · D < 2^{63}
and max C · (q + max L_j) < 2^{63}, proved in Python integers before the check; set q = ⌊D Q²/P²⌋ and
L_j = ⌊D ℓ_j⌋ where ℓ_j is a rigorous rational lower bound for λ^{α−j} from mpmath interval arithmetic at 200
bits. Then check, for every i, in int64,

  C_i D ≤ q C_{(4i+2) mod N} + L_j C̄_{r(i)}.

Since q/D ≤ λ^{−2}, L_j/D ≤ λ^{α−j} and all quantities are nonnegative, the inequality implies
C_i ≤ λ^{−2} C_{4m} + λ^{α−j} C̄, so C is feasible for L^NT_k(λ) (C ≥ 1 by homogeneity). No rounding occurs
anywhere; the only floating-point object is the input vector, whose bits define C.

Two programs perform this check. `certify_fast.py` forms C by bit operations (mantissa shifted by the exponent)
and streams over chunks in NumPy or on the GPU in int64 (MLX int64 was verified bitwise against NumPy).
`verify_cert.py` uses only NumPy and mpmath, forms C as float64(c)·2^b followed by an exact integrality check,
recomputes the interval bounds, re-derives the overflow conditions, and checks the sha256 of the vector against
the certificate's metadata. A `--exact` mode re-checks the same integers with Python integers for small k. The
certificates are rejected when tampered with (an altered entry, q + 1, L + 1, λ raised by 10^{−4}). The check at
k = 22 takes 290 s and 4 min respectively.

### 4.2 Infeasibility certificates

**Lemma.** Let F be monotone and positively 1-homogeneous on the positive cone of R^N and let C > 0 satisfy
F(C)_i < C_i for every i. Then no d ≥ 1 satisfies d ≤ F(d).

*Proof.* Suppose d ≥ 1 with d ≤ F(d). Let s = max_i d_i/C_i, attained at i*. Then d ≤ sC, so by monotonicity and
homogeneity d_{i*} ≤ F(d)_{i*} ≤ s F(C)_{i*} < s C_{i*} = d_{i*}, a contradiction. ∎

An infeasibility certificate is therefore a vector C with the coefficients rounded the other way:
q = ⌈D Q²/P²⌉, L_j = ⌈D u_j⌉ with u_j a rigorous rational upper bound for λ^{α−j}, and the strict reverse
inequality q C_{4m} + L_j C̄ < D C_i checked in int64 for every i. The power-iterated vector at λ_k + 10^{−5}
serves directly (its maximal ratio is about 1 − 3·10^{−6}); at k = 3 the float32 rounding floor of the ratio gap
(≈ 3·10^{−5} at N = 9) required λ_k + 2·10^{−4}, and at k = 22 the int8 path's floor required λ_k + 2·10^{−5}
(1.89891; slack 1.6·10^{−6}, 2252 s to re-tune and 293 s to check). The two certificates bracket λ_k:

| k | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|
| width of [λ_cert, λ_upper] | 2e-5 | 3e-4 | 1e-4 | 7e-5 | 7e-5 | 1e-4 | 8e-5 | 5e-5 | 4e-5 | 5e-5 |

| k | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| width | 4e-5 | 4e-5 | 9e-5 | 8e-5 | 5e-5 | 1e-4 | 4e-5 | 3e-5 | 2e-5 | 6e-5 | 1e-4 |

The brackets confirm the published Table 2 of Krasikov–Lagarias at k = 2 … 11 and show that at level k the method
provably cannot give γ ≥ log₂ λ_upper; at k = 22, γ_22 ∈ [0.92509, 0.92517]. The same reverse check verifies in `verify_cert.py` (format `/2-upper`).

### 4.3 Certificate metadata

Each `cert.json` records k, N, λ = P/Q, D, q, L₂, L₁, b, the sha256 of the vector data and of the file, the minimum
relative slack, the software versions and the claim; the vectors (1 GB at k = 18 to 39 GB at k = 22) are
regenerated by the scripts or available on request. Minimal relative slacks are 6.7·10^{−6} (k = 18), 3.1·10^{−6}
(19), 1.4·10^{−6} (20), 1.1·10^{−5} (21), 2.4·10^{−5} (22); slack of order 10^{−7} is the float32 limit, so k ≥ 23
would need float64 polishing or a λ_cert further below λ_k.

### 4.4 Explicit bounds valid for all x

Theorem 2.2 of Krasikov–Lagarias holds for every y ≥ 0, not only asymptotically. A feasible point with 1 ≤ c ≤ t at
level k and parameter λ gives φ_m(y) ≥ c_m λ^y/(4t). Hence, with no threshold,

  π_a(x) ≥ (x/a)^{log₂ λ}/(4t)   for all x ≥ a and every a ≢ 0 (mod 3) not on a cycle.

The Perron vectors of §3 have spread ≈ 1.52^k, which makes this constant useless at large k. But Krasikov and
Lagarias's own linear program (their (2.7)) minimises the spread. The minimal spread t*(k, λ) is non-increasing in k
(lifting) and converges at fixed λ, whereas the Perron spread does not:

| k \ λ | 1.60 | 1.65 | 1.70 | 1.75 | 1.78 | 1.80 |
|---|---|---|---|---|---|---|
| 9 | 4.448 | – | 7.752 | – | – | – |
| 11 | 4.448 | 5.551 | 7.613 | 11.707 | 18.193 | – |
| 13 | 4.448 | 5.543 | 7.580 | 11.157 | 15.416 | 20.883 |
| 14 | 4.448 | 5.542 | 7.571 | 11.017 | 15.000 | 19.347 |
| 16 | 4.448 | 5.539 | 7.556 | 10.850 | 14.547 | 18.164 |

At λ = 1.80 the Perron spread is 1594 at k = 16. The values were computed by an LP (HiGHS) for k ≤ 9 and by the
monotone iteration c ← min(t, F(c)) with bisection on t to k = 16. The two agree to four decimals. Extrapolating
the decrements gives t*_∞ ≈ 4.45, 5.54, 7.55, 10.7, 14.3, 17.6 for λ = 1.60 … 1.80. This fits C(2 − λ)^{−a} with
a = 2.0–2.1, though the local exponents drift slightly upward.

The constant 1/(4t) improves by a factor of 40–60 if the Krasikov–Lagarias induction (their Theorem 5.1) is started
at a higher base window [Y − 2, Y]. In that window φ_m(y) is bounded below by exactly enumerating each class's
*guaranteed* predecessor tree: 2n always, and (2n − 1)/3 when n ≡ 2 (mod 3), which is decidable for ≤ k odd steps.
The base constant is

  Δ = min over grid cells [y_i, y_{i+1}] of L(y_i)/(c λ^{y_{i+1}}).

Here the counts L(y) are exact integers. The float64 path heights stay at least 2.5·10^{−5} from every grid point, so
no node is misplaced. Certified bounded-spread points are checked like §4.1 and by `verify_cert.py`. With them, for
a ≡ 2 (mod 3) not on a cycle:

| range of x/a | bound | certificate |
|---|---|---|
| 2^{6.25} … 2^{15.7} | 0.7146 (x/a)^{0.8480} | k = 14, λ = 1.80, spread 19.35 |
| 2^{15.7} … 2^{18.3} | 0.5514 (x/a)^{0.8718} | k = 16, λ = 1.83, spread 29.49 |
| 2^{18.3} … 2^{335} | 0.4987 (x/a)^{0.8797} | k = 17, λ = 1.84, spread 33.84 |
| ≥ 2^{335} | (x/a)^{0.92509}·C_min/(4λC_max), C_max/C_min = 9840.7 | k = 22 Perron certificate |

Each lifted bound holds for all x ≥ 2^{6.25} a. For a ≡ 1 (mod 3) use π_a ≥ π_{2a}: divide the constant by λ and
require x ≥ 2^{7.25} a. The lifting costs are:
- k = 14: 1.6·10^6 trees, 4·10^9 nodes, 3 min;
- k = 17: 1.7·10^{11} nodes, 2.4 h, on one core.

An earlier value of 0.865 for k = 8 took the minimum only at grid points; the rigorous value is 0.8435. Mazur's
positive-density constants are ineffective for general a, so these are the best lower bounds for π_a(x) that can be
written down at any height. If t*_∞(λ) ∝ (2 − λ)^{−2} continued to λ = 2, which is unproved, it would give
π_a(x) ≫ x/(log x)², uniformly in a.

## 5. Formal verification

### 5.1 Mazur's development

The Lean development `collatz_predecessor_090` (ProofAtlas, July 2026; Lean v4.30.0-rc2, Mathlib pinned) proves,
for a weights certificate W: [N) → u32 and a forced-potential certificate P: [N) → u8 on the level-k principal
classes, the statement

  ∀ a > 0, a ≢ 0 (mod 3): x^{γ} ≤ π_a(x) for all sufficiently large real x,

with γ = p/q given and λ = 2^{p/q}. W must satisfy scale · W_i ≤ A · W_{4i} + B_j · min(lifts) for all i, with
scale = 2^{28} and A, B_j dyadic lower bounds for λ^{−2}, λ^{α−2}, λ^{α−1} computed by exact integer root extraction
(his `kl_predecessor_common.py`); this is our row check with the same index formulas. P must satisfy
P[4i + 2] ≤ P[i] + 6, min over lifts of P at the D1 auxiliary index ≤ P[3q] + 1, and min over lifts at the D3
auxiliary index ≤ P[3q + 2] − 2; this replaces the Kőnig-type elimination in Krasikov–Lagarias's Theorem 2.2 by a
finite object (his `AdaptiveCriticalChoice.exponential_lower_bound`). P depends on k only. Both certificates are
embedded as hexadecimal chunks of 32 MiB (`include_str`) and checked by `native_decide`.

### 5.2 Our additions

- The weights are our vector rescaled to u32 with minimum 2^{20} (2^{19} at k = 20, where C_max/C_min = 4231
  would overflow 32 bits at 2^{20}; the row check is scale-invariant). Before export the vector is re-tuned at the
  target λ = 2^{p/q} by power iteration, because a vector feasible at λ₁ is not automatically feasible at
  λ₂ < λ₁: λ^{α−1} decreases with λ and the m ≡ 8 (mod 9) rows can fail (our k = 18 vector at 1.8703 failed 34.8
  million rows at 2^{0.903}).
- The potential is computed as the least fixed point of the constraint system by chunked NumPy (23–26 iterations,
  15 s at k = 18 to 4 min at k = 20); it reproduces Mazur's k = 18 payload bit for bit (sha256 778584ce…).
- `LoopCheck.lean` replaces his list-based checker by a tail-recursive loop, proved equivalent to his `Valid`,
  which removes a `List.range N` (16 B per class) from the peak and makes k = 19 and 20 feasible on 64 GB.
- The level-specific modules K18, K19, K20 (principal index, power-of-two targets, source bridge, coefficient
  bridge, critical choice, predecessor bridge, all-targets) are generated from his K18 files by textual
  substitution; the generated certificate modules embed no hashes, only the chunk list, so a regenerated vector
  needs no Lean changes.
- Two facts about large `.olean` files mattered at k = 20 (9.3 GB weights, 2.3 GB potential). Lean maps each
  olean at a base address derived from a hash of the module name and, if that range is taken, falls back to a
  single `read()` that fails above 2 GiB on macOS. So the 9.3 GB module is imported first in every dependent
  module, and the potential module was renamed (`Generated.K20Potential10`) because the original name's range
  contained `Mathlib.Algebra.Field.Defs`; the base address of a candidate name can be predicted from the hash
  and checked against all existing oleans before building. The 139-chunk array also needs a higher `simp`
  recursion limit.

### 5.3 Results

| k | γ = p/q | Lean theorem | potential check | weights check | peak RSS | axioms |
|---|---|---|---|---|---|---|
| 18 | 9032/10000 | x^{903/1000} ≤ π_a(x) (`CollatzPredecessor0903`) | 643 s | 871 s | 14.0 GB | 3 standard + 2 `native_decide` |
| 19 | 9093/10000 | x^{909/1000} ≤ π_a(x) (`CollatzPredecessor0909`) | 2113 s | 2554 s | 24.4 GB | 3 standard + 2 `native_decide` |
| 20 | 9150/10000 | x^{914/1000} ≤ π_a(x) (`CollatzPredecessor0914`) | 5940 s | 7382 s | 55.9 GB | 3 standard + 2 `native_decide` |

Each level also yields the constant-free forms `_nat` (natural cutoffs) and `_0903x` (c · x^{p/q} with the full
certificate exponent). The publication exponent must be strictly below the certificate exponent for the
constant to be absorbed (0.903 < 0.9032, 0.909 < 0.9093); at k = 20 the natural choice 915/1000 equals 9150/10000, so
the unit-coefficient theorem is stated at 914/1000 and the constant form keeps 9150/10000. `#print axioms` lists propext, Classical.choice, Quot.sound and the two named `native_decide`
axioms per level, the same trust base as Mazur's 0.90. Mazur's own Python verifier passes on the three exports
(129 140 163, 387 420 489 and 1 162 261 467 rows, zero failures), and his potential verifier passes on the k = 19
and k = 20 potentials (645 700 815 and 1 937 102 445 inequalities).

### 5.4 Trust

`native_decide` places the Lean compiler in the trust base. A kernel soundness bug (Lean issue #14576, July 2026,
fixed in 4.32.2) was exposed by an AI-assisted "disproof" of the Collatz conjecture; we therefore report the axiom
audit of every theorem, keep both external verifiers in the loop, and recommend re-running the builds on a
toolchain at or above 4.32.2. Theorem 1 (§2.4) is not affected: it uses no `native_decide`, and it was replayed by
nanoda on v4.35. The memory of `native_decide` scales linearly with N (about 8–24 bytes per class),
so k = 21 and 22 (estimated 90 and 270 GiB) are out of reach of this route on 64 GB; a streamed verified checker
in the style of cake_lpr or lrat-catcher, proved once and run natively in constant memory, is the natural next
step and would also move the compiled code out of the trust base of each individual certificate.

## 6. The finite-level loss and the question λ_k → 2

### 6.1 One number

Summing the inequalities over all principal classes, and using that m ↦ 4m is a bijection of the principal classes
and that each auxiliary map is a bijection from a third of them onto the auxiliary classes, gives

  (1 − λ^{−2}) c̄_{k,k} ≤ (1/3)(λ^{α−1} + λ^{α−2}) c̄_{k−1,k},

with c̄_{k,k} the mean of c and c̄_{k−1,k} the mean of c̄. Write ρ_k = c̄_{k−1,k}/c̄_{k,k} ≤ 1 for the mean loss from the
minimum over lifts. At λ = 2 both sides equal 3/4 when ρ = 1, so λ_k → 2 ⇔ ρ_k → 1. By Theorem 1 (§2.4) the unique
solution at λ_k satisfies every inequality with equality, so the summed inequality is an identity there, and λ_k is
exactly a function of ρ_k (the mean loss of that solution): 1 − λ_k^{−2} = (1/3)(λ_k^{α−1} + λ_k^{α−2}) ρ_k. On our
certified solutions at λ_cert < λ_k the summed inequality holds with a gap of order 10^{−5}.

| k | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 − ρ_k | 0.0573 | 0.0524 | 0.0482 | 0.0443 | 0.0407 | 0.0375 | 0.0347 | 0.0321 | 0.0298 | 0.0277 | 0.0258 | 0.0241 |
| ratio | 0.913 | 0.913 | 0.920 | 0.919 | 0.920 | 0.922 | 0.924 | 0.927 | 0.928 | 0.930 | 0.931 | 0.933 |

The ratio rises monotonically, so 1 − ρ_k is not geometric. Geometric-with-offset (limit ρ∞ = 0.991, γ∞ ≈ 0.971),
stretched-exponential (ρ∞ = 1) and power-law (ρ∞ = 1) models fit k = 11 … 22 with the same maximal residual
≈ 10^{−4}. The data cannot decide.

### 6.2 The λ = 2 operator

At λ = 2 the same map F₂ has spectral radius r_k < 1, non-decreasing in k with limit r∞ ≤ 1, and λ_k → 2 ⇔ r∞ = 1.
The exact identity r_k = 1/4 + (3/4)ρ′_k holds, where ρ′_k is the mixing ratio of the λ = 2 Perron vector itself
(checked to 7 decimals at every k up to 22). The sequence 1 − r_k for k = 5 … 22 shrinks by ratios rising from 0.86
to 0.924; at k = 22, r_22 = 0.974971 and ρ′_22 = 0.966628. Geometric-with-offset (limit 1 − r∞ = 0.0072) and
stretched-exponential (limit 0) fits reach maximal residual 1.8·10^{−4} on k = 5 … 22; fitted on k ≤ 16 the offset
model misses k = 22 by −4.3·10^{−4} and the stretched model by −7.5·10^{−4}, pure geometric by −1.5·10^{−3}.

### 6.3 A renormalisation reading and a prediction

Lift the level-k solution to level k + 1 (its top-digit sensitivity is then 0) and apply F once: the injected
top-digit sensitivity is exactly (3/4)s_k at λ = 2, because the mean is preserved and only the auxiliary term,
whose mass fraction is 3/4, selects lifts by the new digit. Iterating to the fixed point amplifies it by
A_k = s_{k+1}/((3/4)s_k) = 1.20 → 1.23 for k = 8 … 21, and the per-level ratio of 1 − r_k is (3/4)A_k. Hence
λ_k → 2 iff A∞ < 4/3. The amplification comes from the ×4 term recirculating top-digit variation with weight 1/4;
if a fraction e of that variation survives the minimum, A = 1/(1 − e/4). Writing the fixed point as c = P + Q with
P the ×4 term (mass fraction 0.275 → 0.262, tending to 1/4) and Q the auxiliary term, the surviving fraction is
e_k = 0.614, 0.666, 0.692, 0.705, 0.715, 0.724, 0.731, 0.737, 0.742, 0.746 for k = 8 … 17, with shrinking
increments; and the argmins of P and Q over the top digit agree on 0.332–0.333 of the classes at every k, exactly
as if independent. If e∞ ≈ 0.78–0.80 the per-level ratio saturates near (3/4)/(1 − e∞/4) ≈ 0.935–0.94, and
1 − r_k eventually decays geometrically: λ_k → 2.

The prediction is therefore that the ratios keep rising but level off near 0.94 rather than approaching 1. k = 22
gives 0.924, still rising by about 0.002 per level, consistent and not decisive; at the current rate 0.94 would be
reached near k = 31. What a proof would need is that the two argmins stay independent and the two variations stay
comparable in the limit measure.

### 6.4 The limit object

The total variation between the level-j marginals of the normalised solutions at consecutive k decays
geometrically (ratio ≈ 0.92), so a limit measure on Z₃ exists. It is not bounded: C_max/C_min grows like 1.52^k
(147 at k = 12, 9851 at k = 22), the mass in the top 1 % of classes rises from 6.5 % to over 9 %, and the Hölder
exponent of the digit profile on coarse scales falls from 0.14 (k = 12) to 0.085 (k = 19), extrapolating to
0.04–0.09, possibly 0. The boundary layer is universal: the Hölder exponent at distance d from the top digit is
0.665, 0.401, 0.293, 0.232, 0.194 for d = 1 … 5, identical for every k to three decimals. To first order it is not a
new object. Let R(c) be c minimised over its top ternary digit and renormalised to mean 1, a vector on level k − 1.
Then R(c_k) is close to c_{k−1}: the total variation distance is 0.0126 at k = 8 and 0.0045 at k = 17, four times
smaller than the distance from c_k to the lift of c_{k−1}, and R²(c_k) is likewise close to c_{k−2}. The oscillation
over a ball with d free top digits is therefore the loss accumulated along the chain c_k → c_{k−1} → ⋯,
osc_k(d) ≈ Σ_{i<d} (1 − ρ_{k−i}): at k = 17 the measured values 0.0347, 0.0720, 0.1119, 0.1543, 0.1991 stand against
the partial sums 0.0347, 0.0722, 0.1129, 0.1571, 0.2053. The exponents β(d) = log₃(S(d+1)/S(d)) of the partial sums
are 0.668, 0.407, 0.301, 0.243, within 0.003–0.011 of the observed ones; with 1 − ρ_k ≈ q^k they are logarithms of
ratios of geometric partial sums, log₃ 2, log₃ 3/2, log₃ 4/3, … pulled up slightly by q ≈ 0.92. The five numbers
carry no information beyond the ratios of successive 1 − ρ_k. Two remarks. The observed exponents are more
k-independent than the model, which drifts by 0.005 over k = 11 … 17, so a second-order effect remains. And R(c_k) is
not feasible at level k − 1, because the minimum of a sum exceeds the sum of the minima; the defect
R(F_k c) − F_{k−1}(R c) is the misalignment of §6.3, and its size is what decides whether 1 − ρ_k → 0
(`boundary_layer.py`). Integrating the limit inequality on X = {m ∈ Z₃ : m ≡ 2 (mod 3)} with Haar measure gives
1 ≤ λ^{−2} + (1/3)(λ^{α−2} + λ^{α−1}) with equality exactly at λ = 2, so λ = 2 is the critical value of the limit
problem and the finite-k deficit is precisely 1 − ρ_k.

### 6.5 The finite-level loss is mean-field

The object left open in §6.4 is the defect D_k = R(F_k c_k) − F_{k−1}(R c_k). We measured it (`defect.py`), tested
the independence it suggests by randomising the system (`meanfield.py`), and traced the rise of the decay ratio
q_k = (1 − ρ_k)/(1 − ρ_{k−1}) to a measurable distribution (`weights.py`, `popdyn.py`). The conclusion of this section
is a heuristic and is marked as such.

**The defect.** The three level-k rows above a level-(k − 1) index r use the three lifts of the ×4 target and the
three lifts of the auxiliary target in a paired order, so D_k ≥ 0 pointwise, with equality exactly where the two
argmins agree (and on the class 5 mod 9, which has no auxiliary term). Because F_k c_k = c_k, the auxiliary vector
c̄ = R c_k is a strict super-solution at level k − 1, c̄ = F_{k−1}(c̄) + D_k, and the level-(k − 1) summation identity
gives the exact relation

  mean D_k / mean c̄ = g(λ_k) (ρ_k − ρ′_k),   g(λ) = (λ^{α−1} + λ^{α−2})/3,   ρ′_k = mean(R² c_k)/mean(R c_k),

which the data satisfy to all printed digits for k ≤ 19. The mean defect is therefore bookkeeping: with
e_k = ρ_{k−1} − ρ′_k it equals g(1 − ρ_k)[(1 − q_k)/q_k + e_k/(1 − ρ_k)], and the question λ_k → 2 is unchanged,
q_k → q∞ < 1 or q_k → 1. We find q_k = 0.913 at k = 12 rising to 0.931 at k = 21, linear in k to within 0.003
(slope 0.0018 per level, no measurable curvature), and e_k/(1 − ρ_k) falling from 0.048 to 0.029. The pointwise
structure is cleaner than the means. The two argmins are independent: they agree with probability 0.332 for k ≥ 13,
both marginals are uniform to 0.001, the joint law differs from the product by at most 0.002, and which lift wins
is unpredictable from the lowest four digits. The expected size of the defect, by contrast, is a coarse property:
its conditional mean given the top digit is uniform to 10^{−3}, the spread over a single digit falls from 0.60 of
the mean at digit 1 to below 0.06 from digit 4, and the top six digits explain 0.04 % of its variance. The excess
splits 64 % ×4 term and 36 % auxiliary term at every k. The defect is thus the product of two independent fine-scale
choices whose expected size is fixed by the residue mod 3⁴, which is the mean-field structure that §6.3 assumed.

**Random alignments reproduce λ_k.** The index maps are recursive in the top ternary digit: writing a level-k
index as i_low + t·N/3, the ×4 target is nxt_{k−1}(i_low) + σ(t)·N/3 and the auxiliary target is
aux_{k−1}(i_low) + π(t)·N/9, where σ is a cyclic shift and π a shift or a reflection of {0, 1, 2}, both fixed by i_low
through the arithmetic of 2 and 3. We replaced σ and π by independent uniform random bijections above a chosen
level and recomputed λ_k and ρ_k; nxt stays a bijection and aux stays 3-to-1, so the summed identity and the ceiling
λ = 2 are unchanged.

| randomised levels | change in λ_k | change in 1 − ρ_k | q_k |
|---|---|---|---|
| top level only, k = 9 … 13 (8 seeds) | within ±3·10^{−4} | +0.3 % | unchanged |
| 9 … k at k = 14 and k = 15 (6 seeds) | −2.1·10^{−3} ± 5·10^{−4} at both | +1.6 % at both | unchanged within 0.005 |
| 12 … 15 | −7.8·10^{−4} ± 9·10^{−5} | +0.6 % | within 0.003 |
| 6 … 13 | −0.9·10^{−2} | +6 % | noisy |
| 3 … 11 | −4·10^{−2} | +27 % | – |

The cost of randomising the fine levels saturates at 15 % of one level's gain instead of growing with the number of
levels, so the per-level increments of λ_k agree from k = 14 on; the coarse levels carry the arithmetic. The
question λ_k → 2 can therefore be posed for a random Krasikov–Lagarias model, the exact system up to a fixed level
lifted with independent uniform alignments above it, in which it becomes a quenched-versus-annealed question of the
kind studied for branching random walks. The exact system is slightly better than random and no comparison theorem
is known.

**Why q_k rises.** The level-(k + 1) triple above a level-k class m is a λ^{−2}-weighted copy of the triple above 4m
plus an injected triple from the auxiliary target, so the contraction of the loss from one level to the next is
governed by the ×4 weight a_m = λ^{−2} c(4m)/c(m), which equals 1 on class 5 and leaves 1 − a_m for the injection. A
class with a_m near 1 transports its loss without contraction; one with a_m near 0 is dominated by the injection. A
broader distribution of a_m means a weaker contraction and a larger q_k, and the distribution does broaden:

| k | 8 | 12 | 16 | 19 | 21 | fitted limit (ratio of increments) |
|---|---|---|---|---|---|---|
| std of a_m within class 2 mod 9 | 0.227 | 0.244 | 0.255 | 0.260 | 0.264 | 0.278 (0.91) |
| std of a_m within class 8 mod 9 | 0.119 | 0.127 | 0.132 | 0.135 | 0.137 | 0.145 (0.92) |
| std of log c | 0.714 | 0.798 | 0.859 | 0.894 | 0.913 | 1.026 (0.93) |

The increments shrink geometrically (maximal residuals of the fits 10^{−4} to 6·10^{−4}), so the weight distribution
converges, while the growth C_max/C_min ∝ 1.52^k is confined to the extreme tail. The naive variance recursion
q² = E[(1 − a)²]/(1 − E[a²]) gives 0.85 at k = 8 rising to 0.89 at k = 21 (magnitude weighted), well below the actual
0.91 to 0.93 because the minimum is not additive, but rising at the same rate as the data. A cavity model of the
random system, with sibling triples typed by the level-8 residue (`popdyn.py`), reproduces this mechanism but cannot
decide the limit: the loss factor c̄_{k+1}/c_k fluctuates by one third of the loss in the exact system, with sibling
correlation 0.35, and different closures of that fluctuation move q at k = 60 between 0.95 and 0.99.

**Heuristic conclusion.** If the distribution of the ×4 weight converges, the contraction per level converges to a
constant below 1, so q_k → q∞ < 1, 1 − ρ_k → 0 geometrically and λ_k → 2; the fitted limits put q∞ near 0.95.
Against this, q_k itself is linear in k over k = 12 … 21 with no measurable curvature, so the deceleration the
mechanism predicts is not yet visible. We state this as an expectation, not a result. A proof along these lines
needs two statements about the limit object: that the fine alignments may be treated as independent, which the
scrambling experiment supports to 2·10^{−3} in λ, and that the distribution of the ×4 weight converges, which the
data to k = 21 support with geometrically shrinking increments. Together they would give a contraction estimate for
the loss.

### 6.6 The spectrum of the linearisation

At the Perron vector the minimum in every row is attained by a fixed lift, so F is a sparse matrix J there, with
J[i, 4i] = λ^{−2} and J[i, argmin lift] = λ^{α−j}. We computed its spectrum (dense to k = 9, Arnoldi top-40 to
k = 15) at λ = λ_k and λ = 2.

| k | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |
|---|---|---|---|---|---|---|---|---|
| \|λ₂\| at λ_k | 0.857 | 0.865 | 0.861 | 0.865 | 0.861 | 0.865 | 0.867 | 0.865 |
| eigenvalues within 1 % of \|λ₂\| (of top 40) | 4 | 4 | 6 | 6 | 20 | 27 | 25 | 39 |
| \|λ₂\|/λ₁ at λ = 2 | 0.884 | 0.884 | 0.887 | 0.880 | 0.892 | 0.880 | 0.874 | 0.876 |

The gap does not close: |λ₂| is pinned at 0.86–0.87 while a ring of eigenvalues fills in at that radius, the
finite-k shadow of the edge of the essential spectrum. The second eigenvector is delocalised: its energy is 0.667
on every ternary digit (the value for a vector with no digit structure) and 0.71 on the top digit, while the Perron
vector's digit profile decays geometrically from 0.38 to 0.004; λ₂ is complex with a rotating argument. For k ≤ 9
the full spectrum is a disc of radius ≈ 0.8 containing 99 % of the eigenvalues, a thin ring at 0.865, and the
isolated Perron root. Consequently the k-dependence of 1 − ρ_k, and the slowing of the power iteration at large k
(effective contraction ≈ 0.97 at k = 22), are not set by the linear mixing rate; they come from the minimum, that
is, from argmin switching as the iterate moves and from non-normal transients. The question λ_k → 2 is a question
about the minimum structure, which is what §6.3 addresses, not about the spectrum of the linearisation. The
structural reason is that the doubling branch m ↦ 4m is an isometry of Z₃ and mixes nothing: on Hölder-α
functions the essential radius should be near 1/4 + (3/4)3^{−α}, which approaches 1 as α → 0, and the limit
vector's Hölder exponent is at most 0.09.

### 6.7 The same construction on 5x+1

The same construction applies to T(n) = n/2, (5n+1)/2: principal classes a ≡ 3 (mod 5) (odd predecessor
(2a − 1)/5), four doublings return to a principal class (λ^{−4} c_{16a}), and the odd predecessor falls into one
of five cases by a mod 25 (weight λ^{β−1−d} with β = log₂ 5 and d = 0, 1, 2, 3 further doublings, or dropped when
it is ≡ 0 mod 5), with the minimum over five lifts. A residue-walking LP (HiGHS, constraints generated by
following the map on residues, no index formulas) reproduces Table 2 for 3x+1 to 10^{−6} and matches the 5x+1
index formulas to 10^{−8} for k ≤ 6; a Metal kernel matches the NumPy map to 10^{−7}.

Summing the 5x+1 inequalities gives (1 − λ^{−4}) c̄ ≤ (λ^β/5)(λ^{−1} + λ^{−2} + λ^{−3} + λ^{−4}) ρ c̄ with ρ ≤ 1 the mean
loss from the minimum over five lifts. At ρ = 1 the two sides agree at λ = 2, the same mass-conservation identity as
for 3x+1, but that is not the binding root: they also cross at λ* = 1.5701677, and every λ in (λ*, 2) violates the
summed inequality even with ρ = 1. So λ_k(5) ≤ λ* for every k. Factoring 1 − λ^{−4} = (1 − λ^{−1})(1 + λ^{−1} + λ^{−2}
+ λ^{−3}) reduces the ρ = 1 equation to 1/λ + λ^{β−1}/5 = 1, the Malthusian equation of the naive backward
branching walk (child 2a at height +1; child (2a − 1)/5 at height 1 − β with probability 1/5). Its root
γ* = log₂ λ* = 0.650919 is the exponent η_{5,BP} of Kontorovich–Lagarias (Theorem 8.10) to every printed digit; the
0.649 of their Conjecture 7.2 is the same number rounded, and Volkov's 0.678 lies above the ceiling, beyond the
reach of this method at any k. For 3x+1 the same factoring gives 1/λ + λ^{α−1}/3 = 1, whose only root above 1 is 2.
In both systems, therefore,

  λ_k → (Malthusian root of the branching model) ⇔ ρ_k → 1.

5x+1 is thus not a calibration case with a known answer. The heuristic prediction for it is the ceiling itself,
1 − ρ_k(5) → 0, exactly as for 3x+1; it is a second instance of the open question.

| k | 6 | 8 | 10 | 11 | 12 | 13 | 14 |
|---|---|---|---|---|---|---|---|
| γ_k(5) | 0.411 | 0.449 | 0.477 | 0.489 | 0.499 | 0.508 | 0.517 |
| 1 − ρ_k(5) | 0.150 | 0.113 | 0.090 | 0.082 | 0.074 | 0.068 | 0.063 |
| ratio | 0.83 | 0.88 | 0.90 | 0.90 | 0.91 | 0.915 | 0.919 |

At k = 14 the gap to the ceiling is 0.134 in γ, close to the 3x+1 gap of 0.128 at the same k, and the ratios of
1 − ρ_k(5) rise from 0.83 to 0.919, faster than for 3x+1. What 5x+1 offers is a second sequence to set beside the
first under the same conjectural answer, and a constraint on proofs: an argument that ρ_k → 1 must work for 5x+1 as
well, which excludes arguments that use the contracting drift of 3x+1 (the 5x+1 walk drifts upward, since
log₂ 5 > 2). Equivalently, ρ_k → 1 says that the deterministic residue system realises the annealed, first-moment
growth rate of the branching walk. A calibration against a known negative would need a map whose deterministic
predecessor exponent is provably below its Malthusian root; we know of none. (No explicit predecessor-count
exponent for 5x+1 exists in the literature; π_a(x) ≥ x^{0.516} numerically at k = 14 appears to be the first,
pending the same certification.)

### 6.8 The linear limit is Tao's Syracuse measure

Replace the minimum over lifts in F₂ by the mean. The resulting linear operator has Haar measure as a left
eigenvector with eigenvalue 1, and its Perron vector h_k can be identified exactly.

**Proposition.** For k ≥ 3, h_k(m) is proportional to the average density, on the ball m + 3^k Z₃, of Tao's
Syracuse random variable

  Syrac(Z₃) = Σ_{j≥1} 3^{j−1} 2^{−S(j)},   S(j) = a_1 + ⋯ + a_j,   a_j i.i.d. with P(a_j = m) = 2^{−m}.

This is the stationary law of the 3-adic walk x ↦ x/2, x ↦ (3x+1)/2 with probability 1/2 each (Tao, Remark 1.13).

*Proof.*
- At every level the stationary density satisfies h(x) = (1/2)h(2x) + (3/2)[x ≡ 2, 8 (9)]·h((2x − 1)/3), where the
  last term is taken one level coarser.
- For x ≡ 2 (mod 3), 2x ≡ 1 (mod 3) has no odd predecessor, so h(2x) = h(4x)/2.
- For x ≡ 2 (mod 9), (2x − 1)/3 ≡ 1 (mod 3), so likewise h((2x − 1)/3) = h((4x − 2)/3)/2.
- Substituting gives h(x) = (1/4)h(4x) + (3/4)[x ≡ 2 (9)]h((4x − 2)/3) + (3/2)[x ≡ 8 (9)]h((2x − 1)/3). This is
  L^NT_k at λ = 2 (λ^{−2} = 1/4, λ^{α−2} = 3/4, λ^{α−1} = 3/2), with the mean over lifts as the coarser average. ∎

We checked the identification numerically to 10^{−15} for k ≤ 12. Consequently 1 − ρ_k has an exact linear
counterpart: the top-digit oscillation of Syrac. Tao proves (his Prop. 1.14) that its L¹ size,
Osc_{k−1,k}, is O_A(k^{−A}) for every A. This is the linear analogue of ρ_k → 1, and it is a theorem.

**A critical point.** Generalise to odd-step probability p, and let δ_k = h_k − h_{k−1} be the martingale difference
of the level densities. The difference obeys

  δ_k(c) = Σ_{j≥0} 3p(1 − p)^j [2^j c ≡ 2, 8 (9)] δ_{k−1}((2^{j+1}c − 1)/3).

The diagonal part of E[δ_k²] is exactly (3p/(2 − p))·E[δ_{k−1}²]. The off-diagonal part is a correlation between
δ_{k−1}(y) and δ_{k−1}(2^d(y + 1/3) − 1/3), and it is numerically negligible: the measured ratios of ‖δ_k‖₂ converge
to the diagonal prediction (`syracuse_measure.py`, exact marginals to k = 17).

| p | √(3p/(2 − p)) | ‖δ_k‖₂ ratio, k = 15 | ‖δ_k‖₁ ratio, k = 15 |
|---|---|---|---|
| 1/4 | 0.6547 | 0.6503 | 0.6501 |
| 1/3 | 0.7746 | 0.7722 | 0.7656 |
| 0.4 | 0.8660 | 0.8652 | 0.8435 |
| 1/2 | 1 | 1.0006 | 0.9279 |

At p = 1/2, the case of this paper, the factor is exactly 1.
- The density is (numerically) not square-integrable.
- The L¹ decay that Tao proves comes entirely from cancellation. Its per-level ratio is 0.926, 0.928, 0.929, 0.931
  for k = 14 … 17, rising at the same pace as the ratio of 1 − ρ_k (0.919 … 0.924 over the same k, 0.933 at k = 22).

A second effect sets the spread. The fixed point −1 of x ↦ (3x + 1)/2 (the trivial negative cycle) multiplies the
density near −1 by 3p per level. For p = 1/2 the density therefore grows like 1.5^k at −1, and like (1/2)^j·1.5^k at
its images −2^{−j}, which are dense. So it is unbounded on every ball, and its spread grows like 1.6^k. This is the
origin of the C_max ∝ 1.52^k of §6.4. The minimum over the top digit removes the spike at −1 itself (c_k does not
peak there) but not the growth. The min-system vector stays close to h_k without equalling it: total variation 0.14
and log-correlation 0.987 at k = 12.

Counting by depth instead of by size gives p = 1/4. Its density is the 3-adic limit function W_∞ that Applegate and
Lagarias (Experiment. Math. 4 (1995) 193–209, §6) obtained as a martingale limit; see the companion paper. There the
factor is √(3/7) = 0.655, the spread
stays bounded (≈ 3.55), all L^q norms decay fast enough for a continuous density, and the loss of the minimum-system
decays at that rate, 0.65 per digit. The size-counting problem of this paper is thus the critical member of a
one-parameter family whose subcritical members behave well. Heuristically, λ_k → 2 asks for a min-version of Tao's
fine-scale mixing at the critical point. That would explain why 1 − ρ_k decays neither geometrically nor fast.

## 7. What is and is not established

All results here are density statements, and even the limit γ → 1 would exclude neither a nontrivial cycle nor a
divergent orbit. Cycles are the province of Diophantine approximation: with Barina's verification to 2^{71} and
Hercher's analysis, a nontrivial cycle has at least 1.375·10^{11} odd terms and period at least 2.18·10^{11}.
Divergent orbits have no tool at all; Tao's theorem leaves them as a set of logarithmic density zero. Conway's
undecidability result for maps linear on residue classes implies that any proof must use the arithmetic of 2 and
3 specifically; the Krasikov–Lagarias system does, but only through the branching rule mod 3 and the size factors
2 and 3/2, which is why it yields exponents and not individual orbits.

Since September 2026, positive density for every fixed a is a formally verified theorem (Mazur; §1). By its
Corollary 1.2, the Collatz conjecture is equivalent to the set of integers whose orbit reaches 1 having upper
density 1. The results here are of a different type:
- uniform and explicit bounds (§4.4);
- the structure of the method (Theorem 1);
- its capacity (§6).

Within the method, what is now proved is structural: λ_k is attained, tight, unique and strictly increasing
(Theorem 1, machine-checked), so the exponents of §3 approximate a well-defined increasing sequence whose
limit is the method's exact capacity. The open mathematical problem is λ_k → 2 ⇔ ρ_k → 1. §6 reduces it to two statements about the
limit object: that the fine top-digit alignments act as independent, which the scrambling experiment supports to
2·10^{−3} in λ, and that the distribution of the ×4 weight converges, which the data to k = 21 support with
geometrically shrinking increments; together they would give a contraction estimate for the loss and hence λ_k → 2.
The same reduction holds for 5x+1 with ceiling 0.6509 in place of 1, so a proof cannot rest on the contracting drift
of 3x+1. We regard the data to k = 22 as consistent with that limit and not as evidence for it. §6.8 adds a
precise linear counterpart: with mean in place of minimum, ρ_k → 1 becomes Tao's fine-scale mixing, which is proved.
The difficulty therefore lies in the minimum, at a point where the linear problem is exactly critical.

## Data and code availability

Repository: github.com/dpalmqvist/kollatz (MIT). Certificates `certs/k{k}_{λ}/cert.json` and `certs/k{k}_{λ}_upper/`
with sha256 of the vectors; independent verifier `verify_cert.py`; the search (`kl.py`, `kl_mlx.py`, `kl_split.py`);
Lean modules, manifests and verifier reports in `lean_formal/`; measurements in `rho.py`, `holder.py`,
`rF2_fit.py`, `renorm.py`, `renorm2.py`, `spectrum.py`, `boundary_layer.py`, `defect.py`, `meanfield.py`, `weights.py`,
`popdyn.py`, `kl5.py`, `kl5_mlx.py`, `syracuse_measure.py`; explicit bounds in `spread_lp.py`, `spread_iter.py`,
`certify_spread.py`, `base_lift_chunked.py` and `certs/spread_k*/`; Theorem 1 in `monotone_check.py`,
`notes/strict_monotonicity.md` and `lean_formal/KLMonotone/`; the literature survey in `reports/`.

## References

- D. Applegate, J. C. Lagarias, Density bounds for the 3x+1 problem I. Tree-search method; II. Krasikov inequalities, Math. Comp. 64 (1995) 411–426, 427–438.
- D. Applegate, J. C. Lagarias, The distribution of 3x+1 trees, Experiment. Math. 4 (1995) 193–209.
- D. Barina, Improved verification limit for the convergence of the Collatz conjecture, J. Supercomput. 81:810 (2025).
- J. H. Conway, Unpredictable iterations, Proc. 1972 Number Theory Conf., Boulder, 49–52.
- R. E. Crandall, On the "3x+1" problem, Math. Comp. 32 (1978) 1281–1292.
- S. Eliahou, The 3x+1 problem: new lower bounds on nontrivial cycle lengths, Discrete Math. 118 (1993) 45–56.
- C. Hercher, There are no Collatz m-cycles with m ≤ 91, J. Integer Seq. 26 (2023) 23.3.5; corrigendum 14 June 2026.
- A. V. Kontorovich, J. C. Lagarias, Stochastic models for the 3x+1 and 5x+1 problems, in The Ultimate Challenge: the 3x+1 problem, AMS 2010; arXiv:0910.1944.
- I. Krasikov, How many numbers satisfy the 3x+1 conjecture?, Internat. J. Math. Math. Sci. 12 (1989) 791–796.
- I. Krasikov, J. C. Lagarias, Bounds for the 3x+1 problem using difference inequalities, Acta Arith. 109 (2003) 237–258; arXiv:math/0205002.
- S. Kurtz, J. Simon, The undecidability of the generalized Collatz problem, TAMC 2007, LNCS 4484, 542–553.
- J. C. Lagarias, The 3x+1 problem: an overview, in The Ultimate Challenge, AMS 2010; arXiv:2111.02635.
- J. C. Lagarias, D. Weiss, The 3x+1 problem: two stochastic models, Ann. Appl. Probab. 2 (1992) 229–261.
- L. Mazur, Collatz predecessor 0.90 (Lean 4 development), ProofAtlas, July 2026, commit 5f76a170.
- L. Mazur, Positive lower density of Collatz predecessors, v1.0, 6 Sep 2026, with Lean 4 formalisation, ProofAtlas.
- D. Palmqvist, The Krasikov–Lagarias exponents for the 3x+1 problem are attained and strictly increasing, draft, 2026.
- D. Palmqvist, Uniform exponential bounds for the number of 3x+1 preimages, draft, 2026.
- J. W. Sander, On the (3N+1)-conjecture, Acta Arith. 55 (1990) 241–248.
- J. Simons, B. de Weger, Theoretical and computational bounds for m-cycles of the 3n+1 problem, Acta Arith. 117 (2005) 51–70.
- T. Tao, Almost all orbits of the Collatz map attain almost bounded values, Forum Math. Pi 10 (2022) e12; arXiv:1909.03562.
- R. Terras, A stopping time problem on the positive integers, Acta Arith. 30 (1976) 241–252.
- G. J. Wirsching, An improved estimate concerning 3n+1 predecessor sets, Acta Arith. 63 (1993) 205–210; The Dynamical System Generated by the 3n+1 Function, LNM 1681, Springer 1998.
- E. Yolcu, S. Aaronson, M. J. H. Heule, An automated approach to the Collatz conjecture, J. Automated Reasoning 67 (2023) 15; arXiv:2105.14697.
