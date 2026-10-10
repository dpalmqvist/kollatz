# Extension of the m-cycle bound beyond m ≥ 102 (night of 2026-10-10)

Follow-up to `notes/mcycles_102_audit.md`. Everything was built outside the repo, in
`~/devel/mazur_dl/m102/extend/` (a copy-on-write clone of the audited tree). Nothing was committed, pushed or
posted, and nobody was contacted.

## 0. Result (short)

**Update 2026-10-10 06:20: m ≤ 104 is now certified as well (`Collatz.no_104_cycle_2_71`, at least 105 local
minima); see §8 at the end. The bullets below describe the state at 03:25.**

- **New bound: no Collatz m-cycle with m ≤ 103** (previously m ≤ 101). The bound is conditional on the same two
  hypotheses as before: every 0 < n ≤ 2^71 reaches 1, and `RhinBound` (Simons–de Weger Lemma 12).
- The Lean theorem is `Collatz.no_103_cycle_2_71`:
  `(hX : ∀ n, 0 < n → n ≤ 2^71 → Reaches T n 1) → RhinBound →
   ∀ x p, 0 < x → 0 < p → T^[p] x = x → x ≠ 1 → x ≠ 2 → 104 ≤ numLocalMin x p`.
- It depends only on `propext`, `Classical.choice` and `Quot.sound`. Every new module was built and then replayed with `leanchecker`, one module per process; all replays passed.
- My independent restatement `AuditExt.no_small_m_cycle_C` is derived from it in Lean, again with only the
  three standard axioms. It uses my own definitions: the ordinary 3n+1 map for the verification hypothesis,
  local minima counted over the minimal period, and Rhin's bound in its raw form p^(−13.3) ≤ |p log 2 − K log 3|.
- **m = 104 was prepared but not certified.**
  - Its data are generated and pass my exact mirror of the checker: 153 shapes, worst chain ratio 0.7985.
  - One of its two new grid points (N = 87 660) is kernel-checked, in 179 s.
  - The kernel check of its data module is projected at about 15–20 min. Extrapolating the memory of the
    m = 102/103 modules (12.2 GB and 18.2 GB measured) gives about 26–28 GB in one process. That is above the 25 GB budget (the
    extremal-trees job needs the rest), so I stopped at 103 (§5).
- **m = 105 and beyond:**
  - m = 105 needs two more grid points, near N ≈ 139 000 and 144 000.
  - Its walk depth is 24 570, so the data module would need roughly 1 h of kernel time and probably 35–40 GB.
  - Each further m costs about 2.5× the previous in both time and memory, so the method is compute-bound (§5).

## 1. Attribution and license

- This work extends `justinalick/collatz-m-cycles-101-lean` (GitHub; `main` = `d18959450f9acb5c0fa8c54310bc799a636d7db4`,
  2026-09-28; author Justin Alick, prepared with Claude Code). That repository's README credits C. Hercher's
  m ≤ 91 method and the Simons–de Weger framework.
- The repository is licensed under the **Apache License 2.0** (`LICENSE`, no `NOTICE` file).
- Its library is used unchanged: the checker definitions and soundness theorems (`TwoRiseCheck.lean`,
  `MCycleChain.lean`, `MCycleWalk.lean`, `HercherAll.lean`, …) and its theorem `no_101_cycle_2_71`.
- No file of the original was modified. The extension consists of **new** modules added to a private copy of
  the tree. Each new module carries a header stating that it was generated for this extension.
- Nothing has been redistributed. If it is ever published, Apache 2.0 requires shipping the license and
  marking the changes (here: new files only).

## 2. What had to change for m = 102, 103 (and 104)

The mathematics is unchanged: Hercher bootstrap → Farey walk → per-shape chain certificate with the two-rise
bound (see `mcycles_102_audit.md` §7). Three inputs grow with m.

**(a) Shapes.**
- For each m the bootstrap at the floor 2^71 + 1 stalls at K_s = 77 692 117 359 936 589 403 (the shape s₁).
- The Rhin ceiling is K_ceil = ⌈V·G_m⌉, with V the least integer satisfying `rhinOK`. This is SdW Lemma 7 set
  against Lemma 12, and plays the role of K1(m); SdW's tighter K2(m) is not used.
- The walk lists every shape (K, K+L) below the ceiling that survives the stair of Theorem 21 bounds.

| m | K_ceil | V | stair | walk depth (fuel) | walk nodes | shapes | of which floor-only | worst chain ratio |
|---|---|---|---|---|---|---|---|---|
| 101 (theirs) | 2.904e23 | 1067 | 86 | 3 738 (4 000) | 7 629 | 39 | 3 | 0.7980 |
| 102 | 4.663e23 | 1081 | 91 | 6 002 (6 102) | 13 126 | 62 | 4 | 0.7982 |
| 103 | 7.479e23 | 1094 | 96 | 9 627 (9 727) | 23 053 | 103 | 14 | 0.7984 |
| 104 (certified 06:20, §8) | 1.185e24 | 1094 | 101 | 15 258 (15 358) | 37 633 | 153 | 15 | 0.7985 |

Our own `mcycles.py survivors` lists, which use the tighter SdW ceiling K2, are again subsets.

**(b) Two-rise grid.**
- With the committed grid (top N = 23 446) the critical shape s₁ has chain ratio 1.265 at m = 102, so the grid
  must be extended.
- A greedy placement at the critical chain's own values shows that **each extra m needs exactly two more grid
  points, a factor ≈ δ higher**.
- New points, each with B = N + 30 (not the exact maximum, which the kernel does not need; heuristically
  M(N) − N ≤ 20) and W = 2N + 96:

| level | for m | points N | E1 | kernel build | leanchecker replay |
|---|---|---|---|---|---|
| X1 | 102 | 32 955, 36 150 | 16 | 885 s, 75 s | 770 s, 72 s |
| X2 | 103 | 52 248, 57 314 | 32 | 80 s, 103 s | 81 s, 104 s |
| X3 | 104 | 87 660, (90 860) | 32 | 179 s, (killed) | – |

- Points can be shifted upward freely: shifting by up to +2000 changes the worst ratio by at most 0.01.
  This made it possible to swap out slow N values (57 312 was replaced by 57 314).

**(c) Certificates.** One `ShapeCert` per listed shape: (K, P, m₂, N, M, U_b, P_e, Q = 64), with the chain
scale S = 20, exactly the repository's format.

## 3. How the data were produced (own generator)

The generator was written from the Lean definitions only. It is in the session scratchpad
(`m102/gen/mc.py`, `emit.py`); no script of the original repository was run.
- **Mirrors.** `mc.py` mirrors `epsOKX`, `stepOKX`, `chainOKX`, `rhinOK`, `walk`, `mults`, `epsAt`, `uOK`,
  `shapeOK`, `chainF/G/Next/Sum` exactly, in Python `Fraction`/`int`.
- **Construction.** It builds:
  - the bootstrap (best ε over m₂ ∈ {0, …, m}, rounded up to 4 significant digits; Stern–Brocot node of
    (deltaLo, deltaHi + ε));
  - the Rhin parameters;
  - the stair (K_ceil/1.03, then ÷1.1);
  - the walk fuel (measured depth + 100);
  - one certificate per shape (m₂ minimising U_b, N and M capped at 400).
- **Validation against their committed (kernel-accepted) data.**
  - My mirror of `mOK` returns `true` on their data for m = 92, 96, 97 and 101.
  - My generator reproduces their m = 92 data exactly (K_s, K_ceil, V, 7 boot steps, 43 walk nodes).
  - For m = 101 it reproduces the same K_s, K_ceil and V, the same 7 629 walk nodes, and the same 39 shapes,
    with worst ratio 0.7980.
- **Not trusted.** The kernel re-checks every number, so the generator is not part of the trusted base.

## 4. Lean modules, kernel times, axioms, replay

New modules in `~/devel/mazur_dl/m102/extend/src/Collatz/`:

| module | role |
|---|---|
| `MCycleTwoRiseX<N>.lean` | `AllPairs N (N+30)` via `rangeOK` chunks of 3000 first rises, `decide +kernel` |
| `MCycleGridX1/X2.lean` | `gridX1 = gridHi ++ [...]`, `gridX2 = gridX1 ++ [...]` with `…_ok : ∀ e ∈ grid, TwoRiseBound e.1 e.2` |
| `MCycleX102/X103.lean` | `dataX<m> : MData`, `dataX<m>_ok : mOK m 20 gridX<l> dataX<m> = true` (`decide +kernel`) and `no_<m>_cycle_of_floorX` via their `mOK_sound` |
| `MCycleExt.lean` | `no_102_cycle_2_71`, `no_103_cycle_2_71` (from their `no_101_cycle_2_71`, `cycle_gt_of_verified`) |

Kernel times (Lean v4.35.0-rc3, our elan; one process at a time, per-process peak memory):

| module | build | peak memory (build) | `leanchecker` replay |
|---|---|---|---|
| `MCycleTwoRiseX32955` (E1 = 16) | 885 s (one pathological k₀, see §5) | 4.8 GB | 770 s OK |
| `MCycleTwoRiseX36150` (E1 = 16) | 75 s | – | 72 s OK |
| `MCycleGridX1` | 12 s | – | 8 s OK |
| `MCycleX102` (62 shapes, fuel 6 102) | 169 s | 12.2 GB | 143 s OK (11.7 GB) |
| `MCycleTwoRiseX52248` (E1 = 32) | 80 s | – | 81 s OK |
| `MCycleTwoRiseX57314` (E1 = 32) | 103 s | – | 104 s OK |
| `MCycleGridX2` | 11 s | – | 5 s OK |
| `MCycleX103` (103 shapes, fuel 9 727) | 267 s | 18.2 GB | 259 s OK (17.7 GB) |
| `MCycleExt` | 4 s | – | 7 s OK |
| `MCycleTwoRiseX87660` (E1 = 32, for m = 104) | 179 s | – | not replayed |

Total kernel time for m ≤ 103: about 27 min of builds plus 24 min of replays. The original 3 561-job build was
reused unchanged; only the new modules were compiled.

Axioms (`lake env lean ../audit/AuditExt.lean`):

```
'Collatz.no_103_cycle_2_71' depends on axioms: [propext, Classical.choice, Quot.sound]
'Collatz.no_102_cycle_2_71' depends on axioms: [propext, Classical.choice, Quot.sound]
'Collatz.dataX102_ok' depends on axioms: [propext, Classical.choice, Quot.sound]
'Collatz.dataX103_ok' depends on axioms: [propext, Classical.choice, Quot.sound]
'Collatz.TwoRise.allPairsX32955' depends on axioms: [propext, Classical.choice, Quot.sound]
'Collatz.TwoRise.allPairsX57314' depends on axioms: [propext, Classical.choice, Quot.sound]
'Collatz.gridX2_ok' depends on axioms: [propext, Classical.choice, Quot.sound]
'AuditExt.no_small_m_cycle_C' depends on axioms: [propext, Classical.choice, Quot.sound]
'AuditExt.rhinBound_of_raw' depends on axioms: [propext, Classical.choice, Quot.sound]
AuditExt.no_small_m_cycle_C : AuditExt.VerifiedToC (2 ^ 71) → AuditExt.RhinForCycles →
    ∀ (x p : ℕ), 0 < x → 0 < p → AuditExt.Tm^[p] x = x → x ≠ 1 → x ≠ 2 → 104 ≤ AuditExt.localMinCount x
```
`AuditExt.lean` (sha256 b6b50838…) is `AuditM102.lean` from the audit with only the target changed. It keeps the
same own definitions (`Cm`, `Tm`, `localMinCount`, `VerifiedToC`, `RhinForCycles`) and the same bridge lemmas.
It builds with 0 errors.

**nanoda** (independent Rust kernel, `nanoda_bin` 0.4.17, Nat extension on, only the three standard axioms
permitted, hard error otherwise):
- **m ≤ 102 closure** (`leanexport Collatz.MCycleExt -- Collatz.no_102_cycle_2_71`, 170 MB): "Checked 30290
  declarations with no errors", 286 s, 20.7 GB peak RSS. Its pretty-printer shows the checked statement
  `… → 103 ≤ Collatz.numLocalMin x p`.
- **m ≤ 103 closure** (171.5 MB): not completed. `nanoda` passed 24 GB after about 6 min and my watchdog
  killed it (§5b). Lean's own kernel (`leanchecker`) is the only replay for the m = 103 data.

Hashes of the new modules (sha256, first 16 hex digits):

| module | sha256 prefix |
|---|---|
| `MCycleTwoRiseX32955` | e306a8c86b23f78c |
| `MCycleTwoRiseX36150` | 67f609297ea6e82c |
| `MCycleGridX1` | 79f1ca961736dbde |
| `MCycleX102` | de882a030f2f080d |
| `MCycleTwoRiseX52248` | 3914e22e4fbeb827 |
| `MCycleTwoRiseX57314` | 00e18a18d01268b4 |
| `MCycleGridX2` | 89f2c287b36c1067 |
| `MCycleX103` | aee10c4b9fbdd4b0 |
| `MCycleExt` | 641252586e137ebf |

**Prepared for m = 104 but not built.** These files are not imported by `MCycleExt`:
- `MCycleTwoRiseX87660` (built in 179 s, not replayed);
- `MCycleTwoRiseX90860`;
- `MCycleGridX3`;
- `MCycleX104` (153 shapes, fuel 15 358).

The m = 104 data pass my exact mirror of `mOK` with `gridX3`. Adding `import Collatz.MCycleX104` and a
`no_104_cycle_2_71` theorem to `MCycleExt` would finish it on a machine with about 30 GB to spare.

## 5. Why it stops at 103, and what 104–106 would need

**Kernel cost of the walk.**
- The cost of `mOK` grows like (walk nodes) × (walk depth). The walk climbs ladders of length about K_ceil/K_s
  one step at a time.
- Measured: their m = 101 data take 45 s (7 629 nodes × 3 738 depth); the m = 103 walk alone takes 8.7 min
  (23 053 × 9 727).
- Memory grows too: the m = 102 data module peaks at 12.2 GB, the m = 103 walk test at 10.7 GB, and the m = 103
  module at 18.2 GB (build) and 17.7 GB (replay), all measured.
- Projections:

| m | walk nodes | depth | projected kernel time | projected memory |
|---|---|---|---|---|
| 104 | 37 633 | 15 358 | about 18 min | about 26–28 GB |
| 105 | 65 427 | 24 570 | about 50 min | probably 35–40 GB |

**Grid.** Each m needs two new points, a factor δ ≈ 1.585 apart:
- m = 104: N ≈ 87 660 and 90 860 (the first is checked);
- m = 105: N ≈ 138 955 and 144 021;
- m = 106: N ≈ 228 000.

The two-rise kernel cost grows roughly like N^2.3, but erratically (next paragraph).

**A pathology in the two-rise checker** (useful for the original author):
- With the repository's window width E1 = 16, some (N, k₀) are 100× slower than their neighbours:
  - N = 32 955, k₀ = 1 alone takes 644 s, against 5 s for N = 36 150 or N = 32 957;
  - N = 52 248, k₀ ≈ 13 117–13 121 makes one chunk exceed 75 s.
- Mechanism (the second case): c = 3^(−k₀) mod 2^W has a run of ~16 zero bits starting at bit A = N − k₀.
  The E1-bit window P then has its lowest set bit at s = 12…16, the effective pattern length E1 − s − 1 shrinks
  to 3…0, and 5 000–39 000 positions each get a direct test (W-bit multiply and mod).
- **E1 = 32 removes these cases.** With B = N + 30 the checker still has lmin = 1, and the soundness proof does
  not depend on E1. Measured: the same N = 52 248 cluster takes 2 s, and N = 32 955, k₀ = 1 takes 4 s. With
  E1 = 32, N = 52 248 took 80 s for the whole point.
- E1 = 32 did not make N = 57 312 fast; it was killed after 723 s. N = 57 314 took 103 s. So slow N should be
  screened and replaced, which is harmless (§2b).

**Ways to go further (not done).**
- Give the walk a fast ladder step (jump j·(b+d) by division instead of one mediant at a time) with its own
  soundness proof. This would remove the depth factor.
- Prove `D.shapes = [explicit list]` and the certificates in separate declarations, to split the memory.
- A machine with about 30 GB free for one Lean process could certify m = 104 with the present data as it
  stands, in about 1 h including replay.

## 5b. Incidents

My watchdog (22, later 24 GB, covering only my lean, lake, leanchecker and nanoda processes) fired four times:
- 02:34: a grid build plus three screening runs;
- 02:52: a grid build plus two whole-range single-theorem screens;
- 03:01: the m = 103 data module (18 GB) plus a grid build;
- 03:19: `nanoda` on the m ≤ 103 closure.

Correction (06:20): until 03:57 the watchdog used `pkill -x lean`, which kills every process named `lean`.
That includes other sessions' Lean jobs (the v4.30 toolchain runs in `lean_formal/PreimageBound` and `KLMonotone`).
So the claim that no other job was touched is not established. Any other session's `lean` process alive at
02:34, 02:52, 03:01 or 03:19 would also have been killed, and that session should check its runs at those times.
Since 03:58 the watchdog only targets processes of `m102/extend` and my own `leanchecker`/`nanoda` runs. Everything that counts was afterwards
rebuilt and replayed one heavy process at a time. Per-process peaks in the final runs were at most 18.2 GB
(Lean) and 20.7 GB (`nanoda`, m ≤ 102).

## 6. Reproduce

```sh
cd ~/devel/mazur_dl/m102/extend/src      # copy of justinalick/collatz-m-cycles-101-lean @ d1895945 + new modules
export PATH="$HOME/.elan/bin:$PATH"      # leanprover/lean4:v4.35.0-rc3
lake build Collatz.MCycleExt             # NB: builds the new two-rise modules in parallel; run them one by one if memory is tight
lake env lean ../audit/AuditExt.lean     # statements, restatement, #print axioms
for m in MCycleTwoRiseX32955 MCycleTwoRiseX36150 MCycleGridX1 MCycleX102 MCycleTwoRiseX52248 MCycleTwoRiseX57314 \
         MCycleGridX2 MCycleX103 MCycleExt; do lake env leanchecker -v Collatz.$m; done   # one module per process
```

The generator (`mc.py`, `emit.py`, `points.json`) and the logs are in the session scratchpad (`m102/gen/`) and in
`~/devel/mazur_dl/m102/extend/logs/`.


## Addendum (main session, 2026-10-10 ~03:55): nanoda on the m ≤ 103 closure

Re-run with more memory than the agent's 24 GB budget (`num_threads` 2, under a free-memory watchdog):
`nanoda_bin export/nanoda_ext_t2.json` → **"Checked 30446 declarations with no errors"**, 1188 s, peak RSS 31.2 GB
(log: `~/devel/mazur_dl/m102/extend/export/nanoda_ext_main.log`). The pretty-printer output shows
`Collatz.no_103_cycle_2_71` and the restatement `AuditExt.no_small_m_cycle_C`. So the m ≤ 103 result is now also
checked by an independent kernel.

## 8. m = 104 (2026-10-10, 03:47–06:20)

**Result.** `Collatz.no_104_cycle_2_71`:
`(hX : ∀ n, 0 < n → n ≤ 2^71 → Reaches T n 1) → RhinBound → ∀ x p, 0 < x → 0 < p → T^[p] x = x → x ≠ 1 → x ≠ 2 →
105 ≤ numLocalMin x p`. **No Collatz m-cycle with m ≤ 104**, conditional on the same two hypotheses.
- It depends only on `propext`, `Classical.choice` and `Quot.sound`.
- The restatement `AuditExt104.no_small_m_cycle_C` (own definitions, ordinary map, raw Rhin form; conclusion
  105 ≤ local minima over the minimal period) also has only the standard three axioms. The log is
  `extend/logs/audit_ext104.out`, 0 errors.
- The new constants `dataX104_ok`, `allPairsX87660`, `allPairsX90960` and `gridX3_ok` have the same three axioms.

**New modules**, each built and then replayed with `leanchecker` in its own process, sequentially. Before every
heavy step a gate required ≥ 35 GB free (`vm_stat`). The own-process watchdog at 31 GB never fired.

| module | content | build | `leanchecker` replay | sha256 prefix |
|---|---|---|---|---|
| `MCycleTwoRiseX87660` | `AllPairs 87660 87690`, E1 = 32 | 179 s | 166 s OK | 79e83d67514ec96e |
| `MCycleTwoRiseX90960` | `AllPairs 90960 90990`, E1 = 32 | 183 s | 179 s OK | 9a7368d68377590c |
| `MCycleGridX3` | `gridX3 = gridX2 ++ [(87660, 87690), (90960, 90990)]` | 9 s | 11 s OK | a1ff7f386060c094 |
| `MCycleX104` | 153 shapes (15 floor-only), walk fuel 15 358, worst chain ratio 0.7988 | 842 s, peak 27.7 GB | 840 s OK, about 27.2 GB | a4aa78bca687d206 |
| `MCycleExt104` | `no_104_cycle_2_71` from `no_103_cycle_2_71` (imports `MCycleExt`) | 5 s | 5 s OK | 8fbd0a689ac8bbe9 |

The restatement file `extend/audit/AuditExt104.lean` has sha256 prefix d7a14bb9027c91f5.

**Grid point choice.** N = 90 860 and N = 90 900 each exceeded a 900 s limit and were abandoned. N = 90 960 then
checked in 183 s; the shift changes the m = 104 worst ratio only from 0.7985 to 0.7988. The slow cases sit at small
k₀: for N = 57 312 (a slow case from the night) the only slow chunk is the first, k₀ ≤ 3000, where 3^(−k₀) mod 2^W
is short-periodic. A cost model that predicts which N are slow is still missing; screening by time limit works.

**The first m = 104 attempt failed** (04:39, after 995 s; this was not a time-out or memory kill).
- The kernel check of a declaration runs under the options in force: `addDeclCore env maxHeartbeats maxRecDepth`
  in `Lean/Environment.lean`.
- The m = 104 check (about 2.6× the m = 103 work) ran out of the default heartbeat budget.
- `decide +kernel` then hides the kernel's own exception. It re-reduces with the elaborator and reports that
  diagnostic instead ("failed to reduce … Reduction got stuck at … eps.num − (0 + 1)"); see `doKernel`/`diagnose` in
  `Lean/Elab/Tactic/Decide.lean`.
- **Fix:** `set_option maxHeartbeats 0 in set_option maxRecDepth 100000 in` before `theorem dataX104_ok`. These are
  resource limits only (their `Terras.lean` uses the same `maxRecDepth`), and the second attempt passed.
- The `leanchecker` replay is independent of these options: `Lean.Replay` calls `addDeclCore … 0 0`, i.e. no limit.

**nanoda for m ≤ 104: done later (main session, 2026-10-10 12:09; see the addendum at the end).** At 06:20 only
38.8 GB was free, against the 45 GB rule, so it was skipped at first. The full closure then passed the independent
kernel: "Checked 30580 declarations with no errors".

**m = 105 outlook.** Grid points near N ≈ 138 955 and 144 021 are needed (shifts are allowed). The data module has
238 shapes and walk depth 24 570. The m = 102/103/104 peaks of 12.2, 18.2 and 27.7 GB and times of 169, 267 and
842 s suggest about 40–45 GB and about 40 min for its kernel check, plus the same again for the replay. That needs a
machine where one Lean process may use ≥ 45 GB, plus about 1.5–2 h.

**Reproduce (m ≤ 104).**
```sh
cd ~/devel/mazur_dl/m102/extend/src; export PATH="$HOME/.elan/bin:$PATH"
lake build Collatz.MCycleTwoRiseX87660; lake build Collatz.MCycleTwoRiseX90960   # one at a time
lake build Collatz.MCycleExt104                                                    # MCycleX104: ~14 min, ~28 GB
lake env lean ../audit/AuditExt104.lean
for m in MCycleTwoRiseX87660 MCycleTwoRiseX90960 MCycleGridX3 MCycleX104 MCycleExt104; do
  lake env leanchecker -v Collatz.$m; done                                         # one module per process
```

## Addendum (main session, 2026-10-10 12:09): nanoda on the m ≤ 104 closure

`nanoda_bin` 0.4.17 (Lean v4.35.0-rc3 toolchain), replaying the lean4export closure `export/ext104.ndjson`
(171.9 MB) of `AuditExt104.no_small_m_cycle_C` and `Collatz.no_104_cycle_2_71`. Settings: permitted axioms propext,
Classical.choice and Quot.sound, with unpermitted axioms a hard error; Nat and String extensions on; 2 threads.
- Result: **"Checked 30580 declarations with no errors"**, 3540 s wall (6954 s CPU), peak RSS 49.8 GB.
- The pretty-printer shows both statements as in §8: 105 ≤ local minima for every nontrivial cycle, given
  verification to 2^71 and Rhin's bound.
- Log: `~/devel/mazur_dl/m102/extend/export/nanoda_ext104_t2.log`; memory trace in `watchdog_ext104_t2.txt`.

Two earlier attempts were killed by our own watchdog, not by nanoda:
- 2 threads, killed at 1625 s and 35.9 GB;
- 1 thread, killed at 6782 s and 37.8 GB.

Both times the trigger was "Pages free < 3 GB", which ignores reclaimable inactive memory. The successful run used a
watchdog on free + inactive + speculative + purgeable memory (< 2 GB) and swap (> 12 GB). Neither condition was
reached; at least 32 GB stayed available, and no swap was used.

So m ≤ 104 is now checked by Lean's kernel twice (build and `leanchecker`) and by an independent kernel.
