"""Abstract base classes for Language app domain logic."""

from abc import ABC, abstractmethod

from .. import types


class WordStudyDomainABC(ABC):
    """Word study Presentation domain logic."""

    @abstractmethod
    def create(self, params: types.WordStudyParameters) -> types.WordStudyCase:
        """Create Word study Presentation case."""
