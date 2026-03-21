"""Abstract base class for domains."""

from abc import ABC, abstractmethod
from typing import TypeVar, override

from .protocol import DTOFactoryProtocol

Data = TypeVar('Data')
DTO = TypeVar('DTO')


class AbstractDTOFactory(ABC, DTOFactoryProtocol[Data, DTO]):
    """ABC for DTO factory."""

    @override
    @abstractmethod
    def build(self, data: Data) -> DTO:
        """Build repository query result DTO."""
