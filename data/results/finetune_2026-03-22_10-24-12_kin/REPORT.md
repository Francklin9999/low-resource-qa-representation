# Fine-Tuning Evaluation Report — KIN
**Run:** finetune_2026-03-22_10-24-12_kin
**Test samples:** 44
**Language:** kin

## Results Summary

### English-Side Metrics (isolates QA model quality)

| Pipeline | EM | F1 | Semantic Sim |
|----------|----|----|--------------|
| Base translate-pivot | 0.1136 | 0.3015 | 0.5291 |
| **Fine-tuned translate-pivot** | **0.1364** | **0.3655** | **0.6181** |

### KIN-Side Metrics (end-to-end performance)

| Pipeline | EM | F1 | Semantic Sim |
|----------|----|----|--------------|
| Base translate-pivot | 0.1136 | 0.2747 | 0.5750 |
| **Fine-tuned translate-pivot** | **0.1136** | **0.3392** | **0.6734** |

### Improvement (fine-tuned vs base)

- English EM: +0.0228
- English F1: +0.0640
- English Sim: +0.0890
- KIN EM: +0.0000
- KIN F1: +0.0645
- KIN Sim: +0.0984

## Sample Predictions

### 248
- **Question:** Grégoire Kayibanda yayoboye u rwanda ryari?
- **Gold (kin):** 1961
- **Gold (EN):** 1961 The
- **Fine-tuned (EN):** November 1959 (sim=0.544)
- **Fine-tuned (kin):** Ugushyingo 1959 (sim=0.637)
- **Base (EN):** NOT FOUND (sim=0.277)
- **Base (kin):** Ntiyigeze aboneka (sim=0.283)

### 109
- **Question:** urwibuto rwa Jenoside rwa Bisesero rwubatswe ryari?
- **Gold (kin):** 1994
- **Gold (EN):** 1994
- **Fine-tuned (EN):** 1994 (sim=1.000)
- **Fine-tuned (kin):** 1994 (sim=1.000)
- **Base (EN):** NOT_FOUND (sim=0.369)
- **Base (kin):** NTIYARONZE (sim=0.335)

### 236
- **Question:** Mari Giuseppina Cucciari akomoka hehe?
- **Gold (kin):** Cagliari
- **Gold (EN):** Cagliari
- **Fine-tuned (EN):** Cagliari, Sardinia, Italy (sim=0.648)
- **Fine-tuned (kin):** Cagliari, muri Saridiniya, mu Butaliyani (sim=0.716)
- **Base (EN):** Cagliari (sim=1.000)
- **Base (kin):** Cagliari (sim=1.000)

### 48
- **Question:** Igisirikari cya  Kapu Veri cyitwa gute?
- **Gold (kin):** Ingabo za Capu Veri (), Ingabo za Cabo Veri cyangwa FACV
- **Gold (EN):** Capu Veri forces, Cabo Veri forces or FACV
- **Fine-tuned (EN):** The Cape Verdean Armed Forces (sim=0.497)
- **Fine-tuned (kin):** Ingabo za Cape Verde (sim=0.590)
- **Base (EN):** National Guard (sim=0.216)
- **Base (kin):** Umurinda w'Igihugu (sim=0.197)

### 225
- **Question:** jenoside yateguwe igashyirwa no kubikorwa murwanda, yabaye kungoma yande?
- **Gold (kin):** Juvénal Habyarimana
- **Gold (EN):** The young man
- **Fine-tuned (EN):** Juvénal Habyarimana (sim=0.256)
- **Fine-tuned (kin):** Juvénal Habyarimana (sim=0.970)
- **Base (EN):** The genocide was planned and carried out under the reign of Juvénal Habyarimana. (sim=0.101)
- **Base (kin):** Jenoside yateguwe kandi ikorwa ku ngoma ya Juvénal Habyarimana. (sim=0.586)

### 110
- **Question:** Mohammed bin Salman Al Saud yarangirije amashuri ye hehe?
- **Gold (kin):** Kaminuza ya King Saud 
- **Gold (EN):** King Saud University 
- **Fine-tuned (EN):** King Saud University (sim=1.000)
- **Fine-tuned (kin):** Kaminuza ya King Saud (sim=1.000)
- **Base (EN):** King Saud University (sim=1.000)
- **Base (kin):** Kaminuza ya King Saud (sim=1.000)

### 240
- **Question:** perezida wa Repubulika ya Morodoviya atorerwa manda y'imyaka ingahe?
- **Gold (kin):** Imyaka 5
- **Gold (EN):** 5 years
- **Fine-tuned (EN):** eighteen years (sim=0.552)
- **Fine-tuned (kin):** imyaka cumi n'umunani (sim=0.508)
- **Base (EN):** NOT_FOUND (sim=0.388)
- **Base (kin):** NTIYARONZE (sim=0.343)

### 49
- **Question:** Idi Amin Dada amashuri ye yayigiye he?
- **Gold (kin):** Ishuri ry'Abayisilamu muri Bombo
- **Gold (EN):** Islamic School in Bombo
- **Fine-tuned (EN):** Bombo (sim=0.473)
- **Fine-tuned (kin):** Bombo (sim=0.423)
- **Base (EN):** Amin joined an Islamic school in Bombo. (sim=0.702)
- **Base (kin):** Amin yiga mu ishuri ry'Abisilamu ry'i Bombo. (sim=0.562)

### 2
- **Question:** Umurwa mukuru w'u Bugereki ni uwuhe?
- **Gold (kin):** Athens
- **Gold (EN):** Athens
- **Fine-tuned (EN):** Athens (sim=1.000)
- **Fine-tuned (kin):** Atene (sim=0.953)
- **Base (EN):** Athens (sim=1.000)
- **Base (kin):** Atene (sim=0.953)

### 89
- **Question:** Afurika y'epfo yabonye ubwigenge ryari?
- **Gold (kin):** 31 Gicurasi 1910
- **Gold (EN):** 31 May 1910
- **Fine-tuned (EN):** May 31, 1910 (sim=0.987)
- **Fine-tuned (kin):** Tariki ya 31 Gicurasi 1910 (sim=0.981)
- **Base (EN):** 1934 (sim=0.484)
- **Base (kin):** 1934 (sim=0.509)
