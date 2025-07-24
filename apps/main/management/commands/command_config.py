"""Defines main app management command config model."""

from pathlib import Path

from pydantic import BaseModel


class MainCommandConfig(BaseModel):
    """Main app management command config model."""

    sql_execute_order: list[Path]
