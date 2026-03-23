# Fine-Tuning Evaluation Report — HAU
**Run:** finetune_2026-03-22_15-53-34_hau
**Test samples:** 45
**Language:** hau

## Results Summary

### English-Side Metrics (isolates QA model quality)

| Pipeline | EM | F1 | Semantic Sim |
|----------|----|----|--------------|
| Base translate-pivot | 0.2889 | 0.4197 | 0.6056 |
| **Fine-tuned translate-pivot** | **0.3778** | **0.5722** | **0.7879** |

### HAU-Side Metrics (end-to-end performance)

| Pipeline | EM | F1 | Semantic Sim |
|----------|----|----|--------------|
| Base translate-pivot | 0.2444 | 0.3445 | 0.5710 |
| **Fine-tuned translate-pivot** | **0.3556** | **0.4326** | **0.7058** |

### Improvement (fine-tuned vs base)

- English EM: +0.0889
- English F1: +0.1525
- English Sim: +0.1823
- HAU EM: +0.1112
- HAU F1: +0.0881
- HAU Sim: +0.1348

## Sample Predictions

### 215
- **Question:** Yaya sunan wurin yawon bude ido da yafi shahara a garin Bauchi?
- **Gold (hau):** Yankari National Park
- **Gold (EN):** Yankari National Park
- **Fine-tuned (EN):** Yankari National Park (sim=1.000)
- **Fine-tuned (hau):** Yankari National Park (sim=1.000)
- **Base (EN):** Yankari National Park (sim=1.000)
- **Base (hau):** Yankari National Park (sim=1.000)

### 86
- **Question:** Ana iya noman kankana a sahara kuwa?
- **Gold (hau):** eh
- **Gold (EN):** Yes, it is
- **Fine-tuned (EN):** Yes Answer the question using only the context. (sim=0.351)
- **Fine-tuned (hau):** E Ka amsa tambayarka ta wajen yin amfani da mahallin kawai. (sim=0.209)
- **Base (EN):** Yes, watermelon can be grown in the desert. (sim=0.346)
- **Base (hau):** Hakika, ana iya girma tangwa a cikin jeji. (sim=0.070)

### 205
- **Question:** Shin akwai masarauta a Faransa?
- **Gold (hau):** a'a
- **Gold (EN):** No, not at all
- **Fine-tuned (EN):** Yes (sim=0.394)
- **Fine-tuned (hau):** Haka ne (sim=0.387)
- **Base (EN):** Yes (sim=0.394)
- **Base (hau):** Haka ne (sim=0.387)

### 39
- **Question:** Yaya sunan yaren mutanen Ghana?
- **Gold (hau):** Turanci
- **Gold (EN):** English
- **Fine-tuned (EN):** English (sim=1.000)
- **Fine-tuned (hau):** Turanci (sim=1.000)
- **Base (EN):** English (sim=1.000)
- **Base (hau):** Turanci (sim=1.000)

### 216
- **Question:** A wace shekara Amruka ta fara tura sojojinta Afghanistan?
- **Gold (hau):** 2001
- **Gold (EN):** 2001
- **Fine-tuned (EN):** 2001 (sim=1.000)
- **Fine-tuned (hau):** Shekarar 2001 (sim=0.797)
- **Base (EN):** NOT_FOUND (sim=0.298)
- **Base (hau):** Ba a samu ba (sim=0.288)

### 87
- **Question:** Wanene magajin Juma al Majid?
- **Gold (hau):** Khalid Juma Al Majid
- **Gold (EN):** Khalid Juma Al Majid
- **Fine-tuned (EN):** Khalid Juma Al Majid (sim=1.000)
- **Fine-tuned (hau):** Khalid Juma Al Majid (sim=1.000)
- **Base (EN):** Khalid Juma Al Majid is his heir. (sim=0.786)
- **Base (hau):** Khalid Juma Al Majid shi ne magajinsa. (sim=0.789)

### 209
- **Question:** A wane watan musulunci musulmai suke zuwa hajji garin Makkah?
- **Gold (hau):** Dhu al-Hijjah
- **Gold (EN):** Dhu al-Hijjah
- **Fine-tuned (EN):** Dhu-Hijjah (sim=0.942)
- **Fine-tuned (hau):** Dhu-Hijjah (sim=0.942)
- **Base (EN):** Dhu-Hijjah (sim=0.942)
- **Base (hau):** Dhu-Hijjah (sim=0.942)

### 179
- **Question:** Shin fuffuken sauro nawa?
- **Gold (hau):** tagwaye ɗaya
- **Gold (EN):** one twin
- **Fine-tuned (EN):** one (sim=0.704)
- **Fine-tuned (hau):** daya (sim=0.402)
- **Base (EN):** 2 (sim=0.409)
- **Base (hau):** 2 (sim=0.266)

### 40
- **Question:** Wanne fim ne ya sami riba mafi yawa a duniya?
- **Gold (hau):** Avatar
- **Gold (EN):** The Avatar
- **Fine-tuned (EN):** Avatar (sim=0.936)
- **Fine-tuned (hau):** Avatar (sim=1.000)
- **Base (EN):** Titanic (sim=0.247)
- **Base (hau):** Titanic (sim=0.237)

### 1
- **Question:** Menene sunan komfuta ta farko?
- **Gold (hau):** ENIAC
- **Gold (EN):** ENIAC
- **Fine-tuned (EN):** ENIAC (sim=1.000)
- **Fine-tuned (hau):** ENIAC (sim=1.000)
- **Base (EN):** ENIAC (sim=1.000)
- **Base (hau):** ENIAC (sim=1.000)
