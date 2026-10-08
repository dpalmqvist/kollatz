"""
k = 22 on a 64 GB Apple-silicon machine.  The float32 vector (N = 3^21, 39.0 GiB)
exceeds Metal's max_buffer_length (38.9 GiB on an M4 Pro 64 GB), so c is held as
three buffers c_j of length n3 = N/3, j = top ternary digit:  c[i] = c_j[i - j*n3].
The int8 power iteration of kl_mlx.growth_q8 is reproduced with a kernel that
reads the three buffers; the cbar-minimum over the top digit becomes
min(c_0[r], c_1[r], c_2[r]) and the warm start tile(c_{k-1}, 3) is simply three
copies of c_{k-1} (no lift through disk).  Memory: 3 parts (39 GiB) + int8 d
(9.7 GiB) + partials (0.3 GiB) ~ 49 GiB.

Usage:
  python kl_split.py test KMAX                        # split kernels vs kl_mlx at small k (forced split)
  python kl_split.py lambda K SRC.npy [lam0 lam1]     # lambda_K; SRC = c_{K-1} (length N/3) or
                                                      #   c_k{K}_part0.npy (resume); saves c_k{K}_part{0,1,2}.npy
  python kl_split.py certify K LAMBDA SRC.npy         # trim at LAMBDA, write certs/kK_LAMBDA/c_f32.npy
                                                      #   (combined, via memmap), int64 check (numpy), cert.json
Float32 only finds candidates; the certificate is checked exactly (certify_fast.check).
"""
import gc
import os
import sys
import time
import numpy as np
import mlx.core as mx

import kl_mlx
from kl_mlx import GX, INT32_MAX, params, _q8_update, Q8_KW

HEADER_FN = """
inline float cget(const device float* c0, const device float* c1, const device float* c2, ulong idx) {
    ulong b = idx / N3;
    ulong o = idx - b * N3;
    return b == 0 ? c0[o] : (b == 1 ? c1[o] : c2[o]);
}
"""

Q8_SPLIT_SOURCE = """
    ulong i = (ulong)thread_position_in_grid.y * GX + thread_position_in_grid.x;
    float lo = INFINITY, hi = -INFINITY;
    if (i < NN) {
        float v = p[0] * cget(c0, c1, c2, (4 * i + 2) % NN);
        uint t = i % 3;
        ulong j = i / 3;
        if (t == 0) {
            ulong r = (4 * j) % N3;
            v += p[1] * min(min(c0[r], c1[r]), c2[r]);
        } else if (t == 2) {
            ulong r = (2 * j + 1) % N3;
            v += p[2] * min(min(c0[r], c1[r]), c2[r]);
        }
        float rho = v / cget(c0, c1, c2, i);
        float qv = clamp(rint((rho - p[3]) * p[4]), -127.0f, 127.0f);
        d[i] = (char)qv;
        lo = rho;
        hi = rho;
    }
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


def part_shape(n3):
    """2-D shape (s, n3/s) with n3/s <= INT32_MAX, s a power of 3 (always 2-D so that
    the int8 slices d[j*s:(j+1)*s] match the parts exactly)."""
    s = 1
    while n3 // s > INT32_MAX:
        s *= 3
    return (s, n3 // s)


def make_Q8_split(k):
    """Q(parts, p) -> (d, pmin, pmax) exactly as kl_mlx.make_Q8, with c = concat(parts)."""
    N = 3 ** (k - 1)
    n3 = N // 3
    s, w = part_shape(n3)
    header = f"#define NN {N}UL\n#define N3 {n3}UL\n#define GX {GX}UL\n" + HEADER_FN
    kernel = mx.fast.metal_kernel(name=f"kl_Q8s_k{k}", input_names=["c0", "c1", "c2", "p"],
                                  output_names=["d", "pmin", "pmax"], header=header, source=Q8_SPLIT_SOURCE)
    rows = -(-N // GX)
    ntg = rows * (GX // 256)

    def Q(parts, p):
        return kernel(inputs=[*parts, p], grid=(GX, rows, 1), threadgroup=(256, 1, 1),
                      output_shapes=[(3 * s, w), (ntg,), (ntg,)],
                      output_dtypes=[mx.int8, mx.float32, mx.float32])

    return Q, s


def growth_q8_split(lam, Q, N, iters=200000, tol=2.5e-6, c0=None, check=25, patience=4, headroom=1.25,
                    verbose=True):
    """kl_mlx.growth_q8 on a vector held as three parts.  c0: one-element list holding
    the parts list [c_0, c_1, c_2] (emptied).  Returns (lo, hi, parts)."""
    Q, s = Q
    gc.collect()
    t0 = time.time()
    p = params(lam)
    parts = c0.pop() if isinstance(c0, list) else c0
    del c0
    d, pmin, pmax = Q(parts, mx.concatenate([p, mx.array([1.0, 0.0])]))
    lo_a, hi_a = pmin.min(), pmax.max()
    mx.eval(lo_a, hi_a)
    del d, pmin, pmax
    lo = hi = None
    best, stalled = float("inf"), 0
    for it in range(1, iters + 1):
        rho0 = 0.5 * (lo_a + hi_a)
        S = mx.maximum(headroom * (hi_a - lo_a) / 254.0, 1e-12)
        m = mx.minimum(mx.minimum(parts[0].min(), parts[1].min()), parts[2].min())
        d, pmin, pmax = Q(parts, mx.concatenate([p, mx.stack([rho0, 1.0 / S])]))
        lo_a, hi_a = pmin.min(), pmax.max()
        a, b = rho0 / m, S / m
        mx.eval(d, lo_a, hi_a, a, b)
        del pmin, pmax, m, rho0, S
        for j in range(3):
            cj = parts[j]
            parts[j] = None
            dj = d[j * s:(j + 1) * s]
            parts[j] = _q8_update(cj, dj, a, b)   # cj has no other reference -> buffer reused
            del cj, dj
            mx.eval(parts[j])
        del d
        if it % check == 0 or it == iters:
            lo, hi = lo_a.item(), hi_a.item()
            gap = hi - lo
            if verbose:
                print(f"    it={it} lo={lo:.9f} hi={hi:.9f} gap={gap:.2e}  {time.time() - t0:.0f}s", flush=True)
            if gap < tol:
                break
            if gap < 0.99 * best:
                best, stalled = gap, 0
            else:
                stalled += 1
                if stalled >= patience:
                    break
    gc.collect()
    return lo, hi, parts


def load_parts(k, src):
    """Three parts for level k from src: c_{k-1} (size N/3; three copies = tile) or
    c_k{k}_part0.npy (then part1/part2 alongside)."""
    N = 3 ** (k - 1)
    n3 = N // 3
    shape = part_shape(n3)
    n0 = np.load(src, mmap_mode="r").size
    if n0 == n3:
        parts = [mx.load(src).reshape(shape) for _ in range(3)]   # separate buffers
    elif n0 == N:
        raise ValueError("full-length vector cannot be loaded into one buffer; use parts")
    else:
        assert src.endswith("_part0.npy"), src
        parts = [mx.load(src.replace("_part0", f"_part{j}")).reshape(shape) for j in range(3)]
    mx.eval(*parts)
    return parts


def lambda_k_split(k, parts, lam0, lam1, iters=200000, verbose=True, width=1e-7, steps=30):
    """Secant method of kl_mlx.lambda_k with growth_q8_split."""
    N = 3 ** (k - 1)
    Qs = make_Q8_split(k)
    box = [parts]
    del parts
    lo = hi = None

    def f(lam):
        nonlocal lo, hi
        t = time.time()
        lo, hi, pr = growth_q8_split(lam, Qs, N, iters=iters, c0=box, verbose=verbose, **Q8_KW)
        box.append(pr)
        if verbose:
            print(f"  lam={lam:.10f} lo={lo:.9f} hi={hi:.9f}  {time.time() - t:.0f}s  "
                  f"peak {mx.get_peak_memory() / 2**30:.1f} GiB", flush=True)
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


def save_parts(k, parts):
    for j, pj in enumerate(parts):
        mx.save(f"c_k{k}_part{j}.npy", pj)


def combine_to_memmap(k, dst, part_files):
    """Write the full vector dst.npy (float32, shape (N,)) from the three part files,
    chunked through memmaps (no large RAM use)."""
    N = 3 ** (k - 1)
    n3 = N // 3
    out = np.lib.format.open_memmap(dst, mode="w+", dtype=np.float32, shape=(N,))
    for j, pf in enumerate(part_files):
        src = np.load(pf, mmap_mode="r").reshape(-1)
        assert src.size == n3
        for s in range(0, n3, 1 << 26):
            out[j * n3 + s:j * n3 + min(s + (1 << 26), n3)] = src[s:s + (1 << 26)]
        del src
    out.flush()
    del out


def test(kmax):
    """At small k: (1) the split kernel's d/pmin/pmax equal kl_mlx.make_Q8's bit for bit;
    (2) lambda from growth_q8_split equals kl_mlx.lambda_k (same int8 path, forced)."""
    os.environ["KL_FORCE_Q8"] = "1"
    rng = np.random.default_rng(1)
    for k in range(4, kmax + 1):
        N = 3 ** (k - 1)
        n3 = N // 3
        c = rng.uniform(1.0, 50.0, N).astype(np.float32)
        p = mx.concatenate([params(1.8), mx.array([1.0, 100.0])])
        d0, mn0, mx0 = kl_mlx.make_Q8(k)(mx.array(c), p)
        Q, s = make_Q8_split(k)
        parts = [mx.array(c[j * n3:(j + 1) * n3]).reshape(part_shape(n3)) for j in range(3)]
        d1, mn1, mx1 = Q(parts, p)
        mx.eval(d0, mn0, mx0, d1, mn1, mx1)
        same = (np.array_equal(np.array(d0).reshape(-1), np.array(d1).reshape(-1))
                and np.array_equal(np.array(mn0), np.array(mn1)) and np.array_equal(np.array(mx0), np.array(mx1)))
        t = time.time()
        lam_ref, _ = kl_mlx.lambda_k(k, lam0=1.75, lam1=1.85)
        t_ref = time.time() - t
        t = time.time()
        mx.reset_peak_memory()
        parts = [mx.ones(part_shape(n3), dtype=mx.float32) for _ in range(3)]
        lam_sp, pr = lambda_k_split(k, parts, 1.75, 1.85, verbose=False)
        t_sp = time.time() - t
        peak = mx.get_peak_memory() / (4 * N)
        print(f"k={k:2d} N={N:8d} kernel identical={same}  lam q8={lam_ref:.7f} ({t_ref:.1f}s)  "
              f"split={lam_sp:.7f} ({t_sp:.1f}s) d={lam_sp - lam_ref:+.1e}  peak={peak:.2f} vectors", flush=True)
        assert same


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "test":
        test(int(sys.argv[2]))
    elif cmd == "lambda":
        k, src = int(sys.argv[2]), sys.argv[3]
        lam0, lam1 = (float(sys.argv[4]), float(sys.argv[5])) if len(sys.argv) > 5 else (1.75, 1.85)
        t = time.time()
        mx.reset_peak_memory()
        parts = load_parts(k, src)
        lam, parts = lambda_k_split(k, parts, lam0, lam1)
        cmax = max(pj.max().item() for pj in parts) / min(pj.min().item() for pj in parts)
        print(f"MLX peak memory {mx.get_peak_memory() / 2**30:.2f} GiB (one vector = {4 * 3 ** (k - 1) / 2**30:.2f} GiB)")
        print(f"k={k} lam_k={lam:.7f} Cmax={cmax:.4f}  {time.time() - t:.1f}s", flush=True)
        save_parts(k, parts)
    elif cmd == "rate":
        # growth ratio bounds and mixing ratio rho = mean(cbar)/mean(c) at LAMBDA (e.g. 2), nothing written
        from fractions import Fraction
        k, lam_str, src = int(sys.argv[2]), sys.argv[3], sys.argv[4]
        N = 3 ** (k - 1)
        t = time.time()
        parts = load_parts(k, src)
        lo, hi, parts = growth_q8_split(float(Fraction(lam_str)), make_Q8_split(k), N, c0=[parts], **Q8_KW)
        # chunked sums (no full-size temporaries): parts are (s, w) arrays, rows contiguous
        tot = 0.0; totbar = 0.0            # Python float64 accumulation of float32 chunk sums (2^22 elements)
        for r in range(parts[0].shape[0]):
            for c0_ in range(0, parts[0].shape[1], 1 << 22):
                sl = [pj[r, c0_:c0_ + (1 << 22)] for pj in parts]
                tot += sum(x.sum().item() for x in sl)
                totbar += mx.minimum(mx.minimum(sl[0], sl[1]), sl[2]).sum().item()
        rho = 3 * totbar / tot
        print(f"k={k} lam={lam_str} power iteration (int8, split): {time.time() - t:.0f}s  lo={lo:.9f} hi={hi:.9f} "
              f"r_mid={0.5 * (lo + hi):.9f} rho={rho:.7f} 1-rho={1 - rho:.7f}  peak {mx.get_peak_memory() / 2**30:.1f} GiB", flush=True)
    elif cmd == "certify":
        import certify_fast
        from fractions import Fraction
        k, lam_str, src = int(sys.argv[2]), sys.argv[3], sys.argv[4]
        upper = "--upper" in sys.argv          # infeasibility certificate (strict F(C) < C), see certify_fast.py
        N = 3 ** (k - 1)
        outdir = f"certs/k{k}_{lam_str}{'_upper' if upper else ''}"
        os.makedirs(outdir, exist_ok=True)
        t = time.time()
        parts = load_parts(k, src)
        lo, hi, parts = growth_q8_split(float(Fraction(lam_str)), make_Q8_split(k), N, c0=[parts], **Q8_KW)
        print(f"power iteration (float32, GPU, int8 update, split): {time.time() - t:.1f}s  "
              f"lo={lo:.9f} hi={hi:.9f}  peak {mx.get_peak_memory() / 2**30:.1f} GiB", flush=True)
        tmp = [os.path.join(outdir, f"part{j}.npy") for j in range(3)]
        for pf, pj in zip(tmp, parts):
            mx.save(pf, pj)
        del parts
        mx.clear_cache()
        gc.collect()
        cpath = os.path.join(outdir, "c_f32.npy")
        t = time.time()
        combine_to_memmap(k, cpath, tmp)
        for pf in tmp:
            os.remove(pf)
        print(f"combined {cpath}: {time.time() - t:.0f}s", flush=True)
        c = np.load(cpath, mmap_mode="r").reshape(-1)
        t = time.time()
        ok, res = certify_fast.certify(k, lam_str, c, backend="numpy", upper=upper)
        del c
        okb, bad, worst, dt = res["numpy"]
        print(f"C = c * 2^{res['b']}, D = 2^{res['d']}, Cmax/Cmin = {res['Cmax/Cmin']:.3f}")
        print(f"  numpy: VERIFIED={okb}{'' if okb else f' (fails at index {bad})'} min rel. slack={worst:.3e}  {dt:.1f}s")
        if "reason" in res:
            print(f"  reason: {res['reason']}")
        print(f"k={k} lam_cert={lam_str} VERIFIED={ok}" + (" (UPPER: infeasible, lambda_k < lam)" if upper and ok else ""), flush=True)
        if ok:
            cert = certify_fast.write_cert_json(k, lam_str, res, outdir)
            print(f"saved {outdir}/  c sha256 (data) {cert['c_sha256_data']}")
        else:
            print("not saved: certificate did not verify (c_f32.npy left in place for inspection)")
