"""Null validator implementation."""

from typing import Any, TypeVar

from pydantic import BaseModel

from .abstract import AbstractRegularValidator

Validated = TypeVar('Validated')


class NullValidated(BaseModel):
    """Nul validated data."""


class NullValidator(AbstractRegularValidator[Validated]):
    """Validator that returns input unchanged.

    Implements Null Object Pattern for cases
    where validation is not needed.
    """

    @classmethod
    def validate(cls, raw_data: dict[str, Any]) -> Validated:
        """Return raw_data without validation.

        Args:
            raw_data: Input data to pass through

        Returns:
            Same data, cast to Validated type

        """
        return raw_data  # type: ignore
