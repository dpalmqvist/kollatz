"""
Avenue 19, first step: distribution of cycle numerators modulo 2^n - 3^k  (2026-10-09).

A cycle of length n with k odd steps and parity vector v (bit i = 1 iff step i is odd) has starting element
    x0 = N(v) / (2^n - 3^k),   N(v) = sum_{i: bit i set} 3^{o_i} 2^i,   o_i = number of set bits above i,
so a cycle exists iff N(v) == 0 (mod m), m = 2^n - 3^k > 0.  Heuristic count: binom(n, k)/m, summable in n.
Measured on the GPU for every v in [0, 2^n), grouped by k = popcount(v):
  * zeros(n, k) = #{v : N(v) == 0 mod m}  (expected binom(n, k)/m if equidistributed),
  * Weyl sums S_h = sum_v e(h N(v)/m) for h = 1..H, normalised by binom(n, k): equidistribution <=> S_h -> 0,
  * the normalised sums for k near theta*n are the ones that matter (large cycles need n/k ~ log2 3).
Output: cycle_numerators.json.      python cycle_numerators.py NMIN NMAX [H=8] [CHUNK_BITS=24]
"""
import json
import sys
import time

import numpy as np
import mlx.core as mx

NMIN, NMAX = int(sys.argv[1]), int(sys.argv[2])
H = int(sys.argv[3]) if len(sys.argv) > 3 else 8
CB = int(sys.argv[4]) if len(sys.argv) > 4 else 24

SRC = r"""
    uint64_t v = (uint64_t)start[0] + (uint64_t)thread_position_in_grid.x;
    uint64_t limit = (uint64_t)1 << NN;
    if (v >= limit) return;
    int k = popcount((uint32_t)v);
    uint64_t m = mtab[k];                 // 2^n - 3^k, or 0 if 3^k >= 2^n
    uint64_t acc = 0; int cnt = 0;
    if (m > 0) {
        for (int i = NN - 1; i >= 0; i--) {
            if ((v >> i) & 1) {
                uint64_t term = (p3[k * (NN + 1) + cnt] * p2[k * (NN + 1) + i]) % m;   // 3^cnt * 2^i mod m
                acc += term; if (acc >= m) acc -= m;
                cnt++;
            }
        }
    }
    kout[thread_position_in_grid.x] = k;
    rout[thread_position_in_grid.x] = (uint32_t)acc;
"""


def tables(n):
    m = np.zeros(n + 1, dtype=np.uint64); p2 = np.zeros((n + 1, n + 1), dtype=np.uint64); p3 = np.zeros((n + 1, n + 1), dtype=np.uint64)
    for k in range(n + 1):
        mm = (1 << n) - 3 ** k
        if mm <= 0:
            continue
        m[k] = mm
        for i in range(n + 1):
            p2[k, i] = pow(2, i, mm); p3[k, i] = pow(3, i, mm)
    return m, p2.ravel(), p3.ravel()


def run(n):
    m, p2, p3 = tables(n)
    kernel = mx.fast.metal_kernel(name=f"cyc{n}", input_names=["start", "mtab", "p2", "p3"], output_names=["kout", "rout"],
                                  header=f"#define NN {n}\n", source=SRC)
    chunk = min(1 << CB, 1 << n)
    mt, p2t, p3t = mx.array(m), mx.array(p2), mx.array(p3)
    from math import comb
    zeros = np.zeros(n + 1); cnt = np.zeros(n + 1)
    S = np.zeros((H, n + 1), dtype=np.complex128)
    mf = mx.array(np.where(m > 0, m, 1).astype(np.float64).astype(np.float32))
    for s in range(0, 1 << n, chunk):
        kk, rr = kernel(inputs=[mx.array([s], dtype=mx.uint64), mt, p2t, p3t], grid=(chunk, 1, 1), threadgroup=(256, 1, 1),
                        output_shapes=[(chunk,), (chunk,)], output_dtypes=[mx.int32, mx.uint32])
        valid = mx.array(m > 0)[kk]
        cnt += np.bincount(np.array(kk), minlength=n + 1)
        z = (rr == 0) & valid
        zeros += np.bincount(np.array(kk), weights=np.array(z.astype(mx.float32)), minlength=n + 1)
        frac = rr.astype(mx.float32) / mf[kk]                     # N/m in [0,1), ~2^-24 resolution
        for h in range(1, H + 1):
            ang = (2 * np.pi * h) * frac
            re = mx.zeros((n + 1,), dtype=mx.float32).at[kk].add(mx.cos(ang) * valid)
            im = mx.zeros((n + 1,), dtype=mx.float32).at[kk].add(mx.sin(ang) * valid)
            S[h - 1] += np.array(re).astype(np.float64) + 1j * np.array(im).astype(np.float64)
    out = {}
    for k in range(n + 1):
        if m[k] == 0:
            continue
        c = comb(n, k)
        out[k] = dict(m=int(m[k]), count=int(c), zeros=int(zeros[k]), expected_zeros=c / int(m[k]),
                      weyl=[float(abs(S[h - 1, k]) / c) for h in range(1, H + 1)])
    return out


res = {}
t0 = time.time()
for n in range(NMIN, NMAX + 1):
    t = time.time()
    r = run(n)
    res[n] = r
    kmax = max(r)                                    # largest admissible k: smallest modulus, the cycle-relevant regime
    kmid = max(r, key=lambda k: r[k]["count"])
    print(f"n={n:2d}: zeros total {sum(x['zeros'] for x in r.values())} (expected {sum(x['expected_zeros'] for x in r.values()):.2f}); "
          f"k={kmax} (m={r[kmax]['m']}, binom={r[kmax]['count']}): max_h|S_h|/binom = {max(r[kmax]['weyl']):.2e} vs 1/sqrt(binom) = {r[kmax]['count'] ** -0.5:.2e}; "
          f"k={kmid}: {max(r[kmid]['weyl']):.2e} vs {r[kmid]['count'] ** -0.5:.2e}  [{time.time() - t:.0f}s]", flush=True)
    json.dump(res, open("cycle_numerators.json", "w"), indent=1)
print("done", time.time() - t0)
