"""
Measurements for the k -> infinity limit object (CLAUDE.md, idea 2).

Index i <-> 3-adic integer (digit j of i = digit j+1 of m).  For the certified solutions c_k:
 (1) ball oscillation  osc_j = 1 - mean over balls B (low j digits fixed) of min_B c / mean c,  j = 1..k-1.
     If the limit c is Hoelder-beta on Z_3, osc_j ~ 3^(-beta j)  =>  beta_j = -log_3(osc_{j+1}/osc_j).
 (2) directional profile 1 - rho_j (vary one digit, rho.py) and its mid-range decay factor r(k) = max_j ratio.
 (3) spread of c: C_max/C_min, quantiles, mass in the top 1 %  (is the limit bounded?).
 (4) extrapolation of r(k) in k.

  python holder.py
"""
import glob
import json
import os

import numpy as np
from scipy.optimize import curve_fit


def load(k):
    d = glob.glob(f"certs/k{k}_*")[0]
    p = f"{d}/c_f32.npy" if os.path.exists(f"{d}/c_f32.npy") else f"{d}/C.npy"
    c = np.load(p).astype(np.float64).reshape(-1)
    return c / c.min()


def ball_osc(c, k):
    mean = c.mean()
    out = []
    for j in range(1, k - 1):
        v = c.reshape(3 ** (k - 1 - j), 3 ** j)       # axis 0: the high digits varying inside the ball
        out.append(1 - v.min(axis=0).mean() / mean)
    return np.array(out)                               # j = 1 .. k-2


def dir_profile(c, k):
    mean = c.mean()
    return np.array([1 - c.reshape(3 ** (k - 2 - j), 3, 3 ** j).min(axis=1).mean() / mean for j in range(k - 1)])


if __name__ == "__main__":
    ks = list(range(12, 20))
    R, out = [], {}
    for k in ks:
        c = load(k)
        osc = ball_osc(c, k)
        beta = -np.log(osc[1:] / osc[:-1]) / np.log(3)
        prof = dir_profile(c, k)
        ratios = prof[1:] / prof[:-1]
        r_mid = ratios[2:-3].max()
        R.append(r_mid)
        q = np.quantile(c, [0.5, 0.9, 0.99, 0.999])
        srt = np.sort(c)[::-1]
        top1 = srt[: len(c) // 100].sum() / c.sum()
        out[k] = dict(osc=osc.tolist(), beta=beta.tolist(), r_mid=float(r_mid), cmax=float(c.max()),
                      quantiles=q.tolist(), top1_mass=float(top1))
        print(f"k={k}: ball osc_j (j=1..{k-2}):", " ".join(f"{x:.4f}" for x in osc))
        print(f"       Hoelder beta_j:          ", " ".join(f"{x:.3f}" for x in beta))
        print(f"       dir. ratios:             ", " ".join(f"{x:.3f}" for x in ratios), f"  r_mid={r_mid:.4f}")
        print(f"       C_max={c.max():.0f}  quantiles(c/min) 50/90/99/99.9%={np.round(q, 2)}  mass in top 1%={top1:.3f}", flush=True)
    R = np.array(R)
    ks = np.array(ks)
    print("\nr_mid(k):", " ".join(f"{k}:{r:.4f}" for k, r in zip(ks, R)))
    print("increments:", " ".join(f"{d:.4f}" for d in np.diff(R)))
    for name, f, p0 in [("r = rinf - A q^k", lambda k, ri, A, q: ri - A * q ** k, (0.9, 1.0, 0.8)),
                        ("r = rinf - A/k", lambda k, ri, A: ri - A / k, (0.95, 1.0)),
                        ("r = rinf - A/k^2", lambda k, ri, A: ri - A / k ** 2, (0.9, 10.0))]:
        try:
            P, _ = curve_fit(f, ks, R, p0=p0, maxfev=100000)
            res = R - f(ks, *P)
            print(f"{name:20s} params={np.round(P, 4)}  r_inf={P[0]:.4f}  beta_inf=-log3(r_inf)={-np.log(P[0]) / np.log(3):.4f}  maxres={abs(res).max():.1e}")
        except Exception as e:
            print(name, "failed", e)
    json.dump(out, open("holder.json", "w"), indent=1)
