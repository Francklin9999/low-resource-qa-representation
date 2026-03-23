# Fine-Tuning Evaluation Report — IBO
**Run:** finetune_2026-03-22_09-51-43_ibo
**Test samples:** 62
**Language:** ibo

## Results Summary

### English-Side Metrics (isolates QA model quality)

| Pipeline | EM | F1 | Semantic Sim |
|----------|----|----|--------------|
| Base translate-pivot | 0.3226 | 0.5775 | 0.7420 |
| **Fine-tuned translate-pivot** | **0.3387** | **0.5707** | **0.7695** |

### IBO-Side Metrics (end-to-end performance)

| Pipeline | EM | F1 | Semantic Sim |
|----------|----|----|--------------|
| Base translate-pivot | 0.4032 | 0.6105 | 0.7551 |
| **Fine-tuned translate-pivot** | **0.4194** | **0.6019** | **0.7934** |

### Improvement (fine-tuned vs base)

- English EM: +0.0161
- English F1: -0.0068
- English Sim: +0.0275
- IBO EM: +0.0162
- IBO F1: -0.0086
- IBO Sim: +0.0383

## Sample Predictions

### 163
- **Question:** Kedụ aha mba chịburu ala Naijiria tupu ọ nwere onwe ya?
- **Gold (ibo):** British
- **Gold (EN):** British
- **Fine-tuned (EN):** The United Kingdom (sim=0.723)
- **Fine-tuned (ibo):** United Kingdom (sim=0.724)
- **Base (EN):** The Royal Niger Company (sim=0.183)
- **Base (ibo):** Ụlọ Ọrụ Royal Niger (sim=0.178)

### 256
- **Question:** Kedụ mba a ga-ahụ ndị ike pyramids nke Giza?
- **Gold (ibo):** Egypt
- **Gold (EN):** Egypt
- **Fine-tuned (EN):** Egypt (sim=1.000)
- **Fine-tuned (ibo):** Ijipt (sim=0.796)
- **Base (EN):** Egypt (sim=1.000)
- **Base (ibo):** Ijipt (sim=0.796)

### 300
- **Question:** Kedụ otu ndọrọ ndọrọ ọchịchị Peter Obi nọ na ya mgbe ọ bụ gọvanọ Anambra steeti?
- **Gold (ibo):** All Progressives Grand Alliance (APGA)
- **Gold (EN):** All Progressives Grand Alliance (APGA)
- **Fine-tuned (EN):** All Progressives Grand Alliance (APGA) (sim=1.000)
- **Fine-tuned (ibo):** All Progressives Grand Alliance (APGA) (sim=1.000)
- **Base (EN):** NOT FOUND (sim=0.110)
- **Base (ibo):** A Hụghị Ya (sim=0.094)

### 98
- **Question:** Kedụ mba Afrịka e bu ụzọ nye nnwereonwe?
- **Gold (ibo):** Ghana
- **Gold (EN):** Ghana
- **Fine-tuned (EN):** Ghana (sim=1.000)
- **Fine-tuned (ibo):** Ghana (sim=1.000)
- **Base (EN):** NOT FOUND (sim=0.324)
- **Base (ibo):** A Hụghị Ya (sim=0.269)

### 25
- **Question:** Kedụ mgbe eguzobere ihe nrite Headies ?
- **Gold (ibo):** 2006
- **Gold (EN):** 2006 The following
- **Fine-tuned (EN):** 2006 (sim=0.777)
- **Fine-tuned (ibo):** 2006 (sim=1.000)
- **Base (EN):** 2006 (sim=0.777)
- **Base (ibo):** 2006 (sim=1.000)

### 222
- **Question:** Kedụ aha isi obodo mba Gabon?
- **Gold (ibo):** Libreville
- **Gold (EN):** The city of Libreville
- **Fine-tuned (EN):** Libreville (sim=0.864)
- **Fine-tuned (ibo):** Libreville (sim=1.000)
- **Base (EN):** Libreville (sim=0.864)
- **Base (ibo):** Libreville (sim=1.000)

### 60
- **Question:** Kedụ onye mbụ meriri asọmpị nwaanyị kachara ma mma na Naịjirịa?
- **Gold (ibo):** Omasan Buwa
- **Gold (EN):** The Omasan Buwa
- **Fine-tuned (EN):** Chuba (sim=0.332)
- **Fine-tuned (ibo):** Chuba (sim=0.481)
- **Base (EN):** Edna Park (sim=0.220)
- **Base (ibo):** Ogige Edna (sim=0.351)

### 219
- **Question:** Kedụ ezigbo aha Obi Cubana?
- **Gold (ibo):** Obinna "Obi" Iyiegbu
- **Gold (EN):** The "Heart" is Deceitful
- **Fine-tuned (EN):** Obinna "Obi" Iyiegbu (sim=0.691)
- **Fine-tuned (ibo):** Obinna "Obi" Iyiegbu (sim=1.000)
- **Base (EN):** Obinna "Obi" Iyiegbu (sim=0.691)
- **Base (ibo):** Obinna "Obi" Iyiegbu (sim=1.000)

### 20
- **Question:** Kedụ ụbọchị eji eme emume Valentine?
- **Gold (ibo):** Febụwarị 14
- **Gold (EN):** The 14th of February
- **Fine-tuned (EN):** February 14 (sim=0.906)
- **Fine-tuned (ibo):** Ụbọchị 14 Febụwarị (sim=0.935)
- **Base (EN):** February 14 (sim=0.906)
- **Base (ibo):** Ụbọchị 14 Febụwarị (sim=0.935)

### 253
- **Question:** Kedu mgbe a mụrụ Obinna Nsofor?
- **Gold (ibo):** 25 Maachị 1987
- **Gold (EN):** March 25, 1987
- **Fine-tuned (EN):** 25 March 1987 (sim=0.987)
- **Fine-tuned (ibo):** 25 Machị 1987 (sim=0.989)
- **Base (EN):** 25 March 1987 (sim=0.987)
- **Base (ibo):** 25 Machị 1987 (sim=0.989)
