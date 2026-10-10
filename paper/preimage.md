# Uniform exponential bounds for the number of 3x+1 preimages

*Daniel Palmqvist, with Claude (Anthropic). Draft 0.2, 2026-10-10.*

## Abstract

For the 3x+1 map T(n) = n/2 (n even), (3n+1)/2 (n odd), let n_k(a) be the number of positive integers n with
T^k(n) = a. Averaged over residue classes a mod 3^{k+1}, a ≢ 0 (mod 3), the related pruned count has mean exactly
(4/3)^k. Applegate and Lagarias conjectured that n_k(a) = (4/3)^{k(1+o(1))} for every a ≢ 0 (mod 3). In 1995 they
proved (1.302053)^k ≤ n_k(a) ≤ (1.358386)^k for large k, by a search over all pruned trees of depth 30.

We prove, for every a ≢ 0 (mod 3) and every k ≥ 0,

  0.2847·(1.3331664)^k ≤ n_k(a),

with a proof machine-checked in Lean 4: the certificate is evaluated by the kernel itself and only the standard
axioms are used. For the pruned count N*_k(a) we prove, by exact integer computation,

  0.2822·(1.3333119)^k ≤ N*_k(a) ≤ 3.557·(1.3333567)^k.

So the uniform growth constant of n_k(a) is pinned to within 3·10^{−5} of 4/3.

The method is a residue-class version of the Krasikov–Lagarias difference inequalities, applied to depth instead of
size. It is a monotone, homogeneous recursion on the classes mod 3^r, and a single positive sub-eigenvector
certifies a bound valid for all a and all k. We also compute the exact extremal pruned-tree counts N^±(k) up to
depth 59 (N^−) and 55 (N^+). They sharpen the tree-search constants to 1.317329 and 1.346858, and they show
N^±(k)/(4/3)^k constant to within 0.7 % for k ≥ 25, as Conjecture C′ predicts and the random branching models do
not. Finally, the Perron vectors of the averaged recursion are the marginals of one measure on ℤ₃^×: the stationary
law of the walk x ↦ x/2, (3x+1)/2 with probabilities 3/4, 1/4. Krasikov–Lagarias's size-counting system is the
case 1/2, Tao's Syracuse random variable. Conjecture C′ follows if this measure has a continuous density, and the
numerics indicate that it does.

## 1. Introduction

Let T be the 3x+1 map above and a ≢ 0 (mod 3). (For 3 | a the predecessors are just {2^j a}.) Write
n_k(a) = #{n ≥ 1 : T^k(n) = a} for the number of k-step preimages.

Lagarias and Weiss [LW] showed that the average of n_k(a) over a grows like (4/3)^k, and they conjectured:

**Conjecture B** [AL1, (1.5)]. For each a ≢ 0 (mod 3), n_k(a) = (4/3)^{k(1+o(1))}.

The pruned tree T*_k(a) consists of the backward iterates of a that are ≢ 0 (mod 3): the children of n are 2n
always, and (2n−1)/3 when n ≡ 2, 8 (mod 9). Its structure depends only on a mod 3^{k+1}. Let N*_k(a) be its
number of nodes at depth k. Applegate and Lagarias [AL1] compute the extremes N^−(k) ≤ N*_k(a) ≤ N^+(k) over all
classes, for k ≤ 30. Their Theorem 2.1 (concatenating trees) turns depth-30 extremes into

  (1.302053)^k ≤ n_k(a) ≤ (1.358386)^k   for all large k   [AL1, Thm 1.1].

They also formulate **Conjecture C**: N^±(k) = (4/3)^{k(1+o(1))}, i.e. even the extremal trees grow at rate 4/3.
And the stronger **Conjecture C′**: C^−(4/3)^k ≤ N^−(k) ≤ N^+(k) ≤ C^+(4/3)^k. They note that C′ fails for
branching-process models.

These constants appear not to have been improved since; the surveys [L, KL2] still quote them. We give two
improvements.

**Theorem 1 (machine-checked).** For every a ≥ 1 with 3 ∤ a and every k ≥ 0,

  0.2847·(1.3331664)^k ≤ #{n ∈ [1, 2^k a] : T^k(n) = a} = n_k(a).

In particular n_k(a) ≥ (1.333)^k for all k ≥ 20200.

**Theorem 2 (exact computation).** For every a ≢ 0 (mod 3) and every k ≥ 0,

  0.2822·(1.3333119)^k ≤ N*_k(a) ≤ 3.557·(1.3333567)^k.

Since N*_k(a) ≤ n_k(a), and n_k(a) ≤ (k+1)·N*_k(a) for a not on a cycle [AL1, §2], it follows that
(1.3333119)^k ≤ n_k(a) for all large k, uniformly in a; and n_k(a) ≤ (1.3333567 + ε)^k for a not on a cycle.

**Theorem 3 (exact extremal trees).** N^−(k) is computed exactly for k ≤ 59 and N^+(k) for k ≤ 55 (Table 2).
Consequently (1.317329)^k ≤ n_k(a) ≤ (1.346858)^k for all large k, by the method of [AL1]. For 25 ≤ k ≤ 59,
(4/3)^k/N^−(k) ∈ [2.0334, 2.0475]; for 25 ≤ k ≤ 55, N^+(k)/(4/3)^k ∈ [1.7376, 1.7483].

Theorem 1 is weaker than Theorem 2 only because its certificate is smaller (r = 14 instead of r = 19), so that the
Lean kernel can evaluate it. Both rest on the same short argument (§3).

The point of the argument is that it never concatenates trees. The extremal-tree method loses a constant factor
at every concatenation, so its constants approach 4/3 only like 1/k. Tracking the residue class of every node
instead loses only the "top digit" information that a finite modulus cannot see. That loss shrinks geometrically,
by a factor of about 0.65 per additional digit.

The construction is the depth analogue of the Krasikov–Lagarias system for π_a(x) [Kr, KL]. There the
corresponding loss shrinks by only about 0.93 per digit, and whether it tends to zero is open [P1].

**Relation to positive density.** A recent formalisation [M] proves that the predecessor set of every a ≢ 0
(mod 3) has positive lower density. That concerns predecessors of any depth below a size bound, and its
constants are ineffective and depend on a. Conjecture B and C′ concern exact depth and uniformity in a, and remain
open. The bounds here are explicit and uniform.

## 2. The pruned recursion

For b ≢ 0 (mod 3) let β(b) = [b ≡ 2, 8 (mod 9)]. Since T(2b) = b, and T((2b−1)/3) = b for b ≡ 2 (mod 3), and
(2b−1)/3 ≢ 0 (mod 3) iff b ≢ 5 (mod 9):

  N*_0(b) = 1,   N*_{k+1}(b) = N*_k(2b) + β(b)·N*_k((2b−1)/3).                                     (2.1)

The depth-k nodes are distinct integers n with T^k(n) = a, so N*_k(a) ≤ n_k(a). Every such n satisfies
n ≤ 2^k a, because n ≤ 2T(n).

## 3. The residue-class bound

Fix r ≥ 2 and M = 3^r. On the classes c mod M with c ≢ 0 (mod 3), define:
- β(c) = [c ≡ 2, 8 (mod 9)];
- the three lifts l_u(c) = (2c−1)/3 + u·3^{r−1} mod M (u = 0, 1, 2), with c the representative in [0, M);
- Φ(v)(c) = v(2c mod M) + β(c)·min_u v(l_u(c)),   Ψ(v)(c) = v(2c mod M) + β(c)·max_u v(l_u(c)).

**Theorem 4.** If V > 0 satisfies Φ(V) ≥ μV, then N*_k(b) ≥ (V_min/V_max)·μ^k for every b ≢ 0 (mod 3) and every
k ≥ 0. If V′ > 0 satisfies Ψ(V′) ≤ μ′V′, then N*_k(b) ≤ (V′_max/V′_min)·μ′^k.

*Proof.* Let b ≡ c (mod M). Then:
- 2b ≡ 2c (mod M);
- β(b) = β(c), because 9 | M;
- (2b−1)/3 is congruent mod M to one of the lifts l_u(c), with u determined by b mod 3^{r+1}.

Hence, by (2.1), φ_k(c) := inf{N*_k(b) : b ≡ c} satisfies φ_{k+1} ≥ Φ(φ_k). Φ is monotone and positively
1-homogeneous, and φ_0 = 1 ≥ V/V_max. Induction gives φ_k ≥ μ^k V/V_max ≥ (V_min/V_max) μ^k. The upper bound is
identical, with sup and Ψ. ∎

In the formal proof the infimum is avoided. One proves directly, by induction on k over all b, that
P^k·V(b mod M) ≤ V_max·Q^k·N*_k(b) for μ = P/Q, in natural-number arithmetic.

**The summed identity.** The doubling map c ↦ 2c is a permutation of the units mod M; 2 is a primitive root, so it
is a single cycle. The map c ↦ (2c−1)/3 is a bijection from the classes with β = 1 onto the units mod 3^{r−1}.
Summing Φ(v) = μv over all classes therefore gives exactly

  μ = 1 + ρ/3,   ρ = 3·Σ_s min_u v(lifts of s) / Σ_c v(c) ≤ 1,

so μ_r ≤ 4/3, with equality iff v is constant over the top digit. Similarly μ′_r = 1 + ρ′_r/3 ≥ 4/3. This is the
depth analogue of the Krasikov–Lagarias summed inequality [KL, §6], with the ceiling 4/3 in place of λ = 2.

Since c ↦ 2c is a single cycle with positive weight in every row, Φ and Ψ are irreducible in the sense used in
[P1]. We expect that argument to transfer: optimal vectors tight and unique, μ_r strictly increasing and μ′_r
strictly decreasing in r. The tiling and descent steps have not been written out for this system. Numerically
both monotonicities hold for r ≤ 19 (Table 1).

## 4. Certificates

For each r the vectors V, V′ are found by power iteration in floating point, then rounded to integers.
μ = P/10^7 is rounded down (μ′ rounded up), and Q·Φ(V) ≥ P·V (resp. Q·Ψ(V′) ≤ P′·V′) is checked exactly for every
class:
- in int64 for r ≤ 17;
- in 128-bit integers for r = 18, 19, with an overflow guard proved separately in Python integers;
- with plain Python integers for r ≤ 7, together with negative tests at μ ± 2·10^{−4}.

Floating point is used only to find V.

**Table 1.** Certified constants (numpy rows r ≤ 17; C helper r = 18, 19, with a 10^{−6} margin for float32).

| r | classes | μ_r (lower) | V_min/V_max | μ′_r (upper) | V′_max/V′_min | 4 − 3μ_r | 3μ′_r − 4 |
|---|---|---|---|---|---|---|---|
| 2 | 6 | 1.2498514 | 0.5122 | 1.4036023 | 2.7652 | 2.50e-01 | 2.11e-01 |
| 4 | 54 | 1.3215670 | 0.3568 | 1.3590472 | 3.5374 | 3.53e-02 | 7.71e-02 |
| 6 | 486 | 1.3286744 | 0.3188 | 1.3419976 | 3.6190 | 1.40e-02 | 2.60e-02 |
| 8 | 4 374 | 1.3312913 | 0.3003 | 1.3363612 | 3.5683 | 6.13e-03 | 9.08e-03 |
| 10 | 39 366 | 1.3324253 | 0.2915 | 1.3345123 | 3.5693 | 2.72e-03 | 3.54e-03 |
| 12 | 354 294 | 1.3329407 | 0.2872 | 1.3338053 | 3.5721 | 1.18e-03 | 1.42e-03 |
| 14 | 3 188 646 | 1.3331663 | 0.2848 | 1.3335267 | 3.5689 | 5.01e-04 | 5.80e-04 |
| 16 | 28 697 814 | 1.3332617 | 0.2831 | 1.3334139 | 3.5613 | 2.15e-04 | 2.42e-04 |
| 17 | 86 093 442 | 1.3332864 | 0.2828 | 1.3333857 | 3.5592 | 1.41e-04 | 1.57e-04 |
| 18 | 258 280 326 | 1.3333013 | 0.2824 | 1.3333685 | 3.5577 | 9.61e-05 | 1.06e-04 |
| 19 | 774 840 978 | 1.3333119 | 0.2822 | 1.3333567 | 3.5561 | 6.43e-05 | 7.01e-05 |

**Independent checks.** A second implementation, written separately, certifies r = 13 (μ ≥ 1.333075,
μ′ ≤ 1.333637) and r = 16 (μ ≥ 1.333259, μ′ ≤ 1.333416). The bounds of Theorem 2 are also consistent with every
exact extremal count of §6.

**Observations.**
- Both losses decay geometrically. Successive ratios of 4 − 3μ_r for r = 10 … 17 are 0.663, 0.653, 0.653, 0.652,
  0.654, 0.656, 0.655; those of 3μ′_r − 4 rise slowly, 0.630 … 0.650.
- The certificate spreads stay bounded, near 3.5. The Krasikov–Lagarias vectors' spread grows like 1.52^k [P2].
- If both trends persist, μ_r, μ′_r → 4/3 with bounded constants, which is Conjecture B uniformly in a. Letting
  r → ∞ at fixed k would then give Conjecture C′.

## 5. Formalisation

Theorem 1 is proved in Lean 4 with Mathlib (`lean_formal/PreimageBound/`). The statement uses only Mathlib
notions, with T written out:

```lean
theorem PreimageBound.preimage_count_lower_bound (a : ℕ) (ha : 0 < a) (ha3 : a % 3 ≠ 0) (k : ℕ) :
    (2847 / 10000 : ℝ) * (13331664 / 10000000 : ℝ) ^ k ≤
      ((Finset.Icc 1 (2 ^ k * a)).filter
        (fun n => (fun m : ℕ => if m % 2 = 0 then m / 2 else (3 * m + 1) / 2)^[k] n = a)).card
```

The development contains:
- the pruned count as a set cardinality, and its recursion (2.1);
- the inequality N*_k ≤ n_k, and the window lemma;
- Theorem 4 for general r;
- the r = 14 certificate (3 188 646 classes in 729 chunks of 3^8 residues), evaluated by the kernel with
  `decide +kernel`. There is no `native_decide`.

The main theorem depends only on `propext`, `Classical.choice` and `Quot.sound`; the chunk checks depend on no
axioms. Every module passes `leanchecker`. The exported closures (up to 23 481 declarations) also pass the
independent Rust kernel nanoda. Lean versions before 4.32.2 had a kernel soundness bug that used
`addDecl`-injected inductives; this development uses none, and nanoda re-checks everything regardless. The r = 14
build takes about 39 minutes, with at most 2.7 GB per process.

## 6. Exact extremal trees

N^−(k) and N^+(k) are computed by a depth-first branch and bound over the ternary digits of a, from the lowest
digit up:
- each tree is decomposed into doubling chains, whose branch points depend only on the chain start mod 9;
- subtrees within 18–19 levels of the leaves are bounded by exhaustive min/max tables;
- deeper subtrees are bounded by the class optima already computed.

The computation is validated in several ways:
- it reproduces the values printed in [AL1] at k = 30: g^−(30) = 1.302053, g^+(30) = 1.358386 and
  γ*_30 = 0.654717;
- it agrees with two independent brute forces (k ≤ 13) and with an unpruned enumeration (k ≤ 36, where
  Σ N*_k = 2·4^k);
- runs with different table depths and code versions agree;
- every optimum has a witness class, recounted from the definition.

**Table 2.** Selected exact extremal counts (full table in the accompanying notes).

| k | N^−(k) | (4/3)^k/N^−(k) | N^+(k) | N^+(k)/(4/3)^k |
|---|---|---|---|---|
| 30 | 2 747 | 2.0385 | 9 788 | 1.7480 |
| 35 | 11 577 | 2.0383 | 41 120 | 1.7426 |
| 40 | 48 687 | 2.0424 | 173 184 | 1.7416 |
| 45 | 205 479 | 2.0393 | 730 004 | 1.7421 |
| 50 | 865 998 | 2.0390 | 3 075 968 | 1.7420 |
| 55 | 3 648 795 | 2.0393 | 12 962 760 | 1.7421 |
| 59 | 11 533 924 | 2.0390 | – | – |

The normalised extremes are essentially constant, near 2.039 and 1.742. For the random branching models of [AL1]
both diverge, so this is further evidence that 3x+1 trees are much more rigid than random ones.

Optimality of N^±(k) for k > 19 rests on the search code and its cross-checks, not on an independent certificate.
Theorems 1 and 2 do not depend on Theorem 3.

## 7. The limit measure

Replace the minimum in Φ by the mean over the three lifts: A_r v(c) = v(2c) + β(c)·(1/3)Σ_u v(l_u(c)). Let h_r be
the Perron vector of A_r, normalised to mean 1 over the classes.

**Proposition 5.** Let r ≥ 3.
- (a) A_r is primitive with Perron root 4/3. The mean of h_r over the three lifts of s (mod 3^{r−1}) is h_{r−1}(s).
- (b) There is a unique probability measure ν on ℤ₃^× whose density, relative to normalised Haar measure, has
  average h_r(c) on every ball c + 3^r ℤ₃. ν is the stationary law of the Markov chain on ℤ₃^× that maps x to x/2
  with probability 3/4 and to (3x+1)/2 with probability 1/4. Equivalently, ν is the law of
  X = Σ_{j≥1} 3^{j−1} 2^{−S(j)}, with S(j) = a_1 + ⋯ + a_j, a_j i.i.d. and P(a_j = m) = (1/4)(3/4)^{m−1}.
- (c) For every class c mod 3^r, the average of (3/4)^k N*_k(b) over the classes b mod 3^{k+1} with b ≡ c (mod 3^r)
  tends to h_r(c) as k → ∞.

*Proof.*
- (a), Perron root. Summing A_r v over all classes gives (4/3)Σ_c v(c), as in the summed identity of §3. So the
  all-ones row vector is a positive left eigenvector. The cycle c ↦ 2c makes A_r irreducible. The class c ≡ −1 has a
  self-loop, because (2·(−1)−1)/3 = −1, so A_r is primitive and its Perron root is 4/3.
- (a), consistency. Averaging over the top digit commutes with A_r. The doubling term maps the fibres of reduction mod 3^{r−1} onto
  fibres, and β depends only on c mod 9. As the top digit of c runs through 0, 1, 2, the class (2c−1)/3 mod 3^{r−1}
  runs through the three lifts of (2s−1)/3 mod 3^{r−2}, where s ≡ c (mod 3^{r−1}). So the top-digit average of h_r
  is a positive eigenvector of A_{r−1}, and by uniqueness it equals h_{r−1}.
- (b) Existence and uniqueness follow from (a) by Kolmogorov's extension theorem. The map x ↦ x/2 permutes the
  balls of each level. The map x ↦ (3x+1)/2 sends the ball s + 3^{r−1}ℤ₃ onto a level-r ball contained in
  {c ≡ 2, 8 (mod 9)}, and its inverse there is c ↦ (2c−1)/3. So A_r h_r = (4/3)h_r is the stationarity equation on
  level-r balls. Unrolling the x/2 steps gives the series.
- (c) Let g_k(c) be the class average. By (2.1), b ↦ 2b maps class c onto class 2c, and b ↦ (2b−1)/3 maps class c
  onto the union of the three lifts l_u(c). Hence g_{k+1} = (3/4)A_r g_k with g_0 = 1, and primitivity gives
  g_k → h_r, normalised by the left eigenvector. ∎

So the normalised pruned counts (3/4)^k N*_k(b) converge weakly to the measure ν. Conjecture C′ asks for uniform
control.

**Proposition 6.** Suppose h_r converges uniformly on ℤ₃^×, i.e. ν has a continuous density h. Let S = max h/min h.
Then for every b ≢ 0 (mod 3) and k ≥ 1,

  (4S)^{−1}(4/3)^k ≤ N*_k(b) ≤ e^{3/4}S·(4/3)^k,

so Conjecture C′ holds.

*Proof.*
- h is positive. The limit equation h(x) = (3/4)(h(2x) + β(x)h((2x−1)/3)) gives h(x) ≥ (3/4)h(2x). So a zero of h
  propagates along the orbit x·2^j, which is dense because 2 generates ℤ₃^× topologically, and then h ≡ 0.
- Ball averages lie between min h and max h, so V_min/V_max ≥ 1/S for V = h_r.
- Φ(h_r) = (4/3)h_r − β·(mean − min over lifts). So Theorem 4 applies with μ = 4/3 − δ_r, where
  δ_r ≤ ‖h_r − h_{r−1}‖_∞/min h → 0.
- Given k, choose r with δ_r ≤ 1/k. Then (4/3 − δ_r)^k ≥ (4/3)^k(1 − 3/(4k))^k ≥ (4/3)^k/4.
- The upper bound is the same argument with Ψ and (1 + 3/(4k))^k ≤ e^{3/4}. ∎

**Evidence for continuity.** The marginals h_r are computed exactly from h_r(c) = (3/4)h_r(2c) + (3/4)β(c)·
h_{r−1}((2c−1)/3), solved along the doubling cycle (35 s for r = 17). Write δ_r = h_r − h_{r−1} (a martingale
difference). Then

  δ_r(c) = Σ_{j≥0} (3/4)^{j+1} β(2^j c)·δ_{r−1}((2^{j+1}c − 1)/3).

The diagonal part of E[δ_r²] is exactly (3/7)E[δ_{r−1}²]. The off-diagonal part consists of correlations between
δ_{r−1}(y) and δ_{r−1}(2^d(y + 1/3) − 1/3), d even, and numerically they vanish:
- ‖δ_r‖_2/‖δ_{r−1}‖_2 = 0.6467, 0.6477, 0.6491, 0.6503, 0.6514, 0.6519 for r = 12 … 17, against √(3/7) = 0.6547.
  This is the observed decay 0.65 of 4 − 3μ_r in Table 1.
- The L^q norms decay at nearly the same rate: 0.6525, 0.658, 0.668 for q = 4, 6, 8 at r = 17. These are below
  3^{−1/q} (0.760, 0.833, 0.872), which is what Σ_r ‖δ_r‖_∞ ≤ Σ_r (2·3^{r−1})^{1/q}‖δ_r‖_q < ∞ requires.
- The sup ratio is ≈ 0.76, so the density appears Hölder continuous with exponent ≈ 0.25.
- The extremes match the extremal trees of §6. At r = 17, 1/min h_17 = 2.0387 and max h_17 = 1.7386, both still
  rising slowly. Table 2 gives (4/3)^k/N^−(k) → 2.0390–2.0395 and N^+(k)/(4/3)^k → 1.7420.

So, numerically, N^±(k)(3/4)^k → max h and min h, and the Conjecture C′ constants are the extremes of a single
continuous function on ℤ₃^×.

**Relation to the Syracuse random variable.** For general p the chain x ↦ x/2 (probability 1 − p),
x ↦ (3x+1)/2 (probability p) has the stationary law X_p = Σ_{j≥1} 3^{j−1}2^{−S(j)}, with S(j) = a_1 + ⋯ + a_j and P(a = m) = p(1−p)^{m−1}.
- p = 1/2 is Tao's Syracuse random variable Syrac(ℤ₃) [T, Remark 1.13].
- The Krasikov–Lagarias system at λ = 2 with min replaced by mean has as Perron vector exactly the density of X_{1/2}
  on the classes ≡ 2 (mod 3). So counting by size [KL] is the case p = 1/2, and counting by depth is p = 1/4.
- The diagonal L² coefficient is 3p/(2−p). It is < 1 exactly for p < 1/2.
- The density near −1, the fixed point of x ↦ (3x+1)/2, grows by a factor 3p per level, so it is unbounded for
  p > 1/3.

At p = 1/2 both effects bite. The diagonal factor is exactly 1, the density is unbounded on every ball (spread
~1.6^r, the source of the 1.52^k growth of the Krasikov–Lagarias certificates [P2]), and the L¹ decay, which Tao
proves is faster than any power [T, Prop. 1.14], comes entirely from cancellation. Its ratio per level creeps up,
0.926 … 0.931 for r = 14 … 17, like the ratio of 1 − ρ_k in [KL]'s problem (0.919 at k = 14, 0.933 at k = 22 [P2]).
The depth problem sits on the subcritical side, which is why it is so much better behaved.

Wirsching [W] studies a 3-adic Markov process for the inverse 3x+1 map (cf. [T, footnote 5]). We have not checked
whether Proposition 5 appears there.

## 8. Remarks

1. **What would prove Conjecture B.** Prove ρ_r → 1 for the system of §3, i.e. that the Perron vector becomes
   insensitive to its top digit. This is a cleaner instance of the Krasikov–Lagarias problem λ_k → 2 [KL, P1]. Here
   the loss decays 0.65 per digit instead of 0.93, and the spread stays bounded instead of growing exponentially.
   By Proposition 6, Conjecture C′ (hence B) follows from continuity of the density of the stationary measure ν of
   §7. One route is a moment recursion for the martingale differences δ_r: the diagonal coefficients are exact, and
   a bound ‖δ_r‖_4 ≤ Cθ^r with θ < 3^{−1/4} suffices. What must be controlled is the decorrelation of δ_{r−1} under
   the maps y ↦ 2^d(y + 1/3) − 1/3.
2. **Novelty.** We have not found improvements of [AL1, Thm 1.1] in the literature. The surveys [L, KL2] still
   state the tree-growth constant log(4/3) as conjectural. The residue-class system is the evident depth analogue of
   Krasikov's inequalities, so special cases may exist; we would be glad to learn of them.

## References

- [AL1] D. Applegate, J. C. Lagarias, Density bounds for the 3x+1 problem I. Tree-search method, Math. Comp. 64
  (1995) 411–426.
- [Kr] I. Krasikov, How many numbers satisfy the 3x+1 conjecture?, Internat. J. Math. Math. Sci. 12 (1989)
  791–796.
- [KL] I. Krasikov, J. C. Lagarias, Bounds for the 3x+1 problem using difference inequalities, Acta Arith. 109
  (2003) 237–258.
- [KL2] A. V. Kontorovich, J. C. Lagarias, Stochastic models for the 3x+1 and 5x+1 problems, in: The Ultimate
  Challenge: The 3x+1 Problem, AMS, 2010; arXiv:0910.1944.
- [L] J. C. Lagarias, The 3x+1 problem: an overview, arXiv:2111.02635.
- [LW] J. C. Lagarias, A. Weiss, The 3x+1 problem: two stochastic models, Ann. Appl. Probab. 2 (1992) 229–261.
- [M] L. Mazur, Positive lower density of Collatz predecessors, ProofAtlas Lean formalisation, September 2026.
- [P1] D. Palmqvist, The Krasikov–Lagarias exponents for the 3x+1 problem are attained and strictly increasing,
  draft, 2026.
- [P2] D. Palmqvist, Certified Krasikov–Lagarias predecessor bounds for the 3x+1 problem to k = 22, draft, 2026.
- [T] T. Tao, Almost all orbits of the Collatz map attain almost bounded values, Forum Math. Pi 10 (2022) e12;
  arXiv:1909.03562.
- [W] G. J. Wirsching, The Dynamical System Generated by the 3n+1 Function, Lecture Notes in Math. 1681, Springer,
  1998.
