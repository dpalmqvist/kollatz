"""
Avenue 17, idea "lift the base case" (2026-10-09).

K-L Thm 2.2 proves phi_k^m(y) >= Delta c^m lam^y by induction on y from a base window of length nu = 2 at y = 0,
where phi >= 1 forces Delta <= 1/(lam^2 max c): capped classes (c = t) cost a factor t.  The induction can start at
any height Y: Delta_Y := min over m and y in [Y - 2, Y] of phi_k^m(y) / (c^m lam^y).  For y up to about k the counts
phi_k^m(y) = inf_a pi*_a(2^y a) are bounded below by the GUARANTEED tree of the class: predecessors 2n (always) and
(2n-1)/3 (iff n = 2 mod 3), decidable while the residue is known mod 3^(k-j) after j odd steps, i.e. for j <= k.
Values are bounded by a 2^e (2/3)^j (the odd step divides by 3 after doubling), so "path-max <= 2^y a" is implied by
the bound; the count is a rigorous lower bound for phi_k^m(y).  If the tree counts track c^m, Delta_Y stays O(1)
instead of 1/t and the spread penalty disappears from the explicit bound (at the price x >= a 2^Y).

  python base_lift.py K Y [LAM [VEC.npy]]   (Perron lambda_k by default; a fixed lambda with the bounded solution; or a given vector)
"""
import sys
import time

import numpy as np

import kl
import spread_iter

ALPHA = np.log2(3.0)
LAMBDA = {4: 1.6122870, 5: 1.6627590, 6: 1.6944520, 7: 1.7201900, 8: 1.7449630, 9: 1.7615320}


def guaranteed_counts(m, k, Y, step=0.25):
    """L(y) for y on a grid up to Y: number of guaranteed tree nodes of class m (mod 3^k) with path-max <= 2^y."""
    ys = np.arange(0, Y + 1e-9, step)
    counts = np.zeros(len(ys), dtype=np.int64)
    # DFS over (residue, modulus exponent, log2 value, log2 path-max)
    stack = [(m % 3 ** k, k, 0.0, 0.0)]
    while stack:
        r, kk, lv, pm = stack.pop()
        counts[ys >= pm - 1e-12] += 1
        # doubling child (always exists): value 2v, modulus unchanged
        lv2 = lv + 1.0
        if lv2 <= Y + 1e-12:
            stack.append(((2 * r) % 3 ** kk, kk, lv2, max(pm, lv2)))
        # odd child: exists iff r = 2 mod 3, decidable iff kk >= 1; value 2v/3 (upper bound), modulus drops by 3
        if kk >= 1 and r % 3 == 2:
            stack.append((((2 * r - 1) // 3) % 3 ** (kk - 1), kk - 1, lv + 1 - ALPHA, pm))
    return ys, counts


def main():
    k, Y = int(sys.argv[1]), float(sys.argv[2])
    S = kl.structure(k); N = S["N"]
    if len(sys.argv) > 4:                       # fixed lambda and a given (certified) vector
        lam = float(sys.argv[3]); c = np.load(sys.argv[4]).astype(np.float64); label = f"bounded lam={lam} from {sys.argv[4]}"
    elif len(sys.argv) > 3:
        lam = float(sys.argv[3]); c, _, _ = spread_iter.greatest_below(spread_iter.tstar(k, lam, S), lam, S); label = f"bounded lam={lam}"
    else:
        lam = LAMBDA[k]; c = kl.growth(lam, S, iters=200000, tol=1e-12)[2]; label = f"Perron lam_k={lam}"
    c = c / c.min(); t = c.max()
    print(f"k={k} {label}: max c = {t:.3f}, K-L Delta_1 = 1/(4 max c) = {1 / (4 * t):.4e}")
    t0 = time.time()
    ys, _ = guaranteed_counts(2, k, Y)
    L = np.zeros((N, len(ys)))
    for i in range(N):
        L[i] = guaranteed_counts(3 * i + 2, k, Y)[1]
    print(f"trees enumerated in {time.time() - t0:.0f}s; nodes at height Y: min {L[:, -1].min():.0f} max {L[:, -1].max():.0f}")
    ratio = L / (c[:, None] * lam ** ys[None, :])            # phi lower bound / (c lam^y)
    print(" Y    Delta_Y = min_m min_{y in [Y-2,Y]} L/(c lam^y)   argmin class (c value)   mean over m of L(Y)/(c lam^Y)   corr(log L(Y), log c)")
    for Yv in np.arange(2, Y + 1e-9, 1.0):
        w = (ys >= Yv - 2 - 1e-9) & (ys <= Yv + 1e-9)
        per_m = ratio[:, w].min(axis=1)
        i = int(per_m.argmin()); j = int(np.argmin(np.abs(ys - Yv)))
        print(f"{Yv:4.0f}   {per_m.min():.4e}                              {3 * i + 2:6d} (c={c[i]:.2f})        {ratio[:, j].mean():.4e}           {np.corrcoef(np.log(L[:, j]), np.log(c))[0, 1]:.3f}")


if __name__ == "__main__":
    main()
