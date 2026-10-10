"""
m-cycles of the Collatz map: Hercher's bootstrap and the Simons-de Weger bounds it rests on, re-run for an
arbitrary verification bound X0 (avenue 13 in AVENUES.md).

Setting.  T(n) = n/2 (n even), (3n+1)/2 (n odd).  A nontrivial cycle of T is an *m-cycle* if it has m local
minima, i.e. it consists of m blocks "k_i >= 1 odd steps (ascent), then l_i >= 1 even steps (descent)",
i = 1..m ([SdW] section 1.2, [H] Definitions 5, 6).  K = sum k_i = number of odd elements, L = sum l_i = number
of even elements, delta = log 3/log 2 = log2 3 = [1; 1, 1, 2, 2, 3, 1, 5, 2, 23, 2, 2, 1, 1, 55, ...] with
convergents p_n/q_n (indexing as in [SdW]: q_19 = 397 573 379).  X0 is a number such that every n <= X0 is known
to reach 1, so every element of a nontrivial cycle is > X0.

Sources (local copies: scratchpad/hercher/, scratchpad/sdw/)
  [H]    C. Hercher, "There are no Collatz m-cycles with m <= 91", J. Integer Seq. 26 (2023) Art. 23.3.5
         (= arXiv:2201.00406v3); Corrigendum (JIS page, 14 June 2026) repairing the proof of Theorem 21, statement
         unchanged; the Sage worksheet Collatz-m-Cycle-Paper.ipynb on the JIS page (used for Theorem 23).
  [SdW]  J. Simons, B. de Weger, "Theoretical and computational bounds for m-cycles of the 3n+1 problem",
         Acta Arith. 117 (2005) 51-70 (X0 = 301*2^50; m <= 68), and the web version v1.44 (2010) (X0 = 5*2^60;
         m <= 75).  Lemma numbers below are those of v1.44 (they agree with the Acta version).
  [Rh]   G. Rhin, "Approximants de Pade et mesures effectives d'irrationalite", Progr. Math. 71 (1987) 155-164.

Upper bound for K (Simons-de Weger; does not use Hercher's lemmas)
  [SdW L4, C5]  0 < Lambda := (K+L) log 2 - K log 3 < sum_i 1/x_i <= m/X0          (x_i = local minima)
  [SdW L6, L7]  x_{i+1} < b^delta x_i^delta with b = (1 + 1/X0) 2^(-1/delta), hence
                Lambda < m c_m 2^(-(delta-1) K/(delta^m - 1)),
                c_m = (1 + 1/X0)^(m(delta-1)/(delta^m-1)) b^(delta/(delta-1) - delta m/(delta^m-1)).
  [SdW L12]     (from [Rh], Proposition p. 160)  Lambda > exp(-13.3 (0.46057 + log K)).
  [SdW L14]     K < K1(m) := largest root of exp(-13.3 (0.46057 + log x)) = m c_m 2^(-(delta-1) x/(delta^m - 1)).
  [SdW L9, L16] If K > J2(m) then Lambda < log 2/(2K), so (K+L)/K = p_n/q_n with n odd and q_n <= K < K1(m);
                hence a_{n+1} <= A(m) := max{a_j : j even, j <= n(m) - 2}, n(m) = least "champion" index with
                K1(m) < q_{n(m)-1}, and Lambda > log 2/((A(m)+2) K).  Therefore
                K < K2(m) := largest root of m c_m 2^(-(delta-1) x/(delta^m - 1)) = log 2/((A(m) + 2) x).
                Rhin's measure enters ONLY through A(m): for 64 <= m <= 511, K1(m) < q_217 ~ 1.3e106 and
                A(m) = a_14 = 55; any effective irrationality measure with K1(m) < q_217 gives the same K2(m).
  [H Thm 23] uses "K < 1.4784 m delta^m" = [SdW] Thm 3(d), i.e. K2(m) (k2(m) <= 1.4784 for m >= 91).
Lower bound for K (Simons-de Weger)
  [SdW L10]     If q_n + q_{n+1} <= X0 log 2/m then K > q_n  (generalised Crandall lemma; Corollary 11).
  [SdW L18]     Lattice / continued-fraction enumeration of all (K, L) with K < K2(m) that satisfy C5 and L7;
                m is excluded if there are none (this is how [SdW] reach m <= 68 resp. m <= 75).
Lower bound for K (Hercher)
  [H Thm 16]    delta < (K+L)/K < delta + S/(3 K log 2),  S = sum_i T(n_i),  T(n_i) = sum of 1/(odd elements of
                the ascent starting at the i-th local minimum n_i).
  Bounds for S:
  [H Cor 17]    S <= (97/54) m/X0                                     (analytic, any X0 > 765)
  [H Cor 19]    S <= (7/5) m/(695 * 2^60)                             (computer proof; needs X0 >= 695 * 2^60;
                                                                       weaker than Cor 17 once X0 >= 2^70.4)
  [H Thm 21]    (proof repaired in the Corrigendum; the statement and the bound are unchanged) for 1 <= m2 <= m with
                  ((delta^m2 - 1)/(delta - 1)) log2(162 X0/97) <= (m2/m) K,  v := (m2/m) K (delta - 1)/(delta^m2 - 1):
                  S < (97(m - m2) + 73)/(54 X0) + 3/(2^v - 1) + 3 (m2 - 1)/(2^v - 1)^delta     (m2 <= m - 2)
                  S < 3/X0 + 3/(2^v - 1) + 3 (m - 2)/(2^v - 1)^delta                         (m2 = m - 1)
                  S < 3/(2^v - 1) + 3 (m - 1)/(2^v - 1)^delta                                 (m2 = m)
  [H L22]       Every fraction in the open interval (delta, delta + d) has denominator >= q_min(d), the
                denominator of the simplest fraction in that interval.  (K+L)/K lies there, so K >= q_min(d).
  [H Thm 23]    Bootstrap (worksheet): from K >= K_lo take m2 = the largest admissible m2 at K_lo,
                d = min(bounds for S)/(3 K_lo log 2), K_lo <- q_min(d); repeat.  Valid because every bound for S/K
                is nonincreasing in K.  m is excluded once K_lo > K2(m).  Start: K_lo = 7*10^11 ([SdW] Thm 3(d)) in
                the worksheet; here by default the [SdW] L10 bound at the given X0 (the result is the same).
  Note: K and L are the numbers of odd/even elements of the cycle itself, so (K+L)/K need not be reduced; K is
  a multiple of the reduced denominator, which is what L22 bounds.

Rigour.  All decisions are made with exact rationals: delta is enclosed in [delta_lo, delta_hi] (width 1e-1100),
the bound d is rounded up before the simplest fraction in (delta_lo, delta_hi + d) is computed (a larger
interval can only lower q_min), and K2 is rounded up.  Partial quotients of delta are the common prefix of the
continued fractions of delta_lo and delta_hi.  The m2 premise is tested with a relative safety margin.

Exploratory extension (NOT part of [H] or [SdW]; flagged as such in the output): `survivors` enumerates all
(K, L) with K_lo <= K < K2(m) satisfying Hercher's inequality evaluated at the actual K (H Thm 16 + the best of
Cor 17/19/Thm 21 over all admissible m2), with the lattice enumeration of [SdW] L18.  If none survive, m is
excluded by [H]+[SdW] even where the bootstrap stalls.

Usage (.venv/bin/python mcycles.py ...):
  validate                     reproduce [H] Thm 23 and Cor 24, [SdW] Cor 11, the K1/K2 tables and L18 (both versions)
  run X0 [MMAX]                Hercher bootstrap for m = 1..MMAX at X0 (e.g. 2^71, 2075*2^60, 695*2^60)
  trace X0 m [K0]              print the bootstrap steps for one m
  lattice X0 m                 [SdW] L18 candidate list for one m
  survivors X0 m               exploratory: (K, L) surviving Hercher's inequality at their own K, below K2(m)
  needed M [M ...]             least X0 (in units of 2^60) at which the bootstrap excludes m
"""
import math
import sys
from fractions import Fraction

import mpmath
from mpmath import mp, mpf

mp.dps = 300

# ---------------------------------------------------------------------------------------------- constants
LOG2 = mpmath.log(2)
LOG3 = mpmath.log(3)
DELTA = LOG3 / LOG2


def _delta_enclosure(digits=1200):
    with mpmath.workdps(digits + 40):
        d = mpmath.log(3) / mpmath.log(2)
        man, exp = d.man_exp
        mid = Fraction(man) * Fraction(2) ** exp
    eps = Fraction(1, 10 ** (digits - 100))
    return mid - eps, mid + eps


DELTA_LO, DELTA_HI = _delta_enclosure()


def to_fraction(x):
    """Exact value of an mpf as a Fraction."""
    man, exp = mpf(x).man_exp
    return Fraction(man) * Fraction(2) ** exp


def cf_of_fraction(x, nmax):
    out = []
    for _ in range(nmax):
        a = x.numerator // x.denominator
        out.append(a)
        x = x - a
        if x == 0:
            break
        x = 1 / x
    return out


def _delta_cf(nmax=700):
    a_lo = cf_of_fraction(DELTA_LO, nmax + 2)
    a_hi = cf_of_fraction(DELTA_HI, nmax + 2)
    n = 0
    while n < min(len(a_lo), len(a_hi)) and a_lo[n] == a_hi[n]:
        n += 1
    n -= 1                                   # drop the last common term (safety)
    assert n >= nmax, "enclosure of delta too wide for the requested number of partial quotients"
    return a_lo[:nmax]


CF = _delta_cf()                             # rigorous partial quotients a_0 .. a_699 of delta


def _convergents(a):
    p, q = [a[0]], [1]
    pm, qm = 1, 0
    for ai in a[1:]:
        p.append(ai * p[-1] + pm)
        q.append(ai * q[-1] + qm)
        pm, qm = p[-2], q[-2]
    return p, q


P_CONV, Q_CONV = _convergents(CF)


def champions():
    """Even indices n with a_n > a_k for all even k < n ([SdW] section 6.2)."""
    out, best = [], -1
    for n in range(0, len(CF), 2):
        if CF[n] > best:
            out.append(n)
            best = CF[n]
    return out


CHAMPIONS = champions()


# ---------------------------------------------------------------------------------------------- helpers
def parse_x0(s):
    """'2^71', '2**71', '695*2^60', '301*2^50', '12345' -> int (no eval)."""
    s = s.replace("**", "^").replace(" ", "")
    val = 1
    for factor in s.split("*"):
        if "^" in factor:
            b, e = factor.split("^")
            val *= int(b) ** int(e)
        else:
            val *= int(factor)
    return val


def x0_str(X0):
    if X0 & (X0 - 1) == 0:
        return f"2^{X0.bit_length() - 1}"
    for e in (60, 50):
        if X0 % 2 ** e == 0:
            return f"{X0 // 2 ** e}*2^{e}"
    return str(X0)


def sci(x, digits=4):
    return mpmath.nstr(mpf(x), digits)


def simplest_in_open(lo, hi):
    """The fraction with the least denominator (and least numerator) strictly inside (lo, hi), 0 <= lo < hi
    (Stern-Brocot descent; equivalent to [H] Lemma 22)."""
    assert lo < hi
    fl = lo.numerator // lo.denominator
    if fl + 1 < hi:
        return Fraction(fl + 1)
    if lo == fl:
        t = 1 / (hi - fl)
        return fl + Fraction(1, t.numerator // t.denominator + 1)
    return fl + 1 / simplest_in_open(1 / (hi - fl), 1 / (lo - fl))


def qmin_above_delta(d_up):
    """Least denominator of a fraction in (delta, delta + d) for any d <= d_up (rigorous lower bound)."""
    return simplest_in_open(DELTA_LO, DELTA_HI + to_fraction(d_up) * (1 + Fraction(1, 10 ** 60)))


def largest_root(f, x_left, rel=mpf(10) ** -70):
    """Largest root of f on (x_left, inf), f(x_left) > 0 > f(+inf) assumed and f with one sign change there.
    Returns an upper bound for the root (the right end of the final bracket)."""
    lo = mpf(x_left)
    hi = lo * 2 + 10
    while f(hi) > 0:
        hi *= 2
    while (hi - lo) > rel * hi:
        mid = (lo + hi) / 2
        if f(mid) > 0:
            lo = mid
        else:
            hi = mid
    return hi


# ---------------------------------------------------------------------------------------------- [SdW] upper bounds
def c_m(m, X0):
    """[SdW] section 3.4."""
    X0 = mpf(X0)
    b = (1 + 1 / X0) / mpf(2) ** (1 / DELTA)
    dm = DELTA ** m - 1
    return (1 + 1 / X0) ** (m * (DELTA - 1) / dm) * b ** (DELTA / (DELTA - 1) - DELTA * m / dm)


def lambda_upper_log(m, X0, x):
    """log of the [SdW] Lemma 7 bound m c_m 2^(-(delta-1)x/(delta^m-1))."""
    return mpmath.log(m * c_m(m, X0)) - (DELTA - 1) * x * LOG2 / (DELTA ** m - 1)


def K1(m, X0, mu=mpf("13.3"), c0=mpf("0.46057")):
    """[SdW] Lemma 14 (Rhin's measure in the form of [SdW] Lemma 12)."""
    a = (DELTA - 1) * LOG2 / (DELTA ** m - 1)
    f = lambda x: lambda_upper_log(m, X0, x) - (-mu * (c0 + mpmath.log(x)))  # >0 : no contradiction yet
    return largest_root(f, mu / a)


def A_of_m(m, X0, k1=None):
    """[SdW] section 6.2: n(m) and A(m)."""
    if k1 is None:
        k1 = K1(m, X0)
    for n in CHAMPIONS:
        if n >= 1 and Q_CONV[n - 1] > k1:
            A = max(CF[j] for j in range(0, n - 1, 2))
            return n, A
    raise ValueError("continued fraction too short for this m")


def K2(m, X0, A=None):
    """[SdW] Lemma 16 (A(m) from the champion table)."""
    if A is None:
        A = A_of_m(m, X0)[1]
    a = (DELTA - 1) * LOG2 / (DELTA ** m - 1)
    f = lambda x: lambda_upper_log(m, X0, x) - mpmath.log(LOG2 / ((A + 2) * x))
    return largest_root(f, 1 / a)


def J2(m, X0):
    a = (DELTA - 1) * LOG2 / (DELTA ** m - 1)
    f = lambda x: lambda_upper_log(m, X0, x) - mpmath.log(LOG2 / (2 * x))
    return largest_root(f, 1 / a)


_K2_CACHE = {}


def K2_cached(m, X0):
    key = (m, X0)
    if key not in _K2_CACHE:
        _K2_CACHE[key] = K2(m, X0)
    return _K2_CACHE[key]


def lemma10_lower(m, X0):
    """[SdW] Lemma 10: K > q_n for the largest n with q_n + q_{n+1} <= X0 log 2/m.  Returns (n, q_n)."""
    bound = mpf(X0) * LOG2 / m
    best = None
    for n in range(4, len(Q_CONV) - 1):
        if Q_CONV[n] + Q_CONV[n + 1] <= bound:
            best = n
        else:
            break
    return best, (Q_CONV[best] if best is not None else 0)


# ---------------------------------------------------------------------------------------------- [H] bounds for S
H19_X0 = 695 * 2 ** 60
SAFE = 1 + mpf(10) ** -40                   # relative margin in the m2 premise


def m2_admissible(m, K, X0, m2):
    """Premise of [H] Theorem 21 (tested with a small safety margin)."""
    lhs = (DELTA ** m2 - 1) / (DELTA - 1) * mpmath.log(mpf(162) * X0 / 97) / LOG2
    return lhs * SAFE <= mpf(m2) / m * K


def m2_largest(m, K, X0):
    """As in Hercher's worksheet: increase m2 while the premise holds (the premise holds on an initial segment)."""
    m2 = 0
    while m2 + 1 <= m and m2_admissible(m, K, X0, m2 + 1):
        m2 += 1
    return m2


def thm21_bound(m, K, X0, m2):
    """[H] Theorem 21 bound for S (upper bound, with (2^v - 1)^delta as in the paper and worksheet)."""
    X0 = mpf(X0)
    v = mpf(m2) / m * K * (DELTA - 1) / (DELTA ** m2 - 1)
    t = mpf(2) ** v - 1
    tail = 3 / t + 3 * (m2 - 1) / t ** DELTA
    if m2 == m:
        head = mpf(0)
    elif m2 == m - 1:
        head = 3 / X0
    else:
        head = (97 * (m - m2) + 73) / (54 * X0)
    return head + tail


def S_bound(m, K, X0, m2_mode="largest"):
    """Upper bound for S = sum T(n_i) at odd-element count >= K.  Returns (bound, label, m2).
    m2_mode = 'largest' (Hercher's worksheet) or 'best' (min over all admissible m2; also valid by Thm 21)."""
    K = mpf(K)
    cands = [((mpf(97) / 54) * m / mpf(X0), "Cor17", 0)]
    if X0 >= H19_X0:
        cands.append(((mpf(7) / 5) * m / mpf(H19_X0), "Cor19", 0))
    m2max = m2_largest(m, K, X0)
    if m2max >= 1:
        m2s = [m2max] if m2_mode == "largest" else range(1, m2max + 1)
        for m2 in m2s:
            cands.append((thm21_bound(m, K, X0, m2), "Thm21", m2))
    best = min(cands, key=lambda c: c[0])
    return best[0], best[1], (m2max if m2_mode == "largest" else best[2])


def d_bound(m, K, X0, m2_mode="largest"):
    S, lab, m2 = S_bound(m, K, X0, m2_mode)
    return S / (3 * mpf(K) * LOG2) * (1 + mpf(10) ** -50), lab, m2


# ---------------------------------------------------------------------------------------------- [H] bootstrap
def bootstrap(m, X0, K0=None, kup=None, m2_mode="largest", maxit=200):
    """Hercher's Theorem 23 iteration.  Returns dict with keys excluded, K_lo, K2, steps, block."""
    if kup is None:
        kup = K2_cached(m, X0)
    if K0 is None:
        K0 = max(lemma10_lower(m, X0)[1] + 1, 2 * m)
    K = int(K0)
    steps = []
    block = None
    for _ in range(maxit):
        if K > kup:
            break
        d, lab, m2 = d_bound(m, K, X0, m2_mode)
        fr = qmin_above_delta(d)
        q = fr.denominator
        steps.append((m2, lab, d, q))
        if q <= K:
            block = fr
            break
        K = q
    return {"m": m, "X0": X0, "excluded": K > kup, "K_lo": K, "K2": kup, "steps": steps, "block": block}


# ---------------------------------------------------------------------------------------------- lattice enumeration
def _rdiv(a, b):
    """nearest integer to a/b, b > 0"""
    return (2 * a + b) // (2 * b)


def strip_points(Kmin, Kmax, eps):
    """All integer (K, P) with Kmin <= K <= Kmax and 0 < P - K delta < eps (exact filter at the end).
    2-D lattice reduction as in [SdW] section 7.2, in exact integer arithmetic."""
    Kmin, Kmax = int(Kmin), int(Kmax)
    eps = mpf(eps)
    s = Kmax.bit_length() + int(mpmath.ceil(-mpmath.log(eps, 2))) + 24
    S = 1 << s
    with mpmath.workprec(s + 128):
        D = int(mpmath.floor(mpmath.log(3) / mpmath.log(2) * S))
    E = int(mpmath.ceil(eps * S)) + Kmax + 2                      # Y = P S - K D lies in [1, E]
    # weighted coordinates (u, w) = (K E, Y Kmax); basis images of (K, P) = (1, 0), (0, 1)
    def img(k, p):
        return (k * E, (p * S - k * D) * Kmax)
    b1, c1 = (1, 0), img(1, 0)
    b2, c2 = (0, 1), img(0, 1)
    dot = lambda x, y: x[0] * y[0] + x[1] * y[1]
    if dot(c1, c1) > dot(c2, c2):
        b1, c1, b2, c2 = b2, c2, b1, c1
    while True:
        n1 = dot(c1, c1)
        mu = _rdiv(dot(c1, c2), n1)
        b2 = (b2[0] - mu * b1[0], b2[1] - mu * b1[1])
        c2 = (c2[0] - mu * c1[0], c2[1] - mu * c1[1])
        if dot(c2, c2) >= n1:
            break
        b1, c1, b2, c2 = b2, c2, b1, c1
    R = Kmax * E
    with mpmath.workdps(60):
        cx, cy = mpf(R) / 2, mpf(R) / 2
        rad = mpf(R) / mpmath.sqrt(2) * (1 + mpf(10) ** -20) + 2
        det = mpf(c1[0]) * c2[1] - mpf(c1[1]) * c2[0]
        z1c = (cx * c2[1] - cy * c2[0]) / det                      # centre in lattice coordinates
        z2c = (mpf(c1[0]) * cy - mpf(c1[1]) * cx) / det
        n1 = mpf(dot(c1, c1))
        mu = mpf(dot(c1, c2)) / n1
        n2s = mpf(dot(c2, c2)) - mu * mu * n1
        out = []
        r2 = rad / mpmath.sqrt(n2s)
        for z2 in range(int(mpmath.floor(z2c - r2)) - 1, int(mpmath.ceil(z2c + r2)) + 2):
            t = z2 - z2c
            rem = rad * rad - t * t * n2s
            if rem < 0:
                continue
            ctr = z1c - mu * t
            half = mpmath.sqrt(rem / n1)
            for z1 in range(int(mpmath.floor(ctr - half)) - 1, int(mpmath.ceil(ctr + half)) + 2):
                k = z1 * b1[0] + z2 * b2[0]
                p = z1 * b1[1] + z2 * b2[1]
                if Kmin <= k <= Kmax:
                    out.append((k, p))
    res = []
    for k, p in set(out):
        t = p - k * DELTA
        if 0 < t < eps:
            res.append((k, p))
    return sorted(res)


def sdw_candidates(m, X0, Kmax=None, primitive=False):
    """[SdW] Lemma 18: all (K, L) with K < K2(m), 0 < Lambda < m/X0 (Cor 5) and Lambda below Lemma 7.
    primitive=True keeps only gcd(K, K+L) = 1, which is what the tables of [SdW] list: a multiple j(K', L') of a
    candidate has Lambda multiplied by j, so its primitive base is also a candidate and fails at a larger X0."""
    if Kmax is None:
        Kmax = int(mpmath.floor(K2_cached(m, X0)))
    eps = mpf(m) / (mpf(X0) * LOG2)
    out = []
    for k, p in strip_points(1, Kmax, eps):
        lam = (p - k * DELTA) * LOG2
        if k >= m and p - k >= m and mpmath.log(lam) < lambda_upper_log(m, X0, k):
            if not primitive or math.gcd(k, p) == 1:
                out.append((k, p - k, lam))
    return out


def hercher_survivors(m, X0, Klo=None, kup=None, m2_mode="best"):
    """EXPLORATORY: all (K, L), Klo <= K < K2(m), with (K+L)/K - delta < S(K)/(3 K log 2) at their own K."""
    if kup is None:
        kup = K2_cached(m, X0)
    if Klo is None:
        Klo = bootstrap(m, X0, kup=kup)["K_lo"]
    Kmax = int(mpmath.floor(kup))
    out = []
    lo = int(Klo)
    while lo <= Kmax:
        hi = min(2 * lo, Kmax)
        S0, _, _ = S_bound(m, lo, X0, m2_mode)
        eps = S0 / (3 * LOG2) * (1 + mpf(10) ** -30)              # P - K delta < S(K)/(3 log 2) <= S(lo)/(3 log 2)
        for k, p in strip_points(lo, hi, eps):
            S, lab, m2 = S_bound(m, k, X0, m2_mode)
            t = p - k * DELTA
            if t < S / (3 * LOG2):
                out.append((k, p - k, t * 3 * LOG2 / S, lab, m2))
        lo = hi + 1
    return out


# ---------------------------------------------------------------------------------------------- reports
def print_trace(res):
    for m2, lab, d, q in res["steps"]:
        print(f"    m2 = {m2:3d} ({lab}), d = {sci(d, 3):>9}, K >= {q} ({sci(q, 3)})")
    if res["excluded"]:
        print(f"    => K >= {sci(res['K_lo'], 4)} > K2({res['m']}) = {sci(res['K2'], 5)}: EXCLUDED")
    else:
        fr = res["block"]
        print(f"    => stalls at K >= {sci(res['K_lo'], 4)} < K2({res['m']}) = {sci(res['K2'], 5)}; "
              f"blocking fraction {fr.numerator}/{fr.denominator} (denominator {sci(fr.denominator, 4)})")


def cmd_run(X0, mmax=130, K0=None, m2_mode="largest", quiet=False):
    print(f"Hercher bootstrap at X0 = {x0_str(X0)} = 2^{float(mpmath.log(X0, 2)):.4f}, m2 mode = {m2_mode}"
          + (f", K0 = {K0}" if K0 else ", K0 = [SdW] Lemma 10 at this X0"))
    first_fail = None
    rows = []
    for m in range(1, mmax + 1):
        res = bootstrap(m, X0, K0=K0, m2_mode=m2_mode)
        rows.append(res)
        if not res["excluded"] and first_fail is None:
            first_fail = m
        if not quiet and (m >= 85 or not res["excluded"]):
            st = "excluded" if res["excluded"] else "NOT excluded"
            print(f"  m = {m:4d}: {st:12s} steps {len(res['steps']):2d}, final K >= {sci(res['K_lo'], 4):>10}, "
                  f"K2 = {sci(res['K2'], 5):>11}" + (f", blocked by denominator {sci(res['block'].denominator, 5)}"
                                                     if res["block"] is not None else ""))
    excluded = [r["m"] for r in rows if r["excluded"]]
    print(f"  all m <= {first_fail - 1 if first_fail else mmax} excluded; "
          f"excluded m above that: {[m for m in excluded if first_fail and m > first_fail]}")
    return rows


def needed_x0(m, lo=60.0, hi=90.0, K0=None, m2_mode="largest"):
    """Least X0 = c * 2^60 (integer c) at which the bootstrap excludes m (assumes monotonicity, checked)."""
    clo, chi = int(2 ** (lo - 60)) or 1, int(2 ** (hi - 60))
    if not bootstrap(m, chi * 2 ** 60, K0=K0, m2_mode=m2_mode)["excluded"]:
        return None
    while chi - clo > 1:
        mid = (clo + chi) // 2
        if bootstrap(m, mid * 2 ** 60, K0=K0, m2_mode=m2_mode)["excluded"]:
            chi = mid
        else:
            clo = mid
    return chi


# ---------------------------------------------------------------------------------------------- validation
def matches(x, s, how):
    """Does x agree with the printed value s (rounded or truncated to the digits shown)?"""
    mant, ex = s.lower().split("e") if "e" in s.lower() else (s, "0")
    decimals = len(mant.split(".")[1]) if "." in mant else 0
    unit = mpf(10) ** (int(ex) - decimals)
    x, v = mpf(x), mpf(s)
    if how == "trunc":
        return v <= x < v + unit
    if how == "ceil":
        return v - unit < x <= v
    return abs(x - v) <= unit / 2


def rounded(x, nd, how):
    e = int(mpmath.floor(mpmath.log10(x)))
    u = mpf(10) ** (e - nd + 1)
    return (mpmath.floor(mpf(x) / u) if how == "trunc" else mpmath.nint(mpf(x) / u)) * u


def check(label, ok):
    print(f"  [{'OK' if ok else 'FAIL'}] {label}")
    return ok


def known_diff(label, holds, note):
    """A documented discrepancy with the paper (explained in `note`); `holds` checks our side of it."""
    print(f"  [{'DIFF' if holds else 'FAIL'}] {label}\n         -> {note}")
    return holds


def cmd_validate():
    allok = True
    print("Continued fraction of delta and [SdW] convergent indexing")
    allok &= check(f"a_0..a_14 = {CF[:15]}", CF[:15] == [1, 1, 1, 2, 2, 3, 1, 5, 2, 23, 2, 2, 1, 1, 55])
    allok &= check(f"q_18, q_19, q_20, q_21 = {Q_CONV[18]}, {Q_CONV[19]}, {Q_CONV[20]}, {Q_CONV[21]}",
                   (Q_CONV[18], Q_CONV[19], Q_CONV[20], Q_CONV[21]) == (225644606, 397573379, 6189245291, 6586818670))
    allok &= check(f"even-index champions start {CHAMPIONS[:8]} with a = {[CF[n] for n in CHAMPIONS[:8]]}; "
                   "[SdW] table: n(m) = 218, 230, 330, 528 with A = 55, 100, 964, 2436",
                   CHAMPIONS[CHAMPIONS.index(14) + 1: CHAMPIONS.index(14) + 4] == [218, 230, 330]
                   and [CF[218], CF[230], CF[330]] == [100, 964, 2436])

    print("\n[SdW] v1.44 (X0 = 5*2^60): K1, J2, K2 tables (section 6)")
    X0 = 5 * 2 ** 60
    tab_k1 = {2: "3.0877e2", 10: "3.5858e4", 63: "4.8181e15", 64: "7.7350e15", 100: "1.7876e23", 511: "1.3035e106",
              512: "2.0698e106"}
    for m, s in tab_k1.items():
        v = K1(m, X0)
        allok &= check(f"K1({m}) = {sci(v, 6)}  (paper: < {s})", v < mpf(s) and v > mpf(s) * (1 - mpf(1e-4)))
    tab_k2 = {64: ("5.9379e14", "6.4742e14"), 67: ("2.4553e15", "2.6686e15"), 68: ("3.9396e15", "4.2776e15"),
              90: ("1.2542e20", "1.3388e20"), 91: ("2.0068e20", "2.1408e20"), 100: ("1.3737e22", "1.4582e22"),
              511: ("9.9079e104", "1.0043e105"), 512: ("1.5734e105", "1.5984e105")}
    for m, (sj, sk) in tab_k2.items():
        j, k = J2(m, X0), K2(m, X0)
        n, A = A_of_m(m, X0)
        allok &= check(f"m = {m}: n(m) = {n}, A(m) = {A}, J2 = {sci(j, 6)} (< {sj}), K2 = {sci(k, 6)} (< {sk})",
                       j < mpf(sj) and j > mpf(sj) * (1 - mpf(1e-4)) and k < mpf(sk) and k > mpf(sk) * (1 - mpf(1e-4)))
    k = K2(91, X0) / (91 * DELTA ** 91)
    allok &= check(f"k2(91) = K2(91)/(91 delta^91) = {sci(k, 6)} (paper: 1.4784)", abs(k - mpf("1.4784")) < 1e-4)

    print("\n[SdW] v1.44 Corollary 11 (X0 = 5*2^60): K > q_n by Lemma 10")
    cor11 = [(6, 34), (7, 33), (10, 33), (11, 32), (29, 32), (30, 31), (333, 31), (334, 30), (640, 30), (641, 29),
             (4367, 29), (4368, 28), (648401, 24), (648402, 23)]
    ok = all(lemma10_lower(m, X0)[0] == n for m, n in cor11)
    allok &= check("index n(m) at the range boundaries 6/7, 10/11, 29/30, 333/334, 640/641, 4367/4368, 648401/648402",
                   ok)
    allok &= check(f"q_31 = {Q_CONV[31]} (> 5.7509e15), q_24 = {Q_CONV[24]} (> 7.5311e11)",
                   mpf("5.7509e15") < Q_CONV[31] < mpf("5.7510e15") and mpf("7.5311e11") < Q_CONV[24] < mpf("7.5312e11"))
    m_l15 = next(m for m in range(2, 200) if not K1(m, X0) < lemma10_lower(m, X0)[1]) - 1
    m_l17 = next(m for m in range(2, 200) if not K2_cached(m, X0) < lemma10_lower(m, X0)[1]) - 1
    allok &= check(f"Lemma 15 (K1 vs Lemma 10): no m-cycles for m <= {m_l15} (paper: 63)", m_l15 == 63)
    allok &= check(f"Lemma 17 (K2 vs Lemma 10): no m-cycles for m <= {m_l17} (paper: 68)", m_l17 == 68)

    print("\n[SdW] v1.44 Lemma 18 (X0 = 5*2^60): lattice enumeration (tables list primitive (K, L) only)")
    none = [m for m in range(69, 76) if sdw_candidates(m, X0)]
    allok &= check(f"no candidates at all (primitive or not) for 69 <= m <= 75 (m with candidates: {none})", none == [])
    c76 = sdw_candidates(76, X0, primitive=True)
    c77 = sdw_candidates(77, X0, primitive=True)
    exp76 = [(117972833293231014, 69009683580368485), (124207383220472977, 72656661496678846),
             (130441933147714940, 76303639412989207)]
    exp77 = sorted(exp76 + [(254649316368187917, 148960300909668053)])
    allok &= check(f"m = 76: {[(k, l) for k, l, _ in c76]}", [(k, l) for k, l, _ in c76] == exp76)
    allok &= check(f"m = 77: the 4 primitive candidates of the paper", [(k, l) for k, l, _ in c77] == exp77)
    fall76 = [m_over_lam / 2 ** 60 for m_over_lam in (76 / lam for _, _, lam in c76)]
    fall77 = [77 / lam / 2 ** 60 for _, _, lam in c77]
    exp_f76, exp_f77 = ["5.39", "9.39", "36.8"], ["5.46", "9.52", "37.3", "7.58"]
    allok &= check(f"'falls when X0 >=' m/Lambda = {[sci(f, 5) for f in fall76]} (m = 76), "
                   f"{[sci(f, 5) for f in fall77]} (m = 77) * 2^60; paper (rounded up): {exp_f76}, {exp_f77}",
                   all(matches(f, s, "ceil") for f, s in zip(fall76, exp_f76))
                   and all(matches(f, s, "ceil") for f, s in zip(fall77, exp_f77)))
    m77all = sdw_candidates(77, X0)
    extra = [(k, l) for k, l, _ in m77all if (k, l) not in exp77]
    allok &= known_diff(f"m = 77 also admits the non-primitive {extra}", extra == [(260883866295429880,
                                                                                    152607278825978414)],
                        "= 2 x (130441933147714940, 76303639412989207); not listed by [SdW], harmless (dominated)")
    counts = {78: 6, 79: 9, 80: 12, 81: 19, 82: 33, 83: 52, 84: 86, 85: 136, 86: 220, 87: 352, 88: 565, 89: 909,
              90: 1456}
    got = {m: sdw_candidates(m, X0, primitive=True) for m in counts}
    agree = [m for m, c in counts.items() if len(got[m]) == c]
    allok &= check(f"counts m = 78..90: {[len(got[m]) for m in counts]}, paper: {list(counts.values())}; "
                   f"agree except m = {[m for m in counts if m not in agree]}", agree == [m for m in counts if m != 80])
    allok &= known_diff("m = 80: 13 primitive candidates vs 12 in the paper",
                        len(got[80]) == 13 and len(got[79]) == 9 and len(got[81]) == 19
                        and max(k for k, _, _ in got[80]) == 1049770015108961483,
                        "paper's own max K = 1049770015108961483 and the m = 79/81 counts agree; none of the 13 is "
                        "borderline (Lambda/(m/X0) <= 0.90, Lambda/L7 <= 0.983); most likely a typo, harmless")
    kmin = min(k for k, _, _ in got[90])
    lam_paper = (177100989030047175 - 111738283365989051 * DELTA) * LOG2
    allok &= known_diff(f"m = 78..90: min K = {kmin} vs paper 111 738 283 365 989 051",
                        kmin == 117972833293231014 and lam_paper > mpf(90) / X0,
                        f"the paper's K has Lambda = {sci(lam_paper, 4)} > 90/X0 = {sci(mpf(90) / X0, 4)}: it fails "
                        "Cor 5 at X0 = 5*2^60 (leftover from a smaller X0?); the paper's lower bound K > 1.1173e17 "
                        "is weaker than ours, so harmless")
    allok &= check(f"m = 90: max K = {max(k for k, _, _ in got[90])} (paper 1.1442e20)",
                   matches(max(k for k, _, _ in got[90]), "1.1442e20", "round"))

    print("\n[SdW] Acta Arith. 2005 (X0 = 301*2^50): Lemma 18 (primitive (K, L))")
    X0a = 301 * 2 ** 50
    none = [m for m in range(64, 69) if sdw_candidates(m, X0a)]
    allok &= check(f"no candidates at all for 64 <= m <= 68 (m with candidates: {none})", none == [])
    lists = {69: [(5750934602875680, 3364081086781987)], 70: [(5750934602875680, 3364081086781987)],
             71: [(5750934602875680, 3364081086781987), (11985484530117643, 7011059003092348)],
             72: [(5750934602875680, 3364081086781987), (11985484530117643, 7011059003092348),
                  (17736419132993323, 10375140089874335), (18220034457359606, 10658036919402709),
                  (24454584384601569, 14305014835713070)]}
    falls = {69: ["577"], 70: ["585"], 71: ["593", "624"], 72: ["602", "633", "309", "667", "706"]}
    for m, exp in lists.items():
        c = sdw_candidates(m, X0a, primitive=True)
        g = [(k, l) for k, l, _ in c]
        fx = [m / lam / 2 ** 50 for _, _, lam in c]
        allok &= check(f"m = {m}: {len(g)} candidate(s) as listed; falls when X0 >= {[sci(f, 4) for f in fx]} * 2^50 "
                       f"(paper {falls[m]})", g == exp and all(matches(f, s, "ceil") for f, s in zip(fx, falls[m])))
    countsa = {73: 8, 74: 15, 75: 24, 76: 36, 77: 54, 78: 82, 79: 135, 80: 213, 81: 332, 82: 535, 83: 845, 84: 1370,
               85: 2190, 86: 3507, 87: 5623, 88: 9017, 89: 14457, 90: 23181}
    gota = {m: sdw_candidates(m, X0a, primitive=True) for m in countsa}
    allok &= check(f"counts m = 73..90: {[len(v) for v in gota.values()]}", {m: len(v) for m, v in gota.items()} == countsa)
    allok &= check(f"min K for 74..90 = {min(k for k, _, _ in gota[90])} (paper 5 267 319 278 509 397), "
                   f"max K for m = 73, 90: {max(k for k, _, _ in gota[73])}, {sci(max(k for k, _, _ in gota[90]), 5)} "
                   "(paper 36 923 684 239 085 495, 1.1442e20)",
                   all(min(k for k, _, _ in gota[m]) == 5267319278509397 for m in range(74, 91))
                   and max(k for k, _, _ in gota[73]) == 36923684239085495)

    bad = [m for m in range(2, 64) if not K2_cached(m, X0a) < lemma10_lower(m, X0a)[1]]
    allok &= check(f"m <= 63 by K2(m) < Lemma 10 bound at X0 = 301*2^50 (failures {bad}); with 64..68 => m <= 68",
                   bad == [])

    print("\n[H] abstract: 'with newer bounds on X0 [695*2^60] one gets m >= 83' from the [SdW] method")
    Xh = 695 * 2 ** 60
    first = next(m for m in range(2, 100) if not K2_cached(m, Xh) < lemma10_lower(m, Xh)[1]
                 and sdw_candidates(m, Xh, primitive=True))
    allok &= check(f"[SdW] Lemma 10/17 + Lemma 18 at X0 = 695*2^60: first m with candidates = {first} (=> m >= 83)",
                   first == 83)

    print("\n[H] Theorem 23 (X0 = 695*2^60, m = 91, K0 = 7*10^11 as in the worksheet)")
    Xh = 695 * 2 ** 60
    res = bootstrap(91, Xh, K0=7 * 10 ** 11)
    print_trace(res)
    exp = [(47, "6.9e-32", "5.2e15"), (67, "5.1e-36", "3.97e17"), (77, "4.1e-38", "4.64e18"),
           (82, "2.3e-39", "2.74e19"), (86, "2.3e-40", "7.76e19"), (88, "5.3e-41", "2.05e20"),
           (91, "1.11e-43", "7.94e21")]
    got = [(m2, sci(d, 3), sci(q, 4)) for (m2, _, d, q) in res["steps"]]
    allok &= check(f"m2 and K sequence {[(g[0], g[2]) for g in got]}\n         paper: {[(e[0], e[2]) for e in exp]}"
                   " (paper truncates K)", len(res["steps"]) == 7 and all(
                       g[0] == e[0] and matches(res["steps"][i][3], e[2], "trunc") for i, (g, e) in enumerate(zip(got, exp))))
    # the printed d of steps 3, 6, 7 are reproduced only when K is re-entered rounded to 2-3 digits (worksheet use)
    Kin = [7 * 10 ** 11] + [q for (_, _, _, q) in res["steps"][:-1]]
    how = []
    for i, e in enumerate(exp):
        found = None
        for lab, kk in [("exact", mpf(Kin[i]))] + [(f"{w}{nd}", rounded(Kin[i], nd, w)) for nd in (2, 3)
                                                   for w in ("trunc", "round")]:
            dd = d_bound(91, kk, Xh)[0]
            if matches(dd, e[1], "round") or matches(dd, e[1], "trunc"):
                found = f"{lab} K = {sci(kk, 3)}"
                break
        how.append(found)
    allok &= check(f"printed d reproduced from K as typed: {how}", all(how))
    allok &= check(f"first step: simplest fraction denominator {res['steps'][0][3]} (worksheet: 5267319278509397)",
                   res["steps"][0][3] == 5267319278509397)
    allok &= check(f"final K = {sci(res['K_lo'], 3)} > K2(91) = {sci(res['K2'], 4)} (paper: 7.94e21 > 2.2e20)",
                   res["excluded"])
    fails = [m for m in range(1, 92) if not bootstrap(m, Xh, K0=7 * 10 ** 11)["excluded"]]
    allok &= check(f"every m <= 91 excluded with K0 = 7e11 (failures: {fails})", fails == [])
    fails = [m for m in range(1, 92) if not bootstrap(m, Xh)["excluded"]]
    allok &= check(f"every m <= 91 excluded with K0 from [SdW] Lemma 10 (failures: {fails})", fails == [])
    allok &= check("m = 92 NOT excluded at X0 = 695*2^60", not bootstrap(92, Xh)["excluded"])

    print("\n[H] Corollary 24 / Table 1 (X0 = 695*2^60): 'if m <= M then K > ...' (K0 = 7.2e10, the m-free bound)")
    rows = [(98, "7.76e19"), (117, "2.74e19"), (276, "4.68e18"), (3079, "3.97e17"), (12055, "1.30e17")]
    for M, s in rows:
        r = bootstrap(M, Xh, K0=72 * 10 ** 9, kup=mpf(10) ** 40)
        r2 = bootstrap(M + 1, Xh, K0=72 * 10 ** 9, kup=mpf(10) ** 40)
        if M == 276:
            allok &= known_diff(f"m = 276: K >= {r['K_lo']} = {sci(r['K_lo'], 4)} vs paper 4.68e18; "
                                f"m = 277: K >= {sci(r2['K_lo'], 4)}",
                                r["K_lo"] == 4640282259296926456 and r2["K_lo"] < r["K_lo"],
                                "no fraction above delta has a denominator in (4.64e18, 2.74e19) that is a best "
                                "upper approximation, so 4.68e18 cannot occur: typo for 4.64e18; m-boundary 276/277 agrees")
            continue
        allok &= check(f"m = {M}: K >= {sci(r['K_lo'], 4)} (paper {s}); m = {M + 1}: K >= {sci(r2['K_lo'], 4)}",
                       (matches(r["K_lo"], s, "trunc") or matches(r["K_lo"], s, "round")) and r2["K_lo"] < r["K_lo"])
    print("\nALL VALIDATION CHECKS PASSED" if allok else "\nSOME VALIDATION CHECKS FAILED")
    return allok


# ---------------------------------------------------------------------------------------------- main
def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return
    cmd = argv[0]
    if cmd == "validate":
        ok = cmd_validate()
        sys.exit(0 if ok else 1)
    elif cmd == "run":
        X0 = parse_x0(argv[1])
        mmax = int(argv[2]) if len(argv) > 2 else 130
        mode = "best" if "--best-m2" in argv else "largest"
        K0 = None
        for a in argv:
            if a.startswith("--K0="):
                K0 = int(mpf(a[5:]))
        cmd_run(X0, mmax, K0=K0, m2_mode=mode)
    elif cmd == "trace":
        X0, m = parse_x0(argv[1]), int(argv[2])
        K0 = int(mpf(argv[3])) if len(argv) > 3 else None
        print(f"X0 = {x0_str(X0)}, m = {m}, K2(m) = {sci(K2_cached(m, X0), 6)}, A(m) = {A_of_m(m, X0)}")
        print_trace(bootstrap(m, X0, K0=K0))
    elif cmd == "lattice":
        X0, m = parse_x0(argv[1]), int(argv[2])
        c = sdw_candidates(m, X0)
        print(f"[SdW] L18 at X0 = {x0_str(X0)}, m = {m}: {len(c)} candidate(s) below K2 = {sci(K2_cached(m, X0), 6)}")
        for k, l, lam in c[:50]:
            print(f"  K = {k}, L = {l}, falls when X0 >= {sci(m / lam / 2 ** 60, 4)} * 2^60")
    elif cmd == "survivors":
        X0, m = parse_x0(argv[1]), int(argv[2])
        res = bootstrap(m, X0)
        sv = hercher_survivors(m, X0, Klo=res["K_lo"], kup=res["K2"])
        print(f"EXPLORATORY: X0 = {x0_str(X0)}, m = {m}, bootstrap K >= {res['K_lo']}, K2 = {sci(res['K2'], 6)}: "
              f"{len(sv)} (K, L) satisfy Hercher's inequality at their own K")
        for k, l, ratio, lab, m2 in sv[:50]:
            print(f"  K = {k}, L = {l}, (P - K delta)/(S(K)/(3 log 2)) = {sci(ratio, 5)} [{lab}, m2 = {m2}]")
    elif cmd == "needed":
        for m in [int(a) for a in argv[1:]]:
            c = needed_x0(m)
            print(f"  m = {m}: bootstrap excludes m once X0 >= {c} * 2^60 = 2^{math.log2(c) + 60:.3f}"
                  if c else f"  m = {m}: not excluded below 2^90")
    else:
        print(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
