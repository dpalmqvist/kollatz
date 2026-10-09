"""Avenue 17: structure of the minimal-spread feasible points (spread_iter.py vectors) vs the Perron vector.
  python spread_structure.py K LAM [LAM ...]   (reads spread_c_k{K}_{LAM}_s1e-05.npy or spread_c_k{K}_{LAM}.npy)"""
import glob
import sys

import numpy as np

import kl

k = int(sys.argv[1]); lams = sys.argv[2:]
S = kl.structure(k); N = S["N"]; n3 = N // 3
cls = S["cls"]


def explained(v, J, top):
    m = v.reshape(3 ** J, -1).mean(axis=1) if top else v.reshape(-1, 3 ** J).mean(axis=0)
    return float(((m - v.mean()) ** 2).mean() / v.var())


def digit_profile(v):
    out = []
    for j in range(k - 1):
        m = v.reshape(3 ** (k - 2 - j), 3, 3 ** j).min(axis=1, keepdims=True)
        out.append(1 - np.broadcast_to(m, (3 ** (k - 2 - j), 3, 3 ** j)).mean() / v.mean())
    return out


def report(name, c, lam):
    c = c.astype(np.float64); c /= c.min(); t = c.max()
    F = kl.F(c, lam, S); slack = F / c - 1
    tight = slack < 1e-4
    print(f"=== {name}: lam={lam} spread={t:.3f} mean={c.mean():.3f} median={np.median(c):.3f}")
    print(f"  at floor (c<1.001): {(c < 1.001).mean():.3f}  at cap (c>t/1.001): {(c > t / 1.001).mean():.3f}  "
          f"tight rows (F(c)/c-1 < 1e-4): {tight.mean():.3f}; by class 2/5/8: " +
          " ".join(f"{tight[cls == q].mean():.3f}" for q in (2, 5, 8)))
    print("  mean c by class 2/5/8: " + " ".join(f"{c[cls == q].mean():.3f}" for q in (2, 5, 8)) +
          "; floor fraction by class: " + " ".join(f"{(c[cls == q] < 1.001).mean():.3f}" for q in (2, 5, 8)) +
          "; cap fraction by class: " + " ".join(f"{(c[cls == q] > t / 1.001).mean():.3f}" for q in (2, 5, 8)))
    lc = np.log(c)
    print("  explained variance of log c by lowest J digits: " + " ".join(f"J={J}:{explained(lc, J, False):.3f}" for J in (1, 2, 3, 4, 6, 8, 10)))
    print("  explained variance of log c by top J digits:    " + " ".join(f"J={J}:{explained(lc, J, True):.3f}" for J in (1, 2, 3, 4, 6)))
    print("  top-digit loss profile 1-rho_j (j = 0 lowest ... top): " + " ".join(f"{x:.3f}" for x in digit_profile(c)))
    h, e = np.histogram(lc / np.log(t), bins=10, range=(0, 1))
    print("  histogram of log c / log t in tenths: " + " ".join(f"{x / N:.3f}" for x in h))
    return c


LAMK = {12: 1.8064236, 13: 1.8188237, 14: 1.8307723, 15: 1.8419687, 16: 1.8522346}
cs = {}
for lam in lams:
    f = (glob.glob(f"spread_c_k{k}_{float(lam)}_s*.npy") + glob.glob(f"spread_c_k{k}_{float(lam)}.npy"))[0]
    cs[lam] = report(f"min-spread k={k}", np.load(f), float(lam))
p = np.load(f"c_k{k}_mlx.npy").reshape(-1); cs["perron"] = report("Perron vector", p, LAMK[k])
keys = list(cs)
print("\ncorrelation of log c between solutions:")
for i in range(len(keys)):
    for j in range(i + 1, len(keys)):
        print(f"  {keys[i]} vs {keys[j]}: {np.corrcoef(np.log(cs[keys[i]]), np.log(cs[keys[j]]))[0, 1]:.3f}")
