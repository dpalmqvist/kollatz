"""
Krasikov–Lagarias difference-inequality method for lower bounds on pi_1(x)
(3x+1 problem).  Implements the linear program family L^NT_k(lambda) from
I. Krasikov, J. C. Lagarias, "Bounds for the 3x+1 problem using difference
inequalities", Acta Arith. 109 (2003), arXiv:math/0205002.

Principal variables c^m_k, m in [3^k] = {m mod 3^k : m = 2 mod 3}.
Auxiliary   cbar^r_{k-1} = min_j c^{r + j 3^(k-1)}_k,  r in [3^(k-1)].

  m = 2 mod 9 :  c^m <= lam^-2 c^{4m} + lam^(a-2) cbar^{(4m-2)/3}
  m = 5 mod 9 :  c^m <= lam^-2 c^{4m}
  m = 8 mod 9 :  c^m <= lam^-2 c^{4m} + lam^(a-1) cbar^{(2m-1)/3}
  c^m >= 1,   a = log2(3).

A feasible solution for lam gives pi_a(x) >= x^{log2 lam} for large x
(Theorem 2.2 + Section 6 of the paper).
"""
import numpy as np

ALPHA = np.log2(3.0)


def structure(k):
    """Index arrays. Residue m = 3*i + 2 has index i, i = 0..N-1, N = 3^(k-1)."""
    M = 3 ** k
    N = 3 ** (k - 1)
    m = 3 * np.arange(N, dtype=np.int64) + 2
    nxt = ((4 * m) % M - 2) // 3                  # index of 4m mod 3^k
    cls = m % 9                                    # 2, 5 or 8
    # auxiliary residue r mod 3^(k-1), r = 2 mod 3, stored as index (r-2)//3
    Mk1 = 3 ** (k - 1)
    aux = np.full(N, -1, dtype=np.int64)
    s2 = cls == 2
    s8 = cls == 8
    aux[s2] = ((((4 * m[s2] - 2) // 3) % Mk1) - 2) // 3
    aux[s8] = ((((2 * m[s8] - 1) // 3) % Mk1) - 2) // 3
    # children of auxiliary index r: residues r + j*3^(k-1) mod 3^k
    # index of residue (3r'+2) + j*3^(k-1) is r' + j*3^(k-2)
    return dict(N=N, nxt=nxt, cls=cls, aux=aux)


def F(c, lam, S):
    """Right-hand side map of the inequality system (monotone, 1-homogeneous)."""
    N = S["N"]
    n3 = N // 3
    cbar = np.minimum(np.minimum(c[:n3], c[n3:2 * n3]), c[2 * n3:])
    out = c[S["nxt"]] / lam ** 2
    s2 = S["cls"] == 2
    s8 = S["cls"] == 8
    out[s2] += lam ** (ALPHA - 2) * cbar[S["aux"][s2]]
    out[s8] += lam ** (ALPHA - 1) * cbar[S["aux"][s8]]
    return out


def growth(lam, S, iters=20000, tol=1e-13, c0=None):
    """Collatz–Wielandt style estimate of the cone spectral radius of F_lam.
    Returns (lower, upper, c) with min_m F(c)_m/c_m = lower <= r <= upper."""
    c = np.ones(S["N"]) if c0 is None else c0.copy()
    lo = hi = None
    for it in range(iters):
        Fc = F(c, lam, S)
        ratio = Fc / c
        lo, hi = ratio.min(), ratio.max()
        c = Fc / Fc.min()
        if hi - lo < tol:
            break
    return lo, hi, c


def lambda_k(k, iters=200000, tol=1e-12, verbose=False, a=1.0, b=2.0):
    """Bisection on lam for r(F_lam) = 1 (r is decreasing in lam)."""
    S = structure(k)
    c = None
    while b - a > 2e-7:
        lam = 0.5 * (a + b)
        lo, hi, c_new = growth(lam, S, iters=iters, tol=tol, c0=c)
        if lo >= 1.0:          # certificate: F(c) >= c  -> feasible
            a, c = lam, c_new
        elif hi < 1.0:         # F(c) < c everywhere -> r < 1, infeasible
            b = lam
        else:                  # undecided: tighten using midpoint of bounds
            if 0.5 * (lo + hi) >= 1.0:
                a = lam
            else:
                b = lam
        if verbose:
            print(f"  lam={lam:.10f} lo={lo:.12f} hi={hi:.12f}")
    return a, c, S
