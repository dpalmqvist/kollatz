# Overnight 2026-10-09/10: morning briefing

Nothing is committed: everything is in the working tree (`git status`). The detailed log follows below the briefing.

## The five things that matter

1. **Conjecture A (positive density of predecessors) is formally true.** Mazur's ProofAtlas formalisation was rebuilt
   cold, replayed with `leanchecker --fresh`, re-stated independently, and finally **replayed in the independent
   nanoda kernel (43 862 declarations, no errors)**. Sources: `notes/m2_audit.md`, AVENUES "Strategic update".
   - All x^γ bounds for a fixed a are superseded.
   - What remains ours: uniformity in a, explicit constants, the method's structure, and the cycle track.
   - Formally, Collatz ⇔ P(1) has upper density 1; `reports/density_one_gap.md` says exactly why that gap is the
     whole problem.
2. **Our theorem: the K–L constants λ_k are attained, tight, unique and strictly increasing**, plus the closed form
   ρ_k = 3(λ_k − 1)/λ_k^α with 1 − ρ_k ↓.
   - This answers K–L 2003's open problem and A–L's Conjecture 4.1.
   - Lean: ≈1340 lines, standard axioms only. It builds on v4.30 and on the post-fix v4.35, passes leanchecker, and
     passes **nanoda**.
   - Sources: `notes/strict_monotonicity.md`, `paper/monotone.md` (short paper draft), `lean_formal/KLMonotone/`.
3. **New: uniform bounds for k-step preimage counts.** (1.3333119)^k ≲ n_k(a) ≲ (1.3333567)^k for every a,
   against Applegate–Lagarias 1995's 1.302/1.358.
   - Also exact extremal trees to depth 59 (A–L: 30).
   - I re-checked it independently (r = 13, 16).
   - **Lean-formalised:** 0.2847·(1.3331664)^k ≤ n_k(a) for every a, k (r = 14, kernel `decide`, standard axioms, leanchecker + nanoda; `lean_formal/PreimageBound/`).
   - Sources: `notes/extremal_trees.md`, RESULTS.md, AVENUES §15/§28.
4. **m-cycles.**
   - Hercher's method at 2^71 still gives only m ≤ 91; m = 92 needs 2^73.87 (`notes/mcycles_2_71.md`).
   - The unrefereed m ≥ 102 Lean repository is **valid given 2^71 + Rhin** (leanchecker + nanoda + restatement;
     `notes/mcycles_102_audit.md`).
   - **Extended tonight to m ≤ 104: every nontrivial cycle has ≥ 105 local minima** (m ≤ 103 also nanoda-checked), conditional on the same
     inputs. It is Lean-checked on the post-fix v4.35 kernel (standard axioms, per-module leanchecker) and
     restated independently (re-run by me). Sources: `notes/mcycles_extension.md`, extending the Apache-2.0
     repository with attribution.
   - nanoda (independent kernel) also passed for m ≤ 103: 30 446 declarations, no errors (re-run by me with 31 GB).
5. **Explicit uniform-in-a envelope** (RESULTS.md table), using four new certified vectors:
   - π_a(x) ≥ 0.7146 (x/a)^{0.848} from 2^{6.25} a;
   - 0.5514 (x/a)^{0.8718} on 2^{15.7}…2^{18.3};
   - 0.4987 (x/a)^{0.8797} up to 2^{335} (k = 17, certified tonight);
   - then k = 22.

   The earlier "0.865" was corrected to the rigorous 0.8435.

## Your decisions
- **CLAUDE.md "Omvärld 2026"** still calls Mazur's positive density "obekräftat". My edit was blocked by the
  permission classifier. It also misdescribes his 436·log N result, per the density report.
- **Preprint framing:** see `paper/repositioning_proposal.md`. The short paper `paper/monotone.md` could be
  submitted on its own.
- **Committing.** Nothing is committed. The large new data files are `cycles_by_length*.json`,
  `cycle_numerators_*.json`, `base_lift_*.json` and the `certs/spread_k1{5,6,7}_*` directories.

---

# Detailed log

Nothing is committed: all changes are in the working tree (`git status`). Ordered by importance.

## 1. Mazur's positive-density theorem is formally verified (strategic shift)

`notes/m2_audit.md`, built in `~/devel/mazur_dl/m2/`.

The ProofAtlas formalisation "Positive Lower Density of Collatz Predecessors" (Mazur, Sept 2026, AI-generated,
unrefereed) passes everything we threw at it:
- a cold rebuild from published sources (sha256 match);
- `leanchecker --fresh` (whole environment, Mathlib included);
- `#print axioms`, which shows only propext, Classical.choice and Quot.sound;
- an independent restatement with our own Collatz map and `Finset` count (`AuditM2.conjectureA`), which I re-ran
  myself.

So, unless Lean's kernel is unsound, **Applegate–Lagarias Conjecture A is a theorem**: π_a(x) ≥ c_a x for all
a ≢ 0 (mod 3), with c_a ineffective. Also formal: Collatz ⇔ P(1) has upper density 1.

Consequences:
- All x^γ records (ours, 0.9251) are superseded as statements about π_a for fixed a.
- Not superseded:
  - uniformity in a (K–L bounds hold for all a in a class at once);
  - explicit constants;
  - the K–L structure question (λ_k → 2), now the uniform-in-a exponent question.
- AVENUES.md has a "Strategic update" section and new avenues 23–25.
- **Your decision:** my edit to CLAUDE.md's "Omvärld 2026" (which still says "obekräftat") was blocked by the
  permission classifier. Update it if you agree.
- **Your decision:** the preprint `paper/draft.md` still frames the x^γ record as the headline. It needs
  repositioning: structure theorem, explicit uniform bounds, method analysis.

## 2. Theorem: λ_k is attained, tight, unique and strictly increasing (all k)

Sources: `notes/strict_monotonicity.md`, `paper/monotone.md`, `lean_formal/KLMonotone/`.

- Krasikov–Lagarias 2003 §6 list strict increase as an open problem. Applegate–Lagarias 1995 called it easy, but
  their sketch has a gap: slack in one row does not let λ increase for a general LP.
- K–L's conditions (1) attainment and (2) tightness were "likely … but may be difficult to prove". Both are now
  proved, plus uniqueness and 1 < λ_k < 2.
- Corollaries: c λ_k^y solves Krasikov's I_k exactly (K–L's optimality belief), and A–L Conjecture 4.1 holds.
- Key idea: m ↦ 4m is one cycle of length 3^{k−1} on the principal classes, so slack spreads to every row.
- **Lean 4**, about 1250 lines, 10 s, standard axioms only, no certificates. The program is stated literally as
  K–L (2.7)–(2.14), with residue-faithfulness lemmas. Main theorem `KLMono.KL_lambda_strictMono`.
- Short standalone paper `paper/monotone.md` (+ `.html`); preprint draft 0.9 §2.4; `monotone_check.py`
  (numerics); RESULTS.md; AVENUES §22.
- The argument extends to 5x+1 (×16 is one cycle; checked numerically), with the summation and descent lemmas
  for 5x+1 not written out.

## 3. Explicit uniform-in-a bounds: a correction and improvements

Script: `base_lift_chunked.py`.

**Correction.** The earlier "π_a(x) ≥ 0.865 (x/a)^{0.7991}" took the minimum at 0.25-grid points only. The counts
are step functions, so this is not a rigorous infimum. The rigorous value is 0.8435 (grid 1/64), for x ≥ 16a.

**New certified envelope** (a ≡ 2 mod 3, not in a cycle; for a ≡ 1 divide by λ):

| x/a | bound | source |
|---|---|---|
| 2^{6.25} … 2^{20.8} | 0.7146 (x/a)^{0.8480} | `certs/spread_k14_1.80` + lifted base |
| 2^{20.8} … 2^{251} | 0.5681 (x/a)^{0.8639} | `certs/spread_k15_1.82` (new certificate tonight) + lifted base |
| ≥ 2^{251} | (x/a)^{0.92509}/(4λ · 9840.7) | `certs/k22_1.8988` |

These are the best explicit bounds, since Mazur's constants are ineffective.

A k = 16, λ = 1.83 vector was started; see the end of this file.

## 4. Running or partial at the time of writing

- **Avenue 13 (agent):** Hercher's m-cycle bound re-run with X0 = 2^71 (`mcycles.py`, `notes/mcycles_2_71.md`).
- **Avenue 15 (agent):** Applegate–Lagarias extremal trees past depth 30, to improve the 1995 constants
  1.302053/1.358386 of their Theorem 1.1 (`extremal_trees.py`, `notes/extremal_trees.md`).
- **k = 16, λ = 1.83** spread vector, then certify, then base-lift.

Results of these are appended below when they finish.

## 5. Results that came in later

- **Avenue 13 (m-cycles at 2^71): negative, validated** (`notes/mcycles_2_71.md`; `mcycles.py validate` re-run
  by me: all checks pass).
  - The verified range 2^71 still gives exactly m ≤ 91; m = 92 needs X0 ≥ 2^73.87.
  - Hercher and Simons–de Weger are reproduced exactly, with two harmless misprints found in the papers.
  - The unrefereed "m ≥ 102" Lean repository rests on a new combinatorial argument, not on 2^71; it is unverified.
- **Explicit bound, k = 15:** π_a(x) ≥ 0.5681 (x/a)^{0.8639} for x ≥ 2^{6.25} a (certified tonight,
  `certs/spread_k15_1.82`). It is best for 2^{20.8} ≤ x/a ≤ 2^{251} (table in RESULTS.md).
- **5x+1:** the structure theorem holds verbatim, with the ceiling λ* = 1.5701677 in place of 2 (written out in
  `notes/strict_monotonicity.md` §4b; not formalised).
- **Preprint:** a repositioning proposal is in `paper/repositioning_proposal.md`, for you to decide.
- **Lean, later in the night:**
  - New corollary `rho_eq` / `rho_strictMono`: at λ_k the mean loss ρ_k = 3(λ_k − 1)/λ_k^α exactly, and 1 − ρ_k
    is strictly decreasing in k.
  - The development now builds standalone (`lean_formal/KLMonotone/lakefile.toml`, Mathlib pinned to the same
    commit, `autoImplicit = false`). That build exposed and fixed one auto-bound implicit.
  - It passes `leanchecker`; `axioms.txt` was regenerated (standard axioms only, about 1340 lines).
- **k = 16, λ = 1.83** certified (`certs/spread_k16_1.83`, spread 29.49, γ = 0.8718). Its base lift was running.
- **Avenue 19, step 2:**
  - New GPU kernel `cycle_numerators_k.py` for fixed-weight parity vectors (unrank + Gosper, exact integer phases),
    validated against the all-vector run for n ≤ 24.
  - n ≤ 40 done for k_max, k_max−1, k_max−2 (`cycle_numerators_k.json`); n = 41–45 at k_max were running.
  - No nontrivial cycle numerators ≡ 0.
  - At k_max, |S_h|·√binom stays at the random level (≈1–5) when m/2^n ≲ 0.3. It grows with n when
    m/2^n ≈ 0.5–0.66 (6.9 at n = 30 → 86 at n = 41), and much faster below k_max.
  - So equidistribution at random level holds only in the regime of the best approximations of log₂ 3.
- **m ≥ 102 audited** (`notes/mcycles_102_audit.md`). The unrefereed repository proves that every nontrivial cycle
  has ≥ 102 local minima, given 2^71 verification and Rhin's bound.
  - Checks: leanchecker, the independent nanoda kernel, our own restatement in Lean (re-run by me), and independent
    recomputation of the new "two-rise" bound (sharp) and of all 120 chain certificates.
  - This is the current m-cycle record, conditional on the standard inputs. Our own re-run of Hercher's method at
    2^71 gives only m ≤ 91.
- **Density-one survey** (`reports/density_one_gap.md`): after Mazur's Cor. 1.2, density one of P(1) *is* Collatz.
  - Tao's method stops exactly at f → ∞ versus a fixed bound B. The error O(log^{-c} N0) never vanishes at fixed N0.
  - Tao's machinery works unchanged for 3x+5 and 3x−1, where the fixed-B statement is false. So any proof must use
    3x+1-specific arithmetic.
  - It flags two text errors you may want to fix:
    - CLAUDE.md "Omvärld 2026" misdescribes Mazur's 436·log N result: it is Tao's theorem in natural density for
      any f → ∞, not descent "below the start".
    - The adjacent-work report gives Korec's exponent as log 4/log 3; it is log 3/log 4 ≈ 0.7925.

  I did not edit CLAUDE.md (that is your call). I fixed the Korec typo in the report, after checking it.
- **Process note.** The m ≥ 102 audit agent's leanchecker runs briefly used about 45 GB around 01:04. That may have
  interrupted the extremal-trees runs, and I asked that agent to re-check and re-run them.
- **Avenue 19, step 3** (`cycle_numerators_fine.py`): fine-scale tests at k_max for n ≤ 40.
  - Windows next to 0 (down to width m/2^30) are at the random level.
  - Divisibility by prime factors p | m is strongly biased: ×11 for p = 186793 at n = 24, where m = 13p. Exact
    explanation (brute-force confirmed): when d = gcd(n, k) > 1, 2^n − 3^k = (2^{n/d} − 3^{k/d})·Φ, and every
    d-periodic parity vector has N divisible by Φ.
  - Periodic vectors never give new cycles. So the heuristic count must exclude them; what remains is a small-prime
    effect, plus rotation clustering of the variance.
- **Explicit envelope updated:** k = 16, λ = 1.83 certified and lifted: π_a(x) ≥ 0.5514 (x/a)^{0.8718} for x ≥ 2^{6.25} a. It is best for 2^{15.7} ≤ x/a ≤ 2^{288} (table in RESULTS.md). A k = 17 vector is being computed.
- **Avenue 19 confirmation:** with periodic parity vectors excluded (`--aperiodic`), every large divisibility anomaly vanishes (n ≤ 40). Only the mild p = 5 effect (≤ 2 %, shrinking with n) and one ×1.035 at p = 499 = 2^8 + 3^5 remain. The equidistribution heuristic for primitive parity vectors survives every fine-scale test so far.
- **Avenue 27, first data:** `cycles_by_length.py`, an exact census of all 3x+d cycles of length ≤ 34 for 67 values d < 200, on the GPU. It is validated against brute force. It finds 72 cycles of length ≥ 22; their clusters are algebraic (3x+13: 2^8 − 3^5 = 13 = d; d = 71: 71 | 2^27 − 3^17). The uniform necklace heuristic overestimates by a factor 1.5–2, decreasing with length (details in AVENUES §27).
- **Kernel-bug check.** Lean < 4.32.2 had kernel bug #14576 (a proof of False via `addDecl`-injected inductives,
  invisible to `#print axioms`).
  - KLMonotone now also builds on the post-fix v4.35.0-rc3 and passes leanchecker there. The independent Rust kernel
    nanoda checked 30 006 declarations (full closure, Mathlib included) with no errors.
  - For Mazur's M2: built lean4export at its v4.30.0-rc2 tag, exported the full closure (298 MB) and replayed it in
    nanoda: **43 862 declarations, no errors**. M2 is now independent-kernel verified (addendum in
    `notes/m2_audit.md`).
- **Avenue 15 (agent), strong result:** exact Applegate–Lagarias extremal trees to depth 59/55 (A–L stopped at
  30), and **residue-class certificates for k-step preimage counts**:
  0.2822·(1.3333119)^k ≤ N*_k(a) ≤ 3.556·(1.3333567)^k for every a and every k.
  - This improves A–L Theorem 1.1 (1995: 1.302/1.358) to within 3·10^{−5} of 4/3, uniformly in a.
  - I re-implemented the certificate independently and reproduced r = 13 exactly; r = 16 was running.
  - No later improvement was found in the literature.
  - New avenue 28: this "depth K–L system" mixes much faster (0.65 per digit against 0.93) and is a natural model
    for proving ρ → 1.
- **05:40 k = 17 done:** `certs/spread_k17_1.84` (spread 33.84) with lifted base gives π_a(x) ≥ 0.4987 (x/a)^{0.8797}
  for x ≥ 2^{6.25} a. It is best for 2^{18.3} ≤ x/a ≤ 2^{335} (RESULTS table updated).
- **Rate limit.** Both Lean agents (m = 104; preimage-bound formalisation) were stopped by an API session limit at
  about 04:00 and resumed at 05:42. The m = 104 data-module build had failed with an error, which is being
  diagnosed. The preimage formalisation had certificates through r = 14 in place, with the README table still to
  fill.
- **~06:30 m ≤ 104 certified** (≥ 105 local minima; Lean v4.35, standard axioms, leanchecker; restatement re-run by me). Note: until 03:57 the m-cycle agent's memory watchdog used `pkill -x lean`, which could have killed other sessions' Lean jobs at 02:34/02:52/03:01/03:19. None of my results were affected, since all completed with success output; the PreimageBound agent is re-auditing its own builds.
- **08:50 final checks:** I re-ran the PreimageBound axiom audit (standard axioms; statement faithful, T written out). The m ≤ 104 nanoda replay was started.

## 6. Morning session (2026-10-10, while nanoda replays m ≤ 104)

- **Second short paper drafted:** `paper/preimage.md` → `preimage.html`, "Uniform exponential bounds for the number of
  3x+1 preimages". It contains Theorems 1–3 and §7 on the limit measure (below).
- **Avenue 28: the depth system's Perron vectors are the marginals of one 3-adic measure** (`syracuse_measure.py`,
  AVENUES §28).
  - Proved: averaging over the top digit commutes with the averaged operator. So the Perron vectors h_r form a
    martingale, and they are the marginals of the stationary law ν of the walk x ↦ x/2, (3x+1)/2 with probabilities
    3/4, 1/4.
  - Probability 1/2 is Tao's Syracuse random variable, and it is *exactly* the Krasikov–Lagarias system at λ = 2
    with mean instead of min. So K–L (size counting) is p = 1/2 and depth counting is p = 1/4.
  - The L² norm of the martingale differences contracts by √(3p/(2−p)), up to cross-correlations that vanish
    numerically. This explains the 0.65 = √(3/7) loss rate. At p = 1/2 the factor is exactly 1: the K–L problem is
    critical, and its loss ratio rising to 0.93 matches the L¹ decay of Tao's measure.
  - Threshold p = 1/3 for a bounded density: the fixed point −1 multiplies the density by 3p per level. This is the
    origin of the 1.52^k spread of the K–L certificates.
  - p = 1/4: every L^q norm decays fast enough for a continuous density.
  - Its min and max match the exact extremal-tree limits (2.039, 1.742) to 2·10^{−4}.
  - Proved: continuity ⇒ Applegate–Lagarias Conjecture C′. The proof programme is a moment recursion with exact
    diagonal coefficients.
  - **Check before claiming:** Wirsching, LNM 1681, has a 3-adic Markov process for the inverse map.
