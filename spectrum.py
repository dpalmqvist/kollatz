"""
Avenue 16: spectrum, spectral gap and traces of the linearised K-L transfer matrix J (see jacobian.py for J).

For k = 5 .. KMAX, at lambda = lambda_k and lambda = 2:
  * Perron vector c (numpy float64; k >= 12 warm-started from c_k{k}_mlx.npy), J[i, 4i] = lam^-2,
    J[i, argmin lift] = lam^(alpha - j).
  * k <= KDENSE: full spectrum (numpy eigvals) -> |eig| sorted, bulk radii containing 50 / 90 / 99 % of the
    eigenvalues, exact traces tr(J^j) = sum eig^j for j <= JMAX, and the same for the unweighted pattern matrix B
    (closed-walk counts of the residue graph).
  * k > KDENSE: ARPACK (scipy eigs) top NTOP eigenvalues by modulus.
  * second eigenvector: ternary-digit sensitivity profile s_j(v) = 1 - ||mean_j v||^2 / ||v||^2 (fraction of the
    energy of v that lives on digit j), compared with the Perron vector's profile.
Output: spectrum.json and a printed summary (gap = 1 - |eig2|/|eig1| per k).

  python spectrum.py [KMAX=15] [KDENSE=9]
"""
import json
import sys
import time

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

from kl import ALPHA, F, growth, structure

LAMBDA = {5: 1.6627590, 6: 1.6944520, 7: 1.7201900, 8: 1.7449630, 9: 1.7615320, 10: 1.7771270, 11: 1.7922310,
          12: 1.8064236, 13: 1.8188237, 14: 1.8307723, 15: 1.8419687, 16: 1.8522346}
KMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 15
KDENSE = int(sys.argv[2]) if len(sys.argv) > 2 else 9
NTOP = 40
JMAX = 60


def perron(k, lam, S, c0=None):
    lo, hi, c = growth(lam, S, iters=100000, tol=1e-12, c0=c0)
    return c / c.mean(), (lo, hi)


def jacobian(k, lam, c, S, weighted=True):
    N, n3 = S["N"], S["N"] // 3
    lifts = np.stack([c[:n3], c[n3:2 * n3], c[2 * n3:]])
    arg = lifts.argmin(axis=0)
    rows = [np.arange(N)]; cols = [S["nxt"]]; vals = [np.full(N, lam ** -2 if weighted else 1.0)]
    for cls, L in ((2, lam ** (ALPHA - 2)), (8, lam ** (ALPHA - 1))):
        s = np.where(S["cls"] == cls)[0]
        r = S["aux"][s]
        rows.append(s); cols.append(r + arg[r] * n3); vals.append(np.full(len(s), L if weighted else 1.0))
    return sp.csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(N, N))


def digit_profile(v, k):
    """s_j = 1 - ||mean over digit j of v||^2 / ||v||^2, j = 0..k-2 (j = k-2 is the top digit)."""
    v = np.asarray(v)
    tot = np.sum(np.abs(v) ** 2)
    out = []
    for j in range(k - 1):
        m = v.reshape(3 ** (k - 2 - j), 3, 3 ** j).mean(axis=1, keepdims=True)
        m = np.broadcast_to(m, (3 ** (k - 2 - j), 3, 3 ** j)).reshape(-1)
        out.append(float(1 - np.sum(np.abs(m) ** 2) / tot))
    return out


results = {}
t_all = time.time()
for k in range(5, KMAX + 1):
    S = structure(k)
    N = S["N"]
    c_warm = None
    if k >= 12:
        c_warm = np.load(f"c_k{k}_mlx.npy").reshape(-1).astype(np.float64)
    res_k = {}
    for lam, label in ((LAMBDA[k], "lambda_k"), (2.0, "lambda2")):
        t = time.time()
        c, (lo, hi) = perron(k, lam, S, c0=c_warm)
        J = jacobian(k, lam, c, S)
        out = {"lambda": lam, "N": N, "r_bounds": [lo, hi], "perron_digit_profile": digit_profile(c, k)}
        if k <= KDENSE:
            ev = np.linalg.eigvals(J.toarray())
            ev = ev[np.argsort(-np.abs(ev))]
            a = np.abs(ev)
            out["abs_eig_top"] = a[:NTOP].tolist()
            out["bulk_radius"] = {p: float(np.quantile(a, p / 100)) for p in (50, 90, 99)}
            out["traces"] = [float(np.real(np.sum(ev ** j))) for j in range(1, JMAX + 1)]
            B = jacobian(k, lam, c, S, weighted=False)
            evB = np.linalg.eigvals(B.toarray())
            out["traces_unweighted"] = [float(np.real(np.sum(evB ** j))) for j in range(1, JMAX + 1)]
            out["abs_eig_unweighted_top"] = np.sort(np.abs(evB))[::-1][:10].tolist()
            # eigenvectors for the top 3 (dense)
            w, V = np.linalg.eig(J.toarray())
            order = np.argsort(-np.abs(w))
            w, V = w[order], V[:, order]
            vecs = [V[:, i] for i in range(3)]
            eig = w[:3]
        else:
            w, V = spla.eigs(J, k=NTOP, which="LM", tol=1e-9, maxiter=50000, ncv=max(2 * NTOP + 1, 100))
            order = np.argsort(-np.abs(w))
            w, V = w[order], V[:, order]
            out["abs_eig_top"] = np.abs(w).tolist()
            vecs = [V[:, i] for i in range(3)]
            eig = w[:3]
        out["eig_top3"] = [[float(z.real), float(z.imag)] for z in eig]
        out["gap"] = float(1 - abs(eig[1]) / abs(eig[0]))
        out["v2_digit_profile"] = digit_profile(vecs[1], k)
        out["v3_digit_profile"] = digit_profile(vecs[2], k)
        res_k[label] = out
        print(f"k={k:2d} {label:8s} N={N:8d} r=[{lo:.7f},{hi:.7f}] |eig|: " +
              " ".join(f"{x:.4f}" for x in out["abs_eig_top"][:6]) + f"  gap={out['gap']:.4f}  "
              f"eig2={eig[1]:.4f}  v2 top-digit s={out['v2_digit_profile'][-1]:.3f} "
              f"(perron {out['perron_digit_profile'][-1]:.3f})  [{time.time() - t:.0f}s]", flush=True)
    results[k] = res_k
    with open("spectrum.json", "w") as f:
        json.dump(results, f, indent=1)
print(f"done in {time.time() - t_all:.0f}s")
