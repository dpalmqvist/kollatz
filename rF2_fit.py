"""
Avenue 1: extrapolate the spectral radius r_k(F_2) of the K-L map at lambda = 2 (identity: r_k = 1/4 + 3/4 rho'_k).
lambda_k -> 2  <=>  r_k -> 1.  Fit 1 - r_k with competing models and report the implied limit.

  python rF2_fit.py [extra k=r pairs, e.g. 20=0.9710 21=0.9736]
"""
import sys

import numpy as np
from scipy.optimize import curve_fit

R = {5: 0.861014, 6: 0.879668, 7: 0.895020, 8: 0.910334, 9: 0.919391, 10: 0.926725, 11: 0.933490,
     12: 0.9398400, 13: 0.9450493, 14: 0.9499766, 15: 0.9545038, 16: 0.9585192, 17: 0.9620855, 18: 0.9652432,
     19: 0.9680737}
for arg in sys.argv[1:]:
    k, v = arg.split("=")
    R[int(k)] = float(v)
k = np.array(sorted(R)); e = 1 - np.array([R[i] for i in k])
print("k  1-r_k      ratio")
for i in range(len(k)):
    print(f"{k[i]:2d} {e[i]:.6f}  {e[i]/e[i-1] if i else float('nan'):.4f}")
m = k >= 11
models = [("geometric  e=A r^k", lambda k, A, r: A * r ** k, (0.5, 0.92)),
          ("geo+offset e=B+A r^k", lambda k, B, A, r: B + A * r ** k, (0.005, 0.5, 0.9)),
          ("power      e=A k^-p", lambda k, A, p: A * k ** -p, (1.0, 1.2)),
          ("stretched  e=A exp(-b k^s)", lambda k, A, b, s: A * np.exp(-b * k ** s), (0.3, 0.3, 0.7))]
for name, f, p0 in models:
    try:
        P, _ = curve_fit(f, k[m], e[m], p0=p0, maxfev=200000)
        res = e[m] - f(k[m], *P)
        lim = P[0] if "offset" in name else 0.0
        print(f"{name:28s} params={np.round(P, 5)} maxres={abs(res).max():.1e}  limit 1-r_inf={lim:.4f}"
              f"  -> lambda_inf = {2 ** (1 - 0) if lim == 0 else 'see note':}  pred k=25: {f(25, *P):.4f}, k=30: {f(30, *P):.4f}")
    except Exception as ex:
        print(name, "failed", ex)
# blind test: fit on k <= 16, predict the rest
print("\nblind prediction errors (fit k in [11,16]):")
mm = (k >= 11) & (k <= 16)
for name, f, p0 in models:
    try:
        P, _ = curve_fit(f, k[mm], e[mm], p0=p0, maxfev=200000)
        errs = [f(kk, *P) - e[k == kk][0] for kk in k[k > 16]]
        print(f"{name:28s}", " ".join(f"{kk}:{er:+.1e}" for kk, er in zip(k[k > 16], errs)))
    except Exception as ex:
        print(name, "failed", ex)
