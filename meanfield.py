"""
Avenue 1: is lambda_k a mean-field quantity?  (2026-10-09)

The K-L index maps are recursive in the top ternary digit: for level-(k-1) index i_low and top digit t,
    nxt_k(i_low + t*n3) = nxt_{k-1}(i_low) + sigma_{i_low}(t) * n3,      n3 = N/3,
    aux_k(i_low + t*n3) = aux_{k-1}(i_low) + pi_{i_low}(t) * n9,         n9 = N/9   (classes 2, 8 mod 9),
with sigma a cyclic shift and pi a shift or a reflection of {0,1,2} determined by i_low (the arithmetic of 2 and 3).
The relative alignment of sigma and pi is what the coarse-graining defect (defect.py) measures, and the argmins were
found independent.  Test: replace sigma, pi by RANDOM bijections (per i_low) and recompute lambda_k, rho_k.
  * "top":  random bijections at level k only (levels < k exact);
  * "all":  random bijections at every level from K0 upward (a random K-L system with the same coarse structure:
            nxt stays a bijection, aux stays 3-to-1, the summed identity and the ceiling lambda = 2 are unchanged);
  * "sigma" / "pi": scramble only one of the two at level k.
If lambda_k is unchanged within seed noise, the alignment arithmetic is irrelevant and lambda_k -> 2 is a question
about the random model.

  python meanfield.py [KMAX=13] [SEEDS=3] [K0=3] [MODES=top,sigma,pi,all] [TAG]   -> meanfield{_TAG}.json
"""
import json
import sys
import time

import numpy as np

import kl

K0 = 3
MODES = ("top", "sigma", "pi", "all")
TAG = ""


def exact_perms(k):
    """sigma, pi of the exact system at level k, extracted from kl.structure: arrays (n3, 3)."""
    S = kl.structure(k)
    N = S["N"]; n3, n9 = N // 3, N // 9
    nxt = S["nxt"].reshape(3, n3).T          # [i_low, t]
    aux = S["aux"].reshape(3, n3).T
    sigma = nxt // n3
    pi = np.where(aux >= 0, aux // n9, -1)
    return sigma, pi, S


def lift(Sprev, sigma, pi):
    """level-k structure from level-(k-1) structure and top-digit bijections (n3, 3)."""
    n3 = Sprev["N"]; N = 3 * n3; n9 = n3 // 3
    i_low = np.arange(n3)
    nxt = np.empty(N, dtype=np.int64); aux = np.full(N, -1, dtype=np.int64)
    cls = np.tile(Sprev["cls"], 3)
    for t in range(3):
        nxt[t * n3:(t + 1) * n3] = Sprev["nxt"] + sigma[:, t] * n3
        m = Sprev["aux"] >= 0
        aux[t * n3 + i_low[m]] = Sprev["aux"][m] + pi[m, t] * n9
    return dict(N=N, nxt=nxt, cls=cls, aux=aux)


def random_perms(n3, rng, which=("sigma", "pi"), base=None):
    sigma, pi = base
    if "sigma" in which:
        sigma = rng.permuted(np.tile(np.arange(3), (n3, 1)), axis=1)
    if "pi" in which:
        p = rng.permuted(np.tile(np.arange(3), (n3, 1)), axis=1)
        pi = np.where(pi >= 0, p, -1)
    return sigma, pi


def build(k, mode, rng):
    """structure at level k for the given mode."""
    if k < K0:
        return kl.structure(k)
    S = kl.structure(K0 - 1)
    for kk in range(K0, k + 1):
        sigma, pi, _ = exact_perms(kk)
        if mode == "all" or (kk == k and mode in ("top", "sigma", "pi")):
            which = {"all": ("sigma", "pi"), "top": ("sigma", "pi"), "sigma": ("sigma",), "pi": ("pi",)}[mode]
            sigma, pi = random_perms(S["N"], rng, which, base=(sigma, pi))
        S = lift(S, sigma, pi)
    return S


def lambda_secant(S, lam0, lam1, c0=None, width=2e-8, steps=30):
    c = c0
    def f(lam):
        nonlocal c
        lo, hi, c = kl.growth(lam, S, iters=200000, tol=1e-11, c0=c)
        return np.log(0.5 * (lo + hi))
    f0, f1 = f(lam0), f(lam1)
    for _ in range(steps):
        lam2 = lam1 - f1 * (lam1 - lam0) / (f1 - f0)
        if abs(lam2 - lam1) < width:
            lam1 = lam2
            break
        lam0, f0, lam1 = lam1, f1, lam2
        f1 = f(lam1)
    lo, hi, c = kl.growth(lam1, S, iters=200000, tol=1e-11, c0=c)
    n3 = S["N"] // 3
    cbar = np.minimum(np.minimum(c[:n3], c[n3:2 * n3], ), c[2 * n3:])
    return lam1, cbar.mean() / c.mean(), c


def main(kmax, seeds):
    res = {}
    modes = ("exact",) + tuple(MODES)
    lam_prev = {m: 1.6 for m in modes}
    for k in range(max(5, K0), kmax + 1):
        t = time.time()
        # consistency: recursive exact build == kl.structure
        Se = build(k, "exact", None); Sk = kl.structure(k)
        assert np.array_equal(Se["nxt"], Sk["nxt"]) and np.array_equal(Se["aux"], Sk["aux"]) and np.array_equal(Se["cls"], Sk["cls"])
        row = {}
        for mode in modes:
            vals = []
            for seed in range(1 if mode == "exact" else seeds):
                S = Sk if mode == "exact" else build(k, mode, np.random.default_rng(1000 * k + seed))
                lam, rho, _ = lambda_secant(S, lam_prev[mode], lam_prev[mode] + 0.01)
                vals.append((lam, rho))
            lam_prev[mode] = float(np.mean([v[0] for v in vals]))
            row[mode] = dict(lam=[v[0] for v in vals], rho=[v[1] for v in vals])
        res[k] = row
        json.dump(dict(K0=K0, modes=MODES, seeds=seeds, results=res), open(f"meanfield{TAG}.json", "w"), indent=1)
        e = row["exact"]["lam"][0]
        print(f"k={k:2d} exact lam={e:.7f} 1-rho={1 - row['exact']['rho'][0]:.5f} | " +
              " | ".join(f"{m}: dlam={np.mean(row[m]['lam']) - e:+.1e}±{np.std(row[m]['lam']):.0e} "
                         f"1-rho={1 - np.mean(row[m]['rho']):.5f}" for m in MODES) +
              f"  [{time.time() - t:.0f}s]", flush=True)


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) > 2:
        K0 = int(a[2])
    if len(a) > 3:
        MODES = tuple(a[3].split(","))
    if len(a) > 4:
        TAG = "_" + a[4]
    main(int(a[0]) if a else 13, int(a[1]) if len(a) > 1 else 3)
