"""
Fast rigorous certificate for L^NT_k(lambda), exact int64 arithmetic (NumPy on
the CPU or MLX on the GPU), streaming over chunks so that memory is ~4 bytes per
variable.  Same statement as certify.py, which remains the exact Python-integer
reference.

The certificate vector is the float32 vector c itself, read as integers
    C_i = c_i * 2^b,      b = 23 - floor(log2(min c)),
which is an exact integer for every positive normal float32 c_i (ulp(c_i) >= 2^-b).
C_i is formed with integer bit operations (mantissa << shift); an entry that is
not a positive finite float32 with c_i * 2^b integral makes the check fail.

With lam = P/Q rational and D = 2^d:
  q  = floor(D * Q^2 / P^2)              <= D * lam^-2          (exact integers)
  Lj = floor(D * lower(lam^(alpha-j)))   <= D * lam^(alpha-j)   (j = 1, 2; lower()
                                            is the rigorous interval bound of certify.py)
  Cbar_r = min(C_r, C_{r+N/3}, C_{r+2N/3})
and every inequality is checked in the form
  C_m * D <= q * C_{4m} + Lj * Cbar        (Lj = 0 for m = 5 mod 9).
Since q/D <= lam^-2, Lj/D <= lam^(alpha-j) and C >= 0, this implies
  C_m <= lam^-2 C_{4m} + lam^(alpha-j) Cbar,
i.e. C is a feasible point of L^NT_k(lam) (C_m >= 1 by homogeneity).

No rounding occurs anywhere: all operations are int64 shifts, +, *, min and
compare, and before the check we prove in Python integers that every
intermediate is below 2^63 (max C * (q + max Lj) < 2^63 and max C * D < 2^63).

Usage:
  python certify_fast.py k LAMBDA [c0.npy] [--backend numpy|mlx|both] [--exact] [--save]
    c0.npy   warm start for the float32 power iteration (length N or N/3)
    --exact  also re-check the same integers with Python integers (small k)
    --save   keep certs/k{k}_{LAMBDA}/ (c_f32.npy + cert.json; check with verify_cert.py)
"""
import hashlib
import json
import math
import os
import shutil
import sys
import tempfile
import time
from fractions import Fraction
import numpy as np
import mpmath

from certify import lower_power

INT64_LIMIT = 2 ** 63
CHUNK = 2 ** 22


def coefficients(lam, d):
    """Integer coefficients (D, q, L2, L1) for lam (Fraction), D = 2^d."""
    D = 2 ** d
    q = (D * lam.denominator ** 2) // lam.numerator ** 2
    L2 = lower_power(lam, 2)
    L1 = lower_power(lam, 1)
    L2n = (D * L2.numerator) // L2.denominator
    L1n = (D * L1.numerator) // L1.denominator
    return D, q, L2n, L1n


def scale_bits(cmin, cmax):
    """b with c * 2^b integral for all float32 c >= cmin, and d = log2 D such
    that max C * (q + L) < 2^63 (q + L < 2.5 D < 4 D)."""
    b = 23 - math.floor(math.log2(cmin))
    Cmax = Fraction(float(cmax)) * 2 ** b
    d = 63 - 2 - math.ceil(math.log2(Cmax + 1)) - 1
    return b, d


def to_int64(xp, x, b):
    """Exact C = x * 2^b for float32 x via bit operations.  Returns (C, ok) where
    ok is False for entries that are not positive normal finite floats or for
    which x * 2^b is not an integer (C is then meaningless)."""
    if xp is np:
        u = x.view(np.uint32).astype(np.int64)
    else:
        u = xp.view(x, xp.uint32).astype(xp.int64)
    sign = u >> 31
    E = (u >> 23) & 0xFF
    M = (u & 0x7FFFFF) | 0x800000
    sh = E - 150 + b
    ok = (sign == 0) & (E >= 1) & (E <= 254) & (sh >= 0) & (sh <= 38)
    C = xp.left_shift(M, xp.maximum(sh, 0))
    return C, ok


def check(c, b, D, q, L2n, L1n, backend="numpy", chunk=CHUNK):
    """Check all inequalities for C = c * 2^b.  c: float32 vector (numpy array or
    memmap for numpy, mx.array for mlx).  Returns (ok, first failing index or
    None, min relative slack (float, for information only), reason)."""
    if backend == "mlx":
        import mlx.core as mx
        xp = mx
        cx = c if isinstance(c, mx.array) else mx.array(np.asarray(c))
        assert cx.dtype == mx.float32
        take = mx.take
        i64 = lambda v: mx.array(v, dtype=mx.int64)
        any_ = lambda a: mx.any(a).item()
        npy = lambda a: np.array(a)
    else:
        xp = np
        cx = c
        assert cx.dtype == np.float32
        take = np.take
        i64 = np.int64
        any_ = lambda a: bool(a.any())
        npy = lambda a: a
    N = cx.size
    n3 = N // 3
    D_, q_, L2_, L1_, zero = i64(D), i64(q), i64(L2n), i64(L1n), i64(0)
    first_bad, worst = None, np.inf
    for s in range(0, N, chunk):
        e = min(N, s + chunk)
        i = xp.arange(s, e, dtype=xp.int64)
        j, t = i // 3, i % 3
        aux = xp.where(t == 0, (4 * j) % n3, (2 * j + 1) % n3)
        lhs, ok = to_int64(xp, cx[s:e], b)
        if any_(~ok):
            return False, s + int(np.argmax(~npy(ok))), None, "entry of c is not a valid integer after scaling"
        g = lambda idx: to_int64(xp, take(cx, idx), b)[0]
        cbar = xp.minimum(xp.minimum(g(aux), g(aux + n3)), g(aux + 2 * n3))
        L = xp.where(t == 0, L2_, xp.where(t == 2, L1_, zero))
        lhs = lhs * D_
        diff = g((4 * i + 2) % N) * q_ + L * cbar - lhs
        if backend == "mlx":
            rel = (diff.astype(mx.float32) / lhs.astype(mx.float32)).min().item()
        else:
            rel = float((diff / lhs).min())
        worst = min(worst, rel)
        if first_bad is None and any_(diff < 0):
            first_bad = s + int(np.argmax(npy(diff) < 0))
    return first_bad is None, first_bad, worst, None if first_bad is None else "inequality violated"


def check_exact(c, b, D, q, L2n, L1n):
    """Same check with Python integers and Fractions (reference for the int64 code)."""
    N = c.size
    n3 = N // 3
    Cl = []
    for x in c:
        v = Fraction(float(x)) * 2 ** b
        if v.denominator != 1 or v < 1:
            return False, len(Cl)
        Cl.append(int(v))
    for i in range(N):
        j, t = divmod(i, 3)
        rhs = Cl[(4 * i + 2) % N] * q
        if t != 1:
            r = (4 * j) % n3 if t == 0 else (2 * j + 1) % n3
            rhs += (L2n if t == 0 else L1n) * min(Cl[r], Cl[r + n3], Cl[r + 2 * n3])
        if Cl[i] * D > rhs:
            return False, i
    return True, None


def certify(k, lam_str, c, backend="numpy", exact=False):
    """c: float32 vector (numpy array, memmap or mx.array).  With backend
    'both', pass c as numpy/memmap (the mlx check then copies it to the GPU)."""
    lam = Fraction(lam_str)
    if isinstance(c, np.ndarray):
        cmin, cmax = float(c.min()), float(c.max())
    else:
        cmin, cmax = c.min().item(), c.max().item()
    if not (np.isfinite(cmin) and np.isfinite(cmax) and cmin > 0):
        return False, {"reason": "c has non-positive or non-finite entries"}
    b, d = scale_bits(cmin, cmax)
    D, q, L2n, L1n = coefficients(lam, d)
    Cmax = int(Fraction(float(cmax)) * 2 ** b)
    assert Cmax * D < INT64_LIMIT and Cmax * (q + max(L2n, L1n)) < INT64_LIMIT, "int64 overflow possible"
    res = {"b": b, "d": d, "Cmax/Cmin": cmax / cmin, "coefficients": (D, q, L2n, L1n)}
    backends = ["numpy", "mlx"] if backend == "both" else [backend]
    if c.size > 2 ** 31 - 1 and "mlx" in backends:
        # MLX shapes are int32 and the mlx check uses flat take(); k >= 21 -> numpy only
        print("note: N > 2^31, mlx check skipped (numpy check + verify_cert.py)")
        backends = [be for be in backends if be != "mlx"] or ["numpy"]
    oks = []
    for be in backends:
        t = time.time()
        ok, bad, worst, why = check(c, b, D, q, L2n, L1n, backend=be)
        res[be] = (ok, bad, worst, time.time() - t)
        oks.append(ok)
        if why and not ok:
            res["reason"] = why
    if exact:
        t = time.time()
        ok, bad = check_exact(np.asarray(c), b, D, q, L2n, L1n)
        res["exact"] = (ok, bad, None, time.time() - t)
        oks.append(ok)
    assert len(set(oks)) == 1, f"backends disagree: {res}"
    return oks[0], res


def sha256_data(c):
    """sha256 of the raw little-endian float32 data of c (= c.npy minus its header)."""
    h = hashlib.sha256()
    for s in range(0, c.size, 2 ** 24):
        h.update(np.ascontiguousarray(c[s:s + 2 ** 24], dtype="<f4").tobytes())
    return h.hexdigest()


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(2 ** 24), b""):
            h.update(block)
    return h.hexdigest()


def write_cert_json(k, lam_str, res, outdir):
    """Write outdir/cert.json for outdir/c_f32.npy.  verify_cert.py checks them
    without using any code from this project."""
    import platform
    import datetime
    D, q, L2n, L1n = res["coefficients"]
    lam = Fraction(lam_str)
    cpath = os.path.join(outdir, "c_f32.npy")
    c = np.load(cpath, mmap_mode="r").reshape(-1)
    b = res["b"]
    verified = [be for be in ("numpy", "mlx", "exact") if be in res and res[be][0]]
    versions = {"python": platform.python_version(), "numpy": np.__version__, "mpmath": mpmath.__version__}
    try:
        import mlx.core as mx
        versions["mlx"] = mx.__version__
    except ImportError:
        pass
    cert = {
        "format": "krasikov-lagarias-LNT-certificate/2",
        "reference": "I. Krasikov, J. C. Lagarias, Bounds for the 3x+1 problem using difference "
                     "inequalities, Acta Arith. 109 (2003) 237-258, arXiv:math/0205002, Thm 2.2",
        "claim": f"L^NT_{k}(lambda) is feasible for lambda = {lam_str}, hence pi_a(x) >= x^gamma "
                 f"for every gamma < log2(lambda) and x >= x0(a, gamma)",
        "k": k,
        "N": int(c.size),
        "lambda": lam_str,
        "lambda_P": lam.numerator,
        "lambda_Q": lam.denominator,
        "log2_lambda": float(mpmath.log(mpmath.mpf(lam.numerator) / lam.denominator, 2)),
        "D": D,
        "q": q,
        "L2": L2n,
        "L1": L1n,
        "b": b,
        "check": "The integer vector is C[i] = c[i] * 2^b, c read from c_f32.npy (float32); every C[i] "
                 "must be an exact integer >= 1. Index i in [0, N) is the residue m = 3i+2 mod 3^k, "
                 "n3 = N/3. For every i, with j, t = divmod(i, 3), cbar(r) = min(C[r], C[r+n3], "
                 "C[r+2n3]): C[i]*D <= q*C[(4i+2) mod N] + L*cbar(r), where L = L2, r = 4j mod n3 "
                 "if t = 0; L = 0 if t = 1; L = L1, r = (2j+1) mod n3 if t = 2. Requires q/D <= "
                 "lambda^-2, L2/D <= lambda^(alpha-2), L1/D <= lambda^(alpha-1), alpha = log2(3).",
        "c_file": "c_f32.npy",
        "c_dtype": "<f4",
        "c_sha256_data": sha256_data(c),
        "c_file_sha256": sha256_file(cpath),
        "C_min": int(Fraction(float(c.min())) * 2 ** b),
        "C_max": int(Fraction(float(c.max())) * 2 ** b),
        "min_relative_slack": res[verified[0]][2] if verified else None,
        "verified_with": verified,
        "created": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "software": versions,
    }
    with open(os.path.join(outdir, "cert.json"), "w") as f:
        json.dump(cert, f, indent=1)
    return cert


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    opts = sys.argv[1:]
    backend = opts[opts.index("--backend") + 1] if "--backend" in opts else "numpy"
    if "--backend" in opts:
        args.remove(backend)
    k, lam_str = int(args[0]), args[1]
    save = "--save" in opts

    import mlx.core as mx
    import kl_mlx
    N = 3 ** (k - 1)
    box = [None]
    if len(args) > 2:
        c0 = mx.load(args[2])
        box = [mx.tile(c0, 3) if 3 * c0.size == N else c0]
        del c0
    grow, F, extra = kl_mlx.make_growth(k)
    t = time.time()
    lo, hi, c = grow(float(Fraction(lam_str)), F, N, c0=box, **extra)
    print(f"power iteration (float32, GPU{', int8 update' if extra else ''}): {time.time() - t:.1f}s  "
          f"lo={lo:.9f} hi={hi:.9f}")

    # write c once; all checks then stream from it (numpy: memmap, mlx: one GPU copy)
    outdir = f"certs/k{k}_{lam_str}" if save else tempfile.mkdtemp(prefix=f"kl_k{k}_", dir=".")
    os.makedirs(outdir, exist_ok=True)
    cpath = os.path.join(outdir, "c_f32.npy")
    mx.save(cpath, c)
    del c
    mx.clear_cache()

    c = mx.load(cpath) if backend == "mlx" else np.load(cpath, mmap_mode="r").reshape(-1)
    ok, res = certify(k, lam_str, c, backend=backend, exact="--exact" in opts)
    del c
    lam = Fraction(lam_str)
    g = float(mpmath.log(mpmath.mpf(lam.numerator) / lam.denominator, 2))
    if "b" in res:
        print(f"C = c * 2^{res['b']}, D = 2^{res['d']}, Cmax/Cmin = {res['Cmax/Cmin']:.3f}")
    for be in ("numpy", "mlx", "exact"):
        if be in res:
            okb, bad, worst, dt = res[be]
            extra = f" min rel. slack={worst:.3e}" if worst is not None else ""
            print(f"  {be:5s}: VERIFIED={okb}{'' if okb else f' (fails at index {bad})'}{extra}  {dt:.1f}s")
    if "reason" in res:
        print(f"  reason: {res['reason']}")
    print(f"k={k} lam_cert={lam_str} log2(lam)={g:.6f} VERIFIED={ok}")
    if save and ok:
        cert = write_cert_json(k, lam_str, res, outdir)
        print(f"saved {outdir}/  c sha256 (data) {cert['c_sha256_data']}")
    else:
        if save:
            print("not saved: certificate did not verify")
        shutil.rmtree(outdir)
