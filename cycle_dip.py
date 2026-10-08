"""
Off-cycle predecessors dipping below the cycle minimum (generalising Hercher 2023, Lemma 9).

Let m be the minimum of a nontrivial cycle and X0 the verification bound (every n <= X0 reaches 1).
Every predecessor w of a cycle element that is NOT itself on the cycle must satisfy w > X0.  Any predecessor
w < m is certainly off the cycle.  So if the residue class of m forces a predecessor w ~ c*m of some cycle
element with c < 1, then m > X0 / c.  Hercher's Lemma 9 is the case c = 1/2 (minimum followed by k odd steps
and >= 2 even steps:  (m-1)/2 merges).

Finite computation: m = r + M*u with M = 2^a 3^b, u a large unknown.  Forward trajectory for a steps is
determined by r (parity), each element is an exact linear form A + B*u.  Backward from each element: 2z always,
(2z-1)/3 when z = 2 (mod 3) (needs 3 | B, available for depth <= b).  Residues whose forward trajectory dips
below m are not cycle minima and are skipped.  c_min(r) = min over found predecessors of B_w / M;
c* = max over admissible r of c_min(r) gives the universal bound  m > X0 / c*.

  python cycle_dip.py [a=8] [b=5] [D=5]
"""
import sys
from collections import Counter

a = int(sys.argv[1]) if len(sys.argv) > 1 else 8
b = int(sys.argv[2]) if len(sys.argv) > 2 else 5
D = int(sys.argv[3]) if len(sys.argv) > 3 else 5
M = 2 ** a * 3 ** b


def forward(r):
    """Cycle elements z_0..z_a as linear forms (A, B); None if the class cannot be a cycle minimum."""
    A, B = r, M
    out = [(A, B)]
    for t in range(a):
        if A % 2 == 0:
            A, B = A // 2, B // 2
        else:
            A, B = (3 * A + 1) // 2, 3 * B // 2
        if B < M or (B == M and A < r):          # z_t < m for large u: r is not a cycle minimum
            return None
        out.append((A, B))
    return out


def dips(forms):
    """Minimal coefficient ratio B_w/M over predecessors (depth <= D) of the given cycle elements."""
    best = M
    for A, B in forms:
        frontier = [(A, B)]
        for _ in range(D):
            nxt = []
            for A1, B1 in frontier:
                nxt.append((2 * A1, 2 * B1))
                if A1 % 3 == 2 and B1 % 3 == 0:
                    w = ((2 * A1 - 1) // 3, 2 * B1 // 3)
                    nxt.append(w)
                    if w[1] < best:
                        best = w[1]
            frontier = nxt
    return best / M


if __name__ == "__main__":
    hist = Counter()
    admissible = 0
    worst = (0.0, None)
    for r in range(1, M, 2):                      # m is odd
        if r % 3 == 0:                             # multiples of 3 are never on a cycle
            continue
        forms = forward(r)
        if forms is None:
            continue
        admissible += 1
        c = dips(forms)
        hist[round(c, 4)] += 1
        if c > worst[0]:
            worst = (c, r)
    print(f"a={a} b={b} D={D}: M={M}, admissible classes (odd, not 0 mod 3, trajectory stays >= m): {admissible}")
    print("distribution of c_min (ratio of the deepest off-cycle predecessor to m):")
    for c, cnt in sorted(hist.items()):
        print(f"  c_min = {c:8.4f}: {cnt:7d} classes  -> m > X0 / c = {1 / c:6.3f} X0")
    c_star, r_star = worst
    print(f"c* = max c_min = {c_star:.4f} at r = {r_star}  =>  universal bound m > {1 / c_star:.3f} X0  "
          f"(log2 gain {__import__('math').log2(1 / c_star):.3f} bits)")
