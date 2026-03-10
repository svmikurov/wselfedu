"""Abstract base class for factories."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

DTOType = TypeVar('DTOType')


class DTOFactory(ABC, Generic[DTOType]):
    """Result DTO factory."""

    @abstractmethod
    def create(self, **kwargs: object) -> DTOType:
        """Create result DTO."""
