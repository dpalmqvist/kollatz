"""
Avenue 1: the top-digit boundary layer and the ceiling of the K-L method (2026-10-09).

(1) Ceiling.  With rho = mean(cbar)/mean(c) <= 1 the summed inequality caps lambda_k at the smallest root > 1 of
      3x+1:  (1 - lam^-2) = (1/3)(lam^(alpha-1) + lam^(alpha-2)) * rho
      5x+1:  (1 - lam^-4) = (1/5) lam^beta (lam^-1 + ... + lam^-4) * rho          (kl5.py)
    Factoring 1 - lam^-2 = (1 - 1/lam)(1 + 1/lam) etc., at rho = 1 both reduce EXACTLY to the Malthusian equation of
    the naive backward branching walk:  1/lam + lam^(log2 p - 1)/p = 1  (child 2a at +1, child (2a-1)/p at
    +1 - log2 p with probability 1/p).  3x+1: only root lam = 2 (gamma = 1).  5x+1: roots 1.5701677 and 2, so
    gamma_k(5) <= 0.650919 for every k -- Kontorovich-Lagarias's eta_{5,BP} (arXiv:0910.1944, Thm 8.10).
    Hence in BOTH systems lambda_k -> ceiling <=> rho_k -> 1, and 5x+1 is not a known "lambda_inf < ceiling" case.

(2) Boundary layer.  R(c) = min over the top ternary digit, renormalised to mean 1, is a vector on level k-1.
    Measured: R(c_k) ~ c_{k-1} (TV ~0.005, four times closer than c_k to tile(c_{k-1})), and the ball oscillation
    with d free top digits is ~ sum_{i<d} (1 - rho_{k-i}).  So beta(d) = log_3(S(d+1)/S(d)) with S the partial sums
    of the 1 - rho sequence; it is universal because 1 - rho_k is near-geometric in k.

  python boundary_layer.py [KMAX]      (default 17; k <= 11 recomputed with kl.py at Table-2 lambda)
"""
import glob
import os
import sys

import numpy as np
from scipy.optimize import brentq

import kl

ALPHA, BETA5 = np.log2(3.0), np.log2(5.0)
TABLE2 = {6: 1.6944520, 7: 1.7201900, 8: 1.7449630, 9: 1.7615320, 10: 1.7771270, 11: 1.7922310}


def ceiling():
    g3 = lambda l: (1 - l ** -2) - (l ** (ALPHA - 1) + l ** (ALPHA - 2)) / 3
    g5 = lambda l: (1 - l ** -4) - l ** BETA5 * sum(l ** -j for j in range(1, 5)) / 5
    m3 = lambda l: 1 / l + l ** (ALPHA - 1) / 3 - 1
    m5 = lambda l: 1 / l + l ** (BETA5 - 1) / 5 - 1
    for name, g, m in (("3x+1", g3, m3), ("5x+1", g5, m5)):
        L = np.linspace(1.01, 1.999, 5000)
        v = np.array([g(l) for l in L])
        roots = [brentq(g, L[i], L[i + 1]) for i in range(len(L) - 1) if v[i] * v[i + 1] < 0] + [2.0]
        lam = roots[0]
        print(f"{name}: smallest root of summed inequality at rho = 1: lam* = {lam:.7f}, gamma* = {np.log2(lam):.6f};"
              f"  Malthusian residual there {m(lam):+.1e}")


def load(k, prev):
    if k in TABLE2:                       # small k: recompute (only infeasibility certificates are stored)
        c0 = None if prev is None else np.tile(prev, 3)
        c = kl.growth(TABLE2[k] - 1e-7, kl.structure(k), iters=200000, tol=1e-11, c0=c0)[2]
    else:
        d = max((d for d in glob.glob(f"certs/k{k}_*") if not d.endswith("_upper")),
                key=lambda d: float(d.rsplit("_", 1)[1]))
        cands = [f"{d}/c_f32.npy", f"{d}/C.npy", f"c_k{k}_mlx.npy"]   # certificate vector, else lambda_k solution
        p = next(p for p in cands if os.path.exists(p))
        c = np.load(p).astype(np.float64).reshape(-1)
    return c / c.mean()


def R(c, d=1):
    """min over the top d ternary digits (index digit k-2 is axis 0 of reshape(3, N/3))."""
    m = c.reshape(3 ** d, -1).min(axis=0)
    return m / m.mean()


def ball_osc(c, D):
    return np.array([1 - c.reshape(3 ** d, -1).min(axis=0).mean() / c.mean() for d in range(1, D + 1)])


def main(kmax):
    ceiling()
    C, prev = {}, None
    for k in range(6, kmax + 1):
        C[k] = prev = load(k, prev)
    loss = {k: 1 - C[k].reshape(3, -1).min(axis=0).mean() for k in C}
    print("\n k   1-rho_k  | TV(R c_k, c_k-1)  TV(c_k, tile c_k-1) | TV(R^2 c_k, c_k-2)")
    for k in range(8, kmax + 1):
        tv = lambda a, b: 0.5 * np.abs(a - b).mean()
        print(f"{k:2d}  {loss[k]:.5f}  |   {tv(R(C[k]), C[k-1]):.4f}             {tv(C[k], np.tile(C[k-1], 3)):.4f}"
              f"          |   {tv(R(C[k], 2), C[k-2]):.4f}")
    D = 5
    lb = lambda o: -np.log(o[:-1] / o[1:]) / np.log(3)
    print(f"\nball oscillation with d free top digits vs partial sums of 1 - rho_(k-i), d = 1..{D}")
    for k in range(11, kmax + 1):
        osc = ball_osc(C[k], D)
        S = np.cumsum([loss[k - i] for i in range(D)])
        print(f"k={k:2d} osc  " + " ".join(f"{x:.4f}" for x in osc) + "   beta " + " ".join(f"{x:.3f}" for x in lb(osc)))
        print(f"      sum  " + " ".join(f"{x:.4f}" for x in S) + "   beta " + " ".join(f"{x:.3f}" for x in lb(S)))


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 17)
