# Aya-23-8B Baseline Report — HAU
**Run:** aya_baseline_2026-03-22_18-57-17_hau
**Test samples:** 45
**Language:** hau
**Model:** Aya-23-8B (4-bit quantized)

## Results Summary

### HAU-Side Metrics

| Pipeline | EM | F1 | Semantic Sim |
|----------|----|----|--------------|
| Aya direct (hau) | 0.1556 | 0.1941 | 0.4499 |
| Aya translate-pivot | 0.2444 | 0.3728 | 0.5405 |

### English-Side Metrics (translate-pivot only)

| Pipeline | EM | F1 | Semantic Sim |
|----------|----|----|--------------|
| Aya translate-pivot | 0.2889 | 0.4686 | 0.6337 |

## Sample Predictions

### 215
- **Question:** Yaya sunan wurin yawon bude ido da yafi shahara a garin Bauchi?
- **Gold (hau):** Yankari National Park
- **Aya direct:** Yankari National Park (sim=1.000)
- **Aya pivot (EN):** Yankari National Park (sim=1.000)
- **Aya pivot (hau):** Yankari National Park (sim=1.000)

### 86
- **Question:** Ana iya noman kankana a sahara kuwa?
- **Gold (hau):** eh
- **Aya direct:** Citrullus lanatus (sim=0.002)
- **Aya pivot (EN):** Watermelons can be grown in desert-like conditions with sufficient water and the right climate. (sim=0.129)
- **Aya pivot (hau):** Ana iya shuka tangwa a yanayin da yake kama da hamada, inda ake samun ruwa da kuma yanayi mai kyau. (sim=0.073)

### 205
- **Question:** Shin akwai masarauta a Faransa?
- **Gold (hau):** a'a
- **Aya direct:** 50 (sim=0.361)
- **Aya pivot (EN):** NOT FOUND. (sim=0.481)
- **Aya pivot (hau):** Ba a same ta ba. (sim=0.187)

### 39
- **Question:** Yaya sunan yaren mutanen Ghana?
- **Gold (hau):** Turanci
- **Aya direct:** Akan (sim=0.440)
- **Aya pivot (EN):** Akan (sim=0.432)
- **Aya pivot (hau):** Akan (sim=0.440)

### 216
- **Question:** A wace shekara Amruka ta fara tura sojojinta Afghanistan?
- **Gold (hau):** 2001
- **Aya direct:**  (sim=0.231)
- **Aya pivot (EN):** 2001 (sim=1.000)
- **Aya pivot (hau):** Shekarar 2001 (sim=0.797)

### 87
- **Question:** Wanene magajin Juma al Majid?
- **Gold (hau):** Khalid Juma Al Majid
- **Aya direct:** Khalid Juma Al Majid (sim=1.000)
- **Aya pivot (EN):** Khalid Juma Al Majid. (sim=0.920)
- **Aya pivot (hau):** Khalid Juma Al Majid. (sim=0.920)

### 209
- **Question:** A wane watan musulunci musulmai suke zuwa hajji garin Makkah?
- **Gold (hau):** Dhu al-Hijjah
- **Aya direct:** Dhu al-Hijjah (sim=1.000)
- **Aya pivot (EN):** Dhu-Hijjah (sim=0.942)
- **Aya pivot (hau):** Dhu-Hijjah (sim=0.942)

### 179
- **Question:** Shin fuffuken sauro nawa?
- **Gold (hau):** tagwaye ɗaya
- **Aya direct:** mosquito (sim=0.339)
- **Aya pivot (EN):** One pair of wings. (sim=0.527)
- **Aya pivot (hau):** Ƙungiya ɗaya na fuka-fuki. (sim=0.180)

### 40
- **Question:** Wanne fim ne ya sami riba mafi yawa a duniya?
- **Gold (hau):** Avatar
- **Aya direct:** $2.8 billion (sim=0.165)
- **Aya pivot (EN):**  (sim=0.130)
- **Aya pivot (hau):** Ƙarƙashin ƙura (sim=0.145)

### 1
- **Question:** Menene sunan komfuta ta farko?
- **Gold (hau):** ENIAC
- **Aya direct:** Komfuta (sim=0.141)
- **Aya pivot (EN):** ENIAC (sim=1.000)
- **Aya pivot (hau):** ENIAC (sim=1.000)
