"""
Avenue 17: minimal spread t*(k, lam) by monotone iteration instead of an LP (2026-10-09).

For fixed t the set {c : 1 <= c <= t, c <= F(c)} is nonempty iff the decreasing iteration
    c_0 = t,  c_{n+1} = min(t, F(c_n))
converges to a fixed point with min c >= 1 (F monotone, so c_n decreases to the GREATEST feasible point below t).
Bisection on t gives t*(k, lam) = the smallest admissible spread.  Validated against spread_lp.py at k <= 9; scales
to k ~ 16 in numpy (float64) and beyond with the Metal kernel of kl_mlx.

  python spread_iter.py [--slack=1e-5] K LAM [LAM ...]     -> prints t*, appends to spread_iter.json, saves spread_c_k{K}_{LAM}.npy
"""
import json
import os
import sys
import time

import numpy as np

import kl

ALPHA = kl.ALPHA


SLACK = 0.0        # with SLACK = s > 0 the map is (1 - s) F: the fixed point then satisfies c <= (1 - s) F(c), i.e. has
                   # relative slack s in every row, which the integer certifier (certify_fast.py) needs.


def greatest_below(t, lam, S, c0=None, tol=1e-10, iters=100000):
    """greatest fixed point of c -> min(t, (1 - SLACK) F(c)) below t; returns (c, min c, iterations)."""
    c = np.full(S["N"], float(t)) if c0 is None else np.minimum(c0, t)
    for it in range(1, iters + 1):
        new = np.minimum(t, (1.0 - SLACK) * kl.F(c, lam, S))
        d = (c - new).max()
        c = new
        if d < tol * t:
            break
        if c.min() < 1.0 - 1e-9:        # already infeasible: iteration only decreases
            break
    return c, c.min(), it


def tstar(k, lam, S, hi=None, rel=1e-4, verbose=False):
    lo = 1.0
    if hi is None:
        hi = 4.0
        while True:
            c, m, it = greatest_below(hi, lam, S)
            if m >= 1.0 - 1e-9:
                break
            lo, hi = hi, hi * 2
            if hi > 1e6:
                return None
    c_hi = c
    while hi - lo > rel * hi:
        mid = 0.5 * (lo + hi)
        c, m, it = greatest_below(mid, lam, S, c0=c_hi)
        if verbose:
            print(f"    t={mid:.5f} min c={m:.6f} iters={it}", flush=True)
        if m >= 1.0 - 1e-9:
            hi, c_hi = mid, c
        else:
            lo = mid
    np.save(f"spread_c_k{k}_{lam}" + (f"_s{SLACK:g}" if SLACK else "") + ".npy", c_hi.astype(np.float32))   # feasible point, spread <= hi
    return hi


if __name__ == "__main__":
    if sys.argv[1].startswith("--slack="):
        SLACK = float(sys.argv[1].split("=")[1]); sys.argv.pop(1)
    k = int(sys.argv[1]); lams = [float(x) for x in sys.argv[2:]]
    S = kl.structure(k)
    res = json.load(open("spread_iter.json")) if os.path.exists("spread_iter.json") else {}
    for lam in lams:
        t0 = time.time()
        ts = tstar(k, lam, S)
        res[f"{k}_{lam}" + (f"_s{SLACK:g}" if SLACK else "")] = dict(k=k, lam=lam, slack=SLACK, tstar=ts, seconds=time.time() - t0)
        print(f"k={k} lam={lam:.4f} t*={ts}  [{time.time() - t0:.0f}s]", flush=True)
        json.dump(res, open("spread_iter.json", "w"), indent=1)
