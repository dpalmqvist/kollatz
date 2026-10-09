"""
Avenue 8: the Krasikov–Lagarias predecessor system for 5x+1, as a calibration case for the
question lambda_k -> 2 on 3x+1.

T(n) = n/2 (n even), (5n+1)/2 (n odd).  Preimages of a: 2a always, and (2a-1)/5 iff a = 3 (mod 5).
Classes mod 5 (K-L style elimination of classes without an odd preimage):
  a = 0: only 2^j a       -> dropped (contributes O(y))
  a = 1: 2a = 2, 4a = 4, 8a = 3  (three doublings to a principal class)
  a = 2: 4a = 3;   a = 4: 2a = 3;   a = 3: principal.
Principal a = 3 (mod 5): 2a = 1, 4a = 2, 8a = 4, 16a = 3 and none of 2a, 4a, 8a has an odd preimage, so
  phi_a(y) >= phi_{16a}(y - 4) + phi_b(y - 1 + beta),   b = (2a-1)/5,  beta = log2 5,
and b mod 5 is fixed by a mod 25:
  a =  3 (25): b = 1 -> 8b principal: weight lam^(beta-4), class (16a-8)/5
  a =  8 (25): b = 3 principal:        weight lam^(beta-1), class (2a-1)/5
  a = 13 (25): b = 0 -> dropped
  a = 18 (25): b = 2 -> 4b principal:  weight lam^(beta-3), class (8a-4)/5
  a = 23 (25): b = 4 -> 2b principal:  weight lam^(beta-2), class (4a-2)/5
With the ansatz phi_a(y) >= c_a lam^y on residues mod 5^k (b known only mod 5^(k-1): minimum over 5 lifts):
  c_a <= lam^-4 c_{16a} + w_t cbar_r,   cbar_r = min_l c_{r + l 5^(k-1)},   c >= 1.
Indexing: a = 5i + 3, i in [0, N), N = 5^(k-1); t = i mod 5 <-> a mod 25 = 5t + 3; 16a -> (16i + 9) mod N;
auxiliary index (mod M = N/5): t = 0: (16i+5)/5,  t = 1: (2i-2)/5,  t = 3: (8i+1)/5,  t = 4: (4i-1)/5.
Warm start k-1 -> k: tile(c, 5).
Summed inequality (i -> 16i+9 and each i -> aux_t(i) are bijections):
  (1 - lam^-4) <= (1/5) lam^beta (lam^-1 + lam^-2 + lam^-3 + lam^-4) * rho,  rho = mean(cbar)/mean(c),
with equality at lam = 2, rho = 1: the same mass-conservation identity as for 3x+1.  So lam = 2 is formally
critical for 5x+1 too, although the predecessor exponent of 5x+1 is believed to be eta5 ~ 0.65
(Kontorovich-Lagarias, arXiv:0910.1944, Conj. 7.2; Volkov 0.678).
CORRECTED 2026-10-09: since rho <= 1, the summed inequality caps lambda_k(5) at its smallest root 1.5701677
(gamma 0.650919), which is exactly the branching-walk exponent eta_{5,BP} of Kontorovich-Lagarias (Thm 8.10):
at rho = 1 the equation factors to 1/lam + lam^(beta-1)/5 = 1.  So the heuristic predicts rho_k(5) -> 1 here too;
5x+1 is a second instance of the 3x+1 question, not a "lambda_inf < ceiling" case (boundary_layer.py, AVENUES §8).  (Lower bound logic as in K-L Thm 2.2; here used only numerically.)

Usage:
  python kl5.py check            # generic residue LP (HiGHS) for p = 3 vs K-L Table 2 and p = 5 vs the numpy map
  python kl5.py run [KMAX]       # lambda_k(5), gamma_k, rho_k for k = 2..KMAX (numpy float64) -> kl5.json
"""
import json
import sys
import time

import numpy as np

BETA = np.log2(5.0)
ALPHA = np.log2(3.0)
TABLE2 = {2: 1.3534010, 3: 1.5275960, 4: 1.6122870, 5: 1.6627590, 6: 1.6944520, 7: 1.7201900}


# ---------------------------------------------------------------- numpy map for 5x+1 (index formulas)
def structure5(k):
    N = 5 ** (k - 1)
    M = N // 5
    i = np.arange(N, dtype=np.int64)
    t = i % 5
    nxt = (16 * i + 9) % N
    aux = np.full(N, -1, dtype=np.int64)
    num = {0: 16 * i + 5, 1: 2 * i - 2, 3: 8 * i + 1, 4: 4 * i - 1}
    for tt, nm in num.items():
        s = t == tt
        assert np.all(nm[s] % 5 == 0)
        aux[s] = (nm[s] // 5) % M
    # each i -> aux_t(i) is a bijection {i = t mod 5} -> [0, M)
    for tt in num:
        assert len(np.unique(aux[t == tt])) == M
    assert len(np.unique(nxt)) == N
    return dict(N=N, M=M, t=t, nxt=nxt, aux=aux)


def weights5(lam):
    return {0: lam ** (BETA - 4), 1: lam ** (BETA - 1), 3: lam ** (BETA - 3), 4: lam ** (BETA - 2)}


def F5(c, lam, S):
    M = S["M"]
    cbar = c[:M].copy()
    for l in range(1, 5):
        np.minimum(cbar, c[l * M:(l + 1) * M], out=cbar)
    out = c[S["nxt"]] * lam ** -4
    w = weights5(lam)
    for tt, wt in w.items():
        s = S["t"] == tt
        out[s] += wt * cbar[S["aux"][s]]
    return out


def rho5(c, S):
    M = S["M"]
    cbar = c[:M].copy()
    for l in range(1, 5):
        np.minimum(cbar, c[l * M:(l + 1) * M], out=cbar)
    return float(cbar.mean() / c.mean())


def growth5(lam, S, c0=None, iters=100000, tol=1e-11, check=20, patience=10):
    c = np.ones(S["N"]) if c0 is None else c0
    best, stalled = np.inf, 0
    lo = hi = None
    for it in range(1, iters + 1):
        Fc = F5(c, lam, S)
        if it % check == 0:
            r = Fc / c
            lo, hi = float(r.min()), float(r.max())
            gap = hi - lo
            c = Fc / Fc.min()
            if gap < tol:
                break
            if gap < 0.99 * best:
                best, stalled = gap, 0
            else:
                stalled += 1
                if stalled >= patience:
                    break
        else:
            c = Fc / Fc.min()
    if lo is None:
        r = F5(c, lam, S) / c
        lo, hi = float(r.min()), float(r.max())
    return lo, hi, c


def lambda5(k, c0=None, lam0=1.45, lam1=1.55, width=1e-9, steps=40, verbose=False):
    """Secant on log r(F_lam) = 0, warm-started (kl_mlx.lambda_k)."""
    S = structure5(k)
    box = [c0]

    def f(lam):
        lo, hi, c = growth5(lam, S, c0=box.pop())
        box.append(c)
        if verbose:
            print(f"    lam={lam:.10f} lo={lo:.10f} hi={hi:.10f}", flush=True)
        return np.log(0.5 * (lo + hi)), hi - lo

    f0, _ = f(lam0)
    f1, gap = f(lam1)
    slope = (f1 - f0) / (lam1 - lam0)
    for _ in range(steps):
        if f1 == f0:
            break
        lam2 = lam1 - f1 * (lam1 - lam0) / (f1 - f0)
        lam2 = min(max(lam2, 1.0), 2.0)
        if abs(lam2 - lam1) < max(width, 0.5 * gap / abs(slope)):
            break
        lam0, f0 = lam1, f1
        lam1 = lam2
        f1, gap = f(lam1)
    return lam1, box.pop(), S


# ---------------------------------------------------------------- generic residue LP (independent of the formulas)
def build_lp(p, k):
    """Rows of the eliminated K-L system for px+1 (p = 3 or 5) built by following the map on residues:
    principal a (odd preimage exists: 2a = 1 mod p), even chain 2a, 4a, ... until principal again
    (e doublings: weight lam^-e), odd preimage b = (2a-1)/p mod p^(k-1) followed by d doublings until principal
    (weight lam^(log2 p - 1 - d)) or dropped if b hits 0 mod p.  Returns variable lists and rows."""
    P, Pk1 = p ** k, p ** (k - 1)
    princ = [a for a in range(P) if (2 * a) % p == 1]
    princ_r = [r for r in range(Pk1) if (2 * r) % p == 1]
    ci = {a: i for i, a in enumerate(princ)}
    ri = {r: len(princ) + i for i, r in enumerate(princ_r)}
    rows = []
    for a in princ:
        x, e = (2 * a) % P, 1
        while (2 * x) % p != 1:
            x, e = (2 * x) % P, e + 1
        b = ((2 * a - 1) // p) % Pk1          # 2a - 1 = 0 mod p exactly
        d = 0
        while b % p != 0 and (2 * b) % p != 1:
            b, d = (2 * b) % Pk1, d + 1
        rows.append((a, e, x, None if b % p == 0 else (b, d)))
    lifts = [(r, (r + l * Pk1) % P) for r in princ_r for l in range(p)]
    for r, lift in lifts:
        assert lift in ci
    return princ, princ_r, ci, ri, rows, lifts


def lp_feasible(p, k, lam, B):
    from scipy.optimize import linprog
    from scipy.sparse import coo_matrix
    princ, princ_r, ci, ri, rows, lifts = B
    lp2 = np.log2(p)
    I, J, V = [], [], []
    for n, (a, e, x, odd) in enumerate(rows):
        I += [n, n]; J += [ci[a], ci[x]]; V += [1.0, -lam ** -e]
        if odd is not None:
            b, d = odd
            I.append(n); J.append(ri[b]); V.append(-lam ** (lp2 - 1 - d))
    n0 = len(rows)
    for n, (r, lift) in enumerate(lifts):
        I += [n0 + n, n0 + n]; J += [ri[r], ci[lift]]; V += [1.0, -1.0]
    nvar = len(princ) + len(princ_r)
    A = coo_matrix((V, (I, J)), shape=(n0 + len(lifts), nvar)).tocsr()
    bounds = [(1.0, None)] * len(princ) + [(0.0, None)] * len(princ_r)
    res = linprog(np.zeros(nvar), A_ub=A, b_ub=np.zeros(A.shape[0]), bounds=bounds, method="highs")
    return res.status == 0


def lambda_lp(p, k, lo=1.0, hi=2.0, tol=1e-8):
    B = build_lp(p, k)
    while hi - lo > tol:
        mid = 0.5 * (lo + hi)
        if lp_feasible(p, k, mid, B):
            lo = mid
        else:
            hi = mid
    return lo, len(B[0])


def check():
    print("generic residue LP, p = 3, against K-L Table 2:")
    for k in range(2, 7):
        t = time.time()
        lam, n = lambda_lp(3, k)
        print(f"  k={k} N={n:5d} lambda_LP={lam:.8f} table={TABLE2[k]:.7f} diff={lam - TABLE2[k]:+.1e} {time.time() - t:.1f}s", flush=True)
    print("generic residue LP, p = 5, against the numpy map (index formulas):")
    c = None
    for k in range(2, 7):
        t = time.time()
        lam_lp_, n = lambda_lp(5, k)
        t1 = time.time()
        lam_np, c, S = lambda5(k, c0=None if c is None else np.tile(c, 5))
        print(f"  k={k} N={n:5d} lambda_LP={lam_lp_:.8f} ({t1 - t:.1f}s)  numpy={lam_np:.8f} ({time.time() - t1:.1f}s) "
              f"diff={lam_np - lam_lp_:+.1e}", flush=True)


def run(kmax):
    out = {}
    c = None
    lam_prev = None
    print(f"{'k':>2} {'N':>10} {'lambda_k(5)':>12} {'gamma_k':>9} {'rho_k':>9} {'1-rho':>9} {'ratio':>7} {'time':>7}")
    prev = None
    for k in range(2, kmax + 1):
        t = time.time()
        c0 = None if c is None else np.tile(c, 5)
        starts = {} if lam_prev is None else dict(lam0=lam_prev + 0.004, lam1=lam_prev + 0.008)
        lam, c, S = lambda5(k, c0=c0, **starts)
        rho = rho5(c, S)
        g = float(np.log2(lam))
        one = 1 - rho
        ratio = one / prev if prev else float("nan")
        prev = one
        lam_prev = lam
        print(f"{k:2d} {S['N']:10d} {lam:12.8f} {g:9.6f} {rho:9.6f} {one:9.6f} {ratio:7.4f} {time.time() - t:6.1f}s", flush=True)
        out[k] = dict(N=int(S["N"]), lam=float(lam), gamma=g, rho=rho, Cmax=float(c.max() / c.min()))
        with open("kl5.json", "w") as f:
            json.dump(out, f, indent=1)


if __name__ == "__main__":
    if sys.argv[1] == "check":
        check()
    else:
        run(int(sys.argv[2]) if len(sys.argv) > 2 else 10)
