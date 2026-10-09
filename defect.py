"""
Avenue 1: the coarse-graining defect D_k = R(F_k c_k) - F_{k-1}(R c_k)  (2026-10-09).

R(c) = min over the top ternary digit (= the auxiliary vector cbar, length N/3, a level-(k-1) vector).
For level-(k-1) index r and lift t, the level-k row r + t*N/3 reads
    F_k(c)_{r+tN/3} = lam^-2 c[lift_s(nxt(r))] + L_j cbar[lift_s'(aux(r))],
where (s, s') run over permutations of t.  Hence R(F_k c)_r >= lam^-2 cbar[nxt r] + L_j (R cbar)[aux r] =
F_{k-1}(cbar)_r, with equality iff the two argmins (x4 term, aux term) agree: D_k >= 0 pointwise and D_k is
exactly the x4/aux misalignment of renorm2.py.  At lam = lam_k, F_k c_k = c_k, so cbar = F_{k-1}(cbar) + D_k:
cbar is a strict super-solution at level k-1.  Taking means with the summation identity at level k-1,
    mean D_k = mean(R F c) - lam^-2 mean(cbar) - g(lam) mean(R^2 c),   g = (lam^(a-1) + lam^(a-2))/3,
so with F c = c:  delta_k := mean D / mean cbar = g(lam_k) (rho_k - rho'_k), rho'_k = mean(R^2 c)/mean(R c).
The mean defect is therefore the increment of the loss sequence (rho'_k ~ rho_{k-1}); the information beyond the
rho_k sequence lies in the pointwise structure of D (where the argmins disagree, how large the excess is, which
digits it depends on), which this script measures.

  python defect.py [KMAX=19]      -> defect.json, printed tables
"""
import json
import os
import sys
import time

import numpy as np

import kl

ALPHA = kl.ALPHA
LAMBDA = {6: 1.6944520, 7: 1.7201900, 8: 1.7449630, 9: 1.7615320, 10: 1.7771270, 11: 1.7922310,
          12: 1.8064236, 13: 1.8188237, 14: 1.8307723, 15: 1.8419687, 16: 1.8522346, 17: 1.8616888,
          18: 1.8703250, 19: 1.8783132, 20: 1.8857083, 21: 1.8925462}
CHUNK = 1 << 25


def load(k, prev):
    if k <= 11:
        c0 = None if prev is None else np.tile(prev, 3)
        c = kl.growth(LAMBDA[k], kl.structure(k), iters=200000, tol=1e-12, c0=c0)[2]
    else:
        c = np.load(f"c_k{k}_mlx.npy").reshape(-1).astype(np.float64)
    return c / c.mean()


def lifts_min(v):
    n = v.size // 3
    return np.minimum(np.minimum(v[:n], v[n:2 * n]), v[2 * n:])


def coeffs(lam):
    return lam ** -2, {0: lam ** (ALPHA - 2), 1: 0.0, 2: lam ** (ALPHA - 1)}   # by class i mod 3 (2, 5, 8 mod 9)


def aux_index(i, n_aux):
    """auxiliary index for level index i (i mod 3 = 0 -> 4j mod n_aux, = 2 -> 2j+1 mod n_aux; j = i // 3)."""
    j = i // 3
    a = np.where(i % 3 == 0, (4 * j) % n_aux, (2 * j + 1) % n_aux)
    return a


def apply_F(c, cbar, lam, out=None):
    """F_k(c) by the affine index formulas, chunked. cbar = lifts_min(c)."""
    N = c.size
    n3 = N // 3
    q, L = coeffs(lam)
    Lvec = np.array([L[0], L[1], L[2]])
    out = np.empty(N) if out is None else out
    for s in range(0, N, CHUNK):
        i = np.arange(s, min(N, s + CHUNK), dtype=np.int64)
        out[s:s + i.size] = q * c[(4 * i + 2) % N] + Lvec[i % 3] * cbar[aux_index(i, n3)]
    return out


def digit_means(v, k):
    """mean of v conditioned on each ternary digit j (0 = lowest) of the index, shape (k-2, 3) for a level-(k-1) vector."""
    n = v.size
    kk = int(round(np.log(n) / np.log(3))) + 1          # level of v
    out = []
    for j in range(kk - 1):
        out.append(v.reshape(3 ** (kk - 2 - j), 3, 3 ** j).mean(axis=(0, 2)).tolist())
    return out


def analyse(k, c, lam):
    N = c.size
    n3, n9 = N // 3, N // 9
    q, L = coeffs(lam)
    g = (L[0] + L[2]) / 3
    cbar = lifts_min(c)
    R2 = lifts_min(cbar)
    Fc = apply_F(c, cbar, lam)
    ratio = Fc / c
    lo, hi = ratio.min(), ratio.max()
    RFc = lifts_min(Fc)
    tstar = np.argmin(Fc.reshape(3, n3), axis=0)
    Fk1 = apply_F(cbar, R2, lam)                       # F_{k-1}(cbar), same lambda
    D = RFc - Fk1
    # decomposition at the minimising lift
    r = np.arange(n3, dtype=np.int64)
    i_star = r + tstar * n3
    E4 = q * (c[(4 * i_star + 2) % N] - cbar[(4 * r + 2) % n3])
    Lvec = np.array([L[0], L[1], L[2]])[r % 3]
    Ea = Lvec * (cbar[aux_index(i_star, n3)] - R2[aux_index(r, n9)])
    assert np.allclose(E4 + Ea, D, atol=1e-9 * c.mean()), "decomposition"
    assert D.min() > -1e-9, D.min()
    cls = r % 3
    eps = 1e-12
    out = dict(lam=lam, N=N, r_lo=float(lo), r_hi=float(hi),
               rho=float(cbar.mean() / c.mean()), rho2=float(R2.mean() / cbar.mean()),
               delta=float(D.mean() / cbar.mean()),
               delta_pred=float(g * (cbar.mean() / c.mean() - R2.mean() / cbar.mean())),
               delta_exact=float((RFc.mean() - q * cbar.mean() - g * R2.mean()) / cbar.mean()),
               E4_share=float(E4.sum() / D.sum()), Ea_share=float(Ea.sum() / D.sum()),
               frac_zero=float((D < eps).mean()),
               frac_zero_cls={int(cc): float((D[cls == cc] < eps).mean()) for cc in (0, 2)},
               mean_D_cls={int(cc): float(D[cls == cc].mean() / cbar.mean()) for cc in (0, 1, 2)},
               rel_quantiles={p: float(np.quantile(D / cbar, p)) for p in (0.5, 0.9, 0.99, 0.999, 1.0)},
               digit_means=digit_means(D / cbar.mean(), k))
    # spread of lifts of c at r vs defect
    spread = (c.reshape(3, n3).max(axis=0) - cbar) / c.reshape(3, n3).mean(axis=0)
    out["corr_D_spread"] = float(np.corrcoef(D, spread)[0, 1])
    # misalignment: argmin of x4 term vs argmin of aux term over the three lifts (classes 2, 8 only)
    i_all = r[:, None] + np.arange(3)[None, :] * n3                          # (n3, 3)
    a4 = np.argmin(c[(4 * i_all + 2) % N], axis=1)
    aa = np.argmin(cbar[aux_index(i_all.reshape(-1), n3)].reshape(n3, 3), axis=1)
    m = cls != 1
    out["argmin_agree"] = float((a4[m] == aa[m]).mean())
    return out


def main(kmax):
    res = {}
    if os.path.exists("defect.json"):
        res = {int(k): v for k, v in json.load(open("defect.json")).items()}
    prev = None
    print(" k   1-rho_k   1-rho'_k  delta_k   g(rho-rho')  delta/(1-rho)  zero%  E4%  agree  corr  r-gap")
    for k in range(6, kmax + 1):
        t = time.time()
        c = load(k, prev)
        prev = c
        if k in res:
            o = res[k]
        else:
            o = analyse(k, c, LAMBDA[k])
            res[k] = o
            json.dump(res, open("defect.json", "w"), indent=1)
        print(f"{k:2d}  {1 - o['rho']:.5f}  {1 - o['rho2']:.5f}  {o['delta']:.3e}  {o['delta_pred']:.3e}  "
              f"{o['delta'] / (1 - o['rho']):.4f}       {100 * o['frac_zero']:.1f}  {100 * o['E4_share']:.0f}  "
              f"{o['argmin_agree']:.3f}  {o['corr_D_spread']:+.3f}  {o['r_hi'] - o['r_lo']:.1e}  [{time.time() - t:.0f}s]",
              flush=True)


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 19)
