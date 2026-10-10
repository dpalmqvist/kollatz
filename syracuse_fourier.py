"""
Avenue 30 (2026-10-10): worst-case Fourier decay of nu_p, in particular Tao's Syracuse measure p = 1/2.

For each level n: max |nu^(xi)| over primitive characters xi mod 3^n (3 does not divide xi), the ratio to the
previous level, the maximising xi written as +-2^L * s with |s| minimal, and local slopes of log max|nu^| over the
window [n-4, n] against n (exponential decay), log n (power law) and sqrt n (stretched exponential). A model fits
when its slope is constant in n.

Result (n <= 17): p = 1/4 decays exponentially (ratio levels off at 0.62-0.64, log slope per level -> -0.45).
p = 1/2 (Tao's measure) does not in this range: the ratio rises 0.66 -> 0.87-0.89, the log slope per level shrinks
steadily (-0.34 at n = 6, -0.14 at n = 17), and over n = 12-17 the local power exponent is steady at 2.1
(max|nu^| ~ C n^-2.1) while the sqrt-n slope drifts (-1.31 -> -1.10). Tao's Prop. 1.17 gives O_A(n^-A) for every A,
so the local exponent must grow eventually; it has not by n = 17. The maximiser is always a pure 2-power
xi = +-2^L (2^L/3^n between 1/64 and 1/24 for p = 1/2). See notes/limit_function.md, AVENUES.md section 30.

  python syracuse_fourier.py NMAX [p ...]       (default p = 0.25 0.5; per p: NMAX = 16 ~5 s, 7.4 GB; 17: 15 s, 23 GB)
"""
import sys

import numpy as np

from syracuse_measure import marginals


def two_power_form(xi, M, n):
    """Return (s, L, sign) with sign * xi = 2^L * s mod M, 0 <= L < 3^(n-1) and s >= 0 minimal."""
    period = 3 ** (n - 1)                                         # 2 has order 2*3^(n-1) and 2^(3^(n-1)) = -1
    B = 4096
    best = (M, 0, 1)
    inv2 = pow(2, -1, M)                                          # scan s = sign * xi * 2^-L in blocks of B
    small_inv = np.ones(B, dtype=np.int64)
    for j in range(1, B):
        small_inv[j] = small_inv[j - 1] * inv2 % M
    step_inv = small_inv[-1] * inv2 % M
    blk = 1
    for i in range(0, period, B):
        pw = small_inv * blk % M                                  # 2^-(i + j) mod M
        for sign in (1, -1):
            s = (sign * xi % M) * pw % M                      # both signs scanned, so no centring needed
            j = int(s.argmin())
            if i + j < period and s[j] < best[0]:
                best = (int(s[j]), i + j, sign)
        blk = blk * step_inv % M
    return best


def main():
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 13
    ps = [float(a) for a in sys.argv[2:]] or [0.25, 0.5]
    for p in ps:
        print(f"p = {p}")
        logs = {}
        for n, h in marginals(nmax, p):
            if n < 2:
                continue
            M = 3 ** n
            nu = h / (h > 0).sum()
            f = np.abs(np.fft.ifft(nu) * M)
            f[np.arange(M) % 3 == 0] = 0.0
            xi = int(f.argmax())
            mx = float(f[xi])
            logs[n] = np.log(mx)
            s, L, sign = two_power_form(xi, M, n)
            line = f"  n={n:2d}  max|nu^| = {mx:.4e}"
            if n - 1 in logs:
                line += f"  ratio = {mx / np.exp(logs[n - 1]):.3f}"
            line += f"  xi* = {'+' if sign > 0 else '-'}2^{L}*{s}"
            if n - 4 in logs:
                d = logs[n] - logs[n - 4]
                line += (f"  slopes: /n {d / 4:+.3f}  /log n {d / np.log(n / (n - 4)):+.2f}"
                         f"  /sqrt n {d / (np.sqrt(n) - np.sqrt(n - 4)):+.2f}")
            print(line, flush=True)
            del f, nu


if __name__ == "__main__":
    main()
