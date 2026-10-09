"""
Avenue 17 / Conjecture A numerically: predecessor densities pi_a(x)/x for all a < A = 3^8 and their relation to the
K-L vectors c^m (2026-10-09).

For every n < 2^KB the orbit is followed until the first value s < A (GPU, MLX); since every value before s is >= A,
the orbit of n passes through a < A iff a lies on the orbit of s.  So pi_a(X) = sum_s H_X[s] [a in Orb(s)] with
H_X[s] = #{n <= X : first value below A is s}.  Checkpoints X = 2^24, 2^28, 2^KB.  Output pred_density.json:
H at each checkpoint, pi_a(X) for all a < A, and the comparison with the K-L profile (analysis in pred_compare.py).

  python pred_density.py [KB=32] [CHUNK_BITS=24]
"""
import json
import sys
import time

import numpy as np
import mlx.core as mx

KB = int(sys.argv[1]) if len(sys.argv) > 1 else 32
CB = int(sys.argv[2]) if len(sys.argv) > 2 else 24
A = 3 ** 8


def first_below(n0, n1):
    x = mx.arange(n0, n1, dtype=mx.int64)
    active = x >= A
    while True:
        odd = (x % 2 == 1) & active
        x = mx.where(active, mx.where(odd, (3 * x + 1) // 2, x // 2), x)
        active = active & (x >= A)
        mx.eval(x, active)
        if not active.any().item():
            break
    return np.array(x)


def orbit_sets():
    """for s < A: the set of orbit values < A (orbit to 1), as a boolean matrix (A, A)."""
    M = np.zeros((A, A), dtype=bool)
    for s in range(1, A):
        x = s
        seen = set()
        while x != 1 and x not in seen:
            seen.add(x)
            if x < A:
                M[s, x] = True
            x = (3 * x + 1) // 2 if x % 2 else x // 2
        M[s, 1] = True
        if s == 2:
            M[s, 2] = True
    return M


def main():
    t0 = time.time()
    H = np.zeros(A, dtype=np.int64)
    checkpoints = {}
    for c0 in range(1, 1 << KB, 1 << CB):
        c1 = min(1 << KB, c0 + (1 << CB))
        s = first_below(c0, c1)
        H += np.bincount(s, minlength=A)
        if c1 in (1 << 24, 1 << 28, 1 << KB):
            checkpoints[c1] = H.copy()
            print(f"checkpoint X={c1}: {time.time() - t0:.0f}s", flush=True)
    M = orbit_sets()
    out = {"A": A, "KB": KB}
    for X, Hx in checkpoints.items():
        pi = Hx @ M.astype(np.int64)                   # pi_a(X) = sum_s H[s] [a in Orb(s)]
        out[str(X)] = dict(H=Hx.tolist(), pi=pi.tolist())
    json.dump(out, open("pred_density.json", "w"))
    X = max(checkpoints); pi = np.array(out[str(X)]["pi"])
    print("pi_a(X)/X for a = 1, 2, 4, 5, 7, 8, 10, 11, 13, 16:", " ".join(f"{pi[a] / X:.4f}" for a in (1, 2, 4, 5, 7, 8, 10, 11, 13, 16)))
    print(f"done {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
