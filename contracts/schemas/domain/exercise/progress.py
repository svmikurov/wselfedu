"""Item study progress interface."""

from typing import Any

from pydantic import Field

from contracts.schemas.base import BaseDTO


class ProgressDTO(BaseDTO):
    """Item study progress DTO."""

    value: int = Field(
        description='Item study current progress value',
    )
    update_url: str = Field(
        description='Item study update progress url',
    )
    increment_payload: dict[str, Any] = Field(
        description='Item study increment progress payload',
    )
    decrement_payload: dict[str, Any] = Field(
        description='Item study decrement progress payload',
    )


class ProgressConfigDTO(BaseDTO):
    """Item study progress config fields."""

    increment: int = Field(
        description='Increment item study progress value',
    )
    decrement: int = Field(
        description='Decrement item study progress value',
    )
