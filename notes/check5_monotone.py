import sys, numpy as np
sys.path.insert(0, "/Users/daniel/devel/kollatz")
import kl5
# (a) x16 single cycle on indices i -> (16 i + 9) mod N
for k in range(2, 10):
    S = kl5.structure5(k); nxt = S["nxt"]; N = S["N"]
    i, n = 0, 0
    while True:
        i = nxt[i]; n += 1
        if i == 0: break
    print(f"5x+1 k={k}: x16 cycle length {n} of N={N}", "single" if n == N else "SPLIT")
# (b) tiling gain at lambda_k(5)
for k in range(2, 8):
    lam, c, S = kl5.lambda5(k)
    lo, hi, c = kl5.growth5(lam, S, c0=c, iters=400000, tol=1e-14)
    t = np.tile(c, 5); S1 = kl5.structure5(k + 1)
    rel = (kl5.F5(t, lam, S1) - t) / t
    z = t.copy(); y = t.copy()
    for _ in range(1, S1["N"]):
        y = kl5.F5(y, lam, S1); z += y
    cw = (kl5.F5(z, lam, S1) / z).min()
    print(f"5x+1 k={k} lam={lam:.7f} resid={max(abs(lo-1),abs(hi-1)):.0e} min gain {rel.min():+.1e} frac>1e-6 {np.mean(rel>1e-6):.3f}  CW r_(k+1)(lam_k) >= {cw:.6f}")
# (c) 2 - lambda ratios for 3x+1
L = {12:1.8064236,13:1.8188237,14:1.8307723,15:1.8419687,16:1.8522346,17:1.8616888,18:1.8703250,19:1.8783132,20:1.8857083,21:1.8925462,22:1.8988933}
print("3x+1 (2-lam_{k+1})/(2-lam_k):", " ".join(f"{k}:{(2-L[k+1])/(2-L[k]):.4f}" for k in range(12,22)))
