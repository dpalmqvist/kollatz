# Collatz: Krasikov–Lagarias-gränsen för större k

## Bakgrund
Projektet förbättrar den nedre gränsen π_a(x) ≥ x^γ för 3x+1-problemet (antalet n ≤ x vars bana når a, a ≢ 0 mod 3)
med metoden i I. Krasikov & J. C. Lagarias, "Bounds for the 3x+1 problem using difference inequalities",
Acta Arith. 109 (2003) 237–258, arXiv:math/0205002. Publicerat (refereegranskat) rekord: γ = 0,84 (k = 11).
Vårt läge (2026-10-07): γ = 0,9203 certifierat vid k = 21. Se "Omvärld 2026" nedan – vi ligger före alla kända
anspråk, men "rekord" betyder numera formellt verifierat (Lean).

Metoden: för varje k finns linjärprogrammet L^NT_k(λ) med principalvariabler c_m, m ∈ [3^k] = {m mod 3^k : m ≡ 2 mod 3}
(N = 3^(k−1) st), α = log2(3):

- m ≡ 2 (mod 9): c_m ≤ λ^-2 c_{4m} + λ^(α−2) · cbar_{(4m−2)/3}
- m ≡ 5 (mod 9): c_m ≤ λ^-2 c_{4m}
- m ≡ 8 (mod 9): c_m ≤ λ^-2 c_{4m} + λ^(α−1) · cbar_{(2m−1)/3}
- c_m ≥ 1, där cbar_r = min(c_r, c_{r+3^(k−1)}, c_{r+2·3^(k−1)}) för r mod 3^(k−1).

OBS tryckfel i artikeln: (2.13)–(2.14) skriver 3^k, ska vara 3^(k−1). Reproduktionen bekräftar detta.

En tillåten lösning för λ ger (Thm 2.2 + §6) π_a(x) ≥ x^γ för alla γ < log2 λ, x ≥ x0(a, γ).
Konstanten: φ^m_k(y) ≥ Δ1 · c_m λ^y med Δ1 = 1/(4 max c_m), så C_max/C_min (växer ~1.52^k, 6457 vid k = 21)
styr hur stort x0 blir.

Vad artikeln säger om k → ∞ (§6, viktigt): λ_k ≤ λ_{k+1} (lyftet tile(c) är tillåtet), strikt ökning är öppet
problem (empiriskt sant t.o.m. k = 21). Summering av alla olikheter ger
  (1 − λ^-2) · c̄_{k,k} ≤ (1/3)(λ^(α−1) + λ^(α−2)) · c̄_{k−1,k},
där c̄_{k,k} = medel av c och c̄_{k−1,k} = medel av cbar. Nödvändigt och tillräckligt för π_a(x) ≥ x^(1−ε) för
alla ε är λ_k → 2, vilket följer om ρ_k := c̄_{k−1,k}/c̄_{k,k} → 1. K–L tror (utan bevis) att L^NT_k ger den
bästa gräns som differensolikheterna I_k alls medger, och att optimum nås med alla olikheter som likheter.

## Indexering (verifierad för k = 3…11; MLX-F mot NumPy-F för k ≤ 13)
Residy m = 3i+2 har index i ∈ [0, N). Allt är affint, inga indexarrayer behövs:
- index för 4m mod 3^k: `(4i + 2) mod N`
- klass: i mod 3 = 0 ↔ m ≡ 2 (mod 9), 1 ↔ 5, 2 ↔ 8
- hjälpindex (i cbar-arrayen, längd N/3): i = 3j → `4j mod N/3`; i = 3j+2 → `2j+1 mod N/3`
- cbar[r] = min(c[r], c[r + N/3], c[r + 2N/3])
- ternär siffra j av i (j = 0…k−2) = siffra j+1 av m; översta siffran (j = k−2) är den som cbar minimerar över.
  `c.reshape(3^(k−2−j), 3, 3^j)` lägger siffra j på axel 1.

## Algoritm
λ_k = största λ med r(F_λ) ≥ 1, där F är högerledet (monoton, 1-homogen). Potensiteration
c ← F(c)/min F(c); min och max av F(c)/c ger undre/övre gräns för r (Collatz–Wielandt).
Värmestart: lyft lösningen för k−1 med `np.tile(c, 3)` (c_{k}[i + j·N_{k−1}] = c_{k−1}[i]).

λ-sökning (kl_mlx.py): sekantmetod på f(λ) = log r(F_λ), r ≈ mitten av [lo, hi], start λ = 1.75, 1.85,
värmestart från föregående c. 5–7 λ-värden räcker (k = 14, 15). Lärdomar:
- float32 har ett golv för gapet hi − lo (k = 3: ~3e-5, över tol 2e-6) → potensiteration stoppar även när
  gapet slutat minska (stagnation), annars körs hela iters-taket (k = 3 tog 881 s).
- Stoppa sekanten på steglängd, inte på "1 ∈ [lo, hi]": d log r/dλ ≈ −0.3, så gap 1e-6 i r ger fel ~3e-6 i λ.
- float32 bestämmer λ_k till ~2e-7. Vid k = 16 nåddes roten efter 4 λ-värden, sedan 7 steg i brusgolvet innan
  steglängden < 1e-8. width höjd till 1e-7, men k = 18 vandrade ändå 8 steg (~1e-6) i bruset: λ-bruset är
  ~(hi − lo)/|d log r/dλ| och kan vara > 1e-7. Sekanten stoppar nu också när steget < (hi − lo)/(2|lutning|),
  lutningen från de två första punkterna.

GPU utan indexarrayer: `make_F` är en enda Metal-kärna (`mx.fast.metal_kernel`) som räknar index per tråd i
64-bitars heltal, 2-D-grid (i = y·2^16 + x) så att N > 2^31 fungerar. Minne = c och F(c) (2 vektorer);
normaliseringen läggs i koefficienterna (F 1-homogen: F(c/m) = F(c)/m), lo/hi räknas chunkvis.
`growth` tar c0 som lista [c] och tömmer den – annars håller anroparen kvar den gamla vektorn (3 vektorer).
Uppmätt topp: 2.45 vektorer inkl. k−1-vektorn för värmestart. `make_F_slices` (strided slices + concatenate,
~3 vektorer) finns kvar som referens; compare kontrollerar att de ger samma F.

## Rigorös certifiering (certify_fast.py, verify_cert.py)
Heltalsform, inga avrundningar: λ = P/Q, D = 2^d,
q = ⌊D·Q²/P²⌋, L_j = ⌊D · rigorös undre gräns för λ^(α−j)⌋ (j = 1, 2), C = c·2^b (format /2, se nedan), och
C_m·D ≤ q·C_{4m} + L_j·C̄ kontrolleras i int64. Eftersom q/D ≤ λ^-2 och L_j/D ≤ λ^(α−j) följer olikheten.
Format /2 (från k = 20): certifikatet ÄR float32-vektorn c (`c_f32.npy`), med C_i = c_i·2^b,
b = 23 − ⌊log2 min c⌋, vilket är ett exakt heltal för varje positiv normal float32 ≥ min c. certify_fast.py bildar
C med bitoperationer (mantissa << shift) per chunk; verify_cert.py oberoende med float64·2^b + heltalskontroll.
Minne ~4 byte/variabel (c som memmap för numpy, en GPU-kopia för mlx). Format /1 (`C.npy`, int64) läses också.
OBS: macOS-filsystemet är skiftlägesokänsligt – `c.npy` skriver över `C.npy`, därav namnet `c_f32.npy`.
ÖVRE certifikat (2026-10-08, `--upper`): koefficienterna avrundas UPPÅT (q = ⌈D·Q²/P²⌉, L_j = ⌈D·övre
intervallgräns⌉) och varje rad måste uppfylla strikt q·C_{4m} + L_j·C̄ < D·C_m, dvs F(C) < C. För monoton
1-homogen F följer att inget tillåtet d finns (s = max d_i/C_i i i*: d_{i*} ≤ F(d)_{i*} ≤ s·F(C)_{i*} < s·C_{i*}),
alltså λ_k < λ. Sparas i `certs/k{k}_{λ}_upper/` (format /2-upper), verify_cert.py kontrollerar riktningen.
Vektorn = potensitererad c vid λ_k + 1e-5 (k = 3 behövde +2e-4 p.g.a. float32-golvet). Brackets för k = 2…19 i
RESULTS.md; k = 20–22 klara (00:19 2026-10-09), alla 21 nivåer tvåsidiga.
Snabb- och exakt certifiering skiljer sig bara i säker riktning: k = 2, λ = 1.3534 (slack 2e-8 < float32-
upplösning) ger fast=False, certify.py=True (den förfinar c i float64). Snabbvägen kräver slack ≳ 1e-7.
d väljs så att max C·D < 2^63 och max C·(q + L) < 2^63
bevisas med Python-heltal före kontrollen, så overflow är omöjligt. Hur c togs fram (float32) spelar ingen roll.
int64 är exakt även på GPU (MLX, testat bitvis mot NumPy), så kontrollen får köras där; `--backend both`
kör CPU och GPU och kräver samma utslag. OBS: MLX typar Python-int-skalärer som int32 – gör dem explicit int64.
Kontrollen tar 0.1 s vid k = 15; flaskhalsen är potensiterationen.

## Formalisering via Mazurs Lean-ramverk (2026-10-08)
Källa: `proofatlas.ai/sources/collatz-predecessor-090/commits/5f76a17.../collatz_predecessor_090-1.0.0.tar.gz`
(570 MB, MIT, Lech Mazur 2026), uppackad i scratchpad `mazur_dl/collatz_predecessor_090-1.0.0`. Lean v4.30.0-rc2,
Mathlib pinnad (`lake exe cache get` fungerar, ~8300 filer). Verktygskedja: `export PATH="$HOME/.elan/bin:$PATH"`.
Hans certifikatformat (`kl-predecessor-certificate-v1`) = vårt: vikter C_i som u32 little-endian med min 2^20,
λ = 2^(p/q), dyadiska undre gränser för λ^-2, λ^(α−2), λ^(α−1) med nämnare 2^28 via exakt heltalsrotdragning
(`scripts/kl_predecessor_common.py`), radkontroll scale·C_i ≤ a·C_{4i} + b_j·min(lyft) – identiska indexformler.
Lean: `FiniteCertificate.check` (Certificate.lean) via `native_decide`; hex-chunkar ≤ 64 MiB med `include_str`
(`scripts/make_kl_hex_chunks.py`); `RealCertificate.lean` lyfter till reella koefficienter; K–L:s sats 2.2 ersätts av
`AdaptiveCriticalChoice.exponential_lower_bound` som kräver ett andra certifikat: en "forced potential"
pot: [N) → 0..bound (u8) med pot[4i+2] ≤ pot[i]+6, min_t pot[lyft(4q)] ≤ pot[3q]+1, min_t pot[lyft(2q+1)] ≤ pot[3q+2]−2
(`AdaptiveForcedPotentialCertificate.lean`). Potentialen beror BARA på k, inte på vikterna – hans k = 18-payload
återanvänds; `potential.py` räknar den minsta lösningen som minsta fixpunkt för andra k.
De k-specifika filerna K18{CoefficientBridge,CriticalChoice,PredecessorBridge,PredecessorAllTargets}.lean är små
och mekaniska; för γ = 9032/10000 genererades kopior (…9032.lean, namnrymd K18G9032) + `CollatzPredecessor0903.lean`
+ `AxiomAudit0903.lean` + lakefile-poster. Bygg seriellt: `lake build -j 1 CollatzPredecessor0903 AxiomAudit0903`
(native_decide-stegen tar ~10 GiB vardera; hans mått: LP 18.5 min/10.6 GiB, potential 14.6 min/9.3 GiB vid k = 18).
VIKTIG LÄRDOM: en fast vektor c som är tillåten vid λ1 är INTE automatiskt tillåten vid λ2 < λ1 – λ^(α−1) minskar
när λ sjunker, så raderna m ≡ 8 (mod 9) kan spricka (vårt c_18 vid λ = 1.8703 gav 34.8 M fel vid λ = 2^0.903).
Vektorn måste trimmas (potensitereras) vid mål-λ: `certify_fast.py 18 1.87023 c_k18_mlx.npy --save` →
`certs/k18_1.87023` (slack 2.7e-5), export med `export_mazur.py certs/k18_1.87023 9032 10000 OUT --scripts …/scripts`
(slack 2.07e-5, u32-vikter max 1.92e9). Mazurs oberoende Python-verifierare: PASS, 129 140 163 rader, 0 fel.
Potentialcertifikatet: `potential.py 18` (minsta fixpunkt, 23 iterationer, 15 s) ger exakt Mazurs payload
(sha256 778584ce…, max 34). k = 19: max 36, 24 iterationer, 50 s, Mazurs verifierare PASS (645 700 815 olikheter);
k = 20: max 38, Mazurs verifierare PASS (1 937 102 445 olikheter, sha256 9eb9f69d…). Potentialens maximum växer ~2 per k.
Minne i Lean: hans `check` bygger `List.range N` (≥ 16 B/klass) utöver `Array Nat` (8 B/klass) och hex-strängen
(8 B/klass). `LoopCheck.lean` (vårt tillägg, bevisat ekvivalent med `Valid`) ersätter listan med en svansrekursiv
slinga (`allBelow`), så k = 19 bör klara sig på ~8–10 GiB per native_decide. k = 20 (×3) och k = 21 (×9) går inte här.
k = 19-pipeline (2026-10-08): mål λ = 2^0.9093 = 1.878134; trimmad vid 1.87813 (`certs/k19_1.87813`, slack 5.1e-5),
export γ = 9093/10000 (slack 4.7e-5, u32 max 2.91e9), 47 hex-chunkar, Mazurs Python-verifierare PASS (387 420 489 rader).
Lean-filer: K19{PowerOfTwoTargets,SourceBridge,PrincipalIndex,CoefficientBridge,CriticalChoice,PredecessorBridge,
PredecessorAllTargets}.lean + Generated/K19{Gamma9093,AdaptiveForcedPotential}.lean (checkLoop) + CollatzPredecessor0909.
Lake 5 saknar `-j`; bygg de tunga modulerna var för sig: `lake build …Generated.K18AdaptiveForcedPotential`,
sedan `…Generated.K18Gamma9032`, sedan `lake build CollatzPredecessor0903 AxiomAudit0903` (samma för 0909).
Allt som behövs för att återskapa ligger i `lean_formal/` (README med stegen); scratchpad-trädet är tillfälligt.
RESULTAT k = 18 (2026-10-08): `CollatzPredecessor0903` byggt. native_decide-tider: potential 568 s, LP med våra vikter
818 s (Mazur: 876 s / 1111 s). Axiomrevision: `predecessor_count_lower_bound_0903` (x^(903/1000) ≤ π_a(x) för stora x,
alla a ≢ 0 mod 3), `_0903_nat`, `_09032` (konstant·x^(9032/10000)) beror på propext, Classical.choice, Quot.sound +
de två native_decide-axiomen (k18AdaptiveForcedPotentialCertificate_check, k18Gamma9032EncodedCertificate_check) –
samma förtroendebas som Mazurs 0.90. Fallgrop: `open K18G9032` saknades i PredecessorBridge9032 (textersättningen
träffade inte efter namnbytet) – rättad; K19-filerna hade rätt open-rader från början.
RESULTAT k = 19 (2026-10-08): `CollatzPredecessor0909` byggt med LoopCheck-kontrollerna. native_decide: potential
1819 s (topp ~7.7 GB), LP 2335 s (~2.7 GB RSS, mer i swap). Ombyggt på M4 Pro 64 GB (kväll 2026-10-08) med de
regenererade vikterna: potential 2113 s (11.6 GB), LP 2554 s (24.4 GB RSS – ingen swap), samma axiom. k = 18 ombyggt:
643 s / 871 s (14.0 GB). k = 20 KLART 2026-10-09 02:07: `CollatzPredecessor0914` (x^(914/1000) ≤ π_a(x); 915/1000 = 9150/10000 ger ingen strikt
marginal) – potential 5940 s (26.3 GB; ombyggd som K20Potential10 5825 s), LP 7382 s (55.9 GB), axiom = 3 standard +
2 native_decide. FÄLLOR: (1) stora .olean mmappas på hash(modulnamn)-adress, fallback read() misslyckas > 2 GiB –
importera Generated.K20Gamma9150 FÖRST överallt; (2) K20AdaptiveForcedPotentials adressintervall innehöll
Mathlib.Algebra.Field.Defs → modulen döptes om till Generated.K20Potential10; (3) set_option maxRecDepth 100000
(139 chunkar). Se lean_formal/README. k = 21 ≈ 170 GB, k = 22 ≈ 500 GB ⇒ strömmande verifierare krävs. `predecessor_count_lower_bound_0909`: x^(909/1000) ≤ π_a(x),
samt `_0909_nat` och `_09093` (konstant·x^(9093/10000)); axiom: de tre standard + k19AdaptiveForcedPotentialCertificate_
checkLoop och k19Gamma9093EncodedCertificate_checkLoop (native_decide). Fallgrop 2: `Generated.K19Gamma901` blev kvar i
K19CoefficientBridge (regex \b901\b träffar inte inuti identifierare) – rättad med sed. Axiomrevisionerna sparade i
`lean_formal/logs/axiom_audits.txt`. Minnesuppskattning med LoopCheck: k = 20 ≈ 30 GiB, k = 21 ≈ 90 GiB.

## Filer
- `kl.py` – struktur, F, potensiteration, bisektion (NumPy, float64)
- `certify.py` – exakt certifiering: rationellt λ = P/10^6, heltals-c, rigorösa rationella undre gränser
  för λ^(α−2), λ^(α−1) via mpmath intervallaritmetik, alla olikheter kontrolleras med Python-heltal.
  Användning: `python certify.py k LAMBDA [c0.npy] [iters]`
- `iter.py` – iteration med tidsgräns och sparat mellanläge (för stora k)
- `kl_mlx.py` – MLX-port (float32, GPU): F utan indexarrayer, potensiteration med stagnationsstopp, sekantmetod.
  `python kl_mlx.py compare KMAX` (mot kl.py), `python kl_mlx.py lambda K [c0.npy]` (sparar c_k{K}_mlx.npy)
- `certify_fast.py` – rigorös int64-certifiering (NumPy och/eller MLX), strömmande, c från kl_mlx på GPU.
  `python certify_fast.py k LAMBDA [c0.npy] [--backend numpy|mlx|both] [--exact] [--save]`
  `--exact` kontrollerar samma heltal även med Python-heltal; `--save` skriver `certs/k{k}_{LAMBDA}/`.
- `verify_cert.py` – fristående verifierare (bara numpy + mpmath, ingen projektkod): `python verify_cert.py certs/k15_1.8419 [--exact]`
- `certs/k{k}_{λ}/` – certifikat: format /2 `c_f32.npy` (float32) + `cert.json` (k, N, λ = P/Q, D, q, L2, L1, b,
  sha256 för data och fil, minsta relativa slack, mjukvaruversioner, tidsstämpel); k = 4, 13–19 är format /1
  (`C.npy` int64), k = 12, 20, 21 format /2
- `plot_gamma.py` – γ_k mot k med geometrisk anpassning + residualpanel (symlog) → `gamma_trend.png`;
  lägg till nya k i LAMBDA och kör om. OBS: dess γ∞ ≈ 0.98 är modellberoende, se "Trend".
- `adaptive.py` – adaptivt-träd-experimentet (löv i ett 3-adiskt träd, G = min över lövet av F; sekant på log r
  med värmestart från orakellösningen, ~120 iterationer/λ). `python adaptive.py [k]` → `adaptive_k{k}.json`.
  k = 12: 10 s, k = 14: ~3 min. Resultat: se "Idéer att pröva", punkt 1.
- `lp_check.py` – oberoende implementation (plan 7b): L^NT_k som explicit LP (HiGHS), villkoren byggda direkt från
  residyer med Python-heltal, ingen kod delad med sökningen. Bisektion på LP-tillåtlighet → λ_k; exakt rationell
  verifiering av LP-lösningen vid λ_k − 2e-6 (högerled krympta med 1e-7 så lösningen får slack); negativt test.
  `python lp_check.py [KMAX]` (k ≤ 9: 3 min, k = 9 dominerar).
- `holder.py` – mätningar för gränsobjektet k → ∞: kuloscillation osc_j och Hölder-exponent β_j, riktningsprofil,
  spridning (C_max, kvantiler, massa i topp-1 %), extrapolation av r_mid(k) → `holder.json`. `python holder.py`
- `RESULTS.md` – fristående skrivelse (engelska) av resultatet med LP-definition, certifikatformat, sha256 för alla
  certifikat, oberoende kontroller och metodens status. Uppdatera vid nya k eller ny status (formalisering).
- `AVENUES.md` – levande dokument över möjliga spår (7 st) med status, vad som gjorts och hur man plockar upp dem.
- `tree_growth.py k Y` – exakt BFS av föregångarträd per residyklass (spår 2): alla klasser växer ~x^1 vid k = 9,
  mot LP:ts 0.82 ⇒ förlusten är trunkeringen i k, inte vad som räknas. Trädstorlek ~ x^γ i absolut x: håll a·2^Y ≲ 2^27.
- `limit_measure.py` – spår 1: (A) TV-avstånd mellan nivå-j-marginaler av μ_k och μ_{k+1} (avtar ~0.92/nivå ⇒ gränsmått
  finns), (B) Perron-vektorn vid λ = 2 mot c_k (TV 0.085 → 0.075, logkorr 0.997 → 0.998 för k = 8 → 13).
- `jacobian.py` – spår 1: spektrum för lineariseringen av F i Perron-vektorn (andra egenvärdet ~0.86, komplext) och
  r(F_2) för k ≤ 11. r(F_2) för k = 12…21 via `certify_fast.py k 2 [c0]` (bara "power iteration"-raden är relevant).
- `rF2_fit.py` – spår 1: r_k(F_2) för k = 5…21 (exakt r_k = 1/4 + (3/4)ρ'_k, ρ' = blandningskvoten för λ=2-vektorn);
  1 − r_k: kvoter stiger 0.905 → 0.922; offset-modell (r∞ = 0.9929) och sträckt exponential (r∞ = 1) passar lika
  (1.7e-4). Odeciderat; data lutar svagt mot fortsatt inbromsning. k = 21 vid λ = 2 tog 456 s (int8-vägen).
  k = 22 (2026-10-08, `kl_split.py rate 22 2 c_k22_part0.npy`, 43 min): r_22 = 0.974971, ρ(λ=2) = 0.966628,
  kvot för 1 − r_k = 0.9239 (fortsatt stigande ~0.0018/steg). Anpassningar k = 5…22: offset-modell r∞ = 0.9928,
  sträckt exponential r∞ = 1, båda maxres 1.8e-4; blint från k ≤ 16 missar offset-modellen k = 22 med −4.3e-4.
- `renorm.py`, `renorm2.py` – spår 1: renormalisering av toppsiffe-känsligheten. Injektion per nivå exakt 3/4 vid
  λ = 2, förstärkning A_k ≈ 1.21 → 1.23; A∞ < 4/3 ⇔ λ_k → 2. renorm2: uppdelning c = P (×4-term) + Q (aux-term),
  "alignment efficiency" e_k = 0.61 → 0.74 (k = 8…15), argmin-överensstämmelse 0.33 (= oberoende). Prognos:
  kvoten för 1 − r_k planar ut nära 0.94 < 1 ⇒ λ_k → 2. Se AVENUES.md spår 1.
- `kl_d.py` – spår 3: K–L-LP för 3x+d; isomorft med d = 1 via m ↦ d·m′ ⇒ λ_k(d) = λ_k(1) (verifierat k ≤ 7).
- `cycles_d.py` – spår 3: cykelkatalog för 3x+d (d ≤ 29) med Eliahou-olikheten; 3x+13 har sju 8-cykler med k = 5.
- `rho.py` – K–L:s blandningskvot ρ_k för alla certifikat (chunkat, klarar k = 21) och siffer-känslighets-
  profilen 1 − ρ_j per ternär siffra (k ≤ 19, kräver vektorn i RAM som float64). `python rho.py`
- `kl_split.py` – k = 22 på 64 GB: c som tre Metal-buffertar (max_buffer_length 38.9 GiB < 39 GiB), delad int8-kärna
  bitidentisk med make_Q8 (k ≤ 10), topp 1.26 vektorer (49 GiB vid k = 22). `test KMAX`, `lambda K SRC [lam0 lam1]`
  (sparar c_k{K}_part{0,1,2}.npy), `certify K LAMBDA SRC` (trimmar, skriver sammanslagen c_f32.npy via memmap, int64).
- `kl5.py`, `kl5_mlx.py`, `kl5.json` – spår 8: K–L-systemet för 5x+1 (härledning i docstring; generisk residy-LP
  reproducerar tabell 2 för p = 3 och indexformlerna för p = 5). λ_k(5), γ_k(5), ρ_k(5) för k ≤ 13, se AVENUES §8.
- `boundary_layer.py` – spår 1 (2026-10-09): (1) metodens tak: summerade olikheten vid ρ = 1 ⇔ Malthus-ekvationen
  1/λ + λ^(log2 p − 1)/p = 1 för den naiva förgreningsvandringen; 3x+1: λ* = 2, 5x+1: λ* = 1.5701677 (γ* = 0.650919 =
  Kontorovich–Lagarias η_{5,BP}, Thm 8.10) ⇒ 5x+1 är INTE ett fall med känt "λ∞ < tak" (AVENUES §8 rättad);
  (2) gränsskiktet: R(c) = min över toppsiffran (normerad) ger R(c_k) ≈ c_{k−1} (TV 0.0045 vid k = 17, 4× närmare än
  tile), osc_k(d) ≈ Σ_{i<d}(1 − ρ_{k−i}) ⇒ β(d) förklaras till första ordningen av 1 − ρ_k-följden (fel 0.003–0.011).
  `python boundary_layer.py [KMAX]` (k ≤ 11 räknas om med kl.py; < 1 min vid KMAX = 17).
- `.venv/` – Python 3.14, numpy 2.5.3, scipy 1.18.1, mpmath 1.4.1, mlx 0.32.3, matplotlib 3.11.2 (Apple M5, 24 GB)

## Referensvärden (regressionstest – ska reproduceras)
Artikelns tabell 2 (λ_k, C_max):
k=2 1.3534010 1.8317 | k=3 1.5275960 3.4882 | k=4 1.6122870 5.4952 | k=5 1.6627590 9.0756
k=6 1.6944520 12.8769 | k=7 1.7201900 20.1964 | k=8 1.7449630 29.1315 | k=9 1.7615320 43.3394
k=10 1.7771270 64.9801 | k=11 1.7922310 98.4010
Vår implementation stämmer på 6–7 decimaler. Negativt test: `certify.py 4 1.6123` ska ge VERIFIED=False.
Korskontroll (2026-10-07): certify_fast.py (numpy + mlx) och certify.py ger samma utslag för k = 2…14, både för
λ_k avrundat nedåt till 4 decimaler (True) och λ_k + 2e-5 (False). verify_cert.py avvisar manipulerade certifikat
(ändrat C, q + 1, L2 + 1, L1·1.001, höjt λ).
Oberoende LP-implementation (`lp_check.py`, 2026-10-08): λ_k stämmer med tabell 2 inom 1e-6 för k = 2…9
(avvikelser −9e-7 … +9e-7, tabellen har 7 decimaler), exakt rationell verifiering av LP-lösningarna True med slack
1.0e-7, λ_k + 1e-4 otillåtet för alla k. Indexformlerna och λ-värdena är därmed bekräftade av kod utan gemensamt ursprung.
Extern korskontroll (2026-10-08): msharpe248 får 0.895 vid k = 17 (vi 0.8965) och Mazur 0.90/0.901 vid k = 18
(vi 0.9033) med samma LP – tre oberoende implementationer är konsistenta.

## Resultat hittills (certifierade exakt)
| k | N | λ_k numeriskt | λ_cert | γ = log2 λ_cert | certifikat |
|---|---|---|---|---|---|
| 12 | 177 147 | 1.8064236 | 1.8064 | 0.8531 | `certs/k12_1.8064` |
| 13 | 531 441 | 1.8188237 | 1.8188 | 0.8630 | `certs/k13_1.8188` |
| 14 | 1 594 323 | 1.8307723 | 1.8307 | 0.8724 | `certs/k14_1.8307` |
| 15 | 4 782 969 | 1.8419687 | 1.8419 | 0.8812 | `certs/k15_1.8419` |
| 16 | 14 348 907 | 1.8522346 | 1.8522 | 0.8892 | `certs/k16_1.8522` |
| 17 | 43 046 721 | 1.8616888 | 1.8616 | 0.8965 | `certs/k17_1.8616` |
| 18 | 129 140 163 | 1.8703250 | 1.8703 | 0.9033 | `certs/k18_1.8703` |
| 19 | 387 420 489 | 1.8783132 | 1.8783 | 0.9094 | `certs/k19_1.8783` |
| 20 | 1 162 261 467 | 1.8857083 | 1.8857 | 0.9151 | `certs/k20_1.8857` |
| 21 | 3 486 784 401 | 1.8925462 | 1.8925 | 0.9203 | `certs/k21_1.8925` |
| 22 | 10 460 353 203 | 1.8988933 | 1.8988 | 0.9251 | `certs/k22_1.8988` (M4 Pro 64 GB, `kl_split.py`) |
Ökning i γ per steg: 0.0113, 0.0099, 0.0094, 0.0088, 0.0080, 0.0073, 0.0068, 0.0061, 0.0057, 0.0052, 0.0048 (avtagande).
k = 22 (2026-10-08, M4 Pro 64 GB): `kl_split.py lambda 22 c_k21_mlx.npy 1.9005 1.9025` – 3 λ-värden (51 + 40 + 19 min),
110 min totalt, topp 49.0 GiB (1.26 vektorer), λ_22 = 1.8988933 (prognosen från den geometriska anpassningen var
γ_22 = 0.925; utfall 0.92513), Cmax = 9851. Certifiering via `kl_split.py certify 22 1.8988 c_k22_part0.npy`: trim 39 min (int8-golvet 2.5e-6), sammanslagning 90 s, int64-kontroll 290 s, slack 2.40e-5, verify_cert PASS. OBS: "negativt test" vid 1.89888 var FEL VALT (< λ_22 = 1.8988933) och gav True – ett giltigt andra certifikat (slack 3.0e-6, raderat); övre certifikat för k = 22 vid 1.89891 (2026-10-09 00:19): `kl_split.py certify 22 1.89891 … --upper`, trim 2252 s, slack 1.6e-6, verify_cert PASS ⇒ λ_22 ∈ [1.8988, 1.89891].
k = 16 (2026-10-07): λ-sökning 16 s, 240 MB, värmestart från k = 15; certifiering 0.3 s, slack 1.0e-5;
λ = 1.85224 ger VERIFIED=False.
k = 17–21 (2026-10-07, M5 24 GB), sekant med start λ_{k−1} + 0.008 / + 0.010, värmestart från k−1:

| k | λ-sökning | λ-värden | minne | certifiering (numpy / mlx) | minne | slack | negativt test |
|---|---|---|---|---|---|---|---|
| 17 | 18 s | 4 | 0.6 GB | 0.7 s / 0.4 s | 1.9 GB | 2.6e-5 | 1.86172 False |
| 18 | 145 s | 11 | 1.6 GB | 1.9 s / 0.9 s | 4.6 GB | 6.5e-6 | 1.87035 False |
| 19 | 198 s | 5 | 4.7 GB | 6.0 s / 2.6 s | 12.7 GB | 2.9e-6 | 1.87834 False |
| 20 | 161 s | 3 | 10.6 GiB (MLX) | 34 s / 14 s | 10.1 GB | 1.5e-6 | 1.88574 False |
| 21 | 948 s (int8) | 3 | 16.3 GiB (MLX) | 124 s / – | 14.8 GB | 1.1e-5 | 1.89258 False |

k = 20 kördes med den minnessnåla versionen (Metal-kärna, strömmande certifiering, format /2); samma kod ger
k = 19 på 52 s (3 λ-värden) i stället för 198 s.
k = 21 (2026-10-07): int8-vägen (se nedan), 1.8 s/iteration; certifiering bara numpy (MLX-kontrollen klarar
inte N > 2^31) + verify_cert.py. Den geometriska anpassningen förutsade γ_21 = 0.9204 i förväg; utfall 0.9203.
Alla verifierade även med verify_cert.py. Warm-start-vektorer: `c_k{16..21}_mlx.npy` (k = 21: 13 GB, form (3, N/3)).
Disk: certifikat k = 21 13 GB, k = 20 4.3 GB (format /2), k = 19 2.9 GB, k = 18 1 GB (format /1).

## Gränser (varför inte k = 100)
N = 3^(k−1): en float32-vektor är 1.4 GiB (k=19), 4.3 (20), 13 (21), 39 (22), 117 (23), 1 TiB (25),
256 TiB (30), 6e38 GiB (k=100). k = 100 är omöjligt med denna metod på vilken dator som helst.
Dessutom avtar vinsten (Δγ ≈ 0.005/steg, minskar ~8 %/steg) och slacken (1.5e-6 vid k = 20) närmar sig
float32-upplösningen; vid k ≳ 22 behövs float64-polering av c eller λ_cert med större marginal.
Denna maskin (M5, 24 GB; MLX: max_recommended_working_set 17.8 GiB, max_buffer_length 13.3 GiB):
- k = 20: klart (λ-sökning 10.6 GiB, certifiering 10 GB).
- k = 21: klart med int8-vägen (`growth_q8`, väljs automatiskt av `make_growth` när 2 vektorer inte ryms;
  `KL_FORCE_Q8=1` tvingar den för test). Per iteration: kärnan `make_Q8` räknar ρ_i = F(c)_i/c_i exakt i
  float32, min/max per trådgrupp (simd_min/max + threadgroup-minne) och d_i = round((ρ_i − ρ0)/S) som int8,
  ρ0/S från förra iterationen (S = 1.25·(hi − lo)/254); sedan c ← (c/m)(ρ0 + S·d) som kompilerad
  elementvis op som återanvänder c:s buffert. Uppmätt topp 1.26 vektorer (16.3 GiB vid k = 21).
  Lärdomar: (1) MLX återanvänder bara bufferten om c saknar andra referenser när uppdateringen körs –
  evaluera Q först (separat mx.eval), skicka c i en lista som töms, ingen kvarhållen variabel hos anroparen;
  (2) en Python-referenscykel höll kvar ett gammalt d (+0.25 vektor) → `gc.collect()` i början/slutet;
  (3) MLX-shapes är int32: vektorer med N > 2^31 lagras som (3, N/3) (`vec_shape`), även i .npy-filerna;
  (4) lyftet k−1 → k skrivs till disk via numpy-memmap och laddas med mx.load (undviker 4.3 + 13 GiB).
  int8-golvet för hi − lo är ~2e-6 (exakt: ~1.2e-6) och lo blir ~6e-7 lägre → något mindre slack.
  Första iterationen tar ~20 s extra medan macOS swappar ut annat (swap ~7 GB, 10 % fritt minne).
- k = 22 (N = 1.05e10): c 39 GiB + int8 9.8 GiB + partialer 1.2 GiB ≈ 50 GiB → 64 GB-maskin med höjd
  GPU-gräns (`sudo sysctl iogpu.wired_limit_mb=57344`), eller int4-uppdatering (≈ 45 GiB, konvergens otestad).
  Kräver (9, N/9)-shape och ev. uppdelning av c i flera buffertar (max_buffer_length). ~1.5 h.
- k = 23 ≈ 147 GiB (192 GB), k = 24 ≈ 400–440 GiB (512 GB, på gränsen), k ≥ 25 orealistiskt i RAM.
- Korrektionsvektor (c_k ≈ tile(c_{k−1})·(1 + δ)) testad och förkastad: |log δ| median 0.015 men 99 % 0.12
  och max 0.66 (minskar inte med k, inget beroende av översta siffran). Med kravet ~1e-7 relativ precision
  behövs ~24 bitar per element + basvektorn N/3 → mer minne än float32. float32 är nära optimalt; bästa
  tänkbara packning (24-bitars log-fixpunkt) sparar 25 % och ger inget nytt k.
- Certifikatstorleken (13 GB vid k = 21) utesluter kontroll i Lean-kärnan (`decide +kernel`); formell
  verifiering av stora k går bara via `native_decide` + externa verifierare (så gjorde Mazur vid k = 18).

## Blandningskvoten ρ_k och frågan om γ → 1 (`rho.py`, 2026-10-08)
ρ_k = c̄_{k−1,k}/c̄_{k,k} (medel av cbar / medel av c). Den summerade olikheten är tight för våra vektorer
(ρ_k − ρ(λ_cert) ≈ 1–3e-5, skillnaden beror på att λ_cert < λ_k), så λ_k är i praktiken en funktion av ρ_k ensam:
  1 − λ^-2 = (1/3)(λ^(α−1) + λ^(α−2)) ρ.   Vid λ = 2 är båda sidor 3/4 ⇒ λ_k → 2 ⇔ ρ_k → 1.

| k | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 − ρ_k | 0.0573 | 0.0524 | 0.0482 | 0.0443 | 0.0407 | 0.0375 | 0.0347 | 0.0321 | 0.0298 | 0.0277 | 0.0258 | 0.0241 |
| kvot till föregående | 0.913 | 0.913 | 0.920 | 0.919 | 0.920 | 0.922 | 0.924 | 0.927 | 0.928 | 0.930 | 0.931 | 0.933 |

Kvoten stiger monotont (k = 22: ρ_22 = 0.975934 vid λ_cert = 1.8988, `rho.py` 2026-10-08) ⇒ ren geometrisk avklingning passar inte (max residual 5.6e-4). Tre modeller passar
lika bra (max residual ~1e-4, k = 11…21): geometrisk + offset (B = 0.0088 ⇒ ρ∞ = 0.991 ⇒ γ∞ ≈ 0.971),
sträckt exponential (⇒ γ∞ = 1), potenslag (⇒ γ∞ = 1). Data t.o.m. k = 21 kan alltså INTE skilja "metoden
stannar under 1" från "metoden når 1 långsamt". Prognoser för k = 22: 0.925 (alla modeller); k = 30: 0.950–0.960.

Tak och 5x+1 (2026-10-09): ρ ≤ 1 ger λ_k ≤ minsta roten av den summerade olikheten = Malthus-roten för förgrenings-
modellen (3x+1: 2; 5x+1: 2^0.650919 = K–L:s η_{5,BP}). 5x+1 har alltså samma fråga (ρ_k(5) → 1?), inte ett känt nej.
Gränsskiktet β(d) är 1 − ρ_k sett genom grovkorningen R (R(c_k) ≈ c_{k−1}), se `boundary_layer.py`.

Siffer-känslighetsprofil: 1 − ρ_j = 1 − medel(min över siffra j)/medel(c) mäter hur mycket c beror på ternär
siffra j. Den avtar geometriskt i j, snabbare nära toppen (trunkeringseffekt av min). Faktorn i mitten av
profilen (max över j) växer med k: 0.828 (k=12), 0.836, 0.843, 0.849, 0.855, 0.860, 0.864, 0.868 (k=19) –
ökningen per steg halveras ungefär vart fjärde k (0.008 → 0.004), så den ser ut att konvergera mot något r∞ runt
0.89–0.90 < 1. Om r∞ < 1 avtar toppsiffe-känsligheten till slut geometriskt ⇒ ρ_k → 1 ⇒ λ_k → 2 (metoden når
γ = 1 − ε asymptotiskt, men mycket långsamt); om r∞ = 1 är frågan öppen. Det är den rätta observabeln för
frågan om γ∞ – inte γ_k direkt. Heuristik: vid kritikalitet (r(F) = 1) avtar störningar med andra egenvärdet
av lineariseringen; dess beroende av k är obekant.

Gränsobjektet (`holder.py`, k = 12…19, 2026-10-08). Kuloscillation osc_j = 1 − medel över kulor (låga j siffror
fixa) av min/medel; Hölder-exponent β_j = −log_3(osc_{j+1}/osc_j). Fynd:
- Grov skala (j = 1–3) β sjunker med k: 0.143 (k=12), 0.130, 0.118, 0.108, 0.102, 0.096, 0.090, 0.085 (k=19).
  r_mid(k) (riktningsprofilens maxkvot): 0.828 → 0.875, inkrement 0.008 → 0.005; anpassningar ger
  r∞ = 0.939 (geometrisk, maxres 7e-4) / 0.955 (A/k) / 0.904 (A/k²) ⇒ β∞ ≈ 0.04–0.09, möjligen 0.
  Gränsfunktionen är alltså i bästa fall Hölder med mycket liten exponent.
- Universellt gränsskikt: β_j beror bara på avståndet till toppen d = k−1−j för d ≤ 6:
  β = 0.665 (d=1), 0.401, 0.293, 0.232, 0.194 – identiskt för alla k till 3 decimaler. Trunkeringen (min över
  toppsiffran) ger samma form på varje nivå ⇒ renormaliseringsstruktur; det är det renaste nya strukturfaktumet.
- Obegränsad gräns: C_max/C_min växer ~1.52^k (147 vid k=12, 2782 vid k=19), kvantilkvot 99.9 %/50 % växer
  12 → 20, massan i topp-1 % 6.5 % → 9.1 %. Gränsobjektet är inte en begränsad kontinuerlig funktion på Z_3;
  en teori måste arbeta med c ∈ L¹ (eller log c) med singulär toppsvans. Konstanten Δ1 = 1/(4 max c) i
  Thm 2.2 försämras därmed med k, exponenten påverkas inte.
- Gränsolikheten på Z_3 (X = {m ≡ 2 mod 3} med Haarmått): c(m) ≤ λ^-2 c(4m) + λ^(α−2) c((4m−2)/3)·1[m≡2 (9)]
  + λ^(α−1) c((2m−1)/3)·1[m≡8 (9)]. m ↦ 4m bevarar Haar på X; m ↦ (4m−2)/3 resp. (2m−1)/3 är bijektioner från
  X_2 resp. X_8 (mått 1/3 vardera) på X som skalar måttet med 3. Integration ger 1 ≤ λ^-2 + ⅓(λ^(α−2)+λ^(α−1))
  med likhet exakt vid λ = 2 (1/4 + ⅓(3/4 + 3/2) = 1). Vid λ = 2 måste alltså en lösning uppfylla likhet n.ö.:
  ett linjärt egenvärdesproblem för en transferoperator på Z_3. Finit k = samma problem med min-förlusten 1 − ρ_k.

## Trend i γ_k (`plot_gamma.py` → `gamma_trend.png`)
För k ≥ 11 är kvoten mellan successiva ökningar Δγ_k/Δγ_{k−1} ≈ 0.91–0.92 (brusig, ±0.03). Geometrisk anpassning
γ_k ≈ γ∞ − 0.348·0.919^k (k = 11…21): γ∞ ≈ 0.980, max residual 2e-4; anpassad på k ≤ 17 förutsäger den
k = 18–20 med fel 1.5–4e-4 och k = 21 blint med 1e-4. KORRIGERING 2026-10-08: det statistiska felet ±0.001 på
γ∞ är missvisande – modellfelet dominerar, se ρ_k-avsnittet. Påståendet "metoden når inte γ = 1" ska inte göras.
Små k går INTE att fånga med en slät funktion (γ_k är exakt till ~1e-7, residualer ≫ det): testat geometrisk,
geometrisk·potens, två exponentialer, sträckt exponential, förskjuten potens, Padé i 1/k, log-typ och
polynom; alla som tar med k < 11 förutsäger k = 18–20 4–100× sämre, polynom katastrofalt (upp till 1e3).
Residualerna: k = 2–7 en egen geometrisk term (kvot ≈ 0.44, alla negativa), brott vid k = 8–9 (+1.0e-3,
+3.4e-4), k ≥ 11 dämpad svängning ±2e-4 (toppar k = 12, 17). Ingen svängning kopplad till log2 3 (0.415).

## Omvärld 2026 (litteratursökning 2026-10-08, plan punkt 7)
Samma program drivs av flera AI-assisterade Lean-projekt. Alla är orefereegranskade preprints/repos:
- msharpe248/collatz (GitHub): Lean 4, kärnkontrollerat π_1(x) = Ω(x^0.8676) vid k = 14 (1 594 323 klasser som
  729 shards, `decide +kernel`, 29 h, ≤ 37 GB), 0.8569 (k = 13), 0.8476 (k = 12); informellt 0.895 vid k = 17.
  Lägre än våra värden vid samma k p.g.a. "integer-grid weakening" (tak på 1/50-rutnät). Formaliserar
  certifikatinduktionen direkt (ingen Kőnig-eliminering) i stället för att ta Thm 2.2 som axiom.
  Hävdar också "no-go"-satser för begränsade multiplikativa potentialer och att divergenta banor måste ha
  udda-stegsdensitet exakt log 2/log 3.
- ProofAtlas / Lech Mazur (juli 2026): π_a(x) ≥ x^0.90 (och x^0.901) vid k = 18, Lean med `native_decide`
  (två stora nativa kontroller + Python/C++-verifierare), "accepterat" på plattformens egen granskning.
  Samma person hävdar naturlig densitet 1 för nedstigning inom 436·log N steg (annat påstående än Taos log-densitetssats, inte strikt starkare) samt (sep 2026) positiv undre densitet för föregångare – obekräftat, var skeptisk. Litteraturöversikt: `reports/Collatz adjacent work and references.md` (2026-10-08).
- R. A. Tavares, arXiv:2608.27617 (aug 2026): två av Wirschings fem förmodanden (2003) om positiv
  föregångardensitet; förmodan 2 återstår. Wirschings program är "samma fråga en nivå upp": positiv densitet
  för varje a i stället för x^γ.
- Yolcu–Aaronson–Heule, arXiv:2105.14697: Collatz ⇔ terminering av ett strängomskrivningssystem; matris-
  interpretationer via SAT bevisar bara försvagningar. Enda ekvivalenta omformuleringen där GPU/LP-kompetens
  överförs direkt; förväntat utfall negativt resultat, inte bevis.
Slutsats: våra 0.9203 (k = 21) överträffar alla kända anspråk, och tre implementationer stämmer överens vid
samma k. Men för att räknas måste resultatet formaliseras.
Rekognosering av Mazurs ramverk (2026-10-08, källa proofatlas.ai/sources/collatz-predecessor-090, commit 5f76a17):
64 Lean-filer; certifikatet är 32-bitars vikter (516 560 652 byte = 4·N vid k = 18, dvs. samma storlek som vår
float32-vektor) hex-kodade i 16 textchunkar ≤ 64 MiB inlästa med `include_str`, plus en extra "adaptive
potential"-vektor (1 byte/klass, 215 M olikheter) som ersätter K–L:s elimineringsargument (Thm 2.2) – den har vi
inte och måste genereras enligt hans konstruktion. Kontroll via `native_decide`: 18.5 min, 10.6 GiB topp (LP) +
14.6 min, 9.3 GiB (potential) vid k = 18. Linjär skalning ⇒ k = 19 ≈ 32 GiB, k = 20 ≈ 95 GiB, k = 21 ≈ 290 GiB
och ~27 GB hex-text i källträdet. msharpe248 använder `decide +kernel` (29 h vid k = 14) – irrelevant för k ≥ 17.
Slutsats: k = 21 kan inte formaliseras på denna maskin (24 GB) eller med rimlig insats; k = 19 kräver 64 GB,
k = 21 ≥ 384 GB. Realistisk väg: erbjud våra vektorer (k = 19–21) till Mazur/msharpe248 eller kör deras pipeline
på en stor maskin. Ingen Lean-verktygskedja är installerad här (`elan`/`lake` saknas) – inte påbörjat.

## Vad metoden kan och inte kan
- Alla räknemetoder (Terras, Tao, K–L, Wirsching) ger "nästan alla"-utsagor. Även drömutfallet (γ = 1 eller
  positiv densitet för varje a) utesluter inte en enda divergent bana eller en oupptäckt cykel. Cykler kräver
  diofantisk approximation; mot divergenta banor finns inget verktyg alls (Tao: log-densitet 0).
- Conways oavgörbarhet för generaliserade Collatz-avbildningar: varje bevis måste använda 3x+1:s specifika
  aritmetik. Ekvivalenta omformuleringar utan dragkraft: Berg–Meinardus funktionalekvationer, Bernstein–Lagarias
  2-adiska konjugering, omskrivningsterminering (ovan).
- Inom ramen är det öppna matematiska målet λ_k → 2 ⇔ ρ_k → 1 (K–L §6). Det är en fråga om Perron-vektorns
  beroende av översta siffran – mer angripbar än LP:t i sig.

## Idéer att pröva (rangordnade efter värde per insats)
1. ❌ Adaptiv förfining i stället för enhetligt k – TESTAD OCH FÖRKASTAD (2026-10-08, `adaptive.py`, k = 12 och 14).
   Formulering: variabler på löven i ett 3-adiskt träd över i; lövets olikhet G(c)_ℓ = min_{i∈ℓ} F(expand c)_i
   (exakt, giltig relaxation; monoton, 1-homogen). Enhetligt djup k−2 ger λ_{k−1} och djup k−1 ger λ_k exakt
   (7 decimaler) – det validerar koden. Resultat vid k = 14 (andel av vinsten λ_13 → λ_14 mot andel löv av N;
   urval av celler med orakel = spridningen av c_14 över de tre toppsiffrorna, bästa tänkbara urval):

   | träd | löv/N | vinst fångad |
   |---|---|---|
   | förfina 5 / 10 / 25 / 50 / 75 % av cellerna (orakel) | 0.37 / 0.40 / 0.50 / 0.67 / 0.83 | 0.05 / 0.10 / 0.30 / 0.59 / 0.84 |
   | förfina 25 / 50 % slumpmässigt | 0.50 / 0.67 | 0.17 / 0.34 |
   | samma lövbudget som enhetligt djup 12, bas djup 11 + 25 % två nivåer | 0.33 | −0.78 |

   Vinsten är nästan proportionell mot antalet löv (orakel bara marginellt bättre än slump), och vid lika budget
   är ett ojämnt träd klart sämre än ett jämnt (−0.78 steg). k = 12 ger samma bild (0.29 / 0.58 / 0.83; −0.81).
   Spridningen själv är inte koncentrerad (k = 14: median 0.032, 99-percentil 0.11, max 0.30; de 25 % mest
   spridda cellerna står för 46 % av total spridning men bara 30 % av vinsten).
   Slutsats: lösningen behöver alla siffror i alla klasser; antalet variabler är det som räknas. Ingen väg till
   effektivt k > minnet via gles förfining. Stämmer med att korrektionsvektorn är bred (99 % |log δ| < 0.12).
2. Teori för ρ_k: följ den per-siffra-avklingningsfaktorn som funktion av k (k = 12…19 finns), undersök om
   andra egenvärdet av lineariseringen av F förklarar den. Ett bevis för att toppsiffe-känsligheten → 0 ger
   λ_k → 2 och därmed x^(1−ε).
3. k = 22–23 på hyrd maskin (64 resp. 192 GB): ~0.005 i γ per steg, mest värt för trenddata i ρ_k.
4. Formalisering av k = 21-certifikatet (se Omvärld).
5. Starkare olikhetssystem: K–L noterar att L^EL_k (eliminerat system) i princip kan ge mer; testat lika för
   k ≤ 5. Troligen inget att hämta.

## Plan
Klart: 1–4 och 6 (2026-10-07); 5 klart t.o.m. k = 21 (taket på denna maskin); 7a litteratursökning, 7b oberoende
LP, 8 adaptivt träd (negativt), skrivelse `RESULTS.md` och första mätningarna för 9 klara 2026-10-08.
Kvar: 7c (kräver stor maskin eller samarbete), 9 (teori).
1. ✅ Miljö: `pip install numpy scipy mpmath mlx`. Kör regressionstesten ovan (k = 2…11 + negativt test) först.
2. ✅ MLX-port av F (float32 på GPU), utan lagrade indexarrayer (formlerna ovan). Kom ihåg `mx.eval` varje iteration.
   Jämför mot NumPy-versionen för k ≤ 13.
3. ✅ Ersätt bisektion med sekantmetod på λ ↦ log r(F_λ) (3–4 λ-värden räcker), värmestart från lyft k−1-lösning.
4. ✅ (int64, även på GPU) Snabbare rigorös certifiering: int64 med valda skalfaktorer. Behåll den exakta
   Python-heltalsversionen som referens och kör båda för k ≤ 14. Certifieringen körs aldrig i float32.
5. ✅ (t.o.m. k = 21) Kör k = 16, 17, … så långt minnet räcker. k = 22 kräver ≥ 64 GB.
6. ✅ Spara certifikat (λ_cert, heltalsvektor C, undre gränser för potenserna) med sha256 så att andra kan verifiera.
7. Innan något kallas nytt rekord: (a) ✅ litteratursökning – se Omvärld; (b) ✅ oberoende implementation
   (`lp_check.py`, k ≤ 9, exakt rationell verifiering); (c) formalisering i Lean via befintligt ramverk –
   utrett, kräver ≥ 64 GB (k = 19) resp. ≥ 384 GB (k = 21) och Mazurs potentialcertifikat; kontakt med
   Mazur/msharpe248 och ev. Lagarias är nästa steg. Skrivelse: `RESULTS.md`.
8. ✅ Adaptivt-träd-experimentet vid k = 12 och 14 (idé 1) – förkastat, se Idéer punkt 1.
9. ρ_k-teori (idé 2). Mätningarna i `holder.py` är gjorda (se Gränsobjektet). Öppna delfrågor: (i) ✅ gränsskiktet β(d) förklarat till första ordningen
   (2026-10-09, `boundary_layer.py`); kvar: defekten R(F_k(c)) − F_{k−1}(R c) (felriktningen min-av-summa ≥ summa-av-min); (ii) avgör om β∞ > 0 (r∞ < 1) – då är ρ_k → 1 geometriskt och
   γ∞ = 1; (iii) formulera transferoperatorn vid λ = 2 på L¹(X, Haar) och undersök om den har en positiv
   egenfunktion (obegränsad). Uppdatera ρ-tabellen och profilerna när nya k tillkommer (`python rho.py`, `holder.py`).

## Cykelspåret (nytt delprojekt 2026-10-08, Daniels gamla CUDA-idé)
Mål: undre gränser för minsta element / längd hos en icke-trivial cykel, komplementärt till densitetsspåret.
Grund: cykel med n steg, k udda ⇒ 2^n = Π_{udda x_i}(3 + 1/x_i) ⇒ k·log2(1+1/(3M)) ≤ n − kθ ≤ k·log2(1+1/(3m)),
θ = log2 3, m/M = min/max. Minimum m är udda, m ≡ 3 (mod 4), m ≡ 1 eller 5 (mod 6) (multipler av 3 ligger aldrig på
cykler), föregångaren är 2m, efterföljaren (3m+1)/2 är udda. Om alla tal < 2^B når 1 så är m > 2^B och n/k är en övre
rationell approximation av θ med fel ≤ 1/(3·2^B ln 2) → övre semikonvergenter till θ.
- `cycles.py`: reproducerar Eliahou (1993): B = 40 ⇒ n ≥ 17 087 915 (k = 10 781 274) exakt. B = 60 ⇒ n ≥ 630 138 897.
  B = 68 och 71 ⇒ (n, k) = (114 208 327 604, 72 057 431 991) är minsta tillåtna par (fel 1.10e-22); nästa par är
  (217 976 794 617, 137 528 045 312). Att utesluta det första paret kräver med Eliahous grova olikhet 2^B > 4.4e21 ≈ 2^71.9.
- Litteratur: Barina (J. Supercomputing 2025) verifierat till 2^71 (jan 2025). Hercher (JIS 26, 2023, arXiv:2201.00406):
  inga m-cykler med m ≤ 91 (m = antal lokala minima), och verifiering till 3·2^69 räcker för K ≥ 1.375e11 udda steg
  (= nästa par ovan) – alltså är med Barinas 2^71 cykellängden ≥ 2.18e11 steg redan nu. Hercher vinner ~1.3 bitar över
  Eliahous olikhet med struktur (lokala minima).
- `cycle_harmonic.py`: vår första förfining: 1/x_j ≤ 2^{d_j}/m med d_j = j − k_jθ ≤ 0 (banan från m stannar ≥ m),
  d-vandring med steg +1 (jämnt, tillåtet om d+1 ≤ 0) och +1−θ (udda). DP ⇒ max medel av 2^{d} över udda steg
  f = 0.7214 (girig vandring optimal) ⇒ bara 0.47 bitar. Hercher får mer ⇒ läs hans olikhet (pdf i scratchpad/hercher).
- Hur mycket förfining som krävs (vad f i Σ1/x_i ≤ f·k/m måste vara) för att utesluta de tillåtna paren:
  X0 = 2^71: par 1 (1.14e11) kräver f < 0.54 (0.88 bitar – Hercher klarar det, så cykellängd ≥ 2.18e11 är dagens
  läge), par 2 (2.18e11) kräver f < 0.046 (4.4 bitar), par 3 (1.41e12) 7.3 bitar. Varje konvergentsteg kostar ~3.5
  bitar ⇒ frontlinjen flyttas av verifieringen (Barina), inte av förfiningar; 4.4 bitar nås inte med strukturargument.
- Herchers mekanism (Lemma 9): lokalt minimum n_i följt av k_i udda och ≥ 2 jämna steg ⇒ (n_i−1)/2 går in i cykeln
  utanför den ⇒ (n_i−1)/2 > X0 ⇒ n_i > 2X0. Generalisering: varje föregångare w till ett cykelelement med w < m ligger
  utanför cykeln ⇒ w > X0 ⇒ m > X0/c, c = w/m. `cycle_dip.py a b D`: m = r + 2^a3^b·u, framåt a steg (exakta linjära
  former i u), bakåt D steg från varje element, kräver att banan stannar ≥ m. a=8,b=5,D=5: 3078 tillåtna klasser,
  70 % har en off-cycle-föregångare < m (c_min från 0.13 till 0.89, dvs m > 1.1–7.6·X0 för de klasserna), men 30 %
  (918 klasser) har ingen inom djupet ⇒ c* = 1, ingen universell vinst. a=9,b=6,D=6 (3 min): 18 468 klasser, 23 %
  (4284) utan dip, djupaste dip c = 0.088 (m > 11.4·X0). Andelen resistenta klasser sjunker långsamt med djupet. Nästa: viktad (harmonisk) version – man
  behöver inte en universell gräns utan Σ 1/x_i över cykeln; klasser utan dip måste vägas mot sin frekvens längs banan.
- `cycle_lp.py D [--bin h --window W]`: viktad version som LP. Tillstånd (höjdbin, residy mod 3^D), kanter = jämnt/udda
  steg (3-adisk residy deterministisk, paritet fri – exakt modell, CRT), vikt på udda kant min(2^{d_hi}, c(r)) där
  c(r) = min över bakåtvägar (djup ≤ D) av 2^e(2/3)^o (alla föregångare till cykelelement är > X0, på eller utanför
  cykeln). Flödes-LP med udda-andel 1/θ. Resultat: residy-delen mättas vid D ≈ 6: f* = 0.773 (D=6), 0.768 (D=10);
  gemensamt f* = 0.767 (D=7, bin 0.05) ⇒ 0.38 bitar; höjd-LP:t förlorar mot exakt DP (0.72 ⇒ 0.47 bitar) p.g.a. binning.
  Multipler av 3 spelar ingen roll (nås aldrig efter udda steg). Slutsats: residy+höjd-argument av denna typ ger
  högst ~0.4–0.5 bitar.
- Herchers struktur (läst): Sats 27 (analytisk, oberoende av m): Σ T(n_i) ≤ K·(3/4)/X0 ⇒ f = 0.75 ⇒ 0.415 bitar
  (3781·2^60 → 2836·2^60 för att utesluta par 1) – vår exakta höjd-DP (0.72) är marginellt bättre. Korollarium 29
  (beräkning, 5 veckor på 8 kärnor i9): 1536·2^60 = 3·2^69, dvs 1.3 bitar, via fallanalys à la Lemma 26 på block
  (k_i udda, ℓ_i jämna) med exakta linjära former OCH ett avfärdande: om minsta positiva tal i blockets residyklass
  mod 2^j överstiger den behövda gränsen (3781·2^60) räcker den triviala uppskattningen (Lemma 8: k udda steg i rad
  ⇒ n ≡ −1 mod 2^k ⇒ n ≥ 2^k − 1). Det tricket saknar vår LP (den fria pariteten ignorerar att mönster av längd j
  realiseras bara av tal ≡ ρ_j mod 2^j, ρ_j kan vara ≫ X0). Eftersom Barina nått 2^71 > 3·2^69 är par 1 uteslutet:
  dagens läge K ≥ 1.375e11 udda steg, n ≥ 2.18e11. Nästa par kräver X0 ≥ 2^75.05 (grovt) resp. ~2^74 (Hercher-nivå);
  varje extra bit halverar verifieringsjobbet. Möjligt projekt: block-DFS med våra exakta former + höjd/dip-gränser
  + residyavfärdande, parallelliserad (GPU?) – mål 2–3 bitar ⇒ par 2 utesluts med X0 ≈ 2^72–73. Dagar–veckor.
  Vad detta spår inte kan: divergenta banor; och "alla n" kräver Baker-typ gränser som inte sluter sig.

## Principer
- Flyttal hittar kandidater; bara exakt eller rigoröst felbegränsad kontroll räknas som bevis.
- Det matematiska beviset är Krasikov–Lagarias sats 2.2. Bidraget här är beräkningen.
- Extrapolationer i k är modellberoende; uttala inget om γ∞ utan att visa att flera modeller ger samma svar.
- Externa anspråk från AI-genererade/orefereegranskade källor behandlas som data att korskontrollera, inte som fakta.
