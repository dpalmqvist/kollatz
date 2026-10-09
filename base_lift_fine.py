"""
Avenue 17: lifted base case with FINER residues (2026-10-09).

phi_k^m(y) = inf over a = m (mod 3^k) of pi*_a(2^y a) = min over the finer classes m' = m (mod 3^k), m' mod 3^k',
of phi_k'^{m'}(y) >= min_{m'} L_k'(m', y), where L_k' is the guaranteed tree with k' decidable odd steps (base_lift.py).
Finer residues decide more odd steps, so the guaranteed trees track the true counts to greater heights and the base
constant Delta_Y = min_m min_{y in [Y-2, Y]} [min_{m' in m} L_k'(m', y)] / (c^m lam^y) can only increase with k'.
Vectorised level-synchronous BFS over all 3^(k'-1) fine classes at once.

  python base_lift_fine.py K KP Y [LAM VEC.npy [WORST KP_MAX]]   (LAM=perron VEC=- for the Perron vector)
"""
import sys
import time

import numpy as np

import kl
import spread_iter

ALPHA = np.log2(3.0)
LAMBDA = {4: 1.6122870, 5: 1.6627590, 6: 1.6944520, 7: 1.7201900, 8: 1.7449630, 9: 1.7615320, 10: 1.7771270,
          11: 1.7922310, 12: 1.8064236}
STEP = 0.25


def fine_counts(kp, Y, fine_ids=None):
    """L(m', y) for fine classes m' = 3i+2 mod 3^kp (all, or the given fine indices i), y on the grid: shape (n, ny)."""
    Np = 3 ** (kp - 1)
    ys = np.arange(0, Y + 1e-9, STEP); ny = len(ys)
    ids = np.arange(Np, dtype=np.int64) if fine_ids is None else np.asarray(fine_ids, dtype=np.int64)
    L = np.zeros((ids.size, ny), dtype=np.int64)
    # frontier arrays: class id (row), residue r, modulus exponent kk, log2 value lv, log2 path-max pm
    cid = np.arange(ids.size, dtype=np.int64); r = 3 * ids + 2; kk = np.full(ids.size, kp, dtype=np.int64)
    lv = np.zeros(ids.size); pm = np.zeros(ids.size)
    visited = 0
    while cid.size:
        # count this frontier: node counted for every y-bin >= pm
        b = np.searchsorted(ys, pm - 1e-12)              # first bin index with ys >= pm
        np.add.at(L, (cid, b), 1)                          # cumulative later
        visited += cid.size
        # doubling children
        keep = lv + 1.0 <= Y + 1e-12
        c1 = (cid[keep], (2 * r[keep]) % (3 ** kk[keep]), kk[keep], lv[keep] + 1.0, np.maximum(pm[keep], lv[keep] + 1.0))
        # odd children
        odd = (kk >= 1) & (r % 3 == 2)
        c2 = (cid[odd], ((2 * r[odd] - 1) // 3) % (3 ** (kk[odd] - 1)), kk[odd] - 1, lv[odd] + 1 - ALPHA, pm[odd])
        cid = np.concatenate([c1[0], c2[0]]); r = np.concatenate([c1[1], c2[1]]); kk = np.concatenate([c1[2], c2[2]])
        lv = np.concatenate([c1[3], c2[3]]); pm = np.concatenate([c1[4], c2[4]])
    L = np.cumsum(L, axis=1)                                # L(m', y) = nodes with pm <= y
    return ys, L, visited


def refine(k, kp0, Y, c, lam, worst, kp_max, ys, Lmin):
    """adaptively refine the `worst` coarse classes (smallest window ratio) to finer residues kp0+2, ..., kp_max."""
    N = c.size
    for kp in range(kp0 + 2, kp_max + 1, 2):
        ratio = Lmin / (c[:, None] * lam ** ys[None, :])
        best_per_Y = []
        for Yv in np.arange(2, Y + 1e-9, 1.0):
            w = (ys >= Yv - 2 - 1e-9) & (ys <= Yv + 1e-9)
            best_per_Y.append(ratio[:, w].min(axis=1))
        best_per_Y = np.array(best_per_Y)                     # (nY, N): Delta_Y per class
        score = best_per_Y.max(axis=0)                        # the class's best achievable Delta over Y
        sel = np.argsort(score)[:worst]                       # the classes limiting Delta_best
        fine = (sel[:, None] + N * np.arange(3 ** (kp - k))[None, :]).ravel()   # fine indices m' = m mod 3^k
        t0 = time.time()
        _, Lf, visited = fine_counts(kp, Y, fine)
        Lf = Lf.reshape(sel.size, -1, len(ys)).min(axis=1)    # min over fine classes inside each selected coarse class
        Lmin = Lmin.copy(); Lmin[sel] = np.maximum(Lmin[sel], Lf)
        print(f"  refined {worst} worst classes to k'={kp}: {visited:.2e} nodes, {time.time() - t0:.0f}s; "
              f"Delta_best now {np.array([ (Lmin / (c[:, None] * lam ** ys[None, :]))[:, (ys >= Yv - 2 - 1e-9) & (ys <= Yv + 1e-9)].min() for Yv in np.arange(2, Y + 1e-9, 1.0)]).max():.4f}", flush=True)
    return Lmin


def main():
    k, kp, Y = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3])
    S = kl.structure(k); N = S["N"]
    if len(sys.argv) > 5 and sys.argv[4] == "perron":
        lam = LAMBDA[k]; c = kl.growth(lam, S, iters=200000, tol=1e-12)[2]; label = f"Perron lam_k={lam}"
    elif len(sys.argv) > 5:
        lam = float(sys.argv[4]); c = np.load(sys.argv[5]).astype(np.float64); label = f"bounded lam={lam} from {sys.argv[5]}"
    elif len(sys.argv) > 4:
        lam = float(sys.argv[4]); c, _, _ = spread_iter.greatest_below(spread_iter.tstar(k, lam, S), lam, S); label = f"bounded lam={lam}"
    else:
        lam = LAMBDA[k]; c = kl.growth(lam, S, iters=200000, tol=1e-12)[2]; label = f"Perron lam_k={lam}"
    c = c / c.min(); t = c.max()
    t0 = time.time()
    ys, Lf, visited = fine_counts(kp, Y)
    Np = Lf.shape[0]
    coarse = (np.arange(Np) % N)                            # fine index i' -> coarse index i' mod 3^(k-1)  (m' mod 3^k)
    Lmin = np.full((N, len(ys)), np.iinfo(np.int64).max)
    np.minimum.at(Lmin, coarse, Lf)                         # min over fine classes inside each coarse class
    print(f"k={k} k'={kp} {label}: max c = {t:.3f}, Delta_1 = {1 / (4 * t):.4e}; {Np} fine classes, {visited:.2e} nodes, {time.time() - t0:.0f}s")
    if len(sys.argv) > 6:                                   # adaptive refinement: WORST classes to k'_max
        worst, kp_max = int(sys.argv[6]), int(sys.argv[7])
        Lmin = refine(k, kp, Y, c, lam, worst, kp_max, ys, Lmin)
    ratio = Lmin / (c[:, None] * lam ** ys[None, :])
    print(" Y   Delta_Y (fine)   argmin coarse class (c)   mean_m Lmin(Y)/(c lam^Y)")
    for Yv in np.arange(2, Y + 1e-9, 1.0):
        w = (ys >= Yv - 2 - 1e-9) & (ys <= Yv + 1e-9)
        per_m = ratio[:, w].min(axis=1); i = int(per_m.argmin()); j = int(np.argmin(np.abs(ys - Yv)))
        print(f"{Yv:3.0f}   {per_m.min():.4e}        {3 * i + 2:6d} ({c[i]:.2f})          {ratio[:, j].mean():.4e}")


if __name__ == "__main__":
    main()
