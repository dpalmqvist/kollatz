"""
Cycle analysis for the 3x+1 map T(n) = n/2 (n even), (3n+1)/2 (n odd)  -- the Eliahou argument.

A nontrivial cycle with n steps, k of them odd, elements x_i (the k odd ones), satisfies
    2^n = prod_{odd x_i} (3 + 1/x_i)                     (multiply the k factors (3x+1)/(2x) and the n-k factors 1/2)
so with m = min, M = max of the cycle
    k*log2(1 + 1/(3M))  <=  n - k*log2(3)  <=  k*log2(1 + 1/(3m)).                                   (E)
If every integer below 2^B is known to reach 1, a nontrivial cycle has m > 2^B and (E) forces n/k to be a
rational approximation of theta = log2(3) from above with error at most log2(1 + 1/(3*2^B)) ~ 1/(3 ln2 2^B).
Such fractions with small denominators are the upper semiconvergents of theta, so the smallest admissible n
is found by scanning them.  Eliahou (1993) did this with B = 40 and obtained n >= 17 087 915.

  python cycles.py [B ...]      default B = 40 60 68 71
"""
import sys

import mpmath

mpmath.mp.prec = 400
THETA = mpmath.log(3) / mpmath.log(2)


def continued_fraction(x, terms):
    a = []
    for _ in range(terms):
        f = int(mpmath.floor(x))
        a.append(f)
        x = x - f
        if x == 0:
            break
        x = 1 / x
    return a


def convergents(a):
    p0, q0, p1, q1 = 1, 0, a[0], 1
    out = [(p1, q1)]
    for ai in a[1:]:
        p0, q0, p1, q1 = p1, q1, ai * p1 + p0, ai * q1 + q0
        out.append((p1, q1))
    return out


def upper_approximations(a, kmax):
    """Fractions n/k > theta that are best one-sided approximations from above, denominators <= kmax:
    the convergents lying above theta and their semiconvergents (p_{i-1} + j p_i)/(q_{i-1} + j q_i)."""
    conv = convergents(a)
    out = []
    for i in range(1, len(conv)):
        (pprev, qprev), (p, q) = conv[i - 1], conv[i]
        # semiconvergents between conv[i-1] and conv[i+1] have the form (pprev + j p)/(qprev + j q), j = 1..a_{i+1}
        if i + 1 < len(a):
            for j in range(1, a[i + 1] + 1):
                nn, kk = pprev + j * p, qprev + j * q
                if kk > kmax:
                    break
                if mpmath.mpf(nn) / kk > THETA:
                    out.append((nn, kk))
        if q <= kmax and mpmath.mpf(p) / q > THETA:
            out.append((p, q))
    return sorted(set(out), key=lambda t: t[1])


def min_cycle_length(B, kmax=10 ** 14):
    c = mpmath.log(1 + mpmath.mpf(1) / (3 * mpmath.mpf(2) ** B)) / mpmath.log(2)   # bound on n/k - theta
    a = continued_fraction(THETA, 80)
    cands = []
    for n, k in upper_approximations(a, kmax):
        err = mpmath.mpf(n) / k - THETA
        if 0 < err <= c:
            cands.append((n, k, err))
    return c, cands


if __name__ == "__main__":
    Bs = [int(b) for b in sys.argv[1:]] or [40, 60, 68, 71]
    a = continued_fraction(THETA, 40)
    print("log2(3) =", mpmath.nstr(THETA, 40))
    print("continued fraction:", a)
    print("convergents n/k (first 22):", convergents(a)[:22])
    for B in Bs:
        c, cands = min_cycle_length(B)
        print(f"\nB = {B}: cycle minimum m > 2^{B}  =>  n/k - log2(3) <= {mpmath.nstr(c, 5)}")
        if not cands:
            print("  no admissible (n, k) below the denominator cap")
            continue
        n, k, err = cands[0]
        print(f"  smallest admissible cycle: n = {n} steps, k = {k} odd steps, n/k - theta = {mpmath.nstr(err, 5)}")
        print(f"  (every element of the cycle is >= m, so the cycle has at least {n} elements; k/n = {k / n:.6f})")
        print("  first admissible (n, k) in order of k:", [(nn, kk) for nn, kk, _ in cands[:6]])
