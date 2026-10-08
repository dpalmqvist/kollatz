"""
MLX (Apple GPU, float32) port of the performance-critical parts of kl.py:
the map F, the power iteration and the lambda search.

No index arrays are stored.  Every index map in F is affine,
    i -> (a*i + b) mod n   with a in {2, 4},
so the "gather" splits into a strided slices of the input (one per wrap-around
of a*i + b past a multiple of n), joined with one concatenate.

Indexing (see CLAUDE.md), residue m = 3i+2 has index i in [0, N), N = 3^(k-1):
  4m mod 3^k        -> (4i + 2) mod N
  i = 3j   (m = 2 mod 9) -> cbar[4j mod N/3]
  i = 3j+2 (m = 8 mod 9) -> cbar[(2j + 1) mod N/3]
  cbar[r] = min(c[r], c[r + N/3], c[r + 2N/3])

float32 only finds candidates.  Certification: certify_fast.py (exact int64).

Usage:
  python kl_mlx.py compare KMAX            # check F and lambda_k against kl.py for k = 2..KMAX
  python kl_mlx.py lambda K [c0.npy] [lam0 lam1]   # lambda_k on the GPU, saves c_k{K}_mlx.npy
"""
import gc
import os
import sys
import time
import numpy as np
import mlx.core as mx

ALPHA = np.log2(3.0)


def affine_segments(n, a, b):
    """Slices (start, stop, step) of x such that concatenating x[start:stop:step]
    over the list gives y with y[i] = x[(a*i + b) mod n], i = 0..n-1."""
    b %= n
    segs = []
    for m in range(a):
        lo = max(0, -(-(m * n - b) // a))            # ceil((m n - b) / a)
        hi = min(n, -(-((m + 1) * n - b) // a))
        if hi > lo:
            start = a * lo + b - m * n
            segs.append((start, start + a * (hi - lo - 1) + 1, a))
    return segs


def affine_take(x, segs):
    parts = [x[s:e:st] for s, e, st in segs]
    return parts[0] if len(parts) == 1 else mx.concatenate(parts)


GX = 1 << 16          # 2-D grid: i = y * GX + x, so N may exceed 2^31 (k = 21)
INT32_MAX = 2 ** 31 - 1


def vec_shape(N):
    """MLX shapes are 32-bit ints, so a vector with N > 2^31 (k >= 21) is stored as
    (3, N/3): same bytes, row-major, the kernels index the flat buffer in 64 bits."""
    return (N,) if N <= INT32_MAX else (3, N // 3)

F_SOURCE = """
    ulong i = (ulong)thread_position_in_grid.y * GX + thread_position_in_grid.x;
    if (i >= NN) return;
    float v = p[0] * c[(4 * i + 2) % NN];
    uint t = i % 3;
    ulong j = i / 3;
    if (t == 0) {
        ulong r = (4 * j) % N3;
        v += p[1] * min(min(c[r], c[r + N3]), c[r + 2 * N3]);
    } else if (t == 2) {
        ulong r = (2 * j + 1) % N3;
        v += p[2] * min(min(c[r], c[r + N3]), c[r + 2 * N3]);
    }
    out[i] = v;
"""


def make_F(k):
    """F(c, p) as one fused Metal kernel: reads c, writes F(c), no temporaries
    (peak memory of the power iteration = 2 vectors).  Same indexing as
    make_F_slices, computed per thread in 64-bit integers."""
    N = 3 ** (k - 1)
    n3 = N // 3
    header = f"#define NN {N}UL\n#define N3 {n3}UL\n#define GX {GX}UL\n"
    kernel = mx.fast.metal_kernel(name=f"kl_F_k{k}", input_names=["c", "p"], output_names=["out"],
                                  header=header, source=F_SOURCE)
    grid = (GX, -(-N // GX), 1)

    def F(c, p):
        return kernel(inputs=[c, p], grid=grid, threadgroup=(256, 1, 1),
                      output_shapes=[vec_shape(N)], output_dtypes=[mx.float32])[0]

    return F


Q8_SOURCE = """
    ulong i = (ulong)thread_position_in_grid.y * GX + thread_position_in_grid.x;
    float lo = INFINITY, hi = -INFINITY;
    if (i < NN) {
        float v = p[0] * c[(4 * i + 2) % NN];
        uint t = i % 3;
        ulong j = i / 3;
        if (t == 0) {
            ulong r = (4 * j) % N3;
            v += p[1] * min(min(c[r], c[r + N3]), c[r + 2 * N3]);
        } else if (t == 2) {
            ulong r = (2 * j + 1) % N3;
            v += p[2] * min(min(c[r], c[r + N3]), c[r + 2 * N3]);
        }
        float rho = v / c[i];
        float qv = clamp(rint((rho - p[3]) * p[4]), -127.0f, 127.0f);
        d[i] = (char)qv;
        lo = rho;
        hi = rho;
    }
    // exact min/max of rho per threadgroup (256 threads = 8 simdgroups)
    threadgroup float smin[8];
    threadgroup float smax[8];
    lo = simd_min(lo);
    hi = simd_max(hi);
    if (thread_index_in_simdgroup == 0) {
        smin[simdgroup_index_in_threadgroup] = lo;
        smax[simdgroup_index_in_threadgroup] = hi;
    }
    threadgroup_barrier(mem_flags::mem_threadgroup);
    if (thread_index_in_threadgroup == 0) {
        for (int s = 1; s < 8; s++) {
            smin[0] = min(smin[0], smin[s]);
            smax[0] = max(smax[0], smax[s]);
        }
        ulong tg = (ulong)threadgroup_position_in_grid.y * (GX / 256) + threadgroup_position_in_grid.x;
        pmin[tg] = smin[0];
        pmax[tg] = smax[0];
    }
"""


def make_Q8(k):
    """Q(c, p) for the int8 iteration, p = [lam^-2, lam^(a-2), lam^(a-1), rho0, 1/S].
    Returns (d, pmin, pmax): d_i = clamp(round((rho_i - rho0)/S), +-127) as int8 with
    rho_i = F(c)_i / c_i, and per-threadgroup exact min / max of rho (Collatz-Wielandt
    bounds of c).  Memory: N bytes for d + 8N/256 bytes for the partials."""
    N = 3 ** (k - 1)
    n3 = N // 3
    header = f"#define NN {N}UL\n#define N3 {n3}UL\n#define GX {GX}UL\n"
    kernel = mx.fast.metal_kernel(name=f"kl_Q8_k{k}", input_names=["c", "p"],
                                  output_names=["d", "pmin", "pmax"], header=header, source=Q8_SOURCE)
    rows = -(-N // GX)
    ntg = rows * (GX // 256)

    def Q(c, p):
        return kernel(inputs=[c, p], grid=(GX, rows, 1), threadgroup=(256, 1, 1),
                      output_shapes=[vec_shape(N), (ntg,), (ntg,)],
                      output_dtypes=[mx.int8, mx.float32, mx.float32])

    return Q


@mx.compile
def _q8_update(c, d, a, b):
    # c_new = (c / m) * (rho0 + S * d) with a = rho0 / m, b = S / m; fused, so no float temporary
    return c * (a + b * d.astype(mx.float32))


def growth_q8(lam, Q, N, iters=200000, tol=2e-6, c0=None, check=100, patience=20, headroom=1.25):
    """Power iteration with an int8-compressed update, for when c and F(c) do not
    both fit in memory (k = 21: c = 13 GiB).  Per iteration:
        rho_i = F(c)_i / c_i  (exact float32),  lo/hi = min/max rho (exact),
        d_i = round((rho_i - rho0) / S) in int8,  c <- (c/m) * (rho0 + S d)
    with rho0 = (lo + hi)/2 and S = headroom * (hi - lo) / 254 from the previous
    iteration, so the quantisation error is <= S/2 ~ (hi - lo) / 400.  This only
    perturbs the iterate (certification checks the final c exactly).  Same
    interface and stopping rules as growth.  Memory: c + N bytes (+ 1/32 N floats)."""
    gc.collect()      # a Python reference cycle can otherwise keep an old N-byte d alive
    p = params(lam)
    if isinstance(c0, list):
        c0 = c0.pop()
    c = mx.ones(vec_shape(N), dtype=mx.float32) if c0 is None else (
        c0 if isinstance(c0, mx.array) else mx.array(c0, dtype=mx.float32))
    del c0
    # first pass only to get rho0, S
    d, pmin, pmax = Q(c, mx.concatenate([p, mx.array([1.0, 0.0])]))
    lo_a, hi_a = pmin.min(), pmax.max()
    mx.eval(lo_a, hi_a)
    del d, pmin, pmax
    lo = hi = None
    best, stalled = float("inf"), 0
    for it in range(1, iters + 1):
        rho0 = 0.5 * (lo_a + hi_a)
        S = mx.maximum(headroom * (hi_a - lo_a) / 254.0, 1e-12)
        m = c.min()
        d, pmin, pmax = Q(c, mx.concatenate([p, mx.stack([rho0, 1.0 / S])]))
        lo_a, hi_a = pmin.min(), pmax.max()
        a, b = rho0 / m, S / m
        # evaluate Q first: c must have no other pending users when the update
        # runs, otherwise MLX cannot reuse its buffer (peak 3.5 instead of 1.3 vectors)
        mx.eval(d, lo_a, hi_a, a, b)
        del pmin, pmax, m, rho0, S
        c = _q8_update(c, d, a, b)
        del d
        mx.eval(c)
        if it % check == 0 or it == iters:
            lo, hi = lo_a.item(), hi_a.item()
            gap = hi - lo
            if gap < tol:
                break
            if gap < 0.99 * best:
                best, stalled = gap, 0
            else:
                stalled += 1
                if stalled >= patience:
                    break
    gc.collect()
    return lo, hi, c


def needs_q8(N):
    """True when c and F(c) (2 float32 vectors) do not fit comfortably in the GPU
    working set -> use growth_q8 (c + N bytes).  On a 24 GB M5: k <= 20 exact, k = 21 int8."""
    if os.environ.get("KL_FORCE_Q8") == "1":      # for testing the int8 path at small k
        return True
    info = mx.device_info() if hasattr(mx, "device_info") else mx.metal.device_info()
    return 2 * 4 * N > 0.7 * info["max_recommended_working_set_size"]


# stopping rules for the int8 path: an iteration costs ~1.8 s at k = 21, and the
# int8 noise floor of hi - lo (~2e-6) sits near tol, so stall detection must be quicker
Q8_KW = dict(tol=2.5e-6, check=25, patience=4)


def make_growth(k):
    """(growth function, map, extra kwargs) for k: exact 2-vector iteration or int8."""
    N = 3 ** (k - 1)
    if needs_q8(N):
        return growth_q8, make_Q8(k), Q8_KW
    return growth, make_F(k), {}


def lift_to_file(src, dst):
    """Write tile(c_{k-1}, 3) to dst.npy via numpy memmaps (no GPU memory), so
    that mx.load(dst) is the only full-size allocation (k = 21: 13 GiB)."""
    c0 = np.load(src, mmap_mode="r")
    n0 = c0.size
    c0 = c0.reshape(-1)
    out = np.lib.format.open_memmap(dst, mode="w+", dtype=np.float32, shape=(3, n0))   # = tile, see vec_shape
    for j in range(3):
        for s in range(0, n0, 1 << 26):
            out[j, s:s + (1 << 26)] = c0[s:s + (1 << 26)]
    out.flush()
    del out


def make_F_slices(k):
    """Return F(c, p) with p = mx.array([lam^-2, lam^(a-2), lam^(a-1)], float32).
    Compiled; the structure of k is baked into the closure, lam is an input.
    Reference implementation for make_F (uses ~3 vectors of memory)."""
    N = 3 ** (k - 1)
    n3 = N // 3
    nxt = affine_segments(N, 4, 2)
    aux2 = affine_segments(n3, 4, 0)
    aux8 = affine_segments(n3, 2, 1)

    def F(c, p):
        cbar = mx.minimum(mx.minimum(c[:n3], c[n3:2 * n3]), c[2 * n3:])
        out = (p[0] * affine_take(c, nxt)).reshape(n3, 3)
        add2 = p[1] * affine_take(cbar, aux2)
        add8 = p[2] * affine_take(cbar, aux8)
        extra = mx.stack([add2, mx.zeros_like(add2), add8], axis=1)
        return (out + extra).reshape(N)

    return mx.compile(F)


def params(lam):
    return mx.array([lam ** -2, lam ** (ALPHA - 2), lam ** (ALPHA - 1)], dtype=mx.float32)


def ratio_bounds(Fc, c, chunk=1 << 26):
    """min and max of Fc/c, chunked so the temporary is at most `chunk` floats."""
    N = c.size
    los, his = [], []
    for s in range(0, N, chunk):
        r = Fc[s:s + chunk] / c[s:s + chunk]
        lo, hi = r.min(), r.max()
        mx.eval(lo, hi)
        los.append(lo.item())
        his.append(hi.item())
    return min(los), max(his)


def growth(lam, F, N, iters=200000, tol=2e-6, c0=None, check=100, patience=20):
    """Power iteration c <- F(c / min c) on the GPU (F is 1-homogeneous, so the
    normalisation is folded into the coefficients p and no extra vector is
    needed: peak memory = c and F(c)).  Every `check` iterations
    the Collatz–Wielandt bounds lo = min F(c)/c <= r <= hi = max F(c)/c are read
    back.  Stops when hi - lo < tol, or when hi - lo has not improved by 1% for
    `patience` checks: in float32 the gap has a rounding floor that can lie
    above tol (k = 3: ~3e-5), and iterating further is wasted.
    c0 may be a one-element list [c]; it is then emptied so that the caller's
    reference does not keep the old vector alive (otherwise 3 vectors at peak).
    Returns (lo, hi, c) with c an mx.array, NOT normalised (scale is irrelevant).
    The bounds are those of the last F evaluation, i.e. for the returned c's
    predecessor; the returned c = F(previous) is at least as good."""
    p = params(lam)
    if isinstance(c0, list):
        c0 = c0.pop()
    if c0 is None:
        c = mx.ones((N,), dtype=mx.float32)
    else:
        c = c0 if isinstance(c0, mx.array) else mx.array(c0, dtype=mx.float32)
    del c0
    lo = hi = None
    best, stalled = float("inf"), 0
    for it in range(1, iters + 1):
        m = c.min()
        Fc = F(c, p / m)                       # = F(c / min c)
        if it % check == 0 or it == iters:
            mx.eval(Fc, m)
            # Collatz-Wielandt bounds for c/m:  F(c/m) / (c/m) = m * Fc / c
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


def lambda_k(k, iters=200000, tol=2e-6, verbose=False, lam0=1.75, lam1=1.85, c0=None,
             width=1e-7, steps=30, lam_min=1.0, lam_max=2.0):
    """Secant method on f(lam) = log r(F_lam), r estimated by the midpoint of the
    Collatz–Wielandt bounds; the root is lambda_k (r is decreasing in lam).
    Each evaluation warm-starts the power iteration from the previous c.
    Stops when the next secant step is shorter than width (default 1e-7 = float32
    resolution of lam_k; smaller widths only wander in the rounding noise).  (Stopping as soon as
    1 lies in [lo, hi] is too early: the slope d log r / d lam is only ~ -0.3, so
    a gap of 1e-6 in r leaves lam off by ~ 3e-6.)
    c0: optional warm start (length N, or N/3 which is lifted with tile), or a
    one-element list holding it (then emptied, so the old vector can be freed).
    Also stops when the step is below the noise level (hi - lo) / 2|slope|, the
    slope taken from the first two points (k = 18 otherwise wandered 8 steps).
    Returns (lam, c) with c (mx.array, not normalised) computed at lam."""
    N = 3 ** (k - 1)
    grow, F, extra = make_growth(k)
    if extra:
        tol = extra["tol"]
    c = None
    if isinstance(c0, list):          # caller hands over its only reference (see growth)
        c0 = c0.pop()
    if c0 is not None:
        c = c0 if isinstance(c0, mx.array) else mx.array(np.asarray(c0, dtype=np.float32))
        del c0
        if 3 * c.size == N:
            c = mx.tile(c, 3)
        mx.eval(c)

    box = [c]          # the only reference to the current vector between evaluations
    del c

    def f(lam):
        kw = {**extra, "tol": tol}
        lo, hi, c = grow(lam, F, N, iters=iters, c0=box, **kw)
        box.append(c)
        if verbose:
            print(f"  lam={lam:.10f} lo={lo:.9f} hi={hi:.9f}", flush=True)
        return np.log(0.5 * (lo + hi)), lo, hi

    f0, _, _ = f(lam0)
    f1, lo, hi = f(lam1)
    slope = (f1 - f0) / (lam1 - lam0)          # from two well-separated points
    for _ in range(steps):
        if f1 == f0:
            break
        lam2 = lam1 - f1 * (lam1 - lam0) / (f1 - f0)
        lam2 = min(max(lam2, lam_min), lam_max)
        # lam is only determined to ~ (noise in log r) / |slope| = (hi - lo) / 2|slope|
        if abs(lam2 - lam1) < max(width, 0.5 * (hi - lo) / abs(slope)):
            break
        lam0, f0 = lam1, f1
        lam1 = lam2
        f1, lo, hi = f(lam1)
    return lam1, box.pop()


def compare(kmax):
    import kl
    rng = np.random.default_rng(0)
    for k in range(2, kmax + 1):
        S = kl.structure(k)
        N = S["N"]
        c = rng.uniform(1.0, 50.0, N)
        lam = 1.79
        ref = kl.F(c, lam, S)
        got = np.array(make_F(k)(mx.array(c, dtype=mx.float32), params(lam)))
        got_s = np.array(make_F_slices(k)(mx.array(c, dtype=mx.float32), params(lam)))
        assert np.max(np.abs(got - got_s) / got_s) < 1e-6, "kernel F != slice F"
        relF = np.max(np.abs(got - ref) / ref)

        t = time.time()
        lam_np, c_np, _ = kl.lambda_k(k)
        t_np = time.time() - t
        t = time.time()
        lam_mx, c_mx = lambda_k(k)
        t_mx = time.time() - t
        print(f"k={k:2d} N={N:7d}  F rel.err={relF:.1e}  "
              f"lam numpy={lam_np:.7f} ({t_np:6.1f}s)  mlx={lam_mx:.7f} ({t_mx:6.1f}s)  "
              f"d={lam_mx - lam_np:+.1e}", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "compare":
        compare(int(sys.argv[2]))
    elif cmd == "lambda":
        k = int(sys.argv[2])
        c0 = None
        lifted = None
        if len(sys.argv) > 3:
            src = sys.argv[3]
            n0 = np.load(src, mmap_mode="r").size
            if 3 * n0 == 3 ** (k - 1) and needs_q8(3 ** (k - 1)):
                lifted = f"c_k{k}_lift_tmp.npy"
                lift_to_file(src, lifted)
                src = lifted
            c0 = [mx.load(src)]
            if lifted:
                os.remove(lifted)
        starts = dict(lam0=float(sys.argv[4]), lam1=float(sys.argv[5])) if len(sys.argv) > 5 else {}
        t = time.time()
        mx.reset_peak_memory()
        lam, c = lambda_k(k, c0=c0, verbose=True, **starts)
        print(f"MLX peak memory {mx.get_peak_memory() / 2**30:.2f} GiB "
              f"(one vector = {4 * 3 ** (k - 1) / 2**30:.2f} GiB)")
        print(f"k={k} lam_k={lam:.7f} Cmax={(c.max() / c.min()).item():.4f}  {time.time() - t:.1f}s")
        mx.save(f"c_k{k}_mlx.npy", c)
    else:
        sys.exit(__doc__)
