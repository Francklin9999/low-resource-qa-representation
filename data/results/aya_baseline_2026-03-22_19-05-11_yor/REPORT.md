# Aya-23-8B Baseline Report — YOR
**Run:** aya_baseline_2026-03-22_19-05-11_yor
**Test samples:** 51
**Language:** yor
**Model:** Aya-23-8B (4-bit quantized)

## Results Summary

### YOR-Side Metrics

| Pipeline | EM | F1 | Semantic Sim |
|----------|----|----|--------------|
| Aya direct (yor) | 0.2157 | 0.2582 | 0.4449 |
| Aya translate-pivot | 0.1765 | 0.3692 | 0.5935 |

### English-Side Metrics (translate-pivot only)

| Pipeline | EM | F1 | Semantic Sim |
|----------|----|----|--------------|
| Aya translate-pivot | 0.2549 | 0.4880 | 0.6293 |

## Sample Predictions

### 228
- **Question:** Iwe melo ni Thomas Carlyle ti kọ?
- **Gold (yor):** Oogun
- **Aya direct:** Works in Thirty Volumes (sim=-0.001)
- **Aya pivot (EN):** NOT FOUND. (sim=0.188)
- **Aya pivot (yor):** A Ò Rí I. (sim=0.217)

### 238
- **Question:** Ọjọ wo ni Frank Lampard darapo mo ẹgbẹ agbabọlu Everton gẹgẹ bi akonimọgba?
- **Gold (yor):** 13 ṣẹẹrẹ 2022
- **Aya direct:** 31 January 2022 (sim=0.727)
- **Aya pivot (EN):** 31 January 2022. (sim=0.435)
- **Aya pivot (yor):** 31 January 2022. (sim=0.638)

### 86
- **Question:** Odun wo ni a bi Victor Samuel Leonard Malu?
- **Gold (yor):** Ọdun 1947
- **Aya direct:** Oda (sim=0.206)
- **Aya pivot (EN):** 1947 (sim=0.900)
- **Aya pivot (yor):** Ọdún 1947 (sim=0.984)

### 196
- **Question:** Ọdun wo ni a da ilu Sokoto silẹ?
- **Gold (yor):** Ọdun 1976
- **Aya direct:** Odu ninu Sokoto silẹ (sim=0.136)
- **Aya pivot (EN):** 1976 (sim=0.923)
- **Aya pivot (yor):** 1976 (sim=0.951)

### 227
- **Question:** ọdun wo ni eré Muvhango jade?
- **Gold (yor):** 1997
- **Aya direct:** SA (sim=0.293)
- **Aya pivot (EN):** NOT FOUND (sim=0.343)
- **Aya pivot (yor):** A Ò Rí I (sim=0.245)

### 39
- **Question:** Ni gba wo ni cinema agbelewo lati ori fọnran bẹrẹ ni orilẹ ede Naijiria?
- **Gold (yor):** 1960s
- **Aya direct:** Oga (sim=0.206)
- **Aya pivot (EN):** The question context does not mention the start of watching movies on cassette in Nigeria. (sim=0.163)
- **Aya pivot (yor):** Àwọn ẹsẹ tó wà nínú ìbéèrè yìí kò sọ bí fíìmù ṣe bẹ̀rẹ̀ sí í wà lórí fóònù lóríṣiríṣi ní Nàìjíríà. (sim=0.127)

### 212
- **Question:** Apa wo n'ilẹ Adulawo ni orilẹ-ede South Sudan wa?
- **Gold (yor):** ila-oorun afirika
- **Aya direct:** Adulawo ni orilẹ-ede South Sudan wa ni ọbọ ọbọ-ọbọ-ọbọ-ọbọ-ọbọ-ọbọ-ọbọ-ọbọ-ọbọ-ọbọ-ọbọ-ọbọ-ọbọ-ọbọ-ọbọ-ọbọ-ọbọ-ọbọ-ọbọ-ọbọ-ọbọ-ọbọ-ọbọ-ọbọ-ọbọ-ọbọ-ọbọ-ọ (sim=0.295)
- **Aya pivot (EN):** South Sudan is located in East Africa. (sim=0.535)
- **Aya pivot (yor):** Gúúsù Súdàn wà ní Ìlà Oòrùn Áfíríkà. (sim=0.394)

### 87
- **Question:** Ijọba tani o si Nyakuron Cultural Centre?
- **Gold (yor):** Abel Alier
- **Aya direct:** 1976 (sim=0.246)
- **Aya pivot (EN):** Abel Alier's government. (sim=0.668)
- **Aya pivot (yor):** Ìjọba Abel Alier. (sim=0.753)

### 231
- **Question:** Ni ọdun wo ni a bi Bassey Henshaw?
- **Gold (yor):** Ọdun 1943
- **Aya direct:** Oron (sim=0.368)
- **Aya pivot (EN):** 1943 (sim=0.907)
- **Aya pivot (yor):** 1943 (sim=0.951)

### 178
- **Question:** Kọntinẹẹti wo ni Vietnam wa?
- **Gold (yor):** Asia (Eṣia)
- **Aya direct:** Kọntinẹẹti wo ni Vietnam wa (sim=0.197)
- **Aya pivot (EN):** Southeast Asia (sim=0.738)
- **Aya pivot (yor):** Gúúsù Ìlà Oòrùn Éṣíà (sim=0.438)
