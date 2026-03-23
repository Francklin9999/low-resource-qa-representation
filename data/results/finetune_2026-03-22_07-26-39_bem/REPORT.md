# Fine-Tuning Evaluation Report — BEM
**Run:** finetune_2026-03-22_07-26-39_bem
**Test samples:** 47
**Language:** bem

## Results Summary

### English-Side Metrics (isolates QA model quality)

| Pipeline | EM | F1 | Semantic Sim |
|----------|----|----|--------------|
| Base translate-pivot | 0.1702 | 0.3280 | 0.5759 |
| **Fine-tuned translate-pivot** | **0.3191** | **0.4645** | **0.6614** |

### BEM-Side Metrics (end-to-end performance)

| Pipeline | EM | F1 | Semantic Sim |
|----------|----|----|--------------|
| Base translate-pivot | 0.1915 | 0.3199 | 0.5168 |
| **Fine-tuned translate-pivot** | **0.3404** | **0.4155** | **0.6073** |

### Improvement (fine-tuned vs base)

- English EM: +0.1489
- English F1: +0.1365
- English Sim: +0.0855
- BEM EM: +0.1489
- BEM F1: +0.0956
- BEM Sim: +0.0905

## Sample Predictions

### 99
- **Question:** Nani walembele ubuuku lya mubaibolo ilya kusokolola?
- **Gold (bem):** Yohane
- **Gold (EN):** John
- **Fine-tuned (EN):** John (sim=1.000)
- **Fine-tuned (bem):** Yohane (sim=1.000)
- **Base (EN):** Second-century Christian writers such as Papias of Hierapolis, Justin Martyr, Irenaeus, Melito of Sardis, Clement of Alexandria, and the author of the Muratorian fragment of John the Apostle as the 'John' of Revelation. (sim=0.161)
- **Base (bem):** Abalembele Baibolo aba mu myaka ya ba 200 pamo nga Papias uwa ku Hierapolis, Justin Martyr, Irenaeus, Melito uwa ku Sardis, Clement uwa ku Alexandria, e lyo na Yohane Umutumwa uo baleita ukuti 'Yohane' uwa mu Ukusokolola, e walembele icitabo ca Muratorian. (sim=0.216)

### 214
- **Question:** Bushe ukulingana na FIFA ranking Tanzania yaba pa namba shani mu afrika?
- **Gold (bem):** 90th
- **Gold (EN):** 90th
- **Fine-tuned (EN):** 90th (sim=1.000)
- **Fine-tuned (bem):** 90th (sim=1.000)
- **Base (EN):** NOT_FOUND (sim=0.343)
- **Base (bem):** TWABULWA (sim=0.249)

### 224
- **Question:** Bushe miku inga icalo ca Nigeria casendepo icikombe ca Afrika cup?
- **Gold (bem):** katatu
- **Gold (EN):** three times
- **Fine-tuned (EN):** four times (sim=0.831)
- **Fine-tuned (bem):** imiku ine (sim=0.425)
- **Base (EN):** Nigeria wore the Africa Cup of Nations 4 times. (sim=0.286)
- **Base (bem):** Nigeria yaliba ne nkombe ya Africa Nations pa miku 4. (sim=0.182)

### 87
- **Question:** Bushe lunshi ekala inshiku shinga?
- **Gold (bem):** Inshiku shibili ukufika kuli shine
- **Gold (EN):** Two to four days
- **Fine-tuned (EN):** about two weeks (sim=0.581)
- **Fine-tuned (bem):** pa milungu ibili (sim=0.080)
- **Base (EN):** NOT FOUND (sim=0.239)
- **Base (bem):** TWALISHILA (sim=-0.047)

### 213
- **Question:** Bushe kakansha wa mupila uwe bumba lya Realmadrid nani?
- **Gold (bem):** Carlo Ancelotti
- **Gold (EN):** Carlo Ancelotti
- **Fine-tuned (EN):** Carlo Ancelotti (sim=1.000)
- **Fine-tuned (bem):** Ba Carlo Ancelotti (sim=0.951)
- **Base (EN):** Carlo Ancelotti (sim=1.000)
- **Base (bem):** Ba Carlo Ancelotti (sim=0.951)

### 39
- **Question:** Bushe Kateya wamupila Leon Messi afuma ku caalo nshi?
- **Gold (bem):** Argentina
- **Gold (EN):** Argentina
- **Fine-tuned (EN):** Argentina (sim=1.000)
- **Fine-tuned (bem):** Argentina (sim=1.000)
- **Base (EN):** Argentina (sim=1.000)
- **Base (bem):** Argentina (sim=1.000)

### 196
- **Question:** Nani kakansha we bumba lya mupila ilya calo ca Dennmark?
- **Gold (bem):** Kasper Hjulmand
- **Gold (EN):** Kasper Hjulmand
- **Fine-tuned (EN):** Kasper Hjulmand (sim=1.000)
- **Fine-tuned (bem):** Kasper Hjulmand (sim=1.000)
- **Base (EN):** Kasper Hjulmand (sim=1.000)
- **Base (bem):** Kasper Hjulmand (sim=1.000)

### 88
- **Question:** Bushe pakutendeka ifibanda fyali ni ba malaika bakwa Lesa?
- **Gold (bem):** Ee
- **Gold (EN):** Yes, it is
- **Fine-tuned (EN):** The sons of God (sim=0.275)
- **Fine-tuned (bem):** Abana ba kwa Lesa (sim=0.163)
- **Base (EN):** Yes (sim=0.775)
- **Base (bem):** Ee, nalimutemwa (sim=0.454)

### 217
- **Question:** Bushe icalo ca zambia cakwata ama boma yanga?
- **Gold (bem):** 116
- **Gold (EN):** 116 The first
- **Fine-tuned (EN):** 116 (sim=0.835)
- **Fine-tuned (bem):** 116 (sim=1.000)
- **Base (EN):** 116 (sim=0.835)
- **Base (bem):** 116 (sim=1.000)

### 181
- **Question:** Bushe ninani walashikwa bu minister mu ciputulwa cisopa umutende mu zambia?
- **Gold (bem):** Grey Zulu
- **Gold (EN):** Grey Blue
- **Fine-tuned (EN):** Kenneth Kaunda (sim=0.144)
- **Fine-tuned (bem):** Kenneth Kaunda (sim=0.110)
- **Base (EN):** NOT FOUND (sim=0.234)
- **Base (bem):** TWALISHILA (sim=0.195)
