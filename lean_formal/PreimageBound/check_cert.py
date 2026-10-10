#!/usr/bin/env python3
"""Independent check of a certificate cert_r{r}.json (pure Python, no numpy, no code shared with gen_cert.py).

1. The inequality Q * Phi(V)(c) >= P * V(c) for every class c mod 3^r, c % 3 != 0, with the lift class of
   (2b-1)/3 computed from an actual integer b = c + 3^r * t (t = 0, 1, 2) rather than from the lift formula.
2. Brute force: for all a < A with a % 3 != 0 and k <= K, the number of n in [1, 2^k a] with T^k(n) = a
   (computed by iterating T on every n) is >= (c_num/c_den) * (P/Q)^k, and the pruned count
   (backward tree, children 2n and (2n-1)/3 for n = 2, 8 mod 9) is <= it.

Usage: python check_cert.py certs/cert_r8.json [A K]     (also accepts .json.gz)
"""
import gzip
import json
import sys
from fractions import Fraction


def T(n):
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2


def main():
    path = sys.argv[1]
    cert = json.load(gzip.open(path, "rt") if path.endswith(".gz") else open(path))
    A = int(sys.argv[2]) if len(sys.argv) > 2 else 60
    K = int(sys.argv[3]) if len(sys.argv) > 3 else 14
    r, P, Q, V = cert["r"], cert["P"], cert["Q"], cert["V"]
    M = 3 ** r
    assert len(V) == M
    classes = [c for c in range(M) if c % 3]
    assert all(V[c] > 0 for c in classes)
    Vmin, Vmax = min(V[c] for c in classes), max(V[c] for c in classes)
    assert (Vmin, Vmax) == (cert["Vmin"], cert["Vmax"])
    bad = 0
    for c in classes:
        rhs = V[(2 * c) % M]
        if c % 9 in (2, 8):
            # the three classes reached by (2b-1)/3 for b = c, c + M, c + 2M
            lift = [((2 * (c + t * M) - 1) // 3) % M for t in range(3)]
            assert len(set(lift)) == 3 and all(x % 3 for x in lift)
            rhs += min(V[x] for x in lift)
        if Q * rhs < P * V[c]:
            bad += 1
    print(f"r={r}: {len(classes)} classes, {bad} violations of Q*Phi(V) >= P*V; P/Q = {P / Q:.7f}")
    assert bad == 0
    cconst = Fraction(cert["c_num"], cert["c_den"])
    assert cconst <= Fraction(Vmin, Vmax)
    mu = Fraction(P, Q)

    # brute force n_k(a) for a < A, k <= K
    targets = [a for a in range(1, A) if a % 3]
    worst = None
    for k in range(K + 1):
        cnt = {a: 0 for a in targets}
        lim = 2 ** k * A
        for n in range(1, lim + 1):
            m = n
            for _ in range(k):
                m = T(m)
            if m in cnt and n <= 2 ** k * m:
                cnt[m] += 1

        def pruned(b, d):
            if d == 0:
                return 1
            s = pruned(2 * b, d - 1)
            if b % 9 in (2, 8):
                s += pruned((2 * b - 1) // 3, d - 1)
            return s

        for a in targets:
            pa = pruned(a, k)
            assert pa <= cnt[a], (a, k, pa, cnt[a])
            bound = cconst * mu ** k
            assert bound <= cnt[a] and Fraction(Vmin, Vmax) * mu ** k <= pa, (a, k)
            q = Fraction(pa) / mu ** k
            if worst is None or q < worst[0]:
                worst = (q, a, k)
    print(f"brute force a < {A}, k <= {K}: all bounds hold; min pruned/mu^k = {float(worst[0]):.4f} at a={worst[1]}, k={worst[2]}"
          f" (stated c = {float(cconst)})")


if __name__ == "__main__":
    main()
