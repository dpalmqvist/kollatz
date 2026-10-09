"""
Avenue 17: certify a bounded-spread feasible point (from spread_iter.py --slack=...) exactly as the Perron
certificates: integer check with rounded-down coefficients (certify_fast.certify), cert.json + c_f32.npy in
certs/spread_k{k}_{lam}/, then the independent verify_cert.py.  The certificate proves: L^NT_k(lam) is feasible
with 1 <= c <= t, hence by Krasikov-Lagarias Thm 2.2 pi_a(x) >= (x/a)^{log2 lam} / (4 t) for all x >= a and every
a not in a cycle, a != 0 mod 3.

  python certify_spread.py K LAM VECTOR.npy
"""
import os
import subprocess
import sys

import numpy as np

import certify_fast as cf

k, lam_str, path = int(sys.argv[1]), sys.argv[2], sys.argv[3]
c = np.load(path).astype(np.float32)
t = float(c.max() / c.min())
ok, res = cf.certify(k, lam_str, c, backend="numpy", exact=(k <= 12))
print(f"k={k} lam={lam_str} spread={t:.4f} VERIFIED={ok} slack={res['numpy'][2]:.2e}")
if ok:
    outdir = f"certs/spread_k{k}_{lam_str}"
    os.makedirs(outdir, exist_ok=True)
    np.save(os.path.join(outdir, "c_f32.npy"), c)
    cf.write_cert_json(k, lam_str, res, outdir)
    print(subprocess.run([sys.executable, "verify_cert.py", outdir], capture_output=True, text=True).stdout.strip().splitlines()[-1])
    print(f"=> pi_a(x) >= (x/a)^{np.log2(float(lam_str)):.4f} / {4 * t:.2f} for all x >= a")
