"""Avenue 18: compare the measured gap statistics (parity_stats.py) with the i.i.d. geometric model.
  python analyse_parity.py parity_stats_32.json"""
import json
import sys

import numpy as np

J = json.load(open(sys.argv[1]))

print(f"n < 2^{J['KBITS']}: count {J['count']}, mean sigma {J['mean_sigma']:.2f}, mean odd steps {J['mean_odd']:.2f}, "
      f"odd fraction {J['mean_odd'] / J['mean_sigma']:.4f} (random walk to 1: 1/2 on the free part)")
G = len(J["gap_hist"][0]) - 1
names = {0: f"window t < {J['KBITS']} (i.i.d. fair bits in a window: deviations are windowing only)",
         1: f"t >= {J['KBITS']} and x >= 2^{J['BIG']} (large values beyond the start range)",
         2: f"x < 2^{J['BIG']} (small values, forced descent)"}
g = np.arange(1, G + 1)
for reg in (1, 2, 0):
    h = np.array(J["gap_hist"][reg], dtype=float)[1:]; tot = h.sum(); p = h / tot
    geo = 2.0 ** -g; geo[-1] = 2.0 ** -(G - 1)
    print(f"--- regime {reg}: {names[reg]}: {tot:.3e} gaps; mean gap {np.sum(g * p):.4f} (geometric 2)")
    print("  gap  measured   2^-g      ratio    (ratio - 1)*sqrt(count) in sigma units")
    for gg in list(range(1, 9)) + [10, 12, 16]:
        cnt = h[gg - 1]
        print(f"  {gg:3d}  {p[gg-1]:.6f}  {geo[gg-1]:.6f}  {p[gg-1] / geo[gg-1]:.5f}   {(p[gg-1] / geo[gg-1] - 1) * np.sqrt(max(cnt, 1)):+.1f}")
    P = np.array(J["pair_hist"][reg], dtype=float)[1:, 1:]; npairs = P.sum(); P /= npairs
    a = P.sum(axis=1); b = P.sum(axis=0)
    dev = P - np.outer(a, b)
    ma, mb = np.sum(g * a), np.sum(g * b)
    corr = (np.sum(np.outer(g, g) * P) - ma * mb) / np.sqrt((np.sum(g ** 2 * a) - ma ** 2) * (np.sum(g ** 2 * b) - mb ** 2))
    print(f"  pairs: {npairs:.3e}; max |P(g,g') - P(g)P(g')| = {np.abs(dev).max():.2e}; TV from product {0.5 * np.abs(dev).sum():.2e}; "
          f"corr(gap, next gap) = {corr:+.6f} (1-sigma noise {1 / np.sqrt(npairs):.1e})")
    sub = P[:4, :4] / np.outer(a[:4], b[:4])
    print("  P(g,g')/(P(g)P(g')), g,g' = 1..4:\n" + "\n".join("   " + " ".join(f"{x:.4f}" for x in row) for row in sub))
print("--- records of R(n)/log2 n (last time orbit >= n):", J["records_R"][-5:])
print("--- records of height/log2 n:", J["records_height"][-5:])
s = np.array(J["sigma_hist"]); print(f"--- sigma: max {np.nonzero(s)[0].max()}, quantiles 50/99/99.99 %: ",
      [int(np.searchsorted(np.cumsum(s) / s.sum(), q)) for q in (0.5, 0.99, 0.9999)])
