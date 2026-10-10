/*
 * extremal_trees_core.c -- exact extremal leaf counts of the pruned 3x+1 trees T*_k(a)
 * of Applegate & Lagarias, "Density bounds for the 3x+1 problem I", Math. Comp. 64 (1995).
 *
 * Driven by extremal_trees.py (which compiles it); see notes/extremal_trees.md.
 *
 * Tree: root a (a != 0 mod 3); children of n: 2n always, and (2n-1)/3 iff n = 2 or 8 (mod 9).
 * Leaves are the nodes at depth exactly k; weight = number of (2n-1)/3 edges on the path.
 *
 * Chain decomposition.  Call a node a HEAD if it is the root or an odd child (2n-1)/3.  Every head
 * h at depth d starts the doubling chain h, 2h, ..., 2^(k-d) h, all of the same weight, which ends
 * in exactly one leaf at depth k.  Hence #leaves of weight >= tau = #heads of weight >= tau, and
 * N*_k(a) = #heads.  A chain node 2^i h (depth d+i < k) branches iff 2^i h = 2,8 (mod 9), which
 * depends on h mod 9 only.
 *
 * Digit revelation.  Write a = A + 3^J T with A = a mod 3^J known.  A head of weight w at depth d
 * is h = (2^d a - s)/3^w = h_A + 3^(J-w) 2^d T: it is known mod 3^(J-w), and revealing digit J of a
 * (T -> t + 3T') adds t 3^(J-w) 2^d to it.  After J digits every head of weight <= J-1 exists and
 * is located; the heads of weight J-1 are known mod 3 ("active").  Revealing digit J makes them
 * known mod 9, which fixes their chains and the weight-J heads they spawn.  Heads are carried as
 * exact representatives (unknown digits of a set to 0), so all residues are exact.
 *
 * Bounds.  A head with remaining depth m = k - d <= M is not expanded but kept "lazy": its exact
 * contribution is f_{m,tau'}(h) = #heads of relative weight >= tau' in T*_m(h), a function of
 * h mod 3^(m+1), and with s known digits it lies between the min and max of f_{m,tau'} over that
 * residue class mod 3^s (pyramid tables, computed exhaustively over all residues).  Active heads
 * (m > M) are bounded by the class extrema L_{m,tau'}(c mod 3) found at earlier depths.  Depth-
 * first branch and bound over the digits of a with these valid bounds is exact: every class of a is
 * either explored until its tree is fully determined or discarded because its bound cannot beat the
 * incumbent.
 *
 * Table layout ("trie order"): level s of a pyramid stores residues q mod 3^s at index
 * rev_s(q) (digits reversed), so the three refinements of a class are contiguous (3i, 3i+1, 3i+2).
 * A lazy head is stored as (idx = rev_s(r mod 3^s), hi = r div 3^s): revealing a digit adds
 * t 2^(k-m) to hi (mod 3^(m+1-s)) and moves one digit from hi to idx.  No divisions by variables.
 *
 * Modes:
 *   tables M TMAX                        build tables, print class extrema per (m, tau) and checks
 *   lp R SENSE THREADS [MAXIT]           certified residue-class bound mod 3^R (see lp_main)
 *   enum M TMAX K                        unpruned enumeration, sum identity (see enum_dfs)
 *   search M TMAX K0 K1 THR J0 [TAUMODE [SENSES [MAXLOG]]]
 *                                        tables, then branch and bound for k = K0..K1 (K0 <= M+1);
 *                                        with SENSES = 2 and MAXLOG the process forks after building
 *                                        the tables: parent = minimum (stdout), child = maximum (MAXLOG)
 * TMAX: 0 = only tau = 0 (leaf counts), 1 = all relative thresholds (for w^+-).
 * TAUMODE: 0 = tau = 0 only, 1 = all tau.  SENSES: 0 = min, 1 = max, 2 = both.
 * Output lines:  T m tau' min1 min2 max1 max2   (tables; class 1 and class 2 mod 3)
 *                S m sum                        (sum of f_m over n mod 3^(m+1), n != 0 mod 3)
 *                R k tau sense value secs nodes leaves   (search; class a = 2 mod 3)
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <pthread.h>
#include <stdatomic.h>
#include <time.h>
#include <unistd.h>
#include <math.h>

typedef unsigned __int128 u128;
typedef uint16_t tval;

#define MAXK 76            /* 3^(k+1) < 2^127 and all intermediate values fit */
#define MAXM 20

static u128 pow3q[MAXK + 4];
#define INV3 ((((u128)0xAAAAAAAAAAAAAAAAull) << 64) | 0xAAAAAAAAAAAAAAABull)  /* 3^-1 mod 2^128 */
static uint64_t pow3[41];

static int M, TMAX;
static tval *Pmin[MAXM + 1][MAXM + 2], *Pmax[MAXM + 1][MAXM + 2]; /* [m][tau'] pyramids, trie order */
static int64_t LminC[MAXK + 2][MAXK + 2][3], LmaxC[MAXK + 2][MAXK + 2][3]; /* [m][tau'][c mod 3] */

static inline size_t lvl_off(int s) { return (size_t)((pow3[s] - 3) / 2); } /* offset of level s>=1 */

static double now(void) {
    struct timespec ts; clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + 1e-9 * ts.tv_nsec;
}

static inline int ntau(int m) { return TMAX ? m + 1 : 1; }

/* ---------- tables ---------- */
static void to_trie(const tval *nat, tval *top, int s) {
    /* top[rev_s(n)] = nat[n], n < 3^s; rev updated incrementally */
    int dig[41] = { 0 };
    uint64_t N = pow3[s], rev = 0;
    for (uint64_t n = 0; n < N; n++) {
        top[rev] = nat[n];
        for (int i = 0; i < s; i++) {          /* n += 1 in base 3, keep rev in sync */
            if (dig[i] < 2) { dig[i]++; rev += pow3[s - 1 - i]; break; }
            dig[i] = 0; rev -= 2 * pow3[s - 1 - i];
        }
    }
}

static void build_tables(void) {
    double t0 = now();
    size_t total = 0;
    for (int m = 0; m <= M; m++) {
        size_t sz = lvl_off(m + 2);
        size_t szx = lvl_off(m + 1) + 1;   /* Pmax: levels 1..m only; the top level (exact f) is in Pmin */
        for (int tp = 0; tp < ntau(m); tp++) {
            Pmin[m][tp] = (tval *)malloc(sz * sizeof(tval));
            Pmax[m][tp] = (tval *)malloc(szx * sizeof(tval));
            if (!Pmin[m][tp] || !Pmax[m][tp]) { fprintf(stderr, "oom\n"); exit(1); }
            total += (sz + szx) * sizeof(tval);
        }
    }
    fprintf(stderr, "tables: %.2f GB\n", total / 1e9);
    /* natural-order f arrays for the previous and current depth (temporary) */
    tval *prev[MAXM + 2] = { 0 }, *cur[MAXM + 2] = { 0 };
    prev[0] = malloc(3 * sizeof(tval)); prev[0][0] = prev[0][1] = prev[0][2] = 1;
    memcpy(Pmin[0][0] + lvl_off(1), prev[0], 3 * sizeof(tval)); /* rev_1 = identity */
    for (int m = 1; m <= M; m++) {
        uint64_t Nm = pow3[m + 1], Np = pow3[m];
        for (int tp = 0; tp < ntau(m); tp++) {
            tval *f = malloc(Nm * sizeof(tval));
            if (!f) { fprintf(stderr, "oom\n"); exit(1); }
            const tval *g0 = (tp <= m - 1) ? prev[tp] : NULL;     /* even child: same tau' */
            int tq = tp - 1 < 0 ? 0 : tp - 1;
            const tval *g1 = prev[tq];                             /* odd child: tau'-1 */
            for (uint64_t n = 0; n < Nm; n++) {
                uint32_t v = g0 ? g0[(2 * n) % Np] : 0;
                uint64_t r9 = n % 9;
                if (r9 == 2 || r9 == 8) v += g1[((2 * n - 1) / 3) % Np];
                if (v > 65535) { fprintf(stderr, "overflow\n"); exit(1); }
                f[n] = (tval)v;
            }
            cur[tp] = f;
            to_trie(f, Pmin[m][tp] + lvl_off(m + 1), m + 1);
        }
        for (int tp = 0; tp < ntau(m - 1); tp++) { free(prev[tp]); prev[tp] = NULL; }
        for (int tp = 0; tp < ntau(m); tp++) { prev[tp] = cur[tp]; cur[tp] = NULL; }
    }
    for (int tp = 0; tp < ntau(M); tp++) free(prev[tp]);
    /* pyramids (trie order: children of i at level s are 3i, 3i+1, 3i+2 at level s+1) */
    for (int m = 0; m <= M; m++)
        for (int tp = 0; tp < ntau(m); tp++) {
            tval *mn = Pmin[m][tp], *mx = Pmax[m][tp];
            for (int s = m; s >= 1; s--) {
                tval *a = mn + lvl_off(s), *b = mn + lvl_off(s + 1);
                tval *c = mx + lvl_off(s), *d = (s == m) ? b : mx + lvl_off(s + 1);
                uint64_t P = pow3[s];
                for (uint64_t i = 0; i < P; i++) {
                    tval x = b[3 * i], y = b[3 * i + 1], z = b[3 * i + 2];
                    tval lo = x < y ? x : y; lo = lo < z ? lo : z;
                    a[i] = lo;
                    x = d[3 * i]; y = d[3 * i + 1]; z = d[3 * i + 2];
                    tval hi = x > y ? x : y; hi = hi > z ? hi : z;
                    c[i] = hi;
                }
            }
            for (int c = 1; c <= 2; c++) {     /* level 1: rev_1(c) = c (m = 0: level 1 is the top) */
                LminC[m][tp][c] = mn[lvl_off(1) + c];
                LmaxC[m][tp][c] = m ? mx[lvl_off(1) + c] : mn[lvl_off(1) + c];
            }
        }
    fprintf(stderr, "tables built in %.1f s\n", now() - t0);
}

/* ---------- search state ---------- */
typedef struct { u128 h; int16_t d; uint8_t r9; uint8_t pad; } Active;  /* weight J-1; r9 = h mod 9 */
typedef struct { uint32_t idx, hi; int8_t m, w; } Lazy;                 /* s = J - w known digits */

typedef struct {
    Active *act; int nact, cact;
    Lazy *lz; int nlz, clz;
    int64_t C;      /* exact part */
    int64_t B;      /* bound = C + bounds of pending heads */
    u128 A;         /* a mod 3^J (the digits chosen so far) */
} State;

static int K, TAU, SENSE, ROOTC;
static uint32_t C2[MAXM + 1][MAXM + 2];   /* 2^(k-m) mod 3^(m+1-s), [m][s], s = 1..m */
static uint32_t MODS[MAXM + 1][MAXM + 2]; /* 3^(m+1-s) */
static u128 inc_act[MAXK + 1];            /* 3 * 2^d mod 3^(k-d+1) */
static uint8_t inc_act9[MAXK + 1];        /* inc_act mod 9 */
static _Atomic int64_t best;
static _Atomic uint64_t nodes_total, leaves_total;
static pthread_mutex_t wmu = PTHREAD_MUTEX_INITIALIZER;
static u128 witness; static int have_witness;   /* a residue class attaining best */

static inline void reserve_act(State *s, int n) {
    if (n > s->cact) { s->cact = n * 2 + 16; s->act = realloc(s->act, s->cact * sizeof(Active)); }
}
static inline void reserve_lz(State *s, int n) {
    if (n > s->clz) { s->clz = n * 2 + 16; s->lz = realloc(s->lz, s->clz * sizeof(Lazy)); }
}

static inline int tau_rel(int w) { int t = TAU - w; return t < 0 ? 0 : t; }

static inline int64_t act_bound(int m, int w, int c) {
    int tp = tau_rel(w);
    if (tp > m) return 0;
    return SENSE ? LmaxC[m][tp][c] : LminC[m][tp][c];
}

static inline uint32_t mod9_u128(u128 x) {
    uint64_t lo = (uint64_t)x, hi = (uint64_t)(x >> 64);
    return (uint32_t)(((lo % 9) + (hi % 9) * 7) % 9);   /* 2^64 = 7 (mod 9) */
}

/* new lazy head: weight w, remaining depth m, representative r (< 3^(m+1)), 1 known digit.
   Adds exact contributions to *C, bounds to *B; appends to o if pending (o may be NULL). */
static inline void new_lazy(State *o, int m, int w, uint64_t r, int64_t *C, int64_t *B) {
    int tp = tau_rel(w);
    if (tp > m) return;
    uint32_t idx = (uint32_t)(r % 3);
    if (m == 0) { *C += Pmin[0][tp][lvl_off(1) + idx]; return; }
    tval lo = Pmin[m][tp][lvl_off(1) + idx], hi = Pmax[m][tp][lvl_off(1) + idx];
    if (lo == hi) { *C += lo; return; }
    *B += SENSE ? hi : lo;
    if (o) {
        if (o->nlz >= o->clz) reserve_lz(o, o->nlz + 1);
        o->lz[o->nlz++] = (Lazy){ idx, (uint32_t)(r / 3), (int8_t)m, (int8_t)w };
    }
}

/* expand the active heads of p (weight J-1) with digit t; new actives/lazies go to o (if o) */
static void expand(const State *p, int J, int t, State *o, int64_t *C, int64_t *B) {
    int w = J - 1;
    for (int i = 0; i < p->nact; i++) {
        Active A = p->act[i];
        int d = A.d, m = K - d;
        u128 mod = pow3q[m + 1];
        u128 x = A.h;
        if (t) { x += (u128)t * inc_act[d]; if (x >= mod) x -= mod; if (x >= mod) x -= mod; }
        unsigned r9 = (A.r9 + t * inc_act9[d]) % 9;
        if (w >= TAU) *C += 1;
        else if (TAU - w > m) continue;
        /* chain: node j at depth d+j, value x mod 3^(m+1-j) (x kept reduced), r9 = x mod 9 */
        for (int j = 0; j < m; j++) {
            if (r9 == 2 || r9 == 8) {
                int mc = m - j - 1, dc = d + j + 1;
                u128 c = (2 * x - 1) * INV3;           /* exact division; < 2 * 3^(mc+1) */
                u128 cm = pow3q[mc + 1];
                if (c >= cm) c -= cm;
                if (mc > M) {
                    if (TAU - (w + 1) <= mc) {
                        int cls = (r9 == 2) ? 1 : 2;
                        *B += act_bound(mc, w + 1, cls);
                        if (o) {
                            if (o->nact >= o->cact) reserve_act(o, o->nact + 1);
                            o->act[o->nact++] = (Active){ c, (int16_t)dc, (uint8_t)mod9_u128(c), 0 };
                        }
                    }
                } else new_lazy(o, mc, w + 1, (uint64_t)c, C, B);
            }
            if (j + 1 < m) {
                u128 nm = pow3q[m - j];                 /* modulus for node j+1 */
                x = 2 * x;
                while (x >= nm) x -= nm;                /* x < 2*3^(m+1-j) = 6 nm: <= 5 steps */
                r9 = (2 * r9) % 9;
            }
        }
    }
}

/* full child state o of p (J digits known) for digit J := t */
static void advance(const State *p, int J, int t, State *o) {
    o->nact = 0; o->nlz = 0;
    int64_t C = p->C, B = 0;
    reserve_lz(o, p->nlz + 16);
    for (int i = 0; i < p->nlz; i++) {
        Lazy L = p->lz[i];
        int m = L.m, w = L.w, s = J - w, tp = tau_rel(w);
        uint32_t mod = MODS[m][s], h = L.hi;
        if (t) { h += t * C2[m][s]; if (h >= mod) h -= mod; if (h >= mod) h -= mod; }
        uint32_t dg = h % 3, idx = 3 * L.idx + dg; h /= 3;
        int s1 = s + 1;
        tval lo = Pmin[m][tp][lvl_off(s1) + idx];
        if (s1 == m + 1) { C += lo; continue; }
        tval hi = Pmax[m][tp][lvl_off(s1) + idx];
        if (lo == hi) { C += lo; continue; }
        B += SENSE ? hi : lo;
        o->lz[o->nlz++] = (Lazy){ idx, h, (int8_t)m, (int8_t)w };
    }
    expand(p, J, t, o, &C, &B);
    o->C = C; o->B = C + B;
    o->A = p->A + (u128)t * pow3q[J];
}

/* bounds of the three children without building them */
static void child_bounds(const State *p, int J, int64_t Bt[3]) {
    int64_t C[3] = { p->C, p->C, p->C }, B[3] = { 0, 0, 0 };
    for (int i = 0; i < p->nlz; i++) {
        Lazy L = p->lz[i];
        int m = L.m, w = L.w, s = J - w, tp = tau_rel(w);
        uint32_t mod = MODS[m][s], c2 = C2[m][s];
        uint32_t h = L.hi;
        int s1 = s + 1;
        const tval *pl = Pmin[m][tp] + lvl_off(s1) + 3 * (size_t)L.idx;
        const tval *ph = (s1 <= m) ? Pmax[m][tp] + lvl_off(s1) + 3 * (size_t)L.idx : pl;
        for (int t = 0; t < 3; t++) {
            uint32_t dg = h % 3;
            tval lo = pl[dg];
            if (s1 == m + 1) C[t] += lo;
            else {
                tval hi = ph[dg];
                if (lo == hi) C[t] += lo; else B[t] += SENSE ? hi : lo;
            }
            h += c2; if (h >= mod) h -= mod;
        }
    }
    for (int t = 0; t < 3; t++) {
        int64_t c = 0, b = 0;
        expand(p, J, t, NULL, &c, &b);
        Bt[t] = C[t] + B[t] + c + b;
    }
}

static inline int prunable(int64_t bound, int64_t inc) {
    return SENSE ? (bound <= inc) : (bound >= inc);
}

static void update_best(int64_t v, u128 A) {
    int64_t cur = atomic_load(&best);
    if (!(SENSE ? (v > cur) : (v < cur))) return;
    pthread_mutex_lock(&wmu);
    cur = atomic_load(&best);
    if (SENSE ? (v > cur) : (v < cur)) { atomic_store(&best, v); witness = A; have_witness = 1; }
    pthread_mutex_unlock(&wmu);
}

typedef struct { State lv[MAXK + 4]; uint64_t nodes, leaves; } Work;

static void dfs(Work *W, int J, State *s) {
    W->nodes++;
    if (s->nact == 0 && s->nlz == 0) { W->leaves++; update_best(s->C, s->A); return; }
    int64_t Bt[3];
    child_bounds(s, J, Bt);
    int ord[3] = { 0, 1, 2 };
    for (int a = 0; a < 3; a++)
        for (int b = a + 1; b < 3; b++) {
            int64_t ba = Bt[ord[a]], bb = Bt[ord[b]];
            if (SENSE ? (bb > ba) : (bb < ba)) { int tmp = ord[a]; ord[a] = ord[b]; ord[b] = tmp; }
        }
    State *ch = &W->lv[J + 1];
    for (int a = 0; a < 3; a++) {
        if (prunable(Bt[ord[a]], atomic_load(&best))) continue;
        advance(s, J, ord[a], ch);
        dfs(W, J + 1, ch);
    }
}

/* ---- parallel driver ---- */
typedef struct { int64_t B; uint64_t prefix; } Sub;
static Sub *subs; static int nsubs, J0;
static _Atomic int next_sub;

static void make_root(State *s) {
    s->nact = 0; s->nlz = 0; s->C = 0; s->A = (u128)ROOTC;
    reserve_act(s, 4); reserve_lz(s, 4);
    if (K <= M) {
        int64_t C = 0, B = 0;
        new_lazy(s, K, 0, (uint64_t)ROOTC, &C, &B);
        s->C = C; s->B = C + B;
    } else {
        s->act[s->nact++] = (Active){ (u128)ROOTC, 0, (uint8_t)ROOTC, 0 };
        s->B = SENSE ? INT64_MAX / 4 : 0;
    }
}

static State *replay(Work *W, uint64_t prefix) {
    State *cur = &W->lv[1];
    make_root(cur);
    for (int J = 1; J < J0; J++) {
        int t = (int)(prefix % 3); prefix /= 3;
        State *nx = &W->lv[J + 1];
        advance(cur, J, t, nx);
        cur = nx;
    }
    return cur;
}

static int cmp_sub(const void *a, const void *b) {
    const Sub *x = a, *y = b;
    if (x->B != y->B) return SENSE ? (x->B < y->B ? 1 : -1) : (x->B < y->B ? -1 : 1);
    return 0;
}

static void free_work(Work *W) {
    for (int i = 0; i < MAXK + 4; i++) { free(W->lv[i].act); free(W->lv[i].lz); }
    free(W);
}

static void *worker(void *arg) {
    (void)arg;
    Work *W = calloc(1, sizeof(Work));
    for (;;) {
        int i = atomic_fetch_add(&next_sub, 1);
        if (i >= nsubs) break;
        if (prunable(subs[i].B, atomic_load(&best))) continue;
        State *s = replay(W, subs[i].prefix);
        if (prunable(s->B, atomic_load(&best))) continue;
        dfs(W, J0, s);
    }
    atomic_fetch_add(&nodes_total, W->nodes);
    atomic_fetch_add(&leaves_total, W->leaves);
    free_work(W);
    return NULL;
}

static void *prefix_worker(void *arg) {
    (void)arg;
    Work *W = calloc(1, sizeof(Work));
    for (;;) {
        int i = atomic_fetch_add(&next_sub, 64);
        if (i >= nsubs) break;
        for (int j = i; j < i + 64 && j < nsubs; j++) {
            State *s = replay(W, (uint64_t)j);
            subs[j].B = s->B; subs[j].prefix = (uint64_t)j;
            if (s->nact == 0 && s->nlz == 0) update_best(s->C, s->A);
        }
    }
    free_work(W);
    return NULL;
}

static void setup_k(int k) {
    K = k;
    for (int m = 0; m <= M && m <= k; m++)
        for (int s = 1; s <= m; s++) {
            uint64_t mod = pow3[m + 1 - s], v = 1 % mod;
            for (int i = 0; i < k - m; i++) v = (2 * v) % mod;
            C2[m][s] = (uint32_t)v; MODS[m][s] = (uint32_t)mod;
        }
    for (int d = 0; d <= k; d++) {
        u128 mod = pow3q[k - d + 1], v = 3 % mod;
        for (int i = 0; i < d; i++) v = (2 * v) % mod;
        inc_act[d] = v; inc_act9[d] = (uint8_t)mod9_u128(v);
    }
}

static int64_t solve(int k, int tau, int sense, int rootc, int nthreads, int j0,
                     int64_t init, double *secs, uint64_t *nodes, uint64_t *leaves) {
    double t0 = now();
    setup_k(k); TAU = tau; SENSE = sense; ROOTC = rootc;
    atomic_store(&best, init); have_witness = 0;
    atomic_store(&nodes_total, 0); atomic_store(&leaves_total, 0);
    J0 = j0 < 1 ? 1 : j0;
    if (J0 > k + 2) J0 = k + 2;
    nsubs = 1; for (int i = 1; i < J0; i++) nsubs *= 3;
    subs = malloc(nsubs * sizeof(Sub));
    pthread_t th[64];
    if (nthreads > 64) nthreads = 64;
    if (nthreads < 1) nthreads = 1;
    /* phase 1 (parallel): bounds of all prefixes of J0-1 digits */
    atomic_store(&next_sub, 0);
    for (int i = 0; i < nthreads; i++) pthread_create(&th[i], NULL, prefix_worker, NULL);
    for (int i = 0; i < nthreads; i++) pthread_join(th[i], NULL);
    qsort(subs, nsubs, sizeof(Sub), cmp_sub);
    atomic_store(&next_sub, 0);
    for (int i = 0; i < nthreads; i++) {
        pthread_attr_t at; pthread_attr_init(&at);
        pthread_attr_setstacksize(&at, 64 << 20);
        pthread_create(&th[i], &at, worker, NULL);
    }
    for (int i = 0; i < nthreads; i++) pthread_join(th[i], NULL);
    free(subs);
    *secs = now() - t0; *nodes = atomic_load(&nodes_total); *leaves = atomic_load(&leaves_total);
    return atomic_load(&best);
}

static void print_u128(u128 v) {
    char buf[64]; int i = 63; buf[i] = 0;
    if (v == 0) { printf("0"); return; }
    while (v) { buf[--i] = '0' + (int)(v % 10); v /= 10; }
    printf("%s", buf + i);
}

/* full enumeration (no pruning, no bounds used): every class of a is followed until its count is
   determined.  Checks the bookkeeping: sum over a mod 3^(K+1), a != 0 mod 3, of N*_K(a) = 2*4^K, and
   min/max over the enumeration equal the branch-and-bound values. */
static u128 enum_sum, enum_cnt; static uint64_t enum_leaves; static int64_t enum_min, enum_max;
static void enum_dfs(Work *W, int J, State *s) {
    if (s->nact == 0 && s->nlz == 0) {
        enum_leaves++;
        enum_sum += (u128)s->C * pow3q[K + 1 - J];   /* class a mod 3^J covers 3^(K+1-J) residues */
        enum_cnt += pow3q[K + 1 - J];
        if (s->C < enum_min) enum_min = s->C;
        if (s->C > enum_max) enum_max = s->C;
        return;
    }
    State *ch = &W->lv[J + 1];
    for (int t = 0; t < 3; t++) {
        advance(s, J, t, ch);
        enum_dfs(W, J + 1, ch);
    }
}

static void print_tables(void) {
    for (int m = 0; m <= M; m++)
        for (int tp = 0; tp < ntau(m); tp++)
            printf("T %d %d %lld %lld %lld %lld\n", m, tp,
                   (long long)LminC[m][tp][1], (long long)LminC[m][tp][2],
                   (long long)LmaxC[m][tp][1], (long long)LmaxC[m][tp][2]);
}


/* ---------- residue-class (depth Krasikov-Lagarias) system for large r ----------
   Phi(v)(c) = v(2c) + [c = 2,8 mod 9] min_t v(l_t(c)),  l_t(c) = (2c-1)/3 + 2t 3^(r-1) mod 3^r,
   Psi with max.  Power iteration in float32 (only to find V); the certificate
   Q*Phi(V) >= P*V (resp. Q*Psi(V) <= P*V) is checked exactly in 64-bit integers for every class.
   Usage: lp R SENSE THREADS MAXIT    prints  L r sense P Q Vmin Vmax iters rmin rmax  */
static int LR, LSENSE; static uint64_t LRN, L3; static float *lv, *lw;
typedef struct { uint64_t lo, hi; int phase; double rmin, rmax, wmax; uint64_t P, Q; int ok; uint32_t vmin, vmax; double scale; } LPpart;

static inline uint64_t lpe(uint64_t c) { uint64_t e = 2 * c; return e >= LRN ? e - LRN : e; }
static inline void lpl(uint64_t c, uint64_t l[3]) {
    uint64_t b = (2 * c - 1) / 3;
    for (int t = 0; t < 3; t++) { uint64_t x = b + 2 * (uint64_t)t * L3; while (x >= LRN) x -= LRN; l[t] = x; }
}
static void *lp_worker(void *arg) {
    LPpart *P = arg;
    if (P->phase == 0) {            /* w = Phi(v), ratios */
        double rmin = 1e300, rmax = -1e300, wmax = 0;
        for (uint64_t c = P->lo; c < P->hi; c++) {
            if (c % 3 == 0) continue;
            float w = lv[lpe(c)];
            unsigned r9 = c % 9;
            if (r9 == 2 || r9 == 8) {
                uint64_t l[3]; lpl(c, l);
                float a = lv[l[0]], b = lv[l[1]], d = lv[l[2]];
                float m = LSENSE ? (a > b ? a : b) : (a < b ? a : b);
                m = LSENSE ? (m > d ? m : d) : (m < d ? m : d);
                w += m;
            }
            lw[c] = w;
            double q = (double)w / lv[c];
            if (q < rmin) rmin = q;
            if (q > rmax) rmax = q;
            if (w > wmax) wmax = w;
        }
        P->rmin = rmin; P->rmax = rmax; P->wmax = wmax;
    } else if (P->phase == 1) {     /* v = (v + w/wmax)/2 */
        float inv = (float)(1.0 / P->wmax);
        for (uint64_t c = P->lo; c < P->hi; c++) if (c % 3) lv[c] = 0.5f * lv[c] + 0.5f * lw[c] * inv;
    } else if (P->phase == 2) {     /* integer V into lw (as uint32) */
        uint32_t *V = (uint32_t *)lw; uint32_t mn = UINT32_MAX, mx = 0;
        for (uint64_t c = P->lo; c < P->hi; c++) {
            if (c % 3 == 0) { V[c] = 0; continue; }
            double x = (double)lv[c] * P->scale;
            uint32_t q = x < 1 ? 1 : (uint32_t)llround(x);
            V[c] = q; if (q < mn) mn = q; if (q > mx) mx = q;
        }
        P->vmin = mn; P->vmax = mx;
    } else {                        /* exact check */
        const uint32_t *V = (const uint32_t *)lw; int ok = 1;
        for (uint64_t c = P->lo; c < P->hi && ok; c++) {
            if (c % 3 == 0) continue;
            uint64_t w = V[lpe(c)];
            unsigned r9 = c % 9;
            if (r9 == 2 || r9 == 8) {
                uint64_t l[3]; lpl(c, l);
                uint64_t a = V[l[0]], b = V[l[1]], d = V[l[2]];
                uint64_t m = LSENSE ? (a > b ? a : b) : (a < b ? a : b);
                m = LSENSE ? (m > d ? m : d) : (m < d ? m : d);
                w += m;
            }
            unsigned __int128 lhs = (unsigned __int128)w * P->Q, rhs = (unsigned __int128)V[c] * P->P;
            if (LSENSE ? (lhs > rhs) : (lhs < rhs)) ok = 0;
        }
        P->ok = ok;
    }
    return NULL;
}
static void lp_run(int nth, LPpart *parts, int phase) {
    pthread_t th[64];
    for (int i = 0; i < nth; i++) { parts[i].phase = phase; pthread_create(&th[i], NULL, lp_worker, &parts[i]); }
    for (int i = 0; i < nth; i++) pthread_join(th[i], NULL);
}
static int lp_main(int r, int sense, int nth, int maxit) {
    LR = r; LSENSE = sense; LRN = 1; for (int i = 0; i < r; i++) LRN *= 3; L3 = LRN / 3;
    lv = malloc(LRN * sizeof(float)); lw = malloc(LRN * sizeof(float));
    if (!lv || !lw) { fprintf(stderr, "oom\n"); return 1; }
    for (uint64_t c = 0; c < LRN; c++) lv[c] = 1.0f;
    if (nth > 64) nth = 64;
    LPpart parts[64]; memset(parts, 0, sizeof parts);
    for (int i = 0; i < nth; i++) { parts[i].lo = LRN * i / nth; parts[i].hi = LRN * (i + 1) / nth; }
    double rmin = 0, rmax = 0, best = sense ? 1e300 : -1e300; int stall = 0, it;
    double t0 = now();
    for (it = 0; it < maxit; it++) {
        lp_run(nth, parts, 0);
        rmin = 1e300; rmax = -1e300; double wmax = 0;
        for (int i = 0; i < nth; i++) {
            if (parts[i].rmin < rmin) rmin = parts[i].rmin;
            if (parts[i].rmax > rmax) rmax = parts[i].rmax;
            if (parts[i].wmax > wmax) wmax = parts[i].wmax;
        }
        double key = sense ? rmax : rmin;
        if (sense ? key < best - 1e-9 : key > best + 1e-9) { best = key; stall = 0; } else stall++;
        if (it % 20 == 0) { fprintf(stderr, "lp r=%d s=%d it=%d [%.9f, %.9f] %.0fs\n", r, sense, it, rmin, rmax, now() - t0); }
        if (rmax - rmin < 2e-7 || stall > 40) break;
        for (int i = 0; i < nth; i++) parts[i].wmax = wmax;
        lp_run(nth, parts, 1);
    }
    /* v is the vector whose ratios are [rmin, rmax]; certify */
    float vmaxf = 0; for (uint64_t c = 0; c < LRN; c++) if (c % 3 && lv[c] > vmaxf) vmaxf = lv[c];
    for (int i = 0; i < nth; i++) parts[i].scale = 2147483648.0 / vmaxf;  /* V <= 2^31 */
    lp_run(nth, parts, 2);
    uint32_t vmn = UINT32_MAX, vmx = 0;
    for (int i = 0; i < nth; i++) { if (parts[i].vmin < vmn) vmn = parts[i].vmin; if (parts[i].vmax > vmx) vmx = parts[i].vmax; }
    uint64_t Q = 10000000ull;
    uint64_t P = sense ? (uint64_t)ceil(rmax * Q) + 10 : (uint64_t)floor(rmin * Q) - 10;
    int ok = 0;
    for (int tries = 0; tries < 20 && !ok; tries++) {
        for (int i = 0; i < nth; i++) { parts[i].P = P; parts[i].Q = Q; }
        lp_run(nth, parts, 3);
        ok = 1; for (int i = 0; i < nth; i++) ok &= parts[i].ok;
        if (!ok) P = sense ? P + 10 : P - 10;
    }
    printf("L %d %d %llu %llu %u %u %d %.10f %.10f %s %.0f\n", r, sense, (unsigned long long)P, (unsigned long long)Q,
           vmn, vmx, it, rmin, rmax, ok ? "CERTIFIED" : "FAILED", now() - t0);
    fflush(stdout);
    free(lv); free(lw);
    return ok ? 0 : 2;
}

int main(int argc, char **argv) {
    pow3[0] = 1; for (int i = 1; i < 41; i++) pow3[i] = pow3[i - 1] * 3;
    pow3q[0] = 1; for (int i = 1; i < MAXK + 4; i++) pow3q[i] = pow3q[i - 1] * 3;
    if (argc < 4) { fprintf(stderr, "usage: see header\n"); return 1; }
    const char *mode = argv[1];
    if (!strcmp(mode, "lp")) {      /* lp R SENSE THREADS [MAXIT] */
        int r = atoi(argv[2]), sense = atoi(argv[3]), nth = argc > 4 ? atoi(argv[4]) : 4;
        int maxit = argc > 5 ? atoi(argv[5]) : 3000;
        if (r < 2 || r > 20) { fprintf(stderr, "r in 2..20\n"); return 1; }
        return lp_main(r, sense, nth, maxit);
    }
    M = atoi(argv[2]); TMAX = atoi(argv[3]);
    if (M < 0 || M > 19) { fprintf(stderr, "M must be in 0..19\n"); return 1; }
    if (!strcmp(mode, "tables")) {
        build_tables();
        print_tables();
        /* A-L (2.8): sum over a mod 3^(m+1), a != 0 mod 3, of N*_m(a) = 2*3^m*(4/3)^m = 2*4^m.
           In trie order the lowest digit of the residue is the top digit of the index. */
        for (int m = 0; m <= M; m++) {
            const tval *f = Pmin[m][0] + lvl_off(m + 1);
            u128 sum = 0;
            for (uint64_t i = 0; i < pow3[m + 1]; i++) if (i / pow3[m] != 0) sum += f[i];
            printf("S %d ", m); print_u128(sum); printf("\n");
        }
        return 0;
    }
    if (!strcmp(mode, "enum")) {   /* enum M TMAX K: needs class bounds only for SENSE use; none used */
        int k = atoi(argv[4]);
        build_tables();
        setup_k(k); TAU = 0; SENSE = 0;
        for (int c = 1; c <= 2; c++) {
            Work *W = calloc(1, sizeof(Work));
            ROOTC = c; enum_sum = 0; enum_cnt = 0; enum_leaves = 0; enum_min = INT64_MAX; enum_max = -1;
            State *s0 = &W->lv[1];
            make_root(s0);
            /* make_root with K > M puts the root as an active head; bounds are irrelevant here */
            enum_dfs(W, 1, s0);
            printf("E %d %d %llu %lld %lld ", k, c, (unsigned long long)enum_leaves,
                   (long long)enum_min, (long long)enum_max);
            print_u128(enum_sum); printf(" "); print_u128(enum_cnt); printf("\n");
            fflush(stdout);
            free_work(W);
        }
        return 0;
    }
    if (!strcmp(mode, "search")) {
        if (argc < 8) { fprintf(stderr, "usage: see header\n"); return 1; }
        int K0 = atoi(argv[4]), K1 = atoi(argv[5]), thr = atoi(argv[6]), j0 = atoi(argv[7]);
        int taumode = argc > 8 ? atoi(argv[8]) : 0;
        int senses = argc > 9 ? atoi(argv[9]) : 2;
        if (taumode && !TMAX) { fprintf(stderr, "thresholds need TMAX=1\n"); return 1; }
        /* ET_LOAD=log1[,log2..]: class extrema of earlier depths from previous runs (R lines) */
        int kload = M;
        const char *ld = getenv("ET_LOAD");
        if (ld) {
            char buf[4096]; strncpy(buf, ld, sizeof buf - 1); buf[sizeof buf - 1] = 0;
            for (char *path = strtok(buf, ","); path; path = strtok(NULL, ",")) {
                FILE *fh = fopen(path, "r");
                if (!fh) { perror(path); return 1; }
                char line[512];
                while (fgets(line, sizeof line, fh)) {
                    int k, tau, sn; long long v;
                    if (line[0] == 'R' && sscanf(line + 1, "%d %d %d %lld", &k, &tau, &sn, &v) == 4 &&
                        k > M && k <= MAXK) {
                        if (sn) { LmaxC[k][tau][2] = v; LmaxC[k + 1][tau][1] = v; }
                        else { LminC[k][tau][2] = v; LminC[k + 1][tau][1] = v; }
                        if (tau == 0 && k > kload) kload = k;
                    }
                }
                fclose(fh);
            }
        }
        if (K0 > kload + 1) { fprintf(stderr, "K0 must be <= %d (class bounds of all smaller depths)\n", kload + 1); return 1; }
        /* ET_INIT_MIN / ET_INIT_MAX: incumbent for the first depth (verification of a known value:
           the result equals the incumbent iff no class-2 tree beats it); printed as V lines */
        const char *imin = getenv("ET_INIT_MIN"), *imax = getenv("ET_INIT_MAX");
        if (K1 > MAXK) K1 = MAXK;
        build_tables();
        if (argc > 10 && senses == 2) {
            /* fork: the child runs the maximum (output to argv[10]), the parent the minimum;
               the tables are shared copy-on-write and never written after this point */
            fflush(stdout); fflush(stderr);
            pid_t pid = fork();
            if (pid < 0) { perror("fork"); return 1; }
            if (pid == 0) {
                if (!freopen(argv[10], "w", stdout)) { perror("freopen"); _exit(1); }
                senses = 1;
            } else senses = 0;
        }
        print_tables();
        fflush(stdout);
        for (int k = K0; k <= K1; k++) {
            int taumax = taumode ? k : 0;
            for (int tau = 0; tau <= taumax; tau++)
                for (int sense = 0; sense <= 1; sense++) {
                    if (senses != 2 && sense != senses) continue;
                    double secs; uint64_t nodes, leaves;
                    int64_t init = sense ? -1 : INT64_MAX / 4;
                    int verify = 0;
                    if (k == K0 && tau == 0 && !sense && imin) { init = atoll(imin); verify = 1; }
                    if (k == K0 && tau == 0 && sense && imax) { init = atoll(imax); verify = 1; }
                    int64_t v = solve(k, tau, sense, 2, thr, j0, init, &secs, &nodes, &leaves);
                    if (verify) {   /* v == init: no class-2 tree beats init (v is then only a bound) */
                        printf("V %d %d %d %lld %lld %.3f %llu %llu\n", k, tau, sense, (long long)v,
                               (long long)init, secs, (unsigned long long)nodes, (unsigned long long)leaves);
                        fflush(stdout);
                        if (v == init) return 0;  /* class value not exact: nothing further is valid */
                        /* otherwise a strictly better tree exists and v is the exact optimum */
                    }
                    if (sense) { LmaxC[k][tau][2] = v; LmaxC[k][tau][1] = LmaxC[k - 1][tau][2]; }
                    else { LminC[k][tau][2] = v; LminC[k][tau][1] = LminC[k - 1][tau][2]; }
                    printf("R %d %d %d %lld %.3f %llu %llu\n", k, tau, sense, (long long)v, secs,
                           (unsigned long long)nodes, (unsigned long long)leaves);
                    if (have_witness && tau == 0) {   /* a = witness (mod 3^(k+1)) attains v */
                        printf("W %d %d %d %lld ", k, tau, sense, (long long)v);
                        print_u128(witness); printf("\n");
                    }
                    fflush(stdout);
                }
        }
        return 0;
    }
    fprintf(stderr, "unknown mode\n");
    return 1;
}
