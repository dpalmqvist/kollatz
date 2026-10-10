# Lower bounds for 3x+1 predecessor counts: the Krasikov–Lagarias program to k = 22

Daniel Palmqvist, October 2026. Computation and certificates; the mathematics is Krasikov–Lagarias (2003).

## Statement

For a ≢ 0 (mod 3) let π_a(x) = #{n ≤ x : some T^(j)(n) = a}, T the 3x+1 map (T(n) = n/2 or (3n+1)/2).
Krasikov and Lagarias [KL] prove (Theorem 2.2 and §6): if the linear program L^NT_k(λ) has a feasible
solution, then for every γ < log₂ λ and every a ≢ 0 (mod 3), π_a(x) ≥ x^γ for all x ≥ x₀(a, γ).
Their computation reached k = 11, λ = 1.7922310, γ = 0.84.

We exhibit feasible solutions of L^NT_k(λ) for k = 12, …, 21 and the rational values λ below, verified
exactly in integer arithmetic. Consequently

    π_a(x) ≥ x^γ   for every γ < log₂(1.8925) = 0.92029…,   x ≥ x₀(a, γ).

| k | N = 3^(k−1) | λ (exact, rational) | log₂ λ | numerical optimum λ_k |
|---|---|---|---|---|
| 12 | 177 147 | 1.8064 | 0.85314 | 1.8064236 |
| 13 | 531 441 | 1.8188 | 0.86301 | 1.8188237 |
| 14 | 1 594 323 | 1.8307 | 0.87243 | 1.8307723 |
| 15 | 4 782 969 | 1.8419 | 0.88119 | 1.8419687 |
| 16 | 14 348 907 | 1.8522 | 0.88923 | 1.8522346 |
| 17 | 43 046 721 | 1.8616 | 0.89653 | 1.8616888 |
| 18 | 129 140 163 | 1.8703 | 0.90326 | 1.8703250 |
| 19 | 387 420 489 | 1.8783 | 0.90941 | 1.8783132 |
| 20 | 1 162 261 467 | 1.8857 | 0.91509 | 1.8857083 |
| 21 | 3 486 784 401 | 1.8925 | 0.92029 | 1.8925462 |
| 22 | 10 460 353 203 | 1.8988 | 0.92509 | 1.8988933 |

## The linear program

Variables c_m for m ∈ [3^k] = {m mod 3^k : m ≡ 2 (mod 3)}, α = log₂ 3,
c̄_r = min(c_r, c_{r+3^(k−1)}, c_{r+2·3^(k−1)}) for r ∈ [3^(k−1)]:

- m ≡ 2 (mod 9): c_m ≤ λ^−2 c_{4m} + λ^(α−2) c̄_{(4m−2)/3}
- m ≡ 5 (mod 9): c_m ≤ λ^−2 c_{4m}
- m ≡ 8 (mod 9): c_m ≤ λ^−2 c_{4m} + λ^(α−1) c̄_{(2m−1)/3}
- c_m ≥ 1.

(Equations (2.13)–(2.14) of [KL] print 3^k where 3^(k−1) is meant; the k ≤ 11 values of their Table 2 are
reproduced to 6–7 decimals only with 3^(k−1).) The map c ↦ right-hand side is monotone and 1-homogeneous;
λ_k is the λ at which its cone spectral radius equals 1. Candidates were found by power iteration in
float32 on an Apple M5 GPU (MLX), with warm starts from the lifted solution of level k−1.

## Certificates

Directory `certs/k{k}_{λ}/` holds the vector and `cert.json`. The exact check, for λ = P/Q and D = 2^d:

    q = ⌊D Q²/P²⌋,   L_j = ⌊D · (rigorous lower bound for λ^(α−j))⌋   (j = 1, 2; mpmath interval arithmetic),
    C_i = c_i · 2^b  (an exact integer for every entry of the float32 vector),
    C_i · D ≤ q · C_{(4i+2) mod N} + L_j · C̄_r   for every i,   checked in int64 with overflow excluded a priori.

Since q/D ≤ λ^−2 and L_j/D ≤ λ^(α−j), the inequality for C implies the one for c. Index i ↔ residue m = 3i+2;
4m ↔ (4i+2) mod N; for i = 3j the auxiliary index is 4j mod N/3, for i = 3j+2 it is (2j+1) mod N/3.
Formats: /1 stores the integer vector `C.npy` (int64); /2 stores the float32 vector `c_f32.npy` and b.

| k | file | sha256 of file | min relative slack |
|---|---|---|---|
| 12 | c_f32.npy | 858128e65f87ac7eb4238aef56fb8577b55e00b32a6c67b104209b7ef43f4639 | 7.8e-6 |
| 13 | C.npy | f3df159e561089ede2c6e6d7bab75d2d031e1f811bea944e79b7520e14ea35d4 | 7.4e-6 |
| 14 | C.npy | 34c1f41341da7e2861656aa1417ac12e44877a646a50bbe5dfb15258ee3f4a9e | 2.3e-5 |
| 15 | C.npy | 1f8ac1857ad47307eb6b375477f532bd66ce6e3d76b25985305da717a74aadfb | 2.1e-5 |
| 16 | C.npy | 9af1d7f3d931b475da77a015176567578e0f807f425ec7bc21d3e50b40f489b3 | 1.0e-5 |
| 17 | C.npy | 0aa746d0340b210c92d6ca6e614600e9fa743206703f1f84c65336bea58c03e5 | 2.6e-5 |
| 18 | C.npy | fdbda6a1a6e5b78ae011ff5c3abfe33ca579354702f5e99aed28f901fa4b21ab | 6.5e-6 |
| 19 | C.npy | ec8a1df9cb3abf47a60b3410a2d58a3464715feb687c3dbc04ebce03cd7f80a4 | 2.9e-6 |
| 20 | c_f32.npy | 8d7800f0be0634f5d6371782bc92bda2467e0f2d4bed83879dc873228dfd0083 | 1.4e-06 |
| 21 | c_f32.npy | a9b12240f5780ed7d62b22ffe19540a6e99c61edb1e72d923b11b55fe83f714f | 1.1e-05 |
| 22 | c_f32.npy | 83c9456a177c46178f8498687d80c9f9c64f894c776cf01a02b948075cadf3a8 | 2.4e-05 |
| 19 | c_f32.npy | 1b2bc9ad953f0bd0b81b2a71f01f07ade37db81f9e3a4a12d60b98e982b1ce7b | 3.1e-06 |
| 18 | c_f32.npy | 4602d3774a24081b4819c95e464356b27d3cb921da51942a2ec90b56db9d3f19 | 6.7e-06 |

Note (2026-10-08): the vectors for k = 18–21 were regenerated on a second machine (Apple M4 Pro, 64 GB) and are not bit-identical to the originals, so their hashes above are the new ones; λ and all integer constants are unchanged and the slacks agree to within 10 %. k = 22 (N = 3^21 = 10 460 353 203, 39 GB) was computed on that machine with the vector split across three GPU buffers (`kl_split.py`): λ_22 = 1.8988933, certificate at 1.8988 (γ = 0.9251), slack 2.4e-5.

Verification: `python verify_cert.py certs/k21_1.8925` (numpy + mpmath only, independent of the search code;
`--exact` repeats the check with Python integers). The k = 21 vector is 13 GB; the check takes about two
minutes on a laptop. Negative controls: each certificate's λ raised by 1e-4 to 5e-5 fails verification,
and tampered certificates (modified C, q+1, L₂+1, L₁·1.001) are rejected.

### Two-sided brackets: infeasibility certificates (2026-10-08)

A feasibility certificate shows λ_k ≥ λ_cert. The reverse direction uses the same integer check: for the
monotone, 1-homogeneous right-hand side F, a positive vector C with F(C) < C strictly in every row proves that
no feasible point exists (if d ≥ 1 with d ≤ F(d), put s = max_i d_i/C_i, attained at i*; then d ≤ sC gives
d_{i*} ≤ F(d)_{i*} ≤ sF(C)_{i*} < sC_{i*} = d_{i*}). `certify_fast.py --upper` rounds the coefficients up
(q = ⌈Dλ^-2⌉, L_j = ⌈D · rigorous upper bound of λ^(α−j)⌉) and checks q C_{4m} + L_j C̄ < D C_m in int64;
`verify_cert.py` checks the format independently. So λ_k lies in [λ_cert, λ_upper]:

| k | λ_cert (feasible) | λ_upper (infeasible) | width | k | λ_cert | λ_upper | width |
|---|---|---|---|---|---|---|---|
| 2 | 1.3534 (Table 2) | 1.35342 | 2e-5 | 11 | 1.7922 | 1.79225 | 5e-5 |
| 3 | 1.5275 | 1.5278 | 3e-4 | 12 | 1.8064 | 1.80644 | 4e-5 |
| 4 | 1.6122 | 1.61230 | 1e-4 | 13 | 1.8188 | 1.81884 | 4e-5 |
| 5 | 1.6627 | 1.66277 | 7e-5 | 14 | 1.8307 | 1.83079 | 9e-5 |
| 6 | 1.6944 | 1.69447 | 7e-5 | 15 | 1.8419 | 1.84198 | 8e-5 |
| 7 | 1.7201 | 1.72020 | 1e-4 | 16 | 1.8522 | 1.85225 | 5e-5 |
| 8 | 1.7449 | 1.74498 | 8e-5 | 17 | 1.8616 | 1.86170 | 1e-4 |
| 9 | 1.7615 | 1.76155 | 5e-5 | 18 | 1.8703 | 1.87034 | 4e-5 |
| 10 | 1.7771 | 1.77714 | 4e-5 | 19 | 1.8783 | 1.87833 | 3e-5 |
| | | | | 20 | 1.8857 | 1.88572 | 2e-5 |
| | | | | 21 | 1.8925 | 1.89256 | 6e-5 |
| | | | | 22 | 1.8988 | 1.89891 | 1e-4 |

The upper values are λ_k (float32 estimate) rounded up to 5 decimals plus 1e-5 (k = 3: +2e-4, because at
N = 9 the float32 ratio gap has a rounding floor of ~3e-5); all 21 upper certificates (k = 2 … 22) verify with relative slack
1.6e-6 … 1.3e-4 (`certs/k{k}_{λ}_upper/`; k = 22: 39 GB, data sha256 e86951cb…). Consequence: the numerical
λ_k are rigorously confirmed to 4–5 decimals, and the method at level k provably cannot reach γ ≥ log2 λ_upper.

## Explicit bounds from bounded-spread certificates (2026-10-09)

Krasikov–Lagarias's linear program minimises the spread C_max = max c / min c, and their Theorem 2.2 gives, for
any feasible point with 1 ≤ c ≤ t at level k and parameter λ, φ_k^m(y) ≥ c^m λ^y/(4t) for all y ≥ 0, where
φ_k^m(y) is the infimum of π*_a(2^y a) over a ≡ m (mod 3^k) not in a cycle. Hence such a point proves, with no
threshold x₀,

  π_a(x) ≥ (x/a)^{log₂ λ} / (4t)   for all x ≥ a and all a ≢ 0 (mod 3) not in a cycle.

The Perron vectors above have spread ≈ 1.52^k; at fixed λ < 2 the minimal spread stays bounded as k grows
(`spread_iter.py`; AVENUES §17). Certified bounded-spread points (format /2, `certs/spread_k{k}_{λ}/`, checked in
int64 with rounded-down coefficients and by `verify_cert.py`):

| k | λ | γ = log₂ λ | spread t | bound | data sha256 (prefix) |
|---|---|---|---|---|---|
| 9 | 1.70 | 0.7655 | 7.753 | π_a(x) ≥ (x/a)^{0.7655}/31.01 | see cert.json |
| 14 | 1.78 | 0.8319 | 15.003 | π_a(x) ≥ (x/a)^{0.8319}/60.01 | see cert.json |
| 14 | 1.80 | 0.8480 | 19.353 | π_a(x) ≥ (x/a)^{0.8480}/77.41 | see cert.json |

The certified k = 22 Perron vector gives (x/a)^{0.9251}/39404, which overtakes the k = 14 bound only beyond
x/a ≈ 10^{35}.

The constant improves by starting Krasikov–Lagarias's induction (their Theorem 5.1) at a higher base window
[Y − 2, Y], where the counts φ_k^m(y) are bounded below by exact enumeration of the residue-determined
("guaranteed") predecessor tree of each class (`base_lift.py`; counts verified against brute-force trees of
integers in the class). With the certified vector `certs/spread_k8_1.74/` (k = 8, λ = 1.74, spread 14.28) and
the window [4, 6] the constant is Δ = 0.843 instead of 1/(4·14.28) = 0.0175.

CORRECTION 2026-10-10: the value 0.865 stated here earlier took the minimum of L(y)/(cλ^y) only at the points of a
0.25-grid. The counts L(y) are step functions that jump off the grid, so the infimum over the real window is
smaller, by up to λ^{0.25}. `base_lift_chunked.py` (2026-10-10) computes the rigorous value: on the grid y_i it uses
min_i L(y_i)/(c λ^{y_{i+1}}). With grid 1/64 this gives Δ = 0.8435. Statement for a ≡ 2 (mod 3) not in a cycle:

  π_a(x) ≥ 0.843 · (x/a)^{0.7991}   for all x ≥ 2^4 a.

For a ≡ 1 (mod 3) use π_a ≥ π_{2a}: divide the constant by λ and require x ≥ 2^5 a.

**Improved (2026-10-10).** The certified k = 14 vector `certs/spread_k14_1.80/` (λ = 1.80, spread 19.35), with the
lifted base window around Y = 8.25 (1.6·10^6 guaranteed trees, 4·10^9 nodes, 3 min; `base_lift_chunked.py
certs/spread_k14_1.80 10 20000 1/64` → `base_lift_spread_k14_1.80.json`), gives for a ≡ 2 (mod 3) not in a cycle

  π_a(x) ≥ 0.7146 · (x/a)^{0.8480}   for all x ≥ 2^{6.25} a,

compared with 1/(4·19.35) = 0.0129 from Theorem 2.2 directly. For a ≡ 1 (mod 3) divide by 1.8 and require
x ≥ 2^{7.25} a.

A further certified vector, `certs/spread_k15_1.82/` (k = 15, λ = 1.82, spread 26.10, slack 9.9·10^{−6}, made with
`spread_iter.py --slack=1e-5 15 1.82` + `certify_spread.py`), gives the same way (4.8·10^6 trees, 2.3·10^{10} nodes,
19 min):

  π_a(x) ≥ 0.5681 · (x/a)^{0.8639}   for all x ≥ 2^{6.25} a   (a ≡ 2 mod 3; a ≡ 1: divide by 1.82, x ≥ 2^{7.25} a).

Explicit envelope, for a ≡ 2 (mod 3) not in a cycle:

| range of x/a | best explicit bound | source |
|---|---|---|
| 2^{6.25} … 2^{15.7} | 0.7146 (x/a)^{0.8480} | k = 14, λ = 1.80, lifted base |
| 2^{15.7} … 2^{18.3} | 0.5514 (x/a)^{0.8718} | k = 16, λ = 1.83 (`certs/spread_k16_1.83`), lifted base |
| 2^{18.3} … 2^{335} | 0.4987 (x/a)^{0.8797} | k = 17, λ = 1.84 (`certs/spread_k17_1.84`), lifted base |
| ≥ 2^{335} | (x/a)^{0.92509} · C_min/(4λ C_max), C_max/C_min = 9840.7 | k = 22 Perron certificate, Thm 2.2 |

The k = 16 vector (spread 29.49, slack 9.9·10^{−6}) gives π_a(x) ≥ 0.5514 (x/a)^{0.8718} for all x ≥ 2^{6.25} a. Its
base lift takes 5.8·10^{10} nodes in 67 min (grid 1/32). It dominates the k = 15 bound everywhere. The k = 17 vector
(λ = 1.84, spread 33.84, slack 9.9·10^{−6}) gives 0.4987 (x/a)^{0.8797} for x ≥ 2^{6.25} a (1.7·10^{11} nodes, 2.4 h).

The λ in the last row covers all residues.

(Rigor of the lifted constants: the counts are exact integers, the infimum over each grid cell uses the right-hand
end, and the float64 path maxima e − j(α − 1) are never within 2.5·10^{−5} of a grid point (j ≤ 80, mpmath check),
so the binning tolerance of 10^{−12} cannot misplace a node.)

Mazur's positive-density theorem (`notes/m2_audit.md`) has ineffective constants for general a, so these remain the
best *explicit* lower bounds at any height one can write down. The minimal spread t*_∞(λ) grows like (2 − λ)^{−2} on λ ≤ 1.78; if that continued to λ = 2 (an
unproved limit statement) it would give π_a(x) ≫ x/(log x)².

## Structure of L^NT_k: attainment, tightness, uniqueness, strict increase (proved 2026-10-09)

Theorem (`notes/strict_monotonicity.md`; machine-checked in Lean 4, `lean_formal/KLMonotone/`, standard axioms
only). Let λ_k = sup{λ ∈ [1, 2] : L^NT_k(λ) feasible}. For every k ≥ 2:
1. λ_k is attained, and 1 < λ_k < 2.
2. Every feasible point at λ_k satisfies all principal inequalities with equality, and it is unique up to scaling.
3. λ_k < λ_{k+1}.

Consequences:
- c·λ_k^y solves Krasikov's difference inequalities I_k exactly, so no exponent above log₂ λ_k can be obtained
  from I_k.
- Every Applegate–Lagarias splitting/truncation LP has λ* ≤ λ_k ([AL2, Conjecture 4.1]).
- The bound of [KL, Theorem 2.2] holds at λ_k itself.

Literature status:
- [KL, §6] lists strict increase as open and conditions (1)–(2) as "likely … but may be difficult to prove".
- [AL2, §4] (1995) had called strict increase easy. Its sketch shows only that the lifted solution has a strict
  inequality somewhere; for a parametric LP that does not let λ increase.

The missing ingredient: m ↦ 4m is a single cycle of length 3^{k−1} on [3^k], and every row contains
λ^{−2} c_{4m}. So slack in one row spreads to all rows, and a positive vector with F(c) ≥ c, F(c) ≠ c can be
improved to F(z) > z everywhere. Numerical companion: `monotone_check.py`.

For the certificates above this means: each λ_cert < λ_k is a strict lower bound of a uniquely defined number λ_k,
whose fixed point is the (unique) Perron vector of the certificate computation. The brackets [λ_cert, λ_upper] pin
it down to 2·10^{−5} … 10^{−4}.

## Uniform bounds for the number of k-step preimages (2026-10-10)

Let n_k(a) = #{n : T^k(n) = a}, and let N*_k(a) be the number of leaves of the depth-k pruned tree (nodes ≢ 0 mod 3)
of Applegate–Lagarias I. They proved (1.302053)^k ≤ n_k(a) ≤ (1.358386)^k for large k (Theorem 1.1, depth-30
extremal trees). This night's results (`notes/extremal_trees.md`, `extremal_trees.py`):

- **Exact extremal counts:** N^−(k) to k = 59 and N^+(k) to k = 55. They give (1.317329)^k ≤ n_k(a) ≤
  (1.346858)^k. N^±(k)/(4/3)^k is constant to 0.7 % for k ≥ 25, which supports Conjecture C′.
- **Residue-class certificates** (a monotone, homogeneous recursion on classes mod 3^r, verified in exact integer
  arithmetic for r ≤ 19):

    0.2822 · (1.3333119)^k ≤ N*_k(a) ≤ 3.556 · (1.3333567)^k   for every a ≢ 0 (mod 3) and every k ≥ 0,

  hence (1.3333119)^k ≤ n_k(a) ≤ (1.3333567 + ε)^k for all large k, uniformly in a. The losses shrink by ≈ 0.65 per
  residue digit.
- **Machine-checked** (`lean_formal/PreimageBound/`, Lean 4 + Mathlib, 2026-10-10). For every a ≢ 0 (mod 3) and every
  k ≥ 0:

    0.2847 · (1.3331664)^k ≤ #{n ∈ [1, 2^k a] : T^k(n) = a},

  and (1.333)^k ≤ n_k(a) for k ≥ 20200.
  - The r = 14 certificate (3.2 M classes) is evaluated by the kernel with `decide +kernel`; no `native_decide`.
  - Only the three standard axioms (`#print axioms` re-run by the main session).
  - `leanchecker` passes per module (138 modules for r = 14).
  - The independent kernel nanoda passes on all three exports (up to 23 481 declarations).
  - An exact Python check with brute-force comparisons passes.
- **Independent check:** a separate implementation in the main session certifies r = 13 (μ ≥ 1.333075,
  μ′ ≤ 1.333637) and r = 16 (μ ≥ 1.333259, μ′ ≤ 1.333416), in agreement with the agent's values.
- **The limit measure** (`syracuse_measure.py`, `paper/preimage.md` §7, 2026-10-10). With the minimum replaced by the
  mean, the Perron vectors h_r are exactly the level-r marginals of one probability measure ν on ℤ₃^× (proved: the
  top-digit average commutes with the operator). ν is the stationary law of x ↦ x/2, x ↦ (3x+1)/2 with
  probabilities 3/4, 1/4. Probability 1/2 gives Tao's Syracuse random variable, which is also exactly the
  Krasikov–Lagarias system at λ = 2 with mean instead of min.
  - The normalised counts (3/4)^k N*_k converge weakly to ν (proved).
  - Continuity of ν's density implies Conjecture C′ (proved).
  - The martingale differences contract in L² by √(3/7) = 0.6547 up to cross-correlations that vanish numerically.
    This explains the 0.65 loss rate. All L^q norms decay fast enough for a continuous density.
  - At r = 17 the density's extremes, 1/min h = 2.0387 and max h = 1.7386, sit within 2·10^{−4} of the limits
    2.039 and 1.742 of the exact extremal counts.

  For Tao's case the diagonal L² factor is exactly 1, so the Krasikov–Lagarias problem sits at a critical point.
  Its L¹ decay ratio (0.931 at r = 17, rising) tracks the 1 − ρ_k ratios.

## Independent checks

- `lp_check.py`: L^NT_k(λ) solved as an explicit LP (HiGHS), constraints built from residues with Python
  integers, no code shared with the search. λ_k agrees with Table 2 of [KL] to < 1e-6 for k = 2…9; the LP
  solutions at λ_k − 2e-6 verify exactly in rational arithmetic; λ_k + 1e-4 is infeasible.
- Two 2026 Lean-formalised projects on the same LP report values consistent with ours at equal k:
  0.895 (k = 17, informal; msharpe248/collatz) and 0.90, 0.901 (k = 18; L. Mazur, ProofAtlas), against our
  0.8965 and 0.9033.
- Lean 4 (Mathlib, Lean v4.30.0-rc2), via Mazur's development: our k = 18 vector, re-tuned at λ = 2^(9032/10000) and
  exported to his certificate format (`export_mazur.py`), passes his `native_decide` checker together with his
  k = 18 termination potential. The resulting theorem `CollatzPredecessor0903.predecessor_count_lower_bound_0903`
  states x^(903/1000) ≤ π_a(x) for all large x and every a ≢ 0 (mod 3); its axioms are propext, Classical.choice,
  Quot.sound and the two named native_decide checks, the same trust base as his 0.90. Modules and manifests are in
  `lean_formal/`. The k = 19 certificate (γ = 9093/10000) passed the same way, using a loop-based checker
  (`LoopCheck.lean`, proved equivalent to Mazur's) to fit in memory and a termination potential generated by
  `potential.py` (least fixed point of his constraints; it reproduces his k = 18 payload bit for bit). Theorem
  `CollatzPredecessor0909.predecessor_count_lower_bound_0909`: x^(909/1000) ≤ π_a(x) for all large x, every
  a ≢ 0 (mod 3); axioms as above with the two k = 19 checks. native_decide times: 568 s and 818 s (k = 18),
  1819 s and 2335 s (k = 19), one core each. Both results exceed the previously formalised exponent 0.90.
  k = 20 and 21 exceed the memory of a proof-assistant check on this machine (about 30 and 90 GiB with the loop checker).

## Where the method stands

- The summed inequality (1 − λ^−2) c̄_{k,k} ≤ ⅓(λ^(α−1) + λ^(α−2)) c̄_{k−1,k} [KL §6] is tight to 3e-5 on
  all our solutions, so λ_k is determined by the mixing ratio ρ_k = c̄_{k−1,k}/c̄_{k,k} alone. [KL]:
  exponent 1 is reachable iff λ_k → 2, which holds iff ρ_k → 1. We find 1 − ρ_k = 0.0573 (k = 11) … 0.0241
  (k = 22) with successive ratios rising from 0.913 to 0.933; the data do not decide whether ρ_k → 1.
- The ceiling is the branching-walk exponent. Since ρ ≤ 1, the summed inequality caps λ_k at the smallest root of
  its ρ = 1 form, which factors to the Malthusian equation 1/λ + λ^(log2 p − 1)/p = 1 of the naive backward
  branching walk. For 3x+1 (p = 3) the only root is 2; for 5x+1 (p = 5) the smallest root is 1.5701677,
  γ = 0.650919, exactly the Kontorovich–Lagarias exponent η_{5,BP}. In both systems λ_k → ceiling ⇔ ρ_k → 1; the
  5x+1 system (`kl5.py`, k ≤ 14, γ_14 = 0.517) is a second instance of the same open question (`boundary_layer.py`).
- The universal top-digit boundary layer (Hölder exponents 0.665, 0.401, 0.293, 0.232, 0.194 at distance 1 … 5
  from the top digit, k-independent to three decimals) is explained to first order: minimising c_k over its top
  digit gives c_{k−1} to total variation 0.0045 (k = 17), so the ball oscillation with d free digits is the partial
  sum of 1 − ρ_{k−i} and the exponents are log_3 of ratios of those sums (model 0.668, 0.407, 0.301, 0.243). The
  remaining object is the defect R(F_k c) − F_{k−1}(R c) between coarse-graining and the level-(k−1) map. Measured
  (`defect.py`, k ≤ 19): it is nonnegative, its mean obeys the exact identity mean D/mean c̄ = g(λ_k)(ρ_k − ρ′_k)
  (so it adds nothing to the ρ_k sequence), and pointwise it is the product of two independent argmin choices
  (agreement 0.332) whose expected size depends only on the residue mod 3^4. The decisive sequence is
  q_k = (1 − ρ_k)/(1 − ρ_{k−1}) = 0.913 (k = 12) … 0.931 (k = 21), rising ≈ 0.002 per level; undecided.
- λ_k is a mean-field quantity (`meanfield.py`): the index maps are recursive in the top ternary digit with a
  bijection of {0, 1, 2} per class fixed by the arithmetic of 2 and 3; replacing these bijections by i.i.d. uniform
  random ones at every level from 9 up changes λ_14 and λ_15 by the same −2.1·10^{−3} ± 5·10^{−4} (a saturated offset,
  15 % of one level's gain), raises 1 − ρ by 1.6 % and leaves q_k unchanged within 0.005. Scrambling only the top level is invisible from
  k = 9 on; scrambling from level 6 or 3 costs 10^{−2} or more. The arithmetic matters in the coarse residues and
  the weights; the fine alignment can be random. The question λ_k → 2 can thus be posed for a random K–L model.
  A cavity (population-dynamics) treatment of that model reproduces the mechanism behind the rising q_k, the
  broadening of the magnitude distribution, but its asymptotics depend on how the loss-factor fluctuation is
  closed (q at k = 60 between 0.95 and 0.99), so it does not decide q∞ (`popdyn.py`). In the exact vectors the
  spread of the ×4 weight and of log c both grow to k = 21 with geometrically shrinking increments (ratios
  0.91–0.93, fitted limits 0.278 and 1.03; `weights.py`), which heuristically points to q∞ < 1 but is not yet
  visible in q_k itself (linear in k, slope 0.0018, over k = 12 … 21).
- The dependence of c on each ternary digit decays geometrically in the digit position, with a factor
  that rises with k (0.828 at k = 12, 0.875 at k = 19) and extrapolates to roughly 0.94. The spread
  C_max/C_min grows like 1.52^k, so the k → ∞ limit object is unbounded.
- Sparse refinement (variables on a non-uniform 3-adic tree) captures gain only in proportion to the
  number of variables and loses badly at equal variable count (`adaptive.py`); the method needs every
  digit in every class. Memory therefore caps k at 21 on 24 GB, 22 on 64 GB, 23 on 192 GB.

[KL] I. Krasikov, J. C. Lagarias, Bounds for the 3x+1 problem using difference inequalities,
Acta Arith. 109 (2003) 237–258, arXiv:math/0205002.
[AL2] D. Applegate, J. C. Lagarias, Density bounds for the 3x+1 problem II. Krasikov inequalities,
Math. Comp. 64 (1995) 427–438.

Formalisation status (2026-10-09): the structure theorem (attainment, tightness, uniqueness, λ_k < λ_{k+1}, for
all k) is `KLMono.KL_lambda_strictMono` in `lean_formal/KLMonotone/Basic.lean` (Lean 4 + Mathlib, standard axioms
only, no certificates, 10 s to check). `CollatzPredecessor0903` (x^{903/1000}, k = 18), `CollatzPredecessor0909`
(x^{909/1000}, k = 19) and `CollatzPredecessor0914` (x^{914/1000}, k = 20) are Lean 4 theorems in Mazur's development,
each depending on propext, Classical.choice, Quot.sound and two `native_decide` checks (the LP certificate and the
adaptive forced potential). k = 20: potential check 5940 s (26 GB), weights check 7382 s (55.9 GB) on an M4 Pro 64 GB;
the publication exponent is 914/1000 because the transfer lemma needs it strictly below the certificate exponent
9150/10000. Lessons on multi-gigabyte oleans (import order, module-name hash) are in `lean_formal/README.md`.
