# Aya-23-8B Baseline Report — FON
**Run:** aya_baseline_2026-03-22_18-52-59_fon
**Test samples:** 57
**Language:** fon
**Model:** Aya-23-8B (4-bit quantized)

## Results Summary

### FON-Side Metrics

| Pipeline | EM | F1 | Semantic Sim |
|----------|----|----|--------------|
| Aya direct (fon) | 0.0526 | 0.1083 | 0.3303 |
| Aya translate-pivot | 0.1754 | 0.2210 | 0.4291 |

### English-Side Metrics (translate-pivot only)

| Pipeline | EM | F1 | Semantic Sim |
|----------|----|----|--------------|
| Aya translate-pivot | 0.1930 | 0.3393 | 0.4938 |

## Sample Predictions

### 151
- **Question:** E tɛ nyí "assemblée monocamérale" ?
- **Gold (fon):** système parlementaire e ɖo xɔ̀ ɖokpo
- **Aya direct:** Moncamérisme (sim=0.155)
- **Aya pivot (EN):** A single-camera meeting is a type of meeting where all participants are able to see and hear each other, and can communicate directly with each other, without the need for a moderator or facilitator. (sim=0.421)
- **Aya pivot (fon):** Kplé ɖé mɛ e nɔ ɖó kamera ɖokpo é nyí kplé ɖé mɛ e mɛ ɖò kplé ɔ mɛ lɛ bǐ nɔ mɔ nǔ, nɔ se nǔ, bo nɔ kpéwú dó ɖɔ xó xá yěɖée tẽe, bɔ nǔ byɔ́ ɖɔ è kún ɖó nǔɖokponɔ alǒ mɛɖokponɔ ɖé ó. (sim=0.191)

### 93
- **Question:** E tɛ nyĭ Polio?
- **Gold (fon):** azɔn é nɔn jεmεjí ɖo poliovirus wú
- **Aya direct:** Poliomyélite (sim=0.424)
- **Aya pivot (EN):** Polio is an infectious disease caused by the poliovirus, which is transmitted through the digestive tract and can lead to paralysis and respiratory issues. (sim=0.621)
- **Aya pivot (fon):** Polio ɔ nyí azɔn ɖé bɔ è nɔ dɔn dó azɔn gbɔ nú mɛ ɖó azɔn gbɔ nú mɛ ɖó azɔn gbɔ nú mɛ ɖó azɔn gbɔ nú mɛ ɖó azɔn gbɔ nú mɛ ɖó azɔn gbɔ nú mɛ ɖó azɔn gbɔ nú mɛ ɖó azɔn gbɔ nú mɛ ɖó azɔn gbɔ nú mɛ ɖó azɔn gbɔ nú mɛ ɖó azɔn gbɔ nú mɛ ɖó azɔn gbɔ nú mɛ ɖó azɔn gbɔ nú mɛ ɖó azɔn gbɔ nú mɛ ɖó azɔn gbɔ nú mɛ ɖó azɔn gbɔ nú mɛ ɖó azɔn gbɔ nú mɛ ɖó azɔn gbɔ nú mɛ ɖó azɔn gbɔ nú mɛ ɖó azɔn gbɔ nú mɛ ɖó azɔn gbɔ nú mɛ ɖó azɔn gbɔ nú mɛ ɖó azɔn gbɔ nú mɛ ɖó azɔn gbɔ nú mɛ ɖó azɔn gbɔ nú mɛ ɖó azɔn gbɔ nú mɛ ɖó azɔn gbɔ nú mɛ ɖó azɔn gbɔ nú mɛ ɖó azɔn gbɔ nú mɛ ɖó azɔn gbɔ nú mɛ. (sim=0.319)

### 225
- **Question:** Tò tɛ ɖo Aksoum sín ayìkúngban xóxó ɔ jí ?
- **Gold (fon):** Éthiopie, Djibouti kpódó Érythrée kpán
- **Aya direct:** ɔ́sɔm (sim=0.078)
- **Aya pivot (EN):** Ethiopia, Djibouti, and present-day Eritrea (sim=0.920)
- **Aya pivot (fon):** Etiopíi, Djibouti, kpo Eritreya égbé tɔn kpo (sim=0.888)

### 231
- **Question:** Hwe tɛ nu Allemagne nɔ̀n ɖù tó xwe tɔ̀n ?
- **Gold (fon):** azǎn atɔn gɔ kɔnyasùn tɔn
- **Aya direct:** 3 octobre (sim=0.302)
- **Aya pivot (EN):** 3 October. (sim=0.356)
- **Aya pivot (fon):** azǎn 3 octobre. (sim=0.294)

### 162
- **Question:** Nɛ̌ ahwan Algerie tɔ̀n vɔ̀ gbɔn ɖŏ 1962 ?
- **Gold (fon):** mεɖésúsínínɔ glegbεtá tɔn
- **Aya direct:** 1954-1962 (sim=0.168)
- **Aya pivot (EN):** The Algerian War ended in 1962 with the recognition of the independence of the Algerian territory. (sim=0.154)
- **Aya pivot (fon):** Algejianu ɔ fó ɖò 1962 hwenu e Algejianu lɛ́ɛ yí gbe ɖɔ to ɔ́ ɖò tuto jí é. (sim=0.164)

### 165
- **Question:** Nɛ̌ Archevêque archidiocèse Ouagadougou tɔ́n yɔyɔ ɔ́ nɔ̀n nyi ?
- **Gold (fon):** Compaoré
- **Aya direct:** 10 juin 1995-13 mai 2009 (sim=0.152)
- **Aya pivot (EN):** NOT FOUND (sim=0.325)
- **Aya pivot (fon):** È ma mɔ ǎ (sim=0.245)

### 217
- **Question:** Tó tɛ blŏ protectorat ?
- **Gold (fon):** France
- **Aya direct:** La France (sim=0.925)
- **Aya pivot (EN):** France. (sim=0.827)
- **Aya pivot (fon):** Fransi. (sim=0.620)

### 76
- **Question:** Mɛ nyĭ pop jí tɔ ɖaxó gbɛ ɔ mɛ tɔ̀n ?
- **Gold (fon):** Michael Jackson
- **Aya direct:** The King of Pop (sim=0.292)
- **Aya pivot (EN):** Michael Jackson (sim=1.000)
- **Aya pivot (fon):** Michael Jackson (sim=1.000)

### 145
- **Question:** Mɛ nyi Pipi Wobaho ?
- **Gold (fon):** hanjitɔ́‚ manahὲn e go sín Bénin
- **Aya direct:** Simplice Behanzin (sim=0.256)
- **Aya pivot (EN):** Pipi Wobaho is a comedian and singer of traditional music from Benin. (sim=0.511)
- **Aya pivot (fon):** Pipi Wobaho nyí nùɖíɖóɖókpɔ́tɔ́ ɖé, bó nyí ɖɛ̌tɔ́ nú nùɖíɖó klisanwun tɔn ɖé bɔ è wá Benín. (sim=0.400)

### 20
- **Question:** É tɛ nyi xɔgbonú Benε tɔn ?
- **Gold (fon):** Porto-Novo
- **Aya direct:** Benin (sim=0.330)
- **Aya pivot (EN):** Porto-Novo (sim=1.000)
- **Aya pivot (fon):** Porto-Novo (sim=1.000)
