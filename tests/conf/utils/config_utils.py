"""Defines test configuration utils."""

from pathlib import Path
from typing import Any

import yaml

CONFIG_DIR = Path(__file__).resolve().parents[1]
CONFIG_PATH = CONFIG_DIR / 'test_config.yml'


def load_config(config_path: Path | None = None) -> dict[str, Any]:
    """Load the test configuration."""
    file_path = config_path if config_path is not None else CONFIG_PATH
    with open(file_path, 'r', encoding='utf-8') as f:
        data: dict[str, Any] = yaml.safe_load(f)
        return data
