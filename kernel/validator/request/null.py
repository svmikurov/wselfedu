"""Null validator implementation."""

from typing import TypeVar

from ports.abstract.validator import AbstractRequestValidator
from ports.interfaces.protocols.web import RequestDataProtocol

Validated = TypeVar('Validated')


class NullValidator(AbstractRequestValidator[RequestDataProtocol, Validated]):  # type: ignore
    """Validator that returns input unchanged.

    Implements Null Object Pattern for cases
    where validation is not needed.
    """

    @classmethod
    def validate(cls, data: RequestDataProtocol) -> Validated:  # type: ignore
        """Return raw_data without validation.

        Args:
            data: Input data to pass through

        Returns:
            Same data, cast to Validated type

        """
        return data  # type: ignore
