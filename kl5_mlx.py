"""
MLX (Metal, float32) version of the 5x+1 Krasikov–Lagarias system of kl5.py, for k = 13, 14 (N = 5^(k-1):
2.4e8 and 1.2e9 variables, 2 float32 vectors = 2 / 9.8 GB).  Same indexing as kl5.structure5, computed per
thread; same power iteration and secant as kl_mlx (2 vectors, normalisation folded into the coefficients).

  python kl5_mlx.py compare KMAX              # lambda_k(5) vs kl5.py (numpy float64) for k = 2..KMAX
  python kl5_mlx.py lambda K [c0.npy] [lam0 lam1]   # saves c5_k{K}_mlx.npy and prints lambda_k, gamma_k, rho_k
"""
import sys
import time

import numpy as np
import mlx.core as mx

from kl_mlx import GX, vec_shape, ratio_bounds

BETA = np.log2(5.0)

F5_SOURCE = """
    ulong i = (ulong)thread_position_in_grid.y * GX + thread_position_in_grid.x;
    if (i >= NN) return;
    float v = p[0] * c[(16 * i + 9) % NN];
    uint t = i % 5;
    if (t != 2) {
        ulong j;
        float w;
        if (t == 0)      { j = ((16 * i + 5) / 5) % N5; w = p[1]; }
        else if (t == 1) { j = ((2 * i - 2) / 5) % N5;  w = p[2]; }
        else if (t == 3) { j = ((8 * i + 1) / 5) % N5;  w = p[3]; }
        else             { j = ((4 * i - 1) / 5) % N5;  w = p[4]; }
        float m = c[j];
        m = min(m, c[j + N5]);
        m = min(m, c[j + 2 * N5]);
        m = min(m, c[j + 3 * N5]);
        m = min(m, c[j + 4 * N5]);
        v += w * m;
    }
    out[i] = v;
"""


def make_F5(k):
    N = 5 ** (k - 1)
    header = f"#define NN {N}UL\n#define N5 {N // 5}UL\n#define GX {GX}UL\n"
    kernel = mx.fast.metal_kernel(name=f"kl5_F_k{k}", input_names=["c", "p"], output_names=["out"],
                                  header=header, source=F5_SOURCE)
    grid = (GX, -(-N // GX), 1)

    def F(c, p):
        return kernel(inputs=[c, p], grid=grid, threadgroup=(256, 1, 1),
                      output_shapes=[vec_shape(N)], output_dtypes=[mx.float32])[0]

    return F


def params5(lam):
    return mx.array([lam ** -4, lam ** (BETA - 4), lam ** (BETA - 1), lam ** (BETA - 3), lam ** (BETA - 2)],
                    dtype=mx.float32)


def growth5(lam, F, N, iters=200000, tol=2e-6, c0=None, check=100, patience=20):
    p = params5(lam)
    if isinstance(c0, list):
        c0 = c0.pop()
    c = mx.ones(vec_shape(N), dtype=mx.float32) if c0 is None else c0
    del c0
    lo = hi = None
    best, stalled = float("inf"), 0
    for it in range(1, iters + 1):
        m = c.min()
        Fc = F(c, p / m)
        if it % check == 0 or it == iters:
            mx.eval(Fc, m)
            lo, hi = ratio_bounds(Fc, c)
            lo, hi = lo * m.item(), hi * m.item()
            c = Fc
            gap = hi - lo
            if gap < tol:
                break
            if gap < 0.99 * best:
                best, stalled = gap, 0
            else:
                stalled += 1
                if stalled >= patience:
                    break
        else:
            c = Fc
            mx.eval(c)
        del Fc
    return lo, hi, c


def rho5(c, N):
    n5 = N // 5
    cb = c[:n5]
    for l in range(1, 5):
        cb = mx.minimum(cb, c[l * n5:(l + 1) * n5])
    return (cb.mean() / c.mean()).item()


def lambda5(k, c0=None, lam0=1.40, lam1=1.42, width=1e-7, steps=30, verbose=False):
    N = 5 ** (k - 1)
    F = make_F5(k)
    if c0 is not None and 5 * c0.size == N:
        c0 = mx.tile(c0, 5)
    box = [c0]
    lo = hi = None

    def f(lam):
        nonlocal lo, hi
        lo, hi, c = growth5(lam, F, N, c0=box)
        box.append(c)
        if verbose:
            print(f"  lam={lam:.10f} lo={lo:.9f} hi={hi:.9f}", flush=True)
        return np.log(0.5 * (lo + hi))

    f0 = f(lam0)
    f1 = f(lam1)
    slope = (f1 - f0) / (lam1 - lam0)
    for _ in range(steps):
        if f1 == f0:
            break
        lam2 = lam1 - f1 * (lam1 - lam0) / (f1 - f0)
        lam2 = min(max(lam2, 1.0), 2.0)
        if abs(lam2 - lam1) < max(width, 0.5 * (hi - lo) / abs(slope)):
            break
        lam0, f0 = lam1, f1
        lam1 = lam2
        f1 = f(lam1)
    return lam1, box.pop()


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "compare":
        import kl5
        c = None
        for k in range(2, int(sys.argv[2]) + 1):
            N = 5 ** (k - 1)
            rng = np.random.default_rng(0)
            x = rng.uniform(1.0, 50.0, N).astype(np.float32)
            ref = kl5.F5(x.astype(np.float64), 1.4, kl5.structure5(k))
            got = np.array(make_F5(k)(mx.array(x), params5(1.4)))
            relF = np.max(np.abs(got - ref) / ref)
            t = time.time()
            lam_np, c_np, S = kl5.lambda5(k, c0=None if c is None else np.tile(c, 5))
            c = c_np
            t_np = time.time() - t
            t = time.time()
            lam_mx, cm = lambda5(k)
            t_mx = time.time() - t
            print(f"k={k:2d} N={N:9d} F rel.err={relF:.1e} lam numpy={lam_np:.7f} ({t_np:.1f}s) "
                  f"mlx={lam_mx:.7f} ({t_mx:.1f}s) d={lam_mx - lam_np:+.1e} rho mlx={rho5(cm, N):.6f} "
                  f"numpy={kl5.rho5(c_np, S):.6f}", flush=True)
    elif cmd == "lambda":
        k = int(sys.argv[2])
        c0 = mx.load(sys.argv[3]) if len(sys.argv) > 3 else None
        starts = dict(lam0=float(sys.argv[4]), lam1=float(sys.argv[5])) if len(sys.argv) > 5 else {}
        N = 5 ** (k - 1)
        t = time.time()
        mx.reset_peak_memory()
        lam, c = lambda5(k, c0=c0, verbose=True, **starts)
        rho = rho5(c, N)
        print(f"MLX peak memory {mx.get_peak_memory() / 2**30:.2f} GiB (one vector = {4 * N / 2**30:.2f} GiB)")
        print(f"k={k} N={N} lam_k(5)={lam:.7f} gamma={np.log2(lam):.6f} rho={rho:.6f} 1-rho={1 - rho:.6f} "
              f"Cmax={(c.max() / c.min()).item():.3f}  {time.time() - t:.1f}s", flush=True)
        mx.save(f"c5_k{k}_mlx.npy", c)
