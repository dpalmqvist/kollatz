# Four older "long-shot" strands of the 3x+1 problem (state as of 2026-10-08)

Conventions used below. T(n) = n/2 (n even), (3n+1)/2 (n odd); σ(n) = stopping time (least k with T^(k)(n) < n);
"primary-confirmed" = read in the primary source or in Lagarias's annotated bibliographies (which I treat as
authoritative secondary for pre-2010 items); "secondhand" = only seen via an abstract page, OEIS comment, search
snippet or citing paper. All arXiv/OEIS/HAL/DMTCS pages were fetched on 2026-10-08; the two Lagarias bibliography PDFs
(arXiv:math/0309224 v13, arXiv:math/0608208) were downloaded and text-extracted locally, so quotations from them are
exact modulo PDF hyphenation.

## Strand A — Terras's Coefficient Stopping Time Conjecture (1976)

### Takeaway
The conjecture "κ(n) = σ(n) for all n ≥ 2" is still open. The classical rigorous checks are tiny by modern standards
(Terras 1976: all n with κ(n) ≤ 2593; Garner 1981: all n with κ(n) < 105 000), but Rozier–Terracol (Discrete Math.
2026) now claim, via "paradoxical sequences" plus the Oliveira e Silva / Roosendaal record tables, that σ(n) = τ(n)
for every 2 ≤ n ≤ 2.8·10^19 — i.e. the strand has been quietly revisited and the computational frontier moved from
~10^5 (in κ) to ~10^19 (in n) in 2025–26.

### Cited Findings
- Primary reference: Riho Terras, "A stopping time problem on the positive integers", Acta Arithmetica 30 (1976),
  241–252 (MR 58 #27879). Lagarias's annotation (verbatim): "This paper introduces the notion of the coefficient
  stopping time κ(n) of an integer n > 1. Write T^(k)(n) = α(n)n + β(n) with α(n) = 3^a(n)/2^k [the extracted text has
  '2^n', a typo], where a(n) is the number of iterates T^(j)(n) ≡ 1 (mod 2) with 0 ≤ j < k. Then κ(n) is defined to be
  the least k ≥ 1 such that T^(k)(n) = α(n)n + β(n) has α(n) < 1, and κ(n) = ∞ if no such value exists. It is clear
  that κ(n) ≤ σ(n), where σ(n) is the stopping time of n. Terras formulates the Coefficient Stopping Time Conjecture,
  which asserts that κ(n) = σ(n) for all n ≥ 2. He proves this conjecture for all values κ(n) ≤ 2593. This can be
  done for κ(n) below a fixed bound by upper bounding β(n) and showing ... α(n) < 1 − δ for suitable δ and
  determining the maximal value 3^l/2^j < 1 possible with j below the given bound. The convergents of the continued
  fraction expansion of log_2 3 play a role in determining the values of j that must be checked." — primary-confirmed
  from [Lagarias, annotated bibliography I, entry 164](https://arxiv.org/abs/math/0309224)
- Same entry: Terras's main result (stopping-time sets are unions of congruence classes mod 2^k minus finitely many
  elements; integers with finite stopping time have natural density 1) was obtained "independently and
  contemporaneously by Everett (1977)"; further details in R. Terras, "On the existence of a density", Acta Arith. 35
  (1979), 101–102, after criticism by Möller (1978). — primary-confirmed, [bibliography I, entries 164–165](https://arxiv.org/abs/math/0309224)
- Garner's extension: Lynn E. Garner, "On the Collatz 3n+1 algorithm", Proc. Amer. Math. Soc. 82 (1981), 19–22
  (MR 82j:10090). Lagarias's annotation: "the Coefficient Stopping Time Conjecture of Terras (1976) asserts that
  κ(n) = σ(n) for all n ≥ 2. This paper proves that κ(n) < 105,000 implies that κ(n) ≤ σ(n) [sic; i.e. equality].
  The proof methods used are those of Terras (1976), who proved the conjecture holds for κ(n) < 2593. They involve the
  use of the continued fraction expansion of log_2 3 and the truth of the 3x+1 Conjecture for n < 2.0 × 10^9." —
  primary-confirmed from [bibliography I, entry 71](https://arxiv.org/abs/math/0309224). (NB: the 1985 Garner paper
  "On heights in the Collatz 3n+1 problem", Discrete Math. 55 (1985), 57–64, is about consecutive integers with equal
  height, not about the CST conjecture — [bibliography I, entry 72](https://arxiv.org/abs/math/0309224).)
- Lagarias's 1985 survey (J. C. Lagarias, "The 3x+1 problem and its generalizations", Amer. Math. Monthly 92 (1985),
  3–23; citation confirmed in the reference list of the CADE-28 paper by Yolcu–Aaronson–Heule) discusses the
  conjecture in Section 2 ("The 3x+1 problem"), in the sub-sections "Behavior of the stopping time function"
  (Theorem C: "Terras [67] defines the coefficient stopping time to be the least value of k such that (2.7) holds ...
  and ∞ if no such value of k exists"; Theorem C(a): "The set of integers with coefficient stopping time k are
  exactly the set of integers in those congruence classes ...") and "What is the relation between the coefficient
  stopping time and the stopping time?" ("Theorem C shows that generally they are equal ... for any fixed k, only
  finitely many n with coefficient stopping time k have stopping time ≠ k. Terras [67] and later Garner [34]
  conjecture that this never occurs. Coefficient Stopping Time Conjecture: For all n ≥ 2, the stopping time σ(n)
  equals the coefficient stopping time κ(n)"; Theorem E gives "an effectively computable constant"). In the
  sub-section "Are there non-trivial cycles?" he notes: "This approach also allows one to check the truth of the
  Coefficient Stopping Time Conjecture for all n with [bound lost in HTML]" and that it "holds for the infinite set of
  admissible vectors" of the form (2.27), and that "This approach has been taken by Crandall [28], Garner [34],
  Schuppar [61] and Terras [67]"; the combined cycle bound there is "no nontrivial cycles with period length less than
  275,000". — primary-confirmed from the HTML edition of the survey, [node4](https://www.cecm.sfu.ca/organics/papers/lagarias/paper/html/node4.html),
  [node5](https://www.cecm.sfu.ca/organics/papers/lagarias/paper/html/node5.html),
  [node8](https://www.cecm.sfu.ca/organics/papers/lagarias/paper/html/node8.html),
  [table of contents](https://www.cecm.sfu.ca/organics/papers/lagarias/paper/html/paper.html). The HTML edition
  numbers these as 2.2, 2.3 and 2.6 (inferred from anchors); the printed Monthly numbering may differ, so cite as
  "Section 2, Theorems C–E and the CST Conjecture; Section 2, 'Are there non-trivial cycles?'".
- Implication for cycles (explicit in the 2026 paper): "the paper says CST 'implies the absence of nontrivial cycles.'
  If a nontrivial cycle of length l existed, its smallest term would have infinite stopping time, while τ(n) ≤ l."
  — primary-confirmed from [Rozier–Terracol, arXiv:2502.00948](https://arxiv.org/html/2502.00948)
- Modern revisit #1: Olivier Rozier, Claude Terracol, "Paradoxical behavior in Collatz sequences", arXiv:2502.00948
  (v1 2 Feb 2025, v5 17 May 2026), published as Discrete Mathematics 349 (2026) 115167, DOI
  10.1016/j.disc.2026.115167. Definitions used: C_j(n) = 3^q/2^j (q = number of odd terms among the first j), τ(n) =
  least j with C_j(n) < 1 (= Terras's κ), "Terras conjectured that equality [t(n) = τ(n)] holds for n ≥ 2". A
  sequence is paradoxical if it exceeds its first term although the odd-term proportion predicts descent. Results:
  Theorem 1.3 "There are exactly 593 paradoxical sequences that begin with an integer lower than or equal to 4614"
  (550 distinct starting integers; exhaustive search of all starts ≤ 10^9); Theorem 3.2: an n ≥ 2 with infinite
  stopping time yields infinitely many paradoxical sequences starting from 2^k·n; Corollary 3.3: "If there are only
  finitely many paradoxical sequences, then the Collatz conjecture is true"; Theorem 5.3 combines the search with the
  Oliveira e Silva / Roosendaal maximum-excursion and delay record tables to exclude further paradoxical sequences
  with 93 ≤ j ≤ 301 993 or 4615 ≤ n ≤ 2.8·10^19; Corollary 5.4: t(n) = τ(n) for every 2 ≤ n ≤ 2.8·10^19; Conjecture
  6.1: no paradoxical sequence has first term > 4614. — primary-confirmed from
  [arXiv:2502.00948 (abs)](https://arxiv.org/abs/2502.00948) and [HTML full text](https://arxiv.org/html/2502.00948)
- Modern revisit #2: Mike Winkler, "Deterministic Structures in the Stopping Time Dynamics of the 3x+1 Problem",
  arXiv:1709.03385 (v1 6 Sep 2017, v8 28 Jul 2026, math.GM, no journal). Studies Terras's coefficient stopping time
  via parity vectors and exponential Diophantine equations, residue classes mod 2^k by admissible positions of odd
  iterates, a Pascal-type recursion and periodicity results; the abstract states the paper "neither prove[s] that
  every starting value has finite coefficient stopping time nor establish[es] equality between the coefficient
  stopping time and the classical stopping time." — primary-confirmed from [arXiv:1709.03385](https://arxiv.org/abs/1709.03385)
- Modern revisit #3 (Chinese, 2003): Wu Jia Bang and Hao Shen Wang, "On the equality of the adequate stopping time
  and the coefficient stopping time of n in the 3N+1 conjecture", J. Huazhong Univ. Sci. Technol. Nat. Sci. 31 (2003),
  no. 5, 114–116 (MR 2000420). Lagarias's annotation quotes the English summary: "It was proved that t_a(n) = t_c(n)
  on condition that d = Σ x_i(n) is not very large. Therefore it was conjectured that when the bound condition for d
  was unnecessary ... t_c(n) = t_a(n) in all cases." — primary-confirmed from
  [bibliography II, entry 124](https://arxiv.org/abs/math/0608208)

### Inferences
- The "last known bound" depends on what is bounded. In κ (coefficient stopping time value) the rigorous classical
  bound is κ(n) < 105 000 (Garner 1981), resting on 3x+1 verified to 2·10^9. In n, the 2026 Rozier–Terracol
  Corollary 5.4 gives n ≤ 2.8·10^19, resting on the Oliveira e Silva / Roosendaal record tables (not on an
  independent exhaustive CST check). Both are "cheap to redo" with today's verification range (Barina: 2^71): the
  Terras/Garner argument scales with the verified range and with the continued-fraction convergents of log_2 3, so a
  modern run could push the κ-bound by orders of magnitude; this is exactly the kind of long-shot the user is after.
- The CST conjecture is strictly stronger than "no non-trivial cycles" (a cycle minimum would have σ = ∞ but κ ≤
  cycle length). It does not address divergent trajectories.

### Gaps
- Conflict I could not resolve: Rozier–Terracol (per the HTML text) say CST was "verified up to n = 250,000 (Terras)
  and extended to n = 1,150,000 (Garner, who used the Col variant)", whereas Lagarias's bibliography gives bounds in κ
  (2593 and 105 000). I could not fetch Garner's PAMS page (HTTP 403) or Terras's paper to see which quantity each
  bound refers to; treat the 250 000 / 1 150 000 figures as unconfirmed.
- The numeric bound in Lagarias 1985, Section 2 ("check the truth of the CST Conjecture for all n with ...") is lost
  in the HTML conversion; the printed Monthly text would need to be checked.
- No post-2000 paper other than Rozier–Terracol and Winkler was found that mentions the CST conjecture by name; no
  dedicated large-scale computation of κ(n) = σ(n) (e.g. to 2^60 or 2^71) was found.

## Strand B — Cycles of the 3x+d maps and Belaga–Mignotte's catalogues

### Takeaway
Lagarias (1990) set up the "rational cycles = integer cycles of 3x+k" framework and conjectured that every k ≡ ±1
(mod 6) has at least one primitive cycle and only finitely many; Belaga–Mignotte computed (conjecturally complete)
primitive-cycle catalogues for all 6667 values 1 ≤ d ≤ 19 999 (2000, re-issued 2006), and the only later extension
found is G. H. Morley's 2013 OEIS work (recomputation for k < 20 000 by exhausting all starts < 10^8, with a
correction of −8 cycles to Belaga–Mignotte's total, plus a partial sweep to k < 158 195).

### Cited Findings
- Jeffrey C. Lagarias, "The set of rational cycles for the 3x+1 problem", Acta Arithmetica 56 (1990), 33–53, DOI
  10.4064/aa-56-1-33-53 (MR 91i:11024). Lagarias's own annotation: "This paper studies the sets of those integer cycles
  of T_k(x) = (3x+k)/2 if x ≡ 1 (mod 2), x/2 if x ≡ 0 (mod 2), for positive k ≡ ±1 (mod 6) which have (x, k) = 1.
  These correspond to rational cycles x/k of the 3x+1 function T. It conjectures that every T_k has such an integer
  cycle. It shows that infinitely many k have at least k^(1−ε) distinct such cycles of period at most log k, and
  infinitely many k have no such cycles having period length less than k^(1/3). Estimates are given for the counting
  function C(k, y) counting the number of such cycles of T_k of period ≤ y, for all k ≤ x with y = β log x. In
  particular C(k, 1.01k) ≤ 5k(log k)^5." — primary-confirmed from [bibliography I, entry 108](https://arxiv.org/abs/math/0309224);
  DOI/pages from the [IMPAN journal page](https://www.impan.pl/en/publishing-house/journals-and-series/acta-arithmetica/all/56/1/106574/the-set-of-rational-cycles-for-the-3x-1-problem)
- OEIS restatement of the two Lagarias conjectures: "Following Lagarias (1990), a cycle is primitive if all its
  elements are relatively prime to k. Lagarias conjectured that every k coprime to 6 has at least one primitive cycle
  and that the number of such cycles is finite." — secondhand (OEIS comment by Morley), [A226607](https://oeis.org/A226607)
- OEIS A102280 cites Table 3.1 on p. 41 of the 1990 paper for primitive-cycle data and notes "there are errors –
  a(12)[k=35] and a(25)[k=73] are incorrect". — secondhand (search snippet of [A102280](https://oeis.org/A102280))
- Edward G. Belaga, Maurice Mignotte, "Embedding the 3x+1 Conjecture in a 3x+d Context", Experimental Mathematics
  7 (1998), no. 2, 145–151 (zbMATH 0918.11008, MR1677087; MSC 11B83, 11K31; Lagarias's bibliography dates it 1999).
  Abstract (Project Euclid): studies 3n+d with d = −1 or an odd positive integer not divisible by 3; "new cyclic
  phenomena appear, side by side with the general convergent dynamics typical of the 3x+1 case"; conjectures that for
  each such d there is a finite set of positive integers into which iteration eventually lands; "along with a new
  boundedness result, we present an improved formalism". Lagarias's annotation of the content: "It proves that there
  is an absolute constant c such that there are at most d·k^c periodic orbits which contain at most k odd integers.
  Furthermore c is effectively computable. This follows using a transcendence result of Baker and Wüstholz." —
  primary-confirmed from [Project Euclid](https://projecteuclid.org/journals/experimental-mathematics/volume-7/issue-2/Embedding-the-3x1-conjecture-in-a-3xd-context/em/1048515662.full)
  and [bibliography I, entry 18](https://arxiv.org/abs/math/0309224). No range of d computed is stated on the abstract page.
- Edward Belaga, Maurice Mignotte, "Cyclic Structure of Dynamical Systems Associated with 3x+d Extensions of Collatz
  Problem", Université Louis Pasteur / IRMA Strasbourg preprint 2000-18 (cited by OEIS as "Preprint math. 2000/17"),
  57 pages, HAL hal-00129656. HAL abstract (paraphrase from the HAL API): cyclic structures of the systems D_d for odd
  d ≥ 1 coprime to 6; primitive cycles computed for the 6 667 systems with 1 ≤ d ≤ 19 999; unifies primitive
  membership in one framework; "experimentally confirms three of Jeff Lagarias's conjectures"; proposes and tests
  new conjectures using Diophantine formulae; proves a new upper bound on the number of primitive cycles of a given
  odd length. A search snippet of the abstract reads: "For every one of 6667 systems D_d, 1 ≤ d ≤ 19999, we calculate
  its (complete, as we argue) list of primitive cycles." Lagarias: "a theoretical and experimental study of the
  distribution of number and lengths of finite cycles to the 3x+d map, for d ≡ ±1 (mod 6). It contains much data and
  a wealth of interesting results and conjectures." — primary-confirmed abstract via
  [HAL API record hal-00129656](https://api.archives-ouvertes.fr/search/?q=halId_s:hal-00129656&fl=title_s,abstract_s,authFullName_s,producedDate_s)
  and [bibliography II, entry 10](https://arxiv.org/abs/math/0608208)
- Edward Belaga, "Effective polynomial upper bounds to perigees and numbers of (3x+d)-cycles of a given odd length",
  Acta Arithmetica 106 (2003), no. 2, 197–206 (MR 2003m:11120). Lagarias: for a cycle C of length l with k odd
  elements, "the smallest element prg(C) in the cycle satisfies prg(C) ≤ d/(2^(l/k) − 3). From this follows log_2 3 <
  length(C)/oddlength(C) ≤ log_2(d+3)"; using linear forms in logarithms the number U_{d,k} of cycles of odd-length
  k is ≤ d·k^c0 with c0 = 32, and the largest element S < d·k^c0·(3/2)^k. — primary-confirmed from
  [bibliography II, entry 11](https://arxiv.org/abs/math/0608208)
- Edward G. Belaga, Maurice Mignotte, "Walking Cautiously Into the Collatz Wilderness: Algorithmically, Number
  Theoretically, Randomly", DMTCS Proceedings vol. AG (Fourth Colloquium on Mathematics and Computer Science:
  Algorithms, Trees, Combinatorics and Probabilities), 249–260, published 31 Dec 2005 (Lagarias dates it 2006), DOI
  10.46298/dmtcs.3512, HAL hal-01184717. Abstract: "Building on theoretical insights and rich experimental data of
  our preprints", new theoretical and experimental results on algorithmic decidability, random behaviour and
  Diophantine representation of related dynamical systems and their cyclic/divergent properties. Lagarias: "discusses
  many open questions about the 3x+1 map and related maps, and recent new numerical evidence supporting them. It
  formulates some new conjectures." — primary-confirmed from [DMTCS](https://dmtcs.episciences.org/3512) and
  [bibliography II, entry 12](https://arxiv.org/abs/math/0608208)
- Edward G. Belaga, Maurice Mignotte, "The Collatz Problem and Its Generalizations: Experimental Data. Table 1.
  Primitive Cycles of (3n+d)-mappings", Univ. Strasbourg preprint 2006-015, "9 pages + 400+ page table", HAL
  hal-00129727 (produced 2006-07-04). HAL abstract: primitive cycles (no common divisor > 1) computed for the 6 667
  systems with 1 ≤ d ≤ 19 999; "confirm two long-standing conjectures of Lagarias (1990) and support several new
  conjectures by Belaga and Mignotte (2000)"; mentions the bound on the minimal member of a primitive cycle proved by
  Belaga 2003. Lagarias: "detailed tables of primitive cycles on the positive integers for 3x+d maps for 1 < d <
  20000. The authors conjecture they obtain the complete list of such cycles, for these values of d." Companion:
  "Table 2. Factorization of Collatz numbers 2^l − 3^k", preprint 2006-018, "6 pages text + 156 page table",
  divisors of 2^l − 3^k for l ≤ 114 ("Numbers D of this form give 3x+D problems having many primitive cycles"). —
  primary-confirmed abstract via [HAL API record hal-00129727](https://api.archives-ouvertes.fr/search/?q=halId_s:hal-00129727&fl=title_s,abstract_s,authFullName_s,producedDate_s)
  and [bibliography II, entries 13–14](https://arxiv.org/abs/math/0608208)
- Later extension (OEIS, Geoffrey H. Morley, 13 Jun 2013): A226607 "Irregular array ... lists the smallest elements,
  in ascending order, of conjecturally all primitive cycles of positive integers under iteration by the 3x+k
  function". Comments: for k < 20 000 "the 42757 primitive cycles were found by examining every trajectory with a
  starting value below 10^8"; largest minimal element 8 013 899 at k = 17 021; "Belaga and Mignotte's Table 3
  overcounts the cycles for k < 20000 with both 3 and 5 cycles by 1, so their total of 42765 is 8 too high"; for
  k < 158 195, no trajectory with start < 10^8 has a primitive cycle with minimal element > 28 306 063 (attained at
  k = 103 645); b-file rows 1..6667 (k < 20 000). Related: A226613 (conjectured number of primitive cycles, indexed
  n = floor(k/3)+1; data 1, 5, 1, 2, 9, 2, 1, 3, 2, 4, ...; cites Belaga–Mignotte 2000 Table 1 p. 19 for a(1)..a(500)),
  A226662 (smallest k with exactly n primitive cycles), A226663 (record k for number of cycles), A226670 (record
  lengths of longest primitive cycles), A226629 (3x−k analogue). — primary-confirmed from
  [A226607](https://oeis.org/A226607) and [A226613](https://oeis.org/A226613); the OEIS search listing is at
  [oeis.org search "3x+d cycles"](https://oeis.org/search?q=3x%2Bd+cycles&fmt=short)
- Statistical follow-up: Darrell Cox, "The 3n+1 Problem: A Probabilistic Approach", Journal of Integer Sequences 15
  (2012), Article 12.5.2. Uses Belaga–Mignotte's table for d < 20 000; proposes a Poisson(λ = 1) model for the number
  of (interrelated-)cycles per d; "For d less than 100 ... 14 d values where there is only 1 cycle, ... 12 ... exactly
  2 ..., 6 ... exactly 3 ..., 1 ... exactly 4"; recomputed cycles up to d = 10 000 over positive and negative n and
  reports "new cycles that do not appear in Belaga and Mignotte's table" (because negative n are allowed); "The
  article consists entirely of analysis of empirical results; no proofs are given." — primary-confirmed from
  [JIS PDF](https://cs.uwaterloo.ca/journals/JIS/VOL15/Cox/cox10.pdf)
- Darrell Cox, Sourangshu Ghosh, Eldar Sultanow, "Collatz Cycles and 3n+c Cycles", arXiv:2101.04067 (2021), J.
  Math. Computer Sci. 24 (2022), no. 4, 330–337: extends Halbeisen–Hungerbühler's optimal cycle-length bounds to
  3n+c cycles; no computation range stated on the abstract page. — primary-confirmed abstract,
  [arXiv:2101.04067](https://arxiv.org/abs/2101.04067)
- Robert Tremblay, "Generalized 3x+1 Mappings: searching for cycles", arXiv:1907.13302 (2019) and "Generalized 3x+1
  Mappings: counting cycles", arXiv:1909.00213 (2019, v2 2021; "We demonstrate that the number of cycles for two
  problems of the family of generalized 3x+1 mappings is possible finite"); no journal, no ranges on abstract pages.
  — primary-confirmed abstracts, [1907.13302](https://arxiv.org/abs/1907.13302), [1909.00213](https://arxiv.org/abs/1909.00213)
- Background bound used by this literature: Lorenz Halbeisen, Norbert Hungerbühler, "Optimal bounds for the length
  of rational Collatz cycles", Acta Arith. 78 (1997), 227–239: "optimal" upper bounds for the minimal element of a
  rational cycle of length k; if 3x+1 is verified to 212 366 032 807 211 ≈ 2.1·10^14 the cycle-length bound jumps to
  102 225 496. — primary-confirmed from [bibliography I, entry 80](https://arxiv.org/abs/math/0309224)
- Related Lagarias note on 5x+1 cycles (Metzger 1999, PM 41, 25–27): on the positive integers 5x+1 has no cycle of
  size 1, a unique cycle of size 2 (smallest element 1) and exactly two cycles of size 3 (smallest elements 13 and
  17). — primary-confirmed from [bibliography I, entry 127](https://arxiv.org/abs/math/0309224)

### Inferences
- The Belaga–Mignotte catalogue is "complete as we argue" — a heuristic completeness claim (all starts below a
  fixed bound), not a proof; Morley's 2013 recount with starts < 10^8 is the only independent check found, and it
  found 8 fewer cycles (a table-counting error, not missing cycles). No published 2014–2026 extension beyond
  d < 20 000 (complete) / d < 158 195 (partial, starts < 10^8) was found; a modern GPU sweep to d ~ 10^6 with starts
  ≤ 2^40 would be new data for the "number of primitive cycles ~ Poisson" conjecture (Cox) and for Lagarias's
  finiteness/existence conjectures.
- The "(n,k) pairs" structure referred to in the task corresponds to Belaga–Mignotte's use of the Diophantine
  numbers 2^l − 3^k (their Table 2): d with many primitive cycles are divisors of such numbers (Lagarias's note on
  preprint 2006-018).

### Gaps
- I could not read the full text of Lagarias 1990, so the exact wording of his conjectures (in particular whether a
  statement about eventual periodicity of every rational with odd denominator is formulated as a conjecture there) is
  unconfirmed; what is confirmed is "every T_k has a primitive cycle" (Lagarias's own annotation) and, secondhand
  via OEIS/HAL, "the number of primitive cycles is finite for each k".
- The exact per-d cycle-minimum search bound used by Belaga–Mignotte (2000/2006) is not on the HAL abstracts; only
  Morley's "every trajectory with a starting value below 10^8" is explicit.
- Belaga–Mignotte's new conjectures (number of cycles as a function of d, "Collatz numbers" 2^l − 3^k) are only
  described generically in Lagarias's annotations; the 57-page preprint would need to be read for their statements.
- HAL's human pages (hal.science / hal.archives-ouvertes.fr) are behind an Anubis bot wall; only the HAL API worked.

## Strand C — Collatz as string-rewriting termination (Yolcu–Aaronson–Heule)

### Takeaway
YAH (CADE-28 2021; J. Automated Reasoning 67 (2023), art. 15) built an 11-rule mixed binary–ternary SRS T whose
termination is equivalent to the Collatz conjecture, proved that Zantema's unary system Z admits no natural-matrix
termination proof (even with dependency pairs), and automatically proved several weakenings (W′, Farkas' variant,
all 11 single-rule-deleted subsystems of T, all residue classes mod 4, classes 2,3,4,6 mod 8) with their own
SAT-based prover (github.com/emreyolcu/rewriting-collatz). The open "challenge" variants (classes 0,1,5,7 mod 8,
$500 each; W′′; the busy-beaver system BB) have, as far as I can find, not been resolved and no substantive
follow-up using termination tools has appeared through Oct 2026; the only related 2026 item is Carelli's ICALP paper
linking loop termination to generalized Collatz maps.

### Cited Findings
- Bibliographic record: Emre Yolcu, Scott Aaronson, Marijn J. H. Heule, "An Automated Approach to the Collatz
  Conjecture", arXiv:2105.14697 (v1 31 May 2021, v2 20 Aug 2022, v3 31 Dec 2022); conference version CADE-28, LNCS
  12699 (Springer, 2021), DOI 10.1007/978-3-030-79876-5_27; journal version J. Automated Reasoning 67, art. 15 (2023),
  DOI 10.1007/s10817-022-09658-8; short version "Mixed Base Rewriting for the Collatz Conjecture", WST 2021. NSF grant
  CCF-2006363. — primary-confirmed from [arXiv abs](https://arxiv.org/abs/2105.14697),
  [Springer CADE chapter](https://link.springer.com/10.1007/978-3-030-79876-5_27),
  [Springer JAR](https://link.springer.com/10.1007/s10817-022-09658-8), [WST21 PDF](https://www.cs.cmu.edu/~mheule/publications/WST21.pdf)
- Reformulation (exact): the 11-rule SRS T over alphabet {f, t, 0, 1, 2, ◁, ▷} (f/t = binary digits, 0/1/2 =
  ternary digits in a mixed binary–ternary representation): dynamic rules D_T = {f▷ → ▷, t▷ → 2▷}; auxiliary rules
  A = {f0 → 0f, f1 → 0t, f2 → 1f, t0 → 1t, t1 → 2f, t2 → 2t}, B = {◁0 → ◁t, ◁1 → ◁ff, ◁2 → ◁ft}; X = A ∪ B
  "push binary symbols towards the rightmost end ... by swapping the bases of adjacent positions without changing the
  represented value". Rewriting stops at ◁▷ (the representation of 1). "Theorem 3.17. T is terminating if and only
  if T is convergent (i.e., the Collatz conjecture holds)." A hybrid variant L (Theorem 3.19) is also equivalent.
  Lemma 3.16: termination on canonical strings ◁(f|t|0|1|2)*▷ suffices. — primary-confirmed from the full paper
  [emreyolcu.com/research/rewriting-collatz.pdf](https://emreyolcu.com/research/rewriting-collatz.pdf)
- Negative result: Zantema's unary system Z (5 symbols, 7 rules: h11 → 1h, 11h⋄ → 11s⋄, 1s → s1, ⋄s → ⋄h, h1⋄ →
  t11⋄, 1t → t111, ⋄t → ⋄h; [Zantema 2005, Theorem 16]: Z terminating iff Collatz). "Theorem 3.8. Let Σ = {1, ⋄, h,
  s, t}. There exists no collection [·]_Σ of natural matrix interpretations of any dimension d satisfying the
  requirements for an extended monotone Σ-algebra such that for at least one rule ℓ → r ∈ Z we have [ℓ](x) > [r](x)
  for all x ∈ N^d, and for the remaining ℓ′ → r′ ∈ Z we have [ℓ′](x) ≳ [r′](x)"; Theorem 3.10 extends this to the
  dependency-pair setting (SN(DP(Z)top/Z)); analogues hold for Z^rev and for Zantema's W = {h11 → 1h, 1h⋄ → 1t⋄, 1t
  → t111, ⋄t → ⋄h} (TPDB z079), which simulates the trivially convergent W(n) = 3n/2 (n even), 1 (n odd) and whose
  termination "has yet to be proved via automated methods". — primary-confirmed, [full paper](https://emreyolcu.com/research/rewriting-collatz.pdf), [WST21](https://www.cs.cmu.edu/~mheule/publications/WST21.pdf)
- Positive automated results: Theorem 4.1 SN(W′) (mixed-base version of W; 2-dimensional natural interpretations
  shown explicitly, "found in less than a second"); Farkas' variant F′ (n/3 if n ≡ 0 mod 3; (n+1)/2 if n ≡ 1 mod 4;
  (3n+1)/2 if n ≡ 3 mod 4, [Far05]) via a Collatz-like F — automated proof, "also able to find automated proofs via
  arctic matrix interpretations" (Theorem 4.2 gives the hand induction); Section 4.3 "we considered the 11
  subsystems obtained by leaving out a single rewriting rule from T, and we found termination proofs via matrix
  interpretations for all of the 11 subproblems" (Table 1 lists the smallest natural/arctic dimensions per removed
  rule, up to 5; search timeout 30 s, matrices up to dimension 7); Section 4.4 the accelerated odd map S(n) =
  (3n+1)/4 (n ≡ 1 mod 8), (n−1)/4 (n ≡ 5 mod 8), (3n+1)/2 (n ≡ 3 mod 4) — "surprisingly difficult Collatz-like
  problems"; Section 4.5: "Theorem 4.9. If there exists a nonconvergent Collatz trajectory, it cannot avoid any of the
  residue classes modulo 4"; "Theorem 4.10. ... it cannot avoid the residue classes of 2, 3, 4, 6 modulo 8"; "it
  remains open whether an analogue of Theorem 4.10 holds for the residue classes of 0, 1, 5, 7 modulo 8 ... we offer a
  $500 reward for a resolution of any of the following conjectures. Conjecture 4.11 [n ≡ 1 (mod 8)]. Conjecture 4.12
  [n ≡ 5]. Conjecture 4.13 [n ≡ 7]" (and the {1,5}, {1,7} versions were proved, the {5,7} version not). — primary-confirmed, [full paper](https://emreyolcu.com/research/rewriting-collatz.pdf)
- Variants that resisted: W′′ = {f▷ → 0▷} ∪ X′ ("we were unable to find an automated proof of termination for
  W′′"); the ternary–quinary busy-beaver system BB in Appendix C.2 ("We were unable to prove the termination of this
  system, so we include it as yet another challenge"); the mod-8 classes 0, 1, 5, 7; T itself. Other appendix
  encodings: Mahler's 3/2 problem (C.1), Erdős's ternary-expansions-of-2^n conjecture (C.3). — primary-confirmed,
  [full paper](https://emreyolcu.com/research/rewriting-collatz.pdf)
- Tools: "we chose to implement our own minimal prover ... AProVE, Matchbox, TTT2 ... at least for the rewriting
  systems of the specific form in this paper it appears that the method of matrix interpretations is the most
  effective ... one of the most difficult instances ... appears to require arctic matrix interpretations in all the
  proofs that we (and the authors of AProVE and Matchbox) could find"; large-scale runs on AWS EC2 m5.metal; SAT
  finding: phase-saving hurts, negative branching helps (Section 4.6). — primary-confirmed, [full paper](https://emreyolcu.com/research/rewriting-collatz.pdf)
- Repository: github.com/emreyolcu/rewriting-collatz — Python/NumPy prover (natural, arctic and tropical matrix
  interpretations in the extended/weakly monotone Σ-algebra framework) using CaDiCaL (scripts also for Kissat,
  MiniSat); directories prover/, rules/ (e.g. collatz-T.srs, z086.srs), relative/, proofs/; scripts proofs.sh,
  subsystems.py, negative-shuffle.py, tpdb-convert.py; 7 commits, 13 stars. — primary-confirmed from
  [GitHub](https://github.com/emreyolcu/rewriting-collatz) and the paper
- Author's later talk: "Encoding Collatz-like problems into termination of string rewriting", Dagstuhl, June 2023
  (slides at emreyolcu.com/talks/encoding-collatz.pdf). No later Collatz paper by Yolcu is listed on his page. —
  primary-confirmed from [emreyolcu.com](http://emreyolcu.com/)
- Citation sweep (Semantic Scholar, 15 citing papers as of fetch): none on string rewriting or matrix
  interpretations; Collatz-related citers are Ebnenasir "Specifying and Verifying the Convergence Stairs of the
  Collatz Program" (arXiv:2403.04777, 2024), Riaño-Rojas "An optimal convergent Collatz algorithm" (arXiv:2308.01214,
  2023; restates YAH), Tiwari "A Conjecture Equivalent to the Collatz Conjecture" (arXiv:2108.06922), Sharipov
  (arXiv:2202.04441), Knight "A Small Collatz Rule without the Plus One" (Complex Systems 2026), Heule "Easier variants
  of notorious math problems" (2021), Rahnama (arXiv:2512.00081, machine-checked termination theory). — secondhand
  from the [Semantic Scholar citations API](https://api.semanticscholar.org/graph/v1/paper/arXiv:2105.14697/citations?fields=title,year,authors,venue,externalIds&limit=200)
- 2026 follow-on in a different direction: Mishel Carelli, "Loop Termination and Generalized Collatz Sequences",
  arXiv:2605.15094 (14 May 2026), accepted to ICALP 2026: termination of one-variable linear-constraint loops over
  the integers is decidable in polynomial time assuming a "Reachability Conjecture" for weak generalized Collatz
  mappings (proved for d = 2); conversely any decision procedure would settle specific open Collatz-type instances; a
  one-variable loop with a cyclic trace has one of length ≤ 2. Whether it cites YAH is not visible on the abstract
  page. — primary-confirmed abstract, [arXiv:2605.15094](https://arxiv.org/abs/2605.15094)
- Termination Competition context: TPDB contains problems "whose termination behavior corresponds to famous
  mathematical problems, e.g., Collatz conjecture" (Zantema's z079/z086 family); 2022–2025 competitions ran on
  StarExec with 300 s wall-clock; no evidence found that T or its subsystems were added to TPDB or solved. —
  secondhand from [termination-portal.org](https://termination-portal.org/wiki/Termination_Competition) and the
  termtools mailing-list snippets
- Earlier rewriting precedent (for completeness): J. Błażewicz and A. Pettorossi, "Some properties of binary
  sequences useful for proving Collatz's conjecture", J. Found. Control Engr. 8 (1983), 53–63 — "the 3x+1 Problem
  interpreted as a strong termination property of a term rewriting system". — primary-confirmed from
  [bibliography I, entry 24](https://arxiv.org/abs/math/0309224)

### Inferences
- YAH's own framing is that non-unary encodings are the key; the difficulty wall is visible already at the mod-8
  residue-class questions, which are elementary number-theoretic statements. A modern compute push would mean
  (a) much larger matrix dimensions / longer SAT budgets on the three $500 conjectures and W′′, (b) trying newer
  interpretation classes the authors list as untried ([CGP10, NM11]). Expected outcome per the project's own CLAUDE
  note: negative results, not a proof.
- The absence of any 2022–2026 termination-tool follow-up (zero rewriting-related citers) means the strand is
  dormant rather than exhausted.

### Gaps
- Could not confirm whether the three $500 conjectures (classes 1, 5, 7 mod 8) or W′′/BB have been claimed solved
  anywhere; no source found either way.
- The GitHub license and last-commit date were not visible in the fetched page.
- Google Scholar "cited by" was not accessible; Semantic Scholar may be incomplete.

## Strand D — Predecessor-density exponents for 5x+1 / px+1, plus two one-line references

### Takeaway
No numerical Krasikov–Lagarias-type exponent for 5x+1 or any px+1 map was found in the literature: the only
published statement is the qualitative Kontorovich–Lagarias Theorem 7.6 (π_{a,5}(x) ≥ x^{c1} for some unspecified
c1 > 0, "well below" the predictions), and the heuristic growth exponent is their conjectured η5 ≈ 0.649–0.651
(branching random walk; Volkov's model gives ≈ 0.678) with Conjecture 7.2 asserting η5 < 1. Wirsching's LNM 1681 is
a 3n+1-only treatment.

### Cited Findings
- Alex V. Kontorovich, Jeffrey C. Lagarias, "Stochastic Models for the 3x+1 and 5x+1 Problems", arXiv:0910.1944, in:
  The Ultimate Challenge: The 3x+1 Problem (J. C. Lagarias, ed.), AMS 2010, pp. 131–188. Definition 7.7: π_{a,5}(x) =
  #{n : |n| ≤ x, T_5^(k)(n) = a for some k ≥ 0} (the source text says "3x+1 function" there, an evident typo);
  Definition 7.8: upper/lower 5x+1 growth exponents η5^±(a) = limsup/liminf log π_{a,5}(x)/log x. "Conjecture 7.2":
  for all a ≢ 0 (mod 5) the growth exponent exists, "takes a constant value" η5 independent of a, and "This value
  satisfies" η5 < 1. "Theorem 7.6 (Inverse Iterate Lower Bound). There is a positive constant c1 such that the
  following holds": for each a ≢ 0 (mod 5) there is x0(a) with π_{a,5}(x) ≥ x^{c1} for x ≥ x0(a); the proof is said
  to follow because "the inverse tree methods for the 3x+1 problem carry over to the 5x+1 problem, so that one can
  obtain a result qualitatively of the following type, by similar proofs" (citing the Applegate–Lagarias tree
  methods); on c1: "we suspect it is well below either of the above predictions", so it cannot discriminate between
  them. Numerical predictions: the repeated random walk and a branching random walk model "both suggest the value"
  η5 ≈ 0.649; "A different branching random walk model formulated by Volkov" suggests η5 ≈ 0.678; "There is some
  controversy concerning the conjectured value of the constant." §1.3 states the count of n ≤ x whose 5x+1 orbit
  contains 1 is "about x^{η5+o(1)}, where η5 ≈ 0.65049" (elsewhere in the overview written δ5 ≈ 0.65041 — the two
  values differ in the 5th digit) and that integers reaching 1 do so in at most (γ_{5,BP} + o(1)) log x steps with
  γ_{5,BP} ≈ 84.76012. A search snippet from the same paper gives the branching-process constant as "η_{5,BP} ≈
  0.650919 is the maximum value of f(a) taken over the interval 0 ≤ a < (1/6) log(64/5)". — primary-confirmed from the
  [ar5iv rendering of arXiv:0910.1944](https://ar5iv.labs.arxiv.org/html/0910.1944) (two partial reads) and the
  [arXiv abstract page](https://arxiv.org/abs/0910.1944); the 0.650919 formula is secondhand (search snippet).
- Stanislav Volkov, "A probabilistic model for the 5k+1 problem and related maps", Stochastic Processes and their
  Applications 116 (2006), no. 4, 662–674: a randomly labelled binary tree model "mimicking" the 5x+1 inverse
  iteration; Lagarias's bibliography II describes the empirical picture it addresses as "the count of starting values
  n ≤ x whose orbit reaches 1 under the 5x+1 map appears to scale like x^α with α roughly 0.68". — secondhand
  (IDEAS/RePEc record and search snippet of bibliography II), [IDEAS record](https://ideas.repec.org/a/eee/spapps/v116y2006i4p662-674.html)
- Lagarias, "The 3x+1 Problem: An Overview" (arXiv:2111.02635, from the 2010 AMS volume): defines T_5, states that
  stochastic models "predict that almost all orbits should 'escape to infinity'", that it "remains an unsolved
  problem to prove that there exists even one trajectory for the 5x+1 problem that 'escapes to infinity'", cites
  Wirsching's LNM 1681 only as the dynamical-systems treatment of 3n+1, restates Krasikov–Lagarias x^0.84 and the
  "infinite family of nonlinear programs of increasing complexity", and poses as open whether c(ε)x^{1−ε} holds. No
  5x+1 predecessor exponent appears there. — primary-confirmed from [ar5iv 2111.02635](https://ar5iv.labs.arxiv.org/html/2111.02635)
- Krasikov–Lagarias 3x+1 lineage, for comparison: Applegate–Lagarias, "Density bounds for the 3x+1 problem II.
  Krasikov inequalities", Math. Comp. 64 (1995), 427–438: π_a(x) > x^0.809 "derived by computer for such a nonlinear
  program having about 20000 variables" (the AMS page lists the exponent as .804, a version/rounding discrepancy);
  Krasikov–Lagarias 2003: x^0.84. — primary-confirmed from [bibliography I, entry 7](https://arxiv.org/abs/math/0309224)
  and [AMS Math. Comp. page](https://www.ams.org/mcom/1995-64-209/S0025-5718-1995-1270613-2/)
- Wirsching's book: Günther J. Wirsching, "The Dynamical System Generated by the 3n+1 Function", Lecture Notes in
  Math. 1681, Springer 1998 (= "Wirsching (1998a)" in Lagarias). Related: Wirsching, "On the problem of positive
  predecessor density in 3N+1 dynamics", Discrete Contin. Dyn. Syst. 9 (2003), no. 3, 771–787 — "formulates three
  conjectures which, if proved, would establish" positive predecessor density; Wirsching, "Balls in constrained urns
  and Cantor-like sets", Z. Anal. Anwend. 17 (1998), 979–996 — the integral equation φ(x) = q/(q−1)∫_{qx−q+1}^{qx}
  φ(y)dy with q = 3 for the 3x+1 case. Everything found concerns 3n+1 only. Tavares, arXiv:2608.27617 (Aug 2026)
  claims proofs of Wirsching's Conjectures 1 and 3 (3n+1). — primary-confirmed from
  [bibliography II, entries 120–122](https://arxiv.org/abs/math/0608208) and [bibliography I, entry 187](https://arxiv.org/abs/math/0309224);
  Tavares secondhand from search ([arXiv:2608.27617](https://arxiv.org/pdf/2608.27617))
- Computational 5x+1 data: Tomás Oliveira e Silva, "Computational verification of the 5x+1 and 7x+1 conjectures"
  (page dated 28 Dec 2015): for the variant T_5 that divides by 2 or 3 when possible and otherwise maps x ↦ 5x+1, all
  starts below 10 000 002 894 004 224 ≈ 1.0·10^16 were checked (7x+1 analogue to ≈ 1.0·10^16); maximum-excursion
  records scale like n^ρ with ρ5 = 1.442762198279 (Markov-chain model after Lagarias–Weiss). The page gives no count
  or exponent for the number of starts reaching 1. — primary-confirmed from [sweet.ua.pt/tos/px+1.html](https://sweet.ua.pt/tos/px+1.html)
- Heuristic 5x+1 "tree growth": Lagarias's bibliography (Feix–Muriel–Merlini–Tartini 1995) records the 3x+1 analogue
  — inverse-iterate trees with ≈ A(4/3)^k leaves at depth k; the corresponding 5x+1 branching factor is the input to
  Kontorovich–Lagarias's η5. — primary-confirmed from [bibliography I, entry 59](https://arxiv.org/abs/math/0309224)
- One-line references requested: Marc Chamberland, "A Continuous Extension of the 3x+1 Problem to the Real Line",
  Dynamics of Continuous, Discrete and Impulsive Systems 2 (1996), 495–509 (MR 97f:39031): iterates of f(x) = x +
  1/4 − (x/2 + 1/4)cos(πx) interpolating T; negative Schwarzian derivative; on [μ1, μ3] = [0.27773…, 2.44570…] a.e.
  point is attracted to the cycles A1 = {1, 2} or A2 = {1.19253…, 2.13865…}; μ3 is a homoclinic point. — primary-confirmed,
  [bibliography I, entry 35](https://arxiv.org/abs/math/0309224)
- Daniel J. Bernstein, Jeffrey C. Lagarias, "The 3x+1 Conjugacy Map", Canadian J. Math. 48 (1996), 1154–1169 (MR
  98a:11027): the map Φ: Z_2 → Z_2 (inverse of Q_∞ from Lagarias 1985) conjugating the 2-adic shift to T; Φ mod 2^n is
  a permutation of order 2^(n−4) for n ≥ 6; Φ has odd fixed points −1 and 1/3 and the 2-cycle {1, −1/3}, conjectured
  to be the only odd fixed points; the analogous "25x−3" conjugacy has no nonzero fixed points. — primary-confirmed,
  [bibliography I, entry 23](https://arxiv.org/abs/math/0309224)

### Inferences
- The 5x+1 predecessor problem is structurally identical to the K–L setup (inverse tree, residue classes mod 5^k
  instead of 3^k, branching when (x−1)/5 is integral), so the project's LP machinery could produce the first explicit
  lower exponent c1 for 5x+1. Because the conjectured truth is η5 ≈ 0.65 < 1, the interesting output would be how
  close a finite-k LP gets to 0.65 — a test of the method's convergence (λ_k → 2 question) in a setting where the
  target is strictly below 1. Nobody appears to have done this (Kontorovich–Lagarias explicitly left c1 unspecified).
- The two heuristic values (0.649/0.651 vs 0.678) differ by more than the K–L method's typical per-k gains, so even a
  moderately good LP bound (say > 0.55) would be publishable as the first rigorous constraint; a bound > 0.651 would
  refute the Kontorovich–Lagarias prediction in favour of Volkov's.

### Gaps
- Section 8 of Kontorovich–Lagarias (the derivation of η5 ≈ 0.649 and the formula max f(a)) could not be read in
  full (ar5iv truncation; arXiv PDF returned 403 on the last attempt); the 0.650919 value and the f(a) formula are
  from a search snippet only.
- Volkov's paper is paywalled; the 0.678 figure is confirmed only via Kontorovich–Lagarias's citation of it.
- No source was found stating a predecessor-density exponent for general px+1 (p = 7, 11, …) beyond the qualitative
  "carry over" remark; nothing in Wirsching's book or Lagarias's bibliographies addresses px+1 predecessor trees
  quantitatively.
- Lagarias's bibliography entry for Wirsching (1998a) itself was not located in the extracted text (only cross-
  references), so the book's exact scope is taken from the 2010 overview's citation.
