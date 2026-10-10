# PreimageBound: a kernel-checked uniform lower bound for 3x+1 preimage counts

Lean 4 + Mathlib formalisation of the residue-class bound in `notes/extremal_trees.md` §5.2. For the 3x+1 map
T(n) = n/2 (n even), (3n+1)/2 (n odd), every a ≢ 0 (mod 3) and **every** k ≥ 0:

    0.2847 · 1.3331664^k  ≤  n_k(a) = #{ n ≥ 1 : T^k(n) = a }.

In particular n_k(a) ≥ 1.333^k for all k ≥ 20200. Applegate and Lagarias (*Density bounds for the 3x+1 problem I.
Tree-search method*, Math. Comp. 64 (1995) 411–426, Theorem 1.1) prove n_k(a) ≥ 1.302053^k for all sufficiently
large k. Their Conjecture B says n_k(a) = (4/3)^{k(1+o(1))}. Every constant this method can give is below 4/3:
at an eigenvector μ_r = 1 + ρ_r/3 with ρ_r ≤ 1 (notes §5.2). 1.3331664 is within 1.7·10⁻⁴ of 4/3.

Everything is checked by the Lean kernel. There is no `native_decide`, no `sorry`, and no axiom beyond `propext`,
`Classical.choice`, `Quot.sound`. The numerical certificates are evaluated in the kernel with `decide +kernel`.

## Statement

```lean
theorem PreimageBound.preimage_count_lower_bound (a : ℕ) (ha : 0 < a) (ha3 : a % 3 ≠ 0) (k : ℕ) :
    (2847 / 10000 : ℝ) * (13331664 / 10000000 : ℝ) ^ k ≤
      ((Finset.Icc 1 (2 ^ k * a)).filter
        (fun n => (fun m : ℕ => if m % 2 = 0 then m / 2 else (3 * m + 1) / 2)^[k] n = a)).card

theorem PreimageBound.preimage_count_ge_pow (a : ℕ) (ha : 0 < a) (ha3 : a % 3 ≠ 0) (k : ℕ) (hk : 20200 ≤ k) :
    (1333 / 1000 : ℝ) ^ k ≤ ((Finset.Icc 1 (2 ^ k * a)).filter (fun n => …same…)).card
```

Only Mathlib notions occur in these statements: `T` is written out, and the count is a `Finset.card`. The window
`[1, 2^k a]` loses nothing: `mem_preimages_iff` proves that every n ≥ 1 with T^k(n) = a satisfies n ≤ 2^k a, because
n ≤ 2·T(n). The theorem covers every a ≢ 0 (mod 3), including a ≡ 1 (mod 3), where the root of the tree does not
branch, and a on the trivial cycle {1, 2}.

## Certified constants

All of these are separate theorems `PreimageBound.preimage_count_lower_bound_R{r}'` with the same statement form,
c·μ^k ≤ n_k(a) for all k:

| r | classes (c mod 3^r, 3 ∤ c) | μ = P/Q (certified) | c = Vmin/Vmax ↓ | theorem | kernel chunks (3^8 residues each) | kernel check, wall (chunk modules) | data modules |
|---|---|---|---|---|---|---|---|
| 4 | 54 | 13215671/10^7 = 1.3215671 | 0.3567 | `…_R4'` | 1 (81 residues) | 1 s | in `CertR4` |
| 5 | 162 | 13258205/10^7 = 1.3258205 | 0.3315 | `…_R5'` | 1 (243 residues) | 1 s | in `CertR5` |
| **8** | **4 374** | **13312914/10^7 = 1.3312914** | **0.3002** | `…_R8'` | 1 | 3 s | in `CertR8` |
| 10 | 39 366 | 13324254/10^7 = 1.3324254 | 0.2915 | `…_R10'` | 9 | 15 s | in `CertR10` (5 s) |
| 12 | 354 294 | 13329408/10^7 = 1.3329408 | 0.2871 | `…_R12'` | 81 | 165 s (9 modules) | 6 parts, 47 s |
| 13 | 1 062 882 | 13330772/10^7 = 1.3330772 | 0.2859 | `…_R13'` | 243 | 541 s (27 modules) | 18 parts, 145 s |
| **14** | **3 188 646** | **13331664/10^7 = 1.3331664** | **0.2847** | `…_R14'`, **main theorem** | 729 | 1870 s (81 modules) | 54 parts, 459 s |

Wall times are on an M4 Pro, one module at a time, and include about 1 s of module loading per module. Peak RSS
per process is at most 2.7 GB, of which 0.7 GB is `lake`. r = 8 (the original target) takes 3 s. The whole r = 14
build (data, chunks, chaining) takes about 39 min. Stopping at r = 14 was a time-budget choice. r = 15 (14.3M
residues, 2187 chunks) would take about 2 h to build and as long again to re-check, for a gain of 6·10⁻⁵ in μ
(1.3332241 per the notes).

Comparison (lower bounds for n_k(a), a ≢ 0 (mod 3)):

| source | bound | range of k | status |
|---|---|---|---|
| Applegate–Lagarias 1995, Thm 1.1 | 1.302053^k | all sufficiently large k | refereed, paper proof + computation |
| extremal trees, `notes/extremal_trees.md` §5.1 | 1.317329^k | all sufficiently large k | Python/C computation |
| residue classes, notes §5.2, r = 19 | 0.2822·1.333311^k | all k | Python/C computation (int64/int128) |
| **this development, r = 14** | **0.2847·1.3331664^k** | **all k** | **Lean kernel-checked** |


μ_r is the certified lower bound P/Q for the eigenvalue of the min-system (rounded down to 7 decimals; P + 1 fails).
c is Vmin/Vmax rounded down to 4 decimals. The values agree with the numpy column of the table in
`notes/extremal_trees.md` §5.2 (to ±1 in the last digit, from a different rounding of V).

## Mathematics

* `prunedCount k a` = #{n : T^k(n) = a and T^j(n) ≢ 0 (mod 3) for all j ≤ k} is the number of depth-k nodes of
  Applegate–Lagarias' pruned tree T*_k(a). `prunedCount_le` gives `prunedCount k a ≤ nk k a`.
  `prunedCount_succ` derives the recursion
  N*_{k+1}(b) = N*_k(2b) + [b ≡ 2, 8 (mod 9)]·N*_k((2b−1)/3) for b ≢ 0 (mod 3), and `prunedCount_zero` gives N*_0 = 1.
* **Residue-class theorem** (`residue_class_bound`). Fix r ≥ 2 and M = 3^r. For classes c mod M with c ≢ 0 (mod 3) let
  β(c) = [c ≡ 2, 8 (mod 9)], lift_u(c) = ((2c−1)/3 + u·3^(r−1)) mod M (u = 0, 1, 2), and
  Φ(V)(c) = V(2c mod M) + β(c)·min_u V(lift_u(c)). If P·V(c) ≤ Q·Φ(V)(c) and V(c) ≤ Vmax on every class, then
  P^k·V(b mod M) ≤ Vmax·Q^k·N*_k(b) for every k and every b ≢ 0 (mod 3).
  The proof is a direct induction on k over all b, using natural-number arithmetic only. For b ≡ c (mod M):
  2b ≡ 2c, β(b) = β(c) since 9 | M, and (2b−1)/3 ≡ lift_u(c) with u = 2⌊b/M⌋ mod 3 (`lift_cover`).
* `residue_class_bound_real` adds Vmin ≤ V and divides: (Vmin/Vmax)·(P/Q)^k ≤ N*_k(b) ≤ n_k(b).

| file | contents |
|---|---|
| `PreimageBound/Basic.lean` | T, n_k, the pruned count, its recursion, `lift_cover`, the residue-class theorem (Mathlib) |
| `PreimageBound/Kernel.lean` | what the kernel evaluates: ternary trie `VTree`, `classOk`, `allRange` (Lean core only) |
| `PreimageBound/Check.lean` | soundness of `classOk`/`allRange` (`classOk_sound`, `cover_step`, `lower_bound_of_check`) |
| `PreimageBound/Generated/CertR{r}.lean`, `R{r}/Part*.lean` | certificate data (the trie), generated |
| `PreimageBound/Generated/R{r}/Chunks*.lean` | `theorem chunkR{r}_j : allRange fR{r} 6561 (j·6561) = true := by decide +kernel` |
| `PreimageBound/R{r}.lean` | chains the chunks into `certR{r}_ok` and states the bound for that r |
| `PreimageBound/Main.lean` | imports all r, main theorem (r = 14) and the A–L-form corollary |
| `Audit.lean` | `#print axioms` for the main statements; output in `axioms.txt` |
| `leanchecker.txt`, `nanoda.txt` | audit logs (see below) |
| `gen_cert.py` | certificate generator (numpy power iteration, integer rounding, exact Python check, Lean emitter) |
| `check_cert.py` | independent pure-Python check of a certificate + brute-force comparison with n_k(a) |
| `certs/cert_r{r}.json[.gz]` | the certificates (r, P, Q, Vmin, Vmax, c, V indexed by residue) |

## How the kernel check works

`classOk M t P Q Vmin Vmax V c` tests one residue: 3 | c, or Vmin ≤ V c ≤ Vmax and
P·V(c) ≤ Q·(V(2c mod M) + β(c)·min_u V(lift_u(c))). `classOk_sound` proves that this is exactly the hypothesis of the
residue-class theorem. V is a lookup in a ternary trie indexed by the base-3 digits of c, least significant first.
A lookup is r steps. The trie has 3^r leaf positions, and subtrees that hold only multiples of 3 are collapsed into a
single leaf. The kernel evaluates all of this. Four choices make it fast:

* `Nat.add/mul/div/mod/beq/ble` on literals are GMP-accelerated in the kernel. Typeclass arithmetic (`%`, `*`, `≤`)
  would cost several unfoldings per operation.
* `VTree.rec`, `Nat.rec` and `Bool.rec` are used directly. Structural recursion compiles to `brecOn`, and
  `cond`/`&&`/`||` go through `match` auxiliaries. Together these choices made the check about 6× faster than
  the first version (8.9 s → 1.4 s for r = 8), with 6× less kernel memory (2.0 → 0.34 GB).
* The residues are checked in chunks of 3^8 = 6561 (for r ≤ 8 a single chunk of 3^r), one `decide +kernel` theorem each, about 2 s and under 1 GB of
  kernel memory per chunk. Kernel caches are per declaration, so the memory does not accumulate.
  `cover_step` chains the chunks.
* The computational part (`Kernel.lean`, data, chunks) imports only Lean core. That saves about 1.5 GB per process
  compared with loading the Mathlib subset. A chunk-module build peaks at 1.9–2.7 GB, of which 0.7 GB is `lake`.

## Build and check

Toolchain `leanprover/lean4:v4.30.0-rc2`, Mathlib `5450b53e` (`lake-manifest.json`, the same pin as `KLMonotone` and
Mazur's development). The package tree can be APFS-cloned from an existing checkout:

    cp -cR ~/devel/mazur_dl/collatz_predecessor_090-1.0.0/.lake/packages .lake/packages   # or: lake exe cache get
    export PATH="$HOME/.elan/bin:$PATH"

Large generated files are not tracked (`.gitignore`). Regenerate them from the certificates, which is
deterministic, and optionally recheck the certificates in Python:

    for r in 4 5 8 10 12 13 14; do python gen_cert.py $r --from-json; done
    python check_cert.py certs/cert_r14.json.gz 30 12

Then build. `lake build` works, but it runs modules in parallel, at about 1.5–2.5 GB each. To stay within a memory
budget, build the modules one at a time, in this order:

    lake build PreimageBound.Kernel PreimageBound.Basic PreimageBound.Check
    # for each r: Generated.R{r}.Part* , Generated.CertR{r}, Generated.R{r}.Chunks*, R{r}
    lake build PreimageBound.Generated.R14.Part0   # … etc.
    lake build PreimageBound                        # Main + root, once everything else is built
    lake env lean Audit.lean

`python gen_cert.py r` (without `--from-json`) recomputes a certificate from scratch. Power iteration takes
seconds at r = 14 with tolerance 1e-11. The committed r ≤ 12 certificates were made with tolerance 1e-15, so a
fresh run can differ in the last digits of V (and by ±1 in P).

## Audit (2026-10-10)

**Axioms** (`lake env lean Audit.lean`, full output in `axioms.txt`):

    'PreimageBound.preimage_count_lower_bound' depends on axioms: [propext, Classical.choice, Quot.sound]
    'PreimageBound.preimage_count_ge_pow' depends on axioms: [propext, Classical.choice, Quot.sound]
    'PreimageBound.preimage_count_lower_bound_R{4,5,8,10,12,13,14}'' depends on axioms: [propext, Classical.choice, Quot.sound]
    'PreimageBound.residue_class_bound' depends on axioms: [propext, Classical.choice, Quot.sound]
    'PreimageBound.classOk_sound' depends on axioms: [propext, Quot.sound]
    'PreimageBound.certR14_ok' depends on axioms: [propext, Quot.sound]
    'PreimageBound.chunkR14_0' does not depend on any axioms
    'PreimageBound.chunkR14_728' does not depend on any axioms

No `native_decide` (`Lean.ofReduceBool` would appear above), no `sorry`. `decide +kernel` adds no axiom: the
chunk theorems depend on none.

**leanchecker** (`lake env leanchecker -v <module>`, full log in `leanchecker.txt`). Every module was replayed
separately: `Kernel`, `Basic`, `Check`, every `Generated` data/chunk module, every `R{r}` and `Main`. The root module
`PreimageBound` only imports `Main` and declares nothing, so it was not replayed on its own. One module was checked
at a time. Note that `leanchecker X` replays every module whose name has prefix `X`, in parallel, so the leaf names
must be passed. Results:

| modules | count | time | result |
|---|---|---|---|
| Kernel, Basic, Check, r = 4, 5, 8, 10 | 15 | 83 s | all exit 0 |
| r = 12 | 17 | 230 s | all exit 0 |
| r = 13 | 47 | 725 s | all exit 0 |
| r = 14 + Main | 138 | 2354 s | all exit 0 |

**nanoda** (independent Rust kernel, `nanoda_bin` 0.4.17, `nat_extension`, permitted axioms = the three above).
The input was exported with lean4export 3.1.0 at tag v4.30.0-rc2 (`~/devel/mazur_dl/tools/lean4export_v430`),
restricted to the closure of the named theorems (Mathlib dependencies included):

| export | declarations | result | time, peak RSS |
|---|---|---|---|
| `preimage_count_lower_bound_R{4,5,8,10,12}'` (one export, 152 MB) | 9 868 | "Checked 9868 declarations with no errors" | 75 s, 7.0 GB (2 threads) |
| `preimage_count_lower_bound_R13'` (354 MB) | 13 046 | "Checked 13046 declarations with no errors" | 662 s, 2.9 GB (1 thread) |
| `preimage_count_lower_bound`, `preimage_count_ge_pow` (r = 14, 1.02 GB) | 23 481 | "Checked 23481 declarations with no errors" | 2568 s, 3.6 GB (1 thread) |

nanoda's pretty-printer output confirms the statement of the main theorem, with `T` spelled out:

    theorem PreimageBound.preimage_count_lower_bound (a : Nat) (ha : LT.lt (OfNat.ofNat 0) a)
      (ha3 : Ne (HMod.hMod a (OfNat.ofNat 3)) (OfNat.ofNat 0)) (k : Nat) :
      LE.le (HMul.hMul (HDiv.hDiv (OfNat.ofNat 2847) (OfNat.ofNat 10000))
          (HPow.hPow (HDiv.hDiv (OfNat.ofNat 13331664) (OfNat.ofNat 10000000)) k))
        (Nat.cast (Finset.card (Finset.filter (fun (n : Nat) => Eq (Nat.iterate (fun (n : Nat) =>
            ite (Eq (HMod.hMod n (OfNat.ofNat 2)) (OfNat.ofNat 0)) (HDiv.hDiv n (OfNat.ofNat 2))
              (HDiv.hDiv (HAdd.hAdd (HMul.hMul (OfNat.ofNat 3) n) (OfNat.ofNat 1)) (OfNat.ofNat 2))) k n) a)
          (Finset.Icc (OfNat.ofNat 1) (HMul.hMul (HPow.hPow (OfNat.ofNat 2) k) a)))))

Why the independent replay: Lean v4.30.0-rc2 predates the fix of kernel bug #14576 (July 2026, see
`../KLMonotone/README.md`). That bug needs `addDecl`-injected inductives. This development declares exactly one
inductive (`VTree`, through the ordinary front end), and nanoda re-checks everything, `VTree` included.

**Python** (`check_cert.py`, independent of `gen_cert.py`). It checks every certificate exactly with Python integers,
computing the lift classes from actual integers b = c + t·3^r rather than from the lift formula. It also checks the
stated bounds against brute-force counts n_k(a) (iterating T on every n ≤ 2^k a) and the pruned recursion, for
a < 30 and k ≤ 12. All r pass. The smallest observed N*_k(a)/μ^k is 0.4220 (a = 7, k = 3) against c = 0.2847.

## Certificates

| r | file | sha256 |
|---|---|---|
| 4 | `certs/cert_r4.json` | `c05c570be72ff895413c8aa49f1a8e85e8a0b6b905b29d6a2f0d6817446d115c` |
| 5 | `certs/cert_r5.json` | `3dad887ec1d8c40f7278121dfa655aa3bfca1f0a49b96fd4d5352fd9dfddc481` |
| 8 | `certs/cert_r8.json` | `af27a995dda0d191df169904a1ac3032b50c4b50e961d6698bd50b844588fa71` |
| 10 | `certs/cert_r10.json` | `df8059925e9b5bdcb1d38a5771b2c0147917977454a268742f27b02f43084958` |
| 12 | `certs/cert_r12.json` | `995750461d132bea7420548fde2e46817fa60e6d39b3d9c704b06a02f19ac178` |
| 13 | `certs/cert_r13.json` (gzip: `cert_r13.json.gz`) | `ec140024349b1e6fc997b5bce63f115a34e70ecd55fa4a013551fa2711de1674` |
| 14 | `certs/cert_r14.json` (gzip: `cert_r14.json.gz`) | `f1c1e5a4f2453c8cbd98f49c29e90bd97f31352549f5146feaa7ba0779316abc` |

The sha256 values are of the uncompressed JSON. The Lean data modules are a deterministic function of these files
(`gen_cert.py r --from-json`).

