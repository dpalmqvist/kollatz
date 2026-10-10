"""
Avenue 27 (2026-10-10): exact census of ALL cycles of T_d(x) = x/2 (even), (3x+d)/2 (odd) up to a given length.

A parity vector v of length n with k odd steps gives the rational periodic point x0 = d N(v) / (2^n - 3^k),
N(v) = sum over set bits i (high to low) of 3^cnt 2^i, cnt = number of set bits above i (cycle_numerators.py).  The
2-adic parity map is a bijection on periodic points, so x0 has parity vector v^infinity; hence T_d has a cycle with
parity vector v iff x0 is a positive integer, i.e. (2^n - 3^k) | d N(v).  Enumerating every v of length n <= NMAX
therefore finds every cycle of length <= NMAX, however large its elements (unlike a search by starting value).
GPU: each thread scans B consecutive v and reports at most two hits (overflow is rescanned on the host); the host
verifies each hit exactly, keeps aperiodic v (minimal period n), reduces rotations to one cycle, records
min/max element, and marks primitive cycles (gcd(min, d) = 1; otherwise the cycle is a scaled cycle of 3x + d/g).
Heuristic comparison: for each (n, k), E = (#aperiodic necklaces) * gcd(m, d) / m.

  python cycles_by_length.py NMAX d [d ...]          -> cycles_by_length.json
"""
import json
import math
import sys
import time

import numpy as np
import mlx.core as mx

NMAX = int(sys.argv[1])
DS = [int(x) for x in sys.argv[2:]]
OUTF = "cycles_by_length.json" if NMAX <= 34 else f"cycles_by_length_n{NMAX}.json"
B = 4096

SRC = r"""
    uint tid = thread_position_in_grid.x;
    uint64_t v0 = (uint64_t)start[0] + (uint64_t)tid * (uint64_t)BB;
    uint64_t limit = (uint64_t)1 << NN;
    uint c = 0; uint64_t h0 = 0, h1 = 0;
    uint64_t dd = (uint64_t)dval[0];
    for (uint64_t s = 0; s < (uint64_t)BB; s++) {
        uint64_t v = v0 + s;
        if (v >= limit) break;
        int k = popcount((uint)(v & 0xffffffffu)) + popcount((uint)(v >> 32));
        uint64_t mm = mtab[k];
        if (k == 0 || mm == 0) continue;
        uint64_t acc = 0; int cnt = 0; uint64_t w = v;
        while (w) {
            int i = 63 - clz(w);
            acc += T[(k * NN + cnt) * NN + i]; if (acc >= mm) acc -= mm;
            cnt++; w &= ~((uint64_t)1 << i);
        }
        if ((dd * acc) % mm == 0) {
            if (c == 0) h0 = v; else if (c == 1) h1 = v;
            c++;
        }
    }
    cout[tid] = c; hout[2 * tid] = h0; hout[2 * tid + 1] = h1;
"""


def numer(v, n):
    N, cnt = 0, 0
    for i in range(n - 1, -1, -1):
        if (v >> i) & 1:
            N += 3 ** cnt * 2 ** i
            cnt += 1
    return N, cnt


def rotations(v, n):
    mask = (1 << n) - 1
    out, w = [], v
    for _ in range(n):
        out.append(w)
        w = ((w >> 1) | ((w & 1) << (n - 1))) & mask
    return out


def cycle_of(x, d, n):
    xs = []
    for _ in range(n):
        xs.append(x)
        x = x // 2 if x % 2 == 0 else (3 * x + d) // 2
    assert x == xs[0]
    return xs


def scan(n, d):
    mt = np.zeros(n + 1, dtype=np.uint64)
    T = np.zeros((n + 1, n, n), dtype=np.uint64)
    for k in range(1, n + 1):
        m = 2 ** n - 3 ** k
        if m <= 0:
            continue
        mt[k] = m
        for cnt in range(k):
            for i in range(n):
                T[k, cnt, i] = (pow(3, cnt, m) * pow(2, i, m)) % m
    kernel = mx.fast.metal_kernel(name=f"cbl{n}", input_names=["start", "mtab", "T", "dval"], output_names=["cout", "hout"],
                                  header=f"#define NN {n}\n#define BB {B}\n", source=SRC)
    threads = 1 << 18
    hits = []
    mtx, Tx, dx = mx.array(mt), mx.array(T.ravel()), mx.array([d], dtype=mx.uint64)
    for s in range(0, 1 << n, threads * B):
        c, h = kernel(inputs=[mx.array([s], dtype=mx.uint64), mtx, Tx, dx], grid=(threads, 1, 1), threadgroup=(256, 1, 1),
                      output_shapes=[(threads,), (2 * threads,)], output_dtypes=[mx.uint32, mx.uint64])
        c = np.array(c); h = np.array(h).reshape(threads, 2)
        for t in np.nonzero(c)[0]:
            if c[t] <= 2:
                hits.extend(int(x) for x in h[t, :c[t]])
            else:                                           # overflow: rescan this block on the host
                for v in range(s + int(t) * B, min(s + (int(t) + 1) * B, 1 << n)):
                    k = bin(v).count("1"); m = 2 ** n - 3 ** k
                    if k and m > 0 and (d * numer(v, n)[0]) % m == 0:
                        hits.append(v)
    return hits


def necklaces_aperiodic(n, k):
    """number of aperiodic binary necklaces of length n with k ones (Moebius)."""
    def mu(x):
        r, q = 1, 2
        while q * q <= x:
            if x % q == 0:
                x //= q
                if x % q == 0:
                    return 0
                r = -r
            q += 1
        return -r if x > 1 else r
    g = math.gcd(n, k)
    return sum(mu(e) * math.comb(n // e, k // e) for e in range(1, g + 1) if g % e == 0) // n


def main():
    try:
        out = json.load(open(OUTF))
    except Exception:
        out = {}
    for d in DS:
        t0 = time.time()
        cyc = {}
        heur = 0.0
        for n in range(1, NMAX + 1):
            for k in range(1, n + 1):
                m = 2 ** n - 3 ** k
                if m > 0:
                    heur += necklaces_aperiodic(n, k) * math.gcd(m, d) / m
            for v in scan(n, d):
                N, k = numer(v, n)
                m = 2 ** n - 3 ** k
                assert (d * N) % m == 0
                if min(rotations(v, n)) != v:
                    continue                                 # one representative per rotation class
                if any(rotations(v, n)[j] == v for j in range(1, n)):
                    continue                                 # periodic: belongs to a shorter cycle
                x0 = d * N // m
                xs = cycle_of(x0, d, n)
                key = min(xs)
                cyc[key] = dict(n=n, k=k, min=key, max=max(xs), primitive=math.gcd(key, d) == 1)
        prim = [c for c in cyc.values() if c["primitive"]]
        out[str(d)] = dict(nmax=NMAX, cycles=sorted(cyc.values(), key=lambda c: (c["n"], c["min"])),
                           n_primitive=len(prim), n_all=len(cyc), heuristic_all=heur)
        print(f"d={d}: {len(cyc)} cycles of length <= {NMAX} ({len(prim)} primitive); heuristic (all, incl. scaled) "
              f"{heur:.2f}; largest min element {max((c['min'] for c in cyc.values()), default=0)}  [{time.time() - t0:.0f}s]",
              flush=True)
        json.dump(out, open(OUTF, "w"), indent=1)


if __name__ == "__main__":
    main()
