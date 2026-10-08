"""
Independent check of lambda_k (plan item 7b): L^NT_k(lambda) solved as an actual linear program (HiGHS via
scipy), with the constraints built directly from residues m with Python integers.  Shares no code or index
formulas with kl.py / kl_mlx.py / certify*.py.

For each k: bisection on lambda for LP feasibility -> lambda_k (compare with K-L Table 2 and our values);
then an LP solution at lambda_lo = floor(lambda_k * 10^6) / 10^6 - 2e-6 (right-hand sides shrunk by 1e-7 so the
solution has slack) is verified EXACTLY with Fractions
(rational lambda, rigorous rational lower bounds for lambda^(alpha-1), lambda^(alpha-2)), and the LP at
lambda_lo + 1e-4 is checked to be infeasible.

  python lp_check.py [KMAX]      (default 9; k = 10 takes a few minutes)
"""
import sys
import time
from fractions import Fraction

import mpmath
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix

TABLE2 = {2: 1.3534010, 3: 1.5275960, 4: 1.6122870, 5: 1.6627590, 6: 1.6944520, 7: 1.7201900,
          8: 1.7449630, 9: 1.7615320, 10: 1.7771270, 11: 1.7922310}
OURS = {12: 1.8064236, 13: 1.8188237}


def build(k):
    """Variables: c_m for m in [3^k] (m = 2 mod 3), then cbar_r for r in [3^(k-1)].  Returns index maps and
    the constraint rows as lists of (m, type, 4m, r) and (r, lift)."""
    M, Mk1 = 3 ** k, 3 ** (k - 1)
    ms = [m for m in range(M) if m % 3 == 2]
    rs = [r for r in range(Mk1) if r % 3 == 2]
    ci = {m: i for i, m in enumerate(ms)}
    ri = {r: len(ms) + i for i, r in enumerate(rs)}
    rows = []
    for m in ms:
        m4 = (4 * m) % M
        if m % 9 == 2:
            rows.append((m, 2, m4, ((4 * m - 2) // 3) % Mk1))
        elif m % 9 == 5:
            rows.append((m, 5, m4, None))
        else:
            rows.append((m, 8, m4, ((2 * m - 1) // 3) % Mk1))
    lifts = [(r, (r + t * Mk1) % M) for r in rs for t in range(3)]
    for r, lift in lifts:
        assert lift % 3 == 2 and lift in ci
    return ms, rs, ci, ri, rows, lifts


def lp(k, lam, B, objective=False, shrink=0.0):
    """shrink > 0 scales every right-hand-side coefficient by (1 - shrink): a feasible solution then has
    relative slack >= shrink, enough for the exact rational check to pass despite solver tolerances."""
    ms, rs, ci, ri, rows, lifts = B
    nvar = len(ms) + len(rs)
    a = np.log2(3.0)
    q, L2, L1 = (lam ** -2) * (1 - shrink), lam ** (a - 2) * (1 - shrink), lam ** (a - 1) * (1 - shrink)
    I, J, V = [], [], []
    for n, (m, typ, m4, r) in enumerate(rows):          # c_m - q c_4m - L cbar_r <= 0
        I += [n, n]; J += [ci[m], ci[m4]]; V += [1.0, -q]
        if typ != 5:
            I.append(n); J.append(ri[r]); V.append(-(L2 if typ == 2 else L1))
    n0 = len(rows)
    for n, (r, lift) in enumerate(lifts):               # cbar_r - c_lift <= 0
        I += [n0 + n, n0 + n]; J += [ri[r], ci[lift]]; V += [1.0, -1.0]
    A = coo_matrix((V, (I, J)), shape=(n0 + len(lifts), nvar)).tocsr()
    b = np.zeros(A.shape[0])
    cost = np.r_[np.ones(len(ms)), np.zeros(len(rs))] if objective else np.zeros(nvar)
    bounds = [(1.0, None)] * len(ms) + [(0.0, None)] * len(rs)
    res = linprog(cost, A_ub=A, b_ub=b, bounds=bounds, method="highs")
    return res


def lambda_lp(k, B, lo=1.0, hi=2.0, tol=1e-8):
    while hi - lo > tol:
        mid = 0.5 * (lo + hi)
        if lp(k, mid, B).status == 0:
            lo = mid
        else:
            hi = mid
    return lo


def lower_power(lam: Fraction, shift: int) -> Fraction:
    """Rigorous rational lower bound for lam^(log2(3) - shift)."""
    iv = mpmath.iv
    iv.prec = 150
    x = iv.mpf(lam.numerator) / iv.mpf(lam.denominator)
    alpha = iv.log(iv.mpf(3)) / iv.log(iv.mpf(2))
    val = iv.exp((alpha - shift) * iv.log(x))
    man, ex = mpmath.mpf(val.a).man_exp
    lo = Fraction(int(man)) * Fraction(2) ** int(ex)
    return lo


def verify_exact(k, lam: Fraction, c_float, B):
    """Exact rational check of the inequalities for the given (float) principal variables."""
    ms, rs, ci, ri, rows, lifts = B
    c = {m: Fraction(float(c_float[ci[m]])) for m in ms}          # exact binary rationals
    cbar = {}
    for r, lift in lifts:
        cbar[r] = min(cbar.get(r, c[lift]), c[lift])
    q = 1 / lam ** 2
    L2, L1 = lower_power(lam, 2), lower_power(lam, 1)
    worst = None
    for m, typ, m4, r in rows:
        rhs = q * c[m4] + (L2 * cbar[r] if typ == 2 else L1 * cbar[r] if typ == 8 else 0)
        slack = (rhs - c[m]) / c[m]
        if slack < 0:
            return False, float(slack)
        worst = slack if worst is None or slack < worst else worst
    return all(c[m] >= 1 for m in ms), float(worst)


if __name__ == "__main__":
    KMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 9
    print(f"{'k':>2} {'N':>6} {'lambda_LP':>11} {'reference':>10} {'diff':>9} {'exact @ lambda_lo':>22} {'slack':>9} {'infeasible @ +1e-4':>19} {'time':>6}")
    for k in range(2, KMAX + 1):
        t0 = time.time()
        B = build(k)
        lam_k = lambda_lp(k, B)
        ref = TABLE2.get(k, OURS.get(k))
        lam_lo = Fraction(int(lam_k * 10 ** 6) - 2, 10 ** 6)        # >= 2e-6 below lambda_k
        # LP at lambda_lo with right-hand sides shrunk by 1e-7 -> solution with relative slack >= 1e-7,
        # then exact rational verification of that solution at lambda_lo
        res = lp(k, float(lam_lo), B, objective=True, shrink=1e-7)
        ok, slack = verify_exact(k, lam_lo, res.x, B) if res.status == 0 else (False, float("nan"))
        neg = lp(k, float(lam_lo) + 1e-4, B).status != 0
        print(f"{k:2d} {len(B[0]):6d} {lam_k:11.8f} {ref:10.7f} {lam_k - ref:+9.1e} {str(lam_lo):>12} {str(ok):>9} "
              f"{slack:9.1e} {str(neg):>19} {time.time() - t0:5.1f}s", flush=True)
