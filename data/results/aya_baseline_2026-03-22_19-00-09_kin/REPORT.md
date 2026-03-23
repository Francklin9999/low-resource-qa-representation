# Aya-23-8B Baseline Report — KIN
**Run:** aya_baseline_2026-03-22_19-00-09_kin
**Test samples:** 44
**Language:** kin
**Model:** Aya-23-8B (4-bit quantized)

## Results Summary

### KIN-Side Metrics

| Pipeline | EM | F1 | Semantic Sim |
|----------|----|----|--------------|
| Aya direct (kin) | 0.0682 | 0.1253 | 0.3604 |
| Aya translate-pivot | 0.1591 | 0.3648 | 0.6508 |

### English-Side Metrics (translate-pivot only)

| Pipeline | EM | F1 | Semantic Sim |
|----------|----|----|--------------|
| Aya translate-pivot | 0.1818 | 0.3491 | 0.5852 |

## Sample Predictions

### 248
- **Question:** Grégoire Kayibanda yayoboye u rwanda ryari?
- **Gold (kin):** 1961
- **Aya direct:** 1961 (sim=1.000)
- **Aya pivot (EN):** Grégoire Kayibanda led Rwanda from 1961 to 1973. (sim=0.412)
- **Aya pivot (kin):** Grégoire Kayibanda yayoboye u Rwanda kuva mu mwaka wa 1961 kugeza mu wa 1973. (sim=0.507)

### 109
- **Question:** urwibuto rwa Jenoside rwa Bisesero rwubatswe ryari?
- **Gold (kin):** 1994
- **Aya direct:** 250,000 (sim=0.359)
- **Aya pivot (EN):** The Bisesero Genocide Memorial was built in 2004. (sim=0.311)
- **Aya pivot (kin):** Urwibutso rwa Jenoside rwa Bisesero rwubatswe mu mwaka wa 2004. (sim=0.377)

### 236
- **Question:** Mari Giuseppina Cucciari akomoka hehe?
- **Gold (kin):** Cagliari
- **Aya direct:** Cagliari (sim=1.000)
- **Aya pivot (EN):** Cagliari (sim=1.000)
- **Aya pivot (kin):** Cagliari (sim=1.000)

### 48
- **Question:** Igisirikari cya  Kapu Veri cyitwa gute?
- **Gold (kin):** Ingabo za Capu Veri (), Ingabo za Cabo Veri cyangwa FACV
- **Aya direct:** Cabo Verdean Armed Forces (sim=0.581)
- **Aya pivot (EN):** The Cape Verdean Armed Forces (sim=0.497)
- **Aya pivot (kin):** Ingabo za Cape Verde (sim=0.590)

### 225
- **Question:** jenoside yateguwe igashyirwa no kubikorwa murwanda, yabaye kungoma yande?
- **Gold (kin):** Juvénal Habyarimana
- **Aya direct:** 1994 (sim=0.291)
- **Aya pivot (EN):** Hutu (sim=0.295)
- **Aya pivot (kin):** Abahutu (sim=0.229)

### 110
- **Question:** Mohammed bin Salman Al Saud yarangirije amashuri ye hehe?
- **Gold (kin):** Kaminuza ya King Saud 
- **Aya direct:** Amashuri (sim=0.332)
- **Aya pivot (EN):** King Saud University. (sim=0.884)
- **Aya pivot (kin):** Kaminuza ya King Saud. (sim=0.920)

### 240
- **Question:** perezida wa Repubulika ya Morodoviya atorerwa manda y'imyaka ingahe?
- **Gold (kin):** Imyaka 5
- **Aya direct:** 5 y'inyo (sim=0.762)
- **Aya pivot (EN):** NOT FOUND. (sim=0.305)
- **Aya pivot (kin):** Ntiyigeze aboneka. (sim=0.239)

### 49
- **Question:** Idi Amin Dada amashuri ye yayigiye he?
- **Gold (kin):** Ishuri ry'Abayisilamu muri Bombo
- **Aya direct:** Bombo (sim=0.423)
- **Aya pivot (EN):** Bombo (sim=0.473)
- **Aya pivot (kin):** Bombo (sim=0.423)

### 2
- **Question:** Umurwa mukuru w'u Bugereki ni uwuhe?
- **Gold (kin):** Athens
- **Aya direct:** 3,400 y'atandwa (sim=0.082)
- **Aya pivot (EN):** Athens (sim=1.000)
- **Aya pivot (kin):** Atene (sim=0.953)

### 89
- **Question:** Afurika y'epfo yabonye ubwigenge ryari?
- **Gold (kin):** 31 Gicurasi 1910
- **Aya direct:** 1961 (sim=0.512)
- **Aya pivot (EN):** 1961 (sim=0.492)
- **Aya pivot (kin):** 1961 (sim=0.512)
