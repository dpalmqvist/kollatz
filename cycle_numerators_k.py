"""
Avenue 19, step 2 (2026-10-10): cycle numerators N(v) mod m = 2^n - 3^k for a FIXED k (k near k_max), n up to 40.

Same quantities as cycle_numerators.py (zeros = #{v : N(v) = 0 mod m}, Weyl sums S_h = sum_v e(h N(v)/m) / binom(n, k))
but enumerating only the binom(n, k) parity vectors of weight k: each GPU thread unranks one k-subset in colex
order (combinatorial number system) and steps through B successors with Gosper's hack.  N(v) = sum over set bits
i (high to low) of T[cnt][i] = 3^cnt 2^i mod m, cnt = number of set bits above i (host table, so no 128-bit
products); h N mod m is exact in uint64 (m < 2^41, h <= 8), only the final phase is float32.  Per-thread partial
sums are float32 over B terms and are summed on the host in float64.

  python cycle_numerators_k.py NMIN NMAX [DK=0,1,2] [H=8] [B=2048]    (DK: offsets below k_max)
Validation: for n <= 32 the results must equal cycle_numerators.json (all-vector enumeration).
"""
import json
import math
import sys
import time

import numpy as np
import mlx.core as mx

NMIN, NMAX = int(sys.argv[1]), int(sys.argv[2])
DKS = [int(x) for x in sys.argv[3].split(",")] if len(sys.argv) > 3 else [0, 1, 2]
H = int(sys.argv[4]) if len(sys.argv) > 4 else 8
B = int(sys.argv[5]) if len(sys.argv) > 5 else 2048

SRC = r"""
    uint tid = thread_position_in_grid.x;
    uint64_t r = (uint64_t)start[0] + (uint64_t)tid * (uint64_t)BB;      // colex rank of the first subset
    uint64_t total = (uint64_t)tot[0];
    float re[HH], im[HH];
    for (int h = 0; h < HH; h++) { re[h] = 0.0f; im[h] = 0.0f; }
    uint zc = 0;
    if (r < total) {
        // unrank: largest c with binom(c, j) <= r, for j = KK .. 1
        uint64_t v = 0; uint64_t rr = r; int c = NN - 1;
        for (int j = KK; j >= 1; j--) {
            while (binom[c * (KK + 1) + j] > rr) c--;
            v |= ((uint64_t)1 << c); rr -= binom[c * (KK + 1) + j]; c--;
        }
        uint64_t mm = mtab[0];
        float mf = (float)mm;
        uint64_t steps = total - r; if (steps > (uint64_t)BB) steps = (uint64_t)BB;
        for (uint64_t s = 0; s < steps; s++) {
            uint64_t acc = 0; int cnt = 0;
            uint64_t w = v;
            while (w) {
                int i = 63 - clz(w);
                acc += T[cnt * NN + i]; if (acc >= mm) acc -= mm;
                cnt++; w &= ~((uint64_t)1 << i);
            }
            if (acc == 0) zc++;
            for (int h = 0; h < HH; h++) {
                uint64_t x = ((uint64_t)(h + 1) * acc) % mm;
                float ang = 6.283185307179586f * ((float)x / mf);
                re[h] += cos(ang); im[h] += sin(ang);
            }
            // Gosper: next larger integer with the same popcount
            uint64_t t = v | (v - 1);
            v = (t + 1) | (((~t & (t + 1)) - 1) >> (ctz(v) + 1));
        }
    }
    zout[tid] = zc;
    for (int h = 0; h < HH; h++) { sout[tid * 2 * HH + 2 * h] = re[h]; sout[tid * 2 * HH + 2 * h + 1] = im[h]; }
"""


def run(n, k):
    m = (1 << n) - 3 ** k
    assert m > 0 and m < (1 << 61)
    T = np.zeros((k, n), dtype=np.uint64)
    for cnt in range(k):
        for i in range(n):
            T[cnt, i] = (pow(3, cnt, m) * pow(2, i, m)) % m
    bt = np.zeros((n, k + 1), dtype=np.uint64)
    for c in range(n):
        for j in range(k + 1):
            bt[c, j] = math.comb(c, j)
    total = math.comb(n, k)
    kernel = mx.fast.metal_kernel(name=f"cyck{n}_{k}", input_names=["start", "tot", "mtab", "T", "binom"],
                                  output_names=["zout", "sout"],
                                  header=f"#define NN {n}\n#define KK {k}\n#define HH {H}\n#define BB {B}\n", source=SRC)
    threads = 1 << 20
    per_launch = threads * B
    zeros = 0; S = np.zeros(H, dtype=np.complex128)
    Tm, bm, mm, tt = mx.array(T.ravel()), mx.array(bt.ravel()), mx.array([m], dtype=mx.uint64), mx.array([total], dtype=mx.uint64)
    for s in range(0, total, per_launch):
        z, so = kernel(inputs=[mx.array([s], dtype=mx.uint64), tt, mm, Tm, bm], grid=(threads, 1, 1), threadgroup=(256, 1, 1),
                       output_shapes=[(threads,), (threads * 2 * H,)], output_dtypes=[mx.uint32, mx.float32])
        zeros += int(np.array(z).astype(np.int64).sum())
        so = np.array(so).astype(np.float64).reshape(threads, H, 2).sum(axis=0)
        S += so[:, 0] + 1j * so[:, 1]
    return dict(m=m, count=total, zeros=zeros, expected_zeros=total / m, weyl=[float(abs(x) / total) for x in S],
                weyl_times_sqrt=[float(abs(x) / math.sqrt(total)) for x in S], m_over_2n=m / 2 ** n)


def main():
    out = {}
    try:
        out = json.load(open("cycle_numerators_k.json"))
    except Exception:
        pass
    for n in range(NMIN, NMAX + 1):
        kmax = max(k for k in range(n + 1) if 3 ** k < 2 ** n)
        for dk in DKS:
            k = kmax - dk
            t0 = time.time()
            r = run(n, k)
            out[f"{n}_{k}"] = r
            print(f"n={n} k={k} (kmax-{dk}) m/2^n={r['m_over_2n']:.3f} binom={r['count']:.3e}: zeros {r['zeros']} "
                  f"(exp {r['expected_zeros']:.2e}); max_h |S_h| sqrt(binom) = {max(r['weyl_times_sqrt']):.2f}  "
                  f"[{time.time() - t0:.0f}s]", flush=True)
            json.dump(out, open("cycle_numerators_k.json", "w"), indent=1)


if __name__ == "__main__":
    main()
