# Lower bounds for non-trivial 3x+1 cycles and the computational verification range (state as of 2026-10-08)

Conventions used below. T(n) = n/2 (n even), (3n+1)/2 (n odd) is the "shortcut" map; C(n) = n/2, 3n+1 is the
unaccelerated Collatz map. For a hypothetical cycle: K = number of odd members (o-steps), L = number of even
members (e-steps), so the T-period is K+L and the C-period is 2K+L. m = number of local minima ("m-cycle",
Simons–de Weger terminology). δ = log 3/log 2. p_n/q_n = convergents of δ (OEIS A005663 numerators); indexing
p_0/q_0 = 1/1, ..., p_13/q_13 = 301994/190537, p_15/q_15 = 17087915/10781274, p_16 = 85137581,
p_19 = 630138897, p_21/q_21 = 10439860591/6586818670, p_22/q_22 = 103768467013/65470613321,
p_23/q_23 = 217976794617/137528045312, p_24/q_24 = 1193652440098/753110839881 (recomputed locally with mpmath;
agrees with OEIS A005663 — [OEIS A005663](https://oeis.org/A005663)). NB: Halbeisen–Hungerbühler use a different
index convention (their p_14 = 301994, p_16 = 17087915, p_18 = 102225496 = 85137581 + 17087915, i.e. they include
an intermediate fraction).

Provenance key: [PRIMARY] = number read directly from the primary source (PDF text extracted locally or page fetched);
[SECONDARY] = quoted from another source (Lagarias's bibliography, Hercher's introduction, Wikipedia, GitHub);
[UNVERIFIED] = could not be checked at all.

Local copies of the primary PDFs used (session scratchpad, temporary):
`/private/tmp/claude-501/-Users-daniel-devel-kollatz/5dbd70ce-fd1a-4829-8257-0deb71d8ab46/scratchpad/pdfs/`
(hercher2023.pdf, hercher_corrigendum.pdf, hercher_wurzel.pdf, sdw2005.pdf, sdw2010.pdf, barina2025.pdf,
halbeisen1997.pdf, lagarias1.pdf, lagarias2.pdf, angeltveit2026.pdf, bouhamidi2026.pdf, plus .txt extractions).

## 1. Eliahou (1993): exact statement, the bound 17 087 915 and the 2^40 verification bound

### Takeaway
Eliahou, Discrete Math. 118 (1993) 45–56, proves that any nontrivial T-cycle has period
p = 301994a + 17087915b + 85137581c (a, b, c ≥ 0, b ≥ 1, ac = 0), hence period ≥ 17 087 915, using the continued
fraction of log_2 3 and the verification of the conjecture below 2^40. The 2^40 input is confirmed by two
independent primary-adjacent sources (Lagarias's annotated bibliography and Halbeisen–Hungerbühler, who state
k(2^40) = 17 087 915); the Elsevier full text itself was not accessible (HTTP 403).

### Cited Findings
- Bibliographic data: S. Eliahou, "The 3x+1 problem: new lower bounds on nontrivial cycle lengths", Discrete
  Mathematics 118 (1993), no. 1–3, 45–56, DOI 10.1016/0012-365X(93)90052-U; abstract: any nontrivial cyclic orbit
  under iteration of T must contain at least 17 087 915 elements. [PRIMARY: publisher abstract via UNIGE record] —
  [UNIGE archive ouverte](https://archive-ouverte.unige.ch/unige:12087)
- Lagarias's annotation (entry 53 of the 1963–1999 bibliography): "any nontrivial cycle on Z+ of the 3x+1 function
  T(x) has period p = 301994A + 17087915B + 85137581C with A,B,C nonnegative integers where B ≥ 1, and at least one of
  A or C is zero. Hence the minimal possible period length is at least 17087915. The method uses the continued
  fraction expansion of log_2 3, and the truth of the 3x+1 Conjecture for all n < 2^40." (MR 94h:11017)
  [SECONDARY, but authoritative] — [Lagarias, arXiv:math/0309224](https://arxiv.org/abs/math/0309224)
- Halbeisen–Hungerbühler restate Eliahou's criterion as Theorem 2: if k(m) is the smallest k with
  k/n(k) ≤ log_2(3 + 1/m) then |C| ≥ k(min C) for every Collatz cycle C in N, and: "Using the theory of continued
  fractions Eliahou showed that k(2^40) = 17 087 915". They also note that Crandall's earlier estimate with the same
  2^40 verification gave only l ≥ 301 994 (attributed to Lagarias [5]). [PRIMARY for H–H's text] —
  [Halbeisen–Hungerbühler PDF](https://math.ch/norbert.hungerbuehler/publications/Optimal_bounds_for_the_length_of_rational_Collatz_cycles.pdf)
- Crandall, "On the 3x+1 problem", Math. Comp. 32 (1978) 1281–1292, is the origin of the convergent argument
  (Lemma: n > min(q_k, 2m/(q_k+q_{k+1}))). [SECONDARY via H–H and OEIS A005663 reference] —
  [OEIS A005663](https://oeis.org/A005663)
- 17 087 915 is p_15 (numerator of a convergent of log_2 3); 301994 = p_13, 85137581 = p_16. [PRIMARY: OEIS
  A005663 lists 1, 2, 3, 8, 19, 65, 84, 485, 1054, 24727, 50508, 125743, 176251, 301994, 16785921, 17087915,
  85137581, 272500658, 357638239, 630138897, 9809721694, 10439860591, 103768467013, 217976794617, ...] —
  [OEIS A005663](https://oeis.org/A005663)
- Later re-applications of Eliahou's criterion with bigger X0 (all secondary unless noted):
  Sinisalo (2003+ preprint, Oulu): period ≥ 630 138 897 using Oliveira e Silva's 2.70×10^16 [SECONDARY, Lagarias
  bib II entry 105] — [arXiv:math/0608208](https://arxiv.org/abs/math/0608208);
  Lagarias, "The 3x+1 problem: an overview" (in The Ultimate Challenge, AMS 2010, pp. 3–29), record (W2): the
  trivial cycle is the only cycle with period < 10 439 860 591 and the only one with < 6 586 818 670 odd integers,
  citing Eliahou [Theorem 3.2] with X0 = 20×2^58 ≈ 5.7646×10^18 (record W1) [PRIMARY, local copy
  lagarias_overview2021.txt] (10 439 860 591 = p_21, 6 586 818 670 = q_21);
  Martiny (Pittsburgh talk, 2015): "improved to 10,439,860,591" with n < 5·2^60 [SECONDARY] —
  [Pitt math talk page](https://www.mathematics.pitt.edu/node/2786).

### Inferences
- Eliahou's structure theorem is exactly the statement that (K+L)/K must be an upper semiconvergent of log_2 3 with
  the admissible numerators determined by X0; the project's own `cycles.py` reproduces n ≥ 17 087 915 at B = 40 and
  630 138 897 at B = 60, consistent with Eliahou and Sinisalo respectively.

### Gaps
- Could not read Eliahou's full text (ScienceDirect returned 403; zbMATH blocked). The received date, the exact
  wording of the theorem (number 3.2 per Lagarias 2010) and the convergent table are therefore quoted secondhand.

## 2. Simons & de Weger (Acta Arith. 2005 and the 2010 update): which m excluded, which X0

### Takeaway
The published Acta Arith. 117 (2005) 51–70 paper excludes nontrivial m-cycles for 1 ≤ m ≤ 68 with
X0 ≈ 3.39×10^17 (Roosendaal, Nov 2004); the authors' web update v1.41 pushed this to m ≤ 74 and v1.44
(31 Aug 2010) to m ≤ 75 using Oliveira e Silva's X0 = 5·2^60 > 5.7646·10^18. Hence "m ≥ 76" (as cited by Hercher)
refers to the 2010 preprint, "m ≥ 69" to the journal version.

### Cited Findings
- Bibliographic: J. Simons, B. de Weger, "Theoretical and computational bounds for m-cycles of the 3n+1-problem",
  Acta Arithmetica 117 (2005), 51–70, DOI 10.4064/aa117-1-3, MSC 11B83. [PRIMARY] —
  [IMPAN journal page](https://www.impan.pl/en/publishing-house/journals-and-series/acta-arithmetica/all/117/1/82263/theoretical-and-computational-bounds-for-m-cycles-of-the-3n-1-problem)
- 2005 version, §1.3: "At the moment of writing this (November 10, 2004) it is known from extensive distributed
  computations [Ro] that xmin > X0 = 301 250 [·2^? — exponent lost in PDF extraction] > 3.3889·10^17"; the
  rate of progress then was "about 3·10^14 per day". [PRIMARY, local sdw2005.txt; the multiplier's power of two
  did not survive extraction — Roosendaal reported in units of 2^50 at the time, and 301 250·2^50 ≈ 3.39·10^17]
- Lagarias's annotation of the 2005 paper (bib II, entry 101): "there are no non-trivial such cycles on the
  positive integers for 1 ≤ m ≤ 68, and strong constraints are put on any such cycle of length at most 72 ...
  they use a transcendence result of G. Rhin [Progress in Math. 71 (1987), 155–164] ... [Subsequent to publication,
  the authors showed there are also no nontrivial such cycles for 69 ≤ m ≤ 74, see
  http://www.win.tue.nl/~bdeweger/3n+1_v1.41.pdf]". [SECONDARY, authoritative] —
  [arXiv:math/0608208](https://arxiv.org/abs/math/0608208)
- Wikipedia summarises the journal version as "no k-cycle up to k = 68". [SECONDARY] —
  [Wikipedia, Collatz conjecture](https://en.wikipedia.org/wiki/Collatz_conjecture)
- 2010 preprint v1.44 (31 Aug 2010), abstract: "we prove that there do not exist nontrivial m-cycles for
  1 ≤ m ≤ 75"; footnote: "Version 1.3 of this paper has been published in Acta Arithmetica, Vol. 117, pp. 51–70,
  2005"; "The main improvements in this version 1.44 over version 1.3 are due to impressive computational work by
  Tomás Oliveira e Silva." [PRIMARY] — [de Weger's PDF](https://deweger.net/papers/[35a]SidW-3n+1-v1.44[2010].pdf)
- 2010 §1.3: "At the moment of writing this (August 31, 2010) it is known from extensive computations by Tomás
  Oliveira e Silva [OS] that xmin > X0 = 5·2^60 > 5.7646·10^18. Eric Roosendaal's independent computations [Ro]
  have reached xmin > 890×2^50 > 1.0020·10^18." [PRIMARY, same PDF]
- 2010 Theorem 3 (Main Theorem): (a) [Brox] finitely many m-cycles for each m; (b) no nontrivial m-cycles for
  1 ≤ m ≤ 75; (c) for 76 ≤ m ≤ 77 the only possible cycles have xmin > 5.7646·10^18 and (K, L, xmin) in an explicit
  list of three (m = 76) resp. four (m = 77) rows, e.g. K = 117 972 833 293 231 014, L = 69 009 683 580 368 485;
  (d) for 78 ≤ m ≤ 90: 1.1173·10^17 < K < 1.3993 m δ^m; for 91 ≤ m ≤ 515 619: 7.5311·10^11 < K < 1.4784 m δ^m,
  5.7646·10^18 < xmin < 5.1825·10^7 m^2 δ^m; for 515 620 ≤ m ≤ 527 875 034: 9.0240·10^8 < K < 15.109 m δ^m;
  for m ≥ 527 875 035: 1.7095 m < K < 15.108 m δ^m. "We expect that ... m = 76 and m = 77 can be expected to be
  solved within 30 years". [PRIMARY, same PDF]
- 2010 Corollary 11 (lower bounds on K from convergents): e.g. 30 ≤ m ≤ 333 ⇒ K > q_31 > 5.7509×10^15;
  648 402 ≤ m ≤ 4 486 354 ⇒ K > q_23 > 1.3752×10^11; 55 451 900 ≤ m ≤ 312 750 582 ⇒ K > q_20 > 6.1892×10^9.
  [PRIMARY, same PDF]
- Transcendence input (2010 §5): "For general linear forms x log a + y log b ... the best results today are
  Laurent, Mignotte and Nesterenko [LMN] for small x, y, and for large x, y that of Matveev [Ma] ... For our
  specific case x log 2 + y log 3 however, the result of Rhin [Rh] is best." Lemma 12: Λ > e^{−13.3(0.46057 + log K)}
  ("We apply the Proposition on p. 160 of [Rh] with u0 = 0, H = u1 = K+L, u2 = −K"). Rhin = G. Rhin,
  "Approximants de Padé et mesures effectives d'irrationalité", Progress in Mathematics 71 (1987), 155–164.
  [PRIMARY, same PDF]
- Related: J. L. Simons, "On the nonexistence of 2-cycles for the 3x+1 problem", Math. Comp. 74 (2005) 1565–1572
  (uses LMN); Steiner (1978) excluded 1-cycles. [SECONDARY, Lagarias bib II entries 94, 101; AMS page] —
  [AMS Math. Comp.](https://www.ams.org/mcom/2005-74-251/S0025-5718-04-01728-4/)

### Inferences
- The project's Eliahou-style pair list and the SdW Corollary 11 thresholds agree: q_23 = 137 528 045 312 ≈ 1.3752·10^11
  is the "next threshold" that Hercher later targets.

### Gaps
- The exact X0 multiplier in the 2005 journal version (301 250·2^50 vs other unit) is inferred, not read cleanly.
- The intermediate v1.41 (m ≤ 74) file at win.tue.nl was not fetched; only Lagarias's description is available.

## 3. Hercher (JIS 2023, arXiv:2201.00406): X0 used, cycle-length bound, next-pair statement, 2026 corrigendum

### Takeaway
Hercher proves m ≥ 92 using X0 = 695·2^60 ≈ 8·10^20 (JIS version; the arXiv v3/ar5iv text says 704·2^60) — not
2^68 and not 3·2^69. The value 3·2^69 = 1536·2^60 appears only in Corollary 29: if X0 ≥ 3·2^69 then every
nontrivial cycle has K > 1.375·10^11 odd members (i.e. the pair (p,q) = (114 208 327 604, 72 057 431 991) is
excluded and K ≥ q_23 = 137 528 045 312). Since Barina reached 2^71 > 3·2^69 in Jan 2025, this corollary is now
unconditional. A corrigendum dated 14 June 2026 fixes an error in the proof of Theorem 21; the m ≤ 91 result is
stated to stand.

### Cited Findings
- Bibliographic: C. Hercher, "There are no Collatz m-cycles with m ≤ 91", Journal of Integer Sequences 26 (2023),
  Article 23.3.5, 22 pp.; received Jan 23 2022, revised Jan 24 2022 / Dec 21 2022 / Dec 28 2022 / Mar 12 2023,
  published Mar 15 2023; arXiv:2201.00406 v1 2 Jan 2022, v2 23 Jan 2022, v3 4 Apr 2023; Zbl 1536.11052
  (reviewer O. Rozier); MSC 11B83, 11B37. [PRIMARY] — [JIS article page](https://cs.uwaterloo.ca/journals/JIS/VOL26/Hercher/hercher5.html),
  [arXiv abs](https://arxiv.org/abs/2201.00406), [zbMATH API](https://api.zbmath.org/v1/document/_search?search_string=ti%3A%22There%20are%20no%20Collatz%20m-cycles%22)
- Version history of the claim: v1 title "m ≤ 90"/abstract m ≥ 91; v2 "m ≤ 90"; v3 and JIS: m ≥ 92. [PRIMARY arXiv
  listing; SECONDARY for v1/v2 wording] — [arXiv v2](https://arxiv.org/abs/2201.00406v2), [arXiv v3](https://arxiv.org/abs/2201.00406v3)
- Abstract (JIS/v3): "Simons and de Weger proved m ≥ 76. With newer bounds on the range of starting values for
  which the Collatz conjecture has been checked, one gets m ≥ 83. In this paper, we prove m ≥ 92. Furthermore, we
  examine what would be needed to prove that the number of odd members of a nontrivial cycle is at least
  K ≥ 1.375·10^11. We prove that it suffices to show that, for every integer smaller than or equal to
  1536·2^60 = 3·2^69, the respective Collatz sequence enters the trivial cycle. This reduces the range of numbers
  to be checked by nearly 60%." [PRIMARY] — [arXiv abs](https://arxiv.org/abs/2201.00406)
- Definition 4 (JIS text): "We define X0 as the largest number for which it is known that for all positive integers
  n ≤ X0 their Collatz sequences reach the trivial cycle. As of the date of writing this paper, we have
  X0 = 695·2^60." Proof of Theorem 23: "With X0 = 695·2^60 ≈ 8·10^20". [PRIMARY, local hercher2023.txt]. The
  ar5iv rendering of the arXiv version gives X0 = 704·2^60 instead. [PRIMARY for ar5iv text] —
  [ar5iv](https://ar5iv.labs.arxiv.org/html/2201.00406). (Both ≈ 2^69.4; neither is 2^68 or 3·2^69.)
- History paragraph (JIS §1): Eliahou proved "K > 10^7 o-steps"; "This bound was subsequently improved by Hercher
  and Puchert [4, 5, 9] to the current K > 7.2·10^10"; "Simons and de Weger [11] proved that m ≥ 68 ... they
  estimated that bounds on m like m ≥ 77 were unlikely to be obtained before the year 2419. In an updated version
  [12] in 2010 ... m ≥ 76 ... m ≥ 83 could not be reached before the year 2429 ... In 2018, Hercher [4, 5] ...
  proved that m ≥ 77. With the current best bound on X0, Simons and de Weger [11, 12] suggested that with methods
  of their paper m ≥ 83 could be proven." [PRIMARY]
- Theorem 23 (Main Theorem): "There is no m-cycle with m ≤ 91." Proof iterates Theorem 21 + continued fractions
  (Lemma 22) starting from K > 7·10^11 (SdW Theorem 3): m2 ≥ 47, δ < (K+L)/K < δ + 6.9·10^−32 ⇒ K > 5.2·10^15;
  then K > 3.97·10^17, 4.64·10^18, 2.74·10^19, 7.76·10^19, 2.05·10^20, finally m2 ≥ 91,
  (K+L)/K < δ + 1.11·10^−43 ⇒ K > 7.94·10^21, contradicting SdW's upper bound K < 1.4784 m δ^m < 2.2·10^20.
  [PRIMARY]
- Corollary 24 / Table 1 (lower bounds on K if m ≤ ...): m ≤ 98: 7.76·10^19; 117: 2.74·10^19; 276: 4.68·10^18;
  3079: 3.97·10^17; 12055: 1.30·10^17; ...; 948987: 4.30·10^15; 1.14·10^6: 3.81·10^15; ...; 1.33·10^9: 1.64·10^12;
  1.54·10^9: 8.90·10^11; 9.46·10^9: 1.37·10^11; "For all m ∈ N: 7.20·10^10". [PRIMARY]
- Lemma 8: if n, C(n), ..., C^{k−1}(n) are all odd then n ≡ −1 (mod 2^k), so n ≥ 2^k − 1. Lemma 9: if ℓ_i ≥ 2 then the
  sequences of n_i and n'_i = (n_i − 1)/2 merge, C^{k_i+2}(n_i) = C^{k_i+1}(n'_i). Remark 7: T(n_i) < 3/n_i < 3/X0.
  Lemma 26: T(n_i) < k_i·(3/4)·(1/X0) (and analogues for 2–3 consecutive blocks). Theorem 27 (independent of m):
  δ < (K+L)/K < δ + (1/(3 log 2))·(3/4)·(1/X0). [PRIMARY]
- Remark 28: with previous (Eliahou-type) methods, proving K > 1.375·10^11 "(which is the next threshold reachable)"
  needs X0 ≥ 3781·2^60; Theorem 27 lowers this to X0 ≥ 2836·2^60 (25% reduction). Corollary 29: "If
  X0 ≥ 1536·2^60 = 3·2^69 then every nontrivial cycle contains at least K > 1.375·10^11 odd numbers", proved by a C++
  program (residue classes mod powers of two, cases dropped when the smallest residue member exceeds 3781·2^60),
  "five weeks of computing time on an i9 processor of the 11th generation with 8 cores". Remark 30: Barina's
  project needed over 27 months to reach 512·2^60 = 2^69; lowering the bound by 2^60 costs only ~1.5% more
  computing. [PRIMARY]
- Corrigendum (JIS page: "Corrigendum, June 14 2026"): "The derivation of the inequalities
  T(n_{m−m2+1+ℓ}) < 3/(2^v−1)^δ in the proof of Theorem 21 at the bottom of page 14 contains an error"; it re-proves
  T(n_{m−m2+1}) + Σ T(n_i) < 3/(2^v−1) + 3(m2−1)/(2^v−1)^δ by a convexity/vertex argument. [PRIMARY] —
  [corrigendum PDF](https://cs.uwaterloo.ca/journals/JIS/VOL26/Hercher/corrigendum.pdf). The zbMATH review
  (Rozier) had already noted that Theorem 21's proof "has a potential flaw near the end" and that the main result
  "appears not to depend on Corollary 19 (computer-assisted)". [PRIMARY, zbMATH API]
- Hercher's earlier work (Die Wurzel 6/2018 118–128 and 7/2018 146–154; Flensburg preprint): verified all
  starting values ≤ 87·2^60 ≈ 1.003·10^20 (previous best 5·2^60) and proved "Satz. Ein nicht-trivialer
  Collatz-Zyklus besteht aus mehr als 17 026 679 261 ... Folgegliedern" (= p_21 + q_21, i.e. the C-period), via
  log_2(3+μ) < p_21/q_21 = 10 439 860 591/6 586 818 670 and the requirement μ < 1/(2.17·10^20). [PRIMARY] —
  [Flensburg PDF](https://www.uni-flensburg.de/fileadmin/content/abteilungen/mathematik/hercher/forschung/wurzel-artikel-collatz.pdf).
  S. Puchert, "Anmerkung zum Artikel ...", Die Wurzel 11 (2018) 243–250 [UNVERIFIED content; cited by Hercher 2023
  as co-source of K > 7.2·10^10].

### Inferences
- K > 7.2·10^10 corresponds to excluding the semiconvergent pair (p_21+p_22, q_21+q_22) = (114 208 327 604,
  72 057 431 991); the "next threshold" K ≥ 1.375·10^11 is q_23 = 137 528 045 312 with T-period p_23 = 217 976 794 617
  and C-period p_23 + q_23 = 355 504 839 929. (Arithmetic checked locally; matches Barina's and Wikipedia's figures.)
- Because 2^71 = 2048·2^60 > 1536·2^60, Corollary 29 applies unconditionally since 2025-01-15: every nontrivial
  cycle has K ≥ 137 528 045 312 odd members, T-period ≥ 217 976 794 617, C-period ≥ 355 504 839 929. Hercher's
  Theorem 23 itself was proved with X0 = 695·2^60; nobody has published a re-run of the m-iteration with 2^71.
- The m-bound of 92 is proved with X0 ≈ 2^69.4; Hercher's Table 1 shows what K-bounds the method gives for larger m.

### Gaps
- No statement found in Hercher about what X0 would exclude the pair after (p_23, q_23), i.e. force K ≥ q_24 =
  753 110 839 881; the trivial Eliahou-type requirement is roughly X0 ≳ 2^75 (project's own estimate, not a
  published figure).
- Hercher 2023 Theorem 3 of [12] = SdW 2010 is quoted as "K > 7·10^11"; the SdW text gives 7.5311·10^11 for
  91 ≤ m ≤ 515 619 — consistent, but Hercher's rounding is his own.

## 4. Barina (J. Supercomputing 2025): verified bound, date, method; any newer bound (2025–2026)

### Takeaway
Barina's project verified convergence for all n < 2^71 = 2048·2^60 on 2025-01-15 (project log and paper Table 10);
the paper (accepted 21 April 2025, J. Supercomput. 81:810) states the limit 2^71 and explicitly notes that this is
"the moment when the length of a non-trivial cycle rises to 355 504 839 929 [Hercher 2023]". The live project page
shows 2075·2^60 ≈ 2^71.02 verified (as generated 2026-10-08), with no later milestone; no 2^72 announcement exists.
A Feb 2026 preprint (Angeltveit) proposes a faster algorithm but reports no new verified bound.

### Cited Findings
- D. Barina, "Improved verification limit for the convergence of the Collatz conjecture", The Journal of
  Supercomputing 81, article 810 (2025), DOI 10.1007/s11227-025-07337-0, Accepted 21 April 2025, open access.
  Abstract: "pushes the limit for which the conjecture is verified up to 2^71 ... total acceleration ... 1 335× ...
  thousands of parallel workers running on several European supercomputers ... four new path records". [PRIMARY,
  local barina2025.txt] — [VUT publication record](https://www.fit.vut.cz/research/result/c197809/.en),
  [VUT postprint PDF](https://www.fit.vut.cz/research/publication-file/c197809/298514/s11227-025-07337-0.pdf)
- §6 Results: "we have managed to verify the convergence of the Collatz conjecture for all numbers up to the limit
  of 2^71 (which is equal to 2 048 × 2^60). This is the moment when the length of a non-trivial cycle rises to
  355 504 839 929 [12]" ([12] = Hercher 2023). Table 10 timeline: 2019-09-04 start; 2020-05-07 2^68; 2021-12-10 2^69;
  2023-07-09 2^70; 2023-11-03 1.5×2^70; 2025-01-15 2^71. [PRIMARY]
- History recap in §1 (useful citable chain): Dunn 1973 ≈ 2^24.78; Leavens–Vermeulen 1992 ≈ 2^45.67; Roosendaal
  2^60 (before 2012); Oliveira e Silva 5×2^60; yoyo@home 2017: 87×2^60 (each number checked twice, 1000
  volunteers); Honda et al. 2017 GPU 64-bit only; Barina 2019–2021: 2^68 ("From 2019 to 2021, our project [4]
  verified the convergence of all numbers below 2^68"). [PRIMARY]
- Method: baseline algorithm + sub-algorithms (3^k sieves, 2^32/2^34 sieves on CPU, 2^24 and 3^1 sieves on GPU),
  128-bit arithmetic, OpenCL on NVIDIA and AMD; best GPU implementation 52.1× faster than best CPU; work units of
  2^40 numbers; infrastructure MetaCentrum, IT4Innovations (Karolina, 128-core AMD EPYC 7H12 nodes) and LUMI (8× AMD
  MI250X per node); computational resources from e-INFRA CZ (ID 90254). Five new path records listed (the abstract
  says four), e.g. 274 133 054 632 352 106 267 ... 2 358 909 599 867 980 429 759 (OEIS A006884). [PRIMARY]
- Earlier paper: D. Barina, "Convergence verification of the Collatz problem", J. Supercomput. 77 (2021) 2681–2688,
  DOI 10.1007/s11227-020-03368-x (2^68 reached 2020-05-07). [PRIMARY for DOI/pages via project page; 2^68 from the
  2025 paper] — [project page](https://pcbarina.fit.vutbr.cz/)
- Live project page (generated 2026-10-08): "The convergence of all numbers below 2075 × 2^60 (≈ 2^71.02) has been
  verified"; target 2076×2^60; lowest incomplete work unit 17.87% into it; log's last entry 2025-01-15; code at
  github.com/xbarin02/collatz. [PRIMARY] — [pcbarina.fit.vutbr.cz](https://pcbarina.fit.vutbr.cz/)
- GitHub README gives no numeric limit, only that the programs check 128-bit numbers and cite both J. Supercomput.
  papers. [PRIMARY] — [xbarin02/collatz](https://github.com/xbarin02/collatz)
- No 2^72 or 2^73 announcement found in any search (extended web search, Oct 2026). [negative result]
- V. Angeltveit, "An improved algorithm for checking the Collatz conjecture for all n < 2^N", arXiv:2602.10466
  (11 Feb 2026, math.NT, 14 pp., "Comments very welcome"): recursive bit-by-bit search with precomputed bitvectors;
  "takes less than twice as long to verify convergence for all n < 2^{N+1} as ... for all n < 2^N"; cites Barina 2^71
  as state of the art; per search snippets it says 2^77 should be reachable with resources similar to Barina's and
  names 2^75 as a more modest goal — no verification run is reported. [PRIMARY for abstract/intro; SECONDARY for the
  2^75/2^77 sentences, which the local text extraction did not surface cleanly] — [arXiv:2602.10466](https://arxiv.org/abs/2602.10466)
- Wikipedia (Oct 2026): "checked by computer for all starting values up to 2^71 ≈ 2.36×10^21" citing Barina 2025;
  "As of 2025, the best known bound on cycle length is 217976794617 (355504839929 without shortcut)". [SECONDARY] —
  [Wikipedia](https://en.wikipedia.org/wiki/Collatz_conjecture)

### Inferences
- The project page's 2075·2^60 is ~1.3% beyond 2^71 — no new power-of-two milestone is imminent at the current rate
  (27 work-unit-months per 2^60 step historically per Hercher Remark 30 / Table 10).

### Gaps
- Springer's article page itself redirected to an auth wall; the "published online" date was not captured (only
  "Accepted: 21 April 2025" from the VoR PDF). The PDF metadata shows creation 1–2 May 2025.

## 5. Updates since January 2025 using the 2^71 range (m-cycle bound or cycle length)

### Takeaway
No refereed or arXiv paper since January 2025 updates the m-cycle bound or the cycle-length bound using 2^71. The
only "updates" are (a) Barina's own remark that 2^71 triggers Hercher's Corollary 29 (cycle length 355 504 839 929
in C-steps), (b) Hercher's June 2026 corrigendum, and (c) unrefereed GitHub Lean 4 projects (Sept 2026) claiming a
formalisation of m ≥ 92 and a conditional m ≥ 102 using 2^71 + Rhin's bound.

### Cited Findings
- arXiv search (extended) for 2025–2026 Collatz cycle papers found only generalised-map or heuristic preprints:
  Bouhamidi, "Weakly and strongly admissible triplets for a Collatz-type map", arXiv:2601.17573 (24 Jan 2026,
  math.GM, 31 pp.) — in §5.3 applies its Theorem 4.2/4.5 to the classical case with M0 = 2^71, obtaining
  L ≥ μ0·√M0 ≈ 46 859 289 878 and L ≥ p_23 = 217 976 794 617, i.e. nothing beyond Hercher/Barina; it also notes
  Barina's 2^71 verification. [PRIMARY, local bouhamidi2026.txt] — [arXiv:2601.17573](https://arxiv.org/abs/2601.17573)
- "A note on two Collatz evolution flows", arXiv:2511.17650 (Nov 2025) cites Eliahou and 2^71 but proves no new
  cycle bound. [SECONDARY, search snippet] — [arXiv:2511.17650](https://arxiv.org/pdf/2511.17650)
- D. Sha, "On the bounds of stopping and cycle numbers in the Collatz process", arXiv:2112.12962 (v16 Jan 2026),
  claims no nontrivial cycle exists; unrefereed, not assessed. [SECONDARY] — [arXiv:2112.12962](https://arxiv.org/abs/2112.12962v8)
- GitHub justinalick/collatz-m-cycles-101-lean (© 2026, single commit, "Not yet refereed", prepared with Claude
  Code): Lean 4 proof that every nontrivial cycle has ≥ 102 local minima, *assuming* (i) all n ≤ 2^71 reach 1
  (Barina 2025) and (ii) "RhinBound" on |p log 2 − K log 3|; no sorry/native_decide; "A paper with the human-readable
  proof is in preparation". [SECONDARY/UNVERIFIED claim] — [repo](https://github.com/justinalick/collatz-m-cycles-101-lean)
- GitHub PhilNorfleet/Hercher2023_lean issue #1 (27 Sept 2026) and azadveersingh/collatz-research: report a Lean 4
  formalisation of Hercher's m ≤ 91 (theorem `Collatz.Hercher.hercher_m_ge_92`) with X0 = 695·2^60 and SdW
  Theorem 3 as explicit hypotheses; says the corrigendum credits Xinjun Wang with finding the error. [SECONDARY;
  the azadveersingh repo URL returned 404 when fetched] — [issue](https://github.com/PhilNorfleet/Hercher2023_lean/issues/1)
- MathOverflow could not be fetched (tool restriction); web searches restricted to mathoverflow.net returned no
  relevant threads. OEIS: 17087915 appears only in A005663 (convergent numerators); no OEIS entry tracks cycle-length
  bounds. [PRIMARY for OEIS search] — [OEIS search](https://oeis.org/search?q=17087915&fmt=short)

### Inferences
- The formal record as of Oct 2026: m ≥ 92 (Hercher 2023 + corrigendum 2026, X0 = 695·2^60), K ≥ 137 528 045 312
  (Hercher Cor. 29 + Barina 2^71). The "m ≥ 102" claim is a GitHub-only conditional result and should be cited, if
  at all, as unrefereed.

### Gaps
- Could not inspect the Lean sources or confirm the m ≥ 102 derivation; no preprint exists.
- No MathOverflow content could be examined directly.

## 6. New theoretical tools for cycle bounds (linear forms in two logarithms, 2020–2026)

### Takeaway
The transcendence input in this strand is still Rhin's 1987 specific bound for x log 2 + y log 3 (used by SdW as
Λ > e^{−13.3(0.46057 + log K)}), with Laurent–Mignotte–Nesterenko (1995) and Matveev (2000) as the general tools;
Gouillon (2006) and Laurent (2008) sharpen the two-log constants, but no 2020–2026 paper was found that improves the
2^n − 3^k / log 2, log 3 case specifically or that has been applied to Collatz cycles.

### Cited Findings
- SdW 2010 §5: LMN best for small x, y; Matveev for large; "For our specific case x log 2 + y log 3 however, the
  result of Rhin [Rh] is best"; Lemma 12 constant 13.3 from the Proposition on p. 160 of Rhin, Progress in Math. 71
  (1987) 155–164. [PRIMARY] — [SdW 2010 PDF](https://deweger.net/papers/[35a]SidW-3n+1-v1.44[2010].pdf)
- M. Laurent, M. Mignotte, Yu. Nesterenko, "Formes linéaires en deux logarithmes et déterminants d'interpolation",
  J. Number Theory 55 (1995) 285–321 — used by Simons (2005) for 2-cycles. [SECONDARY] —
  [AMS Math. Comp. abstract](https://www.ams.org/mcom/2005-74-251/S0025-5718-04-01728-4/)
- N. Gouillon, "Explicit lower bounds for linear forms in two logarithms", J. Théor. Nombres Bordeaux 18 (2006)
  125–146: constant ≈ 5·10^4 instead of ≈ 10^8 (Schneider method with multiplicity). [SECONDARY, search snippet of
  abstract] — [JTNB](https://jtnb.centre-mersenne.org/articles/10.5802/jtnb.537)
- Irrationality-measure side: Rhin's bound for the linear span of log 2 and log 3 gives μ < 8.616 (Zudilin's essay);
  Salikhov 2007 / Wu–Wang 2014 give μ(log 3) < 5.126 / 5.117 — these concern log 3 alone or (log 2, log 3)
  jointly, not directly the Collatz constant. [SECONDARY] — [Zudilin, arXiv:math/0404523](https://arxiv.org/pdf/math/0404523)
- Mignotte et al., "A kit for linear forms in three logarithms" (revised Sept 2023) and Yamada's 2025 Acta Arith.
  note on Laurent's two-log bound exist but are not applied to 2^n − 3^k. [SECONDARY, search snippets] —
  [Yamada, Acta Arith. 221](https://www.impan.pl/en/publishing-house/journals-and-series/acta-arithmetica/all/221/2/116174/a-note-on-laurent-s-paper-on-linear-forms-in-two-logarithms-the-argument-of-an-algebraic-power)
- Hercher 2023 contains no transcendence step of its own; its K-upper bound is imported from SdW (K < 1.4784 m δ^m),
  so any improved two-log constant would only enter through SdW's Lemma 12. [PRIMARY, Hercher proof of Thm 23]

### Inferences
- The binding constraint for pushing m-bounds is the K-upper bound K < c·m·δ^m (from Rhin via SdW Lemma 14) versus
  the K-lower bounds from continued fractions; improved two-log constants would raise the excluded m only
  logarithmically. The frontier for cycle *length* is set by X0 (Barina), not by transcendence.

### Gaps
- Rhin's 1987 proposition itself was not read (no accessible copy); the 13.3 exponent is quoted from SdW.
- No Baker-type improvement specific to |2^n − 3^k| from 2020–2026 was found; absence of evidence, not proof of absence.

## 7. Lagarias's annotated bibliography: arXiv ids and relevant entries

### Takeaway
Part I (1963–1999) is arXiv:math/0309224 (v13, Jan 2011); Part II (2000–2009) is arXiv:math/0608208 (v6, Feb 2012).
Relevant entries: Eliahou (1993) #53, Halbeisen–Hungerbühler (1997) #80, Steiner (1978) #158, Oliveira e Silva (1999)
#136, Leavens–Vermeulen (1992) #113 in Part I; Simons (2005, 2007, 2008) #94–98, Simons–de Weger (2005) #101,
Sinisalo (2003+) #105, Oliveira e Silva (2004+) #81, Roosendaal (2004+) #88 in Part II.

### Cited Findings
- J. C. Lagarias, "The 3x+1 problem: An annotated bibliography (1963–1999)", arXiv:math/0309224 (v1 Sept 2003,
  latest v13 Jan 2011). [PRIMARY] — [arXiv:math/0309224](https://arxiv.org/abs/math/0309224)
- J. C. Lagarias, "The 3x+1 problem: An annotated bibliography, II (2000–2009)", arXiv:math/0608208 (latest v6 Feb
  2012); states the conjecture verified to 17×2^58 > 4.899×10^18 (Oliveira e Silva, as of 21 Feb 2008) and
  612×2^50 > 6.89×10^17 (Roosendaal). [PRIMARY, local lagarias2.txt] — [arXiv:math/0608208](https://arxiv.org/abs/math/0608208)
- Part I #80 (Halbeisen–Hungerbühler, Acta Arith. 78 (1997) 227–239, MR 98g:11025): "optimal upper bounds for the
  size of a minimal element in a rational cycle of length k ... if the 3x+1 Conjecture is verified for
  1 ≤ n ≤ 212,366,032,807,211 (≈ 2.1×10^14) then the lower bound on cycle length jumps to 102,225,496". H–H's own
  note added in proof: Oliveira e Silva verified up to 3·2^50, "Thus the length of non-trivial Collatz cycles is in
  fact at least 102 225 496". [PRIMARY for both] — [H–H PDF](https://math.ch/norbert.hungerbuehler/publications/Optimal_bounds_for_the_length_of_rational_Collatz_cycles.pdf)
- Part I #53 Eliahou — see §1. Part II #101 Simons–de Weger, #105 Sinisalo — see §2 and §1.
- Part II #98: Simons (2008a+), "Post-transcendence conditions for the existence of m-cycles", extends SdW to all
  m ≤ 73 [SECONDARY]; #97 Simons, "Exotic Collatz cycles", Acta Arith. 134 (2008) 201–209; #96 Simons, "On the
  (non)-existence of m-cycles for generalized Syracuse sequences", Acta Arith. 131 (2008). [PRIMARY for listing]
- The printed version of the bibliography is in J. C. Lagarias (ed.), The Ultimate Challenge: The 3x+1 Problem, AMS
  2010; the overview chapter (pp. 3–29) lists records W1 (20×2^58) and W2 (period ≥ 10 439 860 591; ≥ 6 586 818 670
  odd members). [PRIMARY, local copy]

### Inferences
- Lagarias's bibliography stops at 2009; Hercher (2018/2023), Barina (2021/2025) and the yoyo@home 87·2^60 result
  are not in it and must be cited from the sources in §3–4.

### Gaps
- None material; the two arXiv PDFs were extracted and grepped locally.

## Summary table (for the citing researcher)

| Result | Source | X0 assumed | Bound | Provenance |
|---|---|---|---|---|
| T-period = 301994a+17087915b+85137581c, ≥ 17 087 915 | Eliahou, Discrete Math. 118 (1993) 45–56 | 2^40 | p_15 | secondhand (Lagarias #53, H–H Thm 2) |
| T-period ≥ 102 225 496 | Halbeisen–Hungerbühler, Acta Arith. 78 (1997) 227–239 | 2.12×10^14 (met by OeS 3·2^50) | p_16+p_15 | primary |
| T-period ≥ 630 138 897 | Sinisalo preprint (2003+) | 2.70×10^16 | p_19 | secondhand (Lagarias #105) |
| no m-cycles, m ≤ 68 | Simons–de Weger, Acta Arith. 117 (2005) 51–70 | ≈3.39×10^17 (Roosendaal, Nov 2004) | – | primary |
| no m-cycles, m ≤ 74 / m ≤ 75 | SdW web v1.41 / v1.44 (2010) | 5·2^60 (OeS) | – | secondhand / primary |
| T-period ≥ 10 439 860 591, K ≥ 6 586 818 670 | Lagarias overview (AMS 2010), Eliahou Thm 3.2 | 20·2^58 | p_21, q_21 | primary |
| C-period > 17 026 679 261 (= p_21+q_21) | Hercher, Die Wurzel 2018 | 87·2^60 (Hercher's own run; also yoyo@home 2017) | – | primary (preprint) |
| K > 7.2·10^10 (= q_21+q_22) | Hercher–Puchert, Die Wurzel 2018 | 87·2^60 | semiconvergent | secondhand (Hercher 2023) |
| no m-cycles, m ≤ 91 | Hercher, JIS 26 (2023) 23.3.5 + corrigendum 14 Jun 2026 | 695·2^60 (JIS) / 704·2^60 (arXiv v3) | – | primary |
| K > 1.375·10^11 if X0 ≥ 3·2^69 | Hercher 2023, Cor. 29 | 1536·2^60 | q_23 | primary |
| all n < 2^71 converge (2025-01-15); C-period ≥ 355 504 839 929 | Barina, J. Supercomput. 81:810 (2025) | 2048·2^60 | p_23+q_23 | primary |
| 2075·2^60 ≈ 2^71.02 verified | pcbarina.fit.vutbr.cz (2026-10-08) | – | – | primary (web) |
| m ≥ 102 (conditional on 2^71 + Rhin) | GitHub justinalick (Sept 2026), unrefereed | 2^71 | – | unverified |

Open as of Oct 2026: (i) nobody has re-run Hercher's Theorem 23 iteration with X0 = 2^71 in a refereed venue;
(ii) excluding the pair (p_23, q_23) itself (forcing K ≥ q_24 = 753 110 839 881) has no published sufficient X0;
(iii) no new verification milestone beyond 2^71 is announced; Angeltveit's 2026 algorithm is untested at scale.
