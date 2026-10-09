"""
Avenue 1: the x4 weight a_m = lam^-2 c(4m)/c(m) and the spread of log c, by level (2026-10-09).

At the Perron vector c = F(c), so a in (0, 1] and the auxiliary weight is b = 1 - a (a = 1 on class 5 mod 9).
The spread of a within a class is the "polarisation" that weakens the per-level contraction of the loss (AVENUES
§1, popdyn.py); whether it saturates in k is what decides q_inf heuristically.  Chunked (memmap), so k = 20, 21 run
on the 4.6 / 13 GB warm-start vectors; k <= 11 recomputed with kl.py.  Output: weights_stats.json and a table.

  python weights.py [KMAX=21]
"""
import json
import sys
import time

import numpy as np

import kl

LAMBDA = {8: 1.7449630, 9: 1.7615320, 10: 1.7771270, 11: 1.7922310, 12: 1.8064236, 13: 1.8188237, 14: 1.8307723,
          15: 1.8419687, 16: 1.8522346, 17: 1.8616888, 18: 1.8703250, 19: 1.8783132, 20: 1.8857083, 21: 1.8925462}
CHUNK = 1 << 24


def stats(c, lam):
    """c: 1-D array-like (memmap ok), any dtype. Returns dict of moments of a by class, E[a^2], E[b^2], log-c spread."""
    N = c.size
    acc = {cls: np.zeros(3) for cls in (0, 1, 2)}          # sum a, sum a^2, count  per class (i mod 3)
    wsum = np.zeros(2)                                     # magnitude-weighted sum of a^2 and (1-a)^2 (weights c)
    lsum = np.zeros(3)                                     # sum log c, sum log^2 c, sum c
    for s in range(0, N, CHUNK):
        i = np.arange(s, min(N, s + CHUNK), dtype=np.int64)
        ci = np.asarray(c[s:s + i.size], dtype=np.float64)
        tgt = (4 * i + 2) % N
        ct = np.asarray(c[tgt], dtype=np.float64)
        a = lam ** -2 * ct / ci
        cls = i % 3
        for k_ in (0, 1, 2):
            m = cls == k_
            acc[k_] += [a[m].sum(), (a[m] ** 2).sum(), m.sum()]
        wsum += [(ci * a ** 2).sum(), (ci * (1 - a) ** 2).sum()]
        lc = np.log(ci)
        lsum += [lc.sum(), (lc ** 2).sum(), ci.sum()]
    tot = sum(acc[k_] for k_ in (0, 1, 2))
    Ea, Ea2 = tot[0] / tot[2], tot[1] / tot[2]
    Eb2 = 1 - 2 * Ea + Ea2
    out = dict(N=int(N), Ea=Ea, Ea2=Ea2, Eb2=Eb2, q_naive=float(np.sqrt(Eb2 / (1 - Ea2))))
    for k_, name in ((0, "cls2"), (2, "cls8")):
        m1, m2 = acc[k_][0] / acc[k_][2], acc[k_][1] / acc[k_][2]
        out[f"mean_a_{name}"] = m1
        out[f"std_a_{name}"] = float(np.sqrt(max(m2 - m1 ** 2, 0)))
    Ea2w, Eb2w = wsum / lsum[2]
    out["q_naive_weighted"] = float(np.sqrt(Eb2w / (1 - Ea2w)))
    ml = lsum[0] / N
    out["std_log_c"] = float(np.sqrt(lsum[1] / N - ml ** 2))
    return out


def main(kmax):
    res = {}
    prev = None
    print(" k    E[a]   std a cls2  std a cls8   q_naive  q_naive_w  std(log c)")
    for k in range(8, kmax + 1):
        t = time.time()
        if k <= 11:
            S = kl.structure(k)
            c = kl.growth(LAMBDA[k], S, iters=200000, tol=1e-12, c0=None if prev is None else np.tile(prev, 3))[2]
            prev = c
        else:
            c = np.load(f"c_k{k}_mlx.npy", mmap_mode="r").reshape(-1)
        o = stats(c, LAMBDA[k])
        res[k] = o
        print(f"{k:2d}  {o['Ea']:.4f}   {o['std_a_cls2']:.4f}      {o['std_a_cls8']:.4f}      {o['q_naive']:.4f}   "
              f"{o['q_naive_weighted']:.4f}     {o['std_log_c']:.4f}   [{time.time() - t:.0f}s]", flush=True)
        json.dump(res, open("weights_stats.json", "w"), indent=1)


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 21)
