# Absolute continuity of ν_p via the conditional collision (2026-10-10, night)

Target: ν_p, the stationary law of x ↦ x/2 (prob q = 1 − p), x ↦ (3x+1)/2 (prob p) on ℤ₃, for p = 1/4. Its density
is the Applegate–Lagarias limit function W_∞. We want ν_p ≪ Haar, ideally with an L² density.

Scripts: `cond_collision.py` (NumPy reference), `cond_collision_mlx.py` (GPU, deeper levels; writes
`cond_collision_L{ℓ}.json`).

## 0. Why a new route

Every previous attempt (`notes/limit_function.md`, steps 3–6) worked with |ν̂| or with signed Fourier recursions.
The decay there comes from cancellation, and every positive majorant hit the pure 2-power chain near the identity.

This route conditions on block sums. That makes the problem **positive**: no cancellation is needed anywhere. The
price is some collision (Rényi-2) entropy, which is affordable exactly when p < 1/3.

## 1. Reduction (rigorous)

Fix a block length ℓ. Group the gaps a_1, a_2, … into consecutive blocks of ℓ. Write c_i for the block sums
(i.i.d. negative binomial NB(ℓ, p) on {ℓ, ℓ+1, …}) and C = (c_1, c_2, …).

Given C, the arrangement of each block is uniform over the N(c) = C(c−1, ℓ−1) compositions of c_i, independently
across blocks. The rotations 2^{−(c_1+…+c_{i−1})} are fixed by C, so the conditional law μ_C of X is a
**convolution of independent block laws**:

  X = Σ_i 3^{ℓ(i−1)} 2^{−C_{i−1}} V_i,   V_i = 2^{−c_i} N_{V_i},   N_V = Σ_{t=1}^{ℓ} 3^{t−1} 2^{c−S_t} ∈ ℤ.

Since ν = E_C μ_C and ‖·‖₂² is convex,

  ‖ν_m‖₂² ≤ Γ_m := E_C[3^m P(X ≡ X′ mod 3^m | C)] = Σ_{ξ of level ≤ m} R(ξ).

Here X and X′ are conditionally independent given the same C, and R(ξ) = E_C ∏_i |β̂_{c_i}(ζ_i)|² ≥ 0, with
β_c the block law. **If sup_m Γ_m < ∞, then ν has an L² density.**

R satisfies R(ξ) = E_c[|β̂_c(ξ)|² R(3^ℓ 2^{−c} ξ)], with R ≡ 1 at level ≤ 0. Write M_j = Σ_{level j} R.

## 2. The circle operator and its exact eigenmeasure

Let Ŵ_c(y) = E e(y N_V), the **real** Fourier transform of the integer N_V, and w_c = |Ŵ_c|². For η of level
j′ ≥ 1, the lifts ξ with 3^ℓ 2^{−c} ξ = η have real coordinates 2^c (x_η + t)/3^ℓ (t mod 3^ℓ), and
|β̂_c(ξ)|² = w_c((x_η + t)/3^ℓ).

So the R-mass distribution ρ_j = Σ_{level j} R(ξ) δ_{x_ξ} on ℝ/ℤ satisfies, exactly, ρ_{j+ℓ} = 𝓛^* ρ_j, where

  (𝓛f)(x) = Σ_c P(c) Σ_{t=0}^{3^ℓ−1} w_c((x+t)/3^ℓ) · f(2^c (x+t)/3^ℓ).

**2-adic injectivity lemma.** N_V mod 2^c determines the composition. (Peel off 3^{ℓ−1}: the 2-adic valuation of
the remainder is a_ℓ, and so on; all exponents stay below c.) Consequences:
- P(N − N′ = 2^c m) = 0 for m ≠ 0.
- Lebesgue measure λ is an **eigenmeasure**: λ∘𝓛 = κ₀ λ, with

    κ₀ = 3^ℓ E_c[1/N(c)] = 3^ℓ p^{ℓ−1} = (3p)^ℓ / p   (p = 1/4: 4(3/4)^ℓ).

- Equivalently, the density-side adjoint 𝓛^† satisfies 𝓛^†1 ≡ κ₀. Since 𝓛^† is positive,
  ‖𝓛^† f‖_∞ ≤ κ₀ ‖f‖_∞, so 𝓛^† contracts **every** bounded density by κ₀.
- K := 𝓛1 = Σ_h a_h e(hx) with a_h = E_c 3^ℓ P(N − N′ = 3^ℓ h) ≥ 0. So K is continuous and positive definite,
  ∫K = a_0 = κ₀, and M_{j+ℓ} = ρ_j(K).

κ₀ < 1 for some ℓ iff p < 1/3 (p = 1/4: ℓ ≥ 5). This is the bounded-density threshold. At p = 1/2 the route
cannot work.

## 3. Numerics (all ℓ, levels up to 15–16)

Per-block ratio M_{j+ℓ}/M_j against κ₀ (`cond_collision_mlx.py`):

| ℓ | κ₀ | ratio at the deepest blocks |
|---|---|---|
| 5 | 0.9492 | 0.9493, 0.9507, 0.9512 |
| 6 | 0.7119 | 0.7104, 0.7116, 0.7118 |
| 7 | 0.5339 | 0.5326, 0.5341, 0.5343 |
| 8 | 0.4005 | 0.4006, 0.3998, 0.4012 |

Γ_15 = 4.69, 3.37 (ℓ = 6, j = 14), 2.84, 2.34. These sit above ‖ν‖₂² ≈ 1.75, as they must.

Profile of K for ℓ = 6, on level-8 points:
- the mean is κ₀;
- K ≤ 0.83 away from 0 and 1/2;
- K > 1 only within about 0.002 of 0 (K(0) ≈ 2.2) and of 1/2 (max 1.40).

The point 1/2 feeds 0 with weight exactly 1, because N_V is odd and so |Ŵ_c(1/2)| = 1. Dyadics m/2^s feed 0 with
weight E_c|Ŵ_c(m/2^s)|²: 1, 0.29, 0.19, 0.19, …. The mean over depth s decays like 0.69^s, and the maximum
plateaus near 0.07 (dyadics close to 1/3 and 2/3).

R-mass density near 0 and near 1/2, relative to the Lebesgue share, at scales σ = 10^{−1} … 10^{−6}: 0.5–1.4 for
every j ≤ 16, mostly 0.9–1.0. **No concentration at the bad points.** The mass is uniformly spread in the real
coordinate: the fraction in |x| < δ is 2δ to three digits.

The spikes of R are the pure 2-power characters 2^L/3^j (j = 16: L = 22, 21, 23, at x = 0.097, 0.049, 0.195). There
R reaches about 4300× the average, growing about 2–2.8× per level. They are the Fourier extremisers of the earlier
log. Their share of the **mass** is about j·(0.7–0.9)^j, which vanishes, and they sit where K ≈ κ₀. So in this
L¹ formulation they are harmless.

## 4. What remains (the precise open lemma)

M_{j+ℓ} = κ₀ M_j + ρ_j(K − κ₀), and K − κ₀ has mean zero. With ℓ = 6 it is enough to show:

  **Lemma (to prove).** For all large j, the normalised R-mass π_j = ρ_j/M_j puts mass at most η into the
  0.01-neighbourhoods of 0 and 1/2, with 0.83(1 − η) + 2.2η < 1, e.g. η = 0.1. Numerically η ≈ 0.04 (Lebesgue
  share).

Then M_j decays geometrically, Γ < ∞, and ν_{1/4} has an L² density. In particular it is absolutely continuous,
A–L's martingale is uniformly integrable, and E W_∞ = 1. With ℓ = 8 the room is larger: κ₀ = 0.40.

**Mechanisms available for the lemma:**
- **Coarse-grained density evolves by 𝓛^†.** At scales σ ≫ 2^c 3^{−j}, the 2-adic digits of characters in an
  interval are equidistributed by an exact CRT count, and 𝓛^† contracts sup norm by κ₀ exactly.
- **The grid identity holds for every shift.** Σ_{n<2^c} w_c((b+n)/2^c) = 2^c/N(c) for every b. Hence 𝓛^†1 ≡ κ₀.
  This does **not** by itself bound the inflow into a small neighbourhood. The pull-back intervals 3^ℓ(I+n)/2^c
  cover each point at most once, so one still needs the R-mass to be equidistributed near the grid (1/2^c)ℤ.
  (Corrected; an earlier draft of this note claimed a free bound.)
- **Self-loop at 0 and the dyadic tree are expanding.** The branch x ↦ 2^c x/3^ℓ multiplies the near-0 density by
  E_c[3^ℓ/2^c] = (3p/(1+p))^ℓ = 0.6^ℓ, against κ₀ = 4(0.75)^ℓ for the bulk. With an |x|^{−s} weight the factor is
  E_c[(3^ℓ/2^c)^{1−s}] < 1.

**Rigorous partial result: the continuous problem contracts.** On Hölder densities, 𝓛^† satisfies a Lasota–Yorke
inequality:

  |𝓛^†f|_α ≤ θ_α |f|_α + C‖f‖_∞,   ‖𝓛^†f‖_∞ ≤ κ₀‖f‖_∞,
  θ_α = (3^{1+α} p 2^{−α})^ℓ / (1 − q 2^{−α}).

The first term uses the exact grid sum. The second uses |ΔŴ_c| ≤ 2π|Δy|·E N. For example θ_{0.1} = 0.76 and
θ_{0.2} = 0.84 at ℓ = 6, and θ_{0.2} = 0.55 at ℓ = 8. So 𝓛^† has spectral radius ≤ max(θ_α, κ₀) < 1 on C^α, and
every **absolutely continuous** initial measure with Hölder density loses mass geometrically under 𝓛^*.

The actual ρ_j are discrete, supported on 3^{−j}ℤ. All remaining difficulty is in passing from smooth to discrete:
- 𝓛 itself roughens functions, since its branches expand by 2^c/3^ℓ.
- So point values of 𝓛^k 1 at the base points are not controlled by the C^α theory.

**Why the obvious discrete norms fail** (each was checked against the numbers above):
- *Sup density.* Fails at the spikes. A black character ξ (all c-predecessors near 0) has
  τ(ξ) = Σ_c P(c) w_c(y_c(ξ)) ≈ 1, against κ₀/3^ℓ ≈ 10^{−3} typically. So R/avg grows by 3^ℓ/κ₀ per block for as
  long as ξ stays black. Observed: 98 → 4323 between j = 10 and 16.
- *Morrey norm sup_I ρ(I)/|I|^{1−s} with one exponent.* The generic contraction factor
  Σ_c P(c)(3^ℓ/2^c)^{1−s} 2^c/N(c) is finite only for s < 0.415. Absorbing the spikes needs s ≳ log₃ 2.5 ≈ 0.85.
  This is the familiar "40 %" conflict: lifts consume about 4 bits of 2-adic scale per 1.58 bits of 3-adic level.
- *Discrete L^{1+ε} (Jensen on R = Σ_c P(c) w_c R(η_c)).* The weights sum to τ(ξ), not to κ₀/3^ℓ. So black
  characters again give the factor 3^{ℓ(q−1)}.

**Mass bookkeeping (heuristic, matches the data).** The spikes cost little mass:
- Black characters are rare: real coordinate < δ and a 2-adic run ≥ c, so a fraction about 2δ·2^{−c}.
- Black mass at level j comes only from the part of the previous level with x < δ·3^ℓ/2^c. So it shrinks by
  E_c[3^ℓ/2^c] = 0.6^ℓ per block, against κ₀ for the bulk. Observed for the top spike: 0.06 per block.

In path language:
- Paths in the good set G = {K ≤ 0.83} lose weight geometrically.
- Reaching the d-neighbourhood of 0 (or of 1/2 and the dyadics) from G costs weight ∝ d.
- A path can stay near 0 for log(δ/d)/(E c·log 2 − ℓ log 3) steps. While it does, its weight grows by up to K(0)
  per step, which gives a singularity of order (δ/d)^{0.08} at ℓ = 6. That is integrable.

**What is still missing:** a rigorous version of this bookkeeping, i.e. a Lyapunov function V ≥ 1 on ℝ/ℤ with
𝓛V ≤ θV at all 3-adic rationals. Its natural shape is V = 1 + Σ_b α_b (d_b/|x−b|)^s over b ∈ {0} ∪ dyadics,
with d_b ≈ ε 2^{−depth}, small s and α_b ≈ v_b × const.

The delicate cases:
- (i) Points x whose images z_t land within 3^{−j−ℓ} of a singularity through a branch with non-negligible P(c).
  This happens exactly at the "anti-black" points k ≡ r·2^{−c} (mod 3^j) with small r and c, i.e. returns to the
  identity, a Diophantine (Baker-type) condition.
- (ii) Tail bounds in c, uniform over all positions.

This is a positive, explicit problem on the circle, and no cancellation has to be controlled anywhere. It is
nonetheless a substantial computer-assisted project.

## 5. Relation to earlier steps

- The κ₀-eigenmeasure is the conditional analogue of the diagonal L² factor 3p/(2−p), which is exact for the
  unconditioned problem (step 2). Here the off-diagonal part has **exact mean zero**, by the 2-adic injectivity
  lemma, rather than being merely numerically small.
- The near-identity/2-power chain, fatal for sup and ℓ² certificates (steps 5–6), shows up here only as sparse
  spikes. Their total mass is small and they sit where K ≈ κ₀.
