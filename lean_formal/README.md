# Lean formalisation of the k = 18, gamma = 9032/10000 certificate

Add-on to Lech Mazur's `collatz_predecessor_090-1.0.0` (ProofAtlas, MIT; source archive
https://proofatlas.ai/sources/collatz-predecessor-090/commits/5f76a170e74ea5b0c37c56683bd4c1e9d72e5e3f/collatz_predecessor_090-1.0.0.tar.gz).

Steps (from the project root, Mazur's archive unpacked at $M):
1. `python certify_fast.py 18 1.87023 c_k18_mlx.npy --save`            -> certs/k18_1.87023 (vector tuned at the target lambda)
2. `python export_mazur.py certs/k18_1.87023 9032 10000 $M/artifacts/kl_predecessor/k18_g9032_10000 --scripts $M/scripts`
3. `python -I $M/scripts/make_kl_hex_chunks.py $M/artifacts/kl_predecessor/k18_g9032_10000/weights.u32le $M/artifacts/kl_predecessor/k18_g9032_10000`
4. `python -I $M/scripts/verify_kl_predecessor_certificate.py $M/artifacts/kl_predecessor/k18_g9032_10000/manifest.json`   (independent check)
5. copy the .lean files here into $M (same relative paths), replace $M/lakefile.toml with the one here
6. `cd $M && export PATH="$HOME/.elan/bin:$PATH" && lake exe cache get && lake build -j 1 CollatzPredecessor0903 AxiomAudit0903`

The potential certificate (second native_decide) is Mazur's own k = 18 payload; `potential.py 18` regenerates it
bit for bit (sha256 778584ce...). The .lean files were generated from his K18*.lean by textual substitution
(901/1000 -> 9032/10000, namespaces suffixed 9032, unit-coefficient exponent 903/1000 via the generic
`eventually_rpow_le_of_const_mul_rpow_le`).

## Second machine (Apple M4 Pro, 64 GB, 2026-10-08): k = 18, 19 regenerated, k = 20 added

Mazur's archive lives at `$M = ~/devel/mazur_dl/collatz_predecessor_090-1.0.0` (sha256 of the tarball bc59cf30…,
all 125 SHA256SUMS OK, `lake exe cache get` done, Lean v4.30.0-rc2 via elan). The vectors were regenerated on this
machine, so the weights differ bit-wise from the ones the first-machine hex chunks were made from; the manifests in
`artifacts/` are the new ones (the generated `.lean` files embed no hashes, only the chunk file list, so they are
unchanged except for K20).

k = 20 (gamma = 9150/10000, λ = 1.8855691 < λ_20 = 1.8857083):
1. `python certify_fast.py 20 1.88558 c_k20_mlx.npy --save`         -> certs/k20_1.88558 (slack 3.5e-5)
2. `python export_mazur.py certs/k20_1.88558 9150 10000 $M/artifacts/kl_predecessor/k20_g9150_10000 --weight-bits 19 --scripts $M/scripts`
   (19 bits: C_max/C_min = 4231 at k = 20, so 2^20 · 4231 > 2^32; the Lean row check is scale-invariant)
3. `python -I $M/scripts/make_kl_hex_chunks.py …/weights.u32le …/k20_g9150_10000`   (139 chunks of 32 MiB)
4. `mkdir -p $M/artifacts/kl_predecessor/k20_adaptive_potential && python potential.py 20 --out that_dir`
   (bit-identical to the first-machine payload, sha256 9eb9f69d…, 35 chunks), then Mazur's two verifiers.
5. K20*.lean, Generated/K20{Gamma9150,AdaptiveForcedPotential}.lean, CollatzPredecessor0915.lean,
   AxiomAudit0915.lean were generated from the K19 files by substitution (19→20, 18→19, 9093→9150, 909→915) and
   the coefficients 268435456 / 75501396 / 206310311 / 389012342 from `kl_predecessor_common.py`.
6. `cd $M && lake build Erdos1135.KrasikovLagarias.Generated.K20Potential10` (5825 s, 27.8 GB), then
   `…Generated.K20Gamma9150` (7382 s, 55.9 GB), then `lake build CollatzPredecessor0914 AxiomAudit0914`.
   Result (2026-10-09 02:07): `CollatzPredecessor0914.predecessor_count_lower_bound_0914` (x^(914/1000) ≤ π_a(x)),
   `_0914_nat`, `_09150` (constant · x^(9150/10000)); axioms: propext, Classical.choice, Quot.sound,
   k20AdaptiveForcedPotentialCertificate_checkLoop and k20Gamma9150EncodedCertificate_checkLoop (native_decide).
   The publication exponent is 914/1000, not 915/1000: the transfer lemma needs γ_pub < γ_cert strictly and
   915/1000 = 9150/10000.

### Large oleans: two rules learned at k = 20 (2026-10-09)

Lean mmaps every `.olean` at a base address derived from a hash of the module name
(`name.hash % 0x7f0000000000`, 64 KB aligned; `lean_read_module_data_parts` in `src/library/module.cpp`). If that
address range is already occupied, Lean falls back to reading the whole file with one `read()` call, which on macOS
fails above 2 GiB with `failed to read file '….olean'`. Consequences for the generated certificate modules
(k = 20: weights olean 9.3 GB, potential olean 2.3 GB):

1. **Import the big module first.** `import Erdos1135.KrasikovLagarias.Generated.K20Gamma9150` is the first line of
   every module that depends on it (K20CoefficientBridge, K20CriticalChoice, K20PredecessorBridge,
   K20PredecessorAllTargets, CollatzPredecessor0915, AxiomAudit0915), so that its 9.3 GB range is mapped before
   anything else can land in it. Importing it after `EliminationSourceSystem` fails deterministically.
2. **Check the name's address range before building.** The original `Generated.K20AdaptiveForcedPotential` hashed to
   a range containing `Mathlib.Algebra.Field.Defs`, so it could never be mapped once Mathlib was loaded. The module
   was renamed `Generated.K20Potential10` (base 0x233c07560000, 51 GB clear on both sides). Predict a candidate's base
   in Lean with `(n.hash % 0x7f0000000000) &&& ~~~0xffff` and compare against the base addresses at byte offset 0x50
   of all existing oleans (`.lake/build/lib/lean/**/*.olean` and the packages').
3. The four `simp` proofs in K20CoefficientBridge need `set_option maxRecDepth 100000` because the 139-chunk array
   exceeds the default recursion depth (47 chunks at k = 19 did not).
