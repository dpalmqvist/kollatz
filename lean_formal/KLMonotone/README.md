# KLMonotone: the Krasikov–Lagarias constants λ_k are attained, tight and strictly increasing

Lean 4 formalisation of `notes/strict_monotonicity.md`. One file, `Basic.lean` (≈1340 lines), Lean v4.30.0-rc2 +
Mathlib, the same toolchain and Mathlib commit as Mazur's `collatz_predecessor_090` (we compile against its tree).
No `sorry`, no `native_decide`, no certificates. Every result depends only on `propext`, `Classical.choice`,
`Quot.sound`; see `axioms.txt` (from the standalone build with `autoImplicit = false`, `Audit.lean`). The module also
passes a kernel replay with `lake env leanchecker -v Basic`.

## Check it

Standalone, with the pinned Mathlib (`lakefile.toml`, `lake-manifest.json`, `lean-toolchain` here, the same
Mathlib commit 5450b53e as Mazur's development):

    export PATH="$HOME/.elan/bin:$PATH"
    cd lean_formal/KLMonotone && lake exe cache get && lake build

Or, faster, inside any existing project with this Mathlib (what was used on 2026-10-10):

    cd ~/devel/mazur_dl/collatz_predecessor_090-1.0.0
    lake env lean /path/to/kollatz/lean_formal/KLMonotone/Basic.lean

The check takes about 10 s on an M4 Pro. To reproduce `axioms.txt`, append `#print axioms KLMono.KL_lambda_strictMono`
(etc.) to a copy of the file.

## Independent kernel checks (2026-10-10)

Lean versions before the fix of kernel bug #14576 (July 2026: an axiom-free proof of False via `addDecl`-injected
inductives with wrong-structure projections) include the v4.30.0-rc2 used here. So the development was also checked
in two other ways:
- **Ported to Lean v4.35.0-rc3 + Mathlib c55e6e78** (post-fix; the same source file builds under both toolchains).
  Axioms are the standard three, and `leanchecker -v Basic` gives exit 0.
- **Exported with `leanexport`** (lean4export 3.1.0) and replayed in the independent Rust kernel **nanoda 0.4.17**
  (`nat_extension`, permitted axioms = the standard three): **"Checked 30006 declarations with no errors"**. That is
  the full closure, Mathlib included, in 4 s. Its pretty-printer output confirms the statements of
  `KL_lambda_strictMono`, `LamKL` and `KLFeasible`.
- **The original v4.30.0-rc2 build** was also exported, with lean4export at tag v4.30.0-rc2 (built in
  `~/devel/mazur_dl/tools/lean4export_v430`), and replayed in nanoda: **"Checked 29202 declarations with no
  errors"**.

## Main statements (namespace `KLMono`, level `k = n + 2`)

- `KLFeasible n λ` is Krasikov–Lagarias' program L^NT_k(λ), literally (2.7)–(2.14) of arXiv:math/0205002:
  principal variables 1 ≤ c ≤ C^max, auxiliary variables d bounded by each of the three lifts, and (L1)–(L3) with
  coefficients λ^{−2}, λ^{α−2}, λ^{α−1}, α = log₂ 3.
- `LamKL n = {λ ∈ [1, 2] | KLFeasible n λ}`.
- `KL_lambda_strictMono`: `StrictMono (fun n => sSup (LamKL n))`. Moreover, for every n the supremum belongs to
  `LamKL n` (attainment) and lies strictly between 1 and 2.
- `klFeasible_iff`: the literal program is equivalent to `Feasible n λ`, i.e. ∃ c > 0 with c ≤ F_λ(c), where F
  replaces each auxiliary variable by the minimum over its lifts.
- `tight`: at λ_k every feasible c satisfies c = F(c) (all principal inequalities tight).
- `unique`: such a c is unique up to a positive factor.
- `rho_eq`, `rho_strictMono`: at λ_k the mean loss of the solution is ρ = 3Σc̄/Σc = 3(λ_k − 1)/λ_k^α, and it
  is strictly increasing in k (so 1 − ρ_k strictly decreases).
- `exact_solution`: φ_m(y) = c_m λ_k^y satisfies Krasikov's difference inequalities (D1)–(D3) with equality for
  all real y. So no exponential rate above λ_k follows from I_k (K–L's belief after their Theorem 2.2).

## Index encoding and faithfulness lemmas

The principal class m = 3i + 2 (mod 3^k) has index i : Fin (3^(k−1)). These lemmas tie the encoding to K–L's
residue notation:
- `nu_is_times_four`: 3·ν(i) + 2 ≡ 4(3i + 2) (mod 3^k), i.e. the index of 4m.
- `class_mod9`: m mod 9 = 3(i mod 3) + 2.
- `auxA_is_KL` / `auxB_is_KL`: for the auxiliary index s with r = 3s + 2, 3r ≡ 4m − 2 (resp. 2m − 1) (mod 3^k), so
  r is K–L's (4m−2)/3 (resp. (2m−1)/3) mod 3^{k−1}.
- `lift_is_KL`: the three lifts of r are r + u·3^{k−1}, u = 0, 1, 2 (K–L's (2.12)–(2.14), with the 3^k → 3^{k−1}
  misprint corrected).

## Proof map (lemma ↔ note)

| note | Lean |
|---|---|
| Lemma 1 (monotone, superadditive, homogeneous, continuous) | `Fc_mono`, `Fc_superadd`, `Fc_smul`, `Fc_ge`, `continuousAt_F`, `tendsto_F` |
| Lemma 2 (×4 is one cycle) | `orderOf_four` (Mathlib `ZMod.orderOf_one_add_prime`), `nu_reach` |
| Lemma 3 (propagation of slack) | `strict_spread`, `exists_strict` |
| Lemma 4 (positivity) | `exists_pos` |
| Lemma 5 (openness) | `open_strict`, `exists_mem_above` |
| Lemma 6 (summation) | `sum_Fc`, `sum_cbar_le`, `topInv_of_sum_eq` |
| Lemma 7 (uniqueness) | `fixed_unique` |
| Lemma 8 (descent) | `descent_step`, `const_of_topInv`, `p_eq_one_of_const` |
| Lemma 9 (tiling) | `tile_ge`, `sum_tile_gain`, `exists_tile_strict` |
| Theorem (i)–(iii) | `lamk_mem`, `one_lt_lamk`, `lamk_lt_two`, `not_feasible_two`, `tight`, `unique`, `lamk_lt_succ` |
