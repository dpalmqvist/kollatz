"""Compare empirical predecessor densities d_a = pi_a(X)/X (pred_density.py) with the K-L vectors.
  python pred_compare.py [pred_density.json]"""
import json
import sys

import numpy as np

import kl
import spread_iter

J = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "pred_density.json"))
A = J["A"]; Xs = sorted(int(x) for x in J if x.isdigit())
X = Xs[-1]; pi = np.array(J[str(X)]["pi"], dtype=float); d = pi / X
a = np.arange(A)
print(f"X = 2^{int(np.log2(X))}; checkpoints {Xs}")
if len(Xs) > 1:
    p0 = np.array(J[str(Xs[-2])]["pi"], dtype=float) / Xs[-2]
    m = (a % 3 != 0) & (a > 0)
    rel = np.abs(d[m] - p0[m]) / d[m]
    print(f"convergence of d_a between X={Xs[-2]} and {X}: median rel. change {np.median(rel):.2e}, max {rel.max():.2e}")
m2 = (a % 3 == 2)
mass = d * a
print(f"d_a a over a = 2 mod 3, a < {A}: min {mass[m2].min():.3f} median {np.median(mass[m2]):.3f} max {mass[m2].max():.3f}; "
      f"d_a: min {d[m2].min():.2e} max {d[m2].max():.3f}")
LAM = {4: 1.6122870, 5: 1.6627590, 6: 1.6944520, 7: 1.7201900, 8: 1.7449630}
print(" k   N    corr(log class-mean of d_a a^gam, log c^m): Perron gam=gam_k | Perron gam=1 | bounded(1.60) gam=1 | spread emp (gam=1) vs Perron vs bounded")
prev = None
for k in range(4, 9):
    S = kl.structure(k); N = S["N"]
    cP = kl.growth(LAM[k], S, iters=200000, tol=1e-12, c0=None if prev is None else np.tile(prev, 3))[2]; prev = cP
    cP = cP / cP.min()
    cB, _, _ = spread_iter.greatest_below(spread_iter.tstar(k, 1.60, S), 1.60, S)
    cB = cB / cB.min()
    idx = ((a % 3 ** k) - 2) // 3                          # class index for a = 2 mod 3
    res = []
    for gam in (np.log2(LAM[k]), 1.0):
        v = d * a ** gam
        cm = np.zeros(N); cnt = np.zeros(N)
        np.add.at(cm, idx[m2], v[m2]); np.add.at(cnt, idx[m2], 1)
        cm /= cnt
        res.append((cm, np.corrcoef(np.log(cm), np.log(cP))[0, 1], np.corrcoef(np.log(cm), np.log(cB))[0, 1]))
    cm1 = res[1][0]
    print(f"{k:2d} {N:5d}   {res[0][1]:.3f}        {res[1][1]:.3f}        {res[1][2]:.3f}          "
          f"{cm1.max() / cm1.min():7.1f}  {cP.max():7.1f}  {cB.max():6.2f}")
