# Extremal 3x+1 trees beyond depth 30, and sharper constants in Applegate–Lagarias Theorem 1.1

Avenue 15. Night run 2026-10-10 (M4 Pro 64 GB, shared with other jobs). Code: `extremal_trees.py` (driver,
validation, reports, residue-class certificates) and `extremal_trees_core.c` (the branch-and-bound search,
compiled by the driver). Nothing else in the repository was changed.

Reference: D. Applegate, J. C. Lagarias, "Density bounds for the 3x+1 problem I. Tree-search method",
Math. Comp. 64 (1995) 411–426 ("A–L" below).

## 0. Summary

1. **Exact extremal counts far past depth 30.** N^−(k) is exact for every k ≤ 59 and N^+(k) for
   every k ≤ 55. A–L computed k ≤ 30 in 1993. The method is a branch and bound over the ternary digits of a,
   with exact table bounds (§2). The weight vectors w^±(k) are exact for k ≤ 45.
2. **Validation.** The k = 30 values A–L print are reproduced: g^−(30) = 1.302053 and g^+(30) = 1.358386
   (Theorem 1.1), and γ*_30 = 0.654717 (Theorem 1.2, which depends on all of w^−(30)). These printed digits
   force N^−(30) = 2747 and N^+(30) = 9788. Small k are checked against two independent brute forces and an
   unpruned enumeration (k ≤ 36). Different table depths and two code versions agree. Every extremal
   value has a witness residue a, recounted from the definition.
   Caveat: A–L's Tables 2.1/2.2 are not in the available PDF, so the k ≤ 29 entries were not compared one by
   one (§8).
3. **Theorem 1.1 from the extremal trees** (Theorem 2.1 with the best k): for every a ≢ 0 (mod 3) and all
   large k,
   (**1.317329**)^k ≤ n_k(a) ≤ (**1.346858**)^k, from k = 59 and k = 55,
   against A–L's (1.302053)^k and (1.358386)^k.
4. **Much sharper, and new as far as I can tell: residue-class certificates** (§5.2). These are the depth
   analogue of the Krasikov–Lagarias system: one exact integer inequality per class mod 3^r. With r = 19
   they give, for every a ≢ 0 (mod 3) and every k ≥ 0,
   **0.2822·(1.333311)^k ≤ N*_k(a) ≤ 3.557·(1.333357)^k**.
   So (1.333311)^k ≤ n_k(a) ≤ (1.333357)^k for all large k, and for a off cycles the constants do not depend
   on a. This pins the growth constant of Conjecture B, n_k(a) = (4/3)^(k(1+o(1))), to within 2.3·10^−5 of
   4/3 on either side. The losses
   4 − 3μ_r and 3μ′_r − 4 fall geometrically, by a factor of about 0.65 per digit, while the analogous K–L
   loss 1 − ρ_k falls by only about 0.93 per digit.
5. **Conjecture C′ evidence.** For 25 ≤ k ≤ 59, (4/3)^k/N^−(k) stays in [2.0334, 2.0475]. For
   25 ≤ k ≤ 55, N^+(k)/(4/3)^k stays in [1.7376, 1.7483]. There is no drift. The random branching models
   predict that both diverge. The normalised extremes look convergent, to about 2.04 and 1.74.
6. The tree-search exponent of A–L Theorem 1.2 improves from γ*_30 = 0.654717 to γ*_45 = 0.722362.
   This is of historical interest only.

## 1. Objects (A–L §2)

For a ≢ 0 (mod 3), T*_k(a) is the depth-k tree of backward iterates of T restricted to n ≢ 0 (mod 3):
the children of n are 2n always, and (2n−1)/3 when n ≡ 2, 8 (mod 9) (A–L (2.2); checked against the paper).
Leaves are the nodes at depth exactly k. The weight of a leaf is its number of (2n−1)/3 edges. The structure
depends only on a mod 3^(k+1).

- w_kj(a) = number of leaves of weight j; N*_k(a) = Σ_j w_kj(a).
- N^−(k), N^+(k) = min, max of N*_k(a) over a mod 3^(k+1), a ≢ 0 (mod 3); g^±(k) = N^±(k)^(1/k).
- w^−(k), w^+(k) are the minorizing and majorizing vectors, defined by the min/max of the tail sums
  Σ_{j ≥ τ} w_kj(a) (A–L (2.9)–(2.10)).
- Theorem 2.1: for every k, g^−(k) ≤ liminf N*_j(a)^(1/j) ≤ limsup ≤ g^+(k), and the same for n_j(a).
  A–L used k = 30 to get Theorem 1.1, (1.302053)^k ≤ n_k(a) ≤ (1.358386)^k for large k.

Root classes. If a ≡ 1 (mod 3) the root does not branch, and 2a runs over all classes ≡ 2 (mod 3).
Every statistic of class 1 at depth k is therefore the class-2 statistic at depth k−1. The search only
optimises over a ≡ 2 (mod 3) ("L2(k)" below). Empirically, for every k ≥ 2 the minimum N^−(k) is attained in
class 1, so N^−(k) = L2_min(k−1), and the maximum is attained in class 2, so N^+(k) = L2_max(k).

## 2. Method

### 2.1 Chain decomposition
Call a node a *head* if it is the root or an odd child (2n−1)/3. A head h at depth d starts the doubling chain
h, 2h, …, 2^(k−d)h. All nodes of a chain have the same weight, and the chain ends in exactly one leaf at
depth k. Hence

  #leaves of weight ≥ τ = #heads of weight ≥ τ,  and  N*_k(a) = #heads.

The chain node 2^i h (depth < k) branches iff 2^i h ≡ 2, 8 (mod 9). This depends only on h mod 9, because 2 has
order 6 mod 9. So a head's chain, and the positions and classes mod 3 of the heads it spawns, are fixed by
h mod 9.

### 2.2 State: digits of a revealed from the bottom
Write a = A + 3^J·T with A = a mod 3^J known. A head of weight w at depth d equals

  h = (2^d a − s)/3^w = h_A + 3^(J−w)·2^d·T,

so it is known mod 3^(J−w). Revealing digit J of a (T ↦ t + 3T′) adds t·3^(J−w)·2^d to every head. After J
digits, every head of weight ≤ J−1 exists and is located. The heads of weight J−1 are known mod 3. Those
with remaining depth m > M are called *active*; the others are kept lazy (§2.3). Revealing digit J makes the
active heads known mod 9, which fixes their chains and creates the weight-J heads. A search node is
therefore:

- the exact count C of finished heads,
- the active heads (depth d and an exact representative h mod 3^(k−d+1), with the unknown digits of a set to 0),
- the lazy heads (below).

Revealing a digit updates every head by an exact integer increment. No floating point is used anywhere in the
search.

### 2.3 Lazy heads and table bounds
A head whose remaining depth m = k − d is at most M (the table depth, 18 or 19 in the long runs) is not
expanded. It is kept as a *lazy* head (m, w, residue). Its exact contribution is f_{m,τ′}(h), the number of
heads of relative weight ≥ τ′ in T*_m(h). This is a function of h mod 3^(m+1). With s known digits it lies
between the min and the max of f_{m,τ′} over the residue class mod 3^s. Both are read from exhaustive tables:
f_m is computed for every residue mod 3^(m+1) by the A–L recursion f_m(n) = f_{m−1}(2n) + [n ≡ 2,8 (9)]
f_{m−1}((2n−1)/3), and then reduced to min/max pyramids over all levels s ≤ m+1. A lazy head is resolved
(added to C) when s = m+1, or as soon as min = max on its class.

Active heads (m > M) are bounded by the class extrema L_{m,τ′}(h mod 3), which are exact results of the
search at smaller depths. This is why depths are processed in increasing order.

Each search node has an exact part C plus, for every pending head, a valid lower bound (min search) or upper
bound (max search). The depth-first search reveals one digit per level. It visits the most promising child
first and discards a child when its bound cannot beat the incumbent (≥ incumbent for the min, ≤ for the max).
A node with no pending heads is a fully determined tree with exactly C heads.

**Why this is exact.** The search tree is the ternary tree of residue classes of a. Every class is either
(a) explored until its tree is determined, which gives its exact value, or (b) discarded because a valid bound
shows that no member of the class beats a value that is actually attained. So the final incumbent is the exact
optimum. Merging is implicit: a class whose tree is already determined is not split further, which is
A–L's "clone". The tables replace the A–L hashtable of depth-(k−1) clones.

### 2.4 Implementation notes
- Tables are stored in "trie order" (level s holds residues mod 3^s at digit-reversed index), so the three
  refinements of a class are adjacent. A lazy head is stored as (index, high part). One digit step is an
  addition, a conditional subtraction and a division by 3, with no variable divisions.
- The min and max pyramids share the top level. Tables: M = 18 needs 7.0 GB and builds in 10 s; M = 19 needs
  20.9 GB and builds in 31 s. With a MAXLOG argument (`search … 2 MAXLOG`), one process builds the tables,
  then forks into a min and a max process that share them copy-on-write.
- Parallelism: all prefixes of J0−1 digits (3^8 or 3^9) are bounded and sorted, then threads take them
  dynamically. The incumbent is a shared atomic.
- Representatives of active heads are `unsigned __int128` (k ≤ 76). Children use exact division by 3
  (multiplication by 3^(−1) mod 2^128).
- A witness residue a is printed for every class optimum (`W` lines). The driver recounts N*_k(a) for it from
  the definition, using actual integers.

### 2.5 A remark on the A–L clone criterion
A–L (end of §2) state that all trees T*_k(a′) with a′ ≡ a (mod 3^(mw_k(a)+1)) coincide, where mw_k(a) is the
maximum leaf weight. As printed this is off by one digit when a maximal-weight node at depth k−1 is ≡ 5
(mod 9). Example: k = 1, a ≡ 5 (mod 9) gives one leaf and mw = 0, but a + 3 ≡ 8 (mod 9) gives two leaves. Their
k = 30 values are reproduced exactly (§3), so their implementation must have keyed the clones correctly. Our
search does not use this criterion.

## 3. Validation

`python extremal_trees.py validate` (PASS, 46 s) runs every row below except three. The enumeration for
22 ≤ k ≤ 36, the long-run consistency check and the witness recount come from the night's logs (`report`).

| check | range | result |
|---|---|---|
| literal brute force (actual integers a < 3^(k+1), trees built from the definition) vs numpy residue recursion, all tail sums | k ≤ 10 | identical |
| numpy residue recursion vs C tables (all thresholds, min and max, both root classes) | k ≤ 13 | identical |
| A–L (2.8): Σ_a N*_m(a) = 2·4^m over all a mod 3^(m+1) | m ≤ 12 (tables) | exact |
| search with tiny tables (M = 4, 7, 12, all thresholds) vs exhaustive tables | k ≤ 14 | identical |
| search M = 10 vs M = 14 (different bound/pruning patterns) | 15 ≤ k ≤ 40 | identical |
| unpruned enumeration (no bounds at all): Σ_a N*_k(a) = 2·4^k over all 2·3^k classes, and its min/max per root class | 15 ≤ k ≤ 36 | exact; extremes = branch-and-bound values |
| long runs: M = 16 / 18 / 19 and code versions v1 (natural-order tables) vs v3+ (trie order); every overlapping (k, sense) | k ≤ 53 (min), ≤ 50 (max) | identical (the report refuses inconsistent logs) |
| witnesses: residue a printed by the search, N*_k(a) recounted from the definition with Python integers | every class optimum, 13 ≤ k ≤ 58 (min) and ≤ 55 (max) | all equal |
| **A–L k = 30**: g^−(30) = 2747^(1/30) = 1.3020529, g^+(30) = 9788^(1/30) = 1.3583858; A–L print 1.302053 and 1.358386 | k = 30 | **match**; the neighbours 2746, 2748, 9787, 9789 give 1.302037, 1.302069, 1.358381, 1.358391, so the printed digits pin N^−(30) = 2747 and N^+(30) = 9788 |
| **A–L Theorem 1.2**: γ*_30 from our w^−(30) through A–L (3.9) = 0.6547171; A–L print .654717 | k = 30 | **match** (tests the whole vector w^−(30)) |

w^−(30) = (1, 10, 43, 127, 265, 418, 510, 506, 402, 266, 134, 56, 9, 0, …, 0) (weights 0…30, sum 2747)
w^+(30) = (1, 10, 53, 174, 408, 708, 1053, 1310, 1382, 1279, 1025, 749, 517, 359, 251, 174, 111, 70, 50, 35, 24,
14, 10, 6, 5, 3, 2, 2, 1, 1, 1) (sum 9788)

As noted in §8, Tables 2.1/2.2 themselves were not available, so the k ≤ 29 entries could not be compared
one by one.

## 4. Results: exact extremal counts

N^−(k) = min and N^+(k) = max of N*_k(a) over all a mod 3^(k+1), a ≢ 0 (mod 3). Bold rows are new
(k > 30). Rows k ≤ 30 are the quantities of A–L Tables 2.1/2.2 (N^±) and Table 2.3 (the two ratios); only
k = 30 could be compared (§3). For k ≥ 2 the minimum is attained in class 1 (N^−(k) = L2_min(k−1)) and the
maximum in class 2. The last N^−(k) row comes from a cheap verification search (`ET_INIT_MIN`, §10, `V` line in
the log). It shows that no class-2 tree at that depth has fewer than L2_min(k−1) leaves, so the class-1 value is
the minimum.

| k | N^−(k) | g^−(k) | (4/3)^k / N^−(k) | N^+(k) | g^+(k) | N^+(k) / (4/3)^k |
|---|---|---|---|---|---|---|
| 1 | 1 | 1.000000 | 1.3333 | 2 | 2.000000 | 1.5000 |
| 2 | 1 | 1.000000 | 1.7778 | 3 | 1.732051 | 1.6875 |
| 3 | 1 | 1.000000 | 2.3704 | 4 | 1.587401 | 1.6875 |
| 4 | 2 | 1.189207 | 1.5802 | 6 | 1.565085 | 1.8984 |
| 5 | 2 | 1.148698 | 2.1070 | 8 | 1.515717 | 1.8984 |
| 6 | 3 | 1.200937 | 1.8729 | 10 | 1.467799 | 1.7798 |
| 7 | 4 | 1.219014 | 1.8729 | 14 | 1.457916 | 1.8688 |
| 8 | 5 | 1.222845 | 1.9977 | 18 | 1.435189 | 1.8020 |
| 9 | 6 | 1.220285 | 2.2197 | 24 | 1.423498 | 1.8020 |
| 10 | 9 | 1.245731 | 1.9731 | 32 | 1.414214 | 1.8020 |
| 11 | 11 | 1.243575 | 2.1525 | 42 | 1.404650 | 1.7739 |
| 12 | 16 | 1.259921 | 1.9731 | 55 | 1.396466 | 1.7422 |
| 13 | 20 | 1.259155 | 2.1046 | 74 | 1.392474 | 1.7580 |
| 14 | 27 | 1.265436 | 2.0786 | 100 | 1.389495 | 1.7818 |
| 15 | 36 | 1.269853 | 2.0786 | 134 | 1.386140 | 1.7907 |
| 16 | 48 | 1.273731 | 2.0786 | 178 | 1.382456 | 1.7840 |
| 17 | 64 | 1.277162 | 2.0786 | 237 | 1.379403 | 1.7815 |
| 18 | 87 | 1.281596 | 2.0388 | 311 | 1.375583 | 1.7533 |
| 19 | 114 | 1.283093 | 2.0746 | 413 | 1.373035 | 1.7463 |
| 20 | 154 | 1.286400 | 2.0476 | 548 | 1.370689 | 1.7378 |
| 21 | 206 | 1.288796 | 2.0410 | 736 | 1.369361 | 1.7505 |
| 22 | 274 | 1.290645 | 2.0460 | 988 | 1.368124 | 1.7624 |
| 23 | 363 | 1.292112 | 2.0591 | 1314 | 1.366442 | 1.7579 |
| 24 | 484 | 1.293804 | 2.0591 | 1744 | 1.364786 | 1.7499 |
| 25 | 649 | 1.295656 | 2.0475 | 2309 | 1.363129 | 1.7376 |
| 26 | 868 | 1.297239 | 2.0412 | 3084 | 1.362061 | 1.7406 |
| 27 | 1159 | 1.298627 | 2.0383 | 4130 | 1.361207 | 1.7483 |
| 28 | 1549 | 1.299961 | 2.0334 | 5500 | 1.360142 | 1.7461 |
| 29 | 2052 | 1.300807 | 2.0467 | 7336 | 1.359226 | 1.7468 |
| 30 | 2747 | 1.302053 | 2.0385 | 9788 | 1.358386 | 1.7480 |
| **31** | 3650 | 1.302905 | 2.0455 | 13022 | 1.357474 | 1.7441 |
| **32** | 4880 | 1.303957 | 2.0400 | 17342 | 1.356663 | 1.7420 |
| **33** | 6492 | 1.304748 | 2.0446 | 23126 | 1.355956 | 1.7423 |
| **34** | 8670 | 1.305642 | 2.0413 | 30824 | 1.355271 | 1.7417 |
| **35** | 11577 | 1.306480 | 2.0383 | 41120 | 1.354659 | 1.7426 |
| **36** | 15417 | 1.307174 | 2.0408 | 54824 | 1.354061 | 1.7425 |
| **37** | 20584 | 1.307922 | 2.0380 | 73124 | 1.353509 | 1.7431 |
| **38** | 27448 | 1.308588 | 2.0378 | 97508 | 1.352977 | 1.7433 |
| **39** | 36571 | 1.309192 | 2.0393 | 129908 | 1.352443 | 1.7419 |
| **40** | 48687 | 1.309741 | 2.0424 | 173184 | 1.351956 | 1.7416 |
| **41** | 64972 | 1.310339 | 2.0406 | 230886 | 1.351495 | 1.7414 |
| **42** | 86709 | 1.310910 | 2.0387 | 307858 | 1.351061 | 1.7415 |
| **43** | 115529 | 1.311405 | 2.0402 | 410642 | 1.350659 | 1.7422 |
| **44** | 154142 | 1.311920 | 2.0388 | 547508 | 1.350262 | 1.7422 |
| **45** | 205479 | 1.312386 | 2.0393 | 730004 | 1.349883 | 1.7421 |
| **46** | 273794 | 1.312819 | 2.0406 | 973178 | 1.349516 | 1.7418 |
| **47** | 365175 | 1.313261 | 2.0400 | 1297342 | 1.349165 | 1.7415 |
| **48** | 487043 | 1.313684 | 2.0394 | 1729858 | 1.348834 | 1.7416 |
| **49** | 649373 | 1.314082 | 2.0394 | 2306730 | 1.348519 | 1.7418 |
| **50** | 865998 | 1.314469 | 2.0390 | 3075968 | 1.348216 | 1.7420 |
| **51** | 1154737 | 1.314838 | 2.0389 | 4101504 | 1.347924 | 1.7421 |
| **52** | 1539255 | 1.315185 | 2.0394 | 5468458 | 1.347641 | 1.7420 |
| **53** | 2052206 | 1.315523 | 2.0395 | 7291108 | 1.347369 | 1.7420 |
| **54** | 2736843 | 1.315856 | 2.0391 | 9721632 | 1.347109 | 1.7420 |
| **55** | 3648795 | 1.316169 | 2.0393 | 12962760 | 1.346858 | 1.7421 |
| **56** | 4865777 | 1.316477 | 2.0390 | – | – | – |
| **57** | 6487462 | 1.316770 | 2.0391 | – | – | – |
| **58** | 8649454 | 1.317053 | 2.0392 | – | – | – |
| **59** | 11533924 | 1.317330 | 2.0390 | – | – | – |

## 5. Theorem 1.1 constants

### 5.1 From extremal trees (Theorem 2.1, as in A–L)
Theorem 2.1 holds for every k, so the best k gives the bound. g^−(k) is increasing for k ≥ 13 in our
data and g^+(k) is decreasing for k ≥ 2. Rigorous rounding (largest 6-decimal d with d^k ≤ N^−(k), smallest
with d^k ≥ N^+(k)):

  **(1.317329)^k ≤ n_k(a) ≤ (1.346858)^k** for every a ≢ 0 (mod 3) and all sufficiently large k
  (from N^−(59) and N^+(55)). A–L 1995: (1.302053)^k and (1.358386)^k (k = 30).

Because the ratios N^±(k)/(4/3)^k are essentially constant, g^±(k) ≈ (4/3)·C_±^(±1/k) approaches 4/3 only
like 1/k. About 0.0003 per k is gained at k ≈ 55, at a cost that doubles with each k. §5.2 removes this
limitation.

### 5.2 Much sharper: the residue-class (depth Krasikov–Lagarias) system
The extremal-tree bound loses a constant factor at every concatenation. N^−(k) ≈ (4/3)^k/2.04, so
g^−(k) ≈ (4/3)·2.04^(−1/k), which approaches 4/3 only like 1/k. Tracking the residue class of every node
removes that loss. This is the depth analogue of the Krasikov / Krasikov–Lagarias difference inequalities.
A–L II and K–L apply them to π_a(x), not to n_k(a).

**Theorem (residue-class bound).** Fix r ≥ 2. For a class c mod 3^r with c ≢ 0 (mod 3), put
β(c) = [c ≡ 2, 8 (mod 9)] and let l_t(c) = (2c−1)/3 + 2t·3^(r−1) mod 3^r (t = 0, 1, 2) be the three lifts.
For positive vectors v on these classes put

  Φ(v)(c) = v(2c) + β(c)·min_t v(l_t(c)),  Ψ(v)(c) = v(2c) + β(c)·max_t v(l_t(c)).

If V > 0 satisfies Φ(V) ≥ μV, then N*_n(a) ≥ (V_min/V_max)·μ^n for every a ≢ 0 (mod 3) and every n ≥ 0.
If V′ > 0 satisfies Ψ(V′) ≤ μ′V′, then N*_n(a) ≤ (V′_max/V′_min)·μ′^n for every a and n.

*Proof.* Let φ_n(c) = min{N*_n(b) : b ≡ c (mod 3^r)}. For b ≡ c, A–L's recursion gives
N*_{n+1}(b) = N*_n(2b) + β(b)·N*_n((2b−1)/3). Here β(b) = β(c) because r ≥ 2, 2b ≡ 2c, and
(2b−1)/3 ≡ l_t(c) (mod 3^r), with t fixed by b mod 3^(r+1). Hence φ_{n+1} ≥ Φ(φ_n). Φ is monotone and
1-homogeneous, and φ_0 = 1 ≥ V/V_max, so induction gives φ_n ≥ μ^n·V/V_max ≥ (V_min/V_max)·μ^n.
The upper bound is the same argument with ψ_n = max and Ψ. ∎

Then n_k(a) ≥ n*_k(a) = N*_k(a) when a is not on a cycle, and n_k(a) ≤ (k+1)·n*_k(a) ≤ (k+1)·N*_k(a)
(A–L §2). So for every a not on a cycle and every k:

  (V_min/V_max)·μ^k ≤ n_k(a) ≤ (k+1)·(V′_max/V′_min)·μ′^k,

with constants independent of a. If a is on a cycle, pass to a non-cycle node of its tree, as in the proof of
A–L Thm 2.1; this shifts k by a bounded amount. Either way (μ−ε)^k ≤ n_k(a) ≤ (μ′+ε)^k for all large k,
which is the form of A–L Theorem 1.1.

**Certificates.** Run `python extremal_trees.py lp 2 17` (numpy) and `lp 18 19 --engine c` (C helper).
Power iteration (float64 in numpy, float32 in C) finds V. V is rounded to integers, at most 2^34 (numpy) or
2^31 (C), and μ = P/10^7 is rounded down (μ′ rounded up; the C engine leaves a 10^−6 margin for float32).
Then Q·Φ(V) ≥ P·V (resp. ≤) is checked exactly, in int64 (numpy) or 128-bit integers (C), for every class.
Results, all certified:

| r | classes | μ_r (certified, lower) | V_min/V_max | μ′_r (certified, upper) | V′_max/V′_min | 4 − 3μ_r | 3μ′_r − 4 | engine |
|---|---|---|---|---|---|---|---|---|
| 2 | 6 | 1.2498514 | 0.5122 | 1.4036023 | 2.7652 | 2.50e-01 | 2.11e-01 | numpy |
| 3 | 18 | 1.3074986 | 0.3978 | 1.3767090 | 3.3013 | 7.75e-02 | 1.30e-01 | numpy |
| 4 | 54 | 1.3215670 | 0.3568 | 1.3590472 | 3.5374 | 3.53e-02 | 7.71e-02 | numpy |
| 5 | 162 | 1.3258204 | 0.3315 | 1.3471279 | 3.5737 | 2.25e-02 | 4.14e-02 | numpy |
| 6 | 486 | 1.3286744 | 0.3188 | 1.3419976 | 3.6190 | 1.40e-02 | 2.60e-02 | numpy |
| 7 | 1,458 | 1.3303588 | 0.3077 | 1.3381937 | 3.5502 | 8.92e-03 | 1.46e-02 | numpy |
| 8 | 4,374 | 1.3312913 | 0.3003 | 1.3363612 | 3.5683 | 6.13e-03 | 9.08e-03 | numpy |
| 9 | 13,122 | 1.3319678 | 0.2958 | 1.3352163 | 3.5801 | 4.10e-03 | 5.65e-03 | numpy |
| 10 | 39,366 | 1.3324253 | 0.2915 | 1.3345123 | 3.5693 | 2.72e-03 | 3.54e-03 | numpy |
| 11 | 118,098 | 1.3327317 | 0.2889 | 1.3340761 | 3.5767 | 1.80e-03 | 2.23e-03 | numpy |
| 12 | 354,294 | 1.3329407 | 0.2872 | 1.3338053 | 3.5721 | 1.18e-03 | 1.42e-03 | numpy |
| 13 | 1,062,882 | 1.3330771 | 0.2859 | 1.3336346 | 3.5708 | 7.69e-04 | 9.04e-04 | numpy |
| 14 | 3,188,646 | 1.3331663 | 0.2848 | 1.3335267 | 3.5689 | 5.01e-04 | 5.80e-04 | numpy |
| 15 | 9,565,938 | 1.3332241 | 0.2838 | 1.3334580 | 3.5647 | 3.28e-04 | 3.74e-04 | numpy |
| 16 | 28,697,814 | 1.3332617 | 0.2831 | 1.3334139 | 3.5613 | 2.15e-04 | 2.42e-04 | numpy |
| 17 | 86,093,442 | 1.3332864 | 0.2828 | 1.3333857 | 3.5592 | 1.41e-04 | 1.57e-04 | numpy |
| 18 | 258,280,326 | 1.3333013 | 0.2824 | 1.3333685 | 3.5577 | 9.61e-05 | 1.06e-04 | c |
| 19 | 774,840,978 | 1.3333119 | 0.2822 | 1.3333567 | 3.5561 | 6.43e-05 | 7.01e-05 | c |

The recursion inequality φ_{n+1} ≥ Φ(φ_n), ψ_{n+1} ≤ Ψ(ψ_n) was also checked directly on exact class
extrema (r = 2..5, n ≤ 10). The bounds were checked against every exact N^±(k) of §4 (`report --lp` for
r ≤ 17, the same check by hand for r = 18, 19): consistent.

**Structure.** At an eigenvector, summing Φ(v) = μv over all classes gives exactly μ_r = 1 + ρ_r/3, where
ρ_r = mean of the lift-minimum / mean of v. This is the analogue of K–L's summed inequality, and ρ_r → 1 is
equivalent to μ_r → 4/3. Likewise μ′_r = 1 + ρ′_r/3 with ρ′_r ≥ 1. The losses 4 − 3μ_r = 1 − ρ_r and
3μ′_r − 4 = ρ′_r − 1 shrink geometrically, as the last columns of the table show. Successive ratios of
4 − 3μ_r for r = 10…17 are 0.663, 0.653, 0.653, 0.652, 0.654, 0.656, 0.655, and of 3μ′_r − 4 they are 0.630,
0.635, 0.638, 0.642, 0.645, 0.646, 0.650. These use the numpy rows only, because the C rows carry a 10^−6
safety margin.

The ratio per digit is about 0.65. The K–L analogue, 1 − ρ_k, shrinks by only about 0.93 per digit
(CLAUDE.md, ρ_k table). If the geometric decay continues, both μ_r and μ′_r → 4/3, which is Conjecture B.
Unlike K–L, the certificate spread V_max/V_min stays bounded (about 3.5 at both ends, see the table), which
is what makes Conjecture C′ reachable along this route (§9).

A numpy experiment also combined depth-k trees with residue classes (min over a ≡ c mod 3^r of
Σ_leaves v(leaf class)). At k = 13, r = 1, 2, 3 gave 1.27516, 1.31023 and 1.32216, against
g^−(13) = 1.25916. The residue depth r is the lever that matters; tree depth adds little once r ≥ 3.

## 6. Weight vectors and Theorem 1.2

w^±(k) need the extrema of every tail sum (2(k+1) searches per depth), run with tables M = 15 and all
thresholds. They are exact for k ≤ 45. γ*_k is A–L's optimised Chernoff exponent (3.9) computed from
w^−(k). For k = 30 it reproduces their 0.654717.

| k | γ*_k | α*_k | E[Z^−_k]/k |
|---|---|---|---|
| 20 | 0.581699 | 0.268750 | 0.471641 |
| 21 | 0.591224 | 0.274193 | 0.469158 |
| 22 | 0.599240 | 0.277591 | 0.467338 |
| 23 | 0.606344 | 0.281793 | 0.465503 |
| 24 | 0.614848 | 0.286125 | 0.463229 |
| 25 | 0.621639 | 0.288559 | 0.461643 |
| 26 | 0.629568 | 0.292749 | 0.459970 |
| 27 | 0.636608 | 0.296715 | 0.458350 |
| 28 | 0.643504 | 0.299907 | 0.456692 |
| 29 | 0.649338 | 0.303753 | 0.455602 |
| 30 | 0.654717 | 0.305943 | 0.454481 |
| **31** | 0.660730 | 0.309977 | 0.453278 |
| **32** | 0.666850 | 0.312798 | 0.451813 |
| **33** | 0.671779 | 0.316024 | 0.451098 |
| **34** | 0.677090 | 0.318335 | 0.449997 |
| **35** | 0.682396 | 0.321308 | 0.449028 |
| **36** | 0.686790 | 0.323984 | 0.448340 |
| **37** | 0.690609 | 0.325903 | 0.447570 |
| **38** | 0.695357 | 0.328337 | 0.446710 |
| **39** | 0.699293 | 0.330498 | 0.445981 |
| **40** | 0.703109 | 0.332625 | 0.445305 |
| **41** | 0.707291 | 0.334928 | 0.444649 |
| **42** | 0.711566 | 0.337474 | 0.443986 |
| **43** | 0.715175 | 0.339478 | 0.443412 |
| **44** | 0.718924 | 0.341678 | 0.442856 |
| **45** | 0.722362 | 0.343640 | 0.442302 |

New weight vectors (weights 0, 1, …, k; w^− truncated after its last nonzero entry):

- k = 31: w^− = (1, 10, 46, 141, 305, 503, 648, 679, 569, 394, 224, 96, 32, 2, 0, …), w^+ = (1, 11, 54, 179, 443, 840, 1288, 1659, 1810, 1738, 1479, 1095, 774, 529, 362, 251, 174, 111, 70, 50, 35, 24, 14, 10, 6, 5, 3, 2, 2, 1, 1, 1)
- k = 32: w^− = (1, 10, 50, 156, 352, 606, 810, 889, 799, 597, 360, 172, 66, 12, 0, …), w^+ = (1, 11, 60, 210, 519, 985, 1567, 2084, 2354, 2310, 2035, 1614, 1143, 792, 535, 362, 251, 174, 111, 70, 50, 35, 24, 14, 10, 6, 5, 3, 2, 2, 1, 1, 1)
- k = 33: w^− = (1, 10, 54, 171, 406, 724, 1015, 1164, 1092, 852, 551, 292, 121, 36, 3, 0, …), w^+ = (1, 12, 64, 230, 600, 1160, 1899, 2608, 3065, 3092, 2791, 2264, 1696, 1177, 807, 538, 362, 251, 174, 111, 70, 50, 35, 24, 14, 10, 6, 5, 3, 2, 2, 1, 1, 1)
- k = 34: w^− = (1, 11, 57, 189, 462, 863, 1264, 1497, 1467, 1219, 845, 480, 221, 81, 13, 0, …), w^+ = (1, 12, 68, 251, 676, 1349, 2280, 3232, 3938, 4150, 3823, 3175, 2436, 1751, 1206, 816, 538, 362, 251, 174, 111, 70, 50, 35, 24, 14, 10, 6, 5, 3, 2, 2, 1, 1, 1)
- k = 35: w^− = (1, 11, 60, 210, 525, 1014, 1554, 1923, 1979, 1694, 1255, 766, 386, 154, 42, 3, 0, …), w^+ = (1, 12, 72, 274, 761, 1612, 2730, 3997, 4998, 5453, 5214, 4479, 3473, 2547, 1795, 1224, 818, 538, 362, 251, 174, 111, 70, 50, 35, 24, 14, 10, 6, 5, 3, 2, 2, 1, 1, 1)
- k = 36: w^− = (1, 12, 64, 231, 594, 1190, 1878, 2452, 2635, 2351, 1800, 1186, 631, 279, 95, 18, 0, …), w^+ = (1, 12, 76, 297, 850, 1853, 3262, 4905, 6322, 7119, 7049, 6224, 5002, 3686, 2622, 1830, 1235, 819, 538, 362, 251, 174, 111, 70, 50, 35, 24, 14, 10, 6, 5, 3, 2, 2, 1, 1, 1)
- k = 37: w^− = (1, 12, 68, 252, 669, 1383, 2280, 3082, 3457, 3231, 2624, 1792, 1022, 467, 190, 50, 4, 0, …), w^+ = (1, 13, 80, 322, 950, 2171, 3865, 5998, 7977, 9210, 9433, 8576, 7067, 5378, 3819, 2689, 1856, 1240, 819, 538, 362, 251, 174, 111, 70, 50, 35, 24, 14, 10, 6, 5, 3, 2, 2, 1, 1, 1)
- k = 38: w^− = (1, 12, 72, 274, 757, 1609, 2744, 3822, 4497, 4373, 3689, 2643, 1647, 831, 340, 116, 21, 0, …), w^+ = (1, 13, 84, 350, 1057, 2493, 4562, 7302, 9984, 11874, 12473, 11739, 9936, 7739, 5636, 3937, 2738, 1869, 1240, 821, 538, 362, 251, 174, 111, 70, 50, 35, 24, 14, 10, 6, 5, 3, 2, 2, 1, 1, 1)
- k = 39: w^− = (1, 12, 76, 298, 848, 1861, 3278, 4732, 5733, 5900, 5145, 3871, 2533, 1386, 599, 233, 60, 5, 0, …), w^+ = (1, 14, 89, 379, 1174, 2817, 5328, 8815, 12401, 15235, 16429, 15855, 13865, 11071, 8225, 5821, 4028, 2766, 1874, 1240, 821, 538, 362, 251, 174, 111, 70, 50, 35, 24, 14, 10, 6, 5, 3, 2, 2, 1, 1, 1)
- k = 40: w^− = (1, 13, 80, 324, 946, 2140, 3899, 5818, 7286, 7757, 7149, 5594, 3802, 2224, 1069, 420, 138, 27, 0, …), w^+ = (1, 14, 94, 409, 1304, 3234, 6316, 10568, 15343, 19340, 21537, 21312, 19106, 15674, 11928, 8567, 5972, 4088, 2781, 1875, 1240, 821, 538, 362, 251, 174, 111, 70, 50, 35, 24, 14, 10, 6, 5, 3, 2, 2, 1, 1, 1)
- k = 41: w^− = (1, 13, 84, 350, 1050, 2457, 4619, 7127, 9272, 10208, 9669, 8017, 5630, 3498, 1838, 774, 289, 68, 8, 0, …), w^+ = (1, 14, 98, 440, 1438, 3669, 7418, 12626, 18888, 24434, 27987, 28570, 26221, 22002, 17130, 12553, 8803, 6082, 4126, 2789, 1876, 1240, 821, 538, 362, 251, 174, 111, 70, 50, 35, 24, 14, 10, 6, 5, 3, 2, 2, 1, 1, 1)
- k = 42: w^− = (1, 14, 88, 378, 1169, 2817, 5440, 8660, 11647, 13310, 13055, 11276, 8334, 5376, 2997, 1399, 545, 168, 34, 1, 0, …), w^+ = (1, 14, 102, 472, 1585, 4145, 8720, 15036, 23065, 30745, 36095, 37900, 35798, 30795, 24439, 18272, 12998, 8993, 6152, 4144, 2790, 1876, 1240, 821, 538, 362, 251, 174, 111, 70, 50, 35, 24, 14, 10, 6, 5, 3, 2, 2, 1, 1, 1)
- k = 43: w^− = (1, 14, 93, 408, 1300, 3195, 6372, 10501, 14498, 17195, 17500, 15523, 12146, 8162, 4770, 2389, 1003, 359, 90, 10, 0, …), w^+ = (1, 15, 107, 506, 1741, 4673, 10209, 18044, 28069, 38435, 46295, 49862, 48403, 42780, 34756, 26441, 19112, 13315, 9138, 6198, 4154, 2791, 1876, 1240, 821, 538, 362, 251, 174, 111, 70, 50, 35, 24, 14, 10, 6, 5, 3, 2, 2, 1, 1, 1)
- k = 44: w^− = (1, 14, 98, 438, 1436, 3630, 7456, 12611, 18015, 22046, 23262, 21405, 17326, 12179, 7488, 3983, 1810, 691, 209, 42, 2, 0, …), w^+ = (1, 15, 112, 541, 1913, 5251, 11745, 21363, 34053, 47790, 59168, 65316, 64987, 58872, 49059, 38047, 27987, 19698, 13580, 9237, 6226, 4159, 2791, 1876, 1240, 821, 538, 362, 251, 174, 111, 70, 50, 35, 24, 14, 10, 6, 5, 3, 2, 2, 1, 1, 1)
- k = 45: w^− = (1, 14, 103, 471, 1584, 4110, 8660, 15066, 22221, 27995, 30631, 29168, 24464, 17984, 11577, 6462, 3110, 1281, 451, 111, 15, 0, …), w^+ = (1, 16, 117, 578, 2090, 5896, 13511, 25362, 41098, 59111, 75153, 85034, 86754, 80462, 68652, 54388, 40700, 29087, 20152, 13760, 9293, 6240, 4161, 2791, 1876, 1240, 821, 538, 362, 251, 174, 111, 70, 50, 35, 24, 14, 10, 6, 5, 3, 2, 2, 1, 1, 1)

## 7. Timings and memory

Machine: Apple M4 Pro (14 cores), 64 GB, shared with other agents' jobs. Load was 12–29 most of the night,
so wall times are pessimistic. The search printed `secs` and the number of search nodes for each class-2
optimum. The time per depth roughly doubles: the node count grows by about 1.35×, and the pending-head lists by
4/3.

| class-2 depth k | min: s / nodes | max: s / nodes | configuration |
|---|---|---|---|
| 30 | 0.003 / 848 | 0.007 / 4 775 | M = 14, 8 threads |
| 40 | 0.37 / 15 236 | 1.5 / 82 362 | M = 16, 4 threads |
| 45 | 5.6 / 35 060 | 8.4 / 175 681 | M = 19, 5 + 5 threads (fork) |
| 50 | 35 / 207 043 | 115 / 914 605 | M = 19 / 18, 5 threads |
| 52 | 72 / 534 649 | 512 / 1 960 269 | M = 18, 5 / 4 threads |
| 53 | 185 / 704 292 | 951 / 2 689 716 | M = 18, 6 (code v1) / 4 threads |
| 54 | 234 / 988 061 | 1785 / 3 674 187 | M = 18, 4 + 4 threads |
| 55 | 396 / 1 434 758 | 2544 / 4 964 320 | M = 18, 4 + 4 threads |
| 56 | 720 / 1 847 323 | – | M = 18, 4 threads |
| 57 | 1441 / 2 588 497 | – | M = 18, 4 threads |
| 58 | 2237 / 3 558 179 | – | M = 18, 4 threads |
| 59 | 41 / 15 352 (verification with incumbent L2_min(58), `V` line) | – | M = 18, 4 threads |

- Tables: M = 18 needs 7.0 GB (10 s to build), M = 19 needs 20.9 GB (31 s), and M = 15 with all thresholds
  4.0 GB. Peak RSS per search process is the table size plus about 3 GB of temporary arrays while building,
  plus well under 1 GB of search state. Two M = 18 processes used about 11 GB together.
- Unpruned enumeration (single thread, M = 16): k = 30 takes about 1 min (3·10^8 determined classes);
  each further k takes about 2×.
- w^± runs (2 threads, M = 15, all thresholds, 2(k+1) searches per depth): k = 40 takes 106 s, k = 44 26 min,
  k = 45 43 min. The run was stopped after k = 45.
- Residue-class certificates: numpy r = 17 takes 1111 s for both systems, single thread, about 5 GB. The C
  helper does r = 19 in 200 s per system on 3 threads, with 9.3 GB (two float32 vectors over 3^19
  classes). r = 20 would need 28 GB and was not run.

## 8. Caveats

1. **The A–L tables are not available here.** The preprint PDF in the scratchpad (`kl_paper/al1.pdf`) has
   "Insert Table 2.1 about here" placeholders, and every attempt to fetch the published version (AMS,
   Lagarias's home page, EMIS) hit a Cloudflare challenge; web search was unavailable. The validation against
   A–L therefore uses the three k = 30 numbers printed in the text (§3). They pin N^−(30), N^+(30) uniquely and
   test w^−(30) through γ*_30. Entries k ≤ 29 of Tables 2.1/2.2 and the clone counts R(k) of Table 2.4 were not
   compared. `python extremal_trees.py report …` prints every value, so a comparison is mechanical once the
   tables are at hand.
2. **What certifies the extremal counts.** Attainment is certified independently: a witness residue is
   recounted from the definition with actual integers. Optimality ("no tree is smaller/larger") rests on the
   branch-and-bound code and its tables. That code is cross-checked in several ways:
   - two independent brute forces (literal integers for k ≤ 10, a numpy residue recursion for k ≤ 13);
   - the exhaustive tables up to k = 19;
   - search runs with table depths M = 4, 7, 10, 12, 14, 16, 18, 19 agree wherever they overlap;
   - two code versions (natural-order tables v1, trie-order tables v3+) agree for k ≤ 53 (min) and k ≤ 49 (max);
   - the k = 30 values of A–L.

   There is no independent optimality certificate, such as a dual or an exhaustive clone list, for k > 19.
3. **The residue-class bounds (§5.2) are certified differently and more strongly.** The inequality
   Q·Φ(V) ≥ P·V is checked exactly in int64, with an overflow guard proved in Python integers. For r ≤ 7 it is
   re-checked with plain Python integers, and a negative test (μ ± 2·10^−4) is rejected. The proof that the
   certificate implies the bound is the short induction in §5.2. Floating point is only used to find V.
4. **Novelty of §5.2 not checked.** I could not search the post-1995 literature tonight. The repository's
   literature notes (2026-10-08) quote A–L Theorem 1.1 as the best bound for n_k(a). Kontorovich–Lagarias (2010)
   still state the tree-growth constant log(4/3) as a conjecture. The system is the obvious depth analogue of
   Krasikov's and Krasikov–Lagarias's difference inequalities, so it may well be known in some form. Check
   before claiming priority.
5. Conventions: weight and depth exactly as A–L (2.3); n ≡ 0 (mod 3) nodes are pruned. N*_k(a) counts tree
   nodes, so labels repeat when a lies on a cycle. n_k(a) differs from N*_k(a) by at most a factor k+1
   (A–L §2), which does not affect growth rates.
6. Run history. Around 01:04–01:06 another job briefly took about 45 GB, and the first long run (M = 19,
   21 GB of tables) was being paged out. I stopped it at 01:07 and resumed with M = 18 from its logs
   (`ET_LOAD`), later with fewer threads because of the load. A result row is written only after its search
   has finished, so stopped runs leave no partial values. Every (k, sense) computed by more than one run
   (different M, code versions v1/v3+) has the same value, and the report refuses inconsistent logs.
7. γ*_k (Theorem 1.2 analogue) is only a by-product. Its exponent for π_a(x) was superseded long ago
   (K–L 0.84, this repository 0.925, Mazur positive density).

## 9. Relevance

- **Conjecture B** (Lagarias–Weiss; A–L (1.5)): n_k(a) = (4/3)^(k(1+o(1))) for each a ≢ 0 (mod 3). The
  residue-class certificates squeeze the growth rate to within 2.3·10^−5 of 4/3 on either side, uniformly in a
  and with explicit constants for every k (§5.2). Conjecture B itself would follow from
  μ_r → 4/3 and μ′_r → 4/3 (r → ∞). This is the exact depth analogue of the Krasikov–Lagarias question
  λ_k → 2 (avenue 1). As there, the summed inequality gives μ_r = 1 + ρ_r/3, where ρ_r is the mean of the
  lift-minimum over the mean of v. But here 1 − ρ_r shrinks by a factor of about 0.65 per digit, against
  about 0.93 per digit in K–L (`rho.py`). The depth problem is the easy version of avenue 1 and the natural
  model problem for a proof attempt.
- **Conjectures C, C′.** For 25 ≤ k ≤ 59, (4/3)^k/N^−(k) stays in [2.0334, 2.0475]. For 25 ≤ k ≤ 55,
  N^+(k)/(4/3)^k stays in [1.7376, 1.7483], with no drift. The branching-process models predict that both ratios diverge (A–L §4 and the Experimental Math. companion), so the 3x+1 trees
  remain much more rigid than the random model. A–L wondered whether the normalised extremes have limits.
  The data suggest yes: about 2.039 and 1.742.

  The certificates also give a route to C′. N^−(k) ≥ (V_min/V_max)·μ_r^k holds for every r. The certificate
  constant V_min/V_max stays about 0.28 and V_max/V_min about 3.6 for the upper system, as r grows (§5.2),
  unlike the K–L vectors, whose spread grows like 1.52^k. If μ_r → 4/3 with the spread bounded in r, letting
  r → ∞ at fixed k gives C^−(4/3)^k ≤ N^−(k) ≤ N^+(k) ≤ C^+(4/3)^k, which is Conjecture C′.
- **Uniformity in a after Mazur.** The formal positive-density theorem (`notes/m2_audit.md`) gives
  π_a(x) ≥ c_a·x with ineffective c_a. It counts predecessors by size, at any depth, and says nothing about
  n_k(a), the number at exact depth k. Conjecture B (for each a) and Conjectures C/C′ (extremes over all a,
  hence uniform in a) concern exact-depth counts and remain open. The bounds here are uniform in a and
  explicit. For n_k(a) they replace (1.302053, 1.358386) by (1.333311, 1.333357).

## 10. Reproduce

```
export EXTREMAL_BIN=$TMPDIR/extremal_trees_core           # where the helper binary is compiled
.venv/bin/python extremal_trees.py validate               # cross-checks of §3 (about 1 min)
.venv/bin/python extremal_trees.py lp 2 17 --json lp.json # certified residue-class bounds (§5.2)
.venv/bin/python extremal_trees.py lp 18 19 --engine c --threads 3 --json lp_c.json   # 9.3 GB at r = 19
# extremal searches (tables M = 18: 7 GB; the min and max halves can run as two processes):
.venv/bin/python extremal_trees.py run min.log --M 18 --k1 60 --sense min --threads 4
.venv/bin/python extremal_trees.py run max.log --M 18 --k1 60 --sense max --threads 4
.venv/bin/python extremal_trees.py run tau.log --M 15 --k1 60 --tau --threads 2      # w^+-(k)
# resume a run from earlier logs, or certify one more N^-(k) cheaply (class 1 = class 2 one level down):
ET_LOAD=min.log ET_INIT_MIN=<L2_min(K-1)> $EXTREMAL_BIN search 18 0 K K 4 9 0 0
.venv/bin/python extremal_trees.py report min.log max.log tau.log --lp lp.json --md tables.md --json out.json
```
The night's logs are in the session scratchpad (`et/*.log`; not in the repository).
