"""
Plot gamma_k = log2(lambda_k) against k with the geometric fit
gamma_k ~ gamma_inf - A r^k (fitted to k >= 11), and below it the residuals
gamma_k - fit for all k (symmetric log scale).  Writes gamma_trend.png.

  python plot_gamma.py            # add new k to LAMBDA below and re-run
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# numerical lambda_k (float64 bisection for k <= 13, MLX secant for k >= 14); see CLAUDE.md
LAMBDA = {2: 1.3534010, 3: 1.5275960, 4: 1.6122870, 5: 1.6627590, 6: 1.6944520, 7: 1.7201900,
          8: 1.7449630, 9: 1.7615320, 10: 1.7771270, 11: 1.7922310, 12: 1.8064236, 13: 1.8188237,
          14: 1.8307723, 15: 1.8419687, 16: 1.8522346, 17: 1.8616888, 18: 1.8703250,
          19: 1.8783132, 20: 1.8857083, 21: 1.8925462, 22: 1.8988933}
FIT_FROM = 11
PUBLISHED = (11, 0.84)          # Krasikov-Lagarias 2003 record

# chart chrome / palette (dataviz reference palette, light mode; validated)
SURFACE, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
BLUE, ORANGE = "#2a78d6", "#eb6834"

k = np.array(sorted(LAMBDA))
g = np.log2([LAMBDA[i] for i in k])
geo = lambda k, ginf, A, r: ginf - A * r ** k
m = k >= FIT_FROM
P, C = curve_fit(geo, k[m], g[m], p0=(0.95, 0.5, 0.9), maxfev=20000)
ginf, A, r = P

plt.rcParams.update({"font.size": 11, "axes.edgecolor": INK2, "axes.labelcolor": INK2,
                     "xtick.color": INK2, "ytick.color": INK2, "font.family": "sans-serif"})
fig, (ax, axr) = plt.subplots(2, 1, figsize=(9, 8.2), facecolor=SURFACE, sharex=True,
                              gridspec_kw={"height_ratios": [3, 2], "hspace": 0.08})
for a in (ax, axr):
    a.set_facecolor(SURFACE)
    for side in ("top", "right"):
        a.spines[side].set_visible(False)
    a.grid(axis="y", color=GRID, linewidth=0.8)
    a.set_axisbelow(True)

kk = np.linspace(FIT_FROM, k.max(), 200)
kx = np.linspace(k.max(), 30, 200)
ax.plot(kk, geo(kk, *P), color=ORANGE, lw=2, zorder=2)
ax.plot(kx, geo(kx, *P), color=ORANGE, lw=2, ls=(0, (4, 3)), zorder=2)
ax.axhline(ginf, color=INK2, lw=1, ls=(0, (2, 3)), zorder=1)
ax.scatter(k, g, s=46, color=BLUE, edgecolor=SURFACE, linewidth=2, zorder=3)

# direct labels (text in ink, marks carry identity)
ax.annotate(f"computed γ_k = log₂ λ_k", (5, g[k == 5][0]), xytext=(10, -22),
            textcoords="offset points", ha="left", color=INK, fontsize=10.5)
ax.annotate(f"k = {k[-1]}: γ = {g[-1]:.4f}", (k[-1], g[-1]), xytext=(-6, 14),
            textcoords="offset points", ha="right", color=INK, fontsize=10)
ax.annotate(f"geometric fit to k ≥ {FIT_FROM}:\nγ∞ − {A:.3f}·{r:.3f}^k\n(dashed = extrapolation)", (26, geo(26, *P)),
            xytext=(0, -62), textcoords="offset points", ha="center", color=INK, fontsize=10.5,
            arrowprops=dict(arrowstyle="-", color=INK2, lw=0.8))
ax.text(30, ginf + 0.004, f"γ∞ ≈ {ginf:.3f}", ha="right", va="bottom", color=INK2, fontsize=10.5)
ax.annotate("published record 0.84 (k = 11)", PUBLISHED, xytext=(14, -26), textcoords="offset points",
            color=INK2, fontsize=10, arrowprops=dict(arrowstyle="-", color=INK2, lw=0.8))

ax.set_xlim(1, 30.5)
ax.set_ylim(0.42, 1.0)
ax.set_ylabel("γ_k = log₂ λ_k")

# residual panel: filled = used in the fit, hollow = not used (k < FIT_FROM)
res = g - geo(k, *P)
axr.axhline(0, color=INK2, lw=1, zorder=1)
axr.plot(k, res, color=GRID, lw=1, zorder=1)
axr.scatter(k[m], res[m], s=46, color=BLUE, edgecolor=SURFACE, linewidth=2, zorder=3)
axr.scatter(k[~m], res[~m], s=46, facecolor=SURFACE, edgecolor=BLUE, linewidth=1.8, zorder=3)
axr.set_yscale("symlog", linthresh=1e-4, linscale=1.0)
axr.set_ylim(-0.5, 2e-2)
axr.set_yticks([-1e-1, -1e-2, -1e-3, -1e-4, 0, 1e-4, 1e-3, 1e-2])
axr.set_yticklabels(["−10⁻¹", "−10⁻²", "−10⁻³", "−10⁻⁴", "0", "10⁻⁴", "10⁻³", "10⁻²"])
axr.axvspan(1, FIT_FROM - 0.5, color=GRID, alpha=0.35, lw=0, zorder=0)
axr.text(1.4, 8e-3, f"not fitted (k < {FIT_FROM})", color=INK2, fontsize=10, va="center")
axr.text(FIT_FROM + 0.2, 8e-3, f"fitted, |residual| ≤ {np.abs(res[m]).max():.0e}", color=INK2, fontsize=10, va="center")
axr.text(29.8, -3e-3, "γ_k is accurate to ~10⁻⁷:\nresiduals are structure, not noise",
         ha="right", color=INK2, fontsize=10)
axr.set_ylabel("residual γ_k − fit\n(symmetric log scale)")
axr.set_xticks([2, 5, 10, 15, 20, 25, 30])
axr.set_xlabel("k  (linear program L^NT_k has 3^(k−1) variables)")
ax.set_title("Krasikov–Lagarias exponent γ_k: π_a(x) ≥ x^γ for γ < γ_k", loc="left", color=INK, fontsize=13)
fig.subplots_adjust(left=0.11, right=0.97, top=0.94, bottom=0.08)
fig.savefig("gamma_trend.png", dpi=160, facecolor=SURFACE)
print(f"gamma_inf = {ginf:.4f} +- {np.sqrt(C[0, 0]):.4f}, A = {A:.4f}, r = {r:.4f}; wrote gamma_trend.png")
