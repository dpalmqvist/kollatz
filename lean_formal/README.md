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
6. `cd $M && lake build Erdos1135.KrasikovLagarias.Generated.K20AdaptiveForcedPotential`, then
   `…Generated.K20Gamma9150`, then `lake build CollatzPredecessor0915 AxiomAudit0915` (≈ 30 GiB per native_decide).
