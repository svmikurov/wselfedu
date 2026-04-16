"""Abstract base class for domains."""

from abc import ABC, abstractmethod
from typing import TypeVar, override

from apps.core.contracts.infra.factory import FactoryProtocol

SpecT = TypeVar('SpecT')
ResultT = TypeVar('ResultT')


class AbstractFactory(ABC, FactoryProtocol[SpecT, ResultT]):
    """ABC for factory."""

    @override
    @abstractmethod
    def build(self, spec: SpecT) -> ResultT:
        """Build repository query result DTO."""
