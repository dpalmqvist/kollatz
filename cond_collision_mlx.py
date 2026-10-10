"""
GPU (MLX) version of cond_collision.py: conditional (shared block sums) collision for nu_p, to deeper levels.
Same recursion  R(xi) = E_c[ |beta_c^(xi)|^2 R(3^l 2^-c xi) ],  M_j = sum_(level j) R,  Gamma_m = 1 + sum_(j<=m) M_j.
Extra diagnostics: fraction of M_j on characters k/3^j with |k/3^j| < delta (centred), per-block ratios.

  python cond_collision_mlx.py L MMAX [p]  -> cond_collision_L{L}.json
"""
import json
import sys
import time
from math import comb

import mlx.core as mx
import numpy as np


def run(l, mmax, p=0.25, chunk=1 << 18):
    q = 1 - p
    mean, sd = l / p, np.sqrt(l * q) / p
    cmax = int(mean + 9 * sd) + 2
    cs = np.arange(l, cmax + 1)
    Pc = np.array([comb(int(c) - 1, l - 1) * p ** l * q ** (int(c) - l) for c in cs])
    tail = max(0.0, 1 - Pc.sum())
    Nc = np.array([float(comb(int(c) - 1, l - 1)) for c in cs])
    wts = mx.array((Pc / Nc ** 2).astype(np.float32))          # P(c) / N(c)^2
    R = {0: np.ones(1, dtype=np.float32)}
    res = []
    for j in range(1, mmax + 1):
        t0 = time.time()
        M = 3 ** j
        inv2 = pow(2, -1, M)
        pw = [1]
        for s in range(1, cmax + 1):
            pw.append(pw[-1] * inv2 % M)
        tabs = [mx.array(np.array([(3 ** (t - 1) * pw[s]) % M if t - 1 < j else 0 for s in range(cmax + 1)],
                                  dtype=np.int64)) for t in range(1, l + 1)]
        jl = max(j - l, 0)
        Ml = 3 ** jl
        pwc = mx.array(np.array([pw[int(c)] % Ml for c in cs], dtype=np.int64))
        Rlow = mx.array(R[jl])
        rmax_low = float(R[jl].max())
        Rj = np.zeros(M, dtype=np.float32)
        for st in range(0, M, chunk):
            kn = np.arange(st, min(st + chunk, M), dtype=np.int64)
            kn = kn[kn % 3 != 0]
            if len(kn) == 0:
                continue
            k = mx.array(kn)
            B = len(kn)
            Fr = mx.zeros((B, cmax + 1)); Fi = mx.zeros((B, cmax + 1))
            Fr = mx.concatenate([mx.ones((B, 1)), Fr[:, 1:]], axis=1)
            for t in range(l):
                num = (k[:, None] * tabs[t][None, :]) % M
                ang = (num.astype(mx.float32) * (2 * np.pi / M))
                cr, ci = mx.cos(ang), mx.sin(ang)
                Sr = mx.cumsum(Fr, axis=1); Si = mx.cumsum(Fi, axis=1)
                Sr = mx.concatenate([mx.zeros((B, 1)), Sr[:, :-1]], axis=1)   # sum over s' < s
                Si = mx.concatenate([mx.zeros((B, 1)), Si[:, :-1]], axis=1)
                Fr, Fi = Sr * cr - Si * ci, Sr * ci + Si * cr
            g = Fr[:, l:] ** 2 + Fi[:, l:] ** 2                                # |F_l(c)|^2, c = l..cmax
            if j - l <= 0:
                Rn = mx.ones(g.shape)
            else:
                eta = (k[:, None] * pwc[None, :]) % Ml
                Rn = mx.take(Rlow, eta)
            val = (g * Rn) @ wts + tail * rmax_low
            mx.eval(val)
            Rj[kn] = np.array(val)
        R[j] = Rj
        Mj = float(Rj.astype(np.float64).sum())
        kk = np.arange(M)
        xc = np.minimum(kk, M - kk) / M
        fr = {d: float(Rj[(xc < d) & (kk % 3 != 0)].astype(np.float64).sum() / Mj) for d in (1e-1, 1e-2, 1e-3)}
        res.append(dict(j=j, M=Mj, frac_small_x=fr, maxR=float(Rj.max()), sec=time.time() - t0))
        rb = Mj / res[j - l - 1]["M"] if j > l else float("nan")
        print(f"l={l} j={j:2d} M_j={Mj:.5e} block_ratio={rb:.4f} Gamma={1 + sum(r['M'] for r in res):.5f} "
              f"frac|x|<.1/.01/.001={fr[0.1]:.3f}/{fr[0.01]:.4f}/{fr[0.001]:.5f} ({time.time() - t0:.1f}s)", flush=True)
        for jj in list(R):
            if 0 < jj < j - l + 1:
                del R[jj]
    json.dump(dict(l=l, p=p, levels=res), open(f"cond_collision_L{l}.json", "w"), indent=1)
    return res


if __name__ == "__main__":
    l = int(sys.argv[1]); mmax = int(sys.argv[2]); p = float(sys.argv[3]) if len(sys.argv) > 3 else 0.25
    print(f"identical-block factor per block 3^l E[1/N(c)] = 4(3/4)^l = {4 * 0.75 ** l:.4f} (p=1/4)")
    run(l, mmax, p)
