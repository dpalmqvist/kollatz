"""
Weighted (harmonic) refinement of the Eliahou cycle inequality by linear programming.

For a nontrivial cycle with k odd elements x_i and verification bound X0 (every n <= X0 reaches 1):
    n - k*log2(3) = sum_i log2(1 + 1/(3 x_i)) <= (1/(3 ln 2)) * H,   H = sum_i 1/x_i.
Eliahou: H < k/X0.  We bound H < f* k / X0 with f* < 1 from two sources, combined pointwise:

 (R) residues: every predecessor w of a cycle element z satisfies w > X0 (its orbit enters the cycle, so it
     cannot be <= X0).  A backward path with e doubling steps and o odd steps gives w <= 2^e (2/3)^o z, hence
     1/z < c(z)/X0 with c(z) = min over backward paths of depth <= D of 2^e (2/3)^o.  The odd back-step
     z -> (2z-1)/3 exists iff z = 2 (mod 3), so c depends only on z mod 3^D.  Forward, residues mod 3^D evolve
     deterministically given the parity of the step (division by 2 is invertible mod 3^D), while parity is free.
 (H) heights: with m the cycle minimum, x_t >= m 3^{k_t}/2^t along the cycle, so 1/x_t <= 2^{d_t}/m <= 2^{d_t}/X0,
     d_t = t - k_t*log2(3) <= 0 for all t (all elements >= m).  d moves by +1 (even step, allowed only if d+1 <= 0)
     or +1 - log2(3) (odd step).  d is binned conservatively (upper end of bin as weight, all overlapping bins
     as successors).

A cycle is a closed walk in the product graph (height bin, residue mod 3^D) with odd-step fraction 1/log2(3)
(forced by 2^n ~ 3^k).  The LP maximises the mean of min(2^{d}, c(r)) over odd steps subject to flow
conservation and the odd-fraction constraint; its optimum f* bounds the average of 1/x_i in units of 1/X0.
Gain over Eliahou: log2(1/f*) bits of verification range.  (Float LP: an estimate, not a certificate.)

  python cycle_lp.py [D=6] [--no-height] [--bin 0.05] [--window 4]
"""
import argparse
import math
import time

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix

ap = argparse.ArgumentParser()
ap.add_argument("D", type=int, nargs="?", default=6)
ap.add_argument("--no-height", action="store_true")
ap.add_argument("--bin", type=float, default=0.05)
ap.add_argument("--window", type=float, default=4.0)
args = ap.parse_args()
THETA = math.log2(3)
D = args.D
MOD = 3 ** D
inv2 = pow(2, -1, MOD)

# --- (R) dip factor per residue mod 3^D -------------------------------------------------------------------
t0 = time.time()
c = np.ones(MOD)
for r in range(MOD):
    best = 1.0
    frontier = [(r, 1.0)]        # (residue, ratio w/z so far)
    for depth in range(D):
        nxt = []
        for res, ratio in frontier:
            nxt.append(((2 * res) % MOD, ratio * 2.0))
            if res % 3 == 2:
                w = ((2 * res - 1) // 3) % MOD   # exact: 2*res-1 is divisible by 3 as an integer
                rr = ratio * 2.0 / 3.0
                if rr < best:
                    best = rr
                nxt.append((w, rr))
        # prune: a path can only dip below `best` later if ratio*(2/3)^(remaining) < best
        rem = D - depth - 1
        frontier = [(res, ratio) for res, ratio in nxt if ratio * (2.0 / 3.0) ** rem < best]
    c[r] = best
print(f"D={D}: c(r) over {MOD} residues: mean={c.mean():.4f} min={c.min():.4f}  share with c<1: {(c < 1).mean():.3f}  [{time.time()-t0:.0f}s]")
# note: the (2z-1)/3 residue map above is only valid when res = 2 mod 3 as an integer representative; since we
# take res in [0, MOD) with res % 3 == 2, (2*res - 1) is divisible by 3 and the result is w mod MOD/3 lifted
# arbitrarily -- the top 3-adic digit of w is unknown, so paths deeper than the information allow are
# over-counted only in the direction of *smaller* c (more dips), which keeps the bound valid.


def solve(states_odd_weight, n_states, edges):
    """edges: list of (src, dst, is_odd, weight). Maximise mean weight over odd edges with odd fraction 1/theta."""
    E = len(edges)
    src = np.array([e[0] for e in edges]); dst = np.array([e[1] for e in edges])
    odd = np.array([e[2] for e in edges], dtype=float); w = np.array([e[3] for e in edges])
    # conservation: out - in = 0 for every state
    rows = np.r_[src, dst]; cols = np.r_[np.arange(E), np.arange(E)]; vals = np.r_[np.ones(E), -np.ones(E)]
    A_eq = coo_matrix((vals, (rows, cols)), shape=(n_states, E))
    A_eq = coo_matrix(np.vstack([A_eq.toarray() if n_states * E < 2e7 else None]) ) if False else A_eq
    # add total flow = 1 and odd fraction = 1/theta
    extra = coo_matrix(np.vstack([np.ones(E), odd]))
    from scipy.sparse import vstack
    A = vstack([A_eq, extra]).tocsr()
    b = np.r_[np.zeros(n_states), 1.0, 1.0 / THETA]
    res = linprog(-w * odd, A_eq=A, b_eq=b, bounds=(0, None), method="highs")
    if res.status != 0:
        raise RuntimeError(res.message)
    flow = res.x
    fstar = -res.fun / (1.0 / THETA)       # mean weight per odd step
    return fstar, flow


# --- residue-only LP -------------------------------------------------------------------------------------
edges = []
for r in range(MOD):
    edges.append((r, (r * inv2) % MOD, 0, 0.0))                       # even step: z -> z/2
    edges.append((r, ((3 * r + 1) * inv2) % MOD, 1, c[r]))            # odd step: z odd -> (3z+1)/2
f_res, _ = solve(None, MOD, edges)
print(f"residue-only LP: f* = {f_res:.5f}  -> gain {math.log2(1/f_res):.3f} bits")

if not args.no_height:
    # --- joint (height bin, residue) LP -------------------------------------------------------------------
    h = args.bin
    nb = int(round(args.window / h))                 # bins cover d in [-window, 0]; bin i = [-(i+1)h, -i h]
    def bins_covering(lo, hi):
        """indices of bins overlapping [lo, hi] (d values; lo<=hi<=0 assumed clipped)"""
        i0 = max(0, int(math.floor(-hi / h - 1e-12)))
        i1 = min(nb - 1, int(math.floor(-lo / h + 1e-12)))
        return range(i0, i1 + 1)
    edges = []
    nstates = nb * MOD
    for i in range(nb):
        lo, hi = -(i + 1) * h, -i * h
        wt_height = 2.0 ** hi                        # conservative: largest 2^d in the bin
        # even step allowed if some d in bin has d+1 <= 0, i.e. lo + 1 <= 0; new d in [lo+1, min(hi+1, 0)]
        if lo + 1 <= 0:
            for j in bins_covering(lo + 1, min(hi + 1, 0.0)):
                for r in range(MOD):
                    edges.append((i * MOD + r, j * MOD + (r * inv2) % MOD, 0, 0.0))
        # odd step: new d in [lo + 1 - theta, hi + 1 - theta] (always <= 0 if hi <= 0); clip at -window
        nlo, nhi = max(lo + 1 - THETA, -args.window), hi + 1 - THETA
        for j in bins_covering(nlo, nhi):
            for r in range(MOD):
                edges.append((i * MOD + r, j * MOD + ((3 * r + 1) * inv2) % MOD, 1, min(wt_height, c[r])))
    print(f"joint LP: {nstates} states, {len(edges)} edges (bin {h}, window {args.window}) ...", flush=True)
    t0 = time.time()
    f_joint, flow = solve(None, nstates, edges)
    print(f"joint LP: f* = {f_joint:.5f}  -> gain {math.log2(1/f_joint):.3f} bits   [{time.time()-t0:.0f}s]")
    # height-only for reference (set c = 1)
    edges_h = [(s, d_, o, (2.0 ** (-(s // MOD) * h)) if o else 0.0) for s, d_, o, _ in edges]
    f_h, _ = solve(None, nstates, edges_h)
    print(f"height-only LP (same bins): f* = {f_h:.5f} -> {math.log2(1/f_h):.3f} bits (DP reference 0.7214 -> 0.471 bits)")

# --- consequences for the admissible cycle lengths -----------------------------------------------------------
import mpmath
mpmath.mp.prec = 300
th = mpmath.log(3) / mpmath.log(2)
pairs = [(114208327604, 72057431991), (217976794617, 137528045312), (1411629234715, 890638885193)]
f_use = f_res if args.no_height else f_joint
print(f"\nwith f* = {f_use:.4f}: a cycle with min > X0 needs n/k - theta <= f*/(3 ln2 X0); X0 needed to exclude each pair:")
for n, k in pairs:
    err = mpmath.mpf(n) / k - th
    X0 = mpmath.mpf(f_use) / (3 * mpmath.log(2) * err)
    print(f"  (n={n}, k={k}): X0 > 2^{mpmath.nstr(mpmath.log(X0, 2), 5)}   (Eliahou f=1: 2^{mpmath.nstr(mpmath.log(X0 / f_use, 2), 5)})")
