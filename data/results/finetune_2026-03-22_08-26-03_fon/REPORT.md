# Fine-Tuning Evaluation Report — FON
**Run:** finetune_2026-03-22_08-26-03_fon
**Test samples:** 57
**Language:** fon

## Results Summary

### English-Side Metrics (isolates QA model quality)

| Pipeline | EM | F1 | Semantic Sim |
|----------|----|----|--------------|
| Base translate-pivot | 0.1930 | 0.2631 | 0.4481 |
| **Fine-tuned translate-pivot** | **0.1754** | **0.3155** | **0.5503** |

### FON-Side Metrics (end-to-end performance)

| Pipeline | EM | F1 | Semantic Sim |
|----------|----|----|--------------|
| Base translate-pivot | 0.1579 | 0.1840 | 0.4089 |
| **Fine-tuned translate-pivot** | **0.1228** | **0.2033** | **0.4723** |

### Improvement (fine-tuned vs base)

- English EM: -0.0176
- English F1: +0.0524
- English Sim: +0.1022
- FON EM: -0.0351
- FON F1: +0.0193
- FON Sim: +0.0634

## Sample Predictions

### 151
- **Question:** E tɛ nyí "assemblée monocamérale" ?
- **Gold (fon):** système parlementaire e ɖo xɔ̀ ɖokpo
- **Gold (EN):** a parliamentary system in one chamber
- **Fine-tuned (EN):** unicameral (sim=0.459)
- **Fine-tuned (fon):** kpò ɖokpó (sim=0.192)
- **Base (EN):** Monocameralism (sim=0.489)
- **Base (fon):** Monocameralism (sim=0.421)

### 93
- **Question:** E tɛ nyĭ Polio?
- **Gold (fon):** azɔn é nɔn jεmεjí ɖo poliovirus wú
- **Gold (EN):** the disease was caused by poliovirus
- **Fine-tuned (EN):** a virus that causes paralysis (sim=0.582)
- **Fine-tuned (fon):** azɔnkwín ɖé e nɔ dɔn nǔkwɛ́n (sim=0.174)
- **Base (EN):** Polio is an acute and infectious disease caused by poliovirus, transmitted through the digestive tract. It affects humans and can lead to paralysis, with a potential for life-threatening conditions affecting the respiratory tract. Treatment involves managing spinal cord injury. (sim=0.589)
- **Base (fon):** Polio ɔ nyí azɔn kpinkpɛn ɖé bɔ è nɔ hɛn azɔn dó mɛ bɔ è nɔ hɛn ɔ è nɔ hɛn ɔ è nɔ hɛn azɔn dó mɛ, bɔ è nɔ hɛn ɔ è nɔ hɛn azɔn dó mɛ, bɔ è nɔ hɛn ɔ è nɔ hɛn azɔn dó mɛ. (sim=0.349)

### 225
- **Question:** Tò tɛ ɖo Aksoum sín ayìkúngban xóxó ɔ jí ?
- **Gold (fon):** Éthiopie, Djibouti kpódó Érythrée kpán
- **Gold (EN):** Ethiopia, Djibouti and Eritrea
- **Fine-tuned (EN):** ethiopia (sim=0.592)
- **Fine-tuned (fon):** etiopii (sim=0.507)
- **Base (EN):** Ethiopia (sim=0.654)
- **Base (fon):** Etiopía (sim=0.659)

### 231
- **Question:** Hwe tɛ nu Allemagne nɔ̀n ɖù tó xwe tɔ̀n ?
- **Gold (fon):** azǎn atɔn gɔ kɔnyasùn tɔn
- **Gold (EN):** three days of full moon
- **Fine-tuned (EN):** 3 october (sim=0.399)
- **Fine-tuned (fon):** azǎn 3 ɔ́tógbò (sim=0.606)
- **Base (EN):** 3 October (sim=0.411)
- **Base (fon):** 3 octobre (sim=0.302)

### 162
- **Question:** Nɛ̌ ahwan Algerie tɔ̀n vɔ̀ gbɔn ɖŏ 1962 ?
- **Gold (fon):** mεɖésúsínínɔ glegbεtá tɔn
- **Gold (EN):** the selfless man of the field
- **Fine-tuned (EN):** the independence of the territory on 5 July 1962 (sim=0.357)
- **Fine-tuned (fon):** tuto e nɔ nyí to ɔ tɔn ɖò 5 juillet 1962 é (sim=0.207)
- **Base (EN):** The Algerian War ended on 5 July 1962 with the recognition of the independence of the territory. (sim=0.217)
- **Base (fon):** Akpa Algeji tɔn ɔ fó ɖò 5 juillet 1962 hwenu è tuùn tuto tɔn. (sim=0.187)

### 165
- **Question:** Nɛ̌ Archevêque archidiocèse Ouagadougou tɔ́n yɔyɔ ɔ́ nɔ̀n nyi ?
- **Gold (fon):** Compaoré
- **Gold (EN):** compared
- **Fine-tuned (EN):** Jean-Marie Untaani Compaoré (sim=0.140)
- **Fine-tuned (fon):** Jean-Marie Untaani Compaoré (sim=0.353)
- **Base (EN):** NOT FOUND (sim=0.325)
- **Base (fon):** È ma mɔ ǎ (sim=0.245)

### 217
- **Question:** Tó tɛ blŏ protectorat ?
- **Gold (fon):** France
- **Gold (EN):** France
- **Fine-tuned (EN):** the Holy Empire (sim=0.315)
- **Fine-tuned (fon):** Axɔsuɖuto mímɛ́ ɔ (sim=0.117)
- **Base (EN):** France (sim=1.000)
- **Base (fon):** Fransi (sim=0.786)

### 76
- **Question:** Mɛ nyĭ pop jí tɔ ɖaxó gbɛ ɔ mɛ tɔ̀n ?
- **Gold (fon):** Michael Jackson
- **Gold (EN):** Michael Jackson
- **Fine-tuned (EN):** michael jackson (sim=0.961)
- **Fine-tuned (fon):** Michael Jackson (sim=1.000)
- **Base (EN):** Michael Jackson (sim=1.000)
- **Base (fon):** Michael Jackson (sim=1.000)

### 145
- **Question:** Mɛ nyi Pipi Wobaho ?
- **Gold (fon):** hanjitɔ́‚ manahὲn e go sín Bénin
- **Gold (EN):** singer from Benin
- **Fine-tuned (EN):** a comedian (sim=0.390)
- **Fine-tuned (fon):** nùɖíɖóɖókpɔ́ (sim=0.219)
- **Base (EN):** Pipi Wobaho is a comedian, singer of traditional music from Benin. He is a founding member of the company of theatre and cinema Sèmako Wobaho. Simplice Behanzin. (sim=0.421)
- **Base (fon):** Pipi Wobaho nyí mɛɖemaɖɔ, mɛɖemaɖɔ sinsɛngbɛ́ sín Benín tɔn ɖé. É nyí mɛ e ɖó nukɔn nú wemaxɔmɛ kpo sinsɛngbɛ́ kpo sín to ɔ́ mɛ̀ é. (sim=0.393)

### 20
- **Question:** É tɛ nyi xɔgbonú Benε tɔn ?
- **Gold (fon):** Porto-Novo
- **Gold (EN):** Porto-Novo
- **Fine-tuned (EN):** the bonnese republic (sim=0.278)
- **Fine-tuned (fon):** Bonnese tɔn (sim=0.332)
- **Base (EN):** NOT_FOUND (sim=0.424)
- **Base (fon):** E HWƐN (sim=0.259)
