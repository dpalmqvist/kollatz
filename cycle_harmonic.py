"""
Refinement of the Eliahou inequality (see cycles.py): n - k*log2(3) = sum_{odd x_i} log2(1 + 1/(3 x_i)) <= (1/(3 ln 2)) sum 1/x_i.
Eliahou bounds sum 1/x_i <= k/m.  Here: x_j >= m 3^{k_j}/2^j along the cycle (all elements >= m), so sum 1/x_i <= (f k)/m
with f the maximal average of 2^{d_j} over odd steps of a walk d_{j+1} = d_j + 1 (even) or d_j + 1 - theta (odd) confined to
d <= 0.  Dynamic programming gives f = 0.7214 (the greedy walk is optimal), i.e. 0.47 bits of verification range.
Hercher (2023) gains ~1.3 bits with more structure (local minima), so this relaxation alone does not reproduce him.

  python cycle_harmonic.py [steps]
"""
# Upper bound for sum over odd cycle elements of 1/x_i in units of 1/m (m = cycle minimum).
# x_j >= m 3^{k_j} / 2^j  ==>  1/x_j <= (1/m) 2^{d_j},  d_j = j - k_j*theta <= 0 for every prefix (all elements >= m).
# Walk: even step d -> d+1 (allowed iff d+1 <= 0), odd step d -> d + 1 - theta, contributes 2^{d} (evaluated before the step).
# DP over (j, k) maximizing the total; f = max total / number of odd steps (asymptotic per-odd-step average).
import math, sys
theta = math.log2(3)
L = int(sys.argv[1]) if len(sys.argv) > 1 else 300000
W = 6  # window in k above the line
# best[k] at time j, keyed by k; store (total, odd_count)
cur = {0: (0.0, 0)}
for j in range(L):
    nxt = {}
    for k, (tot, cnt) in cur.items():
        d = j - k * theta
        # even step
        if (j + 1) - k * theta <= 1e-12:
            v = nxt.get(k)
            if v is None or tot > v[0]:
                nxt[k] = (tot, cnt)
        # odd step
        t2 = tot + 2.0 ** d
        v = nxt.get(k + 1)
        if v is None or t2 > v[0]:
            nxt[k + 1] = (t2, cnt + 1)
    # prune: keep k within window above the line
    kmin = math.ceil((j + 1) / theta - 1e-12)
    cur = {k: v for k, v in nxt.items() if k - kmin <= W}
best = max(cur.values(), key=lambda v: v[0])
tot, cnt = best
print(f"L={L}: max sum = {tot:.1f} over {cnt} odd steps  ->  f = {tot/cnt:.5f}   (odd density {cnt/L:.5f}, 1/theta = {1/theta:.5f})")
# greedy walk for comparison
d = 0.0; tot = 0.0; cnt = 0
for j in range(L):
    if d + 1 <= 1e-12:
        d += 1
    else:
        tot += 2.0 ** d; cnt += 1; d += 1 - theta
print(f"greedy (even whenever allowed): f = {tot/cnt:.5f}")
# equivalent gain in verification exponent: Eliahou's crude bound uses f = 1
f = best[0] / best[1]
print(f"gain: log2(1/f) = {math.log2(1/f):.3f} bits of verification range")
