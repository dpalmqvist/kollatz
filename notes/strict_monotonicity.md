# The Krasikov–Lagarias constants λ_k are attained, tight and strictly increasing

Daniel Palmqvist, with Claude; October 2026.

## Summary

For the linear program L^NT_k(λ) of Krasikov–Lagarias [KL, (2.7)–(2.14)] let λ_k be the supremum of the λ ∈ [1, 2]
for which it is feasible. We prove, for every k ≥ 2:

1. **Attainment.** L^NT_k(λ_k) is feasible, and 1 < λ_k < 2.
2. **Tightness and uniqueness.** Every feasible point at λ = λ_k satisfies all principal inequalities (L1)–(L3) with
   equality, and it is unique up to a positive factor.
3. **Strict increase.** λ_k < λ_{k+1}.
4. **Optimality.** φ^m(y) = c^m λ_k^y is a positive nondecreasing solution of Krasikov's system I_k with equality.
   Hence no exponential lower bound φ ≥ C λ^y with λ > λ_k follows from I_k (with positivity and monotonicity).
   In particular, every linear program obtained from I_k by splitting and truncation in the sense of
   Applegate–Lagarias has λ* ≤ λ_k.

Status of these statements in the literature:
- Item 3 was claimed as "easy to prove" in [AL2, §4], with a one-line sketch.
- [KL, §6], eight years later and with Lagarias as co-author, writes: *"It remains an open problem to show that the
  values λ_k are strictly increasing in k."*
- Items 1 and 2 are [KL]'s conditions (1) and (2): *"We think it likely that properties (1), (2) hold for all k ≥ 2,
  but this may be difficult to prove."*
- Item 2 is also asserted without proof in [AL2, §4]: "At an optimal solution of (L^NT_k), all of (4.2a)–(4.2c) must
  hold with equality".
- The first half of item 4 is [KL]'s belief after Theorem 2.2: "We believe, although we have no proof, that this
  result gives the largest exponential-type lower bound that can be extracted from the difference inequalities I_k".
- The second half of item 4 is [AL2, Conjecture 4.1].

The sketch in [AL2] shows that the lifted solution has a strict inequality somewhere. It then concludes "not
optimal, hence λ*(L^NT_k) > λ*(L^NT_{k−1})". For a general parametric LP, slack in one row does not allow the
parameter to increase. The missing ingredient is an irreducibility property, which is the key fact below.

**Key fact.** m ↦ 4m permutes [3^k] = {m mod 3^k : m ≡ 2 (mod 3)} as a single cycle of length 3^{k−1}. Every
principal inequality contains the term λ^{−2} c_{4m}, with no minimum. Consequently:
- strict slack in one row spreads backwards along the cycle to every row (Lemma 3);
- zeros spread forwards along the cycle (Lemmas 4, 7).

Everything else is elementary: monotonicity, homogeneity, superadditivity and continuity of the right-hand side, a
compactness argument, and the "descent" argument that [AL2] already has in a footnote.

**Machine-checked.** The following are formalised in Lean 4 + Mathlib (`lean_formal/KLMonotone/`, ≈1340 lines,
standard axioms only, no certificates; standalone build and `leanchecker` replay; main theorem
`KLMono.KL_lambda_strictMono`):
- Theorem (i)–(iii) and the uniqueness;
- Corollary 1 (exact solution of I_k);
- the closed form ρ_k = 3(λ_k − 1)/λ_k^α of §4a, with 1 − ρ_k strictly decreasing;
- the equivalence with K–L's literal program (2.7)–(2.14). Corollary 2 is not formalised:
it would need A–L's splitting framework.

References:
- [AL2] D. Applegate, J. C. Lagarias, Density bounds for the 3x+1 problem II. Krasikov inequalities, Math. Comp. 64
  (1995) 427–438 (preprint dated 15 Dec 1993, used here).
- [KL] I. Krasikov, J. C. Lagarias, Bounds for the 3x+1 problem using difference inequalities, Acta Arith. 109 (2003)
  237–258, arXiv:math/0205002.

## 1. Setting

Fix k ≥ 2, put N = 3^{k−1}, α = log₂ 3, and identify the class m = 3i + 2 (mod 3^k) of [3^k] with its index
i ∈ ℤ/N. Then:
- the class m ≡ 2, 5, 8 (mod 9) corresponds to i ≡ 0, 1, 2 (mod 3);
- 4m corresponds to ν(i) := 4i + 2 (mod N);
- the auxiliary classes r ∈ [3^{k−1}] correspond to s ∈ ℤ/(N/3);
- the three lifts r, r + 3^{k−1}, r + 2·3^{k−1} correspond to s, s + N/3, s + 2N/3 (mod N).

For m ≡ 2 (mod 9), i.e. i = 3j, the auxiliary class (4m−2)/3 has index a(i) := 4j (mod N/3). For m ≡ 8 (mod 9),
i.e. i = 3j + 2, the auxiliary class (2m−1)/3 has index b(i) := 2j + 1 (mod N/3). (These are the formulas in
`kl.py` and CLAUDE.md, verified there against an independent LP.) For k = 2 we have N/3 = 1 and a ≡ b ≡ 0.

For c ∈ V := ℝ^{ℤ/N} with c ≥ 0 define c̄ ∈ ℝ^{ℤ/(N/3)} and F_λ(c) ∈ V by

  c̄_s = min(c_s, c_{s+N/3}, c_{s+2N/3}),

  F_λ(c)_i = λ^{−2} c_{ν(i)} + λ^{α−2} c̄_{a(i)}   (i ≡ 0 mod 3),
  F_λ(c)_i = λ^{−2} c_{ν(i)}                      (i ≡ 1 mod 3),
  F_λ(c)_i = λ^{−2} c_{ν(i)} + λ^{α−1} c̄_{b(i)}   (i ≡ 2 mod 3).

When the level matters we write F^{(k)}_λ.

**Feasibility.** As [KL, §2 and §6] note, L^NT_k(λ) has a feasible solution iff there is a positive c with c ≤ F_λ(c):
- the auxiliary variables can be raised to c̄;
- a positive solution can be rescaled to min c = 1;
- C^max is free.

So we define

  Λ_k := {λ ∈ [1, 2] : there is c > 0 with c ≤ F_λ(c)},   λ_k := sup Λ_k.

The restriction λ ≤ 2 is the range of [KL, Theorem 2.2], which turns a feasible point into a bound for π_a(x).
[AL2, §2] also takes 1 ≤ λ ≤ 2 as an a priori range. Whether L^NT_k(λ) is ever feasible for λ ≥ 4 plays no role
here. (Summing the inequalities excludes 2 < λ < 4, see Lemma 6.)

Inequalities between vectors are componentwise; c > 0 means every component is positive.

## 2. Lemmas

**Lemma 1 (structure of F).** For λ > 0:
(a) F_λ is monotone on V_{≥0}: 0 ≤ x ≤ y implies F_λ(x) ≤ F_λ(y).
(b) F_λ is positively 1-homogeneous.
(c) F_λ is superadditive on V_{≥0}: F_λ(x + y) ≥ F_λ(x) + F_λ(y).
(d) (λ, c) ↦ F_λ(c) is continuous on (0, ∞) × V_{≥0}.
(e) F_λ(x)_i ≥ λ^{−2} x_{ν(i)} for x ≥ 0.

*Proof.* Each component is a nonnegative combination of coordinates and of minima of coordinates. This gives
(a), (b) and (d), and (e) is immediate. For (c): min(x_p + y_p) ≥ min x_p + min y_p over the same index set. ∎

**Lemma 2 (single cycle).** ν is a cyclic permutation of ℤ/N of length N.

*Proof.* ν corresponds to m ↦ 4m on [3^k]. Since m is a unit mod 3^k, 4^n m ≡ m (mod 3^k) iff 4^n ≡ 1 (mod 3^k).
By lifting the exponent, v₃(4^n − 1) = v₃(4 − 1) + v₃(n) = 1 + v₃(n). So 4^n ≡ 1 (mod 3^k) iff 3^{k−1} | n. Every
orbit therefore has length 3^{k−1} = N = |[3^k]|. ∎

(Checked by direct iteration for k = 2, …, 14.)

**Lemma 3 (propagation of slack).** Fix λ > 0 and write F = F_λ. Let x > 0 with F(x) ≥ x and F(x) ≠ x. Then there
are z > 0 and η > 0 with F(z) ≥ (1 + η) z.

*Proof.* Put y_n = F^n(x), so y_0 = x. From F(x) ≥ x and monotonicity, y_{n+1} ≥ y_n for all n. Let
S_n = {i : (y_n)_i > x_i}; then S_1 ≠ ∅ and S_n ⊆ S_{n+1}.

Let i ∈ S_n and let i′ = ν^{−1}(i). Write A_{i′}(·) for the auxiliary part of row i′, which is monotone. Then

  (y_{n+1})_{i′} = λ^{−2} (y_n)_i + A_{i′}(y_n) > λ^{−2} x_i + A_{i′}(x) = F(x)_{i′} ≥ x_{i′},

so i′ ∈ S_{n+1}. Hence S_{n+1} ⊇ S_n ∪ ν^{−1}(S_n). By Lemma 2, S_N = ℤ/N, so y_N ≥ (1 + ε) x for some ε > 0.

Let z = y_0 + … + y_{N−1} > 0. By superadditivity,

  F(z) ≥ F(y_0) + … + F(y_{N−1}) = y_1 + … + y_N = z − x + y_N ≥ z + ε x.

Since x > 0, there is M with z ≤ M x componentwise, so F(z) ≥ (1 + ε/M) z. ∎

**Lemma 4 (positivity).** Let x ≥ 0, x ≠ 0, with F_λ(x) ≥ x. Then y = F_λ^{N−1}(x) > 0 and F_λ(y) ≥ y.

*Proof.* By Lemma 1(e), F(x)_{i′} ≥ λ^{−2} x_{ν(i′)}. Together with F(x) ≥ x this gives
supp F(x) ⊇ supp x ∪ ν^{−1}(supp x). After N − 1 steps the support is everything, by Lemma 2. Finally
F(y) = F^N(x) ≥ F^{N−1}(x) = y, because the iterates increase. ∎

**Lemma 5 (openness).** If λ₀ > 0, z > 0 and F_{λ₀}(z) ≥ (1 + η) z with η > 0, then F_λ(z) ≥ z for all λ in a
neighbourhood of λ₀.

*Proof.* Lemma 1(d), applied to the N components at the fixed point z. ∎

**Lemma 6 (summation).** For c ≥ 0,

  Σ_i F_λ(c)_i = λ^{−2} Σ_i c_i + (λ^{α−2} + λ^{α−1}) Σ_s c̄_s,   and   Σ_s c̄_s ≤ (1/3) Σ_i c_i,

with equality in the second relation iff c is *top-digit invariant*, i.e. c_{s + uN/3} does not depend on u.

*Proof.* ν is a bijection of ℤ/N. The map a: {3j} → ℤ/(N/3), 3j ↦ 4j, is a bijection because 4 is invertible
mod N/3. So is b: {3j+2} → ℤ/(N/3), 3j+2 ↦ 2j+1. This proves the identity.

For the inequality, c̄_s ≤ (c_s + c_{s+N/3} + c_{s+2N/3})/3, and the lifts of all s partition ℤ/N. Equality holds
for every s iff each triple is constant. ∎

So a feasible c at λ gives (1 − λ^{−2}) ≤ (1/3)(λ^{α−1} + λ^{α−2}) ρ with ρ = 3 Σc̄/Σc ≤ 1. This is [AL2, (4.5)] and
[KL, §6]. The function 1 − λ^{−2} − (λ^{α−1} + λ^{α−2})/3 vanishes at λ = 2 and λ = 4 (4^{α−1} = 9/4,
4^{α−2} = 9/16), and is positive in between.

**Lemma 7 (uniqueness of fixed points).** If c, c′ > 0 and F_λ(c) = c, F_λ(c′) = c′, then c′ = t c for some t > 0.

*Proof.* Let t = min_i c′_i / c_i, attained at i₀, and put d = c′ − t c ≥ 0, so d_{i₀} = 0. By superadditivity,

  c′ = F(t c + d) ≥ t F(c) + F(d) = t c + F(d),

so F(d) ≤ d. At i₀ this gives λ^{−2} d_{ν(i₀)} ≤ F(d)_{i₀} ≤ 0, so d_{ν(i₀)} = 0. Iterating along the cycle gives
d = 0. ∎

(The same argument with F(c) = r c and F(c′) = r′ c′ shows r = r′ and uniqueness of the positive eigenvector of F_λ
for every λ.)

**Lemma 8 (descent).** Let λ > 0, c > 0, and suppose the rows i ≡ 0 (mod 3) of c ≤ F_λ(c) hold with equality. If
c is top-digit invariant, then c is constant.

*Proof.* For 0 ≤ d ≤ k − 2, write D(d) for "c_i depends only on i mod 3^d". Top-digit invariance is D(k − 2),
because the top digit of i has place value N/3 = 3^{k−2}. D(0) means c is constant. We show D(d) ⇒ D(d − 1) for
1 ≤ d ≤ k − 2 (for k = 2 there is nothing to do).

Assume D(d). Since 3^d divides N/3, the three lifts s + uN/3 agree mod 3^d, so c̄_s = c_s = f(s mod 3^d) for a
function f on ℤ/3^d. Row i = 3j, j ∈ ℤ/(N/3), reads

  c_{3j} = λ^{−2} c_{12j+2} + λ^{α−2} f(4j mod 3^d).

Replace j by j′ = j + 3^{d−1}. Then:
- 3j′ ≡ 3j (mod 3^d), so the left side is unchanged;
- 12j′ + 2 ≡ 12j + 2 (mod 3^d), so the first term on the right is unchanged.

Hence f(4j) = f(4j + 4·3^{d−1}) = f(4j + 3^{d−1}) (mod 3^d). As j runs over ℤ/(N/3), 4j runs over all of ℤ/3^d.
So f(t) = f(t + 3^{d−1}) for all t, i.e. f depends only on t mod 3^{d−1}. That is D(d − 1). ∎

[AL2, footnote on p. 15] uses the same downward induction.

**Lemma 9 (tiling).** Let c ∈ V^{(k)}_{≥0} and x = tile(c) ∈ V^{(k+1)}, i.e. x_{i + tN} = c_i for i ∈ ℤ/N and
t ∈ {0, 1, 2}. Then

  F^{(k+1)}_λ(x)_{i+tN} = F^{(k)}_λ(c)_i + δ_{i,t},   δ_{i,t} ≥ 0.

Here δ_{i,t} = 0 for i ≡ 1 (mod 3). For i ≡ 0 (resp. 2) (mod 3):
- δ_{i,t} = λ^{α−2}(c_ℓ − c̄_{a(i)}) (resp. λ^{α−1}(c_ℓ − c̄_{b(i)}));
- ℓ = ℓ(i, t) is a lift of a(i) (resp. b(i));
- as t runs over {0, 1, 2}, ℓ runs over all three lifts.

In particular F^{(k+1)}_λ(x) = tile(F^{(k)}_λ(c)) iff c is top-digit invariant.

*Proof.* Let N′ = 3N be the level-(k+1) size, whose auxiliary vectors have length N.
- *Class.* N ≡ 0 (mod 3), so i + tN and i have the same class.
- *×4 term.* ν′(i + tN) = 4i + 2 + 4tN (mod 3N), and x there equals c_{(4i+2) mod N} = c_{ν(i)}.
- *Auxiliary vector.* At level k+1, c̄′_ℓ = min_u x_{ℓ+uN} = c_ℓ for ℓ ∈ ℤ/N.
- *Class-0 rows.* For i = 3j, i + tN = 3(j + tN/3), and the auxiliary index is a′ = 4j + 4tN/3 (mod N). This is
  ≡ 4j = a(i) (mod N/3), so it is a lift of a(i). It runs through all lifts as t does, because 4t ≡ t (mod 3).
- *Class-2 rows.* For i = 3j + 2, b′ = 2j + 1 + 2tN/3 (mod N), a lift of b(i), and 2t (mod 3) is a bijection.

Comparing with F^{(k)}_λ(c)_i, which uses the minimum c̄_{a(i)} (resp. c̄_{b(i)}), gives the formula.

For the last statement: δ ≡ 0 iff each referenced triple is constant. Every auxiliary index is referenced by
class-0 rows, since a is onto. ∎

## 3. The theorem

**Theorem.** For every k ≥ 2:
(i) λ_k ∈ Λ_k and 1 < λ_k < 2.
(ii) Every c > 0 with c ≤ F_{λ_k}(c) satisfies c = F_{λ_k}(c), and such c is unique up to a positive factor.
(iii) λ_k < λ_{k+1}.

*Proof.*

*Step 1: λ_k > 1.* With c = 1, F_1(1)_i = 1 + [i ≢ 1 mod 3] ≥ 1, with strict inequality on class 0. Lemma 3 gives
z > 0 and η > 0 with F_1(z) ≥ (1 + η) z, and Lemma 5 then gives [1, 1 + δ) ⊆ Λ_k for some δ > 0.

*Step 2: 2 ∉ Λ_k.* Let c > 0 with c ≤ F_2(c). By Lemma 6, using 2^{α−2} + 2^{α−1} = 9/4,

  Σ c ≤ Σ F_2(c) = (1/4) Σ c + (9/4) Σ c̄ ≤ (1/4 + 3/4) Σ c = Σ c.

All inequalities are therefore equalities. So c = F_2(c), and c is top-digit invariant (Lemma 6). By Lemma 8, c is
constant. The class-1 row c = 2^{−2} c then forces c = 0, a contradiction.

*Step 3: Λ_k is closed.* Let λ_n ∈ Λ_k with λ_n → λ*, and let c_n > 0 be feasible, normalised by Σ c_n = 1. A
subsequence converges to some x ≥ 0 with Σ x = 1, and F_{λ*}(x) ≥ x by Lemma 1(d). By Lemma 4, F^{N−1}_{λ*}(x) is
a positive feasible point, so λ* ∈ Λ_k. Hence λ_k = max Λ_k, and by Steps 1–2, 1 < λ_k < 2. This proves (i).

*Step 4: tightness.* Let c > 0 with c ≤ F_{λ_k}(c), and suppose F_{λ_k}(c) ≠ c. Lemma 3 gives z > 0 with
F_{λ_k}(z) ≥ (1 + η) z, and Lemma 5 gives F_λ(z) ≥ z for λ ∈ [λ_k, λ_k + δ]. Since λ_k < 2 we may take
λ_k + δ ≤ 2, which contradicts λ_k = max Λ_k. Uniqueness follows from Lemma 7. This proves (ii).

*Step 5: strict increase.* Let c be the fixed point from (ii). It is not top-digit invariant: otherwise it would be
constant by Lemma 8, and the class-1 row c = λ_k^{−2} c would force λ_k = 1, contradicting Step 1.

Put x = tile(c) at level k + 1. By Lemma 9, F^{(k+1)}_{λ_k}(x) ≥ tile(F^{(k)}_{λ_k}(c)) = x, with strict inequality
in some row. Lemma 3 (at level k + 1, where Lemma 2 also holds) and Lemma 5 give λ_k + δ ∈ Λ_{k+1} for some
δ > 0 with λ_k + δ ≤ 2. So λ_{k+1} > λ_k. ∎

## 4. Consequences for the difference inequalities

**Corollary 1 (exact exponential solution; [KL]'s conditions (1), (2) and their belief).** Let c be the fixed point
of (ii), scaled so that min c = 1, and put φ^m_k(y) = c^m λ_k^y for y ≥ 0. Define φ^n_j for j < k by the
minimisation relations (P3), so φ^n_j(y) = c^{(j),n} λ_k^y, where c^{(j)} is the iterated c̄.

Then the φ are positive (≥ 1) and nondecreasing, and they satisfy I_k with equality for every y. Indeed, (D1)–(D3)
divided by λ_k^y are exactly the rows of c = F_{λ_k}(c).

Hence any statement of the form "every positive nondecreasing solution of I_k satisfies φ^m_k(y) ≥ C λ^y for large
y" has λ ≤ λ_k. Conversely, [KL, Theorem 2.2] applied at λ_k itself (now allowed by (i)) gives

  π_a(x) ≥ x^{log₂ λ_k}   for x ≥ x₀(a).

The exponent log₂ λ_k is therefore attained, and it is optimal for I_k.

**Lemma 10 (projection).** Let φ_k = {φ^m_k} be any family satisfying I_k, and let φ_j be its iterated minima. Then
φ_j satisfies I_j for 2 ≤ j ≤ k.

*Proof.* Let n ≡ 2 (mod 9) in [3^j], and let m ∈ [3^k] be any lift of n (m ≡ n mod 3^j), so m ≡ 2 (mod 9). The
inequality (D1) for m reads

  φ^m_k(y) ≥ φ^{4m}_k(y − 2) + φ^{(4m−2)/3}_{k−1}(y + α − 2).

Two facts about the right side:
- 4m is a lift of 4n mod 3^j, so φ^{4m}_k ≥ φ^{4n}_j.
- (4m − 2)/3 ≡ (4n − 2)/3 (mod 3^{j−1}), so it is a lift of (4n−2)/3 at level j − 1, and therefore
  φ^{(4m−2)/3}_{k−1} ≥ φ^{(4n−2)/3}_{j−1}.

So the right side is at least φ^{4n}_j(y−2) + φ^{(4n−2)/3}_{j−1}(y+α−2), for every lift m. Minimising the left side
over the lifts gives (D1) for n at level j. (D2) and (D3) are the same. ∎

**Corollary 2 ([AL2, Conjecture 4.1]).** Let (L) be a linear program in the sense of [AL2, (2.9)], derived from I_k
(and I_l, 2 ≤ l < k) by repeated splitting and then µ-truncation. Then λ*(L) ≤ λ*(L^NT_k) = λ_k. The same holds for
the limit µ → 0.

*Proof.* Take the exponential family φ of Corollary 1.
- *It satisfies the derived system.* It satisfies I_k, and by Lemma 10 the I_l. Splitting substitutes valid
  inequalities into right-hand sides, so the derived inequalities hold. µ-truncation replaces φ(y′) by
  φ(y − µ) ≤ φ(y′) for y − µ ≤ y′, which is valid because φ is nondecreasing. So φ satisfies (2.8).
- *Theorem 2.1 applies to it.* The proof of [AL2, Theorem 2.1] uses only three things:
  - the inequalities (2.8);
  - the minimisation relations between levels;
  - φ ≥ 1 on an initial interval.

  So it applies to φ and gives φ^m_k(y) ≥ a c′^m λ*(L)^y for all y > 0, with a > 0 and c′ > 0.
- *Conclusion.* Since φ^m_k(y) = c^m λ_k^y, letting y → ∞ forces λ*(L) ≤ λ_k. For µ → 0 use
  λ*(+₀) = lim λ*(+_µ) [AL2, §2]. ∎

## 4a. Corollary: the mean loss has a closed form and decreases strictly

At λ_k all rows are tight (Theorem (ii)), so Lemma 6 is an identity: (1 − λ_k^{−2}) Σ c = (λ_k^{α−2} + λ_k^{α−1}) Σ c̄.
Since λ^{α−2} + λ^{α−1} = λ^α (1 + λ)/λ² and 1 − λ^{−2} = (λ − 1)(λ + 1)/λ², the mean loss of the (unique) solution
has the closed form

  ρ_k := 3 Σ c̄ / Σ c = R(λ_k),   R(x) = 3 (x − 1) / x^α.

Its derivative is R′(x) = 3 x^{−α−1} (α − (α − 1) x), which is positive for x < α/(α − 1) ≈ 2.71. So R is strictly
increasing on [1, 2], and by Theorem (iii) **ρ_k is strictly increasing in k, i.e. the mean loss 1 − ρ_k strictly
decreases**.

Check against the data: λ_21 = 1.8925462 gives 1 − ρ = 0.0258 and λ_22 = 1.8988933 gives 0.0241, matching the ρ
table (`rho.py`). The relation is exact, so the 1 − ρ_k table and the λ_k table carry the same information.

Lean: `KLMono.rho_eq` (ρ(c) = R(λ_k) for every feasible c at λ_k) and `KLMono.rho_strictMono`.

## 4b. The same theorem for the 5x+1 system

`kl5.py` uses the K–L system for T₅(n) = n/2, (5n+1)/2:
- classes a = 5i + 3 (mod 5^k), i ∈ ℤ/N with N = 5^{k−1}, and t = i mod 5;
- the return map ν₅(i) = 16i + 9 (mod N), i.e. a ↦ 16a, with coefficient λ^{−4};
- auxiliary maps into ℤ/(N/5), with the minimum over 5 lifts:
  - t = 0: (16i + 5)/5, weight λ^{β−4};
  - t = 1: (2i − 2)/5, weight λ^{β−1};
  - t = 3: (8i + 1)/5, weight λ^{β−3};
  - t = 4: (4i − 1)/5, weight λ^{β−2};
- no auxiliary term for t = 2;
- β = log₂ 5.

Every lemma carries over.
- **Lemma 2.** 16 = 1 + 3·5 with v₅(16 − 1) = 1, so 16 has order 5^{k−1} modulo 5^k, and ν₅ is one N-cycle
  (checked for k ≤ 9).
- **Lemmas 1, 3, 4, 5, 7.** Verbatim.
- **Lemma 6.** For t ∈ {0, 1, 3, 4}, writing i = 5j + t, the auxiliary index is a unit multiple of j plus a constant
  (16j + c, 2j, 8j + c′, 4j + c″ mod N/5). So each class t maps bijectively onto ℤ/(N/5), and
  Σ F(c) = λ^{−4} Σ c + (Σ_t w_t) Σ_s c̄_s, with 5 Σ c̄ ≤ Σ c.
  - Equality forces top-digit invariance.
  - (1 − λ^{−4}) − (Σ_t w_t)/5 vanishes at λ* = 1.5701677 (Malthus root; AVENUES §8) and at λ = 2, and is
    positive in between, so a feasible point needs λ ≤ λ* or λ ≥ 2.
  - At λ* the inequalities are therefore tight and c is top-digit invariant.
- **Lemma 8.** Use the rows t = 1: c_{5j+1} = λ^{−4} c_{16(5j+1)+9} + w₁ f(2j). Replacing j by j + 5^{d−1} fixes
  the left side and the ×4 term mod 5^d (16·5^d ≡ 0) and shifts the argument of f by 2·5^{d−1}. Since 2 is a unit
  mod 5, f is invariant under 5^{d−1}. So a tight top-digit-invariant point is constant, and the rows t = 2
  (no auxiliary term) force λ = 1.
- **Lemma 9.** At level k + 1 the auxiliary index of row i + uN is the level-k index plus (unit)·u·N/5. So the five
  values of u hit the five lifts, and the tiled vector gains exactly where c varies over its top digit.

**Theorem (5x+1).** Define λ_k(5) = sup{λ ∈ [1, λ*] : feasible}. Then for every k ≥ 2:
- λ_k(5) is attained and 1 < λ_k(5) < λ*;
- at λ_k(5) every feasible point is tight and unique up to scaling;
- λ_k(5) < λ_{k+1}(5).

The proof is that of §3 with 2 replaced by λ*. Feasibility in [λ*, 2) is excluded by the summation identity, so
nothing is lost by the restriction.

Numerical confirmation (`notes/check5_monotone.py`): ν₅ is one cycle for k ≤ 9; the tiling gain is positive on
exactly 16/25 of the rows (four classes with auxiliary terms, four of five lifts non-minimal); and
r_{k+1}(λ_k) ≥ 1.061, 1.055, 1.065, 1.036, 1.025 for k = 2…6. This 5x+1 version is not formalised. The Lean
development is specific to 3x+1, but its abstract lemmas (`Fc_*`, `exists_strict`, `exists_pos`, `fixed_unique`)
would transfer.

## 5. Remarks

1. **What is not proved.** The argument gives no rate. In Lemma 3, slack travels backwards along the ×4 cycle with a
   factor λ^{−2} per step. Rows whose forward ×4 orbit meets no positive gain for many steps get exponentially small
   gains. Typical gain-free runs are class 5 rows (no auxiliary term) and rows where the tiled lift is the minimising
   one; there are runs of length about log N/log(9/5) ≈ 1.9 k. So the δ in Step 5 is not quantitative. A
   quantitative version, λ_{k+1} − λ_k ≥ κ (2 − λ_k) with κ > 0 independent of k, would give geometric convergence
   λ_k → 2: by Lemma 6 and tightness, 2 − λ_k is comparable to 1 − ρ_k. That is the open problem of avenue 1, now
   in a sharper form: control how the auxiliary (expanding, mixing) branch spreads the gain, instead of the ×4
   (isometric) branch used here.

2. **Numerical confirmation** (`monotone_check.py`, log in the module docstring's sections (1)–(4)).
   - (1) ν is a single N-cycle for k = 2 … 14.
   - (2) For k = 2 … 9, at λ_k with the power-iterated fixed point (|F(c)/c − 1| ≤ 10^{−7}), the tiling gain δ of
     Lemma 9 is exactly zero on class 1 (m ≡ 5). It is positive on exactly 2/3 of class 0 and 2/3 of class 2, i.e. on
     4/9 of the rows, with the minimising lift as the remaining third. The vector z of Lemma 3 gives the
     Collatz–Wielandt bounds r_{k+1}(λ_k) ≥ 1.1042 (k = 2), 1.0490, 1.0252, 1.0153, 1.0116, 1.0103, 1.0066 and
     1.0059 (k = 9).
   - (3) Power iteration from five random positive starts converges to the same direction as c_k, to 10^{−15}
     (k = 2 … 8), as Lemma 7 says it must.

3. **The range λ ≥ 4, and monotonicity in λ.** Lemma 6 excludes 2 < λ < 4 at every k, but not λ ≥ 4. Averaging over
   lifts (min ≤ mean) bounds r(F_λ) by the common column sum λ^{−2} + (λ^{α−2} + λ^{α−1})/3. That is < 1 exactly on
   (2, 4), so it says nothing at λ ≥ 4. Class-dependent rescalings c = λ^{e(class)} d cannot make all coefficients
   nonincreasing in λ either: the class-8 rows whose auxiliary class is again class 8 obstruct it (the 3-adic fixed
   point m = −1 of m ↦ (2m − 1)/3).
   Numerically (`monotone_check.py` (4), k = 2 … 7):
   - r_k(λ) is strictly decreasing on [1, 2] (41-point grid; r(1) ≈ 1.52–1.66, r(2) ≈ 0.61–0.90);
   - r_k(λ) < 0.57 for every λ ∈ {4, 4.5, 5, 6, 8, 12, 20, 50, 100, 1000}.

   So {λ ≥ 1 : L^NT_k(λ) feasible} = [1, λ_k] looks true, but it is not proved, and nothing above needs it. The
   definition with λ ∈ [1, 2] matters for [KL, Theorem 2.2], which is stated for 1 ≤ λ ≤ 2. It is also the quantity
   computed in [KL, Table 2] and in this project.

4. **Relation to nonlinear Perron–Frobenius theory.** F_λ is a monotone, homogeneous, concave map (a min of linear
   maps) whose dependency graph contains a Hamiltonian cycle with strictly positive weights. Lemmas 3, 4 and 7 are
   instances of the standard Perron–Frobenius theory for such maps (Gaubert–Gunawardena, Lemmens–Nussbaum), proved
   here directly because the cycle makes it two lines.
