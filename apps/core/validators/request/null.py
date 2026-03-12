"""Null validator implementation."""

from typing import TypeVar

from pydantic import BaseModel

from apps.core.handlers.protocol import RequestDataProtocol

from .abstract import AbstractRequestValidator

Validated = TypeVar('Validated')


class NullValidated(BaseModel):
    """Nul validated data."""


class NullValidator(AbstractRequestValidator[Validated]):
    """Validator that returns input unchanged.

    Implements Null Object Pattern for cases
    where validation is not needed.
    """

    @classmethod
    def validate(cls, data: RequestDataProtocol) -> Validated:
        """Return raw_data without validation.

        Args:
            data: Input data to pass through

        Returns:
            Same data, cast to Validated type

        """
        return data  # type: ignore
