"""Abstract base classes for response adapter."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

DomainType = TypeVar('DomainType')
ResponseType = TypeVar('ResponseType')


class AbstractResponseAdapter(ABC, Generic[DomainType, ResponseType]):
    """Abstract base class for response adapters."""

    @abstractmethod
    def to_response(self, schema: DomainType) -> ResponseType:
        """Convert domain schema to response representation."""
