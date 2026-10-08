"""
Avenue 1: renormalisation of top-digit sensitivity across levels.

Top-digit sensitivity of a level-k vector:  s(c) = 1 - mean(min over the three lifts) / mean(c) = 1 - rho.
Step 1: lift c_k to level k+1 by tiling (no top-digit dependence, s = 0).
Step 2: apply F_{k+1} once.  The lift-selection mechanism injects top-digit variation:  s1 = s(F(tile c_k)).
Step 3: iterate to the fixed point c_{k+1}: s_{k+1} = s(c_{k+1}).
Report s_k, s1, s_{k+1}, and the ratios s1/s_k (injection efficiency) and s_{k+1}/s1 (amplification by the fixed
point).  The product is the per-level ratio of 1 - rho_k seen in the data (~0.92).  Also at lambda = 2.

  python renorm.py [kmax=13]
"""
import sys

import numpy as np

from kl import F, growth, structure

LAMBDA = {8: 1.7449630, 9: 1.7615320, 10: 1.7771270, 11: 1.7922310, 12: 1.8064236, 13: 1.8188237, 14: 1.8307723}
kmax = int(sys.argv[1]) if len(sys.argv) > 1 else 13


def sens(c):
    n3 = len(c) // 3
    return 1 - np.minimum(np.minimum(c[:n3], c[n3:2 * n3]), c[2 * n3:]).mean() / c.mean()


def digit_sens(c, k):
    """sensitivity to each digit j = 0..k-2 (j = k-2 is the top)."""
    mean = c.mean()
    return np.array([1 - c.reshape(3 ** (k - 2 - j), 3, 3 ** j).min(axis=1).mean() / mean for j in range(k - 1)])


for lam_mode in ("lambda_k", "lambda=2"):
    print(f"== {lam_mode}")
    print(" k      s_k  s1=s(F tile c_k)  s_(k+1)  s1/s_k  s_(k+1)/s1  s_(k+1)/s_k  digit-profile ratio s_(k+1)(j)/s_k(j), j = 0..k-2")
    for k in range(8, kmax):
        S1, S2 = structure(k), structure(k + 1)
        lam1 = LAMBDA[k] if lam_mode == "lambda_k" else 2.0
        lam2 = LAMBDA[k + 1] if lam_mode == "lambda_k" else 2.0
        _, _, ck = growth(lam1, S1, iters=100000, tol=1e-13)
        tiled = np.tile(ck, 3)
        f1 = F(tiled, lam2, S2)
        _, _, ck1 = growth(lam2, S2, iters=100000, tol=1e-13, c0=tiled)
        sk, s1, sk1 = sens(ck), sens(f1), sens(ck1)
        pk, pk1 = digit_sens(ck, k), digit_sens(ck1, k + 1)
        ratios = pk1[: k - 1] / pk
        print(f"{k:2d} {sk:8.5f} {s1:17.5f} {sk1:8.5f} {s1/sk:7.4f} {sk1/s1:10.4f} {sk1/sk:11.4f}  " +
              " ".join(f"{x:.3f}" for x in ratios), flush=True)
