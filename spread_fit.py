"""Avenue 17: table of t*(k, lam) from spread_iter.json, extrapolation in k, and the growth of t*_inf(lam) as lam -> 2.
  python spread_fit.py"""
import json
import numpy as np

d = json.load(open("spread_iter.json"))
d = {key: v for key, v in d.items() if not v.get("slack") and v["tstar"] is not None}
ks = sorted({v["k"] for v in d.values()}); ls = sorted({v["lam"] for v in d.values()})
T = {(v["k"], v["lam"]): v["tstar"] for v in d.values()}
print("t*(k, lam): minimal spread of a feasible point of L^NT_k(lam)")
print("k\\lam " + " ".join(f"{l:8.2f}" for l in ls))
for k in ks:
    print(f"{k:5d} " + " ".join(f"{T[(k, l)]:8.3f}" if (k, l) in T else "       -" for l in ls))
print("\nextrapolation in k (t* is nonincreasing in k; decrements fitted geometrically on the last 4 levels):")
print(" lam    2-lam   last k   t*(last)   decrement ratio   t*_inf (fit)")
tinf = {}
for l in ls:
    kk = [k for k in ks if (k, l) in T]
    v = np.array([T[(k, l)] for k in kk])
    if len(v) < 4:
        continue
    dec = -np.diff(v)
    if dec[-1] <= 1e-9:
        r, inf = 0.0, v[-1]
    else:
        r = (dec[-1] / dec[-3]) ** 0.5 if dec[-3] > 1e-9 else 0.0
        r = min(r, 0.97)
        inf = v[-1] - dec[-1] * r / (1 - r)
    tinf[l] = inf
    print(f"{l:.2f}   {2 - l:.2f}   {kk[-1]:4d}    {v[-1]:8.3f}     {r:.3f}            {inf:8.3f}")
L = np.array(sorted(tinf)); Ti = np.array([tinf[l] for l in L])
x = np.log(2 - L); y = np.log(Ti)
for lo in (0, 2):
    a, b = np.polyfit(x[lo:], y[lo:], 1)
    print(f"power-law fit t*_inf ~ C (2-lam)^(-a) on lam >= {L[lo]:.2f}: a = {-a:.2f}, max resid {np.abs(a * x[lo:] + b - y[lo:]).max():.3f}")
a2, b2 = np.polyfit(L, y, 1)
print(f"exponential fit t*_inf ~ exp(b lam): b = {a2:.2f}, max resid {np.abs(a2 * L + b2 - y).max():.3f}")
print("local exponents a between consecutive lam:", " ".join(f"{-(y[i+1]-y[i])/(x[i+1]-x[i]):.2f}" for i in range(len(L) - 1)))
