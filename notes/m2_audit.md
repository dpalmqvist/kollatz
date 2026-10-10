# Audit: ProofAtlas "Positive Lower Density of Collatz Predecessors" (L. Mazur, Sept 2026)

Audit date: 2026-10-09/10 (night run, M4 Pro 64 GB). Everything was downloaded to and built in
`~/devel/mazur_dl/m2/` (outside the repo). No script shipped in the archives was executed; only `lake`/`lean`/
`leanchecker` from our own elan toolchain were run on the sources.

## 0. Verdict (short)

- **Statement: faithful.** The formal theorem is exactly Applegate–Lagarias "Conjecture A" in the strong
  every-cutoff form: for every a > 0 with 3 ∤ a there are real c > 0 and X0 such that for all X ≥ X0,
  c·X ≤ #{n : 1 ≤ n < X, C^t(n) = a for some t ≥ 0}, C the ordinary map (n/2, 3n+1). I re-stated it from
  scratch with only Mathlib notions (own Collatz map, `Finset.filter` count) and derived it from their theorem
  in Lean. That restatement depends only on `propext`, `Classical.choice` and `Quot.sound`.
- **No trust gap found.** All 388 project modules were rebuilt from the published sources. Our assembled files
  match their evidence manifest byte for byte. No `axiom`, `sorry`, `native_decide`, `implemented_by`, `extern`,
  `unsafe`, macros or meta code occur in the import closure. `#print axioms` gives the three standard axioms.
  `leanchecker` replays every project module through the kernel without error, and so does a `--fresh`
  replay of the whole environment, Mathlib included. What remains to trust: the Lean v4.30.0-rc2 kernel itself,
  the Mathlib definitions used in the statement (`Nat.count`, `Function.iterate`, `ℝ`), and the three
  standard axioms.
- **Method: genuine and non-trivial, nothing suspicious found.** The method uses a weighted inverse-orbit
  ("backward tree") mass from one fixed seed. The inputs are a formalized, explicit-constant version of Tao's
  fine-scale mixing for Syracuse random variables (Tao 2022, Props 1.14/1.17) and a seed-uniform variation bound.
  That bound comes from an elementary affine multiplicity estimate. Positivity comes from choosing the residue
  class of the seed first and the seed afterwards. I read the informal argument (both papers) and found it
  coherent. The evidence is the kernel check, not my reading.
- **Consequence:** unless the Lean kernel is unsound, π_a(x) ≥ c_a·x eventually for every a ≢ 0 (mod 3).
  This supersedes every x^γ lower bound, including ours (x^0.9251 at k = 22) and Mazur's own x^0.90.
  Their constants are ineffective (general a) or astronomically small (a = 1). Our explicit, uniform-in-a
  bound is a different kind of result and is not superseded as such (§8).

## 1. Provenance

| item | value |
|---|---|
| page | https://www.proofatlas.ai/formalizations/positive-lower-density-collatz-predecessors/ |
| source page | https://proofatlas.ai/sources/positive-lower-density-collatz-predecessors/ |
| manuscript | Lech Mazur, "Positive Lower Density of Collatz Predecessors", v1.0, 6 Sep 2026, 8 pp. `papers/positive-lower-density-collatz-predecessors/paper-v1.pdf`, sha256 `a848cf45…68883c` (matches release JSON) |
| companion source | `papers/positive-lower-density-collatz-predecessors/positive-lower-density-collatz-predecessors-v1.1-source.zip`, 55 103 B, sha256 `55ceb4df0cca17ae728dc65b30bf5077000e1b47f2dc322454eea9f637ac75b3` (**matches** the published value); package commit `c290ac229b379d2b51026d3e86140496870d6f39` |
| supporting source (preceding paper, slim v2.1) | `papers/positive-density-log-time-collatz/positive-density-log-time-collatz-v2.1-source.zip`, 914 975 B, sha256 `23f5cac4d66e696401144658752cf180a13ce70373a122f00693e1e1fe969c1f` (**matches**); commit `830b9d3f38f2a8da8cd921bf6a9310dd69336fd0` |
| main Lean file | `CollatzPredecessorDensity.lean`, sha256 `eb5aef15…d383f9` (matches) |
| evidence JSON | `sources/…/commits/c290ac22…/artifact.collatz.predecessors_positive_lower_density.v001.evidence.json` lists 388 files with sha256. **All 388 match our assembled tree**, and this set is exactly the set of modules Lake built. 61 800 non-empty lines, as on the page. |
| preceding paper | "Explicit Positive-Density Collatz Convergence in Logarithmic Time", v2.1 (13 pp., sha256 `a7e8a0ad…406a07`) |
| toolchain | `leanprover/lean4:v4.30.0-rc2` (commit 3dc1a088), Lake 5.0.0; Mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`. All 9 package revisions are identical to the earlier `collatz_predecessor_090` artifact, whose `.lake/packages` (official cache) was APFS-cloned. |
| credits / review | Lech Mazur is the author. OpenAI Codex is credited for "computation, exposition, formalization, and proof strategy". The evidence JSON says "accepted_result_recorded" with 4 internal ProofAtlas (AI) reviews. The release JSON's `reviews` list is empty and no human review is claimed. Their own check reused compiled dependencies and was not cold-rebuilt or run through LeanChecker. **We did both** (§6). |

Downloads are kept in `~/devel/mazur_dl/m2/dl/`: zips, both PDFs, release JSONs, evidence JSONs and HTML pages.
The assembled tree is `m2/assembled` (supporting tree + companion `.lean` files + companion lakefile/manifest).
No companion file overwrites a baseline file.

## 2. What is claimed (paper v1.0)

- **Thm 1.1:** for every positive integer a with 3 ∤ a there are c_a > 0 and X_a such that
  #P(a)∩[1,X) ≥ c_a X for every integer X ≥ X_a, where P(a) = {x ≥ 1 : C^t(x) = a for some t ≥ 0}.
  The claim needs neither "a reaches 1" nor any cycle classification. It gives no density limit and no
  uniformity in a.
- **Cor 1.2:** either every n reaches 1, or the non-convergent set has positive lower density. Hence upper
  density 1 of G = P(1) implies the Collatz conjecture.
- The T map (odd n ↦ (3n+1)/2) is covered via P(2a) ⊆ P_T(a) ⊆ P(a). I checked this by hand: the omitted even
  values are exactly the 3m+1 outputs. It is not formalized.
- The preceding paper (the supporting library) claims, for a = 1, an explicit c > 0 and X0 such that
  c·X ≤ #{1 ≤ n < X : n reaches 1 within (523/50)·ln n ordinary steps}.

## 3. Formal statement and every definition it rests on

Output of `#check` / `#print` in our build (`lake env lean audit/AuditMain.lean`):

```
@CollatzPredecessorDensity.predecessors_positive_lower_density : ∀ {a : ℕ},
  0 < a → ¬3 ∣ a → CollatzPredecessorDensity.HasPositiveLowerDensity (CollatzPredecessorDensity.predecessors a)

def CollatzPredecessorDensity.HasPositiveLowerDensity : Set ℕ → Prop :=
fun s => ∃ c, 0 < c ∧ ∃ X0, ∀ (X : ℕ), X0 ≤ X → c * ↑X ≤ ↑(CollatzPredecessorDensity.countBelow s X)
@[reducible] def CollatzPredecessorDensity.predecessors : ℕ → Set ℕ :=
fun a => Erdos1135.ND.PositiveDensity.ordinaryPredecessorSet a
@[reducible] def CollatzPredecessorDensity.countBelow : Set ℕ → ℕ → ℕ :=
fun s X => Erdos1135.Terras.natCount s X
def Erdos1135.ND.PositiveDensity.ordinaryPredecessorSet : ℕ → Set ℕ :=
fun a => {n | 0 < n ∧ Erdos1135.Reaches n a}
def Erdos1135.Reaches : ℕ → ℕ → Prop :=
fun a b => ∃ m, Erdos1135.collatzStep^[m] a = b
def Erdos1135.Terras.natCount : Set ℕ → ℕ → ℕ :=
fun s N => Nat.count (fun n => n ∈ s) N            -- with Classical.propDecidable
@[reducible] def Erdos1135.collatzStep : ℕ → ℕ :=
CollatzConjecture.collatzStep
def CollatzConjecture.collatzStep : ℕ → ℕ :=
fun n => if Even n then n / 2 else 3 * n + 1
def Nat.count : (p : ℕ → Prop) → [DecidablePred p] → ℕ → ℕ :=
fun p [DecidablePred p] n => List.countP (fun b => decide (p b)) (List.range n)
```

Checklist (task step 3):
- Map: the standard ordinary map on ℕ: even ↦ n/2, odd ↦ 3n+1. It is Mazur's own copy of the
  formal-conjectures definition, trimmed to this one `def`.
- "Reaches a": ∃ m ≥ 0 with C^m(n) = a (plain `Function.iterate`), so a ∈ P(a). Domain ℕ, n > 0 required.
- Count: `Nat.count p X` = #{n < X : p n}, so this is #{1 ≤ n < X}. Each integer is counted once. It is not a
  path or multiplicity count, and the bound is not taken at a larger cutoff.
- Quantifiers: ∃ c > 0 (real), ∃ X0, ∀ X ≥ X0. This is lower density at every cutoff, not a liminf along a
  subsequence. c and X0 may depend on a, and only on a.
- Hypotheses: 0 < a and ¬ 3 ∣ a. They are not vacuous (a = 1 qualifies) and are necessary (3 | a ⇒ P(a) = {2^j a}).
- Pitfalls checked: no ℕ subtraction in the statement, no division by a variable, no casts that trivialize
  (c·X ≤ count in ℝ with c > 0), no `Nat.find`/`choose` in the statement, no auxiliary object.

**Independent restatement** (`m2/audit/AuditMain.lean`, sha256 `8c16d3b6…`). It defines its own map and count and
proves equality with theirs (`C_eq`, `P_eq`):

```lean
def C (n : ℕ) : ℕ := if n % 2 = 0 then n / 2 else 3 * n + 1
noncomputable def P (a X : ℕ) : ℕ := by
  classical
  exact ((Finset.range X).filter (fun n => 1 ≤ n ∧ ∃ t : ℕ, C^[t] n = a)).card
theorem conjectureA (a : ℕ) (ha : 1 ≤ a) (h3 : a % 3 ≠ 0) :
    ∃ c : ℝ, 0 < c ∧ ∃ X0 : ℕ, ∀ X : ℕ, X0 ≤ X → c * (X : ℝ) ≤ (P a X : ℝ)
-- 'AuditM2.conjectureA' depends on axioms: [propext, Classical.choice, Quot.sound]
```

The base paper is handled the same way (`m2/audit/AuditBase.lean`): own map, own count of
n < X with 1 ≤ n and ∃ t, t ≤ (523/50)·ln n ∧ C^[t] n = 1. The result `AuditBase.base`
(∃ c > 0, X0, ∀ X ≥ X0, c·X ≤ count) also has only the three standard axioms.

**T map (this project's convention).** `m2/audit/AuditTMap.lean` defines T(n) = n/2 or (3n+1)/2. It proves
P(2a) ⊆ P_T(a) by strong induction (`T_reaches_of_C_reaches_double`) and derives `conjectureA_T`: for a ≥ 1,
a % 3 ≠ 0, ∃ c > 0, X0, ∀ X ≥ X0, c·X ≤ #{1 ≤ n < X : ∃ s, T^s(n) = a}. Axioms: the standard three.

The other two advertised theorems are faithful and are easy corollaries of the main one. They are checked in
`NonconvergenceDensityAmplification.lean`:
- `nonconvergence_positive_lower_density_of_counterexample`: (∃ n > 0, ¬Reaches n 1) → positive lower density of
  {n > 0 : ¬Reaches n 1}.
- `universal_reaches_one_of_arbitrarily_dense_convergence`: (∀ ε > 0, ∀ N, ∃ X ≥ N, X > 0 ∧ (1−ε)X ≤ #P(1)∩[1,X))
  → ∀ n > 0, Reaches n 1.

## 4. Axioms (exact output, our build)

```
'CollatzPredecessorDensity.predecessors_positive_lower_density' depends on axioms: [propext, Classical.choice, Quot.sound]
'CollatzPredecessorDensity.nonconvergence_positive_lower_density_of_counterexample' depends on axioms: [propext, Classical.choice, Quot.sound]
'CollatzPredecessorDensity.universal_reaches_one_of_arbitrarily_dense_convergence' depends on axioms: [propext, Classical.choice, Quot.sound]
'CollatzPositiveDensity.positive_density' depends on axioms: [propext, Classical.choice, Quot.sound]
'CollatzPositiveDensity.densityConstant_pos' depends on axioms: [propext, Classical.choice, Quot.sound]
'CollatzPositiveDensity.cutoff_pos' depends on axioms: [propext, Classical.choice, Quot.sound]
'AuditM2.conjectureA' depends on axioms: [propext, Classical.choice, Quot.sound]
'AuditBase.base' depends on axioms: [propext, Classical.choice, Quot.sound]
'AuditTMap.conjectureA_T' depends on axioms: [propext, Classical.choice, Quot.sound]
```

There is no `sorryAx`, no `Lean.ofReduceBool`/`trustCompiler` (so no `native_decide`), and no project axiom.
(As a control, a broken draft of my restatement did show `sorryAx`, so the check is live.)

## 5. Trust-relevant constructs (grep over all 401 `.lean` files of the assembled tree, `m2/audit/trustgrep.txt`)

Searched for: `axiom`, `sorry`, `admit`, `native_decide`, `decide +…`, `implemented_by`, `@[extern`, `@[csimp`,
`unsafe`, `opaque`, `ofReduceBool`, `trustCompiler`, `debug.*` (e.g. `debug.skipKernelTC`), `addDecl`,
`modifyEnv`, `setEnv`, `Kernel.`, `import Lean`, `#eval`, `run_cmd`/`run_elab`/`run_meta`, `initialize`, `IO.`,
`macro`, `elab`, `syntax`, `notation`.

| hit | where | matters? |
|---|---|---|
| `run_cmd`, `import Lean`, `IO.FS.writeFile "evidence/dependency-closure.json"` | `Verification/{ReleaseAudit,Dependencies,Axioms}.lean` | No. These are audit scripts outside the import closure of the theorem. They were not built or run by us. |
| `import Lean.Elab.Tactic.Omega` | 22 files | No. This is a standard tactic import. |
| `set_option maxHeartbeats` (1), `maxRecDepth` (2), `exponentiation.threshold` (1) | proof files | No. These only change resource limits. |
| `local instance … : Decidable … := Classical.propDecidable _` | `Geom2ShiftedWideSymmetricTerminalDepthShiftMarkedLoss.lean:14` | No. It is classical and inside proofs, and the final statement is re-derived independently. |
| `@[irreducible] def` constants (explicit numbers such as `2^80`) | ~25 | No. These are definitions, opaque to unfolding only. |

**Zero** occurrences of `axiom`, `sorry`, `admit`, `native_decide`, `implemented_by`, `extern`, `unsafe`,
`opaque`, `csimp`, `debug.`/`skipKernelTC`, `addDecl`/`modifyEnv`, `macro`/`elab`/`syntax`/`notation`.
`FormalConjectures/Wikipedia/CollatzConjecture.lean` was trimmed to the single `def collatzStep`; the upstream
`sorry`-stated conjecture is absent.

## 6. Build and kernel replay

| step | command | result |
|---|---|---|
| Mathlib up to date | `lake build --no-build Mathlib` | "All targets up-to-date (8312 jobs)" (cloned official cache) |
| shipped artifacts | `unzip -l` of both zips | no `.olean`/`.ilean`/`.lake` in either archive, so every project object below was compiled by us |
| project build | `LEAN_NUM_THREADS=8 lake build CollatzPredecessorDensity` | **success**, 3951 jobs, 388 project modules built from source (23:46:45 → 23:51:34, 289 s wall, 707 s user; each `lean` ≤ 3.6 GB). No errors and no `sorry` warnings; only linter or deprecation warnings (`push_neg`, unused simp args, …). |
| audit file | `lake env lean m2/audit/AuditMain.lean` | output in §3/§4, 0 errors (2.4 s) |
| base module | `lake build Erdos1135.ND.PositiveDensity.ExplicitUnitSeedPositiveDensityPair` + `lean -o` of `CollatzPositiveDensity.lean` + `AuditBase.lean` | success, see §4 |
| kernel replay | `lake env leanchecker -v Erdos1135 FormalConjectures CollatzPredecessorDensity` | **388/388 modules replayed, exit 0, no problem reported** (133 s, 33 GB peak with 8 threads) |
| kernel replay, base modules | `lake env leanchecker Erdos1135.ND.PositiveDensity CollatzPositiveDensity` | exit 0 |
| fresh replay (incl. Mathlib) | `lake env leanchecker -v --fresh CollatzPredecessorDensity` | **exit 0**: every constant of the environment (Mathlib + project) re-added to an empty kernel environment without error (23:59:57 → 00:05:19, 322 s, 4.1 GB) |

The non-fresh `leanchecker` re-adds every declaration of every project module to the kernel, starting from the
environment of its imports. It rules out "environment hacking" (declarations that entered the environment without
a kernel check). `--fresh` does the same for every constant, Mathlib included. Logs: `m2/build.log`,
`m2/leanchecker*.log`, `m2/audit_*.out`.

## 7. Proof architecture

Formal chain, from the top (file = module under `Erdos1135/ND/PositiveDensity/` unless stated):

1. `CollatzPredecessorDensity.predecessors_positive_lower_density` is a wrapper for
   `generalTarget_predecessors_positive_lower_density` (`GeneralTargetPositiveDensity.lean`, companion). It fixes
   b = 2^80 and C = `explicitSyracuseMixingCoefficient`, and outputs c = η/(32·r) and X0 = 32(H+1), where
   η = 3/(8·3^m) and m = 132·r·C + 1.
2. **Mixing input:** `explicitSyracuseMixing_six : Tao.syracFineScaleMixingAt 6 C`, i.e.
   Σ_y |P(Syrac_n = y) − 3^{m−n}·P(Syrac_n ≡ y mod 3^m)| ≤ C/m^6. This is Tao's Prop 1.14 with an explicit
   constant, derived (`ExplicitNumericalSyracuseMixing.lean`, `Tao/Section6/*`) from
   `explicitRenewal_numericalPrimitiveDecay`. That is Tao's Prop 1.17 (Fourier decay ≤ C·n^{−6409} at primitive
   frequencies), proved via the renewal-process argument of Tao §7 (`Tao/Fourier/*`, `Tao/Renewal/*`). Here
   `syracPMF` is Tao's Syrac(Z/3^n) with iid Geom(1/2) valuations (`Tao/Syracuse/Syrac.lean`). This
   formalization of Tao's mixing proposition is the bulk of the 61 800 lines and is itself a substantial result.
3. **Seed** (`GeneralTargetFrozenSeed.lean`, `GeneralTargetResidueCoverage.lean`, `GeneralTargetSeedNonreturn.lean`,
   companion):
   - At a fixed generation N, the backward "core mark" pulled back to residues mod 3^q has mean over units equal to
     ∏ p_j ≥ 255/256 (`exists_unit_rootCoreBackwardMark_ge_full_product`, `coreProbabilityProduct_ge_255_div_256`).
     So some unit residue y has mark ≥ 255/256.
   - In that class, take an odd seed r ≥ 16^b that reaches a and has no positive Syracuse return
     (`exists_large_nonreturning_predecessor_in_residue`). This uses R_k = ((3r0+1)·4^k − 1)/3 and
     v3(R_{k+h} − R_k) = v3(h), which runs through every residue mod 3^q.
   - Then `explicit_good_marked_margin_logarithmic_full` (baseline) gives a ρ-weighted terminal mass
     ≥ 255/256 − 1/16 − 1/8 − 1/8 = 175/256 ≥ 2/3 at every late generation and every admissible scale X.
4. **Remove the residue weight** (`fullGoodCoreTerminalMass_ge_of_square_budget_and_height_of_nonreturningSeed`,
   `GeneralTargetTerminalCensus.lean`). Split ρ_k = ρ_m∘π + (ρ_k − ρ_m∘π), use ρ_m ≤ (2/3)3^m, and bound the error
   by 33·r·⟨|ρ_k − ρ_m∘π|⟩_k via a residue-class census over *distinct* sources. Distinctness comes from the seed's
   no-return property. Result: unweighted mass ≥ η.
5. **Count** (`generalTarget_publicCount_from_mass`, `GeneralTargetPredecessorCount.lean`). For every Y ≥ 32(H+1),
   take X = Y/32:
   - some generation has all physical intervals containing X (`exists_unstopped_generation_all_intervals_contain`);
   - the sources lie in [X, 32X) (`fullTerminal_source_window`) and reach r, hence a;
   - each distinct source x carries weight ≤ r/x, so X·mass ≤ r·#sources.

   Hence natCount ≥ η/(32r)·Y.

**Where positivity comes from (the non-obvious step).** The quantity
Z_n(r) = Σ_{central inverse histories h of generation n} ω(h)·ρ_{k_n}(endpoint_h), with ω = 3^d 2^{−A},
is a near-martingale in n. The transfer identity ρ_{q+1} = Σ_a T_a ρ_q (Lemma 2.1 of the base paper) makes the
one-generation change equal to a pairing of the endpoint histogram H_{n,Q} with a mixing error of L¹ size
≲ k_n^{−6} + (1 − p_n).

The seed-uniform ingredient is the multiplicity bound (base paper (3.9)–(3.10)). Fix a pair (depth D, valuation
sum A). Then every endpoint R satisfies W·R + β = r with W = 3^D 2^{−A} and 0 ≤ β ≤ 2^{b0+1}, so the endpoints
lie in an interval of length 2^{b0+1}/W. Hence 3^Q·H_{n,Q}(y) ≤ #pairs·(2^{b0+1} + 16^{b0}(9/16)^{b_n}),
uniformly in y and in r. The number of pairs grows only like poly(n)·(1.0065)^n, while k_n^{−6} decays like
(200/201)^{6n}. So the increments are summable with a tail R_N that does not depend on r. One can therefore fix N
first, choose the residue class of r so that Z_N ≥ 255/256, and then pick r. This changes Tao's averaged (log-density)
mixing statement into a statement about one fixed seed. The ingredients are:
- backward rather than forward;
- L¹ mixing paired against a histogram bounded by Haar measure times C(n);
- geometric growth of scales b_{n+1} = b_n + ⌊b_n/100⌋, which beats C(n).

I found no step that proves more than it should. The method needs the backward tree to expand (4/3 > 1), units
mod 3, and Tao's 3-adic mixing, all of which are specific to 3x+1. It does not obviously transfer to 5x+1, where
the central first-crossing words would be large deviations.

**Caveats (not errors):**
- c(a) is ineffective for general a. Lemma 2.1 bounds the seed by the largest element of the cycle through the
  odd part of a *if* it is periodic, which cannot be decided. For a = 1 the base paper gives explicit but tower-sized
  constants.
- The informal Prop 3.1 of the companion paper is not a separate formal declaration. It does not need to be: the
  Lean proof goes directly through the baseline lemmas listed above.
- The work is AI-generated (Codex) with no human referee. Formal verification makes that irrelevant for
  correctness of the Lean statement. It does not make the expository paper correct line by line.

## 8. Consequences for this project

- Unless Lean's kernel is unsound, Conjecture A is now a theorem (ineffective constants): π_a(x) ≥ c_a x for
  x ≥ X0(a) and every a ≢ 0 mod 3, for the T map as well (formalized here as `AuditTMap.conjectureA_T`). Exponent "records" x^γ, γ < 1 (K–L 0.84,
  Mazur 0.90/0.901, our 0.9203 Lean-free certificate and 0.909/0.914 Lean-checked) are superseded as statements
  about π_a.
- Not superseded:
  - explicit, uniform-in-a bounds with small cutoffs, e.g. our certified π_a(x) ≥ 0.865·(x/a)^{0.7991} for x ≥ 64a (corrected 2026-10-10 to the rigorous 0.8435 for x ≥ 16a, and improved to 0.7146·(x/a)^{0.848} for x ≥ 2^{6.25} a, see RESULTS.md);
  - the structural question λ_k → 2 (ρ_k → 1) for the K–L linear program, which concerns that method, not π_a;
  - effective or explicit c_a for general a, a natural-density limit, and density one (the last would imply
    Collatz by their Cor 1.2).
- CLAUDE.md "Omvärld 2026" currently calls Mazur's September positive-density claim "obekräftat, var skeptisk".
  After this audit it should read: formally verified (Lean, standard axioms; our cold rebuild and leanchecker,
  2026-10-10), mathematically unrefereed.

## 9. Reproduce

```sh
cd ~/devel/mazur_dl/m2/assembled
export PATH="$HOME/.elan/bin:$PATH"
LEAN_NUM_THREADS=8 lake build CollatzPredecessorDensity          # ~5 min, Mathlib from cache
lake env lean ../audit/AuditMain.lean                           # statements, definitions, axioms
lake env lean ../audit/AuditTMap.lean                           # T-map version
lake env leanchecker -v Erdos1135 FormalConjectures CollatzPredecessorDensity   # ~2 min, ~33 GB
lake env leanchecker -v --fresh CollatzPredecessorDensity        # whole environment incl. Mathlib
```

A stronger independent check would be an external kernel (lean4lean or nanoda) on an `.olean` export. That is not
installed here and was not done.


## Addendum 2026-10-10 (main session): Lean kernel bug #14576

Found by the density-one literature survey (`reports/density_one_gap.md` §5.1). Issue leanprover/lean4#14576
(28 Jul 2026, fixed by PR #14577): the kernel accepted an inductive declaration whose constructor type applies a
projection of one structure to a value of another. This allows an axiom-free proof of False, invisible to
`#print axioms`. The exploit needs a **metaprogram that adds raw declarations with `addDecl`**; surface syntax
cannot produce such a projection.

M2 was built and replayed with v4.30.0-rc2, which predates the fix, and `leanchecker` uses the same kernel. However,
§5's trust grep found **no** `addDecl`, `modifyEnv`, `elab`, `macro`, `syntax`, `run_cmd` or `import Lean` meta code
in the theorem's import closure (only in `Verification/` audit files outside it). So the bug cannot have been used.

**Independent kernel replay: done (2026-10-10, 02:37).**
- lean4export was built at its tag `v4.30.0-rc2`, in `~/devel/mazur_dl/tools/lean4export_v430`.
- It exported the closure of `predecessors_positive_lower_density`,
  `nonconvergence_positive_lower_density_of_counterexample` and `universal_reaches_one_of_arbitrarily_dense_convergence`
  from our build (`m2/m2_export.ndjson`, 298 MB, format 3.1.0). The export holds 31 938 theorems, 9 329 definitions,
  823 inductives, 28 opaques and exactly 3 axioms; 5 527 names lie in the project namespaces.
- That export was replayed in the independent Rust kernel **nanoda 0.4.17**, with permitted axioms = propext,
  Classical.choice, Quot.sound and unpermitted axioms a hard error. Result: **"Checked 43862 declarations with no
  errors"** (15 s, 0.55 GB).
- nanoda's pretty-printer shows the statement exactly as in §3.

So the result no longer depends on the pre-fix Lean kernel. The exporter pipeline was first validated on our own
`lean_formal/KLMonotone` (v4.30 build: 29 202 declarations, no errors). Config and log: `m2/nanoda_m2.json`,
`m2/nanoda_m2.log`.
