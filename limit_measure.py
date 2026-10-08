"""
Avenue 1: does the K-L solution converge to a limit object as k -> infinity, and what is it?

(A) Mass convergence.  mu_k(class) = c_m / sum c is a probability measure on residue classes mod 3^k, i.e. on
    3-adic balls of radius 3^-(k-1) in the index i.  Its marginal on balls of radius 3^-j (sum over the high
    digits) can be compared between consecutive k.  TV_j(k) = total variation between the level-j marginals of
    mu_k and mu_{k+1}.  Convergence of a limit measure <=> TV_j(k) -> 0 for every fixed j.

(B) Shape at lambda = 2.  F_lambda at lambda = 2 has spectral radius < 1 for finite k, but the normalised power
    iteration still converges to its Perron vector.  Compare it with c_k (Perron vector at lambda_k): TV distance
    of the normalised masses, correlation of log c, and the digit-sensitivity profile.  If the shapes agree, the
    limit object is the lambda = 2 eigenmeasure of the 3-adic operator, which is the natural object for a proof.

  python limit_measure.py            (uses certs/ for (A), recomputes small k for (B))
"""
import glob
import os

import numpy as np

from kl import growth, structure

LAMBDA = {8: 1.7449630, 9: 1.7615320, 10: 1.7771270, 11: 1.7922310, 12: 1.8064236, 13: 1.8188237, 14: 1.8307723}


def load(k):
    d = glob.glob(f"certs/k{k}_*")[0]
    p = f"{d}/c_f32.npy" if os.path.exists(f"{d}/c_f32.npy") else f"{d}/C.npy"
    return np.load(p).astype(np.float64).reshape(-1)


def marginal(c, k, j):
    """mass on balls fixing the low j digits of the index: shape (3^j,)"""
    return c.reshape(3 ** (k - 1 - j), 3 ** j).sum(axis=0) / c.sum()


def digit_profile(c, k):
    mean = c.mean()
    return np.array([1 - c.reshape(3 ** (k - 2 - j), 3, 3 ** j).min(axis=1).mean() / mean for j in range(k - 1)])


print("(A) total variation between level-j marginals of mu_k and mu_{k+1}")
ks = list(range(12, 19))
print("   k ->k+1 |", " ".join(f"j={j:2d}  " for j in range(1, 9)))
for k in ks:
    c1, c2 = load(k), load(k + 1)
    row = []
    for j in range(1, 9):
        row.append(0.5 * np.abs(marginal(c1, k, j) - marginal(c2, k + 1, j)).sum())
    print(f"  {k:2d}->{k+1:2d} |", " ".join(f"{x:.1e}" for x in row))
print("  (ratio of successive rows at j=4:)", end=" ")
tv4 = [0.5 * np.abs(marginal(load(k), k, 4) - marginal(load(k + 1), k + 1, 4)).sum() for k in ks]
print(" ".join(f"{tv4[i+1]/tv4[i]:.3f}" for i in range(len(tv4) - 1)))

print("\n(B) Perron vector at lambda = 2 versus c_k at lambda_k")
for k in (8, 10, 12, 13):
    S = structure(k)
    _, _, ck = growth(LAMBDA[k], S, iters=50000, tol=1e-12)
    lo, hi, c2 = growth(2.0, S, iters=50000, tol=1e-12)
    ck, c2 = ck / ck.min(), c2 / c2.min()
    tv = 0.5 * np.abs(ck / ck.sum() - c2 / c2.sum()).sum()
    corr = np.corrcoef(np.log(ck), np.log(c2))[0, 1]
    pk, p2 = digit_profile(ck, k), digit_profile(c2, k)
    print(f"  k={k}: r(F_2) in [{lo:.5f},{hi:.5f}]  Cmax/Cmin: {ck.max():.1f} vs {c2.max():.1f}  TV={tv:.4f}  corr(log c)={corr:.5f}")
    print(f"        digit profile 1-rho_j  lambda_k: {' '.join(f'{x:.3f}' for x in pk)}")
    print(f"                               lambda=2: {' '.join(f'{x:.3f}' for x in p2)}")
    print(f"        top-layer Hoelder beta (d=1..4) lambda_k: {' '.join(f'{-np.log(pk[i+1]/pk[i])/np.log(3):.3f}' for i in range(k-6, k-2))}"
          f"   lambda=2: {' '.join(f'{-np.log(p2[i+1]/p2[i])/np.log(3):.3f}' for i in range(k-6, k-2))}")
