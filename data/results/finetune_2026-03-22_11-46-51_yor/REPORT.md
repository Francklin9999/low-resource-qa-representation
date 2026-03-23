# Fine-Tuning Evaluation Report — YOR
**Run:** finetune_2026-03-22_11-46-51_yor
**Test samples:** 51
**Language:** yor

## Results Summary

### English-Side Metrics (isolates QA model quality)

| Pipeline | EM | F1 | Semantic Sim |
|----------|----|----|--------------|
| Base translate-pivot | 0.1373 | 0.4090 | 0.5998 |
| **Fine-tuned translate-pivot** | **0.3137** | **0.5287** | **0.7497** |

### YOR-Side Metrics (end-to-end performance)

| Pipeline | EM | F1 | Semantic Sim |
|----------|----|----|--------------|
| Base translate-pivot | 0.1176 | 0.3207 | 0.5906 |
| **Fine-tuned translate-pivot** | **0.2157** | **0.4101** | **0.7019** |

### Improvement (fine-tuned vs base)

- English EM: +0.1764
- English F1: +0.1197
- English Sim: +0.1499
- YOR EM: +0.0981
- YOR F1: +0.0894
- YOR Sim: +0.1113

## Sample Predictions

### 228
- **Question:** Iwe melo ni Thomas Carlyle ti kọ?
- **Gold (yor):** Oogun
- **Gold (EN):** War
- **Fine-tuned (EN):** Thirty Volumes (sim=0.169)
- **Fine-tuned (yor):** Àwọn Àkájọ Ìwé Mẹ́ta (sim=-0.027)
- **Base (EN):** NOT_FOUND (sim=0.176)
- **Base (yor):** ÀWỌN ÀWỌN (sim=0.334)

### 238
- **Question:** Ọjọ wo ni Frank Lampard darapo mo ẹgbẹ agbabọlu Everton gẹgẹ bi akonimọgba?
- **Gold (yor):** 13 ṣẹẹrẹ 2022
- **Gold (EN):** 13 example 2022
- **Fine-tuned (EN):** 31 January 2022 (sim=0.492)
- **Fine-tuned (yor):** 31 January 2022 (sim=0.727)
- **Base (EN):** 31 January 2022 (sim=0.492)
- **Base (yor):** 31 January 2022 (sim=0.727)

### 86
- **Question:** Odun wo ni a bi Victor Samuel Leonard Malu?
- **Gold (yor):** Ọdun 1947
- **Gold (EN):** The year 1947
- **Fine-tuned (EN):** 1947 (sim=0.900)
- **Fine-tuned (yor):** Ọdún 1947 (sim=0.984)
- **Base (EN):** 1947 (sim=0.900)
- **Base (yor):** Ọdún 1947 (sim=0.984)

### 196
- **Question:** Ọdun wo ni a da ilu Sokoto silẹ?
- **Gold (yor):** Ọdun 1976
- **Gold (EN):** 1976 year
- **Fine-tuned (EN):** 1976 (sim=0.923)
- **Fine-tuned (yor):** 1976 (sim=0.951)
- **Base (EN):** 1976 (sim=0.923)
- **Base (yor):** 1976 (sim=0.951)

### 227
- **Question:** ọdun wo ni eré Muvhango jade?
- **Gold (yor):** 1997
- **Gold (EN):** 1997
- **Fine-tuned (EN):** 1997 (sim=1.000)
- **Fine-tuned (yor):** Ọdún 1997 (sim=0.922)
- **Base (EN):** NOT_FOUND (sim=0.355)
- **Base (yor):** ÀWỌN ÀWỌN (sim=0.210)

### 39
- **Question:** Ni gba wo ni cinema agbelewo lati ori fọnran bẹrẹ ni orilẹ ede Naijiria?
- **Gold (yor):** 1960s
- **Gold (EN):** 1960s
- **Fine-tuned (EN):** The 1960s (sim=0.960)
- **Fine-tuned (yor):** Àwọn ọdún 1960 (sim=0.899)
- **Base (EN):** NOT FOUND (sim=0.280)
- **Base (yor):** A Ò Rí I (sim=0.228)

### 212
- **Question:** Apa wo n'ilẹ Adulawo ni orilẹ-ede South Sudan wa?
- **Gold (yor):** ila-oorun afirika
- **Gold (EN):** eastern africa
- **Fine-tuned (EN):** East Africa (sim=0.951)
- **Fine-tuned (yor):** Ìlà Oòrùn Áfíríkà (sim=0.582)
- **Base (EN):** Africa (sim=0.787)
- **Base (yor):** Àríwá (sim=0.550)

### 87
- **Question:** Ijọba tani o si Nyakuron Cultural Centre?
- **Gold (yor):** Abel Alier
- **Gold (EN):** Abel Alier
- **Fine-tuned (EN):** Abel Alier (sim=1.000)
- **Fine-tuned (yor):** Abel Alier (sim=1.000)
- **Base (EN):** Abel Alier's government (sim=0.730)
- **Base (yor):** Ìjọba Abel Alier (sim=0.836)

### 231
- **Question:** Ni ọdun wo ni a bi Bassey Henshaw?
- **Gold (yor):** Ọdun 1943
- **Gold (EN):** The year 1943
- **Fine-tuned (EN):** 1943 May 4 (sim=0.750)
- **Fine-tuned (yor):** 1943 May 4 (sim=0.808)
- **Base (EN):** 1943 (sim=0.907)
- **Base (yor):** 1943 (sim=0.951)

### 178
- **Question:** Kọntinẹẹti wo ni Vietnam wa?
- **Gold (yor):** Asia (Eṣia)
- **Gold (EN):** Asia (Asia)
- **Fine-tuned (EN):** Asia (sim=0.872)
- **Fine-tuned (yor):** Ásíà (sim=0.749)
- **Base (EN):** Asia (sim=0.872)
- **Base (yor):** Ásíà (sim=0.749)
