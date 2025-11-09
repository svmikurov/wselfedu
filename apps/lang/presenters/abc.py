"""Abstract base classes for Language discipline app."""

from abc import ABC, abstractmethod

from apps.users.models import CustomUser

from ..types import WordParamsType


class WordStudyParamsPresenterABC(ABC):
    """ABC for Word study params presenter."""

    @abstractmethod
    def get_initial(self, user: CustomUser) -> WordParamsType:
        """Get Word study initial params."""
