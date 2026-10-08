"""
Adaptive-tree experiment for L^NT_k (CLAUDE.md, idea 1), k = 14 by default.

Variables live on the leaves of a 3-adic tree over the index i in [0, N): a leaf at depth j is a class
i = a (mod 3^j).  A leaf vector c_leaf expands to c_full[i] = c_leaf[leaf(i)], and the tightest valid
leaf constraint is

    G(c_leaf)_l = min_{i in l} F(c_full)_i          (F = full-resolution right-hand side of L^NT_k)

G is monotone and 1-homogeneous, so r(G_lambda) >= 1 gives a feasible full solution of L^NT_k(lambda)
that is constant on every leaf.  Uniform depth k-2 reproduces lambda_{k-1} (G = F_{k-1} exactly),
uniform depth k-1 reproduces lambda_k.  The question: how much of the gain lambda_{k-1} -> lambda_k
survives when only a fraction of the depth-(k-2) cells is refined?

  python adaptive.py [k]        # writes adaptive_k{k}.json
"""
import json
import sys
import time

import numpy as np

from kl import F, structure

K = int(sys.argv[1]) if len(sys.argv) > 1 else 14
S = structure(K)
N = S["N"]
C_FULL = {14: "certs/k14_1.8307/C.npy", 13: "certs/k13_1.8188/C.npy", 12: "certs/k12_1.8064/c_f32.npy"}
LAMBDA = {10: 1.7771270, 11: 1.7922310, 12: 1.8064236, 13: 1.8188237, 14: 1.8307723, 15: 1.8419687}


class Tree:
    """Partition of [0, N) given by a leaf id per index."""

    def __init__(self, leaf_id):
        ids, inv = np.unique(leaf_id, return_inverse=True)
        self.leaf = inv.astype(np.int64)
        self.n = len(ids)
        self.perm = np.argsort(self.leaf, kind="stable")
        sorted_ids = self.leaf[self.perm]
        self.starts = np.flatnonzero(np.r_[True, sorted_ids[1:] != sorted_ids[:-1]])

    def expand(self, c_leaf):
        return c_leaf[self.leaf]

    def G(self, c_leaf, lam):
        Fc = F(self.expand(c_leaf), lam, S)
        return np.minimum.reduceat(Fc[self.perm], self.starts)

    def restrict_min(self, c_full):
        return np.minimum.reduceat(c_full[self.perm], self.starts)

    def restrict_mean(self, c_full):
        sums = np.add.reduceat(c_full[self.perm], self.starts)
        cnt = np.diff(np.r_[self.starts, N])
        return sums / cnt


def uniform(depth):
    return Tree(np.arange(N) % 3 ** depth)


def refined(base_depth, full_depth, refine_mask):
    """Cells a (mod 3^base_depth) with refine_mask[a] are split to depth full_depth."""
    i = np.arange(N)
    a = i % 3 ** base_depth
    key = np.where(refine_mask[a], 3 ** base_depth + i % 3 ** full_depth, a)
    return Tree(key)


def growth(tree, lam, c0, iters=100000, tol=1e-9):
    """Collatz-Wielandt bounds for r(G_lambda) by power iteration; returns lo, hi, c, iterations."""
    c = c0
    lo = hi = None
    best = np.inf
    stall = 0
    for it in range(1, iters + 1):
        Gc = tree.G(c, lam)
        ratio = Gc / c
        lo, hi = ratio.min(), ratio.max()
        c = Gc / Gc.min()
        gap = hi - lo
        if gap < tol:
            break
        if gap < best * (1 - 1e-3):
            best, stall = gap, 0
        else:
            stall += 1
            if stall > 200:          # float64 noise floor
                break
    return lo, hi, c, it


def lambda_tree(tree, c0, lo_lam, hi_lam, verbose=True):
    """Largest lambda with r(G_lambda) >= 1: secant on log r (r = mid of bounds) inside a bracket."""
    c = c0
    pts = []
    t0 = time.time()

    def f(lam):
        nonlocal c
        lo, hi, c, it = growth(tree, lam, c)
        v = np.log(0.5 * (lo + hi))
        if verbose:
            print(f"    lam={lam:.8f} log r={v:+.3e} gap={hi - lo:.1e} iters={it} [{time.time() - t0:.0f}s]", flush=True)
        return v

    a, b = lo_lam, hi_lam
    fa, fb = f(a), f(b)
    while fa < 0:                # bracket safety
        a -= 0.01; fa = f(a)
    while fb > 0:
        b += 0.01; fb = f(b)
    lam_prev, f_prev, lam_cur, f_cur = a, fa, b, fb
    for _ in range(12):
        lam_new = lam_cur - f_cur * (lam_cur - lam_prev) / (f_cur - f_prev)
        if not (a < lam_new < b):
            lam_new = 0.5 * (a + b)
        f_new = f(lam_new)
        if f_new >= 0:
            a, fa = lam_new, f_new
        else:
            b, fb = lam_new, f_new
        lam_prev, f_prev, lam_cur, f_cur = lam_cur, f_cur, lam_new, f_new
        if abs(lam_new - lam_prev) < 3e-7 or b - a < 1e-6:
            break
    # root estimate by linear interpolation of the final bracket
    lam_root = a + (b - a) * fa / (fa - fb) if fa != fb else a
    return lam_root, c


def run(name, tree, c_init_full, results, lo_lam, hi_lam):
    print(f"\n== {name}: {tree.n} leaves ({tree.n / N:.4f} of N)", flush=True)
    c0 = tree.restrict_mean(c_init_full)
    lam, c_leaf = lambda_tree(tree, c0, lo_lam, hi_lam)
    gam = float(np.log2(lam))
    results.append(dict(name=name, leaves=int(tree.n), leaf_frac=tree.n / N, lam=float(lam), gamma=gam))
    print(f"   -> lambda = {lam:.7f}  gamma = {gam:.5f}", flush=True)
    return lam, tree.expand(c_leaf)


if __name__ == "__main__":
    c_full = np.load(C_FULL[K]).astype(np.float64)              # oracle: exact solution at level K
    c_full /= c_full.min()
    lam_prev, lam_full = LAMBDA[K - 1], LAMBDA[K]
    results = []
    d = K - 2                                                     # depth of "top digit fixed" tree
    top3 = c_full.reshape(3, 3 ** d)                              # top3[t, a]: top digit t, low digits a

    # A. baselines
    run(f"uniform depth {d} (= k-1)", uniform(d), c_full, results, lam_prev - 2e-4, lam_prev + 2e-4)
    run(f"uniform depth {d + 1} (= k)", uniform(d + 1), c_full, results, lam_full - 2e-4, lam_full + 2e-4)

    # B. refine a fraction of depth-d cells to full depth, chosen by oracle spread of the 3 children
    spread = 1 - top3.min(axis=0) / top3.mean(axis=0)
    order = np.argsort(-spread)
    rng = np.random.default_rng(0)
    for frac in (0.05, 0.1, 0.25, 0.5, 0.75):
        mask = np.zeros(3 ** d, bool); mask[order[: int(frac * 3 ** d)]] = True
        run(f"refine top {frac:.0%} by spread", refined(d, d + 1, mask), c_full, results, lam_prev, lam_full)
    for frac in (0.25, 0.5):
        mask = np.zeros(3 ** d, bool); mask[rng.choice(3 ** d, int(frac * 3 ** d), replace=False)] = True
        run(f"refine random {frac:.0%}", refined(d, d + 1, mask), c_full, results, lam_prev, lam_full)

    # C. equal budget: base depth d-1, refine 1/4 of its cells two levels -> 3^d leaves (same count as uniform d)
    top9 = c_full.reshape(9, 3 ** (d - 1))
    spread9 = 1 - top9.min(axis=0) / top9.mean(axis=0)
    order9 = np.argsort(-spread9)
    for frac in (0.25, 0.5):
        mask = np.zeros(3 ** (d - 1), bool); mask[order9[: int(frac * 3 ** (d - 1))]] = True
        run(f"base depth {d - 1}, refine top {frac:.0%} two levels", refined(d - 1, d + 1, mask), c_full, results,
            LAMBDA[K - 2], lam_full)

    g0, g1 = np.log2(lam_prev), np.log2(lam_full)
    print(f"\n{'tree':45s} {'leaves/N':>9} {'lambda':>10} {'gamma':>8} {'gain captured':>13}")
    for r in results:
        r["gain_captured"] = (r["gamma"] - g0) / (g1 - g0)
        print(f"{r['name']:45s} {r['leaf_frac']:9.4f} {r['lam']:10.7f} {r['gamma']:8.5f} {r['gain_captured']:13.3f}")
    json.dump(dict(k=K, N=N, lambda_prev=lam_prev, lambda_full=lam_full, results=results),
              open(f"adaptive_k{K}.json", "w"), indent=1)
