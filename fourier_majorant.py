"""
Avenue 28, step 4 (2026-10-10): Tao's pairing trick as a positive Fourier majorant for nu_{1/4}.

Conditioning on b = a + a' (the split is uniform for any geometric law) gives the exact majorant
  |nu^(xi)| <= sum_s p^2 q^s |Phi_s(xi)| |nu^(9 xi 2^-(s+2))|,   Phi_s(xi) = sum_{i=0..s} e(xi 2^-(i+1)),
with sum_s p^2 q^s (s+1) = 1, so all saving comes from the cosine sums |Phi_s| < s+1. Iterating from |nu^| <= 1 at
levels 0, 1 gives B_n >= max over level-n xi of |nu^(xi)|. Absolute continuity via Tao's §6 for p = 1/4 needs
exponential decay below 2^(-1/4) = 0.84 per level (0.706 per two levels).

Result: B_n per two levels 0.59-0.64 on even n (0.615 at n = 14, i.e. 0.784 per level) but 0.72-0.73 on odd n
(0.721 at n = 15, i.e. 0.849 per level): borderline. True max |nu^| decays like 0.64 per level.

  python fourier_majorant.py NMAX        (NMAX = 15: 25 s, 2.7 GB)
"""
import sys

import numpy as np

from syracuse_measure import marginals
p, q = 0.25, 0.75
SMAX = 70
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 12
# true |nu^| maxima per level
true = {}
for r, h in marginals(NMAX, p):
    M = 3 ** r
    nu = h / (h > 0).sum() if r > 1 else h / 2
    f = np.abs(np.fft.ifft(nu) * M)
    k = np.arange(M)
    true[r] = f[k % 3 != 0].max() if r >= 1 else 1.0
B = {0: np.ones(1), 1: np.ones(3)}
w = p * p * q ** np.arange(SMAX + 1)
tail = sum(p * p * q ** s * (s + 1) for s in range(SMAX + 1, 2000))
for n in range(2, NMAX + 1):
    M = 3 ** n
    k = np.arange(M, dtype=np.int64)
    inv2 = pow(2, -1, M)
    # E[i] = e(k * 2^-(i+1) / 3^n), cumulative sums give Phi_s
    acc = np.zeros(M, dtype=complex)
    Bn = np.full(M, tail)                       # tail bound (|Phi_s| <= s+1, B <= 1)
    kk = (k * inv2) % M
    for s in range(SMAX + 1):
        acc += np.exp(2j * np.pi * kk / M)
        Mprev = 3 ** (n - 2)
        if n - 2 >= 1:
            kprev = (k * pow(inv2, s + 2, M)) % Mprev         # 9 xi 2^-(s+2) at level n-2 (index mod 3^(n-2))
            Bprev = B[n - 2][kprev]
        else:
            Bprev = 1.0
        Bn += w[s] * np.abs(acc) * Bprev
        kk = (kk * inv2) % M
    if n - 2 >= 1:
        pass
    B[n] = np.minimum(Bn, 1.0)
    lvl = k % 3 != 0
    mb = B[n][lvl].max()
    print(f"n={n:2d}: pairing majorant max = {mb:.4e}   true max|nu^| = {true[n]:.4e}"
          + (f"   majorant ratio/2 levels = {mb/B[n-2][(np.arange(3**(n-2))%3!=0)].max():.4f}" if n >= 4 else ""), flush=True)
