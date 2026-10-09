"""
Avenue 17, first step: do the Krasikov-Lagarias inequalities admit feasible points of BOUNDED spread?  (2026-10-09)

Conjecture A (positive predecessor density) via K-L needs, besides lambda = 2, a solution c with max c / min c bounded:
the constant in Thm 2.2 is 1/(4 max c).  The Perron vector at lambda_k has C_max ~ 1.52^k.  But any feasible point
works, so ask the LP:   minimise t  s.t.  1 <= c_i <= t,  c_i <= lam^-2 c_{4i} + L_j c_{aux(i) + s N/3} (s = 0, 1, 2).
(The min over lifts is a conjunction of three linear constraints.)  Feasible iff lam <= lambda_k.  Measured: the
optimum t*(k, lam) for lam = lambda_k - delta and for fixed lam, against the Perron vector's spread.

  python spread_lp.py [KMAX=11]   -> spread_lp.json
"""
import json
import sys
import time

import numpy as np
import scipy.sparse as sp
from scipy.optimize import linprog

import kl

ALPHA = kl.ALPHA
LAMBDA = {5: 1.6627590, 6: 1.6944520, 7: 1.7201900, 8: 1.7449630, 9: 1.7615320, 10: 1.7771270, 11: 1.7922310,
          12: 1.8064236}
CMAX_PERRON = {5: 9.0756, 6: 12.8769, 7: 20.1964, 8: 29.1315, 9: 43.3394, 10: 64.9801, 11: 98.4010, 12: 147}


def solve(k, lam, S):
    N = S["N"]; n3 = N // 3
    q = lam ** -2
    L = {2: lam ** (ALPHA - 2), 5: 0.0, 8: lam ** (ALPHA - 1)}
    i = np.arange(N); nxt = S["nxt"]; cls = S["cls"]; aux = S["aux"]
    m5 = cls == 5; m28 = ~m5
    Lv = np.where(cls == 2, L[2], L[8])
    # class-5 rows: c_i - q c_nxt <= 0
    i5 = i[m5]; n5 = i5.size
    rows = [np.repeat(np.arange(n5), 2)]; cols = [np.stack([i5, nxt[i5]], 1).ravel()]; vals = [np.tile([1.0, -q], n5)]
    r = n5
    # classes 2, 8: three rows each
    i28 = i[m28]; n28 = i28.size
    for s_ in range(3):
        rr = r + np.arange(n28)
        rows.append(np.repeat(rr, 3)); cols.append(np.stack([i28, nxt[i28], aux[i28] + s_ * n3], 1).ravel())
        vals.append(np.stack([np.ones(n28), np.full(n28, -q), -Lv[i28]], 1).ravel())
        r += n28
    # c_i - t <= 0
    rr = r + i
    rows.append(np.repeat(rr, 2)); cols.append(np.stack([i, np.full(N, N)], 1).ravel()); vals.append(np.tile([1.0, -1.0], N))
    r += N
    rows, cols, vals = np.concatenate(rows), np.concatenate(cols), np.concatenate(vals)
    A = sp.csr_matrix((vals, (rows, cols)), shape=(r, N + 1))
    b = np.zeros(r)
    cobj = np.zeros(N + 1); cobj[N] = 1.0
    bounds = [(1.0, None)] * N + [(1.0, None)]
    res = linprog(cobj, A_ub=A, b_ub=b, bounds=bounds, method="highs")
    if res.status != 0:
        return None, None
    return float(res.x[N]), res.x[:N]


KMIN = int(sys.argv[2]) if len(sys.argv) > 2 else 5


def main(kmax):
    out = {}
    print(" k   lambda_k    lam        t* = min C_max   Perron C_max   (t*: bounded-spread optimum)")
    for k in range(KMIN, kmax + 1):
        S = kl.structure(k)
        out[k] = {}
        for label, lam in (("lam_k-1e-3", LAMBDA[k] - 1e-3), ("1.60", 1.60), ("1.65", 1.65), ("1.70", 1.70), ("1.75", 1.75),
                           ("1.78", 1.78), ("1.80", 1.80)):
            if lam > LAMBDA[k]:
                continue
            t = time.time()
            tstar, c = solve(k, lam, S)
            if tstar is None:
                print(f"{k:2d}  {LAMBDA[k]:.7f}  {lam:.5f}   infeasible"); continue
            n3 = S["N"] // 3
            cbar = np.minimum(np.minimum(c[:n3], c[n3:2 * n3]), c[2 * n3:])
            rho = cbar.mean() / c.mean()
            out[k][label] = dict(lam=lam, tstar=tstar, rho=float(rho), mean=float(c.mean()), frac_at_1=float((c < 1 + 1e-7).mean()), frac_at_t=float((c > tstar - 1e-7).mean()))
            print(f"{k:2d}  {LAMBDA[k]:.7f}  {lam:.5f}   {tstar:9.4f}        {CMAX_PERRON[k]:8.3f}     rho={rho:.4f} at1={out[k][label]['frac_at_1']:.2f} atT={out[k][label]['frac_at_t']:.2f} [{time.time() - t:.0f}s]", flush=True)
        json.dump(out, open(f"spread_lp_k{KMIN}_{kmax}.json", "w"), indent=1)


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 11)
