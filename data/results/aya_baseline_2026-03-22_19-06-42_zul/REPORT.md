# Aya-23-8B Baseline Report — ZUL
**Run:** aya_baseline_2026-03-22_19-06-42_zul
**Test samples:** 49
**Language:** zul
**Model:** Aya-23-8B (4-bit quantized)

## Results Summary

### ZUL-Side Metrics

| Pipeline | EM | F1 | Semantic Sim |
|----------|----|----|--------------|
| Aya direct (zul) | 0.0816 | 0.1147 | 0.3572 |
| Aya translate-pivot | 0.0816 | 0.2739 | 0.5772 |

### English-Side Metrics (translate-pivot only)

| Pipeline | EM | F1 | Semantic Sim |
|----------|----|----|--------------|
| Aya translate-pivot | 0.3061 | 0.4996 | 0.6469 |

## Sample Predictions

### 223
- **Question:** Sibangwa yini isifo samarabi ezinjeni?
- **Gold (zul):** lyssaviruses
- **Aya direct:** Rabies (sim=0.499)
- **Aya pivot (EN):** Rabies is caused by bites, including the rabies virus and the lyssa. It is spread when a human infection or infection is infected with saliva, but in most cases rabies can be transmitted from the mouth to the mouth. (sim=0.284)
- **Aya pivot (zul):** Ulaka lubangelwa ukulunywa, kuhlanganise negciwane lobuhlungu kanye ne-lyssa. Lusabalala lapho umuntu etheleleka noma etheleleke ngamanzi, kodwa ezimweni eziningi ubuhlungu bungadluliselwa ngomlomo. (sim=0.193)

### 233
- **Question:** Ngubani owaba umongameli wokuqala wenhlangano ebusayo i-African National Congress?
- **Gold (zul):** Nelson Mandela
- **Aya direct:**  (sim=0.048)
- **Aya pivot (EN):** Nelson Mandela. (sim=0.905)
- **Aya pivot (zul):** UNelson Mandela. (sim=0.850)

### 87
- **Question:** Ingakanani inani lemali yase-UK?
- **Gold (zul):** Isigaxa sephawundi
- **Aya direct:** Pound sterling (sim=0.316)
- **Aya pivot (EN):** The pound sterling. (sim=0.597)
- **Aya pivot (zul):** Ipound sterling. (sim=0.138)

### 196
- **Question:** wayefundisaphi uPitika Ntuli ngesikhathi esekudingisweni e-UK?
- **Gold (zul):** ICamberwell College of Art, Central Saint Martins College of Art and Design, iLondon College of Printing, Middlesex University kanye ne-University of East London
- **Aya direct:** 32 (sim=0.272)
- **Aya pivot (EN):** Pitika Ntuli taught at Camberwell College of Arts, Central Saint Martins College of Art and Design, the London College of Printing, Middlesex University, and the University of East London. (sim=0.861)
- **Aya pivot (zul):** UPitika Ntuli wafundisa eCamberwell College of Arts, eCentral Saint Martins College of Art and Design, eLondon College of Printing, eMiddlesex University naseNyuvesi yaseMpumalanga London. (sim=0.918)

### 222
- **Question:** Mangaki amazwe okukhulunywa kuwo isiBhunu?
- **Gold (zul):** INingizimu Afrika, iNamibia, futhi, ngezinga elincane, iBotswana, iZambia naseZimbabwe.
- **Aya direct:** Afrikaans (sim=0.226)
- **Aya pivot (EN):** 4 (sim=0.046)
- **Aya pivot (zul):** 4 (sim=0.191)

### 40
- **Question:** Wazalelwa kuphi uJoe Slovo?
- **Gold (zul):** Obeliai, Lithuania
- **Aya direct:**  (sim=0.141)
- **Aya pivot (EN):** Obeliai, Lithuania (sim=1.000)
- **Aya pivot (zul):** Obeliai, eLithuania (sim=0.883)

### 207
- **Question:** ubani umkhulu kaClements Kadalie?
- **Gold (zul):** Chiweyu
- **Aya direct:** Lameck Koniwaka Kadali Muwamba (sim=-0.035)
- **Aya pivot (EN):** Chiweyu (sim=1.000)
- **Aya pivot (zul):** UChiweyu (sim=0.876)

### 88
- **Question:** ikuphi ikomkhulu le-Pixar?
- **Gold (zul):** Emeryville, California
- **Aya direct:** Pixar Animation Studios (sim=0.176)
- **Aya pivot (EN):** Emeryville, California (sim=1.000)
- **Aya pivot (zul):** E-Emeryville, eCalifornia (sim=0.905)

### 226
- **Question:** Mingaki imidlalo eyabhalwa uWilliam Shakespeare?
- **Gold (zul):** 39
- **Aya direct:** 39 (sim=1.000)
- **Aya pivot (EN):** 39 (sim=1.000)
- **Aya pivot (zul):** 39 (sim=1.000)

### 179
- **Question:** Ubani umnikazi weTikTok?
- **Gold (zul):** Zhang Yiming
- **Aya direct:** Douyin (sim=0.338)
- **Aya pivot (EN):** ByteDance (sim=0.242)
- **Aya pivot (zul):** I-ByteDance (sim=0.256)
