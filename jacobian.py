"""
Avenue 1: spectrum of the linearisation of F at its Perron vector.

F(c)_i = q c_{4i} + L_j cbar_{r(i)} with cbar_r = min over three lifts: piecewise linear.  At the Perron vector c
(where F(c) = r c with r = 1 at lambda_k) the derivative is the sparse matrix J with J[i, 4i] = q and
J[i, argmin lift] = L_j (the lift attaining the minimum; ties are measure zero).  Its leading eigenvalue is r;
the second eigenvalue modulus gives the mixing rate of the dynamics and is a candidate explanation for the
~0.92 per-level decay seen in 1 - rho_k and in the convergence of the mass marginals.

  python jacobian.py [kmax=11]
"""
import sys

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

from kl import ALPHA, growth, structure

LAMBDA = {5: 1.6627590, 6: 1.6944520, 7: 1.7201900, 8: 1.7449630, 9: 1.7615320, 10: 1.7771270, 11: 1.7922310,
          12: 1.8064236}
kmax = int(sys.argv[1]) if len(sys.argv) > 1 else 11

for k in range(5, kmax + 1):
    S = structure(k)
    N, n3 = S["N"], S["N"] // 3
    for lam, label in ((LAMBDA[k], "lambda_k"), (2.0, "lambda=2")):
        _, _, c = growth(lam, S, iters=100000, tol=1e-13)
        lifts = np.stack([c[:n3], c[n3:2 * n3], c[2 * n3:]])
        arg = lifts.argmin(axis=0)                      # which lift attains the min, per auxiliary index
        rows = [np.arange(N)]; cols = [S["nxt"]]; vals = [np.full(N, lam ** -2)]
        for cls, L in ((2, lam ** (ALPHA - 2)), (8, lam ** (ALPHA - 1))):
            s = np.where(S["cls"] == cls)[0]
            r = S["aux"][s]
            rows.append(s); cols.append(r + arg[r] * n3); vals.append(np.full(len(s), L))
        J = sp.csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(N, N))
        ev = spla.eigs(J, k=6, which="LM", return_eigenvectors=False, tol=1e-10, maxiter=20000)
        ev = sorted(ev, key=lambda z: -abs(z))
        # sanity: J c should equal F(c) = r c
        Jc = J @ c
        r_est = (Jc / c)
        print(f"k={k:2d} {label:9s} r=[{r_est.min():.6f},{r_est.max():.6f}]  |eig| = " +
              " ".join(f"{abs(z):.4f}" for z in ev[:6]) + f"   eig2/eig1 = {abs(ev[1])/abs(ev[0]):.4f}"
              f"   eig2 = {ev[1]:.4f}", flush=True)
