import Erdos1135.KrasikovLagarias.AdaptiveForcedPotentialCertificate
import Erdos1135.KrasikovLagarias.ChunkedEncoding
import Erdos1135.KrasikovLagarias.LoopCheck

namespace Erdos1135
namespace KrasikovLagarias

def k20AdaptiveForcedPotentialHexChunks : Array String := #[
  include_str "../../../artifacts/kl_predecessor/k20_adaptive_potential/raw.000.hex",
  include_str "../../../artifacts/kl_predecessor/k20_adaptive_potential/raw.001.hex",
  include_str "../../../artifacts/kl_predecessor/k20_adaptive_potential/raw.002.hex",
  include_str "../../../artifacts/kl_predecessor/k20_adaptive_potential/raw.003.hex",
  include_str "../../../artifacts/kl_predecessor/k20_adaptive_potential/raw.004.hex",
  include_str "../../../artifacts/kl_predecessor/k20_adaptive_potential/raw.005.hex",
  include_str "../../../artifacts/kl_predecessor/k20_adaptive_potential/raw.006.hex",
  include_str "../../../artifacts/kl_predecessor/k20_adaptive_potential/raw.007.hex",
  include_str "../../../artifacts/kl_predecessor/k20_adaptive_potential/raw.008.hex",
  include_str "../../../artifacts/kl_predecessor/k20_adaptive_potential/raw.009.hex",
  include_str "../../../artifacts/kl_predecessor/k20_adaptive_potential/raw.010.hex",
  include_str "../../../artifacts/kl_predecessor/k20_adaptive_potential/raw.011.hex",
  include_str "../../../artifacts/kl_predecessor/k20_adaptive_potential/raw.012.hex",
  include_str "../../../artifacts/kl_predecessor/k20_adaptive_potential/raw.013.hex",
  include_str "../../../artifacts/kl_predecessor/k20_adaptive_potential/raw.014.hex",
  include_str "../../../artifacts/kl_predecessor/k20_adaptive_potential/raw.015.hex",
  include_str "../../../artifacts/kl_predecessor/k20_adaptive_potential/raw.016.hex",
  include_str "../../../artifacts/kl_predecessor/k20_adaptive_potential/raw.017.hex",
  include_str "../../../artifacts/kl_predecessor/k20_adaptive_potential/raw.018.hex",
  include_str "../../../artifacts/kl_predecessor/k20_adaptive_potential/raw.019.hex",
  include_str "../../../artifacts/kl_predecessor/k20_adaptive_potential/raw.020.hex",
  include_str "../../../artifacts/kl_predecessor/k20_adaptive_potential/raw.021.hex",
  include_str "../../../artifacts/kl_predecessor/k20_adaptive_potential/raw.022.hex",
  include_str "../../../artifacts/kl_predecessor/k20_adaptive_potential/raw.023.hex",
  include_str "../../../artifacts/kl_predecessor/k20_adaptive_potential/raw.024.hex",
  include_str "../../../artifacts/kl_predecessor/k20_adaptive_potential/raw.025.hex",
  include_str "../../../artifacts/kl_predecessor/k20_adaptive_potential/raw.026.hex",
  include_str "../../../artifacts/kl_predecessor/k20_adaptive_potential/raw.027.hex",
  include_str "../../../artifacts/kl_predecessor/k20_adaptive_potential/raw.028.hex",
  include_str "../../../artifacts/kl_predecessor/k20_adaptive_potential/raw.029.hex",
  include_str "../../../artifacts/kl_predecessor/k20_adaptive_potential/raw.030.hex",
  include_str "../../../artifacts/kl_predecessor/k20_adaptive_potential/raw.031.hex",
  include_str "../../../artifacts/kl_predecessor/k20_adaptive_potential/raw.032.hex",
  include_str "../../../artifacts/kl_predecessor/k20_adaptive_potential/raw.033.hex",
  include_str "../../../artifacts/kl_predecessor/k20_adaptive_potential/raw.034.hex"
]

def k20AdaptiveForcedPotentialCertificate :
    AdaptiveForcedPotentialCertificate where
  k := 20
  bound := 38
  values := decodeU8HexChunks k20AdaptiveForcedPotentialHexChunks

theorem k20AdaptiveForcedPotentialEncodingValid :
    u8HexChunksEncodingValid k20AdaptiveForcedPotentialHexChunks
      1162261467 = true := by
  native_decide

theorem k20AdaptiveForcedPotentialCertificate_checkLoop :
    k20AdaptiveForcedPotentialCertificate.checkLoop = true := by
  native_decide

theorem k20AdaptiveForcedPotentialCertificate_valid :
    k20AdaptiveForcedPotentialCertificate.Valid :=
  AdaptiveForcedPotentialCertificate.valid_of_checkLoop
    k20AdaptiveForcedPotentialCertificate_checkLoop

def k20AdaptiveForcedPotential :
    AdaptiveEliminationPolicy.ForcedPotential 20 (by norm_num) :=
  AdaptiveForcedPotentialCertificate.forcedPotential_of_checkLoop
    k20AdaptiveForcedPotentialCertificate_checkLoop

end KrasikovLagarias
end Erdos1135
