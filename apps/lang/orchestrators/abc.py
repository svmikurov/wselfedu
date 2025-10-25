"""Abstract base classes for Language discipline."""

from abc import ABC, abstractmethod

from apps.users.models import CustomUser

from ..types import WordParamsType, WordStudyParams, WordType


class WordStudyOrchestratorABC(ABC):
    """ABC for word study orchestrator."""

    @abstractmethod
    def get_candidates(self, params: WordParamsType) -> WordStudyParams:
        """Get candidates of words to study."""

    @abstractmethod
    def get_case(self, english_word_id: int, user: CustomUser) -> WordType:
        """Get items for exercise case."""
