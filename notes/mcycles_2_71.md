# m-cycles with the 2^71 verified range: re-run of Simons–de Weger / Hercher (avenue 13)

Date: 2026-10-10 (night run). Script: `mcycles.py` (repo root). Nothing was committed or posted.

## Bottom line

- **With X0 = 2^71 (and with 2075·2^60), Hercher's method still excludes exactly m ≤ 91. The larger verified
  range gives no new m.** The established method (Simons–de Weger upper bound plus Hercher's bootstrap) needs
  X0 ≥ 14948·2^60 ≈ 2^73.87 to exclude m = 92, and X0 ≈ 2^76.07 to reach m ≤ 101.
- **Binding constraint at 2^71.** For m = 92 the bootstrap stalls at K ≥ 205 632 218 873 398 596 256 ≈ 2.06e20.
  The Simons–de Weger ceiling is K2(92) = 3.42e20. The stall is not an artefact of the iteration: (K, L) =
  (205 632 218 873 398 596 256, 120 287 136 981 023 372 109) satisfies Hercher's inequality *at its own K*, with
  P − Kδ equal to 0.196 of the allowed bound. An exhaustive enumeration up to K2(m) finds such surviving
  shapes for every m = 92, …, 101 (1, 2, 3, 4, 6, 7, 9, 11, 18 and 29 shapes).
- **The unrefereed claim m ≥ 102** (GitHub `justinalick/collatz-m-cycles-101-lean`, 2026-09-28) is therefore
  *not* a re-run of Hercher with 2^71. Its README says so itself: m = 92 … 101 rest on a **new** "two-rise bound"
  and "chain argument" that exclude the shapes the bootstrap leaves. Our surviving shapes are a subset of the
  shapes it lists and excludes, so the two computations agree at the data level. I did **not** check the new
  argument, and I did not build or run the repository.
- **The reproduction is exact.** It covers Hercher's Theorem 23 sequence and the result m ≤ 91 (and m = 92
  not excluded) at 695·2^60. It also covers his Table 1 and the m ≥ 83 that his abstract attributes to the
  Simons–de Weger method. On the Simons–de Weger side it covers the K1/J2/K2 tables, Corollary 11, Lemmas 15
  and 17 (m ≤ 63, m ≤ 68), and the Lemma 18 lattice results of both versions: m ≤ 68 at 301·2^50 (all 22
  candidate counts) and m ≤ 75 at 5·2^60.
  There are four small discrepancies, all printing errors or omissions in the papers that don't affect any
  result (§3).

## 1. Method (what `mcycles.py` computes)

Notation: T(n) = n/2 or (3n+1)/2, δ = log2 3. An m-cycle has m local minima, i.e. m blocks of k_i odd steps
followed by l_i even steps. K = Σk_i is the number of odd elements, L = Σl_i the number of even ones. Every
element is > X0.

**Upper bound** (Simons–de Weger v1.44, §3, §5, §6; Hercher uses it as "K < 1.4784 m δ^m"):
- Lemma 4 and Cor. 5: 0 < Λ = (K+L) log 2 − K log 3 < m/X0.
- Lemmas 6–7 (chaining x_{i+1} < b^δ x_i^δ): Λ < m c_m 2^{−(δ−1)K/(δ^m−1)}.
- Lemma 12 (Rhin 1987): Λ > e^{−13.3(0.46057 + log K)}. Combined with the above this gives Lemma 14,
  K < K1(m).
- Lemmas 9 and 16: if K > J2(m), then (K+L)/K is an odd-index convergent with q_n < K1(m), so a_{n+1} ≤ A(m).
  This gives K < K2(m), the largest root of m c_m 2^{−(δ−1)x/(δ^m−1)} = log 2/((A(m)+2)x).
  For 64 ≤ m ≤ 511, A(m) = a_14 = 55.

**Lower bound** (Hercher, JIS 26 (2023) 23.3.5 = arXiv:2201.00406v3, with the Sage worksheet from the JIS
page):
- Theorem 16: δ < (K+L)/K < δ + S/(3K log 2), where S = Σ T(n_i) and T(n_i) is the reciprocal sum over the
  ascent from the i-th minimum.
- Bounds for S:
  - Cor. 17: S ≤ (97/54) m/X0.
  - Cor. 19 (a computer proof valid for 695·2^60 only): S ≤ (7/5) m/(695·2^60).
  - Theorem 21, with premise ((δ^{m2}−1)/(δ−1)) log2(162X0/97) ≤ (m2/m)K and v = (m2/m)K(δ−1)/(δ^{m2}−1):
    S < (97(m−m2)+73)/(54X0) + 3/(2^v−1) + 3(m2−1)/(2^v−1)^δ. There are special cases for m2 = m−1 and m2 = m.
- Lemma 22: (K+L)/K lies in (δ, δ+d), so K ≥ the smallest denominator in that interval.
- Theorem 23: iterate K_lo → m2(K_lo) → d(K_lo) → K_lo := q_min(δ, δ+d). This is valid because every bound
  for S/K is nonincreasing in K.
- m is excluded once K_lo > K2(m). The start value is the SdW Lemma 10 bound at the given X0. Hercher's
  7·10^11 gives identical results.

**Rigour.** All decisions use exact rationals:
- δ is enclosed to 1e-1100.
- d is rounded up, and the simplest fraction is taken in the widened interval (δ_lo, δ_hi + d).
- K2 is rounded up, and the partial quotients come from the common prefix of the continued fractions of δ_lo
  and δ_hi.
- Everything else uses mpmath at 300 digits.

The Lemma 18 lattice enumeration is exact integer Gauss reduction, followed by a high-precision filter.

**Exploratory extension (not in either paper).** `survivors` enumerates all (K, L) with K_lo ≤ K < K2(m) that
satisfy Hercher's inequality evaluated at their own K. It uses the best of Cor. 17/19 and Theorem 21 over all
admissible m2. The enumeration is the same lattice code as for SdW Lemma 18.

## 2. The corrigendum (14 June 2026)

It replaces the faulty derivation at the bottom of p. 14 of the proof of Theorem 21. The new argument:
- Choose the window of m2 consecutive minima that maximises Σx_i, where x_i = log2(n_i + 1).
- Bound T(n_i) < 3/(2^{x_i} − 1).
- Maximise this convex function over the polytope {x_i ≥ 1, x_{i+1} ≤ δx_i, x_first < δx_last,
  Σx ≥ (m2/m)K}. The maximum is attained at a vertex, which is a cyclic geometric progression starting at v.

It ends at the same bound 3/(2^v−1) + 3(m2−1)/(2^v−1)^δ as the original. **The statement and every number
used in the computation are unchanged.** The premise of Theorem 21 is still what rules out vertices with
x_i = 1. I checked the convexity and vertex steps (the polyhedron is unbounded, but its recession directions
are nonnegative and S decreases along them, so the supremum is still attained at a vertex). The repaired
bound is what `mcycles.py` uses.

## 3. Validation (`mcycles.py validate`: 55 s, 49 checks OK, 4 documented DIFFs, exit 0)

**Hercher, X0 = 695·2^60:**
- Theorem 23 with m = 91 and K0 = 7·10^11:
  - m2 = 47, 67, 77, 82, 86, 88, 91 (exact).
  - K ≥ 5 267 319 278 509 397, 3.976e17, 4.640e18, 2.744e19, 7.769e19, 2.056e20, 7.942e21. The paper
    truncates these to 5.2e15, 3.97e17, …, 7.94e21.
  - The first-step fraction 8348503535763010/5267319278509397 matches the worksheet.
  - The printed d values match exactly at steps 1, 2, 4 and 5. At steps 3, 6 and 7 they match only if K is
    re-entered rounded (3.9e17, 7.7e19, 2.06e20). Hercher evidently re-typed rounded K values into the
    worksheet. At step 7 this used 2.06e20, slightly above the proven 2.0563e20. The exact value gives
    d = 1.23e-43 instead of 1.11e-43 and the **same** final K ≥ 7.94e21 > K2(91) = 2.14e20, so this is harmless.
- Every m ≤ 91 is excluded (with either start), and m = 92 is not.
- Table 1 (Cor. 24): the m-boundaries 98/99, 117/118, 276/277, 3079/3080 and 12055/12056 and the K levels all
  agree. One exception: the row "m ≤ 276 ⇒ K > 4.68e18" should read 4.64e18. No best upper approximation of δ
  has a denominator between 4.640e18 and 2.744e19 (**DIFF**, typo).
- The abstract's claim that the Simons–de Weger method at 695·2^60 gives m ≥ 83 is reproduced: the first m
  with lattice candidates is 83.

**Simons–de Weger v1.44, X0 = 5·2^60:**
- K1, J2 and K2 (m = 2 … 512), n(m) and A(m) (218/55, 230/100) and k2(91) = 1.4784 all agree to the printed
  digits.
- Corollary 11 range boundaries: all agree.
- Lemma 15 gives m ≤ 63 and Lemma 17 gives m ≤ 68.
- Lemma 18:
  - There are no candidates for 69 ≤ m ≤ 75.
  - The m = 76 and 77 lists match, with "falls when X0 ≥" values 5.39, 9.39, 36.8 / 5.46, 9.52, 37.3, 7.58
    (the paper rounds up).
  - The counts for m = 78–90 agree except m = 80: we find 13 against the paper's 12 (**DIFF**). The paper's own
    maximum K and its counts for m = 79 and 81 agree with ours, and none of the 13 is borderline. Probably a
    typo.
  - The paper's "K ≥ 111 738 283 365 989 051" for m = 78–90 fails the paper's own Corollary 5 at 5·2^60
    (Λ = 1.75e-17 > 90/X0). Our minimum is 117 972 833 293 231 014 (**DIFF**). Their stated bound is weaker
    than ours, so this is harmless.

**Simons–de Weger, Acta Arith. 117 (2005), X0 = 301·2^50** (the scanned published version):
- m ≤ 63 follows from K2 against Lemma 10, and there are no lattice candidates for m = 64–68, so m ≤ 68.
- The candidate lists for m = 69–72 agree, including the "falls when X0 ≥" values 577, 585, 593/624 and
  602/633/309/667/706 (·2^50).
- All 18 counts for m = 73–90 (8 … 23 181) agree, as do the minimum and maximum K.

**Note on primitivity.** Both versions list only primitive (K, L), i.e. gcd(K, K+L) = 1. For example, m = 77
at 5·2^60 also admits 2·(130441933147714940, 76303639412989207) (**DIFF**). This is harmless: a multiple
j·(K′, L′) has Λ multiplied by j, so its primitive base is itself a candidate and fails at a larger X0. No
exclusion claim is affected. With non-primitive pairs counted, there are still no candidates for any excluded m.

## 4. Results at X0 = 2^71 and 2075·2^60

`mcycles.py run '2^71' 140` (13 s). 2075·2^60 gives identical output.

| | 2^71 | 695·2^60 (Hercher) |
|---|---|---|
| Hercher's bootstrap excludes | m ≤ 91 | m ≤ 91 |
| m = 92: bootstrap floor | K ≥ 2.0563e20 | K ≥ 7.769e19 |
| K2(92) (SdW ceiling) | 3.4228e20 | 3.4228e20 |
| Simons–de Weger method alone (L10/L17 + L18) | m ≤ 82 | m ≤ 82 |

**Robustness.** I tried:
- start values 7·10^11, 7.2·10^10 and SdW Lemma 10 at 2^71;
- m2 = the largest admissible value (as in the worksheet), and the best bound over all admissible m2.

All give m ≤ 91. At 2^71 Corollary 19 is irrelevant: Corollary 17 with X0 = 2^71 is 2.3× stronger.

**Why it stops at 91.** At 2^71 and m = 92 the bootstrap runs 4 steps:
- m2 = 82 → K ≥ 2.74e19
- m2 = 86 → 7.77e19
- m2 = 88 → 2.06e20
- m2 = 91, with d = 3.19e-42

The interval (δ, δ + 3.19e-42) contains 325919355854421968365/205632218873398596256, whose denominator is the
current floor. At m = 91 the same step has d = 1.23e-43 and jumps to 7.94e21 > K2(91). The difference is the
factor δ in the ceiling (K2 grows by about 1.6 per unit of m) against a lower bound that can only jump between
the sparse denominators of best approximations of δ.

The exploratory enumeration shows that the m = 92 shape satisfies Hercher's inequality with margin (ratio
0.196). So no refinement of the iteration can remove it: one needs either a larger X0 or a new inequality.

**X0 at which the bootstrap would exclude m** (`needed`; checked monotone on a grid):

| m | 92 | 93 | 94 | 95 | 96 | 97 | 98 | 99 | 100 | 101 | 102 | 110 | 120 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| X0/2^60 | 14 948 | 21 896 | 27 731 | 33 566 | 39 401 | 45 236 | 51 071 | 56 905 | 62 740 | 68 575 | 2.17e6 | 1.27e7 | 2.83e7 |
| log2 X0 | 73.87 | 74.42 | 74.76 | 75.04 | 75.27 | 75.47 | 75.64 | 75.80 | 75.94 | 76.07 | 81.05 | 83.60 | 84.75 |

Barina's range is about 2075·2^60, so m = 92 needs about 7.2 times the current range (2.85 more bits).

**By-product: lower bounds on K at X0 = 2^71** (Corollary-24 style; m-boundaries found by bisection
assuming monotonicity in m). Compare Hercher's Table 1 at 695·2^60.

| m range | K ≥ |
|---|---|
| 92 – 100 | 205 632 218 873 398 596 256 (2.06e20) |
| 101 – 124 | 77 692 117 359 936 589 403 (7.77e19) |
| 125 – 186 | 2.744e19 |
| 187 – 669 | 4.640e18 |
| 670 – 7 134 | 3.976e17 |
| 7 135 – 27 748 | 1.304e17 |

## 5. Comparison with the m ≥ 102 claim

Repository `justinalick/collatz-m-cycles-101-lean`, one commit (d1895945, 2026-09-28), Lean v4.35.0-rc3. I
read its README, the statement, the bootstrap script and three certificate files. I ran nothing from it.

**What it assumes.** The main theorem `no_101_cycle_2_71` has two hypotheses, given as parameters:
- `hX`: every 0 < n ≤ 2^71 reaches 1.
- `RhinBound`: SdW Lemma 12 for the cycle, i.e. Λ > exp(−13.3(0.46057 + log K)), stated as a Prop.

The README states that the proof uses no `sorry`, `axiom` or `native_decide`.

**What it does.**
1. It formalizes Hercher's m ≤ 91 with the repaired Theorem 21. Its ceiling is the Rhin bound K1(m), not SdW's
   K2(m).
2. It adds a new "two-rise bound": for an odd n < 2^N, the first two ascents have total length at most M(N),
   with M(74) ≤ 84, checked by a kernel-verified 2-adic computation.
3. It adds a "chain bound" on the growth of consecutive minima.
4. These exclude the shapes that survive the bootstrap for m = 92 … 101. The README calls this work new and
   says a paper is in preparation.

**Consistency with this run.**
- Its m = 92 file lists exactly one shape: K = 205 632 218 873 398 596 256, K+L = 325 919 355 854 421 968 365.
  That is our unique survivor.
- For m = 100 and 101 our 18 and 29 survivors are subsets of its 24 and 39 listed shapes. It lists more because
  it uses the larger ceiling K1, and because its bootstrap ε is about 1.4 times ours (apparently a more
  conservative formalised bound). Its floors are therefore lower (7.77e19 against our 2.06e20 at m = 100).
- Both computations agree that Hercher's method at 2^71 alone stops at 91.

**Assessment.** m ≥ 102 at 2^71 is not established by the refereed literature. It depends on a new, unrefereed
argument (two-rise plus chain), which I have not verified. A Lean kernel check is strong evidence if the
statement is faithful and the toolchain sound. I checked neither here; there was a reported Lean kernel
soundness incident in July/August 2026 (Lean kernel soundness bug 14576, post-mortem by L. de Moura dated 2026-08-01; seen only in a web search, not checked by me). The
right next step would be an audit like `notes/m2_audit.md`: rebuild, check the statement and replay with
`leanchecker`, and read the two-rise and chain argument mathematically. The shape lists computed here give an
independent target for that audit.

## 6. Caveats: what is assumed

- **Verified range.** 2^71 is Barina, J. Supercomput. 81:810 (2025), milestone 2025-01-15. 2075·2^60 is only on
  his project page (ongoing, no separate double-check stated). For this method the two give identical results.
- **Rhin's constant** enters only through A(m), via K1(m) < q_217 ≈ 1.31e106. For m ≤ 120, K1(m) < 1e28, so any
  effective irrationality measure of log2 3 gives the same K2(m) and the same conclusions.
  SdW's Lemma 12 uses 0.46057, which is marginally below log δ = 0.4605749 (a factor 1.00008 in the bound).
  This is irrelevant here.
- **Hercher's Corollary 19** is a computer proof (C++ on the JIS page) specific to 695·2^60. It is not needed
  at 2^71, nor for m ≤ 91 at 695·2^60 (Theorem 21 decides every step).
- **The corrigendum** leaves the Theorem 21 bound unchanged (§2).
- **Our own code.** Single implementation; Python plus mpmath. It was validated against the four sources
  above, with which it agrees to every printed digit apart from the explained discrepancies. The `survivors`
  extension combines published inequalities in a way neither paper does. It is used here only to show that
  the stall is genuine, not to claim a new bound.

## 7. Reproduce

```
.venv/bin/python mcycles.py validate                 # 55 s
.venv/bin/python mcycles.py run '2^71' 140           # also '2075*2^60', '695*2^60', '5*2^60', '301*2^50'
.venv/bin/python mcycles.py trace '2^71' 92          # bootstrap steps and blocking fraction
.venv/bin/python mcycles.py survivors '2^71' 92      # exploratory
.venv/bin/python mcycles.py lattice '5*2^60' 76      # SdW Lemma 18 list
.venv/bin/python mcycles.py needed 92 101            # least X0 for the bootstrap
```

Sources were downloaded to the session scratchpad (not in the repo):
- `hercher/`: arXiv v3 and JIS PDF/TeX, corrigendum, worksheet, C++ programs.
- `sdw/`: v1.44 and the Acta scan.
- `justinalick_repo/`: read-only copy of the key files.
