"""Abstract base class for request validator."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

RequestData = TypeVar('RequestData')
Validated = TypeVar('Validated')


class AbstractRequestValidator(ABC, Generic[RequestData, Validated]):
    """ABC for request validator."""

    @abstractmethod
    def validate(self, data: RequestData) -> Validated:
        """Validate request data."""
