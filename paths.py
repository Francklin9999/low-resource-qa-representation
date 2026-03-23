"""Central path constants for the entire project."""

from pathlib import Path

# Project root
ROOT = Path(__file__).resolve().parent

# Config paths
CONFIGS_DIR = ROOT / "configs"
BENCHMARK_CONFIG = CONFIGS_DIR / "benchmark.yaml"
FINETUNE_CONFIG = CONFIGS_DIR / "finetune.yaml"
LANGUAGES_CONFIG = CONFIGS_DIR / "languages.yaml"
MODELS_CONFIG = CONFIGS_DIR / "models.yaml"
PROMPTS_CONFIG = CONFIGS_DIR / "prompts.yaml"

# Data paths
DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
TRAINING_DIR = DATA_DIR / "training"
RESULTS_DIR = DATA_DIR / "results"
