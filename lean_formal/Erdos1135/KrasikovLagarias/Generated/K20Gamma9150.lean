import Erdos1135.KrasikovLagarias.ChunkedEncoding
import Erdos1135.KrasikovLagarias.LoopCheck
import Erdos1135.KrasikovLagarias.RealCertificate

namespace Erdos1135
namespace KrasikovLagarias

def k20Gamma9150EncodedWeightHexChunks : Array String := #[
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.000.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.001.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.002.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.003.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.004.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.005.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.006.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.007.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.008.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.009.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.010.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.011.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.012.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.013.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.014.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.015.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.016.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.017.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.018.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.019.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.020.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.021.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.022.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.023.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.024.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.025.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.026.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.027.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.028.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.029.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.030.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.031.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.032.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.033.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.034.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.035.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.036.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.037.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.038.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.039.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.040.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.041.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.042.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.043.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.044.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.045.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.046.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.047.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.048.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.049.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.050.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.051.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.052.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.053.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.054.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.055.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.056.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.057.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.058.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.059.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.060.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.061.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.062.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.063.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.064.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.065.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.066.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.067.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.068.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.069.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.070.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.071.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.072.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.073.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.074.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.075.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.076.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.077.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.078.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.079.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.080.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.081.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.082.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.083.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.084.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.085.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.086.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.087.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.088.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.089.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.090.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.091.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.092.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.093.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.094.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.095.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.096.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.097.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.098.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.099.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.100.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.101.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.102.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.103.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.104.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.105.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.106.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.107.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.108.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.109.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.110.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.111.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.112.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.113.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.114.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.115.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.116.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.117.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.118.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.119.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.120.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.121.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.122.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.123.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.124.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.125.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.126.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.127.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.128.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.129.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.130.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.131.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.132.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.133.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.134.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.135.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.136.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.137.hex",
  include_str "../../../artifacts/kl_predecessor/k20_g9150_10000/raw.138.hex"
]

def k20Gamma9150EncodedCertificate : FiniteCertificate where
  k := 20
  gammaNum := 9150
  gammaDen := 10000
  coefficients := {
    scale := 268435456
    lambdaNeg2 := 75501396
    lambdaAlphaMinus2 := 206310311
    lambdaAlphaMinus1 := 389012342
  }
  weights := decodeU32LEHexChunks k20Gamma9150EncodedWeightHexChunks

theorem k20Gamma9150EncodedEncodingValid :
    u32HexChunksEncodingValid k20Gamma9150EncodedWeightHexChunks
      1162261467 = true := by
  native_decide

theorem k20Gamma9150EncodedCertificate_checkLoop :
    k20Gamma9150EncodedCertificate.checkLoop = true := by
  native_decide

theorem k20Gamma9150EncodedCertificate_valid :
    k20Gamma9150EncodedCertificate.Valid :=
  FiniteCertificate.valid_of_checkLoop k20Gamma9150EncodedCertificate_checkLoop

theorem k20Gamma9150EncodedCertificate_realRowValid {index : Nat}
    (hindex : index < k20Gamma9150EncodedCertificate.principalCount) :
    k20Gamma9150EncodedCertificate.RealRowValid
      (realCoefficients k20Gamma9150EncodedCertificate.gammaNum
        k20Gamma9150EncodedCertificate.gammaDen) index :=
  k20Gamma9150EncodedCertificate_valid.klRealRowValid hindex

end KrasikovLagarias
end Erdos1135
