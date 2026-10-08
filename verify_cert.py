"""
Independent verifier for a Krasikov–Lagarias L^NT_k(lambda) certificate written
by certify_fast.py --save.  Needs only numpy and mpmath; uses no project code.

  python verify_cert.py certs/k19_1.8783 [--exact]

Two formats:
  /1  C.npy  int64 vector C
  /2  c_f32.npy  float32 vector c with C[i] = c[i] * 2^b, which must be an exact integer.
      Converted here as float64(c[i]) * 2^b (exact: float32 -> float64 is exact,
      multiplying by a power of two is exact below 2^1023) followed by an exact
      integrality and range check (< 2^53) before the cast to int64.  certify_fast.py
      uses bit operations instead, so the two conversions are independent.

Checks, all exactly (integers) or with rigorous interval arithmetic:
 1. the vector file has the right dtype, N = 3^(k-1) entries and matches both sha256 hashes.
 2. lambda = P/Q, and 0 <= q <= D lambda^-2, i.e. q P^2 <= D Q^2 (integers).
 3. 0 <= L2 <= D lambda^(alpha-2) and 0 <= L1 <= D lambda^(alpha-1), alpha = log2 3,
    via mpmath interval arithmetic (lower endpoint compared as an exact rational).
 4. min C >= 1, and max C * D < 2^63, max C * (q + max(L1, L2)) < 2^63, so the
    int64 check below cannot overflow.
 5. For every i in [0, N) (residue m = 3i + 2 mod 3^k), n3 = N/3, j, t = divmod(i, 3):
      C[i] D <= q C[(4i+2) mod N] + L cbar(r),  cbar(r) = min(C[r], C[r+n3], C[r+2n3]),
      t = 0 (m = 2 mod 9): L = L2, r = 4j mod n3
      t = 1 (m = 5 mod 9): L = 0
      t = 2 (m = 8 mod 9): L = L1, r = (2j+1) mod n3
    in int64 (and with Python integers if --exact).
Then C_m <= lam^-2 C_{4m} + lam^(alpha-j) cbar holds for all m, so C is feasible
for L^NT_k(lambda) and by Theorem 2.2 of the paper pi_a(x) >= x^gamma for
all gamma < log2(lambda), x >= x0(a, gamma).
"""
import hashlib
import json
import os
import sys
from fractions import Fraction

import numpy as np
import mpmath


def fail(msg):
    print(f"FAILED: {msg}")
    sys.exit(1)


def sha256_data(C, dtype):
    h = hashlib.sha256()
    for s in range(0, C.size, 2 ** 24):
        h.update(np.ascontiguousarray(C[s:s + 2 ** 24], dtype=dtype).tobytes())
    return h.hexdigest()


def integers(x, b):
    """Format /2: exact int64 C = x * 2^b for float32 x, or fail."""
    if b is None:
        return np.asarray(x)
    y = np.asarray(x, dtype=np.float64) * (2.0 ** b)
    if not (np.isfinite(y).all() and (y == np.floor(y)).all() and (y >= 1).all() and (y < 2.0 ** 53).all()):
        fail("c[i] * 2^b is not an integer in [1, 2^53) for some i")
    return y.astype(np.int64)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(2 ** 24), b""):
            h.update(block)
    return h.hexdigest()


def lower_endpoint(lam, shift):
    """Exact rational lower bound of lam^(log2(3) - shift), interval arithmetic."""
    iv = mpmath.iv
    iv.prec = 256
    x = iv.mpf(lam.numerator) / lam.denominator
    alpha = iv.log(iv.mpf(3)) / iv.log(iv.mpf(2))
    val = iv.exp((alpha - shift) * iv.log(x))
    man, ex = mpmath.mpf(val.a).man_exp
    return Fraction(int(man)) * Fraction(2) ** int(ex)


def main(certdir, exact=False):
    with open(os.path.join(certdir, "cert.json")) as f:
        cert = json.load(f)
    k, N = cert["k"], cert["N"]
    D, q, L2, L1 = cert["D"], cert["q"], cert["L2"], cert["L1"]
    P, Q = cert["lambda_P"], cert["lambda_Q"]
    lam = Fraction(P, Q)

    # 1. data
    if N != 3 ** (k - 1):
        fail("N != 3^(k-1)")
    fmt = cert["format"]
    if fmt == "krasikov-lagarias-LNT-certificate/1":
        name, dtype, key, b = cert["C_file"], "<i8", "C", None
    elif fmt == "krasikov-lagarias-LNT-certificate/2":
        name, dtype, key, b = cert["c_file"], "<f4", "c", cert["b"]
        if not isinstance(b, int) or not 0 <= b <= 60:
            fail("b out of range")
    else:
        fail(f"unknown format {fmt}")
    cpath = os.path.join(certdir, name)
    if sha256_file(cpath) != cert[f"{key}_file_sha256"]:
        fail(f"sha256 of {name} does not match")
    C = np.load(cpath, mmap_mode="r")
    if C.ndim == 2 and C.shape == (3, N // 3):     # k >= 21: stored as (3, N/3), same bytes
        C = C.reshape(-1)
    if C.dtype != np.dtype(dtype) or C.ndim != 1 or C.size != N:
        fail(f"{name} has dtype {C.dtype}, shape {C.shape}")
    if sha256_data(C, dtype) != cert[f"{key}_sha256_data"]:
        fail(f"sha256 of {name} data does not match")
    print(f"k={k} N={N}: {name} present, sha256 OK" + (f", C = c * 2^{b}" if b is not None else ""))

    # 2.-3. coefficients
    if Fraction(cert["lambda"]) != lam or not (1 < lam < 2):
        fail("lambda inconsistent with P/Q, or not in (1, 2)")
    if not (D > 0 and q >= 0 and L1 >= 0 and L2 >= 0):
        fail("negative coefficient")
    if q * P * P > D * Q * Q:
        fail("q/D > lambda^-2")
    if Fraction(L2, D) > lower_endpoint(lam, 2):
        fail("L2/D not proven <= lambda^(alpha-2)")
    if Fraction(L1, D) > lower_endpoint(lam, 1):
        fail("L1/D not proven <= lambda^(alpha-1)")
    print(f"lambda = {P}/{Q}: q/D <= lambda^-2, L2/D <= lambda^(alpha-2), L1/D <= lambda^(alpha-1) OK")

    # 4. range
    Cmin, Cmax = int(integers(C.min(keepdims=True), b)[0]), int(integers(C.max(keepdims=True), b)[0])
    if Cmin < 1:
        fail("min C < 1")
    if Cmax * D >= 2 ** 63 or Cmax * (q + max(L1, L2)) >= 2 ** 63:
        fail("int64 overflow possible")
    print(f"C in [{Cmin}, {Cmax}], no int64 overflow possible")

    # 5. inequalities
    n3 = N // 3
    worst = np.inf
    for s in range(0, N, 2 ** 22):
        e = min(N, s + 2 ** 22)
        i = np.arange(s, e, dtype=np.int64)
        j, t = i // 3, i % 3
        r = np.where(t == 0, (4 * j) % n3, (2 * j + 1) % n3)
        G = lambda idx: integers(C[idx], b)
        cbar = np.minimum(np.minimum(G(r), G(r + n3)), G(r + 2 * n3))
        L = np.where(t == 0, np.int64(L2), np.where(t == 2, np.int64(L1), np.int64(0)))
        lhs = integers(C[s:e], b) * np.int64(D)
        diff = G((4 * i + 2) % N) * np.int64(q) + L * cbar - lhs
        if (diff < 0).any():
            fail(f"inequality violated at index {s + int(np.argmax(diff < 0))}")
        worst = min(worst, float((diff / lhs).min()))
    print(f"all {N} inequalities hold (int64), min relative slack {worst:.3e}")

    if exact:
        Cl = [int(x) for x in integers(C[:], b)]
        for i in range(N):
            j, t = divmod(i, 3)
            rhs = Cl[(4 * i + 2) % N] * q
            if t != 1:
                r = (4 * j) % n3 if t == 0 else (2 * j + 1) % n3
                rhs += (L2 if t == 0 else L1) * min(Cl[r], Cl[r + n3], Cl[r + 2 * n3])
            if Cl[i] * D > rhs:
                fail(f"exact check: inequality violated at index {i}")
        print(f"all {N} inequalities hold (Python integers)")

    g = mpmath.log(mpmath.mpf(P) / Q, 2)
    print(f"VERIFIED: L^NT_{k}({cert['lambda']}) feasible; pi_a(x) >= x^gamma for all gamma < "
          f"log2(lambda) = {mpmath.nstr(g, 10)}")


if __name__ == "__main__":
    main(sys.argv[1], exact="--exact" in sys.argv[2:])
