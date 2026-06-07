"""File operations."""

import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    """Load JSON from path."""
    return json.loads(path.read_text(encoding='utf-8'))
