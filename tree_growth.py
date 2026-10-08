"""
Avenue 2: how fast do real predecessor trees grow, class by class, compared with the LP exponent?

For a residue class m mod 3^k pick integers a = m + t*3^k and compute pi*_a(x) exactly by backward BFS:
predecessors of n are 2n and (2n-1)/3 (when n = 2 mod 3; the result is automatically odd).  Every node stores
the maximum element on its path to a, so pi*_a(x) = #{nodes with path-max <= x} for all x <= X at once.
Fit the exponent of pi*_a(x) over [2^lo, X] and compare with gamma_k = log2(lambda_k) and with the LP weight c_m.

Scaling: x = a * 2^y (K-L's variable y), so trees of different a are compared over the same y-range;
the LP predicts pi*_a(a 2^y) >= Delta_1 * c_m * lambda_k^y, so counts / (c_m lambda^y) should be roughly
class-independent if the LP weights capture the class dependence.

  python tree_growth.py [k=9] [Y=22] [--classes 6] [--per-class 4] [--lo 10]
"""
import argparse
import glob
import math
import time

import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("k", type=int, nargs="?", default=9)
ap.add_argument("Y", type=int, nargs="?", default=22)
ap.add_argument("--classes", type=int, default=6)
ap.add_argument("--per-class", type=int, default=4)
ap.add_argument("--lo", type=int, default=10)
ap.add_argument("--random", type=int, default=2, help="extra random classes")
args = ap.parse_args()
k = args.k
M = 3 ** k
LAMBDA = {7: 1.7201900, 8: 1.7449630, 9: 1.7615320, 10: 1.7771270, 11: 1.7922310, 12: 1.8064236, 13: 1.8188237, 14: 1.8307723}
gamma_k = math.log2(LAMBDA[k])

# LP solution for the class weights c_m (index i <-> m = 3i+2)
from kl import structure, growth
S = structure(k)
lo_, hi_, c = growth(LAMBDA[k], S, iters=20000, tol=1e-11)
c = c / c.min()
order = np.argsort(c)
rng = np.random.default_rng(1)
picks = list(order[: args.classes // 2]) + list(order[-(args.classes - args.classes // 2):]) + list(rng.choice(len(c), args.random, replace=False))


def tree_counts(a):
    """pi*_a(a 2^y) for y = lo..Y, via BFS with path-max tracking (cap X = a 2^Y)."""
    X = a << args.Y
    nodes = np.array([a], dtype=np.int64)
    pmax = np.array([a], dtype=np.int64)
    all_pmax = [pmax]
    while nodes.size:
        even = 2 * nodes
        ok = even <= X
        n_even, p_even = even[ok], np.maximum(pmax[ok], even[ok])
        sel = nodes % 3 == 2
        odd = (2 * nodes[sel] - 1) // 3
        pm = pmax[sel]
        ok2 = (odd <= X) & (odd > 0)
        n_odd, p_odd = odd[ok2], np.maximum(pm[ok2], odd[ok2])
        nodes = np.concatenate([n_even, n_odd])
        pmax = np.concatenate([p_even, p_odd])
        all_pmax.append(pmax)
    pm = np.concatenate(all_pmax)
    ys = list(range(args.lo, args.Y + 1))
    return np.array([int((pm <= (a << y)).sum()) for y in ys]), ys


print(f"k={k}: lambda_k={LAMBDA[k]} gamma_k={gamma_k:.4f}; x = a 2^y, y up to {args.Y}; fit over y in [{args.lo}, {args.Y}]")
print(f"{'class i':>8} {'m':>8} {'c_m':>8} {'a':>10} {'pi*(a 2^Y)':>11} {'fit exp':>8} {'last oct':>9} {'count/(c_m lam^Y)':>18}")
t0 = time.time()
for i in picks:
    m = 3 * int(i) + 2
    exps = []
    for t in range(args.per_class):
        a = m + t * M
        counts, ys = tree_counts(a)
        ly = np.log2(np.maximum(counts, 1))
        slope = np.polyfit(ys, ly, 1)[0]
        local = ly[-1] - ly[-2]
        exps.append(slope)
        ratio = counts[-1] / (c[i] * LAMBDA[k] ** args.Y)
        print(f"{int(i):8d} {m:8d} {c[i]:8.3f} {a:10d} {counts[-1]:11d} {slope:8.4f} {local:9.4f} {ratio:18.4f}", flush=True)
    print(f"{'':8} class mean fit exponent {np.mean(exps):.4f}  (gamma_k = {gamma_k:.4f})   [{time.time()-t0:.0f}s]")
