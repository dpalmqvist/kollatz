# kollatz — Krasikov–Lagarias predecessor bounds for 3x+1, taken to k = 21

Lower bounds π_a(x) ≥ x^γ for the number of integers below x whose 3x+1 orbit reaches a, by the linear-programming
method of Krasikov & Lagarias (Acta Arith. 2003, published record γ = 0.84 at k = 11). This repository holds the
computation, the rigorous integer certificates, two formally verified instances (Lean 4, via Lech Mazur's
development), the analysis of where the method is heading, and a side track on cycle lengths.

| Result | Where |
|---|---|
| γ = 0.9203 certified at k = 21 (3.5 × 10^9 LP variables), all k = 12 … 21 | `RESULTS.md`, `certs/*/cert.json` |
| Lean-checked theorems x^0.903 (k = 18) and x^0.909 (k = 19) | `lean_formal/` |
| Why the exponent may or may not reach 1, with a mechanism and a prediction | `AVENUES.md` §1 |
| Cycle track: Eliahou's bound reproduced, weighted LP, what Hercher adds | `AVENUES.md` §4, `cycles*.py` |
| Everything else we tried, learned or rejected | `CLAUDE.md` (working notes, Swedish) |
| Slide deck for walking through all of it | `presentation.html` (open locally; arrows to navigate) |

## Start here on a new machine

```bash
python3.14 -m venv .venv && source .venv/bin/activate
pip install numpy scipy mpmath mlx matplotlib
python kl.py            # nothing; import test
python lp_check.py 6    # independent LP, should reproduce K-L Table 2 for k <= 6 in seconds
python rho.py           # needs the certificate vectors (see below)
```

The big binaries are **not in git** (`*.npy`, 24 GB of certificates plus 20 GB of warm-start vectors). Two ways to
get them back:

1. Copy `certs/*/c_f32.npy`, `certs/*/C.npy` and `c_k{16..21}_mlx.npy` from the original machine by disk.
2. Regenerate: `python kl_mlx.py lambda 12` then `python kl_mlx.py lambda K c_k{K-1}_mlx.npy` for K = 13 … 21 (warm
   start from the previous level; k = 21 takes ~16 min and 16 GiB on an M5 24 GB), and certify each with
   `python certify_fast.py K LAMBDA c_kK_mlx.npy --save` using the λ values in `RESULTS.md`. Every `cert.json`
   carries the sha256 of the vector it was made from, so a regenerated vector can be checked against it only if
   the float32 computation is bit-reproducible; otherwise re-certify and compare λ and slack.

On a 64 GB machine the natural next computations are k = 22 (about 50 GiB with the int8 path, see
CLAUDE.md "Gränser") and the Lean check of k = 20 (about 30 GiB with `LoopCheck.lean`), plus the k = 22–23 test
of the prediction in `AVENUES.md` §1.

## Layout

- `kl.py`, `kl_mlx.py` — the map F, power iteration, λ search (NumPy reference; MLX/Metal production)
- `certify.py`, `certify_fast.py`, `verify_cert.py` — exact rational reference, int64 certification, independent verifier
- `lp_check.py`, `kl_d.py` — independent LP implementation (HiGHS); the 3x+d generalisation
- `rho.py`, `holder.py`, `limit_measure.py`, `jacobian.py`, `rF2_fit.py`, `renorm.py`, `renorm2.py`, `tree_growth.py` — limit-object analysis
- `adaptive.py` — adaptive-tree experiment (negative result)
- `cycles.py`, `cycle_harmonic.py`, `cycle_dip.py`, `cycle_lp.py`, `cycles_d.py` — cycle track
- `export_mazur.py`, `potential.py`, `lean_formal/` — pipeline into Mazur's Lean development, generated modules, audit logs
- `plot_gamma.py`, `gamma_trend.png`, `presentation.html` — figures and deck
- `certs/k{k}_{λ}/cert.json` — certificate metadata (λ = P/Q, scale constants, sha256, slack); vectors not tracked

## Trust

Floating point finds candidates; only exact or rigorously error-bounded checks count as proof. The mathematics is
Krasikov–Lagarias Theorem 2.2; the contribution here is the computation. The Lean results rest on Lean's three
standard axioms plus two named `native_decide` checks each, the same trust base as Mazur's 0.90.
