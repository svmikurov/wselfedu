"""Abstract base classes for core views."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

ResultT = TypeVar('ResultT')


class AbstractStartAction(ABC, Generic[ResultT]):
    """ABC for start action."""

    @abstractmethod
    def _start(self, **kwargs: object) -> ResultT:
        """Provide start action result."""


class AbstractProcessAction(ABC, Generic[ResultT]):
    """ABC for process action."""

    @abstractmethod
    def _process(self, **kwargs: object) -> ResultT:
        """Provide process action result."""
