"""
Avenue 28, step 2 (2026-10-10): exact two-point correlation recursion for the stationary measure nu_p of
x -> x/2 (prob 1-p), x -> (3x+1)/2 (prob p) on Z_3^x  (p = 1/4: Applegate-Lagarias limit function W_inf).

Fourier: nu^(xi) = (1-p) nu^(xi/2) + p e(xi/2) nu^(3 xi/2). For level-n characters xi (denominator 3^n) let
  S_n = sum_{xi level n} |nu^(xi)|^2   (= ||delta_n||_2^2, delta_n the level-n martingale difference),
  G_n(d, u) = sum_{xi level n} e(u xi) nu^(xi) conj(nu^(2^-d xi)),   d in Z, u in Z_3,
so G_n(d, u) = 3^n P(2^d(X+u) = Y mod 3^n) - 3^(n-1) P(... mod 3^(n-1)) for X, Y iid ~ nu: the correlation of
delta_n under the affine map x -> 2^d (x + u). Exact recursion (q = 1 - p):
  G_n(d, u) = 3p^2 sum_{i,j>=0, 2^(i+1)u + 1 - 2^(i-d-j) = 0 mod 3} q^(i+j) G_(n-1)(d+j-i, (2^(i+1)u + 1 - 2^(i-d-j))/3),
in particular S_n = (3p/(2-p)) [S_(n-1) + 2 sum_{d>=2 even} q^d Re G_(n-1)(d, u_d)],  u_d = (1 - 2^-d)/3.

  python corr_recursion.py NMAX [p]     checks both identities and prints the normalised correlations rho = G/S
"""
import sys

import numpy as np

from syracuse_measure import marginals


def fourier_level(nu, n):
    """nu^(k/3^n) for all k mod 3^n (numpy convention e(+k x / 3^n)), and the mask of level-n characters."""
    M = 3 ** n
    f = np.fft.ifft(nu) * M                       # sum_x nu(x) e(+2 pi i k x / M)
    lvl = np.arange(M) % 3 != 0
    return f, lvl


def G(f, lvl, n, d, u):
    M = 3 ** n
    k = np.arange(M)
    inv2 = pow(2, -1, M)
    kd = (k * pow(inv2, d % (2 * 3 ** (n - 1)), M)) % M if d >= 0 else (k * pow(2, -d, M)) % M
    ph = np.exp(2j * np.pi * ((u % M) * k % M) / M)
    return np.sum((ph * f * np.conj(f[kd]))[lvl])


def u_d(d, n):
    M = 3 ** n
    return ((1 - pow(pow(2, -1, 3 * M), d, 3 * M)) % (3 * M)) // 3      # (1 - 2^-d)/3 mod 3^n (d even)


def main():
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    p = float(sys.argv[2]) if len(sys.argv) > 2 else 0.25
    q = 1 - p
    F = {}
    for r, h in marginals(nmax, p):
        nu = h / (h > 0).sum() if r > 1 else h / 2
        F[r] = fourier_level(nu, r)
    print(f"p = {p}:  S_n, ratio, identity check, and rho(d) = Re G_(n-1)(d, u_d)/S_(n-1) for d = 2, 4, ..., 12")
    for n in range(3, nmax + 1):
        f, lvl = F[n]
        S = np.sum(np.abs(f[lvl]) ** 2)
        fp, lvlp = F[n - 1]
        Sp = np.sum(np.abs(fp[lvlp]) ** 2)
        dmax = min(2 * 3 ** (n - 2), 120)
        rho = {d: (G(fp, lvlp, n - 1, d, u_d(d, n - 1)) / Sp) for d in range(2, dmax + 1, 2)}
        pred = 3 * p / (2 - p) * Sp * (1 + 2 * sum(q ** d * rho[d].real for d in rho))
        tail = 2 * sum(q ** d for d in range(dmax + 2, 4000, 2))
        print(f"n={n:2d} S={S:.4e} ratio={S/Sp:.5f} pred/S={pred/S:.6f} (tail<= {tail:.1e})  rho:",
              " ".join(f"{rho[d].real:+.3f}" for d in range(2, min(dmax, 12) + 1, 2)),
              f"  weighted sum={2*sum(q**d*rho[d].real for d in rho):+.4f}")


if __name__ == "__main__":
    main()
