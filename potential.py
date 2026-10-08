"""
Adaptive forced-transition potential (Mazur's `AdaptiveForcedPotentialCertificate`) for level k, as the
least fixed point of the constraint system.  The potential depends only on k (the residue graph), not on
the LP weights.  Constraints (verify_kl_adaptive_potential.py / AdaptiveForcedPotentialCertificate.lean),
N = 3^(k-1), L = N/3, index i, q = i // 3:
  P  : pot[(4i+2) mod N]                      <= pot[i] + 6        for all i
  D1 : min_t pot[(4q mod L) + tL]             <= pot[3q] + 1       for all q
  D3 : min_t pot[((2q+1) mod L) + tL]         <= pot[3q+2] - 2     for all q
Least solution: start at 0 and raise pot[i] to the required minimum until nothing changes
(monotone; converges iff the system is feasible).  Output: pot as uint8 payload `k{k}_adaptive.u8`.

  python potential.py k [--compare FILE.u8] [--out DIR]
"""
import argparse
import hashlib
import sys
import time
from pathlib import Path

import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("k", type=int)
ap.add_argument("--compare", help="existing payload to compare with (e.g. Mazur's k18_adaptive.u8)")
ap.add_argument("--out", default=".")
ap.add_argument("--chunk", type=int, default=1 << 24)
args = ap.parse_args()
k = args.k
N = 3 ** (k - 1)
L = N // 3
pot = np.zeros(N, dtype=np.int16)
t0 = time.time()
for it in range(1, 1000):
    changed = 0
    new = pot.copy()
    # P: pot[i] >= pot[4i+2] - 6
    for s in range(0, N, args.chunk):
        i = np.arange(s, min(s + args.chunk, N), dtype=np.int64)
        req = pot[(4 * i + 2) % N] - 6
        np.maximum(new[s:s + len(i)], req, out=new[s:s + len(i)])
    # D1: pot[3q] >= min_t pot[4q mod L + tL] - 1 ;  D3: pot[3q+2] >= min_t pot[(2q+1) mod L + tL] + 2
    for s in range(0, L, args.chunk):
        q = np.arange(s, min(s + args.chunk, L), dtype=np.int64)
        b1 = (4 * q) % L
        m1 = np.minimum(np.minimum(pot[b1], pot[b1 + L]), pot[b1 + 2 * L])
        idx = 3 * q
        new[idx] = np.maximum(new[idx], m1 - 1)
        b3 = (2 * q + 1) % L
        m3 = np.minimum(np.minimum(pot[b3], pot[b3 + L]), pot[b3 + 2 * L])
        idx = 3 * q + 2
        new[idx] = np.maximum(new[idx], m3 + 2)
    changed = int((new != pot).sum())
    pot = new
    print(f"iter {it}: changed={changed} max={int(pot.max())} [{time.time() - t0:.0f}s]", flush=True)
    if changed == 0:
        break
    if pot.max() > 250:
        sys.exit("potential exceeds uint8 range: system looks infeasible")

# own verification of all three families
fails = 0
mins = []
for s in range(0, N, args.chunk):
    i = np.arange(s, min(s + args.chunk, N), dtype=np.int64)
    sl = pot[i] + 6 - pot[(4 * i + 2) % N]
    fails += int((sl < 0).sum()); mins.append(int(sl.min()))
for s in range(0, L, args.chunk):
    q = np.arange(s, min(s + args.chunk, L), dtype=np.int64)
    b1 = (4 * q) % L
    sl = pot[3 * q] + 1 - np.minimum(np.minimum(pot[b1], pot[b1 + L]), pot[b1 + 2 * L])
    fails += int((sl < 0).sum()); mins.append(int(sl.min()))
    b3 = (2 * q + 1) % L
    sl = pot[3 * q + 2] - 2 - np.minimum(np.minimum(pot[b3], pot[b3 + L]), pot[b3 + 2 * L])
    fails += int((sl < 0).sum()); mins.append(int(sl.min()))
print(f"k={k}: least potential, max={int(pot.max())}, failures={fails}, min slack={min(mins)}, "
      f"histogram={np.bincount(pot.astype(np.int64)).tolist()}")
assert fails == 0
out = Path(args.out) / f"k{k}_adaptive.u8"
pot.astype(np.uint8).tofile(out)
print("wrote", out, "sha256", hashlib.sha256(out.read_bytes()).hexdigest())
if args.compare:
    other = np.fromfile(args.compare, dtype=np.uint8).astype(np.int16)
    print(f"compare with {args.compare}: identical={bool((other == pot).all())}, other max={int(other.max())}, "
          f"ours <= other everywhere={bool((pot <= other).all())}, #differences={int((other != pot).sum())}")
