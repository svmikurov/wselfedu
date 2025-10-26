"""Abstract base classes for Language discipline app."""

from abc import ABC, abstractmethod
from typing import TypedDict, override

from apps.core.presenters.abc import StudyPresenterGenABC
from apps.users.models import CustomUser

from ..types import WordParamsType, WordType

# Types
# -----


class WordStudyInitialParamsType(TypedDict):
    """Word study initial params field types."""

    marks: list[dict[int, str]]


# ABC
# ---


class WordStudyPresenterABC(
    StudyPresenterGenABC[WordParamsType, WordType],
    ABC,
):
    """ABC fore Word study presenter."""

    @abstractmethod
    @override
    def get_presentation(
        self,
        params: WordParamsType,
        user: CustomUser,
    ) -> WordType:
        """Get Word study presentation case."""


class WordStudyParamsPresenterABC(ABC):
    """ABC for Word study params presenter."""

    @abstractmethod
    def get_initial(self) -> WordStudyInitialParamsType:
        """Get Word study initial params."""
