# The density-one gap after M2: how far existing methods are from "P(1) has density 1"

Date: 2026-10-10. Written overnight for the K–L/Collatz project. It is a research note, not a proof.
Inputs: `notes/m2_audit.md` (§2, §7, §8), `reports/Collatz adjacent work and references.md`, and primary sources
downloaded to a temporary scratch directory (Tao arXiv v7 PDF, sha256 `62cf49d4…394e`; Mazur's natural-density paper v2,
sha256 `08a46dd1…73cf`; Korec 1994; Inselmann arXiv v3; Gonçalves–Greenfeld–Madrid arXiv v2; Chang arXiv v6; Mazur's
base paper and M2 paper from `~/devel/mazur_dl/m2/dl/`).

**Provenance tags.** **[P]** read in the primary source (page, equation or theorem number given). **[S]** seen only in an
abstract, a listing, a citing paper or a search snippet. **[U]** could not be checked. **[I]** this project's own
measurement or audit. **[A]** our own argument in this note. It is not taken from any source and should be checked
like any new argument.

Notation. C is the ordinary map (n/2, 3n+1). Col_min(N) = min over the orbit of N. G = P(1) = {N ≥ 1 : N reaches 1}.
E = N_{>0} \ G is the non-convergent set. For A ⊆ N_{>0}, A(X) = #(A ∩ [1, X)).
d_(A) and d̄(A) are the lower and upper natural densities. δ_(A) and δ̄(A) are the lower and upper logarithmic densities
(the liminf and limsup of (log x)^{-1} Σ_{n≤x, n∈A} 1/n).

---

## 0. Bottom line

1. **The gap as one statement [A].** Let B be any integer with 1 ≤ B ≤ 2^71. By Barina's verification, B = 1 needs no
   computation and every larger B gives the same set: {N : Col_min(N) ≤ B} = P(1). The open statement is then

   > **(G)** limsup_{X→∞} X^{-1} · #{1 ≤ N < X : Col_min(N) ≤ B} = 1.

   (G) is Tao's Theorem 1.3 with the **bounded** function f ≡ B + 1 in place of f → ∞ (Tao's inequality is strict).
   It is needed only in **upper natural** density. Tao's own form, logarithmic density 1, also suffices, because it
   implies (G). By Mazur's M2 Corollary 1.2
   (formally verified, `notes/m2_audit.md`), (G) is **equivalent** to the Collatz conjecture. So are all its
   variants: lower, upper, natural or logarithmic density 1 of P(1), and lower density 0 of E (§1.3).
2. **What is proved.**
   - For every f → ∞: logarithmic density 1 (Tao, refereed).
   - For every f → ∞: natural density 1 with a uniform clock of 436·log N raw steps (Mazur, Lean-checked by its
     author, unrefereed; Allikvere, unrefereed).
   - For a fixed threshold N0: the exceptional set {Col_min > N0} has upper density ≤ C·(log N0)^{-d}, with C
     ineffective. For Tao this is upper logarithmic density, with exponent c unspecified. Mazur's natural-density
     version gives upper natural density (for odd N) with any d < 5/143.
   - Hence δ̄(E) ≤ C·(71 log 2)^{-c}. This number is not known to be below 1.
3. **The distance is qualitative, not a matter of rates [A].**
   - At any fixed threshold, every known bound on the exceptional density is strictly positive.
   - Under M2, "exceptional density exactly 0 at a fixed threshold" is the same as "no counterexample". No improvement
     in c, d or C closes this.
   - Combining an effective M2 with explicit exceptional bounds would need bounds below the basin density of a
     hypothetical counterexample at height m. That basin density is heuristically of order Σ 1/y over the orbit, so the
     method would have to resolve individual integers. Polylogarithmic rates are many orders of magnitude away.
4. **Three independent signs that (G) needs new input of a different kind.**
   - (i) **Tao's own heuristic is now a theorem.** Tao's Remark 1.4 argues that a constant bound is "almost as hard" as
     Collatz, because an exceptional orbit should attract a positive density. M2 proves exactly that attraction, so
     "almost as hard" becomes "equivalent".
   - (ii) **The probabilistic machinery is map-generic.** Tao's almost-boundedness theorem also holds for 3x+5 and
     3x−1 (Gonçalves–Greenfeld–Madrid, Theorem 1.3, whose hypotheses these maps satisfy). For 3x+5 the multiples of 5
     form an invariant set of density 1/5 that never reaches 1, and our counts to 10^6 split the rest among five
     cycles. For 3x−1 the counts split ≈ 33/32/35 %
     among three cycles. So the step from f → ∞ to f bounded must use arithmetic specific to 3x+1.
   - (iii) **It needs transcendence-strength input.** (G) implies the weak Collatz conjecture (no nontrivial cycles).
     By Tao (2011), that implies 2^a − 3^k ≫ (1+ε)^k. So any proof of (G) "must either use transcendence theory, or
     introduce new techniques" giving exponential separation of powers of 2 and 3.
5. **Corrections to existing project text** (details in §5.3):
   - Mazur's "436·log N" result is the natural-density version of Tao's theorem, for an arbitrary threshold f → ∞. It
     implies Tao's Theorem 1.3. It is not "descent below the start" and not "a different statement, not strictly
     stronger".
   - Korec's exponent is θ > log 3/log 4 ≈ 0.7925, not log 4/log 3.
   - Tao's printed formula for Allouche's exponent contains a typo.

---

## 1. The reduction and the density logic

### 1.1 Density notions (standard; proof included for completeness)

**Lemma 1.** For every A ⊆ N_{>0}: d_(A) ≤ δ_(A) ≤ δ̄(A) ≤ d̄(A).

*Proof.* Partial summation gives Σ_{n≤x, n∈A} 1/n = A(x)/x + ∫_1^x A(t) t^{-2} dt, where A(t) counts up to t.

If A(t) ≥ (α − ε)t for all t ≥ t0, then the integral is at least (α − ε)(log x − log t0). Dividing by log x gives
δ_(A) ≥ α − ε. The upper inequality is symmetric. ∎

This is the standard chain (e.g. Tenenbaum, *Introduction to Analytic and Probabilistic Number Theory*, Ch. III.1)
**[S]**. Gonçalves–Greenfeld–Madrid §1.3 note that natural density 1 implies log density 1 and the converse fails
**[P, arXiv:2111.06170v2 p. 6]**. Inselmann notes that a set can have log density 1 and lower natural density 0
**[P, arXiv:2402.03276v3 p. 4]**.

### 1.2 What M2 provides (verified)

- **M2 Theorem 1.1.** For every a ≥ 1 with 3 ∤ a there are c_a > 0 and X_a with #P(a) ∩ [1, X) ≥ c_a·X for all
  X ≥ X_a. The constants are ineffective for general a. **[P, paper v1.0 p. 1; I, Lean statement re-derived in
  `AuditMain.lean`, three standard axioms]**
- **M2 Corollary 1.2.** Either E = ∅ or d_(E) > 0. The formal version is `nonconvergence_positive_lower_density_
  of_counterexample`, which gives c > 0 and X0 with E(X) ≥ cX for all X ≥ X0. **[P, §5; I]**
- The mechanism is bidirectional invariance (§5 of M2). Pick n ∈ E and a point a of its orbit with 3 ∤ a. Then
  P(a) ⊆ E.
- **Barina** (J. Supercomput. 81:810, 2025) verified that every n < 2^71 reaches 1 **[P via existing report]**. Hence
  E ∩ [1, 2^71] = ∅, so E = {N : Col_min(N) > 2^71}.

### 1.3 Equivalences [A, short proofs from M2 + Lemma 1]

Assume M2 and Barina's verification. Then the following are equivalent:

| | Statement |
|---|---|
| (C) | Collatz: E = ∅ |
| (a) | d̄(P(1)) = 1 (M2's own formal hypothesis: ∀ε ∀N ∃X ≥ N, P(1)(X) ≥ (1−ε)X) |
| (b) | δ̄(P(1)) = 1 |
| (c) | δ(P(1)) = 1 (log density exists and equals 1), i.e. Tao's Theorem 1.3 with the constant f ≡ 2 (Tao's inequality Col_min(N) < f(N) is strict) |
| (d) | d(P(1)) = 1 |
| (e) | d̄({Col_min ≤ B}) = 1 for some, equivalently every, B ∈ [1, 2^71] |
| (f) | d_(E) = 0; or δ_(E) = 0 |

Proofs:
- (C) ⇒ (d) is trivial, since P(1) = N_{>0}.
- (d) ⇒ (c) ⇒ (b) ⇒ (a) follow from Lemma 1 (d̄ ≥ δ̄ ≥ δ_ ≥ d_).
- (a) ⇔ (f): E is the complement of P(1).
- (a) ⇒ (C): if E ≠ ∅, M2 gives d_(E) ≥ c > 0, so d̄(P(1)) ≤ 1 − c.
- (e) ⇔ (a): for B ≤ 2^71, {Col_min ≤ B} = P(1) (§1.2).

For B > 2^71, (e) is still equivalent to Collatz once one adds the finite check that every n ≤ B reaches 1.

Two "split" versions follow from the same argument [A]:

- **No divergent orbits ⇔ the set of N with a bounded orbit has upper density 1.** A divergent orbit through some a with
  3 ∤ a has a basin P(a) of positive lower density, and every element of that basin diverges.
- **No nontrivial cycles ⇔ the union of the basins of nontrivial cycles has lower density 0.** Each nonempty basin has
  positive lower density by M2.

So both classical failure modes now have equivalent density formulations. The density formulations do not make either
one easier.

### 1.4 Answer to Q1(c): is the logic right?

Yes. Suppose E had log density 0, or merely lower log density 0. By Lemma 1, d_(E) ≤ δ_(E) = 0. M2 Cor 1.2 then forces
E = ∅.

Tao's theorem does **not** say that E has log density 0. It says that {N : Col_min(N) ≥ f(N)} has log density 0 for each
f → ∞. Elements of E are not in that set in general. If N lies in the basin of a hypothetical cycle with minimum m,
then Col_min(N) = m < f(N) as soon as f(N) > m. So Tao's theorem is consistent with E having positive density.

What Tao does give about E is quantitative and harmless. Theorem 3.1 with N0 = 2^71 holds for all x, so
δ̄(E) ≤ C·(71·log 2)^{-c}, where C and c are unspecified absolute constants **[P, Thm 3.1 p. 16; A for the
specialisation]**. M2 gives d_(E) ≥ c_E if E ≠ ∅, with c_E unknown. These two bounds do not contradict each other.

---

## 2. Tao, "Almost all orbits of the Collatz map attain almost bounded values"

arXiv:1909.03562 (v1 8 Sep 2019 … v5 15 Feb 2022, v6 6 Jul 2026, v7 16 Jul 2026). The v7 comment reads "Two more minor
typos corrected, and one medium typo (affecting the statement of Lemma 7.9) corrected". Published in Forum Math. Pi 10
(2022) e12, 56 pp., doi:10.1017/fmp.2022.8 **[P, arXiv abstract page]**. Page numbers below refer to arXiv v7.

### 2.1 Exact statements

- **Definition 1.2 (p. 2).** Log(R) is the random variable on a finite set R with P(Log(R) ∈ A) =
  Σ_{N∈A∩R} 1/N / Σ_{N∈R} 1/N. The logarithmic density of A is lim_{x→∞} P(Log(N+1 ∩ [1,x]) ∈ A). "Almost all" means
  logarithmic density 1. **[P]**
- **Theorem 1.3 (p. 3).** "Let f : N+1 → R be any function with lim_{N→∞} f(N) = +∞. Then one has Col_min(N) < f(N) for
  almost all N ∈ N+1 (in the sense of logarithmic density)." **[P]** Theorem 1.6 (p. 4) is the Syracuse form.
- **Remark 1.4 (p. 3).** Theorem 1.3 "is easily seen to be equivalent to" the statement that for every δ > 0 there is
  C_δ with Col_min(N) ≤ C_δ on a set of lower log density ≥ 1 − δ. The argument gives C_δ ≪ exp(δ^{−O(1)}).
  **[P]**
- **Theorem 3.1 (p. 16).** For N0 ≥ 2 and x ≥ 2,
  (1/log x) Σ_{N ∈ 2N+1 ∩ [1,x], Syr_min(N) > N0} 1/N ≪ 1/log^c N0.
  Equivalently, P(Col_min(Log(N+1 ∩ [1,x])) ≤ N0) ≥ 1 − O(log^{-c} N0) for all x ≥ 2. Here c > 0 is an absolute
  constant that is not specified. **[P]**

### 2.2 Where f → ∞ is needed

- **Theorem 3.1 ⇒ Theorem 1.3 (p. 18).** Tao sets f̃(x) := inf_{N ≥ x} f(N) and applies Theorem 3.1 with N0 := f̃(x).
  The error O(log^{-c} f̃(x)) tends to 0 only because f̃(x) → ∞. This is the only place where the growth of f is used.
  **[P]**
- **Inside Theorem 3.1 (pp. 17–18).** The proof telescopes the stabilisation estimate (1.20) over the scales
  y^{α^j}, α = 1.001, from y ≈ N0^{1/α} up to x. The error is Σ_j O((α^j log y)^{-c}) = O(log^{-c} N0). The bottom scale
  dominates, and nothing at that scale is small when N0 is bounded. **[P]**
- **Proposition 1.11 (pp. 8–9).** It gives P(T_x(N_y) = ∞) ≪ x^{-c} (1.19) and
  d_TV(Pass_x(N_{x^α}), Pass_x(N_{x^{α²}})) ≪ log^{-c} x (1.20). The log^{-c} x losses come from three sources:
  - the Chernoff tail and the window boundary of the first-passage time, (5.12) and (5.16), pp. 23–24;
  - the multiplicative uncertainty exp(O(log^{0.6} x)) in (5.14);
  - the polynomial decay n^{-A} in Propositions 1.14 and 1.17.
  **[P]**
- **Tao on improving these losses (p. 9, p. 13).** Any bound O((log log x)^{-1-c}) in (1.20) would suffice, and the
  bound "may" improve "perhaps all the way to x^{-c}". Propositions 1.14 and 1.17 might improve to exp(−cn). **[P]**
  Even an error of x^{-c} would leave O(N0^{-c}) > 0 at a fixed threshold [A].
- **Why logarithmic density (p. 7).** "the multiplicative inaccuracy of exp(O(n^{1/2})) in (1.17) is the main reason why
  we work with logarithmic density instead of natural density". **Remark 1.16 (p. 12):** to upgrade to natural density
  "it seems necessary to strengthen Proposition 1.14 by establishing a suitable fine scale mixing property of the
  entire random affine map Aff_{Geom(2)^n}". **[P]** That gap has since been claimed closed twice (§5).

### 2.3 What Tao says about obstacles to a fixed bound

- **Remark 1.4 (p. 3), verbatim core:** a constant C0 "is likely to be almost as hard to settle as the full Collatz
  conjecture, and out of reach of the methods of this paper". The reason given: if an orbit never drops below C0,
  "probabilistic heuristics … suggest that for a positive density set of N … the orbit … should encounter one of the
  elements … of the orbit of N0 before going below C0". **[P]** M2 proves this heuristic for every orbit avoiding
  [1, 2^71] [A].
- **Remark 1.4, continued (footnote 3 credits Ben Green).** "it is possible in principle that a sufficiently explicit
  version of the arguments here, when combined with numerical verification of the Collatz conjecture, can be used to
  show that the Collatz conjecture holds for a set of N of positive logarithmic density" **[P, p. 3]**. Tao's 2020
  blog post makes the same point for the positive-density case of #P(1) ∩ [1,x] ≫ x **[P, blog 25 Jan 2020]**. Mazur's base paper carries this out in natural density (§4).
- **2019 blog post (10 Sep 2019).**
  - Collatz "remains out of reach of current techniques (… it is basically at least as difficult as Baker's
    theorem …)".
  - Known results are "local-in-time" (times ≤ c log N). Reaching f(N) needs "something more like an '(almost)
    global-in-time' result".
  **[P]**
- **2011 blog post (25 Aug 2011), Propositions 6–7.** The weak Collatz conjecture (no nontrivial cycles) implies
  2^a − 3^k ≫ k, and in fact ≫ (1+ε)^k. "Thus we see that any proposed proof of the Collatz conjecture must either use
  transcendence theory, or introduce new techniques that are powerful enough to create exponential separation between
  powers of 2 and powers of 3." **[P]** Because (G) ⇒ Collatz ⇒ weak Collatz, this applies to every proof of (G) [A].
- **Blog comment, 29 Apr 2025.** It is not yet ruled out that almost all orbits diverge. Explicit thresholds plus
  numerical verification would give a positive density of non-divergent orbits, "But even then this would fall short of
  the claim that a density 1 set of orbits do not diverge. In fact, heuristically, if there was a single orbit that
  diverged, then there should be a positive probability that a general orbit would encounter this orbit and then also
  diverge, so the density 1 problem may be nearly as hard as the full Collatz conjecture!" **[P, comment-page-4]**
- **Blog comment, 23 Aug 2026.** "Apparently, there are now some AI-generated solutions to the natural density version
  of my result; if they check out, they should be able to give something along the lines of your statement … However,
  this would need to be done carefully." **[P]** So Tao has not endorsed the natural-density claims.

### 2.4 Errata and a typo worth knowing

- Mazur reported (blog comments, 5 Jul 2026) that a displayed estimate in the printed proof of Corollary 6.3 "seems to
  fail" at the upper end of the range (6.8). He gave an explicit witness and traced the problem to v4's tightening from
  C_A^3 log n to C_A^2 log n. Tao replied the next day: "The simplest fix is to replace the constant 1/2 that starts
  appearing in (6.7) onwards with, say, 0.99, and then the numerical bounds go through". arXiv v6 followed on
  6 Jul 2026. **[P, blog comments]** The theorem is unaffected.
- **Allouche's exponent.** Tao p. 2 prints "θ > 3/2 − log 3/log 2 ≈ 0.869". That expression is negative. The intended
  value is 3/2 − log_3 2 = 0.86907…, as Korec states (Math. Slovaca 44 (1994) p. 86) and as Mazur's natural-density
  paper notes in its footnote 1. **[P]**

---

## 3. Known density results about convergence and descent

"Natural" means asymptotic density d. All entries concern sets of starting values.

| Result | Density notion | Exact claim | Status |
|---|---|---|---|
| Terras, Acta Arith. 30 (1976) 241–252; 35 (1979) 101–102 | natural | For the map T (n/2, (3n+1)/2), let σ(n) be the least k with T^k(n) < n. For each k, {n : σ(n) ≤ k} has a limiting asymptotic density F(k), and F(k) → 1. So almost all n have finite stopping time. | refereed; [P via Korec p. 85 and Lagarias 1985 Thm A, HTML edition], [S] for exact wording |
| Everett, Adv. Math. 25 (1977) 42–45 | natural | {y : ∃n T^n(y) < y} has density 1 (independently of Terras) | refereed; [P via Korec p. 85] |
| Lagarias, Amer. Math. Monthly 92 (1985) 3–23, Thm D | natural | 1 − F(k) ≤ 2^{−ηk}, with η = 1 − H(1/log_2 3) ≈ 0.05 | refereed; [S] (formulas are images in the HTML edition) |
| Heppner, Arch. Math. 31 (1978); Möller, Acta Arith. 34 (1978) | natural | density-one results for Hasse's generalisations | refereed; [S via Mazur ND §1] |
| Allouche, Sém. Théorie Nombres Bordeaux 1978–79, Exp. 9 | natural | Col_min(N) < N^θ for density-1 many N, for every θ > 3/2 − log_3 2 = 0.86907 (pointed out by Korec's referee) | [P via Korec p. 86] |
| Korec, Math. Slovaca 44 (1994) 85–89, Thm 1 | natural ("asymptotic density") | "For every real c > log_4 3 (= 0.79248125…) the set M_c = {y : (∃n)(T^n(y) < y^c)} has asymptotic density 1." The step count n "could be bounded by log_2 y, but it could not be bounded independently of y". | refereed; [P] |
| Tao 2022, Remark 5.1 | logarithmic (as stated) | Syr_min(N) ≤ N^θ for every θ > 1/α. Also P(Syr^n(N_y) = N_y for some n) ≪ x^{-c}: almost no integer lies on a cycle. This concerns elements of cycles, not basins. | refereed; [P p. 21–22] |
| Tao 2022, Thm 1.3 / 3.1 | logarithmic | §2.1. For fixed N0, the exceptional log density is ≪ log^{-c} N0, with c unspecified. | refereed; [P] |
| Inselmann, arXiv:2402.03276v3 (13 Aug 2024), Cor. 1.4 | natural | For every ε > 0, T^{⌊2 log m/log(4/3)⌋}(m) ≤ m^ε for density-1 many m, hence T_min(m) ≤ m^ε. The author: "it seems unlikely that the methods of this paper would suffice to prove the full natural density version of Tao's result". | preprint; [P] |
| Gonçalves–Greenfeld–Madrid, arXiv:2111.06170 (Indiana Univ. Math. J. 74 (2025) 1–46), Thm 1.3 | logarithmic | Tao's theorem for C_{p,q,r} with gcd(p,q) = 1, q < p^{p/(p−1)}, qj + r(j) ≡ 0 (mod p). Natural density for generic f "seems a very hard task and still is out of reach". Thm 1.8 is the natural-density analogue of Korec's result. | refereed [S for venue]; [P for arXiv text] |
| Siegel–O'Dwyer, arXiv:2609.33018 (26 Sep 2026, math.GM) | logarithmic | Tao-type almost-boundedness for "p-Hydra" maps on rings of integers of number fields, by archimedean methods without Fourier decay | preprint; [S, abstract] |
| ProofAtlas, "Power-saving bound for logarithmic-time Collatz descent" | natural, explicit | "For every N ≥ 15,552, the proportion of n < N that do not fall below their starting value within k ≤ log n accelerated Collatz steps is at most 10,000,000·N^{−1/100}" | Lean (ProofAtlas); [S, listing] |
| Mazur, "Natural-Density Almost-Bounded Collatz Orbits in Logarithmic Time", v2 21 Jul 2026, Thm 1.1–1.2 | natural | See §5.1. This is Tao's Theorem 1.3 in natural density with a uniform clock. For fixed N0 the exceptional proportion is ≤ C_d (log N0)^{−d} for every d < 5/143, with C_d existential. | Lean per author (cold build + leanchecker); ProofAtlas "accepted", AI reviews; unrefereed; [P paper] |
| Allikvere, Zenodo 10.5281/zenodo.21340150 (v1 13 Jul, v2 22 Jul 2026) | natural | Tao's theorem in natural density. Exceptional ratio O((log N0)^{−1/29} + x^{−1/2000}). Witness within (3/ln(4/3) + 1/ln 2 + o(1)) ln N < 12 ln N Collatz steps. | preprint, AI-assisted, no formal proof; [S, Zenodo record + Tao blog comment 25 Jul 2026] |

**Lower bounds for P(a) itself (counting, density 0 information).**

| Result | Bound |
|---|---|
| Crandall 1978 | x^{c}, c > 0 |
| Sander 1990 | 0.3 |
| Krasikov 1989 | 3/7 |
| Wirsching 1993 | 0.48 |
| Applegate–Lagarias, Math. Comp. 64 (1995) | π_a(x) ≥ c_a x^{0.65} for x ≥ a (I); x^{0.81} (II) |
| Krasikov–Lagarias, Acta Arith. 109 (2003) | π_a(x) ≥ x^{0.84}, x ≥ x0(a) |
| this project | 0.9203 (k = 21, certificate); 0.909/0.914 Lean |
| Mazur, ProofAtlas, Jul 2026 | π_a(x) ≥ x^{0.90} and c_a x^{0.901} (k = 18; Lean with two `native_decide` axioms) |

All are natural counts, but they are sublinear. They say nothing about positive density **[P/S, see existing report]**.

**Density of P(1) itself.**
- Before September 2026, no positive-density result for P(1) was known.
  - Tao's blog (25 Jan 2020): "This is not yet established". He adds that his paper reduces it to "an (enormous) finite
    computation" **[P]**.
  - A July 2025 ANTS XVII talk (Elsenhans) still lists "Is the density of the integers that satisfy the conjecture
    positive?" as open **[S]**.
- **Mazur's base paper** (6 Sep 2026; §4) gives explicit c and X0 with #{n < X : τ(n) ≤ 10.46 ln n} ≥ cX for X ≥ X0.
  That is positive lower natural density **[P; I: `AuditBase.base`, three standard axioms]**.
- **M2** extends this to P(a) for every a ≢ 0 (mod 3) **[P; I]**.
- **No result gives an explicit lower density of P(1) beyond this tiny c**, apart from Shaik's unread claim (3) in
  §5, which is also only a positive proportion [A, after the searches in §5].
- Combining Tao with Barina gives δ_(P(1)) ≥ 1 − C(71 log 2)^{-c}. Mazur's natural-density Theorem 1.2 (odd N, then
  the 2-adic fibres) gives d_(P(1)) ≥ 1 − C'(71 log 2)^{-d}. C, C' and c are ineffective, so neither bound is known
  to be positive. Even with prefactor 1 and d = 6993/200000, the natural-density bound would only give about 0.127
  [A, §4.5].

---

## 4. Mazur's base paper: "Explicit Positive-Density Collatz Convergence in Logarithmic Time"

Version 2.1, 6 Sep 2026, 13 pp. The local copy is `~/devel/mazur_dl/m2/dl/prev-paper-v2.pdf`, with text in
`prev-paper-v2.txt`. ProofAtlas status: "Lean formalization checked · acceptance review open". Claude is credited for
manuscript review, Codex for the research. **[P]**

### 4.1 What it proves

- **Theorem 1.1.** With c and X0 given in §8, for every integer X ≥ X0, #{1 ≤ n < X : τ(n) ≤ (523/50) log n} ≥ cX. "Neither
  the existence of its natural density nor density one is asserted." **[P p. 1]**
- **The constants (§8, (8.4)–(8.6)).** c = 3/(256·𝓜·2^m) and X0 = 32(2^B·𝓜 + 1). Here 𝓜 = 4^{2b+1+3^q}, b = 2^80,
  q = Q(b, ⌊β(N)/4⌋, N) > 2^80, and m = ⌊(88·𝓜·C·N)^{1/6}⌋ + 1. **[P]** Hence c < 1/𝓜 < 4^{−3^{2^80}}
  [A, from the recipe]. The paper itself: "The density bound is extremely small and the cutoff extremely large; no
  practical numerical range is claimed".
- This project re-derived the formal statement with its own map and count. `AuditBase.base` depends only on propext,
  Classical.choice and Quot.sound **[I, `notes/m2_audit.md` §3]**.

### 4.2 Method (seed mass), in five steps [P, §§2–6]

1. **Reference densities.** ρ_q = (2/3)·3^q·μ_q on Z/3^q, where μ_q is the law of Tao's Syracuse random variable. Fine-
   scale mixing in L¹ is used: ⟨|ρ_q − ρ_m∘π|⟩ ≤ C_A m^{−A} (Tao Prop 1.14). It is formalised with an explicit C at
   A = 6, from an explicit form of Prop 1.17 with exponent 6409. Lemma 8.1 and audit §7. **[P; I]**
2. **Inverse histories from one seed M.**
   - Words of geometrically growing scales b_{j+1} = b_j + ⌊b_j/100⌋ are appended, each cut at a first crossing of a
     barrier.
   - The weights are ω = 3^d 2^{−A}.
   - Z_n(M) is the ω-weighted sum of ρ over the endpoints. It is a near-martingale whose increments are bounded
     uniformly in M (Prop 3.1). The key ingredient is the multiplicity bound (3.9)–(3.10).
3. **Choosing the seed.** The residue class of M is chosen first, so that Z_N ≥ 255/256 (mean argument). Only then is M
   chosen, from R_v = (4^v − 1)/3 (Lemma 4.1, Prop 4.2). This turns Tao's averaged statement into a statement about one
   fixed seed.
4. **Removing the residue weight (Prop 5.3, §8.4).** The ρ-weighted mass is compared with the unweighted count at a
   coarse modulus 3^m. Since ρ_m ≤ (2/3)2^m, the result is U ≥ 3/(8·2^m). The L¹ mixing error is multiplied by the
   source-charge factor 𝓜, so it needs m^6 ≳ 88·𝓜·C.
5. **Counting (Lemma 6.1, Prop 6.3).** Each distinct source x ∈ [X, 32X) carries weight ≤ 𝓜/x. Hence
   #sources ≥ X·U/𝓜, and the density bound is (1/32)·U/𝓜.

### 4.3 Where density is lost [A, from the cited equations]

| Loss | Size | Cause |
|---|---|---|
| L1 seed size | factor 1/𝓜 | one seed; the source charge x·ω(w) ≤ 𝓜. This is intrinsic: heuristically d(P(𝓜)) is itself of order 1/𝓜 up to a 3-adic factor. The method needs 𝓜 ≥ 16^{b0}, so the affine offsets ≤ 2^b are negligible. |
| L2 residue weight | factor 2^{−m}, with m ≈ (88𝓜CN)^{1/6} (base); 3^{−m}, m = 132RC*+1 (M2) | only L¹ and polynomial mixing is available. Converting weighted mass to a count costs the sup-norm of ρ_m at a modulus large enough to make the L¹ error ≤ 1/(𝓜·const). |
| L3 window | 1/32 | sources lie in [X, 32X) but are charged against Y = 32X |
| L4 central and terminal restrictions | ≥ 175/256 kept | concentration bounds (3.6) and (5.3) |

### 4.4 Can the seed-mass method give density approaching 1? [A]

**One seed: no.** The lower bound is at most of order (mass)/𝓜 ≤ O(1/𝓜). The truth for that seed is heuristically of the
same order.

**Many seeds: only with a forward descent input.**
- Lower density is superadditive on disjoint sets.
- The Syracuse basins of the seeds R_k = (4^k − 1)/3 (k ≥ 2) are pairwise disjoint. 1 is a fixed point of
  S(n) = (3n+1)/2^{v_2(3n+1)}, and S(R_k) = 1, so an orbit meets at most one R_k with k ≥ 2.
- So d_(P(1)) ≥ Σ_k (seed lower bound for R_k). In principle, seeds can be added.
- The method is a backward (inverse-tree) construction. It lower-bounds the mass that provably flows into chosen seeds.
  Nothing in it controls where the rest of the mass goes.
- For the bounds to sum to nearly 1, one must know that almost every forward orbit actually reaches the seeds. That is a
  forward descent statement into verified territory: almost all orbits enter [1, X0] with X0 ≤ 2^71, which is (G)
  itself.
- The natural way to supply it is Tao-type first passage. Assign each N to the first point of [1, X0] that its orbit
  visits. These first-entry basins partition {N : orbit enters [1, X0]}, which is P(1) for X0 ≤ 2^71. The descent
  estimate controls the total only up to the exceptional density at threshold X0 (§4.5).
- So the seed method can feed lower bounds into a density-one argument but cannot supply its missing step.

**Sharp seed bounds would be equivalent to Collatz.**
- Suppose one proved, for a family of seeds with model-predicted total mass Σ w(R) = 1, that
  d_(P(R)) ≥ (1 − ε_R)·w(R) with Σ (1 − ε_R) w(R) → 1. That would give d(P(1)) = 1, hence Collatz by M2.
- Conversely, if a counterexample basin had density δ > 0, then the seeds' true densities would sum to ≤ 1 − δ. The
  model prediction would fail on a δ-share of the seed mass.
- Sharp per-seed bounds therefore have to "see" the absence of every counterexample. Constants alone cannot supply
  that.

### 4.5 What would have to improve (and what that would still leave) [A]

1. **Exponential instead of polynomial fine-scale mixing.** Tao Remark 1.15 predicts exp(−cm) **[P]**. With explicit
   constants, L2 would drop from 2^{−(𝓜C)^{1/6}} to polynomial in 𝓜. Better still would be a sup-norm or local-limit
   version of mixing, giving unweighted counts with relative error o(1).
2. **Thresholds that are uniform in the seed, and small seeds.** The method needs 𝓜 ≥ 16^{b0}, b0 ≥ 2^80, while the
   heuristic mass of P(1) sits on small seeds.
3. **A descent input to a verified box with an explicit exceptional bound.** This is the only way to collect mass
   close to 1. With Mazur's ND exponent d0 = 6993/200000 and the most optimistic prefactor C = 1, the bound at
   X0 = 2^71 is (71 ln 2)^{−d0} = 0.873. That gives d_(P(1)) ≥ 0.127. Reaching 1 − ε requires log X0 ≥ ε^{−1/d0}: for
   ε = 0.01 this is log X0 ≳ 10^{57}. Verification can never close the gap. With these rates it cannot even reach
   density 1/2.
4. **Even with 1–3, the result is 1 − ε(X0) with ε(X0) > 0 at every finite verified range.** Density exactly 1 would
   still need (G).

---

## 5. Recent claims, 2024–2026, that touch the reduction

### 5.1 Table

| Claim | What exactly is claimed | Formal verification | Review |
|---|---|---|---|
| **Mazur, "Natural-Density Almost-Bounded Collatz Orbits in Logarithmic Time"**, v2, 21 Jul 2026, ProofAtlas (= "density-one descent within 436·log N steps") | Thm 1.1(ii): C_Coll = 1509503/(5000 log 2) < 436. For **every** f : N → R with f → ∞, the N with some m ≤ C_Coll log N and Col^m(N) < f(N) have **natural density one**. The quantifier order is ∃C ∀f. (i) is the Syracuse analogue with C_Syr < 145. Thm 1.2: for 0 < d < 5/143 there is C_d with (1/x)#{odd N ≤ x : no Syr^m(N) ≤ N0 within C_Syr log N steps} ≤ C_d (log N0)^{−d} for all N0 ≥ 2, x ≥ 2. Cor 1.3: for f = √N the time is > log N/(2 log 2). "This work does not prove the Collatz conjecture … a density-zero exceptional set may remain." Prefactors and threshold are existential. **[P]** | Lean 4.30.0-rc2. The author reports a fresh-clone cold build and `leanchecker --verbose`, axioms propext/Classical.choice/Quot.sound only. Frozen commit f386357d… in the paper; the ProofAtlas page lists main file `Erdos1135/ND/LogTime/Paper.lean` at ca3dd0d6… (possibly a packaging commit; not reconciled). Listing: 599 files, 182,625 lines. **Not audited by this project.** Tao's Props 1.14/1.17 in explicit form are inside the M2 closure that we rebuilt and replayed **[I]**. | ProofAtlas "accepted", 4 AI reviews; no human referee. Tao (23 Aug 2026): "if they check out". |
| **Mazur, "Explicit Positive-Density Collatz Convergence in Logarithmic Time"**, v2.1, 6 Sep 2026 (= "cX integers reaching 1 within 10.46 ln n steps") | §4.1 **[P]** | Lean, standard axioms. **Re-derived and kernel-replayed by this project** (`AuditBase.base`) **[I]**. | "acceptance review open"; unrefereed |
| **Mazur, "Positive Lower Density of Collatz Predecessors" (M2)**, v1.0, 6 Sep 2026 | §1.2 **[P]** | Lean, standard axioms. **Cold rebuild, leanchecker and `--fresh` replay by this project** **[I]** | unrefereed; AI reviews only |
| **Allikvere**, Zenodo, v1 13 Jul, v2 22 Jul 2026 | Natural-density Tao with rate and clock (§3) **[S]** | none claimed | unrefereed; AI-assisted |
| **Shaik** (Zenodo/SSRN, Aug–Oct 2026) | (1) "Polylogarithmic Descent for Almost All Collatz Orbits in Natural Density", v4.0.2, 4 Oct 2026: for f → ∞, density-1 many n reach below (log n)^{A_FP}·f(n), A_FP ≈ 9.9911. This is weaker than Mazur ND. (2) "Quantitative Endpoint Transport…", v2.2.0, 6 Sep 2026: natural-density descent to exp((log n)^{1−δ}), δ < 0.25124. (3) "Positive density of Collatz convergence at every rate above 3/log(4/3)", v1.0.0, 21 Sep 2026: a positive proportion reach 1 within c log x steps for every c > 3/log(4/3) ≈ 10.43. The author states that none "proves the Collatz conjecture or excludes exceptional cycles or divergent orbits". **[S, author's site; papers not read]** | Lean archives mentioned ("Palomar" registry); axioms not stated **[U]** | unrefereed |
| **Chang**, arXiv:2603.11066 (v6, Apr 2026), "Exploring Collatz Dynamics with Human–LLM Collaboration" | A "Paradigm Exhaustion Theorem". Claim (iii): "the set of potential divergent starting points has natural density 0". The set is ∩_L V_L with V_L = {n : S_j < j log_2 3 for all j ≤ L} (pp. 142–143), i.e. orbits that never drop below the start in the linear approximation. That is a Terras-type statement. It is **not** the set of divergent starts (those may first drop and diverge later), so it does not combine with M2. The paper: "measure zero ≠ empty" and "not a proof of the Collatz conjecture". **[P]** | none | arXiv math.DS/cs.AI |
| **Kalafatelis**, Preprints.org 202604.0411 (Apr 2026) | Reduces a "uniform-window shell-kernel" problem to an unresolved primitive-frequency estimate. No unconditional density theorem. **[S via Mazur ND §1]** | – | unrefereed |
| **neljaouh/ConjectureA** (GitHub, Sep 2026) | Conjecture A plus the growth exponent, "rests on" vendored M2 **[P via existing report]** | inherits M2 | – |
| **Tavares**, arXiv:2608.27617 (Aug 2026) | Wirsching's Conjectures 1 and 3, a positive-density programme. Superseded in aim by M2 if both are right. **[S]** | – | math.GM |
| **Liu**, arXiv:2512.13760 | v1 claimed x^{0.946}. v2 retreated to x^{0.3227} **[P abstract]** | – | math.GM |
| Full-proof claims on arXiv math.GM (e.g. Wey 2309.09991; Kawasaki 2502.20642) and the July 2026 Lean "disproof" (`xrchz/CollatzLean`, a proof of False via kernel bug #14576, fixed in Lean 4.32.2) | None engages the density reduction. The disproof was a kernel soundness bug **[S / P via existing report]** | – | – |

No claim found anywhere, through 2026-10-10, asserts density-one convergence **to 1** in any density notion. Every
density-one claim is for thresholds f → ∞ [A, after the searches listed in §7].

### 5.2 How these sit relative to (G) [A]

- The natural-density versions (Mazur ND, Allikvere, Shaik (1)) close the log-vs-natural gap of Tao's Remark 1.16 for
  f → ∞. They do not touch the bounded-f gap.
- Their fixed-threshold bounds have the same shape as Tao's Theorem 3.1. Each gives a positive constant times
  (log N0)^{−d}, with ineffective prefactors.

### 5.3 Corrections to earlier project text

1. **Mazur ND.**
   - CLAUDE.md ("Omvärld 2026") says: "naturlig densitet 1 för nedstigning inom 436·log N steg (annat påstående än Taos
     log-densitetssats, inte strikt starkare)".
   - The existing literature report (§ on exponents, and the "misstatements" table) says: "density-one descent below the
     start within 436·log N raw steps … weaker in threshold … not a strict improvement".
   - Both are incorrect. The threshold is an **arbitrary** f(N) → ∞ (Thm 1.1(ii)), not the start value.
   - Natural density 1 implies logarithmic density 1 (Lemma 1), and the timed set is contained in {Col_min < f(N)}. So
     Thm 1.1(ii) **implies** Tao's Theorem 1.3. If it is correct, it is a strict strengthening (natural density plus a
     uniform clock) **[P, ND paper pp. 1–3; A for the implication]**.
2. The existing report writes Korec's range as "β > log 4/log 3". Korec's Theorem 1 is c > log_4 3 = log 3/log 4 ≈ 0.7925
   **[P]**.
3. Tao's printed Allouche exponent "3/2 − log 3/log 2" should be 3/2 − log_3 2 ≈ 0.86907 (§2.4).

---

## 6. Synthesis

### 6.1 The gap

> **(G)** For B = 1, equivalently for any constant 1 ≤ B ≤ 2^71:
> limsup_{X→∞} X^{-1}·#{1 ≤ N < X : Col_min(N) ≤ B} = 1.

In words: Tao's Theorem 1.3 (or Mazur's Theorem 1.1(ii) without the clock) for a **bounded** threshold, needed only in
upper natural density. Equivalently, in Mazur's quantitative form: Theorem 1.2 at N0 = 2^71 with right-hand side 0
instead of C_d (log N0)^{−d}, and only along a sequence of x. By M2 + Barina, (G) ⇔ Collatz (§1.3).

| | Proved (with source) | Needed for (G) |
|---|---|---|
| threshold | any f(N) → ∞, however slowly (Tao; Mazur ND) | f ≡ B, bounded |
| density notion | log (Tao, refereed); natural (Mazur ND, Allikvere, unrefereed) | upper natural suffices |
| exceptional density at fixed N0 | ≤ C(log N0)^{−d}, C ineffective, d < 5/143 (ND); c unspecified (Tao) | exactly 0 at N0 = 2^71 (or N0 = 1) |
| lower density of the convergent set | ≥ c with c < 4^{−3^{2^80}} (explicit, Mazur base); ≥ 1 − C(71 ln 2)^{−d} (ineffective) | 1 (upper density suffices) |

### 6.2 Candidate routes and their obstructions

| Route | Idea | Known obstruction | Assessment |
|---|---|---|---|
| R1. Fixed-threshold Tao | Upgrade the telescoped first-passage stabilisation so that the error at the bottom scale is 0, not O(log^{−c} N0) | (a) Errors are positive at every finite scale. Better rates (x^{−c}, exp(−cn)) leave O(N0^{−c}) > 0 [P Tao p. 9, 13; A]. (b) By M2 the statement is Collatz (Tao Remark 1.4; blog 2025). (c) The proof is map-generic: GGM's Theorem 1.3 covers 3x+5 and 3x−1, where the analogue of (G) fails (rigorously for 3x+5, numerically for 3x−1; App. A). Any proof of (G) must use 3x+1-specific arithmetic that probabilistic estimates do not see. (d) Tao 2011: (G) ⇒ exponential separation of 2^a and 3^k. | not reachable by improving the existing machinery |
| R2. Inverse-tree / seed mass to density 1 | Sum sharp per-seed lower bounds (Mazur base, M2; Wirsching's programme) | Losses L1–L2. Covering mass 1 needs descent into a verified box, i.e. (G). Sharp per-seed bounds summing to 1 are equivalent to Collatz (§4.4). | gives positive density, not 1 |
| R3. Quantitative pincer | Effective M2 (d_(E) ≥ g(counterexample)) against an explicit upper bound for {Col_min > N0} | A counterexample with orbit minimum m > 2^71 has a heuristic basin density of order Σ_{y in orbit} 1/y, with no positive lower bound uniform over hypothetical counterexamples. The upper bound must be adapted to m and beat that size: sub-1/m resolution of first-passage laws. Current rates are (log m)^{−d} with ineffective C. | far out of reach [A, heuristic] |
| R4. Attack cycles and divergence separately (density versions §1.3) | No nontrivial cycle ⇔ cycle basins have density 0; no divergence ⇔ bounded orbits have density 1 | Cycles: Diophantine plus verification only bounds cycle length (K ≥ 1.375·10^11 odd elements, m ≥ 92 local minima; existing report). Excluding all cycles needs Baker-type input beyond current bounds. Divergence: no known tool. Tao (2025) notes that even "almost all orbits do not diverge" is open. Mazur's base paper now gives positive density of non-divergent orbits (if correct). | density formulation adds no leverage |
| R5. K–L difference inequalities / this project's LP (λ_k → 2) | Exponents π_a(x) ≥ x^{γ} | Gives x^{1−ε} at best (K–L §6). Superseded for π_a by M2. Cannot produce density statements. | irrelevant to (G) |
| R6. Transfer operator on Z_3 / uniform c/a (Wirsching) | Sharp predecessor densities d(P(a)) ≍ ρ(a)/a uniformly | Would at most make R3's lower half effective. Still needs the integer-resolution upper half. | partial at best |
| R7. Logic / rewriting / SAT (Yolcu–Aaronson–Heule) | Termination of an 11-rule system ⇔ Collatz | Equivalent to the full conjecture. No density content. | orthogonal |

**On undecidability [A, sources S].**
- Conway (1972, "Unpredictable iterations") and Kurtz–Simon (TAMC 2007: the generalised Collatz problem is
  Π^0_2-complete) concern the class of generalised Collatz maps.
- They neither apply to the single map 3x+1 nor say anything about density statements per se.
- Two consequences still bear on density routes:
  - Gonçalves–Greenfeld–Madrid draw from Conway that "one must use some special properties of the Collatz map"
    **[P p. 3]**.
  - Since Tao's density machinery extends to the whole GGM class, the special properties must enter exactly at the
    step from f → ∞ to bounded f.
- By M2, (G) has the same logical form (Π^0_2) as the conjecture and is equivalent to it. A density formulation offers
  no easier logical class.

### 6.3 Conservative conclusions

1. After M2, "density one" is not a weaker target. In every density notion, density one of P(1) **is** the Collatz
   conjecture. (G) is the cleanest way to state where current methods stop.
2. The bounded-versus-unbounded threshold step is where all known density methods stop. That step requires excluding
   counterexample basins. Rate improvements cannot replace that exclusion.
3. The log-versus-natural density issue (Tao Remark 1.16) is probably resolved. Two independent unrefereed claims exist,
   one Lean-checked by its author. It is no longer the bottleneck and was never the essential one.
4. Positive density of P(1) and of every P(a) is now formally verified (M2, base paper), with tower-sized or ineffective
   constants. Explicit densities close to 1 would need effective descent bounds into the verified range. At known rates
   (d ≈ 0.035), these cannot exceed about 0.13 even with optimal prefactors at 2^71.
5. Nothing in this note supports a claim that any existing or announced work is close to (G). The three obstructions in
   §0(4) apply to every method surveyed.

---

## 7. Sources (all accessed 2026-10-09/10)

- T. Tao, *Almost all orbits of the Collatz map attain almost bounded values*, Forum Math. Pi 10 (2022) e12,
  [doi:10.1017/fmp.2022.8](https://doi.org/10.1017/fmp.2022.8); [arXiv:1909.03562v7](https://arxiv.org/abs/1909.03562)
  (read in full where cited).
- T. Tao, blog posts: [10 Sep 2019](https://terrytao.wordpress.com/2019/09/10/almost-all-collatz-orbits-attain-almost-bounded-values/)
  (comments of 5–6 Jul, 21 Jul, 25 Jul, 23 Aug, 5–6 Sep 2026 on the last comment page;
  [29 Apr 2025 comment](https://terrytao.wordpress.com/2019/09/10/almost-all-collatz-orbits-attain-almost-bounded-values/comment-page-4/#comment-687865));
  [25 Jan 2020](https://terrytao.wordpress.com/2020/01/25/equidistribution-of-syracuse-random-variables-and-density-of-collatz-preimages/);
  [25 Aug 2011](https://terrytao.wordpress.com/2011/08/25/the-collatz-conjecture-littlewood-offord-theory-and-powers-of-2-and-3/).
- L. Mazur, *Positive Lower Density of Collatz Predecessors*, v1.0, 6 Sep 2026,
  [ProofAtlas](https://www.proofatlas.ai/formalizations/positive-lower-density-collatz-predecessors/); audit
  `notes/m2_audit.md`.
- L. Mazur, *Explicit Positive-Density Collatz Convergence in Logarithmic Time*, v2.1, 6 Sep 2026,
  [ProofAtlas](https://proofatlas.ai/formalizations/positive-density-log-time-collatz/).
- L. Mazur, *Natural-Density Almost-Bounded Collatz Orbits in Logarithmic Time*, v2, 21 Jul 2026,
  [ProofAtlas page](https://proofatlas.ai/formalizations/natural-density-log-time-collatz/),
  [PDF](https://proofatlas.ai/papers/natural-density-log-time-collatz/Mazur_Natural_Density_Collatz_Orbits_in_Logarithmic_Time_v2.pdf).
- ProofAtlas listings: [advances](https://www.proofatlas.ai/advances/), [formalizations](https://www.proofatlas.ai/formalizations/).
- I. Korec, *A density estimate for the 3x+1 problem*, Math. Slovaca 44 (1994) 85–89,
  [DML-CZ](https://dml.cz/dmlcz/133225).
- J. C. Lagarias, *The 3x+1 problem and its generalizations*, Amer. Math. Monthly 92 (1985) 3–23,
  [HTML edition §2](https://www.cecm.sfu.ca/organics/papers/lagarias/paper/html/node4.html).
- M. Inselmann, [arXiv:2402.03276v3](https://arxiv.org/abs/2402.03276).
- F. Gonçalves, R. Greenfeld, J. Madrid, [arXiv:2111.06170v2](https://arxiv.org/abs/2111.06170) (Indiana Univ. Math. J. 74 (2025)).
- M. Siegel, R. O'Dwyer, [arXiv:2609.33018](https://arxiv.org/abs/2609.33018).
- J. Allikvere, [Zenodo 10.5281/zenodo.21340150](https://doi.org/10.5281/zenodo.21340150).
- I. A. Shaik, [author's site](https://shaikidris.github.io/) (papers not read).
- E. Y. Chang, [arXiv:2603.11066v6](https://arxiv.org/abs/2603.11066).
- J.-P. Allouche, *T. Tao and the Syracuse conjecture*, EMS Magazine 123 (2022) 12–16,
  [doi:10.4171/MAG/64](https://euromathsoc.org/magazine/articles/64) (not read; cited for the 0.86907 value via Mazur ND).
- A.-S. Elsenhans, [ANTS XVII slides](https://antsmath.org/ANTSXVII/slides/antsxvii-elsenhans-slides.pdf) [S].
- D. Barina, J. Supercomput. 81:810 (2025); Hercher, JIS 26 (2023); Krasikov–Lagarias 2003; Applegate–Lagarias 1995;
  Conway 1972; Kurtz–Simon 2007: see `reports/Collatz adjacent work and references.md`.
- arXiv search for "Collatz" (API, sorted by date, 60 most recent, run 2026-10-10). Web searches for
  density-one / "reach 1" claims (2024–2026) found no density-one-to-1 claim.

---

## Appendix A. Generalised maps where Tao's theorem holds but (G) fails [I, A]

Gonçalves–Greenfeld–Madrid's Theorem 1.3 hypotheses are, for C(N) = N/2 (N even), 3N + r (N odd): gcd(2,3) = 1,
3 < 2^{2/1} = 4, and 3 + r ≡ 0 (mod 2). They hold for every odd r with 3 + r ≥ 1, in particular for r = 5 and r = −1.
So Tao's almost-boundedness theorem holds for 3x+5 and 3x−1 **[P for the theorem, arXiv:2111.06170v2 p. 3; A for
checking the hypotheses]**.

- **3x+5.** Multiples of 5 are invariant: 5k ↦ 5k/2 or 5(3k+1). So P(1) ∩ 5N = ∅ and d̄(P(1)) ≤ 4/5. This is rigorous.
  Among non-multiples of 5, our count of n ≤ 10^6 assigns the following basin shares by cycle minimum:

  | cycle minimum | 1 | 19 | 23 | 187 | 347 |
  |---|---|---|---|---|---|
  | share (n ≤ 10^6) | 0.1762 | 0.6205 | 0.1162 | 0.0407 | 0.0464 |

  At 10^4 the shares were 0.1795/0.6021/0.1191/0.0464/0.0529, and at 10^5 they were 0.1771/0.6197/0.1161/0.0402/0.0470.
- **3x−1** (equivalently 3x+1 on negative integers). The cycles have minima 1, 5 and 17, with shares 0.3277/0.3234/0.3490
  at 10^6 (0.3244/0.3213/0.3543 at 10^4).

These are numerical observations, not theorems (except the 3x+5 invariant-set bound). They show what the probabilistic
"almost bounded" conclusion does and does not control. In the same class, the mass that reaches bounded values can be
split among several cycles. So the passage from "almost bounded" to "density one into one cycle" depends on the
arithmetic of the specific map. For 3x+1 that arithmetic is the nonexistence of other cycles and of divergent orbits.

Scripts: `cyc3x5.py` (sha256 `44b4640a…abdff2`, run as `python3 -I cyc3x5.py 5 1000000`) and `cyc3xm1.py`
(sha256 `80dc0ce6…4d27d4`). They are in the session scratchpad `…/scratchpad/density_lit/scripts/`, which is temporary.
Each finishes in under a minute.
