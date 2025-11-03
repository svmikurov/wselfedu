"""Abstract base classes for Language discipline."""

from abc import ABC, abstractmethod

from apps.users.models import CustomUser

from ..types import WordParamsType, WordStudyParams, WordType


class WordStudyRepositoryABC(ABC):
    """ABC for word study repository."""

    @abstractmethod
    def get_candidates(self, params: WordParamsType) -> WordStudyParams:
        """Get candidates of words to study."""

    @abstractmethod
    def get_case(self, english_word_id: int, user: CustomUser) -> WordType:
        """Get items for exercise case."""


class WordStudyParamsRepositoryABC(ABC):
    """ABC for Word study params repository."""

    @abstractmethod
    def fetch_initial(self, user: CustomUser) -> WordParamsType:
        """Fetch initial params."""
