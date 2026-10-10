# Audit: "no Collatz m-cycle with m ≤ 101" (justinalick/collatz-m-cycles-101-lean)

Audit date: 2026-10-10 (night run, M4 Pro 64 GB). Everything was downloaded to and built in
`~/devel/mazur_dl/m102/` (outside the repo). No shell or Python script from the audited repository was run.
Only our own elan toolchain was used: `lake`, `lean`, `leanchecker`, `leanexport` and `nanoda_bin`. The
Python cross-checks below are our own code (`mcycles.py` plus throw-away scripts in the session scratchpad).

## 0. Verdict (short)

- **(a) Formally established, conditional on the two stated hypotheses: yes.**
  - `Collatz.no_101_cycle_2_71` builds from source with Mathlib's official cache.
  - It depends only on `propext`, `Classical.choice` and `Quot.sound`.
  - The repository contains no `sorry`, `axiom`, `native_decide`, `implemented_by`, `extern` or `unsafe`, and
    no meta code.
  - `leanchecker` replays every module through the kernel: 49/49 modules pass, with no problem reported.
  - An export of the whole dependency closure is accepted by the independent Rust kernel `nanoda`:
    30 298 declarations, no errors, only the standard axioms permitted (hard error otherwise).
  - I restated the theorem with my own definitions (`AuditM102.no_small_m_cycle_C`):
    - the ordinary map C in the verification hypothesis;
    - local minima counted over the minimal period;
    - Rhin's bound in its raw form p^(−13.3) ≤ |p log 2 − K log 3|.

    I derived the restatement from their theorem in Lean, with the same three axioms. That derivation
    includes a Lean proof of Simons–de Weger's Lemma 12 (their `RhinBound`) from the raw form.
- **(b) The hypotheses are the standard ones of the field.**
  - "Every n ≤ 2^71 reaches 1" is Bařina's published verification (J. Supercomput. 81 (2025), art. 810).
  - `RhinBound` is Simons–de Weger's Lemma 12 verbatim (Acta Arith. 117 (2005); v1.44 has the same
    numbering), restricted to cycles. SdW and Hercher's m ≤ 91 rest on the same two inputs; Hercher uses
    695·2^60 instead of 2^71.
  - The constant 0.46057 is rounded in the safe direction. Our note `mcycles_2_71.md` §6 had this
    backwards; see §3.
  - Both inputs are trusted, not re-verified: Bařina's computation, and Rhin's 1987 proposition, whose
    paper I could not obtain.
- **(c) The new mathematics is elementary and, as far as I can see, sound.**
  - The "two-rise bound" is an exact 2-adic computation. I recomputed it independently, and the
    kernel-checked bounds equal the true maxima.
  - The "chain argument" bounds all local minima of a hypothetical cycle of a given shape (K, K+L), starting
    from its least element.
  - It excludes all 120 listed shapes. These include every shape our own `mcycles.py survivors` leaves.
  - The worst margin is Σ x_t/K = 0.798, at m = 101, K = 77 692 117 359 936 589 403.
  - Without the two-rise step none of the 111 chain-excluded shapes would be excluded: the ratio is ≥ 1.005
    for all of them.
- **Caveats.**
  - The work is unrefereed and AI-assisted: the commit author is "Claude", and the README credits Claude
    Code. There is no human-readable paper yet.
  - The toolchain is a release candidate (v4.35.0-rc3).
  - The result is conditional; that is the same standard as SdW and Hercher.
  - It is a modest extension: m = 101 is where the compute budget of the two-rise grid ends, not a structural
    wall (§8).
  - It says nothing about divergent orbits, about m ≥ 102, or about the minimal cycle length (§9).

## 1. Provenance

| item | value |
|---|---|
| repository | https://github.com/justinalick/collatz-m-cycles-101-lean (Apache 2.0) |
| `main` | single commit `d18959450f9acb5c0fa8c54310bc799a636d7db4`, 2026-09-28 08:09:51 UTC, author and committer "Claude <noreply@anthropic.com>" |
| README credit | "Author: Justin Alick. The proofs, the Lean code and this repository were prepared with an AI coding assistant (Claude Code) under the author's direction." A paper is "in preparation". |
| other branch | `claude/repo-review-m-constraint-ot1dqv` (`db160011…`, 2026-09-28 10:25 UTC). It adds a CI `leanchecker` step, an AI-written `REVIEW.md` and four Python review scripts. It is not merged; I read it but did not run its scripts (§7.5). |
| contents (`main`) | 68 tracked files: 49 modules under `Collatz/` plus the root `Collatz.lean`, `scripts/{Statement,AxiomAudit}.lean`, `research/scripts/*.py` (generators; not run), README, LICENSE and CI. 9 211 non-empty Lean lines. |
| toolchain | `leanprover/lean4:v4.35.0-rc3` (commit `470d5ce1`), Lake 5.0.0. Installed with our elan. |
| Mathlib | `c55e6e786f49471c72fbddbec5415808896aec1e`. `git ls-remote` shows this is exactly the official tag `v4.35.0-rc3`. The other manifest entries are the standard Mathlib dependencies (batteries, aesop, Qq, proofwidgets, plausible, LeanSearchClient, importGraph, Cli). |
| sha256 | `MCycle101.lean` dc25cb2a…f532d, `Defs.lean` d899f999…60db, `Statements.lean` bb95e4ba…bf01, `HercherRhin.lean` 7aa90267…980d, `TwoRiseCheck.lean` 3941dcc0…017d, `MCycleChain.lean` 1aaa3cb8…3e, `MCycleWalk.lean` f5147f3a…066c, `lakefile.toml` d7f0b538…f5c0, `lake-manifest.json` e95b7a33…e275 |

**Safety review before building.**
- `lakefile.toml` is declarative: package `collatz`, one `require mathlib` at `v4.35.0-rc3`, one
  `lean_lib Collatz` and some options. It defines no scripts or targets.
- The grep over all `.lean` files (§5) found no `run_cmd`, `#eval`, `initialize`, `IO.`, `macro`, `elab`,
  `syntax`, `notation`, `@[extern]`, `implemented_by`, `unsafe`, `axiom`, `sorry`, `native_decide`, `debug.`,
  `addDecl` or `modifyEnv` in the library.
- The library imports no `Lean` meta modules. `TwoRiseCheck.lean` imports nothing at all; the other modules
  import Mathlib.
- Only `scripts/AxiomAudit.lean` defines an `elab` command. It iterates over the environment and calls
  `collectAxioms`, which is read-only. I used my own audit file instead.

The safety review passed, so I built.

## 2. Statement and every definition it rests on

`Collatz/MCycle101.lean`. The output below is from `#check`/`#print` in our build.

```
Collatz.no_101_cycle_2_71 : (∀ (n : ℕ), 0 < n → n ≤ 2 ^ 71 → Collatz.Reaches Collatz.T n 1) →
  Collatz.RhinBound → ∀ (x p : ℕ), 0 < x → 0 < p → Collatz.T^[p] x = x → x ≠ 1 → x ≠ 2 → 102 ≤ Collatz.numLocalMin x p
def Collatz.T : ℕ → ℕ := fun n => if n % 2 = 0 then n / 2 else (3 * n + 1) / 2
def Collatz.Reaches : (ℕ → ℕ) → ℕ → ℕ → Prop := fun f n m => ∃ k, f^[k] n = m
def Collatz.numLocalMin : ℕ → ℕ → ℕ :=
  fun x p => {i ∈ Finset.range p | Collatz.T^[i] x % 2 = 1 ∧ Collatz.T^[i + p - 1] x % 2 = 0}.card
def Collatz.RhinBound : Prop :=
  ∀ (x p : ℕ), 0 < x → 0 < p → Collatz.T^[p] x = x → x ≠ 1 → x ≠ 2 → 1 ≤ Collatz.oddCount Collatz.T x p →
    Real.exp (-(133 / 10 * (46057 / 100000 + Real.log ↑(Collatz.oddCount Collatz.T x p)))) <
      ↑p * Real.log 2 - ↑(Collatz.oddCount Collatz.T x p) * Real.log 3
def Collatz.oddCount (f) (n) : ℕ → ℕ   -- oddCount f n 0 = 0, oddCount f n (k+1) = oddCount f n k + f^[k] n % 2
```

**Checklist.**

- *Map.* T is the usual shortcut map on ℕ, so (3n+1)/2 is exact for odd n. T-cycles are exactly C-cycles.
- *m-cycle.* `numLocalMin x p` counts the indices i < p for which T^i(x) is odd and its cyclic predecessor
  T^(i+p−1)(x) = T^(i−1)(x) is even. A cycle splits into m blocks of "k_i odd steps, then l_i ≥ 1 even
  steps". The odd elements with an even predecessor are exactly the starts of these blocks, which are the
  local minima of SdW §1.2 and Hercher Def. 5–6. So the count is the m of an m-cycle.
- *Period.* p is any period. For p = j·p₀ the count is j·m, so "for all p" is equivalent to "for the least
  period".
- *Trivial cycle.* x ≠ 1, 2 excludes exactly the cycle 1 → 2 → 1, and x > 0 excludes 0. Only positive cycles
  are covered; the negative cycles −1, −5, −17 are outside the scope, as in the literature.
- *Hypotheses.* `hX` and `hR` are parameters, not `axiom`s (§4). Neither makes the theorem trivial:
  - Both follow from the Collatz conjecture, so they are jointly satisfiable.
  - `RhinBound` only constrains hypothetical cycles: it is a lower bound on Λ for each one.
  - `hX` is a finite statement, true by Bařina's computation.
  - A caution, from the side-branch review: the trivial cycle has `numLocalMin 1 182 = 91`. So any statement
    about "all cycles with 91 minima" that drops x ≠ 1, 2 is false. The main theorem has the exclusions.
    Some superseded lemmas in `HercherBootstrap.lean` with such hypotheses exist, but they are not on the
    proof path (all axioms are standard, and `hercher_theorem` takes only the two hypotheses).
- *Pitfalls.* No ℕ subtraction problem: p ≥ 1, so i + p − 1 ≥ i. The statement uses no casts. `RhinBound` is
  in ℝ with an explicit `Real.exp`/`Real.log`.

**Independent restatement** (`~/devel/mazur_dl/m102/audit/AuditM102.lean`, sha256 3fdbab08…; output in
`m102/logs/audit_main.out`). It uses only my own definitions and proves the bridges `Tm_eq`, `oddElems_eq`
and `localMinCount_eq`:

```lean
def Cm (n : ℕ) : ℕ := if n % 2 = 0 then n / 2 else 3 * n + 1          -- ordinary map, as in Bařina
def Tm (n : ℕ) : ℕ := if n % 2 = 0 then n / 2 else (3 * n + 1) / 2
def oddElems (x p : ℕ) : ℕ := ((range p).filter (fun i => Tm^[i] x % 2 = 1)).card
noncomputable def localMinCount (x : ℕ) : ℕ :=        -- over ONE minimal period P, predecessor (i+P-1) mod P
  ((range (minimalPeriod Tm x)).filter (fun i => Tm^[i] x % 2 = 1 ∧
      Tm^[(i + minimalPeriod Tm x - 1) % minimalPeriod Tm x] x % 2 = 0)).card
def VerifiedToC (B : ℕ) : Prop := ∀ n, 1 ≤ n → n ≤ B → ∃ k, Cm^[k] n = 1
def RhinForCycles : Prop :=   -- Rhin with u₀ = 0, u₁ = K+L = p, u₂ = −K, H = p (how SdW apply it)
  ∀ x p, 0 < x → 0 < p → Tm^[p] x = x → x ≠ 1 → x ≠ 2 → 1 ≤ oddElems x p →
    (p : ℝ) ^ (-(133/10 : ℝ)) ≤ |(p : ℝ) * Real.log 2 - (oddElems x p : ℝ) * Real.log 3|
theorem no_small_m_cycle_C (hX : VerifiedToC (2 ^ 71)) (hR : RhinForCycles) :
    ∀ x p, 0 < x → 0 < p → Tm^[p] x = x → x ≠ 1 → x ≠ 2 → 102 ≤ localMinCount x
-- 'AuditM102.no_small_m_cycle_C' depends on axioms: [propext, Classical.choice, Quot.sound]
```

Two lemmas carry the content of the restatement:

- `reaches_T_of_reaches_C` turns the C-version of the verification into the T-version.
- `rhinBound_of_raw` derives their `RhinBound` from `RhinForCycles` plus the verification. The proof uses
  their `cycle_bounds_of_verified`, 2^p ≤ (3 + 1/(2^71+1))^K, to get p/K ≤ 1.58497. It then uses
  log 1.58497 < 0.46057, proved via 3 log c ≤ 2 log 2 + c³/4 − 1, to get
  p^(−13.3) > exp(−13.3(0.46057 + log K)).

The sanity checks `numLocalMin 1 2 = 1` and `numLocalMin 1 4 = 2` hold by `decide`.

## 3. The two hypotheses against the literature

**`hX` (2^71).**
- Source: D. Bařina, "Improved verification limit for the convergence of the Collatz conjecture",
  J. Supercomput. 81 (2025), art. 810. This project records 2^71 as the published milestone (2025-01-15).
- The computation is for C and covers n < 2^71. n = 2^71 is a power of 2, so ≤ versus < does not matter.
- The C/T gap is closed in Lean by `AuditM102.verifiedTo_of_C`.
- The computation itself is trusted, as it is for SdW (5·2^60) and Hercher (695·2^60).

**`RhinBound` (13.3, 0.46057).**
- This is SdW Lemma 12 (v1.44 p. 10, the same number in Acta Arith. 117 (2005)), restricted to cycles:
  Λ > e^(−13.3(0.46057 + log K)).
- SdW's proof applies "the Proposition on p. 160 of [Rhin 1987] with u₀ = 0, H = u₁ = K+L, u₂ = −K" together
  with their Lemma 8, δK < K+L < 1.000001·δK.
- The rounding is safe: log(1.000001·δ) = 0.4605617 < 0.46057. So (K+L)^(−13.3) > e^(−13.3(0.46057+log K)),
  and Lemma 12 follows from Rhin's bound with room to spare (a factor 1.0001).
- **Correction to our `notes/mcycles_2_71.md` §6.** It says "0.46057 is marginally below log δ = 0.4605749".
  That is wrong: log δ = 0.4605607, so 0.46057 lies above log δ. Not edited here.
- In Lean, `AuditM102.rhinBound_of_raw` derives `RhinBound` from the raw form p^(−13.3) ≤ |Λ| for the
  (p, K) of a cycle, plus `hX`.
- The side-branch review (§7.5) shows that the K-form even follows for all integer pairs with 2^p > 3^K
  (two cases). I did not formalise that version.

What I could not check:
- Rhin's paper itself (Progr. Math. 71, Birkhäuser 1987, pp. 155–164; not online).
- In particular, whether the Proposition has a height threshold H ≥ H₀. It would be moot here, since every
  nontrivial cycle has p > 10^11 by the same verification. Its form is taken from SdW's description.

Where the hypothesis enters:
- `RhinBound` is used only to get the ceiling K < K_f(m). The ceiling comes from SdW Lemma 7 (here Hercher's
  Theorem 21 with m₂ = m) set against Lemma 12 (`rhinOK`, `K_lt_of_rhinOK`).
- The margin is large. For m = 92 the deciding rational inequality reads 680.566 < 680.931 in log units
  (V = 987, c = 62, k = 8; margin 0.365). Changing the constant by 10^−5 changes the left side by about 10^−4.
- **Repository vs literature.** Their ceilings `Kceil` are about K1(m) (4.26e21 at m = 92). SdW's tighter K2
  would need the continued-fraction champion table; they avoid it at the price of more shapes.

## 4. Axioms (exact output, our build)

```
'Collatz.no_101_cycle_2_71' depends on axioms: [propext, Classical.choice, Quot.sound]
'Collatz.hercher_theorem_2_71' depends on axioms: [propext, Classical.choice, Quot.sound]
'Collatz.hercher_theorem' depends on axioms: [propext, Classical.choice, Quot.sound]
'Collatz.mOK_sound' depends on axioms: [propext, Classical.choice, Quot.sound]
'Collatz.twoRiseBound_of_allPairs' depends on axioms: [propext, Classical.choice, Quot.sound]
'Collatz.TwoRise.allPairs14558' depends on axioms: [propext, Classical.choice, Quot.sound]
'Collatz.data101_ok' depends on axioms: [propext, Classical.choice, Quot.sound]
'AuditM102.no_small_m_cycle' depends on axioms: [propext, Classical.choice, Quot.sound]
'AuditM102.no_small_m_cycle_C' depends on axioms: [propext, Classical.choice, Quot.sound]
'AuditM102.rhinBound_of_raw' depends on axioms: [propext, Classical.choice, Quot.sound]
```

- There is no `sorryAx`, so no `sorry`. A broken draft of my file did show `sorryAx`, so the check is live.
- There is no `Lean.ofReduceBool` or `trustCompiler`, so no `native_decide`.
- The two hypotheses are parameters, not axioms. Nothing else is assumed.

## 5. Trust-relevant constructs (grep over all 52 `.lean` files)

| hit | where | matters? |
|---|---|---|
| `decide +kernel` (431×) | the two-rise data modules (`MCycleTwoRise*.lean`), the per-m certificates (`MCycle9x.lean`, `MCycle101Data.lean`), `HercherAll/Bootstrap/Chain91/No91/Rhin`, `LogTwoThreeBounds`, `Terras`, `Steiner`, `SharpCycleBound` | It moves the trust onto kernel evaluation, including GMP-accelerated `Nat` arithmetic. It is not an axiom; the kernel re-checks it on replay (§6). |
| `set_option Elab.async false` (7×) | `MCycleTwoRise*.lean` | No (memory/scheduling only). |
| `set_option maxRecDepth 100000` (2×) | `Terras.lean` | No (resource limit). |
| `elab "#audit_axioms"`, `import Lean.Util.CollectAxioms` | `scripts/AxiomAudit.lean` | No. It is outside the library, read-only, and I did not run it. |

Zero occurrences in the library (code, not docstrings; `Checker.lean` mentions `native_decide` only in a docstring saying it is not used): `axiom`, `sorry`, `admit`, `native_decide`, `implemented_by`, `@[extern]`,
`unsafe`, `opaque`, `@[csimp]`, `debug.`, `addDecl`, `modifyEnv`, `run_cmd`, `#eval`, `initialize`, `IO.`,
`import Lean`, `macro`, `elab`, `syntax` and `notation`. `TwoRiseCheck.lean`, the two-rise checker and its
soundness proof, uses only core Lean: plain `Nat.rec` loops and GMP primitives. It deliberately avoids
`Nat.log2`, which the kernel does not accelerate.

## 6. Build and kernel replay

| step | command | result |
|---|---|---|
| Mathlib | `lake exe cache get` | 8 943 files from the official cache in 95 s. `lake build --no-build Mathlib`: up to date. |
| project build | `lake build Collatz.HercherAll Collatz.TwoRiseCheck`, then `lake build` | **success**. 3 561 jobs; all 49 `Collatz/*` modules compiled by us from source in 83 s + 100 s wall. No errors and no `sorry` warnings; only lint and deprecation warnings (`push_neg`, `if_pos`/`if_neg`, unused variables). Peak 21 GB in total and 8.6 GB in one process. The two-rise modules take 28–45 s each and `MCycle101Data` 45 s. |
| audit file | `lake env lean ../audit/AuditM102.lean` | 0 errors. Output in §2 and §4. |
| kernel replay | `lake env leanchecker -v <module>`, one module per process, for all 49 `Collatz.*` modules (`audit/replay_seq.sh`) | **49/49 OK**, 0 problems. 6–75 s per module (the two-rise modules 41–67 s, `MCycle101Data` 75 s); ≤ 12.7 GB. This re-adds every declaration, including all 431 `decide +kernel` evaluations, to the kernel from the environment of its imports. The root `Collatz.lean` (only `import Collatz.MCycle101`, no declarations) was skipped on purpose: `leanchecker Collatz` treats the name as a prefix and replays all 49 modules in parallel. |
| independent kernel | `leanexport AuditM102 -- AuditM102.no_small_m_cycle Collatz.no_101_cycle_2_71` (171 MB, 3.19 M lines; my restatement plus their theorem with their whole closure, Mathlib included), then `nanoda_bin` 0.4.17 (Rust; `nat_extension` on, permitted axioms = the standard three, unpermitted-axiom hard error) | **"Checked 30 298 declarations with no errors"**, exit 0, 216 s, 11.2 GB RSS. Its pretty-printer output (`pp_declars`) confirms that the checked declarations have exactly the statements quoted in §2: `Collatz.no_101_cycle_2_71`, `RhinBound`, `numLocalMin`, `T`, `AuditM102.no_small_m_cycle_C`, `RhinForCycles`, `VerifiedToC`, `localMinCount`, `Cm`, `Tm` and `oddElems`. A first export without the C version also passed: 30 290 declarations, 220 s. |

`lean4lean` ships with the toolchain, but it rejected the 4.35 oleans ("incompatible header"), so it was not
used.

## 7. Proof architecture and the new mathematics

Notation: T, δ = log₂ 3, K = number of odd elements, p = K + L. The quantity
Λ = p·log 2 − K·log 3 > 0 for any nontrivial cycle.

### 7.1 Hercher's part (m ≤ 91)

`Collatz/Hercher*.lean`, `FareyCertificate.lean`, `LogTwoThreeBounds.lean`.
- It formalises Theorem 16, Lemma 8, Lemma 20 and Remark 7, and Theorem 21 in a "vertex-free" form and a
  "two-element" form. These are proved directly, not via the corrigendum's convex-vertex argument; the
  statements and bounds are the same.
- It formalises Lemma 22 (Farey) and the Theorem 23 bootstrap, for each m ≤ 91 (`hercherData_ok`, kernel).
- The ceiling comes from `RhinBound` (`rhinOK`), not from SdW's tables.
- δ is enclosed in [deltaLo, deltaHi] of width 10^−50, proved from Mathlib's series bound for log.
- `hercher_theorem` takes X₀ = 695·2^60. `hercher_theorem_2_71` feeds it from `hX`.
- This matches our own re-run (`mcycles.py validate`).

### 7.2 Shapes left by the bootstrap (m = 92…101)

`MCycleWalk.lean`.
- For each m, the bootstrap at the floor X₀ = 2^71 + 1 runs to K ≥ K_s (`chainOKX`).
- A Farey walk down the Stern–Brocot tree (`walk`, proved complete by `walk_sound`) then lists every (K, p)
  with K_s ≤ K < Kceil whose ratio p/K lies in (δ, δ + ε(K)). Here ε(K) comes from a "stair" of Theorem 21
  bounds valid for K ≥ K_p. The listing includes non-primitive multiples j·(K', p') (`mults`).
- `mOK_sound` turns "every listed shape has an accepted certificate" into `False`.
- Walk sizes: 43, 67, 94, 126, 178, 841, 1308, 2505, 4058 and 7629 nodes for m = 92…101.
- Listed shapes: 1, 2, 3, 5, 6, 10, 11, 19, 24 and 39.

**Cross-check against our `mcycles.py survivors '2^71' m`** (X0 = 2^71, Hercher's inequality at its own K,
SdW ceiling K2):
- Our survivors are 1, 2, 3, 4, 6, 7, 9, 11, 18 and 29 shapes for m = 92…101.
- **For every m our list is a subset of theirs.** The script parses their Lean data as text and compares
  (K, p) exactly.
- Their extra shapes come from three sources:
  - a larger ceiling (≈ K1 instead of K2), which gives more multiples j·s₀;
  - a more conservative ε, which gives the shape s₁ = 77 692 117 359 936 589 403 as a survivor already at
    m = 97–100;
  - a few other fractions, e.g. 449 058 448 471 548 615 631 / 283 324 336 233 335 185 659 and
    12 587 715 785 705 330 118 969 / 7 941 964 418 702 608 664 581.
- Almost all surviving shapes are multiples j·s₀ of the single fraction
  s₀ = 325 919 355 854 421 968 365 / 205 632 218 873 398 596 256, together with s₁ and its multiples.

### 7.3 The two-rise bound (new)

`TwoRiseCheck.lean`, `MCycleTwoRise*.lean`, `MCycleGrid{Lo,Hi}.lean`.

**Statement.** `TwoRiseBound N B`: for every odd n < 2^N, orun(n) + orun(nextMin n) ≤ B. In words, the first
two ascents together are at most B long.

**Mechanism.**
- Write n + 1 = 2^(k₀)·a with a odd and a < 2^(N−k₀). The block identity is
  3^(k₀)·a + 2^ℓ = 2^(ℓ+k₁)·a' + 1.
- This forces a ≡ 3^(−k₀)·(1 − 2^ℓ) (mod 2^(ℓ+k₁)).
- So k₀ + k₁ > B would require a run of zero bits, from bit N − k₀ upward, in that 2-adic number.
- The checker refutes this for every k₀ ≤ N and every ℓ ≥ 1:
  - large ℓ are settled automatically;
  - middle ℓ get a direct test;
  - the small-ℓ range is handled by a bit-parallel window search with a "borrow" case.
- Soundness is proved in Lean (`kCore_sound` → `rangeOK_sound` → `AllPairs` → `twoRiseBound_of_allPairs`).
  The kernel evaluates the checker for 97 grid values N = 70, 72, …, 23 446.

**My independent check** (own 2-adic enumeration):
- First validated against brute force over all odd n < 2^N for N = 3…16.
- The true maximum M(N) equals their B exactly at every grid point I tested:
  - M(70) = 76;
  - M(72…77) = 84;
  - M(85) = 91, M(103) = 107, M(114) = 120, M(196) = 206, M(501) = 512, M(799) = 805.
- Each value has an explicit witness checked by direct iteration. Example: n = 3 603 960 565 806 965 719 039
  < 2^72 has k₀ = 56 and k₁ = 28.
- So the bounds are sharp and not vacuous.
- The side-branch review reports the same equality for all 84 grid points with N ≤ 6 792.

**Paper check.** The derivation is elementary and correct. In general, M(N) − N is a question about long zero
runs in 2-adic expansions of 3^(−k)·(1 − 2^ℓ), and it has no known closed bound. That is why it is computed
grid point by grid point.

### 7.4 The chain (new)

`MCycleSteps.lean`, `MCycleChain.lean`.

Fix a listed shape (K, p). Label the local minima n₀, n₁, … cyclically from the least element n₀ (which is a
local minimum, `exists_least_rotation`), and put x_t = log₂(n_t + 1). Then:

1. x_(t+1) ≤ δ·x_t (Hercher Lemma 20).
2. Two-step bound (`TwoRise.two_step_core`): 4·2^(k+k')·(n''+1) ≤ 3^(k+k')·(n+4). Hence
   x_(t+2) ≤ x_t + (δ−1)(k_t + k_(t+1)) − 2 + 6/(n_t+1).
   With x_t ≤ N and `TwoRiseBound N B` this gives x_(t+2) ≤ x_t + (δ−1)·B − 2 + 2^−20. I re-derived the
   integer inequality by hand; it needs only ℓ ≥ 1.
3. K ≤ Σ_(t<m) x_t, since each ascent satisfies k_t ≤ log₂(n_t+1) (Hercher Lemma 8).
4. The least element: Theorem 21 (two-element form) with X₀ = n₀ itself gives
   Λ < (m−m₂)/n₀ + 1/(2^N−1) + (m₂−1)/(2^M−1). Λ is known exactly for the shape. Hence n₀ < U_b
   (`least_lt_Ub`); if U_b ≤ 2^71 + 1 the shape is excluded by the floor alone.
5. An integer chain Y_t, in units of 2^−20 and rounded up throughout, dominates x_t (`chain_sound`). If
   Σ Y_t < K·2^20 there is a contradiction (`shape_false`).

**My real-arithmetic re-evaluation of all 120 certificates.** This is my own code, following the mathematics
rather than the Lean encoding. I used the exact Λ (80 digits), checked Theorem 21's premises N ≤ v and M ≤ τ,
and used the kernel-checked grid.
- **All pass.**
- 9 shapes fall to the floor alone (n₀ < 2^71 + 1).
- For the other 111 shapes, x₀ lies between 71.0 and 76.7: the least element is at most about 2^77.
- The worst ratio is Σx_t/K = **0.798**, at (m, K) = (101, 77 692 117 359 936 589 403), which is the
  README's "about 80 %".
- With only step 1, i.e. the classical SdW Lemma 7 chain, every one of the 111 shapes gives Σ ≥ 1.005·K, so
  none would be excluded. **The two-rise bound is what does the work.**

### 7.5 The side-branch self-review

`REVIEW.md` on `claude/repo-review-m-constraint-ot1dqv` is AI-written, at the owner's request. Its conclusions
coincide with mine:
- the same statement reading;
- a CI `leanchecker` replay;
- M(N) = B for 84 grid points;
- the checkers transcribed into Python, with a worst case of 0.798;
- the recommendation to restate Rhin in raw form and add C ↔ T.

The last two recommendations are now done in my audit file. I treat the review as data, not as evidence.
Every number quoted above was recomputed here.

## 8. Why 101, and what it would cost to go further

- For the critical shape s₁ my own chain (optimal m₂ = 88, committed grid) gives Σx_t/K = 0.115, 0.183,
  0.290, 0.459, **0.798** and **1.265** for m = 97…102.
- The chain leaves the top of the two-rise grid (x > 23 446) at t = 25. After that only x_(t+1) ≤ δx_t
  applies, so each extra minimum multiplies the tail by about δ (0.798·1.585 = 1.265).
- m = 102 therefore needs a larger grid. Per the review, the top N must grow about 1.6× per extra m, at about
  2.6× kernel cost per m.
- So the limit is compute, not structure. A general bound M(N) ≤ N + O(log N) would push this much further,
  but it is not proved.

## 9. Caveats and scope

1. **Conditional:**
   - on Bařina's computation (published, not formally verified);
   - on Rhin's 1987 measure, in SdW's application (the paper was not re-read; see §3).

   Hercher's m ≤ 91 and SdW's m ≤ 68/75 rest on the same two kinds of input, so "previous record 91" is a fair
   comparison. Our re-run (`notes/mcycles_2_71.md`) shows that Hercher's method alone still gives 91 at 2^71.
2. **Trust base:**
   - the Lean v4.35.0-rc3 kernel, a release candidate, including GMP-accelerated `Nat`. About 431
     `decide +kernel` evaluations carry the numerics.
   - the Mathlib definitions used in the statement: `Real.exp`, `Real.log`, `Function.iterate`, `Finset.card`.

   `nanoda` is an independent kernel. A pass there (§6) removes most of the dependence on Lean's own kernel
   implementation. The reported Lean kernel soundness issue of summer 2026 is not verified by me (see
   `mcycles_2_71.md` §5); the nanoda replay addresses it independently.
3. **Unrefereed and AI-produced:**
   - the commit author is "Claude";
   - there is no human-readable proof; docstrings point to a private `research_notes/` tree;
   - the self-review is AI-written.

   The formal check makes this irrelevant for the truth of the Lean statement, not for the exposition.
4. **Scope:**
   - only positive integer cycles of T (equivalently C);
   - nothing about divergent orbits;
   - nothing about cycles with ≥ 102 minima.

   It does not improve the lower bound on the length of a cycle in general. That bound comes from cycles with
   many minima (Hercher Cor. 24, Eliahou-type bounds). For m ≥ 102 the bootstrap floors of
   `mcycles_2_71.md` §4 still apply (e.g. K ≥ 7.77·10^19 for m ≤ 124).
5. **Not a re-run of Hercher at 2^71.** The new part is not in any refereed source.

## 10. Incident during the audit (memory)

At 01:03:50–01:05:50 I ran `lake env leanchecker --help` and `leanchecker-paranoid --help` to read their
usage. Both tools ignore unknown flags, and with no module argument they replay **every** project module in
parallel, each with its own Mathlib environment. The source confirms this (`checkOlean`, `IO.asTask` per
module).

- Our lean-family processes peaked at **45.5 GB** for about 100 s. I killed the second process at 39 GB.
- In the same window the other session's `etc5` jobs stopped. These were `main_max`/`main_min` with 21 GB
  tables and `tau_M15`, logs in `scratchpad/et/`. `main_min.log` ends at R 52, where the M18 reference run
  continues to R 53.
- The kernel log shows no memorystatus/jetsam kill, and that session relaunched new binaries
  (`etc_final`, `etc_final2`) at 01:06. So it may have stopped them itself. **Please check whether those runs
  need to be repeated.**
- Afterwards the replay was run one module at a time, with a watchdog at 28 GB.

## 11. Consequences for this project (suggested; not edited)

- `CLAUDE.md`, "Cykelspåret": the best formally checked m-cycle bound is now m ≥ 102. It is conditional on
  2^71 + Rhin, unrefereed, Lean v4.35.0-rc3, and was audited here (build, axioms, replay, nanoda,
  restatement).
- `notes/mcycles_2_71.md` §5: replace "I did not check the new argument" with a pointer to this note.
  §6: correct log δ = 0.4605607 (0.46057 is above it; SdW rounded safely).
- Our `survivors` lists are now confirmed as a subset of the shapes they certify, so `mcycles.py` and their
  pipeline agree on the data.

## 12. Reproduce

```sh
cd ~/devel/mazur_dl/m102/src            # clone of main, d1895945
export PATH="$HOME/.elan/bin:$PATH"     # toolchain v4.35.0-rc3 via elan
lake exe cache get && lake build        # ~3 min, ≤ 21 GB
lake env lean ../audit/AuditM102.lean   # restatement, #print axioms
../audit/replay_seq.sh                  # leanchecker one module at a time (NOT plain `leanchecker`: it is parallel)
lake env lean -R ../audit -o ../audit/build/AuditM102.olean ../audit/AuditM102.lean
lake env sh -c 'LEAN_PATH="$LEAN_PATH:$HOME/devel/mazur_dl/m102/audit/build" \
  leanexport AuditM102 -- AuditM102.no_small_m_cycle Collatz.no_101_cycle_2_71 > ../export/main.ndjson'
~/.elan/toolchains/leanprover--lean4---v4.35.0-rc3/bin/nanoda_bin ../export/nanoda_main.json
```

Logs are in `~/devel/mazur_dl/m102/logs/`: `build1.log`, `build2.log`, `audit_main.out`,
`leanchecker_seq.log`, `nanoda_main.log`, `mem.log` and `watchdog.log`. The cross-check scripts are in the
session scratchpad, `m102/`: `parse_certs.py`, `our_survivors.py`, `compare.py`, `tworise_indep.py`,
`chain_margin.py` and `m102_probe_own.py`.
