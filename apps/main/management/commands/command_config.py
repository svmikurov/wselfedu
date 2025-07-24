"""Defines main app management command config model."""

from pathlib import Path

from pydantic import BaseModel


class MainCommandConfig(BaseModel):
    """Main app management command config model."""

    execute_scripts: list[Path]
