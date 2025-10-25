"""Abstract base classes for Language discipline app."""

from abc import ABC, abstractmethod
from typing import override

from apps.core.presenters.abc import StudyPresenterGenABC
from apps.users.models import CustomUser

from ..types import WordParamsType, WordType


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
