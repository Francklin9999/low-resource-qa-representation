# Fine-Tuning Evaluation Report — ZUL
**Run:** finetune_2026-03-22_12-30-48_zul
**Test samples:** 49
**Language:** zul

## Results Summary

### English-Side Metrics (isolates QA model quality)

| Pipeline | EM | F1 | Semantic Sim |
|----------|----|----|--------------|
| Base translate-pivot | 0.2857 | 0.4927 | 0.6352 |
| **Fine-tuned translate-pivot** | **0.4286** | **0.6373** | **0.7758** |

### ZUL-Side Metrics (end-to-end performance)

| Pipeline | EM | F1 | Semantic Sim |
|----------|----|----|--------------|
| Base translate-pivot | 0.0816 | 0.2469 | 0.5764 |
| **Fine-tuned translate-pivot** | **0.1429** | **0.3223** | **0.7045** |

### Improvement (fine-tuned vs base)

- English EM: +0.1429
- English F1: +0.1446
- English Sim: +0.1406
- ZUL EM: +0.0613
- ZUL F1: +0.0754
- ZUL Sim: +0.1281

## Sample Predictions

### 223
- **Question:** Sibangwa yini isifo samarabi ezinjeni?
- **Gold (zul):** lyssaviruses
- **Gold (EN):** lyssaviruses
- **Fine-tuned (EN):** The rabies virus (sim=0.601)
- **Fine-tuned (zul):** Igciwane lobuhlungu (sim=0.534)
- **Base (EN):** The rabies virus and saliva of infected dogs. (sim=0.295)
- **Base (zul):** Igciwane lobuhlungu kanye namafutha ezinja ezithathelwe igciwane. (sim=0.220)

### 233
- **Question:** Ngubani owaba umongameli wokuqala wenhlangano ebusayo i-African National Congress?
- **Gold (zul):** Nelson Mandela
- **Gold (EN):** Nelson Mandela
- **Fine-tuned (EN):** Nelson Mandela (sim=1.000)
- **Fine-tuned (zul):** UNelson Mandela (sim=0.944)
- **Base (EN):** Cyril Ramaphosa (sim=0.253)
- **Base (zul):** UCyril Ramaphosa (sim=0.272)

### 87
- **Question:** Ingakanani inani lemali yase-UK?
- **Gold (zul):** Isigaxa sephawundi
- **Gold (EN):** A pound coin
- **Fine-tuned (EN):** The pound (sim=0.716)
- **Fine-tuned (zul):** Ibhokisi (sim=0.437)
- **Base (EN):** The pound sterling (symbol: £) (sim=0.548)
- **Base (zul):** I-pound sterling (isibonakaliso: £) (sim=0.227)

### 196
- **Question:** wayefundisaphi uPitika Ntuli ngesikhathi esekudingisweni e-UK?
- **Gold (zul):** ICamberwell College of Art, Central Saint Martins College of Art and Design, iLondon College of Printing, Middlesex University kanye ne-University of East London
- **Gold (EN):** Camberwell College of Art, Central Saint Martins College of Art and Design, London College of Printing, Middlesex University and the University of East London
- **Fine-tuned (EN):** Cambridge College of Art and Design (sim=0.604)
- **Fine-tuned (zul):** IKambridge College of Art and Design (sim=0.523)
- **Base (EN):** Camberwell College of Art, Central Saint Martins College of Art and Design, the London College of Printing, Middlesex University and the University of East London. (sim=0.981)
- **Base (zul):** ICamberwell College of Art, iCentral Saint Martins College of Art and Design, iLondon College of Printing, iMiddlesex University ne-University of East London. (sim=0.979)

### 222
- **Question:** Mangaki amazwe okukhulunywa kuwo isiBhunu?
- **Gold (zul):** INingizimu Afrika, iNamibia, futhi, ngezinga elincane, iBotswana, iZambia naseZimbabwe.
- **Gold (EN):** South Africa, Namibia, and, to a lesser extent, Botswana, Zambia, and Zimbabwe.
- **Fine-tuned (EN):** South Africa, Namibia (sim=0.614)
- **Fine-tuned (zul):** INingizimu Afrika, iNamibia (sim=0.604)
- **Base (EN):** 3 (sim=0.039)
- **Base (zul):** 3 Ukuqashwa (sim=0.261)

### 40
- **Question:** Wazalelwa kuphi uJoe Slovo?
- **Gold (zul):** Obeliai, Lithuania
- **Gold (EN):** Obeliai, Lithuania
- **Fine-tuned (EN):** Obeliai, Lithuania (sim=1.000)
- **Fine-tuned (zul):** Obeliai, eLithuania (sim=0.883)
- **Base (EN):** Obeliai, Lithuania (sim=1.000)
- **Base (zul):** Obeliai, eLithuania (sim=0.883)

### 207
- **Question:** ubani umkhulu kaClements Kadalie?
- **Gold (zul):** Chiweyu
- **Gold (EN):** Chiweyu
- **Fine-tuned (EN):** Chiweyu (sim=1.000)
- **Fine-tuned (zul):** UChiweyu (sim=0.876)
- **Base (EN):** Chiweyu (sim=1.000)
- **Base (zul):** UChiweyu (sim=0.876)

### 88
- **Question:** ikuphi ikomkhulu le-Pixar?
- **Gold (zul):** Emeryville, California
- **Gold (EN):** Emeryville, California
- **Fine-tuned (EN):** Emeryville, California (sim=1.000)
- **Fine-tuned (zul):** E-Emeryville, eCalifornia (sim=0.905)
- **Base (EN):** Emeryville, California (sim=1.000)
- **Base (zul):** E-Emeryville, eCalifornia (sim=0.905)

### 226
- **Question:** Mingaki imidlalo eyabhalwa uWilliam Shakespeare?
- **Gold (zul):** 39
- **Gold (EN):** 39
- **Fine-tuned (EN):** 39 (sim=1.000)
- **Fine-tuned (zul):** 39 (sim=1.000)
- **Base (EN):** Approximately 39 plays. (sim=0.519)
- **Base (zul):** Cishe imidlalo engama-39. (sim=0.489)

### 179
- **Question:** Ubani umnikazi weTikTok?
- **Gold (zul):** Zhang Yiming
- **Gold (EN):** Zhang Yiming
- **Fine-tuned (EN):** ByteDance (sim=0.242)
- **Fine-tuned (zul):** I-ByteDance (sim=0.256)
- **Base (EN):** ByteDance (sim=0.242)
- **Base (zul):** I-ByteDance (sim=0.256)
