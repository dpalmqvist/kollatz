import Erdos1135.KrasikovLagarias.ChunkedEncoding
import Erdos1135.KrasikovLagarias.LoopCheck
import Erdos1135.KrasikovLagarias.RealCertificate

namespace Erdos1135
namespace KrasikovLagarias

def k19Gamma9093EncodedWeightHexChunks : Array String := #[
  include_str "../../../artifacts/kl_predecessor/k19_g9093_10000/raw.000.hex",
  include_str "../../../artifacts/kl_predecessor/k19_g9093_10000/raw.001.hex",
  include_str "../../../artifacts/kl_predecessor/k19_g9093_10000/raw.002.hex",
  include_str "../../../artifacts/kl_predecessor/k19_g9093_10000/raw.003.hex",
  include_str "../../../artifacts/kl_predecessor/k19_g9093_10000/raw.004.hex",
  include_str "../../../artifacts/kl_predecessor/k19_g9093_10000/raw.005.hex",
  include_str "../../../artifacts/kl_predecessor/k19_g9093_10000/raw.006.hex",
  include_str "../../../artifacts/kl_predecessor/k19_g9093_10000/raw.007.hex",
  include_str "../../../artifacts/kl_predecessor/k19_g9093_10000/raw.008.hex",
  include_str "../../../artifacts/kl_predecessor/k19_g9093_10000/raw.009.hex",
  include_str "../../../artifacts/kl_predecessor/k19_g9093_10000/raw.010.hex",
  include_str "../../../artifacts/kl_predecessor/k19_g9093_10000/raw.011.hex",
  include_str "../../../artifacts/kl_predecessor/k19_g9093_10000/raw.012.hex",
  include_str "../../../artifacts/kl_predecessor/k19_g9093_10000/raw.013.hex",
  include_str "../../../artifacts/kl_predecessor/k19_g9093_10000/raw.014.hex",
  include_str "../../../artifacts/kl_predecessor/k19_g9093_10000/raw.015.hex",
  include_str "../../../artifacts/kl_predecessor/k19_g9093_10000/raw.016.hex",
  include_str "../../../artifacts/kl_predecessor/k19_g9093_10000/raw.017.hex",
  include_str "../../../artifacts/kl_predecessor/k19_g9093_10000/raw.018.hex",
  include_str "../../../artifacts/kl_predecessor/k19_g9093_10000/raw.019.hex",
  include_str "../../../artifacts/kl_predecessor/k19_g9093_10000/raw.020.hex",
  include_str "../../../artifacts/kl_predecessor/k19_g9093_10000/raw.021.hex",
  include_str "../../../artifacts/kl_predecessor/k19_g9093_10000/raw.022.hex",
  include_str "../../../artifacts/kl_predecessor/k19_g9093_10000/raw.023.hex",
  include_str "../../../artifacts/kl_predecessor/k19_g9093_10000/raw.024.hex",
  include_str "../../../artifacts/kl_predecessor/k19_g9093_10000/raw.025.hex",
  include_str "../../../artifacts/kl_predecessor/k19_g9093_10000/raw.026.hex",
  include_str "../../../artifacts/kl_predecessor/k19_g9093_10000/raw.027.hex",
  include_str "../../../artifacts/kl_predecessor/k19_g9093_10000/raw.028.hex",
  include_str "../../../artifacts/kl_predecessor/k19_g9093_10000/raw.029.hex",
  include_str "../../../artifacts/kl_predecessor/k19_g9093_10000/raw.030.hex",
  include_str "../../../artifacts/kl_predecessor/k19_g9093_10000/raw.031.hex",
  include_str "../../../artifacts/kl_predecessor/k19_g9093_10000/raw.032.hex",
  include_str "../../../artifacts/kl_predecessor/k19_g9093_10000/raw.033.hex",
  include_str "../../../artifacts/kl_predecessor/k19_g9093_10000/raw.034.hex",
  include_str "../../../artifacts/kl_predecessor/k19_g9093_10000/raw.035.hex",
  include_str "../../../artifacts/kl_predecessor/k19_g9093_10000/raw.036.hex",
  include_str "../../../artifacts/kl_predecessor/k19_g9093_10000/raw.037.hex",
  include_str "../../../artifacts/kl_predecessor/k19_g9093_10000/raw.038.hex",
  include_str "../../../artifacts/kl_predecessor/k19_g9093_10000/raw.039.hex",
  include_str "../../../artifacts/kl_predecessor/k19_g9093_10000/raw.040.hex",
  include_str "../../../artifacts/kl_predecessor/k19_g9093_10000/raw.041.hex",
  include_str "../../../artifacts/kl_predecessor/k19_g9093_10000/raw.042.hex",
  include_str "../../../artifacts/kl_predecessor/k19_g9093_10000/raw.043.hex",
  include_str "../../../artifacts/kl_predecessor/k19_g9093_10000/raw.044.hex",
  include_str "../../../artifacts/kl_predecessor/k19_g9093_10000/raw.045.hex",
  include_str "../../../artifacts/kl_predecessor/k19_g9093_10000/raw.046.hex"
]

def k19Gamma9093EncodedCertificate : FiniteCertificate where
  k := 19
  gammaNum := 9093
  gammaDen := 10000
  coefficients := {
    scale := 268435456
    lambdaNeg2 := 76100363
    lambdaAlphaMinus2 := 206648894
    lambdaAlphaMinus1 := 388114314
  }
  weights := decodeU32LEHexChunks k19Gamma9093EncodedWeightHexChunks

theorem k19Gamma9093EncodedEncodingValid :
    u32HexChunksEncodingValid k19Gamma9093EncodedWeightHexChunks
      387420489 = true := by
  native_decide

theorem k19Gamma9093EncodedCertificate_checkLoop :
    k19Gamma9093EncodedCertificate.checkLoop = true := by
  native_decide

theorem k19Gamma9093EncodedCertificate_valid :
    k19Gamma9093EncodedCertificate.Valid :=
  FiniteCertificate.valid_of_checkLoop k19Gamma9093EncodedCertificate_checkLoop

theorem k19Gamma9093EncodedCertificate_realRowValid {index : Nat}
    (hindex : index < k19Gamma9093EncodedCertificate.principalCount) :
    k19Gamma9093EncodedCertificate.RealRowValid
      (realCoefficients k19Gamma9093EncodedCertificate.gammaNum
        k19Gamma9093EncodedCertificate.gammaDen) index :=
  k19Gamma9093EncodedCertificate_valid.klRealRowValid hindex

end KrasikovLagarias
end Erdos1135
