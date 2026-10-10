"""
Numerical companion to notes/strict_monotonicity.md.

  python monotone_check.py [KMAX=9]

(1) nu(i) = 4i+2 mod N is one N-cycle (Lemma 2), k = 2..14.
(2) At lambda_k (power-iterated fixed point c_k): the tiling gain delta = F_{k+1}(tile c) - tile c (Lemma 9) is
    zero on class 1, positive on 2/3 of classes 0 and 2; the vector z = sum_{n<N'} F^n(tile c) of Lemma 3 gives a
    Collatz-Wielandt lower bound for r_{k+1}(lambda_k) > 1.
(3) Uniqueness (Lemma 7): power iteration from random positive starts converges to the same direction.
(4) r_k(lambda) on a grid of [1, 2] (is it monotone?) and on [4, 1000] (is L^NT_k ever feasible there?).
"""
import sys
import numpy as np
import kl


def is_single_cycle(k):
    S = kl.structure(k)
    nxt, N = S["nxt"], S["N"]
    i, n = 0, 0
    while True:
        i = nxt[i]
        n += 1
        if i == 0:
            return n == N


def fixed_point(k):
    lam, c, S = kl.lambda_k(k, tol=1e-13)
    lo, hi, c = kl.growth(lam, S, iters=400000, tol=1e-15, c0=c)
    return lam, c / c.min(), S


def spectral_radius(lam, S, iters=20000, tol=1e-12, c0=None):
    lo, hi, c = kl.growth(lam, S, iters=iters, tol=tol, c0=c0)
    return lo, hi, c


def main(kmax):
    print("(1) nu is a single N-cycle for k = 2..14:", all(is_single_cycle(k) for k in range(2, 15)))
    print("(2) tiling gain at lambda_k")
    for k in range(2, kmax + 1):
        lam, c, S = fixed_point(k)
        resid = np.abs(kl.F(c, lam, S) / c - 1).max()
        S1 = kl.structure(k + 1)
        t = np.tile(c, 3)
        rel = (kl.F(t, lam, S1) - t) / t
        cls = S1["cls"]
        pos = rel > 1e-5
        z, y = t.copy(), t.copy()
        for _ in range(1, S1["N"]):
            y = kl.F(y, lam, S1)
            z += y
        cw = (kl.F(z, lam, S1) / z).min()
        print(f"  k={k:2d} lam_k={lam:.7f} |F(c)/c-1|={resid:.0e}  gain>0 on class5 {pos[cls == 5].mean():.3f}, "
              f"class2 {pos[cls == 2].mean():.3f}, class8 {pos[cls == 8].mean():.3f}; r_(k+1)(lam_k) >= {cw:.6f}")
    print("(3) uniqueness of the fixed point direction (5 random starts)")
    rng = np.random.default_rng(1)
    for k in range(2, min(kmax, 8) + 1):
        lam, c, S = fixed_point(k)
        devs = []
        for _ in range(5):
            x0 = rng.uniform(0.01, 100.0, S["N"])
            _, _, x = kl.growth(lam, S, iters=400000, tol=1e-15, c0=x0)
            x = x / x.min()
            devs.append(np.abs(x / c - 1).max())
        print(f"  k={k} max relative deviation from c_k: {max(devs):.1e}")
    print("(4) r_k(lambda) on [1, 2] and on [4, 1000]")
    grid = np.linspace(1.0, 2.0, 41)
    big = np.array([4.0, 4.5, 5, 6, 8, 12, 20, 50, 100, 1000])
    for k in range(2, min(kmax, 7) + 1):
        S = kl.structure(k)
        r, c = [], None
        for lam in grid:
            lo, hi, c = spectral_radius(lam, S, c0=c)
            r.append(0.5 * (lo + hi))
        r = np.array(r)
        mono = np.all(np.diff(r) < 0)
        rb = []
        for lam in big:
            lo, hi, _ = spectral_radius(lam, S)
            rb.append(hi)
        print(f"  k={k} r decreasing on [1,2]: {mono} (r(1)={r[0]:.4f}, r(2)={r[-1]:.4f}); "
              f"max over lam in [4,1000] of upper bound on r: {max(rb):.4f} at lam={big[int(np.argmax(rb))]}")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 9)
