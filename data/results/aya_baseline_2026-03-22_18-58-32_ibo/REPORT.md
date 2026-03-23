# Aya-23-8B Baseline Report — IBO
**Run:** aya_baseline_2026-03-22_18-58-32_ibo
**Test samples:** 62
**Language:** ibo
**Model:** Aya-23-8B (4-bit quantized)

## Results Summary

### IBO-Side Metrics

| Pipeline | EM | F1 | Semantic Sim |
|----------|----|----|--------------|
| Aya direct (ibo) | 0.2258 | 0.3431 | 0.5174 |
| Aya translate-pivot | 0.3871 | 0.5734 | 0.7568 |

### English-Side Metrics (translate-pivot only)

| Pipeline | EM | F1 | Semantic Sim |
|----------|----|----|--------------|
| Aya translate-pivot | 0.3548 | 0.5937 | 0.7368 |

## Sample Predictions

### 163
- **Question:** Kedụ aha mba chịburu ala Naijiria tupu ọ nwere onwe ya?
- **Gold (ibo):** British
- **Aya direct:** 1960 (sim=0.338)
- **Aya pivot (EN):** Britain (sim=0.881)
- **Aya pivot (ibo):** Briten (sim=0.917)

### 256
- **Question:** Kedụ mba a ga-ahụ ndị ike pyramids nke Giza?
- **Gold (ibo):** Egypt
- **Aya direct:** 1 (sim=0.309)
- **Aya pivot (EN):** Egypt (sim=1.000)
- **Aya pivot (ibo):** Ijipt (sim=0.796)

### 300
- **Question:** Kedụ otu ndọrọ ndọrọ ọchịchị Peter Obi nọ na ya mgbe ọ bụ gọvanọ Anambra steeti?
- **Gold (ibo):** All Progressives Grand Alliance (APGA)
- **Aya direct:** Chris Ngige (sim=0.214)
- **Aya pivot (EN):**  (sim=0.129)
- **Aya pivot (ibo):** Ihe mere (sim=0.076)

### 98
- **Question:** Kedụ mba Afrịka e bu ụzọ nye nnwereonwe?
- **Gold (ibo):** Ghana
- **Aya direct:** Ghana (sim=1.000)
- **Aya pivot (EN):** NOT FOUND. (sim=0.259)
- **Aya pivot (ibo):** A Hụghị Ya. (sim=0.198)

### 25
- **Question:** Kedụ mgbe eguzobere ihe nrite Headies ?
- **Gold (ibo):** 2006
- **Aya direct:** 2006 (sim=1.000)
- **Aya pivot (EN):** The Headies awards were established in 2006. (sim=0.380)
- **Aya pivot (ibo):** E guzobere onyinye Headies na 2006. (sim=0.521)

### 222
- **Question:** Kedụ aha isi obodo mba Gabon?
- **Gold (ibo):** Libreville
- **Aya direct:** Gabon (sim=0.197)
- **Aya pivot (EN):** Libreville (sim=0.864)
- **Aya pivot (ibo):** Libreville (sim=1.000)

### 60
- **Question:** Kedụ onye mbụ meriri asọmpị nwaanyị kachara ma mma na Naịjirịa?
- **Gold (ibo):** Omasan Buwa
- **Aya direct:** Omasan Buwa (sim=1.000)
- **Aya pivot (EN):** Omasan Buwa (sim=0.869)
- **Aya pivot (ibo):** Omasan Buwa (sim=1.000)

### 219
- **Question:** Kedụ ezigbo aha Obi Cubana?
- **Gold (ibo):** Obinna "Obi" Iyiegbu
- **Aya direct:** Obinna "Obi" Iyiegbu (sim=1.000)
- **Aya pivot (EN):** Obinna "Obi" Iyiegbu (sim=0.691)
- **Aya pivot (ibo):** Obinna "Obi" Iyiegbu (sim=1.000)

### 20
- **Question:** Kedụ ụbọchị eji eme emume Valentine?
- **Gold (ibo):** Febụwarị 14
- **Aya direct:** Saint Valentine (sim=0.383)
- **Aya pivot (EN):** February 14 (sim=0.906)
- **Aya pivot (ibo):** Ụbọchị 14 Febụwarị (sim=0.935)

### 253
- **Question:** Kedu mgbe a mụrụ Obinna Nsofor?
- **Gold (ibo):** 25 Maachị 1987
- **Aya direct:** Victor Nsofor Obinna (sim=0.088)
- **Aya pivot (EN):** 25 March 1987. (sim=0.941)
- **Aya pivot (ibo):** 25 Machị 1987. (sim=0.912)
