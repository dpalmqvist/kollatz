"""
Avenue 28 (2026-10-10): the depth Krasikov-Lagarias system for pruned 3x+1 trees, as a model for avenue 1.

Classes c mod 3^r with c != 0 (mod 3) (index = position in sorted list), beta(c) = [c = 2, 8 mod 9],
lifts l_u(c) = (2c-1)/3 + u 3^(r-1) mod 3^r.
  Phi(v)(c) = v(2c) + beta(c) min_u v(l_u(c))     (lower system, eigenvalue mu_r = 1 + rho_r/3 <= 4/3)
  A(v)(c)   = v(2c) + beta(c) mean_u v(l_u(c))    (min-free average operator, eigenvalue 4/3 for every r)
For each r: mu_r, rho_r, the loss 1 - rho_r = 4 - 3 mu_r and its ratio, the digit-sensitivity profile
s_j = 1 - mean(min over digit j)/mean(v) of the Perron vector (j = 0 lowest ... r-1 top digit), the same profile for
the eigenvector of A, and the second eigenvalue of the linearisation J of Phi at its Perron vector and of A.

  python depth_system.py RMAX            -> depth_system.json
"""
import json
import sys

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as sla


def structure(r):
    M = 3 ** r
    cls = np.array([c for c in range(M) if c % 3], dtype=np.int64)
    idx = -np.ones(M, dtype=np.int64); idx[cls] = np.arange(cls.size)
    dbl = idx[(2 * cls) % M]
    beta = np.isin(cls % 9, [2, 8])
    base = ((2 * cls[beta] - 1) // 3) % (M // 3)
    lifts = np.stack([idx[(base + u * (M // 3)) % M] for u in range(3)], axis=1)
    return dict(r=r, M=M, cls=cls, idx=idx, dbl=dbl, beta=beta, lifts=lifts)


def apply(S, v, mode):
    out = v[S["dbl"]].copy()
    L = v[S["lifts"]]
    out[S["beta"]] += L.min(axis=1) if mode == "min" else (L.mean(axis=1) if mode == "mean" else L.max(axis=1))
    return out


def perron(S, mode, iters=20000, tol=1e-14):
    v = np.ones(S["cls"].size)
    for _ in range(iters):
        w = apply(S, v, mode)
        lo, hi = (w / v).min(), (w / v).max()
        v = w / w.mean()
        if hi - lo < tol:
            break
    return 0.5 * (lo + hi), v


def digit_profile(S, v):
    """s_j = 1 - mean over (classes with digit j varied) of min / mean(v), j over ternary digits of c (0 = lowest)."""
    r, M, cls = S["r"], S["M"], S["cls"]
    full = np.full(M, np.nan); full[cls] = v
    prof = []
    for j in range(1, r):                 # digit 0 fixes the class mod 3; vary digits 1..r-1
        a = full.reshape(3 ** (r - 1 - j), 3, 3 ** j)
        mn = np.nanmin(a, axis=1)
        prof.append(1.0 - np.nanmean(mn) / np.nanmean(full))
    return prof


def linearisation(S, v, mode):
    n = S["cls"].size
    rows = [np.arange(n)]; cols = [S["dbl"]]; vals = [np.ones(n)]
    b = np.nonzero(S["beta"])[0]
    if mode == "min":
        am = S["lifts"][np.arange(b.size), v[S["lifts"]].argmin(axis=1)]
        rows.append(b); cols.append(am); vals.append(np.ones(b.size))
    else:
        for u in range(3):
            rows.append(b); cols.append(S["lifts"][:, u]); vals.append(np.full(b.size, 1 / 3))
    return sp.csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(n, n))


def second_eig(J, k=8):
    n = J.shape[0]
    if n <= 1500:
        ev = np.linalg.eigvals(J.toarray().astype(float))
    else:
        try:
            ev = sla.eigs(J.astype(float), k=min(k, n - 2), which="LM", return_eigenvectors=False, maxiter=20000, tol=1e-8)
        except sla.ArpackNoConvergence as e:
            ev = e.eigenvalues
    ev = sorted(np.abs(ev), reverse=True)
    if len(ev) < 2:
        return float("nan"), float("nan")
    return float(ev[0]), float(ev[1])


def main():
    rmax = int(sys.argv[1]) if len(sys.argv) > 1 else 11
    out = {}
    prev = None
    print(" r   mu_r        1-rho_r    ratio  |l2/l1|J(min) |l2/l1|A  4/3-minPhi(h)/h  ratio  maxPsi(h)/h-4/3  spread(h)")
    prevcw = None
    for r in range(2, rmax + 1):
        S = structure(r)
        mu, v = perron(S, "min")
        mu_a, va = perron(S, "mean")
        loss = 4 - 3 * mu
        ratio = loss / prev if prev else float("nan")
        prev = loss
        pv, pa = digit_profile(S, v), digit_profile(S, va)
        l1, l2 = second_eig(linearisation(S, v, "min"))
        a1, a2 = second_eig(linearisation(S, va, "mean"))
        # rigorous Collatz-Wielandt bounds for mu_r from the LINEAR operator's eigenvector h = va:
        # Phi(h) = A(h) - beta*(mean - min over lifts) = (4/3) h - delta, so mu_r >= min Phi(h)/h and mu'_r <= max Psi(h)/h
        lo_cw = (apply(S, va, "min") / va).min(); hi_cw = (apply(S, va, "max") / va).max()
        out[r] = dict(mu=float(mu), mu_mean=float(mu_a), loss=float(loss), ratio=float(ratio),
                      gap_min=l2 / l1, gap_mean=a2 / a1, profile_min=pv, profile_mean=pa,
                      spread_min=float(v.max() / v.min()), spread_mean=float(va.max() / va.min()),
                      cw_lower_from_h=float(lo_cw), cw_upper_from_h=float(hi_cw))
        dcw = 4 / 3 - lo_cw
        print(f"{r:2d}  {mu:.8f}  {loss:.3e}  {ratio:.3f}  {l2 / l1:.4f}      {a2 / a1:.4f}   {dcw:.3e}       "
              f"{dcw / prevcw if prevcw else float('nan'):.3f}  {hi_cw - 4 / 3:.3e}        {va.max() / va.min():.4f}", flush=True)
        prevcw = dcw
    json.dump(out, open("depth_system.json", "w"), indent=1)
    r = max(out)
    print(f"\ndigit profile at r={r} (digit 1 .. top), min-system Perron vector: " + " ".join(f"{x:.2e}" for x in out[r]["profile_min"]))
    print(f"digit profile at r={r}, mean-operator eigenvector:              " + " ".join(f"{x:.2e}" for x in out[r]["profile_mean"]))
    pm = out[r]["profile_mean"]
    print("successive ratios (mean-operator profile, from the top down): " + " ".join(f"{pm[i] / pm[i + 1]:.3f}" for i in range(len(pm) - 1)))


if __name__ == "__main__":
    main()
