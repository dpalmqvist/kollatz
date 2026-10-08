"""
Rigorous certificate for L^NT_k(lambda) (Krasikov–Lagarias 2003, eq. (2.8)-(2.14)).

Steps
 1. lam_cert = P / 10^6 (rational), slightly below the numerical optimum.
 2. Compute c by power iteration at lam_cert, scale and round UP... to integers C_m.
 3. Get rational LOWER bounds for lam^(alpha-2), lam^(alpha-1) by interval arithmetic.
 4. Check every inequality exactly with Python integers:
       C_m * P^2 <= C_{4m} * Q^2 + [P^2 * Cbar * lower(lam^(alpha-j))]   (j = 2 or 1)
    with Cbar = min over the three lifts mod 3^k.
 Positivity C_m >= 1 is automatic (C_m are positive integers, problem is homogeneous).
A pass proves L^NT_k(lam_cert) is feasible, hence by Theorem 2.2 of the paper
pi_a(x) >= x^gamma for every gamma < log2(lam_cert) and x >= x0(a, gamma).
"""
import sys
from fractions import Fraction
import numpy as np
import mpmath
from kl import structure, growth

mpmath.mp.prec = 200


def lower_power(lam_frac, exponent_shift):
    """Rational lower bound for lam^(log2(3) - shift), via mpmath interval arithmetic."""
    iv = mpmath.iv
    iv.prec = 200
    lam = iv.mpf(lam_frac.numerator) / lam_frac.denominator
    alpha = iv.log(iv.mpf(3)) / iv.log(iv.mpf(2))
    val = iv.exp((alpha - exponent_shift) * iv.log(lam))
    man, ex = mpmath.mpf(val.a).man_exp      # exact binary value of the lower endpoint
    lo = Fraction(int(man)) * (Fraction(2) ** int(ex))
    # round down to a rational with denominator 10^40 (still a valid lower bound)
    D = 10 ** 40
    return Fraction((lo.numerator * D) // lo.denominator, D)


def certify(k, lam_cert_str, scale=10 ** 9, iters=400000, c0=None):
    S = structure(k)
    lam = Fraction(lam_cert_str)
    _, _, c = growth(float(lam), S, iters=iters, tol=1e-14, c0=c0)
    # integer vector; rounding down the RHS-side terms is handled by exact check
    C = [int(x) for x in np.ceil(c / c.min() * scale)]
    N, n3 = S["N"], S["N"] // 3
    Cbar = [min(C[r], C[r + n3], C[r + 2 * n3]) for r in range(n3)]
    L2 = lower_power(lam, 2)   # lower bound of lam^(alpha-2)
    L1 = lower_power(lam, 1)   # lower bound of lam^(alpha-1)
    P2 = lam.numerator ** 2
    Q2 = lam.denominator ** 2
    # common denominator 10^40 for L1, L2
    D = 10 ** 40
    A2 = L2.numerator * (D // L2.denominator)
    A1 = L1.numerator * (D // L1.denominator)
    nxt, cls, aux = S["nxt"], S["cls"], S["aux"]
    Co = np.array(C, dtype=object)
    Cb = np.array(Cbar, dtype=object)
    lhs = Co * (P2 * D)
    rhs = Co[nxt] * (Q2 * D)
    s2 = np.where(cls == 2)[0]
    s8 = np.where(cls == 8)[0]
    rhs[s2] = rhs[s2] + Cb[aux[s2]] * (A2 * P2)
    rhs[s8] = rhs[s8] + Cb[aux[s8]] * (A1 * P2)
    diff = rhs - lhs
    bad = [i for i in range(N) if diff[i] < 0]
    if bad:
        return False, bad[0], None
    worst = min(float(Fraction(int(diff[i]), int(lhs[i]))) for i in range(0, N, max(1, N // 200000)))
    return True, None, (float(worst), max(C) / min(C))


if __name__ == "__main__":
    k = int(sys.argv[1])
    lam_str = sys.argv[2]
    c0 = np.load(sys.argv[3]) if len(sys.argv) > 3 else None
    iters = int(sys.argv[4]) if len(sys.argv) > 4 else 400000
    ok, bad, info = certify(k, lam_str, c0=c0, iters=iters)
    g = float(mpmath.log(mpmath.mpf(Fraction(lam_str).numerator) / Fraction(lam_str).denominator, 2))
    print(f"k={k} lam_cert={lam_str} log2(lam)={g:.6f} VERIFIED={ok}", "" if ok else f"fails at index {bad}",
          f"min relative slack (sampled)={info[0]:.3e} Cmax/Cmin={info[1]:.3f}" if ok else "")
