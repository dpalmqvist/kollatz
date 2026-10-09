"""
Avenue 18, first step: parity-sequence statistics of integers (2026-10-09).

For every n in [2, 2^KBITS) iterate T(n) = n/2 or (3n+1)/2 until reaching 1 and record
  * sigma(n) = number of T-steps to 1, m(n) = number of odd steps, height = max log2(T^t n / n),
  * R(n) = last t with T^t(n) >= n (the last time the orbit is at or above its start),
  * gap histogram (gap = steps between consecutive odd steps = 1 + v2(3x+1), geometric(1/2) for random input),
  * gap-pair transition counts in three regimes: (0) the window t < KBITS, where Terras's theorem makes the parities
    exactly i.i.d. fair bits over n (so this regime only checks the windowing), (1) t >= KBITS and the value at the
    START of the gap >= 2^BIG (selection on the past only, so no bias on the gap): the regime where integer-generated
    sequences could differ from random ones without end effects, (2) start value < 2^BIG: the forced descent,
  * records of R(n)/log2 n and height/log2 n.
Random model for comparison: i.i.d. gaps, P(gap = g) = 2^-g.  Output: parity_stats.json.

  python parity_stats.py [KBITS=30] [CHUNK_BITS=24]
"""
import json
import sys
import time

import numpy as np
import mlx.core as mx

KBITS = int(sys.argv[1]) if len(sys.argv) > 1 else 30
CB = int(sys.argv[2]) if len(sys.argv) > 2 else 24
G = 64                                    # gap histogram cap
BIG = 24                                  # regime threshold 2^BIG, applied to the value at the START of a gap
NREG = 3


def run_chunk(n0, n1):
    n = mx.arange(n0, n1, dtype=mx.int64)
    x = n
    log2n = mx.log2(n.astype(mx.float32))
    active = mx.ones(n.shape, dtype=mx.bool_)
    sigma = mx.zeros(n.shape, dtype=mx.int32)
    modd = mx.zeros(n.shape, dtype=mx.int32)
    height = mx.zeros(n.shape, dtype=mx.float32)
    R = mx.zeros(n.shape, dtype=mx.int32)
    since = mx.zeros(n.shape, dtype=mx.int32)          # steps since last odd step
    prev = mx.zeros(n.shape, dtype=mx.int32)           # previous completed gap (0 = none yet)
    xstart = n                                         # orbit value at the start of the current gap
    gap_hist = [mx.zeros((G + 1,), dtype=mx.int32) for _ in range(NREG)]
    pair_hist = [mx.zeros(((G + 1) * (G + 1),), dtype=mx.int32) for _ in range(NREG)]
    t = 0
    while True:
        odd = (x % 2 == 1) & active
        t += 1
        since = since + 1
        gap = mx.minimum(since, G)
        big = xstart >= (1 << BIG)
        for reg, sel in enumerate((odd & (t < KBITS), odd & (t >= KBITS) & big, odd & ~big)):
            idx = mx.where(sel, gap, 0).astype(mx.int32)
            gap_hist[reg] = gap_hist[reg].at[idx].add(sel.astype(mx.int32))
            pidx = mx.where(sel & (prev > 0), prev * (G + 1) + gap, 0).astype(mx.int32)
            pair_hist[reg] = pair_hist[reg].at[pidx].add((sel & (prev > 0)).astype(mx.int32))
        prev = mx.where(odd, gap, prev)
        since = mx.where(odd, 0, since)
        x = mx.where(odd, (3 * x + 1) // 2, x // 2)
        x = mx.where(active, x, 1)
        xstart = mx.where(odd, x, xstart)
        sigma = sigma + active.astype(mx.int32)
        modd = modd + odd.astype(mx.int32)
        h = mx.log2(x.astype(mx.float32)) - log2n
        height = mx.maximum(height, mx.where(active, h, 0.0))
        R = mx.where(active & (x >= n), t, R)
        active = active & (x != 1)
        mx.eval(active, x, sigma, modd, height, R, since, prev, gap_hist[0], gap_hist[1], pair_hist[0], pair_hist[1])
        if not active.any().item():
            break
    return dict(n=n, sigma=sigma, modd=modd, height=height, R=R, log2n=log2n, gap_hist=gap_hist, pair_hist=pair_hist, iters=t)


def main():
    t0 = time.time()
    tot = dict(gap=[np.zeros(G + 1, dtype=np.int64) for _ in range(NREG)], pair=[np.zeros((G + 1) ** 2, dtype=np.int64) for _ in range(NREG)])
    sig_hist = np.zeros(4096, dtype=np.int64); odd_hist = np.zeros(2048, dtype=np.int64)
    rec_R, rec_h = [], []          # record holders (n, value)
    bestR = besth = 0.0
    sum_sig = sum_odd = 0.0; cnt = 0
    for c0 in range(2, 1 << KBITS, 1 << CB):
        c1 = min(1 << KBITS, c0 + (1 << CB))
        r = run_chunk(c0, c1)
        for reg in range(NREG):
            tot["gap"][reg] += np.array(r["gap_hist"][reg]); tot["pair"][reg] += np.array(r["pair_hist"][reg])
        sig = np.array(r["sigma"]); mo = np.array(r["modd"]); h = np.array(r["height"]); R = np.array(r["R"]); l2 = np.array(r["log2n"]); n = np.array(r["n"])
        sig_hist += np.bincount(np.minimum(sig, 4095), minlength=4096); odd_hist += np.bincount(np.minimum(mo, 2047), minlength=2048)
        sum_sig += sig.sum(); sum_odd += mo.sum(); cnt += sig.size
        rr = R / l2; hh = h / l2
        for arr, best, rec in ((rr, bestR, rec_R), (hh, besth, rec_h)):
            i = int(arr.argmax())
            if arr[i] > best:
                rec.append((int(n[i]), float(arr[i]), int(R[i]) if arr is rr else float(h[i])))
        bestR = max(bestR, float(rr.max())); besth = max(besth, float(hh.max()))
        print(f"chunk [{c0}, {c1}) iters={r['iters']} mean sigma={sum_sig / cnt:.2f} mean odd={sum_odd / cnt:.2f} "
              f"record R/log2n={bestR:.3f} height/log2n={besth:.3f} [{time.time() - t0:.0f}s]", flush=True)
    out = dict(KBITS=KBITS, count=cnt, mean_sigma=sum_sig / cnt, mean_odd=sum_odd / cnt,
               sigma_hist=sig_hist.tolist(), odd_hist=odd_hist.tolist(),
               BIG=BIG, gap_hist=[h.tolist() for h in tot["gap"]], pair_hist=[h.reshape(G + 1, G + 1).tolist() for h in tot["pair"]],
               records_R=rec_R, records_height=rec_h, seconds=time.time() - t0)
    json.dump(out, open(f"parity_stats_{KBITS}.json", "w"))
    print("done", time.time() - t0)


if __name__ == "__main__":
    main()
