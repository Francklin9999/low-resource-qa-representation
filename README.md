# Multilingual QA Bench

**Benchmarking Large Language Models on Extractive Question Answering for Low-Resource African Languages**

[![Paper](https://img.shields.io/badge/Paper-PDF-b31b1b.svg)](paper/Franck_Fongang_Low_Resource_QA_Translation.pdf)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)

📄 **[Read the paper (PDF)](paper/Franck_Fongang_Low_Resource_QA_Translation.pdf)** — full methodology, results, and analysis.

## Motivation

Large language models achieve remarkable performance on English NLP tasks, yet their capabilities on low-resource languages remain understudied. For many African languages, there is an open question: should we query LLMs *directly* in the target language, or *translate* to English first, query the LLM, and translate the answer back? This project provides an empirical answer by systematically benchmarking both strategies across 10 African languages, 5 model families, and a locally fine-tuned model.

## Research Questions

1. **Direct vs. translate-pivot**: For a given LLM, does querying directly in the source language outperform translating to English and back?
2. **Model scale vs. specialization**: Can a small, fine-tuned model (Qwen2.5-3B with QLoRA) compete with frontier API models (GPT-5.3, Claude Opus 4.5, Gemini 2.5 Pro)?
3. **Language resource level**: How does performance vary across languages with different levels of representation in pretraining data?

## Experimental Setup

### Dataset

We use [AfriQA](https://github.com/masakhane-io/afriqa) (Ogundepo et al., 2023), a cross-lingual open-retrieval QA dataset for 10 African languages. Each example contains a question, a gold Wikipedia passage (context), and a reference answer in the source language.

### Languages

| Code | Language     | Family         | Pivot | Test Samples |
|------|-------------|----------------|-------|:------------:|
| hau  | Hausa       | Afro-Asiatic   | en    | 45           |
| yor  | Yoruba      | Niger-Congo    | en    | 51           |
| ibo  | Igbo        | Niger-Congo    | en    | 62           |
| swa  | Swahili     | Niger-Congo    | en    | --           |
| kin  | Kinyarwanda | Niger-Congo    | en    | 44           |
| twi  | Twi         | Niger-Congo    | en    | 71           |
| wol  | Wolof       | Niger-Congo    | fr    | --           |
| zul  | Zulu        | Niger-Congo    | en    | 49           |
| bem  | Bemba       | Niger-Congo    | en    | 47           |
| fon  | Fon         | Niger-Congo    | fr    | 57           |

Wolof and Fon use French as the pivot language due to stronger NLLB-200 translation quality through French.

### Pipelines

Each model is evaluated under two conditions:

- **Direct**: The question and gold passage are provided in the source language. The LLM responds in the source language. Evaluation is computed against the source-language reference answer.
- **Translate-pivot**: The question and context are machine-translated to English (or French) via [NLLB-200-distilled-600M](https://huggingface.co/facebook/nllb-200-distilled-600M). The LLM answers in English. The answer is translated back to the source language. Metrics are computed on both the English-side (against a translated reference) and source-side (against the original reference).

### Models Evaluated

| Model | Type | Parameters | Access |
|-------|------|:----------:|--------|
| GPT-5.3 | Frontier API | -- | OpenAI API |
| Claude Opus 4.5 | Frontier API | -- | Anthropic API |
| Claude Sonnet 4.5 (thinking) | Frontier API | -- | Anthropic API |
| Gemini 2.5 Pro | Frontier API | -- | Google API |
| Aya-23-8B | Multilingual baseline | 8B | Local (4-bit) |
| Qwen2.5-3B + QLoRA | Fine-tuned | 3B | Local (4-bit) |
| mT5-large | Seq2seq baseline | 1.2B | Local |

### Metrics

| Metric | Description |
|--------|-------------|
| **Exact Match (EM)** | 1.0 if the normalized prediction exactly equals the gold answer, else 0.0 |
| **F1** | Token-level precision/recall harmonic mean (SQuAD-style) |
| **Semantic Similarity** | Cosine similarity of [LaBSE](https://huggingface.co/sentence-transformers/LaBSE) embeddings (language-agnostic) |

## Results

### Frontier API Models -- Direct Pipeline (Source-Side)

The direct pipeline consistently outperforms translate-pivot for all frontier models. Below are source-side metrics for the direct pipeline:

| Model | Hausa (EM/F1/Sim) | Igbo (EM/F1/Sim) | Yoruba (EM/F1/Sim) | Bemba (EM/F1/Sim) |
|-------|:-----------------:|:-----------------:|:------------------:|:-----------------:|
| **GPT-5.3** | .51 / .59 / .74 | **.56** / **.73** / **.87** | .37 / .57 / .78 | .45 / .47 / .68 |
| **Opus 4.5** | .47 / .50 / .69 | .53 / .67 / .84 | .39 / .55 / .78 | **.49** / **.53** / .67 |
| **Sonnet 4.5** | .40 / .49 / .70 | .52 / .69 / .85 | **.43** / .56 / .78 | .34 / .39 / .60 |
| **Gemini 2.5 Pro** | .40 / .48 / .69 | .47 / .64 / .79 | .31 / .45 / .68 | **.51** / .53 / **.67** |

**Key finding**: Direct querying is superior to translate-pivot for frontier models. The translation round-trip introduces compounding errors -- particularly on the return translation -- that degrade both exact match and semantic similarity. GPT-5.3 leads on Igbo (0.56 EM), while the models are more competitive on other languages.

### Direct vs. Translate-Pivot Gap

Averaging across all 8 evaluated languages, the translate-pivot pipeline drops performance by:

| Model | EM Drop | F1 Drop | Sim Drop |
|-------|:-------:|:-------:|:--------:|
| GPT-5.3 | -0.23 | -0.14 | -0.13 |
| Opus 4.5 | -0.24 | -0.15 | -0.11 |
| Sonnet 4.5 | -0.21 | -0.13 | -0.11 |
| Gemini 2.5 Pro | -0.19 | -0.10 | -0.10 |

The EM penalty is steepest because even minor translation artifacts break exact string matches.

### Fine-Tuned Qwen2.5-3B vs. Baselines (English-Side EM)

The QLoRA-adapted Qwen2.5-3B model operates via the translate-pivot pipeline (it answers in English). Compared against its own base model and the Aya-23-8B baseline:

| Language | Qwen2.5 QLoRA | Qwen2.5 Base (translate) | Aya-23-8B (translate) | Aya-23-8B (direct) |
|----------|:-------------:|:------------------------:|:---------------------:|:-------------------:|
| Hausa    | **.378**      | .289                     | .289                  | .156                |
| Yoruba   | **.314**      | .137                     | .255                  | .216                |
| Igbo     | .339          | .323                     | **.355**              | .226                |
| Bemba    | **.319**      | .170                     | .213                  | .191                |
| Zulu     | **.429**      | .286                     | .306                  | .082                |
| Twi      | .268          | .225                     | **.282**              | .225                |
| Kinyarwanda | **.136**   | .114                     | .182                  | .068                |
| Fon      | .175          | **.193**                  | **.193**              | .053                |

**Key finding**: The QLoRA fine-tuned 3B model outperforms both its own base model and the 2.7x larger Aya-23-8B on 5 out of 8 languages. The largest gains appear on Hausa (+8.9pp over base), Yoruba (+17.6pp), Bemba (+14.9pp), and Zulu (+14.3pp). This demonstrates that language-specific fine-tuning with translated data and round-trip augmentation can compensate for scale.

### mT5-large Baseline

mT5-large scored near zero across all languages and pipelines (EM = 0.00 for all), confirming that encoder-decoder models pretrained on span corruption are not suited for extractive QA without task-specific fine-tuning.

### Semantic Similarity Across Pipelines (Fine-Tuned Qwen2.5-3B)

Even when exact match is low, semantic similarity reveals whether the model captures the right meaning:

| Language | QLoRA (Eng-Side Sim) | Base (Eng-Side Sim) | Delta |
|----------|:--------------------:|:-------------------:|:-----:|
| Hausa    | .788                 | .606                | +.182 |
| Yoruba   | .750                 | .600                | +.150 |
| Zulu     | .776                 | .635                | +.141 |
| Twi      | .732                 | .609                | +.123 |
| Bemba    | .661                 | .576                | +.085 |
| Kinyarwanda | .618              | .529                | +.089 |

The fine-tuned model produces semantically closer answers across all languages, with the largest improvement on Hausa (+0.18).

## Architecture

```
                         configs/
                     (languages.yaml,
                      finetune.yaml,
                      benchmark.yaml)
                            |
                            v
    +-----------------------------------------------+
    |               data/downloader.py              |
    |  Download AfriQA dataset + gold passages      |
    +-----------------------------------------------+
            |                           |
            v                           v
    data/raw/                    data/processed/
    (raw JSONL)                  (filtered JSON)
            |
            v
    +-----------------------------------------------+
    |          EXPERIMENT PIPELINE (main.py)         |
    |                                                |
    |  For each (provider, model, language):         |
    |                                                |
    |  Pipeline 1: DIRECT                            |
    |    question (src lang) -> LLM -> answer        |
    |                                                |
    |  Pipeline 2: TRANSLATE-PIVOT                   |
    |    question -> NLLB translate -> English       |
    |    English question -> LLM -> English answer   |
    |    English answer -> NLLB translate -> src     |
    |                                                |
    |  Evaluate: EM, F1, Semantic Similarity (LaBSE) |
    +-----------------------------------------------+
            |
            v
    data/results/
    (JSON + markdown reports)

    +-----------------------------------------------+
    |     FINE-TUNING PIPELINE (run_finetune.py)     |
    |                                                |
    |  Step 1: PREPARE                               |
    |    Load data with context -> split (70/10/20)  |
    |    -> translate to English -> validate (LaBSE) |
    |                                                |
    |  Step 2: BUILD                                 |
    |    Mix: translated QA + English QA + augmented |
    |    Format as instruction-tuning prompts        |
    |                                                |
    |  Step 3: TRAIN                                 |
    |    QLoRA fine-tune Qwen2.5-3B (4-bit NF4)     |
    |                                                |
    |  Step 4: EVALUATE                              |
    |    Base model vs fine-tuned on held-out test   |
    |    Compute EM / F1 / semantic similarity       |
    +-----------------------------------------------+
            |
            v
    data/training/          data/results/
    (splits, adapters)      (metrics, REPORT.md)
```

## Project Structure

```
multilingual/
├── main.py                      # CLI entry point for API experiments
├── paths.py                     # Centralized path constants
├── configs/
│   ├── benchmark.yaml           # API models to benchmark
│   ├── finetune.yaml            # Fine-tuning hyperparameters
│   ├── languages.yaml           # Supported languages + AfriQA URLs
│   ├── models.yaml              # NLLB codes, embeddings, base model
│   └── prompts.yaml             # Prompt templates (standard/context/finetune)
├── src/
│   ├── translate.py             # NLLB-200 translation (batch, pivot support)
│   ├── evaluate.py              # Metrics: EM, F1, LaBSE semantic similarity
│   ├── experiment/
│   │   ├── standard.py          # Direct + translate-pivot experiment runner
│   │   ├── context.py           # Context-enriched (gold passage) experiments
│   │   ├── finetune.py          # Fine-tuned model evaluation
│   │   ├── summary.py           # Markdown summary table generator
│   │   └── common.py            # Shared experiment utilities
│   ├── finetune/
│   │   ├── prepare.py           # Data prep: split, translate, quality filter
│   │   ├── dataset.py           # Training set: mix, augment, format prompts
│   │   ├── train.py             # QLoRA training (peft + trl)
│   │   ├── inference.py         # Fine-tuned adapter inference
│   │   ├── aya_baseline.py      # Aya-23-8B baseline (4-bit)
│   │   └── gpu.py               # GPU memory management
│   └── llm/
│       ├── base.py              # Abstract LLM provider
│       ├── registry.py          # Decorator-based provider registry
│       └── providers/           # Per-provider implementations
├── data/
│   ├── downloader.py            # AfriQA dataset fetcher
│   ├── raw/                     # Raw JSONL (git-ignored)
│   ├── processed/               # Cleaned JSON (git-ignored)
│   ├── training/                # Splits + checkpoints (git-ignored)
│   └── results/                 # Experiment outputs (git-ignored)
├── scripts/
│   ├── run_finetune.py          # Fine-tuning pipeline orchestrator
│   ├── run_benchmark.py         # Multi-model benchmark runner
│   ├── analyze.py               # Results visualization
│   └── summarize.py             # Summary table generation
├── utils/
│   ├── __init__.py              # Config + JSONL loaders
│   └── prompts.py               # Prompt template loader
└── pyproject.toml               # Dependencies (Python 3.13+, uv)
```

## Setup

### Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) package manager
- GPU with 6+ GB VRAM (for fine-tuning and local inference)

### Installation

```bash
git clone https://github.com/Francklin9999/low-resource-qa-representation.git
cd low-resource-qa-representation

# Core dependencies
uv sync

# Fine-tuning (requires GPU)
uv sync --extra training

# Analysis and plotting
uv sync --extra analysis
```

### API Keys

```bash
cp .env.example .env
```

| Provider   | Environment Variable   |
|------------|------------------------|
| Anthropic  | `ANTHROPIC_API_KEY`    |
| OpenAI     | `OPENAI_API_KEY`       |
| Google     | `GOOGLE_API_KEY`       |

## Usage

### Data Download

```bash
# All languages
uv run python -m data.downloader

# Specific language with gold passages
uv run python -m data.downloader --lang hau --with-context
```

### API Benchmarking

```bash
# Run with context (gold passage)
uv run python main.py --provider anthropic --model claude-opus-4-5-20251101 --lang hau yor ibo --context

# All configured models
uv run python scripts/run_benchmark.py --lang hau yor ibo bem zul twi kin fon
```

### Fine-Tuning

```bash
# Full pipeline for a language
uv run python scripts/run_finetune.py all --lang hau

# Individual steps
uv run python scripts/run_finetune.py prepare --lang hau
uv run python scripts/run_finetune.py build
uv run python scripts/run_finetune.py train
uv run python scripts/run_finetune.py evaluate
```

See [FINETUNE.md](FINETUNE.md) for the full fine-tuning guide.

### Analysis

```bash
uv run python scripts/summarize.py
uv run python scripts/analyze.py --plot
```

## Key Takeaways

1. **Direct wins over translate-pivot for frontier models.** The translation round-trip consistently degrades all three metrics, with EM suffering the most (up to -0.24 pp average drop). Frontier LLMs have internalized enough multilingual signal to answer directly in Hausa, Igbo, Yoruba, and other African languages.

2. **Fine-tuning closes the gap at 100x fewer parameters.** A 3B QLoRA model trained on translated AfriQA data with round-trip augmentation outperforms Aya-23-8B (2.7x larger) on most languages and approaches frontier API models on English-side metrics -- running entirely locally on a single consumer GPU.

3. **Language resource level matters, but not uniformly.** Igbo and Hausa (relatively higher-resource among African languages) see the strongest performance across all models, while Fon and Kinyarwanda remain challenging even for frontier systems.

4. **Semantic similarity is more robust than exact match.** Even when EM is low (e.g., 0.14 for Kinyarwanda), semantic similarity of 0.62-0.67 indicates the models are generating topically relevant answers that differ in surface form.

## Adding a New Provider

```python
from src.llm.base import LLMProvider
from src.llm.registry import register

@register("my-provider")
class MyProvider(LLMProvider):
    def __init__(self, model: str, **kwargs):
        super().__init__(model)

    def ask(self, question: str, system_prompt: str = "") -> str:
        ...
```

## Citation

If you use this work, please cite the paper ([PDF](paper/Franck_Fongang_Low_Resource_QA_Translation.pdf)):

```bibtex
@misc{fongang2026lowresourceqa,
  title  = {Direct vs. Translate-Pivot: Benchmarking LLMs on Extractive Question Answering for Low-Resource African Languages},
  author = {Franck Fongang},
  year   = {2026},
  note   = {\url{https://github.com/Francklin9999/low-resource-qa-representation}}
}
```

Or cite the codebase directly:

```bibtex
@software{multilingual_qa_bench,
  title  = {Multilingual QA Bench: Benchmarking LLMs on Low-Resource Language Question Answering},
  author = {Franck Fongang},
  year   = {2026},
  url    = {https://github.com/Francklin9999/low-resource-qa-representation}
}
```

## Acknowledgments

- [AfriQA](https://github.com/masakhane-io/afriqa) (Ogundepo et al., 2023) for the multilingual QA dataset
- [NLLB-200](https://huggingface.co/facebook/nllb-200-distilled-600M) for machine translation
- [LaBSE](https://huggingface.co/sentence-transformers/LaBSE) for multilingual sentence embeddings
- [Qwen2.5](https://huggingface.co/Qwen/Qwen2.5-3B) as the base model for fine-tuning
- [Aya-23](https://huggingface.co/CohereForAI/aya-23-8B) as a multilingual baseline

## License

MIT -- see [LICENSE](LICENSE) for details.
