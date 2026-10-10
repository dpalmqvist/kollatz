"""Avenue 28 step 6 (2026-10-10): weighted l2 operator norms of the positive triple-majorant operator (level n-3 -> n),
with weights lambda^L_eff (L_eff = remaining 2-adic budget of the best 2-power representation k = 2^L u). Result: the
unweighted norm exceeds 1 from n = 11 (1.032 at n = 12); budget weights do not help (lambda = 0.9: 1.19, 0.8: 1.92 at
n = 12). The top singular vectors sit on the pure 2-power chain, and weighting it down lets its 26 far lifts per step
(cosine factors on 27th roots of unity, |Psi| ~ 0.3-0.5) blow up. See notes/limit_function.md, step 6.
  python weighted_majorant_norm.py NMIN NMAX [lambda ...]
"""
import sys
from math import comb
import numpy as np, scipy.sparse as sp, scipy.sparse.linalg as sla
p, q = 0.25, 0.75
CMAX = 70
Pc = np.array([comb(c - 1, 2) * p ** 3 * q ** (c - 3) if c >= 3 else 0.0 for c in range(CMAX + 1)])

def budget(m):
    """for all k mod 3^m: L* = argmin_L |centered(k 2^-L)| over L <= m log2 3, u* = that value; L_eff = L* - max(0, log2(2^L*|u*|/3^m))."""
    Mm = 3 ** m; kk = np.arange(Mm, dtype=np.int64); i2 = pow(2, -1, Mm)
    Lmax = int(m * np.log2(3)) + 1
    best = np.full(Mm, np.inf); Lb = np.zeros(Mm)
    x = kk.copy()
    for L in range(Lmax + 1):
        cv = np.abs(np.where(x > Mm // 2, x - Mm, x)).astype(float)
        better = cv < best
        best = np.where(better, cv, best); Lb = np.where(better, L, Lb)
        x = (x * i2) % Mm
    E = Lb + np.log2(np.maximum(best, 1)) - m * np.log2(3)
    return np.maximum(0.0, Lb - np.maximum(0.0, E))

def operator(n):
    M = 3 ** n; k = np.arange(M, dtype=np.int64); inv2 = pow(2, -1, M); Mp = 3 ** (n - 3)
    rows_idx = np.nonzero(k % 3 != 0)[0]; kk = k[rows_idx]
    rows, cols, vals = [], [], []
    cum3 = np.zeros(kk.size, complex); S1 = np.zeros(kk.size, complex); S13 = np.zeros(kk.size, complex); km = kk.copy()
    for t in range(1, CMAX + 1):
        km = (km * inv2) % M
        e1 = np.exp(2j * np.pi * km / M); e3 = np.exp(2j * np.pi * ((3 * km) % M) / M)
        S1p, S13p = S1.copy(), S13.copy(); cum3 += e3; S1 += e1; S13 += e1 * cum3
        c = t + 1
        if 3 <= c <= CMAX:
            rows.append(np.arange(kk.size)); cols.append((kk * pow(inv2, c, M)) % Mp)
            vals.append(Pc[c] * np.abs(cum3 * S1p - S13p) / comb(c - 1, 2))
    P = sp.csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(kk.size, Mp))
    P.sum_duplicates()
    colmask = np.nonzero(np.arange(Mp) % 3 != 0)[0]
    return P[:, colmask], rows_idx, colmask

lams = [float(x) for x in sys.argv[3:]] or [1.0, 0.95, 0.9, 0.8]
for n in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
    P, ridx, cidx = operator(n)
    Ln, Lp = budget(n)[ridx], budget(n - 3)[cidx]
    out = []
    for lam in lams:
        Wr = lam ** (Ln / 2); Wc = lam ** (-Lp / 2)
        A = sp.diags(Wr) @ P @ sp.diags(Wc)
        s = sla.svds(A, k=1, return_singular_vectors=False)[0]
        out.append(f"lam={lam}: {s:.4f}")
    print(f"n={n}: weighted l2 norm  " + "   ".join(out), flush=True)

