"""Null validator implementation."""

from typing import Any, TypeVar

from .abstract import AbstractRegularValidator

Validated = TypeVar('Validated')


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
