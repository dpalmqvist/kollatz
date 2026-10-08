# Lower bounds for 3x+1 predecessor counts: the Krasikov–Lagarias program to k = 21

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
| 20 | c_f32.npy | 5bd2a7b1bc8aadd1ab3f6478ee584284205a1f6fa26ca7e1b68ff76aab8486e7 | 1.5e-6 |
| 21 | c_f32.npy | 6121c786ebf1163df50fba87cfef4e5edb6d21d0cb9bc102e218cae29d6a4a9d | 1.1e-5 |

Verification: `python verify_cert.py certs/k21_1.8925` (numpy + mpmath only, independent of the search code;
`--exact` repeats the check with Python integers). The k = 21 vector is 13 GB; the check takes about two
minutes on a laptop. Negative controls: each certificate's λ raised by 1e-4 to 5e-5 fails verification,
and tampered certificates (modified C, q+1, L₂+1, L₁·1.001) are rejected.

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
  exponent 1 is reachable iff λ_k → 2, which holds iff ρ_k → 1. We find 1 − ρ_k = 0.0573 (k = 11) … 0.0258
  (k = 21) with successive ratios rising from 0.913 to 0.931; the data do not decide whether ρ_k → 1.
- The dependence of c on each ternary digit decays geometrically in the digit position, with a factor
  that rises with k (0.828 at k = 12, 0.875 at k = 19) and extrapolates to roughly 0.94. The spread
  C_max/C_min grows like 1.52^k, so the k → ∞ limit object is unbounded.
- Sparse refinement (variables on a non-uniform 3-adic tree) captures gain only in proportion to the
  number of variables and loses badly at equal variable count (`adaptive.py`); the method needs every
  digit in every class. Memory therefore caps k at 21 on 24 GB, 22 on 64 GB, 23 on 192 GB.

[KL] I. Krasikov, J. C. Lagarias, Bounds for the 3x+1 problem using difference inequalities,
Acta Arith. 109 (2003) 237–258, arXiv:math/0205002.
