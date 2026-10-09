"""Avenue 19: where does equidistribution of the cycle numerators fail?  Reads cycle_numerators.json.
  python cycle_analysis.py [n ...]"""
import json
import sys

import numpy as np

J = json.load(open("cycle_numerators.json"))
ns = [int(x) for x in sys.argv[1:]] or [20, 24, 28, 32]
for n in ns:
    r = {int(k): v for k, v in J[str(n)].items()}
    print(f"n = {n}: zeros {sum(v['zeros'] for v in r.values())} (expected {sum(v['expected_zeros'] for v in r.values()):.2f}); "
          f"k_max = {max(r)} (theta n = {n * np.log(2) / np.log(3):.1f})")
    print("   k   k/n    m            binom        max_h|S_h|/binom   x sqrt(binom)   h of max")
    for k in sorted(r):
        v = r[k]; w = np.array(v["weyl"]); b = v["count"]
        print(f"  {k:2d}  {k / n:.2f}  {v['m']:12d}  {b:11d}    {w.max():.2e}         {w.max() * np.sqrt(b):8.1f}       {int(w.argmax()) + 1}")
