# Aya-23-8B Baseline Report — TWI
**Run:** aya_baseline_2026-03-22_19-01-45_twi
**Test samples:** 71
**Language:** twi
**Model:** Aya-23-8B (4-bit quantized)

## Results Summary

### TWI-Side Metrics

| Pipeline | EM | F1 | Semantic Sim |
|----------|----|----|--------------|
| Aya direct (twi) | 0.2254 | 0.2786 | 0.4598 |
| Aya translate-pivot | 0.3662 | 0.4873 | 0.6273 |

### English-Side Metrics (translate-pivot only)

| Pipeline | EM | F1 | Semantic Sim |
|----------|----|----|--------------|
| Aya translate-pivot | 0.2817 | 0.5043 | 0.6287 |

## Sample Predictions

### 37
- **Question:** Hena ne mmarahyɛbadwani ma Asewase wɔ afe mpem mmienu ne aduonu mmienu mu?
- **Gold (twi):** Alhaji Mohammed Mubarak Muntaka
- **Aya direct:** Alhaji Mohammed Mubarak Muntaka (sim=1.000)
- **Aya pivot (EN):** Alhaji Mohammed Mubarak Muntaka (sim=0.764)
- **Aya pivot (twi):** Alhaji Mohammed Mubarak Muntaka (sim=1.000)

### 142
- **Question:** Dɛn na na Romafo frɛ no Scotland?
- **Gold (twi):** Caledonia
- **Aya direct:** Caledonia (sim=1.000)
- **Aya pivot (EN):** Caledonia (sim=1.000)
- **Aya pivot (twi):** Kaledonia (sim=0.936)

### 112
- **Question:** Oman bɛn so na na Ellen Johnson Sirleaf ye ne ɔmampanyin?
- **Gold (twi):** Liberia
- **Aya direct:** 24th (sim=0.304)
- **Aya pivot (EN):** Liberia (sim=0.668)
- **Aya pivot (twi):** Liberia (sim=1.000)

### 189
- **Question:** Ͻmanpanyin bεn aban mu na Condolezza Rice bεyεε Amerika ᴐman kyerεwfo?
- **Gold (twi):** Barack Obama
- **Aya direct:** Republican Party (sim=0.278)
- **Aya pivot (EN):**  (sim=0.219)
- **Aya pivot (twi):**  (sim=0.155)

### 197
- **Question:** Nigeria Kano Ɔman no fa bɛn na ɛwɔ?
- **Gold (twi):** atifi fam mantam
- **Aya direct:** Northern Region (sim=0.095)
- **Aya pivot (EN):** Kano State is located in the northern region of Nigeria. (sim=0.449)
- **Aya pivot (twi):** Kano State wɔ Nigeria atifi fam. (sim=0.006)

### 86
- **Question:** Madagascar amanyɔkuw bɛn na Andry Rajoelina da ano?
- **Gold (twi):** abɔfra Malagasies
- **Aya direct:** na (sim=0.100)
- **Aya pivot (EN):** Young Malagasies Determined (sim=0.552)
- **Aya pivot (twi):** Wɔahyɛ Mmabun a Wɔyɛ Malagase (sim=0.340)

### 194
- **Question:** Mmeae dodow ahe na ɛwɔ Ghana wɔ afe mpem mmienu ne aduonu baako?
- **Gold (twi):** 24
- **Aya direct:** Akan (sim=0.307)
- **Aya pivot (EN):** NOT FOUND (sim=0.250)
- **Aya pivot (twi):** WONNNIM (sim=0.317)

### 241
- **Question:** Kurow bεn ne Argentina ahenkurow?
- **Gold (twi):** Buenos Aires
- **Aya direct:** 16th century (sim=0.167)
- **Aya pivot (EN):** Buenos Aires (sim=0.660)
- **Aya pivot (twi):** Buenos Aires (sim=1.000)

### 328
- **Question:** Ͻman bεn so aduane ne Pozole?
- **Gold (twi):** Mexico
- **Aya direct:** Mesoamerica (sim=0.669)
- **Aya pivot (EN):** Mexico (sim=1.000)
- **Aya pivot (twi):** Mexico (sim=1.000)

### 322
- **Question:** Baguafo baahe na wɔwɔ UK mmarahyɛbedwamu?
- **Gold (twi):** 145
- **Aya direct:** 6 May 2021 (sim=0.105)
- **Aya pivot (EN):** NOT FOUND. (sim=0.145)
- **Aya pivot (twi):** Wannya. (sim=0.321)
