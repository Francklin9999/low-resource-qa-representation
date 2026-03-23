# Fine-Tuning Evaluation Report — TWI
**Run:** finetune_2026-03-22_11-11-19_twi
**Test samples:** 71
**Language:** twi

## Results Summary

### English-Side Metrics (isolates QA model quality)

| Pipeline | EM | F1 | Semantic Sim |
|----------|----|----|--------------|
| Base translate-pivot | 0.2254 | 0.4515 | 0.6091 |
| **Fine-tuned translate-pivot** | **0.2676** | **0.5404** | **0.7320** |

### TWI-Side Metrics (end-to-end performance)

| Pipeline | EM | F1 | Semantic Sim |
|----------|----|----|--------------|
| Base translate-pivot | 0.2958 | 0.4187 | 0.6074 |
| **Fine-tuned translate-pivot** | **0.3239** | **0.4934** | **0.7160** |

### Improvement (fine-tuned vs base)

- English EM: +0.0422
- English F1: +0.0889
- English Sim: +0.1229
- TWI EM: +0.0281
- TWI F1: +0.0747
- TWI Sim: +0.1086

## Sample Predictions

### 37
- **Question:** Hena ne mmarahyɛbadwani ma Asewase wɔ afe mpem mmienu ne aduonu mmienu mu?
- **Gold (twi):** Alhaji Mohammed Mubarak Muntaka
- **Gold (EN):** Alhaji Mohammed Mubarak is the first
- **Fine-tuned (EN):** Alhaji Mohammed Muntaka (sim=0.669)
- **Fine-tuned (twi):** Alhaji Mohammed Muntaka (sim=0.927)
- **Base (EN):** NOT FOUND (sim=0.049)
- **Base (twi):** WONNNIM (sim=0.052)

### 142
- **Question:** Dɛn na na Romafo frɛ no Scotland?
- **Gold (twi):** Caledonia
- **Gold (EN):** Caledonia
- **Fine-tuned (EN):** Caledonia (sim=1.000)
- **Fine-tuned (twi):** Kaledonia (sim=0.936)
- **Base (EN):** Caledonia (sim=1.000)
- **Base (twi):** Kaledonia (sim=0.936)

### 112
- **Question:** Oman bɛn so na na Ellen Johnson Sirleaf ye ne ɔmampanyin?
- **Gold (twi):** Liberia
- **Gold (EN):** Liberia and the United States
- **Fine-tuned (EN):** Liberia (sim=0.668)
- **Fine-tuned (twi):** Liberia (sim=1.000)
- **Base (EN):** Liberia (sim=0.668)
- **Base (twi):** Liberia (sim=1.000)

### 189
- **Question:** Ͻmanpanyin bεn aban mu na Condolezza Rice bεyεε Amerika ᴐman kyerεwfo?
- **Gold (twi):** Barack Obama
- **Gold (EN):** Barack Obama and the
- **Fine-tuned (EN):** Barack Obama (sim=0.845)
- **Fine-tuned (twi):** Barack Obama (sim=1.000)
- **Base (EN):** In Colin Powell's tenure did Condoleezza Rice become America's General Secretary. 

NOT FOUND

Explanation: The context provided does not mention Condoleezza Rice becoming "America's General Secretary." Instead, it states that she became the 66th United States Secretary of State. Therefore, the question cannot be answered with the given context. (sim=0.130)
- **Base (twi):** Wɔ Colin Powell bere so no, Condoleezza Rice bɛyɛɛ America Ɔman Nkyerɛwfo. ANHU ANHU: Nsɛm a wɔaka no mu no nka sɛ Condoleezza Rice bɛyɛɛ "America Ɔman Nkyerɛwfo". Mmom no, ɛka sɛ ɔbɛyɛɛ United States Ɔman Nkyerɛwfo a ɔto so 66 no. Enti, ɛnyɛ nsɛm a wɔaka no mu na yebetumi abua asɛmmisa no. (sim=0.160)

### 197
- **Question:** Nigeria Kano Ɔman no fa bɛn na ɛwɔ?
- **Gold (twi):** atifi fam mantam
- **Gold (EN):** northern region
- **Fine-tuned (EN):** The north of the country (sim=0.695)
- **Fine-tuned (twi):** Asase no atifi fam (sim=0.622)
- **Base (EN):** Kano State is located in the northern region of Nigeria. (sim=0.449)
- **Base (twi):** Kano State wɔ Nigeria atifi fam. (sim=0.006)

### 86
- **Question:** Madagascar amanyɔkuw bɛn na Andry Rajoelina da ano?
- **Gold (twi):** abɔfra Malagasies
- **Gold (EN):** child Malagasies
- **Fine-tuned (EN):** Young Malagasies Determined (sim=0.552)
- **Fine-tuned (twi):** Wɔahyɛ Mmabun a Wɔyɛ Malagase (sim=0.340)
- **Base (EN):** Young Malagasies Determined (sim=0.552)
- **Base (twi):** Wɔahyɛ Mmabun a Wɔyɛ Malagase (sim=0.340)

### 194
- **Question:** Mmeae dodow ahe na ɛwɔ Ghana wɔ afe mpem mmienu ne aduonu baako?
- **Gold (twi):** 24
- **Gold (EN):** 24 The Law
- **Fine-tuned (EN):** The answer is 2021 (sim=0.310)
- **Fine-tuned (twi):** Mmuae no yɛ 2021 (sim=0.285)
- **Base (EN):** NOT_FOUND (sim=0.258)
- **Base (twi):** NOT_FOUND (sim=0.309)

### 241
- **Question:** Kurow bεn ne Argentina ahenkurow?
- **Gold (twi):** Buenos Aires
- **Gold (EN):** Buenos Aires and the surrounding area
- **Fine-tuned (EN):** Buenos Aires (sim=0.660)
- **Fine-tuned (twi):** Buenos Aires (sim=1.000)
- **Base (EN):** Buenos Aires (sim=0.660)
- **Base (twi):** Buenos Aires (sim=1.000)

### 328
- **Question:** Ͻman bεn so aduane ne Pozole?
- **Gold (twi):** Mexico
- **Gold (EN):** Mexico
- **Fine-tuned (EN):** Mexico (sim=1.000)
- **Fine-tuned (twi):** Mexico (sim=1.000)
- **Base (EN):** NOT_FOUND (sim=0.292)
- **Base (twi):** NOT_FOUND (sim=0.292)

### 322
- **Question:** Baguafo baahe na wɔwɔ UK mmarahyɛbedwamu?
- **Gold (twi):** 145
- **Gold (EN):** 145 The Kingdom of God
- **Fine-tuned (EN):** The Parliament of the United Kingdom (sim=0.371)
- **Fine-tuned (twi):** United Kingdom Asɛnnibea (sim=0.152)
- **Base (EN):** NOT_FOUND (sim=0.215)
- **Base (twi):** NOT_FOUND (sim=0.296)
