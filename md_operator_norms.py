"""
Avenue 28, step 3 (2026-10-10): operator norms of the level-raising map K on ARBITRARY martingale differences.

The level-r densities of the stationary measure nu_p obey h_r = K h_(r-1), and their martingale differences
delta_r = h_r - h_(r-1) obey delta_r = K delta_(r-1), with
  K f(c) = sum_j 3p (1-p)^j [2^j c = 2, 8 (9)] f((2^(j+1) c - 1)/3),
mapping functions on the units mod 3^L to functions on the units mod 3^(L+1). This script computes, for p = 1/4,
the Haar-normalised L2 norm of K^m restricted to martingale differences at level L (mean zero over the top digit),
matrix-free with svds.

Result (2026-10-10): ||K|| -> 1.0356 > 1 (stable from L = 6), so there is no one-step contraction. The m-step norms
are below 1 at finite L but grow with L (m = 2: 0.889 / 0.907 / 0.919 at L = 11 / 12 / 13; m = 3: 0.816 at L = 12),
so no level-uniform contraction certificate exists for arbitrary martingale differences. The decay of the actual
delta_r (0.65 per level) is a property of their arithmetic structure, not of K.

  python md_operator_norms.py M LMAX [LMIN]
"""
import sys
import time

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as sla

p, q = 0.25, 0.75
J = 90
def Kmat(L):
    M1, M0 = 3 ** (L + 1), 3 ** L
    c = np.arange(M1, dtype=np.int64); c = c[c % 3 != 0]
    u0 = np.arange(M0, dtype=np.int64); u0 = u0[u0 % 3 != 0]
    idx0 = -np.ones(M0, dtype=np.int64); idx0[u0] = np.arange(u0.size)
    rows, cols, vals = [], [], []
    x = c.copy()
    for j in range(J):
        b = (x % 9 == 2) | (x % 9 == 8)
        rows.append(np.nonzero(b)[0]); cols.append(idx0[((2 * x[b] - 1) // 3) % M0]); vals.append(np.full(b.sum(), 3 * p * q ** j))
        x = (2 * x) % M1
    K = sp.csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(c.size, u0.size))
    K.sum_duplicates(); return K, u0
def proj(u0, M0):
    base = u0 % (M0 // 3)
    _, inv = np.unique(base, return_inverse=True)
    def P(f):
        s = np.bincount(inv, weights=f) / 3.0
        return f - s[inv]
    return P
m, Lmax = int(sys.argv[1]), int(sys.argv[2])
Lmin = int(sys.argv[3]) if len(sys.argv) > 3 else 2
for L in range(Lmin, Lmax + 1):
    t0 = time.time()
    Ks = [Kmat(L + t)[0] for t in range(m)]
    _, u0 = Kmat(L)
    P = proj(u0, 3 ** L)
    n0, n1 = u0.size, Ks[-1].shape[0]
    KT = [K.T.tocsr() for K in Ks]
    def mv(f):
        f = P(np.asarray(f).ravel())
        for K in Ks: f = K @ f
        return f
    def rmv(g):
        g = np.asarray(g).ravel()
        for K in reversed(KT): g = K @ g
        return P(g)
    op = sla.LinearOperator((n1, n0), matvec=mv, rmatvec=rmv, dtype=float)
    s = sla.svds(op, k=1, return_singular_vectors=False, tol=1e-6)[0] * np.sqrt(n0 / n1)
    print(f"m={m} L={L:2d}: ||K^m|| = {s:.4f}, per step {s ** (1 / m):.4f}   ({time.time()-t0:.0f} s)", flush=True)
