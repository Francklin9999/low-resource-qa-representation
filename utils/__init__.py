"""Shared IO and config utilities."""

import json
import logging
from pathlib import Path

import requests
import yaml

logger = logging.getLogger("mqab.utils")


def load_config(path: Path) -> dict:
    """Load a YAML config file."""
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_jsonl(path: Path | str) -> list[dict]:
    """Load a JSONL file into a list of dicts."""
    data = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                data.append(json.loads(line))
    return data


def save_json(data: list[dict], path: Path) -> Path:
    """Write a list of dicts to a JSON file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return path


def save_jsonl(data: list[dict], path: Path) -> Path:
    """Save data as JSONL."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    logger.info("Saved %d samples -> %s", len(data), path)
    return path


def fetch_text(url: str) -> str:
    """Download a URL and return its text content."""
    response = requests.get(url)
    response.raise_for_status()
    return response.text
