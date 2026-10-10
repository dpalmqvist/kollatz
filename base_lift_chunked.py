"""
Avenue 17/10 (2026-10-10): rigorous lifted base constant for a CERTIFIED vector, chunked over classes.

For a feasible c at lambda (certificate in certs/<dir>/c_f32.npy) the K-L induction (Thm 5.1 of [KL]) runs from any
base window [Y-2, Y], so for every a = m (mod 3^k), a = 2 (mod 3), not in a cycle (grid y_i = i*STEP below),
    pi_a(2^y a) >= phi_k^m(y) >= Delta_Y c^m lam^y   for all y >= Y - 2,
    Delta_Y = min_m min_{y in [Y-2, Y]} phi_k^m(y) / (c^m lam^y)
(base_lift.py). phi_k^m(y) >= L_m(y) = guaranteed-tree count (base_lift.fine_counts with k' = k). L_m is a step
function counted exactly on the grid y_i = i/4 (L_m(y_i) = nodes with path-max <= y_i); for y in [y_i, y_{i+1})
L_m(y) >= L_m(y_i) and lam^y <= lam^{y_{i+1}}, so the rigorous value is
    Delta_Y = min_m min_{i : [y_i, y_{i+1}) meets [Y-2, Y]} L_m(y_i) / (c^m lam^{y_{i+1}})
(the c used is c / min c, so c^m >= 1).  Then pi_a(x) >= Delta_Y (x/a)^{log2 lam} for x >= 2^{Y-2} a.
For a = 1 (mod 3): pi_a(x) >= pi_{2a}(x) >= Delta_Y (x/(2a))^{log2 lam}, i.e. one factor 1/lam and x >= 2^{Y-1} a.
Floating point: path maxima are e - j (alpha - 1) (e, j integers, j <= k <= 22) computed in float64, binned with a
1e-12 tolerance. For j <= 80, no value e - j (alpha - 1) lies within 2.5e-5 of a grid point i/16, i/32 or i/64
(checked with mpmath, 40 digits), so the binning is exact.

  python base_lift_chunked.py CERTDIR YMAX [CHUNK [STEP]]      (STEP = grid step in y, default 1/16)
"""
import json
import sys
import time

import numpy as np

import base_lift_fine
from base_lift_fine import fine_counts


def main():
    d, Y = sys.argv[1], float(sys.argv[2])
    chunk = int(sys.argv[3]) if len(sys.argv) > 3 else 20000
    step = float(eval(sys.argv[4])) if len(sys.argv) > 4 else 1 / 16
    base_lift_fine.STEP = step
    j = json.load(open(f"{d}/cert.json"))
    k = j["k"]; lam = j["lambda_P"] / j["lambda_Q"]
    c = np.load(f"{d}/c_f32.npy", mmap_mode="r").astype(np.float64).ravel()
    c = c / c.min()
    N = c.size; assert N == 3 ** (k - 1)
    ys = np.arange(0, Y + 1e-9, step)
    worst = np.full(len(ys) - 1, np.inf)            # min over classes of L(y_i) / (c lam^{y_{i+1}})
    arg = np.zeros(len(ys) - 1, dtype=np.int64)
    t0 = time.time(); nodes = 0
    for s in range(0, N, chunk):
        ids = np.arange(s, min(N, s + chunk))
        _, L, v = fine_counts(k, Y, ids)
        nodes += v
        r = L[:, :-1] / (c[ids, None] * lam ** ys[None, 1:])
        mi = r.min(axis=0); am = r.argmin(axis=0)
        upd = mi < worst
        worst[upd] = mi[upd]; arg[upd] = ids[am[upd]]
        if (s // chunk) % 10 == 0:
            print(f"  {s + len(ids)}/{N} classes, {nodes:.2e} nodes, {time.time() - t0:.0f}s", flush=True)
    print(f"{d}: k={k} lam={lam} gamma={np.log2(lam):.5f} max c/min c={c.max():.2f}; {nodes:.2e} nodes, {time.time() - t0:.0f}s")
    print(" Y   Delta_Y (rigorous)   argmin class m (c)   bound pi_a(x) >= Delta_Y (x/a)^gamma for x >= 2^(Y-2) a")
    best = (0, None)
    out = []
    for Yv in np.arange(2, Y + 1e-9, 0.25):
        sel = (ys[1:] > Yv - 2 + 1e-12) & (ys[:-1] <= Yv + 1e-12)
        dY = worst[sel].min(); i = int(arg[sel][worst[sel].argmin()])
        out.append(dict(Y=float(Yv), Delta=float(dY), argmin=int(3 * i + 2), c=float(c[i])))
        if abs(Yv - round(Yv)) < 1e-9:
            print(f"{Yv:4.1f}   {dY:.5f}            {3 * i + 2:9d} ({c[i]:.2f})")
        if dY > best[0]:
            best = (dY, Yv)
    print(f"best: Delta = {best[0]:.5f} at Y = {best[1]} -> pi_a(x) >= {best[0]:.4f} (x/a)^{np.log2(lam):.4f} for x >= 2^{best[1] - 2:g} a")
    json.dump(dict(cert=d, k=k, lam=lam, gamma=float(np.log2(lam)), Y=out, best=dict(Delta=best[0], Y=best[1])),
              open(f"base_lift_{d.strip('/').split('/')[-1]}.json", "w"), indent=1)


if __name__ == "__main__":
    main()
