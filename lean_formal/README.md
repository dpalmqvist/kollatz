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
