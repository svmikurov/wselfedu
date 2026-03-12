"""Abstract base class for request validator."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from apps.core.handlers.protocol import RequestDataProtocol

Validated = TypeVar('Validated')


class AbstractRequestValidator(ABC, Generic[Validated]):
    """ABC for regular request validator."""

    @classmethod
    @abstractmethod
    def validate(cls, data: RequestDataProtocol) -> Validated:
        """Validate request data."""
