"""Abstract base classes for Language discipline services."""

from abc import ABC, abstractmethod

from ..types import WordStudyCase, WordStudyParams


class WordStudyServiceABC(ABC):
    """Word study service to create task case."""

    @abstractmethod
    def create(self, params: WordStudyParams) -> WordStudyCase:
        """Create word study task case."""
