# The Applegate–Lagarias limit function: steps 1–3 toward Conjecture C′ (2026-10-10)

Target: Conjecture C′ of Applegate–Lagarias, C^−(4/3)^k ≤ N*_k(a) ≤ C^+(4/3)^k for all a ≢ 0 (mod 3), stated as
"Conjecture C#" in [AL2]. By Proposition 6 of `paper/preimage.md` it follows from the **Limit Function Conjecture**
of [AL2]. Scripts: `syracuse_measure.py`, `corr_recursion.py`, `md_operator_norms.py` (+ `md_operator_norms.json`).

## Step 1: what is known (priority)

**[AL2] D. Applegate, J. C. Lagarias, "The distribution of 3x+1 trees", Experiment. Math. 4 (1995) 193–209, §6**
(open access, read in full). It contains the following.
- **Thm 6.1:** the class averages E_k[l mod 3^j] = (W[l mod 3^j] + o(1))(4/3)^k. Their W[l mod 3^j] is our h_j:
  W[1 mod 3] = 6/7, W[2 mod 3] = 8/7, and (6.8) gives the j = 2 values.
- **Recursion (6.6):** W[l] = (3/4)(W[2l] + β(l) W[(2l − 1)/3 mod 3^{j−1}]), the same as ours. They prove the
  mean-value formula (6.9).
- **Thm 6.3:** {W_j} is a martingale. The proof is the induction (I − (3/4)P)A = 0 on top-digit sums, our
  "consistency" argument. By martingale convergence W_∞ = lim W_j exists a.e. on ℤ₃^×.
- **Table 3:** W_j^± for j ≤ 11. W_11^− = 0.491 and W_11^+ = 1.721 match our h_11.
- **Extremal Limit Conjecture:** limsup (3/4)^k N^+(k) = W_∞^+ and liminf (3/4)^k N^−(k) = W_∞^−.
- **Limit Function Conjecture:** W_∞ is continuous and nonzero on ℤ₃^×, and W_j → W_∞ everywhere. They show the
  two conjectures together imply C#.
- A small gap: (6.15) asserts E[W_∞] = 1. Martingale convergence gives only ≤ 1 unless the martingale is uniformly
  integrable, i.e. unless ν is absolutely continuous (see step 3).
- They remark on "some resemblance of (6.6) to the Krasikov inequalities" and do not pursue it.

**Wirsching** (LNM 1681; 1994 Markov chain) uses a different normalisation, a fixed number of odd steps, with a
Fabius-type invariant density on a real interval. [AL2] already note that the relation is unknown.

**What is new (as far as we can tell):**
1. The identification of W_∞·Haar as the stationary law ν_{1/4} of x ↦ x/2 (prob 3/4), x ↦ (3x+1)/2 (prob 1/4), with
   the series X = Σ 3^{j−1} 2^{−S(j)}, a_j ~ Geom(1/4).
2. **Prop. 6:** the Limit Function Conjecture *alone* implies C′. It uses the min/max residue-class certificates; no
   Extremal Limit Conjecture is needed.
3. The relation to Tao's Syracuse variable (p = 1/2) and to the Krasikov–Lagarias system at λ = 2.
4. The L² law and the thresholds p = 1/3 and p = 1/2.
5. Exact data supporting both conjectures: h_r to r = 17 and N^±(k) to k = 59/55, agreeing to 2·10^{−4}.

## Step 2: the exact two-point correlation recursion (`corr_recursion.py`)

Fourier on ℤ₃: ν̂(ξ) = q ν̂(ξ/2) + p e(ξ/2) ν̂(3ξ/2), with q = 1 − p. Define:
- S_n = Σ_{ξ of level n} |ν̂(ξ)|² = ‖δ_n‖₂², where δ_n is the level-n martingale difference;
- G_n(d, u) = Σ_{ξ of level n} e(uξ) ν̂(ξ) conj(ν̂(2^{−d}ξ)) = 3^n P(2^d(X + u) ≡ Y mod 3^n) − (same mod 3^{n−1}),
  for X, Y i.i.d. ~ ν. This is the correlation of δ_n under the affine map x ↦ 2^d(x + u).

The exact recursion (summing over the three preimages of ×3 kills every non-admissible term) is

  G_n(d, u) = 3p² Σ_{i,j ≥ 0 : 2^{i+1}u + 1 − 2^{i−d−j} ≡ 0 (mod 3)} q^{i+j} G_{n−1}(d + j − i, (2^{i+1}u + 1 − 2^{i−d−j})/3).

In particular, with u_d = (1 − 2^{−d})/3,

  S_n = (3p/(2 − p)) · [S_{n−1} + 2 Σ_{d ≥ 2 even} q^d Re G_{n−1}(d, u_d)].

This is checked to all printed digits for n ≥ 5. Odd d drop out exactly.

The states (d, u) range over d ∈ ℤ and u ∈ ℤ[1/2]. The cross terms are correlations under the maps
S_d = T₁^{−1} ∘ (×2^d) ∘ T₁, where T₁(x) = (3x+1)/2: conjugates of the doubling map. They have no fixed point in ℤ₃
(the formal fixed point is −1/3).

Numerically (p = 1/4) the normalised correlations ρ(d) = Re G(d, u_d)/S are tiny and shrinking:
- ρ(2) = −0.040, −0.034, −0.028, −0.024, −0.019 for n = 9 … 13;
- the other d are below 0.005;
- the weighted correction 2Σ q^d ρ(d) is −0.057 → −0.021.

For an L² contraction the correction need only stay below 4/3. By contrast, the pure doubling maps (u = 0) carry
large correlations, ρ(d, 0) ≈ q^{|d|}. These are "hot" states, and the S-recursion does not reach them in one step.

## Step 3: no contraction certificate on arbitrary martingale differences (`md_operator_norms.py`)

δ_n = K δ_{n−1} with K f(c) = Σ_j 3p q^j β(2^j c) f((2^{j+1}c − 1)/3), the same operator at every level (h_n = K h_{n−1}
too). We measured the Haar-normalised L² norm of K^m on all martingale differences at level L:

| m \ L | 4 | 6 | 8 | 10 | 11 | 12 | 13 |
|---|---|---|---|---|---|---|---|
| 1 | 1.0270 | 1.0355 | 1.0356 | | | | |
| 2 | 0.7177 | 0.7940 | 0.8365 | 0.8879 | 0.8889 | 0.9074 | 0.9190 |
| 3 | 0.4978 | 0.6193 | 0.6958 | 0.7695 | 0.7903 | 0.8164 | |
| 4 | 0.3415 | 0.4685 | 0.5708 | | | | |

- One step expands (1.0356 > 1). The sup-norm row sums are 1.43, and the positive weights of the correlation
  recursion sum to 1.53–1.71 per level. So no argument that ignores cancellation can work.
- Multi-step norms are below 1 at each finite L but keep growing with L. Adversarial martingale differences exploit
  ever finer alignment, with near-invariance under the twisted doubling maps. A level-uniform contraction for
  arbitrary martingale differences does not exist (numerically), so no finite operator-norm certificate can prove
  the conjecture.
- The 0.65-per-level decay of the actual δ_n is therefore arithmetic. It comes from the near-vanishing of their
  correlations under S_d, which is a Tao-type equidistribution property, not a property of K.

## Where the proof stands, and the next steps

1. **Absolute continuity: Tao's method does NOT transfer directly** (checked against the text, 2026-10-10).
   - *§7 (Prop. 1.17, polynomial Fourier decay) looks p-independent.* Given a + a′ = b the split is uniform for
     every geometric law. The pair sums are b_j ~ NB(2, p) with P(b = 3) = 2p²q > 0. Lemma 7.4 (black set =
     separated triangles) depends only on χ. The renewal part needs mean slope 2/p > log 9/log 2 (8 > 3.17).
   - *§6 (Prop. 1.17 ⇒ Prop. 1.14) is p = 1/2-specific.* It splits X_n = F_{k+1}(a_1…a_{k+1}) + 3^{k+1}2^{−l}(rest),
     with the stopping rule a[1,k+1] = l ≈ n log₂ 3 so that the offsets are injective mod 3^n (Cor. 6.3). It then
     bounds the collision entropy by max P(tuple) = 2^{−l} ≈ 3^{−n}. This step is exact only because Geom(2) has
     entropy equal to its mean, h(1/2) = 1 bit per unit of 2-adic size.
   - For p = 1/4, P(tuple) = (p/q)^{k+1} q^l with k + 1 ≈ l/4. Then 3^n Σ P² ≲ ((2q)^4 p/q)^{k+1} = 1.6875^{0.4n}
     = 2^{0.30n}, an entropy deficit of h(1/4) = 0.811 bits per unit.
   - To compensate, the second factor needs **exponential** Fourier decay: sup over ξ of level m of |ν̂_{1/4}(ξ)| ≤
     Cθ^m with θ < 2^{−1/4} ≈ 0.84 at level m ≈ 0.6n. Tao's §7 gives only m^{−A}.

   Numerically max |ν̂| decays like 0.64^m (`syracuse_measure.py`), so there is room, but exponential decay of the
   characteristic function is a new estimate. If it holds: Osc_{m,n}(ν_{1/4}) → 0, ν_{1/4} is absolutely
   continuous, A–L's martingale is uniformly integrable, and E W_∞ = 1 (closing the gap in [AL2, (6.15)]). The
   recursion ν̂(ξ) = Σ_j p q^j e(ξ/2^{j+1}) ν̂(3ξ/2^{j+1}) gains nothing from the triangle inequality, because the
   weights sum to 1. A proof must show that the phases e(ξ2^{−j−1}) of the dominant terms are spread: a Dolgopyat-type
   cancellation statement.

   **Tao's pairing as a positive majorant** (`fourier_majorant.py`). Conditioning on b = a + a′ gives
   |ν̂(ξ)| ≤ Σ_s p²q^s |Φ_s(ξ)| |ν̂(9ξ/2^{s+2})| with Φ_s(ξ) = Σ_{i ≤ s} e(ξ/2^{i+1}). Iterating from |ν̂| ≤ 1:

   | n | 10 | 11 | 12 | 13 | 14 | 15 |
   |---|---|---|---|---|---|---|
   | majorant | 4.05e-2 | 6.50e-2 | 2.59e-2 | 4.74e-2 | 1.59e-2 | 3.42e-2 |
   | ratio per 2 levels | 0.642 | 0.619 | 0.639 | 0.730 | 0.615 | 0.721 |
   | true max \|ν̂\| | 1.6e-4 | 9.8e-5 | 6.1e-5 | 3.8e-5 | 2.5e-5 | 1.6e-5 |

   - Even levels: 0.78 per level, below the 0.84 needed.
   - Odd levels: 0.85 per level, just above it.
   - The positive cosine majorant alone is therefore borderline. Characters like ξ = 2^l/3^n have large black
     triangles (Tao's Lemma 7.4) that switch off the saving for a constant fraction of the renewal path.

   **Next levers:**
   - condition on triples (a, a′, a″) instead of pairs, for more phases per saving step;
   - a sharper §6 split for p ≠ 1/2, using the actual L² mass of the first factor rather than its maximum
     (Hölder or additive-energy bounds instead of sup |ν̂|);
   - bound the total size of black triangles along a path; their corners are good rational approximations
     ξ3^{2j}2^{−l} ≈ 0 mod 1, so Baker-type bounds may cap how many can be large.

   Then make the result uniform in n. That is the step that turns per-level numerics into a proof.

   **Triples clear the threshold** (`fourier_majorant3.py`, output in `fourier_majorant3.txt`). Conditioning on
   c = a₁ + a₂ + a₃ (compositions uniform for any geometric law) gives
   |ν̂(ξ)| ≤ Σ_c P(c)|Ψ_c(ξ)||ν̂(27ξ/2^c)|, with P(c) = C(c−1,2)p³q^{c−3} and Ψ_c the average of e(ξ2^{−a₁}(1 + 3·2^{−a₂}))
   over compositions. Taking the max over *all* characters of level n, including the bad ones:

   | n | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 |
   |---|---|---|---|---|---|---|---|---|---|
   | majorant | 1.63e-2 | 3.80e-2 | 4.84e-2 | 6.29e-3 | 1.40e-2 | 2.03e-2 | 2.44e-3 | 5.67e-3 | 8.16e-3 |
   | rate per level (over 3 levels) | 0.702 | 0.718 | 0.730 | 0.728 | 0.717 | 0.748 | 0.730 | 0.740 | 0.739 |

   The rate is stable at 0.72–0.75 on all three residue chains (n = 17: 475 s, 40 GB), clearly below the 0.84
   that the §6 reduction needs for p = 1/4 with consecutive levels.

   **Proof outline for absolute continuity of ν_{1/4}** (A–L's W_∞ is a density, E W_∞ = 1):
   - (a) Exponential Fourier decay, sup_{level n} |ν̂| ≤ Cθⁿ with θ < 2^{−1/4}, for ALL n. The triple majorant gives
     θ ≈ 0.74 for n ≤ 17. What is missing is a uniform argument, i.e. Tao's black-triangle/renewal analysis made
     exponential with explicit constants, using triples.
   - (b) Tao's §6 with consecutive levels: entropy deficit 2^{0.30n} times θ^{1.2n} → 0, so Σ_n Osc_{n−1,n} < ∞ and the
     level densities converge in L¹.

   Item (a) is the remaining analytic lemma for this step. Continuity (C′) needs more: sup-norm control (§ above).
2. **Bounded density (W_∞^± finite), a possible shortcut.** A Donsker–Varadhan bound replaces the sup-norm
   Collatz–Wielandt step by an average. For a nonnegative irreducible B and v > 0,
   log r(B) ≥ Σ_c π_c log((Bv)_c/v_c), where π is stationary for the stochastic matrix P_cd = B_cd v_d/(Bv)_c. The
   Perron root of the min-system is min_s r(B_s) over top-digit selections s. With v = h_r this gives

     log μ_r ≥ log(4/3) − max_s ‖dπ^s/d(uniform)‖_∞ · E[ε]/(1 − ε_max),   with ε_c = (3/4)β(c)(mean − min over lifts)/h_r(c),

   and E[ε] ≲ ‖δ_r‖₁/min h_r. So **C′ (lower) ⇐ L¹ mixing (item 1) + bounded density + bounded density of the
   selection-chain stationary laws π^s.**

   The last condition is not automatic: a selection fixes the top digit as a function of the lower ones, and over
   time every digit was once selected. It needs its own argument. Boundedness of h is weaker than continuity, but no
   route to it is known yet. The upper side similarly needs W_∞^+ < ∞.
3. **Continuity (the full Limit Function Conjecture).** Needs sup-norm, or L^q with q > 2.65, control of δ_n, i.e.
   decorrelation of δ_n under the affine maps above in a quantitative, higher-moment form. The exact recursion of
   step 2 is the bookkeeping. The missing input is an equidistribution estimate for pairs (and quadruples) of
   "Syracuse offsets", of the kind Tao proves for single offsets.

## Step 5: toward uniform exponential Fourier decay (2026-10-10, evening)

Goal: sup over all level-n characters ξ of |ν̂_{1/4}(ξ)| ≤ Cθⁿ with θ < 2^{−1/4} ≈ 0.84 (or < 0.81 for Tao's
general split), for all n.

**1. The extremisers are the pure 2-power characters.** At every n = 9 … 13, the six characters with the largest
triple majorant are ξ = ±2^L/3^n (u = ±1 exactly), with L ≈ 0.87·n·log₂3. In Tao's picture they carry the one
maximal black triangle. Their decay is explained quantitatively:
- Such a character stays near the identity for about L/E[c] triple-steps (E[c] = 12).
- Since L ≤ n log₂3, that is at most a fraction log₂3/4 ≈ 0.40 of the path.
- On the rest it decays at the generic rate θ_g, so the worst rate is ≈ θ_g^{0.60}. With θ_g ≈ 0.6 this gives
  0.74, matching the observed 0.72–0.75.
- Requirement, in this model: θ_g < 0.84^{1/0.60} ≈ 0.75.

**2. The right space is the 2-adic solenoid.** For ξ = k/3^n, the values ξ2^{−t} mod 1 = (c_t + k/3^n)/2^t, where
c_t ∈ [0, 2^t) holds the first t binary digits of the 2-adic number −k·3^{−n}. So |Ψ_c(ξ)| is a continuous function
of the point (k/3^n, −k/3^n) in 𝕋₂ = (ℝ × ℚ₂)/ℤ[1/2]. The step ξ ↦ 27ξ2^{−c} is the group automorphism ×27/2^c of
𝕋₂.
- The level-n characters are the torsion points of order 3^n.
- The majorant is a positive transfer operator 𝒫 on C(𝕋₂), with 𝒫1(0) = 1 at the identity (the trivial
  character).
- The identity is a saddle: attracting in the real coordinate (×27/2^c contracts on average, E c = 12) and repelling
  in the 2-adic one.
- A character near the identity is "black", meaning k ≡ 2^L u with u small. It stays for about v₂(k)/12 steps,
  and v₂(k) ≤ log₂|k| ≤ n log₂3. That is the 40 % budget.

**3. One-step contraction away from the identity.** κ(ξ) = Σ_c P(c)|Ψ_c(ξ)| at n = 12:
- mean 0.17 per triple step; maximum 0.90 near the identity;
- maximum 0.53 (0.81 per level) over characters at 2-adic distance ≥ 10, where distance means
  min_L log₂|centred(k·2^{−L})|.

A binned majorant (bins = capped distance) is too lossy: 0.93 per level overall, 0.77 for the far block d ≥ 10.
Pure 2-power characters map to pure 2-power characters, so the bins must also carry the remaining 2-adic budget.

**4. Returns to the identity are a Baker-type question.** After a pure 2-power character escapes, its orbit is
2^{−s}/3^m. It returns near the identity only if 2^{−s} ≡ u (mod 3^m) with u small. That means 2^s u − 3^m t = 1
with small u and t, i.e. |s log 2 − m log 3| tiny with an exact unit relation. Baker's theorem rules this out
beyond O(log m) scales. General u needs S-unit or Baker bounds on 3^m t − 2^s u.

**Proof architecture (proposed, not done):**
- (i) A finite, level-independent contraction certificate for 𝒫 on 𝕋₂ minus a neighbourhood U of the identity.
  The state must include the real scale and the 2-adic budget, not just the distance. Target: θ_far below about
  0.75 per level, i.e. 0.42 per triple step. The generic rate is about 0.22.
- (ii) The budget near the identity: the first visit lasts at most v₂(k)/E[c] ≤ n log₂3/12 steps.
- (iii) Baker bounds showing that later visits are short, O(log n).
- (iv) A large-deviation bound for the renewal path c. Then |ν̂| ≤ Cθⁿ uniformly, and with §6 for p = 1/4,
  ν_{1/4} is absolutely continuous and A–L's W_∞ is a density with E W_∞ = 1.

Each piece is concrete. (i) is the main computational task: a Lyapunov function on a discretised solenoid with a
Lipschitz error bound. Continuity (C′) remains a further step.

**5. Who controls the black time.** For ξ = k/3^n the majorant path consumes the 2-adic digits of w = −k/3^n,
about E[c]/3 = 4 digits per level, so about 4n in all. The first n·log₂3 ≈ 1.585n digits are free: k ↦ w mod 2^T
is onto for T ≤ n log₂3. An adversarial k can therefore make roughly the first 40 % of the path black (all zeros:
k = 2^L·small, the extremisers). Beyond that, the digits are fixed by k (the eventually periodic expansion of k/3^n).

The uniform lemma therefore amounts to: *no k can buy more black time than its n·log₂3 free bits*. Information-
theoretically this is clear, but proving it for every k is a Diophantine statement about the 2-adic digits of
k/3^n (Baker or S-unit bounds for the returns).

**6. A possibly easier target: L² instead of sup.** Absolute continuity follows from Σ_n S_n < ∞, an average over
characters. Typical characters decay at about 0.38 per level (S_n ~ (3/7)^n spread over about 3^n characters), and
L² summability needs only < 3^{−1/2} ≈ 0.577. The worst case (0.64 true, 0.74 majorant) matters only through its
weight.

A fibre-averaged majorant is natural here: Σ_ξ B_n(ξ)² ≤ Σ_c P(c) max_η [Σ over the 27 lifts ξ of η: κ(ξ)|Ψ_c(ξ)|]
·Σ_η B_{n−3}(η)². Averaging over lifts randomises the top digits, so no adversary is involved, except along the
single 2-power chain (one lift of 2^L/3^{n−3} is again near the identity). Next step: a weighted L² norm that
discounts near-identity characters, plus an explicit treatment of the 2-power chain. This looks more tractable
than the sup-norm certificate (i).
