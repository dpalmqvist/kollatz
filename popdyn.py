"""
Avenue 1: population dynamics (typed cavity approximation) for the random K-L model  (2026-10-09).

Object: the sibling triple Xi_{k+1}(w) = (c_{k+1}(w + t*3^(k-1)))_t below a level-k node w.  Exact equation:
    Xi(w) = lam^-2 P_sigma Xi(nxt_k w) + L_cls(w) P_pi (cbar_{k+1}(w_s))_s,   w_s = children of v = aux_k(w),
    cbar_{k+1}(w_s) = min Xi(w_s).
Types: residue mod 3^(B-1) (level-B class), B = last exact level (= K0-1 of meanfield.py); nxt acts on types exactly,
the aux target's type is aux_B(type) plus a uniformly random lift digit (random level B+1), sigma and pi are uniform
random bijections (the random K-L model), and the nxt source Xi(nxt w) is an independent draw from the current pool
of type nxt(type) (cavity assumption along the x4 chain).
Closure of the aux term: cbar_{k+1}(w_s) = c_k(w_s) * (min/mean of an independent level-(k+1) shape draw of that
type); the sibling magnitudes (c_k(w_s))_s = Xi_k(v) are a level-k triple from the previous pool, with their exact
sibling correlation.  Growth: (1 - lam^-2) E[Xi_{k+1}] = g(lam) rho_{k+1} E[Xi_k]; lam_{k+1} solves 1 - lam^-2 =
g(lam) rho_{k+1} (the summed identity, tight to 1e-5 in the exact system).
Start: the exact random model at level KS (meanfield.build, same seeds as meanfield_all9b), pools from c_{KS-1}, c_KS.
Validation: lam_k, 1 - rho_k against the random model (meanfield_all9b.json) at k = 14, 15.

  python popdyn.py [KMAX=60] [P=300] [SWEEPS=25] [SEED=0] [B=8] [KS=13] [CLOSURE=draw|const|noisy] [NU=0.33] [CC=0.35]   -> popdyn_{tag}.json
"""
import json
import sys
import time

import numpy as np
from scipy.optimize import brentq

import kl
import meanfield as mf

ALPHA = kl.ALPHA
PERMS = np.array([[0, 1, 2], [0, 2, 1], [1, 0, 2], [1, 2, 0], [2, 0, 1], [2, 1, 0]])


def g(lam):
    return (lam ** (ALPHA - 1) + lam ** (ALPHA - 2)) / 3


def lam_from_rho(rho):
    return brentq(lambda l: 1 - l ** -2 - g(l) * rho, 1.01, 2.0)


class Pop:
    def __init__(self, B, P, seed, closure="draw", nu=0.33, cc=0.35):
        self.B, self.P, self.closure, self.nu, self.cc = B, P, closure, nu, cc
        self.rng = np.random.default_rng(seed)
        S = kl.structure(B)
        self.nt = S["N"]                          # number of types = 3^(B-1)
        self.nxt_t = S["nxt"]                     # type -> type
        self.aux_t = S["aux"]                     # type -> level-(B-1) index or -1
        self.cls = S["cls"]                       # 2, 5, 8
        self.n_lift = self.nt // 3

    def weights(self, lam):
        L = np.where(self.cls == 2, lam ** (ALPHA - 2), np.where(self.cls == 8, lam ** (ALPHA - 1), 0.0))
        return lam ** -2, L

    def resample(self, pool_list):
        """pool_list: per type a (n_i, 3) array -> (nt, P, 3) by sampling with replacement."""
        out = np.empty((self.nt, self.P, 3))
        for t in range(self.nt):
            a = pool_list[t]
            out[t] = a[self.rng.integers(0, len(a), self.P)]
        return out

    def step(self, pool_k, lam, sweeps, pool_init=None):
        """pool_k: (nt, P, 3) level-k triples (mean 1 overall). Returns pool_{k+1} (unnormalised) and stats."""
        nt, P, rng = self.nt, self.P, self.rng
        q, L = self.weights(lam)
        cur = pool_k.copy() if pool_init is None else pool_init.copy()
        types = np.arange(nt)[:, None]
        for sw in range(sweeps):
            # x4 transport: independent draw from current pool of type nxt(type), random permutation
            j = rng.integers(0, P, (nt, P))
            src = cur[self.nxt_t[:, None], j]                                  # (nt, P, 3)
            perm = PERMS[rng.integers(0, 6, (nt, P))]
            trans = np.take_along_axis(src, perm, axis=2)
            # aux injection (classes 2, 8): sibling magnitudes from level-k pool, loss factors from current pool
            at = self.aux_t[:, None] + rng.integers(0, 3, (nt, P)) * self.n_lift   # aux type with random lift
            at = np.where(at >= 0, at, 0)
            mag = pool_k[at, rng.integers(0, P, (nt, P))]                       # (nt, P, 3) sibling magnitudes
            shp = cur[at[..., None], rng.integers(0, P, (nt, P, 3))]            # (nt, P, 3, 3) three shape draws
            if self.closure == "draw":
                loss = shp.min(axis=3) / shp.mean(axis=3)                       # (nt, P, 3)  cbar/c of each sibling
            else:                                                               # "const" / "noisy": pool-mean loss factor
                rho_pool = cur.min(axis=2).mean() / cur.mean(axis=2).mean()
                loss = rho_pool
                if self.closure == "noisy":                                     # rel. std nu*(1-rho), sibling corr cc
                    z0 = rng.standard_normal((nt, P, 1)); z = rng.standard_normal((nt, P, 3))
                    eps = self.nu * (1 - rho_pool) * (np.sqrt(self.cc) * z0 + np.sqrt(1 - self.cc) * z)
                    loss = rho_pool * (1 + eps)
            inj = mag * loss
            perm2 = PERMS[rng.integers(0, 6, (nt, P))]
            inj = np.take_along_axis(inj, perm2, axis=2)
            new = q * trans + L[:, None, None] * inj
            cur = new
        return cur

    def stats(self, pool):
        m = pool.mean(axis=2); mn = pool.min(axis=2)
        return dict(mean=float(m.mean()), rho=float(mn.mean() / m.mean()),
                    cmax=float(pool.max() / pool.min()))


def init_pools(B, KS, seed):
    """exact random model (levels >= B+1 random) at levels KS-1 and KS -> per-type lists of triples."""
    mf.K0 = B + 1
    nt = 3 ** (B - 1)
    pools, lams, rhos = {}, {}, {}
    lam_prev = 1.75
    for k in (KS - 1, KS):
        S = mf.build(k, "all", np.random.default_rng(1000 * k + seed))
        lam, rho, c = mf.lambda_secant(S, lam_prev, lam_prev + 0.01)
        lam_prev = lam
        c = c / c.mean()
        n = c.size // 3
        tri = np.stack([c[:n], c[n:2 * n], c[2 * n:]], axis=1)       # (n, 3) triples over level-(k-1) nodes
        typ = np.arange(n) % nt
        pools[k] = [tri[typ == t] for t in range(nt)]
        lams[k], rhos[k] = lam, rho
        print(f"init k={k}: lam={lam:.7f} 1-rho={1 - rho:.5f} samples/type={n // nt}", flush=True)
    return pools, lams, rhos


def main(kmax, P, sweeps, seed, B, KS, closure="draw", nu=0.33, cc=0.35):
    pop = Pop(B, P, seed, closure, nu, cc)
    tag = f"{closure}" + (f"_nu{nu}_c{cc}" if closure == "noisy" else "")
    pools, lams, rhos = init_pools(B, KS, seed)
    pool_k = pop.resample(pools[KS])
    lam = lams[KS]
    hist = {KS: dict(lam=lams[KS], rho=rhos[KS])}
    ref = json.load(open("meanfield_all9b.json"))["results"] if B == 8 else {}
    prev = 1 - rhos[KS]
    print(" k    lam_pop   1-rho_pop   q_pop  | random model: lam  1-rho   q  | exact 1-rho  Cmax")
    for k in range(KS + 1, kmax + 1):
        t = time.time()
        new = pop.step(pool_k, lam, sweeps)
        st = pop.stats(new)
        for _ in range(2):                      # re-iterate with the updated lambda
            lam = lam_from_rho(st["rho"])
            new = pop.step(pool_k, lam, sweeps, pool_init=new)
            st = pop.stats(new)
        lam = lam_from_rho(st["rho"])
        loss = 1 - st["rho"]
        hist[k] = dict(lam=lam, rho=st["rho"], cmax=st["cmax"])
        r = ref.get(str(k))
        rs = ""
        if r:
            rl, rr = np.mean(r["all"]["lam"]), 1 - np.mean(r["all"]["rho"])
            rp = 1 - np.mean(ref[str(k - 1)]["all"]["rho"]) if str(k - 1) in ref else np.nan
            rs = f"{rl:.5f} {rr:.5f} {rr / rp:.4f} | {1 - r['exact']['rho'][0]:.5f}"
        print(f"{k:3d}  {lam:.5f}  {loss:.5f}   {loss / prev:.4f}  | {rs}  {st['cmax']:.0f}  [{time.time() - t:.0f}s]",
              flush=True)
        prev = loss
        pool_k = new / st["mean"]
        json.dump(dict(B=B, KS=KS, P=P, sweeps=sweeps, seed=seed, hist=hist),
                  open(f"popdyn_{tag}_B{B}_P{P}_s{seed}.json", "w"), indent=1)


if __name__ == "__main__":
    a = sys.argv[1:]
    main(int(a[0]) if a else 60, int(a[1]) if len(a) > 1 else 300, int(a[2]) if len(a) > 2 else 25,
         int(a[3]) if len(a) > 3 else 0, int(a[4]) if len(a) > 4 else 8, int(a[5]) if len(a) > 5 else 13,
         a[6] if len(a) > 6 else "draw", float(a[7]) if len(a) > 7 else 0.33, float(a[8]) if len(a) > 8 else 0.35)
