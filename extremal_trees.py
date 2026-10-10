#!/usr/bin/env python3
"""
Exact extremal leaf counts N^-(k), N^+(k) and minorizing/majorizing weight vectors w^-(k), w^+(k)
of the pruned 3x+1 trees T*_k(a) of Applegate & Lagarias, "Density bounds for the 3x+1 problem I.
Tree-search method", Math. Comp. 64 (1995) 411-426 (Tables 2.1, 2.2; Theorems 1.1, 1.2, 2.1).

The search itself is the C helper extremal_trees_core.c (branch and bound over the ternary digits of
a with exact table bounds; see its header and notes/extremal_trees.md).  This script compiles it,
runs it, validates it, and turns its output into the A-L quantities.

    python extremal_trees.py build
    python extremal_trees.py validate              # literal brute force, numpy brute force, tables,
                                                   # search with several M, unpruned enumeration,
                                                   # residue certificates, A-L k = 30 values
    python extremal_trees.py run LOG --M 18 --k0 19 --k1 60 [--sense min|max|both] [--tau]
                                   [--threads 8] [--j0 9]
    python extremal_trees.py lp RMIN RMAX [--json OUT]   # certified residue-class growth bounds
    python extremal_trees.py report LOG [LOG ...] [--lp LP.json] [--md OUT.md] [--json OUT]

The helper binary is compiled to $EXTREMAL_BIN (default: <tmpdir>/extremal_trees_core).

Residue-class bounds (lp): with Phi(v)(c) = v(2c) + [c = 2,8 mod 9] min_t v(lift_t(c)) on classes c
mod 3^r, an integer V > 0 with Q Phi(V) >= P V certifies N*_n(a) >= (Vmin/Vmax) (P/Q)^n for all a, n
(and the max version an upper bound); see the comment block above lp_structure and the notes.

Definitions (A-L section 2).  For a != 0 (mod 3) the tree T*_k(a) has root a, children 2n always and
(2n-1)/3 when n = 2, 8 (mod 9) (2.2); leaves are the nodes at depth k, weight = number of
(2n-1)/3 edges.  w_kj(a) = #leaves of weight j, N*_k(a) = sum_j w_kj(a).  N^-(k), N^+(k) = min, max
over a mod 3^(k+1); w^-(k), w^+(k) are defined by min/max of the tail sums sum_{j>=tau} w_kj(a)
(2.9)-(2.10).  g^(+-)(k) = N^(+-)(k)^(1/k), and Theorem 2.1 gives for every k and every a != 0 mod 3
    g^-(k) <= liminf N*_j(a)^(1/j) <= limsup N*_j(a)^(1/j) <= g^+(k).

Root classes.  For a = 1 (mod 3) the root does not branch and 2a runs over all classes = 2 (mod 3),
so every statistic of class 1 at depth k equals that of class 2 at depth k-1.  The helper therefore
optimises over a = 2 (mod 3) only; the class-1 value is the class-2 value one level down.
"""
import argparse
import json
import math
import os
import subprocess
import sys
import tempfile
import time
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "extremal_trees_core.c"
BIN = Path(os.environ.get("EXTREMAL_BIN", Path(tempfile.gettempdir()) / "extremal_trees_core"))

# Values printed in Applegate-Lagarias 1995 that survive in the available text (the tables
# themselves are missing from the preprint PDF): Theorem 1.1 uses the k = 30 entries of Tables
# 2.1/2.2, Theorem 1.2 the optimised Chernoff bound gamma*_30 of Table 3.1.
AL_K30 = {"g_minus": "1.302053", "g_plus": "1.358386", "gamma_star": "0.654717"}


# ----------------------------------------------------------------------------------------------
def build(quiet=False):
    cmd = ["clang", "-O3", "-march=native", "-Wall", "-o", str(BIN), str(SRC), "-lpthread"]
    if not BIN.exists() or BIN.stat().st_mtime < SRC.stat().st_mtime:
        subprocess.run(cmd, check=True)
        if not quiet:
            print("built", BIN)
    return BIN


def run_helper(args, log=None):
    build(quiet=True)
    cmd = [str(BIN)] + [str(a) for a in args]
    if log is None:
        out = subprocess.run(cmd, check=True, capture_output=True, text=True).stdout
        return out.splitlines()
    with open(log, "w") as fh:
        subprocess.run(cmd, check=True, stdout=fh)
    return Path(log).read_text().splitlines()


# ----------------------------------------------------------------------------------------------
WITNESS = {}     # (k, sense) -> (value, a): a class-2 residue a mod 3^(k+1) with N*_k(a) = value
VERIFIED = {}    # (k, sense) -> init: no a = 2 (mod 3) has N*_k(a) < init (min) / > init (max)


def parse(lines):
    """class-2 extrema: V[(k, tau, sense)] (sense 0 = min, 1 = max); also timings."""
    V, info = {}, {}
    for l in lines:
        p = l.split()
        if not p:
            continue
        if p[0] == "T":                     # T m tau' min1 min2 max1 max2  (tables, exact)
            m, tp = int(p[1]), int(p[2])
            V[(m, tp, 0)] = int(p[4])
            V[(m, tp, 1)] = int(p[6])
        elif p[0] == "R":                   # R k tau sense value secs nodes leaves (search)
            k, tau, s = int(p[1]), int(p[2]), int(p[3])
            V[(k, tau, s)] = int(p[4])
            info[(k, tau, s)] = (float(p[5]), int(p[6]), int(p[7]))
        elif p[0] == "W":                   # W k tau sense value a
            WITNESS[(int(p[1]), int(p[3]))] = (int(p[4]), int(p[5]))
        elif p[0] == "V":                   # V k tau sense value init secs nodes leaves
            k, tau, s, v, init = map(int, p[1:6])
            if tau == 0 and v == init:
                VERIFIED[(k, s)] = init
    return V, info


def merge_logs(paths):
    V, info = {}, {}
    for path in paths:
        v, i = parse(Path(path).read_text().splitlines())
        for key, val in v.items():
            if key in V and V[key] != val:
                raise SystemExit(f"inconsistent value for {key}: {V[key]} vs {val} ({path})")
            V[key] = val
        info.update(i)
    return V, info


def class_value(V, k, tau, s, c):
    """extremum over a = c (mod 3), a mod 3^(k+1), of #leaves of weight >= tau."""
    if tau > k:
        return 0
    if c == 1:
        if k == 0:
            return 1 if tau == 0 else 0
        return class_value(V, k - 1, tau, s, 2)
    return V[(k, tau, s)]


def extremum(V, k, tau, s):
    f = max if s else min
    c1 = class_value(V, k, tau, s, 1)
    if tau == 0 and (k, tau, s) not in V and VERIFIED.get((k, s)) == c1:
        return c1       # class 2 verified not to beat class 1 (last depth of a run)
    return f(c1, class_value(V, k, tau, s, 2))


def have(V, k, tau, s):
    try:
        extremum(V, k, tau, s)
        return True
    except KeyError:
        return False


def weight_vector(V, k, s):
    """w^-(k) (s=0) or w^+(k) (s=1) from the tail-sum extrema (2.9)-(2.10)."""
    S = [extremum(V, k, t, s) for t in range(k + 1)] + [0]
    return [S[i] - S[i + 1] for i in range(k + 1)]


# ----------------------------------------------------------------------------------------------
def gamma_star(w):
    """A-L (3.9): optimised Chernoff lower bound for the exponent from a minorizing vector w."""
    import numpy as np
    from scipy.optimize import minimize_scalar
    k = len(w) - 1
    N = sum(w)
    p = np.array(w, float) / N
    z = k * math.log(2) - np.arange(k + 1) * math.log(3)
    keep = p > 0
    p, z = p[keep], z[keep]
    EZ = float((p * z).sum())

    def logM(th):
        a = th * z
        m = a.max()
        return m + math.log(float((p * np.exp(a - m)).sum()))

    def legendre(beta):     # sup_theta (beta theta - log M(theta)); theta <= 0 for beta < E[Z]
        r = minimize_scalar(lambda th: -(beta * th - logM(th)), bounds=(-80, 0), method="bounded",
                            options={"xatol": 1e-13})
        return -r.fun

    def gam(beta):          # beta = k (log 2 - alpha log 3)
        return (math.log(N) - legendre(beta)) / beta

    r = minimize_scalar(lambda b: -gam(b), bounds=(1e-6, EZ - 1e-9), method="bounded",
                        options={"xatol": 1e-13})
    beta = r.x
    alpha = (math.log(2) - beta / k) / math.log(3)
    return -r.fun, alpha, EZ / k


def root_floor(n, k, digits=6):
    """largest d/10^digits with (d/10^digits)^k <= n (rigorous rounding down of n^(1/k))."""
    s = 10 ** digits
    d = int(n ** (1.0 / k) * s)
    while Fraction(d + 1, s) ** k <= n:
        d += 1
    while Fraction(d, s) ** k > n:
        d -= 1
    return Fraction(d, s)


def root_ceil(n, k, digits=6):
    s = 10 ** digits
    d = int(n ** (1.0 / k) * s) + 1
    while Fraction(d - 1, s) ** k >= n:
        d -= 1
    while Fraction(d, s) ** k < n:
        d += 1
    return Fraction(d, s)


def fmt(fr, digits=6):
    return f"{float(fr):.{digits}f}"


# ----------------------------------------------------------------------------------------------
def literal(kmax):
    """Independent brute force: build T*_k(a) from actual integers a < 3^(k+1)."""
    res = {}
    for k in range(1, kmax + 1):
        cmin = cmax = None
        for a in range(1, 3 ** (k + 1)):
            if a % 3 == 0:
                continue
            w = [0] * (k + 1)
            stack = [(a, 0, 0)]
            while stack:
                n, d, wt = stack.pop()
                if d == k:
                    w[wt] += 1
                    continue
                stack.append((2 * n, d + 1, wt))
                if n % 3 == 2:
                    c = (2 * n - 1) // 3
                    if c % 3:
                        stack.append((c, d + 1, wt + 1))
            cum = [sum(w[t:]) for t in range(k + 1)]
            if cmin is None:
                cmin, cmax = cum[:], cum[:]
            else:
                cmin = [min(x, y) for x, y in zip(cmin, cum)]
                cmax = [max(x, y) for x, y in zip(cmax, cum)]
        res[k] = (cmin, cmax)
    return res


def count_literal(a, k):
    """N*_k(a) from the definition, with actual integers (level by level)."""
    lvl = [a]
    for _ in range(k):
        nxt = []
        for n in lvl:
            nxt.append(2 * n)
            if n % 3 == 2:
                c = (2 * n - 1) // 3
                if c % 3:
                    nxt.append(c)
        lvl = nxt
    return len(lvl)


def count_merged(a, k):
    """N*_k(a) with nodes at depth d merged by residue mod 3^(k-d+1) (structure below depends on
    nothing else); exact, needs far less memory than count_literal for large k."""
    lvl = {a % 3 ** (k + 1): 1}
    for d in range(k):
        mod = 3 ** (k - d)          # modulus for depth d+1
        nxt = {}
        for n, c in lvl.items():
            e = (2 * n) % mod
            nxt[e] = nxt.get(e, 0) + c
            if n % 9 in (2, 8):
                o = ((2 * n - 1) // 3) % mod
                nxt[o] = nxt.get(o, 0) + c
        lvl = nxt
    return sum(lvl.values())


def numpy_bruteforce(kmax):
    """Second independent brute force (numpy, residues): f_m(n) = f_{m-1}(2n) + [n=2,8 mod 9]
    f_{m-1}((2n-1)/3) on n mod 3^(m+1), for every relative threshold; returns tail-sum extrema."""
    import numpy as np
    f = {0: np.ones(3, np.int64)}   # tau = 0
    fprev = {0: np.ones(3, np.int64)}
    res = {}
    for m in range(1, kmax + 1):
        P = 3 ** m
        n = np.arange(3 * P, dtype=np.int64)
        e = (2 * n) % P
        br = (n % 9 == 2) | (n % 9 == 8)
        o = ((2 * n - 1) // 3) % P
        f = {}
        for tp in range(m + 1):
            g0 = fprev.get(tp)
            g1 = fprev.get(max(tp - 1, 0))
            v = g0[e] if g0 is not None else np.zeros(3 * P, np.int64)
            if g1 is not None:
                v = v + np.where(br, g1[o], 0)
            f[tp] = v
        ok = n % 3 != 0
        res[m] = ([int(f[t][ok].min()) for t in range(m + 1)], [int(f[t][ok].max()) for t in range(m + 1)])
        fprev = f
    return res

# ----------------------------------------------------------------------------------------------
# Residue-class growth bounds (depth analogue of the Krasikov-Lagarias system).
#
# For r >= 2 and a class c mod 3^r (c != 0 mod 3) put phi_n(c) = min, psi_n(c) = max of N*_n(b) over
# b = c (mod 3^r).  From N*_{n+1}(b) = N*_n(2b) + [b = 2,8 mod 9] N*_n((2b-1)/3), and since
# (2b-1)/3 mod 3^r is one of the three lifts l_t(c) = (2c-1)/3 + 2t 3^(r-1) (t = 0, 1, 2):
#     phi_{n+1}(c) >= phi_n(2c) + [c = 2,8 mod 9] min_t phi_n(l_t(c))  =: Phi(phi_n)(c)
#     psi_{n+1}(c) <= psi_n(2c) + [c = 2,8 mod 9] max_t psi_n(l_t(c))  =: Psi(psi_n)(c).
# Phi, Psi are monotone and 1-homogeneous.  If V > 0 is an integer vector with Q Phi(V) >= P V, then
# by induction (phi_0 = 1 <= V/V_min ... ) phi_n >= (P/Q)^n V/V_max, so for EVERY a != 0 (mod 3) and
# EVERY n >= 0:  N*_n(a) >= (V_min/V_max) (P/Q)^n.  Likewise Q Psi(V) <= P' V gives
# N*_n(a) <= (V_max/V_min) (P'/Q)^n.  Both are checked below in exact integer arithmetic.
# ----------------------------------------------------------------------------------------------
def lp_structure(r):
    import numpy as np
    R = 3 ** r
    it = np.uint32 if R < 2 ** 32 else np.int64
    c = np.arange(R, dtype=np.int64)
    good = (c % 3) != 0
    e = ((2 * c) % R).astype(it)
    br = (c % 9 == 2) | (c % 9 == 8)
    cb = c[br]
    base = ((2 * cb - 1) // 3) % R
    lifts = [((base + 2 * t * 3 ** (r - 1)) % R).astype(it) for t in range(3)]
    del c, base
    return R, good, e, br, cb.astype(it), lifts


def lp_apply(v, st, sense):
    import numpy as np
    R, good, e, br, cb, lifts = st
    out = v[e].copy()
    a = v[lifts[0]]
    for l in lifts[1:]:
        (np.maximum if sense else np.minimum)(a, v[l], out=a)
    out[cb] += a
    return out


def lp_power(r, sense, st=None, tol=1e-12, maxit=20000, verbose=False):
    import numpy as np
    st = st or lp_structure(r)
    R, good = st[0], st[1]
    v = np.ones(R)
    lo = hi = None
    best = None
    for i in range(maxit):
        w = lp_apply(v, st, sense)
        rat = w[good] / v[good]
        lo, hi = float(rat.min()), float(rat.max())
        key = lo if sense == 0 else -hi
        if best is None or key > best[0]:
            best = (key, v.copy(), lo, hi)
        if hi - lo < tol:
            break
        w /= w[good].max()
        w[~good] = 1.0
        v = 0.5 * v + 0.5 * w
        if verbose and i % 100 == 0:
            print(f"   it {i}: [{lo:.10f}, {hi:.10f}]", flush=True)
    return best[1], best[2], best[3], i + 1, st


def lp_certify(v, st, sense, mu_float, Q=10 ** 7, scale_bits=34):
    """Exact check of Q*Phi(V) >= P*V (sense 0) or Q*Psi(V) <= P*V (sense 1) for integer V."""
    import numpy as np
    R, good, e, br, cb, lifts = st
    vg = v[good]
    V = np.zeros(R, np.int64)
    V[good] = np.maximum(np.rint(vg / vg.max() * 2.0 ** scale_bits), 1).astype(np.int64)
    V[~good] = 0
    Vmax, Vmin = int(V[good].max()), int(V[good].min())
    P = math.floor(mu_float * Q) - 1 if sense == 0 else math.ceil(mu_float * Q) + 1
    # overflow guard (Python integers): Q * (V(2c) + V(lift)) and P * V(c) must stay below 2^63
    assert Q * 2 * Vmax < 2 ** 63 and P * Vmax < 2 ** 63
    for _ in range(50):
        W = lp_apply(V, st, sense)          # int64, exact
        lhs = W[good] * Q
        rhs = V[good] * P
        ok = bool(np.all(lhs >= rhs)) if sense == 0 else bool(np.all(lhs <= rhs))
        if ok:
            return P, Q, Vmin, Vmax
        P += -1 if sense == 0 else 1
    raise RuntimeError("certificate failed")


def lp_check_pure(r, V, P, Q, sense):
    """Independent re-check of a certificate with Python integers (small r)."""
    R = 3 ** r
    for c in range(R):
        if c % 3 == 0:
            continue
        val = V[(2 * c) % R]
        if c % 9 in (2, 8):
            lifts = [V[((2 * (c + t * R) - 1) // 3) % R] for t in range(3)]
            val += max(lifts) if sense else min(lifts)
        if (Q * val < P * V[c]) if sense == 0 else (Q * val > P * V[c]):
            return False
    return True


def cmd_lp(args):
    out = []
    for r in range(args.rmin, args.rmax + 1):
        t0 = time.time()
        st = lp_structure(r) if args.engine == "numpy" else None
        row = {"r": r, "engine": args.engine}
        for sense, name in ((0, "lower"), (1, "upper")):
            if args.engine == "numpy":
                v, lo, hi, iters, _ = lp_power(r, sense, st, tol=args.tol)
                P, Q, Vmin, Vmax = lp_certify(v, st, sense, lo if sense == 0 else hi)
            else:   # C helper: float32 power iteration, exact 64/128-bit integer check
                L = [l.split() for l in run_helper(["lp", r, sense, args.threads]) if l.startswith("L ")][0]
                if L[10] != "CERTIFIED":
                    raise SystemExit(f"certificate failed for r = {r}, sense = {sense}")
                P, Q, Vmin, Vmax, iters = int(L[3]), int(L[4]), int(L[5]), int(L[6]), int(L[7])
                lo, hi = float(L[8]), float(L[9])
            row[name] = {"mu": f"{P}/{Q}", "mu_float": P / Q, "iters": iters, "bracket": [lo, hi],
                         "Vmin": Vmin, "Vmax": Vmax, "const": Vmin / Vmax if sense == 0 else Vmax / Vmin}
        row["secs"] = time.time() - t0
        out.append(row)
        lw, up = row["lower"], row["upper"]
        print(f"r = {r:2d}: for all a != 0 (mod 3), n >= 0:  {lw['const']:.4g} * ({lw['mu_float']:.7f})^n <= N*_n(a)"
              f" <= {up['const']:.4g} * ({up['mu_float']:.7f})^n   [{row['secs']:.0f} s]", flush=True)
    if args.json:
        Path(args.json).write_text(json.dumps(out, indent=1))
    return 0


def cmd_validate(args):
    t0 = time.time()
    report = []
    klit, knp, Mt = args.klit, args.knp, args.mtab
    print(f"literal brute force k <= {klit} ...", flush=True)
    lit = literal(klit)
    print(f"numpy residue brute force k <= {knp} ...", flush=True)
    npb = numpy_bruteforce(knp)
    for k in range(1, klit + 1):
        assert lit[k] == npb[k], ("literal vs numpy", k)
    report.append(f"literal == numpy for k <= {klit} (all thresholds)")
    print(f"C tables M = {Mt} with thresholds ...", flush=True)
    V, _ = parse(run_helper(["tables", Mt, 1]))
    for k in range(1, knp + 1):
        for t in range(k + 1):
            assert extremum(V, k, t, 0) == npb[k][0][t], ("tables vs numpy min", k, t)
            assert extremum(V, k, t, 1) == npb[k][1][t], ("tables vs numpy max", k, t)
    report.append(f"C tables == numpy brute force for k <= {knp} (all thresholds, min and max)")
    sums = [l.split() for l in run_helper(["tables", 12, 0]) if l.startswith("S ")]
    for _, m, s in sums:
        assert int(s) == 2 * 4 ** int(m), ("sum check", m)
    report.append("sum over a of N*_m(a) = 2*4^m (A-L (2.8)) for m <= 12")
    # search with small table depth against the tables (all thresholds)
    for Ms in (4, 7):
        Vs, _ = parse(run_helper(["search", Ms, 1, Ms + 1, Mt, 4, 4, 1, 2]))
        for k in range(Ms + 1, Mt + 1):
            for t in range(k + 1):
                for s in (0, 1):
                    assert Vs[(k, t, s)] == V[(k, t, s)], ("search vs tables", Ms, k, t, s)
        report.append(f"search with M = {Ms} == tables for {Ms + 1} <= k <= {Mt} (all tau, min and max)")
    # search with different M agree on larger k (leaf counts)
    kc = args.kcross
    runs = {}
    for Ms in (10, 14):
        runs[Ms], _ = parse(run_helper(["search", Ms, 0, Ms + 1, kc, 8, 8, 0, 2]))
    for k in range(15, kc + 1):
        for s in (0, 1):
            assert runs[10][(k, 0, s)] == runs[14][(k, 0, s)], ("M=10 vs M=14", k, s)
    report.append(f"search M = 10 and M = 14 agree for 15 <= k <= {kc} (N^- and N^+)")
    # thresholds to k = 30 for the A-L comparison
    Vt, _ = parse(run_helper(["search", 12, 1, 13, 30, 8, 6, 1, 2]))
    for k in range(13, Mt + 1):
        for t in range(k + 1):
            for s in (0, 1):
                assert Vt[(k, t, s)] == V[(k, t, s)], ("search M=12 vs tables", k, t, s)
    report.append(f"search with M = 12 (all thresholds) == tables for 13 <= k <= {Mt}")
    Nm, Np = extremum(Vt, 30, 0, 0), extremum(Vt, 30, 0, 1)
    gm, gp = Nm ** (1 / 30), Np ** (1 / 30)
    gs = gamma_star(weight_vector(Vt, 30, 0))[0]
    ok = (f"{gm:.6f}" == AL_K30["g_minus"] and f"{gp:.6f}" == AL_K30["g_plus"]
          and f"{gs:.6f}" == AL_K30["gamma_star"])
    report.append(f"k = 30: N^- = {Nm}, N^+ = {Np}, g^- = {gm:.7f}, g^+ = {gp:.7f}, "
                  f"gamma*_30 = {gs:.7f}; A-L print {AL_K30['g_minus']}, {AL_K30['g_plus']}, "
                  f"{AL_K30['gamma_star']}: {'MATCH' if ok else 'MISMATCH'}")
    # unpruned enumeration (no bounds): sum identity and extremes agree with the branch and bound
    for k in range(15, args.kenum + 1):
        E = {}
        for l in run_helper(["enum", 12, 0, k]):
            p_ = l.split()
            if p_ and p_[0] == "E":
                E[int(p_[2])] = (int(p_[4]), int(p_[5]), int(p_[6]), int(p_[7]))
        tot = E[1][2] + E[2][2]
        assert tot == 2 * 4 ** k and E[1][3] == E[2][3] == 3 ** k, ("enum sum", k)
        for c in (1, 2):
            assert E[c][0] == class_value(runs[14], k, 0, 0, c), ("enum min", k, c)
            assert E[c][1] == class_value(runs[14], k, 0, 1, c), ("enum max", k, c)
    report.append(f"unpruned enumeration k = 15..{args.kenum}: sum of N*_k(a) over all a = 2*4^k, "
                  "class extremes equal the branch-and-bound values")
    # residue-class certificates: numpy certificate re-checked with Python integers, negative test
    for r in range(2, 8):
        st = lp_structure(r)
        for sense in (0, 1):
            v, lo, hi, _, _ = lp_power(r, sense, st)
            P, Q, Vmin, Vmax = lp_certify(v, st, sense, lo if sense == 0 else hi)
            import numpy as np
            Vg = np.zeros(3 ** r, np.int64)
            good = st[1]
            Vg[good] = np.maximum(np.rint(v[good] / v[good].max() * 2.0 ** 34), 1).astype(np.int64)
            Vl = [int(x) for x in Vg]
            assert lp_check_pure(r, Vl, P, Q, sense), ("pure check", r, sense)
            bad = P + 2000 if sense == 0 else P - 2000     # 2e-4 beyond the eigenvalue must fail
            assert not lp_check_pure(r, Vl, bad, Q, sense), ("negative test", r, sense)
            # consistency with the exact extremal counts of the k <= 40 search above
            const = Vmin / Vmax if sense == 0 else Vmax / Vmin
            for k in range(1, 41):
                N = extremum(runs[14] if k > 14 else V, k, 0, sense)
                bound = const * (P / Q) ** k
                assert (N >= bound * (1 - 1e-12)) if sense == 0 else (N <= bound * (1 + 1e-12)), ("lp vs N", r, sense, k)
    report.append("residue-class certificates r = 2..7: integer check re-done with Python ints, "
                  "mu +- 2e-4 rejected, bounds consistent with N^-(k), N^+(k) for k <= 40")
    for r in report:
        print("  " + r)
    print(f"validate: {'PASS' if ok else 'FAIL'} ({time.time() - t0:.0f} s)")
    return 0 if ok else 1


def cmd_run(args):
    sense = {"min": 0, "max": 1, "both": 2}[args.sense]
    taumode = 1 if args.tau else 0
    hargs = ["search", args.M, taumode, args.k0, args.k1, args.threads, args.j0, taumode, sense]
    build(quiet=True)
    with open(args.log, "w") as fh:
        p = subprocess.Popen([str(BIN)] + [str(a) for a in hargs], stdout=fh)
        p.wait()
    return p.returncode


def cmd_report(args):
    V, info = merge_logs(args.logs)
    rows = []
    kmax = max([k for (k, t, s) in V] + [k for (k, s) in VERIFIED])
    best_lo, best_hi = None, None
    for k in range(1, kmax + 1):
        row = {"k": k}
        for s, name in ((0, "minus"), (1, "plus")):
            if have(V, k, 0, s):
                N = extremum(V, k, 0, s)
                row["N_" + name] = N
                row["g_" + name] = N ** (1.0 / k)
                key = (k, 0, s)
                if key in info:
                    row["secs_" + name], row["nodes_" + name] = info[key][0], info[key][1]
        if "N_minus" in row:
            row["ratio_minus"] = (4 / 3) ** k / row["N_minus"]
            lo = root_floor(row["N_minus"], k)
            if best_lo is None or lo > best_lo[0]:
                best_lo = (lo, k)
        if "N_plus" in row:
            row["ratio_plus"] = row["N_plus"] / (4 / 3) ** k
            hi = root_ceil(row["N_plus"], k)
            if best_hi is None or hi < best_hi[0]:
                best_hi = (hi, k)
        if all(have(V, k, t, 0) for t in range(k + 1)):
            w = weight_vector(V, k, 0)
            row["w_minus"] = w
            if k >= 4:          # for k <= 3 w^- = (1, 0, ...) is degenerate
                g, a, ez = gamma_star(w)
                row["gamma_star"], row["alpha_star"], row["EZ_minus"] = g, a, ez
        if all(have(V, k, t, 1) for t in range(k + 1)):
            row["w_plus"] = weight_vector(V, k, 1)
        rows.append(row)
    print(" k        N^-(k)     g^-(k)    (4/3)^k/N^-        N^+(k)     g^+(k)    N^+/(4/3)^k   gamma*_k")
    for r in rows:
        def g(key, f):
            return f.format(r[key]) if key in r else " " * len(f.format(0.0 if 'f' in f else 0))
        print(f"{r['k']:2d} {g('N_minus', '{:13d}')} {g('g_minus', '{:10.6f}')} {g('ratio_minus', '{:12.4f}')}"
              f"   {g('N_plus', '{:13d}')} {g('g_plus', '{:10.6f}')} {g('ratio_plus', '{:12.4f}')}"
              f"   {g('gamma_star', '{:9.6f}')}")
    if best_lo and best_hi:
        print(f"\nTheorem 2.1 / 1.1 constants: liminf n_k(a)^(1/k) >= {fmt(best_lo[0])} (k = {best_lo[1]}),"
              f" limsup <= {fmt(best_hi[0])} (k = {best_hi[1]});  A-L 1995: 1.302053, 1.358386 (k = 30)")
    if args.lp:
        lp = json.loads(Path(args.lp).read_text())
        print("\nresidue-class bounds vs exact extremal counts (must hold for every k):")
        for row in lp:
            lw, up = row["lower"], row["upper"]
            Pl, Ql = map(int, lw["mu"].split("/"))
            Pu, Qu = map(int, up["mu"].split("/"))
            ok = True
            for r_ in rows:
                k = r_["k"]
                if "N_minus" in r_ and Fraction(lw["Vmin"], lw["Vmax"]) * Fraction(Pl, Ql) ** k > r_["N_minus"]:
                    ok = False
                if "N_plus" in r_ and Fraction(up["Vmax"], up["Vmin"]) * Fraction(Pu, Qu) ** k < r_["N_plus"]:
                    ok = False
            print(f"  r = {row['r']:2d}: {lw['const']:.4f} ({lw['mu_float']:.7f})^k <= N^-(k), "
                  f"N^+(k) <= {up['const']:.4f} ({up['mu_float']:.7f})^k : {'consistent' if ok else 'VIOLATED'}")
    if WITNESS:
        print("\nwitnesses (class a = 2 mod 3 attaining the class extremum), recounted from the definition:")
        bad = 0
        for (k, sn), (val, a) in sorted(WITNESS.items()):
            if k > args.witness_kmax:
                continue
            cnt = count_literal(a, k) if val <= 2_000_000 else count_merged(a, k)
            ok = cnt == val
            bad += not ok
            print(f"  k = {k:2d} {'max' if sn else 'min'}: a = {a}  N*_k(a) = {cnt}  {'ok' if ok else 'MISMATCH'}")
        print(f"  {'all witnesses ok' if not bad else str(bad) + ' MISMATCHES'}")
    if args.md:
        lines = ["| k | N^-(k) | g^-(k) | (4/3)^k/N^- | N^+(k) | g^+(k) | N^+/(4/3)^k | gamma*_k | s (min/max) |",
                 "|---|---|---|---|---|---|---|---|---|"]
        for r in rows:
            if r["k"] < args.md_kmin:
                continue
            def g(key, f):
                return f.format(r[key]) if key in r else "–"
            t = ""
            if "secs_minus" in r or "secs_plus" in r:
                t = f"{g('secs_minus', '{:.1f}')} / {g('secs_plus', '{:.1f}')}"
            lines.append(f"| {r['k']} | {g('N_minus', '{:d}')} | {g('g_minus', '{:.6f}')} | {g('ratio_minus', '{:.4f}')} | "
                         f"{g('N_plus', '{:d}')} | {g('g_plus', '{:.6f}')} | {g('ratio_plus', '{:.4f}')} | "
                         f"{g('gamma_star', '{:.6f}')} | {t} |")
        lines.append("")
        for r in rows:
            if "w_minus" in r and "w_plus" in r and r["k"] >= args.md_kmin:
                lines.append(f"k = {r['k']}: w^- = {r['w_minus']}")
                lines.append(f"k = {r['k']}: w^+ = {r['w_plus']}")
        Path(args.md).write_text("\n".join(lines) + "\n")
        print("wrote", args.md)
    if args.json:
        out = {"rows": rows,
               "witnesses": {f"{k},{sn}": [v, str(a)] for (k, sn), (v, a) in WITNESS.items()},
               "verified": {f"{k},{sn}": v for (k, sn), v in VERIFIED.items()},
               "best_lower": {"value": str(best_lo[0]), "k": best_lo[1]} if best_lo else None,
               "best_upper": {"value": str(best_hi[0]), "k": best_hi[1]} if best_hi else None,
               "logs": [str(p) for p in args.logs]}
        Path(args.json).write_text(json.dumps(out, indent=1))
        print("wrote", args.json)
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("build")
    v = sub.add_parser("validate")
    v.add_argument("--klit", type=int, default=10)
    v.add_argument("--knp", type=int, default=13)
    v.add_argument("--mtab", type=int, default=14)
    v.add_argument("--kcross", type=int, default=40)
    v.add_argument("--kenum", type=int, default=21)
    r = sub.add_parser("run")
    r.add_argument("log")
    r.add_argument("--M", type=int, default=18)
    r.add_argument("--k0", type=int, default=None)
    r.add_argument("--k1", type=int, default=50)
    r.add_argument("--sense", default="both", choices=["min", "max", "both"])
    r.add_argument("--tau", action="store_true", help="all thresholds (w^+-), needs TMAX tables")
    r.add_argument("--threads", type=int, default=8)
    r.add_argument("--j0", type=int, default=9)
    q = sub.add_parser("lp", help="certified residue-class growth bounds (depth K-L system)")
    q.add_argument("rmin", type=int)
    q.add_argument("rmax", type=int)
    q.add_argument("--tol", type=float, default=1e-12)
    q.add_argument("--engine", choices=["numpy", "c"], default="numpy",
                   help="c: compiled helper (float32 search, exact integer check), for r >= 16")
    q.add_argument("--threads", type=int, default=4)
    q.add_argument("--json")
    p = sub.add_parser("report")
    p.add_argument("logs", nargs="+")
    p.add_argument("--json")
    p.add_argument("--witness-kmax", type=int, default=60)
    p.add_argument("--md", help="write markdown tables to this file")
    p.add_argument("--lp", help="JSON from the lp command: check its bounds against the extremal counts")
    p.add_argument("--md-kmin", type=int, default=1)
    a = ap.parse_args()
    if a.cmd == "build":
        build()
        return 0
    if a.cmd == "validate":
        return cmd_validate(a)
    if a.cmd == "run":
        if a.k0 is None:
            a.k0 = a.M + 1
        return cmd_run(a)
    if a.cmd == "report":
        return cmd_report(a)
    if a.cmd == "lp":
        return cmd_lp(a)


if __name__ == "__main__":
    sys.exit(main())
