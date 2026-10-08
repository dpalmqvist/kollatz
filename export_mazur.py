"""
Export one of our certificates to Lech Mazur's `kl-predecessor-certificate-v1` format (ProofAtlas,
collatz_predecessor_090), so that it can be checked by his Lean development (native_decide) and his
independent Python/C++ verifiers.

His format: weights.u32le = C_i as unsigned 32-bit little-endian, minimum weight 2^weight_scale_bits,
lambda = 2^(gamma_num/gamma_den), dyadic lower bounds for lambda^-2, lambda^(alpha-2), lambda^(alpha-1) with
denominator 2^coefficient_scale_bits computed by exact integer root extraction (his kl_predecessor_common.py).
Row check: scale * C_i <= a * C_{4i} + b_j * min(lifts)   -- identical to ours.

  python export_mazur.py certs/k18_1.8703 903 1000 OUTDIR [--weight-bits 20] [--scripts DIR]
"""
import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("cert_dir")
ap.add_argument("gamma_num", type=int)
ap.add_argument("gamma_den", type=int)
ap.add_argument("out_dir")
ap.add_argument("--weight-bits", type=int, default=20)
ap.add_argument("--coefficient-bits", type=int, default=28)
ap.add_argument("--scripts", required=True, help="Mazur's scripts/ directory (for kl_predecessor_common)")
args = ap.parse_args()
sys.path.insert(0, args.scripts)
from kl_predecessor_common import KLParameters, coefficient_power_checks, exact_lower_coefficients  # noqa: E402

cert = json.load(open(Path(args.cert_dir) / "cert.json"))
k = int(cert["k"])
N = 3 ** (k - 1)
params = KLParameters(k=k, gamma_num=args.gamma_num, gamma_den=args.gamma_den,
                      coefficient_scale_bits=args.coefficient_bits, weight_scale_bits=args.weight_bits)
coef = exact_lower_coefficients(params)
checks = coefficient_power_checks(params, coef)
assert all(checks.values()), checks
lam = 2 ** (args.gamma_num / args.gamma_den)
print(f"k={k} gamma={args.gamma_num}/{args.gamma_den} lambda={lam:.7f} (our lambda_cert {cert['lambda']}, "
      f"numerical lambda_k from CLAUDE.md should exceed this)")
print("coefficients:", coef)

# load our vector as exact integers, rescale so that min = 2^weight_bits (rounding down)
d = Path(args.cert_dir)
if (d / "C.npy").exists():
    C = np.load(d / "C.npy", mmap_mode="r")
    cmin = int(cert["C_min"])
    shift = cmin.bit_length() - 1 - args.weight_bits
    assert cmin == 1 << (cmin.bit_length() - 1), "C_min is not a power of two"
    if shift >= 0:
        W = (np.asarray(C) >> shift).astype(np.int64)
    else:
        W = (np.asarray(C) << (-shift)).astype(np.int64)
else:                                   # format /2: float32 c with min c in [1, 2) after normalisation
    c = np.load(d / "c_f32.npy", mmap_mode="r").reshape(-1)
    cmin = float(np.min(c))
    W = np.floor(np.asarray(c, dtype=np.float64) / cmin * (1 << args.weight_bits)).astype(np.int64)
wmin, wmax = int(W.min()), int(W.max())
print(f"weights: min={wmin} (2^{args.weight_bits}={1 << args.weight_bits}) max={wmax} < 2^32: {wmax < 2 ** 32}")
assert wmin == 1 << args.weight_bits and 0 < wmin and wmax < 2 ** 32

# quick numpy row check, chunked (the independent checks are Mazur's verifiers and Lean)
n3 = N // 3
lift = np.minimum(np.minimum(W[:n3], W[n3:2 * n3]), W[2 * n3:])
CH = 1 << 24
min_margin, worst, failed = None, -1, 0
min_rel = np.inf
for s0 in range(0, N, CH):
    i = np.arange(s0, min(s0 + CH, N), dtype=np.int64)
    rhs = coef.lambda_neg2_lower * W[(4 * i + 2) % N]
    j = i // 3
    t = i % 3
    m0, m2 = t == 0, t == 2
    rhs[m0] += coef.lambda_alpha_minus2_lower * lift[(4 * j[m0]) % n3]
    rhs[m2] += coef.lambda_alpha_minus1_lower * lift[(2 * j[m2] + 1) % n3]
    margin = rhs - coef.scale * W[i]
    failed += int((margin < 0).sum())
    a = int(margin.argmin())
    if min_margin is None or int(margin[a]) < min_margin:
        min_margin, worst = int(margin[a]), int(i[a])
    min_rel = min(min_rel, float((margin / (coef.scale * W[i])).min()))
print(f"numpy row check: failed={failed} min_margin={min_margin} min relative slack={min_rel:.3e}")
assert failed == 0

out = Path(args.out_dir)
out.mkdir(parents=True, exist_ok=True)
wpath = out / "weights.u32le"
W.astype("<u4").tofile(wpath)
sha = hashlib.sha256(wpath.read_bytes()).hexdigest()
manifest = {
    "schema": "kl-predecessor-certificate-v1",
    "artifact_status": "CANDIDATE_DATA_ONLY_UNTIL_INDEPENDENTLY_VERIFIED",
    "algorithm": "float32-power-iteration-mlx (Palmqvist), rescaled to integers",
    "parameters": {"k": k, "gamma_num": args.gamma_num, "gamma_den": args.gamma_den,
                   "coefficient_scale_bits": args.coefficient_bits, "weight_scale_bits": args.weight_bits},
    "dimensions": {"modulus": 3 ** k, "principal_count": N, "auxiliary_count": n3},
    "coefficients": {"scale": coef.scale, "lambda_neg2_lower": coef.lambda_neg2_lower,
                     "lambda_alpha_minus2_lower": coef.lambda_alpha_minus2_lower,
                     "lambda_alpha_minus1_lower": coef.lambda_alpha_minus1_lower, "power_checks": checks},
    "weights": {"file": wpath.name, "encoding": "unsigned-32-bit-little-endian", "count": N,
                "bytes": wpath.stat().st_size, "minimum": wmin, "maximum": wmax, "sha256": sha},
    "generator_row_check": {"failed_rows": 0, "minimum_margin": min_margin,
                            "worst_index": worst, "worst_residue": 3 * worst + 2},
    "source": {"our_certificate": str(d), "our_cert_json": cert,
               "note": "weights = our integer vector C rescaled (floor) so that min = 2^weight_scale_bits"},
    "proof_status": "Exact finite rows self-checked; independent verification required.",
}
(out / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
print(f"wrote {wpath} ({wpath.stat().st_size} bytes, sha256 {sha}) and manifest.json")
