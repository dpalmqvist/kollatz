"""
Avenue 28, step 4b (2026-10-10): Tao's conditioning on TRIPLES as a positive Fourier majorant for nu_{1/4}.

X = 2^-a1 + 3 2^-(a1+a2) + 9 2^-c + 27 2^-c X''' with c = a1+a2+a3; given c the composition (a1,a2,a3) is uniform
(any geometric law), so
  |nu^(xi)| <= sum_{c>=3} P(c) |Psi_c(xi)| |nu^(27 xi 2^-c)|,   P(c) = C(c-1,2) p^3 q^(c-3),
  Psi_c(xi) = C(c-1,2)^-1 sum_{a1+a2+a3=c} e(xi 2^-a1 (1 + 3 2^-a2)),
and sum_c P(c) = 1. Iterating from |nu^| <= 1 on levels 0-2 gives B_n >= max_{level n} |nu^|. The inner sums use running
prefix sums in a1, so memory is O(3^n). Tao's §6 reduction for p = 1/4 needs decay below 2^(-1/4) = 0.84 per level
(consecutive-level oscillation), against a collision-entropy deficit of 2^(0.30 n).

  python fourier_majorant3.py NMAX   [CMAX=80]
"""
import sys
from math import comb

import numpy as np

p, q = 0.25, 0.75


def main():
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    cmax = int(sys.argv[2]) if len(sys.argv) > 2 else 80
    Pc = np.array([comb(c - 1, 2) * p ** 3 * q ** (c - 3) if c >= 3 else 0.0 for c in range(cmax + 1)])
    tail = 1.0 - Pc.sum()
    B = {0: np.ones(1), 1: np.ones(3), 2: np.ones(9)}
    best = {}
    for n in range(3, nmax + 1):
        M = 3 ** n
        k = np.arange(M, dtype=np.int64)
        inv2 = pow(2, -1, M)
        Mprev = 3 ** (n - 3)
        Bprev = B[n - 3]
        Bn = np.full(M, tail)
        # running sums: cum3 = sum_{m<=t} e(3 xi 2^-m); S1 = sum_{a1<=t} e(xi 2^-a1); S13 = sum_{a1<=t} e(xi 2^-a1) cum3[a1]
        cum3 = np.zeros(M, complex); S1 = np.zeros(M, complex); S13 = np.zeros(M, complex)
        S1_prev = np.zeros(M, complex); S13_prev = np.zeros(M, complex)    # values at t = c-2
        km = k.copy()                                   # k 2^-t mod M
        kc = k.copy()                                   # k 2^-c mod Mprev (for the next level index)
        for t in range(1, cmax + 1):
            km = (km * inv2) % M
            e1 = np.exp(2j * np.pi * km / M)
            e3 = np.exp(2j * np.pi * ((3 * km) % M) / M)
            # at t: we can evaluate c = t + 1 (needs cum3[c-1] = cum3[t] and S1, S13 at c-2 = t-1)
            S1_prev, S13_prev = S1.copy(), S13.copy()   # values at t-1
            cum3 += e3
            S1 += e1
            S13 += e1 * cum3
            c = t + 1
            if 3 <= c <= cmax:
                val = cum3 * S1_prev - S13_prev
                psi = np.abs(val) / comb(c - 1, 2)
                kprev = (k * pow(inv2, c, M)) % Mprev if Mprev > 1 else np.zeros(M, dtype=np.int64)
                Bn += Pc[c] * psi * Bprev[kprev]
        B[n] = np.minimum(Bn, 1.0)
        if n - 3 >= 3:
            B[n - 3] = None if n - 3 not in (0, 1, 2) and (n - 3) < n - 3 else B[n - 3]
        lvl = k % 3 != 0
        best[n] = float(B[n][lvl].max())
        msg = f"n={n:2d}: triple majorant max = {best[n]:.4e}"
        if n - 3 in best:
            r3 = best[n] / best[n - 3]
            msg += f"   per 3 levels {r3:.4f}  (per level {r3 ** (1 / 3):.4f})"
        print(msg, flush=True)
        if n - 4 >= 3:
            B[n - 4] = None                             # only levels n-2 .. n are needed later


if __name__ == "__main__":
    main()
