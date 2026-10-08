"""
Mixing ratio rho_k = cbar_{k-1,k} / cbar_{k,k} (K-L 2003, end of §6) and digit-sensitivity
profile of the certified solutions.

K-L: summing all inequalities of L^NT_k gives  (1 - lam^-2) cbar_{k,k} <= (1/3)(lam^(a-1) + lam^(a-2)) cbar_{k-1,k},
so lambda_k is determined by rho_k alone when all constraints are tight (they are, to ~3e-5 here), and
pi_a(x) >= x^(1-eps) for every eps  <=>  lambda_k -> 2  <=  rho_k -> 1.

  python rho.py            # rho_k for every certificate in certs/, plus the per-digit profile
                           # 1 - rho_j: sensitivity of c to ternary digit j of the index (j = k-2 is the top digit)
"""
import glob
import json
import os
import time

import numpy as np
from scipy.optimize import brentq

ALPHA = np.log2(3.0)


def rho_from_lam(lam):
    return 3 * (1 - lam ** -2) / (lam ** (ALPHA - 1) + lam ** (ALPHA - 2))


def lam_from_rho(rho):
    return brentq(lambda l: (1 - l ** -2) - (l ** (ALPHA - 1) + l ** (ALPHA - 2)) * rho / 3, 1.0001, 2.5)


def load(d):
    cert = json.load(open(f"{d}/cert.json"))
    k = int(cert["k"])
    lam = float(cert["lambda"]) if "lambda" in cert else cert["lambda_P"] / cert["lambda_Q"]
    path = f"{d}/c_f32.npy" if os.path.exists(f"{d}/c_f32.npy") else f"{d}/C.npy"
    return k, lam, np.load(path, mmap_mode="r")


def rho_top(c, k, step=1 << 26):
    """rho_k from a memmapped vector (chunked, works for the 13 GB k = 21 file)."""
    N = 3 ** (k - 1)
    n3 = N // 3
    c = c.reshape(3, n3)
    tot = totmin = 0.0
    for s in range(0, n3, step):
        blk = np.asarray(c[:, s:s + step], dtype=np.float64)
        tot += blk.sum()
        totmin += blk.min(axis=0).sum()
    return (totmin / n3) / (tot / N)


def digit_profile(c, k):
    """1 - rho_j for every digit position j = 0..k-2 (needs the vector in RAM as float64)."""
    c = np.asarray(c, dtype=np.float64).reshape(-1)
    mean = c.mean()
    return [1 - c.reshape(3 ** (k - 2 - j), 3, 3 ** j).min(axis=1).mean() / mean for j in range(k - 1)]


if __name__ == "__main__":
    print(f"{'k':>2} {'lambda_cert':>11} {'rho_k':>9} {'rho(lam)':>9} {'1-rho':>9} {'lam(rho_k)':>10}")
    dirs = sorted(glob.glob("certs/k*_*"), key=lambda p: int(os.path.basename(p)[1:].split("_")[0]))
    for d in dirs:
        k, lam, c = load(d)
        rho = rho_top(c, k)
        print(f"{k:2d} {lam:11.7f} {rho:9.6f} {rho_from_lam(lam):9.6f} {1 - rho:9.2e} {lam_from_rho(rho):10.6f}", flush=True)
    for d in dirs:
        k, lam, c = load(d)
        if k > 19:          # k = 20, 21 do not fit in RAM as float64
            continue
        t0 = time.time()
        prof = np.array(digit_profile(c, k))
        print(f"k={k:2d} 1-rho_j (j=0..{k - 2}):", " ".join(f"{x:.4f}" for x in prof), f"[{time.time() - t0:.0f}s]")
        print("      ratios:          ", " ".join(f"{x:.3f}" for x in prof[1:] / prof[:-1]), flush=True)
