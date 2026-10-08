"""
Avenue 1: where does the amplification A_k = s_(k+1) / ((3/4) s_k) come from?

At the fixed point c (level k+1, lambda = 2):  c_i = P_i + Q_i,  P_i = (1/4) c_{4i},  Q_i = L_j cbar_{r(i)}.
Top-digit sensitivity s(v) = 1 - mean(min over the 3 lifts of v)/mean(v).  Since min(P+Q) >= min P + min Q,
   mean min(P+Q) >= mean min P + mean min Q,  i.e.  s(c) <= (mean P * s(P) + mean Q * s(Q)) / mean c
with equality iff the argmins of P and Q over the top digit coincide everywhere.  The x4 term is a permutation
of classes, so s(P) = s(c) exactly; the aux term carries the injected variation.  Define the alignment
efficiency  e = [mean c * s(c) - mean Q * s(Q)] / [mean P * s(P)]  (fraction of the x4 term's variation that
survives in the sum).  A perfectly aligned fixed point would have e = 1 and A = 4/3 (no decay of 1 - r_k);
decay of 1 - r_k persists iff e stays below 1.

  python renorm2.py [kmax=15]
"""
import sys

import numpy as np

from kl import ALPHA, growth, structure

kmax = int(sys.argv[1]) if len(sys.argv) > 1 else 15


def sens(v):
    n3 = len(v) // 3
    return 1 - np.minimum(np.minimum(v[:n3], v[n3:2 * n3]), v[2 * n3:]).mean() / v.mean()


def argmin_top(v):
    n3 = len(v) // 3
    return np.stack([v[:n3], v[n3:2 * n3], v[2 * n3:]]).argmin(axis=0)


print(" k   s(c)    s(Q)    meanP/meanc  meanQ/meanc   e (alignment)   A=s(c)/(0.75 s_k)   argmin agreement P vs Q")
c_prev = None
for k in range(8, kmax + 1):
    S = structure(k)
    N, n3 = S["N"], N // 3 if False else S["N"] // 3
    c0 = None if c_prev is None else np.tile(c_prev, 3)
    _, _, c = growth(2.0, S, iters=200000, tol=1e-13, c0=c0)
    lam = 2.0
    P = c[S["nxt"]] / lam ** 2
    cbar = np.minimum(np.minimum(c[:n3], c[n3:2 * n3]), c[2 * n3:])
    Q = np.zeros(N)
    s2, s8 = S["cls"] == 2, S["cls"] == 8
    Q[s2] = lam ** (ALPHA - 2) * cbar[S["aux"][s2]]
    Q[s8] = lam ** (ALPHA - 1) * cbar[S["aux"][s8]]
    F = P + Q
    sc, sP, sQ = sens(F), sens(P), sens(Q)
    mP, mQ, mc = P.mean(), Q.mean(), F.mean()
    e = (mc * sc - mQ * sQ) / (mP * sP)
    agree = (argmin_top(P) == argmin_top(Q)).mean()
    A = sens(c) / (0.75 * sens(c_prev)) if c_prev is not None else float("nan")
    print(f"{k:2d}  {sc:.5f} {sQ:.5f}   {mP/mc:.4f}      {mQ/mc:.4f}      {e:.4f}          {A:.4f}            {agree:.4f}", flush=True)
    c_prev = c
