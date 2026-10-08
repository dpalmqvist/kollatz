import Erdos1135.KrasikovLagarias.ChunkedEncoding
import Erdos1135.KrasikovLagarias.RealCertificate

namespace Erdos1135
namespace KrasikovLagarias

def k18Gamma9032EncodedWeightHexChunks : Array String := #[
  include_str "../../../artifacts/kl_predecessor/k18_g9032_10000/raw.000.hex",
  include_str "../../../artifacts/kl_predecessor/k18_g9032_10000/raw.001.hex",
  include_str "../../../artifacts/kl_predecessor/k18_g9032_10000/raw.002.hex",
  include_str "../../../artifacts/kl_predecessor/k18_g9032_10000/raw.003.hex",
  include_str "../../../artifacts/kl_predecessor/k18_g9032_10000/raw.004.hex",
  include_str "../../../artifacts/kl_predecessor/k18_g9032_10000/raw.005.hex",
  include_str "../../../artifacts/kl_predecessor/k18_g9032_10000/raw.006.hex",
  include_str "../../../artifacts/kl_predecessor/k18_g9032_10000/raw.007.hex",
  include_str "../../../artifacts/kl_predecessor/k18_g9032_10000/raw.008.hex",
  include_str "../../../artifacts/kl_predecessor/k18_g9032_10000/raw.009.hex",
  include_str "../../../artifacts/kl_predecessor/k18_g9032_10000/raw.010.hex",
  include_str "../../../artifacts/kl_predecessor/k18_g9032_10000/raw.011.hex",
  include_str "../../../artifacts/kl_predecessor/k18_g9032_10000/raw.012.hex",
  include_str "../../../artifacts/kl_predecessor/k18_g9032_10000/raw.013.hex",
  include_str "../../../artifacts/kl_predecessor/k18_g9032_10000/raw.014.hex",
  include_str "../../../artifacts/kl_predecessor/k18_g9032_10000/raw.015.hex"
]

def k18Gamma9032EncodedCertificate : FiniteCertificate where
  k := 18
  gammaNum := 9032
  gammaDen := 10000
  coefficients := {
    scale := 268435456
    lambdaNeg2 := 76746626
    lambdaAlphaMinus2 := 207011852
    lambdaAlphaMinus1 := 387155562
  }
  weights := decodeU32LEHexChunks k18Gamma9032EncodedWeightHexChunks

theorem k18Gamma9032EncodedEncodingValid :
    u32HexChunksEncodingValid k18Gamma9032EncodedWeightHexChunks
      129140163 = true := by
  native_decide

theorem k18Gamma9032EncodedCertificate_check :
    k18Gamma9032EncodedCertificate.check = true := by
  native_decide

theorem k18Gamma9032EncodedCertificate_valid :
    k18Gamma9032EncodedCertificate.Valid :=
  FiniteCertificate.valid_of_check k18Gamma9032EncodedCertificate_check

theorem k18Gamma9032EncodedCertificate_realRowValid {index : Nat}
    (hindex : index < k18Gamma9032EncodedCertificate.principalCount) :
    k18Gamma9032EncodedCertificate.RealRowValid
      (realCoefficients k18Gamma9032EncodedCertificate.gammaNum
        k18Gamma9032EncodedCertificate.gammaDen) index :=
  k18Gamma9032EncodedCertificate_valid.klRealRowValid hindex

end KrasikovLagarias
end Erdos1135
