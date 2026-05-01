"""Abstract base class for request validator."""

from abc import ABC, abstractmethod
from typing import TypeVar, override

from .protocol import RequestValidatorProtocol

RequestDataT = TypeVar('RequestDataT')
ValidatedT = TypeVar('ValidatedT')


class AbstractRequestValidator(
    ABC,
    RequestValidatorProtocol[RequestDataT, ValidatedT],
):
    """ABC for request validator."""

    def __init__(
        self,
        name: str | None = None,
    ) -> None:
        """Construct the validator."""
        self._name = name or 'undefined'

    @override
    @abstractmethod
    def validate(self, data: RequestDataT) -> ValidatedT:
        """Validate request data."""

    @property
    def name(self) -> str:
        """Return validator name."""
        return self._name
