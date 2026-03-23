# Aya-23-8B Baseline Report — BEM
**Run:** aya_baseline_2026-03-22_18-51-02_bem
**Test samples:** 47
**Language:** bem
**Model:** Aya-23-8B (4-bit quantized)

## Results Summary

### BEM-Side Metrics

| Pipeline | EM | F1 | Semantic Sim |
|----------|----|----|--------------|
| Aya direct (bem) | 0.1915 | 0.2401 | 0.4373 |
| Aya translate-pivot | 0.2128 | 0.3181 | 0.4896 |

### English-Side Metrics (translate-pivot only)

| Pipeline | EM | F1 | Semantic Sim |
|----------|----|----|--------------|
| Aya translate-pivot | 0.2128 | 0.3385 | 0.5447 |

## Sample Predictions

### 99
- **Question:** Nani walembele ubuuku lya mubaibolo ilya kusokolola?
- **Gold (bem):** Yohane
- **Aya direct:** Ubuuku lya mubaibolo ilya kusokolola (sim=-0.033)
- **Aya pivot (EN):** The author names himself as 'John' in the text. (sim=0.427)
- **Aya pivot (bem):** Mulembi aliilandila ukuti ni 'Yohane' muli ili lembo. (sim=0.394)

### 214
- **Question:** Bushe ukulingana na FIFA ranking Tanzania yaba pa namba shani mu afrika?
- **Gold (bem):** 90th
- **Aya direct:** 97 (sim=0.574)
- **Aya pivot (EN):** NOT FOUND. (sim=0.309)
- **Aya pivot (bem):** TWALISHILA. (sim=0.217)

### 224
- **Question:** Bushe miku inga icalo ca Nigeria casendepo icikombe ca Afrika cup?
- **Gold (bem):** katatu
- **Aya direct:** 1980 (sim=0.231)
- **Aya pivot (EN):** 3 (sim=0.560)
- **Aya pivot (bem):** 3 (sim=0.586)

### 87
- **Question:** Bushe lunshi ekala inshiku shinga?
- **Gold (bem):** Inshiku shibili ukufika kuli shine
- **Aya direct:** Musca domestica (sim=0.041)
- **Aya pivot (EN):** The life span of a housefly varies, but it typically ranges from a few weeks to several months. The lifespan is influenced by environmental factors, lifestyle, and species. (sim=0.225)
- **Aya pivot (bem):** Ubumi bwa nsumbu bwalipusanapusana, lelo ilingi line bwaba pa milungu iinono nelyo imyeshi iingi. (sim=0.024)

### 213
- **Question:** Bushe kakansha wa mupila uwe bumba lya Realmadrid nani?
- **Gold (bem):** Carlo Ancelotti
- **Aya direct:** Carlo Ancelotti (sim=1.000)
- **Aya pivot (EN):** Carlo Ancelotti (sim=1.000)
- **Aya pivot (bem):** Ba Carlo Ancelotti (sim=0.951)

### 39
- **Question:** Bushe Kateya wamupila Leon Messi afuma ku caalo nshi?
- **Gold (bem):** Argentina
- **Aya direct:** Leo Messi (sim=0.120)
- **Aya pivot (EN):** Argentina (sim=1.000)
- **Aya pivot (bem):** Argentina (sim=1.000)

### 196
- **Question:** Nani kakansha we bumba lya mupila ilya calo ca Dennmark?
- **Gold (bem):** Kasper Hjulmand
- **Aya direct:** Kasper Hjulmand (sim=1.000)
- **Aya pivot (EN):** Kasper Hjulmand. (sim=0.893)
- **Aya pivot (bem):** Ba Kasper Hjulmand. (sim=0.809)

### 88
- **Question:** Bushe pakutendeka ifibanda fyali ni ba malaika bakwa Lesa?
- **Gold (bem):** Ee
- **Aya direct:** Malaika wana wana wafanya kufanya kufanya kwa wote wana wana wana wana wana wana wana wana wana wana wana wana wana wana wana wana wana wana wana wana wana wana wana wana wana wana wana wana wana wana wana wana wana wana wana wana wana wana wana wana wana wana wana wana wana wana wana wana wana wana wana wana wana wana w (sim=-0.005)
- **Aya pivot (EN):** NOT FOUND. (sim=0.232)
- **Aya pivot (bem):** TWALISHILA. (sim=0.131)

### 217
- **Question:** Bushe icalo ca zambia cakwata ama boma yanga?
- **Gold (bem):** 116
- **Aya direct:** 10 (sim=0.511)
- **Aya pivot (EN):** 116 (sim=0.835)
- **Aya pivot (bem):** 116 (sim=1.000)

### 181
- **Question:** Bushe ninani walashikwa bu minister mu ciputulwa cisopa umutende mu zambia?
- **Gold (bem):** Grey Zulu
- **Aya direct:** Grey Zulu (sim=1.000)
- **Aya pivot (EN):** NOT FOUND. (sim=0.193)
- **Aya pivot (bem):** TWALISHILA. (sim=0.160)
