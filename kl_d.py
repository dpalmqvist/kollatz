"""
Avenue 3: the Krasikov-Lagarias LP for 3x+d, T_d(n) = n/2 (even), (3n+d)/2 (odd), gcd(d, 6) = 1.

Predecessors of a: 2a always; odd b = (2a-d)/3 when 2a = d (mod 3), i.e. a = -d (mod 3).  Index set: classes
m mod 3^k with m = -d (mod 3).  Two-step structure (b = (2m-d)/3):
  b = -d (mod 3)  <=>  m = -d (mod 9): term c_b with lambda^(alpha-1)           [d=1: m = 8 mod 9]
  b =  d (mod 3)  <=>  m = 2d (mod 9): term c_{2b} = c_{(4m-2d)/3} with lambda^(alpha-2)   [d=1: m = 2 mod 9]
  b =  0 (mod 3)  <=>  m = 5d (mod 9): no auxiliary term                        [d=1: m = 5 mod 9]
Claim: m = d*m' maps the d-system onto the d=1 system class by class, so lambda_k(d) = lambda_k(1) for all d.
This script builds the d-system directly (no reuse of the d=1 index formulas) and checks the claim numerically.

  python kl_d.py [kmax=7] [d ...]
"""
import sys

import numpy as np

ALPHA = np.log2(3.0)


def structure_d(k, d):
    M, Mk1 = 3 ** k, 3 ** (k - 1)
    base = (-d) % 3
    ms = np.arange(base, M, 3, dtype=np.int64)             # m = -d mod 3
    idx = {int(m): i for i, m in enumerate(ms)}
    N = len(ms)
    nxt = np.array([idx[int((4 * m) % M)] for m in ms])
    # auxiliary classes live mod 3^(k-1), again = -d mod 3; cbar_r = min over lifts r + t*3^(k-1)
    aux_ms = np.arange(base, Mk1, 3, dtype=np.int64)
    aidx = {int(r): i for i, r in enumerate(aux_ms)}
    lifts = np.array([[idx[int((r + t * Mk1) % M)] for t in range(3)] for r in aux_ms])
    kind = np.zeros(N, dtype=np.int8)                     # 1: alpha-1 term, 2: alpha-2 term, 0: none
    aux = np.full(N, -1, dtype=np.int64)
    for i, m in enumerate(ms):
        m = int(m)
        if m % 9 == (-d) % 9:
            kind[i] = 1
            aux[i] = aidx[((2 * m - d) // 3) % Mk1]
        elif m % 9 == (2 * d) % 9:
            kind[i] = 2
            aux[i] = aidx[((4 * m - 2 * d) // 3) % Mk1]
        else:
            assert m % 9 == (5 * d) % 9
    return dict(N=N, nxt=nxt, kind=kind, aux=aux, lifts=lifts)


def F_d(c, lam, S):
    cbar = c[S["lifts"]].min(axis=1)
    out = c[S["nxt"]] / lam ** 2
    k1, k2 = S["kind"] == 1, S["kind"] == 2
    out[k1] += lam ** (ALPHA - 1) * cbar[S["aux"][k1]]
    out[k2] += lam ** (ALPHA - 2) * cbar[S["aux"][k2]]
    return out


def lambda_k_d(k, d, tol=1e-9):
    S = structure_d(k, d)
    a, b = 1.0, 2.0
    c = np.ones(S["N"])
    while b - a > tol:
        lam = 0.5 * (a + b)
        for _ in range(20000):
            Fc = F_d(c, lam, S)
            r = Fc / c
            lo, hi = r.min(), r.max()
            c = Fc / Fc.min()
            if hi - lo < 1e-12:
                break
        if 0.5 * (lo + hi) >= 1:
            a = lam
        else:
            b = lam
    return 0.5 * (a + b)


if __name__ == "__main__":
    kmax = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    ds = [int(x) for x in sys.argv[2:]] or [1, 5, 7, 11, 13]
    TABLE2 = {2: 1.3534010, 3: 1.5275960, 4: 1.6122870, 5: 1.6627590, 6: 1.6944520, 7: 1.7201900, 8: 1.7449630}
    print("k  " + "  ".join(f"lambda_k(d={d:2d})" for d in ds) + "   K-L table (d=1)")
    for k in range(2, kmax + 1):
        vals = [lambda_k_d(k, d) for d in ds]
        print(f"{k:2d} " + "  ".join(f"{v:14.7f}" for v in vals) + f"   {TABLE2.get(k, float('nan')):.7f}")
