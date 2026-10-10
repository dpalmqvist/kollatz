"""
Avenue 28, step 7 (2026-10-10): conditional (shared block sums) collision for nu_p.

Group the gaps a_j into blocks of length l, block sums c_i ~ NB(l, p). Given C = (c_1, c_2, ...), the law mu_C of
X = sum 3^(j-1) 2^-(a_1+..+a_j) is a CONVOLUTION of independent block laws (rotations 2^-(c_1+..+c_(i-1)) are fixed by C):
    X = sum_i 3^(l(i-1)) 2^-C_(i-1) V_i,   V_i = sum_(t=1..l) 3^(t-1) 2^-S_t (S_l = c_i), composition uniform.
Jensen: ||nu_m||_2^2 <= Gamma_m := E_C [ 3^m coll_m(mu_C) ] = sum_(xi level <= m) R(xi),
    R(xi) = E_c [ |beta_c^(xi)|^2 R(3^l 2^-c xi) ],   R(0) = 1,
all terms >= 0 (no cancellation needed). Identical-block (diagonal) factor per block: 3^l E[1/N(c)] = 4 (3/4)^l.

  python cond_collision.py L MMAX [p]   -> prints M_j = sum over level-j characters of R, and Gamma_m
"""
import sys
import time
from math import comb

import numpy as np


def run(l, mmax, p=0.25, cmax=None, chunk=1 << 15):
    q = 1 - p
    if cmax is None:
        mean, sd = l / p, np.sqrt(l * q) / p
        cmax = int(mean + 7 * sd) + 2
    cs = np.arange(l, cmax + 1)
    Pc = np.array([comb(int(c) - 1, l - 1) * p ** l * q ** (int(c) - l) for c in cs])
    tail = 1 - Pc.sum()
    Nc = np.array([comb(int(c) - 1, l - 1) for c in cs], dtype=float)
    R = {0: np.ones(1)}                                    # R[j] indexed by k mod 3^j (only 3 \nmid k used)
    out = []
    for j in range(1, mmax + 1):
        t0 = time.time()
        M = 3 ** j
        Rj = np.zeros(M)
        inv2 = pow(2, -1, M)
        # inv2^s mod 3^j for s = 0..cmax
        pw = np.ones(cmax + 1, dtype=np.int64)
        for s in range(1, cmax + 1):
            pw[s] = (pw[s - 1] * inv2) % M
        jl = j - l
        Rlow = R[max(jl, 0)]
        Ml = 3 ** max(jl, 0)
        ks_all = np.arange(M, dtype=np.int64)
        ks_all = ks_all[ks_all % 3 != 0]
        for st in range(0, len(ks_all), chunk):
            ks = ks_all[st:st + chunk]
            B = len(ks)
            F = np.zeros((B, cmax + 1), dtype=np.complex128)
            F[:, 0] = 1.0
            for t in range(1, l + 1):
                # phase e(k 3^(t-1) 2^-s / 3^j) for s = 0..cmax
                if t - 1 >= j:
                    ph = np.ones((B, cmax + 1))
                    ph = ph.astype(np.complex128)
                else:
                    num = (ks[:, None] * pw[None, :]) % M
                    num = (num * (3 ** (t - 1))) % M
                    ph = np.exp(2j * np.pi * num / M)
                cum = np.cumsum(F, axis=1)
                G = np.zeros_like(F)
                G[:, 1:] = cum[:, :-1] * ph[:, 1:]          # sum over s' < s
                F = G
            bhat = F[:, l:cmax + 1] / Nc[None, :]           # (B, len(cs))
            g = np.abs(bhat) ** 2
            if jl <= 0:
                Rn = np.ones((B, len(cs)))
            else:
                eta = (ks[:, None] * pw[None, cs]) % Ml      # 3^l 2^-c xi has numerator k 2^-c mod 3^(j-l)
                Rn = Rlow[eta]
            Rj[ks] = (g * Rn) @ Pc + tail * Rlow.max()         # tail c > cmax: g <= 1, R(eta) <= max R one block down
        R[j] = Rj
        Mj = Rj.sum()
        out.append((j, Mj))
        print(f"l={l} j={j:2d}  M_j={Mj:.6e}  ratio={Mj / out[-2][1] if len(out) > 1 else float('nan'):.4f}"
              f"  Gamma={1 + sum(x[1] for x in out):.5f}  maxR={Rj.max():.3e}  ({time.time() - t0:.1f}s)", flush=True)
    return out


if __name__ == "__main__":
    l = int(sys.argv[1]); mmax = int(sys.argv[2]); p = float(sys.argv[3]) if len(sys.argv) > 3 else 0.25
    print(f"diagonal factor per block 4(3/4)^l = {4 * 0.75 ** l:.4f}  (p=1/4)")
    run(l, mmax, p)
