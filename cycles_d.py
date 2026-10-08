"""
Avenue 3: actual cycles of T_d(n) = n/2 (even), (3n+d)/2 (odd) for small d, against the Diophantine constraint.

For a cycle with n steps, k odd, min m, max M:   2^n = prod_odd (3 + d/x)   =>
    k*log2(1 + d/(3M)) <= n - k*log2(3) <= k*log2(1 + d/(3m)).
Brute force: iterate T_d from every start <= LIMIT with a visited array; every cycle whose minimum is <= LIMIT is
found.  Report (n, k, min, max) per cycle, check the inequality, and list which semiconvergent pairs (n, k) with
n <= nmax admit a cycle for this d and which do not.

  python cycles_d.py [LIMIT=2000000] [d ...]
"""
import math
import sys

import numpy as np

LIMIT = int(sys.argv[1]) if len(sys.argv) > 1 else 2_000_000
ds = [int(x) for x in sys.argv[2:]] or [1, 5, 7, 11, 13, 17, 19, 23, 25, 29]
THETA = math.log2(3)


def cycles(d, limit):
    """All cycles of T_d with minimum <= limit (elements may exceed limit during the orbit)."""
    seen = np.zeros(limit + 1, dtype=np.int8)      # 0 unvisited, 1 on current path, 2 done
    found = {}
    for start in range(1, limit + 1):
        if seen[start]:
            continue
        path = []
        x = start
        while True:
            if x <= limit:
                if seen[x] == 2:
                    break
                if seen[x] == 1:                       # closed a cycle
                    i = path.index(x)
                    cyc = path[i:]
                    found[min(cyc)] = cyc
                    break
                seen[x] = 1
            path.append(x)
            x = x // 2 if x % 2 == 0 else (3 * x + d) // 2
            if len(path) > 10_000_000:
                raise RuntimeError("orbit too long")
        for y in path:
            if y <= limit:
                seen[y] = 2
    return [found[m] for m in sorted(found)]


for d in ds:
    if math.gcd(d, 6) != 1:
        continue
    cs = cycles(d, LIMIT)
    print(f"\n3x+{d}: {len(cs)} cycle(s) with minimum <= {LIMIT}")
    for cyc in cs:
        n = len(cyc)
        k = sum(1 for x in cyc if x % 2)
        m, M = min(cyc), max(cyc)
        err = n / k - THETA
        lo = math.log2(1 + d / (3 * M))
        hi = math.log2(1 + d / (3 * m))
        ok = lo <= err <= hi
        print(f"  n={n:5d} k={k:5d} min={m:8d} max={M:10d}  n/k-theta={err:+.5f} in [{lo:.5f},{hi:.5f}]: {ok}")
