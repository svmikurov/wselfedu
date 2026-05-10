"""Abstract base class for request validator."""

from abc import ABC, abstractmethod
from typing import TypeVar, override

from ports.contract.infra.validator import RequestValidatorProtocol

RequestDataT = TypeVar('RequestDataT')
ValidatedT = TypeVar('ValidatedT')


class AbstractRequestValidator(
    ABC,
    RequestValidatorProtocol[RequestDataT, ValidatedT],
):
    """ABC for request validator."""

    @override
    @abstractmethod
    def validate(self, data: RequestDataT) -> ValidatedT:
        """Validate request data."""
