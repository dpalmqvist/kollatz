"""
Avenue 28 (2026-10-10): the eigenvectors of the min-free depth operator are the marginals of ONE measure on Z_3^x.

For 0 < p < 1 let nu_p be the stationary law of the random walk on the 3-adic units
    x -> x/2 with probability 1 - p,     x -> (3x+1)/2 with probability p,
i.e. the law of X = sum_{j>=1} 3^(j-1) 2^-(a_1+...+a_j), a_j i.i.d. with P(a = m) = p (1-p)^(m-1).
p = 1/2 is Tao's Syracuse random variable (Forum Math. Pi 10 (2022) e12, Sec. 1.3); p = 1/4 is the tree weighting:
its level-r density h_r (w.r.t. Haar on the units mod 3^r, mean 1) is the Perron vector of the depth operator
A_r v(c) = v(2c) + [c = 2, 8 (9)] mean_u v(l_u(c)) of depth_system.py, eigenvalue 4/3, for every r >= 3.
The marginals satisfy, exactly,
    h_r(c) = (1-p) h_r(2c) + 3p [c = 2, 8 (9)] h_(r-1)((2c-1)/3 mod 3^(r-1)),   h_1 = (2(1-p), 2)/(2-p) on c = 1, 2,
which is solved along the single doubling cycle (2 is a primitive root mod 3^r). No power iteration.

Per level r: spread max h/min h; sup relative top-digit oscillation max_s (max_t - min_t h_r(s + t 3^(r-1)))/h_(r-1)(s);
TV distance between nu at level r and its level-(r-1) uniformisation (Tao's fine-scale mixing quantity, consecutive
levels); max |nu^(xi)| over primitive characters of level r; and for p = 1/4 the Collatz-Wielandt bounds that h_r
gives for the min/max depth systems: 4/3 - min Phi(h)/h and max Psi(h)/h - 4/3.

  python syracuse_measure.py RMAX [p ...]      -> syracuse_measure.json   (default p = 0.25 0.5)
"""
import json
import sys

import numpy as np


def marginals(rmax, p):
    q = 1.0 - p
    h = np.array([0.0, 2 * q / (2 - p), 2 / (2 - p)])            # level 1, full array over Z/3
    yield 1, h
    for r in range(2, rmax + 1):
        M = 3 ** r
        c = np.arange(M, dtype=np.int64)
        beta = (c % 9 == 2) | (c % 9 == 8)
        g = np.zeros(M)
        g[beta] = 3 * p * h[((2 * c[beta] - 1) // 3) % (M // 3)]
        P = (2 * c) % M
        qk = q                                                        # h = sum_j q^j g(2^j c), by repeated squaring
        while qk > 1e-20:
            g = g + qk * g[P]
            P = P[P]
            qk *= qk
        h = g
        yield r, h


def stats(r, h, hprev, p):
    M = 3 ** r
    units = np.arange(M) % 3 != 0
    out = dict(r=r, spread=float(h[units].max() / h[units].min()))
    if hprev is None:
        return out
    top = h.reshape(3, M // 3)                                        # top digit on axis 0
    u1 = np.arange(M // 3) % 3 != 0
    mart = np.abs(top.mean(axis=0)[u1] - hprev[u1]).max() / hprev[u1].min()
    out["martingale_err"] = float(mart)
    out["osc_sup"] = float(((top.max(axis=0) - top.min(axis=0))[u1] / hprev[u1]).max())
    nu = h / units.sum()
    nu_un = np.tile(hprev, 3) / units.sum()
    out["tv"] = float(0.5 * np.abs(nu - nu_un).sum())
    if r <= 15:                                                       # FFT of 3^r points; skipped above r = 15
        f = np.abs(np.fft.fft(nu))
        k = np.arange(M)
        out["fourier_max"] = float(f[k % 3 != 0].max())
        out["fourier_l2"] = float(np.sqrt((f[k % 3 != 0] ** 2).sum()))
    if abs(p - 0.25) < 1e-12 and r >= 3:
        c = np.arange(M, dtype=np.int64)
        beta = (c % 9 == 2) | (c % 9 == 8)
        base = ((2 * c[beta] - 1) // 3) % (M // 3)
        L = np.stack([h[(base + u * (M // 3)) % M] for u in range(3)], axis=1)
        dbl = h[(2 * c) % M]
        phi, psi = dbl.copy(), dbl.copy()
        phi[beta] += L.min(axis=1); psi[beta] += L.max(axis=1)
        out["cw_lower_gap"] = float(4 / 3 - (phi[units] / h[units]).min())
        out["cw_upper_gap"] = float((psi[units] / h[units]).max() - 4 / 3)
        a = dbl.copy(); a[beta] += L.mean(axis=1)
        out["eig_check"] = float(np.abs(a[units] / h[units] - 4 / 3).max())
    return out


def main():
    rmax = int(sys.argv[1]) if len(sys.argv) > 1 else 13
    ps = [float(x) for x in sys.argv[2:]] or [0.25, 0.5]
    res = {}
    for p in ps:
        rows, hprev = [], None
        print(f"\np = {p}:  r  spread    osc_sup   ratio   TV        ratio   max|nu^|  ratio   "
              + ("CW lower gap  ratio   CW upper gap" if p == 0.25 else ""))
        for r, h in marginals(rmax, p):
            s = stats(r, h, hprev, p)
            if rows and "osc_sup" in rows[-1]:
                for key in ("osc_sup", "tv", "fourier_max", "cw_lower_gap"):
                    if key in s and key in rows[-1]:
                        s[key + "_ratio"] = s[key] / rows[-1][key]
            rows.append(s)
            hprev = h
            if "osc_sup" in s:
                line = (f"  {r:3d}  {s['spread']:.4f}  {s['osc_sup']:.3e}  {s.get('osc_sup_ratio', np.nan):.3f}  "
                        f"{s['tv']:.3e}  {s.get('tv_ratio', np.nan):.3f}  {s.get('fourier_max', np.nan):.3e}  "
                        f"{s.get('fourier_max_ratio', np.nan):.3f}")
                if "cw_lower_gap" in s:
                    line += (f"  {s['cw_lower_gap']:.3e}  {s.get('cw_lower_gap_ratio', np.nan):.3f}  "
                             f"{s['cw_upper_gap']:.3e}   [mart {s['martingale_err']:.1e}, eig {s['eig_check']:.1e}]")
                print(line, flush=True)
        res[str(p)] = rows
    json.dump(res, open("syracuse_measure.json", "w"), indent=1)


if __name__ == "__main__":
    main()
