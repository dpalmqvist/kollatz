"""
Avenue 19, step 3 (2026-10-10): FINE-SCALE equidistribution of cycle numerators N(v) mod m = 2^n - 3^k near 0.

A cycle needs N(v) = 0 (mod m) exactly, so the relevant test is not a low-frequency Weyl sum but the count of v with
N(v) mod m in a short window next to 0 and the counts of v with N(v) = 0 mod d for divisors d of m.  For weight-k
parity vectors (same enumeration as cycle_numerators_k.py: colex unrank + Gosper, exact uint64 residues) we count
  win_j = #{v : N(v) mod m < m >> (10 j)}           j = 1, 2, 3   (expected binom / 2^(10 j))
  win_j' = #{v : N(v) mod m > m - (m >> (10 j))}    (the window just below m, i.e. just below 0)
  div_p = #{v : N(v) = 0 mod p}  for the smallest prime factors p > 3 of m (up to 4 of them, p < 10^6)  (expected binom / p)
and print the ratios observed/expected with the Poisson z-score.

  python cycle_numerators_fine.py NMIN NMAX [DK=0] [B=2048] [--aperiodic]
With --aperiodic, d-periodic parity vectors (v = w^d for a prime d | gcd(n, k)) are skipped: they never give a new
cycle, and they cause the large divisibility anomalies, since 2^n - 3^k = (2^{n/d} - 3^{k/d}) Phi and N(w^d) = N(w) Phi.
Expected counts then use the number of aperiodic vectors, sum over d | g of mu(d) binom(n/d, k/d).
"""
import json
import math
import sys
import time

import numpy as np
import mlx.core as mx

APER = '--aperiodic' in sys.argv
sys.argv = [a for a in sys.argv if a != '--aperiodic']
NMIN, NMAX = int(sys.argv[1]), int(sys.argv[2])
DKS = [int(x) for x in sys.argv[3].split(",")] if len(sys.argv) > 3 else [0]
B = int(sys.argv[4]) if len(sys.argv) > 4 else 2048
NP = 4

SRC = r"""
    uint tid = thread_position_in_grid.x;
    uint64_t r = (uint64_t)start[0] + (uint64_t)tid * (uint64_t)BB;
    uint64_t total = (uint64_t)tot[0];
    uint cnt_out[6 + NPP];
    for (int q = 0; q < 6 + NPP; q++) cnt_out[q] = 0;
    if (r < total) {
        uint64_t v = 0; uint64_t rr = r; int c = NN - 1;
        for (int j = KK; j >= 1; j--) {
            while (binom[c * (KK + 1) + j] > rr) c--;
            v |= ((uint64_t)1 << c); rr -= binom[c * (KK + 1) + j]; c--;
        }
        uint64_t mm = mtab[0];
        uint64_t steps = total - r; if (steps > (uint64_t)BB) steps = (uint64_t)BB;
        for (uint64_t s = 0; s < steps; s++) {
            bool periodic = false;
            for (int q = 0; q < NPER; q++) {
                int sh = pershift[q];
                uint64_t rotv = ((v >> sh) | (v << (NN - sh))) & (((uint64_t)1 << NN) - 1);
                if (rotv == v) periodic = true;
            }
            if (periodic) {
                uint64_t t2 = v | (v - 1);
                v = (t2 + 1) | (((~t2 & (t2 + 1)) - 1) >> (ctz(v) + 1));
                continue;
            }
            uint64_t acc = 0; int cnt = 0;
            uint64_t w = v;
            while (w) {
                int i = 63 - clz(w);
                acc += T[cnt * NN + i]; if (acc >= mm) acc -= mm;
                cnt++; w &= ~((uint64_t)1 << i);
            }
            for (int q = 0; q < 3; q++) {
                uint64_t W = mm >> (10 * (q + 1));
                if (acc < W) cnt_out[q]++;
                if (acc > mm - W) cnt_out[3 + q]++;
            }
            for (int q = 0; q < NPP; q++) {
                uint64_t p = ptab[q];
                if (p > 1 && (acc % p) == 0) cnt_out[6 + q]++;
            }
            uint64_t t = v | (v - 1);
            v = (t + 1) | (((~t & (t + 1)) - 1) >> (ctz(v) + 1));
        }
    }
    for (int q = 0; q < 6 + NPP; q++) out[tid * (6 + NPP) + q] = cnt_out[q];
"""


def small_primes(m, limit=10 ** 6, count=NP):
    ps = []
    x = m
    p = 5
    while p < limit and len(ps) < count:
        if x % p == 0:
            ps.append(p)
            while x % p == 0:
                x //= p
        p += 2
    return ps


def run(n, k):
    m = (1 << n) - 3 ** k
    T = np.zeros((k, n), dtype=np.uint64)
    for cnt in range(k):
        for i in range(n):
            T[cnt, i] = (pow(3, cnt, m) * pow(2, i, m)) % m
    bt = np.zeros((n, k + 1), dtype=np.uint64)
    for c in range(n):
        for j in range(k + 1):
            bt[c, j] = math.comb(c, j)
    total = math.comb(n, k)
    g = math.gcd(n, k)
    dprimes = [q for q in range(2, g + 1) if g % q == 0 and all(q % r for r in range(2, q))]
    pers = [n // q for q in dprimes] if APER else []
    ps = small_primes(m)
    ptab = np.array(ps + [1] * (NP - len(ps)), dtype=np.uint64)
    kernel = mx.fast.metal_kernel(name=f"cycf{n}_{k}", input_names=["start", "tot", "mtab", "T", "binom", "ptab", "pershift"],
                                  output_names=["out"],
                                  header=f"#define NN {n}\n#define KK {k}\n#define BB {B}\n#define NPP {NP}\n#define NPER {len(pers)}\n", source=SRC)
    threads = 1 << 20
    acc = np.zeros(6 + NP, dtype=np.int64)
    args = [mx.array([total], dtype=mx.uint64), mx.array([m], dtype=mx.uint64), mx.array(T.ravel()), mx.array(bt.ravel()),
            mx.array(ptab), mx.array(np.array(pers + [0], dtype=np.int32))]
    for s in range(0, total, threads * B):
        (o,) = kernel(inputs=[mx.array([s], dtype=mx.uint64)] + args, grid=(threads, 1, 1), threadgroup=(256, 1, 1),
                      output_shapes=[(threads * (6 + NP),)], output_dtypes=[mx.uint32])
        acc += np.array(o).astype(np.int64).reshape(threads, 6 + NP).sum(axis=0)
    def mobius(d):
        r, x, q = 1, d, 2
        while q * q <= x:
            if x % q == 0:
                x //= q
                if x % q == 0:
                    return 0
                r = -r
            q += 1
        return -r if x > 1 else r
    eff = sum(mobius(d) * math.comb(n // d, k // d) for d in range(1, g + 1) if g % d == 0) if APER else total
    res = dict(m=m, count=total, counted=eff, aperiodic=APER, primes=ps)
    for q in range(3):
        W = m >> (10 * (q + 1))
        e = eff * W / m
        res[f"win{q + 1}"] = [int(acc[q]), e, (acc[q] - e) / math.sqrt(e) if e > 0 else None]
        res[f"winm{q + 1}"] = [int(acc[3 + q]), e, (acc[3 + q] - e) / math.sqrt(e) if e > 0 else None]
    for q, p in enumerate(ps):
        e = eff / p
        res[f"div{p}"] = [int(acc[6 + q]), e, (acc[6 + q] - e) / math.sqrt(e)]
    return res


def main():
    try:
        out = json.load(open("cycle_numerators_fine" + ("_aper" if APER else "") + ".json"))
    except Exception:
        out = {}
    for n in range(NMIN, NMAX + 1):
        kmax = max(k for k in range(n + 1) if 3 ** k < 2 ** n)
        for dk in DKS:
            k = kmax - dk
            t0 = time.time()
            r = run(n, k)
            out[f"{n}_{k}"] = r
            parts = [f"{key}: {v[0]}/{v[1]:.1f} (z={v[2]:+.1f})" for key, v in r.items()
                     if key.startswith(("win", "div")) and v[2] is not None]
            print(f"n={n} k={k} m/2^n={r['m'] / 2 ** n:.3f} binom={r['count']:.2e} primes={r['primes']}: " + "; ".join(parts)
                  + f"  [{time.time() - t0:.0f}s]", flush=True)
            json.dump(out, open("cycle_numerators_fine" + ("_aper" if APER else "") + ".json", "w"), indent=1)


if __name__ == "__main__":
    main()
