# What a proof of the Collatz conjecture cannot look like: no-go theorems (avenue 21)

Daniel Palmqvist, with Claude; October 2026. Folklore results collected with proofs, to delimit where a proof can live.

Throughout, T(n) = n/2 for even n and (3n+1)/2 for odd n, and a *potential* is a function V on the positive integers
with V(T(n)) < V(n) for every n ≥ 2 (a strict Lyapunov function). Such a V with values in a well-ordered set would prove
the conjecture, since every orbit would then reach the only fixed point of the ordering. The theorems below say that
V cannot be built from finitely many residue conditions, nor from bounded lookahead, nor from any quantity that is
monotone in n within residue classes. They are all consequences of one fact.

**Lemma (Terras, 1976).** For every L ≥ 1 and every residue class r mod 2^L there is exactly one parity pattern
(T^j(n) mod 2)_{j<L} shared by all n ≡ r (mod 2^L), and the map r ↦ pattern is a bijection of ℤ/2^L onto {0,1}^L.
In particular n ≡ −1 (mod 2^L) iff the first L iterates of n are all odd, and then T^j(n) = (3^j(n+1) − 2^j)/2^j,
so T^j(n) ≡ −1 (mod 2^{L−j}) and T^j(n) > (3/2)^j n − 1 for j ≤ L.

*Proof.* T(n) mod 2^{L−1} is determined by n mod 2^L in both branches (n/2 and (3n+1)/2 are affine with an
invertible factor on the appropriate residues), and the two branches send the two lifts of a residue mod 2^{L−1} to
distinct parities; induction on L. ∎

## Theorem 1 (no residue-class potential)

Let M ≥ 1 and V: ℤ/Mℤ → ℝ be arbitrary. Then the set of n ≥ 1 with V(T(n) mod M) ≥ V(n mod M) has positive lower
density (at least 2^{−L} for an explicit L = L(M)). In particular no function of n mod M is a potential, even if
exceptions of density zero are allowed.

*Proof.* Write M = 2^a m with m odd. On ℤ/mℤ the odd step n ↦ (3n+1)/2 is the affine bijection π(r) = (3r+1)·2^{−1};
let p be the order of π as a permutation of ℤ/mℤ, so π^p = id. Put L = a + p and take any n ≡ −1 (mod 2^L). By the
lemma the first L steps are odd, and for j ≤ p the iterate n_j = T^j(n) satisfies n_j ≡ −1 (mod 2^a) and
n_j ≡ π^j(n mod m) (mod m). Hence n_p ≡ n (mod M) by the Chinese remainder theorem, so V(n_p mod M) = V(n mod M), and
V cannot have decreased strictly at each of the p steps from n to n_p: at least one of n, n_1, …, n_{p−1} violates
the inequality. These n form the residue class −1 mod 2^L, of density 2^{−L}, and each violation is attributed to one
of at most p iterates of such an n, so the violating set has lower density at least 2^{−L}/p·(something positive);
more simply, the violating iterates themselves lie in the classes −1 mod 2^{L−j}, j < p, each of positive density. ∎

## Theorem 2 (no bounded lookahead)

Let M, L ≥ 1 and let V be a function of (n mod M, the parity vector of the next L steps). Then V is not a potential,
and the violating set has positive lower density.

*Proof.* By the lemma the next L parities are a function of n mod 2^L, so V is a function of n mod 2^L M, and
Theorem 1 applies with modulus 2^L M. ∎

So "look ahead L steps" buys nothing for any fixed L: the all-odd runs of Theorem 1 are exactly the inputs on which a
lookahead potential must gamble, and they recur in every residue class.

## Theorem 3 (no potential monotone in n within residue classes)

Let M ≥ 1 and let V(n) = Ψ(n, n mod M) where for each residue r the function n ↦ Ψ(n, r) is nondecreasing on
{n : n ≡ r (mod M)}. Then V is not a potential, and the violating set has positive lower density.

*Proof.* Take L, p as in Theorem 1 and n ≡ −1 (mod 2^L) with n large. Then n_p ≡ n (mod M) and n_p > (3/2)^p n − 1 > n,
so V(n_p) = Ψ(n_p, r) ≥ Ψ(n, r) = V(n): V did not decrease over the p steps. ∎

This covers every potential of the forms n^s g(n mod M), log n + g(n mod M), f(n)·g(n mod M) with f nondecreasing,
and the "bounded multiplicative potentials" of the kind whose non-existence has been claimed in recent repositories.
It also covers potentials depending on n mod M and on finitely many bits of lookahead by Theorem 2. The only
potentials not excluded are those that are *not* monotone in n inside a residue class — for instance the total
stopping time itself, which is a potential exactly when the conjecture holds.

## Theorem 4 (no uniform method; Conway 1972, Kurtz–Simon 2007)

For generalised Collatz maps g(n) = a_i n + b_i on n ≡ i (mod d), with rational a_i, b_i, the question "does every
orbit reach 1" is undecidable (Conway for the halting form, Kurtz–Simon for the ∀-form, Π⁰₂-complete). Hence no
proof can proceed from properties shared by all maps of this shape: the arithmetic of the specific pair (2, 3)
must enter.

## Theorem 5 (matrix interpretations prove only weakenings; Yolcu–Aaronson–Heule 2023)

The conjecture is equivalent to termination of an explicit string rewriting system; matrix and arctic
interpretations found by SAT prove termination of weakened variants only, and the authors argue that the full
system has no interpretation of these linear shapes because such interpretations are bounded-lookahead certificates
in disguise. Together with Theorem 2 this says: a termination certificate must carry unbounded residue information.

## What survives

Any proof must use (i) the specific pair (2, 3) (Theorem 4) and (ii) information not determined by n modulo any
fixed M (Theorems 1–3), i.e. the whole 2-adic expansion of n (avenue 18: the parity map Q and the series Φ), or
the whole predecessor tree (avenues 1, 17), or a potential that is non-monotone in n within residue classes. The
one mechanical route left open is termination with *unbounded* residue labelling (avenue 21(ii)), which escapes
Theorem 2 only if the labelling is not eventually periodic in n.
