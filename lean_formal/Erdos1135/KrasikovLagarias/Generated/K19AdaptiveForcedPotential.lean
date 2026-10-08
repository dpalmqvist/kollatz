import Erdos1135.KrasikovLagarias.AdaptiveForcedPotentialCertificate
import Erdos1135.KrasikovLagarias.ChunkedEncoding
import Erdos1135.KrasikovLagarias.LoopCheck

namespace Erdos1135
namespace KrasikovLagarias

def k19AdaptiveForcedPotentialHexChunks : Array String := #[
  include_str "../../../artifacts/kl_predecessor/k19_adaptive_potential/raw.000.hex",
  include_str "../../../artifacts/kl_predecessor/k19_adaptive_potential/raw.001.hex",
  include_str "../../../artifacts/kl_predecessor/k19_adaptive_potential/raw.002.hex",
  include_str "../../../artifacts/kl_predecessor/k19_adaptive_potential/raw.003.hex",
  include_str "../../../artifacts/kl_predecessor/k19_adaptive_potential/raw.004.hex",
  include_str "../../../artifacts/kl_predecessor/k19_adaptive_potential/raw.005.hex",
  include_str "../../../artifacts/kl_predecessor/k19_adaptive_potential/raw.006.hex",
  include_str "../../../artifacts/kl_predecessor/k19_adaptive_potential/raw.007.hex",
  include_str "../../../artifacts/kl_predecessor/k19_adaptive_potential/raw.008.hex",
  include_str "../../../artifacts/kl_predecessor/k19_adaptive_potential/raw.009.hex",
  include_str "../../../artifacts/kl_predecessor/k19_adaptive_potential/raw.010.hex",
  include_str "../../../artifacts/kl_predecessor/k19_adaptive_potential/raw.011.hex"
]

def k19AdaptiveForcedPotentialCertificate :
    AdaptiveForcedPotentialCertificate where
  k := 19
  bound := 36
  values := decodeU8HexChunks k19AdaptiveForcedPotentialHexChunks

theorem k19AdaptiveForcedPotentialEncodingValid :
    u8HexChunksEncodingValid k19AdaptiveForcedPotentialHexChunks
      387420489 = true := by
  native_decide

theorem k19AdaptiveForcedPotentialCertificate_checkLoop :
    k19AdaptiveForcedPotentialCertificate.checkLoop = true := by
  native_decide

theorem k19AdaptiveForcedPotentialCertificate_valid :
    k19AdaptiveForcedPotentialCertificate.Valid :=
  AdaptiveForcedPotentialCertificate.valid_of_checkLoop
    k19AdaptiveForcedPotentialCertificate_checkLoop

def k19AdaptiveForcedPotential :
    AdaptiveEliminationPolicy.ForcedPotential 19 (by norm_num) :=
  AdaptiveForcedPotentialCertificate.forcedPotential_of_checkLoop
    k19AdaptiveForcedPotentialCertificate_checkLoop

end KrasikovLagarias
end Erdos1135
